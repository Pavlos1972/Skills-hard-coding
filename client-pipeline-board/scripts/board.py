"""The model of the client-pipeline-board: the board as ONE data file, the changes the chat enters, the rules on every card, the change log,
the follow-up check-in, the Sitamah messages and the checks on the emails. No client data is kept in this file.

What this module can prove: card shapes and tags, one fact per bullet, word limits, no stage codes, that every Identified point carries a line that
is really in a registered document (and its figures are in that line), that every Actions Taken point has a receipt, that To and Cc are exactly
the table's, that a referral email carries the client's full details block, that the Sitamah messages follow the tier rules.
What it cannot prove (attested): that a document line means what the bullet says, that a send really happened, that the right Outlook thread was found.
"""
import copy
import datetime as dt
import html as _html
import json
import os
import re

import wrlib as w

ASSETS = os.path.join(w.SKILL_DIR, "assets")


def _asset(name):
    return w.load_json(os.path.join(ASSETS, name))


def settings():
    return _asset("settings.json")


def contacts():
    return _asset("contacts.json")


def routes():
    return _asset("routes.json")


def triggers():
    return _asset("triggers.json")


def wording():
    return _asset("wording.json")


def line_ids():
    return list(routes()["lines"].keys())


def card_title(card):
    return {"fact_find": "Fact Find", "general": "General"}.get(card) or routes()["lines"][card]["title"]


def words(text):
    return len(re.findall(r"\S+", str(text or "")))


TAGS = ("New Business", "Servicing")
STATUSES = ("NTU", "Inactive")


# ------------------------------------------------------------------ the board
def new_board():
    return {"schema": 1, "client": None, "created": None, "prospect_log": [], "lines": [],
            "cards": {"fact_find": {"identified": [], "next_appointment": None},
                      "general": {"identified": [], "pending": None, "actions": []}},
            "change_log": [], "closed": None, "stamp": None, "state_sha": None}


def state_sha(board):
    b = copy.deepcopy(board)
    b["state_sha"] = None
    return w.content_hash(b)


def seal(board):
    board["state_sha"] = state_sha(board)
    return board


def is_empty(board):
    return not board or not board.get("client")


def client_full(board):
    c = board["client"]
    return ("%s %s" % (c["first"], c["surname"])).strip()


# ------------------------------------------------------------------ small rule helpers
def _stage_code_re():
    return re.compile(wording()["stage_code_pattern"], re.I)


def text_problems(text, label, limit, jargon=True):
    """Problems with one bullet or question: [str]."""
    out = []
    t = str(text or "").strip()
    if not t:
        return ["%s: the text is empty" % label]
    if words(t) > limit:
        out.append("%s: %d words, the limit is %d (short means short)" % (label, words(t), limit))
    if re.search(r"[.!?](?:\s+)[A-Z0-9]", t) or ";" in t or " and then " in t.lower():
        out.append("%s: more than one fact in one bullet (one fact per bullet)" % label)
    if jargon:
        if _stage_code_re().search(t):
            out.append("%s: shows an internal stage code" % label)
        low = t.lower()
        hit = [j for j in wording()["jargon"] if j in low]
        if hit:
            out.append("%s: internal jargon (%s)" % (label, hit[0]))
    return out


def number_tokens(text):
    return {re.sub(r"\D", "", m) for m in re.findall(r"\d[\d  ,.]*\d|\d", str(text or ""))} - {""}


def identified_problems(b, label, evid, docs_known, limit):
    """One Identified bullet: the text rules and its proof. evid: {role: docread.Evidence}."""
    if not isinstance(b, dict):
        return ["%s: a bullet must be an object with text and its proof" % label]
    out = text_problems(b.get("text"), label, limit)
    ev, pa = b.get("evidence"), (b.get("paul_said") or "").strip()
    if ev:
        role, line = ev.get("doc"), (ev.get("line") or "").strip()
        if role not in docs_known:
            out.append("%s: the document '%s' is not registered for this run" % (label, role))
        elif words(line) < 3 and not number_tokens(line):
            out.append("%s: the evidence line is too short to prove anything" % label)
        else:
            e = evid.get(role)
            if e is None or not e.has_text:
                out.append("%s: '%s' has no readable text, so the program cannot check the line (use paul_said, or read the image yourself and say so)" % (label, role))
            else:
                bad = e.name(label, line)
                if bad:
                    out.append("%s: the evidence line is not in the document's text" % label)
                missing = sorted(number_tokens(b.get("text")) - number_tokens(line))
                if missing:
                    out.append("%s: the figure(s) %s are in the bullet but not in its evidence line" % (label, ", ".join(missing)))
    elif len(pa) >= 5:
        pass
    else:
        out.append("%s: no proof (give the document and a verbatim line, or Paul's own words)" % label)
    pv = b.get("provisional")
    if pv is not None and len(str(pv).strip()) < 5:
        out.append("%s: a provisional point must say why (for example: the box says Yes, the note says client not sure)" % label)
    return out


