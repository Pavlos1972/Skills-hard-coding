"""INVENTED documents and answers for the life insurer comparison test (Pat Samplecase, the invented insurers Samplelife, Testco and Examplecover, invented notes, guides and quotes).
No real client, insurer document or guide, ever."""
import copy
import json
import os
import sys
from decimal import ROUND_HALF_UP, Decimal

SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
sys.path.insert(0, SCRIPTS)

OWNER = "Patricia Anne Samplecase"
EMAIL = "pat@example.invalid"
FOLDER = "Samplecase, Pat - (Risk comparison)"
DELETE = object()

# ---- the projection tables: Samplelife (rand figures only, one outlier year), Testco (rand figures AND printed percentages), Examplecover (rand figures only, 8 years)
SL_PREMS = ["1850.00", "1940.00", "2040.00", "2150.00", "2270.00", "3100.00", "3260.00", "3440.00", "3640.00", "3850.00"]
TC_PREMS = []
_p = Decimal("1420.00")
for _i in range(10):
    TC_PREMS.append(str(_p.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)))
    _p = _p * Decimal("1.1")
EC_PREMS = []
_p = Decimal("1610.00")
for _i in range(8):
    EC_PREMS.append(str(_p.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)))
    _p = _p * Decimal("1.075")


def money(s):
    d = Decimal(s)
    whole, frac = ("%.2f" % d).split(".")
    g = []
    while whole:
        g.insert(0, whole[-3:])
        whole = whole[:-3]
    return "R " + " ".join(g) + "." + frac


def _rows(prems, start_year=2027, start_age=46, pct=False):
    out = []
    for i, p in enumerate(prems):
        s = "Year %d %d age %d %s" % (i + 1, start_year + i, start_age + i, money(p))
        if pct and i:
            s += " %s%%" % "10.00"
        out.append(s)
    return out


SL_LINES = ["Samplelife Life Plan Schedule", "Policy number SL-5501234", "Policy schedule dated 14/08/2026", "Client: %s" % OWNER, "Commencement date 01/09/2020",
            "Total monthly premium R 1 850.00",
            "Premium pattern: Age Rated Premium Pattern - your premium is recalculated against your age at each yearly review",
            "Premium guaranteed for 12 months",
            "Life cover R 1 500 000.00 monthly cost R 900.00",
            "Terminal illness benefit R 1 500 000.00 paid early from the life cover",
            "Severe illness cover R 0.00 not selected",
            "Second life: Robin Samplecase life cover R 500 000.00 as a rider on the main policy",
            "Projected premiums"] + _rows(SL_PREMS)
TC_LINES = ["Testco Risk Cover Quote", "Quote number TC-7788-2026", "Quote dated 28/10/2026", "Client: %s" % OWNER, "Proposed commencement date 01/12/2026",
            "Total monthly premium R 1 420.00",
            "Yearly premium increase: 10.0% (fixed for the life of the policy)", "Yearly cover increase 5.0%",
            "Premium guaranteed for the life of the policy",
            "Life cover R 1 500 000.00 monthly cost R 700.00",
            "Terminal illness benefit R 1 500 000.00 included in the life cover",
            "Second life: Robin Samplecase independent life cover R 500 000.00",
            "Testco Wealth Bonus 15% discount on the premium for the first 24 months",
            "Projected premiums"] + _rows(TC_PREMS, pct=True)
EC_LINES = ["Examplecover Life Quote", "Quote number EC-0042", "Quote dated 30/10/2026", "Client: %s" % OWNER,
            "Total monthly premium R 1 610.00", "Yearly premium increase 7.5% compulsory",
            "Life cover R 1 500 000.00 monthly cost R 800.00", "Terminal illness benefit included",
            "Second life: no cover for Robin on this quote", "Projected premiums"] + _rows(EC_PREMS, start_year=2027)
EC_IMAGE_TEXT = "Funeral cover R 25 000.00"
NOTES = ["Follow-Up Appointment Summary Notes 02/10/2026", "Client: %s" % OWNER,
         "Pat wants life cover only for her family.", "Elected to remove disability from the proposed option due to budget constraints.", "Severe illness is not included.",
         "Income protection is not required.", "No debt cover is needed.", "No childcare or education benefits were asked for.",
         "Her husband Robin is the second life on the policy."]
