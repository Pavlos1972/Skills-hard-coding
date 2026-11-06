#!/usr/bin/env python3
"""Reads the Fact Find form's data file (the JSON the new Fact Find form saves; app = "wr-fact-find") and its saved PDF.

The form is READ-ONLY for this skill (Paul corrects a wrong field in the form himself and saves again; the skill uses the saved value).
A program reads both files, so no value is retyped by Claude.
"""
import datetime as dt
import json
import os
import re
import sys

import wrlib as w


class FormError(Exception):
    """The message is the one line to give Paul."""


STATUSES = ("confirmed", "preset", "empty", "heard", "verify")
TOP_KEYS = ("app", "schema", "created", "modified", "f", "l", "sum", "pa", "unplaced", "claude", "openai")


# ------------------------------------------------------------------ layout knowledge
def layout_keys(lay):
    """(scalar keys, {list name: set of columns | None when any column is allowed}, notes keys)"""
    keys, lists, notes = set(), {}, set()
    for sec in lay["sections"]:
        for g in sec["groups"]:
            for r in g.get("rows", []):
                if r.get("key"):
                    keys.add(r["key"])
                    if r.get("notes"):
                        notes.add(r["key"])
            if g.get("list"):
                lists[g["list"]] = None if g["cols"] == "generic" else {c["col"] for c in g["cols"]}
    for r in lay["closing"]["rows"]:
        keys.add(r["key"])
    return keys, lists, notes


def is_form(raw):
    return isinstance(raw, dict) and raw.get("app") == "wr-fact-find"


def load_raw(path):
    try:
        with open(path, encoding="utf-8-sig") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def tidy(v):
    """Text of a value with the stray spaces taken off (a real first name was saved with a trailing space)."""
    if v is None:
        return ""
    if isinstance(v, bool):
        return "Yes" if v else "No"
    if isinstance(v, (list, tuple)):
        return "; ".join(tidy(x) for x in v if tidy(x))
    return str(v).replace(" ", " ").strip()


# ------------------------------------------------------------------ the company look-up text (Paul, 02/11/2026)
def check_lookup(text, status, lay=None):
    """The form can look up on the web what a company does. Throw the text out when it talks to the reader or is far too long."""
    lay = lay or w.layout()
    rules = lay["lookup"]
    t = tidy(text)
    if not t:
        return {"verdict": "empty", "words": 0, "reasons": [], "status": status}
    reasons = []
    n = w.words(t)
    low = " " + w.norm(t) + " "
    for phrase in rules["chatter"]:
        if " " + w.norm(phrase) + " " in low or w.norm(phrase) in low:
            reasons.append("talks to the reader (%r)" % phrase.strip())
            break
    if "?" in t:
        reasons.append("asks a question")
    if n > rules["max_words"]:
        reasons.append("%d words, a short description is at most about %d" % (n, rules["max_words"]))
    return {"verdict": "thrown_out" if reasons else "clean", "words": n, "reasons": reasons, "status": status}


# ------------------------------------------------------------------ South African ID number, years
def luhn_ok(idno):
    d = w.digits(idno)
    if len(d) != 13:
        return False
    total = 0
    for i, ch in enumerate(reversed(d)):
        n = int(ch)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0


def age_on(born, on):
    return on.year - born.year - ((on.month, on.day) < (born.month, born.day))


def id_facts(idno, meeting, age_hint=None):
    """Date of birth and gender from a South African ID number: first 6 digits YYMMDD; the next four digits below 5000 mean female."""
    d = w.digits(idno)
    out = {"ok": False, "dob": None, "gender": None, "problems": []}
    if len(d) != 13:
        out["problems"].append("an ID number has 13 digits, this has %d" % len(d))
        return out
    yy, mm, dd = int(d[0:2]), int(d[2:4]), int(d[4:6])
    cands = []
    for century in (2000, 1900):
        try:
            born = dt.date(century + yy, mm, dd)
        except ValueError:
            continue
        if born <= meeting:
            cands.append(born)
    if not cands:
        out["problems"].append("the first six digits (%s) are not a real date" % d[:6])
        return out
    pick = None
    if age_hint is not None:
        pick = next((c for c in cands if age_on(c, meeting) == age_hint), None)
    if pick is None:
        pick = cands[0]          # the 2000s when that date is not in the future, otherwise the 1900s
    out["dob"] = pick
    out["ambiguous_century"] = age_hint is None and len(cands) > 1       # both 20yy and 19yy are real dates not in the future
    out["gender"] = "Female" if int(d[6:10]) < 5000 else "Male"
    if not luhn_ok(d):
        out["problems"].append("the ID number's check digit does not match: confirm the number digit for digit")
    out["ok"] = True
    return out


