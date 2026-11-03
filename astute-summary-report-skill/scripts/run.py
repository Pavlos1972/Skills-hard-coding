#!/usr/bin/env python3
"""The step driver of the astute-summary-report-skill: shows ONE step at a time, refuses to skip, keeps the run on disk.

  run.py start <run> --client "First Surname"
  run.py next | status | preflight
  run.py access <run> --purpose locate|save --route device|m365|zapier --result found|failed [--note TEXT]
  run.py source <run> --file PDF --route ROUTE [--folder-count N --chosen TEXT]
  run.py read <run> [--ack N --note TEXT]          the report's text, one page at a time, each page acknowledged
  run.py data <run> --file data.json               the entered data: validated, then checked against the report's own text
  run.py product <run> --name NAME (--source URL --desc TEXT | --unconfirmed)
  run.py flag <run> (--kind K --text TEXT [--policy N] [--provider P] | --none --note TEXT)
  run.py build <run>                               compose the content and draw the PDF
  run.py name <run> --existing "a.pdf;b.pdf"       the file name to save (never overwriting)
  run.py receipt <run> KEY VALUE
  run.py done <run> STEP                           prove the step, then show the next one

Claude runs these programs as they are and never rewrites them during a run. Nothing here sends anything to anyone.
"""
import argparse
import os
import shutil
import sys

import model
import report
import verify
import wrlib as w

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
RULE = "=" * 78
LATER = {"data": ["products", "flags", "build", "save", "final"], "products": ["build", "save", "final"], "flags": ["build", "save", "final"]}


def p(run, name):
    return os.path.join(run, name)


def steps():
    return w.load_json(os.path.join(w.SKILL_DIR, "steps.json"))["steps"]


def load_run(run):
    path = p(run, w.RUN)
    if not os.path.exists(path):
        w.die('This is not a run folder (no %s). Start one with: python3 %s/run.py start <run folder> --client "First Surname"' % (w.RUN, SCRIPTS), 2)
    return w.load_json(path)


def save_run(run, rj):
    w.save_json(p(run, w.RUN), rj)


def read_ref(name):
    with open(os.path.join(w.SKILL_DIR, "references", name), encoding="utf-8") as f:
        return f.read()


def expand(text, run):
    return text.replace("{scripts}", SCRIPTS).replace("{run}", run)


def current_step(rj):
    for s in steps():
        if rj["steps"].get(s["id"], {}).get("state") != "done":
            return s
    return None


def show_step(run, rj, step):
    plist = steps()
    n = [s["id"] for s in plist].index(step["id"]) + 1
    print(RULE)
    print("STEP %d of %d: %s        [%s]" % (n, len(plist), step["title"], step["id"]))
    print(RULE)
    for line in step["do"]:
        print(expand(line, run))
    for r in step.get("ref", []):
        print("\nRULES FOR THIS STEP (references/%s):\n" % r)
        print(expand(read_ref(r), run))
    print("\nPROOF NEEDED: %s" % step["proof"])
    print("WHEN DONE RUN: python3 %s/run.py done %s %s" % (SCRIPTS, run, step["id"]))
    later = [s["title"] for s in plist[n:]]
    if later:
        print("COMING LATER (titles only): " + " | ".join(later))
    print(RULE)


def preflight():
    rows = []
    for mod in ("pdfplumber", "reportlab"):
        try:
            __import__(mod)
            rows.append((True, "python module %s is available" % mod))
        except ImportError:
            rows.append((False, "python module %s is NOT available (try: pip install %s)" % (mod, mod)))
    rows.append((shutil.which("pdftoppm") is not None, "pdftoppm (page images) is %savailable" % ("" if shutil.which("pdftoppm") else "NOT ")))
    rows.append((w.skill_stamp() is not None, "the skill has a Last updated stamp (%s)" % (w.stamp_display(w.skill_stamp()) or "none")))
    return all(r[0] for r in rows), rows


def _checks(run, *groups):
    R, rj = verify.run_checks(run, "pre")
    out = [r[1] for r in R.rows if r[0] == verify.BAD and r[3] in groups]
    for g in groups:
        if not any(r[3] == g for r in R.rows):
            out.append("the checker has no result yet for '%s'" % g)
    return out


def ck_final(run, rj):
    R, rj2 = verify.run_checks(run, "final")
    if R.fails:
        verify.print_audit(R, rj2, "final", run)
        return ["the checker has %d red cross(es) above" % len(R.fails)]
    return []


