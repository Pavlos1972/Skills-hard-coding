#!/usr/bin/env python3
"""The domain model of the ROA: the dropdown lists (read from the template itself), the reason-text bank, validation of the setup answers,
the data assembled for build_roa.py, the reference number and the file name.

Everything here is a pure function of the answers (answers.json), the template and the bank, so the checker can recompute it and refuse a
file that was edited by hand. Rules are Paul's (the old skill, kept) and his answers of 03/11/2026.
"""
import datetime as dt
import re
import zipfile
from decimal import Decimal

from lxml import etree

import build_roa as br
import wrlib as w

NS = br.NS
WN = br.W
BUNDLES = ("risk", "retirement", "investment")
COVERS = {"death": "LIFE:", "disability": "DISABILITY:", "income_1st24": "INCOME PROTECTION:", "dread": "DREAD:"}
COVER_NAMES = {"death": "Life Cover", "disability": "Lump Sum Disability", "income_1st24": "Income Protection (1st 24 months)", "dread": "Dread Disease"}
STATES = ("accepted", "not_accepted", "declined", "not_pursued")
RISK_PROFILES = ["Conservative", "Moderately Conservative", "Moderate", "Moderately Aggressive", "Aggressive"]
ROA_DATE_TYPES = {"risk": ("client_reply_email", "recap_email", "follow_up_notes"), "retirement": ("client_reply_email", "recap_email"),
                  "investment": ("client_reply_email", "recap_email")}
INVESTMENT_NEEDS = ("Children Education Planning", "General Investment Planning")
OTHER_COVER_SENTENCE = "Although the client has other Risk Cover in force, this transaction does not constitute a replacement of that cover."
PROVIDER_POINTER = ("The client's email reply confirming their go-ahead on this proposal (%s), with the original proposal email quoted in full beneath it, "
                    "is reproduced on the following pages.")
REQUIRED_DOCS = {"risk": ("fna_quote", "application", "follow_up_notes", "fact_find_summary"),
                 "retirement": ("proposal_email", "client_reply_email", "fact_find_summary"),
                 "investment": ("proposal_email", "client_reply_email", "fact_find_summary")}
OPTIONAL_DOCS = {"risk": ("accepted_quote", "overview", "risk_tolerance"), "retirement": ("risk_tolerance",), "investment": ("risk_tolerance",)}
ALL_ROLES = sorted({r for d in (REQUIRED_DOCS, OPTIONAL_DOCS) for v in d.values() for r in v})
SERVED_ROLES = ("fna_quote", "accepted_quote", "application", "follow_up_notes", "proposal_email", "client_reply_email")   # read page by page
SOURCE_KEYS = {"risk": ("bundle", "client_name_id", "risk_profile", "insurers", "roa_date", "scope", "replacement", "taken_up", "premium", "amounts"),
               "retirement": ("bundle", "client_name_id", "risk_profile", "insurers", "roa_date", "product", "amount", "replacement"),
               "investment": ("bundle", "client_name_id", "risk_profile", "insurers", "roa_date", "product", "amount", "replacement")}
ANSWER_KEYS = {"bundle", "client_name", "client_id", "risk_profile", "roa_date", "roa_date_source", "insurers_considered", "recommended_insurer", "recommended_product", "sources",
               "conflicts", "scope", "premium", "covers", "product_provider", "product_name", "amount", "frequency", "need_identified", "replacement", "other_risk_cover_in_force",
               "reply_email"}
COVER_KEYS = {"state", "replacement", "new_while_other_replaced", "scenario", "recommended_amount", "taken_up_amount", "need_identified", "is_monthly", "recommended_product",
              "declined_reason", "declined_source", "custom_reason"}