def years_from(value, meeting_year):
    """'Number of years' that holds a year (2015) -> (years, year); anything else -> None."""
    m = re.fullmatch(r"(19\d{2}|20\d{2})", tidy(value))
    if not m or int(m.group(1)) > meeting_year:
        return None
    return meeting_year - int(m.group(1)), int(m.group(1))


# ------------------------------------------------------------------ reading
def read_form(path, lay=None):
    lay = lay or w.layout()
    raw = load_raw(path)
    if raw is None:
        raise FormError("STOP: %s could not be read as a JSON file. Tell Paul in one line." % os.path.basename(path))
    if not is_form(raw):
        raise FormError("STOP: %s is not the Fact Find form's data file (its `app` is %r, not 'wr-fact-find')." % (os.path.basename(path), raw.get("app") if isinstance(raw, dict) else None))
    if str(raw.get("schema")) != lay["schema"]:
        raise FormError("STOP: the Fact Find form's data file says schema %r. This skill knows only schema %s (the form's layout has changed). "
                        "Tell Paul in one line; the skill must be updated once before it can read this file." % (raw.get("schema"), lay["schema"]))
    known, list_cols, _ = layout_keys(lay)
    ign_top, ign_fields = set(lay["ignored"]["top"]), set(lay["ignored"]["fields"])
    f = raw.get("f") if isinstance(raw.get("f"), dict) else {}
    lists_raw = raw.get("l") if isinstance(raw.get("l"), dict) else {}
    out = {"app": raw["app"], "schema": str(raw["schema"]), "file": os.path.basename(path), "sha256": w.sha256_file(path),
           "created": raw.get("created"), "modified": raw.get("modified"), "fields": {}, "lists": {}, "empty_rows": {},
           "statuses": {}, "presets": [], "other_statuses": [], "odd": [], "unknown_fields": [], "unknown_lists": [], "unknown_cols": {},
           "ignored": {}, "top_unknown": []}
    for k in ign_top:
        if k in raw:
            v = raw[k]
            out["ignored"][k] = "ignored, not read (%s)" % (("%d entries" % len(v)) if isinstance(v, (list, dict)) else "present")
    for k in raw:
        if k not in TOP_KEYS:
            out["top_unknown"].append(k)
    for k, cell in f.items():
        if k in ign_fields:
            out["ignored"]["f." + k] = "ignored, not read (the form's own drafted action list is not a source)"
            continue
        if isinstance(cell, dict):
            v, st = tidy(cell.get("v")), tidy(cell.get("st")).lower()
        else:
            v, st = tidy(cell), ""
            out["odd"].append("%s: not saved in the usual {v, st} form" % k)
        if st and st not in STATUSES:
            out["odd"].append("%s: unknown status %r" % (k, st))
        if st == "empty" and v:
            out["odd"].append("%s: marked empty but holds a value (%s): used as populated" % (k, v[:40]))
        populated = bool(v)
        out["fields"][k] = {"v": v, "st": st or "confirmed", "populated": populated}
        if populated:
            out["statuses"][st or "confirmed"] = out["statuses"].get(st or "confirmed", 0) + 1
            if (st or "confirmed") == "preset":
                out["presets"].append(k)
            if st in ("heard", "verify"):
                out["other_statuses"].append(k)
            if k not in known:
                out["unknown_fields"].append(k)
    for name, rows in lists_raw.items():
        if not isinstance(rows, list):
            out["odd"].append("list %s is not a list" % name)
            continue
        if name not in list_cols:
            out["unknown_lists"].append(name)
        clean = []
        for i, row in enumerate(rows):
            d = row.get("d") if isinstance(row, dict) and isinstance(row.get("d"), dict) else (row if isinstance(row, dict) else {})
            st = tidy(row.get("st")).lower() if isinstance(row, dict) else ""
            cells = {c: tidy(v) for c, v in d.items()}
            if not any(cells.values()):
                out["empty_rows"][name] = out["empty_rows"].get(name, 0) + 1
                continue
            clean.append({"index": len(clean), "d": cells, "st": st or "confirmed"})
            allowed = list_cols.get(name)
            if allowed is not None:
                for c, v in cells.items():
                    if v and c not in allowed:
                        out["unknown_cols"].setdefault(name, []).append(c)
        if clean:
            out["lists"][name] = clean
            for r in clean:
                if r["st"] == "preset":
                    out["presets"].append("%s.%d" % (name, r["index"]))
    for name in out["unknown_cols"]:
        out["unknown_cols"][name] = sorted(set(out["unknown_cols"][name]))
    out["client"] = {"first": out["fields"].get("fname", {}).get("v", ""), "surname": out["fields"].get("sname", {}).get("v", "")}
    out["date"] = out["fields"].get("date", {}).get("v", "")
    co = out["fields"].get("co_does")
    out["lookup"] = check_lookup(co["v"] if co else "", co["st"] if co else "", lay)
    return out


