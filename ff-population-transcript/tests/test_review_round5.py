"""Regression tests for the FIFTH review, fix round 5: two real holes left after round 4. Every test asserts that the program REFUSES (or FAILS) what the reviewer showed it let
through. Invented people only. G1, G2, G3 are the reviewer's ids (G3, a typed answer by the same chat that quotes the line, is inherent: no change, the glance list shows it)."""
import os
import re
import shutil
import tempfile

from support import Chat, Staged, SCRIPTS, drv, sh, jdump, jload, slurp, spit
import verify
from test_review_round4 import fails, fna_blank_form

TWO = "For the risk cover I will ask BrightRock for a new business FNA quote and a shortfall quote for you."
SKILL = os.path.dirname(SCRIPTS)


def two_products(text):
    key = "For the risk cover I will ask BrightRock for a new business FNA quote for you."
    assert key in text
    return text.replace(key, TWO)


# ----------------------------------------------------------------------------------------------------------------------------- G1: a quote line that names two products
class TwoProducts(Staged):
    """The call line names an FNA quote AND a shortfall quote. The shortfall (bf) row covers it; the FNA fields are claimed N/A."""
    STAGE = "joint"
    TRANSCRIPT_EDIT = staticmethod(two_products)

    def form_json(self):
        return fna_blank_form()

    def answers(self):
        a = super().answers()
        a["sf_req"] = {"r": "differs", "line": self.L("new business FNA quote"), "quote": "FNA quote and a shortfall quote for you", "value": "Yes"}      # the form says No, the call asks for one
        return a

    def src(self):
        return [{"line": self.L("new business FNA quote"), "quote": "FNA quote and a shortfall quote for you"}]

    def shortfall_only(self):
        return {"fills": [{"id": "z1", "key": "bf_sf_req", "value": "Yes", "src": self.src()}],
                "quotes": [{"id": "z2", "group": "bf_sf", "insurer": "BrightRock", "mode": "New Business", "src": self.src()}]}

    def fna_entry(self):
        return next(e for e in self.load("ledger.json")["entries"] if e["kind"] == "quote_request" and "FNA" in e["quote"])

    def cover_with(self, *items):
        led = self.load("ledger.json")
        for e in led["entries"]:
            if e["id"] == self.fna_entry()["id"]:
                e["covered_by"] = list(items)
        self.write("ledger.json", led)

    def test_g1_a_line_naming_two_products_covered_for_one_only_fails_and_names_the_missing_product(self):
        self.write("overlay.json", self.shortfall_only())
        self.ok("compose", self.run_dir)
        r = self.ok("ledger", self.run_dir, "cover", self.fna_entry()["id"], "quote.bf_sf")     # the cover itself is fine: it is the shortfall's
        self.assertIn("STILL OPEN", r.stdout)
        self.assertIn("FNA", r.stdout)
        out = self.verify("--stage", "pre")
        bad = [ln for ln in fails(out) if "names FNA and shortfall" in ln]
        self.assertTrue(bad, fails(out))
        self.assertIn("not covered for FNA", bad[0])
        self.assertNotIn("not covered for shortfall", bad[0])

    def test_g1_covering_each_product_with_its_own_row_passes_the_rule(self):
        ov = self.shortfall_only()
        ov["fills"].append({"id": "z0", "key": "fna_req", "value": "Yes", "src": self.src()})
        self.write("overlay.json", ov)
        self.ok("compose", self.run_dir)
        self.ok("ledger", self.run_dir, "cover", self.fna_entry()["id"], "z0", "quote.bf_sf")
        out = self.verify("--stage", "pre")
        self.assertFalse([ln for ln in fails(out) if "names FNA and shortfall" in ln], fails(out))

    def test_g1_each_product_may_also_have_its_own_entry_on_the_same_line(self):
        ov = self.shortfall_only()
        ov["fills"].append({"id": "z0", "key": "fna_req", "value": "Yes", "src": self.src()})
        self.write("overlay.json", ov)
        self.ok("compose", self.run_dir)
        n = self.L("new business FNA quote")
        self.ok("ledger", self.run_dir, "add", "--line", n, "--kind", "quote_request", "--quote", "a shortfall quote for you")
        e2 = self.load("ledger.json")["entries"][-1]
        self.ok("ledger", self.run_dir, "cover", self.fna_entry()["id"], "z0")
        self.ok("ledger", self.run_dir, "cover", e2["id"], "quote.bf_sf")
        out = self.verify("--stage", "pre")
        self.assertFalse([ln for ln in fails(out) if "names FNA and shortfall" in ln], fails(out))

    def test_g1_na_is_refused_on_the_fna_fields_while_the_ledger_records_the_request(self):
        self.ok("compose", self.run_dir)
        for key in ("fna_req", "fna_type", "fna_ins"):
            r = self.refused("claim", self.run_dir, "--key", key, "--as", "N/A",
                             "--reviewed", "this client has no FNA to be requested here: the shortfall quote is the one asked for on this call")
            self.assertIn("quote request", r.stdout + r.stderr)
            self.assertIn("FNA", r.stdout + r.stderr)

    def test_g1_the_checker_repeats_the_rule_for_a_hand_made_na_claim(self):
        self.ok("compose", self.run_dir)
        path = self.p("claims.json")
        cl = jload(path) if os.path.exists(path) else {}
        cl["fna_req"] = {"as": "N/A", "terms": [], "hits": [], "docs": [], "searched": "", "weak": False, "t": "x",
                         "reviewed": "this client has no FNA to be requested here: the shortfall quote is the one asked for on this call"}
        jdump(path, cl)
        self.ok("compose", self.run_dir)
        out = self.verify("--stage", "pre")
        self.assertTrue(any("claim fna_req 'N/A'" in ln and "quote request" in ln for ln in fails(out)), fails(out))

    def test_g1_a_request_field_filled_with_na_cannot_cover_a_quote_request(self):
        ov = {"fills": [{"id": "z1", "key": "fna_req", "value": "N/A", "src": self.src()}]}
        self.write("overlay.json", ov)
        self.ok("compose", self.run_dir)
        r = self.refused("ledger", self.run_dir, "cover", self.fna_entry()["id"], "z1")
        self.assertIn("not an answer", r.stdout + r.stderr)
        self.cover_with("z1")                                                    # and the checker repeats it on a hand-edited ledger
        out = self.verify("--stage", "pre")
        self.assertTrue(any("not an answer" in ln for ln in fails(out)), fails(out))

    def test_g1_a_line_paul_freed_is_not_checked_for_its_products(self):
        n = self.L("new business FNA quote")
        q = "Line %d says: For the risk cover I will ask BrightRock for a new business FNA quote and a shortfall quote for you. Is that a real request?" % n
        self.ok("ask", self.run_dir, "--need", "dismissals", "--about", str(n), "--kind", "knowledge", "--question", q, "--searched", "the whole call, twice")
        self.ok("answer", self.run_dir, "--need", "dismissals", "--said", "no, that was only an example of what we could do")
        self.write("overlay.json", self.shortfall_only())
        self.ok("compose", self.run_dir)
        self.ok("ledger", self.run_dir, "cover", self.fna_entry()["id"], "quote.bf_sf")
        out = self.verify("--stage", "pre")
        self.assertFalse([ln for ln in fails(out) if "names FNA and shortfall" in ln], fails(out))

    def test_g1_the_two_product_rule_works_on_the_helper_too(self):
        lines = ["x", TWO]
        ents = [{"id": "L1", "line": 2, "kind": "quote_request", "quote": "new business FNA quote and a shortfall quote", "covered_by": ["a"]}]
        t = {"a": {"types": {"quote"}, "lines": [2], "texts": ["new business FNA quote and a shortfall quote"], "terms": [], "group": "bf_sf"}}
        self.assertEqual(verify.topic_gaps(2, lines, ents, t), ["FNA"])
        t["b"] = {"types": {"quote_req"}, "lines": [2], "texts": ["Yes"], "terms": ["fna"], "group": "fna", "value": "Yes"}
        ents[0]["covered_by"] = ["a", "b"]
        self.assertEqual(verify.topic_gaps(2, lines, ents, t), [])


