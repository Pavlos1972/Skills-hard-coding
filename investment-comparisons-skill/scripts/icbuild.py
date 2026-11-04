#!/usr/bin/env python3
"""The comparison email: the four tables built from the data file into the fixed template, the checks on what was built, the Teams message to Sitamah, the checks on what
comes back from Outlook and Teams, and the confirmation table. Pure functions of the answers, the documents' names and today's date."""
import html
import json
import re
from decimal import Decimal

import icmp as c
import wrlib as w

D = Decimal
TABLE = '<table width="100%" cellpadding="0" cellspacing="0" border="1" bordercolor="#dddddd" style="border-collapse:collapse;font-size:10pt;">\n'
SPACER = '<table width="100%%" cellpadding="0" cellspacing="0" border="0"><tr><td height="%d" style="font-size:1px;line-height:%dpx;">&nbsp;</td></tr></table>\n'
P = '<p style="font-size:12pt;margin:0;">%s</p>\n'


def E(s):
    return html.escape(str(s), quote=False)


def th(text, bg=c.CHARCOAL, align="left", colspan=1):
    return '<td bgcolor="%s" colspan="%d" style="color:#ffffff;font-weight:bold;font-size:10pt;padding:5px 8px;text-align:%s;">%s</td>' % (bg, colspan, align, text)


def td(text, bg="#ffffff", bold=False, align="left", colspan=1):
    return '<td bgcolor="%s" colspan="%d" style="padding:5px 8px;font-size:10pt;text-align:%s;%s">%s</td>' % (bg, colspan, align, "font-weight:bold;" if bold else "", text)


def label_cell(label, plain=""):
    inner = E(label) + ('<br><span style="font-size:8.5pt;color:#666666;font-weight:normal;">%s</span>' % E(plain) if plain else "")
    return td(inner, bg=c.HOUSE_LIGHT, bold=True)


def pcell(i):
    return c.PALETTE[i % len(c.PALETTE)]


def pct_cell(v):
    v = str(v).strip()
    return v if "%" in v or v.lower() in ("not available", "none") else v + "%"


def money_cell(v):
    d = w.parse_money(v)
    return "R " + c.money_shown(v) if d is not None else str(v)


def contribution_text(p):
    return "%s %s" % (money_cell(p["contribution"]), "per month" if p["contribution_type"] == "recurring" else "once-off")


def escalation_text(p):
    return "No yearly increase" if str(p["escalation"]).strip().lower() == "none" else "%s%% a year" % c.pct_digits(p["escalation"])


# ------------------------------------------------------------------ the four tables
def provider_header(a, first=""):
    return "<tr>" + th(first) + "".join(th(E(p["name"]), bg=pcell(i)[0], align="center") for i, p in enumerate(a["providers"])) + "</tr>\n"


def table1(a):
    rows = [("Plan", [E(p["product_name"]) for p in a["providers"]]), ("Contribution", [E(contribution_text(p)) for p in a["providers"]]),
            ("Yearly increase", [E(escalation_text(p)) for p in a["providers"]]), ("Term or retirement age", [E(p["term"]) for p in a["providers"]]),
            ("Investment funds", ["<br>".join(E("%s (%s%%)" % (f["name"], c.pct_digits(f["allocation"]))) for f in p["funds"]) for p in a["providers"]])]
    out = TABLE + provider_header(a)
    for lab, vals in rows:
        out += "<tr>" + label_cell(lab) + "".join(td(v, bg=pcell(i)[1]) for i, v in enumerate(vals)) + "</tr>\n"
    ini = c.initial_rows(a)
    if not ini:
        out += "<tr>" + label_cell("Once-off costs when the plan starts") + "".join(td(E(c.wording()["no_initial_fees"]), bg=pcell(i)[1]) for i in range(len(a["providers"]))) + "</tr>\n"
    for lab, plain, vals in ini:
        out += "<tr>" + label_cell(lab, plain) + "".join(td(E(money_cell(v) if v and "%" not in v else (v or c.wording()["fee_not_on_quote"])), bg=pcell(i)[1]) for i, v in enumerate(vals)) + "</tr>\n"
    return out + "</table>\n"


