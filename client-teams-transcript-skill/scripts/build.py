#!/usr/bin/env python3
"""Build Output 1 (Planner note) and Output 2 (PDF) from content.json.

  build.py <run_dir>

Refuses to draft anything until the pre-build gate (verify.py --stage pre) passes:
both reads, the ledger, the source trace and the mandatory checks. Both outputs come
from the same content.json, so a correction made there reaches both on rebuild.
A first/Fact Find meeting gets the Planner note only (its PDF is the Fact Find Summary).
"""
import argparse
import glob
import os
import subprocess
import sys
from xml.sax.saxutils import escape

import verify
import wrlib as w

NAVY = "#1F3A5F"
GREY = "#666666"


def item_status(it):
    return (it.get("status") or it.get("tag") or "").strip()


# ------------------------------------------------------------------ Output 1
def planner_note(content, names):
    mt = content["meeting_type"]
    c = content["client"]
    lines = ["**%s %s – %s**" % (c["first"], c["surname"], content["meeting_date"])]
    topic = content["topic"].strip()
    lines.append("*%s*" % ("WhatsApp call, %s: %s" % (content["meeting_time"], topic) if mt == "whatsapp" else topic))
    lines.append("")
    if mt == "first":
        lines.append("Please view the **%s** PDF in the client's Fact Find folder." % names["ff_summary_stem"])
    else:
        lines.append("Please view the **%s** file in the client's Fact Find folder." % names["pdf_stem"])

    def bullet(it, label=None):
        text, st = it["text"].strip(), item_status(it)
        if label and not text.lower().startswith(label.lower()):
            text = "%s: %s" % (label, text)
        if st.endswith(":"):
            return "• **%s** %s" % (st, text)
        return "• %s – **%s**" % (text, st) if st else "• " + text

    by_key = {a["key"]: a.get("bullets") or [] for a in content.get("areas") or []}
    done = []
    for key, _, heading in w.AREAS:
        if heading in done:
            continue
        group = [k for k, _, h in w.AREAS if h == heading]
        rows = []
        for k in group:
            label = w.COMBINED_LABEL.get(k) if len(group) > 1 else None
            rows += [bullet(it, label) for it in by_key.get(k, [])]
        if rows:
            lines += ["", "**%s**" % heading, ""] + rows
        done.append(heading)
    if content.get("applications"):
        lines += ["", "**Applications**", ""] + [bullet(it) for it in content["applications"]]
    if content.get("actions"):
        lines += ["", "**Actions**", ""] + [bullet(it) for it in content["actions"]]
    lines += ["", "**Next appointment:** %s" % content["next_appointment"]["text"].strip()]
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------ Output 2
def build_pdf(content, names, path):
    from reportlab.lib.colors import HexColor
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer

    navy = HexColor(NAVY)
    title = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=17, leading=21, textColor=navy, spaceAfter=3)
    sub = ParagraphStyle("s", fontName="Helvetica", fontSize=9.5, leading=12, textColor=HexColor(GREY), spaceAfter=5)
    body = ParagraphStyle("b", fontName="Helvetica", fontSize=10, leading=14, spaceAfter=4)
    head = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=12.5, leading=16, textColor=navy,
                          spaceBefore=11, spaceAfter=4, keepWithNext=1)
    bul = ParagraphStyle("u", parent=body, leftIndent=16, bulletIndent=4, spaceAfter=3, leading=13.5)

    mt, c = content["meeting_type"], content["client"]
    full = "%s %s" % (c["first"], c["surname"])
    if mt == "whatsapp":
        subtitle = "%s (Client)   |   Paul Kafentzis (Broker)   |   Wealth Revolution   |   Call Date: %s   |   Call Time: %s" % (
            full, content["meeting_date"], content["meeting_time"])
    else:
        subtitle = "%s   |   Wealth Revolution   |   Advisor: Paul Kafentzis   |   Meeting Date: %s" % (full, content["meeting_date"])

    story, headings = [], [names["pdf_stem"]]
    story += [Paragraph(escape(names["pdf_stem"]), title), Paragraph(escape(subtitle), sub),
              HRFlowable(width="100%", thickness=1.2, color=navy, spaceAfter=6),
              Paragraph(escape(content["opening"].strip()), body)]

    def section(name, items, tagged=False):
        if not items:
            return
        headings.append(name)
        story.append(Paragraph(escape(name), head))
        for it in items:
            st = item_status(it)
            txt = escape(it["text"].strip())
            if tagged and st:
                html = "<b>%s:</b> %s" % (escape(st.capitalize()), txt)
            elif st.endswith(":"):
                html = "<b>%s</b> %s" % (escape(st), txt)
            elif st:
                html = "%s – <b>%s</b>" % (txt, escape(st))
            else:
                html = txt
            story.append(Paragraph(html, bul, bulletText="•"))

    section("Since the Last Meeting", content.get("since_last"), tagged=True)
    by_key = {a["key"]: a.get("bullets") or [] for a in content.get("areas") or []}
    for key, pdf_head, _ in w.AREAS:
        section(pdf_head, by_key.get(key))
    rest = [h for k, h, _ in w.AREAS if not by_key.get(k)]
    if rest:
        story.append(Spacer(1, 4))
        story.append(Paragraph("Not discussed this meeting: %s." % escape(", ".join(rest)), body))
    section("Applications", content.get("applications"))
    section("Action Points", content.get("actions"))
    nxt = list(content.get("next_steps") or [])
    nxt.append({"text": "Next appointment: " + content["next_appointment"]["text"].strip()})
    section("Next Steps", nxt)

    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm,
                            bottomMargin=1.8 * cm, title=names["pdf_stem"], author="Wealth Revolution")
    doc.build(story)
    return headings


