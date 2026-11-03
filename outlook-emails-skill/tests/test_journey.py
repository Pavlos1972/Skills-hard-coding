"""The ONE test of the outlook-emails-skill (Operation Skill Restructure: one end-to-end test on invented data).

It plays whole jobs through the program exactly as a chat would, on an invented email (a revised-quote request about Pat Samplecase to two
invented addresses at *.example.invalid), with today fixed by WR_TODAY (for tests only). Nothing is created anywhere: the tool results are typed
in as receipts, as a chat would copy them. It proves:
  1. the driver refuses to skip a step, and bad facts are refused (no sender, a bad address, Paul's own address, a future date, no reason,
     an email so old that the watching time is over);
  2. the plan is built exactly (hourly weekday cron in South African time, push alert, fresh chat each time, the Microsoft 365 connector only,
     the flag at 09:00 Athens time on the 2nd business day, weekends skipped, summer and winter Athens offsets) and ends in a short audit of ticks;
  3. a task the tool returned that differs from the plan is caught, and so is a plan file edited by hand;
  4. a plan is never created in the past: an old email moves the flag to the next business day.
"""
import datetime as dt
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
SCRIPTS = os.path.join(SKILL, "scripts")
sys.path.insert(0, SCRIPTS)
import track as trk  # noqa: E402

SUBJECT = "Revised quote request - Pat Samplecase"
SENDERS = "quotes@insurer.example.invalid, admin@broker.example.invalid"


def run(today, script, *args, expect=0):
    env = dict(os.environ, WR_TODAY=today)
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS, script)] + list(args), capture_output=True, text=True, encoding="utf-8", env=env)
    if expect == "refused":
        assert r.returncode != 0, "%s %s should have been refused\n%s" % (script, args, r.stdout[-1200:])
    else:
        assert r.returncode == expect, "%s %s -> exit %d (wanted %d)\n%s\n%s" % (script, args, r.returncode, expect, r.stdout[-1800:], r.stderr[-800:])
    return r.stdout + r.stderr


def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)


def write_text(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text + "\n")


