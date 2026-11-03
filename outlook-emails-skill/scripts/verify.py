#!/usr/bin/env python3
"""The one checker of the outlook-emails-skill.

  verify.py <run_dir> [pre|final] [--full]

It REBUILDS the tracking plan from the recorded facts, so nothing is taken on trust from a file Claude could have edited, and compares what the
scheduled-task tool returned with that plan. The reply to Paul carries the SHORT AUDIT it prints: one line per check with a green tick or a red
cross, and one closing line for what is only attested (Paul, 03/11/2026). The full record is written to out_record/audit-full.txt.
"""
import hashlib
import os
import sys

import track as trk
import wrlib as w

OK, BAD = "✅", "❌"
STEP_IDS = ["email", "plan", "show", "create", "readback", "final"]


class Results:
    def __init__(self):
        self.rows, self.attested, self.group = [], [], ""

    def add(self, ok, short, detail=""):
        self.rows.append((OK if ok else BAD, short, detail, self.group))

    @property
    def fails(self):
        return [r for r in self.rows if r[0] == BAD]


def prompt_sha(text):
    return hashlib.sha256((text or "").strip().encode("utf-8")).hexdigest()


def run_checks(run, stage):
    R = Results()
    rj = w.load_json(os.path.join(run, w.RUN))
    today = w.parse_date(rj["today"])
    # ---------------------------------------------------------------- the email, with its source
    R.group = "email"
    facts = w.load_opt(os.path.join(run, w.FACTS), None)
    log = w.load_opt(os.path.join(run, w.ACCESS), [])
    if not facts:
        R.add(False, "The email to track is not recorded yet", "step 'email': run.py email")
    else:
        fp = trk.fact_problems(facts, today)
        R.add(not fp, ("Email recorded and valid: %s, sent %s, reply expected from %d sender(s), reason and source given" % (facts["subject"].strip()[:50], facts["sent"], len(facts["senders"]))) if not fp
              else "Email problem: %s" % fp[0], "; ".join(fp))
        R.add(bool(log), "The email was looked up and the try logged (%d on record)" % len(log) if log else "No lookup of the email is logged: run.py access, even if it failed",
              "; ".join("%s %s" % (e["route"], e["result"]) for e in log))
    # ---------------------------------------------------------------- the plan, rebuilt by the program
    R.group = "plan"
    plan = None
    wp, fpth = os.path.join(run, w.OUT, w.WATCH), os.path.join(run, w.OUT, w.FLAG)
    if not facts or trk.fact_problems(facts, today):
        R.add(False, "The plan cannot be checked until the email is good")
    elif not (os.path.exists(wp) and os.path.exists(fpth)):
        R.add(False, "The plan has not been built yet", "step 'plan'")
    else:
        plan = trk.build_plan(facts, today)
        got = {"watch": w.load_json(wp), "flag": w.load_json(fpth), "stop": plan["stop"], "flag_date": plan["flag_date"]}
        pp = trk.plan_problems(facts, got, today)
        R.add(not pp, "Plan follows the rules: hourly Mon-Fri 08:00-17:00 SA time, stops %s, flag %s 09:00 Athens, fresh chat, phone alert, %s only" % (plan["stop"], plan["flag_date"], w.CONNECTOR)
              if not pp else "Plan problem: " + pp[0], "; ".join(pp))
        R.add(got == plan, "The two task files are exactly what the program builds from the email (not edited by hand)")
        # ------------------------------------------------------------ shown to Paul
        R.group = "show"
        st = w.load_opt(os.path.join(run, w.STATE), {})
        R.add(bool(st.get("shown_sha")) and st.get("shown_sha") == trk.plan_sha(plan), "The plan was shown to Paul in the reply" if st.get("shown_sha") == trk.plan_sha(plan) else "The plan was not shown (or was rebuilt after it was shown): run.py show")
        # ------------------------------------------------------------ what the tool returned, against the plan
        R.group = "create"
        rc = w.load_opt(os.path.join(run, w.RECEIPT), {})
        for key, label in (("watch", "watcher"), ("flag", "flag")):
            t = plan[key]
            bad = []
            if not (rc.get(key + ".id") or "").strip():
                bad.append("id")
            if (rc.get(key + ".name") or "").strip() != t["name"]:
                bad.append("name")
            if key == "watch":
                if (rc.get("watch.cron") or "").strip() != t["cron_expression"]:
                    bad.append("schedule")
            else:
                a, b = trk.instant(rc.get("flag.run_once_at")), trk.instant(t["run_once_at"])
                if a is None or a != b:
                    bad.append("fire time")
                n = trk.instant(rc.get("flag.next_run"))
                if n is None or n != b:
                    bad.append("next run")
            if key == "watch" and not (rc.get("watch.next_run") or "").strip():
                bad.append("next run")
            if (rc.get(key + ".enabled") or "").strip().lower() != "yes":
                bad.append("switched on")
            if (rc.get(key + ".new_session") or "").strip().lower() != "yes":
                bad.append("fresh chat each time")
            if (rc.get(key + ".connector_ok") or "").strip().lower() != "yes":
                bad.append("connector warning")
            if rc.get(key + ".prompt_sha") != prompt_sha(t["prompt"]):
                bad.append("instruction text")
            R.add(not bad, ("The %s the tool returned equals the plan (id, name, %s, switched on, fresh chat, instruction text, no connector warning)" % (label, "hourly schedule" if key == "watch" else "fire time"))
                  if not bad else "The %s the tool returned does not match the plan: %s" % (label, ", ".join(bad)), ", ".join(bad))
        ids = (rc.get("watch.id"), rc.get("flag.id"))
        R.add(bool(ids[0]) and bool(ids[1]) and ids[0] != ids[1], "The two tasks have different ids" if ids[0] and ids[1] and ids[0] != ids[1] else "The two task ids are missing or the same")
    if stage == "final":
        R.group = "final"
        done = [s for s in STEP_IDS[:-1] if (rj.get("steps", {}).get(s) or {}).get("state") == "done"]
        fpok = rj.get("program_fingerprint") == w.program_fingerprint()
        R.add(done == STEP_IDS[:-1] and fpok, "Every step done in order (%d of %d) and the programs did not change during the run" % (len(done), len(STEP_IDS) - 1) if done == STEP_IDS[:-1] and fpok else
              "Steps done: %s%s" % (", ".join(done) or "none", "; the programs changed during the run" if not fpok else ""))
        R.attested += ["that the hourly checks really run, find a reply and alert your phone (they run later, in other chats)",
                       "that the watcher stops itself on %s (its own instruction ends it)" % (plan["stop"] if plan else "the last day"),
                       "that this email really needs a reply (the reason is the chat's judgement)",
                       "the sender, subject and date, which the chat typed from Sent Items or from Paul"]
    return R, rj


