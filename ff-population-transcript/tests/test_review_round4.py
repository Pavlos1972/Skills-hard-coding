"""Regression tests for the FOURTH (confirmation) review, fix round 4: three fresh routes to the same hole. Every test asserts that the program REFUSES (or FAILS) what the
reviewer showed it let through. Invented people only. F1, F2, F3 are the reviewer's ids."""
import json
import os
import re
import shutil
import tempfile

from support import Chat, Staged, H, drv, sh, jdump, jload, slurp, spit
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


# ----------------------------------------------------------------------------------------------------------------------------- F1: the right product's quote row
class QuoteProduct(Staged):
    """The FNA line (kind quote_request) covered by the SHORTFALL (bf) quote row, with the FNA fields claimed 'Not discussed'."""
    STAGE = "joint"

    def form_json(self):
        return fna_blank_form()

    def src(self):
        n = self.L("new business FNA quote")
        return [{"line": n, "quote": FNA}]

    def wrong_overlay(self):
        return {"fills": [{"id": "z1", "key": "bf_sf_req", "value": "Yes", "src": self.src()}],
                "quotes": [{"id": "z2", "group": "bf_sf", "insurer": "BrightRock", "mode": "New Business", "src": self.src()}]}

    def fna_entry(self):
        return next(e for e in self.load("ledger.json")["entries"] if e["kind"] == "quote_request")

    def test_f1_the_fna_line_cannot_be_covered_by_the_shortfall_quote_row(self):
        self.write("overlay.json", self.wrong_overlay())
        self.ok("compose", self.run_dir)
        e = self.fna_entry()
        r = self.refused("ledger", self.run_dir, "cover", e["id"], "quote.bf_sf")
        text = r.stdout + r.stderr
        self.assertIn("FNA", text)
        self.assertIn("shortfall", text.lower())

    def test_f1_the_fna_line_cannot_be_covered_by_the_shortfall_request_field_either(self):
        self.write("overlay.json", self.wrong_overlay())
        self.ok("compose", self.run_dir)
        r = self.refused("ledger", self.run_dir, "cover", self.fna_entry()["id"], "z1")
        self.assertIn("shortfall", (r.stdout + r.stderr).lower())

    def test_f1_the_right_product_still_covers(self):
        ov = {"fills": [{"id": "z1", "key": "fna_req", "value": "Yes", "src": self.src()}]}
        self.write("overlay.json", ov)
        self.ok("compose", self.run_dir)
        self.ok("ledger", self.run_dir, "cover", self.fna_entry()["id"], "z1")

    def test_f1_the_checker_repeats_the_product_rule(self):
        self.write("overlay.json", self.wrong_overlay())
        self.ok("compose", self.run_dir)
        led = self.load("ledger.json")
        for e in led["entries"]:
            if e["kind"] == "quote_request":
                e["covered_by"] = ["quote.bf_sf"]
        self.write("ledger.json", led)
        out = self.verify("--stage", "pre")
        self.assertTrue(any("shortfall" in ln.lower() and "FNA" in ln for ln in fails(out)), fails(out))

    def test_f1_not_discussed_on_the_fna_request_is_refused_while_the_ledger_records_the_request(self):
        self.ok("compose", self.run_dir)
        for key in ("fna_req", "fna_type", "fna_ins"):
            r = self.refused("claim", self.run_dir, "--key", key, "--as", "Not discussed",
                             "--reviewed", "line 66 says 'For the risk cover I will ask BrightRock' which is about the cover only")
            self.assertIn("quote request", r.stdout + r.stderr)

    def test_f1_the_checker_repeats_the_not_discussed_rule(self):
        self.ok("compose", self.run_dir)
        cl = self.load("claims.json")
        cl["fna_req"] = {"as": "Not discussed", "terms": ["fna"], "hits": [66], "docs": [], "searched": "", "weak": False,
                         "reviewed": "line 66 says 'For the risk cover I will ask BrightRock' which is about the cover only"}
        self.write("claims.json", cl)
        self.fresh_overlay({})
        out = self.verify("--stage", "pre")
        self.assertTrue(any("claim fna_req" in ln and "quote request" in ln for ln in fails(out)), fails(out))

    def test_f1_the_other_bf_product_is_not_blocked_by_an_fna_request(self):
        self.ok("compose", self.run_dir)
        self.ok("claim", self.run_dir, "--key", "bf_fna_req", "--as", "Not discussed",
                "--reviewed", "line 66 says 'For the risk cover I will ask BrightRock' which is about the main FNA quote, not a second (bf) one")

    def test_f1_the_products_of_a_line_are_named(self):
        self.assertEqual({p[0] for p in verify.products_in("an FNA and a shortfall quote")}, {"FNA", "shortfall"})
        self.assertEqual({p[0] for p in verify.products_in("the Retirement Goal Analysis")}, {"RGAR"})
        self.assertEqual({p[0] for p in verify.products_in("the education goal analysis")}, {"EGAR"})
        self.assertEqual(verify.products_in("I would like a quote"), [])


