#!/usr/bin/env python3
"""Delivery gate for the client-teams-transcript skill.

  verify.py <run_dir> [--stage pre|built|final]

Stages (each includes the one before):
  pre    A reading lock, S client file and access, B ledger and coverage, C source trace, D mandatory checks
  built  + E the outputs on disk are exactly what content.json produces
  final  + F the hand-over receipt and the step driver (default)

Prints PASS / FAIL / WARN per item and a RESULT line. Exit code 0 only on PASS.
ATTEST rows are things only Claude can do (chat hand-over, saving through the device bridge, the Zapier
send); they are recorded, not machine-proven, and are labelled that way. A malformed file gives a FAIL
line, never a crash.
"""
import argparse
import datetime as dt
import html
import json
import os
import re
import subprocess
import sys
import tempfile

import tx
import wrlib as w

KINDS_MUST_COVER = {"decision", "change", "request", "instruction", "offer", "acceptance", "refusal", "hold"}
KINDS_OPTIONAL = {"fact", "figure"}
MEETING_TYPES = ("followup", "first", "whatsapp")
GROUP_ORDER = "ASBCDEF"
GROUP_NAMES = {
    "A": "A. Reading lock",
    "S": "S. Client file and access (S3, S4)",
    "B": "B. Ledger and coverage",
    "C": "C. Source trace",
    "D": "D. Mandatory checks",
    "E": "E. Outputs",
    "F": "F. Hand-over (attested by Claude, not machine-proven) and the step driver",
}
QUOTE_WINDOW = 2          # a quote may sit on the cited line or within 2 lines of it (wrapped speech)
COVER_SPAN = 8            # a covering item must cite the transcript within this many lines of the ledger entry
ITEM_QUOTE_MIN = 10       # characters (after cleaning) a quote must have to count as a source for an item
LEDGER_QUOTE_MIN = 6
ALLOWED_ROUTES = w.ROUTES + ("user", "passed")
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HANDOVER_KEYS = ("planner_page", "pdf_sent_in_chat", "saved", "png_visual_check", "applications_handoff",
                 "independent_check", "judgment", "revised_quote_draft")
JUDGMENT_KEYS = ("quotes_named", "benefits_from_quote", "nothing_to_confirm_on_file", "independent_actions", "garbled_flagged")


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
    R.add("PASS" if p1 else "FAIL", g, "Pass 1 served all %d chunks in order" % k if p1
          else "Pass 1 has NOT served every chunk (run `tx.py status`)")
    R.add("PASS" if p2 else "FAIL", g, "Pass 2 served all %d chunks in order" % k if p2
          else "Pass 2 has NOT served every chunk: the Two-Read Lock is not met")
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


# ---------------------------------------------------------------- S client file and access
def meeting_type_of(run, content):
    if isinstance(content, dict) and content.get("meeting_type") in MEETING_TYPES:
        return content["meeting_type"]
    rj = load(os.path.join(run, w.RUN), {})
    return rj.get("meeting_type") if isinstance(rj, dict) else None


def source_ref(e):
    ref = S(e.get("ref")).strip()
    if ref:
        return ref
    base = re.split(r"[\\/]", S(e.get("path")).strip())[-1]
    return re.sub(r"\.[A-Za-z0-9]{1,5}$", "", base)


def check_sources(run, mt, R, lines=None, content=None):
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
        return

    # the run is tied to what Paul asked for, and to the real transcript
    cl = rj.get("client") or {}
    if not (S(cl.get("first")) and S(cl.get("surname")) and S(rj.get("date"))):
        fail("the run was not started with the client and meeting date from Paul's message (run.py start --client ... --date ...)")
    else:
        try:
            dt.datetime.strptime(rj["date"], "%d/%m/%Y")
        except ValueError:
            fail("the meeting date %r is not a real date (DD/MM/YYYY)" % rj["date"])
        if isinstance(content, dict):
            cc = content.get("client") if isinstance(content.get("client"), dict) else {}
            if w.norm(S(cc.get("first"))) != w.norm(cl["first"]) or w.norm(S(cc.get("surname"))) != w.norm(cl["surname"]):
                fail("content.json is for %s %s but Paul's request was for %s %s" % (cc.get("first"), cc.get("surname"), cl["first"], cl["surname"]))
            if S(content.get("meeting_date")) != rj["date"]:
                fail("content.json has meeting_date %s but Paul's request was for %s" % (content.get("meeting_date"), rj["date"]))
        if lines is not None and w.norm(cl["surname"]) not in w.norm(" ".join(lines)):
            (R.add("WARN", g, "the notes do not mention the client's surname (%s): check it is the right file" % cl["surname"])
             if mt == "whatsapp" else fail("this transcript never mentions the client's surname (%s): is it the right file?" % cl["surname"]))

    need_kinds = w.REQUIRED_SOURCE_KINDS.get(mt, w.SOURCE_KINDS)
    refs = {}
    for e in sources:
        k = e.get("kind")
        if k not in w.SOURCE_KINDS:
            fail("source with unknown kind %r (allowed: %s)" % (k, w.SOURCE_KINDS))
        elif "none" in e:
            if len(S(e.get("none")).strip()) < 8:
                fail("source kind %s: 'none' needs a reason (what was searched and not found)" % k)
            tried = {x.get("route") for x in access if x.get("need") == k and x.get("result") == "fail"}
            if len(tried & set(w.ROUTES)) < 2:
                fail("source kind %s was recorded as 'none on file' but the searches are not logged: try at least two routes and log each with run.py access --need %s ..." % (k, k))
        elif e.get("read") == "yes":
            if not S(e.get("path")).strip() or not S(e.get("date")).strip():
                fail("source %s: a document that was read needs its path and date" % k)
            ref = source_ref(e)
            if ref in refs:
                fail("two sources share the reference %r: give each its own --ref" % ref)
            refs[ref] = k
        else:
            fail("source %s: record read=yes with path and date, or a 'none' reason" % k)
    have = {e.get("kind") for e in sources if e.get("read") == "yes" or len(S(e.get("none")).strip()) >= 8}
    missing = [k for k in need_kinds if k not in have]
    if missing:
        fail("client-file sources not accounted for: %s (read them from the client's file, or record why none exist; Paul is asked last)" % missing)

    by_need = {}
    for e in access:
        if e.get("route") not in ALLOWED_ROUTES or e.get("result") not in ("ok", "fail") or not S(e.get("need")).strip():
            fail("access_log entry malformed (need, route in %s, result ok|fail): %s" % (ALLOWED_ROUTES, e))
            continue
        by_need.setdefault(e["need"], []).append(e)
    if "transcript" not in by_need or not any(e["result"] == "ok" for e in by_need["transcript"]):
        fail("the transcript has no successful access entry (run.py access --need transcript ... --result ok)")
    asked = {q.get("need") for q in questions}
    for need, es in by_need.items():
        if any(e["result"] == "ok" for e in es) or need in {k for k in w.SOURCE_KINDS}:
            continue
        tried_fail = {e["route"] for e in es if e["result"] == "fail"}
        untried = [r for r in w.ROUTES if r not in tried_fail]
        if untried:
            fail("'%s' could not be fetched but these routes were never tried: %s. Never say 'I cannot access your files' until all three failed" % (need, untried))
        elif need not in asked:
            fail("'%s' failed on all three routes but nothing was recorded for Paul: use run.py ask with the errors" % need)
    for q in questions:
        if len(S(q.get("question")).strip()) < 8 or len(S(q.get("searched")).strip()) < 8:
            fail("a question to Paul needs the question and what was searched first: %s" % q)
        if q.get("need") in by_need and any(e["result"] == "ok" for e in by_need[q["need"]]):
            R.add("WARN", g, "question about '%s' was recorded although that need was later fetched: do not ask Paul" % q["need"])
    if not probs:
        R.add("PASS", g, "client and date match Paul's request; client-file sources accounted for (%d read, %d kinds required); access log has %d entries for %d need(s); %d question(s) to Paul, each with what was searched"
              % (len(refs), len(need_kinds), len(access), len(by_need), len(questions)))
    return refs


