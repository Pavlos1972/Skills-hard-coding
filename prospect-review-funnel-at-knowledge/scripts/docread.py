#!/usr/bin/env python3
"""Reads a client document's text (PDF or HTML/text), page by page, and checks that what the chat entered really appears in it.

This module never guesses a layout: it only (1) extracts the text of each page with pdfplumber, and (2) answers "does this figure / date / name
appear in the document's own text?". A figure that is not in the text cannot have come from the document, so it is a red cross. What it cannot
prove: that a figure sits in the right place or column (attested), and anything on a page with no text (a scanned page): the program says which.
"""
import datetime as dt
import re
from decimal import Decimal

import wrlib as w

MIN_TEXT = 25                    # a page with fewer characters than this is treated as an image-only page


def read_pdf(path):
    """{"page_count", "pages": [{"n", "text", "chars"}], "image_only": [n, ...]}. Raises ValueError if it is not a readable PDF."""
    with open(path, "rb") as f:
        if not f.read(5).startswith(b"%PDF"):
            raise ValueError("this file is not a PDF (some 'PDF' files are zipped page images: extract and view every page)")
    import pdfplumber
    pages = []
    with pdfplumber.open(path) as pdf:
        for i, pg in enumerate(pdf.pages, 1):
            text = pg.extract_text() or ""
            pages.append({"n": i, "text": text, "chars": len(text.strip())})
    if not pages:
        raise ValueError("the PDF has no pages")
    return {"page_count": len(pages), "pages": pages, "image_only": [p["n"] for p in pages if p["chars"] < MIN_TEXT]}


def full_text(rep):
    return "\n".join(p["text"] for p in rep["pages"])


_NUM = re.compile(r"\d{1,3}(?:[  ,]\d{3})+(?:[.,]\d{1,2})?|\d+(?:[.,]\d{1,2})?")


def numbers_in(text):
    """Every number in the text as a Decimal (grouped thousands, a decimal comma or point)."""
    out = set()
    for m in _NUM.finditer(text.replace(" ", " ")):
        tok = m.group(0)
        d = w.parse_money(tok)
        if d is not None:
            out.add(d)
        plain = re.sub(r"\D", "", tok)
        if plain and len(plain) <= 12:
            out.add(Decimal(plain))
    return out


def alnum(s):
    return re.sub(r"[^0-9a-z]", "", str(s).lower())


def date_forms(text):
    """The ways a DD/MM/YYYY date may be printed in the report."""
    d = w.parse_date(text)
    if d is None:
        return []
    forms = ["%d/%m/%Y", "%Y/%m/%d", "%d-%m-%Y", "%Y-%m-%d", "%d.%m.%Y", "%d %b %Y", "%d %B %Y", "%Y%m%d", "%d%m%Y", "%b %d, %Y", "%B %d, %Y"]
    out = {d.strftime(f).lower() for f in forms}
    out |= {d.strftime(f).lower().lstrip("0") for f in forms}
    return sorted(out)


class Evidence:
    """Answers 'is this in the report?' against the extracted text."""

    def __init__(self, rep):
        self.text = full_text(rep)
        self.norm = w.norm(self.text)
        self.alnum = alnum(self.text)
        self.flat = " ".join(self.text.lower().split())
        self.numbers = numbers_in(self.text)
        self.has_text = len(self.text.strip()) >= MIN_TEXT
        self.image_only = rep["image_only"]

    def number(self, label, value):
        if value in (None, ""):
            return None
        d = w.parse_money(value) if not isinstance(value, Decimal) else value
        if d is None:
            return "%s: %r is not an amount" % (label, value)
        return None if d in self.numbers else "%s: %s is not in the document's text" % (label, w.fmt_money(d))

    def percent(self, label, value):
        if value in (None, ""):
            return None
        d = w.parse_money(str(value).replace("%", ""))
        if d is None:
            return "%s: %r is not a percentage" % (label, value)
        return None if d in self.numbers else "%s: %s%% is not in the document's text" % (label, w.fmt_pct(d))

    def exact_percent(self, label, value):
        """A percentage with ITS OWN decimals (0.733 is not 0.73): the digits must appear in the text exactly, point or comma."""
        if value in (None, ""):
            return "%s: a percentage is needed" % label
        t = str(value).replace("%", "").strip().replace(" ", "")
        if not re.fullmatch(r"\d+(?:[.,]\d+)?", t):
            return "%s: %r is not a percentage" % (label, value)
        pat = r"(?<![\d.,])" + re.escape(t.replace(",", ".")).replace(r"\.", "[.,]") + r"(?!\d)"
        return None if re.search(pat, self.text) else "%s: %s%% is not in the document's text" % (label, t)

    def date(self, label, value):
        if value in (None, ""):
            return None
        forms = date_forms(value)
        if not forms:
            return "%s: %r is not a date (enter DD/MM/YYYY, or leave it empty if the report does not show it)" % (label, value)
        return None if any(f in self.flat for f in forms) else "%s: %s is not in the document's text" % (label, value)

    def name(self, label, value):
        if not value:
            return None
        return None if w.norm(value) in self.norm else "%s: %r is not in the document's text" % (label, value)

    def code(self, label, value):
        if not value:
            return None
        return None if alnum(value) and alnum(value) in self.alnum else "%s: %r is not in the document's text" % (label, value)


import html as _html


def read_text_file(path):
    """An .html or .txt document as one 'page' of plain text (tags removed)."""
    with open(path, encoding="utf-8", errors="replace") as f:
        raw = f.read()
    if path.lower().endswith((".html", ".htm")):
        raw = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw)
        raw = re.sub(r"(?i)<br\s*/?>|</p>|</tr>|</div>|</h\d>", "\n", raw)
        raw = _html.unescape(re.sub(r"<[^>]+>", " ", raw))
    text = "\n".join(" ".join(line.split()) for line in raw.splitlines() if line.strip())
    return {"page_count": 1, "pages": [{"n": 1, "text": text, "chars": len(text)}], "image_only": []}


def read_document(path):
    return read_text_file(path) if path.lower().endswith((".html", ".htm", ".txt")) else read_pdf(path)
