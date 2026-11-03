"""The ONE test of the om-tax-free-skill (Operation Skill Restructure: one end-to-end test on invented data).

It plays a whole job through the program exactly as a chat would, on invented documents (Pat Samplecase, invented funds, an invented quote), with today and the
clock fixed by WR_TODAY and WR_NOW. Nothing is saved or sent anywhere: the folder listing, the Outlook read-back and the posted Teams message are typed in as files.
It proves:
  1. the driver refuses to skip a step, and the routes must be tried in order; documents that do not exist need Paul's words; the quote can never be missing;
  2. only the documents that must be read are served page by page; the fund fact sheets are kept for the checks only;
  3. bad answers are refused (nothing saved): a figure, fund, allocation or fee that is not in the quote (0.73% is not 0.733%), allocations not adding up to 100%,
     a name, employer, position or income not in the Fact Find Summary, an email not in it, a child, a lump sum, a plan owner under 18, a start date nobody confirmed,
     a conflicting risk profile, a meeting in the future, a next meeting in the past, a missing fact sheet, a conflict, the wrong client;
  4. nothing is built before Paul's yes, a changed answer voids it, and the email the program builds has no placeholder, computed weekdays, the fee total added up,
     the logo only in the full copy, and a body for the Outlook draft with no header and no signature; a hand-edited file is caught;
  5. the saved copy is the no-logo copy, never overwritten without a yes; the draft read-back is refused for every fault (a second signature, a wrong Cc, a wrong
     subject, low importance, a placeholder, an unclosed table, a missing fund, a Loop box); Sitamah is messaged only after a checked draft, with the greeting from
     the clock, and the posted message must read back right in the 1:1 chat as markdown;
  6. the final audit is short and every line is a green tick.
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
        self.d = tempfile.mkdtemp(prefix="wr-tf-test-")
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

    def test_whole_journey(self):
        A = sample.answers()
        # ---- order and refusals before anything is registered
        R0 = os.path.join(self.d, "order-test")
        run("run.py", "start", R0, "--client", "Pat", expect="refused")
        out = run("run.py", "start", R0, "--client", "Pat Samplecase")
        self.assertIn("Using om-tax-free-skill, last updated", out)
        run("run.py", "done", R0, "answers", expect="refused")
        run("run.py", "doc", R0, "--role", "quote", "--file", self.docs["quote"], "--route", "device", expect="refused")        # no access try logged
        run("run.py", "access", R0, "--purpose", "locate", "--route", "m365", "--result", "found")
        out = run("run.py", "doc", R0, "--role", "quote", "--file", self.docs["quote"], "--route", "m365", expect="refused")
        self.assertIn("in order", out)

        R = os.path.join(self.d, "run1")
        run("run.py", "start", R, "--client", "Pat Samplecase")
        run("run.py", "access", R, "--purpose", "locate", "--route", "device", "--result", "found", "--note", "test")
        run("run.py", "doc", R, "--role", "bogus", "--file", self.docs["quote"], "--route", "device", expect="refused")
        for role in ("quote", "fact_find_summary", "fact_find_summary_older", "overview", "fund_fact_sheet_1", "fund_fact_sheet_2"):
            run("run.py", "doc", R, "--role", role, "--file", self.docs[role], "--route", "device")
        out = run("run.py", "doc", R, "--role", "risk_questionnaire", "--file", self.docs["risk_questionnaire"], "--route", "device")
        self.assertIn("no readable text", out)
        out = run("run.py", "done", R, "locate", expect=3)                                  # the strategy summary is neither registered nor declared missing
        self.assertIn("strategy_summary", out)
        run("run.py", "doc", R, "--missing", "quote", "--said", "there is none", expect="refused")           # the quote can never be missing
        run("run.py", "doc", R, "--missing", "strategy_summary", "--said", "no", expect="refused")           # Paul's real words are needed
        run("run.py", "doc", R, "--role", "strategy_summary", "--file", self.docs["strategy_summary"], "--route", "device")
        run("run.py", "done", R, "locate")
        served = self.read_all(R)
        self.assertNotIn("Sample Growth Fund fact sheet", served, "the fact sheets are kept for the checks, not served")
        self.assertEqual(len(re.findall(r"- PAGE \d+ of \d+ -", served)), 6)

        # ---- bad answers are refused, nothing saved
        self.refused(R, sample.bad(A, contribution="R 2 700.00"), "contribution in the quote")
        self.refused(R, sample.bad(A, **{"funds.0.name": "Invented Fund"}), "Invented Fund")
        self.refused(R, sample.bad(A, **{"fees.advice": "0.50%", "fees.asset_management": "0.73%"}), "not in the document's text")
        self.refused(R, sample.bad(A, funds=[A["funds"][0]]), "add up to 60%")
        self.refused(R, sample.bad(A, employer="Invented Corp"), "employer")
        self.refused(R, sample.bad(A, gross_monthly_income="R 99 000.00"), "income")
        self.refused(R, sample.bad(A, client_email="other@example.invalid"), "not in the Fact Find Summary")
        self.refused(R, sample.bad(A, email_source="other"), "email_note")
        self.refused(R, sample.bad(A, owner_is_child=True), "child")
        self.refused(R, sample.bad(A, plan_type="lump_sum"), "MONTHLY")
        self.refused(R, sample.bad(A, owner_age=17), "child")
        self.refused(R, sample.bad(A, **{"start_date_choice.paul_said": ""}), "start_date_choice")
        self.refused(R, sample.bad(A, start_date="02/12/2026"), "start date")
        self.refused(R, sample.bad(A, ffs_risk_profile="Aggressive"), "conflict")
        self.refused(R, sample.bad(A, meetings_held=["10/11/2026"]), "future")
        self.refused(R, sample.bad(A, **{"next_meeting.date": "01/11/2026"}), "past")
        self.refused(R, sample.bad(A, **{"next_meeting.time": "5"}), "time like 5pm")
        self.refused(R, sample.bad(A, **{"fund_sheets.Sample Growth Fund": sample.DELETE}), "fund_sheets")
        self.refused(R, sample.bad(A, conflicts=[{"what": "income"}]), "conflict")
        self.refused(R, sample.bad(A, client_first_name="Robin", client_surname="Testcase"), "not the client Paul named")
        self.refused(R, sample.bad(A, **{"sources.risk": ""}), "sources.risk")
        self.refused(R, sample.bad(A, owner_full_name="Patricia Beth Samplecase"), "plan owner")
        run("run.py", "done", R, "answers", expect=3)

        # ---- good answers; Paul's yes
        run("run.py", "answers", R, "--file", self.afile(A))
        run("run.py", "done", R, "answers")
        run("run.py", "approve", R, "--said", "yes", expect="refused")                     # not shown yet
        run("run.py", "build", R, expect="refused")                                         # no yes yet
        out = run("run.py", "show", R)
        for frag in ("Total ongoing fees", "1.583% p.a.", "Subject", "Teams message to Sitamah", "<greeting by the clock>", "Are these answers right", "Thursday, 29/10/2026 & Monday, 02/11/2026",
                     "Start date (Paul always confirms it)"):
            self.assertIn(frag, out)
        run("run.py", "approve", R, "--said", "Yes, those are right")
        changed = sample.bad(A, flags=A["flags"] + ["The quote expires on 30/11/2026."])
        run("run.py", "answers", R, "--file", self.afile(changed))                         # a changed answer voids the yes
        run("run.py", "build", R, expect="refused")
        run("run.py", "show", R)
        run("run.py", "approve", R, "--said", "Yes, those are right")
        run("run.py", "done", R, "confirm")

        # ---- the build
        out = run("run.py", "build", R)
        name = "Pat_Samplecase_OM_TaxFree_Proposal_Email - 05.11.26.html"
        full, saved, body = (self.read(os.path.join(R, "out", name)), self.read(os.path.join(R, "out", "saved", name)), self.read(os.path.join(R, "out", "draft_body.html")))
        self.assertIn("data:image/png;base64,", full)
        self.assertNotIn("data:image", saved)
        self.assertNotIn("Kind regards", body)
        self.assertNotIn("Importance:", body)
        for frag in ("Sent:</td><td style=\"font-size:12pt;\">Thursday, 05/11/2026 10:15", "Sitamah Nathoo", "Patricia Anne Samplecase / Old Mutual Tax Free Investment Proposal \u2013 R 2,500.00 p.m.",
                     "You work at Sample Holdings in the position of Analyst.", "Thursday, 29/10/2026 &amp; Monday, 02/11/2026", "Thursday, 12/11/2026 @ 5pm", "where you can contribute R 2,500.00 p.m.",
                     "The funds that are recommended are as follows", "1.583% p.a.", "R 46,000.00", "R 500,000.00", "taxed at 40%"):
            self.assertIn(frag, full, frag)
        self.assertEqual(len(re.findall(r"\[[A-Z][A-Z0-9 %().,/&#-]*\]", full)), 0)
        run("run.py", "done", R, "build")

        # ---- save: never overwrite without a yes
        run("run.py", "name", R, "--existing", "x.html;" + name, expect=5)
        run("run.py", "name", R, "--existing", "x.html;" + name, "--overwrite-yes", "Yes, replace it")
        run("run.py", "access", R, "--purpose", "save", "--route", "device", "--result", "found")
        size = os.path.getsize(os.path.join(R, "out", "saved", name))
        run("run.py", "receipt", R, "save.folder", "C:\\Clients\\Samplecase, Pat (CL)\\%s\\Comparative Quotes" % sample.FOLDER)
        run("run.py", "receipt", R, "save.listed_bytes", str(size + 1))
        run("run.py", "done", R, "save", expect=3)                                          # the listed size does not match
        run("run.py", "name", R, "--existing", "x.html")
        run("run.py", "receipt", R, "save.listed_bytes", str(size))
        run("run.py", "done", R, "save")

        # ---- the Outlook draft: refused for every fault; no message before a checked draft
        import tfi
        subj = tfi.subject(A)
        run("run.py", "message", R, "--used-today", "no", expect="refused")
        faults = {"a second signature": dict(signature=sample.SIGNATURE + "<p>Kind regards,</p>"), "no signature": dict(signature=""), "a wrong Cc": dict(cc="someone@example.invalid"),
                  "a wrong subject": dict(subject=subj.replace("\u2013", "-")), "low importance": dict(importance="normal"),
                  "a placeholder": dict(content=lambda c: c.replace("Dear Pat,", "Dear [CLIENT FIRST NAME],")),
                  "an unclosed table": dict(content=lambda c: c.replace("</table>", "", 1)),
                  "a missing fund": dict(content=lambda c: c.replace("Sample Growth Fund", "Another Fund")),
                  "a Loop box": dict(content=lambda c: c + "<div>Loop component</div>")}
        for label, v in faults.items():
            bad_rb = self.tfile(sample.draft_json(A, body, subj, **v), "bad-draft.json")
            out = run("run.py", "draft", R, "--file", bad_rb, expect=5)
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
        self.assertIn(tfi.SITAMAH_CHAT, out)
        qn = tfi.quote_name(self.load(os.path.join(R, "docs.json")))
        for label, v in {"a wrong greeting": dict(greeting="Good afternoon"), "a literal ** ": dict(html=lambda h: h.replace("<strong>Action needed:</strong>", "**Action needed:**")),
                         "no numbered list": dict(html=lambda h: h.replace("<ol>", "<ul>").replace("</ol>", "</ul>")),
                         "a do-not-send line": dict(html=lambda h: h + "<p>Please do not send it.</p>")}.items():
            g = v.pop("greeting", "Good morning")
            out = run("run.py", "messagecheck", R, "--file", self.tfile(sample.message_json(A, qn, g, **v), "bad-msg.json"), expect=5)
            self.assertIn(BAD, out, label)
        run("run.py", "messagecheck", R, "--file", self.tfile(sample.message_json(A, qn, "Good morning"), "good-msg.json"))
        run("run.py", "receipt", R, "message.chat", "19:someone-else@unq.gbl.spaces")
        run("run.py", "receipt", R, "message.format", "markdown")
        run("run.py", "done", R, "message", expect=3)                                       # the wrong chat
        run("run.py", "receipt", R, "message.chat", tfi.SITAMAH_CHAT)
        run("run.py", "done", R, "message")

        # ---- the final audit: short, all ticks
        out = run("run.py", "done", R, "final")
        self.assertIn("RESULT: PASS", out)
        self.assertFalse([ln for ln in out.splitlines() if ln.startswith(BAD)])
        self.assertLessEqual(len([ln for ln in out.splitlines() if ln.startswith(OK)]), 16)
        self.assertTrue(os.path.exists(os.path.join(R, "out_record", "audit-full.txt")))
        self.assertIn("Only attested", out)
        out = run("verify.py", R)
        self.assertIn("RESULT: PASS", out)
        with open(os.path.join(R, "out", "saved", name), "a", encoding="utf-8") as f:       # a hand-edited saved copy is caught
            f.write("<!-- edited by hand -->")
        out = run("verify.py", R, expect=1)
        self.assertIn(BAD, out)
        self.assertIn("RESULT: FAIL", out)

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


if __name__ == "__main__":
    unittest.main()
