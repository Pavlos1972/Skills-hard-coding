#!/usr/bin/env python3
"""The domain model of the OM Optimal RA proposal emails: the answers (every figure checked against the documents' text), the figures for the Tax Reform Tool, the audit
checks on the tool's results, the two emails built from the fixed templates (the main proposal and the separate Lump Sum Investment proposal), the Teams message to
Sitamah, the file names, the confirmation table, and the checks of what comes back (the Outlook draft and the posted message).

Everything here is a pure function of the answers (answers.json), the tool results (tax.json) and the stored build time, so the checker can recompute it and refuse a
file edited by hand. Rules are Paul's (the old skill, kept) and his answers of 04/11/2026. Nothing here sends anything.
"""
import calendar
import html
import json
import os
import re
from decimal import ROUND_HALF_UP, Decimal

import docread
import taxtool as tt
import wrlib as w

ASSETS = os.path.join(w.SKILL_DIR, "assets")
TEMPLATES = {"main": os.path.join(ASSETS, "OM_Optimal_RA_Proposal_TEMPLATE.html"), "lump_sum": os.path.join(ASSETS, "OM_Optimal_RA_LumpSum_Proposal_TEMPLATE.html")}
SETTINGS = os.path.join(ASSETS, "settings.json")
WORDING = os.path.join(ASSETS, "wording.json")

CC_NAME = "Sitamah Nathoo"
CC_EMAIL = "admin@liferisk.co.za"
SITAMAH_CHAT = "19:bd2a130a-35d9-459e-9025-55f356810236_e6901cee-de73-46d9-88a5-5e4a1c296418@unq.gbl.spaces"
CHAT_LABEL = "(1:1 Chat) Paul Kafentzis, Sitamah Nathoo"

DOCUMENTS = ("main", "lump_sum")
ROLE_LABEL = {"quote": "OM Optimal RA Quote (Plan 1)", "fact_find_summary": "Fact Find Summary", "booster_doc": "Optimal Illustrator (RA Booster Value)",
              "astute_ccp": "Astute CCP report or the policy schedules", "client_overview": "Client Overview ('Current Investments')",
              "fund_statement": "Pension / Provident Fund statement", "poi": "Proof of income / payslip", "rgar": "RGAR report (from Alwyn)", "lump_sum_quote": "OM Lump Sum Quote (Plan 2)"}
ALWAYS = {"main": ("quote", "fact_find_summary", "booster_doc"), "lump_sum": ("lump_sum_quote", "fact_find_summary")}
OPTIONAL = {"main": ("astute_ccp", "client_overview", "fund_statement", "poi", "rgar"), "lump_sum": ("astute_ccp", "client_overview")}
SERVED_ORDER = ("fact_find_summary", "quote", "lump_sum_quote", "booster_doc", "astute_ccp", "client_overview", "fund_statement", "poi", "rgar")
FIXED_ROLES = tuple(r for r in SERVED_ORDER)
SOURCE_KEYS = {"main": ("personal", "income", "fund", "existing_ras", "ra_decision", "rgar", "quote", "funds_fees", "email", "meetings", "next_meeting"),
               "lump_sum": ("personal", "lump", "quote", "email", "meetings", "next_meeting")}
COMMON_KEYS = {"document", "client_full_name", "client_first_name", "client_surname", "client_email", "email_source", "email_note", "meetings_held", "next_meeting",
               "plan_folder", "flags", "sources", "conflicts", "start_date", "funds"}
ANSWER_KEYS = {"main": COMMON_KEYS | {"age", "employer", "position", "gross_monthly_income", "fund", "existing_ras", "ra_decision", "rgar", "proposed_premium", "net_admin_fee",
                                      "advice_fee", "adviser_charge", "monthly_admin_fee", "lump_sum_applies"},
               "lump_sum": COMMON_KEYS | {"lump", "ls_fees"}}
