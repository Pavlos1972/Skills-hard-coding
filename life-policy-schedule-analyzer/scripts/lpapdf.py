#!/usr/bin/env python3
"""Draws the two documents from the confirmed analysis (reportlab) and checks the finished PDFs by reading them back:
  1. the INTERNAL report, one per policy (A4, the 17 fixed sections, 'INTERNAL - NOT FOR CLIENT DISTRIBUTION' on every page);
  2. the CLIENT slides, one deck per current insurer (Report 1, six slides) and, only when a proposed quote exists, Report 2 (seven slides): 1280x720 pages.
Nothing here is typed by the chat and nothing here sends anything. A slide whose text does not fit stops the build (never clipped silently)."""
import os
import re
from decimal import Decimal
from xml.sax.saxutils import escape

import lpa as c
import wrlib as w

NAVY, NAVY_L, GOLD, GOLD_L = "#1F3A5F", "#EAF1F8", "#B08D57", "#F3ECE0"
GREEN, GREEN_L, AMBER, AMBER_L, RED, RED_L = "#2E7D32", "#E8F5E9", "#E65100", "#FFF3E0", "#B0271A", "#FDECEA"
TEXT, MUTED, BORDER = "#2C2C2C", "#666666", "#E0DDD8"
SW, SH = 1280, 720


class SlideOverflow(ValueError):
    pass


def E(s):
    return escape(str(s))


# ------------------------------------------------------------------ the internal report
def tag(st):
    wd = c.wording()["tags"]
    k = st.get("_kind") or st.get("basis")
    return {"document": wd["document"], "product_verified": wd["product_verified"], "product_single": wd["product_single"], "inference": wd["inference"], "absent": wd["absent"]}.get(k, "")


