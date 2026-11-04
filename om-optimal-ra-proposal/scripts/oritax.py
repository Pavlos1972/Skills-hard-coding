#!/usr/bin/env python3
"""The Tax Reform Tool results of one proposal: are they the ones these answers need, and the audit checks 1 to 9 of the old skill (Step 7), proven from the results.

Checks 4 and 5 (tax saved = a difference between two tax-payable figures) are COMPUTED and, when the two figures differ, flagged to Paul with both figures; they are
never forced (Paul, 04/11/2026: his known edge case). Every other check must hold.
"""
from decimal import Decimal

import ori as o
import taxtool as tt
import wrlib as w

D = Decimal
CENT = D("0.01")


def out(tax, run, key):
    return D(tax["runs"][run]["outputs"][key])


def bars(tax):
    return [D(b) for b in tax["runs"]["t3"]["bars"]]


def stale_problems(a, tax, today):
    """Problems that make the stored results unusable for these answers (empty = fine)."""
    probs = []
    p = tt.tax_year_problem(today)
    p and probs.append(p)
    if tax.get("workbook_sha") != w.sha256_file(tt.WORKBOOK):
        probs.append("the Tax Reform Tool workbook is not the one used for the stored results")
    if tax.get("facts_sha") != w.sha256_file(tt.FACTS):
        probs.append("the tax facts are not the ones used for the stored results")
    want = tt.scenarios(o.tool_context(a))
    for name, inp in want.items():
        got = (tax.get("runs") or {}).get(name)
        if not got:
            probs.append("scenario %s has not been run" % name)
            continue
        if got["inputs"] != tt.ser(inp):
            probs.append("scenario %s: the tool was run with other inputs than these answers need" % name)
        if got.get("problems"):
            probs.append("scenario %s: the workbook and the tax facts disagree: %s" % (name, "; ".join(got["problems"][:2])))
        e = got.get("echo") or {}
        try:
            echo_ok = (abs(D(e["remuneration"]) - D(inp["remuneration"])) < D("0.001") and int(D(e["age"])) == int(inp["age"]) and abs(D(e["ra_monthly"]) - D(inp["ra_monthly"])) < D("0.001"))
        except (KeyError, ArithmeticError):
            echo_ok = False
        if not echo_ok:
            probs.append("scenario %s: the recalculated copy does not carry the inputs that were written into it" % name)
        if got["outputs"].get("switch_in_copy") != tt.facts()["employment_switch"][inp["switch"]]:
            probs.append("scenario %s: the employment type in Calcs!B2 is not the one the client needs" % name)
    return probs


