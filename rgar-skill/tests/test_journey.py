"""The ONE test of the rgar-skill (Operation Skill Restructure: one end-to-end test on invented data).

It plays whole jobs through the program exactly as a chat would, on invented documents (Pat Samplecase, an invented RGAR and Fact Find Summary), with today and the
clock fixed by WR_TODAY and WR_NOW. Nothing is saved or sent anywhere: the folder listing, the Outlook read-back and the posted Teams message are typed in as files.
It proves:
  1. the driver refuses to skip a step, the routes must be tried in order, and the RGAR report and the Fact Find Summary can never be missing;
  2. bad answers are refused (nothing saved): a figure not in the RGAR, a figure that is in it but not next to its label, a net target that is the Reduced Quote's
     contribution target, a date of birth or an age that does not agree, a lump sum of R 0, an escalation not in the report, a name, employer, job title or income
     not in the Fact Find Summary, an email that is not there, a conflict, a meeting in the future, a next meeting in the past, a missing source; a Fact Find Summary
     with no net-target label stops the run; the old label is accepted too;
  3. nothing is built before Paul's yes, a changed answer voids it, and the email the program builds has no placeholder, computed weekdays, the shortfall period worked
     out by the program, the real RGAR file name in the header, the logo only in the full copy, and a body for the Outlook draft with no header and no signature;
  4. the saved copy is the no-logo copy and the RGAR copy must be in the listing, never overwritten without a yes; the draft read-back is refused for every fault (a
     second signature, a wrong Cc, a wrong subject, low importance, a placeholder, BODY_PLACEHOLDER left, an unclosed table, a missing figure, a Loop box); Sitamah is
     messaged only after a checked draft, with the greeting from the clock, and the posted message must read back right in the 1:1 chat as markdown;
  5. the final audit is short and every line is a green tick; a hand-edited saved copy is caught.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
SCRIPTS = os.path.join(SKILL, "scripts")
sys.path.insert(0, SCRIPTS)
sys.path.insert(0, HERE)
import sample  # noqa: E402

OK, BAD = "\u2705", "\u274c"


def run(script, *args, expect=0, env=None):
    e = dict(os.environ, WR_TODAY="05/11/2026", WR_NOW="10:15")
    e.update(env or {})
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS, script)] + list(args), capture_output=True, text=True, encoding="utf-8", env=e)
    if expect == "refused":
        assert r.returncode != 0, "%s %s should have been refused\n%s" % (script, args, r.stdout[-1200:])
    else:
        assert r.returncode == expect, "%s %s -> exit %d (wanted %d)\n%s\n%s" % (script, args, r.returncode, expect, r.stdout[-1800:], r.stderr[-800:])
    return r.stdout + r.stderr


class Journey(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="wr-rgar-test-")
        self.docs = sample.make_docs(self.d)

    def load(self, path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def read(self, path):
        with open(path, encoding="utf-8") as f:
            return f.read()

    def afile(self, data, name="answers.json"):
        path = os.path.join(self.d, name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        return path

    def tfile(self, text, name):
        path = os.path.join(self.d, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return path

    def refused(self, R, data, fragment):
        out = run("run.py", "answers", R, "--file", self.afile(data), expect="refused")
        self.assertIn(fragment, out)
        self.assertFalse(os.path.exists(os.path.join(R, "answers.json")), "a refused answers file must not be saved")

    def read_all(self, R):
        seen = []
        for _ in range(20):
            out = run("run.py", "read", R)
            seen.append(out)
            m = re.search(r"--ack ([a-z_0-9]+:\d+)", out)
            if not m:
                break
            run("run.py", "read", R, "--ack", m.group(1), "--note", "read " + m.group(1))
        run("run.py", "done", R, "read")
        return "\n".join(seen)

    def register(self, R, roles):
        run("run.py", "access", R, "--purpose", "locate", "--route", "device", "--result", "found", "--note", "test")
        for role, key in roles.items():
            run("run.py", "doc", R, "--role", role, "--file", self.docs[key], "--route", "device")

    def test_whole_journey(self):
        self.main_case()
        self.old_label_case()
        self.no_label_case()

    # ------------------------------------------------------------------ the whole job
    def main_case(self):
        import rgi
        A = sample.answers()
        R0 = os.path.join(self.d, "order-test")
        run("run.py", "start", R0, "--client", "Pat", expect="refused")
        out = run("run.py", "start", R0, "--client", "Pat Samplecase")
        self.assertIn("Using rgar-skill, last updated", out)
        run("run.py", "done", R0, "answers", expect="refused")
        run("run.py", "doc", R0, "--role", "rgar_report", "--file", self.docs["rgar_report"], "--route", "device", expect="refused")        # no access try logged
        run("run.py", "access", R0, "--purpose", "locate", "--route", "m365", "--result", "found")
        out = run("run.py", "doc", R0, "--role", "rgar_report", "--file", self.docs["rgar_report"], "--route", "m365", expect="refused")
        self.assertIn("in order", out)

        R = os.path.join(self.d, "run1")
        run("run.py", "start", R, "--client", "Pat Samplecase")
        run("run.py", "access", R, "--purpose", "locate", "--route", "device", "--result", "found", "--note", "test")
        run("run.py", "doc", R, "--role", "bogus", "--file", self.docs["rgar_report"], "--route", "device", expect="refused")
        run("run.py", "doc", R, "--missing", "fact_find_summary", "--said", "there is none", expect="refused")      # can never be missing
        run("run.py", "doc", R, "--role", "rgar_report", "--file", self.docs["rgar_report"], "--route", "device")
        out = run("run.py", "done", R, "locate", expect=3)                                  # no Fact Find Summary yet: the skill stops
        self.assertIn("fact_find_summary", out)
        run("run.py", "doc", R, "--role", "fact_find_summary", "--file", self.docs["fact_find_summary"], "--route", "device")
        run("run.py", "doc", R, "--role", "fact_find_summary_older", "--file", self.docs["fact_find_summary_older"], "--route", "device")
        run("run.py", "done", R, "locate")
        served = self.read_all(R)
        self.assertEqual(len(re.findall(r"- PAGE \d+ of \d+ -", served)), 4)

        # ---- bad answers are refused, nothing saved
        self.refused(R, sample.bad(A, lump_sum="R 160 000"), "lump sum")
        self.refused(R, sample.bad(A, monthly="R 150 000"), "not next to its label")           # in the report, but next to the lump-sum label
        self.refused(R, sample.bad(A, net_monthly_target="R 1 500.00"), "Reduced Quote")        # the contribution target, not the income need
        self.refused(R, sample.bad(A, net_monthly_target="R 26 000.00"), "net monthly target")
        self.refused(R, sample.bad(A, age=42), "does not match the date of birth")
        self.refused(R, sample.bad(A, rgar_dob="16/03/1985"), "date of birth")
        self.refused(R, sample.bad(A, lump_sum="R 0"), "R 0")
        self.refused(R, sample.bad(A, escalation="6.5%"), "escalation")
        self.refused(R, sample.bad(A, years_until_retirement="24.5"), "whole number")
        self.refused(R, sample.bad(A, employer="Invented Corp"), "employer")
        self.refused(R, sample.bad(A, job_title="Invented Role"), "job title")
        self.refused(R, sample.bad(A, gross_monthly_income="R 99 000.00"), "income")
        self.refused(R, sample.bad(A, client_email="other@example.invalid"), "not in the Fact Find Summary")
        self.refused(R, sample.bad(A, email_source="other"), "email_note")
        self.refused(R, sample.bad(A, conflicts=[{"what": "age"}]), "conflict")
        self.refused(R, sample.bad(A, meetings_held=["10/11/2026"]), "future")
        self.refused(R, sample.bad(A, **{"next_meeting.date": "01/11/2026"}), "past")
        self.refused(R, sample.bad(A, **{"next_meeting.time": "5"}), "time like 12pm")
        self.refused(R, sample.bad(A, client_first_name="Robin", client_surname="Testcase"), "not the client Paul named")
        self.refused(R, sample.bad(A, **{"sources.net_target": ""}), "sources.net_target")
        self.refused(R, sample.bad(A, client_full_name="Patricia Beth Samplecase"), "client name")
        run("run.py", "done", R, "answers", expect=3)
        self.assertEqual(rgi.auto_flags(sample.bad(A, recurring_investment="R 0")), [rgi.R0_FLAG])
        self.assertEqual(rgi.auto_flags(A), [])

        # ---- good answers; Paul's yes
        run("run.py", "answers", R, "--file", self.afile(A))
        run("run.py", "done", R, "answers")
        run("run.py", "approve", R, "--said", "yes", expect="refused")                     # not shown yet
        run("run.py", "build", R, expect="refused")                                         # no yes yet
        out = run("run.py", "show", R)
        for frag in ("1st December 2026 until 1st December 2050", "Subject", "Teams message to Sitamah", "<greeting by the clock>", "Are these answers right", "Thursday, 29/10/2026 & Monday, 02/11/2026",
                     "Net monthly target", "The saved copy has no logo."):
            self.assertIn(frag, out)
        run("run.py", "approve", R, "--said", "Yes, those are right")
        changed = sample.bad(A, flags=A["flags"] + ["The RGAR report is dated 03/11/2026."])
        run("run.py", "answers", R, "--file", self.afile(changed))                         # a changed answer voids the yes
        run("run.py", "build", R, expect="refused")
        run("run.py", "show", R)
        run("run.py", "approve", R, "--said", "Yes, those are right")
        run("run.py", "done", R, "confirm")

        # ---- the build
        run("run.py", "build", R)
        name = "Pat_Samplecase_RGAR_Proposal_Email - 05.11.26.html"
        full, saved, body = (self.read(os.path.join(R, "out", name)), self.read(os.path.join(R, "out", "saved", name)), self.read(os.path.join(R, "out", "draft_body.html")))
        self.assertIn("data:image/png;base64,", full)
        self.assertNotIn("data:image", saved)
        self.assertNotIn("Kind regards", body)
        self.assertNotIn("Importance:", body)
        for frag in ("Sent:</td><td style=\"font-size:12pt;\">Thursday, 05/11/2026 10:15", "Sitamah Nathoo", "Patricia Anne Samplecase / Retirement Goal Analysis Report", sample.RGAR_NAME,
                     "pat@example.invalid", "You work for Sample Holdings as an Analyst.", "Thursday, 29/10/2026 &amp; Monday, 02/11/2026", "Thursday, 12/11/2026 @ 12pm",
                     "as of the 1st December 2026 until 1st December 2050", "R 25,000.00 per month (R 30,000.00 gross)", "Future Value of: R 61,000.00", "Once-off lump sum contribution required to fund remaining shortfall: R 150,000.",
                     "Debit order increases every year at: 6%.", "sustainable until you are 85 years old"):
            self.assertIn(frag, full, frag)
        self.assertEqual(len(re.findall(r"\[[A-Z][A-Z0-9 %().,/&#-]*\]", full)), 0)
        run("run.py", "done", R, "build")

        # ---- save: the no-logo copy and the RGAR copy; never overwrite without a yes
        run("run.py", "name", R, "--existing", "x.html;" + name, expect=5)
        run("run.py", "name", R, "--existing", "x.html;" + name, "--overwrite-yes", "Yes, replace it")
        run("run.py", "access", R, "--purpose", "save", "--route", "device", "--result", "found")
        size = os.path.getsize(os.path.join(R, "out", "saved", name))
        run("run.py", "receipt", R, "save.folder", "C:\\Clients\\Samplecase, Pat (CL)\\%s\\Comparative Quotes" % sample.FOLDER)
        run("run.py", "receipt", R, "save.listed_bytes", str(size + 1))
        run("run.py", "done", R, "save", expect=3)                                          # the listed size does not match
        run("run.py", "name", R, "--existing", "x.html")
        run("run.py", "receipt", R, "save.listed_bytes", str(size))
        run("run.py", "done", R, "save", expect=3)                                          # the RGAR copy is not in the listing yet
        run("run.py", "receipt", R, "save.rgar_name", sample.RGAR_NAME)
        run("run.py", "receipt", R, "save.rgar_listed_bytes", str(os.path.getsize(self.docs["rgar_report"])))
        run("run.py", "done", R, "save")

        # ---- the Outlook draft: refused for every fault; no message before a checked draft
        subj = rgi.subject(A)
        run("run.py", "message", R, "--used-today", "no", expect="refused")
        faults = {"a second signature": dict(signature=sample.SIGNATURE + "<p>Kind regards,</p>"), "no signature": dict(signature=""), "a wrong Cc": dict(cc="someone@example.invalid"),
                  "a wrong subject": dict(subject="Pat Samplecase / RGAR"), "low importance": dict(importance="normal"),
                  "a placeholder": dict(content=lambda c: c.replace("Dear Pat,", "Dear [CLIENT FIRST NAME],")),
                  "BODY_PLACEHOLDER left": dict(content=lambda c: c + "<p>BODY_PLACEHOLDER</p>"),
                  "an unclosed table": dict(content=lambda c: c + "<table><tr><td>x</td></tr>"),
                  "a missing figure": dict(content=lambda c: c.replace("Monthly recurring contribution required to fund remaining shortfall: R 4,200.00.", "Monthly recurring contribution: see report.")),
                  "a Loop box": dict(content=lambda c: c + "<div>Loop component</div>")}
        for label, v in faults.items():
            out = run("run.py", "draft", R, "--file", self.tfile(sample.draft_json(A, body, subj, **v), "bad-draft.json"), expect=5)
            self.assertIn(BAD, out, label)
        run("run.py", "draft", R, "--file", self.tfile(sample.draft_json(A, body, subj), "good-draft.json"))
        run("run.py", "done", R, "draft", expect=3)                                         # the cleanup is not recorded
        run("run.py", "receipt", R, "draft.tab_closed", "yes")
        run("run.py", "receipt", R, "draft.stray_deleted", "none")
        run("run.py", "done", R, "draft")

        # ---- the Teams message: greeting from the clock, then the posted message read back
        out = run("run.py", "message", R, "--used-today", "yes")
        self.assertIn("Hi Sitamah,", out)
        out = run("run.py", "message", R, "--used-today", "no")
        self.assertIn("Good morning Sitamah,", out)
        self.assertIn(rgi.SITAMAH_CHAT, out)
        self.assertIn("1. The RGAR report (%s)" % sample.RGAR_NAME[:-4], out)
        for label, v in {"a wrong greeting": dict(greeting="Good afternoon"), "a literal **": dict(html=lambda h: h.replace("<strong>Action needed:</strong>", "**Action needed:**")),
                         "no numbered list": dict(html=lambda h: h.replace("<ol>", "<ul>").replace("</ol>", "</ul>")),
                         "a do-not-send line": dict(html=lambda h: h + "<p>Please do not send it.</p>")}.items():
            g = v.pop("greeting", "Good morning")
            out = run("run.py", "messagecheck", R, "--file", self.tfile(sample.message_json(A, g, **v), "bad-msg.json"), expect=5)
            self.assertIn(BAD, out, label)
        run("run.py", "messagecheck", R, "--file", self.tfile(sample.message_json(A, "Good morning"), "good-msg.json"))
        run("run.py", "receipt", R, "message.chat", "19:someone-else@unq.gbl.spaces")
        run("run.py", "receipt", R, "message.format", "markdown")
        run("run.py", "done", R, "message", expect=3)                                       # the wrong chat
        run("run.py", "receipt", R, "message.chat", rgi.SITAMAH_CHAT)
        run("run.py", "done", R, "message")

        # ---- the final audit: short, all ticks
        out = run("run.py", "done", R, "final")
        self.assertIn("RESULT: PASS", out)
        self.assertFalse([ln for ln in out.splitlines() if ln.startswith(BAD)])
        self.assertLessEqual(len([ln for ln in out.splitlines() if ln.startswith(OK)]), 16)
        self.assertIn("Only attested", out)
        self.assertIn("recurring investment", out)                                          # the attested line about the RGAR matching the product
        self.assertTrue(os.path.exists(os.path.join(R, "out_record", "audit-full.txt")))
        out = run("verify.py", R)
        self.assertIn("RESULT: PASS", out)
        with open(os.path.join(R, "out", "saved", name), "a", encoding="utf-8") as f:       # a hand-edited saved copy is caught
            f.write("<!-- edited by hand -->")
        out = run("verify.py", R, expect=1)
        self.assertIn(BAD, out)
        self.assertIn("RESULT: FAIL", out)

    # ------------------------------------------------------------------ the old label is accepted too
    def old_label_case(self):
        A = sample.answers()
        R = os.path.join(self.d, "run2")
        run("run.py", "start", R, "--client", "Pat Samplecase")
        self.register(R, {"rgar_report": "rgar_report", "fact_find_summary": "ffs_old_label"})
        run("run.py", "done", R, "locate")
        self.read_all(R)
        self.refused(R, sample.bad(A, net_monthly_target="R 1 500.00"), "Reduced Quote")
        run("run.py", "answers", R, "--file", self.afile(A))
        run("run.py", "done", R, "answers")
        run("run.py", "show", R)
        run("run.py", "approve", R, "--said", "Yes")
        run("run.py", "done", R, "confirm")
        run("run.py", "build", R)
        run("run.py", "done", R, "build")

    # ------------------------------------------------------------------ no net-target line at all: the run stops
    def no_label_case(self):
        A = sample.answers()
        R = os.path.join(self.d, "run3")
        run("run.py", "start", R, "--client", "Pat Samplecase")
        self.register(R, {"rgar_report": "rgar_report", "fact_find_summary": "ffs_no_label"})
        run("run.py", "done", R, "locate")
        self.read_all(R)
        self.refused(R, A, "has no line labelled")


if __name__ == "__main__":
    unittest.main()
