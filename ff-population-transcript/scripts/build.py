#!/usr/bin/env python3
"""Builds the Fact Find Transcript PDF from content.json (reportlab) and renders every page to an image.

  build.py <run_dir>

The PDF is the only deliverable of this skill (never a Word file). It is drawn from content.json alone, so a correction made there
reaches the PDF on rebuild. The look is the one Paul approved: navy section headings, smaller navy sub-headings, two-column field
tables with a bold light-blue label column, one fact per line, no page numbers, no forced page breaks, headings kept with their
table, no row split across pages. The font is Aptos when it can be found; otherwise a named substitute, and WHICH font was really
used is recorded and printed (never claimed to be Aptos when it is not).
"""
import argparse
import glob
import os
import re
import subprocess
import sys
from xml.sax.saxutils import escape

import wrlib as w

STYLE_NAMES = (("regular", ("regular", "book", "roman", "normal", "")), ("bold", ("bold",)), ("italic", ("italic", "oblique")),
               ("bolditalic", ("bold italic", "bold oblique", "bolditalic")))
FALLBACKS = ["Aptos", "Carlito", "Liberation Sans", "DejaVu Sans"]
DEFAULT_DIRS = ["/usr/share/fonts", "/usr/local/share/fonts", os.path.expanduser("~/.fonts"), os.path.expanduser("~/.local/share/fonts"),
                "/Library/Fonts", "/System/Library/Fonts/Supplemental", "C:\\Windows\\Fonts", "/mnt/skills", "/mnt/user-data"]


def _style_of(filename):
    n = os.path.splitext(os.path.basename(filename))[0].lower()
    bold, ital = "bold" in n, ("italic" in n or "oblique" in n)
    return "bolditalic" if bold and ital else "bold" if bold else "italic" if ital else "regular"


def _files_in(dirs, depth=4):
    for d in dirs:
        if not d or not os.path.isdir(d):
            continue
        base = d.rstrip(os.sep).count(os.sep)
        for root, subdirs, files in os.walk(d):
            if root.count(os.sep) - base >= depth:
                subdirs[:] = []
            for f in files:
                if f.lower().endswith(".ttf"):
                    yield os.path.join(root, f)


STYLE_TAILS = {"", "regular", "bold", "italic", "bolditalic", "oblique", "boldoblique", "book", "roman", "normal"}


def _stem_match(path, want):
    stem = os.path.splitext(os.path.basename(path))[0].lower().replace(" ", "").replace("_", "").replace("-", "")
    return stem.startswith(want) and stem[len(want):] in STYLE_TAILS


def find_family(family, dirs=None):
    """{'regular','bold','italic','bolditalic'} -> .ttf paths for a family, or None when any of the four is missing."""
    want = family.lower().replace(" ", "")
    found = {}
    for path in _files_in(dirs or []):
        if _stem_match(path, want):
            found.setdefault(_style_of(path), path)
    if len(found) < 4:
        try:
            out = subprocess.run(["fc-list", ":", "family", "file", "style"], capture_output=True, text=True, timeout=20).stdout
        except (OSError, subprocess.SubprocessError):
            out = ""
        for line in out.splitlines():
            m = re.match(r"^(.*?\.ttf): (.*?):style=(.*)$", line.strip(), re.I)
            if not m or family.lower() not in m.group(2).lower().split(","):
                continue
            st = m.group(3).lower()
            kind = "bolditalic" if "bold" in st and ("italic" in st or "oblique" in st) else "bold" if "bold" in st else "italic" if ("italic" in st or "oblique" in st) else "regular"
            if kind == "regular" and not any(x in st for x in ("regular", "book", "roman", "normal")) and st.strip() not in ("",):
                continue
            found.setdefault(kind, m.group(1))
    if len(found) < 4:
        found = {}
        for path in _files_in(DEFAULT_DIRS):
            if _stem_match(path, want):
                found.setdefault(_style_of(path), path)
    return found if len(found) == 4 else None


def is_aptos(ps_names):
    return bool(ps_names) and all(str(n).lower().startswith("aptos") for n in ps_names)


def pick_font(dirs=None):
    """Aptos when found; otherwise the first substitute that has all four styles. Returns the record that is printed in the final checklist."""
    dirs = dirs if dirs is not None else [d for d in os.environ.get("WR_FONT_DIRS", "").split(os.pathsep) if d]
    for fam in FALLBACKS:
        files = find_family(fam, dirs)
        if files:
            return {"wanted": "Aptos", "family": fam, "files": files}
    return {"wanted": "Aptos", "family": "Helvetica", "files": None}


