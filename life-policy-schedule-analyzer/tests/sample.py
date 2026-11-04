"""INVENTED documents and analysis for the life policy schedule analyzer test (Pat Samplecase, the invented insurers Samplelife and Testco, invented schedules, a proposed quote and its
payback document, a Fact Find Summary, meeting notes, saved product sources). No real client, insurer document or product source, ever."""
import copy
import os
import sys

SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
sys.path.insert(0, SCRIPTS)

OWNER = "Patricia Anne Samplecase"
FOLDER = "Samplecase, Pat - (Policy analysis)"
DELETE = object()

LIFE_LINES = ["Samplelife Life Plan Schedule", "Policy number SL-5501234", "Policy schedule dated 14/08/2026", "Life assured: %s" % OWNER, "Client age at commencement 46",
              "Commencement date 01/09/2026", "Policy status: In force", "Policy type: Whole of life cover", "Total monthly premium R 1 450.00",
              "Premium pattern: Age Rated Premium Pattern - your premium is recalculated against your age at each yearly review", "Premium guaranteed for 12 months",
              "Life cover R 1 500 000.00 monthly cost R 900.00",
              "Dread disease cover R 400 000.00 monthly cost R 450.00 accelerated: a claim reduces the life cover",
              "Dread disease paid in severity bands of 25% 50% 75% and 100% of the cover", "Survival period 14 days",
              "Second life: Robin Samplecase life cover R 500 000.00 monthly cost R 100.00 as a rider on the main policy",
              "Cession: this policy is ceded to Samplebank as security for a home loan", "Exclusions: suicide within 24 months of commencement", "Beneficiary: Robin Samplecase 100%"]
DIS_LINES = ["Samplelife Work Disability Schedule", "Policy number SL-5509876", "Policy schedule dated 14/08/2026", "Life assured: %s" % OWNER, "Commencement date 01/09/2026",
             "Policy status: In force", "Total monthly premium R 300.00", "Yearly premium increase 8.0% fixed by contract", "Premium guarantee not stated",
             "Permanent disability lump sum R 800 000.00 monthly cost R 300.00", "Cession: none noted", "Exclusions: disability from a pre-existing condition", "Beneficiary: %s" % OWNER]
DIS_IMAGE = "Waiting period 30 days"
PROPOSED = ["Testco Risk Cover Quote", "Quote number TC-7788-2026", "Quote dated 28/10/2026", "Quote valid until 28/11/2026", "Client: %s" % OWNER, "Total monthly premium R 1 900.00",
            "Life cover R 1 500 000.00 monthly cost R 800.00", "Dread disease cover R 400 000.00 monthly cost R 600.00 paid at 100% on any qualifying condition",
            "Permanent disability lump sum R 800 000.00 monthly cost R 500.00", "Income protection not selected"]
PAYBACK = ["Testco Payback Guide for quote TC-7788-2026", "Payback value today R 12 000.00", "Projected payback value at pay-out R 95 000.00 (estimate)",
           "Retirement component R 60 000.00 paid on 01/12/2046 as a lump sum", "Childcare component R 35 000.00 paid on 01/12/2036 in monthly instalments over 24 months",
           "Payback is guaranteed for 10 years", "The payback is lost if the policy is cancelled before the pay-out date"]
FF = ["Fact Find Summary", "Client: %s (Pat)" % OWNER, "Age 46 married to Robin Samplecase age 48", "Two dependent children aged 12 and 9", "Home loan balance about R 1 200 000.00", "Monthly income R 60 000.00"]
NOTES = ["Follow-Up Appointment Summary Notes 02/10/2026", "Client: %s" % OWNER, "Income protection was left out on purpose because of the budget."]
GUIDES = {
    "guide_samplelife_technical_guide": ["Samplelife Technical Guide", "A staged claim cannot pay more than the cover amount in total.", "Samplelife offers no needs-matched trauma benefit.",
                                         "Life cover on the Life Plan is the top tier of the Samplelife range.", "The Premier Dread Disease option pays 100% of the cover on any qualifying condition.",
                                         "The disability lump sum pays out once on permanent disability."],
    "source_samplelife_independent_review": ["Independent review of Samplelife products", "Samplelife does not sell a needs-matched trauma benefit.", "The Samplelife Life Plan is the insurer's top life cover tier.",
                                             "Samplelife's Premier dread disease option has no severity bands."],
    "guide_testco_product_guide": ["Testco Product Guide", "The Change Moment Pay-Out is described in the separate payback guide."]}
