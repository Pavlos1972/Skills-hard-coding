"""The program must REFUSE (non-zero exit, a plain message) in each of the cases Paul asked about. Invented data only."""
import json
import os
import subprocess
import sys

from support import Chat, H, SCRIPTS, drv, sh, jdump, jload, slurp, spit, CLIENT, make_form_pdf
from fixtures import household as HH


class Steps(Chat):
    def test_a_step_cannot_be_skipped(self):
        self.s_start()
        r = self.refused("done", self.run_dir, "prep")
        self.assertEqual(r.returncode, 3)
        self.assertIn("finish step 'locate' first", r.stderr)
        r = self.refused("done", self.run_dir, "locate")
        self.assertIn("no successful access entry for 'transcript'", r.stdout)
        self.assertIn("run.py access --need form", r.stdout)     # nothing about the form was logged: the program says what to do

    def test_a_step_without_its_proof_does_not_open_the_next(self):
        self.through("locate")
        self.refused("done", self.run_dir, "form", text="has not been read by the program")
        self.refused("done", self.run_dir, "prep", text="finish step 'form' first")

    def test_the_transcript_must_be_read_twice(self):
        self.through("documents")
        r = sh("tx.py", "chunk", self.run_dir, 2, 1)
        self.assertEqual(r.returncode, 3)
        self.assertIn("Pass 2 cannot start until Pass 1", r.stderr)
        self.refused("done", self.run_dir, "pass1", text="has not served every chunk")
        sh("tx.py", "chunk", self.run_dir, 1, 1, ok=True)
        r = sh("tx.py", "chunk", self.run_dir, 1, 2)
        self.assertEqual(r.returncode, 3)                         # chunk 1 has no ledger entry and no acknowledgement
        self.assertIn("no ledger entry and no acknowledgement", r.stderr)
        self.s_pass1()
        self.refused("done", self.run_dir, "pass2", text="Pass 2 has not served every chunk")
        self.refused("done", self.run_dir, "scan", text="finish step 'pass2' first")


