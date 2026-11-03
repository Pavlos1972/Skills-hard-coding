#!/usr/bin/env python3
"""The one checker of the fact-find-summary skill.

  verify.py <run_dir> [--stage pre|final] [--full]

It re-reads the Fact Find PDF itself, recomposes the Summary from it and compares, so nothing is taken on trust from a file Claude could have
edited. The reply to Paul carries the SHORT AUDIT it prints: one line per check, a green tick or a red cross, and ONE closing line for what is
only attested (Paul, 03/11/2026). The full record (every detail) is written to out/audit-full.txt and printed with --full.
"""
import glob
import os
import re
import sys
from decimal import Decimal

import compose as cp
import ffread
import wrlib as w

OK, BAD = "✅", "❌"
STEP_IDS = ["locate", "read", "compose", "build", "check", "deliver", "final"]


class Results:
    def __init__(self):
        self.rows, self.attested = [], []

    def add(self, ok, short, detail=""):
        self.rows.append((OK if ok else BAD, short, detail))

    @property
    def fails(self):
        return [r for r in self.rows if r[0] == BAD]


def pdf_pages(pdf):
    """Text of every page, or None when the file cannot be read."""
    try:
        import pdfplumber
        with pdfplumber.open(pdf) as p:
            return [(pg.extract_text() or "") for pg in p.pages]
    except Exception:
        return None


def pdf_size_pt(pdf):
    import pdfplumber
    with pdfplumber.open(pdf) as p:
        return float(p.pages[0].width), float(p.pages[0].height)


def _run(run):
    return w.load_json(os.path.join(run, w.RUN)), w.load_opt(os.path.join(run, w.STATE), {})


def _same_rows(a, b):
    return a["values"] == b["values"] and a["flags"] == b["flags"]


def run_checks(run, stage):
    R = Results()
    rj, st = _run(run)
    client = rj["client"]
    # ------------------------------------------------------------- A. the Fact Find PDF, read by the program
    pdf = os.path.join(run, w.FACTFIND_PDF)
    ffd, content = None, None
    if not os.path.exists(pdf):
        R.add(False, "The Fact Find Transcript PDF is not in the run folder", "step 'locate' copies it with run.py source")
        return R, st, None
    try:
        ffd = ffread.read_pdf(pdf)
    except Exception as e:
        R.add(False, "The Fact Find PDF could not be read by the program", str(e))
        return R, st, None
    probs = ffread.layout_problems(ffd)
    R.add(not probs, "Fact Find Transcript PDF read by program (%d sections, %d rows, %d flags)" % (ffd["stats"]["sections"], ffd["stats"]["rows"], ffd["stats"]["flags"])
          if not probs else "The PDF is not the program-drawn Fact Find Transcript: " + "; ".join(probs)[:150], "; ".join(probs))
    ok = w.norm("%s %s" % (client["first"], client["surname"])) == w.norm(ffd.get("client_name") or "") and ffd.get("meeting_date") == rj["date"]
    R.add(ok, "Client and meeting date match your request (%s %s, %s)" % (client["first"], client["surname"], rj["date"]) if ok else
          "The PDF is for %r, %s but you asked for %s %s, %s" % (ffd.get("client_name"), ffd.get("meeting_date"), client["first"], client["surname"], rj["date"]))
    saved = os.path.join(run, w.FACTFIND)
    R.add(os.path.exists(saved) and w.load_json(saved) == ffd, "fact_find.json is exactly what the program reads from the PDF (not edited by hand)")
    # ------------------------------------------------------------- B. access routes and the source file
    log = w.load_opt(os.path.join(run, w.ACCESS), [])
    src = rj.get("source") or {}
    order_ok, why = True, ""
    seen_fail = set()
    for e in log:
        i = w.ROUTES.index(e["route"]) if e.get("route") in w.ROUTES else -1
        if i < 0 or any(r not in seen_fail for r in w.ROUTES[:i]):
            order_ok, why = False, "route %r was used before the earlier routes were tried and failed" % e.get("route")
        if e.get("result") == "failed":
            seen_fail.add(e["route"])
    found = [e for e in log if e.get("result") == "found"]
    R.add(bool(log) and order_ok and bool(found) and src.get("route") == found[-1]["route"],
          "Access routes tried in order and logged (%s)" % (", ".join("%s %s" % (e["route"], e["result"]) for e in log) or "none"), why or "access log: " + str(log))
    R.add(bool(src) and os.path.getsize(pdf) == src.get("size") and w.sha256_file(pdf) == src.get("sha256"), "The PDF in the run folder is the file that was found (size and fingerprint equal)")
    # ------------------------------------------------------------- C. the Summary content
    cpath = os.path.join(run, w.CONTENT)
    if os.path.exists(cpath):
        content = w.load_json(cpath)
        exp = cp.compose(ffd, {"client": client, "date": rj["date"], "joint": rj.get("joint")})
        R.add(content == exp, "content.json is exactly what the program composes from the Fact Find (not edited by hand)",
              "" if content == exp else "content.json differs from the recomposed content")
        content = exp                                           # everything below is checked on the recomposed content
        _content_checks(R, ffd, content, rj)
    else:
        R.add(False, "The Summary content has not been composed yet", "step 'compose'")
    # ------------------------------------------------------------- D. the PDF and the hand-over
    if content is not None and (stage == "final" or st.get("build")):
        _pdf_checks(R, run, st, content)
    if stage == "final":
        _final_checks(R, run, rj, st, content)
    return R, st, content


