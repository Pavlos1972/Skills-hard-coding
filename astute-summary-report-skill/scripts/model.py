#!/usr/bin/env python3
"""The data model of the Astute summary: validation, which section a policy goes in, the flags, the totals, and the composed content.

Everything here is a pure function of what was entered (data.json), the product records and the judgement flags, so the checker can recompute
it and refuse a content.json that was edited by hand. Fixed by Paul's rules (the old skill, kept) and his answers of 03/11/2026.
"""
import re
from decimal import Decimal

import wrlib as w

RISK_PATTERNS = ("ACI", "ABI", "age-rated", "fixed", "other")
BENEFIT_TYPES = ("stand-alone", "accelerated", "unable")
PROVIDER_RESULTS = ("data", "not_found", "unable_to_match", "no_row")
FREQUENCIES = ("monthly", "annual", "single")
KINDS = ("risk", "investment")
CHAT_FLAG_KINDS = ("status_contradiction", "unknown_product", "wrapper_ambiguity", "bank_arm", "other")
# kind -> (priority: 1 = most important, heading)
FLAG_KINDS = {"status_contradiction": (1, "Status contradiction"), "unknown_product": (2, "Unknown or thinly described product"),
              "wrapper_ambiguity": (3, "RA versus endowment wrapper ambiguity"), "no_data": (4, "Provider returned no data"),
              "zero_missing": (5, "Zero or missing value"), "total_mismatch": (6, "Total does not match the report"),
              "unconfirmed": (7, "Product not confirmed online"), "bank_arm": (8, "Policy held with a bank's insurance arm"), "other": (9, "Other")}
MAX_DESC_WORDS = 30
HEADER_KEYS = ("client_name", "id_number", "date_of_birth", "report_reference", "report_date", "requested_by")
POLICY_KEYS = {"provider", "policy_number", "product_name", "status", "start_date", "kind", "owner", "life_assured", "premium_payer", "beneficiaries",
               "benefits", "premium", "premium_frequency", "premium_pattern", "pattern_text", "values", "fund_allocation", "note"}
CESSION_NOTE = ("Cession status is not held in Astute's data, so this summary does not state whether any policy is or is not ceded. "
                "Verify cession status directly with the insurer, in particular for any policy held with a bank's insurance arm.")
NOT_FOUND_WORDS = {"not_found": "client record not found", "unable_to_match": "unable to match", "no_row": "no row returned"}


# ------------------------------------------------------------------ validation
def _money_problem(label, v, allow_empty=True):
    if v in (None, ""):
        return None if allow_empty else "%s is missing" % label
    return None if w.parse_money(v) is not None else "%s: %r is not an amount" % (label, v)