def register(fontrec):
    """Register the chosen font with reportlab; fills in the PostScript names that really end up inside the PDF."""
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    if not fontrec["files"]:
        fontrec.update(names={"regular": "Helvetica", "bold": "Helvetica-Bold", "italic": "Helvetica-Oblique", "bolditalic": "Helvetica-BoldOblique"},
                       ps_names=["Helvetica"], aptos=False, substitute=True, mark="!", glyph_font=None)
        return fontrec
    names, ps = {}, []
    for style, path in fontrec["files"].items():
        nm = "WR-%s-%s" % (fontrec["family"].replace(" ", ""), style)
        tt = TTFont(nm, path)
        pdfmetrics.registerFont(tt)
        names[style] = nm
        ps.append(tt.face.name.decode("latin-1") if isinstance(tt.face.name, bytes) else str(tt.face.name))
    pdfmetrics.registerFontFamily(names["regular"], normal=names["regular"], bold=names["bold"], italic=names["italic"], boldItalic=names["bolditalic"])
    fontrec.update(names=names, ps_names=sorted(set(ps)), aptos=is_aptos(ps), substitute=not is_aptos(ps))
    # the warning sign is not in every font: use it only when it can really be drawn
    face = pdfmetrics.getFont(names["regular"]).face
    mark, gfont = "!", None
    if 0x26A0 in face.charToGlyph:
        mark = "\u26a0"
    else:
        cands = sorted((p for p in _files_in(DEFAULT_DIRS) if _stem_match(p, "dejavusans")), key=lambda p: (_style_of(p) != "bold", p))
        if cands:
            try:
                gt = TTFont("WR-Mark", cands[0])
                pdfmetrics.registerFont(gt)
                mark, gfont = "\u26a0", "WR-Mark"
                fontrec["glyph_ps"] = gt.face.name.decode("latin-1") if isinstance(gt.face.name, bytes) else str(gt.face.name)
            except Exception:  # pragma: no cover
                pass
    fontrec.update(mark=mark, glyph_font=gfont)
    return fontrec


# ------------------------------------------------------------------ drawing
def build_pdf(content, path, lay=None, fontrec=None):
    from reportlab.lib.colors import HexColor
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import HRFlowable, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    lay = lay or w.layout()
    st = lay["style"]
    fontrec = register(fontrec or pick_font())
    nm = fontrec["names"]
    navy, flag_c, border, blue, grey = (HexColor("#" + st[k]) for k in ("navy", "flag", "border", "blue", "grey"))
    label_bg = HexColor("#" + st["label_bg"])
    size = st["size"]
    lead = size * 1.25
    mark = fontrec["mark"] if not fontrec.get("glyph_font") else '<font name="%s">%s</font>' % (fontrec["glyph_font"], fontrec["mark"])

    def S(name, **kw):
        base = dict(fontName=nm["regular"], fontSize=size, leading=lead, textColor=HexColor("#000000"))
        base.update(kw)
        return ParagraphStyle(name, **base)

    title = S("title", fontName=nm["bold"], fontSize=st["title_size"], leading=st["title_size"] * 1.25, textColor=navy, alignment=1, spaceAfter=4)
    brand = S("brand", fontName=nm["bold"], fontSize=size - 1, textColor=blue, alignment=1, spaceAfter=1)
    tag = S("tag", fontSize=size - 4, textColor=grey, alignment=1, spaceAfter=8)
    meta = S("meta", fontSize=size - 1, textColor=grey, alignment=1, spaceAfter=6)
    head = S("head", fontName=nm["bold"], fontSize=st["head_size"], leading=st["head_size"] * 1.25, textColor=navy, spaceBefore=12, spaceAfter=4, keepWithNext=1)
    sub = S("sub", fontName=nm["bold"], fontSize=size, textColor=navy, spaceBefore=7, spaceAfter=3, keepWithNext=1)
    label = S("label", fontName=nm["bold"], fontSize=size - 0.5, leading=lead - 0.5)
    val = S("val", fontSize=size - 0.5, leading=lead - 0.5)
    bul = S("bul", fontSize=size - 0.5, leading=lead - 0.5, leftIndent=11, bulletIndent=1, bulletFontName=nm["regular"], bulletFontSize=size - 0.5)
    added = S("added", parent=None, fontName=nm["italic"], fontSize=size - 0.5, leading=lead - 0.5, leftIndent=11, bulletIndent=1, textColor=flag_c)
    flagp = S("flag", fontName=nm["bold"], fontSize=size - 1, leading=lead - 1, textColor=flag_c, leftIndent=11, bulletIndent=0, spaceBefore=1)

    avail = A4[0] - 2 * st["margin_cm"] * cm
    cw = [avail * st["label_width"], avail * (1 - st["label_width"])]
    headings = []

    def cell(r):
        out = []
        bs = r["bullets"] or [""]
        if r.get("style") == "flag":
            out += [Paragraph("%s %s" % (mark, escape(b)), flagp, bulletText=None) for b in bs]
            return out
        many = len(bs) > 1 or r.get("style") == "added"
        for b in bs:
            if r.get("style") == "added":
                out.append(Paragraph(escape(b), added, bulletText="\u2022"))
            elif many:
                out.append(Paragraph(escape(b), bul, bulletText="\u2022"))
            else:
                out.append(Paragraph(escape(b), val))
        for f in r.get("flags") or []:
            out.append(Paragraph("%s %s" % (mark, escape(f["text"])), flagp))
        return out

    def table(rows):
        data = [[Paragraph(escape(r["label"]), label), cell(r)] for r in rows]
        t = Table(data, colWidths=cw, splitByRow=1)
        t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.5, border), ("BACKGROUND", (0, 0), (0, -1), label_bg), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                               ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5), ("TOPPADDING", (0, 0), (-1, -1), 3),
                               ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
        return t

    def block(heading_flow, rows):
        """Heading + the first rows travel together; the rest of the table follows. A row is never split."""
        if not rows:
            return []
        first, rest = rows[:2], rows[2:]
        out = [KeepTogether([heading_flow, table(first)])]
        if rest:
            out.append(table(rest))
        return out

    story = [Paragraph("WEALTH REVOLUTION", brand), Paragraph("INSURANCE &amp; INVESTMENT BROKERS", tag), Paragraph("CLIENT FACT FIND", title),
             Paragraph(escape("%s %s   |   Meeting date: %s   |   Advisor: %s" % (content["client"]["first"], content["client"]["surname"], content["meeting_date"], lay["advisor"])), meta),
             HRFlowable(width="100%", thickness=1.2, color=navy, spaceAfter=4)]
    for sec in content["sections"]:
        if not sec["blocks"]:
            continue
        h = "%d. %s" % (sec["num"], sec["title"])
        headings.append(h)
        story.append(Paragraph(escape(h), head))
        for b in sec["blocks"]:
            headings.append(b["sub"])
            story += block(Paragraph(escape(b["sub"]), sub), b["rows"])
    cl = content["closing"]
    story += [Spacer(1, 6), HRFlowable(width="100%", thickness=1.0, color=navy, spaceBefore=4, spaceAfter=2)]
    headings.append(cl["title"])
    story += block(Paragraph(escape(cl["title"]), head), cl["rows"])
    if content.get("other_fields"):
        headings.append("Other fields from the form")
        story += block(Paragraph("Other fields from the form", head), content["other_fields"])

    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=st["margin_cm"] * cm, rightMargin=st["margin_cm"] * cm, topMargin=st["margin_cm"] * cm,
                            bottomMargin=st["margin_cm"] * cm, title=(content.get("file_name") or "Fact Find Transcript").replace(".pdf", ""), author="Wealth Revolution",
                            subject="Fact Find Transcript")
    doc.build(story)
    return {"headings": headings, "font": {k: fontrec.get(k) for k in ("wanted", "family", "ps_names", "aptos", "substitute", "mark", "glyph_ps")}}


