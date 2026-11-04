#!/usr/bin/env python3
"""The Tax Reform Tool, run by the program: the workbook is recalculated by LibreOffice for each scenario, the sheet and cell of every figure are named, and every figure
is recomputed independently here from the 2026/27 tax facts (assets/tax_facts.json). A workbook that disagrees with the facts, or a recalculation that does not match
the independent figures, stops the run. Nothing here is typed by the chat.

The workbook (assets/Tax_Reform_Tool_TEMPLATE_4.xlsm) is never changed: each scenario is a copy saved as .xlsx (its radio buttons are not needed: the employment type
is the text in Calcs!B2).
"""
import json
import os
import shutil
import subprocess
import tempfile
import warnings
from decimal import ROUND_HALF_UP, Decimal

import wrlib as w

ASSETS = os.path.join(w.SKILL_DIR, "assets")
WORKBOOK = os.path.join(ASSETS, "Tax_Reform_Tool_TEMPLATE_4.xlsm")
FACTS = os.path.join(ASSETS, "tax_facts.json")
SHEET, CALCS, REINVEST = "Maximise Allowance Tool", "Calcs", "Reinvest Calcs"
BAR_CELLS = ["H41", "I41", "J41", "K41", "L41", "M41", "N41", "O41", "P41", "Q41"]
TOL = Decimal("0.5")                       # the workbook is compared with the independent figures to within 50 cents


def facts():
    with open(FACTS, encoding="utf-8") as f:
        return json.load(f)


def valid_until():
    return w.parse_date(facts()["valid_until"])


def tax_year_problem(today):
    vu = valid_until()
    if today > vu:
        return ("The Tax Reform Tool and the tax facts are the %s tables, valid until %s. Today is %s. STOP: ask Paul to confirm the workbook has been updated, "
                "then update assets/Tax_Reform_Tool_TEMPLATE_4.xlsm and assets/tax_facts.json (valid_until) in Claude Code." % (facts()["tax_year"], facts()["valid_until"], today.strftime("%d/%m/%Y")))
    return None


def soffice_path():
    return shutil.which("soffice") or shutil.which("libreoffice")


def soffice_version():
    p = soffice_path()
    if not p:
        return None
    try:
        return subprocess.run([p, "--version"], capture_output=True, text=True, timeout=60).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None


# ------------------------------------------------------------------ the independent recomputation
def D(x):
    return Decimal(str(x))


def _lookup(table, key):
    """The last row whose first column is <= key (what the workbook's VLOOKUP(..., TRUE) does)."""
    row = table[0]
    for r in table:
        if key >= D(r[0]):
            row = r
    return row


def tax_on(taxable, f):
    br = f["brackets"]
    base, tax = Decimal(0), Decimal(0)
    for i, (lo, rate) in enumerate(br):
        lo = D(lo)
        hi = D(br[i + 1][0]) if i + 1 < len(br) else None
        if taxable > lo:
            top = taxable if hi is None or taxable < hi else hi
            tax += (top - lo) * D(rate)
    return tax


def marginal(taxable, f):
    return D(_lookup(f["brackets"], taxable)[1])


def independent(inp, f=None):
    """The tool's outputs from its inputs, worked out here. inp: remuneration (monthly), age, switch ('self_employed'|'pension'|'provident'), the four fund percentages
    as fractions of remuneration (employer_pension, member_pension, employer_provident, member_provident) and ra_monthly."""
    f = f or facts()
    rem, age, ra = D(inp["remuneration"]), int(inp["age"]), D(inp["ra_monthly"])
    sw = inp["switch"]
    A = rem * 12
    b16 = A * D(inp["employer_pension"]) if sw == "pension" else Decimal(0)
    b17 = A * D(inp["member_pension"]) if sw == "pension" else Decimal(0)
    b18 = A * D(inp["employer_provident"]) if sw == "provident" else Decimal(0)
    b19 = A * D(inp["member_provident"]) if sw == "provident" else Decimal(0)
    b20 = ra * 12
    b24 = b16 + b18
    b35 = A + b24
    cap = min(D(f["cap_rand"]), D(f["cap_percent"]) * b35)
    b15 = min(b16 + b17 + b18 + b19 + b20, cap)
    taxable = A - b15 + b24
    thr = D(_lookup(f["threshold_by_age"], D(age))[1])
    reb = D(_lookup(f["rebate_by_age"], D(age))[1])
    below = taxable <= thr
    rate = marginal(taxable, f)
    payable = Decimal(0) if below else max(Decimal(0), tax_on(taxable, f) - reb)
    saved_ra = Decimal(0) if below else min(b15 - (b16 + b17 + b18 + b19), b15) * rate
    saved_pen = Decimal(0) if below else min(b17, b15) * rate
    saved_prov = Decimal(0) if below else min(b19, b15) * rate
    left = 1 - min(b16 + b17 + b18 + b19 + b20, cap) / cap
    extra = cap - min(b15, cap)
    return {"cap": cap, "annual_base": b35, "tax_saved_ra": saved_ra, "tax_saved_pension": saved_pen, "tax_saved_provident": saved_prov, "tax_payable": payable,
            "pct_left": left, "additional_monthly": extra / 12, "lump_sum": extra, "taxable": taxable}


# ------------------------------------------------------------------ the workbook
def cell_inputs(inp):
    """{(sheet, cell): value} written into the copy of the workbook for one scenario."""
    c = facts()["cells"]
    sw = facts()["employment_switch"][inp["switch"]]
    return {(SHEET, c["remuneration"]): float(inp["remuneration"]), (SHEET, c["age"]): int(inp["age"]),
            (SHEET, c["employer_pension"]): float(inp["employer_pension"]), (SHEET, c["member_pension"]): float(inp["member_pension"]),
            (SHEET, c["employer_provident"]): float(inp["employer_provident"]), (SHEET, c["member_provident"]): float(inp["member_provident"]),
            (SHEET, c["ra_monthly"]): float(inp["ra_monthly"]), (CALCS, "B2"): sw}


