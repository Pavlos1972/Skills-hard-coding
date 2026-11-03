#!/usr/bin/env python3
"""Reads the Fact Find form's data file (the JSON the new Fact Find form saves; app = "wr-fact-find").

  ffform.py identify <file> [<file> ...]      which of these files is the form's data file (by what is INSIDE, never by name)
  ffform.py read <file> <run_dir> [--again]   read it for this run: schema check, statuses, trimming, the look-up check,
                                              what is ignored; writes form_read.json and crosscheck.json in the run folder
  ffform.py pdf <form pdf> <run_dir>          the form's saved PDF is a source too: every populated value of the data file must be in it
  ffform.py pdfreview <run_dir> --key K ...   record what the PDF shows for a value the program could not find in it

A program reads the file, so no value is retyped by Claude. The form is READ-ONLY for this skill (Paul corrects a wrong
field in the form himself and saves again; the skill uses the saved value).
"""
import argparse
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
def cmd_identify(a):
    found = 0
    for p in a.files:
        raw = load_raw(p)
        if is_form(raw):
            f = raw.get("f") if isinstance(raw.get("f"), dict) else {}
            g = lambda k: tidy((f.get(k) or {}).get("v") if isinstance(f.get(k), dict) else "")  # noqa: E731
            print("FORM DATA FILE  %s   schema %s   client: %s %s   date: %s   modified: %s" % (os.path.basename(p), raw.get("schema"), g("fname"), g("sname"), g("date"), raw.get("modified")))
            found += 1
        else:
            print("not the form's data file  %s" % os.path.basename(p))
    print("%d of %d file(s) are the form's data file (recognised by their content, not their name)." % (found, len(a.files)))
    sys.exit(0 if found else 1)


def read_into_run(file, run, again=False, quiet=False):
    """Read the form's data file for this run. Returns (form, problems); writes nothing when it is the wrong file or the wrong schema."""
    import shutil
    lay = w.layout()
    rj = w.load_opt(os.path.join(run, w.RUN), None)
    if rj is None:
        w.die("MISSING: run.json (run `run.py start` first)")
    try:
        form = read_form(file, lay)
    except FormError as e:
        print(str(e))
        sys.exit(4)
    cross_path = os.path.join(run, w.CROSS)
    old = w.load_opt(cross_path, [])
    if any(i.get("answer") for i in old) and not again:
        w.die("REFUSED: crosscheck answers already exist for this run. Use --again only if the form was saved again and you will redo them.")
    problems = []
    cl = rj["client"]
    if not w.same_person(form["client"]["first"], form["client"]["surname"], cl["first"], cl["surname"]):
        problems.append("the form is for %s %s but this run is for %s %s" % (form["client"]["first"], form["client"]["surname"], cl["first"], cl["surname"]))
    if form["date"] != rj["date"]:
        problems.append("the form's Date completed is %s but Paul's meeting date is %s" % (form["date"] or "empty", rj["date"]))
    if problems:                       # also with --again: a form of another client or date is never accepted
        for p_ in problems:
            print("PROBLEM: " + p_)
        print("\nSTOP. This is not the right file for this run (nothing was saved). Find the right one (identify by content), or ask Paul.")
        sys.exit(5)
    shutil.copyfile(file, os.path.join(run, "form_source.json"))       # the saved copy lets the checker read the file again and compare
    w.save_json(os.path.join(run, w.FORM), form)
    w.save_json(cross_path, crosscheck_items(form, lay))
    if not quiet:
        pop = sum(1 for c in form["fields"].values() if c["populated"])
        print("FORM READ  %s  schema %s  saved %s" % (form["file"], form["schema"], form["modified"]))
        print("  populated fields: %d (%s)   list rows: %d   empty rows left out: %s" % (
            pop, ", ".join("%s %d" % (k, v) for k, v in sorted(form["statuses"].items())), sum(len(v) for v in form["lists"].values()), form["empty_rows"] or "none"))
        for k, v in sorted(form["ignored"].items()):
            print("  %-12s %s" % (k, v))
        if form["presets"]:
            print("  preset values (will be listed in the source report): %s" % ", ".join(form["presets"]))
        lk = form["lookup"]
        if lk["verdict"] != "empty":
            print("  company look-up text: %s%s" % (lk["verdict"].upper().replace("_", " "), (" (" + "; ".join(lk["reasons"]) + ")") if lk["reasons"] else ""))
        for what, items in (("fields the layout does not know (printed in the closing block)", form["unknown_fields"]), ("lists the layout does not know", form["unknown_lists"]),
                            ("columns the layout does not know", ["%s: %s" % kv for kv in form["unknown_cols"].items()]), ("odd entries", form["odd"])):
            if items:
                print("  %s: %s" % (what, ", ".join(items)))
        print("  crosscheck list: %d items to compare with the call (%s)" % (len(crosscheck_items(form, lay)), cross_path))
    return form, problems


