#!/usr/bin/env python3
"""The domain model of the RGAR proposal email: the answers (every figure checked against the documents' text), the shortfall dates, the email built from the fixed
template, the Teams message to Sitamah, the file names, the confirmation table, and the checks of what comes back (the Outlook draft and the posted message).

Everything here is a pure function of the answers (answers.json) and the stored build time, so the checker can recompute it and refuse a file edited by hand.
Rules are Paul's (the old skill, kept) and his answers of 03/11/2026. Nothing here sends anything.
"""
import html
import json
import os
import re
from decimal import Decimal

import rgar_dates as rd
import wrlib as w

ASSETS = os.path.join(w.SKILL_DIR, "assets")
TEMPLATE = os.path.join(ASSETS, "RGAR_Proposal_Email_TEMPLATE.html")
SETTINGS = os.path.join(ASSETS, "settings.json")
LABELS = os.path.join(ASSETS, "net_target_labels.json")

CC_NAME = "Sitamah Nathoo"
CC_EMAIL = "admin@liferisk.co.za"
SITAMAH_CHAT = "19:bd2a130a-35d9-459e-9025-55f356810236_e6901cee-de73-46d9-88a5-5e4a1c296418@unq.gbl.spaces"
CHAT_LABEL = "(1:1 Chat) Paul Kafentzis, Sitamah Nathoo"

FIXED_ROLES = ("rgar_report", "fact_find_summary", "fact_find_summary_older")
SERVED_ROLES = FIXED_ROLES
ALWAYS_NEEDED = ("rgar_report", "fact_find_summary")
SOURCE_KEYS = ("rgar", "personal", "net_target", "email", "meetings", "next_meeting")
ANSWER_KEYS = {"client_full_name", "client_first_name", "client_surname", "age", "rgar_dob", "retirement_age", "years_until_retirement", "current_value", "future_value",
               "net_monthly_target", "lump_sum", "monthly", "escalation", "sustainability_age", "recurring_investment", "employer", "job_title", "gross_monthly_income",
               "client_email", "email_source", "email_note", "meetings_held", "next_meeting", "plan_folder", "flags", "sources", "conflicts"}
PLACEHOLDER = re.compile(r"\[[A-Z][A-Z0-9 %().,/&#-]*\]")
EXPECTED_COUNT = {"[RETIREMENT AGE]": 2}
SINGLE = ("[DATE AND TIME SENT]", "[CLIENT EMAIL]", "[CC NAME(S)]", "[SUBJECT]", "[RGAR FILE NAME]", "[CLIENT FIRST NAME]", "[MEETING DATES LIST]", "[AGE]", "[EMPLOYER NAME]", "[JOB TITLE]",
          "[A OR AN]", "[GROSS MONTHLY INCOME]", "[NET MONTHLY TARGET]", "[CURRENT VALUE / GROSS EXPENSE]", "[FUTURE VALUE]", "[LUMP SUM SHORTFALL]", "[MONTHLY SHORTFALL]", "[ESCALATION]",
          "[SUSTAINABILITY AGE]", "[SHORTFALL START DATE]", "[SHORTFALL END DATE]", "[NEXT MEETING DAY]", "[NEXT MEETING DD/MM/YYYY]", "[TIME]")
R0_FLAG = "The RGAR shows a recurring investment of R 0: its sustainability age and shortfall may not reflect the proposed product."


def valid_role(role):
    return role in FIXED_ROLES


def can_be_missing(role):
    return role == "fact_find_summary_older"


def settings():
    with open(SETTINGS, encoding="utf-8") as f:
        return json.load(f)


def net_labels():
    with open(LABELS, encoding="utf-8") as f:
        return json.load(f)["labels"]


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


def dates_of(lst):
    return sorted(w.parse_date(x) for x in lst)


def meetings_line(a):
    return rd.format_meeting_dates_list(dates_of(a["meetings_held"]))


def next_date(a):
    return w.parse_date(a["next_meeting"]["date"])


def next_line(a):
    return "%s @ %s" % (rd.format_date_with_day(next_date(a)), a["next_meeting"]["time"].strip())


def shortfall(a):
    """(start, end) as '1st August 2026': the 1st of the month after the next meeting, and the same day `years until retirement` later."""
    return rd.shortfall_period(next_date(a), int(a["years_until_retirement"]))


