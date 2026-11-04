#!/usr/bin/env python3
"""The one checker of the investment-comparisons-skill.

  verify.py <run_dir> [pre|final] [--full]

It re-reads the registered documents, re-checks every answer against their text (the quotes, the saved fund fact sheets, the supplementary documents), recomputes the comparison
(apples-to-apples, fee totals, Tax-Free room, stale and missing fact sheets), rebuilds the email from the answers and the fixed template, compares it with the files that were
built, re-checks what came back from Outlook and Teams, and prints the SHORT AUDIT: one line per check with a green tick or a red cross, and one closing line for what is only
attested (Paul, 03/11/2026). The full record is written to out_record/audit-full.txt.
"""
import hashlib
import json
import os
import sys

import docread
import icbuild as b
import icmp as c
import wrlib as w

OK, BAD = "✅", "❌"
STEP_IDS = ["locate", "read", "answers", "check", "confirm", "build", "save", "draft", "message", "final"]


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


def check_summary(a, today):
    """What the check step proves and shows (a pure function of the answers): bound to the step by its hash."""
    return {"mismatches": c.mismatches(a), "fees": [[p["name"], list(c.fee_total(p))] for p in a["providers"]], "stale": c.stale_sheets(a, today), "notfound": c.not_found_sheets(a),
            "risk": c.risk_flags(a), "tfsa": [[n, str(y), [list(map(str, x)) for x in br]] for n, y, br in c.tfsa_rows(a)] if a["product_type"] == "TFSA" else [],
            "supplement": [list(x) for x in c.supplement_items(a)]}


def confirm_sha(a, docs, state, today):
    """What Paul's yes is bound to: the answers, the declared funds, every registered document, everything shown in the table, the check results, the wording and the signature setting."""
    return sha_of({"answers": a, "funds": c.declared_funds(state), "docs": {k: d["sha"] for k, d in docs["docs"].items()}, "check": check_summary(a, today),
                   "table": b.table_rows(a, docs, today), "sig": c.settings()["signature_mode"], "wording": c.wording(), "terms": c.terms()})


def load_docs(run):
    docs = w.load_opt(os.path.join(run, w.DOCS), {"docs": {}, "missing": {}})
    ev = {}
    for key, d in docs["docs"].items():
        try:
            ev[key] = docread.Evidence(w.load_json(os.path.join(run, d["text_file"])))
        except Exception:
            ev[key] = None
    return docs, ev


def served_keys(docs):
    keys = []
    for key in c.served_keys_order(docs):
        keys += [(key, n) for n in docs["docs"][key]["served"]]
    return keys


def docs_problems(docs, state):
    """(problems about what must be registered or accounted for)."""
    out = []
    quotes = c.docs_of(docs, "quote")
    if not c.MIN_PROVIDERS <= len(quotes) <= c.MAX_PROVIDERS:
        out.append("%d quote(s) registered: from %d to %d are needed (one per provider)" % (len(quotes), c.MIN_PROVIDERS, c.MAX_PROVIDERS))
    if "fact_find" not in docs["docs"] and not (docs["missing"].get("fact_find") or "").strip():
        out.append("the client's Fact Find is neither registered nor accounted for with Paul's words")
    funds = c.declared_funds(state)
    if not funds:
        out.append("no funds declared yet (run.py funds)")
    for d in funds:
        k = c.dkey("factsheet", c.sheet_label(d["provider"], d["name"]))
        if k not in docs["docs"] and not (docs["missing"].get(k) or "").strip():
            out.append("no fact sheet (and no words from Paul) for %s" % c.sheet_label(d["provider"], d["name"]))
    return out