def schema_problems(data):
    """Problems with the entered data (empty = fine). These are the program's refusals."""
    out = []
    h = data.get("header")
    if not isinstance(h, dict):
        return ["the 'header' block is missing"]
    for k in HEADER_KEYS:
        if not str(h.get(k) or "").strip():
            out.append("header.%s is missing" % k)
    if h.get("report_date") and w.parse_date(h["report_date"]) is None:
        out.append("header.report_date %r is not a date (DD/MM/YYYY)" % h["report_date"])
    if h.get("date_of_birth") and w.parse_date(h["date_of_birth"]) is None:
        out.append("header.date_of_birth %r is not a date (DD/MM/YYYY)" % h["date_of_birth"])
    provs = data.get("providers") or []
    if not provs:
        out.append("providers is empty: list EVERY provider block in the report, including 'client record not found' ones")
    names = {}
    for p in provs:
        if p.get("result") not in PROVIDER_RESULTS:
            out.append("provider %r: result must be one of %s" % (p.get("name"), ", ".join(PROVIDER_RESULTS)))
        names[w.norm(p.get("name", ""))] = p.get("result")
    pols = data.get("policies") or []
    seen = set()
    for i, p in enumerate(pols, 1):
        tag = "policy %d (%s)" % (i, p.get("policy_number") or "no number")
        for k in set(p) - POLICY_KEYS:
            out.append("%s: unknown field %r" % (tag, k))
        for k in ("provider", "policy_number", "product_name", "status"):
            if not str(p.get(k) or "").strip():
                out.append("%s: %s is missing" % (tag, k))
        key = (w.norm(p.get("provider", "")), re.sub(r"[^0-9a-z]", "", str(p.get("policy_number", "")).lower()))
        if key in seen:
            out.append("%s: listed twice" % tag)
        seen.add(key)
        if w.norm(p.get("provider", "")) not in names:
            out.append("%s: provider %r is not in the providers list" % (tag, p.get("provider")))
        elif names[w.norm(p["provider"])] != "data":
            out.append("%s: provider %r returned no data, so it cannot have policies" % (tag, p["provider"]))
        if p.get("kind") not in KINDS:
            out.append("%s: kind must be risk or investment" % tag)
        if p.get("premium_pattern") not in RISK_PATTERNS:
            out.append("%s: premium_pattern must be one of %s" % (tag, ", ".join(RISK_PATTERNS)))
        if p.get("start_date") and w.parse_date(p["start_date"]) is None:
            out.append("%s: start_date %r is not DD/MM/YYYY (leave it empty if the report does not show it)" % (tag, p["start_date"]))
        if p.get("premium") not in (None, "") and p.get("premium_frequency") not in FREQUENCIES:
            out.append("%s: premium_frequency must be one of %s" % (tag, ", ".join(FREQUENCIES)))
        m = _money_problem(tag + " premium", p.get("premium"))
        if m:
            out.append(m)
        for b in p.get("beneficiaries") or []:
            if not b.get("name"):
                out.append("%s: a beneficiary has no name" % tag)
        if p.get("kind") == "risk":
            bens = p.get("benefits") or []
            if not bens:
                out.append("%s: a risk policy needs at least one benefit" % tag)
            for b in bens:
                if not b.get("name"):
                    out.append("%s: a benefit has no name" % tag)
                if b.get("type") not in BENEFIT_TYPES:
                    out.append("%s: benefit %r must be labelled stand-alone, accelerated or unable (unable = report does not allow it)" % (tag, b.get("name")))
                m = _money_problem("%s benefit %r cover" % (tag, b.get("name")), b.get("cover_amount"))
                if m:
                    out.append(m)
        if p.get("kind") == "investment":
            vals = p.get("values")
            if not isinstance(vals, dict) or "fund_value" not in vals:
                out.append("%s: an investment needs values with at least fund_value (an empty string if the report does not show it)" % tag)
            else:
                for k, v in vals.items():
                    for kk, vv in (v.items() if isinstance(v, dict) else [(k, v)]):
                        m = _money_problem("%s %s" % (tag, kk), vv)
                        if m:
                            out.append(m)
            for f in p.get("fund_allocation") or []:
                if not f.get("fund"):
                    out.append("%s: a fund allocation has no fund name" % tag)
    s2 = data.get("section2")
    if not isinstance(s2, dict) or not all(isinstance(s2.get(k), dict) and isinstance(s2[k].get("reflected"), bool) for k in ("group_risk", "retirement_fund")):
        out.append("section2 needs group_risk and retirement_fund, each with reflected true or false (and details if true)")
    else:
        for k in ("group_risk", "retirement_fund"):
            if s2[k]["reflected"] and not s2[k].get("details"):
                out.append("section2.%s is reflected but has no details" % k)
    for k, v in (data.get("report_totals") or {}).items():
        if k not in ("monthly_premiums", "fund_value"):
            out.append("report_totals.%s: only monthly_premiums and fund_value are accepted" % k)
        elif w.parse_money(v) is None:
            out.append("report_totals.%s: %r is not an amount" % (k, v))
    return out


# ------------------------------------------------------------------ sections, totals, products
def section_of(p):
    """Only a policy Astute labels paid-up goes in Section 3; lapsed, surrendered and anything not active go in Additional Notes."""
    s = w.norm(p.get("status", ""))
    if re.search(r"\bpaid up\b|\bpaidup\b", s):
        return "paid_up"
    if re.search(r"lapse|surrender|inactive|cancel|terminat|matur|expire|declin|claim|not taken", s):
        return "inactive"
    if re.search(r"\b(active|in force|premium paying|paying)\b", s):
        return "active"
    return "unrecognised"


