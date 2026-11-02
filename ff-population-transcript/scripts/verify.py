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
            if w.norm(S(cc.get("first"))) != w.norm(cl["first"]) or w.norm(S(cc.get("surname"))) != w.norm(cl["surname"]):
                fail("content.json is for %s %s but Paul's request was for %s %s" % (cc.get("first"), cc.get("surname"), cl["first"], cl["surname"]))
        if lines is not None and w.norm(cl["surname"]) not in w.norm(" ".join(lines)):
            fail("this transcript never mentions the client's surname (%s): is it the right file?" % cl["surname"])
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
    if w.norm(fr["client"]["first"]) != w.norm(cl.get("first")) or w.norm(fr["client"]["surname"]) != w.norm(cl.get("surname")):
        fail("the form is for %s %s but Paul asked for %s %s" % (fr["client"]["first"], fr["client"]["surname"], cl.get("first"), cl.get("surname")))
    if fr["date"] != rj.get("date"):
        qs = [q for q in load(os.path.join(run, w.QUESTIONS), []) if isinstance(q, dict) and q.get("need") == "date" and len(S(q.get("paul_said")).strip()) >= 3]
        if not qs:
            fail("the form's Date completed is %s but Paul's meeting date is %s: ask Paul which is right (run.py ask --need date, then run.py answer)" % (fr["date"], rj.get("date")))
    # the form's own parking list, summaries and drafted actions are never a source and never printed
    try:
        raw = json.load(open(src_path, encoding="utf-8-sig"))
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
            ptxt = open(txt_path, encoding="utf-8").read()
            checked, missing = ffform.pdf_check(fr, ptxt)
            if json.dumps(missing, sort_keys=True) != json.dumps(fp.get("not_found"), sort_keys=True):
                fail("form_pdf.json is not what the program finds when it checks the data file against the PDF text (edited by hand?)")
            nt = w.norm(ptxt)
            for m in missing:
                rv = (fp.get("reviews") or {}).get(m["key"])
                if not rv or rv.get("result") not in ("format_only", "disagree"):
                    fail("%s (%r) is in the data file but not in the form's saved PDF, and nobody looked: run.py pdfreview" % (m["label"], m["value"]))
                elif w.norm(S(rv.get("quote"))) not in nt:
                    fail("pdfreview %s: the quote is not in the PDF text" % m["key"])
                elif rv["result"] == "disagree" and w.norm(S(rv.get("pdf_value"))) == w.norm(m["value"]):
                    fail("pdfreview %s: a disagreement needs a PDF value that differs from the data file's" % m["key"])
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
        if r == "not_on_call" and not i.get("row") and len(w.digits(i["value"])) >= 4 and re.search(r"\d", i["value"]):
            if w.digits(i["value"]) in w.digits(" ".join(lines or [])):
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
def cover_targets(run, ov, cross, lead):
    """Items a ledger entry can be covered by: overlay entries, answered cross-check fields, the lead search, the claims."""
    t = {}
    for name, it in compose.overlay_items(ov):
        lines = [s["line"] for s in it.get("src") or [] if isinstance(s, dict) and isinstance(s.get("line"), int)]
        t[it.get("id", name)] = lines
    for i in cross:
        a = i.get("answer")
        if isinstance(a, dict) and a.get("r") in ("same", "differs"):
            t[i["key"]] = [a["line"]] if isinstance(a.get("line"), int) else []
    if lead:
        t["lead"] = []
    for k in load(os.path.join(run, w.CLAIMS), {}):
        t["claim:" + k] = []
    return t


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
                R.add("FAIL", g, "%s (%s, line %d) is not covered by any fill, difference, note or answer: %r" % (where, kind, ln, e.get("quote")))
                bad += 1
            elif len(S(e.get("excluded")).strip()) < 8:
                R.add("FAIL", g, "%s (%s) is neither covered nor excluded with a reason" % (where, kind))
                bad += 1
            continue
        line_lists = [targets[c] for c in cov if targets[c]]
        if kind in KINDS_MUST_COVER and line_lists and not any(abs(x - ln) <= COVER_SPAN for ls in line_lists for x in ls):
            R.add("FAIL", g, "%s (%s, line %d): none of the covering items %s cites the call within %d lines of it, so they are not about the same thing" % (where, kind, ln, cov, COVER_SPAN))
            bad += 1
    if not bad:
        must = sum(1 for e in ents if e.get("kind") in KINDS_MUST_COVER)
        R.add("PASS", g, "%d ledger entries, every quote found verbatim; all %d gap/difference/contact/quote/next-step entries covered by an item that cites the same part of the call" % (len(ents), must))
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
        near = sorted(e["line"] for e in ents if isinstance(e.get("line"), int))
        reviewed = reviewed_lines(ledger)
        res = lambda h: h in reviewed or any(abs(h - n) <= 3 for n in near)  # noqa: E731
        unresolved = [h for h in sc["hits"] if not res(h)]
        if unresolved:
            closing = [h for h in unresolved if cz and h >= cz]
            R.add("FAIL", g, "%d decision/change/request keyword hits are not covered by a ledger entry within 3 lines or a recorded review%s: lines %s%s"
                  % (len(unresolved), " (%d in the closing minutes)" % len(closing) if closing else "", unresolved[:15], "..." if len(unresolved) > 15 else ""))
        else:
            R.add("PASS", g, "every decision/change/request keyword hit is covered by a ledger entry or a recorded review")


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
    paul_words = {S(q.get("paul_said")).strip() for q in (ov.get("asked_paul") or []) if isinstance(q, dict)} | {S(q.get("paul_said")).strip() for q in questions if isinstance(q, dict)}
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
                if len(S(s["paul"]).strip()) < 3 or S(s["paul"]).strip() not in paul_words:
                    R.add("FAIL", g, "%s: Paul's words %r are not recorded in an answered question (asked_paul or run.py answer)" % (rid, s.get("paul")))
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
        if rj.get("spouse") and r.get("status") == "filled" and any("line" in s for s in srcs if isinstance(s, dict)):
            if not any(len(S(it.get("attrib")).strip()) >= 10 for _, it in compose.overlay_items(ov) if rid in (it.get("key"), "flag." + S(it.get("id")))):
                R.add("WARN", g, "%s: two spouses in one meeting: say in `attrib` why this call statement belongs to this spouse (from its content, not the speaker label)" % rid)
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
POLICY_NO = re.compile(r"(?i)\bpolic(?:y|ies)\s*(?:no\.?|number|nr\.?|#)\s*[:\-]?\s*([A-Z0-9][A-Z0-9\-/]{4,})")
FLAG_REF = re.compile(r"(?i)\bsee\s+(?:the\s+)?(flag|flags|notes?)\b")
YEAR_LINE = re.compile(r"^(19|20)\d{2}\s*:\s*\S")
DEPENDS = re.compile(r"\b(pending|once|until|after|when|awaiting|waiting for)\b", re.I)
QUOTE_WORDS = re.compile(r"\b(FNA|shortfall|reduced quote|quote)\b", re.I)
DOC_WORDS = re.compile(r"\b(report|medical|psychiatric|document|payslip|statement)\b", re.I)


