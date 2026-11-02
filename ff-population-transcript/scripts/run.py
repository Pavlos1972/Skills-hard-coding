#!/usr/bin/env python3
"""Step driver for the ff-population-transcript skill (SKILL-STANDARDS.md S16).

  run.py start   <run_dir> --client "First Surname" --date DD/MM/YYYY [--spouse "First Surname" [--spouse-run DIR]]
  run.py next    <run_dir>            show the current step again
  run.py done    <run_dir> <step>     check the proof; only then move on
  run.py status  <run_dir>            where the job is up to (also the recovery point after a long chat)
  run.py preflight                    the self-test on its own

  run.py access  <run_dir> --need N --route device|m365|zapier|user|passed --tool T --result ok|fail [--detail D]
  run.py ask     <run_dir> --need N [--question Q] --searched S [--kind file|knowledge]
  run.py answer  <run_dir> --need N --said "Paul's own words" [--choice manual|transcript]
  run.py form    <run_dir> <form data file> [--again]       read it with the program (schema, statuses, look-up check ...)
  run.py formpdf <run_dir> <form saved PDF> | --none REASON  the form's saved PDF is a source too
  run.py pdfreview <run_dir> --key K --result format_only|disagree --quote Q [--pdf-value V]
  run.py source  <run_dir> --kind K (--path P --date YYYY-MM-DD --read yes [--ref NAME] [--text-file F] | --none REASON)
  run.py join    <run_dir> <transcript 1> <transcript 2> ...   several transcripts of one meeting -> one file to prep
  run.py continuity <run_dir> --between 1,2 --result ok|gap --detail D
  run.py ledger  <run_dir> add --line N --kind K --quote Q [--speaker S] [--meaning M]
  run.py ledger  <run_dir> cover <ledger id> <item id> [<item id> ...]  | exclude <id> <reason> | ack --pass 1|2 --chunk N --reason R
  run.py ledger  <run_dir> review (--line N | --from A --to B) --reason R | list
  run.py lead    <run_dir> --folder-result found|none --mailbox-result found|none|skipped [--received DD/MM/YYYY --ref NAME --quote Q]
  run.py cross   <run_dir> (--file answers.json | --key K --r same|differs|not_on_call [--line N --quote Q --value V]) [--rest not_on_call --reviewed R]
  run.py claim   <run_dir> (--all-empty | --key K --as "Not discussed"|Requested|N/A [--reviewed R] [--searched S] [--terms a,b])
  run.py compose <run_dir>            write content.json from the form, the overlay and the recorded answers
  run.py spouse  <run_dir>            search this document for the other spouse's data (two spouses in one meeting)
  run.py receipt <run_dir> --set a.b=value [--set ...]

The program shows one step at a time and will not show the next until the proof for this one is on file.
It is run as it is; it is never edited during a run.
"""
import argparse
import datetime as dt
import json
import os
import re
import shutil
import sys
import types

import build
import compose
import ffform
import tx
import verify
import wrlib as w

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPTS)
RULE = "-" * 78
FORM_QUESTION = ("The Fact Find form's data file for %s was not found on any of the three routes (the computer, Microsoft 365, Zapier). "
                 "Should I use the filled-in Manual Fact Find PDF as the first source, or work from the transcript alone?")


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


def save_run(run, rj):
    w.save_json(p(run, w.RUN), rj)


def applicable(rj):
    return steps_file()["steps"]


def refs_of(step):
    r = step.get("ref") or []
    return [r] if isinstance(r, str) else r


def read_ref(name):
    path = os.path.join(SKILL_DIR, "references", name)
    if not os.path.exists(path):
        return "(MISSING reference page %s: the skill package is broken; tell Paul)" % name
    with open(path, encoding="utf-8") as f:
        return f.read().rstrip()


def chunk_commands(run, pass_no):
    st = w.load_json(p(run, w.STATE)) if os.path.exists(p(run, w.STATE)) else None
    k = len(st["chunks"]) if st else 0
    if not k:
        return "(chunk commands appear once `tx.py prep` has run)"
    return ("  python3 %s/tx.py chunk %s %d 1     (%d chunks in all; each chunk prints the command for the next one, and the next is\n"
            "  refused until this one has ledger entries or a reasoned acknowledgement)" % (SCRIPTS, run, pass_no, k))


def font_line():
    rec = build.pick_font()
    if rec["family"] == "Aptos":
        return "Font: Aptos was found and will be used."
    return "Font: Aptos is NOT installed here; the PDF will be set in %s. Tell Paul in your reply (never say Aptos)." % rec["family"]


def valid_ids_text():
    v = compose.valid_ids(w.layout())
    lists = "; ".join("%s (%s)" % (k, ", ".join(c) if c else "any column") for k, c in sorted(v["lists"].items()))
    return ("section ids for notes/flags: %s. List names for rows_add/joint (and their columns): %s. Quote groups: %s. ABI keys: %s. Field keys for fills/diffs (or list.row.column such as debts.0.cl; rows count from 0): %s."
            % (", ".join(v["sections"]), lists, ", ".join(v["groups"]), ", ".join(v["abi"]), ", ".join(v["keys"])))


