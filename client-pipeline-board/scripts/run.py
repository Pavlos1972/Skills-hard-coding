#!/usr/bin/env python3
"""The step driver of the client-pipeline-board: shows ONE step at a time, refuses to skip, keeps the run on disk.

  run.py start <run> --client "First Surname"
  run.py next | status | preflight
  run.py access <run> --purpose board|docs|onfile|other --route device|m365|zapier --result found|failed [--note TEXT]
  run.py base <run> (--file PAGE_READBACK.html --url URL | --first-board yes --said "Paul's words")
  run.py doc <run> --role ROLE --file FILE --route ROUTE
  run.py change <run> --file change.json          apply and check the changes the chat entered
  run.py route <run>                              what is allowed next, from the send table
  run.py build <run>                              board page, messages, email previews, check-in, confirmation table
  run.py show <run>                               show Paul everything with the ONE question
  run.py approve <run> --said "Paul's exact words"
  run.py receipt <run> KEY VALUE
  run.py email <run> --id ID --file READBACK      check a saved draft or a sent item read back from Outlook
  run.py message <run> --id M1 [--used-today yes]  print a Sitamah message with the greeting set by the clock
  run.py messagecheck <run> --id M1 --file READBACK
  run.py checkin <run>                            the exact settings of the same-day check-in
  run.py publish <run> --url URL --file PAGE_READBACK.html
  run.py done <run> STEP                          prove the step, then show the next one

Nothing in these programs sends or publishes: the chat does, after Paul's yes, with exactly what the program printed or wrote.
Claude runs these programs as they are and never rewrites them during a run.
"""
import argparse
import json
import os
import shutil
import sys

import board as b
import boardhtml as bh
import docread
import engine as eng
import wrlib as w

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
RULE = "=" * 78
NATIVE_TOOLS = ("outlook_create_draft", "outlook_create_reply_all_draft", "outlook_create_reply_draft", "outlook_send_mail", "outlook_send_draft")


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
        rows.append((True, "python module pdfplumber is available (reads the Fact Find Summary and other PDFs)"))
    except ImportError:
        rows.append((False, "python module pdfplumber is NOT available (try: pip install pdfplumber)"))
    rows.append((w.skill_stamp() is not None, "the skill has a Last updated stamp (%s)" % (w.stamp_display(w.skill_stamp()) or "none")))
    return all(r[0] for r in rows), rows


def _checks(run, *groups):
    import verify
    R, rj = verify.run_checks(run, "pre")
    out = [r[1] for r in R.rows if r[0] == verify.BAD and r[3] in groups]
    for g in groups:
        if not any(r[3] == g for r in R.rows):
            out.append("the checker has no result yet for '%s'" % g)
    return out


CHECKS = {}


def check(name):
    def deco(fn):
        CHECKS[name] = fn
        return fn
    return deco


@check("locate_ok")
def ck_locate(run, rj):
    return _checks(run, "locate")


@check("change_ok")
def ck_change(run, rj):
    return _checks(run, "locate", "change")


@check("route_ok")
def ck_route(run, rj):
    return _checks(run, "locate", "change", "route")


@check("build_ok")
def ck_build(run, rj):
    return _checks(run, "locate", "change", "route", "build")


@check("confirm_ok")
def ck_confirm(run, rj):
    return _checks(run, "build", "confirm")


@check("send_ok")
def ck_send(run, rj):
    return _checks(run, "build", "confirm", "send")


@check("publish_ok")
def ck_publish(run, rj):
    return _checks(run, "build", "confirm", "send", "publish")


@check("verify_final")
def ck_final(run, rj):
    import verify
    R, rj2 = verify.run_checks(run, "final")
    if R.fails:
        verify.print_audit(R, rj2, "final", run)
        return ["the checker has %d red cross(es) above" % len(R.fails)]
    return []