# ---------------------------------------------------------------- helpers for B/C/D
def item_index(content):
    idx, dup = {}, []
    for lst, it in w.all_items(content):
        iid = it.get("id") if isinstance(it, dict) else None
        if not isinstance(iid, str) or not iid:
            continue
        if iid in idx:
            dup.append(iid)
        idx[iid] = (lst, it)
    return idx, dup


def window_slice(lines, line):
    lo, hi = max(0, line - 1 - QUOTE_WINDOW), min(len(lines), line + QUOTE_WINDOW)
    return " ".join(lines[lo:hi])


def window_norm(lines, line):
    return w.norm(window_slice(lines, line))


def quote_ok(lines, line, quote, minimum=4):
    q = w.norm(quote)
    return len(q) >= minimum and q in window_norm(lines, line)


NUM = re.compile(r"\d[\d ,]*(?:\.\d+)?")


def num_forms(text):
    out = set()
    for m in NUM.finditer(text):
        t = m.group(0).replace(" ", "").replace(",", "").strip(".")
        if "." in t:
            t = t.rstrip("0").rstrip(".")
        out.add(t)
    return out


MONEY = re.compile(r"R\s?(\d[\d ,]*(?:\.\d+)?)")
LONGNUM = re.compile(r"(?<![\d.])(\d{6,})(?!\d)")
PCT = re.compile(r"(\d+(?:\.\d+)?)\s?%")


def figures(text):
    """Money amounts, 6+ digit numbers (quote/policy numbers) and percentages in an item's text."""
    toks = set()
    for rx in (MONEY, LONGNUM, PCT):
        for m in rx.finditer(text):
            toks |= num_forms(m.group(1))
    return {t for t in toks if t}


def doc_text(run, ref):
    p = os.path.join(run, w.DOCS, ref + ".txt")
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read()


# ---------------------------------------------------------------- B ledger and coverage
def near_source(items, ln):
    for it in items:
        for s in it.get("src") or []:
            if isinstance(s, dict) and isinstance(s.get("line"), int) and abs(s["line"] - ln) <= COVER_SPAN:
                return True
    return False


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


def check_ledger(run, st, lines, ledger, idx, R):
    g = "B"
    ents = ledger.get("entries") if isinstance(ledger, dict) else None
    if not ents or not dict_list(ents):
        R.add("FAIL", g, "ledger.json has no entries: Pass 1 must record every decision, request, change and figure")
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
            R.add("FAIL", g, "%s: kind '%s' not one of %s" % (where, kind, sorted(KINDS_MUST_COVER | KINDS_OPTIONAL)))
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
        unknown = [c for c in cov if c not in idx]
        if unknown:
            R.add("FAIL", g, "%s: covered_by names items that do not exist in content.json: %s" % (where, unknown))
            bad += 1
            continue
        if not cov:
            if kind in KINDS_MUST_COVER:
                R.add("FAIL", g, "%s (%s, line %d) is not covered by any bullet or action: %r" % (where, kind, ln, e.get("quote")))
                bad += 1
            elif len(S(e.get("excluded")).strip()) < 8:
                R.add("FAIL", g, "%s (%s) is neither covered nor excluded with a reason" % (where, kind))
                bad += 1
            continue
        lists = [idx[c][0] for c in cov]
        items = [idx[c][1] for c in cov]
        if kind in KINDS_MUST_COVER and not near_source(items, ln):
            R.add("FAIL", g, "%s (%s, line %d): none of the covering items %s cites the transcript within %d lines of it, so they are not about the same thing"
                  % (where, kind, ln, cov, COVER_SPAN))
            bad += 1
        if kind == "change" and not any("changed" in (S(i.get("status")) + S(i.get("tag"))).lower() for i in items):
            R.add("FAIL", g, "%s (change, line %d) is not recorded as CHANGED (before -> after) in any covering item" % (where, ln))
            bad += 1
        if kind in ("request", "instruction", "offer") and not any(
                lst == "actions" or i.get("status") or i.get("tag") for lst, i in zip(lists, items)):
            R.add("FAIL", g, "%s (%s, line %d) must map to a Sitamah action or a status line" % (where, kind, ln))
            bad += 1
        if kind == "hold" and all(lst == "actions" for lst in lists):
            R.add("FAIL", g, "%s (hold, line %d) is covered only by an action: items on hold/left with the client are reported as on hold, not as tasks" % (where, ln))
            bad += 1
    if not bad:
        must = sum(1 for e in ents if e.get("kind") in KINDS_MUST_COVER)
        R.add("PASS", g, "%d ledger entries, every quote found verbatim; all %d decision/request/change entries covered by an item that cites the same part of the call" % (len(ents), must))

    # every chunk of both reads produced entries or a reasoned acknowledgement
    k = len(st["chunks"])
    gaps = [(p, c) for p in (1, 2) for c in range(1, k + 1) if not tx.chunk_acked(st, ledger, p, c)]
    if gaps:
        R.add("FAIL", g, "chunks read without a ledger entry or acknowledgement (pass, chunk): %s" % gaps[:12])
    else:
        R.add("PASS", g, "every chunk of both passes has ledger entries or a reasoned acknowledgement")

    sc = st["scan"] or {}
    cz = sc.get("closing_from")
    if cz and not any(isinstance(e.get("line"), int) and e["line"] >= cz for e in ents):
        R.add("WARN", g, "no ledger entry from the closing minutes (lines %d+): the skill warns requests there are the easiest to miss" % cz)
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
        low_unres = [h for h in sc.get("low_hits", []) if cz and h >= cz and not res(h)]
        if low_unres:
            R.add("WARN", g, "%d closing-minute lines mention figures/days/products with no nearby ledger entry (lines %s): check them" % (len(low_unres), low_unres[:12]))


