"""Regression tests for the THIRD independent review (fix round 3): the FNA request on the call can no longer be dropped silently.
Every test asserts that the program REFUSES (or FAILS) what the reviewer showed it let through. Invented people only. A1 ... A9 are the reviewer's ids."""
import json
import os
import re

from support import Chat, Staged, H, SCRIPTS, drv, sh, jdump, jload, slurp, spit, make_form_pdf
from fixtures import household as HH
import verify
import wrlib as w_

FNA = "ask BrightRock for a new business FNA quote"


def fails(out):
    return [ln for ln in out.stdout.splitlines() if "[FAIL" in ln]


def fna_blank_form():
    f = HH.pat_form()
    for k in ("fna_req", "fna_type", "fna_ins"):
        f["f"][k] = {"v": "", "st": "empty"}
    return f


# ----------------------------------------------------------------------------------------------------------------------------- the words
class Words(Chat):
    def test_a1_the_soft_request_words_are_found(self):
        """Each phrase alone (so the test fails if any ONE of them is removed from the list)."""
        phrases = ("ask", "request", "sign", "can you", "could you", "would you", "please", "i'd like", "i would like", "i will need", "organise", "organize", "arrange", "book",
                   "prepare", "run the numbers", "come back to me", "get back to me", "send me", "email me", "let me know")
        for ph in phrases:
            text = "Well then, %s about the thing" % ph
            m = verify.SOFT_RE.search(text)
            self.assertIsNotNone(m, ph)
            self.assertEqual(m.group(0).lower(), ph, ph)
        self.assertIsNone(verify.request_word("Good evening Pat, thanks for joining the fact find"))

    def test_a1_the_hard_words_and_the_quote_words(self):
        for text in ("an FNA", "a quote", "the shortfall", "the RGAR", "the EGAR", "a letter of authority", "your payslip", "the appointment", "our next meeting", "we set up", "a follow up", "a reduced policy", "the Retirement Goal Analysis"):
            self.assertIsNotNone(verify.hard_word(text), text)
        for text in ("an FNA", "a quote", "the shortfall", "the RGAR", "the EGAR", "a reduced policy", "the Retirement Goal Analysis"):
            self.assertIsNotNone(verify.quote_word(text), text)
        for text in ("a letter of authority", "your payslip", "our next meeting"):
            self.assertIsNone(verify.quote_word(text), text)
        self.assertIsNone(verify.hard_word("Please send it"))                 # soft words only: the line may be dismissed with a reason