def expand(text, run):
    return (text.replace("{run}", run).replace("{scripts}", SCRIPTS).replace("{skill_dir}", SKILL_DIR)
            .replace("{chunk_commands_pass1}", chunk_commands(run, 1)).replace("{chunk_commands_pass2}", chunk_commands(run, 2))
            .replace("{font_line}", font_line()).replace("{valid_ids}", valid_ids_text()))


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
        add(True, "reportlab (draws the PDF)")
    except ImportError:
        add(False, "reportlab is not installed: the PDF cannot be built")
    for tool, why, fatal in (("pdftotext", "reads the form's saved PDF and checks the PDF text", True), ("pdftoppm", "renders the page images", True),
                             ("pdffonts", "proves which font is really inside the PDF", True), ("pandoc", "reads a .docx transcript", True)):
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
    add(not missing, "skill package complete (steps.json and every reference page)" if not missing else "skill package is missing: %s" % sorted(set(missing)))
    try:
        lay = w.layout()
        add(bool(lay["sections"]) and lay["schema"] == w.SCHEMA, "layout.json present (schema %s, %d sections)" % (lay["schema"], len(lay["sections"])))
    except (SystemExit, KeyError):
        add(False, "layout.json is missing or broken")
    rec = build.pick_font()
    add(rec["family"] == "Aptos", font_line(), fatal=False)
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
    parts = a.client.split()
    first, surname = (a.first, a.surname) if (a.first and a.surname) else ((parts[0], " ".join(parts[1:])) if len(parts) >= 2 else (None, None))
    if not first:
        w.die('--client must be the first name and surname, for example --client "Pat Samplecase" (for several first names give --first "Pat Jo" --surname "Samplecase")')
    if w.parse_date(a.date) is None:
        w.die("--date must be a real date as DD/MM/YYYY (taken from Paul's message), got %r" % a.date)
    if os.path.exists(p(a.run, w.RUN)):
        old = w.load_json(p(a.run, w.RUN))
        oc = old.get("client", {})
        if not (w.same_person(first, surname, oc.get("first", ""), oc.get("surname", "")) and old.get("date") == a.date):
            w.die("REFUSED: this run folder already belongs to %s %s, meeting date %s. Start the new job in a NEW run folder (you asked for %s %s, %s)."
                  % (oc.get("first"), oc.get("surname"), old.get("date"), first, surname, a.date), 2)
    ok, rows = preflight(a.run)
    print_preflight(rows)
    if not ok:
        print("\nSTOP. Tell Paul exactly which items failed above. Do NOT carry on, and do NOT replace the PDF or any other output with a text draft. Fix the environment first.")
        sys.exit(4)
    if os.path.exists(p(a.run, w.RUN)):
        print("\nThis run already exists (same client and date). Showing where it is up to (use `status` / `next`).")
        return cmd_next(a)
    rj = {"skill": w.skill_name(), "meeting_type": "factfind", "created": w.now(), "skill_stamp": w.skill_stamp(), "steps": {},
          "client": {"first": first, "surname": surname}, "date": a.date, "form_mode": "pending", "program_fingerprint": w.program_fingerprint()}
    if len(parts) > 2 and not (a.first and a.surname):
        print("NOTE: taking %r as the first name and %r as the surname. The form's name is compared as a whole, so a different split does not matter; to be exact use --first and --surname." % (first, surname))
    if a.spouse:
        sp = a.spouse.split()
        rj["spouse"] = {"name": a.spouse, "first": sp[0], "surname": " ".join(sp[1:]), "run": os.path.abspath(a.spouse_run) if a.spouse_run else None}
    save_run(a.run, rj)
    for name in (w.SOURCES, w.ACCESS, w.QUESTIONS):
        w.save_json(p(a.run, name), [])
    w.save_json(p(a.run, w.LEDGER), {"entries": [], "scan_reviewed": []})
    w.save_json(p(a.run, w.RECEIPT), {})
    w.save_json(p(a.run, w.OVERLAY), {})
    w.save_json(p(a.run, w.CLAIMS), {})
    print("\nSAY THIS TO PAUL FIRST, before anything else in your reply, in exactly these words:\n    %s.\n"
          "(It comes from the skill's own Last updated stamp, so it changes with every update. The final printout repeats it.)" % w.version_line())
    print("\nRUN STARTED  client: %s %s   meeting date: %s   skill version: %s%s"
          % (rj["client"]["first"], rj["client"]["surname"], a.date, w.stamp_display(rj["skill_stamp"]) or "unstamped", ("   TWO SPOUSES: this run is for %s only" % a.client) if a.spouse else ""))
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
    print("RUN %s   client: %s %s   skill version: %s   form: %s" % (a.run, rj["client"]["first"], rj["client"]["surname"], w.stamp_display(rj.get("skill_stamp")) or "unstamped", rj.get("form_mode")))
    for s in applicable(rj):
        state = rj["steps"].get(s["id"], {}).get("state")
        mark = "DONE   " if state == "done" else ("NEXT ->" if cur and s["id"] == cur["id"] else "waiting")
        print("  [%s] %-10s %s" % (mark, s["id"], s["title"]))
    if cur:
        print("\nNEXT: python3 %s/run.py next %s" % (SCRIPTS, a.run))


# ------------------------------------------------------------------ proofs
def fails_of(R, prefixes=None):
    out = [m for lvl, _, m in R.rows if lvl == "FAIL"]
    if prefixes:
        out = [m for m in out if any(m.startswith(x) or x in m for x in prefixes)]
    return out


def ck_locate(run, rj):
    acc = load_list(run, w.ACCESS)
    errs = []
    if not any(e.get("need") == "transcript" and e.get("result") == "ok" for e in acc):
        errs.append("no successful access entry for 'transcript' (run.py access ... --need transcript ... --result ok)")
    form = [e for e in acc if e.get("need") == "form"]
    if any(e["result"] == "ok" for e in form):
        pass
    else:
        failed = {e["route"] for e in form if e["result"] == "fail"}
        untried = [r_ for r_ in w.ROUTES if r_ not in failed]
        if untried:
            errs.append("the form's data file was not obtained and these routes were not tried and logged: %s (run.py access --need form ...). All three, in order, every time" % untried)
        else:
            q = next((q for q in load_list(run, w.QUESTIONS) if q.get("need") == "form"), None)
            if not q:
                errs.append("STOP: the form's data file is missing on all three routes. Ask Paul: run.py ask %s --need form --searched \"<where>\" (it prints the exact question), then wait for his answer" % run)
            elif len(str(q.get("paul_said") or "").strip()) < 3 or q.get("choice") not in ("manual", "transcript"):
                errs.append("STOP: Paul has not answered the question about the missing form file. Record his own words: run.py answer %s --need form --said \"...\" --choice manual|transcript" % run)
    return errs


def ck_form(run, rj):
    mode = rj.get("form_mode")
    if mode in ("manual", "transcript"):
        return []
    if mode != "form" or not os.path.exists(p(run, w.FORM)):
        return ["the form's data file has not been read by the program (run.py form %s <file>)" % run]
    R = verify.Results()
    lines = None
    verify.check_form(run, R, lines or [], {})
    return [m for m in fails_of(R) if "crosscheck" not in m and "never compared" not in m and "report" not in m and "Other fields" not in m and "printed" not in m and "look-up" not in m]


def ck_prep(run, rj):
    path = p(run, w.STATE)
    if not os.path.exists(path):
        return ["tx.py prep has not been run"]
    st = w.load_json(path)
    errs = [] if st["complete"] else ["the transcript is incomplete: %s" % "; ".join(st["notes"])]
    if os.path.exists(p(run, w.TRANSCRIPT)):
        td = verify.transcript_date(w.read_lines(run))
        want = w.parse_date(rj.get("date"))
        if td and want and td != want:
            errs.append("the transcript says the meeting started on %s but Paul's meeting date is %s: this is another meeting's transcript. STOP and tell Paul; find the right transcript" % (td.strftime("%d/%m/%Y"), rj["date"]))
    return errs


def ck_sources(run, rj):
    R = verify.Results()
    lines = w.read_lines(run) if os.path.exists(p(run, w.TRANSCRIPT)) else None
    verify.check_sources(run, R, lines, None)
    return fails_of(R)


def _state(run):
    return w.load_json(p(run, w.STATE), "state.json")


def load_ledger(run):
    path = p(run, w.LEDGER)
    return w.load_json(path) if os.path.exists(path) else {"entries": [], "scan_reviewed": []}


def unacked(run, pass_no):
    st = _state(run)
    led = load_ledger(run)
    return [c for c in range(1, len(st["chunks"]) + 1) if not tx.chunk_acked(st, led, pass_no, c)]


def ck_pass1(run, rj):
    errs = []
    if not tx.passes_done(_state(run))[0]:
        errs.append("Pass 1 has not served every chunk (see `tx.py status %s`)" % run)
    if not load_ledger(run).get("entries"):
        errs.append("the ledger is empty: record what the call adds (gaps, differences, contact details, quote requests, next steps) with run.py ledger add")
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


def ck_joint(run, rj):
    j = rj.get("joint") or {}
    if j.get("answer") not in ("yes", "no"):
        return ["the question is not answered: is this a joint meeting with a spouse? Look at who spoke on the call, then run.py joint %s --answer yes|no --evidence \"<what shows it>\"" % run]
    return []