# ------------------------------------------------------------------ applying the changes the chat entered
class Ctx:
    def __init__(self, today, evid, docs_known, receipts, access):
        self.today, self.evid, self.docs_known, self.receipts, self.access = today, evid, docs_known, receipts, access


def _card(board, card):
    return board["cards"].get(card)


def apply_ops(base, ops, ctx):
    """Apply the entered changes to a copy of the base board. Returns (board, problems [str], log bullets [str], new_actions [dict])."""
    b = copy.deepcopy(base) if not is_empty(base) else new_board()
    lim = settings()["limits"]
    probs, log, new_actions = [], [], []
    today = ctx.today
    if not isinstance(ops, list) or not ops:
        return b, ["no changes were entered: a board is republished only because something changed"], [], []
    for i, op in enumerate(ops, 1):
        who = "change %d" % i
        kind = (op or {}).get("op")
        if kind == "init":
            if not is_empty(b):
                probs.append("%s: the board already exists; 'init' is only for the first run" % who)
                continue
            c = op.get("client") or {}
            if not (c.get("first") and c.get("surname")) or op.get("kind") not in ("prospect", "existing") or len((op.get("paul_said") or "").strip()) < 3:
                probs.append("%s: init needs the client's first name and surname, kind prospect or existing, and Paul's answer (paul_said)" % who)
                continue
            b["client"] = {"first": c["first"].strip(), "surname": c["surname"].strip(), "kind": op["kind"], "paul_said": op["paul_said"].strip()}
            b["created"] = today.strftime("%d/%m/%Y")
            log.append("Board created (%s)" % wording()["prospect_label"][op["kind"]])
            continue
        if is_empty(b):
            probs.append("%s: the board has no client yet; the first change must be 'init'" % who)
            return b, probs, log, new_actions
        if b.get("closed") and kind != "close":
            probs.append("%s: the board is closed (%s); only Paul can reopen it" % (who, b["closed"]["status"]))
            continue
        if kind == "add_line":
            ln = op.get("line")
            if ln not in line_ids():
                probs.append("%s: '%s' is not a product line (%s)" % (who, ln, ", ".join(line_ids())))
            elif ln in b["lines"]:
                probs.append("%s: the %s line already exists" % (who, card_title(ln)))
            else:
                b["lines"].append(ln)
                b["cards"][ln] = {"tag": None, "identified": [], "pending": None, "actions": []}
                log.append("%s: line added" % card_title(ln))
        elif kind == "tag":
            ln = op.get("line")
            if ln not in b["lines"] or not routes()["lines"][ln]["taggable"]:
                probs.append("%s: only Life Cover, Retirement Annuity and Investments lines carry the New Business / Servicing tag" % who)
            elif op.get("tag") not in TAGS or len((op.get("paul_said") or "").strip()) < 5:
                probs.append("%s: the tag must be New Business or Servicing, given by Paul in his own words (paul_said). Never inferred from documents." % who)
            elif b["cards"][ln]["tag"] and b["cards"][ln]["tag"] != op["tag"]:
                probs.append("%s: the %s line is already tagged %s; ask Paul before changing it" % (who, card_title(ln), b["cards"][ln]["tag"]))
            else:
                b["cards"][ln]["tag"] = op["tag"]
                b["cards"][ln]["tag_paul_said"] = op["paul_said"].strip()
                log.append("%s: tagged %s" % (card_title(ln), op["tag"]))
        elif kind == "identified":
            cd = op.get("card")
            if cd not in b["cards"]:
                probs.append("%s: no card '%s' on this board" % (who, cd))
                continue
            bl = op.get("bullets")
            if not isinstance(bl, list) or not bl:
                probs.append("%s: Identified needs at least one bullet" % who)
                continue
            if cd == "general":
                need = settings()["on_file_folders"]
                have = [f for f in need if any(e.get("purpose") == "onfile" and e.get("result") == "found" and w.norm(f) in w.norm(e.get("note", "")) for e in ctx.access)]
                if len(have) < len(need):
                    probs.append("%s: General's list is written only after the on-file check of %s; not logged yet: %s (run.py access --purpose onfile, folder name in the note)" % (
                        who, ", ".join(need), ", ".join(f for f in need if f not in have)))
            for j, bu in enumerate(bl, 1):
                probs += identified_problems(bu, "%s, %s point %d" % (who, card_title(cd), j), ctx.evid, ctx.docs_known, lim["identified_words"])
            b["cards"][cd]["identified"] = bl
            log.append("%s: Identified updated (%d point%s)" % (card_title(cd), len(bl), "" if len(bl) == 1 else "s"))
        elif kind in ("pending", "pending_clear"):
            cd = op.get("card")
            if cd == "fact_find" or cd not in b["cards"]:
                probs.append("%s: a question can sit only on General or a product card" % who)
                continue
            if kind == "pending_clear":
                if not b["cards"][cd]["pending"]:
                    probs.append("%s: %s has no question to clear" % (who, card_title(cd)))
                else:
                    b["cards"][cd]["pending"] = None
                    log.append("%s: question answered" % card_title(cd))
                continue
            t = (op.get("text") or "").strip()
            pp = text_problems(t, "%s, %s question" % (who, card_title(cd)), lim["pending_words"])
            if not t.endswith("?"):
                pp.append("%s, %s question: a question must end with a question mark" % (who, card_title(cd)))
            probs += pp
            if not pp:
                b["cards"][cd]["pending"] = {"kind": "text", "text": t}
                log.append("%s: question for Paul" % card_title(cd))
        elif kind == "action":
            cd = op.get("card")
            if cd == "fact_find" or cd not in b["cards"]:
                probs.append("%s: Actions Taken sits only on General or a product card" % who)
                continue
            t = (op.get("text") or "").strip()
            local = text_problems(t, "%s, %s action" % (who, card_title(cd)), lim["action_words"])
            key = (op.get("receipt") or "").strip()
            via = op.get("via")
            if via and via not in {r.get("skill") for r in routes()["routes"].values() if r.get("skill")}:
                local.append("%s: '%s' is not a skill this board hands over to" % (who, via))
            if not key:
                local.append("%s: an action needs a receipt key (what the tool or skill returned)" % who)
            elif not (ctx.receipts.get(key) or "").strip():
                local.append("%s: receipt '%s' is not recorded; an action is logged only when it really happened (run.py receipt)" % (who, key))
            probs += local
            if not local:
                a = {"text": t, "date": today.strftime("%d/%m/%Y"), "receipt": key}
                if via:
                    a["via"] = via
                b["cards"][cd]["actions"].append(a)
                new_actions.append(dict(a, card=cd))
                log.append("%s: %s" % (card_title(cd), t.rstrip(".")))
        elif kind == "followup":
            d, tm = w.parse_date(op.get("date")), (op.get("time") or "")
            cur = b["cards"]["fact_find"]["next_appointment"]
            ok_time = re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", tm) is not None
            if d is None or d < today or not ok_time:
                probs.append("%s: the follow-up needs a date (DD/MM/YYYY, not in the past) and a time (HH:MM, South African time)" % who)
            elif len((op.get("source") or "").strip()) < 5:
                probs.append("%s: say where the confirmed date came from (the transcript, or Paul's words)" % who)
            elif op.get("via") != "teams-meeting-setup-skill" or not (ctx.receipts.get(op.get("receipt") or "") or "").strip():
                probs.append("%s: the Teams invite is built by teams-meeting-setup-skill; give via and the receipt it returned" % who)
            elif cur and not op.get("reschedule"):
                probs.append("%s: a follow-up date is already recorded (%s); a move is entered with reschedule: true" % (who, cur["date"]))
            elif cur and op.get("reschedule") and not (ctx.receipts.get("checkin.deleted") or "").strip():
                probs.append("%s: a reschedule cancels the old same-day check-in first (receipt checkin.deleted), and the existing invite is updated, never recreated" % who)
            else:
                b["cards"]["fact_find"]["next_appointment"] = {"date": d.strftime("%d/%m/%Y"), "time": tm, "source": op["source"].strip()}
                log.append("Fact Find: next appointment %s %s" % (d.strftime("%d/%m/%Y"), tm))
        elif kind == "prospect_log":
            d, t = w.parse_date(op.get("date")), (op.get("text") or "").strip()
            pp = text_problems(t, "%s, prospect log" % who, lim["prospect_log_words"])
            if d is None or d > today:
                pp.append("%s: the log date must be DD/MM/YYYY and not in the future" % who)
            probs += pp
            if not pp:
                b["prospect_log"].append({"date": d.strftime("%d/%m/%Y"), "text": t})
                log.append("Prospect: %s" % t.rstrip("."))
        elif kind == "close":
            if op.get("status") not in STATUSES or len((op.get("paul_said") or "").strip()) < 5:
                probs.append("%s: closing needs the status NTU or Inactive and Paul's own words (never closed on Claude's own judgment)" % who)
            elif b.get("closed"):
                probs.append("%s: the board is already closed" % who)
            elif not (ctx.receipts.get("closeout.triggers_cancelled") or "").strip():
                probs.append("%s: close-out cancels the client's scheduled check-ins first; record receipt closeout.triggers_cancelled (the ids, or none)" % who)
            else:
                b["closed"] = {"status": op["status"], "date": today.strftime("%d/%m/%Y"), "paul_said": op["paul_said"].strip(), "index": wording()["board_index_line"]}
                log.append("Board closed: %s" % op["status"])
        else:
            probs.append("%s: unknown change '%s'" % (who, kind))
    return b, probs, log, new_actions


