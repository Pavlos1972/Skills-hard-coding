#!/usr/bin/env python3
"""The step driver of the client-transcript-download skill: shows ONE step at a time, refuses to skip, keeps the run on disk.

  run.py start <run> --client "First Surname" --date DD/MM/YYYY [--type first|follow-up]
  run.py next | status | preflight <run>
  run.py meeting <run> --title TEXT --started "DD/MM/YYYY, HH:MM" --length "1h 36m 2s" --via m365|zapier|chrome|paul
  run.py access <run> --purpose fetch|save --route ROUTE --result found|failed [--note TEXT]
  run.py source <run> --file FILE --route m365|zapier|chrome      bring the received transcript into the run folder
  run.py check <run>       read the transcript and check header, length and gaps
  run.py name <run>        build the derived-name .docx
  run.py receipt <run> KEY VALUE
  run.py done <run> STEP   prove the step, then show the next one

Claude runs these programs as they are and never rewrites them during a run.
"""
import argparse
import os
import shutil
import sys

import trread as tr
import wrlib as w

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
RULE = "=" * 78


def p(run, name):
    return os.path.join(run, name)


def steps():
    return w.load_json(os.path.join(w.SKILL_DIR, "steps.json"))["steps"]


def load_run(run):
    path = p(run, w.RUN)
    if not os.path.exists(path):
        w.die('This is not a run folder (no %s). Start one with: python3 %s/run.py start <run folder> --client "First Surname" --date DD/MM/YYYY' % (w.RUN, SCRIPTS), 2)
    return w.load_json(path)


def save_run(run, rj):
    w.save_json(p(run, w.RUN), rj)


def read_ref(name):
    with open(os.path.join(w.SKILL_DIR, "references", name), encoding="utf-8") as f:
        return f.read()


def expand(text, run):
    return text.replace("{scripts}", SCRIPTS).replace("{run}", run)


def current_step(rj):
    for s in steps():
        if rj["steps"].get(s["id"], {}).get("state") != "done":
            return s
    return None


def show_step(run, rj, step):
    plist = steps()
    n = [s["id"] for s in plist].index(step["id"]) + 1
    print(RULE)
    print("STEP %d of %d: %s        [%s]" % (n, len(plist), step["title"], step["id"]))
    print(RULE)
    for line in step["do"]:
        print(expand(line, run))
    for r in step.get("ref", []):
        print("\nRULES FOR THIS STEP (references/%s):\n" % r)
        print(expand(read_ref(r), run))
    print("\nPROOF NEEDED: %s" % step["proof"])
    print("WHEN DONE RUN: python3 %s/run.py done %s %s" % (SCRIPTS, run, step["id"]))
    later = [s["title"] for s in plist[n:]]
    if later:
        print("COMING LATER (titles only): " + " | ".join(later))
    print(RULE)


def preflight():
    rows = [(sys.version_info >= (3, 8), "python %d.%d is new enough" % sys.version_info[:2]),
            (w.skill_stamp() is not None, "the skill has a Last updated stamp (%s)" % (w.stamp_display(w.skill_stamp()) or "none"))]
    return all(r[0] for r in rows), rows


def _pre(run):
    import verify
    R, rj, m = verify.run_checks(run, "pre")
    return R, rj


# ------------------------------------------------------------------ the checks behind each step
def _bad(run, *groups):
    import verify
    R, _ = _pre(run)
    return [r[1] for r in R.rows if r[0] == verify.BAD and (not groups or r[3] in groups)], R


def ck_identify(run, rj):
    return _bad(run, "meeting")[0]


def ck_fetch(run, rj):
    return _bad(run, "fetch")[0]


def ck_check(run, rj):
    bad, R = _bad(run, "transcript")
    return bad or ([] if any(r[3] == "transcript" for r in R.rows) else ["the transcript has not been read: run.py source, then run.py check"])


def ck_name(run, rj):
    name = w.output_name(rj["client"]["first"], rj["client"]["surname"], rj["date"])
    if not name or not os.path.exists(p(run, os.path.join(w.OUT, name))):
        return ["the file has not been built: run.py name"]
    return _bad(run, "meeting", "fetch", "transcript", "built")[0]


