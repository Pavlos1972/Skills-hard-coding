#!/usr/bin/env python3
"""Reads a Teams meeting transcript (a .docx, the connector's .vtt text, or plain text), checks that it is complete, and can write a plain .docx.

  trread.py <file>        prints what the reader found (for a quick look)

A transcript is COMPLETE (Paul, 03/11/2026) when its last time stamp is within 2 minutes of the meeting length, and no gap between two
time stamps is longer than 10 minutes. The header (meeting title, date, length) is read from the file; a .vtt file has no header, so there
the header comes from the meeting record (run.py meeting). Standard library only.
"""
import datetime as dt
import os
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from xml.sax.saxutils import escape

import wrlib as w

TS_ARROW = re.compile(r"^\s*(\d{1,2}):(\d{1,2}):(\d{1,2})(?:[.,]\d+)?\s*-->")
TS_START = re.compile(r"^\s*(\d{1,2}):(\d{2})(?::(\d{2}))?(?:[.,]\d+)?(?!\d)")
NAME_WORD = r"(?:[A-Z][\w'’-]*|van|de|der|den|la|le|du|di|von)"
TS_END = re.compile(r"^" + NAME_WORD + r"(?:\s+" + NAME_WORD + r"){0,4}\s+(\d{1,2}):(\d{2})(?::(\d{2}))?\s*$")
DURATION = re.compile(r"(?i)(?:duration|length)\W{0,5}(?:(\d+)\s*h\w*)?\s*(?:(\d+)\s*m\w*)?\s*(?:(\d+)\s*s\w*)?")
TITLE = re.compile(r"(?i)^\s*(?:meeting\s+)?title\s*[:\-]\s*(.+)$")
MONTHS = {m: i for i, m in enumerate(["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"], 1)}


def ts_seconds(line):
    m = TS_ARROW.match(line)
    if m:
        return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
    m = TS_START.match(line) or TS_END.match(line)
    if not m:
        return None
    a, b, c = int(m.group(1)), int(m.group(2)), m.group(3)
    return a * 60 + b if c is None else a * 3600 + b * 60 + int(c)


def parse_length(text):
    """'1h 36m 2s' / 'Duration: 16m 30s' / '1:36:02' -> seconds, or None."""
    m = DURATION.search(text or "") or DURATION.search("duration " + (text or ""))
    if m:
        h, mi, s = (int(x) if x else 0 for x in m.groups())
        if h or mi or s:
            return h * 3600 + mi * 60 + s
    m = re.fullmatch(r"\s*(\d{1,2}):(\d{2}):(\d{2})\s*", text or "")
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3)) if m else None


