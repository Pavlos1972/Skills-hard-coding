#!/usr/bin/env python3
"""The emails of om-optimal-ra-proposal: the main proposal and the separate Lump Sum Investment proposal built from the fixed templates, the checks on what was built, the
Teams message to Sitamah, the checks on what comes back from Outlook and Teams, and the confirmation table. Pure functions of the answers and the tool results."""
import html
import json
import re
from decimal import Decimal

import ori as o
import oritax as ot
import wrlib as w

D = Decimal
CENT = D("0.01")
P = '<p style="font-size:12pt;margin:0;">%s</p>'
LABEL_TD = 'bgcolor="#c8e6c9" style="padding:4px 8px;font-size:10pt;"'
VALUE_TD = 'bgcolor="#a5d6a7" style="padding:4px 8px;font-size:10pt;font-weight:bold;text-align:right;" nowrap'


def E(s):
    return html.escape(str(s), quote=False)


# ------------------------------------------------------------------ the pieces of the main email
def input_row(label, amount_html):
    return "<tr><td %s>%s</td><td %s>R &nbsp;%s</td></tr>\n" % (LABEL_TD, E(label), VALUE_TD, amount_html)


def fund_rows(a):
    fd = o.fund_of(a)
    if fd["type"] == "none":
        return ""
    labels = o.wording()["fund_labels"][fd["type"]]
    return input_row(labels[0], o.rand_cell(fd["employer_monthly"])) + input_row(labels[1], o.rand_cell(fd["member_monthly"]))


def ra_label_existing(r):
    return o.wording()["ra_label_existing"].format(insurer=r["insurer"].strip(), policy=r["policy_number"].strip())


def existing_rows(a):
    return "".join(input_row(ra_label_existing(r), o.rand_cell(r["monthly"])) for r in a["existing_ras"])


def new_ra_row(amount):
    return input_row(o.wording()["ra_label_new"], o.rand_cell(D(amount)))


def t1_ra_rows(a):
    return existing_rows(a) if a["existing_ras"] else input_row(o.wording()["ra_label_none"], "&#8211;")


def t3_ra_rows(a, ctx):
    return (existing_rows(a) if a.get("ra_decision") == "keep" else "") + new_ra_row(ctx["proposed"])


def ra_rows(a):
    reco = o.wording()["recommendation"][a["ra_decision"]]
    note = o.wording()["penalty_note"]
    rows = []
    for r in a["existing_ras"]:
        extra = "<br><i>%s</i>" % note if r["no_penalties"] else ""
        rows.append('  <tr>\n    <td style="padding:5px 10px;">%s</td>\n    <td style="padding:5px 10px;">%s</td>\n    <td style="padding:5px 10px;">R %s</td>\n'
                    '    <td style="padding:5px 10px;">R %s (%s)</td>\n    <td style="padding:5px 10px;">%s%s</td>\n  </tr>\n' %
                    (E(r["insurer"].strip()), E(r["policy_number"].strip()), o.money_shown(r["monthly"]), o.money_shown(r["gross_value"]), E(r["value_date"].strip()), reco, extra))
    return "".join(rows)


def pension_block(a):
    wd = o.wording()
    fd = o.fund_of(a)
    if fd["type"] == "none":
        return P % wd["no_fund"]
    txt = wd["fund_block"].format(type=fd["type"].capitalize(), employer=E(a["employer"].strip()), employer_amount=o.money_shown(fd["employer_monthly"]),
                                  employer_pct=o.pct_digits(fd["employer_pct"]), member_amount=o.money_shown(fd["member_monthly"]), member_pct=o.pct_digits(fd["member_pct"]),
                                  value=o.money_shown(fd["value"]), date=E(fd["value_date"].strip()))
    return '<p style="font-size:12pt;font-weight:bold;margin:0;">%s</p>' % txt


def total_cap_monthly(tax):
    return (ot.out(tax, "t1", "cap") / 12).quantize(CENT)


def save_sentence(a, tax):
    return P % o.wording()["save_sentence"][o.fund_of(a)["type"] if o.fund_of(a)["type"] != "none" else "none"].format(total=o.money_shown(total_cap_monthly(tax)))


def rgar_paragraph(a):
    wd = o.wording()
    rg = a.get("rgar")
    if rg is None:
        return P % wd["no_rgar"]
    return P % wd["rgar"].format(shortfall=o.money_shown(rg["shortfall"]), years=int(w.parse_money(rg["years"])), current=o.money_shown(rg["current_value"]),
                                 future=o.money_shown(rg["future_value"]), age=int(w.parse_money(rg["retirement_age"])))


def orange_message(tax, run):
    wd = o.wording()
    left = ot.out(tax, run, "pct_left")
    return wd["still_use"].format(pct=o.pct_shown(left)) if D(o.pct_shown(left)) > 0 else wd["maximised"]


def funds_sentence(a):
    names = [E(f["name"].strip()) for f in a["funds"]]
    wd = o.wording()
    return (wd["funds_one"] if len(names) == 1 else wd["funds_many"]).format(names=o.names_list(names, the=True, amp="&amp;"))


