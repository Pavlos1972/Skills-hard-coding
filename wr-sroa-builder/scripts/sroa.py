#!/usr/bin/env python3
"""The domain model of the SROA: validation of the answers (every figure checked against the documents' text), the bullets, the data assembled for
build_sroa.py, the file name and the confirmation table.

Everything here is a pure function of the answers (answers.json), so the checker can recompute it and refuse a file edited by hand. Rules are Paul's
(the old skill, kept) and his answers of 03/11/2026. The old and new figures are TYPED by the chat from the documents; the program proves each one
appears in the right document's text, computes "No change" itself, and builds every bullet in one fixed format.
"""
import re
from decimal import Decimal

import build_sroa as bs
import wrlib as w

QUOTES = ("fna", "shortfall", "alternative")
QUOTE_TITLE = {"fna": "Servicing FNA Quote", "shortfall": "Shortfall Quote", "alternative": "Alternative Quote"}
QUOTE_ROLE = {"fna": "fna_quote", "shortfall": "shortfall_quote", "alternative": "alternative_quote"}
ALL_ROLES = ("current_ps", "fna_quote", "shortfall_quote", "alternative_quote", "acceptance_email", "fact_find_summary")
SERVED_ROLES = ("current_ps", "fna_quote", "shortfall_quote", "alternative_quote", "acceptance_email", "fact_find_summary")
GROUP_HEADINGS = ["Life Cover", "Lump Sum Disability Cover", "Income Protector / Sickness Benefit", "Additional Expense Needs / Dread Disease", "Policy Details"]
PREMIUM = "Premium (incl. R20 policy fee)"
ACI, ABI = "ACI (Automatic Cover Increase)", "ABI (Automatic Benefit Increase)"
POLICY_DETAILS = (PREMIUM, ACI, ABI)
FLAT_ITEMS = ["Life Cover", "Disability Cover", "Dread Disease", "Income Protection", PREMIUM, ACI, ABI, "Retrenchment Cover"]
COVER_ITEMS = ("Life Cover", "Disability Cover", "Dread Disease", "Income Protection", "Retrenchment Cover")
UNITS = ("amount", "monthly", "premium", "percent")
DECLINED_NOTE = "Not compiled — declined by the client."
NOT_COMPILED = "Not compiled for this client."
SOURCE_KEYS = ("quotes", "accepted_quote", "owner_id", "sroa_date", "signature_name", "cp", "investment_linked")
ANSWER_KEYS = {"insurer", "policy_number", "owner", "owner_id", "client_first_name", "client_surname", "client_signature_name", "sroa_date", "sroa_date_source", "compiled", "fna_declined",
               "accepted", "cp_numbers", "layout", "blocks", "changes", "reason", "reason_source", "investment_linked", "portfolio_reason", "portfolio_source", "sources", "conflicts"}
FEE_PHRASE = "including the policy fee"


# ------------------------------------------------------------------ values
def num(v, unit):
    t = str(v).replace("%", "").strip()
    d = w.parse_money(t)
    return d


def fmt_value(v, unit):
    """One fixed format: R1,500,000 / R25,000 p.m. / R1,850.00 p.m. / 3.0%."""
    if unit == "percent":
        t = str(v).strip().replace(" ", "")
        return t if t.endswith("%") else t + "%"
    d = num(v, unit)
    if unit == "amount":
        return "R" + format(int(d), ",d")
    if unit == "monthly":
        return "R" + format(int(d), ",d") + " p.m."
    return "R" + format(d, ",.2f") + " p.m."


def value_problem(label, v, unit):
    if unit not in UNITS:
        return "%s: unit must be one of %s" % (label, ", ".join(UNITS))
    d = num(v, unit)
    if d is None:
        return "%s: %r is not a number" % (label, v)
    if unit in ("amount", "monthly") and d != d.to_integral_value():
        return "%s: %r has cents but this is a whole-rand item (use unit premium for the premium)" % (label, v)
    return None


def same(a, b, unit):
    return num(a, unit) == num(b, unit)


def bullet_changed(it):
    u, lab = it["unit"], it["label"]
    old, new = (it.get("old") or "").strip(), (it.get("new") or "").strip()
    if old and new:
        if same(old, new, u):
            return "%s: No change (%s)" % (lab, fmt_value(new, u))
        return "%s: %s → %s" % (lab, fmt_value(old, u), fmt_value(new, u))
    if new:
        return "%s (new): %s" % (lab, fmt_value(new, u))
    return "%s (removed): was %s" % (lab, fmt_value(old, u))


