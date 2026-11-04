#!/usr/bin/env python3
"""The domain model of the investment comparison: the answers (every figure checked against the right document's text), the fund fact sheets (saved text, checked), the
apples-to-apples comparison of the quotes, the fee totals, the Tax-Free room, the stale and missing fact sheets, the flags.

Everything here is a pure function of the answers (answers.json), the declared funds (state.json) and the registered documents, so the checker can recompute it and refuse a
file edited by hand. Rules are Paul's (the old skill, kept) and his answers of 04/11/2026. Nothing here sends anything.
"""
import calendar
import html
import json
import os
import re
from decimal import ROUND_HALF_UP, Decimal

import docread
import wrlib as w

ASSETS = os.path.join(w.SKILL_DIR, "assets")
TEMPLATE = os.path.join(ASSETS, "Investment_Comparison_Email_TEMPLATE.html")
SETTINGS = os.path.join(ASSETS, "settings.json")
WORDING = os.path.join(ASSETS, "wording.json")
TERMS = os.path.join(ASSETS, "plain_terms.json")
FACTS = os.path.join(ASSETS, "tax_facts.json")

CC_NAME = "Sitamah Nathoo"
CC_EMAIL = "admin@liferisk.co.za"
SITAMAH_CHAT = "19:bd2a130a-35d9-459e-9025-55f356810236_e6901cee-de73-46d9-88a5-5e4a1c296418@unq.gbl.spaces"
CHAT_LABEL = "(1:1 Chat) Paul Kafentzis, Sitamah Nathoo"

PRODUCTS = ("RA", "TFSA", "Endowment", "Living Annuity")
PRODUCT_WORDS = {"RA": ["retirement annuity"], "TFSA": ["tax free", "tfsa"], "Endowment": ["endowment"], "Living Annuity": ["living annuity"]}
MIN_PROVIDERS, MAX_PROVIDERS = 2, 6
ROLES = ("quote", "fact_find", "supplement", "tfsa_statement", "factsheet")
LABELLED = ("quote", "supplement", "factsheet")
OPTIONAL_ROLES = ("fact_find", "tfsa_statement")
STALE_DAYS = 92
PALETTE = [("#B8860B", "#FBF1DE"), ("#2C3E70", "#E9ECF5"), ("#1B7A72", "#E4F3F1"), ("#6B4C9A", "#EFE7F5"), ("#1565C0", "#E3EFFB"), ("#5D6D7E", "#E9ECEE")]
HOUSE_GOLD, HOUSE_LIGHT, CHARCOAL = "#B08D57", "#F3ECE0", "#1A1A1A"
SOURCE_KEYS = ("personal", "risk", "providers", "fees", "funds", "email", "meetings", "next_meeting")
ANSWER_KEYS = {"client_full_name", "client_first_name", "client_surname", "client_email", "email_source", "email_note", "product_type", "risk_profile", "providers", "fund_sheets",
               "supplement_checks", "extras", "tfsa", "meetings_held", "next_meeting", "plan_folder", "flags", "sources", "conflicts"}
PROVIDER_KEYS = {"name", "product_name", "contribution_type", "contribution", "escalation", "term", "funds", "fee_lines", "initial_fees", "loyalty", "performance_fees", "flexibility"}
PLACEHOLDER = re.compile(r"\[[A-Z][A-Z0-9 _%().,/&#-]*\]")
TEMPLATE_PLACEHOLDERS = ("[DATE AND TIME SENT]", "[CLIENT EMAIL]", "[CC NAME(S)]", "[SUBJECT]", "[CLIENT FIRST NAME]", "[MEETING DATES LIST]", "[PRODUCT NAME]", "[PROVIDERS LIST]", "[THINGS TO KNOW]",
                         "[TABLE1 TITLE]", "[TABLE1 INTRO]", "[TABLE1]", "[TABLE2 INTRO]", "[TABLE2]", "[FEE NOTES]", "[TABLE3 INTRO]", "[TABLE3]", "[FUND NOTES]", "[TABLE4 INTRO]",
                         "[LOYALTY EXPLANATIONS]", "[TABLE4]", "[EXTRAS]", "[NEXT MEETING LINE]")
TEMPLATE_MARKERS = ("BODY", "LOGO")
EAC_TITLE = "Total Ongoing Fees – Per Annum (Excluding EAC)"


def settings():
    with open(SETTINGS, encoding="utf-8") as f:
        return json.load(f)


def wording():
    with open(WORDING, encoding="utf-8") as f:
        return json.load(f)


def terms():
    with open(TERMS, encoding="utf-8") as f:
        return json.load(f)


def facts():
    with open(FACTS, encoding="utf-8") as f:
        return json.load(f)


def D(x):
    return x if isinstance(x, Decimal) else Decimal(str(x))


# ------------------------------------------------------------------ keys and roles
def slug(s):
    return re.sub(r"[^a-z0-9]+", "_", str(s).lower()).strip("_")


