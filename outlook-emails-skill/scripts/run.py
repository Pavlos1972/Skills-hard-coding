#!/usr/bin/env python3
"""The step driver of the outlook-emails-skill: shows ONE step at a time, refuses to skip, keeps the run on disk.

  run.py start <run>
  run.py next | status | preflight
  run.py access <run> --route m365|zapier|device --result found|failed [--note TEXT]     the lookup of the email (Sent Items)
  run.py email <run> --senders "a@x.com,b@y.com" --subject TEXT --sent DD/MM/YYYY --why TEXT --source TEXT [--folder TEXT]
  run.py build <run>        build the two scheduled-task files (out/watch.json, out/flag.json)
  run.py show <run>         print the plan for Paul (no question: it is a standing rule)
  run.py receipt <run> KEY VALUE
  run.py promptfile <run> watch|flag --file F     the instruction text list_triggers returned, saved to a file
  run.py done <run> STEP    prove the step, then show the next one

Nothing in these programs creates the scheduled tasks: the chat does, with exactly out/watch.json and out/flag.json.
Claude runs these programs as they are and never rewrites them during a run.
"""
import argparse
import os
import sys

import track as trk
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
        w.die('This is not a run folder (no %s). Start one with: python3 %s/run.py start <run folder>' % (w.RUN, SCRIPTS), 2)
    return w.load_json(path)


def save_run(run, rj):
    w.save_json(p(run, w.RUN), rj)


def read_ref(name):
    with open(os.path.join(w.SKILL_DIR, "references", name), encoding="utf-8") as f:
        return f.read()


def expand(text, run):
    return (text.replace("{scripts}", SCRIPTS).replace("{run}", run).replace("{watch}", os.path.join(run, w.OUT, w.WATCH))
            .replace("{flag}", os.path.join(run, w.OUT, w.FLAG)))


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
    rows = [(w.skill_stamp() is not None, "the skill has a Last updated stamp (%s)" % (w.stamp_display(w.skill_stamp()) or "none"))]
    try:
        ok = trk.athens_0900(__import__("datetime").date(2026, 7, 1)) == "2026-07-01T09:00:00+03:00" and trk.athens_0900(__import__("datetime").date(2026, 11, 9)) == "2026-11-09T09:00:00+02:00"
    except Exception:
        ok = False
    rows.append((ok, "the Athens summer/winter time rule gives +03:00 in July and +02:00 in November"))
    return all(r[0] for r in rows), rows


def _checks(run, *groups):
    import verify
    R, rj = verify.run_checks(run, "pre")
    out = [r[1] for r in R.rows if r[0] == verify.BAD and r[3] in groups]
    for g in groups:
        if not any(r[3] == g for r in R.rows):
            out.append("the checker has no result yet for '%s'" % g)
    return out, R


def _facts_plan(run):
    rj = load_run(run)
    facts = w.load_json(p(run, w.FACTS))
    today = w.parse_date(rj["today"])
    return rj, facts, trk.build_plan(facts, today), today


# ------------------------------------------------------------------ the checks behind each step
def ck_create(run, rj):
    """Step 'create': both ids are recorded and the tool gave no connector warning (the rest is checked after the read-back)."""
    rc = w.load_opt(p(run, w.RECEIPT), {})
    out = []
    for key in ("watch", "flag"):
        if not (rc.get(key + ".id") or "").strip():
            out.append("the id the tool returned for the %s is not recorded" % key)
        if (rc.get(key + ".connector_ok") or "").strip().lower() != "yes":
            out.append("record whether the %s result warned that no connector is stored (%s.connector_ok yes|no); a warning means STOP and tell Paul" % (key, key))
    if rc.get("watch.id") and rc.get("watch.id") == rc.get("flag.id"):
        out.append("the two tasks cannot have the same id")
    return out


def ck_final(run, rj):
    import verify
    R, rj2 = verify.run_checks(run, "final")
    if R.fails:
        verify.print_audit(R, rj2, "final", run)
        return ["the checker has %d red cross(es) above" % len(R.fails)]
    return []


CHECKS = {
    "email_ok": lambda run, rj: _checks(run, "email")[0],
    "plan_ok": lambda run, rj: _checks(run, "email", "plan")[0],
    "show_ok": lambda run, rj: _checks(run, "email", "plan", "show")[0],
    "create_ok": ck_create,
    "readback_ok": lambda run, rj: _checks(run, "email", "plan", "show", "create")[0],
    "verify_final": ck_final,
}


# ------------------------------------------------------------------ commands
def cmd_start(a):
    if os.path.exists(p(a.run, w.RUN)):
        print("This run already exists. Showing where it is up to.")
        return cmd_next(a)
    ok, rows = preflight()
    print("SELF-TEST BEFORE ANYTHING ELSE:")
    for good, text in rows:
        print("  [%s] %s" % ("OK" if good else "FAIL", text))
    if not ok:
        w.die("\nSTOP. Tell Paul exactly which item failed above. Do not carry on.", 4)
    os.makedirs(os.path.join(a.run, w.OUT), exist_ok=True)
    rj = {"skill": w.skill_name(), "created": w.now(), "skill_stamp": w.skill_stamp(), "steps": {}, "today": w.today().strftime("%d/%m/%Y"),
          "program_fingerprint": w.program_fingerprint()}
    save_run(a.run, rj)
    for name, empty in ((w.ACCESS, []), (w.RECEIPT, {}), (w.STATE, {})):
        w.save_json(p(a.run, name), empty)
    print("\nSAY THIS TO PAUL FIRST, before anything else in your reply, in exactly these words:\n    %s.\n" % w.version_line())
    print("RUN STARTED   today (South Africa): %s\n" % rj["today"])
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
    print("lookup try recorded: %s %s (%d on record)" % (a.route, a.result, len(log)))


