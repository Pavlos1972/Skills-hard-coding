"""Unit tests for the form reader, the composer, the money and ID helpers, the joined-transcript reader and the font report. Invented data."""
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal

from support import HERE, SCRIPTS, H, drv, jdump, jload, sh, slurp, spit

import build  # noqa: E402
import compose  # noqa: E402
import ffform  # noqa: E402
import tx  # noqa: E402
import wrlib as w  # noqa: E402

REAL_KEYS = """consent date meet ref fname sname dob age idtype idno gender nat nat_other tax cell work home pemail wemail edu edu_notes profile n_info
employed employer co_does bizowner occ ft years biz_name biz_struct biz_struct_other biz_does biz_partners biz_pct biz_loans biz_assur d_desk d_supo d_trav d_sups d_light d_mod d_heavy d_tot d_desc n_occ
gross dnet net exp disp marital marr_date sp_name sp_tel sp_occ n_income has_debts n_debts has_kids n_kids
has_risk joint ps_risk ps_risk_ot has_group ps_grp ps_grp_ot n_cover has_ra ps_ra ps_ra_ot has_pp ps_pp ps_pp_ot n_retire has_inv ps_inv ps_inv_ot n_inv
ma ma_prov ma_plan ma_broker n_ma gap gap_prov gap_broker n_gap will will_up will_where will_where_other will_broker will_date n_will sti sti_broker sti_car sti_house sti_struct sti_personal sti_biz sti_biz_spend n_sti
smoker h_gen h_dia h_chol h_bp h_bmi h_oth h_notes pr_life pr_life_cm bf_fna_req bf_fna_type fna_req fna_type fna_ins bf_sf_req bf_sf_type sf_req sf_type sf_ins
lc_sa lc_term lc_termv lc_aci lc_aciv lc_abiv lc_cmt pd_sa pd_term pd_termv pd_aci pd_aciv pd_abiv pd_cmt ips_age ips_amt ips_wait ips_aci ips_aciv ips_abiv ips_cmt
dds_cover dds_term dds_termv dds_aci dds_aciv dds_abiv dds_cmt pref_spend pr_ra pr_ra_cm pr_rgar pr_rgar_cm rgar_req ret_age ret_net pr_inv pr_inv_cm pr_egar pr_egar_cm egar_req
pr_med pr_med_cm ref_med pr_will pr_will_cm ref_will pr_st pr_st_cm ref_sti bs_req bs_ins bs_value bs_basis bs_own cl_req cl_lender cl_bal cl_life km_req km_name km_role km_amt km_basis n_prio
lc_hh lc_cc lc_dr lc_need lc_f_aci lc_f_aciv lc_wol lc_ccabi pd_f_aci pd_f_aciv pd_ccabi ip_age ip_amt ip_hh ip_wait ip_aci ip_aciv ip_abiv ip_cmt
dd_cover dd_term dd_termv dd_aci dd_aciv dd_abiv dd_cmt n_calc loa next_appt next_day next_time""".split()
REAL_LISTS = {"risk": {"prov", "spend", "broker", "notes"}, "ret_ra": {"prov", "status", "val", "contrib", "broker"}, "ret_pp": {"type", "prov", "val", "contrib", "broker"},
              "inv": {"type", "prov", "val", "prem", "broker"}, "debts": {"type", "prov", "desc", "owner", "payer", "term", "inst", "bal", "asset", "cl", "surety", "notes"},
              "kids": {"name", "sname", "gender", "dob", "age", "stage", "cost"}, "bfred": {"req", "type", "amt"}, "raq": {"req"}, "invq": {"purpose"}}


def form_with(**fields):
    f = H.pat_form()
    for k, v in fields.items():
        f["f"][k] = {"v": v, "st": "confirmed"}
    return f


def read(form):
    d = tempfile.mkdtemp(prefix="wrunit-")
    p = os.path.join(d, "f.json")
    jdump(p, form)
    try:
        return ffform.read_form(p)
    finally:
        shutil.rmtree(d, True)


def content_for(form, **inp):
    base = {"layout": w.layout(), "run": {"client": {"first": "Pat", "surname": "Samplecase"}, "date": "05/11/2026"}, "form": read(form), "overlay": {}, "cross": [], "claims": {}, "lead": {}}
    base.update(inp)
    return compose.compose(base)