# ------------------------------------------------------------------ commands
def cmd_start(a):
    parts = a.client.split()
    if len(parts) < 2:
        w.die('--client must be the first name and surname, for example --client "Pat Samplecase"')
    first, surname = parts[0], " ".join(parts[1:])
    if os.path.exists(p(a.run, w.RUN)):
        old = load_run(a.run)
        oc = old["client"]
        if w.norm("%s %s" % (oc["first"], oc["surname"])) != w.norm(a.client):
            w.die("REFUSED: this run folder already belongs to %s %s. One client, one chat, one board: use a NEW run folder." % (oc["first"], oc["surname"]), 2)
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
    rj = {"skill": w.skill_name(), "created": w.now(), "skill_stamp": w.skill_stamp(), "steps": {}, "client": {"first": first, "surname": surname},
          "today": w.today().strftime("%d/%m/%Y"), "program_fingerprint": w.program_fingerprint()}
    save_run(a.run, rj)
    for name, empty in ((w.ACCESS, []), (w.RECEIPT, {}), (w.STATE, {}), (w.DOCS, {"docs": {}})):
        w.save_json(p(a.run, name), empty)
    print("\nSAY THIS TO PAUL FIRST, before anything else in your reply, in exactly these words:\n    %s.\n" % w.version_line())
    print("RUN STARTED  client: %s %s   today (South Africa): %s\n" % (first, surname, rj["today"]))
    print("Standing rules for the whole job:\n")
    print(expand(read_ref("00-rules.md"), a.run))
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
        w.die("REFUSED: the skill's programs, steps, rule pages or tables changed while this run was in progress. The programs are run as they are. Start again in a new run folder.", 3)


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
    print("access try recorded: %s / %s / %s (%d on record)" % (a.purpose, a.route, a.result, len(log)))


def _route_ok(run, route, purpose):
    log = w.load_opt(p(run, w.ACCESS), [])
    if not any(e["route"] == route and e["result"] == "found" and e.get("purpose") == purpose for e in log):
        w.die("REFUSED: record the access try first: run.py access %s --purpose %s --route %s --result found" % (run, purpose, route))
    bad = eng.route_order_problems(log)
    if bad:
        w.die("REFUSED: the routes are tried in order (computer, Microsoft 365, Zapier); %s was used before the earlier ones failed." % ", ".join(bad))


def cmd_base(a):
    rj = load_run(a.run)
    guard(rj)
    st = w.load_opt(p(a.run, w.STATE), {})
    if a.first_board:
        if len((a.said or "").strip()) < 5:
            w.die('REFUSED: a first board needs Paul\'s own words that there is no board yet: --said "..."')
        if not any(e.get("purpose") == "board" for e in w.load_opt(p(a.run, w.ACCESS), [])):
            w.die("REFUSED: log the search for an existing board first: run.py access --purpose board ...")
        w.save_json(p(a.run, w.BASE), {})
        st["base"] = {"first": True, "said": a.said}
        w.save_json(p(a.run, w.STATE), st)
        print("First board: nothing to read back. The first change must be 'init'.")
        return
    if not a.file or not os.path.isfile(a.file) or not a.url:
        w.die("REFUSED: give --file (the published page read back) and --url, or --first-board yes --said ...")
    if not any(e.get("purpose") == "board" and e["result"] == "found" for e in w.load_opt(p(a.run, w.ACCESS), [])):
        w.die("REFUSED: log how the board was found first: run.py access --purpose board --route artifact --result found --note ...")
    with open(a.file, encoding="utf-8", errors="replace") as f:
        html = f.read()
    bd = bh.extract_state(html)
    if bd is None:
        w.die("STOP. The read-back has no board data (state-data). It is not a page this program built; do not rebuild from memory. Tell Paul.", 5)
    if b.state_sha(bd) != bd.get("state_sha"):
        w.die("STOP. The page's data does not match its checksum: it was edited by hand or damaged. Tell Paul; do not carry on from it.", 5)
    c = rj["client"]
    if w.norm(b.client_full(bd)) != w.norm("%s %s" % (c["first"], c["surname"])):
        w.die("STOP. That board is for %s, not %s %s. One client, one chat, one board." % (b.client_full(bd), c["first"], c["surname"]), 5)
    w.save_json(p(a.run, w.BASE), bd)
    st["base"] = {"first": False, "url": a.url, "sha": bd["state_sha"], "stamp": bd.get("stamp")}
    w.save_json(p(a.run, w.STATE), st)
    print("Board read back from %s: last updated %s, %d product line(s), %d change log entr%s." % (a.url, bd.get("stamp"), len(bd["lines"]), len(bd["change_log"]), "y" if len(bd["change_log"]) == 1 else "ies"))


