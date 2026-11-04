#!/usr/bin/env python3
"""The one checker of the life-insurer-comparison skill.

  verify.py <run_dir> [pre|final] [--full]

It re-reads the registered documents, re-checks the scope and every answer against their text (the quotes and schedules, the notes, the saved insurer guides), recomputes the premium
escalation, rebuilds the letter and the email body from the answers and the fixed template, compares them with the files that were built, re-checks what came back from Outlook and
Teams, and prints the SHORT AUDIT: one line per check with a green tick or a red cross, and one closing line for what is only attested (Paul, 03/11/2026). The full record is written
to out_record/audit-full.txt.
"""
import hashlib
import json
import os
import sys

import docread
import lic as c
import licbuild as b
import wrlib as w

OK, BAD = "✅", "❌"
STEP_IDS = ["locate", "read", "scope", "research", "answers", "check", "confirm", "build", "save", "draft", "message", "final"]


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


def confirm_sha(a, scope, docs, ev, state, today):
    """What Paul's yes is bound to: the answers, the scope, the declared insurers, every registered document, everything shown in the table, the check results, the wording and the settings."""
    return sha_of({"answers": a, "scope": scope, "insurers": c.declared(state), "docs": {k: d["sha"] for k, d in docs["docs"].items()}, "check": c.check_summary(a, scope, today),
                   "table": b.table_rows(a, scope, docs, ev, today), "settings": c.settings(), "wording": c.wording()})


def load_docs(run):
    docs = w.load_opt(os.path.join(run, w.DOCS), {"docs": {}, "missing": {}})
    ev = {}
    for key, d in docs["docs"].items():
        try:
            ev[key] = docread.Evidence(w.load_json(os.path.join(run, d["text_file"])))
        except Exception:
            ev[key] = None
    return docs, ev


def served_keys(docs, include_guides=True):
    keys = []
    for key in c.served_keys_order(docs):
        if include_guides or docs["docs"][key]["role"] != "guide":
            keys += [(key, n) for n in docs["docs"][key]["served"]]
    return keys


def image_figures(a):
    """Every figure the chat marked as read from a page image: (where, document, page)."""
    out = []

    def walk(x, path):
        if isinstance(x, dict):
            if x.get("image_read"):
                out.append("%s (%s, page %s)" % (path, x.get("source") or "the side's document", x.get("page")))
            for k, v in x.items():
                walk(v, "%s.%s" % (path, k) if path else k)
        elif isinstance(x, list):
            for i, v in enumerate(x):
                walk(v, "%s[%d]" % (path, i))
    walk(a, "")
    return out


def docs_problems(docs, state):
    out = []
    sd = c.side_docs(docs)
    if not c.limits()["sides_min"] <= len(sd) <= c.limits()["sides_max"]:
        out.append("%d quote(s) or schedule(s) registered: from %d to %d are needed" % (len(sd), c.limits()["sides_min"], c.limits()["sides_max"]))
    for role in c.OPTIONAL_ROLES:
        if role == "intake_notes":
            ok = bool(c.docs_of(docs, role)) or any(k.startswith("intake_notes_") and (v or "").strip() for k, v in docs["missing"].items())
        else:
            ok = role in docs["docs"] or (docs["missing"].get(role) or "").strip()
        if not ok:
            out.append("the %s is neither registered nor accounted for with Paul's words" % role.replace("_", " "))
    dec = {d["label"]: d["insurer"] for d in c.declared(state)}
    if sorted(dec) != sorted(sd):
        out.append("the insurers are not declared for every quote and schedule (run.py insurers)")
    return out


def research_problems(docs, state):
    out = []
    dec = c.declared(state)
    if not dec:
        return ["no insurers declared yet (run.py insurers)"]
    insurers = sorted({d["insurer"] for d in dec})
    glabels = [d["label"] for d in docs["docs"].values() if d["role"] == "guide"]
    for ins in insurers:
        has_g = any(w.norm(g).startswith(w.norm(ins) + " ") for g in glabels)
        if not has_g and not (docs["missing"].get(c.dkey("guide", ins)) or "").strip():
            out.append("no guide (and no words from Paul) for %s" % ins)
    for g in glabels:
        if not any(w.norm(g).startswith(w.norm(i) + " ") for i in insurers):
            out.append("the guide %r is not one of the declared insurers'" % g)
    return out