def bullet_standalone(it):
    return "%s: %s" % (it["label"], fmt_value(it["value"], it["unit"]))


# ------------------------------------------------------------------ validation
def _items_problems(tag, items, kind, grouped_heading=None):
    out = []
    for it in items or []:
        lab = (it.get("label") or "").strip()
        if not lab:
            out.append("%s: an item has no label" % tag)
            continue
        u = it.get("unit")
        vals = ["value"] if kind == "standalone" else ["old", "new"]
        present = [k for k in vals if str(it.get(k) or "").strip()]
        if not present:
            out.append("%s: %s has no figure" % (tag, lab))
        for k in present:
            m = value_problem("%s %s %s" % (tag, lab, k), it[k], u)
            if m:
                out.append(m)
        if kind == "change" and len(present) == 1 and len((it.get("confirmed") or "").strip()) < 5:
            out.append("%s: %s appears only in the %s documents: confirm with Paul whether it is renamed or genuinely new/removed and record his words in 'confirmed'" %
                       (tag, lab, "new" if "new" in present else "old"))
        if lab.split(" (")[0] == "Premium" and (lab != PREMIUM or u != "premium"):
            out.append("%s: the premium line must be labelled exactly %r with unit premium" % (tag, PREMIUM))
        if lab == PREMIUM and u != "premium":
            out.append("%s: %s must have unit premium" % (tag, PREMIUM))
        if lab in (ACI, ABI) and u != "percent":
            out.append("%s: %s must have unit percent" % (tag, lab))
    return out


def answers_problems(a, ev, today, run_client=None):
    """Problems with the entered answers (empty = fine). `ev` maps a document role to a docread.Evidence (or None if it is not registered)."""
    out = []
    for k in set(a) - ANSWER_KEYS:
        out.append("unknown field %r" % k)
    for k in ("insurer", "policy_number", "owner", "client_first_name", "client_surname", "client_signature_name", "reason", "reason_source"):
        if not str(a.get(k) or "").strip():
            out.append("%s is missing" % k)
    if not re.fullmatch(r"\d{13}", a.get("owner_id") or ""):
        out.append("owner_id must be 13 digits, no spaces or dashes")
    ow = w.norm(a.get("owner", ""))
    if ow and w.norm(a.get("client_surname", "")) not in ow:
        out.append("the surname must be part of the owner's full legal name (the everyday first name may differ from the legal one)")
    if run_client and w.norm("%s %s" % (a.get("client_first_name", ""), a.get("client_surname", ""))) != w.norm(run_client):
        out.append("the everyday name is not the client Paul named (%s)" % run_client)
    d = w.parse_date(a.get("sroa_date"))
    if d is None:
        out.append("sroa_date %r is not a date (DD/MM/YYYY)" % a.get("sroa_date"))
    elif d > today:
        out.append("sroa_date %s is in the future" % a["sroa_date"])
    src = a.get("sroa_date_source") or {}
    if len((src.get("file") or "").strip()) < 3:
        out.append("sroa_date_source.file: say which document gives the date the accepted quote was signed")
    srcs = a.get("sources") or {}
    for k in SOURCE_KEYS:
        if len(str(srcs.get(k) or "").strip()) < 3:
            out.append("sources.%s: every answer needs its source (a document or Paul's words)" % k)
    if a.get("conflicts"):
        out.append("%d unresolved conflict(s) between sources: STOP and ask Paul, quoting both values and their sources" % len(a["conflicts"]))
    comp = a.get("compiled") or {}
    if set(comp) != set(QUOTES) or not all(isinstance(comp[q], bool) for q in QUOTES):
        return out + ["compiled must say true or false for each of fna, shortfall, alternative"]
    if a.get("accepted") not in QUOTES or not comp.get(a.get("accepted")):
        return out + ["accepted must be one of the compiled quotes (fna, shortfall or alternative)"]
    if not comp["fna"] and not isinstance(a.get("fna_declined"), bool):
        out.append("fna_declined must be true or false when no FNA quote was compiled")
    for q in QUOTES:
        if comp[q] and ev.get(QUOTE_ROLE[q]) is None:
            out.append("the %s document (%s) is not registered but the quote was compiled" % (QUOTE_TITLE[q], QUOTE_ROLE[q]))
    cpn = a.get("cp_numbers")
    if not isinstance(cpn, dict) or set(cpn) != {q for q in QUOTES if comp[q]} or not all(isinstance(v, str) for v in cpn.values()):
        out.append("cp_numbers needs one entry for each compiled quote (fna, shortfall, alternative), a text value, empty '' only when Paul/the document says that quote has no CP number")
    lay = a.get("layout")
    if lay not in ("grouped", "flat"):
        out.append("layout must be grouped (BrightRock's needs-based policies) or flat")
    if lay == "grouped" and w.norm(a.get("insurer", "")) != "brightrock":
        out.append("the grouped headings are BrightRock's: for another insurer use the flat layout, or ask Paul")
    out += _blocks_problems(a, comp)
    out += _changes_problems(a)
    inv = a.get("investment_linked")
    if not isinstance(inv, bool):
        out.append("investment_linked must be true or false (asked, never inferred)")
    elif inv and (len((a.get("portfolio_reason") or "").strip()) < 20 or len((a.get("portfolio_source") or "").strip()) < 5):
        out.append("an investment-linked policy needs the portfolio reason in Paul's words (portfolio_reason, portfolio_source)")
    elif inv is False and (a.get("portfolio_reason") or "").strip():
        out.append("portfolio_reason must be empty when the policy is not investment-linked: that section is always 'N/A'")
    if len((a.get("reason") or "").strip()) < 20:
        out.append("reason is too short: it is the advisor's own words, there is no default sentence")
    return out + evidence_problems(a, ev, d)


