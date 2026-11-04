#!/usr/bin/env python3
"""The step driver of the complete-applications-skill: shows ONE step at a time, refuses to skip, keeps the run on disk.

  run.py start <run> --client "First Surname" --mode prefill|correct
  run.py next | status | preflight
  run.py access <run> --purpose folder|docs|other --route device|m365|zapier --result found|failed [--note TEXT]
  run.py doc <run> --role ROLE --file FILE --route ROUTE         a source document (Fact Find, FICA, quote, schedule ...)
  run.py current <run> --id ID --file PDF --route ROUTE          a CURRENT application read for a correction
  run.py plan <run> --file plan.json                             apply and check what the chat entered
  run.py show <run>                                              show Paul the table with the ONE question
  run.py approve <run> --said "Paul's exact words"
  run.py fill <run>                                              fill the real forms, read back every field, prove each box shows something
  run.py receipt <run> KEY VALUE
  run.py save <run> --id ID --file LISTING                       check the folder listing shows the saved file
  run.py rename <run> --id ID --file LISTING                     check the listing shows the renamed transaction folder
  run.py done <run> STEP                                         prove the step, then show the next one

Nothing in these programs saves into the client's folder or renames anything: the chat does, after Paul's yes, with exactly out/*.pdf.
Claude runs these programs as they are and never rewrites them during a run.
"""
import argparse
import os
import re
import shutil
import sys

import apps as A
import docread
import engine as eng
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
        w.die('This is not a run folder (no %s). Start one with: python3 %s/run.py start <run folder> --client "First Surname" --mode prefill|correct' % (w.RUN, SCRIPTS), 2)
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
    for mod, why in (("pypdf", "fills and reads the real PDF forms"), ("pdfplumber", "reads the source documents"), ("PIL", "compares the renders of the forms (Pillow)")):
        try:
            __import__(mod)
            rows.append((True, "python module %s is available (%s)" % (mod, why)))
        except ImportError:
            rows.append((False, "python module %s is NOT available (%s; try: pip install %s)" % (mod, why, "pillow" if mod == "PIL" else mod)))
    rows.append((shutil.which("pdftoppm") is not None, "pdftoppm is available (draws the forms for the render check)" if shutil.which("pdftoppm") else "pdftoppm is NOT available (poppler-utils)"))
    rows.append((w.skill_stamp() is not None, "the skill has a Last updated stamp (%s)" % (w.stamp_display(w.skill_stamp()) or "none")))
    try:
        for f in A.FORMS:
            dp = A.drift_problems(f)
            rows.append((not dp, "the blank %s form is the one this skill knows" % A.FORM_NAMES[f] if not dp else "the blank %s form has changed: %s" % (A.FORM_NAMES[f], dp[0])))
    except Exception as e:
        rows.append((False, "the blank forms could not be checked: %s" % e))
    return all(r[0] for r in rows), rows


def _checks(run, *groups):
    import verify
    R, rj = verify.run_checks(run, "pre")
    out = [r[1] for r in R.rows if r[0] == verify.BAD and r[3] in groups]
    for g in groups:
        if not any(r[3] == g for r in R.rows):
            out.append("the checker has no result yet for '%s'" % g)
    return out