def rows_of(c):
    return {r["id"]: r for s in c["sections"] for b in s["blocks"] for r in b["rows"]} | {r["id"]: r for r in c["closing"]["rows"]}


class Layout(unittest.TestCase):
    def test_every_real_key_of_the_form_has_a_place_exactly_once(self):
        lay = w.layout()
        keys, lists, notes = ffform.layout_keys(lay)
        self.assertEqual(set(REAL_KEYS) - keys, set())
        seen = []
        for sec in lay["sections"]:
            for g in sec["groups"]:
                seen += [r["key"] for r in g.get("rows", []) if r.get("key")]
        seen += [r["key"] for r in lay["closing"]["rows"]]
        self.assertEqual([k for k in set(seen) if seen.count(k) > 1], [])
        for name, cols in REAL_LISTS.items():
            self.assertIn(name, lists)
            self.assertEqual(lists[name] - cols, set())
        for name in ("grp", "bizpol", "shares", "redq"):
            self.assertIsNone(lists[name])             # columns never seen: any column is printed

    def test_fixed_eleven_sections_then_the_closing_block_in_order(self):
        lay = w.layout()
        self.assertEqual([s["title"] for s in lay["sections"]], ["Client Info", "Occupation", "Income & Household", "Existing Cover & Retirement", "Investments",
                                                                  "Medical, Will & Short-Term", "Debts", "Children", "Health", "Advisor Actions", "Risk Calculation"])
        self.assertEqual(lay["closing"]["title"], "Next Steps & Next Meeting")
        self.assertEqual(lay["style"]["navy"], "1F3A5F")
        self.assertEqual(lay["style"]["label_bg"], "EAF1F8")
        self.assertEqual(lay["style"]["size"], 12)

    def test_the_form_is_never_edited_the_ignored_parts_are_named(self):
        lay = w.layout()
        self.assertEqual(sorted(lay["ignored"]["top"]), ["claude", "openai", "pa", "sum", "unplaced"])
        self.assertEqual(lay["ignored"]["fields"], ["pa_actions"])


