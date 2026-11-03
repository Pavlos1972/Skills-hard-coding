"""INVENTED documents and answers for the OM Tax-Free test (Pat Samplecase, invented funds and wording, invented numbers). No real client, ever."""
import copy
import json
import os
import sys

SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
sys.path.insert(0, SCRIPTS)

OWNER = "Patricia Anne Samplecase"
EMAIL = "pat@example.invalid"
FOLDER = "Samplecase, Pat - (OM Tax-Free - R2500)"
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


QUOTE = [["Old Mutual Savings and Income - Tax Free Plan", "DETAILS OF YOUR COMPREHENSIVE TAX FREE PLAN", "Owner: %s" % OWNER, "Age: 41",
          "HOW WILL I CONTRIBUTE TO MY PLAN?", "Regular contribution: R 2 500.00 per month", "Start date: 01/12/2026"],
         ["HOW WILL MY MONEY BE INVESTED?", "Sample Balanced Fund 60%", "Sample Growth Fund 40%",
          "HOW MUCH WILL I PAY FOR THE MANAGEMENT OF MY INVESTMENT FUND(S)?", "Asset management fee 0.733%",
          "HOW MUCH WILL I PAY FOR THE ADMINISTRATION OF MY PLAN?", "Net administration fee 0.250%",
          "WHAT IS PAID TO MY ADVISER?", "Ongoing advice fee 0.500%", "Adviser remuneration account charge 0.100%"]]
FFS = [["Fact Find Summary", "Client: %s (Pat)" % OWNER, "Employer: Sample Holdings", "Position: Analyst", "Gross monthly income: R 45 000.00",
        "Email: %s" % EMAIL, "Risk Profile: Moderate"]]
FFS_OLD = [["Fact Find Summary (older version)", "Client: %s" % OWNER, "Employer: Sample Holdings", "Position: Analyst", "Gross monthly income: R 44 000.00", "Email: %s" % EMAIL]]
RISK = [["WR Risk"]]                                   # almost no text: a scanned page for the test of image-only pages
OVERVIEW = [["WR Overview for %s" % OWNER, "Current investments: none"]]
SHEET1 = [["Sample Balanced Fund fact sheet", "A balanced fund for the test."]]
SHEET2 = [["Sample Growth Fund fact sheet", "A growth fund for the test."]]
STRATEGY = [["OM Wealth Investment Strategy Summary", "The strategy summary for the test."]]


def make_docs(d):
    out = {}
    for role, pages in (("quote", QUOTE), ("fact_find_summary", FFS), ("fact_find_summary_older", FFS_OLD), ("risk_questionnaire", RISK), ("overview", OVERVIEW),
                        ("fund_fact_sheet_1", SHEET1), ("fund_fact_sheet_2", SHEET2), ("strategy_summary", STRATEGY)):
        out[role] = os.path.join(d, {"quote": "Pat Samplecase - Old Mutual Savings and Income - Tax Free Plan - R2500.pdf"}.get(role, role + ".pdf"))
        _pdf(out[role], pages)
    return out


def answers():
    return {
        "client_full_name": OWNER, "client_first_name": "Pat", "client_surname": "Samplecase", "owner_full_name": OWNER, "owner_is_child": False, "plan_type": "monthly",
        "owner_age": 41, "employer": "Sample Holdings", "position": "Analyst", "gross_monthly_income": "R 45 000.00", "contribution": "R 2 500.00",
        "start_date": "01/12/2026", "start_date_choice": {"choice": "quote", "paul_said": "Yes, the Quote's date stands"},
        "risk_profile": "Moderate", "risk_profile_source": "questionnaire", "risk_paul_said": "", "ffs_risk_profile": "Moderate",
        "funds": [{"name": "Sample Balanced Fund", "allocation": "60%"}, {"name": "Sample Growth Fund", "allocation": "40%"}],
        "fees": {"asset_management": "0.733%", "administration": "0.250%", "advice": "0.500%", "adviser_remuneration": "0.100%"},
        "fund_sheets": {"Sample Balanced Fund": "fund_fact_sheet_1", "Sample Growth Fund": "fund_fact_sheet_2"},
        "client_email": EMAIL, "email_source": "fact_find_summary", "email_note": "",
        "meetings_held": ["29/10/2026", "02/11/2026"], "next_meeting": {"date": "12/11/2026", "time": "5pm"},
        "plan_folder": FOLDER, "flags": ["The questionnaire pages were viewed as images (no text layer)."],
        "sources": {"quote": "the Tax-Free quote from Alwyn", "personal": "Fact Find Summary", "risk": "WR - New Risk Tolerance (viewed as images)", "email": "Fact Find Summary",
                    "meetings": "dates in the transcript file names, confirmed by Paul", "next_meeting": "Paul, in chat", "start_date": "Paul, in chat"},
        "conflicts": []}


def bad(a, **path_value):
    """A copy of the answers with deep changes: bad(a, **{"fees.advice": "0.73%"}); DELETE removes a key."""
    a = copy.deepcopy(a)
    for path, value in path_value.items():
        cur, keys = a, path.split(".")
        for k in keys[:-1]:
            cur = cur[int(k)] if isinstance(cur, list) else cur[k]
        last = keys[-1]
        if isinstance(cur, list):
            cur[int(last)] = value
        elif value is DELETE:
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


def message_json(a, quote_name, greeting="Good morning", **v):
    funds = ", ".join(f["name"] for f in a["funds"])
    html = ("<p>%s Sitamah,</p><p><strong>Action needed:</strong> I have compiled the draft Old Mutual Tax-Free proposal email to %s and saved it in <strong>Drafts</strong> (To: %s, Cc: you).</p>"
            "<p>Please kindly review that draft and attach the following to it:</p><ol><li>The OM Tax-Free Quote (%s)</li><li>The relevant fund fact sheets as per the quote (%s)</li>"
            "<li>The &quot;OM Wealth Investment Strategy Summary&quot; document</li></ol><p>All three are in %s's folder: %s &gt; Comparative Quotes.</p>"
            "<p>Once attached, please email the client - Thank you!</p>") % (greeting, a["client_full_name"], a["client_email"], quote_name, funds, a["client_first_name"], a["plan_folder"])
    if "html" in v:
        html = v["html"](html)
    return json.dumps({"id": "1700000000000", "body": {"contentType": "html", "content": html}})
