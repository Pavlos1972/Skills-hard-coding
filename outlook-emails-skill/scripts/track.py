#!/usr/bin/env python3
"""Builds the reply-tracking plan, exactly, from facts that were recorded with their source.

A pure function: the same facts and the same day always give the same plan, so the checker can rebuild it and refuse a plan that was edited
by hand. Fixed by Paul's answers (03/11/2026):
  the watcher     every hour on weekdays 08:00 to 17:00 South African time; a sender who replied is dropped from its list; it stops for good
                  at 17:00 on the 5th business day after sending, with one last message, and deletes itself;
  the flag        once, 09:00 Athens time on the 2nd business day after sending (never in the past), a phone alert if anyone is outstanding;
  both            run as a fresh chat each time (so the phone alert works), may use the Microsoft 365 connector and nothing else, never depend on
                  read/unread, and report a failed search as a failure, never as "no reply".
Weekends are skipped; public holidays are not (a known limit).
"""
import datetime as dt
import hashlib
import re

import wrlib as w

EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$")
CRON = "CRON_TZ=%s 0 8-17 * * 1-5" % w.TZ_SA
WATCH_BUSINESS_DAYS = 5
FLAG_BUSINESS_DAYS = 2
NOT_GENUINE = ("automatic replies", "out-of-office messages", "delivery failures or bounces", "read receipts",
               "'we have received your email' acknowledgements that give no answer")


# ------------------------------------------------------------------ dates
def add_business_days(d, n):
    """The date n business days after d (Saturdays and Sundays skipped; public holidays are not)."""
    while n > 0:
        d += dt.timedelta(days=1)
        if d.weekday() < 5:
            n -= 1
    return d


def next_business_day(d):
    return add_business_days(d, 1)


def _last_sunday(year, month):
    d = dt.date(year, month + 1, 1) - dt.timedelta(days=1) if month < 12 else dt.date(year, 12, 31)
    return d - dt.timedelta(days=(d.weekday() + 1) % 7)


def athens_offset_hours(d):
    """Athens at 09:00 local: +3 (summer time) from the last Sunday of March to the day before the last Sunday of October, else +2."""
    return 3 if _last_sunday(d.year, 3) <= d < _last_sunday(d.year, 10) else 2


def athens_0900(d):
    """09:00 Athens time on date d as an RFC3339 string (no time-zone database needed)."""
    return "%sT09:00:00+%02d:00" % (d.isoformat(), athens_offset_hours(d))


def instant(text):
    """An RFC3339 text as an aware datetime (None if it is not one)."""
    try:
        return dt.datetime.fromisoformat((text or "").strip().replace("Z", "+00:00").replace(" ", "T", 1))
    except ValueError:
        return None


# ------------------------------------------------------------------ the facts
def fact_problems(facts, today):
    """Problems with the recorded facts (empty = fine)."""
    out = []
    senders = facts.get("senders") or []
    if not senders:
        out.append("no sender: give the address(es) a reply is expected from (--senders)")
    for s in senders:
        if not EMAIL.match(s):
            out.append("%r is not a real email address" % s)
        elif s.lower() == w.OWN_MAILBOX:
            out.append("%s is Paul's own mailbox: never a sender to wait for" % s)
    if len({s.lower() for s in senders}) != len(senders):
        out.append("a sender is listed twice")
    if len((facts.get("subject") or "").strip()) < 3:
        out.append("give the subject of the email (--subject)")
    sent = w.parse_date(facts.get("sent"))
    if sent is None:
        out.append("the date sent %r is not a real date (DD/MM/YYYY)" % facts.get("sent"))
    elif sent > today:
        out.append("the date sent %s is in the future: for a draft Paul has not sent yet, give today's date" % facts["sent"])
    elif add_business_days(sent, WATCH_BUSINESS_DAYS) < today:
        out.append("the email was sent %s: the %d business days of watching are already over, so there is nothing to set up. Ask Paul." % (facts["sent"], WATCH_BUSINESS_DAYS))
    if len((facts.get("why") or "").strip()) < 8:
        out.append("say why a reply is needed (--why, at least 8 characters): without a reason the email does not need tracking")
    if len((facts.get("source") or "").strip()) < 8:
        out.append("say where the sender, subject and date came from (--source, at least 8 characters)")
    return out