CHECKS = {
    "locate_ok": lambda run, rj: _checks(run, "report"),
    "read_ok": lambda run, rj: _checks(run, "report", "read"),
    "data_ok": lambda run, rj: _checks(run, "report", "read", "data"),
    "products_ok": lambda run, rj: _checks(run, "data", "products"),
    "flags_ok": lambda run, rj: _checks(run, "data", "products", "flags"),
    "build_ok": lambda run, rj: _checks(run, "data", "products", "flags", "build"),
    "save_ok": lambda run, rj: _checks(run, "build", "save"),
    "verify_final": ck_final,
}


def reopen(run, after):
    """A correction re-opens every later step (Paul: a correction re-opens the whole task)."""
    rj = load_run(run)
    again = [s for s in LATER[after] if (rj["steps"].get(s) or {}).get("state") == "done"]
    for s in again:
        rj["steps"].pop(s, None)
    save_run(run, rj)
    if again:
        print("LATER STEPS RE-OPENED because this changed: redo %s." % ", ".join(again))


# ------------------------------------------------------------------ commands
def cmd_start(a):
    parts = a.client.split()
    if len(parts) < 2:
        w.die('--client must be the first name and surname, for example --client "Pat Samplecase"')
    if os.path.exists(p(a.run, w.RUN)):
        old = load_run(a.run)
        if w.norm(old["client"]) != w.norm(a.client):
            w.die("REFUSED: this run folder already belongs to %s. Use a NEW run folder." % old["client"], 2)
        print("This run already exists. Showing where it is up to.")
        return cmd_next(a)
    ok, rows = preflight()
    print("SELF-TEST BEFORE ANYTHING ELSE:")
    for good, text in rows:
        print("  [%s] %s" % ("OK" if good else "FAIL", text))
    if not ok:
        w.die("\nSTOP. Tell Paul exactly which item failed above. Do not carry on.", 4)
    os.makedirs(os.path.join(a.run, w.OUT), exist_ok=True)
    rj = {"skill": w.skill_name(), "created": w.now(), "skill_stamp": w.skill_stamp(), "steps": {}, "client": " ".join(parts), "program_fingerprint": w.program_fingerprint()}
    save_run(a.run, rj)
    for name, empty in ((w.ACCESS, []), (w.RECEIPT, {}), (w.STATE, {}), (w.PRODUCTS, {}), (w.FLAGS, {"flags": []})):
        w.save_json(p(a.run, name), empty)
    print("\nSAY THIS TO PAUL FIRST, before anything else in your reply, in exactly these words:\n    %s.\n" % w.version_line())
    print("RUN STARTED  client: %s\n" % rj["client"])
    print("Standing rules for the whole job:\n")
    print(expand(read_ref("00-rules.md"), a.run))
    print()
    show_step(a.run, rj, current_step(rj))


def cmd_next(a):
    rj = load_run(a.run)
    s = current_step(rj)
    if s is None:
        print("Every step is done. Run: python3 %s/verify.py %s  and put its SHORT AUDIT in your reply." % (SCRIPTS, a.run))
        return
    show_step(a.run, rj, s)


def cmd_status(a):
    rj = load_run(a.run)
    for s in steps():
        print("  [%s] %s" % ("done" if rj["steps"].get(s["id"], {}).get("state") == "done" else "    ", s["title"]))
    cur = current_step(rj)
    print("Now: %s" % (cur["id"] if cur else "all done"))


def cmd_preflight(a):
    ok, rows = preflight()
    for good, text in rows:
        print("  [%s] %s" % ("OK" if good else "FAIL", text))
    print("PREFLIGHT: %s" % ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 4)


def guard(rj):
    if rj.get("program_fingerprint") and rj["program_fingerprint"] != w.program_fingerprint():
        w.die("REFUSED: the skill's programs, steps or rule pages changed while this run was in progress. The programs are run as they are. Start again in a new run folder.", 3)


def cmd_done(a):
    rj = load_run(a.run)
    guard(rj)
    ids = [s["id"] for s in steps()]
    if a.step not in ids:
        w.die("'%s' is not a step. Steps: %s" % (a.step, ", ".join(ids)))
    cur = current_step(rj)
    if cur is None or ids.index(a.step) > ids.index(cur["id"]):
        w.die("REFUSED: finish step '%s' first. Steps are done in order, none skipped." % (cur["id"] if cur else "?"), 3)
    step = steps()[ids.index(a.step)]
    fails = CHECKS[step["check"]](a.run, rj)
    if fails:
        print("NOT DONE: step '%s' is missing its proof:" % a.step)
        for f in fails:
            print("  - " + f)
        sys.exit(3)
    rj["steps"][a.step] = {"state": "done", "t": w.now()}
    save_run(a.run, rj)
    print("STEP '%s' DONE.\n" % a.step)
    nxt = current_step(rj)
    if nxt is None:
        print("EVERY STEP IS DONE.\nPut this in your reply, as it is: first the numbered flag list, then the SHORT AUDIT (nothing longer):\n")
        print("FLAGS TO VERIFY (most important first):")
        fl = verify.flag_list(a.run)
        print("\n".join(fl) if fl else "None.")
        print()
        R, rj2 = verify.run_checks(a.run, "final")
        verify.print_audit(R, rj2, "final", a.run)
        return
    show_step(a.run, rj, nxt)