def fund_table_rows(a):
    return "".join('  <tr><td style="font-size:10pt;padding:4px 12px 4px 24px;">&#8211; %s</td><td style="font-size:10pt;padding:4px 12px;text-align:right;">%s%%</td></tr>\n' %
                   (E(f["name"].strip()), o.pct_digits(f["allocation"])) for f in a["funds"])


def next_meeting_line(a):
    return o.wording()["next_meeting"].format(day=__import__("calendar").day_name[o.next_date(a).weekday()], date=o.next_date(a).strftime("%d/%m/%Y"), time=E(a["next_meeting"]["time"].strip()))


def fees_of(a):
    """(the four fee components as shown, their total as shown): the total adds up the SHOWN figures, so the client's own addition checks out."""
    comps = [o.blended_fee(a)] + [o.pct_decimal(a[k]) for k in ("net_admin_fee", "advice_fee", "adviser_charge")]
    shown = [o.fee_shown(x) for x in comps]
    return shown, o.fee_shown(sum((D(x) for x in shown), D(0)))


def main_values(a, sent, docs, tax):
    ctx = o.tool_context(a)
    wd = o.wording()
    t1o, t2o, t3o = (tax["runs"][k]["outputs"] for k in ("t1", "t2", "t3"))
    ft = o.fund_of(a)["type"]
    fee_parts, fee_total = fees_of(a)
    mx = ctx["max_ra"].quantize(CENT)
    v = {"[DATE AND TIME SENT]": E(sent), "[CLIENT EMAIL]": E(a["client_email"].strip()), "[CC NAME(S)]": E(o.CC_NAME), "[SUBJECT]": E(o.subject(a)),
         "[CLIENT FIRST NAME]": E(a["client_first_name"].strip()), "[MEETING DATES LIST]": E(o.meetings_line(a)), "[AGE]": str(a["age"]), "[EMPLOYER NAME]": E(a["employer"].strip()),
         "[POSITION]": E(a["position"].strip()), "[GROSS MONTHLY INCOME]": o.money_shown(a["gross_monthly_income"]), "[MONTHLY REMUNERATION]": o.money_shown(a["gross_monthly_income"]),
         "[RA_ROWS]": ra_rows(a) if a["existing_ras"] else "", "[PENSION_BLOCK]": pension_block(a), "[SAVE SENTENCE]": save_sentence(a, tax), "[RGAR PARAGRAPH]": rgar_paragraph(a),
         "[PROPOSED PREMIUM]": o.premium_of(a), "[PRODUCT START DATE]": E(a["start_date"].strip()),
         "[T1_FUND_ROWS]": fund_rows(a), "[T1_RA_ROWS]": t1_ra_rows(a), "[T1 ANNUAL TAX SAVED RA]": o.rand_cell(t1o["tax_saved_ra"], True),
         "[FUND TAX LABEL]": wd["fund_tax_label"].get(ft, ""), "[TAX SAVED FUND]": o.rand_cell(t1o["tax_saved_pension" if ft == "pension" else "tax_saved_provident"], True),
         "[T1 ANNUAL TAX PAYABLE]": o.rand_cell(t1o["tax_payable"], True), "[T1 PCT REMAINING]": o.pct_shown(t1o["pct_left"]),
         "[T1 ADDITIONAL MONTHLY PREMIUM]": o.rand_cell(t1o["additional_monthly"]), "[T1 LUMP SUM]": o.rand_cell(t1o["lump_sum"]), "[T1 MESSAGE]": orange_message(tax, "t1"),
         "[MAXIMUM CONTRIBUTION]": o.money_shown(mx), "[T2_FUND_ROWS]": fund_rows(a), "[T2_RA_ROWS]": new_ra_row(mx), "[T2 ANNUAL TAX SAVED RA]": o.rand_cell(t2o["tax_saved_ra"], True),
         "[T2 ANNUAL TAX PAYABLE]": o.rand_cell(t2o["tax_payable"], True), "[T3_FUND_ROWS]": fund_rows(a), "[T3_RA_ROWS]": t3_ra_rows(a, ctx),
         "[T3 ANNUAL TAX SAVED RA]": o.rand_cell(t3o["tax_saved_ra"], True), "[T3 ANNUAL TAX PAYABLE]": o.rand_cell(t3o["tax_payable"], True), "[T3 PCT REMAINING]": o.pct_shown(t3o["pct_left"]),
         "[T3 ADDITIONAL MONTHLY PREMIUM]": o.rand_cell(t3o["additional_monthly"]), "[T3 LUMP SUM]": o.rand_cell(t3o["lump_sum"]), "[T3 MESSAGE]": orange_message(tax, "t3"),
         "[FUNDS SENTENCE]": funds_sentence(a), "[FUND_ROWS]": fund_table_rows(a), "[ASSET MGMT FEE]": fee_parts[0], "[NET ADMIN FEE]": fee_parts[1],
         "[ADVICE FEE]": fee_parts[2], "[ADVISER CHARGE]": fee_parts[3],
         "[TOTAL ONGOING FEES]": fee_total, "[MONTHLY ADMIN FEE]": o.money_shown(a["monthly_admin_fee"]),
         "[FUND NAMES LIST]": o.names_list([E(f["name"].strip()) for f in a["funds"]], amp="&amp;"), "[NEXT MEETING LINE]": next_meeting_line(a)}
    for i, b in enumerate(ot.bars(tax), 1):
        v["[BAR_%d]" % i] = "R " + o.rand0(b)
    regions = {}
    if not a["existing_ras"]:
        regions["RA TABLE"] = P % wd["no_ra"]
    if ft == "none":
        regions["FUND TAX"] = ""
    return v, regions