def dkey(role, label=None):
    return "%s_%s" % (role, slug(label)) if role in LABELLED else role


def valid_role(role):
    return role in ROLES


def can_be_missing(role):
    return role in OPTIONAL_ROLES or role == "factsheet"


def sheet_label(provider, fund):
    return "%s - %s" % (provider.strip(), fund.strip())


def declared_funds(state):
    return list((state or {}).get("funds") or [])


def served_keys_order(docs):
    """The registered documents in the order they are read: quotes, fact find, supplements, TFSA statement, fund sheets."""
    out = []
    for role in ROLES:
        out += sorted(k for k, d in docs["docs"].items() if d.get("role") == role)
    return out


def docs_of(docs, role):
    return {d["label"]: k for k, d in docs["docs"].items() if d.get("role") == role}


# ------------------------------------------------------------------ values
def money_shown(v):
    d = w.parse_money(v) if not isinstance(v, Decimal) else v
    if d is None:
        return str(v)
    cents = bool(re.search(r"[.,]\d{2}\s*$", str(v).strip())) or d != d.to_integral_value()
    return format(d, ",.2f") if cents else format(int(d), ",d")


def rand_whole(v):
    return "R " + format(int(D(v).quantize(Decimal("1"), rounding=ROUND_HALF_UP)), ",d")


def pct_digits(v):
    return str(v).replace("%", "").strip().replace(" ", "").replace(",", ".")


def pct_decimal(v):
    s = pct_digits(v)
    return Decimal(s) if re.fullmatch(r"[+-]?\d+(?:\.\d+)?", s) else None


def fee_shown(d):
    d = D(d).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)
    s = format(d, "f")
    return s[:-1] if s.endswith("0") else s


def names_list(names, amp="&"):
    nm = list(names)
    return nm[0] if len(nm) == 1 else ", ".join(nm[:-1]) + " " + amp + " " + nm[-1]


def fmt_date_with_day(d):
    return "%s, %s" % (calendar.day_name[d.weekday()], d.strftime("%d/%m/%Y"))


def meetings_line(a):
    parts = [fmt_date_with_day(d) for d in sorted(w.parse_date(x) for x in a["meetings_held"])]
    return parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " & " + parts[-1]


def next_date(a):
    return w.parse_date(a["next_meeting"]["date"])


def next_line(a):
    return "%s @ %s" % (fmt_date_with_day(next_date(a)), a["next_meeting"]["time"].strip())


def provider_names(a):
    return [p["name"].strip() for p in a["providers"]]


def subject(a):
    return html.unescape(wording()["subject"].format(name=a["client_full_name"].strip(), product=wording()["product_titles"][a["product_type"]].replace(" Comparison", ""),
                                                      providers=" vs ".join(provider_names(a))))


def sent_text(clock):
    return "%s, %s %s" % (calendar.day_name[clock.weekday()], clock.strftime("%d/%m/%Y"), clock.strftime("%H:%M"))


def file_name(a, d):
    first = a["client_first_name"].strip().replace(" ", "_")
    sur = a["client_surname"].strip().replace(" ", "_")
    return w.safe_filename("%s_%s_Investment_Comparison_Email - %s" % (first, sur, d.strftime("%d.%m.%y"))) + ".html"


def greeting_for(clock, used_today):
    if used_today:
        return "Hi"
    return "Good morning" if clock.hour < 12 else ("Good afternoon" if clock.hour < 18 else "Good evening")


def no_ext(name):
    return name[:-4] if name.lower().endswith((".pdf", ".txt")) else name


def doc_name(docs, key):
    return docs["docs"][key]["name"]


def tfsa_limits():
    """(annual, lifetime, confirmed)."""
    t = facts()["tfsa"]
    return w.parse_money(t["annual_limit"]), w.parse_money(t["lifetime_limit"]), bool(t.get("confirmed"))


def label_regex(label):
    return r"\s+".join(re.escape(x) for x in str(label).split())


# ------------------------------------------------------------------ evidence helpers
def _has(e):
    return e is not None and e.has_text


def _any(evs, fn):
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
    hits = [m.end() for p in pats for m in re.finditer(p, e.flat, re.I)]
    if not hits:
        return "NOLABEL"
    t = pct_digits(tok).lstrip("+-")
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


def _exact_pct(e, label, v):
    return e.exact_percent(label, pct_digits(v).lstrip("+-"))


def verbatim_run(desc, text, n=8):
    """True when the description repeats n or more words in a row from the document's text (Paul's rule: fund descriptions are in our own words)."""
    tok = w.norm(desc).split()
    hay = " " + w.norm(text) + " "
    return any((" " + " ".join(tok[i:i + n]) + " ") in hay for i in range(0, max(0, len(tok) - n + 1)))


