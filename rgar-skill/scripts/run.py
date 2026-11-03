#!/usr/bin/env python3
"""The step driver of the rgar-skill: shows ONE step at a time, refuses to skip, keeps the run on disk.

  run.py start <run> --client "First Surname"
  run.py next | status | preflight
  run.py access <run> --purpose locate|save --route device|m365|zapier --result found|failed [--note TEXT]
  run.py doc <run> --role ROLE --file FILE --route ROUTE          register a client document (rgar_report, fact_find_summary, fact_find_summary_older)
  run.py doc <run> --missing ROLE --said "Paul's words"           a document that does not exist
  run.py read <run> [--ack ROLE:PAGE --note TEXT]                 the documents' text, one page at a time
  run.py answers <run> --file answers.json                        the answers, each with its source
  run.py show <run>                                               the confirmation table and the ONE question
  run.py approve <run> --said "Paul's exact words"
  run.py build <run>                                              build the email, the saved no-logo copy and the text for the Outlook draft
  run.py name <run> --existing "a.html;b.html" [--overwrite-yes "Paul's words"]
  run.py draft <run> --file readback.json                         check the saved read-back of the Outlook draft
  run.py message <run> --used-today yes|no                        the exact Teams message and how to send it (only after the draft check)
  run.py messagecheck <run> --file readback.txt                   check the saved read-back of the posted Teams message
  run.py receipt <run> KEY VALUE
  run.py done <run> STEP                                          prove the step, then show the next one

Claude runs these programs as they are and never rewrites them during a run. Nothing here sends anything to anyone: the chat sends, after Paul's yes.
"""
import argparse
import os
import re
import shutil
import sys

import docread
import rgi
import verify
import wrlib as w

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
RULE = "=" * 78
LATER = {"answers": ["confirm", "build", "save", "draft", "message", "final"], "build": ["save", "draft", "message", "final"]}


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
    rows = []
    try:
        __import__("pdfplumber")
        rows.append((True, "python module pdfplumber is available"))
    except ImportError:
        rows.append((False, "python module pdfplumber is NOT available (try: pip install pdfplumber)"))
    rows.append((os.path.exists(rgi.TEMPLATE) and os.path.exists(rgi.LABELS) and os.path.exists(rgi.SETTINGS), "the proposal template, the net-target labels and the settings are in the skill"))
    try:
        with open(rgi.TEMPLATE, encoding="utf-8") as f:
            t = f.read()
        ok = all(t.count(ph) == rgi.EXPECTED_COUNT.get(ph, 1) for ph in rgi.SINGLE + tuple(rgi.EXPECTED_COUNT)) and "<!-- BODY START -->" in t and "<!-- LOGO START -->" in t
        rows.append((ok, "the template carries every placeholder and marker the program fills"))
    except OSError:
        rows.append((False, "the template cannot be read"))
    rows.append((w.skill_stamp() is not None, "the skill has a Last updated stamp (%s)" % (w.stamp_display(w.skill_stamp()) or "none")))
    return all(r[0] for r in rows), rows


def _checks(run, *groups):
    R, rj = verify.run_checks(run, "pre")
    out = [r[1] for r in R.rows if r[0] == verify.BAD and r[3] in groups]
    for g in groups:
        if not any(r[3] == g for r in R.rows):
            out.append("the checker has no result yet for '%s'" % g)
    return out


def ck_final(run, rj):
    R, rj2 = verify.run_checks(run, "final")
    if R.fails:
        verify.print_audit(R, rj2, "final", run)
        return ["the checker has %d red cross(es) above" % len(R.fails)]
    return []


CHECKS = {
    "locate_ok": lambda run, rj: _checks(run, "docs"),
    "read_ok": lambda run, rj: _checks(run, "docs", "read"),
    "answers_ok": lambda run, rj: _checks(run, "docs", "answers"),
    "confirm_ok": lambda run, rj: _checks(run, "answers", "confirm"),
    "build_ok": lambda run, rj: _checks(run, "answers", "confirm", "build"),
    "save_ok": lambda run, rj: _checks(run, "build", "save"),
    "draft_ok": lambda run, rj: _checks(run, "build", "draft"),
    "message_ok": lambda run, rj: _checks(run, "draft", "message"),
    "verify_final": ck_final,
}


