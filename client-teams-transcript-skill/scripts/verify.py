#!/usr/bin/env python3
"""Delivery gate for the client-teams-transcript skill.

  verify.py <run_dir> [--stage pre|built|final]

Stages (each includes the one before):
  pre    A reading lock, S client file and access, B ledger and coverage, C source trace, D mandatory checks
  built  + E the outputs on disk match content.json and each other
  final  + F the hand-over receipt (default)

Prints PASS / FAIL / WARN per item and a RESULT line. Exit code 0 only on PASS.
ATTEST rows are things only Claude can do (chat hand-over, saving through the
device bridge); they are recorded, not machine-proven, and are labelled that way.
"""
import argparse
import html
import os
import re
import subprocess
import sys

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
    "F": "F. Hand-over (attested by Claude, not machine-proven)",
}
QUOTE_WINDOW = 2  # a quote may sit on the cited line or within 2 lines of it (wrapped speech)


class Results:
    def __init__(self):
        self.rows = []

    def add(self, level, group, msg):
        self.rows.append((level, group, msg))

    @property
    def fails(self):
        return [r for r in self.rows if r[0] == "FAIL"]


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
        R.add("PASS", g, "keyword scan run (%d hits)" % len(st["scan"]["hits"]))
    else:
        R.add("FAIL", g, "keyword scan not run (`tx.py scan`)")
    if st["forced"]:
        R.add("WARN", g, "reading was FORCED past a completeness warning; Paul must have approved this")


# ---------------------------------------------------------------- S client file and access
ALLOWED_ROUTES = w.ROUTES + ("user", "passed")


def meeting_type_of(run, content):
    if content and content.get("meeting_type") in MEETING_TYPES:
        return content["meeting_type"]
    p = os.path.join(run, w.RUN)
    if os.path.exists(p):
        return w.load_json(p).get("meeting_type")
    return None


def check_sources(run, mt, R):
    g = "S"
    sp, ap, qp = (os.path.join(run, n) for n in (w.SOURCES, w.ACCESS, w.QUESTIONS))
    sources = w.load_json(sp) if os.path.exists(sp) else []
    access = w.load_json(ap) if os.path.exists(ap) else []
    questions = w.load_json(qp) if os.path.exists(qp) else []
    probs = 0

    def fail(m):
        nonlocal probs
        probs += 1
        R.add("FAIL", g, m)

    # sources: every kind the skill must read is either read or explained
    need_kinds = w.REQUIRED_SOURCE_KINDS.get(mt, w.SOURCE_KINDS)
    for e in sources:
        if e.get("kind") not in w.SOURCE_KINDS:
            fail("source with unknown kind %r (allowed: %s)" % (e.get("kind"), w.SOURCE_KINDS))
        elif "none" in e:
            if len((e.get("none") or "").strip()) < 8:
                fail("source kind %s: 'none' needs a reason (what was searched and not found)" % e["kind"])
        elif e.get("read") == "yes":
            if not (e.get("path") or "").strip() or not (e.get("date") or "").strip():
                fail("source %s: a document that was read needs its path and date" % e.get("kind"))
        else:
            fail("source %s: record read=yes with path and date, or a 'none' reason" % e.get("kind"))
    have = {e.get("kind") for e in sources if e.get("read") == "yes" or len((e.get("none") or "").strip()) >= 8}
    missing = [k for k in need_kinds if k not in have]
    if missing:
        fail("client-file sources not accounted for: %s (read them from the client's file, or record why none exist; Paul is asked last)" % missing)

    # access: the transcript must have been obtained; a need that never succeeded must have all three routes tried
    by_need = {}
    for e in access:
        if e.get("route") not in ALLOWED_ROUTES or e.get("result") not in ("ok", "fail") or not (e.get("need") or "").strip():
            fail("access_log entry malformed (need, route in %s, result ok|fail): %s" % (ALLOWED_ROUTES, e))
            continue
        by_need.setdefault(e["need"], []).append(e)
    if "transcript" not in by_need or not any(e["result"] == "ok" for e in by_need["transcript"]):
        fail("the transcript has no successful access entry (run.py access --need transcript ... --result ok)")
    asked = {q.get("need") for q in questions}
    for need, es in by_need.items():
        if any(e["result"] == "ok" for e in es):
            continue
        tried_fail = {e["route"] for e in es if e["result"] == "fail"}
        untried = [r for r in w.ROUTES if r not in tried_fail]
        if untried:
            fail("'%s' could not be fetched but these routes were never tried: %s. Never say 'I cannot access your files' until all three failed" % (need, untried))
        elif need not in asked:
            fail("'%s' failed on all three routes but nothing was recorded for Paul: use run.py ask with the errors" % need)
    for q in questions:
        if len((q.get("question") or "").strip()) < 8 or len((q.get("searched") or "").strip()) < 8:
            fail("a question to Paul needs the question and what was searched first: %s" % q)
        if q.get("need") in by_need and any(e["result"] == "ok" for e in by_need[q["need"]]):
            R.add("WARN", g, "question about '%s' was recorded although that need was later fetched: do not ask Paul" % q["need"])
    if not probs:
        R.add("PASS", g, "client-file sources accounted for (%d read, kinds required: %s); access log has %d entries across %d need(s); %d question(s) to Paul, each with what was searched"
              % (sum(1 for e in sources if e.get("read") == "yes"), len(need_kinds), len(access), len(by_need), len(questions)))


