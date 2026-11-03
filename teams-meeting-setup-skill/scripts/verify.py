#!/usr/bin/env python3
"""The one checker of the teams-meeting-setup-skill.

  verify.py <run_dir> [pre|final] [--full]

It re-reads the Fact Find PDF itself and REBUILDS the invite from the recorded facts, so nothing is taken on trust from a file Claude could
have edited. The reply to Paul carries the SHORT AUDIT it prints: one line per check with a green tick or a red cross, and one closing line
for what is only attested (Paul, 03/11/2026). The full record is written to out_record/audit-full.txt (--full prints it).
"""
import os
import sys

import ffread
import invite as inv
import wrlib as w

OK, BAD = "✅", "❌"
STEP_IDS = ["client", "facts", "build", "show", "send", "log", "final"]


class Results:
    def __init__(self):
        self.rows, self.attested, self.group = [], [], ""

    def add(self, ok, short, detail=""):
        self.rows.append((OK if ok else BAD, short, detail, self.group))

    @property
    def fails(self):
        return [r for r in self.rows if r[0] == BAD]


def client_from_pdf(ffd):
    ff = {}
    for s in ffd["sections"]:
        for b in s["blocks"]:
            for r in b["rows"]:
                ff[(s["num"], b["sub"], r["label"])] = " ".join(r["values"]).strip()
    email = ff.get((1, "Contact details", "Personal email"), "")
    return {"first": ff.get((1, "Client", "Name"), ""), "surname": ff.get((1, "Client", "Surname"), ""),
            "email": email if inv.EMAIL.match(email) else ""}