class RequestedStats(Chat):
    def test_a_requested_claim_that_overrode_call_lines_is_counted_for_the_glance_list(self):
        d = tempfile.mkdtemp(prefix="wrcs-")
        self.addCleanup(shutil.rmtree, d, True)
        lines = ["x", "Yes, there is credit life with Absa on the home loan."]
        jdump(os.path.join(d, "claims.json"), {"debts.0.cl": {"as": "Requested", "terms": [], "hits": [], "docs": [], "reviewed": "line 2 says credit life with Absa, which is about the first loan", "searched": "the form, the call", "weak": False}})
        out = verify.claim_stats(d, lines, {}, {})
        self.assertEqual([(c["key"], c["as"], c["hits"]) for c in out], [("debts.0.cl", "Requested", [2])])


class TwoProductsNextLine(Staged):
    """The second product is named on the NEXT line: that line is handled by the same entry, so it must be covered for its product too."""
    STAGE = "joint"
    TRANSCRIPT_EDIT = staticmethod(lambda text: text.replace("For the risk cover I will ask BrightRock for a new business FNA quote for you.",
                                                              "For the risk cover I will ask BrightRock for a new business FNA quote for you.\n\n0:08:40 Paul Kafentzis\nAnd a shortfall quote for the cover as well."))

    def form_json(self):
        return fna_blank_form()

    def answers(self):
        a = super().answers()
        a["sf_req"] = {"r": "differs", "line": self.L("a shortfall quote for the cover"), "quote": "a shortfall quote for the cover as well", "value": "Yes"}
        return a

    def test_g1_a_second_product_on_the_next_line_is_not_forgotten(self):
        n = self.L("new business FNA quote")
        src = [{"line": n, "quote": "ask BrightRock for a new business FNA quote"}]
        self.write("overlay.json", {"fills": [{"id": "z0", "key": "fna_req", "value": "Yes", "src": src}]})
        self.ok("compose", self.run_dir)
        e = next(e for e in self.load("ledger.json")["entries"] if e["kind"] == "quote_request" and "FNA" in e["quote"])
        self.ok("ledger", self.run_dir, "cover", e["id"], "z0")
        out = self.verify("--stage", "pre")
        self.assertTrue([ln for ln in fails(out) if "shortfall" in ln and "not covered for shortfall" in ln], fails(out))


