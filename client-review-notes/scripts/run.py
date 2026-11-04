#!/usr/bin/env python3
"""The step driver of the client-review-notes: shows ONE step at a time, refuses to skip, keeps the run on disk.

  run.py start <run> --client "First Surname"
  run.py next | status | preflight
  run.py access <run> --purpose notes|earlier|save --route device|m365|zapier --result found|failed [--note TEXT]
  run.py notes <run> --file FILE --route device|m365|zapier|pasted      register the raw notes (the only source)
  run.py earlier <run> --id ID --file FILE --route ROUTE                register an earlier Client Record (.md) for the duplicate check
  run.py read <run> [--ack N --note TEXT]                               the raw notes, in parts, in order
  run.py duplicate <run> --decision merge|separate --said "Paul's words"
  run.py record <run> --file record.json                                check the record against the raw notes and build the .md
  run.py receipt <run> KEY VALUE
  run.py save <run> --file LISTING                                      only when Paul asked for a copy in the client's folder
  run.py done <run> STEP                                                prove the step, then show the next one

Nothing in these programs sends or saves anything: the chat does, with exactly out/<file>.md.
Claude runs these programs as they are and never rewrites them during a run.
"""
import argparse
import os
import shutil
import sys

import crn
import docread
import engine as eng
import notes as N
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
        w.die('This is not a run folder (no %s). Start one with: python3 %s/run.py start <run folder> --client "First Surname"' % (w.RUN, SCRIPTS), 2)
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
    rows = [(w.skill_stamp() is not None, "the skill has a Last updated stamp (%s)" % (w.stamp_display(w.skill_stamp()) or "none"))]
    try:
        crn.settings()
        rows.append((True, "the field list, glossary and layout settings load"))
    except Exception as e:
        rows.append((False, "the settings could not be loaded: %s" % e))
    return all(r[0] for r in rows), rows


def _checks(run, *groups):
    import verify
    R, rj = verify.run_checks(run, "pre")
    out = [r[1] for r in R.rows if r[0] == verify.BAD and r[3] in groups]
    for g in groups:
        if not any(r[3] == g for r in R.rows):
            out.append("the checker has no result yet for '%s'" % g)
    return out


CHECKS = {"source_ok": lambda run, rj: _checks(run, "source"), "read_ok": lambda run, rj: _checks(run, "source", "read"),
          "dup_ok": lambda run, rj: _checks(run, "source", "read", "duplicates"), "record_ok": lambda run, rj: _checks(run, "source", "read", "duplicates", "record"),
          "deliver_ok": lambda run, rj: _checks(run, "record", "deliver")}


def ck_final(run, rj):
    import verify
    R, rj2 = verify.run_checks(run, "final")
    if R.fails:
        verify.print_audit(R, rj2, "final", run)
        return ["the checker has %d red cross(es) above" % len(R.fails)]
    return []


CHECKS["verify_final"] = ck_final


# ------------------------------------------------------------------ commands
def cmd_start(a):
    parts = a.client.split()
    if len(parts) < 2:
        w.die('--client must be the first name and surname, for example --client "Pat Samplecase"')
    first, surname = parts[0], " ".join(parts[1:])
    if os.path.exists(p(a.run, w.RUN)):
        old = load_run(a.run)
        oc = old["client"]
        if w.norm("%s %s" % (oc["first"], oc["surname"])) != w.norm(a.client):
            w.die("REFUSED: this run folder already belongs to %s %s. Use a NEW run folder." % (oc["first"], oc["surname"]), 2)
        print("This run already exists. Showing where it is up to.")
        return cmd_next(a)
    ok, rows = preflight()
    print("SELF-TEST BEFORE ANYTHING ELSE:")
    for good, text in rows:
        print("  [%s] %s" % ("OK" if good else "FAIL", text))
    if not ok:
        w.die("\nSTOP. Tell Paul exactly which item failed above. Do not carry on.", 4)
    for d in (w.OUT, "notes"):
        os.makedirs(os.path.join(a.run, d), exist_ok=True)
    rj = {"skill": w.skill_name(), "created": w.now(), "skill_stamp": w.skill_stamp(), "steps": {}, "client": {"first": first, "surname": surname},
          "today": w.today().strftime("%d/%m/%Y"), "program_fingerprint": w.program_fingerprint()}
    save_run(a.run, rj)
    for name, empty in ((w.ACCESS, []), (w.RECEIPT, {}), (w.STATE, {}), ("earlier.json", [])):
        w.save_json(p(a.run, name), empty)
    print("\nSAY THIS TO PAUL FIRST, before anything else in your reply, in exactly these words:\n    %s.\n" % w.version_line())
    print("RUN STARTED  client: %s %s   today (South Africa): %s\n" % (first, surname, rj["today"]))
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
        w.die("REFUSED: the skill's programs, steps, rule pages or settings changed while this run was in progress. The programs are run as they are. Start again in a new run folder.", 3)


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
        print("EVERY STEP IS DONE.\nPut this SHORT AUDIT and the block for Paul in your reply, as they are (nothing longer):\n")
        import verify
        R, rj2 = verify.run_checks(a.run, "final")
        verify.print_audit(R, rj2, "final", a.run)
        print()
        print(handback(a.run))
        return
    show_step(a.run, rj, nxt)


