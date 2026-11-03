"""Regression tests for the SECOND independent review (fix round 2). Every test asserts that the program REFUSES (or FAILS) what the reviewer showed it let through.
Invented people only. N1 ... N10 and A14 are the reviewer's finding ids."""
import json
import os
import re
import shutil
import subprocess
import sys

from support import (Chat, Staged, H, SCRIPTS, REPO, drv, sh, jdump, jload, slurp, spit, make_form_pdf, CLIENT, FIXTURE)
from fixtures import household as HH
import teams_driver
import verify
import wrlib as w_


def fails(out):
    return [ln for ln in out.stdout.splitlines() if "[FAIL" in ln]


def words_of(line, n=8):
    return " ".join(line.split()[:n])


# ----------------------------------------------------------------------------------------------------------------------------- N1: kind laundering and nonsense reasons
class Laundry(Staged):
    """The call asks for an FNA quote. Filing that line as a plain 'fact' and excluding it, and giving flagged fields nonsense reasons, used to reach RESULT: PASS."""
    STAGE = "pass2"
    LEDGER = [x for x in Chat.LEDGER if "new business FNA" not in x[0]]           # the chat never records the FNA request at all

    def form_json(self):
        f = HH.pat_form()
        for k in ("fna_req", "fna_type", "fna_ins"):
            f["f"][k] = {"v": "", "st": "empty"}
        return f

    def line(self, text):
        return self.L(text)

    def test_k1_a_request_line_cannot_be_recorded_as_a_plain_fact(self):
        n = self.line("new business FNA quote")
        for kind in ("fact", "figure"):
            r = self.refused("ledger", self.run_dir, "add", "--line", n, "--kind", kind, "--quote", "ask BrightRock for a new business FNA quote")
            self.assertIn("cannot be recorded as a plain", r.stdout + r.stderr)

    def test_k1_a_ledger_that_was_edited_to_say_fact_fails_the_checker(self):
        n = self.line("new business FNA quote")
        led = self.load("ledger.json")
        led["entries"].append({"id": "L99", "line": n, "kind": "fact", "quote": "ask BrightRock for a new business FNA quote", "pass": 1, "covered_by": [], "excluded": "just a plain fact"})
        self.write("ledger.json", led)
        sh("tx.py", "scan", self.run_dir, ok=True)
        out = self.verify("--stage", "pre")
        self.assertTrue(any("is recorded as 'fact' but line %d holds the word" % n in ln for ln in fails(out)), fails(out))

    def test_k1_an_entry_on_a_request_line_cannot_be_set_aside_as_plain_talk(self):
        n = self.line("new business FNA quote")
        led = self.load("ledger.json")
        led["entries"].append({"id": "L99", "line": n, "kind": "fact", "quote": "ask BrightRock for a new business FNA quote", "pass": 1, "covered_by": []})
        self.write("ledger.json", led)
        r = self.refused("ledger", self.run_dir, "exclude", "L99", "just a plain fact")
        self.assertIn("cannot be set aside as plain talk", r.stdout + r.stderr)

    def test_k1_leaving_the_request_line_out_altogether_stops_the_scan_step(self):
        n = self.line("new business FNA quote")
        sh("tx.py", "scan", self.run_dir, ok=True)
        r = self.refused("done", self.run_dir, "scan")
        self.assertIn("are not covered by a ledger entry that must be covered", r.stdout)
        self.assertIn(str(n), r.stdout)

    def test_k1_a_dismissal_needs_a_reason_that_quotes_the_line(self):
        n = self.line("new business FNA quote")
        sh("tx.py", "scan", self.run_dir, ok=True)
        for bad in ("xxxxxxxxxxxxxxxxxxxx", "just a plain fact", "plain talk", "nothing here at all really", "ok ok ok ok ok ok ok ok"):
            r = drv("ledger", self.run_dir, "review", "--line", str(n), "--reason", bad)
            self.assertNotEqual(r.returncode, 0, "accepted the reason %r" % bad)
        self.ok("ledger", self.run_dir, "review", "--line", str(n), "--reason", "line %d only says: %s so no quote is wanted from the client" % (n, "I will ask BrightRock for a new business FNA quote"))

    def test_k1_every_dismissed_line_is_named_on_the_glance_list(self):
        n = self.line("new business FNA quote")
        sh("tx.py", "scan", self.run_dir, ok=True)
        self.ok("ledger", self.run_dir, "review", "--line", str(n), "--reason", "line %d only says: I will ask BrightRock for a new business FNA quote so nothing is wanted" % n)
        st, led = self.load("state.json"), self.load("ledger.json")
        out = verify.summary_lines(self.run_dir, st, led, {})
        text = "\n".join(out)
        self.assertIn("dismissed lines", text)
        self.assertIn("line %d" % n, text)
        self.assertIn("were dismissed instead of recorded", text)


