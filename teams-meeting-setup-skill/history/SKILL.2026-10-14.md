<!-- The live skill text as of 14/10/2026 16:26 (Athens time), kept as the rule-by-rule baseline. -->
---
name: "teams-meeting-setup-skill"
description: "Creates the follow-up Teams meeting invite in Outlook Calendar for a Wealth Revolution client once the date is confirmed. Use when client-pipeline-board chains to it or Paul says 'set up the follow-up meeting'."
---

# Teams Meeting Set Up Skill

## Index

| Section | What it covers |
|---|---|
| Universal operating rules | Nine rules that apply to every step, and the Delivery gate (5 checks) |
| Last updated, maintenance rule, changelog | Athens stamp, how to edit this skill, five one-line rows |
| What this does | Creates the real Outlook event with a Teams meeting once a follow-up date is confirmed |
| 1. Subject line | Client name / short topic labels (table of product-line labels) |
| 2. Time zone | Always Africa/Johannesburg on start and end, and why |
| 3. Body | Body shape, date-aware opening line, agenda, what we need from you, Teams link, signature |
| 4. Attendee, duration, other fields | Client only, responseRequested, always 1 hour |
| 5. Sending is a real send | Show Paul the full invite and get his yes before outlook_create_event |
| 6. Logging and Sitamah | Fact Find card log, Teams message to Sitamah, reschedules via outlook_update_event |
| Verification | Ten checks to run before finishing |

## UNIVERSAL OPERATING RULES - READ FIRST, APPLY TO EVERY STEP OF THE TASK

*These rules come before everything else in this skill. They apply from the first message to the last, not just at the start, and they are repeated here at the top because long conversations get compressed and only the beginning of a skill survives. If anything below seems to conflict with these rules, these rules win.*

1. **Re-load this skill before you start, and again after any compression.** At the start of every run - and whenever the conversation has been summarised or compressed, or has run long - open this skill in full (Skill tool) and re-read it before you produce or change any deliverable. Never work from a summary of the rules or from memory of them.
2. **Source first - never invent.** Write only what is in the source material (transcript, quote, document, file) or in a named document this skill tells you to use. If a line is unclear, garbled or ambiguous, do not turn it into a fact: flag it to the user. "It seems implied", "it is usual" and "it would make sense" are not sources.
3. **Read before you write.** Read the source material completely and carefully - at least as many times as this skill requires - before drafting anything. Searching for keywords is not reading.
4. **Check before you claim.** Never tell the user something is done, saved, sent, visible or working until you have checked it yourself (open the file, list the folder, look at the screen). Say what you checked.
5. **Deliver everything this skill lists, every time.** A run is not finished until every deliverable this skill names has been produced AND handed over exactly the way this skill specifies (shown in chat, sent as a file in the chat, saved to the named folder). Before you reply, list each deliverable and confirm each was handed over.
6. **Every correction re-opens the whole task, not just the item.** When the user corrects anything: (a) go back to the source and re-check that point and everything related to it; (b) fix it everywhere it appears, in every deliverable; (c) re-run this skill's full checklist; (d) re-deliver every affected deliverable in full, as in rule 5. Never fix only the item named and stop.
7. **Never lower the standard.** A correction, a frustrated user, a short request or a "quick" task does not relax any rule in this skill.
8. **If a rule cannot be met, stop and say so.** State exactly which rule or step could not be completed and why. Never hand over partial work as if it were complete.
9. **Changes to a skill:** edit the existing skill, never create a new one. Update its "Last updated" stamp (Athens time) and changelog. Then put the full updated SKILL.md forward for the user to review and save using the propose_skills tool (the "Update skill" review card). Never say the change is live until the user confirms they saved it. If the card does not appear, say so plainly and ask the user how to proceed - do not claim it was delivered.

**Delivery gate for this skill (rules 5 and 6 applied):** a run is complete only when ALL of these are done and confirmed in one line each: (1) the invite was built to Sections 1-4 (subject, Africa/Johannesburg time zone on start and end, body, the client as the only attendee, 1-hour duration unless Paul specified otherwise); (2) the full invite (subject, date and time in SA time, duration, full body) was shown to Paul and he said yes BEFORE outlook_create_event was called (Section 5); (3) the event was created and the result was checked; (4) the logging was done and Sitamah was messaged on Teams once it was actually sent (Section 6); (5) the Verification checklist was run item by item. After ANY correction, rebuild the invite, show it to Paul again and get his yes before sending, then repeat (3) to (5).


**Last updated:** 2026-10-14 16:26 (Athens/Greece time)

> Maintenance rule: bump this timestamp and add a changelog row at the top (Athens time) on every edit — same convention as every other skill in this project.

