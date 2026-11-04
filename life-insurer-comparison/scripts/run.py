#!/usr/bin/env python3
"""The step driver of the life-insurer-comparison skill: shows ONE step at a time, refuses to skip, keeps the run on disk.

  run.py start <run> --client "First Surname"
  run.py next | status | preflight
  run.py access <run> --purpose locate|research|save --route device|m365|zapier|web|chrome --result found|failed [--note TEXT]
  run.py doc <run> --role ROLE [--label LABEL] --file FILE --route ROUTE [--url URL --fetched-at DD/MM/YYYY]       register a document
  run.py doc <run> --missing ROLE [--label LABEL] --said "Paul's words"                                           a document that does not exist or could not be found
  run.py insurers <run> --file insurers.json                       the insurer behind each quote or schedule (each needs its own guide in the research step)
  run.py read <run> [--ack KEY:PAGE --note TEXT]                   the documents' text, one page at a time
  run.py scope <run> [--file scope.json]                           without --file: the lines of the notes that mention each benefit category; with it: the scope, checked
  run.py answers <run> --file answers.json                         the figures and statements, each with its evidence
  run.py check <run>                                               the premium escalation worked out, the flags
  run.py show <run>                                                the confirmation table and the ONE question
  run.py approve <run> --said "Paul's exact words"
  run.py build <run>                                               build the letter and the text for the Outlook draft
  run.py name <run> --existing "a.html;b.html" [--overwrite-yes "Paul's words"]
  run.py draft <run> --file readback.json                          check the saved read-back of the Outlook draft
  run.py message <run> --used-today yes|no                         the exact Teams message and how to send it (only after the draft check)
  run.py messagecheck <run> --file readback.txt                    check the saved read-back of the posted Teams message
  run.py receipt <run> KEY VALUE
  run.py done <run> STEP                                           prove the step, then show the next one

Claude runs these programs as they are and never rewrites them during a run. Nothing here sends anything to anyone: the chat sends, after Paul's yes.
"""
import argparse
import os
import shutil
import sys

import docread
import lic as c
import licbuild as b
import verify
import wrlib as w

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
RULE = "=" * 78
ALL = ["read", "scope", "research", "answers", "check", "confirm", "build", "save", "draft", "message", "final"]
LATER = {"doc": ALL, "scope": ALL[2:], "answers": ALL[4:], "check": ALL[5:], "build": ALL[7:]}


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
    rows.append((all(os.path.exists(x) for x in (c.TEMPLATE, c.SETTINGS, c.WORDING, c.TERMS)), "the letter template, the wording, the scope word lists and the settings are in the skill"))
    try:
        with open(c.TEMPLATE, encoding="utf-8") as f:
            t = f.read()
        rows.append((t.count("[TITLE]") == 1 and t.count("[CONTENT]") == 1, "the template carries the two places the program fills"))
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
    "scope_ok": lambda run, rj: _checks(run, "scope"),
    "research_ok": lambda run, rj: _checks(run, "research"),
    "answers_ok": lambda run, rj: _checks(run, "answers"),
    "check_ok": lambda run, rj: _checks(run, "answers", "check"),
    "confirm_ok": lambda run, rj: _checks(run, "answers", "check", "confirm"),
    "build_ok": lambda run, rj: _checks(run, "answers", "check", "confirm", "build"),
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
        w.die("REFUSED: the skill's programs, steps, rule pages, template, wording or settings changed while this run was in progress. The programs are run as they are. Start again in a new run folder.", 3)


def today_of(rj):
    return w.parse_date(rj["today"])


def state_of(run):
    return w.load_opt(p(run, w.STATE), {})