def run_checks(run, stage):
    R = Results()
    rj = w.load_json(os.path.join(run, w.RUN))
    st = w.load_opt(os.path.join(run, w.STATE), {})
    rc = w.load_opt(os.path.join(run, w.RECEIPT), {})
    today = w.parse_date(rj["today"])
    docs, ev = load_docs(run)
    a = w.load_opt(os.path.join(run, w.ANSWERS), None)
    sig_mode = c.settings()["signature_mode"]
    # ---------------------------------------------------------------- the documents
    R.group = "docs"
    log = [e for e in w.load_opt(os.path.join(run, w.ACCESS), []) if e.get("purpose") == "locate"]
    flog = [e for e in w.load_opt(os.path.join(run, w.ACCESS), []) if e.get("purpose") == "factsheet"]
    prob = docs_problems(docs, st)
    changed = [k for k, d in docs["docs"].items() if not os.path.exists(os.path.join(run, d["file"])) or w.sha256_file(os.path.join(run, d["file"])) != d["sha"]]
    bad = route_order_problems(log) + route_order_problems(flog, w.FACT_ROUTES)
    good = not prob and not changed and bool(log) and not bad and (bool(flog) or all(not d.get("route") in w.FACT_ROUTES for d in docs["docs"].values()))
    nq, nf = len(c.docs_of(docs, "quote")), len(c.docs_of(docs, "factsheet"))
    R.add(good, "The client's documents are registered (%d quotes, %d fund fact sheets, the Fact Find%s), unchanged; the routes were tried in order, each try logged (%d for the files, %d for the fact sheets)" %
          (nq, nf, ", %d supplementary" % len(c.docs_of(docs, "supplement")) if c.docs_of(docs, "supplement") else "", len(log), len(flog)) if good else
          "Documents problem: %s; changed %s; route log %s" % ("; ".join(prob) or "none", changed or "none", "out of order" if bad else ("empty" if not log else "fine")),
          "; ".join("%s %s" % (e["route"], e["result"]) for e in log + flog))
    said = [k for k, v in docs["missing"].items() if (v or "").strip()]
    if said:
        R.attested.append("the document(s) Paul said do not exist or could not be found: %s" % ", ".join(sorted(said)))
    if c.docs_of(docs, "factsheet"):
        R.attested.append("that each saved fact sheet text is the real, current page it says it is (the chat saved it; the program cannot prove it)")
    # ---------------------------------------------------------------- reading lock
    R.group = "read"
    if docs["docs"]:
        acked = st.get("read", {}).get("acked", {})
        todo = ["%s:%d" % k for k in served_keys(docs)]
        miss = [k for k in todo if len((acked.get(k) or "").strip()) < 3]
        R.add(not miss, "Every page of the %d registered document(s) was served in order and acknowledged (%d of %d)" % (len(docs["docs"]), len(todo) - len(miss), len(todo)) if not miss else
              "Pages not yet acknowledged: %s" % ", ".join(miss[:6]))
        image_only = [k for k, d in docs["docs"].items() if d.get("image_only")]
        if image_only:
            R.attested.append("anything on page(s) with no readable text in: %s" % ", ".join(sorted(image_only)))
    # ---------------------------------------------------------------- the answers
    R.group = "answers"
    ok_a = False
    if a:
        pr = c.answers_problems(a, ev, docs, today, rj["client"], st)
        ok_a = not pr
        R.add(ok_a, "Answers valid and sourced (%s: %s, %d providers, %d funds); conflicts: none" % (a["client_full_name"], a["product_type"], len(a["providers"]), len(c.sheet_entries(a))) if ok_a else
              "Answers problem: %s" % pr[0], "; ".join(pr))
        if ok_a:
            R.add(True, "Every fee, premium, term, fund, allocation and loyalty figure is in the quote's own text (exact, next to its label); every fund figure and date is in its saved fact sheet; allocations add up to 100%; "
                  "no quote is an EAC only; descriptions are in our own words")
            if any(e is not None and not e.has_text for e in ev.values()):
                R.attested.append("figures in a document with no readable text")
    else:
        R.add(False, "The answers have not been entered yet", "step 'answers'")
    # ---------------------------------------------------------------- the comparison
    R.group = "check"
    ck = st.get("check")
    if ok_a:
        summ = check_summary(a, today)
        good = bool(ck) and ck.get("sha") == sha_of(summ)
        mm = summ["mismatches"]
        R.add(good, "The comparison was worked out by the program from these answers: apples-to-apples %s; fee totals %s; %d stale and %d missing fact sheet(s)" %
              ("all the same" if not mm else "NOT the same (%s: shown to Paul and labelled in the email)" % ", ".join(f for f, _d in mm), ", ".join("%s %s%%" % (n, t[1]) for n, t in summ["fees"]),
               len(summ["stale"]), len(summ["notfound"])) if good else "The comparison step (run.py check) has not been run for these answers")
        if a["product_type"] == "TFSA":
            lim = c.tfsa_limits()
            R.add(lim[2], "The Tax-Free limits come from assets/tax_facts.json, confirmed by Paul (annual R %s, lifetime R %s)" % (c.money_shown(lim[0]), c.money_shown(lim[1])) if lim[2] else
                  "The Tax-Free limits are NOT confirmed by Paul")
        if summ["risk"]:
            R.attested.append("whether the funds suit the client's risk profile (the program only compares the fact sheet's risk label with the profile and flags %d difference(s))" % len(summ["risk"]))
    # ---------------------------------------------------------------- Paul's yes
    R.group = "confirm"
    ap = w.load_opt(os.path.join(run, w.APPROVAL), None)
    if ok_a:
        cur = confirm_sha(a, docs, st, today)
        good = bool(ap) and ap.get("sha") == cur and len((ap.get("said") or "").strip()) >= 3 and st.get("shown_sha") == cur
        R.add(good, "Paul was shown the confirmation table (the comparison, the flags, the email subject and the Teams message) and said yes to exactly these answers%s" %
              (", including going on although the quotes do not match" if c.mismatches(a) else "") if good else
              "No valid yes from Paul for these answers: run.py show, put the table in the reply, then run.py approve with his words")
        if good:
            R.attested.append("Paul's yes (the words are typed by the chat)")
    # ---------------------------------------------------------------- the built email
    R.group = "build"
    bd = st.get("build")
    data = None
    if ok_a and bd:
        try:
            full, nologo, body = b.build_all(a, bd["sent"], docs, today)
        except ValueError as e:
            full = nologo = body = None
            R.add(False, "The email could not be rebuilt from the answers: %s" % e)
        if full is not None:
            out = os.path.join(run, w.OUT)
            paths = {"full": os.path.join(out, bd["name"]), "saved": os.path.join(out, "saved", bd["name"]), "body": os.path.join(out, "draft_body.html")}
            texts = {"full": full, "saved": nologo, "body": body}
            exact = all(os.path.exists(paths[k]) and w.sha256_file(paths[k]) == w.sha256_text(texts[k]) and w.sha256_text(texts[k]) == bd["sha"][k] for k in paths)
            R.add(exact, "The three files are exactly what the program builds from the confirmed answers and the fixed template (not edited by hand)")
            R.add(bd["name"] == c.file_name(a, w.parse_date(bd["date"])), "The file name is derived, not typed: %s" % bd["name"])
            res = b.html_problems(full, nologo, body, a, bd["sent"], docs, today)
            badr = [r for r in res if not r[0]]
            if not badr:
                R.add(True, "The built email passed all %d program checks (no placeholder, header, weekdays, the four tables in order with an intro line each, no EAC headline, every industry term explained, "
                      "totals add up, every fund dated, flags and optional parts only when due, logo only in the full copy)" % len(res), "; ".join(r[1] for r in res))
            else:
                for ok, short, detail in badr:
                    R.add(False, short, detail)
                R.add(True, "%d other program checks on the built email passed" % (len(res) - len(badr)))
            data = {"name": bd["name"]}
            R.attested.append("how the email looks and that its plain English really is plain (the program checks structure, terms and figures, not the eye)")
    elif ok_a:
        R.add(False, "The email has not been built yet", "step 'build'")
    # ---------------------------------------------------------------- the save
    R.group = "save"
    sv = st.get("save")
    slog = [e for e in w.load_opt(os.path.join(run, w.ACCESS), []) if e.get("purpose") == "save"]
    if data and sv:
        local = os.path.join(run, w.OUT, "saved", sv["name"])
        size = os.path.getsize(local) if os.path.exists(local) else -1
        R.add(sv["name"] == bd["name"] and size == bd["size"], "The saved copy is the no-logo copy, named %s" % sv["name"] if sv["name"] == bd["name"] else "The saved file name is not the derived name")
        folder = rc.get("save.folder", "")
        good = (bool(slog) and not route_order_problems(slog) and folder.rstrip("\\/").lower().endswith("comparative quotes") and w.norm(a["plan_folder"]) in w.norm(folder) and
                (rc.get("save.listed_bytes") or "").strip() == str(size))
        R.add(good, "The no-logo copy is saved in %s > Comparative Quotes through the routes in order; the listing shows %d bytes, equal to the local file%s" % (a["plan_folder"], size, " (Paul said to overwrite)" if sv.get("overwrite") else "")
              if good else "The save is not proven: record the save tries in order, the folder (the client's folder, then Comparative Quotes) and the listed size (%d bytes)" % size)
        R.add(not sv.get("existing_clash") or bool(sv.get("overwrite")), "No existing file was overwritten without Paul's yes" if not sv.get("existing_clash") or sv.get("overwrite") else
              "A file with this name exists and Paul has not said to overwrite")
        R.attested.append("that the file really sits in the client's folder (the listing is typed by the chat)")
    elif data:
        R.add(False, "The saved copy has not been recorded yet", "step 'save'")
    # ---------------------------------------------------------------- the Outlook draft
    R.group = "draft"
    dr = st.get("draft")
    rb = os.path.join(run, w.OUT, "draft_readback.txt")
    if ok_a and bd and dr and os.path.exists(rb):
        with open(rb, encoding="utf-8") as f:
            res = b.draft_problems(f.read(), a, today, sig_mode)
        badr = [r for r in res if not r[0]]
        if not badr and w.sha256_file(rb) == dr["sha"]:
            R.add(True, "The Outlook draft was read back and passed all %d checks (To the client, Cc Sitamah, exact subject, High importance, tables open = close, 'Kind regards,' %s, no placeholder, no Loop, every figure and date)" %
                  (len(res), "once" if sig_mode == "insert" else "none"), "; ".join(r[1] for r in res))
        else:
            for ok, short in badr:
                R.add(False, short)
            if w.sha256_file(rb) != dr["sha"]:
                R.add(False, "The saved read-back was changed after it was checked")
        tab, stray = (rc.get("draft.tab_closed") or "").strip().lower(), (rc.get("draft.stray_deleted") or "").strip()
        R.add(tab == "yes" and bool(stray), "The Chrome tab was closed and stray drafts were dealt with (%s)" % stray if tab == "yes" and stray else
              "Record draft.tab_closed = yes and draft.stray_deleted = the number deleted (or none)")
        R.attested.append("that the draft was NOT sent by Claude and looks right in Outlook; the signature (%s) is the open question with Paul" % ("inserted by Claude" if sig_mode == "insert" else "added by the server"))
    elif ok_a and bd:
        R.add(False, "The Outlook draft has not been read back yet", "step 'draft'")
    # ---------------------------------------------------------------- the Teams message
    R.group = "message"
    ms = st.get("message")
    mrb = os.path.join(run, w.OUT, "message_readback.txt")
    if ok_a and ms and dr and os.path.exists(mrb):
        with open(mrb, encoding="utf-8") as f:
            res = b.message_problems(f.read(), a, docs, ms["greeting"])
        badr = [r for r in res if not r[0]]
        chat_ok = (rc.get("message.chat") or "").strip() == c.SITAMAH_CHAT and (rc.get("message.format") or "").strip().lower() == "markdown"
        if not badr and chat_ok and w.sha256_file(mrb) == ms.get("sha"):
            R.add(True, "Sitamah's message went to the 1:1 chat as markdown and was read back: greeting, bold labels, numbered list, no raw tags (%d checks)" % len(res), "; ".join(r[1] for r in res))
        else:
            for ok, short in badr:
                R.add(False, short)
            if not chat_ok:
                R.add(False, "The message must go to the 1:1 chat with Sitamah (record message.chat and message.format = markdown)")
            if w.sha256_file(mrb) != ms.get("sha"):
                R.add(False, "The saved read-back was changed after it was checked")
        R.attested.append("that the Teams message really arrived (the read-back is typed by the chat)")
    elif ok_a and dr:
        R.add(False, "The Teams message has not been sent and read back yet", "step 'message'")
    if stage == "final":
        R.group = "final"
        done = [s for s in STEP_IDS[:-1] if (rj.get("steps", {}).get(s) or {}).get("state") == "done"]
        fpok = rj.get("program_fingerprint") == w.program_fingerprint()
        R.add(done == STEP_IDS[:-1] and fpok, "Every step done in order (%d of %d) and the programs, the template and the wording did not change during the run" % (len(done), len(STEP_IDS) - 1) if done == STEP_IDS[:-1] and fpok else
              "Steps done: %s%s" % (", ".join(done) or "none", "; the programs changed during the run" if not fpok else ""))
        R.attested += ["the advice itself, which plan suits the client and the next meeting (judgement, recorded with sources)", "that each figure sits in the right row of its document where its label was not found in the text",
                       "that every difference between a supplementary document and its quote was noticed (the program lists the figures only in the supplement, the chat compares)"]
        if a and ok_a:
            fl = c.paul_flags(a, today)
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
