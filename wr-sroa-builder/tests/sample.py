"""INVENTED documents and answers for the SROA test (Pat Samplecase, invented insurers' wording, invented numbers). No real client, ever."""
import copy
import os
import sys

SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
sys.path.insert(0, SCRIPTS)

POLICY = "TEST-100200"
OTHER = "TEST-900800"
FLAT_POLICY = "TEST-555666"
ID = "1111111111111"
OWNER = "Patricia Anne Samplecase"


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


MANUAL = [
    ["Owner's Manual for Patricia Anne Samplecase", "Contents: the schedules of all your policies"],
    ["Policy Schedule", "Policy Number %s" % POLICY, "Owner: %s" % OWNER, "ID number: %s" % ID,
     "Cover caused by death R 1 200 000", "Permanent cover R 600 000", "Recoverable income R 25 000 per month", "Additional expense needs R 300 000",
     "Yearly base increase 5%", "Yearly premium increase 5%", "Total premium (including the policy fee) R 1 300.00"],
    ["Policy Schedule", "Policy Number %s" % OTHER, "Owner: %s" % OWNER,
     "Cover caused by death R 750 000", "Permanent cover R 250 000", "Recoverable income R 9 000 per month", "Additional expense needs R 100 000",
     "Yearly base increase 4%", "Yearly premium increase 4%", "Total premium (including the policy fee) R 640.00"],
]
QUOTE_FNA = [["BrightRock proposal (Servicing FNA quote) for Pat Samplecase", "Proposal number CP111222", "Policy Number %s" % POLICY,
              "Cover caused by death R 1 500 000", "Permanent cover R 700 000", "Recoverable income R 30 000 per month", "Additional expense needs R 350 000",
              "Yearly base increase 5%", "Yearly premium increase 5%", "Total premium (including the policy fee) R 1 650.00"]]
QUOTE_ALT = [["BrightRock proposal (Alternative quote) for Pat Samplecase", "Proposal number CP333444", "Policy Number %s" % POLICY,
              "Cover caused by death R 1 000 000", "Permanent cover R 400 000", "Recoverable income R 20 000 per month", "Additional expense needs R 250 000",
              "Yearly base increase 5%", "Yearly premium increase 5%", "Total premium (including the policy fee) R 1 172.80"]]
FACT_FIND = [["Fact Find Summary", "Client: %s (Pat)" % OWNER, "ID number: %s" % ID]]
EMAIL = ("From: pat@example.invalid\nSent: Tuesday, 3 November 2026 10:15\nTo: adviser@example.invalid\nSubject: Re: Alternative Quote CP333444\n\n"
         "Hi, I accept the Alternative Quote CP333444 for policy %s. Regards, Pat\n" % POLICY)

# a second, flat-layout case (another insurer, Shortfall + Alternative compiled, FNA declined)
FLAT_PS = [["Policy Schedule", "Policy Number %s" % FLAT_POLICY, "Owner: %s" % OWNER, "ID number: %s" % ID,
            "Life Cover R 500 000", "Disability Cover R 400 000", "Dread Disease R 200 000", "Income Protection R 15 000 per month", "Premium R 900.00 per month, including the policy fee",
            "Annual cover increase 6%", "Annual premium increase 6%"]]
FLAT_SHORT = [["Sampleinsurer Shortfall quote for Pat Samplecase", "Proposal number CP555111", "Policy Number %s" % FLAT_POLICY,
               "Life Cover R 550 000", "Disability Cover R 420 000", "Premium R 990.00 per month, including the policy fee"]]
FLAT_ALT = [["Sampleinsurer Alternative quote for Pat Samplecase", "Proposal number CP555222", "Policy Number %s" % FLAT_POLICY,
             "Life Cover R 450 000", "Disability Cover R 400 000", "Dread Disease R 200 000", "Income Protection R 15 000 per month",
             "Premium R 800.00 per month, including the policy fee", "Annual cover increase 6%", "Annual premium increase 6%"]]
FLAT_EMAIL = ("From: pat@example.invalid\nSent: Monday, 2 November 2026 09:40\nSubject: Re: Alternative Quote CP555222\n\n"
              "Please proceed with the Alternative Quote CP555222 for policy %s. Pat\n" % FLAT_POLICY)


def make_docs(d):
    out = {}
    for role, pages in (("current_ps", MANUAL), ("fna_quote", QUOTE_FNA), ("alternative_quote", QUOTE_ALT), ("fact_find_summary", FACT_FIND),
                        ("flat_ps", FLAT_PS), ("flat_shortfall", FLAT_SHORT), ("flat_alternative", FLAT_ALT)):
        out[role] = os.path.join(d, role + ".pdf")
        _pdf(out[role], pages)
    for role, text in (("acceptance_email", EMAIL), ("flat_email", FLAT_EMAIL)):
        out[role] = os.path.join(d, role + ".txt")
        with open(out[role], "w", encoding="utf-8") as f:
            f.write(text)
    return out


PREM = "Premium (incl. R20 policy fee)"
ACI = "ACI (Automatic Cover Increase)"
ABI = "ABI (Automatic Benefit Increase)"


def _g(heading, *items):
    return {"heading": heading, "items": list(items)}


def _v(label, value, unit):
    return {"label": label, "value": value, "unit": unit}


def _c(label, old, new, unit, **kw):
    d = {"label": label, "old": old, "new": new, "unit": unit}
    d.update(kw)
    return d


