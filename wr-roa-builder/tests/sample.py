"""INVENTED documents and answers for the ROA test (Pat Samplecase, invented insurers' wording, invented numbers). No real client, ever."""
import copy
import os
import stat
import sys

SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
sys.path.insert(0, SCRIPTS)


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


QUOTE_FNA = [["BrightRock proposal (FNA quote) for Pat Samplecase", "Summary: Value of your cover",
              "That's caused by death R 1 000 000", "That's permanent R 500 000", "That you can recover from R 20 000 per month", "Additional expense needs R 300 000",
              "Total premium (including the policy fee) R 1,172.80"]]
QUOTE_ACC = [["BrightRock proposal (Reduced quote) for Pat Samplecase", "Summary: Value of your cover",
              "That's caused by death R 1 000 000", "That's permanent R 400 000", "That you can recover from R 0 per month", "Additional expense needs R 0",
              "Total premium (including the policy fee) R 1,172.80"]]
APPLICATION = [["BrightRock General Short Risk Application", "Client: Pat Samplecase    ID number: 1111111111111", "Personal cover lines selected: life, disability, income",
                "Replacement: the client's existing Instant Life policy is being replaced"]]
NOTES = [["Follow-Up Appointment Summary Notes", "Client: Pat Samplecase", "The client accepted the reduced quote in the Teams meeting on 05/11/2026."]]
FACT_FIND = [["Fact Find Summary", "Client: Pat Samplecase    ID number: 1111111111111"]]
PROPOSAL_HTML = """<html><head><style>p{font-size:12pt}</style></head><body>
<table><tr><td>From:</td><td>adviser@example.invalid</td></tr><tr><td>Sent:</td><td>Tuesday, 11 August 2026 09:00</td></tr><tr><td>To:</td><td>pat@example.invalid</td></tr>
<tr><td>Subject:</td><td>Retirement Annuity proposal</td></tr></table>
<p>Hi Pat, please find the proposal for a Retirement Annuity Xtra Max at R 1 500.00 per month.</p><p style="font-size:10pt">Fine print.</p></body></html>"""
REPLY_HTML = """<html><head><style>p{font-size:12pt}</style></head><body>
<table><tr><td>From:</td><td>pat@example.invalid</td></tr><tr><td>Sent:</td><td>Wednesday, 12 August 2026 10:46</td></tr><tr><td>To:</td><td>adviser@example.invalid</td></tr>
<tr><td>Subject:</td><td>Re: Retirement Annuity proposal</td></tr></table>
<p>Hi All, as per our meeting today, kindly proceed with the attached. Regards, Pat</p></body></html>"""
COMPOSITE_HTML = """<html><head><style>p{font-size:12pt}</style></head><body>
<table><tr><td>From:</td><td>pat@example.invalid</td></tr><tr><td>Sent:</td><td>Wednesday, 12 August 2026 10:46</td></tr><tr><td>To:</td><td>adviser@example.invalid</td></tr>
<tr><td>Subject:</td><td>Re: Retirement Annuity proposal</td></tr></table>
<p>Hi All, as per our meeting today, kindly proceed with the attached. Regards, Pat</p>
<p>On Tuesday, 11 August 2026 at 09:00, Adviser wrote:</p>
<div style="border-left:3px solid #cccccc;padding-left:16px">
<table><tr><td>From:</td><td>adviser@example.invalid</td></tr><tr><td>Sent:</td><td>Tuesday, 11 August 2026 09:00</td></tr><tr><td>To:</td><td>pat@example.invalid</td></tr>
<tr><td>Subject:</td><td>Retirement Annuity proposal</td></tr></table>
<p>Hi Pat, please find the proposal for a Retirement Annuity Xtra Max at R 1 500.00 per month.</p><p style="font-size:10pt">Fine print.</p></div></body></html>"""
PROPOSAL_FIRST_HTML = COMPOSITE_HTML.replace("From:</td><td>pat@example.invalid", "From:</td><td>adviser@example.invalid", 1)


def make_docs(d):
    out = {}
    for role, pages in (("fna_quote", QUOTE_FNA), ("accepted_quote", QUOTE_ACC), ("application", APPLICATION), ("follow_up_notes", NOTES), ("fact_find_summary", FACT_FIND)):
        out[role] = os.path.join(d, role + ".pdf")
        _pdf(out[role], pages)
    for role, html in (("proposal_email", PROPOSAL_HTML), ("client_reply_email", REPLY_HTML), ("composite", COMPOSITE_HTML), ("proposal_first", PROPOSAL_FIRST_HTML)):
        out[role] = os.path.join(d, role + ".html")
        with open(out[role], "w", encoding="utf-8") as f:
            f.write(html)
    return out


def _prod(lists, key):
    return next(p for p in lists["products"] if key in p)