def cmd_read(a):
    read_into_run(a.file, a.run, a.again)


# ------------------------------------------------------------------ the form's saved PDF (a source too: the data file's values must be in it)
TRIVIAL = {"yes", "no", "y", "n", "true", "false", "none", "nil", "n a", "na"}
AMOUNT_RX = re.compile(r"(?<![\d.,])R?\s?\d{1,3}(?:[ ,]\d{3})+(?:[.,]\d{1,2})?(?![\d])|(?<![\d.,])R?\s?\d+(?:[.,]\d{1,2})?(?![\d])")


def pdf_text(path):
    import subprocess
    try:
        r = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True)
    except OSError:
        w.die("STOP: pdftotext is not installed, so the form's saved PDF cannot be read.", 4)
    if r.returncode:
        w.die("pdftotext could not read %s: %s" % (path, r.stderr.strip()[:120]), 4)
    return r.stdout


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


def cmd_pdf(a):
    form = w.load_json(os.path.join(a.run, w.FORM), "form_read.json (run `run.py form` first)")
    rec = {"file": None, "sha256": None, "checked": 0, "not_found": [], "reviews": {}, "missing": None}
    if getattr(a, "paul_go_on", None):
        rec["paul_go_on"] = a.paul_go_on
        w.save_json(os.path.join(a.run, w.FORMPDF), rec)
        print("recorded: Paul said to go on with the data file alone (his words: %r). The saved PDF was NOT used; Paul will see this in the glance list." % a.paul_go_on)
        return
    if a.none:
        if len(a.none.strip()) < 8:
            w.die("REFUSED: say why there is no saved PDF (what was searched, at least 8 characters).")
        rec["missing"] = a.none
        w.save_json(os.path.join(a.run, w.FORMPDF), rec)
        print("recorded: no saved PDF of the form (%s). The data file is the source; Paul will see this in the glance list." % a.none)
        return
    if not a.file or not os.path.exists(a.file):
        w.die("REFUSED: give the form's saved PDF (or --none \"reason\" after all three routes were tried).")
    text = pdf_text(a.file)
    if not text.strip():
        w.die("STOP: the form's saved PDF has no extractable text. Tell Paul; render it and read it by eye (not machine-checked).", 4)
    ident = pdf_identity_problems(form, text)
    checked, missing = pdf_check(form, text)
    if ident or (checked and len(missing) > 0.25 * checked):
        for i_ in ident:
            print("PROBLEM: " + i_)
        if checked and len(missing) > 0.25 * checked:
            print("PROBLEM: %d of the %d populated values of the data file are not in this PDF" % (len(missing), checked))
        print("\nSTOP. This does not look like the saved PDF of this data file (nothing was recorded). Find the right PDF, or tell Paul in one line. "
              "If Paul says to go on with the data file alone: run.py ask --need formpdf --kind knowledge ..., then run.py answer ..., then run.py formpdf <run> --paul-go-on.")
        sys.exit(5)
    with open(os.path.join(a.run, "form_pdf.txt"), "w", encoding="utf-8") as f:
        f.write(text)
    rec.update(file=os.path.basename(a.file), sha256=w.sha256_file(a.file), checked=checked, not_found=missing)
    w.save_json(os.path.join(a.run, w.FORMPDF), rec)
    print("FORM PDF READ  %s: %d populated values of the data file checked against its text; %d not found in the PDF." % (rec["file"], checked, len(missing)))
    for m in missing:
        print("  NOT IN THE PDF: %s (%s) = %r" % (m["label"], m["key"], m["value"]))
    if missing:
        print("\nFor each one, look at the PDF and record what it shows: `run.py pdfreview <run> --key K --result format_only|disagree --quote \"<words from the PDF>\" [--pdf-value V]`. "
              "A disagreement is flagged with both values (the data file's value is the one used).")


