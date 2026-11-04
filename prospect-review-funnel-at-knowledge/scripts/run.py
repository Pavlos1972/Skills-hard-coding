#!/usr/bin/env python3
"""The step driver of the prospect-review-funnel-at-knowledge: shows ONE step at a time, refuses to skip, keeps the run on disk.

  run.py start <run> --kind question|move|build|test|docs|review --request "Paul's words"
  run.py next | status | preflight | info
  run.py access <run> --purpose ROLE|other --route device|m365|zapier --result found|failed [--note TEXT]
  run.py doc <run> --role ROLE --file FILE --route device|m365|zapier|pasted --modified TIME     register a source document
  run.py stages <run> --codes A6d,A12 | --general "why no stage"                               name the stages the work touches
  run.py read <run> [--ack N --note TEXT]                                                     the pages for this work, in order
  run.py evidence <run> --stage CODE --doc ROLE --line "a line exactly as written"             prove the stage was read in the document
  run.py answer <run> --file FILE                                                             a question or a move: check the answer
  run.py plan <run> --file plan.json                                                          check the plan for AdviceTech or document work
  run.py confirm <run>                                                                        the table and ONE question for Paul
  run.py approve <run> --said "Paul's words"
  run.py changed <run> --role ROLE --modified TIME [--note TEXT]                              a document was changed (documents first)
  run.py result <run> --key checklist:233 --lines N --ok yes|no [--note TEXT]                 the read-back of one AdviceTech object
  run.py done <run> STEP                                                                      prove the step, then show the next one

Nothing in these programs changes a document or AdviceTech: the chat does, after Paul's yes, with the AdviceTech skill's methods.
Claude runs these programs as they are and never rewrites them during a run.
"""
import argparse
import os
import shutil
import sys

import doctext
import engine as eng
import funnel as F
import wrlib as w

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
RULE = "=" * 78


def p(run, name):
    return os.path.join(run, name)


def all_steps():
    return w.load_json(os.path.join(w.SKILL_DIR, "steps.json"))["steps"]


def steps(rj):
    ids = eng.steps_for(rj["kind"])
    by = {s["id"]: s for s in all_steps()}
    return [by[i] for i in ids]


def load_run(run):
    path = p(run, w.RUN)
    if not os.path.exists(path):
        w.die('This is not a run folder (no %s). Start one with: python3 %s/run.py start <run folder> --kind question --request "..."' % (w.RUN, SCRIPTS), 2)
    return w.load_json(path)


def save_run(run, rj):
    w.save_json(p(run, w.RUN), rj)


def read_ref(name):
    with open(os.path.join(w.SKILL_DIR, "references", name), encoding="utf-8") as f:
        return F.expand(f.read())


def expand(text, run):
    return text.replace("{scripts}", SCRIPTS).replace("{run}", run).replace("{folder}", F.status()["folder"])


def current_step(rj):
    for s in steps(rj):
        if rj["steps"].get(s["id"], {}).get("state") != "done":
            return s
    return None


def show_step(run, rj, step):
    plist = steps(rj)
    n = [s["id"] for s in plist].index(step["id"]) + 1
    print(RULE)
    print("STEP %d of %d: %s        [%s]" % (n, len(plist), step["title"], step["id"]))
    print(RULE)
    for line in step["do"]:
        print(expand(line, run))
    if step["id"] == "locate":
        cfg = eng.kind_cfg(rj["kind"])
        by = {d["role"]: d for d in F.status()["documents"]}
        print("\nDOCUMENTS THIS WORK NEEDS:")
        for r in cfg["roles"]:
            print("  - %s: %s" % (r, by[r]["name"]))
        print("Others you register (for example when a plan changes them): " + ", ".join("%s (%s)" % (r, by[r]["name"]) for r in F.ROLES if r not in cfg["roles"]))
    if step["id"] == "read":
        c = eng.compute(run)
        print("\nPAGES FOR THIS WORK, IN ORDER: " + ", ".join(c["pages"]))
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
        rp = F.route_problems()
        ns, nr, nu = F.stats()
        rows.append((not rp, "the stage routes are consistent (%d stages, %d routes)" % (ns, nr) if not rp else "the stage routes have a problem: %s" % rp[0]))
        pp = F.pages_problems()
        rows.append((not pp, "the pages agree with the data" if not pp else "a page has a problem: %s" % pp[0]))
        missing = [pg for k in F.settings()["kinds"].values() for pg in k["pages"] if pg not in F.page_names()]
        rows.append((not missing, "every page named in the settings exists" if not missing else "missing pages: %s" % ", ".join(sorted(set(missing)))))
        st = F.status()
        rows.append((all(k in st["counts"] for k in ("checklists", "lines", "triggers", "done", "skip")) and len(st["documents"]) == 6, "status.json holds the counts and the six documents"))
    except Exception as e:
        rows.append((False, "the data files could not be loaded: %s" % e))
    return all(r[0] for r in rows), rows


