#!/usr/bin/env python3
"""Step driver for the client-teams-transcript skill (SKILL-STANDARDS.md S16).

  run.py start   <run_dir> --type followup|first|whatsapp --client "First Surname" --date DD/MM/YYYY
  run.py next    <run_dir>            show the current step again
  run.py done    <run_dir> <step>     check the proof; only then move on
  run.py status  <run_dir>            where the job is up to (also the recovery point after a long chat)
  run.py preflight                    the self-test on its own

  run.py computer <run_dir> (--device NAME --folder F --listing L | --none WHAT_HAPPENED)    step 1: how this chat reaches the computer
  run.py access  <run_dir> --need N --route device|m365|zapier|user|passed --tool T --result ok|fail [--detail D]
                            [--file COPY --device-output "<sha256sum + stat output from the computer>"]
  run.py source  <run_dir> --kind K (--path P --date YYYY-MM-DD --read yes [--ref NAME] [--file COPY --device-output O] [--text-file F] | --none REASON)
  run.py ask     <run_dir> --need N --question Q --searched S [--kind file|knowledge]
  run.py ledger  <run_dir> add --line N --kind K --quote Q [--speaker S] [--meaning M]
  run.py ledger  <run_dir> cover <ledger id> <item id> [<item id> ...]
  run.py ledger  <run_dir> exclude <ledger id> <reason>
  run.py ledger  <run_dir> ack --pass 1|2 --chunk N --reason R
  run.py ledger  <run_dir> review (--line N | --from A --to B) --reason R
  run.py ledger  <run_dir> list
  run.py receipt <run_dir> --set a.b=value [--set ...]

The program shows one step at a time and will not show the next until the proof for
this one is on file. It is run as it is; it is never edited during a run.
"""
import argparse
import datetime as dt
import os
import re
import shutil
import sys

import page
import tx
import verify
import wrlib as w

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPTS)
LEDGER_KINDS = sorted(verify.KINDS_MUST_COVER | verify.KINDS_OPTIONAL)
RULE = "-" * 78


# ------------------------------------------------------------------ helpers
def steps_file():
    return w.load_json(os.path.join(SKILL_DIR, "steps.json"), "steps.json")


def p(run, name):
    return os.path.join(run, name)


def load_list(run, name):
    path = p(run, name)
    return w.load_json(path) if os.path.exists(path) else []


def load_run(run):
    return w.load_json(p(run, w.RUN), "run.json (run `run.py start` first)")


def applicable(rj):
    return [s for s in steps_file()["steps"] if rj["meeting_type"] in s["applies"]]


def refs_of(step):
    r = step.get("ref") or []
    return [r] if isinstance(r, str) else r


def read_ref(name):
    path = os.path.join(SKILL_DIR, "references", name)
    if not os.path.exists(path):
        return "(MISSING reference page %s: the skill package is broken; tell Paul)" % name
    return open(path, encoding="utf-8").read().rstrip()


def chunk_commands(run, pass_no):
    st = w.load_json(p(run, w.STATE)) if os.path.exists(p(run, w.STATE)) else None
    k = len(st["chunks"]) if st else 0
    if not k:
        return "(chunk commands appear once `tx.py prep` has run)"
    return ("  python3 %s/tx.py chunk %s %d 1     (%d chunks in all; each chunk prints the command for the next one, and the next is\n"
            "  refused until this one has ledger entries or a reasoned acknowledgement)" % (SCRIPTS, run, pass_no, k))


def teams_block(run):
    cp = p(run, w.CONTENT)
    if not os.path.exists(cp):
        return "(the Teams message is built from content.json: finish the earlier steps first)"
    content = w.load_json(cp)
    msg = page.teams_message(content)
    if not msg:
        return "(no message could be built: check content.json)"
    R, *_ = verify.run_checks(run, "final", ("teams",))
    if R.fails:
        return ("NOT YET. The message must not be shown or sent until every other check passes. Fix these first:\n" +
                "\n".join("  - " + m for lvl, _, m in R.rows if lvl == "FAIL")[:2500] +
                "\nThen run `python3 %s/run.py next %s` again." % (SCRIPTS, run))
    lines = ["BEFORE SENDING: if this meeting's message was already sent by ff-population-transcript or fact-find-summary in this chat, "
             "record teams.status=already_sent with teams.already_sent_evidence (which skill, when, message id) and do NOT send again.", "",
             "THE MESSAGE TO SITAMAH, exactly this (POST it NOW through Zapier: Paul's standing instruction, no question; show it in your reply with the page and the PDF):", "  " + msg, "",
             "WHY THE FOLLOW-UP SENTENCE IS %s: %s" % (
                 "IN" if content["next_appointment"].get("agreed") else "OUT", content["next_appointment"].get("check", "")),
             "", "THE ZAPIER ROUTE (hard-coded, use exactly this):"]
    return "\n".join(lines + ["  " + z for z in page.zapier_steps(msg)])


