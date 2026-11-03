#!/usr/bin/env python3
"""The domain model of the OM Tax-Free proposal: the answers (every figure checked against the documents' text), the email built from the fixed
template, the Teams message to Sitamah, the file names, the confirmation table, and the checks of what comes back (the draft and the posted message).

Everything here is a pure function of the answers (answers.json) and the stored build time, so the checker can recompute it and refuse a file edited
by hand. Rules are Paul's (the old skill, kept) and his answers of 03/11/2026. Nothing here sends anything.
"""
import html
import json
import os
import re
from decimal import Decimal

import tax_free_dates as td
import wrlib as w

ASSETS = os.path.join(w.SKILL_DIR, "assets")
TEMPLATE = os.path.join(ASSETS, "OM_TaxFree_Proposal_TEMPLATE.html")
FACTS = os.path.join(ASSETS, "tax_facts.json")
SETTINGS = os.path.join(ASSETS, "settings.json")

CC_NAME = "Sitamah Nathoo"
CC_EMAIL = "admin@liferisk.co.za"
SITAMAH_CHAT = "19:bd2a130a-35d9-459e-9025-55f356810236_e6901cee-de73-46d9-88a5-5e4a1c296418@unq.gbl.spaces"
CHAT_LABEL = "(1:1 Chat) Paul Kafentzis, Sitamah Nathoo"

FIXED_ROLES = ("quote", "fact_find_summary", "fact_find_summary_older", "risk_questionnaire", "overview", "strategy_summary")
SERVED_ROLES = ("quote", "fact_find_summary", "fact_find_summary_older", "risk_questionnaire", "overview")
ALWAYS_NEEDED = ("quote", "fact_find_summary")
FEE_KEYS = ("asset_management", "administration", "advice", "adviser_remuneration")
FEE_LABEL = {"asset_management": "Asset management fee", "administration": "Net administration fee", "advice": "Ongoing advice fee", "adviser_remuneration": "Adviser remuneration account charge"}
SOURCE_KEYS = ("quote", "personal", "risk", "email", "meetings", "next_meeting", "start_date")
ANSWER_KEYS = {"client_full_name", "client_first_name", "client_surname", "owner_full_name", "owner_is_child", "plan_type", "owner_age", "employer", "position",
               "gross_monthly_income", "contribution", "start_date", "start_date_choice", "risk_profile", "risk_profile_source", "risk_paul_said", "ffs_risk_profile",
               "funds", "fees", "fund_sheets", "client_email", "email_source", "email_note", "meetings_held", "next_meeting", "plan_folder", "flags", "sources", "conflicts"}
PLACEHOLDER = re.compile(r"\[[A-Z][A-Z0-9 %().,/&#-]*\]")
EXPECTED_COUNT = {"[CONTRIBUTION AMOUNT]": 2, "[ANNUAL LIMIT]": 2}
SINGLE = ("[DATE AND TIME SENT]", "[CLIENT EMAIL]", "[CC EMAIL]", "[SUBJECT]", "[CLIENT FIRST NAME]", "[MEETING DATE(S) WITH DAY]", "[AGE]", "[EMPLOYER NAME]", "[POSITION]",
          "[GROSS MONTHLY INCOME]", "[START DATE DD/MM/YYYY]", "[RISK PROFILE]", "[ASSET MGMT FEE]", "[ADMIN FEE]", "[ONGOING ADVICE FEE]", "[ADVISER REMUNERATION]", "[TOTAL FEES]",
          "[LIFETIME LIMIT]", "[EXCESS TAX RATE]", "[NEXT MEETING DATE WITH DAY]", "[TIME]")


def valid_role(role):
    return role in FIXED_ROLES or re.fullmatch(r"fund_fact_sheet(_\d+)?", role or "") is not None


def is_sheet(role):
    return re.fullmatch(r"fund_fact_sheet(_\d+)?", role or "") is not None


def can_be_missing(role):
    return role in ("fact_find_summary_older", "risk_questionnaire", "overview", "strategy_summary") or is_sheet(role) or role == "fund_fact_sheet"


def facts():
    with open(FACTS, encoding="utf-8") as f:
        return json.load(f)