def table2(a):
    out = TABLE + provider_header(a, "Fee")
    for lab, plain, vals in c.fee_rows(a):
        out += "<tr>" + label_cell(lab, plain) + "".join(td(("%s%%" % v) if v is not None else E(c.wording()["fee_not_on_quote"]), bg=pcell(i)[1], align="right") for i, v in enumerate(vals)) + "</tr>\n"
    out += "<tr>" + td("Total ongoing fees", bg=c.HOUSE_LIGHT, bold=True) + "".join(td("%s%% p.a." % c.fee_total(p)[1], bg=c.HOUSE_LIGHT, bold=True, align="right") for p in a["providers"]) + "</tr>\n"
    return out + "</table>\n"


def fee_notes(a):
    wd, out = c.wording(), ""
    for p in a["providers"]:
        for pf in p.get("performance_fees") or []:
            out += '<p style="font-size:10pt;font-style:italic;color:#444444;margin:6px 0 0 0;">%s: %s</p>\n' % (E(p["name"]), E(wd["perf_fee_note"].format(fund=pf["fund"], note=pf["note"])))
    return out


def table3(a):
    heads = ("Fund", "Benchmark", "Target", "1 year", "3 years", "5 years", "What it does", "Fact sheet date")
    out = TABLE + "<tr>" + "".join(th(h) for h in heads) + "</tr>\n"
    ents = {(w.norm(e["provider"]), w.norm(e["fund"])): e for e in c.sheet_entries(a)}
    for i, p in enumerate(a["providers"]):
        for f in p["funds"]:
            e = ents.get((w.norm(p["name"]), w.norm(f["name"])))
            row = td("<b>%s</b><br>%s" % (E(p["name"]), E(f["name"])), bg=pcell(i)[1])
            if e is None or e.get("not_found"):
                row += td(E(c.wording()["fund_not_found_cell"]), colspan=7)
            else:
                row += td(E(e["benchmark"])) + td(E(e["target"])) + "".join(td(E(pct_cell(e[k])), align="right") for k in ("perf_1y", "perf_3y", "perf_5y")) + td(E(e["description"])) + td(E(e["as_at"]))
            out += "<tr>" + row + "</tr>\n"
    return out + "</table>\n"


def fund_notes(a):
    return '<p style="font-size:10pt;font-style:italic;color:#444444;margin:6px 0 0 0;">%s</p>\n' % E(c.wording()["fund_source_note"])


def loyalty_explanations(a):
    out = ""
    for p in a["providers"]:
        for lo in p.get("loyalty") or []:
            if str(lo.get("explanation") or "").strip():
                out += '<p style="font-size:11pt;margin:0 0 8px 0;"><strong>%s: %s.</strong> %s</p>\n' % (E(p["name"]), E(lo["name"]), E(lo["explanation"].strip()))
    return out


def table4(a):
    heads = ("Provider", "Benefit", "What triggers it", "Guaranteed or discretionary?", "When it pays out")
    out = TABLE + "<tr>" + "".join(th(h) for h in heads) + "</tr>\n"
    for i, p in enumerate(a["providers"]):
        items = p.get("loyalty") or []
        if not items:
            out += "<tr>" + td(E(p["name"]), bg=pcell(i)[1], bold=True) + td(E(c.wording()["no_loyalty"]), colspan=4) + "</tr>\n"
        for lo in items:
            pcs = " (%s)" % ", ".join(pct_cell(x) for x in lo["percentages"]) if lo["percentages"] else ""
            out += "<tr>" + td(E(p["name"]), bg=pcell(i)[1], bold=True) + td(E(lo["name"] + pcs)) + td(E(lo["trigger"])) + td(E(lo["guaranteed"].capitalize())) + td(E(lo["pays"])) + "</tr>\n"
    return out + "</table>\n"


# ------------------------------------------------------------------ the optional parts
def things_box(a, today):
    items = c.things_to_know(a, today)
    if not items:
        return ""
    wd = c.wording()
    body = "".join('<p style="margin:4px 0 0 0;font-size:11pt;">&#8226;&nbsp; %s</p>\n' % E(x) for x in items)
    return ('<table width="100%%" cellpadding="0" cellspacing="0" border="0"><tr><td bgcolor="%s" style="border-left:4px solid %s;padding:8px 12px;">'
            '<p style="margin:0;font-size:11pt;font-weight:bold;">%s</p>\n%s</td></tr></table>\n' % (c.HOUSE_LIGHT, c.HOUSE_GOLD, E(wd["things_heading"]), body)) + SPACER % (16, 16)


