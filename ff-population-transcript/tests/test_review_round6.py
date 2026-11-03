"""Regression tests for the SIXTH review, fix round 6: two silent routes. The glance list showed WHICH field covered a request line but never the VALUE the chat wrote. A bare 'No'
could cover a line that asks for a quote (H1) and 'No' could cover a credit-life line that says credit life exists (H2). Every test asserts that the program REFUSES (or FAILS) what the
reviewer showed it let through, or prints what Paul needs to see. Invented people only. H1 and H2 are the reviewer's ids."""
import os
import re
import shutil
import tempfile

from support import Chat, Staged, SCRIPTS, drv, jdump, jload, slurp
import compose
import verify
from test_review_round4 import fails, fna_blank_form

SKILL = os.path.dirname(SCRIPTS)
FNA_KEY = "For the risk cover I will ask BrightRock for a new business FNA quote for you."
FNA_QUOTE = "ask BrightRock for a new business FNA quote"
NOT_WANTED = "For the risk cover I was going to ask BrightRock for a new business FNA quote, but Pat says I do not want one."


def not_wanted(text):
    assert FNA_KEY in text
    return text.replace(FNA_KEY, NOT_WANTED)


def targets_of(run):
    inp = compose.load_inputs(run)
    content = compose.compose(inp) if not compose.check_inputs(inp) else None
    return verify.cover_targets(run, inp["overlay"], inp["cross"], inp["lead"], content)