def age_from_dob(dob, on):
    return on.year - dob.year - ((on.month, on.day) < (dob.month, dob.day))


def subject(a):
    return "%s / Retirement Goal Analysis Report" % a["client_full_name"].strip()


def sent_text(clock):
    return "%s, %s %s" % (rd.calendar.day_name[clock.weekday()], clock.strftime("%d/%m/%Y"), clock.strftime("%H:%M"))


def file_name(a, d):
    first = a["client_first_name"].strip().replace(" ", "_")
    sur = a["client_surname"].strip().replace(" ", "_")
    return w.safe_filename("%s_%s_RGAR_Proposal_Email - %s" % (first, sur, d.strftime("%d.%m.%y"))) + ".html"


def greeting_for(clock, used_today):
    if used_today:
        return "Hi"
    return "Good morning" if clock.hour < 12 else ("Good afternoon" if clock.hour < 18 else "Good evening")


def article(job_title):
    """'a' or 'an' before the job title ("as an Analyst", "as a Director"): by the first letter, with the usual exceptions for words that start with a 'you' or 'wun' sound."""
    t = job_title.strip().lower()
    return "an" if t[:1] in "aeiou" and not t.startswith(("uni", "use", "usu", "eur", "one", "ubi")) else "a"


def rgar_name(docs):
    return docs["docs"]["rgar_report"]["name"]


def rgar_name_no_ext(docs):
    n = rgar_name(docs)
    return n[:-4] if n.lower().endswith(".pdf") else n


def auto_flags(a):
    return [R0_FLAG] if w.parse_money(a.get("recurring_investment")) == 0 else []


def all_flags(a):
    return auto_flags(a) + list(a.get("flags") or [])


def teams_text(a, docs, greeting):
    return "\n".join([
        "%s Sitamah," % greeting, "",
        "**Action needed:** I have compiled the draft Retirement Goal Analysis (RGAR) proposal email to %s and saved it in **Drafts** (To: %s, Cc: you)." % (a["client_full_name"].strip(), a["client_email"].strip()), "",
        "Please kindly attach the following to that draft:",
        "1. The RGAR report (%s)" % rgar_name_no_ext(docs), "",
        "It is in %s's folder: %s > Comparative Quotes." % (a["client_first_name"].strip(), a["plan_folder"].strip()), "",
        "Once attached, please email the client - Thank you!"])


# ------------------------------------------------------------------ validation
def _has(e):
    return e is not None and e.has_text


# (answer key, display label, regexes of the label in the RGAR, unit)
RGAR_FIGURES = (("retirement_age", "retirement age", [r"retirement age"], "number"), ("years_until_retirement", "years until retirement", [r"years until retirement"], "number"),
                ("current_value", "current value of the expenses", [r"current value"], "amount"), ("future_value", "future value of the expenses", [r"future value"], "amount"),
                ("lump_sum", "once-off lump sum", [r"lump sum"], "amount"), ("monthly", "monthly recurring contribution", [r"monthly recurring", r"recurring contribution", r"monthly contribution"], "amount"),
                ("sustainability_age", "sustainability age", [r"sustainable until", r"sustainab"], "number"))