PLACEHOLDER = re.compile(r"\[[A-Z][A-Z0-9 _%().,/&#-]*\]")
EXPECTED_COUNT = {"[AGE]": 4, "[MONTHLY REMUNERATION]": 3, "[PROPOSED PREMIUM]": 3}
MAIN_PLACEHOLDERS = ("[DATE AND TIME SENT]", "[CLIENT EMAIL]", "[CC NAME(S)]", "[SUBJECT]", "[CLIENT FIRST NAME]", "[MEETING DATES LIST]", "[AGE]", "[MONTHLY REMUNERATION]", "[PROPOSED PREMIUM]", "[EMPLOYER NAME]", "[POSITION]",
                     "[GROSS MONTHLY INCOME]", "[RA_ROWS]", "[PENSION_BLOCK]", "[SAVE SENTENCE]", "[RGAR PARAGRAPH]", "[PRODUCT START DATE]", "[T1_FUND_ROWS]", "[T1_RA_ROWS]",
                     "[T1 ANNUAL TAX SAVED RA]", "[FUND TAX LABEL]", "[TAX SAVED FUND]", "[T1 ANNUAL TAX PAYABLE]", "[T1 PCT REMAINING]", "[T1 ADDITIONAL MONTHLY PREMIUM]",
                     "[T1 LUMP SUM]", "[T1 MESSAGE]", "[MAXIMUM CONTRIBUTION]", "[T2_FUND_ROWS]", "[T2_RA_ROWS]", "[T2 ANNUAL TAX SAVED RA]", "[T2 ANNUAL TAX PAYABLE]",
                     "[T3_FUND_ROWS]", "[T3_RA_ROWS]", "[T3 ANNUAL TAX SAVED RA]", "[T3 ANNUAL TAX PAYABLE]", "[T3 PCT REMAINING]", "[T3 ADDITIONAL MONTHLY PREMIUM]",
                     "[T3 LUMP SUM]", "[T3 MESSAGE]") + tuple("[BAR_%d]" % i for i in range(1, 11)) + (
                     "[FUNDS SENTENCE]", "[FUND_ROWS]", "[ASSET MGMT FEE]", "[NET ADMIN FEE]", "[ADVICE FEE]", "[ADVISER CHARGE]", "[TOTAL ONGOING FEES]", "[MONTHLY ADMIN FEE]",
                     "[FUND NAMES LIST]", "[NEXT MEETING LINE]")
LUMP_PLACEHOLDERS = ("[DATE AND TIME SENT]", "[CLIENT EMAIL]", "[CC NAME(S)]", "[SUBJECT]", "[CLIENT FIRST NAME]", "[MEETING DATES LIST]", "[LUMP_SUM_BLOCK]", "[PRODUCT START DATE]",
                     "[LS_FUND_FEE_BLOCK]", "[LS_TAX_TREATMENT_NOTE]", "[NEXT MEETING LINE]")
MARKERS = {"main": ("BODY", "LOGO", "RA TABLE", "FUND TAX"), "lump_sum": ("BODY", "LOGO")}
REGION_PLACEHOLDERS = {"RA TABLE": ("[RA_ROWS]",), "FUND TAX": ("[FUND TAX LABEL]", "[TAX SAVED FUND]")}


def valid_role(role, document):
    return role in ALWAYS[document] + OPTIONAL[document]


def can_be_missing(role, document):
    return role in OPTIONAL[document]


def served_roles(document):
    return tuple(r for r in SERVED_ORDER if r in ALWAYS[document] + OPTIONAL[document])


def settings():
    with open(SETTINGS, encoding="utf-8") as f:
        return json.load(f)


def wording():
    with open(WORDING, encoding="utf-8") as f:
        return json.load(f)


def D(x):
    return x if isinstance(x, Decimal) else Decimal(str(x))


# ------------------------------------------------------------------ values
def money_shown(v):
    """Rand with thousands commas; cents only when the figure has cents (the document's own formatting)."""
    d = w.parse_money(v)
    if d is None:
        return str(v)
    cents = bool(re.search(r"[.,]\d{2}\s*$", str(v).strip())) or d != d.to_integral_value()
    return format(d, ",.2f") if cents else format(int(d), ",d")


def rand0(v):
    return format(int(D(v).quantize(Decimal("1"), rounding=ROUND_HALF_UP)), ",d")


def num(v):
    """A Decimal from a Decimal, a plain number string from the tool ('30457.5') or a figure as a document shows it ('R 2 500.00')."""
    if isinstance(v, Decimal):
        return v
    try:
        return Decimal(str(v))
    except ArithmeticError:
        d = w.parse_money(v)
        if d is None:
            raise ValueError("%r is not an amount" % (v,))
        return d


