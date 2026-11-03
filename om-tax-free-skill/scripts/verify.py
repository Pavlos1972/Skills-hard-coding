#!/usr/bin/env python3
"""The one checker of the om-tax-free-skill.

  verify.py <run_dir> [pre|final] [--full]

It re-reads the registered documents, re-checks every answer against their text, rebuilds the email from the answers and the fixed template, compares
it with the files that were built, re-checks what came back from Outlook and Teams, and prints the SHORT AUDIT: one line per check with a green tick or a
red cross, and one closing line for what is only attested (Paul, 03/11/2026). The full record is written to out_record/audit-full.txt.
"""
import hashlib
import json
import os
import sys

import docread
import tfi
import wrlib as w

OK, BAD = "✅", "❌"
STEP_IDS = ["locate", "read", "answers", "confirm", "build", "save", "draft", "message", "final"]


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


def confirm_sha(a, docs):
    """What Paul's yes is bound to: the answers, everything shown in the table, the signature setting and the fixed tax facts."""
    return sha_of({"answers": a, "table": tfi.table_rows(a, docs), "sig": tfi.settings()["signature_mode"], "facts": tfi.facts()})


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
    for role in tfi.SERVED_ROLES:
        d = docs["docs"].get(role)
        if d:
            keys += [(role, n) for n in d["served"]]
    return keys


def missing_docs(docs):
    """Roles still neither registered nor declared missing by Paul."""
    reg, mis = docs["docs"], {k for k, v in docs["missing"].items() if (v or "").strip()}
    out = [r for r in tfi.ALWAYS_NEEDED if r not in reg]
    for r in ("strategy_summary", "risk_questionnaire", "overview"):
        if r not in reg and r not in mis:
            out.append(r)
    if not any(tfi.is_sheet(r) for r in reg) and "fund_fact_sheet" not in mis:
        out.append("fund_fact_sheet")
    return out