class QuoteProductPopulated(Staged):
    STAGE = "joint"

    def test_f1_a_not_on_the_call_answer_for_the_populated_fna_request_is_refused_too(self):
        items = self.load("crosscheck.json")
        for i in items:
            if i["key"] == "fna_req":
                i["answer"] = None
        self.write("crosscheck.json", items)
        r = self.refused("cross", self.run_dir, "--key", "fna_req", "--r", "not_on_call", "--reviewed", "line 66 says 'For the risk cover I will ask BrightRock' which is about the cover only")
        self.assertIn("quote request", r.stdout + r.stderr)


    def test_f1_the_checker_repeats_it_on_a_hand_edited_cross_check_answer(self):
        items = self.load("crosscheck.json")
        for i in items:
            if i["key"] == "fna_req":
                i["answer"] = {"r": "not_on_call", "reviewed": "line 66 says 'For the risk cover I will ask BrightRock' which is about the cover only", "hits": 1, "hit_lines": [66], "searched": ["fna"], "weak": False}
        self.write("crosscheck.json", items)
        self.ok("compose", self.run_dir)
        out = self.verify("--stage", "pre")
        self.assertTrue(any("crosscheck fna_req is 'not on the call'" in ln and "quote request" in ln for ln in fails(out)), fails(out))


