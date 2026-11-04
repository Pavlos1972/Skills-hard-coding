"""The ONE test of the investment-comparisons-skill (Operation Skill Restructure: one end-to-end test on invented data).

It plays whole jobs through the program exactly as a chat would, on invented documents (Pat Samplecase, the invented providers Samplelife and Testco, invented quotes, fund
fact sheets saved as text, a supplementary document), with today and the clock fixed by WR_TODAY and WR_NOW. Nothing is saved or sent anywhere: the folder listing, the
Outlook read-back and the posted Teams message are typed in as files. It proves:
  1. the driver refuses to skip a step, the routes must be tried in order (the computer, Microsoft 365, Zapier for the files; the web, Chrome for the fact sheets), the quotes
     can never be missing, the funds must be named and each needs its fact sheet (saved text with its address and date) or Paul's words;
  2. bad answers are refused (nothing saved): a premium, term, fee, fund, allocation, loyalty figure, fund-sheet figure or date that is not in the right document; allocations
     that do not add up; a blended or total fee line; a quote that is not the product compared; a description copied from the fact sheet; a missing loyalty explanation; a
     risk profile or email not in the Fact Find; supplementary differences not in the documents; a conflict; dates in the wrong place;
  3. the comparison is worked out by the program (apples-to-apples, fee totals added up as shown, stale and missing fact sheets, the Tax-Free room, risk fit flags); a changed
     answer voids the check and Paul's yes; nothing is built before his yes; when the quotes do not match the question asks him and the email labels the mismatch;
  4. the email has the four tables in the fixed order with an intro line each, no EAC headline, every industry term explained, every fund dated, the 'Things to know' box only
     when due, the optional parts only when asked, the logo only in the full copy, and a body for the Outlook draft with no header and no signature;
  5. the save never overwrites without a yes, the draft read-back is refused for every fault, Sitamah is messaged only after a checked draft, and the posted message must read
     back right in the 1:1 chat as markdown;
  6. the final audit is short and every line is a green tick; a hand-edited saved copy and a hand-edited fact sheet are caught;
  7. small model-level checks: the Tax-Free room and the unconfirmed limits stop, an endowment tax note stops, a stale and a missing fact sheet, the jargon and EAC checks.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
SCRIPTS = os.path.join(SKILL, "scripts")
sys.path.insert(0, SCRIPTS)
sys.path.insert(0, HERE)
import sample  # noqa: E402

OK, BAD = "\u2705", "\u274c"
URL = "https://example.invalid/factsheet"


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
        self.d = tempfile.mkdtemp(prefix="wr-inv-test-")
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
        for _ in range(40):
            out = run("run.py", "read", R)
            seen.append(out)
            m = re.search(r"--ack ([a-z_0-9]+:\d+)", out)
            if not m:
                break
            run("run.py", "read", R, "--ack", m.group(1), "--note", "read " + m.group(1))
        run("run.py", "done", R, "read")
        return "\n".join(seen)

    def register(self, R, files=None, funds=None, sheets=True):
        files = files or self.docs
        run("run.py", "access", R, "--purpose", "locate", "--route", "device", "--result", "found", "--note", "test")
        run("run.py", "doc", R, "--role", "quote", "--label", "Samplelife", "--file", files["quote_samplelife"], "--route", "device")
        run("run.py", "doc", R, "--role", "quote", "--label", "Testco", "--file", files["quote_testco"], "--route", "device")
        run("run.py", "doc", R, "--role", "fact_find", "--file", files["fact_find"], "--route", "device")
        run("run.py", "doc", R, "--role", "supplement", "--label", "Testco Booster Illustrator", "--file", files["supplement_testco_booster_illustrator"], "--route", "device")
        run("run.py", "funds", R, "--file", self.afile(funds or sample.FUNDS, "funds.json"))
        if sheets:
            run("run.py", "access", R, "--purpose", "factsheet", "--route", "web", "--result", "found", "--note", "test")
            for lab in sample.SHEETS:
                import icmp
                run("run.py", "doc", R, "--role", "factsheet", "--label", lab, "--file", files[icmp.dkey("factsheet", lab)], "--route", "web", "--url", URL, "--fetched-at", "04/11/2026")

    def test_whole_journey(self):
        self.main_case()
        self.mismatch_case()
        self.small_cases()

    # ------------------------------------------------------------------ the whole job
    def main_case(self):
        import icmp
        A = sample.answers()
        R0 = os.path.join(self.d, "order-test")
        run("run.py", "start", R0, "--client", "Pat", expect="refused")
        out = run("run.py", "start", R0, "--client", "Pat Samplecase")
        self.assertIn("Using investment-comparisons-skill, last updated", out)
        run("run.py", "done", R0, "answers", expect="refused")
        run("run.py", "doc", R0, "--role", "quote", "--label", "Samplelife", "--file", self.docs["quote_samplelife"], "--route", "device", expect="refused")      # no access try logged
        run("run.py", "access", R0, "--purpose", "locate", "--route", "m365", "--result", "found")
        out = run("run.py", "doc", R0, "--role", "quote", "--label", "Samplelife", "--file", self.docs["quote_samplelife"], "--route", "m365", expect="refused")
        self.assertIn("in order", out)
        run("run.py", "access", R0, "--purpose", "factsheet", "--route", "chrome", "--result", "found")
        out = run("run.py", "doc", R0, "--role", "factsheet", "--label", "X - Y", "--file", self.docs["factsheet_samplelife_sample_balanced_fund"], "--route", "chrome", "--url", URL, "--fetched-at", "04/11/2026", expect="refused")
        self.assertIn("in order", out)                                                                                                                  # chrome before the web failed

        R = os.path.join(self.d, "run1")
        run("run.py", "start", R, "--client", "Pat Samplecase")
        run("run.py", "access", R, "--purpose", "locate", "--route", "device", "--result", "found", "--note", "test")
        run("run.py", "doc", R, "--role", "bogus", "--file", self.docs["quote_samplelife"], "--route", "device", expect="refused")
        run("run.py", "doc", R, "--role", "quote", "--file", self.docs["quote_samplelife"], "--route", "device", expect="refused")                   # a quote needs its provider's name as label
        run("run.py", "doc", R, "--missing", "quote", "--label", "Samplelife", "--said", "there is none", expect="refused")                          # quotes can never be missing
        run("run.py", "doc", R, "--role", "quote", "--label", "Samplelife", "--file", self.docs["quote_samplelife"], "--route", "device")
        out = run("run.py", "done", R, "locate", expect=3)                                                                                            # one quote only, no funds, no Fact Find
        self.assertIn("quote(s) registered", out)
        run("run.py", "doc", R, "--role", "quote", "--label", "Testco", "--file", self.docs["quote_testco"], "--route", "device")
        run("run.py", "doc", R, "--role", "fact_find", "--file", self.docs["fact_find"], "--route", "device")
        run("run.py", "doc", R, "--role", "supplement", "--label", "Testco Booster Illustrator", "--file", self.docs["supplement_testco_booster_illustrator"], "--route", "device")
        out = run("run.py", "done", R, "locate", expect=3)
        self.assertIn("no funds declared", out)
        run("run.py", "funds", R, "--file", self.afile([{"provider": "Samplelife", "name": "Invented Fund"}], "bad-funds.json"), expect="refused")          # not in the quote
        run("run.py", "funds", R, "--file", self.afile([{"provider": "Nobody", "name": "Sample Balanced Fund"}], "bad-funds.json"), expect="refused")      # no such quote
        out = run("run.py", "funds", R, "--file", self.afile(sample.FUNDS, "funds.json"))
        self.assertIn("Samplelife - Sample Balanced Fund", out)
        sheet = [self.docs[icmp.dkey("factsheet", "Samplelife - Sample Balanced Fund")], "Samplelife - Sample Balanced Fund"]
        run("run.py", "doc", R, "--role", "factsheet", "--label", sheet[1], "--file", sheet[0], "--route", "web", "--url", URL, "--fetched-at", "04/11/2026", expect="refused")   # no web try logged
        run("run.py", "access", R, "--purpose", "factsheet", "--route", "web", "--result", "found")
        run("run.py", "doc", R, "--role", "factsheet", "--label", sheet[1], "--file", sheet[0], "--route", "device", "--url", URL, "--fetched-at", "04/11/2026", expect="refused")  # wrong route for a fact sheet
        run("run.py", "doc", R, "--role", "factsheet", "--label", sheet[1], "--file", sheet[0], "--route", "web", expect="refused")                                              # no address or date
        run("run.py", "doc", R, "--role", "factsheet", "--label", "Samplelife - Invented Fund", "--file", sheet[0], "--route", "web", "--url", URL, "--fetched-at", "04/11/2026", expect="refused")
        run("run.py", "doc", R, "--role", "factsheet", "--label", sheet[1], "--file", sheet[0], "--route", "web", "--url", URL, "--fetched-at", "04/11/2026")
        out = run("run.py", "done", R, "locate", expect=3)                                                                                            # two sheets still missing
        self.assertIn("no fact sheet", out)
        for lab in ("Samplelife - Sample Growth Fund", "Testco - Test Cautious Fund"):
            run("run.py", "doc", R, "--role", "factsheet", "--label", lab, "--file", self.docs[icmp.dkey("factsheet", lab)], "--route", "web", "--url", URL, "--fetched-at", "04/11/2026")
        run("run.py", "done", R, "locate")
        served = self.read_all(R)
        self.assertEqual(len(re.findall(r"- PAGE \d+ of \d+ -", served)), 8)

        # ---- bad answers are refused, nothing saved
        for path, val, frag in (("providers.0.contribution", "R 3 500.00", "contribution in the quote"), ("providers.0.escalation", "12%", "yearly increase in the quote"),
                                ("providers.0.term", "Retirement age 70", "term or retirement age in the quote"), ("providers.0.product_name", "Invented Plan", "product name in the quote"),
                                ("providers.0.funds.0.name", "Invented Fund", "fund in the Samplelife quote"), ("providers.0.funds.1.allocation", "30", "add up to"),
                                ("providers.0.funds.0.asset_mgmt_fee", "0.86%", "asset management fee of Sample Balanced Fund"), ("providers.0.fee_lines.0.pct", "1.5%", "Net administration fee in the quote"),
                                ("providers.0.fee_lines.0.label", "Invented fee", "fee label"), ("providers.0.loyalty.0.percentages", ["2.5%", "3.5%"], "percentage in the Samplelife quote"),
                                ("providers.0.loyalty.0.guaranteed", "maybe", "guaranteed must be"), ("providers.1.performance_fees.0.fund", "Invented Fund", "not on this quote"),
                                ("providers.0.initial_fees.0.value", "4.00%", "initial fee"), ("providers.1.initial_fees.0.value", "R 99.00", "initial fee"),
                                ("product_type", "Endowment", "never compare different product types"), ("fund_sheets.0.perf_1y", "8.9%", "1 year performance"),
                                ("fund_sheets.0.as_at", "01/10/2026", "fact sheet date"), ("fund_sheets.0.benchmark", "Invented benchmark", "benchmark"),
                                ("fund_sheets.0.description", "The fund spreads money between shares, bonds, property and cash.", "repeats 8 or more words"),
                                ("fund_sheets.0.description", "word " * 30, "25 words or fewer"), ("fund_sheets.0.risk_label", "Speculative", "risk label"),
                                ("risk_profile", "Aggressive", "risk profile in the Fact Find"), ("client_email", "other@example.invalid", "not in the Fact Find"), ("email_source", "other", "email_note"),
                                ("supplement_checks", {"Testco Booster Illustrator": [{"provider": "Testco", "field": "Wealth Bonus", "quote_value": "2.0%", "supplement_value": "9.99%", "supplement_date": "06/07/2026"}]},
                                 "not in the text of the supplementary document"),
                                ("supplement_checks", {}, "nothing said about the supplementary document"), ("extras", {"verdict": True}, "extras needs exactly"),
                                ("extras.verdict", False, "only used with a verdict"), ("conflicts", [{"what": "term"}], "conflict"), ("meetings_held", ["10/11/2026"], "future"),
                                ("next_meeting.date", "01/11/2026", "past"), ("next_meeting.time", "5", "time like 12pm"), ("client_first_name", "Robin", "not the client Paul named"),
                                ("sources.fees", "", "sources.fees"), ("client_full_name", "Patricia Beth Samplecase", "client name"), ("surprise", 1, "unknown field")):
            self.refused(R, sample.bad(A, **{path: val}), frag)
        self.refused(R, sample.bad(A, providers=[A["providers"][0]]), "from 2 to 6 providers")
        self.refused(R, sample.bad(A, **{"providers.0.fee_lines": []}), "fee breakdown is needed")
        self.refused(R, sample.bad(A, **{"providers.0.fee_lines.0.label": "Total EAC", "providers.0.fee_lines.0.pct": "2.9%"}), "blended or total")
        self.refused(R, sample.bad(A, **{"providers.0.loyalty.0.explanation": sample.DELETE}), "plain-language explanation")
        self.refused(R, sample.bad(A, **{"fund_sheets.2": sample.DELETE}), "no entry for Testco - Test Cautious Fund")
        self.refused(R, sample.bad(A, **{"providers.0.flexibility": [], "providers.1.flexibility": []}), "flexibility was asked for")
        run("run.py", "done", R, "answers", expect=3)

        # ---- good answers, then the comparison
        run("run.py", "answers", R, "--file", self.afile(A))
        run("run.py", "done", R, "answers")
        run("run.py", "show", R, expect="refused")                                          # the comparison has not been worked out
        run("run.py", "done", R, "check", expect=3)
        out = run("run.py", "check", R)
        for frag in ("contribution structure, amount, yearly increase and term are the same", "Samplelife: asset management 0.89%", "total ongoing fees 2.665% a year",
                     "Testco: asset management 0.60%", "total ongoing fees 2.075% a year", "HINT", "Testco Booster Illustrator shows 3.50%", "FLAG for Paul: The Sample Growth Fund"):
            self.assertIn(frag, out)
        run("run.py", "done", R, "check")

        # ---- Paul's yes
        run("run.py", "approve", R, "--said", "yes", expect="refused")                     # not shown yet
        run("run.py", "build", R, expect="refused")                                         # no yes yet
        out = run("run.py", "show", R)
        for frag in ("Fund fact sheets (own date each)", "30/09/2026", "all the same", "Subject", "Teams message to Sitamah", "<greeting by the clock>", "Are these answers right",
                     "Thursday, 29/10/2026 & Monday, 02/11/2026", "Please confirm with Testco", "The saved copy has no logo.", "total 2.665% p.a.", "verdict yes; tax note yes; flexibility yes"):
            self.assertIn(frag, out)
        run("run.py", "approve", R, "--said", "Yes, those are right")
        changed = sample.bad(A, flags=A["flags"] + ["The Samplelife quote expires on 30/11/2026."])
        run("run.py", "answers", R, "--file", self.afile(changed))                         # a changed answer voids the yes AND the check
        run("run.py", "build", R, expect="refused")
        run("run.py", "show", R, expect="refused")
        run("run.py", "check", R)
        run("run.py", "done", R, "check")
        run("run.py", "show", R)
        run("run.py", "approve", R, "--said", "Yes, those are right")
        run("run.py", "done", R, "confirm")

        # ---- the build
        run("run.py", "build", R)
        name = "Pat_Samplecase_Investment_Comparison_Email - 05.11.26.html"
        full, saved, body = (self.read(os.path.join(R, "out", name)), self.read(os.path.join(R, "out", "saved", name)), self.read(os.path.join(R, "out", "draft_body.html")))
        self.assertIn("data:image/png;base64,", full)
        self.assertNotIn("data:image", saved)
        self.assertNotIn("Kind regards", body)
        self.assertNotIn("Importance:", body)
        self.assertEqual(len(re.findall(r"\[[A-Z][A-Z0-9 _%().,/&#-]*\]", re.sub(r"base64,[A-Za-z0-9+/=]+", "", full))), 0)
        for frag in ("Sent:</td><td style=\"font-size:12pt;\">Thursday, 05/11/2026 10:15", "Sitamah Nathoo", "Patricia Anne Samplecase / Retirement Annuity Comparison – Samplelife vs Testco",
                     "pat@example.invalid", "Thursday, 29/10/2026 &amp; Monday, 02/11/2026", "Thursday, 12/11/2026 @ 12pm", "Retirement Annuity Comparison", "Total Ongoing Fees &#8211; Per Annum (Excluding EAC)",
                     "Investment Fund Comparison", "Loyalty and Value-Add Benefits", "2.665% p.a.", "2.075% p.a.", "Not on this quote", "0.575%", "30/09/2026", "31/10/2026",
                     "Things to know before you read the tables:", "Please confirm with Testco which figure applies", "Performance fee: the Test Cautious Fund can charge a performance fee",
                     "Fees only: how the plans compare", "Testco has the lowest total ongoing fees: 0.59 percentage points a year less than Samplelife.", "about R 590 a year",
                     "Contributions to a retirement annuity are tax deductible up to 27,5%", "Flexibility and contract terms", "You can pause contributions without a penalty.",
                     "A once-off payment to the adviser when the plan starts.", "Samplelife &amp; Testco"):
            self.assertIn(frag, full, frag)
        self.assertEqual(full.count("Effective Annual Cost"), 1)
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
        subj = icmp.subject(A)
        run("run.py", "message", R, "--used-today", "no", expect="refused")
        faults = {"a second signature": dict(signature=sample.SIGNATURE + "<p>Kind regards,</p>"), "no signature": dict(signature=""), "a wrong Cc": dict(cc="someone@example.invalid"),
                  "a wrong subject": dict(subject="Pat Samplecase / comparison"), "low importance": dict(importance="normal"),
                  "a placeholder": dict(content=lambda c: c.replace("Dear Pat,", "Dear [CLIENT FIRST NAME],")),
                  "BODY_PLACEHOLDER left": dict(content=lambda c: c + "<p>BODY_PLACEHOLDER</p>"),
                  "an unclosed table": dict(content=lambda c: c + "<table><tr><td>x</td></tr>"),
                  "a wrong total": dict(content=lambda c: c.replace("2.665% p.a.", "2.7% p.a.")),
                  "a missing fact sheet date": dict(content=lambda c: c.replace("31/10/2026", "")),
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
        self.assertIn(icmp.SITAMAH_CHAT, out)
        for frag in ("1. The Samplelife quote (%s)" % sample.NAMES["quote_samplelife"][:-4], "2. The Testco quote (%s)" % sample.NAMES["quote_testco"][:-4],
                     "3. The fund fact sheets (Sample Balanced Fund, Sample Growth Fund & Test Cautious Fund)", "4. The supplementary document: Testco Booster Illustrator"):
            self.assertIn(frag, out)
        for label, v in {"a wrong greeting": dict(greeting="Good afternoon"), "a literal **": dict(html=lambda h: h.replace("<strong>Action needed:</strong>", "**Action needed:**")),
                         "no numbered list": dict(html=lambda h: h.replace("<ol>", "<ul>").replace("</ol>", "</ul>")),
                         "a do-not-send line": dict(html=lambda h: h + "<p>Please do not send it.</p>"),
                         "a missing quote": dict(html=lambda h: h.replace(sample.NAMES["quote_testco"][:-4], "x"))}.items():
            g = v.pop("greeting", "Good morning")
            out = run("run.py", "messagecheck", R, "--file", self.tfile(sample.message_json(A, g, **v), "bad-msg.json"), expect=5)
            self.assertIn(BAD, out, label)
        run("run.py", "messagecheck", R, "--file", self.tfile(sample.message_json(A, "Good morning"), "good-msg.json"))
        run("run.py", "receipt", R, "message.chat", "19:someone-else@unq.gbl.spaces")
        run("run.py", "receipt", R, "message.format", "markdown")
        run("run.py", "done", R, "message", expect=3)                                       # the wrong chat
        run("run.py", "receipt", R, "message.chat", icmp.SITAMAH_CHAT)
        run("run.py", "done", R, "message")

        # ---- the final audit: short, all ticks
        out = run("run.py", "done", R, "final")
        self.assertIn("RESULT: PASS", out)
        self.assertFalse([ln for ln in out.splitlines() if ln.startswith(BAD)])
        self.assertLessEqual(len([ln for ln in out.splitlines() if ln.startswith(OK)]), 30)
        for frag in ("Only attested", "real, current page", "flags for Paul", "risk profile"):
            self.assertIn(frag, out)
        self.assertTrue(os.path.exists(os.path.join(R, "out_record", "audit-full.txt")))
        out = run("verify.py", R)
        self.assertIn("RESULT: PASS", out)
        fs = os.path.join(R, "docs", icmp.dkey("factsheet", "Samplelife - Sample Balanced Fund") + ".txt")        # a hand-edited fact sheet is caught
        original = self.read(fs)
        with open(fs, "a", encoding="utf-8") as f:
            f.write(" edited by hand")
        out = run("verify.py", R, expect=1)
        self.assertIn(BAD, out)
        with open(fs, "w", encoding="utf-8") as f:
            f.write(original)
        with open(os.path.join(R, "out", "saved", name), "a", encoding="utf-8") as f:       # a hand-edited saved copy is caught
            f.write("<!-- edited by hand -->")
        out = run("verify.py", R, expect=1)
        self.assertIn(BAD, out)
        self.assertIn("RESULT: FAIL", out)

    # ------------------------------------------------------------------ the quotes do not match: the one question asks, the email labels it
    def mismatch_case(self):
        import icmp
        d2 = tempfile.mkdtemp(prefix="wr-inv-test2-")
        docs2 = sample.make_docs(d2, testco_premium="R 2 500.00")
        A = sample.bad(sample.answers(), **{"providers.1.contribution": "R 2 500.00"})
        R = os.path.join(self.d, "run-mismatch")
        run("run.py", "start", R, "--client", "Pat Samplecase")
        self.register(R, files=docs2)
        run("run.py", "done", R, "locate")
        self.read_all(R)
        run("run.py", "answers", R, "--file", self.afile(A))
        run("run.py", "done", R, "answers")
        out = run("run.py", "check", R)
        self.assertIn("NOT the same: contribution amount", out)
        self.assertIn("Do not go on unless Paul says so", out)
        run("run.py", "done", R, "check")
        out = run("run.py", "show", R)
        self.assertIn("The quotes are NOT for the same contribution amount", out)
        self.assertNotIn("Are these answers right", out)
        run("run.py", "approve", R, "--said", "Yes, go on and label it")
        run("run.py", "done", R, "confirm")
        run("run.py", "build", R)
        full = self.read(os.path.join(R, "out", "Pat_Samplecase_Investment_Comparison_Email - 05.11.26.html"))
        self.assertIn("The quotes are not for the same contribution amount: Samplelife R 3,000.00; Testco R 2,500.00. They are shown as quoted, so this is not a like-for-like comparison.", full)
        out = run("verify.py", R, "pre", expect=1)                                          # the later steps are not done: red crosses expected
        self.assertIn("NOT the same (contribution amount", out)

    # ------------------------------------------------------------------ small model-level checks
    def small_cases(self):
        import icbuild as b
        import icmp as c
        import wrlib as w
        import docread
        today = w.parse_date("05/11/2026")
        sent = "Thursday, 05/11/2026 10:15"

        def world(files, labels):
            reg = {"docs": {}, "missing": {}}
            for k, p in files.items():
                role, lab = labels[k]
                reg["docs"][k] = {"role": role, "label": lab, "name": os.path.basename(p)}
            ev = {k: docread.Evidence(docread.read_document(p)) for k, p in files.items()}
            return reg, ev
        labels = {"quote_samplelife": ("quote", "Samplelife"), "quote_testco": ("quote", "Testco"), "fact_find": ("fact_find", None), "tfsa_statement": ("tfsa_statement", None),
                  "supplement_testco_booster_illustrator": ("supplement", "Testco Booster Illustrator")}
        for lab in sample.SHEETS:
            labels[c.dkey("factsheet", lab)] = ("factsheet", lab)
        reg, ev = world(self.docs, labels)
        state = {"funds": sample.FUNDS}
        A = sample.answers()
        self.assertEqual(c.answers_problems(A, ev, reg, today, "Pat Samplecase", state), [])
        # ---- fees: blended and added up as shown; a fee a provider does not show is 'Not on this quote'
        self.assertEqual(c.fee_total(A["providers"][0]), (["0.89", "1.20", "0.575", "0.00"], "2.665"))
        rows = c.fee_rows(A)
        self.assertEqual([r[0] for r in rows], ["Asset management fee", "Net administration fee", "Ongoing advice fee", "Adviser remuneration account charge", "Administration fee"])
        self.assertEqual(rows[1][2], ["1.20", None])
        self.assertEqual(c.pct_decimal("0.575%"), c.Decimal("0.575"))
        # ---- the apples-to-apples checks
        self.assertEqual(c.mismatches(A), [])
        mm = c.mismatches(sample.bad(A, **{"providers.1.term": "Retirement age 60", "providers.1.escalation": "None", "providers.1.contribution_type": "lump_sum"}))
        self.assertEqual([m[0] for m in mm], ["contribution structure", "yearly increase", "term or retirement age"])
        # ---- the jargon and EAC checks catch what the builder never writes
        self.assertEqual(b.jargon_problems("<p>The TER is 1% a year.</p>", A), ["TER"])
        self.assertEqual(b.jargon_problems("<p>The TER (Total Expense Ratio: the fund's yearly running costs) is 1% a year.</p>", A), [])
        sneaky = sample.bad(A, **{"providers.0.loyalty.0.explanation": "The bonus is paid once, and unlike the EAC it does not hide a fee inside one blended number at all."})
        full, nologo, body = b.build_all(sneaky, sent, reg, today)
        bad = [r[1] for r in b.html_problems(full, nologo, body, sneaky, sent, reg, today) if not r[0]]
        self.assertTrue([x for x in bad if "EAC" in x])
        # ---- a stale fact sheet and a missing one are flagged in the email (the date is later, the sheet text is not needed for the build)
        later = w.parse_date("15/03/2027")
        full, nologo, body = b.build_all(A, sent, reg, later)
        self.assertEqual([r[1] for r in b.html_problems(full, nologo, body, A, sent, reg, later) if not r[0]], [])
        self.assertIn("is dated 30/09/2026, which is more than three months ago", b.text_of(body))
        self.assertEqual(len(c.stale_sheets(A, later)), 3)
        self.assertEqual(c.stale_sheets(A, today), [])
        miss = sample.bad(A, **{"fund_sheets.2": {"provider": "Testco", "fund": "Test Cautious Fund", "not_found": True}})
        reg2 = {"docs": {k: v for k, v in reg["docs"].items() if k != c.dkey("factsheet", "Testco - Test Cautious Fund")}, "missing": {c.dkey("factsheet", "Testco - Test Cautious Fund"): "Paul: no sheet exists online"}}
        self.assertEqual(c.answers_problems(miss, ev, reg2, today, "Pat Samplecase", state), [])
        full, nologo, body = b.build_all(miss, sent, reg2, today)
        self.assertEqual([r[1] for r in b.html_problems(full, nologo, body, miss, sent, reg2, today) if not r[0]], [])
        self.assertIn("A current fact sheet for the Test Cautious Fund could not be found", b.text_of(body))
        self.assertIn("Fact sheet not found", b.text_of(body))
        # ---- no extras: no optional parts and no flag box when nothing is flagged
        plain = sample.bad(A, **{"extras": {"verdict": False, "tax_note": False, "flexibility": False, "example_fund_value": None}, "supplement_checks": {"Testco Booster Illustrator": "none"},
                                 "fund_sheets.1.risk_label": "Moderate"})
        full, nologo, body = b.build_all(plain, sent, reg, today)
        self.assertEqual([r[1] for r in b.html_problems(full, nologo, body, plain, sent, reg, today) if not r[0]], [])
        bt = b.text_of(body)
        for frag in ("Things to know", "Fees only", "Tax treatment", "Flexibility and contract terms"):
            self.assertNotIn(frag, bt)
        # ---- an endowment tax note stops: no approved wording (the quote words are changed so the product check passes)
        reg_e = {"docs": dict(reg["docs"]), "missing": {}}
        ev_e = dict(ev)
        for k in ("quote_samplelife", "quote_testco"):
            ev_e[k] = docread.Evidence({"page_count": 1, "pages": [{"n": 1, "text": ev[k].text.replace("Retirement Annuity", "Endowment Plan"), "chars": 10}], "image_only": []})
        endow = sample.bad(A, **{"product_type": "Endowment", "providers.0.product_name": "Samplelife Endowment Plan", "providers.1.product_name": "Testco Endowment Plan"})
        out = c.answers_problems(endow, ev_e, reg_e, today, "Pat Samplecase", state)
        self.assertTrue([x for x in out if "no approved tax wording for a Endowment" in x], out)
        # ---- the Tax-Free room: stops until Paul confirms the limits; then the arithmetic and the breach flag
        tdocs = sample.make_tfsa_docs(self.d)
        files_t = dict(self.docs)
        files_t.update(tdocs)
        reg_t, ev_t = world(files_t, labels)
        T = sample.bad(A, **{"product_type": "TFSA", "providers.0.escalation": "0%", "providers.1.escalation": "0%", "providers.0.term": "No fixed term", "providers.1.term": "No fixed term",
                             "providers.0.product_name": "Samplelife Tax-Free Savings Account", "providers.1.product_name": "Testco Tax Free Savings Account", "providers.1.contribution": "R 4 000.00",
                             "providers.0.loyalty.0.source_line": "paid at retirement if no premiums are missed", "tfsa": {"annual_used": "R 10 000.00", "lifetime_used": "R 120 000.00"},
                             "sources.tfsa": "the TFSA statement", "extras.tax_note": True})
        out = c.answers_problems(T, ev_t, reg_t, today, "Pat Samplecase", state)
        self.assertTrue([x for x in out if "are NOT confirmed by Paul" in x], out)
        confirmed = os.path.join(self.d, "tax_facts_confirmed.json")
        with open(confirmed, "w", encoding="utf-8") as f:
            json.dump({"tfsa": {"annual_limit": "R 46,000.00", "lifetime_limit": "R 500,000.00", "confirmed": True}}, f)
        real_facts = c.FACTS
        c.FACTS = confirmed
        try:
            out = [x for x in c.answers_problems(T, ev_t, reg_t, today, "Pat Samplecase", state) if "TFSA" in x or "Tax-Free" in x]
            self.assertEqual(out, [])
            rows_t = c.tfsa_rows(T)
            self.assertEqual([(n, str(y), [(k, str(v)) for k, v in br]) for n, y, br in rows_t], [("Samplelife", "36000.00", []), ("Testco", "48000.00", [("annual", "12000.00")])])
            items = c.things_to_know(T, today)
            self.assertTrue([x for x in items if "Testco's quote proposes R 48,000 in the first year. This would take you over your annual limit by R 12,000." in x], items)
            full, nologo, body = b.build_all(T, sent, reg_t, today)
            self.assertEqual([r[1] for r in b.html_problems(full, nologo, body, T, sent, reg_t, today) if not r[0]], [])
            self.assertIn("SARS allows you to contribute up to R 46,000.00 a year and R 500,000.00 over your lifetime", b.text_of(body))
        finally:
            c.FACTS = real_facts


if __name__ == "__main__":
    unittest.main()