# ------------------------------------------------------------------ validation
def _common(a, ev, docs, today, run_client, out):
    for k in set(a) - ANSWER_KEYS:
        out.append("unknown field %r" % k)
    for k in ("client_full_name", "client_first_name", "client_surname", "plan_folder", "client_email"):
        if not str(a.get(k) or "").strip():
            out.append("%s is missing" % k)
    if run_client and w.norm("%s %s" % (a.get("client_first_name", ""), a.get("client_surname", ""))) != w.norm(run_client):
        out.append("the everyday name is not the client Paul named (%s)" % run_client)
    if w.norm(a.get("client_surname", "")) not in w.norm(a.get("client_full_name", "")):
        out.append("the surname must be part of the client's full name")
    if a.get("conflicts"):
        out.append("%d unresolved conflict(s) between sources: STOP and ask Paul, quoting both values and their sources" % len(a["conflicts"]))
    keys = list(SOURCE_KEYS) + (["tfsa"] if a.get("product_type") == "TFSA" else []) + (["supplement"] if docs_of(docs, "supplement") else [])
    srcs = a.get("sources") or {}
    for k in keys:
        if len(str(srcs.get(k) or "").strip()) < 3:
            out.append("sources.%s: every answer needs its source (a document or Paul's words)" % k)
    if not isinstance(a.get("flags"), list) or not all(isinstance(x, str) for x in a.get("flags", [])):
        out.append("flags must be a list of short sentences (empty list if there is nothing to flag)")
    ff = ev.get("fact_find")
    if "fact_find" not in docs["docs"] and not (docs["missing"].get("fact_find") or "").strip():
        out.append("the client's Fact Find: register it, or record with Paul's words that there is none (run.py doc --missing fact_find --said ...)")
    em = str(a.get("client_email") or "").strip()
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", em):
        out.append("client_email %r is not an email address" % em)
    elif a.get("email_source") == "fact_find":
        if _has(ff) and em.lower() not in ff.text.lower():
            out.append("client_email is not in the Fact Find's text (email_source says it is)")
    elif a.get("email_source") == "other":
        if len(str(a.get("email_note") or "").strip()) < 10:
            out.append("client_email from another source: say which (Fact Find Summary, Zapier contact lookup, Outlook search) in email_note")
    else:
        out.append("email_source must be 'fact_find' or 'other' (with email_note)")
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
    if _has(ff):
        m = ff.name("client name in the Fact Find", a.get("client_full_name"))
        m and out.append(m)
        rp = str(a.get("risk_profile") or "").strip()
        if rp:
            m = ff.name("risk profile in the Fact Find", rp)
            m and out.append(m)
    if not str(a.get("risk_profile") or "").strip():
        out.append("risk_profile is missing (read it from the client's Fact Find; ask Paul only if the Fact Find does not show it)")


