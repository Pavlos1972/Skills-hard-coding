#!/usr/bin/env python3
"""The one checker of the life-policy-schedule-analyzer skill.

  verify.py <run_dir> [pre|final] [--full]

It re-reads the registered documents, re-checks the analysis against their text (the schedules, the proposed quote and its payback document, the Fact Find Summary, the saved product
sources), recomputes the premium tables and the findings' numbers, reads the finished PDFs back (the internal report(s) and the client slides) and checks them against the analysis, checks
that the files are as built and saved, and prints the SHORT AUDIT: one line per check with a green tick or a red cross, and one closing line for what is only attested (Paul, 03/11/2026).
The full record is written to out_record/audit-full.txt.
"""
import hashlib
import json
import os
import sys

import docread
import lpa as c
import lpapdf as b
import wrlib as w

OK, BAD = "✅", "❌"
STEP_IDS = ["locate", "read", "research", "analysis", "check", "confirm", "build", "save", "final"]


class Results:
    def __init__(self):
        self.rows, self.attested, self.group = [], [], ""

    def add(self, ok, short, detail=""):
        self.rows.append((OK if ok else BAD, short, detail, self.group))

    @property
    def fails(self):
        return [r for r in self.rows if r[0] == BAD]


def route_order_problems(log, routes=None):
    routes = routes or w.ROUTES
    bad, failed = [], set()
    for e in log:
        if e["route"] not in routes:
            bad.append(e["route"])
            continue
        i = routes.index(e["route"])
        if any(r not in failed for r in routes[:i]):
            bad.append(e["route"])
        if e["result"] == "failed":
            failed.add(e["route"])
    return bad


