#!/usr/bin/env python3
"""Draws the Astute Report Summary PDF from content.json (reportlab) and renders every page to an image.

  build.py <run_dir>

The PDF is the one deliverable of this skill (never chat text alone). It is drawn from content.json alone, in the look Paul's skill has always
described: landscape A4, 15 mm margins, navy title, section bars and table headers (#1B2A4A), gold insurer bands (#9C7A28), light grey row stripes
(#F2F2F2) with a #DADADA grid, orange flag boxes (background #FFF4E5, border #C97A1A, title #C97A1A, text #5A3E00), repeatRows=1 on every table, and a
footer "Astute Report Summary - [Client name] - Confidential" with "Page N". Helvetica (a standard PDF font) needs no font file.
"""
import glob
import os
import subprocess
import sys
from xml.sax.saxutils import escape

import wrlib as w

NAVY, GOLD, STRIPE, GRID, FLAG_BG, FLAG_LINE, FLAG_TEXT = "#1B2A4A", "#9C7A28", "#F2F2F2", "#DADADA", "#FFF4E5", "#C97A1A", "#5A3E00"


def build_pdf(content, path):
    from reportlab.lib.colors import HexColor, white
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    navy, gold, stripe, grid = HexColor(NAVY), HexColor(GOLD), HexColor(STRIPE), HexColor(GRID)
    flag_bg, flag_line, flag_text = HexColor(FLAG_BG), HexColor(FLAG_LINE), HexColor(FLAG_TEXT)
    PW, PH = landscape(A4)
    avail = PW - 30 * mm

    def S(name, **kw):
        base = dict(fontName="Helvetica", fontSize=7.8, leading=9.8, textColor=HexColor("#000000"))
        base.update(kw)
        return ParagraphStyle(name, **base)

    title = S("title", fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=navy, spaceAfter=4)
    hdr = S("hdr", fontSize=9.5, leading=12.5)
    intro = S("intro", fontSize=8.4, leading=11, textColor=HexColor("#404040"), spaceBefore=4, spaceAfter=6)
    bar = S("bar", fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=white)
    band = S("band", fontName="Helvetica-Bold", fontSize=9.4, leading=12, textColor=white)
    sub = S("sub", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=navy, spaceBefore=6, spaceAfter=3, keepWithNext=1)
    th = S("th", fontName="Helvetica-Bold", textColor=white)
    cell = S("cell")
    num = S("num", fontName="Helvetica-Bold", fontSize=8.2)
    small = S("small", fontSize=7, leading=8.8, textColor=HexColor("#444444"))
    party = S("party", fontName="Helvetica-Oblique", fontSize=7.2, leading=9, textColor=HexColor("#333333"))
    ftitle = S("ftitle", fontName="Helvetica-Bold", fontSize=8.4, textColor=flag_line)
    ftext = S("ftext", fontSize=8, leading=10.2, textColor=flag_text)
    bullet = S("bullet", fontSize=8.4, leading=11, leftIndent=10, bulletIndent=0)

    def P(text, style=cell):
        return Paragraph(escape(str(text)), style)

    def lines(items, style=cell):
        return [Paragraph(escape(str(i)), style) for i in items]

    def section_bar(text):
        t = Table([[P(text, bar)]], colWidths=[avail])
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), navy), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4), ("LEFTPADDING", (0, 0), (-1, -1), 6)]))
        return t

    def insurer_band(name):
        t = Table([[P(name, band)]], colWidths=[avail])
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), gold), ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3), ("LEFTPADDING", (0, 0), (-1, -1), 6)]))
        return t

    def flag_box(f):
        inner = Table([[P("FLAG %d: %s" % (f["n"], f["title"]), ftitle)], [P(f["text"], ftext)]], colWidths=[avail])
        inner.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), flag_bg), ("BOX", (0, 0), (-1, -1), 0.9, flag_line), ("TOPPADDING", (0, 0), (-1, -1), 3),
                                   ("BOTTOMPADDING", (0, 0), (-1, -1), 3), ("LEFTPADDING", (0, 0), (-1, -1), 6)]))
        return inner

    def table(head, widths_mm, rows, spans):
        cw = [x * mm for x in widths_mm]
        scale = avail / sum(cw)
        cw = [x * scale for x in cw]
        t = Table([[P(h, th) for h in head]] + rows, colWidths=cw, repeatRows=1)
        st = [("BACKGROUND", (0, 0), (-1, 0), navy), ("GRID", (0, 0), (-1, -1), 0.5, grid), ("VALIGN", (0, 0), (-1, -1), "TOP"),
              ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4), ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
        for i in spans:
            st += [("SPAN", (0, i), (-1, i)), ("BACKGROUND", (0, i - 1), (-1, i), stripe if (i // 2) % 2 == 0 else HexColor("#FFFFFF"))]
        t.setStyle(TableStyle(st))
        return t

    def first_col(p):
        return [P(p["number"], num), P(p["product"], cell), P(p["desc"], small)]

    def policy_tables(policies):
        out = []
        risk = [p for p in policies if p["kind"] == "risk"]
        inv = [p for p in policies if p["kind"] == "investment"]
        if risk:
            rows, spans = [], []
            for p in risk:
                rows.append([first_col(p), lines(p["status"]), lines(p["benefits"]), lines(p["types"]), lines(p["premium"])])
                rows.append([P((p["parties"] or "Parties not shown") + (("  |  Note: " + p["note"]) if p["note"] else ""), party), "", "", "", ""])
                spans.append(len(rows))
            out.append(table(["Policy number / Product (verified)", "Status and start date", "Benefit(s) and cover amount", "Stand-alone or Accelerated", "Premium and premium pattern"],
                             [66, 36, 62, 46, 57], rows, spans))
        if inv:
            rows, spans = [], []
            for p in inv:
                rows.append([first_col(p), lines(p["status"]), lines(p["values"]), lines(p["pattern"]), lines(p["funds"])])
                rows.append([P((p["parties"] or "Parties not shown") + (("  |  Note: " + p["note"]) if p["note"] else ""), party), "", "", "", ""])
                spans.append(len(rows))
            out.append(table(["Policy number / Product (verified)", "Status and start date", "Values", "Premium pattern", "Fund allocation"],
                             [66, 36, 62, 46, 57], rows, spans))
        return out

    def groups(gs, empty, lead=()):
        """A heading is never left alone at the bottom of a page: the lead, the insurer band, its flags and the first table are kept together."""
        lead = list(lead)
        if not gs:
            return [KeepTogether(lead + [P(empty, cell)]), Spacer(1, 4)]
        flow = []
        for k, g in enumerate(gs):
            head = (lead if k == 0 else []) + [insurer_band(g["provider"])]
            for f in g["flags"]:
                head += [Spacer(1, 2), flag_box(f)]
            head.append(Spacer(1, 2))
            tables = policy_tables(g["policies"])
            flow.append(KeepTogether(head + tables[:1]))
            for t in tables[1:]:
                flow.append(t)
            flow.append(Spacer(1, 4))
        return flow

    c = content
    story = [P(c["title"], title)] + [P(x, hdr) for x in c["header_lines"]] + [P(c["intro"], intro)]
    story += groups(c["s1_risk"], "No active risk covers are reflected on the Astute report.", [section_bar(c["headings"][0]), P("Risk Covers", sub)])
    story += groups(c["s1_invest"], "No active investments are reflected on the Astute report.", [P("Investments", sub)])
    rows = [[P(r["category"], num), P(r["reflected"], cell), lines(r["details"])] for r in c["s2_rows"]]
    story += [Spacer(1, 4), KeepTogether([section_bar(c["headings"][1]), Spacer(1, 3), table(["Category", "Reflected on Astute?", "Details"], [60, 40, 167], rows, [])]), Spacer(1, 6)]
    story += groups(c["s3"], "No policies are labelled paid-up on the Astute report.", [section_bar(c["headings"][2]), Spacer(1, 3)])
    story += groups(c["additional"], "No inactive, lapsed or surrendered policies are reflected on the Astute report.", [section_bar(c["headings"][3]), Spacer(1, 3)])
    gen = [section_bar(c["headings"][4]), Spacer(1, 3)] + [Paragraph(escape(x), bullet, bulletText="\u2022") for x in c["general"]]
    story.append(KeepTogether(gen[:3]))
    story += gen[3:]
    for f in c["general_flags"]:
        story += [Spacer(1, 3), flag_box(f)]

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(HexColor("#555555"))
        canvas.drawString(15 * mm, 8 * mm, c["footer"])
        canvas.drawRightString(PW - 15 * mm, 8 * mm, "Page %d" % doc.page)
        canvas.restoreState()

    doc = SimpleDocTemplate(path, pagesize=landscape(A4), leftMargin=15 * mm, rightMargin=15 * mm, topMargin=15 * mm, bottomMargin=15 * mm,
                            title=c["file_name"].replace(".pdf", ""), author="Wealth Revolution", subject="Astute Report Summary")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return {"headings": c["headings"]}


def render_pngs(pdf, out):
    for old in glob.glob(os.path.join(out, "page*.png")):
        os.remove(old)
    r = subprocess.run(["pdftoppm", "-png", "-r", "60", pdf, os.path.join(out, "page")], capture_output=True, text=True)
    if r.returncode:
        w.die("pdftoppm failed: " + r.stderr.strip())


def build_run(run):
    import model
    import verify
    run = os.path.abspath(run)
    R, rj = verify.run_checks(run, "pre")
    blockers = [r for r in R.fails if r[3] in ("report", "read", "data", "products", "flags")]
    if blockers:
        verify.print_audit(R, rj, "pre", run)
        print("\nBUILD REFUSED. The PDF is not drawn until the checks above pass.")
        return False
    data = w.load_json(os.path.join(run, w.DATA))
    products = w.load_opt(os.path.join(run, w.PRODUCTS), {})
    chat = w.load_opt(os.path.join(run, w.FLAGS), {}).get("flags", [])
    content = model.compose(data, products, chat, rj["client"])
    w.save_json(os.path.join(run, w.CONTENT), content)
    out = os.path.join(run, w.OUT)
    os.makedirs(out, exist_ok=True)
    for old in glob.glob(os.path.join(out, "*.pdf")):
        os.remove(old)
    pdf = os.path.join(out, content["file_name"])
    build_pdf(content, pdf)
    render_pngs(pdf, out)
    st = w.load_opt(os.path.join(run, w.STATE), {})
    st["build"] = {"t": w.now(), "content_sha": w.content_hash(content), "pdf": content["file_name"], "pdf_sha": w.sha256_file(pdf), "pdf_size": os.path.getsize(pdf)}
    st.pop("save", None)
    w.save_json(os.path.join(run, w.STATE), st)
    rjp = os.path.join(run, w.RUN)
    rj = w.load_json(rjp)
    again = [sid for sid in ("build", "save", "final") if (rj.get("steps", {}).get(sid) or {}).get("state") == "done"]
    for sid in ("build", "save", "final"):
        rj.get("steps", {}).pop(sid, None)
    w.save_json(rjp, rj)
    if again:
        print("LATER STEPS RE-OPENED because the PDF was rebuilt: redo steps %s." % ", ".join(again))
    print("BUILT from the entered data (hash %s...)" % st["build"]["content_sha"][:10])
    print("  PDF: %s   (%d bytes, landscape A4)" % (pdf, st["build"]["pdf_size"]))
    print("  Page images: %s" % ", ".join(sorted(os.path.basename(p) for p in glob.glob(os.path.join(out, "page*.png")))))
    return True


def main():
    sys.exit(0 if build_run(sys.argv[1]) else 1)


if __name__ == "__main__":
    main()