def _provider_problems(p, i, a, ev, docs, state, out):
    name = str(p.get("name") or "").strip()
    pre = "provider %d (%s)" % (i + 1, name or "?")
    if set(p) - PROVIDER_KEYS or not name:
        out.append("%s: unknown or missing field(s) %s" % (pre, sorted(set(p) - PROVIDER_KEYS) or "name"))
        return
    qk = dkey("quote", name)
    if qk not in docs["docs"]:
        out.append("%s: its quote must be registered first (run.py doc --role quote --label %r)" % (pre, name))
        return
    q = ev.get(qk)
    # the product type: the quote must say so
    words = PRODUCT_WORDS[a["product_type"]]
    if _has(q) and not any(x in q.norm for x in words):
        out.append("%s: the quote does not say it is a %s (none of %s is in its text): never compare different product types" % (pre, a["product_type"], ", ".join(repr(x) for x in words)))
    if str(p.get("product_name") or "").strip():
        m = _any([q], lambda e: e.name("%s product name in the quote" % pre, p["product_name"]))
        m and out.append(m)
    else:
        out.append("%s: product_name is missing (the quote's own words)" % pre)
    ct = p.get("contribution_type")
    if ct not in ("recurring", "lump_sum"):
        out.append("%s: contribution_type must be 'recurring' or 'lump_sum'" % pre)
    amt = w.parse_money(p.get("contribution"))
    if amt is None or amt <= 0:
        out.append("%s: contribution %r is not an amount" % (pre, p.get("contribution")))
    else:
        m = _any([q], lambda e: e.number("%s contribution in the quote" % pre, amt))
        m and out.append(m)
        if not m:
            m = _near_any([q], "%s contribution in the quote" % pre, [r"premium", r"contribution", r"lump sum", r"investment amount"], amt, window=80)
            m and out.append(m)
    esc = str(p.get("escalation") or "").strip()
    if ct == "lump_sum" and esc.lower() != "none":
        out.append("%s: a lump sum has no yearly increase: escalation must be 'None'" % pre)
    elif esc.lower() != "none":
        if pct_decimal(esc) is None:
            out.append("%s: escalation %r is not a percentage or 'None'" % (pre, esc))
        else:
            m = _any([q], lambda e: _exact_pct(e, "%s yearly increase in the quote" % pre, esc))
            m and out.append(m)
    term = str(p.get("term") or "").strip()
    if not term:
        out.append("%s: term is missing ('Not applicable' when the product has none)" % pre)
    elif term.lower() not in ("not applicable", "n/a"):
        m = _any([q], lambda e: e.name("%s term or retirement age in the quote" % pre, term))
        m and out.append(m)
    # funds
    fs = p.get("funds")
    if not isinstance(fs, list) or not fs:
        out.append("%s: funds: at least one fund, each with name, allocation and asset_mgmt_fee" % pre)
        fs = []
    tot, seen = Decimal(0), set()
    for f in fs:
        if not isinstance(f, dict) or set(f) != {"name", "allocation", "asset_mgmt_fee"} or not str(f.get("name") or "").strip():
            out.append("%s: each fund needs exactly name, allocation and asset_mgmt_fee" % pre)
            return
        alloc, fee = pct_decimal(f["allocation"]), pct_decimal(f["asset_mgmt_fee"])
        if alloc is None or alloc <= 0 or fee is None:
            out.append("%s: fund %r: allocation and asset_mgmt_fee must be numbers" % (pre, f["name"]))
            continue
        if w.norm(f["name"]) in seen:
            out.append("%s: fund %r is listed twice" % (pre, f["name"]))
        seen.add(w.norm(f["name"]))
        tot += alloc
        m = _any([q], lambda e: e.name("fund in the %s quote" % name, f["name"]))
        m and out.append(m)
        m = _any([q], lambda e: e.number("allocation of %s in the %s quote" % (f["name"], name), alloc))
        m and out.append(m)
        pat = [label_regex(f["name"])]
        if not m:
            m = _near_any([q], "allocation of %s in the %s quote" % (f["name"], name), pat, alloc, window=160)
            m and out.append(m)
        m = _any([q], lambda e: _exact_pct(e, "asset management fee of %s in the %s quote" % (f["name"], name), f["asset_mgmt_fee"]))
        m and out.append(m)
        if not m:
            m = _pct_near_any([q], "asset management fee of %s in the %s quote" % (f["name"], name), pat, f["asset_mgmt_fee"], window=120)
            m and out.append(m)
        if state is not None and not any(w.norm(d["name"]) == w.norm(f["name"]) and w.norm(d["provider"]) == w.norm(name) for d in declared_funds(state)):
            out.append("%s: fund %r was not declared (run.py funds) and so has no fact sheet step" % (pre, f["name"]))
    if fs and tot != 100:
        out.append("%s: the allocations add up to %s%%, not 100%%" % (pre, tot))
    # fee lines: the quote's own breakdown, never a blended total only
    lines = p.get("fee_lines")
    if not isinstance(lines, list) or not lines:
        out.append("%s: fee_lines: the quote's fee breakdown is needed (a quote that shows only EAC or one blended cost is refused: ask Paul for the fee schedule or fund fact sheet)" % pre)
        lines = []
    glossary = terms()["fee_labels"]
    for ln in lines:
        if not isinstance(ln, dict) or not {"label", "pct"} <= set(ln) or set(ln) - {"label", "pct", "plain"}:
            out.append("%s: each fee line needs label and pct (plain only when the label is not in assets/plain_terms.json)" % pre)
            continue
        lab = str(ln["label"]).strip()
        if re.search(r"\beac\b|effective annual cost|^total", lab, re.I):
            out.append("%s: fee line %r is a blended or total figure: only the separate fees are entered (the total is added up by the program)" % (pre, lab))
            continue
        if pct_decimal(ln["pct"]) is None:
            out.append("%s: fee line %r: pct %r is not a percentage" % (pre, lab, ln["pct"]))
            continue
        m = _any([q], lambda e: e.name("fee label %r in the %s quote" % (lab, name), lab))
        m and out.append(m)
        m = _any([q], lambda e: _exact_pct(e, "%s %s in the quote" % (name, lab), ln["pct"]))
        m and out.append(m)
        if not m:
            m = _pct_near_any([q], "%s %s in the quote" % (name, lab), [label_regex(lab)], ln["pct"], window=100)
            m and out.append(m)
        if w.norm(lab) not in {w.norm(k) for k in glossary} and len(str(ln.get("plain") or "").strip()) < 8:
            out.append("%s: fee line %r is not in assets/plain_terms.json: give a plain-English explanation in 'plain'" % (pre, lab))
    # once-off costs
    for it in p.get("initial_fees") or []:
        if not isinstance(it, dict) or not {"label", "value"} <= set(it) or set(it) - {"label", "value", "plain"}:
            out.append("%s: each initial fee needs label and value (plain only when the label is not in assets/plain_terms.json)" % pre)
            continue
        lab, val = str(it["label"]).strip(), str(it["value"]).strip()
        m = _any([q], lambda e: e.name("initial fee label %r in the %s quote" % (lab, name), lab))
        m and out.append(m)
        if val.lower() != "none" and w.parse_money(val) != 0:
            if "%" in val:
                m = _any([q], lambda e: _exact_pct(e, "initial fee %r in the %s quote" % (lab, name), val))
            else:
                d = w.parse_money(val)
                m = "initial fee %r: %r is not an amount, a percentage or 'None'" % (lab, val) if d is None else _any([q], lambda e: e.number("initial fee %r in the %s quote" % (lab, name), d))
            m and out.append(m)
        if w.norm(lab) not in {w.norm(k) for k in glossary} and len(str(it.get("plain") or "").strip()) < 8:
            out.append("%s: initial fee %r is not in assets/plain_terms.json: give a plain-English explanation in 'plain'" % (pre, lab))
    # loyalty and bonus features
    for lo in p.get("loyalty") or []:
        need = {"name", "trigger", "guaranteed", "pays", "percentages"}
        if not isinstance(lo, dict) or not need <= set(lo) or set(lo) - need - {"explanation", "source_line"}:
            out.append("%s: each loyalty item needs name, trigger, guaranteed, pays, percentages (explanation and source_line when needed)" % pre)
            continue
        m = _any([q], lambda e: e.name("loyalty feature in the %s quote" % name, lo["name"]))
        m and out.append(m)
        if lo["guaranteed"] not in ("guaranteed", "discretionary"):
            out.append("%s: loyalty %r: guaranteed must be 'guaranteed' or 'discretionary'" % (pre, lo["name"]))
        if not isinstance(lo["percentages"], list):
            out.append("%s: loyalty %r: percentages must be a list" % (pre, lo["name"]))
            continue
        for pc in lo["percentages"]:
            m = _any([q], lambda e: _exact_pct(e, "loyalty %r percentage in the %s quote" % (lo["name"], name), pc))
            m and out.append(m)
        ex = str(lo.get("explanation") or "").strip()
        if (len(lo["percentages"]) > 1 or lo.get("explanation") is not None) and not 30 <= len(ex) <= 600:
            out.append("%s: loyalty %r has more than one percentage (or an explanation): the plain-language explanation (30 to 600 characters) is needed before the numbers" % (pre, lo["name"]))
        if lo.get("source_line"):
            m = _any([q], lambda e: e.name("source line of loyalty %r in the %s quote" % (lo["name"], name), lo["source_line"]))
            m and out.append(m)
    # performance fees
    for pf in p.get("performance_fees") or []:
        if not isinstance(pf, dict) or set(pf) != {"fund", "note"} or len(str(pf["note"]).strip()) < 10:
            out.append("%s: each performance fee needs fund and note (10 characters or more)" % pre)
        elif not any(w.norm(f["name"]) == w.norm(pf["fund"]) for f in fs):
            out.append("%s: performance fee note names a fund (%r) that is not on this quote" % (pre, pf["fund"]))
    for fx in p.get("flexibility") or []:
        if not isinstance(fx, dict) or set(fx) != {"topic", "text", "quote_words"}:
            out.append("%s: each flexibility item needs topic, text and quote_words (a short phrase from the quote)" % pre)
            continue
        m = _any([q], lambda e: e.name("flexibility phrase in the %s quote" % name, fx["quote_words"]))
        m and out.append(m)