# ----------------------------------------------------------------------------------------------------------------------------- G2: credit life
class CreditLifeWords(Chat):
    def test_g2_the_credit_life_phrases_are_hard_words(self):
        for text in ("Is there credit life on it?", "the Credit Life policy", "creditor life on the bond", "creditor-life cover", "you have life cover on the bond"):
            self.assertTrue(verify.hard_word(text), text)
        for text in ("my life cover is with BrightRock", "I pay my credit card on time", "a good life"):
            self.assertIsNone(verify.hard_word(text), text)

    def test_g2_the_fixture_lines_about_credit_life_are_hard_lines(self):
        lines = slurp(os.path.join(SKILL, "tests", "fixtures", "transcript_ff.txt")).split("\n")
        hard = verify.hard_lines(lines)
        self.assertIn(42, hard)
        self.assertIn(45, hard)

    def test_g2_the_credit_life_key_is_found_in_every_form_the_layout_uses(self):
        layout_text = slurp(os.path.join(SKILL, "scripts", "layout.json"))
        keys = sorted(set(re.findall(r'"key": "(cl_\w+)"', layout_text)))
        self.assertTrue(keys)                                                    # the layout has credit-life fields (cl_req, cl_lender, cl_bal, cl_life)
        for k in keys + ["debts.0.cl", "debts.3.cl"]:
            self.assertTrue(verify.credit_life_key(k), k)
        for k in ("debts.0.bal", "cell", "fna_req", "debts.0"):
            self.assertFalse(verify.credit_life_key(k), k)