def section(heading, intro, inner):
    return ('<p style="font-size:12pt;font-weight:bold;margin:0;">%s</p>\n' % E(heading)) + SPACER % (6, 6) + P % E(intro) + SPACER % (8, 8) + inner + SPACER % (16, 16)


def verdict_lines(a):
    tot = [(p["name"], D(c.fee_total(p)[1])) for p in a["providers"]]
    return tot, sorted(tot, key=lambda x: x[1])


def verdict_summary(a):
    wd = c.wording()
    tot, srt = verdict_lines(a)
    if srt[0][1] == srt[1][1]:
        return "%s and %s have the same total ongoing fees." % (srt[0][0], srt[1][0]), None
    diff = srt[1][1] - srt[0][1]
    s = wd["verdict_summary"].format(cheapest=srt[0][0], diff=c.fee_shown(diff), next=srt[1][0])
    ex = a["extras"]["example_fund_value"]
    if ex is not None:
        rand = (diff / 100 * w.parse_money(ex)).quantize(D("1"))
        return s, wd["verdict_example"].format(value="R " + c.money_shown(ex), rand="R " + format(int(rand), ",d"))
    return s, None


def extras(a, today):
    wd, ex, out = c.wording(), a["extras"], ""
    if ex["tax_note"]:
        if a["product_type"] == "RA":
            inner = P % E(wd["tax_ra"])
        else:
            annual, lifetime, _ok = c.tfsa_limits()
            ua, ul = w.parse_money(a["tfsa"]["annual_used"]), w.parse_money(a["tfsa"]["lifetime_used"])
            inner = P % E(wd["tax_tfsa"].format(annual="R " + c.money_shown(annual), lifetime="R " + c.money_shown(lifetime), annual_used="R " + c.money_shown(ua), lifetime_used="R " + c.money_shown(ul),
                                                annual_left="R " + c.money_shown(max(D(0), annual - ua)), lifetime_left="R " + c.money_shown(max(D(0), lifetime - ul))))
            for name, yearly, _br in c.tfsa_rows(a):
                inner += P % E(wd["tax_tfsa_provider"].format(provider=name, yearly=c.rand_whole(yearly)))
        out += section(wd["tax_ra_heading"], wd["tax_ra_intro"], inner)
    if ex["flexibility"]:
        t = TABLE + "<tr>" + th("Provider") + th("Topic") + th("What the quote says") + "</tr>\n"
        for i, p in enumerate(a["providers"]):
            for fx in p.get("flexibility") or []:
                t += "<tr>" + td(E(p["name"]), bg=pcell(i)[1], bold=True) + td(E(fx["topic"])) + td(E(fx["text"])) + "</tr>\n"
        out += section(wd["flex_heading"], wd["flex_intro"], t + "</table>\n")
    if ex["verdict"]:
        tot, _srt = verdict_lines(a)
        s1, s2 = verdict_summary(a)
        inner = "".join(P % E(wd["verdict_line"].format(provider=n, total=c.fee_shown(v))) for n, v in tot) + P % E(s1) + (P % E(s2) if s2 else "")
        out += section(wd["verdict_heading"], wd["verdict_intro"], inner)
    return out


# ------------------------------------------------------------------ filling the template
def _fill(t, ph, value):
    n = t.count(ph)
    if n != 1:
        raise ValueError("the template has %d x %s, expected 1: the template was changed" % (n, ph))
    return t.replace(ph, value)


def next_meeting_line(a):
    return c.wording()["next_meeting"].format(day=__import__("calendar").day_name[c.next_date(a).weekday()], date=c.next_date(a).strftime("%d/%m/%Y"), time=E(a["next_meeting"]["time"].strip()))