def _sheet_problems(e, ent, label, today, out):
    for k, lab in (("benchmark", "benchmark"), ("target", "target or objective")):
        if not str(ent.get(k) or "").strip():
            out.append("%s: %s is missing (the fact sheet's own wording)" % (label, lab))
        else:
            m = _any([e], lambda ev_: ev_.name("%s %s" % (label, lab), ent[k]))
            m and out.append(m)
    for k, lab in (("perf_1y", "1 year"), ("perf_3y", "3 year"), ("perf_5y", "5 year")):
        v = str(ent.get(k) or "").strip()
        if not v:
            out.append("%s: %s performance is missing ('Not available' when the fund is too young)" % (label, lab))
        elif v.lower() != "not available":
            if pct_decimal(v) is None:
                out.append("%s: %s performance %r is not a percentage" % (label, lab, v))
            else:
                m = _any([e], lambda ev_: _exact_pct(ev_, "%s %s performance" % (label, lab), v))
                m and out.append(m)
    d = w.parse_date(ent.get("as_at"))
    if d is None:
        out.append("%s: as_at must be DD/MM/YYYY (the fact sheet's own date)" % label)
    else:
        if d > today:
            out.append("%s: the fact sheet date %s is in the future" % (label, ent["as_at"]))
        m = _any([e], lambda ev_: ev_.date("%s fact sheet date" % label, ent["as_at"]))
        m and out.append(m)
    desc = str(ent.get("description") or "").strip()
    if not desc or len(desc.split()) > 25:
        out.append("%s: description must be one plain line of 25 words or fewer, in our own words" % label)
    elif _has(e) and verbatim_run(desc, e.text):
        out.append("%s: the description repeats 8 or more words in a row from the fact sheet: rewrite it in our own words (never copied)" % label)
    if str(ent.get("risk_label") or "").strip():
        m = _any([e], lambda ev_: ev_.name("%s risk label" % label, ent["risk_label"]))
        m and out.append(m)