def ck_save(run, rj):
    rc = w.load_opt(p(run, w.RECEIPT), {})
    out = ["run.py receipt %s <value>" % k for k in ("save.folder", "save.listed_bytes", "save.already_existed") if not rc.get(k)]
    if not any(e.get("purpose") == "save" for e in w.load_opt(p(run, w.ACCESS), [])):
        out.append("record every save try: run.py access --purpose save --route device|m365|zapier --result found|failed")
    return out


def ck_final(run, rj):
    import verify
    R, rj2, m = verify.run_checks(run, "final")
    if R.fails:
        verify.print_audit(R, rj2, "final", run)
        return ["the checker has %d red cross(es) above" % len(R.fails)]
    return []


CHECKS = {"identify_ok": ck_identify, "fetch_ok": ck_fetch, "check_ok": ck_check, "name_ok": ck_name, "save_ok": ck_save, "verify_final": ck_final}


# ------------------------------------------------------------------ commands
def cmd_start(a):
    parts = a.client.split()
    if len(parts) < 2:
        w.die('--client must be the first name and surname, for example --client "Pat Samplecase"')
    first, surname = parts[0], " ".join(parts[1:])
    if w.parse_date(a.date) is None:
        w.die("--date must be a real date as DD/MM/YYYY (the meeting date from Paul's message), got %r" % a.date)
    if os.path.exists(p(a.run, w.RUN)):
        old = load_run(a.run)
        oc = old["client"]
        if not (w.norm("%s %s" % (oc["first"], oc["surname"])) == w.norm(a.client) and old["date"] == a.date):
            w.die("REFUSED: this run folder already belongs to %s %s, %s. Use a NEW run folder for %s, %s." % (oc["first"], oc["surname"], old["date"], a.client, a.date), 2)
        print("This run already exists (same client and date). Showing where it is up to.")
        return cmd_next(a)
    ok, rows = preflight()
    print("SELF-TEST BEFORE ANYTHING ELSE:")
    for good, text in rows:
        print("  [%s] %s" % ("OK" if good else "FAIL", text))
    if not ok:
        w.die("\nSTOP. Tell Paul exactly which item failed above. Do not carry on.", 4)
    os.makedirs(os.path.join(a.run, w.OUT), exist_ok=True)
    rj = {"skill": w.skill_name(), "created": w.now(), "skill_stamp": w.skill_stamp(), "steps": {}, "client": {"first": first, "surname": surname},
          "date": a.date, "type": a.type, "program_fingerprint": w.program_fingerprint()}
    save_run(a.run, rj)
    for name, empty in ((w.ACCESS, []), (w.RECEIPT, {})):
        w.save_json(p(a.run, name), empty)
    print("\nSAY THIS TO PAUL FIRST, before anything else in your reply, in exactly these words:\n    %s.\n" % w.version_line())
    print("RUN STARTED  client: %s %s   meeting date: %s%s\n" % (first, surname, a.date, ("   meeting type: " + a.type) if a.type else ""))
    print("Standing rules for the whole job:\n")
    print(expand(read_ref("00-rules.md"), a.run))
    print()
    show_step(a.run, rj, current_step(rj))


def cmd_next(a):
    rj = load_run(a.run)
    s = current_step(rj)
    if s is None:
        print("Every step is done. Run: python3 %s/verify.py %s  and put its SHORT AUDIT in your reply (that is the whole report)." % (SCRIPTS, a.run))
        return
    show_step(a.run, rj, s)


def cmd_status(a):
    rj = load_run(a.run)
    for s in steps():
        print("  [%s] %s" % ("done" if rj["steps"].get(s["id"], {}).get("state") == "done" else "    ", s["title"]))
    cur = current_step(rj)
    print("Now: %s" % (cur["id"] if cur else "all done"))


def cmd_preflight(a):
    ok, rows = preflight()
    for good, text in rows:
        print("  [%s] %s" % ("OK" if good else "FAIL", text))
    print("PREFLIGHT: %s" % ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 4)