def cmd_access(a):
    rj = load_run(a.run)
    guard(rj)
    log = w.load_opt(p(a.run, w.ACCESS), [])
    log.append({"purpose": a.purpose, "route": a.route, "result": a.result, "note": a.note or "", "t": w.now()})
    w.save_json(p(a.run, w.ACCESS), log)
    print("access try recorded: %s %s %s (%d on record)" % (a.purpose, a.route, a.result, len(log)))


def cmd_source(a):
    rj = load_run(a.run)
    guard(rj)
    if not os.path.isfile(a.file):
        w.die("MISSING: %s" % a.file)
    log = [e for e in w.load_opt(p(a.run, w.ACCESS), []) if e.get("purpose") == "locate"]
    if not any(e["route"] == a.route and e["result"] == "found" for e in log):
        w.die("REFUSED: record the access try first: run.py access %s --purpose locate --route %s --result found" % (a.run, a.route))
    bad = verify.route_order_problems(log)
    if bad:
        w.die("REFUSED: the routes are tried in order (computer, Microsoft 365, Zapier); %s was used before the earlier ones failed." % ", ".join(bad))
    if (a.folder_count or 1) > 1 and len((a.chosen or "").strip()) < 8:
        w.die("REFUSED: the 5. Astute folder holds %d reports: say which one you used and why (--chosen), normally the most recent by report date." % a.folder_count)
    shutil.copyfile(a.file, p(a.run, w.REPORT_PDF))
    try:
        rep = report.read_pdf(p(a.run, w.REPORT_PDF))
    except Exception as e:
        os.remove(p(a.run, w.REPORT_PDF))
        print("STOP. This file cannot be used: %s" % e)
        sys.exit(5)
    w.save_json(p(a.run, w.REPORT_TEXT), rep)
    rj["source"] = {"route": a.route, "name": os.path.basename(a.file), "size": os.path.getsize(a.file), "sha256": w.sha256_file(p(a.run, w.REPORT_PDF)),
                    "pages": rep["page_count"], "image_only": rep["image_only"], "chosen": a.chosen or ""}
    save_run(a.run, rj)
    print("Astute report brought into the run folder: %s (%d bytes, %d page(s)) via %s" % (rj["source"]["name"], rj["source"]["size"], rep["page_count"], a.route))
    if rep["image_only"]:
        print("NOTE: page(s) %s have no readable text (scanned images). You must view them as images yourself; figures on them cannot be checked by the program." % ", ".join(map(str, rep["image_only"])))


def cmd_read(a):
    rj = load_run(a.run)
    guard(rj)
    if not os.path.exists(p(a.run, w.REPORT_TEXT)):
        w.die("The report is not in the run folder yet: run.py source first.")
    rep = w.load_json(p(a.run, w.REPORT_TEXT))
    st = w.load_opt(p(a.run, w.STATE), {})
    acked = st.setdefault("read", {}).setdefault("acked", {})
    n_total = rep["page_count"]
    nxt = next((n for n in range(1, n_total + 1) if str(n) not in acked), None)
    if a.ack is not None:
        if a.ack != nxt:
            w.die("REFUSED: pages are acknowledged in order. The next page is %s." % (nxt or "none (all done)"))
        if len((a.note or "").strip()) < 3:
            w.die('REFUSED: acknowledge the page with a one-line note of what is on it: --note "..."')
        acked[str(a.ack)] = a.note.strip()
        w.save_json(p(a.run, w.STATE), st)
        print("page %d acknowledged (%d of %d)" % (a.ack, len(acked), n_total))
        nxt = next((n for n in range(1, n_total + 1) if str(n) not in acked), None)
    if nxt is None:
        print("All %d pages were read and acknowledged. Now run: python3 %s/run.py done %s read" % (n_total, SCRIPTS, a.run))
        return
    pg = rep["pages"][nxt - 1]
    print("-" * 30 + " PAGE %d of %d " % (nxt, n_total) + "-" * 30)
    if nxt in rep["image_only"]:
        print("THIS PAGE HAS NO READABLE TEXT. View it as an image yourself (for example: pdftoppm -f %d -l %d -png -r 80 %s page), then acknowledge it." % (nxt, nxt, p(a.run, w.REPORT_PDF)))
    else:
        print(pg["text"])
    print("-" * 78)
    print('Read it fully, then: python3 %s/run.py read %s --ack %d --note "one line on what is on this page"' % (SCRIPTS, a.run, nxt))