def answers_problems(a, ev, docs, today, run_client=None, state=None):
    """Problems with the entered answers (empty = fine). `ev` maps a registry key to a docread.Evidence (or None); `docs` is docs.json; `state` holds the declared funds."""
    out = []
    _common(a, ev, docs, today, run_client, out)
    if a.get("product_type") not in PRODUCTS:
        return out + ["product_type must be one of %s (the quotes' own product, the same for every quote)" % ", ".join(PRODUCTS)]
    provs = a.get("providers")
    if not isinstance(provs, list) or not MIN_PROVIDERS <= len(provs) <= MAX_PROVIDERS:
        return out + ["providers: from %d to %d providers, each with its own registered quote" % (MIN_PROVIDERS, MAX_PROVIDERS)]
    names = [str(p.get("name") or "").strip() for p in provs if isinstance(p, dict)]
    if len(set(w.norm(n) for n in names)) != len(names):
        out.append("two providers have the same name")
    reg_quotes = docs_of(docs, "quote")
    extra = [n for n in reg_quotes if w.norm(n) not in {w.norm(x) for x in names}]
    if extra:
        out.append("a registered quote has no provider in the answers: %s" % ", ".join(extra))
    for i, p in enumerate(provs):
        if not isinstance(p, dict):
            out.append("provider %d is not an object" % (i + 1))
            continue
        _provider_problems(p, i, a, ev, docs, state, out)
    # ---- the fund fact sheets
    if state is not None:
        want = declared_funds(state)
        mine = {(w.norm(p["name"]), w.norm(f["name"])) for p in provs if isinstance(p, dict) and p.get("name") for f in (p.get("funds") or []) if isinstance(f, dict) and f.get("name")}
        for d in want:
            if (w.norm(d["provider"]), w.norm(d["name"])) not in mine:
                out.append("the declared fund %r (%s) is not in the answers" % (d["name"], d["provider"]))
        ents = a.get("fund_sheets")
        if not isinstance(ents, list):
            out.append("fund_sheets must be a list with one entry per declared fund")
            ents = []
        for d in want:
            lab = sheet_label(d["provider"], d["name"])
            k = dkey("factsheet", lab)
            ent = next((x for x in ents if isinstance(x, dict) and w.norm(x.get("provider", "")) == w.norm(d["provider"]) and w.norm(x.get("fund", "")) == w.norm(d["name"])), None)
            if ent is None:
                out.append("fund_sheets: no entry for %s" % lab)
            elif k in docs["docs"]:
                need = {"provider", "fund", "benchmark", "target", "perf_1y", "perf_3y", "perf_5y", "as_at", "description", "risk_label"}
                if set(ent) != need:
                    out.append("fund_sheets %s needs exactly %s" % (lab, ", ".join(sorted(need))))
                else:
                    _sheet_problems(ev.get(k), ent, lab, today, out)
            elif (docs["missing"].get(k) or "").strip():
                if set(ent) != {"provider", "fund", "not_found"} or ent.get("not_found") is not True:
                    out.append("fund_sheets %s: no fact sheet could be found (Paul's words recorded): the entry is exactly provider, fund and not_found: true" % lab)
            else:
                out.append("%s: register its fact sheet, or record with Paul's words that none could be found" % lab)
    # ---- supplementary documents
    sup = docs_of(docs, "supplement")
    sc = a.get("supplement_checks")
    if sup and not isinstance(sc, dict):
        out.append("supplement_checks: a supplementary document is registered, so say for each (by its label) 'none' or the list of differences from the quote")
        sc = {}
    for lab, k in sup.items():
        if lab not in (sc or {}):
            out.append("supplement_checks: nothing said about the supplementary document %r" % lab)
            continue
        v = sc[lab]
        if v == "none":
            continue
        if not isinstance(v, list) or not v:
            out.append("supplement_checks[%r] must be 'none' or a non-empty list" % lab)
            continue
        owner = next((n for n in names if w.norm(n) in w.norm(lab)), None)
        for c in v:
            if not isinstance(c, dict) or set(c) != {"provider", "field", "quote_value", "supplement_value", "supplement_date"} or w.parse_date(c.get("supplement_date")) is None:
                out.append("supplement_checks[%r]: each difference needs provider, field, quote_value, supplement_value and supplement_date (DD/MM/YYYY)" % lab)
                continue
            qk = dkey("quote", c["provider"])
            if qk not in docs["docs"]:
                out.append("supplement_checks[%r]: provider %r has no registered quote" % (lab, c["provider"]))
                continue
            for val, doc_key, what in ((c["quote_value"], qk, "the quote"), (c["supplement_value"], k, "the supplementary document")):
                e = ev.get(doc_key)
                if _has(e) and w.norm(val) not in e.norm and not (w.parse_money(val) is not None and w.parse_money(val) in e.numbers):
                    out.append("supplement_checks[%r]: %r is not in the text of %s" % (lab, val, what))
        del owner
    # ---- the extras Paul asked for
    ex = a.get("extras")
    if not isinstance(ex, dict) or set(ex) != {"verdict", "tax_note", "flexibility", "example_fund_value"} or not all(isinstance(ex[k], bool) for k in ("verdict", "tax_note", "flexibility")):
        out.append("extras needs exactly verdict, tax_note, flexibility (true or false, Paul's answers) and example_fund_value (null or an amount)")
    else:
        if ex["tax_note"] and a["product_type"] in ("Endowment", "Living Annuity"):
            out.append("STOP: there is no approved tax wording for a %s comparison: ask Paul what the tax note should say (never invented)" % a["product_type"])
        if ex["example_fund_value"] is not None and (w.parse_money(ex["example_fund_value"]) is None or not ex["verdict"]):
            out.append("example_fund_value is an amount and is only used with a verdict (Paul's answer): %r" % ex["example_fund_value"])
        if ex["flexibility"] and not any(p.get("flexibility") for p in provs if isinstance(p, dict)):
            out.append("flexibility was asked for but no provider has flexibility items")
    # ---- the Tax-Free comparison
    if a["product_type"] == "TFSA":
        lim = tfsa_limits()
        if not lim[2]:
            out.append("STOP: the TFSA limits (annual R %s, lifetime R %s in assets/tax_facts.json) are NOT confirmed by Paul. Ask him for the 2026/27 annual and lifetime limits; they are set in Claude Code (the old skill said R36,000 a year, the Tax-Free skill R46,000)" %
                       (money_shown(lim[0]), money_shown(lim[1])))
        t = a.get("tfsa")
        if not isinstance(t, dict) or set(t) != {"annual_used", "lifetime_used"} or any(w.parse_money(t.get(k)) is None for k in ("annual_used", "lifetime_used")):
            out.append("tfsa needs exactly annual_used (this tax year) and lifetime_used, as amounts (R 0 only when the Fact Find or the statement says so)")
        elif "tfsa_statement" not in docs["docs"] and not (docs["missing"].get("tfsa_statement") or "").strip() and "fact_find" not in docs["docs"]:
            out.append("the TFSA contributions already made: register the TFSA statement (or the Fact Find), or record Paul's words")
        else:
            for k in ("annual_used", "lifetime_used"):
                d = w.parse_money(t[k])
                if d != 0:
                    m = _any([ev.get("tfsa_statement"), ev.get("fact_find")], lambda e: e.number("TFSA %s in the statement or Fact Find" % k, d))
                    m and out.append(m)
    return out


