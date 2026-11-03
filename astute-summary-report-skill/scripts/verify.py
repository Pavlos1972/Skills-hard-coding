#!/usr/bin/env python3
"""The one checker of the astute-summary-report-skill.

  verify.py <run_dir> [pre|final] [--full]

It re-reads the Astute report itself, re-checks every entry against the report's text, recomputes the totals, the flags and the whole content, and
reads the finished PDF back. The reply to Paul carries the SHORT AUDIT it prints: one line per check with a green tick or a red cross, and one
closing line for what is only attested (Paul, 03/11/2026). The full record is written to out_record/audit-full.txt.
"""
import os
import sys

import model
import report
import wrlib as w

OK, BAD = "✅", "❌"
STEP_IDS = ["locate", "read", "data", "products", "flags", "build", "save", "final"]
LANDSCAPE_A4 = (841.89, 595.28)


class Results:
    def __init__(self):
        self.rows, self.attested, self.group = [], [], ""

    def add(self, ok, short, detail=""):
        self.rows.append((OK if ok else BAD, short, detail, self.group))

    @property
    def fails(self):
        return [r for r in self.rows if r[0] == BAD]


def route_order_problems(log):
    """The routes are tried in order (computer, Microsoft 365, Zapier): a later route is used only after every earlier one failed."""
    bad, failed = [], set()
    for e in log:
        i = w.ROUTES.index(e["route"])
        if any(r not in failed for r in w.ROUTES[:i]):
            bad.append(e["route"])
        if e["result"] == "failed":
            failed.add(e["route"])
    return bad


def pdf_facts(path):
    import pdfplumber
    with pdfplumber.open(path) as pdf:
        return [{"w": float(p.width), "h": float(p.height), "text": p.extract_text() or ""} for p in pdf.pages]


