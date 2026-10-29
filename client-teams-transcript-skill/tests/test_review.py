"""Tests written from an independent review of the program: each one tries a cheap way round it. Invented data only."""
import json
import os
import shutil
import unittest

from test_gate import Base, FIXTURE, sh, slurp, spit


class InventedFacts(Base):
    def test_an_invented_bullet_with_an_unrelated_quote_fails(self):
        def f(c):
            c["areas"][0]["bullets"].append({"id": "bad1", "text": "Client diagnosed with diabetes, 50% loading, R9,999 p.m.", "status": "still open",
                                             "src": [self.src("proposal emails")]})
        r = self.mutate_content(f)
        self.assertFails(r, "bad1", "appear in none of its sources")

    def test_a_short_quote_does_not_count_as_a_source(self):
        def f(c):
            c["areas"][0]["bullets"].append({"id": "bad2", "text": "Client is a smoker", "status": "still open",
                                             "src": [{"line": 9, "quote": "Yes I"}]})
        self.assertFails(self.mutate_content(f), "at least 10 characters")

    def test_a_figure_spoken_in_words_must_also_be_shown_by_a_document(self):
        def f(c):   # R1,100.00 is only spoken in the transcript ("one thousand one hundred rand"): no document cited
            c["areas"][0]["bullets"][0]["src"] = [self.src("one thousand one hundred rand a month")]
        self.assertFails(self.mutate_content(f), "figures", "appear in none of its sources")

    def test_a_policy_number_must_be_in_a_source(self):
        def f(c):
            c["areas"][0]["bullets"][0]["text"] = "BrightRock Revised Reduced Quote CP 999999999, R1,100.00 p.m."
        self.assertFails(self.mutate_content(f), "999999999")

    def test_a_document_without_a_text_copy_is_flagged_not_trusted_silently(self):
        self.to_ready()
        os.remove(self.p("docs", "BrightRock quote 100000001.txt"))
        r = self.verify("pre")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("cannot be machine-checked", r.stdout)


class WrongRun(Base):
    def test_wrong_client_in_content_fails(self):
        r = self.mutate_content(lambda c: c.update(client={"first": "Jane", "surname": "Doe"}))
        self.assertFails(r, "content.json is for Jane Doe but Paul's request was for Sam Testcase")

    def test_wrong_date_in_content_fails(self):
        r = self.mutate_content(lambda c: c.update(meeting_date="07/11/2026"))
        self.assertFails(r, "Paul's request was for 05/10/2026")

    def test_an_impossible_date_fails(self):
        r = self.mutate_content(lambda c: c.update(meeting_date="31/02/2026"))
        self.assertFails(r, "not a real date")

    def test_a_transcript_that_never_mentions_the_client_fails(self):
        self.to_ready()
        rj = self.load("run.json")
        rj["client"] = {"first": "Zelda", "surname": "Quillfeather"}
        self.write("run.json", rj)
        c = self.content()
        c["client"] = {"first": "Zelda", "surname": "Quillfeather"}
        self.write("content.json", c)
        self.assertFails(self.verify("pre"), "never mentions the client's surname")

    def test_a_run_not_started_with_client_and_date_fails(self):
        self.to_ready()
        self.write("run.json", {"meeting_type": "followup", "steps": {}})
        self.assertFails(self.verify("pre"), "was not started with the client and meeting date")

    def test_a_run_that_skipped_the_driver_cannot_pass(self):
        self.to_final()
        os.remove(self.p("run.json"))
        self.assertFails(self.verify(), "was not started with the client and meeting date")
        self.write("run.json", self.run_json("followup", done=["locate"]))
        self.assertFails(self.verify(), "steps not completed through the driver")


class BadShapes(Base):
    """Plausible mistakes in content.json must give a clear FAIL line, never a traceback."""
    def check(self, fn, needle):
        r = self.mutate_content(fn, stage="final")
        self.assertNotIn("Traceback", r.stdout + r.stderr)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn(needle, r.stdout)

    def test_areas_as_an_object(self):
        self.check(lambda c: c.update(areas={"risk": [{"id": "x", "text": "t", "src": []}]}), "areas must be a LIST")

    def test_src_as_a_dict(self):
        self.check(lambda c: c["actions"][0].update(src={"line": 5, "quote": "x"}), "src of item a1 must be a list")

    def test_src_as_a_list_of_strings(self):
        self.check(lambda c: c["actions"][0].update(src=["line 5"]), "src of item a1 must be a list")

    def test_client_as_a_string(self):
        self.check(lambda c: c.update(client="Sam Testcase"), "client must look like")

    def test_status_as_a_number(self):
        self.check(lambda c: c["areas"][0]["bullets"][0].update(status=5), "status of item b1 must be text")

    def test_text_as_a_number(self):
        self.check(lambda c: c["actions"][0].update(text=12), "every item needs text")

    def test_action_id_as_a_list(self):
        self.check(lambda c: c["checks"]["owner_change"].update(action_id=["a4"]), "must be one item id as text")

    def test_checks_as_a_list(self):
        self.check(lambda c: c.update(checks=[]), "checks must be an object")

    def test_content_as_a_list(self):
        self.to_ready()
        self.write("content.json", [])
        r = self.verify("final")
        self.assertNotIn("Traceback", r.stdout + r.stderr)
        self.assertIn("content must be an object", r.stdout.replace("content.json must be an object", "content must be an object"))

    def test_ledger_add_before_prep_and_pandoc_missing_are_clear(self):
        src = os.path.join(self.tmp, "t.docx")
        spit(src, "not really a docx", "w")
        r = sh("tx.py", "prep", src, self.run_dir)       # a real run has pandoc; here we hide it by emptying PATH
        env = dict(os.environ, PATH="/nonexistent")
        import subprocess, sys
        r = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts", "tx.py"),
                            "prep", src, self.run_dir], capture_output=True, text=True, env=env)
        self.assertEqual(r.returncode, 4)
        self.assertIn("pandoc is not installed", r.stderr)
        self.assertNotIn("Traceback", r.stderr)


class Wording(Base):
    def test_the_status_phrase_the_rules_ask_for_is_accepted(self):
        r = self.mutate_content(lambda c: c["areas"][0]["bullets"][0].update(status="Verbally confirmed - awaiting email reply to proposal"))
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertNotIn("is not one of the skill's status words", r.stdout)

    def test_on_hold_is_a_documented_status(self):
        self.assertIn("**on hold**", slurp(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "references", "06a-planner-note.md")))

    def test_the_final_printout_says_what_paul_should_glance_at(self):
        self.to_final()
        out = self.verify().stdout
        self.assertIn("WHAT PAUL SHOULD GLANCE AT", out)
        self.assertIn("left out: line", out)                        # the plain facts that were left out of the report, with their reasons
        self.assertIn("garbled line", out)
        self.assertIn("sha256", out)


if __name__ == "__main__":
    unittest.main()