class FormFile(Chat):
    def test_schema_other_than_3_0_stops_with_one_line_and_saves_nothing(self):
        bad = self.form
        bad["schema"] = "3.1"
        jdump(self.form_path, bad)
        self.s_start()
        self.s_locate()
        r = drv("form", self.run_dir, self.form_path)
        self.assertEqual(r.returncode, 4)
        self.assertIn("schema '3.1'", r.stdout)
        self.assertIn("Tell Paul in one line", r.stdout)
        self.assertEqual(len(r.stdout.strip().splitlines()), 1)
        self.assertFalse(os.path.exists(self.p("form_read.json")))

    def test_a_file_that_is_not_the_form_is_refused_by_content_not_name(self):
        other = {"app": "something-else", "schema": "3.0", "f": {}}
        jdump(self.form_path, other)
        self.s_start()
        self.s_locate()
        r = drv("form", self.run_dir, self.form_path)
        self.assertEqual(r.returncode, 4)
        self.assertIn("is not the Fact Find form's data file", r.stdout)
        # ... and by content: a file with the wrong name but the right content IS recognised
        odd = os.path.join(self.tmp, "notes final v2.json")
        jdump(odd, HH.pat_form())
        r = sh("ffform.py", "identify", odd, self.form_path)
        self.assertIn("FORM DATA FILE  notes final v2.json", r.stdout)
        self.assertIn("not the form's data file", r.stdout)

    def test_the_form_of_another_client_or_date_is_refused(self):
        f = self.form
        f["f"]["sname"]["v"] = "Someoneelse"
        jdump(self.form_path, f)
        self.s_start()
        self.s_locate()
        r = drv("form", self.run_dir, self.form_path)
        self.assertEqual(r.returncode, 5)
        self.assertIn("the form is for Pat Someoneelse but this run is for Pat Samplecase", r.stdout)
        self.assertFalse(os.path.exists(self.p("form_read.json")))
        f = HH.pat_form()
        f["f"]["date"]["v"] = "06/11/2026"
        jdump(self.form_path, f)
        r = drv("form", self.run_dir, self.form_path)
        self.assertEqual(r.returncode, 5)
        self.assertIn("Date completed is 06/11/2026 but Paul's meeting date is 05/11/2026", r.stdout)

    def test_missing_form_file_stops_and_asks_and_goes_on_only_with_pauls_words(self):
        self.s_start()
        self.access("transcript")
        # not asked before all three routes were tried and logged
        self.access("form", "device", "fail", "device_stage_files", "not on the drive")
        r = self.refused("ask", self.run_dir, "--need", "form", "--searched", "the 2. Fact Find folder")
        self.assertIn("have not been tried", r.stderr)
        r = self.refused("done", self.run_dir, "locate")
        self.assertIn("were not tried and logged", r.stdout)
        self.access("form", "m365", "fail", "sharepoint_search", "nothing found")
        self.access("form", "zapier", "fail", "zapier_find", "nothing found")
        r = self.refused("done", self.run_dir, "locate")
        self.assertIn("STOP: the form's data file is missing on all three routes. Ask Paul", r.stdout)
        # the program words the question itself
        r = self.ok("ask", self.run_dir, "--need", "form", "--searched", "the 2. Fact Find folder on the drive, SharePoint and Zapier")
        self.assertIn("use the filled-in Manual Fact Find PDF", r.stdout)
        self.assertIn("or work from the transcript alone", r.stdout)
        r = self.refused("done", self.run_dir, "locate")
        self.assertIn("Paul has not answered", r.stdout)
        self.refused("answer", self.run_dir, "--need", "form", "--said", "ok")                      # a choice is needed
        self.refused("answer", self.run_dir, "--need", "form", "--said", "x", "--choice", "manual")  # his own words, not a letter
        self.ok("answer", self.run_dir, "--need", "form", "--said", "Use the transcript alone, I did not save the form this time", "--choice", "transcript")
        self.ok("done", self.run_dir, "locate")
        self.ok("done", self.run_dir, "form")                       # nothing to read: settled by Paul's answer
        self.assertEqual(self.load("run.json")["form_mode"], "transcript")
        # the manual PDF is read only when Paul chose it
        r = self.refused("source", self.run_dir, "--kind", "Manual Fact Find", "--path", "C:\\x\\Company - Paul\\a.pdf", "--date", "2026-11-05", "--read", "yes")
        self.assertIn("only when the form's data file is missing and Paul chose it", r.stderr)

    def test_a_form_that_was_not_missing_cannot_be_declared_missing(self):
        self.through("locate")
        self.refused("ask", self.run_dir, "--need", "form", "--searched", "the whole folder, again")