def values(a, sent, today):
    wd = c.wording()
    return {"[DATE AND TIME SENT]": E(sent), "[CLIENT EMAIL]": E(a["client_email"].strip()), "[CC NAME(S)]": E(c.CC_NAME), "[SUBJECT]": E(c.subject(a)), "[CLIENT FIRST NAME]": E(a["client_first_name"].strip()),
            "[MEETING DATES LIST]": E(c.meetings_line(a)), "[PRODUCT NAME]": E(wd["product_names"][a["product_type"]]), "[PROVIDERS LIST]": c.names_list([E(n) for n in c.provider_names(a)], amp="&amp;"),
            "[THINGS TO KNOW]": things_box(a, today), "[TABLE1 TITLE]": E(wd["product_titles"][a["product_type"]]), "[TABLE1 INTRO]": E(wd["intro1"]), "[TABLE1]": table1(a),
            "[TABLE2 INTRO]": E(wd["intro2"]), "[TABLE2]": table2(a), "[FEE NOTES]": fee_notes(a), "[TABLE3 INTRO]": E(wd["intro3"]), "[TABLE3]": table3(a), "[FUND NOTES]": fund_notes(a),
            "[TABLE4 INTRO]": E(wd["intro4"]), "[LOYALTY EXPLANATIONS]": loyalty_explanations(a), "[TABLE4]": table4(a), "[EXTRAS]": extras(a, today), "[NEXT MEETING LINE]": next_meeting_line(a)}


def build_all(a, sent, docs, today):
    """(full, nologo, body): the email with the logo, the saved copy without it, and the text pasted into the Outlook draft."""
    with open(c.TEMPLATE, encoding="utf-8") as fh:
        t = fh.read()
    v = values(a, sent, today)
    for ph in c.TEMPLATE_PLACEHOLDERS:
        t = _fill(t, ph, v[ph])
    left = [ph for ph in c.TEMPLATE_PLACEHOLDERS if ph in t]
    if left:
        raise ValueError("placeholders not filled: %s" % left)
    b0, b1 = t.index("<!-- BODY START -->"), t.index("<!-- BODY END -->")
    body = _to_body(t[b0 + len("<!-- BODY START -->"):b1])
    l0, l1 = t.index("<!-- LOGO START -->"), t.index("<!-- LOGO END -->")
    nologo = t[:l0] + t[l1 + len("<!-- LOGO END -->"):]
    full = t.replace("<!-- LOGO START -->", "").replace("<!-- LOGO END -->", "")
    for m in ("<!-- BODY START -->", "<!-- BODY END -->"):
        full, nologo = full.replace(m + "\n", "").replace(m, ""), nologo.replace(m + "\n", "").replace(m, "")
    return full, nologo, body


def _to_body(frag):
    frag = re.sub(r"<table[^>]*>\s*<tr><td height=\"(\d+)\"[^>]*>&nbsp;</td></tr></table>", lambda m: '<p style="margin:0;">&nbsp;</p>' if int(m.group(1)) >= 8 else "", frag)
    frag = frag.replace("<strong>", "<b>").replace("</strong>", "</b>")

    def bold_tag(m):
        style = re.sub(r"font-weight:\s*bold;?", "", m.group(3))
        return "<%s%s%s><b>%s</b></%s>" % (m.group(1), m.group(2), style, m.group(4), m.group(1))
    frag = re.sub(r'<(p|td)((?:\s[^>]*?)?)(?=[^>]*font-weight:\s*bold)([^>]*)>(.*?)</\1>', bold_tag, frag, flags=re.S)
    return frag.strip() + "\n"


def text_of(h):
    h = re.sub(r"</?(?:p|td|tr|th|table|div|li|ol|ul|br|h\d|body|html|head|title)\b[^>]*>", " ", h)
    return " ".join(html.unescape(re.sub(r"<[^>]+>", "", h)).split())


# ------------------------------------------------------------------ checks on the built email
def explanations_for(a):
    t = c.terms()
    out = list(t["fee_labels"].values()) + list(t["jargon"].values())
    for p in a["providers"]:
        out += [str(x.get("plain")) for x in (p.get("fee_lines") or []) + (p.get("initial_fees") or []) if x.get("plain")]
    return [x for x in out if x]


def jargon_problems(body, a):
    """Every industry term in the body sits in a block that explains it (its glossary explanation, a plain explanation from the answers, or a bracketed explanation next to it)."""
    t = c.terms()
    expl = explanations_for(a)
    bad = []
    blocks = re.split(r"</p>|</td>|</tr>", body)
    for blk in blocks:
        txt = text_of(blk)
        if not txt or txt == c.EAC_TITLE:
            continue
        for term, plain in t["jargon"].items():
            pat = r"\b%s\b" % re.escape(term) if term.isupper() else re.escape(term)
            for m in re.finditer(pat, txt, re.I if not term.isupper() else 0):
                near = txt[max(0, m.start() - 60):m.end() + 120]
                if "(" in near or any(x and x.lower() in txt.lower() for x in expl):
                    break
                bad.append(term)
                break
    return sorted(set(bad))