# ---------------------------------------------------------------- shape check (clear FAIL lines, never a crash)
def validate_shape(content):
    errs = []
    if not isinstance(content, dict):
        return ["content.json must be an object"]
    for k in ("meeting_type", "meeting_date", "topic"):
        if k in content and not isinstance(content[k], str):
            errs.append("%s must be text" % k)
    c = content.get("client")
    if not isinstance(c, dict) or not isinstance(c.get("first"), str) or not isinstance(c.get("surname"), str):
        errs.append('client must look like {"first": "...", "surname": "..."}')
    for name in ("since_last", "applications", "actions", "next_steps"):
        v = content.get(name, [])
        if not dict_list(v):
            errs.append("%s must be a list of {id, text, src} objects" % name)
    areas = content.get("areas", [])
    if not isinstance(areas, list) or not all(isinstance(a, dict) and isinstance(a.get("key"), str) and dict_list(a.get("bullets", [])) for a in areas):
        errs.append('areas must be a LIST like [{"key": "risk", "bullets": [{id, text, src}]}], not an object')
    na = content.get("next_appointment")
    if na is not None and not isinstance(na, dict):
        errs.append("next_appointment must be an object {id, text, src}")
    for lst, it in (w.all_items(content) if not errs else []):
        if not isinstance(it.get("id", ""), str) or not isinstance(it.get("text", ""), str):
            errs.append("every item needs text and an id as plain text (%s)" % lst)
        for fld in ("status", "tag"):
            if fld in it and not isinstance(it[fld], str):
                errs.append("%s of item %s must be text" % (fld, it.get("id")))
        src = it.get("src", [])
        if not dict_list(src):
            errs.append('src of item %s must be a list like [{"line": 12, "quote": "exact words"}]' % it.get("id"))
    ck = content.get("checks")
    if ck is not None:
        if not isinstance(ck, dict):
            errs.append("checks must be an object")
        else:
            for k in ("correspondence", "owner_change", "cession", "credit_life", "applications"):
                if k in ck and not isinstance(ck[k], dict):
                    errs.append("checks.%s must be an object" % k)
            for k, f in (("owner_change", "action_id"), ("cession", "action_id"), ("credit_life", "bullet_id")):
                if isinstance(ck.get(k), dict) and f in ck[k] and not isinstance(ck[k][f], str):
                    errs.append("checks.%s.%s must be one item id as text" % (k, f))
            cl = ck.get("credit_life")
            if isinstance(cl, dict) and not isinstance(cl.get("action_ids", []), list):
                errs.append("checks.credit_life.action_ids must be a list of item ids")
    return errs


# ---------------------------------------------------------------- C source trace
OWNER_BAD = re.compile(r"(?:^|[;]\s*|\band\s+)Paul to\b|\bPaul (?:will|should|must)\b|\bI'?ll\b|\bI will\b")
CHASE = re.compile(r"\b(chase|follow[- ]up|remind)\b", re.I)
LEFT_WITH_CLIENT = ("get back to", "leave it", "come back to you", "let you know")
DEPENDS = re.compile(r"\b(once|pending|until|after|when)\b", re.I)
ID13 = re.compile(r"(?<!\d)\d{13}(?!\d)")
ID10 = re.compile(r"(?<!\d)\d{10}(?!\d)")


def all_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from all_strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from all_strings(v)