class FormPdf(Chat):
    pdf_drop = ("tax", "edu")

    def test_a_value_missing_from_the_saved_pdf_must_be_looked_at(self):
        self.s_start()
        self.s_locate()
        make_form_pdf(self.pdf_path, self.form, drop=self.pdf_drop, extra_lines=["Highest education: Diploma"])      # the PDF shows another value for education
        self.ok("form", self.run_dir, self.form_path)
        r = self.ok("formpdf", self.run_dir, self.pdf_path)
        self.assertIn("NOT IN THE PDF: Highest education (edu)", r.stdout)
        r = self.refused("done", self.run_dir, "form")
        self.assertIn("nobody looked", r.stdout)                                  # a value missing from the PDF that nobody looked at
        self.refused("pdfreview", self.run_dir, "--key", "edu", "--result", "disagree", "--quote", "invented words that are not there")
        self.refused("pdfreview", self.run_dir, "--key", "edu", "--result", "disagree", "--quote", "WR Fact Find v3.0")           # needs the PDF's own value
        self.refused("pdfreview", self.run_dir, "--key", "edu", "--result", "disagree", "--quote", "WR Fact Find v3.0", "--pdf-value", "Diploma")   # ... and the quote must contain it (A8)
        self.ok("pdfreview", self.run_dir, "--key", "edu", "--result", "disagree", "--quote", "Highest education: Diploma", "--pdf-value", "Diploma")
        self.ok("done", self.run_dir, "form")
        self.ok("compose", self.run_dir)
        flags = [f["text"] for sec in self.load("content.json")["sections"] for b in sec["blocks"] for r_ in b["rows"] for f in r_["flags"]]
        self.assertTrue(any("data file says 3-year degree" in f and "saved PDF says Diploma" in f for f in flags), flags)

    def test_a_value_hidden_by_editing_the_pdf_record_by_hand_is_caught(self):
        self.s_start()
        self.s_locate()
        make_form_pdf(self.pdf_path, self.form, drop=self.pdf_drop)
        self.ok("form", self.run_dir, self.form_path)
        r = self.ok("formpdf", self.run_dir, self.pdf_path)
        self.assertIn("NOT IN THE PDF: Highest education (edu)", r.stdout)
        rec = self.load("form_pdf.json")
        rec["not_found"] = []                                           # someone empties the list instead of looking at the PDF
        self.write("form_pdf.json", rec)
        r = self.refused("done", self.run_dir, "form")
        self.assertIn("form_pdf.json is not what the program finds", r.stdout)

    def test_a_missing_saved_pdf_needs_all_three_routes(self):
        self.s_start()
        self.s_locate()
        self.ok("form", self.run_dir, self.form_path)
        self.refused("formpdf", self.run_dir, "--none", "not in the folder")
        for route in ("device", "m365", "zapier"):
            self.access("formpdf", route, "fail", "t_" + route, "not found")
        self.ok("formpdf", self.run_dir, "--none", "searched the 2. Fact Find folder on all three routes")
        self.ok("done", self.run_dir, "form")


class Sources(Chat):
    def test_a_quote_not_in_the_transcript_is_refused(self):
        self.through("prep")
        self.s_documents()
        sh("tx.py", "chunk", self.run_dir, 1, 1, ok=True)
        r = self.refused("ledger", self.run_dir, "add", "--line", 3, "--kind", "gap", "--quote", "words nobody ever said on this call")
        self.assertIn("not found at transcript line 3", r.stderr)
        self.refused("ledger", self.run_dir, "add", "--line", 3, "--kind", "made-up", "--quote", "Is it fine if we record")

    def test_a_cross_check_quote_must_be_real_and_a_difference_needs_the_calls_value(self):
        self.through("contact")
        self.refused("cross", self.run_dir, "--key", "edu", "--r", "differs", "--line", self.L("one-year diploma"), "--quote", "He studied law abroad for six years")
        self.refused("cross", self.run_dir, "--key", "edu", "--r", "differs", "--line", self.L("one-year diploma"), "--quote", "I did a one-year diploma after school")     # no value
        self.refused("cross", self.run_dir, "--key", "edu", "--r", "differs", "--line", self.L("one-year diploma"), "--quote", "I did a one-year diploma after school", "--value", "3-year degree")
        self.refused("done", self.run_dir, "crosscheck", text="never compared")

    def test_a_difference_is_flagged_with_both_values_in_the_pdf(self):
        self.through("pdf")
        content = self.load("content.json")
        text = json.dumps(content, ensure_ascii=False)
        self.assertIn("Difference: the form says 3-year degree; on the call: a one-year diploma (line", text)
        pages = subprocess.run(["pdftotext", os.path.join(self.p("out"), content["file_name"]), "-"], capture_output=True, text=True).stdout
        self.assertIn("3-year degree", pages)
        self.assertIn("one-year diploma", pages)

    def test_a_row_without_a_source_fails_the_checker(self):
        self.through("content")
        ov = self.load("overlay.json")
        ov["fills"].append({"id": "o99", "key": "debts.1.notes", "value": "Fixed rate", "src": []})
        self.write("overlay.json", ov)
        r = self.refused("compose", self.run_dir)                       # the program refuses an entry without a source at once (M2)
        self.assertIn("needs `src`", r.stdout + r.stderr)

    def test_a_fill_with_a_quote_that_is_not_in_the_call_fails(self):
        self.through("content")
        ov = self.load("overlay.json")
        ov["fills"].append({"id": "o99", "key": "debts.1.notes", "value": "Fixed rate", "src": [{"line": 5, "quote": "a rate that was never discussed on this call"}]})
        self.write("overlay.json", ov)
        self.ok("compose", self.run_dir)
        out = self.verify("--stage", "pre")
        self.assertIn("source quote not found at transcript line 5", out.stdout)

    def test_the_form_wins_a_fill_may_not_overwrite_a_populated_field(self):
        self.through("content")
        ov = self.load("overlay.json")
        ov["fills"].append({"id": "o99", "key": "occ", "value": "Director", "src": [{"line": self.L("operations manager"), "quote": "I'm an operations manager"}]})
        self.write("overlay.json", ov)
        self.ok("compose", self.run_dir)
        out = self.verify("--stage", "pre")
        self.assertIn("already has a value in the form: the form wins", out.stdout)

    def test_another_brokers_folder_is_refused(self):
        self.through("prep")
        r = self.refused("source", self.run_dir, "--kind", "Other document", "--path", "C:\\liferisk.co.za\\Company - WR Clients\\Another Broker (Client Files)\\x\\a.pdf", "--date", "2026-11-01", "--read", "yes")
        self.assertIn("another broker's folder", r.stderr)

    def test_an_overview_may_be_called_missing_only_after_two_routes_were_logged(self):
        self.through("prep")
        r = self.refused("source", self.run_dir, "--kind", "Overview", "--none", "searched the 1. Overview folder, none found")
        self.assertIn("at least two routes", r.stderr)