class FormReader(unittest.TestCase):
    def test_trailing_space_is_trimmed_and_statuses_counted(self):
        fr = read(H.pat_form())
        self.assertEqual(fr["fields"]["fname"]["v"], "Pat")
        self.assertEqual(fr["client"], {"first": "Pat", "surname": "Samplecase"})
        self.assertEqual(fr["statuses"], {"confirmed": 73, "preset": 10})
        self.assertIn("lc_wol", fr["presets"])
        self.assertFalse(fr["fields"]["dob"]["populated"])

    def test_the_parking_list_summaries_actions_and_counters_are_not_read(self):
        fr = read(H.pat_form())
        self.assertNotIn("pa_actions", fr["fields"])
        self.assertNotIn("unplaced", json.dumps(fr["fields"]))
        self.assertEqual(sorted(k for k in fr["ignored"] if not k.startswith("f.")), ["claude", "openai", "pa", "sum", "unplaced"])
        self.assertIn("ignored, not read", fr["ignored"]["unplaced"])
        self.assertNotIn("old policy", json.dumps(fr))

    def test_older_statuses_are_accepted_and_listed(self):
        f = H.pat_form()
        f["f"]["occ"]["st"] = "heard"
        f["f"]["ft"]["st"] = "verify"
        fr = read(f)
        self.assertEqual(sorted(fr["other_statuses"]), ["ft", "occ"])
        c = content_for(f)
        self.assertIn("Operations manager", json.dumps(c))                 # heard and verify values are used like the others
        self.assertTrue(any("heard or verify" in g for g in c["glance"]))

    def test_an_empty_status_with_a_value_is_used_and_noticed(self):
        f = H.pat_form()
        f["f"]["occ"]["st"] = "empty"
        fr = read(f)
        self.assertTrue(fr["fields"]["occ"]["populated"])
        self.assertTrue(any("marked empty but holds a value" in o for o in fr["odd"]))

    def test_schema_and_app_are_checked(self):
        d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, d, True)
        p = os.path.join(d, "x.json")
        f = H.pat_form()
        f["schema"] = "2.0"
        jdump(p, f)
        with self.assertRaises(ffform.FormError) as e:
            ffform.read_form(p)
        self.assertIn("schema '2.0'", str(e.exception))
        self.assertEqual(len(str(e.exception).splitlines()), 1)
        f["schema"] = 3.0                              # a number, not the text "3.0": still schema 3.0
        jdump(p, f)
        self.assertEqual(ffform.read_form(p)["schema"], "3.0")

    def test_company_look_up_rules(self):
        cl = ffform.check_lookup
        self.assertEqual(cl("", "empty")["verdict"], "empty")
        self.assertEqual(cl("Freight and logistics company serving retailers.", "confirmed")["verdict"], "clean")
        self.assertEqual(cl("That's Fakeco. Try Fakeco Freight once more.", "confirmed")["verdict"], "thrown_out")
        self.assertEqual(cl("I found no company with this name.", "confirmed")["verdict"], "thrown_out")
        self.assertEqual(cl("Did you mean Fakeco Freight?", "confirmed")["verdict"], "thrown_out")
        long = " ".join(["word"] * 45)
        r = cl(long, "confirmed")
        self.assertEqual(r["verdict"], "thrown_out")
        self.assertIn("45 words", r["reasons"][0])
        self.assertEqual(cl(" ".join(["word"] * 40), "confirmed")["verdict"], "clean")

    def test_a_chatter_look_up_is_replaced_from_the_call_or_shown_as_not_stated(self):
        c = content_for(H.pat_form())
        r = rows_of(c)["co_does"]
        self.assertEqual(r["bullets"], ["Not stated"])
        self.assertTrue(any("thrown out" in g for g in c["glance"]))
        c = content_for(H.pat_form(), overlay={"lookup": {"id": "o1", "text": "Moves freight for retailers", "src": [{"line": 5, "quote": "we move freight for retailers"}]}})
        self.assertEqual(rows_of(c)["co_does"]["bullets"], ["Moves freight for retailers"])
        self.assertNotIn("Try Fakeco", json.dumps(c))

    def test_a_clean_look_up_nobody_confirmed_is_marked_and_paul_is_told(self):
        c = content_for(form_with(co_does="Freight and logistics company serving retailers"))
        self.assertEqual(rows_of(c)["co_does"]["bullets"], ["Freight and logistics company serving retailers", "(web look-up, not confirmed with the client)"])
        self.assertTrue(any("should say 'to verify', never 'confirmed'" in g for g in c["glance"]))
        c = content_for(form_with(co_does="Freight and logistics company serving retailers"),
                        overlay={"lookup": {"id": "o1", "client_confirmed": True, "src": [{"line": 5, "quote": "we move freight for retailers"}]}})
        self.assertEqual(rows_of(c)["co_does"]["bullets"], ["Freight and logistics company serving retailers"])

    def test_years_that_holds_a_year_is_worked_out(self):
        self.assertEqual(ffform.years_from("2015", 2026), (11, 2015))
        self.assertIsNone(ffform.years_from("11", 2026))
        self.assertIsNone(ffform.years_from("2031", 2026))            # a year in the future is not a start year
        self.assertEqual(rows_of(content_for(H.pat_form()))["years"]["bullets"], ["11 years (since 2015)"])
        self.assertEqual(rows_of(content_for(form_with(years="6")))["years"]["bullets"], ["6"])

    def test_id_number_gives_date_of_birth_and_gender(self):
        m = dt.date(2026, 11, 5)
        a = ffform.id_facts(H.PAT_ID, m)
        self.assertEqual((a["dob"], a["gender"], a["ok"], a["problems"]), (dt.date(1990, 1, 1), "Male", True, []))
        b = ffform.id_facts(H.ROBIN_ID, m)
        self.assertEqual((b["dob"], b["gender"]), (dt.date(1992, 2, 2), "Female"))
        self.assertEqual(ffform.id_facts(H.make_id("920202", 4999), m)["gender"], "Female")     # below 5000 is female
        self.assertEqual(ffform.id_facts(H.make_id("920202", 5000), m)["gender"], "Male")
        self.assertEqual(ffform.id_facts(H.make_id("051231", 1234), m)["dob"], dt.date(2005, 12, 31))
        self.assertEqual(ffform.id_facts(H.make_id("301231", 1234), m)["dob"], dt.date(1930, 12, 31))     # not in the future
        self.assertFalse(ffform.id_facts("12345", m)["ok"])
        self.assertFalse(ffform.id_facts(H.make_id("901301", 5009), m)["ok"])                   # month 13
        bad = H.PAT_ID[:-1] + str((int(H.PAT_ID[-1]) + 1) % 10)
        self.assertIn("check digit", ffform.id_facts(bad, m)["problems"][0])

    def test_dob_and_gender_are_derived_only_when_the_form_has_none_and_a_difference_is_flagged(self):
        c = content_for(H.pat_form())
        r = rows_of(c)
        self.assertEqual(r["dob"]["bullets"], ["01/01/1990 (worked out from the ID number)"])
        self.assertEqual(r["gender"]["bullets"], ["Male (worked out from the ID number)"])
        self.assertEqual(r["age"]["bullets"], ["36 (worked out from the date of birth)"])
        c = content_for(form_with(dob="02/01/1990", gender="Female"))
        r = rows_of(c)
        self.assertEqual(r["dob"]["bullets"], ["02/01/1990"])
        self.assertIn("the form says 02/01/1990; the ID number gives 01/01/1990", r["dob"]["flags"][0]["text"])
        self.assertIn("the form says Female; the ID number gives Male", r["gender"]["flags"][0]["text"])

    def test_populated_unknown_keys_and_columns_are_found(self):
        f = H.pat_form()
        f["f"]["zz"] = {"v": "new", "st": "confirmed"}
        f["l"]["shares"] = [H.row(co="Fakeshares", units="10")]
        f["l"]["debts"][0]["d"]["extra"] = "x"
        fr = read(f)
        self.assertEqual(fr["unknown_fields"], ["zz"])
        self.assertEqual(fr["unknown_cols"], {"debts": ["extra"]})
        self.assertNotIn("shares", fr["unknown_lists"])           # a generic list prints whatever columns it has