# ----------------------------------------------------------------------------------------------------------------------------- H1: a bare No covers a line that asks for a quote
class NoCoversFna(Staged):
    STAGE = "joint"

    def form_json(self):
        return fna_blank_form()

    def src(self):
        return [{"line": self.L("new business FNA quote"), "quote": FNA_QUOTE}]

    def overlay_with(self, value, quote_row=False):
        ov = {"fills": [{"id": "z1", "key": "fna_req", "value": value, "src": self.src()}]}
        if quote_row:
            ov["quotes"] = [{"id": "z2", "group": "fna", "insurer": "BrightRock", "mode": "New Business", "src": self.src()}]
        self.write("overlay.json", ov)
        self.ok("compose", self.run_dir)

    def fna_entry(self):
        return next(e for e in self.load("ledger.json")["entries"] if e["kind"] == "quote_request" and "FNA" in e["quote"])

    def cover_with(self, *items):
        led = self.load("ledger.json")
        for e in led["entries"]:
            if e["id"] == self.fna_entry()["id"]:
                e["covered_by"] = list(items)
        self.write("ledger.json", led)

    def test_h1_a_bare_no_cannot_cover_a_line_that_asks_for_a_quote(self):
        self.overlay_with("No")
        r = self.refused("ledger", self.run_dir, "cover", self.fna_entry()["id"], "z1")
        text = r.stdout + r.stderr
        self.assertIn("line 66", text)
        self.assertIn("'No'", text)
        self.assertIn("z1", text)

    def test_h1_the_checker_repeats_it(self):
        self.overlay_with("No")
        self.cover_with("z1")
        out = self.verify("--stage", "pre")
        self.assertTrue(any("z1" in ln and "'No'" in ln and "line 66" in ln for ln in fails(out)), fails(out))

    def test_h1_a_bad_value_is_refused_even_when_a_good_item_covers_too(self):
        n = self.L("letter of authority")
        self.write("overlay.json", {"fills": [{"id": "z9", "key": "fna_req", "value": "No", "src": [{"line": n, "quote": "a letter of authority from you"}]}]})
        self.ok("compose", self.run_dir)
        e = next(e for e in self.load("ledger.json")["entries"] if e["kind"] == "request" and "letter of authority" in e["quote"])
        self.ok("ledger", self.run_dir, "cover", e["id"], "loa")                                  # the answered field covers it
        led = self.load("ledger.json")
        for x in led["entries"]:
            if x["id"] == e["id"]:
                x["covered_by"] = ["loa", "z9"]
        self.write("ledger.json", led)
        out = self.verify("--stage", "pre")
        self.assertTrue(any("z9" in ln and "'No'" in ln and "line %d" % n in ln for ln in fails(out)), fails(out))
        r = self.refused("ledger", self.run_dir, "cover", e["id"], "loa", "z9")
        self.assertIn("z9", r.stdout + r.stderr)

    def test_h1_a_request_field_that_covers_a_quote_line_must_say_yes(self):
        for value in ("Maybe", "Later", "No - not now"):
            self.overlay_with(value)
            r = self.refused("ledger", self.run_dir, "cover", self.fna_entry()["id"], "z1")
            self.assertIn("Yes", r.stdout + r.stderr, value)

    def test_h1_yes_covers(self):
        self.overlay_with("Yes")
        self.ok("ledger", self.run_dir, "cover", self.fna_entry()["id"], "z1")
        out = self.verify("--stage", "pre")
        self.assertFalse([ln for ln in fails(out) if "z1" in ln and "line 66" in ln], fails(out))

    def test_h1_pauls_recorded_no_lets_a_no_through_and_his_words_are_shown(self):
        self.overlay_with("No")
        self.ok("ask", self.run_dir, "--need", "fna_decision", "--about", "fna_req", "--kind", "knowledge", "--searched", "the whole call, twice",
                "--question", "Does Pat want the FNA quote? (the field FNA quote: requested)")
        self.ok("answer", self.run_dir, "--need", "fna_decision", "--said", "No, Pat does not want the FNA quote")
        self.ok("ledger", self.run_dir, "cover", self.fna_entry()["id"], "z1")
        label = verify.cover_label("z1", targets_of(self.run_dir))
        self.assertIn("No, Pat does not want the FNA quote", label)
        self.assertIn("fna_req = No", label)

    def test_h1_pauls_recorded_no_does_not_make_an_na_an_answer(self):
        self.overlay_with("N/A")
        self.ok("ask", self.run_dir, "--need", "fna_decision", "--about", "fna_req", "--kind", "knowledge", "--searched", "the whole call, twice",
                "--question", "Does Pat want the FNA quote? (the field FNA quote: requested)")
        self.ok("answer", self.run_dir, "--need", "fna_decision", "--said", "No, Pat does not want the FNA quote")
        r = self.refused("ledger", self.run_dir, "cover", self.fna_entry()["id"], "z1")
        self.assertIn("not an answer", r.stdout + r.stderr)

    def test_h1_an_answer_of_pauls_that_does_not_say_no_does_not_free_a_no(self):
        self.overlay_with("No")
        self.ok("ask", self.run_dir, "--need", "fna_decision", "--about", "fna_req", "--kind", "knowledge", "--searched", "the whole call, twice",
                "--question", "Does Pat want the FNA quote? (the field FNA quote: requested)")
        self.ok("answer", self.run_dir, "--need", "fna_decision", "--said", "Yes, Pat wants the FNA quote")
        self.refused("ledger", self.run_dir, "cover", self.fna_entry()["id"], "z1")

    def test_the_quote_rows_insurer_and_basis_are_shown(self):
        self.overlay_with("Yes", quote_row=True)
        label = verify.cover_label("quote.fna", targets_of(self.run_dir))
        self.assertIn("BrightRock", label)
        self.assertIn("New Business", label)
        self.assertTrue(label.endswith("[the FNA quote]"), label)

    def test_h1_the_glance_list_names_the_value_of_a_cover(self):
        self.overlay_with("Yes")
        t = targets_of(self.run_dir)
        self.assertEqual(verify.cover_label("z1", t), "z1 (fna_req = Yes) [the FNA quote]")


class NoWithNegation(Staged):
    """The honest No: the line itself says the client does not want it."""
    STAGE = "joint"
    TRANSCRIPT_EDIT = staticmethod(not_wanted)

    def form_json(self):
        return fna_blank_form()

    def test_h1_a_no_with_a_negation_on_the_line_is_accepted(self):
        src = [{"line": self.L("new business FNA quote"), "quote": FNA_QUOTE}]
        self.write("overlay.json", {"fills": [{"id": "z1", "key": "fna_req", "value": "No", "src": src}]})
        self.ok("compose", self.run_dir)
        e = next(e for e in self.load("ledger.json")["entries"] if e["kind"] == "quote_request" and "FNA" in e["quote"])
        self.ok("ledger", self.run_dir, "cover", e["id"], "z1")
        out = self.verify("--stage", "pre")
        self.assertFalse([ln for ln in fails(out) if "z1" in ln and "'No'" in ln], fails(out))