def run_checks(run, stage):
    R = Results()
    rj = w.load_json(os.path.join(run, w.RUN))
    st = w.load_opt(os.path.join(run, w.STATE), {})
    # ---------------------------------------------------------------- the report
    R.group = "report"
    rep = None
    pdf = os.path.join(run, w.REPORT_PDF)
    log = [e for e in w.load_opt(os.path.join(run, w.ACCESS), []) if e.get("purpose") == "locate"]
    if not os.path.exists(pdf) or not rj.get("source"):
        R.add(False, "The Astute report is not in the run folder yet", "step 'locate': run.py source")
    else:
        try:
            rep = report.read_pdf(pdf)
        except Exception as e:
            R.add(False, "The report could not be read: %s" % e)
        if rep:
            same = w.sha256_file(pdf) == rj["source"]["sha256"]
            R.add(same, "The Astute report is a real PDF of %d page(s), unchanged since it was copied%s" % (rep["page_count"], (" (no readable text on page(s) %s)" % ", ".join(map(str, rep["image_only"]))) if rep["image_only"] else "")
                  if same else "The report in the run folder changed after it was copied")
            bad = route_order_problems(log)
            R.add(bool(log) and not bad and any(e["result"] == "found" for e in log),
                  "Routes tried in order, each try logged (%d on record); report found via %s" % (len(log), rj["source"]["route"]) if log and not bad else
                  "The route log is empty or out of order%s" % ((": " + ", ".join(bad)) if bad else ""), "; ".join("%s %s" % (e["route"], e["result"]) for e in log))
    # ---------------------------------------------------------------- reading lock
    R.group = "read"
    if rep:
        acked = st.get("read", {}).get("acked", {})
        missing = [n for n in range(1, rep["page_count"] + 1) if len((acked.get(str(n)) or "").strip()) < 3]
        R.add(not missing, "Every page was served in order and acknowledged (%d of %d)" % (rep["page_count"] - len(missing), rep["page_count"]) if not missing else
              "Pages not yet acknowledged: %s" % ", ".join(map(str, missing)))
    # ---------------------------------------------------------------- the entered data
    R.group = "data"
    data = w.load_opt(os.path.join(run, w.DATA), None)
    products = w.load_opt(os.path.join(run, w.PRODUCTS), {})
    chat = w.load_opt(os.path.join(run, w.FLAGS), {}).get("flags", [])
    ok_data = False
    if not data:
        R.add(False, "The report's data has not been entered yet", "step 'data': run.py data --file ...")
    else:
        sp = model.schema_problems(data)
        R.add(not sp, "Data entered in the fixed layout: %d provider(s), %d policy(ies)" % (len(data.get("providers") or []), len(data.get("policies") or [])) if not sp
              else "Data problem: %s" % sp[0], "; ".join(sp))
        if not sp:
            ok_data = True
            nben = sum(len(p.get("benefits") or []) for p in data["policies"])
            R.add(True, "Every benefit (%d) is labelled stand-alone, accelerated or unable, and every policy has a premium pattern" % nben)
            if rep:
                ep = report.evidence_problems(data, rep)
                if ep is None:
                    R.add(True, "The report has no readable text, so the figures could not be checked against it (see the attested line)")
                    R.attested.append("every figure, policy number, date and name, because the report has no readable text")
                else:
                    R.add(not ep, "Every policy number, figure, date and name entered was found in the report's own text" if not ep else
                          "%d entry(ies) not found in the report's text: %s" % (len(ep), ep[0]), "; ".join(ep))
                    if rep["image_only"]:
                        R.attested.append("anything on the page(s) with no readable text (%s)" % ", ".join(map(str, rep["image_only"])))
            secs = {}
            for p in data["policies"]:
                secs[model.section_of(p)] = secs.get(model.section_of(p), 0) + 1
            tot = model.total_amounts(data)
            R.add(True, "Policies placed by their Astute status: %d active, %d paid-up, %d other. Totals added up by the program: premiums %s a month, fund value %s" %
                  (secs.get("active", 0), secs.get("paid_up", 0), secs.get("inactive", 0) + secs.get("unrecognised", 0), w.fmt_money(tot["monthly_premiums"]), w.fmt_money(tot["fund_value"])))
    # ---------------------------------------------------------------- products
    R.group = "products"
    if ok_data:
        pp = model.product_problems(data, products)
        names = model.product_names(data)
        unconf = [n for n in names if (products.get(w.norm(n)) or {}).get("state") == "unconfirmed"]
        R.add(not pp, "Every product (%d) has a source or is flagged as not confirmed online (%d unconfirmed)" % (len(names), len(unconf)) if not pp else "Product problem: %s" % pp[0], "; ".join(pp))
    # ---------------------------------------------------------------- flags
    R.group = "flags"
    if ok_data:
        fp = model.flag_problems(data, chat)
        confirmed = bool(chat) or bool(st.get("flags_none"))
        R.add(not fp and confirmed, "Flags: %d raised by the program, %d judgement flag(s) added" % (len(model.computed_flags(data, products)), len(chat)) if not fp and confirmed else
              ("Flag problem: %s" % fp[0] if fp else "The judgement flags were not considered: add them (run.py flag) or say none are needed (run.py flag --none ...)"), "; ".join(fp))
    # ---------------------------------------------------------------- the built PDF
    R.group = "build"
    content = w.load_opt(os.path.join(run, w.CONTENT), None)
    b = st.get("build")
    if ok_data and not model.product_problems(data, products):
        if not content or not b:
            R.add(False, "The PDF has not been built yet", "step 'build'")
        else:
            expected = model.compose(data, products, chat, rj["client"])
            R.add(content == expected and w.content_hash(content) == b["content_sha"], "The content is exactly what the program composes from the entered data (not edited by hand)")
            path = os.path.join(run, w.OUT, b["pdf"])
            if not os.path.exists(path) or w.sha256_file(path) != b["pdf_sha"]:
                R.add(False, "The PDF is missing or changed after it was built")
            else:
                pages = pdf_facts(path)
                land = all(abs(p["w"] - LANDSCAPE_A4[0]) < 2 and abs(p["h"] - LANDSCAPE_A4[1]) < 2 for p in pages)
                foot = all(content["footer"] in p["text"] and ("Page %d" % (i + 1)) in p["text"] for i, p in enumerate(pages))
                R.add(land and foot, "The PDF is landscape A4, %d page(s), with the footer and page number on every page" % len(pages) if land and foot else
                      "The PDF layout is wrong (landscape A4: %s; footer on every page: %s)" % (land, foot))
                text = "\n".join(p["text"] for p in pages)
                flat = report.alnum(text)
                absent = [n for n in content["policy_numbers"] if report.alnum(n) not in flat]
                pos = [text.find(h) for h in content["headings"]]
                R.add(not absent and all(x >= 0 for x in pos) and pos == sorted(pos),
                      "The PDF read back contains all %d policy numbers and the 5 headings in the fixed order" % len(content["policy_numbers"]) if not absent and all(x >= 0 for x in pos) and pos == sorted(pos) else
                      "The PDF read back is missing policy numbers %s or its headings are out of order" % (absent or "none"))
                R.attested.append("how the pages look to the eye (the page images are saved; viewing them is the chat's)")
    # ---------------------------------------------------------------- the save
    R.group = "save"
    sv = st.get("save")
    rc = w.load_opt(os.path.join(run, w.RECEIPT), {})
    slog = [e for e in w.load_opt(os.path.join(run, w.ACCESS), []) if e.get("purpose") == "save"]
    if b and sv:
        path = os.path.join(run, w.OUT, sv["name"])
        size = os.path.getsize(path) if os.path.exists(path) else -1
        derived = content["file_name"] if content else None
        stem_ok = derived and (sv["name"] == derived or sv["name"].startswith(derived[:-4] + " ("))
        folder = rc.get("save.folder", "")
        R.add(bool(stem_ok) and size == b["pdf_size"], "The file name is derived, not typed: %s" % sv["name"] if stem_ok else "The saved file name is not the derived name")
        R.add(bool(slog) and "5. astute" in folder.lower() and (rc.get("save.listed_bytes") or "").strip() == str(size),
              "Saved in the client's 5. Astute folder; the folder listing shows %s bytes, equal to the local file%s" % (size, " (existing file kept, new one numbered)" if sv["name"] != derived else "")
              if slog and "5. astute" in folder.lower() and (rc.get("save.listed_bytes") or "").strip() == str(size) else
              "The save is not proven: record the save try, the folder (ending 5. Astute) and the listed size (%s bytes)" % size)
        R.attested.append("that the file really sits in the client's folder (the listing is typed by the chat)")
    if stage == "final":
        R.group = "final"
        done = [s for s in STEP_IDS[:-1] if (rj.get("steps", {}).get(s) or {}).get("state") == "done"]
        fpok = rj.get("program_fingerprint") == w.program_fingerprint()
        R.add(done == STEP_IDS[:-1] and fpok, "Every step done in order (%d of %d) and the programs did not change during the run" % (len(done), len(STEP_IDS) - 1) if done == STEP_IDS[:-1] and fpok else
              "Steps done: %s%s" % (", ".join(done) or "none", "; the programs changed during the run" if not fpok else ""))
        R.attested += ["that the chat understood each page and that every figure sits on the right policy (a real figure on the wrong policy passes the text check)",
                       "that each product description is true (only the recorded source is checked)"]
    return R, rj


def print_audit(R, rj, stage, run, full=False):
    lines = ["AUDIT   %s" % w.version_line()]
    for mark, short, detail, _g in R.rows:
        lines.append("%s %s" % (mark, short))
    if R.attested:
        seen, uniq = set(), []
        for a in R.attested:
            if a not in seen:
                seen.add(a)
                uniq.append(a)
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


def flag_list(run):
    """The numbered flag list for the chat (most important first), built from the same data as the PDF."""
    content = w.load_opt(os.path.join(run, w.CONTENT), None)
    if not content:
        return []
    return ["%d. %s: %s" % (f["n"], f["title"], f["text"]) for f in content["flags"]]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    run = os.path.abspath(args[0])
    stage = args[1] if len(args) > 1 and args[1] in ("pre", "final") else "final"
    R, rj = run_checks(run, stage)
    ok = print_audit(R, rj, stage, run, full="--full" in sys.argv)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
