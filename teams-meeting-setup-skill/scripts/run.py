#!/usr/bin/env python3
"""The step driver of the teams-meeting-setup-skill: shows ONE step at a time, refuses to skip, keeps the run on disk.

  run.py start <run> --client "First Surname" [--mode new|reschedule --event-id ID]
  run.py next | status | preflight
  run.py access <run> --route device|m365|zapier --result found|failed [--note TEXT]     tries to find the Fact Find PDF
  run.py source <run> --file PDF --route ROUTE
  run.py client <run> [--email ADDRESS --said "Paul's words"]                             read name and email from the Fact Find
  run.py facts <run> --date DD/MM/YYYY --time HH:MM --source TEXT [--last-contact DD/MM/YYYY --contact met|spoke
                        --topics "Risk,RA" --needs "a; b" --needs-source TEXT --agenda "a; b"]
  run.py build <run>       build the exact invite (out/invite.json) and the Sitamah message
  run.py show <run>        show Paul the invite and the message, with the one question
  run.py approve <run> --said "Paul's exact words"
  run.py receipt <run> KEY VALUE
  run.py log <run>         print the lines for the board's Fact Find card
  run.py done <run> STEP   prove the step, then show the next one

The invite is a REAL SEND. Nothing in these programs sends it: the chat does, after Paul's yes, with exactly out/invite.json.
Claude runs these programs as they are and never rewrites them during a run.
"""
import argparse
import os
import shutil
import sys

import invite as inv
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
        w.die('This is not a run folder (no %s). Start one with: python3 %s/run.py start <run folder> --client "First Surname"' % (w.RUN, SCRIPTS), 2)
    return w.load_json(path)


def save_run(run, rj):
    w.save_json(p(run, w.RUN), rj)


def read_ref(name):
    with open(os.path.join(w.SKILL_DIR, "references", name), encoding="utf-8") as f:
        return f.read()


def expand(text, run):
    return text.replace("{scripts}", SCRIPTS).replace("{run}", run).replace("{invite}", os.path.join(run, w.OUT, w.INVITE)).replace("{sitamah}", os.path.join(run, w.OUT, w.SITAMAH))


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
    rows.append((w.skill_stamp() is not None, "the skill has a Last updated stamp (%s)" % (w.stamp_display(w.skill_stamp()) or "none")))
    return all(r[0] for r in rows), rows


def _checks(run, *groups):
    import verify
    R, rj = verify.run_checks(run, "pre")
    out = [r[1] for r in R.rows if r[0] == verify.BAD and r[3] in groups]
    for g in groups:
        if not any(r[3] == g for r in R.rows):
            out.append("the checker has no result yet for '%s'" % g)
    return out, R


def _verified(run):
    """(client, facts, payload, sitamah text) as the program rebuilds them, or None."""
    import verify
    rj = load_run(run)
    pdf = p(run, w.FACTFIND_PDF)
    import ffread
    found = verify.client_from_pdf(ffread.read_pdf(pdf))
    email = found["email"] or (rj.get("email_override") or {}).get("email", "")
    client = {"first": found["first"], "surname": found["surname"], "email": email}
    facts = w.load_json(p(run, w.FACTS))
    today = w.parse_date(rj["today"])
    payload = inv.build_payload(client, facts, rj["mode"], rj.get("event_id"), today)
    return rj, client, facts, payload, inv.sitamah_text(client, facts, rj["mode"]), today


# ------------------------------------------------------------------ the checks behind each step
def ck_client(run, rj):
    return _checks(run, "client")[0]


def ck_facts(run, rj):
    return _checks(run, "facts")[0]


def ck_build(run, rj):
    return _checks(run, "client", "facts", "build")[0]


def ck_show(run, rj):
    return _checks(run, "client", "facts", "build", "approval")[0]


def ck_send(run, rj):
    return _checks(run, "client", "facts", "build", "approval", "send")[0]


def ck_log(run, rj):
    return _checks(run, "log")[0]


def ck_final(run, rj):
    import verify
    R, rj2 = verify.run_checks(run, "final")
    if R.fails:
        verify.print_audit(R, rj2, "final", run)
        return ["the checker has %d red cross(es) above" % len(R.fails)]
    return []