CHECKS = {"locate_ok": lambda run, rj: _checks(run, "locate"), "plan_ok": lambda run, rj: _checks(run, "locate", "plan"),
          "confirm_ok": lambda run, rj: _checks(run, "plan", "confirm"), "fill_ok": lambda run, rj: _checks(run, "plan", "confirm", "fill"),
          "save_ok": lambda run, rj: _checks(run, "plan", "confirm", "fill", "save")}


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
    parts = a.client.split()
    if len(parts) < 2:
        w.die('--client must be the first name and surname, for example --client "Pat Samplecase"')
    first, surname = parts[0], " ".join(parts[1:])
    if os.path.exists(p(a.run, w.RUN)):
        old = load_run(a.run)
        oc = old["client"]
        if w.norm("%s %s" % (oc["first"], oc["surname"])) != w.norm(a.client) or old["mode"] != a.mode:
            w.die("REFUSED: this run folder already belongs to %s %s (%s). Use a NEW run folder." % (oc["first"], oc["surname"], old["mode"]), 2)
        print("This run already exists. Showing where it is up to.")
        return cmd_next(a)
    ok, rows = preflight()
    print("SELF-TEST BEFORE ANYTHING ELSE:")
    for good, text in rows:
        print("  [%s] %s" % ("OK" if good else "FAIL", text))
    if not ok:
        w.die("\nSTOP. Tell Paul exactly which item failed above. Do not carry on.", 4)
    for d in (w.OUT, w.DOCS_DIR, w.CURRENT_DIR):
        os.makedirs(os.path.join(a.run, d), exist_ok=True)
    rj = {"skill": w.skill_name(), "created": w.now(), "skill_stamp": w.skill_stamp(), "steps": {}, "client": {"first": first, "surname": surname}, "mode": a.mode,
          "today": w.today().strftime("%d/%m/%Y"), "program_fingerprint": w.program_fingerprint()}
    save_run(a.run, rj)
    for name, empty in ((w.ACCESS, []), (w.RECEIPT, {}), (w.STATE, {}), (w.DOCS, {"docs": {}, "currents": {}})):
        w.save_json(p(a.run, name), empty)
    print("\nSAY THIS TO PAUL FIRST, before anything else in your reply, in exactly these words:\n    %s.\n" % w.version_line())
    print("RUN STARTED  client: %s %s   mode: %s   today (South Africa): %s\n" % (first, surname, "NEW applications (pre-fill)" if a.mode == "prefill" else "CORRECTION of existing applications", rj["today"]))
    print("Standing rules for the whole job:\n")
    print(expand(read_ref("00-rules.md"), a.run))
    print()
    show_step(a.run, rj, current_step(rj))


def cmd_next(a):
    rj = load_run(a.run)
    s = current_step(rj)
    if s is None:
        print("Every step is done. Run: python3 %s/verify.py %s  and put its SHORT AUDIT in your reply (that is the whole report, with the hand-back)." % (SCRIPTS, a.run))
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
        w.die("REFUSED: the skill's programs, steps, rule pages, forms or tables changed while this run was in progress. The programs are run as they are. Start again in a new run folder.", 3)


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
        print("EVERY STEP IS DONE.\nPut this SHORT AUDIT and the hand-back in your reply, as they are (nothing longer):\n")
        import verify
        R, rj2 = verify.run_checks(a.run, "final")
        verify.print_audit(R, rj2, "final", a.run)
        c = eng.compute(a.run)
        print("\nHAND-BACK (ID and account numbers masked to the last 4):\n")
        print(eng.handback(c, w.load_opt(p(a.run, w.RECEIPT), {})))
        return
    show_step(a.run, rj, nxt)


def cmd_access(a):
    rj = load_run(a.run)
    guard(rj)
    log = w.load_opt(p(a.run, w.ACCESS), [])
    log.append({"purpose": a.purpose, "route": a.route, "result": a.result, "note": a.note or "", "t": w.now()})
    w.save_json(p(a.run, w.ACCESS), log)
    print("access try recorded: %s / %s / %s (%d on record)" % (a.purpose, a.route, a.result, len(log)))


def _route_ok(run, route, purpose):
    log = w.load_opt(p(run, w.ACCESS), [])
    if not any(e["route"] == route and e["result"] == "found" and e.get("purpose") == purpose for e in log):
        w.die("REFUSED: record the access try first: run.py access %s --purpose %s --route %s --result found" % (run, purpose, route))
    bad = eng.route_order_problems(log)
    if bad:
        w.die("REFUSED: the routes are tried in order (computer, Microsoft 365, Zapier); %s was used before the earlier ones failed." % ", ".join(bad))