def _checks(run, *groups):
    import verify
    R, rj = verify.run_checks(run, "pre")
    out = [r[1] + ((" [all: %s]" % r[2]) if r[2] and r[2] != r[1] else "") for r in R.rows if r[0] == verify.BAD and r[3] in groups]
    for g in groups:
        if not any(r[3] == g for r in R.rows):
            out.append("the checker has no result yet for '%s'" % g)
    return out


def _g(*groups):
    return lambda run, rj: _checks(run, "skill", *groups)


CHECKS = {"locate_ok": _g("locate"), "stages_ok": _g("locate", "stages"), "read_ok": _g("locate", "stages", "read"), "proof_ok": _g("locate", "stages", "read", "proof"),
          "answer_ok": _g("locate", "stages", "read", "proof", "answer"), "plan_ok": _g("locate", "stages", "read", "proof", "plan"),
          "confirm_ok": _g("plan", "confirm"), "record_ok": _g("plan", "confirm", "record")}


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
    if os.path.exists(p(a.run, w.RUN)):
        old = load_run(a.run)
        if old["kind"] != a.kind:
            w.die("REFUSED: this run folder already holds a '%s' run. Use a NEW run folder." % old["kind"], 2)
        print("This run already exists. Showing where it is up to.")
        return cmd_next(a)
    if len((a.request or "").strip()) < 5:
        w.die('--request must be Paul\'s own words that asked for this work')
    ok, rows = preflight()
    print("SELF-TEST BEFORE ANYTHING ELSE:")
    for good, text in rows:
        print("  [%s] %s" % ("OK" if good else "FAIL", text))
    if not ok:
        w.die("\nSTOP. Tell Paul exactly which item failed above. Do not carry on.", 4)
    for d in (w.OUT, w.DOCS_DIR):
        os.makedirs(os.path.join(a.run, d), exist_ok=True)
    rj = {"skill": w.skill_name(), "created": w.now(), "skill_stamp": w.skill_stamp(), "kind": a.kind, "request": a.request, "steps": {}, "today": w.today().strftime("%d/%m/%Y"),
          "program_fingerprint": w.program_fingerprint()}
    save_run(a.run, rj)
    for name, empty in ((w.ACCESS, []), (w.RECEIPT, {}), (w.STATE, {}), (w.DOCS, {})):
        w.save_json(p(a.run, name), empty)
    print("\nSAY THIS TO PAUL FIRST, before anything else in your reply, in exactly these words:\n    %s.\n" % w.version_line())
    print("RUN STARTED  kind: %s   today (South Africa): %s\nPaul's request: %s\n" % (eng.kind_cfg(a.kind)["title"], rj["today"], a.request))
    print("Standing rules for the whole job:\n")
    print(read_ref("00-rules.md"))
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
    for s in steps(rj):
        print("  [%s] %s" % ("done" if rj["steps"].get(s["id"], {}).get("state") == "done" else "    ", s["title"]))
    cur = current_step(rj)
    print("Now: %s" % (cur["id"] if cur else "all done"))


def cmd_preflight(a):
    ok, rows = preflight()
    for good, text in rows:
        print("  [%s] %s" % ("OK" if good else "FAIL", text))
    print("PREFLIGHT: %s" % ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 4)