def expand(text, run):
    return (text.replace("{run}", run).replace("{scripts}", SCRIPTS).replace("{skill_dir}", SKILL_DIR)
            .replace("{chunk_commands_pass1}", chunk_commands(run, 1))
            .replace("{chunk_commands_pass2}", chunk_commands(run, 2))
            .replace("{teams_message_block}", teams_block(run)))


# ------------------------------------------------------------------ preflight (S16 self-test)
def preflight(run=None):
    rows, ok = [], True

    def add(good, msg, fatal=True):
        nonlocal ok
        rows.append(("PASS" if good else ("FAIL" if fatal else "WARN"), msg))
        if not good and fatal:
            ok = False

    add(sys.version_info >= (3, 9), "python 3.9 or newer (this is %d.%d)" % sys.version_info[:2])
    try:
        import reportlab  # noqa: F401
        add(True, "reportlab (builds the PDF)")
    except ImportError:
        add(False, "reportlab is not installed: the PDF cannot be built")
    for tool, why, fatal in (("pdftotext", "checks the PDF text", True), ("pdftoppm", "renders the page images", True),
                             ("pandoc", "reads a .docx transcript", True)):
        add(shutil.which(tool) is not None, "%s (%s)" % (tool, why), fatal)
    add(w.stamp_display(w.skill_stamp()) is not None, "skill has a Last updated stamp (%s)" % w.version_short(), fatal=False)
    try:
        import zoneinfo
        zoneinfo.ZoneInfo("Europe/Athens")
        add(True, "Athens time zone (for the Last updated stamp)")
    except Exception:
        add(False, "Athens time zone data is missing (only needed when stamping a skill)", fatal=False)
    missing = []
    try:
        for s in steps_file()["steps"]:
            for r in refs_of(s):
                if not os.path.exists(os.path.join(SKILL_DIR, "references", r)):
                    missing.append(r)
    except SystemExit:
        missing.append("steps.json")
    add(not missing, "skill package complete (steps.json and every reference page)" if not missing
        else "skill package is missing: %s" % sorted(set(missing)))
    if run:
        try:
            os.makedirs(run, exist_ok=True)
            probe = p(run, ".write-test")
            open(probe, "w").close()
            os.remove(probe)
            add(True, "run folder is writable")
        except OSError as e:
            add(False, "run folder is not writable: %s" % e)
    return ok, rows


def print_preflight(rows):
    print("SELF-TEST")
    for lvl, msg in rows:
        print("  [%-4s] %s" % (lvl, msg))


# ------------------------------------------------------------------ steps
def show_step(run, rj, step):
    plist = applicable(rj)
    n = [s["id"] for s in plist].index(step["id"]) + 1
    print(RULE)
    print("STEP %d of %d: %s        [%s]" % (n, len(plist), step["title"], step["id"]))
    print(RULE)
    for line in step["do"]:
        print(expand(line, run))
    for r in refs_of(step):
        print("\nRULES FOR THIS STEP (references/%s):\n" % r)
        print(expand(read_ref(r), run))
    print("\nPROOF NEEDED: %s" % step["proof"])
    print("WHEN DONE RUN: python3 %s/run.py done %s %s" % (SCRIPTS, run, step["id"]))
    later = [s["title"] for s in plist[n:]]
    if later:
        print("COMING LATER (titles only): " + " | ".join(later))
    print(RULE)


def current_step(rj):
    for s in applicable(rj):
        if rj["steps"].get(s["id"], {}).get("state") != "done":
            return s
    return None


def cmd_start(a):
    ok, rows = preflight(a.run)
    print_preflight(rows)
    if not ok:
        print("\nSTOP. Tell Paul exactly which items failed above. Do NOT carry on, and do NOT replace the PDF or any "
              "other output with a text draft. Fix the environment first.")
        sys.exit(4)
    if os.path.exists(p(a.run, w.RUN)):
        print("\nThis run already exists. Showing where it is up to (use `status` / `next`).")
        return cmd_next(a)
    parts = a.client.split()
    if len(parts) < 2:
        w.die('--client must be the first name and surname, for example --client "Sam Testcase"')
    try:
        dt.datetime.strptime(a.date, "%d/%m/%Y")
    except ValueError:
        w.die("--date must be a real date as DD/MM/YYYY (taken from Paul's message), got %r" % a.date)
    rj = {"skill": "client-teams-transcript-skill", "meeting_type": a.type, "created": w.now(),
          "skill_stamp": w.skill_stamp(), "steps": {}, "client": {"first": parts[0], "surname": " ".join(parts[1:])}, "date": a.date}
    w.save_json(p(a.run, w.RUN), rj)
    for name in (w.SOURCES, w.ACCESS, w.QUESTIONS):
        w.save_json(p(a.run, name), [])
    w.save_json(p(a.run, w.LEDGER), {"entries": [], "scan_reviewed": []})
    w.save_json(p(a.run, w.RECEIPT), {})
    print("\nSAY THIS TO PAUL FIRST, before anything else in your reply, in exactly these words:\n    %s.\n"
          "(It comes from the skill's own Last updated stamp, so it changes with every update. The final printout repeats it.)" % w.version_line())
    print("\nRUN STARTED  type: %s   client: %s %s   meeting date: %s   skill version: %s"
          % (a.type, rj["client"]["first"], rj["client"]["surname"], a.date, w.stamp_display(rj["skill_stamp"]) or "unstamped"))
    print("Standing rules for the whole job:\n")
    print(expand(read_ref("00-rules.md"), a.run))
    print()
    show_step(a.run, rj, current_step(rj))