def check_content(run, st, lines, content, idx, dup, refs, R):
    g = "C"
    mt = content.get("meeting_type")
    if mt not in MEETING_TYPES:
        R.add("FAIL", g, "meeting_type must be one of %s" % (MEETING_TYPES,))
        return
    c = content.get("client") or {}
    if not (S(c.get("first")).strip() and S(c.get("surname")).strip()):
        R.add("FAIL", g, "client.first and client.surname are required (the filename is built from them)")
    if not w.short_date(content.get("meeting_date")):
        R.add("FAIL", g, "meeting_date must be DD/MM/YYYY")
    else:
        try:
            dt.datetime.strptime(content["meeting_date"], "%d/%m/%Y")
        except ValueError:
            R.add("FAIL", g, "meeting_date %s is not a real date" % content["meeting_date"])
    if mt == "whatsapp" and not re.fullmatch(r"\d{1,2}:\d{2}", S(content.get("meeting_time"))):
        R.add("FAIL", g, "meeting_time (HH:MM) is required for a WhatsApp call")
    if not S(content.get("topic")).strip():
        R.add("FAIL", g, "topic is required (the italic line under the Planner title)")
    if mt != "first" and not S(content.get("opening")).strip():
        R.add("FAIL", g, "opening sentence is required for the PDF")
    if dup:
        R.add("FAIL", g, "duplicate item ids: %s" % sorted(set(dup)))
    keys = [a.get("key") for a in content.get("areas") or []]
    if any(k not in w.AREA_KEYS for k in keys) or len(keys) != len(set(keys)):
        R.add("FAIL", g, "areas keys must be unique and from %s (got %s)" % (w.AREA_KEYS, keys))
    if mt == "first" and content.get("since_last"):
        R.add("FAIL", g, "a first/Fact Find meeting has nothing to carry forward: since_last must be empty")
    if mt != "first" and not content.get("since_last") and len(S(content.get("since_last_none")).strip()) < 10:
        R.add("FAIL", g, "since_last is empty: carry forward what is resolved, still open, new or changed since the last meeting, or give since_last_none (why there is nothing to carry forward)")
    na = content.get("next_appointment")
    if not isinstance(na, dict):
        R.add("FAIL", g, "next_appointment {id, text, src} is required")
    elif mt != "whatsapp":
        # the Teams message to Sitamah depends on these (ff-population-transcript Step 8)
        n = content.get("appointment_number")
        srcs = load(os.path.join(run, w.SOURCES), [])
        if not (isinstance(n, int) and not isinstance(n, bool) and n >= 1):
            R.add("FAIL", g, "appointment_number must be 1, 2, 3... (count the Teams meetings with this client on file, plus this one; never guess)")
        else:
            earlier = sum(1 for e in srcs if isinstance(e, dict) and e.get("kind") == "Earlier Note" and e.get("read") == "yes")
            if n > earlier + 2:
                R.add("FAIL", g, "appointment_number %d is more than the client's file supports (%d earlier note(s) read, so at most %d)" % (n, earlier, earlier + 2))
        status = content.get("client_status")
        if status not in w.CLIENT_STATUSES:
            R.add("FAIL", g, "client_status must be \"Review Client\" or \"Prospect\": decide it from where the client's folder sits (Company - WR Clients\\Paul Kafentzis (Client Files) = Review Client; Company - Paul\\New Business = Prospect); if unclear, ask Paul")
        else:
            seen = w.status_from_paths(srcs if isinstance(srcs, list) else [])
            if len(S(content.get("client_status_basis")).strip()) < 10:
                R.add("FAIL", g, "client_status_basis: say where the client's folder sits (the path), so the label can be checked")
            elif seen and seen != status:
                R.add("FAIL", g, "client_status is %s but the folders read for this client sit where a %s's would: if it is unclear, ask Paul (run.py ask)" % (status, seen))
        if len(S(content.get("appointment_number_basis")).strip()) < 10:
            R.add("FAIL", g, "appointment_number_basis: say which earlier meetings/files on the client's file give that number")
        agreed = na.get("agreed")
        if not isinstance(agreed, bool):
            R.add("FAIL", g, "next_appointment.agreed must be true (a real agreed/booked follow-up) or false (vague or none)")
        else:
            text = S(na.get("text"))
            has_date = bool(w.AGREED_RE.search(text))
            vague = bool(w.VAGUE_RE.search(text))
            if agreed and (not has_date or vague):
                R.add("FAIL", g, "next_appointment.agreed is true but the text %r does not show a specific agreed date/time (or sounds vague): a vague intention is not a follow-up appointment" % text)
            if not agreed and has_date and not vague:
                R.add("WARN", g, "next_appointment.agreed is false but the text %r looks like a real date: is the follow-up sentence left out on purpose?" % text)
        if len(S(na.get("check")).strip()) < 10:
            R.add("FAIL", g, "next_appointment.check: one line on what the Summary and the Planner note say about the next appointment, and so why the follow-up sentence is in or out")

    n_src, problems = 0, 0
    unchecked = {}
    refs = refs or {}
    for lst, it in w.all_items(content):
        iid = it.get("id", "?")
        if not S(it.get("id")) or not S(it.get("text")).strip():
            R.add("FAIL", g, "%s: every item needs an id and text" % lst)
            problems += 1
            continue
        if lst == "next_appointment" and iid != "next":
            R.add("FAIL", g, "next_appointment id must be 'next'")
            problems += 1
        srcs = it.get("src") or []
        if not srcs:
            R.add("FAIL", g, "item %s has no source: 'anything with no source is deleted' (%r)" % (iid, it["text"][:70]))
            problems += 1
            continue
        evidence = []            # raw text each source supports the item with
        item_unchecked = False
        for s in srcs:
            n_src += 1
            if "line" in s:
                ln = s.get("line")
                if not isinstance(ln, int) or not 1 <= ln <= len(lines) or not quote_ok(lines, ln, S(s.get("quote")), ITEM_QUOTE_MIN):
                    R.add("FAIL", g, "item %s: source quote not found at transcript line %r (quotes must be at least %d characters of the exact words): %r" % (iid, ln, ITEM_QUOTE_MIN, s.get("quote")))
                    problems += 1
                else:
                    evidence.append(window_slice(lines, ln))
            elif "doc" in s:
                ref, kind = S(s.get("ref")).strip(), s.get("doc")
                if kind not in w.DOC_TYPES or not ref or len(w.norm(S(s.get("quote")))) < 6:
                    R.add("FAIL", g, "item %s: a document source needs doc (one of %s), ref and quote" % (iid, w.DOC_TYPES))
                    problems += 1
                    continue
                if kind == "Paul (chat)":
                    unchecked.setdefault("Paul's own message", set()).add(iid)
                    item_unchecked = True
                    continue
                if ref not in refs:
                    R.add("FAIL", g, "item %s cites document %r which was never recorded as read: record it with run.py source (client-file kinds %s)" % (iid, ref, w.SOURCE_KINDS))
                    problems += 1
                elif refs[ref] != kind:
                    R.add("FAIL", g, "item %s calls document %r a %s but it was recorded as a %s" % (iid, ref, kind, refs[ref]))
                    problems += 1
                else:
                    txt = doc_text(run, ref)
                    if txt is None:
                        unchecked.setdefault(ref, set()).add(iid)
                        item_unchecked = True
                    elif w.norm(S(s.get("quote"))) not in w.norm(txt):
                        R.add("FAIL", g, "item %s: quote not found in document %s" % (iid, ref))
                        problems += 1
                    else:
                        evidence.append(txt)
            else:
                R.add("FAIL", g, "item %s: a source needs either line+quote or doc+ref+quote" % iid)
                problems += 1
        status = (S(it.get("status")) or S(it.get("tag"))).strip().lower()
        if status and not any(status.startswith(sw) for sw in w.STATUS_WORDS + w.TAG_WORDS):
            R.add("WARN", g, "item %s: status/tag %r is not one of the skill's status words" % (iid, it.get("status") or it.get("tag")))

        # every figure in the text must be in the sources the item cites
        if not item_unchecked:
            have = set()
            for e in evidence:
                have |= num_forms(e)
            lost = sorted(t for t in figures(it["text"]) if t not in have)
            if lost:
                R.add("FAIL", g, "item %s states figures %s that appear in none of its sources: cite the transcript or the document that shows them" % (iid, lost))
                problems += 1

        if lst == "actions":
            if not it["text"].startswith("Sitamah to "):
                R.add("FAIL", g, "action %s must start 'Sitamah to ' (all actions go to Sitamah): %r" % (iid, it["text"][:60]))
                problems += 1
            if OWNER_BAD.search(it["text"]):
                R.add("FAIL", g, "action %s names Paul/'I'll' as the owner: Paul is never the owner of an action" % iid)
                problems += 1
            window = " ".join(window_norm(lines, s["line"]) for s in srcs if isinstance(s.get("line"), int) and 1 <= s["line"] <= len(lines))
            if CHASE.search(it["text"]) and any(p in window for p in LEFT_WITH_CLIENT):
                R.add("FAIL", g, "action %s is a chase action next to words where the client left it with himself ('leave it / get back to us'): that is not a chase action" % iid)
                problems += 1
            if DEPENDS.search(it["text"]) and "in force" not in it["text"].lower():
                R.add("WARN", g, "action %s is worded as dependent on something (%r): the transcript or Paul must have said so; independent actions are parallel bullets" % (iid, DEPENDS.search(it["text"]).group(0)))

    if not (content.get("actions") or []):
        R.add("WARN", g, "no actions at all: check Step 1b item 2 (requests/instructions) was applied")

    bad_chars, ids13, ids10 = set(), [], []
    for s in all_strings(content):
        for ch in s:
            try:
                ch.encode("cp1252")
            except UnicodeEncodeError:
                bad_chars.add(ch)
        ids13 += ID13.findall(s)
        ids10 += ID10.findall(s)
    if bad_chars:
        R.add("FAIL", g, "characters outside WinAnsi would break the PDF: %s" % sorted(bad_chars))
        problems += 1
    if ids13:
        R.add("FAIL", g, "a 13-digit number (ID number?) appears in the outputs: never write ID, account or tax numbers")
        problems += 1
    if ids10:
        R.add("WARN", g, "a 10-digit number appears (tax/phone/account number?): confirm it is allowed")
    for ref, ids in sorted(unchecked.items()):
        R.add("WARN", g, "document source '%s' (items %s) cannot be machine-checked: no text copy was recorded (run.py source --text-file ...). Paul should glance at those items" % (ref, sorted(ids)))
    if not problems:
        R.add("PASS", g, "%d items, %d sources: every quote found, every figure traced to a source, every action starts 'Sitamah to', no ID numbers, PDF-safe characters" % (len(idx), n_src))