def render_pngs(pdf, out):
    for old in glob.glob(os.path.join(out, "page*.png")):
        os.remove(old)
    r = subprocess.run(["pdftoppm", "-png", "-r", "70", pdf, os.path.join(out, "page")], capture_output=True, text=True)
    if r.returncode:
        w.die("pdftoppm failed: " + r.stderr.strip())


def main():
    import verify
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    a = ap.parse_args()
    run = os.path.abspath(a.run)
    R, st, ledger, content = verify.run_checks(run, "pre")
    if R.fails:
        verify.report(R, st, ledger, content, "pre", run)
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
    st["build"] = {"t": w.now(), "content_sha": w.content_hash(content), "pdf": content["file_name"], "pdf_sha": w.sha256_file(pdf), "pdf_size": os.path.getsize(pdf),
                   "pages": len(pages), "headings": info["headings"], "font": info["font"]}
    w.save_json(os.path.join(run, w.STATE), st)
    rjp = os.path.join(run, w.RUN)
    if os.path.exists(rjp):                  # a rebuild re-opens every later step (Paul's rule: a correction re-opens the whole task)
        rj = w.load_json(rjp)
        later = ["check", "pdf", "handoffs", "final"]
        again = [sid for sid in later if (rj.get("steps", {}).get(sid) or {}).get("state") == "done"]
        for sid in later:
            rj.get("steps", {}).pop(sid, None)
        w.save_json(rjp, rj)
        if again:
            print("HAND-OVER RE-OPENED because the PDF was rebuilt: redo steps %s and record them again." % ", ".join(again))
    f = info["font"]
    print("BUILT from content.json (hash %s...)" % st["build"]["content_sha"][:10])
    print("  PDF: %s   (%d page(s), %d bytes)" % (pdf, len(pages), st["build"]["pdf_size"]))
    print("  FONT USED: %s%s" % (", ".join(f["ps_names"] or [f["family"]]), "" if f["aptos"] else "   <-- NOT Aptos (Aptos was not found on this computer); tell Paul"))
    print("  Page images: %s" % ", ".join(sorted(os.path.basename(p) for p in glob.glob(os.path.join(out, "page*.png")))))


if __name__ == "__main__":
    main()