def cmd_next(a):
    rj = load_run(a.run)
    s = current_step(rj)
    if s is None:
        print("Every step is done. Run: python3 %s/verify.py %s  and put its whole printout in your reply." % (SCRIPTS, a.run))
        return
    show_step(a.run, rj, s)


def cmd_status(a):
    rj = load_run(a.run)
    cur = current_step(rj)
    print("RUN %s   type: %s   skill version: %s" % (a.run, rj["meeting_type"], w.stamp_display(rj.get("skill_stamp")) or "unstamped"))
    for s in applicable(rj):
        state = rj["steps"].get(s["id"], {}).get("state")
        mark = "DONE   " if state == "done" else ("NEXT ->" if cur and s["id"] == cur["id"] else "waiting")
        print("  [%s] %-10s %s" % (mark, s["id"], s["title"]))
    skipped = [s["id"] for s in steps_file()["steps"] if rj["meeting_type"] not in s["applies"]]
    if skipped:
        print("  not applicable to a %s: %s" % (rj["meeting_type"], ", ".join(skipped)))
    if cur:
        print("\nNEXT: python3 %s/run.py next %s" % (SCRIPTS, a.run))


# ------------------------------------------------------------------ proofs
def ck_access_transcript(run, rj):
    errs = []
    if not (rj.get("computer") or {}).get("found"):
        errs.append("the computer is not connected: connect first and record it (python3 %s/run.py computer %s --device ... --folder ... --listing ...), or --none \"<what happened>\" for the STOP" % (SCRIPTS, run))
    ok = [e for e in load_list(run, w.ACCESS) if e.get("need") == "transcript" and e.get("result") == "ok"]
    if not ok:
        errs.append("no successful access entry for 'transcript' (run.py access ... --need transcript ... --result ok)")
    return errs


def ck_prep_done(run, rj):
    path = p(run, w.STATE)
    if not os.path.exists(path):
        return ["tx.py prep has not been run"]
    st = w.load_json(path)
    return [] if st["complete"] else ["the transcript is incomplete: %s" % "; ".join(st["notes"])]


def ck_sources_ok(run, rj):
    R = verify.Results()
    verify.check_sources(run, rj["meeting_type"], R)
    return [m for lvl, _, m in R.rows if lvl == "FAIL"]


def _state(run):
    return w.load_json(p(run, w.STATE), "state.json")


def unacked(run, p):
    st = _state(run)
    led = load_list_ledger(run)
    return [c for c in range(1, len(st["chunks"]) + 1) if not tx.chunk_acked(st, led, p, c)]


def ck_pass1(run, rj):
    errs = []
    if not tx.passes_done(_state(run))[0]:
        errs.append("Pass 1 has not served every chunk (see `tx.py status %s`)" % run)
    if not (load_list_ledger(run).get("entries")):
        errs.append("the ledger is empty: record decisions, requests and figures with run.py ledger add")
    if unacked(run, 1):
        errs.append("Pass 1 chunks %s have no ledger entry or reasoned acknowledgement" % unacked(run, 1))
    return errs


def ck_pass2(run, rj):
    errs = [] if tx.passes_done(_state(run))[1] else ["Pass 2 has not served every chunk (see `tx.py status %s`)" % run]
    if unacked(run, 2):
        errs.append("Pass 2 chunks %s have no ledger entry or reasoned acknowledgement" % unacked(run, 2))
    return errs


def ck_scan(run, rj):
    return [] if _state(run).get("scan") else ["the keyword scan has not been run (tx.py scan)"]


def ck_verify(stage):
    def check(run, rj):
        R, st, ledger, content = verify.run_checks(run, stage)
        if stage == "final":
            verify.report_short(R, st, ledger, content, stage, run)   # the SHORT audit goes into the chat; the full report is out_record/audit-full.txt
        return [m for lvl, _, m in R.rows if lvl == "FAIL"][:15]
    return check


def ck_build(run, rj):
    st = _state(run)
    cp = p(run, w.CONTENT)
    if not st.get("build") or not os.path.exists(cp):
        return ["the outputs have not been built (build.py)"]
    if st["build"]["content_sha"] != w.content_hash(w.load_json(cp)):
        return ["content.json changed after the build: run build.py again"]
    return []


def rc_get(run, dotted):
    d = w.load_json(p(run, w.RECEIPT)) if os.path.exists(p(run, w.RECEIPT)) else {}
    for k in dotted.split("."):
        d = d.get(k) if isinstance(d, dict) else None
    return d


