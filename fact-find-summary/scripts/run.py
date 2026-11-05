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
    comp = rj.get("computer") or {}
    if not comp.get("found"):
        out.append(w.COMPUTER_STOP + " (record the connection: run.py computer %s --device ... --folder ... --listing ..., or run.py computer %s --none \"<what happened>\")" % (run, run))
    log = w.load_opt(p(run, w.ACCESS), [])
    if not log:
        out.append("no access try is recorded: run.py access for the PDF (route device with its fingerprint, or passed)")
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
    bridge = (rj.get("computer") or {}).get("mode") == "bridge"
    for k in ("pdf.saved_folder", "pdf.listed_bytes") + (("pdf.device_output",) if bridge else ()):
        if not rc.get(k):
            out.append("run.py receipt %s <value from the computer's own listing%s>" % (k, " and fingerprint" if k == "pdf.device_output" else ""))
    if bridge and rc.get("pdf.device_output"):
        st = w.load_opt(p(run, w.STATE), {})
        b = st.get("build") or {}
        dsha, dsize, why = w.parse_device_output(str(rc["pdf.device_output"]), str(b.get("pdf")))
        if why:
            out.append("pdf.device_output: " + why)
        elif dsha != b.get("pdf_sha") or dsize != b.get("pdf_size"):
            out.append("the PDF on the computer is not the PDF built here (computer: %d bytes, %s...; built: %s bytes, %s...): commit it again and fingerprint it again" % (dsize, dsha[:12], b.get("pdf_size"), str(b.get("pdf_sha"))[:12]))
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


def cmd_computer(a):
    """Records how this chat reaches the client's OneDrive folder on the computer. In a cloud chat the computer is a separate machine reached through the device tools
    (the chat connects, lists the client's folder and records it here); where the folder is mounted into this machine (a test) the program finds it itself."""
    rj = load_run(a.run)
    comp = rj.get("computer") or {}
    if a.none:
        if len(a.none.strip()) < 8:
            w.die("REFUSED: say what happened to the connection (at least 8 characters).")
        rj["computer"] = {"found": False, "t": w.now(), "detail": a.none.strip()}
        save_run(a.run, rj)
        print(w.COMPUTER_STOP)
        print("\nYour whole reply is those words, nothing more, and no question. When Paul says to go on, connect again and run: python3 %s/run.py computer %s --device ... --folder ... --listing ..." % (SCRIPTS, a.run))
        sys.exit(6)
    if a.device or a.folder or a.listing:
        if not (a.device and a.folder and a.listing):
            w.die("REFUSED: give --device (the computer's name), --folder (the folder the connection was granted for) and --listing (the file names device_list_dir showed in the client's folder).")
        if "liferisk.co.za" not in a.folder.lower().replace("/", "\\"):
            w.die("REFUSED: the connected folder must be the client files' root, liferisk.co.za (it was %r)." % a.folder)
        if len(a.listing.strip()) < 20:
            w.die("REFUSED: --listing must be what device_list_dir showed in the client's folder (the file names), not a summary.")
        rj["computer"] = {"found": True, "mode": "bridge", "device": a.device.strip(), "folder": a.folder.strip(), "listing": a.listing.strip()[:2000], "t": w.now()}
        save_run(a.run, rj)
        print("COMPUTER CONNECTED through the device tools (%s, folder %s). Read the PDF and save the Summary as pages 01 and 04 say." % (a.device.strip(), a.folder.strip()))
        return
    root = w.find_computer_root()
    if root:
        rj["computer"] = {"found": True, "mode": "mount", "root": root, "t": w.now()}
        save_run(a.run, rj)
        print("COMPUTER FOUND: the client's OneDrive folder is mounted at %s. Copy each file with cp and log it with --original." % root)
        return
    print("No connection is recorded yet. Connect with the device tools (page 01: get_device_info, then device_request_folder_access for ~/liferisk.co.za if it is not connected, then device_list_dir "
          "on the client's folder) and record it: python3 %s/run.py computer %s --device <name> --folder <granted folder> --listing \"<the file names>\"   "
          "If the connection is refused or cannot be made: python3 %s/run.py computer %s --none \"<what happened>\"" % (SCRIPTS, a.run, SCRIPTS, a.run))
    sys.exit(6)