class Rules(Chat):
    def test_a_total_that_does_not_reconcile_is_caught(self):
        self.through("content")
        c = self.load("content.json")
        for sec in c["sections"]:
            for b in sec["blocks"]:
                for r in b["rows"]:
                    if r["id"] == "total.debts_monthly":
                        r["bullets"] = ["R 12 500.00"]            # the credit-life debt left out of the total
        self.write("content.json", c)
        out = self.verify("--stage", "pre")
        self.assertEqual(out.returncode, 1)
        self.assertIn("debt is never left out of a calculation (not even for credit life)", out.stdout)
        self.assertIn("is not the sum of its components", out.stdout)

    def test_a_risk_calculation_that_leaves_a_debt_out_is_flagged_not_silently_accepted(self):
        f = HH.pat_form()
        f["f"]["lc_dr"]["v"] = "R 12 500.00"
        jdump(self.form_path, f)
        self.form = f
        self.through("content")
        text = json.dumps(self.load("content.json"), ensure_ascii=False)
        self.assertIn("Debt is never left out because of credit life: Paul decides.", text)
        self.assertIn("R 12 500.00", text)
        self.assertIn("R 19 000.00", text)

    def test_a_standing_abi_that_is_wrong_is_caught(self):
        self.through("content")
        c = self.load("content.json")
        for sec in c["sections"]:
            for b in sec["blocks"]:
                for r in b["rows"]:
                    if r["id"] == "dd_abiv":
                        r["bullets"] = ["5%"]
        self.write("content.json", c)
        out = self.verify("--stage", "pre")
        self.assertIn("must read 3% (the standing value; only Paul can state otherwise)", out.stdout)

    def test_pd_fractured_never_shows_a_life_cover_wol_line(self):
        self.through("content")
        c = self.load("content.json")
        for sec in c["sections"]:
            for b in sec["blocks"]:
                if b["sub"] == "Permanent disability: fractured cover":
                    b["rows"].append({"id": "x", "label": "Life Cover (WOL) ABI", "bullets": ["3%"], "src": [{"standing": "abi:lc_wol"}], "flags": [], "status": "standing"})
        self.write("content.json", c)
        out = self.verify("--stage", "pre")
        self.assertIn("must not carry a 'Life Cover (WOL) ABI' line", out.stdout)

    def test_a_quarter_of_the_facts_in_one_line_is_refused(self):
        self.through("content")
        ov = self.load("overlay.json")
        ov["notes"].append({"id": "o50", "section": "medical", "text": "The will is old. The medical aid is Discovery. The gap cover is not in place",
                            "src": [{"line": self.L("not been updated since before"), "quote": "it has not been updated since before the children were born"}]})
        self.write("overlay.json", ov)
        self.ok("compose", self.run_dir)
        out = self.verify("--stage", "pre")
        self.assertIn("one fact per line", out.stdout)

    def test_a_policy_number_not_from_a_policy_schedule_is_refused(self):
        self.through("content")
        ov = self.load("overlay.json")
        ov["notes"].append({"id": "o51", "section": "cover", "text": "Policy number QX99887 is the BrightRock policy",
                            "src": [{"line": self.L("BrightRock policy"), "quote": "Yes, the BrightRock policy"}]})
        self.write("overlay.json", ov)
        self.ok("compose", self.run_dir)
        out = self.verify("--stage", "pre")
        self.assertIn("prints policy number 'QX99887' that is not confirmed by a policy schedule", out.stdout)
        # ... and from the Overview it is still refused
        ov["policy_numbers"] = [{"id": "o52", "found": "QX99887", "resolved": "QX99887", "ref": "WR Overview Pat Samplecase", "quote": "BrightRock life cover"}]
        self.write("overlay.json", ov)
        self.ok("compose", self.run_dir)
        out = self.verify("--stage", "pre")
        self.assertIn("must come from a recorded Policy schedule", out.stdout)

    def test_a_policy_number_from_the_schedule_wins_and_the_difference_is_flagged(self):
        self.through("prep")
        sched = os.path.join(self.tmp, "sched.txt")
        spit(sched, "BrightRock policy schedule (invented) for Pat Samplecase. Policy number: ZZ445566. Life cover.")
        self.ok("source", self.run_dir, "--kind", "Policy schedule", "--path", "C:\\liferisk.co.za\\Company - Paul\\New Business\\Samplecase, Pat\\Policies\\sched.pdf", "--date", "2026-10-01",
                "--read", "yes", "--ref", "BrightRock schedule", "--text-file", sched)
        import compose
        inp = compose.load_inputs(self.run_dir)
        inp["form"]["lists"]["risk"][0]["d"]["notes"] = "Fractured life cover, policy number AB123456"
        inp["overlay"] = {"policy_numbers": [{"id": "o1", "found": "AB123456", "resolved": "ZZ445566", "ref": "BrightRock schedule", "quote": "Policy number: ZZ445566"}]}
        c = compose.compose(inp)
        text = json.dumps(c, ensure_ascii=False)
        self.assertIn("Fractured life cover, policy number ZZ445566", text)
        self.assertIn("the form or Overview says AB123456; the policy schedule says ZZ445566", text)

    def test_business_parts_are_not_printed_for_a_non_owner(self):
        f = HH.pat_form()
        f["f"]["biz_name"] = {"v": "Samplecase Consulting", "st": "confirmed"}
        f["f"]["bs_req"] = {"v": "Yes", "st": "confirmed"}
        jdump(self.form_path, f)
        self.form = f
        make_form_pdf(self.pdf_path, f)
        self.through("content")
        c = self.load("content.json")
        subs = [b["sub"] for s in c["sections"] for b in s["blocks"]]
        self.assertNotIn("Business", subs)
        self.assertNotIn("Business assurance", subs)
        self.assertTrue(any("Business owner is Yes" in g for g in c["glance"]), c["glance"])


