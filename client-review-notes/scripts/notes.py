"""Reads raw Outlook contact notes: splits them into dated entries and pulls out the tokens a record must keep (dates, amounts, percentages, numbers,
contract-like codes, ids, emails, links, names and abbreviations). No client data is kept in this file. It never guesses a layout: when it cannot find
dated entries it says so and treats the whole note as ONE entry (a weaker check, and the audit says so).
"""
import re
from datetime import date

import wrlib as w

MONTHS = {"jan": 1, "january": 1, "feb": 2, "february": 2, "mar": 3, "march": 3, "apr": 4, "april": 4, "may": 5, "jun": 6, "june": 6, "jul": 7, "july": 7, "aug": 8, "august": 8,
          "sep": 9, "sept": 9, "september": 9, "oct": 10, "october": 10, "nov": 11, "november": 11, "dec": 12, "december": 12}
_D1 = re.compile(r"\b(\d{1,2})[/.\-](\d{1,2})[/.\-](\d{4}|\d{2})\b")
_D2 = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")
_D3 = re.compile(r"\b(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]{3,9})\.?,?\s+(\d{4})\b")
_D4 = re.compile(r"\b([A-Za-z]{3,9})\.?\s+(\d{4})\b")
_TIME = re.compile(r"\b([01]?\d|2[0-3]):[0-5]\d(?::[0-5]\d)?\b")
_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_URL = re.compile(r"https?://[^\s)\]>]+")
_AMOUNT = re.compile(r"\bR\s?\d[\d ,]*(?:\.\d+)?\s?(?:k|m)?\b", re.I)
_PCT = re.compile(r"\b\d+(?:\.\d+)?\s?%")
_CODE = re.compile(r"\b(?=[A-Za-z0-9\-/]*\d)[A-Za-z0-9][A-Za-z0-9\-/]{4,}\b")
_NUM = re.compile(r"\b\d{2,}\b")
_CAP = re.compile(r"\b[A-Z][a-z]{2,}\b")
_ALLCAPS = re.compile(r"\b[A-Z]{2,}\b")
_SCI = re.compile(r"\b\d(?:\.\d+)?[eE]\+?\d+\b")


def _year(y):
    y = int(y)
    return y if y >= 100 else (2000 + y if y < 70 else 1900 + y)


def find_dates(text):
    """[(start, end, key, precision)] key 'YYYY-MM-DD' or 'YYYY-MM'; a span matched by a fuller date is not matched again."""
    out, taken = [], []

    def free(s, e):
        return not any(s < te and e > ts for ts, te in taken)

    def add(m, key, prec):
        if free(m.start(), m.end()):
            taken.append((m.start(), m.end()))
            out.append((m.start(), m.end(), key, prec))
    for m in _D2.finditer(text):
        try:
            date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            add(m, "%04d-%02d-%02d" % (int(m.group(1)), int(m.group(2)), int(m.group(3))), "day")
        except ValueError:
            pass
    for m in _D1.finditer(text):
        try:
            y = _year(m.group(3))
            date(y, int(m.group(2)), int(m.group(1)))
            add(m, "%04d-%02d-%02d" % (y, int(m.group(2)), int(m.group(1))), "day")
        except ValueError:
            pass
    for m in _D3.finditer(text):
        mo = MONTHS.get(m.group(2).lower())
        if mo:
            try:
                date(int(m.group(3)), mo, int(m.group(1)))
                add(m, "%04d-%02d-%02d" % (int(m.group(3)), mo, int(m.group(1))), "day")
            except ValueError:
                pass
    for m in _D4.finditer(text):
        mo = MONTHS.get(m.group(1).lower())
        if mo and 1900 <= int(m.group(2)) <= 2100:
            add(m, "%04d-%02d" % (int(m.group(2)), mo), "month")
    return sorted(out)


def heading(key, months):
    """BOLD ALL CAPS heading text from a date key: '14 FEBRUARY 2022' (day) or 'MARCH 2024' (month only)."""
    p = key.split("-")
    return ("%d %s %s" % (int(p[2]), months[int(p[1]) - 1], p[0])) if len(p) == 3 else "%s %s" % (months[int(p[1]) - 1], p[0])


def _line_date(line):
    """The date a line STARTS with (after bullets, bold marks and brackets), or None."""
    s = re.sub(r"^[\s\[\]\(\)\*#>\-•_|]+", "", line)
    for st, en, key, prec in find_dates(s[:40]):
        if st <= 1:
            return key, prec, en
    return None


def split_entries(text):
    """Dated entries: [{"n", "key", "precision", "text", "line"}]. Entry 0 holds undated text before the first dated line. Fewer than 2 dated lines: ONE entry."""
    lines = text.split("\n")
    starts = []
    for i, ln in enumerate(lines):
        d = _line_date(ln)
        if d:
            starts.append((i, d))
    if len(starts) < 2:
        return [{"n": 1, "key": None, "precision": None, "text": text, "line": 1}], False
    out = []
    if starts[0][0] > 0 and "\n".join(lines[:starts[0][0]]).strip():
        out.append({"n": 0, "key": None, "precision": None, "text": "\n".join(lines[:starts[0][0]]), "line": 1})
    for k, (i, (key, prec, _e)) in enumerate(starts):
        j = starts[k + 1][0] if k + 1 < len(starts) else len(lines)
        out.append({"n": k + 1, "key": key, "precision": prec, "text": "\n".join(lines[i:j]), "line": i + 1})
    return out, True