def _hash(path):
    return w.sha256_file(path) if os.path.exists(path) else None


def cmd_data(a):
    rj = load_run(a.run)
    guard(rj)
    if not os.path.exists(p(a.run, w.REPORT_TEXT)):
        w.die("The report is not in the run folder yet: run.py source first.")
    data = w.load_json(a.file, "the data file")
    probs = model.schema_problems(data)
    if not probs and w.norm((data.get("header") or {}).get("client_name", "")) != w.norm(rj["client"]):
        probs.append("header.client_name %r is not the client Paul named (%s)" % (data["header"].get("client_name"), rj["client"]))
    if probs:
        print("REFUSED (nothing saved):\n  - " + "\n  - ".join(probs))
        sys.exit(5)
    before = _hash(p(a.run, w.DATA))
    w.save_json(p(a.run, w.DATA), data)
    if before and before != _hash(p(a.run, w.DATA)):
        reopen(a.run, "data")
    rep = w.load_json(p(a.run, w.REPORT_TEXT))
    ep = report.evidence_problems(data, rep)
    print("data saved: %d provider(s), %d policy(ies)" % (len(data["providers"]), len(data["policies"])))
    if ep is None:
        print("The report has no readable text, so nothing could be checked against it. This stays attested.")
    elif ep:
        print("NOT FOUND IN THE REPORT'S TEXT (fix the data file and run data again):\n  - " + "\n  - ".join(ep))
        sys.exit(3)
    else:
        print("Every policy number, figure, date and name entered was found in the report's own text.")
    names = model.product_names(data)
    print("Distinct products to check online next (one search each): %s" % "; ".join(names))


def cmd_product(a):
    rj = load_run(a.run)
    guard(rj)
    data = w.load_opt(p(a.run, w.DATA), None)
    if not data:
        w.die("Enter the data first (run.py data).")
    names = {w.norm(n): n for n in model.product_names(data)}
    if w.norm(a.name) not in names:
        w.die("REFUSED: %r is not a product in the data. Products: %s" % (a.name, "; ".join(names.values())))
    prods = w.load_opt(p(a.run, w.PRODUCTS), {})
    if a.unconfirmed:
        rec = {"state": "unconfirmed"}
    else:
        if not a.source or not a.desc:
            w.die("REFUSED: give --source (the web address) and --desc (the description), or --unconfirmed.")
        if not a.source.startswith(("http://", "https://")) or len(a.desc.split()) > model.MAX_DESC_WORDS:
            w.die("REFUSED: the source must be a web address and the description at most %d words." % model.MAX_DESC_WORDS)
        rec = {"state": "described", "source": a.source, "desc": a.desc.strip()}
    if prods.get(w.norm(a.name)) != rec:
        prods[w.norm(a.name)] = rec
        w.save_json(p(a.run, w.PRODUCTS), prods)
        reopen(a.run, "products")
    left = [n for k, n in names.items() if k not in prods]
    print("product recorded: %s (%s). Still to do: %s" % (a.name, rec["state"], "; ".join(left) or "none"))


def cmd_flag(a):
    rj = load_run(a.run)
    guard(rj)
    data = w.load_opt(p(a.run, w.DATA), None)
    if not data:
        w.die("Enter the data first (run.py data).")
    st = w.load_opt(p(a.run, w.STATE), {})
    fl = w.load_opt(p(a.run, w.FLAGS), {"flags": []})
    if a.none:
        if len((a.note or "").strip()) < 8:
            w.die('REFUSED: say why no further judgement flag applies: --none --note "..."')
        st["flags_none"] = a.note.strip()
        w.save_json(p(a.run, w.STATE), st)
        print("recorded: no judgement flags needed (%s)" % a.note.strip())
        return
    f = {"kind": a.kind, "text": (a.text or "").strip(), "policy": (a.policy or "").strip(), "provider": ""}
    pols = {w.norm(x["policy_number"]): x["provider"] for x in data["policies"]}
    if f["policy"]:
        f["provider"] = pols.get(w.norm(f["policy"]), "")
    elif a.provider:
        f["provider"] = a.provider
    probs = model.flag_problems(data, [f])
    if probs:
        w.die("REFUSED: " + "; ".join(probs))
    fl["flags"].append(f)
    w.save_json(p(a.run, w.FLAGS), fl)
    reopen(a.run, "flags")
    print("flag recorded (%d judgement flag(s))" % len(fl["flags"]))