def cmd_info(a):
    st = F.status()
    print("Status as at %s (Athens time). Counts: %s" % (st["as_of"], ", ".join("%s %s" % (format(v, ","), k) for k, v in st["counts"].items())))
    print("\nOPEN ITEMS:")
    for o in st["open_items"]:
        print("  %s (%s, since %s): %s" % (o["id"], o["owner"], o["since"], o["text"]))
    print("\nBUILD PHASES:")
    for ph in st["phases"]:
        print("  %s | %s | %s" % (ph["phase"], ph["what"][:90], ph["status"][:90]))
    print("\nOUTSIDE THIS SKILL:")
    for o in st["outside"]:
        print("  %s (%s): %s" % (o["name"], o["for"], o["state"]))
    print("  the working flow page: %s" % st["review_page"])


def guard(rj):
    if rj.get("program_fingerprint") and rj["program_fingerprint"] != w.program_fingerprint():
        w.die("REFUSED: the skill's programs, steps, pages, data or settings changed while this run was in progress. The programs are run as they are. Start again in a new run folder.", 3)


def cmd_done(a):
    rj = load_run(a.run)
    guard(rj)
    plist = steps(rj)
    ids = [s["id"] for s in plist]
    if a.step not in ids:
        w.die("'%s' is not a step of this kind of work. Steps: %s" % (a.step, ", ".join(ids)))
    cur = current_step(rj)
    if cur is None or ids.index(a.step) > ids.index(cur["id"]):
        w.die("REFUSED: finish step '%s' first. Steps are done in order, none skipped." % (cur["id"] if cur else "?"), 3)
    step = plist[ids.index(a.step)]
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
        print("EVERY STEP IS DONE.\nPut this SHORT AUDIT (and the items table, if there is one) in your reply, as they are (nothing longer):\n")
        import verify
        R, rj2 = verify.run_checks(a.run, "final")
        verify.print_audit(R, rj2, "final", a.run)
        print()
        print(handback(a.run))
        return
    show_step(a.run, rj, nxt)


def handback(run):
    c = eng.compute(run)
    out = []
    if c["table"]:
        out.append("ITEMS (one row per item, running totals):")
        out.append(eng.format_table(c["table"]))
        if c["plan"].get("documents"):
            out.append("Documents changed (documents first): " + "; ".join("%s (Date Modified %s)" % (r, c["changed"][r]["modified"]) for r in [d["role"] for d in c["plan"]["documents"]] if r in c["changed"]))
        out.append("Go ahead with %s?" % (c["plan"].get("next") or "the next batch (tell me which)"))
    elif c["kind"] in ("docs", "review") and c["plan"]:
        out.append("Documents changed (documents first): " + "; ".join("%s (Date Modified %s)" % (r, c["changed"][r]["modified"]) for r in [d["role"] for d in c["plan"]["documents"]] if r in c["changed"]))
        out.append("Go ahead with %s?" % (c["plan"].get("next") or "the next step (tell me which)"))
    else:
        out.append("FOR PAUL: the answer is checked against the funnel data; the quoted lines were found in the two documents.")
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


def cmd_doc(a):
    rj = load_run(a.run)
    guard(rj)
    if not os.path.isfile(a.file):
        w.die("MISSING: %s" % a.file)
    _route_ok(a.run, a.route, a.role)
    when = w.parse_when(a.modified)
    if when is None:
        w.die("REFUSED: --modified must be the file's Date Modified (ISO time such as 2026-11-04T10:15:00Z, or YYYY-MM-DD HH:MM in Athens time)")
    try:
        text = doctext.read(a.file)
    except Exception as e:
        print("STOP. This file cannot be read: %s" % e)
        sys.exit(5)
    if len(text.strip()) < 40:
        print("STOP. The document has no readable text. The program cannot prove anything on it; save it as text and tell Paul.")
        sys.exit(5)
    rel = os.path.join(w.DOCS_DIR, "%s.txt" % a.role)
    with open(p(a.run, rel), "w", encoding="utf-8", newline="") as f:
        f.write(text)
    docs = w.load_opt(p(a.run, w.DOCS), {})
    docs[a.role] = {"name": os.path.basename(a.file), "route": a.route, "modified": a.modified, "text_file": rel, "sha": w.sha256_file(p(a.run, rel)), "chars": len(text), "t": w.now()}
    w.save_json(p(a.run, w.DOCS), docs)
    print("document registered: %s = %s (%d characters) via %s, Date Modified %s" % (a.role, os.path.basename(a.file), len(text), a.route, a.modified))
    asof = w.parse_when(F.status()["as_of"])
    if asof and when > asof:
        print("NOTE: this document was modified after this skill's status date (%s). The skill's pages may be behind it: read the document itself, and tell Paul where they differ." % F.status()["as_of"])


