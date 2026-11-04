#!/usr/bin/env python3
"""The one checker of the complete-applications-skill.

  verify.py <run_dir> [pre|final] [--full]

It REBUILDS every value, name and table from the run folder, re-reads the filled PDFs field by field and draws them again, so nothing is taken on trust
from a file Claude could have edited. The reply to Paul carries the SHORT AUDIT it prints: one line per check with a green tick or a red cross, and one
closing line for what is only attested (Paul, 03/11/2026). The full record is written to out_record/audit-full.txt (--full prints it).
"""
import os
import sys

import apps as A
import engine as eng
import wrlib as w

OK, BAD = "✅", "❌"
STEP_IDS = ["locate", "plan", "confirm", "fill", "save", "final"]


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
    st = w.load_opt(os.path.join(run, w.STATE), {})
    rc = w.load_opt(os.path.join(run, w.RECEIPT), {})
    log = w.load_opt(os.path.join(run, w.ACCESS), [])
    c = eng.compute(run)
    mode = rj["mode"]
    # ---------------------------------------------------------------- locate
    R.group = "locate"
    docs = c.get("docs") or w.load_opt(os.path.join(run, w.DOCS), {"docs": {}, "currents": {}})
    bad = eng.route_order_problems(log)
    dbad = []
    for role, d in docs["docs"].items():
        path = os.path.join(run, d["file"])
        if not os.path.exists(path) or w.sha256_file(path) != d["sha"]:
            dbad.append(role + " (file changed)")
        elif not any(e["route"] == d["route"] and e["result"] == "found" and e.get("purpose") == "docs" for e in log):
            dbad.append(role + " (no access try logged)")
    for cid, d in docs["currents"].items():
        path = os.path.join(run, d["file"])
        if not os.path.exists(path) or w.sha256_file(path) != d["sha"]:
            dbad.append("current " + cid + " (file changed)")
        elif A.detect_form(path) != d["form"] or A.drift_problems(d["form"], path):
            dbad.append("current " + cid + " (not the known form)")
    okl = bool(log) and not bad and not dbad and (mode == "prefill" or bool(docs["currents"]))
    R.add(okl, "%d access tries logged in route order; documents: %s%s; each found through a logged route and unchanged" % (
        len(log), ", ".join(sorted(docs["docs"])) or "none", ("; current applications: " + ", ".join(sorted(docs["currents"]))) if mode == "correct" else "") if okl else
        ("The routes were not tried in order: %s" % ", ".join(bad)) if bad else ("Document problem: %s" % ", ".join(dbad)) if dbad else
        "No access try is logged" if not log else "A correction needs the current applications registered (run.py current)")
    fd = []
    for f in A.FORMS:
        fd += ["%s: %s" % (A.FORM_NAMES[f], x) for x in A.drift_problems(f)]
    R.add(not fd, "Both blank forms are the ones this skill knows (checksum, every field, type and dropdown option)" if not fd else "Form problem: %s" % fd[0], "; ".join(fd))
    # ---------------------------------------------------------------- plan
    R.group = "plan"
    if c["plan"] is None:
        R.add(False, "The plan has not been entered yet", "step 'plan': run.py plan")
    else:
        pr = c["problems"]
        n_doc = n_pa = n_prog = n_carry = 0
        for a in c["apps"]:
            for n, s in a["sources"].items():
                if s.startswith("program"):
                    n_prog += 1
                elif s.startswith("Paul:"):
                    n_pa += 1
                elif s.startswith("carried"):
                    n_carry += 1
                else:
                    n_doc += 1
        R.add(not pr, "%d application(s) pass every rule; %d value(s) proved by a verbatim document line, %d by Paul's words%s, %d built by the program (N/A rules, replacement, signature date)" % (
            len(c["apps"]), n_doc, n_pa, ", %d carried from a current application" % n_carry if n_carry else "", n_prog) if not pr else "Plan problem: %s" % A.mask_text(pr[0]), "; ".join(A.mask_text(x) for x in pr))
        if n_pa:
            R.attested.append("%d value(s) rest on Paul's own words typed by the chat" % n_pa)
        if mode == "prefill" and not pr:
            R.add(all(a["file_name"] and a["folder_name"] for a in c["apps"]), "The file names and transaction folder names are built by the program from fixed lists (%s)" % "; ".join(a["file_name"] for a in c["apps"]))
        if c["flags"] and not pr:
            R.add(True, "%d flag(s) were raised and shown to Paul (not refusals): %s" % (len(c["flags"]), "; ".join(c["flags"][:2])))
    # ---------------------------------------------------------------- confirm
    R.group = "confirm"
    ap = w.load_opt(os.path.join(run, w.APPROVAL), None)
    cur = eng.confirm_sha(c) if c["plan"] is not None and not c["problems"] else None
    okap = bool(ap) and cur is not None and ap.get("sha") == cur and len((ap.get("said") or "").strip()) >= 3 and st.get("shown_sha") == cur
    R.add(okap, "Paul's yes is recorded for exactly this version, after he was shown the table (field, old to new, source, names, overwrite and rename)" if okap else "No valid yes from Paul for this version: show it, then approve with his exact words")
    # ---------------------------------------------------------------- fill
    R.group = "fill"
    fills = st.get("fill") or {}
    fbad, rbad, cbad, pbad = [], [], [], []
    for a in (c["apps"] if okap else []):
        path = os.path.join(run, w.OUT, a["file_name"])
        if not os.path.exists(path) or not fills.get(a["id"], {}).get("ok") or w.sha256_file(path) != fills[a["id"]].get("sha"):
            fbad.append(a["id"])
            continue
        if A.detect_form(path) != a["form"] or A.drift_problems(a["form"], path):
            fbad.append(a["id"] + " (not the form)")
        rb = A.readback_problems(a["form"], path, a["values"])
        if rb:
            rbad.append("%s: %s" % (a["id"], rb[0]))
        names = [n for n, v in a["values"].items() if (v or "").strip()] if mode == "prefill" else [n for n, _o, _n, _s in a["changes"]]
        miss = A.render_proof(path, a["base"], names)
        if miss:
            pbad.append("%s: %s" % (a["id"], ", ".join(A.label(a["form"], n) for n in miss[:3])))
        if mode == "correct":
            after = A.read_values(path)
            changed = {n for n, _o, _n, _s in a["changes"]}
            odd = [n for n in after if (after[n] or "") != (a["old"].get(n) or "") and n not in changed]
            sig = [n for n in A.fspec(a["form"])["never"] if (after.get(A.key_to_field(a["form"], n) or n) or "") != (a["old"].get(A.key_to_field(a["form"], n) or n) or "")]
            if odd or sig:
                cbad.append("%s: %s" % (a["id"], ", ".join(odd + sig)))
    nfields = sum(len(A.fspec(a["form"])["fields"]) for a in c["apps"])
    R.add(okap and not fbad and not rbad, "%d PDF(s) are fills of the real %s; EVERY field (%d) of each saved PDF reads back exactly as intended, nothing else written" % (
        len(c["apps"]), "blank form" if mode == "prefill" else "current application", nfields) if okap and not fbad and not rbad else
        "Fill problem: %s" % ((fbad + rbad + ["no valid yes"])[0]), "; ".join(fbad + rbad))
    R.add(okap and not pbad, "Every filled box shows something in the render (pixels compared with the %s); the program does not read the text it draws" % ("blank form" if mode == "prefill" else "application before the correction") if okap and not pbad else
          "Nothing drawn in: %s" % (pbad[0] if pbad else "no valid yes"), "; ".join(pbad))
    if mode == "correct":
        R.add(okap and not cbad, "Only the planned fields changed in each application; the signature fields are untouched" if okap and not cbad else "Unplanned change: %s" % (cbad[0] if cbad else "no valid yes"))
    # ---------------------------------------------------------------- save
    R.group = "save"
    sv = st.get("save") or {}
    sbad, nosize = [], []
    for a in (c["apps"] if okap else []):
        s = sv.get(a["id"]) or {}
        ok = bool(s.get("ok")) and (rc.get("save.%s.folder" % a["id"]) or "").strip() and (rc.get("chat.%s.sent" % a["id"]) or "").strip()
        if mode == "correct":
            ok = ok and (rc.get("stage.%s.mtime" % a["id"]) or "").strip() and rc.get("stage.%s.mtime" % a["id"]) == rc.get("commit.%s.expected_mtime" % a["id"])
        if not ok:
            sbad.append(a["id"])
        elif not s.get("sized"):
            nosize.append(a["id"])
    R.add(okap and not sbad, "%d file(s) sent in the chat and saved into the client's Applications folder; the listing shows each name%s" % (
        len(c["apps"]), " (and its size)" if not nosize else " (size not shown for %s: attested)" % ", ".join(nosize)) + ("; staged fresh and committed with the same expectedMtimeMs" if mode == "correct" else "") if okap and not sbad else
        "Not saved or not checked: %s" % (", ".join(sbad) or "no valid yes"))
    ren = [a for a in c["apps"] if a["rename"]]
    if ren and okap:
        rbd = [a["id"] for a in ren if not (st.get("rename") or {}).get(a["id"], {}).get("ok")]
        R.add(not rbd, "%d transaction folder(s) renamed with mv -n after Paul's yes; the listing shows the new name and no copy" % len(ren) if not rbd else "Rename not done or not checked: %s" % ", ".join(rbd))
    if stage == "final":
        R.group = "final"
        done = [s for s in STEP_IDS[:-1] if (rj.get("steps", {}).get(s) or {}).get("state") == "done"]
        fpok = rj.get("program_fingerprint") == w.program_fingerprint()
        R.add(done == STEP_IDS[:-1] and fpok, "Every step done in order (%d of %d) and the programs did not change during the run" % (len(done), len(STEP_IDS) - 1) if done == STEP_IDS[:-1] and fpok else
              "Steps done: %s%s" % (", ".join(done) or "none", "; the programs changed during the run" if not fpok else ""))
        R.attested += ["that each client value is TRUE (the program proves it is in a document or Paul's words, and that it was written)", "Paul's yes (the words are typed by the chat)",
                       "that the chat really saved, renamed and sent through the routes (the program checks the listing and the receipts)", "that the text in each box is the right text in Paul's own viewer"]
        if any(a["form"] == "general" for a in c["apps"]):
            R.attested.append("that the General form's field meanings (a table made once by hand from positions) are right")
    return R, rj


def print_audit(R, rj, stage, run, full=False):
    lines = ["AUDIT   %s" % w.version_line()]
    for mark, short, detail, _g in R.rows:
        lines.append("%s %s" % (mark, A.mask_text(short)))
    if R.attested:
        lines.append("Only attested (not proven): " + "; ".join(dict.fromkeys(R.attested)) + ".")
    ok = len([r for r in R.rows if r[0] == OK])
    bad = len(R.fails)
    lines.append("RESULT: %s   (%d %s, %d %s)" % ("PASS" if not bad else "FAIL", ok, OK, bad, BAD))
    text = "\n".join(lines)
    print(text)
    fulltext = text + "\n\nFULL RECORD\n" + "\n".join("%s %s\n    %s" % (m, s, A.mask_text(d)) for m, s, d, _g in R.rows if d)
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
