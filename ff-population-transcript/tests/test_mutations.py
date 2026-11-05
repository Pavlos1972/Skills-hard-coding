"""MUTATION CHECK: take one passing end-to-end run, change ONE thing at a time, and confirm the checker catches it.

The passing run is played once for the whole class; every test works on its own copy of the finished run folder."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from support import Chat, H, SCRIPTS, jdump, jload, slurp, spit, sh


class Mutations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        class C(Chat):
            def runTest(self):
                pass
        cls.chat = C()
        cls.chat.setUp()
        cls.chat.through("handoffs")
        cls.base = cls.chat.run_dir
        cls.tmpdirs = []

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.chat.tmp, True)
        for d in cls.tmpdirs:
            shutil.rmtree(d, True)

    def setUp(self):
        d = tempfile.mkdtemp(prefix="wrmut-")
        self.__class__.tmpdirs.append(d)
        self.run_dir = os.path.join(d, "run")
        shutil.copytree(self.base, self.run_dir)

    def p(self, *a):
        return os.path.join(self.run_dir, *a)

    def verify(self, *extra):
        return sh("verify.py", self.run_dir, *extra)

    def caught(self, text, *extra):
        out = self.verify(*extra)
        self.assertEqual(out.returncode, 1, "NOT CAUGHT:\n" + out.stdout[-2500:])
        self.assertIn(text, out.stdout)
        self.assertIn("NOT COMPLETE", out.stdout)

    def edit_content(self, fn):
        c = jload(self.p("content.json"))
        fn(c)
        jdump(self.p("content.json"), c)

    def row(self, c, rid):
        return next(r for s in c["sections"] for b in s["blocks"] for r in b["rows"] if r["id"] == rid)

    def test_the_untouched_run_passes(self):
        out = self.verify()
        self.assertEqual(out.returncode, 0, out.stdout[-3000:])
        self.assertIn("RESULT: PASS", out.stdout)
        self.assertIn("SOURCES USED", out.stdout)          # the default printout is the SHORT audit (Paul, 05/11/2026)
        self.assertIn("GLANCE AT", out.stdout)
        self.assertIn("DELIVERY LINE", out.stdout)
        self.assertIn("FONT:", out.stdout)
        self.assertNotIn("PROVEN BY THE PROGRAM", out.stdout)
        full = self.verify("--full")                        # the long report is still there on request
        self.assertEqual(full.returncode, 0, full.stdout[-3000:])
        self.assertIn("SOURCE REPORT", full.stdout)
        self.assertIn("WHAT PAUL SHOULD GLANCE AT", full.stdout)
        self.assertIn("PROVEN BY THE PROGRAM", full.stdout)

    def test_wrong_standing_abi(self):
        self.edit_content(lambda c: self.row(c, "lc_wol").update(bullets=["5%"]))
        self.caught("must read 3% (the standing value")

    def test_a_deleted_source(self):
        self.edit_content(lambda c: self.row(c, "occ").update(src=[]))
        self.caught("has no source")

    def test_a_changed_figure_in_the_content_after_the_check(self):
        self.edit_content(lambda c: self.row(c, "gross").update(bullets=["R 54 000.00"]))
        self.caught("content.json is not what the program composes")
        self.caught("the printed value 'R 54 000.00' is not the form's value")

    def test_a_tampered_pdf(self):
        pdf = [f for f in os.listdir(self.p("out")) if f.endswith(".pdf")][0]
        with open(self.p("out", pdf), "ab") as f:
            f.write(b"\n% a late edit\n")
        self.caught("the PDF on disk is not the one build.py made")

    def test_a_different_pdf_with_the_same_name(self):
        pdf = [f for f in os.listdir(self.p("out")) if f.endswith(".pdf")][0]
        from reportlab.pdfgen import canvas
        c = canvas.Canvas(self.p("out", pdf))
        c.drawString(72, 700, "A hand-made page that is not the Fact Find")
        c.save()
        self.caught("the PDF on disk is not the one build.py made")

    def test_a_word_file_next_to_the_pdf(self):
        spit(self.p("out", "Fact Find Transcript - 05.11.26 - (Pat Samplecase).docx"), "x")
        self.caught("never a Word file")

    def test_an_overlay_note_edited_after_the_build(self):
        ov = jload(self.p("overlay.json"))
        ov["notes"][0]["text"] = "The will is up to date"
        jdump(self.p("overlay.json"), ov)
        self.caught("content.json is not what the program composes")

    def test_a_form_value_edited_after_reading(self):
        fr = jload(self.p("form_read.json"))
        fr["fields"]["gross"]["v"] = "R 99 000.00"
        jdump(self.p("form_read.json"), fr)
        self.caught("form_read.json is not what the program reads from the form's file")

    def test_the_forms_own_file_edited_after_reading(self):
        f = jload(self.p("form_source.json"))
        f["f"]["net"]["v"] = "R 1.00"
        jdump(self.p("form_source.json"), f)
        self.caught("form_read.json is not what the program reads")

    def test_the_transcript_edited_after_prep(self):
        t = slurp(self.p("transcript.txt")).replace("one-year diploma", "five-year degree")
        spit(self.p("transcript.txt"), t)
        self.caught("transcript.txt changed after prep")

    def test_a_ledger_entry_that_covers_nothing(self):
        led = jload(self.p("ledger.json"))
        led["entries"][1]["covered_by"] = []
        jdump(self.p("ledger.json"), led)
        self.caught("is not covered by any fill, difference, note, request or answer")

    def test_a_ledger_entry_with_an_invented_quote(self):
        led = jload(self.p("ledger.json"))
        led["entries"][0]["quote"] = "words that were never said on this call"
        jdump(self.p("ledger.json"), led)
        self.caught("quote not found at line")

    def test_a_chunk_of_the_second_read_removed(self):
        st = jload(self.p("state.json"))
        st["reads"] = [r for r in st["reads"] if not (r["pass"] == 2 and r["chunk"] == 3)]
        jdump(self.p("state.json"), st)
        self.caught("Pass 2 has NOT served every chunk")

    def test_a_claim_that_the_call_contradicts(self):
        cl = jload(self.p("claims.json"))
        cl["wemail"] = {"as": "Not discussed", "terms": ["email address", "e-mail", "gmail", "personal email", "email"], "hits": [], "docs": [], "reviewed": "", "searched": ""}
        jdump(self.p("claims.json"), cl)
        self.caught("the search still finds call lines")

    def test_a_saved_file_listing_with_another_size(self):
        rc = jload(self.p("receipt.json"))
        rc["saved"]["listed_size"] = "999"
        jdump(self.p("receipt.json"), rc)
        self.caught("saved.listed_size is 999 but the local PDF is")

    def test_the_wrong_save_folder(self):
        rc = jload(self.p("receipt.json"))
        rc["saved"]["folder"] = "C:\\liferisk.co.za\\Company - Paul\\New Business\\Samplecase, Pat\\5. Admin"
        jdump(self.p("receipt.json"), rc)
        self.caught("does not end in the client's '2. Fact Find' folder")

    def test_the_teams_hand_over_for_another_client(self):
        rc = jload(self.p("receipt.json"))
        tr = rc["teams"]["run_folder"]
        other = tempfile.mkdtemp(prefix="wrteams-")
        self.__class__.tmpdirs.append(other)
        jdump(os.path.join(other, "run.json"), {"meeting_type": "first", "client": {"first": "Robin", "surname": "Testcase"}, "date": "05/11/2026"})
        rc["teams"]["run_folder"] = other
        jdump(self.p("receipt.json"), rc)
        self.caught("is not a first-meeting run for Pat Samplecase on 05/11/2026")

    def test_a_missing_hand_over_receipt(self):
        rc = jload(self.p("receipt.json"))
        del rc["summary"]
        jdump(self.p("receipt.json"), rc)
        self.caught("summary{invoked, abi_same}")

    def test_a_step_that_was_not_done_through_the_driver(self):
        rj = jload(self.p("run.json"))
        del rj["steps"]["crosscheck"]
        jdump(self.p("run.json"), rj)
        self.caught("steps not completed through the driver")

    def test_a_page_image_removed(self):
        os.remove(self.p("out", "page-03.png"))
        self.caught("page images for the visual check are missing")

    def test_a_row_cut_or_edited_in_the_pdf_text_is_seen_by_rebuilding(self):
        # content changed AND the PDF rebuilt by hand with the wrong text: the rebuild from content.json no longer matches the composed content
        self.edit_content(lambda c: self.row(c, "net").update(bullets=["R 1.00"]))
        sh("build.py", self.run_dir)
        self.caught("content.json is not what the program composes")

    def test_receipts_from_before_a_rebuild_do_not_count(self):
        ov = jload(self.p("overlay.json"))
        ov["notes"][0]["text"] = "The will was last updated before the children were born"
        jdump(self.p("overlay.json"), ov)
        sh("run.py", "compose", self.run_dir, ok=True)
        sh("build.py", self.run_dir, ok=True)
        self.caught("hand-over receipts recorded for an older build")
        rj = jload(self.p("run.json"))
        self.assertNotIn("check", rj["steps"])                  # the rebuild re-opened the later steps

    def test_a_correction_composed_but_not_built_is_caught(self):
        ov = jload(self.p("overlay.json"))
        ov["notes"][0]["text"] = "The will was drawn up before the children were born"
        jdump(self.p("overlay.json"), ov)
        sh("run.py", "compose", self.run_dir, ok=True)                 # content.json is now right ... but the PDF still shows the old note
        self.caught("content.json changed after the PDF was built")

    # ---- mutant-killing tests (M5): each one drives the checker to a message that only ONE line of the checker can produce
    def test_text_from_the_forms_parking_list_printed_in_the_document(self):
        parked = jload(self.p("form_source.json"))["unplaced"][0]["fact"]
        self.edit_content(lambda c: self.row(c, "occ")["bullets"].append(parked))
        self.caught("text from the form's parking list, summaries or drafted action list (never a source) is printed")

    def test_the_forms_own_drafted_action_text_printed_in_the_document(self):
        drafted = jload(self.p("form_source.json"))["f"]["pa_actions"]["v"]
        self.edit_content(lambda c: self.row(c, "occ")["bullets"].append(drafted))
        self.caught("text from the form's parking list, summaries or drafted action list (never a source) is printed")

    def test_the_thrown_out_company_look_up_text_printed_in_the_document(self):
        text = jload(self.p("form_source.json"))["f"]["co_does"]["v"]
        self.edit_content(lambda c: self.row(c, "occ")["bullets"].append(text))
        self.caught("the company look-up text was meant to be thrown out")

    def test_an_identifier_that_is_not_in_its_sources_digit_for_digit(self):
        def ed(c):
            self.row(c, "idno").update(status="filled", bullets=[H.make_id("800101", 5009)],
                                       src=[{"line": 12, "quote": "Your name is Pat Samplecase"}])
        self.edit_content(ed)
        self.caught("is not in its sources digit for digit")

    def test_a_hand_made_pdf_whose_hash_was_also_rewritten_is_seen_by_its_text(self):
        import hashlib
        st = jload(self.p("state.json"))
        pdf = self.p("out", st["build"]["pdf"])
        from reportlab.pdfgen import canvas
        c = canvas.Canvas(pdf)
        c.drawString(72, 700, "A hand-made page that is not the Fact Find")
        c.save()
        with open(pdf, "rb") as f:
            st["build"]["pdf_sha"] = hashlib.sha256(f.read()).hexdigest()
        st["build"]["pdf_size"] = os.path.getsize(pdf)
        jdump(self.p("state.json"), st)
        self.caught("the PDF text is not what content.json produces")

    def test_business_parts_printed_for_a_client_who_is_not_a_business_owner(self):
        def ed(c):
            c["sections"][0]["blocks"].append({"kind": "fields", "sub": "Business assurance", "rows": [
                {"id": "bs_req", "label": "Business assurance", "bullets": ["Yes"], "src": [{"form": "bs_req"}], "status": "confirmed", "flags": [], "kind": "text"}]})
        self.edit_content(ed)
        self.caught("Business Assurance and the other business parts are printed")

    def test_an_overview_whose_text_copy_was_lost_fails_the_checker(self):
        os.remove(self.p("docs", "WR Overview Pat Samplecase.txt"))
        self.caught("has no text copy: it cannot be accepted")

    def test_an_overview_text_that_is_not_this_clients_fails_the_checker(self):
        spit(self.p("docs", "WR Overview Pat Samplecase.txt"), "An invented overview of nobody in particular. Fakeco unit trust R 777 000.00")
        self.caught("does not mention the client")

    def test_the_insurer_of_a_quote_is_shown_once_not_twice(self):
        c = jload(self.p("content.json"))
        q = self.row(c, "quote.fna")
        self.assertTrue(q.get("hidden"), "the form already shows the insurer and the basis: the quote row is kept for the checker, not printed")
        st = jload(self.p("state.json"))
        text = subprocess.run(["pdftotext", "-layout", self.p("out", st["build"]["pdf"]), "-"], capture_output=True, text=True).stdout
        self.assertNotIn("Insurer: BrightRock", text)
        self.assertNotIn("insurer and basis", text.lower())

    def test_a_preset_left_out_of_the_source_report(self):
        self.edit_content(lambda c: c["report"].update(presets=[]))
        self.caught("preset values missing from the source report")

    def test_the_skill_updated_while_the_run_was_going_is_reported(self):
        rj = jload(self.p("run.json"))
        rj["skill_stamp"] = "1999-01-01 00:00"
        jdump(self.p("run.json"), rj)
        out = self.verify()
        self.assertIn("the skill was updated while this run was in progress", out.stdout)


if __name__ == "__main__":
    unittest.main()