FF = ["Fact Find Summary", "Client: %s (Pat)" % OWNER, "Email: %s" % EMAIL, "Risk profile: Moderate"]
OVERVIEW = ["WR Overview", "Client: %s" % OWNER, "Current insurer Samplelife premium R 1 850.00 a month"]
GUIDES = {
    "Samplelife": ["Samplelife Technical Guide", "Cover can be increased only with new medical underwriting.", "Claims are assessed against the policy wording."],
    "Testco": ["Testco Product Guide", "Testco offers a cover increase facility without medical underwriting on marriage or the birth of a child.",
               "Retrenchment protection pays the premium for up to six months after a retrenchment."],
    "Examplecover": ["Examplecover Technical Guide", "Cover increases require full underwriting."]}
NAMES = {"quote_testco_proposal": "Testco Quote - P Samplecase.pdf", "schedule_samplelife_schedule": "Samplelife Policy Schedule - P Samplecase.pdf", "quote_examplecover_quote": "Examplecover Quote - P Samplecase.pdf",
         "intake_notes_2026_10_02": "Follow-Up Appointment Summary Notes - 02.10.26.pdf", "fact_find_summary": "Fact Find Summary - 28.10.26 - (Pat Samplecase).pdf", "overview": "WR Overview - P Samplecase.pdf"}


def _pdf(path, pages, image_page=None):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate
    st = getSampleStyleSheet()["Normal"]
    story = []
    for i, lines in enumerate(pages):
        story += [Paragraph(l.replace("&", "&amp;"), st) for l in lines]
        if i < len(pages) - 1 or image_page:
            story.append(PageBreak())
    if image_page:
        from PIL import Image, ImageDraw
        from reportlab.platypus import Image as RLImage
        png = path + ".png"
        im = Image.new("RGB", (900, 200), "white")
        ImageDraw.Draw(im).text((20, 80), image_page, fill="black")
        im.save(png)
        story.append(RLImage(png, width=450, height=100))
    SimpleDocTemplate(path, pagesize=A4).build(story)


