#!/usr/bin/env python3
"""The one checker of the wr-roa-builder.

  verify.py <run_dir> [pre|final] [--full]

It re-reads the registered documents, re-checks every answer against their text, rebuilds the data the program assembles, reopens the finished
.docx and proves the checks a program can prove. The reply to Paul carries the SHORT AUDIT it prints: one line per check with a green tick or a red
cross, and one closing line for what is only attested (Paul, 03/11/2026). The full record is written to out_record/audit-full.txt.
"""
import datetime as dt
import hashlib
import json
import os
import sys

import docread
import docxcheck
import embedpipe
import roa
import wrlib as w

OK, BAD = "✅", "❌"
STEP_IDS = ["locate", "read", "answers", "confirm", "email", "build", "check", "save", "final"]


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
        src = d.get("same_as")
        rec = docs["docs"].get(src) if src else d
        try:
            ev[role] = docread.Evidence(w.load_json(os.path.join(run, rec["text_file"])))
        except Exception:
            ev[role] = None
    return docs, ev


def run_checks(run, stage):
    R = Results()
    rj = w.load_json(os.path.join(run, w.RUN))
    st = w.load_opt(os.path.join(run, w.STATE), {})
    today = w.parse_date(rj["today"])
    lists, bk = roa.template_lists(), roa.bank()
    docs, ev = load_docs(run)
    a = w.load_opt(os.path.join(run, w.ANSWERS), None)
    bundle = rj.get("bundle") or (a or {}).get("bundle")
    # ---------------------------------------------------------------- the documents
    R.group = "docs"
    log = [e for e in w.load_opt(os.path.join(run, w.ACCESS), []) if e.get("purpose") == "locate"]
    if bundle not in roa.BUNDLES:
        R.add(False, "The bundle is not known yet (it is in the answers)", "step 'answers'")
    else:
        need = roa.REQUIRED_DOCS[bundle]
        absent = [r for r in need if r not in docs["docs"] and not (docs["missing"].get(r) or "").strip()]
        changed = [r for r, d in docs["docs"].items() if not d.get("same_as") and (not os.path.exists(os.path.join(run, d["file"])) or w.sha256_file(os.path.join(run, d["file"])) != d["sha"])]
        bad = route_order_problems(log)
        R.add(not absent and not changed and bool(log) and not bad,
              "The client's documents are registered (%s), unchanged, and the routes were tried in order, each try logged (%d on record)" % (", ".join(sorted(docs["docs"])), len(log))
              if not absent and not changed and log and not bad else
              "Documents problem: missing %s; changed %s; route log %s" % (absent or "none", changed or "none", "out of order" if bad else ("empty" if not log else "fine")),
              "; ".join("%s %s" % (e["route"], e["result"]) for e in log))
        said = [r for r in need if r in docs["missing"]]
        if said:
            R.attested.append("the document(s) Paul said are not available: %s" % ", ".join(said))
    # ---------------------------------------------------------------- reading lock
    R.group = "read"
    if docs["docs"]:
        acked = st.get("read", {}).get("acked", {})
        todo = []
        for role in roa.SERVED_ROLES:
            d = docs["docs"].get(role)
            if d and not d.get("same_as"):
                todo += ["%s:%d" % (role, n) for n in range(1, d["pages"] + 1)]
        miss = [k for k in todo if len((acked.get(k) or "").strip()) < 3]
        R.add(not miss, "Every page of the quotes, application, follow-up notes and emails was served in order and acknowledged (%d of %d)" % (len(todo) - len(miss), len(todo)) if not miss else
              "Pages not yet acknowledged: %s" % ", ".join(miss[:6]))
        image_only = [r for r, d in docs["docs"].items() if d.get("image_only")]
        if image_only:
            R.attested.append("anything on page(s) with no readable text in: %s" % ", ".join(image_only))
    # ---------------------------------------------------------------- the answers
    R.group = "answers"
    ok_a = False
    rs = {}
    if a:
        pr = roa.answers_problems(a, lists, bk, ev, today)
        ok_a = not pr
        R.add(ok_a, "Setup answers valid and sourced (%s ROA for %s, ROA date %s); every dropdown choice is a real option of the template; conflicts: none" %
              (a["bundle"], a["client_name"], a["roa_date"]) if ok_a else "Answers problem: %s" % pr[0], "; ".join(pr))
        if ok_a:
            R.add(True, "Names, ID and every figure entered were found in the documents' own text")
            if any(e is not None and not e.has_text for e in ev.values()):
                R.attested.append("figures in a document with no readable text")
            rs = roa.reasons_for(a, bk)
            extra = roa.not_in_lists(a, lists)
            if extra:
                R.attested.append("entries written as text because they are not in the template's dropdown lists (%s)" % "; ".join(extra))
    else:
        R.add(False, "The setup answers have not been entered yet", "step 'answers'")
    # ---------------------------------------------------------------- Paul's yes
    R.group = "confirm"
    ap = w.load_opt(os.path.join(run, w.APPROVAL), None)
    if ok_a:
        cur = sha_of({"answers": a, "table": roa.table_rows(a, bk)})
        good = bool(ap) and ap.get("sha") == cur and len((ap.get("said") or "").strip()) >= 3 and st.get("shown_sha") == cur
        R.add(good, "Paul was shown the confirmation table and said yes to exactly these answers" if good else
              "No valid yes from Paul for these answers: run.py show, put the table in the reply, then run.py approve with his words")
        if good:
            R.attested.append("Paul's yes (the words are typed by the chat)")
    # ---------------------------------------------------------------- the email pages (Retirement / Investment)
    R.group = "email"
    if ok_a and a["bundle"] != "risk":
        em = st.get("email")
        R.add(bool(em) and os.path.exists(os.path.join(run, w.EMAIL_HTML)) and w.sha256_file(os.path.join(run, w.EMAIL_HTML)) == em["sha"],
              "The email page opens on the client's own reply (%s), shows their acceptance wording, then the quoted proposal" % a["reply_email"]["from"] if em else
              "The combined reply-and-proposal email page is not registered: run.py email --file ...")
    # ---------------------------------------------------------------- the built document
    R.group = "build"
    bd = st.get("build")
    docx_path = os.path.join(run, w.OUT, bd["docx"]) if bd else None
    data = None
    if ok_a and bd and docx_path and os.path.exists(docx_path):
        data = roa.assemble(a, bk)
        R.add(w.sha256_file(docx_path) == bd["sha"] and sha_of(data) == bd["data_sha"], "The ROA is exactly what the program builds from the confirmed answers with the fixed scripts (not edited by hand)")
        if a["bundle"] != "risk":
            emb = bd.get("embed") or {}
            good = (emb.get("command") or [""])[0].startswith("wkhtmltopdf") and "--zoom" not in emb.get("command", []) and emb.get("heading") == embedpipe.HEADING_FOR[a["bundle"]] and emb.get("pages", 0) > 0
            R.add(good, "The email pages were rendered with wkhtmltopdf at the fixed geometry (no --zoom, no LibreOffice), fonts scaled to 15 pt, and embedded before '%s'" % emb.get("heading") if good else
                  "The email embedding was not done as the skill requires (%s)" % (emb or "not done"))
            pdf = os.path.join(run, "embed", "email.pdf")
            if os.path.exists(pdf):
                pages = docread.read_pdf(pdf)["pages"]
                t = pages[0]["text"] if pages else ""
                frm = a["reply_email"]["from"].lower()
                first, second = t.lower().find("from:"), t.lower().find("from:", t.lower().find("from:") + 5)
                acc = w.norm(a["reply_email"]["acceptance_text"]) in w.norm(t)
                opens = first >= 0 and frm in t.lower()[first:first + 160] and acc and (second < 0 or t.lower().find(frm) < second)
                R.add(opens, "The first rendered email page opens on the client's own reply (their address and acceptance wording) before the adviser's proposal header" if opens else
                      "The first rendered email page does NOT open on the client's own reply: the ROA is incomplete and must be rebuilt")
    elif ok_a:
        R.add(False, "The ROA has not been built yet", "step 'build'")
    # ---------------------------------------------------------------- the .docx opened and checked
    R.group = "docx"
    if data and docx_path and os.path.exists(docx_path):
        res = docxcheck.check(docx_path, a, data, rs, lists, bd.get("embed"))
        bad = [r for r in res if not r[0]]
        if not bad:
            R.add(True, "The finished ROA was reopened and passed all %d program checks (one bundle only, no Health Care, fixed sentences, valid dropdowns, reason text word for word, amounts, "
                  "name and ID line, reference number, replacement wording, next review date, author, no placeholder or grey fields%s)" %
                  (len(res), ", embedded email pages in place" if a["bundle"] != "risk" else ""), "; ".join(r[1] for r in res))
        else:
            for ok, short, detail in bad:
                R.add(False, short, detail)
            R.add(True, "%d other program checks on the finished ROA passed" % (len(res) - len(bad)), "; ".join(r[1] for r in res if r[0]))
        R.attested.append("how the pages look to the eye (placeholder grey on screen, the embedded pages' size next to the ROA's text, image borders near the footer)")
    # ---------------------------------------------------------------- the save
    R.group = "save"
    sv = st.get("save")
    rc = w.load_opt(os.path.join(run, w.RECEIPT), {})
    slog = [e for e in w.load_opt(os.path.join(run, w.ACCESS), []) if e.get("purpose") == "save"]
    if data and sv:
        local = os.path.join(run, w.OUT, sv["name"])
        size = os.path.getsize(local) if os.path.exists(local) else -1
        derived = roa.delivery_filename(a)
        R.add(sv["name"] == derived and size == bd["size"], "The file name is derived, not typed: %s" % sv["name"] if sv["name"] == derived else "The saved file name is not the derived name")
        folder = rc.get("save.folder", "")
        good = bool(slog) and not route_order_problems(slog) and folder.rstrip("\\/").lower().endswith("roa & bus roa") and (rc.get("save.listed_bytes") or "").strip() == str(size)
        R.add(good, "Saved in the client's ROA & Bus ROA folder through the routes in order; the listing shows %d bytes, equal to the local file%s" % (size, " (Paul said to overwrite)" if sv.get("overwrite") else "")
              if good else "The save is not proven: record the save tries in order, the folder (ending ROA & Bus ROA) and the listed size (%d bytes)" % size)
        R.add(True, "No existing file was overwritten without Paul's yes" if not sv.get("existing_clash") or sv.get("overwrite") else "A file with this name exists and Paul has not said to overwrite")
        R.attested.append("that the file really sits in the client's folder (the listing is typed by the chat)")
    if stage == "final":
        R.group = "final"
        done = [s for s in STEP_IDS[:-1] if (rj.get("steps", {}).get(s) or {}).get("state") == "done"]
        fpok = rj.get("program_fingerprint") == w.program_fingerprint()
        R.add(done == STEP_IDS[:-1] and fpok, "Every step done in order (%d of %d) and the programs and the template did not change during the run" % (len(done), len(STEP_IDS) - 1) if done == STEP_IDS[:-1] and fpok else
              "Steps done: %s%s" % (", ".join(done) or "none", "; the programs changed during the run" if not fpok else ""))
        R.attested += ["the advice itself, the ROA date's source and that this is the right transaction folder (judgement, recorded with sources)",
                       "that each figure sits in the right column of the quote (it is only proven to appear in the document)"]
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
