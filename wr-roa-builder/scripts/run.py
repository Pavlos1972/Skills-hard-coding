#!/usr/bin/env python3
"""The step driver of the wr-roa-builder: shows ONE step at a time, refuses to skip, keeps the run on disk.

  run.py start <run> --client "First Surname" --bundle risk|retirement|investment
  run.py next | status | preflight
  run.py access <run> --purpose locate|save --route device|m365|zapier --result found|failed [--note TEXT]
  run.py doc <run> --role ROLE --file FILE --route ROUTE [--same-as ROLE]       register a client document
  run.py doc <run> --missing ROLE --said "Paul's words"                         a required document that does not exist
  run.py read <run> [--ack ROLE:PAGE --note TEXT]                               the documents' text, one page at a time
  run.py answers <run> --file answers.json                                      the setup answers (Step 0b), each with its source
  run.py show <run>                                                             the confirmation table and the ONE question
  run.py approve <run> --said "Paul's exact words"
  run.py email <run> --file email.html [--base-pt N]                            Retirement / Investment: the reply + quoted proposal page
  run.py build <run>                                                            assemble, build the ROA, embed the email pages
  run.py check <run> [--no-render]                                              prove what the program can; render page images
  run.py name <run> --existing "a.docx;b.docx" [--overwrite-yes "Paul's words"]
  run.py receipt <run> KEY VALUE
  run.py done <run> STEP                                                        prove the step, then show the next one

Claude runs these programs as they are and never rewrites them during a run (the two scripts included). Nothing here sends anything to anyone.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

import build_roa as br
import docread
import embedpipe
import roa
import verify
import wrlib as w

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
RULE = "=" * 78
LATER = {"answers": ["confirm", "email", "build", "check", "save", "final"], "email": ["build", "check", "save", "final"], "build": ["check", "save", "final"]}


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
    for mod, pip in (("pdfplumber", "pdfplumber"), ("docx", "python-docx"), ("lxml", "lxml"), ("PIL", "Pillow")):
        try:
            __import__(mod)
            rows.append((True, "python module %s is available" % mod))
        except ImportError:
            rows.append((False, "python module %s is NOT available (try: pip install %s)" % (mod, pip)))
    for t in ("zip", "unzip", "pdftoppm"):
        rows.append((shutil.which(t) is not None, "%s is %savailable" % (t, "" if shutil.which(t) else "NOT ")))
    rows.append((os.path.exists(w.TEMPLATE) and os.path.exists(w.BANK), "the ROA template and the reason-text bank are in the skill"))
    rows.append((w.skill_stamp() is not None, "the skill has a Last updated stamp (%s)" % (w.stamp_display(w.skill_stamp()) or "none")))
    return all(r[0] for r in rows), rows


def _checks(run, *groups):
    R, rj = verify.run_checks(run, "pre")
    out = [r[1] for r in R.rows if r[0] == verify.BAD and r[3] in groups]
    for g in groups:
        if not any(r[3] == g for r in R.rows):
            out.append("the checker has no result yet for '%s'" % g)
    return out


def _bundle(run):
    a = w.load_opt(p(run, w.ANSWERS), None)
    return (a or {}).get("bundle")


def ck_email(run, rj):
    return [] if _bundle(run) == "risk" else _checks(run, "docs", "answers", "confirm", "email")


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
    "email_ok": ck_email,
    "build_ok": lambda run, rj: _checks(run, "answers", "confirm", "build") + (_checks(run, "email") if _bundle(run) != "risk" else []),
    "check_ok": lambda run, rj: _checks(run, "build", "docx"),
    "save_ok": lambda run, rj: _checks(run, "docx", "save"),
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


# ------------------------------------------------------------------ commands
def cmd_start(a):
    parts = a.client.split()
    if len(parts) < 2:
        w.die('--client must be the first name and surname, for example --client "Pat Samplecase"')
    if os.path.exists(p(a.run, w.RUN)):
        old = load_run(a.run)
        if w.norm(old["client"]) != w.norm(a.client) or old.get("bundle") != a.bundle:
            w.die("REFUSED: this run folder already belongs to %s (%s). Use a NEW run folder." % (old["client"], old.get("bundle")), 2)
        print("This run already exists. Showing where it is up to.")
        return cmd_next(a)
    ok, rows = preflight()
    print("SELF-TEST BEFORE ANYTHING ELSE:")
    for good, text in rows:
        print("  [%s] %s" % ("OK" if good else "FAIL", text))
    for t in embedpipe.tools_problems():
        if "wkhtmltopdf" in t:
            print("  [NOTE] %s: a Retirement or Investment ROA cannot be built here; a Risk ROA can" % t)
    if not ok:
        w.die("\nSTOP. Tell Paul exactly which item failed above. Do not carry on.", 4)
    os.makedirs(os.path.join(a.run, w.OUT), exist_ok=True)
    os.makedirs(os.path.join(a.run, w.DOCS_DIR), exist_ok=True)
    rj = {"skill": w.skill_name(), "created": w.now(), "skill_stamp": w.skill_stamp(), "steps": {}, "client": " ".join(parts), "bundle": a.bundle,
          "today": w.today().strftime("%d/%m/%Y"), "program_fingerprint": w.program_fingerprint()}
    save_run(a.run, rj)
    for name, empty in ((w.ACCESS, []), (w.RECEIPT, {}), (w.STATE, {}), (w.DOCS, {"docs": {}, "missing": {}})):
        w.save_json(p(a.run, name), empty)
    print("\nSAY THIS TO PAUL FIRST, before anything else in your reply, in exactly these words:\n    %s.\n" % w.version_line())
    print("RUN STARTED  client: %s   bundle: %s\n" % (rj["client"], rj["bundle"]))
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


def guard(rj):
    if rj.get("program_fingerprint") and rj["program_fingerprint"] != w.program_fingerprint():
        w.die("REFUSED: the skill's programs, steps, rule pages or template changed while this run was in progress. The programs are run as they are. Start again in a new run folder.", 3)


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
        if a.missing not in roa.ALL_ROLES or len((a.said or "").strip()) < 5:
            w.die("REFUSED: --missing needs a known role (%s) and Paul's own words (--said)" % ", ".join(roa.ALL_ROLES))
        docs["missing"][a.missing] = a.said.strip()
        w.save_json(p(a.run, w.DOCS), docs)
        print("recorded: %s is not available (Paul: %s)" % (a.missing, a.said.strip()))
        return
    if a.role not in roa.ALL_ROLES:
        w.die("REFUSED: role must be one of %s" % ", ".join(roa.ALL_ROLES))
    if a.same_as:
        if a.role != "accepted_quote" or a.same_as != "fna_quote" or "fna_quote" not in docs["docs"]:
            w.die("REFUSED: --same-as is only for accepted_quote = fna_quote (the client accepted the FNA in full), after fna_quote is registered")
        docs["docs"][a.role] = {"same_as": a.same_as}
        docs["missing"].pop(a.role, None)
        w.save_json(p(a.run, w.DOCS), docs)
        print("recorded: the accepted quote is the FNA quote")
        return
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
    tf = os.path.join(w.DOCS_DIR, a.role + ".text.json")
    w.save_json(p(a.run, tf), rep)
    before = docs["docs"].get(a.role)
    docs["docs"][a.role] = {"file": dst, "text_file": tf, "name": os.path.basename(a.file), "route": a.route, "sha": w.sha256_file(p(a.run, dst)), "pages": rep["page_count"],
                            "image_only": rep["image_only"]}
    docs["missing"].pop(a.role, None)
    w.save_json(p(a.run, w.DOCS), docs)
    print("document registered: %s = %s (%d page(s)) via %s" % (a.role, os.path.basename(a.file), rep["page_count"], a.route))
    if rep["image_only"]:
        print("NOTE: page(s) %s have no readable text. View them as images yourself; figures on them cannot be checked by the program." % ", ".join(map(str, rep["image_only"])))
    if before and before["sha"] != docs["docs"][a.role]["sha"] and os.path.exists(p(a.run, w.ANSWERS)):
        print("A document changed: run answers again so every entry is re-checked against it.")


def _served_keys(run):
    docs = w.load_opt(p(run, w.DOCS), {"docs": {}})
    keys = []
    for role in roa.SERVED_ROLES:
        d = docs["docs"].get(role)
        if d and not d.get("same_as"):
            keys += [(role, n) for n in range(1, d["pages"] + 1)]
    return keys, docs


def cmd_read(a):
    rj = load_run(a.run)
    guard(rj)
    keys, docs = _served_keys(a.run)
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
    pg = rep["pages"][n - 1]
    print("-" * 24 + " %s - PAGE %d of %d " % (role, n, rep["page_count"]) + "-" * 24)
    if n in rep["image_only"]:
        print("THIS PAGE HAS NO READABLE TEXT. View it as an image yourself (for example: pdftoppm -f %d -l %d -png -r 80 %s page), then acknowledge it." % (n, n, p(a.run, docs["docs"][role]["file"])))
    else:
        print(pg["text"])
    print("-" * 78)
    print('Read it fully, then: python3 %s/run.py read %s --ack %s:%d --note "one line on what is on this page"' % (SCRIPTS, a.run, role, n))


def _load_answers_checked(run, rj, file=None):
    lists, bk = roa.template_lists(), roa.bank()
    docs, ev = verify.load_docs(run)
    a = w.load_json(file or p(run, w.ANSWERS), "the answers file")
    probs = roa.answers_problems(a, lists, bk, ev, w.parse_date(rj["today"]))
    if not probs and w.norm(a["client_name"]) != w.norm(rj["client"]):
        probs.append("client_name %r is not the client Paul named (%s)" % (a["client_name"], rj["client"]))
    if a.get("bundle") != rj.get("bundle"):
        probs.append("the bundle %r is not the one this run was started for (%s)" % (a.get("bundle"), rj.get("bundle")))
    return a, probs, lists, bk


def cmd_answers(a):
    rj = load_run(a.run)
    guard(rj)
    ans, probs, lists, bk = _load_answers_checked(a.run, rj, a.file)
    if probs:
        print("REFUSED (nothing saved):\n  - " + "\n  - ".join(probs))
        sys.exit(5)
    before = verify.sha_of(w.load_opt(p(a.run, w.ANSWERS), {}))
    w.save_json(p(a.run, w.ANSWERS), ans)
    rj = load_run(a.run)
    rj["bundle"] = ans["bundle"]
    save_run(a.run, rj)
    if before != verify.sha_of(ans):
        for f in (w.APPROVAL,):
            if os.path.exists(p(a.run, f)):
                os.remove(p(a.run, f))
        st = w.load_opt(p(a.run, w.STATE), {})
        st.pop("shown_sha", None)
        w.save_json(p(a.run, w.STATE), st)
        reopen(a.run, "answers")
    print("answers saved: a %s ROA for %s; every name, ID and figure was found in the documents' text." % (ans["bundle"], ans["client_name"]))
    extra = roa.not_in_lists(ans, lists)
    if extra:
        print("NOT IN THE TEMPLATE'S DROPDOWN LISTS (will be written as text; Paul is told in the confirmation table): " + "; ".join(extra))
    if ans["bundle"] == "risk":
        for k, (t, m, h) in roa.reasons_for(ans, bk).items():
            if m == "custom":
                print("CUSTOM reason text (not from the bank) for %s: it is marked as such for Paul." % roa.COVER_NAMES[k])


def cmd_show(a):
    rj = load_run(a.run)
    guard(rj)
    ans, probs, lists, bk = _load_answers_checked(a.run, rj)
    if probs:
        w.die("REFUSED: the answers are not valid yet: " + "; ".join(probs[:2]))
    rows = roa.table_rows(ans, bk)
    st = w.load_opt(p(a.run, w.STATE), {})
    st["shown_sha"] = verify.sha_of({"answers": ans, "table": rows})
    w.save_json(p(a.run, w.STATE), st)
    print("CONFIRMATION TABLE (question | answer | source):\n")
    for q, v, s in rows:
        print("- %s | %s | %s" % (q, v, s or ""))
    extra = roa.not_in_lists(ans, lists)
    if extra:
        print("\nNOT IN THE TEMPLATE'S DROPDOWN LISTS, written as text: " + "; ".join(extra))
    print("\nTHE ONE QUESTION TO PAUL (show the whole table in the reply, then ask exactly this):\n    Are these answers right, so that I build the %s ROA for %s?\n" % (ans["bundle"].title(), ans["client_name"]))
    print("When he says yes: python3 %s/run.py approve %s --said \"his exact words\"" % (SCRIPTS, a.run))


def cmd_approve(a):
    rj = load_run(a.run)
    guard(rj)
    ans, probs, lists, bk = _load_answers_checked(a.run, rj)
    if probs:
        w.die("REFUSED: the answers are not valid yet.")
    cur = verify.sha_of({"answers": ans, "table": roa.table_rows(ans, bk)})
    st = w.load_opt(p(a.run, w.STATE), {})
    if st.get("shown_sha") != cur:
        w.die("REFUSED: Paul has not been shown exactly these answers. Run show, put the table in the reply, and only then record his yes.")
    if len((a.said or "").strip()) < 3:
        w.die("REFUSED: record Paul's own words with --said.")
    w.save_json(p(a.run, w.APPROVAL), {"sha": cur, "said": a.said, "t": w.now()})
    print("Paul's yes recorded for exactly these answers.")


def cmd_email(a):
    rj = load_run(a.run)
    guard(rj)
    ans = w.load_opt(p(a.run, w.ANSWERS), None)
    if not ans:
        w.die("Enter the answers first (run.py answers).")
    if ans["bundle"] == "risk":
        print("A Risk ROA embeds no email: nothing to do. Run: done email")
        return
    if not a.file or not os.path.isfile(a.file):
        w.die("REFUSED: give --file (the one HTML page: the client's reply header and words, then the quoted proposal).")
    probs = embedpipe.tools_problems()
    if probs:
        w.die("REFUSED: " + "; ".join(probs) + ". This session cannot build a Retirement or Investment ROA.")
    rep = docread.read_text_file(a.file)
    text = rep["pages"][0]["text"]
    low, r = text.lower(), ans["reply_email"]
    first = low.find("from:")
    second = low.find("from:", first + 5) if first >= 0 else -1
    bad = []
    if first < 0 or r["from"].lower() not in low[first:first + 200]:
        bad.append("the page must OPEN with the reply's own header block (From: the client's address %s)" % r["from"])
    if w.norm(r["acceptance_text"]) not in w.norm(text):
        bad.append("the client's own acceptance wording is not in the page")
    if second >= 0 and low.find(r["from"].lower()) > second:
        bad.append("the client's reply must come BEFORE the quoted proposal's header")
    for lab in ("sent:", "subject:"):
        if lab not in low:
            bad.append("the header block must show %s" % lab)
    if bad:
        print("REFUSED:\n  - " + "\n  - ".join(bad))
        sys.exit(5)
    shutil.copyfile(a.file, p(a.run, w.EMAIL_HTML))
    st = w.load_opt(p(a.run, w.STATE), {})
    st["email"] = {"sha": w.sha256_file(p(a.run, w.EMAIL_HTML)), "base_pt": a.base_pt}
    w.save_json(p(a.run, w.STATE), st)
    reopen(a.run, "email")
    print("email page registered: it opens on the client's own reply, then the quoted proposal.")


def cmd_build(a):
    rj = load_run(a.run)
    guard(rj)
    probs = _checks(a.run, "answers", "confirm") + (_checks(a.run, "email") if _bundle(a.run) != "risk" else [])
    if probs:
        w.die("REFUSED: " + "; ".join(probs))
    ans = w.load_json(p(a.run, w.ANSWERS))
    bk = roa.bank()
    data = roa.assemble(ans, bk)
    w.save_json(p(a.run, w.ROA_DATA), data)
    out = p(a.run, w.OUT)
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        if f.endswith(".docx"):
            os.remove(os.path.join(out, f))
    name = roa.delivery_filename(ans)
    final = os.path.join(out, name)
    tmpd = tempfile.mkdtemp(prefix="roa_run_")
    base = os.path.join(tmpd, "base.docx")
    br.build_roa(w.TEMPLATE, base, data)
    emb = None
    if ans["bundle"] != "risk":
        st0 = w.load_opt(p(a.run, w.STATE), {})
        try:
            emb = embedpipe.run(p(a.run, w.EMAIL_HTML), p(a.run, "embed"), base, final, ans["bundle"], (st0.get("email") or {}).get("base_pt"))
        except Exception as e:
            w.die("STOP. The email embedding failed: %s" % e)
    else:
        shutil.copyfile(base, final)
    shutil.rmtree(tmpd, ignore_errors=True)
    st = w.load_opt(p(a.run, w.STATE), {})
    st["build"] = {"t": w.now(), "docx": name, "sha": w.sha256_file(final), "size": os.path.getsize(final), "data_sha": verify.sha_of(data), "embed": emb}
    st.pop("save", None)
    w.save_json(p(a.run, w.STATE), st)
    reopen(a.run, "build")
    print("BUILT %s (%d bytes) from the confirmed answers with the fixed scripts%s" % (final, st["build"]["size"], (", %d email page(s) embedded before '%s'" % (emb["pages"], emb["heading"])) if emb else ""))


def cmd_check(a):
    rj = load_run(a.run)
    guard(rj)
    R, rj2 = verify.run_checks(a.run, "pre")
    rows = [r for r in R.rows if r[3] in ("build", "docx")]
    if not rows:
        w.die("Build the ROA first (run.py build).")
    for mark, short, detail, _g in rows:
        print("%s %s" % (mark, short))
    st = w.load_opt(p(a.run, w.STATE), {})
    pages = p(a.run, os.path.join(w.OUT, "pages"))
    if a.no_render:
        print("\n(page images were not rendered: --no-render)")
    else:
        soffice = shutil.which("soffice") or shutil.which("libreoffice")
        if not soffice:
            print("\nNOTE: LibreOffice is not available, so no page images were made. View the .docx yourself before delivering.")
        else:
            os.makedirs(pages, exist_ok=True)
            tmpd = tempfile.mkdtemp(prefix="roa_render_")
            docx = p(a.run, os.path.join(w.OUT, st["build"]["docx"]))
            r = subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", tmpd, docx], capture_output=True, text=True, timeout=240)
            pdfs = [f for f in os.listdir(tmpd) if f.endswith(".pdf")]
            if pdfs:
                for f in os.listdir(pages):
                    os.remove(os.path.join(pages, f))
                subprocess.run(["pdftoppm", "-jpeg", "-r", "70", os.path.join(tmpd, pdfs[0]), os.path.join(pages, "page")], capture_output=True)
                print("\nPAGE IMAGES for your eyes: %s   (look at every page: filled fields black not grey, the embedded pages the same size as the ROA's own text, no border touching a footer)" % pages)
            else:
                print("\nNOTE: the page images could not be made (%s). View the .docx yourself." % (r.stderr or r.stdout)[-200:])
            shutil.rmtree(tmpd, ignore_errors=True)
    print("\nWhen every line above is a green tick and you have looked at the pages: run done check.")


def cmd_name(a):
    rj = load_run(a.run)
    guard(rj)
    st = w.load_opt(p(a.run, w.STATE), {})
    ans = w.load_opt(p(a.run, w.ANSWERS), None)
    if not st.get("build") or not ans:
        w.die("Build the ROA first (run.py build).")
    existing = [x.strip() for x in (a.existing or "").split(";") if x.strip()]
    name = roa.delivery_filename(ans)
    clash = w.norm(name) in {w.norm(e) for e in existing}
    if clash and len((a.overwrite_yes or "").strip()) < 3:
        print("STOP. A file named %r already exists in the client's folder. Never overwrite a compliance document silently: ask Paul. If he says to overwrite, run this again with --overwrite-yes \"his words\"." % name)
        sys.exit(5)
    st["save"] = {"name": name, "existing": existing, "existing_clash": clash, "overwrite": (a.overwrite_yes or "").strip() if clash else ""}
    w.save_json(p(a.run, w.STATE), st)
    path = p(a.run, os.path.join(w.OUT, name))
    print("SAVE THIS FILE: %s" % path)
    print("Name to use in the client's ROA & Bus ROA folder: %s" % name)
    print("Then record: run.py access ... --purpose save (computer, then Microsoft 365, then Zapier), run.py receipt save.folder <the folder> and save.listed_bytes <the size the folder listing shows> (%d bytes)" % os.path.getsize(path))


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
    x = sub.add_parser("start")
    x.add_argument("run")
    x.add_argument("--client", required=True)
    x.add_argument("--bundle", required=True, choices=roa.BUNDLES)
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
    x.add_argument("--same-as", dest="same_as")
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
    x = sub.add_parser("email")
    x.add_argument("run")
    x.add_argument("--file")
    x.add_argument("--base-pt", dest="base_pt", type=float)
    x.set_defaults(fn=cmd_email)
    x = sub.add_parser("check")
    x.add_argument("run")
    x.add_argument("--no-render", dest="no_render", action="store_true")
    x.set_defaults(fn=cmd_check)
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
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
