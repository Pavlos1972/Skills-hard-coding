"""The ONE test of the teams-meeting-setup-skill (Operation Skill Restructure: one end-to-end test on invented data).

It plays whole jobs through the program exactly as a chat would, on an invented client (Pat Samplecase, personal email pat@example.invalid,
in tests/fixtures/*.pdf) with today fixed at 05/11/2026 (WR_TODAY, for tests only). Nothing is sent anywhere: the tool results are typed in as
receipts, as a chat would copy them. It proves:
  1. the driver refuses to skip a step, refuses a PDF of another client, and refuses a route used before the earlier ones failed;
  2. bad facts are refused (past date, unknown topic, follow-up not after the last contact, owed items with no source);
  3. a new invite is built exactly (subject in the fixed order, Africa/Johannesburg on start and end, 1 hour, the client only, Teams on, no link),
     cannot be approved before Paul was shown it, is voided if rebuilt, and ends in a short audit of green ticks;
  4. what the tool returned that differs from what Paul approved is caught; an invite edited by hand is caught by the final checker;
  5. a reschedule updates the existing event (its id) and also passes.
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
import invite as inv  # noqa: E402

PDF = os.path.join(HERE, "fixtures", "Fact Find Transcript - 05.11.26 - (Pat Samplecase).pdf")
ENV = dict(os.environ, WR_TODAY="05/11/2026")
SUBJECT = "Pat Samplecase / Risk & RA"


def run(script, *args, expect=0):
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS, script)] + list(args), capture_output=True, text=True, encoding="utf-8", env=ENV)
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


def good_facts(R, **over):
    a = dict(date="12/11/2026", time="16:00", last_contact="05/11/2026", contact="met", topics="RA,Risk", source="invented follow-up summary",
             needs="Confirm budget; Send latest RA statement", needs_source="invented Fact Find documents to request")
    a.update(over)
    args = ["facts", R, "--date", a["date"], "--time", a["time"], "--source", a["source"], "--last-contact", a["last_contact"],
            "--contact", a["contact"], "--topics", a["topics"]]
    if a["needs"]:
        args += ["--needs", a["needs"], "--needs-source", a["needs_source"]]
    return args


class Journey(unittest.TestCase):
    def start(self, d, name, client="Pat Samplecase", *more):
        R = os.path.join(d, name)
        out = run("run.py", "start", R, "--client", client, *more)
        self.assertIn("Using teams-meeting-setup-skill, last updated", out)
        run("run.py", "access", R, "--route", "device", "--result", "found", "--note", "test")
        run("run.py", "source", R, "--file", PDF, "--route", "device")
        return R

    def to_shown(self, d, name, mode="new", **over):
        extra = ("--mode", "reschedule", "--event-id", "EVENT-ID-1") if mode == "reschedule" else ()
        R = self.start(d, name, "Pat Samplecase", *extra)
        run("run.py", "client", R)
        run("run.py", "done", R, "client")
        if mode == "reschedule":
            run("run.py", "facts", R, "--date", "14/11/2026", "--time", "10:30", "--source", "invented: client asked to move")
        else:
            run("run.py", *good_facts(R, **over))
        run("run.py", "done", R, "facts")
        run("run.py", "build", R)
        run("run.py", "done", R, "build")
        return R

    def approve(self, R):
        shown = run("run.py", "show", R)
        run("run.py", "approve", R, "--said", "Yes, send it")
        run("run.py", "done", R, "show")
        return shown

    def receipts(self, R, mode="new", start="2026-11-12T16:00:00", end="2026-11-12T17:00:00"):
        pairs = [("event.id", "EVENT-ID-1"), ("event.start", start), ("event.end", end), ("sitamah.sent", "msg-1")]
        if mode == "new":
            pairs += [("event.subject", SUBJECT), ("event.attendee", "pat@example.invalid"), ("event.online", "yes")]
        for k, v in pairs:
            run("run.py", "receipt", R, k, v)

    def finish(self, R):
        run("run.py", "done", R, "send")
        run("run.py", "receipt", R, "log.done", "yes")
        run("run.py", "done", R, "log")
        final = run("run.py", "done", R, "final")
        self.assertIn("RESULT: PASS", final)
        audit = final[final.index("AUDIT"):].strip().splitlines()
        marks = [ln for ln in audit if ln.startswith("✅") or ln.startswith("❌")]
        self.assertLessEqual(len(audit), 20, "the audit must stay short")
        self.assertTrue(all(ln.startswith("✅") for ln in marks), "every check line must be a green tick:\n" + "\n".join(marks))
        self.assertTrue(any(ln.startswith("Only attested") for ln in audit))

    def test_one_journey_on_invented_data(self):
        d = tempfile.mkdtemp(prefix="wr-tm-test-")
        # 1. no step is skipped; another client's PDF is refused; routes are tried in order; a reschedule needs an event id
        R0 = os.path.join(d, "run0")
        run("run.py", "start", R0, "--client", "Pat Samplecase")
        run("run.py", "done", R0, "facts", expect=3)
        run("run.py", "source", R0, "--file", PDF, "--route", "device", expect="refused")
        run("run.py", "access", R0, "--route", "zapier", "--result", "found", "--note", "test")
        run("run.py", "source", R0, "--file", PDF, "--route", "zapier", expect="refused")
        run("run.py", "start", os.path.join(d, "runx"), "--client", "Pat Samplecase", "--mode", "reschedule", expect="refused")
        R9 = self.start(d, "run9", "Robin Testcase")
        self.assertIn("STOP", run("run.py", "client", R9, expect=5))
        # 2. bad facts are refused
        R1 = self.start(d, "run1")
        run("run.py", "client", R1)
        run("run.py", "done", R1, "client")
        for bad in (dict(date="04/11/2026"), dict(topics="Cars"), dict(topics="RA,RA"), dict(topics=""), dict(last_contact="12/11/2026"),
                    dict(time="25:00"), dict(needs="Confirm budget", needs_source=""), dict(source="x"), dict(date="31/02/2026")):
            run("run.py", *good_facts(R1, **bad), expect=5)
        run("run.py", "build", R1, expect="refused")
        # 3. the good invite: built exactly, not approvable before it was shown, voided if rebuilt
        run("run.py", *good_facts(R1))
        run("run.py", "done", R1, "facts")
        run("run.py", "build", R1)
        run("run.py", "done", R1, "build")
        run("run.py", "approve", R1, "--said", "Yes", expect="refused")
        run("run.py", "done", R1, "show", expect=3)
        shown = run("run.py", "show", R1)
        self.assertIn("Ready to send Pat Samplecase the Teams meeting invite for 12/11/2026 at 16:00 SAST (1 hour), covering Risk & RA", shown)
        self.assertIn("MESSAGE TO SITAMAH", shown)
        run("run.py", "approve", R1, "--said", "Yes, send it")
        run("run.py", "build", R1)                                   # a rebuild voids the earlier yes
        run("run.py", "done", R1, "show", expect=3)
        self.approve(R1)
        payload = read_json(os.path.join(R1, "out", "invite.json"))
        self.assertEqual(payload["subject"], SUBJECT)
        self.assertEqual((payload["start"]["timeZone"], payload["end"]["timeZone"]), ("Africa/Johannesburg", "Africa/Johannesburg"))
        s, e = (dt.datetime.fromisoformat(payload[k]["dateTime"]) for k in ("start", "end"))
        self.assertEqual(e - s, dt.timedelta(hours=1))
        self.assertEqual([a["email"] for a in payload["attendees"]], ["pat@example.invalid"])
        self.assertTrue(payload["isOnlineMeeting"] and payload["responseRequested"] and payload["bodyType"] == "html")
        self.assertIn("Great to have met with you earlier today.", payload["body"])
        self.assertNotIn("http", payload["body"].lower())
        # 4. what the tool returned must equal what Paul approved
        self.receipts(R1, start="2026-11-12T15:00:00")
        self.assertIn("event.start", run("run.py", "done", R1, "send", expect=3))
        self.receipts(R1)
        self.finish(R1)
        # 4b. an invite edited by hand afterwards is caught by the final checker
        payload["attendees"].append({"email": "sitamah@liferisk.co.za", "name": "Sitamah", "type": "required"})
        write_json(os.path.join(R1, "out", "invite.json"), payload)
        self.assertIn("RESULT: FAIL", run("verify.py", R1, expect=1))
        # 5. a reschedule updates the existing event in place and also passes
        R2 = self.to_shown(d, "run2", mode="reschedule")
        p2 = read_json(os.path.join(R2, "out", "invite.json"))
        self.assertEqual(set(p2), {"eventId", "start", "end"})
        self.assertEqual(p2["eventId"], "EVENT-ID-1")
        self.approve(R2)
        self.receipts(R2, "reschedule", start="2026-11-14T10:30:00", end="2026-11-14T11:30:00")
        self.finish(R2)
        # 6. the opening line follows the real gap and the real kind of contact
        today = dt.date(2026, 11, 5)
        self.assertEqual(inv.opening_line(today, "met", today), "Great to have met with you earlier today.")
        self.assertEqual(inv.opening_line(today - dt.timedelta(days=1), "met", today), "Great to have met with you yesterday.")
        self.assertEqual(inv.opening_line(dt.date(2026, 10, 20), "spoke", today), "Great to have spoken with you on 20/10/2026.")
        self.assertEqual(inv.subject_topics(["Risk", "RA", "RGAR"]), "Risk, RA & RGAR")
        self.assertEqual(inv.subject_topics(["RA"]), "RA")


if __name__ == "__main__":
    unittest.main()