def ck_lead(run, rj):
    ld = w.load_opt(p(run, w.LEAD), {})
    if not ld.get("searched"):
        return ["the lead source was not searched (run.py lead): the Outlook search for a D&R Marketing appointment email is always made"]
    return []


def ck_cross(run, rj):
    if rj.get("form_mode") != "form":
        return []
    R = verify.Results()
    lines = w.read_lines(run)
    verify.check_form(run, R, lines, {})
    return [m for m in fails_of(R) if m.startswith("crosscheck") or "never compared" in m or "does not list exactly" in m]


def ck_verify(stage):
    def check(run, rj):
        R, st, ledger, content = verify.run_checks(run, stage)
        if stage == "final":
            verify.report(R, st, ledger, content, stage, run)
        return [m for lvl, _, m in R.rows if lvl == "FAIL"][:15]
    return check


def ck_build(run, rj):
    st = _state(run)
    cp = p(run, w.CONTENT)
    if not st.get("build") or not os.path.exists(cp):
        return ["the PDF has not been built (build.py)"]
    if st["build"]["content_sha"] != w.content_hash(w.load_json(cp)):
        return ["content.json changed after the build: run build.py again"]
    return []


def rc_get(run, dotted):
    d = w.load_json(p(run, w.RECEIPT)) if os.path.exists(p(run, w.RECEIPT)) else {}
    for k in dotted.split("."):
        d = d.get(k) if isinstance(d, dict) else None
    return d


def ck_receipt(*keys, n=1):
    def check(run, rj):
        return ["receipt is missing '%s' (run.py receipt --set %s=...)" % (k, k) for k in keys if len(str(rc_get(run, k) or "").strip()) < n]
    return check


def ck_pdf_saved(run, rj):
    errs = ck_receipt("pdf_sent_in_chat", "saved.tool", "saved.folder", "saved.filename", "saved.tool_result", "saved.folder_listing_check", "saved.listed_size")(run, rj)
    if errs:
        return errs
    b = _state(run).get("build") or {}
    if str(rc_get(run, "saved.listed_size")).strip().replace(",", "") != str(b.get("pdf_size")):
        errs.append("the folder listing shows %s bytes but the local PDF is %s bytes: the save is not proven (a new time with the old size means the copy lagged). Commit it again, list again, record the new listing" % (rc_get(run, "saved.listed_size"), b.get("pdf_size")))
    if str(rc_get(run, "saved.filename")) != b.get("pdf"):
        errs.append("saved.filename is %r but the PDF is %r" % (rc_get(run, "saved.filename"), b.get("pdf")))
    fp_ = verify.save_folder_problem(rc_get(run, "saved.folder"), rj.get("client") or {}, str(rc_get(run, "saved.folder_spelling") or ""))
    if fp_:
        errs.append("saved.folder: " + fp_)
    return errs


def ck_judgment(run, rj):
    errs = ck_receipt("independent_check", n=10)(run, rj) + ck_receipt("png_visual_check", n=20)(run, rj)
    for k in verify.JUDGMENT_KEYS:
        errs += ck_receipt("judgment." + k, n=12)(run, rj)
    return errs


def ck_handoffs(run, rj):
    errs = ck_receipt("summary.invoked", "summary.abi_same", n=12)(run, rj) + ck_receipt("teams.run_folder", "teams.skill_dir", "teams.next_appointment_carried", n=3)(run, rj)
    if not errs:
        tm = (w.load_opt(p(run, w.RECEIPT), {}).get("teams") or {})
        msg = verify.check_teams_handoff(run, rj, w.load_opt(p(run, w.CONTENT), {}), tm)
        if msg:
            errs.append("Teams hand-over: " + msg)
    if rj.get("spouse"):
        errs += ck_receipt("spouse.cross_check", n=12)(run, rj)
    return errs


CHECKS = {
    "locate_ok": ck_locate, "form_done": ck_form, "prep_done": ck_prep, "sources_ok": ck_sources, "pass1_done": ck_pass1, "pass2_done": ck_pass2,
    "scan_done": ck_scan, "lead_done": ck_lead, "joint_done": ck_joint, "cross_done": ck_cross, "verify_pre": ck_verify("pre"), "build_fresh": ck_build, "receipt_check": ck_judgment,
    "receipt_pdf": ck_pdf_saved,
    "receipt_handoffs": ck_handoffs, "verify_final": ck_verify("final"),
}


def cmd_done(a):
    rj = load_run(a.run)
    if rj.get("program_fingerprint") and rj["program_fingerprint"] != w.program_fingerprint():
        w.die("REFUSED: the skill's programs, layout, steps or rule pages changed while this run was in progress. The programs are run as they are, never edited during a run. Start the run again.", 3)
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
    save_run(a.run, rj)
    print("STEP '%s' DONE.\n" % a.step)
    nxt = current_step(rj)
    if nxt is None:
        print("EVERY STEP IS DONE. The job is finished only when your reply contains the verify.py printout (it was shown above if the last step was `final`).")
        return
    show_step(a.run, rj, nxt)


# ------------------------------------------------------------------ logs
def cmd_access(a):
    log = load_list(a.run, w.ACCESS)
    log.append({"t": w.now(), "need": a.need, "route": a.route, "tool": a.tool, "result": a.result, "detail": a.detail or ""})
    w.save_json(p(a.run, w.ACCESS), log)
    es = [e for e in log if e["need"] == a.need]
    if any(e["result"] == "ok" for e in es):
        print("logged: '%s' obtained via %s." % (a.need, a.route))
        return
    failed = {e["route"] for e in es if e["result"] == "fail"}
    untried = [r_ for r_ in w.ROUTES if r_ not in failed]
    if untried:
        print("logged failure. NEXT ROUTE TO TRY for '%s': %s (%s). You may not give up before all three are logged." % (a.need, untried[0], w.ROUTE_NAMES[untried[0]]))
    elif a.need == "form":
        print("logged failure. All three routes have now failed for the form's data file. STOP and ASK Paul: run.py ask %s --need form --searched \"<where>\"" % a.run)
    else:
        print("logged failure. All three routes have now failed for '%s'. Record the question for Paul with: run.py ask" % a.need)