def add_email_actions(board, emails, today):
    """The Actions Taken line of each email the chat built: its receipt is the draft id or the sent id, recorded after the yes."""
    log, acts = [], []
    for e in emails:
        cd = e["card"]
        if cd not in board["cards"] or cd == "fact_find":
            continue
        key = "email.%s.%s" % (e["id"], "sent" if routes()["routes"][e["route"]]["kind"] == "send" else "draft")
        a = {"text": e["action_text"].strip(), "date": today.strftime("%d/%m/%Y"), "receipt": key}
        board["cards"][cd]["actions"].append(a)
        acts.append(dict(a, card=cd))
        log.append("%s: %s" % (card_title(cd), a["text"].rstrip(".")))
    return log, acts


def finish_log(board, log, today):
    """One dated entry per republish, newest at the top."""
    seen, bullets = set(), []
    for x in log:
        if x not in seen:
            seen.add(x)
            bullets.append(x)
    if bullets:
        board["change_log"].insert(0, {"date": today.strftime("%d/%m/%Y"), "bullets": bullets})


# ------------------------------------------------------------------ rules on the finished board
def board_problems(board, today):
    """[(ok, short, detail)] on the finished board (the program re-runs this on the rebuilt board)."""
    R = []
    lim = settings()["limits"]

    def add(ok, short, detail=""):
        R.append((bool(ok), short, detail))
    if is_empty(board):
        return [(False, "The board has no client", "")]
    tagless = [card_title(ln) for ln in board["lines"] if routes()["lines"][ln]["taggable"] and not board["cards"][ln].get("tag")]
    wrong = [card_title(ln) for ln in board["lines"] if not routes()["lines"][ln]["taggable"] and board["cards"][ln].get("tag")]
    add(not tagless and not wrong, "The New Business / Servicing tag shows on Life Cover, RA and Investments only, and every one of those has it" if not (tagless or wrong) else
        "Tag problem: %s" % ("missing on " + ", ".join(tagless) if tagless else "wrongly on " + ", ".join(wrong)))
    ff = board["cards"]["fact_find"]
    add(set(ff) <= {"identified", "next_appointment"}, "The Fact Find card holds Identified only (and the next appointment)")
    bad = []
    for cd in ["general"] + board["lines"]:
        c = board["cards"][cd]
        if c.get("pending") and (c["pending"].get("kind") != "text" or not c["pending"].get("text")):
            bad.append(card_title(cd))
    add(not bad, "Every pending question is plain text, at most one per card" if not bad else "Pending problem on %s" % ", ".join(bad))
    allb = []
    for cd in ["fact_find", "general"] + board["lines"]:
        c = board["cards"][cd]
        allb += [("%s Identified" % card_title(cd), x.get("text"), lim["identified_words"]) for x in c.get("identified", [])]
        allb += [("%s Actions Taken" % card_title(cd), x.get("text"), lim["action_words"]) for x in c.get("actions", [])]
    probs = []
    for lab, t, limit in allb:
        probs += text_problems(t, lab, limit)
    add(not probs, "Every bullet is short, one fact, with no stage codes or internal words (%d checked)" % len(allb) if not probs else "Bullet problem: %s" % probs[0], "; ".join(probs))
    noproof = [x for cd in ["fact_find", "general"] + board["lines"] for x in board["cards"][cd].get("identified", []) if not (x.get("evidence") or (x.get("paul_said") or "").strip())]
    add(not noproof, "Every Identified point carries its proof (a document line, or Paul's words)" if not noproof else "%d Identified point(s) have no proof" % len(noproof))
    noreceipt = [x for cd in ["general"] + board["lines"] for x in board["cards"][cd].get("actions", []) if not x.get("receipt")]
    add(not noreceipt, "Every Actions Taken point names its receipt" if not noreceipt else "%d action(s) have no receipt" % len(noreceipt))
    cl = board["change_log"]
    dates = [w.parse_date(e["date"]) for e in cl]
    add(bool(cl) and cl[0]["date"] == today.strftime("%d/%m/%Y") and cl[0]["bullets"] and all(dates) and dates == sorted(dates, reverse=True),
        "The Change Log has today's entry at the top, newest first (%d entr%s)" % (len(cl), "y" if len(cl) == 1 else "ies") if cl else "The Change Log is empty")
    return R