# ------------------------------------------------------------------ the template's own lists
def template_lists(path=None):
    z = zipfile.ZipFile(path or w.TEMPLATE)
    root = etree.fromstring(z.read("word/document.xml"))
    out = {"insurers": [], "products": [], "status": [], "risk_profile": [], "need": {}}
    for sdt in root.iter(WN + "sdt"):
        pr = sdt.find("w:sdtPr", NS)
        dd = pr.find("w:dropDownList", NS) if pr is not None else None
        if dd is None:
            continue
        al = pr.find("w:alias", NS)
        alias = al.get(WN + "val") if al is not None else None
        items = [li.get(WN + "displayText") for li in dd]
        items = [i.strip() for i in items if i and i.strip() not in ("Choose an item.", ".")]
        if alias == "CCS1":
            out["status"] = items
        elif alias == "DDB81":
            out["products"] = items
        elif alias in ("5A", "5B1", "5B2", "5B3", "5C", "5D", "5E"):
            out["need"][alias] = items
        elif alias is None and len(items) == 5 and not out["risk_profile"]:
            out["risk_profile"] = items
        elif alias is None and len(items) >= 9 and not out["insurers"]:
            out["insurers"] = items
    return out


# ------------------------------------------------------------------ the reason-text bank
def bank():
    """{cover key: {scenario heading: paragraph}} read from the response bank (Word) exactly as written."""
    import docx
    ps = [p.text.strip() for p in docx.Document(w.BANK).paragraphs if p.text.strip()]
    names = {v: k for k, v in COVERS.items()}
    out, cur, i = {}, None, 0
    while i < len(ps):
        if ps[i] in names:
            cur = names[ps[i]]
            out[cur] = {}
            i += 1
        elif cur and ps[i].endswith(":") and ps[i].upper() == ps[i] and i + 1 < len(ps):
            out[cur][ps[i]] = ps[i + 1]
            i += 2
        else:
            i += 1
    return out


def heading_replacement(heading):
    """True / False when the scenario heading says replacement or non-replacement, None when it says neither."""
    if heading.endswith("/ NON-REPLACEMENT:"):
        return False
    if heading.endswith("/ REPLACEMENT:"):
        return True
    return None


def cut_to_other_cover(text):
    """The paragraph up to its replacement sentence, then the verbatim 'other Risk Cover in force' sentence (Paul's rule). None if it cannot be cut."""
    i = text.rfind(" As the client ")
    return None if i < 0 else text[:i].rstrip() + " " + OTHER_COVER_SENTENCE


def cover_reason(key, c, bk):
    """(text, mode, heading) for one risk cover; text is None when the entries are wrong."""
    st = c.get("state")
    if st == "declined":
        return (c.get("declined_reason") or "").strip(), "asked", ""
    if st == "not_pursued":
        return br.DECLINED_NEED, "fixed", ""
    if c.get("custom_reason"):
        return c["custom_reason"].strip(), "custom", ""
    head = c.get("scenario") or ""
    text = (bk.get(key) or {}).get(head)
    if text is None:
        return None, "bank", head
    if c.get("new_while_other_replaced"):
        text = cut_to_other_cover(text)
    return text, "bank", head


# ------------------------------------------------------------------ small helpers
def amount_number(v):
    """A whole-rand amount from 'R 1 000 000' (the template shows whole rands) as an int, or None."""
    d = w.parse_money(v) if v not in (None, "") else None
    if d is None or d != d.to_integral_value():
        return None
    return int(d)


def insurer_display(name):
    n = (name or "").strip()
    return {"BRIGHTROCK": "BrightRock"}.get(n.upper(), n.title())


def iso(date_text):
    d = w.parse_date(date_text)
    return d.strftime("%Y-%m-%d") if d else None


def next_review(roa_iso):
    d = dt.datetime.strptime(roa_iso, "%Y-%m-%d")
    try:
        n = d.replace(year=d.year + 1)
    except ValueError:
        n = d + dt.timedelta(days=365)
    return n.strftime("%Y-%m-%d")


def is_risk(a):
    return a.get("bundle") == "risk"


def any_replacement(a):
    if is_risk(a):
        return any(bool(c.get("replacement")) for c in (a.get("covers") or {}).values() if c.get("state") in ("accepted", "not_accepted"))
    return bool(a.get("replacement"))