SOURCES = {"quotes": "Paul in chat and the quote documents", "accepted_quote": "acceptance email", "owner_id": "Fact Find Summary and the policy schedule",
           "sroa_date": "acceptance email (Sent line)", "signature_name": "Fact Find Summary", "cp": "the quotes and the acceptance email", "investment_linked": "Paul, in chat"}


def answers_grouped():
    return {
        "insurer": "BrightRock", "policy_number": POLICY, "owner": OWNER, "owner_id": ID, "client_first_name": "Pat", "client_surname": "Samplecase",
        "client_signature_name": OWNER, "sroa_date": "03/11/2026", "sroa_date_source": {"file": "acceptance_email", "paul_said": ""},
        "compiled": {"fna": True, "shortfall": False, "alternative": True}, "accepted": "alternative", "cp_numbers": {"fna": "CP111222", "alternative": "CP333444"},
        "layout": "grouped",
        "blocks": {
            "fna": {"groups": [_g("Life Cover", _v("Cover caused by death", "R1,500,000", "amount")), _g("Lump Sum Disability Cover", _v("Permanent cover", "R700,000", "amount")),
                               _g("Income Protector / Sickness Benefit", _v("Recoverable income", "R30,000", "monthly")),
                               _g("Additional Expense Needs / Dread Disease", _v("Additional expense needs", "R350,000", "amount")),
                               _g("Policy Details", _v(PREM, "R1,650.00", "premium"), _v(ACI, "5%", "percent"), _v(ABI, "5%", "percent"))]},
            "alternative": {"groups": [_g("Life Cover", _v("Cover caused by death", "R1,000,000", "amount")), _g("Lump Sum Disability Cover", _v("Permanent cover", "R400,000", "amount")),
                                       _g("Income Protector / Sickness Benefit", _v("Recoverable income", "R20,000", "monthly")),
                                       _g("Additional Expense Needs / Dread Disease", _v("Additional expense needs", "R250,000", "amount")),
                                       _g("Policy Details", _v(PREM, "R1,172.80", "premium"), _v(ACI, "5%", "percent"), _v(ABI, "5%", "percent"))]}},
        "changes": {"groups": [_g("Life Cover", _c("Cover caused by death", "R1,200,000", "R1,000,000", "amount")),
                               _g("Lump Sum Disability Cover", _c("Permanent cover", "R600,000", "R400,000", "amount")),
                               _g("Income Protector / Sickness Benefit", _c("Recoverable income", "R25,000", "R20,000", "monthly")),
                               _g("Additional Expense Needs / Dread Disease", _c("Additional expense needs", "R300,000", "R250,000", "amount")),
                               _g("Policy Details", _c(PREM, "R1,300.00", "R1,172.80", "premium"), _c(ACI, "5%", "5%", "percent"), _c(ABI, "5%", "5%", "percent"))]},
        "reason": "Pat asked for a lower premium because her income dropped; the Alternative Quote keeps cover in line with what she can afford.",
        "reason_source": "Paul, 03/11/2026, in chat", "investment_linked": False, "portfolio_reason": "", "portfolio_source": "",
        "sources": dict(SOURCES), "conflicts": []}


def answers_flat():
    return {
        "insurer": "Sampleinsurer", "policy_number": FLAT_POLICY, "owner": OWNER, "owner_id": ID, "client_first_name": "Pat", "client_surname": "Samplecase",
        "client_signature_name": OWNER, "sroa_date": "02/11/2026", "sroa_date_source": {"file": "acceptance_email", "paul_said": ""},
        "compiled": {"fna": False, "shortfall": True, "alternative": True}, "fna_declined": True, "accepted": "alternative",
        "cp_numbers": {"shortfall": "CP555111", "alternative": "CP555222"}, "layout": "flat",
        "blocks": {"shortfall": {"groups": [_g("Life Cover", _v("Life Cover", "R550,000", "amount")), _g("Lump Sum Disability Cover", _v("Disability Cover", "R420,000", "amount")),
                                            _g("Policy Details", _v(PREM, "R990.00", "premium"))]},
                   "alternative": {"groups": [_g("Life Cover", _v("Life Cover", "R450,000", "amount")), _g("Lump Sum Disability Cover", _v("Disability Cover", "R400,000", "amount")),
                                              _g("Policy Details", _v(PREM, "R800.00", "premium"))]}},
        "changes": {"items": [_c(PREM, "R900.00", "R800.00", "premium"), _c("Life Cover", "R500,000", "R450,000", "amount"), _c(ABI, "6%", "6%", "percent"),
                              _c("Disability Cover", "R400,000", "R400,000", "amount"), _c(ACI, "6%", "6%", "percent"), _c("Dread Disease", "R200,000", "R200,000", "amount"),
                              _c("Income Protection", "R15,000", "R15,000", "monthly")]},
        "reason": "Pat can no longer afford the current premium, so she accepted the Alternative Quote with a lower life cover.",
        "reason_source": "Paul, 02/11/2026, in chat", "investment_linked": False, "portfolio_reason": "", "portfolio_source": "",
        "sources": dict(SOURCES, sroa_date="acceptance email (Sent line)"), "conflicts": []}


def bad(answers, **path_value):
    """A copy of the answers with one deep change: bad(a, **{"blocks.fna.groups.0.items.0.value": "R9"})."""
    a = copy.deepcopy(answers)
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


DELETE = object()