def total_amounts(data):
    """Added up from the entries (never typed): monthly premiums and fund values of the ACTIVE policies."""
    prem, fund = Decimal("0.00"), Decimal("0.00")
    for p in data.get("policies") or []:
        if section_of(p) != "active":
            continue
        if p.get("premium") not in (None, "") and p.get("premium_frequency") == "monthly":
            prem += w.parse_money(p["premium"]) or Decimal("0.00")
        if p.get("kind") == "investment":
            fund += w.parse_money((p.get("values") or {}).get("fund_value")) or Decimal("0.00")
    return {"monthly_premiums": prem, "fund_value": fund}


def product_names(data):
    seen, out = set(), []
    for p in data.get("policies") or []:
        n = w.norm(p.get("product_name", ""))
        if n and n not in seen:
            seen.add(n)
            out.append(p["product_name"].strip())
    return out


def product_problems(data, products):
    out = []
    for n in product_names(data):
        r = products.get(w.norm(n))
        if not r:
            out.append("product %r has no record: run.py product --name ... (with a source) or --unconfirmed" % n)
        elif r.get("state") == "described":
            if not str(r.get("source") or "").startswith(("http://", "https://")):
                out.append("product %r: the source must be a web address" % n)
            if not (r.get("desc") or "").strip() or len(r["desc"].split()) > MAX_DESC_WORDS:
                out.append("product %r: the description must be 1 to %d words" % (n, MAX_DESC_WORDS))
        elif r.get("state") != "unconfirmed":
            out.append("product %r: unknown state" % n)
    return out


def description(products, name):
    r = products.get(w.norm(name)) or {}
    if r.get("state") == "described":
        return r["desc"].strip()
    return "Not confirmed online. Described only as named in the report."


# ------------------------------------------------------------------ flags
def _zero_or_missing(v):
    d = w.parse_money(v) if v not in (None, "") else None
    return d is None or d <= 0


def computed_flags(data, products):
    """The orange flags the program can decide itself."""
    out = []
    for pr in data.get("providers") or []:
        if pr["result"] != "data":
            out.append({"kind": "no_data", "provider": pr["name"], "policy": "",
                        "text": "Astute shows '%s' for %s. A provider that returned no data is not proof of no cover: verify directly with the insurer." % (NOT_FOUND_WORDS[pr["result"]], pr["name"])})
    for p in data.get("policies") or []:
        sec, num = section_of(p), p["policy_number"]
        miss = []
        if p["kind"] == "risk":
            miss += ["cover for %s" % b.get("name") for b in p.get("benefits") or [] if _zero_or_missing(b.get("cover_amount"))]
        else:
            for k, v in (p.get("values") or {}).items():
                for kk, vv in (v.items() if isinstance(v, dict) else [(k, v)]):
                    if _zero_or_missing(vv):
                        miss.append(kk.replace("_", " "))
        if p.get("premium") not in (None, "") and _zero_or_missing(p["premium"]):
            miss.append("premium")
        if not p.get("start_date"):
            miss.append("start date")
        if miss:
            out.append({"kind": "zero_missing", "provider": p["provider"], "policy": num,
                        "text": "Policy %s: the report shows zero or no value for %s. Treated as absent data to verify with the insurer, not as a real zero." % (num, ", ".join(miss))})
        if p["kind"] == "investment" and sec not in ("paid_up", "inactive") and _zero_or_missing((p.get("values") or {}).get("fund_value")):
            out.append({"kind": "zero_missing", "provider": p["provider"], "policy": num,
                        "text": "Policy %s has zero or no fund value but Astute does not label it paid-up, so it is NOT shown as paid-up." % num})
        if sec == "unrecognised":
            out.append({"kind": "other", "provider": p["provider"], "policy": num,
                        "text": "Policy %s: the status '%s' is not recognised, so it is shown under Additional Notes. Verify the status." % (num, p["status"])})
    for n in product_names(data):
        if (products.get(w.norm(n)) or {}).get("state") == "unconfirmed":
            prov = next(p["provider"] for p in data["policies"] if w.norm(p["product_name"]) == w.norm(n))
            out.append({"kind": "unconfirmed", "provider": prov, "policy": "", "product": n, "text": "Product '%s' could not be confirmed online. Its description is only what the report says." % n})
    tot = total_amounts(data)
    for k, label in (("monthly_premiums", "monthly premiums"), ("fund_value", "fund value")):
        given = (data.get("report_totals") or {}).get(k)
        if given not in (None, "") and w.parse_money(given) != tot[k]:
            out.append({"kind": "total_mismatch", "provider": "", "policy": "",
                        "text": "The report shows total %s %s but the entries add up to %s." % (label, w.fmt_money(w.parse_money(given)), w.fmt_money(tot[k]))})
    return out