# ------------------------------------------------------------------ the follow-up check-in (a scheduled task the chat creates)
def checkin_settings(board):
    """The exact settings of the same-day check-in, or None when no follow-up date is recorded."""
    na = board["cards"]["fact_find"]["next_appointment"] if not is_empty(board) else None
    if not na:
        return None
    d = w.parse_date(na["date"])
    at = "%sT%s:00[Africa/Johannesburg]" % (d.strftime("%Y-%m-%d"), settings()["checkin"]["time_sast"])
    name = "Check-in: %s follow-up %s" % (client_full(board), na["date"])
    msg = ("Check Paul's Outlook calendar (outlook_calendar_search) for %s's follow-up Teams meeting today at %s SAST. Is it still on, and has the client accepted? "
           "If confirmed, tell Paul in one short line: 'Confirmed - %s at %s today; upload the transcript once it is done.' "
           "If it was moved or not accepted, say so plainly and ask Paul; do not assume it happened. If you can reach Sitamah's Teams chat only after Paul's yes, do not message her yourself."
           % (client_full(board), na["time"], client_full(board), na["time"]))
    return {"name": name, "at": at, "message": msg, "initiation": "own_followup"}


# ------------------------------------------------------------------ the Sitamah messages
GREETING_MARK = "<greeting by the clock>"