NAMES = {"schedule_samplelife_life_plan": "Samplelife Life Plan Schedule - P Samplecase.pdf", "schedule_samplelife_disability_plan": "Samplelife Disability Schedule - P Samplecase.pdf",
         "proposed_testco_proposal": "Testco Cover Proposal - P Samplecase.pdf", "payback_doc_testco_payback_guide": "Testco Payback Guide - TC-7788-2026.pdf",
         "fact_find_summary": "Fact Find Summary - 28.10.26 - (Pat Samplecase).pdf", "intake_notes_2026_10_02": "Follow-Up Appointment Summary Notes - 02.10.26.pdf"}
LABELS = {"Samplelife Life Plan": ("schedule", "schedule_samplelife_life_plan"), "Samplelife Disability Plan": ("schedule", "schedule_samplelife_disability_plan"),
          "Testco Proposal": ("proposed", "proposed_testco_proposal"), "Testco Payback Guide": ("payback_doc", "payback_doc_testco_payback_guide")}
INSURERS = [{"label": "Samplelife Life Plan", "insurer": "Samplelife"}, {"label": "Samplelife Disability Plan", "insurer": "Samplelife"}, {"label": "Testco Proposal", "insurer": "Testco"}]
SOURCE_LABELS = {"guide_samplelife_technical_guide": ("guide", "Samplelife - Technical Guide"), "source_samplelife_independent_review": ("source", "Samplelife - Independent Review"),
                 "guide_testco_product_guide": ("guide", "Testco - Product Guide")}


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