def _reset(run, *keys):
    st = w.load_opt(p(run, w.STATE), {})
    for k in keys:
        st.pop(k, None)
    w.save_json(p(run, w.STATE), st)
    if os.path.exists(p(run, w.APPROVAL)):
        os.remove(p(run, w.APPROVAL))
        print("NOTE: any earlier yes from Paul no longer counts. Show him the new version.")


def cmd_doc(a):
    rj = load_run(a.run)
    guard(rj)
    roles = A.settings()["doc_roles"]
    if a.role not in roles or a.role == "application_current":
        w.die("REFUSED: role must be one of %s (a current application is registered with run.py current)" % ", ".join(r for r in roles if r != "application_current"))
    if not os.path.isfile(a.file):
        w.die("MISSING: %s" % a.file)
    _route_ok(a.run, a.route, "docs")
    docs = w.load_opt(p(a.run, w.DOCS), {"docs": {}, "currents": {}})
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
    docs["docs"][a.role] = {"file": dst, "text_file": tf, "name": os.path.basename(a.file), "route": a.route, "sha": w.sha256_file(p(a.run, dst)), "pages": rep["page_count"], "image_only": rep["image_only"]}
    w.save_json(p(a.run, w.DOCS), docs)
    _reset(a.run, "shown_sha")
    print("document registered: %s = %s (%d page(s)) via %s" % (a.role, os.path.basename(a.file), rep["page_count"], a.route))
    if rep["image_only"]:
        print("NOTE: page(s) %s have no readable text. Look at them yourself; a value on them needs Paul's words (the program cannot prove it)." % ", ".join(map(str, rep["image_only"])))


def cmd_current(a):
    rj = load_run(a.run)
    guard(rj)
    if rj["mode"] != "correct":
        w.die("REFUSED: current applications are registered only in a correction run.")
    if not os.path.isfile(a.file):
        w.die("MISSING: %s" % a.file)
    _route_ok(a.run, a.route, "docs")
    try:
        form = A.detect_form(a.file)
    except Exception as e:
        print("STOP. This file cannot be read as a PDF form: %s" % e)
        sys.exit(5)
    if form is None:
        print("STOP. This PDF is neither of the two forms this skill knows (its field names differ). Tell Paul; do not carry on.")
        sys.exit(5)
    dp = A.drift_problems(form, a.file)
    if dp:
        print("STOP. This %s has changed from the form this skill knows:\n  - %s" % (A.FORM_NAMES[form], "\n  - ".join(dp)))
        sys.exit(5)
    docs = w.load_opt(p(a.run, w.DOCS), {"docs": {}, "currents": {}})
    dst = os.path.join(w.CURRENT_DIR, "%s.pdf" % a.id)
    shutil.copyfile(a.file, p(a.run, dst))
    docs["currents"][a.id] = {"file": dst, "form": form, "values": A.read_values(p(a.run, dst)), "name": os.path.basename(a.file), "route": a.route, "sha": w.sha256_file(p(a.run, dst))}
    w.save_json(p(a.run, w.DOCS), docs)
    _reset(a.run, "shown_sha")
    filled = sum(1 for v in docs["currents"][a.id]["values"].values() if (v or "").strip())
    print("current application %s registered: %s (%s, %d field(s) filled) via %s" % (a.id, os.path.basename(a.file), A.FORM_NAMES[form], filled, a.route))


def cmd_plan(a):
    rj = load_run(a.run)
    guard(rj)
    if not os.path.isfile(a.file):
        w.die("MISSING: --file plan.json")
    w.save_json(p(a.run, w.PLAN), w.load_json(a.file, "the plan file"))
    _reset(a.run, "shown_sha", "fill", "save")
    c = eng.compute(a.run)
    if c["problems"]:
        print("REFUSED. These must be put right (fix the plan file and run this again):")
        for x in c["problems"]:
            print("  - " + A.mask_text(x))
        sys.exit(5)
    print("PLAN APPLIED for %s %s:" % (c["client"]["first"], c["client"]["surname"]))
    for x in c["apps"]:
        print("  %s: %s | %s | %d field(s) %s" % (x["id"], x["file_name"], A.FORM_NAMES[x["form"]], len(x["changes"]) if x["changes"] or rj["mode"] == "correct" else len([v for v in x["values"].values() if v]), "to change" if rj["mode"] == "correct" else "filled"))
    for fl in c["flags"]:
        print("  FLAG (not a refusal): " + fl)
    print("Next: run.py done %s plan, then show." % a.run)