def guard(rj):
    if rj.get("program_fingerprint") and rj["program_fingerprint"] != w.program_fingerprint():
        w.die("REFUSED: the skill's programs, steps or rule pages changed while this run was in progress. The programs are run as they are. Start again in a new run folder.", 3)


def cmd_done(a):
    rj = load_run(a.run)
    guard(rj)
    ids = [s["id"] for s in steps()]
    if a.step not in ids:
        w.die("'%s' is not a step. Steps: %s" % (a.step, ", ".join(ids)))
    cur = current_step(rj)
    if cur is None or ids.index(a.step) > ids.index(cur["id"]):
        w.die("REFUSED: finish step '%s' first. Steps are done in order, none skipped." % (cur["id"] if cur else "?"), 3)
    step = steps()[ids.index(a.step)]
    fails = CHECKS[step["check"]](a.run, rj)
    if fails:
        print("NOT DONE: step '%s' is missing its proof:" % a.step)
        for f in fails:
            print("  - " + f)
        sys.exit(3)
    rj["steps"][a.step] = {"state": "done", "t": w.now()}
    save_run(a.run, rj)
    print("STEP '%s' DONE.\n" % a.step)
    nxt = current_step(rj)
    if nxt is None:
        print("EVERY STEP IS DONE.\nPut this SHORT AUDIT in your reply, as it is (it is the whole report; nothing longer):\n")
        import verify
        R, rj2, m = verify.run_checks(a.run, "final")
        verify.print_audit(R, rj2, "final", a.run)
        return
    show_step(a.run, rj, nxt)


def cmd_meeting(a):
    rj = load_run(a.run)
    guard(rj)
    length = tr.parse_length(a.length)
    d = tr.find_date([a.started])
    if not a.title.strip() or length is None or d is None:
        w.die('REFUSED: give --title "the meeting title", --started "DD/MM/YYYY, HH:MM" and --length like "1h 36m 2s" (all three must be readable).')
    rec = {"title": a.title.strip(), "started": a.started, "date": d.strftime("%d/%m/%Y"), "length_text": a.length, "length_s": length, "via": a.via}
    w.save_json(p(a.run, w.MEETING), rec)
    print("meeting recorded: %s, %s, length %s (via %s)" % (rec["title"], rec["date"], w.fmt_hms(length), a.via))
    if rec["date"] != rj["date"]:
        print("WARNING: that is %s but Paul asked for %s. Stop and check with Paul before going on." % (rec["date"], rj["date"]))


def cmd_access(a):
    rj = load_run(a.run)
    guard(rj)
    if a.route not in w.PURPOSES[a.purpose]:
        w.die("REFUSED: for --purpose %s the routes are %s" % (a.purpose, ", ".join(w.PURPOSES[a.purpose])))
    log = w.load_opt(p(a.run, w.ACCESS), [])
    log.append({"purpose": a.purpose, "route": a.route, "result": a.result, "note": a.note or "", "t": w.now()})
    w.save_json(p(a.run, w.ACCESS), log)
    print("access try recorded: %s %s %s (%d on record)" % (a.purpose, a.route, a.result, len(log)))


def cmd_source(a):
    rj = load_run(a.run)
    guard(rj)
    if not os.path.isfile(a.file):
        w.die("MISSING: %s" % a.file)
    log = [e for e in w.load_opt(p(a.run, w.ACCESS), []) if e.get("purpose") == "fetch"]
    if not any(e["route"] == a.route and e["result"] == "found" for e in log):
        w.die("REFUSED: record the fetch try first: run.py access %s --purpose fetch --route %s --result found" % (a.run, a.route))
    ext = ".docx" if tr.read_file(a.file)[0] == "docx" else (".vtt" if tr.read_file(a.file)[0] == "vtt" else ".txt")
    for old in os.listdir(a.run):
        if old.startswith(w.SOURCE + "."):
            os.remove(p(a.run, old))
    shutil.copyfile(a.file, p(a.run, w.SOURCE + ext))
    rj["source"] = {"route": a.route, "name": os.path.basename(a.file), "file": w.SOURCE + ext, "size": os.path.getsize(a.file), "sha256": w.sha256_file(a.file)}
    save_run(a.run, rj)
    print("transcript brought into the run folder: %s (%d bytes, %s) via %s" % (rj["source"]["name"], rj["source"]["size"], ext, a.route))


