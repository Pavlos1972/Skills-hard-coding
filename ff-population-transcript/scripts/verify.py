#!/usr/bin/env python3
"""The checker and the SHORT AUDIT of the ff-population-transcript skill.

  verify.py <run_dir> [--full]

One line per group with a green tick or a red cross, one closing line for what is only attested, RESULT, what Paul should glance at.
The full record is written to <run>/out_record/audit-full.txt (--full prints it). Every check is cheap and local: it asks whether a
step was DONE, never whether a sentence was worded well.
"""
import json
import os
import sys

import tx
import wrlib as w

GROUPS = [("A", "Files"), ("B", "Form read"), ("C", "Transcript read twice"), ("D", "Contact details and lead source"), ("E", "ONE combined report"),
          ("F", "Standing rules"), ("G", "PDF"), ("H", "Saved and approved"), ("I", "Summary, Planner note, Sitamah"), ("J", "Steps and program")]
STEP_ORDER = ["find", "form", "read", "lead", "combine", "build", "save", "chain"]


def load(run, name, default=None):
    return w.load_opt(os.path.join(run, name), default)


def inputs_sha(run):
    """What the combined report is made from: if any of it changes, content.json is out of date."""
    parts = []
    for name in (w.OVERLAY, w.LEAD, w.FORM, w.FORMPDF):
        p = os.path.join(run, name)
        parts.append(w.sha256_file(p) if os.path.exists(p) else "-")
    rj = load(run, w.RUN, {})
    parts.append(json.dumps(rj.get("spouse") or {}, sort_keys=True))
    return w.sha256_text("|".join(parts))


def all_rows(content):
    for s in content.get("sections", []):
        for b in s["blocks"]:
            for r in b["rows"]:
                yield s["title"] + " / " + b["sub"], r
    for r in (content.get("closing") or {}).get("rows", []):
        yield "closing", r
    for r in content.get("other_fields") or []:
        yield "other", r
    for r in content.get("pdf_fields") or []:
        yield "pdf", r