def cmd_access(a):
    rj = load_run(a.run)
    guard(rj)
    log = w.load_opt(p(a.run, w.ACCESS), [])
    detail, result, verified, got, sha = a.note or "", a.result, False, None, None
    if a.route in ("m365", "zapier") and a.result == "found":
        w.die("REFUSED: the Fact Find Transcript PDF cannot be taken through %s: a PDF arrives there cut off, as text. Take it from the computer (--route device, with --device-output), "
              "or use --route passed when ff-population-transcript handed it over in this chat." % ("Microsoft 365" if a.route == "m365" else "Zapier"))
    if a.route == "device" and a.result == "found":
        if not (rj.get("computer") or {}).get("found"):
            w.die("REFUSED: no computer connection is recorded in this run (run.py computer %s). A try on the computer is logged only when it is connected." % a.run)
        if not a.file or not (a.device_output or a.original):
            w.die("REFUSED: a PDF taken from the computer needs its proof: --file <your copy> with --device-output <the whole output of sha256sum and stat run on the computer with device_bash> "
                  "(or --original, where the folder is mounted into this machine). Nobody is asked for anything.")
    if a.device_output and a.original:
        w.die("REFUSED: give --original (a mounted folder) or --device-output (the computer's own fingerprint), not both.")
    if a.file or a.device_output or a.original:
        if not a.file or not os.path.isfile(a.file):
            w.die("MISSING: the copy %s" % a.file)
        if a.route != "device":
            w.die("REFUSED: --device-output and --original are for the computer route (--route device).")
        got, sha = os.path.getsize(a.file), w.sha256_file(a.file)
        if a.original:
            root = (rj.get("computer") or {}).get("root")
            if not root or not w.under_root(a.original, root):
                w.die("REFUSED: --original must be a file on the computer, inside %s." % root)
            if not os.path.isfile(a.original):
                w.die("MISSING: the original %s" % a.original)
            same = w.sha256_file(a.original) == sha
        else:
            dsha, dsize, why = w.parse_device_output(a.device_output, os.path.basename(a.file))
            if why:
                w.die("REFUSED: " + why)
            same = dsha == sha and dsize == got
        if same:
            verified = True
            detail = (detail + " ").lstrip() + "copy verified: identical to the file on the computer (%d bytes, sha256 %s...)" % (got, sha[:12])
        else:
            result = "failed"
            detail = (detail + " ").lstrip() + "copy NOT identical to the file on the computer (%d bytes saved)" % got
            print("logged as a FAIL: the copy is not identical to the file on the computer. Stage it again (device_stage_files) and compare again.")
    log.append({"route": a.route, "result": result, "note": detail, "t": w.now(), "verified": verified, "bytes": got, "sha256": sha})
    w.save_json(p(a.run, w.ACCESS), log)
    print("access try recorded: %s %s (%d on record)" % (a.route, result, len(log)))


def cmd_source(a):
    rj = load_run(a.run)
    guard(rj)
    if not os.path.isfile(a.file):
        w.die("MISSING: %s" % a.file)
    log = w.load_opt(p(a.run, w.ACCESS), [])
    mine = [e for e in log if e["route"] == a.route and e["result"] == "found"]
    if a.route not in ("device", "passed") or not mine:
        w.die("REFUSED: record the access try first: run.py access %s --route device --result found --file <copy> --device-output <the computer's fingerprint> (or --route passed when ff-population-transcript handed it over)" % a.run)
    if a.route == "device" and not (mine[-1].get("verified") and mine[-1].get("sha256") == w.sha256_file(a.file)):
        w.die("REFUSED: this file is not the copy that was proved identical to the file on the computer. Log it with --file <this copy> --device-output <the computer's fingerprint> first.")
    bad = w.pdf_file_problems(a.file)
    if bad:
        w.die("STOP: this is not the whole PDF: %s. Nothing was recorded. Take the PDF from the computer (it must be identical to the file there)." % "; ".join(bad), 4)
    shutil.copyfile(a.file, p(a.run, w.FACTFIND_PDF))
    rj["source"] = {"route": a.route, "name": os.path.basename(a.file), "size": os.path.getsize(a.file), "sha256": w.sha256_file(a.file), "size_checked": a.route == "device"}
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
    x.add_argument("--file", help="the copy you staged from the computer")
    x.add_argument("--device-output", dest="device_output", help="the whole output of sha256sum and stat -c %%s for that file, run on the computer with device_bash")
    x.add_argument("--original", help="a file in a folder mounted into this machine that you copied (the program compares the two byte for byte)")
    x.set_defaults(fn=cmd_access)
    x = sub.add_parser("source")
    x.add_argument("run")
    x.add_argument("--file", required=True)
    x.add_argument("--route", required=True, choices=w.SOURCE_ROUTES)
    x.set_defaults(fn=cmd_source)
    x = sub.add_parser("computer")
    x.add_argument("run")
    x.add_argument("--device", help="the computer's name (get_device_info)")
    x.add_argument("--folder", help="the folder the connection was granted for (for example C:\\Users\\Paul\\liferisk.co.za)")
    x.add_argument("--listing", help="the file names device_list_dir showed in the client's folder")
    x.add_argument("--none", help="what happened, when the connection was refused or could not be made (prints the STOP)")
    x.set_defaults(fn=cmd_computer)
    x = sub.add_parser("receipt")
    x.add_argument("run")
    x.add_argument("key")
    x.add_argument("value")
    x.set_defaults(fn=cmd_receipt)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
