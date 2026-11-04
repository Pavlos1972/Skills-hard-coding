"""The ONE test of the life-insurer-comparison skill (Operation Skill Restructure: one end-to-end test on invented data).

It plays a whole job through the program exactly as a chat would, on invented documents (Pat Samplecase, the invented insurers Samplelife, Testco and Examplecover: an in-force schedule,
a proposal and a quote with one page that is only an image, the client's meeting notes, a Fact Find Summary, a WR Overview and the insurers' guides saved as text), with today and the
clock fixed by WR_TODAY and WR_NOW. Nothing is saved or sent anywhere: the folder listing, the Outlook read-back and the posted Teams message are typed in as files. It proves:
  1. the driver refuses to skip a step; the routes must be tried in order; a quote can never be missing; the insurers must be declared and each needs a saved guide with its address and date;
  2. the benefit scope is proved by a line of the client's notes for every category (a line that is not in the notes, a missing category, life cover out are refused);
  3. bad answers are refused (nothing saved): a figure that is not in its evidence line, an evidence line that is not in the document, a category that is out of scope (in a cover or in a
     word of a text), a 'wins' badge on an inference, an 'exclusive' claim not checked against every other insurer, a figure not in the document, a text over its limit, a slip of voice,
     quote-version history, too few email bullets, image_read on a page that has text, a wrong insurer, a missing second-life status, an email not in the Fact Find Summary;
  4. the premium escalation is worked out by the program (an outlier, a printed against a calculated percentage, a table shorter than ten years, a guarantee not stated); a changed answer
     voids the check and Paul's yes; nothing is built before his yes;
  5. the letter has the sections ticked in the fixed order, the banner, the salutation, the closing, the scope respected, a badge on every year with a figure, 'not provided' for a gap, a
     footnote that names printed and calculated, and the email body has only the allowed tags and no signature; the checks catch a mutated letter and a mutated email;
  6. the save never overwrites without a yes, the draft read-back is refused for every fault, Sitamah is messaged only after a checked draft and the posted message must read back right;
  7. the final audit is short and every line is a green tick; a hand-edited letter is caught; small model-level checks.
"""
import copy
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
URL = "https://example.invalid/guide"
FILE_NAME = "Pat_Samplecase_Life_Insurance_Comparison - 05.11.26.html"


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
        self.d = tempfile.mkdtemp(prefix="wr-lic-test-")
        self.docs = sample.make_docs(self.d)

    def read(self, path):
        with open(path, encoding="utf-8") as f:
            return f.read()

    def load(self, path):
        return json.loads(self.read(path))

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

    def refused_answers(self, R, data, fragment):
        out = run("run.py", "answers", R, "--file", self.afile(data), expect="refused")
        self.assertIn(fragment, out)
        self.assertFalse(os.path.exists(os.path.join(R, "answers.json")), "a refused answers file must not be saved")

    def refused_scope(self, R, data, fragment):
        out = run("run.py", "scope", R, "--file", self.afile(data, "scope.json"), expect="refused")
        self.assertIn(fragment, out)
        self.assertFalse(os.path.exists(os.path.join(R, "scope.json")), "a refused scope file must not be saved")

    def read_all(self, R, done=None):
        seen = []
        for _ in range(60):
            out = run("run.py", "read", R)
            seen.append(out)
            m = re.search(r"--ack ([a-z_0-9]+:\d+)", out)
            if not m:
                break
            run("run.py", "read", R, "--ack", m.group(1), "--note", "read " + m.group(1))
        if done:
            run("run.py", "done", R, done)
        return "\n".join(seen)

    def register(self, R, via="device"):
        run("run.py", "access", R, "--purpose", "locate", "--route", via, "--result", "found", "--note", "test")
        for lab, (role, key) in sample.LABELS.items():
            run("run.py", "doc", R, "--role", role, "--label", lab, "--file", self.docs[key], "--route", via)
        run("run.py", "doc", R, "--role", "intake_notes", "--label", "2026-10-02", "--file", self.docs["intake_notes_2026_10_02"], "--route", via)
        run("run.py", "doc", R, "--role", "fact_find_summary", "--file", self.docs["fact_find_summary"], "--route", via)
        run("run.py", "doc", R, "--role", "overview", "--file", self.docs["overview"], "--route", via)

    def test_whole_journey(self):
        self.main_case()
        self.small_cases()

    # ------------------------------------------------------------------ the whole job
    def main_case(self):
        # --- a separate run: the routes must be tried in order, a quote can never be missing
        R0 = os.path.join(self.d, "run0")
        run("run.py", "start", R0, "--client", "Pat Samplecase")
        run("run.py", "access", R0, "--purpose", "locate", "--route", "m365", "--result", "found")
        out = run("run.py", "doc", R0, "--role", "quote", "--label", "Testco Proposal", "--file", self.docs["quote_testco_proposal"], "--route", "m365", expect="refused")
        self.assertIn("tried in order", out)
        out = run("run.py", "doc", R0, "--missing", "quote", "--label", "Testco Proposal", "--said", "could not find it", expect="refused")
        self.assertIn("can never be missing", out)

        R = os.path.join(self.d, "run")
        out = run("run.py", "start", R, "--client", "Pat Samplecase")
        self.assertIn("Using life-insurer-comparison, last updated", out)
        self.assertIn("STEP 1 of 12", out)
        self.assertIn("refused", run("run.py", "done", R, "scope", expect="refused").lower())
        # --- locate
        self.register(R)
        out = run("run.py", "insurers", R, "--file", self.afile([{"label": "Samplelife Schedule", "insurer": "Nobody"}, {"label": "Testco Proposal", "insurer": "Testco"},
                                                                  {"label": "Examplecover Quote", "insurer": "Examplecover"}], "insurers.json"), expect="refused")
        self.assertIn("is not in the text", out)
        out = run("run.py", "insurers", R, "--file", self.afile(sample.INSURERS, "insurers.json"))
        self.assertIn("Examplecover - <title of the guide>", out)
        run("run.py", "done", R, "locate")
        # --- read (the image-only page is flagged)
        out = self.read_all(R, "read")
        self.assertIn("NO READABLE TEXT", out)
        # --- scope
        out = run("run.py", "scope", R)
        self.assertIn("[EXCLUSION LANGUAGE]", out)
        self.assertIn("Elected to remove disability", out)
        sc = sample.scope()
        self.refused_scope(R, sample.bad(sc, **{"categories.severe_illness.evidence": "Severe illness is covered in full."}), "not in the text")
        self.refused_scope(R, sample.bad(sc, **{"categories.life.status": "out"}), "life cover must be in scope")
        self.refused_scope(R, sample.bad(sc, **{"categories.childcare": sample.DELETE}), "categories must have exactly")
        self.refused_scope(R, sample.bad(sc, **{"voice": "second_person"}), "voice must be")
        self.refused_scope(R, sample.bad(sc, **{"sections": ["premium_snapshot", "poetry"]}), "sections must be")
        run("run.py", "scope", R, "--file", self.afile(sc, "scope.json"))
        run("run.py", "done", R, "scope")
        # --- research: a guide needs an address and a date, and its label starts with a declared insurer
        run("run.py", "access", R, "--purpose", "research", "--route", "web", "--result", "found", "--note", "test")
        g = self.docs["guide_testco_guide"]
        out = run("run.py", "doc", R, "--role", "guide", "--label", "Testco - Product Guide", "--file", g, "--route", "web", expect="refused")
        self.assertIn("--url", out)
        out = run("run.py", "doc", R, "--role", "guide", "--label", "Nobody - Product Guide", "--file", g, "--route", "web", "--url", URL, "--fetched-at", "04/11/2026", expect="refused")
        self.assertIn("declare the insurers first", out)
        out = run("run.py", "done", R, "research", expect=3)
        self.assertIn("no guide", out)
        for ins, lab in sample.GUIDE_LABELS.items():
            run("run.py", "doc", R, "--role", "guide", "--label", lab, "--file", self.docs["guide_%s_guide" % ins.lower()], "--route", "web", "--url", URL, "--fetched-at", "04/11/2026")
        self.read_all(R, "research")
        # --- answers
        a = sample.answers()
        self.refused_answers(R, sample.bad(a, **{"sides.0.premium.monthly": "R 1 851.00"}), "not in the evidence line")
        self.refused_answers(R, sample.bad(a, **{"sides.0.premium.evidence": "Total monthly premium R 1 850.00 payable by debit order"}), "not in the text of")
        self.refused_answers(R, sample.bad(a, **{"sides.1.covers.0.category": "severe_illness"}), "out of scope")
        self.refused_answers(R, sample.bad(a, **{"features.1.text": "Your severe illness cover is a strong point."}), "out of scope")
        self.refused_answers(R, sample.bad(a, **{"features.2.badge": "wins"}), "cannot rest on an inference")
        self.refused_answers(R, sample.bad(a, **{"features.0.exclusive_checks": [a["features"][0]["exclusive_checks"][0]]}), "missing: Examplecover")
        self.refused_answers(R, sample.bad(a, **{"sides.0.projection.3.premium": "R 9 999.00"}), "not in the document's text")
        self.refused_answers(R, sample.bad(a, **{"banner": "Your premium " + "is very " * 40 + "high."}), "the limit is 60")
        self.refused_answers(R, sample.bad(a, **{"banner": "Wealth Revolution recommends Testco for you."}), "institutional phrase")
        self.refused_answers(R, sample.bad(a, **{"opening": "He should look at Testco."}), "third person")
        self.refused_answers(R, sample.bad(a, **{"verdict.1.detail": "The Samplelife premium no longer follows your age."}), "quote-version history")
        self.refused_answers(R, sample.bad(a, **{"email.bullets": ["One.", "Two.", "Three."]}), "from 4 to 6")
        self.refused_answers(R, sample.bad(a, **{"sides.0.covers.0": dict(a["sides"][0]["covers"][0], image_read=True, page=1)}), "image_read is only for a page")
        self.refused_answers(R, sample.bad(a, **{"sides.0.insurer": "Testco"}), "not the declared one")
        self.refused_answers(R, sample.bad(a, **{"sides.1.second_life": sample.DELETE}), "second_life")
        self.refused_answers(R, sample.bad(a, **{"client_email": "other@example.invalid"}), "not in the Fact Find Summary")
        self.refused_answers(R, sample.bad(a, **{"sides.2.guarantee": {}}), "guarantee is")
        self.refused_answers(R, sample.bad(a, **{"sides.1.loyalty.amount_or_pct": "20%"}), "20% is not in the evidence line")
        self.refused_answers(R, sample.bad(a, **{"sides.1.escalation.type": "annual"}), "must be 'fixed' or 'age_rated'")
        self.refused_answers(R, sample.bad(a, **{"features.3.conditions": ""}), "conditions")
        self.refused_answers(R, sample.bad(a, **{"unexpected": 1}), "keys exactly")
        out = run("run.py", "answers", R, "--file", self.afile(a))
        self.assertIn("answers saved", out)
        run("run.py", "done", R, "answers")
        # --- check, show, approve
        out = run("run.py", "show", R, expect="refused")
        self.assertIn("run.py check first", out)
        out = run("run.py", "check", R)
        self.assertIn("year 6 is 36.56%", out)
        self.assertIn("projection table has 8 year(s)", out)
        self.assertIn("guarantee period is not stated", out)
        self.assertIn("1 inference(s)", out)
        run("run.py", "done", R, "check")
        out = run("run.py", "approve", R, "--said", "yes", expect="refused")
        self.assertIn("not been shown", out)
        out = run("run.py", "build", R, expect="refused")
        self.assertIn("REFUSED", out)
        out = run("run.py", "show", R)
        self.assertIn("THE ONE QUESTION TO PAUL", out)
        self.assertIn("FIGURES READ FROM PAGE IMAGES", out)
        self.assertIn("Benefit scope: Severe illness / dread disease | OUT", out)
        self.assertIn("Teams message to Sitamah", out)
        self.assertIn("Paul will attach it", out)
        # a changed answer voids the check and the yes
        run("run.py", "answers", R, "--file", self.afile(sample.bad(a, **{"banner": "Your premium would start at R 1 420.00 a month with Testco, against R 1 850.00 today."})))
        out = run("run.py", "show", R, expect="refused")
        self.assertIn("run.py check first", out)
        run("run.py", "answers", R, "--file", self.afile(a))
        run("run.py", "done", R, "answers")
        run("run.py", "check", R)
        run("run.py", "done", R, "check")
        run("run.py", "show", R)
        run("run.py", "approve", R, "--said", "Yes, build it")
        run("run.py", "done", R, "confirm")
        # --- build
        out = run("run.py", "build", R)
        self.assertIn("program checks passed", out)
        self.assertIn(FILE_NAME, out)
        letter_path = os.path.join(R, "out", FILE_NAME)
        letter = self.read(letter_path)
        body = self.read(os.path.join(R, "out", "draft_body.html"))
        self.check_letter(letter, body)
        run("run.py", "done", R, "build")
        # --- save
        out = run("run.py", "name", R, "--existing", FILE_NAME, expect=5)
        self.assertIn("already exists", out)
        out = run("run.py", "name", R, "--existing", "something else.html")
        self.assertIn("SAVE THIS FILE", out)
        run("run.py", "access", R, "--purpose", "save", "--route", "device", "--result", "found", "--note", "test")
        size = str(os.path.getsize(letter_path))
        folder = "C:\\Clients\\%s\\Risk Transaction\\Comparative Quotes" % sample.FOLDER
        run("run.py", "receipt", R, "save.folder", folder)
        run("run.py", "receipt", R, "save.listed_bytes", size)
        run("run.py", "done", R, "save")
        # --- draft
        a_ = self.load(os.path.join(R, "answers.json"))
        subj = "Pat Samplecase / Life Insurance Comparison \u2013 Samplelife vs Testco vs Examplecover"
        for kw, frag in (({"signature": None, "extra": "<p>Kind regards,</p><p>Paul Kafentzis</p>"}, "Kind regards"), ({"to": "someone@example.invalid"}, "client"),
                         ({"cc": "other@example.invalid"}, "Cc"), ({"subject": "A different subject"}, "subject"), ({"has_att": True}, "attachment"),
                         ({"extra": "<p>082 454 1751</p>"}, "contact details"), ({"content": lambda c: c.replace("Testco starts at R 1 420.00 a month", "Testco starts at R 1 421.00 a month")}, "Missing from the draft"),
                         ({"content": lambda c: c + "<img src='x'>"}, "allowed tags")):
            kw = {k: v for k, v in kw.items() if v is not None}
            bad = self.tfile(sample.draft_json(a_, body, subj, **kw), "dr-bad.json")
            out = run("run.py", "draft", R, "--file", bad, expect=5)
            self.assertIn(BAD, out, frag)
        out = run("run.py", "done", R, "draft", expect=3)
        good = self.tfile(sample.draft_json(a_, body, subj), "dr-good.json")
        out = run("run.py", "draft", R, "--file", good)
        self.assertNotIn(BAD, out)
        run("run.py", "receipt", R, "draft.created_with", "outlook_create_draft")
        run("run.py", "done", R, "draft")
        # --- message
        out = run("run.py", "message", R, "--used-today", "no")
        self.assertIn("Good morning Sitamah,", out)
        self.assertIn("**FYI:**", out)
        self.assertIn(FILE_NAME, out)
        bad = self.tfile(sample.message_json(a_, FILE_NAME, html=lambda h: h.replace("<strong>Drafts</strong>", "**Drafts**")), "ms-bad.json")
        out = run("run.py", "messagecheck", R, "--file", bad, expect=5)
        self.assertIn(BAD, out)
        goodm = self.tfile(sample.message_json(a_, FILE_NAME), "ms-good.json")
        out = run("run.py", "messagecheck", R, "--file", goodm)
        self.assertNotIn(BAD, out)
        out = run("run.py", "done", R, "message", expect=3)
        run("run.py", "receipt", R, "message.chat", "19:bd2a130a-35d9-459e-9025-55f356810236_e6901cee-de73-46d9-88a5-5e4a1c296418@unq.gbl.spaces")
        run("run.py", "receipt", R, "message.format", "markdown")
        out = run("run.py", "done", R, "message")
        self.assertIn("STEP 'message' DONE", out)
        out = run("run.py", "done", R, "final")
        self.assertIn("RESULT: PASS", out)
        self.assertEqual([l for l in out.splitlines() if l.startswith(BAD)], [])
        self.assertIn("Only attested (not proven):", out)
        self.assertLess(len(out.splitlines()), 40, "the audit must be short")
        # --- a hand-edited letter is caught
        with open(letter_path, "a", encoding="utf-8") as f:
            f.write("<!-- edited by hand -->")
        r = subprocess.run([sys.executable, os.path.join(SCRIPTS, "verify.py"), R], capture_output=True, text=True, encoding="utf-8", env=dict(os.environ, WR_TODAY="05/11/2026", WR_NOW="10:15"))
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("not edited by hand", r.stdout)
        self.R, self.letter, self.body = R, letter, body

    def check_letter(self, letter, body):
        low = letter.lower()
        for word in ("severe illness", "disability", "income protection", "debt cover", "childcare", "dread disease"):
            self.assertNotIn(word, re.sub(r"(?is)<section id=\"sec-sources\">.*?</section>", "", low), word)
        order = [letter.find(x) for x in ('<header class="top">', 'class="banner"', 'class="salutation"', 'id="sec-premium_snapshot"', 'id="sec-cover_comparison"', 'id="sec-escalation_table"',
                                          'id="sec-loyalty"', 'id="sec-definitions"', 'id="sec-verdict"', 'class="closing"', 'id="sec-sources"')]
        self.assertEqual(order, sorted(order))
        self.assertTrue(all(o >= 0 for o in order))
        self.assertIn("Dear Pat,", letter)
        self.assertIn("082 454 1751", letter)
        self.assertIn("not provided", letter)                                   # Examplecover has no year 9 and 10
        self.assertIn("&dagger;", letter)                                       # calculated percentages are marked
        self.assertRegex(letter, r"percentages for Testco Proposal are printed by the insurer")
        self.assertRegex(letter, r"percentages for Samplelife Schedule, Examplecover Quote are our own calculation")
        self.assertIn("the increase in year 6 (36.56%) stands out", letter)
        self.assertIn("Testco wins", letter)
        self.assertIn("Fair trade-off", letter)
        self.assertIn("To be confirmed with Examplecover", letter)
        self.assertIn("Not on this proposal, and not confirmed for you", letter)
        self.assertIn("Not on this schedule", letter)
        self.assertIn("Not on this quote", letter)
        self.assertIn("Second life (Robin)", letter)
        self.assertIn("Funeral cover", letter)
        self.assertNotIn("<script", letter)
        self.assertIn("<ul><li>Testco starts at R 1 420.00 a month", body)
        self.assertNotIn("Kind regards", body)
        self.assertNotIn("<img", body)

    # ------------------------------------------------------------------ small model-level checks
    def small_cases(self):
        import lic as c
        import licbuild as b
        import verify
        a = sample.answers()
        sc = sample.scope()
        # the scope word lists: only OUT categories are scanned, terminal illness is always fine
        hits = c.scope_hits("Your severe illness cover and disability benefit, plus terminal illness", sc)
        self.assertEqual({k for k, _t in hits}, {"severe_illness", "disability"})
        sc_in = sample.bad(sc, **{"categories.severe_illness": {"status": "in", "paul_said": "Paul wants severe illness compared"}})
        self.assertEqual(c.scope_hits("severe illness", sc_in), [])
        # the escalation: Samplelife has one outlier (year 6), Testco prints its percentages, Examplecover is calculated and has only 8 years
        s0, s1, s2 = (c.esc_summary(s) for s in a["sides"])
        self.assertEqual([n for n, _p in s0["outliers"]], [6])
        self.assertEqual((s1["mode"], s2["mode"], s2["years"]), ("printed", "calculated", 8))
        self.assertEqual(str(c.proj_rows(a["sides"][0])[1]["pct"]), "4.86")
        self.assertEqual(s0["anchor"], 1)
        # a premium that is year 2 of the table, not year 1, is flagged
        moved = sample.bad(a, **{"sides.0.premium.monthly": "R 1 940.00"})
        self.assertEqual(c.esc_summary(moved["sides"][0])["anchor"], 2)
        # the wording contradicts the type: flagged
        wrong = sample.bad(a, **{"sides.0.escalation.type": "fixed"})
        self.assertIn("entered as FIXED", c.type_cue_flag(wrong["sides"][0]))
        # the voice and the version words
        self.assertTrue(c.voice_problems("I recommend this", "third_person", "Pat Samplecase"))
        self.assertTrue(c.voice_problems("he should", "first_person", "Pat Samplecase"))
        self.assertTrue(c.version_problems("the updated quote removes it"))
        # the built letter is checked: a mutated letter and a mutated email are caught
        docs, ev = verify.load_docs(self.R)
        from datetime import date
        letter, body = b.build_all(a, sc, docs, date(2026, 11, 5))
        self.assertTrue(all(ok for ok, _s, _d in b.html_problems(letter, body, a, sc, docs, date(2026, 11, 5))))

        def fails(l=None, bd=None):
            return [s for ok, s, _d in b.html_problems(l or letter, bd or body, a, sc, docs, date(2026, 11, 5)) if not ok]
        self.assertTrue(fails(l=letter.replace("<h2>Cover Comparison</h2>", "<h2>Cover Comparison</h2><p>Your disability cover is not selected.</p>")))
        self.assertTrue(fails(l=letter.replace('<div class="salutation">', '<p>Welcome</p><section id="sec-x"></section><div class="salutation">')))
        self.assertTrue(fails(l=letter.replace('data-badge="1"', 'data-b="1"', 3)))
        self.assertTrue(fails(l=letter.replace("Kind regards,", "")))
        self.assertTrue(fails(l=letter.replace("<p>Dear Pat,</p>", "<p>Dear Pat Samplecase,</p>")))
        self.assertTrue(fails(l=letter.replace("<table", "<table", 1) + "<table>"))
        self.assertTrue(fails(bd=body + "<p>Kind regards,</p>"))
        self.assertTrue(fails(bd=body + "<span>x</span>"))
        self.assertTrue(fails(bd=body.replace("fixed at 10%", "fixed at 11%")))
        self.assertTrue(fails(bd=body.replace("Google Chrome", "your browser")))
        # the words that must not be there come from the settings, not from the letter
        self.assertEqual(c.settings()["attach_by"], "paul")


if __name__ == "__main__":
    unittest.main()