# ------------------------------------------------------------------ validation
def answers_problems(a, lists, bk, ev, today):
    """Problems with the entered answers (empty = fine). `ev` maps a document role to a docread.Evidence (or None if it is not registered)."""
    out = []
    for k in set(a) - ANSWER_KEYS:
        out.append("unknown field %r" % k)
    b = a.get("bundle")
    if b not in BUNDLES:
        return out + ["bundle must be risk, retirement or investment (one ROA is one bundle)"]
    if len((a.get("client_name") or "").strip().split()) < 2:
        out.append("client_name must be the full name")
    if not re.fullmatch(r"\d{13}", a.get("client_id") or ""):
        out.append("client_id must be 13 digits, no spaces or dashes")
    if a.get("risk_profile") not in RISK_PROFILES:
        out.append("risk_profile must be one of %s" % ", ".join(RISK_PROFILES))
    d = w.parse_date(a.get("roa_date"))
    if d is None:
        out.append("roa_date %r is not a date (DD/MM/YYYY)" % a.get("roa_date"))
    elif d > today:
        out.append("roa_date %s is in the future: it is the date the client gave the go-ahead" % a["roa_date"])
    src = a.get("roa_date_source") or {}
    if src.get("type") not in ROA_DATE_TYPES[b]:
        out.append("roa_date_source.type must be one of %s%s" % (", ".join(ROA_DATE_TYPES[b]), " (a Retirement or Investment ROA needs the client's own reply email)" if b != "risk" else ""))
    if len((src.get("file") or "").strip()) < 3:
        out.append("roa_date_source.file: say which document or message gives the date")
    srcs = a.get("sources") or {}
    for k in SOURCE_KEYS[b]:
        if len(str(srcs.get(k) or "").strip()) < 3:
            out.append("sources.%s: every answer needs its source (a document or Paul's words)" % k)
    if a.get("conflicts"):
        out.append("%d unresolved conflict(s) between sources: STOP and ask Paul, quoting both values and their sources" % len(a["conflicts"]))
    ins = a.get("insurers_considered") or []
    if not 1 <= len(ins) <= 3 or len(set(ins)) != len(ins):
        out.append("insurers_considered must list 1 to 3 different insurers")
    if not (a.get("recommended_insurer") or "").strip():
        out.append("recommended_insurer is missing")
    if not (a.get("recommended_product") or "").strip() and b != "risk":
        out.append("recommended_product is missing")
    for lab, v in [("insurer", x) for x in ins + [a.get("recommended_insurer")] if x]:
        if v.strip() != v.strip().upper():
            out.append("%s %r must be in CAPITALS (as in the dropdown list, e.g. NINETY-ONE)" % (lab, v))
    if b == "risk":
        out += _risk_problems(a, lists, bk, ev)
    else:
        out += _ri_problems(a, lists, ev)
    out += _evidence_problems(a, ev)
    return out


