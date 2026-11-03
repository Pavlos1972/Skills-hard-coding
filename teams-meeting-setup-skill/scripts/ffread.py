#!/usr/bin/env python3
"""Reads the Fact Find Transcript PDF (the report that ff-population-transcript draws) into sections, blocks and rows.

  ffread.py <fact_find.pdf>          prints a short report (for a quick look)

The report is drawn by a program in a fixed layout: a title block, then numbered sections (14 pt bold headings), each with 12 pt bold
sub-headings and two-column tables (bold label | value), then "Next Steps & Next Meeting". This reader follows that layout. If the PDF is
not in it (a hand-made Fact Find, an old layout, a scan) it says so and the job STOPS: it never guesses.
"""
import json
import re
import sys

import wrlib as w

EXPECTED = {1: "Client Info", 2: "Occupation", 3: "Income & Household", 4: "Existing Cover & Retirement", 5: "Investments",
            6: "Medical, Will & Short-Term", 7: "Debts", 8: "Children", 9: "Health", 10: "Advisor Actions", 11: "Risk Calculation"}
CLOSING = "Next Steps & Next Meeting"
OTHER = "Other fields from the form"
FLAG_MARKS = ("⚠", "!")                 # '!' when the font could not draw the warning sign
BULLET_CID = re.compile(r"^\(cid:\d+\)\s*")             # the bullet glyph, when the PDF font has no text map for it
META = re.compile(r"^(?P<name>.+?)\s*\|\s*Meeting date:\s*(?P<date>\d{2}/\d{2}/\d{4})\s*\|\s*Advisor:\s*(?P<adv>.+)$")


def _paragraphs(cell):
    """Cell text -> (values, flags, bullets). A '•' or a warning sign starts a new paragraph; any other line wraps the one before."""
    values, flags, kind = [], [], None
    for ln in (cell or "").split("\n"):
        s = BULLET_CID.sub("• ", ln.strip(), count=1)
        if not s:
            continue
        if s[0] in FLAG_MARKS and (len(s) == 1 or s[1] == " "):
            flags.append(s[1:].strip())
            kind = "flag"
        elif s.startswith("•"):
            values.append(s[1:].strip())
            kind = "bullet"
        elif kind == "flag" and flags:
            flags[-1] += " " + s
        elif values:
            values[-1] += " " + s
        else:
            values.append(s)
            kind = "value"
    bullets = len(values) > 1 or any(BULLET_CID.sub("• ", ln.strip(), count=1).startswith("•") for ln in (cell or "").split("\n"))
    return values, flags, bullets


def _row(cells):
    label = " ".join((cells[0] or "").split())
    values, flags, bullets = _paragraphs(cells[1] if len(cells) > 1 else "")
    return {"label": label, "values": values, "flags": flags, "bullets": bullets}


