#!/usr/bin/env python3
"""The one checker for the ff-population-transcript skill.

  verify.py <run_dir> [--stage pre|built|final]

Stages (each includes the one before):
  pre    A reading lock, S client file and access, G the form's data file and saved PDF, B ledger and coverage, C source trace,
         D the skill's rules, L short means short
  built  + E the PDF on disk is exactly what content.json produces
  final  + F the hand-over receipts and the step driver (default)

Prints PASS / FAIL / WARN / ATTEST per item and a RESULT line; exit code 0 only on PASS. ATTEST rows are things only Claude can do
(chat hand-over, saving through the device bridge, the other skills); they are recorded, not machine-proven, and are labelled so.
A malformed file gives a FAIL line, never a crash.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

import compose
import ffform
import tx
import wrlib as w

KINDS_MUST_COVER = {"gap", "difference", "contact", "quote_request", "next_step", "change", "request"}
KINDS_OPTIONAL = {"fact", "figure"}
LEDGER_KINDS = sorted(KINDS_MUST_COVER | KINDS_OPTIONAL)
GROUP_ORDER = "ASGBCDLEF"
GROUP_NAMES = {
    "A": "A. Reading lock (the transcript, twice)",
    "S": "S. Client file and access (S3, S4)",
    "G": "G. The form's data file and its saved PDF (first source)",
    "B": "B. Ledger and coverage",
    "C": "C. Source trace (every value has its source)",
    "D": "D. The skill's rules (totals, ABIs, quotes, policy numbers, claims, two spouses)",
    "L": "L. Short means short",
    "E": "E. The PDF",
    "F": "F. Hand-over (attested by Claude, not machine-proven) and the step driver",
}
QUOTE_WINDOW = 2
COVER_SPAN = 8
ITEM_QUOTE_MIN = 10
LEDGER_QUOTE_MIN = 6
ALLOWED_ROUTES = w.ROUTES + ("user", "passed")
JUDGMENT_KEYS = ("not_discussed_rechecked", "independent_actions_parallel", "prior_year_current", "garbled_flagged", "overview_compared", "other_documents_checked")
HANDOVER_KEYS = ("pdf_sent_in_chat", "saved", "png_visual_check", "independent_check", "judgment", "summary", "teams", "spouse")
RULE_NAMES = {"not_applicable", "aci_pending", "lookup_not_stated", "lead_default", "duties_remainder"}
CONTACT_KEYS = ("cell", "work", "home", "pemail", "wemail")
ASK_QUOTE = "Which insurer should the FNA, Shortfall or Reduced quote(s) be requested from, and is it New Business or Servicing?"
PENDING = compose.PENDING


class Results:
    def __init__(self):
        self.rows = []

    def add(self, level, group, msg):
        self.rows.append((level, group, msg))

    @property
    def fails(self):
        return [r for r in self.rows if r[0] == "FAIL"]


def S(x):
    return x if isinstance(x, str) else ""


def dict_list(x):
    return isinstance(x, list) and all(isinstance(i, dict) for i in x)


def load(path, default):
    return w.load_json(path) if os.path.exists(path) else default


def truthy(v):
    return v is True or (isinstance(v, str) and v.strip().lower() == "true")


def iter_rows(content):
    for sec in content.get("sections") or []:
        for b in sec.get("blocks") or []:
            for r in b.get("rows") or []:
                yield sec["id"], b, r
    for r in (content.get("closing") or {}).get("rows") or []:
        yield "next", {"sub": "closing", "kind": "fields"}, r
    for r in content.get("other_fields") or []:
        yield "other", {"sub": "other", "kind": "fields"}, r


def row_text(r):
    return " ".join([S(r.get("label"))] + [S(b) for b in r.get("bullets") or []] + [S(f.get("text")) for f in r.get("flags") or []])


# ---------------------------------------------------------------- quotes in the transcript and documents
def window_norm(lines, line):
    lo, hi = max(0, line - 1 - QUOTE_WINDOW), min(len(lines), line + QUOTE_WINDOW)
    return w.norm(" ".join(lines[lo:hi]))


def quote_ok(lines, line, quote, minimum=4):
    q = w.norm(quote)
    return len(q) >= minimum and q in window_norm(lines, line)


def window_slice(lines, line):
    return " ".join(lines[max(0, line - 1 - QUOTE_WINDOW):min(len(lines), line + QUOTE_WINDOW)])


def doc_text(run, ref):
    p = os.path.join(run, w.DOCS, ref + ".txt")
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read()


NUM = re.compile(r"\d[\d ,]*(?:\.\d+)?")


def num_forms(text):
    out = set()
    for m in NUM.finditer(text):
        t = m.group(0).replace(" ", "").replace(",", "").strip(".")
        if "." in t:
            t = t.rstrip("0").rstrip(".")
        out.add(t)
    return out


MONEY = re.compile(r"R\s?(\d[\d ]*(?:[.,]\d+)?)")
LONGNUM = re.compile(r"(?<![\d.])(\d{6,})(?!\d)")
PCT = re.compile(r"(\d+(?:\.\d+)?)\s?%")


def figures(text):
    toks = set()
    for rx in (MONEY, LONGNUM, PCT):
        for m in rx.finditer(text):
            toks |= num_forms(m.group(1))
    return {t for t in toks if t}


def source_ref(e):
    ref = S(e.get("ref")).strip()
    if ref:
        return ref
    base = re.split(r"[\\/]", S(e.get("path")).strip())[-1]
    return re.sub(r"\.[A-Za-z0-9]{1,5}$", "", base)


# ---------------------------------------------------------------- search terms for 'Not discussed' / 'not on the call' (every claimable field has curated ones)
def _specs(lay):
    d = {}
    for sec in lay["sections"]:
        for g in sec["groups"]:
            for r in g.get("rows", []):
                if r.get("key"):
                    d[r["key"]] = r
            if g.get("list"):
                d["list:" + g["list"]] = g
    for r in lay["closing"]["rows"]:
        d[r["key"]] = r
    return d


def field_terms(lay, key, label="", row_values=None):
    """(terms, curated). A field with only its label words to search for is a WEAK search: it is never accepted without a reason written for that field."""
    specs = _specs(lay)
    parts = str(key).split(".")
    if parts[0] == "list" and len(parts) == 2:
        g = specs.get("list:" + parts[1])
        if g and g.get("terms"):
            return list(g["terms"]), True
    if len(parts) == 3 and parts[1].isdigit():
        g = specs.get("list:" + parts[0])
        if g and isinstance(g["cols"], list):
            col = next((c for c in g["cols"] if c["col"] == parts[2]), None)
            if col and col.get("terms"):
                return list(col["terms"]), True
    if len(parts) == 2 and parts[1].isdigit() and row_values:
        words = []
        for v in row_values:
            for x in re.findall(r"[A-Za-z][A-Za-z'-]{3,}", str(v)):
                if x.lower() not in ("none", "years", "year", "month", "months", "primary", "school"):
                    words.append(x.lower())
        words = list(dict.fromkeys(words))
        if words:
            return words, True
    r = specs.get(key)
    if r and r.get("terms"):
        return list(r["terms"]), True
    return [re.sub(r"\s*\([^)]*\)", "", label or key).lower().strip() or str(key)], False


def row_values(fr, key):
    p_ = parse_key(key)
    rows = (fr or {}).get("lists", {}).get(p_[0], [])
    if len(p_) == 2 and p_[1] < len(rows):
        return list(rows[p_[1]]["d"].values())
    return []


NO_WORDS = {"no", "n", "false", "none", "0", "nil", "n a", "na", ""}


def sibling_hits(lay, fr, key):
    """Populated fields of the form that say the thing this field asks about exists (for example a debt with credit life), so 'Not discussed' would contradict the form."""
    r = _specs(lay).get(key) or {}
    out = []
    for sp in r.get("siblings") or []:
        if "*" in sp:
            name, _, col = sp.partition(".*.")
            for row in (fr or {}).get("lists", {}).get(name, []):
                v = row["d"].get(col, "")
                if v and w.norm(v) not in NO_WORDS:
                    out.append("%s %d %s = %s" % (name, row["index"] + 1, col, v))
        else:
            c = (fr or {}).get("fields", {}).get(sp)
            if c and c.get("populated") and w.norm(c["v"]) not in NO_WORDS:
                out.append("%s = %s" % (sp, c["v"]))
    return out


DATE_LINE = re.compile(r"(?i)(?:meeting started|started|date|when)\D{0,12}(\d{1,2})[/.\-](\d{1,2})[/.\-](\d{2,4})")


def transcript_date(lines):
    """The date the transcript says the meeting started (first 15 lines), or None when it states none."""
    for ln in lines[:15]:
        m = DATE_LINE.search(ln)
        if m:
            d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
            y += 2000 if y < 100 else 0
            try:
                import datetime as _dt
                return _dt.date(y, mo, d)
            except ValueError:
                return None
    return None


def save_folder_problem(folder, client, spelling=""):
    """The client's own `2. Fact Find` folder. The root must be the FIRST part of the path: (drive, user, ...) liferisk.co.za, then Company - Paul or
    Company - WR Clients\\Paul Kafentzis (Client Files); the folder before `2. Fact Find` must be 'Surname, First' of this client (a different spelling needs a written reason
    that names the surname). It does not look at anything else: that the folder really exists is read from the listing the chat records, which is attested."""
    segs = [x for x in re.split(r"[\\/]+", S(folder)) if x.strip()]
    low = [x.strip().lower() for x in segs]
    if not low or low[-1] != "2. fact find":
        return "the folder %r does not end in the client's '2. Fact Find' folder" % folder
    k = next((i for i, x in enumerate(low) if x == "liferisk.co.za"), None)
    start = 0 if low[0] in ("company - paul", "company - wr clients") else (k + 1 if k is not None and k <= 3 else None)
    root_ok = False
    if start is not None and start < len(low):
        root_ok = low[start] == "company - paul" or (low[start] == "company - wr clients" and start + 1 < len(low) and low[start + 1] == "paul kafentzis (client files)")
    if not root_ok:
        return ("the folder %r does not start (after the drive and liferisk.co.za) with 'Company - Paul' or 'Company - WR Clients\\Paul Kafentzis (Client Files)' (never another broker's folder, never another disk)" % folder)
    if len(segs) < 3:
        return "the folder has no client folder before '2. Fact Find'"
    want = w.norm("%s, %s" % (client.get("surname", ""), client.get("first", "")))
    got = w.norm(segs[-2])
    if got != want:
        sp = S(spelling).strip()
        if w.reason_problem(sp) or w.last_name_token(client.get("surname", "")) not in w.norm(sp):
            return ("the client folder is %r but this run is for %s, %s: save only into the client's own folder (if the folder is really spelled differently, say so in saved.folder_spelling in a real sentence that names the surname; it is then shown to Paul)"
                    % (segs[-2], client.get("surname"), client.get("first")))
    return None


SPEAKER_FIRST = re.compile(r"^\s*\d{1,2}:\d{2}(?::\d{2})?\s+([A-Za-z][A-Za-z'-]*(?:\s+[A-Za-z][A-Za-z.'()-]*){1,4})\s*$")
SPEAKER_LAST = re.compile(r"^([A-Za-z][A-Za-z'-]*(?:\s+[A-Za-z][A-Za-z.'()-]*){1,4}?)\s+\d{1,2}:\d{2}(?::\d{2})?\s*$")
SPEAKER_SUFFIX = re.compile(r"(?i)\s+(?:started|stopped|joined|left)\b.*$")


def speaker_labels(lines):
    """[(line number, label)] of every speaker heading of the transcript (time then name, or name then time)."""
    out = []
    for i, ln in enumerate(lines, 1):
        m = SPEAKER_FIRST.match(ln) or SPEAKER_LAST.match(ln)
        if m:
            label = SPEAKER_SUFFIX.sub("", m.group(1)).strip()
            if label:
                out.append((i, label))
    return out


def other_speakers(lines, client):
    """{label: [lines]} of the speakers who are neither the advisor nor the client."""
    me = [w.norm(w.layout().get("advisor", "")), w.norm("%s %s" % (client.get("first", ""), client.get("surname", "")))]
    out = {}
    for i, label in speaker_labels(lines):
        n = w.norm(label)
        if any(m and (m in n or n in m) for m in me):
            continue
        out.setdefault(label, []).append(i)
    return out


# ---------------------------------------------------------------- A reading lock
def check_reading(run, st, R):
    g = "A"
    k = len(st["chunks"])
    if not st["complete"]:
        R.add("FAIL", g, "transcript flagged incomplete at prep: " + "; ".join(st["notes"]))
        return
    for n in st["notes"]:
        R.add("WARN", g, n)
    lines = w.read_lines(run)
    if w.sha256_text("\n".join(lines)) != st["sha256"]:
        R.add("FAIL", g, "transcript.txt changed after prep")
    p1, p2 = tx.passes_done(st)
    R.add("PASS" if p1 else "FAIL", g, "Pass 1 served all %d chunks in order" % k if p1 else "Pass 1 has NOT served every chunk (run `tx.py status`)")
    R.add("PASS" if p2 else "FAIL", g, "Pass 2 served all %d chunks in order" % k if p2 else "Pass 2 has NOT served every chunk: the Two-Read Lock is not met")
    t1 = [r["t"] for r in st["reads"] if r["pass"] == 1]
    t2 = [r["t"] for r in st["reads"] if r["pass"] == 2]
    if t1 and t2 and min(t2) < max(t1):
        R.add("FAIL", g, "Pass 2 started before Pass 1 finished")
    if st["chunks"][-1][1] != st["total_lines"]:
        R.add("FAIL", g, "last chunk does not reach the last line")
    if st["scan"]:
        R.add("PASS", g, "keyword scan run (%d decision/change/request hits)" % len(st["scan"]["hits"]))
    else:
        R.add("FAIL", g, "keyword scan not run (`tx.py scan`)")
    if st["forced"]:
        R.add("WARN", g, "reading was FORCED past a completeness warning; Paul must have approved this")
    parts = st.get("parts") or [[1, st["total_lines"]]]
    if len(parts) > 1:
        pj = load(os.path.join(run, w.PARTS), {})
        cont = {tuple(c.get("between") or []): c for c in pj.get("continuity") or [] if isinstance(c, dict)}
        bad = []
        for n in range(1, len(parts)):
            c = cont.get((n, n + 1))
            if not c or c.get("result") not in ("ok", "gap") or len(S(c.get("detail")).strip()) < 20:
                bad.append("%d/%d" % (n, n + 1))
            elif c["result"] == "gap":
                R.add("WARN", g, "continuity between transcript %d and %d: a real gap was reported (%s): tell Paul" % (n, n + 1, S(c["detail"])[:80]))
        if bad:
            R.add("FAIL", g, "%d transcripts for one meeting: continuity between %s was not checked (run.py continuity: the last exchange of one and the opening of the next must pick up the same topic)" % (len(parts), ", ".join(bad)))
        else:
            R.add("PASS", g, "%d transcripts read as one continuous meeting; continuity checked at every join" % len(parts))


# ---------------------------------------------------------------- S client file and access
def check_sources(run, R, lines=None, content=None):
    g = "S"
    sources = load(os.path.join(run, w.SOURCES), [])
    access = load(os.path.join(run, w.ACCESS), [])
    questions = load(os.path.join(run, w.QUESTIONS), [])
    rj = load(os.path.join(run, w.RUN), {})
    probs = 0

    def fail(m):
        nonlocal probs
        probs += 1
        R.add("FAIL", g, m)

    if not (dict_list(sources) and dict_list(access) and dict_list(questions)):
        fail("sources.json, access_log.json and questions.json must each be a list of objects")
        return {}
    cl = rj.get("client") or {}
    if not (S(cl.get("first")) and S(cl.get("surname")) and S(rj.get("date"))):
        fail("the run was not started with the client and meeting date from Paul's message (run.py start --client ... --date ...)")
    else:
        if w.parse_date(rj["date"]) is None:
            fail("the meeting date %r is not a real date (DD/MM/YYYY)" % rj["date"])
        if isinstance(content, dict):
            cc = content.get("client") or {}
            if not w.same_person(S(cc.get("first")), S(cc.get("surname")), cl["first"], cl["surname"]):
                fail("content.json is for %s %s but Paul's request was for %s %s" % (cc.get("first"), cc.get("surname"), cl["first"], cl["surname"]))
        if lines is not None and w.last_name_token(cl["surname"]) not in w.norm(" ".join(lines)):
            fail("this transcript never mentions the client's surname (%s): is it the right file?" % cl["surname"])
        if lines is not None and w.parse_date(rj.get("date")):
            td = transcript_date(lines)
            if td and td != w.parse_date(rj["date"]):
                fail("the transcript says the meeting started on %s but Paul's meeting date is %s: this is another meeting's transcript" % (td.strftime("%d/%m/%Y"), rj["date"]))
            elif not td:
                R.add("WARN", g, "the transcript states no meeting date in its first lines, so its date could not be checked against %s" % rj["date"])
    by_need = {}
    for e in access:
        if e.get("route") not in ALLOWED_ROUTES or e.get("result") not in ("ok", "fail") or not S(e.get("need")).strip():
            fail("access_log entry malformed (need, route in %s, result ok|fail): %s" % (ALLOWED_ROUTES, e))
            continue
        by_need.setdefault(e["need"], []).append(e)
    if "transcript" not in by_need or not any(e["result"] == "ok" for e in by_need["transcript"]):
        fail("the transcript has no successful access entry (run.py access --need transcript ... --result ok)")
    mode = rj.get("form_mode")
    asked = {q.get("need"): q for q in questions}
    if mode == "form":
        if "form" not in by_need or not any(e["result"] == "ok" for e in by_need["form"]):
            fail("the form's data file has no successful access entry (run.py access --need form ... --result ok)")
    elif mode in ("manual", "transcript"):
        failed = {e["route"] for e in by_need.get("form", []) if e["result"] == "fail"}
        q = asked.get("form")
        if any(r not in failed for r in w.ROUTES):
            fail("the form's data file is treated as missing but these routes were never tried: %s (Paul's rule: all three, every time)" % [r for r in w.ROUTES if r not in failed])
        elif not q or len(S(q.get("paul_said")).strip()) < 3 or q.get("choice") != mode:
            fail("the form's data file is missing: the run must STOP and ASK Paul whether to use the filled-in Manual Fact Find PDF or the transcript alone, and record his own words (run.py answer)")
        else:
            R.add("WARN", g, "the form's data file was missing on all three routes; Paul chose %r (his words: %r)" % (mode, S(q["paul_said"])[:80]))
    else:
        fail("the form's data file has not been settled (read it, or find it missing on all three routes and ask Paul)")
    for need, es in by_need.items():
        if any(e["result"] == "ok" for e in es) or need in w.SOURCE_KINDS or need in ("form", "formpdf", "lead", "date"):
            continue
        failed = {e["route"] for e in es if e["result"] == "fail"}
        untried = [r for r in w.ROUTES if r not in failed]
        if untried:
            fail("'%s' could not be fetched but these routes were never tried: %s. Never say 'I cannot access your files' until all three failed" % (need, untried))
        elif need not in asked:
            fail("'%s' failed on all three routes but nothing was recorded for Paul: use run.py ask with the errors" % need)
    for q in questions:
        if len(S(q.get("question")).strip()) < 8 or len(S(q.get("searched")).strip()) < 8:
            fail("a question to Paul needs the question and what was searched first: %s" % q)
    refs = {}
    for e in sources:
        k = e.get("kind")
        if k not in w.SOURCE_KINDS:
            fail("source with unknown kind %r (allowed: %s)" % (k, w.SOURCE_KINDS))
        elif "none" in e:
            if len(S(e.get("none")).strip()) < 8:
                fail("source kind %s: 'none' needs a reason (what was searched and not found)" % k)
            tried = {x.get("route") for x in access if x.get("need") == k and x.get("result") == "fail"}
            if k in w.REQUIRED_SOURCE_KINDS and len(tried & set(w.ROUTES)) < 2:
                fail("source kind %s was recorded as 'none on file' but the searches are not logged: try at least two routes and log each with run.py access --need %s ..." % (k, k))
        elif e.get("read") == "yes":
            if not S(e.get("path")).strip() or not S(e.get("date")).strip():
                fail("source %s: a document that was read needs its path and date" % k)
            p = S(e.get("path")).lower().replace("/", "\\")
            if "company - wr clients" in p and "paul kafentzis (client files)" not in p:
                fail("source path %r sits in another broker's folder: only 'Paul Kafentzis (Client Files)' may ever be read or written" % e.get("path"))
            if k == "Manual Fact Find" and mode != "manual":
                fail("a Manual Fact Find was read although Paul did not choose it after the stop-and-ask (it is the last resort, only if the form's data file is missing)")
            ref = source_ref(e)
            if ref in refs:
                fail("two sources share the reference %r: give each its own --ref" % ref)
            refs[ref] = k
            if k in ("Overview", "Policy schedule"):
                txt = doc_text(run, ref)
                if txt is None:
                    fail("the %s %r has no text copy: it cannot be accepted unless its text was recorded (run.py source ... --text-file), because nothing in it could be checked" % (k, ref))
                else:
                    fr_ = load(os.path.join(run, w.FORM), {})
                    idd = w.digits(((fr_.get("fields") or {}).get("idno") or {}).get("v", ""))
                    sur = w.last_name_token(cl.get("surname", ""))
                    if not ((sur and sur in w.norm(txt)) or (len(idd) >= 10 and idd in w.digits(txt))):
                        fail("the %s %r does not mention the client (%s, or the ID number): it does not look like this client's document" % (k, ref, cl.get("surname")))
        else:
            fail("source %s: record read=yes with path and date, or a 'none' reason" % k)
    have = {e.get("kind") for e in sources if e.get("read") == "yes" or len(S(e.get("none")).strip()) >= 8}
    missing = [k for k in w.REQUIRED_SOURCE_KINDS if k not in have]
    if missing:
        fail("client-file sources not accounted for: %s (read the latest one from the client's 1. Overview folder, or record why none exists after searching)" % missing)
    if not probs:
        R.add("PASS", g, "client and date match Paul's request; form file %s; access log has %d entries for %d need(s); %d document(s) read, none from another broker's folder; %d question(s) to Paul"
              % ("read" if mode == "form" else "handled by the stop-and-ask", len(access), len(by_need), len(refs), len(questions)))
    return refs


# ---------------------------------------------------------------- G the form's data file and its saved PDF
def numeric_value(v):
    d = w.digits(v)
    return d if len(d) >= 3 else None


def compose_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from compose_strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from compose_strings(v)


def check_form(run, R, lines, content):
    g = "G"
    rj = load(os.path.join(run, w.RUN), {})
    mode = rj.get("form_mode")
    probs = 0

    def fail(m):
        nonlocal probs
        probs += 1
        R.add("FAIL", g, m)

    if mode != "form":
        if mode in ("manual", "transcript"):
            R.add("PASS", g, "no form data file in this run (%s, on Paul's word): every value comes from fills with their sources" % mode)
        else:
            R.add("FAIL", g, "the form's data file was not read (run.py form)")
        return None
    fr = load(os.path.join(run, w.FORM), None)
    src_path = os.path.join(run, "form_source.json")
    if not isinstance(fr, dict) or not os.path.exists(src_path):
        fail("form_read.json or form_source.json is missing: read the form with run.py form (a program reads it, nobody retypes it)")
        return None
    try:
        again = ffform.read_form(src_path)
    except ffform.FormError as e:
        fail(str(e))
        return None
    again["file"] = fr.get("file")
    if json.dumps(again, sort_keys=True) != json.dumps(fr, sort_keys=True):
        fail("form_read.json is not what the program reads from the form's file (edited by hand?)")
    if fr.get("schema") != w.SCHEMA:
        fail("schema is %r; this skill knows only %s" % (fr.get("schema"), w.SCHEMA))
    cl = rj.get("client") or {}
    if not w.same_person(fr["client"]["first"], fr["client"]["surname"], cl.get("first"), cl.get("surname")):
        fail("the form is for %s %s but Paul asked for %s %s" % (fr["client"]["first"], fr["client"]["surname"], cl.get("first"), cl.get("surname")))
    if fr["date"] != rj.get("date"):
        qs = [q for q in load(os.path.join(run, w.QUESTIONS), []) if isinstance(q, dict) and q.get("need") == "date" and len(S(q.get("paul_said")).strip()) >= 3]
        if not qs:
            fail("the form's Date completed is %s but Paul's meeting date is %s: ask Paul which is right (run.py ask --need date, then run.py answer)" % (fr["date"], rj.get("date")))
    # the form's own parking list, summaries and drafted actions are never a source and never printed
    try:
        with open(src_path, encoding="utf-8-sig") as fh_:
            raw = json.load(fh_)
    except (OSError, ValueError):
        raw = {}
    ignored_texts = []
    for k in ("sum", "pa", "unplaced"):
        ignored_texts += [s for s in compose_strings(raw.get(k)) if len(s) >= 12]
    pa = ((raw.get("f") or {}).get("pa_actions") or {}) if isinstance(raw.get("f"), dict) else {}
    ignored_texts += [s for s in compose_strings(pa) if len(s) >= 12]
    printed = w.norm(" ".join(row_text(r) for _, _, r in iter_rows(content))) if isinstance(content, dict) else ""
    leaked = [t[:40] for t in ignored_texts if w.norm(t) in printed]
    if leaked:
        fail("text from the form's parking list, summaries or drafted action list (never a source) is printed: %s" % leaked[:3])
    lk = fr.get("lookup") or {}
    if lk.get("verdict") == "thrown_out":
        text = (fr["fields"].get("co_does") or {}).get("v", "")
        if text and w.norm(text) in printed:
            fail("the company look-up text was meant to be thrown out (%s) but is printed" % "; ".join(lk.get("reasons") or []))
    rep_keys = {p.get("key") for p in (content.get("report") or {}).get("presets") or []} if isinstance(content, dict) else set()
    miss = [k for k in fr.get("presets") or [] if k not in rep_keys]
    if miss:
        fail("preset values missing from the source report: %s" % miss)
    other_ids = {r.get("id") for r in (content.get("other_fields") or [])} if isinstance(content, dict) else set()
    lost = [k for k in fr.get("unknown_fields") or [] if "other." + k not in other_ids]
    if lost:
        fail("populated form fields the layout has no place for are not in the closing block 'Other fields from the form': %s" % lost)
    # the form's saved PDF is a source too
    fp = load(os.path.join(run, w.FORMPDF), None)
    if not isinstance(fp, dict):
        fail("the form's saved PDF was not read (run.py formpdf), nor recorded as missing after all three routes")
    elif fp.get("paul_go_on"):
        qs_ = [q for q in load(os.path.join(run, w.QUESTIONS), []) if isinstance(q, dict) and q.get("need") == "formpdf" and S(q.get("paul_said")).strip() == S(fp["paul_go_on"]).strip()]
        if not qs_:
            fail("the form's saved PDF is recorded as set aside on Paul's word, but his answer is not on record (run.py ask --need formpdf ..., then run.py answer)")
        else:
            R.add("WARN", g, "the form's saved PDF did not match the data file and was NOT used: Paul said to go on with the data file alone (his words, as the chat recorded them: %r)" % S(fp["paul_go_on"])[:80])
    elif fp.get("missing"):
        acc = [e for e in load(os.path.join(run, w.ACCESS), []) if isinstance(e, dict) and e.get("need") == "formpdf" and e.get("result") == "fail"]
        if {e.get("route") for e in acc} < set(w.ROUTES):
            fail("the form's saved PDF is recorded as missing but not all three routes were tried and logged (need 'formpdf')")
        else:
            R.add("WARN", g, "the form's saved PDF could not be found on any route (%s): the data file alone was used" % S(fp["missing"])[:80])
    else:
        txt_path = os.path.join(run, "form_pdf.txt")
        if not os.path.exists(txt_path):
            fail("form_pdf.txt is missing: read the saved PDF with run.py formpdf")
        else:
            with open(txt_path, encoding="utf-8") as fh_:
                ptxt = fh_.read()
            checked, missing = ffform.pdf_check(fr, ptxt)
            if json.dumps(missing, sort_keys=True) != json.dumps(fp.get("not_found"), sort_keys=True):
                fail("form_pdf.json is not what the program finds when it checks the data file against the PDF text (edited by hand?)")
            nt = w.norm(ptxt)
            for pr_ in ffform.pdf_identity_problems(fr, ptxt):
                fail("the form's saved PDF is not this client's: " + pr_)
            if checked and len(missing) > 0.25 * checked:
                fail("%d of the %d populated values of the data file are not in the saved PDF: it is not the PDF of this data file" % (len(missing), checked))
            for m in missing:
                rv = (fp.get("reviews") or {}).get(m["key"])
                if not rv or rv.get("result") not in ("format_only", "disagree"):
                    fail("%s (%r) is in the data file but not in the form's saved PDF, and nobody looked: run.py pdfreview" % (m["label"], m["value"]))
                elif w.norm(S(rv.get("quote"))) not in nt:
                    fail("pdfreview %s: the quote is not in the PDF text" % m["key"])
                elif rv["result"] == "disagree" and (w.norm(S(rv.get("pdf_value"))) == w.norm(m["value"]) or w.norm(S(rv.get("pdf_value"))) not in w.norm(S(rv.get("quote")))):
                    fail("pdfreview %s: a disagreement needs a PDF value that differs from the data file's and is in the quote" % m["key"])
                elif rv["result"] == "format_only":
                    dg = w.digits(m["value"])
                    if (len(dg) >= 2 and dg not in w.digits(S(rv.get("quote")))) or (len(dg) < 2 and w.norm(m["value"]) not in w.norm(S(rv.get("quote")))):
                        fail("pdfreview %s says format_only but the quote does not hold the value's own digits or words: it does not show the same value" % m["key"])
    cross = load(os.path.join(run, w.CROSS), [])
    if not dict_list(cross):
        fail("crosscheck.json is not a list")
        cross = []
    expect = {i["key"] for i in ffform.crosscheck_items(fr)}
    got = {i.get("key") for i in cross}
    extra = [k for k in got - expect if not (S(k).count(".") == 2 and ".".join(S(k).split(".")[:2]) in expect and form_value(fr, k) is not None)]
    if (expect - got) or extra:
        fail("crosscheck.json does not list exactly the form's populated fields (missing %s, extra %s): run.py form again" % (sorted(expect - got)[:5], sorted(extra)[:5]))
    unanswered = [i["key"] for i in cross if not isinstance(i.get("answer"), dict)]
    if unanswered:
        fail("%d populated form field(s) were never compared with the call (run.py cross): %s" % (len(unanswered), unanswered[:10]))
    for i in cross:
        a = i.get("answer")
        if not isinstance(a, dict):
            continue
        k, r = i["key"], a.get("r")
        if r not in ("same", "differs", "not_on_call"):
            fail("crosscheck %s: answer must be same, differs or not_on_call" % k)
            continue
        if i.get("row") and r == "differs":
            fail("crosscheck %s: a difference must name the column (for example debts.0.bal), not the whole row" % k)
        if r in ("same", "differs"):
            ln = a.get("line")
            if not isinstance(ln, int) or not lines or not 1 <= ln <= len(lines) or not quote_ok(lines, ln, S(a.get("quote")), ITEM_QUOTE_MIN):
                fail("crosscheck %s: the quote is not found at transcript line %r: %r" % (k, ln, a.get("quote")))
        if r == "differs":
            if len(S(a.get("value")).strip()) < 1 or w.norm(S(a.get("value"))) == w.norm(i["value"]):
                fail("crosscheck %s: 'differs' needs the call's own value, and it must differ from the form's (%r)" % (k, i["value"]))
        if r == "same" and numeric_value(i["value"]) and isinstance(a.get("line"), int) and lines and 1 <= a["line"] <= len(lines) and not i.get("row"):
            if numeric_value(i["value"]) not in w.digits(window_slice(lines, a["line"])):
                R.add("WARN", g, "crosscheck %s says the call agrees with the form (%s) but the quote near line %s does not hold those digits: check" % (k, i["value"], a["line"]))
        if r == "not_on_call":
            conf_ = quote_request_conflict(lines or [], load(os.path.join(run, w.LEDGER), {}), k)
            if conf_:
                fail("crosscheck %s is 'not on the call': %s" % (k, conflict_text(k, conf_, lines)))
            lay_ = w.layout()
            terms, curated = field_terms(lay_, k, i.get("label", k), row_values(fr, k) if i.get("row") else None)
            hits, _ = search_terms(run, lines or [], terms)
            why = S(a.get("reviewed")).strip()
            prob = w.reason_hit_problem(why, hits, lines or []) if hits else (w.reason_problem(why) if not curated else None)
            if hits and prob:
                fail("crosscheck %s is 'not on the call' but the call mentions it (searched %s: lines %s): answer same or differs with the words, or give a reason: %s" % (k, terms[:4], hits[:6], prob))
            elif not curated and prob:
                fail("crosscheck %s is 'not on the call' on a WEAK search (only its label words were searched): write a reason for this field (%s)" % (k, prob))
            if re.search(r"\d", i["value"]) and len(w.digits(i["value"])) >= 4 and not i.get("row") and w.digits(i["value"]) in w.digits(" ".join(lines or [])):
                R.add("WARN", g, "crosscheck %s: marked not on the call, yet the digits of %r appear in the transcript: check" % (k, i["value"]))
    if not probs:
        n = sum(1 for i in cross if isinstance(i.get("answer"), dict))
        R.add("PASS", g, "form %s schema %s read by program (matches the saved file exactly); client and date match; saved PDF %s; ignored: parking list, summaries, drafted actions, cost counters (none printed); "
                         "%d presets all in the source report; look-up text %s; %d populated fields each compared with the call (%d same, %d differ)"
              % (fr["file"], fr["schema"], "read and every value of the data file found in it or reviewed" if fp and not fp.get("missing") else "not available", len(fr.get("presets") or []),
                 (lk.get("verdict") or "empty").replace("_", " "), n, sum(1 for i in cross if (i.get("answer") or {}).get("r") == "same"),
                 sum(1 for i in cross if (i.get("answer") or {}).get("r") == "differs")))
    return fr


# ---------------------------------------------------------------- B ledger and coverage
# Lines of the call that carry a request, a decision, a change or a quote word. The scan's own list (tx.HIGH_RE) plus the words of this skill's job.
#  HARD words (FNA, quote, shortfall, RGAR, EGAR, goal analysis, reduced, authority, payslip, appointment, next meeting, set up, follow up, credit life): a line that holds one can NOT be
#  dismissed by a review at all; it must be an entry of a kind that has to be covered, unless Paul's recorded answer says that line is not a request (round 3, A1).
#  QUOTE words (FNA, quote, shortfall, RGAR, EGAR, goal analysis, reduced): an entry on such a line must be kind quote_request (round 3, A3).
#  SOFT words (ask, request, sign, can you, could you, would you, please, I'd like, I will need, organise, arrange, book, prepare, run the numbers, come back to me, get back to me,
#  send me, email me, let me know): with the scan's own words (send, email, tomorrow ...) these lines may be dismissed with a reason that quotes the line.
# Every such line must be within 3 lines of a ledger entry of a kind that must be covered AND share a word of 4 letters or more with it (a line with no such word: any near
# entry), or be dismissed with a reason that quotes it. A request line cannot be filed as a plain "fact" (N1), also when the entry sits a line or two away (A8).
CREDIT_LIFE_RE = re.compile(r"\bcredit(?:or)?[ -]?life\b|\blife cover on the (?:bond|home loan|loan)\b", re.I)        # Paul has a special rule for credit life (round 5, G2)
HARD_RE = re.compile(r"\b(?:fna|quot(?:e|es|ed|ing)|shortfall|rgar|egar|goal analysis|reduced|authori[sz]\w*|authority|payslip\w*|appointment\w*|next meeting|set up|follow[- ]?up)\b|" + CREDIT_LIFE_RE.pattern, re.I)
QUOTE_RE = re.compile(r"\b(?:fna|quot(?:e|es|ed|ing)|shortfall|rgar|egar|goal analysis|reduced)\b", re.I)
SOFT_RE = re.compile(r"\b(?:ask(?:ed|ing)?|request\w*|sign(?:ed|ing|ature)?|can you|could you|would you|please|i['\u2019]?d like|i would like|i will need|organi[sz]\w*|arrange\w*|book(?:ed|ing)?|prepare\w*|run the numbers|come back to me|get back to me|send me|email me|let me know)\b", re.I)
EXTRA_RE = re.compile(HARD_RE.pattern + "|" + SOFT_RE.pattern, re.I)


def request_word(text):
    m = tx.HIGH_RE.search(text or "") or EXTRA_RE.search(text or "")
    return m.group(0) if m else None


def hard_word(text):
    m = HARD_RE.search(text or "")
    return m.group(0) if m else None


def quote_word(text):
    m = QUOTE_RE.search(text or "")
    return m.group(0) if m else None


# The products a quote request can be for, the words that name them, and the quote groups / request fields that belong to each (round 4, F1). A quote_request entry whose line names a
# product must be covered by that product's group, and "Not discussed" on that product's request, type or insurer field is refused while such an entry exists.
PRODUCTS = (
    ("FNA", re.compile(r"\bfna\b|needs analysis", re.I), {"fna"}),
    ("shortfall", re.compile(r"\bshortfall\b", re.I), {"sf", "bf_sf"}),
    ("reduced quote", re.compile(r"\breduced\b", re.I), {"bfred"}),
    ("RGAR", re.compile(r"\brgar\b|retirement goal", re.I), {"rgar"}),
    ("EGAR", re.compile(r"\begar\b|education goal", re.I), {"egar"}),
    ("goal analysis", re.compile(r"(?<!retirement )(?<!education )\bgoal analysis\b", re.I), {"rgar", "egar"}),
)
GROUP_TITLES = {"fna": "the FNA quote", "sf": "the shortfall quote (group risk)", "bf_sf": "the shortfall quote (bf)", "bf_fna": "the FNA quote (bf)", "bfred": "the reduced quote", "rgar": "the RGAR", "egar": "the EGAR"}


def products_in(text):
    """[(product name, its groups)] named in a text."""
    return [(n, set(g)) for n, rx, g in PRODUCTS if rx.search(text or "")]


def key_group(key):
    """The quote group (or RGAR / EGAR) a request, type or insurer field belongs to; None for any other field."""
    k = str(key)
    if k in ("rgar_req",):
        return "rgar"
    if k in ("egar_req",):
        return "egar"
    for q in w.layout()["quote_groups"]:
        if q.get("list"):
            if k.split(".")[0] == q["list"]:
                return q["id"]
        elif k in (q.get("req"), q.get("type"), q.get("ins")):
            return q["id"]
    return None


def quote_request_conflict(lines, ledger, key):
    """The quote_request entry of the ledger whose line (and the lines either side) names the product the field `key` belongs to, or None."""
    if str(key) == "cl_req":                                  # the credit-life answer: refused while the ledger records credit life on the call (round 5, G2)
        for e in (ledger or {}).get("entries") or []:
            if isinstance(e, dict) and e.get("kind") in KINDS_MUST_COVER and isinstance(e.get("line"), int) and 1 <= e["line"] <= len(lines) and CREDIT_LIFE_RE.search(lines[e["line"] - 1]):
                return e
        return None
    gid = key_group(key)
    if not gid:
        return None
    for e in (ledger or {}).get("entries") or []:
        if isinstance(e, dict) and e.get("kind") == "quote_request" and isinstance(e.get("line"), int) and 1 <= e["line"] <= len(lines):
            if any(gid in g for _, g in products_in(window_text(lines, e["line"]))):
                return e
    return None


def conflict_text(key, e, lines):
    if str(key) == "cl_req":
        return ("the ledger records credit life on the call at line %d (%r): fill the field from the call's words; 'Not discussed', 'N/A' and 'not on the call' are all refused while the call talks about credit life"
                % (e["line"], lines[e["line"] - 1].strip()[:50]))
    return ("the ledger records a quote request for %s at line %d (%r): fill the request from the call's words; 'Not discussed', 'N/A' and 'not on the call' are all refused while the request stands"
            % (GROUP_TITLES.get(key_group(key), "this product"), e["line"], lines[e["line"] - 1].strip()[:50]))


def window_text(lines, line, span=2):
    """The text of a ledger entry's line and the `span` lines either side of it."""
    return " ".join(lines[max(0, line - 1 - span):min(len(lines), line + span)])


