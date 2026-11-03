"""INVENTED documents and answers for the RGAR test (Pat Samplecase, invented insurer wording, invented numbers). No real client, ever."""
import copy
import json
import os
import sys

SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
sys.path.insert(0, SCRIPTS)

OWNER = "Patricia Anne Samplecase"
EMAIL = "pat@example.invalid"
FOLDER = "Samplecase, Pat - (OM RA - R2000)"
RGAR_NAME = "Retirement Goal Analysis - 03.11.26 - P Samplecase.pdf"
DELETE = object()


def _pdf(path, pages):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate
    st = getSampleStyleSheet()["Normal"]
    story = []
    for i, lines in enumerate(pages):
        story += [Paragraph(l.replace("&", "&amp;"), st) for l in lines]
        if i < len(pages) - 1:
            story.append(PageBreak())
    SimpleDocTemplate(path, pagesize=A4).build(story)


RGAR = [["Retirement Goal Analysis Report", "YOUR GOAL", "Client: %s" % OWNER, "Date of birth: 15/03/1985", "Retirement age: 65", "Years until retirement: 24",
         "Expected monthly expenses in retirement", "Current value R 30 000.00", "Future value R 61 000.00"],
        ["WHAT YOU HAVE AGREED TO DO AND WHY", "Once-off lump sum contribution required R 150 000", "Monthly recurring contribution required R 4 200.00",
         "Debit order escalation 6%", "Your income is projected to be sustainable until you are 85 years old", "Recurring investment R 2 000.00"]]


def _ffs(label_line, extra=()):
    return [["Fact Find Summary", "Client: %s (Pat)" % OWNER, "Age: 41", "Employer: Sample Holdings", "Occupation: Analyst", "Gross monthly income: R 45 000.00", "Email: %s" % EMAIL,
             "7. What the Client Requires", "Personal Risk Cover & Retirement", "Retirement Age: 65", label_line, "Reduced quote monthly contribution target R 1 500.00"] + list(extra)]


FFS = _ffs("Net amount needed at retirement R 25 000.00 per month")
FFS_OLD_LABEL = _ffs("Net Amount Needed (today's terms) (R) R 25 000.00")
FFS_NO_LABEL = _ffs("Income wanted at retirement R 25 000.00 per month")
FFS_OLDER = [["Fact Find Summary (older version)", "Client: %s" % OWNER, "Age: 40", "Employer: Sample Holdings", "Occupation: Analyst", "Gross monthly income: R 44 000.00", "Email: %s" % EMAIL]]


def make_docs(d):
    out = {}
    for role, pages in (("rgar_report", RGAR), ("fact_find_summary", FFS), ("fact_find_summary_older", FFS_OLDER), ("ffs_old_label", FFS_OLD_LABEL), ("ffs_no_label", FFS_NO_LABEL)):
        out[role] = os.path.join(d, RGAR_NAME if role == "rgar_report" else role + ".pdf")
        _pdf(out[role], pages)
    return out


SOURCES = {"rgar": "the RGAR from Alwyn", "personal": "Fact Find Summary", "net_target": "Fact Find Summary, the line after its label", "email": "Fact Find Summary",
           "meetings": "dates in the transcript file names, confirmed by Paul", "next_meeting": "Paul, in chat"}


def answers():
    return {
        "client_full_name": OWNER, "client_first_name": "Pat", "client_surname": "Samplecase", "age": 41, "rgar_dob": "15/03/1985", "retirement_age": "65", "years_until_retirement": "24",
        "current_value": "R 30 000.00", "future_value": "R 61 000.00", "net_monthly_target": "R 25 000.00", "lump_sum": "R 150 000", "monthly": "R 4 200.00", "escalation": "6%",
        "sustainability_age": "85", "recurring_investment": "R 2 000.00", "employer": "Sample Holdings", "job_title": "Analyst", "gross_monthly_income": "R 45 000.00",
        "client_email": EMAIL, "email_source": "fact_find_summary", "email_note": "", "meetings_held": ["29/10/2026", "02/11/2026"], "next_meeting": {"date": "12/11/2026", "time": "12pm"},
        "plan_folder": FOLDER, "flags": ["The saved copy has no logo."], "sources": dict(SOURCES), "conflicts": []}


def bad(a, **path_value):
    """A copy of the answers with deep changes: bad(a, **{"next_meeting.time": "5"}); DELETE removes a key."""
    a = copy.deepcopy(a)
    for path, value in path_value.items():
        cur, keys = a, path.split(".")
        for k in keys[:-1]:
            cur = cur[int(k)] if isinstance(cur, list) else cur[k]
        last = keys[-1]
        if value is DELETE:
            cur.pop(last, None)
        else:
            cur[last] = value
    return a


SIGNATURE = "<p>Kind regards,</p><p>Paul Kafentzis, FSP45946</p><p>Disclaimer and Confidentiality Notice: invented for the test.</p>"


def draft_json(a, body, subj, **v):
    """What an Outlook read-back could look like (invented shape): variants change one thing."""
    content = "<html><body>" + body + v.get("signature", SIGNATURE) + "</body></html>"
    if "content" in v:
        content = v["content"](content)
    return json.dumps({"id": "AAMkINVENTED", "subject": v.get("subject", subj),
                       "toRecipients": [{"emailAddress": {"address": v.get("to", EMAIL), "name": "Pat"}}],
                       "ccRecipients": [{"emailAddress": {"address": v.get("cc", "admin@liferisk.co.za"), "name": "Sitamah Nathoo"}}],
                       "importance": v.get("importance", "high"), "body": {"contentType": "html", "content": content}})


def message_json(a, greeting="Good morning", **v):
    html = ("<p>%s Sitamah,</p><p><strong>Action needed:</strong> I have compiled the draft Retirement Goal Analysis (RGAR) proposal email to %s and saved it in <strong>Drafts</strong> (To: %s, Cc: you).</p>"
            "<p>Please kindly attach the following to that draft:</p><ol><li>The RGAR report (%s)</li></ol><p>It is in %s's folder: %s &gt; Comparative Quotes.</p>"
            "<p>Once attached, please email the client - Thank you!</p>") % (greeting, a["client_full_name"], a["client_email"], RGAR_NAME[:-4], a["client_first_name"], a["plan_folder"])
    if "html" in v:
        html = v["html"](html)
    return json.dumps({"id": "1700000000000", "body": {"contentType": "html", "content": html}})