def find_date(lines):
    """The meeting date in the header lines: DD/MM/YYYY, YYYY-MM-DD or '5 October 2026'."""
    for ln in lines:
        m = re.search(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b", ln)
        if m:
            try:
                return dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
            except ValueError:
                pass
        m = re.search(r"\b(\d{4})-(\d{2})-(\d{2})\b", ln)
        if m:
            try:
                return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            except ValueError:
                pass
        m = re.search(r"\b(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})\b", ln)
        if m and m.group(2).lower() in MONTHS:
            try:
                return dt.date(int(m.group(3)), MONTHS[m.group(2).lower()], int(m.group(1)))
            except ValueError:
                pass
    return None


def read_docx_lines(path):
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    out = []
    for p in root.iter(ns + "p"):
        out.append("".join(t.text or "" for t in p.iter(ns + "t")))
    return out


def read_file(path):
    """-> (kind, lines). kind: 'docx' | 'vtt' | 'text'."""
    if zipfile.is_zipfile(path):
        return "docx", read_docx_lines(path)
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read().replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    return ("vtt" if text.lstrip("﻿").lstrip().startswith("WEBVTT") else "text"), lines


def analyse(kind, lines, meeting=None):
    """Everything the checker needs: header, time stamps, completeness. meeting = the record from run.py meeting (or None)."""
    head = lines[:15]
    title = next((m.group(1).strip() for m in (TITLE.match(l) for l in head) if m), None)
    if title is None and kind == "docx":
        title = next((l.strip() for l in head if l.strip()), None)
    hdate = find_date(head)
    hdur = None
    for l in head:
        m = DURATION.search(l)
        if m and any(m.groups()):
            hdur = parse_length(l)
            break
    stamps = []
    top = -1
    for i, l in enumerate(lines, 1):
        s = ts_seconds(l)
        if s is not None and s >= top:
            stamps.append((i, s))
            top = s
    m = meeting or {}
    return {"kind": kind, "lines": len(lines), "title": title, "date": hdate.strftime("%d/%m/%Y") if hdate else None, "length_s": hdur,
            "meeting_title": m.get("title"), "meeting_date": m.get("date"), "meeting_length_s": m.get("length_s"),
            "stamps": len(stamps), "first_s": stamps[0][1] if stamps else None, "last_s": stamps[-1][1] if stamps else None,
            "gaps": [(a[1], b[1]) for a, b in zip(stamps, stamps[1:]) if b[1] - a[1] > w.JUMP_S]}


def completeness(a):
    """-> list of problems (empty = complete)."""
    out = []
    if a["stamps"] < 2:
        out.append("fewer than 2 time stamps could be read, so completeness cannot be checked")
        return out
    length = a["length_s"] if a["length_s"] is not None else a["meeting_length_s"]
    if length is None:
        out.append("no meeting length: the file states none and the meeting record has none")
    else:
        if a["last_s"] < length - w.TOLERANCE_S:
            out.append("incomplete: the last time stamp is %s but the meeting length is %s (%s missing)" % (w.fmt_hms(a["last_s"]), w.fmt_hms(length), w.fmt_hms(length - a["last_s"])))
        if a["last_s"] > length + w.TOLERANCE_S:
            out.append("the last time stamp %s is later than the meeting length %s" % (w.fmt_hms(a["last_s"]), w.fmt_hms(length)))
        if a["length_s"] is not None and a["meeting_length_s"] is not None and abs(a["length_s"] - a["meeting_length_s"]) > w.TOLERANCE_S:
            out.append("the file states a length of %s but the meeting record says %s" % (w.fmt_hms(a["length_s"]), w.fmt_hms(a["meeting_length_s"])))
    for s1, s2 in a["gaps"]:
        out.append("gap of %s between time stamps %s and %s" % (w.fmt_hms(s2 - s1), w.fmt_hms(s1), w.fmt_hms(s2)))
    return out


def header_problems(a):
    """-> list of problems with the header (title and date)."""
    out = []
    title = a["title"] or a["meeting_title"]
    if not title:
        out.append("no meeting title in the file or in the meeting record")
    date = a["date"] or a["meeting_date"]
    if not date:
        out.append("no meeting date in the file or in the meeting record")
    elif a["meeting_date"] and a["date"] and a["date"] != a["meeting_date"]:
        out.append("the file's date %s differs from the meeting record's date %s" % (a["date"], a["meeting_date"]))
    return out


# ---------------------------------------------------------------- writing a plain .docx (from a .vtt, when the connector gives text)
def vtt_to_lines(lines, meeting):
    """A .vtt transcript -> the lines of a Teams-style transcript: header, then 'H:MM:SS Speaker' and the words."""
    out = ["Meeting title: %s" % meeting["title"], "Meeting started: %s" % meeting["started"], "Duration: %s" % meeting["length_text"], ""]
    i = 0
    while i < len(lines):
        m = TS_ARROW.match(lines[i])
        if m:
            sec = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
            body = []
            i += 1
            while i < len(lines) and lines[i].strip():
                body.append(lines[i].strip())
                i += 1
            speaker, words = "Speaker", []
            for b in body:
                mv = re.match(r"^<v\s+([^>]+)>(.*?)(?:</v>)?$", b)
                if mv:
                    speaker = mv.group(1).strip()
                    words.append(mv.group(2).strip())
                else:
                    words.append(re.sub(r"<[^>]+>", "", b))
            out += ["%s %s" % (w.fmt_hms(sec), speaker), " ".join(x for x in words if x), ""]
        else:
            i += 1
    return out


def write_docx(path, lines):
    """A minimal, valid .docx: one paragraph per line."""
    body = "".join('<w:p><w:r><w:t xml:space="preserve">%s</w:t></w:r></w:p>' % escape(l) for l in lines)
    doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
           "<w:body>%s</w:body></w:document>" % body)
    ctypes = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
              '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
              '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ctypes)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/document.xml", doc)


def main():
    kind, lines = read_file(sys.argv[1])
    a = analyse(kind, lines)
    print({k: v for k, v in a.items() if v is not None})
    print("COMPLETE" if not completeness(a) else "; ".join(completeness(a)))


if __name__ == "__main__":
    main()