def handback(run):
    c = eng.compute(run)
    out = ["FOR PAUL (the file is the deliverable: %s)" % c["file_name"]]
    ch = c["chk"] or {"left_out": [], "flags": [], "dnc": []}
    out.append("Left out of the record on purpose (with the reason): " + ("; ".join("%s (%s)" % (k, v) for k, v in ch["left_out"]) if ch["left_out"] else "nothing"))
    out.append("Flags at the top of Notes: " + (crn.mask_text("; ".join(ch["flags"])) if ch["flags"] else "none"))
    if ch["dnc"]:
        out.append("DO NOT CONTACT lines reproduced in full: %d" % len(ch["dnc"]))
    return "\n".join(out)


def cmd_access(a):
    rj = load_run(a.run)
    guard(rj)
    log = w.load_opt(p(a.run, w.ACCESS), [])
    log.append({"purpose": a.purpose, "route": a.route, "result": a.result, "note": a.note or "", "t": w.now()})
    w.save_json(p(a.run, w.ACCESS), log)
    print("access try recorded: %s / %s / %s (%d on record)" % (a.purpose, a.route, a.result, len(log)))


def _route_ok(run, route, purpose):
    if route == "pasted":
        return
    log = w.load_opt(p(run, w.ACCESS), [])
    if not any(e["route"] == route and e["result"] == "found" and e.get("purpose") == purpose for e in log):
        w.die("REFUSED: record the access try first: run.py access %s --purpose %s --route %s --result found" % (run, purpose, route))
    bad = eng.route_order_problems(log)
    if bad:
        w.die("REFUSED: the routes are tried in order (computer, Microsoft 365, Zapier); %s was used before the earlier ones failed." % ", ".join(bad))


def _clear(run, *keys):
    st = w.load_opt(p(run, w.STATE), {})
    for k in keys:
        st.pop(k, None)
    w.save_json(p(run, w.STATE), st)


def cmd_notes(a):
    rj = load_run(a.run)
    guard(rj)
    if not os.path.isfile(a.file):
        w.die("MISSING: %s" % a.file)
    _route_ok(a.run, a.route, "notes")
    try:
        rep = docread.read_document(a.file)
    except Exception as e:
        print("STOP. This file cannot be read: %s" % e)
        sys.exit(5)
    text = "\n".join(pg["text"] for pg in rep["pages"])
    if rep["image_only"] or len(text.strip()) < 20:
        print("STOP. The notes have no readable text (an image or an empty file). Read them yourself and give them to Paul as text; the program cannot prove anything on an image.")
        sys.exit(5)
    with open(p(a.run, os.path.join("notes", "raw.txt")), "w", encoding="utf-8", newline="") as f:
        f.write(text)
    entries, recognised = N.split_entries(text)
    parts = N.parts(text, crn.settings()["entry_part_chars"])
    meta = {"text_file": os.path.join("notes", "raw.txt"), "name": os.path.basename(a.file), "route": a.route, "sha": w.sha256_file(p(a.run, os.path.join("notes", "raw.txt"))),
            "chars": len(text), "parts": len(parts), "entries": len(entries), "recognised": recognised}
    w.save_json(p(a.run, w.NOTES), meta)
    _clear(a.run, "read", "duplicate")
    print("raw notes registered: %s (%d characters, %d part(s)) via %s" % (meta["name"], meta["chars"], meta["parts"], a.route))
    if recognised:
        print("%d dated entr%s recognised (the coverage check runs entry by entry)." % (len([e for e in entries if e["key"]]), "y" if len(entries) == 1 else "ies"))
    else:
        print("NOTE: no recognisable dated entries. The whole note is ONE entry, so the coverage check is weaker; the audit says so.")


