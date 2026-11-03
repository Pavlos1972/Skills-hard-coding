#!/usr/bin/env python3
"""Builds the follow-up Teams meeting invite, exactly, from facts that were recorded with their source.

A pure function: the same facts always give the same payload, so the checker can rebuild it and refuse a payload that was edited by hand.
The invite is a REAL SEND (creating the event with the client as attendee emails them at once), so everything here is fixed by rule (Paul):
  subject    `{Client Name} / {topics}`: short labels only, in the fixed order, joined naturally;
  time zone  Africa/Johannesburg on start and end (SAST, no daylight saving);
  duration   exactly 1 hour;
  attendee   the client only, from the Fact Find; never Sitamah, never Paul;
  Teams      isOnlineMeeting true (Microsoft makes the real link; never a hand-written link, meeting ID or passcode);
  body       HTML with a blank line between paragraphs, no hand-typed signature (an Exchange rule adds Paul's signature).
"""
import datetime as dt
import hashlib
import re
from xml.sax.saxutils import escape

import wrlib as w

# Product line -> (short label for the subject, plain client wording for the agenda). The ORDER is the subject's order.
LINES = [("Risk", "Your life cover quote"), ("RA", "Your Retirement Annuity"), ("Investments", "Your investments"), ("RGAR", "Your retirement goal analysis"),
         ("EGAR", "Your education goal analysis"), ("Medical Aid", "Your medical aid and gap cover"), ("Will", "Your will"), ("STI", "Your short-term insurance")]
LABELS = [l for l, _ in LINES]
PLAIN = dict(LINES)
EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$")
FORBIDDEN_IN_BODY = ("http", "teams.microsoft.com", "meeting id", "passcode", "kind regards", "regards,", "best regards", "wealth revolution")
GREETINGS = ("Hey Sitamah!", "Hi Sitamah, quick one for you.", "Hope your day's going well, Sitamah.")


def subject_topics(topics):
    """Labels in the fixed order, joined naturally: 'RA', 'Risk & RA', 'Risk, RA & RGAR'."""
    ordered = [l for l in LABELS if l in topics]
    if len(ordered) == 1:
        return ordered[0]
    return ", ".join(ordered[:-1]) + " & " + ordered[-1] if len(ordered) > 2 else " & ".join(ordered)


def topic_problems(topics):
    out = []
    unknown = [t for t in topics if t not in LABELS]
    if unknown:
        out.append("unknown topic(s) %s: the labels are %s" % (", ".join(unknown), ", ".join(LABELS)))
    if len(set(topics)) != len(topics):
        out.append("a topic is listed twice")
    if not topics:
        out.append("no topic: list the product lines that are open for this client")
    return out


def opening_line(last_contact, contact, today):
    """Date-aware and accurate: 'met' for a Teams or video appointment, 'spoke' only when the last contact was a phone or WhatsApp call."""
    verb = "met with" if contact == "met" else "spoken with"
    gap = (today - last_contact).days
    if gap == 0:
        return "Great to have %s you earlier today." % verb
    if gap == 1:
        return "Great to have %s you yesterday." % verb
    return "Great to have %s you on %s." % (verb, last_contact.strftime("%d/%m/%Y"))


def agenda_lines(facts):
    custom = facts.get("agenda")
    return list(custom) if custom else [PLAIN[l] for l in LABELS if l in facts["topics"]]


def body_html(client, facts, today):
    last = w.parse_date(facts["last_contact"])
    parts = ["Hi %s," % escape(client["first"]), opening_line(last, facts["contact"], today),
             "As discussed, kindly accept the above Teams meeting request.",
             "On the agenda:<br>" + "<br>".join("- " + escape(a) for a in agenda_lines(facts))]
    if facts.get("needs"):
        parts.append("What we need from you before then:<br>" + "<br>".join("- " + escape(n) for n in facts["needs"]))
    parts.append("Below is the link to join the Teams meeting on %s." % facts["date"])
    return "<br><br>".join(parts)