def cmd_doc(a):
    rj = load_run(a.run)
    guard(rj)
    if not a.role or not (a.role.split("_")[0] in {r.split("_")[0] for r in b.settings()["doc_roles"]} or a.role in b.settings()["doc_roles"]):
        w.die("REFUSED: role must be one of %s (a second document of a kind is quote_2, policy_schedule_2 ...)" % ", ".join(b.settings()["doc_roles"]))
    if not a.file or not os.path.isfile(a.file) or not a.route:
        w.die("REFUSED: give --file (an existing file) and --route")
    _route_ok(a.run, a.route, "docs")
    docs = w.load_opt(p(a.run, w.DOCS), {"docs": {}})
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
    print("document registered: %s = %s (%d page(s)) via %s" % (a.role, os.path.basename(a.file), rep["page_count"], a.route))
    if rep["image_only"]:
        print("NOTE: page(s) %s have no readable text. Look at them yourself; a figure on them cannot be proven by the program (use Paul's words)." % ", ".join(map(str, rep["image_only"])))


def _clear_after(run, *keys):
    st = w.load_opt(p(run, w.STATE), {})
    for k in keys:
        st.pop(k, None)
    w.save_json(p(run, w.STATE), st)
    if os.path.exists(p(run, w.APPROVAL)):
        os.remove(p(run, w.APPROVAL))
        print("NOTE: any earlier yes from Paul no longer counts. Show him the new version.")


def cmd_change(a):
    rj = load_run(a.run)
    guard(rj)
    if not os.path.exists(p(a.run, w.BASE)):
        w.die("REFUSED: load the board first: run.py base (or --first-board yes).")
    if not a.file or not os.path.isfile(a.file):
        w.die("MISSING: --file change.json")
    ch = w.load_json(a.file, "the change file")
    w.save_json(p(a.run, w.CHANGE), ch)
    _clear_after(a.run, "shown_sha", "build")
    c = eng.compute(a.run)
    allp = c["problems"] + c["email_problems"] + c["notify_problems"]
    if allp:
        print("REFUSED. These must be put right (fix the change file and run this again):")
        for x in allp:
            print("  - " + x)
        sys.exit(5)
    print("CHANGES APPLIED to %s's board:" % b.client_full(c["board"]))
    for x in c["log"]:
        print("  - " + x)
    print("%d email(s) checked, %d message(s) to Sitamah planned." % (len(c["emails"]), len(c["messages"])))
    print("Next: run.py route %s" % a.run)


def cmd_route(a):
    rj = load_run(a.run)
    c = eng.compute(a.run)
    if c["board"] is None or c["problems"] or c["email_problems"] or c["notify_problems"]:
        w.die("REFUSED: apply the changes first: run.py change (and put every problem right).")
    bd = c["board"]
    print("ROUTING FOR %s (from the send table; the playbooks stay Paul's business logic)\n" % b.client_full(bd).upper())
    shown = set()
    for ln in bd["lines"]:
        pb = b.routes()["lines"][ln]["playbook"]
        print("%s%s -> playbook %s" % (b.card_title(ln), " [%s]" % bd["cards"][ln]["tag"] if bd["cards"][ln].get("tag") else "", pb))
        if pb not in shown:
            shown.add(pb)
            print(read_ref(pb))
    print("\nTHIS RUN:")
    for e in c["emails"]:
        r = b.routes()["routes"][e["route"]]
        print("  email %s | %s | asked Paul first: %s | lands: %s | sent by: %s | fresh yes before it goes: %s" % (
            e["id"], r["label"], ("yes (%s)" % e["asked_paul"]) if r["ask_first"] else "not needed", r["lands"], r["sender"], "YES" if r["yes_before_send"] else "no"))
    for m in c["messages"]:
        print("  message %s | %s | %s" % (m["id"], "Action needed" if m["tier"] == "action" else "FYI", m["trigger"]))
    for x in c["new_actions"]:
        if x.get("via"):
            print("  handed to %s: %s (receipt %s)" % (x["via"], x["text"], x["receipt"]))
    if c["checkin"]:
        print("  same-day check-in: %s at %s" % (c["checkin"]["name"], c["checkin"]["at"]))
    st = w.load_opt(p(a.run, w.STATE), {})
    st["route"] = {"t": w.now()}
    w.save_json(p(a.run, w.STATE), st)
    print("\nNothing here is sent yet. Next: run.py done %s route, then build." % a.run)