class CreditLifeDismissed(Staged):
    """The reviewer's G2 route: the credit-life entry is not recorded and the lines are dismissed as soft."""
    STAGE = "pass2"
    LEDGER = [x for x in Chat.LEDGER if "credit life" not in x[0]]

    def test_g2_a_credit_life_line_cannot_be_dismissed(self):
        sh("tx.py", "scan", self.run_dir, ok=True)
        r = self.refused("ledger", self.run_dir, "review", "--line", "45", "--reason", "line 45 says: Yes, there is credit life with Absa on the home loan, so nothing needs recording")
        self.assertIn("cannot be dismissed", r.stdout + r.stderr)

    def test_g2_the_scan_step_will_not_finish_while_the_credit_life_lines_are_unhandled(self):
        sh("tx.py", "scan", self.run_dir, ok=True)
        r = self.refused("done", self.run_dir, "scan")
        self.assertIn("credit life", r.stdout + r.stderr)
        self.assertRegex(r.stdout + r.stderr, r"\b45\b")


class CreditLifeRequested(Staged):
    """'Requested' for the credit-life cell of the Absa loan, although the call says there is credit life on it (the reviewer's repro)."""
    STAGE = "joint"
    SEARCHED = "the form, the call, the Overview, other documents and Outlook were all searched for it"

    def claim(self, why=None):
        args = ["claim", self.run_dir, "--key", "debts.0.cl", "--as", "Requested", "--searched", self.SEARCHED]
        if why:
            args += ["--reviewed", why]
        return drv(*args)

    def test_g2_requested_is_refused_when_the_call_mentions_credit_life(self):
        self.ok("compose", self.run_dir)
        r = self.claim()
        self.assertNotEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("call lines", r.stdout + r.stderr)
        self.assertIn("45", r.stdout + r.stderr)

    def test_g2_a_reason_that_cites_the_line_and_quotes_it_lets_requested_through(self):
        self.ok("compose", self.run_dir)
        r = self.claim("line 45 says: Yes, there is credit life with Absa on the home loan, so this second loan is the one whose credit life nobody gave")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_g2_a_thin_reason_does_not(self):
        self.ok("compose", self.run_dir)
        r = self.claim("not said anywhere at all on the call")
        self.assertNotEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_g2_the_checker_repeats_the_rule_on_a_hand_made_claim(self):
        self.ok("compose", self.run_dir)
        path = self.p("claims.json")
        cl = jload(path) if os.path.exists(path) else {}
        cl["debts.0.cl"] = {"as": "Requested", "terms": [], "hits": [], "docs": [], "reviewed": "", "searched": self.SEARCHED, "weak": False, "t": "x"}
        jdump(path, cl)
        self.ok("compose", self.run_dir)
        out = self.verify("--stage", "pre")
        self.assertTrue(any("claim debts.0.cl 'Requested'" in ln and "call" in ln and "45" in ln for ln in fails(out)), fails(out))


class CreditLifeAnswer(Staged):
    """The credit-life answer (cl_req) cannot be 'Not discussed' / 'N/A' while the ledger records credit life on the call; the balance and the cover still may be, with a reason."""
    STAGE = "joint"
    WHY = "line 45 says there is credit life with Absa on the home loan, but this is a question about something else"

    def test_g2_not_discussed_and_na_are_refused_on_cl_req(self):
        self.ok("compose", self.run_dir)
        for word in ("Not discussed", "N/A"):
            r = self.refused("claim", self.run_dir, "--key", "cl_req", "--as", word, "--reviewed", self.WHY)
            self.assertIn("credit life", r.stdout + r.stderr)
            self.assertIn("line 45", r.stdout + r.stderr)

    def test_g2_the_balance_and_the_cover_may_still_be_not_discussed_with_a_reason(self):
        self.ok("compose", self.run_dir)
        for key in ("cl_bal", "cl_life"):
            self.ok("claim", self.run_dir, "--key", key, "--as", "Not discussed", "--reviewed",
                    "line 45 says there is credit life with Absa on the home loan, but it gives no balance and no cover amount for it")

    def test_g2_the_checker_repeats_it_on_a_hand_made_claim(self):
        self.ok("compose", self.run_dir)
        path = self.p("claims.json")
        cl = jload(path) if os.path.exists(path) else {}
        cl["cl_req"] = {"as": "Not discussed", "terms": [], "hits": [], "docs": [], "reviewed": self.WHY, "searched": "", "weak": False, "t": "x"}
        jdump(path, cl)
        self.ok("compose", self.run_dir)
        out = self.verify("--stage", "pre")
        self.assertTrue(any("claim cl_req 'Not discussed'" in ln and "credit life" in ln for ln in fails(out)), fails(out))