def ck_judgment(run, rj):
    errs = ck_receipt("independent_check", n=10)(run, rj)
    for k in verify.JUDGMENT_KEYS:
        errs += ck_receipt("judgment." + k, n=12)(run, rj)
    if rj["meeting_type"] != "first":
        errs += ck_receipt("png_visual_check", n=20)(run, rj)
    return errs


def ck_receipt(*keys, n=1):
    def check(run, rj):
        return ["receipt is missing '%s' (run.py receipt --set %s=...)" % (k, k) for k in keys
                if len(str(rc_get(run, k) or "").strip()) < n]
    return check


def ck_planner(run, rj):
    mode = rc_get(run, "planner_page.mode")
    if mode == "artifact":
        return ck_receipt("planner_page.url")(run, rj)
    if mode == "fallback_text":
        return ck_receipt("planner_page.reason", n=10)(run, rj)
    return ["planner_page.mode must be artifact or fallback_text"]


def ck_pdf_saved(run, rj):
    """The PDF is saved ON THE COMPUTER with device_commit_files; the computer's own fingerprint of the saved file must equal the PDF this run built."""
    keys = ("pdf_sent_in_chat", "saved.tool", "saved.folder", "saved.filename", "saved.tool_result", "saved.folder_listing_check", "saved.device_output")
    errs = ck_receipt(*keys)(run, rj)
    if errs:
        return errs
    if "device_commit_files" not in str(rc_get(run, "saved.tool")):
        errs.append("saved.tool must be device_commit_files: the PDF is saved on the computer, never through Microsoft 365 or Zapier")
    b = _state(run).get("build") or {}
    dsha, dsize, why = w.parse_device_output(str(rc_get(run, "saved.device_output")), str(b.get("pdf")))
    if why:
        errs.append("saved.device_output: " + why)
    elif dsha != b.get("pdf_sha") or dsize != b.get("pdf_size"):
        errs.append("the PDF on the computer is not the PDF built here (computer: %d bytes, %s...; built: %s bytes, %s...): commit it again and fingerprint it again"
                    % (dsize, dsha[:12], b.get("pdf_size"), str(b.get("pdf_sha"))[:12]))
    return errs


def ck_teams(run, rj):
    st = rc_get(run, "teams.status")
    if st not in ("sent", "already_sent", "declined", "failed"):
        return ["teams.status must be sent, already_sent, declined or failed"]
    need = {"sent": ("teams.message_id", "teams.sent_time", "teams.body_as_stored", "teams.approved_by_paul"),
            "already_sent": ("teams.already_sent_evidence",), "declined": ("teams.paul_said",), "failed": ("teams.detail",)}[st]
    return ck_receipt(*need)(run, rj)


CHECKS = {
    "access_transcript": ck_access_transcript, "prep_done": ck_prep_done, "sources_ok": ck_sources_ok,
    "pass1_done": ck_pass1, "pass2_done": ck_pass2, "scan_done": ck_scan, "verify_pre": ck_verify("pre"),
    "build_fresh": ck_build, "receipt_check": ck_judgment, "receipt_planner": ck_planner,
    "receipt_pdf": ck_pdf_saved,
    "receipt_apps": ck_receipt("applications_handoff"), "receipt_teams": ck_teams, "verify_final": ck_verify("final"),
}


def cmd_done(a):
    rj = load_run(a.run)
    plist = applicable(rj)
    ids = [s["id"] for s in plist]
    if a.step not in ids:
        w.die("'%s' is not a step of this run. Steps: %s" % (a.step, ", ".join(ids)))
    cur = current_step(rj)
    if cur is None or ids.index(a.step) > ids.index(cur["id"]):
        w.die("REFUSED: finish step '%s' first. Steps are done in order, none skipped." % (cur["id"] if cur else "?"), 3)
    step = plist[ids.index(a.step)]
    fails = CHECKS[step["check"]](a.run, rj)
    if fails:
        print("NOT DONE: step '%s' is missing its proof:" % a.step)
        for f in fails:
            print("  - " + f)
        print("\nFix this, then run `done %s` again. You cannot move on until it passes." % a.step)
        sys.exit(1)
    rj["steps"][a.step] = {"state": "done", "t": w.now()}
    w.save_json(p(a.run, w.RUN), rj)
    print("STEP '%s' DONE.\n" % a.step)
    nxt = current_step(rj)
    if nxt is None:
        print("EVERY STEP IS DONE. The job is finished only when your reply contains the verify.py printout "
              "(it was shown above if the last step was `final`).")
        return
    show_step(a.run, rj, nxt)


# ------------------------------------------------------------------ ledger
def load_list_ledger(run):
    path = p(run, w.LEDGER)
    return w.load_json(path) if os.path.exists(path) else {"entries": [], "scan_reviewed": []}