def cmd_build(a):
    import build
    rj = load_run(a.run)
    guard(rj)
    if not build.build_run(a.run):
        sys.exit(1)


def cmd_name(a):
    rj = load_run(a.run)
    guard(rj)
    st = w.load_opt(p(a.run, w.STATE), {})
    b = st.get("build")
    content = w.load_opt(p(a.run, w.CONTENT), None)
    if not b or not content:
        w.die("The PDF has not been built yet (run.py build).")
    existing = [x.strip() for x in (a.existing or "").split(";") if x.strip()]
    name = w.unique_name(content["file_name"], existing)
    src = p(a.run, os.path.join(w.OUT, b["pdf"]))
    dst = p(a.run, os.path.join(w.OUT, name))
    if dst != src:
        shutil.copyfile(src, dst)
    st["save"] = {"name": name, "existing": existing}
    w.save_json(p(a.run, w.STATE), st)
    print("SAVE THIS FILE: %s" % dst)
    print("Name to use in the client's 5. Astute folder: %s%s" % (name, "   (a file with the derived name already exists, so this one is numbered; tell Paul)" if name != content["file_name"] else ""))
    print("Then record: run.py access ... --purpose save, and run.py receipt save.folder <the folder> / save.listed_bytes <the size the folder listing shows> (%d bytes)" % os.path.getsize(dst))


def cmd_receipt(a):
    rj = load_run(a.run)
    guard(rj)
    rc = w.load_opt(p(a.run, w.RECEIPT), {})
    rc[a.key] = a.value
    w.save_json(p(a.run, w.RECEIPT), rc)
    print("receipt recorded: %s = %s" % (a.key, a.value))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    x = sub.add_parser("start")
    x.add_argument("run")
    x.add_argument("--client", required=True)
    x.set_defaults(fn=cmd_start)
    x = sub.add_parser("preflight")
    x.set_defaults(fn=cmd_preflight)
    for name, fn in (("next", cmd_next), ("status", cmd_status), ("build", cmd_build)):
        x = sub.add_parser(name)
        x.add_argument("run")
        x.set_defaults(fn=fn)
    x = sub.add_parser("done")
    x.add_argument("run")
    x.add_argument("step")
    x.set_defaults(fn=cmd_done)
    x = sub.add_parser("access")
    x.add_argument("run")
    x.add_argument("--purpose", required=True, choices=("locate", "save"))
    x.add_argument("--route", required=True, choices=w.ROUTES)
    x.add_argument("--result", required=True, choices=("found", "failed"))
    x.add_argument("--note")
    x.set_defaults(fn=cmd_access)
    x = sub.add_parser("source")
    x.add_argument("run")
    x.add_argument("--file", required=True)
    x.add_argument("--route", required=True, choices=w.ROUTES)
    x.add_argument("--folder-count", dest="folder_count", type=int)
    x.add_argument("--chosen")
    x.set_defaults(fn=cmd_source)
    x = sub.add_parser("read")
    x.add_argument("run")
    x.add_argument("--ack", type=int)
    x.add_argument("--note")
    x.set_defaults(fn=cmd_read)
    x = sub.add_parser("data")
    x.add_argument("run")
    x.add_argument("--file", required=True)
    x.set_defaults(fn=cmd_data)
    x = sub.add_parser("product")
    x.add_argument("run")
    x.add_argument("--name", required=True)
    x.add_argument("--source")
    x.add_argument("--desc")
    x.add_argument("--unconfirmed", action="store_true")
    x.set_defaults(fn=cmd_product)
    x = sub.add_parser("flag")
    x.add_argument("run")
    x.add_argument("--kind", choices=model.CHAT_FLAG_KINDS)
    x.add_argument("--text")
    x.add_argument("--policy")
    x.add_argument("--provider")
    x.add_argument("--none", action="store_true")
    x.add_argument("--note")
    x.set_defaults(fn=cmd_flag)
    x = sub.add_parser("name")
    x.add_argument("run")
    x.add_argument("--existing", default="")
    x.set_defaults(fn=cmd_name)
    x = sub.add_parser("receipt")
    x.add_argument("run")
    x.add_argument("key")
    x.add_argument("value")
    x.set_defaults(fn=cmd_receipt)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