def _table_text(c):
    out = ["WHAT WILL BE DONE (each line with its source; ID and account numbers masked to the last 4):", ""]
    for i, (what, value, src) in enumerate(c["rows"], 1):
        out.append("%3d. %s\n       %s\n       source: %s" % (i, what, value, src))
    return "\n".join(out)


def cmd_show(a):
    rj = load_run(a.run)
    guard(rj)
    c = eng.compute(a.run)
    if c["plan"] is None or c["problems"]:
        w.die("REFUSED: apply the plan first (run.py plan) and put every problem right.")
    print(_table_text(c))
    st = w.load_opt(p(a.run, w.STATE), {})
    st["shown_sha"] = eng.confirm_sha(c)
    w.save_json(p(a.run, w.STATE), st)
    n = len(c["apps"])
    if rj["mode"] == "prefill":
        ren = sum(1 for x in c["apps"] if x["rename"])
        q = "Ready to fill and save %d new application%s for %s %s in the client's Applications folder%s?" % (n, "" if n == 1 else "s", c["client"]["first"], c["client"]["surname"], " and rename %d transaction folder%s" % (ren, "" if ren == 1 else "s") if ren else "")
    else:
        q = "Ready to correct %d application%s for %s %s in place (one copy, nothing deleted)?" % (n, "" if n == 1 else "s", c["client"]["first"], c["client"]["surname"])
    print("\nTHE ONE QUESTION TO PAUL (show everything above in the reply, then ask exactly this):\n    %s\n" % q)
    print("When he says yes, record his exact words: python3 %s/run.py approve %s --said \"his words\"" % (SCRIPTS, a.run))


def cmd_approve(a):
    rj = load_run(a.run)
    guard(rj)
    c = eng.compute(a.run)
    st = w.load_opt(p(a.run, w.STATE), {})
    sha = eng.confirm_sha(c)
    if st.get("shown_sha") != sha:
        w.die("REFUSED: Paul has not been shown this exact version. Run show, put it all in the reply, and only then record his yes.")
    if len((a.said or "").strip()) < 3:
        w.die("REFUSED: record Paul's own words with --said.")
    w.save_json(p(a.run, w.APPROVAL), {"sha": sha, "said": a.said, "t": w.now()})
    print("Paul's yes recorded for this exact version. Now fill (step fill).")


def _approved(run, c):
    ap = w.load_opt(p(run, w.APPROVAL), None)
    return bool(ap) and ap.get("sha") == eng.confirm_sha(c)