def docs_of_run(run):
    return w.load_opt(p(run, w.DOCS), {"docs": {}, "missing": {}})


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
    os.makedirs(os.path.join(a.run, w.OUT), exist_ok=True)
    os.makedirs(os.path.join(a.run, w.DOCS_DIR), exist_ok=True)
    rj = {"skill": w.skill_name(), "created": w.now(), "skill_stamp": w.skill_stamp(), "steps": {}, "client": " ".join(parts), "today": w.today().strftime("%d/%m/%Y"),
          "program_fingerprint": w.program_fingerprint()}
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
    if a.route not in w.ROUTES_FOR[a.purpose]:
        w.die("REFUSED: for %s the routes are %s" % (a.purpose, ", ".join(w.ROUTES_FOR[a.purpose])))
    log = w.load_opt(p(a.run, w.ACCESS), [])
    log.append({"purpose": a.purpose, "route": a.route, "result": a.result, "note": a.note or "", "t": w.now()})
    w.save_json(p(a.run, w.ACCESS), log)
    print("access try recorded: %s %s %s (%d on record)" % (a.purpose, a.route, a.result, len(log)))


def _label_needed(role, label):
    if role in c.LABELLED and not (label or "").strip():
        w.die("REFUSED: --label is needed for a %s (the policy's or proposal's own name for a quote or schedule, the date for meeting notes, '<Insurer> - <title>' for a guide)" % role)
    if role not in c.LABELLED and label:
        w.die("REFUSED: a %s has no label" % role)


def cmd_doc(a):
    rj = load_run(a.run)
    guard(rj)
    docs = docs_of_run(a.run)
    st = state_of(a.run)
    if a.missing:
        if not c.can_be_missing(a.missing) or len((a.said or "").strip()) < 5:
            w.die("REFUSED: --missing is only for the meeting notes, the Fact Find Summary, the WR Overview or an insurer's guide that could not be found, with Paul's own words (--said). A quote or schedule can never be missing.")
        if a.missing == "guide":
            if (a.label or "").strip() not in [d["insurer"] for d in c.declared(st)]:
                w.die("REFUSED: for a guide --label is the INSURER's name as declared (run.py insurers first)")
            k = c.dkey("guide", a.label)
        else:
            _label_needed(a.missing, a.label)
            k = c.dkey(a.missing, a.label)
        docs["missing"][k] = a.said.strip()
        w.save_json(p(a.run, w.DOCS), docs)
        reopen(a.run, "doc")
        print("recorded: %s is not available (Paul: %s)" % (k, a.said.strip()))
        return
    if not c.valid_role(a.role):
        w.die("REFUSED: role must be one of %s" % ", ".join(c.ROLES))
    _label_needed(a.role, a.label)
    if not a.file or not os.path.isfile(a.file) or not a.route:
        w.die("REFUSED: give --file (an existing file) and --route")
    purpose = "research" if a.role == "guide" else "locate"
    if a.route not in w.ROUTES_FOR[purpose]:
        w.die("REFUSED: a %s comes by %s" % (a.role, " or ".join(w.ROUTES_FOR[purpose])))
    log = [e for e in w.load_opt(p(a.run, w.ACCESS), []) if e.get("purpose") == purpose]
    if not any(e["route"] == a.route and e["result"] == "found" for e in log):
        w.die("REFUSED: record the access try first: run.py access %s --purpose %s --route %s --result found" % (a.run, purpose, a.route))
    bad = verify.route_order_problems(log, w.ROUTES_FOR[purpose])
    if bad:
        w.die("REFUSED: the routes are tried in order (%s); %s was used before the earlier ones failed." % (", ".join(w.ROUTES_FOR[purpose]), ", ".join(bad)))
    if a.role == "guide":
        if not any(w.norm(a.label).startswith(w.norm(d["insurer"]) + " ") for d in c.declared(st)):
            w.die("REFUSED: declare the insurers first (run.py insurers). The guide's label starts with the insurer's name: '<Insurer> - <title>'. Declared: %s" % "; ".join(d["insurer"] for d in c.declared(st) or [{"insurer": "(none yet)"}]))
        fa = w.parse_date(a.fetched_at)
        if not (a.url or "").strip().lower().startswith(("http://", "https://")) or fa is None or fa > today_of(rj):
            w.die("REFUSED: a guide needs --url (where it came from) and --fetched-at (DD/MM/YYYY, not in the future)")
    if a.role in c.SIDE_ROLES and len(c.side_docs(docs)) >= c.limits()["sides_max"] and a.label.strip() not in c.side_docs(docs):
        w.die("REFUSED: at most %d policies or proposals are compared in one letter" % c.limits()["sides_max"])
    if a.role in c.SIDE_ROLES and a.label.strip() in c.side_docs(docs) and c.dkey(a.role, a.label) not in docs["docs"]:
        w.die("REFUSED: %r is already registered as the other kind of document (quote or schedule)" % a.label)
    key = c.dkey(a.role, a.label)
    ext = os.path.splitext(a.file)[1].lower() or ".pdf"
    dst = os.path.join(w.DOCS_DIR, key + ext)
    shutil.copyfile(a.file, p(a.run, dst))
    try:
        rep = docread.read_document(p(a.run, dst))
    except Exception as e:
        os.remove(p(a.run, dst))
        print("STOP. This file cannot be used: %s" % e)
        sys.exit(5)
    tf = os.path.join(w.DOCS_DIR, key + ".text.json")
    w.save_json(p(a.run, tf), rep)
    before = docs["docs"].get(key)
    docs["docs"][key] = {"role": a.role, "label": (a.label or "").strip() or None, "file": dst, "text_file": tf, "name": os.path.basename(a.file), "route": a.route, "sha": w.sha256_file(p(a.run, dst)),
                         "pages": rep["page_count"], "served": [pg["n"] for pg in rep["pages"]], "image_only": rep["image_only"], "url": (a.url or "").strip(), "fetched_at": (a.fetched_at or "").strip()}
    docs["missing"].pop(key, None)
    w.save_json(p(a.run, w.DOCS), docs)
    if a.role != "guide" or before:
        reopen(a.run, "doc")
    print("document registered: %s = %s (%d page(s)) via %s" % (key, os.path.basename(a.file), rep["page_count"], a.route))
    if rep["image_only"]:
        print("NOTE: page(s) %s have no readable text. View them as images yourself (render the page at high resolution, crop and zoom a garbled table); figures read from an image are marked image_read, "
              "shown to Paul and listed as only attested." % ", ".join(map(str, rep["image_only"])))
    if before and before["sha"] != docs["docs"][key]["sha"] and os.path.exists(p(a.run, w.ANSWERS)):
        print("A document changed: run answers again so every entry is re-checked against it.")