def cmd_build(a):
    rj = load_run(a.run)
    guard(rj)
    c = eng.compute(a.run)
    allp = c["problems"] + c["email_problems"] + c["notify_problems"]
    if c["board"] is None or allp:
        w.die("REFUSED: " + ("; ".join(allp) if allp else "apply the changes first"))
    bd = c["board"]
    bd["stamp"] = w.athens_stamp()
    b.seal(bd)
    bp = [x for x in b.board_problems(bd, c["today"]) if not x[0]]
    if bp:
        w.die("REFUSED: " + "; ".join(x[1] for x in bp))
    w.save_json(p(a.run, w.BOARD), bd)
    html = bh.render(bd)
    out = os.path.join(a.run, w.OUT)
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, w.PAGE), "w", encoding="utf-8", newline="") as f:
        f.write(html)
    for e in c["emails"]:
        with open(os.path.join(out, "email_%s.txt" % e["id"]), "w", encoding="utf-8") as f:
            f.write("To: %s\nCc: %s\nSubject: %s\n\n%s\n" % (", ".join(e["to"]), ", ".join(e["cc"]), e["subject"], b.plain(e["body_html"]).strip()))
        w.save_json(os.path.join(out, "email_%s.json" % e["id"]), e)
    w.save_json(os.path.join(out, "messages.json"), c["messages"])
    for m in c["messages"]:
        with open(os.path.join(out, "message_%s.txt" % m["id"]), "w", encoding="utf-8") as f:
            f.write(m["text"])
    if c["checkin"]:
        w.save_json(os.path.join(out, "checkin.json"), c["checkin"])
    _clear_after(a.run, "shown_sha")
    print("BUILT out/%s (the page, stamped %s Athens time), %d email preview(s), %d message(s)%s." % (w.PAGE, bd["stamp"], len(c["emails"]), len(c["messages"]), ", out/checkin.json" if c["checkin"] else ""))
    for ok, short, _d in bh.html_problems(html, bd):
        print("  %s %s" % ("OK " if ok else "BAD", short))


def _table_text(c):
    rows = eng.confirm_rows(c)
    out = ["WHAT WILL CHANGE (each line with its source):", ""]
    for i, (what, value, src) in enumerate(rows, 1):
        out.append("%2d. %s\n      %s\n      source: %s" % (i, what, value.replace("\n", "\n      "), src))
    return "\n".join(out)


def cmd_show(a):
    rj = load_run(a.run)
    guard(rj)
    c = eng.compute(a.run)
    if c["board"] is None or not os.path.exists(p(a.run, w.BOARD)):
        w.die("REFUSED: build first.")
    print(_table_text(c))
    for e in c["emails"]:
        print("\nEMAIL %s IN FULL:\nTo: %s\nCc: %s\nSubject: %s\n\n%s" % (e["id"], ", ".join(e["to"]), ", ".join(e["cc"]), e["subject"], b.plain(e["body_html"]).strip()))
    st = w.load_opt(p(a.run, w.STATE), {})
    st["shown_sha"] = eng.confirm_sha(c)
    w.save_json(p(a.run, w.STATE), st)
    sends = [e for e in c["emails"] if b.routes()["routes"][e["route"]]["kind"] == "send"]
    drafts = len(c["emails"]) - len(sends)
    bits = ["republish %s's board" % b.client_full(c["board"])]
    if sends:
        bits.append("send %d email%s (%s)" % (len(sends), "" if len(sends) == 1 else "s", "; ".join(b.routes()["routes"][e["route"]]["label"] for e in sends)))
    if drafts:
        bits.append("save %d draft%s in Outlook" % (drafts, "" if drafts == 1 else "s"))
    if c["messages"]:
        bits.append("message Sitamah on Teams (%d)" % len(c["messages"]))
    print("\nTHE ONE QUESTION TO PAUL (show everything above in the reply, then ask exactly this):\n    Ready to %s?\n" % ", ".join(bits))
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
    print("Paul's yes recorded for this exact version. Now do the sends (step send).")