def window(facts):
    start = dt.datetime.strptime("%s %s" % (facts["date"], facts["time"]), "%d/%m/%Y %H:%M")
    return start, start + dt.timedelta(hours=1)


def fmt_local(d):
    return d.strftime("%Y-%m-%dT%H:%M:00")


def build_payload(client, facts, mode, event_id, today):
    """The exact arguments for outlook_create_event (new) or outlook_update_event (reschedule)."""
    start, end = window(facts)
    when = {"start": {"dateTime": fmt_local(start), "timeZone": w.TZ}, "end": {"dateTime": fmt_local(end), "timeZone": w.TZ}}
    if mode == "reschedule":
        return dict(eventId=event_id, **when)                       # the existing event is updated in place; never deleted and recreated
    name = "%s %s" % (client["first"], client["surname"])
    return {"subject": "%s / %s" % (name, subject_topics(facts["topics"])), **when, "body": body_html(client, facts, today), "bodyType": "html",
            "attendees": [{"email": client["email"], "name": name, "type": "required"}], "isOnlineMeeting": True, "responseRequested": True}


def fact_problems(facts, today):
    """Problems with the recorded facts (empty = fine)."""
    out = []
    d = w.parse_date(facts.get("date"))
    if d is None:
        out.append("the follow-up date %r is not a real date (DD/MM/YYYY)" % facts.get("date"))
    elif d < today:
        out.append("the follow-up date %s is in the past" % facts["date"])
    if not re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", facts.get("time") or ""):
        out.append("the time %r is not HH:MM (24-hour, South African time)" % facts.get("time"))
    if len((facts.get("source") or "").strip()) < 8:
        out.append("say where the date, time and topics came from (--source, at least 8 characters)")
    if facts.get("mode") == "new":
        lc = w.parse_date(facts.get("last_contact"))
        if lc is None:
            out.append("the last contact date %r is not a real date (DD/MM/YYYY)" % facts.get("last_contact"))
        elif lc > today:
            out.append("the last contact %s is in the future" % facts["last_contact"])
        elif d and d <= lc:
            out.append("the follow-up date %s is not after the last contact %s" % (facts["date"], facts["last_contact"]))
        if facts.get("contact") not in ("met", "spoke"):
            out.append("--contact must be met (a Teams or video appointment) or spoke (a phone or WhatsApp call)")
        out += topic_problems(facts.get("topics") or [])
        if facts.get("needs") and len((facts.get("needs_source") or "").strip()) < 8:
            out.append("the 'what we need from you' items need their source (--needs-source): never invent an item")
        n = len(agenda_lines(facts)) if not topic_problems(facts.get("topics") or []) else 0
        if n > 5:
            out.append("%d agenda lines: at most 5 (give --agenda with up to 5 short lines in plain client words)" % n)
    return out


def sitamah_text(client, facts, mode):
    """An FYI message (the board's rule: no tag, ends with 'nothing needed from you'). Time-neutral greeting, so no clock check is needed."""
    name = "%s %s" % (client["first"], client["surname"])
    g = GREETINGS[int(hashlib.sha256((name + facts["date"]).encode()).hexdigest()[:2], 16) % len(GREETINGS)]
    when = "%s at %s SAST (1 hour)" % (facts["date"], facts["time"])
    if mode == "reschedule":
        return ("%s Claude here. Just moved %s's follow-up Teams meeting:\n- Now: %s\n- The client's invite has been updated in place (not re-sent)\n\n"
                "Nothing needed from you right now — just keeping you posted." % (g, name, when))
    return ("%s Claude here. Just sent %s's follow-up Teams meeting invite:\n- When: %s\n- Covering: %s\n- To: %s (%s)\n\n"
            "Nothing needed from you right now — just keeping you posted." % (g, name, when, subject_topics(facts["topics"]), name, client["email"]))