def _groups_problems(tag, groups, kind, required_policy_details=False):
    out, last = [], -1
    for g in groups or []:
        h = g.get("heading")
        if h not in GROUP_HEADINGS:
            out.append("%s: heading %r must be one of %s" % (tag, h, "; ".join(GROUP_HEADINGS)))
            continue
        i = GROUP_HEADINGS.index(h)
        if i <= last:
            out.append("%s: the headings must follow the fixed order (%s)" % (tag, "; ".join(GROUP_HEADINGS)))
        last = i
        out += _items_problems("%s / %s" % (tag, h), g.get("items"), kind, h)
        if not (g.get("items") or []):
            out.append("%s / %s has no items" % (tag, h))
    if required_policy_details:
        pd = next((g for g in groups or [] if g.get("heading") == "Policy Details"), None)
        labels = {(it.get("label") or "") for it in (pd or {}).get("items", [])}
        miss = [x for x in POLICY_DETAILS if x not in labels]
        if miss:
            out.append("%s: Policy Details must carry %s (ACI and ABI are always compared, even when unchanged)" % (tag, ", ".join(miss)))
        if not any(g.get("heading") != "Policy Details" for g in groups or []):
            out.append("%s: at least one cover heading is needed" % tag)
    return out


def _blocks_problems(a, comp):
    out = []
    blocks = a.get("blocks") or {}
    for q in QUOTES:
        if comp[q] and not (blocks.get(q) or {}).get("groups"):
            out.append("blocks.%s: the compiled %s needs its own figures (groups)" % (q, QUOTE_TITLE[q]))
        if not comp[q] and blocks.get(q):
            out.append("blocks.%s: the quote was not compiled, so it has no figures: never invent any" % q)
        if comp[q]:
            out += _groups_problems("blocks.%s" % q, blocks[q].get("groups"), "standalone")
    return out


def _changes_problems(a):
    out = []
    ch = a.get("changes") or {}
    if a.get("layout") == "grouped":
        out += _groups_problems("changes", ch.get("groups"), "change", required_policy_details=True)
    elif a.get("layout") == "flat":
        items = ch.get("items") or []
        labels = [(it.get("label") or "") for it in items]
        out += _items_problems("changes", items, "change")
        for it in items:
            if not (it.get("old") and it.get("new")):
                out.append("changes: %s: the flat layout needs both an old and a new figure" % it.get("label"))
            if it.get("label") not in FLAT_ITEMS and len((it.get("extra_asked") or "").strip()) < 5:
                out.append("changes: %r is not in the fixed list: include it only if Paul asked for it, and record his words in 'extra_asked'" % it.get("label"))
        miss = [x for x in (PREMIUM, ACI, ABI) if x not in labels]
        if miss:
            out.append("changes: the flat layout must carry %s" % ", ".join(miss))
        if not any(l in COVER_ITEMS for l in labels):
            out.append("changes: at least one cover item is needed")
        if "Waiting Period" in labels and len((next(it for it in items if it["label"] == "Waiting Period").get("extra_asked") or "").strip()) < 5:
            out.append("changes: Waiting Period only when Paul asked for it")
    return out