CHECKS = {"client_ok": ck_client, "facts_ok": ck_facts, "build_ok": ck_build, "show_ok": ck_show, "send_ok": ck_send, "log_ok": ck_log, "verify_final": ck_final}


# ------------------------------------------------------------------ commands
def cmd_start(a):
    parts = a.client.split()
    if len(parts) < 2:
        w.die('--client must be the first name and surname, for example --client "Pat Samplecase"')
    first, surname = parts[0], " ".join(parts[1:])
    if a.mode == "reschedule" and not a.event_id:
        w.die("REFUSED: a reschedule needs --event-id (the id of the existing event). Never delete and recreate the meeting.")
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
    os.makedirs(os.path.join(a.run, w.OUT), exist_ok=True)
    rj = {"skill": w.skill_name(), "created": w.now(), "skill_stamp": w.skill_stamp(), "steps": {}, "client": {"first": first, "surname": surname},
          "mode": a.mode, "event_id": a.event_id, "today": w.today().strftime("%d/%m/%Y"), "program_fingerprint": w.program_fingerprint()}
    save_run(a.run, rj)
    for name, empty in ((w.ACCESS, []), (w.RECEIPT, {}), (w.STATE, {})):
        w.save_json(p(a.run, name), empty)
    print("\nSAY THIS TO PAUL FIRST, before anything else in your reply, in exactly these words:\n    %s.\n" % w.version_line())
    print("RUN STARTED  client: %s %s   %s   today (South Africa): %s\n" % (first, surname, "RESCHEDULE of event " + a.event_id if a.mode == "reschedule" else "NEW follow-up invite", rj["today"]))
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
        w.die("REFUSED: the skill's programs, steps or rule pages changed while this run was in progress. The programs are run as they are. Start again in a new run folder.", 3)


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
    log.append({"route": a.route, "result": a.result, "note": a.note or "", "t": w.now()})
    w.save_json(p(a.run, w.ACCESS), log)
    print("access try recorded: %s %s (%d on record)" % (a.route, a.result, len(log)))


def cmd_source(a):
    rj = load_run(a.run)
    guard(rj)
    if not os.path.isfile(a.file):
        w.die("MISSING: %s" % a.file)
    log = w.load_opt(p(a.run, w.ACCESS), [])
    if not any(e["route"] == a.route and e["result"] == "found" for e in log):
        w.die("REFUSED: record the access try first: run.py access %s --route %s --result found" % (a.run, a.route))
    order_bad = []
    failed = set()
    for e in log:
        i = w.ROUTES.index(e["route"])
        if any(r not in failed for r in w.ROUTES[:i]):
            order_bad.append(e["route"])
        if e["result"] == "failed":
            failed.add(e["route"])
    if order_bad:
        w.die("REFUSED: the routes are tried in order (computer, Microsoft 365, Zapier); %s was used before the earlier ones failed." % ", ".join(order_bad))
    shutil.copyfile(a.file, p(a.run, w.FACTFIND_PDF))
    rj["source"] = {"route": a.route, "name": os.path.basename(a.file), "size": os.path.getsize(a.file), "sha256": w.sha256_file(a.file)}
    save_run(a.run, rj)
    print("Fact Find PDF brought into the run folder: %s (%d bytes) via %s" % (rj["source"]["name"], rj["source"]["size"], a.route))