def make_docs(d, tc_premium=None):
    """{registry key: path}: the sides, the notes, the Fact Find Summary, the WR Overview, and the saved guide texts."""
    out = {}
    tcl = list(TC_LINES)
    if tc_premium:
        tcl = [l.replace("Total monthly premium R 1 420.00", "Total monthly premium " + tc_premium) for l in tcl]
    for key, lines, img in (("quote_testco_proposal", tcl, None), ("schedule_samplelife_schedule", SL_LINES, None), ("quote_examplecover_quote", EC_LINES, EC_IMAGE_TEXT),
                            ("intake_notes_2026_10_02", NOTES, None), ("fact_find_summary", FF, None), ("overview", OVERVIEW, None)):
        out[key] = os.path.join(d, NAMES[key])
        _pdf(out[key], [lines], image_page=img)
    for ins, lines in GUIDES.items():
        k = "guide_" + ins.lower() + "_guide"
        out[k] = os.path.join(d, "guide-%s.txt" % ins.lower())
        with open(out[k], "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
    return out


LABELS = {"Samplelife Schedule": ("schedule", "schedule_samplelife_schedule"), "Testco Proposal": ("quote", "quote_testco_proposal"), "Examplecover Quote": ("quote", "quote_examplecover_quote")}
INSURERS = [{"label": "Samplelife Schedule", "insurer": "Samplelife"}, {"label": "Testco Proposal", "insurer": "Testco"}, {"label": "Examplecover Quote", "insurer": "Examplecover"}]
GUIDE_LABELS = {"Samplelife": "Samplelife - Technical Guide", "Testco": "Testco - Product Guide", "Examplecover": "Examplecover - Technical Guide"}


def scope():
    return {"categories": {
        "life": {"status": "in", "source": "intake_notes_2026_10_02", "evidence": "Pat wants life cover only for her family."},
        "severe_illness": {"status": "out", "source": "intake_notes_2026_10_02", "evidence": "Severe illness is not included."},
        "disability": {"status": "out", "source": "intake_notes_2026_10_02", "evidence": "Elected to remove disability from the proposed option due to budget constraints."},
        "income_protection": {"status": "out", "source": "intake_notes_2026_10_02", "evidence": "Income protection is not required."},
        "debt_cover": {"status": "out", "source": "intake_notes_2026_10_02", "evidence": "No debt cover is needed."},
        "childcare": {"status": "out", "source": "intake_notes_2026_10_02", "evidence": "No childcare or education benefits were asked for."}},
        "second_life": {"present": True, "name": "Robin", "source": "intake_notes_2026_10_02", "evidence": "Her husband Robin is the second life on the policy."},
        "basis": "against-proposal", "basis_source": "Paul chose to compare the new proposal against the existing policy",
        "voice": "first_person", "sections": ["premium_snapshot", "cover_comparison", "escalation_table", "loyalty", "definitions", "verdict", "sources"]}


def _proj(prems, printed=False, n=None):
    rows = []
    for i, p in enumerate(prems[:n]):
        r = {"n": i + 1, "label": str(2027 + i), "age": 46 + i, "premium": money(p)}
        if printed and i:
            r["printed_pct"] = "10.00"
        rows.append(r)
    return rows


def answers():
    return {
        "client_full_name": "Pat Samplecase", "client_first_name": "Pat", "client_surname": "Samplecase", "client_email": EMAIL, "email_source": "fact_find_summary", "email_note": "",
        "plan_folder": FOLDER,
        "sides": [
            {"label": "Samplelife Schedule", "insurer": "Samplelife", "role": "existing", "product_name": "Samplelife Life Plan", "reference": "SL-5501234", "document_date": "14/08/2026", "start_date": "01/09/2020",
             "premium": {"monthly": "R 1 850.00", "evidence": "Total monthly premium R 1 850.00"},
             "escalation": {"type": "age_rated", "evidence": "Premium pattern: Age Rated Premium Pattern - your premium is recalculated against your age at each yearly review"},
             "guarantee": {"text": "12 months", "evidence": "Premium guaranteed for 12 months"},
             "covers": [{"category": "life", "label": "Life cover", "amount": "R 1 500 000.00", "monthly": "R 900.00", "evidence": "Life cover R 1 500 000.00 monthly cost R 900.00"},
                        {"category": "terminal_illness", "label": "Terminal illness benefit", "amount": "R 1 500 000.00", "evidence": "Terminal illness benefit R 1 500 000.00 paid early from the life cover"},
                        {"category": "life", "label": "Life cover", "life": "second", "amount": "R 500 000.00", "evidence": "Second life: Robin Samplecase life cover R 500 000.00 as a rider on the main policy"}],
             "projection": _proj(SL_PREMS), "loyalty": None,
             "second_life": {"status": "rider", "evidence": "Second life: Robin Samplecase life cover R 500 000.00 as a rider on the main policy"}},
            {"label": "Testco Proposal", "insurer": "Testco", "role": "proposal", "product_name": "Testco Risk Cover", "reference": "TC-7788-2026", "document_date": "28/10/2026", "start_date": "01/12/2026",
             "premium": {"monthly": "R 1 420.00", "evidence": "Total monthly premium R 1 420.00"},
             "escalation": {"type": "fixed", "rate": "10", "evidence": "Yearly premium increase: 10.0% (fixed for the life of the policy)"},
             "benefit_escalation": {"rate": "5", "evidence": "Yearly cover increase 5.0%"},
             "guarantee": {"text": "the life of the policy", "evidence": "Premium guaranteed for the life of the policy"},
             "covers": [{"category": "life", "label": "Life cover", "amount": "R 1 500 000.00", "monthly": "R 700.00", "evidence": "Life cover R 1 500 000.00 monthly cost R 700.00"},
                        {"category": "terminal_illness", "label": "Terminal illness benefit", "amount": "R 1 500 000.00", "evidence": "Terminal illness benefit R 1 500 000.00 included in the life cover"},
                        {"category": "life", "label": "Life cover", "life": "second", "amount": "R 500 000.00", "evidence": "Second life: Robin Samplecase independent life cover R 500 000.00"}],
             "projection": _proj(TC_PREMS, printed=True),
             "loyalty": {"name": "Testco Wealth Bonus", "amount_or_pct": "15%", "when": "Upfront, first 24 months", "evidence": "Testco Wealth Bonus 15% discount on the premium for the first 24 months"},
             "second_life": {"status": "independent", "evidence": "Second life: Robin Samplecase independent life cover R 500 000.00"}},
            {"label": "Examplecover Quote", "insurer": "Examplecover", "role": "other", "product_name": "Examplecover Life", "reference": "EC-0042", "document_date": "30/10/2026",
             "premium": {"monthly": "R 1 610.00", "evidence": "Total monthly premium R 1 610.00"},
             "escalation": {"type": "fixed", "rate": "7.5", "evidence": "Yearly premium increase 7.5% compulsory"},
             "guarantee": {"not_stated": True},
             "covers": [{"category": "life", "label": "Life cover", "amount": "R 1 500 000.00", "monthly": "R 800.00", "evidence": "Life cover R 1 500 000.00 monthly cost R 800.00"},
                        {"category": "life", "label": "Funeral cover", "amount": "R 25 000.00", "evidence": EC_IMAGE_TEXT, "image_read": True, "page": 2}],
             "projection": _proj(EC_PREMS), "loyalty": None, "second_life": {"status": "none"}}],
        "features": [
            {"side": "Testco Proposal", "category": "life", "text": "Your cover can grow without new medical tests when you marry or have a child.", "basis": "insurer_guide", "source": "guide_testco_product_guide",
             "evidence": "Testco offers a cover increase facility without medical underwriting on marriage or the birth of a child.", "badge": "wins",
             "exclusive": True, "exclusive_checks": [{"insurer": "Samplelife", "source": "guide_samplelife_technical_guide", "evidence": "Cover can be increased only with new medical underwriting."},
                                                     {"insurer": "Examplecover", "source": "guide_examplecover_technical_guide", "evidence": "Cover increases require full underwriting."}]},
            {"side": "Samplelife Schedule", "category": "life", "text": "Your current premium is recalculated against your age at every yearly review.", "basis": "client_document",
             "source": "schedule_samplelife_schedule", "evidence": "Age Rated Premium Pattern", "badge": "tradeoff"},
            {"side": "Examplecover Quote", "category": "life", "text": "Claims are usually assessed within a month.", "basis": "inference", "badge": None},
            {"side": "Testco Proposal", "category": "life", "text": "Retrenchment protection can pay your premium for a time.", "basis": "insurer_guide", "source": "guide_testco_product_guide",
             "evidence": "Retrenchment protection pays the premium for up to six months after a retrenchment.", "badge": None, "not_on_proposal": True,
             "conditions": "ask Testco to add it before the policy starts."}],
        "definitions": [{"side": "Samplelife Schedule", "category": "life", "set": "Death benefit", "note": "Pays on death or early on a terminal diagnosis.", "basis": "client_document",
                         "source": "schedule_samplelife_schedule", "evidence": "Terminal illness benefit R 1 500 000.00 paid early from the life cover"}],
        "banner": "Your premium would start at R 1 420.00 a month with Testco, against R 1 850.00 today, and Testco's yearly increase is fixed at 10%.",
        "opening": "I have put together a plain comparison of your cover with Samplelife against the Testco proposal and one more quote.",
        "verdict": [{"headline": "Testco is the lowest starting premium.", "detail": "R 1 420.00 a month against R 1 850.00 with Samplelife and R 1 610.00 with Examplecover."},
                    {"headline": "Testco's increase is fixed.", "detail": "Your premium rises by a set 10% a year, while Samplelife's follows your age."},
                    {"headline": "I recommend we go through the Testco proposal together.", "detail": "We can look at what the fixed increase means for you over ten years."}],
        "email": {"opening": "Thank you for trusting me with your cover, Pat. I have put the options side by side so we can decide together.",
                  "concern": "I know the cost of your current premium has been on your mind, and this comparison speaks to that.",
                  "bullets": ["Testco starts at R 1 420.00 a month, against R 1 850.00 with Samplelife.", "Testco's yearly increase is fixed at 10%.",
                              "Samplelife's increase follows your age, and one year stands out in its table.", "Testco can raise your cover without new medical tests."]},
        "flags": ["Examplecover's guarantee period is not on its quote: confirm it with Examplecover."]}


def bad(a, **path_value):
    """A copy with deep changes: bad(a, **{"sides.0.premium.monthly": "R 1"}); DELETE removes a key."""
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


def draft_json(a, body, subj, **v):
    content = "<html><body>" + body + v.get("extra", "") + "</body></html>"
    if "content" in v:
        content = v["content"](content)
    return json.dumps({"id": "AAMkINVENTED", "subject": v.get("subject", subj), "hasAttachments": v.get("has_att", False),
                       "toRecipients": [{"emailAddress": {"address": v.get("to", EMAIL), "name": "Pat"}}],
                       "ccRecipients": [{"emailAddress": {"address": v.get("cc", "admin@liferisk.co.za"), "name": "Sitamah Nathoo"}}],
                       "body": {"contentType": "html", "content": content}})


def message_json(a, name, greeting="Good morning", **v):
    html = ("<p>%s Sitamah,</p><p><strong>FYI:</strong> I have compiled the draft life insurance comparison email to %s (Samplelife vs Testco vs Examplecover; against the new proposal) and saved it in "
            "<strong>Drafts</strong> (To: %s, Cc: you).</p><p>The comparison letter is saved in %s &gt; Comparative Quotes as %s. Paul will attach it to that draft himself before it goes out.</p>"
            "<p>No action is needed from you now - Thank you!</p>") % (greeting, a["client_full_name"], a["client_email"], a["plan_folder"], name)
    if "html" in v:
        html = v["html"](html)
    return json.dumps({"id": "1700000000000", "body": {"contentType": "html", "content": html}})