def run_checks(run, finishing=False):
    rows = []

    def add(level, g, msg):
        rows.append((level, g, msg))

    rj = load(run, w.RUN, {})
    form = load(run, w.FORM)
    pdf = load(run, w.FORMPDF, {})
    st = load(run, w.STATE)
    lead = load(run, w.LEAD)
    content = load(run, w.CONTENT)
    files = rj.get("files") or {}

    # A files
    if form:
        add("PASS", "A", "the form's data file %s was recognised by its content (schema %s, saved %s)" % (form["file"], form["schema"], form["modified"]))
    else:
        add("FAIL", "A", "the form's data file was never read (step 1: run.py files)")
    if st and st.get("complete"):
        add("PASS" if not st.get("forced") else "WARN", "A", "%d transcript file(s), %d lines, checked complete%s" % (len(st["parts"]), st["total_lines"], " (FORCED on Paul's say-so)" if st.get("forced") else ""))
    else:
        add("FAIL", "A", "the transcript was never prepared, or is not complete")
    if pdf.get("used"):
        add("PASS", "A", "the form's PDF %s was read whole (%d page(s))" % (pdf.get("file"), pdf.get("pages", 0)))
    else:
        add("WARN", "A", "the form's PDF was not used (%s): the data file alone was the source" % (pdf.get("why") or "not given"))
    if files.get("overview"):
        add("PASS", "A", "the latest Overview was registered as a reference")
    else:
        add("WARN", "A", "no Overview was registered (%s)" % (files.get("missing") or "no reason given"))

    # B form read
    if form:
        stc = form.get("statuses") or {}
        add("PASS", "B", "%d populated fields read (%s)" % (sum(stc.values()), ", ".join("%s %d" % kv for kv in sorted(stc.items()))))
        if pdf.get("used"):
            nf = len(pdf.get("not_found") or [])
            add("WARN" if nf else "PASS", "B", "%d values of the data file were checked against the PDF: %d not found in it" % (pdf.get("checked", 0), nf))
            if content is not None:
                add("PASS", "B", "%d amount(s) only the PDF holds were put into the report under their own heading (none is lost)" % len(content.get("pdf_fields") or []) if content.get("pdf_fields") else
                    "every amount only the PDF holds is in the report already")

    # C transcript
    if st:
        d1, d2 = tx.passes_done(st)
        k = len(st["chunks"])
        if d1 and d2:
            add("PASS", "C", "the transcript was handed over in order and read twice (Pass 1 and Pass 2, %d chunks each)" % k)
        else:
            add("FAIL", "C", "the transcript was not read twice in order (Pass 1 %s, Pass 2 %s)" % ("done" if d1 else "not done", "done" if d2 else "not done"))
    else:
        add("FAIL", "C", "no transcript state")

    # D lead
    if lead:
        if lead.get("found"):
            add("PASS", "D", "the lead source is D&R Marketing (email received %s)" % lead.get("received"))
        elif lead.get("unavailable"):
            add("WARN", "D", "the Outlook search for the D&R Marketing email could not be made: %s" % str(lead.get("unavailable"))[:80])
        else:
            add("PASS", "D", "the Outlook search for a D&R Marketing email was made: %s" % str(lead.get("none"))[:80])
    else:
        add("FAIL", "D", "the lead source was never recorded (step 4)")
    if content:
        empt = [r["label"] for _, r in all_rows(content) if r["id"] in ("cell", "work", "home", "pemail", "wemail") and r["status"] == "empty"]
        if empt:
            add("WARN", "D", "contact details still empty: %s" % ", ".join(empt))

    # E combined report
    cb = rj.get("combine") or {}
    if content is None:
        add("FAIL", "E", "the combined report was never made (step 5: run.py combine)")
    else:
        if cb.get("inputs_sha") != inputs_sha(run):
            add("FAIL", "E", "content.json is out of date: the overlay, the form or the lead changed after the last combine")
        else:
            rep = content.get("report") or {}
            add("PASS", "E", "ONE report made from the form and the call: %d contradiction(s), %d SORTED by a rule, %d HIGHLIGHTED for Paul" % (
                len(rep.get("differences") or []), rep.get("sorted", 0), rep.get("highlighted", 0)))
            add("PASS", "E", "%d quoted call line(s) were found in the transcript; %d document source(s) are not machine-checked (attested)" % (cb.get("call_quotes", 0), cb.get("doc_sources", 0)))
            nd = len(rep.get("not_discussed") or [])
            if nd:
                add("WARN", "E", "%d row(s) left as Not discussed after the search" % nd)
            if rep.get("cleaned"):
                add("PASS", "E", "%d note line(s) of the form were cleaned (listed in the report)" % len(rep["cleaned"]))
        if content.get("unsettled"):
            add("FAIL", "E", "quote request(s) without a known insurer or New Business/Servicing: %s (ask Paul)" % ", ".join(content["unsettled"][:6]))
        if content.get("overlay_unused"):
            add("WARN", "E", "overlay entries that did not land anywhere: %s" % ", ".join(content["overlay_unused"][:8]))

    # F standing rules
    if content:
        lay = w.layout()
        bad = []
        rowmap = {}
        for _, r in all_rows(content):
            rowmap[r["id"]] = r
        for a in lay["standing"]["abi"]:
            r = rowmap.get(a["key"])
            if r is None:
                bad.append("%s missing" % a["key"])
            elif r["status"] != "paul" and [w.norm(x) for x in r["bullets"]] != [w.norm(a["value"])]:
                bad.append("%s shows %s, not %s" % (a["key"], " ".join(r["bullets"]), a["value"]))
        for blk, labels in lay["standing"]["forbidden_labels"].items():
            for sub, r in all_rows(content):
                if sub.endswith(blk) and r["label"] in labels:
                    bad.append("%s must not have a '%s' line" % (blk, r["label"]))
        add("FAIL" if bad else "PASS", "F", ("standing ABIs wrong: " + "; ".join(bad[:4])) if bad else "the standing ABIs (Dread Disease 3% and the others) are as the rule says, or changed on Paul's word")
        rec = [(rid, t) for sub, r in all_rows(content) for f in r.get("flags", []) if f.get("kind") == "reconcile" for rid, t in [(r["id"], f["text"])]]
        if rec:
            add("WARN", "F", "%d total(s) did not reconcile and are flagged in the report: %s" % (len(rec), "; ".join(x[0] for x in rec[:5])))
        else:
            add("PASS", "F", "every total reconciles to the cent")

    # G pdf
    b = rj.get("build")
    if not b:
        add("FAIL", "G", "the PDF was never built (step 6)")
    else:
        cur = w.content_hash(content) if content else None
        if cur != b.get("content_sha"):
            add("FAIL", "G", "the PDF is older than the report: build it again")
        else:
            f = b.get("font") or {}
            add("PASS" if f.get("aptos") else "WARN", "G", "%s built from the current report (%d page(s), font %s)" % (b["pdf"], b["pages"], ", ".join(f.get("ps_names") or [str(f.get("family"))])))
        lk = rj.get("look") or {}
        add("PASS" if lk.get("build_sha") == b.get("pdf_sha") else "FAIL", "G", "the page images were looked at" if lk.get("build_sha") == b.get("pdf_sha") else "the page images were not looked at for this build")

    # H saved and approved
    sv, ok = rj.get("saved") or {}, rj.get("ok") or {}
    if b and sv.get("build_sha") == b.get("pdf_sha") and sv.get("size") == b.get("pdf_size"):
        add("PASS", "H", "saved into %s; the folder listing shows %d bytes, the same as the built file" % (sv.get("folder"), sv["size"]))
    else:
        add("FAIL", "H", "the PDF is not saved with a matching size listing (step 7)")
    add("PASS" if b and ok.get("build_sha") == b.get("pdf_sha") else "FAIL", "H", "Paul's OK is recorded: \"%s\"" % str(ok.get("said"))[:50] if ok.get("said") and b and ok.get("build_sha") == b.get("pdf_sha")
        else "Paul's OK of this version of the Fact Find is not recorded")

    # I chain
    ch = rj.get("chain") or {}
    if ch.get("summary") and ch.get("planner") and ch.get("sitamah"):
        add("PASS", "I", "Summary %s; Planner note %s; Sitamah message %s" % (str(ch["summary"])[:50], str(ch["planner"])[:40], str(ch["sitamah"])[:50]))
        if str(ch["sitamah"]).lower().startswith("failed"):
            add("WARN", "I", "the message to Sitamah failed: give Paul the text to paste")
    else:
        add("FAIL", "I", "the Summary, the Planner note and the Sitamah message are not all recorded (step 8)")

    # J steps and program
    pend = [s for s in STEP_ORDER if (rj.get("steps", {}).get(s) or {}).get("state") != "done" and not (finishing and s == "chain")]
    add("FAIL" if pend else "PASS", "J", ("steps not done through the driver: %s" % ", ".join(pend)) if pend else "every step was done through the driver, in order")
    fp = rj.get("program_fp")
    if fp and fp != w.program_fingerprint():
        add("FAIL", "J", "the skill's programs or pages changed during this run (they must never be edited in a run)")
    return rows, content, st


