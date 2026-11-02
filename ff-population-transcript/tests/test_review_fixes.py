"""Regression tests for the independent reviewer's findings (fix round 1). Every test here asserts that the program REFUSES (or FAILS) a thing the
reviewer showed it used to let through. Invented people only. The ids (A1 ... M10) are the reviewer's finding numbers."""
import json
import os
import re
import shutil
import subprocess
import sys

from support import (Chat, Staged, H, SCRIPTS, REPO, drv, sh, jdump, jload, slurp, spit, make_form_pdf, CLIENT, FIXTURE)
from fixtures import household as HH
import teams_driver


def fails(out):
    return [ln for ln in out.stdout.splitlines() if "[FAIL" in ln]


class Cover(Staged):
    """A1: a ledger entry is covered only by the KIND of item that can cover it, and that item must cite the same part of the call."""
    STAGE = "joint"

    def prepare(self):
        self.ok("compose", self.run_dir)
        self.ok("claim", self.run_dir, "--all-empty")
        self.ok("claim", self.run_dir, "--key", "pr_will", "--as", "Not discussed", "--reviewed", "line 54 only asks whether there is a will; no priority is given for it")
        self.write("overlay.json", {})
        self.ok("compose", self.run_dir)

    def test_a1_the_lead_search_cannot_cover_a_request_a_quote_or_a_next_step(self):
        self.prepare()
        for e in self.load("ledger.json")["entries"]:
            r = drv("ledger", self.run_dir, "cover", e["id"], "lead")
            self.assertNotEqual(r.returncode, 0, "the lead search was accepted as cover for %s %r" % (e["kind"], e["quote"]))
            self.assertIn("REFUSED", r.stdout + r.stderr)

    def test_a1_a_claim_of_not_discussed_cannot_cover_a_request_or_a_quote(self):
        self.prepare()
        for e in self.load("ledger.json")["entries"]:
            if e["kind"] in ("quote_request", "request", "next_step", "difference"):
                r = drv("ledger", self.run_dir, "cover", e["id"], "claim:pr_will")
                self.assertNotEqual(r.returncode, 0, "a 'Not discussed' claim covered a %s entry" % e["kind"])

    def test_a1_a_claim_whose_hits_sit_next_to_the_request_still_cannot_cover_it(self):
        self.prepare()
        e = next(e for e in self.load("ledger.json")["entries"] if e["kind"] == "request")
        cl = self.load("claims.json")
        cl["sp_tel"] = {"as": "Not discussed", "terms": ["spouse number"], "hits": [e["line"]], "docs": [], "reviewed": "lines next to the request", "searched": "", "weak": False}
        self.write("claims.json", cl)
        r = self.refused("ledger", self.run_dir, "cover", e["id"], "claim:sp_tel")
        self.assertIn("cannot cover a request", r.stdout + r.stderr)
        e2 = next(e for e in self.load("ledger.json")["entries"] if e["kind"] == "quote_request")
        cl["sp_tel"]["hits"] = [e2["line"]]
        self.write("claims.json", cl)
        r = self.refused("ledger", self.run_dir, "cover", e2["id"], "claim:sp_tel")
        self.assertIn("cannot cover a quote_request", r.stdout + r.stderr)

    def test_a1_a_fill_that_cites_another_part_of_the_call_cannot_cover(self):
        self.prepare()
        ov = {"fills": [{"id": "o9", "key": "debts.0.cl", "value": "Yes", "src": [{"line": self.L("Good evening Pat"), "quote": "Good evening Pat, thanks for joining the fact find"}]}]}
        self.fresh_overlay(ov)
        gap = next(e for e in self.load("ledger.json")["entries"] if "credit life" in e["quote"])
        r = self.refused("ledger", self.run_dir, "cover", gap["id"], "o9")
        self.assertIn("not within", r.stdout + r.stderr)

    def test_a1_a_hand_edited_ledger_that_covers_everything_with_lead_fails_the_checker(self):
        self.s_content_done()
        led = self.load("ledger.json")
        for e in led["entries"]:
            e["covered_by"] = ["lead"]
        self.write("ledger.json", led)
        out = self.verify("--stage", "pre")
        self.assertEqual(out.returncode, 1)
        self.assertIn("is not really covered", out.stdout)

    def test_a1_cover_by_an_item_that_does_not_exist_is_refused(self):
        self.prepare()
        e = self.load("ledger.json")["entries"][0]
        self.refused("ledger", self.run_dir, "cover", e["id"], "zz_nothing")


class NotDiscussed(Staged):
    """A2: 'Not discussed' is a claim the program searches for. Weak searches are never accepted without a reason written for that field."""
    STAGE = "joint"

    def test_a2_a_field_whose_search_finds_the_call_is_not_claimed_without_a_reason(self):
        self.ok("compose", self.run_dir)
        r = self.ok("claim", self.run_dir, "--all-empty")
        self.assertIn("pr_will", r.stdout)                                             # left for the chat, not claimed by the program
        self.assertNotIn("pr_will", self.load("claims.json"))
        r = self.refused("claim", self.run_dir, "--key", "pr_will", "--as", "Not discussed")
        self.assertIn("the search finds", r.stdout + r.stderr)
        self.refused("claim", self.run_dir, "--key", "pr_will", "--as", "Not discussed", "--reviewed", "ok")        # a real reason, not a word

    def test_a2_the_program_claims_only_what_its_own_search_finds_nothing_for(self):
        self.ok("compose", self.run_dir)
        self.ok("claim", self.run_dir, "--all-empty")
        cl = self.load("claims.json")
        self.assertTrue(cl, "nothing was claimed")
        for k, c in cl.items():
            self.assertEqual(c["hits"], [], "%s was claimed although the call mentions it" % k)
            self.assertFalse(c["weak"], "%s was claimed on a label-only search" % k)

    def test_a2_a_label_only_search_is_never_accepted_on_its_own(self):
        r = self.refused("cross", self.run_dir, "--key", "ip_abiv", "--r", "not_on_call")
        self.assertIn("WEAK", r.stdout + r.stderr)
        self.ok("cross", self.run_dir, "--key", "ip_abiv", "--r", "not_on_call", "--reviewed", "searched the whole call for any income protection percentage")
        self.assertTrue(next(i for i in self.load("crosscheck.json") if i["key"] == "ip_abiv")["answer"]["weak"])

    def test_a2_a_claim_on_label_words_only_is_refused_without_a_reason_for_that_field(self):
        import argparse
        import run as runmod
        import verify
        self.ok("compose", self.run_dir)
        orig = verify.field_terms
        verify.field_terms = lambda lay, key, label="", row_values=None: ([(label or key).lower()], False)        # a field that has no curated search words
        try:
            a = argparse.Namespace(run=self.run_dir, all_empty=False, key="home", as_="Not discussed", reviewed="", terms=None, searched=None)
            with self.assertRaises(SystemExit):
                runmod.cmd_claim(a)
            self.assertNotIn("home", self.load("claims.json"))
            a.reviewed = "searched the whole call for any home telephone number and found none"
            runmod.cmd_claim(a)
            self.assertTrue(self.load("claims.json")["home"]["weak"])                       # recorded, and counted as a weak search
        finally:
            verify.field_terms = orig

    def test_a2_not_on_the_call_is_refused_when_the_search_finds_the_call(self):
        r = self.refused("cross", self.run_dir, "--key", "employer", "--r", "not_on_call")
        self.assertIn("the call mentions it", r.stdout + r.stderr)

    def test_a2_the_rest_command_leaves_the_found_fields_to_the_chat(self):
        base = self.load("crosscheck.json")
        left = [i["key"] for i in base if not i.get("answer")]
        self.assertEqual(left, [], "the staged run answered everything")
        # a fresh cross-check file: nothing answered, so the program must list what it found in the call
        items = self.load("crosscheck.json")
        for i in items:
            i["answer"] = None
        self.write("crosscheck.json", items)
        r = self.ok("cross", self.run_dir, "--rest", "not_on_call")
        self.assertIn("LEFT for you", r.stdout)
        todo = [i["key"] for i in self.load("crosscheck.json") if not i.get("answer")]
        self.assertIn("employer", todo)
        self.assertIn("fna_req", todo)
        r = self.refused("done", self.run_dir, "crosscheck")

    def test_a2_requested_needs_a_recorded_outlook_search_not_the_word_outlook(self):
        rj = self.load("lead.json")
        rj["searched"] = []
        self.write("lead.json", rj)
        self.ok("compose", self.run_dir)
        r = self.refused("claim", self.run_dir, "--key", "debts.0.cl", "--as", "Requested", "--searched", "searched the form, the call, the Overview, other documents and Outlook")
        self.assertIn("Requested", r.stdout + r.stderr)

    def test_a2_contact_details_are_not_claimed_before_the_lead_search(self):
        rj = self.load("lead.json")
        rj["searched"] = []
        self.write("lead.json", rj)
        self.ok("compose", self.run_dir)
        r = self.ok("claim", self.run_dir, "--all-empty")
        self.assertIn("run.py lead first", r.stdout)
        self.assertNotIn("home", self.load("claims.json"))
        self.refused("claim", self.run_dir, "--key", "home", "--as", "Not discussed")

    def test_a2_credit_life_claimed_as_not_discussed_when_the_form_says_it_exists_is_refused(self):
        import verify
        import ffform
        f = HH.pat_form()
        f["l"]["debts"][0]["d"]["cl"] = "Yes"
        p_ = os.path.join(self.tmp, "cl.json")
        jdump(p_, f)
        fr = ffform.read_form(p_)
        lay = verify.w.layout()
        self.assertTrue(verify.sibling_hits(lay, fr, "cl_bal"), "the form says a debt has credit life: 'Not discussed' would contradict it")
        f["l"]["debts"][0]["d"]["cl"] = "No"
        jdump(p_, f)
        self.assertFalse(verify.sibling_hits(lay, ffform.read_form(p_), "cl_bal"))