def _content_checks(R, ffd, c, rj):
    ff = cp.FF(ffd)
    # every Summary value equals its Fact Find value
    n, wrong = 0, []
    for s in c["sections"]:
        for b in s["blocks"]:
            for r in b["rows"]:
                if r.get("computed") or r.get("item"):
                    continue
                n += 1
                sr = r["src"]
                if len(sr) == 1:
                    f = ff.row(sr[0]["sec"], sr[0]["sub"], sr[0]["label"])
                    if f is None or not _same_rows(f, r):
                        wrong.append("%d. %s / %s" % (s["num"], b["sub"], r["label"]))
                else:
                    parts = [ff.row(x["sec"], x["sub"], x["label"]) for x in sr]
                    if any(p is None for p in parts) or " ".join(" ".join(p["values"]) for p in parts) != " ".join(r["values"]):
                        wrong.append("%d. %s / %s" % (s["num"], b["sub"], r["label"]))
    R.add(not wrong, "Every Summary value equals its Fact Find value (%d values traced)" % n if not wrong else "%d Summary value(s) differ from the Fact Find: %s" % (len(wrong), ", ".join(wrong[:3])), "; ".join(wrong))
    # totals: recomputed to the cent from the item rows
    t = c["totals"]
    def dd(x):
        return Decimal(x)
    for sec, sub_t, items in ((7, "Totals", (("Total monthly repayments", "debts_monthly"), ("Total liabilities (balances)", "debts_balances"), ("Total asset value", "debts_assets"))),
                               (8, "Totals", (("Total childcare (monthly)", "kids_monthly"),))):
        name = "Debt" if sec == 7 else "Childcare"
        bad = []
        for lab, key in items:
            fr = ff.row(sec, sub_t, lab)
            fv = w.parse_money(" ".join(fr["values"])) if fr and fr["values"] else None
            if fv is None or fv != dd(t[key]):
                if not (fr and fr["flags"]):                       # a difference the Fact Find already flagged is carried, not hidden
                    bad.append("%s: Fact Find %s, recomputed %s" % (lab, w.fmt_money(fv) if fv is not None else "(none)", w.fmt_money(dd(t[key]))))
        R.add(not bad, "%s totals recomputed to the cent from the items and equal the Fact Find's" % name if not bad else "%s total differs: %s" % (name, bad[0]), "; ".join(bad))
    # Section 8 against Sections 4 and 5
    def money(sub, lab):
        r = ff.row(11, sub, lab)
        return w.parse_money(" ".join(r["values"])) if r and r["values"] else None
    cc, dr, hh, need = (money("Life cover: fractured cover", l) for l in ("Childcare (monthly)", "Debt repayments (monthly)", "Total household income needed", "Total needed"))
    msgs = []
    if cc is not None and cc != dd(t["kids_monthly"]):
        msgs.append("childcare in Section 8 is %s but the children add up to %s" % (w.fmt_money(cc), w.fmt_money(dd(t["kids_monthly"]))))
    if dr is not None and dr != dd(t["debts_monthly"]):
        msgs.append("debt repayments in Section 8 are %s but ALL the debts add up to %s (debt is never left out)" % (w.fmt_money(dr), w.fmt_money(dd(t["debts_monthly"]))))
    if None not in (hh, cc, dr, need) and hh + cc + dr != need:
        msgs.append("total needed %s is not %s + %s + %s" % (w.fmt_money(need), w.fmt_money(hh), w.fmt_money(cc), w.fmt_money(dr)))
    flagged = any(r["flags"] for r in (ff.block(11, "Life cover: fractured cover") or {"rows": []})["rows"] if r["label"] in ("Childcare (monthly)", "Debt repayments (monthly)", "Total household income needed", "Total needed"))
    R.add(not msgs or flagged, "Section 8 childcare and debt repayments equal Sections 5 and 4; total needed adds up" if not msgs else "Section 8 does not agree with Sections 4 and 5: " + msgs[0] +
          (" (flagged in the Fact Find, carried)" if flagged else ""), "; ".join(msgs))
    # standing ABIs
    bad = []
    for sub, lab, want in cp.STANDING_ABI:
        r = ff.row(11, sub, lab)
        if r is None:
            bad.append("%s / %s is missing" % (sub, lab))
        elif " ".join(r["values"]).replace(" ", "") != want:
            bad.append("%s / %s is %s, the standing value is %s" % (sub, lab, " ".join(r["values"]), want))
    for sub, lab in cp.FORBIDDEN:
        if ff.row(11, sub, lab) is not None:
            bad.append("%s must have no %s line" % (sub, lab))
    s8 = [b for b in c["sections"][7]["blocks"] if b["sub"] != "Notes"]
    heads_ok = all(b["sub"] in [h for _, h in cp.SEC8_HEADINGS] for b in s8) and not any("action plan" in b["sub"].lower() for b in s8)
    R.add(not bad, "Standing ABIs correct (Life Cover WOL 3%, Childcare 5%, Household needs 5%, Dread Disease 3%, no WOL ABI under Disability)" if not bad else "ABI problem: " + bad[0], "; ".join(bad))
    # structure
    titles = [(s["num"], s["title"]) for s in c["sections"]]
    R.add(titles == list(enumerate(cp.TITLES, 1)) and heads_ok, "Nine sections in the fixed order; Section 8 sub-headings exactly as fixed; Items Requiring Follow-Up last",
          "sections: %s" % titles)
    # flags carried
    n_ff = ffd["stats"]["flags"]
    items = c["sections"][8]["blocks"][0]["rows"]
    n_item = sum(1 for r in items if r["item"]["rule"] == "flag")
    owners_bad = [r["item"]["text"] for r in items if r["item"]["owner"] not in (None,) + w.OWNERS]
    R.add(n_ff == n_item and not owners_bad, "Every flag of the Fact Find (%d) reached Items Requiring Follow-Up; owners only Cameron, CL, Valerie, Lizelle" % n_ff if n_ff == n_item and not owners_bad else
          "%d flag(s) in the Fact Find but %d in the follow-up list%s" % (n_ff, n_item, "; unknown owner" if owners_bad else ""))
    # business assurance only for a business owner
    owner_yes = w.norm(ff.val(2, "Work", "Business owner")) == "yes"
    has_ba = any(b["sub"] == "Business assurance" for b in c["sections"][6]["blocks"]) or any(b["sub"] == "Business" for b in c["sections"][1]["blocks"])
    R.add(owner_yes or not has_ba, "Business parts appear only when Business owner = Yes (%s)" % ("yes" if owner_yes else "no"))
    # joint meeting
    if rj.get("joint"):
        sp = rj.get("spouse_pdf")
        if sp and os.path.exists(sp):
            sd = ffread.read_pdf(sp)
            ids = []
            for s in sd["sections"]:
                for b in s["blocks"]:
                    for r in b["rows"]:
                        v = " ".join(r["values"])
                        if r["label"] in ("ID / passport number", "Cell number", "Work number", "Home number", "Personal email", "Work email") and not blank(v):
                            ids.append(v)
            text = w.norm(" ".join(" ".join(r["values"]) for s in c["sections"] for b in s["blocks"] for r in b["rows"]))
            hit = [i for i in ids if w.norm(i) and w.norm(i) in text]
            R.add(not hit, "Joint meeting: none of the other spouse's identifiers appear in this Summary" if not hit else "The other spouse's details appear in this Summary: %d identifier(s)" % len(hit))
        else:
            R.attested.append("the other spouse's details were not compared (no second Fact Find PDF was given)")
    R.add(True, "Left out of the Summary: %d rows that say Not discussed / N/A (they stay in the Fact Find)" % len(c["left_out"]))