# ---------------------------------------------------------------- helpers for B/C/D
def item_index(content):
    idx, dup = {}, []
    for lst, it in w.all_items(content):
        iid = it.get("id") if isinstance(it, dict) else None
        if not iid:
            continue
        if iid in idx:
            dup.append(iid)
        idx[iid] = (lst, it)
    return idx, dup


def window_norm(lines, line):
    lo, hi = max(0, line - 1 - QUOTE_WINDOW), min(len(lines), line + QUOTE_WINDOW)
    return w.norm(" ".join(lines[lo:hi]))


def quote_ok(lines, line, quote):
    q = w.norm(quote)
    return len(q) >= 4 and q in window_norm(lines, line)


# ---------------------------------------------------------------- B ledger and coverage
def check_ledger(run, st, lines, ledger, idx, R):
    g = "B"
    ents = ledger.get("entries") if isinstance(ledger, dict) else None
    if not ents:
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
        if not quote_ok(lines, ln, e.get("quote") or ""):
            R.add("FAIL", g, "%s: quote not found at line %d: %r" % (where, ln, e.get("quote")))
            bad += 1
            continue
        cov = e.get("covered_by") or []
        unknown = [c for c in cov if c not in idx]
        if unknown:
            R.add("FAIL", g, "%s: covered_by names items that do not exist in content.json: %s" % (where, unknown))
            bad += 1
            continue
        if not cov:
            if kind in KINDS_MUST_COVER:
                R.add("FAIL", g, "%s (%s, line %d) is not covered by any bullet or action: %r"
                      % (where, kind, ln, e.get("quote")))
                bad += 1
            elif len((e.get("excluded") or "").strip()) < 8:
                R.add("FAIL", g, "%s (%s) is neither covered nor excluded with a reason" % (where, kind))
                bad += 1
            continue
        lists = [idx[c][0] for c in cov]
        items = [idx[c][1] for c in cov]
        if kind == "change" and not any("changed" in (i.get("status", "") + i.get("tag", "")).lower() for i in items):
            R.add("FAIL", g, "%s (change, line %d) is not recorded as CHANGED (before -> after) in any covering item" % (where, ln))
            bad += 1
        if kind in ("request", "instruction", "offer") and not any(
                lst == "actions" or it.get("status") or it.get("tag") for lst, it in zip(lists, items)):
            R.add("FAIL", g, "%s (%s, line %d) must map to a Sitamah action or a status line" % (where, kind, ln))
            bad += 1
        if kind == "hold" and all(lst == "actions" for lst in lists):
            R.add("FAIL", g, "%s (hold, line %d) is covered only by an action: items on hold/left with the client are reported as on hold, not as tasks" % (where, ln))
            bad += 1
    if not bad:
        must = sum(1 for e in ents if e.get("kind") in KINDS_MUST_COVER)
        R.add("PASS", g, "%d ledger entries, every quote found verbatim; all %d decision/request/change entries covered" % (len(ents), must))
    # closing minutes
    cz = (st["scan"] or {}).get("closing_from")
    if cz and not any(e.get("line", 0) >= cz for e in ents):
        R.add("WARN", g, "no ledger entry from the closing minutes (lines %d+): the skill warns requests there are the easiest to miss" % cz)

    # keyword scan resolution
    if st["scan"]:
        near = sorted(e["line"] for e in ents if isinstance(e.get("line"), int))
        reviewed = {r.get("line") for r in (ledger.get("scan_reviewed") or []) if len((r.get("reason") or "").strip()) >= 6}
        unresolved, closing_unres = [], []
        for h in st["scan"]["hits"]:
            if h in reviewed or any(abs(h - n) <= 3 for n in near):
                continue
            (closing_unres if h >= st["scan"]["closing_from"] else unresolved).append(h)
        if closing_unres:
            R.add("FAIL", g, "keyword-scan hits in the closing minutes not covered by a ledger entry or scan_reviewed: lines %s" % closing_unres)
        if unresolved:
            R.add("WARN", g, "%d earlier keyword-scan hits have no nearby ledger entry (lines %s%s): add entries or list them in scan_reviewed"
                  % (len(unresolved), unresolved[:12], "..." if len(unresolved) > 12 else ""))
        low_unres = [h for h in st["scan"].get("low_hits", []) if h >= st["scan"]["closing_from"]
                     and h not in reviewed and not any(abs(h - n) <= 3 for n in near)]
        if low_unres:
            R.add("WARN", g, "%d closing-minute lines mention figures/days/products with no nearby ledger entry (lines %s): check them" % (len(low_unres), low_unres[:12]))
        if not closing_unres and not unresolved:
            R.add("PASS", g, "every decision/change/request keyword-scan hit is covered or reviewed")