class ClaimReasons(Staged):
    """A 'Not discussed' that overrides what the search found must name a hit line by number and hold a word of that line."""
    STAGE = "joint"

    def prepare(self):
        self.ok("compose", self.run_dir)
        self.ok("claim", self.run_dir, "--all-empty")

    def test_k1_nonsense_reasons_are_refused(self):
        self.prepare()
        for bad in ("xxxxxxxxxxxxxxxxxxxx", "a a a a a a a a a a a a", "not about this field at all really", "line 54 is irrelevant here, truly irrelevant",
                    "line 12 says your name which is about something else"):                       # line 12 is not a hit line of pr_will
            r = drv("claim", self.run_dir, "--key", "pr_will", "--as", "Not discussed", "--reviewed", bad)
            self.assertNotEqual(r.returncode, 0, "accepted the reason %r" % bad)
        self.assertNotIn("pr_will", self.load("claims.json"))
        r = self.refused("claim", self.run_dir, "--key", "pr_will", "--as", "Not discussed", "--reviewed", "not about this field at all really")
        self.assertIn("name at least one of them by number", r.stdout + r.stderr)
        r = self.refused("claim", self.run_dir, "--key", "pr_will", "--as", "Not discussed", "--reviewed", "line 54 is irrelevant here, truly irrelevant")
        self.assertIn("holds no word", r.stdout + r.stderr)

    def test_k1_a_reason_that_names_the_hit_line_and_quotes_it_is_accepted(self):
        self.prepare()
        self.ok("claim", self.run_dir, "--key", "pr_will", "--as", "Not discussed", "--reviewed", "line 54 only asks 'Do you have a will' and gives no priority for it")
        self.assertIn("pr_will", self.load("claims.json"))

    def test_k1_the_checker_repeats_the_rule_on_a_hand_edited_claim(self):
        self.prepare()
        cl = self.load("claims.json")
        cl["pr_will"] = {"as": "Not discussed", "terms": ["a will"], "hits": [54], "docs": [], "reviewed": "xxxxxxxxxxxxxxxxxxxx", "searched": "", "weak": False}
        self.write("claims.json", cl)
        self.fresh_overlay({})
        out = self.verify("--stage", "pre")
        self.assertTrue(any("claim pr_will 'Not discussed'" in ln for ln in fails(out)), fails(out))

    def test_k1_a_not_on_the_call_answer_that_overrides_hits_needs_the_same_kind_of_reason(self):
        items = self.load("crosscheck.json")
        for i in items:
            if i["key"] == "employer":
                i["answer"] = None
        self.write("crosscheck.json", items)
        r = self.refused("cross", self.run_dir, "--key", "employer", "--r", "not_on_call", "--reviewed", "xxxxxxxxxxxxxxxxxxxx")
        self.assertIn("the call mentions it", r.stdout + r.stderr)
        self.ok("cross", self.run_dir, "--key", "employer", "--r", "not_on_call", "--reviewed", "line 27 says 'I work at Fakeco Logistics' but that is not about this field at all")

    def test_k1_the_report_counts_the_overrides(self):
        self.prepare()
        self.ok("claim", self.run_dir, "--key", "pr_will", "--as", "Not discussed", "--reviewed", "line 54 only asks 'Do you have a will' and gives no priority for it")
        self.fresh_overlay({})
        content = self.load("content.json")
        lines = slurp(self.p("transcript.txt")).split("\n")
        cs = verify.claim_stats(self.run_dir, lines, self.load("form_read.json"), content)
        mine = next(c for c in cs if c["key"] == "pr_will")
        self.assertEqual(mine["hits"], [54])
        rep = "\n".join(verify.source_report(self.run_dir, self.load("state.json"), content))
        self.assertIn("overrode search hits on a written reason", rep)

    def test_w1_a_reason_of_one_repeated_character_or_two_words_is_never_a_reason(self):
        for bad in ("xxxxxxxxxxxxxxxxxxxx", "................", "ab ab ab ab ab ab", "aaaaaaaaaaaaaaaaaaaaaaaa b c", "two words", "", "short"):
            self.assertIsNotNone(w_.reason_problem(bad), bad)
        self.assertIsNone(w_.reason_problem("the call names a different policy entirely"))

    def test_n10_the_search_words_find_plurals_stems_and_the_will_update(self):
        lines = ["I have diabetes", "my kids are small", "the premiums are high", "a willing partner", "the will has not been updated since before the children were born"]
        hits, _ = verify.search_terms("/nonexistent", lines, ["diabet*", "kid", "premium", "a will"])
        self.assertEqual(hits, [1, 2, 3])                                   # a stem, a plural, a plural; "a will" is not "a willing"
        lay = w_.layout()
        terms, curated = verify.field_terms(lay, "will_date", "Will last updated")
        self.assertTrue(curated)
        for t in ("updated", "last updated", "not updated"):
            self.assertIn(t, terms)
        self.refused("claim", self.run_dir, "--key", "will_date", "--as", "Not discussed")      # the call says it has not been updated: line 57 is found


