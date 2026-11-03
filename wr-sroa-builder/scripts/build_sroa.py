#!/usr/bin/env python3
"""
Build a Wealth Revolution Servicing Record of Advice (SROA) PDF.

Usage:
    python build_sroa.py <data.json> <output.pdf>

See references/sroa_data_schema.md for the exact shape of data.json.
"""

import json
import os
import sys
import textwrap

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import black, white
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

PAGE_W, PAGE_H = A4
MARGIN_L = 50
MARGIN_R = 50
CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R

FONT = "Helvetica"
FONT_B = "Helvetica-Bold"

# Fixed order for the servicing-change line items (per WR convention).
LINE_ITEM_ORDER = [
    "Life Cover",
    "Disability Cover",
    "Dread Disease",
    "Income Protection",
    "Premium",
    "ACI (Automatic Cover Increase)",
    "ABI (Automatic Benefit Increase)",
    "Retrenchment Cover",
]

FIXED_ADVISOR_NAME = "Paul Kafentzis"
FIXED_ADVISOR_CODE = "FSP45946"

BOTTOM_MARGIN = 50
TOP_Y = PAGE_H - 55

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(SCRIPT_DIR, "..", "assets", "WR_Logo.png")


def ensure_space(c, y, needed_height):
    """Start a new page if the next block won't fit above BOTTOM_MARGIN.
    Content length varies a lot on this document (BrightRock needs-based
    policies especially can run to 9-10 line items), so a single fixed page
    is not guaranteed to be enough — without this check, trailing content
    like the Financial Advisor block silently draws off the bottom edge of
    the page and gets clipped instead of flowing onto a second page."""
    if y - needed_height < BOTTOM_MARGIN:
        c.showPage()
        y = TOP_Y
    return y


def wrap_text(c, text, font, size, max_width):
    """Wrap text to fit max_width, honoring explicit newlines as paragraph breaks."""
    lines = []
    for para in text.split("\n"):
        if para.strip() == "":
            lines.append("")
            continue
        words = para.split(" ")
        current = ""
        for w in words:
            trial = (current + " " + w).strip()
            if stringWidth(trial, font, size) <= max_width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = w
        if current:
            lines.append(current)
    return lines


def draw_box(c, x, y_top, w, h):
    c.rect(x, y_top - h, w, h, stroke=1, fill=0)


def measure_box_height(c, text, w, font=FONT, size=9.5, pad=6, leading=12.5, min_h=70):
    """Compute the box height needed to fit all wrapped lines of text without
    truncation. Callers should use this instead of hardcoding a box height,
    since content length varies a lot (e.g. BrightRock's needs-based policies
    can produce far more servicing-change line items than a traditional
    Life/Disability/Dread/Income policy)."""
    lines = wrap_text(c, text, font, size, w - 2 * pad)
    needed = 2 * pad + max(len(lines), 1) * leading + (size - leading if lines else 0)
    return max(min_h, needed)


def draw_wrapped_in_box(c, x, y_top, w, h, text, font=FONT, size=9.5, pad=6, leading=12.5):
    draw_box(c, x, y_top, w, h)
    lines = wrap_text(c, text, font, size, w - 2 * pad)
    c.setFont(font, size)
    ty = y_top - pad - size
    for line in lines:
        if ty < (y_top - h) + pad - 2:
            break  # would overflow the box; caller should size boxes generously
        c.drawString(x + pad, ty, line)
        ty -= leading
    return lines


def measure_grouped_box_height(c, groups, w, font=FONT, font_b=FONT_B, size=9.5,
                                pad=6, leading=12.5, heading_gap=4, group_gap=6,
                                min_h=70):
    """Like measure_box_height, but for the grouped-heading layout: a list of
    {"heading": str, "bullets": [str]} groups, each rendered as a bold
    heading followed by indented bullet lines."""
    total = 2 * pad
    for gi, group in enumerate(groups):
        total += leading  # heading line
        for b in group["bullets"]:
            lines = wrap_text(c, "\u2022 " + b, font, size, w - 2 * pad - 14)
            total += max(len(lines), 1) * leading
        if gi < len(groups) - 1:
            total += group_gap
    return max(min_h, total)


