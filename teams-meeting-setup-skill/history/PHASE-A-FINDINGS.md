# teams-meeting-setup-skill: Phase A findings (Operation Skill Restructure, 03/11/2026)

Read-only analysis of the LIVE skill (Paul's synced copy, 14/10/2026 16:26 build). No client data is kept here. Nothing has been changed or built.

## Facts
- Live skill: `SKILL.md` 156 lines, 15,454 bytes, about 2,600 words, ONE file, no script. 156 single rules (sentences) are the baseline for the rule-by-rule check.
- Job: once a follow-up (2nd or later) appointment date and time is confirmed, create the real Outlook calendar event with a Teams meeting attached, addressed to the client only. Creating it with the client as attendee SENDS the invite at once, so Paul's yes comes first. Then log it and tell Sitamah.
- Receives from: `client-pipeline-board` (chains to it when a follow-up date is confirmed) and `client-teams-transcript-skill` (suggests it when a new appointment was agreed). Uses `paul-email-signature` (the signature is added by an Exchange rule).
- Tool: `outlook_create_event` / `outlook_update_event` of the Microsoft 365 connector. The connector holds `Calendars.ReadWrite` (checked 03/11/2026).
- Client data scan: none (only Paul's own address and "[Client Name]" placeholders).

## Flaws found
Contradicts Paul's decisions or other skills (serious):
1. **Two senders of the same invite.** Paul decided on 02/11/2026 that the follow-up appointment is an action for Sitamah at every meeting (she books it, or sends the Teams meeting request), and `client-teams-transcript-skill` v35 now writes that action. This skill sends the invite itself from Paul's calendar. If both happen, the client gets two invites.
2. **Three different "tell Sitamah" messages around one meeting:** the Teams skill's "Appointment Completed" message, the action "Sitamah to set up the follow-up appointment", and this skill's own Teams message to Sitamah after sending the invite (wording is in another skill's page). It is not stated whether that last message needs Paul's yes (S10).
3. Rule 9 (changes through the `propose_skills` card) conflicts with S7 (changes only in Claude Code, uploaded as a zip).
4. The subject labels differ from the eight planning areas used elsewhere ("Investments" and "STI" here; "Investment" and "Short-Term" in the Planner note and the Fact Find).
Nothing forces the rules (text only):
5. The invite is a REAL SEND, yet everything is built by hand each time: subject, time zone, body, attendee, duration, `isOnlineMeeting`, `bodyType`. Correctness rests on a 10-point checklist that the chat reports about itself.
6. Where the facts come from is vague: "client name exactly as captured in the Fact Find", "the FF-captured personal email", "open product lines", "outstanding items", "met or spoke". Nothing proves any of them. The Fact Find is now the Fact Find Transcript PDF, which a program can read (name, surname, personal email).
7. Several rules a program can compute but the chat decides: the opening line by the real gap (same day, yesterday, longer), the "&" and comma joining of topics in the fixed order, duration exactly 1 hour, time zone `Africa/Johannesburg` on both start and end.
8. "Log under the Fact Find card's Actions Taken": it does not say in which system now (the pipeline board's card?). Not checkable.
9. There is one route only (the Microsoft 365 connector) and no step for what to do when the tool fails.
Standards and clutter:
10. About 40% of the 156 lines are the generic "universal rules" and the Delivery gate copied into every skill. The time-zone explanation alone is 12 lines.
11. The stamp is typed by hand (S2) and the changelog archive `claude/teams-meeting-setup-skill-changelog.md` is a project document outside the skill (could not be checked).
12. The signature paragraph repeats what `paul-email-signature` already says.

## Duplications between skills
- Who sends the follow-up invite: this skill, Sitamah's action (Teams skill), and the board's hand-off.
- Messages to Sitamah: this skill step 6, `client-pipeline-board`'s `sitamah-messaging.md` and the Teams skill's message.
- The reschedule rule (`outlook_update_event`, never delete and recreate) is written here and in `client-pipeline-board`.
- The signature rule is written here and in `paul-email-signature`.

## Score against the 13 ingredients
Full 0. Partial 6 (1 short entry page, 2 inputs, 5 evidence, 7 short means short, 10 one reply one question, 12 history outside). Missing 5 (3 step driver, 6 built by program, 9 one checker, 11 tests, 13 package and upload). Not applicable 2 (4 reading lock, 8 sorted actions).

## Yes/No list for Paul (recommended answers in brackets)
1. **Who sends a Teams follow-up invite?** (A) This skill, from your calendar after your yes; the Teams skill's action for Sitamah later changes to "Sitamah books a physical appointment, or confirms the client accepted the invite". (B) Sitamah sends it, and this skill only prepares the invite for her. (A) The catch: it means changing the live Teams skill's action line later.
2. Drop the copied generic rules and rule 9; keep the standing rules (the invite is a real send so Paul's yes comes first, `Africa/Johannesburg`, exactly 1 hour). (Yes)
3. A program builds the whole invite (subject, body, time zone, duration, attendee, `isOnlineMeeting`, `bodyType`), shows it to Paul, and the chat sends exactly that through `outlook_create_event` after his yes. The program then checks what the tool returned against what was approved. The catch: the program cannot press send itself. (Yes)
4. The client's name and personal email come from the Fact Find Transcript PDF (read by the program). The topics, outstanding items, how the last contact happened (met or spoke) and the date and time come from Paul or the follow-up summary and are typed in with their source. (Yes)
5. The message to Sitamah about the invite is shown to Paul in the same reply as the invite, so one yes covers both. (Yes)
6. Where is the confirmed meeting logged now? (a) as today, on the board's Fact Find card; (b) nowhere, the calendar is the record. (Paul to say)
The subject labels stay as they are now ("Investments", "STI"): they are client-facing and already in use. (No question)

## Status
Phase A report given to Paul 03/11/2026.

## Paul's answers (03/11/2026)
"Agree to all, except 6: keep it as today": yes to 1 to 5 as recommended (A: this skill sends a Teams follow-up invite from Paul's calendar after his yes, and the Teams skill's action for Sitamah changes later; drop the generic rules and rule 9; a program builds the invite and the chat sends exactly it, the program checks what the tool returned; name and personal email from the Fact Find Transcript PDF, the rest typed with its source; the Sitamah message shown in the same reply, one yes covers both). 6: the confirmed meeting is logged on the board's Fact Find card as today.

Next: Phase B (plan) given to Paul 03/11/2026, waiting for his approval.
