INVENTORY of the old skill: 154 sentences
  kept (word for word or nearly): 6
  reworded, with a recorded change: 99
  dropped, with a recorded decision: 49
  UNACCOUNTED: 0


REWORDED (each is covered by a recorded change):
- old line 24: Write only what is in the source material (transcript, quote, document, file) or in a named document this skill tells you to use.
    now: If the PDF is not the program-drawn Fact Find, or it is for another client, it stops and you tell Paul in one line.
    why: Shortened to what applies to this skill; the program now records and checks the source.
- old line 24: If a line is unclear, garbled or ambiguous, do not turn it into a fact:
    now: if client is None or not facts or inv.fact_problems(facts, today):
    why: Shortened to what applies to this skill; the program now records and checks the source.
- old line 24: flag it to the user.
    now: FLAG_MARKS = ("⚠", "!")                 # '!' when the font could not draw the warning sign
    why: Shortened to what applies to this skill; the program now records and checks the source.
- old line 24: "It seems implied", "it is usual" and "it would make sense" are not sources.
    now: ".join(probs) if probs else "it is for %s %s, not %s %s" % (found["first"], found["surname"], req["first"], req["surname"])), ";
    why: Shortened to what applies to this skill; the program now records and checks the source.
- old line 26: Never tell the user something is done, saved, sent, visible or working until you have checked it yourself (open the file, list the folder, look at the screen).
    now: Never tell the user something is sent, created or logged until you have checked it yourself (the event the tool returned, the message id).
    why: Shortened to what applies to this skill; the program now records and checks the source.
- old line 28: When the user corrects anything:
    now: if a result is unclear, look in the calendar before anything else.
    why: Shortened to what applies to this skill; the program now records and checks the source.
- old line 28: (a) go back to the source and re-check that point and everything related to it;
    now: 1 | Run it | The one command that starts the job and how every step works |
    why: Shortened to what applies to this skill; the program now records and checks the source.
- old line 28: (b) fix it everywhere it appears, in every deliverable;
    now: 1 | Run it | The one command that starts the job and how every step works |
    why: Shortened to what applies to this skill; the program now records and checks the source.
- old line 28: (c) re-run this skill's full checklist;
    now: which version of this skill is running.
    why: Shortened to what applies to this skill; the program now records and checks the source.