def answers_problems(a, ev, docs, today, run_client=None):
    """Problems with the entered answers (empty = fine). `ev` maps a document role to a docread.Evidence (or None); `docs` is docs.json."""
    out = []
    for k in set(a) - ANSWER_KEYS:
        out.append("unknown field %r" % k)
    for k in ("client_full_name", "client_first_name", "client_surname", "employer", "job_title", "plan_folder", "client_email"):
        if not str(a.get(k) or "").strip():
            out.append("%s is missing" % k)
    if run_client and w.norm("%s %s" % (a.get("client_first_name", ""), a.get("client_surname", ""))) != w.norm(run_client):
        out.append("the everyday name is not the client Paul named (%s)" % run_client)
    if w.norm(a.get("client_surname", "")) not in w.norm(a.get("client_full_name", "")):
        out.append("the surname must be part of the client's full name")
    if a.get("conflicts"):
        out.append("%d unresolved conflict(s) between sources: STOP and ask Paul, quoting both values and their sources" % len(a["conflicts"]))
    srcs = a.get("sources") or {}
    for k in SOURCE_KEYS:
        if len(str(srcs.get(k) or "").strip()) < 3:
            out.append("sources.%s: every answer needs its source (a document or Paul's words)" % k)
    if not isinstance(a.get("flags"), list) or not all(isinstance(x, str) for x in a.get("flags", [])):
        out.append("flags must be a list of short sentences (empty list if there is nothing to flag; the R 0 flag is added by the program)")
    r, f = ev.get("rgar_report"), ev.get("fact_find_summary")
    if r is None or f is None:
        return out + ["the RGAR report and the Fact Find Summary must be registered first"]
    # ---- the RGAR figures: in the report's text, and next to their label when the label is found
    for key, label, pats, unit in RGAR_FIGURES:
        v = a.get(key)
        d = w.parse_money(v) if v not in (None, "") else None
        if d is None:
            out.append("%s %r is not a number" % (label, v))
            continue
        if _has(r):
            m = r.number("%s in the RGAR" % label, d)
            if m:
                out.append(m)
            else:
                n = r.near("%s in the RGAR" % label, pats, d)
                if n and n != "NOLABEL":
                    out.append(n)
    if w.parse_money(a.get("lump_sum")) == 0 or w.parse_money(a.get("monthly")) == 0:
        out.append("STOP: the RGAR shows a lump sum or a monthly contribution of R 0: the template prints both lines and there is no wording for R 0: ask Paul what to write (never invented)")
    if w.parse_money(a.get("recurring_investment")) is None:
        out.append("recurring_investment %r is not an amount (the RGAR's recurring investment: R 0 raises a flag)" % a.get("recurring_investment"))
    elif _has(r):
        m = r.number("recurring investment in the RGAR", a["recurring_investment"])
        m and out.append(m)
    if _has(r):
        m = r.exact_percent("debit order escalation in the RGAR", a.get("escalation"))
        m and out.append(m)
    elif w.parse_money(str(a.get("escalation") or "").replace("%", "")) is None:
        out.append("escalation %r is not a percentage" % a.get("escalation"))
    # ---- age: from the date of birth in the RGAR, compared with the Fact Find Summary
    dob = w.parse_date(a.get("rgar_dob"))
    age = a.get("age")
    if dob is None:
        out.append("rgar_dob %r is not a date (DD/MM/YYYY, as the RGAR's date of birth)" % a.get("rgar_dob"))
    else:
        if _has(r):
            m = r.date("date of birth in the RGAR", a["rgar_dob"])
            m and out.append(m)
        if not isinstance(age, int) or isinstance(age, bool):
            out.append("age must be a whole number (the client's age in the Fact Find Summary)")
        elif age_from_dob(dob, today) != age:
            out.append("STOP: the age %d (Fact Find Summary) does not match the date of birth in the RGAR, which makes the client %d today: ask Paul which is right" % (age, age_from_dob(dob, today)))
    if isinstance(age, int) and not isinstance(age, bool) and _has(f):
        m = f.number("age in the Fact Find Summary", Decimal(age))
        m and out.append(m)
    # ---- the client's own facts (Fact Find Summary)
    if _has(f):
        for m in (f.name("client name in the Fact Find Summary", a.get("client_full_name")), f.name("employer in the Fact Find Summary", a.get("employer")),
                  f.name("job title in the Fact Find Summary", a.get("job_title")), f.number("gross monthly income in the Fact Find Summary", a.get("gross_monthly_income"))):
            m and out.append(m)
        net = a.get("net_monthly_target")
        res = [f.near("net monthly target", [re.escape(l).replace(r"\ ", r"\s+") for l in [lab]], net, window=70, first=True) for lab in net_labels()]
        if all(x == "NOLABEL" for x in res):
            out.append("STOP: the Fact Find Summary has no line labelled %s: ask Paul where the net monthly target is (never derived from the gross figure by assuming a tax rate)" % " or ".join(repr(l) for l in net_labels()))
        elif not any(x is None for x in res):
            out.append("net monthly target: %s is not the figure that follows its label (%s) in the Fact Find Summary: the Reduced Quote's contribution target is a different figure" % (net, " / ".join(net_labels())))
    for k in ("gross_monthly_income", "net_monthly_target"):
        if w.parse_money(a.get(k)) is None:
            out.append("%s %r is not an amount" % (k, a.get(k)))
    # ---- the email address: never invented
    em = str(a.get("client_email") or "").strip()
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
        out.append("next_meeting needs a date (DD/MM/YYYY) and a time like 12pm or 5:30pm")
    elif nd < today:
        out.append("the next meeting date %s is in the past" % nm["date"])
    yu = a.get("years_until_retirement")
    if w.parse_money(yu) is not None and w.parse_money(yu) != w.parse_money(yu).to_integral_value():
        out.append("years_until_retirement must be a whole number (it drives the shortfall end date)")
    return out