def required_lines(lines, st):
    hits = set(((st or {}).get("scan") or {}).get("hits") or [])
    return sorted(hits | {i for i, ln in enumerate(lines, 1) if request_word(ln)})


def hard_lines(lines):
    return {i for i, ln in enumerate(lines, 1) if hard_word(ln)}


DISMISS_MAX_LINES = 5
# Words that carry no topic: a request verb or a filler. A request line is NOT handled by an entry that shares only such a word with it (round 4, F3).
REQUEST_FILLER = frozenset("""
send sent sending email emailed emails ask asked asking sign signed need needs please would could your with that this have will also what says about
book booked arrange prepare organise organize request requests like come back from them they there then than when where which just very some
""".split())


def dismissal_problem(about, question, lines):
    """([lines], None) when a dismissals question really frees the lines it names; otherwise ([], the plain reason). At most 5 lines in all, and the question's own text must quote
    at least 4 of the words (4 letters or more, compared by their first 5 letters, in any order; all of them for a line that has fewer) of EVERY named line: the program checks that against the call."""
    nums = []
    for tok in about or []:
        t = S(tok).strip()
        m = re.fullmatch(r"(?:lines?\s*)?(\d+)(?:\s*-\s*(\d+))?", t, re.I)
        if not m:
            return [], "--about for the dismissals question is the line numbers (for example 66 or 66-67), not %r" % t
        lo, hi = int(m.group(1)), int(m.group(2) or m.group(1))
        if hi < lo or hi - lo + 1 > DISMISS_MAX_LINES:
            return [], "one answer can free at most %d lines (%r names %d)" % (DISMISS_MAX_LINES, t, max(0, hi - lo + 1))
        nums += list(range(lo, hi + 1))
    nums = sorted(set(nums))
    if not nums:
        return [], "no line is named"
    if len(nums) > DISMISS_MAX_LINES:
        return [], "one answer can free at most %d lines (this one names %d)" % (DISMISS_MAX_LINES, len(nums))
    for n in nums:
        if not 1 <= n <= len(lines):
            return [], "line %d is not in the transcript" % n
        cw = w.content_words(lines[n - 1])
        need = min(4, len(set(cw)))
        if need == 0:
            return [], "line %d holds no word of 4 letters or more to quote" % n
        got = len(w.shared_content_words(question or "", lines[n - 1]))
        if got < need:
            return [], "the question must name at least %d of the words (4 letters or more) of line %d (%r): it names %d. Put what that line says into the question, so Paul can see it" % (need, n, lines[n - 1].strip()[:50], got)
    return nums, None