# ---------------------------------------------------------------- C source trace
OWNER_BAD = re.compile(r"\bPaul\s+(to|will|should|must|can)\b|\bI'?ll\b|\bI will\b")
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


def check_content(run, st, lines, content, idx, dup, R):
    g = "C"
    mt = content.get("meeting_type")
    if mt not in MEETING_TYPES:
        R.add("FAIL", g, "meeting_type must be one of %s" % (MEETING_TYPES,))
        return
    c = content.get("client") or {}
    if not (c.get("first") and c.get("surname")):
        R.add("FAIL", g, "client.first and client.surname are required (the filename is built from them)")
    if not w.short_date(content.get("meeting_date")):
        R.add("FAIL", g, "meeting_date must be DD/MM/YYYY")
    if mt == "whatsapp" and not re.fullmatch(r"\d{1,2}:\d{2}", content.get("meeting_time") or ""):
        R.add("FAIL", g, "meeting_time (HH:MM) is required for a WhatsApp call")
    if not (content.get("topic") or "").strip():
        R.add("FAIL", g, "topic is required (the italic line under the Planner title)")
    if mt != "first" and not (content.get("opening") or "").strip():
        R.add("FAIL", g, "opening sentence is required for the PDF")
    if dup:
        R.add("FAIL", g, "duplicate item ids: %s" % sorted(set(dup)))
    keys = [a.get("key") for a in content.get("areas") or []]
    if any(k not in w.AREA_KEYS for k in keys) or len(keys) != len(set(keys)):
        R.add("FAIL", g, "areas keys must be unique and from %s (got %s)" % (w.AREA_KEYS, keys))
    if mt == "first" and content.get("since_last"):
        R.add("FAIL", g, "a first/Fact Find meeting has nothing to carry forward: since_last must be empty")
    na = content.get("next_appointment")
    if not isinstance(na, dict):
        R.add("FAIL", g, "next_appointment {id, text, src} is required")
    elif mt != "whatsapp":
        # the Teams message to Sitamah depends on these (ff-population-transcript Step 8)
        n = content.get("appointment_number")
        if not (n == "review" or (isinstance(n, int) and not isinstance(n, bool) and n >= 1)):
            R.add("FAIL", g, "appointment_number must be 1, 2, 3... or \"review\" (worked out from the client's file, never guessed)")
        if len((content.get("appointment_number_basis") or "").strip()) < 10:
            R.add("FAIL", g, "appointment_number_basis: say which earlier meetings/files on the client's file give that number")
        if not isinstance(na.get("agreed"), bool):
            R.add("FAIL", g, "next_appointment.agreed must be true (a real agreed/booked follow-up) or false (vague or none)")
        if len((na.get("check") or "").strip()) < 10:
            R.add("FAIL", g, "next_appointment.check: one line on what the Summary and the Planner note say about the next appointment, and so why the follow-up sentence is in or out")

    n_src, problems, unverifiable = 0, 0, set()
    for name in ("since_last", "applications", "actions", "next_steps"):
        if any(not isinstance(x, dict) for x in content.get(name) or []):
            R.add("FAIL", g, "%s must be a list of {id, text, src} objects" % name)
            problems += 1
    for a_ in content.get("areas") or []:
        if not isinstance(a_, dict) or any(not isinstance(x, dict) for x in a_.get("bullets") or []):
            R.add("FAIL", g, "each area must be {key, bullets:[{id, text, src}]}")
            problems += 1
    for lst, it in w.all_items(content):
        iid = it.get("id", "?")
        if not it.get("id") or not (it.get("text") or "").strip():
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
        for s in srcs:
            n_src += 1
            if "line" in s:
                ln = s.get("line")
                if not isinstance(ln, int) or not 1 <= ln <= len(lines) or not quote_ok(lines, ln, s.get("quote") or ""):
                    R.add("FAIL", g, "item %s: source quote not found at transcript line %r: %r" % (iid, ln, s.get("quote")))
                    problems += 1
            elif "doc" in s:
                if s["doc"] not in w.DOC_TYPES or not (s.get("ref") or "").strip() or len(w.norm(s.get("quote") or "")) < 4:
                    R.add("FAIL", g, "item %s: a document source needs doc (one of %s), ref and quote" % (iid, w.DOC_TYPES))
                    problems += 1
                else:
                    p = os.path.join(run, w.DOCS, s["ref"] + ".txt")
                    if os.path.exists(p):
                        with open(p, encoding="utf-8", errors="replace") as f:
                            if w.norm(s["quote"]) not in w.norm(f.read()):
                                R.add("FAIL", g, "item %s: quote not found in document %s" % (iid, s["ref"]))
                                problems += 1
                    else:
                        unverifiable.add(s["ref"])
            else:
                R.add("FAIL", g, "item %s: a source needs either line+quote or doc+ref+quote" % iid)
                problems += 1
        status = (it.get("status") or it.get("tag") or "").strip().lower()
        if status and not any(status.startswith(sw) for sw in w.STATUS_WORDS + w.TAG_WORDS):
            R.add("WARN", g, "item %s: status/tag %r is not one of the skill's status words" % (iid, it.get("status") or it.get("tag")))

        if lst == "actions":
            if not it["text"].startswith("Sitamah to "):
                R.add("FAIL", g, "action %s must start 'Sitamah to ' (all actions go to Sitamah): %r" % (iid, it["text"][:60]))
                problems += 1
            if OWNER_BAD.search(it["text"]):
                R.add("FAIL", g, "action %s names Paul/'I'll' as owner: Paul is never the owner of an action" % iid)
                problems += 1
            quotes = " ".join(w.norm(s.get("quote") or "") for s in srcs)
            if CHASE.search(it["text"]) and any(p in quotes for p in LEFT_WITH_CLIENT):
                R.add("FAIL", g, "action %s is a chase action sourced from 'leave it / get back to us': that is not a chase action" % iid)
                problems += 1
            if DEPENDS.search(it["text"]):
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
    for ref in sorted(unverifiable):
        R.add("WARN", g, "document source '%s' cannot be machine-checked: put its text in %s/%s.txt to enable the quote check" % (ref, w.DOCS, ref))
    if not problems:
        R.add("PASS", g, "%d items, %d sources: every quote found; every action starts 'Sitamah to'; no ID numbers; PDF-safe characters" % (len(idx), n_src))