def cmd_stages(a):
    rj = load_run(a.run)
    guard(rj)
    S = F.stages()
    st = w.load_opt(p(a.run, w.STATE), {})
    if a.general:
        if rj["kind"] not in ("docs", "review"):
            w.die("REFUSED: only a document edit or a review may touch no stage. Name the stage(s) with --codes.")
        if len(a.general.strip()) < 5:
            w.die("REFUSED: say why no stage is touched.")
        st["stages"] = {"codes": [], "general": a.general.strip()}
    else:
        codes = F.split_codes(a.codes)
        bad = [c for c in codes if c not in S]
        if not codes or bad:
            w.die("REFUSED: %s. Stage codes: %s" % (("%s is not a stage" % ", ".join(bad)) if bad else "name at least one stage with --codes", ", ".join(S)))
        st["stages"] = {"codes": list(dict.fromkeys(codes)), "general": None}
    st.pop("read", None)
    w.save_json(p(a.run, w.STATE), st)
    for c in st["stages"]["codes"]:
        print(F.stage_card(c) + "\n")
    c = eng.compute(a.run)
    print("Pages to read for this work: " + ", ".join(c["pages"]))


def cmd_read(a):
    rj = load_run(a.run)
    guard(rj)
    c = eng.compute(a.run)
    if not c["declared"] and not c["general"]:
        w.die("Name the stages first: run.py stages.")
    pages = c["pages"]
    st = w.load_opt(p(a.run, w.STATE), {})
    acked = st.setdefault("read", {}).setdefault("acked", {})
    nxt = next((i for i in range(1, len(pages) + 1) if str(i) not in acked), None)
    if a.ack:
        if nxt is None or a.ack != nxt:
            w.die("REFUSED: pages are acknowledged in order. The next page is %s." % (nxt if nxt else "none (all done)"))
        if len((a.note or "").strip()) < 3:
            w.die('REFUSED: acknowledge the page with a one-line note of what is in it: --note "..."')
        acked[str(a.ack)] = a.note.strip()
        w.save_json(p(a.run, w.STATE), st)
        print("page %d acknowledged (%d of %d)" % (a.ack, len(acked), len(pages)))
        nxt = next((i for i in range(1, len(pages) + 1) if str(i) not in acked), None)
    if nxt is None:
        print("All %d page(s) were read and acknowledged. Now run: python3 %s/run.py done %s read" % (len(pages), SCRIPTS, a.run))
        return
    print("-" * 22 + " PAGE %d of %d: %s " % (nxt, len(pages), pages[nxt - 1]) + "-" * 22)
    print(read_ref(pages[nxt - 1]))
    print("-" * 78)
    print('Read it fully, then: python3 %s/run.py read %s --ack %d --note "one line on what is in this page"' % (SCRIPTS, a.run, nxt))


def cmd_evidence(a):
    rj = load_run(a.run)
    guard(rj)
    c = eng.compute(a.run)
    if a.stage not in c["declared"]:
        w.die("REFUSED: %s was not named with run.py stages." % a.stage)
    entry = {"stage": a.stage, "doc": a.doc, "line": a.line}
    probs, _ = eng.evidence_state(c["docs"], c["declared"], c["evidence"] + [entry])
    probs = [x for x in probs if x.startswith("%s/%s" % (a.stage, a.doc)) or "not registered" in x]
    if probs:
        print("REFUSED:")
        for x in probs:
            print("  - " + x)
        sys.exit(5)
    st = w.load_opt(p(a.run, w.STATE), {})
    ev = [e for e in st.get("evidence", []) if not (e["stage"] == a.stage and e["doc"] == a.doc and w.norm(e["line"]) == w.norm(a.line))] + [dict(entry, t=w.now())]
    st["evidence"] = ev
    w.save_json(p(a.run, w.STATE), st)
    c = eng.compute(a.run)
    print("line found in %s for %s. Still missing: %s" % (a.doc, a.stage, ", ".join(c["ev_missing"]) or "nothing"))