# ----------------------------------------------------------------------------------------------------------------------------- A3: the FNA line filed under another kind
class QuoteLineKind(Staged):
    STAGE = "pass2"
    LEDGER = [x for x in Chat.LEDGER if "new business FNA" not in x[0]]

    def form_json(self):
        return fna_blank_form()

    def add(self, kind, line=None):
        n = line or self.L("new business FNA quote")
        return drv("ledger", self.run_dir, "add", "--line", str(n), "--kind", kind, "--quote", FNA)

    def test_a3_the_fna_line_cannot_be_filed_as_a_gap_or_any_other_kind(self):
        for kind in ("gap", "difference", "contact", "next_step", "request", "change"):
            r = self.add(kind)
            self.assertNotEqual(r.returncode, 0, "accepted kind %s" % kind)
            self.assertIn("must be kind quote_request", r.stdout + r.stderr)

    def test_a3_the_fna_line_as_a_quote_request_is_accepted(self):
        r = self.add("quote_request")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_a3_a_ledger_edited_to_file_the_line_as_a_gap_fails_the_checker(self):
        n = self.L("new business FNA quote")
        led = self.load("ledger.json")
        led["entries"].append({"id": "L99", "line": n, "kind": "gap", "quote": FNA, "pass": 1, "covered_by": []})
        self.write("ledger.json", led)
        sh("tx.py", "scan", self.run_dir, ok=True)
        out = self.verify("--stage", "pre")
        self.assertTrue(any("L99" in ln and "must be recorded as a quote_request" in ln for ln in fails(out)), fails(out))

    def test_a3_an_unrelated_fill_that_shares_a_word_with_the_field_label_is_not_a_cover(self):
        """The reviewer's repro: sti_biz = No (label 'Business insurance') cited at line 66 covered the FNA line because 'business' is in the quote and in the label."""
        n = self.L("new business FNA quote")
        led = self.load("ledger.json")
        led["entries"].append({"id": "L99", "line": n, "kind": "gap", "quote": FNA, "pass": 1, "covered_by": []})
        self.write("ledger.json", led)
        self.write("overlay.json", {"fills": [{"id": "z1", "key": "sti_biz", "value": "No", "src": [{"line": n, "quote": FNA}]}]})
        self.ok("compose", self.run_dir)
        r = self.refused("ledger", self.run_dir, "cover", "L99", "z1")
        self.assertIn("none of the field's own search words", r.stdout + r.stderr)

    def test_a3_a_fill_whose_own_search_words_are_in_the_entry_line_is_a_cover(self):
        n = self.L("credit life with Absa")
        led = self.load("ledger.json")
        led["entries"].append({"id": "L98", "line": n, "kind": "gap", "quote": "there is credit life with Absa on the home loan", "pass": 1, "covered_by": []})
        self.write("ledger.json", led)
        self.write("overlay.json", {"fills": [{"id": "o1", "key": "debts.0.cl", "value": "Yes", "src": [{"line": n, "quote": "there is credit life with Absa on the home loan"}]}]})
        self.ok("compose", self.run_dir)
        self.ok("ledger", self.run_dir, "cover", "L98", "o1")

    def test_a3_the_checker_repeats_the_cover_rule(self):
        n = self.L("new business FNA quote")
        led = self.load("ledger.json")
        led["entries"].append({"id": "L99", "line": n, "kind": "gap", "quote": FNA, "pass": 1, "covered_by": ["z1"]})
        self.write("ledger.json", led)
        self.write("overlay.json", {"fills": [{"id": "z1", "key": "sti_biz", "value": "No", "src": [{"line": n, "quote": FNA}]}]})
        self.ok("compose", self.run_dir)
        sh("tx.py", "scan", self.run_dir, ok=True)
        out = self.verify("--stage", "pre")
        self.assertTrue(any("says nothing about this part of the call" in ln for ln in fails(out)), fails(out))


# ----------------------------------------------------------------------------------------------------------------------------- A9: a claim cannot cover what the call said
class ClaimCovers(Staged):
    STAGE = "joint"

    def setup_claim(self, key, hits):
        self.ok("compose", self.run_dir)
        cl = self.load("claims.json")
        cl[key] = {"as": "Not discussed", "terms": ["x"], "hits": hits, "docs": [], "reviewed": "line %d says something else entirely about it" % hits[0], "searched": "", "weak": False}
        self.write("claims.json", cl)

    def test_a9_a_gap_cannot_be_covered_by_a_not_discussed_claim_even_next_to_it(self):
        e = next(e for e in self.load("ledger.json")["entries"] if e["kind"] == "gap" and "credit life" in e["quote"])
        self.setup_claim("cl_bal", [e["line"]])
        r = self.refused("ledger", self.run_dir, "cover", e["id"], "claim:cl_bal")
        self.assertIn("cannot cover a gap", r.stdout + r.stderr)

    def test_a9_a_contact_cannot_be_covered_by_a_not_discussed_claim_either(self):
        e = next(e for e in self.load("ledger.json")["entries"] if e["kind"] == "contact")
        self.setup_claim("home", [e["line"]])
        r = self.refused("ledger", self.run_dir, "cover", e["id"], "claim:home")
        self.assertIn("cannot cover a contact", r.stdout + r.stderr)

    def test_a9_the_checker_repeats_it_on_a_hand_edited_ledger(self):
        e = next(e for e in self.load("ledger.json")["entries"] if e["kind"] == "gap" and "credit life" in e["quote"])
        self.setup_claim("cl_bal", [e["line"]])
        led = self.load("ledger.json")
        for x in led["entries"]:
            if x["id"] == e["id"]:
                x["covered_by"] = ["claim:cl_bal"]
        self.write("ledger.json", led)
        self.fresh_overlay({})
        out = self.verify("--stage", "pre")
        self.assertTrue(any("cannot cover a gap" in ln for ln in fails(out)), fails(out))