def paul_allowed_lines(run, lines=None):
    """{line: {"said": Paul's recorded words, "question": the question as recorded}} of the lines Paul's recorded answer (run.py ask --need dismissals --about "<line numbers>", then run.py answer)
    frees. A question that does not quote its lines, names more than 5 lines or a wide range frees nothing."""
    if lines is None:
        lines = w.read_lines(run) if os.path.exists(os.path.join(run, w.TRANSCRIPT)) else []
    out = {}
    for q in load(os.path.join(run, w.QUESTIONS), []):
        if not isinstance(q, dict) or q.get("need") != "dismissals" or len(S(q.get("paul_said")).strip()) < 3 or not q.get("about"):
            continue
        nums, _prob = dismissal_problem(q.get("about"), S(q.get("question")), lines)      # a question that does not meet the rules frees nothing (nums is empty)
        for n in nums:
            out[n] = {"said": S(q.get("paul_said")).strip(), "question": S(q.get("question")).strip()}
    return out


def line_resolution(h, lines, ents):
    """The entry (of a kind that must be covered) that handles request line h: one on the line itself, or within 3 lines that shares a TOPIC word of 4 letters or more with the line (not a
    request verb or filler such as send, please, would). A line with no such word at all (an 'OK, please do that') is handled by any entry within 3 lines."""
    cw = w.content_words(lines[h - 1]) if 1 <= h <= len(lines) else []
    best = None
    for e in ents:
        d = abs(e["line"] - h)
        if d == 0:
            return e
        if d <= 3 and best is None and (not cw or [x for x in w.shared_content_words(lines[h - 1], S(e.get("quote"))) if x not in REQUEST_FILLER]):
            best = e
    return best


# What may cover which kind of ledger entry (A1). A "lead" or a claim is never a blanket cover, and every cover must cite the same part of the call.
KIND_ALLOWED = {
    "contact": {"fill", "cross", "lead"},                 # a claim that the call did NOT discuss a thing cannot cover something the call DID say (round 3, A9)
    "gap": {"fill"},
    "difference": {"cross_differs", "diff", "note"},
    "quote_request": {"quote", "quote_req"},
    "next_step": {"request", "note", "cross", "fill"},
    "request": {"request", "note", "cross", "fill"},
    "change": {"note", "cross_differs", "fill", "diff"},
}
OVERLAY_TYPE = {"fills": "fill", "rows_add": "fill", "lookup": "fill", "notes": "note", "flags": "note", "joint": "note", "diffs": "diff", "quotes": "quote_entry",
                "policy_numbers": "policy", "abi_override": "abi", "documents_to_request": "request", "next_steps": "request"}


def key_texts(lay, key, label=""):
    """The words a field stands for: its label and its curated search terms (for a list cell: the column's)."""
    out = [label]
    specs = _specs(lay)
    parts = str(key).split(".")
    r = specs.get(key)
    if r:
        out.append(r.get("label", ""))
    if len(parts) == 3 and parts[1].isdigit():
        g = specs.get("list:" + parts[0])
        if g and isinstance(g.get("cols"), list):
            col = next((c for c in g["cols"] if c["col"] == parts[2]), None)
            if col:
                out.append(col.get("label", "") or col["col"])
        out.append(parts[2].replace("_", " "))
    terms, _ = field_terms(lay, key, label)
    out += terms
    return [S(x) for x in out if x]


def curated_terms(lay, key, label=""):
    """The curated search words of a field (empty for a field that only has its label to search for: its label is not a reason to say a fill is about the call's words)."""
    if not key:
        return []
    terms, curated = field_terms(lay, str(key), label)
    return list(terms) if curated else []


CL_KEY_RE = re.compile(r"cl_(?:req|lender|bal|life)|debts\.\d+\.cl")


def credit_life_key(key):
    """True for a credit-life field: the four credit-life answers (requested, lender, balance, cover) and a debt's 'Credit life with lender' cell (round 5, G2)."""
    return bool(CL_KEY_RE.fullmatch(str(key or "")))


# ---- Round 6: the VALUE a fill or an answer writes (H1, H2). A bare No cannot cover a line that asks for something, a request field that covers a quote line must say Yes, and No for credit
# life cannot cover a line that says credit life exists. Paul's recorded answer about the field (its words say no) is the way round. Every value is printed on the glance list.
ASK_RE = re.compile(r"\b(?:ask(?:ed|ing|s)?|request\w*|send|sent|sending|quot(?:e|es|ed|ing)|will need|would like|could you|can you|please|i['\u2019]?d like|want\w*|need\w*)\b", re.I)
NEG_RE = re.compile(r"\b(?:no|not|never|none|without|nothing|neither|nor|decline\w*|cancel\w*)\b|n['\u2019]t\b|\bno longer\b", re.I)
BARE_NO_RE = re.compile(r"\W*(?:no|none)\W*", re.I)
POSITIVE_RE = re.compile(r"\b(?:yes|yeah|yep|there is|there['\u2019]s|there are|have|has|got|covered)\b", re.I)
STAMP_RE = re.compile(r"^\d{1,2}:\d{2}(?::\d{2})?\s+\S")
ASKING_KINDS = ("quote_request", "request", "next_step")


def paul_field_answers(run):
    """[{about, said, question}] of the questions about fields (not the dismissals question) that Paul answered with words that say no: the only way round a bare No on a request or credit-life field."""
    out = []
    for q in load(os.path.join(run, w.QUESTIONS), []):
        if isinstance(q, dict) and q.get("need") != "dismissals" and q.get("about") and len(S(q.get("paul_said")).strip()) >= 3 and NEG_RE.search(S(q.get("paul_said"))):
            out.append({"about": [S(x) for x in q["about"]], "said": S(q.get("paul_said")).strip(), "question": S(q.get("question")).strip()})
    return out


def paul_no_for(key, answers):
    k = S(key)
    for a in answers:
        for x in a["about"]:
            if k and (x == k or k.startswith(x + ".") or x == key_group(k)):
                return a
    return None


def sentence_of(text, quote):
    """The sentence of a line of the call that holds the cited quote (the one that shares most of its words)."""
    parts = [x for x in re.split(r"(?<=[.!?])\s+", S(text).strip()) if x]
    if not parts:
        return ""
    return max(parts, key=lambda x: len(w.shared_content_words(S(quote), x)))


def credit_life_no_problem(tid, tinfo, lines):
    """None, or the plain reason a 'No' for a credit-life field is refused: the sentence it cites (or, for a question, the answer after it) says credit life exists and holds no negation."""
    for ln, q in tinfo.get("cites") or []:
        if not isinstance(ln, int) or not 1 <= ln <= len(lines):
            continue
        sent, at = sentence_of(lines[ln - 1], q), ln
        if sent.rstrip().endswith("?"):
            sent = ""
            for j in range(ln + 1, min(len(lines), ln + 4) + 1):
                t = lines[j - 1].strip()
                if t and not STAMP_RE.match(t):
                    sent, at = sentence_of(t, t), j
                    break
        if not sent or NEG_RE.search(sent):
            continue
        if CREDIT_LIFE_RE.search(sent) or POSITIVE_RE.search(sent):
            return ("%s writes No for credit life, but line %d says %r and holds no no, not, none, never or without: a 'No' cannot cover a line that says credit life exists. Fill it from what the line says, "
                    "or, if the client really said no, ask Paul (run.py ask --kind knowledge --need <name> --about <the field id> --question ..., then run.py answer): his words are then shown next to it" % (tid, at, sent.strip()[:70]))
    return None


def value_problem(kind, line, tid, tinfo, window="", lines=None):
    """None, or the plain reason the VALUE a fill or an answer writes cannot cover a ledger entry of this kind. The program cannot read the call for you: it refuses a value that is not an answer
    (N/A, Not discussed ...), a bare No for a line that asks for something (a request verb in its window and no negation), a request field that is not Yes for such a quote line, and No for
    credit life when the sentence it cites says credit life exists. Paul's recorded answer about the field (words that say no) allows a No."""
    if "value" not in tinfo:
        return None
    val = S(tinfo["value"])
    if kind == "quote_request" and "quote_req" in tinfo["types"] and re.sub(r"[^a-z]+", "", val.lower()) in NOT_AN_ANSWER:
        return ("%s says %r, which is not an answer to a quote request: a request field that covers one must be a Yes or a No. The program cannot read the call for you: it checks the form of the value, "
                "refuses a bare No when the line asks for something, and prints the value on the glance list for Paul" % (tid, val))
    if tinfo.get("paul_no"):
        return None
    bare_no = bool(BARE_NO_RE.fullmatch(val))
    where = (lines[line - 1].strip() if lines and 1 <= line <= len(lines) else S(window).strip())[:60]
    if kind in ASKING_KINDS and ASK_RE.search(window or "") and not NEG_RE.search(window or ""):
        tok = re.match(r"\W*([a-z]+)", val.lower())
        if "quote_req" in tinfo["types"]:
            if not tok or tok.group(1) != "yes":
                return ("%s writes %r for line %d (%r), which asks for a quote and holds no no, not, don't, never, none, without, decline or cancel: a request field that covers it must say Yes. "
                        "If the client really said no, ask Paul (run.py ask --kind knowledge --need <name> --about <the field id> --question ..., then run.py answer): his words are then shown next to it" % (tid, val, line, where))
        elif bare_no:
            return ("%s writes a bare %r for line %d (%r), which asks for something and holds no no, not, don't, never, none, without, decline or cancel: a bare No cannot cover a request. "
                    "Fill it from what the line says, or, if the client really said no, ask Paul (run.py ask --kind knowledge --need <name> --about <the field id> --question ..., then run.py answer)" % (tid, val, line, where))
    if tinfo.get("cl") and bare_no and lines:
        return credit_life_no_problem(tid, tinfo, lines)
    return None


def _pair(name, it):
    """'key = value' for a fill; the cells for a new row; the call's value for a difference: what the chat wrote (shown on the glance list)."""
    if name == "fills":
        return "%s = %s" % (S(it.get("key")), S(it.get("value")))
    if name == "rows_add" and isinstance(it.get("cells"), dict):
        return ("%s row: %s" % (S(it.get("list")), ", ".join("%s=%s" % (k, S(v)) for k, v in it["cells"].items())))[:70]
    return ""


def cover_targets(run, ov, cross, lead, content=None):
    """Everything a ledger entry can be covered by: id -> {types, lines (the call lines it cites), texts (its own words: value, text ...; never the field's label), terms (the field's curated search words)}."""
    lay = w.layout()
    req_keys = {q["req"] for q in lay["quote_groups"] if not q.get("list")} | {"rgar_req", "egar_req"}
    t = {}
    pa = paul_field_answers(run)
    for name, it in compose.overlay_items(ov):
        typ = OVERLAY_TYPE.get(name, "note")
        types = {typ}
        if name == "fills" and it.get("key") in req_keys:
            types.add("quote_req")
        lines = [x["line"] for x in it.get("src") or [] if isinstance(x, dict) and isinstance(x.get("line"), int)]
        texts = [S(it.get(f)) for f in ("text", "value", "other", "insurer", "mode", "found", "resolved", "with") if isinstance(it.get(f), str)]
        if isinstance(it.get("cells"), dict):
            texts += [S(v) for v in it["cells"].values()]
        terms = curated_terms(lay, S(it.get("key"))) if it.get("key") else []
        if name == "quotes":
            grp = next((q for q in lay["quote_groups"] if q["id"] == it.get("group")), {})
            texts.append(S(grp.get("title")))
        cl = credit_life_key(S(it.get("key"))) or (name == "rows_add" and it.get("list") == "debts" and isinstance(it.get("cells"), dict) and bool(S(it["cells"].get("cl")).strip()))
        t[it.get("id", name)] = {"types": types, "lines": lines, "texts": texts, "terms": terms, "cl": cl, "key": S(it.get("key")),
                                 "group": it.get("group") if name == "quotes" else (key_group(S(it.get("key"))) if it.get("key") else None),
                                 "cites": [(x["line"], S(x.get("quote"))) for x in it.get("src") or [] if isinstance(x, dict) and isinstance(x.get("line"), int)]}
        ti = t[it.get("id", name)]
        if name == "fills":
            ti["value"] = S(it.get("value"))
        elif name == "rows_add" and isinstance(it.get("cells"), dict) and S(it["cells"].get("cl")).strip():
            ti["value"] = S(it["cells"].get("cl"))
        ti["pair"] = _pair(name, it)
        if name == "quotes":
            ti["show"] = "%s: %s, %s" % (S(grp.get("title")), S(it.get("insurer")), S(it.get("mode")))
        else:
            ti["show"] = ti["pair"] or next((S(it.get(f)).strip()[:40] for f in ("text", "found", "value", "with", "other") if S(it.get(f)).strip()), "")
        pn = paul_no_for(it.get("key"), pa) if it.get("key") else None
        if pn:
            ti["paul_no"] = pn
    cross_lines = {}
    for i in cross:
        a = i.get("answer")
        if isinstance(a, dict) and a.get("r") in ("same", "differs") and isinstance(a.get("line"), int):
            types = {"cross"} | ({"cross_differs"} if a["r"] == "differs" else set()) | ({"quote_req"} if i["key"] in req_keys else set())
            t[i["key"]] = {"types": types, "lines": [a["line"]], "texts": [S(i.get("value"))] + ([S(a.get("value"))] if a.get("value") else []), "terms": curated_terms(lay, S(i["key"]), S(i.get("label"))), "group": key_group(S(i["key"])),
                      "cl": credit_life_key(S(i["key"])), "value": S(a.get("value")) if a["r"] == "differs" else S(i.get("value")), "key": S(i["key"]),
                      "cites": [(a["line"], S(a.get("quote")))]}
            t[i["key"]]["show"] = "%s = %s" % (i["key"], t[i["key"]]["value"])
            if a["r"] == "differs":
                t[i["key"]]["pair"] = t[i["key"]]["show"]
            pn = paul_no_for(i["key"], pa)
            if pn:
                t[i["key"]]["paul_no"] = pn
            cross_lines[i["key"]] = a["line"]
    if lead:
        t["lead"] = {"types": {"lead"}, "lines": [], "texts": [], "terms": []}
    for k, cl in load(os.path.join(run, w.CLAIMS), {}).items():
        t["claim:" + k] = {"types": {"claim"}, "lines": [x for x in (cl.get("hits") or []) if isinstance(x, int)], "texts": [], "terms": curated_terms(lay, k)}
    for _, _, r in iter_rows(content or {}):
        if str(r.get("id", "")).startswith("quote."):
            grp = next((q for q in lay["quote_groups"] if q["id"] == r.get("quote_group")), None)
            lines = []
            if grp:
                lines = [cross_lines[k] for k in (grp.get("req"), grp.get("type"), grp.get("ins")) if k in cross_lines]
            lines += [x["line"] for x in r.get("src") or [] if isinstance(x, dict) and isinstance(x.get("line"), int)]
            t[r["id"]] = {"types": {"quote"}, "lines": lines, "texts": [S(r.get("label"))] + [S(b) for b in r.get("bullets") or []] + [S((grp or {}).get("title"))], "terms": [], "group": r.get("quote_group"),
                      "show": "; ".join(S(b) for b in (r.get("bullets") or [])[:3])[:70]}
    return t


LEAD_WORDS = re.compile(r"(?i)\b(referr\w*|recommend\w*|heard (?:about|of)|found (?:you|us)|d\s*&\s*r|marketing|lead|introduced)\b")


NOT_AN_ANSWER = frozenset(("", "na", "notapplicable", "notdiscussed", "none", "requested", "tbc"))