# ------------------------------------------------------------------ the pieces of the lump sum email
def sources_text(a):
    return o.names_list([E(p["name"].strip()) for p in a["lump"]["policies"]], amp="&amp;")


def lump_block(a):
    wd = o.wording()
    lp = a["lump"]
    if lp["type"] == "section14":
        return P % wd["lump_section14"].format(amount=o.money_shown(lp["amount"]), sources=sources_text(a))
    return P % wd["lump_voluntary"].format(amount=o.money_shown(lp["amount"]), source=E(lp["source_of_funds"].strip()))


def lump_tax_note(a):
    lp = a["lump"]
    return P % (o.wording()["lump_tax_section14"] if lp["type"] == "section14" else E(lp["tax_note"].strip()))


def ls_fee_value(v):
    v = str(v).strip()
    return v if v.lower() == "none" or "%" in v else v + "%"


def lump_fund_fee_block(a):
    fe = a["ls_fees"]
    funds = ('<table cellpadding="5" cellspacing="0" border="1" bordercolor="#cccccc" style="border-collapse:collapse;">\n  <tr>\n'
             '    <td bgcolor="#1a5c38" style="color:#ffffff;font-weight:bold;font-size:10pt;padding:5px 12px;">Investment Plan / Fund Name</td>\n'
             '    <td bgcolor="#1a5c38" style="color:#ffffff;font-weight:bold;font-size:10pt;padding:5px 12px;text-align:right;">Allocation (%)</td>\n  </tr>\n'
             '  <tr><td colspan="2" bgcolor="#f5f5f5" style="font-weight:bold;font-size:10pt;padding:4px 12px;">Optimal Investment Plan 2 (Lump Sum)</td></tr>\n' + fund_table_rows(a) + "</table>\n")
    spacer = '<table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td height="8" style="font-size:1px;line-height:8px;">&nbsp;</td></tr></table>\n'
    rows = [("Asset management fee", o.fee_shown(o.blended_fee(a)) + "%"), ("Administration fee", ls_fee_value(fe["admin_fee"])), ("Asset advice fee", ls_fee_value(fe["advice_fee"])),
            ("As-and-when advice fee", ls_fee_value(fe["as_and_when"]))]
    fees = ('<table cellpadding="7" cellspacing="0" border="1" bordercolor="#dddddd" style="border-collapse:collapse;">\n  <tr>\n'
            '    <td style="font-size:10pt;font-weight:bold;color:#444444;border-bottom:2px solid #bbbbbb;padding:6px 14px;">Fee Component</td>\n'
            '    <td style="font-size:10pt;font-weight:bold;color:#444444;text-align:right;border-bottom:2px solid #bbbbbb;padding:6px 14px;">Per annum</td>\n  </tr>\n' +
            "".join('  <tr><td style="font-size:10pt;padding:5px 14px;">%s</td><td style="font-size:10pt;text-align:right;padding:5px 14px;">%s</td></tr>\n' % (E(k), E(v)) for k, v in rows) + "</table>\n")
    return funds + spacer + fees


def lump_values(a, sent, docs, tax):
    return ({"[DATE AND TIME SENT]": E(sent), "[CLIENT EMAIL]": E(a["client_email"].strip()), "[CC NAME(S)]": E(o.CC_NAME), "[SUBJECT]": E(o.subject(a)),
             "[CLIENT FIRST NAME]": E(a["client_first_name"].strip()), "[MEETING DATES LIST]": E(o.meetings_line(a)), "[LUMP_SUM_BLOCK]": lump_block(a),
             "[PRODUCT START DATE]": E(a["start_date"].strip()), "[LS_FUND_FEE_BLOCK]": lump_fund_fee_block(a), "[LS_TAX_TREATMENT_NOTE]": lump_tax_note(a),
             "[NEXT MEETING LINE]": next_meeting_line(a)}, {})


# ------------------------------------------------------------------ filling the template
def _fill(t, ph, value):
    n = t.count(ph)
    want = o.EXPECTED_COUNT.get(ph, 1)
    if n != want:
        raise ValueError("the template has %d x %s, expected %d: the template was changed" % (n, ph, want))
    return t.replace(ph, value)


def _region(t, name, repl):
    a0, a1 = "<!-- %s START -->" % name, "<!-- %s END -->" % name
    if t.count(a0) != 1 or t.count(a1) != 1:
        raise ValueError("the template lost its %s markers" % name)
    return t[:t.index(a0)] + repl + t[t.index(a1) + len(a1):]