def cmd_answer(a):
    rj = load_run(a.run)
    guard(rj)
    if rj["kind"] not in ("question", "move"):
        w.die("REFUSED: an answer file is for a question or a move.")
    if not os.path.isfile(a.file):
        w.die("MISSING: %s" % a.file)
    shutil.copyfile(a.file, p(a.run, "answer.txt"))
    c = eng.compute(a.run)
    if c["answer_problems"]:
        print("REFUSED. Put these right and run this again:")
        for x in c["answer_problems"]:
            print("  - " + x)
        sys.exit(5)
    print("answer checked: it names every stage with its owner and where it leads.")


def cmd_plan(a):
    rj = load_run(a.run)
    guard(rj)
    if rj["kind"] not in ("build", "test", "docs", "review"):
        w.die("REFUSED: a plan is for a build, a test, a document edit or a review.")
    plan = w.load_json(a.file, "the plan file")
    old = w.load_opt(p(a.run, w.PLAN), None)
    w.save_json(p(a.run, w.PLAN), plan)
    c = eng.compute(a.run)
    if c["plan_problems"]:
        print("REFUSED. Put these right in the plan file and run this again:")
        for x in c["plan_problems"]:
            print("  - " + x)
        sys.exit(5)
    if old is not None and w.content_hash(old) != w.content_hash(plan) and os.path.exists(p(a.run, w.APPROVAL)):
        os.remove(p(a.run, w.APPROVAL))
        print("The plan changed after Paul's go-ahead: his go-ahead is cleared. Show him the new table.")
    print("plan checked: %d object(s), %d document(s)." % (len(plan.get("objects") or []), len(plan.get("documents") or [])))


def confirm_table(c):
    plan = c["plan"]
    out = ["DECISION: %s" % plan["decision"], "PAUL ASKED: %s" % plan["paul_request"], ""]
    if plan.get("documents"):
        out.append("DOCUMENTS (changed first, before AdviceTech):")
        for d in plan["documents"]:
            out.append("  - %s: %s" % (d["role"], d["change"]))
    if plan.get("objects"):
        out.append("ADVICETECH OBJECTS:")
        for o in plan["objects"]:
            own = sorted({F.OWNER_PREFIX.match(l["text"]).group(1) for l in o.get("lines") or [] if F.OWNER_PREFIX.match(l["text"])})
            out.append("  - %s #%s %s (stage %s)%s" % (o["type"], o["id"], o["title"], o.get("stage", "-"), (", %d line(s), owner %s" % (len(o["lines"]), "/".join(own) or "-")) if o.get("lines") else ""))
    if plan.get("tick_path"):
        out.append("TICKS on %s:" % plan.get("client"))
        for n, t in enumerate(plan["tick_path"], 1):
            out.append("  %d. %s: %s -> opens %s" % (n, t["module"], t["line"][:60], t["opens"]))
    out.append("")
    out.append("Checked by the program: Charl's items are not touched; one owner per checklist; the line rules; names; line counts.")
    out.append("Nothing has been changed yet.")
    return "\n".join(out)


def cmd_confirm(a):
    rj = load_run(a.run)
    guard(rj)
    c = eng.compute(a.run)
    if c["plan"] is None or c["plan_problems"]:
        w.die("REFUSED: the plan is not checked yet (run.py plan).")
    print(confirm_table(c))
    print("\nASK PAUL (this is the ONE question of your reply, then STOP): \"Go ahead with %s?\"" % c["plan"]["decision"])
    print("When he says yes: python3 %s/run.py approve %s --said \"his words\"" % (SCRIPTS, a.run))


def cmd_approve(a):
    rj = load_run(a.run)
    guard(rj)
    c = eng.compute(a.run)
    if c["plan"] is None or c["plan_problems"]:
        w.die("REFUSED: the plan is not checked yet (run.py plan).")
    if len((a.said or "").strip()) < 5:
        w.die("REFUSED: record Paul's own words with --said.")
    w.save_json(p(a.run, w.APPROVAL), {"said": a.said.strip(), "t_iso": w.utc_now().isoformat(timespec="seconds"), "plan_sha": c["plan_sha"]})
    print("Paul's go-ahead recorded for this plan.")