def run_workbook(inp, workdir):
    """Recalculate one scenario in LibreOffice. Returns the outputs read from the recalculated copy (Decimal), plus the ten bar values."""
    import openpyxl
    soffice = soffice_path()
    if not soffice:
        raise RuntimeError("LibreOffice (soffice) is not installed: the tax tool cannot be recalculated")
    os.makedirs(workdir, exist_ok=True)
    src = os.path.join(workdir, "scenario.xlsx")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        wb = openpyxl.load_workbook(WORKBOOK)
        for (sheet, cell), v in cell_inputs(inp).items():
            wb[sheet][cell] = v
        wb.save(src)
    out = os.path.join(workdir, "out")
    os.makedirs(out, exist_ok=True)
    profile = tempfile.mkdtemp(prefix="wr-lo-")
    try:
        r = subprocess.run([soffice, "--headless", "-env:UserInstallation=file://" + profile, "--calc", "--convert-to", "xlsx", "--outdir", out, src],
                           capture_output=True, text=True, timeout=240)
    finally:
        shutil.rmtree(profile, ignore_errors=True)
    done = os.path.join(out, "scenario.xlsx")
    if r.returncode != 0 or not os.path.exists(done):
        raise RuntimeError("LibreOffice did not recalculate the workbook: %s" % (r.stderr or r.stdout)[:300])
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        wb2 = openpyxl.load_workbook(done, data_only=True)
    c = facts()["cells"]
    s = wb2[SHEET]
    res = {k: s[c[k]].value for k in ("tax_saved_ra", "tax_saved_pension", "tax_saved_provident", "tax_payable", "pct_left", "additional_monthly", "lump_sum")}
    res["cap"] = wb2[CALCS]["C15"].value
    res["annual_base"] = wb2[CALCS]["B35"].value
    res["switch_in_copy"] = wb2[CALCS]["B2"].value
    res["echo"] = {k: s[c[k]].value for k in ("remuneration", "age", "ra_monthly")}
    bars = [wb2[REINVEST][b].value for b in BAR_CELLS]
    if any(v is None for v in res.values() if not isinstance(v, dict)) or any(b is None or isinstance(b, str) for b in bars):
        raise RuntimeError("the recalculated workbook has empty or error cells: %s" % {k: v for k, v in res.items() if v is None or isinstance(v, str)})
    res = {k: (D(v) if not isinstance(v, (str, dict)) else v) for k, v in res.items()}
    return res, [D(b) for b in bars]


def compare(inp, got):
    """Problems (list of strings) between what the workbook returned and the independent figures."""
    ind = independent(inp)
    probs = []
    for k in ("cap", "annual_base", "tax_saved_ra", "tax_saved_pension", "tax_saved_provident", "tax_payable", "pct_left", "additional_monthly", "lump_sum"):
        tol = TOL if k not in ("pct_left",) else Decimal("0.00001")
        if abs(D(got[k]) - ind[k]) > tol:
            probs.append("%s: the workbook says %s, the tax facts say %s" % (k, D(got[k]).quantize(Decimal("0.01")), ind[k].quantize(Decimal("0.01"))))
    return probs


def money0(x):
    return D(x).quantize(Decimal("1"), rounding=ROUND_HALF_UP)


# ------------------------------------------------------------------ the scenarios of one proposal
def scenarios(ctx):
    """The inputs of the scenarios, from the answers' facts. ctx: remuneration, age, switch, fund percentages as fractions, existing_total, proposed, ra_decision, max_ra."""
    base = {"remuneration": ctx["remuneration"], "age": ctx["age"], "switch": ctx["switch"], "employer_pension": ctx["employer_pension"], "member_pension": ctx["member_pension"],
            "employer_provident": ctx["employer_provident"], "member_provident": ctx["member_provident"]}
    t3_ra = D(ctx["proposed"]) + (D(ctx["existing_total"]) if ctx["ra_decision"] == "keep" else Decimal(0))
    return {"baseline": dict(base, ra_monthly=Decimal(0)), "t1": dict(base, ra_monthly=D(ctx["existing_total"])), "t2": dict(base, ra_monthly=D(ctx["max_ra"])), "t3": dict(base, ra_monthly=t3_ra)}


def ser(x):
    return {k: (str(v) if isinstance(v, Decimal) else v) for k, v in x.items()}


def run_all(ctx, workdir):
    """Run the scenarios (identical ones once). Returns the dict stored as tax.json."""
    sc = scenarios(ctx)
    runs, cache = {}, {}
    for name, inp in sc.items():
        key = json.dumps(ser(inp), sort_keys=True)
        if key not in cache:
            got, bars = run_workbook(inp, os.path.join(workdir, name))
            cache[key] = (got, bars)
        got, bars = cache[key]
        runs[name] = {"inputs": ser(inp), "outputs": {k: (str(v) if isinstance(v, Decimal) else v) for k, v in got.items() if k != "echo"},
                      "echo": {k: str(v) for k, v in got["echo"].items()}, "bars": [str(b) for b in bars], "problems": compare(inp, got)}
    return {"workbook_sha": w.sha256_file(WORKBOOK), "facts_sha": w.sha256_file(FACTS), "soffice": soffice_version(), "tax_year": facts()["tax_year"], "runs": runs}