class NotApplicable(Staged):
    """'N/A' is as much a claim of silence as 'Not discussed': when the call mentions the field, the reason must cite a line and quote it."""
    STAGE = "joint"

    def test_na_on_a_field_the_call_mentions_needs_a_reason_that_cites_the_line(self):
        self.ok("compose", self.run_dir)
        r = self.refused("claim", self.run_dir, "--key", "cl_bal", "--as", "N/A", "--reviewed", "the client gave no balance for any loan on this call at all")
        self.assertIn("call lines", r.stdout + r.stderr)
        self.ok("claim", self.run_dir, "--key", "cl_bal", "--as", "N/A", "--reviewed", "line 45 says there is credit life with Absa on the home loan but no balance was given for it")

    def test_the_checker_repeats_it_on_a_hand_made_na_claim(self):
        self.ok("compose", self.run_dir)
        path = self.p("claims.json")
        cl = jload(path) if os.path.exists(path) else {}
        cl["cl_bal"] = {"as": "N/A", "terms": [], "hits": [], "docs": [], "reviewed": "the client gave no balance for any loan on this call at all", "searched": "", "weak": False, "t": "x"}
        jdump(path, cl)
        self.ok("compose", self.run_dir)
        out = self.verify("--stage", "pre")
        self.assertTrue(any("claim cl_bal 'N/A' but the call mentions it" in ln for ln in fails(out)), fails(out))


class CreditLifeCover(Staged):
    """The credit-life entry exists, but only a NOTE covers it: the cl fields are not answered."""
    STAGE = "joint"

    def test_g2_a_credit_life_line_covered_only_by_a_note_fails_and_names_credit_life(self):
        n = self.L("credit life with Absa")
        src = [{"line": n, "quote": "there is credit life with Absa on the home loan"}]
        self.write("overlay.json", {"notes": [{"id": "n1", "section": "debts", "text": "Absa home loan: the client asked about the credit life", "src": src}]})
        self.ok("compose", self.run_dir)
        led = self.load("ledger.json")
        e = next(e for e in led["entries"] if "credit life" in e["quote"])
        e["kind"] = "request"
        self.write("ledger.json", led)
        r = self.ok("ledger", self.run_dir, "cover", e["id"], "n1")
        self.assertIn("STILL OPEN", r.stdout)
        out = self.verify("--stage", "pre")
        bad = [ln for ln in fails(out) if "names credit life" in ln]
        self.assertTrue(bad, fails(out))
        self.assertIn("not covered for credit life", bad[0])

    def test_g2_a_credit_life_rows_add_covers_it(self):
        n = self.L("credit life with Absa")
        src = [{"line": n, "quote": "there is credit life with Absa on the home loan"}]
        self.write("overlay.json", {"rows_add": [{"id": "r1", "list": "debts", "cells": {"type": "Home loan", "prov": "Absa", "cl": "Yes"}, "src": src}]})
        self.ok("compose", self.run_dir)
        e = next(e for e in self.load("ledger.json")["entries"] if "credit life" in e["quote"])
        self.ok("ledger", self.run_dir, "cover", e["id"], "r1")
        out = self.verify("--stage", "pre")
        self.assertFalse([ln for ln in fails(out) if "names credit life" in ln], fails(out))

    def test_g2_a_credit_life_fill_covers_it(self):
        n = self.L("credit life with Absa")
        src = [{"line": n, "quote": "there is credit life with Absa on the home loan"}]
        self.write("overlay.json", {"fills": [{"id": "o1", "key": "debts.0.cl", "value": "Yes", "src": src}]})
        self.ok("compose", self.run_dir)
        e = next(e for e in self.load("ledger.json")["entries"] if "credit life" in e["quote"])
        self.ok("ledger", self.run_dir, "cover", e["id"], "o1")
        out = self.verify("--stage", "pre")
        self.assertFalse([ln for ln in fails(out) if "names credit life" in ln], fails(out))