def reopen(run, after):
    rj = load_run(run)
    again = [s for s in LATER[after] if (rj["steps"].get(s) or {}).get("state") == "done"]
    for s in again:
        rj["steps"].pop(s, None)
    save_run(run, rj)
    if again:
        print("LATER STEPS RE-OPENED because this changed: redo %s." % ", ".join(again))


def guard(rj):
    if rj.get("program_fingerprint") and rj["program_fingerprint"] != w.program_fingerprint():
        w.die("REFUSED: the skill's programs, steps, rule pages, template or settings changed while this run was in progress. The programs are run as they are. Start again in a new run folder.", 3)


# ------------------------------------------------------------------ commands
def cmd_start(a):
    parts = a.client.split()
    if len(parts) < 2:
        w.die('--client must be the first name and surname, for example --client "Pat Samplecase"')
    if os.path.exists(p(a.run, w.RUN)):
        old = load_run(a.run)
        if w.norm(old["client"]) != w.norm(a.client):
            w.die("REFUSED: this run folder already belongs to %s. Use a NEW run folder." % old["client"], 2)
        print("This run already exists. Showing where it is up to.")
        return cmd_next(a)
    ok, rows = preflight()
    print("SELF-TEST BEFORE ANYTHING ELSE:")
    for good, text in rows:
        print("  [%s] %s" % ("OK" if good else "FAIL", text))
    if not ok:
        w.die("\nSTOP. Tell Paul exactly which item failed above. Do not carry on.", 4)
    os.makedirs(os.path.join(a.run, w.OUT, "saved"), exist_ok=True)
    os.makedirs(os.path.join(a.run, w.DOCS_DIR), exist_ok=True)
    rj = {"skill": w.skill_name(), "created": w.now(), "skill_stamp": w.skill_stamp(), "steps": {}, "client": " ".join(parts),
          "today": w.today().strftime("%d/%m/%Y"), "program_fingerprint": w.program_fingerprint()}
    save_run(a.run, rj)
    for name, empty in ((w.ACCESS, []), (w.RECEIPT, {}), (w.STATE, {}), (w.DOCS, {"docs": {}, "missing": {}})):
        w.save_json(p(a.run, name), empty)
    print("\nSAY THIS TO PAUL FIRST, before anything else in your reply, in exactly these words:\n    %s.\n" % w.version_line())
    print("RUN STARTED  client: %s\n" % rj["client"])
    print("Standing rules for the whole job:\n")
    print(expand(read_ref("00-rules.md"), a.run))
    print()
    show_step(a.run, rj, current_step(rj))


def cmd_next(a):
    rj = load_run(a.run)
    s = current_step(rj)
    if s is None:
        print("Every step is done. Run: python3 %s/verify.py %s  and put its SHORT AUDIT in your reply." % (SCRIPTS, a.run))
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
        print("EVERY STEP IS DONE.\nPut this SHORT AUDIT in your reply, as it is (nothing longer):\n")
        R, rj2 = verify.run_checks(a.run, "final")
        verify.print_audit(R, rj2, "final", a.run)
        return
    show_step(a.run, rj, nxt)


def cmd_access(a):
    rj = load_run(a.run)
    guard(rj)
    log = w.load_opt(p(a.run, w.ACCESS), [])
    log.append({"purpose": a.purpose, "route": a.route, "result": a.result, "note": a.note or "", "t": w.now()})
    w.save_json(p(a.run, w.ACCESS), log)
    print("access try recorded: %s %s %s (%d on record)" % (a.purpose, a.route, a.result, len(log)))