def greeting_for(clock, used_today):
    if used_today:
        return "Hi"
    return "Good morning" if clock.hour < 12 else ("Good afternoon" if clock.hour < 18 else "Good evening")


def _fill(line, slots, client):
    def rep(m):
        k = m.group(1)
        return client if k == "client" else str(slots.get(k, ""))
    return re.sub(r"\{(\w+)\}", rep, line)


def action_slot_problems(tid, slots):
    t = triggers()["action"].get(tid)
    if not t:
        return ["'%s' is not a message on the list (%s)" % (tid, ", ".join(triggers()["action"]))]
    out = []
    slots = slots or {}
    for k in t["slots"]:
        v = slots.get(k)
        if k in ("outstanding",):
            if not isinstance(v, list) or not v or not all(isinstance(x, str) and x.strip() for x in v):
                out.append("%s: '%s' must be a list of lines naming the contact and what is outstanding" % (tid, k))
        elif not isinstance(v, str) or not v.strip():
            out.append("%s: the detail '%s' is missing" % (tid, k))
    extra = sorted(set(slots) - set(t["slots"]))
    if extra:
        out.append("%s: unknown detail(s) %s" % (tid, ", ".join(extra)))
    return out


def render_action(tid, slots, client):
    t = triggers()["action"][tid]
    lines = ["%s Sitamah, %s." % (GREETING_MARK, triggers()["identity"]), "", "**Action needed:** " + _fill(t["summary"], slots, client), ""]
    for ln in t["body"]:
        m = re.fullmatch(r"\{@(\w+)\}", ln)
        if m:
            lines += ["- " + str(x).strip() for x in slots[m.group(1)]]
        else:
            lines.append(_fill(ln, slots, client))
    return "\n".join(lines).rstrip() + "\n"