def build_internal(a, p, docs, ev, today, path):
    from reportlab.lib.colors import HexColor, white
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import HRFlowable, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    wd, st_ = c.wording(), c.settings()
    label = st_["internal_label"]
    C = HexColor
    base = ParagraphStyle("b", fontName="Helvetica", fontSize=9, leading=12, textColor=C(TEXT))
    small = ParagraphStyle("s", parent=base, fontSize=7.5, leading=9.5, textColor=C(MUTED))
    h2 = ParagraphStyle("h2", parent=base, fontName="Helvetica-Bold", fontSize=13, leading=16, textColor=C(NAVY), spaceBefore=10, spaceAfter=2)
    h3 = ParagraphStyle("h3", parent=base, fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=C(NAVY), spaceBefore=6, spaceAfter=2)
    title = ParagraphStyle("t", parent=base, fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=C(NAVY))
    lab = ParagraphStyle("l", parent=base, fontName="Helvetica-Bold", fontSize=9, textColor=C(RED))
    bul = ParagraphStyle("bu", parent=base, leftIndent=10, bulletIndent=0)
    act = ParagraphStyle("a", parent=base, textColor=C(RED))
    awr = ParagraphStyle("w", parent=base, textColor=C(AMBER))
    W = A4[0] - 36 * mm

    def para(t, s=base):
        return Paragraph(t, s)

    def stmt(st, extra=""):
        return "%s %s<font size=7 color='%s'>(%s)</font>" % (E(st["text"]), extra, MUTED, E(tag(st)))

    def kv(rows, widths=(48 * mm, None)):
        data = [[para("<b>%s</b>" % E(k)), para(v) if isinstance(v, str) else v] for k, v in rows]
        t = Table(data, colWidths=[widths[0], W - widths[0]])
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, -1), C(NAVY_L)), ("GRID", (0, 0), (-1, -1), 0.5, C(BORDER)), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                               ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
        return t

    def grid(head, rows, widths, repeat=True):
        data = [[para("<font color='white'><b>%s</b></font>" % E(h)) for h in head]] + [[para(x) if isinstance(x, str) else x for x in r] for r in rows]
        t = Table(data, colWidths=widths, repeatRows=1 if repeat else 0)
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), C(NAVY)), ("GRID", (0, 0), (-1, -1), 0.5, C(BORDER)), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                               ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
        return t

    def box(content, bg, line):
        t = Table([[content]], colWidths=[W])
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), C(bg)), ("BOX", (0, 0), (-1, -1), 1.2, C(line)), ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                               ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
        return t

    def heading(key):
        return [para(E(wd["sections"][key]), h2), HRFlowable(width="100%", thickness=0.8, color=C(GOLD), spaceAfter=4)]

    key = p["_key"] if "_key" in p else c.policy_docs(docs)[p["label"]]
    d = docs["docs"][key]
    fn = c.finding_numbers(p)
    S = []
    # header
    S += [para(E(wd["report_title"]), title), HRFlowable(width="100%", thickness=2, color=C(GOLD), spaceBefore=2, spaceAfter=4), para(E(label), lab), Spacer(1, 4)]
    S.append(kv([("Client", E(a["client_full_name"])), ("Insurer and product", E("%s - %s%s" % (p["insurer"], p["product_name"], " (%s)" % p["tier"] if p.get("tier") else ""))),
                 ("Policy or quote number", E(p["policy_number"])), ("Date of analysis", c.today_str(today)),
                 ("Document", E("%s (found in: %s)" % (d["name"], p["found_in"])))]))
    S.append(Spacer(1, 6))
    S.append(box(para("<b>%s</b><br/>%s" % (E(wd["sections"]["verdict"]), E(p["verdict"])), base), GOLD_L, GOLD))
    S.append(Spacer(1, 6))
    # the benefit summary table
    S += [para("<b>%s</b>" % E("%s - %s - %s - %s" % (p["insurer"], p["product_name"], p["policy_number"], a["client_full_name"])), h3)]
    S.append(grid(["Benefit", "Sum Assured", "Premium"], [[E(x), E(y), E(z)] for x, y, z in c.benefit_rows(p)], [W * 0.5, W * 0.3, W * 0.2]))
    nh = c.not_held_types(p)
    S.append(para(E(wd["not_held_footer"].format(types=", ".join(nh)) if nh else wd["none_held_footer"]), small))
    # the findings, headline only
    S += heading("findings")
    if not fn:
        S.append(para("No obvious gaps, mistakes, or inferior benefits found on this schedule."))
    for n, tier, h, _d in fn:
        S.append(para("<b>%d. %s</b> - %s" % (n, E(h), E(wd["tier_action"] if tier == "action" else wd["tier_awareness"])), act if tier == "action" else awr))
    # 1 identity
    S += heading("identity")
    same_op = (p.get("owner") in (None, "") or p.get("owner") == p["life_assured"]) and (p.get("payer") in (None, "") or p.get("payer") == p["life_assured"])
    rows = [("Insurer", E(p["insurer"])), ("Product and tier", E("%s%s" % (p["product_name"], " - %s" % p["tier"] if p.get("tier") else ""))), ("Policy or quote number", E(p["policy_number"])),
            ("Life assured", E(p["life_assured"] + (" (also the policy owner and premium payer)" if same_op else "")))]
    if not same_op:
        rows += [("Policy owner", E(p.get("owner") or p["life_assured"])), ("Premium payer", E(p.get("payer") or p["life_assured"]))]
    rows += [("Start or quote date", E(p.get("start_date") or "not stated")), ("Status", E(p["status"])), ("Life cover type", stmt(p["life_cover_type"]) if p.get("life_cover_type") else E("No life cover benefit on this policy")),
             ("Cession", stmt(p["cession"], "(to %s)" % E(p["cession"]["to"]) if p["cession"]["status"] == "ceded" else ""))]
    S.append(kv(rows))
    # 2 benefits
    S += heading("benefits")
    for b in p["benefits"]:
        rows = [("Benefit", E(b["label"] + (" (second life)" if b.get("life") == "second" else ""))), ("Sum assured", E(c.money(b["sum_assured"]) + (" per month" if b.get("unit") == "monthly" else ""))),
                ("Premium", E(c.money(b["premium"]) if b.get("premium") else "not itemised")), ("Accelerated or standalone", E(b["accelerated"].replace("_", " ")))]
        if b.get("definition_set"):
            rows.append(("Definition set", E(b["definition_set"])))
        for r in b.get("details") or []:
            rows.append(("Detail", stmt(r)))
        blk = [kv(rows)]
        for r in b.get("bullets") or []:
            blk.append(Paragraph(stmt(r), bul, bulletText="•"))
        S.append(KeepTogether(blk))
        S.append(Spacer(1, 4))
        if b["category"] == "dread_disease" and p.get("dread_disease") and b.get("life", "main") == "main":
            S += [para("Dread Disease Deep-Dive", h3), kv([(c.TOPIC_NAMES[t], stmt(p["dread_disease"][t])) for t in c.DD_TOPICS])]
    # 3 second life
    S += heading("second_life")
    sl = p["second_life"]
    if sl["status"] == "none":
        S.append(para(E(wd["no_second_life"]) + "<font size=7 color='%s'> (%s)</font>" % (MUTED, E(tag(sl)))))
    else:
        S.append(kv([("Structure", E(sl["status"] == "rider" and "A rider on the main policy" or "Independent cover")), ("Detail", stmt(sl))]))
        sb = [b for b in p["benefits"] if b.get("life") == "second"]
        S.append(Spacer(1, 3))
        S.append(grid(["Benefit", "Sum Assured", "Premium"], [[E(b["label"]), E(c.money(b["sum_assured"])), E(c.money(b["premium"]) if b.get("premium") else "-")] for b in sb], [W * 0.5, W * 0.3, W * 0.2]))
    if sl.get("ff_note"):
        S.append(para(stmt(sl["ff_note"])))
    if sl["status"] == "none" and "fact_find_summary" not in docs["docs"]:
        pass
    # 4 premiums
    S += heading("premiums")
    pr = p["premium"]
    rows = [("Total monthly premium", E(c.money(pr["monthly"]))), ("Escalation", E("%s%s" % ("Fixed (set by the contract)" if pr["pattern"]["type"] == "fixed" else "Age-related (rises as the client ages)",
                                                                                      " at %s%% a year" % c.pct_digits(pr["pattern"]["rate"]) if pr["pattern"].get("rate") else "")))]
    g = pr["guarantee"]
    rows.append(("Premium guarantee", E(g["text"] if not g.get("not_stated") else "Not stated on the document: confirm with the insurer")))
    if pr.get("loading"):
        rows.append(("Loading", stmt(pr["loading"])))
    for r in pr.get("components") or []:
        rows.append(("Driver of the increase", stmt(r)))
    S.append(kv(rows))
    t = c.projection_table(p)
    S += [para(E(wd["projection_title"]), h3)]
    basis = {"printed": wd["projection_basis"]["printed"], "computed": wd["projection_basis"]["computed"].format(rate=w.fmt_pct(t["rate"]) if t["rate"] is not None else ""),
             "assumption": wd["projection_basis"]["assumption"].format(text=pr["assumption"]["text"] if pr.get("assumption") else ""), "none": wd["projection_basis"]["none"]}[t["mode"]]
    S.append(para(E(basis), small))
    prows = []
    for n in range(1, c.limits()["projection_years"] + 1):
        r = next((x for x in t["rows"] if x["n"] == n), None)
        if r is None:
            prows.append([E("Year %d" % n), "-", E(wd["na"]), E(wd["na"])])
        else:
            prows.append([E("Year %d" % n), E(str(r["age"]) if r["age"] is not None else "-"), E(c.money(r["premium"])), E("%s%%" % c.pct_str(r["pct"]) if r["pct"] is not None else "-")])
    S.append(grid(wd["projection_cols"], prows, [W * 0.15, W * 0.2, W * 0.35, W * 0.3]))
    # 5 and 6
    for key_, topics in (("vitality", c.VIT_TOPICS), ("payback", c.PB_TOPICS)):
        S += heading(key_)
        v = p[key_]
        if not v["applicable"]:
            S.append(para(E(wd["not_applicable"].format(note=v["note"]))))
        else:
            S.append(kv([(c.TOPIC_NAMES[t], stmt(v["rows"][t])) for t in topics]))
    # 7 benchmark
    S += heading("benchmark")
    for r in p["benchmark"]:
        outc = {"better_exists": "A materially better current option exists with the same insurer", "top_tier": "Current cover already reflects the insurer's top tier for this benefit", "unsure": "Unsure whether a better current option exists"}[r["outcome"]]
        k = r.get("_kind")
        rows = [("Benefit", E(c.CAT_NAMES[r["category"]])), ("What they have", E(r["have"])), ("Outcome", E(outc) + (" <font size=7 color='%s'>(%s)</font>" % (MUTED, E(tag(r))) if k else ""))]
        if r.get("available"):
            rows.append(("What is available now", E(r["available"])))
        rows.append(("What it would mean for a claim", E(r["meaning"])))
        S.append(KeepTogether([kv(rows), Spacer(1, 4)]))
    # 8, 9, 10
    for key_, name in (("exclusions", "exclusions"), ("riders", "riders"), ("beneficiaries", "beneficiaries")):
        S += heading(key_)
        if not p[name]:
            S.append(para("None noted on the document."))
        for r in p[name]:
            S.append(Paragraph(stmt(r), bul, bulletText="•"))
    # 11 red flags, full detail, same numbers
    S += heading("redflags")
    if not fn:
        S.append(para("No obvious gaps, mistakes, or inferior benefits found on this schedule."))
    for n, tier, h, det in fn:
        S.append(para("<b>%d. %s</b><br/>%s" % (n, E(h), E(det)), act if tier == "action" else awr))
        S.append(Spacer(1, 3))
    # opinion
    ho = p["honest_opinion"]
    S += heading("opinion")
    inner = "<b>Overall:</b> %s" % E(ho["assessment"])
    if ho["good"]:
        inner += "<br/><b>What is genuinely good:</b> " + E(" ".join(ho["good"]))
    if ho["better"]:
        inner += "<br/><b>What would make it materially better:</b> " + E(" ".join(ho["better"]))
    S.append(box(para(inner), NAVY_L, NAVY))
    # sources
    S += heading("sources")
    items = ["%s (found in: %s)" % (d["name"], p["found_in"])]
    items.append(("Fact Find Summary: %s" % docs["docs"]["fact_find_summary"]["name"]) if "fact_find_summary" in docs["docs"] else wd["sources_no_ff"])
    for k, dd in sorted(docs["docs"].items()):
        if dd["role"] in ("guide", "source") and w.norm(dd["label"]).startswith(w.norm(p["insurer"]) + " "):
            items.append("%s source: %s - %s (read %s)" % ("Insurer's own" if dd["role"] == "guide" else "Independent", dd["label"], dd["url"], dd["fetched_at"]))
    for it in items:
        S.append(Paragraph(E(it), bul, bulletText="•"))
    if "fact_find_summary" not in docs["docs"]:
        S.append(para(E(wd["no_fact_find"])))
    S.append(Spacer(1, 4))
    S.append(para(E(wd["sources_closing"]), small))

    def footer(cv, doc):
        cv.saveState()
        cv.setFont("Helvetica", 7.5)
        cv.setFillColor(C(MUTED))
        cv.drawString(18 * mm, 10 * mm, "%s - %s - %s" % (wd["report_title"], a["client_full_name"], p["label"]))
        cv.drawRightString(A4[0] - 18 * mm, 10 * mm, "Page %d" % doc.page)
        cv.setFillColor(C(RED))
        cv.setFont("Helvetica-Bold", 7.5)
        cv.drawCentredString(A4[0] / 2, 14.5 * mm, label)
        cv.restoreState()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=20 * mm, title="%s - %s" % (wd["report_title"], a["client_full_name"]))
    doc.build(S, onFirstPage=footer, onLaterPages=footer)


