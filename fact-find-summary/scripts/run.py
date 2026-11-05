#!/usr/bin/env python3
"""The step driver of the fact-find-summary skill: shows ONE step at a time, refuses to skip, keeps the run on disk.

  run.py start <run> --client "First Surname" --date DD/MM/YYYY [--joint "Other Surname" [--spouse-pdf FILE]]
  run.py next | status <run>
  run.py access <run> --route device|m365|zapier --result found|failed [--note TEXT]
  run.py source <run> --file FILE --route device|m365|zapier     copy the Fact Find Transcript PDF into the run folder
  run.py read <run>        read the PDF into rows (stops when it is not the program-drawn report)
  run.py compose <run>     build content.json (nine sections)
  run.py build <run>       draw the PDF (A4) and the page images
  run.py receipt <run> KEY VALUE
  run.py done <run> STEP   prove the step, then show the next one

Claude runs these programs as they are and never rewrites them during a run.
"""
import argparse
import os
import shutil
import sys

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
        w.die("This is not a run folder (no %s). Start one with: python3 %s/run.py start <run folder> --client \"First Surname\" --date DD/MM/YYYY" % (w.RUN, SCRIPTS), 2)
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
    rows = []
    for mod in ("pdfplumber", "reportlab"):
        try:
            __import__(mod)
            rows.append((True, "python module %s is available" % mod))
        except ImportError:
            rows.append((False, "python module %s is NOT available (try: pip install %s)" % (mod, mod)))
    rows.append((shutil.which("pdftoppm") is not None, "pdftoppm (page images) is %savailable" % ("" if shutil.which("pdftoppm") else "NOT ")))
    rows.append((w.skill_stamp() is not None, "the skill has a Last updated stamp (%s)" % (w.stamp_display(w.skill_stamp()) or "none")))
    return all(r[0] for r in rows), rows


# ------------------------------------------------------------------ the checks behind each step
def ck_locate(run, rj):
    out = []
    log = w.load_opt(p(run, w.ACCESS), [])
    if not log:
        out.append("no access try is recorded: run.py access for EVERY route you try, failures included")
    elif log[0].get("route") not in ("device", "passed"):
        out.append("the first try must be the computer (log it at once as not connected) or the PDF passed in by ff-population-transcript; the first recorded try is %r" % log[0].get("route"))
    if not rj.get("source"):
        out.append("the Fact Find Transcript PDF has not been brought into the run folder: run.py source --file ... --route ...")
    return out


def ck_read(run, rj):
    import ffread
    if not os.path.exists(p(run, w.FACTFIND)):
        return ["the PDF has not been read: run.py read"]
    ffd = w.load_json(p(run, w.FACTFIND))
    return ffread.layout_problems(ffd)


def ck_compose(run, rj):
    return [] if os.path.exists(p(run, w.CONTENT)) else ["content.json does not exist: run.py compose"]


def ck_build(run, rj):
    st = w.load_opt(p(run, w.STATE), {})
    b = st.get("build")
    if not b:
        return ["the PDF has not been built: run.py build"]
    pdf = os.path.join(run, w.OUT, b["pdf"])
    if not os.path.exists(pdf) or w.sha256_file(pdf) != b["pdf_sha"]:
        return ["the PDF is missing or was changed after it was built: run.py build again"]
    return []


def _verify(stage):
    def ck(run, rj):
        import verify
        R, st, c = verify.run_checks(run, stage)
        if R.fails:
            verify.print_audit(R, st, c, stage, run)
            return ["the checker has %d red cross(es) above" % len(R.fails)]
        return []
    return ck


def ck_deliver(run, rj):
    rc = w.load_opt(p(run, w.RECEIPT), {})
    need = [("pdf.sent", "yes"), ("images.looked", "yes")]
    out = ["run.py receipt %s %s" % (k, v) for k, v in need if rc.get(k) != v]
    for k in ("pdf.saved_folder", "pdf.listed_bytes"):
        if not rc.get(k):
            out.append("run.py receipt %s <value from the real folder listing>" % k)
    return out


CHECKS = {"locate_ok": ck_locate, "read_ok": ck_read, "compose_ok": ck_compose, "build_ok": ck_build, "verify_pre": _verify("pre"),
          "deliver_ok": ck_deliver, "verify_final": _verify("final")}


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
        w.die("\nSTOP. Tell Paul exactly which item failed above. Do not carry on and do not replace the PDF with a text draft or a Word file.", 4)
    os.makedirs(os.path.join(a.run, w.OUT), exist_ok=True)
    rj = {"skill": w.skill_name(), "created": w.now(), "skill_stamp": w.skill_stamp(), "steps": {}, "client": {"first": first, "surname": surname},
          "date": a.date, "joint": a.joint, "spouse_pdf": os.path.abspath(a.spouse_pdf) if a.spouse_pdf else None,
          "program_fingerprint": w.program_fingerprint()}
    save_run(a.run, rj)
    for name, empty in ((w.ACCESS, []), (w.RECEIPT, {}), (w.STATE, {})):
        w.save_json(p(a.run, name), empty)
    print("\nSAY THIS TO PAUL FIRST, before anything else in your reply, in exactly these words:\n    %s.\n" % w.version_line())
    print("RUN STARTED  client: %s %s   meeting date: %s%s\n" % (first, surname, a.date, ("   JOINT MEETING with %s" % a.joint) if a.joint else ""))
    print("Standing rules for the whole job:\n")
    print(expand(read_ref("00-rules.md"), a.run))
    print()
    show_step(a.run, rj, current_step(rj))


