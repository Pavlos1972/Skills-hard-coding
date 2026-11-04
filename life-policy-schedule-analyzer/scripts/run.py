#!/usr/bin/env python3
"""The step driver of the life-policy-schedule-analyzer skill: shows ONE step at a time, refuses to skip, keeps the run on disk.

  run.py start <run> --client "First Surname"
  run.py next | status | preflight
  run.py access <run> --purpose locate|research|save --route device|m365|zapier|web|chrome --result found|failed [--note TEXT]
  run.py doc <run> --role ROLE [--label LABEL] --file FILE --route ROUTE [--url URL --fetched-at DD/MM/YYYY]      register a document
  run.py doc <run> --missing ROLE [--label LABEL] --said "Paul's words"                                          a document that does not exist or could not be found
  run.py insurers <run> --file insurers.json                       the insurer behind each schedule, quote and proposed quote
  run.py read <run> [--ack KEY:PAGE --note TEXT]                   the documents' text, one page at a time
  run.py analysis <run> --file analysis.json                       the analysis, every figure with its evidence line
  run.py check <run>                                               the premium tables, the findings, the flags
  run.py show <run>                                                the confirmation table and the ONE question
  run.py approve <run> --said "Paul's exact words"
  run.py build <run>                                               draw the internal report(s) and the client slides
  run.py name <run> --existing "a.pdf;b.pdf" [--overwrite-yes "Paul's words"]
  run.py receipt <run> KEY VALUE
  run.py done <run> STEP                                           prove the step, then show the next one

Claude runs these programs as they are and never rewrites them during a run. Nothing here sends anything to anyone.
"""
import argparse
import os
import shutil
import sys

import docread
import lpa as c
import lpapdf as b
import verify
import wrlib as w

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
RULE = "=" * 78
ALL = ["read", "research", "analysis", "check", "confirm", "build", "save", "final"]
LATER = {"doc": ALL, "analysis": ALL[3:], "check": ALL[4:], "build": ALL[6:]}


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
    for mod in ("pdfplumber", "reportlab"):
        try:
            __import__(mod)
            rows.append((True, "python module %s is available" % mod))
        except ImportError:
            rows.append((False, "python module %s is NOT available (try: pip install %s)" % (mod, mod)))
    rows.append((all(os.path.exists(x) for x in (c.SETTINGS, c.WORDING, c.SLIDE_WORDS)), "the settings, the wording and the slide word list are in the skill"))
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
    "research_ok": lambda run, rj: _checks(run, "research"),
    "analysis_ok": lambda run, rj: _checks(run, "analysis"),
    "check_ok": lambda run, rj: _checks(run, "analysis", "check"),
    "confirm_ok": lambda run, rj: _checks(run, "analysis", "check", "confirm"),
    "build_ok": lambda run, rj: _checks(run, "analysis", "check", "confirm", "build"),
    "save_ok": lambda run, rj: _checks(run, "build", "save"),
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
        sp = p(a.run, os.path.join(w.OUT, "chat_summary.txt"))
        if os.path.exists(sp):
            print("\nTHE TABULATED CHAT SUMMARY (put it in your reply, before the audit, as it is):\n")
            with open(sp, encoding="utf-8") as f:
                print(f.read())
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
            w.die("REFUSED: --missing is only for the Fact Find Summary, meeting notes, the proposed insurer's payback document, or an insurer's guide or independent source that could not be found, with Paul's own words (--said). A schedule, a quote or the proposed quote can never be missing.")
        if a.missing in ("guide", "source"):
            if (a.label or "").strip() not in [d["insurer"] for d in c.declared(st)]:
                w.die("REFUSED: for a guide or source --label is the INSURER's name as declared (run.py insurers first)")
            k = c.dkey(a.missing, a.label)
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
    purpose = "research" if a.role in ("guide", "source") else "locate"
    if a.route not in w.ROUTES_FOR[purpose]:
        w.die("REFUSED: a %s comes by %s" % (a.role, " or ".join(w.ROUTES_FOR[purpose])))
    log = [e for e in w.load_opt(p(a.run, w.ACCESS), []) if e.get("purpose") == purpose]
    if not any(e["route"] == a.route and e["result"] == "found" for e in log):
        w.die("REFUSED: record the access try first: run.py access %s --purpose %s --route %s --result found" % (a.run, purpose, a.route))
    bad = verify.route_order_problems(log, w.ROUTES_FOR[purpose])
    if bad:
        w.die("REFUSED: the routes are tried in order (%s); %s was used before the earlier ones failed." % (", ".join(w.ROUTES_FOR[purpose]), ", ".join(bad)))
    if a.role in ("guide", "source"):
        if not any(w.norm(a.label).startswith(w.norm(d["insurer"]) + " ") for d in c.declared(st)):
            w.die("REFUSED: declare the insurers first (run.py insurers). The label starts with the insurer's name: '<Insurer> - <title>'. Declared: %s" % "; ".join(d["insurer"] for d in c.declared(st) or [{"insurer": "(none yet)"}]))
        fa = w.parse_date(a.fetched_at)
        if not (a.url or "").strip().lower().startswith(("http://", "https://")) or fa is None or fa > today_of(rj):
            w.die("REFUSED: a product source needs --url (where it came from) and --fetched-at (DD/MM/YYYY, not in the future)")
    if a.role == "proposed" and c.docs_of(docs, "proposed") and c.dkey("proposed", a.label) not in docs["docs"]:
        w.die("REFUSED: only one proposed quote is used for Report 2")
    if a.role == "payback_doc" and c.docs_of(docs, "payback_doc") and c.dkey("payback_doc", a.label) not in docs["docs"]:
        w.die("REFUSED: only one payback document (the proposed insurer's own) is used")
    if a.role in c.POLICY_ROLES and a.label.strip() in c.policy_docs(docs) and c.dkey(a.role, a.label) not in docs["docs"]:
        w.die("REFUSED: %r is already registered as the other kind of document (schedule or quote)" % a.label)
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
    if a.role not in ("guide", "source") or before:
        reopen(a.run, "doc")
    print("document registered: %s = %s (%d page(s)) via %s" % (key, os.path.basename(a.file), rep["page_count"], a.route))
    if rep["image_only"]:
        print("NOTE: page(s) %s have no readable text. View them as images yourself (render the page at high resolution, crop and zoom a garbled table); figures read from an image are marked image_read, "
              "shown to Paul and listed as only attested." % ", ".join(map(str, rep["image_only"])))
    if before and before["sha"] != docs["docs"][key]["sha"] and os.path.exists(p(a.run, w.ANSWERS)):
        print("A document changed: run analysis again so every entry is re-checked against it.")


