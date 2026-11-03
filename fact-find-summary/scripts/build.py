#!/usr/bin/env python3
"""Draws the Fact Find Summary PDF from content.json (reportlab) and renders every page to an image.

  build.py <run_dir>

The PDF is the one deliverable of this skill (never a Word file). It is drawn from content.json alone, A4, in the look the Summary has always
had (Paul): navy title and headings, a light-blue shaded label column, 0.5 pt grey grid, follow-up items in red bullets, no page numbers.
Helvetica (a standard PDF font) is used, so the PDF needs no font file.
"""
import glob
import os
import subprocess
import sys
from xml.sax.saxutils import escape

import wrlib as w

NAVY, LIGHT, RED, GREY = "#1F3A5F", "#EAF1F8", "#B0271A", "#808080"


def build_pdf(content, path):
    from reportlab.lib.colors import HexColor
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import HRFlowable, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    navy, light, red, grey, border = HexColor(NAVY), HexColor(LIGHT), HexColor(RED), HexColor(GREY), HexColor("#CBD5E0")

    def S(name, **kw):
        base = dict(fontName="Helvetica", fontSize=9.7, leading=13.5, textColor=HexColor("#000000"))
        base.update(kw)
        return ParagraphStyle(name, **base)

    title = S("title", fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=navy, alignment=1, spaceAfter=4)
    sub = S("sub", fontSize=10, textColor=grey, alignment=1, spaceAfter=10)
    joint = S("joint", fontName="Helvetica-Oblique", fontSize=9.7, textColor=HexColor("#404040"), spaceAfter=8)
    h1 = S("h1", fontName="Helvetica-Bold", fontSize=14, leading=17, textColor=navy, spaceBefore=12, spaceAfter=5, keepWithNext=1)
    h2 = S("h2", fontName="Helvetica-Bold", fontSize=11.5, leading=14, textColor=navy, spaceBefore=8, spaceAfter=3, keepWithNext=1)
    h3 = S("h3", fontName="Helvetica-Bold", fontSize=9.7, textColor=navy, spaceBefore=5, spaceAfter=2, keepWithNext=1)
    label = S("label", fontName="Helvetica-Bold")
    val = S("val")
    bul = S("bul", leftIndent=10, bulletIndent=0)
    flag = S("flag", fontName="Helvetica-Bold", textColor=red, leftIndent=10, bulletIndent=0, spaceBefore=1)
    fu = S("fu", textColor=red, leftIndent=12, bulletIndent=2, spaceAfter=2)

    avail = A4[0] - 2 * 18 * mm
    cw = [avail * 0.37, avail * 0.63]

    def cell(r):
        out = []
        vs = r["values"] or [""]
        for v in vs:
            out.append(Paragraph(escape(v), bul, bulletText="•") if (r.get("bullets") or len(vs) > 1) else Paragraph(escape(v), val))
        for f in r.get("flags") or []:
            out.append(Paragraph("Flag: " + escape(f), flag))
        return out

    def table(rows):
        t = Table([[Paragraph(escape(r["label"]), label), cell(r)] for r in rows], colWidths=cw, splitByRow=1)
        t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.5, border), ("BACKGROUND", (0, 0), (0, -1), light), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                               ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                               ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
        return t

    c = content
    story = [Paragraph(escape(c["title"]), title),
             Paragraph(escape("%s %s  |  Wealth Revolution  |  Advisor: %s  |  Date Completed: %s" % (c["client"]["first"], c["client"]["surname"], c["advisor"], c["date_completed"])), sub),
             HRFlowable(width="100%", thickness=1, color=navy, spaceAfter=8)]
    if c.get("joint"):
        story.append(Paragraph(escape("Joint meeting with a spouse (%s): this Summary covers %s %s only. The debts and the children are common to both." %
                                      (c["joint"], c["client"]["first"], c["client"]["surname"])), joint))
    headings = []
    for sec in c["sections"]:
        h = "%d. %s" % (sec["num"], sec["title"])
        headings.append(h)
        first = True
        if sec["num"] == 9:
            story.append(Paragraph(escape(h), h1))
            for r in sec["blocks"][0]["rows"]:
                story.append(Paragraph(escape(r["values"][0]), fu, bulletText="•"))
            if not sec["blocks"][0]["rows"]:
                story.append(Paragraph("Nothing is outstanding.", val))
            continue
        for b in sec["blocks"]:
            heads = [Paragraph(escape(h), h1)] if first else []
            first = False
            if b["level"] == 2:
                story.append(KeepTogether(heads + [Paragraph(escape(b["sub"]), h2)]) if heads else Paragraph(escape(b["sub"]), h2))
                headings.append(b["sub"])
                continue
            if b["sub"]:
                heads.append(Paragraph(escape(b["sub"]), h3))
                headings.append(b["sub"])
            if b["rows"]:
                rows = b["rows"]
                story.append(KeepTogether(heads + [table(rows[:2])]))
                if rows[2:]:
                    story.append(table(rows[2:]))
            elif heads:
                story += heads
        if first:                                         # a section with no rows still shows its heading
            story += [Paragraph(escape(h), h1), Paragraph("Nothing recorded in the Fact Find.", val)]
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=18 * mm, bottomMargin=18 * mm,
                            title=c["file_name"].replace(".pdf", ""), author="Wealth Revolution", subject="Fact Find Summary")
    doc.build(story)
    return {"headings": headings}