def build_all(a, sent, docs, tax):
    """(full, nologo, body): the email with the logo, the saved copy without it, and the text pasted into the Outlook draft."""
    doc = o.doc_of(a)
    with open(o.TEMPLATES[doc], encoding="utf-8") as fh:
        t = fh.read()
    values, regions = (main_values if doc == "main" else lump_values)(a, sent, docs, tax)
    skipped = set()
    for name, repl in regions.items():
        t = _region(t, name, repl)
        skipped |= set(o.REGION_PLACEHOLDERS.get(name, ()))
    for ph in (o.MAIN_PLACEHOLDERS if doc == "main" else o.LUMP_PLACEHOLDERS):
        if ph in skipped:
            continue
        t = _fill(t, ph, values[ph])
    left = [ph for ph in (o.MAIN_PLACEHOLDERS if doc == "main" else o.LUMP_PLACEHOLDERS) + tuple(o.EXPECTED_COUNT) if ph in t]
    if left:
        raise ValueError("placeholders not filled: %s" % left)
    for name in o.MARKERS[doc]:
        if name in ("BODY", "LOGO"):
            continue
        for end in ("START", "END"):
            t = t.replace("<!-- %s %s -->\n" % (name, end), "").replace("<!-- %s %s -->" % (name, end), "")
    b0, b1 = t.index("<!-- BODY START -->"), t.index("<!-- BODY END -->")
    body = _to_body(t[b0 + len("<!-- BODY START -->"):b1])
    l0, l1 = t.index("<!-- LOGO START -->"), t.index("<!-- LOGO END -->")
    nologo = t[:l0] + t[l1 + len("<!-- LOGO END -->"):]
    full = t.replace("<!-- LOGO START -->", "").replace("<!-- LOGO END -->", "")
    for m in ("<!-- BODY START -->", "<!-- BODY END -->"):
        full, nologo = full.replace(m + "\n", "").replace(m, ""), nologo.replace(m + "\n", "").replace(m, "")
    return full, nologo, body


def _to_body(frag):
    """The part pasted into the Outlook draft: <b> not <strong>, a blank line where the template has a spacer, no header, no signature."""
    frag = re.sub(r"<table[^>]*>\s*<tr><td height=\"(\d+)\"[^>]*>&nbsp;</td></tr></table>", lambda m: '<p style="margin:0;">&nbsp;</p>' if int(m.group(1)) >= 8 else "", frag)
    frag = frag.replace("<strong>", "<b>").replace("</strong>", "</b>")

    def bold_tag(m):
        style = re.sub(r"font-weight:\s*bold;?", "", m.group(2))
        return "<%s%s><b>%s</b></%s>" % (m.group(1), style, m.group(3), m.group(1))
    # Outlook drops font-weight on paste: a heading that is bold by style becomes a real <b>
    frag = re.sub(r'<(p|td)(?=[^>]*font-weight:\s*bold)([^>]*)>(.*?)</\1>', bold_tag, frag, flags=re.S)
    return frag.strip() + "\n"


def text_of(h):
    """Readable text of some HTML: block tags become a space, inline tags (b, strong, span...) vanish, so '<b>x</b>,' reads 'x,'."""
    h = re.sub(r"</?(?:p|td|tr|th|table|div|li|ol|ul|br|h\d|body|html|head|title)\b[^>]*>", " ", h)
    return " ".join(html.unescape(re.sub(r"<[^>]+>", "", h)).split())


# ------------------------------------------------------------------ the sentences the built email must carry
def _lines(a, tax):
    wd = o.wording()
    nl = "We will discuss this in further detail in our Teams Meeting on %s @ %s." % (o.fmt_date_with_day(o.next_date(a)), a["next_meeting"]["time"].strip())
    if o.doc_of(a) == "lump_sum":
        lp = a["lump"]
        first = (text_of(lump_block(a)))
        return [first, text_of(lump_tax_note(a)), "effective date of %s" % a["start_date"].strip(), nl] + [f["name"].strip() for f in a["funds"]]
    ft = o.fund_of(a)["type"]
    lines = ["You are %d years old." % a["age"], "You are working at %s in the position of %s." % (a["employer"].strip(), a["position"].strip()),
             "You have a gross income of R %s per month." % o.money_shown(a["gross_monthly_income"]), text_of(rgar_paragraph(a)),
             "You have indicated that you are able to contribute R %s per month towards your retirement planning." % o.premium_of(a),
             "starting on: %s." % a["start_date"].strip(), text_of(save_sentence(a, tax)), text_of(pension_block(a)),
             "In addition, a monthly fixed administration fee of R %s per month" % o.money_shown(a["monthly_admin_fee"]), nl] + [
                 "Annual Tax Payable After Deductions and Rebate R %s" % o.rand0(ot.out(tax, k, "tax_payable")) for k in ("t1", "t2", "t3")]
    if not a["existing_ras"]:
        lines.append(wd["no_ra"])
    return lines


