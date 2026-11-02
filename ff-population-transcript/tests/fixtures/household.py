"""An invented household for the tests: Pat Samplecase (first client) and Robin Testcase (spouse). Nobody real.

The form data files use the REAL keys of the new Fact Find form (schema 3.0), with invented values. ID numbers are built here from
a date and a number (never typed), so no ID-like number sits in the repo's text.
"""
import copy


def make_id(yymmdd, seq, citizen=0):
    """A 13-digit South African ID number with a correct check digit, built from its parts."""
    body = "%s%04d%d8" % (yymmdd, seq, citizen)
    total = 0
    for i, ch in enumerate(reversed(body)):          # the check digit is the 13th: double every second digit counted from the right of the 12
        n = int(ch)
        if i % 2 == 0:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return body + str((10 - total % 10) % 10)


PAT_ID = make_id("900101", 5009)       # 01/01/1990, male
ROBIN_ID = make_id("920202", 2001)     # 02/02/1992, female

DATE = "05/11/2026"


def cell(v, st="confirmed"):
    return {"v": v, "st": st}


def row(st="confirmed", **cols):
    return {"d": cols, "st": st}


def pat_form():
    f = {
        "consent": cell("Yes"), "date": cell(DATE), "meet": cell("Teams Meeting"), "ref": cell("Current client"),
        "fname": cell("Pat "), "sname": cell("Samplecase"), "dob": cell("", "empty"), "age": cell("", "empty"), "idtype": cell("ID"),
        "idno": cell(PAT_ID), "gender": cell("", "empty"), "nat": cell("South African"), "tax": cell("", "empty"),
        "cell": cell("082 555 0100"), "work": cell("", "empty"), "home": cell("", "empty"), "pemail": cell("pat@example.invalid"), "wemail": cell("", "empty"),
        "edu": cell("3-year degree"), "edu_notes": cell("", "empty"), "profile": cell("", "empty"), "n_info": cell("", "empty"), "smoker": cell("No"),
        "employed": cell("Employed"), "employer": cell("Fakeco Logistics"),
        "co_does": cell("That's Fakeco Logistics. Try Fakeco Freight once more. I found no company with this name."),
        "bizowner": cell("No"), "occ": cell("Operations manager"), "ft": cell("Full time"), "years": cell("2015"),
        "d_desk": cell("60%"), "d_supo": cell("20%"), "d_trav": cell("20%"), "d_tot": cell("100%"), "d_desc": cell("Runs the depot teams. Reports to the director."),
        "gross": cell("R 45 000.00"), "dnet": cell("R 36 000.00"), "net": cell("R 34 500.00"), "exp": cell("R 22 000.00"), "disp": cell("R 12 500.00"),
        "marital": cell("Married"), "marr_date": cell("12/03/2016"), "sp_name": cell("Robin Testcase"), "sp_occ": cell("Teacher"),
        "has_debts": cell("Yes"), "has_kids": cell("Yes"),
        "has_risk": cell("Yes"), "joint": cell("No"), "ps_risk": cell("BrightRock"), "has_group": cell("No"), "has_ra": cell("Yes"), "has_pp": cell("No"),
        "has_inv": cell("Yes"), "ma": cell("Yes"), "ma_prov": cell("Discovery"), "ma_plan": cell("Classic Saver"), "gap": cell("No"),
        "will": cell("Yes"), "will_up": cell("No"), "will_where": cell("Attorney"), "sti": cell("Yes"), "sti_broker": cell("Other broker"),
        "h_gen": cell("Yes"), "h_dia": cell("No"), "h_chol": cell("No"), "h_bp": cell("No"), "h_bmi": cell("No"), "h_oth": cell("", "empty"),
        "fna_req": cell("Yes"), "fna_type": cell("New Business"), "fna_ins": cell("BrightRock"), "sf_req": cell("No"),
        "pr_ra": cell("High"), "rgar_req": cell("Yes"), "ret_age": cell("65"), "ret_net": cell("R 30 000.00"),
        "lc_hh": cell("R 10 000.00"), "lc_cc": cell("R 5 500.00"), "lc_dr": cell("R 19 000.00"), "lc_need": cell("R 34 500.00"),
        "lc_f_aciv": cell("?", "preset"), "lc_wol": cell("5%", "preset"), "lc_ccabi": cell("5%", "preset"), "pd_ccabi": cell("5%", "preset"),
        "dds_cover": cell("R 500 000.00", "preset"), "dds_term": cell("WOL", "preset"), "dds_abiv": cell("3%", "preset"),
        "dd_abiv": cell("3%", "preset"), "ips_abiv": cell("5%", "preset"), "ip_abiv": cell("5%", "preset"),
        "loa": cell("Yes"), "next_appt": cell("12/11/2026"), "next_day": cell("Thursday"), "next_time": cell("16:00"),
        "pa_actions": cell("Ask the client to decide. Set up the next appointment."),
    }
    lists = {
        "risk": [row(prov="BrightRock", spend="R 1 100.00", broker="Paul Kafentzis", notes="Fractured life cover")],
        "ret_ra": [row(prov="Old Mutual", status="Active", val="R 150 000.00", contrib="R 2 000.00", broker="Paul Kafentzis")],
        "inv": [row(type="Tax-free", prov="Fakeinvest", val="R 80 000.00", prem="R 1 000.00", broker="Paul Kafentzis")],
        "debts": [
            row(type="Home loan", prov="Absa", desc="Primary residence", owner="Pat", payer="Pat", term="18 years", inst="R 12 500.00", bal="R 1 450 000.00", asset="R 2 100 000.00", cl="", surety="No", notes=""),
            row(type="Vehicle finance", prov="WesBank", desc="Family car", owner="Pat", payer="Pat", term="3 years", inst="R 6 500.00", bal="R 180 000.00", asset="R 250 000.00", cl="No", surety="No", notes=""),
        ],
        "kids": [
            row(name="Sam", sname="Samplecase", gender="Female", dob="02/02/2018", age="8", stage="Primary school", cost="R 3 000.00"),
            row(name="Alex", sname="Samplecase", gender="Male", dob="03/03/2021", age="5", stage="Grade R", cost="R 2 500.00"),
        ],
        "bfred": [], "raq": [], "invq": [],
    }
    return {"app": "wr-fact-find", "schema": "3.0", "created": "2026-11-05T15:00:00.000Z", "modified": "2026-11-05T15:20:00.000Z", "f": f, "l": lists,
            "sum": {"life": "A drafted summary that must be ignored"}, "pa": {"x": 1}, "unplaced": [{"fact": "Pat mentioned an old policy somewhere", "why": "no box"}],
            "claude": {"in": 1, "out": 2}, "openai": {"sec": 3}}