def cmd_ledger(a):
    led = load_list_ledger(a.run)
    save = lambda: w.save_json(p(a.run, w.LEDGER), led)  # noqa: E731
    if a.action == "list":
        for e in led["entries"]:
            cov = ",".join(e.get("covered_by") or []) or ("EXCLUDED" if e.get("excluded") else "NOT COVERED")
            print("%-5s line %-5s %-11s %-12s %s" % (e["id"], e["line"], e["kind"], cov, e["quote"][:70]))
        print("%d entries, %d scan reviews" % (len(led["entries"]), len(led["scan_reviewed"])))
        return
    if a.action == "add":
        if not os.path.exists(p(a.run, w.TRANSCRIPT)):
            w.die("REFUSED: the transcript has not been prepared yet (tx.py prep).")
        lines = w.read_lines(a.run)
        if a.kind not in LEDGER_KINDS:
            w.die("kind must be one of %s" % LEDGER_KINDS)
        if not 1 <= a.line <= len(lines) or not verify.quote_ok(lines, a.line, a.quote):
            w.die("REFUSED: that quote is not found at transcript line %d. Copy the exact words from the chunk you read." % a.line)
        st = _state(a.run)
        in_pass2 = any(r["pass"] == 2 for r in st["reads"])
        e = {"id": "L%d" % (len(led["entries"]) + 1), "line": a.line, "kind": a.kind, "quote": a.quote,
             "pass": 2 if in_pass2 else 1, "covered_by": []}
        if a.speaker:
            e["speaker"] = a.speaker
        if a.meaning:
            e["meaning"] = a.meaning
        led["entries"].append(e)
        save()
        print("%s added (%s, line %d, pass %d)%s" % (e["id"], a.kind, a.line, e["pass"],
              "  - must be covered by an item in content.json" if a.kind in verify.KINDS_MUST_COVER else ""))
        return
    ent = {e["id"]: e for e in led["entries"]}
    if a.action == "cover":
        cp = p(a.run, w.CONTENT)
        if not os.path.exists(cp):
            w.die("REFUSED: write content.json first; items must exist before they can cover a ledger entry.")
        idx, _ = verify.item_index(w.load_json(cp))
        if a.id not in ent:
            w.die("no ledger entry %s" % a.id)
        bad = [i for i in a.items if i not in idx]
        if bad:
            w.die("REFUSED: these item ids are not in content.json: %s" % bad)
        ent[a.id]["covered_by"] = sorted(set(ent[a.id].get("covered_by") or []) | set(a.items))
        save()
        print("%s covered by %s" % (a.id, ent[a.id]["covered_by"]))
    elif a.action == "exclude":
        if a.id not in ent:
            w.die("no ledger entry %s" % a.id)
        if ent[a.id]["kind"] not in verify.KINDS_OPTIONAL:
            w.die("REFUSED: a %s entry cannot be excluded: it must map to a bullet or action." % ent[a.id]["kind"])
        if len(a.reason.strip()) < 8:
            w.die("REFUSED: give a real reason (at least 8 characters).")
        ent[a.id]["excluded"] = a.reason
        save()
        print("%s excluded: %s" % (a.id, a.reason))
    elif a.action == "review":
        if len(a.reason.strip()) < 6:
            w.die("REFUSED: give a real reason.")
        if a.line is None and (a.frm is None or a.to is None):
            w.die("REFUSED: give --line N or --from A --to B.")
        rec = {"line": a.line, "reason": a.reason} if a.line is not None else {"from": a.frm, "to": a.to, "reason": a.reason}
        led["scan_reviewed"].append(rec)
        save()
        print("scan hit(s) %s reviewed: %s" % (a.line if a.line is not None else "%d-%d" % (a.frm, a.to), a.reason))
    elif a.action == "ack":
        st = _state(a.run)
        if a.pass_ not in (1, 2) or not 1 <= a.chunk <= len(st["chunks"]):
            w.die("REFUSED: --pass must be 1 or 2 and --chunk 1..%d." % len(st["chunks"]))
        if not any(r["pass"] == a.pass_ and r["chunk"] == a.chunk for r in st["reads"]):
            w.die("REFUSED: chunk %d of Pass %d has not been read yet." % (a.chunk, a.pass_))
        if len(a.reason.strip()) < 20:
            w.die("REFUSED: say in your own words what this chunk contained and why it holds nothing to record (at least 20 characters).")
        led.setdefault("chunk_acks", []).append({"pass": a.pass_, "chunk": a.chunk, "reason": a.reason, "t": w.now()})
        save()
        print("chunk %d of Pass %d acknowledged." % (a.chunk, a.pass_))