# ------------------------------------------------------------------ the client slides
def build_slides(a, kind, insurer, docs, ev, today, path):
    from reportlab.lib.colors import HexColor, white
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.pdfgen import canvas
    from reportlab.platypus import Paragraph, Table, TableStyle
    wd = c.wording()
    C = HexColor
    pols = [p for p in a["policies"] if p["insurer"] == insurer]
    left_out = {x["category"] for x in a["left_out"]}
    cv = canvas.Canvas(path, pagesize=(SW, SH))
    cv.setTitle("%s - %s" % (a["client_full_name"], insurer))
    slides = []

    def style(size, bold=False, color=TEXT, lead=None):
        return ParagraphStyle("x%d%s" % (size, bold), fontName="Helvetica-Bold" if bold else "Helvetica", fontSize=size, leading=lead or size * 1.3, textColor=C(color))

    def frame(title, n, total):
        cv.setFillColor(C(NAVY))
        cv.rect(0, SH - 90, SW, 90, fill=1, stroke=0)
        cv.setFillColor(C(GOLD))
        cv.rect(0, SH - 96, SW, 6, fill=1, stroke=0)
        cv.setFillColor(white)
        cv.setFont("Helvetica-Bold", 34)
        cv.drawString(50, SH - 60, title)
        cv.setFillColor(C(MUTED))
        cv.setFont("Helvetica", 14)
        cv.drawString(50, 24, "%s - %s" % (a["client_full_name"], c.today_str(today)))
        cv.drawRightString(SW - 50, 24, "%d / %d" % (n, total))

    def paras(texts, x, ytop, width, avail, sizes=(26, 24, 22, 20, 18, 16), bullet=True, color=TEXT):
        for sz in sizes:
            ps = [Paragraph(("• " if bullet else "") + E(t), style(sz, color=color)) for t in texts]
            hs = [pp.wrap(width, 10000)[1] + sz * 0.5 for pp in ps]
            if sum(hs) <= avail:
                y = ytop
                for pp, h in zip(ps, hs):
                    pp.wrap(width, 10000)
                    pp.drawOn(cv, x, y - h + sz * 0.5)
                    y -= h
                return
        raise SlideOverflow("text does not fit on the slide: %s" % texts[0][:60])

    def table(data, widths, x, ytop, avail, size=18, head=True, shade=None):
        rows = [[Paragraph(E(v), style(size, bold=(head and i == 0), color="#FFFFFF" if (head and i == 0) else TEXT)) if isinstance(v, str) else v for v in r] for i, r in enumerate(data)]
        t = Table(rows, colWidths=widths)
        sty = [("GRID", (0, 0), (-1, -1), 0.6, C(BORDER)), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]
        if head:
            sty.append(("BACKGROUND", (0, 0), (-1, 0), C(NAVY)))
        for (r, col, bg) in shade or []:
            sty.append(("BACKGROUND", (col, r), (col, r), C(bg)))
        t.setStyle(TableStyle(sty))
        tw, th = t.wrapOn(cv, sum(widths), 10000)
        if th > avail:
            raise SlideOverflow("a table does not fit on the slide (%d > %d)" % (th, avail))
        t.drawOn(cv, x, ytop - th)
        return th

    def tile(x, y, w_, h_, head, big, small_, bg, line):
        cv.setFillColor(C(bg))
        cv.setStrokeColor(C(line))
        cv.roundRect(x, y, w_, h_, 12, fill=1, stroke=1)
        cv.setFillColor(C(NAVY))
        cv.setFont("Helvetica-Bold", 22)
        cv.drawString(x + 20, y + h_ - 36, head)
        ph2 = 0
        if small_:
            p2 = Paragraph(E(small_), style(16, color=MUTED))
            ph2 = p2.wrap(w_ - 40, 10000)[1]
            p2.drawOn(cv, x + 20, y + 12)
        room = h_ - 48 - 12 - ph2 - 8
        for sz in (30, 26, 22, 18, 16):
            p_ = Paragraph(E(big), style(sz, bold=True, color=NAVY))
            ph = p_.wrap(w_ - 40, 10000)[1]
            if ph <= room:
                p_.drawOn(cv, x + 20, y + h_ - 48 - ph)
                return
        raise SlideOverflow("a tile does not fit: %s" % big[:40])

    def tbl_years(rows_by_label, labels):
        """A 10-year table: Year | Age | one column per label; est. when computed."""
        head = ["Year", "Age"] + labels
        data = [head]
        for n in range(1, c.limits()["projection_years"] + 1):
            r = [str(n), "-"]
            for lb in labels:
                cell = rows_by_label[lb].get(n)
                r.append(cell if cell else wd["na"])
            data.append(r)
        return data

    contents = []
    if kind == "report1":
        # title
        contents.append(("title", wd["slide_titles"]["title1"].format(insurer=insurer)))
        contents += [("glance", None), ("how", None), ("cost", None), ("key", None), ("short", None)]
    else:
        pd = a["proposed"]
        contents.append(("title", wd["slide_titles"]["title2"].format(current=insurer, proposed=pd["insurer"])))
        contents += [("side", None), ("gains", None), ("detail", None), ("costcmp", None), ("paybacks", None), ("next", None)]
    total = len(contents)
    si = a["slides"]["by_insurer"].get(insurer) if kind == "report1" else None
    r2 = a["slides"]["report2"] if kind == "report2" else None
    for idx, (sid, val) in enumerate(contents, 1):
        cv.setFillColor(C("#FFFFFF"))
        cv.rect(0, 0, SW, SH, fill=1, stroke=0)
        title = val if sid == "title" else wd["slide_titles"][sid]
        frame(title if sid != "title" else wd["report_title"].replace(" (Internal)", ""), idx, total)
        top = SH - 130
        if sid == "title":
            cv.setFillColor(C(NAVY))
            cv.setFont("Helvetica-Bold", 44)
            for line_i, line in enumerate(_wrap_text(val, 34)):
                cv.drawString(60, top - 120 - line_i * 56, line)
            cv.setFillColor(C(MUTED))
            cv.setFont("Helvetica", 24)
            cv.drawString(60, top - 330, "Prepared for %s" % a["client_full_name"])
            cv.drawString(60, top - 366, c.today_str(today))
        elif sid == "glance":
            xs, ys = [50, 650], [top - 230, top - 460]
            cats = list(c.FOUR)
            for i, cat in enumerate(cats):
                ent = c.category_entries(pols, cat)
                x, y = xs[i % 2], ys[i // 2]
                if ent:
                    big = amount_text(ent)
                    sm = ", ".join("%s%s" % (b["label"], " (second life)" if b.get("life") == "second" else "") for _p, b in ent)
                    prem = [b for _p, b in ent if b.get("premium")]
                    if prem:
                        sm += " - premium " + " + ".join(c.money(b["premium"]) for b in prem)
                    tile(x, y, 580, 210, wd["slide_categories"][cat], big, sm, GREEN_L, GREEN)
                else:
                    tile(x, y, 580, 210, wd["slide_categories"][cat], wd["slide_not_held_choice"] if cat in left_out else wd["slide_not_held"], "", AMBER_L, AMBER)
            others = [b for p_ in pols for b in p_["benefits"] if b["category"] == "other"]
            cv.setFillColor(C(NAVY))
            cv.setFont("Helvetica-Bold", 24)
            comb = "%s: %s" % (wd["slide_combined"], c.money(c.combined_premium(pols))) if len(pols) > 1 else "Monthly premium: %s" % c.money(c.combined_premium(pols))
            cv.drawString(50, 62, comb + ("   Also: " + ", ".join("%s %s" % (b["label"], c.money(b["sum_assured"])) for b in others) if others else ""))
        elif sid == "how":
            paras(si["how_it_works"], 60, top, 1160, 520)
        elif sid == "cost":
            labels = [p_["label"] for p_ in pols]
            cells, notes = {}, []
            for p_ in pols:
                t = c.projection_table(p_)
                cells[p_["label"]] = {r["n"]: c.money(r["premium"]) + (" (est.)" if t["mode"] in ("computed", "assumption") else "") for r in t["rows"]}
                if t["mode"] in ("computed", "assumption"):
                    notes.append(wd["slide_estimate_note"].format(basis=("computed from the stated yearly increase of %s%%." % w.fmt_pct(t["rate"])) if t["mode"] == "computed" else "computed from an assumption we agreed."))
                elif t["mode"] == "none":
                    notes.append("No projection is available for %s." % p_["label"])
            data = tbl_years(cells, labels)
            for r_, rowv in enumerate(data[1:], 1):
                age = next((x["age"] for p_ in pols for x in c.projection_table(p_)["rows"] if x["n"] == r_ and x["age"] is not None), None)
                rowv[1] = str(age) if age is not None else "-"
            widths = [90, 90] + [(1180 - 180) // max(1, len(labels))] * len(labels)
            th = table(data, widths, 50, top, 470, size=16 if len(labels) > 2 else 18)
            if notes:
                paras(sorted(set(notes)), 50, top - th - 10, 1180, 60, sizes=(16, 14), bullet=False, color=MUTED)
        elif sid == "key":
            items = [k_["text"] for k_ in si["key_things"]] or ["Nothing urgent to sort out right now."]
            paras(items, 60, top, 1160, 520)
        elif sid == "short":
            if "fact_find_summary" not in docs["docs"]:
                paras([wd["no_fact_find"]], 60, top, 1160, 520, bullet=False)
            else:
                paras([s["text"] for s in si["shortfalls"]] or ["Your cover meets the needs we recorded."], 60, top, 1160, 520)
        elif sid == "side":
            cur, pr = [p_ for p_ in a["policies"] if p_["insurer"] == pd["versus"]], a["proposed"]
            data = [["", "Today (%s)" % pd["versus"], "Proposed (%s)" % pd["insurer"]]]
            shade = []
            for r_, cat in enumerate(c.FOUR, 1):
                ent = c.category_entries(cur, cat)
                today_v = amount_text(ent) if ent else (wd["slide_not_held_choice"] if cat in left_out else wd["slide_not_held"])
                pv = pr["categories"][cat]
                prop_v = c.money(pv["amount"]) if pv["held"] else (wd["slide_not_held_choice"] if cat in left_out else wd["slide_not_held"])
                data.append([wd["slide_categories"][cat], today_v, prop_v])
                if not ent:
                    shade.append((r_, 1, AMBER_L))
                if not pv["held"]:
                    shade.append((r_, 2, AMBER_L))
            pb = pr["payback"]
            pcur = r2["payback_current"]
            data.append([wd["slide_payback_row"], pcur["name"] if pcur["present"] else wd["slide_no_payback_current"],
                         ("%s: %s today, %s projected (estimate)" % (pb["name"], c.money(pb["today_value"]["amount"]), c.money(pb["projected_value"]["amount"]))) if pb["present"] else wd["slide_no_payback_proposed"]])
            data.append(["Monthly cost", c.money(c.combined_premium(cur)), c.money(pr["premium"]["monthly"])])
            table(data, [260, 460, 460], 50, top, 520, size=20, shade=shade)
        elif sid == "gains":
            paras(["What you gain"], 60, top, 560, 70, sizes=(28,), bullet=False, color=NAVY)
            paras(r2["gains"], 60, top - 80, 560, 430, sizes=(22, 20, 18, 16))
            paras(["What to know"], 660, top, 560, 70, sizes=(28,), bullet=False, color=NAVY)
            paras(r2["know"], 660, top - 80, 560, 430, sizes=(22, 20, 18, 16))
        elif sid == "detail":
            pr = a["proposed"]
            lines = ["%s: %s a month (%s, quote %s)" % (pr["product_name"], c.money(pr["premium"]["monthly"]), pr["insurer"], pr["quote_number"])]
            lines += ["%s: %s" % (wd["slide_categories"][cat], c.money(pr["categories"][cat]["amount"])) for cat in c.FOUR if pr["categories"][cat]["held"]]
            paras(lines + r2["detail"], 60, top, 1160, 520, sizes=(24, 22, 20, 18, 16))
        elif sid == "costcmp":
            cur = [p_ for p_ in a["policies"] if p_["insurer"] == pd["versus"]]
            cells, notes = {"Today (%s)" % pd["versus"]: {}, "Proposed (%s)" % pd["insurer"]: {}}, []
            tabs = [c.projection_table(p_) for p_ in cur]
            if all(t["mode"] != "none" for t in tabs):
                for n in range(1, c.limits()["projection_years"] + 1):
                    tot = sum((next(x for x in t["rows"] if x["n"] == n)["premium"] for t in tabs if any(x["n"] == n for x in t["rows"])), Decimal("0.00"))
                    if all(any(x["n"] == n for x in t["rows"]) for t in tabs):
                        cells["Today (%s)" % pd["versus"]][n] = c.money(tot) + (" (est.)" if any(t["mode"] in ("computed", "assumption") for t in tabs) else "")
                if any(t["mode"] in ("computed", "assumption") for t in tabs):
                    notes.append(wd["slide_estimate_note"].format(basis="the current premiums are computed from the stated yearly increase."))
            else:
                notes.append("No projection is available for the current policies.")
            fake = {"premium": {"monthly": pd["premium"]["monthly"], "pattern": {"type": "age_rated"}, "projection": pd.get("projection"), "assumption": pd.get("assumption"), "age_start": None}}
            pt = c.projection_table(fake)
            for r_ in pt["rows"]:
                cells["Proposed (%s)" % pd["insurer"]][r_["n"]] = c.money(r_["premium"]) + (" (est.)" if pt["mode"] == "assumption" else "")
            if pt["mode"] == "assumption":
                notes.append(wd["slide_estimate_note"].format(basis="the proposed premium is computed from an assumption we agreed."))
            if pt["mode"] == "none":
                notes.append("The proposed quote gives no projection table.")
            labels = list(cells)
            th = table(tbl_years(cells, labels), [120, 80, 490, 490], 50, top, 470, size=17)
            if notes:
                paras(sorted(set(notes)), 50, top - th - 10, 1180, 60, sizes=(16, 14), bullet=False, color=MUTED)
        elif sid == "paybacks":
            pb, pcur = a["proposed"]["payback"], r2["payback_current"]
            paras(["Today: " + (pcur["name"] if pcur["present"] else wd["slide_no_payback_current"])], 60, top, 560, 70, sizes=(26,), bullet=False, color=NAVY)
            paras([pcur["text"]] if pcur["present"] else ["No cash back is paid on the current policy."], 60, top - 80, 560, 420, sizes=(22, 20, 18, 16))
            paras(["Proposed: " + (pb["name"] if pb["present"] else wd["slide_no_payback_proposed"])], 660, top, 560, 70, sizes=(26,), bullet=False, color=NAVY)
            if pb["present"]:
                lines = ["Value today: %s" % c.money(pb["today_value"]["amount"]), "Projected at pay-out: %s (estimate, not guaranteed)" % c.money(pb["projected_value"]["amount"])]
                lines += ["%s: %s%s, %s" % (x["name"], c.money(x["amount"]), " on %s" % x["pay_out_date"] if x.get("pay_out_date") else "", x["how_paid"]) for x in pb["components"]]
                lines += ["Guarantee: %s" % pb["guarantee"]["text"] if pb["guarantee"].get("text") else "Guarantee: see the payback document", pb["conditions"]["text"]]
                paras(lines, 660, top - 80, 560, 420, sizes=(20, 18, 16, 14))
            else:
                paras(["The proposed quote has no payback."], 660, top - 80, 560, 420, sizes=(22,))
        elif sid == "next":
            items = ["%s - %s" % (x["text"], x["timing"]) for x in r2["next_steps"]]
            vu = a["proposed"].get("valid_until")
            if vu:
                items.append(wd["slide_valid_until"].format(date=vu))
            paras(items, 60, top, 1160, 520)
        cv.showPage()
    cv.save()
    return total


def amount_text(ent):
    """The sum assured of a category across policies: the main life's amounts added with +, the second life's shown separately (never added to the main life's)."""
    main = [b for _p, b in ent if b.get("life", "main") == "main"]
    sec = [b for _p, b in ent if b.get("life") == "second"]
    s = " + ".join("%s%s" % (c.money(b["sum_assured"]), " a month" if b.get("unit") == "monthly" else "") for b in main)
    if sec:
        s += (" " if s else "") + "(second life: %s)" % " + ".join(c.money(b["sum_assured"]) for b in sec)
    return s


def _wrap_text(text, width):
    words_, lines, cur = text.split(), [], ""
    for wd_ in words_:
        if len(cur) + len(wd_) + 1 > width and cur:
            lines.append(cur)
            cur = wd_
        else:
            cur = (cur + " " + wd_).strip()
    return lines + ([cur] if cur else [])


# ------------------------------------------------------------------ read the finished PDFs back
def read_pdf(path):
    import pdfplumber
    pages = []
    with pdfplumber.open(path) as pdf:
        for pg in pdf.pages:
            txt = pg.extract_text() or ""
            out_of = [ch for ch in pg.chars if ch["x0"] < -1 or ch["x1"] > pg.width + 1 or ch["top"] < -1 or ch["bottom"] > pg.height + 1]
            pages.append({"text": txt, "w": float(pg.width), "h": float(pg.height), "outside": len(out_of)})
    return pages


def flat(pages):
    return "\n".join(p["text"] for p in pages)


def internal_problems(path, a, p, docs, today):
    R = []
    pages = read_pdf(path)
    txt = flat(pages)
    ntxt = w.norm(txt)
    wd, label = c.wording(), c.settings()["internal_label"]

    def add(ok, short):
        R.append((bool(ok), short))
    add(all(abs(pg["w"] - 595.3) < 2 and abs(pg["h"] - 841.9) < 2 for pg in pages), "The report is A4 (%d page(s))" % len(pages))
    add(all(label in pg["text"] for pg in pages), "'%s' is on every page" % label)
    add(wd["report_title"] in pages[0]["text"] and a["client_full_name"] in pages[0]["text"], "The header names the report and the client")
    heads = [wd["sections"][k] for k in ("verdict", "findings", "identity", "benefits", "second_life", "premiums", "vitality", "payback", "benchmark", "exclusions", "riders", "beneficiaries", "redflags", "opinion", "sources")]
    pos, last, ok = [], -1, True
    for h in heads:
        i = txt.find(h, last + 1)
        if i < 0:
            ok = False
            pos.append(h)
        else:
            last = i
    add(ok, "The sections are all there in the fixed order (Verdict, Benefit Summary, Findings, 1 to 11, Honest Opinion, Sources)" if ok else "Sections missing or out of order near: %s" % pos[0])
    add(p["verdict"].split()[0] in txt and w.norm(p["verdict"]) in ntxt, "The Verdict is the first box and carries the confirmed text")
    miss = [x for x, _y, _z in c.benefit_rows(p) if w.norm(x) not in ntxt]
    add(not miss and all(w.norm(c.money(b["sum_assured"])) in ntxt for b in p["benefits"]), "Every benefit and its sum assured is in the report")
    fn = c.finding_numbers(p)
    bad = [n for n, _t, h, _d in fn if len(re.findall(r"%d\. %s" % (n, re.escape(h.split()[0])), txt)) < 2]
    add(not bad, "Every numbered finding is in the top list AND in section 11 with the same number (%d finding(s))" % len(fn) if not bad else "Finding number(s) not in both places: %s" % bad)
    t = c.projection_table(p)
    add(txt.count("Year ") >= c.limits()["projection_years"] and (t["mode"] != "none" or wd["na"] in txt), "The 10-year premium table has its ten rows (%s)" % {"printed": "the insurer's own table", "computed": "illustrative, computed from the stated yearly increase",
                                                                                                                                       "assumption": "illustrative, from Paul's assumption", "none": "'not provided': no number invented"}[t["mode"]])
    add(not c.PLACEHOLDER.search(txt) and not c.LEFTOVER.search(txt), "No placeholder text in the report")
    add(sum(pg["outside"] for pg in pages) == 0, "All text is inside the page edges")
    return R


def slides_problems(path, a, kind, insurer, docs, today):
    R = []
    pages = read_pdf(path)
    txt = flat(pages)
    wd = c.wording()

    def add(ok, short):
        R.append((bool(ok), short))
    exp = 6 if kind == "report1" else 7
    add(len(pages) == exp and all(abs(pg["w"] - SW) < 2 and abs(pg["h"] - SH) < 2 for pg in pages), "%d slides, each 1280x720" % len(pages))
    bw = c.banned_slide_words(txt)
    add(not bw, "No INTERNAL wording, Honest Opinion, benchmark or other internal jargon on any slide" if not bw else "Words that must not be on a client slide: %s" % ", ".join(bw))
    add(sum(pg["outside"] for pg in pages) == 0, "All slide text is inside the slide edges (nothing clipped)")
    add(not c.PLACEHOLDER.search(txt), "No placeholder text on the slides")
    left_out = {x["category"] for x in a["left_out"]}
    if kind == "report1":
        pols = [p for p in a["policies"] if p["insurer"] == insurer]
        glance = pages[1]["text"]
        okc = all(wd["slide_categories"][cat] in glance for cat in c.FOUR)
        nh = [cat for cat in c.FOUR if not c.category_entries(pols, cat)]
        okn = all((wd["slide_not_held_choice"] if cat in left_out else wd["slide_not_held"]) in glance for cat in nh)
        add(okc and okn, "All four categories are on the at-a-glance slide; the ones not held read 'Not held'%s" % (" (your choice) where the client's notes say so" if left_out else ""))
        est = any(c.projection_table(p_)["mode"] in ("computed", "assumption") for p_ in pols)
        add(not est or "est" in pages[3]["text"].lower(), "Every illustrative premium is labelled as an estimate")
        add(a["client_full_name"] in pages[0]["text"] and insurer in pages[0]["text"], "The title slide names the client and the insurer")
    else:
        add("Paybacks compared" in pages[5]["text"] and wd["slide_payback_row"] in pages[1]["text"], "The payback row is in the side-by-side table and 'Paybacks compared' is its own slide")
        add(all(wd["slide_categories"][cat] in pages[1]["text"] for cat in c.FOUR), "All four categories are in the side-by-side table")
        pb = a["proposed"]["payback"]
        add(not pb["present"] or ("estimate" in pages[5]["text"].lower() and c.money(pb["today_value"]["amount"]) in pages[5]["text"]), "The proposed payback's figures are on the slide and projected values are labelled as estimates")
        vu = a["proposed"].get("valid_until")
        add(not vu or vu in pages[6]["text"], "The proposed quote's validity date is in the next steps" if vu else "The quote shows no validity date")
    return R


# ------------------------------------------------------------------ the chat summary (Step 6.8) and the confirmation table
def chat_summary(a, d, folder):
    wd = c.wording()
    out = []
    for p in a["policies"]:
        out.append("**%s - %s (%s)**" % (p["insurer"], p["product_name"], p["policy_number"]))
        out.append("Verdict: %s" % p["verdict"])
        out.append("| Benefit | Sum Assured | Premium |\n|---|---|---|\n" + "\n".join("| %s | %s | %s |" % r for r in c.benefit_rows(p)))
        fn = [x for x in c.finding_numbers(p) if x[1] == "action"]
        out.append("Action Required:" + ("\n" + "\n".join("%d. %s" % (n, h) for n, _t, h, _d in fn) if fn else " none"))
        out.append(wd["chat_summary_pointer"])
        out.append("")
    for kind, ins, name in c.slide_names(a, d):
        out.append("%s - %s: %s" % ("Report 1" if kind == "report1" else "Report 2", ins, name))
    if a["proposed_status"] == "none_for_now":
        out.append("Report 2 was skipped: no proposed covers for now (%s)." % a["proposed_said"])
    out.append(wd["chat_summary_saved"].format(folder=folder))
    return "\n".join(out)


def table_rows(a, docs, ev, today):
    wd = c.wording()
    rows = [("Client", a["client_full_name"], "the documents")]
    for p in a["policies"]:
        t = c.projection_table(p)
        rows.append(("%s: policy" % p["label"], "%s, %s, %s: %s a month, %s" % (p["insurer"], p["product_name"], p["policy_number"], c.money(p["premium"]["monthly"]),
                                                                              "fixed" if p["premium"]["pattern"]["type"] == "fixed" else "age-rated"), "found in: %s" % p["found_in"]))
        rows.append(("%s: benefits" % p["label"], "; ".join("%s %s" % (x, y) for x, y, _z in c.benefit_rows(p)), "the schedule"))
        rows.append(("%s: premium table" % p["label"], {"printed": "the insurer's own printed table", "computed": "computed from the stated yearly increase (illustrative)", "assumption": "computed from Paul's assumption (illustrative)",
                                                         "none": "NOT PROVIDED: no number invented"}[t["mode"]], "the schedule"))
        for r_ in p["benchmark"]:
            rows.append(("%s: benchmark %s" % (p["label"], c.CAT_NAMES[r_["category"]]), "%s%s" % (r_["outcome"].replace("_", " "), " (%s)" % tag(r_) if r_.get("_kind") else ""), "the saved sources"))
        for n, tier, h, _d in c.finding_numbers(p):
            rows.append(("%s: finding %d (%s)" % (p["label"], n, wd["tier_action"] if tier == "action" else wd["tier_awareness"]), h, "the chat's judgement"))
        rows.append(("%s: Verdict" % p["label"], p["verdict"], "the chat's judgement"))
        ho = p["honest_opinion"]
        rows.append(("%s: Broker's Honest Opinion" % p["label"], ho["assessment"], "the chat's judgement"))
    if a["proposed_status"] == "present":
        pd = a["proposed"]
        rows.append(("Proposed quote (Report 2)", "%s %s, %s a month, valid until %s; payback: %s" % (pd["insurer"], pd["product_name"], c.money(pd["premium"]["monthly"]), pd.get("valid_until") or "not stated",
                                                                                                           pd["payback"].get("name") if pd["payback"]["present"] else "none on the quote"), "the proposed quote and its payback document"))
    else:
        rows.append(("Proposed quote", "none for now: Report 2 is NOT built (%s)" % a["proposed_said"], "Paul's words"))
    for x in a["left_out"]:
        rows.append(("Left out on purpose", "%s: shown on the slides as 'Not held (your choice)'" % c.CAT_NAMES[x["category"]], x.get("source")))
    d = today
    for kind, ins, name in c.slide_names(a, d):
        rows.append(("Slides: %s" % ("Report 1 - %s" % ins if kind == "report1" else "Report 2 - proposal against %s" % ins), name, "built by the program"))
    for p in a["policies"]:
        rows.append(("Internal report: %s" % p["label"], c.internal_name(a, p, d), "built by the program"))
    rows.append(("Folder for all the files", "%s > %s" % (a["plan_folder"], c.settings()["folder_name"]), "the client's file"))
    for x in c.paul_flags(a, docs, ev, today):
        rows.append(("Flag", x, "the program" if x not in (a.get("flags") or []) else "the chat"))
    return rows