def cmd_client(a):
    import ffread
    import verify
    rj = load_run(a.run)
    guard(rj)
    if not os.path.exists(p(a.run, w.FACTFIND_PDF)):
        w.die("The Fact Find PDF is not in the run folder yet: run.py source first.")
    ffd = ffread.read_pdf(p(a.run, w.FACTFIND_PDF))
    probs = ffread.layout_problems(ffd)
    found = verify.client_from_pdf(ffd)
    if probs:
        print("STOP. This PDF is not the program-drawn Fact Find Transcript:\n  - " + "\n  - ".join(probs))
        sys.exit(5)
    c = rj["client"]
    if w.norm("%s %s" % (found["first"], found["surname"])) != w.norm("%s %s" % (c["first"], c["surname"])):
        print("STOP. The PDF is for %s %s but Paul asked for %s %s." % (found["first"], found["surname"], c["first"], c["surname"]))
        sys.exit(5)
    if a.email:
        if not inv.EMAIL.match(a.email) or len((a.said or "").strip()) < 5:
            w.die('REFUSED: give a real address with --email and Paul\'s own words with --said "..." (the chat never invents an email).')
        rj["email_override"] = {"email": a.email, "said": a.said, "t": w.now()}
        save_run(a.run, rj)
    print("READ: %s %s | personal email in the Fact Find: %s" % (found["first"], found["surname"], found["email"] or "NONE USABLE"))
    if not found["email"] and not (rj.get("email_override") or {}).get("email"):
        print("The Fact Find has no usable personal email. Ask Paul for it, then: run.py client %s --email ADDRESS --said \"Paul's words\"" % a.run)
        sys.exit(5)
    print("Client and email are settled.")


def cmd_facts(a):
    rj = load_run(a.run)
    guard(rj)
    facts = {"mode": rj["mode"], "date": a.date, "time": a.time, "source": a.source}
    if rj["mode"] == "new":
        facts.update(last_contact=a.last_contact, contact=a.contact, topics=[x.strip() for x in (a.topics or "").split(",") if x.strip()],
                     needs=[x.strip() for x in (a.needs or "").split(";") if x.strip()], needs_source=a.needs_source or "",
                     agenda=[x.strip() for x in (a.agenda or "").split(";") if x.strip()])
    probs = inv.fact_problems(facts, w.parse_date(rj["today"]))
    if probs:
        print("REFUSED:\n  - " + "\n  - ".join(probs))
        sys.exit(5)
    w.save_json(p(a.run, w.FACTS), facts)
    print("facts recorded: %s" % {k: v for k, v in facts.items() if v})


def cmd_build(a):
    rj, client, facts, payload, sit, today = _verified(a.run)
    guard(rj)
    probs = inv.payload_problems(client, facts, rj["mode"], rj.get("event_id"), payload, today)
    if probs:
        w.die("REFUSED: " + "; ".join(probs))
    w.save_json(p(a.run, os.path.join(w.OUT, w.INVITE)), payload)
    with open(p(a.run, os.path.join(w.OUT, w.INVITE_TXT)), "w", encoding="utf-8") as f:
        f.write(inv.invite_text(client, facts, rj["mode"], payload, today) + "\n")
    with open(p(a.run, os.path.join(w.OUT, w.SITAMAH)), "w", encoding="utf-8") as f:
        f.write(sit)
    for name in (w.APPROVAL,):
        if os.path.exists(p(a.run, name)):
            os.remove(p(a.run, name))
            print("NOTE: the earlier yes from Paul no longer counts, because the invite was rebuilt. Show it to him again.")
    st = w.load_opt(p(a.run, w.STATE), {})
    st.pop("shown_sha", None)
    w.save_json(p(a.run, w.STATE), st)
    print("BUILT out/%s (the exact arguments for the Microsoft 365 tool), out/%s and out/%s" % (w.INVITE, w.INVITE_TXT, w.SITAMAH))


def cmd_show(a):
    rj, client, facts, payload, sit, today = _verified(a.run)
    guard(rj)
    with open(p(a.run, os.path.join(w.OUT, w.INVITE_TXT)), encoding="utf-8") as f:
        text = f.read()
    sha = inv.payload_sha({"invite": w.load_json(p(a.run, os.path.join(w.OUT, w.INVITE))), "sitamah": sit})
    st = w.load_opt(p(a.run, w.STATE), {})
    st["shown_sha"] = sha
    w.save_json(p(a.run, w.STATE), st)
    print(text)
    print("\nMESSAGE TO SITAMAH (sent after the invite, through Zapier, once):\n")
    print(sit)
    start, _ = inv.window(facts)
    if rj["mode"] == "reschedule":
        q = "Ready to move %s %s's Teams meeting to %s at %s SAST (1 hour), updating the existing invite, and to message Sitamah?" % (client["first"], client["surname"], facts["date"], facts["time"])
    else:
        q = "Ready to send %s %s the Teams meeting invite for %s at %s SAST (1 hour), covering %s, and to message Sitamah?" % (
            client["first"], client["surname"], facts["date"], facts["time"], inv.subject_topics(facts["topics"]))
    print("\nTHE ONE QUESTION TO PAUL (show everything above in the reply, then ask exactly this):\n    %s\n" % q)
    print("When he says yes, record his exact words: python3 %s/run.py approve %s --said \"his words\"" % (SCRIPTS, a.run))


