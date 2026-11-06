#!/usr/bin/env python3
"""Step driver for the ff-population-transcript skill.

  run.py start   <run_dir> --client "First Surname" --date DD/MM/YYYY [--other-run <the other spouse's run folder>]
  run.py next    <run_dir>            show the current step again
  run.py done    <run_dir> <step>     check the proof; only then show the next step
  run.py status  <run_dir>            where the job is up to (also the recovery point after a long chat)
  run.py preflight                    the self-test on its own

  run.py files   <run_dir> --form F [--formpdf P] --transcript T [--transcript T2] [--overview O] [--missing WHAT] [--force-incomplete WORDS]
  run.py form    <run_dir>            read both form files and print what to act on
  tx.py chunk    <run_dir> <1|2> <n>  hand the transcript over, in order, twice
  run.py lead    <run_dir> (--found --received DD/MM/YYYY --ref R --quote Q | --none WHAT | --unavailable WHAT)
  run.py combine <run_dir>            check overlay.json and make content.json (the ONE combined report)
  run.py build   <run_dir>            draw the Fact Find Transcript PDF and the page images
  run.py look    <run_dir> --saw "what you saw on the pages"
  run.py saved   <run_dir> --folder PATH --listed-size BYTES
  run.py report  <run_dir>            the short source report for Paul
  run.py ok      <run_dir> --paul-said "his words"
  run.py chain   <run_dir> --summary S --planner P --sitamah M

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

import build
import compose
import ffform
import tx
import verify
import wrlib as w

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPTS)
RULE = "-" * 78
STEP_IDS = verify.STEP_ORDER


# ------------------------------------------------------------------ helpers
def steps_file():
    return w.load_json(os.path.join(SKILL_DIR, "steps.json"), "steps.json")["steps"]


def p(run, name):
    return os.path.join(run, name)


def load_run(run):
    return w.load_json(p(run, w.RUN), "run.json (run `run.py start` first)")


def save_run(run, rj):
    w.save_json(p(run, w.RUN), rj)


def read_ref(name):
    path = os.path.join(SKILL_DIR, "references", name)
    if not os.path.exists(path):
        return "(MISSING reference page %s: the skill package is broken; tell Paul)" % name
    return open(path, encoding="utf-8").read().rstrip()


def chunk_commands(run):
    st = w.load_opt(p(run, w.STATE), None)
    if not st:
        return "(the chunk commands appear once step 1 has prepared the transcript)"
    k = len(st["chunks"])
    return ("Pass 1 then Pass 2: python3 %s/tx.py chunk %s 1 1   (%d chunks in all; each chunk prints the command for the next one; Pass 2 starts after Pass 1 is complete)" % (SCRIPTS, run, k))


def expand(text, run):
    return text.replace("{run}", run).replace("{scripts}", SCRIPTS).replace("{skill_dir}", SKILL_DIR).replace("{chunk_commands}", chunk_commands(run))


def current_step(rj):
    for s in steps_file():
        if rj["steps"].get(s["id"], {}).get("state") != "done":
            return s
    return None


def show_step(run, rj, step):
    plist = steps_file()
    n = [s["id"] for s in plist].index(step["id"]) + 1
    print(RULE)
    print("STEP %d of %d: %s        [%s]" % (n, len(plist), step["title"], step["id"]))
    print(RULE)
    for line in step["do"]:
        print(expand(line, run))
    for r in step.get("ref") or []:
        print("\nRULES FOR THIS STEP (references/%s):\n" % r)
        print(expand(read_ref(r), run))
    print("\nPROOF NEEDED: %s" % step["proof"])
    print("WHEN DONE RUN: python3 %s/run.py done %s %s" % (SCRIPTS, run, step["id"]))
    later = [s["title"] for s in plist[n:]]
    if later:
        print("COMING LATER (titles only): " + " | ".join(later))
    print(RULE)


def reopen(run, rj, from_steps):
    """A correction re-opens everything after it (Paul's rule): the steps and what was recorded for them."""
    gone = [s for s in from_steps if (rj["steps"].get(s) or {}).get("state") == "done"]
    for s in from_steps:
        rj["steps"].pop(s, None)
    return gone


# ------------------------------------------------------------------ preflight
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
    for tool, why, fatal in (("pdftotext", "reads the form's PDF", True), ("pdftoppm", "renders the page images", True), ("pandoc", "reads a .docx transcript", False)):
        add(shutil.which(tool) is not None, "%s (%s)" % (tool, why), fatal)
    add(w.stamp_display(w.skill_stamp()) is not None, "skill has a Last updated stamp (%s)" % w.version_short(), fatal=False)
    missing = [r for s in steps_file() for r in (s.get("ref") or []) if not os.path.exists(os.path.join(SKILL_DIR, "references", r))]
    add(not missing and os.path.exists(os.path.join(SCRIPTS, "layout.json")), "skill package complete (steps, reference pages, layout)" if not missing else "missing: %s" % sorted(set(missing)))
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


# ------------------------------------------------------------------ start, next, done, status
def cmd_start(a):
    ok, rows = preflight(a.run)
    print_preflight(rows)
    if not ok:
        print("\nSTOP. Tell Paul which items failed above in one line. Do not carry on and do not replace the PDF with a text draft.")
        sys.exit(4)
    if os.path.exists(p(a.run, w.RUN)):
        print("\nThis run already exists. Showing where it is up to.")
        return cmd_next(a)
    parts = a.client.split()
    if len(parts) < 2:
        w.die('--client must be the first name and surname, for example --client "Sam Testcase"')
    try:
        dt.datetime.strptime(a.date, "%d/%m/%Y")
    except ValueError:
        w.die("--date must be a real date as DD/MM/YYYY (the meeting date from Paul's message), got %r" % a.date)
    rj = {"skill": "ff-population-transcript", "created": w.now(), "skill_stamp": w.skill_stamp(), "program_fp": w.program_fingerprint(), "steps": {},
          "client": {"first": parts[0], "surname": " ".join(parts[1:])}, "date": a.date}
    if a.other_run:
        rj["spouse"] = {"run": os.path.abspath(a.other_run)}
    save_run(a.run, rj)
    print("\nSAY THIS TO PAUL FIRST, before anything else in your reply, in exactly these words:\n    %s.\n"
          "(It comes from the skill's own Last updated stamp. The final audit repeats it.)" % w.version_line())
    print("\nRUN STARTED  client: %s %s   meeting date: %s   version: %s" % (rj["client"]["first"], rj["client"]["surname"], a.date, w.stamp_display(rj["skill_stamp"]) or "unstamped"))
    print("Standing rules for the whole job:\n")
    print(expand(read_ref("00-rules.md"), a.run))
    print()
    show_step(a.run, rj, current_step(rj))


def cmd_next(a):
    rj = load_run(a.run)
    s = current_step(rj)
    if s is None:
        print("Every step is done. The short audit was printed when the last step was done; run `python3 %s/verify.py %s` to see it again." % (SCRIPTS, a.run))
        return
    show_step(a.run, rj, s)


def cmd_status(a):
    rj = load_run(a.run)
    cur = current_step(rj)
    print("RUN %s   client: %s %s   version: %s" % (a.run, rj["client"]["first"], rj["client"]["surname"], w.stamp_display(rj.get("skill_stamp")) or "unstamped"))
    for s in steps_file():
        state = rj["steps"].get(s["id"], {}).get("state")
        mark = "DONE   " if state == "done" else ("NEXT ->" if cur and s["id"] == cur["id"] else "waiting")
        print("  [%s] %-8s %s" % (mark, s["id"], s["title"]))
    if cur:
        print("\nNEXT: python3 %s/run.py next %s" % (SCRIPTS, a.run))


def current_content(run, rj):
    """content.json, if it is made from the current inputs."""
    c = w.load_opt(p(run, w.CONTENT), None)
    if c is None or (rj.get("combine") or {}).get("inputs_sha") != verify.inputs_sha(run):
        return None
    return c


# ------------------------------------------------------------------ the proofs (cheap, local: was the step done?)
def ck_find(run, rj):
    errs = []
    if not rj.get("files"):
        errs.append("no files registered (run.py files ...)")
    if not os.path.exists(p(run, w.FORM)):
        errs.append("the form's data file was not read")
    st = w.load_opt(p(run, w.STATE), None)
    if not st or not st.get("complete"):
        errs.append("the transcript is not prepared or not complete")
    return errs


def ck_form(run, rj):
    return [] if rj.get("form_report_shown") else ["run.py form has not been run (it reads both form files and prints your list)"]


def ck_read(run, rj):
    st = w.load_opt(p(run, w.STATE), None)
    if not st:
        return ["the transcript is not prepared"]
    d1, d2 = tx.passes_done(st)
    errs = []
    if not d1:
        errs.append("Pass 1 has not served every chunk (python3 %s/tx.py status %s)" % (SCRIPTS, run))
    if not d2:
        errs.append("Pass 2 has not served every chunk")
    return errs


def ck_lead(run, rj):
    return [] if os.path.exists(p(run, w.LEAD)) else ["the lead source was not recorded (run.py lead ...)"]


def ck_combine(run, rj):
    c = current_content(run, rj)
    if c is None:
        return ["content.json is missing or out of date: run `run.py combine %s` again until it prints COMBINED" % run]
    errs = []
    if c.get("unsettled"):
        errs.append("quote request(s) without a known insurer or basis: %s: ask Paul in one message, then add them to overlay.json `quotes`" % ", ".join(c["unsettled"][:6]))
    return errs


def ck_build(run, rj):
    c = current_content(run, rj)
    b = rj.get("build")
    errs = []
    if not b or c is None or b.get("content_sha") != w.content_hash(c):
        errs.append("the PDF is not built from the current report (run.py build)")
    elif (rj.get("look") or {}).get("build_sha") != b.get("pdf_sha"):
        errs.append("the page images of this build were not looked at (run.py look --saw ...)")
    return errs


def ck_save(run, rj):
    b, sv, ok = rj.get("build") or {}, rj.get("saved") or {}, rj.get("ok") or {}
    errs = []
    if sv.get("build_sha") != b.get("pdf_sha") or sv.get("size") != b.get("pdf_size"):
        errs.append("the saved file is not recorded with a matching listed size (run.py saved ...)")
    if ok.get("build_sha") != b.get("pdf_sha"):
        errs.append("Paul's OK of this version is not recorded (run.py ok ...)")
    return errs


def ck_chain(run, rj):
    ch = rj.get("chain") or {}
    errs = ["run.py chain: --%s is missing" % k for k in ("summary", "planner", "sitamah") if not str(ch.get(k) or "").strip()]
    if errs:
        return errs
    ok = verify.report_short(run, finishing=True)
    return [] if ok else ["the audit above has a red cross: fix it first"]


CHECKS = {"find": ck_find, "form": ck_form, "read": ck_read, "lead": ck_lead, "combine": ck_combine, "build": ck_build, "save": ck_save, "chain": ck_chain}


def cmd_done(a):
    rj = load_run(a.run)
    ids = [s["id"] for s in steps_file()]
    if a.step not in ids:
        w.die("'%s' is not a step. Steps: %s" % (a.step, ", ".join(ids)))
    cur = current_step(rj)
    if cur is None or ids.index(a.step) > ids.index(cur["id"]):
        w.die("REFUSED: finish step '%s' first. Steps are done in order, none skipped." % (cur["id"] if cur else "?"), 3)
    fails = CHECKS[a.step](a.run, rj)
    if fails:
        print("NOT DONE: step '%s' is missing its proof:" % a.step)
        for f in fails:
            print("  - " + f)
        print("\nFix this, then run `done %s` again." % a.step)
        sys.exit(1)
    rj = load_run(a.run)
    rj["steps"][a.step] = {"state": "done", "t": w.now()}
    save_run(a.run, rj)
    print("STEP '%s' DONE.\n" % a.step)
    nxt = current_step(rj)
    if nxt is None:
        print("EVERY STEP IS DONE. The job is finished only when your reply contains the audit printed above.")
        return
    show_step(a.run, rj, nxt)


# ------------------------------------------------------------------ step 1: files
def cmd_files(a):
    rj = load_run(a.run)
    for path in [a.form, a.formpdf, a.overview] + list(a.transcript or []):
        if path and not os.path.isfile(path):
            w.die("MISSING: %s" % path)
    if not a.form or not a.transcript:
        w.die("give --form <the form's data file> and --transcript <the transcript file> (a missing optional file is told with --missing \"<where you looked>\")")
    try:
        form = ffform.read_form_into_run(a.form, a.run)
    except ffform.FormError as e:
        print(str(e))
        sys.exit(4)
    rec = {"file": form["file"], "used": False, "why": "not given"}
    if a.formpdf:
        bad = ffform.pdf_file_problems(a.formpdf)
        text = None if bad else ffform.pdf_text(a.formpdf)
        if bad:
            rec["why"] = "not a whole PDF: " + "; ".join(bad)
        elif not text or not text.strip():
            rec["why"] = "no text could be read from it"
        else:
            ident = ffform.pdf_identity_problems(form, text)
            rep = ffform.pdf_report(form, text)
            if ident or (rep["checked"] and len(rep["not_found"]) > 0.25 * rep["checked"]):
                rec["why"] = "it does not look like the PDF of this data file (%s)" % ("; ".join(ident) or "%d of %d values are not in it" % (len(rep["not_found"]), rep["checked"]))
            else:
                with open(p(a.run, "form_pdf.txt"), "w", encoding="utf-8") as f:
                    f.write(text)
                rep.update(used=True, file=os.path.basename(a.formpdf), pages=text.count("\f") or 1, why="")
                rec = rep
    w.save_json(p(a.run, w.FORMPDF), rec)
    rj["files"] = {"form": os.path.basename(a.form), "formpdf": os.path.basename(a.formpdf) if a.formpdf else None, "transcripts": [os.path.basename(t) for t in a.transcript],
                   "overview": os.path.basename(a.overview) if a.overview else None, "missing": a.missing or ""}
    save_run(a.run, rj)
    print("FORM: %s (schema %s, saved %s), %d populated fields." % (form["file"], form["schema"], form["modified"], sum(1 for c in form["fields"].values() if c["populated"])))
    print("FORM PDF: %s" % (("read whole (%d page(s))" % rec.get("pages", 0)) if rec.get("used") else "NOT USED: %s. The data file alone is the source; Paul is told in the audit." % rec["why"]))
    if not a.overview:
        print("OVERVIEW: none registered%s." % ((" (" + a.missing + ")") if a.missing else ""))
    try:
        tx.cmd_prep(a.run, list(a.transcript), bool(a.force_incomplete))
    except SystemExit as e:
        if e.code:
            sys.exit(e.code)


# ------------------------------------------------------------------ step 2: form
def cmd_form(a):
    rj = load_run(a.run)
    form = w.load_json(p(a.run, w.FORM), "form_read.json (step 1: run.py files ...)")
    pdf = w.load_opt(p(a.run, w.FORMPDF), {})
    lay = w.layout()
    labels = {r["key"]: r["label"] for s in lay["sections"] for g in s["groups"] for r in g.get("rows", []) if r.get("key")}
    labels.update({r["key"]: r["label"] for r in lay["closing"]["rows"]})
    stc = form["statuses"]
    print("THE FORM  %s   schema %s   saved %s" % (form["file"], form["schema"], form["modified"]))
    print("  populated fields: %d (%s); list rows: %d" % (sum(stc.values()), ", ".join("%s %d" % kv for kv in sorted(stc.items())), sum(len(v) for v in form["lists"].values())))
    for k, v in sorted(form["ignored"].items()):
        print("  not read: %-12s %s" % (k, v))
    for st_ in ("preset", "heard", "verify"):
        ks = [k for k, c in form["fields"].items() if c["populated"] and c["st"] == st_]
        if ks:
            print("\n  %s values (check each against the call; each goes into the report either way):" % st_.upper())
            for k in ks:
                print("    %-28s %s" % (labels.get(k, k)[:28], form["fields"][k]["v"][:70].replace("\n", " ")))
    lk = form["lookup"]
    if lk["verdict"] != "empty":
        print("\n  COMPANY LOOK-UP TEXT: %s%s" % (lk["verdict"].upper().replace("_", " "), (" (" + "; ".join(lk["reasons"]) + ")") if lk["reasons"] else ""))
    np_ = ffform.note_problems(form)
    if np_:
        print("\n  NOTES THAT NEED CLEANING (name the chatter lines in overlay `clean`; repeated lines are dropped by the program; a cut-off note is flagged):")
        for n in np_:
            print("    - " + n)
    if pdf.get("used"):
        print("\n  THE PDF: %d values of the data file were checked against it; %d not found in it." % (pdf["checked"], len(pdf["not_found"])))
        for m in pdf["not_found"][:12]:
            print("    NOT IN THE PDF: %s = %r" % (m["label"], m["value"]))
        if pdf["pdf_only"]:
            print("  AMOUNTS ONLY THE PDF HOLDS (the form works them out; the data file has them empty). They go into the report automatically under their own heading;")
            print("  if one belongs in a row (for example a Risk Calculation line) add it as an overlay `fill` with the source {\"doc\": \"form PDF\", \"quote\": \"<the PDF's words>\"}:")
            for amt in pdf["pdf_only"]:
                print("    R %-12s  %s" % (amt, pdf["pdf_only_labels"].get(amt, "")))
    else:
        print("\n  THE PDF WAS NOT USED (%s): the data file alone is the source." % pdf.get("why"))
    if form["unknown_fields"] or form["odd"] or form["top_unknown"]:
        print("\n  Unusual: fields the layout does not know %s; odd entries %s; unknown top keys %s" % (form["unknown_fields"] or "none", form["odd"][:4] or "none", form["top_unknown"] or "none"))
    rj["form_report_shown"] = True
    save_run(a.run, rj)
    print("\nNEXT: python3 %s/run.py done %s form" % (SCRIPTS, a.run))


# ------------------------------------------------------------------ step 4: lead
def cmd_lead(a):
    load_run(a.run)
    if a.found:
        d = w.parse_date(a.received)
        if not d or not a.ref or not a.quote:
            w.die("REFUSED: --found needs --received DD/MM/YYYY, --ref (the email subject) and --quote (the line that shows it).")
        rec = {"searched": True, "found": True, "received": d.strftime("%d/%m/%Y"), "ref": a.ref, "quote": a.quote}
    elif a.none:
        if len(a.none.strip()) < 8:
            w.die("REFUSED: say what you searched and where (at least 8 characters).")
        rec = {"searched": True, "found": False, "none": a.none.strip()}
    elif a.unavailable:
        rec = {"searched": False, "found": False, "unavailable": a.unavailable.strip()}
    else:
        w.die("give --found, --none or --unavailable")
    w.save_json(p(a.run, w.LEAD), rec)
    print("lead recorded: %s" % json.dumps(rec)[:200])


# ------------------------------------------------------------------ step 5: combine
def check_quotes(run, ov):
    """Every call quote in the overlay must really be in the transcript, and every form-PDF quote in the PDF's text. Documents (Overview and the like) are not machine-checked. Returns (errors, call_quotes, doc_sources)."""
    st = w.load_opt(p(run, w.STATE), None)
    tr = w.norm(" ".join(w.read_lines(run))) if st and os.path.exists(p(run, w.TRANSCRIPT)) else ""
    pt = ""
    if os.path.exists(p(run, "form_pdf.txt")):
        pt = w.norm(open(p(run, "form_pdf.txt"), encoding="utf-8").read())
    errs, calls, docs = [], 0, 0
    items = [(n, it) for n in compose.OVERLAY_LISTS for it in ov.get(n) or [] if isinstance(it, dict)]
    if isinstance(ov.get("lookup"), dict):
        items.append(("lookup", ov["lookup"]))
    for name, it in items:
        for s in it.get("src") or []:
            if not isinstance(s, dict):
                continue
            q = str(s.get("quote") or "").strip()
            doc = str(s.get("doc") or "")
            if "line" in s or (not doc and q):
                calls += 1
                if not q:
                    errs.append("overlay.%s %s: a call source needs the exact words in `quote`" % (name, it.get("id")))
                elif w.norm(q) not in tr:
                    errs.append("overlay.%s %s: this quote is not in the transcript: %r (copy the exact words from the chunk you read)" % (name, it.get("id"), q[:70]))
            elif doc.lower() == "form pdf":
                if q and pt and w.norm(q) not in pt:
                    errs.append("overlay.%s %s: this quote is not in the form's PDF text: %r" % (name, it.get("id"), q[:70]))
            elif doc:
                docs += 1
    return errs, calls, docs


def cmd_combine(a):
    rj = load_run(a.run)
    if not os.path.exists(p(a.run, w.FORM)):
        w.die("step 1 first: run.py files ...")
    ov_path = p(a.run, w.OVERLAY)
    if not os.path.exists(ov_path):
        w.save_json(ov_path, {})
    try:
        inp = compose.load_inputs(a.run)
    except (ValueError, OSError) as e:
        w.die("overlay.json could not be read (%s): it must be valid JSON" % e)
    errs = compose.check_inputs(inp)
    qerrs, calls, docs = check_quotes(a.run, inp["overlay"])
    if errs or qerrs:
        print("COMBINE REFUSED. overlay.json has problems (nothing was made):")
        for e in (errs + qerrs)[:25]:
            print("  - " + e)
        sys.exit(1)
    content = compose.compose(inp)
    w.save_json(p(a.run, w.CONTENT), content)
    rj = load_run(a.run)
    gone = []
    if rj.get("combine") and rj["combine"].get("inputs_sha") != verify.inputs_sha(a.run):
        gone = reopen(a.run, rj, ["build", "save", "chain"])
        for k in ("build", "look", "saved", "ok", "chain"):
            rj.pop(k, None)
    rj["combine"] = {"inputs_sha": verify.inputs_sha(a.run), "call_quotes": calls, "doc_sources": docs, "t": w.now()}
    save_run(a.run, rj)
    rep = content["report"]
    nrows = sum(len(b["rows"]) for s in content["sections"] for b in s["blocks"])
    print("COMBINED content.json: %d sections, %d rows" % (len(content["sections"]), nrows))
    print("  contradictions between the form and the call or documents: %d (%d SORTED by a rule, %d HIGHLIGHTED for Paul)" % (len(rep["differences"]), rep["sorted"], rep["highlighted"]))
    for d in rep["differences"][:12]:
        print("    - %s: form %s | %s %s | %s" % (d["label"], d["form"], d["where"], d["other"], ("SORTED: " + d["settled"]) if d.get("settled") else "HIGHLIGHTED"))
    nd = rep["not_discussed"]
    print("  rows still 'Not discussed': %d" % len(nd))
    if nd:
        print("    " + ", ".join("%s (%s)" % (lbl, rid) for rid, lbl in nd[:60]) + (" ..." if len(nd) > 60 else ""))
        print("    Before you leave any of these, search the call, the Overview and the client's documents for it; fill what you find in overlay.json `fills`.")
    if rep["cleaned"]:
        print("  notes cleaned: %d" % len(rep["cleaned"]))
    if content["unsettled"]:
        print("  QUOTE REQUESTS WITHOUT INSURER OR BASIS: %s: ask Paul (one message), then add them under overlay `quotes`." % ", ".join(content["unsettled"]))
    if content["overlay_unused"]:
        print("  overlay entries that landed nowhere: %s" % ", ".join(content["overlay_unused"]))
    if content["pdf_fields"]:
        print("  amounts only the form's PDF holds, added under their own heading: %d" % len(content["pdf_fields"]))
    for g in content["glance"][:8]:
        print("  note: " + g[:200])
    if gone:
        print("  RE-OPENED because the report changed: steps %s. Redo them." % ", ".join(gone))
    print("\nWhen nothing is left to settle: python3 %s/run.py done %s combine" % (SCRIPTS, a.run))


# ------------------------------------------------------------------ step 6: build, look
def cmd_build(a):
    rj = load_run(a.run)
    c = current_content(a.run, rj)
    if c is None:
        w.die("REFUSED: content.json is missing or out of date: run `run.py combine %s` first." % a.run, 3)
    if not c.get("file_name"):
        w.die("REFUSED: the client's name or the meeting date is missing, so the file name cannot be made.", 3)
    info = build.build_run(a.run, c)
    gone = reopen(a.run, rj, ["save", "chain"])
    for k in ("look", "saved", "ok", "chain"):
        rj.pop(k, None)
    rj["build"] = {k: info[k] for k in ("pdf", "pdf_sha", "pdf_size", "pages", "headings", "font", "content_sha")}
    save_run(a.run, rj)
    f = info["font"]
    print("BUILT  %s   (%d page(s), %d bytes)" % (info["path"], info["pages"], info["pdf_size"]))
    print("  font used: %s%s" % (", ".join(f["ps_names"] or [f["family"]]), "" if f["aptos"] else "   <-- NOT Aptos (it was not found on this computer); say so to Paul"))
    print("  page images: %s/out/page-*.png: LOOK at every page, then: python3 %s/run.py look %s --saw \"<what you saw>\"" % (a.run, SCRIPTS, a.run))
    if gone:
        print("  RE-OPENED because the PDF was rebuilt: steps %s." % ", ".join(gone))


def cmd_look(a):
    rj = load_run(a.run)
    if not rj.get("build"):
        w.die("REFUSED: build the PDF first (run.py build).", 3)
    if len((a.saw or "").strip()) < 20:
        w.die("REFUSED: say what you saw on the pages (at least 20 characters).")
    rj["look"] = {"saw": a.saw.strip(), "build_sha": rj["build"]["pdf_sha"], "t": w.now()}
    save_run(a.run, rj)
    print("recorded: the page images of this build were looked at.")


# ------------------------------------------------------------------ step 7: saved, report, ok
def cmd_saved(a):
    rj = load_run(a.run)
    b = rj.get("build")
    if not b:
        w.die("REFUSED: build the PDF first.", 3)
    if a.listed_size != b["pdf_size"]:
        print("NOT THE SAME SIZE: the folder listing shows %d bytes but the built file is %d bytes. The file may be locked or the copy may lag: commit it again, wait a moment, list again, and record the new size. "
              "Never report it as saved until the sizes are equal." % (a.listed_size, b["pdf_size"]))
        sys.exit(1)
    rj["saved"] = {"folder": a.folder, "size": a.listed_size, "build_sha": b["pdf_sha"], "t": w.now()}
    save_run(a.run, rj)
    print("recorded: saved into %s, listed size %d bytes = the built file." % (a.folder, a.listed_size))
    if "2. fact find" not in a.folder.lower():
        print("NOTE: the folder path does not say '2. Fact Find': check it is the client's own folder.")


def cmd_report(a):
    rj = load_run(a.run)
    c = current_content(a.run, rj)
    if c is None:
        w.die("combine first")
    rep = c["report"]
    f = rj.get("files") or {}
    print("SOURCE REPORT (for the reply that presents the PDF)")
    print("(a) Sources used: the form's data file %s%s; the Teams transcript(s) %s; the Overview: %s." % (
        f.get("form"), (" and its PDF " + f["formpdf"]) if (w.load_opt(p(a.run, w.FORMPDF), {}) or {}).get("used") else " (its PDF was not used)",
        ", ".join(f.get("transcripts") or []), f.get("overview") or ("none (" + (f.get("missing") or "no reason given") + ")")))
    stc = rep.get("statuses") or {}
    print("(b) The form's fields: %s. Preset values: %s." % (", ".join("%s %d" % kv for kv in sorted(stc.items())), "; ".join("%s: %s" % (x["label"], x["done"]) for x in rep["presets"][:20]) or "none"))
    print("(c) Contradictions: %d (%d sorted, %d highlighted)." % (len(rep["differences"]), rep["sorted"], rep["highlighted"]))
    for d in rep["differences"]:
        print("    - %s: the form says %s; %s says %s. %s" % (d["label"], d["form"], d["where"], d["other"], ("SORTED: " + d["settled"]) if d.get("settled") else "HIGHLIGHTED: Paul decides."))
    nd = rep["not_discussed"]
    print("(d) Left 'Not discussed' after the search: %d%s; filled from the call or documents: %d." % (len(nd), (": " + ", ".join(lbl for _, lbl in nd[:25])) if nd else "", len(rep["filled"])))
    if rep["cleaned"]:
        print("(e) Notes cleaned: " + "; ".join("%s: %s (%s)" % (x["key"], x["line"][:40], x["why"]) for x in rep["cleaned"][:8]))
    for g in c["glance"][:8]:
        print("    glance: " + g[:220])


def cmd_ok(a):
    rj = load_run(a.run)
    if not (rj.get("saved") and rj.get("build")):
        w.die("REFUSED: save the PDF and list it back first (run.py saved).", 3)
    if len((a.paul_said or "").strip()) < 2:
        w.die("REFUSED: give Paul's own words.")
    rj["ok"] = {"said": a.paul_said.strip(), "build_sha": rj["build"]["pdf_sha"], "t": w.now()}
    save_run(a.run, rj)
    print("recorded Paul's OK of this version of the Fact Find.")


# ------------------------------------------------------------------ step 8: chain
def cmd_chain(a):
    rj = load_run(a.run)
    if not (rj.get("ok") and rj["ok"].get("build_sha") == (rj.get("build") or {}).get("pdf_sha")):
        w.die("REFUSED: Paul's OK of this version is not recorded yet (run.py ok).", 3)
    for k in ("summary", "planner", "sitamah"):
        if len((getattr(a, k) or "").strip()) < 3:
            w.die("REFUSED: --%s is needed (what was made / where it went)." % k)
    rj["chain"] = {"summary": a.summary.strip(), "planner": a.planner.strip(), "sitamah": a.sitamah.strip(), "t": w.now()}
    save_run(a.run, rj)
    print("recorded the three outputs. Now: python3 %s/run.py done %s chain  (it prints the short audit)" % (SCRIPTS, a.run))


# ------------------------------------------------------------------ cli
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add(name, fn, *args):
        sp = sub.add_parser(name)
        for arg in args:
            sp.add_argument(arg)
        sp.set_defaults(fn=fn)
        return sp

    sp = add("start", cmd_start, "run")
    sp.add_argument("--client", required=True)
    sp.add_argument("--date", required=True)
    sp.add_argument("--other-run", dest="other_run")
    add("next", cmd_next, "run")
    add("done", cmd_done, "run", "step")
    add("status", cmd_status, "run")
    sp = sub.add_parser("preflight")
    sp.set_defaults(fn=lambda a: (lambda r: (print_preflight(r[1]), sys.exit(0 if r[0] else 4)))(preflight()))
    sp = add("files", cmd_files, "run")
    sp.add_argument("--form")
    sp.add_argument("--formpdf")
    sp.add_argument("--transcript", action="append")
    sp.add_argument("--overview")
    sp.add_argument("--missing")
    sp.add_argument("--force-incomplete", dest="force_incomplete")
    add("form", cmd_form, "run")
    sp = add("lead", cmd_lead, "run")
    sp.add_argument("--found", action="store_true")
    sp.add_argument("--received")
    sp.add_argument("--ref")
    sp.add_argument("--quote")
    sp.add_argument("--none")
    sp.add_argument("--unavailable")
    add("combine", cmd_combine, "run")
    add("build", cmd_build, "run")
    sp = add("look", cmd_look, "run")
    sp.add_argument("--saw", required=True)
    sp = add("saved", cmd_saved, "run")
    sp.add_argument("--folder", required=True)
    sp.add_argument("--listed-size", dest="listed_size", type=int, required=True)
    add("report", cmd_report, "run")
    sp = add("ok", cmd_ok, "run")
    sp.add_argument("--paul-said", dest="paul_said", required=True)
    sp = add("chain", cmd_chain, "run")
    sp.add_argument("--summary", required=True)
    sp.add_argument("--planner", required=True)
    sp.add_argument("--sitamah", required=True)
    a = ap.parse_args()
    if getattr(a, "run", None):
        a.run = os.path.abspath(a.run)
    a.fn(a)


if __name__ == "__main__":
    main()