# ----------------------------------------------------------------------------------------------------------------------------- N2: a cover must share words with the entry
class VacuousCover(Staged):
    STAGE = "joint"

    def setup_items(self):
        self.ok("compose", self.run_dir)
        self.ok("claim", self.run_dir, "--all-empty")
        led = self.load("ledger.json")
        self.L4 = next(e for e in led["entries"] if "credit life" in e["quote"])
        self.L8 = next(e for e in led["entries"] if "letter of authority" in e["quote"])
        ov = {"fills": [{"id": "z1", "key": "sti_car", "value": "No", "src": [{"line": self.L4["line"], "quote": "there is credit life with Absa on the home loan"}]}],
              "notes": [{"id": "z2", "section": "next", "text": "Noted", "src": [{"line": self.L8["line"], "quote": "we also need a letter of authority from you"}]}]}
        self.write("overlay.json", ov)
        self.ok("compose", self.run_dir)

    def test_m3_a_gap_covered_by_an_unrelated_fill_is_refused(self):
        self.setup_items()
        r = self.refused("ledger", self.run_dir, "cover", self.L4["id"], "z1")
        self.assertIn("says nothing about this part of the call", r.stdout + r.stderr)

    def test_m3_a_request_covered_by_a_note_that_says_noted_is_refused(self):
        self.setup_items()
        r = self.refused("ledger", self.run_dir, "cover", self.L8["id"], "z2")
        self.assertIn("share no word", r.stdout + r.stderr)

    def test_m3_a_note_about_the_letter_of_authority_is_accepted(self):
        self.setup_items()
        ov = self.load("overlay.json")
        ov["notes"][0]["text"] = "Letter of authority to be signed by the client"
        self.write("overlay.json", ov)
        self.ok("compose", self.run_dir)
        self.ok("ledger", self.run_dir, "cover", self.L8["id"], "z2")

    def test_m3_the_checker_repeats_it_on_a_hand_edited_ledger(self):
        self.setup_items()
        led = self.load("ledger.json")
        for e in led["entries"]:
            if e["id"] == self.L4["id"]:
                e["covered_by"] = ["z1"]
        self.write("ledger.json", led)
        out = self.verify("--stage", "pre")
        self.assertTrue(any("says nothing about this part of the call" in ln for ln in fails(out)), fails(out))


# ----------------------------------------------------------------------------------------------------------------------------- N3: the chat cannot answer its own question
class PaulsAnswers(Staged):
    STAGE = "joint"

    def ask(self, need="dd_abi", about="dd_abiv", said="make it 8 percent"):
        self.ok("ask", self.run_dir, "--need", need, "--kind", "knowledge", "--question", "Which ABI for dread disease for this client?", "--searched", "form, call and Overview", "--about", about)
        self.ok("answer", self.run_dir, "--need", need, "--said", said)

    def test_p1_a_question_must_say_what_it_is_about(self):
        r = self.refused("ask", self.run_dir, "--need", "dd_abi", "--kind", "knowledge", "--question", "Which ABI for dread disease for this client?", "--searched", "form, call and Overview")
        self.assertIn("--about", r.stdout + r.stderr)

    def test_p1_a_value_that_is_not_in_pauls_words_is_refused(self):
        self.ask(said="yes please do that")
        self.write("overlay.json", {"abi_override": [{"id": "ab1", "key": "dd_abiv", "value": "20%", "ask": "dd_abi"}]})
        r = self.refused("compose", self.run_dir)
        self.assertIn("not in Paul's recorded words", r.stdout + r.stderr)

    def test_p1_a_value_he_said_in_digits_or_in_words_is_accepted(self):
        self.ask(said="make it 8 percent")
        self.write("overlay.json", {"abi_override": [{"id": "ab1", "key": "dd_abiv", "value": "8%", "ask": "dd_abi"}]})
        self.ok("compose", self.run_dir)
        self.assertEqual(w_.numbers_in("make it twenty five percent"), {"25"})
        self.assertEqual(w_.numbers_in("eight please"), {"8"})

    def test_p1_his_answer_cannot_be_used_for_a_field_the_question_was_not_about(self):
        self.ask(said="make it 8 percent")
        self.write("overlay.json", {"fills": [{"id": "idf", "key": "tax", "value": "9876543210", "src": [{"ask": "dd_abi"}]}]})
        r = self.refused("compose", self.run_dir)
        self.assertIn("a question may be used only for what it asked", r.stdout + r.stderr)

    def test_p1_the_checker_repeats_the_number_rule(self):
        self.ask(said="make it 8 percent")
        self.write("overlay.json", {"abi_override": [{"id": "ab1", "key": "dd_abiv", "value": "8%", "ask": "dd_abi"}]})
        self.ok("compose", self.run_dir)
        c = self.load("content.json")
        row = next(r for s in c["sections"] for b in s["blocks"] for r in b["rows"] if r["id"] == "dd_abiv")
        row["bullets"] = ["9%"]                                         # the printed value is changed after composing; Paul's recorded words still say 8
        self.write("content.json", c)
        out = self.verify("--stage", "pre")
        self.assertTrue(any("it prints 9" in ln and "not in Paul's recorded words" in ln for ln in fails(out)), fails(out))      # the checker's own row check