def cmd_doc(a):
    rj = load_run(a.run)
    guard(rj)
    docs = w.load_opt(p(a.run, w.DOCS), {"docs": {}, "missing": {}})
    if a.missing:
        if not rgi.can_be_missing(a.missing) or len((a.said or "").strip()) < 5:
            w.die("REFUSED: --missing is only for fact_find_summary_older, with Paul's own words (--said). The RGAR report and the Fact Find Summary can never be missing: "
                  "with no Fact Find Summary the skill STOPS and asks Paul.")
        docs["missing"][a.missing] = a.said.strip()
        w.save_json(p(a.run, w.DOCS), docs)
        print("recorded: %s is not available (Paul: %s)" % (a.missing, a.said.strip()))
        return
    if not rgi.valid_role(a.role):
        w.die("REFUSED: role must be one of %s" % ", ".join(rgi.FIXED_ROLES))
    if not a.file or not os.path.isfile(a.file) or not a.route:
        w.die("REFUSED: give --file (an existing file) and --route")
    log = [e for e in w.load_opt(p(a.run, w.ACCESS), []) if e.get("purpose") == "locate"]
    if not any(e["route"] == a.route and e["result"] == "found" for e in log):
        w.die("REFUSED: record the access try first: run.py access %s --purpose locate --route %s --result found" % (a.run, a.route))
    bad = verify.route_order_problems(log)
    if bad:
        w.die("REFUSED: the routes are tried in order (computer, Microsoft 365, Zapier); %s was used before the earlier ones failed." % ", ".join(bad))
    ext = os.path.splitext(a.file)[1].lower() or ".pdf"
    dst = os.path.join(w.DOCS_DIR, a.role + ext)
    shutil.copyfile(a.file, p(a.run, dst))
    try:
        rep = docread.read_document(p(a.run, dst))
    except Exception as e:
        os.remove(p(a.run, dst))
        print("STOP. This file cannot be used: %s" % e)
        sys.exit(5)
    served = [pg["n"] for pg in rep["pages"]]
    tf = os.path.join(w.DOCS_DIR, a.role + ".text.json")
    w.save_json(p(a.run, tf), rep)
    before = docs["docs"].get(a.role)
    docs["docs"][a.role] = {"file": dst, "text_file": tf, "name": os.path.basename(a.file), "route": a.route, "sha": w.sha256_file(p(a.run, dst)), "pages": rep["page_count"],
                            "served": served, "image_only": rep["image_only"]}
    docs["missing"].pop(a.role, None)
    w.save_json(p(a.run, w.DOCS), docs)
    print("document registered: %s = %s (%d page(s)) via %s" % (a.role, os.path.basename(a.file), rep["page_count"], a.route))
    if rep["image_only"]:
        print("NOTE: page(s) %s have no readable text. View them as images yourself; figures on them cannot be checked by the program." % ", ".join(map(str, rep["image_only"])))
    if before and before["sha"] != docs["docs"][a.role]["sha"] and os.path.exists(p(a.run, w.ANSWERS)):
        print("A document changed: run answers again so every entry is re-checked against it.")


def cmd_read(a):
    rj = load_run(a.run)
    guard(rj)
    docs = w.load_opt(p(a.run, w.DOCS), {"docs": {}, "missing": {}})
    keys = verify.served_keys(docs)
    if not keys:
        w.die("No document is registered yet: run.py doc first.")
    st = w.load_opt(p(a.run, w.STATE), {})
    acked = st.setdefault("read", {}).setdefault("acked", {})
    nxt = next((k for k in keys if "%s:%d" % k not in acked), None)
    if a.ack:
        if nxt is None or a.ack != "%s:%d" % nxt:
            w.die("REFUSED: pages are acknowledged in order. The next page is %s." % ("%s:%d" % nxt if nxt else "none (all done)"))
        if len((a.note or "").strip()) < 3:
            w.die('REFUSED: acknowledge the page with a one-line note of what is on it: --note "..."')
        acked[a.ack] = a.note.strip()
        w.save_json(p(a.run, w.STATE), st)
        print("page %s acknowledged (%d of %d)" % (a.ack, len(acked), len(keys)))
        nxt = next((k for k in keys if "%s:%d" % k not in acked), None)
    if nxt is None:
        print("All %d pages were read and acknowledged. Now run: python3 %s/run.py done %s read" % (len(keys), SCRIPTS, a.run))
        return
    role, n = nxt
    rep = w.load_json(p(a.run, docs["docs"][role]["text_file"]))
    pg = next(x for x in rep["pages"] if x["n"] == n)
    print("-" * 24 + " %s - PAGE %d of %d " % (role, n, rep["page_count"]) + "-" * 24)
    if n in rep["image_only"]:
        print("THIS PAGE HAS NO READABLE TEXT. View it as an image yourself (for example: pdftoppm -f %d -l %d -png -r 80 %s page), then acknowledge it." % (n, n, p(a.run, docs["docs"][role]["file"])))
    else:
        print(pg["text"])
    print("-" * 78)
    print('Read it fully, then: python3 %s/run.py read %s --ack %s:%d --note "one line on what is on this page"' % (SCRIPTS, a.run, role, n))