def cmd_insurers(a):
    rj = load_run(a.run)
    guard(rj)
    docs = docs_of_run(a.run)
    fl = w.load_json(a.file, "the insurers file")
    if not isinstance(fl, list) or not fl or any(not isinstance(x, dict) or set(x) != {"label", "insurer"} or not str(x["label"]).strip() or not str(x["insurer"]).strip() for x in fl):
        w.die('REFUSED: the insurers file is a list of {"label": "<the schedule, quote or proposed quote label>", "insurer": "<insurer name>"}, one per registered schedule, quote and proposed quote')
    need = dict(c.policy_docs(docs))
    need.update(c.docs_of(docs, "proposed"))
    if sorted(x["label"] for x in fl) != sorted(need):
        w.die("REFUSED: the insurers file must cover exactly the registered schedules, quotes and the proposed quote, once each: %s" % "; ".join(sorted(need)))
    ev = verify.load_docs(a.run)[1]
    for x in fl:
        e = ev.get(need[x["label"]])
        if c.has(e) and w.norm(x["insurer"]) not in e.norm:
            w.die("REFUSED: the insurer %r is not in the text of %r" % (x["insurer"], x["label"]))
    st = state_of(a.run)
    before = c.declared(st)
    st["insurers"] = [{"label": x["label"].strip(), "insurer": x["insurer"].strip()} for x in fl]
    w.save_json(p(a.run, w.STATE), st)
    if before != st["insurers"]:
        reopen(a.run, "doc")
    names = sorted({x["insurer"] for x in st["insurers"]})
    print("insurers declared (%d). In the research step each needs its OWN guide (the insurer's technical guide, product guide or policy wording) and, where one exists, an INDEPENDENT source: fetch them "
          "(web, then Chrome; log every try with --purpose research), SAVE the text and register it:" % len(names))
    for n in names:
        print('  python3 %s/run.py doc %s --role guide --label "%s - <title>" --file <saved text> --route web|chrome --url <where it came from> --fetched-at DD/MM/YYYY' % (SCRIPTS, a.run, n))
        print('  python3 %s/run.py doc %s --role source --label "%s - <title>" --file <saved text> --route web|chrome --url <where it came from> --fetched-at DD/MM/YYYY' % (SCRIPTS, a.run, n))
    print('A source that cannot be found: ask Paul, then run.py doc --missing guide|source --label "<Insurer>" --said "Paul\'s words". Statements with one source are labelled SINGLE SOURCE in the report.')


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


def _load_analysis_checked(run, rj, file=None):
    docs, ev = verify.load_docs(run)
    raw = w.load_json(file or p(run, w.ANSWERS), "the analysis file")
    ann, probs = c.annotate(raw, ev, docs, today_of(rj), rj["client"], state_of(run))
    return raw, ann, probs, docs, ev