class JointAnswer(Chat):
    """N3b: 'no' is refused when the form's spouse, or someone else, speaks on the call."""

    def spouse_transcript(self):
        t = slurp(self.transcript).replace("0:12:45 Pat Samplecase\nThursday the twelfth", "0:12:40 Robin Testcase\nI am Robin, his wife, and I work at Fakeschool as a teacher.\n\n0:12:45 Pat Samplecase\nThursday the twelfth")
        p = os.path.join(self.tmp, "t_joint.txt")
        spit(p, t)
        self.transcript = p

    def test_s2_no_is_refused_while_the_spouse_speaks(self):
        self.spouse_transcript()
        self.through("crosscheck")
        r = self.refused("joint", self.run_dir, "--answer", "no", "--evidence", "Only Pat and Paul spoke on the call; no spouse took part")
        self.assertIn("Robin Testcase", r.stdout + r.stderr)
        self.assertIn("--reason", r.stdout + r.stderr)

    def test_s2_a_written_reason_is_accepted_and_shown_to_paul(self):
        self.spouse_transcript()
        self.through("crosscheck")
        self.ok("joint", self.run_dir, "--answer", "no", "--evidence", "Only Pat's own cover was discussed on the call",
                "--reason", "Robin only said hello for a minute; she is not a client in this meeting and nothing of hers was discussed")
        self.ok("compose", self.run_dir)
        self.assertTrue(any("NOT a joint meeting although other people speak" in g for g in self.load("content.json")["glance"]))

    def test_s2_the_checker_repeats_it(self):
        self.spouse_transcript()
        self.through("crosscheck")
        rj = self.load("run.json")
        rj["joint"] = {"answer": "no", "evidence": "Only Pat and Paul spoke on the call"}
        self.write("run.json", rj)
        self.ok("compose", self.run_dir)
        out = self.verify("--stage", "pre")
        self.assertTrue(any("these people speak on the call" in ln for ln in fails(out)), fails(out))

    def test_s2_the_two_people_of_a_normal_call_are_not_a_problem(self):
        lines = slurp(FIXTURE).split("\n")
        self.assertEqual(verify.other_speakers(lines, {"first": "Pat", "surname": "Samplecase"}), {})
        self.assertEqual(sorted(verify.other_speakers(lines, {"first": "Zed", "surname": "Otherperson"})), ["Pat Samplecase"])