class QuoteRequests(Chat):
    def setUp(self):
        super().setUp()
        f = HH.pat_form()
        f["f"]["fna_type"]["v"] = ""
        f["f"]["fna_type"]["st"] = "empty"
        f["f"]["fna_ins"]["v"] = ""
        f["f"]["fna_ins"]["st"] = "empty"
        jdump(self.form_path, f)
        self.form = f
        make_pdf = __import__("support").make_form_pdf
        make_pdf(self.pdf_path, f)

    def test_a_quote_request_without_insurer_or_basis_is_refused_and_asks_paul(self):
        self.through("crosscheck")
        self.ok("compose", self.run_dir)
        r = self.ok("claim", self.run_dir, "--all-empty")
        r = self.ok("compose", self.run_dir)
        self.assertIn("quote.fna", r.stdout)
        out = self.verify("--stage", "pre")
        self.assertIn("there is no default. ASK PAUL", out.stdout)
        self.assertIn("Which insurer should the FNA, Shortfall or Reduced quote(s) be requested from, and is it New Business or Servicing?", out.stdout)

    def test_paul_answers_and_the_basis_needs_a_source_that_says_servicing(self):
        self.through("crosscheck")
        self.write("overlay.json", {})
        self.ok("compose", self.run_dir)
        self.ok("claim", self.run_dir, "--all-empty")
        # Paul's words are recorded by the PROGRAM (ask, then answer); the overlay only refers to them
        self.ok("ask", self.run_dir, "--need", "fna_quote", "--kind", "knowledge", "--question", "Which insurer should the FNA quote be requested from, and is it New Business or Servicing?",
                "--searched", "the form, the call, the Overview and the other documents")
        self.ok("answer", self.run_dir, "--need", "fna_quote", "--said", "BrightRock, New Business")
        ov = {"quotes": [{"id": "o1", "group": "fna", "insurer": "BrightRock", "mode": "Servicing", "src": [{"ask": "fna_quote"}]}]}
        self.write("overlay.json", ov)
        self.ok("compose", self.run_dir)
        out = self.verify("--stage", "pre")
        self.assertIn("says Servicing but no source (the form, the call or Paul) says Servicing: Servicing is never a default", out.stdout)
        ov["quotes"][0]["mode"] = "New Business"
        self.write("overlay.json", ov)
        self.ok("compose", self.run_dir)
        c = self.load("content.json")
        row = [r for s in c["sections"] for b in s["blocks"] for r in b["rows"] if r["id"] == "quote.fna"][0]
        self.assertEqual(row["bullets"], ["Insurer: BrightRock", "Basis: New Business"])
        self.assertEqual(c["unsettled"] and [u for u in c["unsettled"] if u.startswith("quote.")], [])
        # a typed-in answer from Paul is refused (A7)
        ov["asked_paul"] = [{"id": "q1", "about": "FNA quote", "question": "Which insurer?", "suggestion": "BrightRock", "paul_said": "BrightRock, Servicing"}]
        self.write("overlay.json", ov)
        r = self.refused("compose", self.run_dir)
        self.assertIn("asked_paul is no longer accepted", r.stdout + r.stderr)