def html_problems(full, nologo, body, a, sent, docs, tax):
    """The checks on the built email, as [(ok, short, detail)] (audit check 9 and the template rules)."""
    R = []

    def add(ok, short, detail=""):
        R.append((bool(ok), short, detail))
    doc = o.doc_of(a)
    for nm, h in (("full copy", full), ("saved copy", nologo), ("pasted body", body)):
        add(not o.PLACEHOLDER.search(re.sub(r"base64,[A-Za-z0-9+/=]+", "", h)) and "@@" not in h, "No [PLACEHOLDER] text is left in the %s" % nm)
        add(h.count("<table") == h.count("</table>"), "Tables open = close in the %s (%d)" % (nm, h.count("<table")))
    for nm, h in (("full copy", full), ("saved copy", nologo)):
        hd = re.findall(r'<td[^>]*font-weight:bold[^>]*>(From|Sent|To|Cc|Subject|Importance):</td><td[^>]*>(.*?)</td>', h, re.S)
        hd = {k: html.unescape(v).strip() for k, v in hd}
        ok = hd.get("To") == a["client_email"].strip() and hd.get("Cc") == o.CC_NAME and hd.get("Subject") == o.subject(a) and hd.get("Importance") == "High" and hd.get("Sent") == sent
        add(ok, "The header of the %s: To = the client's email, Cc = %s, Subject exactly the draft's, Importance High, Sent filled" % (nm, o.CC_NAME) if ok else
            "Header problem in the %s: %s" % (nm, hd))
    bt = text_of(body)
    add(bt.startswith("Dear %s," % a["client_first_name"].strip()) and "Kind regards" not in bt and "<img" not in body and "FSP45946" not in body and "Importance:" not in bt,
        "The pasted body runs from 'Dear %s,' to the next-meeting line: no header, no signature block, no 'Kind regards,', no logo" % a["client_first_name"].strip())
    nlx = "Teams Meeting on %s @ %s." % (o.fmt_date_with_day(o.next_date(a)), a["next_meeting"]["time"].strip())
    add(bt.rstrip().endswith(nlx), "The email ends with the next meeting '%s', the weekday computed" % o.next_line(a))
    add(("Teams Meeting on %s," % o.meetings_line(a)) in bt, "The meetings already held read '%s', the weekdays computed" % o.meetings_line(a))
    miss = [x for x in _lines(a, tax) if x not in bt]
    add(not miss, "Every figure and fixed sentence of the email is there as the rules phrase it" if not miss else "Missing from the email: %s" % miss[0][:100])
    add("data:image/png;base64," in full and "data:image" not in nologo and "FSP45946" in full and "FSP45946" in nologo and "Kind regards," in full and "Kind regards," in nologo,
        "The full copy carries the logo; the saved copy is the no-logo copy; both keep Paul's signature block")
    if doc == "main":
        ft = o.fund_of(a)["type"]
        add("You will be working" not in bt and "You are working at" in bt, "The personal circumstances read 'You are working at ...' (the stale 'You will be working' is gone)")
        wrong = {"pension": "Provident Fund", "provident": "Pension Fund"}.get(ft)
        add(not wrong or wrong not in bt, "%s" % ("The fund is labelled %s everywhere and never %s" % (ft.capitalize(), wrong.split()[0]) if wrong else "No fund rows or fund tax line are shown (self-employed or no fund)"))
        pays = re.findall(r"Annual Tax Payable After Deductions and Rebate R (\d[\d,]*)", bt)
        add(pays == [o.rand0(ot.out(tax, k, "tax_payable")) for k in ("t1", "t2", "t3")], "Tables 1, 2 and 3 carry the tool's tax payable (%s), in that order" % ", ".join("R " + x for x in pays))
        svd = re.findall(r"Annual Tax Saved from RA Deduction R (\d[\d,]*|–)", bt)
        add(svd == [("–" if ot.out(tax, k, "tax_saved_ra") == 0 else o.rand0(ot.out(tax, k, "tax_saved_ra"))) for k in ("t1", "t2", "t3")], "Tables 1, 2 and 3 carry the tool's tax saved from the RA")
        m = re.search(r"Yr 10 ((?:R \d[\d,]* ?){10})", bt)
        vals = re.findall(r"R (\d[\d,]*)", m.group(1)) if m else []
        add(vals == [o.rand0(b) for b in ot.bars(tax)], "The bar chart carries the tool's ten yearly values (year 1 R %s)" % (vals[0] if vals else "?"))
        add(("Maximum Deduction Left to Use %s%%" % o.pct_shown(ot.out(tax, "t3", "pct_left"))) in bt, "Table 3 shows the tool's 'maximum deduction left' of %s%%" % o.pct_shown(ot.out(tax, "t3", "pct_left")))
        att = [x for x in ("Old Mutual Optimal Investment – RA Quote", "Old Mutual Fund Fact Sheets (%s)" % html.unescape(o.names_list([f["name"].strip() for f in a["funds"]])),
                           "Old Mutual Optimal Investment – RA Booster Value", "Old Mutual Wealth Investment Strategy Summary") if x not in bt]
        add(not att and bt.count("Retirement Goal Analysis Report") <= 1 and "5. " not in bt.split("Please see attached:")[1].split("Hoping")[0],
            "The attachments list has exactly the 4 standard items and never the RGAR" if not att else "Attachments problem: %s" % att[0])
        parts, tot = fees_of(a)
        add(all(("%s%%" % x) in bt for x in parts) and ("%s%% p.a." % tot) in bt,
            "The fees add up: blended asset management fee %s%% + the quote's other fees = total ongoing fees %s%% p.a." % (parts[0], tot))
        fixed = ("“Moderate”", "increasing at 10% per annum", "an admin charge of R 300.00", "Hoping that above is in order.", "R 430,000 per annum")
        add(all(x in bt for x in fixed), "The fixed text is there (Moderate risk profile, 10% escalation, R 300.00 admin charge, R 430,000 cap, the closing line)")
    else:
        add("Your Lump Sum Investment:" in bt and "tax" in bt.lower() and "Retirement Goal" not in bt and "Maximum Deduction" not in bt,
            "The lump sum email has its own heading and tax note, and no tax tables, bar chart or RGAR")
        lp = a["lump"]
        add(("R %s" % o.money_shown(lp["amount"])) in bt and (lp["type"] != "section14" or all(p["name"].strip() in bt for p in lp["policies"])),
            "The lump sum is R %s, %s" % (o.money_shown(lp["amount"]), "from the named source policies (Section 14)" if lp["type"] == "section14" else "from the client's own savings"))
    return R


