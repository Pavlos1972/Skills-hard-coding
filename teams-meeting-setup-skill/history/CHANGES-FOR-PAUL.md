# What changed in the Teams Meeting Setup skill, in plain words

For Paul. **Not uploaded, not live.** This is the program-driven version of `teams-meeting-setup-skill` (Operation Skill Restructure, 03/11/2026). The old version stays in the skill's version history in claude.ai, and a backup of its file is sent with the zip.

## What the skill does now
Once the follow-up date and time are confirmed, a program builds the Teams meeting invite, shows it to you with **one question**, and only after your yes does the chat create it in your Outlook calendar (the client is emailed at that moment). The same reply shows the message to Sitamah, so **one yes covers both**. A checker then compares what the Microsoft 365 tool sent back with the invite you approved and prints a **short audit** (green ticks and red crosses). A reschedule updates the existing event in place; it never deletes and recreates.

## What a program now does that Claude did by hand
- Forces the order of the steps (find the Fact Find, record the facts, build, show you, send, log, final check); none can be skipped.
- Reads the client's **name and personal email from the Fact Find Transcript PDF** itself (three routes tried in order and logged: computer, Microsoft 365, Zapier). If there is no usable email, it stops and asks you; it never guesses one.
- Builds the whole invite: subject `Client Name / topics` (labels in the fixed order, "Risk & RA", "Risk, RA & RGAR"), `Africa/Johannesburg` on start and end, **exactly 1 hour**, the client as the only attendee, Teams on, a date-aware opening line (earlier today, yesterday, or the date; "met" or "spoken"), the agenda in plain words, "what we need from you" only when each item has a source, no hand-written link, ID, passcode or signature.
- Refuses a date in the past, a follow-up that is not after the last contact, a topic outside the fixed list, and owed items with no source.
- Will not accept your yes unless you were shown **exactly** this invite and message; if anything is rebuilt, the earlier yes no longer counts.
- Compares the event the tool returned (id, subject, start, end, the client, Teams on) with what you approved.

## What left this skill
The nine copied generic rules and the Delivery gate (the program and the checker do their work), the "propose skills card" rule (changes are made only in Claude Code, standard S7), the hand-typed stamp and changelog, the long time-zone and signature explanations (shortened; the signature detail stays in `paul-email-signature`).

## What stayed the same
The invite is a real send and your yes comes first; `Africa/Johannesburg`; always 1 hour; the client only; Teams on; the Exchange rule adds your signature; Sitamah is told through Zapier (not Microsoft 365); the meeting is logged on the board's Fact Find card as today (your answer); a reschedule uses `outlook_update_event`.

A program (`tools/inventory.py`) went through all 154 sentences of the old text: **6 are still there word for word, 99 are reworded (each with a written reason), 49 were dropped on purpose (each with a written reason), and none was lost without a record.** The records are `history/changes.json` and `history/decisions.json`; the full list is `history/INVENTORY-REPORT.md`.

## Your yes/no list
1. **The wording of the agenda lines** is mine, in plain client words: Risk "Your life cover quote", RA "Your Retirement Annuity", Investments "Your investments", RGAR "Your retirement goal analysis", EGAR "Your education goal analysis", Medical Aid "Your medical aid and gap cover", Will "Your will", STI "Your short-term insurance". **OK? Yes / No.**
2. **A longer gap since the last contact always names the exact date** ("Great to have met with you on 20/10/2026."). The old text also allowed "It was great catching up with you recently." **OK to drop that one? Yes / No.**
3. **A reschedule does not touch the body of the invite**, so its last line still names the old date ("Below is the link to join the Teams meeting on ..."). The program warns you in the invite text. **OK to leave it? Yes / No.**
4. **The message to Sitamah** is an FYI in the board's style (no tag, ends "Nothing needed from you right now"), sent once through Zapier after your yes. **OK? Yes / No.**
5. **At most 5 agenda lines.** More than 5 topics need five short lines typed in. **OK? Yes / No.**

## What I could not do or check
- **The program cannot press send.** The chat creates the event through the Microsoft 365 tool; the checker can only compare what the chat reports back. That the tool was really called, and your yes as typed by the chat, stay attested.
- **I have not sent a real invite.** It would email a client. The first real run is the real test of the tool call, the Zapier message to Sitamah and the signature on the client's copy (the organizer's own calendar never shows it).
- **The three routes to the Fact Find are unproven** until one real run; the program supports all three and logs each try.
- **It does not check your calendar** for a clash, or the client's availability.
- **The live Teams skill still tells Sitamah to set up the follow-up** as an action. Once this skill is live, that action line has to change (your answer 1, option A). That is a later job, not part of this upload.
- Only one test was run, as agreed: one end-to-end run on invented data (a new invite and a reschedule, bad facts refused, a changed returned time caught, a hand-edited invite caught). Nothing was sent anywhere.