# ---------------------------------------------------------------- D mandatory checks
def check_declared(content, idx, R):
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
        e = idx.get(aid)
        return e[1]["text"] if e and e[0] == "actions" else None

    # Step 1c correspondence
    c = ck.get("correspondence")
    if not isinstance(c, dict) or "done" not in c:
        fail("checks.correspondence missing (Step 1c): {done:true, looked_at:'...'} or {done:false, reason:'...'}")
    elif c["done"] and len((c.get("looked_at") or "").strip()) < 8:
        fail("checks.correspondence.looked_at must say what was checked in Outlook")
    elif not c["done"] and (mt != "first" or len((c.get("reason") or "").strip()) < 8):
        fail("correspondence was not checked: only allowed at a first meeting, with a reason")

    # Step 4b owner change
    o = ck.get("owner_change")
    if not isinstance(o, dict) or "occurred" not in o:
        fail("checks.owner_change missing (Step 4b): {occurred:false} or {occurred:true, action_id:'a..'}")
    elif o["occurred"]:
        t = action_text(o.get("action_id"))
        if not t or not re.search(r"revised\b.*\bquote", t, re.I):
            fail("owner_change occurred: action_id must name a Sitamah action to request/chase a revised quote")
        if not any("changed" in (it.get("status", "") + it.get("tag", "")).lower() for _, it in w.all_items(content)):
            fail("owner_change occurred: an item must carry status CHANGED (old -> new)")

    # Step 4c cession
    s = ck.get("cession")
    if not isinstance(s, dict) or "needed" not in s:
        fail("checks.cession missing (Step 4c): {needed:false} or {needed:true, action_id:'a..'}")
    elif s["needed"]:
        t = action_text(s.get("action_id"))
        if not t or not re.search(r"ced", t, re.I):
            fail("cession needed: action_id must name a Sitamah action to arrange the cession and send the documents")

    # Step 4d credit life
    cl = ck.get("credit_life")
    if not isinstance(cl, dict) or "debts_protected" not in cl:
        fail("checks.credit_life missing (Step 4d, ALWAYS): {debts_protected:false, reason:'...'} or {debts_protected:true, debts:[...], bullet_id, action_ids:[...]}")
    elif cl["debts_protected"]:
        b = idx.get(cl.get("bullet_id"))
        acts = [action_text(a) for a in cl.get("action_ids") or []]
        if not cl.get("debts"):
            fail("credit_life: list each debt {lender, credit_life: yes|no|unconfirmed}")
        if not b or not re.search(r"credit life", b[1]["text"], re.I):
            fail("credit_life: bullet_id must be a report bullet that mentions credit life")
        if not acts or any(a is None for a in acts):
            fail("credit_life: action_ids must name Sitamah actions (get details, ask client, cancel only once the new policy is in force)")
        elif not any(re.search(r"in force", a, re.I) for a in acts):
            fail("credit_life: one action must state cancellation happens only once the new policy is accepted and in force")
    elif len((cl.get("reason") or "").strip()) < 10:
        fail("credit_life.debts_protected is false: give the reason (which cover, why no debt is protected)")
    elif any(re.search(r"credit life", s_, re.I) for s_ in all_strings(content.get("areas") or [])):
        R.add("WARN", g, "report mentions credit life but checks.credit_life.debts_protected is false")

    # Step 2b/6 applications
    ap = ck.get("applications")
    if not isinstance(ap, dict) or "exist" not in ap:
        fail("checks.applications missing (Step 2b/6): {exist:false} or {exist:true, ...}")
    elif ap["exist"]:
        if mt == "first":
            R.add("WARN", g, "applications declared at a first meeting: unusual, confirm")
        if not content.get("applications") and len((ap.get("reason") or "").strip()) < 10:
            fail("applications exist but none are reported: add them, or give the reason (e.g. 'all match the call')")

    # quotes
    q = ck.get("quotes_matched")
    if q is not True and not (isinstance(q, str) and q.lower().startswith("n/a") and len(q) > 8):
        fail("checks.quotes_matched must be true (Step 4: matched against the quote register) or 'n/a: <reason>'")
    if not probs:
        R.add("PASS", g, "every conditional rule answered (correspondence, owner change, cession, credit life, applications, quotes) and its consequences present")


