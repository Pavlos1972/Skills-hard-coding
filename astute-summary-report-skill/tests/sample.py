"""An INVENTED Astute-style report and the data a chat would enter for it. Invented people and numbers only (Pat Samplecase, Robin Testcase)."""
import copy

PAGES = [
    ["Consolidated Client Portfolio Report", "Report reference: CCP-TEST-0001    Report date: 05/11/2026",
     "Client: Pat Samplecase    ID number: 1111111111111    Date of birth: 01/01/1980", "Requested by: Test Adviser"],
    ["Insurer A Life", "Policy number AL-1001    Product: Alpha Life Plan    Status: Active    Start date: 01/03/2019",
     "Owner: Pat Samplecase    Life assured: Pat Samplecase    Premium payer: Pat Samplecase    Beneficiary: Robin Testcase 100%",
     "Benefit: Life cover R 1 000 000.00    Benefit: Severe illness cover R 500 000.00",
     "Premium R 350.00 monthly    Premium pattern: ACI    Annual escalation 5%",
     "Policy number AL-1002    Product: Alpha Growth Fund    Status: Active    Start date: 15/06/2020",
     "Owner: Pat Samplecase    Life assured: Pat Samplecase    Premium payer: Pat Samplecase",
     "Premiums paid R 100 000.00    Fund value R 120 345.67    Surrender value R 118 000.00",
     "Premium R 1 000.00 monthly    Premium pattern: fixed    Escalation 6%    Balanced Fund 60%    Equity Fund 40%"],
    ["Insurer A Life (continued)", "Policy number AL-0900    Product: Alpha Old Endowment    Status: Paid-up    Start date: 01/01/2005",
     "Owner: Pat Samplecase    Life assured: Pat Samplecase    Premium payer: Pat Samplecase",
     "Premiums paid R 20 000.00    Fund value R 15 000.00    Surrender value R 14 000.00    Premium pattern: fixed",
     "Insurer B Assurance: client record not found",
     "Insurer C Cover", "Policy number BC-77    Product: Beta Cover    Status: Lapsed    Start date: 01/01/2012",
     "Owner: Pat Samplecase    Life assured: Pat Samplecase    Premium payer: Pat Samplecase",
     "Benefit: Death cover R 0.00    Premium R 0.00 monthly    Premium pattern: fixed"],
    ["Group risk: no group risk cover is reflected.",
     "Retirement fund: Gamma Provident Fund    Employer: Test Employer    Membership start 01/02/2015    Fund value R 250 000.00"],
]

DATA = {
    "header": {"client_name": "Pat Samplecase", "id_number": "1111111111111", "date_of_birth": "01/01/1980", "report_reference": "CCP-TEST-0001",
               "report_date": "05/11/2026", "requested_by": "Test Adviser"},
    "providers": [{"name": "Insurer A Life", "result": "data"}, {"name": "Insurer B Assurance", "result": "not_found"}, {"name": "Insurer C Cover", "result": "data"}],
    "policies": [
        {"provider": "Insurer A Life", "policy_number": "AL-1001", "product_name": "Alpha Life Plan", "status": "Active", "start_date": "01/03/2019", "kind": "risk",
         "owner": "Pat Samplecase", "life_assured": "Pat Samplecase", "premium_payer": "Pat Samplecase", "beneficiaries": [{"name": "Robin Testcase", "percent": "100"}],
         "benefits": [{"name": "Life cover", "cover_amount": "R 1 000 000.00", "type": "stand-alone"}, {"name": "Severe illness cover", "cover_amount": "R 500 000.00", "type": "accelerated"}],
         "premium": "R 350.00", "premium_frequency": "monthly", "premium_pattern": "ACI", "pattern_text": "annual benefit increase 5%"},
        {"provider": "Insurer A Life", "policy_number": "AL-1002", "product_name": "Alpha Growth Fund", "status": "Active", "start_date": "15/06/2020", "kind": "investment",
         "owner": "Pat Samplecase", "life_assured": "Pat Samplecase", "premium_payer": "Pat Samplecase", "beneficiaries": [],
         "values": {"premiums_paid": "R 100 000.00", "fund_value": "R 120 345.67", "surrender_value": "R 118 000.00"},
         "premium": "R 1 000.00", "premium_frequency": "monthly", "premium_pattern": "fixed", "pattern_text": "escalation 6%",
         "fund_allocation": [{"fund": "Balanced Fund", "percent": "60"}, {"fund": "Equity Fund", "percent": "40"}]},
        {"provider": "Insurer A Life", "policy_number": "AL-0900", "product_name": "Alpha Old Endowment", "status": "Paid-up", "start_date": "01/01/2005", "kind": "investment",
         "owner": "Pat Samplecase", "life_assured": "Pat Samplecase", "premium_payer": "Pat Samplecase", "beneficiaries": [],
         "values": {"premiums_paid": "R 20 000.00", "fund_value": "R 15 000.00", "surrender_value": "R 14 000.00"}, "premium_pattern": "fixed"},
        {"provider": "Insurer C Cover", "policy_number": "BC-77", "product_name": "Beta Cover", "status": "Lapsed", "start_date": "01/01/2012", "kind": "risk",
         "owner": "Pat Samplecase", "life_assured": "Pat Samplecase", "premium_payer": "Pat Samplecase", "beneficiaries": [],
         "benefits": [{"name": "Death cover", "cover_amount": "R 0.00", "type": "unable"}], "premium": "R 0.00", "premium_frequency": "monthly", "premium_pattern": "fixed"},
    ],
    "section2": {"group_risk": {"reflected": False},
                 "retirement_fund": {"reflected": True, "details": ["Gamma Provident Fund; employer Test Employer; membership start 01/02/2015; fund value R 250 000.00"]}},
}


def data():
    return copy.deepcopy(DATA)


def make_pdf(path, pages=PAGES):
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