def cmd_receipt(a):
    rj = load_run(a.run)
    guard(rj)
    rc = w.load_opt(p(a.run, w.RECEIPT), {})
    rc[a.key] = a.value
    w.save_json(p(a.run, w.RECEIPT), rc)
    print("receipt recorded: %s = %s" % (a.key, a.value))


def _approved(run, c):
    ap = w.load_opt(p(run, w.APPROVAL), None)
    return bool(ap) and ap.get("sha") == eng.confirm_sha(c)


def _text(path):
    if not path or not os.path.isfile(path):
        w.die("REFUSED: give --file (the saved read-back).")
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def cmd_email(a):
    rj = load_run(a.run)
    guard(rj)
    c = eng.compute(a.run)
    e = next((x for x in c["emails"] if x["id"] == a.id), None)
    if e is None:
        w.die("REFUSED: no email '%s' in this run (ids: %s)" % (a.id, ", ".join(x["id"] for x in c["emails"])))
    if not _approved(a.run, c):
        w.die("REFUSED: nothing is created or sent before Paul's yes for exactly this version (show, then approve).")
    rc = w.load_opt(p(a.run, w.RECEIPT), {})
    r = b.routes()["routes"][e["route"]]
    kind_key = "sent" if r["kind"] == "send" else "draft"
    tool = (rc.get("email.%s.created_with" % e["id"]) or "").strip()
    probs = []
    if tool not in NATIVE_TOOLS:
        probs.append("receipt email.%s.created_with must be a native Microsoft 365 tool (%s), never Zapier" % (e["id"], ", ".join(NATIVE_TOOLS)))
    elif (e.get("thread") or {}).get("reply_all_to") and r["kind"] == "draft" and tool != "outlook_create_reply_all_draft":
        probs.append("a request on an existing thread is a reply-all draft (outlook_create_reply_all_draft), not %s" % tool)
    if not (rc.get("email.%s.%s" % (e["id"], kind_key)) or "").strip():
        probs.append("receipt email.%s.%s (the id the tool returned) is not recorded" % (e["id"], kind_key))
    text = _text(a.file)
    res = b.readback_problems(text, e)
    for ok, short in res:
        print("%s %s" % ("✅" if ok else "❌", short))
    st = w.load_opt(p(a.run, w.STATE), {})
    good = all(ok for ok, _ in res) and not probs
    st.setdefault("emails", {})[e["id"]] = {"t": w.now(), "ok": good, "sha": w.sha256_text(text)}
    w.save_json(p(a.run, w.STATE), st)
    dst = p(a.run, os.path.join(w.OUT, "readback_%s.txt" % e["id"]))
    with open(dst, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    for x in probs:
        print("❌ " + x)
    if not good:
        print("\nThe %s is NOT right. Fix it in Outlook (never send a wrong draft), read it back and run this again. Do not message Sitamah." % ("sent item" if kind_key == "sent" else "draft"))
        sys.exit(5)
    print("\nEmail %s is right." % e["id"])


def cmd_message(a):
    rj = load_run(a.run)
    guard(rj)
    c = eng.compute(a.run)
    st = w.load_opt(p(a.run, w.STATE), {})
    m = next((x for x in c["messages"] if x["id"] == a.id), None)
    if m is None:
        w.die("REFUSED: no message '%s' in this run (ids: %s)" % (a.id, ", ".join(x["id"] for x in c["messages"])))
    if not _approved(a.run, c):
        w.die("REFUSED: Sitamah is messaged only after Paul's yes for exactly this version.")
    bad = [e["id"] for e in c["emails"] if not (st.get("emails") or {}).get(e["id"], {}).get("ok")]
    if bad:
        w.die("REFUSED: Sitamah is messaged only after the emails are checked: %s not yet right" % ", ".join(bad))
    sent_before = [k for k, v in (st.get("messages") or {}).items() if v.get("posted_for_greeting")]
    used = a.used_today == "yes" or bool(sent_before)
    clock = w.now_sast()
    greeting = b.greeting_for(clock, used)
    text = m["text"].replace(b.GREETING_MARK, greeting)
    st.setdefault("messages", {})[m["id"]] = {"t": w.now(), "greeting": greeting, "clock": clock.strftime("%H:%M"), "tier": m["tier"], "text_sha": w.sha256_text(text), "posted_for_greeting": True}
    w.save_json(p(a.run, w.STATE), st)
    print("TEAMS MESSAGE %s (send it through Zapier, never through the Teams tool that lacks the scope):\n" % m["id"])
    print(text)
    s = b.settings()["sitamah"]
    print("HOW: Zapier list_dynamic_enum_values (tool_name microsoft_teams_send_chat_message, property_name chat, search \"%s\") and take the 1:1 chat:\n  %s\n  (label %s) - never a meeting chat." % (s["name"], s["chat"], s["chat_label"]))
    print("Then microsoft_teams_send_chat_message with that chat, format \"markdown\" and content = the text above (an output_hint is required). Read the posted message back with read_resource, save it to a file,")
    print("record: run.py receipt %s message.%s.chat <the chat value used>   run.py receipt %s message.%s.format markdown   then: run.py messagecheck %s --id %s --file <the saved read-back>" % (a.run, m["id"], a.run, m["id"], a.run, m["id"]))


def cmd_messagecheck(a):
    rj = load_run(a.run)
    guard(rj)
    c = eng.compute(a.run)
    st = w.load_opt(p(a.run, w.STATE), {})
    m = next((x for x in c["messages"] if x["id"] == a.id), None)
    if m is None or a.id not in (st.get("messages") or {}):
        w.die("REFUSED: run.py message %s first (it builds and shows the message; nothing is posted before that)." % a.id)
    text = _text(a.file)
    res = b.message_problems(text, m["text"], m["tier"], st["messages"][a.id]["greeting"])
    for ok, short in res:
        print("%s %s" % ("✅" if ok else "❌", short))
    dst = p(a.run, os.path.join(w.OUT, "readback_message_%s.txt" % a.id))
    with open(dst, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    st["messages"][a.id]["ok"] = all(ok for ok, _ in res)
    st["messages"][a.id]["sha"] = w.sha256_file(dst)
    w.save_json(p(a.run, w.STATE), st)
    if not st["messages"][a.id]["ok"]:
        print("\nThe posted message does not read right. Tell Paul exactly which line; only delete a message Claude itself posted, and only when Paul asks for a redo.")
        sys.exit(5)
    print("\nMessage %s reads right." % a.id)


def cmd_checkin(a):
    rj = load_run(a.run)
    guard(rj)
    c = eng.compute(a.run)
    if not c["checkin"]:
        print("No follow-up date was entered in this run, so there is no check-in to create.")
        return
    if not _approved(a.run, c):
        w.die("REFUSED: the check-in is created only after Paul's yes.")
    print("CREATE THIS SCHEDULED TASK (create_trigger / send_later, bound to this chat; never the local in-session cron tools), exactly:\n")
    print(json.dumps(c["checkin"], indent=2, ensure_ascii=False))
    print("\nThen record: run.py receipt %s checkin.trigger_id <the id it returned>" % a.run)


def cmd_publish(a):
    rj = load_run(a.run)
    guard(rj)
    c = eng.compute(a.run)
    bd = eng.final_board(a.run, c)
    if bd is None:
        w.die("REFUSED: build first.")
    html = _text(a.file)
    res = bh.html_problems(html, bd)
    for ok, short, _d in res:
        print("%s %s" % ("✅" if ok else "❌", short))
    rc = w.load_opt(p(a.run, w.RECEIPT), {})
    unreal = [x["receipt"] for x in c["new_actions"] if not (rc.get(x["receipt"]) or "").strip()]     # actions of earlier runs were proved in their own run
    if unreal:
        print("❌ The page claims actions that have no receipt yet: %s. Do those first; a board shows only what happened." % ", ".join(unreal))
    st = w.load_opt(p(a.run, w.STATE), {})
    st["publish"] = {"t": w.now(), "url": a.url, "ok": all(ok for ok, _s, _d in res) and not unreal, "sha": w.sha256_text(html)}
    w.save_json(p(a.run, w.STATE), st)
    if not st["publish"]["ok"]:
        print("\nThe published page is NOT what the program built. Do not say the board is updated. Tell Paul exactly which line failed.")
        sys.exit(5)
    print("\nThe published page is exactly the board the program built. Record: run.py receipt %s publish.result <the result the tool gave>" % a.run)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("start")
    s.add_argument("run")
    s.add_argument("--client", required=True)
    s.set_defaults(fn=cmd_start)
    x = sub.add_parser("preflight")
    x.set_defaults(fn=cmd_preflight)
    for name, fn in (("next", cmd_next), ("status", cmd_status), ("route", cmd_route), ("build", cmd_build), ("show", cmd_show), ("checkin", cmd_checkin)):
        x = sub.add_parser(name)
        x.add_argument("run")
        x.set_defaults(fn=fn)
    x = sub.add_parser("done")
    x.add_argument("run")
    x.add_argument("step")
    x.set_defaults(fn=cmd_done)
    x = sub.add_parser("access")
    x.add_argument("run")
    x.add_argument("--purpose", required=True, choices=("board", "docs", "onfile", "other"))
    x.add_argument("--route", required=True, choices=w.ROUTES + ("artifact",))
    x.add_argument("--result", required=True, choices=("found", "failed"))
    x.add_argument("--note")
    x.set_defaults(fn=cmd_access)
    x = sub.add_parser("base")
    x.add_argument("run")
    x.add_argument("--file")
    x.add_argument("--url")
    x.add_argument("--first-board", dest="first_board")
    x.add_argument("--said")
    x.set_defaults(fn=cmd_base)
    x = sub.add_parser("doc")
    x.add_argument("run")
    x.add_argument("--role", required=True)
    x.add_argument("--file", required=True)
    x.add_argument("--route", required=True, choices=w.ROUTES)
    x.set_defaults(fn=cmd_doc)
    x = sub.add_parser("change")
    x.add_argument("run")
    x.add_argument("--file", required=True)
    x.set_defaults(fn=cmd_change)
    x = sub.add_parser("approve")
    x.add_argument("run")
    x.add_argument("--said", required=True)
    x.set_defaults(fn=cmd_approve)
    x = sub.add_parser("receipt")
    x.add_argument("run")
    x.add_argument("key")
    x.add_argument("value")
    x.set_defaults(fn=cmd_receipt)
    x = sub.add_parser("email")
    x.add_argument("run")
    x.add_argument("--id", required=True)
    x.add_argument("--file", required=True)
    x.set_defaults(fn=cmd_email)
    x = sub.add_parser("message")
    x.add_argument("run")
    x.add_argument("--id", required=True)
    x.add_argument("--used-today", dest="used_today", choices=("yes", "no"), default="no")
    x.set_defaults(fn=cmd_message)
    x = sub.add_parser("messagecheck")
    x.add_argument("run")
    x.add_argument("--id", required=True)
    x.add_argument("--file", required=True)
    x.set_defaults(fn=cmd_messagecheck)
    x = sub.add_parser("publish")
    x.add_argument("run")
    x.add_argument("--url", required=True)
    x.add_argument("--file", required=True)
    x.set_defaults(fn=cmd_publish)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