# ------------------------------------------------------------------ the email
def _fill(t, ph, value):
    n = t.count(ph)
    want = EXPECTED_COUNT.get(ph, 1)
    if n != want:
        raise ValueError("the template has %d x %s, expected %d: the template was changed" % (n, ph, want))
    return t.replace(ph, value)


def _esc(s):
    return html.escape(str(s), quote=False)


def build_all(a, sent, docs):
    """(full, nologo, body): the email with the logo, the saved copy without it, and the text pasted into the Outlook draft."""
    with open(TEMPLATE, encoding="utf-8") as fh:
        t = fh.read()
    start, end = shortfall(a)
    nd = next_date(a)
    values = {"[DATE AND TIME SENT]": sent, "[CLIENT EMAIL]": a["client_email"].strip(), "[CC NAME(S)]": CC_NAME, "[SUBJECT]": subject(a), "[RGAR FILE NAME]": rgar_name(docs),
              "[CLIENT FIRST NAME]": a["client_first_name"].strip(), "[MEETING DATES LIST]": meetings_line(a), "[AGE]": str(a["age"]), "[EMPLOYER NAME]": a["employer"].strip(),
              "[A OR AN]": article(a["job_title"]), "[JOB TITLE]": a["job_title"].strip(), "[GROSS MONTHLY INCOME]": money_shown(a["gross_monthly_income"]), "[RETIREMENT AGE]": str(int(w.parse_money(a["retirement_age"]))),
              "[NET MONTHLY TARGET]": money_shown(a["net_monthly_target"]), "[CURRENT VALUE / GROSS EXPENSE]": money_shown(a["current_value"]), "[FUTURE VALUE]": money_shown(a["future_value"]),
              "[LUMP SUM SHORTFALL]": money_shown(a["lump_sum"]), "[MONTHLY SHORTFALL]": money_shown(a["monthly"]), "[ESCALATION]": pct_digits(a["escalation"]),
              "[SUSTAINABILITY AGE]": str(int(w.parse_money(a["sustainability_age"]))), "[SHORTFALL START DATE]": start, "[SHORTFALL END DATE]": end,
              "[NEXT MEETING DAY]": rd.calendar.day_name[nd.weekday()], "[NEXT MEETING DD/MM/YYYY]": nd.strftime("%d/%m/%Y"), "[TIME]": a["next_meeting"]["time"].strip()}
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


def _lines(a):
    """The sentences of the email that carry the figures (as they read in the template)."""
    s, e = shortfall(a)
    ra = str(int(w.parse_money(a["retirement_age"])))
    return ["You are %d years old." % a["age"], "You work for %s as %s %s." % (a["employer"].strip(), article(a["job_title"]), a["job_title"].strip()),
            "R %s per month." % money_shown(a["gross_monthly_income"]), "You intend to retire at age %s." % ra,
            "At age %s, you would like to net the equivalent in today’s terms of R %s per month (R %s gross) which equates to a Future Value of: R %s per month." %
            (ra, money_shown(a["net_monthly_target"]), money_shown(a["current_value"]), money_shown(a["future_value"])),
            "Once-off lump sum contribution required to fund remaining shortfall: R %s." % money_shown(a["lump_sum"]),
            "Monthly recurring contribution required to fund remaining shortfall: R %s." % money_shown(a["monthly"]),
            "Debit order increases every year at: %s%%." % pct_digits(a["escalation"]),
            "your income is projected to be sustainable until you are %d years old." % int(w.parse_money(a["sustainability_age"])),
            "the shortfall that would have to be covered as of the %s until %s." % (s, e)]