def render_fyi(client, bullets):
    f = triggers()["fyi"]
    lines = ["%s Sitamah, %s %s" % (GREETING_MARK, triggers()["identity"] + ",", _fill(f["intro"], {}, client)), ""]
    lines += ["- " + b.rstrip(".") for b in bullets]
    lines += ["", f["closing"]]
    return "\n".join(lines) + "\n"


def fyi_bullets(new_actions, board_card_titles=True):
    """The FYI message covers ordinary Actions Taken of this run, except those a product skill already told her about itself."""
    own = {r["skill"] for r in routes()["routes"].values() if r.get("own_message")}
    out = []
    for a in new_actions:
        if a.get("via") in own:
            continue
        out.append("%s: %s" % (card_title(a["card"]), a["text"]))
    return out


def plain(text):
    t = re.sub(r"(?i)<br\s*/?>|</p>|</li>|</ol>|</ul>", "\n", str(text))
    t = re.sub(r"<[^>]+>", "", t)
    return _html.unescape(t).replace("**", "")


def message_problems(readback, expected, tier, greeting):
    """Checks on the saved read-back of a posted Teams message: [(ok, short)]."""
    flat, _o, leaves = flatten(readback)
    cands = [x for x in leaves if "Sitamah" in x]
    body = max(cands, key=len) if cands else flat
    exp = expected.replace(GREETING_MARK, greeting)
    R = []

    def add(ok, short):
        R.append((bool(ok), short))
    pt = plain(body)
    add(w.norm(plain(exp)) in w.norm(pt), "The posted message carries the wording the program built, word for word")
    add(pt.lstrip().startswith("%s Sitamah," % greeting), "It opens with the greeting '%s Sitamah,' and says it is Claude" % greeting)
    if tier == "action":
        add("<strong>Action needed:</strong>" in body, "'Action needed:' is real bold, first after the greeting")
    else:
        add("Action needed" not in pt and pt.rstrip().endswith(triggers()["fyi"]["closing"]), "It is an FYI: no tag, and it ends 'Nothing needed from you.'")
    add("**" not in body and "&lt;" not in body and "\\u003c" not in body, "No literal ** and no escaped tags show")
    return R


# ------------------------------------------------------------------ the emails the board builds itself
PLACEHOLDER = re.compile(r"\[[A-Z][A-Z0-9 %().,/&#-]*\]|\{\{|@@|\bTODO\b|lorem ipsum", re.I)
EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")


def flatten(text):
    try:
        obj = json.loads(text)
    except ValueError:
        return text, None, [text]
    out = []

    def walk(o):
        if isinstance(o, dict):
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
        elif isinstance(o, str):
            out.append(o)
    walk(obj)
    return "\n".join(out), obj, out


def find_key(obj, names):
    names = {n.lower() for n in names}
    found = []

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k.lower() in names:
                    found.append(v)
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(obj)
    return found