def sha_of(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def confirm_sha(raw, docs, ev, state, today):
    """What Paul's yes is bound to: the analysis, the declared insurers, every registered document, everything shown in the table, the check results, the wording and the settings."""
    ann = _annotated(raw, ev, docs, state, today)
    return sha_of({"analysis": raw, "insurers": c.declared(state), "docs": {k: d["sha"] for k, d in docs["docs"].items()}, "check": c.check_summary(ann, today),
                   "table": b.table_rows(ann, docs, ev, today), "settings": c.settings(), "wording": c.wording(), "slide_words": c.slide_words()})


def _annotated(raw, ev, docs, state, today):
    return c.annotate(raw, ev, docs, today, None, state)[0]


def load_docs(run):
    docs = w.load_opt(os.path.join(run, w.DOCS), {"docs": {}, "missing": {}})
    ev = {}
    for key, d in docs["docs"].items():
        try:
            ev[key] = docread.Evidence(w.load_json(os.path.join(run, d["text_file"])))
        except Exception:
            ev[key] = None
    return docs, ev


def served_keys(docs, include_sources=True):
    keys = []
    for key in c.served_keys_order(docs):
        if include_sources or docs["docs"][key]["role"] not in ("guide", "source"):
            keys += [(key, n) for n in docs["docs"][key]["served"]]
    return keys


def image_figures(raw):
    out = []

    def walk(x, path):
        if isinstance(x, dict):
            if x.get("image_read"):
                out.append("%s (%s, page %s)" % (path, x.get("source") or "the policy's document", x.get("page")))
            for k, v in x.items():
                walk(v, "%s.%s" % (path, k) if path else k)
        elif isinstance(x, list):
            for i, v in enumerate(x):
                walk(v, "%s[%d]" % (path, i))
    walk(raw, "")
    return out


def docs_problems(docs, state):
    out = []
    if not c.policy_docs(docs):
        out.append("no schedule or quote registered")
    need = dict(c.policy_docs(docs))
    need.update(c.docs_of(docs, "proposed"))
    dec = {d["label"]: d["insurer"] for d in c.declared(state)}
    if sorted(dec) != sorted(need):
        out.append("the insurers are not declared for every schedule, quote and proposed quote (run.py insurers)")
    return out


def research_problems(docs, state):
    dec = c.declared(state)
    if not dec:
        return ["no insurers declared yet (run.py insurers)"]
    out = []
    insurers = sorted({d["insurer"] for d in dec})
    glabels = [d["label"] for d in docs["docs"].values() if d["role"] == "guide"]
    slabels = [d["label"] for d in docs["docs"].values() if d["role"] in ("guide", "source")]
    for ins in insurers:
        if not any(w.norm(g).startswith(w.norm(ins) + " ") for g in glabels) and not (docs["missing"].get(c.dkey("guide", ins)) or "").strip():
            out.append("no guide (and no words from Paul) for %s" % ins)
    for g in slabels:
        if not any(w.norm(g).startswith(w.norm(i) + " ") for i in insurers):
            out.append("the source %r is not one of the declared insurers'" % g)
    return out


def run_checks(run, stage):
    R = Results()
    rj = w.load_json(os.path.join(run, w.RUN))
    st = w.load_opt(os.path.join(run, w.STATE), {})
    rc = w.load_opt(os.path.join(run, w.RECEIPT), {})
    today = w.parse_date(rj["today"])
    docs, ev = load_docs(run)
    raw = w.load_opt(os.path.join(run, w.ANSWERS), None)
    allog = w.load_opt(os.path.join(run, w.ACCESS), [])
    # ---------------------------------------------------------------- the documents
    R.group = "docs"
    log = [e for e in allog if e.get("purpose") == "locate"]
    prob = docs_problems(docs, st)
    changed = [k for k, d in docs["docs"].items() if not os.path.exists(os.path.join(run, d["file"])) or w.sha256_file(os.path.join(run, d["file"])) != d["sha"]]
    bad = route_order_problems(log)
    good = not prob and not changed and bool(log) and not bad
    R.add(good, "The documents are registered (%d schedule/quote(s), %s, the Fact Find Summary %s), unchanged; the routes were tried in order, each try logged (%d)" %
          (len(c.policy_docs(docs)), "a proposed quote%s" % (" with its payback document" if c.docs_of(docs, "payback_doc") else "") if c.docs_of(docs, "proposed") else "no proposed quote",
           "found" if "fact_find_summary" in docs["docs"] else "not found", len(log)) if good else
          "Documents problem: %s; changed %s; route log %s" % ("; ".join(prob) or "none", changed or "none", "out of order" if bad else ("empty" if not log else "fine")),
          "; ".join("%s %s" % (e["route"], e["result"]) for e in log))
    said = [k for k, v in docs["missing"].items() if (v or "").strip()]
    if said:
        R.attested.append("the document(s) Paul said do not exist or could not be found: %s" % ", ".join(sorted(said)))
    # ---------------------------------------------------------------- the reading lock
    R.group = "read"
    if docs["docs"]:
        acked = st.get("read", {}).get("acked", {})
        todo = ["%s:%d" % k for k in served_keys(docs, False)]
        miss = [k for k in todo if len((acked.get(k) or "").strip()) < 3]
        R.add(not miss, "Every page of the %d client document(s) was served in order and acknowledged (%d of %d)" % (len([k for k in docs["docs"] if docs["docs"][k]["role"] not in ("guide", "source")]), len(todo) - len(miss), len(todo)) if not miss else
              "Pages not yet acknowledged: %s" % ", ".join(miss[:6]))
        image_only = [k for k, d in docs["docs"].items() if d.get("image_only")]
        if image_only:
            R.attested.append("anything on page(s) with no readable text in: %s" % ", ".join(sorted(image_only)))
    # ---------------------------------------------------------------- the research
    R.group = "research"
    glog = [e for e in allog if e.get("purpose") == "research"]
    srcs = {k: d for k, d in docs["docs"].items() if d["role"] in ("guide", "source")}
    prob = research_problems(docs, st)
    bad = route_order_problems(glog, w.FACT_ROUTES)
    acked = st.get("read", {}).get("acked", {})
    gmiss = ["%s:%d" % k for k in served_keys(docs) if docs["docs"][k[0]]["role"] in ("guide", "source") and len((acked.get("%s:%d" % k) or "").strip()) < 3]
    good = not prob and not bad and not gmiss and (bool(glog) or not srcs)
    R.add(good, "Every insurer has its own saved guide (%d guide(s), %d independent source(s)), each with its web address and date, read page by page; the routes (web, then Chrome) were tried in order (%d tries)" %
          (len([1 for d in srcs.values() if d["role"] == "guide"]), len([1 for d in srcs.values() if d["role"] == "source"]), len(glog)) if good else
          "Research problem: %s%s%s" % ("; ".join(prob) or "none", "; routes out of order" if bad else "", "; source pages not acknowledged: %s" % ", ".join(gmiss[:3]) if gmiss else ""))
    if srcs:
        R.attested.append("that each saved product source is the real, current page it says it is (the chat saved it; the program cannot prove it)")
    # ---------------------------------------------------------------- the analysis
    R.group = "analysis"
    ok_a, ann = False, None
    if raw:
        ann, pr = c.annotate(raw, ev, docs, today, rj["client"], st)
        ok_a = not pr
        R.add(ok_a, "Analysis valid and sourced (%s: %d polic%s%s; every client figure sits in the evidence line it cites and every evidence line is in the document's text; every product statement has its saved source line)" %
              (raw["client_full_name"], len(raw["policies"]), "y" if len(raw["policies"]) == 1 else "ies", ", a proposed quote" if raw["proposed_status"] == "present" else ", no proposed quote") if ok_a else "Analysis problem: %s" % pr[0], "; ".join(pr))
        if ok_a:
            R.add(True, "The cession, the second life, the dread disease deep-dive, the Vitality and payback sections and a benchmark row for every major benefit held are all present; no invented premium number; client slide text has no internal wording")
            if image_figures(raw):
                R.attested.append("figures read from page images: %s" % "; ".join(image_figures(raw)))
    else:
        R.add(False, "The analysis has not been entered yet", "step 'analysis'")
    # ---------------------------------------------------------------- the check
    R.group = "check"
    ck = st.get("check")
    if ok_a:
        summ = c.check_summary(ann, today)
        good = bool(ck) and ck.get("sha") == sha_of(summ)
        cnt = summ["counts"]
        R.add(good, "The premium tables and the numbered findings were worked out by the program (tables: %s); statements: %d from the documents, %d verified by two sources, %d single-source, %d inference(s)" %
              ("; ".join("%s %s" % (lab, v["mode"]) for lab, v in summ["per_policy"].items()), cnt.get("document", 0), cnt.get("product_verified", 0), cnt.get("product_single", 0), cnt.get("inference", 0)) if good else
              "The check step (run.py check) has not been run for this analysis")
        if cnt.get("product_single"):
            R.attested.append("%d product statement(s) rest on a single source (labelled SINGLE SOURCE in the report)" % cnt["product_single"])
        if cnt.get("inference"):
            R.attested.append("%d statement(s) are inferences labelled 'to be confirmed'" % cnt["inference"])
        R.attested.append("the critique itself: whether the product is good, whether a 'better current option' really exists and is materially better, the Verdict, the Honest Opinion and which tier a finding belongs in (judgement, shown to Paul on the table before the build)")
    # ---------------------------------------------------------------- Paul's yes
    R.group = "confirm"
    ap = w.load_opt(os.path.join(run, w.APPROVAL), None)
    if ok_a:
        cur = confirm_sha(raw, docs, ev, st, today)
        good = bool(ap) and ap.get("sha") == cur and len((ap.get("said") or "").strip()) >= 3 and st.get("shown_sha") == cur
        R.add(good, "Paul was shown the confirmation table (the policies, the findings and tiers, the Verdict and the Honest Opinion, the flags, the slides plan and the file names) and said yes to exactly this analysis" if good else
              "No valid yes from Paul for this analysis: run.py show, put the table in the reply, then run.py approve with his words")
        if good:
            R.attested.append("Paul's yes (the words are typed by the chat)")
    # ---------------------------------------------------------------- the drawn PDFs
    R.group = "build"
    bd = st.get("build")
    if ok_a and bd:
        out = os.path.join(run, w.OUT)
        names = c.all_names(ann, w.parse_date(bd["date"]))
        exact = sorted(bd["files"]) == sorted(names) and all(os.path.exists(os.path.join(out, n)) and w.sha256_file(os.path.join(out, n)) == bd["files"][n]["sha"] for n in names)
        R.add(exact, "The %d PDF(s) are exactly the files the program drew (not edited by hand) and their names are derived, not typed" % len(names) if exact else "The PDFs differ from what the program drew (edited by hand?), or a file name is not the derived one")
        if exact:
            t = w.parse_date(bd["date"])
            allres = []
            for n in names:
                kind, who = bd["files"][n]["kind"], bd["files"][n]["who"]
                path = os.path.join(out, n)
                try:
                    res = b.internal_problems(path, ann, next(x for x in ann["policies"] if x["label"] == who), docs, t) if kind == "internal" else b.slides_problems(path, ann, kind, who, docs, t)
                except Exception as e:  # a PDF that cannot be read back is a red cross, not a crash
                    res = [(False, "%s cannot be read back: %s" % (n, e))]
                allres += [(n, ok, s) for ok, s in res]
            badr = [(n, s) for n, ok, s in allres if not ok]
            if not badr:
                R.add(True, "The finished PDFs were read back and passed all %d checks (the 17 sections in order with the INTERNAL label on every page, the numbered findings in both places, the ten-row premium table, "
                      "four categories and 'Not held' on every slide deck, the payback row and slide, estimates labelled, no internal wording on a slide, all text inside the page)" % len(allres), "; ".join("%s: %s" % (n, s) for n, ok, s in allres))
            else:
                for n, s in badr:
                    R.add(False, "%s: %s" % (n, s))
                R.add(True, "%d other read-back checks on the PDFs passed" % (len(allres) - len(badr)))
            sp = os.path.join(out, "chat_summary.txt")
            want = b.chat_summary(ann, t, "%s > %s" % (ann["plan_folder"], c.settings()["folder_name"]))
            R.add(os.path.exists(sp) and open(sp, encoding="utf-8").read() == want, "The tabulated chat summary (Verdict, Benefit Summary Table, numbered Action Required list, folder) is the one the program builds from the analysis")
        R.attested.append("how the PDFs look and that the plain English is plain (the program checks structure, figures, word lists and page edges, not the eye)")
    elif ok_a:
        R.add(False, "The PDFs have not been drawn yet", "step 'build'")
    # ---------------------------------------------------------------- the save
    R.group = "save"
    sv = st.get("save")
    slog = [e for e in allog if e.get("purpose") == "save"]
    if ok_a and bd and sv:
        folder = rc.get("save.folder", "")
        listed = {}
        for part in (rc.get("save.listed") or "").split(";"):
            if "=" in part:
                k, v = part.rsplit("=", 1)
                listed[k.strip()] = v.strip()
        sizes_ok = all(listed.get(n) == str(bd["files"][n]["size"]) for n in bd["files"])
        good = bool(slog) and not route_order_problems(slog) and folder.rstrip("\\/").lower().endswith(c.settings()["folder_name"].lower()) and w.norm(ann["plan_folder"]) in w.norm(folder) and sizes_ok and sorted(sv["names"]) == sorted(bd["files"])
        R.add(good, "All %d file(s) are saved in %s > %s through the routes in order; the listing shows each file's size, equal to the local file%s" % (len(bd["files"]), ann["plan_folder"], c.settings()["folder_name"], " (Paul said to overwrite)" if sv.get("overwrite") else "")
              if good else "The save is not proven: record the save tries in order, the folder (the client's folder, then %s) and the listing 'name=bytes;...' for every file" % c.settings()["folder_name"])
        R.add(not sv.get("existing_clash") or bool(sv.get("overwrite")), "No existing file was overwritten without Paul's yes" if not sv.get("existing_clash") or sv.get("overwrite") else "A file with this name exists and Paul has not said to overwrite")
        R.attested.append("that the files really sit in the client's folder (the listing is typed by the chat); the optional live Artifact design, if the chat made one, is not part of the program")
    elif ok_a and bd:
        R.add(False, "The save has not been recorded yet", "step 'save'")
    if stage == "final":
        R.group = "final"
        done = [s for s in STEP_IDS[:-1] if (rj.get("steps", {}).get(s) or {}).get("state") == "done"]
        fpok = rj.get("program_fingerprint") == w.program_fingerprint()
        R.add(done == STEP_IDS[:-1] and fpok, "Every step done in order (%d of %d) and the programs, the wording and the settings did not change during the run" % (len(done), len(STEP_IDS) - 1) if done == STEP_IDS[:-1] and fpok else
              "Steps done: %s%s" % (", ".join(done) or "none", "; the programs changed during the run" if not fpok else ""))
        R.attested += ["that every product statement is true (the program proves the cited line is in the saved source, not that the source is right)", "that each evidence line is the right line of its document for the figure it supports"]
        if ann and ok_a:
            fl = c.paul_flags(ann, docs, ev, today)
            if fl:
                R.attested.append("flags for Paul: %s" % "; ".join(fl))
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
