"""INVENTED documents and answers for the om-optimal-ra-proposal test (Pat Samplecase, invented insurer, fund and fee wording, invented numbers). No real client, ever."""
import copy
import json
import os
import sys
from decimal import Decimal

SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
sys.path.insert(0, SCRIPTS)

OWNER = "Patricia Anne Samplecase"
EMAIL = "pat@example.invalid"
FOLDER = "Samplecase, Pat - (OM RA - R3000)"
NAMES = {"quote": "OM Optimal RA Quote - P Samplecase.pdf", "booster_doc": "Optimal Illustrator - P Samplecase.pdf", "lump_sum_quote": "OM Lump Sum Quote - P Samplecase.pdf"}
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


PAGES = {
    "quote": [["Old Mutual Savings and Income - Optimal Retirement Annuity Plan Quote Report", "Client: %s" % OWNER, "Regular contribution R 3 000.00 per month", "Plan start date 01/12/2026",
               "FUND SELECTION", "Sample Balanced Fund 60% asset management fee 0.85%", "Sample Growth Fund 40% asset management fee 0.95%"],
              ["PAYABLE FROM THE PLAN'S FUND VALUE", "Net administration fee 3.05%", "Asset advice fees 0.575%", "Adviser remuneration account charge 0.00%", "Monthly fixed administration fee R 36.50"]],
    "fact_find_summary": [["Fact Find Summary", "Client: %s (Pat)" % OWNER, "Age: 40", "Employer: Sample Holdings", "Position: Analyst", "Gross monthly income: R 50 000.00", "Email: %s" % EMAIL]],
    "booster_doc": [["Optimal Illustrator - RA Booster Value", "Client: %s" % OWNER, "Monthly premium R 3 000.00", "Start date 01/12/2026"]],
    "astute_ccp": [["Astute Consolidated Client Portfolio", "Existing policies", "Samplelife Retirement Annuity SL-123456 Monthly contribution R 1 500.00 Gross fund value R 90 000.00 as at 30/09/2026"]],
    "client_overview": [["Client Overview - Current Investments", "Samplelife Retirement Annuity SL-123456 Gross R 90 000.00 Monthly R 1 500.00",
                         "Sample Preservation Fund PF-998877 Gross R 125 000.00 Penalties R 5 000.00 Net fund value R 120 000.00"]],
    "fund_statement": [["Pension Fund Statement", "Member: %s" % OWNER, "Employer contribution R 2 500.00 (5%)", "Member contribution R 3 750.00 (7.5%)", "Fund value R 150 000.00 as at 30/09/2026"]],
    "poi": [["Payslip", "Gross monthly income R 50 000.00", "Pension contribution R 3 750.00"]],
    "rgar": [["Retirement Goal Analysis Report", "Client: %s" % OWNER, "Retirement age: 65", "Years until retirement: 24", "Current value R 30 000.00", "Future value R 61 000.00"],
             ["WHAT YOU HAVE AGREED TO DO AND WHY", "Additional monthly contribution required R 4 200.00"]],
    "lump_sum_quote": [["Old Mutual Optimal Retirement Annuity - Lump Sum Quote (Plan 2)", "Client: %s" % OWNER, "Lump sum R 120 000.00", "Plan start date 01/12/2026", "Sample Cash Fund 100% asset management fee 0.45%",
                        "Administration fee 0.90%", "Asset advice fee 0.575%"]],
}


def make_docs(d):
    out = {}
    for role, pages in PAGES.items():
        out[role] = os.path.join(d, NAMES.get(role, role + ".pdf"))
        _pdf(out[role], pages)
    return out


SOURCES = {"personal": "Fact Find Summary", "income": "Fact Find Summary and the payslip", "fund": "the fund statement", "existing_ras": "the Astute report",
           "ra_decision": "Paul, in chat", "rgar": "the RGAR from Alwyn", "quote": "the OM Optimal RA Quote", "funds_fees": "the OM Optimal RA Quote", "email": "Fact Find Summary",
           "meetings": "dates in the transcript file names, confirmed by Paul", "next_meeting": "Paul, in chat"}


def answers():
    return {
        "client_full_name": OWNER, "client_first_name": "Pat", "client_surname": "Samplecase", "client_email": EMAIL, "email_source": "fact_find_summary", "email_note": "",
        "age": 40, "employer": "Sample Holdings", "position": "Analyst", "gross_monthly_income": "R 50 000.00",
        "fund": {"type": "pension", "employer_monthly": "R 2 500.00", "employer_pct": "5%", "member_monthly": "R 3 750.00", "member_pct": "7.5%", "value": "R 150 000.00", "value_date": "30/09/2026"},
        "existing_ras": [{"insurer": "Samplelife", "policy_number": "SL-123456", "monthly": "R 1 500.00", "gross_value": "R 90 000.00", "value_date": "30/09/2026", "no_penalties": False}],
        "ra_decision": "keep",
        "rgar": {"shortfall": "R 4 200.00", "years": "24", "current_value": "R 30 000.00", "future_value": "R 61 000.00", "retirement_age": "65"},
        "proposed_premium": "R 3 000.00", "start_date": "01/12/2026",
        "funds": [{"name": "Sample Balanced Fund", "allocation": "60", "asset_mgmt_fee": "0.85%"}, {"name": "Sample Growth Fund", "allocation": "40", "asset_mgmt_fee": "0.95%"}],
        "net_admin_fee": "3.05%", "advice_fee": "0.575%", "adviser_charge": "0.00%", "monthly_admin_fee": "R 36.50", "lump_sum_applies": True,
        "meetings_held": ["29/10/2026", "02/11/2026"], "next_meeting": {"date": "12/11/2026", "time": "12pm"},
        "plan_folder": FOLDER, "flags": ["The saved copy has no logo."], "sources": dict(SOURCES), "conflicts": []}