def cmd_insurers(a):
    rj = load_run(a.run)
    guard(rj)
    docs = docs_of_run(a.run)
    fl = w.load_json(a.file, "the insurers file")
    if not isinstance(fl, list) or not fl or any(not isinstance(x, dict) or set(x) != {"label", "insurer"} or not str(x["label"]).strip() or not str(x["insurer"]).strip() for x in fl):
        w.die('REFUSED: the insurers file is a list of {"label": "<the quote or schedule label>", "insurer": "<insurer name>"}, one per registered quote or schedule')
    sdocs = c.side_docs(docs)
    if sorted(x["label"] for x in fl) != sorted(sdocs):
        w.die("REFUSED: the insurers file must cover exactly the registered quotes and schedules, once each: %s" % "; ".join(sorted(sdocs)))
    ev = verify.load_docs(a.run)[1]
    for x in fl:
        e = ev.get(sdocs[x["label"]])
        if c.has(e) and w.norm(x["insurer"]) not in e.norm:
            w.die("REFUSED: the insurer %r is not in the text of %r" % (x["insurer"], x["label"]))
    st = state_of(a.run)
    before = c.declared(st)
    st["insurers"] = [{"label": x["label"].strip(), "insurer": x["insurer"].strip()} for x in fl]
    w.save_json(p(a.run, w.STATE), st)
    if before != st["insurers"]:
        reopen(a.run, "doc")
    names = sorted({x["insurer"] for x in st["insurers"]})
    print("insurers declared (%d). Each needs its OWN current guide in the research step (the insurer's technical guide, product guide or policy wording): fetch it (web, then Chrome; log every try with --purpose research), "
          "SAVE its text and register it:" % len(names))
    for n in names:
        print('  python3 %s/run.py doc %s --role guide --label "%s - <title of the guide>" --file <saved text> --route web|chrome --url <where it came from> --fetched-at DD/MM/YYYY' % (SCRIPTS, a.run, n))
    print('A guide that cannot be found: ask Paul, then run.py doc --missing guide --label "<Insurer>" --said "Paul\'s words".')