# ---------------------------------------------------------------- E outputs
def pdf_pages(path):
    r = subprocess.run(["pdftotext", path, "-"], capture_output=True, text=True)
    if r.returncode:
        return None
    pages = r.stdout.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    return pages


TEAMS_RE = re.compile(
    r"^(?P<name>.+) \u2013 (?P<kind>(?:\d+(?:st|nd|rd|th)|Review) Teams Appointment) Completed: (?P<date>\d{2}/\d{2}/\d{4}) "
    r"\u2013 Please see instructions in Client / Prospect Task\.(?P<fu> Please take note of Follow Up Appt\.)?$")
TAG = re.compile(r"<[^>]+>")


def visible_text(page_html):
    body = page_html.split("<article", 1)[-1].split("</article>", 1)[0]
    return html.unescape(TAG.sub(" ", body))


def check_outputs(run, st, content, R):
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

    def read(fname):
        p = os.path.join(out, fname)
        if not os.path.exists(p):
            R.add("FAIL", g, "%s is missing from out/" % fname)
            return None
        text = open(p, encoding="utf-8").read()
        if w.sha256_text(text) != b["files"].get(fname):
            R.add("FAIL", g, "%s was edited by hand or replaced: rebuild it from content.json (build.py)" % fname)
            return None
        return text

    in_note = ("applications", "actions", "next_appointment")
    note_items = [it for lst, it in w.all_items(content) if lst in in_note or lst.startswith("areas:")]
    page_html, note_txt = read(names["page"]), read(names["note_txt"])
    if page_html is not None:
        miss = [it["id"] for it in note_items if w.norm(it["text"]) not in w.norm(visible_text(page_html))]
        if 'id="copy-note"' not in page_html:
            R.add("FAIL", g, "Planner page has no Copy note button")
        elif miss:
            R.add("FAIL", g, "Planner page is missing items: %s" % miss)
        else:
            R.add("PASS", g, "Planner page built from content.json with a Copy note button; every item present")
    if note_txt is not None:
        miss = [it["id"] for it in note_items if w.norm(it["text"]) not in w.norm(note_txt)]
        if "```" in note_txt:
            R.add("FAIL", g, "Planner fallback text contains a code fence: never a code block")
        elif miss:
            R.add("FAIL", g, "Planner fallback text is missing items: %s" % miss)
        else:
            R.add("PASS", g, "Planner fallback text matches the page (used only if the page tool is unavailable)")

    if mt == "whatsapp":
        if os.path.exists(os.path.join(out, names["teams"])):
            R.add("FAIL", g, "a WhatsApp call must not produce the Teams appointment message")
    else:
        msg = read(names["teams"])
        if msg is not None:
            m = TEAMS_RE.match(msg.strip())
            c = content["client"]
            if not m:
                R.add("FAIL", g, "Teams message is not in the fixed Step 8 wording: %r" % msg.strip())
            elif m["name"] != "%s %s" % (c["first"], c["surname"]) or m["date"] != content["meeting_date"]:
                R.add("FAIL", g, "Teams message has the wrong client name or date")
            elif bool(m["fu"]) != (content["next_appointment"].get("agreed") is True):
                R.add("FAIL", g, "Teams message follow-up sentence does not match next_appointment.agreed")
            else:
                R.add("PASS", g, "Teams message to Sitamah built in the fixed wording (%s%s)"
                      % (m["kind"], ", with follow-up sentence" if m["fu"] else ", no follow-up sentence"))

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
    if w.sha256_file(pdf) != b["pdf_sha"]:
        R.add("FAIL", g, "the PDF was replaced after it was built: rebuild from content.json")
    pages = pdf_pages(pdf)
    if not pages:
        R.add("FAIL", g, "the PDF has no extractable text")
        return
    full = w.norm(" ".join(pages))
    miss = [it["id"] for _, it in w.all_items(content) if w.norm(it["text"]) not in full]
    if miss:
        R.add("FAIL", g, "PDF text does not contain items: %s" % miss)
    heads = [h for h in b["headings"] if w.norm(h) not in full]
    if heads:
        R.add("FAIL", g, "PDF is missing headings: %s" % heads)
    hn = {w.norm(h) for h in b["headings"]}
    for i, pg in enumerate(pages[:-1], 1):
        ls = [x.strip() for x in pg.split("\n") if x.strip()]
        if ls and w.norm(ls[-1]) in hn:
            R.add("FAIL", g, "heading '%s' is stranded at the bottom of page %d" % (ls[-1], i))
    if len(pages) > 2:
        R.add("WARN", g, "the PDF is %d pages: the skill aims at two at most" % len(pages))
    if not miss and not heads:
        R.add("PASS", g, "PDF '%s': %d page(s), every heading and item present, no stranded heading" % (names["pdf"], len(pages)))
    pngs = sorted(f for f in os.listdir(out) if f.startswith("page") and f.endswith(".png"))
    if len(pngs) != len(pages) or any(os.path.getsize(os.path.join(out, f)) < 3000 for f in pngs):
        R.add("FAIL", g, "page images for the visual check are missing (%d images for %d pages)" % (len(pngs), len(pages)))
    else:
        R.add("PASS", g, "page images rendered for the visual check: %s" % pngs)


