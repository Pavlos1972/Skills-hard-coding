#!/usr/bin/env python3
"""The Retirement / Investment email-embedding pipeline, exactly as the skill has always described it, made a fixed program.

  the chat writes ONE html page as before (the client's own reply header + body + the quoted proposal beneath it);
  this program then does the rest: rewrite every font-size so the body text maps to 15 pt, render with wkhtmltopdf at a known page geometry
  (never LibreOffice, never --zoom), turn each page into a 150 dpi JPEG, and embed the pages (embed_email_images.embed) right after the
  active section's table: before 'Investment Planning' for a Retirement ROA, before 'POLICY REPLACEMENT' for an Investment ROA.

The font rule: the embedded image is shown at 5,000,000 EMU wide (about 5.468 in); the page content is 7.5 in wide, so the scale is 0.729 and a
base font of 15 pt shows as the ROA's own 11 pt Aptos.
"""
import os
import re
import shutil
import subprocess

import embed_email_images as emb
import wrlib as w

TARGET_PT = 15.0
WK_FLAGS = ["--page-width", "8.5in", "--page-height", "11in", "--margin-left", "0.5in", "--margin-right", "0.5in", "--margin-top", "0.5in", "--margin-bottom", "0.5in"]
HEADING_FOR = {"retirement": "Investment Planning", "investment": "POLICY REPLACEMENT"}
_FS = re.compile(r"font-size\s*:\s*([0-9]*\.?[0-9]+)\s*(pt|px)\b", re.I)


def renderer():
    """The wkhtmltopdf program (WR_WKHTMLTOPDF may name it; used for tests and special installs). None if it is not available."""
    return os.environ.get("WR_WKHTMLTOPDF") or shutil.which("wkhtmltopdf")


def tools_problems():
    out = []
    if not renderer():
        out.append("wkhtmltopdf is not available (the email pages are always rendered with it, never with LibreOffice)")
    for t in ("pdftoppm", "zip", "unzip"):
        if not shutil.which(t):
            out.append("%s is not available" % t)
    return out


def rescale_fonts(html, base_pt=None):
    """(new html, info): every font-size value rewritten by one factor so the dominant body size becomes 15 pt."""
    sizes = []
    for m in _FS.finditer(html):
        v = float(m.group(1)) * (0.75 if m.group(2).lower() == "px" else 1.0)
        sizes.append(round(v, 2))
    if not sizes and not base_pt:
        return html.replace("</head>", "<style>body{font-size:%gpt}</style></head>", 1) if "</head>" in html else "<style>body{font-size:%gpt}</style>" % TARGET_PT + html, {"dominant": None, "factor": 1.0}
    dominant = float(base_pt) if base_pt else max(set(sizes), key=lambda s: (sizes.count(s), s))
    factor = TARGET_PT / dominant

    def sub(m):
        v = float(m.group(1)) * (0.75 if m.group(2).lower() == "px" else 1.0)
        return "font-size:%.2fpt" % (v * factor)
    return _FS.sub(sub, html), {"dominant": dominant, "factor": round(factor, 4), "values": len(sizes)}


def run(html_in, workdir, docx_in, docx_out, bundle, base_pt=None):
    """Render, image and embed. Returns a record of what was done (command line, pages, heading, factor)."""
    if bundle not in HEADING_FOR:
        raise ValueError("only Retirement and Investment ROAs embed the email")
    wk = renderer()
    if not wk:
        raise RuntimeError("wkhtmltopdf is not available")
    os.makedirs(workdir, exist_ok=True)
    with open(html_in, encoding="utf-8") as f:
        html, info = rescale_fonts(f.read(), base_pt)
    scaled = os.path.join(workdir, "email_scaled.html")
    with open(scaled, "w", encoding="utf-8") as f:
        f.write(html)
    pdf = os.path.join(workdir, "email.pdf")
    cmd = [wk] + WK_FLAGS + [scaled, pdf]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if not os.path.exists(pdf):
        raise RuntimeError("wkhtmltopdf produced no PDF: %s" % (r.stderr or r.stdout)[-400:])
    images = os.path.join(workdir, "images")
    shutil.rmtree(images, ignore_errors=True)
    os.makedirs(images)
    r = subprocess.run(["pdftoppm", "-jpeg", "-r", "150", pdf, os.path.join(images, "page")], capture_output=True, text=True)
    pages = sorted(f for f in os.listdir(images) if f.lower().endswith(".jpg"))
    if r.returncode or not pages:
        raise RuntimeError("pdftoppm produced no pages: %s" % r.stderr[-300:])
    emb.embed(docx_in, images, docx_out, HEADING_FOR[bundle])
    return {"command": [os.path.basename(cmd[0])] + WK_FLAGS, "pages": len(pages), "heading": HEADING_FOR[bundle], "dominant_pt": info["dominant"], "factor": info["factor"],
            "pdf_sha": w.sha256_file(pdf), "html_sha": w.sha256_file(html_in)}