def cmd_analysis(a):
    rj = load_run(a.run)
    guard(rj)
    raw, ann, probs, docs, ev = _load_analysis_checked(a.run, rj, a.file)
    if probs:
        print("REFUSED (nothing saved):\n  - " + "\n  - ".join(probs))
        sys.exit(5)
    before = verify.sha_of(w.load_opt(p(a.run, w.ANSWERS), {}))
    w.save_json(p(a.run, w.ANSWERS), raw)
    if before != verify.sha_of(raw):
        if os.path.exists(p(a.run, w.APPROVAL)):
            os.remove(p(a.run, w.APPROVAL))
        st = state_of(a.run)
        for k in ("shown_sha", "check"):
            st.pop(k, None)
        w.save_json(p(a.run, w.STATE), st)
        reopen(a.run, "analysis")
    print("analysis saved: %d polic%s for %s; every client figure is in the evidence line it cites and every evidence line is in the document's text. NEXT: run.py done %s analysis, then run.py check %s" %
          (len(ann["policies"]), "y" if len(ann["policies"]) == 1 else "ies", ann["client_full_name"], a.run, a.run))


def cmd_check(a):
    rj = load_run(a.run)
    guard(rj)
    probs = _checks(a.run, "analysis")
    if probs:
        w.die("REFUSED: the analysis is not valid yet: " + "; ".join(probs[:2]))
    raw, ann, _pr, docs, ev = _load_analysis_checked(a.run, rj)
    t = today_of(rj)
    summ = c.check_summary(ann, t)
    st = state_of(a.run)
    st["check"] = {"t": w.now(), "sha": verify.sha_of(summ)}
    w.save_json(p(a.run, w.STATE), st)
    reopen(a.run, "check")
    print("WHAT THE PROGRAM WORKED OUT:")
    for p_ in ann["policies"]:
        v = summ["per_policy"][p_["label"]]
        acts = len([f for f in v["findings"] if f[1] == "action"])
        print("%s %s: premium table %s (%d rows); %d Action Required and %d For Your Awareness finding(s); benchmark %s" % (verify.OK if v["mode"] != "none" else verify.BAD, p_["label"], v["mode"], v["years"], acts, len(v["findings"]) - acts,
                                                                                                                       ", ".join("%s: %s" % kv for kv in v["benchmark"].items()) or "none"))
    for f_ in c.paul_flags(ann, docs, ev, t):
        print("FLAG for Paul: " + f_)
    cnt = summ["counts"]
    print("Statements: %d from the documents, %d verified by two product sources, %d on a SINGLE source, %d inference(s), %d on what the document does not say." %
          (cnt.get("document", 0), cnt.get("product_verified", 0), cnt.get("product_single", 0), cnt.get("inference", 0), cnt.get("absent", 0)))
    print("\nNext: run.py done %s check" % a.run)


def cmd_show(a):
    rj = load_run(a.run)
    guard(rj)
    raw, ann, probs, docs, ev = _load_analysis_checked(a.run, rj)
    if probs:
        w.die("REFUSED: the analysis is not valid yet: " + "; ".join(probs[:2]))
    st = state_of(a.run)
    if not st.get("check") or st["check"]["sha"] != verify.sha_of(c.check_summary(ann, today_of(rj))):
        w.die("REFUSED: run.py check first (the premium tables and findings have not been worked out for this analysis).")
    rows = b.table_rows(ann, docs, ev, today_of(rj))
    st["shown_sha"] = verify.confirm_sha(raw, docs, ev, st, today_of(rj))
    w.save_json(p(a.run, w.STATE), st)
    print("CONFIRMATION TABLE (question | answer | source):\n")
    for q, v, s in rows:
        print("- %s | %s | %s" % (q, v.replace("\n", " / ") if len(v) < 90 else "\n" + v, s or ""))
    imgs = verify.image_figures(raw)
    if imgs:
        print("\nFIGURES READ FROM PAGE IMAGES (cannot be proved by the program; look at them): " + "; ".join(imgs))
    print("\nTHE ONE QUESTION TO PAUL (show the whole table in the reply, then ask exactly this):\n    Are these right, so that I draw the internal report(s)%s for %s, save them in Analysis & Comparison Reports and give you the summary?\n" %
          (" and the client slides" if True else "", ann["client_full_name"]))
    print("When he says yes: python3 %s/run.py approve %s --said \"his exact words\"" % (SCRIPTS, a.run))


def cmd_approve(a):
    rj = load_run(a.run)
    guard(rj)
    raw, ann, probs, docs, ev = _load_analysis_checked(a.run, rj)
    if probs:
        w.die("REFUSED: the analysis is not valid yet.")
    st = state_of(a.run)
    cur = verify.confirm_sha(raw, docs, ev, st, today_of(rj))
    if st.get("shown_sha") != cur:
        w.die("REFUSED: Paul has not been shown exactly this analysis. Run show, put the table in the reply, and only then record his yes.")
    if len((a.said or "").strip()) < 3:
        w.die("REFUSED: record Paul's own words with --said.")
    w.save_json(p(a.run, w.APPROVAL), {"sha": cur, "said": a.said, "t": w.now()})
    print("Paul's yes recorded for exactly this analysis.")