def settings():
    with open(SETTINGS, encoding="utf-8") as f:
        return json.load(f)


# ------------------------------------------------------------------ values
def money_shown(v):
    """Rand with thousands commas; cents only when the source figure showed cents ('match the document's own formatting')."""
    d = w.parse_money(v)
    if d is None:
        return str(v)
    cents = bool(re.search(r"[.,]\d{2}\s*$", str(v).strip())) or d != d.to_integral_value()
    return format(d, ",.2f") if cents else format(int(d), ",d")


def pct_digits(v):
    return str(v).replace("%", "").strip().replace(" ", "").replace(",", ".")


def pct_shown(v):
    return pct_digits(v) + "%"


def pct_decimal(v):
    try:
        return Decimal(pct_digits(v))
    except Exception:
        return None


def total_fees(a):
    parts = [pct_decimal(a["fees"][k]) for k in FEE_KEYS]
    return format(sum(parts), "f")


def allocation_total(a):
    return sum(pct_decimal(f["allocation"]) for f in a["funds"])


def dates_of(lst):
    return sorted(w.parse_date(x) for x in lst)


def meetings_line(a):
    return td.format_meeting_dates_list(dates_of(a["meetings_held"]))


def next_line(a):
    return "%s @ %s" % (td.format_date_with_day(w.parse_date(a["next_meeting"]["date"])), a["next_meeting"]["time"].strip())


def subject(a):
    return "%s / Old Mutual Tax Free Investment Proposal – R %s p.m." % (a["client_full_name"].strip(), money_shown(a["contribution"]))


def sent_text(clock):
    return "%s, %s %s" % (td.calendar.day_name[clock.weekday()], clock.strftime("%d/%m/%Y"), clock.strftime("%H:%M"))


def file_name(a, d):
    first = a["client_first_name"].strip().replace(" ", "_")
    sur = a["client_surname"].strip().replace(" ", "_")
    return w.safe_filename("%s_%s_OM_TaxFree_Proposal_Email - %s" % (first, sur, d.strftime("%d.%m.%y"))) + ".html"


def greeting_for(clock, used_today):
    if used_today:
        return "Hi"
    return "Good morning" if clock.hour < 12 else ("Good afternoon" if clock.hour < 18 else "Good evening")


def quote_name(docs):
    n = docs["docs"]["quote"]["name"]
    return n[:-4] if n.lower().endswith(".pdf") else n


def teams_text(a, docs, greeting):
    funds = ", ".join(f["name"] for f in a["funds"])
    return "\n".join([
        "%s Sitamah," % greeting, "",
        "**Action needed:** I have compiled the draft Old Mutual Tax-Free proposal email to %s and saved it in **Drafts** (To: %s, Cc: you)." % (a["client_full_name"].strip(), a["client_email"].strip()), "",
        "Please kindly review that draft and attach the following to it:",
        "1. The OM Tax-Free Quote (%s)" % quote_name(docs),
        "2. The relevant fund fact sheets as per the quote (%s)" % funds,
        "3. The \"OM Wealth Investment Strategy Summary\" document", "",
        "All three are in %s's folder: %s > Comparative Quotes." % (a["client_first_name"].strip(), a["plan_folder"].strip()), "",
        "Once attached, please email the client - Thank you!"])


# ------------------------------------------------------------------ validation
def _has(e):
    return e is not None and e.has_text


