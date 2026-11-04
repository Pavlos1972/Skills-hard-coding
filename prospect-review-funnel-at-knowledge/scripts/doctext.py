#!/usr/bin/env python3
"""Plain text of the funnel documents (standard library only): .docx, .xlsx, .md, .txt, .html.

The six documents of the funnel are Word files (STREAMLINED, AT MASTER PLAN, AUTOMATION), an Excel file (AT BUILD REGISTER), a Markdown file (Logic & Flow)
and an HTML page (Flow Comparison). The program reads their text so that a line the chat quotes can be found in the document: a line that is not in the text
cannot have come from the document. It does not understand the layout; it only extracts text (table cells of one row are joined with ' | ').
"""
import re
import zipfile
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def _docx(path):
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    lines = []

    def para_text(p):
        out = []
        for el in p.iter():
            if el.tag == W + "t" and el.text:
                out.append(el.text)
            elif el.tag in (W + "tab",):
                out.append(" ")
            elif el.tag in (W + "br", W + "cr"):
                out.append("\n")
        return "".join(out)

    body = root.find(W + "body")
    for el in (body if body is not None else root):
        if el.tag == W + "p":
            t = para_text(el)
            if t.strip():
                lines.append(t)
        elif el.tag == W + "tbl":
            for tr in el.iter(W + "tr"):
                cells = []
                for tc in tr.findall(W + "tc"):
                    cells.append(" ".join(x for x in (para_text(p) for p in tc.iter(W + "p")) if x.strip()))
                if any(c.strip() for c in cells):
                    lines.append(" | ".join(cells))
    return "\n".join(lines)


def _xlsx(path):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        shared = []
        if "xl/sharedStrings.xml" in names:
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")).iter(S + "si"):
                shared.append("".join(t.text or "" for t in si.iter(S + "t")))
        lines = []
        for name in sorted(n for n in names if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", n)):
            root = ET.fromstring(z.read(name))
            for row in root.iter(S + "row"):
                cells = []
                for c in row.findall(S + "c"):
                    v = c.find(S + "v")
                    t = c.get("t")
                    if t == "s" and v is not None and v.text is not None:
                        cells.append(shared[int(v.text)])
                    elif t == "inlineStr":
                        cells.append("".join(x.text or "" for x in c.iter(S + "t")))
                    elif v is not None and v.text is not None:
                        cells.append(v.text)
                if any(x.strip() for x in cells):
                    lines.append(" | ".join(cells))
    return "\n".join(lines)


def _plain(path):
    import html as _html
    with open(path, encoding="utf-8", errors="replace") as f:
        raw = f.read()
    if path.lower().endswith((".html", ".htm")):
        raw = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw)
        raw = re.sub(r"(?i)<br\s*/?>|</p>|</tr>|</div>|</h\d>|</li>", "\n", raw)
        raw = _html.unescape(re.sub(r"<[^>]+>", " ", raw))
    return "\n".join(" ".join(line.split()) for line in raw.splitlines() if line.strip())


def read(path):
    """The text of the document. Raises ValueError when the file cannot be read as one of the supported kinds."""
    low = path.lower()
    try:
        if low.endswith(".docx"):
            return _docx(path)
        if low.endswith(".xlsx"):
            return _xlsx(path)
        if low.endswith((".md", ".txt", ".html", ".htm")):
            return _plain(path)
    except (zipfile.BadZipFile, KeyError, ET.ParseError) as e:
        raise ValueError("this file is not a readable %s file (%s)" % (low.rsplit(".", 1)[-1], e))
    raise ValueError("unsupported file type (use .docx, .xlsx, .md, .txt or .html; save a PDF or other file as text first)")


if __name__ == "__main__":
    import sys
    print(read(sys.argv[1]))