def _need_approval(run):
    c = eng.compute(run)
    ap = c["approval"]
    if c["plan"] is None or c["plan_problems"] or not ap or ap.get("plan_sha") != c.get("plan_sha"):
        w.die("REFUSED: nothing is changed before Paul's yes for exactly this plan (run.py confirm, then approve).")
    return c


def cmd_changed(a):
    rj = load_run(a.run)
    guard(rj)
    c = _need_approval(a.run)
    roles = [d["role"] for d in c["plan"].get("documents") or []]
    if a.role not in roles:
        w.die("REFUSED: %s is not a document of the plan (%s)." % (a.role, ", ".join(roles) or "none"))
    if w.parse_when(a.modified) is None:
        w.die("REFUSED: --modified must be the document's new Date Modified (ISO time, or YYYY-MM-DD HH:MM in Athens time)")
    ch = w.load_opt(p(a.run, w.CHANGED), {})
    ch[a.role] = {"modified": a.modified, "note": a.note or "", "t_iso": w.utc_now().isoformat(timespec="seconds")}
    w.save_json(p(a.run, w.CHANGED), ch)
    print("document change recorded: %s (Date Modified %s). Still to change: %s" % (a.role, a.modified, ", ".join(r for r in roles if r not in ch) or "nothing"))


def cmd_result(a):
    rj = load_run(a.run)
    guard(rj)
    c = _need_approval(a.run)
    keys = F.planned_keys(c["plan"], c["kind"])
    if a.key not in keys:
        w.die("REFUSED: %s is not in the plan. Planned: %s" % (a.key, ", ".join(keys)))
    roles = [d["role"] for d in c["plan"].get("documents") or []]
    todo = [r for r in roles if r not in c["changed"]]
    if todo:
        w.die("REFUSED: documents first. Change and record these documents before the first AdviceTech read-back: %s" % ", ".join(todo))
    res = w.load_opt(p(a.run, w.RESULTS), {})
    res[a.key] = {"lines": a.lines, "ok": a.ok, "note": a.note or "", "t_iso": w.utc_now().isoformat(timespec="seconds")}
    w.save_json(p(a.run, w.RESULTS), res)
    print("read-back recorded: %s = %d line(s), %s (%d of %d items recorded)" % (a.key, a.lines, a.ok, len(res), len(keys)))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add(name, fn, *args):
        x = sub.add_parser(name)
        for spec, kw in args:
            x.add_argument(*spec, **kw)
        x.set_defaults(fn=fn)
        return x

    R = (("run",), {})
    add("start", cmd_start, R, (("--kind",), {"required": True, "choices": F.KINDS}), (("--request",), {"required": True}))
    add("preflight", cmd_preflight)
    add("info", cmd_info)
    add("next", cmd_next, R)
    add("status", cmd_status, R)
    add("done", cmd_done, R, (("step",), {}))
    add("access", cmd_access, R, (("--purpose",), {"required": True, "choices": F.ROLES + ("other",)}), (("--route",), {"required": True, "choices": w.ROUTES}),
        (("--result",), {"required": True, "choices": ("found", "failed")}), (("--note",), {}))
    add("doc", cmd_doc, R, (("--role",), {"required": True, "choices": F.ROLES}), (("--file",), {"required": True}), (("--route",), {"required": True, "choices": w.SOURCE_ROUTES}),
        (("--modified",), {"required": True}))
    add("stages", cmd_stages, R, (("--codes",), {}), (("--general",), {}))
    add("read", cmd_read, R, (("--ack",), {"type": int}), (("--note",), {}))
    add("evidence", cmd_evidence, R, (("--stage",), {"required": True}), (("--doc",), {"required": True, "choices": F.ROLES}), (("--line",), {"required": True}))
    add("answer", cmd_answer, R, (("--file",), {"required": True}))
    add("plan", cmd_plan, R, (("--file",), {"required": True}))
    add("confirm", cmd_confirm, R)
    add("approve", cmd_approve, R, (("--said",), {"required": True}))
    add("changed", cmd_changed, R, (("--role",), {"required": True, "choices": F.ROLES}), (("--modified",), {"required": True}), (("--note",), {}))
    add("result", cmd_result, R, (("--key",), {"required": True}), (("--lines",), {"required": True, "type": int}), (("--ok",), {"required": True, "choices": ("yes", "no")}), (("--note",), {}))
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