def _risk_problems(a, lists, bk, ev):
    out = []
    if a.get("scope") not in ("personal", "business"):
        out.append("scope must be personal or business")
    if w.parse_money(a.get("premium")) is None:
        out.append("premium %r is not an amount (the 'Total premium' printed inside the accepted quote)" % a.get("premium"))
    covers = a.get("covers") or {}
    if set(covers) != set(COVERS):
        out.append("covers must have exactly: %s (never income_after24 or health care)" % ", ".join(COVERS))
    for k, c in covers.items():
        if k not in COVERS:
            continue
        tag = COVER_NAMES[k]
        for kk in set(c) - COVER_KEYS:
            out.append("%s: unknown field %r" % (tag, kk))
        if c.get("state") not in STATES:
            out.append("%s: state must be one of %s" % (tag, ", ".join(STATES)))
            continue
        if c["state"] in ("accepted", "not_accepted"):
            for f in ("recommended_amount", "taken_up_amount"):
                if amount_number(c.get(f)) is None:
                    out.append("%s: %s %r must be a whole-rand amount" % (tag, f, c.get(f)))
            if c["state"] == "not_accepted" and amount_number(c.get("taken_up_amount")) != 0:
                out.append("%s: FNA done but benefit not accepted means taken_up_amount is R 0" % tag)
            if c["state"] == "accepted" and (amount_number(c.get("taken_up_amount")) or 0) <= 0:
                out.append("%s: accepted but the taken-up amount is zero" % tag)
            if k in ("disability", "income_1st24"):
                need = lists["need"].get("5B1" if k == "disability" else "5B2") or []
                if c.get("need_identified") not in need:
                    out.append("%s: need_identified must be one of %s (it renders BLANK otherwise)" % (tag, "; ".join(need)))
            elif c.get("need_identified"):
                out.append("%s: need_identified is fixed by the script, do not enter it" % tag)
            if not (c.get("recommended_product") or "").strip():
                out.append("%s: recommended_product is missing" % tag)
            if not isinstance(c.get("replacement"), bool):
                out.append("%s: replacement must be true or false, per cover type" % tag)
            text, mode, head = cover_reason(k, c, bk)
            if mode == "custom":
                if len(text) < 20:
                    out.append("%s: the custom wording is too short" % tag)
            elif text is None:
                out.append("%s: scenario %r is not a heading in the response bank for this cover (headings: %s). If none fits, give custom_reason in Paul's own wording" %
                           (tag, c.get("scenario"), "; ".join(sorted(bk.get(k, {})))))
            else:
                hr = heading_replacement(head)
                if hr is not None and hr != bool(c.get("replacement")):
                    out.append("%s: the scenario says %s but replacement is %s" % (tag, "replacement" if hr else "non-replacement", c.get("replacement")))
                if c.get("new_while_other_replaced"):
                    if hr is not False:
                        out.append("%s: new_while_other_replaced needs a NON-REPLACEMENT scenario" % tag)
                    if cut_to_other_cover(bk[k][head]) is None:
                        out.append("%s: this bank paragraph cannot be cut at its replacement sentence: use custom_reason" % tag)
                    if c.get("replacement"):
                        out.append("%s: new_while_other_replaced contradicts replacement true" % tag)
        elif c["state"] == "declined":
            if len((c.get("declined_reason") or "").strip()) < 8 or (c.get("declined_reason") or "").strip() == br.DECLINED_NEED:
                out.append("%s: a declined need needs the specific reason Paul gave (asked for, never generic)" % tag)
            if len((c.get("declined_source") or "").strip()) < 5:
                out.append("%s: say where the declined reason came from (declined_source, for example Paul's own words)" % tag)
    if not any(c.get("state") in ("accepted", "not_accepted") for c in covers.values()):
        out.append("at least one cover type must be active in a Risk ROA")
    return out


def _ri_problems(a, lists, ev):
    out = []
    b = a["bundle"]
    for f in ("product_provider", "product_name"):
        if not (a.get(f) or "").strip():
            out.append("%s is missing (asked, never inferred from the insurer)" % f)
    if w.parse_money(a.get("amount")) is None or (w.parse_money(a.get("amount")) or 0) <= 0:
        out.append("amount %r is not a positive amount (the figure the client confirmed in their own reply)" % a.get("amount"))
    if a.get("frequency") not in ("lump_sum", "monthly"):
        out.append("frequency must be lump_sum or monthly (asked directly)")
    if not isinstance(a.get("replacement"), bool):
        out.append("replacement must be true or false")
    if not isinstance(a.get("other_risk_cover_in_force"), bool):
        out.append("other_risk_cover_in_force must be true or false")
    if b == "investment" and a.get("need_identified") not in INVESTMENT_NEEDS:
        out.append("need_identified must be %s" % " or ".join(INVESTMENT_NEEDS))
    if b == "retirement" and a.get("need_identified"):
        out.append("need_identified is fixed (Retirement Planning) for a Retirement ROA, do not enter it")
    for f in ("covers", "scope", "premium"):
        if a.get(f):
            out.append("%s belongs to a Risk ROA only" % f)
    r = a.get("reply_email") or {}
    for f in ("from", "sent", "to", "subject", "acceptance_text"):
        if len(str(r.get(f) or "").strip()) < 3:
            out.append("reply_email.%s is missing (the client's own reply email must be embedded)" % f)
    if r.get("from") and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[A-Za-z]{2,}", r["from"]):
        out.append("reply_email.from must be the client's own email address")
    return out