def search_terms(run, lines, terms):
    """Lines of the call (and recorded documents) that mention any of the terms."""
    hits = []
    nterms = [" %s " % w.norm(t) for t in terms if w.norm(t)]
    for i, ln in enumerate(lines, 1):
        n = " %s " % w.norm(ln)
        if any(t in n for t in nterms):
            hits.append(i)
    docs = []
    d = os.path.join(run, w.DOCS)
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            t = " %s " % w.norm(open(os.path.join(d, f), encoding="utf-8", errors="replace").read())
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
        fail("a quote request has no insurer or no New Business/Servicing (%s): there is no default. ASK PAUL: \"%s\" and record his words (asked_paul, then overlay `quotes`)" % (quotes_un[:4], ASK_QUOTE))
    # 'Not discussed' is a claim: the search is repeated here
    claims = load(os.path.join(run, w.CLAIMS), {})
    lead = load(os.path.join(run, w.LEAD), {})
    for key, cl in claims.items():
        word = S(cl.get("as"))
        if word not in ("Not discussed", "Requested", "N/A"):
            fail("claim %s: %r is not allowed (Not discussed, Requested or N/A)" % (key, word))
            continue
        terms = cl.get("terms") or []
        if word == "Not discussed":
            hits, docs = search_terms(run, lines, terms)
            if (hits or docs) and len(S(cl.get("reviewed")).strip()) < 15:
                fail("claim %s 'Not discussed': the search still finds %s%s. Read it, then fill the field or record why it does not answer it (run.py claim --reviewed)" % (key, ("call lines %s" % hits[:6]) if hits else "", (" and documents %s" % docs) if docs else ""))
            if not terms:
                fail("claim %s: no search terms were recorded" % key)
            if key in CONTACT_KEYS and not lead.get("searched"):
                fail("claim %s: contact details may be called 'Not discussed' only after the lead-source search and the documents were checked (run.py lead)" % key)
        elif word == "Requested":
            if not key.startswith("debts.") or "outlook" not in S(cl.get("searched")).lower() or len(S(cl.get("searched"))) < 20:
                fail("claim %s 'Requested': only a debt detail that is truly missing after the form, the call, the Overview, other documents AND Outlook were checked (say so in --searched)" % key)
        elif len(S(cl.get("reviewed")).strip()) < 15:
            fail("claim %s 'N/A' needs the reason (--reviewed)" % key)
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
                if m.group(1) not in pns:
                    fail("%s prints policy number %r that is not confirmed by a policy schedule (overlay `policy_numbers`)" % (rid, m.group(1)))
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
    if not emb or any(n not in claimed for n in emb):
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
    else:
        R.add("WARN", g, "FONT USED: %s (embedded in the PDF: %s). Aptos was NOT found on this computer, so this is a substitute: tell Paul (never say Aptos)" % (rec.get("family") or "?", ", ".join(emb)))
    if not probs:
        R.add("PASS", g, "PDF '%s': %d page(s), text identical to what content.json produces, no page numbers, no heading stranded, no row split across pages, one PDF only (no Word file), page images rendered: %s"
              % (content["file_name"], len(pages), ", ".join(pngs)))