def cover_problem(kind, line, tid, tinfo, quote="", window="", lines=None):
    """None when `tid` really covers a ledger entry of this kind at this line; otherwise the plain reason it does not.
    Besides the kind and the nearness, the covering item must be ABOUT the entry: the field's own curated search words must be found in the entry's line (and the lines either side of it),
    or the item's own words (its value or text, never its field label) must share a word of 4 letters or more with the entry's quote."""
    allowed = KIND_ALLOWED.get(kind, set())
    if kind in KINDS_OPTIONAL:
        return None
    if not (tinfo["types"] & allowed):
        return "%s (a %s) cannot cover a %s entry: a %s entry needs %s" % (tid, "/".join(sorted(tinfo["types"])), kind, kind, " or ".join(sorted(allowed)))
    if "lead" in tinfo["types"]:
        if not LEAD_WORDS.search(quote or ""):
            return "the lead search can cover only a line about how the client came to Paul (a referral, a recommendation, a marketing lead), not %r" % (quote or "")[:50]
        return None
    if not tinfo["lines"]:
        return "%s cites no line of the call, so it cannot be about this part of the call" % tid
    if not any(abs(x - line) <= COVER_SPAN for x in tinfo["lines"]):
        return "%s cites the call at line(s) %s, not within %d lines of line %d" % (tid, tinfo["lines"][:4], COVER_SPAN, line)
    if kind == "quote_request" and tinfo.get("group"):
        prods = products_in(window or quote or "")
        if prods and not any(tinfo["group"] in g for _, g in prods):
            return ("%s covers %s, but the entry's own line is about %s: a quote request is covered only by the quote row or request field of the product it names (%s)"
                    % (tid, GROUP_TITLES.get(tinfo["group"], tinfo["group"]), " and ".join(n for n, _ in prods), ", ".join(sorted(set().union(*[g for _, g in prods])))))
    vp = value_problem(kind, line, tid, tinfo, window or quote or "", lines)
    if vp:
        return vp
    own = " ".join(tinfo.get("texts") or [])
    if not w.shared_content_words(quote or "", own) and not terms_in_text(tinfo.get("terms") or [], window or quote or ""):
        return ("%s says nothing about this part of the call: none of the field's own search words (%s) is in the entry's line, and the ledger quote's words (%s) share no word of 4 letters or more with %s's own words (%s)"
                % (tid, ", ".join((tinfo.get("terms") or [])[:5]) or "none", ", ".join(w.content_words(quote)[:6]) or "none", tid, ", ".join(dict.fromkeys(w.content_words(own)))[:80] or "none"))
    return None


def handling_entries(h, lines, ents):
    """EVERY entry (of a kind that must be covered) that handles request line h: one on the line, or within 3 lines and sharing a topic word with it (line_resolution gives only the first)."""
    cw = w.content_words(lines[h - 1]) if 1 <= h <= len(lines) else []
    out = []
    for e in ents:
        d = abs(e["line"] - h)
        if d == 0 or (d <= 3 and (not cw or [x for x in w.shared_content_words(lines[h - 1], S(e.get("quote"))) if x not in REQUEST_FILLER])):
            out.append(e)
    return out


def line_topics(line):
    """[(name, quote groups or None for credit life)] of the topics a line of the call names: each product a quote can be for, and credit life (round 5)."""
    out = [(n, g) for n, g in products_in(line)]
    if CREDIT_LIFE_RE.search(line or ""):
        out.append(("credit life", None))
    return out


def topic_gaps(h, lines, ents, targets):
    """The topics that request line h names (each product, and credit life) that no entry handling the line is REALLY covered for: a quote line that names two products needs a cover from
    each product's own quote row or request field, and a credit-life line needs a fill or an answer of a credit-life field (round 5, G1 and G2)."""
    hand = handling_entries(h, lines, ents)
    gaps = []
    for name, groups in line_topics(lines[h - 1]):
        done = False
        for e in hand:
            for c in e.get("covered_by") or []:
                t = targets.get(c)
                if not t or cover_problem(e["kind"], e["line"], c, t, S(e.get("quote")), window_text(lines, e["line"]), lines):
                    continue
                if (t.get("group") in groups) if groups is not None else t.get("cl"):
                    done = True
        if not done:
            gaps.append(name)
    return gaps


def topic_gap_text(h, lines, gaps, ents, targets):
    named = [n for n, _ in line_topics(lines[h - 1])]
    now = ["%s on line %d" % (cover_label(c, targets), e["line"]) for e in handling_entries(h, lines, ents) for c in e.get("covered_by") or []]
    return ("line %d (%r) names %s, but it is not covered for %s: a line that names several products needs a cover from EACH product's own quote row or request field, and a credit-life line "
            "needs a fill or an answer of a credit-life field (cl_req, cl_lender, cl_bal, cl_life, or a debt's 'Credit life with lender'). Covered now: %s"
            % (h, lines[h - 1].strip()[:70], " and ".join(named), " and ".join(gaps), "; ".join(now) or "nothing"))


def open_topics(lines, ents, targets, entry):
    """[(line, missing topics)] of the hard request lines that `entry` handles and that still lack a cover for something they name (shown when a cover is added)."""
    out = []
    for h in sorted(hard_lines(lines)):
        if entry in handling_entries(h, lines, ents):
            gaps = topic_gaps(h, lines, ents, targets)
            if gaps:
                out.append((h, gaps))
    return out


def cover_label(c, targets):
    """A covering item as the glance list shows it: its id, WHAT IT WROTE (key = value; a note or request: its first 40 characters; a quote row: its insurer and basis), its group, and Paul's recorded
    words when his answer is what lets a No stand (round 6)."""
    t = (targets or {}).get(c) or {}
    show = S(t.get("show")).strip()
    what = c if not show else (show if show.startswith(c) else "%s (%s)" % (c, show))
    lab = GROUP_TITLES.get(t.get("group")) or t.get("group") or ("a credit-life field" if t.get("cl") else None)
    out = "%s [%s]" % (what, lab) if lab else what
    if t.get("paul_no"):
        out += " [Paul's recorded words: \"%s\"]" % t["paul_no"]["said"][:80]
    return out


def covering_values(ledger, targets, lines):
    """([(what was written, line)] first 40, how many in all) for every fill (and every difference answer) that covers any ledger entry: the value the chat wrote, in the chat's own reading of the call."""
    seen, out = set(), []
    for e in (ledger or {}).get("entries") or []:
        if not isinstance(e, dict):
            continue
        for c in e.get("covered_by") or []:
            t = (targets or {}).get(c)
            if c in seen or not t or not t.get("pair") or not ({"fill", "cross_differs"} & set(t.get("types") or ())):
                continue
            seen.add(c)
            out.append((t["pair"], (t.get("lines") or [e.get("line")])[0]))
    return out[:40], len(out)


def values_line(ledger, targets, lines):
    items, total = covering_values(ledger, targets, lines)
    if not total:
        return ""
    return ("Values written to cover the call (%d in all; the chat's own reading of the call, the program does not know what the client really said): %s%s"
            % (total, "; ".join("%s (line %s)" % (p_, n) for p_, n in items), (" ... and %d more" % (total - len(items))) if total > len(items) else ""))


def reviewed_lines(ledger):
    out = set()
    for r in ledger.get("scan_reviewed") or []:
        if not isinstance(r, dict) or len(S(r.get("reason")).strip()) < 6:
            continue
        if isinstance(r.get("line"), int):
            out.add(r["line"])
        elif isinstance(r.get("from"), int) and isinstance(r.get("to"), int):
            out |= set(range(r["from"], r["to"] + 1))
    return out


def check_ledger(run, st, lines, ledger, targets, R):
    g = "B"
    ents = ledger.get("entries") if isinstance(ledger, dict) else None
    if not ents or not dict_list(ents):
        R.add("FAIL", g, "ledger.json has no entries: Pass 1 must record what the call adds (a gap filled, a difference, a contact detail, a quote request, a next step)")
        return
    seen, bad = set(), 0
    for e in ents:
        eid = e.get("id")
        where = "ledger %s" % eid
        if not eid or eid in seen:
            R.add("FAIL", g, "%s: missing or duplicate id" % where)
            bad += 1
            continue
        seen.add(eid)
        kind = e.get("kind")
        if kind not in KINDS_MUST_COVER | KINDS_OPTIONAL:
            R.add("FAIL", g, "%s: kind '%s' not one of %s" % (where, kind, LEDGER_KINDS))
            bad += 1
            continue
        ln = e.get("line")
        if not isinstance(ln, int) or not 1 <= ln <= len(lines):
            R.add("FAIL", g, "%s: line %r is outside the transcript (1-%d)" % (where, ln, len(lines)))
            bad += 1
            continue
        if not quote_ok(lines, ln, S(e.get("quote")), LEDGER_QUOTE_MIN):
            R.add("FAIL", g, "%s: quote not found at line %d (or too short): %r" % (where, ln, e.get("quote")))
            bad += 1
            continue
        cov = e.get("covered_by") or []
        if not isinstance(cov, list) or not all(isinstance(c, str) for c in cov):
            R.add("FAIL", g, "%s: covered_by must be a list of item ids" % where)
            bad += 1
            continue
        unknown = [c for c in cov if c not in targets]
        if unknown:
            R.add("FAIL", g, "%s: covered_by names items that do not exist: %s" % (where, unknown))
            bad += 1
            continue
        if not cov:
            if kind in KINDS_MUST_COVER:
                R.add("FAIL", g, "%s (%s, line %d) is not covered by any fill, difference, note, request or answer: %r" % (where, kind, ln, e.get("quote")))
                bad += 1
            elif w.reason_problem(S(e.get("excluded")), 8):
                R.add("FAIL", g, "%s (%s) is neither covered nor excluded with a real reason (%s)" % (where, kind, w.reason_problem(S(e.get("excluded")), 8) or "give one"))
                bad += 1
            continue
        if kind in KINDS_MUST_COVER:
            probs = [cover_problem(kind, ln, c, targets[c], S(e.get('quote')), window_text(lines, ln), lines) for c in cov]
            if all(probs):
                R.add("FAIL", g, "%s (%s, line %d) is not really covered: %s" % (where, kind, ln, "; ".join(probs)))
                bad += 1
            else:                                                       # a covering item that writes a bad VALUE is a problem even when another item covers the entry (round 6)
                for c in cov:
                    vp = value_problem(kind, ln, c, targets[c], window_text(lines, ln), lines)
                    if vp:
                        R.add("FAIL", g, "%s (%s, line %d): %s" % (where, kind, ln, vp))
                        bad += 1
    must_ents = [e for e in ents if e.get("kind") in KINDS_MUST_COVER and isinstance(e.get("line"), int) and 1 <= e["line"] <= len(lines)]
    freed = paul_allowed_lines(run, lines)
    for h in sorted(hard_lines(lines)):
        if h in freed:
            continue
        hand = handling_entries(h, lines, must_ents)
        if not any(e.get("covered_by") for e in hand):                 # nothing handles it (already a FAIL) or nothing is covered yet (already a FAIL)
            continue
        gaps = topic_gaps(h, lines, must_ents, targets)
        if gaps:
            R.add("FAIL", g, topic_gap_text(h, lines, gaps, must_ents, targets))
            bad += 1
    if not bad:
        must = sum(1 for e in ents if e.get("kind") in KINDS_MUST_COVER)
        R.add("PASS", g, "%d ledger entries, every quote found verbatim; all %d gap/difference/contact/quote/next-step entries are covered by the kind of item that can cover them (a fill, a difference, a quote row, a request, an answer) and that item cites the call within %d lines of the entry" % (len(ents), must, COVER_SPAN))
    k = len(st["chunks"])
    gaps = [(p, c) for p in (1, 2) for c in range(1, k + 1) if not tx.chunk_acked(st, ledger, p, c)]
    if gaps:
        R.add("FAIL", g, "chunks read without a ledger entry or acknowledgement (pass, chunk): %s" % gaps[:12])
    else:
        R.add("PASS", g, "every chunk of both passes has ledger entries or a reasoned acknowledgement")
    sc = st["scan"] or {}
    cz = sc.get("closing_from")
    if cz and not any(isinstance(e.get("line"), int) and e["line"] >= cz for e in ents):
        R.add("WARN", g, "no ledger entry from the closing minutes (lines %d+): requests there are the easiest to miss" % cz)
    if sc:
        check_scan_resolution(run, st, lines, ledger, R)


def check_scan_resolution(run, st, lines, ledger, R):
    """Every line of the call with a decision, change, request or quote word is handled by an entry that must be covered and shares a word with it (or sits on it), or dismissed with a real reason
    (a HARD request line only on Paul's recorded answer); no entry is filed under the wrong kind; and not too much is dismissed."""
    g = "B"
    sc = st.get("scan") or {}
    cz = sc.get("closing_from")
    ents = [e for e in (ledger or {}).get("entries") or [] if isinstance(e, dict)]
    must_ents = [e for e in ents if e.get("kind") in KINDS_MUST_COVER and isinstance(e.get("line"), int)]
    reviewed = reviewed_lines(ledger)
    required = required_lines(lines, st)
    hard = hard_lines(lines)
    allowed = paul_allowed_lines(run, lines)
    for q in load(os.path.join(run, w.QUESTIONS), []):
        if isinstance(q, dict) and q.get("need") == "dismissals" and q.get("about") and len(S(q.get("paul_said")).strip()) >= 3:
            _, qprob = dismissal_problem(q.get("about"), S(q.get("question")), lines)
            if qprob:
                R.add("FAIL", g, "Paul's recorded answer to the dismissals question about %s does not free those lines: %s" % (", ".join(S(x) for x in q.get("about")), qprob))
    handled = lambda h: line_resolution(h, lines, must_ents) is not None  # noqa: E731
    resolved = lambda h: handled(h) or (h in reviewed and (h not in hard or h in allowed))  # noqa: E731
    unresolved = [h for h in required if not resolved(h)]
    hard_open = [h for h in unresolved if h in hard]
    soft_open = [h for h in unresolved if h not in hard]
    if hard_open:
        R.add("FAIL", g, "%d line(s) of the call hold a request word that cannot be dismissed (FNA, quote, shortfall, RGAR, EGAR, authority, payslip, appointment, next meeting, set up, follow up, reduced, credit life) and are not handled by an entry of a kind that must be covered on the line or within 3 lines of it that shares a word with it: lines %s%s. "
              "Record each as an entry (a quote line as quote_request), or, if a line really is not a request, ask Paul (run.py ask --need dismissals --about \"<the line numbers>\" --kind knowledge ..., then run.py answer)"
              % (len(hard_open), hard_open[:15], "..." if len(hard_open) > 15 else ""))
    if soft_open:
        closing = [h for h in soft_open if cz and h >= cz]
        R.add("FAIL", g, "%d line(s) of the call with a decision, change or request word are not handled by an entry that must be covered (on the line, or within 3 lines of it and sharing a word of 4 letters or more with it) or a recorded review with a reason that quotes the line%s: lines %s%s"
              % (len(soft_open), " (%d in the closing minutes)" % len(closing) if closing else "", soft_open[:15], "..." if len(soft_open) > 15 else ""))
    if not unresolved:
        R.add("PASS", g, "every line of the call with a decision, change, request or quote word (%d lines) is handled by an entry that sits on it or is near it and shares a word with it, or was dismissed with a reason (a hard request line only on Paul's recorded answer)" % len(required))
    # a request cannot be filed away as a plain fact or figure, and a quote line is a quote_request
    for e in ents:
        ln = e.get("line")
        if not isinstance(ln, int) or not 1 <= ln <= len(lines) or ln in allowed:
            continue
        near = request_word(window_text(lines, ln))
        if e.get("kind") in KINDS_OPTIONAL and near:
            R.add("FAIL", g, "ledger %s is recorded as '%s' but line %d (or a line next to it) holds the word '%s' (a request, decision, change or quote word): record it as a gap, difference, contact, quote_request, next_step, change or request, or dismiss the line with a review whose reason quotes its words"
                  % (e.get("id"), e.get("kind"), ln, near))
        elif e.get("kind") != "quote_request" and quote_word(lines[ln - 1]):
            R.add("FAIL", g, "ledger %s (%s, line %d): the line holds the word '%s', so the entry must be recorded as a quote_request (or Paul must say the line is not a request: run.py ask --need dismissals --about \"%d\" ..., then run.py answer)"
                  % (e.get("id"), e.get("kind"), ln, quote_word(lines[ln - 1]), ln))
    # every dismissal needs a reason that says something about THAT line
    for rv in ledger.get("scan_reviewed") or []:
        prob = review_problem(rv, lines, required)
        if prob:
            R.add("FAIL", g, "scan review %s: %s" % (("of line %s" % rv.get("line")) if rv.get("line") is not None else ("of lines %s-%s" % (rv.get("from"), rv.get("to"))), prob))
    # dismissing too much is not a review
    qs = load(os.path.join(run, w.QUESTIONS), [])
    go_on = any(isinstance(q, dict) and q.get("need") == "dismissals" and len(S(q.get("paul_said")).strip()) >= 3 for q in qs)
    dismissed_req = [h for h in required if h in reviewed and not handled(h)]
    in_call = len([i for i in reviewed if 1 <= i <= len(lines)])
    share_call = in_call / float(len(lines) or 1)
    share_req = len(dismissed_req) / float(len(required) or 1)
    if (share_call > 0.25 or share_req > 0.60) and not go_on:
        R.add("FAIL", g, "too much of the call was dismissed instead of recorded: %d%% of its lines and %d%% of its decision/change/request/quote lines (the limits are 25%% and 60%%). Record what the call says, or ask Paul: run.py ask --need dismissals --kind knowledge ..., then run.py answer"
              % (round(100 * share_call), round(100 * share_req)))
    elif (share_call > 0.25 or share_req > 0.60) and go_on:
        R.add("WARN", g, "%d%% of the call's lines and %d%% of its decision/change/request/quote lines were dismissed; Paul's recorded answer says to go on" % (round(100 * share_call), round(100 * share_req)))


def review_problem(rv, lines, required):
    """None when a scan review is real: its reason must be a reason and quote a content word of every decision/change/request line it dismisses (or of the line itself)."""
    if not isinstance(rv, dict):
        return "is not an entry"
    p = w.reason_problem(S(rv.get("reason")))
    if p:
        return p
    if isinstance(rv.get("line"), int):
        span = [rv["line"]]
    elif isinstance(rv.get("from"), int) and isinstance(rv.get("to"), int):
        span = [i for i in required if rv["from"] <= i <= rv["to"]]
        if rv["to"] - rv["from"] + 1 > 40:
            return "dismisses more than 40 lines at once"
    else:
        return "names no line"
    for i in span:
        if not 1 <= i <= len(lines):
            return "names line %s, which is not in the transcript" % i
        if w.content_words(lines[i - 1]) and not w.shared_content_words(S(rv.get("reason")), lines[i - 1]):
            return "the reason holds no word (4 letters or more) from line %d (%r): quote what the line says and why nothing needs recording" % (i, lines[i - 1].strip()[:50])
    return None


# ---------------------------------------------------------------- C source trace
def parse_key(k):
    """'fname' -> ('fname',); 'debts.0.bal' -> ('debts', 0, 'bal')"""
    parts = k.split(".")
    if len(parts) >= 2 and parts[1].isdigit():
        return (parts[0], int(parts[1])) + tuple(parts[2:])
    return (k,)


def form_value(fr, key):
    p = parse_key(key)
    if len(p) == 1:
        c = (fr.get("fields") or {}).get(p[0])
        return c["v"] if c and c.get("populated") else None
    rows = (fr.get("lists") or {}).get(p[0]) or []
    if p[1] >= len(rows):
        return None
    if len(p) == 2:
        return " ".join(v for v in rows[p[1]]["d"].values() if v)
    return rows[p[1]]["d"].get(p[2]) or None


def check_composed(run, content, R):
    inp = compose.load_inputs(run)
    again = json.loads(json.dumps(compose.compose(inp), ensure_ascii=False))
    if json.dumps(again, sort_keys=True) != json.dumps(content, sort_keys=True):
        diff = [k for k in set(again) | set(content) if json.dumps(again.get(k), sort_keys=True) != json.dumps(content.get(k), sort_keys=True)]
        R.add("FAIL", "C", "content.json is not what the program composes from the form, the overlay and the answers (edited by hand, or an input changed since): run `run.py compose` again (differs in: %s)" % sorted(diff))
    else:
        R.add("PASS", "C", "content.json is exactly what the program composes from the form's file, the overlay and the recorded answers (not edited by hand)")