def cmd_source(a):
    srcs = load_list(a.run, w.SOURCES)
    if a.kind not in w.SOURCE_KINDS:
        w.die("kind must be one of %s" % w.SOURCE_KINDS)
    if a.none:
        if len(a.none.strip()) < 8:
            w.die("REFUSED: say what you searched and where (at least 8 characters).")
        tried = {e.get("route") for e in load_list(a.run, w.ACCESS) if e.get("need") == a.kind and e.get("result") == "fail"}
        if a.kind in w.REQUIRED_SOURCE_KINDS and len(tried & set(w.ROUTES)) < 2:
            w.die("REFUSED: you may say there is no %s on file only after searching on at least two routes (device, m365, zapier) and logging each: "
                  "run.py access %s --need %s --route device --tool <tool> --result fail --detail \"nothing found in <where>\"." % (a.kind, a.run, a.kind))
        srcs.append({"kind": a.kind, "none": a.none})
    else:
        if not (a.path and a.date and a.read == "yes"):
            w.die("REFUSED: a document needs --path, --date and --read yes (or use --none \"reason\").")
        low = a.path.lower().replace("/", "\\")
        if "company - wr clients" in low and "paul kafentzis (client files)" not in low:
            w.die("REFUSED: that path is in another broker's folder. Only 'Paul Kafentzis (Client Files)' is ever read or written.")
        if a.kind == "Manual Fact Find" and load_run(a.run).get("form_mode") != "manual":
            w.die("REFUSED: the Manual Fact Find is read only when the form's data file is missing and Paul chose it (run.py answer ... --choice manual).")
        ref = a.ref or re.sub(r"\.[A-Za-z0-9]{1,5}$", "", re.split(r"[\\/]", a.path.strip())[-1])
        if any(verify.source_ref(e) == ref for e in srcs if e.get("read") == "yes"):
            w.die("REFUSED: a document called %r is already recorded; give this one its own --ref." % ref)
        if a.kind in ("Overview", "Policy schedule"):
            if not a.text_file:
                w.die("REFUSED: a %s is accepted only with a text copy (--text-file, for a PDF: pdftotext \"<file>\" /tmp/<name>.txt): without it nothing in it can be checked." % a.kind)
            if not os.path.exists(a.text_file):
                w.die("REFUSED: text file not found: %s" % a.text_file)
            txt = open(a.text_file, encoding="utf-8", errors="replace").read()
            cl_ = load_run(a.run)["client"]
            fr_ = w.load_opt(p(a.run, w.FORM), {})
            idd = w.digits(((fr_.get("fields") or {}).get("idno") or {}).get("v", ""))
            if not ((w.last_name_token(cl_["surname"]) in w.norm(txt)) or (len(idd) >= 10 and idd in w.digits(txt))):
                w.die("REFUSED: the text of this %s does not mention the client (%s, or the ID number): it does not look like this client's document." % (a.kind, cl_["surname"]))
        entry = {"kind": a.kind, "path": a.path, "date": a.date, "read": "yes", "ref": ref}
        if a.text_file:
            if not os.path.exists(a.text_file):
                w.die("REFUSED: text file not found: %s" % a.text_file)
            os.makedirs(os.path.join(a.run, w.DOCS), exist_ok=True)
            shutil.copyfile(a.text_file, os.path.join(a.run, w.DOCS, ref + ".txt"))
            entry["text"] = True
        srcs.append(entry)
    w.save_json(p(a.run, w.SOURCES), srcs)
    print("recorded %s source (%d so far)%s." % (a.kind, len(srcs), "" if a.none or srcs[-1].get("text") else
          ". NOTE: no --text-file given, so quotes and figures from this document cannot be machine-checked (Paul will be told)"))


def cmd_ask(a):
    log = load_list(a.run, w.ACCESS)
    es = [e for e in log if e["need"] == a.need]
    rj = load_run(a.run)
    q = a.question
    if a.need == "form" and not q:
        q = FORM_QUESTION % ("%s %s" % (rj["client"]["first"], rj["client"]["surname"]))
    if not q:
        w.die("REFUSED: give the question (--question).")
    if a.kind == "file" and a.need != "date":
        if not es:
            w.die("REFUSED: no access attempts are logged for '%s'. Try the routes first (run.py access)." % a.need)
        if any(e["result"] == "ok" for e in es):
            w.die("REFUSED: '%s' was obtained, so there is nothing to ask Paul." % a.need)
        failed = {e["route"] for e in es if e["result"] == "fail"}
        untried = [r_ for r_ in w.ROUTES if r_ not in failed]
        if untried:
            w.die("REFUSED: these routes have not been tried for '%s': %s. Never ask Paul before all three failed." % (a.need, untried))
    if len(a.searched.strip()) < 8:
        w.die("REFUSED: say what you already searched (at least 8 characters).")
    qs = load_list(a.run, w.QUESTIONS)
    qs.append({"t": w.now(), "need": a.need, "question": q, "searched": a.searched, "kind": a.kind})
    w.save_json(p(a.run, w.QUESTIONS), qs)
    print("RECORDED. Now STOP and ask Paul, in plain words, exactly this, and wait for his answer:\n")
    print("  %s" % q)
    print("  (I already looked in: %s)" % a.searched)
    for e in es:
        print("  - tried %s via %s: %s %s" % (w.ROUTE_NAMES.get(e["route"], e["route"]), e["tool"], e["result"], e.get("detail", "")))
    print("\nWhen he has answered, record his own words: run.py answer %s --need %s --said \"...\"%s" % (a.run, a.need, " --choice manual|transcript" if a.need == "form" else ""))


def cmd_answer(a):
    qs = load_list(a.run, w.QUESTIONS)
    mine = [q for q in qs if q.get("need") == a.need]
    if not mine:
        w.die("REFUSED: no question about '%s' was recorded (run.py ask)." % a.need)
    if len(a.said.strip()) < 3:
        w.die("REFUSED: record Paul's own words (at least 3 characters).")
    if a.need == "form" and a.choice not in ("manual", "transcript"):
        w.die("REFUSED: for the missing form file Paul chooses: --choice manual (the filled-in Manual Fact Find PDF) or --choice transcript (the transcript alone).")
    mine[-1]["paul_said"] = a.said
    if a.choice:
        mine[-1]["choice"] = a.choice
    w.save_json(p(a.run, w.QUESTIONS), qs)
    if a.need == "form":
        rj = load_run(a.run)
        if any(e.get("result") == "ok" for e in load_list(a.run, w.ACCESS) if e.get("need") == "form"):
            w.die("REFUSED: the form's data file was obtained, so there is nothing to decide.")
        rj["form_mode"] = a.choice
        save_run(a.run, rj)
        w.save_json(p(a.run, w.CROSS), [])
        print("recorded Paul's words. The form is treated as missing: every value now comes from %s, with its source." % ("the filled-in Manual Fact Find PDF (record it with run.py source --kind \"Manual Fact Find\")" if a.choice == "manual" else "the transcript alone"))
    else:
        print("recorded Paul's words for '%s'." % a.need)


def cmd_form(a):
    acc = [e for e in load_list(a.run, w.ACCESS) if e.get("need") == "form" and e.get("result") == "ok"]
    if not acc:
        w.die("REFUSED: log how you got the form's data file first (run.py access --need form --route ... --result ok).")
    ffform.read_into_run(a.file, a.run, a.again)
    rj = load_run(a.run)
    rj["form_mode"] = "form"
    save_run(a.run, rj)
    print("\nNEXT: the form's saved PDF: run.py formpdf %s <the PDF>" % a.run)


def cmd_formpdf(a):
    rj = load_run(a.run)
    if rj.get("form_mode") != "form":
        w.die("REFUSED: read the form's data file first (run.py form).")
    acc = [e for e in load_list(a.run, w.ACCESS) if e.get("need") == "formpdf"]
    if a.none:
        failed = {e["route"] for e in acc if e["result"] == "fail"}
        if set(w.ROUTES) - failed:
            w.die("REFUSED: the saved PDF may be called missing only after all three routes were tried and logged (run.py access --need formpdf ... --result fail). Not yet tried: %s" % [r_ for r_ in w.ROUTES if r_ not in failed])
    elif not any(e["result"] == "ok" for e in acc):
        w.die("REFUSED: log how you got the form's saved PDF first (run.py access --need formpdf --route ... --result ok).")
    ffform.cmd_pdf(types.SimpleNamespace(run=a.run, file=a.file, none=a.none))