def cmd_email(a):
    rj = load_run(a.run)
    guard(rj)
    facts = {"senders": [x.strip() for x in (a.senders or "").split(",") if x.strip()], "subject": a.subject or "", "sent": a.sent, "why": a.why or "",
             "source": a.source or ""}
    if a.folder:
        facts["folder"] = a.folder
    probs = trk.fact_problems(facts, w.parse_date(rj["today"]))
    if probs:
        print("REFUSED:\n  - " + "\n  - ".join(probs))
        sys.exit(5)
    w.save_json(p(a.run, w.FACTS), facts)
    print("email recorded: %s" % {k: v for k, v in facts.items() if v})


def cmd_build(a):
    rj, facts, plan, today = _facts_plan(a.run)
    guard(rj)
    probs = trk.plan_problems(facts, plan, today)
    if probs:
        w.die("REFUSED: " + "; ".join(probs))
    w.save_json(p(a.run, os.path.join(w.OUT, w.WATCH)), plan["watch"])
    w.save_json(p(a.run, os.path.join(w.OUT, w.FLAG)), plan["flag"])
    with open(p(a.run, os.path.join(w.OUT, w.PLAN_TXT)), "w", encoding="utf-8") as f:
        f.write(trk.plan_text(facts, plan) + "\n")
    st = w.load_opt(p(a.run, w.STATE), {})
    st.pop("shown_sha", None)
    w.save_json(p(a.run, w.STATE), st)
    print("BUILT out/%s and out/%s (the exact arguments for the two create_trigger calls) and out/%s" % (w.WATCH, w.FLAG, w.PLAN_TXT))


def cmd_show(a):
    rj, facts, plan, today = _facts_plan(a.run)
    guard(rj)
    got = {"watch": w.load_json(p(a.run, os.path.join(w.OUT, w.WATCH))), "flag": w.load_json(p(a.run, os.path.join(w.OUT, w.FLAG))),
           "stop": plan["stop"], "flag_date": plan["flag_date"]}
    if got != plan:
        w.die("REFUSED: out/ is not what the program builds from the email. Run build again.")
    st = w.load_opt(p(a.run, w.STATE), {})
    st["shown_sha"] = trk.plan_sha(plan)
    w.save_json(p(a.run, w.STATE), st)
    with open(p(a.run, os.path.join(w.OUT, w.PLAN_TXT)), encoding="utf-8") as f:
        print(f.read())
    print("No question to Paul: this is his standing rule and nothing is sent to anyone. Put the plan above in your reply, then create the two tasks (step create).")


def cmd_receipt(a):
    rj = load_run(a.run)
    guard(rj)
    rc = w.load_opt(p(a.run, w.RECEIPT), {})
    rc[a.key] = a.value
    w.save_json(p(a.run, w.RECEIPT), rc)
    print("receipt recorded: %s = %s" % (a.key, a.value))


def cmd_promptfile(a):
    import verify
    rj, facts, plan, today = _facts_plan(a.run)
    guard(rj)
    if not os.path.isfile(a.file):
        w.die("MISSING: %s" % a.file)
    with open(a.file, encoding="utf-8") as f:
        text = f.read()
    rc = w.load_opt(p(a.run, w.RECEIPT), {})
    rc[a.which + ".prompt_sha"] = verify.prompt_sha(text)
    w.save_json(p(a.run, w.RECEIPT), rc)
    same = verify.prompt_sha(text) == verify.prompt_sha(plan[a.which]["prompt"])
    print("instruction text of the %s: %s" % (a.which, "equals the plan" if same else "DIFFERS from the plan (the checker will show a red cross)"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, fn in (("start", cmd_start), ("next", cmd_next), ("status", cmd_status), ("build", cmd_build), ("show", cmd_show)):
        x = sub.add_parser(name)
        x.add_argument("run")
        x.set_defaults(fn=fn)
    x = sub.add_parser("preflight")
    x.set_defaults(fn=cmd_preflight)
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
    x = sub.add_parser("email")
    x.add_argument("run")
    x.add_argument("--senders", required=True)
    x.add_argument("--subject", required=True)
    x.add_argument("--sent", required=True)
    x.add_argument("--why", required=True)
    x.add_argument("--source", required=True)
    x.add_argument("--folder")
    x.set_defaults(fn=cmd_email)
    x = sub.add_parser("receipt")
    x.add_argument("run")
    x.add_argument("key")
    x.add_argument("value")
    x.set_defaults(fn=cmd_receipt)
    x = sub.add_parser("promptfile")
    x.add_argument("run")
    x.add_argument("which", choices=("watch", "flag"))
    x.add_argument("--file", required=True)
    x.set_defaults(fn=cmd_promptfile)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