# ----------------------------------------------------------------------------------------------------------------------------- F2: a generic question frees a hard line
class DismissalQuestion(Staged):
    STAGE = "pass2"
    LEDGER = [x for x in Chat.LEDGER if "new business FNA" not in x[0]]

    def form_json(self):
        return fna_blank_form()

    def ask(self, about, question, need="dismissals"):
        return drv("ask", self.run_dir, "--need", need, "--kind", "knowledge", "--question", question, "--searched", "the whole call, twice", "--about", about)

    def full_question(self, n):
        return "Line %d says: For the risk cover I will ask BrightRock for a new business FNA quote for you. Is that only a mention of last year's quote, and not a request?" % n

    def test_f2_a_generic_question_cannot_free_a_hard_line(self):
        n = self.L("new business FNA quote")
        r = self.ask(str(n), "Is this fine?")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("quote at least", r.stdout + r.stderr)

    def test_f2_the_question_must_quote_every_named_line(self):
        n, other = self.L("new business FNA quote"), self.L("Retirement Goal Analysis")
        r = self.ask("%d,%d" % (n, other), self.full_question(n))                    # quotes line 66 only
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("line %d" % other, r.stdout + r.stderr)

    def test_f2_one_answer_frees_at_most_five_lines(self):
        r = self.ask("60,61,62,63,64,65", "Line 60 line 61 line 62 line 63 line 64 line 65 are fine to dismiss, aren't they?")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("at most 5", r.stdout + r.stderr)

    def test_f2_a_wide_range_is_refused(self):
        for about in ("1-98", "50-60", "lines 1 - 98"):
            r = self.ask(about, "Is this whole stretch of the call fine to dismiss, as it is only chatter?")
            self.assertNotEqual(r.returncode, 0, about)
            self.assertIn("at most 5", r.stdout + r.stderr)

    def test_f2_a_question_that_quotes_the_line_frees_it_and_the_glance_list_shows_the_question_and_the_words(self):
        n = self.L("new business FNA quote")
        q = self.full_question(n)
        r = self.ask(str(n), q)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.ok("answer", self.run_dir, "--need", "dismissals", "--said", "Right, only a mention of last year's quote, not a request")
        sh("tx.py", "scan", self.run_dir, ok=True)
        self.ok("ledger", self.run_dir, "review", "--line", str(n), "--reason", "line %d only says: I will ask BrightRock for a new business FNA quote so nothing is wanted" % n)
        text = "\n".join(verify.summary_lines(self.run_dir, self.load("state.json"), self.load("ledger.json"), {}))
        self.assertIn("freed on Paul's recorded answer", text)
        self.assertIn(q, text)                                                          # the full question text
        self.assertIn("Right, only a mention of last year's quote, not a request", text)  # his recorded words
        self.assertIn("line %d" % n, text)

    def test_f2_a_hand_made_generic_question_frees_nothing_and_the_checker_says_so(self):
        n = self.L("new business FNA quote")
        sh("tx.py", "scan", self.run_dir, ok=True)
        qs = self.load("questions.json")
        qs.append({"need": "dismissals", "question": "Is this fine?", "kind": "knowledge", "about": [str(n)], "searched": "the call", "paul_said": "yes that is fine"})
        self.write("questions.json", qs)
        led = self.load("ledger.json")
        led["scan_reviewed"].append({"line": n, "reason": "line %d only says: I will ask BrightRock for a new business FNA quote so nothing is wanted" % n})
        self.write("ledger.json", led)
        self.assertNotIn(n, verify.paul_allowed_lines(self.run_dir))
        r = self.refused("done", self.run_dir, "scan")
        self.assertIn("cannot be dismissed", r.stdout)
        out = self.verify("--stage", "pre")
        self.assertTrue(any("does not free" in ln for ln in fails(out)), fails(out))

    def test_f2_a_hand_made_range_of_390_lines_frees_nothing(self):
        sh("tx.py", "scan", self.run_dir, ok=True)
        qs = self.load("questions.json")
        qs.append({"need": "dismissals", "question": "Is this whole stretch fine?", "kind": "knowledge", "about": ["1-390"], "searched": "the call", "paul_said": "yes that is fine"})
        self.write("questions.json", qs)
        self.assertEqual(verify.paul_allowed_lines(self.run_dir), {})

    def test_f2_a_huge_range_is_refused_before_it_is_expanded(self):
        lines = ["x"] * 10
        nums, prob = verify.dismissal_problem(["1-5000000"], "Is it fine?", lines)
        self.assertEqual(nums, [])
        self.assertIn("'1-5000000' names 5000000", prob)               # the range itself is refused, not the 5 million lines it would expand to

    def test_f2_the_question_helper_counts_content_words(self):
        lines = ["x", "For the risk cover I will ask BrightRock for a new business FNA quote for you."]
        lines_, prob = verify.dismissal_problem(["2"], "Is this about the risk cover, the BrightRock business quote?", lines)
        self.assertIsNone(prob)
        lines_, prob = verify.dismissal_problem(["2"], "Is this fine?", lines)
        self.assertIn("quote at least", prob)
        lines_, prob = verify.dismissal_problem(["3"], "Is this fine?", lines)
        self.assertIn("not in the transcript", prob)


# ----------------------------------------------------------------------------------------------------------------------------- F3: a soft line next to an entry that shares only a verb
def add_soft_request(text):
    key = "Please also send us your latest payslip."
    assert key in text
    return text.replace(key, key + "\n\n0:14:05 Pat Samplecase\nCan you also send me what BrightRock says about the cover?")