# ------------------------------------------------------------------ the plan
def dates(facts, today):
    sent = w.parse_date(facts["sent"])
    stop = add_business_days(sent, WATCH_BUSINESS_DAYS)
    flag = add_business_days(sent, FLAG_BUSINESS_DAYS)
    if flag <= today:                        # the flag is never in the past: the next business day after today
        flag = next_business_day(today)
    return sent, stop, flag


def ident(facts):
    key = "|".join([facts["subject"].strip(), facts["sent"]] + sorted(s.lower() for s in facts["senders"]))
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:6]


def task_names(facts):
    short = re.sub(r"\s+", " ", facts["subject"].strip())[:40].strip()
    tag = "%s %s" % (w.short_date(facts["sent"]), ident(facts))
    return "Reply watch: %s (%s)" % (short, tag), "Reply flag: %s (%s)" % (short, tag)


def _head(facts):
    lines = ["- Subject: %s" % facts["subject"].strip(), "- Sent: %s (South African date)" % facts["sent"], "- Why a reply is needed: %s" % facts["why"].strip()]
    if facts.get("folder"):
        lines.append("- Client folder (OneDrive/SharePoint): %s" % facts["folder"].strip())
    return lines


def genuine_text():
    return ("A GENUINE reply is a message from that sender that answers or acts on the request. These are NOT genuine replies: %s." % ", ".join(NOT_GENUINE))


def watch_prompt(facts, name, stop):
    return "\n".join([
        "You are checking Paul Kafentzis's Outlook for replies to ONE email he sent. You have no memory of earlier chats: everything you need is here.",
        "",
        "WHAT WAS SENT",
        *_head(facts),
        "- Replies expected from: %s" % ", ".join(facts["senders"]),
        "- Last day of watching: %s (South African date)" % stop.strftime("%d/%m/%Y"),
        "- This scheduled task is named: %s" % name,
        "",
        "EACH TIME YOU RUN",
        "1. For each sender still on the list, search Paul's Outlook with the Microsoft 365 connector (outlook_email_search, sender filter, received after %s). Never rely on read or unread." % facts["sent"],
        "2. " + genuine_text(),
        "3. If a search itself fails, say so plainly in your last line: a failed search is NOT 'no reply'. Never report 'no reply' from a failed search.",
        "4. When a sender has genuinely replied: end your run with a clear summary for Paul (who, when, and one line on what they said or provided; this alerts his phone). "
        "Then find this scheduled task by its name with list_triggers and update_trigger its prompt so that sender is no longer on the list. When nobody is left on the list, delete this scheduled task (delete_trigger).",
        "5. If nothing new and genuine has arrived, end with one short unremarkable line and no summary, so nothing alerts his phone.",
        "",
        "LAST DAY (%s)" % stop.strftime("%d/%m/%Y"),
        "If today (South African date) is %s and the time is 17:00 or later, and anyone is still on the list, end with ONE clear message: "
        "\"%s: no reply from <names>. I have stopped checking.\" Then delete this scheduled task (delete_trigger, found by its name). Never leave it running." % (stop.strftime("%d/%m/%Y"), facts["subject"].strip()),
    ])


def flag_prompt(facts):
    return "\n".join([
        "You are checking ONE thing for Paul Kafentzis. You have no memory of earlier chats: everything you need is here.",
        "",
        "WHAT WAS SENT",
        *_head(facts),
        "- Replies expected from: %s" % ", ".join(facts["senders"]),
        "",
        "WHAT TO DO (two business days have passed since it was sent)",
        "1. For each sender, search Paul's Outlook with the Microsoft 365 connector (outlook_email_search, sender filter, received after %s). Never rely on read or unread." % facts["sent"],
        "2. " + genuine_text(),
        "3. If a search itself fails, say so plainly in your last line: a failed search is NOT 'no reply'.",
        "4. If every sender has genuinely replied, end with one short unremarkable line and no summary, so nothing alerts his phone.",
        "5. Otherwise end with a clear message for Paul (this alerts his phone) naming each sender still outstanding, what was asked and since when, one line each.",
        "Do not delete or change any other scheduled task.",
    ])


def _common(name):
    return {"name": name, "create_new_session_on_fire": True, "notifications": {"push": True}, "connectors": [w.CONNECTOR], "initiation": "human_schedule"}