class Money(unittest.TestCase):
    def test_amounts_parse_to_the_cent(self):
        for text, want in (("R 24 000.00", "24000.00"), ("R24,000.00", "24000.00"), ("24000", "24000.00"), ("R 1 234,50", "1234.50"), ("R 0.10", "0.10"), ("R 1 172.79", "1172.79")):
            self.assertEqual(w.parse_money(text), Decimal(want), text)
        for text in ("", "N/A", "Not discussed", "R", "12 years"):
            self.assertIsNone(w.parse_money(text), text)

    def test_amounts_are_written_in_the_forms_own_style(self):
        self.assertEqual(w.fmt_money(Decimal("24000")), "R 24 000.00")
        self.assertEqual(w.fmt_money(Decimal("1450000.5")), "R 1 450 000.50")
        self.assertEqual(w.fmt_money(Decimal("0")), "R 0.00")
        self.assertEqual(w.fmt_money(Decimal("-12.3")), "-R 12.30")

    def test_totals_add_to_the_cent_not_in_floating_point(self):
        c = content_for(H.pat_form())
        r = rows_of(c)
        self.assertEqual(r["total.debts_monthly"]["bullets"], ["R 19 000.00"])
        self.assertEqual(r["total.debts_liabilities"]["bullets"], ["R 1 630 000.00"])
        self.assertEqual(r["total.kids_total"]["bullets"], ["R 5 500.00"])
        f = H.pat_form()
        f["l"]["debts"][0]["d"]["inst"] = "R 0.10"
        f["l"]["debts"][1]["d"]["inst"] = "R 0.20"
        self.assertEqual(rows_of(content_for(f))["total.debts_monthly"]["bullets"], ["R 0.30"])

    def test_a_debt_with_no_amount_is_flagged_never_left_out_quietly(self):
        f = H.pat_form()
        f["l"]["debts"][1]["d"]["inst"] = ""
        r = rows_of(content_for(f, claims={"debts.1.inst": {"as": "Requested", "terms": ["x"], "searched": "form, call, Overview, documents and Outlook"}}))
        self.assertTrue(any("have no amount yet" in x["text"] for x in r["total.debts_monthly"]["flags"]))

    def test_the_forms_own_totals_are_recomputed_and_a_difference_is_flagged_with_both(self):
        f = form_with(disp="R 13 000.00", d_tot="90%")
        r = rows_of(content_for(f))
        self.assertIn("the form says R 13 000.00; disposable income = take-home net income minus monthly expenses works out to R 12 500.00", r["disp"]["flags"][0]["text"])
        self.assertIn("the form says 90%; the percentages above add up to 100%", r["d_tot"]["flags"][0]["text"])
        self.assertEqual(r["d_tot"]["bullets"], ["100%"])