def render_pngs(pdf, out):
    for old in glob.glob(os.path.join(out, "page*.png")):
        os.remove(old)
    r = subprocess.run(["pdftoppm", "-png", "-r", "70", pdf, os.path.join(out, "page")], capture_output=True, text=True)
    if r.returncode:
        w.die("pdftoppm failed: " + r.stderr.strip())


def main():
    import verify
    run = os.path.abspath(sys.argv[1])
    R, st, content = verify.run_checks(run, "pre")
    if R.fails:
        verify.print_audit(R, st, content, "pre", run)
        print("\nBUILD REFUSED. The PDF is not drawn until the checks above pass.")
        sys.exit(1)
    out = os.path.join(run, w.OUT)
    os.makedirs(out, exist_ok=True)
    for old in glob.glob(os.path.join(out, "*.pdf")):
        os.remove(old)
    pdf = os.path.join(out, content["file_name"])
    info = build_pdf(content, pdf)
    render_pngs(pdf, out)
    pages = verify.pdf_pages(pdf) or []
    st["build"] = {"t": w.now(), "content_sha": w.content_hash(content), "pdf": content["file_name"], "pdf_sha": w.sha256_file(pdf),
                   "pdf_size": os.path.getsize(pdf), "pages": len(pages), "headings": info["headings"]}
    w.save_json(os.path.join(run, w.STATE), st)
    rjp = os.path.join(run, w.RUN)
    if os.path.exists(rjp):                  # a rebuild re-opens every later step (Paul: a correction re-opens the whole task)
        rj = w.load_json(rjp)
        again = [sid for sid in ("check", "deliver", "final") if (rj.get("steps", {}).get(sid) or {}).get("state") == "done"]
        for sid in ("check", "deliver", "final"):
            rj.get("steps", {}).pop(sid, None)
        w.save_json(rjp, rj)
        if again:
            print("HAND-OVER RE-OPENED because the PDF was rebuilt: redo steps %s." % ", ".join(again))
    print("BUILT from content.json (hash %s...)" % st["build"]["content_sha"][:10])
    print("  PDF: %s   (%d page(s), %d bytes, A4)" % (pdf, len(pages), st["build"]["pdf_size"]))
    print("  Page images: %s" % ", ".join(sorted(os.path.basename(p) for p in glob.glob(os.path.join(out, "page*.png")))))


if __name__ == "__main__":
    main()