def all_flags(data, products, chat_flags):
    flags = computed_flags(data, products) + [dict(f) for f in chat_flags]
    for p in data.get("policies") or []:
        if p.get("bank_insurance_arm") is True:
            flags.append({"kind": "bank_arm", "provider": p["provider"], "policy": p["policy_number"],
                          "text": "Policy %s is held with a bank's insurance arm: verify cession status directly with the insurer." % p["policy_number"]})
    flags.sort(key=lambda f: (FLAG_KINDS[f["kind"]][0], f.get("provider", ""), f.get("policy", ""), f["text"]))
    for i, f in enumerate(flags, 1):
        f["n"] = i
    return flags


def flag_problems(data, chat_flags):
    out = []
    pols = {w.norm(p["policy_number"]) for p in data.get("policies") or []}
    for f in chat_flags:
        if f.get("kind") not in CHAT_FLAG_KINDS:
            out.append("flag kind %r: must be one of %s" % (f.get("kind"), ", ".join(CHAT_FLAG_KINDS)))
        if len((f.get("text") or "").strip()) < 8:
            out.append("a flag needs its reason in words (at least 8 characters)")
        if f.get("policy") and w.norm(f["policy"]) not in pols:
            out.append("flag names policy %r, which is not in the data" % f["policy"])
    return out


# ------------------------------------------------------------------ composed content
def _m(v):
    d = w.parse_money(v) if v not in (None, "") else None
    return w.fmt_money(d) if d is not None else "Not shown"


def _party_line(p):
    bits = []
    for label, k in (("Owner", "owner"), ("Life assured", "life_assured"), ("Premium payer", "premium_payer")):
        if p.get(k):
            bits.append("%s: %s" % (label, p[k]))
    if p.get("beneficiaries"):
        bits.append("Beneficiaries: " + ", ".join("%s (%s%%)" % (b["name"], w.fmt_pct(b["percent"]) if b.get("percent") else "no ") for b in p["beneficiaries"]))
    return " | ".join(bits)


def policy_view(p, products):
    start = ("Start: " + p["start_date"]) if p.get("start_date") else "Start date not shown"
    base = {"number": p["policy_number"], "product": p["product_name"].strip(), "desc": description(products, p["product_name"]), "status": [p["status"].strip(), start],
            "parties": _party_line(p), "note": (p.get("note") or "").strip(), "kind": p["kind"]}
    pattern = p["premium_pattern"] + ((" - " + p["pattern_text"].strip()) if p.get("pattern_text") else "")
    if p["kind"] == "risk":
        base["benefits"] = ["%s: %s" % (b["name"], _m(b.get("cover_amount"))) for b in p["benefits"]]
        base["types"] = [{"stand-alone": "Stand-alone", "accelerated": "Accelerated", "unable": "Unable to determine - verify with insurer"}[b["type"]] for b in p["benefits"]]
        base["premium"] = ["%s (%s)" % (_m(p.get("premium")), p.get("premium_frequency") or "frequency not shown"), "Pattern: " + pattern]
    else:
        v = p.get("values") or {}
        lines = []
        for k, label in (("premiums_paid", "Premiums paid"), ("fund_value", "Fund value"), ("surrender_value", "Surrender value")):
            if k in v:
                lines.append("%s: %s" % (label, _m(v[k])))
        for k, vv in v.items():
            if isinstance(vv, dict):
                lines += ["Two-Pot %s: %s" % (kk, _m(x)) for kk, x in vv.items()]
        base["values"] = lines or ["Values not shown"]
        base["pattern"] = [pattern] + (["Premium: %s (%s)" % (_m(p.get("premium")), p.get("premium_frequency"))] if p.get("premium") not in (None, "") else [])
        base["funds"] = ["%s: %s%%" % (f["fund"], w.fmt_pct(f["percent"]) if f.get("percent") else "no ") for f in p.get("fund_allocation") or []] or ["Allocation not shown"]
    return base