# ------------------------------------------------------------------ the Teams message
def fact_sheet_names(a):
    return o.names_list([f["name"].strip() for f in a["funds"]])


def teams_text(a, docs, greeting):
    client = a["client_full_name"].strip()
    first = a["client_first_name"].strip()
    head = ["%s Sitamah," % greeting, ""]
    if o.doc_of(a) == "lump_sum":
        head.append("**Action needed:** I have compiled the draft Old Mutual Optimal Retirement Annuity (RA) Lump Sum Investment proposal email to %s and saved it in **Drafts** (To: %s, Cc: you)." %
                    (client, a["client_email"].strip()))
        items = ["The OM Optimal RA Lump Sum Quote (%s)" % o.no_ext(o.doc_name(docs, "lump_sum_quote")), "The relevant fund fact sheet(s) as per the Lump Sum Quote (%s)" % fact_sheet_names(a)]
        where = "Both are in %s's folder: %s > Comparative Quotes." % (first, a["plan_folder"].strip())
    else:
        head.append("**Action needed:** I have compiled the draft Old Mutual Optimal Retirement Annuity (RA) proposal email to %s and saved it in **Drafts** (To: %s, Cc: you)." %
                    (client, a["client_email"].strip()))
        items = ["The OM Optimal RA Quote (%s)" % o.no_ext(o.doc_name(docs, "quote")), "The relevant fund fact sheets as per the quote (%s)" % fact_sheet_names(a),
                 "The OM Optimal RA Booster Value document (%s)" % o.no_ext(o.doc_name(docs, "booster_doc")), "The \"OM Wealth Investment Strategy Summary\" document"]
        where = "All four are in %s's folder: %s > Comparative Quotes." % (first, a["plan_folder"].strip())
    body = ["", "Please kindly attach the following to that draft:"] + ["%d. %s" % (i, x) for i, x in enumerate(items, 1)] + ["", where, "", "Once attached, please email the client - Thank you!"]
    return "\n".join(head + body)


# ------------------------------------------------------------------ what comes back from Outlook and Teams
def flatten(text):
    """(all the strings of a saved read-back joined, the parsed object or None, the list of strings)."""
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


def draft_problems(text, a, tax, sig_mode):
    """Checks on the saved read-back of the Outlook draft: [(ok, short)]."""
    flat, obj, leaves = flatten(text)
    R = []

    def add(ok, short):
        R.append((bool(ok), short))
    to_v = find_key(obj, ("toRecipients", "to")) if obj is not None else []
    cc_v = find_key(obj, ("ccRecipients", "cc")) if obj is not None else []
    client = a["client_email"].strip().lower()
    if to_v or cc_v:
        to_set, cc_set = set().union(*[_emails(x) for x in to_v]) if to_v else set(), set().union(*[_emails(x) for x in cc_v]) if cc_v else set()
        add(client in to_set and o.CC_EMAIL in cc_set and o.CC_EMAIL not in to_set, "To = the client (%s) and Cc = %s, read back from the saved draft" % (a["client_email"].strip(), o.CC_NAME))
    else:
        add(client in flat.lower() and o.CC_EMAIL in flat.lower(), "The client (%s) and %s are on the draft (the read-back has no separate To and Cc fields)" % (a["client_email"].strip(), o.CC_NAME))
    subs = [x for x in (find_key(obj, ("subject",)) if obj is not None else []) if isinstance(x, str)]
    add((o.subject(a) in subs) if subs else (o.subject(a) in flat), "The subject is exactly the one in the HTML")
    imp = [x for x in (find_key(obj, ("importance",)) if obj is not None else []) if isinstance(x, str)]
    add((imp and imp[0].lower() == "high") if imp else bool(re.search(r"importance\W{1,6}high", flat, re.I)), "Importance is High")
    cands = [x for x in leaves if "Dear " in x and "<" in x]
    body = max(cands, key=len) if cands else flat
    add(body.count("<table") == body.count("</table>"), "Tables open = close in the saved draft (%d)" % body.count("<table"))
    kr = body.count("Kind regards,")
    add(kr == (1 if sig_mode == "insert" else 0), "'Kind regards,' appears %d time(s) (%s)" % (kr, "exactly once, from the inserted signature" if sig_mode == "insert" else "none: the server adds the signature"))
    add(not o.PLACEHOLDER.search(body) and "@@" not in body and "BODY_PLACEHOLDER" not in body, "No placeholder text is left in the draft (not even BODY_PLACEHOLDER)")
    add(not re.search(r"\bLoop\b", flat), "No Loop component is in the draft")
    bt = text_of(body)
    bold = len(re.findall(r"<(?:b|strong)[ >]", body))
    add(bold >= 2 and ("Your Lump Sum Investment:" in bt if o.doc_of(a) == "lump_sum" else "Your personal circumstances:" in bt), "The section headings and the next-meeting line are bold (%d bold tags)" % bold)
    need = ["Dear %s," % a["client_first_name"].strip(), o.meetings_line(a), o.next_line(a)] + _lines(a, tax)
    miss = [x for x in need if x not in bt]
    add(not miss, "The draft carries the client's name, the dates and every figure as the email phrases it" if not miss else "Missing from the draft: %s" % miss[0][:100])
    return R