def _all_items(a):
    """[(where, item, kind)] for every figure entered."""
    out = []
    for q, b in (a.get("blocks") or {}).items():
        for g in (b or {}).get("groups", []):
            out += [("block:" + q, it, "standalone") for it in g.get("items", [])]
    ch = a.get("changes") or {}
    for g in ch.get("groups", []) or []:
        out += [("change", it, "change") for it in g.get("items", [])]
    out += [("change", it, "change") for it in ch.get("items", []) or []]
    return out


def evidence_problems(a, ev, sroa_date):
    """Every figure, name, ID, CP number and the date must appear in the right document's text."""
    out = []
    ps, fnd, acc = ev.get("current_ps"), ev.get("fact_find_summary"), ev.get(QUOTE_ROLE.get(a.get("accepted"), ""))
    mail = ev.get("acceptance_email")

    def has(e):
        return e is not None and e.has_text
    if ps is None:
        out.append("the Current Policy Schedule (current_ps) is not registered")
    if acc is None:
        out.append("the accepted quote's document is not registered")
    if out:
        return out
    pol = a.get("policy_number")
    if has(ps):
        m = ps.code("policy number in the Current Policy Schedule pages", pol)
        m and out.append(m)
    if has(acc):
        m = acc.code("policy number in the accepted quote", pol)
        m and out.append(m)
    ident = [e for e in (ps, fnd) if has(e)]
    if ident:
        if not any(e.name("x", a.get("owner")) is None for e in ident):
            out.append("the owner's name %r is not in the Current Policy Schedule pages or the Fact Find text" % a.get("owner"))
        if not any(e.code("x", a.get("owner_id")) is None for e in ident):
            out.append("the ID number is not in the Current Policy Schedule pages or the Fact Find text")
    cps = a.get("cp_numbers") if isinstance(a.get("cp_numbers"), dict) else {}
    for q, cp in cps.items():
        if not cp or q not in QUOTE_ROLE:
            continue
        docs = [e for e in (ev.get(QUOTE_ROLE[q]), mail) if has(e)]
        if docs and not any(e.code("x", cp) is None for e in docs):
            out.append("the CP number for %s is not in its quote or the acceptance email text" % q)
    date_docs = [e for e in (acc, mail) if has(e)]
    if date_docs and sroa_date and not any(e.date("x", a["sroa_date"]) is None for e in date_docs):
        if len(str((a.get("sroa_date_source") or {}).get("paul_said") or "").strip()) < 5:
            out.append("the SROA date %s is not in the accepted quote or the acceptance email text: if Paul chose it, record his words in sroa_date_source.paul_said" % a["sroa_date"])
    for where, it, kind in _all_items(a):
        u, lab = it.get("unit"), it.get("label")
        if u not in UNITS:
            continue
        if kind == "standalone":
            e = ev.get(QUOTE_ROLE[where.split(":")[1]])
            pairs = [("value", e)]
        else:
            pairs = [("old", ps), ("new", acc)]
        for k, e in pairs:
            v = str(it.get(k) or "").strip()
            if not v or not has(e):
                continue
            d = num(v, u)
            if d is not None and d not in e.numbers:
                out.append("%s %s (%s): %s is not in the %s's text" % (where, lab, k, fmt_value(v, u), "Current Policy Schedule pages" if e is ps else "quote"))
        if lab == PREMIUM:
            e = acc if kind == "change" else ev.get(QUOTE_ROLE[where.split(":")[1]])
            if has(e) and FEE_PHRASE not in e.flat:
                out.append("%s: the quote does not state a total premium '%s': the R20 policy fee rule cannot be proven: ask Paul" % (where, FEE_PHRASE))
    return out


# ------------------------------------------------------------------ assembly
def _groups_out(groups, kind):
    return [{"heading": g["heading"], "bullets": [(bullet_standalone if kind == "standalone" else bullet_changed)(it) for it in g["items"]]} for g in groups]