class UnknownKeys(Chat):
    def setUp(self):
        super().setUp()
        f = HH.pat_form()
        f["f"]["zz_new_question"] = {"v": "Interested in a funeral plan", "st": "confirmed"}
        f["l"]["rental"] = [HH.row(addr="Flat 4", rent="R 8 000.00")]
        f["l"]["debts"][0]["d"]["surprise"] = "Variable rate"
        jdump(self.form_path, f)
        self.form = f
        __import__("support").make_form_pdf(self.pdf_path, f)

    def test_an_unknown_populated_key_goes_to_the_closing_block_and_the_glance_list(self):
        self.through("pdf")
        c = self.load("content.json")
        labels = [r["label"] for r in c["other_fields"]]
        self.assertIn("zz_new_question", labels)
        self.assertTrue(any("rental row 1" in l for l in labels))
        self.assertTrue(any("debts row 1: surprise" in l for l in labels), labels)
        self.assertTrue(any("zz_new_question" in g for g in c["glance"]), c["glance"])
        pages = subprocess.run(["pdftotext", os.path.join(self.p("out"), c["file_name"]), "-"], capture_output=True, text=True).stdout
        self.assertIn("Other fields from the form", pages)
        self.assertIn("Interested in a funeral plan", pages)
        # and removing it from content.json is caught
        c["other_fields"] = []
        self.write("content.json", c)
        out = self.verify("--stage", "pre")
        self.assertIn("not in the closing block 'Other fields from the form'", out.stdout)