def html_problems(full, nologo, body, a, sent, docs):
    """The checks on the built email, as [(ok, short, detail)]."""
    R = []

    def add(ok, short, detail=""):
        R.append((bool(ok), short, detail))
    for nm, h in (("full copy", full), ("saved copy", nologo), ("pasted body", body)):
        add(not PLACEHOLDER.search(h) and "@@" not in h, "No [PLACEHOLDER] text is left in the %s" % nm)
        add(h.count("<table") == h.count("</table>"), "Tables open = close in the %s (%d)" % (nm, h.count("<table")))
    for nm, h in (("full copy", full), ("saved copy", nologo)):
        hd = re.findall(r'<td[^>]*font-weight:bold[^>]*>(From|Sent|To|Cc|Subject|Attachments|Importance):</td><td[^>]*>(.*?)</td>', h, re.S)
        hd = {k: html.unescape(v).strip() for k, v in hd}
        ok = (hd.get("To") == a["client_email"].strip() and hd.get("Cc") == CC_NAME and hd.get("Subject") == subject(a) and hd.get("Importance") == "High" and hd.get("Sent") == sent and
              hd.get("Attachments") == rgar_name(docs))
        add(ok, "The header of the %s: To = the client's email, Cc = %s, Subject exactly the draft's, Attachments = the real RGAR file name, Importance High, Sent filled" % (nm, CC_NAME) if ok else
            "Header problem in the %s: %s" % (nm, hd))
    bt = text_of(body)
    add(bt.startswith("Dear %s," % a["client_first_name"].strip()) and "Kind regards" not in bt and "<img" not in body and "FSP45946" not in body and "Importance:" not in bt,
        "The pasted body runs from 'Dear %s,' to the next-meeting line: no header, no signature block, no 'Kind regards,', no logo" % a["client_first_name"].strip())
    nl = "Teams Meeting on %s, %s @ %s." % (rd.calendar.day_name[next_date(a).weekday()], next_date(a).strftime("%d/%m/%Y"), a["next_meeting"]["time"].strip())
    add(nl in bt and bt.rstrip().endswith(a["next_meeting"]["time"].strip() + "."), "The next meeting reads '%s' with its weekday computed" % next_line(a))
    add(("Teams Meeting on %s," % meetings_line(a)) in bt, "The meetings already held read '%s' with their weekdays computed" % meetings_line(a))
    miss = [x for x in _lines(a) if x not in bt]
    add(not miss, "Every figure is in the email as the template phrases it (age, employer, income, retirement age, net target, expenses, lump sum, monthly, escalation, sustainability age, shortfall period)"
        if not miss else "Missing from the email: %s" % miss[0])
    s, e = shortfall(a)
    add(s != e and s.startswith("1st ") and e.startswith("1st "), "The shortfall runs from %s to %s, worked out by the program from the next meeting and %s years" % (s, e, a["years_until_retirement"]))
    fixed = ("After taking into consideration the above mentioned additional investment contributions, your shortfall is as follows:", "You intend to save monies monthly.", "Hoping the above is in order.",
             "To change your income sustainability you can either review your requirements or change your investment amount/s and/or personal investment target.")
    add(all(x in bt for x in fixed), "The fixed text is there (the shortfall introduction, the sustainability advice, the closing line)")
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
    add((subject(a) in subs) if subs else (subject(a) in flat), "The subject is exactly the one in the HTML")
    imp = [x for x in (find_key(obj, ("importance",)) if obj is not None else []) if isinstance(x, str)]
    add((imp and imp[0].lower() == "high") if imp else bool(re.search(r"importance\W{1,6}high", flat, re.I)), "Importance is High")
    cands = [x for x in leaves if "Dear " in x and "<" in x]
    body = max(cands, key=len) if cands else flat
    add(body.count("<table") == body.count("</table>"), "Tables open = close in the saved draft (%d)" % body.count("<table"))
    kr = body.count("Kind regards,")
    add(kr == (1 if sig_mode == "insert" else 0), "'Kind regards,' appears %d time(s) (%s)" % (kr, "exactly once, from the inserted signature" if sig_mode == "insert" else "none: the server adds the signature"))
    add(not PLACEHOLDER.search(body) and "@@" not in body and "BODY_PLACEHOLDER" not in body, "No placeholder text is left in the draft (not even BODY_PLACEHOLDER)")
    add(not re.search(r"\bLoop\b", flat), "No Loop component is in the draft")
    bt = text_of(body)
    bold = len(re.findall(r"<(?:b|strong)[ >]", body))
    add("Your personal circumstances:" in bt and bold >= 2, "The section heading and the next-meeting line are bold (%d bold tags)" % bold)
    need = ["Dear %s," % a["client_first_name"].strip(), meetings_line(a), next_line(a)] + _lines(a)
    miss = [x for x in need if x not in bt]
    add(not miss, "The draft carries the client's name, the dates and every figure as the email phrases it" if not miss else "Missing from the draft: %s" % miss[0])
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
    add("<ol>" in flat and flat.count("<li>") == 1, "The RGAR report is a real numbered list")
    add("**" not in flat and "&lt;" not in flat and "\\u003c" not in flat, "No literal ** and no escaped tags show")
    add(rgar_name_no_ext(docs) in plain and ("%s > Comparative Quotes" % a["plan_folder"].strip()) in plain, "The message names the RGAR report and the folder (%s > Comparative Quotes)" % a["plan_folder"].strip())
    add(plain.rstrip().endswith("Once attached, please email the client - Thank you!") and "do not send" not in plain.lower() and "leave it in drafts" not in plain.lower(),
        "It ends 'Once attached, please email the client - Thank you!' with no 'do not send' line")
    return R