def assemble(a):
    """The data dict for build_sroa.build_sroa, built by the program from the answers."""
    comp = a["compiled"]
    blocks = []
    for n, q in enumerate(QUOTES, 1):
        b = {"block_label": "Block %d" % n, "title": QUOTE_TITLE[q] + (" (Accepted)" if a["accepted"] == q else ""), "compiled": comp[q]}
        cp = (a.get("cp_numbers") or {}).get(q) or ""
        if cp:
            b["cp_number"] = cp
        if comp[q]:
            b["groups"] = _groups_out(a["blocks"][q]["groups"], "standalone")
        elif q == "fna" and a.get("fna_declined"):
            b["not_compiled_note"] = DECLINED_NOTE
        blocks.append(b)
    data = {"insurer": a["insurer"].strip(), "policy_number": a["policy_number"].strip(), "owner": a["owner"].strip(), "owner_id": a["owner_id"], "quote_blocks": blocks,
            "advice_narrative": a["reason"].strip(), "portfolio_changes_narrative": a["portfolio_reason"].strip() if a["investment_linked"] else "N/A",
            "client_signature_name": a["client_signature_name"].strip()}
    acp = (a.get("cp_numbers") or {}).get(a["accepted"])
    if acp:
        data["accepted_quote_cp_number"] = acp
    ch = a["changes"]
    if a["layout"] == "grouped":
        data["grouped_changes"] = _groups_out(ch["groups"], "change")
    else:
        data["servicing_changes"] = [{"item": it["label"], "old": fmt_value(it["old"], it["unit"]), "new": fmt_value(it["new"], it["unit"]), "no_change": same(it["old"], it["new"], it["unit"])}
                                     for it in ch["items"]]
    return data


def delivery_filename(a):
    d = w.parse_date(a["sroa_date"]).strftime("%d.%m.%y")
    first, sur = a["client_first_name"].strip().replace(" ", "_"), a["client_surname"].strip().replace(" ", "_")
    return w.safe_filename("SROA - %s_%s - %s - (%s_%s)" % (a["insurer"].strip(), a["policy_number"].strip(), d, first, sur)) + ".pdf"


def _flat_sorted(items):
    order = [n.split(" (")[0].strip() for n in bs.LINE_ITEM_ORDER]

    def key(it):
        b = it["label"].split(" (")[0].strip()
        return order.index(b) if b in order else len(order)
    return sorted(items, key=key)


def table_rows(a):
    """The confirmation table: (question, answer, source). Every figure Paul will see on the page is in it."""
    s = a.get("sources") or {}
    comp, cpn = a["compiled"], a.get("cp_numbers") or {}
    rows = [("Insurer and policy number", "%s %s" % (a["insurer"], a["policy_number"]), s.get("quotes")),
            ("Owner (full legal name) and ID", "%s (ID %s)" % (a["owner"], a["owner_id"]), s.get("owner_id")),
            ("Typed on the signature line", a["client_signature_name"], s.get("signature_name")),
            ("Quotes compiled", ", ".join("%s%s" % (QUOTE_TITLE[q], " (accepted)" if a["accepted"] == q else "") for q in QUOTES if comp[q]) +
             ("; the client declined the FNA" if (not comp["fna"] and a.get("fna_declined")) else ""), s.get("quotes")),
            ("Accepted quote", QUOTE_TITLE[a["accepted"]], s.get("accepted_quote")),
            ("CP number(s)", ", ".join("%s: %s" % (QUOTE_TITLE[q], cpn[q]) for q in QUOTES if cpn.get(q)) or "none", s.get("cp")),
            ("SROA date (from the signed quote)", a["sroa_date"], s.get("sroa_date")),
            ("Layout", "BrightRock grouped headings" if a["layout"] == "grouped" else "flat list (one line per item)", s.get("accepted_quote"))]
    for n, q in enumerate(QUOTES, 1):
        if not comp[q]:
            rows.append(("Block %d \u2014 %s" % (n, QUOTE_TITLE[q]), DECLINED_NOTE if (q == "fna" and a.get("fna_declined")) else NOT_COMPILED, s.get("quotes")))
            continue
        for g in a["blocks"][q]["groups"]:
            for it in g["items"]:
                rows.append(("Block %d \u2014 %s / %s" % (n, QUOTE_TITLE[q], g["heading"]), bullet_standalone(it), "that quote's own figures"))
    ch = a["changes"]
    groups = ch["groups"] if a["layout"] == "grouped" else [{"heading": "Requested Servicing Change/s", "items": _flat_sorted(ch["items"])}]
    for g in groups:
        for it in g["items"]:
            src = s.get("accepted_quote")
            if (it.get("confirmed") or "").strip():
                src = "Paul said: " + it["confirmed"].strip()
            elif (it.get("extra_asked") or "").strip():
                src = "Paul asked for this item: " + it["extra_asked"].strip()
            rows.append(("Block 4 \u2014 %s" % g["heading"], bullet_changed(it), src))
    rows += [("Reason for the change (Paul's words)", a["reason"].strip(), a["reason_source"]),
             ("Investment-linked", "yes: " + a["portfolio_reason"].strip() if a["investment_linked"] else "no (Portfolio Changes reads N/A)", s.get("investment_linked"))]
    return rows