def eac_allowed():
    return len(re.findall(r"\bEAC\b", c.EAC_TITLE)) + len(re.findall(r"\bEAC\b", c.wording()["intro2"]))


def _lines(a, today):
    wd = c.wording()
    nl = "We will discuss this in further detail in our Teams Meeting on %s @ %s." % (c.fmt_date_with_day(c.next_date(a)), a["next_meeting"]["time"].strip())
    out = [wd["product_titles"][a["product_type"]], c.EAC_TITLE, "Investment Fund Comparison", "Loyalty and Value-Add Benefits", nl] + c.provider_names(a)
    out += ["%s%% p.a." % c.fee_total(p)[1] for p in a["providers"]]
    out += [f["name"] for p in a["providers"] for f in p["funds"]]
    out += [e["as_at"] for e in c.sheet_entries(a) if e.get("as_at")]
    out += c.things_to_know(a, today)
    return out


def html_problems(full, nologo, body, a, sent, docs, today):
    """The checks on the built email, as [(ok, short, detail)]."""
    R = []

    def add(ok, short, detail=""):
        R.append((bool(ok), short, detail))
    wd = c.wording()
    for nm, h in (("full copy", full), ("saved copy", nologo), ("pasted body", body)):
        add(not c.PLACEHOLDER.search(re.sub(r"base64,[A-Za-z0-9+/=]+", "", h)) and "@@" not in h, "No [PLACEHOLDER] text is left in the %s" % nm)
        add(h.count("<table") == h.count("</table>"), "Tables open = close in the %s (%d)" % (nm, h.count("<table")))
    for nm, h in (("full copy", full), ("saved copy", nologo)):
        hd = re.findall(r'<td[^>]*font-weight:bold[^>]*>(From|Sent|To|Cc|Subject|Importance):</td><td[^>]*>(.*?)</td>', h, re.S)
        hd = {k: html.unescape(v).strip() for k, v in hd}
        ok = hd.get("To") == a["client_email"].strip() and hd.get("Cc") == c.CC_NAME and hd.get("Subject") == c.subject(a) and hd.get("Importance") == "High" and hd.get("Sent") == sent
        add(ok, "The header of the %s: To = the client's email, Cc = %s, Subject exactly the draft's, Importance High, Sent filled" % (nm, c.CC_NAME) if ok else "Header problem in the %s: %s" % (nm, hd))
    bt = text_of(body)
    add(bt.startswith("Dear %s," % a["client_first_name"].strip()) and "Kind regards" not in bt and "<img" not in body and "FSP45946" not in body and "Importance:" not in bt,
        "The pasted body runs from 'Dear %s,' to the next-meeting line: no header, no signature block, no 'Kind regards,', no logo" % a["client_first_name"].strip())
    nlx = "Teams Meeting on %s @ %s." % (c.fmt_date_with_day(c.next_date(a)), a["next_meeting"]["time"].strip())
    add(bt.rstrip().endswith(nlx), "The email ends with the next meeting '%s', the weekday computed" % c.next_line(a))
    add(("Teams Meeting on %s," % c.meetings_line(a)) in bt, "The meetings already held read '%s', the weekdays computed" % c.meetings_line(a))
    titles = [wd["product_titles"][a["product_type"]], c.EAC_TITLE, "Investment Fund Comparison", "Loyalty and Value-Add Benefits"]
    pos = [bt.find(t_) for t_ in titles]
    add(all(x >= 0 for x in pos) and pos == sorted(pos), "The four tables are there, in the fixed order: %s" % "; ".join(titles))
    intros = [wd["intro1"], wd["intro2"], wd["intro3"], wd["intro4"]]
    ip = [bt.find(x) for x in intros]
    add(all(x >= 0 for x in ip) and ip == sorted(ip) and all(ip[i] > pos[i] for i in range(4)), "A short plain-English intro line sits under each table heading")
    add(len(re.findall(r"\bEAC\b", bt)) == eac_allowed(), "No EAC figure or row appears: the word is only in the fee table's title and its explanation (%d times)" % eac_allowed())
    jb = jargon_problems(body, a)
    add(not jb, "Every industry term is explained where it is used (EAC, commission, ...)" if not jb else "Industry terms used without an explanation: %s" % ", ".join(jb))
    tots = re.search(r"Total ongoing fees((?:\s[\d.]+%% p\.a\.){%d})" % len(a["providers"]), bt)
    got = re.findall(r"([\d.]+)% p\.a\.", tots.group(1)) if tots else []
    add(got == [c.fee_total(p)[1] for p in a["providers"]], "The fee table's totals add up the figures shown: %s" % ", ".join("%s %s%%" % (p["name"], c.fee_total(p)[1]) for p in a["providers"]))
    add(all(n in bt for n in c.provider_names(a)) and all(f["name"] in bt for p in a["providers"] for f in p["funds"]), "Every provider and every fund of the data file is in the email")
    miss_d = [e["as_at"] for e in c.sheet_entries(a) if e.get("as_at") and e["as_at"] not in bt]
    nf = [f for _p, f in c.not_found_sheets(a)]
    add(not miss_d and bt.count(wd["fund_not_found_cell"]) == len(nf), "Every fund shows its own fact sheet date, or 'Fact sheet not found' (%d fund(s))" % len(c.sheet_entries(a)))
    items = c.things_to_know(a, today)
    add(all(x in bt for x in items) and (bool(items) == (wd["things_heading"] in bt)),
        "The 'Things to know' box is there only when something must be flagged (%d item(s)): mismatches, a Tax-Free limit breach, a supplementary document that disagrees, a stale or missing fact sheet" % len(items))
    ex = a["extras"]
    add(((wd["verdict_heading"] in bt) == ex["verdict"]) and ((wd["flex_heading"] in bt) == ex["flexibility"]) and ((wd["tax_ra_heading"] in bt) == ex["tax_note"]),
        "The optional parts (tax note, flexibility, fees-only comparison) are there only if Paul asked for them")
    if ex["tax_note"] and a["product_type"] == "RA":
        add(wd["tax_ra"] in bt, "The tax note says the deduction is identical in law for every provider (no fake tax advantage)")
    if ex["verdict"]:
        s1, s2 = verdict_summary(a)
        add(s1 in bt and (s2 is None or s2 in bt) and all(wd["verdict_line"].format(provider=n, total=c.fee_shown(v)) in bt for n, v in verdict_lines(a)[0]),
            "The fees-only comparison is built from the fee table's totals: %s" % s1)
    add("data:image/png;base64," in full and "data:image" not in nologo and "FSP45946" in full and "FSP45946" in nologo and "Kind regards," in full and "Kind regards," in nologo,
        "The full copy carries the logo; the saved copy is the no-logo copy; both keep Paul's signature block")
    return R