def run_checks(run, stage):
    R = Results()
    rj = w.load_json(os.path.join(run, w.RUN))
    st = w.load_opt(os.path.join(run, w.STATE), {})
    rc = w.load_opt(os.path.join(run, w.RECEIPT), {})
    today = w.parse_date(rj["today"])
    docs, ev = load_docs(run)
    scope = w.load_opt(os.path.join(run, w.SCOPE), None)
    a = w.load_opt(os.path.join(run, w.ANSWERS), None)
    attach_by = c.settings()["attach_by"]
    allog = w.load_opt(os.path.join(run, w.ACCESS), [])
    # ---------------------------------------------------------------- the documents
    R.group = "docs"
    log = [e for e in allog if e.get("purpose") == "locate"]
    prob = docs_problems(docs, st)
    changed = [k for k, d in docs["docs"].items() if not os.path.exists(os.path.join(run, d["file"])) or w.sha256_file(os.path.join(run, d["file"])) != d["sha"]]
    bad = route_order_problems(log)
    good = not prob and not changed and bool(log) and not bad
    n_sides, n_notes = len(c.side_docs(docs)), len(c.docs_of(docs, "intake_notes"))
    R.add(good, "The documents are registered (%d quotes/schedules, %d meeting notes, the Fact Find Summary and the WR Overview accounted for), unchanged; the routes were tried in order, each try logged (%d)" %
          (n_sides, n_notes, len(log)) if good else
          "Documents problem: %s; changed %s; route log %s" % ("; ".join(prob) or "none", changed or "none", "out of order" if bad else ("empty" if not log else "fine")),
          "; ".join("%s %s" % (e["route"], e["result"]) for e in log))
    said = [k for k, v in docs["missing"].items() if (v or "").strip()]
    if said:
        R.attested.append("the document(s) Paul said do not exist or could not be found: %s" % ", ".join(sorted(said)))
    # ---------------------------------------------------------------- reading lock
    R.group = "read"
    if docs["docs"]:
        acked = st.get("read", {}).get("acked", {})
        todo = ["%s:%d" % k for k in served_keys(docs, False)]
        miss = [k for k in todo if len((acked.get(k) or "").strip()) < 3]
        R.add(not miss, "Every page of the %d policy and intake document(s) was served in order and acknowledged (%d of %d)" % (len([k for k in docs["docs"] if docs["docs"][k]["role"] != "guide"]), len(todo) - len(miss), len(todo)) if not miss else
              "Pages not yet acknowledged: %s" % ", ".join(miss[:6]))
        image_only = [k for k, d in docs["docs"].items() if d.get("image_only")]
        if image_only:
            R.attested.append("anything on page(s) with no readable text in: %s" % ", ".join(sorted(image_only)))
    # ---------------------------------------------------------------- the scope
    R.group = "scope"
    ok_s = False
    if scope:
        pr = c.scope_problems(scope, ev, docs)
        ok_s = not pr
        if ok_s:
            ins = [c.terms()["category_names"][k] for k in c.CATEGORIES if scope["categories"][k]["status"] == "in"]
            outs = [c.terms()["category_names"][k] for k in c.CATEGORIES if scope["categories"][k]["status"] == "out"]
            R.add(True, "The benefit scope is proved by a line of the client's own notes for every category (in: %s; out: %s); second life: %s; basis %s; %d sections" %
                  (", ".join(ins), ", ".join(outs) or "none", scope["second_life"].get("name") or "none", scope["basis"], len(scope["sections"])))
            said_cats = [k for k in c.CATEGORIES if scope["categories"][k].get("paul_said")]
            if said_cats:
                R.attested.append("the scope of %s rests on Paul's own words" % ", ".join(said_cats))
            R.attested.append("that the scope reading is right (the program proves the cited line is in the notes, not that it means what the chat says)")
        else:
            R.add(False, "Scope problem: %s" % pr[0], "; ".join(pr))
    else:
        R.add(False, "The scope has not been entered yet", "step 'scope'")
    # ---------------------------------------------------------------- the research (insurers' guides)
    R.group = "research"
    glog = [e for e in allog if e.get("purpose") == "research"]
    guides = c.docs_of(docs, "guide")
    prob = research_problems(docs, st)
    bad = route_order_problems(glog, w.FACT_ROUTES)
    acked = st.get("read", {}).get("acked", {})
    gmiss = ["%s:%d" % k for k in served_keys(docs) if docs["docs"][k[0]]["role"] == "guide" and len((acked.get("%s:%d" % k) or "").strip()) < 3]
    good = not prob and not bad and not gmiss and (bool(glog) or not guides)
    R.add(good, "Every insurer has its own saved guide (%d), each with its web address and date, read page by page; the routes (web, then Chrome) were tried in order (%d tries)" % (len(guides), len(glog)) if good else
          "Research problem: %s%s%s" % ("; ".join(prob) or "none", "; routes out of order" if bad else "", "; guide pages not acknowledged: %s" % ", ".join(gmiss[:3]) if gmiss else ""))
    if guides:
        R.attested.append("that each saved insurer guide is the real, current page it says it is (the chat saved it; the program cannot prove it)")
    # ---------------------------------------------------------------- the answers
    R.group = "answers"
    ok_a = False
    if a and ok_s:
        pr = c.answers_problems(a, scope, ev, docs, today, rj["client"], st)
        ok_a = not pr
        R.add(ok_a, "Answers valid and sourced (%s: %d policies/proposals; %d statements; every figure sits in the evidence line it cites and every evidence line is in the document's text)" %
              (a["client_full_name"], len(a["sides"]), len(a["features"]) + len(a["definitions"] or [])) if ok_a else "Answers problem: %s" % pr[0], "; ".join(pr))
        if ok_a:
            R.add(True, "No category outside the scope appears in any cover, feature, definition, banner, verdict or email text; no placeholder; word limits kept; voice and quote-version rules kept")
            if image_figures(a):
                R.attested.append("figures read from page images: %s" % "; ".join(image_figures(a)))
    elif not a:
        R.add(False, "The answers have not been entered yet", "step 'answers'")
    # ---------------------------------------------------------------- the escalation check
    R.group = "check"
    ck = st.get("check")
    if ok_a:
        summ = c.check_summary(a, scope, today)
        good = bool(ck) and ck.get("sha") == sha_of(summ)
        counts = summ["basis_counts"]
        R.add(good, "The premium escalation was worked out by the program from the printed figures (%s); statements: %d from the policy documents, %d from guides, %d inference(s)" %
              ("; ".join("%s %s%%" % (lab, v["avg"]) for lab, v in summ["per_side"].items() if v["avg"]) or "no projection tables", counts["client_document"], counts["insurer_guide"], counts["inference"]) if good else
              "The check step (run.py check) has not been run for these answers")
        if counts["inference"]:
            R.attested.append("%d statement(s) are inferences shown to the client as 'to be confirmed'" % counts["inference"])
        R.attested.append("the 'who wins' badges, the 'who is ahead' line, the Key Facts Banner and the Verdict (judgement: shown to Paul on the table; the program checks only that each badge rests on a sourced statement)")
    # ---------------------------------------------------------------- Paul's yes
    R.group = "confirm"
    ap = w.load_opt(os.path.join(run, w.APPROVAL), None)
    if ok_a:
        cur = confirm_sha(a, scope, docs, ev, st, today)
        good = bool(ap) and ap.get("sha") == cur and len((ap.get("said") or "").strip()) >= 3 and st.get("shown_sha") == cur
        R.add(good, "Paul was shown the confirmation table (scope with its evidence, figures, flags, statements, the banner and the Verdict, the subject and the Teams message) and said yes to exactly these answers" if good else
              "No valid yes from Paul for these answers: run.py show, put the table in the reply, then run.py approve with his words")
        if good:
            R.attested.append("Paul's yes (the words are typed by the chat)")
    # ---------------------------------------------------------------- the built letter and email
    R.group = "build"
    bd = st.get("build")
    data = None
    if ok_a and bd:
        try:
            letter, body = b.build_all(a, scope, docs, w.parse_date(bd["date"]))
        except (ValueError, KeyError) as e:
            letter = body = None
            R.add(False, "The letter could not be rebuilt from the answers: %s" % e)
        if letter is not None:
            out = os.path.join(run, w.OUT)
            paths = {"letter": os.path.join(out, bd["name"]), "body": os.path.join(out, "draft_body.html")}
            texts = {"letter": letter, "body": body}
            exact = all(os.path.exists(paths[k]) and w.sha256_file(paths[k]) == w.sha256_text(texts[k]) and w.sha256_text(texts[k]) == bd["sha"][k] for k in paths)
            R.add(exact, "The letter and the email body are exactly what the program builds from the confirmed answers and the fixed template (not edited by hand)")
            R.add(bd["name"] == c.file_name(a, w.parse_date(bd["date"])), "The file name is derived, not typed: %s" % bd["name"])
            res = b.html_problems(letter, body, a, scope, docs, today)
            badr = [r for r in res if not r[0]]
            if not badr:
                R.add(True, "The built letter and email passed all %d program checks (sections as ticked and in order, header/banner/salutation/closing in place, no out-of-scope word, voice, a percentage badge on every "
                      "year with a figure and a printed/calculated footnote, the email within the draft tool's allowed tags with no typed signature)" % len(res), "; ".join(r[1] for r in res))
            else:
                for ok, short, detail in badr:
                    R.add(False, short, detail)
                R.add(True, "%d other program checks on the built letter passed" % (len(res) - len(badr)))
            data = {"name": bd["name"]}
            R.attested.append("how the letter looks in Chrome and that its plain English really is plain and its tone natural (the program checks structure, figures and word lists, not the eye)")
            soft = c.soft_version_words(b.text_of(letter) + " " + b.text_of(body))
            if soft:
                R.attested.append("the word(s) %s in the prose (Paul glances: they must not describe an earlier version of a quote)" % ", ".join(repr(x) for x in soft))
    elif ok_a:
        R.add(False, "The letter has not been built yet", "step 'build'")
    # ---------------------------------------------------------------- the save
    R.group = "save"
    sv = st.get("save")
    slog = [e for e in allog if e.get("purpose") == "save"]
    if data and sv:
        local = os.path.join(run, w.OUT, sv["name"])
        size = os.path.getsize(local) if os.path.exists(local) else -1
        R.add(sv["name"] == bd["name"] and size == bd["size"], "The saved file is the letter, named %s" % sv["name"] if sv["name"] == bd["name"] else "The saved file name is not the derived name")
        folder = rc.get("save.folder", "")
        good = (bool(slog) and not route_order_problems(slog) and folder.rstrip("\\/").lower().endswith("comparative quotes") and w.norm(a["plan_folder"]) in w.norm(folder) and
                (rc.get("save.listed_bytes") or "").strip() == str(size))
        R.add(good, "The letter is saved in %s > Comparative Quotes through the routes in order; the listing shows %d bytes, equal to the local file%s" % (a["plan_folder"], size, " (Paul said to overwrite)" if sv.get("overwrite") else "")
              if good else "The save is not proven: record the save tries in order, the folder (the client's folder, then Comparative Quotes) and the listed size (%d bytes)" % size)
        R.add(not sv.get("existing_clash") or bool(sv.get("overwrite")), "No existing file was overwritten without Paul's yes" if not sv.get("existing_clash") or sv.get("overwrite") else
              "A file with this name exists and Paul has not said to overwrite")
        R.attested.append("that the file really sits in the client's folder (the listing is typed by the chat)")
    elif data:
        R.add(False, "The saved letter has not been recorded yet", "step 'save'")
    # ---------------------------------------------------------------- the Outlook draft
    R.group = "draft"
    dr = st.get("draft")
    rb = os.path.join(run, w.OUT, "draft_readback.txt")
    if ok_a and bd and dr and os.path.exists(rb):
        with open(rb, encoding="utf-8") as f:
            res = b.draft_problems(f.read(), a, scope, docs, today)
        badr = [r for r in res if not r[0]]
        made = (rc.get("draft.created_with") or "").strip() == "outlook_create_draft"
        if not badr and w.sha256_file(rb) == dr["sha"] and made:
            R.add(True, "The Outlook draft was made with the Microsoft 365 draft tool, read back and passed all %d checks (To the client, Cc Sitamah, exact subject, every built line, no typed signature, no attachment yet)" % len(res), "; ".join(r[1] for r in res))
        else:
            for ok, short in badr:
                R.add(False, short)
            if w.sha256_file(rb) != dr["sha"]:
                R.add(False, "The saved read-back was changed after it was checked")
            if not made:
                R.add(False, "Record draft.created_with = outlook_create_draft (the draft is made with the Microsoft 365 draft tool so the server signature is added once)")
        R.attested.append("that the draft was NOT sent by Claude, that the HTML letter is attached by %s before it goes out, and that the server signature appears once at send time" % ("Paul" if attach_by == "paul" else "Sitamah"))
    elif ok_a and bd:
        R.add(False, "The Outlook draft has not been read back yet", "step 'draft'")
    # ---------------------------------------------------------------- the Teams message
    R.group = "message"
    ms = st.get("message")
    mrb = os.path.join(run, w.OUT, "message_readback.txt")
    if ok_a and ms and dr and os.path.exists(mrb):
        with open(mrb, encoding="utf-8") as f:
            res = b.message_problems(f.read(), a, scope, docs, ms["greeting"], bd["name"])
        badr = [r for r in res if not r[0]]
        chat_ok = (rc.get("message.chat") or "").strip() == c.SITAMAH_CHAT and (rc.get("message.format") or "").strip().lower() == "markdown"
        if not badr and chat_ok and w.sha256_file(mrb) == ms.get("sha"):
            R.add(True, "Sitamah's message went to the 1:1 chat as markdown and was read back: greeting, bold labels, file, folder, insurers and basis (%d checks)" % len(res), "; ".join(r[1] for r in res))
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
        R.attested += ["the advice itself and which insurer suits the client (judgement, recorded with sources)", "that every product-knowledge statement is true (the program proves the cited line is in the saved guide or the policy document, not that the guide is right)",
                       "that each evidence line is the right line of its document for the figure it supports"]
        if a and ok_a:
            fl = c.paul_flags(a, scope, docs, ev, today)
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