def check_content(run, lines, content, fr, refs, ov, R):
    g = "C"
    lay = w.layout()
    n_src, problems = 0, 0
    unchecked = {}
    refs = refs or {}
    rj = load(os.path.join(run, w.RUN), {})
    claims = load(os.path.join(run, w.CLAIMS), {})
    questions = load(os.path.join(run, w.QUESTIONS), [])
    paul_words = {S(q.get("need")): S(q.get("paul_said")).strip() for q in questions if isinstance(q, dict) and len(S(q.get("paul_said")).strip()) >= 3}
    row_by_id = {r["id"]: r for _, _, r in iter_rows(content) if isinstance(r, dict) and r.get("id")}
    for sid, blk, r in iter_rows(content):
        rid = S(r.get("id"))
        if not rid or not isinstance(r.get("bullets"), list) or not S(r.get("label")):
            R.add("FAIL", g, "a row has no id, label or bullets: %r" % (r.get("label"),))
            problems += 1
            continue
        srcs = r.get("src") or []
        if not srcs:
            R.add("FAIL", g, "%s (%s) has no source: 'anything with no source is deleted'" % (rid, r["label"]))
            problems += 1
            continue
        text = " ".join(r["bullets"])
        evidence, item_unchecked = [], False
        for s in srcs:
            n_src += 1
            if not isinstance(s, dict):
                R.add("FAIL", g, "%s: a source must be an object" % rid)
                problems += 1
            elif "form" in s:
                v = form_value(fr, S(s["form"])) if fr else None
                if s.get("from_spouse"):
                    evidence.append(text)
                elif v is None:
                    R.add("FAIL", g, "%s: it cites form field %r, which is empty or does not exist in the form's file" % (rid, s["form"]))
                    problems += 1
                else:
                    evidence.append(v)
                    if r.get("status") in ("confirmed", "preset", "heard", "verify", "form") and w.norm(v) not in w.norm(text) and not r.get("flags"):
                        R.add("FAIL", g, "%s: the printed value %r is not the form's value %r (nothing may be changed without a flag)" % (rid, text[:50], v[:50]))
                        problems += 1
            elif "line" in s:
                ln = s.get("line")
                if not isinstance(ln, int) or not 1 <= ln <= len(lines) or not quote_ok(lines, ln, S(s.get("quote")), ITEM_QUOTE_MIN):
                    R.add("FAIL", g, "%s: source quote not found at transcript line %r (at least %d characters of the exact words): %r" % (rid, ln, ITEM_QUOTE_MIN, s.get("quote")))
                    problems += 1
                else:
                    evidence.append(window_slice(lines, ln))
            elif "formpdf" in s:
                evidence.append(text)
            elif "doc" in s:
                ref, kind = S(s.get("ref")).strip(), s.get("doc")
                if kind not in w.DOC_TYPES or len(w.norm(S(s.get("quote")))) < 6:
                    R.add("FAIL", g, "%s: a document source needs doc (one of %s), ref and quote" % (rid, w.DOC_TYPES))
                    problems += 1
                    continue
                if kind == "Paul (chat)":
                    unchecked.setdefault("Paul's own message", set()).add(rid)
                    item_unchecked = True
                    continue
                if ref not in refs:
                    R.add("FAIL", g, "%s cites document %r which was never recorded as read (run.py source)" % (rid, ref))
                    problems += 1
                elif refs[ref] != kind:
                    R.add("FAIL", g, "%s calls document %r a %s but it was recorded as a %s" % (rid, ref, kind, refs[ref]))
                    problems += 1
                else:
                    txt = doc_text(run, ref)
                    if txt is None:
                        unchecked.setdefault(ref, set()).add(rid)
                        item_unchecked = True
                    elif w.norm(S(s.get("quote"))) not in w.norm(txt):
                        R.add("FAIL", g, "%s: quote not found in document %s" % (rid, ref))
                        problems += 1
                    else:
                        evidence.append(txt)
            elif "derived" in s or "total_of" in s:
                evidence.append(text)
            elif "standing" in s:
                nm = S(s["standing"])
                if not (nm in ("advisor", "dd_cover") or (nm.startswith("abi:") and nm[4:] in {a["key"] for a in lay["standing"]["abi"]})):
                    R.add("FAIL", g, "%s: unknown standing rule %r" % (rid, nm))
                    problems += 1
                evidence.append(text)
            elif "rule" in s:
                if s["rule"] not in RULE_NAMES:
                    R.add("FAIL", g, "%s: unknown rule %r" % (rid, s["rule"]))
                    problems += 1
                evidence.append(text)
            elif "claim" in s:
                if S(s["claim"]) not in claims:
                    R.add("FAIL", g, "%s: it cites a claim that is not on record (run.py claim)" % rid)
                    problems += 1
                evidence.append(text)
            elif "paul" in s:
                if len(S(s["paul"]).strip()) < 3 or paul_words.get(S(s.get("need"))) != S(s["paul"]).strip():
                    R.add("FAIL", g, "%s: Paul's words %r are not the ones the program recorded (run.py ask --kind knowledge --need ..., then run.py answer): words typed into the overlay are not accepted" % (rid, s.get("paul")))
                    problems += 1
                elif all(isinstance(x_, dict) and "paul" in x_ for x_ in srcs):
                    row_nums = {n.replace(",", ".").rstrip("0").rstrip(".") if "." in n.replace(",", ".") else n for n in re.findall(r"\d+(?:[.,]\d+)?", text)}
                    gone = sorted(n for n in row_nums if n not in w.numbers_in(S(s["paul"])))
                    if gone:
                        R.add("FAIL", g, "%s: it prints %s, which is not in Paul's recorded words %r: a value sourced only to Paul must be what he said" % (rid, ", ".join(gone), S(s["paul"])[:60]))
                        problems += 1
                evidence.append(text)
            else:
                R.add("FAIL", g, "%s: a source needs form, line+quote, doc+ref+quote, derived, total_of, standing, rule, claim or paul" % rid)
                problems += 1
        if not item_unchecked and not any(("total_of" in s or "derived" in s) for s in srcs if isinstance(s, dict)):
            have = set()
            for e in evidence:
                have |= num_forms(e)
            lost = sorted(t for t in figures(text) if t not in have)
            if lost:
                R.add("FAIL", g, "%s states figures %s that appear in none of its sources" % (rid, lost))
                problems += 1
        if r.get("kind") == "id" and r.get("status") == "filled" and len(w.digits(text)) >= 6:
            if not any(w.digits(text) in w.digits(e) for e in evidence):
                R.add("FAIL", g, "%s: the identifier %r is not in its sources digit for digit" % (rid, text[:30]))
                problems += 1
    idno = next((r["bullets"][0] for r in row_by_id.values() if r["id"] == "idno" and r["bullets"]), "")
    if len(w.digits(idno)) == 13:
        d = w.digits(idno)
        dob = row_by_id.get("dob")
        if dob and dob.get("status") == "derived":
            m = re.search(r"(\d{2})/(\d{2})/(\d{4})", " ".join(dob["bullets"]))
            if not m or (m.group(3)[2:], m.group(2), m.group(1)) != (d[0:2], d[2:4], d[4:6]):
                R.add("FAIL", g, "date of birth %r does not follow from the ID number's first six digits (YYMMDD)" % " ".join(dob["bullets"])[:30])
                problems += 1
        gen = row_by_id.get("gender")
        if gen and gen.get("status") == "derived":
            want = "female" if int(d[6:10]) < 5000 else "male"
            if not re.match(r"%s\b" % want, " ".join(gen["bullets"]).lower()):
                R.add("FAIL", g, "gender %r does not follow from the ID number (digits 7-10 below 5000 mean female)" % " ".join(gen["bullets"])[:20])
                problems += 1
    for ref, ids in sorted(unchecked.items()):
        R.add("WARN", g, "document source '%s' (rows %s) cannot be machine-checked: no text copy was recorded (run.py source --text-file ...). Paul should glance at those rows" % (ref, sorted(ids)[:6]))
    if not problems:
        R.add("PASS", g, "%d rows, %d sources: every value traces to the form, a quote found in the call or a recorded document, a recomputation, a standing rule or a claim on record; every figure traced; identifiers digit for digit" % (len(row_by_id), n_src))


# ---------------------------------------------------------------- D the skill's rules
POLICY_NO = re.compile(r"(?i)\bpolic(?:y|ies)\b\s*(?:(?:no\.?|number|nr\.?|#)\s*[:\-]?\s*([A-Z0-9][A-Z0-9\-/]{4,})|[:\-]?\s*([A-Z]{0,4}\d{3,}[A-Z0-9\-/]*))")
FLAG_REF = re.compile(r"(?i)\bsee\s+(?:the\s+)?(flag|flags|notes?)\b")
YEAR_LINE = re.compile(r"^(19|20)\d{2}\s*:\s*\S")
DEPENDS = re.compile(r"\b(pending|once|until|after|when|awaiting|waiting for)\b", re.I)
QUOTE_WORDS = re.compile(r"\b(FNA|shortfall|reduced quote|quote)\b", re.I)
DOC_WORDS = re.compile(r"\b(report|medical|psychiatric|document|payslip|statement)\b", re.I)


def term_patterns(terms):
    """The padded patterns a list of search words matches: a word or phrase (its plural too), or a stem written with a star (diabet*)."""
    out = []
    for t in terms:
        nt = w.norm(str(t).rstrip().rstrip("*"))
        if not nt:
            continue
        if str(t).rstrip().endswith("*"):
            out.append(" %s" % nt)
        else:
            out.append(" %s " % nt)
            if not nt.endswith("s"):
                out += [" %ss " % nt, " %ses " % nt]
    return out


def terms_in_text(terms, text):
    n = " %s " % w.norm(text)
    return any(p in n for p in term_patterns(terms))


def search_terms(run, lines, terms):
    """Lines of the call (and recorded documents) that mention any of the terms."""
    hits = []
    nterms = term_patterns(terms)
    for i, ln in enumerate(lines, 1):
        n = " %s " % w.norm(ln)
        if any(t in n for t in nterms):
            hits.append(i)
    docs = []
    d = os.path.join(run, w.DOCS)
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            with open(os.path.join(d, f), encoding="utf-8", errors="replace") as fh_:
                t = " %s " % w.norm(fh_.read())
            if any(x in t for x in nterms):
                docs.append(os.path.splitext(f)[0])
    return hits, docs


def parse_amount(v, kind):
    return w.parse_money(v) if kind == "money" else w.parse_pct(v)


ID_TOKEN = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+|\d[\d ]{8,}\d")


def spouse_overlap(mine, other):
    """Identifiers (ID, phone, email, policy numbers) of the other spouse's own sections that appear in this document. Debts, children and joint policies are common."""
    common_sections = {"debts", "children"}
    theirs = set()
    for sid, blk, r in iter_rows(other):
        if sid in common_sections or r.get("id", "").startswith(("joint.", "other.")):
            continue
        for b in r.get("bullets") or []:
            for m in ID_TOKEN.finditer(b):
                t = re.sub(r"\s", "", m.group(0)).lower()
                if len(w.digits(t)) >= 7 or "@" in t:
                    theirs.add(t)
    mine_text = re.sub(r"\s", "", " ".join(row_text(r) for sid, _, r in iter_rows(mine) if sid not in common_sections and not r.get("id", "").startswith("joint."))).lower()
    return sorted(t for t in theirs if t in mine_text)


SPOUSE_COMMON_IDS = {"consent", "advisor", "date", "meet", "ref", "nat", "nat_other", "marital", "marr_date", "idtype", "loa", "next_appt", "next_day", "next_time", "has_debts", "has_kids"}
SPOUSE_TRIVIAL = {"yes", "no", "n a", "not discussed", "not stated", "pending fna", "none", "south african", "teams meeting", "paul kafentzis", "full time", "employed", "active"}


def spouse_values_overlap(mine, other):
    """The other spouse's own values (names, employers, occupations, amounts, short policy numbers) found in what was written for this spouse.
    Rows copied straight from this spouse's own form are skipped (two people can have the same salary); what the chat wrote is checked."""
    common = {"debts", "children", "other"}
    theirs = {}
    for sid, blk, r in iter_rows(other):
        if sid in common or S(r.get("id")).startswith(("joint.", "notes.", "flag.", "docs_to_request", "next_steps", "total.")) or r.get("id") in SPOUSE_COMMON_IDS:
            continue
        if r.get("status") in ("standing", "rule", "na", "claim", "derived", "unsettled"):
            continue
        for b in r.get("bullets") or []:
            nb = w.norm(b)
            if len(nb) >= 4 and nb not in SPOUSE_TRIVIAL and not re.fullmatch(r"\d{1,3}", nb):
                theirs[nb] = r.get("id")
    mine_own = {w.norm(b) for sid, _, r in iter_rows(mine) for b in r.get("bullets") or [] if any(isinstance(x, dict) and "form" in x for x in r.get("src") or [])}
    hits = []
    for sid, blk, r in iter_rows(mine):
        if sid in common or S(r.get("id")).startswith("joint."):
            continue
        written = r.get("style") in ("added", "flag") or r.get("status") in ("filled", "flag", "quote", "lead", "paul") or any(isinstance(x, dict) and ("line" in x or "doc" in x) for x in r.get("src") or [])
        if not written:
            continue
        text = " %s " % w.norm(" ".join(list(r.get("bullets") or []) + [f.get("text", "") for f in r.get("flags") or []]))
        for v, vid in theirs.items():
            if " %s " % v in text and v not in mine_own:
                hits.append((v, r.get("id")))
    return hits