def cmd_read(a):
    rj = load_run(a.run)
    guard(rj)
    docs = docs_of_run(a.run)
    keys = verify.served_keys(docs, True)
    if not keys:
        w.die("No document is registered yet: run.py doc first.")
    st = state_of(a.run)
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
        print("All %d pages were read and acknowledged. Now run: python3 %s/run.py done %s read   (or research, if you are in that step)" % (len(keys), SCRIPTS, a.run))
        return
    key, n = nxt
    rep = w.load_json(p(a.run, docs["docs"][key]["text_file"]))
    pg = next(x for x in rep["pages"] if x["n"] == n)
    print("-" * 24 + " %s - PAGE %d of %d " % (key, n, rep["page_count"]) + "-" * 24)
    if n in rep["image_only"]:
        print("THIS PAGE HAS NO READABLE TEXT. View it as an image yourself (for example: pdftoppm -f %d -l %d -png -r 150 %s page), crop and enlarge a garbled table, then acknowledge it." % (n, n, p(a.run, docs["docs"][key]["file"])))
    else:
        print(pg["text"])
    print("-" * 78)
    print('Read it fully, then: python3 %s/run.py read %s --ack %s:%d --note "one line on what is on this page"' % (SCRIPTS, a.run, key, n))


def cmd_scope(a):
    rj = load_run(a.run)
    guard(rj)
    docs, ev = verify.load_docs(a.run)
    if not a.file:
        sug = c.scope_suggestions(docs, ev)
        print("LINES OF THE CLIENT'S OWN NOTES THAT MENTION EACH BENEFIT CATEGORY (found by the program; a hint for you, never the verdict):")
        for cat in c.CATEGORIES:
            print("\n%s (%d line(s))" % (c.terms()["category_names"][cat], len(sug[cat])))
            for k, ln, ex in sug[cat][:8]:
                print("  %s %s: %s" % ("[EXCLUSION LANGUAGE]" if ex else "                    ", k, ln[:160]))
        print("\nWrite scope.json in the layout the rules page describes: for EVERY category its status and a verbatim line of the notes as evidence (or Paul's own words if the notes are silent or conflict), "
              "the second life, the basis, the voice and the sections. Then run: python3 %s/run.py scope %s --file scope.json" % (SCRIPTS, a.run))
        return
    s = w.load_json(a.file, "the scope file")
    probs = c.scope_problems(s, ev, docs)
    if probs:
        print("REFUSED (nothing saved):\n  - " + "\n  - ".join(probs))
        sys.exit(5)
    before = verify.sha_of(w.load_opt(p(a.run, w.SCOPE), {}))
    w.save_json(p(a.run, w.SCOPE), s)
    if before != verify.sha_of(s):
        if os.path.exists(p(a.run, w.APPROVAL)):
            os.remove(p(a.run, w.APPROVAL))
        st = state_of(a.run)
        for k in ("shown_sha", "check"):
            st.pop(k, None)
        w.save_json(p(a.run, w.STATE), st)
        reopen(a.run, "scope")
    out = [c.terms()["category_names"][k] for k in c.CATEGORIES if s["categories"][k]["status"] == "out"]
    print("scope saved: in = %s; out = %s; second life: %s; basis: %s; voice: %s; sections: %s. NEXT: run.py done %s scope" % (
        ", ".join(c.terms()["category_names"][k] for k in c.CATEGORIES if s["categories"][k]["status"] == "in"), ", ".join(out) or "none", s["second_life"].get("name") or "none", s["basis"], s["voice"],
        ", ".join(c.canonical_sections(s)), a.run))
    for f_ in c.scope_flags(s, docs, ev):
        print("FLAG for Paul: " + f_)