class ValueRule(Chat):
    """The rule itself, on small cases."""
    ASK = ["x", "For the risk cover I will ask BrightRock for a new business FNA quote for you."]
    NEG = ["x", "I do not want an FNA quote from BrightRock, thank you."]

    def info(self, value, types=("fill",), **kw):
        d = {"types": set(types), "lines": [2], "texts": [value], "terms": [], "value": value, "cl": False}
        d.update(kw)
        return d

    def test_a_bare_no_or_none_is_refused_where_the_line_asks_for_something(self):
        for value in ("No", "no", "No.", "None", "none"):
            p = verify.value_problem("request", 2, "z1", self.info(value), verify.window_text(self.ASK, 2), self.ASK)
            self.assertTrue(p and "line 2" in p, value)

    def test_a_negation_in_the_window_allows_a_no(self):
        for word in ("I do not want an FNA quote", "I don't want an FNA quote", "never an FNA quote", "an FNA quote? no", "an FNA quote without BrightRock", "decline the FNA quote", "cancel the FNA quote"):
            lines = ["x", "Please " + word]
            self.assertIsNone(verify.value_problem("request", 2, "z1", self.info("No"), verify.window_text(lines, 2), lines), word)

    def test_a_line_that_asks_nothing_does_not_need_the_rule(self):
        lines = ["x", "The cover is with BrightRock."]
        self.assertIsNone(verify.value_problem("request", 2, "z1", self.info("No"), verify.window_text(lines, 2), lines))

    def test_the_request_verbs(self):
        for text in ("ask them", "please do it", "can you send it", "I will need a quote", "would like a quote", "a request", "we will send", "I want it"):
            lines = ["x", text]
            self.assertTrue(verify.value_problem("request", 2, "z1", self.info("No"), verify.window_text(lines, 2), lines), text)

    def test_the_negation_words(self):
        for word in ("no", "not", "don't", "do not", "never", "none", "without", "decline", "declined", "cancel", "cancelled", "won't", "isn't"):
            self.assertTrue(verify.NEG_RE.search("we said " + word + " today"), word)

    def test_only_the_kinds_that_ask_are_checked(self):
        for kind in ("gap", "contact", "difference", "change"):
            self.assertIsNone(verify.value_problem(kind, 2, "z1", self.info("No"), verify.window_text(self.ASK, 2), self.ASK), kind)

    def test_a_quote_request_field_must_say_yes(self):
        p = verify.value_problem("quote_request", 2, "z1", self.info("No", types=("fill", "quote_req")), verify.window_text(self.ASK, 2), self.ASK)
        self.assertTrue(p and "Yes" in p)
        self.assertIsNone(verify.value_problem("quote_request", 2, "z1", self.info("Yes", types=("fill", "quote_req")), verify.window_text(self.ASK, 2), self.ASK))
        self.assertIsNone(verify.value_problem("quote_request", 2, "z1", self.info("No", types=("fill", "quote_req")), verify.window_text(self.NEG, 2), self.NEG))

    def test_the_message_says_what_the_program_really_checks(self):
        p = verify.value_problem("quote_request", 2, "z1", self.info("N/A", types=("fill", "quote_req")), verify.window_text(self.ASK, 2), self.ASK)
        self.assertIn("not an answer", p)
        self.assertNotIn("from the call's own words", p)
        self.assertIn("cannot read the call", p)