# ------------------------------------------------------------------ logs
def cmd_computer(a):
    """Records how this chat reaches the client's OneDrive folder on the computer. In a cloud chat the computer is a separate machine reached through the device tools
    (the chat connects, lists the client's folder and records it here); where the folder is mounted into this machine (a test) the program finds it itself."""
    rj = load_run(a.run)
    if a.none:
        if len(a.none.strip()) < 8:
            w.die("REFUSED: say what happened to the connection (at least 8 characters).")
        rj["computer"] = {"found": False, "t": w.now(), "detail": a.none.strip()}
        w.save_json(p(a.run, w.RUN), rj)
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
        w.save_json(p(a.run, w.RUN), rj)
        print("COMPUTER CONNECTED through the device tools (%s, folder %s). Take the transcript and every client document from it as page 01 says." % (a.device.strip(), a.folder.strip()))
        return
    root = w.find_computer_root()
    if root:
        rj["computer"] = {"found": True, "mode": "mount", "root": root, "t": w.now()}
        w.save_json(p(a.run, w.RUN), rj)
        print("COMPUTER FOUND: the client's OneDrive folder is mounted at %s. Copy each file with cp and log it with --original." % root)
        return
    print("No connection is recorded yet. Connect with the device tools (page 01: get_device_info, then device_request_folder_access for ~/liferisk.co.za if it is not connected, then device_list_dir "
          "on the client's folder) and record it: python3 %s/run.py computer %s --device <name> --folder <granted folder> --listing \"<the file names>\"   "
          "If the connection is refused or cannot be made: python3 %s/run.py computer %s --none \"<what happened>\"" % (SCRIPTS, a.run, SCRIPTS, a.run))
    sys.exit(6)


def prove_copy(a, rj, need):
    """A file taken from the computer is accepted only when the copy is identical to the original: either the computer's own fingerprint
    (sha256sum and stat run with device_bash, pasted whole) or, where the folder is mounted into this machine, the original itself.
    Returns (verified, bytes, sha256, detail). Refuses when the proof is missing; a copy that differs is returned as not verified."""
    if not (rj.get("computer") or {}).get("found"):
        w.die("REFUSED: no computer connection is recorded in this run (run.py computer %s). A try on the computer is logged only when it is connected." % a.run)
    if not a.file or not (a.device_output or a.original):
        w.die("REFUSED: a file taken from the computer needs its proof: --file <your copy> with --device-output <the whole output of sha256sum and stat run on the computer with device_bash> "
              "(or --original, where the folder is mounted into this machine). Nobody is asked for anything.")
    if a.device_output and a.original:
        w.die("REFUSED: give --original (a mounted folder) or --device-output (the computer's own fingerprint), not both.")
    if not os.path.isfile(a.file):
        w.die("MISSING: the copy %s" % a.file)
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
        return True, got, sha, "copy verified: identical to the file on the computer (%d bytes, sha256 %s...)" % (got, sha[:12])
    return False, got, sha, "copy NOT identical to the file on the computer (%d bytes saved)" % got


def cmd_access(a):
    rj = load_run(a.run)
    log = load_list(a.run, w.ACCESS)
    detail, result, entry = a.detail or "", a.result, {}
    if a.route in ("m365", "zapier") and a.result == "ok" and a.need in w.DOC_KINDS:
        w.die("REFUSED: a %s cannot be taken through %s: a PDF or Word file arrives there cut off, as text. Take it from the computer (--route device, with --file and --device-output)."
              % (a.need, "Microsoft 365" if a.route == "m365" else "Zapier"))
    if a.route == "device" and a.result == "ok":
        verified, got, sha, why = prove_copy(a, rj, a.need)
        detail = (detail + " ").lstrip() + why
        entry = {"verified": verified, "bytes": got, "sha256": sha, "file": os.path.basename(a.file)}
        if not verified:
            result = "fail"
            print("logged as a FAIL: the copy is not identical to the file on the computer. Stage it again (device_stage_files) and compare again.")
    elif a.file or a.device_output or a.original:
        w.die("REFUSED: --file, --device-output and --original are for the computer route (--route device --result ok).")
    log.append({"t": w.now(), "need": a.need, "route": a.route, "tool": a.tool, "result": result, "detail": detail, **entry})
    w.save_json(p(a.run, w.ACCESS), log)
    es = [e for e in log if e["need"] == a.need]
    if any(e["result"] == "ok" for e in es):
        print("logged: '%s' obtained via %s." % (a.need, a.route))
        return
    failed = {e["route"] for e in es if e["result"] == "fail"}
    untried = [r for r in w.ROUTES if r not in failed]
    if untried:
        print("logged failure. NEXT ROUTE TO TRY for '%s': %s (%s). Go on to it at once; do not ask Paul anything."
              % (a.need, untried[0], w.ROUTE_NAMES[untried[0]]))
    else:
        print("logged failure. All three routes have now failed for '%s'. Say so in at most five lines (the log of the tries) and stop. Never ask Paul to attach or upload anything." % a.need)