# ----------------------------------------------------------------------------------------------------------------------------- N4, N5: the Teams skill folder and the Teams run
class TeamsFolder(Staged):
    STAGE = "pdf"

    def fake_teams(self):
        sd, rd = os.path.join(self.tmp, "fake-teams-skill"), os.path.join(self.tmp, "fake-teams-run")
        os.makedirs(os.path.join(sd, "scripts"))
        os.makedirs(os.path.join(rd, "out"))
        spit(os.path.join(sd, "SKILL.md"), '---\nname: "client-teams-transcript-skill"\n---\n')
        jdump(os.path.join(sd, "steps.json"), {"steps": [{"id": "locate", "applies": ["first"]}, {"id": "teams", "applies": ["first"]}]})
        spit(os.path.join(sd, "scripts", "verify.py"), 'print("RESULT: PASS")\n')
        jdump(os.path.join(rd, "run.json"), {"meeting_type": "first", "client": {"first": "Pat", "surname": "Samplecase"}, "date": "05/11/2026", "steps": {"locate": {"state": "done"}}})
        spit(os.path.join(rd, "out", "planner_note.html"), "<html>planner</html>")
        spit(os.path.join(rd, "out", "teams_message.txt"), "Pat Samplecase (Prospect) - 1st Teams Appointment Completed: 05/11/2026")
        jdump(os.path.join(rd, "content.json"), {"next_appointment": {"agreed": True, "text": "Thursday 12/11/2026 at 16:00"}})
        return sd, rd

    def record(self, rd, sd):
        self.ok("receipt", self.run_dir, "--set", "summary.invoked=fact-find-summary run on the saved PDF: Summary built and saved",
                "--set", "summary.abi_same=Section 8 shows Life Cover (WOL) ABI 3%, Childcare ABI 5%, Household needs ABI 5% and Dread Disease ABI 3%",
                "--set", "teams.run_folder=" + rd, "--set", "teams.skill_dir=" + sd, "--set", "teams.next_appointment_carried=Thursday 12/11/2026 at 16:00")

    def test_t1_a_stub_teams_folder_whose_checker_just_prints_pass_is_refused(self):
        sd, rd = self.fake_teams()
        self.record(rd, sd)
        r = self.refused("done", self.run_dir, "handoffs")
        self.assertIn("does not look like the real Teams program", r.stdout)

    def test_t1_a_stub_with_the_right_step_names_but_a_short_checker_is_refused(self):
        sd, rd = self.fake_teams()
        steps = [{"id": i, "applies": ["first"]} for i in verify.TEAMS_STEPS]
        jdump(os.path.join(sd, "steps.json"), {"steps": steps})
        spit(os.path.join(sd, "scripts", "verify.py"), '# --skip-teams def near_source KINDS_MUST_COVER COVER_SPAN\nprint("RESULT: PASS")\n')
        spit(os.path.join(sd, "scripts", "run.py"), "def cmd_ledger(): pass\ndef cmd_done(): pass\ndef cmd_receipt(): pass\n")
        self.assertIn("only", verify.teams_skill_problem(sd))
        self.record(rd, sd)
        self.refused("done", self.run_dir, "handoffs")

    def test_t2_the_real_skill_with_a_hand_made_run_folder_is_refused(self):
        rd = os.path.join(self.tmp, "hand-made-run")
        os.makedirs(os.path.join(rd, "out"))
        with open(os.path.join(teams_driver.TEAMS_DIR, "steps.json"), encoding="utf-8") as f:
            steps = [x["id"] for x in json.load(f)["steps"] if "first" in x.get("applies", [])]
        jdump(os.path.join(rd, "run.json"), {"meeting_type": "first", "client": {"first": "Pat", "surname": "Samplecase"}, "date": "05/11/2026",
                                            "steps": {s: {"state": "done"} for s in steps if s != "teams"}})
        spit(os.path.join(rd, "out", "planner_note.html"), "x")
        spit(os.path.join(rd, "out", "teams_message.txt"), "Pat Samplecase 05/11/2026")
        jdump(os.path.join(rd, "content.json"), {"next_appointment": {"agreed": True, "text": "Thursday 12/11/2026"}})
        self.record(rd, teams_driver.TEAMS_DIR)
        r = self.refused("done", self.run_dir, "handoffs")
        self.assertIn("another transcript", r.stdout)                  # it holds no state of this run's transcript

    def test_t3_a_teams_run_made_from_another_transcript_is_refused(self):
        other = slurp(self.transcript).replace("Good evening Pat, thanks for joining the fact find.", "Hello Pat, welcome to a completely different meeting about something else.")
        other = other.replace("Tell me about work.", "Tell me about your holiday.")
        p_ = os.path.join(self.tmp, "other_transcript.txt")
        spit(p_, other)
        rd = os.path.join(self.tmp, "teams-other")
        teams_driver.drive(rd, p_)
        self.record(rd, teams_driver.TEAMS_DIR)
        r = self.refused("done", self.run_dir, "handoffs")
        self.assertIn("another transcript than this run's", r.stdout)

    def spoiled_copy(self, spoil):
        dst = os.path.join(self.tmp, "teams-copy")
        shutil.copytree(teams_driver.TEAMS_DIR, dst, ignore=shutil.ignore_patterns("tests", "__pycache__", "history", "releases"))
        spoil(dst)
        return dst

    def test_t6_a_copy_of_the_real_skill_without_the_first_meeting_steps_is_refused(self):
        def spoil(d):
            with open(os.path.join(d, "steps.json"), encoding="utf-8") as f:
                s = json.load(f)
            s["steps"] = [x for x in s["steps"] if x["id"] != "planner"]
            jdump(os.path.join(d, "steps.json"), s)
        self.assertIn("has not the steps of a first-meeting run", verify.teams_skill_problem(self.spoiled_copy(spoil)))

    def test_t6_a_copy_of_the_real_skill_whose_driver_lost_its_marks_is_refused(self):
        def spoil(d):
            p_ = os.path.join(d, "scripts", "run.py")
            spit(p_, slurp(p_).replace("def cmd_receipt", "def cmd_receipx"))
        self.assertIn("lacks def cmd_receipt", verify.teams_skill_problem(self.spoiled_copy(spoil)))

    def test_t6_a_copy_of_the_real_skill_with_a_shortened_checker_is_refused(self):
        def spoil(d):
            p_ = os.path.join(d, "scripts", "verify.py")
            spit(p_, "\n".join(slurp(p_).split("\n")[:300]))
        self.assertIn("only", verify.teams_skill_problem(self.spoiled_copy(spoil)))

    def test_t4_the_fingerprint_is_made_of_the_three_files(self):
        fp = verify.teams_fingerprint(teams_driver.TEAMS_DIR)
        self.assertEqual(sorted(fp), ["scripts/run.py", "scripts/verify.py", "steps.json"])
        self.assertTrue(all(re.fullmatch(r"[0-9a-f]{16}", v) for v in fp.values()))
        self.assertIsNone(verify.teams_skill_problem(teams_driver.TEAMS_DIR))

    def test_t5_a_teams_run_that_does_not_carry_the_follow_up_is_refused(self):
        rd = os.path.join(self.tmp, "teams-run")
        teams_driver.drive(rd, self.transcript, next_text="Friday 20/11/2026 at 10am")
        self.record(rd, teams_driver.TEAMS_DIR)
        r = self.refused("done", self.run_dir, "handoffs")
        self.assertIn("does not carry it as an agreed follow-up appointment", r.stdout)


