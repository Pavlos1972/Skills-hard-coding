"""Rebuilds, from the run folder, everything the program is responsible for: the documents' text, the pages to read, the quoted lines, the answer check, the
plan check, the approval, the documents-first order and the read-backs. run.py uses it to decide, verify.py REBUILDS it and compares, so a file edited by hand
cannot pass.
"""
import datetime as dt
import os
import re

import doctext
import funnel as F
import wrlib as w

TOLERANCE = dt.timedelta(seconds=120)          # clock difference between the document store and this machine


def p(run, name):
    return os.path.join(run, name)


def kind_cfg(kind):
    return F.settings()["kinds"][kind]


def steps_for(kind):
    return kind_cfg(kind)["steps"]


def pages_for(kind, declared):
    cfg = kind_cfg(kind)
    S = F.stages()
    pages = list(cfg["pages"])
    for c in declared:
        pg = S[c]["page"] if c in S else None
        if pg and pg not in pages:
            pages.append(pg)
    return sorted(pages)


def route_order_problems(log):
    bad, failed = [], {}
    for e in log:
        if e["route"] not in w.ROUTES:
            continue
        pur = e.get("purpose", "other")
        f = failed.setdefault(pur, set())
        i = w.ROUTES.index(e["route"])
        if any(r not in f for r in w.ROUTES[:i]):
            bad.append("%s (%s)" % (e["route"], pur))
        if e["result"] == "failed":
            f.add(e["route"])
    return bad


def load_docs(run):
    """{role: meta with the text}. A document whose stored text changed is reported by the checker."""
    docs = w.load_opt(p(run, w.DOCS), {})
    out = {}
    for role, m in docs.items():
        path = p(run, m["text_file"])
        text = ""
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                text = f.read()
        out[role] = dict(m, text=text, norm=w.norm(text), sha_ok=os.path.exists(path) and w.sha256_file(path) == m["sha"])
    return out


def evidence_state(docs, declared, evidence):
    """(problems, missing) for the lines quoted from the documents."""
    problems, have, used = [], set(), {}
    need_docs = F.settings()["evidence_docs"]
    minc = F.settings()["evidence_min_chars"]
    for e in evidence:
        d = docs.get(e["doc"])
        n = w.norm(e["line"])
        if e["stage"] not in declared:
            problems.append("a line was quoted for %s, which was not declared" % e["stage"])
        elif d is None:
            problems.append("%s: the document %s is not registered" % (e["stage"], e["doc"]))
        elif len(n) < minc:
            problems.append("%s/%s: the quoted line is too short to prove anything (at least %d characters)" % (e["stage"], e["doc"], minc))
        elif n not in d["norm"]:
            problems.append("%s/%s: the quoted line is not in the document's text: %r" % (e["stage"], e["doc"], e["line"][:70]))
        else:
            other = used.get((e["doc"], n))
            if other and other != e["stage"]:
                problems.append("%s/%s: the same line was already used for %s; each stage needs its own line" % (e["stage"], e["doc"], other))
            used[(e["doc"], n)] = e["stage"]
            have.add((e["stage"], e["doc"]))
    missing = ["%s in %s" % (c, doc) for c in declared for doc in need_docs if (c, doc) not in have]
    return problems, missing


def answer_problems(text, declared, kind):
    S = F.stages()
    t = text or ""
    out = []
    if len(t.strip()) < F.settings()["answer_min_chars"]:
        return ["the answer is too short"]
    codes = set(F.CODE.findall(t))
    for c in sorted(codes):
        if not F.valid_code(c, S):
            out.append("the answer names %s, which is not a stage of the funnel" % c)
    for c in declared:
        if c not in codes:
            out.append("the answer does not name stage %s" % c)
            continue
        s = S[c]
        if s.get("owner") and not re.search(r"\b%s\b" % s["owner"], t):
            out.append("stage %s: the answer does not give its owner (%s)" % (c, s["owner"]))
        targets = {x for o in s["outcomes"] for x in o["to"]}
        if targets and not (targets & codes):
            out.append("stage %s: the answer does not say where it leads (%s)" % (c, ", ".join(sorted(targets))))
    if kind == "move" and not (re.search(r"\btick", t, re.I) and re.search(r"\bopen\b", t, re.I)):
        out.append("moving a client: say which items are still open and which line to tick")
    return out