# ---------------------------------------------------------------- F receipt
def truthy(v):
    return v is True or (isinstance(v, str) and v.strip().lower() == "true")


def check_receipt(run, content, R):
    g = "F"
    p = os.path.join(run, w.RECEIPT)
    if not os.path.exists(p):
        R.add("FAIL", g, "receipt.json missing: record the hand-over evidence before declaring the run complete (run.py receipt)")
        return
    rc = w.load_json(p)
    names = w.output_names(content)
    mt = content["meeting_type"]
    probs = 0

    def fail(m):
        nonlocal probs
        probs += 1
        R.add("FAIL", g, m)

    def text(d, *keys, n=1):
        return all(len(str((d or {}).get(k) or "").strip()) >= n for k in keys)

    # Planner page: published as the right-hand-pane page, or the stated fallback
    pp = rc.get("planner_page") or {}
    if pp.get("mode") == "artifact":
        if not str(pp.get("url") or "").startswith("https://claude.ai/"):
            fail("planner_page.url must be the link returned by the page (Artifact) tool, starting https://claude.ai/")
        else:
            R.add("ATTEST", g, "Planner note published as a page with a Copy button: %s" % pp["url"])
    elif pp.get("mode") == "fallback_text":
        if not text(pp, "reason", n=10):
            fail("planner_page.reason: say why the page tool was unavailable (the fallback must be stated)")
        else:
            R.add("ATTEST", g, "Planner note shown as formatted chat text (FALLBACK, page tool unavailable: %s)" % pp["reason"][:60])
    else:
        fail("planner_page.mode must be 'artifact' or 'fallback_text'")

    if mt != "first":
        if not truthy(rc.get("pdf_sent_in_chat")):
            fail("the PDF must be sent in the chat for download (pdf_sent_in_chat)")
        else:
            R.add("ATTEST", g, "PDF sent in the chat")
        sv = rc.get("saved") or {}
        if not text(sv, "tool", "folder", "filename", "tool_result", "folder_listing_check"):
            fail("saved{tool, folder, filename, tool_result, folder_listing_check} must all be filled from the real tool output")
        else:
            before = probs
            if sv["filename"] != names["pdf"]:
                fail("saved.filename %r is not the expected %r" % (sv["filename"], names["pdf"]))
            if names["pdf"] not in sv["folder_listing_check"]:
                fail("saved.folder_listing_check does not show the file in the folder listing")
            if "2. Fact Find" not in sv["folder"]:
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

    # Teams message to Sitamah (Step 8): last thing, only with Paul's yes
    tm = rc.get("teams") or {}
    status = tm.get("status")
    if mt == "whatsapp":
        R.add("ATTEST", g, "Teams message not applicable to a WhatsApp call")
    elif status == "sent":
        if not text(tm, "message_id", "sent_time", "approved_by_paul"):
            fail("teams: status=sent needs message_id and sent_time from Zapier and approved_by_paul (Paul's own words)")
        else:
            R.add("ATTEST", g, "Teams message sent to Sitamah via Zapier after Paul's yes (message id %s, %s)" % (tm["message_id"], tm["sent_time"]))
    elif status == "declined":
        if not text(tm, "paul_said", n=2):
            fail("teams: status=declined needs paul_said (his words)")
        else:
            R.add("ATTEST", g, "Paul declined the Teams message")
    elif status == "failed":
        if not text(tm, "detail", n=8) or not truthy(tm.get("text_given_to_paul")):
            fail("teams: status=failed needs detail (the error) and text_given_to_paul=true")
        else:
            R.add("ATTEST", g, "Teams send failed; message text given to Paul to paste (not claimed as sent)")
    else:
        fail("teams.status must be sent, declined or failed: the Teams message to Sitamah is the last step of every Teams meeting")