def blank(v):
    return w.norm(v) in cp.BLANKS


def _pdf_checks(R, run, st, c):
    out = os.path.join(run, w.OUT)
    pdfs = glob.glob(os.path.join(out, "*.pdf"))
    path = os.path.join(out, c["file_name"] or "")
    if len(pdfs) != 1 or not os.path.exists(path):
        R.add(False, "The Summary PDF is missing or there is more than one PDF (%d found; expected %r)" % (len(pdfs), c["file_name"]))
        return
    import build
    import tempfile
    tmp = os.path.join(tempfile.mkdtemp(prefix="wrfs-"), "check.pdf")
    build.build_pdf(c, tmp)
    a, b = pdf_pages(path), pdf_pages(tmp)
    same = a is not None and b is not None and w.norm(" ".join(a)) == w.norm(" ".join(b))
    wd, ht = pdf_size_pt(path)
    a4 = abs(wd - 595.3) < 3 and abs(ht - 841.9) < 3
    stale = (st.get("build") or {}).get("pdf_sha") != w.sha256_file(path)
    name_ok = c["file_name"] == w.output_name(c["client"]["first"], c["client"]["surname"], c["date_completed"])
    ok = same and a4 and name_ok and not stale
    R.add(ok, "PDF rebuilt from the data and identical, A4, one PDF only, file name correct (%s)" % c["file_name"] if ok else
          "PDF problem: %s" % ", ".join(x for x, f in (("text differs from content.json", not same), ("not A4", not a4), ("wrong file name", not name_ok), ("changed after it was built", stale)) if f))