def cmd_earlier(a):
    rj = load_run(a.run)
    guard(rj)
    if not os.path.isfile(a.file):
        w.die("MISSING: %s" % a.file)
    _route_ok(a.run, a.route, "earlier")
    lst = w.load_opt(p(a.run, "earlier.json"), [])
    dst = os.path.join("notes", "earlier_%s.md" % a.id)
    shutil.copyfile(a.file, p(a.run, dst))
    lst = [x for x in lst if x["id"] != a.id] + [{"id": a.id, "file": dst, "name": os.path.splitext(os.path.basename(a.file))[0], "route": a.route, "sha": w.sha256_file(p(a.run, dst))}]
    w.save_json(p(a.run, "earlier.json"), lst)
    _clear(a.run, "duplicate")
    print("earlier record registered: %s (%s)" % (a.id, os.path.basename(a.file)))


def cmd_read(a):
    rj = load_run(a.run)
    guard(rj)
    c = eng.compute(a.run)
    if c["meta"] is None:
        w.die("No raw notes are registered yet: run.py notes first.")
    ps = N.parts(c["raw"], crn.settings()["entry_part_chars"])
    st = w.load_opt(p(a.run, w.STATE), {})
    acked = st.setdefault("read", {}).setdefault("acked", {})
    nxt = next((i for i in range(1, len(ps) + 1) if str(i) not in acked), None)
    if a.ack:
        if nxt is None or a.ack != nxt:
            w.die("REFUSED: parts are acknowledged in order. The next part is %s." % (nxt if nxt else "none (all done)"))
        if len((a.note or "").strip()) < 3:
            w.die('REFUSED: acknowledge the part with a one-line note of what is in it: --note "..."')
        acked[str(a.ack)] = a.note.strip()
        w.save_json(p(a.run, w.STATE), st)
        print("part %d acknowledged (%d of %d)" % (a.ack, len(acked), len(ps)))
        nxt = next((i for i in range(1, len(ps) + 1) if str(i) not in acked), None)
    if nxt is None:
        print("All %d part(s) were read and acknowledged. Now run: python3 %s/run.py done %s read" % (len(ps), SCRIPTS, a.run))
        return
    print("-" * 24 + " RAW NOTES - PART %d of %d " % (nxt, len(ps)) + "-" * 24)
    print(ps[nxt - 1])
    print("-" * 78)
    print('Read it fully, then: python3 %s/run.py read %s --ack %d --note "one line on what is in this part"' % (SCRIPTS, a.run, nxt))


def cmd_duplicate(a):
    rj = load_run(a.run)
    guard(rj)
    c = eng.compute(a.run)
    if not c["dups"]:
        print("No earlier record matches this client: nothing to decide.")
        return
    if len((a.said or "").strip()) < 5:
        w.die("REFUSED: record Paul's own words with --said.")
    st = w.load_opt(p(a.run, w.STATE), {})
    st["duplicate"] = {"decision": a.decision, "said": a.said, "ids": [d["id"] for d in c["dups"]], "t": w.now()}
    w.save_json(p(a.run, w.STATE), st)
    print("decision recorded: %s (earlier record(s): %s)" % (a.decision, ", ".join(d["id"] for d in c["dups"])))


def cmd_record(a):
    rj = load_run(a.run)
    guard(rj)
    if not os.path.isfile(a.file):
        w.die("MISSING: --file record.json")
    w.save_json(p(a.run, w.RECORD), w.load_json(a.file, "the record file"))
    for f in os.listdir(p(a.run, w.OUT)):
        if f.endswith(".md"):
            os.remove(p(a.run, os.path.join(w.OUT, f)))
    c = eng.compute(a.run)
    if c["meta"] is None:
        w.die("REFUSED: register the raw notes first.")
    if c["problems"]:
        print("REFUSED. These must be put right (fix the record file and run this again):")
        for x in c["problems"]:
            print("  - " + x)
        sys.exit(5)
    with open(p(a.run, os.path.join(w.OUT, c["file_name"])), "w", encoding="utf-8", newline="") as f:
        f.write(c["md"])
    print("RECORD BUILT: out/%s (%d characters)" % (c["file_name"], len(c["md"])))
    ch = c["chk"]
    print("Left out on purpose: %s" % ("; ".join("%s (%s)" % (k, v) for k, v in ch["left_out"]) if ch["left_out"] else "nothing"))
    for fl in ch["flags"]:
        print("FLAG (shown at the top of Notes): " + crn.mask_text(fl))
    print("Next: run.py done %s record." % a.run)