def _groups(data, products, flags, sections, kind=None):
    """[{provider, flags, policies}] in the order the providers appear in the report. A flag sits above the table of the policy (or product) it is about."""
    out = []
    for pr in data["providers"]:
        pols = [p for p in data["policies"] if w.norm(p["provider"]) == w.norm(pr["name"]) and section_of(p) in sections and (kind is None or p["kind"] == kind)]
        if not pols:
            continue
        nums = {w.norm(p["policy_number"]) for p in pols}
        prods = {w.norm(p["product_name"]) for p in pols}
        fl = [f for f in flags if (f.get("policy") and w.norm(f["policy"]) in nums) or (f.get("product") and w.norm(f["product"]) in prods)]
        out.append({"provider": pr["name"], "flags": [{"n": f["n"], "title": FLAG_KINDS[f["kind"]][1], "text": f["text"]} for f in fl],
                    "policies": [policy_view(p, products) for p in pols]})
    return out


def compose(data, products, chat_flags, client_name):
    h = data["header"]
    first, _, surname = client_name.partition(" ")
    flags = all_flags(data, products, chat_flags)
    tot = total_amounts(data)
    s2 = data["section2"]
    rows = []
    for key, label in (("group_risk", "Group Risk cover"), ("retirement_fund", "Pension or Provident Fund")):
        r = s2[key]
        rows.append({"category": label, "reflected": "Yes" if r["reflected"] else "No",
                     "details": list(r.get("details") or []) if r["reflected"] else ["Not reflected on the Astute report."]})
    gen = [CESSION_NOTE]
    missing = [pr["name"] for pr in data["providers"] if pr["result"] != "data"]
    gen.append(("Providers that returned no data (not found, unable to match or no row): %s." % ", ".join("%s (%s)" % (m["name"], NOT_FOUND_WORDS[m["result"]]) for m in data["providers"] if m["result"] != "data"))
               if missing else "Every provider on the report returned data.")
    gen.append("Totals for active policies, added up from the entries above (not typed): monthly premiums %s; fund value %s." % (w.fmt_money(tot["monthly_premiums"]), w.fmt_money(tot["fund_value"])))
    name_line = h["client_name"] + ((" (Astute holds the name: %s)" % h["astute_name"]) if h.get("astute_name") and w.norm(h["astute_name"]) != w.norm(h["client_name"]) else "")
    return {
        "file_name": w.output_name(first, surname, h["report_date"]),
        "title": "Astute Report Summary",
        "header_lines": ["Client: " + name_line, "ID number: %s   |   Date of birth: %s" % (h["id_number"], h["date_of_birth"]),
                         "Report reference: %s   |   Report date: %s" % (h["report_reference"], h["report_date"]), "Requested by: " + h["requested_by"]],
        "intro": ("Product descriptions were cross-checked against the insurers' own public product information where a source could be found; products that could not be "
                  "confirmed are flagged. Every figure comes from the Astute report. Orange flags need verification."),
        "s1_risk": _groups(data, products, flags, ("active",), "risk"),
        "s1_invest": _groups(data, products, flags, ("active",), "investment"),
        "s2_rows": rows,
        "s3": _groups(data, products, flags, ("paid_up",)),
        "additional": _groups(data, products, flags, ("inactive", "unrecognised")),
        "general": gen,
        "general_flags": [{"n": f["n"], "title": FLAG_KINDS[f["kind"]][1], "text": f["text"]} for f in flags if not f.get("policy") and not f.get("product")],
        "flags": [{"n": f["n"], "title": FLAG_KINDS[f["kind"]][1], "text": f["text"]} for f in flags],
        "footer": "Astute Report Summary - %s - Confidential" % h["client_name"],
        "policy_numbers": [p["policy_number"] for p in data["policies"]],
        "headings": ["Section 1: Active Policies - Personal Risk Covers and Investments", "Section 2: Group Risk and Retirement Funds", "Section 3: Paid-Up Policies",
                     "Additional Notes: Inactive, Lapsed or Surrendered Policies", "General Verification Notes"],
    }