- old line 28: (d) re-deliver every affected deliverable in full, as in rule 5.
    now: print("EVERY STEP IS DONE.\nPut this SHORT AUDIT in your reply, as it is (it is the whole report;
    why: Shortened to what applies to this skill; the program now records and checks the source.
- old line 28: Never fix only the item named and stop.
    now: "For a RESCHEDULE only the new --date, --time and --source are needed.",
    why: Shortened to what applies to this skill; the program now records and checks the source.
- old line 51: Once a follow-up/2nd (or later) appointment date and time is confirmed for a client — from the Fact Find/transcript or from Paul directly — this skill creates the real Outlook calendar event with a Te
    now: "The follow-up Teams meeting invite (a calendar event with a Teams meeting, the client as attendee)",
    why: Shortened: the program now builds the invite; the chat only sends exactly what the program built, after Paul's yes.
- old line 55: {Client Name} / {short topic list}
    now: ff.get((1, "Client", "Name"), ""), "surname":
    why: Built by the program from the client's name and the topics.
- old line 57: Client Name exactly as captured in the Fact Find (e.g.
    now: The client's name and email come from the Fact Find;
    why: Program-read name; fixed labels checked.
- old line 58: Topic list — the open product lines this follow-up covers, short labels only, never the full product name and never an internal stage code:
    now: the product lines that are open for this client right now (from the follow-up summary, the Fact Find's Advisor Actions, or Paul).
    why: Program-read name; fixed labels checked.
- old line 71: List only the lines actually open for this client at the time the meeting is set up, in the order above.
    now: list the product lines that are open for this client")
    why: Joined by the program.
- old line 71: two items get "&" ("Risk & RA");
    now: -topics "Risk,RA" --needs "a;
    why: Joined by the program.
- old line 71: three or more are comma-separated with "&" before the last ("Risk, RA & RGAR");
    now: one topic is just that label (RA), two get "&" (Risk & RA), three or more are comma-separated with "&" before the last (Risk, RA & RGAR).
    why: Joined by the program.
- old line 71: one line alone is just that label ("RA").
    now: one line per check with a green tick or a red cross, one closing line for what is only attested",
    why: Joined by the program.
- old line 71: "[Client Name] / Risk, RA & RGAR".
    now: 'RA', 'Risk & RA', 'Risk, RA & RGAR'."""
    why: Joined by the program.
- old line 73: Keep it short — a calendar subject, not a sentence.
    now: # Product line -> (short label for the subject, plain client wording for the agenda).
    why: Same rule, built by the program.
- old line 73: No "Follow-up," no "Meeting," no stage code — the entry being a meeting is already obvious from the calendar itself.
    now: No "Follow-up", no "Meeting", no stage code.
    why: Same rule, built by the program.
- old line 75: Time zone — always South Africa ("Harare, Pretoria")
    now: TZ = "Africa/Johannesburg"              # always South Africa, on start and end (SAST, UTC+2, no daylight saving)
    why: Constant in the program.
- old line 77: Set both start.timeZone and end.timeZone on outlook_create_event to Africa/Johannesburg (the tool maps this IANA name to the Windows zone Outlook displays as "(UTC+02:00) Harare, Pretoria").
    now: Load mcp__Microsoft_365__outlook_update_event and call it ONCE with exactly the fields in out/invite.json (the existing event id, the new start and end).
    why: Built and checked by the program.
- old line 77: Never use Paul's own Greek zone, never the client's specifically, never leave it defaulted.
    now: run.py client <run> [--email ADDRESS --said "Paul's words"]                             read name and email from the Fact Find
    why: Built and checked by the program.
- old line 79: *Why this is deliberate, not an oversight:
    now: w.die('This is not a run folder (no %s).
    why: Shortened; the explanation is kept in plain words.
- old line 79: South Africa Standard Time (SAST, UTC+2) does not observe daylight saving.
    now: TZ = "Africa/Johannesburg"              # always South Africa, on start and end (SAST, UTC+2, no daylight saving)
    why: Shortened; the explanation is kept in plain words.
- old line 79: Greece does observe EU daylight saving — EEST (UTC+3) roughly late March to late October, EET (UTC+2, same as SAST) the rest of the year.
    now: South Africa Standard Time does not observe daylight saving, so the wall-clock time on the invite is always the real South African time.
    why: Shortened; the explanation is kept in plain words.
- old line 81: Outlook always stores an event's real instant (UTC) and displays it back to each viewer converted into *their own* calendar's time zone.
    now: Outlook shows Paul the same event converted to his own Athens time:
    why: Shortened.
- old line 83: Creating the event with the zone set to SAST means the wall-clock time attached to the invite is always the real South African time — exactly what the client needs to see, in every month of the year.
    now: South Africa Standard Time does not observe daylight saving, so the wall-clock time on the invite is always the real South African time.
    why: Shortened.
- old line 84: When Paul looks at his own Outlook (set to Athens time), the same event shows one hour later during the European summer (EEST) and the same time as SA during the European winter (EET = SAST = UTC+2).
    now: one hour later in the European summer, the same in winter.
    why: Shortened.
- old line 84: This is expected, correct behaviour — Outlook's normal per-viewer conversion — not a bug to fix.
    now: That is expected, not a bug.
    why: Shortened.
- old line 88: Adapt this shape — don't send Paul's own example wording verbatim if the specifics don't fit:
    now: print("\nTHE ONE QUESTION TO PAUL (show everything above in the reply, then ask exactly this):\n    %s\n" % q)
    why: Paul's approved plan (03/11/2026): the program builds the whole invite.
- old line 93: {opening line — see below, date-aware and factually accurate}
    now: "Hi {First name}," then an opening line that is date-aware and accurate (same day:
    why: Computed by the program from the real gap and the kind of contact.
- old line 98: {open topic 1 in plain words}
    now: normally made from the topics in plain client words.
    why: Made by the program from the topics, in plain client words.
- old line 101: What we need from you before then:
    now: What we need from you (optional):
    why: Built by the program.
- old line 105: Below is the link to join the Teams meeting on {DD/MM/YYYY}.
    now: parts.append("Below is the link to join the Teams meeting on %s." % facts["date"])
    why: Built by the program.
- old line 108: Opening line is date-aware and describes the contact accurately — never hardcode "yesterday." Work out the real gap between the 1st (or most recent) appointment and today:
    now: "Hi {First name}," then an opening line that is date-aware and accurate (same day:
    why: Moved into the program; the longer signature explanation is shortened and points to paul-email-signature.
- old line 109: Same day → "Great to have met with you earlier today."
    now: "Great to have met with you earlier today.";
    why: Moved into the program; the longer signature explanation is shortened and points to paul-email-signature.
- old line 110: Previous calendar day → "Great to have met with you yesterday."
    now: "Great to have met with you earlier today.";
    why: Moved into the program; the longer signature explanation is shortened and points to paul-email-signature.
- old line 111: Longer gap → "Great to have met with you on {DD/MM/YYYY}." or a neutral "It was great catching up with you recently." if naming the exact date reads awkwardly.
    now: "Creates the follow-up Teams meeting invite in Outlook Calendar for a Wealth Revolution client once the date is confirmed (or moves an existing one).
    why: Moved into the program; the longer signature explanation is shortened and points to paul-email-signature.
- old line 112: Say "met" for a Teams/video appointment;
    now: 'met' for a Teams or video appointment, 'spoke' only when the last contact was a phone or WhatsApp call."""
    why: Moved into the program; the longer signature explanation is shortened and points to paul-email-signature.
- old line 112: use "spoke" / "spoken" only when the last contact really was a phone or WhatsApp call.
    now: 'met' for a Teams or video appointment, 'spoke' only when the last contact was a phone or WhatsApp call."""
    why: Moved into the program; the longer signature explanation is shortened and points to paul-email-signature.
- old line 112: If genuinely unclear how or when the last conversation happened, ask Paul rather than guessing.
    now: If it is genuinely unclear, ask Paul rather than guessing.
    why: Moved into the program; the longer signature explanation is shortened and points to paul-email-signature.
- old line 113: 2-5 short bullets, the open topics in plain client language (e.g.
    now: normally made from the topics in plain client words.
    why: Moved into the program; the longer signature explanation is shortened and points to paul-email-signature.
- old line 113: "Your life cover quote", "Retirement Annuity and Tax-Free options", "Retirement goal analysis").
    now: LINES = [("Risk", "Your life cover quote"), ("RA", "Your Retirement Annuity"), ("Investments", "Your investments"), ("RGAR", "Your retirement goal analysis"),
    why: Moved into the program; the longer signature explanation is shortened and points to paul-email-signature.
- old line 113: Never internal stage codes or product jargon.
    now: You never type or edit any of them."
    why: Moved into the program; the longer signature explanation is shortened and points to paul-email-signature.
- old line 114: What we need from you:
    now: What we need from you (optional):
    why: Moved into the program; the longer signature explanation is shortened and points to paul-email-signature.
- old line 114: only items the client actually owes (e.g.
    now: attendee   the client only, from the Fact Find;
    why: Moved into the program; the longer signature explanation is shortened and points to paul-email-signature.
- old line 114: confirm budget and any cover changes, send a statement, sign a form), taken from the Fact Find / the client's Planner Task checklist / the follow-up summary.
    now: only items the client actually owes (for example confirm budget and any cover changes, send a statement, sign a form), taken from the Fact Find's documents to request, the follow-up summary or the cli
    why: Moved into the program; the longer signature explanation is shortened and points to paul-email-signature.
- old line 114: Leave this block out entirely if nothing is outstanding — never invent items.
    now: Leave it out when nothing is outstanding;
    why: Moved into the program; the longer signature explanation is shortened and points to paul-email-signature.
- old line 115: The date in the closing line is the follow-up meeting's own date (DD/MM/YYYY), not the 1st appointment's date.
    now: out.append("the follow-up date %r is not a real date (DD/MM/YYYY)" % facts.get("date"))
    why: Moved into the program; the longer signature explanation is shortened and points to paul-email-signature.
- old line 116: Never hand-write or fabricate a Teams link, meeting ID, or passcode.
    now: never a hand-written link, meeting ID or passcode);
    why: Moved into the program; the longer signature explanation is shortened and points to paul-email-signature.
- old line 116: true on outlook_create_event — Microsoft Graph generates the real join link/meeting ID/passcode and appends the standard "Microsoft Teams meeting / Join / Meeting ID / Passcode" block to the body auto
    now: FORBIDDEN_IN_BODY = ("http", "teams.microsoft.com", "meeting id", "passcode", "kind regards", "regards,", "best regards", "wealth revolution")
    why: Moved into the program; the longer signature explanation is shortened and points to paul-email-signature.
- old line 116: Never recreate that block manually, and never invent a placeholder link.
    now: Never rewrite, shorten or "improve" the programs during a run, and never type or edit the invite yourself.
    why: Moved into the program; the longer signature explanation is shortened and points to paul-email-signature.
- old line 117: "html", with a blank line between each paragraph (use line breaks rather than paragraph tags, per Paul's Outlook spacing preference;
    now: body       HTML with a blank line between paragraphs, no hand-typed signature (an Exchange rule adds Paul's signature).
    why: Moved into the program; the longer signature explanation is shortened and points to paul-email-signature.
- old line 117: use ul/li only if the allowlist accepts it, otherwise "- " lines).
    now: If there are several, use the latest.
    why: Moved into the program; the longer signature explanation is shortened and points to paul-email-signature.
- old line 117: This is also required for the signature described next to render as styled HTML rather than being downgraded to plain text.
    now: If it is genuinely unclear, ask Paul rather than guessing.
    why: Moved into the program; the longer signature explanation is shortened and points to paul-email-signature.
- old line 118: Signature — confirmed working, applied automatically.
    now: Paul's signature is added by the Exchange rule.", "", "BODY:", body]
    why: Moved into the program; the longer signature explanation is shortened and points to paul-email-signature.
- old line 118: A dedicated Exchange transport rule ("Auto-signature - Calendar invites (Paul)":
    now: It is added automatically by an Exchange transport rule to every calendar invite from Paul's mailbox.
    why: Moved into the program; the longer signature explanation is shortened and points to paul-email-signature.
- old line 118: condition = message type is Calendaring AND sender is paulk@liferisk.co.za) appends Paul's full Wealth Revolution signature — including logo — to every calendar invite sent from his mailbox via outloo
    now: an Exchange rule adds Paul's full signature to every calendar invite from his mailbox.
    why: Moved into the program; the longer signature explanation is shortened and points to paul-email-signature.
- old line 118: Verified on a real invite received by a third-party attendee.
    now: verify on a real third-party recipient (the first real invite).
    why: Moved into the program; the longer signature explanation is shortened and points to paul-email-signature.
- old line 118: Checking the *organizer's own* calendar entry will never show the signature, so always verify via a real third-party recipient.
    now: Checking the organizer's own calendar entry never shows it:
    why: Moved into the program; the longer signature explanation is shortened and points to paul-email-signature.
- old line 118: Do not hand-type a signature into the invite body — a hand-typed one would duplicate it.
    now: the body of the invite is not changed, so its closing line still names the old date.")
    why: Moved into the program; the longer signature explanation is shortened and points to paul-email-signature.
- old line 118: Detail lives in paul-email-signature.
    now: If a client reports it missing, see paul-email-signature.
    why: Moved into the program; the longer signature explanation is shortened and points to paul-email-signature.
- old line 120: Attendee, duration, and other fields
    now: OTHER = "Other fields from the form"
    why: Built by the program.
- old line 122: "required", using the FF-captured personal email — the same address General and product-line emails use.
    now: "The program reads the client's name and personal email from the Fact Find.
    why: Built and checked by the program.
- old line 122: Never Sitamah, never Paul (he's the organizer automatically).
    now: never Sitamah, never Paul (he is the organizer).
    why: Built and checked by the program.
- old line 123: true so the client's Accept actually reaches Paul.
    now: responseRequested is true so the client's Accept reaches Paul.
    why: Built and checked by the program.
- old line 124: always 1 hour, fixed — never a shorter default, even if the Fact Find/transcript names a shorter window.
    now: where the Fact Find Transcript PDF is and the three routes.
    why: Built and checked by the program.
- old line 124: This is a standing rule from Paul ("Meetings are always 1 hour long").
    now: exactly 1 hour ("Meetings are always 1 hour long":
    why: Built and checked by the program.
- old line 124: If Paul himself specifies a different length for a specific meeting, that explicit instruction overrides this default for that one invite only.
    now: Only if Paul himself specifies another length for one meeting does it change, and then he tells Claude Code to change the program, never the chat to type it.
    why: Built and checked by the program.
- old line 125: Leave location blank (Graph fills in "Microsoft Teams Meeting" once isOnlineMeeting is set) and other fields at their defaults.
    now: Call mcp__Microsoft_365__outlook_create_event ONCE, with exactly the fields in out/invite.json and nothing added or changed.
    why: Built and checked by the program.
- old line 127: Sending the invite is a real send — get Paul's go-ahead first
    now: The invite is a real send:
    why: The program shows the invite and records Paul's yes before the send step.
- old line 129: There is no draft state for a calendar event with an attendee:
    now: There is no draft state.
    why: Shortened.
- old line 129: the moment outlook_create_event runs with the client listed, Graph emails them the invite immediately.
    now: The moment the event is created with the client as attendee, Microsoft emails them.
    why: Shortened.
- old line 131: once a follow-up date (and time, and topic list) is confirmed, show Paul exactly what would go out — subject, date/time in SA time, the (fixed 1-hour) duration, the full body text including the agenda
    now: Every fact (the follow-up date and time, the last contact, the topics, what the client owes) comes from Paul, the follow-up summary or the Fact Find and is recorded with its source.
    why: Program-driven.
- old line 131: *"Ready to send [Client] the Teams meeting invite for [date] at [time] SAST (1 hour), covering [topics]?"* Only call outlook_create_event once Paul says yes.
    now: q = "Ready to send %s %s the Teams meeting invite for %s at %s SAST (1 hour), covering %s, and to message Sitamah?" % (
    why: Program-driven.
- old line 133: If Paul later says he wants this to auto-send, that's his explicit call to make — don't assume it.
    now: If he later says he wants it to auto-send, that is his explicit call to make:
    why: Kept in the rules page.
- old line 135: Logging and keeping Sitamah in the loop
    now: Nothing is sent without Paul's yes, and the message to Sitamah is shown in the same reply as the invite, so one yes covers both.
    why: Logging and Sitamah now have their own page and a program step.
- old line 137: Log the confirmed meeting under the Fact Find card's Actions Taken (or the relevant product card) — subject, date/time (SAST), attendee, as separate short bullets.
    now: "Log the lines it prints on the client's Fact Find card under Actions Taken (the board's card, as today), then record:
    why: Lines built by the program; Sitamah is messaged after Paul's yes (same reply, one question).
- old line 138: Message Sitamah on Teams once it's actually sent, per client-pipeline-board's "Keeping Sitamah in the loop" (via the Zapier Teams connector).
    now: print("\nMESSAGE TO SITAMAH (sent after the invite, through Zapier, once):\n")
    why: Lines built by the program; Sitamah is messaged after Paul's yes (same reply, one question).
- old line 138: She's notified by Teams message, not added as an attendee or cc.
    now: R.add(not bad and okap, ("The event returned by the tool equals the approved invite (id, subject, start, end, attendee, Teams on)" if mode == "new" else
    why: Lines built by the program; Sitamah is messaged after Paul's yes (same reply, one question).
- old line 139: If Paul later reports a reschedule, use outlook_update_event on the existing event id (never delete-and-recreate) so the client's already-accepted invite updates in place.
    now: A reschedule updates the existing event in place (outlook_update_event with its event id), so the client's already-accepted invite changes.
    why: Lines built by the program; Sitamah is messaged after Paul's yes (same reply, one question).
- old line 143: client name, forward slash, short topic labels only, matching the product lines actually open for this client right now.
    now: list the product lines that are open for this client")
    why: The checking list is now done by the checker.
- old line 144: Time zone on both start and end:
    now: Africa/Johannesburg on start and end, always.
    why: The checking list is now done by the checker.
- old line 144: Africa/Johannesburg — never Paul's own zone, never the client's, never left blank.
    now: that is Paul or Sitamah, never the client")
    why: The checking list is now done by the checker.
- old line 145: Duration is exactly 1 hour unless Paul explicitly specified a different length for this invite.
    now: existing event id, SAST on start and end, exactly 1 hour, nothing else changed") if not pp else "Invite problem:
    why: The checking list is now done by the checker.
- old line 146: opening line matches the real gap AND the real type of contact (met vs spoke);
    now: Never rewrite, shorten or "improve" the programs during a run, and never type or edit the invite yourself.
    why: The checking list is now done by the checker.
- old line 146: agenda bullets match the open topics;
    now: normally made from the topics in plain client words.
    why: The checking list is now done by the checker.
- old line 146: outstanding items are real (or the block is omitted);
    now: The invite is a real send:
    why: The checking list is now done by the checker.
- old line 146: closing date is the follow-up meeting's own date;
    now: out.append("the follow-up date %s is in the past" % facts["date"])
    why: The checking list is now done by the checker.
- old line 146: no hand-written Teams link, meeting ID, or passcode.
    now: never a hand-written link, meeting ID or passcode);
    why: The checking list is now done by the checker.
- old line 148: Attendee is the client's FF-captured email only — not Sitamah, not Paul.
    now: responseRequested is true so the client's Accept reaches Paul.
    why: The checking list is now done by the checker.
- old line 149: Paul's explicit go-ahead (having seen the full body) was obtained before outlook_create_event ran.
    now: INVITE = "invite.json"                  # the exact payload for outlook_create_event / outlook_update_event
    why: The checking list is now done by the checker.
- old line 150: Signature applies automatically via the calendar transport rule;
    now: if a result is unclear, look in the calendar before anything else.
    why: The checking list is now done by the checker.
- old line 150: if a client reports it missing, check the rule per paul-email-signature.
    now: If a client reports it missing, see paul-email-signature.
    why: The checking list is now done by the checker.
- old line 151: outlook_update_event was used on the existing event.
    now: a reschedule needs --event-id (the id of the existing event).
    why: The checking list is now done by the checker.
- old line 152: Sitamah was messaged on Teams once the invite was actually sent.
    now: ## Tell Sitamah (once, after the invite is sent)
    why: The checking list is now done by the checker.


DROPPED (each is covered by a recorded decision):
- # Teams Meeting Set Up Skill: Replaced by the new short title.
- Section | What it covers |: Replaced by the new short Index (five sections).
- ## UNIVERSAL OPERATING RULES - READ FIRST, APPLY TO EVERY STEP OF THE : The preamble and heading are replaced by the short intro of references/00-rules.md; the program shows the rules at the start and the right page at each step.
- Re-load this skill before you start, and again after any compression. : Rule 1 (re-load this skill) is replaced by the program: it shows the standing rules at the start and the right page at each step, and `run.py status` tells a chat where the job is up to after a compression.
- Read before you write. Read the source material completely and careful: Rule 3 (read before you write) concerned drafting from a source. This skill drafts nothing from a document: the program reads the Fact Find itself.
- Deliver everything this skill lists, every time. A run is not finished: Rule 5 (deliver everything) is replaced by deliverables.json and the checker: a run is finished only with a PASS audit.
- Changes to a skill: edit the existing skill, never create a new one. U: Rule 9 (changes through the propose_skills card) is replaced by standard S7: skills are changed only in Claude Code and uploaded as a zip by Paul; the 'never say it is live' part is standing rule 6 in SKILL.md.
- Delivery gate for this skill (rules 5 and 6 applied): a run is complet: The Delivery gate is replaced by the steps and the checker (the send step compares what the tool returned with what Paul approved).
- Last updated: 2026-10-14 16:26 (Athens/Greece time): The hand-typed stamp, the maintenance rule and the changelog table are replaced by the stamp program (S2); the last five changes are in SKILL.md and the full history is in the repo's history folder.