class StandingValues(unittest.TestCase):
    def test_abis_are_the_standing_values_and_a_different_file_value_is_overwritten_in_one_line(self):
        r = rows_of(content_for(form_with(dd_abiv="5%", dds_abiv="5%")))
        self.assertEqual(r["lc_wol"]["bullets"], ["3%"])
        self.assertIn("The form has 5%; the standing value 3% is written.", r["lc_wol"]["flags"][0]["text"])
        self.assertEqual(r["lc_ccabi"]["bullets"], ["5%"])
        self.assertEqual(r["pd_ccabi"]["bullets"], ["5%"])
        self.assertEqual(r["dd_abiv"]["bullets"], ["3%"])               # Dread Disease ABI is 3% always, both keys
        self.assertEqual(r["dds_abiv"]["bullets"], ["3%"])
        self.assertIn("the standing value 3% is written", r["dd_abiv"]["flags"][0]["text"])
        r = rows_of(content_for(H.pat_form()))                         # the preset 3% needs no note
        self.assertEqual(r["dd_abiv"]["bullets"], ["3%"])
        self.assertEqual(r["dd_abiv"]["flags"], [])

    def test_pd_fractured_has_household_needs_abi_and_no_life_cover_wol_line(self):
        c = content_for(H.pat_form())
        blk = next(b for s in c["sections"] for b in s["blocks"] if b["sub"] == "Permanent disability: fractured cover")
        labels = [r["label"] for r in blk["rows"]]
        self.assertIn("Household needs ABI", labels)
        self.assertNotIn("Life Cover (WOL) ABI", labels)
        row = next(r for r in blk["rows"] if r["label"] == "Household needs ABI")
        self.assertEqual(row["bullets"], ["5%"])
        self.assertIn("Added by the standing rule", row["flags"][0]["text"])

    def test_the_standing_abis_do_not_set_the_other_abis_or_any_aci(self):
        r = rows_of(content_for(H.pat_form()))
        self.assertEqual(r["ip_abiv"]["bullets"], ["5%"])             # as in the form (preset), untouched by the rule
        self.assertEqual(r["lc_abiv"]["bullets"], [compose.PENDING])    # empty: Pending, not a standing value
        self.assertEqual(r["pd_abiv"]["bullets"], [compose.PENDING])
        self.assertNotIn("3%", r["lc_abiv"]["bullets"])

    def test_a_question_mark_in_an_aci_field_is_not_a_value(self):
        r = rows_of(content_for(H.pat_form()))
        self.assertEqual(r["lc_f_aciv"]["bullets"], ["Pending – FNA"])
        self.assertEqual(r["lc_aci"]["bullets"], ["Pending – FNA"])         # empty ACI field too
        r = rows_of(content_for(form_with(lc_f_aciv="5%")))
        self.assertEqual(r["lc_f_aciv"]["bullets"], ["5%"])

    def test_paul_can_state_another_abi_and_it_is_noted(self):
        ov = {"abi_override": [{"id": "o1", "key": "dd_abiv", "value": "5%", "paul_said": "Use 5% for this client"}]}
        r = rows_of(content_for(H.pat_form(), overlay=ov))
        self.assertEqual(r["dd_abiv"]["bullets"], ["5%"])
        self.assertIn("Paul stated this ABI", r["dd_abiv"]["flags"][0]["text"])

    def test_dread_disease_cover_defaults_to_500000_unless_the_form_has_another(self):
        r = rows_of(content_for(H.pat_form()))
        self.assertEqual(r["dd_cover"]["bullets"], ["R 500 000.00"])
        self.assertEqual(r["dds_cover"]["bullets"], ["R 500 000.00"])
        r = rows_of(content_for(form_with(dd_cover="R 750 000.00")))
        self.assertEqual(r["dd_cover"]["bullets"], ["R 750 000.00"])
        self.assertIn("not the standing default of R 500 000.00", r["dd_cover"]["flags"][0]["text"])