# ----------------------------------------------------------------------------------------------------------------------------- A2b: requests next to an unrelated entry
def add_unworded_requests(text):
    key = "We also need a letter of authority from you so we can speak to the other providers."
    add = (key + "\n\n0:11:05 Pat Samplecase\nSend me what BrightRock says about that cover.\n\n0:11:08 Paul Kafentzis\n"
           "Can you have Alwyn run the numbers on the Discovery option for the medical aid?\n\n0:11:12 Pat Samplecase\nYes, organise that and come back to me.")
    assert key in text
    return text.replace(key, add)


class NearEntry(Staged):
    """The letter-of-authority entry is on line 78; three new requests follow it. None of them shares a word with that entry, so none is handled by it."""
    STAGE = "pass2"
    TRANSCRIPT_EDIT = staticmethod(add_unworded_requests)

    def lines_of(self, *texts):
        return [self.L(t) for t in texts]

    def test_a2b_requests_next_to_an_unrelated_entry_stop_the_scan_step(self):
        sh("tx.py", "scan", self.run_dir, ok=True)
        r = self.refused("done", self.run_dir, "scan")
        for n in self.lines_of("Send me what BrightRock says", "run the numbers on the Discovery", "organise that and come back"):
            self.assertIn(str(n), r.stdout)

    def test_a2b_a_quoting_reason_handles_a_soft_line_and_the_glance_list_says_how(self):
        sh("tx.py", "scan", self.run_dir, ok=True)
        lines = slurp(self.p("transcript.txt")).split("\n")
        st = self.load("state.json")
        led = self.load("ledger.json")
        must = [e for e in led["entries"] if e["kind"] in verify.KINDS_MUST_COVER]
        for n in verify.required_lines(lines, st):
            if verify.line_resolution(n, lines, must) is None:
                self.assertNotIn(n, verify.hard_lines(lines))
                self.ok("ledger", self.run_dir, "review", "--line", str(n), "--reason", "line %d says: %s so nothing is recorded" % (n, " ".join(lines[n - 1].split()[:8])))
        self.ok("done", self.run_dir, "scan")
        out = "\n".join(verify.summary_lines(self.run_dir, self.load("state.json"), self.load("ledger.json"), {}))
        self.assertIn("how every request line was handled", out)
        self.assertRegex(out, r"line \d+ -> entry L\d+ \(quote_request, covered by")      # an entry that handles a line
        self.assertRegex(out, r"line \d+ dismissed: line \d+ says: Send me")                # a dismissal, with its reason

    def test_a2b_an_entry_on_the_line_or_one_that_shares_a_word_handles_it(self):
        lines = ["x", "Please send us your latest payslip", "OK, the payslip will come tomorrow", "Thanks", "unrelated chatter here"]
        ents = [{"id": "L1", "line": 2, "kind": "request", "quote": "send us your latest payslip"}]
        self.assertEqual(verify.line_resolution(2, lines, ents)["id"], "L1")           # on the line
        self.assertEqual(verify.line_resolution(3, lines, ents)["id"], "L1")           # shares 'payslip'
        self.assertIsNone(verify.line_resolution(5, lines, ents))                     # near enough but nothing shared... and 5 is 3 lines away with its own words
        self.assertEqual(verify.line_resolution(4, lines, ents)["id"], "L1")           # 'Thanks' holds no word of 4 letters: any near entry will do

    def test_a2b_the_checker_repeats_it(self):
        sh("tx.py", "scan", self.run_dir, ok=True)
        out = self.verify("--stage", "pre")
        self.assertTrue(any("are not handled by an entry that must be covered" in ln or "cannot be dismissed" in ln for ln in fails(out)), fails(out))