def run_checks(run, stage):
    R = Results()
    rj = w.load_json(os.path.join(run, w.RUN))
    mode = rj["mode"]
    today = w.parse_date(rj["today"])
    req = rj["client"]
    # ---------------------------------------------------------------- the client, read from the Fact Find by the program
    R.group = "client"
    pdf = os.path.join(run, w.FACTFIND_PDF)
    client = None
    if not os.path.exists(pdf):
        R.add(False, "The Fact Find Transcript PDF is not in the run folder", "run.py source")
    else:
        try:
            ffd = ffread.read_pdf(pdf)
            probs = ffread.layout_problems(ffd)
            found = client_from_pdf(ffd)
        except Exception as e:
            ffd, probs, found = None, ["the PDF could not be read: %s" % e], {"first": "", "surname": "", "email": ""}
        same = w.norm("%s %s" % (found["first"], found["surname"])) == w.norm("%s %s" % (req["first"], req["surname"]))
        R.add(not probs and same, "Fact Find PDF read by program; it is for %s %s, as you asked" % (found["first"], found["surname"]) if not probs and same else
              "The Fact Find PDF problem: %s" % ("; ".join(probs) if probs else "it is for %s %s, not %s %s" % (found["first"], found["surname"], req["first"], req["surname"])), "; ".join(probs))
        ov = rj.get("email_override")
        email = found["email"] or (ov or {}).get("email", "")
        if found["email"]:
            R.add(True, "The client's personal email is read from the Fact Find (%s)" % found["email"])
        elif ov and inv.EMAIL.match(ov.get("email", "")) and len((ov.get("said") or "").strip()) >= 5:
            R.add(True, "The Fact Find has no personal email; Paul gave it in his own words (%s)" % ov["email"])
            R.attested.append("the client's email, which Paul gave in words typed by the chat")
        else:
            R.add(False, "The Fact Find has no usable personal email: ask Paul for it, then run.py client --email ... --said \"his words\"")
        if not probs and same:
            client = {"first": found["first"], "surname": found["surname"], "email": email}
    # ---------------------------------------------------------------- the facts
    R.group = "facts"
    facts = w.load_opt(os.path.join(run, w.FACTS), None)
    if not facts:
        R.add(False, "The facts of the follow-up are not recorded yet", "step 'facts': run.py facts")
    else:
        fp = inv.fact_problems(facts, today)
        if mode == "new":
            what = "follow-up %s %s SAST, topics %s, last contact %s (%s)" % (facts["date"], facts["time"], inv.subject_topics(facts.get("topics") or []) if not inv.topic_problems(facts.get("topics") or []) else "?", facts["last_contact"], facts["contact"])
        else:
            what = "new date and time %s %s SAST" % (facts["date"], facts["time"])
        R.add(not fp, "Facts valid and sourced: %s" % what if not fp else "Facts problem: %s" % fp[0], "; ".join(fp))
    # ---------------------------------------------------------------- the invite, rebuilt by the program
    R.group = "build"
    ipath = os.path.join(run, w.OUT, w.INVITE)
    payload = w.load_opt(ipath, None)
    if client is None or not facts or inv.fact_problems(facts, today):
        R.add(False, "The invite cannot be checked until the client and the facts are good")
    elif payload is None:
        R.add(False, "The invite has not been built yet", "step 'build'")
    else:
        expected = inv.build_payload(client, facts, mode, rj.get("event_id"), today)
        pp = inv.payload_problems(client, facts, mode, rj.get("event_id"), payload, today)
        R.add(not pp, ("Invite follows the rules: subject, SAST on start and end, exactly 1 hour, the client only, Teams on, no link or signature" if mode == "new" else
                       "Reschedule follows the rules: existing event id, SAST on start and end, exactly 1 hour, nothing else changed") if not pp else "Invite problem: " + pp[0], "; ".join(pp))
        R.add(payload == expected, "invite.json is exactly what the program builds from the facts (not edited by hand)")
        st = w.load_opt(os.path.join(run, "state.json"), {})
        sit = open(os.path.join(run, w.OUT, w.SITAMAH), encoding="utf-8").read() if os.path.exists(os.path.join(run, w.OUT, w.SITAMAH)) else None
        R.add(sit == inv.sitamah_text(client, facts, mode), "The message to Sitamah is exactly what the program builds (an FYI: nothing needed from her)")
        # ------------------------------------------------------------ Paul's yes for exactly this invite
        R.group = "approval"
        ap = w.load_opt(os.path.join(run, w.APPROVAL), None)
        cur = inv.payload_sha({"invite": payload, "sitamah": sit})
        okap = bool(ap) and ap.get("sha") == cur and len((ap.get("said") or "").strip()) >= 3 and bool(st.get("shown_sha")) and st.get("shown_sha") == cur
        R.add(okap, "Paul's yes is recorded for exactly this invite and message, after he was shown them" if okap else "No valid yes from Paul for this invite: show it, then run.py approve with his exact words")
        # ------------------------------------------------------------ what the tool returned, against what he approved
        R.group = "send"
        rc = w.load_opt(os.path.join(run, w.RECEIPT), {})
        if mode == "new":
            want = {"event.subject": payload["subject"], "event.attendee": client["email"]}
        else:
            want = {"event.id": rj.get("event_id")}
        bad = [k for k, v in want.items() if (rc.get(k) or "").strip().lower() != (v or "").strip().lower()]
        for k, src in (("event.start", payload["start"]["dateTime"]), ("event.end", payload["end"]["dateTime"])):
            if (rc.get(k) or "").replace(" ", "T")[:16] != src[:16]:
                bad.append(k)
        if mode == "new":
            if not (rc.get("event.id") or "").strip():
                bad.append("event.id")
            if (rc.get("event.online") or "").strip().lower() != "yes":
                bad.append("event.online")
        R.add(not bad and okap, ("The event returned by the tool equals the approved invite (id, subject, start, end, attendee, Teams on)" if mode == "new" else
                                 "The updated event returned by the tool equals the approved new time (same event id)") if not bad and okap else
              "What the tool returned does not match what Paul approved (or there was no valid approval): %s" % (", ".join(bad) or "approval"), ", ".join(bad))
        R.add(bool((rc.get("sitamah.sent") or "").strip()) and okap, "Sitamah was messaged once (message id or sent time recorded)" if rc.get("sitamah.sent") else "The message to Sitamah is not recorded as sent")
        R.group = "log"
        R.add(rc.get("log.done") == "yes", "Logged on the board's Fact Find card, as today" if rc.get("log.done") == "yes" else "The log on the board's Fact Find card is not recorded")
    if stage == "final":
        R.group = "final"
        rj2 = rj
        done = [s for s in STEP_IDS[:-1] if (rj2.get("steps", {}).get(s) or {}).get("state") == "done"]
        fpok = rj2.get("program_fingerprint") == w.program_fingerprint()
        R.add(done == STEP_IDS[:-1] and fpok, "Every step done in order (%d of %d) and the programs did not change during the run" % (len(done), len(STEP_IDS) - 1) if done == STEP_IDS[:-1] and fpok else
              "Steps done: %s%s" % (", ".join(done) or "none", "; the programs changed during the run" if not fpok else ""))
        R.attested += ["Paul's yes (the words are typed by the chat)", "that the chat really called the Microsoft 365 tool and sent the Sitamah message (the program checks only what was reported back)",
                       "the logging on the board's Fact Find card", "that Paul's signature appears on the client's copy (check on the first real invite)"]
    return R, rj


def print_audit(R, rj, stage, run, full=False):
    lines = ["AUDIT   %s" % w.version_line()]
    for mark, short, detail, _g in R.rows:
        lines.append("%s %s" % (mark, short))
    if R.attested:
        lines.append("Only attested (not proven): " + "; ".join(R.attested) + ".")
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