def crosscheck_items(form, lay=None):
    """Every populated field and list row, in the order of the layout: what Claude compares with the call (one answer each)."""
    lay = lay or w.layout()
    items = []
    skip = {r.get("key") for sec in lay["sections"] for g in sec["groups"] for r in g.get("rows", []) if r.get("nocross")}
    for sec in lay["sections"]:
        for g in sec["groups"]:
            for r in g.get("rows", []):
                k = r.get("key")
                c = form["fields"].get(k) if k else None
                if not c or not c["populated"] or k in skip or r.get("notes"):
                    continue
                items.append({"key": k, "label": r["label"], "value": c["v"], "status": c["st"], "section": sec["title"], "answer": None})
            if g.get("list") and g["list"] in form["lists"]:
                for row in form["lists"][g["list"]]:
                    desc = " | ".join(v for v in row["d"].values() if v)[:90]
                    items.append({"key": "%s.%d" % (g["list"], row["index"]), "label": "%s %d" % (g["item"], row["index"] + 1), "value": desc,
                                  "status": row["st"], "section": sec["title"], "answer": None, "row": True})
    for r in lay["closing"]["rows"]:
        c = form["fields"].get(r["key"])
        if c and c["populated"]:
            items.append({"key": r["key"], "label": r["label"], "value": c["v"], "status": c["st"], "section": lay["closing"]["title"], "answer": None})
    return items


# ------------------------------------------------------------------ command line


# ------------------------------------------------------------------ the form's saved PDF
TRIVIAL = {"yes", "no", "y", "n", "true", "false", "none", "nil", "n a", "na"}
AMOUNT_RX = re.compile(r"(?<![\d.,])R?\s?\d{1,3}(?:[ ,]\d{3})+(?:[.,]\d{1,2})?(?![\d])|(?<![\d.,])R?\s?\d+(?:[.,]\d{1,2})?(?![\d])")


def pdf_file_problems(path):
    """A PDF is real bytes, whole: it starts with %PDF- and ends with %%EOF. A text copy or a cut-off copy (what Microsoft 365 returns) is never accepted."""
    try:
        size = os.path.getsize(path)
        with open(path, "rb") as fh:
            head = fh.read(8)
            fh.seek(max(0, size - 2048))
            tail = fh.read()
    except OSError as e:
        return ["the PDF cannot be opened (%s)" % e]
    out = []
    if not head.startswith(b"%PDF-"):
        out.append("it does not start like a PDF file (it may be text)")
    if b"%%EOF" not in tail:
        out.append("it does not end like a whole PDF file (cut off? %d bytes)" % size)
    return out


def pdf_text(path):
    import subprocess
    try:
        r = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True)
    except OSError:
        return None
    return r.stdout if r.returncode == 0 else None


def _compact(s):
    return re.sub(r"[\s,]+", "", str(s)).lower().replace("\u2013", "-")


def pdf_amounts(text):
    """Every amount written in the PDF's text, as exact Decimals (so R 45 000.00 is never 'found' inside R 1 450 000.00)."""
    out = set()
    for m in AMOUNT_RX.finditer(text):
        d = w.parse_money(m.group(0))
        if d is not None:
            out.add(d)
    return out