def audit(a, tax):
    """([(ok, short, detail)], [flag sentences]) : the old skill's audit checks 1 to 9 as far as the tool's results prove them (9 is proven on the built email)."""
    ctx = o.tool_context(a)
    cap = out(tax, "t1", "cap")
    fm, mx = ctx["fund_monthly"], ctx["max_ra"]
    rows, flags = [], []

    def add(ok, short, detail=""):
        rows.append((bool(ok), short, detail))
    tcm = cap / 12
    add(abs(cap - ctx["cap"]) <= tt.TOL and all(abs(out(tax, n, "cap") - cap) <= tt.TOL for n in ("baseline", "t2", "t3")),
        "Check 1: [TOTAL CAP MONTHLY] R %s = the tool's cap (Calcs!C15, R %s) divided by 12, and the cap equals MIN(R 430,000, 27.5%% of the annual remuneration plus the employer contributions)" %
        (o.money_shown(tcm.quantize(CENT)), o.money_shown(cap.quantize(CENT))))
    base_add = out(tax, "baseline", "additional_monthly")
    add(abs(base_add - mx) <= CENT and abs((cap - 12 * fm) / 12 - mx) <= CENT,
        "Check 2: [MAXIMUM RA CONTRIBUTION] R %s = (cap minus the yearly fund contributions) divided by 12, and equals the tool's own additional monthly premium at an RA of R 0 (C36)" % o.money_shown(mx.quantize(CENT)))
    pay = [out(tax, k, "tax_payable") for k in ("t1", "t2", "t3")]
    ra3 = D(tax["runs"]["t3"]["inputs"]["ra_monthly"])
    same23 = o.rand0(pay[1]) == o.rand0(pay[2])
    add(o.rand0(pay[0]) != o.rand0(pay[1]) and o.rand0(pay[0]) != o.rand0(pay[2]) and (not same23 or ra3 >= mx),
        "Check 3: the tax payable of Tables 1, 2 and 3 differ (R %s, R %s, R %s)%s" % (tuple(o.rand0(x) for x in pay) + (" (Tables 2 and 3 are equal because the proposed contribution uses the whole deduction)" if same23 else "",)))
    for n, name in ((4, "t2"), (5, "t3")):
        native = out(tax, name, "tax_saved_ra")
        diff = pay[0] - out(tax, name, "tax_payable")
        same = abs(native - diff) <= 1
        add(True, "Check %d: Table %s tax saved from the RA is R %s and Table 1 tax payable minus Table %s tax payable is R %s%s" %
            (n, name[1], o.rand0(native), name[1], o.rand0(diff), " (equal)" if same else " (they differ: the known edge case, flagged to Paul, not forced)"))
        if not same:
            flags.append("Table %s: the tool's own tax saved from the RA is R %s but Table 1 tax payable minus Table %s tax payable is R %s: the difference is the known bracket edge case (not forced)." %
                         (name[1], o.rand0(native), name[1], o.rand0(diff)))
    t2 = tax["runs"]["t2"]["outputs"]
    add(abs(fm + mx.quantize(CENT) - tcm) <= CENT and D(t2["pct_left"]) == 0 and D(t2["additional_monthly"]) == 0 and D(t2["lump_sum"]) == 0,
        "Check 6: Table 2 fund rows R %s + RA row R %s = [TOTAL CAP MONTHLY] R %s, and the tool shows 0%% left, no extra premium and no extra lump sum (the fixed lines of Table 2 are true)" %
        (o.money_shown(fm.quantize(CENT)), o.money_shown(mx.quantize(CENT)), o.money_shown(tcm.quantize(CENT))))
    left = max(D(0), (cap - 12 * (fm + ra3)) / cap * 100)
    got_left = out(tax, "t3", "pct_left") * 100
    add(abs(left - got_left) <= CENT, "Check 7: Table 3 maximum deduction left %s%% = (cap minus Table 3's yearly contributions) divided by the cap x 100, equal to the tool's C34" % o.pct_shown(left / 100))
    b1 = bars(tax)[0]
    add(abs(b1 - out(tax, "t3", "tax_saved_ra")) <= 1, "Check 8: the bar chart's year 1 (R %s) equals Table 3's tax saved from the RA (R %s)" % (o.rand0(b1), o.rand0(out(tax, "t3", "tax_saved_ra"))))
    if ctx["existing_total"] > 0 and out(tax, "t1", "tax_saved_ra") <= 0:
        flags.append("The client has an existing RA but the tool shows no tax saved from it in Table 1 (the income may be below the tax threshold).")
    room = mx
    if ra3 > room:
        flags.append("Table 3 contributes R %s a month to retirement annuities but only R %s a month is deductible: the excess is not tax-deductible." % (o.money_shown(ra3.quantize(CENT)), o.money_shown(room.quantize(CENT))))
    fd = o.fund_of(a)
    if fd["type"] != "none":
        rem = w.parse_money(a["gross_monthly_income"])
        for k, pk in (("employer_monthly", "employer_pct"), ("member_monthly", "member_pct")):
            share = rem * o.pct_decimal(fd[pk]) / 100
            if abs(share - w.parse_money(fd[k])) > 1:
                flags.append("The fund statement's %s%% of the gross income is R %s but its rand amount is R %s: the tool was given the rand amounts as a share of the gross income." %
                             (o.pct_digits(fd[pk]), o.money_shown(share.quantize(CENT)), o.money_shown(fd[k])))
    return rows, flags