def print_audit(R, rj, stage, run, full=False):
    lines = ["AUDIT   %s" % w.version_line()]
    for mark, short, detail, _g in R.rows:
        lines.append("%s %s" % (mark, short))
    if R.attested:
        lines.append("Only attested (not proven): " + "; ".join(R.attested) + ".")
    ok = len([r for r in R.rows if r[0] == OK])
    bad = len(R.fails)
    lines.append("RESULT: %s   (%d %s, %d %s)" % ("PASS" if not bad else "FAIL", ok, OK, bad, BAD))
    text = "\n".join(lines)
    print(text)
    fulltext = text + "\n\nFULL RECORD\n" + "\n".join("%s %s\n    %s" % (m, s, d) for m, s, d, _g in R.rows if d)
    try:
        os.makedirs(os.path.join(run, w.OUT + "_record"), exist_ok=True)
        with open(os.path.join(run, w.OUT + "_record", "audit-full.txt"), "w", encoding="utf-8") as f:
            f.write(fulltext + "\n")
    except OSError:
        pass
    if full:
        print("\n" + fulltext.split("FULL RECORD", 1)[1])
    return not bad


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    run = os.path.abspath(args[0])
    stage = args[1] if len(args) > 1 and args[1] in ("pre", "final") else "final"
    R, rj = run_checks(run, stage)
    ok = print_audit(R, rj, stage, run, full="--full" in sys.argv)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