def risk_answers():
    import roa
    L = roa.template_lists()
    return {
        "bundle": "risk", "client_name": "Pat Samplecase", "client_id": "1111111111111", "risk_profile": "Moderate", "roa_date": "05/11/2026",
        "roa_date_source": {"type": "follow_up_notes", "file": "follow_up_notes"}, "insurers_considered": ["BRIGHTROCK"], "recommended_insurer": "BRIGHTROCK",
        "scope": "personal", "premium": "R 1 172.80", "conflicts": [],
        "sources": {"bundle": "follow_up_notes", "client_name_id": "application", "risk_profile": "Paul said", "insurers": "overview", "roa_date": "follow_up_notes", "scope": "application",
                    "replacement": "application", "taken_up": "accepted_quote", "premium": "accepted_quote", "amounts": "fna_quote and accepted_quote"},
        "covers": {
            "death": {"state": "accepted", "replacement": True, "scenario": "FNA DONE & ACCEPTED / REPLACEMENT:", "recommended_amount": "R 1 000 000", "taken_up_amount": "R 1 000 000",
                      "recommended_product": _prod(L, "(Life)")},
            "disability": {"state": "accepted", "replacement": True, "scenario": "FNA DONE BUT REDUCED QUOTE ACCEPTED / REPLACEMENT:", "recommended_amount": "R 500 000",
                           "taken_up_amount": "R 400 000", "need_identified": "Lump Sum Disability Cover", "recommended_product": _prod(L, "(Disability)")},
            "income_1st24": {"state": "not_accepted", "replacement": False, "new_while_other_replaced": False, "scenario": "FNA DONE / BENEFIT NOT ACCEPTED:", "recommended_amount": "R 20 000",
                             "taken_up_amount": "R 0", "need_identified": "Sickness and/or Income Protection Cover", "recommended_product": _prod(L, "(Temporary Sickness)")},
            "dread": {"state": "declined", "declined_reason": "The client already has severe illness cover through their employer.", "declined_source": "Paul said, 03/11/2026"},
        }}


def retirement_answers():
    return {
        "bundle": "retirement", "client_name": "Pat Samplecase", "client_id": "1111111111111", "risk_profile": "Moderate", "roa_date": "12/08/2026",
        "roa_date_source": {"type": "client_reply_email", "file": "client_reply_email"}, "insurers_considered": ["OLD MUTUAL"], "recommended_insurer": "OLD MUTUAL",
        "product_provider": "Old Mutual", "product_name": "Retirement Annuity Xtra Max", "amount": "R 1 500.00", "frequency": "monthly",
        "recommended_product": "Old Mutual Retirement Annuity Xtra Max", "replacement": False, "other_risk_cover_in_force": True, "conflicts": [],
        "reply_email": {"from": "pat@example.invalid", "sent": "12/08/2026 10:46", "to": "adviser@example.invalid", "cc": "", "subject": "Re: Retirement Annuity proposal",
                        "acceptance_text": "kindly proceed with the attached"},
        "sources": {"bundle": "client_reply_email", "client_name_id": "fact_find_summary", "risk_profile": "Paul said", "insurers": "proposal_email", "roa_date": "client_reply_email",
                    "product": "proposal_email", "amount": "client_reply_email", "replacement": "Paul said"}}


def investment_answers():
    a = retirement_answers()
    a.update(bundle="investment", need_identified="General Investment Planning", product_name="Tax-Free Investment Plan", recommended_product="Old Mutual - Max Investment", amount="R 1 500.00")
    a["other_risk_cover_in_force"] = False
    return a


def stub_wkhtmltopdf(d, log):
    """A stand-in for wkhtmltopdf used ONLY by the test (the real one is not installable here): it checks the mandated flags, then draws the page text
    with reportlab so the rest of the pipeline (images, embedding, the first-page check) runs for real."""
    path = os.path.join(d, "wkhtmltopdf")
    with open(path, "w") as f:
        f.write('''#!%s
import re, sys
args = sys.argv[1:]
open(%r, "a").write(" ".join(args) + "\\n")
need = ["--page-width", "8.5in", "--page-height", "11in", "--margin-left", "0.5in", "--margin-right", "0.5in", "--margin-top", "0.5in", "--margin-bottom", "0.5in"]
assert all(n in args for n in need) and "--zoom" not in args, args
html, pdf = args[-2], args[-1]
raw = open(html, encoding="utf-8").read()
sizes = re.findall(r"font-size:([0-9.]+)pt", raw)
text = re.sub(r"(?i)</(tr|p|div)>", "\\n", raw)
text = re.sub(r"(?s)<style.*?</style>", "", text)
text = re.sub(r"<[^>]+>", " ", text)
lines = [" ".join(l.split()) for l in text.splitlines() if l.strip()]
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
c = canvas.Canvas(pdf, pagesize=letter)
y = 740
for l in lines:
    c.setFont("Helvetica", 10)
    c.drawString(50, y, l[:110]); y -= 18
    if y < 60:
        c.showPage(); y = 740
c.showPage(); c.save()
''' % (sys.executable, log))
    os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)
    return path