def message_problems(text, a, docs, greeting):
    """Checks on the saved read-back of the posted Teams message: [(ok, short)]."""
    flat, _obj, leaves = flatten(text)
    R = []

    def add(ok, short):
        R.append((bool(ok), short))
    cands = [x for x in leaves if "Sitamah" in x]
    flat = max(cands, key=len) if cands else flat
    plain = text_of(flat)
    n = 2 if o.doc_of(a) == "lump_sum" else 4
    add(plain.startswith("%s Sitamah," % greeting), "The message opens with the greeting '%s Sitamah,'" % greeting)
    add("<strong>Action needed:</strong>" in flat and "<strong>Drafts</strong>" in flat, "'Action needed:' and 'Drafts' are bold (real <strong> tags)")
    add("<ol>" in flat and flat.count("<li>") == n, "The documents are a real numbered list (%d items)" % n)
    add("**" not in flat and "&lt;" not in flat and "\\u003c" not in flat, "No literal ** and no escaped tags show")
    role = "lump_sum_quote" if o.doc_of(a) == "lump_sum" else "quote"
    add(o.no_ext(o.doc_name(docs, role)) in plain and ("%s > Comparative Quotes" % a["plan_folder"].strip()) in plain and "Retirement Goal Analysis" not in plain and "RGAR" not in plain,
        "The message names the quote and the folder (%s > Comparative Quotes) and never the RGAR" % a["plan_folder"].strip())
    add(plain.rstrip().endswith("Once attached, please email the client - Thank you!") and "do not send" not in plain.lower() and "leave it in drafts" not in plain.lower(),
        "It ends 'Once attached, please email the client - Thank you!' with no 'do not send' line")
    return R


# ------------------------------------------------------------------ the confirmation table
GREETING_MARK = "<greeting by the clock>"