def run_checks(run, stage):
    R = Results()
    rj = w.load_json(os.path.join(run, w.RUN))
    st = w.load_opt(os.path.join(run, w.STATE), {})
    rc = w.load_opt(os.path.join(run, w.RECEIPT), {})
    today = w.parse_date(rj["today"])
    docs, ev = load_docs(run)
    a = w.load_opt(os.path.join(run, w.ANSWERS), None)
    sig_mode = tfi.settings()["signature_mode"]
    # ---------------------------------------------------------------- the documents
    R.group = "docs"
    log = [e for e in w.load_opt(os.path.join(run, w.ACCESS), []) if e.get("purpose") == "locate"]
    absent = missing_docs(docs)
    changed = [r for r, d in docs["docs"].items() if not os.path.exists(os.path.join(run, d["file"])) or w.sha256_file(os.path.join(run, d["file"])) != d["sha"]]
    bad = route_order_problems(log)
    good = not absent and not changed and bool(log) and not bad
    R.add(good, "The client's documents are registered (%s), unchanged; the routes were tried in order, each try logged (%d on record)" % (", ".join(sorted(docs["docs"])), len(log)) if good else
          "Documents problem: missing %s; changed %s; route log %s" % (absent or "none", changed or "none", "out of order" if bad else ("empty" if not log else "fine")),
          "; ".join("%s %s" % (e["route"], e["result"]) for e in log))
    said = [r for r, v in docs["missing"].items() if (v or "").strip()]
    if said:
        R.attested.append("the document(s) Paul said are not available: %s" % ", ".join(sorted(said)))
    # ---------------------------------------------------------------- reading lock
    R.group = "read"
    if docs["docs"]:
        acked = st.get("read", {}).get("acked", {})
        todo = ["%s:%d" % k for k in served_keys(docs)]
        miss = [k for k in todo if len((acked.get(k) or "").strip()) < 3]
        R.add(not miss, "Every page of the quote, the Fact Find Summary, the questionnaire and the Overview was served in order and acknowledged (%d of %d)" % (len(todo) - len(miss), len(todo)) if not miss else
              "Pages not yet acknowledged: %s" % ", ".join(miss[:6]))
        image_only = [r for r, d in docs["docs"].items() if d.get("image_only")]
        if image_only:
            R.attested.append("anything on page(s) with no readable text in: %s" % ", ".join(sorted(image_only)))
    # ---------------------------------------------------------------- the answers
    R.group = "answers"
    ok_a = False
    if a:
        pr = tfi.answers_problems(a, ev, docs, today, rj["client"])
        ok_a = not pr
        R.add(ok_a, "Answers valid and sourced (%s: %d fund(s), R %s p.m., start %s); allocations add up to 100%%; conflicts: none" %
              (a["client_full_name"], len(a["funds"]), tfi.money_shown(a["contribution"]), a["start_date"]) if ok_a else "Answers problem: %s" % pr[0], "; ".join(pr))
        if ok_a:
            R.add(True, "Name, age, employer, income, contribution, start date, every fund, allocation and fee were found in the right documents' own text; the fee total is added up by the program")
            if any(e is not None and not e.has_text for e in ev.values()):
                R.attested.append("figures in a document with no readable text")
    else:
        R.add(False, "The answers have not been entered yet", "step 'answers'")
    # ---------------------------------------------------------------- Paul's yes
    R.group = "confirm"
    ap = w.load_opt(os.path.join(run, w.APPROVAL), None)
    if ok_a:
        cur = confirm_sha(a, docs)
        good = bool(ap) and ap.get("sha") == cur and len((ap.get("said") or "").strip()) >= 3 and st.get("shown_sha") == cur
        R.add(good, "Paul was shown the confirmation table (with the email subject and the Teams message) and said yes to exactly these answers" if good else
              "No valid yes from Paul for these answers: run.py show, put the table in the reply, then run.py approve with his words")
        if good:
            R.attested.append("Paul's yes (the words are typed by the chat)")
    # ---------------------------------------------------------------- the built email
    R.group = "build"
    bd = st.get("build")
    data = None
    if ok_a and bd:
        try:
            full, nologo, body = tfi.build_all(a, bd["sent"])
        except ValueError as e:
            full = nologo = body = None
            R.add(False, "The email could not be rebuilt from the answers: %s" % e)
        if full is not None:
            out = os.path.join(run, w.OUT)
            paths = {"full": os.path.join(out, bd["name"]), "saved": os.path.join(out, "saved", bd["name"]), "body": os.path.join(out, "draft_body.html")}
            texts = {"full": full, "saved": nologo, "body": body}
            exact = all(os.path.exists(paths[k]) and w.sha256_file(paths[k]) == w.sha256_text(texts[k]) and w.sha256_text(texts[k]) == bd["sha"][k] for k in paths)
            R.add(exact, "The three files are exactly what the program builds from the confirmed answers and the fixed template (not edited by hand)")
            R.add(bd["name"] == tfi.file_name(a, w.parse_date(bd["date"])), "The file name is derived, not typed: %s" % bd["name"])
            res = tfi.html_problems(full, nologo, body, a, bd["sent"])
            badr = [r for r in res if not r[0]]
            if not badr:
                R.add(True, "The built email passed all %d program checks (no placeholder left, tables open = close, header To/Cc/Subject/Importance, weekdays computed, every fund, fee and the "
                      "contribution, the fixed text, logo only in the full copy)" % len(res), "; ".join(r[1] for r in res))
            else:
                for ok, short, detail in badr:
                    R.add(False, short, detail)
                R.add(True, "%d other program checks on the built email passed" % (len(res) - len(badr)))
            data = {"name": bd["name"]}
            R.attested.append("how the email looks (the program checks its text and tags, not the eye)")
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
        R.add(good, "Saved in %s > Comparative Quotes through the routes in order; the listing shows %d bytes, equal to the local file%s" % (a["plan_folder"], size, " (Paul said to overwrite)" if sv.get("overwrite") else "")
              if good else "The save is not proven: record the save tries in order, the folder (the plan folder, then Comparative Quotes) and the listed size (%d bytes)" % size)
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
            res = tfi.draft_problems(f.read(), a, sig_mode)
        badr = [r for r in res if not r[0]]
        if not badr and w.sha256_file(rb) == dr["sha"]:
            R.add(True, "The Outlook draft was read back and passed all %d checks (To the client, Cc Sitamah, exact subject, High importance, tables open = close, 'Kind regards,' %s, no placeholder, no Loop, every fund, fee and date)" %
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
            res = tfi.message_problems(f.read(), a, docs, ms["greeting"])
        badr = [r for r in res if not r[0]]
        chat_ok = (rc.get("message.chat") or "").strip() == tfi.SITAMAH_CHAT and (rc.get("message.format") or "").strip().lower() == "markdown"
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
        R.add(done == STEP_IDS[:-1] and fpok, "Every step done in order (%d of %d) and the programs and the template did not change during the run" % (len(done), len(STEP_IDS) - 1) if done == STEP_IDS[:-1] and fpok else
              "Steps done: %s%s" % (", ".join(done) or "none", "; the programs changed during the run" if not fpok else ""))
        tf = tfi.facts()
        R.attested += ["the advice itself and the next meeting (judgement, recorded with sources)", "that each figure sits in the right row of its document (it is only proven to appear in it)",
                       "the fixed tax facts in the email (%s a year, %s lifetime, %s on the excess): kept as in Paul's template, not verified" % (tf["annual_limit"], tf["lifetime_limit"], tf["excess_tax_rate"])]
        if a and a.get("flags"):
            R.attested.append("flags for Paul: %s" % "; ".join(a["flags"]))
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