def _load_answers_checked(run, rj, file=None):
    docs, ev = verify.load_docs(run)
    a = w.load_json(file or p(run, w.ANSWERS), "the answers file")
    return a, rgi.answers_problems(a, ev, docs, w.parse_date(rj["today"]), rj["client"]), docs


def cmd_answers(a):
    rj = load_run(a.run)
    guard(rj)
    ans, probs, docs = _load_answers_checked(a.run, rj, a.file)
    if probs:
        print("REFUSED (nothing saved):\n  - " + "\n  - ".join(probs))
        sys.exit(5)
    before = verify.sha_of(w.load_opt(p(a.run, w.ANSWERS), {}))
    w.save_json(p(a.run, w.ANSWERS), ans)
    if before != verify.sha_of(ans):
        if os.path.exists(p(a.run, w.APPROVAL)):
            os.remove(p(a.run, w.APPROVAL))
        st = w.load_opt(p(a.run, w.STATE), {})
        st.pop("shown_sha", None)
        w.save_json(p(a.run, w.STATE), st)
        reopen(a.run, "answers")
    st_, en_ = rgi.shortfall(ans)
    print("answers saved: an RGAR proposal for %s; every figure was found in the right document's text; the shortfall runs from %s until %s (worked out by the program)." % (ans["client_full_name"], st_, en_))


def cmd_show(a):
    rj = load_run(a.run)
    guard(rj)
    ans, probs, docs = _load_answers_checked(a.run, rj)
    if probs:
        w.die("REFUSED: the answers are not valid yet: " + "; ".join(probs[:2]))
    rows = rgi.table_rows(ans, docs)
    st = w.load_opt(p(a.run, w.STATE), {})
    st["shown_sha"] = verify.confirm_sha(ans, docs)
    w.save_json(p(a.run, w.STATE), st)
    print("CONFIRMATION TABLE (question | answer | source):\n")
    for q, v, s in rows:
        print("- %s | %s | %s" % (q, v.replace("\n", " / ") if len(v) < 80 else "\n" + v, s or ""))
    print("\nTHE ONE QUESTION TO PAUL (show the whole table in the reply, then ask exactly this):\n    Are these answers right, so that I build the email for %s, save the copy, make the Outlook draft "
          "and then message Sitamah?\n" % ans["client_full_name"])
    print("When he says yes: python3 %s/run.py approve %s --said \"his exact words\"" % (SCRIPTS, a.run))


def cmd_approve(a):
    rj = load_run(a.run)
    guard(rj)
    ans, probs, docs = _load_answers_checked(a.run, rj)
    if probs:
        w.die("REFUSED: the answers are not valid yet.")
    cur = verify.confirm_sha(ans, docs)
    st = w.load_opt(p(a.run, w.STATE), {})
    if st.get("shown_sha") != cur:
        w.die("REFUSED: Paul has not been shown exactly these answers. Run show, put the table in the reply, and only then record his yes.")
    if len((a.said or "").strip()) < 3:
        w.die("REFUSED: record Paul's own words with --said.")
    w.save_json(p(a.run, w.APPROVAL), {"sha": cur, "said": a.said, "t": w.now()})
    print("Paul's yes recorded for exactly these answers.")