def cmd_check(a):
    import verify
    rj = load_run(a.run)
    guard(rj)
    R, _ = _pre(a.run)
    for mark, short, detail, _g in R.rows:
        print("%s %s" % (mark, short))
    if R.fails:
        print("\nThe transcript is not good enough to save. Tell Paul exactly what is above; do not save an incomplete transcript as if it were complete.")
        sys.exit(5)
    print("\nThe transcript passes the header, length and gap checks.")


def cmd_name(a):
    rj = load_run(a.run)
    guard(rj)
    m = w.load_opt(p(a.run, w.MEETING), None)
    sp = os.path.join(a.run, (rj.get("source") or {}).get("file", "-"))
    if not m or not os.path.exists(sp):
        w.die("REFUSED: identify the meeting and bring the transcript in first.")
    name = w.output_name(rj["client"]["first"], rj["client"]["surname"], rj["date"])
    outdir = p(a.run, w.OUT)
    for old in os.listdir(outdir):
        os.remove(os.path.join(outdir, old))
    out = os.path.join(outdir, name)
    kind, lines = tr.read_file(sp)
    if kind == "docx":
        shutil.copyfile(sp, out)                                    # a Teams .docx is copied as it is
        how = "copied unchanged"
    else:
        tr.write_docx(out, tr.vtt_to_lines(lines, m) if kind == "vtt" else lines)
        how = "written as a .docx from the received %s" % ("WebVTT text" if kind == "vtt" else "text")
    print("BUILT %s (%s, %d bytes)" % (out, how, os.path.getsize(out)))


def cmd_receipt(a):
    rj = load_run(a.run)
    guard(rj)
    rc = w.load_opt(p(a.run, w.RECEIPT), {})
    rc[a.key] = a.value
    w.save_json(p(a.run, w.RECEIPT), rc)
    print("receipt recorded: %s = %s" % (a.key, a.value))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("start")
    s.add_argument("run")
    s.add_argument("--client", required=True)
    s.add_argument("--date", required=True)
    s.add_argument("--type", choices=("first", "follow-up"))
    s.set_defaults(fn=cmd_start)
    x = sub.add_parser("preflight")
    x.set_defaults(fn=cmd_preflight)
    for name, fn in (("next", cmd_next), ("status", cmd_status), ("check", cmd_check), ("name", cmd_name)):
        x = sub.add_parser(name)
        x.add_argument("run")
        x.set_defaults(fn=fn)
    x = sub.add_parser("done")
    x.add_argument("run")
    x.add_argument("step")
    x.set_defaults(fn=cmd_done)
    x = sub.add_parser("meeting")
    x.add_argument("run")
    x.add_argument("--title", required=True)
    x.add_argument("--started", required=True)
    x.add_argument("--length", required=True)
    x.add_argument("--via", required=True, choices=("m365", "zapier", "chrome", "paul"))
    x.set_defaults(fn=cmd_meeting)
    x = sub.add_parser("access")
    x.add_argument("run")
    x.add_argument("--purpose", required=True, choices=("fetch", "save"))
    x.add_argument("--route", required=True)
    x.add_argument("--result", required=True, choices=("found", "failed"))
    x.add_argument("--note")
    x.set_defaults(fn=cmd_access)
    x = sub.add_parser("source")
    x.add_argument("run")
    x.add_argument("--file", required=True)
    x.add_argument("--route", required=True, choices=w.FETCH_ROUTES)
    x.set_defaults(fn=cmd_source)
    x = sub.add_parser("receipt")
    x.add_argument("run")
    x.add_argument("key")
    x.add_argument("value")
    x.set_defaults(fn=cmd_receipt)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