# ---------------------------------------------------------------- driver
def run_checks(run, stage):
    R = Results()
    st = w.load_json(os.path.join(run, w.STATE), "state.json (run tx.py prep first)")
    check_reading(run, st, R)
    lines = w.read_lines(run)
    lp, cp = os.path.join(run, w.LEDGER), os.path.join(run, w.CONTENT)
    ledger = w.load_json(lp) if os.path.exists(lp) else None
    content = w.load_json(cp) if os.path.exists(cp) else None
    check_sources(run, meeting_type_of(run, content), R)
    if ledger is None:
        R.add("FAIL", "B", "ledger.json missing (record the decision ledger after Pass 1)")
    if content is None:
        R.add("FAIL", "C", "content.json missing")
    if ledger is not None and content is not None:
        idx, dup = item_index(content)
        check_ledger(run, st, lines, ledger, idx, R)
        check_content(run, st, lines, content, idx, dup, R)
        check_declared(content, idx, R)
        if stage in ("built", "final") and not R.fails:
            check_outputs(run, st, content, R)
        elif stage in ("built", "final"):
            R.add("FAIL", "E", "outputs not checked: fix the failures above first")
        if stage == "final" and not R.fails:
            check_receipt(run, content, R)
        elif stage == "final":
            R.add("FAIL", "F", "hand-over not checked: fix the failures above first")
    return R, st, ledger, content


def report(R, st, ledger, content, stage):
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
        print("\nDELIVERY LINE (copy into the reply, unedited):")
        print("Transcript read in full TWICE (Pass 1 and Pass 2, %d lines each, %d chunks); %d ledger entries; "
              "every bullet and action source-traced (%d sources, all quotes found in the transcript or named documents)."
              % (st["total_lines"], k, len(ledger["entries"]), n_src))
        print("Attested by Claude, not machine-proven: chat hand-over, saving to the client's folder, visual check of the page images.")
    elif fails:
        print("\nNOT COMPLETE. You may not tell Paul this run is finished. Fix every FAIL above and re-run.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    ap.add_argument("--stage", choices=["pre", "built", "final"], default="final")
    a = ap.parse_args()
    R, st, ledger, content = run_checks(a.run, a.stage)
    report(R, st, ledger, content, a.stage)
    sys.exit(1 if R.fails else 0)


if __name__ == "__main__":
    main()