def _emails(x):
    return {e.lower() for e in re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", json.dumps(x))}


def expected_recipients(route_id, client_email, extra_to=None):
    """(To set, Cc set) for a route, as lower-case addresses."""
    r = routes()["routes"][route_id]
    c = contacts()

    def one(x):
        return client_email.lower() if x == "client" else c[x]["email"].lower()
    to = {one(x) for x in r["to"] if x != "*"} | {a.lower() for a in (extra_to or [])}
    cc = {one(x) for x in r["cc"]}
    return to, cc


def email_problems(e, evid, docs_known):
    """Everything checkable about one email the chat built: [str]. Wording stays in Paul's Drafts templates (attested)."""
    out = []
    rid = e.get("route")
    r = routes()["routes"].get(rid)
    if not r or r["kind"] not in ("draft", "send"):
        return ["email %s: '%s' is not an email route this board builds (delegated skills send their own)" % (e.get("id"), rid)]
    tag = "email %s (%s)" % (e.get("id"), rid)
    if r["ask_first"] and len(((e.get("asked_paul") or "")).strip()) < 5:
        out.append("%s: Paul decides this one BEFORE it is built; record his words (asked_paul)" % tag)
    cl = e.get("client_details") or {}
    cemail = (cl.get("email") or "").strip()
    if "client" in r["to"] + r["cc"] and not EMAIL_RE.match(cemail):
        out.append("%s: the client's email is needed (client_details.email)" % tag)
    to_exp, cc_exp = expected_recipients(rid, cemail or "x@x.x", e.get("extra_to"))
    to_got = {a.lower() for a in e.get("to", [])}
    cc_got = {a.lower() for a in e.get("cc", [])}
    if r["to"] == ["*"]:
        ok_to = bool(to_got) and all(EMAIL_RE.match(a) for a in to_got) and settings()["sitamah"]["email"].lower() not in to_got
    else:
        ok_to = to_got == to_exp
    if not ok_to:
        out.append("%s: To is %s; the table says %s" % (tag, sorted(to_got), sorted(to_exp) if r["to"] != ["*"] else "the named contact (never Sitamah)"))
    if cc_got != cc_exp:
        out.append("%s: Cc is %s; the table says exactly %s" % (tag, sorted(cc_got), sorted(cc_exp)))
    subj = (e.get("subject") or "").strip()
    if not subj:
        out.append("%s: the subject is empty" % tag)
    if "no_bracket_subject" in r["checks"] and re.match(r"^\s*\[[^\]]+\]", subj):
        out.append("%s: the subject carries a bracket tag; that belongs only on the saved template, never on a real draft" % tag)
    body_html = e.get("body_html") or ""
    text = plain(body_html)
    low = text.lower()
    if words(text) < 15:
        out.append("%s: the body is too short to be an email" % tag)
    if any(s in low for s in wording()["sign_offs"]):
        out.append("%s: the body types a sign-off; the Exchange rule adds Paul's signature once (paul-email-signature)" % tag)
    if PLACEHOLDER.search(body_html):
        out.append("%s: a placeholder is left in the body" % tag)
    if re.search(r"(?i)\b(%s)\b" % "|".join(wording()["client_forbidden"]), text) or re.search(r"\b\d{1,2}(?::\d{2})?\s?(?:am|pm)?\s*\(\d{1,2}(?::\d{2})?\s?(?:am|pm)?\)", text):
        out.append("%s: it shows Paul's Greek location or a bracketed Greek time; nothing a client or provider sees may" % tag)
    if "thread" in r["checks"]:
        th = e.get("thread") or {}
        if not ((th.get("reply_all_to") or "").strip() or len((th.get("none_found") or "").strip()) >= 10):
            out.append("%s: a request to a provider contact is a reply to the latest thread: give thread.reply_all_to (the message id) or thread.none_found (what you searched)" % tag)
    if "ff_summary_line" in r["checks"] and not e.get("revised_quote"):
        line = wording()["ff_summary_line"]
        paras = [x.strip() for x in re.split(r"\n\s*\n|\n", text) if x.strip()]
        idx = [i for i, p_ in enumerate(paras) if p_ == line]
        if len(idx) != 1 or idx[0] < len(paras) - 2:
            out.append("%s: the line '%s' must appear exactly once, immediately before the closing urgency sentence" % (tag, line))
    for att in e.get("attach") or []:
        prefix = "%s %s" % (wording()["attach_before_sending_prefix"], att.get("name", ""))
        if prefix.lower() not in low:
            out.append("%s: the body must say '%s ...' for %s" % (tag, wording()["attach_before_sending_prefix"], att.get("name")))
    if "details_block" in r["checks"]:
        keys = {"Name": cl.get("name"), "ID number": cl.get("id_number"), "Cell number": cl.get("cell"), "Email": cl.get("email")}
        miss = [k for k, v in keys.items() if not (v or "").strip()]
        if miss:
            out.append("%s: the client's details block needs %s (never the ID number alone)" % (tag, ", ".join(miss)))
        else:
            if len(w.digits(cl["id_number"])) != 13:
                out.append("%s: the ID number is not 13 digits" % tag)
            if len(w.digits(cl["cell"])) < 9:
                out.append("%s: the cell number looks too short" % tag)
            dg = w.digits(text)
            for k, v in keys.items():
                present = (w.digits(v) in dg) if k in ("ID number", "Cell number") else (w.norm(v) in w.norm(text))
                if not present:
                    out.append("%s: the body does not show the client's %s" % (tag, k.lower()))
            proofs = cl.get("evidence") or {}
            for k, v in keys.items():
                role = proofs.get(k)
                ev = evid.get(role) if role in docs_known else None
                if ev is None:
                    out.append("%s: %s has no registered document as its source" % (tag, k.lower()))
                elif k in ("ID number", "Cell number"):
                    if w.digits(v) not in w.digits(ev.text):
                        out.append("%s: the client's %s is not in the document's text" % (tag, k.lower()))
                elif ev.name(k, v):
                    out.append("%s: the client's %s is not in the document's text" % (tag, k.lower()))
    if not (e.get("action_text") or "").strip():
        out.append("%s: give the Actions Taken line (action_text) to log once it is done" % tag)
    else:
        out += text_problems(e["action_text"], tag + " action_text", settings()["limits"]["action_words"])
    return out


def readback_problems(text, e):
    """The saved draft or sent item read back from Outlook against the email the program checked: [(ok, short)]."""
    flat, obj, leaves = flatten(text)
    R = []

    def add(ok, short):
        R.append((bool(ok), short))
    to_v = find_key(obj, ("toRecipients", "to")) if obj is not None else []
    cc_v = find_key(obj, ("ccRecipients", "cc")) if obj is not None else []
    to_exp = {a.lower() for a in e["to"]}
    cc_exp = {a.lower() for a in e["cc"]}
    if to_v or cc_v:
        to_set = set().union(*[_emails(x) for x in to_v]) if to_v else set()
        cc_set = set().union(*[_emails(x) for x in cc_v]) if cc_v else set()
        add(to_set == to_exp and cc_set == cc_exp, "To and Cc read back from Outlook equal the checked email")
    else:
        add(all(a in flat.lower() for a in to_exp | cc_exp), "Every To and Cc address is on the saved item (the read-back has no separate fields)")
    subs = [x for x in (find_key(obj, ("subject",)) if obj is not None else []) if isinstance(x, str)]
    add((e["subject"].strip() in subs) if subs else (e["subject"].strip() in flat), "The subject read back is exactly the checked subject")
    add(not re.match(r"^\s*\[[^\]]+\]", (subs[0] if subs else e["subject"])), "No bracket tag on the real subject")
    return R


# ------------------------------------------------------------------ the confirmation table (what Paul's one yes is bound to)
def op_lines(ops, board):
    out = []
    for op in ops:
        k = op.get("op")
        if k == "init":
            out.append(("Create the board", "%s (%s)" % ("%s %s" % (op["client"]["first"], op["client"]["surname"]), wording()["prospect_label"].get(op.get("kind"), "?")), "Paul: %s" % op.get("paul_said")))
        elif k == "add_line":
            out.append(("New product line", card_title(op["line"]), "Fact Find"))
        elif k == "tag":
            out.append(("%s tag" % card_title(op["line"]), op["tag"], "Paul: %s" % op.get("paul_said")))
        elif k == "identified":
            for b_ in op["bullets"]:
                src = ("%s: \"%s\"" % (b_["evidence"]["doc"], b_["evidence"]["line"])) if b_.get("evidence") else "Paul: %s" % b_.get("paul_said")
                out.append(("%s Identified%s" % (card_title(op["card"]), " (provisional)" if b_.get("provisional") else ""), b_["text"], src))
        elif k == "pending":
            out.append(("%s question for Paul" % card_title(op["card"]), op["text"], "the chat"))
        elif k == "pending_clear":
            out.append(("%s question answered" % card_title(op["card"]), "removed", "Paul"))
        elif k == "action":
            out.append(("%s Actions Taken" % card_title(op["card"]), op["text"], "receipt %s" % op.get("receipt")))
        elif k == "followup":
            out.append(("Next appointment", "%s %s SAST%s" % (op["date"], op["time"], " (moved)" if op.get("reschedule") else ""), op.get("source")))
        elif k == "prospect_log":
            out.append(("Prospect log", "%s: %s" % (op["date"], op["text"]), "the chat"))
        elif k == "close":
            out.append(("Close the board", op["status"], "Paul: %s" % op.get("paul_said")))
    return out