# ----------------------------------------------------------------------------------------------------------------------------- A1: hard request lines cannot be dismissed
class HardLines(Staged):
    STAGE = "pass2"
    LEDGER = [x for x in Chat.LEDGER if "new business FNA" not in x[0]]

    def form_json(self):
        return fna_blank_form()

    def reason(self, n):
        return "line %d only says: %s so no quote is wanted" % (n, "I will ask BrightRock for a new business FNA quote")

    def test_a1_a_hard_line_cannot_be_dismissed_by_a_review_at_all(self):
        n = self.L("new business FNA quote")
        sh("tx.py", "scan", self.run_dir, ok=True)
        r = self.refused("ledger", self.run_dir, "review", "--line", str(n), "--reason", self.reason(n))
        self.assertIn("cannot be dismissed", r.stdout + r.stderr)
        self.assertEqual(self.load("ledger.json")["scan_reviewed"], [])

    def test_a1_a_range_that_holds_a_hard_line_is_refused_too(self):
        n = self.L("new business FNA quote")
        sh("tx.py", "scan", self.run_dir, ok=True)
        r = self.refused("ledger", self.run_dir, "review", "--from", str(n - 2), "--to", str(n + 2), "--reason", "line %d only says: %s so no quote is wanted" % (n, "I will ask BrightRock for a new business FNA quote"))
        self.assertIn("cannot be dismissed", r.stdout + r.stderr)

    def test_a1_a_hand_edited_review_of_a_hard_line_fails_the_checker_and_the_scan_step(self):
        n = self.L("new business FNA quote")
        sh("tx.py", "scan", self.run_dir, ok=True)
        led = self.load("ledger.json")
        led["scan_reviewed"].append({"line": n, "reason": self.reason(n)})
        self.write("ledger.json", led)
        r = self.refused("done", self.run_dir, "scan")
        self.assertIn("cannot be dismissed", r.stdout)
        out = self.verify("--stage", "pre")
        self.assertTrue(any("cannot be dismissed" in ln for ln in fails(out)), fails(out))

    def test_a1_paul_can_say_a_line_is_not_a_request_and_it_is_shown_with_the_line(self):
        n = self.L("new business FNA quote")
        sh("tx.py", "scan", self.run_dir, ok=True)
        self.ok("ask", self.run_dir, "--need", "dismissals", "--kind", "knowledge", "--question", "Line %d mentions a quote but is it a request?" % n, "--searched", "the whole call", "--about", str(n))
        self.refused("ledger", self.run_dir, "review", "--line", str(n), "--reason", self.reason(n))              # asked, not answered
        self.ok("answer", self.run_dir, "--need", "dismissals", "--said", "Not a request, it is only about last year's quote")
        self.ok("ledger", self.run_dir, "review", "--line", str(n), "--reason", self.reason(n))
        st, led = self.load("state.json"), self.load("ledger.json")
        text = "\n".join(verify.summary_lines(self.run_dir, st, led, {}))
        self.assertIn("on Paul's recorded answer", text)
        self.assertIn("line %d" % n, text)

    def test_a1_pauls_answer_for_one_line_does_not_free_another(self):
        n = self.L("new business FNA quote")
        other = self.L("Retirement Goal Analysis")
        sh("tx.py", "scan", self.run_dir, ok=True)
        self.ok("ask", self.run_dir, "--need", "dismissals", "--kind", "knowledge", "--question", "Line %d mentions a quote but is it a request?" % n, "--searched", "the whole call", "--about", str(n))
        self.ok("answer", self.run_dir, "--need", "dismissals", "--said", "Not a request, it is only about last year's quote")
        self.refused("ledger", self.run_dir, "review", "--line", str(other), "--reason", "line %d only says: I will also ask for the Retirement Goal Analysis so nothing" % other)

    def test_a1_a_soft_line_is_still_dismissible_with_a_quoting_reason(self):
        n = self.L("email it tomorrow")
        sh("tx.py", "scan", self.run_dir, ok=True)
        self.ok("ledger", self.run_dir, "review", "--line", str(n), "--reason", "line %d only says: I will email it tomorrow so nothing else is wanted" % n)


