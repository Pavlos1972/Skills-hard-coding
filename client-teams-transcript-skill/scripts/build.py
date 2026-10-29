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

import page
import verify
import wrlib as w

NAVY = "#1F3A5F"
GREY = "#666666"


def item_status(it):
    return (it.get("status") or it.get("tag") or "").strip()


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
    for key, heading in w.AREAS:
        section(heading, by_key.get(key))
    rest = [w.AREA_HEADING[k] for k in w.EIGHT if not by_key.get(k)]
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
    for old in glob.glob(os.path.join(out, "*.pdf")):
        os.remove(old)

    model = page.note_model(content, names)
    files = {
        names["page"]: page.render_page(model, content),
        names["note_txt"]: page.render_text(model, markdown=True),
    }
    msg = page.teams_message(content)
    files[names["teams"]] = msg + "\n"
    for old in glob.glob(os.path.join(out, "planner_note.*")) + glob.glob(os.path.join(out, "teams_message.txt")):
        os.remove(old)
    for fname, body in files.items():
        with open(os.path.join(out, fname), "w", encoding="utf-8") as f:
            f.write(body)
    build = {"t": w.now(), "content_sha": w.content_hash(content),
             "files": {fname: w.sha256_text(body) for fname, body in files.items()},
             "pdf": None, "pdf_sha": None, "headings": []}
    if content["meeting_type"] != "first":
        pdf = os.path.join(out, names["pdf"])
        build["headings"] = build_pdf(content, names, pdf)
        render_pngs(pdf, out)
        build.update(pdf=names["pdf"], pdf_sha=w.sha256_file(pdf))
    st["build"] = build
    w.save_json(os.path.join(a.run, w.STATE), st)
    rjp = os.path.join(a.run, w.RUN)
    if os.path.exists(rjp):                  # a rebuild re-opens every hand-over step (Paul's rule: a correction re-opens the whole task)
        rj = w.load_json(rjp)
        again = [sid for sid in ("check", "planner", "pdf", "handoffs", "final") if (rj.get("steps", {}).get(sid) or {}).get("state") == "done"]
        for sid in ("check", "planner", "pdf", "handoffs", "final"):
            rj.get("steps", {}).pop(sid, None)
        w.save_json(rjp, rj)
        if again:
            print("HAND-OVER RE-OPENED because the outputs were rebuilt: redo steps %s and record them again." % ", ".join(again))

    print("BUILT from content.json (hash %s...)" % build["content_sha"][:10])
    print("  Planner page (publish this as the Artifact): %s" % os.path.join(out, names["page"]))
    print("  Planner note, fallback text only if the page tool is unavailable: %s" % os.path.join(out, names["note_txt"]))
    if build["pdf"]:
        print("  PDF: %s" % os.path.join(out, build["pdf"]))
        print("  Page images: %s" % ", ".join(sorted(os.path.basename(p) for p in glob.glob(os.path.join(out, "page*.png")))))
    else:
        print("  PDF: not produced (first/Fact Find meeting: the Fact Find Summary is that meeting's PDF)")
    print("  Message to Sitamah (needs Paul's yes before sending): %s" % os.path.join(out, names["teams"]))
    print("    " + msg)


if __name__ == "__main__":
    main()
