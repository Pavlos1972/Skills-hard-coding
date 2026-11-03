# What changed in the Outlook Emails skill, in plain words

For Paul. **Not uploaded, not live.** This is the program-driven version of `outlook-emails-skill` (Operation Skill Restructure, 03/11/2026). The old version stays in the skill's version history in claude.ai, and a backup of its file is sent with the zip.

## What the skill does now
Whenever Claude sends, or drafts for you to send, an email that needs a reply, a program sets up the tracking, with no question each time (your standing rule). It builds two scheduled checks, shows you the plan in a few lines, and then a checker compares what the scheduled-task tool returned with that plan and prints a **short audit** (green ticks and red crosses). Nothing is sent to anyone.

## The two checks (your answers 2 to 4)
- **The watcher:** every hour on weekdays, 08:00 to 17:00 South African time. A real reply alerts your phone with one line and that sender is dropped from the list. It **stops for good** at 17:00 on the 5th business day, with one last message ("no reply, I have stopped checking") if anyone is still silent, and then deletes itself. It no longer depends on read/unread, so it does not mark your mail as read on purpose.
- **The silence flag:** once, at 09:00 Athens time on the 2nd business day after sending (weekends skipped). It alerts your phone only if someone is still outstanding. The daily brief is not involved.
- Both start a **fresh chat each time** (so the phone alert can work) and may use the **Microsoft 365 connector only**, to read your Outlook (you approved this). Each instruction is written by the program and says what is NOT a real reply (automatic replies, out-of-office, bounces, read receipts, "we got your email" acknowledgements) and that a failed search is a failure, never "no reply".

## What a program now does that Claude did by hand
- Forces the order of the steps (record the email, build the plan, show it, create, read back, final check); none can be skipped.
- Refuses a missing or bad address, your own address, a date in the future, an email so old that the 5 business days are over, and a missing reason or source (if you cannot say why a reply is needed, the email is not tracked).
- Works out the business days (weekends skipped) and the Athens summer/winter time by itself.
- Compares what `list_triggers` shows (names, schedule, fire time, switched on, fresh chat, instruction text) with the plan.

## What left this skill
The nine copied generic rules and the Delivery gate (the program and the checker do their work), the "propose skills card" rule (changes are made only in Claude Code, standard S7), the hand-typed stamp, version and changelog, your own address in the text, and the whole **Signatures section** (your answer 5): one line now points to `paul-email-signature`.

## What stayed the same
The standing rule and its scope (quote requests, chases for documents or sign-off, "please confirm by X"; not purely informational notes), the scheduled-task tool, a phone alert only when something is found, several senders in one task, and the self-delete.

A program (`tools/inventory.py`) went through all 94 sentences of the old text: **3 are still there word for word, 46 are reworded (each with a written reason), 45 were dropped on purpose (each with a written reason), and none was lost without a record.** The records are `history/changes.json` and `history/decisions.json`; the full list is `history/INVENTORY-REPORT.md`.

## Your yes/no list
1. **Instruction wording for the checks** is mine (see `out/watch.json` in any run, or `scripts/track.py`). In particular "a genuine reply answers or acts on the request" and the list of what is not one. **OK? Yes / No.**
2. **A client folder is optional.** If you give a folder, the checks also look there for a dropped file (what the board does today). The board's own daily recipe is NOT changed in this upload, so until that later step both recipes exist. **OK? Yes / No.**
3. **Public holidays are not skipped** (only weekends). A holiday can make "2 business days" arrive one day early. **OK? Yes / No.**

## What I could not do or check
- **I cannot create the scheduled tasks from here.** The chat does, with exactly the program's settings. The first real tracked email is the real test of the tool: whether it accepts the fresh-chat, phone-alert, connector and South African time-zone settings. If it refuses any, the chat stops and shows you the exact error.
- **That the checks really run, find a reply and alert your phone cannot be proven now.** They run later, in other chats. The audit says so on its closing line.
- **That the watcher stops itself on the last day** rests on its own instruction. Each run is a chat that spends some of your tokens, which is why the checks are now limited to working hours and five business days.
- **The old "board" recipe still exists** in `client-pipeline-board/outstanding-tracking.md` (one daily trigger per client). Moving that page to point here is a later job, with that skill.
- Only one test was run, as agreed: one end-to-end run on invented data (the plan built exactly, weekends and the Athens summer/winter offsets, bad facts refused, a changed schedule or fire time caught, a hand-edited plan caught). Nothing was created anywhere.