def lump_answers():
    return {
        "document": "lump_sum", "client_full_name": OWNER, "client_first_name": "Pat", "client_surname": "Samplecase", "client_email": EMAIL, "email_source": "fact_find_summary", "email_note": "",
        "lump": {"type": "section14", "amount": "R 120 000.00", "policies": [{"name": "Sample Preservation Fund", "net_value": "R 120 000.00"}]},
        "start_date": "01/12/2026", "funds": [{"name": "Sample Cash Fund", "allocation": "100", "asset_mgmt_fee": "0.45%"}],
        "ls_fees": {"admin_fee": "0.90%", "advice_fee": "0.575%", "as_and_when": "None"},
        "meetings_held": ["29/10/2026", "02/11/2026"], "next_meeting": {"date": "12/11/2026", "time": "12pm"}, "plan_folder": FOLDER, "flags": [], "conflicts": [],
        "sources": {"personal": "Fact Find Summary", "lump": "Paul, in chat, and the Client Overview", "quote": "the OM Lump Sum Quote", "email": "Fact Find Summary",
                    "meetings": "dates in the transcript file names, confirmed by Paul", "next_meeting": "Paul, in chat"}}


def bad(a, **path_value):
    """A copy of the answers with deep changes: bad(a, **{"next_meeting.time": "5"}); DELETE removes a key."""
    a = copy.deepcopy(a)
    for path, value in path_value.items():
        cur, keys = a, path.split(".")
        for k in keys[:-1]:
            cur = cur[int(k)] if isinstance(cur, list) else cur[k]
        last = keys[-1]
        if value is DELETE:
            if isinstance(cur, list):
                cur.pop(int(last))
            else:
                cur.pop(last, None)
        elif isinstance(cur, list):
            cur[int(last)] = value
        else:
            cur[last] = value
    return a


def fake_tax(a):
    """Tool results for the small model-level checks: the program's own independent recomputation stands in for LibreOffice (the journey tests use the real thing)."""
    import ori as o
    import taxtool as tt
    import wrlib as w
    ctx = o.tool_context(a)
    runs = {}
    for name, inp in tt.scenarios(ctx).items():
        ind = tt.independent(inp)
        outs = {k: str(v) for k, v in ind.items() if k != "taxable"}
        outs["switch_in_copy"] = tt.facts()["employment_switch"][inp["switch"]]
        bars = [str(ind["tax_saved_ra"] * (Decimal("1.1") ** i)) for i in range(10)]
        runs[name] = {"inputs": tt.ser(inp), "outputs": outs, "echo": {"remuneration": str(inp["remuneration"]), "age": str(inp["age"]), "ra_monthly": str(inp["ra_monthly"])}, "bars": bars, "problems": []}
    return {"workbook_sha": w.sha256_file(tt.WORKBOOK), "facts_sha": w.sha256_file(tt.FACTS), "soffice": "stand-in", "tax_year": tt.facts()["tax_year"], "runs": runs}


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
    if a.get("document") == "lump_sum":
        items = "<li>The OM Optimal RA Lump Sum Quote (%s)</li><li>The relevant fund fact sheet(s) as per the Lump Sum Quote (Sample Cash Fund)</li>" % NAMES["lump_sum_quote"][:-4]
        kind, where = "Lump Sum Investment proposal email", "Both are in Pat's folder"
    else:
        items = ("<li>The OM Optimal RA Quote (%s)</li><li>The relevant fund fact sheets as per the quote (Sample Balanced Fund &amp; Sample Growth Fund)</li>"
                 "<li>The OM Optimal RA Booster Value document (%s)</li><li>The \"OM Wealth Investment Strategy Summary\" document</li>") % (NAMES["quote"][:-4], NAMES["booster_doc"][:-4])
        kind, where = "proposal email", "All four are in Pat's folder"
    html = ("<p>%s Sitamah,</p><p><strong>Action needed:</strong> I have compiled the draft Old Mutual Optimal Retirement Annuity (RA) %s to %s and saved it in <strong>Drafts</strong> (To: %s, Cc: you).</p>"
            "<p>Please kindly attach the following to that draft:</p><ol>%s</ol><p>%s: %s &gt; Comparative Quotes.</p>"
            "<p>Once attached, please email the client - Thank you!</p>") % (greeting, kind, a["client_full_name"], a["client_email"], items, where, a["plan_folder"])
    if "html" in v:
        html = v["html"](html)
    return json.dumps({"id": "1700000000000", "body": {"contentType": "html", "content": html}})