def _load_answers_checked(run, rj, file=None):
    docs, ev = verify.load_docs(run)
    scope = w.load_opt(p(run, w.SCOPE), None)
    a = w.load_json(file or p(run, w.ANSWERS), "the answers file")
    if scope is None:
        w.die("REFUSED: the scope has not been saved yet (run.py scope).")
    return a, scope, c.answers_problems(a, scope, ev, docs, today_of(rj), rj["client"], state_of(run)), docs, ev


def cmd_answers(a):
    rj = load_run(a.run)
    guard(rj)
    ans, scope, probs, docs, ev = _load_answers_checked(a.run, rj, a.file)
    if probs:
        print("REFUSED (nothing saved):\n  - " + "\n  - ".join(probs))
        sys.exit(5)
    before = verify.sha_of(w.load_opt(p(a.run, w.ANSWERS), {}))
    w.save_json(p(a.run, w.ANSWERS), ans)
    if before != verify.sha_of(ans):
        if os.path.exists(p(a.run, w.APPROVAL)):
            os.remove(p(a.run, w.APPROVAL))
        st = state_of(a.run)
        for k in ("shown_sha", "check"):
            st.pop(k, None)
        w.save_json(p(a.run, w.STATE), st)
        reopen(a.run, "answers")
    print("answers saved: a comparison for %s (%s); every figure is in the evidence line it cites and every evidence line is in the document's text. NEXT: run.py done %s answers, then run.py check %s" %
          (ans["client_full_name"], " vs ".join(s["label"] for s in ans["sides"]), a.run, a.run))


def cmd_check(a):
    rj = load_run(a.run)
    guard(rj)
    probs = _checks(a.run, "answers")
    if probs:
        w.die("REFUSED: the answers are not valid yet: " + "; ".join(probs[:2]))
    ans = w.load_json(p(a.run, w.ANSWERS))
    scope = w.load_json(p(a.run, w.SCOPE))
    docs, ev = verify.load_docs(a.run)
    t = today_of(rj)
    summ = c.check_summary(ans, scope, t)
    st = state_of(a.run)
    st["check"] = {"t": w.now(), "sha": verify.sha_of(summ)}
    w.save_json(p(a.run, w.STATE), st)
    reopen(a.run, "check")
    print("THE PREMIUM ESCALATION (worked out by the program from the printed figures):")
    for s in ans["sides"]:
        v = summ["per_side"][s["label"]]
        if v["years"]:
            print("%s %s: %d years, average %s%% a year (%s); %s" % (verify.OK, s["label"], v["years"], v["avg"] or "-", v["mode"] or "-", "the current premium is year %d of the table" % v["anchor"] if v["anchor"] else "the current premium is not in the table"))
        else:
            print("%s %s: no projection table (its column shows 'not provided')" % (verify.BAD, s["label"]))
    for f_ in c.paul_flags(ans, scope, docs, ev, t):
        print("FLAG for Paul: " + f_)
    counts = summ["basis_counts"]
    print("Statements: %d from the policy documents, %d from the insurers' guides, %d inference(s) (shown as 'to be confirmed')." % (counts["client_document"], counts["insurer_guide"], counts["inference"]))
    print("\nNext: run.py done %s check" % a.run)


