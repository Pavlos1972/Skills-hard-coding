"""INVENTED documents and answers for the investment comparison test (Pat Samplecase, the invented providers Samplelife and Testco, invented funds, fees and wording).
No real client, provider quote or fund fact sheet, ever."""
import copy
import json
import os
import sys

SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
sys.path.insert(0, SCRIPTS)

OWNER = "Patricia Anne Samplecase"
EMAIL = "pat@example.invalid"
FOLDER = "Samplecase, Pat - (RA comparison)"
DELETE = object()
NAMES = {"quote_samplelife": "Samplelife RA Quote - P Samplecase.pdf", "quote_testco": "Testco RA Illustration - P Samplecase.pdf", "supplement_testco_booster_illustrator": "Testco Booster Illustrator - P Samplecase.pdf"}
SHEETS = {"Samplelife - Sample Balanced Fund": "balanced", "Samplelife - Sample Growth Fund": "growth", "Testco - Test Cautious Fund": "cautious"}


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
    "quote_samplelife": [["Samplelife Retirement Annuity Quote", "Client: %s" % OWNER, "Monthly premium R 3 000.00", "Yearly increase 10%", "Retirement age 65",
                          "Fund selection", "Sample Balanced Fund 60% asset management fee 0.85%", "Sample Growth Fund 40% asset management fee 0.95%"],
                         ["Fees", "Net administration fee 1.20%", "Ongoing advice fee 0.575%", "Adviser remuneration account charge 0.00%", "Initial commission 3.00%",
                          "Samplelife Loyalty Bonus 2.5% paid at retirement if no premiums are missed, and 1.0% each later year"]],
    "quote_testco": [["Testco Retirement Annuity Illustration", "Client: %s" % OWNER, "Monthly premium R 3 000.00", "Yearly increase 10%", "Retirement age 65",
                      "Test Cautious Fund 100% asset management fee 0.60%", "Administration fee 0.90%", "Ongoing advice fee 0.575%", "Initial advice fee R 0.00",
                      "Performance fee on the Test Cautious Fund: 20% of the return above its benchmark", "Wealth Bonus 2.0% paid at retirement, funded by a lower charge in the early years"]],
    "supplement_testco_booster_illustrator": [["Testco Booster Illustrator dated 06/07/2026", "Client: %s" % OWNER, "Wealth Bonus 3.50%", "Monthly premium R 3 000.00"]],
    "fact_find": [["Fact Find Summary", "Client: %s (Pat)" % OWNER, "Email: %s" % EMAIL, "Risk profile: Moderate"]],
    "tfsa_statement": [["Tax-Free Savings Account statement", "Client: %s" % OWNER, "Contributed this tax year R 10 000.00", "Contributed in total R 120 000.00"]],
}
TXT = {
    "balanced": "Sample Balanced Fund fact sheet. Fund data as at 30 September 2026. Benchmark: CPI plus 5%. Objective: CPI + 5% over rolling five years. Performance per year: 1 year 8.2% 3 years 9.1% 5 years 10.3%. "
                "Risk rating: Moderate. The fund spreads money between shares, bonds, property and cash.",
    "growth": "Sample Growth Fund fact sheet. Fund data as at 30 September 2026. Benchmark: ASISA Aggressive Allocation average. Objective: CPI + 6% over rolling seven years. Performance per year: "
              "1 year 11.4% 3 years 12.0% 5 years 13.5%. Risk rating: Aggressive. The fund holds mostly shares.",
    "cautious": "Test Cautious Fund fact sheet. Fund data as at 31 October 2026. Benchmark: CPI plus 3%. Objective: CPI + 3% over rolling three years. Performance per year: 1 year 6.1% 3 years 6.9% 5 years 7.4%. "
                "Risk rating: Cautious. The fund mostly holds bonds and cash.",
}


def make_docs(d, testco_premium="R 3 000.00"):
    """{registry key: path}: the quote, Fact Find, supplement and TFSA files, and the saved fact sheet texts."""
    out = {}
    for key, pages in PAGES.items():
        out[key] = os.path.join(d, NAMES.get(key, key + ".pdf"))
        if key == "quote_testco" and testco_premium != "R 3 000.00":
            pages = [[l.replace("Monthly premium R 3 000.00", "Monthly premium " + testco_premium) for l in pages[0]]]
        _pdf(out[key], pages)
    for lab, short in SHEETS.items():
        k = "factsheet_" + "".join(ch if ch.isalnum() else "_" for ch in lab.lower()).strip("_")
        k = "_".join(x for x in k.split("_") if x)
        out[k] = os.path.join(d, "factsheet-%s.txt" % short)
        with open(out[k], "w", encoding="utf-8") as f:
            f.write(TXT[short])
    return out