def answers_problems(a, ev, docs, today, run_client=None):
    """Problems with the entered answers (empty = fine). `ev` maps a document role to a docread.Evidence (or None); `docs` is docs.json."""
    out = []
    for k in set(a) - ANSWER_KEYS:
        out.append("unknown field %r" % k)
    for k in ("client_full_name", "client_first_name", "client_surname", "owner_full_name", "employer", "position", "plan_folder", "risk_profile", "client_email"):
        if not str(a.get(k) or "").strip():
            out.append("%s is missing" % k)
    if run_client and w.norm("%s %s" % (a.get("client_first_name", ""), a.get("client_surname", ""))) != w.norm(run_client):
        out.append("the everyday name is not the client Paul named (%s)" % run_client)
    if a.get("plan_type") != "monthly":
        out.append("STOP: this skill has wording only for a MONTHLY contribution plan; for a lump sum there is no wording yet: ask Paul (never invent it)")
    if not isinstance(a.get("owner_is_child"), bool):
        out.append("owner_is_child must be true or false")
    elif a["owner_is_child"]:
        out.append("STOP: the plan is in a child's name; the template's wording ('You work at...') does not fit and there is no child wording yet: ask Paul")
    age = a.get("owner_age")
    if not isinstance(age, int) or isinstance(age, bool) or age < 18 or age > 100:
        out.append("owner_age must be a whole number from 18 to 100 (a plan owner under 18 is a child's plan: STOP and ask Paul)")
    if w.norm(a.get("client_surname", "")) not in w.norm(a.get("client_full_name", "")):
        out.append("the surname must be part of the client's full name")
    if w.norm(a.get("client_full_name", "")) != w.norm(a.get("owner_full_name", "")):
        out.append("STOP: the plan owner on the quote is not the client (a child's or joint plan?): ask Paul")
    if a.get("conflicts"):
        out.append("%d unresolved conflict(s) between sources: STOP and ask Paul, quoting both values and their sources" % len(a["conflicts"]))
    srcs = a.get("sources") or {}
    for k in SOURCE_KEYS:
        if len(str(srcs.get(k) or "").strip()) < 3:
            out.append("sources.%s: every answer needs its source (a document or Paul's words)" % k)
    if not isinstance(a.get("flags"), list) or not all(isinstance(x, str) for x in a.get("flags", [])):
        out.append("flags must be a list of short sentences (empty list if there is nothing to flag)")
    q, f, rq = ev.get("quote"), ev.get("fact_find_summary"), ev.get("risk_questionnaire")
    if q is None or f is None:
        return out + ["the quote and the Fact Find Summary must be registered first"]
    # ---- the quote
    if _has(q):
        for m in (q.name("owner name in the quote", a.get("owner_full_name")), q.number("contribution in the quote", a.get("contribution")),
                  q.number("owner age in the quote", Decimal(age)) if isinstance(age, int) and not isinstance(age, bool) else None):
            m and out.append(m)
    if w.parse_money(a.get("contribution")) is None:
        out.append("contribution %r is not an amount" % a.get("contribution"))
    # ---- the start date: always double-checked with Paul (his own rule)
    d = w.parse_date(a.get("start_date"))
    ch = a.get("start_date_choice") or {}
    if d is None:
        out.append("start_date %r is not a date (DD/MM/YYYY)" % a.get("start_date"))
    if ch.get("choice") not in ("quote", "changed") or len(str(ch.get("paul_said") or "").strip()) < 3:
        out.append("start_date_choice: Paul must say whether the Quote's start date stands or has changed ({\"choice\": \"quote\"|\"changed\", \"paul_said\": \"his words\"}); it is always asked")
    elif d is not None:
        if ch["choice"] == "quote" and _has(q):
            m = q.date("start date in the quote", a["start_date"])
            m and out.append(m + " (Paul said the Quote's date stands)")
        if ch["choice"] == "changed" and d < today:
            out.append("the changed start date %s is in the past" % a["start_date"])
    # ---- funds and fees
    funds = a.get("funds")
    if not isinstance(funds, list) or not 1 <= len(funds) <= 8:
        out.append("funds must list every fund in the quote's allocation table (1 to 8)")
        funds = []
    names = [w.norm(x.get("name", "")) for x in funds]
    if len(set(names)) != len(names) or "" in names:
        out.append("every fund needs its own name")
    for x in funds:
        if not isinstance(x, dict) or not x.get("name"):
            continue
        if _has(q):
            m = q.name("fund '%s'" % x["name"], x["name"])
            m and out.append(m)
            m = q.exact_percent("allocation of '%s'" % x["name"], x.get("allocation"))
            m and out.append(m)
        elif pct_decimal(x.get("allocation")) is None:
            out.append("allocation of '%s' is not a percentage" % x["name"])
    if funds and all(pct_decimal(x.get("allocation")) is not None for x in funds if isinstance(x, dict)):
        if sum(pct_decimal(x["allocation"]) for x in funds) != Decimal(100):
            out.append("the fund allocations add up to %s%%, not 100%%" % format(sum(pct_decimal(x["allocation"]) for x in funds), "f"))
    fees = a.get("fees") or {}
    if set(fees) != set(FEE_KEYS):
        out.append("fees needs exactly: %s" % ", ".join(FEE_KEYS))
    else:
        for k in FEE_KEYS:
            if pct_decimal(fees[k]) is None:
                out.append("fee %s %r is not a percentage" % (k, fees[k]))
            elif _has(q):
                m = q.exact_percent("%s in the quote" % FEE_LABEL[k], fees[k])
                m and out.append(m)
    # ---- fund fact sheets: one for every fund
    fs = a.get("fund_sheets") or {}
    for x in funds:
        nm = x.get("name") if isinstance(x, dict) else None
        role = fs.get(nm)
        if not role:
            out.append("fund_sheets: no fact sheet named for '%s' (a registered fund_fact_sheet role, or MISSING if Paul said it does not exist)" % nm)
        elif role == "MISSING":
            if not (docs.get("missing", {}).get("fund_fact_sheet") or "").strip():
                out.append("fund_sheets: '%s' is MISSING but Paul's words were not recorded (run.py doc --missing fund_fact_sheet --said ...)" % nm)
        elif not is_sheet(role) or role not in docs.get("docs", {}):
            out.append("fund_sheets: %r for '%s' is not a registered fund fact sheet" % (role, nm))
        else:
            sheet = ev.get(role)
            if _has(sheet):
                m = sheet.name("fund fact sheet %s" % role, nm)
                m and out.append(m + " (is this the right fact sheet?)")
    # ---- the client's own facts (Fact Find Summary)
    if _has(f):
        for m in (f.name("client name in the Fact Find Summary", a.get("client_full_name")), f.name("employer in the Fact Find Summary", a.get("employer")),
                  f.name("position in the Fact Find Summary", a.get("position")), f.number("gross monthly income in the Fact Find Summary", a.get("gross_monthly_income"))):
            m and out.append(m)
    if w.parse_money(a.get("gross_monthly_income")) is None:
        out.append("gross_monthly_income %r is not an amount" % a.get("gross_monthly_income"))
    # ---- the email address: never invented
    em = str(a.get("client_email") or "").strip()
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", em):
        out.append("client_email %r is not an email address" % em)
    elif a.get("email_source") == "fact_find_summary":
        if _has(f) and em.lower() not in f.text.lower():
            out.append("client_email is not in the Fact Find Summary's text (email_source says it is)")
    elif a.get("email_source") == "other":
        if len(str(a.get("email_note") or "").strip()) < 10:
            out.append("client_email from another source: say which (manual Fact Find, Overview, Zapier contact lookup, Outlook search) in email_note")
    else:
        out.append("email_source must be 'fact_find_summary' or 'other' (with email_note)")
    # ---- risk profile
    rp = str(a.get("risk_profile") or "").strip()
    src = a.get("risk_profile_source")
    if src == "questionnaire":
        if rq is None:
            out.append("risk_profile_source is the questionnaire but none is registered")
        elif _has(rq):
            m = rq.name("Risk Profile in the questionnaire", rp)
            m and out.append(m)
    elif src == "paul":
        if len(str(a.get("risk_paul_said") or "").strip()) < 5:
            out.append("risk_profile_source is Paul's answer: record his words in risk_paul_said")
    else:
        out.append("risk_profile_source must be 'questionnaire' or 'paul'")
    ffs_rp = str(a.get("ffs_risk_profile") or "").strip()
    if ffs_rp and w.norm(ffs_rp) != w.norm(rp):
        out.append("the Fact Find Summary says the Risk Profile is %r but the answers say %r: a conflict: STOP and ask Paul" % (ffs_rp, rp))
    # ---- the dates (weekdays are computed, never typed)
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
        out.append("next_meeting needs a date (DD/MM/YYYY) and a time like 5pm or 5:30pm")
    elif nd < today:
        out.append("the next meeting date %s is in the past" % nm["date"])
    return out