# ----------------------------------------------------------------------------------------------------------------------------- A4: a question that is about everything
class WideAbout(Staged):
    STAGE = "joint"

    def ask(self, about, question="Which ABI value should this client's dread disease cover use?", need="wide"):
        return drv("ask", self.run_dir, "--need", need, "--kind", "knowledge", "--question", question, "--searched", "form, call and Overview", "--about", about)

    def test_a4_all_the_field_keys_in_one_about_is_refused(self):
        import compose
        keys = compose.valid_ids(w_.layout())["keys"]
        self.assertGreater(len(keys), 100)
        r = self.ask(",".join(keys), "Anything to change on this client's file?")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("at most 10", r.stdout + r.stderr)

    def test_a4_an_id_the_question_does_not_name_is_refused(self):
        r = self.ask("dd_abiv,tax", "Which ABI value should this client's dread disease cover use?")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("'tax' is not named in the question", r.stdout + r.stderr)

    def test_a4_an_unknown_id_is_refused(self):
        r = self.ask("dd_abiv_typo")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("is not a field key", r.stdout + r.stderr)

    def test_a4_ids_the_question_names_as_id_or_label_are_accepted(self):
        self.assertEqual(self.ask("dd_abiv").returncode, 0)
        self.assertEqual(self.ask("dd_abiv,tax", "Which ABI value and what income tax number? (dd_abiv, tax)", need="two").returncode, 0)
        self.assertEqual(self.ask("fna", "Which insurer should the FNA quote be requested from?", need="q").returncode, 0)

    def test_a4_a_wide_answer_cannot_fill_a_tax_number(self):
        self.ok("ask", self.run_dir, "--need", "wide", "--kind", "knowledge", "--question", "Which ABI value should this client's dread disease cover use?", "--searched", "form, call and Overview", "--about", "dd_abiv")
        self.ok("answer", self.run_dir, "--need", "wide", "--said", "the tax number is 9876543210 and use 20 percent for the dread disease ABI")
        self.write("overlay.json", {"fills": [{"id": "z9", "key": "tax", "value": "9876543210", "src": [{"ask": "wide"}]}]})
        r = self.refused("compose", self.run_dir)
        self.assertIn("a question may be used only for what it asked", r.stdout + r.stderr)

    def test_a4_the_dismissals_question_takes_line_numbers_only(self):
        r = drv("ask", self.run_dir, "--need", "dismissals", "--kind", "knowledge", "--question", "Is line 66 a request?", "--searched", "the call", "--about", "dd_abiv")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("line numbers", r.stdout + r.stderr)


# ----------------------------------------------------------------------------------------------------------------------------- A8: one line off
class OneLineOff(Staged):
    STAGE = "pass2"
    LEDGER = [x for x in Chat.LEDGER if "new business FNA" not in x[0]]

    def form_json(self):
        return fna_blank_form()

    def test_a8_a_fact_on_the_line_before_or_after_a_request_line_is_refused(self):
        n = self.L("new business FNA quote")
        for ln in (n - 2, n - 1, n + 1, n + 2):
            for kind in ("fact", "figure"):
                r = drv("ledger", self.run_dir, "add", "--line", str(ln), "--kind", kind, "--quote", FNA)           # the quote is found in the window of the lines either side
                self.assertNotEqual(r.returncode, 0, "accepted %s at line %d (the request is on %d)" % (kind, ln, n))
                self.assertIn("or a line next to it", r.stdout + r.stderr)

    def lines(self):
        return slurp(self.p("transcript.txt")).split("\n")

    def test_a8_a_fact_far_from_any_request_word_is_fine(self):
        n = self.L("Sixty percent at a desk")
        r = drv("ledger", self.run_dir, "add", "--line", str(n), "--kind", "fact", "--quote", "Sixty percent at a desk")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_a8_the_checker_repeats_the_window_rule(self):
        n = self.L("new business FNA quote")
        led = self.load("ledger.json")
        led["entries"].append({"id": "L99", "line": n + 1, "kind": "fact", "quote": FNA, "pass": 1, "covered_by": [], "excluded": "a plain fact about it"})
        self.write("ledger.json", led)
        sh("tx.py", "scan", self.run_dir, ok=True)
        out = self.verify("--stage", "pre")
        self.assertTrue(any("L99" in ln and "or a line next to it" in ln for ln in fails(out)), fails(out))