# ----------------------------------------------------------------------------------------------------------------------------- the glance list
class SummaryGroups(Staged):
    STAGE = "joint"

    def test_the_summary_of_a_real_run_names_the_group_of_each_cover(self):
        self.s_content_done()
        text = "\n".join(verify.summary_lines(self.run_dir, self.load("state.json"), self.load("ledger.json"), self.load("content.json")))
        self.assertIn("fna_req [the FNA quote]", text)
        self.assertIn("o1 [a credit-life field]", text)
        self.assertIn("[products: FNA]", text)


class GlanceFull(Chat):
    def synthetic(self, text, covered=("quote.bf_sf",), n=6):
        d = tempfile.mkdtemp(prefix="wrgl-")
        self.addCleanup(shutil.rmtree, d, True)
        lines = ["we agree about item %d here" % i for i in range(1, n + 1)]
        lines[2] = text
        spit(os.path.join(d, "transcript.txt"), "\n".join(lines))
        ents = [{"id": "L3", "line": 3, "kind": "quote_request", "quote": text[:40], "covered_by": list(covered)}]
        st = {"scan": {"hits": [3], "closing_from": n + 1}, "total_lines": n, "chunks": [[1, n]]}
        return d, lines, st, {"entries": ents, "scan_reviewed": []}

    LONG = "Please ask BrightRock for a new business FNA quote and a shortfall quote for you and the family next week."

    def test_a_hard_word_line_is_printed_in_full(self):
        d, lines, st, led = self.synthetic(self.LONG)
        out = {x[0]: x for x in verify.request_resolutions(d, led, lines, st)}
        self.assertIn('"%s"' % self.LONG, out[3][2])
        self.assertGreater(len(self.LONG), 60)

    def test_a_line_without_a_hard_word_is_still_cut_at_sixty_characters(self):
        d, lines, st, led = self.synthetic("we agree about " + "word " * 30)
        out = {x[0]: x for x in verify.request_resolutions(d, led, lines, st)}
        self.assertEqual(len(re.match(r'line 3 "(.*?)"', out[3][2]).group(1)), 60)

    def test_the_products_named_in_the_window_and_the_covering_rows_group_are_printed(self):
        d, lines, st, led = self.synthetic(self.LONG)
        targets = {"quote.bf_sf": {"types": {"quote"}, "lines": [3], "texts": [], "terms": [], "group": "bf_sf"}}
        out = {x[0]: x for x in verify.request_resolutions(d, led, lines, st, targets)}
        self.assertIn("products: FNA, shortfall", out[3][2])
        self.assertIn("quote.bf_sf [the shortfall quote (bf)]", out[3][2])

    def test_the_summary_prints_them_too(self):
        d, lines, st, led = self.synthetic(self.LONG)
        text = "\n".join(verify.summary_lines(d, st, led, {}))
        self.assertIn(self.LONG, text)
        self.assertIn("products: FNA, shortfall", text)


# ----------------------------------------------------------------------------------------------------------------------------- wording
class Wording5(Chat):
    def test_the_attested_sentence_says_names_not_quotes(self):
        import inspect
        src = inspect.getsource(verify.report)
        self.assertNotIn("quotes at least 4 words", src)
        self.assertIn("names at least 4 of the line's words", src)

    def test_the_proven_paragraph_says_each_product_needs_its_cover_and_which_answers_the_conflict_covers(self):
        import inspect
        src = inspect.getsource(verify.report)
        self.assertIn("covered for each product", src)
        self.assertIn("'Not discussed', 'N/A' and 'not on the call'", src)

    def test_the_refusal_says_name_not_quote(self):
        lines = ["x", "For the risk cover I will ask BrightRock for a new business FNA quote for you."]
        _, prob = verify.dismissal_problem(["2"], "Is this fine?", lines)
        self.assertIn("name at least", prob)
        self.assertNotIn("quote at least", prob)

    def test_the_paul_page_has_a_fix_round_5_section_and_the_corrected_wording(self):
        text = slurp(os.path.join(SKILL, "history", "CHANGES-FOR-PAUL.md"))
        self.assertIn("Fix round 5", text)
        self.assertNotIn("quote at least 4 words", text)
        self.assertIn("names at least 4 of the line's words", text)