# ---------------------------------------------------------------- D mandatory checks
CESSION = re.compile(r"\bced(?:e|ed|ing)\b|\bcession\b", re.I)
OWNER_WORDS = re.compile(r"\b(owner|life assured|policyholder|contracting party|payer)\b", re.I)


def check_declared(run, content, idx, ledger, R):
    g = "D"
    ck = content.get("checks")
    mt = content.get("meeting_type")
    if not isinstance(ck, dict):
        R.add("FAIL", g, "content.json has no `checks` block: every conditional rule of the skill must be answered, never skipped")
        return
    probs = 0

    def fail(msg):
        nonlocal probs
        probs += 1
        R.add("FAIL", g, msg)

    def action_text(aid):
        e = idx.get(aid) if isinstance(aid, str) else None
        return S(e[1].get("text")) if e and e[0] == "actions" else None

    items = [it for _, it in w.all_items(content)]
    changed = [it for it in items if "changed" in (S(it.get("status")) + S(it.get("tag"))).lower()]

    c = ck.get("correspondence")
    if not isinstance(c, dict) or "done" not in c:
        fail("checks.correspondence missing (Step 1c): {done:true, looked_at:'...'} or {done:false, reason:'...'}")
    elif c["done"] and len(S(c.get("looked_at")).strip()) < 8:
        fail("checks.correspondence.looked_at must say what was checked in Outlook")
    elif not c["done"] and (mt != "first" or len(S(c.get("reason")).strip()) < 8):
        fail("correspondence was not checked: only allowed at a first meeting, with a reason")

    o = ck.get("owner_change")
    if not isinstance(o, dict) or "occurred" not in o:
        fail("checks.owner_change missing (Step 4b): {occurred:false} or {occurred:true, action_id:'a..'}")
    elif o["occurred"]:
        t = action_text(o.get("action_id"))
        if not t or not re.search(r"revised\b.*\bquote", t, re.I):
            fail("owner_change occurred: action_id must name a Sitamah action to request/chase a revised quote")
        if not changed:
            fail("owner_change occurred: an item must carry status CHANGED (old -> new)")
    elif any(OWNER_WORDS.search(S(it.get("text"))) for it in changed):
        fail("owner_change.occurred is false but an item marked CHANGED is about an owner, life assured, payer or policyholder: declare it (Step 4b: a revised quote is needed)")

    s = ck.get("cession")
    if not isinstance(s, dict) or "needed" not in s:
        fail("checks.cession missing (Step 4c): {needed:false} or {needed:true, action_id:'a..'}")
    elif s["needed"]:
        t = action_text(s.get("action_id"))
        if not t or not CESSION.search(t):
            fail("cession needed: action_id must name a Sitamah action to arrange the cession and send the documents")
    elif any(CESSION.search(S(i.get("text"))) and "ceded to" in S(i.get("text")).lower() for i in items if i.get("status") != "resolved"):
        R.add("WARN", g, "an item talks about a debt being ceded but checks.cession.needed is false: confirm no cession action is needed")

    cl = ck.get("credit_life")
    credit_items = [i for i in items if re.search(r"credit life", S(i.get("text")), re.I)]
    if not isinstance(cl, dict) or "debts_protected" not in cl:
        fail("checks.credit_life missing (Step 4d, ALWAYS): {debts_protected:false, reason:'...'} or {debts_protected:true, debts:[...], bullet_id, action_ids:[...]}")
    elif cl["debts_protected"]:
        b = idx.get(cl.get("bullet_id")) if isinstance(cl.get("bullet_id"), str) else None
        ids = cl.get("action_ids") if isinstance(cl.get("action_ids"), list) else []
        acts = [action_text(a) for a in ids]
        if not cl.get("debts"):
            fail("credit_life: list each debt {lender, credit_life: yes|no|unconfirmed}")
        if not b or not re.search(r"credit life", S(b[1].get("text")), re.I):
            fail("credit_life: bullet_id must be a report bullet that mentions credit life")
        if not acts or any(a is None for a in acts):
            fail("credit_life: action_ids must name Sitamah actions")
        else:
            joined = " ".join(acts)
            if not (re.search(r"\b(get|obtain|request)\b.*\bdetails?\b", joined, re.I) and re.search(r"\bask\b", joined, re.I) and re.search(r"in force", joined, re.I)):
                fail("credit_life: the actions must (a) get the credit-life details from the client, (b) ask the client what he wants to do, and (c) cancel ONLY once the new policy is accepted and in force")
    elif len(S(cl.get("reason")).strip()) < 10:
        fail("credit_life.debts_protected is false: give the reason (which cover, why no debt is protected)")
    elif credit_items:
        fail("checks.credit_life.debts_protected is false but item %s mentions credit life: declare it and add the three actions" % credit_items[0].get("id"))

    ap = ck.get("applications")
    if not isinstance(ap, dict) or "exist" not in ap:
        fail("checks.applications missing (Step 2b/6): {exist:false} or {exist:true, ...}")
    elif ap["exist"]:
        if mt == "first":
            R.add("WARN", g, "applications declared at a first meeting: unusual, confirm")
        if not content.get("applications") and len(S(ap.get("reason")).strip()) < 10:
            fail("applications exist but none are reported: add them, or give the reason (e.g. 'all match the call')")
    else:
        srcs = load(os.path.join(run, w.SOURCES), [])
        if any(isinstance(e, dict) and e.get("kind") == "Application" and e.get("read") == "yes" for e in srcs):
            fail("applications were read (sources.json) but checks.applications.exist is false")

    q = ck.get("quotes_matched")
    if q is not True and not (isinstance(q, str) and q.lower().startswith("n/a") and len(q) > 8):
        fail("checks.quotes_matched must be true (Step 4: matched against the quote register) or 'n/a: <reason>'")
    if not probs:
        R.add("PASS", g, "every conditional rule answered (correspondence, owner change, cession, credit life, applications, quotes), cross-checked against the text, and its consequences present")