class SharedVerb(Staged):
    STAGE = "pass2"
    TRANSCRIPT_EDIT = staticmethod(add_soft_request)

    def test_f3_a_soft_line_next_to_an_entry_that_shares_only_a_verb_is_not_handled(self):
        n = self.L("send me what BrightRock says")
        sh("tx.py", "scan", self.run_dir, ok=True)
        r = self.refused("done", self.run_dir, "scan")
        self.assertIn(str(n), r.stdout)
        # a quoting review handles it
        self.ok("ledger", self.run_dir, "review", "--line", str(n), "--reason", "line %d says: Can you also send me what BrightRock says about the cover? so nothing else" % n)

    def test_f3_the_shared_word_must_be_a_topic_word(self):
        lines = ["x", "Please send us your latest payslip", "Can you also send me what BrightRock says about the cover?"]
        ents = [{"id": "L1", "line": 2, "kind": "next_step", "quote": "send us your latest payslip"}]
        self.assertIsNone(verify.line_resolution(3, lines, ents))                   # shares only 'send'
        lines[2] = "Can you also send me that payslip?"
        self.assertEqual(verify.line_resolution(3, lines, ents)["id"], "L1")        # shares 'payslip', a topic word

    def test_f3_the_filler_list(self):
        for word in ("send", "sent", "email", "ask", "sign", "need", "please", "would", "could", "your", "with", "that", "this", "have", "will", "also", "what", "says", "about"):
            self.assertIn(word, verify.REQUEST_FILLER)


# ----------------------------------------------------------------------------------------------------------------------------- the glance list: every request line with its text
class GlanceList(Chat):
    def synthetic(self, n=60, on=(), closing_from=50):
        d = tempfile.mkdtemp(prefix="wrgl-")
        self.addCleanup(shutil.rmtree, d, True)
        lines = ["we agree about item %d here" % i for i in range(1, n + 1)]
        spit(os.path.join(d, "transcript.txt"), "\n".join(lines))
        ents = [{"id": "L%d" % i, "line": i, "kind": "request", "quote": "we agree about item %d" % i, "covered_by": []} for i in on]
        st = {"scan": {"hits": list(range(1, n + 1)), "closing_from": closing_from}, "total_lines": n, "chunks": [[1, n]]}
        return d, lines, st, {"entries": ents, "scan_reviewed": [{"line": i, "reason": "line %d we agree about item only" % i} for i in range(1, n + 1) if i not in on and i % 7 == 0]}

    def test_every_request_line_is_listed_with_its_text_when_there_are_forty_or_fewer(self):
        d, lines, st, led = self.synthetic(n=30, on=(1, 2, 3))
        text = "\n".join(verify.summary_lines(d, st, led, {}))
        self.assertIn("how every request line was handled (all 30)", text)
        self.assertIn('line 2 "we agree about item 2 here" -> entry L2', text)
        self.assertIn('line 14 "we agree about item 14 here" dismissed', text)

    def test_text_is_cut_at_sixty_characters(self):
        d, lines, st, led = self.synthetic(n=3, on=(1,))
        lines[0] = "we agree about " + "word " * 30
        spit(os.path.join(d, "transcript.txt"), "\n".join(lines))
        out = verify.request_resolutions(d, led, lines, st)
        self.assertEqual(len(re.match(r'line 1 "(.*?)" ->', out[0][2]).group(1)), 60)
        self.assertTrue(out[0][1])                                                       # on its own entry

    def test_above_forty_lines_every_line_not_on_an_entry_and_the_closing_minutes_are_listed(self):
        d, lines, st, led = self.synthetic(n=60, on=(1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 55, 58), closing_from=50)
        text = "\n".join(verify.summary_lines(d, st, led, {}))
        self.assertIn("how every request line was handled", text)
        self.assertIn('line 20 "we agree about item 20 here" NOT HANDLED', text)      # not on an entry: listed
        self.assertIn('line 55 "we agree about item 55 here" -> entry L55', text)     # on an entry but in the closing minutes: listed
        self.assertNotIn('line 3 "we agree about item 3 here"', text)                  # on an entry, early: only counted
        self.assertRegex(text, r"and \d+ more directly on an entry")


# ----------------------------------------------------------------------------------------------------------------------------- wording
class Wording(Chat):
    def test_the_attested_sentence_says_exactly_what_is_checked_about_pauls_answers(self):
        import inspect
        src = inspect.getsource(verify.report)
        self.assertNotIn("the at most 10 ids it was about", src)
        self.assertIn("at most 5 lines", src)
        self.assertIn("quotes at least 4 words", src)