class SaveProof(Chat):
    def test_a_listing_with_another_size_is_refused(self):
        self.through("check")
        r = self.s_pdf(listed_size=12345)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("the save is not proven", r.stdout)
        self.s_pdf()                                           # a correct listing then passes

    def test_the_checker_compares_the_listing_with_the_local_file_too(self):
        self.through("handoffs")
        rc = self.load("receipt.json")
        rc["saved"]["listed_size"] = "999"
        self.write("receipt.json", rc)
        out = self.verify()
        self.assertEqual(out.returncode, 1)
        self.assertIn("saved.listed_size is 999 but the local PDF is", out.stdout)

    def test_another_folder_of_the_same_client_is_not_accepted_as_the_save_folder(self):
        # (another client's and another broker's folders are in test_review_fixes.SaveFolders)
        self.through("check")
        r = self.s_pdf(expect_refusal=True, folder="C:\\liferisk.co.za\\Company - WR Clients\\Paul Kafentzis (Client Files)\\Samplecase, Pat\\3. Applications")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("does not end in the client's '2. Fact Find' folder", r.stdout)


class TwoSpouses(Chat):
    def compose_for(self, form, client, spouse_form=None):
        import compose
        import ffform
        p_ = os.path.join(self.tmp, client["first"] + ".json")
        jdump(p_, form)
        fr = ffform.read_form(p_)
        common = None
        if spouse_form:
            p2 = os.path.join(self.tmp, "other.json")
            jdump(p2, spouse_form)
            common = ffform.read_form(p2)
        run = {"client": client, "date": "05/11/2026"}
        return compose.compose({"layout": compose.w.layout(), "run": run, "form": fr, "overlay": {}, "cross": [], "claims": {}, "lead": {}, "common": common})

    def test_each_spouse_gets_her_own_data_and_only_the_common_debts_and_children(self):
        pat = self.compose_for(HH.pat_form(), {"first": "Pat", "surname": "Samplecase"})
        robin = self.compose_for(HH.robin_form(), {"first": "Robin", "surname": "Testcase"}, spouse_form=HH.pat_form())
        import verify
        self.assertEqual(verify.spouse_overlap(robin, pat), [])
        self.assertEqual(verify.spouse_overlap(pat, robin), [])
        rows = {r["id"]: r for s in robin["sections"] for b in s["blocks"] for r in b["rows"]}
        self.assertIn("Home loan", json.dumps(robin))                          # the common debts and children are in both
        self.assertIn("Alex", json.dumps(robin))
        self.assertEqual(robin["common_used"], ["debts", "kids"])
        self.assertNotIn("R 45 000.00", json.dumps(robin))                     # Pat's income is not in Robin's document
        self.assertNotIn("082 555 0100", json.dumps(robin))

    def test_mixing_the_spouses_data_is_found_both_ways(self):
        pat = self.compose_for(HH.pat_form(), {"first": "Pat", "surname": "Samplecase"})
        robin = self.compose_for(HH.robin_form(), {"first": "Robin", "surname": "Testcase"}, spouse_form=HH.pat_form())
        import verify
        for sid_b in robin["sections"]:
            if sid_b["id"] == "occupation":
                sid_b["blocks"][0]["rows"][0]["bullets"].append("Cell 082 555 0100")        # Pat's cell number slipped into Robin's document
        self.assertEqual(verify.spouse_overlap(robin, pat), ["0825550100"])
        robin2 = self.compose_for(HH.robin_form(), {"first": "Robin", "surname": "Testcase"}, spouse_form=HH.pat_form())
        pat["sections"][1]["blocks"][0]["rows"][0]["bullets"].append(HH.ROBIN_ID)
        self.assertEqual(verify.spouse_overlap(robin2, pat), [HH.ROBIN_ID])

    def test_run_spouse_command_fails_on_overlap_and_passes_when_clean(self):
        pat = self.compose_for(HH.pat_form(), {"first": "Pat", "surname": "Samplecase"})
        robin = self.compose_for(HH.robin_form(), {"first": "Robin", "surname": "Testcase"}, spouse_form=HH.pat_form())
        a, b = os.path.join(self.tmp, "pat-run"), os.path.join(self.tmp, "robin-run")
        for d, c, sp in ((a, pat, ("Robin Testcase", b)), (b, robin, ("Pat Samplecase", a))):
            os.makedirs(d)
            jdump(os.path.join(d, "run.json"), {"client": c["client"], "date": "05/11/2026", "steps": {}, "spouse": {"name": sp[0], "run": sp[1]}})
            jdump(os.path.join(d, "content.json"), c)
        r = drv("spouse", b)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("none found", r.stdout)
        robin["sections"][1]["blocks"][0]["rows"][0]["bullets"].append("pat@example.invalid")
        jdump(os.path.join(b, "content.json"), robin)
        r = drv("spouse", b)
        self.assertEqual(r.returncode, 1)
        self.assertIn("FOUND", r.stdout)

    def test_the_spouse_run_cannot_end_without_the_cross_check_receipt(self):
        # a run started with --spouse needs spouse.cross_check at the hand-over step
        r = drv("start", self.run_dir, *CLIENT, "--spouse", "Robin Testcase", "--spouse-run", os.path.join(self.tmp, "robin"))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(self.load("run.json")["spouse"]["surname"], "Testcase")
        import run as runmod
        errs = runmod.ck_handoffs(self.run_dir, self.load("run.json"))
        self.assertTrue(any("spouse.cross_check" in e for e in errs), errs)