def docs_first_problems(plan, kind, changed, results, approval):
    """The documents are changed after Paul's yes and before the first AdviceTech change."""
    out = []
    roles = [d["role"] for d in plan.get("documents") or []]
    appr = w.parse_when(approval.get("t_iso", "")) if approval else None
    first = min((w.parse_when(r["t_iso"]) for r in results.values()), default=None)
    for r in roles:
        c = changed.get(r)
        if not c:
            out.append("%s: no change recorded (run.py changed)" % r)
            continue
        mod = w.parse_when(c["modified"])
        if mod is None:
            out.append("%s: the Date Modified could not be read" % r)
            continue
        if appr and mod < appr - TOLERANCE:
            out.append("%s: its Date Modified is before Paul's go-ahead, so it was not changed in this run" % r)
        if first and mod > first + TOLERANCE:
            out.append("%s: changed AFTER the first AdviceTech change; documents come first" % r)
    return out


def results_problems(plan, kind, results):
    out = []
    keys = F.planned_keys(plan, kind)
    for k in keys:
        r = results.get(k)
        if not r:
            out.append("%s: no read-back recorded" % F.title_of(plan, k))
            continue
        if r.get("ok") != "yes":
            out.append("%s: the read-back is not OK%s" % (F.title_of(plan, k), (" (" + r["note"] + ")") if r.get("note") else ""))
        exp = F.expected_lines(plan, k)
        if k.startswith("tick:"):
            n = int(k.split(":")[1])
            exp = (plan.get("tick_path") or [{}])[n - 1].get("expect_lines")
        if exp is not None and r.get("lines") != exp:
            out.append("%s: read back %s line(s), the plan expects %s" % (F.title_of(plan, k), r.get("lines"), exp))
    for k in results:
        if k not in keys:
            out.append("%s: a read-back for something that was not planned" % k)
    return out


def items_table(plan, kind, results):
    """The table AdviceTech work is reported with: one row per item, running totals."""
    rows, done, lines_done, lines_all = [], 0, 0, 0
    keys = F.planned_keys(plan, kind)
    for n, k in enumerate(keys, 1):
        exp = F.expected_lines(plan, k)
        if k.startswith("tick:"):
            exp = (plan.get("tick_path") or [{}])[int(k.split(":")[1]) - 1].get("expect_lines")
        r = results.get(k) or {}
        ok = r.get("ok") == "yes" and (exp is None or r.get("lines") == exp)
        done += 1 if ok else 0
        lines_all += exp or 0
        lines_done += (r.get("lines") or 0) if ok else 0
        rows.append((n, F.title_of(plan, k), "-" if exp is None else exp, r.get("lines", "-"), "OK" if ok else "NOT DONE", "%d of %d" % (done, len(keys)), "%d of %d" % (lines_done, lines_all)))
    return rows


def format_table(rows):
    head = ("#", "Item", "Plan lines", "Read back", "Result", "Items", "Lines")
    allr = [head] + [tuple(str(c) for c in r) for r in rows]
    wd = [max(len(r[i]) for r in allr) for i in range(len(head))]
    return "\n".join(" | ".join(c.ljust(wd[i]) for i, c in enumerate(r)) for r in allr)


def compute(run):
    rj = w.load_json(p(run, w.RUN))
    kind = rj["kind"]
    st = w.load_opt(p(run, w.STATE), {})
    docs = load_docs(run)
    declared = (st.get("stages") or {}).get("codes") or []
    S = F.stages()
    declared = [c for c in declared if c in S]
    ev = st.get("evidence") or []
    ev_problems, ev_missing = evidence_state(docs, declared, ev)
    plan = w.load_opt(p(run, w.PLAN), None)
    registered = set(docs)
    plan_probs = F.plan_problems(plan, kind, declared, registered, F.status()["test_client"]["name"]) if plan is not None else None
    approval = w.load_opt(p(run, w.APPROVAL), None)
    changed = w.load_opt(p(run, w.CHANGED), {})
    results = w.load_opt(p(run, w.RESULTS), {})
    out = {"rj": rj, "kind": kind, "st": st, "docs": docs, "declared": declared, "general": (st.get("stages") or {}).get("general"), "pages": pages_for(kind, declared),
           "evidence": ev, "ev_problems": ev_problems, "ev_missing": ev_missing, "plan": plan, "plan_problems": plan_probs, "approval": approval, "changed": changed,
           "results": results, "answer": None, "answer_problems": None, "docs_first": [], "result_problems": [], "table": []}
    ans = p(run, "answer.txt")
    if os.path.exists(ans):
        with open(ans, encoding="utf-8") as f:
            out["answer"] = f.read()
        out["answer_problems"] = answer_problems(out["answer"], declared, kind)
    if plan is not None and plan_probs == []:
        out["plan_sha"] = w.content_hash(plan)
        out["docs_first"] = docs_first_problems(plan, kind, changed, results, approval)
        out["result_problems"] = results_problems(plan, kind, results)
        out["table"] = items_table(plan, kind, results)
    return out