# ----------------------------------------------------------------------------------------------------------------------------- H2: credit life filled 'No' on a line that says it exists
class CreditLifeNo(Staged):
    STAGE = "joint"
    YES = {"line": 45, "quote": "there is credit life with Absa on the home loan"}

    def fill(self, key, value, cite=None):
        return {"id": "c1", "key": key, "value": value, "src": [cite or {"line": self.L("credit life with Absa"), "quote": self.YES["quote"]}]}

    def put(self, *fills):
        self.write("overlay.json", {"fills": list(fills)})
        self.ok("compose", self.run_dir)

    def cl_entry(self):
        return next(e for e in self.load("ledger.json")["entries"] if "credit life" in e["quote"])

    def test_h2_no_for_the_absa_loan_is_refused_when_the_line_says_credit_life_exists(self):
        self.put(self.fill("debts.0.cl", "No"))
        r = self.refused("ledger", self.run_dir, "cover", self.cl_entry()["id"], "c1")
        text = r.stdout + r.stderr
        self.assertIn("credit life", text)
        self.assertIn("line 45", text)

    def test_h2_no_for_credit_life_requested_is_refused_too(self):
        self.put(self.fill("cl_req", "No"))
        self.refused("ledger", self.run_dir, "cover", self.cl_entry()["id"], "c1")

    def test_h2_a_question_line_is_decided_by_the_answer_near_it(self):
        self.put(self.fill("debts.0.cl", "No", {"line": self.L("is there credit life on it"), "quote": "is there credit life on it"}))
        r = self.refused("ledger", self.run_dir, "cover", self.cl_entry()["id"], "c1")
        self.assertIn("line 45", r.stdout + r.stderr)

    def test_h2_a_no_for_the_other_loan_that_cites_its_own_sentence_is_accepted(self):
        self.put(self.fill("debts.0.cl", "Yes"),
                 {"id": "c2", "key": "debts.1.cl", "value": "No", "src": [{"line": self.L("credit life with Absa"), "quote": "The WesBank car finance has none"}]})
        self.ok("ledger", self.run_dir, "cover", self.cl_entry()["id"], "c1", "c2")
        out = self.verify("--stage", "pre")
        self.assertFalse([ln for ln in fails(out) if "credit life" in ln and "'No'" in ln], fails(out))

    def test_h2_a_new_debt_row_with_credit_life_no_is_refused_too(self):
        n = self.L("credit life with Absa")
        self.write("overlay.json", {"rows_add": [{"id": "r1", "list": "debts", "cells": {"type": "Home loan", "prov": "Absa", "cl": "No"}, "src": [{"line": n, "quote": self.YES["quote"]}]}]})
        self.ok("compose", self.run_dir)
        r = self.refused("ledger", self.run_dir, "cover", self.cl_entry()["id"], "r1")
        self.assertIn("line 45", r.stdout + r.stderr)

    def test_h2_yes_covers(self):
        self.put(self.fill("debts.0.cl", "Yes"))
        self.ok("ledger", self.run_dir, "cover", self.cl_entry()["id"], "c1")

    def test_h2_the_checker_repeats_it_even_when_a_good_item_covers_too(self):
        self.put(self.fill("debts.0.cl", "No"), {"id": "c3", "key": "cl_lender", "value": "Absa", "src": [{"line": 45, "quote": "there is credit life with Absa on the home loan"}]})
        led = self.load("ledger.json")
        for e in led["entries"]:
            if "credit life" in e["quote"]:
                e["covered_by"] = ["c1", "c3"]
        self.write("ledger.json", led)
        out = self.verify("--stage", "pre")
        self.assertTrue(any("c1" in ln and "credit life" in ln and "line 45" in ln for ln in fails(out)), fails(out))

    def test_h2_pauls_recorded_no_lets_it_through(self):
        self.put(self.fill("debts.0.cl", "No"))
        self.ok("ask", self.run_dir, "--need", "cl_decision", "--about", "debts", "--kind", "knowledge", "--searched", "the whole call, twice",
                "--question", "Does the Absa home loan (the debts list, debts.0.cl) really have no credit life?")
        self.ok("answer", self.run_dir, "--need", "cl_decision", "--said", "No, the credit life was cancelled last year")
        self.ok("ledger", self.run_dir, "cover", self.cl_entry()["id"], "c1")
        self.assertIn("No, the credit life was cancelled last year", verify.cover_label("c1", targets_of(self.run_dir)))

    def test_h2_the_glance_list_names_the_value(self):
        self.put(self.fill("debts.0.cl", "Yes"))
        self.assertEqual(verify.cover_label("c1", targets_of(self.run_dir)), "c1 (debts.0.cl = Yes) [a credit-life field]")