# ------------------------------------------------------------------ the comparison itself
FIELD_WORDS = {"contribution_type": "contribution structure", "contribution": "contribution amount", "escalation": "yearly increase", "term": "term or retirement age"}


def _norm_val(field, p):
    v = str(p.get(field) or "").strip()
    if field == "contribution":
        d = w.parse_money(v)
        return str(d) if d is not None else v
    if field == "escalation":
        return "none" if v.lower() == "none" else str(pct_decimal(v))
    return w.norm(v)


def _show_val(field, p):
    v = p.get(field)
    if field == "contribution_type":
        return {"recurring": "a monthly contribution", "lump_sum": "a lump sum"}[v]
    if field == "contribution":
        return "R " + money_shown(v)
    if field == "escalation":
        return "no yearly increase" if str(v).lower() == "none" else "%s%% a year" % pct_digits(v)
    return str(v)


def mismatches(a):
    """[(field in plain words, 'Provider A x; Provider B y')]: the apples-to-apples checks across the quotes."""
    out = []
    for f in ("contribution_type", "contribution", "escalation", "term"):
        vals = {_norm_val(f, p) for p in a["providers"]}
        if len(vals) > 1:
            out.append((FIELD_WORDS[f], "; ".join("%s %s" % (p["name"], _show_val(f, p)) for p in a["providers"])))
    return out


def blended_fee(p):
    return sum((pct_decimal(f["allocation"]) / 100 * pct_decimal(f["asset_mgmt_fee"]) for f in p["funds"]), Decimal(0)).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)


def fee_total(p):
    """(the blended asset management fee as shown, the shown lines, the total adding up the SHOWN figures)."""
    comps = [fee_shown(blended_fee(p))] + [fee_shown(pct_decimal(ln["pct"])) for ln in p["fee_lines"]]
    return comps, fee_shown(sum((Decimal(x) for x in comps), Decimal(0)))