# ------------------------------------------------------------------ the email
def _fill(t, ph, value, count=None):
    n = t.count(ph)
    want = EXPECTED_COUNT.get(ph, 1) if count is None else count
    if n != want:
        raise ValueError("the template has %d x %s, expected %d: the template was changed" % (n, ph, want))
    return t.replace(ph, value)


def _esc(s):
    return html.escape(str(s), quote=False)


def build_all(a, sent):
    """(full, nologo, body): the email with the logo, the saved copy without it, and the text pasted into the Outlook draft."""
    with open(TEMPLATE, encoding="utf-8") as fh:
        t = fh.read()
    tf = facts()
    rows = "".join('  <tr>\n    <td style="font-weight:bold;padding:6px 10px;background:#f5f5f5;">%s</td>\n    <td style="padding:6px 10px;">%s</td>\n  </tr>\n' % (_esc(x["name"].strip()), pct_shown(x["allocation"]))
                   for x in a["funds"])
    pat = re.compile(r"[ \t]*<tr>\s*<td[^>]*>\[FUND NAME 1\]</td>\s*<td[^>]*>\[ALLOCATION %\]</td>\s*</tr>\s*<!--.*?-->\s*", re.S)
    if len(pat.findall(t)) != 1:
        raise ValueError("the template's fund row was not found: the template was changed")
    t = pat.sub(lambda m: rows, t, count=1)
    nd = w.parse_date(a["next_meeting"]["date"])
    values = {"[DATE AND TIME SENT]": sent, "[CLIENT EMAIL]": a["client_email"].strip(), "[CC EMAIL]": CC_NAME, "[SUBJECT]": subject(a), "[CLIENT FIRST NAME]": a["client_first_name"].strip(),
              "[MEETING DATE(S) WITH DAY]": meetings_line(a), "[AGE]": str(a["owner_age"]), "[EMPLOYER NAME]": a["employer"].strip(), "[POSITION]": a["position"].strip(),
              "[GROSS MONTHLY INCOME]": money_shown(a["gross_monthly_income"]), "[CONTRIBUTION AMOUNT]": money_shown(a["contribution"]),
              "[START DATE DD/MM/YYYY]": a["start_date"], "[RISK PROFILE]": a["risk_profile"].strip(),
              "[ASSET MGMT FEE]": pct_digits(a["fees"]["asset_management"]), "[ADMIN FEE]": pct_digits(a["fees"]["administration"]),
              "[ONGOING ADVICE FEE]": pct_digits(a["fees"]["advice"]), "[ADVISER REMUNERATION]": pct_digits(a["fees"]["adviser_remuneration"]), "[TOTAL FEES]": total_fees(a),
              "[ANNUAL LIMIT]": tf["annual_limit"], "[LIFETIME LIMIT]": tf["lifetime_limit"], "[EXCESS TAX RATE]": tf["excess_tax_rate"],
              "[NEXT MEETING DATE WITH DAY]": td.format_date_with_day(nd), "[TIME]": a["next_meeting"]["time"].strip()}
    for ph, v in values.items():
        t = _fill(t, ph, _esc(v))
    left = [ph for ph in SINGLE + tuple(EXPECTED_COUNT) if ph in t]
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
    """The part pasted into the Outlook draft: <b> not <strong>, a blank line where the template has a spacer, borders on the table cells, no header, no signature."""
    frag = re.sub(r"<table[^>]*>\s*<tr><td height=\"(\d+)\"[^>]*>&nbsp;</td></tr></table>", lambda m: '<p style="margin:0;">&nbsp;</p>' if int(m.group(1)) >= 8 else "", frag)
    frag = frag.replace("<strong>", "<b>").replace("</strong>", "</b>")

    def bold_tag(m):
        style = re.sub(r"font-weight:\s*bold;?", "", m.group(2))
        return "<%s%s>%s<b>%s</b></%s>" % (m.group(1), style, "", m.group(3), m.group(1))
    # Outlook drops font-weight on paste: a heading or cell that is bold by style becomes a real <b>
    frag = re.sub(r'<(p|td)(?=[^>]*font-weight:\s*bold)([^>]*)>(.*?)</\1>', bold_tag, frag, flags=re.S)

    def borders(m):
        return m.group(0).replace('<td style="', '<td style="border:1px solid #dddddd;')
    frag = re.sub(r'<table width="624".*?</table>', borders, frag, flags=re.S)
    return frag.strip() + "\n"


