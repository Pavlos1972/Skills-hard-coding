"""INVENTED documents and a typical change file for the client-pipeline-board test (Pat Samplecase, invented numbers, example.invalid addresses). No real client, ever."""
import os

NAME = "Pat Samplecase"
ID_NUMBER = "800101" + "5009087"      # an invented 13-digit number, built in two pieces so no ID-like number sits in any file
CELL = "082 555 0100"
EMAIL = "pat.samplecase@example.invalid"

FF_SUMMARY = [
    "Fact Find Summary",
    "Name: Pat Samplecase",
    "ID number: " + ID_NUMBER,
    "Cell number: 082 555 0100",
    "Personal email: pat.samplecase@example.invalid",
    "Life cover required: Yes. Sum assured R 2 000 000",
    "Group risk cover: Yes (note: client not sure)",
    "Retirement annuity: monthly contribution R 3 500",
    "Medical aid: Yes, wants a review of the current scheme",
    "Will: Yes, no current will",
]


def make_pdf(path, lines):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(path, pagesize=A4)
    y = 800
    for ln in lines:
        c.drawString(60, y, ln)
        y -= 22
    c.save()


def body(*paras):
    return "".join("<p>%s</p>" % x for x in paras)


def change_first(subject_doc, subject_quote):
    """The first-run change file: a new prospect with three lines, a General email, a Lizelle quote request, a Medical Aid referral, a follow-up."""
    ev = lambda line: {"doc": "fact_find_summary", "line": line}
    return {
        "ops": [
            {"op": "init", "client": {"first": "Pat", "surname": "Samplecase"}, "kind": "prospect", "paul_said": "Brand-new prospect"},
            {"op": "prospect_log", "date": "05/11/2026", "text": "Fact Find meeting held on Teams"},
            {"op": "add_line", "line": "life_cover"},
            {"op": "tag", "line": "life_cover", "tag": "New Business", "paul_said": "A new policy, not a servicing change"},
            {"op": "add_line", "line": "retirement_annuity"},
            {"op": "tag", "line": "retirement_annuity", "tag": "New Business", "paul_said": "A new RA for her"},
            {"op": "add_line", "line": "medical_aid"},
            {"op": "identified", "card": "fact_find", "bullets": [
                {"text": "Life cover needed: R2 000 000", "evidence": ev("Life cover required: Yes. Sum assured R 2 000 000")},
                {"text": "Retirement annuity: R3 500 a month", "evidence": ev("Retirement annuity: monthly contribution R 3 500")},
                {"text": "Medical aid review wanted", "evidence": ev("Medical aid: Yes, wants a review of the current scheme")},
                {"text": "Group risk cover unclear", "evidence": ev("Group risk cover: Yes (note: client not sure)"), "provisional": "the form says Yes, the note says client not sure"}]},
            {"op": "identified", "card": "general", "bullets": [{"text": "Latest policy schedule and proof of income needed", "paul_said": "Ask her for the schedule and her payslip"}]},
            {"op": "identified", "card": "life_cover", "bullets": [{"text": "Sum assured R2 000 000", "evidence": ev("Life cover required: Yes. Sum assured R 2 000 000")}]},
            {"op": "pending", "card": "life_cover", "text": "Which insurer for the FNA quote, and do you want a Reduced Quote now or to hold for the Group Risk statement?"},
            {"op": "followup", "date": "20/11/2026", "time": "16:00", "source": "agreed on the call, Paul's words", "via": "teams-meeting-setup-skill", "receipt": "skill.teams.run"},
            {"op": "action", "card": "life_cover", "text": "Follow-up Teams invite sent", "receipt": "skill.teams.run", "via": "teams-meeting-setup-skill"},
        ],
        "emails": [
            {"id": "e1", "route": "general_document_request", "card": "general", "to": [EMAIL], "cc": ["admin@liferisk.co.za"], "subject": subject_doc,
             "body_html": body("Dear Pat,", "Please send us your latest policy schedule and your most recent payslip so we can prepare your quotes.", "Thank you."),
             "client_details": {"email": EMAIL}, "asked_paul": "Yes, send her one email", "action_text": "Document-request email saved in Outlook Drafts"},
            {"id": "e2", "route": "quote_request_life", "card": "life_cover", "to": ["Lizelle.Cachado@brightrock.co.za"], "cc": ["admin@liferisk.co.za"], "subject": subject_quote,
             "body_html": body("Dear Lizelle,", "Please quote an FNA for Pat Samplecase, life cover of R2 000 000, new business.",
                               "Please see attached Fact Find Summary for this client.", "This is urgent because the follow-up meeting is on 20/11/2026."),
             "thread": {"none_found": "searched Outlook for Lizelle and Samplecase, nothing"}, "asked_paul": "BrightRock, FNA basis", "action_text": "FNA quote request to Lizelle saved in Outlook Drafts",
             "client_details": {"email": EMAIL}},
            {"id": "e3", "route": "medical_aid_referral", "card": "medical_aid", "to": ["valeries@hampshireind.co.za"],
             "cc": ["jhbhealthadmin@hampshireind.co.za", EMAIL, "admin@liferisk.co.za", "paulk@liferisk.co.za"], "subject": "Pat Samplecase / Medical aid referral",
             "body_html": body("Dear Valerie,", "Please would you assist Pat Samplecase with a review of her medical aid scheme.",
                               "Name: Pat Samplecase", "ID number: " + ID_NUMBER, "Cell number: 082 555 0100", "Email: pat.samplecase@example.invalid", "Thank you."),
             "client_details": {"name": NAME, "id_number": ID_NUMBER, "cell": CELL, "email": EMAIL,
                               "evidence": {"Name": "fact_find_summary", "ID number": "fact_find_summary", "Cell number": "fact_find_summary", "Email": "fact_find_summary"}},
             "action_text": "Medical aid referral sent to Valerie"},
        ],
        "notify": [
            {"trigger": "general_email_drafted", "slots": {"draft_subject": subject_doc}},
            {"trigger": "lizelle_attach", "slots": {"draft_subject": subject_quote, "folder": "Pat Samplecase > 2. Fact Find"}},
        ],
    }