# ------------------------------------------------------------------ the Teams message
def attachments(a, docs):
    wd = c.wording()
    items = [wd["teams_attach_quote"].format(provider=p["name"], file=c.no_ext(c.doc_name(docs, c.dkey("quote", p["name"])))) for p in a["providers"]]
    funds = [f["name"] for p in a["providers"] for f in p["funds"]]
    items.append(wd["teams_attach_sheets"].format(funds=c.names_list(funds)))
    for lab, k in sorted(c.docs_of(docs, "supplement").items()):
        items.append(wd["teams_attach_supplement"].format(label=lab, file=c.no_ext(c.doc_name(docs, k))))
    return items


def teams_text(a, docs, greeting):
    items = attachments(a, docs)
    lines = ["%s Sitamah," % greeting, "",
             "**Action needed:** I have compiled the draft investment comparison email to %s (%s: %s) and saved it in **Drafts** (To: %s, Cc: you)." %
             (a["client_full_name"].strip(), a["product_type"], " vs ".join(c.provider_names(a)), a["client_email"].strip()), "", "Please kindly attach the following to that draft:"]
    lines += ["%d. %s" % (i, x) for i, x in enumerate(items, 1)]
    lines += ["", "All of them are in %s's folder: %s > Comparative Quotes." % (a["client_first_name"].strip(), a["plan_folder"].strip()), "", "Once attached, please email the client - Thank you!"]
    return "\n".join(lines)


# ------------------------------------------------------------------ what comes back from Outlook and Teams
def flatten(text):
    try:
        obj = json.loads(text)
    except ValueError:
        return text, None, [text]
    out = []

    def walk(x):
        if isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
        elif isinstance(x, str):
            out.append(x)
    walk(obj)
    return "\n".join(out), obj, out