def cmd_approve(a):
    rj, client, facts, payload, sit, today = _verified(a.run)
    guard(rj)
    st = w.load_opt(p(a.run, w.STATE), {})
    sha = inv.payload_sha({"invite": w.load_json(p(a.run, os.path.join(w.OUT, w.INVITE))), "sitamah": sit})
    if st.get("shown_sha") != sha:
        w.die("REFUSED: Paul has not been shown this exact invite and message. Run show, put it all in the reply, and only then record his yes.")
    if len((a.said or "").strip()) < 3:
        w.die("REFUSED: record Paul's own words with --said.")
    w.save_json(p(a.run, w.APPROVAL), {"sha": sha, "said": a.said, "t": w.now()})
    print("Paul's yes recorded for this exact invite and message. Now send them (step send).")


def cmd_receipt(a):
    rj = load_run(a.run)
    guard(rj)
    rc = w.load_opt(p(a.run, w.RECEIPT), {})
    rc[a.key] = a.value
    w.save_json(p(a.run, w.RECEIPT), rc)
    print("receipt recorded: %s = %s" % (a.key, a.value))


def cmd_log(a):
    rj, client, facts, payload, sit, today = _verified(a.run)
    print("Log these lines on the board's Fact Find card, under Actions Taken:")
    for line in inv.log_lines(client, facts, rj["mode"], payload):
        print("  " + line)
    print("Then record: python3 %s/run.py receipt %s log.done yes" % (SCRIPTS, a.run))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("start")
    s.add_argument("run")
    s.add_argument("--client", required=True)
    s.add_argument("--mode", choices=("new", "reschedule"), default="new")
    s.add_argument("--event-id", dest="event_id")
    s.set_defaults(fn=cmd_start)
    x = sub.add_parser("preflight")
    x.set_defaults(fn=cmd_preflight)
    for name, fn in (("next", cmd_next), ("status", cmd_status), ("build", cmd_build), ("show", cmd_show), ("log", cmd_log)):
        x = sub.add_parser(name)
        x.add_argument("run")
        x.set_defaults(fn=fn)
    x = sub.add_parser("done")
    x.add_argument("run")
    x.add_argument("step")
    x.set_defaults(fn=cmd_done)
    x = sub.add_parser("access")
    x.add_argument("run")
    x.add_argument("--route", required=True, choices=w.ROUTES)
    x.add_argument("--result", required=True, choices=("found", "failed"))
    x.add_argument("--note")
    x.set_defaults(fn=cmd_access)
    x = sub.add_parser("source")
    x.add_argument("run")
    x.add_argument("--file", required=True)
    x.add_argument("--route", required=True, choices=w.ROUTES)
    x.set_defaults(fn=cmd_source)
    x = sub.add_parser("client")
    x.add_argument("run")
    x.add_argument("--email")
    x.add_argument("--said")
    x.set_defaults(fn=cmd_client)
    x = sub.add_parser("facts")
    x.add_argument("run")
    x.add_argument("--date", required=True)
    x.add_argument("--time", required=True)
    x.add_argument("--source", required=True)
    x.add_argument("--last-contact", dest="last_contact")
    x.add_argument("--contact", choices=("met", "spoke"))
    x.add_argument("--topics")
    x.add_argument("--needs")
    x.add_argument("--needs-source", dest="needs_source")
    x.add_argument("--agenda")
    x.set_defaults(fn=cmd_facts)
    x = sub.add_parser("approve")
    x.add_argument("run")
    x.add_argument("--said", required=True)
    x.set_defaults(fn=cmd_approve)
    x = sub.add_parser("receipt")
    x.add_argument("run")
    x.add_argument("key")
    x.add_argument("value")
    x.set_defaults(fn=cmd_receipt)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