# ----------------------------------------------------------------------------------------------------------------------------- N8: the save folder
class Folders(Staged):
    STAGE = "check"

    def try_folder(self, folder, spelling=""):
        st = self.load("state.json")
        name, size = st["build"]["pdf"], st["build"]["pdf_size"]
        args = ["--set", "pdf_sent_in_chat=true", "--set", "saved.tool=device_commit_files", "--set", "saved.filename=" + name, "--set", "saved.tool_result=ok",
                "--set", "saved.folder_listing_check=listing shows " + name, "--set", "saved.listed_size=%s" % size, "--set", "saved.folder=" + folder, "--set", "saved.folder_spelling=" + spelling]
        self.ok("receipt", self.run_dir, *args)
        return drv("done", self.run_dir, "pdf")

    def test_f1_the_root_must_be_the_first_part_of_the_path(self):
        for folder, spelling in (
            ("C:\\liferisk.co.za\\Company - Paul\\New Business\\Someone, Else\\2. Fact Find", ""),
            ("C:\\liferisk.co.za\\Company - Paul\\New Business\\Someone, Else\\2. Fact Find", "xxxxxxxxxx"),
            ("D:\\temp\\Company - Paul\\Samplecase, Pat\\2. Fact Find", ""),
            ("C:\\liferisk.co.za\\Company - WR Clients\\Other Broker (Client Files)\\Company - Paul\\Samplecase, Pat\\2. Fact Find", ""),
            ("C:\\liferisk.co.za\\Company - WR Clients\\Other Broker (Client Files)\\Samplecase, Pat\\2. Fact Find", ""),
            ("C:\\temp\\Company - WR Clients\\Paul Kafentzis (Client Files)\\Samplecase, Pat\\2. Fact Find", ""),
        ):
            r = self.try_folder(folder, spelling)
            self.assertNotEqual(r.returncode, 0, "accepted %s (spelling %r)" % (folder, spelling))

    def test_f1_the_right_folders_are_accepted(self):
        for folder in ("C:\\liferisk.co.za\\Company - Paul\\New Business\\Samplecase, Pat\\2. Fact Find",
                       "C:\\Users\\Paul\\liferisk.co.za\\Company - Paul\\New Business\\Samplecase, Pat\\2. Fact Find"):
            self.assertIsNone(verify.save_folder_problem(folder, {"first": "Pat", "surname": "Samplecase"}), folder)
        self.assertIsNone(verify.save_folder_problem("C:\\liferisk.co.za\\Company - WR Clients\\Paul Kafentzis (Client Files)\\Samplecase, Pat\\2. Fact Find", {"first": "Pat", "surname": "Samplecase"}))

    def test_f1_a_different_spelling_needs_a_real_sentence_that_names_the_surname_and_is_shown(self):
        folder = "C:\\liferisk.co.za\\Company - Paul\\New Business\\Samplecase, P\\2. Fact Find"
        for bad in ("", "xxxxxxxxxx", "spelled differently ok ok", "the folder was spelled with a dash"):             # the last two do not name the surname
            self.assertIsNotNone(verify.save_folder_problem(folder, {"first": "Pat", "surname": "Samplecase"}, bad), bad)
        good = "this client's folder is spelled Samplecase, P on the shared drive, I listed the parent folder"
        self.assertIsNone(verify.save_folder_problem(folder, {"first": "Pat", "surname": "Samplecase"}, good))
        r = self.try_folder(folder, good)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        out = verify.summary_lines(self.run_dir, self.load("state.json"), self.load("ledger.json"), self.load("content.json"))
        self.assertTrue(any("not named 'Surname, First'" in ln for ln in out), out)


# ----------------------------------------------------------------------------------------------------------------------------- A14: dismissing the call
class Dismissals(Staged):
    STAGE = "pass2"

    def reason_for(self, a, b):
        """A reason that holds a word from every request line in a..b (so the program's per-line check passes): only the SHARE can stop it."""
        lines = slurp(self.p("transcript.txt")).split("\n")
        st = self.load("state.json")
        req = [i for i in verify.required_lines(lines, st) if a <= i <= b]
        ws = []
        for i in req:
            cw = w_.content_words(lines[i - 1])
            ws.append(cw[0] if cw else "line")
        return "reviewed %d to %d and read %s so nothing needs recording" % (a, b, " ".join(dict.fromkeys(ws)))

    def test_m2_three_reviews_of_forty_lines_cannot_dismiss_the_whole_call(self):
        sh("tx.py", "scan", self.run_dir, ok=True)
        n = len(slurp(self.p("transcript.txt")).split("\n"))
        for a, b in ((1, 40), (41, 80), (81, n)):
            self.ok("ledger", self.run_dir, "review", "--from", str(a), "--to", str(b), "--reason", self.reason_for(a, b))
        r = self.refused("done", self.run_dir, "scan")
        self.assertIn("too much of the call was dismissed", r.stdout)

    def test_m2_the_blank_reasons_of_the_first_review_are_refused_at_once(self):
        sh("tx.py", "scan", self.run_dir, ok=True)
        r = self.refused("ledger", self.run_dir, "review", "--from", "1", "--to", "40", "--reason", "plain talk batch A")
        self.assertIn("holds no word", r.stdout + r.stderr)

    def test_p2_a_one_entry_ledger_with_every_other_hit_dismissed_line_by_line_is_refused(self):
        led = self.load("ledger.json")
        keep = next(e for e in led["entries"] if "cell number" in e["quote"])
        led["entries"] = [dict(keep, id="L1")]
        st0 = self.load("state.json")
        led["chunk_acks"] = [{"pass": p_, "chunk": c, "reason": "read this whole chunk and found nothing worth recording in it at all, chunk %d" % c} for p_ in (1, 2) for c in range(1, len(st0["chunks"]) + 1)]
        self.write("ledger.json", led)
        sh("tx.py", "scan", self.run_dir, ok=True)
        lines = slurp(self.p("transcript.txt")).split("\n")
        for n in verify.required_lines(lines, self.load("state.json")):
            if abs(n - keep["line"]) > 3:
                self.ok("ledger", self.run_dir, "review", "--line", str(n), "--reason", "line %d says: %s so nothing to record" % (n, words_of(lines[n - 1])))
        r = self.refused("done", self.run_dir, "scan")
        self.assertIn("too much of the call was dismissed", r.stdout)
        # Paul's recorded answer lets it go on, and the checker still warns
        self.ok("ask", self.run_dir, "--need", "dismissals", "--kind", "knowledge", "--question", "Most of this call was dismissed as plain talk. Go on?", "--searched", "the whole call, twice")
        self.ok("answer", self.run_dir, "--need", "dismissals", "--said", "Yes go on, the rest is chatter")
        self.ok("done", self.run_dir, "scan")

    def test_p2_every_dismissed_hit_line_is_listed_up_to_fifteen_then_counted(self):
        import tempfile
        d = tempfile.mkdtemp(prefix="wrdis-")
        self.addCleanup(shutil.rmtree, d, True)
        lines = ["we agree about item %d here" % i for i in range(1, 41)]           # 'agree' is a decision word: every line is a request line
        spit(os.path.join(d, "transcript.txt"), "\n".join(lines))
        st = {"scan": {"hits": list(range(1, 41))}, "total_lines": 40, "chunks": [[1, 40]]}
        few = {"entries": [], "scan_reviewed": [{"line": i, "reason": "line %d we agree about item" % i} for i in range(1, 11)]}
        many = {"entries": [], "scan_reviewed": [{"line": i, "reason": "line %d we agree about item" % i} for i in range(1, 31)]}
        t_few = "\n".join(verify.summary_lines(d, st, few, {}))
        t_many = "\n".join(verify.summary_lines(d, st, many, {}))
        self.assertIn("dismissed lines (all)", t_few)
        self.assertEqual(t_few.count("line 10 ("), 1)
        self.assertIn("dismissed lines (the first 15 of 30)", t_many)
        self.assertNotIn("line 20 (", t_many)                                         # only the first 15 are named
        self.assertIn("MORE THAN A QUARTER", t_many)