def text_of(h):
    """Readable text of some HTML: block tags become a space, inline tags (b, strong, span...) vanish, so '<b>x</b>,' reads 'x,'."""
    h = re.sub(r"</?(?:p|td|tr|th|table|div|li|ol|ul|br|h\d|body|html|head|title)\b[^>]*>", " ", h)
    return " ".join(html.unescape(re.sub(r"<[^>]+>", "", h)).split())


def html_problems(full, nologo, body, a, sent):
    """The checks on the built email, as [(ok, short, detail)]."""
    R = []

    def add(ok, short, detail=""):
        R.append((bool(ok), short, detail))
    tf = facts()
    for nm, h in (("full copy", full), ("saved copy", nologo), ("pasted body", body)):
        add(not PLACEHOLDER.search(h) and "@@" not in h, "No [PLACEHOLDER] text is left in the %s" % nm)
        add(h.count("<table") == h.count("</table>"), "Tables open = close in the %s (%d)" % (nm, h.count("<table")))
    for nm, h in (("full copy", full), ("saved copy", nologo)):
        hd = re.findall(r'<td[^>]*font-weight:bold[^>]*>(From|Sent|To|Cc|Subject|Importance):</td><td[^>]*>(.*?)</td>', h, re.S)
        hd = {k: html.unescape(v).strip() for k, v in hd}
        ok = hd.get("To") == a["client_email"].strip() and hd.get("Cc") == CC_NAME and hd.get("Subject") == subject(a) and hd.get("Importance") == "High" and hd.get("Sent") == sent
        add(ok, "The header of the %s: To = the client, Cc = %s, Subject exactly the draft's, Importance High, Sent filled" % (nm, CC_NAME) if ok else
            "Header problem in the %s: %s" % (nm, hd))
    bt = text_of(body)
    add(bt.startswith("Dear %s," % a["client_first_name"].strip()) and "Kind regards" not in bt and "<img" not in body and "FSP45946" not in body and "Importance:" not in bt,
        "The pasted body runs from 'Dear %s,' to the next-meeting line: no header, no signature block, no second 'Kind regards,', no logo" % a["client_first_name"].strip())
    add(("on %s @ %s" % (td.format_date_with_day(w.parse_date(a["next_meeting"]["date"])), a["next_meeting"]["time"].strip())) in bt and bt.rstrip().endswith("%s." % a["next_meeting"]["time"].strip()),
        "The next meeting reads '%s' with its weekday computed" % next_line(a))
    add(("Teams Meeting on %s," % meetings_line(a)) in bt, "The meetings already held read '%s' with their weekdays computed" % meetings_line(a))
    rows_ok = all(("%s %s" % (x["name"].strip(), pct_shown(x["allocation"]))) in bt for x in a["funds"]) and "Total allocation 100%" in bt
    add(rows_ok, "One row per fund (%d) with its allocation, and the total is 100%%" % len(a["funds"]))
    fee_ok = all(("%s %s%%" % (FEE_LABEL[k], pct_digits(a["fees"][k]))) in bt for k in FEE_KEYS) and ("Total ongoing fees %s%% p.a." % total_fees(a)) in bt
    add(fee_ok, "The four fees are as in the quote and the total (%s%% p.a.) is added up by the program" % total_fees(a))
    c = money_shown(a["contribution"])
    add(bt.count("R %s p.m." % c) >= 2 and ("starting on: %s." % a["start_date"]) in bt and ("You are %d years old." % a["owner_age"]) in bt and ("“%s”" % a["risk_profile"].strip()) in bt,
        "Contribution R %s p.m., start date %s, age %d and Risk Profile “%s” are in the email" % (c, a["start_date"], a["owner_age"], a["risk_profile"].strip()))
    fixed = ("inflation plus 4-5% after asset management fees", "The recommended minimum investment period is 5-7 years.", "Hoping that the above is in order.", "Old Mutual Wealth Investment Strategy Summary.")
    add(all(x in bt for x in fixed) and all(tf[k] in bt for k in ("annual_limit", "lifetime_limit", "excess_tax_rate")),
        "The fixed text is there: target (inflation plus 4-5%%, 5-7 years), the three attachments, the closing line and the tax facts (%s, %s, %s)" % (tf["annual_limit"], tf["lifetime_limit"], tf["excess_tax_rate"]))
    add("data:image/png;base64," in full and "data:image" not in nologo and "FSP45946" in full and "FSP45946" in nologo and "Kind regards," in full and "Kind regards," in nologo,
        "The full copy carries the logo; the saved copy is the no-logo copy; both keep Paul's signature block")
    return R


