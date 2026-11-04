#!/usr/bin/env python3
"""The one checker of the prospect-review-funnel-at-knowledge.

  verify.py <run_dir> [pre|final] [--full]

It REBUILDS the documents' text, the quoted lines, the answer check, the plan check and the read-backs from the run folder, so nothing is taken on trust from a
file Claude could have edited. The reply to Paul carries the SHORT AUDIT it prints: one line per check with a green tick or a red cross, and one closing line for
what is only attested (Paul, 03/11/2026). The full record is written to out_record/audit-full.txt (--full prints it).
"""
import os
import sys

import engine as eng
import funnel as F
import wrlib as w

OK, BAD = "✅", "❌"


class Results:
    def __init__(self):
        self.rows, self.attested, self.group = [], [], ""

    def add(self, ok, short, detail=""):
        self.rows.append((OK if ok else BAD, short, detail, self.group))

    @property
    def fails(self):
        return [r for r in self.rows if r[0] == BAD]


def run_checks(run, stage):
    R = Results()
    rj = w.load_json(os.path.join(run, w.RUN))
    log = w.load_opt(os.path.join(run, w.ACCESS), [])
    c = eng.compute(run)
    kind = c["kind"]
    cfg = eng.kind_cfg(kind)
    st = F.status()
    # ---------------------------------------------------------------- the skill itself
    R.group = "skill"
    rp = F.route_problems()
    ns, nr, nu = F.stats()
    R.add(not rp, "The stage routes are consistent (%d stages, %d routes)" % (ns, nr) if not rp else "Route problem: %s" % rp[0], "; ".join(rp))
    pp = F.pages_problems()
    R.add(not pp, "The pages agree with the data (stage codes exist, counts come from one file)" if not pp else "Page problem: %s" % pp[0], "; ".join(pp))
    if nu:
        R.attested.append("the owner of %d stage(s) the skill does not state (see the Master Plan)" % nu)
    # ---------------------------------------------------------------- locate
    R.group = "locate"
    docs = c["docs"]
    need = cfg["roles"]
    missing = [r for r in need if r not in docs]
    bad_order = eng.route_order_problems(log)
    not_logged = [r for r, m in docs.items() if m["route"] != "pasted" and not any(e["route"] == m["route"] and e["result"] == "found" and e.get("purpose") == r for e in log)]
    changed = [r for r, m in docs.items() if not m["sha_ok"]]
    ok = not missing and not bad_order and not not_logged and not changed and bool(docs)
    R.add(ok, "%d document(s) located and registered by logged routes, in order, unchanged (%s)" % (len(docs), ", ".join(docs)) if ok else
          "Documents problem: %s" % ("missing %s" % ", ".join(missing) if missing else "routes out of order: %s" % ", ".join(bad_order) if bad_order else "no access try logged for %s" % ", ".join(not_logged) if not_logged else "a registered text changed: %s" % ", ".join(changed) if changed else "no document registered"))
    asof = w.parse_when(st["as_of"])
    stale = [(r, m["modified"]) for r, m in docs.items() if w.parse_when(m["modified"]) and asof and w.parse_when(m["modified"]) > asof]
    if stale:
        R.attested.append("that the skill's pages are current (%s modified after its status date %s)" % (", ".join(x[0] for x in stale), st["as_of"]))
    # ---------------------------------------------------------------- stages, read, proof
    R.group = "stages"
    decl = c["declared"]
    gen = (c["general"] or "").strip()
    named = (c["st"].get("stages") or {}).get("codes") or []
    unknown = [x for x in named if x not in F.stages()]
    okst = (bool(decl) or (kind in ("docs", "review") and len(gen) >= 5)) and not unknown
    R.add(okst, ("Stages named: %s (all exist in the funnel data)" % ", ".join(decl)) if decl and okst else ("No stage is touched (%s)" % gen) if okst else "No valid stage is named (run.py stages)")
    R.group = "read"
    acked = (c["st"].get("read") or {}).get("acked") or {}
    R.add(len(acked) == len(c["pages"]) and bool(c["pages"]), "All %d page(s) for this work were read in order and acknowledged" % len(c["pages"]) if len(acked) == len(c["pages"]) else
          "Not every page was read and acknowledged (%d of %d)" % (len(acked), len(c["pages"])))
    R.group = "proof"
    if decl:
        okp = not c["ev_problems"] and not c["ev_missing"]
        R.add(okp, "Every stage touched (%s) has a line quoted from both documents, found in their text (%d lines)" % (", ".join(decl), len(c["evidence"])) if okp else
              "Quoted lines: %s" % ((c["ev_problems"] or ["missing " + ", ".join(c["ev_missing"])])[0]), "; ".join(c["ev_problems"] + ["missing " + x for x in c["ev_missing"]]))
        R.attested.append("that each quoted line belongs to its stage")
    else:
        R.add(bool(gen), "No stage is touched, so no line needs quoting (%s)" % gen if gen else "No stage is named and no reason is given (run.py stages)")
    # ---------------------------------------------------------------- answer
    if "answer" in cfg["steps"]:
        R.group = "answer"
        if c["answer"] is None:
            R.add(False, "The answer has not been checked yet (run.py answer)")
        else:
            R.add(not c["answer_problems"], "The answer names each stage with its owner and where it leads, and no stage that does not exist" if not c["answer_problems"] else "Answer problem: %s" % c["answer_problems"][0],
                  "; ".join(c["answer_problems"]))
    # ---------------------------------------------------------------- plan, confirm, record
    if "plan" in cfg["steps"]:
        R.group = "plan"
        pl = c["plan"]
        if pl is None:
            R.add(False, "The plan has not been checked yet (run.py plan)")
        else:
            pr = c["plan_problems"] or []
            nt = [x for x in pr if "REFUSED" in x]
            R.add(not nt, "No planned object is one of Charl's" if not nt else "Never-touch: %s" % nt[0])
            rest = [x for x in pr if "REFUSED" not in x]
            nobj = len(pl.get("objects") or [])
            nlines = sum(len(o.get("lines") or []) for o in pl.get("objects") or [])
            R.add(not rest, "The plan follows every rule (%d object(s), %d line(s)%s)" % (nobj, nlines, "" if kind != "test" else ", on %s only" % st["test_client"]["name"]) if not rest else "Plan problem: %s" % rest[0], "; ".join(rest))
        R.group = "confirm"
        ap = c["approval"]
        okc = bool(ap) and len((ap.get("said") or "").strip()) >= 5 and ap.get("plan_sha") == c.get("plan_sha") and c.get("plan_sha") is not None
        R.add(okc, "Paul's go-ahead is recorded for exactly this plan" if okc else "Paul's go-ahead is missing, or the plan changed after it (run.py confirm, then approve)")
        R.attested.append("that the words recorded are Paul's")
        R.group = "record"
        if c["plan"] is not None and c["plan_problems"] == []:
            roles = [d["role"] for d in c["plan"].get("documents") or []]
            if roles:
                R.add(not c["docs_first"], "Documents first (%s): changed after Paul's go-ahead, before AdviceTech" % ", ".join(roles) if not c["docs_first"] else "Documents first: %s" % c["docs_first"][0], "; ".join(c["docs_first"]))
            keys = F.planned_keys(c["plan"], kind)
            if keys:
                n_lines = sum(r.get("lines") or 0 for r in c["results"].values())
                R.add(not c["result_problems"], "All %d planned item(s) were read back with the planned line count (%d lines)" % (len(keys), n_lines) if not c["result_problems"] else "Read-back: %s" % c["result_problems"][0], "; ".join(c["result_problems"]))
                R.attested.append("that AdviceTech, the register and the Master Plan agree (the program checks the chat's read-back record)")
            if kind in ("docs", "review"):
                pass
        else:
            R.add(False, "Nothing to record: the plan is not checked yet")
    R.attested += ["that the funnel logic is right (yours)", "that the six documents agree with each other"]
    if stage == "final":
        R.group = "final"
        ids = cfg["steps"][:-1]
        done = [s for s in ids if (rj.get("steps", {}).get(s) or {}).get("state") == "done"]
        fpok = rj.get("program_fingerprint") == w.program_fingerprint()
        R.add(done == ids and fpok, "Every step done in order (%d of %d); the programs did not change during the run" % (len(done), len(ids)) if done == ids and fpok else
              "Steps done: %s%s" % (", ".join(done) or "none", "; the programs changed during the run" if not fpok else ""))
    return R, rj