def read_pdf(path):
    """-> dict: client, meeting_date, advisor, title_ok, sections [{num,title,blocks:[{sub,rows}]}], closing {title, blocks}, other [rows], stats."""
    import pdfplumber
    sections, closing, other = [], None, []
    state = {"mode": None, "block": None}
    head_lines, title_ok, meta = [], False, None
    with pdfplumber.open(path) as pdf:
        n_pages = len(pdf.pages)
        for page in pdf.pages:
            tables = page.find_tables()
            boxes = [t.bbox for t in tables]

            def outside(obj, boxes=boxes):
                if obj.get("object_type") != "char":
                    return True
                cx, cy = (obj["x0"] + obj["x1"]) / 2, (obj["top"] + obj["bottom"]) / 2
                return not any(b[0] - 1 <= cx <= b[2] + 1 and b[1] - 1 <= cy <= b[3] + 1 for b in boxes)

            events = []
            for ln in page.filter(outside).extract_text_lines(return_chars=True):
                text = ln["text"].strip()
                if text:
                    ch = ln["chars"][0]
                    events.append((ln["top"], "line", text, float(ch.get("size", 0)), "bold" in str(ch.get("fontname", "")).lower()))
            for t in tables:
                events.append((t.bbox[1], "table", t.extract(), 0, False))
            for _, kind, payload, size, bold in sorted(events, key=lambda e: e[0]):
                if kind == "line":
                    m = re.match(r"^(\d{1,2})\.\s+(.+)$", payload)
                    if bold and size >= 13 and m:
                        sec = {"num": int(m.group(1)), "title": m.group(2).strip(), "blocks": []}
                        sections.append(sec)
                        state.update(mode="section", block=None)
                    elif bold and size >= 13 and payload == CLOSING:
                        closing = {"title": CLOSING, "blocks": []}
                        state.update(mode="closing", block=None)
                    elif bold and size >= 13 and payload == OTHER:
                        state.update(mode="other", block=None)
                    elif state["mode"] in ("section",) and bold and size >= 11:
                        blk = {"sub": payload, "rows": []}
                        sections[-1]["blocks"].append(blk)
                        state["block"] = blk
                    elif state["mode"] is None:
                        head_lines.append(payload)
                        mm = META.match(payload)
                        if mm and not meta:
                            meta = mm.groupdict()
                        if payload.strip().upper() == "CLIENT FACT FIND":
                            title_ok = True
                else:
                    rows = [_row(r) for r in payload if r and any(c for c in r)]
                    if state["mode"] == "section":
                        if state["block"] is None:
                            state["block"] = {"sub": "", "rows": []}
                            sections[-1]["blocks"].append(state["block"])
                        state["block"]["rows"] += rows
                    elif state["mode"] == "closing":
                        if not closing["blocks"]:
                            closing["blocks"].append({"sub": "", "rows": []})
                        closing["blocks"][0]["rows"] += rows
                    elif state["mode"] == "other":
                        other += rows
    nrows = sum(len(b["rows"]) for s in sections for b in s["blocks"]) + sum(len(b["rows"]) for b in (closing or {"blocks": []})["blocks"])
    nflags = sum(len(r["flags"]) for s in sections for b in s["blocks"] for r in b["rows"]) + \
        sum(len(r["flags"]) for b in (closing or {"blocks": []})["blocks"] for r in b["rows"])
    name = (meta or {}).get("name", "").strip()
    parts = name.split()
    return {"pages": n_pages, "title_ok": title_ok, "meta": meta, "client_name": name,
            "meeting_date": (meta or {}).get("date"), "advisor": (meta or {}).get("adv"),
            "sections": sections, "closing": closing, "other": other,
            "stats": {"sections": len(sections), "rows": nrows, "flags": nflags, "other_rows": len(other)}}


def layout_problems(ff):
    """Reasons this PDF is NOT the program-drawn Fact Find Transcript (empty list = it is)."""
    out = []
    if not ff.get("title_ok"):
        out.append("the title block 'CLIENT FACT FIND' was not found on page 1")
    if not ff.get("meta"):
        out.append("the line 'Name | Meeting date: DD/MM/YYYY | Advisor: ...' was not found on page 1")
    nums = [s["num"] for s in ff["sections"]]
    if nums != sorted(nums) or len(set(nums)) != len(nums):
        out.append("the section numbers are not in order: %s" % nums)
    for s in ff["sections"]:
        if EXPECTED.get(s["num"]) != s["title"]:
            out.append("section %s is called %r, expected %r" % (s["num"], s["title"], EXPECTED.get(s["num"])))
        if not s["blocks"] or not any(b["rows"] for b in s["blocks"]):
            out.append("section %s %r has no table rows" % (s["num"], s["title"]))
    if len(ff["sections"]) < 6:
        out.append("only %d of the 11 sections were found" % len(ff["sections"]))
    if not ff.get("closing") or not ff["closing"]["blocks"]:
        out.append("the closing section 'Next Steps & Next Meeting' was not found")
    return out


def main():
    ff = read_pdf(sys.argv[1])
    print(json.dumps({k: ff[k] for k in ("client_name", "meeting_date", "advisor", "pages", "stats")}, indent=1))
    probs = layout_problems(ff)
    print("LAYOUT:", "OK" if not probs else "; ".join(probs))


if __name__ == "__main__":
    main()
