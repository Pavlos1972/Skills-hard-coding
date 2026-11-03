#!/usr/bin/env python3
"""Reads the Astute report's text, page by page, and checks that what the chat entered really appears in it.

The Astute (Consolidated Client Portfolio) report is a PDF. This module never guesses its layout: it only (1) extracts the text of each page
with pdfplumber, and (2) answers "does this policy number / figure / date / name appear in the report's own text?". A figure that is not in the
text cannot have come from the report, so it is a red cross. What it cannot prove: that a figure sits on the right policy (attested), and
anything on a page that has no text (a scanned page): the program says which pages those are.
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
        return None if d in self.numbers else "%s: %s is not in the report's text" % (label, w.fmt_money(d))

    def percent(self, label, value):
        if value in (None, ""):
            return None
        d = w.parse_money(str(value).replace("%", ""))
        if d is None:
            return "%s: %r is not a percentage" % (label, value)
        return None if d in self.numbers else "%s: %s%% is not in the report's text" % (label, w.fmt_pct(d))

    def date(self, label, value):
        if value in (None, ""):
            return None
        forms = date_forms(value)
        if not forms:
            return "%s: %r is not a date (enter DD/MM/YYYY, or leave it empty if the report does not show it)" % (label, value)
        return None if any(f in self.flat for f in forms) else "%s: %s is not in the report's text" % (label, value)

    def name(self, label, value):
        if not value:
            return None
        return None if w.norm(value) in self.norm else "%s: %r is not in the report's text" % (label, value)

    def code(self, label, value):
        if not value:
            return None
        return None if alnum(value) and alnum(value) in self.alnum else "%s: %r is not in the report's text" % (label, value)


def _pols(data):
    return data.get("policies") or []


def evidence_problems(data, rep):
    """Everything the chat entered that cannot be found in the report's text (empty list = every entry was found)."""
    ev = Evidence(rep)
    if not ev.has_text:
        return None                                   # nothing to check against: the caller says so (attested)
    out = []

    def add(msg):
        if msg:
            out.append(msg)
    h = data.get("header") or {}
    if h.get("astute_name"):
        add(ev.name("header: the name Astute holds", h["astute_name"]))
    else:
        add(ev.name("header: client name", h.get("client_name")))
    add(ev.code("header: ID number", h.get("id_number")))
    add(ev.date("header: date of birth", h.get("date_of_birth")))
    add(ev.code("header: report reference", h.get("report_reference")))
    add(ev.date("header: report date", h.get("report_date")))
    add(ev.name("header: requested by", h.get("requested_by")))
    for p in data.get("providers") or []:
        add(ev.name("provider %r" % p.get("name"), p.get("name")))
    for p in _pols(data):
        tag = "policy %s" % (p.get("policy_number") or "?")
        add(ev.name(tag + " provider", p.get("provider")))
        add(ev.code(tag + " number", p.get("policy_number")))
        add(ev.name(tag + " product", p.get("product_name")))
        add(ev.name(tag + " status", p.get("status")))
        add(ev.date(tag + " start date", p.get("start_date")))
        for k in ("owner", "life_assured", "premium_payer"):
            add(ev.name(tag + " " + k.replace("_", " "), p.get(k)))
        for b in p.get("beneficiaries") or []:
            add(ev.name(tag + " beneficiary", b.get("name")))
            add(ev.percent(tag + " beneficiary %", b.get("percent")))
        for b in p.get("benefits") or []:
            add(ev.number(tag + " cover for %s" % b.get("name"), b.get("cover_amount")))
        add(ev.number(tag + " premium", p.get("premium")))
        for k, v in (p.get("values") or {}).items():
            if isinstance(v, dict):
                for kk, vv in v.items():
                    add(ev.number(tag + " %s %s" % (k, kk), vv))
            else:
                add(ev.number(tag + " " + k.replace("_", " "), v))
        for f in p.get("fund_allocation") or []:
            add(ev.percent(tag + " allocation to %s" % f.get("fund"), f.get("percent")))
    s2 = data.get("section2") or {}
    for key in ("group_risk", "retirement_fund"):
        for line in (s2.get(key) or {}).get("details") or []:
            for tok in _NUM.finditer(str(line)):
                d = w.parse_money(tok.group(0))
                if d is not None and len(re.sub(r"\D", "", tok.group(0))) >= 3:
                    add(ev.number("%s detail %r" % (key.replace("_", " "), str(line)[:40]), d))
    for k, v in (data.get("report_totals") or {}).items():
        add(ev.number("the report's own total %s" % k, v))
    return out