# ----------------------------------------------------------------------------------------------------------------------------- MINOR
class Minor(Staged):
    STAGE = "joint"

    def test_m6_a_short_policy_code_in_a_note_must_be_in_a_recorded_schedule(self):
        ov = {"notes": [{"id": "n1", "section": "cover", "text": "Old Mutual policy AB1234 is paid up",
                         "src": [{"line": self.L("BrightRock policy"), "quote": "Yes, the BrightRock policy"}]}]}
        self.write("overlay.json", ov)
        self.ok("compose", self.run_dir)
        out = self.verify("--stage", "pre")
        self.assertTrue(any("AB1234" in ln for ln in fails(out)), fails(out))

    def test_m6_ordinary_words_after_policy_are_not_a_policy_number(self):
        for text in ("policy schedule received", "the policy is paid up", "Fractured life cover"):
            self.assertEqual([m.group(1) or m.group(2) for m in verify.POLICY_NO.finditer(text)], [], text)
        self.assertEqual([m.group(1) or m.group(2) for m in verify.POLICY_NO.finditer("policy AB1234 and policy number QX99887")], ["AB1234", "QX99887"])

    def test_a5_a_long_number_in_a_note_needs_a_document_that_shows_it(self):
        ov = {"notes": [{"id": "n1", "section": "next", "text": "Reference 7654321 is open",
                         "src": [{"line": self.L("Thursday the twelfth at four works"), "quote": "Thursday the twelfth at four works"}]}]}
        self.write("overlay.json", ov)
        self.ok("compose", self.run_dir)
        out = self.verify("--stage", "pre")
        self.assertTrue(any("7654321" in ln and "6 or more digits" in ln for ln in fails(out)), fails(out))

    def test_n6_text_copies_are_chat_made_and_their_hash_is_on_the_glance_list(self):
        out = verify.summary_lines(self.run_dir, self.load("state.json"), self.load("ledger.json"), {})
        text = "\n".join(out)
        self.assertIn("MADE BY THE CHAT", text)
        self.assertRegex(text, r"WR Overview Pat Samplecase [0-9a-f]{12}")