def make_docs(d):
    out = {}
    for key, lines, img in (("schedule_samplelife_life_plan", LIFE_LINES, None), ("schedule_samplelife_disability_plan", DIS_LINES, DIS_IMAGE), ("proposed_testco_proposal", PROPOSED, None),
                            ("payback_doc_testco_payback_guide", PAYBACK, None), ("fact_find_summary", FF, None), ("intake_notes_2026_10_02", NOTES, None)):
        out[key] = os.path.join(d, NAMES[key])
        _pdf(out[key], [lines], image_page=img)
    for key, lines in GUIDES.items():
        out[key] = os.path.join(d, key + ".txt")
        with open(out[key], "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
    return out


def stm(text, basis="absent", **kw):
    d = {"text": text, "basis": basis}
    d.update(kw)
    return d


def doc(text, evidence, **kw):
    return stm(text, "document", evidence=evidence, **kw)


def prod(text, *srcs):
    return stm(text, "product", sources=[{"source": s, "evidence": e} for s, e in srcs])


G, S = "guide_samplelife_technical_guide", "source_samplelife_independent_review"


def analysis():
    life = {
        "label": "Samplelife Life Plan", "insurer": "Samplelife", "found_in": "6. Policy Schedules", "product_name": "Samplelife Life Plan", "policy_number": "SL-5501234",
        "life_assured": OWNER, "start_date": "01/09/2026", "status": "In force",
        "life_cover_type": {"type": "whole_of_life", "basis": "document", "evidence": "Policy type: Whole of life cover"},
        "benefits": [
            {"category": "life", "label": "Life cover", "sum_assured": "R 1 500 000.00", "premium": "R 900.00", "evidence": "Life cover R 1 500 000.00 monthly cost R 900.00", "accelerated": "standalone",
             "bullets": [stm("Pays a lump sum to your family if you die.", "inference"), doc("Runs for your whole life, not to a set age.", "Policy type: Whole of life cover")]},
            {"category": "dread_disease", "label": "Dread disease cover", "sum_assured": "R 400 000.00", "premium": "R 450.00",
             "evidence": "Dread disease cover R 400 000.00 monthly cost R 450.00 accelerated: a claim reduces the life cover", "accelerated": "accelerated",
             "bullets": [doc("A claim reduces your life cover.", "Dread disease cover R 400 000.00 monthly cost R 450.00 accelerated: a claim reduces the life cover"),
                         doc("Pays by severity: 25, 50, 75 or 100%.", "Dread disease paid in severity bands of 25% 50% 75% and 100% of the cover")]},
            {"category": "life", "label": "Life cover", "life": "second", "sum_assured": "R 500 000.00", "premium": "R 100.00",
             "evidence": "Second life: Robin Samplecase life cover R 500 000.00 monthly cost R 100.00 as a rider on the main policy", "accelerated": "standalone", "self_explanatory": True}],
        "premium": {"monthly": "R 1 450.00", "evidence": "Total monthly premium R 1 450.00",
                    "pattern": {"type": "age_rated", "evidence": "Premium pattern: Age Rated Premium Pattern - your premium is recalculated against your age at each yearly review"},
                    "age_start": {"value": 46, "evidence": "Client age at commencement 46"},
                    "guarantee": {"text": "12 months", "evidence": "Premium guaranteed for 12 months"}},
        "exclusions": [doc("Suicide within 24 months of commencement.", "Exclusions: suicide within 24 months of commencement")], "riders": [],
        "beneficiaries": [doc("Robin Samplecase, 100%.", "Beneficiary: Robin Samplecase 100%")],
        "cession": {"status": "ceded", "to": "Samplebank", "text": "Ceded to Samplebank as security for a home loan", "basis": "document", "evidence": "Cession: this policy is ceded to Samplebank as security for a home loan"},
        "second_life": {"status": "rider", "text": "Robin's cover is a rider and depends on the main policy staying in force.", "basis": "document",
                        "evidence": "Second life: Robin Samplecase life cover R 500 000.00 monthly cost R 100.00 as a rider on the main policy"},
        "dread_disease": {
            "multiple_claims": stm("The schedule does not say whether more than one claim is possible."),
            "payout_structure": doc("Severity-tiered: pays 25, 50, 75 or 100% by severity, generally the lesser definition.", "Dread disease paid in severity bands of 25% 50% 75% and 100% of the cover"),
            "duration": stm("The schedule does not say how long the benefit lasts."),
            "exceed_100": prod("A staged claim cannot pay more than the cover in total.", (G, "A staged claim cannot pay more than the cover amount in total.")),
            "survival_period": doc("14 days.", "Survival period 14 days"),
            "children": stm("The schedule shows no cover for the children."),
            "trauma_equivalent": prod("Samplelife has no needs-matched trauma benefit.", (G, "Samplelife offers no needs-matched trauma benefit."), (S, "Samplelife does not sell a needs-matched trauma benefit.")),
            "severe_illness_scope": stm("Severe illness looks folded into the dread disease benefit.", "inference"),
            "accelerated_vs_standalone": doc("Accelerated: a dread disease claim reduces the life cover.", "Dread disease cover R 400 000.00 monthly cost R 450.00 accelerated: a claim reduces the life cover")},
        "vitality": {"applicable": False, "note": "Samplelife has no wellness-linked pricing mechanism."},
        "payback": {"applicable": False, "note": "This policy has no payback or cash back benefit."},
        "benchmark": [
            {"category": "life", "have": "Whole of life cover of R 1 500 000", "available": None, "outcome": "top_tier", "meaning": "Current cover already reflects Samplelife's top tier for life cover.",
             "sources": [{"source": G, "evidence": "Life cover on the Life Plan is the top tier of the Samplelife range."}, {"source": S, "evidence": "The Samplelife Life Plan is the insurer's top life cover tier."}]},
            {"category": "dread_disease", "have": "Severity-tiered dread disease of R 400 000", "available": "The Premier Dread Disease option pays 100% on any qualifying condition.", "outcome": "better_exists",
             "meaning": "A claim would pay the full amount on a broader range of conditions.",
             "sources": [{"source": G, "evidence": "The Premier Dread Disease option pays 100% of the cover on any qualifying condition."}, {"source": S, "evidence": "Samplelife's Premier dread disease option has no severity bands."}]}],
        "findings": [
            {"tier": "action", "headline": "Dread disease pays by severity bands", "detail": "A serious claim can pay far less than R 400 000. Samplelife's Premier option pays 100%: discuss moving to it.", "refs": ["benchmark:dread_disease"]},
            {"tier": "action", "headline": "The policy is ceded to Samplebank", "detail": "Samplebank has first claim on the proceeds. Worth confirming with the client and the bank that the cession still matches the loan.", "refs": ["cession"]},
            {"tier": "action", "headline": "Robin's cover is only a rider", "detail": "If the main policy lapses, Robin's cover disappears. Consider independent cover.", "refs": ["second_life"]},
            {"tier": "awareness", "headline": "The premium is age-rated", "detail": "The premium is recalculated against Pat's age each year and will keep climbing; the schedule gives no table."}],
        "verdict": "Solid whole of life cover, but the dread disease benefit pays by severity bands and the policy is ceded.",
        "honest_opinion": {"assessment": "Good life cover, weaker dread disease cover than the insurer offers today.", "good": ["The life cover is the insurer's top tier."],
                           "better": ["Move the dread disease cover to the Premier option.", "Arrange independent cover for Robin."]}}
    dis = {
        "label": "Samplelife Disability Plan", "insurer": "Samplelife", "found_in": "6. Policy Schedules", "product_name": "Samplelife Work Disability", "policy_number": "SL-5509876",
        "life_assured": OWNER, "start_date": "01/09/2026", "status": "In force", "life_cover_type": None,
        "benefits": [{"category": "disability", "label": "Permanent disability lump sum", "sum_assured": "R 800 000.00", "premium": "R 300.00", "evidence": "Permanent disability lump sum R 800 000.00 monthly cost R 300.00",
                      "accelerated": "not_applicable",
                      "details": [doc("Waiting period 30 days.", "Waiting period 30 days", image_read=True, page=2)],
                      "bullets": [prod("Pays a lump sum once, if you become permanently disabled.", (G, "The disability lump sum pays out once on permanent disability.")), stm("Cover ends after one payout.", "inference")]}],
        "premium": {"monthly": "R 300.00", "evidence": "Total monthly premium R 300.00", "pattern": {"type": "fixed", "rate": "8", "evidence": "Yearly premium increase 8.0% fixed by contract"}, "guarantee": {"not_stated": True}},
        "exclusions": [doc("Disability from a pre-existing condition.", "Exclusions: disability from a pre-existing condition")], "riders": [],
        "beneficiaries": [doc("Pat herself.", "Beneficiary: %s" % OWNER)],
        "cession": {"status": "not_ceded"}, "second_life": {"status": "none"}, "dread_disease": None,
        "vitality": {"applicable": False, "note": "Samplelife has no wellness-linked pricing mechanism."}, "payback": {"applicable": False, "note": "This policy has no payback or cash back benefit."},
        "benchmark": [{"category": "disability", "have": "Permanent disability lump sum of R 800 000", "available": None, "outcome": "unsure", "meaning": "Cannot tell whether a better current option exists."}],
        "findings": [{"tier": "action", "headline": "The premium guarantee period is not stated", "detail": "Ask Samplelife how long the premium is guaranteed.", "refs": []}],
        "verdict": "A simple disability lump sum with a fixed yearly increase and no stated guarantee period.",
        "honest_opinion": {"assessment": "Adequate cover for what it is.", "good": ["The yearly increase is fixed."], "better": ["Confirm the guarantee period."]}}
    return {
        "client_full_name": "Pat Samplecase", "client_first_name": "Pat", "client_surname": "Samplecase", "plan_folder": FOLDER, "policies": [life, dis],
        "proposed_status": "present", "proposed_said": "",
        "proposed": {"label": "Testco Proposal", "insurer": "Testco", "abbrev": "TC", "versus": "Samplelife", "product_name": "Testco Risk Cover", "quote_number": "TC-7788-2026", "quote_date": "28/10/2026",
                     "valid_until": "28/11/2026", "premium": {"monthly": "R 1 900.00", "evidence": "Total monthly premium R 1 900.00"},
                     "categories": {"life": {"held": True, "amount": "R 1 500 000.00", "premium": "R 800.00", "evidence": "Life cover R 1 500 000.00 monthly cost R 800.00"},
                                    "disability": {"held": True, "amount": "R 800 000.00", "premium": "R 500.00", "evidence": "Permanent disability lump sum R 800 000.00 monthly cost R 500.00"},
                                    "dread_disease": {"held": True, "amount": "R 400 000.00", "premium": "R 600.00", "evidence": "Dread disease cover R 400 000.00 monthly cost R 600.00 paid at 100% on any qualifying condition"},
                                    "income_protection": {"held": False}},
                     "projection": None, "assumption": {"rate": "9", "text": "9% a year", "said": "Assume nine percent a year"},
                     "payback": {"present": True, "name": "Change Moment Pay-Out", "today_value": {"amount": "R 12 000.00", "evidence": "Payback value today R 12 000.00"},
                                 "projected_value": {"amount": "R 95 000.00", "evidence": "Projected payback value at pay-out R 95 000.00 (estimate)"},
                                 "components": [{"name": "Retirement", "amount": "R 60 000.00", "pay_out_date": "01/12/2046", "how_paid": "as a lump sum", "evidence": "Retirement component R 60 000.00 paid on 01/12/2046 as a lump sum"},
                                                {"name": "Childcare", "amount": "R 35 000.00", "pay_out_date": "01/12/2036", "how_paid": "in monthly instalments over 24 months",
                                                 "evidence": "Childcare component R 35 000.00 paid on 01/12/2036 in monthly instalments over 24 months"}],
                                 "guarantee": {"text": "10 years", "evidence": "Payback is guaranteed for 10 years"},
                                 "conditions": {"text": "Keep the cover in place: the payback is lost if the policy is cancelled.", "evidence": "The payback is lost if the policy is cancelled before the pay-out date"}}},
        "left_out": [{"category": "income_protection", "source": "intake_notes_2026_10_02", "evidence": "Income protection was left out on purpose because of the budget."}],
        "slides": {"by_insurer": {"Samplelife": {
            "how_it_works": ["Your life cover pays your family a lump sum and runs for your whole life.", "Your dread disease cover pays by how serious the illness is.", "Your premium rises as you get older."],
            "key_things": [{"text": "Your dread disease cover may pay less than you expect.", "policy": "Samplelife Life Plan", "n": 1}, {"text": "The policy is ceded to Samplebank, which has first claim on the proceeds.", "policy": "Samplelife Life Plan", "n": 2}],
            "shortfalls": [{"text": "You have two young children to protect.", "evidence": "Two dependent children aged 12 and 9"}]}},
            "report2": {"gains": ["Dread disease pays 100% on any qualifying condition.", "A payback is added to your cover."], "know": ["The monthly premium is higher.", "Keep the cover in place to keep the payback."],
                        "detail": ["Life, disability and dread disease cover are all included."], "next_steps": [{"text": "Go through the proposal together", "timing": "this week"}, {"text": "Decide before the quote expires", "timing": "by 28/11/2026"}],
                        "payback_current": {"present": False}}},
        "flags": ["Confirm Samplebank's loan balance with the client."]}


def bad(a, **path_value):
    """A copy with deep changes: bad(a, **{"policies.0.premium.monthly": "R 1"}); DELETE removes a key."""
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