def rand_cell(v, whole=False):
    d = num(v)
    if d == 0:
        return "&#8211;"
    return rand0(d) if whole else money_shown(d.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def pct_shown(frac):
    p = (D(frac) * 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    s = format(p, "f")
    return s.rstrip("0").rstrip(".") if "." in s else s


def pct_digits(v):
    return str(v).replace("%", "").strip().replace(" ", "").replace(",", ".")


def pct_decimal(v):
    """A percentage as a Decimal with ITS OWN decimals (0.575 stays 0.575), or None: money parsing refuses three decimals."""
    s = pct_digits(v)
    return Decimal(s) if re.fullmatch(r"\d+(?:\.\d+)?", s) else None


def fee_shown(d):
    d = D(d).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)
    s = format(d, "f")
    return s[:-1] if s.endswith("0") else s


def fmt_date_with_day(d):
    return "%s, %s" % (calendar.day_name[d.weekday()], d.strftime("%d/%m/%Y"))


def meetings_line(a):
    parts = [fmt_date_with_day(d) for d in sorted(w.parse_date(x) for x in a["meetings_held"])]
    return parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " & " + parts[-1]


def next_date(a):
    return w.parse_date(a["next_meeting"]["date"])


def next_line(a):
    return "%s @ %s" % (fmt_date_with_day(next_date(a)), a["next_meeting"]["time"].strip())


def names_list(names, the=False, amp="&"):
    """'A', 'A & B', 'A, B & C' (with 'the' before the later ones when the=True: 'A & the B'); amp="&amp;" when the result goes into HTML."""
    nm = [n for n in names]
    if the:
        nm = [nm[0]] + ["the " + n for n in nm[1:]]
    return nm[0] if len(nm) == 1 else ", ".join(nm[:-1]) + " " + amp + " " + nm[-1]


def doc_of(a):
    return a.get("document", "main")


def premium_of(a):
    return money_shown(a["proposed_premium"])


def subject(a):
    wd = wording()
    if doc_of(a) == "lump_sum":
        return html.unescape(wd["subject_lump"].format(name=a["client_full_name"].strip(), amount=money_shown(a["lump"]["amount"])))
    return html.unescape(wd["subject_main"].format(name=a["client_full_name"].strip(), premium=premium_of(a)))


def sent_text(clock):
    return "%s, %s %s" % (calendar.day_name[clock.weekday()], clock.strftime("%d/%m/%Y"), clock.strftime("%H:%M"))


def file_name(a, d):
    first = a["client_first_name"].strip().replace(" ", "_")
    sur = a["client_surname"].strip().replace(" ", "_")
    kind = "OM_Optimal_RA_LumpSum_Proposal_Email" if doc_of(a) == "lump_sum" else "OM_Optimal_RA_Proposal_Email"
    return w.safe_filename("%s_%s_%s - %s" % (first, sur, kind, d.strftime("%d.%m.%y"))) + ".html"


def greeting_for(clock, used_today):
    if used_today:
        return "Hi"
    return "Good morning" if clock.hour < 12 else ("Good afternoon" if clock.hour < 18 else "Good evening")


def no_ext(name):
    return name[:-4] if name.lower().endswith(".pdf") else name


def doc_name(docs, role):
    return docs["docs"][role]["name"]


# ------------------------------------------------------------------ the figures for the Tax Reform Tool
def fund_of(a):
    f = a.get("fund") or {"type": "none"}
    return f if f.get("type") in ("pension", "provident") else {"type": "none"}


def existing_total(a):
    return sum((w.parse_money(r["monthly"]) for r in a.get("existing_ras") or []), Decimal(0))


def blended_fee(a):
    return sum((pct_decimal(f["allocation"]) / 100 * pct_decimal(f["asset_mgmt_fee"]) for f in a["funds"]), Decimal(0)).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)


def total_fees(a):
    parts = [blended_fee(a)] + [w.parse_money(a[k]) for k in ("net_admin_fee", "advice_fee", "adviser_charge")]
    return sum(parts, Decimal(0))


def tool_context(a):
    """Everything the tool needs, worked out from the answers (never typed): the fund contributions as a share of the gross income, the maximum RA."""
    rem = w.parse_money(a["gross_monthly_income"])
    fd = fund_of(a)
    ft = fd["type"]
    ep = w.parse_money(fd.get("employer_monthly")) if ft != "none" else Decimal(0)
    mp = w.parse_money(fd.get("member_monthly")) if ft != "none" else Decimal(0)
    ctx = {"remuneration": rem, "age": int(a["age"]), "switch": "self_employed" if ft == "none" else ft, "employer_pension": Decimal(0), "member_pension": Decimal(0),
           "employer_provident": Decimal(0), "member_provident": Decimal(0), "existing_total": existing_total(a), "proposed": w.parse_money(a["proposed_premium"]),
           "ra_decision": a.get("ra_decision") or "none"}
    if ft == "pension":
        ctx["employer_pension"], ctx["member_pension"] = ep / rem, mp / rem
    elif ft == "provident":
        ctx["employer_provident"], ctx["member_provident"] = ep / rem, mp / rem
    ctx["fund_monthly"] = ep + mp
    base = dict(ctx, ra_monthly=Decimal(0))
    ctx["max_ra"] = tt.independent(base)["additional_monthly"]
    ctx["cap"] = tt.independent(base)["cap"]
    return ctx