def check_rules(run, lines, content, fr, ov, R):
    g = "D"
    lay = w.layout()
    probs = 0

    def fail(m):
        nonlocal probs
        probs += 1
        R.add("FAIL", g, m)

    rows = {r["id"]: r for _, _, r in iter_rows(content) if isinstance(r, dict) and r.get("id")}
    un = list(content.get("unsettled") or [])
    quotes_un = [u for u in un if u.startswith("quote.")]
    other_un = [u for u in un if not u.startswith("quote.")]
    if other_un:
        fail("%d field(s) are empty and not settled: %s. Fill each from the call or a document (overlay `fills` with its source), or run `run.py claim` (it searches the call and the documents before 'Not discussed' is allowed)" % (len(other_un), other_un[:12]))
    if quotes_un:
        fail("a quote request has no insurer or no New Business/Servicing (%s): there is no default. ASK PAUL: \"%s\" and record his words with the program (run.py ask --kind knowledge --need <name>, then run.py answer), then add the overlay `quotes` entry with src [{\"ask\": \"<name>\"}]" % (quotes_un[:4], ASK_QUOTE))
    # 'Not discussed' is a claim: the search is repeated here, with the layout's own terms (a claim cannot shrink its own search)
    claims = load(os.path.join(run, w.CLAIMS), {})
    lead = load(os.path.join(run, w.LEAD), {})
    weak = 0
    for key, cl in claims.items():
        word = S(cl.get("as"))
        if word not in ("Not discussed", "Requested", "N/A"):
            fail("claim %s: %r is not allowed (Not discussed, Requested or N/A)" % (key, word))
            continue
        why = S(cl.get("reviewed")).strip()
        row = rows.get(key) or {}
        terms, curated = field_terms(lay, key, row.get("label", key))
        conf = quote_request_conflict(lines, load(os.path.join(run, w.LEDGER), {}), key)         # for every claim word: Not discussed, N/A and Requested (round 5, G1)
        if conf:
            fail("claim %s '%s': %s" % (key, word, conflict_text(key, conf, lines)))
        if word == "Not discussed":
            hits, docs = search_terms(run, lines, list(dict.fromkeys(terms + list(cl.get("terms") or []))))
            sib = sibling_hits(lay, fr, key)
            if hits or docs or sib:
                prob = w.reason_hit_problem(why, hits, lines)
                if prob:
                    fail("claim %s 'Not discussed': the search still finds %s%s%s. Read it, then fill the field or record why it does not answer it (run.py claim --reviewed): %s"
                         % (key, ("call lines %s" % hits[:6]) if hits else "", (" and documents %s" % docs) if docs else "", (" and the form itself says %s" % "; ".join(sib[:3])) if sib else "", prob))
            if not curated:
                weak += 1
                prob = w.reason_problem(why)
                if prob:
                    fail("claim %s 'Not discussed' rests on a WEAK search (only the field's label words): write a reason for this field (run.py claim --key %s --reviewed ...): %s" % (key, key, prob))
            if key in CONTACT_KEYS and not lead.get("searched"):
                fail("claim %s: contact details may be called 'Not discussed' only after the lead-source search and the documents were checked (run.py lead)" % key)
        elif word == "Requested":
            if not key.startswith("debts.") or not lead.get("searched") or len(S(cl.get("searched"))) < 20:
                fail("claim %s 'Requested': only a debt detail that is truly missing after the form, the call, the Overview, other documents AND Outlook (a recorded lead search) were checked; say what was searched in --searched" % key)
            req_hits, _ = search_terms(run, lines, list(dict.fromkeys(terms + list(cl.get("terms") or []))))
            if req_hits:                                                    # 'Requested' says nobody told us: the call must not mention the field (round 5, G2)
                prob = w.reason_hit_problem(why, req_hits, lines)
                if prob:
                    fail("claim %s 'Requested' but the call mentions it (searched %s: lines %s). Read them, then fill the field from what they say, or record why they do not answer it (run.py claim --reviewed): %s"
                         % (key, terms[:3], req_hits[:6], prob))
        else:
            if w.reason_problem(why):
                fail("claim %s 'N/A' needs the reason (--reviewed): %s" % (key, w.reason_problem(why)))
            na_hits, _ = search_terms(run, lines, list(dict.fromkeys(terms + list(cl.get("terms") or []))))
            if na_hits and w.reason_hit_problem(why, na_hits, lines):         # 'N/A' is as much a claim of silence as 'Not discussed' (round 5)
                fail("claim %s 'N/A' but the call mentions it (searched %s: lines %s). Read them, then fill the field from what they say, or record why they do not answer it (run.py claim --reviewed): %s"
                     % (key, terms[:3], na_hits[:6], w.reason_hit_problem(why, na_hits, lines)))
    # every overlay entry must have landed in the document (nothing may be dropped silently)
    for oid in content.get("overlay_unused") or []:
        fail("overlay entry %r landed nowhere in the document (a section, list, key or group that does not apply here): fix it or remove it" % oid)
    # totals reconcile to the cent, from their named components; debt is never left out
    for rid, r in rows.items():
        for s in r.get("src") or []:
            if isinstance(s, dict) and "total_of" in s and s["total_of"] and all("." in c for c in s["total_of"]):
                tot, missing = 0, 0
                for comp in s["total_of"]:
                    cr = rows.get(comp)
                    v = w.parse_money(" ".join(cr["bullets"])) if cr else None
                    if v is None:
                        missing += 1
                    else:
                        tot += v
                shown = w.parse_money(" ".join(r["bullets"]))
                if shown is None or shown != tot:
                    fail("%s: the total %s is not the sum of its components %s (to the cent)" % (rid, " ".join(r["bullets"]), w.fmt_money(tot)))
    if fr:
        for lst, col, rid in (("debts", "inst", "total.debts_monthly"), ("debts", "bal", "total.debts_liabilities"), ("debts", "asset", "total.debts_assets"), ("kids", "cost", "total.kids_total")):
            r = rows.get(rid)
            rws = fr["lists"].get(lst) or []
            if r and rws and lst not in (content.get("common_used") or []):
                want = sum((w.parse_money(x["d"].get(col, "")) or 0 for x in rws), 0)
                shown = w.parse_money(" ".join(r["bullets"]))
                if shown is None or shown != want:
                    fail("%s: the total is %s but ALL %d row(s) of the form add up to %s: debt is never left out of a calculation (not even for credit life)" % (rid, " ".join(r["bullets"]), len(rws), w.fmt_money(want)))
    # the standing ABIs, the Dread Disease default, ACI "?"
    for a in lay["standing"]["abi"]:
        r = rows.get(a["key"])
        if r is None:
            fail("standing ABI line %s (%s) is missing" % (a["label"], a["block"]))
            continue
        paul = any(isinstance(s, dict) and "paul" in s for s in r["src"])
        if not paul and [b.strip() for b in r["bullets"]] != [a["value"]]:
            fail("%s / %s must read %s (the standing value; only Paul can state otherwise) but reads %s" % (a["block"], a["label"], a["value"], r["bullets"]))
    for _, blk, r in iter_rows(content):
        if r.get("label") in lay["standing"]["forbidden_labels"].get(blk.get("sub"), []):
            fail("%s must not carry a %r line (there is no such thing under Disability)" % (blk.get("sub"), r["label"]))
    for k in lay["aci_keys"] + lay["standing"]["not_set_by_rule"]:
        r = rows.get(k)
        if r and any(b.strip() == "?" for b in r["bullets"]):
            fail("%s shows '?': a '?' is not a value, it must read %s" % (k, PENDING))
    for k in lay["standing"]["dd_cover"]["keys"]:
        r = rows.get(k)
        if r and w.parse_money(" ".join(r["bullets"])) != w.parse_money(lay["standing"]["dd_cover"]["value"]) and not any(f.get("kind") == "standing" for f in r.get("flags") or []):
            fail("%s differs from the default %s without the deviation being noted" % (k, lay["standing"]["dd_cover"]["value"]))
    # quote requests: insurer AND New Business or Servicing, from a source, never a default
    def says_servicing(r):
        for s in r["src"]:
            if isinstance(s, dict) and "form" in s and fr and "servic" in w.norm(form_value(fr, S(s["form"])) or ""):
                return True
            if isinstance(s, dict) and "line" in s and "servic" in w.norm(S(s.get("quote"))):
                return True
            if isinstance(s, dict) and "paul" in s and "servic" in w.norm(S(s.get("paul"))):
                return True
        return False

    for rid, r in rows.items():
        b = " ".join(r["bullets"])
        if rid.startswith("quote."):
            if "NOT KNOWN" in b:
                continue
            if "Basis: Servicing" in b and not says_servicing(r):
                fail("%s says Servicing but no source (the form, the call or Paul) says Servicing: Servicing is never a default" % rid)
            ev = []
            for sx in r["src"]:
                if isinstance(sx, dict) and "form" in sx and fr:
                    ev.append(form_value(fr, S(sx["form"])) or "")
                elif isinstance(sx, dict) and isinstance(sx.get("line"), int) and 1 <= sx["line"] <= len(lines):
                    ev.append(window_slice(lines, sx["line"]))
                elif isinstance(sx, dict) and "paul" in sx:
                    ev.append(S(sx["paul"]))
            evn = w.norm(" ".join(ev))
            m_ins = re.search(r"Insurer: (.+?)(?: Basis:|$)", b)
            m_mode = re.search(r"Basis: (New Business|Servicing)", b)
            if m_ins and w.norm(m_ins.group(1)) not in evn:
                fail("%s names the insurer %r but no source it cites (the form, the call words it quotes, or Paul's recorded words) says that insurer" % (rid, m_ins.group(1).strip()))
            if m_mode and ("new business" if m_mode.group(1) == "New Business" else "servic") not in evn:
                fail("%s says %s but no source it cites says so: the basis is never a default" % (rid, m_mode.group(1)))
        elif "servicing" in w.norm(b) and r.get("status") not in ("flag", "filled") and not says_servicing(r):
            fail("%s mentions Servicing without a source that says so" % rid)
    # policy numbers come from the policy schedule only
    srcs = load(os.path.join(run, w.SOURCES), [])
    kinds = {source_ref(e): e.get("kind") for e in srcs if isinstance(e, dict) and e.get("read") == "yes"}
    pns = {S(p.get("resolved")) for p in ov.get("policy_numbers") or [] if isinstance(p, dict)}
    for p in ov.get("policy_numbers") or []:
        if not isinstance(p, dict):
            continue
        if kinds.get(S(p.get("ref"))) != "Policy schedule":
            fail("policy number %r: it must come from a recorded Policy schedule (never the Overview, an old Fact Find, the form or a quote number), but %r is a %s" % (p.get("resolved"), p.get("ref"), kinds.get(S(p.get("ref"))) or "document that was never recorded"))
        else:
            txt = doc_text(run, S(p["ref"]))
            if txt is not None and S(p.get("resolved")) and S(p["resolved"]) not in txt:
                fail("policy number %r is not in the policy schedule %r" % (p.get("resolved"), p.get("ref")))
    for rid, r in rows.items():
        for b in r["bullets"]:
            for m in POLICY_NO.finditer(b):
                code = m.group(1) or m.group(2)
                if code not in pns:
                    fail("%s prints policy number %r that is not confirmed by a policy schedule (overlay `policy_numbers`)" % (rid, code))
    # Business Assurance only if Business Owner = Yes
    biz = (fr["fields"].get("bizowner", {}).get("v") if fr else "") or next((f.get("value") for f in ov.get("fills") or [] if isinstance(f, dict) and f.get("key") == "bizowner"), "")
    if w.norm(biz) not in ("yes", "y", "true"):
        shown = [blk.get("sub") for _, blk, _ in iter_rows(content) if blk.get("sub") in ("Business", "Business policies", "Business assurance", "Key man")]
        if shown:
            fail("Business Assurance and the other business parts are printed (%s) although Business Owner is not Yes" % sorted(set(shown)))
    # every "see flag" / "see notes" points to something that exists in its section
    for sid in {s for s, _, _ in iter_rows(content)}:
        sec_rows = [r for s, _, r in iter_rows(content) if s == sid]
        has_flag = any(r.get("flags") or r.get("style") == "flag" for r in sec_rows)
        has_notes = any(r.get("style") == "added" or r["id"].startswith("n_") for r in sec_rows)
        for r in sec_rows:
            for b in r["bullets"]:
                m = FLAG_REF.search(b)
                if m and not (has_flag if m.group(1).lower().startswith("flag") else has_notes):
                    fail("%s says %r but there is no such %s in its section" % (r["id"], m.group(0), m.group(1).lower()))
    # prior-year information is shown only if still true: a year line needs its pair
    for rid, r in rows.items():
        yl = [b for b in r["bullets"] if YEAR_LINE.match(b.strip())]
        if yl and len({b.strip()[:4] for b in yl}) < 2:
            fail("%s shows a single %r line: a prior-year value is shown only if still true, otherwise as two lines '[year]: old' and '[year]: current'" % (rid, yl[0][:20]))
    # independent requests are never worded as waiting on each other
    for rid, r in rows.items():
        if r.get("style") in ("added", "flag") or rid == "docs_to_request":
            for b in r["bullets"]:
                if DEPENDS.search(b) and QUOTE_WORDS.search(b) and DOC_WORDS.search(b):
                    R.add("WARN", g, "%s is worded as one request waiting on another (%r): independent requests are separate lines unless the call or Paul said so" % (rid, b[:60]))
    # overlay entries all land somewhere; the form wins over a fill
    for f in ov.get("fills") or []:
        if isinstance(f, dict) and f.get("key") and f["key"] not in rows:
            fail("overlay fill %s is for %r, which is not a field of this document" % (f.get("id"), f.get("key")))
        if isinstance(f, dict) and f.get("key") and fr and form_value(fr, f["key"]) is not None:
            fail("overlay fill %s: %r already has a value in the form: the form wins, record a difference instead (crosscheck answer 'differs')" % (f.get("id"), f["key"]))
        if isinstance(f, dict) and f.get("key") == "gross" and any(isinstance(s, dict) and s.get("doc") == "Correspondence" for s in f.get("src") or []):
            fail("overlay fill %s: a salary bracket from the lead email goes in Notes only, never in Gross Income" % f.get("id"))
    for q in ov.get("asked_paul") or []:
        if isinstance(q, dict) and (len(S(q.get("about")).strip()) < 3 or len(S(q.get("question")).strip()) < 10 or len(S(q.get("suggestion")).strip()) < 3 or len(S(q.get("paul_said")).strip()) < 2):
            fail("asked_paul %s needs about, question, suggestion and Paul's own words (paul_said)" % q.get("id"))
    if not content.get("file_name"):
        fail("the file name could not be built: it needs the first name, surname and the form's Date completed")
    # a number of six or more digits that Claude wrote (a policy number, a reference) must be in a recorded policy schedule or Overview
    doc_digits = set()
    for ref_, kind_ in kinds.items():
        if kind_ in ("Policy schedule", "Overview"):
            t_ = doc_text(run, ref_) or ""
            doc_digits |= {re.sub(r"\D", "", x) for x in re.findall(r"\d[\d ]*\d", t_)}
    for rid, r in rows.items():
        authored = r.get("style") in ("added", "flag") or (r.get("status") in ("filled", "flag", "quote", "lead", "paul") and r.get("kind") != "id") or rid == "docs_to_request"
        if not authored:
            continue
        for b_ in r["bullets"]:
            for m_ in re.finditer(r"(?<![\d.,])(?:[A-Za-z]{0,3}\s?)?(\d{6,})(?![\d])", b_):
                if not any(m_.group(1) in d_ for d_ in doc_digits):
                    fail("%s writes the number %s, which is in no recorded Policy schedule or Overview (a number of 6 or more digits needs a document that shows it)" % (rid, m_.group(1)))
    # two spouses: one run each, the question was asked, and nothing of the other spouse is in this document
    rj_ = load(os.path.join(run, w.RUN), {})
    jn = rj_.get("joint") or {}
    if jn.get("answer") not in ("yes", "no"):
        fail("the question 'Is this a joint meeting with a spouse?' was not answered (run.py joint)")
    elif (jn["answer"] == "yes") != bool(rj_.get("spouse")):
        fail("the joint-meeting answer is %r but this run was %sstarted with --spouse: start one run per spouse" % (jn["answer"], "" if rj_.get("spouse") else "not "))
    elif jn["answer"] == "no":
        others = other_speakers(lines, rj_.get("client") or {})
        spn = S(((fr or {}).get("fields") or {}).get("sp_name", {}).get("v")) if fr else ""
        spouse_speaks = bool(spn) and any(w.last_name_token(spn) and w.last_name_token(spn) in w.norm(lab) for lab in others)
        if (others or spouse_speaks) and w.reason_problem(S(jn.get("reason"))):
            fail("the joint-meeting answer is 'no' but these people speak on the call: %s (the form's spouse is %r): answer yes (one run per spouse), or record why not with run.py joint --answer no --reason \"<who they are and why this is not a joint meeting>\""
                 % (", ".join("%s (line %s)" % (k, v[0]) for k, v in sorted(others.items())[:4]), spn))
    if rj_.get("spouse"):
        for name_, it_ in compose.overlay_items(ov):
            if any(isinstance(x_, dict) and "line" in x_ for x_ in it_.get("src") or []) and len(S(it_.get("attrib")).strip()) < 10:
                fail("overlay %s: two spouses in one meeting: say in `attrib` why this statement belongs to this spouse (from what it says, never from the speaker label)" % it_.get("id"))
    # two spouses: the other spouse's identifiers never appear here
    sp = (load(os.path.join(run, w.RUN), {}).get("spouse") or {})
    if sp.get("run"):
        other = load(os.path.join(sp["run"], w.CONTENT), None)
        if not isinstance(other, dict):
            fail("two spouses in one meeting: the other spouse's run (%s) has no content.json yet, so the cross-check cannot be done" % sp["run"])
        else:
            over = spouse_overlap(content, other)
            if over:
                fail("the other spouse's own data is in this document (%d identifier(s) such as %r): only the common debts, children and joint policies may be shared" % (len(over), over[0]))
            back = spouse_overlap(other, content)
            if back:
                fail("this spouse's own data is in the other spouse's document (%d identifier(s) such as %r)" % (len(back), back[0]))
            vo = spouse_values_overlap(content, other)
            if vo:
                fail("values that belong to the other spouse appear in what was written for this spouse (%d, for example %r in %s): only the common debts, children and joint policies may be shared" % (len(vo), vo[0][0], vo[0][1]))
            vb = spouse_values_overlap(other, content)
            if vb:
                fail("values that belong to this spouse appear in what was written for the other spouse (%d, for example %r in %s)" % (len(vb), vb[0][0], vb[0][1]))
    if not probs:
        R.add("PASS", g, "nothing left unsettled; %d claim(s) re-searched; totals recomputed to the cent from their components (debt never left out); standing ABIs, no Life Cover (WOL) line under Disability, ACI '?' shown as %s; "
                         "quote requests name insurer and basis from a source; policy numbers only from a policy schedule; business parts only for a business owner; every cross-reference exists%s"
              % (len(claims), PENDING, "; the other spouse's identifiers are not in this document" if sp.get("run") else ""))


# ---------------------------------------------------------------- L short means short
def check_short(content, R):
    g = "L"
    lim = w.layout()["limits"]
    probs = 0
    long_form = []
    for sid, blk, r in iter_rows(content):
        rid = r.get("id")
        own = r.get("status") in ("filled", "flag", "quote", "lead", "paul", "claim") or r.get("style") in ("added", "flag")
        for b in r.get("bullets") or []:
            n = w.words(b)
            if n > lim["bullet_words"]:
                if own:
                    R.add("FAIL", g, "%s: a bullet is %d words, at most %d: one short fact per line (%r)" % (rid, n, lim["bullet_words"], b[:60]))
                    probs += 1
                else:
                    long_form.append(rid)
            if own and len(compose.facts(b)) > 1:
                R.add("FAIL", g, "%s: one fact per line: this bullet holds %d facts (%r)" % (rid, len(compose.facts(b)), b[:60]))
                probs += 1
        if r.get("style") == "added" and len(r.get("bullets") or []) > lim["section_notes"]:
            R.add("FAIL", g, "%s: %d notes in one section, at most %d: keep what matters" % (rid, len(r["bullets"]), lim["section_notes"]))
            probs += 1
        for f in r.get("flags") or []:
            if w.words(f.get("text")) > lim["flag_words"] + 15:
                R.add("WARN", g, "%s: a flag is %d words: shorten it" % (rid, w.words(f["text"])))
    if long_form:
        R.add("WARN", g, "%d bullet(s) taken from the form are longer than %d words (not changed: nothing may be rewritten): %s" % (len(long_form), lim["bullet_words"], sorted(set(long_form))[:6]))
    if not probs:
        R.add("PASS", g, "every bullet written for this document is one short fact (at most %d words), notes are limited, no fact is run into another" % lim["bullet_words"])


# ---------------------------------------------------------------- E the PDF
TAG_PAGE = re.compile(r"(?im)^\s*(?:page\s*\d+(?:\s*(?:of|/)\s*\d+)?|-\s*\d+\s*-|\d+\s*(?:/|of)\s*\d+)\s*$|\bpage\s+\d+\s+of\s+\d+\b")


def pdf_pages(path, raw=False, layout=False):
    cmd = ["pdftotext"] + (["-raw"] if raw else ["-layout"] if layout else []) + [path, "-"]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True)
    except OSError:
        return None
    if r.returncode:
        return None
    pages = r.stdout.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    return pages


def pdf_fonts(path):
    try:
        r = subprocess.run(["pdffonts", path], capture_output=True, text=True)
    except OSError:
        return None
    if r.returncode:
        return None
    out = []
    for ln in r.stdout.splitlines()[2:]:
        parts = ln.split()
        if len(parts) >= 7:
            out.append((re.sub(r"^[A-Z]{6}\+", "", parts[0]), parts[-5] == "yes"))
    return out


def check_pdf(run, st, content, R):
    import build
    g = "E"
    b = st.get("build")
    if not b:
        R.add("FAIL", g, "the PDF is not built yet (run build.py)")
        return
    if b["content_sha"] != w.content_hash(content):
        R.add("FAIL", g, "content.json changed after the PDF was built: every correction re-opens the whole task, rebuild (build.py)")
        return
    out = os.path.join(run, w.OUT)
    pdf = os.path.join(out, S(content.get("file_name")))
    if not content.get("file_name") or not os.path.exists(pdf):
        R.add("FAIL", g, "PDF missing: expected '%s'" % content.get("file_name"))
        return
    others = [f for f in os.listdir(out) if f.lower().endswith((".pdf", ".docx", ".doc")) and f != content["file_name"]]
    if others:
        R.add("FAIL", g, "unexpected extra file(s) in out/ (the one deliverable is a PDF, never a Word file): %s" % others)
    if w.sha256_file(pdf) != b["pdf_sha"]:
        R.add("FAIL", g, "the PDF on disk is not the one build.py made (replaced or edited)")
    pages = pdf_pages(pdf)
    if not pages:
        R.add("FAIL", g, "the PDF has no extractable text (is it really a PDF?)")
        return
    probs = 0
    with tempfile.TemporaryDirectory(prefix="wrverify-") as tmp:
        ref = os.path.join(tmp, "ref.pdf")
        info = build.build_pdf(content, ref)
        ref_pages = pdf_pages(ref) or []
    if w.norm(" ".join(pages)) != w.norm(" ".join(ref_pages)):
        R.add("FAIL", g, "the PDF text is not what content.json produces (edited, replaced or made by hand): rebuild it with build.py")
        return
    hn = {w.norm(h) for h in info["headings"]}
    for i, pg in enumerate(pages[:-1], 1):
        ls = [x.strip() for x in pg.split("\n") if x.strip()]
        if ls and w.norm(ls[-1]) in hn:
            R.add("FAIL", g, "heading '%s' is stranded at the bottom of page %d" % (ls[-1], i))
            probs += 1
    for i, pg in enumerate((pdf_pages(pdf, layout=True) or pages), 1):
        ls = [x.strip() for x in pg.split("\n") if x.strip()]
        if TAG_PAGE.search(pg) or (ls and re.fullmatch(r"\d{1,3}", ls[-1])) or (ls and re.fullmatch(r"\d{1,3}", ls[0])):
            R.add("FAIL", g, "page %d carries a page number or 'Page N' label (Paul: none anywhere)" % i)
            probs += 1
    raw_pages = [w.norm(p) for p in (pdf_pages(pdf, raw=True) or [])]
    split = []
    for _, blk, r in iter_rows(content):
        if r.get("hidden"):
            continue
        want = w.norm(row_text(r))
        if want and raw_pages and not any(want in p for p in raw_pages):
            split.append(r.get("id"))
    if split:
        R.add("FAIL", g, "%d row(s) are not whole on one page (a row must never be split across pages): %s" % (len(split), split[:6]))
        probs += 1
    fonts = pdf_fonts(pdf) or []
    emb = [n for n, e in fonts if e]
    rec = b.get("font") or {}
    claimed = list(rec.get("ps_names") or []) + ([rec["glyph_ps"]] if rec.get("glyph_ps") else [])
    standard = list(rec.get("ps_names") or []) == ["Helvetica"]          # no TrueType family was found: the PDF's own standard font is used
    if standard:
        if not any(n.startswith("Helvetica") for n, _ in fonts) or emb:
            R.add("FAIL", g, "the build says the standard font Helvetica was used but the PDF's fonts are %s" % [n for n, _ in fonts])
            probs += 1
    elif not emb or any(n not in claimed for n in emb):
        R.add("FAIL", g, "the font recorded at build (%s) is not what the PDF embeds (%s)" % (claimed, emb))
        probs += 1
    elif rec.get("aptos") and not all(n.lower().startswith(("aptos", "dejavu")) for n in emb):
        R.add("FAIL", g, "the build says Aptos but the PDF embeds %s" % emb)
        probs += 1
    if len(pages) > w.layout()["limits"]["pages_warn"]:
        R.add("WARN", g, "the PDF is %d pages: check that nothing is repeated" % len(pages))
    pngs = sorted(f for f in os.listdir(out) if f.startswith("page") and f.endswith(".png"))
    if len(pngs) != len(pages) or any(os.path.getsize(os.path.join(out, f)) < 3000 for f in pngs):
        R.add("FAIL", g, "page images for the visual check are missing (%d images for %d pages)" % (len(pngs), len(pages)))
        probs += 1
    if rec.get("aptos"):
        R.add("PASS", g, "FONT USED: Aptos (embedded: %s)" % ", ".join(emb))
    elif standard:
        R.add("WARN", g, "FONT USED: Helvetica, a standard PDF font that is not embedded (no usable font family was found on this computer). It is NOT Aptos: tell Paul (never say Aptos)")
    else:
        R.add("WARN", g, "FONT USED: %s (embedded in the PDF: %s). Aptos was NOT found on this computer, so this is a substitute: tell Paul (never say Aptos)" % (rec.get("family") or "?", ", ".join(emb)))
    if not probs:
        R.add("PASS", g, "PDF '%s': %d page(s), text identical to what content.json produces, no page numbers, no heading stranded, no row split across pages, one PDF only (no Word file), page images rendered: %s"
              % (content["file_name"], len(pages), ", ".join(pngs)))