def render_pngs(pdf, out):
    for old in glob.glob(os.path.join(out, "page*.png")):
        os.remove(old)
    r = subprocess.run(["pdftoppm", "-png", "-r", "70", pdf, os.path.join(out, "page")], capture_output=True, text=True)
    if r.returncode:
        w.die("pdftoppm failed: " + r.stderr.strip())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    a = ap.parse_args()

    R, st, ledger, content = verify.run_checks(a.run, "pre")
    if R.fails:
        verify.report(R, st, ledger, content, "pre")
        print("\nBUILD REFUSED. The skill does not allow Output 1 or Output 2 to be drafted until the checks above pass.")
        sys.exit(1)

    names = w.output_names(content)
    out = os.path.join(a.run, w.OUT)
    os.makedirs(out, exist_ok=True)
    for old in glob.glob(os.path.join(out, "*.pdf")) + glob.glob(os.path.join(out, "planner_note.md")):
        os.remove(old)

    note = planner_note(content, names)
    with open(os.path.join(out, "planner_note.md"), "w", encoding="utf-8") as f:
        f.write(note)
    build = {"t": w.now(), "content_sha": w.content_hash(content), "note_sha": w.sha256_text(note),
             "pdf": None, "pdf_sha": None, "headings": []}
    if content["meeting_type"] != "first":
        pdf = os.path.join(out, names["pdf"])
        build["headings"] = build_pdf(content, names, pdf)
        render_pngs(pdf, out)
        build.update(pdf=names["pdf"], pdf_sha=w.sha256_file(pdf))
    st["build"] = build
    w.save_json(os.path.join(a.run, w.STATE), st)

    print("BUILT from content.json (hash %s...)" % build["content_sha"][:10])
    print("  Output 1: %s" % os.path.join(out, "planner_note.md"))
    if build["pdf"]:
        print("  Output 2: %s" % os.path.join(out, build["pdf"]))
        print("  Page images: %s" % ", ".join(sorted(os.path.basename(p) for p in glob.glob(os.path.join(out, "page*.png")))))
    else:
        print("  Output 2: not produced (first/Fact Find meeting: the Fact Find Summary is that meeting's PDF)")
    print("\n----- PLANNER NOTE (paste into the chat verbatim as formatted text, never in a code block) -----")
    print(note)
    print("----- END PLANNER NOTE -----")
    print("NEXT: look at every page image, show the note, send the PDF in the chat, save it with device_commit_files, "
          "write receipt.json, then run verify.py %s" % a.run)


if __name__ == "__main__":
    main()