def _final_checks(R, run, rj, st, c):
    done = [s for s in STEP_IDS[:-1] if (rj.get("steps", {}).get(s) or {}).get("state") == "done"]
    fp_ok = rj.get("program_fingerprint") == w.program_fingerprint()
    R.add(done == STEP_IDS[:-1] and fp_ok, "Every step done in order (%d of %d) and the programs did not change during the run" % (len(done), len(STEP_IDS) - 1)
          if done == STEP_IDS[:-1] and fp_ok else "Steps done: %s%s" % (", ".join(done) or "none", "; the programs changed during the run" if not fp_ok else ""))
    rc = w.load_opt(os.path.join(run, w.RECEIPT), {})
    pdf = os.path.join(run, w.OUT, c["file_name"]) if c else ""
    size = os.path.getsize(pdf) if pdf and os.path.exists(pdf) else None
    listed = rc.get("pdf.listed_bytes")
    folder = rc.get("pdf.saved_folder", "")
    parts = [p.strip().lower() for p in re.split(r"[\\/]+", folder) if p.strip()]
    want = "%s, %s" % (rj["client"]["surname"], rj["client"]["first"])
    root_ok = ("company - paul" in parts[:5]) or ("company - wr clients" in parts[:5] and "paul kafentzis (client files)" in parts[:7])
    folder_ok = bool(parts) and parts[-1] == "2. fact find" and w.norm(want) == w.norm(parts[-2] if len(parts) > 1 else "") and root_ok
    R.add(size is not None and str(listed) == str(size) and folder_ok, "Saved in the client's own 2. Fact Find folder and the listed size equals the local file (%s bytes)" % size
          if (size is not None and str(listed) == str(size) and folder_ok) else
          "Save not proven: listed size %r vs local %r; folder %r (needs ...\\%s\\2. Fact Find under Company - Paul or Paul Kafentzis (Client Files))" % (listed, size, folder, want))
    R.attested += ["the PDF was sent in the chat" if rc.get("pdf.sent") == "yes" else "the PDF was NOT recorded as sent in the chat",
                   "the folder save and its listing (typed by Claude)", "the page images were looked at" if rc.get("images.looked") == "yes" else "the page images were NOT recorded as looked at",
                   "Paul's yes"]
    if rc.get("pdf.sent") != "yes" or rc.get("images.looked") != "yes":
        R.add(False, "Hand-over not recorded: the PDF must be sent in the chat and the page images looked at (run.py receipt)")


def print_audit(R, st, c, stage, run, full=False):
    lines = ["AUDIT   %s" % w.version_line()]
    for mark, short, detail in R.rows:
        lines.append("%s %s" % (mark, short))
    if R.attested:
        lines.append("Only attested (not proven): " + "; ".join(R.attested) + ".")
    ok = len([r for r in R.rows if r[0] == OK])
    bad = len(R.fails)
    lines.append("RESULT: %s   (%d %s, %d %s)" % ("PASS" if not bad else "FAIL", ok, OK, bad, BAD))
    text = "\n".join(lines)
    print(text)
    fulltext = text + "\n\nFULL RECORD\n" + "\n".join("%s %s\n    %s" % (m, s, d) for m, s, d in R.rows if d)
    try:
        os.makedirs(os.path.join(run, w.OUT), exist_ok=True)
        with open(os.path.join(run, w.OUT, "audit-full.txt"), "w", encoding="utf-8") as f:
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
    R, st, c = run_checks(run, stage)
    ok = print_audit(R, st, c, stage, run, full="--full" in sys.argv)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