def cmd_pdfreview(a):
    ffform.cmd_pdfreview(types.SimpleNamespace(run=a.run, key=a.key, result=a.result, quote=a.quote, pdf_value=a.pdf_value))


# ------------------------------------------------------------------ several transcripts, ledger, lead, cross, claim
def cmd_join(a):
    if len(a.parts) < 2:
        w.die("REFUSED: join needs at least two transcript files (one meeting whose call dropped and reconnected).")
    out, info, n = [], [], len(a.parts)
    for k, path in enumerate(a.parts, 1):
        if not os.path.exists(path):
            w.die("Source not found: " + path)
        text = tx.read_source(path).replace("\r\n", "\n").replace("\r", "\n")
        lines = [ln.rstrip() for ln in text.split("\n")]
        while lines and not lines[-1]:
            lines.pop()
        out.append("===== TRANSCRIPT %d OF %d: %s =====" % (k, n, os.path.basename(path)))
        start = len(out) + 1
        out += lines
        info.append({"name": os.path.basename(path), "sha256": w.sha256_text("\n".join(lines)), "lines": [start, len(out)], "head": lines[:4], "tail": lines[-4:]})
    os.makedirs(a.run, exist_ok=True)
    jp = p(a.run, "transcript_joined.txt")
    with open(jp, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    w.save_json(p(a.run, w.PARTS), {"parts": info, "continuity": []})
    print("JOINED %d transcripts into %s (a separator line marks each part)." % (n, jp))
    for k in range(n - 1):
        print("\nCONTINUITY CHECK %d/%d: the end of transcript %d and the start of transcript %d must pick up the same topic or figure." % (k + 1, k + 2, k + 1, k + 2))
        print("  END OF %d:" % (k + 1))
        for ln in info[k]["tail"]:
            print("    | " + ln)
        print("  START OF %d:" % (k + 2))
        for ln in info[k + 1]["head"]:
            print("    | " + ln)
        print("  Record it: run.py continuity %s --between %d,%d --result ok|gap --detail \"<what picks up, or what is missing>\"" % (a.run, k + 1, k + 2))
    print("\nNEXT: python3 %s/tx.py prep %s %s   (it checks every part on its own)" % (SCRIPTS, jp, a.run))


def cmd_continuity(a):
    pj = w.load_opt(p(a.run, w.PARTS), None)
    if not pj:
        w.die("REFUSED: there is no joined transcript in this run (run.py join).")
    m = re.fullmatch(r"(\d+),(\d+)", a.between)
    if not m or int(m.group(2)) != int(m.group(1)) + 1 or int(m.group(2)) > len(pj["parts"]):
        w.die("REFUSED: --between must name two neighbouring transcripts, for example 1,2.")
    if len(a.detail.strip()) < 20:
        w.die("REFUSED: say in your own words what picks up (or what is missing): at least 20 characters.")
    pj["continuity"] = [c for c in pj["continuity"] if tuple(c["between"]) != (int(m.group(1)), int(m.group(2)))]
    pj["continuity"].append({"between": [int(m.group(1)), int(m.group(2))], "result": a.result, "detail": a.detail, "t": w.now()})
    w.save_json(p(a.run, w.PARTS), pj)
    print("continuity %s recorded: %s%s" % (a.between, a.result, "  (a real gap: Paul is told at the end)" if a.result == "gap" else ""))


def cmd_ledger(a):
    led = load_ledger(a.run)
    save = lambda: w.save_json(p(a.run, w.LEDGER), led)  # noqa: E731
    if a.action == "list":
        for e in led["entries"]:
            cov = ",".join(e.get("covered_by") or []) or ("EXCLUDED" if e.get("excluded") else "NOT COVERED")
            print("%-5s line %-5s %-13s %-14s %s" % (e["id"], e["line"], e["kind"], cov, e["quote"][:70]))
        print("%d entries, %d scan reviews" % (len(led["entries"]), len(led["scan_reviewed"])))
        return
    if a.action == "add":
        if not os.path.exists(p(a.run, w.TRANSCRIPT)):
            w.die("REFUSED: the transcript has not been prepared yet (tx.py prep).")
        lines = w.read_lines(a.run)
        if a.kind not in verify.LEDGER_KINDS:
            w.die("kind must be one of %s" % verify.LEDGER_KINDS)
        if not 1 <= a.line <= len(lines) or not verify.quote_ok(lines, a.line, a.quote):
            w.die("REFUSED: that quote is not found at transcript line %d. Copy the exact words from the chunk you read." % a.line)
        st = _state(a.run)
        in_pass2 = any(r_["pass"] == 2 for r_ in st["reads"])
        e = {"id": "L%d" % (len(led["entries"]) + 1), "line": a.line, "kind": a.kind, "quote": a.quote, "pass": 2 if in_pass2 else 1, "covered_by": []}
        if a.speaker:
            e["speaker"] = a.speaker
        if a.meaning:
            e["meaning"] = a.meaning
        led["entries"].append(e)
        save()
        print("%s added (%s, line %d, pass %d)%s" % (e["id"], a.kind, a.line, e["pass"], "  - must be covered by a fill, difference, note or answer" if a.kind in verify.KINDS_MUST_COVER else ""))
        return
    ent = {e["id"]: e for e in led["entries"]}
    if a.action == "cover":
        inp = compose.load_inputs(a.run)
        try:
            content = compose.compose(inp) if not compose.check_inputs(inp) else None
        except Exception:
            content = None
        targets = verify.cover_targets(a.run, inp["overlay"], inp["cross"], inp["lead"], content)
        if a.id not in ent:
            w.die("no ledger entry %s" % a.id)
        bad = [i for i in a.items if i not in targets]
        if bad:
            w.die("REFUSED: these items do not exist (overlay ids, answered cross-check keys, 'lead', 'claim:<key>', quote rows such as quote.fna): %s" % bad)
        e_ = ent[a.id]
        probs = [verify.cover_problem(e_["kind"], e_["line"], i, targets[i], e_["quote"]) for i in a.items]
        if all(probs) and e_["kind"] in verify.KINDS_MUST_COVER:
            w.die("REFUSED: %s" % "; ".join(probs))
        ent[a.id]["covered_by"] = sorted(set(ent[a.id].get("covered_by") or []) | set(a.items))
        save()
        print("%s covered by %s" % (a.id, ent[a.id]["covered_by"]))
    elif a.action == "exclude":
        if a.id not in ent:
            w.die("no ledger entry %s" % a.id)
        if ent[a.id]["kind"] not in verify.KINDS_OPTIONAL:
            w.die("REFUSED: a %s entry cannot be excluded: it must map to a fill, difference, note or answer." % ent[a.id]["kind"])
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
        span = 1 if a.line is not None else (a.to - a.frm + 1)
        if span < 1 or span > 40:
            w.die("REFUSED: one review may dismiss at most 40 lines (this one is %d). Dismiss each stretch of plain talk on its own, with its own reason." % span)
        if any(w.norm(r_.get("reason", "")) == w.norm(a.reason) for r_ in led["scan_reviewed"]):
            w.die("REFUSED: that reason was already used for another review. Say what is in THESE lines and why nothing needs recording.")
        rec = {"line": a.line, "reason": a.reason} if a.line is not None else {"from": a.frm, "to": a.to, "reason": a.reason}
        led["scan_reviewed"].append(rec)
        save()
        print("scan hit(s) %s reviewed: %s" % (a.line if a.line is not None else "%d-%d" % (a.frm, a.to), a.reason))
    elif a.action == "ack":
        st = _state(a.run)
        if a.pass_ not in (1, 2) or not 1 <= a.chunk <= len(st["chunks"]):
            w.die("REFUSED: --pass must be 1 or 2 and --chunk 1..%d." % len(st["chunks"]))
        if not any(r_["pass"] == a.pass_ and r_["chunk"] == a.chunk for r_ in st["reads"]):
            w.die("REFUSED: chunk %d of Pass %d has not been read yet." % (a.chunk, a.pass_))
        if len(a.reason.strip()) < 20:
            w.die("REFUSED: say in your own words what this chunk contained and why it holds nothing to record (at least 20 characters).")
        led.setdefault("chunk_acks", []).append({"pass": a.pass_, "chunk": a.chunk, "reason": a.reason, "t": w.now()})
        save()
        print("chunk %d of Pass %d acknowledged." % (a.chunk, a.pass_))


def cmd_lead(a):
    if "unavailable" in (a.folder_result, a.mailbox_result):
        acc_all = load_list(a.run, w.ACCESS)
        failed = {e["route"] for e in acc_all if e.get("need") == "lead" and e.get("result") == "fail"}
        if set(w.ROUTES) - failed:
            w.die("REFUSED: the Outlook search may be called unavailable only after all three routes were tried and logged as failed (run.py access --need lead ... --result fail). Not yet logged: %s" % [r_ for r_ in w.ROUTES if r_ not in failed])
        q = next((q for q in load_list(a.run, w.QUESTIONS) if q.get("need") == "lead" and len(str(q.get("paul_said") or "").strip()) >= 3), None)
        if not q:
            w.die("REFUSED: STOP and ask Paul first: run.py ask %s --need lead --kind knowledge --question \"The Outlook search for a D&R Marketing email for this client could not be made on any route. Carry on without it, or wait?\" --searched \"<the errors>\", then run.py answer ... with his words." % a.run)
        rec = {"searched": [{"where": "Outlook (Leads - D&R Marketing and the whole mailbox)", "result": "unavailable"}], "found": False, "unavailable": True, "paul_said": q["paul_said"], "t": w.now()}
        w.save_json(p(a.run, w.LEAD), rec)
        print("lead source recorded as NOT SEARCHED (Outlook unavailable on all three routes; Paul's words: %r). The Referral From value comes from the form or the call; Paul will see this on the glance list." % q["paul_said"])
        return
    acc = [e for e in load_list(a.run, w.ACCESS) if e.get("need") == "lead" and e.get("route") == "m365" and e.get("result") == "ok"]
    if not acc:
        w.die("REFUSED: log the Outlook search first: run.py access --need lead --route m365 --tool <the Outlook search tool> --result ok --detail \"<folder and query searched>\".")
    searched = [{"where": "Inbox > Business > Leads - D&R Marketing", "result": a.folder_result}]
    if a.folder_result == "none":
        if a.mailbox_result == "skipped":
            w.die("REFUSED: nothing was found in the Leads - D&R Marketing folder, so the whole mailbox must be searched too (the client's name + \"Appointment from D & R Marketing\").")
        searched.append({"where": "whole mailbox", "result": a.mailbox_result})
    found = "found" in (a.folder_result, a.mailbox_result)
    rec = {"searched": searched, "found": found, "t": w.now()}
    if found:
        if not (a.received and w.parse_date(a.received) and a.ref and a.quote):
            w.die("REFUSED: an email was found: give --received DD/MM/YYYY (the date it was received), --ref (the name you recorded it under with run.py source --kind Correspondence) and --quote (words from the email).")
        srcs = [e for e in load_list(a.run, w.SOURCES) if e.get("read") == "yes" and verify.source_ref(e) == a.ref and e.get("kind") == "Correspondence"]
        if not srcs:
            w.die("REFUSED: record the email first: run.py source --kind Correspondence --path <where> --date <date> --read yes --ref %s --text-file <its text>." % a.ref)
        txt = verify.doc_text(a.run, a.ref)
        if txt is not None and w.norm(a.quote) not in w.norm(txt):
            w.die("REFUSED: that quote is not in the email's text copy.")
        rec.update(received=a.received, ref=a.ref, quote=a.quote)
    w.save_json(p(a.run, w.LEAD), rec)
    print("lead source recorded: %s." % (("D&R Marketing lead - %s" % a.received) if found else "no D&R Marketing email found (the Referral From value comes from the form or the call)"))


def search_for_item(run, lines, fr, lay, item):
    """The call lines that mention this populated field (its curated terms, or the words of its row), and whether the terms were curated."""
    rv = verify.row_values(fr, item["key"]) if item.get("row") else None
    terms, curated = verify.field_terms(lay, item["key"], item.get("label", item["key"]), rv)
    hits, _ = verify.search_terms(run, lines, terms)
    return terms, curated, hits


def cmd_cross(a):
    path = p(a.run, w.CROSS)
    items = w.load_json(path, "crosscheck.json (run `run.py form` first)")
    if not items:
        w.die("REFUSED: there is nothing to compare (no form data file in this run).")
    by = {i["key"]: i for i in items}
    lines = w.read_lines(a.run)
    lay = w.layout()
    answers = {}
    if a.file:
        answers = w.load_json(a.file, "the answers file")
    elif a.key:
        answers = {a.key: {"r": a.r, "line": a.line, "quote": a.quote, "value": a.value, "reviewed": a.reviewed}}
    fr = w.load_opt(p(a.run, w.FORM), {})
    for k, ans in answers.items():
        if k not in by:
            parts = k.split(".")
            row = ".".join(parts[:2])
            cellv = verify.form_value(fr, k) if len(parts) == 3 else None
            if cellv is not None and row in by:                  # one cell of a list row: the place to record a difference
                by[k] = {"key": k, "label": "%s: %s" % (by[row]["label"], parts[2]), "value": cellv, "status": by[row]["status"], "section": by[row]["section"], "answer": None, "cell": True}
                items.append(by[k])
            else:
                w.die("REFUSED: %s is not one of the form's populated fields (see crosscheck.json)." % k)
        r_ = ans.get("r")
        if r_ not in ("same", "differs", "not_on_call"):
            w.die("REFUSED: %s: r must be same, differs or not_on_call." % k)
        if by[k].get("row") and r_ == "differs":
            w.die("REFUSED: %s is a whole row: name the column (for example debts.0.bal) for a difference." % k)
        if r_ in ("same", "differs"):
            ln = ans.get("line")
            if not isinstance(ln, int) or not 1 <= ln <= len(lines) or not verify.quote_ok(lines, ln, str(ans.get("quote") or ""), verify.ITEM_QUOTE_MIN):
                w.die("REFUSED: %s: the quote is not found at transcript line %s. Copy the exact words (at least %d characters)." % (k, ln, verify.ITEM_QUOTE_MIN))
        if r_ == "differs":
            if not str(ans.get("value") or "").strip() or w.norm(str(ans["value"])) == w.norm(by[k]["value"]):
                w.die("REFUSED: %s: 'differs' needs the call's own value, and it must differ from the form's (%r)." % (k, by[k]["value"]))
        rec = {kk: vv for kk, vv in ans.items() if vv is not None and kk in ("r", "line", "quote", "value", "reviewed")}
        if r_ == "not_on_call":
            terms, curated, hits = search_for_item(a.run, lines, fr, lay, by[k])
            why = str(ans.get("reviewed") or "").strip()
            if hits and len(why) < 15:
                w.die("REFUSED: %s is 'not on the call' but the call mentions it (searched %s: lines %s). Read them and answer same or differs with the exact words, or give --reviewed saying why those lines are not about this field (at least 15 characters)." % (k, terms[:4], hits[:8]))
            if not curated and len(why) < 15:
                w.die("REFUSED: %s: only its label words could be searched (a WEAK search). Give --reviewed saying what you checked for this field (at least 15 characters)." % k)
            rec.update(searched=terms[:8], hits=len(hits), weak=not curated)
        by[k]["answer"] = rec
    if a.rest:
        left_hits = []
        n_auto = 0
        for i in [i for i in items if not i.get("answer")]:
            terms, curated, hits = search_for_item(a.run, lines, fr, lay, i)
            if hits or not curated:
                left_hits.append((i["key"], hits[:6], curated))
            else:
                i["answer"] = {"r": a.rest, "searched": terms[:8], "hits": 0, "weak": False}
                n_auto += 1
        print("%d field(s) were searched for in the call (their own search terms) and found nowhere: recorded as 'not on the call'." % n_auto)
        if left_hits:
            print("%d field(s) are LEFT for you because the call mentions them (or only their label words could be searched):" % len(left_hits))
            for k_, h_, c_ in left_hits[:60]:
                print("  - %s: %s" % (k_, ("call lines %s" % h_) if h_ else "weak search (label words only)"))
            print("Answer each: same / differs with the exact words, or not_on_call with --reviewed \"<why those lines are not about this field>\".")
    w.save_json(path, items)
    todo = [i for i in items if not i.get("answer")]
    print("recorded %d answer(s). %d of %d populated fields still need an answer%s" % (len(answers), len(todo), len(items), (": " + ", ".join(i["key"] for i in todo[:15])) if todo else "."))


def default_terms(lay, key, label):
    return verify.field_terms(lay, key, label)


def cmd_claim(a):
    path = p(a.run, w.CLAIMS)
    claims = w.load_opt(path, {})
    inp = compose.load_inputs(a.run)
    lines = w.read_lines(a.run)
    lay = inp["layout"]
    content = compose.compose(inp)
    rows = {r["id"]: r for _, _, r in verify.iter_rows(content)}
    lead = w.load_opt(p(a.run, w.LEAD), {})
    fr = inp["form"]

    def record(key, word, terms, hits, docs, reviewed="", searched="", weak=False):
        claims[key] = {"as": word, "terms": terms, "hits": hits, "docs": docs, "reviewed": reviewed, "searched": searched, "weak": weak, "t": w.now()}

    if a.all_empty:
        pending = [u for u in content["unsettled"] if not u.startswith("quote.")]
        auto, need = [], []
        for key in pending:
            label = rows[key]["label"] if key in rows else key
            if key in verify.CONTACT_KEYS and not lead.get("searched"):
                need.append((key, label, "run.py lead first: contact details are called 'Not discussed' only after the lead-source search"))
                continue
            if key.startswith("debts.") and key.count(".") == 2:
                need.append((key, label, "a debt detail: find it in the form, the call, the Overview, other documents or Outlook; if truly missing: run.py claim --key %s --as Requested --searched \"<what was searched, the Outlook search included>\"" % key))
                continue
            terms, curated = verify.field_terms(lay, key, label)
            hits, docs = verify.search_terms(a.run, lines, terms)
            sib = verify.sibling_hits(lay, fr, key)
            if not curated:
                need.append((key, label, "WEAK search (only its label words): write a reason for this field: run.py claim --key %s --as \"Not discussed\" --reviewed \"...\"" % key))
            elif hits or docs or sib:
                need.append((key, label, "the search finds %s%s%s: read them" % (("call lines %s" % hits[:6]) if hits else "", (" documents " + str(docs)) if docs else "", ("; the form itself says " + "; ".join(sib[:3])) if sib else "")))
            else:
                record(key, "Not discussed", terms, [], [])
                auto.append(key)
        w.save_json(path, claims)
        print("CLAIMS: %d field(s) recorded as 'Not discussed' because the search of the call and the documents (with the field's own search terms) found nothing: %s" % (len(auto), ", ".join(auto[:30])))
        if need:
            print("\n%d field(s) need your attention:" % len(need))
            for key, label, why in need:
                print("  - %s (%s): %s" % (key, label, why))
            print("\nFill each from what the call or a document says (overlay `fills`, with its source), or, when the lines found do not answer it: "
                  "run.py claim %s --key K --as \"Not discussed\" --reviewed \"<why those lines do not answer it>\"." % a.run)
        return
    if not (a.key and a.as_):
        w.die("REFUSED: give --all-empty, or --key and --as.")
    if a.key not in content["unsettled"] and a.key not in claims:
        w.die("REFUSED: %s is not an empty, unsettled field of this document." % a.key)
    label = rows[a.key]["label"] if a.key in rows else a.key
    base, curated = verify.field_terms(lay, a.key, label)
    terms = list(dict.fromkeys(base + ([t.strip() for t in a.terms.split(",") if t.strip()] if a.terms else [])))
    hits, docs = verify.search_terms(a.run, lines, terms)
    sib = verify.sibling_hits(lay, fr, a.key)
    why = (a.reviewed or "").strip()
    if a.as_ == "Not discussed" and (hits or docs or sib) and len(why) < 15:
        w.die("REFUSED: the search finds %s%s%s. 'Not discussed' is a claim: read them, then give --reviewed saying why they do not answer it (at least 15 characters), or fill the field." % (("call lines %s" % hits[:8]) if hits else "", (" documents " + str(docs)) if docs else "", ("; the form itself says " + "; ".join(sib[:3])) if sib else ""))
    if a.as_ == "Not discussed" and not curated and len(why) < 15:
        w.die("REFUSED: only this field's label words could be searched (a WEAK search): give --reviewed saying what you checked (at least 15 characters).")
    if a.as_ == "Requested" and (not a.key.startswith("debts.") or not lead.get("searched") or len(a.searched or "") < 20):
        w.die("REFUSED: 'Requested' is for a debt detail only, and only after the form, the call, the Overview, other documents AND Outlook were checked: a recorded Outlook search (run.py lead) and what was searched (--searched, at least 20 characters) are needed.")
    if a.as_ == "N/A" and len(why) < 15:
        w.die("REFUSED: 'N/A' needs the reason (--reviewed, at least 15 characters).")
    if a.key in verify.CONTACT_KEYS and not lead.get("searched"):
        w.die("REFUSED: contact details are called 'Not discussed' only after the lead-source search (run.py lead).")
    record(a.key, a.as_, terms, hits, docs, why, a.searched or "", weak=not curated)
    w.save_json(path, claims)
    print("claim recorded: %s = %s%s (the checker searches again before it accepts it)" % (a.key, a.as_, "  [weak search]" if not curated else ""))


def cmd_joint(a):
    rj = load_run(a.run)
    if len(a.evidence.strip()) < 15:
        w.die("REFUSED: say what shows it (for example 'only Pat spoke, no spouse on the call' or 'Pat and Robin were both on the call'): at least 15 characters.")
    if a.answer == "yes" and not rj.get("spouse"):
        w.die("REFUSED: a joint meeting with a spouse needs one run per spouse. Start this job again with --spouse \"Other Surname\" --spouse-run <their run folder> (and a second run for the other spouse).")
    if a.answer == "no" and rj.get("spouse"):
        w.die("REFUSED: this run was started with --spouse, so it is for one spouse of a joint meeting. Answer yes, or start a new run without --spouse.")
    rj["joint"] = {"answer": a.answer, "evidence": a.evidence, "t": w.now()}
    save_run(a.run, rj)
    print("recorded: joint meeting with a spouse = %s (%s)%s" % (a.answer, a.evidence, ". Page 03 of the rules (two spouses) applies to every step from here." if a.answer == "yes" else "."))


def cmd_compose(a):
    inp = compose.load_inputs(a.run)
    errs = compose.check_inputs(inp)
    if errs:
        print("COMPOSE REFUSED. overlay.json has the wrong shape:")
        for e in errs:
            print("  - " + e)
        sys.exit(1)
    content = compose.compose(inp)
    w.save_json(p(a.run, w.CONTENT), json.loads(json.dumps(content, ensure_ascii=False)))
    n = sum(len(b["rows"]) for s in content["sections"] for b in s["blocks"])
    print("COMPOSED content.json: %d sections, %d rows, %d flags, %d unsettled" % (len(content["sections"]), n, sum(len(r["flags"]) for s in content["sections"] for b in s["blocks"] for r in b["rows"]), len(content["unsettled"])))
    if content["unsettled"]:
        print("  UNSETTLED (empty, and not N/A, not filled, not claimed): " + ", ".join(content["unsettled"][:40]))
        print("  Settle them: run.py claim --all-empty (it searches the call and the documents), or add a fill to overlay.json with its source.")
    for g in content["glance"]:
        print("  glance: " + g)


def cmd_spouse(a):
    rj = load_run(a.run)
    sp = rj.get("spouse") or {}
    if not sp.get("run"):
        w.die("REFUSED: this run was not started with --spouse and --spouse-run.")
    mine = w.load_opt(p(a.run, w.CONTENT), None)
    other = w.load_opt(p(sp["run"], w.CONTENT), None)
    if not mine or not other:
        w.die("REFUSED: both spouses' content.json must exist (run.py compose in each run) before the cross-check.")
    over = verify.spouse_overlap(mine, other)
    back = verify.spouse_overlap(other, mine)
    res = "searched this document for the other spouse's ID, phone numbers, emails and policy numbers: %s; searched theirs for this spouse's: %s" % (("FOUND %s" % over) if over else "none found", ("FOUND %s" % back) if back else "none found")
    print("SPOUSE CROSS-CHECK: " + res)
    print("Only the common debts, the children and the joint policies may appear in both. Record the one-line result: run.py receipt %s --set spouse.cross_check=\"%s\"" % (a.run, res))
    if over or back:
        sys.exit(1)


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
    sp.add_argument("--client", required=True, help='the client exactly as in Paul\'s message, "First Surname"')
    sp.add_argument("--first", help="the first name(s), when there is more than one")
    sp.add_argument("--surname", help="the surname, when it is more than one word")
    sp.add_argument("--date", required=True, help="the meeting date from Paul's message, DD/MM/YYYY")
    sp.add_argument("--spouse", help="two spouses in one meeting: the OTHER spouse, First Surname")
    sp.add_argument("--spouse-run", dest="spouse_run", help="the other spouse's run folder")
    add("next", cmd_next, "run")
    add("done", cmd_done, "run", "step")
    add("status", cmd_status, "run")
    sp = sub.add_parser("preflight")
    sp.set_defaults(fn=lambda a: (lambda r: (print_preflight(r[1]), sys.exit(0 if r[0] else 4)))(preflight()))

    sp = add("access", cmd_access, "run")
    sp.add_argument("--need", required=True)
    sp.add_argument("--route", required=True, choices=list(verify.ALLOWED_ROUTES))
    sp.add_argument("--tool", required=True)
    sp.add_argument("--result", required=True, choices=["ok", "fail"])
    sp.add_argument("--detail")
    sp = add("source", cmd_source, "run")
    sp.add_argument("--kind", required=True)
    sp.add_argument("--path")
    sp.add_argument("--date")
    sp.add_argument("--read", choices=["yes"])
    sp.add_argument("--none")
    sp.add_argument("--ref")
    sp.add_argument("--text-file", dest="text_file")
    sp = add("ask", cmd_ask, "run")
    sp.add_argument("--need", required=True)
    sp.add_argument("--question")
    sp.add_argument("--searched", required=True)
    sp.add_argument("--kind", choices=["file", "knowledge"], default="file")
    sp = add("answer", cmd_answer, "run")
    sp.add_argument("--need", required=True)
    sp.add_argument("--said", required=True)
    sp.add_argument("--choice", choices=["manual", "transcript"])
    sp = add("form", cmd_form, "run", "file")
    sp.add_argument("--again", action="store_true")
    sp = add("formpdf", cmd_formpdf, "run")
    sp.add_argument("file", nargs="?")
    sp.add_argument("--none")
    sp = add("pdfreview", cmd_pdfreview, "run")
    sp.add_argument("--key", required=True)
    sp.add_argument("--result", required=True, choices=["format_only", "disagree"])
    sp.add_argument("--quote", required=True)
    sp.add_argument("--pdf-value", dest="pdf_value")
    sp = add("join", cmd_join, "run")
    sp.add_argument("parts", nargs="+")
    sp = add("continuity", cmd_continuity, "run")
    sp.add_argument("--between", required=True)
    sp.add_argument("--result", required=True, choices=["ok", "gap"])
    sp.add_argument("--detail", required=True)
    sp = add("lead", cmd_lead, "run")
    sp.add_argument("--folder-result", dest="folder_result", required=True, choices=["found", "none", "unavailable"])
    sp.add_argument("--mailbox-result", dest="mailbox_result", required=True, choices=["found", "none", "skipped", "unavailable"])
    sp.add_argument("--received")
    sp.add_argument("--ref")
    sp.add_argument("--quote")
    sp = add("cross", cmd_cross, "run")
    sp.add_argument("--file")
    sp.add_argument("--key")
    sp.add_argument("--r", choices=["same", "differs", "not_on_call"])
    sp.add_argument("--line", type=int)
    sp.add_argument("--quote")
    sp.add_argument("--value")
    sp.add_argument("--rest", choices=["not_on_call"])
    sp.add_argument("--reviewed")
    sp = add("claim", cmd_claim, "run")
    sp.add_argument("--all-empty", dest="all_empty", action="store_true")
    sp.add_argument("--key")
    sp.add_argument("--as", dest="as_", choices=["Not discussed", "Requested", "N/A"])
    sp.add_argument("--reviewed")
    sp.add_argument("--searched")
    sp.add_argument("--terms")
    add("compose", cmd_compose, "run")
    sp = add("joint", cmd_joint, "run")
    sp.add_argument("--answer", required=True, choices=["yes", "no"])
    sp.add_argument("--evidence", required=True)
    add("spouse", cmd_spouse, "run")
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
