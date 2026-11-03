# outlook-emails-skill: Phase A findings (Operation Skill Restructure, 03/11/2026)

Read-only analysis of the LIVE skill (Paul's synced copy, v7, 14/10/2026 16:00 build). No client data is kept here. Nothing has been changed or built.

## Facts
- Live skill: `SKILL.md` 72 lines, 9,560 bytes, ONE file, no script. 94 single rules (sentences) are the baseline for the rule-by-rule check (archived word for word in `SKILL.2026-10-14.md`).
- Job: whenever Claude sends, or drafts for Paul to send, an email that needs a reply from someone else, Claude tracks it: notes who, which thread and the date; tells Paul when a real reply arrives; flags it if nothing comes back in a day or two. The tool is the scheduled-task tool (`create_trigger`), because a chat does not stay open.
- Receives from: any skill that sends or drafts a chasing email. `client-teams-transcript-skill` (live v35) points to it twice (revised-quote requests, correspondence). `client-pipeline-board` (page `outstanding-tracking.md`) says its own daily trigger "mirrors" this skill. Uses `paul-email-signature` (signature rules) and the Microsoft 365 connector (`outlook_email_search`, `read_resource`).
- Client data scan: none (only Paul's own address in the text).

## Flaws found
Contradicts Paul's decisions or other skills (serious):
1. **The Signatures section is out of date.** It says Claude adds no signature and Paul pastes his own. `paul-email-signature` says an Exchange rule adds his full signature to every draft made with the Microsoft 365 tools. Pasting a second one would show it twice.
2. **Two different tracking recipes for the same thing.** This skill: an HOURLY check per email thread, deleted when all have replied. `client-pipeline-board/outstanding-tracking.md`: ONE DAILY trigger per client, plus a folder-drop check, "bound to this chat". Nothing says which one wins, and the board's own page says its recipe is untested on a live client.
3. **A third pointer.** `client-teams-transcript-skill` tells Claude to "follow `outlook-emails-skill` tracking" for revised-quote requests and correspondence, without saying which recipe.
4. Rule 9 (changes through the `propose_skills` card) conflicts with S7 (changes only in Claude Code, uploaded as a zip).
5. **"Fold it into his daily brief."** The silence flag may be "folded into his next daily brief", but the `morning` skill does not read scheduled tasks or any tracking list. That hand-over does not exist.
Nothing forces the rules (text only):
6. Every step is left to the chat: noting who/thread/date, creating the scheduled task, the reply wording, the silence check. The Delivery gate (5 checks) is the chat reporting on itself; "the scheduled task was confirmed as created" is not proven.
7. **The recurring check has no end.** It deletes itself only when everyone being chased has replied. If one person never answers it keeps looking every hour for ever. Each check is a whole chat session that spends your tokens.
8. Vague wording a program must fix: "a business day or two", "roughly 24-48 hours", "a sensible morning time" (whose morning: Athens or South Africa?), "genuine reply" and "substantive" (no list of what is an auto-reply, out-of-office or bounce).
9. **Push notification may not work as written.** The scheduled-task tool allows `notifications: {"push": true}` only on tasks that start a fresh session each time; the live text does not say which kind to create. The board's page says "bound to this chat". Unproven from here.
10. "Open it via the read resource tool, which marks it read" so the same reply is not reported twice. That marks PAUL'S OWN email as read as a side effect, and it is a fragile way to avoid double reports (dropping the sender once they replied would do it).
11. Only one route to read mail (the Microsoft 365 connector). The Zapier Office 365 tools can create a draft or send, not search. No access log, no fallback, and nothing says what to do if the search fails (it must never be read as "no reply").
12. Whether a given email "requires a response" is a judgement; nothing records the reason.
Standards and clutter:
13. About 40% of the 72 lines are the copied "universal rules" and Delivery gate. The stamp and version are typed by hand (S2); the full changelog is said to live in a project file outside the skill (could not be checked). Paul's own address sits in the text.
14. No tests, no checker, no run state.

## Duplications between skills
- The scheduled reply-check: this skill and `client-pipeline-board` (`outstanding-tracking.md`), plus the pointers in `client-teams-transcript-skill`. Exactly one skill should own it.
- The signature rule: this skill's Signatures section and `paul-email-signature`.

## Score against the 13 ingredients
Full 0. Partial 6 (1 short entry page, 2 inputs, 5 evidence, 7 short means short, 10 one reply one question, 12 history outside). Missing 5 (3 step driver, 6 built by program, 9 one checker, 11 tests, 13 package and upload). Not applicable 2 (4 reading lock, 8 sorted actions).

## What a program CAN and CANNOT do here (honest)
- CAN: force the steps, build the tracking plan the same way every time (the check times, the flag time with weekends skipped, the stop date), build the self-contained instruction that the later check runs, and compare what the scheduled-task tool returned (id, schedule, notifications) with the plan.
- CANNOT: prove that a later scheduled check really runs, finds a reply, or that the phone alert arrives. That happens later, in another session. It stays attested until one real tracked email shows it.

## Yes/No list for Paul (recommended answers in brackets)
1. **Who owns reply tracking?** (A) This skill owns the whole scheduled reply-check; the board's page and the Teams skill later point to it; the program can also take an optional client folder for the "dropped file" check the board does. (B) Leave both as they are. (A) The catch: the board's page changes in a later step, not now.
2. **How often does it look?** Today: every hour, all day, no end. Recommend: every hour on weekdays 08:00 to 17:00 South African time, and stop for good after 5 business days, with a last message "still no reply, I have stopped checking". Fewer runs also means fewer of your tokens. (Yes)
3. **When is "nothing came back" flagged?** Recommend: 09:00 Athens time on the second business day after sending (weekends skipped, public holidays not), as a phone alert only (the daily brief is not involved). (Yes)
4. **Stop marking your own mail as read.** Once a sender has replied they are dropped from the list, so the same reply is not reported twice. The summary is read without relying on read/unread. The catch: the connector may still mark a message read when opened; I cannot prove either way from here. (Yes)
5. **Signatures section:** drop it, keep one line "no signature is typed; see `paul-email-signature`". (Yes)
6. **Mail search failing:** if the Microsoft 365 search fails, the check says so and keeps looking next time; it never reports "no reply" from a failed search. (Yes)

## Status
Phase A report given to Paul 03/11/2026.

## Paul's answers (03/11/2026)
"Agree to all": yes to 1 to 6 as recommended. (1) This skill owns the whole scheduled reply-check (the board's page and the Teams skill later point to it; optional client folder for the dropped-file check). (2) Hourly on weekdays 08:00 to 17:00 South African time, stop for good after 5 business days with a last message. (3) "Nothing came back" is flagged at 09:00 Athens time on the second business day after sending, phone alert only. (4) No dependence on read/unread: a sender who replied is dropped from the list. (5) The Signatures section goes; one line points to `paul-email-signature`. (6) A failed mail search is reported as a failure, never as "no reply".

Found while planning (not in the Phase A report): the live text never says the scheduled check may use the Microsoft 365 connector. The scheduled-task tool has a setting for which connectors a fired session may use; without it the check may not be able to read Outlook. The plan sets it (Microsoft 365 only) and asks Paul to approve that.

Next: Phase B (plan) given to Paul 03/11/2026, waiting for his approval.