def log_lines(client, facts, mode, payload):
    name = "%s %s" % (client["first"], client["surname"])
    when = "%s at %s SAST (1 hour)" % (facts["date"], facts["time"])
    head = "Teams follow-up meeting moved" if mode == "reschedule" else "Teams follow-up meeting invite sent: %s" % payload["subject"]
    return ["- " + head, "- " + when, "- Attendee: %s (%s)" % (name, client["email"])]


def invite_text(client, facts, mode, payload, today):
    """The invite in plain words, for Paul (what the client will receive)."""
    start, end = window(facts)
    lines = ["%s" % ("RESCHEDULE of the existing invite" if mode == "reschedule" else "NEW Teams meeting invite (a real send: the client is emailed at once)"),
             "Date and time: %s, %s to %s SAST (1 hour)" % (start.strftime("%A %d/%m/%Y"), start.strftime("%H:%M"), end.strftime("%H:%M"))]
    if mode == "reschedule":
        lines.append("Event: %s (updated in place; the client's invite changes, nothing is deleted)" % payload["eventId"])
        lines.append("Note: the body of the invite is not changed, so its closing line still names the old date.")
        return "\n".join(lines)
    body = payload["body"].replace("<br><br>", "\n\n").replace("<br>", "\n")
    lines += ["Subject: %s" % payload["subject"], "To: %s <%s> (the client only)" % (client["first"] + " " + client["surname"], client["email"]),
              "Microsoft makes the Teams link and adds it under the text below; Paul's signature is added by the Exchange rule.", "", "BODY:", body]
    return "\n".join(lines)


def payload_sha(payload):
    import json
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def payload_problems(client, facts, mode, event_id, payload, today):
    """Every rule checked on a payload (empty = fine). The checker also compares it with a rebuild."""
    out = []
    keys = {"eventId", "start", "end"} if mode == "reschedule" else {"subject", "start", "end", "body", "bodyType", "attendees", "isOnlineMeeting", "responseRequested"}
    if set(payload) != keys:
        out.append("the payload has the wrong fields: %s" % sorted(set(payload) ^ keys))
    for k in ("start", "end"):
        if (payload.get(k) or {}).get("timeZone") != w.TZ:
            out.append("%s.timeZone must be %s" % (k, w.TZ))
    try:
        s = dt.datetime.strptime(payload["start"]["dateTime"], "%Y-%m-%dT%H:%M:%S")
        e = dt.datetime.strptime(payload["end"]["dateTime"], "%Y-%m-%dT%H:%M:%S")
        if e - s != dt.timedelta(hours=1):
            out.append("the duration must be exactly 1 hour")
    except (KeyError, ValueError):
        out.append("start and end must be local date-times")
    if mode == "reschedule":
        if payload.get("eventId") != event_id:
            out.append("eventId must be the existing event's id")
        return out
    if payload.get("subject") != "%s %s / %s" % (client["first"], client["surname"], subject_topics(facts["topics"])):
        out.append("the subject must be `Client Name / topics` in the fixed order")
    att = payload.get("attendees") or []
    if len(att) != 1 or att[0].get("email") != client["email"] or att[0].get("type") != "required":
        out.append("the only attendee must be the client (%s), type required" % client["email"])
    elif att[0]["email"].lower().endswith("@" + w.FIRM_DOMAIN):
        out.append("the attendee is on the firm's own domain: that is Paul or Sitamah, never the client")
    if payload.get("isOnlineMeeting") is not True:
        out.append("isOnlineMeeting must be true")
    if payload.get("bodyType") != "html":
        out.append("bodyType must be html")
    if payload.get("responseRequested") is not True:
        out.append("responseRequested must be true")
    body = payload.get("body") or ""
    low = body.lower()
    bad = [f for f in FORBIDDEN_IN_BODY if f in low]
    if bad:
        out.append("the body must not contain a link, meeting ID, passcode or signature: found %s" % ", ".join(bad))
    if body != body_html(client, facts, today):
        out.append("the body is not what the rules build from the facts")
    return out