class PdfGoOn(Staged):
    STAGE = "locate"

    def thin_pdf(self):
        p_ = os.path.join(self.tmp, "thin.pdf")
        make_form_pdf(p_, self.form, drop=[k for k in self.form["f"] if k not in ("fname", "sname", "date", "consent")])
        return p_

    def test_n10_a_pdf_with_too_much_missing_can_be_set_aside_only_on_pauls_recorded_word(self):
        self.ok("form", self.run_dir, self.form_path)
        r = self.refused("formpdf", self.run_dir, self.thin_pdf())
        self.assertEqual(r.returncode, 5)
        self.assertIn("--paul-go-on", r.stdout)
        r = self.refused("formpdf", self.run_dir, "--paul-go-on")                                  # he has not been asked
        self.assertIn("Paul's decision", r.stdout + r.stderr)
        self.ok("ask", self.run_dir, "--need", "formpdf", "--kind", "knowledge", "--question", "The saved PDF does not match the data file. Go on with the data file alone?", "--searched", "the 2. Fact Find folder")
        self.refused("formpdf", self.run_dir, "--paul-go-on")                                      # asked, not answered
        self.ok("answer", self.run_dir, "--need", "formpdf", "--said", "Go on with the data file alone please")
        self.ok("formpdf", self.run_dir, "--paul-go-on")
        self.assertEqual(self.load("form_pdf.json")["paul_go_on"], "Go on with the data file alone please")
        self.ok("done", self.run_dir, "form")
        out = verify.summary_lines.__globals__["load"](self.p("form_pdf.json"), {})
        self.assertTrue(out.get("paul_go_on"))

    def test_n10_the_checker_repeats_the_quarter_rule_on_a_hand_made_record(self):
        import ffform
        self.ok("form", self.run_dir, self.form_path)
        self.ok("formpdf", self.run_dir, self.pdf_path)                      # the right PDF
        spit(self.p("form_pdf.txt"), "Samplecase 05/11/2026\nzzzz marker\n")           # ... replaced by almost nothing, and every missing value 'looked at'
        _, missing = ffform.pdf_check(self.load("form_read.json"), slurp(self.p("form_pdf.txt")))
        rec = self.load("form_pdf.json")
        rec["not_found"] = missing
        rec["reviews"] = {m["key"]: {"result": "disagree", "quote": "zzzz marker", "pdf_value": "zzzz"} for m in missing}
        self.write("form_pdf.json", rec)
        r = self.refused("done", self.run_dir, "form")
        self.assertIn("are not in the saved PDF: it is not the PDF of this data file", r.stdout)

    def test_n10_yes_no_and_one_character_values_are_not_compared_with_the_pdf_a_known_limit(self):
        import ffform
        text = "something else entirely about Samplecase"
        self.assertTrue(ffform.value_in_pdf("Yes", text))
        self.assertTrue(ffform.value_in_pdf("No", text))
        self.assertTrue(ffform.value_in_pdf("5", text))
        self.assertFalse(ffform.value_in_pdf("Operations manager", text))


# ----------------------------------------------------------------------------------------------------------------------------- mutant-killing tests
class MutantKillers(Staged):
    STAGE = "joint"

    def form_json(self):
        f = HH.pat_form()
        for k in ("fna_type", "fna_ins"):
            f["f"][k] = {"v": "", "st": "empty"}
        f["l"]["debts"][0]["d"]["cl"] = "Yes"                                 # the form says the home loan has credit life
        return f

    def test_a6_the_new_business_basis_must_be_in_a_cited_source(self):
        ov = {"quotes": [{"id": "q1", "group": "fna", "insurer": "BrightRock", "mode": "New Business",
                          "src": [{"line": self.L("BrightRock policy"), "quote": "Yes, the BrightRock policy"}]}]}      # names the insurer, never says New Business
        self.write("overlay.json", ov)
        self.ok("compose", self.run_dir)
        out = self.verify("--stage", "pre")
        self.assertTrue(any("says New Business but no source it cites says so" in ln for ln in fails(out)), fails(out))

    def test_a2_the_form_itself_can_contradict_a_not_discussed_even_when_the_search_finds_nothing(self):
        import argparse
        import run as runmod
        self.ok("compose", self.run_dir)
        orig = verify.search_terms
        verify.search_terms = lambda run, lines, terms: ([], [])
        try:
            a = argparse.Namespace(run=self.run_dir, all_empty=False, key="cl_bal", as_="Not discussed", reviewed="", terms=None, searched=None)
            with self.assertRaises(SystemExit):
                runmod.cmd_claim(a)
            self.assertNotIn("cl_bal", self.load("claims.json"))
            # and the checker repeats it on a hand-made claim
            cl = self.load("claims.json")
            cl["cl_bal"] = {"as": "Not discussed", "terms": ["credit life"], "hits": [], "docs": [], "reviewed": "", "searched": "", "weak": False}
            self.write("claims.json", cl)
            self.fresh_overlay({})
            R, st, led, content = verify.run_checks(self.run_dir, "pre")
            msgs = [m for lvl, _, m in R.rows if lvl == "FAIL" and "claim cl_bal" in m]
            self.assertTrue(msgs and "the form itself says" in msgs[0], msgs)
        finally:
            verify.search_terms = orig

    def test_a2_a_claim_the_checker_finds_weak_needs_a_reason_too(self):
        self.ok("compose", self.run_dir)
        cl = {"home": {"as": "Not discussed", "terms": ["home number"], "hits": [], "docs": [], "reviewed": "", "searched": "", "weak": True}}
        self.write("claims.json", cl)
        self.fresh_overlay({})
        orig = verify.field_terms
        verify.field_terms = lambda lay, key, label="", row_values=None: ([(label or key).lower()], False)
        try:
            R, st, led, content = verify.run_checks(self.run_dir, "pre")
            msgs = [m for lvl, _, m in R.rows if lvl == "FAIL" and "rests on a WEAK search" in m]
            self.assertTrue(msgs, "a weak claim with no reason passed the checker")
        finally:
            verify.field_terms = orig


class PdfFormatOnly(Staged):
    STAGE = "locate"

    def test_a8_a_format_only_quote_for_an_amount_must_hold_its_digits(self):
        p_ = os.path.join(self.tmp, "short.pdf")
        make_form_pdf(p_, self.form, drop=("gross",))
        self.ok("form", self.run_dir, self.form_path)
        self.ok("formpdf", self.run_dir, p_)
        r = self.refused("pdfreview", self.run_dir, "--key", "gross", "--result", "format_only", "--quote", "WR Fact Find v3.0")
        self.assertIn("digits", r.stdout + r.stderr)