def _evidence_problems(a, ev):
    """Names, ID and every figure must appear in the documents' own text. Returns [] when documents without text cannot be checked."""
    out = []
    def need(role):
        e = ev.get(role)
        if e is None:
            out.append("the document %r is not registered" % role)
        return e
    ident = [e for e in (ev.get("application"), ev.get("fact_find_summary")) if e is not None and e.has_text]
    if ident:
        if not any(e.name("x", a.get("client_name")) is None for e in ident):
            out.append("the client name %r is not in the application or the Fact Find text" % a.get("client_name"))
        if not any(e.code("x", a.get("client_id")) is None for e in ident):
            out.append("the ID number is not in the application or the Fact Find text")
    if is_risk(a):
        fna, acc = need("fna_quote"), ev.get("accepted_quote") or ev.get("fna_quote")
        for k, c in (a.get("covers") or {}).items():
            if k not in COVERS or c.get("state") not in ("accepted", "not_accepted"):
                continue
            if fna is not None and fna.has_text:
                m = fna.number("%s recommended amount" % COVER_NAMES[k], c.get("recommended_amount"))
                m and out.append(m)
            if acc is not None and acc.has_text and c.get("state") == "accepted":
                m = acc.number("%s taken-up amount" % COVER_NAMES[k], c.get("taken_up_amount"))
                m and out.append(m)
        if acc is not None and acc.has_text:
            m = acc.number("the premium", a.get("premium"))
            m and out.append(m)
    else:
        docs = [e for e in (ev.get("client_reply_email"), ev.get("proposal_email")) if e is not None and e.has_text]
        if docs and not any(e.number("x", a.get("amount")) is None for e in docs):
            out.append("the amount %s is not in the client's reply or the proposal email text" % a.get("amount"))
        r = a.get("reply_email") or {}
        rep = ev.get("client_reply_email")
        if rep is not None and rep.has_text and r.get("acceptance_text") and w.norm(r["acceptance_text"]) not in rep.norm:
            out.append("the acceptance wording is not in the client's reply email text")
    return out


# ------------------------------------------------------------------ assembly
def reasons_for(a, bk):
    """{section key: (text, mode, heading)} for every active-bundle section, exactly what must appear in the document."""
    out = {}
    if is_risk(a):
        for k, c in a["covers"].items():
            out[k] = cover_reason(k, c, bk)
    else:
        text = PROVIDER_POINTER % a["roa_date"]
        if a.get("other_risk_cover_in_force"):
            text += " " + OTHER_COVER_SENTENCE
        out[a["bundle"]] = (text, "fixed", "")
    return out


def reference_no(a):
    if is_risk(a):
        return "%s %s Cover - R%s p.m." % (insurer_display(a["recommended_insurer"]), a["scope"].title(), format(w.parse_money(a["premium"]), ",.2f"))
    return "%s %s - R %s%s" % (a["product_provider"].strip(), a["product_name"].strip(), format(w.parse_money(a["amount"]), ",.2f"),
                               " - Lump Sum" if a["frequency"] == "lump_sum" else " p.m.")


def delivery_filename(a):
    r = iso(a["roa_date"])
    if is_risk(a):
        return br.build_filename(a["recommended_insurer"], a["scope"].title(), float(w.parse_money(a["premium"])), r, a["client_name"].strip()) + ".docx"
    d = dt.datetime.strptime(r, "%Y-%m-%d").strftime("%d.%m.%y")
    return "ROA - %s %s - R %s%s - %s - (%s).docx" % (a["product_provider"].strip(), a["product_name"].strip(), format(w.parse_money(a["amount"]), ".2f"),
                                                      " - Lump Sum" if a["frequency"] == "lump_sum" else " p.m.", d, a["client_name"].strip())