# ---------------------------------------------------------------- E outputs
TEAMS_RE = re.compile(
    r"^(?P<name>.+) \((?P<label>Review Client|Prospect)\) \u2013 (?P<kind>\d+(?:st|nd|rd|th) Teams Appointment) Completed: (?P<date>\d{2}/\d{2}/\d{4}) "
    r"– Please see instructions in Client / Prospect Task\.(?P<fu> Please take note of Follow Up Appt\.)?$")
TAG = re.compile(r"<[^>]+>")


def visible_text(page_html):
    body = page_html.split("<article", 1)[-1].split("</article>", 1)[0]
    return html.unescape(TAG.sub(" ", body))


def pdf_pages(path):
    r = subprocess.run(["pdftotext", path, "-"], capture_output=True, text=True)
    if r.returncode:
        return None
    pages = r.stdout.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    return pages


def check_outputs(run, st, content, R):
    import page
    g = "E"
    b = st.get("build")
    if not b:
        R.add("FAIL", g, "outputs not built yet (run build.py)")
        return
    if b["content_sha"] != w.content_hash(content):
        R.add("FAIL", g, "content.json changed after the outputs were built: every correction re-opens the whole task, rebuild every output (build.py)")
        return
    names = w.output_names(content)
    out = os.path.join(run, w.OUT)
    mt = content["meeting_type"]
    model = page.note_model(content, names)
    expected = {names["page"]: page.render_page(model, content), names["note_txt"]: page.render_text(model, markdown=True)}
    msg = page.teams_message(content)
    if msg:
        expected[names["teams"]] = msg + "\n"
    elif os.path.exists(os.path.join(out, names["teams"])):
        R.add("FAIL", g, "a WhatsApp call must not produce the Teams appointment message")

    for fname, want in expected.items():
        p = os.path.join(out, fname)
        if not os.path.exists(p):
            R.add("FAIL", g, "%s is missing from out/" % fname)
        elif open(p, encoding="utf-8").read() != want:
            R.add("FAIL", g, "%s is not what content.json produces (edited by hand or replaced): rebuild it with build.py" % fname)
    page_html, note_txt = expected[names["page"]], expected[names["note_txt"]]
    if all(os.path.exists(os.path.join(out, f)) for f in (names["page"], names["note_txt"])) and \
            not any(r[0] == "FAIL" and "planner_note" in r[2] for r in R.rows):
        in_note = ("applications", "actions", "next_appointment")
        note_items = [it for lst, it in w.all_items(content) if lst in in_note or lst.startswith("areas:")]
        miss = [it["id"] for it in note_items if w.norm(it["text"]) not in w.norm(visible_text(page_html))]
        if 'id="copy-note"' not in page_html:
            R.add("FAIL", g, "Planner page has no Copy note button")
        elif miss or "```" in note_txt:
            R.add("FAIL", g, "Planner page/text is missing items %s or contains a code fence" % miss)
        else:
            R.add("PASS", g, "Planner page (with Copy note button) and fallback text are exactly what content.json produces; every item present, no code fence")
    if msg:
        m = TEAMS_RE.match(msg.strip())
        c = content["client"]
        if not m:
            R.add("FAIL", g, "Teams message is not in the fixed Step 8 wording: %r" % msg.strip())
        elif m["name"] != "%s %s" % (c["first"], c["surname"]) or m["date"] != content["meeting_date"] or m["label"] != content.get("client_status"):
            R.add("FAIL", g, "Teams message has the wrong client name, label or date")
        elif os.path.exists(os.path.join(out, names["teams"])):
            R.add("PASS", g, "Teams message to Sitamah is exactly the fixed wording (%s%s)" % (m["kind"], ", with follow-up sentence" if m["fu"] else ", no follow-up sentence"))

    if mt == "first":
        stray = [f for f in os.listdir(out) if f.lower().endswith(".pdf")] if os.path.isdir(out) else []
        if stray:
            R.add("FAIL", g, "a first/Fact Find meeting must not produce a Follow-Up PDF (the Fact Find Summary is that meeting's PDF): %s" % stray)
        else:
            R.add("PASS", g, "no PDF for a first/Fact Find meeting (correct)")
        return

    pdf = os.path.join(out, names["pdf"])
    if not os.path.exists(pdf):
        R.add("FAIL", g, "PDF missing: expected '%s'" % names["pdf"])
        return
    others = [f for f in os.listdir(out) if f.lower().endswith(".pdf") and f != names["pdf"]]
    if others:
        R.add("FAIL", g, "unexpected extra PDF(s) in out/: %s" % others)
    pages = pdf_pages(pdf)
    if not pages:
        R.add("FAIL", g, "the PDF has no extractable text (is it really a PDF?)")
        return
    # rebuild it from content.json and compare the text: a swapped or hand-made PDF cannot pass
    import build
    with tempfile.TemporaryDirectory(prefix="wrverify-") as tmp:
        ref_pdf = os.path.join(tmp, "ref.pdf")
        headings = build.build_pdf(content, names, ref_pdf)
        ref_pages = pdf_pages(ref_pdf) or []
    if w.norm(" ".join(pages)) != w.norm(" ".join(ref_pages)):
        R.add("FAIL", g, "the PDF text is not what content.json produces (edited, replaced or made by hand): rebuild it with build.py")
        return
    hn = {w.norm(h) for h in headings}
    for i, pg in enumerate(pages[:-1], 1):
        ls = [x.strip() for x in pg.split("\n") if x.strip()]
        if ls and w.norm(ls[-1]) in hn:
            R.add("FAIL", g, "heading '%s' is stranded at the bottom of page %d" % (ls[-1], i))
    if len(pages) > 2:
        R.add("WARN", g, "the PDF is %d pages: the skill aims at two at most" % len(pages))
    R.add("PASS", g, "PDF '%s': %d page(s), text identical to what content.json produces, every heading and item present" % (names["pdf"], len(pages)))
    pngs = sorted(f for f in os.listdir(out) if f.startswith("page") and f.endswith(".png"))
    if len(pngs) != len(pages) or any(os.path.getsize(os.path.join(out, f)) < 3000 for f in pngs):
        R.add("FAIL", g, "page images for the visual check are missing (%d images for %d pages)" % (len(pngs), len(pages)))
    else:
        R.add("PASS", g, "page images rendered for the visual check: %s" % pngs)