def parts(text, size):
    """The text in parts of about `size` characters, cut at line ends."""
    out, cur = [], ""
    for ln in text.split("\n"):
        if cur and len(cur) + len(ln) + 1 > size:
            out.append(cur)
            cur = ""
        cur += ln + "\n"
    if cur.strip():
        out.append(cur)
    return out or [""]


def norm_code(s):
    return re.sub(r"[^0-9a-z]", "", s.lower())


def norm_amount(s):
    v = "r" + re.sub(r"[ ,]", "", s[1:].strip().lower())
    return re.sub(r"\.0+$", "", v)


def tokens(text, stop=()):
    """{kind: set(normalised token)} for the things a record must keep."""
    t = text
    out = {"date": set(), "email": set(), "url": set(), "amount": set(), "percent": set(), "code": set(), "number": set(), "name": set()}
    for st, en, key, prec in reversed(find_dates(t)):
        out["date"].add(key)
        t = t[:st] + " " + t[en:]
    t = _TIME.sub(" ", t)
    t = _SCI.sub(" ", t)
    for m in _URL.finditer(t):
        out["url"].add(m.group(0).rstrip(".,;").lower())
    t = _URL.sub(" ", t)
    for m in _EMAIL.finditer(t):
        out["email"].add(m.group(0).lower())
    t = _EMAIL.sub(" ", t)
    for m in _AMOUNT.finditer(t):
        out["amount"].add(norm_amount(m.group(0).strip()))
    t = _AMOUNT.sub(" ", t)
    for m in _PCT.finditer(t):
        out["percent"].add(re.sub(r"\s", "", m.group(0)))
    t = _PCT.sub(" ", t)
    for m in _CODE.finditer(t):
        out["code"].add(norm_code(m.group(0)))
    t = _CODE.sub(" ", t)
    for m in _NUM.finditer(t):
        out["number"].add(m.group(0))
    stop = set(stop)
    for ln in t.split("\n"):
        for m in _CAP.finditer(ln):
            before = ln[:m.start()].rstrip()
            if before == "" or before[-1] in ".!?:-•*#|>[(\"'":
                continue
            if m.group(0) not in stop:
                out["name"].add(m.group(0).lower())
        for m in _ALLCAPS.finditer(ln):
            if m.group(0) not in stop:
                out["name"].add(m.group(0).lower())
    return out


def flat(tok):
    """A readable list of 'kind: value' for a token dict."""
    return ["%s: %s" % (k, v) for k in ("date", "amount", "percent", "code", "number", "email", "url", "name") for v in sorted(tok[k])]


def _edit1(a, b):
    """True when a and b differ by one substitution, insertion, deletion or adjacent swap."""
    if a == b:
        return False
    if len(a) == len(b):
        d = [i for i in range(len(a)) if a[i] != b[i]]
        return len(d) == 1 or (len(d) == 2 and d[1] == d[0] + 1 and a[d[0]] == b[d[1]] and a[d[1]] == b[d[0]])
    if abs(len(a) - len(b)) == 1:
        s, l = (a, b) if len(a) < len(b) else (b, a)
        return any(l[:i] + l[i + 1:] == s for i in range(len(l)))
    return False


def id_check(d13):
    tot = 0
    for i, ch in enumerate(d13[:12]):
        x = int(ch)
        if i % 2:
            x *= 2
            x = x - 9 if x > 9 else x
        tot += x
    return (10 - tot % 10) % 10 == int(d13[12])


def raw_flags(text, entries, recognised, repeats):
    """Flags found in the raw notes themselves: [str]. Shown at the top of Notes by the program."""
    out = []
    codes = sorted({norm_code(m.group(0)) for m in _CODE.finditer(text) if len(norm_code(m.group(0))) >= 6})
    shown = set()
    for i, a in enumerate(codes):
        for b in codes[i + 1:]:
            if _edit1(a, b) and (a, b) not in shown:
                shown.add((a, b))
                out.append("apparent typo: the numbers %s and %s differ by one character" % (a, b))
    for m in _SCI.finditer(text):
        out.append("a number in scientific notation (%s) is probably imprecise: not presented as exact" % m.group(0))
    for m in re.finditer(r"\b\d{13}\b", text):
        if not id_check(m.group(0)):
            out.append("an ID-like number (%s) fails its check digit: possibly mistyped" % ("•••" + m.group(0)[-4:]))
    stamps = {}
    for m in re.finditer(r"\b(\d{1,2}[/.\-]\d{1,2}[/.\-]\d{2,4}|\d{4}-\d{2}-\d{2})[ T]+(\d{1,2}:\d{2})", text):
        stamps[m.group(0)] = stamps.get(m.group(0), 0) + 1
    for k, n in stamps.items():
        if n >= repeats:
            out.append("%d entries carry the same timestamp (%s): it looks system-generated, not an event date" % (n, k))
    if not recognised:
        out.append("the notes carry no recognisable dated entries: the coverage check is over the whole note")
    return out