def cmd_source(a):
    srcs = load_list(a.run, w.SOURCES)
    if a.kind not in w.SOURCE_KINDS:
        w.die("kind must be one of %s" % w.SOURCE_KINDS)
    if a.none:
        if len(a.none.strip()) < 8:
            w.die("REFUSED: say what you searched and where (at least 8 characters).")
        tried = {e.get("route") for e in load_list(a.run, w.ACCESS) if e.get("need") == a.kind and e.get("result") == "fail"}
        if len(tried & set(w.ROUTES)) < 2:
            w.die("REFUSED: you may say there is no %s on file only after searching on at least two routes (device, m365, zapier) and logging each: "
                  "run.py access %s --need %s --route device --tool <tool> --result fail --detail \"nothing found in <where>\"." % (a.kind, a.run, a.kind))
        srcs.append({"kind": a.kind, "none": a.none})
    else:
        if not (a.path and a.date and a.read == "yes"):
            w.die("REFUSED: a document needs --path, --date and --read yes (or use --none \"reason\").")
        ref = a.ref or re.sub(r"\.[A-Za-z0-9]{1,5}$", "", re.split(r"[\\/]", a.path.strip())[-1])
        if any(verify.source_ref(e) == ref for e in srcs if e.get("read") == "yes"):
            w.die("REFUSED: a document called %r is already recorded; give this one its own --ref." % ref)
        entry = {"kind": a.kind, "path": a.path, "date": a.date, "read": "yes", "ref": ref}
        text = None
        if a.kind in w.DOC_KINDS:
            # a client document is a whole file on the computer: proved identical by the computer's own fingerprint, and the text is made by the program from that copy
            rj = load_run(a.run)
            verified, got, sha, why = prove_copy(a, rj, a.kind)
            named = re.split(r"[\\/]", a.path.strip())[-1].lower()
            if named != os.path.basename(a.file).lower():
                w.die("REFUSED: --path names %r but the copy is %r: record the file you really took." % (named, os.path.basename(a.file)))
            log = load_list(a.run, w.ACCESS)
            log.append({"t": w.now(), "need": a.kind, "route": "device", "tool": a.tool or "device_stage_files", "result": "ok" if verified else "fail",
                        "detail": why, "verified": verified, "bytes": got, "sha256": sha, "file": os.path.basename(a.file)})
            w.save_json(p(a.run, w.ACCESS), log)
            if not verified:
                w.die("REFUSED: the copy is not identical to the file on the computer (logged as a fail). Stage it again (device_stage_files) and compare again.")
            entry.update(via="device", bytes=got, sha256=sha, file=os.path.basename(a.file))
            text = w.doc_text(a.file)
            if text is None:
                w.die("REFUSED: the program cannot read a %s file. Give a PDF, a Word file or a text file." % os.path.splitext(a.file)[1])
            if not text.strip():
                if not a.text_file:
                    print("NOTE: this document holds no text the program can read (a scan). Its quotes and figures cannot be machine-checked unless you give --text-file with the text you read from the page images (Paul will be told).")
                else:
                    text = open(a.text_file, encoding="utf-8", errors="replace").read()
                    entry["text_from"] = "the chat (the program found no text in the file)"
            elif a.text_file:
                w.die("REFUSED: --text-file is not needed: the program made the text of this document from the verified copy itself.")
        elif a.text_file:
            if not os.path.exists(a.text_file):
                w.die("REFUSED: text file not found: %s" % a.text_file)
            text = open(a.text_file, encoding="utf-8", errors="replace").read()
        elif a.file or a.device_output or a.original:
            w.die("REFUSED: --file, --device-output and --original are for the client's documents, not for %s." % a.kind)
        if text is not None and text.strip():
            os.makedirs(os.path.join(a.run, w.DOCS), exist_ok=True)
            with open(os.path.join(a.run, w.DOCS, ref + ".txt"), "w", encoding="utf-8") as fh:
                fh.write(text)
            entry["text"] = True
        srcs.append(entry)
    w.save_json(p(a.run, w.SOURCES), srcs)
    print("recorded %s source (%d so far)%s." % (a.kind, len(srcs), "" if a.none or srcs[-1].get("text") else
          ". NOTE: no --text-file given, so quotes and figures from this document cannot be machine-checked (Paul will be told)"))


def cmd_ask(a):
    log = load_list(a.run, w.ACCESS)
    es = [e for e in log if e["need"] == a.need]
    if a.kind == "file":
        if not es:
            w.die("REFUSED: no access attempts are logged for '%s'. Try the routes first (run.py access)." % a.need)
        if any(e["result"] == "ok" for e in es):
            w.die("REFUSED: '%s' was obtained, so there is nothing to ask Paul." % a.need)
        failed = {e["route"] for e in es if e["result"] == "fail"}
        untried = [r for r in w.ROUTES if r not in failed]
        if untried:
            w.die("REFUSED: these routes have not been tried for '%s': %s. Never ask Paul before all three failed." % (a.need, untried))
    if len(a.searched.strip()) < 8:
        w.die("REFUSED: say what you already searched (at least 8 characters).")
    qs = load_list(a.run, w.QUESTIONS)
    qs.append({"t": w.now(), "need": a.need, "question": a.question, "searched": a.searched, "kind": a.kind})
    w.save_json(p(a.run, w.QUESTIONS), qs)
    print("RECORDED. Now ask Paul, in plain words, exactly this:\n")
    print("  %s" % a.question)
    print("  (I already looked in: %s)" % a.searched)
    for e in es:
        print("  - tried %s via %s: %s %s" % (w.ROUTE_NAMES.get(e["route"], e["route"]), e["tool"], e["result"], e.get("detail", "")))