# ---------------------------------------------------------------- F receipt and driver
def applicable_steps(mt):
    steps = load(os.path.join(SKILL_DIR, "steps.json"), {}).get("steps", [])
    return [s["id"] for s in steps if mt in s.get("applies", [])]


def money_in_items(content):
    return any(figures(S(it.get("text"))) for _, it in w.all_items(content) if re.search(r"R\s?\d", S(it.get("text"))))


def check_receipt(run, st, content, ledger, R, skip=()):
    import page
    g = "F"
    p = os.path.join(run, w.RECEIPT)
    mt = content["meeting_type"]
    names = w.output_names(content)
    rc = load(p, None) if os.path.exists(p) else None
    if not isinstance(rc, dict):
        R.add("FAIL", g, "receipt.json missing or unreadable: record the hand-over evidence before declaring the run complete (run.py receipt)")
        return
    probs = 0

    def fail(m):
        nonlocal probs
        probs += 1
        R.add("FAIL", g, m)

    def text(d, *keys, n=1):
        return isinstance(d, dict) and all(len(str(d.get(k) or "").strip()) >= n for k in keys)

    # a rebuilt output re-opens its hand-over: receipts must belong to the current build
    cur = (st.get("build") or {}).get("content_sha")
    stamps = rc.get("_stamps") if isinstance(rc.get("_stamps"), dict) else {}
    stale = [k for k in HANDOVER_KEYS if k in rc and stamps.get(k) != cur]
    if stale:
        fail("hand-over receipts recorded for an older build (the outputs were rebuilt after content.json changed): redo and re-record %s" % stale)

    pp = rc.get("planner_page")
    pp = pp if isinstance(pp, dict) else {}
    if pp.get("mode") == "artifact":
        if not str(pp.get("url") or "").startswith("https://claude.ai/"):
            fail("planner_page.url must be the link returned by the page (Artifact) tool, starting https://claude.ai/")
        else:
            R.add("ATTEST", g, "Planner note published as a page with a Copy button: %s" % pp["url"])
    elif pp.get("mode") == "fallback_text":
        if not text(pp, "reason", n=10):
            fail("planner_page.reason: say why the page tool was unavailable (the fallback must be stated)")
        else:
            R.add("ATTEST", g, "Planner note shown as formatted chat text (FALLBACK, page tool unavailable: %s)" % str(pp["reason"])[:60])
    else:
        fail("planner_page.mode must be 'artifact' or 'fallback_text'")

    if mt != "first":
        if not truthy(rc.get("pdf_sent_in_chat")):
            fail("the PDF must be sent in the chat for download (pdf_sent_in_chat)")
        else:
            R.add("ATTEST", g, "PDF sent in the chat")
        sv = rc.get("saved") if isinstance(rc.get("saved"), dict) else {}
        if not text(sv, "tool", "folder", "filename", "tool_result", "folder_listing_check"):
            fail("saved{tool, folder, filename, tool_result, folder_listing_check} must all be filled from the real tool output")
        else:
            before = probs
            if sv["filename"] != names["pdf"]:
                fail("saved.filename %r is not the expected %r" % (sv["filename"], names["pdf"]))
            if names["pdf"] not in str(sv["folder_listing_check"]):
                fail("saved.folder_listing_check does not show the file in the folder listing")
            if "2. Fact Find" not in str(sv["folder"]):
                fail("saved.folder is not the client's '2. Fact Find' folder")
            if probs == before:
                R.add("ATTEST", g, "PDF saved to the client's 2. Fact Find folder via %s and the folder listing checked" % sv["tool"])
        if len(str(rc.get("png_visual_check") or "").strip()) < 20:
            fail("png_visual_check: say what you saw on each page image (layout, headings, bullets)")
        else:
            R.add("ATTEST", g, "page images looked at")
        if not str(rc.get("applications_handoff") or "").strip():
            fail("applications_handoff: 'complete-applications-skill called' or 'n/a: <reason>'")
        else:
            R.add("ATTEST", g, "applications hand-off: " + str(rc["applications_handoff"])[:80])

    # the checks only Claude can do, each recorded in its own words
    ents = (ledger or {}).get("entries") or []
    needs_recheck = (any(isinstance(e, dict) and e.get("kind") in ("acceptance", "change") for e in ents)
                     or bool(((content.get("checks") or {}).get("owner_change") or {}).get("occurred")) or money_in_items(content))
    ic = str(rc.get("independent_check") or "").strip()
    if len(ic) < 10:
        fail("independent_check: 'subagent: <what it re-checked and found>' (or 'n/a: the Agent tool is not available')")
    elif ic.lower().startswith("n/a") and needs_recheck and "not available" not in ic.lower():
        fail("independent_check: this meeting has an acceptance, a change or money amounts, so a second reader (a subagent) must re-check the key facts against the transcript")
    else:
        R.add("ATTEST", g, "independent re-check: " + ic[:90])
    jd = rc.get("judgment") if isinstance(rc.get("judgment"), dict) else {}
    if not text(jd, *JUDGMENT_KEYS, n=12):
        fail("judgment: one sentence each (at least 12 characters) for %s" % list(JUDGMENT_KEYS))
    else:
        R.add("ATTEST", g, "judgment items answered: " + "; ".join("%s: %s" % (k, str(jd[k])[:50]) for k in JUDGMENT_KEYS))
    if ((content.get("checks") or {}).get("owner_change") or {}).get("occurred"):
        if len(str(rc.get("revised_quote_draft") or "").strip()) < 10:
            fail("revised_quote_draft: the revised-quote email draft must be shown to Paul (never sent without his yes): say what was shown")
        else:
            R.add("ATTEST", g, "revised-quote draft shown to Paul: " + str(rc["revised_quote_draft"])[:70])

    # Teams message to Sitamah (Step 8): last thing, only with Paul's yes, never twice
    if "teams" not in skip:
        tm = rc.get("teams") if isinstance(rc.get("teams"), dict) else {}
        status = tm.get("status")
        if mt == "whatsapp":
            R.add("ATTEST", g, "Teams message not applicable to a WhatsApp call")
        elif status == "sent":
            msg = page.teams_message(content)
            body = w.norm(html.unescape(TAG.sub(" ", str(tm.get("body_as_stored") or ""))))
            if not text(tm, "message_id", "sent_time", "approved_by_paul", n=3) or len(body) < 20:
                fail("teams: status=sent needs message_id, sent_time and body_as_stored from Zapier, and approved_by_paul (Paul's own words)")
            elif w.norm(msg) not in body:
                fail("teams.body_as_stored is not the message that was meant to be sent: what Zapier stored does not match")
            else:
                R.add("ATTEST", g, "Teams message sent to Sitamah via Zapier after Paul's yes (message id %s, %s). Paul's words: \"%s\"" % (tm["message_id"], tm["sent_time"], str(tm["approved_by_paul"])[:60]))
        elif status == "already_sent":
            if not text(tm, "already_sent_evidence", n=10):
                fail("teams: status=already_sent needs already_sent_evidence (which skill sent it, when, message id): it is once per meeting")
            else:
                R.add("ATTEST", g, "Teams message was already sent for this meeting: " + str(tm["already_sent_evidence"])[:80])
        elif status == "declined":
            if not text(tm, "paul_said", n=2):
                fail("teams: status=declined needs paul_said (his words)")
            else:
                R.add("ATTEST", g, "Paul declined the Teams message. His words: \"%s\"" % str(tm["paul_said"])[:60])
        elif status == "failed":
            if not text(tm, "detail", n=8) or not truthy(tm.get("text_given_to_paul")):
                fail("teams: status=failed needs detail (the error) and text_given_to_paul=true")
            else:
                R.add("ATTEST", g, "Teams send failed; message text given to Paul to paste (not claimed as sent)")
        else:
            fail("teams.status must be sent, already_sent, declined or failed: the Teams message to Sitamah is the last step of every Teams meeting")