def cmd_build(a):
    rj = load_run(a.run)
    guard(rj)
    probs = _checks(a.run, "answers", "confirm")
    if probs:
        w.die("REFUSED: " + "; ".join(probs))
    ans = w.load_json(p(a.run, w.ANSWERS))
    clock = w.now_sast()
    sent = rgi.sent_text(clock)
    try:
        full, nologo, body = rgi.build_all(ans, sent, w.load_opt(p(a.run, w.DOCS), {"docs": {}, "missing": {}}))
    except ValueError as e:
        w.die("STOP. The email cannot be built: %s" % e, 5)
    res = rgi.html_problems(full, nologo, body, ans, sent, w.load_opt(p(a.run, w.DOCS), {"docs": {}, "missing": {}}))
    badr = [r for r in res if not r[0]]
    if badr:
        w.die("STOP. The program's own check of the built email failed: %s" % "; ".join(r[1] for r in badr), 5)
    out = p(a.run, w.OUT)
    for d in (out, os.path.join(out, "saved")):
        os.makedirs(d, exist_ok=True)
        for f in os.listdir(d):
            if f.endswith(".html"):
                os.remove(os.path.join(d, f))
    name = rgi.file_name(ans, clock.date())
    files = {"full": os.path.join(out, name), "saved": os.path.join(out, "saved", name), "body": os.path.join(out, "draft_body.html")}
    for k, text in (("full", full), ("saved", nologo), ("body", body)):
        with open(files[k], "w", encoding="utf-8", newline="") as f:
            f.write(text)
    st = w.load_opt(p(a.run, w.STATE), {})
    st["build"] = {"t": w.now(), "sent": sent, "date": clock.strftime("%d/%m/%Y"), "name": name, "size": os.path.getsize(files["saved"]),
                   "sha": {"full": w.sha256_text(full), "saved": w.sha256_text(nologo), "body": w.sha256_text(body)}}
    for k in ("save", "draft", "message"):
        st.pop(k, None)
    w.save_json(p(a.run, w.STATE), st)
    reopen(a.run, "build")
    print("BUILT from the confirmed answers and the fixed template (%d program checks passed):" % len(res))
    print("  email for Paul in the chat (with the logo): %s" % files["full"])
    print("  copy to SAVE in Comparative Quotes (no logo):  %s" % files["saved"])
    print("  text to paste into the Outlook draft:       %s" % files["body"])
    print("  subject (character for character): %s" % rgi.subject(ans))


def cmd_name(a):
    rj = load_run(a.run)
    guard(rj)
    st = w.load_opt(p(a.run, w.STATE), {})
    if not st.get("build"):
        w.die("Build the email first (run.py build).")
    existing = [x.strip() for x in (a.existing or "").split(";") if x.strip()]
    name = st["build"]["name"]
    clash = w.norm(name) in {w.norm(e) for e in existing}
    if clash and len((a.overwrite_yes or "").strip()) < 3:
        print("STOP. A file named %r already exists in the client's folder. Ask Paul. If he says to overwrite, run this again with --overwrite-yes \"his words\"." % name)
        sys.exit(5)
    st["save"] = {"name": name, "existing": existing, "existing_clash": clash, "overwrite": (a.overwrite_yes or "").strip() if clash else ""}
    w.save_json(p(a.run, w.STATE), st)
    path = p(a.run, os.path.join(w.OUT, "saved", name))
    print("SAVE THIS FILE: %s" % path)
    docs = w.load_opt(p(a.run, w.DOCS), {"docs": {}, "missing": {}})
    rg = docs["docs"]["rgar_report"]
    print("Name to use in the RA transaction folder's Comparative Quotes: %s   (%d bytes)" % (name, os.path.getsize(path)))
    print("ALSO put a copy of the RGAR PDF there (sharepoint_copy_item into the same Comparative Quotes folder; the original stays where it is): %s   (%d bytes)" % (rg["name"], os.path.getsize(p(a.run, rg["file"]))))
    print("Then record: run.py access ... --purpose save (computer, then Microsoft 365, then Zapier), run.py receipt save.folder <the folder> and save.listed_bytes <the size the listing shows for the html>, "
          "and run.py receipt save.rgar_name <the RGAR file name in the listing> and save.rgar_listed_bytes <its size in the listing>")


