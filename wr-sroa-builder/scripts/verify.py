#!/usr/bin/env python3
"""The one checker of the wr-sroa-builder.

  verify.py <run_dir> [pre|final] [--full]

It re-reads the registered documents, re-checks every answer against their text, rebuilds the data the program assembles, reopens the finished
PDF and proves the checks a program can prove. The reply to Paul carries the SHORT AUDIT it prints: one line per check with a green tick or a red
cross, and one closing line for what is only attested (Paul, 03/11/2026). The full record is written to out_record/audit-full.txt.
"""
import hashlib
import json
import os
import sys

import docread
import pdfcheck
import sroa
import wrlib as w

OK, BAD = "✅", "❌"
STEP_IDS = ["locate", "read", "answers", "confirm", "build", "check", "save", "final"]
ALWAYS = ("current_ps", "acceptance_email", "fact_find_summary")


class Results:
    def __init__(self):
        self.rows, self.attested, self.group = [], [], ""

    def add(self, ok, short, detail=""):
        self.rows.append((OK if ok else BAD, short, detail, self.group))

    @property
    def fails(self):
        return [r for r in self.rows if r[0] == BAD]


def route_order_problems(log):
    bad, failed = [], set()
    for e in log:
        i = w.ROUTES.index(e["route"])
        if any(r not in failed for r in w.ROUTES[:i]):
            bad.append(e["route"])
        if e["result"] == "failed":
            failed.add(e["route"])
    return bad