def check_driver(run, mt, R, skip=()):
    g = "F"
    rj = load(os.path.join(run, w.RUN), None)
    if not isinstance(rj, dict) or not isinstance(rj.get("steps"), dict):
        R.add("FAIL", g, "run.json missing: this run was not driven by run.py (start it with run.py start)")
        return
    pending = [s for s in applicable_steps(mt) if s != "final" and not (s == "teams" and "teams" in skip)
               and (rj["steps"].get(s) or {}).get("state") != "done"]
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
    lp, cp = os.path.join(run, w.LEDGER), os.path.join(run, w.CONTENT)
    ledger = load(lp, None)
    content = load(cp, None)
    mt = meeting_type_of(run, content)
    shape = validate_shape(content) if content is not None else []
    refs = guarded(R, "S", "client file and access", check_sources, run, mt, R, lines, content if not shape else None)
    if ledger is None or not isinstance(ledger, dict):
        R.add("FAIL", "B", "ledger.json missing (record the decision ledger as you read: run.py ledger add)")
    if content is None:
        R.add("FAIL", "C", "content.json missing")
    elif shape:
        for e in shape:
            R.add("FAIL", "C", "content.json shape: " + e)
    if isinstance(ledger, dict) and content is not None and not shape:
        idx, dup = item_index(content)
        guarded(R, "B", "ledger", check_ledger, run, st, lines, ledger, idx, R)
        guarded(R, "C", "source trace", check_content, run, st, lines, content, idx, dup, refs, R)
        guarded(R, "D", "mandatory checks", check_declared, run, content, idx, ledger, R)
        if stage in ("built", "final") and not R.fails:
            guarded(R, "E", "outputs", check_outputs, run, st, content, R)
        elif stage in ("built", "final"):
            R.add("FAIL", "E", "outputs not checked: fix the failures above first")
        if stage == "final" and not R.fails:
            guarded(R, "F", "hand-over", check_receipt, run, st, content, ledger, R, skip)
            guarded(R, "F", "driver", check_driver, run, content["meeting_type"], R, skip)
        elif stage == "final":
            R.add("FAIL", "F", "hand-over not checked: fix the failures above first")
    return R, st, ledger, content


def summary_lines(run, st, ledger, content):
    """What Paul should glance at: the places where the program could only count, not judge."""
    out = []
    srcs = load(os.path.join(run, w.SOURCES), [])
    none = [e["kind"] for e in srcs if isinstance(e, dict) and "none" in e]
    read = [e for e in srcs if isinstance(e, dict) and e.get("read") == "yes"]
    acc = load(os.path.join(run, w.ACCESS), [])
    routes = sorted({e.get("route") for e in acc if isinstance(e, dict)})
    ents = (ledger or {}).get("entries") or []
    p1 = sum(1 for e in ents if e.get("pass") == 1)
    excl = [e for e in ents if e.get("excluded")]
    sc = st.get("scan") or {}
    rev = len(reviewed_lines(ledger or {}))
    out.append("Source: %s, sha256 %s..., times %s to %s, stated duration %s" % (
        st.get("source"), st.get("sha256", "")[:10], st.get("first_ts"), st.get("last_ts"), st.get("stated_duration") or "not stated"))
    out.append("Client file: %d documents read; no document on file for: %s; access routes used: %s" % (len(read), ", ".join(none) or "nothing missing", ", ".join(routes)))
    out.append("Ledger: %d entries (%d from Pass 1, %d added in Pass 2); %d plain facts/figures left out of the report on purpose; %d keyword-scan lines dismissed with a reason"
               % (len(ents), p1, len(ents) - p1, len(excl), rev))
    for e in excl:
        out.append("   left out: line %s %r because %s" % (e.get("line"), str(e.get("quote"))[:50], str(e.get("excluded"))[:80]))
    return out


def report(R, st, ledger, content, stage, run=None):
    print("DELIVERY GATE  (stage: %s)" % stage)
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
        n_src = sum(len(it.get("src") or []) for _, it in w.all_items(content))
        print("\nWHAT PAUL SHOULD GLANCE AT (the program counted these; it cannot judge them):")
        for ln in summary_lines(run or ".", st, ledger, content):
            print("  " + ln)
        print("\nDELIVERY LINE (copy into the reply, unedited):")
        print("Transcript read in full TWICE (Pass 1 and Pass 2, %d lines each, %d chunks, every chunk acknowledged in the ledger); %d ledger entries; "
              "every bullet and action source-traced (%d sources: every quote found in the transcript or a recorded document, every figure traced)."
              % (st["total_lines"], k, len(ledger["entries"]), n_src))
        print("Attested by Claude, not machine-proven: chat hand-over, saving to the client's folder, the Zapier send, the visual check of the page images, the independent re-check and the judgment items.")
    elif fails:
        print("\nNOT COMPLETE. You may not tell Paul this run is finished. Fix every FAIL above and re-run.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    ap.add_argument("--stage", choices=["pre", "built", "final"], default="final")
    ap.add_argument("--skip-teams", action="store_true", help="check everything except the Teams receipt (used before the message is shown)")
    a = ap.parse_args()
    R, st, ledger, content = run_checks(a.run, a.stage, ("teams",) if a.skip_teams else ())
    report(R, st, ledger, content, a.stage, a.run)
    sys.exit(1 if R.fails else 0)


if __name__ == "__main__":
    main()
