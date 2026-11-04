"""Rebuilds, from the run folder, everything the program is responsible for: the board after the changes, the checked emails, the Sitamah
messages and the follow-up check-in. run.py uses it to build, verify.py uses it to REBUILD and compare, so a file edited by hand cannot pass.
"""
import copy
import os

import board as b
import docread
import wrlib as w


def p(run, name):
    return os.path.join(run, name)


def load_docs(run):
    """(docs.json, {role: Evidence})."""
    docs = w.load_opt(p(run, w.DOCS), {"docs": {}})
    evid = {}
    for role, d in docs["docs"].items():
        try:
            rep = w.load_json(p(run, d["text_file"]))
            evid[role] = docread.Evidence(rep)
        except Exception:
            pass
    return docs, evid


def route_order_problems(log):
    """The routes are tried in order, separately for each purpose: [route names used too early]."""
    bad, failed = [], {}
    for e in log:
        pur = e.get("purpose", "docs")
        if e["route"] not in w.ROUTES:
            continue                                  # the Artifact tool (reading the published board) is not one of the three file routes
        f = failed.setdefault(pur, set())
        i = w.ROUTES.index(e["route"])
        if any(r not in f for r in w.ROUTES[:i]):
            bad.append("%s (%s)" % (e["route"], pur))
        if e["result"] == "failed":
            f.add(e["route"])
    return bad


def compute(run):
    """Everything derived from the run folder. Returns a dict; 'problems' lists everything wrong so far."""
    rj = w.load_json(p(run, w.RUN))
    today = w.parse_date(rj["today"])
    base = w.load_opt(p(run, w.BASE), None)
    change = w.load_opt(p(run, w.CHANGE), None)
    out = {"rj": rj, "today": today, "base": base, "change": change, "problems": [], "email_problems": [], "notify_problems": [],
           "board": None, "log": [], "new_actions": [], "emails": [], "messages": [], "checkin": None}
    if base is None or change is None:
        return out
    docs, evid = load_docs(run)
    ctx = b.Ctx(today, evid, set(docs["docs"]), w.load_opt(p(run, w.RECEIPT), {}), w.load_opt(p(run, w.ACCESS), []))
    out["docs"], out["evid"] = docs, evid
    board, probs, log, acts = b.apply_ops(base, change.get("ops"), ctx)
    out["problems"] = probs
    # ---- the emails the board builds itself
    emails = change.get("emails") or []
    seen = set()
    good = []
    for e in emails:
        if e.get("id") in seen or not e.get("id"):
            out["email_problems"].append("email ids must be present and different")
            continue
        seen.add(e["id"])
        ep = b.email_problems(e, evid, set(docs["docs"]))
        if e.get("card") not in board["cards"] or e.get("card") == "fact_find":
            ep.append("email %s: its card '%s' is not General or a product card on this board" % (e["id"], e.get("card")))
        out["email_problems"] += ep
        if not ep:
            good.append(e)
    if not b.is_empty(board) and not probs and not out["email_problems"]:
        elog, eacts = b.add_email_actions(board, good, today)
        log += elog
        acts += eacts
    out["emails"] = good
    # ---- the messages to Sitamah
    notify = change.get("notify") or []
    need = {}
    for e in good:
        r = b.routes()["routes"][e["route"]]
        if r.get("notify") and not (e["route"] == "quote_request_life" and e.get("revised_quote")):
            need[e["id"]] = r["notify"]
    for n in notify:
        out["notify_problems"] += b.action_slot_problems(n.get("trigger"), n.get("slots"))
    for e in good:
        t = need.get(e["id"])
        if t:
            hit = [n for n in notify if n.get("trigger") == t and (n.get("slots") or {}).get("draft_subject", e["subject"]) == e["subject"]]
            if not hit:
                out["notify_problems"].append("email %s (%s) needs the Sitamah message '%s' with draft_subject exactly the email's subject" % (e["id"], e["route"], t))
    if b.is_empty(board):
        client = ""
    else:
        client = b.client_full(board)
    msgs = []
    if client and not out["notify_problems"]:
        for n in notify:
            msgs.append({"tier": "action", "trigger": n["trigger"], "text": b.render_action(n["trigger"], n.get("slots") or {}, client)})
        covered = {e["id"] for e in good if need.get(e["id"])}
        fy_acts = [a for a in acts if not any(a["receipt"] == "email.%s.%s" % (i, k) for i in covered for k in ("draft", "sent"))]
        bullets = b.fyi_bullets(fy_acts)
        if bullets and change.get("fyi", True) is not False:
            msgs.append({"tier": "fyi", "trigger": "fyi", "text": b.render_fyi(client, bullets)})
    for i, m in enumerate(msgs, 1):
        m["id"] = "m%d" % i
    out["messages"] = msgs
    # ---- the board
    if not b.is_empty(board):
        b.finish_log(board, log, today)
    out["board"], out["log"], out["new_actions"] = board, log, acts
    if any(o.get("op") == "followup" for o in (change.get("ops") or [])):
        out["checkin"] = b.checkin_settings(board)
    return out


def final_board(run, c):
    """The board with the stamp the build recorded (board.json), sealed. None until built."""
    saved = w.load_opt(p(run, w.BOARD), None)
    if saved is None or c["board"] is None:
        return None
    bd = copy.deepcopy(c["board"])
    bd["stamp"] = saved.get("stamp")
    return b.seal(bd)


# ------------------------------------------------------------------ the confirmation table: what Paul's ONE yes is bound to
def confirm_rows(c):
    rows = b.op_lines(c["change"]["ops"], c["board"])
    for e in c["emails"]:
        r = b.routes()["routes"][e["route"]]
        rows.append(("Email %s: %s" % (e["id"], r["label"]), "To %s | Cc %s | Subject: %s" % (", ".join(e["to"]), ", ".join(e["cc"]), e["subject"]),
                     "%s; %s; %s" % (r["lands"], r["sender"], "your yes covers the send" if r["yes_before_send"] else "saved as a draft, nothing is sent")))
    for m in c["messages"]:
        rows.append(("Teams message to Sitamah (%s)" % ("Action needed" if m["tier"] == "action" else "FYI"), m["text"].strip(), "program wording; the greeting is set by the clock when it is sent"))
    if c["checkin"]:
        rows.append(("Same-day check-in (scheduled task)", "%s at %s" % (c["checkin"]["name"], c["checkin"]["at"]), "program settings"))
    rows.append(("Board republished", "%s — Pipeline, in the same reply, only with what has a receipt" % b.client_full(c["board"]), "program page"))
    return rows


def confirm_sha(c):
    return w.content_hash({"ops": c["change"]["ops"], "emails": c["emails"], "messages": [m["text"] for m in c["messages"]], "checkin": c["checkin"], "rows": confirm_rows(c)})