def make_tfsa_docs(d):
    """Two invented Tax-Free quotes (the second one proposes R 4 000.00 a month, which is over a R46,000 yearly limit)."""
    out = {}
    for key, name, prem in (("quote_samplelife", "Samplelife", "R 3 000.00"), ("quote_testco", "Testco", "R 4 000.00")):
        pages = [l.replace("Retirement Annuity Quote", "Tax-Free Savings Account Quote").replace("Retirement Annuity Illustration", "Tax Free Savings Account Illustration").replace("Retirement age 65", "No fixed term")
                 .replace("Monthly premium R 3 000.00", "Monthly premium " + prem).replace("Yearly increase 10%", "Yearly increase 0%") for l in PAGES[key][0]]
        out[key] = os.path.join(d, "tfsa-" + key + ".pdf")
        _pdf(out[key], [pages] + PAGES[key][1:])
    return out


SOURCES = {"personal": "Fact Find Summary", "risk": "Fact Find Summary", "providers": "the two quotes", "fees": "the two quotes", "funds": "the two quotes and the fund fact sheets",
           "email": "Fact Find Summary", "meetings": "dates in the transcript file names, confirmed by Paul", "next_meeting": "Paul, in chat", "supplement": "the Testco Booster Illustrator"}
FUNDS = [{"provider": "Samplelife", "name": "Sample Balanced Fund"}, {"provider": "Samplelife", "name": "Sample Growth Fund"}, {"provider": "Testco", "name": "Test Cautious Fund"}]


def answers():
    return {
        "client_full_name": OWNER, "client_first_name": "Pat", "client_surname": "Samplecase", "client_email": EMAIL, "email_source": "fact_find", "email_note": "",
        "product_type": "RA", "risk_profile": "Moderate",
        "providers": [
            {"name": "Samplelife", "product_name": "Samplelife Retirement Annuity", "contribution_type": "recurring", "contribution": "R 3 000.00", "escalation": "10%", "term": "Retirement age 65",
             "funds": [{"name": "Sample Balanced Fund", "allocation": "60", "asset_mgmt_fee": "0.85%"}, {"name": "Sample Growth Fund", "allocation": "40", "asset_mgmt_fee": "0.95%"}],
             "fee_lines": [{"label": "Net administration fee", "pct": "1.20%"}, {"label": "Ongoing advice fee", "pct": "0.575%"}, {"label": "Adviser remuneration account charge", "pct": "0.00%"}],
             "initial_fees": [{"label": "Initial commission", "value": "3.00%"}],
             "loyalty": [{"name": "Samplelife Loyalty Bonus", "trigger": "No premiums missed", "guaranteed": "discretionary", "pays": "At retirement, then each later year", "percentages": ["2.5%", "1.0%"],
                          "explanation": "The bonus is not added along the way: 2.5% is paid once at retirement if you never miss a premium, and a further 1.0% is paid each later year.",
                          "source_line": "paid at retirement if no premiums are missed"}],
             "performance_fees": [], "flexibility": [{"topic": "Pausing contributions", "text": "You can pause contributions without a penalty.", "quote_words": "Loyalty Bonus"}]},
            {"name": "Testco", "product_name": "Testco Retirement Annuity", "contribution_type": "recurring", "contribution": "R 3 000.00", "escalation": "10%", "term": "Retirement age 65",
             "funds": [{"name": "Test Cautious Fund", "allocation": "100", "asset_mgmt_fee": "0.60%"}],
             "fee_lines": [{"label": "Administration fee", "pct": "0.90%"}, {"label": "Ongoing advice fee", "pct": "0.575%"}],
             "initial_fees": [{"label": "Initial advice fee", "value": "R 0.00"}],
             "loyalty": [{"name": "Wealth Bonus", "trigger": "Staying until retirement", "guaranteed": "discretionary", "pays": "Once, at retirement", "percentages": ["2.0%"],
                          "explanation": "The Wealth Bonus is paid once, at retirement, and the quote says it is funded by a lower charge in the early years, so it is partly a refund of a cost already priced in.",
                          "source_line": "funded by a lower charge in the early years"}],
             "performance_fees": [{"fund": "Test Cautious Fund", "note": "20% of the return above its benchmark"}], "flexibility": []}],
        "fund_sheets": [
            {"provider": "Samplelife", "fund": "Sample Balanced Fund", "benchmark": "CPI plus 5%", "target": "CPI + 5% over rolling five years", "perf_1y": "8.2%", "perf_3y": "9.1%", "perf_5y": "10.3%",
             "as_at": "30/09/2026", "description": "A balanced fund that spreads your money across several asset types to beat inflation.", "risk_label": "Moderate"},
            {"provider": "Samplelife", "fund": "Sample Growth Fund", "benchmark": "ASISA Aggressive Allocation average", "target": "CPI + 6% over rolling seven years", "perf_1y": "11.4%", "perf_3y": "12.0%", "perf_5y": "13.5%",
             "as_at": "30/09/2026", "description": "A growth fund that puts most of your money in shares for higher long-term returns.", "risk_label": "Aggressive"},
            {"provider": "Testco", "fund": "Test Cautious Fund", "benchmark": "CPI plus 3%", "target": "CPI + 3% over rolling three years", "perf_1y": "6.1%", "perf_3y": "6.9%", "perf_5y": "7.4%",
             "as_at": "31/10/2026", "description": "A low-risk fund that keeps most of your money in bonds and cash.", "risk_label": "Cautious"}],
        "supplement_checks": {"Testco Booster Illustrator": [{"provider": "Testco", "field": "Wealth Bonus", "quote_value": "2.0%", "supplement_value": "3.50%", "supplement_date": "06/07/2026"}]},
        "extras": {"verdict": True, "tax_note": True, "flexibility": True, "example_fund_value": "R 100 000.00"},
        "meetings_held": ["29/10/2026", "02/11/2026"], "next_meeting": {"date": "12/11/2026", "time": "12pm"}, "plan_folder": FOLDER, "flags": ["The saved copy has no logo."], "sources": dict(SOURCES), "conflicts": []}