def cmd_build(a):
    rj = load_run(a.run)
    guard(rj)
    probs = _checks(a.run, "analysis", "check", "confirm")
    if probs:
        w.die("REFUSED: " + "; ".join(probs))
    raw, ann, _pr, docs, ev = _load_analysis_checked(a.run, rj)
    t = today_of(rj)
    out = p(a.run, w.OUT)
    for f in os.listdir(out):
        if f.endswith(".pdf"):
            os.remove(os.path.join(out, f))
    made, bad = {}, []
    try:
        for pol in ann["policies"]:
            name = c.internal_name(ann, pol, t)
            b.build_internal(ann, pol, docs, ev, t, os.path.join(out, name))
            made[name] = ("internal", pol["label"])
        for kind, ins, name in c.slide_names(ann, t):
            b.build_slides(ann, kind, ins, docs, ev, t, os.path.join(out, name))
            made[name] = (kind, ins)
    except b.SlideOverflow as e:
        w.die("STOP. A slide cannot be drawn: %s. Shorten that text in the analysis (the limits are in assets/settings.json) and run analysis again." % e, 5)
    results = []
    for name, (kind, who) in made.items():
        path = os.path.join(out, name)
        if kind == "internal":
            res = b.internal_problems(path, ann, next(x for x in ann["policies"] if x["label"] == who), docs, t)
        else:
            res = b.slides_problems(path, ann, kind, who, docs, t)
        results.append((name, res))
        bad += ["%s: %s" % (name, s) for ok, s in res if not ok]
    if bad:
        w.die("STOP. The program's own check of the drawn PDFs failed: %s" % "; ".join(bad[:4]), 5)
    st = state_of(a.run)
    summary = b.chat_summary(ann, t, "%s > %s" % (ann["plan_folder"], c.settings()["folder_name"]))
    with open(os.path.join(out, "chat_summary.txt"), "w", encoding="utf-8", newline="") as f:
        f.write(summary)
    st["build"] = {"t": w.now(), "date": t.strftime("%d/%m/%Y"), "files": {n: {"sha": w.sha256_file(os.path.join(out, n)), "size": os.path.getsize(os.path.join(out, n)), "kind": k, "who": who} for n, (k, who) in made.items()}}
    for k in ("save",):
        st.pop(k, None)
    w.save_json(p(a.run, w.STATE), st)
    reopen(a.run, "build")
    print("BUILT from the confirmed analysis (%d program checks passed on %d PDF(s)):" % (sum(len(r) for _n, r in results), len(results)))
    for n, (k, who) in made.items():
        print("  %-9s %s   (%d bytes)" % ("internal" if k == "internal" else k, os.path.join(out, n), os.path.getsize(os.path.join(out, n))))
    print("Present each PDF to Paul in the chat as a file, then SAVE them all in the client's Analysis & Comparison Reports folder (next step).")


def cmd_name(a):
    rj = load_run(a.run)
    guard(rj)
    st = state_of(a.run)
    if not st.get("build"):
        w.die("Build the PDFs first (run.py build).")
    existing = [x.strip() for x in (a.existing or "").split(";") if x.strip()]
    names = sorted(st["build"]["files"])
    clash = [n for n in names if w.norm(n) in {w.norm(e) for e in existing}]
    if clash and len((a.overwrite_yes or "").strip()) < 3:
        print("STOP. File(s) with the same name already exist in the client's folder: %s. Ask Paul. If he says to overwrite, run this again with --overwrite-yes \"his words\"." % "; ".join(clash))
        sys.exit(5)
    st["save"] = {"names": names, "existing": existing, "existing_clash": clash, "overwrite": (a.overwrite_yes or "").strip() if clash else ""}
    w.save_json(p(a.run, w.STATE), st)
    print("SAVE THESE FILES, straight into the client's Analysis & Comparison Reports folder (create it, and tell Paul, only if it does not exist):")
    for n in names:
        print("  %s   (%d bytes)" % (os.path.join(p(a.run, w.OUT), n), st["build"]["files"][n]["size"]))
    print("Then record: run.py access ... --purpose save (computer, then Microsoft 365, then Zapier), run.py receipt save.folder <the folder> and run.py receipt save.listed \"name=bytes;name=bytes\" (the sizes the listing shows)")


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
    x = sub.add_parser("analysis")
    x.add_argument("run")
    x.add_argument("--file", required=True)
    x.set_defaults(fn=cmd_analysis)
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
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