RAND_RX = re.compile(r"(?<![A-Za-z\d])R\s?\d{1,3}(?:[ ,]\d{3})+(?:[.,]\d{1,2})?(?!\d)|(?<![A-Za-z\d])R\s?\d+(?:[.,]\d{1,2})?(?!\d)")


def rand_amounts(text):
    """Every amount written with an R in this text, as exact non-zero Decimals."""
    out = set()
    for m in RAND_RX.finditer(text or ""):
        d = w.parse_money(m.group(0))
        if d is not None and d != 0:
            out.add(d)
    return out


def pdf_only_amounts(form, text):
    """The amounts the form's PDF shows (written with an R) that are in NO value of the data file: the form computes them (for example the Risk Calculation),
    so only the PDF holds them. Each one must end up in the document or be reviewed (a missed one is a missed fact)."""
    have = set()
    for c in form["fields"].values():
        have |= rand_amounts(c["v"])
        d = w.parse_money(c["v"]) if c["populated"] else None
        if d is not None:
            have.add(d)
    for rows in form["lists"].values():
        for r in rows:
            for v in r["d"].values():
                have |= rand_amounts(v)
                d = w.parse_money(v) if v else None
                if d is not None:
                    have.add(d)
    return sorted("%s" % x for x in rand_amounts(text) if x not in have)


def value_in_pdf(value, text, ntext=None, ctext=None, amounts=None, money=False):
    """Is this value of the data file in the PDF's text? Amounts are compared as exact amounts; other values whole word for whole word
    (so Pat is not found inside Patricia, and 65 is not found inside 1650)."""
    v = tidy(value)
    ntext = ntext if ntext is not None else w.norm(text)
    if not v or w.norm(v) in TRIVIAL or len(w.norm(v)) < 2:
        return True
    m = w.parse_money(v)
    looks_money = m is not None and (money or v.upper().startswith("R"))
    if looks_money:
        return m in (amounts if amounts is not None else pdf_amounts(text))
    padded = " %s " % ntext
    nv = w.norm(v)
    if " %s " % nv in padded:
        return True
    if re.fullmatch(r"[\d ./+-]+", v):                      # a number, date or phone number: the same digits as a whole run
        runs = {w.digits(x) for x in re.findall(r"\+?\d[\d ./-]*\d|\d", text)}
        return w.digits(v) in runs
    toks = nv.split()
    return len(toks) > 8 and " ".join(toks[:8]) in ntext


def pdf_check(form, text, lay=None):
    lay = lay or w.layout()
    ntext, amounts = w.norm(text), pdf_amounts(text)
    labels = {r["key"]: r["label"] for sec in lay["sections"] for g in sec["groups"] for r in g.get("rows", []) if r.get("key")}
    labels.update({r["key"]: r["label"] for r in lay["closing"]["rows"]})
    kinds = {r["key"]: r.get("kind") for sec in lay["sections"] for g in sec["groups"] for r in g.get("rows", []) if r.get("key")}
    colkinds = {(g["list"], c["col"]): c.get("kind") for sec in lay["sections"] for g in sec["groups"] if g.get("list") and isinstance(g["cols"], list) for c in g["cols"]}
    checked, missing = 0, []
    for k, c in form["fields"].items():
        if not c["populated"]:
            continue
        checked += 1
        if k == "co_does" and form["lookup"]["verdict"] == "thrown_out":
            continue
        if not value_in_pdf(c["v"], text, ntext, None, amounts, kinds.get(k) == "money"):
            missing.append({"key": k, "label": labels.get(k, k), "value": c["v"]})
    for name, rows in form["lists"].items():
        for r in rows:
            for col, v in r["d"].items():
                if v:
                    checked += 1
                    if not value_in_pdf(v, text, ntext, None, amounts, colkinds.get((name, col)) == "money"):
                        missing.append({"key": "%s.%d.%s" % (name, r["index"], col), "label": "%s %d: %s" % (name, r["index"] + 1, col), "value": v})
    return checked, missing