def summary_lines(run, content):
    rj = load(run, w.RUN, {})
    g = list((content or {}).get("glance") or [])
    return g


def full_text(rows, content, run):
    out = ["SKILL VERSION: %s" % w.version_line()]
    for gid, name in GROUPS:
        rs = [r for r in rows if r[1] == gid]
        if rs:
            out.append("\n%s. %s" % (gid, name))
            out += ["  [%-4s] %s" % (lvl, m) for lvl, _, m in rs]
    out.append("\nWHAT PAUL SHOULD GLANCE AT:")
    out += ["  - " + x for x in summary_lines(run, content)]
    return "\n".join(out)


def _cut(text, n):
    t = " ".join(str(text).split())
    return t if len(t) <= n else t[:n - 1].rstrip() + "…"


def report_short(run, finishing=False, full=False):
    rows, content, st = run_checks(run, finishing)
    text = full_text(rows, content, run)
    try:
        d = os.path.join(run, "out_record")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "audit-full.txt"), "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    except OSError:
        pass
    if full:
        print(text)
    out = ["AUDIT   %s" % w.version_line()]
    nok = nbad = 0
    for gid, name in GROUPS:
        rs = [r for r in rows if r[1] == gid]
        if not rs:
            continue
        bad = [r for r in rs if r[0] == "FAIL"]
        warn = [r for r in rs if r[0] == "WARN"]
        if bad:
            nbad += 1
            out.append("❌ %s: %s%s" % (name, _cut(bad[0][2], 170), (" (+%d more)" % (len(bad) - 1)) if len(bad) > 1 else ""))
        else:
            nok += 1
            out.append("✅ %s (%d checks)%s" % (name, len([r for r in rs if r[0] == "PASS"]), ("; note: " + _cut(warn[0][2], 120)) if warn else ""))
    out.append("Only attested (not proven): that the call was UNDERSTOOD (the program proves it was handed over twice and that quoted call lines are in it); the Overview and other documents quoted; "
               "that the PDF, the Summary, the Planner note and the Sitamah message really went where recorded (the saved size is compared); Paul's OK; the look at the page images. Full record: out_record/audit-full.txt")
    warns = sum(1 for r in rows if r[0] == "WARN")
    out.append("RESULT: %s   (%d ✅, %d ❌, %d warnings)" % ("PASS" if not nbad else "FAIL", nok, nbad, warns))
    if not nbad and content:
        gl = summary_lines(run, content)
        out.append("")
        out.append("WHAT PAUL SHOULD GLANCE AT (the program counted these; it cannot judge them):")
        out += ["  - " + _cut(x, 230) for x in gl[:6]]
        if len(gl) > 6:
            out.append("  - (%d more in out_record/audit-full.txt)" % (len(gl) - 6))
        rep = content.get("report") or {}
        out.append("DELIVERY LINE: %s; the form and the call combined in ONE report (%d contradictions: %d sorted, %d highlighted); transcript read twice (%d lines)." % (
            w.version_short(), len(rep.get("differences") or []), rep.get("sorted", 0), rep.get("highlighted", 0), (st or {}).get("total_lines", 0)))
    elif nbad:
        out.append("NOT COMPLETE. Say so, and say which line failed; fix every ❌ and run the check again.")
    print("\n".join(out))
    return nbad == 0


def main():
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if not a:
        print(__doc__)
        sys.exit(1)
    ok = report_short(os.path.abspath(a[0]), full="--full" in sys.argv)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