class Gates(unittest.TestCase):
    def test_answers_of_no_make_the_dependent_fields_not_applicable(self):
        f = form_with(ma="No", gap="No", sti="No")
        for k in ("ma_prov", "ma_plan", "ma_broker"):
            f["f"][k] = {"v": "", "st": "empty"}
        r = rows_of(content_for(f))
        self.assertEqual(r["ma_prov"]["bullets"], ["N/A"])
        self.assertEqual(r["gap_prov"]["bullets"], ["N/A"])
        self.assertEqual(r["sti_car"]["bullets"], ["N/A"])
        self.assertEqual(r["ma"]["bullets"], ["No"])

    def test_a_single_person_has_no_spouse_fields(self):
        f = form_with(marital="Single")
        for k in ("marr_date", "sp_name", "sp_occ"):
            f["f"][k] = {"v": "", "st": "empty"}
        r = rows_of(content_for(f))
        self.assertEqual(r["sp_name"]["bullets"], ["N/A"])

    def test_one_fact_per_line(self):
        self.assertEqual(compose.facts("Runs the depot teams. Reports to the director."), ["Runs the depot teams.", "Reports to the director."])
        self.assertEqual(compose.facts("one\n• two; three"), ["one", "two", "three"])
        self.assertEqual(compose.facts("Pays R 24 000.00 a month"), ["Pays R 24 000.00 a month"])
        self.assertEqual(compose.facts("Mr. Smith is the broker"), ["Mr. Smith is the broker"])
        self.assertEqual(rows_of(content_for(H.pat_form()))["d_desc"]["bullets"], ["Runs the depot teams.", "Reports to the director."])

    def test_a_referral_comes_from_the_lead_search_first(self):
        lead = {"searched": [{"where": "x", "result": "found"}], "found": True, "received": "01/11/2026", "ref": "Lead email", "quote": "Appointment from D & R Marketing"}
        r = rows_of(content_for(H.pat_form(), lead=lead))
        self.assertEqual(r["ref"]["bullets"], ["D&R Marketing lead - 01/11/2026"])
        self.assertIn("the lead source is D&R Marketing", r["ref"]["flags"][0]["text"])
        r = rows_of(content_for(H.pat_form(), lead={"searched": [{"where": "x", "result": "none"}], "found": False}))
        self.assertEqual(r["ref"]["bullets"], ["Current client"])
        f = form_with(ref="")
        r = rows_of(content_for(f, lead={"searched": [{"where": "x", "result": "none"}], "found": False}))
        self.assertEqual(r["ref"]["bullets"], ["Referral - referrer not stated (please confirm)"])


class JoinedTranscripts(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="wrjoin-")
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.run_dir = os.path.join(self.tmp, "run")
        os.makedirs(self.run_dir)
        jdump(os.path.join(self.run_dir, "run.json"), {"client": {"first": "Pat", "surname": "Samplecase"}, "date": "05/11/2026", "steps": {}})
        self.a = os.path.join(self.tmp, "a.txt")
        self.b = os.path.join(self.tmp, "b.txt")
        spit(self.a, "Duration: 2m 0s\n\n0:00:05 Paul Kafentzis\nLet us start with your income.\n\n0:00:30 Pat Samplecase\nI earn about forty five thousand rand.\n\n0:02:00 Paul Kafentzis\nThe call dropped, one moment\n")
        spit(self.b, "Duration: 1m 0s\n\n0:00:03 Paul Kafentzis\nSorry, you said about forty five thousand rand.\n\n0:00:50 Pat Samplecase\nYes.\n\n0:01:00 Paul Kafentzis stopped transcription\n")

    def test_two_transcripts_are_joined_checked_part_by_part_and_need_a_continuity_note(self):
        r = drv("join", self.run_dir, self.a, self.b)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("CONTINUITY CHECK 1/2", r.stdout)
        self.assertIn("===== TRANSCRIPT 1 OF 2: a.txt =====", slurp(os.path.join(self.run_dir, "transcript_joined.txt")))
        r = sh("tx.py", "prep", os.path.join(self.run_dir, "transcript_joined.txt"), self.run_dir)
        self.assertEqual(r.returncode, 0, r.stdout)
        st = jload(os.path.join(self.run_dir, "state.json"))
        self.assertEqual(len(st["parts"]), 2)
        self.assertEqual(st["stated_duration"], "0:03:00")
        self.assertEqual(st["last_ts"], "0:01:00")
        # no continuity note yet: the checker fails
        import verify
        R = verify.Results()
        verify.check_reading(self.run_dir, st, R)
        self.assertTrue(any("continuity between 1/2 was not checked" in m for l, _, m in R.rows if l == "FAIL"))
        self.assertNotEqual(drv("continuity", self.run_dir, "--between", "1,3", "--result", "ok", "--detail", "x" * 30).returncode, 0)
        self.assertNotEqual(drv("continuity", self.run_dir, "--between", "1,2", "--result", "ok", "--detail", "short").returncode, 0)
        self.assertEqual(drv("continuity", self.run_dir, "--between", "1,2", "--result", "ok", "--detail", "part 2 opens by repeating the income figure from the end of part 1").returncode, 0)
        R = verify.Results()
        verify.check_reading(self.run_dir, st, R)
        self.assertFalse([m for l, _, m in R.rows if l == "FAIL" and "continuity" in m])

    def test_a_truncated_part_is_caught_on_its_own(self):
        spit(self.b, "Duration: 10m 0s\n\n0:00:03 Paul Kafentzis\nSorry.\n\n0:01:00 Paul Kafentzis stopped transcription\n")
        drv("join", self.run_dir, self.a, self.b)
        r = sh("tx.py", "prep", os.path.join(self.run_dir, "transcript_joined.txt"), self.run_dir)
        self.assertEqual(r.returncode, 2)
        self.assertIn("part 2: INCOMPLETE: stated duration 0:10:00", r.stdout)

    def test_a_single_transcript_behaves_as_before(self):
        r = sh("tx.py", "prep", self.b, self.run_dir)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertEqual(jload(os.path.join(self.run_dir, "state.json"))["parts"], [[1, 9]])

    def test_join_needs_two_files(self):
        self.assertNotEqual(drv("join", self.run_dir, self.a).returncode, 0)