def assemble(a, bk):
    """The data dict for build_roa.build_roa, built by the program from the answers."""
    data = {"bundle": a["bundle"], "client_name": a["client_name"].strip(), "client_id": a["client_id"], "roa_date": iso(a["roa_date"]),
            "roa_reference_no": reference_no(a), "risk_profile": a["risk_profile"], "policy_replacement": any_replacement(a), "sections": {}}
    rs = reasons_for(a, bk)
    if is_risk(a):
        for k, c in a["covers"].items():
            text = rs[k][0]
            if c["state"] in ("declined", "not_pursued"):
                data["sections"][k] = {"declined": True, "reason_text": text}
                continue
            s = {"status": "IMPORTANT", "recommended_amount": amount_number(c["recommended_amount"]), "taken_up_amount": amount_number(c["taken_up_amount"]),
                 "insurers_considered": a["insurers_considered"], "recommended_insurer": a["recommended_insurer"], "recommended_product": c["recommended_product"], "reason_text": text}
            if k in ("disability", "income_1st24"):
                s["need_identified"] = c["need_identified"]
            if k == "income_1st24":
                s["is_monthly"] = True
            data["sections"][k] = s
    else:
        s = {"status": "IMPORTANT", "insurers_considered": a["insurers_considered"], "recommended_insurer": a["recommended_insurer"],
             "recommended_product": a["recommended_product"], "reason_text": rs[a["bundle"]][0]}
        if a["bundle"] == "investment":
            s["need_identified"] = a["need_identified"]
        data["sections"][a["bundle"]] = s
    return data


def table_rows(a, bk):
    """The confirmation table: (question, answer, source) for Paul's ONE question (Step 0b)."""
    s = a.get("sources") or {}
    rows = [("Bundle", a["bundle"].title(), s.get("bundle")), ("Client name and ID", "%s (ID %s)" % (a["client_name"], a["client_id"]), s.get("client_name_id")),
            ("Risk profile", a["risk_profile"], s.get("risk_profile")),
            ("ROA date (the date the client gave the go-ahead)", "%s (%s: %s)" % (a["roa_date"], a["roa_date_source"]["type"].replace("_", " "), a["roa_date_source"]["file"]), s.get("roa_date")),
            ("Insurers considered", ", ".join(a["insurers_considered"]), s.get("insurers")), ("Recommended insurer", a["recommended_insurer"], s.get("insurers"))]
    if is_risk(a):
        rows.insert(1, ("Personal or Business", a["scope"].title(), s.get("scope")))
        rows.append(("Premium (inside the accepted quote)", a["premium"], s.get("premium")))
        rs = reasons_for(a, bk)
        for k, c in a["covers"].items():
            if c["state"] in ("accepted", "not_accepted"):
                ans = "%s: recommended %s, taken up %s; %s; %s" % (COVER_NAMES[k], c["recommended_amount"], c["taken_up_amount"], "replacement" if c["replacement"] else "not a replacement",
                                                                    "FNA done but benefit not accepted" if c["state"] == "not_accepted" else "accepted")
            else:
                ans = "%s: %s" % (COVER_NAMES[k], "DECLINED" if c["state"] == "declined" else "need exists, client does not want to pursue it")
            text, mode, head = rs[k]
            rows.append((COVER_NAMES[k], ans, s.get("taken_up")))
            rows.append(("  reason text", "%s: %s" % ({"bank": "FROM THE BANK (%s)" % head, "custom": "CUSTOM, NOT FROM THE BANK", "asked": "the reason Paul gave", "fixed": "fixed sentence"}[mode], text), None))
    else:
        rows += [("Product provider and name", "%s %s" % (a["product_provider"], a["product_name"]), s.get("product")),
                 ("Amount", "%s, %s" % (a["amount"], "lump sum" if a["frequency"] == "lump_sum" else "recurring (monthly)"), s.get("amount")),
                 ("Replacement", "yes" if a["replacement"] else "no", s.get("replacement")),
                 ("The client's own reply email", "from %s, sent %s: %r" % (a["reply_email"]["from"], a["reply_email"]["sent"], a["reply_email"]["acceptance_text"]), s.get("amount"))]
    rows.append(("Replacement wording in the document", "replace" if any_replacement(a) else "not replace", s.get("replacement")))
    return rows


def not_in_lists(a, lists):
    """Entries that are not an option of the template's dropdowns: they are written as text (Paul is told)."""
    out = []
    for x in (a.get("insurers_considered") or []) + [a.get("recommended_insurer")]:
        if x and x not in lists["insurers"]:
            out.append("insurer %s" % x)
    prods = [a.get("recommended_product")] + [c.get("recommended_product") for c in (a.get("covers") or {}).values()]
    for x in prods:
        if x and x not in lists["products"]:
            out.append("product %s" % x)
    return sorted(set(out))