def pdf_identity_problems(form, text):
    """The PDF must be THIS client's: the surname and the form's date have to be in its text."""
    nt = " %s " % w.norm(text)
    out = []
    sur = w.last_name_token(form["client"]["surname"])
    if sur and " %s " % sur not in nt:
        out.append("the client's surname (%s) is not in the PDF's text" % form["client"]["surname"])
    d = form.get("date") or ""
    if d and d not in text and w.norm(d) not in nt:
        out.append("the form's Date completed (%s) is not in the PDF's text" % d)
    return out


CHATTER_RX = re.compile(r"^(all right|alright|okay|ok|right|let'?s move on|i'?ve taken note|i can move on|moving on|thanks?|thank you)\b", re.I)
DANGLING = {"the", "a", "an", "and", "to", "of", "for", "with", "in", "on", "at", "by", "from", "is", "are", "was", "or", "that", "this"}


def note_problems(form):
    """Notes of the form that need cleaning: chatter lines, a note that stops in the middle of a sentence, a line that only repeats another field."""
    out = []
    flat = {k: w.norm(c["v"]) for k, c in form["fields"].items() if c["populated"]}
    for k, c in form["fields"].items():
        if not c["populated"] or not (k.startswith("n_") or k.endswith("_notes") or k in ("d_desc", "h_notes")):
            continue
        lines = [ln.strip(" -\u2022\t") for ln in c["v"].split("\n") if ln.strip()]
        for ln in lines:
            if CHATTER_RX.search(ln) or ("move on" in ln.lower() and len(ln) < 70):
                out.append("%s: chatter, not a fact: %r" % (k, ln[:60]))
            elif len(ln) >= 25:
                nl = w.norm(ln)
                other = [kk for kk, v in flat.items() if kk != k and nl in v]
                if other:
                    out.append("%s: a line that only repeats %s: %r" % (k, other[0], ln[:50]))
        last = lines[-1].split()[-1].lower().strip(".,;:") if lines and lines[-1].split() else ""
        if lines and last in DANGLING and not lines[-1].rstrip().endswith((".", "!", "?", ")")):
            out.append("%s: stops in the middle of a sentence: %r" % (k, lines[-1][-40:]))
    return out


def _label_before(line, amount):
    """The PDF's own label for an amount: the words between the previous amount (or the start of the line) and this amount."""
    prev = 0
    for m in RAND_RX.finditer(line):
        d = w.parse_money(m.group(0))
        if d is not None and str(d) == amount:
            seg = line[prev:m.start()]
            chunks = [c for c in re.split(r"\s{3,}", seg.strip()) if c.strip()]
            return (chunks[-1] if chunks else seg).strip(" :-") or " ".join(line.split())[:80]
        prev = m.end()
    return " ".join(line.split())[:80]


def pdf_report(form, text, lay=None):
    """What the form's PDF adds to its data file: values the data file could not be found in the PDF (not_found), and the amounts only the PDF holds because the form works them out (pdf_only, each with the PDF's own label)."""
    checked, missing = pdf_check(form, text, lay)
    only = pdf_only_amounts(form, text)
    labels = {}
    for amt in only:
        for ln in text.splitlines():
            if amt in {str(x) for x in rand_amounts(ln)}:
                labels[amt] = _label_before(ln, amt)
                break
    return {"checked": checked, "not_found": missing, "pdf_only": only, "pdf_only_labels": labels, "identity": pdf_identity_problems(form, text)}


def read_form_into_run(path, run):
    """Read the form's data file for this run (writes form_read.json and a saved copy). Raises FormError with the one line for Paul."""
    import shutil
    rj = w.load_json(os.path.join(run, w.RUN), "run.json (run `run.py start` first)")
    form = read_form(path, w.layout())
    problems = []
    cl = rj["client"]
    if not w.same_person(form["client"]["first"], form["client"]["surname"], cl["first"], cl["surname"]):
        problems.append("the form is for %s %s but this run is for %s %s" % (form["client"]["first"], form["client"]["surname"], cl["first"], cl["surname"]))
    if form["date"] != rj["date"]:
        problems.append("the form's Date completed is %s but the meeting date is %s" % (form["date"] or "empty", rj["date"]))
    if problems:
        raise FormError("STOP. This is not the right form file for this run: " + "; ".join(problems) + ". Find the right one (it is recognised by its content), or tell Paul.")
    shutil.copyfile(path, os.path.join(run, "form_source.json"))
    w.save_json(os.path.join(run, w.FORM), form)
    return form
