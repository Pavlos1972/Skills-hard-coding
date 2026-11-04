"""The ONE test of the om-optimal-ra-proposal skill (Operation Skill Restructure: one end-to-end test on invented data).

It plays whole jobs through the program exactly as a chat would, on invented documents (Pat Samplecase, an invented quote, Fact Find Summary, Astute report, fund
statement, RGAR and Lump Sum Quote), with today and the clock fixed by WR_TODAY and WR_NOW. The Tax Reform Tool is run for real in LibreOffice (about 10 seconds a
run). Nothing is saved or sent anywhere: the folder listing, the Outlook read-back and the posted Teams message are typed in as files. It proves:
  1. the driver refuses to skip a step, the routes must be tried in order, the required documents can never be missing and every optional document is registered or
     accounted for with Paul's words;
  2. bad answers are refused (nothing saved): a figure, fund, allocation, fee, date, name, employer, income or email that is not in the right document; allocations
     that do not add up; a client with both a pension and a provident fund; an existing RA that is not in the Astute report; a wrong replace-or-keep; a conflict; a
     missing source; dates in the wrong place;
  3. the tax tool is run by the program, every figure equals the independent recomputation, the audit checks hold and the two edge-case checks are flagged with both
     figures; a changed answer voids the tool results and Paul's yes; nothing is built before his yes;
  4. the email the program builds has no placeholder, computed weekdays, the tool's figures and bar chart, the right fund label, the fees added up, the 4 standard
     attachments and never the RGAR, the logo only in the full copy, and a body for the Outlook draft with no header and no signature;
  5. the save never overwrites without a yes, the draft read-back is refused for every fault, Sitamah is messaged only after a checked draft with the greeting from the
     clock, and the posted message must read back right in the 1:1 chat as markdown;
  6. the final audit is short and every line is a green tick; a hand-edited saved copy and a hand-edited tool result are caught;
  7. the separate Lump Sum Investment email (Section 14 and voluntary) has its own run, no tax tables, the verbatim sentences and a stop for a voluntary lump sum with
     no tax note from Paul; and a set of small model-level checks (no fund, no RA, no RGAR, provident, replace, three funds, a maximised Table 3, stale results, the tax year).
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from decimal import Decimal

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
        assert r.returncode == expect, "%s %s -> exit %d (wanted %d)\n%s\n%s" % (script, args, r.returncode, expect, r.stdout[-2400:], r.stderr[-800:])
    return r.stdout + r.stderr


class Journey(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="wr-optra-test-")
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
        for _ in range(30):
            out = run("run.py", "read", R)
            seen.append(out)
            m = re.search(r"--ack ([a-z_0-9]+:\d+)", out)
            if not m:
                break
            run("run.py", "read", R, "--ack", m.group(1), "--note", "read " + m.group(1))
        run("run.py", "done", R, "read")
        return "\n".join(seen)

    def register(self, R, roles, missing=None):
        run("run.py", "access", R, "--purpose", "locate", "--route", "device", "--result", "found", "--note", "test")
        for role in roles:
            run("run.py", "doc", R, "--role", role, "--file", self.docs[role], "--route", "device")
        for role, said in (missing or {}).items():
            run("run.py", "doc", R, "--missing", role, "--said", said)

    def test_whole_journey(self):
        self.main_case()
        self.lump_case()
        self.small_cases()

    # ------------------------------------------------------------------ the main proposal, with the real tool
    def main_case(self):
        import ori
        A = sample.answers()
        R0 = os.path.join(self.d, "order-test")
        run("run.py", "start", R0, "--client", "Pat", expect="refused")
        out = run("run.py", "start", R0, "--client", "Pat Samplecase")
        self.assertIn("Using om-optimal-ra-proposal, last updated", out)
        self.assertIn("[OK] LibreOffice", out)
        run("run.py", "done", R0, "answers", expect="refused")
        run("run.py", "doc", R0, "--role", "quote", "--file", self.docs["quote"], "--route", "device", expect="refused")                  # no access try logged
        run("run.py", "access", R0, "--purpose", "locate", "--route", "m365", "--result", "found")
        out = run("run.py", "doc", R0, "--role", "quote", "--file", self.docs["quote"], "--route", "m365", expect="refused")
        self.assertIn("in order", out)

        R = os.path.join(self.d, "run1")
        run("run.py", "start", R, "--client", "Pat Samplecase")
        run("run.py", "access", R, "--purpose", "locate", "--route", "device", "--result", "found", "--note", "test")
        run("run.py", "doc", R, "--role", "bogus", "--file", self.docs["quote"], "--route", "device", expect="refused")
        run("run.py", "doc", R, "--role", "lump_sum_quote", "--file", self.docs["lump_sum_quote"], "--route", "device", expect="refused")        # not a role of the main run
        run("run.py", "doc", R, "--missing", "quote", "--said", "there is none", expect="refused")                       # required documents can never be missing
        run("run.py", "doc", R, "--missing", "poi", "--said", "", expect="refused")                                       # Paul's words are needed
        for role in ("quote", "fact_find_summary", "booster_doc", "astute_ccp", "client_overview", "fund_statement", "rgar"):
            run("run.py", "doc", R, "--role", role, "--file", self.docs[role], "--route", "device")
        out = run("run.py", "done", R, "locate", expect=3)                                                                # the payslip is neither registered nor accounted for
        self.assertIn("poi", out)
        run("run.py", "doc", R, "--missing", "poi", "--said", "there is no payslip on file; the income is in the Fact Find Summary")
        run("run.py", "done", R, "locate")
        served = self.read_all(R)
        self.assertEqual(len(re.findall(r"- PAGE \d+ of \d+ -", served)), 9)

        # ---- bad answers are refused, nothing saved
        self.refused(R, sample.bad(A, proposed_premium="R 3 500.00"), "proposed premium")
        self.refused(R, sample.bad(A, start_date="02/12/2026"), "start date")
        self.refused(R, sample.bad(A, **{"funds.0.name": "Invented Fund"}), "fund in the quote")
        self.refused(R, sample.bad(A, **{"funds.1.allocation": "30"}), "add up to")
        self.refused(R, sample.bad(A, **{"funds.0.asset_mgmt_fee": "0.86%"}), "asset management fee")
        self.refused(R, sample.bad(A, net_admin_fee="3.5%"), "net administration fee")
        self.refused(R, sample.bad(A, adviser_charge="0.10%"), "adviser remuneration")
        self.refused(R, sample.bad(A, monthly_admin_fee="R 40.00"), "monthly fixed administration fee")
        self.refused(R, sample.bad(A, employer="Invented Corp"), "employer")
        self.refused(R, sample.bad(A, position="Invented Role"), "position")
        self.refused(R, sample.bad(A, gross_monthly_income="R 60 000.00"), "gross monthly income")
        self.refused(R, sample.bad(A, age=41), "age in the Fact Find Summary")
        self.refused(R, sample.bad(A, **{"fund.type": "both"}), "BOTH")
        self.refused(R, sample.bad(A, **{"fund.employer_monthly": "R 2 600.00"}), "employer contribution")
        self.refused(R, sample.bad(A, **{"fund.employer_pct": "6%"}), "employer contribution percentage")
        self.refused(R, sample.bad(A, **{"fund.value": "R 160 000.00"}), "fund value")
        self.refused(R, sample.bad(A, **{"fund.value_date": "01/10/2026"}), "fund value date")
        self.refused(R, sample.bad(A, **{"existing_ras.0.monthly": "R 1 600.00"}), "monthly contribution")
        self.refused(R, sample.bad(A, **{"existing_ras.0.policy_number": "SL-999999"}), "policy number")
        self.refused(R, sample.bad(A, **{"existing_ras.0.insurer": "Otherlife"}), "insurer")
        self.refused(R, sample.bad(A, ra_decision="none"), "ra_decision")
        self.refused(R, sample.bad(A, **{"rgar.shortfall": "R 4 300.00"}), "second shortfall")
        self.refused(R, sample.bad(A, **{"rgar.years": "25"}), "years to retirement")
        self.refused(R, sample.bad(A, lump_sum_applies=sample.DELETE), "lump_sum_applies")
        self.refused(R, sample.bad(A, client_email="other@example.invalid"), "not in the Fact Find Summary")
        self.refused(R, sample.bad(A, email_source="other"), "email_note")
        self.refused(R, sample.bad(A, conflicts=[{"what": "age"}]), "conflict")
        self.refused(R, sample.bad(A, meetings_held=["10/11/2026"]), "future")
        self.refused(R, sample.bad(A, **{"next_meeting.date": "01/11/2026"}), "past")
        self.refused(R, sample.bad(A, **{"next_meeting.time": "5"}), "time like 12pm")
        self.refused(R, sample.bad(A, client_first_name="Robin", client_surname="Testcase"), "not the client Paul named")
        self.refused(R, sample.bad(A, **{"sources.funds_fees": ""}), "sources.funds_fees")
        self.refused(R, sample.bad(A, client_full_name="Patricia Beth Samplecase"), "client name")
        self.refused(R, sample.bad(A, surprise=1), "unknown field")
        run("run.py", "done", R, "answers", expect=3)

        # ---- good answers, then the real Tax Reform Tool
        run("run.py", "answers", R, "--file", self.afile(A))
        run("run.py", "done", R, "answers")
        run("run.py", "show", R, expect="refused")                                          # no tool results yet
        run("run.py", "done", R, "tax", expect=3)
        out = run("run.py", "tax", R)
        for frag in ("TAX RESULTS", "LibreOffice", "Table 1 (now)", "Check 1:", "Check 8:", "FLAG for Paul: Table 2", "FLAG for Paul: Table 3", "known bracket edge case"):
            self.assertIn(frag, out)
        tax = self.load(os.path.join(R, "tax.json"))
        self.assertEqual(sorted(tax["runs"]), ["baseline", "t1", "t2", "t3"])
        for name, r in tax["runs"].items():
            self.assertEqual(r["problems"], [], name)                                       # the workbook equals the independent recomputation
        self.assertEqual(Decimal(tax["runs"]["t2"]["inputs"]["ra_monthly"]), Decimal("8187.5"))
        self.assertEqual(Decimal(tax["runs"]["t3"]["inputs"]["ra_monthly"]), Decimal("4500"))      # keep: the existing R 1 500 + the proposed R 3 000
        self.assertEqual(Decimal(tax["runs"]["t1"]["inputs"]["ra_monthly"]), Decimal("1500"))
        run("run.py", "done", R, "tax")

        # ---- Paul's yes
        run("run.py", "approve", R, "--said", "yes", expect="refused")                     # not shown yet
        run("run.py", "build", R, expect="refused")                                         # no yes yet
        out = run("run.py", "show", R)
        for frag in ("Table 3 (proposed)", "Subject", "Teams message to Sitamah", "<greeting by the clock>", "Are these answers right", "Thursday, 29/10/2026 & Monday, 02/11/2026",
                     "keep in force alongside it", "The saved copy has no logo.", "Table 2: the tool's own tax saved", "0.89%", "total 4.515%"):
            self.assertIn(frag, out)
        run("run.py", "approve", R, "--said", "Yes, those are right")
        changed = sample.bad(A, flags=A["flags"] + ["The quote expires on 30/11/2026, before the start date."])
        run("run.py", "answers", R, "--file", self.afile(changed))                         # a changed answer voids the yes AND the tool results
        self.assertFalse(os.path.exists(os.path.join(R, "tax.json")))
        run("run.py", "build", R, expect="refused")
        run("run.py", "tax", R)
        run("run.py", "done", R, "tax")
        run("run.py", "show", R)
        run("run.py", "approve", R, "--said", "Yes, those are right")
        run("run.py", "done", R, "confirm")
        tax = self.load(os.path.join(R, "tax.json"))

        # ---- the build
        run("run.py", "build", R)
        name = "Pat_Samplecase_OM_Optimal_RA_Proposal_Email - 05.11.26.html"
        full, saved, body = (self.read(os.path.join(R, "out", name)), self.read(os.path.join(R, "out", "saved", name)), self.read(os.path.join(R, "out", "draft_body.html")))
        self.assertIn("data:image/png;base64,", full)
        self.assertNotIn("data:image", saved)
        self.assertNotIn("Kind regards", body)
        self.assertNotIn("Importance:", body)
        self.assertEqual(len(re.findall(r"\[[A-Z][A-Z0-9 _%().,/&#-]*\]", re.sub(r"base64,[A-Za-z0-9+/=]+", "", full))), 0)
        pay = [ori.rand0(tax["runs"][k]["outputs"]["tax_payable"]) for k in ("t1", "t2", "t3")]
        for frag in ("Sent:</td><td style=\"font-size:12pt;\">Thursday, 05/11/2026 10:15", "Sitamah Nathoo", "Patricia Anne Samplecase / Old Mutual Retirement Annuity Proposal – R 3,000.00 p.m.",
                     "pat@example.invalid", "You are working at Sample Holdings in the position of Analyst.", "Thursday, 29/10/2026 &amp; Monday, 02/11/2026", "Thursday, 12/11/2026 @ 12pm",
                     "(Pension Fund and Retirement Annuity combined)", "R 14,437.50", "R 8,187.50", "Monthly Retirement Annuity Contribution (New OM Optimal RA)", "Samplelife, policy SL-123456",
                     "Tax Saved from Pension Fund Deduction", "0.89%", "4.515% p.a.", "R 36.50", "Sample Balanced Fund &amp; the Sample Growth Fund", "Sample Balanced Fund &amp; Sample Growth Fund",
                     "R 4,200.00", "over the next 24 years", "starting on: <strong>01/12/2026.</strong>", "Keep in force"):
            self.assertIn(frag, full, frag)
        for x in pay:
            self.assertIn("R &nbsp;%s</td>" % x, full)
        self.assertNotIn("Retirement Goal Analysis Report</td>", full)
        self.assertNotIn("5.&nbsp;", full)                                                   # four attachments, never an RGAR as a fifth
        run("run.py", "done", R, "build")

        # ---- save: the no-logo copy; never overwrite without a yes
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
        import oriemail as oe
        subj = ori.subject(A)
        run("run.py", "message", R, "--used-today", "no", expect="refused")
        faults = {"a second signature": dict(signature=sample.SIGNATURE + "<p>Kind regards,</p>"), "no signature": dict(signature=""), "a wrong Cc": dict(cc="someone@example.invalid"),
                  "a wrong subject": dict(subject="Pat Samplecase / RA"), "low importance": dict(importance="normal"),
                  "a placeholder": dict(content=lambda c: c.replace("Dear Pat,", "Dear [CLIENT FIRST NAME],")),
                  "BODY_PLACEHOLDER left": dict(content=lambda c: c + "<p>BODY_PLACEHOLDER</p>"),
                  "an unclosed table": dict(content=lambda c: c + "<table><tr><td>x</td></tr>"),
                  "a missing figure": dict(content=lambda c: c.replace("You have indicated that you are able to contribute", "You can contribute")),
                  "a wrong tax figure": dict(content=lambda c: c.replace("R &nbsp;%s</td>" % pay[2], "R &nbsp;1</td>").replace("R %s" % pay[2], "R 1")),
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
        self.assertIn(ori.SITAMAH_CHAT, out)
        self.assertIn("1. The OM Optimal RA Quote (%s)" % sample.NAMES["quote"][:-4], out)
        self.assertIn("3. The OM Optimal RA Booster Value document (%s)" % sample.NAMES["booster_doc"][:-4], out)
        self.assertNotIn("RGAR", out)
        for label, v in {"a wrong greeting": dict(greeting="Good afternoon"), "a literal **": dict(html=lambda h: h.replace("<strong>Action needed:</strong>", "**Action needed:**")),
                         "no numbered list": dict(html=lambda h: h.replace("<ol>", "<ul>").replace("</ol>", "</ul>")),
                         "a do-not-send line": dict(html=lambda h: h + "<p>Please do not send it.</p>"),
                         "the RGAR mentioned": dict(html=lambda h: h.replace("</ol>", "<li>The RGAR report</li></ol>"))}.items():
            g = v.pop("greeting", "Good morning")
            out = run("run.py", "messagecheck", R, "--file", self.tfile(sample.message_json(A, g, **v), "bad-msg.json"), expect=5)
            self.assertIn(BAD, out, label)
        run("run.py", "messagecheck", R, "--file", self.tfile(sample.message_json(A, "Good morning"), "good-msg.json"))
        run("run.py", "receipt", R, "message.chat", "19:someone-else@unq.gbl.spaces")
        run("run.py", "receipt", R, "message.format", "markdown")
        run("run.py", "done", R, "message", expect=3)                                       # the wrong chat
        run("run.py", "receipt", R, "message.chat", ori.SITAMAH_CHAT)
        run("run.py", "done", R, "message")

        # ---- the final audit: short, all ticks
        out = run("run.py", "done", R, "final")
        self.assertIn("RESULT: PASS", out)
        self.assertFalse([ln for ln in out.splitlines() if ln.startswith(BAD)])
        self.assertLessEqual(len([ln for ln in out.splitlines() if ln.startswith(OK)]), 40)
        for frag in ("Audit check 9", "Check 6:", "Only attested", "flag for Paul: Table 2", "SECOND shortfall"):
            self.assertIn(frag, out)
        self.assertTrue(os.path.exists(os.path.join(R, "out_record", "audit-full.txt")))
        out = run("verify.py", R)
        self.assertIn("RESULT: PASS", out)
        tp = os.path.join(R, "tax.json")                                                   # a hand-edited tool result is caught
        original = self.read(tp)
        edited = self.load(tp)
        edited["runs"]["t3"]["outputs"]["tax_payable"] = "1000"
        with open(tp, "w", encoding="utf-8") as f:
            json.dump(edited, f)
        out = run("verify.py", R, expect=1)
        self.assertIn(BAD, out)
        with open(tp, "w", encoding="utf-8") as f:
            f.write(original)
        with open(os.path.join(R, "out", "saved", name), "a", encoding="utf-8") as f:       # a hand-edited saved copy is caught
            f.write("<!-- edited by hand -->")
        out = run("verify.py", R, expect=1)
        self.assertIn(BAD, out)
        self.assertIn("RESULT: FAIL", out)

    # ------------------------------------------------------------------ the separate Lump Sum Investment email
    def lump_case(self):
        import ori
        L = sample.lump_answers()
        R = os.path.join(self.d, "run-lump")
        out = run("run.py", "start", R, "--client", "Pat Samplecase", "--document", "lump_sum")
        self.assertNotIn("[OK] LibreOffice", out)                                                # the tool is not used for this email
        run("run.py", "access", R, "--purpose", "locate", "--route", "device", "--result", "found", "--note", "test")
        run("run.py", "doc", R, "--role", "quote", "--file", self.docs["quote"], "--route", "device", expect="refused")        # the Plan 1 quote is not a role here
        for role in ("lump_sum_quote", "fact_find_summary", "client_overview"):
            run("run.py", "doc", R, "--role", role, "--file", self.docs[role], "--route", "device")
        run("run.py", "doc", R, "--missing", "astute_ccp", "--said", "Paul: the Client Overview shows everything; no Astute report this time")
        run("run.py", "done", R, "locate")
        self.read_all(R)
        self.refused(R, sample.bad(L, **{"lump.amount": "R 130 000.00"}), "sum of the source policies")
        self.refused(R, sample.bad(L, **{"lump.policies.0.net_value": "R 125 000.00"}), "net fund value")      # the gross value is in the text but not next to the label
        self.refused(R, sample.bad(L, **{"lump.policies.0.name": "Invented Preservation Fund"}), "source policy name")
        self.refused(R, sample.bad(L, **{"lump.type": "unknown"}), "section14")
        self.refused(R, sample.bad(L, lump={"type": "voluntary", "amount": "R 120 000.00", "source_of_funds": "savings", "tax_note": ""}), "no approved tax-treatment wording")
        self.refused(R, sample.bad(L, **{"funds.0.name": "Invented Fund"}), "fund in the Lump Sum Quote")
        self.refused(R, sample.bad(L, **{"ls_fees.admin_fee": "1.20%"}), "ls_fees.admin_fee")
        self.refused(R, sample.bad(L, start_date="02/12/2026"), "start date")
        self.refused(R, sample.bad(L, document="main"), "document must be")
        run("run.py", "answers", R, "--file", self.afile(L))
        run("run.py", "done", R, "answers")
        out = run("run.py", "tax", R, expect="refused")
        self.assertIn("no tax tables", out)
        run("run.py", "done", R, "tax")
        out = run("run.py", "show", R)
        for frag in ("Section 14 from Sample Preservation Fund (net R 120,000.00)", "Lump Sum Investment (R 120,000.00)", "Lump Sum Quote (attachment 1)", "fact sheet(s)"):
            self.assertIn(frag, out)
        run("run.py", "approve", R, "--said", "Yes")
        run("run.py", "done", R, "confirm")
        run("run.py", "build", R)
        name = "Pat_Samplecase_OM_Optimal_RA_LumpSum_Proposal_Email - 05.11.26.html"
        full = self.read(os.path.join(R, "out", name))
        body = self.read(os.path.join(R, "out", "draft_body.html"))
        for frag in ("A lump sum amount of R 120,000.00 will be transferred into your new OM Optimal RA via a Section 14 transfer from your existing Sample Preservation Fund policy/policies. "
                     "This is a tax-neutral transfer between approved retirement funds and does not attract any tax at the point of transfer.", "Optimal Investment Plan 2 (Lump Sum)", "Sample Cash Fund",
                     "100%", "Administration fee", "0.90%", "As-and-when advice fee", "None", "Your Lump Sum Investment:", "01/12/2026"):
            self.assertIn(frag, full, frag)
        for frag in ("Maximum Deduction", "Retirement Goal", "RE-INVESTING", "Booster"):
            self.assertNotIn(frag, full)
        self.assertNotIn("Kind regards", body)
        run("run.py", "done", R, "build")
        run("run.py", "name", R, "--existing", "")
        run("run.py", "access", R, "--purpose", "save", "--route", "device", "--result", "found")
        run("run.py", "receipt", R, "save.folder", "C:\\Clients\\Samplecase, Pat (CL)\\%s\\Comparative Quotes" % sample.FOLDER)
        run("run.py", "receipt", R, "save.listed_bytes", str(os.path.getsize(os.path.join(R, "out", "saved", name))))
        run("run.py", "done", R, "save")
        subj = ori.subject(L)
        self.assertEqual(subj, "Patricia Anne Samplecase / Old Mutual Retirement Annuity – Lump Sum Investment (R 120,000.00)")
        run("run.py", "draft", R, "--file", self.tfile(sample.draft_json(L, body, subj), "good-draft2.json"))
        run("run.py", "receipt", R, "draft.tab_closed", "yes")
        run("run.py", "receipt", R, "draft.stray_deleted", "1")
        run("run.py", "done", R, "draft")
        out = run("run.py", "message", R, "--used-today", "no")
        self.assertIn("1. The OM Optimal RA Lump Sum Quote (%s)" % sample.NAMES["lump_sum_quote"][:-4], out)
        self.assertIn("Both are in Pat's folder", out)
        run("run.py", "messagecheck", R, "--file", self.tfile(sample.message_json(L, "Good morning"), "good-msg2.json"))
        run("run.py", "receipt", R, "message.chat", ori.SITAMAH_CHAT)
        run("run.py", "receipt", R, "message.format", "markdown")
        run("run.py", "done", R, "message")
        out = run("run.py", "done", R, "final")
        self.assertIn("RESULT: PASS", out)
        self.assertIn("The lump sum email has no tax tables", out)
        self.assertFalse([ln for ln in out.splitlines() if ln.startswith(BAD)])

    # ------------------------------------------------------------------ small model-level checks (the tool's results are the program's own recomputation here)
    def small_cases(self):
        import ori
        import oriemail as oe
        import oritax as ot
        import taxtool as tt
        import wrlib as w
        import docread
        evs = {r: docread.Evidence(docread.read_document(p)) for r, p in self.docs.items()}
        registry = {"docs": {r: {"name": os.path.basename(p)} for r, p in self.docs.items()}, "missing": {}}
        today = w.parse_date("05/11/2026")
        sent = "Thursday, 05/11/2026 10:15"

        def built(a, tax=None):
            tax = tax or sample.fake_tax(a)
            full, nologo, body = oe.build_all(a, sent, registry, tax)
            res = oe.html_problems(full, nologo, body, a, sent, registry, tax)
            self.assertEqual([r for r in res if not r[0]], [], [r[1] for r in res if not r[0]])
            rows, flags = ot.audit(a, tax)
            self.assertEqual([r[1] for r in rows if not r[0]], [])
            return oe.text_of(body), full, tax, flags
        A = sample.answers()
        self.assertEqual(ori.pct_decimal("0.575%"), Decimal("0.575"))
        self.assertEqual(ori.pct_decimal("7,5 %"), Decimal("7.5"))
        self.assertIsNone(ori.pct_decimal("R 5"))
        # ---- keep: the existing policy is named in the personal table, Table 1 and Table 3
        bt, full, tax, flags = built(A)
        self.assertEqual(bt.count("SL-123456"), 3)
        self.assertEqual(len(flags), 2)
        # ---- replace: the existing policy is not in Table 3; recommendation says so
        bt, full, tax, flags = built(sample.bad(A, ra_decision="replace"))
        self.assertEqual(bt.count("SL-123456"), 2)
        self.assertIn("Replace with OM Optimal RA", bt)
        # ---- provident, no existing RA, no RGAR, a penalty note, three funds
        P = sample.bad(A, **{"fund.type": "provident", "existing_ras": [], "ra_decision": "none", "rgar": None})
        P["funds"] = [{"name": "Fund One", "allocation": "50", "asset_mgmt_fee": "0.80%"}, {"name": "Fund Two", "allocation": "30", "asset_mgmt_fee": "0.90%"}, {"name": "Fund Three", "allocation": "20", "asset_mgmt_fee": "1.00%"}]
        bt, full, tax, flags = built(P)
        for frag in ("You have no active or Paid-Up Retirement Annuities.", "You did not request for a Retirement Goal Analysis Report.", "(Provident Fund and Retirement Annuity combined)",
                     "Tax Saved from Provident Fund Deduction", "Employer Provident Fund Contribution", "The funds that are recommended are the Fund One, the Fund Two & the Fund Three (See attached).",
                     "Old Mutual Fund Fact Sheets (Fund One, Fund Two & Fund Three)", "0.87%"):
            self.assertIn(frag, bt, frag)
        self.assertNotIn("Pension Fund", bt)
        self.assertNotIn("SL-123456", bt)
        self.assertEqual(oe.text_of(oe.pension_block(P)).count("Provident"), 1)
        self.assertEqual(ori.fee_shown(ori.blended_fee(P)), "0.87")
        # ---- self-employed: no fund rows and no fund tax line; the sentence says Retirement Annuity only
        S = sample.bad(P, fund={"type": "none"})
        bt, full, tax, flags = built(S)
        self.assertIn("You have no Pension or Provident Fund with your employer.", bt)
        self.assertIn("towards a Retirement Annuity to take full advantage", bt)
        self.assertNotIn("Contribution (Samplelife", bt)
        self.assertNotIn("Tax Saved from", bt.replace("Annual Tax Saved from RA Deduction", ""))
        self.assertNotIn("Employer Pension Fund", bt)
        # ---- a penalty note, and a Table 3 that uses the whole deduction says so
        N = sample.bad(A, **{"existing_ras.0.no_penalties": True, "proposed_premium": "R 9 000.00"})
        bt, full, tax, flags = built(N)
        self.assertIn("No penalties apply – policy is too new", bt)
        self.assertEqual(bt.count("You have maximised your deductions and cannot make any more tax savings."), 2)           # Tables 2 and 3
        self.assertTrue([f for f in flags if "not tax-deductible" in f])
        # ---- the tool results must belong to these answers; the audit catches a broken figure
        T = sample.fake_tax(A)
        self.assertEqual(ot.stale_problems(A, T, today), [])
        self.assertTrue(ot.stale_problems(sample.bad(A, proposed_premium="R 3 200.00"), T, today))
        self.assertTrue(ot.stale_problems(sample.bad(A, **{"fund.type": "provident"}), T, today))
        T2 = sample.fake_tax(A)
        T2["runs"]["t1"]["outputs"]["cap"] = "170000"
        self.assertTrue([r for r in ot.audit(A, T2)[0] if not r[0]])
        T3 = sample.fake_tax(A)
        T3["runs"]["t3"]["bars"][0] = "1"
        self.assertTrue([r for r in ot.audit(A, T3)[0] if not r[0]])                         # check 8
        T4 = sample.fake_tax(A)
        T4["runs"]["t2"]["problems"] = ["cap: the workbook says 1, the tax facts say 2"]
        self.assertTrue([p for p in ot.stale_problems(A, T4, today) if "disagree" in p])
        # ---- the tax year: valid until 28/02/2027, then the program stops
        self.assertIsNone(tt.tax_year_problem(date(2027, 2, 28)))
        self.assertIn("STOP", tt.tax_year_problem(date(2027, 3, 1)))
        self.assertTrue([p for p in ori.answers_problems(A, evs, registry, date(2027, 3, 1), "Pat Samplecase", "main") if "tables" in p])
        # ---- the independent recomputation agrees with a hand calculation (pension: R50,000 a month, 5% employer + 7.5% member, no RA)
        ind = tt.independent({"remuneration": "50000", "age": 40, "switch": "pension", "employer_pension": "0.05", "member_pension": "0.075", "employer_provident": 0, "member_provident": 0, "ra_monthly": 0})
        self.assertEqual(ind["cap"], Decimal("173250"))
        self.assertEqual(ind["additional_monthly"], Decimal("8187.5"))
        # ---- a voluntary lump sum with Paul's tax note builds; Section 14 and voluntary use their verbatim sentences
        V = sample.bad(sample.lump_answers(), lump={"type": "voluntary", "amount": "R 120 000.00", "source_of_funds": "savings from a bonus", "tax_note": "Paul: this is after-tax money and gets no extra deduction."})
        self.assertEqual(ori.answers_problems(V, evs, registry, today, "Pat Samplecase", "lump_sum"), [])
        full, nologo, body = oe.build_all(V, sent, registry, None)
        self.assertIn("A lump sum amount of R 120,000.00 will be invested into your new OM Optimal RA from your own savings (savings from a bonus).", oe.text_of(body))
        self.assertIn("Paul: this is after-tax money and gets no extra deduction.", oe.text_of(body))
        self.assertEqual([r for r in oe.html_problems(full, nologo, body, V, sent, registry, None) if not r[0]], [])


if __name__ == "__main__":
    unittest.main()