class FontAndLook(unittest.TestCase):
    def test_a_font_called_aptos_that_is_not_aptos_is_never_reported_as_aptos(self):
        d = tempfile.mkdtemp(prefix="wrfont-")
        self.addCleanup(shutil.rmtree, d, True)
        src = "/usr/share/fonts/truetype/crosextra"
        if not os.path.exists(os.path.join(src, "Carlito-Regular.ttf")):
            self.skipTest("no substitute font on this computer")
        for style, name in (("Regular", "Aptos.ttf"), ("Bold", "Aptos-Bold.ttf"), ("Italic", "Aptos-Italic.ttf"), ("BoldItalic", "Aptos-BoldItalic.ttf")):
            shutil.copy(os.path.join(src, "Carlito-%s.ttf" % style), os.path.join(d, name))
        rec = build.pick_font([d])
        self.assertEqual(rec["family"], "Aptos")                         # found by its file name ...
        rec = build.register(rec)
        self.assertFalse(rec["aptos"])                                   # ... but its real name inside is Carlito, so it is reported as a substitute
        self.assertTrue(rec["substitute"])
        self.assertIn("Carlito-Regular", rec["ps_names"])

    def test_the_aptos_test_is_on_the_real_names_inside_the_font(self):
        self.assertTrue(build.is_aptos(["Aptos", "Aptos-Bold", "Aptos-Italic"]))
        self.assertFalse(build.is_aptos(["Aptos", "Carlito-Bold"]))
        self.assertFalse(build.is_aptos([]))

    def test_the_substitute_is_named_when_aptos_is_missing(self):
        rec = build.register(build.pick_font([]))
        if rec["family"] != "Aptos":
            self.assertFalse(rec["aptos"])
            self.assertIn(rec["family"], ("Carlito", "Liberation Sans", "DejaVu Sans", "Helvetica"))

    def test_no_forced_page_break_anywhere_in_the_builder(self):
        src = slurp(os.path.join(SCRIPTS, "build.py"))
        self.assertIsNone(re.search(r"(?<!Cond)PageBreak\(", src))
        self.assertNotIn("showPage", src)
        self.assertNotIn("pageNumber", src.replace("page number", ""))

    def test_the_driver_self_test_passes_and_names_the_font(self):
        r = drv("preflight")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("SELF-TEST", r.stdout)
        self.assertIn("Font:", r.stdout)

    def test_every_script_compiles(self):
        for f in sorted(os.listdir(SCRIPTS)):
            if f.endswith(".py"):
                r = subprocess.run([sys.executable, "-m", "py_compile", os.path.join(SCRIPTS, f)], capture_output=True, text=True)
                self.assertEqual(r.returncode, 0, f + r.stderr)

    def test_no_real_client_data_style_content_in_the_scripts(self):
        for f in sorted(os.listdir(SCRIPTS)):
            if f.endswith((".py", ".json")):
                text = slurp(os.path.join(SCRIPTS, f))
                self.assertIsNone(re.search(r"(?<!\d)\d{13}(?!\d)", text), f)
                self.assertNotIn("@gmail", text.lower())


if __name__ == "__main__":
    unittest.main()