# ---------------------------------------------------------------- F receipt and driver
TEAMS_STEPS = ("locate", "prep", "pass1", "pass2", "scan", "content", "build", "check", "planner", "teams", "final")
TEAMS_MARKERS = {
    os.path.join("scripts", "verify.py"): ("--skip-teams", "def near_source", "KINDS_MUST_COVER", "COVER_SPAN"),
    os.path.join("scripts", "run.py"): ("def cmd_ledger", "def cmd_done", "def cmd_receipt"),
}


def teams_fingerprint(sd):
    """sha256 (first 16 hex) of the Teams program's verify.py, run.py and steps.json, so Paul can compare them with the released ones."""
    out = {}
    for rel in (os.path.join("scripts", "verify.py"), os.path.join("scripts", "run.py"), "steps.json"):
        try:
            out[rel.replace(os.sep, "/")] = w.sha256_file(os.path.join(S(sd), rel))[:16]
        except OSError:
            out[rel.replace(os.sep, "/")] = "missing"
    return out


def teams_skill_problem(sd):
    """None when the folder the chat named looks like the real Teams skill (the step names, the size and the marks of its checker and driver); otherwise why not.
    This is a plausibility check, not a proof: the folder was named by the chat, so its fingerprint is printed for Paul to compare."""
    md = os.path.join(sd, "SKILL.md")
    md_text = ""
    if os.path.exists(md):
        with open(md, encoding="utf-8", errors="replace") as fh_:
            md_text = fh_.read()
    if not re.search(r'(?m)^name:\s*"?client-teams-transcript-skill"?\s*$', md_text):
        return "%r is not the folder of client-teams-transcript-skill (its SKILL.md must say so)" % sd
    steps = load(os.path.join(sd, "steps.json"), {}).get("steps", [])
    first = [x.get("id") for x in steps if isinstance(x, dict) and "first" in (x.get("applies") or [])]
    if [x for x in TEAMS_STEPS if x not in first]:
        return "%r has not the steps of a first-meeting run (%s): it does not look like the real Teams program" % (sd, ", ".join(x for x in TEAMS_STEPS if x not in first))
    for rel, marks in TEAMS_MARKERS.items():
        try:
            with open(os.path.join(sd, rel), encoding="utf-8", errors="replace") as f:
                txt = f.read()
        except OSError:
            return "%r has no %s: it does not look like the real Teams program" % (sd, rel)
        if rel.endswith("verify.py") and txt.count("\n") < 500:
            return "%s in %r is only %d lines: the real Teams checker is much longer, so this is not the real Teams program" % (rel, sd, txt.count("\n"))
        missing = [m for m in marks if m not in txt]
        if missing:
            return "%s in %r lacks %s: it does not look like the real Teams program" % (rel, sd, ", ".join(missing))
    return None


def check_teams_handoff(run, rj, content, tm):
    """None when the Teams run is really there and finished up to the message; otherwise the plain reason. Reads the Teams program's own records and runs its own checker.
    The Teams skill folder is named by the chat: it is checked for plausibility and its fingerprint is printed, which Paul compares with the released one."""
    sd, rd = S(tm.get("skill_dir")), S(tm.get("run_folder"))
    prob = teams_skill_problem(sd)
    if prob:
        return prob
    tr = load(os.path.join(rd, w.RUN), None)
    cl = rj.get("client") or {}
    if not isinstance(tr, dict):
        return "%r holds no run.json: the Teams program was not started there" % rd
    tc = tr.get("client") or {}
    if tr.get("meeting_type") != "first" or not w.same_person(S(tc.get("first")), S(tc.get("surname")), cl.get("first"), cl.get("surname")) or tr.get("date") != rj.get("date"):
        return "the Teams run at %r is not a first-meeting run for %s %s on %s" % (rd, cl.get("first"), cl.get("surname"), rj.get("date"))
    steps = [x for x in load(os.path.join(sd, "steps.json"), {}).get("steps", []) if "first" in (x.get("applies") or [])]
    ids = [x["id"] for x in steps]
    before = ids[:ids.index("teams")] if "teams" in ids else ids[:-1]
    open_ = [x for x in before if (tr.get("steps", {}).get(x) or {}).get("state") != "done"]
    if open_:
        return "the Teams run has not finished these steps before its message step: %s (drive it with its own run.py until it shows the message to Sitamah)" % open_
    mine = load(os.path.join(run, w.STATE), {})
    theirs = load(os.path.join(rd, w.STATE), None)
    if not isinstance(theirs, dict) or not mine.get("sha256") or theirs.get("sha256") != mine.get("sha256"):
        return "the Teams run was made from another transcript than this run's (its transcript fingerprint %s is not %s): run the Teams program on the same transcript" % (str((theirs or {}).get("sha256"))[:12], str(mine.get("sha256"))[:12])
    for f in ("planner_note.html", "teams_message.txt"):
        if not os.path.exists(os.path.join(rd, "out", f)):
            return "the Teams run has no out/%s: its Planner page and message were not built" % f
    with open(os.path.join(rd, "out", "teams_message.txt"), encoding="utf-8") as f_:
        msg = f_.read()
    if w.norm("%s %s" % (cl.get("first"), cl.get("surname"))) not in w.norm(msg) or rj.get("date") not in msg:
        return "the Teams message does not name %s %s and %s" % (cl.get("first"), cl.get("surname"), rj.get("date"))
    r = subprocess.run([sys.executable, os.path.join(sd, "scripts", "verify.py"), rd, "--skip-teams"], capture_output=True, text=True)
    if r.returncode != 0 or "RESULT: PASS" not in r.stdout:
        return "the Teams program's own checker does not pass for that run (verify.py --skip-teams): %s" % ((r.stdout.strip().splitlines() or ["no output"])[-1])[:120]
    tcnt = load(os.path.join(rd, w.CONTENT), {})
    form_next = next((r_["bullets"][0] for _, _, r_ in iter_rows(content) if r_.get("id") == "next_appt" and r_.get("bullets") and r_["bullets"][0] not in ("N/A", "Not discussed")), "")
    day = next((r_["bullets"][0] for _, _, r_ in iter_rows(content) if r_.get("id") == "next_day" and r_.get("bullets")), "")
    if form_next:
        na = tcnt.get("next_appointment") or {}
        txt = w.norm(S(na.get("text")))
        if na.get("agreed") is not True or not (w.digits(form_next) in w.digits(S(na.get("text"))) or (day and w.norm(day) in txt)):
            return "the form has a next appointment (%s %s) but the Teams run does not carry it as an agreed follow-up appointment (next_appointment.agreed true with that day or date)" % (day, form_next)
    return None


def check_receipt(run, st, content, R, skip=()):
    g = "F"
    p = os.path.join(run, w.RECEIPT)
    rj = load(os.path.join(run, w.RUN), {})
    rc = load(p, None) if os.path.exists(p) else None
    if not isinstance(rc, dict):
        R.add("FAIL", g, "receipt.json missing or unreadable: record the hand-over evidence before declaring the run complete (run.py receipt)")
        return

    def fail(m):
        R.add("FAIL", g, m)

    def text(d, *keys, n=1):
        return isinstance(d, dict) and all(len(str(d.get(k) or "").strip()) >= n for k in keys)

    cur = (st.get("build") or {}).get("content_sha")
    stamps = rc.get("_stamps") if isinstance(rc.get("_stamps"), dict) else {}
    stale = [k for k in HANDOVER_KEYS if k in rc and stamps.get(k) != cur]
    if stale:
        fail("hand-over receipts recorded for an older build (the PDF was rebuilt after content.json changed): redo and re-record %s" % stale)
    if not truthy(rc.get("pdf_sent_in_chat")):
        fail("the PDF must be sent in the chat for download (pdf_sent_in_chat)")
    else:
        R.add("ATTEST", g, "PDF sent in the chat")
    sv = rc.get("saved") if isinstance(rc.get("saved"), dict) else {}
    if not text(sv, "tool", "folder", "filename", "tool_result", "folder_listing_check", "listed_size"):
        fail("saved{tool, folder, filename, tool_result, folder_listing_check, listed_size} must all be filled from the real tool output")
    else:
        bad = 0
        local = (st.get("build") or {}).get("pdf_size")
        if sv["filename"] != content.get("file_name"):
            fail("saved.filename %r is not the expected %r" % (sv["filename"], content.get("file_name")))
            bad += 1
        if S(content.get("file_name")) not in str(sv["folder_listing_check"]):
            fail("saved.folder_listing_check does not show the file in the folder listing")
            bad += 1
        fp_ = save_folder_problem(sv["folder"], rj.get("client") or {}, S(sv.get("folder_spelling")))
        if fp_:
            fail("saved.folder: " + fp_)
            bad += 1
        if str(sv["listed_size"]).strip().replace(",", "") != str(local):
            fail("saved.listed_size is %s but the local PDF is %s bytes: a save is proven only when the listed size equals the local file's (a new time with the old size means the copy lagged: commit again and list again)" % (sv["listed_size"], local))
            bad += 1
        if not bad:
            R.add("ATTEST", g, "PDF saved to the client's 2. Fact Find folder via %s; the listing shows the file at %s bytes, equal to the local file (compared by the program)" % (sv["tool"], sv["listed_size"]))
    if len(str(rc.get("png_visual_check") or "").strip()) < 20:
        fail("png_visual_check: say what you saw on each page image (layout, headings, bullets, red flags)")
    else:
        R.add("ATTEST", g, "page images looked at")
    ic = str(rc.get("independent_check") or "").strip()
    if len(ic) < 10:
        fail("independent_check: 'subagent: <what it re-checked and found>' (or 'n/a: the Agent tool is not available')")
    else:
        R.add("ATTEST", g, "independent re-check: " + ic[:90])
    jd = rc.get("judgment") if isinstance(rc.get("judgment"), dict) else {}
    if not text(jd, *JUDGMENT_KEYS, n=12):
        fail("judgment: one sentence each (at least 12 characters) for %s" % list(JUDGMENT_KEYS))
    else:
        R.add("ATTEST", g, "judgment items answered: " + "; ".join("%s: %s" % (k, str(jd[k])[:40]) for k in JUDGMENT_KEYS[:3]) + " ...")
    sm = rc.get("summary") if isinstance(rc.get("summary"), dict) else {}
    if not text(sm, "invoked", "abi_same", n=12):
        fail("summary{invoked, abi_same}: the Fact Find Summary is made by the fact-find-summary skill from this PDF; say what was run and confirm its Section 8 shows the same ABIs")
    else:
        R.add("ATTEST", g, "Fact Find Summary hand-over: " + str(sm["invoked"])[:80])
    tm = rc.get("teams") if isinstance(rc.get("teams"), dict) else {}
    if not text(tm, "run_folder", "skill_dir", "next_appointment_carried", n=3):
        fail("teams{run_folder, skill_dir, next_appointment_carried}: the Planner note page and the message to Sitamah are made ONLY by client-teams-transcript-skill (run.py start --type first, driven to its message step); record its run folder, the skill's own folder and which next appointment it carries")
    else:
        msg = check_teams_handoff(run, rj, content, tm)
        if msg:
            fail("Teams hand-over: " + msg)
        else:
            R.add("ATTEST", g, "Planner note page and message to Sitamah: the Teams run at %s has every step before its message step done, was made from this run's transcript, and its own checker (verify.py --skip-teams, in the Teams skill folder the chat named) printed RESULT: PASS when this checker ran it; that the folder is the real released Teams skill is attested (its fingerprint is on the glance list); the page was published, the message shown and Paul's yes obtained by Claude (attested); next appointment carried: %s"
                  % (tm["run_folder"], str(tm["next_appointment_carried"])[:60]))
    if rj.get("spouse"):
        sp = rc.get("spouse") if isinstance(rc.get("spouse"), dict) else {}
        if not text(sp, "cross_check", n=12):
            fail("spouse.cross_check: say the result of the search for the other spouse's data in this PDF (run.py spouse)")
        else:
            R.add("ATTEST", g, "other spouse's data searched for: " + str(sp["cross_check"])[:80])


def check_programs_unchanged(run, R):
    """The programs, the layout, the steps and the rule pages must be what they were when the run started (every stage, not only the last)."""
    g = "F"
    rj = load(os.path.join(run, w.RUN), None)
    if not isinstance(rj, dict):
        return
    fp0 = rj.get("program_fingerprint")
    if not fp0:
        R.add("FAIL", g, "this run has no program fingerprint (it was not started by run.py start of this version)")
    elif fp0 != w.program_fingerprint():
        R.add("FAIL", g, "the skill's programs, layout, steps or rule pages were CHANGED while this run was in progress: the programs are run as they are and never edited during a run. Start the run again")


def check_driver(run, R, skip=()):
    g = "F"
    rj = load(os.path.join(run, w.RUN), None)
    if not isinstance(rj, dict) or not isinstance(rj.get("steps"), dict):
        R.add("FAIL", g, "run.json missing: this run was not driven by run.py (start it with run.py start)")
        return
    started, now_stamp = rj.get("skill_stamp"), w.skill_stamp()
    if started and now_stamp and started != now_stamp:
        R.add("WARN", g, "the skill was updated while this run was in progress (the run started under %s, the skill is now %s): tell Paul" % (w.stamp_display(started), w.stamp_display(now_stamp)))
    steps = load(os.path.join(w.SKILL_DIR, "steps.json"), {}).get("steps", [])
    pending = [s["id"] for s in steps if s["id"] != "final" and (rj["steps"].get(s["id"]) or {}).get("state") != "done"]
    if pending:
        R.add("FAIL", g, "steps not completed through the driver (run.py done): %s" % pending)
    else:
        R.add("PASS", g, "every step before the final check was completed through the driver, in order; the programs, layout, steps and rule pages did not change during the run")


# ---------------------------------------------------------------- driver
def guarded(R, group, name, fn, *a, **kw):
    try:
        return fn(*a, **kw)
    except Exception as e:  # a malformed file must be a clear FAIL, never a traceback
        R.add("FAIL", group, "the check '%s' could not read the files (%s: %s): fix the shape of the input" % (name, type(e).__name__, str(e)[:120]))
        return None


def run_checks(run, stage, skip=()):
    R = Results()
    st = w.load_json(os.path.join(run, w.STATE), "state.json (run tx.py prep first)")
    guarded(R, "A", "reading", check_reading, run, st, R)
    guarded(R, "F", "programs unchanged", check_programs_unchanged, run, R)
    lines = w.read_lines(run)
    ledger = load(os.path.join(run, w.LEDGER), None)
    content = load(os.path.join(run, w.CONTENT), None)
    ov = load(os.path.join(run, w.OVERLAY), {})
    cross = load(os.path.join(run, w.CROSS), [])
    lead = load(os.path.join(run, w.LEAD), {})
    shape = compose.check_inputs(compose.load_inputs(run))
    if not isinstance(content, dict):
        R.add("FAIL", "C", "content.json missing (run `run.py compose` after the overlay is written)")
    for e in shape:
        R.add("FAIL", "C", "overlay.json shape: " + e)
    refs = guarded(R, "S", "client file and access", check_sources, run, R, lines, content if isinstance(content, dict) else None)
    fr = guarded(R, "G", "the form's data file", check_form, run, R, lines, content if isinstance(content, dict) else {})
    if ledger is None or not isinstance(ledger, dict):
        R.add("FAIL", "B", "ledger.json missing (record the ledger as you read: run.py ledger add)")
    elif not shape:
        guarded(R, "B", "ledger", check_ledger, run, st, lines, ledger, cover_targets(run, ov, cross if dict_list(cross) else [], lead, content if isinstance(content, dict) else None), R)
    if isinstance(content, dict) and not shape:
        guarded(R, "C", "composed content", check_composed, run, content, R)
        guarded(R, "C", "source trace", check_content, run, lines, content, fr, refs, ov, R)
        guarded(R, "D", "rules", check_rules, run, lines, content, fr, ov, R)
        guarded(R, "L", "short notes", check_short, content, R)
        if stage in ("built", "final") and not R.fails:
            guarded(R, "E", "pdf", check_pdf, run, st, content, R)
        elif stage in ("built", "final"):
            R.add("FAIL", "E", "the PDF was not checked: fix the failures above first")
        if stage == "final" and not R.fails:
            guarded(R, "F", "hand-over", check_receipt, run, st, content, R, skip)
            guarded(R, "F", "driver", check_driver, run, R, skip)
        elif stage == "final":
            R.add("FAIL", "F", "hand-over not checked: fix the failures above first")
    return R, st, ledger, content


def claim_stats(run, lines, fr, content):
    """For the report: every 'Not discussed' claim and every 'not on the call' answer, with what the search found now (the search is repeated here) and whether it rests on a weak search."""
    lay = w.layout()
    rows = {r["id"]: r for _, _, r in iter_rows(content or {})}
    out = []
    for key, cl in load(os.path.join(run, w.CLAIMS), {}).items():
        if not isinstance(cl, dict) or cl.get("as") not in ("Not discussed", "Requested"):
            continue
        label = (rows.get(key) or {}).get("label", key)
        terms, curated = field_terms(lay, key, label)
        hits, docs = search_terms(run, lines, list(dict.fromkeys(terms + list(cl.get("terms") or []))))
        out.append({"key": key, "label": label, "hits": hits, "docs": docs, "sib": sibling_hits(lay, fr, key), "weak": not curated, "reason": S(cl.get("reviewed")), "kind": "claim", "as": cl.get("as")})
    for i in load(os.path.join(run, w.CROSS), []):
        a = i.get("answer") if isinstance(i, dict) else None
        if isinstance(a, dict) and a.get("r") == "not_on_call" and (a.get("hit_lines") or a.get("weak")):
            out.append({"key": i["key"], "label": i.get("label", i["key"]), "hits": list(a.get("hit_lines") or []), "docs": [], "sib": [], "weak": bool(a.get("weak")), "reason": S(a.get("reviewed")), "kind": "not_on_call"})
    return out