class Modes(Chat):
    def test_transcript_only_mode_builds_a_document_that_says_where_everything_came_from(self):
        self.s_start()
        self.access("transcript")
        for route in ("device", "m365", "zapier"):
            self.access("form", route, "fail", "t_" + route, "not found")
        self.ok("ask", self.run_dir, "--need", "form", "--searched", "the 2. Fact Find folder on all three routes")
        self.ok("answer", self.run_dir, "--need", "form", "--said", "Transcript alone please", "--choice", "transcript")
        sh("tx.py", "prep", self.transcript, self.run_dir, ok=True)
        r = self.ok("compose", self.run_dir)
        c = self.load("content.json")
        self.assertEqual(c["form"]["mode"], "transcript")
        self.assertEqual(c["client"], {"first": "Pat", "surname": "Samplecase"})
        self.assertEqual(c["file_name"], "Fact Find Transcript - 05.11.26 - (Pat Samplecase).pdf")
        self.assertIn("UNSETTLED", r.stdout)                       # nothing is invented: every empty field has to be filled with a source or claimed
        self.ok("claim", self.run_dir, "--all-empty")
        out = self.verify("--stage", "pre")
        self.assertIn("no form data file in this run (transcript, on Paul's word)", out.stdout)

    def test_two_spouses_each_in_their_own_run_with_the_common_debts_and_children(self):
        pat, robin = os.path.join(self.tmp, "pat-run"), os.path.join(self.tmp, "robin-run")
        self.ok("start", pat, *CLIENT, "--spouse", "Robin Testcase", "--spouse-run", robin)
        self.access_to(pat, "form")
        self.ok("form", pat, self.form_path)
        rpath = os.path.join(self.tmp, "robin.json")
        jdump(rpath, HH.robin_form())
        self.ok("start", robin, "--client", "Robin Testcase", "--date", "05/11/2026", "--spouse", "Pat Samplecase", "--spouse-run", pat)
        self.access_to(robin, "form")
        self.ok("form", robin, rpath)
        sh("tx.py", "prep", self.transcript, pat, ok=True)
        sh("tx.py", "prep", self.transcript, robin, ok=True)
        self.ok("compose", pat)
        self.ok("compose", robin)
        c = jload(os.path.join(robin, "content.json"))
        self.assertEqual(c["common_used"], ["debts", "kids"])
        text = json.dumps(c, ensure_ascii=False)
        self.assertIn("Absa", text)
        self.assertIn("Common to both spouses: taken from the other spouse's form.", text)
        self.assertNotIn("082 555 0100", text)                         # Pat's cell number
        self.assertNotIn("R 45 000.00", text)                          # Pat's income
        self.assertIn("083 555 0111", text)                            # Robin's own
        r = self.ok("spouse", robin)
        self.assertIn("none found", r.stdout)

    def access_to(self, run, need):
        r = drv("access", run, "--need", need, "--route", "device", "--tool", "device_stage_files", "--result", "ok")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
