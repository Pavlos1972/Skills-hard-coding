"""INVENTED documents and plans for the complete-applications-skill test (Pat Samplecase, Robin Testcase, example.invalid, the invented insurer Samplelife).
ID numbers are computed here (never typed as digits), so no ID-like number sits in any file. No real client, ever."""
import os

NAME = "Pat Samplecase"


def make_id(prefix12, ok=True):
    """A 13-digit South African style ID number with a right (or deliberately wrong) check digit."""
    tot = 0
    for i, ch in enumerate(prefix12):
        x = int(ch)
        if i % 2:
            x = x * 2
            x = x - 9 if x > 9 else x
        tot += x
    chk = (10 - tot % 10) % 10
    if not ok:
        chk = (chk + 1) % 10
    return prefix12 + str(chk)


PAT_ID = make_id("800101" + "5009" + "08")
ROBIN_ID = make_id("100202" + "5011" + "08", ok=False)          # a wrong check digit on purpose: the program only FLAGS it
ACCOUNT = "62" + "123456789"
NEW_ACCOUNT = "62" + "987654321"
ACCOUNT3 = "62" + "555555555"

FF = [
    "Fact Find Summary - Pat Samplecase",
    "Title: Ms",
    "Name: Pat Samplecase",
    "First names: Pat",
    "Surname: Samplecase",
    "ID number: " + PAT_ID,
    "Cell number: 082 555 0100",
    "Personal email: pat.samplecase@example.invalid",
    "Marital status: Single",
    "Occupation: Analyst",
    "Foreign tax obligation: No",
    "Advisor knows the source of funds: Yes",
    "Account holder: Pat Samplecase",
    "Bank: FNB",
    "Branch code: 250655",
    "Account type: Current",
    "Account number: " + ACCOUNT,
    "Beneficiary: Robin Testcase, son, 100%",
    "Beneficiary ID number: " + ROBIN_ID,
    "Start date: 01/12/2026",
    "Replacing an existing policy: Yes",
]
SCHEDULE = ["Samplelife policy schedule", "Policy holder: Pat Samplecase", "Policy No. SL-123456", "Monthly premium R 950.00"]


def make_pdf(path, lines):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(path, pagesize=A4)
    y = 800
    for ln in lines:
        c.drawString(60, y, ln)
        y -= 20
    c.save()


def ev(line):
    return {"doc": "fact_find", "line": line}


def E(value, line):
    return {"value": value, "evidence": ev(line)}


def om_fields():
    return {
        "Title": E("Ms", "Title: Ms"),
        "FullName": E("Pat Samplecase", "Name: Pat Samplecase"),
        "IDNumber": E(PAT_ID, "ID number: " + PAT_ID),
        "TelCell": E("082 555 0100", "Cell number: 082 555 0100"),
        "Email": E("pat.samplecase@example.invalid", "Personal email: pat.samplecase@example.invalid"),
        "MaritalStatus": E("Single", "Marital status: Single"),
        "Occupation": E("Analyst", "Occupation: Analyst"),
        "ForeignTaxObligation": E("No", "Foreign tax obligation: No"),
        "OwnKnowledge": E("Yes", "Advisor knows the source of funds: Yes"),
        "DeferredPremiumFacility": {"value": "No", "paul_said": "No deferred premium facility, as discussed"},
        "AccountHolder": E("Pat Samplecase", "Account holder: Pat Samplecase"),
        "NameOfBank": E("FNB", "Bank: FNB"),
        "BranchCode": E("250655", "Branch code: 250655"),
        "AccountType": E("Current", "Account type: Current"),
        "AccountNumber": E(ACCOUNT, "Account number: " + ACCOUNT),
        "BenName": E("Robin", "Beneficiary: Robin Testcase, son, 100%"),
        "BenSurname": E("Testcase", "Beneficiary: Robin Testcase, son, 100%"),
        "BenIDNumber": E(ROBIN_ID, "Beneficiary ID number: " + ROBIN_ID),
        "BenRelationship": E("son", "Beneficiary: Robin Testcase, son, 100%"),
        "BenShare": E("100", "Beneficiary: Robin Testcase, son, 100%"),
        "DateOfEntry": E("01/12/2026", "Start date: 01/12/2026"),
    }


def general_fields():
    return {
        "owner": E("Pat Samplecase", "Name: Pat Samplecase"),
        "owner_pays": {"value": "Yes", "paul_said": "She pays the premium herself"},
        "title": E("Ms", "Title: Ms"),
        "first_names": E("Pat", "First names: Pat"),
        "surname": E("Samplecase", "Surname: Samplecase"),
        "id_number": E(PAT_ID, "ID number: " + PAT_ID),
        "cell": E("082 555 0100", "Cell number: 082 555 0100"),
        "email": E("pat.samplecase@example.invalid", "Personal email: pat.samplecase@example.invalid"),
        "account_holder": E("Pat Samplecase", "Account holder: Pat Samplecase"),
        "bank": E("FNB", "Bank: FNB"),
        "branch_code": E("250655", "Branch code: 250655"),
        "account_type": E("Current", "Account type: Current"),
        "account_number": E(ACCOUNT, "Account number: " + ACCOUNT),
        "debit_date": {"value": "25th", "paul_said": "Debit on the 25th"},
        "insolvent": {"value": "No", "paul_said": "Not insolvent, from the meeting"},
        "debt_review": {"value": "No", "paul_said": "Not under debt review, from the meeting"},
        "debt_assistance": {"value": "No", "paul_said": "No debt assistance, from the meeting"},
    }


def plan_prefill(listing=None):
    return {
        "mode": "prefill",
        "listing": {"applications": listing if listing is not None else ["Notes.pdf", "OM - Optimal RA Application - 13.10.26 - R 2,500.00 p.m. - (Pat Samplecase).pdf"]},
        "apps": [
            {"id": "a1", "form": "om", "insurer": {"name": "Old Mutual"}, "product": {"option": "OM Optimal RA – Recurring", "type": "Recurring"}, "kind": "recurring", "amount": "2800",
             "meeting_date": "20/11/2026", "fields": om_fields(), "replacement": {"answer": "No", "source": {"paul_said": "No replacement, a new RA"}},
             "txn_folder": {"root": "New Business", "current_name": "Samplecase, Pat - (OM RA - R2800)", "is_current_transaction": True}},
            {"id": "a2", "form": "general", "insurer": {"name": "Brightrock"}, "product": {"cover_line": "Personal Covers"}, "kind": "recurring", "amount": "1000",
             "meeting_date": "20/11/2026", "fields": general_fields(),
             "replacement": {"answer": "Yes", "source": ev("Replacing an existing policy: Yes"),
                             "policies": [{"insurer": "Samplelife", "policy_no": "SL-123456", "evidence": {"doc": "policy_schedule", "line": "Policy No. SL-123456"}}]},
             "txn_folder": {"root": "New Business", "current_name": "Samplecase, Pat - (BR - Personal Covers - R 1,000.00 p.m.)", "is_current_transaction": True}},
        ],
    }