# ------------------------------------------------------------------ validation
def _has(e):
    return e is not None and e.has_text


def _any(evs, fn):
    """None if any readable document passes (or none is readable: then it is only attested), else the first message."""
    texts = [e for e in evs if _has(e)]
    if not texts:
        return None
    first = None
    for e in texts:
        m = fn(e)
        if m is None:
            return None
        first = first or m
    return first


def _near_any(evs, label, pats, value, window=160):
    texts = [e for e in evs if _has(e)]
    if not texts:
        return None
    first, nolabel = None, False
    for e in texts:
        m = e.near(label, pats, value, window=window)
        if m is None:
            return None
        if m == "NOLABEL":
            nolabel = True
        else:
            first = first or m
    return None if nolabel and first is None else first


def _pct_after(e, label, pats, tok, window=100):
    """A percentage with its own decimals must follow its label closely (None = fine, "NOLABEL" = no label in the text, else a message)."""
    hits = [m.end() for p in pats for m in re.finditer(p, e.flat, re.I)]
    if not hits:
        return "NOLABEL"
    t = pct_digits(tok)
    pat = r"(?<![\d.,])" + re.escape(t).replace(r"\.", "[.,]") + r"(?!\d)"
    if any(re.search(pat, e.flat[end:end + window]) for end in hits):
        return None
    return "%s: %s%% is not next to its label in the document's text" % (label, t)


def _pct_near_any(evs, label, pats, tok, window=100):
    texts = [e for e in evs if _has(e)]
    if not texts:
        return None
    first, nolabel = None, False
    for e in texts:
        m = _pct_after(e, label, pats, tok, window)
        if m is None:
            return None
        if m == "NOLABEL":
            nolabel = True
        else:
            first = first or m
    return None if nolabel and first is None else first


def _common_problems(a, ev, docs, today, run_client, document, out):
    for k in set(a) - ANSWER_KEYS[document]:
        out.append("unknown field %r" % k)
    if a.get("document", "main") != document:
        out.append("document must be %r in this run" % document)
    for k in ("client_full_name", "client_first_name", "client_surname", "plan_folder", "client_email"):
        if not str(a.get(k) or "").strip():
            out.append("%s is missing" % k)
    if run_client and w.norm("%s %s" % (a.get("client_first_name", ""), a.get("client_surname", ""))) != w.norm(run_client):
        out.append("the everyday name is not the client Paul named (%s)" % run_client)
    if w.norm(a.get("client_surname", "")) not in w.norm(a.get("client_full_name", "")):
        out.append("the surname must be part of the client's full name")
    if a.get("conflicts"):
        out.append("%d unresolved conflict(s) between sources: STOP and ask Paul, quoting both values and their sources" % len(a["conflicts"]))
    srcs = a.get("sources") or {}
    for k in SOURCE_KEYS[document]:
        if len(str(srcs.get(k) or "").strip()) < 3:
            out.append("sources.%s: every answer needs its source (a document or Paul's words)" % k)
    if not isinstance(a.get("flags"), list) or not all(isinstance(x, str) for x in a.get("flags", [])):
        out.append("flags must be a list of short sentences (empty list if there is nothing to flag)")
    # every optional document is registered or Paul said it does not exist
    for role in OPTIONAL[document]:
        if role not in docs["docs"] and not (docs["missing"].get(role) or "").strip():
            out.append("%s: register it, or record that it does not exist with Paul's words (run.py doc --missing %s --said ...)" % (ROLE_LABEL[role], role))
    # the client's email and the dates
    em = str(a.get("client_email") or "").strip()
    f = ev.get("fact_find_summary")
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", em):
        out.append("client_email %r is not an email address" % em)
    elif a.get("email_source") == "fact_find_summary":
        if _has(f) and em.lower() not in f.text.lower():
            out.append("client_email is not in the Fact Find Summary's text (email_source says it is)")
    elif a.get("email_source") == "other":
        if len(str(a.get("email_note") or "").strip()) < 10:
            out.append("client_email from another source: say which (manual Fact Find, Zapier contact lookup, Outlook search) in email_note")
    else:
        out.append("email_source must be 'fact_find_summary' or 'other' (with email_note)")
    mh = a.get("meetings_held")
    if not isinstance(mh, list) or not mh or any(w.parse_date(x) is None for x in mh):
        out.append("meetings_held: at least one date, each DD/MM/YYYY")
    elif any(w.parse_date(x) > today for x in mh):
        out.append("a meeting already held cannot be in the future")
    elif len(set(mh)) != len(mh):
        out.append("meetings_held has the same date twice")
    nm = a.get("next_meeting") or {}
    nd = w.parse_date(nm.get("date"))
    if nd is None or not re.fullmatch(r"\d{1,2}(:\d{2})?\s?(am|pm)", str(nm.get("time") or "").strip(), re.I):
        out.append("next_meeting needs a date (DD/MM/YYYY) and a time like 12pm or 5:30pm")
    elif nd < today:
        out.append("the next meeting date %s is in the past" % nm["date"])
    if f is None:
        out.append("the Fact Find Summary must be registered first")
    elif _has(f):
        m = f.name("client name in the Fact Find Summary", a.get("client_full_name"))
        m and out.append(m)