class OverlayLanding(Staged):
    """A3: every overlay entry must land in the document; names that land nowhere are refused with the list of valid ones."""
    STAGE = "joint"

    def cite(self, text="Thursday the twelfth at four works"):
        return [{"line": self.L(text), "quote": text}]

    def refused_with(self, overlay, *words):
        self.write("overlay.json", overlay)
        r = self.refused("compose", self.run_dir)
        text = r.stdout + r.stderr
        self.assertNotIn("Traceback", text)
        for w_ in words:
            self.assertIn(w_, text)
        return text

    def test_a3_a_note_in_a_section_that_does_not_exist_is_refused_and_the_valid_ones_are_listed(self):
        self.refused_with({"notes": [{"id": "n1", "section": "no_such_section", "text": "Client wants cover for a new baby", "src": self.cite()}]}, "no_such_section", "Valid sections")

    def test_a3_a_flag_in_a_section_that_does_not_exist_is_refused(self):
        self.refused_with({"flags": [{"id": "f1", "section": "typo", "text": "Check the will", "src": self.cite()}]}, "typo", "Valid sections")

    def test_a3_a_row_for_a_list_that_does_not_exist_is_refused(self):
        self.refused_with({"rows_add": [{"id": "r1", "list": "no_such_list", "cells": {"a": "b"}, "src": self.cite()}]}, "no_such_list", "Valid lists")

    def test_a3_a_row_with_a_column_that_does_not_exist_is_refused(self):
        self.refused_with({"rows_add": [{"id": "r1", "list": "debts", "cells": {"zzz": "b"}, "src": self.cite()}]}, "zzz", "Valid columns")

    def test_a3_a_fill_for_a_field_that_does_not_exist_is_refused(self):
        self.refused_with({"fills": [{"id": "f9", "key": "lc_aciv_typo", "value": "7%", "src": self.cite()}]}, "lc_aciv_typo", "Valid keys")

    def test_a3_a_fill_for_a_list_row_that_does_not_exist_is_refused(self):
        self.refused_with({"fills": [{"id": "f9", "key": "debts.9.cl", "value": "Yes", "src": self.cite()}]}, "debts has only 2 row(s)")

    def test_a3_a_quote_group_that_does_not_exist_is_refused(self):
        self.refused_with({"quotes": [{"id": "q1", "group": "nope", "insurer": "BrightRock", "mode": "New Business", "src": self.cite()}]}, "nope", "Valid groups")

    def test_a3_an_id_used_twice_is_refused(self):
        n = {"id": "n1", "section": "next", "text": "A note", "src": self.cite()}
        self.refused_with({"notes": [n, dict(n)]}, "used twice")

    def test_a3_the_content_step_lists_every_valid_name_so_nothing_is_guessed(self):
        r = self.ok("next", self.run_dir)
        self.assertIn("THE VALID NAMES", r.stdout)
        for name in ("lc_aciv", "debts", "ret_ra", "advisor", "fna", "dd_abiv"):
            self.assertIn(name, r.stdout)

    def test_a3_the_aci_fill_beats_the_pending_default(self):
        ov = {"fills": [{"id": "f9", "key": "lc_aciv", "value": "7%", "src": self.cite()}]}
        self.write("overlay.json", ov)
        self.ok("compose", self.run_dir)
        c = self.load("content.json")
        rows = {r["id"]: r for s in c["sections"] for b in s["blocks"] for r in b["rows"]}
        self.assertIn("7%", json.dumps(rows["lc_aciv"]["bullets"]))
        self.assertNotIn("f9", c.get("overlay_unused") or [])

    def test_a3_a_valid_entry_that_lands_nowhere_is_listed_and_fails_the_checker(self):
        # a difference for a field the form does not hold (tax is empty in the form): the entry is valid but there is nothing to attach it to
        ov = {"diffs": [{"id": "d1", "key": "tax", "other": "1234567890", "label": "the Overview", "src": self.cite("Thursday the twelfth at four works")}]}
        self.write("overlay.json", ov)
        self.ok("compose", self.run_dir)
        c = self.load("content.json")
        self.assertIn("d1", c["overlay_unused"])
        out = self.verify("--stage", "pre")
        self.assertEqual(out.returncode, 1)
        self.assertTrue(any("d1" in ln for ln in fails(out)), fails(out))

    def test_m2_malformed_overlay_entries_get_plain_messages_and_never_a_traceback(self):
        cases = {
            "fill without value": {"fills": [{"id": "x", "key": "debts.0.cl", "src": self.cite()}]},
            "note without text": {"notes": [{"id": "x", "section": "next", "src": self.cite()}]},
            "quote insurer a number": {"quotes": [{"id": "x", "group": "fna", "insurer": 5, "mode": "New Business", "src": self.cite()}]},
            "next_steps without text": {"next_steps": [{"id": "x"}]},
            "abi_override without value": {"abi_override": [{"id": "x", "key": "dd_abiv"}]},
            "entry that is not an object": {"notes": ["a note"]},
            "overlay that is a list": [],
        }
        for name, ov in cases.items():
            self.write("overlay.json", ov)
            r = drv("compose", self.run_dir)
            self.assertNotEqual(r.returncode, 0, name)
            self.assertNotIn("Traceback", r.stderr + r.stdout, name)
            self.assertIn("overlay", r.stdout + r.stderr, name)