def draw_grouped_box(c, x, y_top, w, h, groups, font=FONT, font_b=FONT_B,
                      size=9.5, pad=6, leading=12.5, group_gap=6):
    """Render bold group headings with indented bullet lines underneath,
    inside a bordered box — used for the BrightRock-style Life
    Cover/Lump Sum Disability Cover/Income Protector/Additional Expense
    Needs (Dread Disease)/Policy Details breakdown."""
    draw_box(c, x, y_top, w, h)
    ty = y_top - pad - size
    bottom_limit = (y_top - h) + pad - 2
    for gi, group in enumerate(groups):
        if ty < bottom_limit:
            print(
                f"WARNING: grouped box overflow — heading "
                f"'{group['heading']}' and everything after it was cut off. "
                f"This should not happen; measure_grouped_box_height and "
                f"draw_grouped_box have diverged again — check for another "
                f"width/prefix mismatch between them.",
                file=sys.stderr,
            )
            break
        c.setFont(font_b, size)
        c.drawString(x + pad, ty, group["heading"])
        ty -= leading
        c.setFont(font, size)
        for b in group["bullets"]:
            for line in wrap_text(c, "\u2022 " + b, font, size, w - 2 * pad - 14):
                if ty < bottom_limit:
                    print(
                        f"WARNING: grouped box overflow inside heading "
                        f"'{group['heading']}' — a bullet was cut off. This "
                        f"should not happen; check measure_grouped_box_height "
                        f"for a mismatch against draw_grouped_box.",
                        file=sys.stderr,
                    )
                    break
                c.drawString(x + pad + 14, ty, line)
                ty -= leading
        if gi < len(groups) - 1:
            ty -= group_gap


def build_requested_changes_text(servicing_changes):
    """
    servicing_changes: list of dicts:
        {"item": str, "old": str, "new": str, "no_change": bool}
    Rendered in LINE_ITEM_ORDER when items match that fixed list; any item
    not in the fixed list (e.g. a one-off change) is appended at the end.
    """
    def base(name):
        """'Premium (incl. R20 policy fee)' -> 'Premium', 'ACI (Automatic Cover Increase)' -> 'ACI': the fixed list is matched by the name before the bracket."""
        return name.split(" (")[0].strip()

    by_item = {base(sc["item"]): sc for sc in servicing_changes}
    ordered_lines = []

    def fmt(sc):
        if sc.get("no_change"):
            # the figure is shown in brackets (Paul's yes/no list, 03/11/2026) so the reader sees what stayed the same
            return f"{sc['item']}: No change" + (f" ({sc['new']})" if sc.get("new") else "")
        return f"{sc['item']}: {sc['old']} \u2192 {sc['new']}"

    fixed = [base(i) for i in LINE_ITEM_ORDER]
    for item in fixed:
        if item in by_item:
            ordered_lines.append(fmt(by_item[item]))
    for sc in servicing_changes:
        if base(sc["item"]) not in fixed:
            ordered_lines.append(fmt(sc))
    return "\n".join(ordered_lines)


def check_premium_includes_fee(data):
    """Soft reminder only — never blocks the build. The R20 monthly policy
    fee must always be included in the Premium figures shown (source docs
    usually state this directly as 'Total premium (including the policy
    fee)' — use that number rather than doing the arithmetic by hand)."""
    texts = []
    for sc in data.get("servicing_changes", []):
        if "premium" in sc.get("item", "").lower():
            texts.append(sc.get("item", ""))
    for g in data.get("grouped_changes", []) or []:
        for b in g.get("bullets", []):
            if "premium" in b.lower():
                texts.append(b)
    if texts and not any(
        "r20" in t.lower() or "incl" in t.lower() for t in texts
    ):
        print(
            "WARNING: Premium line item doesn't mention the R20 policy fee "
            "or 'incl.' — confirm the figures already include it before "
            "delivering this SROA.",
            file=sys.stderr,
        )