def _funds_problems(a, quote_evs, out, label="quote"):
    """The funds, their allocations and fees against the quote's text; the allocations add up to 100."""
    fs = a.get("funds")
    if not isinstance(fs, list) or not fs:
        out.append("funds: at least one fund, each with name, allocation and asset_mgmt_fee")
        return
    tot = Decimal(0)
    seen = set()
    for f in fs:
        if not isinstance(f, dict) or set(f) != {"name", "allocation", "asset_mgmt_fee"} or not str(f.get("name") or "").strip():
            out.append("each fund needs exactly name, allocation and asset_mgmt_fee")
            return
        alloc, fee = pct_decimal(f["allocation"]), pct_decimal(f["asset_mgmt_fee"])
        if alloc is None or alloc <= 0 or fee is None:
            out.append("fund %r: allocation and asset_mgmt_fee must be numbers" % f["name"])
            continue
        if w.norm(f["name"]) in seen:
            out.append("fund %r is listed twice" % f["name"])
        seen.add(w.norm(f["name"]))
        tot += alloc
        m = _any(quote_evs, lambda e: e.name("fund in the %s" % label, f["name"]))
        m and out.append(m)
        m = _any(quote_evs, lambda e: e.number("allocation of %s in the %s" % (f["name"], label), alloc))
        m and out.append(m)
        pat = [re.escape(f["name"]).replace(r"\ ", r"\s+")]
        m = _near_any(quote_evs, "allocation of %s" % f["name"], pat, alloc, window=160)
        m and out.append(m)
        m = _any(quote_evs, lambda e: e.exact_percent("asset management fee of %s in the %s" % (f["name"], label), pct_digits(f["asset_mgmt_fee"])))
        m and out.append(m)
        if not m:
            m = _pct_near_any(quote_evs, "asset management fee of %s in the %s" % (f["name"], label), pat, f["asset_mgmt_fee"], window=120)
            m and out.append(m)
    if tot != 100:
        out.append("the allocations add up to %s%%, not 100%%" % tot)


def answers_problems(a, ev, docs, today, run_client=None, document="main"):
    """Problems with the entered answers (empty = fine). `ev` maps a document role to a docread.Evidence (or None); `docs` is docs.json."""
    out = []
    _common_problems(a, ev, docs, today, run_client, document, out)
    for r in ALWAYS[document]:
        if r not in docs["docs"]:
            return out + ["%s must be registered first" % ROLE_LABEL[r]]
    if document == "lump_sum":
        return out + _lump_problems(a, ev, docs)
    return out + _main_problems(a, ev, docs, today)