def cmd_show(a):
    rj = load_run(a.run)
    guard(rj)
    ans, scope, probs, docs, ev = _load_answers_checked(a.run, rj)
    if probs:
        w.die("REFUSED: the answers are not valid yet: " + "; ".join(probs[:2]))
    st = state_of(a.run)
    if not st.get("check") or st["check"]["sha"] != verify.sha_of(c.check_summary(ans, scope, today_of(rj))):
        w.die("REFUSED: run.py check first (the escalation has not been worked out for these answers).")
    rows = b.table_rows(ans, scope, docs, ev, today_of(rj))
    st["shown_sha"] = verify.confirm_sha(ans, scope, docs, ev, st, today_of(rj))
    w.save_json(p(a.run, w.STATE), st)
    print("CONFIRMATION TABLE (question | answer | source):\n")
    for q, v, s in rows:
        print("- %s | %s | %s" % (q, v.replace("\n", " / ") if len(v) < 80 else "\n" + v, s or ""))
    imgs = verify.image_figures(ans)
    if imgs:
        print("\nFIGURES READ FROM PAGE IMAGES (cannot be proved by the program; look at them): " + "; ".join(imgs))
    print("\nTHE ONE QUESTION TO PAUL (show the whole table in the reply, then ask exactly this):\n    Are these answers right, so that I build the comparison letter and the covering email for %s, save the letter, "
          "make the Outlook draft and then message Sitamah?\n" % ans["client_full_name"])
    print("When he says yes: python3 %s/run.py approve %s --said \"his exact words\"" % (SCRIPTS, a.run))


def cmd_approve(a):
    rj = load_run(a.run)
    guard(rj)
    ans, scope, probs, docs, ev = _load_answers_checked(a.run, rj)
    if probs:
        w.die("REFUSED: the answers are not valid yet.")
    st = state_of(a.run)
    cur = verify.confirm_sha(ans, scope, docs, ev, st, today_of(rj))
    if st.get("shown_sha") != cur:
        w.die("REFUSED: Paul has not been shown exactly these answers. Run show, put the table in the reply, and only then record his yes.")
    if len((a.said or "").strip()) < 3:
        w.die("REFUSED: record Paul's own words with --said.")
    w.save_json(p(a.run, w.APPROVAL), {"sha": cur, "said": a.said, "t": w.now()})
    print("Paul's yes recorded for exactly these answers.")


def cmd_build(a):
    rj = load_run(a.run)
    guard(rj)
    probs = _checks(a.run, "answers", "check", "confirm")
    if probs:
        w.die("REFUSED: " + "; ".join(probs))
    ans = w.load_json(p(a.run, w.ANSWERS))
    scope = w.load_json(p(a.run, w.SCOPE))
    docs = docs_of_run(a.run)
    t = today_of(rj)
    try:
        letter, body = b.build_all(ans, scope, docs, t)
    except (ValueError, KeyError) as e:
        w.die("STOP. The letter cannot be built: %s" % e, 5)
    res = b.html_problems(letter, body, ans, scope, docs, t)
    badr = [r for r in res if not r[0]]
    if badr:
        w.die("STOP. The program's own check of the built letter failed: %s" % "; ".join(r[1] + (" - " + r[2] if r[2] else "") for r in badr), 5)
    out = p(a.run, w.OUT)
    for f in os.listdir(out):
        if f.endswith(".html"):
            os.remove(os.path.join(out, f))
    name = c.file_name(ans, t)
    files = {"letter": os.path.join(out, name), "body": os.path.join(out, "draft_body.html")}
    for k, text in (("letter", letter), ("body", body)):
        with open(files[k], "w", encoding="utf-8", newline="") as f:
            f.write(text)
    st = state_of(a.run)
    st["build"] = {"t": w.now(), "date": t.strftime("%d/%m/%Y"), "name": name, "size": os.path.getsize(files["letter"]), "sha": {"letter": w.sha256_text(letter), "body": w.sha256_text(body)}}
    for k in ("save", "draft", "message"):
        st.pop(k, None)
    w.save_json(p(a.run, w.STATE), st)
    reopen(a.run, "build")
    print("BUILT from the confirmed answers and the fixed template (%d program checks passed):" % len(res))
    print("  the comparison letter (send it to Paul in the chat as a file, and SAVE it): %s" % files["letter"])
    print("  the text for the Outlook draft (HTML body):                                   %s" % files["body"])
    print("  subject (character for character): %s" % c.subject(ans))
    print("  To: %s   Cc: %s <%s>" % (ans["client_email"], c.CC_NAME, c.CC_EMAIL))