def bad(a, **path_value):
    """A copy of the answers with deep changes: bad(a, **{"providers.0.contribution": "R 1"}); DELETE removes a key."""
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


SIGNATURE = "<p>Kind regards,</p><p>Paul Kafentzis, FSP45946</p><p>Disclaimer and Confidentiality Notice: invented for the test.</p>"


def draft_json(a, body, subj, **v):
    content = "<html><body>" + body + v.get("signature", SIGNATURE) + "</body></html>"
    if "content" in v:
        content = v["content"](content)
    return json.dumps({"id": "AAMkINVENTED", "subject": v.get("subject", subj),
                       "toRecipients": [{"emailAddress": {"address": v.get("to", EMAIL), "name": "Pat"}}],
                       "ccRecipients": [{"emailAddress": {"address": v.get("cc", "admin@liferisk.co.za"), "name": "Sitamah Nathoo"}}],
                       "importance": v.get("importance", "high"), "body": {"contentType": "html", "content": content}})


def message_json(a, greeting="Good morning", **v):
    items = ["<li>The Samplelife quote (%s)</li>" % NAMES["quote_samplelife"][:-4], "<li>The Testco quote (%s)</li>" % NAMES["quote_testco"][:-4],
             "<li>The fund fact sheets (Sample Balanced Fund, Sample Growth Fund &amp; Test Cautious Fund)</li>", "<li>The supplementary document: Testco Booster Illustrator (%s)</li>" % NAMES["supplement_testco_booster_illustrator"][:-4]]
    html = ("<p>%s Sitamah,</p><p><strong>Action needed:</strong> I have compiled the draft investment comparison email to %s (RA: Samplelife vs Testco) and saved it in <strong>Drafts</strong> (To: %s, Cc: you).</p>"
            "<p>Please kindly attach the following to that draft:</p><ol>%s</ol><p>All of them are in Pat's folder: %s &gt; Comparative Quotes.</p>"
            "<p>Once attached, please email the client - Thank you!</p>") % (greeting, a["client_full_name"], a["client_email"], "".join(items), a["plan_folder"])
    if "html" in v:
        html = v["html"](html)
    return json.dumps({"id": "1700000000000", "body": {"contentType": "html", "content": html}})