def cmd_pdfreview(a):
    path = os.path.join(a.run, w.FORMPDF)
    rec = w.load_json(path, "form_pdf.json (run `run.py formpdf` first)")
    if a.key not in {m["key"] for m in rec["not_found"]}:
        w.die("REFUSED: %s is not one of the values the program could not find in the PDF." % a.key)
    with open(os.path.join(a.run, "form_pdf.txt"), encoding="utf-8") as f:
        ntext = w.norm(f.read())
    if w.norm(a.quote) not in ntext or len(w.norm(a.quote)) < 4:
        w.die("REFUSED: that quote is not in the form's PDF text. Copy the exact words from the PDF.")
    miss = next(m for m in rec["not_found"] if m["key"] == a.key)
    if a.result == "disagree" and not (a.pdf_value or "").strip():
        w.die("REFUSED: a disagreement needs --pdf-value (what the PDF says).")
    if a.result == "disagree" and w.norm(a.pdf_value) not in w.norm(a.quote):
        w.die("REFUSED: the quote must contain the PDF's own value (%r)." % a.pdf_value)
    if a.result == "format_only":
        v = miss["value"]
        digs = w.digits(v)
        if len(digs) >= 2 and digs not in w.digits(a.quote):
            w.die("REFUSED: 'format_only' means the PDF shows the SAME value written differently: the quote must contain its digits (%s)." % digs)
        if len(digs) < 2 and w.norm(v) not in w.norm(a.quote):
            w.die("REFUSED: 'format_only' means the PDF shows the same value: the quote must contain %r." % v)
    rec["reviews"][a.key] = {"result": a.result, "quote": a.quote, "pdf_value": a.pdf_value or ""}
    w.save_json(path, rec)
    left = [m["key"] for m in rec["not_found"] if m["key"] not in rec["reviews"]]
    print("recorded %s for %s. Still to review: %s" % (a.result, a.key, left or "nothing"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("identify")
    p.add_argument("files", nargs="+")
    p.set_defaults(fn=cmd_identify)
    p = sub.add_parser("read")
    p.add_argument("file")
    p.add_argument("run")
    p.add_argument("--again", action="store_true")
    p.set_defaults(fn=cmd_read)
    p = sub.add_parser("pdf")
    p.add_argument("file", nargs="?")
    p.add_argument("run")
    p.add_argument("--none")
    p.set_defaults(fn=cmd_pdf)
    p = sub.add_parser("pdfreview")
    p.add_argument("run")
    p.add_argument("--key", required=True)
    p.add_argument("--result", required=True, choices=["format_only", "disagree"])
    p.add_argument("--quote", required=True)
    p.add_argument("--pdf-value", dest="pdf_value")
    p.set_defaults(fn=cmd_pdfreview)
    a = ap.parse_args()
    if getattr(a, "run", None):
        a.run = os.path.abspath(a.run)
    a.fn(a)


if __name__ == "__main__":
    main()