def _main_problems(a, ev, docs, today):
    out = []
    q, f, b = ev.get("quote"), ev.get("fact_find_summary"), ev.get("booster_doc")
    p = tt.tax_year_problem(today)
    p and out.append(p)
    for k in ("employer", "position"):
        if not str(a.get(k) or "").strip():
            out.append("%s is missing" % k)
    age = a.get("age")
    if not isinstance(age, int) or isinstance(age, bool) or not 18 <= age <= 100:
        out.append("age must be a whole number (the client's age in the Fact Find Summary)")
    elif _has(f):
        m = f.number("age in the Fact Find Summary", Decimal(age))
        m and out.append(m)
    if _has(f):
        for lab, key in (("employer", "employer"), ("position", "position")):
            m = f.name("%s in the Fact Find Summary" % lab, a.get(key))
            m and out.append(m)
    inc = w.parse_money(a.get("gross_monthly_income"))
    if inc is None or inc <= 0:
        out.append("gross_monthly_income %r is not an amount" % a.get("gross_monthly_income"))
    else:
        m = _any([f, ev.get("poi")], lambda e: e.number("gross monthly income in the Fact Find Summary / proof of income", inc))
        m and out.append(m)
    # ---- the fund
    fd = a.get("fund") or {}
    ft = fd.get("type")
    if ft == "both":
        out.append("STOP: the client has BOTH a pension and a provident fund: the Tax Reform Tool takes one fund type at a time (the employment switch in Calcs!B2): ask Paul how to proceed")
    elif ft not in ("none", "pension", "provident"):
        out.append("fund.type must be 'none', 'pension' or 'provident'")
    elif ft == "none":
        if set(fd) - {"type"}:
            out.append("fund.type is 'none': leave the other fund fields out")
    else:
        if "fund_statement" not in docs["docs"]:
            out.append("the client has a %s fund: the fund statement must be registered" % ft)
        if set(fd) != {"type", "employer_monthly", "employer_pct", "member_monthly", "member_pct", "value", "value_date"}:
            out.append("fund needs exactly type, employer_monthly, employer_pct, member_monthly, member_pct, value, value_date")
        else:
            fs = [ev.get("fund_statement"), ev.get("poi")]
            for k, lab in (("employer_monthly", "employer contribution"), ("member_monthly", "member contribution")):
                d = w.parse_money(fd[k])
                if d is None or d < 0:
                    out.append("fund.%s %r is not an amount" % (k, fd[k]))
                elif d != 0:
                    m = _any(fs, lambda e: e.number("%s in the fund statement / proof of income" % lab, d))
                    m and out.append(m)
            for k, lab in (("employer_pct", "employer contribution percentage"), ("member_pct", "member contribution percentage")):
                if pct_decimal(fd[k]) is None:
                    out.append("fund.%s %r is not a percentage" % (k, fd[k]))
                elif pct_decimal(fd[k]) != 0:
                    m = _any(fs, lambda e: e.exact_percent("%s in the fund statement / proof of income" % lab, fd[k]))
                    m and out.append(m)
            v = w.parse_money(fd["value"])
            if v is None or v <= 0:
                out.append("fund.value %r is not an amount" % fd["value"])
            else:
                m = _any([ev.get("fund_statement")], lambda e: e.number("fund value in the fund statement", v))
                m and out.append(m)
            if w.parse_date(fd["value_date"]) is None:
                out.append("fund.value_date must be DD/MM/YYYY")
            else:
                m = _any([ev.get("fund_statement")], lambda e: e.date("fund value date in the fund statement", fd["value_date"]))
                m and out.append(m)
    # ---- the existing retirement annuities
    ras = a.get("existing_ras")
    if not isinstance(ras, list):
        out.append("existing_ras must be a list (empty when the client has none)")
        ras = []
    dec = a.get("ra_decision")
    if dec not in ("none", "replace", "keep") or (dec == "none") != (not ras):
        out.append("ra_decision must be 'none' exactly when there are no existing RAs, otherwise 'replace' or 'keep' (Paul's answer)")
    if ras and not any(r in docs["docs"] for r in ("astute_ccp", "client_overview")):
        out.append("the client has existing RAs: the Astute CCP report, the policy schedules or the Client Overview must be registered")
    for r in ras:
        if not isinstance(r, dict) or set(r) != {"insurer", "policy_number", "monthly", "gross_value", "value_date", "no_penalties"}:
            out.append("each existing RA needs exactly insurer, policy_number, monthly, gross_value, value_date, no_penalties")
            continue
        evs = [ev.get("astute_ccp"), ev.get("client_overview")]
        for k, lab in (("monthly", "monthly contribution"), ("gross_value", "gross fund value")):
            d = w.parse_money(r[k])
            if d is None or d < 0:
                out.append("existing RA %s: %s %r is not an amount" % (r["policy_number"], lab, r[k]))
            else:
                m = _any(evs, lambda e: e.number("%s of RA %s" % (lab, r["policy_number"]), d))
                m and out.append(m)
        m = _any(evs, lambda e: e.name("insurer of RA %s" % r["policy_number"], r["insurer"]))
        m and out.append(m)
        m = _any(evs, lambda e: e.code("policy number", r["policy_number"]))
        m and out.append(m)
        if w.parse_date(r["value_date"]) is None:
            out.append("existing RA %s: value_date must be DD/MM/YYYY" % r["policy_number"])
        else:
            m = _any(evs, lambda e: e.date("value date of RA %s" % r["policy_number"], r["value_date"]))
            m and out.append(m)
        if not isinstance(r["no_penalties"], bool):
            out.append("existing RA %s: no_penalties must be true or false (true only on Paul's word that the policy is too new for penalties)" % r["policy_number"])
    # ---- the RGAR
    rg = a.get("rgar")
    if rg is None:
        if "rgar" in docs["docs"]:
            out.append("an RGAR is registered but the rgar answer is null")
    else:
        if "rgar" not in docs["docs"]:
            out.append("rgar answers need the RGAR report registered")
        if not isinstance(rg, dict) or set(rg) != {"shortfall", "years", "current_value", "future_value", "retirement_age"}:
            out.append("rgar needs exactly shortfall, years, current_value, future_value, retirement_age")
        else:
            r = ev.get("rgar")
            for k, lab, pats in (("shortfall", "second shortfall amount", None), ("years", "years to retirement", [r"years until retirement", r"years to retirement"]),
                                 ("current_value", "current value of the expenses", [r"current value"]), ("future_value", "future value of the expenses", [r"future value"]),
                                 ("retirement_age", "retirement age", [r"retirement age"])):
                d = w.parse_money(rg[k])
                if d is None or d <= 0:
                    out.append("rgar.%s %r is not a number" % (k, rg[k]))
                    continue
                m = _any([r], lambda e: e.number("%s in the RGAR" % lab, d))
                m and out.append(m)
                if pats and not m:
                    m = _near_any([r], "%s in the RGAR" % lab, pats, d, window=70)
                    m and out.append(m)
    # ---- the quote
    prem = w.parse_money(a.get("proposed_premium"))
    if prem is None or prem <= 0:
        out.append("proposed_premium %r is not an amount" % a.get("proposed_premium"))
    else:
        m = _any([q], lambda e: e.number("proposed premium in the quote", prem))
        m and out.append(m)
        if not m:
            m = _near_any([q], "proposed premium in the quote", [r"regular contribution", r"premium", r"monthly contribution"], prem, window=60)
            m and out.append(m)
    if w.parse_date(a.get("start_date")) is None:
        out.append("start_date must be DD/MM/YYYY (the plan start date in the quote)")
    else:
        m = _any([q], lambda e: e.date("plan start date in the quote", a["start_date"]))
        m and out.append(m)
    _funds_problems(a, [q], out)
    for k, lab, pats in (("net_admin_fee", "net administration fee", [r"net administration fee"]), ("advice_fee", "ongoing advice fee", [r"advice fees?"]),
                         ("adviser_charge", "adviser remuneration account charge", [r"adviser remuneration"])):
        if pct_decimal(a.get(k) or "") is None:
            out.append("%s %r is not a percentage" % (k, a.get(k)))
        else:
            m = _any([q], lambda e: e.exact_percent("%s in the quote" % lab, a[k]))
            m and out.append(m)
            if not m:
                m = _pct_near_any([q], "%s in the quote" % lab, pats, a[k], window=60)
                m and out.append(m)
    mf = w.parse_money(a.get("monthly_admin_fee"))
    if mf is None or mf < 0:
        out.append("monthly_admin_fee %r is not an amount" % a.get("monthly_admin_fee"))
    else:
        m = _any([q], lambda e: e.number("monthly fixed administration fee in the quote", mf))
        m and out.append(m)
        if not m:
            m = _near_any([q], "monthly fixed administration fee in the quote", [r"fixed administration fee"], mf, window=40)
            m and out.append(m)
    if not isinstance(a.get("lump_sum_applies"), bool):
        out.append("lump_sum_applies must be true or false (Paul's answer: a second, separate email is built when it is true)")
    if not out:
        c = tool_context(a)
        if c["max_ra"] <= 0:
            out.append("STOP: the fund contributions already use the whole yearly allowance (the maximum RA is R %s a month): Table 2 has no room. Ask Paul" % money_shown(c["max_ra"]))
    return out