def build_sroa(data, output_path):
    check_premium_includes_fee(data)
    c = canvas.Canvas(output_path, pagesize=A4)
    c.setTitle(f"SROA - {data.get('insurer','')} - {data.get('owner','')}")

    y = PAGE_H - 55

    # Header — WR logo
    logo_w = 95
    logo_h = 53.5  # preserves the cropped logo's ~1.78:1 aspect ratio
    if os.path.exists(LOGO_PATH):
        c.drawImage(
            ImageReader(LOGO_PATH),
            MARGIN_L, y - logo_h + 12,
            width=logo_w, height=logo_h,
            preserveAspectRatio=True, mask="auto",
        )
    else:
        # Fallback if the logo asset is ever missing — never block document
        # generation on a missing image.
        c.setFont(FONT_B, 9)
        c.drawString(MARGIN_L, y, "WEALTH REVOLUTION")
        c.setFont(FONT, 7.5)
        c.drawString(MARGIN_L, y - 11, "INSURANCE & INVESTMENT BROKERS")
    y -= 75

    c.setFont(FONT_B, 13)
    c.drawCentredString(PAGE_W / 2, y, "FAIS \u2018RECORD OF ADVICE\u2019 FOR SERVICING CHANGES")
    y -= 30

    # Insurer / Policy Number / Owner
    label_w = 110
    field_h = 18
    for label, value in [
        ("Insurer :", data.get("insurer", "")),
        ("Policy Number :", data.get("policy_number", "")),
        ("Owner :", data.get("owner", "")),
        ("ID Number :", data.get("owner_id", "")),
    ]:
        c.setFont(FONT, 10)
        c.drawString(MARGIN_L, y - 13, label)
        draw_box(c, MARGIN_L + label_w, y, CONTENT_W - label_w, field_h)
        c.setFont(FONT, 10)
        c.drawString(MARGIN_L + label_w + 6, y - 13, value)
        y -= field_h + 12

    y -= 6

    # Blocks 1-3: standalone quote summaries (FNA / Shortfall / Alternative),
    # each showing that quote's own figures under the same grouped headings
    # used in Block 4. Not an old->new comparison - just what that quote
    # itself offers.
    for block in data.get("quote_blocks", []):
        label = block.get("block_label", "")
        title = block.get("title", "")
        cp = block.get("cp_number", "")
        header_bits = [f"{label} \u2014 {title}"] if label or title else []
        cp_line = f"CP Number: {cp}" if cp else ""

        if not block.get("compiled", True):
            note = block.get(
                "not_compiled_note",
                "Not compiled for this client.",
            )
            box_h = measure_box_height(c, note, CONTENT_W, min_h=30)
            y = ensure_space(c, y, 14 + box_h)
            c.setFont(FONT_B, 10.5)
            c.drawString(MARGIN_L, y, " ".join(header_bits))
            y -= 14
            draw_wrapped_in_box(c, MARGIN_L, y, CONTENT_W, box_h, note)
            y -= box_h + 16
            continue

        groups = block.get("groups", [])
        box_h = measure_grouped_box_height(c, groups, CONTENT_W, min_h=70)
        heading_extra = 13 if cp_line else 0
        y = ensure_space(c, y, 14 + heading_extra + box_h)

        c.setFont(FONT_B, 10.5)
        c.drawString(MARGIN_L, y, " ".join(header_bits))
        y -= 14
        if cp_line:
            c.setFont(FONT, 9)
            c.drawString(MARGIN_L, y, cp_line)
            y -= heading_extra
        draw_grouped_box(c, MARGIN_L, y, CONTENT_W, box_h, groups)
        y -= box_h + 16

    # Block 4: Requested Servicing Change/s — Current PS -> Accepted Quote
    grouped = data.get("grouped_changes")
    if grouped:
        box_h = measure_grouped_box_height(c, grouped, CONTENT_W, min_h=70)
    else:
        changes_text = build_requested_changes_text(data.get("servicing_changes", []))
        box_h = measure_box_height(c, changes_text, CONTENT_W, min_h=70)

    cp_number = data.get("accepted_quote_cp_number", "")
    block4_label = "Block 4 \u2014 " if data.get("quote_blocks") else ""
    heading_extra = 13 if cp_number else 0
    y = ensure_space(c, y, 14 + heading_extra + box_h)

    c.setFont(FONT, 10.5)
    c.drawString(MARGIN_L, y, f"{block4_label}Requested Servicing Change/s:")
    y -= 14
    if cp_number:
        c.setFont(FONT, 9)
        c.drawString(
            MARGIN_L, y,
            f"Policy Number: {data.get('policy_number', '')}    |    "
            f"Accepted Quote \u2014 CP Number: {cp_number}",
        )
        y -= heading_extra

    if grouped:
        draw_grouped_box(c, MARGIN_L, y, CONTENT_W, box_h, grouped)
    else:
        draw_wrapped_in_box(c, MARGIN_L, y, CONTENT_W, box_h, changes_text)
    y -= box_h + 16

    # Record of Advice (basis of recommendation)
    box_h = measure_box_height(c, data.get("advice_narrative", ""), CONTENT_W, min_h=70)
    y = ensure_space(c, y, 13 + 14 + box_h)
    c.setFont(FONT, 10.5)
    c.drawString(
        MARGIN_L, y,
        "Record of Advice: (Financial Advisor to give a brief summary of the basis of",
    )
    y -= 13
    c.drawString(MARGIN_L, y, "recommending the requested servicing changes):")
    y -= 14
    draw_wrapped_in_box(c, MARGIN_L, y, CONTENT_W, box_h, data.get("advice_narrative", ""))
    y -= box_h + 16

    # Portfolio Changes
    box_h = measure_box_height(
        c, data.get("portfolio_changes_narrative", "N/A"), CONTENT_W, min_h=40,
    )
    y = ensure_space(c, y, 14 + 13 + 14 + box_h)
    c.setFont(FONT_B, 10.5)
    c.drawString(MARGIN_L, y, "Portfolio Changes")
    y -= 14
    c.setFont(FONT, 10.5)
    c.drawString(
        MARGIN_L, y,
        "Record of Advice: (Financial Advisor to provide a reason for portfolio",
    )
    y -= 13
    c.drawString(MARGIN_L, y, "change, in light of owner\u2019s risk profile)")
    y -= 14
    draw_wrapped_in_box(
        c, MARGIN_L, y, CONTENT_W, box_h,
        data.get("portfolio_changes_narrative", "N/A"),
    )
    y -= box_h + 18

    # Confirmation paragraph + signatures + advisor block: kept together as
    # one unit and pre-measured, so this whole block moves to a fresh page
    # together rather than splitting awkwardly or being clipped off the
    # bottom of the page.
    confirm_text = (
        "I confirm that the above information is a correct reflection of the advice "
        "provided in respect of the requested servicing changes and a copy of this "
        "document was provided to me in writing."
    )
    confirm_lines = wrap_text(c, confirm_text, FONT, 9.5, CONTENT_W)
    block_needed = (
        len(confirm_lines) * 12.5 + 10  # confirmation paragraph
        + 34  # blank signing space above the lines
        + 13 + 13 + 11 + 16  # names/captions + gap before date row
        + 20  # per-signatory date row
        + 26  # gap before Financial Advisor block
        + 20 + 14  # Financial Advisor block
    )
    y = ensure_space(c, y, block_needed)

    c.setFont(FONT, 9.5)
    for line in confirm_lines:
        c.drawString(MARGIN_L, y, line)
        y -= 12.5
    y -= 10

    # Two distinct signature lines: blank space above each line is left
    # clear for the client/advisor to physically sign. Typed names and
    # captions are printed below the line, never on or above it.
    y -= 34  # blank signing space above the lines
    col_w = CONTENT_W / 2
    col_gap = 20
    line_y = y
    c.setLineWidth(1)
    c.line(MARGIN_L, line_y, MARGIN_L + col_w - col_gap, line_y)
    c.line(MARGIN_L + col_w + col_gap, line_y, MARGIN_L + CONTENT_W, line_y)

    y -= 13
    c.setFont(FONT, 10)
    c.drawString(MARGIN_L, y, data.get("client_signature_name", ""))
    c.drawString(MARGIN_L + col_w + col_gap, y, FIXED_ADVISOR_NAME)

    y -= 13
    c.setFont(FONT, 9)
    c.drawString(MARGIN_L, y, "Signature of Owner/")
    c.drawString(MARGIN_L + col_w + col_gap, y, "Signature of Financial Advisor")
    y -= 11
    c.drawString(MARGIN_L, y, "Authorised Signatory")
    y -= 16

    # Each signatory gets their own date field — the client and the advisor
    # do not necessarily sign on the same day, so a single shared date field
    # is not accurate.
    c.setFont(FONT, 9)
    c.drawString(MARGIN_L, y - 11, "Date :")
    c.drawString(MARGIN_L + col_w + col_gap, y - 11, "Date :")
    form = c.acroForm
    form.textfield(
        name="sroa_date_client",
        tooltip="Date signed by client",
        x=MARGIN_L + 32,
        y=y - 15,
        width=110,
        height=14,
        borderStyle="underlined",
        borderColor=black,
        fillColor=white,
        textColor=black,
        fontSize=9,
        forceBorder=True,
    )
    form.textfield(
        name="sroa_date_advisor",
        tooltip="Date signed by financial advisor",
        x=MARGIN_L + col_w + col_gap + 32,
        y=y - 15,
        width=110,
        height=14,
        borderStyle="underlined",
        borderColor=black,
        fillColor=white,
        textColor=black,
        fontSize=9,
        forceBorder=True,
    )
    y -= 26

    # Financial Advisor block (fixed)
    c.setFont(FONT_B, 10)
    c.drawString(MARGIN_L, y, "Financial Advisor:")
    y -= 20
    c.setFont(FONT, 10)
    c.drawString(MARGIN_L, y, "Code:")
    c.drawString(MARGIN_L + 45, y, FIXED_ADVISOR_CODE)
    c.drawString(MARGIN_L + 230, y, "Name :")
    c.drawString(MARGIN_L + 275, y, FIXED_ADVISOR_NAME)

    c.showPage()
    c.save()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python build_sroa.py <data.json> <output.pdf>")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        data = json.load(f)
    build_sroa(data, sys.argv[2])
    print(f"Wrote {sys.argv[2]}")