def print_audit(R, rj, stage, run, full=False):
    lines = ["AUDIT   %s   (%s)" % (w.version_line(), eng.kind_cfg(rj["kind"])["title"])]
    for mark, short, detail, _g in R.rows:
        lines.append("%s %s" % (mark, short))
    if R.attested:
        lines.append("Only attested (not proven): " + "; ".join(dict.fromkeys(R.attested)) + ".")
    ok = len([r for r in R.rows if r[0] == OK])
    bad = len(R.fails)
    lines.append("RESULT: %s   (%d %s, %d %s)" % ("PASS" if not bad else "FAIL", ok, OK, bad, BAD))
    text = "\n".join(lines)
    print(text)
    fulltext = text + "\n\nFULL RECORD\n" + "\n".join("%s %s\n    %s" % (m, s, d) for m, s, d, _g in R.rows if d)
    try:
        os.makedirs(os.path.join(run, w.OUT + "_record"), exist_ok=True)
        with open(os.path.join(run, w.OUT + "_record", "audit-full.txt"), "w", encoding="utf-8") as f:
            f.write(fulltext + "\n")
    except OSError:
        pass
    if full:
        print("\n" + fulltext.split("FULL RECORD", 1)[1])
    return not bad


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    run = os.path.abspath(args[0])
    stage = args[1] if len(args) > 1 and args[1] in ("pre", "final") else "final"
    R, rj = run_checks(run, stage)
    ok = print_audit(R, rj, stage, run, full="--full" in sys.argv)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