def cmd_preflight(a):
    ok, rows = preflight()
    for good, text in rows:
        print("  [%s] %s" % ("OK" if good else "FAIL", text))
    print("PREFLIGHT: %s" % ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 4)


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
        R, st, c = verify.run_checks(a.run, "final")
        verify.print_audit(R, st, c, "final", a.run)
        return
    show_step(a.run, rj, nxt)


def cmd_access(a):
    rj = load_run(a.run)
    guard(rj)
    log = w.load_opt(p(a.run, w.ACCESS), [])
    log.append({"route": a.route, "result": a.result, "note": a.note or "", "t": w.now()})
    w.save_json(p(a.run, w.ACCESS), log)
    print("access try recorded: %s %s (%d on record)" % (a.route, a.result, len(log)))


def cmd_source(a):
    rj = load_run(a.run)
    guard(rj)
    if not os.path.isfile(a.file):
        w.die("MISSING: %s" % a.file)
    log = w.load_opt(p(a.run, w.ACCESS), [])
    if not any(e["route"] == a.route and e["result"] == "found" for e in log):
        w.die("REFUSED: record the access try first: run.py access %s --route %s --result found" % (a.run, a.route))
    if a.source_size is not None and os.path.getsize(a.file) != a.source_size:
        w.die("REFUSED: the copy is %d bytes but the connector reports %d. Read the file again through the connector and save it whole. Do NOT ask Paul for anything." % (os.path.getsize(a.file), a.source_size))
    shutil.copyfile(a.file, p(a.run, w.FACTFIND_PDF))
    rj["source"] = {"route": a.route, "name": os.path.basename(a.file), "size": os.path.getsize(a.file), "sha256": w.sha256_file(a.file), "size_checked": a.source_size is not None}
    save_run(a.run, rj)
    print("Fact Find PDF brought into the run folder: %s (%d bytes) via %s" % (rj["source"]["name"], rj["source"]["size"], a.route))


def cmd_read(a):
    import ffread
    rj = load_run(a.run)
    guard(rj)
    if not os.path.exists(p(a.run, w.FACTFIND_PDF)):
        w.die("The Fact Find PDF is not in the run folder yet: run.py source first.")
    ffd = ffread.read_pdf(p(a.run, w.FACTFIND_PDF))
    probs = ffread.layout_problems(ffd)
    w.save_json(p(a.run, w.FACTFIND), ffd)
    c = rj["client"]
    print("READ: %s | meeting date %s | %d sections | %d rows | %d flags | %d page(s)" % (ffd["client_name"], ffd["meeting_date"], ffd["stats"]["sections"], ffd["stats"]["rows"], ffd["stats"]["flags"], ffd["pages"]))
    if probs:
        print("STOP. This PDF is not the program-drawn Fact Find Transcript:\n  - " + "\n  - ".join(probs))
        print("Tell Paul in one line which PDF this is (a hand-made Fact Find, an old layout or a scan cannot be summarised by this skill). Do NOT guess the values.")
        sys.exit(5)
    if w.norm("%s %s" % (c["first"], c["surname"])) != w.norm(ffd["client_name"]) or ffd["meeting_date"] != rj["date"]:
        print("STOP. The PDF is for %s, %s but Paul asked for %s %s, %s. Find the right PDF (step locate) or tell Paul." % (ffd["client_name"], ffd["meeting_date"], c["first"], c["surname"], rj["date"]))
        sys.exit(5)
    print("The layout is the program-drawn Fact Find Transcript. Client and date match.")


def cmd_compose(a):
    import compose
    rj = load_run(a.run)
    guard(rj)
    ffd = w.load_json(p(a.run, w.FACTFIND), "fact_find.json (run.py read first)")
    content = compose.compose(ffd, rj)
    w.save_json(p(a.run, w.CONTENT), content)
    items = content["sections"][8]["blocks"][0]["rows"]
    n = sum(len(b["rows"]) for s in content["sections"] for b in s["blocks"])
    print("COMPOSED %d rows in 9 sections; %d rows left out (Not discussed / N/A / 0%%); file name: %s" % (n, len(content["left_out"]), content["file_name"]))
    print("Items Requiring Follow-Up (%d):" % len(items))
    for r in items:
        print("  - " + r["values"][0])
    for pr in content["problems"]:
        print("PROBLEM: " + pr)


def cmd_build(a):
    import build
    sys.argv = ["build.py", a.run]
    build.main()


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
    s.add_argument("--joint")
    s.add_argument("--spouse-pdf", dest="spouse_pdf")
    s.set_defaults(fn=cmd_start)
    for name, fn in (("next", cmd_next), ("status", cmd_status), ("read", cmd_read), ("compose", cmd_compose), ("build", cmd_build)):
        x = sub.add_parser(name)
        x.add_argument("run")
        x.set_defaults(fn=fn)
    x = sub.add_parser("preflight")
    x.set_defaults(fn=cmd_preflight)
    x = sub.add_parser("done")
    x.add_argument("run")
    x.add_argument("step")
    x.set_defaults(fn=cmd_done)
    x = sub.add_parser("access")
    x.add_argument("run")
    x.add_argument("--route", required=True, choices=w.SOURCE_ROUTES)
    x.add_argument("--result", required=True, choices=("found", "failed"))
    x.add_argument("--note")
    x.set_defaults(fn=cmd_access)
    x = sub.add_parser("source")
    x.add_argument("run")
    x.add_argument("--file", required=True)
    x.add_argument("--route", required=True, choices=w.SOURCE_ROUTES)
    x.add_argument("--source-size", dest="source_size", type=int, help="the size in bytes the connector reported for the PDF")
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