def find_key(obj, names):
    names = {n.lower() for n in names}
    found = []

    def walk(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if k.lower() in names:
                    found.append(v)
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(obj)
    return found


def _emails(x):
    return {e.lower() for e in re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", json.dumps(x))}


def draft_problems(text, a, today, sig_mode):
    flat, obj, leaves = flatten(text)
    R = []

    def add(ok, short):
        R.append((bool(ok), short))
    to_v = find_key(obj, ("toRecipients", "to")) if obj is not None else []
    cc_v = find_key(obj, ("ccRecipients", "cc")) if obj is not None else []
    client = a["client_email"].strip().lower()
    if to_v or cc_v:
        to_set, cc_set = set().union(*[_emails(x) for x in to_v]) if to_v else set(), set().union(*[_emails(x) for x in cc_v]) if cc_v else set()
        add(client in to_set and c.CC_EMAIL in cc_set and c.CC_EMAIL not in to_set, "To = the client (%s) and Cc = %s, read back from the saved draft" % (a["client_email"].strip(), c.CC_NAME))
    else:
        add(client in flat.lower() and c.CC_EMAIL in flat.lower(), "The client (%s) and %s are on the draft (the read-back has no separate To and Cc fields)" % (a["client_email"].strip(), c.CC_NAME))
    subs = [x for x in (find_key(obj, ("subject",)) if obj is not None else []) if isinstance(x, str)]
    add((c.subject(a) in subs) if subs else (c.subject(a) in flat), "The subject is exactly the one in the HTML")
    imp = [x for x in (find_key(obj, ("importance",)) if obj is not None else []) if isinstance(x, str)]
    add((imp and imp[0].lower() == "high") if imp else bool(re.search(r"importance\W{1,6}high", flat, re.I)), "Importance is High")
    cands = [x for x in leaves if "Dear " in x and "<" in x]
    body = max(cands, key=len) if cands else flat
    add(body.count("<table") == body.count("</table>"), "Tables open = close in the saved draft (%d)" % body.count("<table"))
    kr = body.count("Kind regards,")
    add(kr == (1 if sig_mode == "insert" else 0), "'Kind regards,' appears %d time(s) (%s)" % (kr, "exactly once, from the inserted signature" if sig_mode == "insert" else "none: the server adds the signature"))
    add(not c.PLACEHOLDER.search(body) and "@@" not in body and "BODY_PLACEHOLDER" not in body, "No placeholder text is left in the draft (not even BODY_PLACEHOLDER)")
    add(not re.search(r"\bLoop\b", flat), "No Loop component is in the draft")
    bt = text_of(body)
    bold = len(re.findall(r"<(?:b|strong)[ >]", body))
    add(bold >= 4, "The headings, the header rows and the next-meeting line are bold (%d bold tags)" % bold)
    need = ["Dear %s," % a["client_first_name"].strip(), c.meetings_line(a), c.next_line(a)] + _lines(a, today)
    miss = [x for x in need if x not in bt]
    add(not miss, "The draft carries the client's name, the dates, the four tables, every provider, fund, total and date as the email phrases them" if not miss else "Missing from the draft: %s" % miss[0][:100])
    return R


def message_problems(text, a, docs, greeting):
    flat, _obj, leaves = flatten(text)
    R = []

    def add(ok, short):
        R.append((bool(ok), short))
    cands = [x for x in leaves if "Sitamah" in x]
    flat = max(cands, key=len) if cands else flat
    plain = text_of(flat)
    n = len(attachments(a, docs))
    add(plain.startswith("%s Sitamah," % greeting), "The message opens with the greeting '%s Sitamah,'" % greeting)
    add("<strong>Action needed:</strong>" in flat and "<strong>Drafts</strong>" in flat, "'Action needed:' and 'Drafts' are bold (real <strong> tags)")
    add("<ol>" in flat and flat.count("<li>") == n, "The documents are a real numbered list (%d items)" % n)
    add("**" not in flat and "&lt;" not in flat and "\\u003c" not in flat, "No literal ** and no escaped tags show")
    quotes_ok = all(c.no_ext(c.doc_name(docs, c.dkey("quote", p["name"]))) in plain for p in a["providers"])
    add(quotes_ok and ("%s > Comparative Quotes" % a["plan_folder"].strip()) in plain, "The message names every provider's quote and the folder (%s > Comparative Quotes)" % a["plan_folder"].strip())
    add(plain.rstrip().endswith("Once attached, please email the client - Thank you!") and "do not send" not in plain.lower() and "leave it in drafts" not in plain.lower(),
        "It ends 'Once attached, please email the client - Thank you!' with no 'do not send' line")
    return R


# ------------------------------------------------------------------ the confirmation table
GREETING_MARK = "<greeting by the clock>"


def table_rows(a, docs, today):
    s = a.get("sources") or {}
    wd = c.wording()
    sig = "inserted by Claude (Paul K New)" if c.settings()["signature_mode"] == "insert" else "added by the Exchange rule"
    rows = [("Client (greeting, full name)", "%s (%s)" % (a["client_full_name"], a["client_first_name"]), s.get("personal")),
            ("Product compared; client's risk profile", "%s; %s" % (a["product_type"], a["risk_profile"]), s.get("risk"))]
    for p in a["providers"]:
        rows.append(("%s: plan, contribution, yearly increase, term" % p["name"], "%s; %s; %s; %s" % (p["product_name"], contribution_text(p), escalation_text(p), p["term"]), s.get("providers")))
        rows.append(("%s: funds (allocation, asset management fee)" % p["name"], "; ".join("%s %s%% (%s%%)" % (f["name"], c.pct_digits(f["allocation"]), c.pct_digits(f["asset_mgmt_fee"])) for f in p["funds"]), s.get("funds")))
        comps, total = c.fee_total(p)
        rows.append(("%s: ongoing fees (blended asset management first, then the quote's own lines); total" % p["name"],
                     "%s%%; %s; total %s%% p.a." % (comps[0], "; ".join("%s %s%%" % (ln["label"], x) for ln, x in zip(p["fee_lines"], comps[1:])), total), s.get("fees")))
    ents = c.sheet_entries(a)
    rows.append(("Fund fact sheets (own date each)", "; ".join(("%s: not found" % e["fund"]) if e.get("not_found") else "%s: %s, 1/3/5 years %s / %s / %s" % (e["fund"], e["as_at"], e["perf_1y"], e["perf_3y"], e["perf_5y"]) for e in ents), "the saved fact sheet texts"))
    mm = c.mismatches(a)
    rows.append(("Apples-to-apples (contribution structure, amount, yearly increase, term)", "all the same" if not mm else "; ".join("%s: %s" % (f, d) for f, d in mm), "the quotes"))
    if a["product_type"] == "TFSA":
        rows.append(("Tax-Free room (first year)", "; ".join("%s %s%s" % (n, c.rand_whole(y), " (over the %s limit)" % ", ".join(b[0] for b in br) if br else " (within the limits)") for n, y, br in c.tfsa_rows(a)), s.get("tfsa")))
    for prov, lab, field, qv, sv, dt in c.supplement_items(a):
        rows.append(("Supplementary document differs from the quote", "%s: %s says %s, the quote says %s (%s)" % (prov, lab, sv, qv, dt), s.get("supplement")))
    ex = a["extras"]
    rows.append(("Extras you asked for", "verdict %s; tax note %s; flexibility %s%s" % ("yes" if ex["verdict"] else "no", "yes" if ex["tax_note"] else "no", "yes" if ex["flexibility"] else "no",
                 "; example fund value %s" % ex["example_fund_value"] if ex["example_fund_value"] else ""), "Paul's answer"))
    rows += [("Client email (To)", a["client_email"], s.get("email")), ("Meetings already held", c.meetings_line(a), s.get("meetings")), ("Next Teams meeting", c.next_line(a), s.get("next_meeting")),
             ("Subject", c.subject(a), "built by the program"), ("Cc", "%s (%s)" % (c.CC_NAME, c.CC_EMAIL), "fixed"),
             ("Client's folder for the saved copy", "%s > Comparative Quotes" % a["plan_folder"], "the client's file"), ("Signature in the Outlook draft", sig, "settings.json; the question is still open with Paul")]
    own = len(a.get("flags") or [])
    fl = c.paul_flags(a, today)
    rows += [("Flag", x, "the chat" if i >= len(fl) - own else "the program") for i, x in enumerate(fl)]
    rows.append(("Teams message to Sitamah (sent only after the draft is checked; the greeting is set by the clock when it is sent)", teams_text(a, docs, GREETING_MARK), "fixed wording"))
    return rows