def cmd_receipt(a):
    rj = load_run(a.run)
    guard(rj)
    rc = w.load_opt(p(a.run, w.RECEIPT), {})
    rc[a.key] = a.value
    w.save_json(p(a.run, w.RECEIPT), rc)
    print("receipt recorded: %s = %s" % (a.key, a.value))


def cmd_save(a):
    rj = load_run(a.run)
    guard(rj)
    c = eng.compute(a.run)
    rc = w.load_opt(p(a.run, w.RECEIPT), {})
    if len((rc.get("save.paul_said") or "").strip()) < 5:
        w.die("REFUSED: a copy goes into the client's folder only when Paul asks for it: record receipt save.paul_said with his words.")
    if not (rc.get("save.folder") or "").strip():
        w.die("REFUSED: record receipt save.folder (the folder path used) first.")
    if not os.path.isfile(a.file):
        w.die("MISSING: the saved listing")
    with open(a.file, encoding="utf-8", errors="replace") as f:
        text = f.read()
    ok = c["file_name"].lower() in text.lower()
    st = w.load_opt(p(a.run, w.STATE), {})
    st["save"] = {"t": w.now(), "ok": ok}
    w.save_json(p(a.run, w.STATE), st)
    if not ok:
        print("❌ the folder listing does not show %s" % c["file_name"])
        sys.exit(5)
    print("✅ %s is in the client's folder." % c["file_name"])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("start")
    s.add_argument("run")
    s.add_argument("--client", required=True)
    s.set_defaults(fn=cmd_start)
    x = sub.add_parser("preflight")
    x.set_defaults(fn=cmd_preflight)
    for name, fn in (("next", cmd_next), ("status", cmd_status)):
        x = sub.add_parser(name)
        x.add_argument("run")
        x.set_defaults(fn=fn)
    x = sub.add_parser("done")
    x.add_argument("run")
    x.add_argument("step")
    x.set_defaults(fn=cmd_done)
    x = sub.add_parser("access")
    x.add_argument("run")
    x.add_argument("--purpose", required=True, choices=("notes", "earlier", "save", "other"))
    x.add_argument("--route", required=True, choices=w.ROUTES)
    x.add_argument("--result", required=True, choices=("found", "failed"))
    x.add_argument("--note")
    x.set_defaults(fn=cmd_access)
    x = sub.add_parser("notes")
    x.add_argument("run")
    x.add_argument("--file", required=True)
    x.add_argument("--route", required=True, choices=w.SOURCE_ROUTES)
    x.set_defaults(fn=cmd_notes)
    x = sub.add_parser("earlier")
    x.add_argument("run")
    x.add_argument("--id", required=True)
    x.add_argument("--file", required=True)
    x.add_argument("--route", required=True, choices=w.SOURCE_ROUTES)
    x.set_defaults(fn=cmd_earlier)
    x = sub.add_parser("read")
    x.add_argument("run")
    x.add_argument("--ack", type=int)
    x.add_argument("--note")
    x.set_defaults(fn=cmd_read)
    x = sub.add_parser("duplicate")
    x.add_argument("run")
    x.add_argument("--decision", required=True, choices=("merge", "separate"))
    x.add_argument("--said", required=True)
    x.set_defaults(fn=cmd_duplicate)
    x = sub.add_parser("record")
    x.add_argument("run")
    x.add_argument("--file", required=True)
    x.set_defaults(fn=cmd_record)
    x = sub.add_parser("receipt")
    x.add_argument("run")
    x.add_argument("key")
    x.add_argument("value")
    x.set_defaults(fn=cmd_receipt)
    x = sub.add_parser("save")
    x.add_argument("run")
    x.add_argument("--file", required=True)
    x.set_defaults(fn=cmd_save)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
