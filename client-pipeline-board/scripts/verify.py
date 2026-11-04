#!/usr/bin/env python3
"""The one checker of the client-pipeline-board.

  verify.py <run_dir> [pre|final] [--full]

It REBUILDS the board, the emails, the Sitamah messages and the check-in from the run folder itself and compares them with what is on disk, so
nothing is taken on trust from a file Claude could have edited. The reply to Paul carries the SHORT AUDIT it prints: one line per check with a
green tick or a red cross, and one closing line for what is only attested (Paul, 03/11/2026). The full record is written to
out_record/audit-full.txt (--full prints it).
"""
import os
import sys

import board as b
import boardhtml as bh
import engine as eng
import wrlib as w

OK, BAD = "✅", "❌"
STEP_IDS = ["locate", "change", "route", "build", "confirm", "send", "publish", "final"]


class Results:
    def __init__(self):
        self.rows, self.attested, self.group = [], [], ""

    def add(self, ok, short, detail=""):
        self.rows.append((OK if ok else BAD, short, detail, self.group))

    @property
    def fails(self):
        return [r for r in self.rows if r[0] == BAD]


def _read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def run_checks(run, stage):
    R = Results()
    rj = w.load_json(os.path.join(run, w.RUN))
    st = w.load_opt(os.path.join(run, w.STATE), {})
    rc = w.load_opt(os.path.join(run, w.RECEIPT), {})
    log = w.load_opt(os.path.join(run, w.ACCESS), [])
    c = eng.compute(run)
    req = rj["client"]
    reqname = "%s %s" % (req["first"], req["surname"])
    # ---------------------------------------------------------------- locate
    R.group = "locate"
    base = c["base"]
    if base is None:
        R.add(False, "The board has not been loaded (read the published page back, or say it is the first board)", "step 'locate': run.py base")
    elif base == {}:
        R.add(bool((st.get("base") or {}).get("said")), "First board: Paul said there is no board yet, and the search for one is logged" if (st.get("base") or {}).get("said") else "A first board needs Paul's words")
    else:
        good = b.state_sha(base) == base.get("state_sha") and w.norm(b.client_full(base)) == w.norm(reqname)
        R.add(good, "The existing board was read back from the published page: its checksum is right and it is %s's" % reqname if good else "The base board is damaged or belongs to someone else")
    bad = eng.route_order_problems(log)
    searched = any(e.get("purpose") == "board" for e in log)
    docs = w.load_opt(os.path.join(run, w.DOCS), {"docs": {}})
    dbad = []
    for role, d in docs["docs"].items():
        path = os.path.join(run, d["file"])
        if not os.path.exists(path) or w.sha256_file(path) != d["sha"]:
            dbad.append(role + " (file changed)")
        elif not any(e["route"] == d["route"] and e["result"] == "found" and e.get("purpose") == "docs" for e in log):
            dbad.append(role + " (no access try logged)")
    okacc = searched and not bad and not dbad
    R.add(okacc, "%d access tries logged in route order; documents registered: %s, each found through a logged route and unchanged" % (len(log), ", ".join(sorted(docs["docs"])) or "none") if okacc else
          ("The routes were not tried in order: %s" % ", ".join(bad)) if bad else ("Document problem: %s" % ", ".join(dbad)) if dbad else "No search for the board is logged")
    # ---------------------------------------------------------------- change
    R.group = "change"
    if c["change"] is None or base is None:
        R.add(False, "The changes have not been entered yet", "step 'change': run.py change")
    else:
        pr = c["problems"]
        n_ops = len(c["change"].get("ops") or [])
        ev_n = sum(1 for o in c["change"].get("ops", []) if o.get("op") == "identified" for x in o.get("bullets", []) if x.get("evidence"))
        pa_n = sum(1 for o in c["change"].get("ops", []) if o.get("op") == "identified" for x in o.get("bullets", []) if not x.get("evidence"))
        R.add(not pr, "All %d change(s) apply and every rule holds; every Identified point is proved (%d by a verbatim document line with its figures, %d by Paul's words)" % (n_ops, ev_n, pa_n) if not pr else
              "Change problem: %s" % pr[0], "; ".join(pr))
        if pa_n:
            R.attested.append("%d Identified point(s) rest on Paul's own words typed by the chat" % pa_n)
        ep, np_ = c["email_problems"], c["notify_problems"]
        R.add(not ep and not np_, "%d email(s) follow the send table (To and Cc exactly the table's, plain subject, no sign-off, details block where needed); %d Sitamah message(s) are on the list" % (len(c["emails"]), len([m for m in c["messages"] if m["tier"] == "action"])) if not (ep or np_) else
              "Email or message problem: %s" % (ep + np_)[0], "; ".join(ep + np_))
        deleg = [a for a in c["new_actions"] if a.get("via")]
        if deleg:
            R.attested.append("that the product skill(s) %s passed their own audit (the board holds only the receipt)" % ", ".join(sorted({a["via"] for a in deleg})))
    # ---------------------------------------------------------------- route
    R.group = "route"
    ok_route = bool(st.get("route")) and c["board"] is not None and not (c["problems"] or c["email_problems"] or c["notify_problems"])
    R.add(ok_route, "The routing was printed from the send table; every item that needs Paul first has his words, every send has a fresh-yes route" if ok_route else "The routing has not been shown or something is wrong: run.py route")
    # ---------------------------------------------------------------- build
    R.group = "build"
    saved = w.load_opt(os.path.join(run, w.BOARD), None)
    fb = eng.final_board(run, c) if c["board"] is not None else None
    if saved is None or fb is None:
        R.add(False, "The board has not been built yet", "step 'build'")
    else:
        R.add(saved == fb, "board.json is exactly what the program builds from the old board and the changes (not edited by hand)")
        bp = b.board_problems(saved, c["today"])
        badbp = [x for x in bp if not x[0]]
        R.add(not badbp, "Every card rule holds (%d of %d): tags, Fact Find shape, one plain question per card, short one-fact bullets, proof on every point, receipts, Change Log" % (len(bp), len(bp)) if not badbp else
              "Card rule broken: %s" % badbp[0][1], "; ".join(x[1] + " " + x[2] for x in badbp))
        page = _read(os.path.join(run, w.OUT, w.PAGE))
        same = page == bh.render(saved) if page else False
        hp = [x for x in bh.html_problems(page or "", saved) if not x[0]] if page else [(False, "no page", "")]
        R.add(same and not hp, "The page is exactly what the program draws, and follows every layout rule (order, badges, read-out only, no script, dark mode, phone width)" if same and not hp else
              ("out/board.html is missing or is not what the program draws" if not same else "Page problem: %s" % hp[0][1]))
        mj = w.load_opt(os.path.join(run, w.OUT, "messages.json"), None)
        msg_same = mj == c["messages"] and all(_read(os.path.join(run, w.OUT, "message_%s.txt" % m["id"])) == m["text"] for m in c["messages"])
        R.add(msg_same, "The %d Sitamah message(s) are exactly what the program builds (tier tag first; an FYI ends 'Nothing needed from you.')" % len(c["messages"]) if msg_same else "The messages on disk are not what the program builds")
        ci = w.load_opt(os.path.join(run, w.OUT, "checkin.json"), None)
        R.add(ci == c["checkin"], "The same-day check-in settings are exactly the program's" if c["checkin"] else "No follow-up date this run, so no check-in")
    # ---------------------------------------------------------------- confirm
    R.group = "confirm"
    ap = w.load_opt(os.path.join(run, w.APPROVAL), None)
    cur = eng.confirm_sha(c) if c["board"] is not None and saved is not None else None
    okap = bool(ap) and cur is not None and ap.get("sha") == cur and len((ap.get("said") or "").strip()) >= 3 and st.get("shown_sha") == cur
    R.add(okap, "Paul's yes is recorded for exactly this version, after he was shown the table, the emails and the messages" if okap else "No valid yes from Paul for this version: show it, then approve with his exact words")
    # ---------------------------------------------------------------- send
    R.group = "send"
    es = st.get("emails") or {}
    ms = st.get("messages") or {}
    ebad = []
    for e in c["emails"]:
        r = b.routes()["routes"][e["route"]]
        key = "sent" if r["kind"] == "send" else "draft"
        tool = (rc.get("email.%s.created_with" % e["id"]) or "").strip()
        rb = _read(os.path.join(run, w.OUT, "readback_%s.txt" % e["id"]))
        if not (okap and es.get(e["id"], {}).get("ok") and tool in ("outlook_create_draft", "outlook_create_reply_all_draft", "outlook_create_reply_draft", "outlook_send_mail", "outlook_send_draft")
                and (rc.get("email.%s.%s" % (e["id"], key)) or "").strip() and rb is not None and w.sha256_text(rb) == es[e["id"]].get("sha")):
            ebad.append(e["id"])
    R.add(not ebad and okap, ("%d email(s): created with a native Microsoft 365 tool after Paul's yes, id recorded, and the saved item read back equals the checked email" % len(c["emails"])) if c["emails"] else "No email in this run"
          if not ebad and okap else "Email(s) not done or not right: %s" % (", ".join(ebad) or "no valid yes"))
    mbad = []
    for m in c["messages"]:
        s = ms.get(m["id"], {})
        chat_ok = (rc.get("message.%s.chat" % m["id"]) or "").strip() == b.settings()["sitamah"]["chat"]
        fmt_ok = (rc.get("message.%s.format" % m["id"]) or "").strip().lower() == "markdown"
        rb = _read(os.path.join(run, w.OUT, "readback_message_%s.txt" % m["id"]))
        rbp = os.path.join(run, w.OUT, "readback_message_%s.txt" % m["id"])
        if not (okap and s.get("ok") and chat_ok and fmt_ok and rb is not None and w.sha256_file(rbp) == s.get("sha")):
            mbad.append(m["id"])
    greet_ok = all(ms.get(m["id"], {}).get("greeting") for m in c["messages"])
    later_hi = all(ms.get(m["id"], {}).get("greeting") == "Hi" for m in c["messages"][1:])
    R.add(not mbad and okap and greet_ok and later_hi, ("%d message(s) to Sitamah: posted to the 1:1 chat through Zapier in markdown after Paul's yes and the checked emails, greeting from the clock, read back right" % len(c["messages"])) if c["messages"] else "No message to Sitamah in this run"
          if not mbad and okap and greet_ok and later_hi else "Message(s) not done or not right: %s" % (", ".join(mbad) or "greeting or yes"))
    if c["checkin"]:
        R.add(bool((rc.get("checkin.trigger_id") or "").strip()) and okap, "The same-day check-in was created (trigger id recorded)" if rc.get("checkin.trigger_id") else "The same-day check-in is not recorded as created")
    # ---------------------------------------------------------------- publish
    R.group = "publish"
    pub = st.get("publish") or {}
    unreal = []
    if saved:
        unreal = [x["receipt"] for x in c["new_actions"] if not (rc.get(x["receipt"]) or "").strip()]     # actions of earlier runs were proved in their own run
    pok = bool(pub.get("ok")) and bool(pub.get("url")) and bool((rc.get("publish.result") or "").strip()) and (rc.get("publish.forced") or "").lower() != "yes" and not unreal
    R.add(pok, "The board was published in this reply, the page read back is exactly the board the program built, and every new Actions Taken line has its receipt" if pok else
          "The board is not published or not verified%s" % (": actions without receipt: " + ", ".join(unreal) if unreal else ""))
    if stage == "final":
        R.group = "final"
        done = [s for s in STEP_IDS[:-1] if (rj.get("steps", {}).get(s) or {}).get("state") == "done"]
        fpok = rj.get("program_fingerprint") == w.program_fingerprint()
        R.add(done == STEP_IDS[:-1] and fpok, "Every step done in order (%d of %d) and the programs did not change during the run" % (len(done), len(STEP_IDS) - 1) if done == STEP_IDS[:-1] and fpok else
              "Steps done: %s%s" % (", ".join(done) or "none", "; the programs changed during the run" if not fpok else ""))
        R.attested += ["Paul's yes (the words are typed by the chat)", "that the chat really called the Microsoft 365, Zapier and Artifact tools (the program checks what they returned and read back)",
                       "that the evidence lines mean what the bullets say", "that the referral wording matches Paul's Drafts template", "that Paul's signature appears once on every email"]
        if c["base"] == {} or (st.get("base") or {}).get("first"):
            R.attested.append("that no earlier board exists")
        if b.wording()["board_index_line"] and saved and saved.get("closed"):
            R.attested.append(b.wording()["board_index_line"])
    return R, rj


def print_audit(R, rj, stage, run, full=False):
    lines = ["AUDIT   %s" % w.version_line()]
    for mark, short, detail, _g in R.rows:
        lines.append("%s %s" % (mark, short))
    if R.attested:
        lines.append("Only attested (not proven): " + "; ".join(dict.fromkeys(R.attested)) + ".")
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
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    run = os.path.abspath(args[0])
    stage = args[1] if len(args) > 1 and args[1] in ("pre", "final") else "final"
    R, rj = run_checks(run, stage)
    ok = print_audit(R, rj, stage, run, full="--full" in sys.argv)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