def fee_rows(a):
    """[(label, plain explanation, [value or None per provider])]: the asset management fee first, then the union of the quotes' own lines in order of first appearance."""
    glossary = {w.norm(k): v for k, v in terms()["fee_labels"].items()}
    rows = [("Asset management fee", glossary["asset management fee"], [fee_shown(blended_fee(p)) for p in a["providers"]])]
    order, info = [], {}
    for p in a["providers"]:
        for ln in p["fee_lines"]:
            k = w.norm(ln["label"])
            if k not in info:
                order.append(k)
                info[k] = (str(ln["label"]).strip(), glossary.get(k) or str(ln.get("plain") or "").strip())
    for k in order:
        vals = []
        for p in a["providers"]:
            hit = next((ln for ln in p["fee_lines"] if w.norm(ln["label"]) == k), None)
            vals.append(fee_shown(pct_decimal(hit["pct"])) if hit else None)
        rows.append((info[k][0], info[k][1], vals))
    return rows


def initial_rows(a):
    glossary = {w.norm(k): v for k, v in terms()["fee_labels"].items()}
    order, info = [], {}
    for p in a["providers"]:
        for it in p.get("initial_fees") or []:
            k = w.norm(it["label"])
            if k not in info:
                order.append(k)
                info[k] = (str(it["label"]).strip(), glossary.get(k) or str(it.get("plain") or "").strip())
    rows = []
    for k in order:
        vals = []
        for p in a["providers"]:
            hit = next((it for it in p.get("initial_fees") or [] if w.norm(it["label"]) == k), None)
            vals.append(str(hit["value"]).strip() if hit else None)
        rows.append((info[k][0], info[k][1], vals))
    return rows


def sheet_entries(a):
    return list(a.get("fund_sheets") or [])


def stale_sheets(a, today):
    out = []
    for e in sheet_entries(a):
        d = w.parse_date(e.get("as_at"))
        if d and (today - d).days > STALE_DAYS:
            out.append((e["provider"], e["fund"], e["as_at"]))
    return out


def not_found_sheets(a):
    return [(e["provider"], e["fund"]) for e in sheet_entries(a) if e.get("not_found")]


def risk_flags(a):
    out = []
    rp = w.norm(a.get("risk_profile") or "")
    for e in sheet_entries(a):
        rl = str(e.get("risk_label") or "").strip()
        if rl and w.norm(rl) != rp:
            out.append("The %s (%s) is labelled %r on its fact sheet, but the client's risk profile is %r: check the fund suits the client (your judgement, not the program's)." % (e["fund"], e["provider"], rl, a["risk_profile"]))
    return out


def tfsa_rows(a):
    """[(provider, yearly contribution, [breach sentences])] for a Tax-Free comparison (first-year arithmetic from the confirmed limits)."""
    annual, lifetime, _ok = tfsa_limits()
    used_y, used_l = w.parse_money(a["tfsa"]["annual_used"]), w.parse_money(a["tfsa"]["lifetime_used"])
    rows = []
    for p in a["providers"]:
        c = w.parse_money(p["contribution"])
        yearly = c * 12 if p["contribution_type"] == "recurring" else c
        br = []
        if used_y + yearly > annual:
            br.append(("annual", used_y + yearly - annual))
        if used_l + yearly > lifetime:
            br.append(("lifetime", used_l + yearly - lifetime))
        rows.append((p["name"], yearly, br))
    return rows


def supplement_items(a):
    """[(provider, doc label, field, quote value, supplement value, date)]"""
    out = []
    for lab, v in (a.get("supplement_checks") or {}).items():
        if v != "none":
            for c in v:
                out.append((c["provider"], lab, c["field"], c["quote_value"], c["supplement_value"], c["supplement_date"]))
    return out


def things_to_know(a, today):
    """The sentences of the 'Things to know' box (only what must be flagged to the client), in a fixed order."""
    wd = wording()
    items = []
    for field, detail in mismatches(a):
        items.append(wd["tk_mismatch"].format(field=field, detail=detail))
    if a["product_type"] == "TFSA":
        annual, lifetime, _ok = tfsa_limits()
        for name, yearly, br in tfsa_rows(a):
            for which, excess in br:
                items.append("%s's quote proposes %s in the first year. %s" % (name, rand_whole(yearly), wd["tax_tfsa_over"].format(which=which, excess=rand_whole(excess))))
    for prov, lab, field, qv, sv, dt in supplement_items(a):
        items.append(wd["tk_supplement"].format(provider=prov, doc=lab, date=dt, field=field, supplement_value=sv, quote_value=qv))
    for prov, fund, dt in stale_sheets(a, today):
        items.append(wd["tk_stale"].format(fund=fund, date=dt))
    for prov, fund in not_found_sheets(a):
        items.append(wd["tk_notfound"].format(fund=fund))
    return items


def paul_flags(a, today):
    """What Paul sees in the confirmation table (not the client): the things to know plus the risk-fit flags and his own flags."""
    return things_to_know(a, today) + risk_flags(a) + list(a.get("flags") or [])