def cmd_fill(a):
    rj = load_run(a.run)
    guard(rj)
    c = eng.compute(a.run)
    if c["plan"] is None or c["problems"]:
        w.die("REFUSED: apply the plan first.")
    if not _approved(a.run, c):
        w.die("REFUSED: nothing is filled before Paul's yes for exactly this version (show, then approve).")
    st = w.load_opt(p(a.run, w.STATE), {})
    st["fill"] = {}
    bad = False
    for x in c["apps"]:
        dp = A.drift_problems(x["form"])
        if dp:
            w.die("STOP. The blank %s form has changed: %s" % (A.FORM_NAMES[x["form"]], dp[0]), 5)
        out_path = p(a.run, os.path.join(w.OUT, x["file_name"]))
        A.fill(x["form"], x["values"], out_path, x["new_option"], start_path=x["base"] if rj["mode"] == "correct" else None)
        rb = A.readback_problems(x["form"], out_path, x["values"])
        if rj["mode"] == "prefill":
            names = [n for n, v in x["values"].items() if (v or "").strip()]
        else:
            names = [n for n, _o, _n, _s in x["changes"]]
        miss = A.render_proof(out_path, x["base"], names)
        extra = []
        if rj["mode"] == "correct":
            changed = {n for n, _o, _n, _s in x["changes"]}
            after = A.read_values(out_path)
            extra = ["%s changed but was not planned" % n for n in after if (after[n] or "") != (x["old"].get(n) or "") and n not in changed]
        ok = not rb and not miss and not extra
        st["fill"][x["id"]] = {"file": x["file_name"], "sha": w.sha256_file(out_path), "size": os.path.getsize(out_path), "ok": ok}
        print("%s %s: %d field(s) read back %s; %d box(es) checked for a visible value%s" % ("✅" if ok else "❌", x["file_name"], len(A.fspec(x["form"])["fields"]), "equal" if not rb else "DIFFERENT", len(names) - len(miss),
                                                                                     "" if not miss else "; NOTHING DRAWN in: " + ", ".join(A.label(x["form"], n) for n in miss)))
        for r_ in rb[:5] + extra[:5]:
            print("   - " + r_)
        bad = bad or not ok
    w.save_json(p(a.run, w.STATE), st)
    if bad:
        print("\nSomething did not read back or does not show. Tell Paul exactly which line; a dropdown that does not draw is reported, never hidden.")
        sys.exit(5)
    print("\nFILLED into out/. Send each file in the chat, then save it into the client's folder (step save).")


def cmd_receipt(a):
    rj = load_run(a.run)
    guard(rj)
    rc = w.load_opt(p(a.run, w.RECEIPT), {})
    rc[a.key] = a.value
    w.save_json(p(a.run, w.RECEIPT), rc)
    print("receipt recorded: %s = %s" % (a.key, a.value))


def _text(path):
    if not path or not os.path.isfile(path):
        w.die("REFUSED: give --file (the saved listing).")
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def cmd_save(a):
    rj = load_run(a.run)
    guard(rj)
    c = eng.compute(a.run)
    st = w.load_opt(p(a.run, w.STATE), {})
    x = next((y for y in c["apps"] if y["id"] == a.id), None)
    if x is None or not (st.get("fill") or {}).get(a.id, {}).get("ok"):
        w.die("REFUSED: fill application '%s' first (it must read back and show)." % a.id)
    if not _approved(a.run, c):
        w.die("REFUSED: nothing is saved before Paul's yes for exactly this version.")
    rc = w.load_opt(p(a.run, w.RECEIPT), {})
    probs = []
    if not (rc.get("save.%s.folder" % a.id) or "").strip():
        probs.append("receipt save.%s.folder (the folder path used) is not recorded" % a.id)
    if not (rc.get("chat.%s.sent" % a.id) or "").strip():
        probs.append("receipt chat.%s.sent (the file was sent in the chat) is not recorded" % a.id)
    if rj["mode"] == "correct":
        sm, em = (rc.get("stage.%s.mtime" % a.id) or "").strip(), (rc.get("commit.%s.expected_mtime" % a.id) or "").strip()
        if not sm or sm != em:
            probs.append("the file was staged fresh and committed with the same expectedMtimeMs (receipts stage.%s.mtime and commit.%s.expected_mtime, equal) so a newer edit by Paul is never overwritten" % (a.id, a.id))
    text = _text(a.file)
    fn = x["file_name"]
    line = next((ln for ln in text.splitlines() if fn.lower() in ln.lower()), None)
    size = st["fill"][a.id]["size"]
    if line is None:
        probs.append("the folder listing does not show %s" % fn)
    sized = bool(line) and str(size) in re.sub(r"[,\s]", "", line)
    st.setdefault("save", {})[a.id] = {"t": w.now(), "ok": not probs, "sized": bool(sized), "listing_sha": w.sha256_text(text)}
    w.save_json(p(a.run, w.STATE), st)
    for pr in probs:
        print("❌ " + pr)
    if probs:
        sys.exit(5)
    print("✅ %s is in the client's Applications folder%s." % (fn, " (listing shows %d bytes)" % size if sized else " (the listing shows no size: attested)"))