def cmd_receipt(a):
    rj = load_run(a.run)
    guard(rj)
    rc = w.load_opt(p(a.run, w.RECEIPT), {})
    rc[a.key] = a.value
    w.save_json(p(a.run, w.RECEIPT), rc)
    print("receipt recorded: %s = %s" % (a.key, a.value))


def _readback(run, rj, path, key, fn):
    """Save the chat's read-back next to the run, check it, and record the result."""
    if not path or not os.path.isfile(path):
        w.die("REFUSED: give --file (the saved read-back).")
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    return text


def cmd_draft(a):
    rj = load_run(a.run)
    guard(rj)
    ans = w.load_opt(p(a.run, w.ANSWERS), None)
    st = w.load_opt(p(a.run, w.STATE), {})
    if not ans or not st.get("build") or not st.get("save"):
        w.die("REFUSED: build the email and record the save first.")
    text = _readback(a.run, rj, a.file, "draft", None)
    dst = p(a.run, os.path.join(w.OUT, "draft_readback.txt"))
    with open(dst, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    res = rgi.draft_problems(text, ans, rgi.settings()["signature_mode"])
    for ok, short in res:
        print("%s %s" % (verify.OK if ok else verify.BAD, short))
    good = all(ok for ok, _ in res)
    st["draft"] = {"t": w.now(), "sha": w.sha256_file(dst), "ok": good}
    st.pop("message", None)
    w.save_json(p(a.run, w.STATE), st)
    if not good:
        print("\nThe draft is NOT right. Fix it in Outlook (never send it), read it back again and run this again. Do not message Sitamah.")
        sys.exit(5)
    print("\nThe draft passed. Record the cleanup: run.py receipt %s draft.tab_closed yes   and   run.py receipt %s draft.stray_deleted <number or none>" % (a.run, a.run))


def cmd_message(a):
    rj = load_run(a.run)
    guard(rj)
    ans = w.load_opt(p(a.run, w.ANSWERS), None)
    st = w.load_opt(p(a.run, w.STATE), {})
    probs = _checks(a.run, "answers", "confirm", "build", "save", "draft")
    if probs or not (st.get("draft") or {}).get("ok"):
        w.die("REFUSED: Sitamah is messaged only after Paul's yes and a checked draft: " + ("; ".join(probs[:3]) if probs else "the draft check has not passed"))
    docs = w.load_opt(p(a.run, w.DOCS), {"docs": {}, "missing": {}})
    clock = w.now_sast()
    greeting = rgi.greeting_for(clock, a.used_today == "yes")
    text = rgi.teams_text(ans, docs, greeting)
    st["message"] = {"t": w.now(), "greeting": greeting, "used_today": a.used_today, "clock": clock.strftime("%H:%M"), "text_sha": w.sha256_text(text)}
    w.save_json(p(a.run, w.STATE), st)
    print("TEAMS MESSAGE (send it through Zapier, never through Chrome or the Teams tool that lacks the scope):\n")
    print(text)
    print("\nHOW: Zapier list_dynamic_enum_values (tool_name microsoft_teams_send_chat_message, property_name chat, search \"Sitamah Nathoo\") and take the 1:1 chat:\n  %s\n  (label %s) - never a meeting chat." %
          (rgi.SITAMAH_CHAT, rgi.CHAT_LABEL))
    print("Then microsoft_teams_send_chat_message with that chat, format \"markdown\" and content = the text above (an output_hint is required). Read the posted message back with read_resource, save it to a file,")
    print("record: run.py receipt %s message.chat <the chat value used>   run.py receipt %s message.format markdown   then: run.py messagecheck %s --file <the saved read-back>" % (a.run, a.run, a.run))


def cmd_messagecheck(a):
    rj = load_run(a.run)
    guard(rj)
    ans = w.load_opt(p(a.run, w.ANSWERS), None)
    st = w.load_opt(p(a.run, w.STATE), {})
    if not st.get("message"):
        w.die("REFUSED: run.py message first (it builds and shows the message; nothing is posted before that).")
    docs = w.load_opt(p(a.run, w.DOCS), {"docs": {}, "missing": {}})
    text = _readback(a.run, rj, a.file, "message", None)
    dst = p(a.run, os.path.join(w.OUT, "message_readback.txt"))
    with open(dst, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    res = rgi.message_problems(text, ans, docs, st["message"]["greeting"])
    for ok, short in res:
        print("%s %s" % (verify.OK if ok else verify.BAD, short))
    st["message"]["sha"] = w.sha256_file(dst)
    st["message"]["ok"] = all(ok for ok, _ in res)
    w.save_json(p(a.run, w.STATE), st)
    if not st["message"]["ok"]:
        print("\nThe posted message does not read right. Tell Paul exactly which line; only delete a message Claude itself posted, and only when Paul asks for a redo.")
        sys.exit(5)
    print("\nThe posted message reads right. Make sure message.chat and message.format are recorded, then: run.py done %s message" % a.run)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    x = sub.add_parser("start")
    x.add_argument("run")
    x.add_argument("--client", required=True)
    x.set_defaults(fn=cmd_start)
    x = sub.add_parser("preflight")
    x.set_defaults(fn=cmd_preflight)
    for name, fn in (("next", cmd_next), ("status", cmd_status), ("show", cmd_show), ("build", cmd_build)):
        x = sub.add_parser(name)
        x.add_argument("run")
        x.set_defaults(fn=fn)
    x = sub.add_parser("done")
    x.add_argument("run")
    x.add_argument("step")
    x.set_defaults(fn=cmd_done)
    x = sub.add_parser("access")
    x.add_argument("run")
    x.add_argument("--purpose", required=True, choices=("locate", "save"))
    x.add_argument("--route", required=True, choices=w.ROUTES)
    x.add_argument("--result", required=True, choices=("found", "failed"))
    x.add_argument("--note")
    x.set_defaults(fn=cmd_access)
    x = sub.add_parser("doc")
    x.add_argument("run")
    x.add_argument("--role")
    x.add_argument("--file")
    x.add_argument("--route", choices=w.ROUTES)
    x.add_argument("--missing")
    x.add_argument("--said")
    x.set_defaults(fn=cmd_doc)
    x = sub.add_parser("read")
    x.add_argument("run")
    x.add_argument("--ack")
    x.add_argument("--note")
    x.set_defaults(fn=cmd_read)
    x = sub.add_parser("answers")
    x.add_argument("run")
    x.add_argument("--file", required=True)
    x.set_defaults(fn=cmd_answers)
    x = sub.add_parser("approve")
    x.add_argument("run")
    x.add_argument("--said", required=True)
    x.set_defaults(fn=cmd_approve)
    x = sub.add_parser("name")
    x.add_argument("run")
    x.add_argument("--existing", default="")
    x.add_argument("--overwrite-yes", dest="overwrite_yes")
    x.set_defaults(fn=cmd_name)
    x = sub.add_parser("receipt")
    x.add_argument("run")
    x.add_argument("key")
    x.add_argument("value")
    x.set_defaults(fn=cmd_receipt)
    x = sub.add_parser("draft")
    x.add_argument("run")
    x.add_argument("--file", required=True)
    x.set_defaults(fn=cmd_draft)
    x = sub.add_parser("message")
    x.add_argument("run")
    x.add_argument("--used-today", dest="used_today", choices=("yes", "no"), required=True)
    x.set_defaults(fn=cmd_message)
    x = sub.add_parser("messagecheck")
    x.add_argument("run")
    x.add_argument("--file", required=True)
    x.set_defaults(fn=cmd_messagecheck)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