def _lump_problems(a, ev, docs):
    out = []
    lq = ev.get("lump_sum_quote")
    lp = a.get("lump") or {}
    typ = lp.get("type")
    amt = w.parse_money(lp.get("amount"))
    if typ not in ("section14", "voluntary"):
        out.append("lump.type must be 'section14' or 'voluntary' (Paul's answer: never inferred)")
    if amt is None or amt <= 0:
        out.append("lump.amount %r is not an amount" % lp.get("amount"))
    else:
        m = _any([lq], lambda e: e.number("lump sum amount in the Lump Sum Quote", amt))
        m and out.append(m)
    if typ == "section14":
        if set(lp) != {"type", "amount", "policies"}:
            out.append("a Section 14 lump sum needs exactly type, amount, policies")
        pols = lp.get("policies")
        if not isinstance(pols, list) or not pols:
            out.append("lump.policies: at least one source policy, each with name and net_value")
        else:
            tot = Decimal(0)
            for pl in pols:
                if not isinstance(pl, dict) or set(pl) != {"name", "net_value"}:
                    out.append("each source policy needs exactly name and net_value (the NET fund value, never the gross)")
                    continue
                d = w.parse_money(pl["net_value"])
                if d is None or d <= 0:
                    out.append("policy %r: net_value %r is not an amount" % (pl["name"], pl["net_value"]))
                    continue
                tot += d
                evs = [ev.get("client_overview"), ev.get("astute_ccp")]
                if not any(r in docs["docs"] for r in ("client_overview", "astute_ccp")):
                    out.append("a Section 14 lump sum needs the Client Overview or the Astute report registered (the net fund values)")
                else:
                    m = _any(evs, lambda e: e.number("net fund value of %s" % pl["name"], d))
                    m and out.append(m)
                    if not m:
                        m = _near_any(evs, "net fund value of %s" % pl["name"], [r"net fund value"], d, window=40)
                        m and out.append(m)
                    m = _any(evs, lambda e: e.name("source policy name", pl["name"]))
                    m and out.append(m)
            if amt is not None and tot != amt:
                out.append("the lump sum amount R %s is not the sum of the source policies' net fund values (R %s)" % (money_shown(amt), money_shown(tot)))
    elif typ == "voluntary":
        if set(lp) != {"type", "amount", "source_of_funds", "tax_note"}:
            out.append("a voluntary lump sum needs exactly type, amount, source_of_funds, tax_note")
        if len(str(lp.get("source_of_funds") or "").strip()) < 3:
            out.append("lump.source_of_funds is missing (Paul's answer)")
        if len(str(lp.get("tax_note") or "").strip()) < 20:
            out.append("STOP: a voluntary lump sum has no approved tax-treatment wording: ask Paul for the note and enter it in lump.tax_note in his words (never invented)")
    if w.parse_date(a.get("start_date")) is None:
        out.append("start_date must be DD/MM/YYYY (the Plan 2 start date in the Lump Sum Quote)")
    else:
        m = _any([lq], lambda e: e.date("Plan 2 start date in the Lump Sum Quote", a["start_date"]))
        m and out.append(m)
    _funds_problems(a, [lq], out, "Lump Sum Quote")
    fe = a.get("ls_fees")
    if not isinstance(fe, dict) or set(fe) != {"admin_fee", "advice_fee", "as_and_when"}:
        out.append("ls_fees needs exactly admin_fee, advice_fee, as_and_when (copy them as the Lump Sum Quote shows them; 'None' when there is no as-and-when fee)")
    else:
        for k in ("admin_fee", "advice_fee", "as_and_when"):
            val = str(fe[k]).strip()
            if not val:
                out.append("ls_fees.%s is empty" % k)
                continue
            if val.lower() == "none" and k == "as_and_when":
                continue
            toks = re.findall(r"(\d+(?:[.,]\d+)?)\s*%", val)
            if not toks:
                out.append("ls_fees.%s %r must show its percentage(s), for example 0.575%%" % (k, val))
            pats = {"admin_fee": [r"administration fee"], "advice_fee": [r"advice fees?"], "as_and_when": [r"as.and.when"]}[k]
            for t in toks:
                m = _any([lq], lambda e: e.exact_percent("ls_fees.%s in the Lump Sum Quote" % k, t))
                m and out.append(m)
                if not m:
                    m = _pct_near_any([lq], "ls_fees.%s in the Lump Sum Quote" % k, pats, t, window=60)
                    m and out.append(m)
    return out