def cmd_receipt(a):
    path = p(a.run, w.RECEIPT)
    rc = w.load_json(path) if os.path.exists(path) else {}
    for kv in a.set:
        if "=" not in kv:
            w.die("--set needs key=value, got %r" % kv)
        key, val = kv.split("=", 1)
        v = True if val == "true" else (False if val == "false" else val)
        d = rc
        parts = key.split(".")
        for k in parts[:-1]:
            d = d.setdefault(k, {})
        d[parts[-1]] = v
        stp = rc.setdefault("_stamps", {})
        stp[parts[0]] = (_state(a.run).get("build") or {}).get("content_sha", "none")
    w.save_json(path, rc)
    print("receipt updated (%d top-level fields)." % len(rc))


# ------------------------------------------------------------------ cli
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add(name, fn, *args, **kw):
        sp = sub.add_parser(name)
        for arg in args:
            sp.add_argument(arg)
        sp.set_defaults(fn=fn)
        return sp

    sp = add("start", cmd_start, "run")
    sp.add_argument("--type", required=True, choices=["followup", "first", "whatsapp"])
    sp.add_argument("--client", required=True, help='the client exactly as in Paul\'s message, "First Surname"')
    sp.add_argument("--date", required=True, help="the meeting date from Paul's message, DD/MM/YYYY")
    add("next", cmd_next, "run")
    sp = add("done", cmd_done, "run", "step")
    add("status", cmd_status, "run")
    sp = sub.add_parser("preflight")
    sp.set_defaults(fn=lambda a: (lambda r: (print_preflight(r[1]), sys.exit(0 if r[0] else 4)))(preflight()))

    sp = add("computer", cmd_computer, "run")
    sp.add_argument("--device", help="the computer's name (get_device_info)")
    sp.add_argument("--folder", help="the folder the connection was granted for (liferisk.co.za)")
    sp.add_argument("--listing", help="the file names device_list_dir showed in the client's folder")
    sp.add_argument("--none", help="the connection was refused or could not be made: what happened (prints the STOP)")
    sp = add("access", cmd_access, "run")
    sp.add_argument("--need", required=True)
    sp.add_argument("--route", required=True, choices=list(verify.ALLOWED_ROUTES))
    sp.add_argument("--tool", required=True)
    sp.add_argument("--result", required=True, choices=["ok", "fail"])
    sp.add_argument("--detail")
    sp.add_argument("--file", help="your copy of the file taken from the computer (the staged copy)")
    sp.add_argument("--device-output", dest="device_output", help="the whole output of sha256sum and stat -c %%s for that file, run on the computer with device_bash")
    sp.add_argument("--original", help="where the client's folder is mounted into this machine: the original file (the program compares it with the copy itself)")
    sp = add("source", cmd_source, "run")
    sp.add_argument("--tool", help="the tool used (default device_stage_files)")
    sp.add_argument("--file", help="a client document: your copy taken from the computer (the program proves it and makes the text from it)")
    sp.add_argument("--device-output", dest="device_output", help="the whole output of sha256sum and stat -c %%s for that file, run on the computer with device_bash")
    sp.add_argument("--original", help="where the client's folder is mounted into this machine: the original file")
    sp.add_argument("--kind", required=True)
    sp.add_argument("--path")
    sp.add_argument("--date")
    sp.add_argument("--read", choices=["yes"])
    sp.add_argument("--none")
    sp.add_argument("--ref", help="a short name for this document; item sources cite it (default: the file name)")
    sp.add_argument("--text-file", dest="text_file", help="correspondence: the text of the email or page, saved to a file, so quotes and figures can be checked (a client document needs --file instead; the program makes its text)")
    sp = add("ask", cmd_ask, "run")
    sp.add_argument("--need", required=True)
    sp.add_argument("--question", required=True)
    sp.add_argument("--searched", required=True)
    sp.add_argument("--kind", choices=["file", "knowledge"], default="file")
    sp = add("receipt", cmd_receipt, "run")
    sp.add_argument("--set", action="append", default=[])

    sp = add("ledger", cmd_ledger, "run")
    lsub = sp.add_subparsers(dest="action", required=True)
    x = lsub.add_parser("add")
    x.add_argument("--line", type=int, required=True)
    x.add_argument("--kind", required=True)
    x.add_argument("--quote", required=True)
    x.add_argument("--speaker")
    x.add_argument("--meaning")
    x = lsub.add_parser("cover")
    x.add_argument("id")
    x.add_argument("items", nargs="+")
    x = lsub.add_parser("exclude")
    x.add_argument("id")
    x.add_argument("reason")
    x = lsub.add_parser("review")
    x.add_argument("--line", type=int)
    x.add_argument("--from", dest="frm", type=int)
    x.add_argument("--to", type=int)
    x.add_argument("--reason", required=True)
    x = lsub.add_parser("ack")
    x.add_argument("--pass", dest="pass_", type=int, required=True)
    x.add_argument("--chunk", type=int, required=True)
    x.add_argument("--reason", required=True)
    lsub.add_parser("list")

    a = ap.parse_args()
    if getattr(a, "run", None):
        a.run = os.path.abspath(a.run)
    a.fn(a)


if __name__ == "__main__":
    main()