# ---------------------------------------------------------------- F receipt and driver
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
        if "2. Fact Find" not in str(sv["folder"]):
            fail("saved.folder is not the client's '2. Fact Find' folder")
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
    if not text(tm, "run_folder", "next_appointment_carried", n=3):
        fail("teams{run_folder, next_appointment_carried}: the Planner note page and the message to Sitamah are made ONLY by client-teams-transcript-skill (run.py start --type first); record its run folder and what next appointment it carries")
    else:
        tr = load(os.path.join(S(tm["run_folder"]), w.RUN), None)
        cl = rj.get("client") or {}
        if not isinstance(tr, dict):
            fail("teams.run_folder %r holds no run.json: the Teams program was not started there" % tm["run_folder"])
        elif tr.get("meeting_type") != "first" or w.norm((tr.get("client") or {}).get("surname")) != w.norm(cl.get("surname")) or tr.get("date") != rj.get("date"):
            fail("the Teams run at %r is not a first-meeting run for %s %s on %s" % (tm["run_folder"], cl.get("first"), cl.get("surname"), rj.get("date")))
        else:
            R.add("ATTEST", g, "Planner note and message to Sitamah: made by client-teams-transcript-skill (a first-meeting run for this client and date exists at %s; its own checker is the proof of those two); next appointment carried: %s"
                  % (tm["run_folder"], str(tm["next_appointment_carried"])[:60]))
    if rj.get("spouse"):
        sp = rc.get("spouse") if isinstance(rc.get("spouse"), dict) else {}
        if not text(sp, "cross_check", n=12):
            fail("spouse.cross_check: say the result of the search for the other spouse's data in this PDF (run.py spouse)")
        else:
            R.add("ATTEST", g, "other spouse's data searched for: " + str(sp["cross_check"])[:80])


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
        R.add("PASS", g, "every step before the final check was completed through the driver, in order")


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
    lines = w.read_lines(run)
    ledger = load(os.path.join(run, w.LEDGER), None)
    content = load(os.path.join(run, w.CONTENT), None)
    ov = load(os.path.join(run, w.OVERLAY), {})
    cross = load(os.path.join(run, w.CROSS), [])
    lead = load(os.path.join(run, w.LEAD), {})
    shape = compose.validate_overlay(ov)
    if not isinstance(content, dict):
        R.add("FAIL", "C", "content.json missing (run `run.py compose` after the overlay is written)")
    for e in shape:
        R.add("FAIL", "C", "overlay.json shape: " + e)
    refs = guarded(R, "S", "client file and access", check_sources, run, R, lines, content if isinstance(content, dict) else None)
    fr = guarded(R, "G", "the form's data file", check_form, run, R, lines, content if isinstance(content, dict) else {})
    if ledger is None or not isinstance(ledger, dict):
        R.add("FAIL", "B", "ledger.json missing (record the ledger as you read: run.py ledger add)")
    elif not shape:
        guarded(R, "B", "ledger", check_ledger, run, st, lines, ledger, cover_targets(run, ov, cross if dict_list(cross) else [], lead), R)
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
    out.append("(d) Left Not discussed (%d, each searched): %s" % (len(nd), ", ".join("%s (%s)" % (l, k) for k, l in nd) or "none"))
    out.append("    Marked Requested (%d): %s" % (len(rq), ", ".join("%s (%s)" % (l, k) for k, l in rq) or "none"))
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
    acc = load(os.path.join(run, w.ACCESS), [])
    routes = sorted({e.get("route") for e in acc if isinstance(e, dict)})
    out.append("Access routes used: %s" % ", ".join(routes))
    ents = (ledger or {}).get("entries") or []
    out.append("Ledger: %d entries; %d keyword-scan lines dismissed with a reason" % (len(ents), len(reviewed_lines(ledger or {}))))
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
        print("\nPROVEN BY PROGRAM: the form's data file read by program and every value of it found in the form's saved PDF (or reviewed); every value's source (form field, quote found in the call, recorded document, "
              "recomputation, standing rule, search-backed claim); totals to the cent; standing ABIs; quote insurer and basis; the PDF rebuilt from content.json and identical; no page numbers; no split rows; "
              "the font really embedded; the save size equals the local file.")
        print("ONLY ATTESTED BY CLAUDE: sending the PDF in the chat, the folder save and listing (the sizes are compared by the program), the visual check, the independent re-check, the judgment sentences, "
              "the Fact Find Summary and the Planner note/message made by the other two skills.")
        fnt = (st.get("build") or {}).get("font") or {}
        print("\nDELIVERY LINE (copy into the reply, unedited):")
        print("Skill version: %s. Transcript read in full TWICE (Pass 1 and Pass 2, %d lines each, %d chunks, every chunk acknowledged in the ledger); %d ledger entries; "
              "every row of the Fact Find Transcript source-traced (%d sources); FONT: %s."
              % (w.version_short(), st["total_lines"], k, len(ledger["entries"]), n_src, "Aptos" if fnt.get("aptos") else "NOT Aptos: %s (a substitute)" % (fnt.get("family") or "?")))
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