class Journey(unittest.TestCase):
    def email_args(self, R, **over):
        a = dict(senders=SENDERS, subject=SUBJECT, sent="05/11/2026", why="waiting for the revised quote before the follow-up", source="invented: Sent Items search")
        a.update(over)
        return ["email", R, "--senders", a["senders"], "--subject", a["subject"], "--sent", a["sent"], "--why", a["why"], "--source", a["source"]]

    def to_shown(self, d, name, today, **over):
        R = os.path.join(d, name)
        run(today, "run.py", "start", R)
        run(today, "run.py", "access", R, "--route", "m365", "--result", "failed", "--note", "test: draft, not sent yet")
        run(today, "run.py", *self.email_args(R, **over))
        run(today, "run.py", "done", R, "email")
        run(today, "run.py", "build", R)
        run(today, "run.py", "done", R, "plan")
        run(today, "run.py", "show", R)
        run(today, "run.py", "done", R, "show")
        return R

    def receipts(self, today, R, **over):
        w, f = read_json(os.path.join(R, "out", "watch.json")), read_json(os.path.join(R, "out", "flag.json"))
        rc = {"watch.id": "trig_w1", "watch.connector_ok": "yes", "flag.id": "trig_f1", "flag.connector_ok": "yes",
              "watch.name": w["name"], "watch.cron": w["cron_expression"], "watch.enabled": "yes", "watch.next_run": "2026-11-06T08:00:00+02:00", "watch.new_session": "yes",
              "flag.name": f["name"], "flag.run_once_at": f["run_once_at"], "flag.enabled": "yes", "flag.next_run": f["run_once_at"], "flag.new_session": "yes"}
        rc.update(over)
        for k, v in rc.items():
            run(today, "run.py", "receipt", R, k, v)
        write_text(os.path.join(R, "w.txt"), w["prompt"])
        write_text(os.path.join(R, "f.txt"), f["prompt"])
        run(today, "run.py", "promptfile", R, "watch", "--file", os.path.join(R, "w.txt"))
        run(today, "run.py", "promptfile", R, "flag", "--file", os.path.join(R, "f.txt"))

    def finish(self, today, R):
        run(today, "run.py", "done", R, "create")
        run(today, "run.py", "done", R, "readback")
        final = run(today, "run.py", "done", R, "final")
        self.assertIn("RESULT: PASS", final)
        audit = final[final.index("AUDIT"):].strip().splitlines()
        marks = [ln for ln in audit if ln.startswith("✅") or ln.startswith("❌")]
        self.assertLessEqual(len(audit), 20, "the audit must stay short")
        self.assertTrue(all(ln.startswith("✅") for ln in marks), "every check line must be a green tick:\n" + "\n".join(marks))
        self.assertTrue(any(ln.startswith("Only attested") for ln in audit))

    def test_one_journey_on_invented_data(self):
        d = tempfile.mkdtemp(prefix="wr-oe-test-")
        T = "05/11/2026"                                       # a Thursday
        # 1. no step is skipped; bad facts are refused
        R0 = os.path.join(d, "run0")
        run(T, "run.py", "start", R0)
        run(T, "run.py", "done", R0, "plan", expect=3)
        run(T, "run.py", "build", R0, expect="refused")
        run(T, "run.py", "done", R0, "email", expect=3)                                    # nothing recorded, no lookup logged
        for bad in (dict(senders="not-an-address"), dict(senders="paulk@liferisk.co.za"), dict(senders="a@x.example.invalid, a@x.example.invalid"),
                    dict(sent="06/11/2026"), dict(sent="31/02/2026"), dict(why="soon"), dict(source="x"), dict(sent="20/10/2026"), dict(subject="")):
            run(T, "run.py", *self.email_args(R0, **bad), expect=5)
        run(T, "run.py", *self.email_args(R0))
        run(T, "run.py", "done", R0, "email", expect=3)                                    # the lookup try is not logged yet
        run(T, "run.py", "access", R0, "--route", "m365", "--result", "failed", "--note", "test: draft")
        run(T, "run.py", "done", R0, "email")
        run(T, "run.py", "done", R0, "show", expect=3)
        # 2. the good plan: built exactly, ends in a short audit of ticks
        R1 = self.to_shown(d, "run1", T)
        w, f = read_json(os.path.join(R1, "out", "watch.json")), read_json(os.path.join(R1, "out", "flag.json"))
        self.assertEqual(w["cron_expression"], "CRON_TZ=Africa/Johannesburg 0 8-17 * * 1-5")
        self.assertEqual(f["run_once_at"], "2026-11-09T09:00:00+02:00")                    # 2nd business day after Thursday 05/11 is Monday 09/11, Athens winter time
        for t in (w, f):
            self.assertIs(t["create_new_session_on_fire"], True)
            self.assertEqual(t["notifications"], {"push": True})
            self.assertEqual(t["connectors"], ["Microsoft 365"])
            for s in ("quotes@insurer.example.invalid", "admin@broker.example.invalid"):
                self.assertIn(s, t["prompt"])
            self.assertNotIn("paulk@", t["prompt"])
        self.assertIn("12/11/2026", w["prompt"])                                            # 5th business day: Fri 6, Mon 9, Tue 10, Wed 11, Thu 12
        self.assertIn("delete_trigger", w["prompt"])
        self.assertIn("NOT 'no reply'", w["prompt"])
        self.assertTrue(w["name"] != f["name"] and w["name"].startswith("Reply watch:") and f["name"].startswith("Reply flag:"))
        self.receipts(T, R1)
        self.finish(T, R1)
        # 3a. a plan file edited by hand is caught by the final checker
        w["cron_expression"] = "0 * * * *"
        write_json(os.path.join(R1, "out", "watch.json"), w)
        self.assertIn("RESULT: FAIL", run(T, "verify.py", R1, expect=1))
        # 3b. a task the tool returned that differs from the plan is caught (wrong schedule), and so is a wrong fire time
        R2 = self.to_shown(d, "run2", T)
        self.receipts(T, R2, **{"watch.cron": "0 * * * *"})
        run(T, "run.py", "done", R2, "create")
        self.assertIn("schedule", run(T, "run.py", "done", R2, "readback", expect=3))
        self.receipts(T, R2, **{"flag.run_once_at": "2026-11-09T09:00:00+03:00", "flag.next_run": "2026-11-09T09:00:00+03:00"})
        self.assertIn("fire time", run(T, "run.py", "done", R2, "readback", expect=3))
        # 3c. a connector warning from the tool stops the job
        R3 = self.to_shown(d, "run3", T)
        self.receipts(T, R3, **{"watch.connector_ok": "no"})
        run(T, "run.py", "done", R3, "create", expect=3)
        # 3d. a rebuild after the plan was shown asks for it to be shown again
        R4 = self.to_shown(d, "run4", T)
        run(T, "run.py", "build", R4)
        self.assertIn("shown", run(T, "verify.py", R4, "pre", expect=1).lower())
        # 4. weekends are skipped and the summer offset is used: sent Friday 24/07/2026
        R5 = self.to_shown(d, "run5", "24/07/2026", sent="24/07/2026")
        f5 = read_json(os.path.join(R5, "out", "flag.json"))
        self.assertEqual(f5["run_once_at"], "2026-07-28T09:00:00+03:00")                    # Mon 27 is 1, Tue 28 is 2
        self.assertIn("31/07/2026", read_json(os.path.join(R5, "out", "watch.json"))["prompt"])   # the 5th business day is Friday 31/07
        # 5. never in the past: an email sent 4 business days ago moves the flag to the next business day
        R6 = self.to_shown(d, "run6", "11/11/2026", sent="05/11/2026")                     # flag day 09/11 has passed; 11/11 is a Wednesday
        self.assertEqual(read_json(os.path.join(R6, "out", "flag.json"))["run_once_at"], "2026-11-12T09:00:00+02:00")
        # 6. helper rules
        self.assertEqual(trk.add_business_days(dt.date(2026, 11, 6), 2), dt.date(2026, 11, 10))
        self.assertEqual(trk.athens_0900(dt.date(2026, 3, 29)), "2026-03-29T09:00:00+03:00")   # summer time starts on the last Sunday of March
        self.assertEqual(trk.athens_0900(dt.date(2026, 10, 25)), "2026-10-25T09:00:00+02:00")  # and ends on the last Sunday of October


if __name__ == "__main__":
    unittest.main()