def build_plan(facts, today):
    """The exact arguments for the two create_trigger calls."""
    sent, stop, flag = dates(facts, today)
    wname, fname = task_names(facts)
    watch = dict(_common(wname), prompt=watch_prompt(facts, wname, stop), cron_expression=CRON)
    flg = dict(_common(fname), prompt=flag_prompt(facts), run_once_at=athens_0900(flag))
    return {"watch": watch, "flag": flg, "stop": stop.strftime("%d/%m/%Y"), "flag_date": flag.strftime("%d/%m/%Y")}


def plan_problems(facts, plan, today):
    """Every rule checked on a plan (empty = fine). The checker also compares it with a rebuild."""
    out = []
    watch, flg = plan.get("watch") or {}, plan.get("flag") or {}
    sent, stop, flag = dates(facts, today)
    for label, t, keys in (("watcher", watch, {"name", "prompt", "cron_expression", "create_new_session_on_fire", "notifications", "connectors", "initiation"}),
                           ("flag", flg, {"name", "prompt", "run_once_at", "create_new_session_on_fire", "notifications", "connectors", "initiation"})):
        if set(t) != keys:
            out.append("the %s has the wrong fields: %s" % (label, sorted(set(t) ^ keys)))
        if t.get("create_new_session_on_fire") is not True or t.get("notifications") != {"push": True}:
            out.append("the %s must start a fresh chat each time with the phone alert on (create_new_session_on_fire true, push true)" % label)
        if t.get("connectors") != [w.CONNECTOR]:
            out.append("the %s may use the %s connector and nothing else" % (label, w.CONNECTOR))
        p = t.get("prompt") or ""
        for s in facts["senders"]:
            if s not in p:
                out.append("the %s instruction does not name %s" % (label, s))
        for need, what in (("outlook_email_search", "the search tool"), ("NOT genuine replies", "what is not a genuine reply"), ("NOT 'no reply'", "that a failed search is not 'no reply'"), ("read or unread", "no reliance on read/unread")):
            if need not in p:
                out.append("the %s instruction is missing %s" % (label, what))
        if w.OWN_MAILBOX in p:
            out.append("the %s instruction must not contain Paul's own address" % label)
    if watch.get("cron_expression") != CRON:
        out.append("the watcher must run %s" % CRON)
    if stop.strftime("%d/%m/%Y") not in (watch.get("prompt") or "") or "delete_trigger" not in (watch.get("prompt") or ""):
        out.append("the watcher instruction must name its last day and tell it to delete itself")
    if "update_trigger" not in (watch.get("prompt") or ""):
        out.append("the watcher instruction must tell it to drop a sender who has replied")
    got = instant(flg.get("run_once_at"))
    want = instant(athens_0900(flag))
    if got is None or got != want:
        out.append("the flag must fire once at 09:00 Athens time on %s (%s)" % (flag.strftime("%d/%m/%Y"), athens_0900(flag)))
    elif got.astimezone(w.SAST).date() <= today:
        out.append("the flag time is not in the future")
    if flag > stop:
        out.append("the flag day %s is after the last day of watching %s" % (flag.strftime("%d/%m/%Y"), stop.strftime("%d/%m/%Y")))
    names = task_names(facts)
    if (watch.get("name"), flg.get("name")) != names:
        out.append("the task names must be %s and %s" % names)
    return out


def plan_text(facts, plan):
    return "\n".join([
        "TRACKING PLAN (nothing is sent to anyone; two scheduled checks are set up)",
        "Email: %s | sent %s | reply expected from: %s" % (facts["subject"].strip(), facts["sent"], ", ".join(facts["senders"])),
        "Why a reply is needed: %s" % facts["why"].strip(),
        "1. Watcher: every hour, Monday to Friday 08:00 to 17:00 South African time. A genuine reply alerts your phone with one line and that sender is dropped. "
        "It stops for good at 17:00 on %s (5 business days) with one last message if anyone is still silent, and deletes itself." % plan["stop"],
        "2. Silence flag: once, %s at 09:00 Athens time. It alerts your phone only if someone is still outstanding." % plan["flag_date"],
        "Both run as a fresh chat each time, may read your Outlook through the %s connector and nothing else, and never rely on read or unread." % w.CONNECTOR,
    ])


def plan_sha(plan):
    import json
    return hashlib.sha256(json.dumps(plan, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()