# ---------------------------------------------------------------------------------------------------------------- A5, A6: documents and quotes
class Documents(Staged):
    """A5: an Overview or a Policy schedule is accepted only with a text copy that is this client's; figures and long numbers must be in recorded text."""
    STAGE = "prep"

    def source(self, kind, text, ref="Some document", with_text=True):
        args = ["source", self.run_dir, "--kind", kind, "--path", "C:\\liferisk.co.za\\Company - Paul\\New Business\\Samplecase, Pat\\1. Overview\\x.pdf", "--date", "2026-10-30", "--read", "yes", "--ref", ref]
        if with_text:
            tf = os.path.join(self.tmp, ref + ".txt")
            spit(tf, text)
            args += ["--text-file", tf]
        return drv(*args)

    def test_a5_an_overview_without_a_text_copy_is_refused(self):
        r = self.source("Overview", "", ref="Made-up Overview", with_text=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("text copy", r.stdout + r.stderr)

    def test_a5_a_policy_schedule_without_a_text_copy_is_refused(self):
        r = self.source("Policy schedule", "", ref="Made-up schedule", with_text=False)
        self.assertNotEqual(r.returncode, 0)

    def test_a5_a_schedule_whose_text_never_mentions_the_client_is_refused(self):
        r = self.source("Policy schedule", "hello world nothing to do with the client", ref="Junk schedule")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("does not mention the client", r.stdout + r.stderr)

    def test_a5_an_overview_of_another_client_is_refused(self):
        r = self.source("Overview", "WR Overview for Robin Testcase. Fakeco unit trust R 777 000.00", ref="Other client's Overview")
        self.assertNotEqual(r.returncode, 0)

    def test_a5_the_documents_step_does_not_close_on_a_refused_overview(self):
        self.source("Overview", "nothing", ref="Junk overview")
        r = self.refused("done", self.run_dir, "documents")
        self.assertIn("Overview", r.stdout)


class LongNumbers(Staged):
    """A5 (C1): a policy or account number of six digits or more is printed only when a recorded schedule or Overview holds it."""
    STAGE = "joint"

    def test_a5_an_invented_policy_number_in_a_note_fails_the_checker(self):
        ov = {"notes": [{"id": "n1", "section": "next", "text": "Old Mutual policy 7654321 is paid up",
                         "src": [{"line": self.L("Thursday the twelfth at four works"), "quote": "Thursday the twelfth at four works"}]}]}
        self.write("overlay.json", ov)
        self.ok("compose", self.run_dir)
        out = self.verify("--stage", "pre")
        self.assertEqual(out.returncode, 1)
        self.assertTrue(any("7654321" in ln for ln in fails(out)), fails(out))

    def test_a5_a_note_citing_a_document_that_was_never_recorded_fails(self):
        ov = {"notes": [{"id": "n1", "section": "next", "text": "Overview shows a unit trust worth R 777 000.00",
                         "src": [{"doc": "Overview", "ref": "Fake Overview", "quote": "unit trust worth R 777 000.00"}]}]}
        self.write("overlay.json", ov)
        r = drv("compose", self.run_dir)
        out = self.verify("--stage", "pre")
        self.assertEqual(out.returncode, 1)
        self.assertTrue(any("Fake Overview" in ln for ln in fails(out)) or r.returncode != 0, (fails(out), r.stdout, r.stderr))

    def test_a5_a_figure_that_is_in_no_source_fails(self):
        ov = {"notes": [{"id": "n1", "section": "next", "text": "Client also has R 888 000.00 in a unit trust",
                         "src": [{"line": self.L("Thursday the twelfth at four works"), "quote": "Thursday the twelfth at four works"}]}]}
        self.write("overlay.json", ov)
        self.ok("compose", self.run_dir)
        out = self.verify("--stage", "pre")
        self.assertEqual(out.returncode, 1)
        self.assertTrue(any("888" in ln for ln in fails(out)), fails(out))


class QuoteBasis(Staged):
    """A6: the insurer and New Business / Servicing of a quote request must be in a source the entry cites."""
    STAGE = "joint"

    def form_json(self):
        f = HH.pat_form()
        for k in ("fna_type", "fna_ins"):
            f["f"][k] = {"v": "", "st": "empty"}
        return f

    def test_a6_an_insurer_that_the_cited_line_does_not_name_fails(self):
        ov = {"quotes": [{"id": "q1", "group": "fna", "insurer": "Discovery", "mode": "New Business",
                          "src": [{"line": self.L("Good evening Pat"), "quote": "Good evening Pat, thanks for joining the fact find"}]}]}
        self.write("overlay.json", ov)
        self.ok("compose", self.run_dir)
        out = self.verify("--stage", "pre")
        self.assertEqual(out.returncode, 1)
        self.assertTrue(any("Discovery" in ln for ln in fails(out)), fails(out))

    def test_a6_servicing_is_never_a_default(self):
        ov = {"quotes": [{"id": "q1", "group": "fna", "insurer": "BrightRock", "mode": "Servicing",
                          "src": [{"line": self.L("new business FNA quote"), "quote": "I will ask BrightRock for a new business FNA quote for you"}]}]}
        self.write("overlay.json", ov)
        self.ok("compose", self.run_dir)
        out = self.verify("--stage", "pre")
        self.assertTrue(any("Servicing" in ln for ln in fails(out)), fails(out))

    def test_a6_a_quote_entry_also_settles_the_forms_own_empty_insurer_and_basis_rows(self):
        ov = {"quotes": [{"id": "q1", "group": "fna", "insurer": "BrightRock", "mode": "New Business",
                          "src": [{"line": self.L("new business FNA quote"), "quote": "I will ask BrightRock for a new business FNA quote for you"}]}]}
        self.write("overlay.json", ov)
        self.ok("compose", self.run_dir)
        c = self.load("content.json")
        rows = {r["id"]: r for s in c["sections"] for b in s["blocks"] for r in b["rows"]}
        self.assertEqual(rows["fna_type"]["bullets"], ["New Business"])
        self.assertEqual(rows["fna_ins"]["bullets"], ["BrightRock"])
        self.assertEqual(rows["fna_ins"]["status"], "filled")                      # not 'Not discussed' beside a named insurer
        self.assertNotIn("q1", c["overlay_unused"])

    def test_a6_the_call_that_names_both_is_accepted(self):
        ov = {"quotes": [{"id": "q1", "group": "fna", "insurer": "BrightRock", "mode": "New Business",
                          "src": [{"line": self.L("new business FNA quote"), "quote": "I will ask BrightRock for a new business FNA quote for you"}]}]}
        self.write("overlay.json", ov)
        self.ok("compose", self.run_dir)
        out = self.verify("--stage", "pre")
        quote_fails = [ln for ln in fails(out) if "ledger" not in ln and ("quote.fna" in ln or "insurer and basis" in ln or "no default" in ln or "never a default" in ln or "Discovery" in ln)]
        self.assertEqual(quote_fails, [])


class QuoteEmptyForm(Staged):
    STAGE = "joint"

    def form_json(self):
        f = HH.pat_form()
        for k in ("fna_req", "fna_type", "fna_ins"):
            f["f"][k] = {"v": "", "st": "empty"}
        return f

    def test_i1_a_quote_request_on_the_call_with_an_empty_form_cannot_be_dropped(self):
        """The call asks for an FNA quote but the form's request box is empty: 'Not discussed' for the request contradicts the ledger."""
        self.ok("compose", self.run_dir)
        self.ok("claim", self.run_dir, "--all-empty")
        self.assertNotIn("fna_req", self.load("claims.json"))                       # the program did not claim it: the call mentions it
        r = self.refused("claim", self.run_dir, "--key", "fna_req", "--as", "Not discussed")
        self.assertIn("the search finds", r.stdout + r.stderr)
        # with a long reason the claim is recorded, but the ledger's quote_request entry then has nothing that can cover it
        self.ok("claim", self.run_dir, "--key", "fna_req", "--as", "Not discussed", "--reviewed", "line 66 is the FNA quote but the client did not ask for it herself")
        self.write("overlay.json", {})
        self.ok("compose", self.run_dir)
        e = next(e for e in self.load("ledger.json")["entries"] if e["kind"] == "quote_request")
        r = self.refused("ledger", self.run_dir, "cover", e["id"], "claim:fna_req")
        self.assertIn("cannot cover a quote_request", r.stdout + r.stderr)
        # filling the request from the call is what covers it
        ov = {"fills": [{"id": "f1", "key": "fna_req", "value": "Yes", "src": [{"line": self.L("new business FNA quote"), "quote": "I will ask BrightRock for a new business FNA quote"}]}]}
        self.write("claims.json", {k: v for k, v in self.load("claims.json").items() if k != "fna_req"})
        self.write("overlay.json", ov)
        self.ok("compose", self.run_dir)
        self.ok("ledger", self.run_dir, "cover", e["id"], "f1")


# ---------------------------------------------------------------------------------------------------------------- A7: Paul's own words
class PaulsWords(Staged):
    STAGE = "joint"

    def abi(self, ask="abi_dd"):
        return {"abi_override": [{"id": "ab1", "key": "dd_abiv", "value": "8%", "ask": ask}]}

    def test_a7_words_typed_into_the_overlay_are_refused(self):
        ov = {"abi_override": [{"id": "ab1", "key": "dd_abiv", "value": "8%", "paul_said": "make it 8%"}]}
        self.write("overlay.json", ov)
        r = self.refused("compose", self.run_dir)
        self.assertIn("Paul's answer", r.stdout + r.stderr)

    def test_a7_an_asked_paul_list_in_the_overlay_is_refused(self):
        self.write("overlay.json", {"asked_paul": [{"id": "q1", "about": "ABI", "question": "Which ABI for dread disease?", "suggestion": "5%", "paul_said": "yes 8%"}]})
        r = self.refused("compose", self.run_dir)
        self.assertIn("asked_paul is no longer accepted", r.stdout + r.stderr)

    def test_a7_a_question_that_was_asked_but_not_answered_is_not_paul_saying_yes(self):
        self.ok("ask", self.run_dir, "--need", "abi_dd", "--kind", "knowledge", "--question", "Which ABI for the dread disease cover of this client?", "--searched", "the form, the call and the standing rules")
        self.write("overlay.json", self.abi())
        self.refused("compose", self.run_dir)

    def test_a7_an_answer_recorded_through_the_program_is_used_and_always_on_the_glance_list(self):
        self.ok("ask", self.run_dir, "--need", "abi_dd", "--kind", "knowledge", "--question", "Which ABI for the dread disease cover of this client?", "--searched", "the form, the call and the standing rules")
        self.ok("answer", self.run_dir, "--need", "abi_dd", "--said", "Make it 8% for this client")
        self.write("overlay.json", self.abi())
        self.ok("compose", self.run_dir)
        c = self.load("content.json")
        self.assertTrue(any("Paul" in g and "8%" in g for g in c["glance"]), c["glance"])
        row = next(r for s in c["sections"] for b in s["blocks"] for r in b["rows"] if r["id"] == "dd_abiv")
        self.assertIn("8%", json.dumps(row["bullets"]))

    def test_a7_a_file_question_cannot_be_asked_before_the_routes_were_tried(self):
        r = self.refused("ask", self.run_dir, "--need", "Overview", "--kind", "file", "--question", "Where is the Overview?", "--searched", "nowhere yet at all")
        self.assertIn("REFUSED", r.stdout + r.stderr)


# ---------------------------------------------------------------------------------------------------------------- A8, M4: the form's saved PDF and the data file
class FormFiles(Staged):
    STAGE = "locate"

    def test_a8_the_saved_pdf_of_another_client_stops_the_job(self):
        self.ok("form", self.run_dir, self.form_path)
        p_ = os.path.join(self.tmp, "robin.pdf")
        make_form_pdf(p_, HH.robin_form())
        r = self.refused("formpdf", self.run_dir, p_)
        self.assertEqual(r.returncode, 5)
        self.assertIn("STOP", r.stdout)
        self.assertFalse(os.path.exists(self.p("form_pdf.json")))

    def test_a8_a_pdf_that_has_no_date_of_this_meeting_stops_the_job(self):
        self.ok("form", self.run_dir, self.form_path)
        p_ = os.path.join(self.tmp, "nodate.pdf")
        f = HH.pat_form()
        f["f"]["date"]["v"] = ""
        make_form_pdf(p_, f)
        r = self.refused("formpdf", self.run_dir, p_)
        self.assertEqual(r.returncode, 5)

    def test_a8_a_pdf_that_never_names_the_client_stops_the_job(self):
        self.ok("form", self.run_dir, self.form_path)
        p_ = os.path.join(self.tmp, "nosurname.pdf")
        f = HH.pat_form()
        f["f"]["sname"]["v"] = ""
        for kid in f["l"]["kids"]:
            kid["d"]["sname"] = ""
        make_form_pdf(p_, f)
        r = self.refused("formpdf", self.run_dir, p_)
        self.assertEqual(r.returncode, 5)
        self.assertIn("surname", r.stdout)

    def test_a8_a_pdf_with_more_than_a_quarter_of_the_values_missing_stops_the_job(self):
        self.ok("form", self.run_dir, self.form_path)
        p_ = os.path.join(self.tmp, "thin.pdf")
        drop = [k for k in self.form["f"] if k not in ("fname", "sname", "date", "consent")]
        make_form_pdf(p_, self.form, drop=drop)
        r = self.refused("formpdf", self.run_dir, p_)
        self.assertEqual(r.returncode, 5)
        self.assertIn("not in this PDF", r.stdout)

    def test_a8_format_only_needs_a_quote_that_holds_the_value(self):
        self.ok("form", self.run_dir, self.form_path)
        p_ = os.path.join(self.tmp, "short.pdf")
        make_form_pdf(p_, self.form, drop=("edu",))
        self.ok("formpdf", self.run_dir, p_)
        self.refused("pdfreview", self.run_dir, "--key", "edu", "--result", "format_only", "--quote", "WR Fact Find v3.0")
        self.refused("pdfreview", self.run_dir, "--key", "edu", "--result", "format_only", "--quote", "words that are not in the PDF at all")

    def test_m4_the_data_file_of_another_client_is_refused_also_with_again(self):
        self.ok("form", self.run_dir, self.form_path)
        p_ = os.path.join(self.tmp, "robin.json")
        jdump(p_, HH.robin_form())
        for extra in ((), ("--again",)):
            r = self.refused("form", self.run_dir, p_, *extra)
            self.assertEqual(r.returncode, 5)
            self.assertIn("is not the right file for this run", r.stdout.replace("\n", " ") if "is not the right file" in r.stdout else r.stdout)
        self.assertEqual(self.load("form_read.json")["client"]["surname"], "Samplecase")          # nothing of hers was saved

    def test_a8_amounts_are_compared_exactly_and_words_as_whole_words(self):
        import ffform
        n = lambda t: (ffform.w.norm(t), ffform._compact(t))  # noqa: E731
        t = "Home loan balance: R 1 450 000.00\n"
        self.assertFalse(ffform.value_in_pdf("R 45 000.00", t, *n(t)[:1], n(t)[1]))
        t2 = "salary R25,000.00"
        self.assertFalse(ffform.value_in_pdf("R 5 000.00", t2, n(t2)[0], n(t2)[1]))
        self.assertTrue(ffform.value_in_pdf("R 25 000.00", t2, n(t2)[0], n(t2)[1]))
        t3 = "Patricia"
        self.assertFalse(ffform.value_in_pdf("Pat", t3, n(t3)[0], n(t3)[1]))
        t4 = "Retire at 1650 next year"
        self.assertFalse(ffform.value_in_pdf("65", t4, n(t4)[0], n(t4)[1]))


# ---------------------------------------------------------------------------------------------------------------- A9: where the PDF is saved
class SaveFolders(Staged):
    STAGE = "check"

    def test_a9_only_the_clients_own_fact_find_folder_is_accepted(self):
        for folder in ("C:\\liferisk.co.za\\Company - Paul\\New Business\\Someone, Else\\2. Fact Find",
                       "C:\\liferisk.co.za\\Company - WR Clients\\Other Broker (Client Files)\\Samplecase, Pat\\2. Fact Find",
                       "C:\\liferisk.co.za\\Company - WR Clients\\Paul Kafentzis (Client Files)\\Zed, Other\\2. Fact Find",
                       "D:\\temp\\2. Fact Find",
                       "C:\\liferisk.co.za\\Company - Paul\\New Business\\Samplecase, Pat\\3. Applications",
                       "C:\\liferisk.co.za\\Company - Paul\\2. Fact Find"):
            r = self.s_pdf(expect_refusal=True, folder=folder)
            self.assertNotEqual(r.returncode, 0, "accepted the folder " + folder)
            self.assertIn("saved.folder", r.stdout)

    def test_a9_both_real_roots_are_accepted_for_the_clients_own_folder(self):
        self.s_pdf(folder="C:\\liferisk.co.za\\Company - WR Clients\\Paul Kafentzis (Client Files)\\Samplecase, Pat\\2. Fact Find")


# ---------------------------------------------------------------------------------------------------------------- A10, A11, A12: starting the job
class Starting(Chat):
    def test_a10_a_run_folder_that_belongs_to_another_client_or_date_is_refused(self):
        self.s_start()
        r = drv("start", self.run_dir, "--client", "Zed Otherperson", "--date", "01/01/2027")
        self.assertEqual(r.returncode, 2)
        self.assertIn("already belongs to", r.stdout + r.stderr)
        r = drv("start", self.run_dir, "--client", "Pat Samplecase", "--date", "06/11/2026")
        self.assertEqual(r.returncode, 2)
        self.assertEqual(self.load("run.json")["client"]["surname"], "Samplecase")
        r = drv("start", self.run_dir, *CLIENT)                                  # the same client and date just shows where it is up to
        self.assertEqual(r.returncode, 0)
        self.assertIn("already exists", r.stdout)

    def test_a2_nothing_can_be_run_ahead_of_its_step(self):
        self.s_start()
        self.s_locate()
        r = self.refused("done", self.run_dir, "final")
        self.assertIn("finish step 'form' first", r.stdout + r.stderr)
        for script in ("build.py", "verify.py"):
            r = sh(script, self.run_dir)
            self.assertNotEqual(r.returncode, 0, script)
            self.assertIn("MISSING: state.json", r.stdout + r.stderr)
            self.assertNotIn("Traceback", r.stderr)
        self.assertFalse(os.path.exists(self.p("out")) and os.listdir(self.p("out")))           # nothing was built

    def test_a8_the_schema_is_read_as_a_value_not_as_a_spelling(self):
        self.s_start()
        self.s_locate()
        f = HH.pat_form()
        p_ = os.path.join(self.tmp, "schema.json")
        f["schema"] = "3.1"
        jdump(p_, f)
        r = drv("form", self.run_dir, p_)
        self.assertEqual(r.returncode, 4)
        self.assertIn("STOP", r.stdout)
        self.assertFalse(os.path.exists(self.p("form_read.json")))                               # nothing was saved
        f["schema"] = 3.0                                                                         # the number 3.0 is the same version as the text "3.0"
        jdump(p_, f)
        self.ok("form", self.run_dir, p_)

    def test_a11_several_first_names_are_kept_together(self):
        import wrlib as w_
        self.assertTrue(w_.same_person("Mary Jane", "Samplecase", "Mary", "Jane Samplecase"))
        self.assertTrue(w_.same_person("Pat", "van der Merwe", "Pat van", "der Merwe"))
        self.assertFalse(w_.same_person("Mary", "Samplecase", "Jane", "Samplecase"))
        self.assertFalse(w_.same_person("", "Samplecase", "", "Samplecase"))
        r = self.ok("start", self.run_dir, "--client", "Mary Jane Samplecase", "--date", "05/11/2026")
        self.assertIn("NOTE: taking", r.stdout)
        rj = self.load("run.json")
        self.assertEqual((rj["client"]["first"], rj["client"]["surname"]), ("Mary", "Jane Samplecase"))
        d2 = os.path.join(self.tmp, "run2")
        self.ok("start", d2, "--first", "Mary Jane", "--surname", "Samplecase", "--client", "x", "--date", "05/11/2026")
        self.assertEqual(jload(os.path.join(d2, "run.json"))["client"], {"first": "Mary Jane", "surname": "Samplecase"})
        self.refused("start", os.path.join(self.tmp, "run3"), "--client", "Pat", "--date", "05/11/2026")                 # a surname is needed
        self.refused("start", os.path.join(self.tmp, "run4"), "--client", "Pat Samplecase", "--date", "31/02/2026")      # a real date is needed

    def test_a12_a_transcript_of_another_date_stops_the_job_at_the_prep_step(self):
        old = slurp(self.transcript).replace("Meeting started: 05/11/2026, 17:00", "Meeting started: 03/03/2025, 17:00")
        self.transcript = os.path.join(self.tmp, "old_transcript.txt")
        spit(self.transcript, old)
        self.s_start()
        self.s_locate()
        self.s_form()
        sh("tx.py", "prep", self.transcript, self.run_dir, ok=True)
        r = self.refused("done", self.run_dir, "prep")
        self.assertIn("another meeting's transcript", r.stdout)
        out = self.verify("--stage", "pre")
        self.assertTrue(any("another meeting's transcript" in ln for ln in fails(out)), fails(out))


# ---------------------------------------------------------------------------------------------------------------- A13: the programs must not change during a run
class Fingerprint(Chat):
    def copy_skill(self):
        src = os.path.dirname(SCRIPTS)
        dst = os.path.join(self.tmp, "skill-copy")
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("tests", "__pycache__", "history"))
        return dst

    def run_in(self, skill, *args):
        env = dict(os.environ, WR_CHUNK_LINES="25")
        env.pop("WR_SCRIPTS", None)
        return subprocess.run([sys.executable, os.path.join(skill, "scripts", "run.py")] + [str(a) for a in args], capture_output=True, text=True, env=env)

    def test_a13_a_program_edited_during_a_run_stops_the_run_and_fails_the_checker(self):
        skill = self.copy_skill()
        r = self.run_in(skill, "start", self.run_dir, *CLIENT)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue(self.load("run.json")["program_fingerprint"])
        env = dict(os.environ, WR_CHUNK_LINES="25")
        env.pop("WR_SCRIPTS", None)
        subprocess.run([sys.executable, os.path.join(skill, "scripts", "tx.py"), "prep", self.transcript, self.run_dir], capture_output=True, text=True, env=env, check=True)
        with open(os.path.join(skill, "scripts", "build.py"), "a", encoding="utf-8") as f:
            f.write("\n# edited during the run\n")
        r = self.run_in(skill, "done", self.run_dir, "locate")
        self.assertEqual(r.returncode, 3)
        self.assertIn("changed while this run was in progress", r.stdout + r.stderr)
        v = subprocess.run([sys.executable, os.path.join(skill, "scripts", "verify.py"), self.run_dir], capture_output=True, text=True, env=dict(os.environ))
        self.assertTrue(any("CHANGED while this run was in progress" in ln for ln in fails(v)), fails(v))

    def test_a13_a_changed_layout_or_rule_page_is_a_change_too(self):
        import wrlib as w_
        before = w_.program_fingerprint()
        self.assertEqual(before, w_.program_fingerprint())                       # stable between two calls
        skill = self.copy_skill()
        r = self.run_in(skill, "start", self.run_dir, *CLIENT)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        for rel in (("scripts", "layout.json"), ("steps.json",), ("references", "00-rules.md")):
            path = os.path.join(skill, *rel)
            orig = slurp(path)
            spit(path, orig + "\n ")
            r = self.run_in(skill, "done", self.run_dir, "locate")
            self.assertEqual(r.returncode, 3, "%s: %s%s" % (rel, r.stdout, r.stderr))
            spit(path, orig)