def cmd_name(a):
    rj = load_run(a.run)
    guard(rj)
    st = state_of(a.run)
    if not st.get("build"):
        w.die("Build the letter first (run.py build).")
    existing = [x.strip() for x in (a.existing or "").split(";") if x.strip()]
    name = st["build"]["name"]
    clash = w.norm(name) in {w.norm(e) for e in existing}
    if clash and len((a.overwrite_yes or "").strip()) < 3:
        print("STOP. A file named %r already exists in the client's folder. Ask Paul. If he says to overwrite, run this again with --overwrite-yes \"his words\"." % name)
        sys.exit(5)
    st["save"] = {"name": name, "existing": existing, "existing_clash": clash, "overwrite": (a.overwrite_yes or "").strip() if clash else ""}
    w.save_json(p(a.run, w.STATE), st)
    path = p(a.run, os.path.join(w.OUT, name))
    print("SAVE THIS FILE: %s" % path)
    print("Name to use in the client's Comparative Quotes folder: %s   (%d bytes)" % (name, os.path.getsize(path)))
    print("Then record: run.py access ... --purpose save (computer, then Microsoft 365, then Zapier), run.py receipt save.folder <the folder> and save.listed_bytes <the size the listing shows for the html>")


def cmd_receipt(a):
    rj = load_run(a.run)
    guard(rj)
    rc = w.load_opt(p(a.run, w.RECEIPT), {})
    rc[a.key] = a.value
    w.save_json(p(a.run, w.RECEIPT), rc)
    print("receipt recorded: %s = %s" % (a.key, a.value))