class CreditLifeRule(Chat):
    LINES = ["x", "Your home loan with Absa, is there credit life on it?", "", "0:04:45 Pat", "Yes, there is credit life with Absa on the home loan. The WesBank car finance has none."]

    def info(self, value, line, quote, key="debts.0.cl"):
        return {"types": {"fill"}, "lines": [line], "texts": [value], "terms": [], "value": value, "cl": True, "cites": [(line, quote)], "key": key}

    def test_the_cited_sentence_decides(self):
        yes = verify.value_problem("gap", 5, "c1", self.info("No", 5, "there is credit life with Absa on the home loan"), "", self.LINES)
        self.assertTrue(yes and "line 5" in yes)
        none = verify.value_problem("gap", 5, "c1", self.info("No", 5, "The WesBank car finance has none", "debts.1.cl"), "", self.LINES)
        self.assertIsNone(none)

    def test_a_question_is_decided_by_the_answer_after_it(self):
        p = verify.value_problem("gap", 2, "c1", self.info("No", 2, "is there credit life on it"), "", self.LINES)
        self.assertTrue(p and "line 5" in p)

    def test_a_yes_is_never_a_problem(self):
        self.assertIsNone(verify.value_problem("gap", 5, "c1", self.info("Yes", 5, "there is credit life with Absa on the home loan"), "", self.LINES))

    def test_no_transcript_no_check(self):
        self.assertIsNone(verify.value_problem("gap", 5, "c1", self.info("No", 5, "there is credit life with Absa on the home loan"), "", None))


# ----------------------------------------------------------------------------------------------------------------------------- the glance list: values
class Values(Staged):
    STAGE = "joint"

    def summary(self):
        self.s_content_done()
        return "\n".join(verify.summary_lines(self.run_dir, self.load("state.json"), self.load("ledger.json"), self.load("content.json")))

    def test_every_covering_item_shows_its_value(self):
        text = self.summary()
        self.assertIn("fna_req = Yes [the FNA quote]", text)
        self.assertIn("o1 (debts.0.cl = Yes) [a credit-life field]", text)
        self.assertIn("o4 (Latest payslip from the client)", text)                  # a request: its text
        self.assertIn("o5 (Email the latest payslip tomorrow)", text)               # a next step: its text

    def test_all_fills_that_cover_the_call_are_listed_with_their_line(self):
        text = self.summary()
        self.assertIn("Values written to cover the call", text)
        self.assertIn("debts.0.cl = Yes (line 45)", text)

    def test_the_values_line_is_cut_at_forty_entries(self):
        lines = ["l%d" % i for i in range(1, 60)]
        targets = {}
        ents = []
        for i in range(1, 46):
            targets["f%d" % i] = {"types": {"fill"}, "lines": [i], "key": "k%d" % i, "value": "v%d" % i, "pair": "k%d = v%d" % (i, i)}
            ents.append({"id": "L%d" % i, "line": i, "kind": "gap", "quote": "x", "covered_by": ["f%d" % i]})
        items, total = verify.covering_values({"entries": ents}, targets, lines)
        self.assertEqual(total, 45)
        self.assertEqual(len(items), 40)
        text = verify.values_line({"entries": ents}, targets, lines)
        self.assertIn("(45 in all", text)
        self.assertIn("and 5 more", text)
        self.assertIn("k1 = v1 (line 1)", text)


# ----------------------------------------------------------------------------------------------------------------------------- wording
class Wording6(Chat):
    SENTENCE = "the VALUE of a fill that covers a request line is the chat's own reading of the call"

    def test_the_attested_sentence(self):
        import inspect
        src = inspect.getsource(verify.report)
        self.assertIn(self.SENTENCE, src)
        self.assertIn("refuses a bare No when the line asks for something", src)
        self.assertIn("cannot know what the client really said", src)

    def test_the_other_pages_say_it_too(self):
        for rel in (("history", "CHANGES-FOR-PAUL.md"), ("references", "12-reading-lock.md"), ("steps.json",)):
            text = slurp(os.path.join(SKILL, *rel))
            self.assertIn("a bare No", text, rel)
            self.assertIn("own reading of the call", text, rel)

    def test_the_paul_page_has_a_fix_round_6_section(self):
        self.assertIn("Fix round 6", slurp(os.path.join(SKILL, "history", "CHANGES-FOR-PAUL.md")))