# ---------------------------------------------------------------------------------------------------------------- A4: the Teams hand-over is proven, not just written down
class TeamsHandover(Staged):
    STAGE = "pdf"

    def record(self, teams_run, skill_dir=None):
        self.ok("receipt", self.run_dir, "--set", "summary.invoked=fact-find-summary run on the saved PDF: Summary built and saved",
                "--set", "summary.abi_same=Section 8 shows Life Cover (WOL) ABI 3%, Childcare ABI 5%, Household needs ABI 5% and Dread Disease ABI 3%",
                "--set", "teams.run_folder=" + teams_run, "--set", "teams.skill_dir=" + (skill_dir or teams_driver.TEAMS_DIR),
                "--set", "teams.next_appointment_carried=Thursday 12/11/2026 at 16:00 (action for Sitamah)")

    def test_a4_a_teams_run_that_was_only_started_is_refused(self):
        tr = os.path.join(self.tmp, "teams-run")
        r = subprocess.run([sys.executable, teams_driver.TEAMS_RUN, "start", tr, "--type", "first", "--client", "Pat Samplecase", "--date", "05/11/2026"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.record(tr)
        r = self.refused("done", self.run_dir, "handoffs")
        self.assertIn("has not finished these steps", r.stdout)

    def test_a4_an_empty_folder_or_the_wrong_skill_folder_is_refused(self):
        tr = os.path.join(self.tmp, "teams-run")
        os.makedirs(tr)
        self.record(tr)
        r = self.refused("done", self.run_dir, "handoffs")
        self.assertIn("holds no run.json", r.stdout)
        self.record(tr, skill_dir=os.path.dirname(SCRIPTS))                       # this skill's own folder is not the Teams skill
        r = self.refused("done", self.run_dir, "handoffs")
        self.assertIn("is not the folder of client-teams-transcript-skill", r.stdout)

    def test_a4_a_teams_run_for_another_client_is_refused(self):
        tr = os.path.join(self.tmp, "teams-other")
        teams_driver.drive(tr, self.transcript, client=("Zed", "Samplecase"))
        self.record(tr)
        r = self.refused("done", self.run_dir, "handoffs")
        self.assertIn("is not a first-meeting run for", r.stdout)

    def test_a4_a_fully_driven_run_is_accepted_and_its_message_is_the_one_shown(self):
        tr = os.path.join(self.tmp, "teams-run")
        teams_driver.drive(tr, self.transcript)
        self.record(tr)
        self.ok("done", self.run_dir, "handoffs")
        msg = slurp(os.path.join(tr, "out", "teams_message.txt"))
        self.assertIn("Pat Samplecase", msg)
        self.assertIn("05/11/2026", msg)

    def test_a4_a_follow_up_appointment_the_teams_run_does_not_carry_is_refused(self):
        tr = os.path.join(self.tmp, "teams-run")
        teams_driver.drive(tr, self.transcript)
        c = jload(os.path.join(tr, "content.json"))
        c["next_appointment"]["agreed"] = False
        jdump(os.path.join(tr, "content.json"), c)
        self.record(tr)
        self.refused("done", self.run_dir, "handoffs")

    def test_a4_a_teams_run_whose_own_checker_fails_is_refused(self):
        tr = os.path.join(self.tmp, "teams-run")
        teams_driver.drive(tr, self.transcript)
        c = jload(os.path.join(tr, "content.json"))
        c["actions"][0]["text"] = "Sitamah to do something nobody said on the call"
        c["actions"][0]["src"] = [{"line": 1, "quote": "Meeting title: Fact Find"}]
        jdump(os.path.join(tr, "content.json"), c)
        self.record(tr)
        r = self.refused("done", self.run_dir, "handoffs")
        self.assertIn("Teams hand-over", r.stdout)


# ---------------------------------------------------------------------------------------------------------------- A14: scan reviews, dismissals
class ScanReview(Staged):
    STAGE = "pass2"

    def test_a14_one_review_cannot_dismiss_the_whole_call(self):
        sh("tx.py", "scan", self.run_dir, ok=True)
        r = self.refused("ledger", self.run_dir, "review", "--from", "1", "--to", "99999", "--reason", "plain talk")
        self.assertIn("at most 40 lines", r.stdout + r.stderr)
        self.refused("ledger", self.run_dir, "review", "--from", "1", "--to", "41", "--reason", "plain talk from the greeting to the diploma")

    def test_a14_the_same_reason_cannot_be_used_twice(self):
        sh("tx.py", "scan", self.run_dir, ok=True)
        self.ok("ledger", self.run_dir, "review", "--from", "1", "--to", "10", "--reason", "greeting and consent only, nothing decided")
        r = self.refused("ledger", self.run_dir, "review", "--from", "11", "--to", "20", "--reason", "Greeting and consent only, nothing decided")
        self.assertIn("already used", r.stdout + r.stderr)

    def test_a14_a_review_needs_a_real_reason_and_a_place(self):
        sh("tx.py", "scan", self.run_dir, ok=True)
        self.refused("ledger", self.run_dir, "review", "--line", "10", "--reason", "ok")
        self.refused("ledger", self.run_dir, "review", "--reason", "plain talk with no line at all")

    def test_a14_more_than_a_quarter_of_the_call_dismissed_is_put_in_front_of_paul(self):
        import verify
        led = self.load("ledger.json")
        led["scan_reviewed"] = [{"from": 1, "to": 40, "reason": "plain talk one"}, {"from": 41, "to": 80, "reason": "plain talk two"}]
        st = self.load("state.json")
        lines = verify.summary_lines(self.run_dir, st, led, {})
        self.assertTrue(any("MORE THAN A QUARTER OF THE CALL WAS DISMISSED" in ln for ln in lines), lines)
        self.assertTrue(any("scan dismissals" in ln for ln in lines))
        led["scan_reviewed"] = [{"from": 1, "to": 10, "reason": "plain talk one"}]
        lines = verify.summary_lines(self.run_dir, st, led, {})
        self.assertFalse(any("MORE THAN A QUARTER" in ln for ln in lines))

    def test_a14_a_pass_with_no_ledger_entry_at_all_does_not_close(self):
        st = self.load("state.json")
        # undo what the staged run recorded: no entries, every chunk acknowledged with the same boilerplate
        led = self.load("ledger.json")
        led["entries"] = []
        led["chunk_acks"] = [{"pass": 1, "chunk": n, "reason": "read this chunk and there is nothing here worth recording at all"} for n in range(1, len(st["chunks"]) + 1)]
        self.write("ledger.json", led)
        rj = self.load("run.json")
        rj["steps"]["pass1"]["state"] = "open"
        self.write("run.json", rj)
        r = self.refused("done", self.run_dir, "pass1")
        self.assertIn("ledger is empty", r.stdout)


# ---------------------------------------------------------------------------------------------------------------- A15: two spouses
class Spouses(Chat):
    def test_a15_the_joint_meeting_question_must_be_answered_before_the_content_step(self):
        self.through("crosscheck")
        r = self.refused("done", self.run_dir, "joint")
        self.assertIn("is this a joint meeting with a spouse", r.stdout)
        r = self.refused("done", self.run_dir, "content")
        self.assertIn("finish step 'joint' first", r.stdout + r.stderr)

    def test_a15_yes_needs_a_run_started_with_spouse_and_no_needs_one_without(self):
        self.through("crosscheck")
        r = self.refused("joint", self.run_dir, "--answer", "yes", "--evidence", "Pat and Robin were both on the call")
        self.assertIn("one run per spouse", r.stdout + r.stderr)
        self.refused("joint", self.run_dir, "--answer", "no", "--evidence", "short")                       # evidence needs words
        sp = os.path.join(self.tmp, "spouse-run")
        d2 = os.path.join(self.tmp, "run2")
        self.ok("start", d2, *CLIENT, "--spouse", "Robin Testcase", "--spouse-run", sp)
        r = self.refused("joint", d2, "--answer", "no", "--evidence", "only Pat spoke on this call, nobody else")
        self.assertIn("one spouse of a joint meeting", r.stdout + r.stderr)
        self.ok("joint", d2, "--answer", "yes", "--evidence", "Pat and Robin were both on the call")
        self.assertEqual(jload(os.path.join(d2, "run.json"))["joint"]["answer"], "yes")

    def test_a15_the_two_spouse_page_is_shown_where_it_matters(self):
        with open(os.path.join(os.path.dirname(SCRIPTS), "steps.json"), encoding="utf-8") as f:
            steps = {s["id"]: s for s in json.load(f)["steps"]}
        for step in ("locate", "joint", "handoffs"):
            self.assertIn("03-two-spouses.md", steps[step]["ref"], step)
        with open(os.path.join(os.path.dirname(SCRIPTS), "references", "03-two-spouses.md"), encoding="utf-8") as f:
            page = f.read()
        self.assertIn("attrib", page)
        self.assertIn("joint", page.lower())

    def test_a15_a_statement_in_a_spouse_run_needs_an_attrib_line(self):
        sp = os.path.join(self.tmp, "robin-run")
        self.ok("start", self.run_dir, *CLIENT, "--spouse", "Robin Testcase", "--spouse-run", sp)
        self.access("form", "device", "ok", "device_stage_files")
        self.ok("form", self.run_dir, self.form_path)
        sh("tx.py", "prep", self.transcript, self.run_dir, ok=True)
        self.ok("joint", self.run_dir, "--answer", "yes", "--evidence", "Pat and Robin were both on the call")
        note = {"id": "n1", "section": "next", "text": "Wants cover", "src": [{"line": self.L("Thursday the twelfth at four works"), "quote": "Thursday the twelfth at four works"}]}
        self.write("overlay.json", {"notes": [note]})
        self.ok("compose", self.run_dir)
        out = self.verify("--stage", "pre")
        self.assertTrue(any("attrib" in ln and "n1" in ln for ln in fails(out)), fails(out))
        note["attrib"] = "the sentence is about Pat's own appointment diary, not about Robin"
        self.write("overlay.json", {"notes": [note]})
        self.ok("compose", self.run_dir)
        out = self.verify("--stage", "pre")
        self.assertFalse(any("attrib" in ln and "n1" in ln for ln in fails(out)), fails(out))

    def test_a15_the_answer_must_match_how_the_run_was_started(self):
        self.through("joint")
        rj = self.load("run.json")
        rj["joint"]["answer"] = "yes"                                    # a single-client run claiming a joint meeting
        self.write("run.json", rj)
        self.ok("compose", self.run_dir)
        out = self.verify("--stage", "pre")
        self.assertTrue(any("joint-meeting answer" in ln for ln in fails(out)), fails(out))

    def test_a15_the_other_spouses_own_values_in_this_document_are_found(self):
        import verify
        mine = {"sections": [{"id": "occupation", "blocks": [{"rows": [{"id": "n1", "label": "Note", "bullets": ["Works at Fakeschool as a Teacher, earns R 30 000.00"], "src": [{"line": 5, "quote": "x"}], "status": "filled", "flags": []}]}]}], "closing": {"rows": []}}
        other = {"sections": [{"id": "occupation", "blocks": [{"rows": [{"id": "employer", "label": "Employer", "bullets": ["Fakeschool"], "src": [{"form": "employer"}], "status": "confirmed", "flags": []},
                                                                         {"id": "gross", "label": "Gross", "bullets": ["R 30 000.00"], "src": [{"form": "gross"}], "status": "confirmed", "flags": []}]}]}],
                 "closing": {"rows": []}}
        found = verify.spouse_values_overlap(mine, other)
        self.assertTrue(found, "the other spouse's employer and income were not found in what was written for this spouse")


# ---------------------------------------------------------------------------------------------------------------- M1, M3, M7, M10, A16
class NoFonts(Staged):
    STAGE = "content"

    def build_and_check_without_fonts(self):
        """Build and check in ONE process in which no TTF font exists at all (a bare sandbox), as the reviewer did."""
        code = ("import sys; sys.path.insert(0, %r); import build, verify; build.FALLBACKS=[]; sys.argv=['build.py', %r]; build.main();"
                "R,st,led,c = verify.run_checks(%r,'built'); verify.report(R,st,led,c,'built',%r)") % (SCRIPTS, self.run_dir, self.run_dir, self.run_dir)
        return subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)

    def test_m1_a_pdf_in_the_plain_helvetica_fallback_is_a_warning_not_a_failure_and_says_so(self):
        r = self.build_and_check_without_fonts()
        self.assertIn("FONT USED: Helvetica", r.stdout)
        out = r.stdout
        font_fails = [ln for ln in out.splitlines() if "[FAIL" in ln and ("font" in ln.lower() or "PDF text" in ln)]
        self.assertEqual(font_fails, [], font_fails)
        self.assertTrue(any("[WARN" in ln and "Helvetica" in ln for ln in out.splitlines()), out[-1500:])


class Money(Chat):
    def test_m3_an_amount_written_two_ways_is_never_guessed(self):
        import wrlib as w_
        from decimal import Decimal
        self.assertEqual(w_.parse_money("R 24 000.00"), Decimal("24000.00"))
        self.assertEqual(w_.parse_money("R24,000.00"), Decimal("24000.00"))
        self.assertEqual(w_.parse_money("R 1.234,50"), Decimal("1234.50"))
        self.assertEqual(w_.parse_money("1234,50"), Decimal("1234.50"))
        self.assertEqual(w_.parse_money("2,000"), Decimal("2000.00"))
        self.assertIsNone(w_.parse_money("R 2.000"))                # two rand or two thousand? never guessed
        self.assertIsNone(w_.parse_money("R 1.2345"))
        self.assertIsNone(w_.parse_money("twelve"))
        self.assertIsNone(w_.parse_money(""))


class LeadSearch(Staged):
    STAGE = "scan"

    def test_m7_the_outlook_search_cannot_be_called_unavailable_before_all_three_routes_failed(self):
        r = self.refused("lead", self.run_dir, "--folder-result", "unavailable", "--mailbox-result", "unavailable")
        self.assertIn("all three routes", r.stdout + r.stderr)
        self.access("lead", "m365", "fail", "outlook_email_search", "the connector returned an error")
        r = self.refused("lead", self.run_dir, "--folder-result", "unavailable", "--mailbox-result", "unavailable")
        self.assertIn("Not yet logged", r.stdout + r.stderr)

    def test_m7_when_all_three_failed_the_chat_must_stop_and_ask_paul_and_his_words_are_recorded(self):
        for route in ("device", "m365", "zapier"):
            self.access("lead", route, "fail", "tool_" + route, "the search returned an error")
        r = self.refused("lead", self.run_dir, "--folder-result", "unavailable", "--mailbox-result", "unavailable")
        self.assertIn("ask Paul", r.stdout + r.stderr)
        self.assertFalse(os.path.exists(self.p("lead.json")) and self.load("lead.json").get("searched"))
        self.ok("ask", self.run_dir, "--need", "lead", "--kind", "knowledge", "--question",
                "The Outlook search for a D&R Marketing email for this client could not be made on any route. Carry on without it, or wait?", "--searched", "Outlook on the drive, Microsoft 365 and Zapier")
        self.refused("lead", self.run_dir, "--folder-result", "unavailable", "--mailbox-result", "unavailable")          # asked, but Paul has not answered
        self.ok("answer", self.run_dir, "--need", "lead", "--said", "Carry on without it, I will look in Outlook myself")
        self.ok("lead", self.run_dir, "--folder-result", "unavailable", "--mailbox-result", "unavailable")
        self.assertTrue(self.load("lead.json")["unavailable"])
        self.ok("done", self.run_dir, "contact")
        self.ok("compose", self.run_dir)
        c = self.load("content.json")
        self.assertTrue(any("could NOT be made" in g for g in c["glance"]), c["glance"])

    def test_m6_requested_needs_a_recorded_lead_search(self):
        self.ok("compose", self.run_dir)
        r = self.refused("claim", self.run_dir, "--key", "debts.0.cl", "--as", "Requested", "--searched", "searched the form, the call, the Overview and Outlook")
        self.assertIn("Requested", r.stdout + r.stderr)


class Century(Chat):
    def test_m10_an_id_whose_year_could_be_either_century_is_put_on_the_glance_list(self):
        import compose
        import ffform
        f = HH.pat_form()
        f["f"]["idno"] = {"v": HH.make_id("100101", 5009), "st": "confirmed"}          # 01/01/10: 2010 or 1910
        f["f"]["dob"] = {"v": "", "st": "empty"}
        f["f"]["age"] = {"v": "", "st": "empty"}
        p_ = os.path.join(self.tmp, "century.json")
        jdump(p_, f)
        fr = ffform.read_form(p_)
        c = compose.compose({"layout": compose.w.layout(), "run": {"client": {"first": "Pat", "surname": "Samplecase"}, "date": "05/11/2026"}, "form": fr, "overlay": {}, "cross": [], "claims": {}, "lead": {}})
        self.assertTrue(any("check the century" in g for g in c["glance"]), c["glance"])
        f["f"]["idno"] = {"v": HH.PAT_ID, "st": "confirmed"}
        jdump(p_, f)
        c = compose.compose({"layout": compose.w.layout(), "run": {"client": {"first": "Pat", "surname": "Samplecase"}, "date": "05/11/2026"}, "form": ffform.read_form(p_), "overlay": {}, "cross": [], "claims": {}, "lead": {}})
        self.assertFalse(any("check the century" in g for g in c["glance"]), c["glance"])


class Wording(Staged):
    """A16: the printout says what the program proved and what is only attested, and does not claim more."""
    STAGE = "handoffs"

    def test_a16_the_printout_separates_proven_from_attested_and_names_the_text_only_rules(self):
        out = self.s_final().stdout
        self.assertIn("RESULT: PASS", out)
        self.assertIn("PROVEN BY THE PROGRAM", out)
        self.assertIn("ONLY ATTESTED BY CLAUDE", out)
        proven = out[out.index("PROVEN BY THE PROGRAM"):out.index("ONLY ATTESTED BY CLAUDE")]
        for claim in ("Paul said yes", "Planner page was published", "visual check", "Fact Find Summary hand-over"):
            self.assertNotIn(claim, proven)
        attested = out[out.index("ONLY ATTESTED BY CLAUDE"):]
        for what in ("Paul's own words", "the visual check", "the independent re-check", "Planner page was published", "text in a document that has no recorded copy", "every rule that is only text"):
            self.assertIn(what, attested)
        self.assertIn("a '?' is not a value", out)                              # the ACI '?' preset line no longer calls it a value
