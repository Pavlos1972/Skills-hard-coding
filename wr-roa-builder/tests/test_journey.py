"""The ONE test of the wr-roa-builder (Operation Skill Restructure: one end-to-end test on invented data).

It plays whole jobs through the program exactly as a chat would, on invented documents (Pat Samplecase, BrightRock-style quotes, an invented
reply email), with today fixed by WR_TODAY. Nothing is saved or sent anywhere: the folder listing is typed in as receipts. The real wkhtmltopdf is not
installable in the container where this was written, so a stand-in with the same command line is used for the HTML-to-PDF render ONLY: it refuses
any command line that does not carry the mandated page geometry or that carries --zoom. Everything else (the font rewrite, the images, the embedding,
the first-page check, the .docx checks) runs for real. It proves:
  1. the driver refuses to skip a step and bad answers are refused (a scenario not in the bank, a scenario that disagrees with the replacement flag, a
     blank-rendering Need Identified, a figure or an ID not in the documents, a lower-case insurer, a declined need with no reason, a conflict, a future date);
  2. a Risk ROA ends in a short audit of ticks: the reason texts are the bank paragraphs word for word, the totals and dropdowns are valid, the finished
     .docx was reopened and checked, nothing can be built before Paul's yes, a changed answer voids it, a hand-edited .docx is caught, and an existing file
     is never overwritten without his yes;
  3. a Retirement ROA embeds the client's own reply email: a page that opens on the proposal is refused, the fonts are rewritten to 15 pt, the renderer gets the
     fixed geometry, the pages land before 'Investment Planning'; an Investment ROA lands them before 'POLICY REPLACEMENT';
  4. the rules in the model: the new-cover-while-another-is-replaced sentence, reference numbers, file names, the next review date, the reason bank.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
SCRIPTS = os.path.join(SKILL, "scripts")
sys.path.insert(0, SCRIPTS)
sys.path.insert(0, HERE)
import roa  # noqa: E402
import sample  # noqa: E402


def run(script, *args, expect=0, env=None):
    e = dict(os.environ, WR_TODAY="05/11/2026")
    e.update(env or {})
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS, script)] + list(args), capture_output=True, text=True, encoding="utf-8", env=e)
    if expect == "refused":
        assert r.returncode != 0, "%s %s should have been refused\n%s" % (script, args, r.stdout[-1200:])
    else:
        assert r.returncode == expect, "%s %s -> exit %d (wanted %d)\n%s\n%s" % (script, args, r.returncode, expect, r.stdout[-1800:], r.stderr[-800:])
    return r.stdout + r.stderr


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)


class Journey(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="wr-roa-test-")
        self.docs = sample.make_docs(self.d)
        self.wk_log = os.path.join(self.d, "wk.log")
        self.env = {"WR_WKHTMLTOPDF": sample.stub_wkhtmltopdf(self.d, self.wk_log)}

    def afile(self, data, name="answers.json"):
        path = os.path.join(self.d, name)
        write_json(path, data)
        return path

    def start(self, name, bundle, roles):
        R = os.path.join(self.d, name)
        out = run("run.py", "start", R, "--client", "Pat Samplecase", "--bundle", bundle, env=self.env)
        self.assertIn("Using wr-roa-builder, last updated", out)
        run("run.py", "access", R, "--purpose", "locate", "--route", "device", "--result", "found", "--note", "test")
        for role in roles:
            run("run.py", "doc", R, "--role", role, "--file", self.docs[role], "--route", "device")
        return R

    def read_all(self, R):
        for _ in range(12):
            out = run("run.py", "read", R)
            m = re.search(r"--ack ([a-z_]+:\d+)", out)
            if not m:
                break
            run("run.py", "read", R, "--ack", m.group(1), "--note", "read " + m.group(1))
        run("run.py", "done", R, "read")

    def to_confirmed(self, name, bundle, answers, roles, email=None):
        R = self.start(name, bundle, roles)
        run("run.py", "done", R, "locate")
        self.read_all(R)
        run("run.py", "answers", R, "--file", self.afile(answers, name + ".json"))
        run("run.py", "done", R, "answers")
        run("run.py", "approve", R, "--said", "Yes", expect="refused")                       # not shown yet
        shown = run("run.py", "show", R)
        self.assertIn("THE ONE QUESTION TO PAUL", shown)
        run("run.py", "approve", R, "--said", "Yes, build it")
        run("run.py", "done", R, "confirm")
        if email:
            run("run.py", "email", R, "--file", email, env=self.env)
        run("run.py", "done", R, "email")
        return R, shown

    def finish(self, R, render=False):
        out = run("run.py", "build", R, env=self.env)
        run("run.py", "done", R, "build", env=self.env)
        chk = run("run.py", "check", R, *([] if render else ["--no-render"]), env=self.env)
        self.assertNotIn("\u274c", chk)
        run("run.py", "done", R, "check", env=self.env)
        name = [ln for ln in run("run.py", "name", R, "--existing", "Other.docx").splitlines() if ln.startswith("SAVE THIS FILE:")][0].split("SAVE THIS FILE: ")[1]
        run("run.py", "access", R, "--purpose", "save", "--route", "device", "--result", "found", "--note", "test")
        run("run.py", "receipt", R, "save.folder", "C:\\Users\\x\\Company - Paul\\Samplecase, Pat\\ROA & Bus ROA")
        run("run.py", "receipt", R, "save.listed_bytes", str(os.path.getsize(name)))
        run("run.py", "done", R, "save", env=self.env)
        final = run("run.py", "done", R, "final", env=self.env)
        self.assertIn("RESULT: PASS", final)
        audit = final[final.index("AUDIT   "):].strip().splitlines()
        marks = [ln for ln in audit if ln.startswith("\u2705") or ln.startswith("\u274c")]
        self.assertLessEqual(len(audit), 20, "the audit must stay short")
        self.assertTrue(all(ln.startswith("\u2705") for ln in marks), "every check line must be a green tick:\n" + "\n".join(marks))
        self.assertTrue(any(ln.startswith("Only attested") for ln in audit))
        return name, out

    def text_of(self, docx):
        from lxml import etree
        root = etree.fromstring(zipfile.ZipFile(docx).read("word/document.xml"))
        return " ".join("".join(root.itertext()).split())

    def test_one_journey_on_invented_data(self):
        risk_roles = ("fna_quote", "application", "follow_up_notes", "fact_find_summary", "accepted_quote")
        # 1. steps cannot be skipped; routes and documents are checked; bad answers are refused
        R0 = os.path.join(self.d, "run0")
        run("run.py", "start", R0, "--client", "Pat Samplecase", "--bundle", "risk")
        run("run.py", "done", R0, "answers", expect=3)
        run("run.py", "build", R0, expect="refused")
        run("run.py", "doc", R0, "--role", "fna_quote", "--file", self.docs["fna_quote"], "--route", "zapier", expect="refused")       # no try logged
        run("run.py", "access", R0, "--purpose", "locate", "--route", "zapier", "--result", "found", "--note", "test")
        run("run.py", "doc", R0, "--role", "fna_quote", "--file", self.docs["fna_quote"], "--route", "zapier", expect="refused")       # zapier before the computer and Microsoft 365
        R1 = self.start("run1", "risk", risk_roles)
        run("run.py", "done", R1, "locate")
        run("run.py", "done", R1, "read", expect=3)
        self.read_all(R1)
        run("run.py", "read", R1, "--ack", "fna_quote:1", "--note", "x", expect="refused")                                              # nothing left to acknowledge
        base = sample.risk_answers()

        def variant(fn):
            a = sample.risk_answers()
            fn(a)
            return a
        bad = {
            "scenario not in the bank": variant(lambda a: a["covers"]["death"].update(scenario="FNA DONE & INVENTED / REPLACEMENT:")),
            "scenario disagrees with replacement": variant(lambda a: a["covers"]["death"].update(replacement=False)),
            "blank-rendering need identified": variant(lambda a: a["covers"]["disability"].pop("need_identified")),
            "figure not in the quote": variant(lambda a: a["covers"]["death"].update(taken_up_amount="R 999 000")),
            "ID of 12 digits": variant(lambda a: a.update(client_id="111111111111")),
            "lower-case insurer": variant(lambda a: a.update(recommended_insurer="Brightrock")),
            "declined without a reason": variant(lambda a: a["covers"]["dread"].update(declined_reason="no")),
            "unresolved conflict": variant(lambda a: a.update(conflicts=[{"what": "premium", "values": ["R 1 172.79", "R 1 172.80"]}])),
            "future ROA date": variant(lambda a: a.update(roa_date="06/11/2026")),
            "not accepted but taken up": variant(lambda a: a["covers"]["income_1st24"].update(taken_up_amount="R 20 000")),
            "income_after24 entered": variant(lambda a: a["covers"].update(income_after24={"state": "declined"})),
            "wrong client": variant(lambda a: a.update(client_name="Someone Else")),
        }
        for label, ans in bad.items():
            self.assertIn("REFUSED", run("run.py", "answers", R1, "--file", self.afile(ans, "bad.json"), expect=5), label)
        # 2. the good Risk ROA
        R2, shown = self.to_confirmed("run2", "risk", base, risk_roles)
        self.assertIn("FROM THE BANK (FNA DONE & ACCEPTED / REPLACEMENT:)", shown)
        self.assertIn("the reason Paul gave", shown)
        chg = sample.risk_answers()
        chg["covers"]["dread"]["declined_reason"] = "The client prefers to keep severe illness cover with their employer."
        run("run.py", "answers", R2, "--file", self.afile(chg, "chg.json"))                                                            # a changed answer voids the yes
        self.assertIn("Now: confirm", run("run.py", "status", R2))
        run("run.py", "build", R2, expect="refused")
        run("run.py", "show", R2)
        run("run.py", "approve", R2, "--said", "Yes again")
        run("run.py", "done", R2, "confirm")
        run("run.py", "done", R2, "email")
        name, out = self.finish(R2, render=True)
        self.assertTrue(os.path.isdir(os.path.join(R2, "out", "pages")) and os.listdir(os.path.join(R2, "out", "pages")))
        self.assertEqual(name.split(os.sep)[-1], "ROA - BR Personal Cover - R 1172.80 p.m. - 05.11.26 - (Pat Samplecase).docx")
        text = self.text_of(name)
        bk = roa.bank()
        self.assertIn(bk["death"]["FNA DONE & ACCEPTED / REPLACEMENT:"], text)                                                         # the bank paragraph, word for word
        self.assertIn(bk["disability"]["FNA DONE BUT REDUCED QUOTE ACCEPTED / REPLACEMENT:"], text)
        self.assertIn(bk["income_1st24"]["FNA DONE / BENEFIT NOT ACCEPTED:"], text)
        self.assertIn("The client prefers to keep severe illness cover with their employer.", text)
        self.assertIn("ROA Reference No: BrightRock Personal Cover - R1,172.80 p.m.", text)
        self.assertIn("diarised for the 2027-11-05", text)
        self.assertNotIn("Health Care", text)
        # a hand-edited .docx is caught; a name that already exists is never overwritten silently
        z = zipfile.ZipFile(name)
        edited = os.path.join(self.d, "edited.docx")
        with zipfile.ZipFile(edited, "w") as zo:
            for it in z.namelist():
                data = z.read(it)
                if it == "word/document.xml":
                    data = data.replace(b"R 400,000", b"R 450,000")
                zo.writestr(it, data)
        os.replace(edited, name)
        self.assertIn("RESULT: FAIL", run("verify.py", R2, expect=1))
        run("run.py", "build", R2, env=self.env)
        self.assertIn("STOP", run("run.py", "name", R2, "--existing", os.path.basename(name), expect=5))
        run("run.py", "name", R2, "--existing", os.path.basename(name), "--overwrite-yes", "Paul said overwrite it")
        # 3. Retirement: the client's own reply must come first; fonts, geometry, position
        ret_roles = ("proposal_email", "client_reply_email", "fact_find_summary")
        R3 = self.start("run3", "retirement", ret_roles)
        run("run.py", "done", R3, "locate")
        self.read_all(R3)
        run("run.py", "answers", R3, "--file", self.afile(sample.retirement_answers(), "ret.json"))
        run("run.py", "done", R3, "answers")
        run("run.py", "show", R3)
        run("run.py", "approve", R3, "--said", "Yes")
        run("run.py", "done", R3, "confirm")
        self.assertIn("OPEN with the reply", run("run.py", "email", R3, "--file", self.docs["proposal_first"], env=self.env, expect=5))
        run("run.py", "done", R3, "email", expect=3)
        run("run.py", "email", R3, "--file", self.docs["composite"], env=self.env)
        run("run.py", "done", R3, "email")
        name3, out3 = self.finish(R3)
        self.assertIn("1 email page(s) embedded before 'Investment Planning'", out3)
        with open(os.path.join(R3, "embed", "email_scaled.html"), encoding="utf-8") as f:
            scaled = f.read()
        self.assertIn("font-size:15.00pt", scaled)                                                                                       # 12 pt body -> 15 pt
        self.assertIn("font-size:12.50pt", scaled)                                                                                       # 10 pt fine print, same factor
        with open(self.wk_log) as f:
            self.assertNotIn("--zoom", f.read())
        t3 = self.text_of(name3)
        self.assertIn("Although the client has other Risk Cover in force, this transaction does not constitute a replacement of that cover.", t3)
        self.assertIn("ROA Reference No: Old Mutual Retirement Annuity Xtra Max - R 1,500.00 p.m.", t3)
        # Investment: the pages land before POLICY REPLACEMENT
        inv = sample.investment_answers()
        R4, _ = self.to_confirmed("run4", "investment", inv, ret_roles, email=self.docs["composite"])
        name4, out4 = self.finish(R4)
        self.assertIn("embedded before 'POLICY REPLACEMENT'", out4)
        # 4. the model's own rules
        c = {"state": "accepted", "replacement": False, "new_while_other_replaced": True, "scenario": "FNA DONE & ACCEPTED / NON-REPLACEMENT:"}
        text, mode, head = roa.cover_reason("income_1st24", c, bk)
        self.assertTrue(text.endswith(roa.OTHER_COVER_SENTENCE) and bk["income_1st24"][head].startswith(text[:60]) and "no Risk Cover currently in force" not in text)
        self.assertEqual(roa.next_review("2028-02-29"), "2029-02-28")
        self.assertEqual(roa.reference_no(sample.investment_answers()), "Old Mutual Tax-Free Investment Plan - R 1,500.00 p.m.")
        self.assertEqual(sorted(bk), ["death", "disability", "dread", "income_1st24"])
        self.assertEqual(len(bk["death"]), 14)
        lists = roa.template_lists()
        self.assertIn("OLD MUTUAL", lists["insurers"])
        self.assertEqual(len(lists["insurers"]), 9)


if __name__ == "__main__":
    unittest.main()