# ------------------------------------------------------------------ the confirmation table
GREETING_MARK = "<greeting by the clock>"


def table_rows(a, docs):
    s = a.get("sources") or {}
    start, end = shortfall(a)
    rows = [("Client (greeting, full name)", "%s (%s)" % (a["client_full_name"], a["client_first_name"]), s.get("personal")),
            ("Age (Fact Find Summary) and date of birth (RGAR)", "%d; born %s: they agree" % (a["age"], a["rgar_dob"]), s.get("rgar")),
            ("Works for (employer, job title)", "%s, %s" % (a["employer"], a["job_title"]), s.get("personal")),
            ("Gross monthly income", "R %s" % money_shown(a["gross_monthly_income"]), s.get("personal")),
            ("Retirement age; years until retirement", "%s; %s" % (int(w.parse_money(a["retirement_age"])), int(w.parse_money(a["years_until_retirement"]))), s.get("rgar")),
            ("Net monthly target in today's terms (the figure after its label in the Fact Find Summary)", "R %s" % money_shown(a["net_monthly_target"]), s.get("net_target")),
            ("Expected monthly expenses: current value (gross) and future value", "R %s gross; R %s" % (money_shown(a["current_value"]), money_shown(a["future_value"])), s.get("rgar")),
            ("Once-off lump sum required", "R %s" % money_shown(a["lump_sum"]), s.get("rgar")),
            ("Monthly recurring contribution required", "R %s" % money_shown(a["monthly"]), s.get("rgar")),
            ("Debit order escalation", "%s%%" % pct_digits(a["escalation"]), s.get("rgar")),
            ("Income sustainable until age", str(int(w.parse_money(a["sustainability_age"]))), s.get("rgar")),
            ("Recurring investment in the RGAR", "R %s" % money_shown(a["recurring_investment"]), s.get("rgar")),
            ("Shortfall period (worked out by the program)", "%s until %s" % (start, end), "the next meeting and the years until retirement"),
            ("RGAR file (attachment, copied into the folder)", rgar_name(docs), "the registered document"),
            ("Client email (To)", a["client_email"], s.get("email")),
            ("Meetings already held", meetings_line(a), s.get("meetings")),
            ("Next Teams meeting", next_line(a), s.get("next_meeting")),
            ("Subject", subject(a), "built by the program"),
            ("Cc", "%s (%s)" % (CC_NAME, CC_EMAIL), "fixed"),
            ("RA transaction folder (saved copy and the RGAR copy)", "%s > Comparative Quotes" % a["plan_folder"], "the client's file"),
            ("Signature in the Outlook draft", "inserted by Claude (Paul K New)" if settings()["signature_mode"] == "insert" else "added by the Exchange rule", "settings.json; the question is still open with Paul")]
    rows += [("Flag", x, "the program" if x == R0_FLAG else "the chat") for x in all_flags(a)]
    rows.append(("Teams message to Sitamah (sent only after the draft is checked; the greeting is set by the clock when it is sent)", teams_text(a, docs, GREETING_MARK), "fixed wording"))
    return rows