def dismissed_lines(ledger, lines, st, run=None):
    """[(line, text, reason)] of the decision/change/request/quote lines that were dismissed by a review instead of being handled by an entry (a hard line only on Paul's recorded answer)."""
    ents = [e for e in (ledger or {}).get("entries") or [] if isinstance(e, dict) and e.get("kind") in KINDS_MUST_COVER and isinstance(e.get("line"), int)]
    allowed = paul_allowed_lines(run) if run else {}
    why = {}
    for rv in (ledger or {}).get("scan_reviewed") or []:
        if not isinstance(rv, dict):
            continue
        if isinstance(rv.get("line"), int):
            why[rv["line"]] = S(rv.get("reason"))
        elif isinstance(rv.get("from"), int) and isinstance(rv.get("to"), int):
            for i in range(rv["from"], rv["to"] + 1):
                why.setdefault(i, S(rv.get("reason")))
    out = []
    for h in required_lines(lines, st):
        if h in why and line_resolution(h, lines, ents) is None:
            out.append((h, lines[h - 1].strip(), ("on Paul's recorded answer (%s): " % allowed[h]["said"][:40] if h in allowed else "") + why[h]))
    return out


def request_resolutions(run, ledger, lines, st, targets=None):
    """[(line number, directly on an entry?, phrase)] for EVERY request line: its text (the FULL line when it holds a hard word, otherwise cut at 60 characters), the products named in its window,
    and how it was handled (the entry, and what covers that entry, with each cover's group), or that it was dismissed (on Paul's recorded answer, for a hard line), or that it is not handled."""
    ents = [e for e in (ledger or {}).get("entries") or [] if isinstance(e, dict) and e.get("kind") in KINDS_MUST_COVER and isinstance(e.get("line"), int)]
    why = {}
    for rv in (ledger or {}).get("scan_reviewed") or []:
        if isinstance(rv, dict) and isinstance(rv.get("line"), int):
            why[rv["line"]] = S(rv.get("reason"))
        elif isinstance(rv, dict) and isinstance(rv.get("from"), int) and isinstance(rv.get("to"), int):
            for i in range(rv["from"], rv["to"] + 1):
                why.setdefault(i, S(rv.get("reason")))
    allowed = paul_allowed_lines(run, lines)
    out = []
    for h in required_lines(lines, st):
        e = line_resolution(h, lines, ents)
        full = lines[h - 1].strip()
        text = full if hard_word(full) else full[:60]                         # a hard-word line is never cut: Paul reads the whole request
        prods = [n for n, _ in products_in(window_text(lines, h))]
        where = '%s"%s"%s' % ("line %d " % h, text, (" [products: %s]" % ", ".join(prods)) if prods else "")
        if e is not None:
            out.append((h, e["line"] == h, '%s -> entry %s (%s, covered by %s)' % (where, e.get("id"), e.get("kind"), ", ".join(cover_label(c, targets) for c in e.get("covered_by") or []) or "nothing yet")))
        elif h in why:
            out.append((h, False, '%s dismissed%s: %s' % (where, " on Paul's recorded answer" if h in allowed else "", why[h][:50])))
        else:
            out.append((h, False, '%s NOT HANDLED' % where))
    return out


def freed_lines_text(run, lines, st):
    """One glance line for every hard request line that Paul's recorded answer freed: the line, the FULL question the chat recorded and Paul's recorded words."""
    allowed = paul_allowed_lines(run, lines)
    out = []
    for h in sorted(allowed):
        out.append("Line %d (%s) was freed on Paul's recorded answer. The question the chat recorded: \"%s\" Paul's recorded words (typed by the chat, attested): \"%s\""
                   % (h, lines[h - 1].strip()[:60], allowed[h]["question"], allowed[h]["said"]))
    return out


def source_report(run, st, content):
    rep = content.get("report") or {}
    out = []
    srcs = load(os.path.join(run, w.SOURCES), [])
    read = [e for e in srcs if isinstance(e, dict) and e.get("read") == "yes"]
    none = [e["kind"] for e in srcs if isinstance(e, dict) and "none" in e]
    rj = load(os.path.join(run, w.RUN), {})
    mode = rj.get("form_mode")
    form = content.get("form") or {}
    fp = load(os.path.join(run, w.FORMPDF), {})
    out.append("(a) Sources used: %s%s; the Teams transcript %s (%s to %s); %s; documents read: %s%s" % (
        ("the form's data file '%s' (schema %s, saved %s)" % (form.get("file"), form.get("schema"), form.get("modified"))) if mode == "form" else "NO form data file (%s, on Paul's word)" % mode,
        (" and its saved PDF '%s'" % fp["file"]) if fp.get("file") else (" (its saved PDF: none found)" if mode == "form" else ""),
        st.get("source"), st.get("first_ts"), st.get("last_ts"), "latest Overview " + ("read" if any(e.get("kind") == "Overview" for e in read) else "none on file"),
        ", ".join(sorted(S(e.get("ref") or source_ref(e)) for e in read)) or "none", ("; nothing on file for: " + ", ".join(none)) if none else ""))
    sts = rep.get("statuses") or {}
    out.append("(b) Form values by status: %s. Preset values (%d):" % (", ".join("%s %d" % kv for kv in sorted(sts.items())) or "none", len(rep.get("presets") or [])))
    for p in rep.get("presets") or []:
        out.append("      %s (%s): %s" % (p.get("label"), p.get("key"), p.get("done")))
    d = rep.get("differences") or []
    out.append("(c) Differences found (%d), both values shown:" % len(d))
    for x in d:
        out.append("      %s: form/first source %s | other %s (%s)" % (x.get("label"), x.get("form"), x.get("other"), x.get("where")))
    nd, rq = rep.get("not_discussed") or [], rep.get("requested") or []
    try:
        lines_ = w.read_lines(run)
        cs = claim_stats(run, lines_, load(os.path.join(run, w.FORM), {}), content)
    except Exception:
        cs = []
    over = [c for c in cs if c["kind"] == "claim" and c["as"] == "Not discussed" and (c["hits"] or c["docs"] or c["sib"])]
    over_req = [c for c in cs if c["kind"] == "claim" and c["as"] == "Requested" and c["hits"]]
    weakn = [c for c in cs if c["weak"] and c.get("as") != "Requested"]
    over_cross = [c for c in cs if c["kind"] == "not_on_call" and c["hits"]]
    out.append("(d) Left Not discussed (%d, each searched with the field's own search words; %d of them overrode search hits on a written reason, %d rest on a weak search; plus %d 'not on the call' answers that overrode hits): %s"
               % (len(nd), len(over), len([c for c in weakn if c["kind"] == "claim"]), len(over_cross), ", ".join("%s (%s)" % (l, k) for k, l in nd) or "none"))
    out.append("    Marked Requested (%d; %d of them overrode call hits on a written reason): %s" % (len(rq), len(over_req), ", ".join("%s (%s)" % (l, k) for k, l in rq) or "none"))
    if rep.get("standing"):
        out.append("    Standing rules applied: " + "; ".join(rep["standing"]))
    if rep.get("derived"):
        out.append("    Worked out by program: " + "; ".join(rep["derived"]))
    return out


def summary_lines(run, st, ledger, content):
    out = list(content.get("glance") or [])
    b = st.get("build") or {}
    f = b.get("font") or {}
    if not f.get("aptos"):
        out.append("FONT: the PDF is set in %s because Aptos is not installed where the skill ran (%s). Everything else of the look is as approved." % (f.get("family") or "?", ", ".join(f.get("ps_names") or ["?"])))
    fp = load(os.path.join(run, w.FORMPDF), {})
    if fp.get("missing"):
        out.append("The form's saved PDF was not found (%s): only its data file was used." % fp["missing"])
    if fp.get("paul_go_on"):
        out.append("The form's saved PDF did NOT match the data file and was not used; the chat recorded that Paul said to go on with the data file alone: \"%s\" (attested)." % S(fp["paul_go_on"])[:100])
    acc = load(os.path.join(run, w.ACCESS), [])
    routes = sorted({e.get("route") for e in acc if isinstance(e, dict)})
    out.append("Access routes used: %s" % ", ".join(routes))
    ents = (ledger or {}).get("entries") or []
    lines = w.read_lines(run)
    dismissed = len([i for i in reviewed_lines(ledger or {}) if 1 <= i <= len(lines)])
    total = st.get("total_lines") or 1
    req = required_lines(lines, st)
    dl = dismissed_lines(ledger, lines, st, run)
    out.append("Ledger: %d entries; %d lines of the call dismissed with a reason (%d%% of the %d lines); %d of the call's %d decision/change/request/quote lines were dismissed instead of recorded (%d%%)%s"
               % (len(ents), dismissed, round(100.0 * dismissed / total), total, len(dl), len(req), round(100.0 * len(dl) / (len(req) or 1)),
                  "  <-- MORE THAN A QUARTER OF THE CALL WAS DISMISSED: look at the reasons" if dismissed > 0.25 * total else ""))
    try:                                                              # the covering items' groups for the glance list (a synthetic folder has no inputs: then none are shown)
        inp_ = compose.load_inputs(run)
        targets_ = cover_targets(run, inp_["overlay"], inp_["cross"] if dict_list(inp_["cross"]) else [], inp_["lead"], content if isinstance(content, dict) and content else None)
    except Exception:
        targets_ = {}
    vline = values_line(ledger, targets_, lines)
    rr = request_resolutions(run, ledger, lines, st, targets_)
    if rr:
        cz = ((st or {}).get("scan") or {}).get("closing_from") or (len(lines) + 1)
        if len(rr) <= 40:
            shown, rest = rr, 0
        else:
            shown = [x for x in rr if not x[1] or x[0] >= cz]                          # every line not directly on an entry, and the whole closing minutes
            rest = len(rr) - len(shown)
        out.append("   how every request line was handled (%s): %s%s" % ("all %d" % len(rr) if not rest else "%d of %d: every line not directly on an entry and every line of the closing minutes" % (len(shown), len(rr)),
                                                                           "; ".join(x[2] for x in shown), ("; and %d more directly on an entry" % rest) if rest else ""))
    if vline:
        out.append(vline)
    out += freed_lines_text(run, lines, st)
    if dl:
        out.append("   dismissed lines (%s): %s%s" % ("all" if len(dl) <= 15 else "the first 15 of %d" % len(dl),
                   "; ".join("line %d (%s): %s" % (n, t[:40], r[:70]) for n, t, r in dl[:15]), "" if len(dl) <= 15 else " ..."))
    # 'Not discussed' that overrode the search
    cs = claim_stats(run, lines, load(os.path.join(run, w.FORM), {}), content)
    over = [c for c in cs if c["hits"] or c["docs"] or c["sib"]]
    if over:
        def what(c):
            if c["hits"]:
                return "call lines %s" % c["hits"][:4]
            return ("documents %s" % c["docs"][:2]) if c["docs"] else ("the form says " + "; ".join(c["sib"][:1]))
        out.append("%d 'Not discussed' / 'Requested' / 'not on the call' answer(s) overrode what the search found, on the chat's written reason (the program checks only its length, three different words, a cited hit line and a word from it): %s%s"
                   % (len(over), "; ".join("%s (%s), %s: %s" % (c["label"], c["key"], what(c), c["reason"][:60]) for c in over[:15]), " ..." if len(over) > 15 else ""))
    # Teams program and this skill's program: fingerprints to compare with the released ones
    rc = load(os.path.join(run, w.RECEIPT), {})
    tm = (rc.get("teams") or {}) if isinstance(rc, dict) else {}
    if tm.get("skill_dir"):
        out.append("Teams program fingerprint, sha256 first 16 characters (the Teams skill folder was NAMED BY THE CHAT; compare these with the released Teams skill): %s" % ", ".join("%s %s" % kv for kv in sorted(teams_fingerprint(tm["skill_dir"]).items())))
    out.append("This skill's program fingerprint (sha256, first 16 characters) %s (taken at the start of the run and compared at every step: a change during the run is detected unless someone also changes the checker; compare it with the released one)." % w.program_fingerprint()[:16])
    # text copies of documents are made by the chat
    docs_dir = os.path.join(run, w.DOCS)
    srcs = [e for e in load(os.path.join(run, w.SOURCES), []) if isinstance(e, dict) and e.get("read") == "yes" and e.get("text")]
    if srcs:
        out.append("Text copies of documents were MADE BY THE CHAT (their authenticity is attested; the program checks that they name the client and that quoted words and figures are in them). sha256: %s"
                   % "; ".join("%s %s" % (source_ref(e), w.sha256_file(os.path.join(docs_dir, source_ref(e) + ".txt"))[:12]) for e in srcs if os.path.exists(os.path.join(docs_dir, source_ref(e) + ".txt"))))
    sv = (rc.get("saved") or {}) if isinstance(rc, dict) else {}
    if S(sv.get("folder_spelling")).strip():
        out.append("The PDF was saved in a folder that is not named 'Surname, First': %s (the chat's reason: \"%s\")." % (S(sv.get("folder")), S(sv["folder_spelling"])[:100]))
    jn = load(os.path.join(run, w.RUN), {}).get("joint") or {}
    if jn.get("answer"):
        out.append("Joint meeting with a spouse: %s (the chat's evidence, attested: \"%s\")." % (jn["answer"], S(jn.get("evidence"))[:100]))
    return out


def report(R, st, ledger, content, stage, run=None):
    print("DELIVERY GATE  (stage: %s)" % stage)
    print("SKILL VERSION: %s" % w.version_line())
    for g in GROUP_ORDER:
        rows = [r for r in R.rows if r[1] == g]
        if not rows:
            continue
        print("\n" + GROUP_NAMES[g])
        for lvl, _, msg in rows:
            print("  [%-6s] %s" % (lvl, msg))
    fails, warns = len(R.fails), sum(1 for r in R.rows if r[0] == "WARN")
    attest = sum(1 for r in R.rows if r[0] == "ATTEST")
    print("\nRESULT: %s   (%d fail, %d warn, %d attested)" % ("PASS" if not fails else "FAIL", fails, warns, attest))
    if not fails and stage == "final" and ledger and content:
        k = len(st["chunks"])
        n_src = sum(len(r.get("src") or []) for _, _, r in iter_rows(content))
        print("\nSOURCE REPORT (for the hand-over message):")
        for ln in source_report(run or ".", st, content):
            print("  " + ln)
        print("\nWHAT PAUL SHOULD GLANCE AT (the program counted these; it cannot judge them):")
        for ln in summary_lines(run or ".", st, ledger, content):
            print("  - " + ln)
        print("\nPROVEN BY THE PROGRAM (it read the files itself or recomputed): the form's data file as read from its saved copy and its schema, client and date; that every value of it is in the form's saved PDF (exact amounts, whole words; a Yes/No or one-character value is not compared) or was looked at; "
              "that the form's summaries, drafted actions, parking list and cost counters are not printed; that every row has a source and each source is checked: the form field, a quote found in the transcript at that line, a quote found in a document's text copy (the copy is made by the chat: it is checked to name the client, not to be the real document; a document without a copy is only listed), a recomputation, a standing rule, a 'Not discussed' claim whose search the program repeated with the field's written search words; "
              "that every ledger entry has a line and quote found in the call and is covered by an item of a kind that can cover that kind of entry, that cites the call within 8 lines and shares a word of 4 letters or more with the entry (the KIND of each entry is chosen by the chat: the program cannot tell whether a request was filed under the right kind). A line of the call with one of the listed request words (the scan's decision/change/request words, and ask, quote, FNA, shortfall, RGAR, EGAR, authority, payslip, appointment, next meeting, set up, follow up, sign, please, can you, could you, would you, I'd like, organise, arrange, book, prepare, run the numbers, come back to me, send me, email me, let me know) counts as HANDLED when an entry of a kind that must be covered sits on it, or sits within 3 lines of it and shares a TOPIC word of 4 letters or more with it (a request verb or filler such as send, please, would does not count); a soft-word line may instead be dismissed with a reason that quotes it, a hard-word line (FNA, quote, shortfall, RGAR, EGAR, authority, payslip, appointment, next meeting, set up, follow up, reduced) only on Paul's recorded answer, and an entry on a quote line must be a quote_request, covered only by the quote row or request field of the product its line names; a quote line that names two products must be covered for each product by that product's own row or request field (a request field answered N/A or Not discussed covers nothing), and the quote-request conflict applies to 'Not discussed', 'N/A' and 'not on the call' (and to 'Requested') on that product's fields while the request is in the ledger. A credit-life line (credit life, creditor life, life cover on the bond) is a hard line, and only a fill or an answer of a credit-life field covers it; 'Requested' is refused while the call mentions the field, unless a reason cites that line and quotes it. A request worded with NONE of those words is not required by the program (inherent). The glance list shows how every request line was handled and every line dismissed by a review; "
              "that an overriding 'Not discussed' rests on a written reason the program checks only for length, three different words, a cited hit line and a word from it; totals to the cent from all rows; the standing ABIs; that a quote's insurer and basis are in a source it cites; policy and other long numbers only from a recorded schedule or Overview; "
              "that every overlay entry landed in the document; the PDF rebuilt from content.json and identical, with no page numbers, no stranded heading, no split row and the font really embedded; that the save size equals the local file and the folder path starts (after the drive and liferisk.co.za) with Company - Paul or Company - WR Clients\\Paul Kafentzis (Client Files) and the folder before 2. Fact Find is named 'Surname, First' of this client.")
        print("ONLY ATTESTED BY CLAUDE (typed or done in the chat, recorded, not proven): Paul's own words (the chat types them with run.py answer; the program checks only that they are on record, that a number used is in them, that the question was recorded with at most 10 field ids that its own text names, and, for a dismissals question, that it names at most 5 lines and that its text names at least 4 of the line's words (compared by their first 5 letters, in any order) for each line it frees; every line freed that way is shown on the glance list with the full question and his recorded words), the VALUE of a fill that covers a request line is the chat's own reading of the call; the program prints it on the glance list and refuses a bare No when the line asks for something, but it cannot know what the client really said, the joint-meeting answer and its evidence, the real send of the PDF in the chat and the real folder save and listing (the listing is typed by the chat), the visual check, the independent re-check, the six judgment sentences, the Fact Find Summary hand-over, "
              "that the Planner page was published and Paul said yes to the message, the Teams skill folder (it was NAMED BY THE CHAT: the program checks that it looks like the real one and prints its fingerprint for you to compare), the text copies of the Overview and Policy schedules (made by the chat), text in a document that has no recorded copy; and every rule that is only text, not a check (pending items stay pending, independent requests not waiting on each other, prior-year figures, garbled lines, comparing the Overview, other documents).")
        fnt = (st.get("build") or {}).get("font") or {}
        rc_ = load(os.path.join(run or ".", w.RECEIPT), {})
        tsd = ((rc_.get("teams") or {}) if isinstance(rc_, dict) else {}).get("skill_dir")
        print("\nDELIVERY LINE (copy into the reply, unedited):")
        print("Skill version: %s. Transcript read in full TWICE (Pass 1 and Pass 2, %d lines each, %d chunks, every chunk acknowledged in the ledger); %d ledger entries; "
              "every row of the Fact Find Transcript source-traced (%d sources); FONT: %s. Program fingerprint (sha256, first 16 characters) %s (a change during a run is detected unless someone also changes the checker; compare it with the released one)%s."
              % (w.version_short(), st["total_lines"], k, len(ledger["entries"]), n_src, "Aptos" if fnt.get("aptos") else "NOT Aptos: %s (a substitute)" % (fnt.get("family") or "?"),
                 w.program_fingerprint()[:16], ("; Teams program fingerprint, sha256 first 16 characters (folder named by the chat) %s" % ", ".join("%s %s" % kv for kv in sorted(teams_fingerprint(tsd).items()))) if tsd else ""))
    elif fails:
        print("\nNOT COMPLETE. You may not tell Paul this run is finished. Fix every FAIL above and re-run.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    ap.add_argument("--stage", choices=["pre", "built", "final"], default="final")
    a = ap.parse_args()
    run = os.path.abspath(a.run)
    R, st, ledger, content = run_checks(run, a.stage)
    report(R, st, ledger, content, a.stage, run)
    sys.exit(1 if R.fails else 0)


if __name__ == "__main__":
    main()