def table_rows(a, docs, tax):
    s = a.get("sources") or {}
    sig = "inserted by Claude (Paul K New)" if o.settings()["signature_mode"] == "insert" else "added by the Exchange rule"
    sig_row = ("Signature in the Outlook draft", sig, "settings.json; the question is still open with Paul")
    common_tail = [("Client email (To)", a["client_email"], s.get("email")), ("Meetings already held", o.meetings_line(a), s.get("meetings")), ("Next Teams meeting", o.next_line(a), s.get("next_meeting")),
                   ("Subject", o.subject(a), "built by the program"), ("Cc", "%s (%s)" % (o.CC_NAME, o.CC_EMAIL), "fixed"),
                   ("RA transaction folder (the saved copy goes in Comparative Quotes)", a["plan_folder"], "the client's file"), sig_row]
    flags = list(a.get("flags") or [])
    if o.doc_of(a) == "lump_sum":
        lp = a["lump"]
        rows = [("Client (greeting, full name)", "%s (%s)" % (a["client_full_name"], a["client_first_name"]), s.get("personal")),
                ("Lump sum", "R %s, %s" % (o.money_shown(lp["amount"]), ("Section 14 from " + ", ".join("%s (net R %s)" % (p["name"], o.money_shown(p["net_value"])) for p in lp["policies"])) if lp["type"] == "section14"
                                           else "voluntary funds: " + lp["source_of_funds"]), s.get("lump")),
                ("Tax note", o.wording()["lump_tax_section14"] if lp["type"] == "section14" else lp["tax_note"], "the rule" if lp["type"] == "section14" else "Paul's words"),
                ("Plan 2 start date", a["start_date"], s.get("quote")),
                ("Plan 2 funds (allocation, asset management fee)", "; ".join("%s %s%% (%s%%)" % (f["name"], o.pct_digits(f["allocation"]), o.pct_digits(f["asset_mgmt_fee"])) for f in a["funds"]), s.get("quote")),
                ("Plan 2 fees (blended asset management, administration, advice, as-and-when)", "%s%%; %s; %s; %s" % (o.fee_shown(o.blended_fee(a)), a["ls_fees"]["admin_fee"], a["ls_fees"]["advice_fee"],
                                                                                                                 a["ls_fees"]["as_and_when"]), s.get("quote")),
                ("Lump Sum Quote (attachment 1)", o.doc_name(docs, "lump_sum_quote"), "the registered document")] + common_tail
    else:
        ctx = o.tool_context(a)
        fd = o.fund_of(a)
        cap = ot.out(tax, "t1", "cap")
        _rows, auto = ot.audit(a, tax)
        flags = auto + flags
        rows = [("Client (greeting, full name)", "%s (%s)" % (a["client_full_name"], a["client_first_name"]), s.get("personal")),
                ("Age, employer, position", "%d; %s; %s" % (a["age"], a["employer"], a["position"]), s.get("personal")),
                ("Gross monthly income (also the tool's monthly remuneration)", "R %s" % o.money_shown(a["gross_monthly_income"]), s.get("income")),
                ("Pension / provident fund", "none" if fd["type"] == "none" else "%s: employer R %s (%s%%), member R %s (%s%%), value R %s on %s" % (
                    fd["type"], o.money_shown(fd["employer_monthly"]), o.pct_digits(fd["employer_pct"]), o.money_shown(fd["member_monthly"]), o.pct_digits(fd["member_pct"]),
                    o.money_shown(fd["value"]), fd["value_date"]), s.get("fund")),
                ("Existing retirement annuities", "none" if not a["existing_ras"] else "; ".join("%s %s R %s a month, gross R %s on %s%s" % (
                    r["insurer"], r["policy_number"], o.money_shown(r["monthly"]), o.money_shown(r["gross_value"]), r["value_date"], " (no penalties: too new)" if r["no_penalties"] else "")
                    for r in a["existing_ras"]), s.get("existing_ras")),
                ("Replace or keep the existing RA(s)", {"none": "no existing RA", "replace": "replace with the OM Optimal RA", "keep": "keep in force alongside it"}[a["ra_decision"]], s.get("ra_decision")),
                ("Retirement Goal Analysis", "not requested" if a["rgar"] is None else "shortfall R %s a month for %s years, goal R %s (future value R %s) at age %s" % (
                    o.money_shown(a["rgar"]["shortfall"]), a["rgar"]["years"], o.money_shown(a["rgar"]["current_value"]), o.money_shown(a["rgar"]["future_value"]), a["rgar"]["retirement_age"]), s.get("rgar")),
                ("Proposed premium; plan start date", "R %s a month; %s" % (o.premium_of(a), a["start_date"]), s.get("quote")),
                ("Funds (allocation, asset management fee)", "; ".join("%s %s%% (%s%%)" % (f["name"], o.pct_digits(f["allocation"]), o.pct_digits(f["asset_mgmt_fee"])) for f in a["funds"]), s.get("funds_fees")),
                ("Fees: asset management (blended by the program), net administration, advice, adviser charge; total; monthly fixed fee",
                 "%s%%, %s%%, %s%%, %s%%; total %s%%; R %s a month" % (tuple(fees_of(a)[0]) + (fees_of(a)[1], o.money_shown(a["monthly_admin_fee"]))), s.get("funds_fees")),
                ("Tax Reform Tool: yearly cap; the monthly cap (the 'what you can save' figure); the maximum RA a month", "R %s; R %s; R %s" % (o.rand0(cap), o.money_shown(total_cap_monthly(tax)), o.money_shown(ctx["max_ra"].quantize(CENT))), "run by the program (LibreOffice)"),
                ("Table 1 (now): tax payable; tax saved from the RA", "R %s; R %s" % (o.rand0(ot.out(tax, "t1", "tax_payable")), o.rand0(ot.out(tax, "t1", "tax_saved_ra"))), "the tool"),
                ("Table 2 (maximum): tax payable; tax saved from the RA", "R %s; R %s" % (o.rand0(ot.out(tax, "t2", "tax_payable")), o.rand0(ot.out(tax, "t2", "tax_saved_ra"))), "the tool"),
                ("Table 3 (proposed): tax payable; tax saved from the RA; deduction left", "R %s; R %s; %s%%" % (o.rand0(ot.out(tax, "t3", "tax_payable")), o.rand0(ot.out(tax, "t3", "tax_saved_ra")),
                                                                                                           o.pct_shown(ot.out(tax, "t3", "pct_left"))), "the tool"),
                ("Lump sum as well (a second, separate email)", "yes" if a["lump_sum_applies"] else "no", "Paul's answer"),
                ("Optimal Illustrator (attachment 3)", o.doc_name(docs, "booster_doc"), "the registered document"), ("OM Optimal RA Quote (attachment 1)", o.doc_name(docs, "quote"), "the registered document")] + common_tail
    n_auto = len(flags) - len(a.get("flags") or [])
    rows += [("Flag", x, "the program" if i < n_auto else "the chat") for i, x in enumerate(flags)]
    rows.append(("Teams message to Sitamah (sent only after the draft is checked; the greeting is set by the clock when it is sent)", teams_text(a, docs, GREETING_MARK), "fixed wording"))
    return rows


def all_flags(a, tax):
    return (ot.audit(a, tax)[1] if o.doc_of(a) == "main" and tax else []) + list(a.get("flags") or [])