# ------------------------------------------------------------------ what comes back from Outlook and Teams
def flatten(text):
    """(all the strings of a saved read-back joined, the parsed object or None, the list of strings)."""
    try:
        obj = json.loads(text)
    except ValueError:
        return text, None, [text]
    out = []

    def walk(o):
        if isinstance(o, dict):
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
        elif isinstance(o, str):
            out.append(o)
    walk(obj)
    return "\n".join(out), obj, out


def find_key(obj, names):
    names = {n.lower() for n in names}
    found = []

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k.lower() in names:
                    found.append(v)
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(obj)
    return found


def _emails(x):
    return {e.lower() for e in re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", json.dumps(x))}


def draft_problems(text, a, sig_mode):
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
        add(client in to_set and CC_EMAIL in cc_set and CC_EMAIL not in to_set, "To = the client (%s) and Cc = %s, read back from the saved draft" % (a["client_email"].strip(), CC_NAME))
    else:
        add(client in flat.lower() and CC_EMAIL in flat.lower(), "The client (%s) and %s are on the draft (the read-back has no separate To and Cc fields)" % (a["client_email"].strip(), CC_NAME))
    subs = [x for x in (find_key(obj, ("subject",)) if obj is not None else []) if isinstance(x, str)]
    add((subject(a) in subs) if subs else (subject(a) in flat), "The subject is exactly the one in the HTML, en dash included")
    imp = [x for x in (find_key(obj, ("importance",)) if obj is not None else []) if isinstance(x, str)]
    add((imp and imp[0].lower() == "high") if imp else bool(re.search(r"importance\W{1,6}high", flat, re.I)), "Importance is High")
    cands = [x for x in leaves if "Dear " in x and "<" in x]
    body = max(cands, key=len) if cands else flat
    add(body.count("<table") == body.count("</table>") and body.count("<table") >= 2, "Tables open = close in the saved draft (%d)" % body.count("<table"))
    kr = body.count("Kind regards,")
    add(kr == (1 if sig_mode == "insert" else 0), "'Kind regards,' appears %d time(s) (%s)" % (kr, "exactly once, from the inserted signature" if sig_mode == "insert" else "none: the server adds the signature"))
    add(not PLACEHOLDER.search(body) and "@@" not in body, "No placeholder text is left in the draft")
    add(not re.search(r"\bLoop\b", flat), "No Loop component is in the draft")
    bt = text_of(body)
    heads = ("Your personal circumstances:", "The product that you can elect to take out", "The Risk profile that was determined for you:", "Description of the product chosen",
             "Costs and fees associated with this product:", "Please see attached:")
    bold = len(re.findall(r"<(?:b|strong)[ >]", body))
    add(all(h in bt for h in heads) and bold >= 8, "All sections are in the draft with bold headings (%d bold tags)" % bold)
    need = ["Dear %s," % a["client_first_name"].strip(), meetings_line(a), next_line(a), "R %s p.m." % money_shown(a["contribution"]), total_fees(a) + "%"]
    need += [x["name"].strip() for x in a["funds"]] + [pct_shown(x["allocation"]) for x in a["funds"]] + [pct_digits(a["fees"][k]) + "%" for k in FEE_KEYS]
    miss = [x for x in need if x not in bt]
    add(not miss, "The draft carries the client's name, the dates, every fund, allocation, fee and the contribution" if not miss else "Missing from the draft: %s" % miss[0])
    return R


def message_problems(text, a, docs, greeting):
    """Checks on the saved read-back of the posted Teams message: [(ok, short)]."""
    flat, _obj, leaves = flatten(text)
    R = []

    def add(ok, short):
        R.append((bool(ok), short))
    cands = [x for x in leaves if "Sitamah" in x]
    flat = max(cands, key=len) if cands else flat          # the message body itself, not the ids and labels around it
    plain = text_of(flat)
    add(plain.startswith("%s Sitamah," % greeting), "The message opens with the greeting '%s Sitamah,'" % greeting)
    add("<strong>Action needed:</strong>" in flat and "<strong>Drafts</strong>" in flat, "'Action needed:' and 'Drafts' are bold (real <strong> tags)")
    add("<ol>" in flat and flat.count("<li>") == 3, "The three attachments are a real numbered list")
    add("**" not in flat and "&lt;" not in flat and "\\u003c" not in flat, "No literal ** and no escaped tags show")
    add(quote_name(docs) in plain and all(x["name"].strip() in plain for x in a["funds"]) and ("%s > Comparative Quotes" % a["plan_folder"].strip()) in plain,
        "The message names the quote, every fund and the folder (%s > Comparative Quotes)" % a["plan_folder"].strip())
    add(plain.rstrip().endswith("Once attached, please email the client - Thank you!") and "do not send" not in plain.lower() and "leave it in drafts" not in plain.lower(),
        "It ends 'Once attached, please email the client - Thank you!' with no 'do not send' line")
    return R


# ------------------------------------------------------------------ the confirmation table
GREETING_MARK = "<greeting by the clock>"


def table_rows(a, docs):
    s = a.get("sources") or {}
    ch = a["start_date_choice"]
    rows = [("Client (greeting, full name)", "%s (%s)" % (a["client_full_name"], a["client_first_name"]), s.get("personal")),
            ("Plan: monthly Tax-Free for the client", "owner age %d" % a["owner_age"], s.get("quote")),
            ("Works at (employer, position)", "%s, %s" % (a["employer"], a["position"]), s.get("personal")),
            ("Gross monthly income", "R %s" % money_shown(a["gross_monthly_income"]), s.get("personal")),
            ("Contribution", "R %s p.m." % money_shown(a["contribution"]), s.get("quote")),
            ("Start date (Paul always confirms it)", "%s: %s" % (a["start_date"], "the Quote's date stands" if ch["choice"] == "quote" else "CHANGED"), "Paul: %s" % ch["paul_said"]),
            ("Risk Profile", a["risk_profile"], "Paul: %s" % a["risk_paul_said"] if a["risk_profile_source"] == "paul" else s.get("risk"))]
    for x in a["funds"]:
        rows.append(("Fund", "%s %s" % (x["name"], pct_shown(x["allocation"])), "its fact sheet: %s" % a["fund_sheets"].get(x["name"])))
    for k in FEE_KEYS:
        rows.append((FEE_LABEL[k], pct_shown(a["fees"][k]), s.get("quote")))
    rows += [("Total ongoing fees (added up by the program)", "%s%% p.a." % total_fees(a), "worked out"),
             ("Client email (To)", a["client_email"], s.get("email")),
             ("Meetings already held", meetings_line(a), s.get("meetings")),
             ("Next Teams meeting", next_line(a), s.get("next_meeting")),
             ("Subject", subject(a), "built by the program"),
             ("Cc", "%s (%s)" % (CC_NAME, CC_EMAIL), "fixed"),
             ("Plan folder (saved copy and the three attachments)", "%s > Comparative Quotes" % a["plan_folder"], "the client's file"),
             ("Signature in the Outlook draft", "inserted by Claude (Paul K New)" if settings()["signature_mode"] == "insert" else "added by the Exchange rule", "settings.json; the question is still open with Paul")]
    rows += [("Flag", x, "the chat") for x in a.get("flags") or []]
    rows.append(("Teams message to Sitamah (sent only after the draft is checked; the greeting is set by the clock when it is sent)", teams_text(a, docs, GREETING_MARK), "fixed wording"))
    return rows