def robin_form():
    """The spouse: her own job and cover; she has no debts or children rows of her own (the common ones come from Pat's form)."""
    f = {k: cell(v) for k, v in {
        "consent": "Yes", "date": DATE, "meet": "Teams Meeting", "ref": "Current client", "fname": "Robin", "sname": "Testcase", "idtype": "ID", "idno": ROBIN_ID,
        "nat": "South African", "cell": "083 555 0111", "pemail": "robin@example.invalid", "employed": "Employed", "employer": "Fakeschool", "co_does": "A primary school",
        "bizowner": "No", "occ": "Teacher", "ft": "Full time", "years": "6", "gross": "R 30 000.00", "net": "R 24 000.00", "exp": "R 15 000.00", "disp": "R 9 000.00",
        "marital": "Married", "sp_name": "Pat Samplecase", "has_debts": "Yes", "has_kids": "Yes", "has_risk": "No", "has_group": "Yes", "has_ra": "No", "has_pp": "Yes",
        "has_inv": "No", "ma": "Yes", "gap": "No", "will": "No", "sti": "No", "h_gen": "Yes", "smoker": "No",
    }.items()}
    lists = {"ret_pp": [row(type="Pension fund", prov="Fakefund", val="R 60 000.00", contrib="R 1 500.00", broker="Employer")]}
    return {"app": "wr-fact-find", "schema": "3.0", "created": "2026-11-05T15:00:00.000Z", "modified": "2026-11-05T15:25:00.000Z", "f": f, "l": lists}


def copy_form(form):
    return copy.deepcopy(form)