**Changelog** (full original rows archived word for word in claude/teams-meeting-setup-skill-changelog.md)
| When (Athens time) | What changed |
|---|---|
| 2026-10-14 16:26 | Index added after the title, plain description, client name in the examples replaced with a placeholder, changelog rows shortened (Route 1 streamlining at Paul's request); no rule changed. |
| 2026-10-08 14:41 | Rule 9 now names the propose_skills review card and says never claim a change is live until Paul confirms. |
| 2026-10-08 14:25 | UNIVERSAL OPERATING RULES block and Delivery gate added at the top. |
| 2026-10-01 08:55 | Body template improved: accurate opening line (met vs spoke), short agenda, "what we need from you" list; the go-ahead question shows them too. |
| 2026-09-03 to 2026-09-04 | Created; duration fixed at 1 hour always; signature settled as automatic via the calendar transport rule. |

## What this does

Once a follow-up/2nd (or later) appointment date and time is confirmed for a client — from the Fact Find/transcript or from Paul directly — this skill creates the real Outlook calendar event with a Teams meeting attached, addressed to the client, so accepting it is all the client has to do.

## 1. Subject line

`{Client Name} / {short topic list}`

- **Client Name** exactly as captured in the Fact Find (e.g. "[Client Name]").
- **Topic list** — the open product lines this follow-up covers, short labels only, never the full product name and never an internal stage code:

| Product line | Short label |
|---|---|
| Life Cover | Risk |
| Retirement Annuity | RA |
| Investments | Investments |
| RGAR | RGAR |
| EGAR | EGAR |
| Medical Aid | Medical Aid |
| Will | Will |
| Short-Term Insurance | STI |

List only the lines actually open for this client at the time the meeting is set up, in the order above. Join naturally: two items get "&" ("Risk & RA"); three or more are comma-separated with "&" before the last ("Risk, RA & RGAR"); one line alone is just that label ("RA"). Example: `"[Client Name] / Risk, RA & RGAR"`.

Keep it short — a calendar subject, not a sentence. No "Follow-up," no "Meeting," no stage code — the entry being a meeting is already obvious from the calendar itself.

## 2. Time zone — always South Africa ("Harare, Pretoria")

Set both `start.timeZone` and `end.timeZone` on `outlook_create_event` to `Africa/Johannesburg` (the tool maps this IANA name to the Windows zone Outlook displays as **"(UTC+02:00) Harare, Pretoria"**). Never use Paul's own Greek zone, never the client's specifically, never leave it defaulted.

**Why this is deliberate, not an oversight:** South Africa Standard Time (SAST, UTC+2) does not observe daylight saving. Greece does observe EU daylight saving — EEST (UTC+3) roughly late March to late October, EET (UTC+2, same as SAST) the rest of the year.

Outlook always stores an event's real instant (UTC) and displays it back to each viewer converted into *their own* calendar's time zone. So:

- Creating the event with the zone set to SAST means the wall-clock time attached to the invite is always the real South African time — exactly what the client needs to see, in every month of the year.
- When Paul looks at his own Outlook (set to Athens time), the same event shows **one hour later** during the European summer (EEST) and the **same time** as SA during the European winter (EET = SAST = UTC+2). This is expected, correct behaviour — Outlook's normal per-viewer conversion — not a bug to fix.

## 3. Body

Adapt this shape — don't send Paul's own example wording verbatim if the specifics don't fit:

```
Hi {Client First Name},

{opening line — see below, date-aware and factually accurate}

As discussed, kindly accept the above Teams meeting request.

On the agenda:
- {open topic 1 in plain words}
- {open topic 2}

What we need from you before then:
- {outstanding client item 1}
- {outstanding client item 2}

Below is the link to join the Teams meeting on {DD/MM/YYYY}.
```

- **Opening line is date-aware and describes the contact accurately — never hardcode "yesterday."** Work out the real gap between the 1st (or most recent) appointment and today:
  - Same day → "Great to have met with you earlier today."
  - Previous calendar day → "Great to have met with you yesterday."
  - Longer gap → "Great to have met with you on {DD/MM/YYYY}." or a neutral "It was great catching up with you recently." if naming the exact date reads awkwardly.
  - Say "met" for a Teams/video appointment; use "spoke" / "spoken" only when the last contact really was a phone or WhatsApp call. If genuinely unclear how or when the last conversation happened, ask Paul rather than guessing.
- **Agenda:** 2-5 short bullets, the open topics in plain client language (e.g. "Your life cover quote", "Retirement Annuity and Tax-Free options", "Retirement goal analysis"). Never internal stage codes or product jargon.
- **What we need from you:** only items the client actually owes (e.g. confirm budget and any cover changes, send a statement, sign a form), taken from the Fact Find / the client's Planner Task checklist / the follow-up summary. Leave this block out entirely if nothing is outstanding — never invent items.
- The date in the closing line is the **follow-up meeting's own date** (DD/MM/YYYY), not the 1st appointment's date.
- **Never hand-write or fabricate a Teams link, meeting ID, or passcode.** Set `isOnlineMeeting: true` on `outlook_create_event` — Microsoft Graph generates the real join link/meeting ID/passcode and appends the standard "Microsoft Teams meeting / Join / Meeting ID / Passcode" block to the body automatically, directly after whatever body text is supplied. Never recreate that block manually, and never invent a placeholder link.
- `bodyType: "html"`, with a blank line between each paragraph (use line breaks rather than paragraph tags, per Paul's Outlook spacing preference; use ul/li only if the allowlist accepts it, otherwise "- " lines). This is also required for the signature described next to render as styled HTML rather than being downgraded to plain text.
- **Signature — confirmed working, applied automatically.** A dedicated Exchange transport rule ("Auto-signature - Calendar invites (Paul)": condition = message type is Calendaring AND sender is paulk@liferisk.co.za) appends Paul's full Wealth Revolution signature — including logo — to every calendar invite sent from his mailbox via `outlook_create_event`. Verified on a real invite received by a third-party attendee. Checking the *organizer's own* calendar entry will never show the signature, so always verify via a real third-party recipient. Do not hand-type a signature into the invite body — a hand-typed one would duplicate it. Detail lives in `paul-email-signature`.

## 4. Attendee, duration, and other fields

- `attendees`: the client only, `type: "required"`, using the FF-captured personal email — the same address General and product-line emails use. Never Sitamah, never Paul (he's the organizer automatically).
- `responseRequested: true` so the client's Accept actually reaches Paul.
- **Duration: always 1 hour, fixed — never a shorter default, even if the Fact Find/transcript names a shorter window.** This is a standing rule from Paul ("Meetings are always 1 hour long"). If Paul himself specifies a different length for a specific meeting, that explicit instruction overrides this default for that one invite only.
- Leave `location` blank (Graph fills in "Microsoft Teams Meeting" once `isOnlineMeeting` is set) and other fields at their defaults.

## 5. Sending the invite is a real send — get Paul's go-ahead first

There is no draft state for a calendar event with an attendee: the moment `outlook_create_event` runs with the client listed, Graph emails them the invite immediately.

So: once a follow-up date (and time, and topic list) is confirmed, show Paul exactly what would go out — subject, date/time in SA time, the (fixed 1-hour) duration, the full body text including the agenda and outstanding-items blocks — as the pending question: *"Ready to send [Client] the Teams meeting invite for [date] at [time] SAST (1 hour), covering [topics]?"* Only call `outlook_create_event` once Paul says yes.

If Paul later says he wants this to auto-send, that's his explicit call to make — don't assume it.

## 6. Logging and keeping Sitamah in the loop

- Log the confirmed meeting under the Fact Find card's Actions Taken (or the relevant product card) — subject, date/time (SAST), attendee, as separate short bullets.
- Message Sitamah on Teams once it's actually sent, per `client-pipeline-board`'s "Keeping Sitamah in the loop" (via the Zapier Teams connector). She's notified by Teams message, not added as an attendee or cc.
- If Paul later reports a reschedule, use `outlook_update_event` on the existing event id (never delete-and-recreate) so the client's already-accepted invite updates in place.

## Verification

- Subject: client name, forward slash, short topic labels only, matching the product lines actually open for this client right now.
- Time zone on both `start` and `end`: `Africa/Johannesburg` — never Paul's own zone, never the client's, never left blank.
- **Duration is exactly 1 hour** unless Paul explicitly specified a different length for this invite.
- Body: opening line matches the real gap AND the real type of contact (met vs spoke); agenda bullets match the open topics; outstanding items are real (or the block is omitted); closing date is the follow-up meeting's own date; no hand-written Teams link, meeting ID, or passcode.
- `isOnlineMeeting: true` and `bodyType: "html"` were actually set.
- Attendee is the client's FF-captured email only — not Sitamah, not Paul.
- Paul's explicit go-ahead (having seen the full body) was obtained before `outlook_create_event` ran.
- Signature applies automatically via the calendar transport rule; if a client reports it missing, check the rule per `paul-email-signature`.
- On a reschedule: `outlook_update_event` was used on the existing event.
- Sitamah was messaged on Teams once the invite was actually sent.