def sha_of(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def load_docs(run):
    """(docs.json, {role: Evidence or None})"""
    docs = w.load_opt(os.path.join(run, w.DOCS), {"docs": {}, "missing": {}})
    ev = {}
    for role, d in docs["docs"].items():
        try:
            ev[role] = docread.Evidence(w.load_json(os.path.join(run, d["text_file"])))
        except Exception:
            ev[role] = None
    return docs, ev


def served_keys(docs):
    keys = []
    for role in sroa.SERVED_ROLES:
        d = docs["docs"].get(role)
        if d:
            keys += [(role, n) for n in d["served"]]
    return keys


def needed_roles(a):
    need = list(ALWAYS)
    if a and isinstance(a.get("compiled"), dict) and a.get("accepted") in sroa.QUOTES:
        need += [sroa.QUOTE_ROLE[q] for q in sroa.QUOTES if a["compiled"].get(q)]
    return need


def run_checks(run, stage):
    R = Results()
    rj = w.load_json(os.path.join(run, w.RUN))
    st = w.load_opt(os.path.join(run, w.STATE), {})
    today = w.parse_date(rj["today"])
    docs, ev = load_docs(run)
    a = w.load_opt(os.path.join(run, w.ANSWERS), None)
    # ---------------------------------------------------------------- the documents
    R.group = "docs"
    log = [e for e in w.load_opt(os.path.join(run, w.ACCESS), []) if e.get("purpose") == "locate"]
    need = needed_roles(a)
    absent = [r for r in need if r not in docs["docs"] and not (docs["missing"].get(r) or "").strip()]
    if not a and not any(r in docs["docs"] for r in sroa.QUOTE_ROLE.values()):
        absent.append("a quote (fna_quote, shortfall_quote or alternative_quote)")
    changed = [r for r, d in docs["docs"].items() if not os.path.exists(os.path.join(run, d["file"])) or w.sha256_file(os.path.join(run, d["file"])) != d["sha"]]
    bad = route_order_problems(log)
    ps = docs["docs"].get("current_ps")
    ps_ok = bool(ps) and bool(ps.get("served")) and docread.alnum(ps.get("policy")) == docread.alnum(rj.get("policy"))
    good = not absent and not changed and bool(log) and not bad and ps_ok
    R.add(good, "The client's documents are registered (%s), unchanged; only the pages of policy %s were taken from the Current Policy Schedule (page%s %s); the routes were tried in order, each try logged (%d on record)" %
          (", ".join(sorted(docs["docs"])), rj["policy"], "" if len(ps["served"]) == 1 else "s", ", ".join(map(str, ps["served"])), len(log)) if good else
          "Documents problem: missing %s; changed %s; route log %s; Current Policy Schedule %s" %
          (absent or "none", changed or "none", "out of order" if bad else ("empty" if not log else "fine"), "fine" if ps_ok else "not registered for this policy"),
          "; ".join("%s %s" % (e["route"], e["result"]) for e in log))
    said = [r for r in need if r in docs["missing"]]
    if said:
        R.attested.append("the document(s) Paul said are not available: %s" % ", ".join(said))
    # ---------------------------------------------------------------- reading lock
    R.group = "read"
    if docs["docs"]:
        acked = st.get("read", {}).get("acked", {})
        todo = ["%s:%d" % k for k in served_keys(docs)]
        miss = [k for k in todo if len((acked.get(k) or "").strip()) < 3]
        R.add(not miss, "Every page of the policy's schedule pages, the quotes and the acceptance email was served in order and acknowledged (%d of %d)" % (len(todo) - len(miss), len(todo)) if not miss else
              "Pages not yet acknowledged: %s" % ", ".join(miss[:6]))
        image_only = [r for r, d in docs["docs"].items() if d.get("image_only")]
        if image_only:
            R.attested.append("anything on page(s) with no readable text in: %s" % ", ".join(image_only))
    # ---------------------------------------------------------------- the answers
    R.group = "answers"
    ok_a = False
    if a:
        pr = sroa.answers_problems(a, ev, today, rj["client"])
        if docread.alnum(a.get("policy_number")) != docread.alnum(rj.get("policy")):
            pr.append("the policy number %r is not the policy this run was started for (%s)" % (a.get("policy_number"), rj.get("policy")))
        ok_a = not pr
        R.add(ok_a, "Answers valid and sourced (%s %s for %s, SROA date %s); the typed layout, headings, units and the R20 premium label are in the fixed form; conflicts: none" %
              (a["insurer"], a["policy_number"], a["client_signature_name"], a["sroa_date"]) if ok_a else "Answers problem: %s" % pr[0], "; ".join(pr))
        if ok_a:
            R.add(True, "Name, ID, policy and CP numbers, the date and every old and new figure were found in the right documents' own text; 'No change' is worked out by the program")
            if any(e is not None and not e.has_text for e in ev.values()):
                R.attested.append("figures in a document with no readable text")
    else:
        R.add(False, "The answers have not been entered yet", "step 'answers'")
    # ---------------------------------------------------------------- Paul's yes
    R.group = "confirm"
    ap = w.load_opt(os.path.join(run, w.APPROVAL), None)
    if ok_a:
        cur = sha_of({"answers": a, "table": sroa.table_rows(a)})
        good = bool(ap) and ap.get("sha") == cur and len((ap.get("said") or "").strip()) >= 3 and st.get("shown_sha") == cur
        R.add(good, "Paul was shown the confirmation table and said yes to exactly these answers" if good else
              "No valid yes from Paul for these answers: run.py show, put the table in the reply, then run.py approve with his words")
        if good:
            R.attested.append("Paul's yes (the words are typed by the chat)")
    # ---------------------------------------------------------------- the built PDF
    R.group = "build"
    bd = st.get("build")
    pdf_path = os.path.join(run, w.OUT, bd["pdf"]) if bd else None
    data = None
    if ok_a and bd and pdf_path and os.path.exists(pdf_path):
        data = sroa.assemble(a)
        same_file = w.sha256_file(pdf_path) == bd["sha"] and sha_of(data) == bd["data_sha"]
        R.add(same_file, "The SROA is exactly what the program builds from the confirmed answers with the fixed script (not edited by hand)")
        R.add(not bd.get("warnings"), "The fixed script printed no warning while it drew the pages" if not bd.get("warnings") else "The script warned: %s" % bd["warnings"][0])
    elif ok_a:
        R.add(False, "The SROA has not been built yet", "step 'build'")
    # ---------------------------------------------------------------- the PDF opened and checked
    R.group = "pdf"
    if data and os.path.exists(pdf_path):
        res = pdfcheck.check(pdf_path, data, a)
        badr = [r for r in res if not r[0]]
        if not badr:
            R.add(True, "The finished SROA was reopened and passed all %d program checks (order and text of every block, ID under Owner, CP lines, premium label, narratives, N/A rule, "
                  "typed names, FSP45946, two empty date fields, nothing clipped, logo, signature lines)" % len(res), "; ".join(r[1] for r in res))
        else:
            for ok, short, detail in badr:
                R.add(False, short, detail)
            R.add(True, "%d other program checks on the finished SROA passed" % (len(res) - len(badr)), "; ".join(r[1] for r in res if r[0]))
        R.attested.append("how the pages look to the eye (logo, spacing, crowding)")
    # ---------------------------------------------------------------- the save
    R.group = "save"
    sv = st.get("save")
    rc = w.load_opt(os.path.join(run, w.RECEIPT), {})
    slog = [e for e in w.load_opt(os.path.join(run, w.ACCESS), []) if e.get("purpose") == "save"]
    if data and sv:
        local = os.path.join(run, w.OUT, sv["name"])
        size = os.path.getsize(local) if os.path.exists(local) else -1
        derived = sroa.delivery_filename(a)
        R.add(sv["name"] == derived and size == bd["size"], "The file name is derived, not typed: %s" % sv["name"] if sv["name"] == derived else "The saved file name is not the derived name")
        folder = rc.get("save.folder", "")
        good = bool(slog) and not route_order_problems(slog) and folder.rstrip("\\/").lower().endswith("servicing") and (rc.get("save.listed_bytes") or "").strip() == str(size)
        R.add(good, "Saved in the client's Servicing folder through the routes in order; the listing shows %d bytes, equal to the local file%s" % (size, " (Paul said to overwrite)" if sv.get("overwrite") else "")
              if good else "The save is not proven: record the save tries in order, the folder (ending Servicing) and the listed size (%d bytes)" % size)
        R.add(not sv.get("existing_clash") or bool(sv.get("overwrite")), "No existing file was overwritten without Paul's yes" if not sv.get("existing_clash") or sv.get("overwrite") else
              "A file with this name exists and Paul has not said to overwrite")
        R.attested.append("that the file really sits in the client's folder (the listing is typed by the chat)")
    if stage == "final":
        R.group = "final"
        done = [s for s in STEP_IDS[:-1] if (rj.get("steps", {}).get(s) or {}).get("state") == "done"]
        fpok = rj.get("program_fingerprint") == w.program_fingerprint()
        R.add(done == STEP_IDS[:-1] and fpok, "Every step done in order (%d of %d) and the programs and the logo did not change during the run" % (len(done), len(STEP_IDS) - 1) if done == STEP_IDS[:-1] and fpok else
              "Steps done: %s%s" % (", ".join(done) or "none", "; the programs changed during the run" if not fpok else ""))
        R.attested += ["the advice itself, the reason for the change and the SROA date (judgement, recorded with sources)",
                       "that each figure sits in the right row and column of its document (it is only proven to appear in it), and that this is the policy and the quote Paul meant"]
    return R, rj


def print_audit(R, rj, stage, run, full=False):
    lines = ["AUDIT   %s" % w.version_line()]
    for mark, short, detail, _g in R.rows:
        lines.append("%s %s" % (mark, short))
    if R.attested:
        seen, uniq = set(), []
        for x in R.attested:
            if x not in seen:
                seen.add(x)
                uniq.append(x)
        lines.append("Only attested (not proven): " + "; ".join(uniq) + ".")
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
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    run = os.path.abspath(args[0])
    stage = args[1] if len(args) > 1 and args[1] in ("pre", "final") else "final"
    R, rj = run_checks(run, stage)
    ok = print_audit(R, rj, stage, run, full="--full" in sys.argv)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