def cmd_rename(a):
    rj = load_run(a.run)
    guard(rj)
    c = eng.compute(a.run)
    st = w.load_opt(p(a.run, w.STATE), {})
    x = next((y for y in c["apps"] if y["id"] == a.id), None)
    if x is None or not x["rename"]:
        w.die("REFUSED: no rename is planned for '%s'." % a.id)
    if not _approved(a.run, c):
        w.die("REFUSED: nothing is renamed before Paul's yes for exactly this version.")
    rc = w.load_opt(p(a.run, w.RECEIPT), {})
    text = _text(a.file)
    probs = []
    if x["folder_name"].lower() not in text.lower():
        probs.append("the listing does not show the folder '%s'" % x["folder_name"])
    if (x["app"].get("txn_folder") or {}).get("current_name", "").lower() in text.lower().replace(x["folder_name"].lower(), ""):
        probs.append("the old folder name is still listed: the rename must be a rename (mv -n), not a copy")
    if not (rc.get("rename.%s.done" % a.id) or "").strip():
        probs.append("receipt rename.%s.done (the output of mv -n) is not recorded" % a.id)
    st.setdefault("rename", {})[a.id] = {"t": w.now(), "ok": not probs}
    w.save_json(p(a.run, w.STATE), st)
    for pr in probs:
        print("❌ " + pr)
    if probs:
        sys.exit(5)
    print("✅ the transaction folder is now '%s'." % x["folder_name"])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("start")
    s.add_argument("run")
    s.add_argument("--client", required=True)
    s.add_argument("--mode", choices=("prefill", "correct"), required=True)
    s.set_defaults(fn=cmd_start)
    x = sub.add_parser("preflight")
    x.set_defaults(fn=cmd_preflight)
    for name, fn in (("next", cmd_next), ("status", cmd_status), ("show", cmd_show), ("fill", cmd_fill)):
        x = sub.add_parser(name)
        x.add_argument("run")
        x.set_defaults(fn=fn)
    x = sub.add_parser("done")
    x.add_argument("run")
    x.add_argument("step")
    x.set_defaults(fn=cmd_done)
    x = sub.add_parser("access")
    x.add_argument("run")
    x.add_argument("--purpose", required=True, choices=("folder", "docs", "other"))
    x.add_argument("--route", required=True, choices=w.ROUTES)
    x.add_argument("--result", required=True, choices=("found", "failed"))
    x.add_argument("--note")
    x.set_defaults(fn=cmd_access)
    x = sub.add_parser("doc")
    x.add_argument("run")
    x.add_argument("--role", required=True)
    x.add_argument("--file", required=True)
    x.add_argument("--route", required=True, choices=w.ROUTES)
    x.set_defaults(fn=cmd_doc)
    x = sub.add_parser("current")
    x.add_argument("run")
    x.add_argument("--id", required=True)
    x.add_argument("--file", required=True)
    x.add_argument("--route", required=True, choices=w.ROUTES)
    x.set_defaults(fn=cmd_current)
    x = sub.add_parser("plan")
    x.add_argument("run")
    x.add_argument("--file", required=True)
    x.set_defaults(fn=cmd_plan)
    x = sub.add_parser("approve")
    x.add_argument("run")
    x.add_argument("--said", required=True)
    x.set_defaults(fn=cmd_approve)
    x = sub.add_parser("receipt")
    x.add_argument("run")
    x.add_argument("key")
    x.add_argument("value")
    x.set_defaults(fn=cmd_receipt)
    for name, fn in (("save", cmd_save), ("rename", cmd_rename)):
        x = sub.add_parser(name)
        x.add_argument("run")
        x.add_argument("--id", required=True)
        x.add_argument("--file", required=True)
        x.set_defaults(fn=fn)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