def _readback(path):
    if not path or not os.path.isfile(path):
        w.die("REFUSED: give --file (the saved read-back).")
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def cmd_draft(a):
    rj = load_run(a.run)
    guard(rj)
    ans = w.load_opt(p(a.run, w.ANSWERS), None)
    scope = w.load_opt(p(a.run, w.SCOPE), None)
    st = state_of(a.run)
    if not ans or not st.get("build") or not st.get("save"):
        w.die("REFUSED: build the letter and record the save first.")
    docs = docs_of_run(a.run)
    text = _readback(a.file)
    dst = p(a.run, os.path.join(w.OUT, "draft_readback.txt"))
    with open(dst, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    res = b.draft_problems(text, ans, scope, docs, today_of(rj))
    for ok, short in res:
        print("%s %s" % (verify.OK if ok else verify.BAD, short))
    good = all(ok for ok, _ in res)
    st["draft"] = {"t": w.now(), "sha": w.sha256_file(dst), "ok": good}
    st.pop("message", None)
    w.save_json(p(a.run, w.STATE), st)
    if not good:
        print("\nThe draft is NOT right. Fix it (never send it), read it back again and run this again. Do not message Sitamah.")
        sys.exit(5)
    print("\nThe draft passed. Record how it was made: run.py receipt %s draft.created_with outlook_create_draft" % a.run)


def cmd_message(a):
    rj = load_run(a.run)
    guard(rj)
    ans = w.load_opt(p(a.run, w.ANSWERS), None)
    scope = w.load_opt(p(a.run, w.SCOPE), None)
    st = state_of(a.run)
    probs = _checks(a.run, "answers", "check", "confirm", "build", "save", "draft")
    if probs or not (st.get("draft") or {}).get("ok"):
        w.die("REFUSED: Sitamah is messaged only after Paul's yes and a checked draft: " + ("; ".join(probs[:3]) if probs else "the draft check has not passed"))
    docs = docs_of_run(a.run)
    clock = w.now_sast()
    greeting = c.greeting_for(clock, a.used_today == "yes")
    text = b.teams_text(ans, scope, docs, greeting, st["build"]["name"])
    st["message"] = {"t": w.now(), "greeting": greeting, "used_today": a.used_today, "clock": clock.strftime("%H:%M"), "text_sha": w.sha256_text(text)}
    w.save_json(p(a.run, w.STATE), st)
    print("TEAMS MESSAGE (send it through Zapier, never through Chrome or the Teams tool that lacks the scope):\n")
    print(text)
    print("\nHOW: Zapier list_dynamic_enum_values (tool_name microsoft_teams_send_chat_message, property_name chat, search \"Sitamah Nathoo\") and take the 1:1 chat:\n  %s\n  (label %s) - never a meeting chat." % (c.SITAMAH_CHAT, c.CHAT_LABEL))
    print("Then microsoft_teams_send_chat_message with that chat, format \"markdown\" and content = the text above (an output_hint is required). Read the posted message back with read_resource, save it to a file,")
    print("record: run.py receipt %s message.chat <the chat value used>   run.py receipt %s message.format markdown   then: run.py messagecheck %s --file <the saved read-back>" % (a.run, a.run, a.run))


def cmd_messagecheck(a):
    rj = load_run(a.run)
    guard(rj)
    ans = w.load_opt(p(a.run, w.ANSWERS), None)
    scope = w.load_opt(p(a.run, w.SCOPE), None)
    st = state_of(a.run)
    if not st.get("message"):
        w.die("REFUSED: run.py message first (it builds and shows the message; nothing is posted before that).")
    docs = docs_of_run(a.run)
    text = _readback(a.file)
    dst = p(a.run, os.path.join(w.OUT, "message_readback.txt"))
    with open(dst, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    res = b.message_problems(text, ans, scope, docs, st["message"]["greeting"], st["build"]["name"])
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
    for name, fn in (("next", cmd_next), ("status", cmd_status), ("show", cmd_show), ("build", cmd_build), ("check", cmd_check)):
        x = sub.add_parser(name)
        x.add_argument("run")
        x.set_defaults(fn=fn)
    x = sub.add_parser("done")
    x.add_argument("run")
    x.add_argument("step")
    x.set_defaults(fn=cmd_done)
    x = sub.add_parser("access")
    x.add_argument("run")
    x.add_argument("--purpose", required=True, choices=("locate", "research", "save"))
    x.add_argument("--route", required=True, choices=w.ROUTES + w.FACT_ROUTES)
    x.add_argument("--result", required=True, choices=("found", "failed"))
    x.add_argument("--note")
    x.set_defaults(fn=cmd_access)
    x = sub.add_parser("doc")
    x.add_argument("run")
    x.add_argument("--role")
    x.add_argument("--label")
    x.add_argument("--file")
    x.add_argument("--route", choices=w.ROUTES + w.FACT_ROUTES)
    x.add_argument("--url")
    x.add_argument("--fetched-at", dest="fetched_at")
    x.add_argument("--missing")
    x.add_argument("--said")
    x.set_defaults(fn=cmd_doc)
    x = sub.add_parser("insurers")
    x.add_argument("run")
    x.add_argument("--file", required=True)
    x.set_defaults(fn=cmd_insurers)
    x = sub.add_parser("read")
    x.add_argument("run")
    x.add_argument("--ack")
    x.add_argument("--note")
    x.set_defaults(fn=cmd_read)
    x = sub.add_parser("scope")
    x.add_argument("run")
    x.add_argument("--file")
    x.set_defaults(fn=cmd_scope)
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
