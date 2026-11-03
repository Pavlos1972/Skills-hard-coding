# Operation Skill Restructure

**APPROVED by Paul, 03/11/2026 ("Yes, save it").** This is the fixed procedure Claude Code applies, strictly and in this order, to EVERY skill that is restructured. Call it by this name: "Operation Skill Restructure". Nothing is added, skipped or swapped. Changes to this list are made only when Paul asks.

It sits on top of SKILL-STANDARDS.md (the standards S1 to S16) and SKILL-TEMPLATE.md (the 13 ingredients). If anything disagrees, SKILL-STANDARDS.md wins.

## Before I start a skill
1. Paul names the skill and says go. One skill at a time.
2. I give the skill's full name and what it does in two lines.
3. I give Paul its rough size (small, medium or big) and roughly how many tokens it will cost. I wait for his yes.
4. No helpers (subagents), from start to finish.

## Phase A: Read and analyse (change nothing yet)
1. Read the live skill completely: the main text, its scripts and all its files. Note the line count and the file count. (Paul's current skills: read-only copies under `/root/.claude/skills/synced/*/<skill-name>/`.)
2. Write down what it is for, what feeds it and what it produces. Note which other skills (full names) it hands over to or receives from.
3. Split the old text into single rules (sentences). This is the baseline, so every old rule can be tracked.
4. Look for these flaws and list each one with where it is:
   - Rules that contradict each other, or contradict another skill.
   - Outdated rules that Paul's later decisions replaced.
   - Steps Claude can skip or do from memory, because nothing forces them.
   - "Check" or "make sure" rules with no way to prove them.
   - Vague wording and missing templates.
   - Repeated text inside the skill.
   - No dated stamp, no access routes, or facts with no source.
   - Client data inside the skill (names, ID numbers, phone numbers, emails, real documents).
   - Scripts Claude is allowed to rewrite during a run.
   - Long text that should live on separate pages.
5. Look for duplications between skills. Does another skill make the same output or message? Exactly one skill must own each output.
6. Score the skill against the 13 ingredients: full, partial or missing.
7. Give Paul a Findings Report in plain words: the flaws, the duplications, what stays, what goes, and a yes/no list for anything uncertain. Wait for his answers. Nothing is built before his yes.

## Phase B: Plan
1. Give Paul ONE recommended route and its honest catch.
2. List the program's steps, what the checker will prove and what can only be attested.
3. Paul approves it before I build.

## Phase C: Build, in one pass
1. A short entry page: index, the "Last updated" line and standing rules, one line each.
2. Detail moves into reference pages that the program shows at the right step.
3. A step-by-step program that cannot skip a step and keeps its run state on disk.
4. Access routes in order (computer or OneDrive, Microsoft 365, Zapier). Every try is logged. Client facts come from the client's file first, and Paul is asked last.
5. A reading lock wherever the skill reads long documents.
6. Every output is built by program from one data file, with the same look every time.
7. Every fact has a source. Nothing is invented.
8. One checker prints PASS or FAIL. It separates what it proved from what was only attested. **The audit report posted in the chat after the skill has run is SHORT (Paul, 03/11/2026): one-liners in point form, each with a green tick (✅) or a red cross (❌). No long printout in the reply.** The program writes that short audit itself (one line per check) and keeps the full record on disk in the run folder. Anything only attested (not proven by the program) goes on ONE closing line, "Only attested (not proven): ...", so nothing is overclaimed.
9. One reply, one question. Nothing is sent without Paul's yes. Teams messages go through Zapier only.
10. Each duplicated output is moved to its one owner skill, and the other skills point to it.
11. House conventions: DD/MM/YYYY, R for money, Athens time, actions owned by Sitamah.
12. No client data in the skill or the repo. Test data uses invented people only.
13. The stamp is set by a program in Athens time and never typed. Every run says its version first.
14. The old text is archived outside the zip.

## Phase D: Prove (ONE test only)
1. Lint (an automatic structure check): index, stamp, steps, no client names.
2. Rule-by-rule check: a program compares every old rule with the new skill. Each is kept, reworded with a reason, or dropped with a reason. Nothing is left unaccounted for. Anything uncertain goes to Paul as a yes/no list.
3. ONE end-to-end test on invented data, from start to PASS, run once in the background.
4. If that one test fails, fix the cause and run the same test again (Paul was asked to correct this reading: it stands unless he says otherwise). Never add more tests, mutation checks or review rounds.

## Phase E: Package and hand over
1. Package the zip.
2. Run the one test on the unpacked zip, because that is what Paul uploads.
3. Check the real folder name with Paul, then make the upload brief (`tools/make_upload_brief.py <zip> --folder "<path>"`). Paul's real folder for the Fact Find skill is `ff-population-transcript-skill`: do not guess.
4. Send Paul the zip, the brief and a plain summary: what changed, what was removed, what is proven, what is only attested, and the open questions.
5. Paul saves the zip and pastes the brief into the Chrome chat. It uploads the skill and runs a before-and-after test. Paul pastes its report back.

## Phase F: Close out
1. Record the result in the memory files: status, version, what changed and open questions.
2. It stays "uploaded (reported)" until Paul says it is live.
3. Ask Paul: "Are you ready for the next skill?" Choose it together. Ask permission before starting Operation Skill Restructure on it.
4. If a real run shows a gap, Paul tells me. I fix it by hand in one pass, with no helpers.

## Always, during the whole operation
1. One skill at a time. Never touch another skill.
2. Simple words, one recommendation with its catch, short answers, one question at a time.
3. Report what was checked and what was only attested.
4. Never say "done" without the checker's PASS, and never say "live" before Paul does.
5. Side issues are written down and told to Paul. Do not chase them.
6. **Audit reports in the chat are SHORT (Paul, 03/11/2026):** one-liners in point form, each with ✅ or ❌, one closing line for what is only attested. Never a long printout. This applies to every skill built under this Operation.
7. Update the memory files after every phase, not only at the end.

## Progress (update after every phase)

| Skill (full name) | Operation Skill Restructure | Status |
|---|---|---|
| `client-teams-transcript-skill` | Built BEFORE this list existed (heavier method). Not redone unless Paul asks. | v35 LIVE (Paul confirmed 03/11/2026) |
| `ff-population-transcript` | Built BEFORE this list existed (heavier method). Not redone unless Paul asks. | v33 uploaded 03/11/2026 (reported); NOT confirmed live; Paul runs it on a real client first |
| `fact-find-summary` | DONE 03/11/2026 (Phases A to F, no helpers, one test passed on the source and on the unpacked zip). Program reads the Fact Find Transcript PDF (needs `pdfplumber`), builds the nine sections, recomputes totals, draws an A4 PDF; SHORT audit of ticks and crosses; Planner note and Sitamah message left this skill; follow-up owners Cameron, CL, Valerie, Lizelle (Lizelle replaces Martin). Rule-by-rule check: 392 old rules, 13 kept, 93 reworded, 286 dropped on record, 0 unaccounted. | v18 UPLOADED 03/11/2026 (reported by a Chrome chat; v17 before; 15 files; test chat correct). NOT confirmed live by Paul: he runs it on a real client first. Backup zip of the old 2 files held by Paul. Open: 5 yes/no design questions in `fact-find-summary/history/CHANGES-FOR-PAUL.md`. |
| `client-transcript-download` | Operation Skill Restructure applied 03/11/2026 (Phases A to E, no helpers, ONE test passed on the source and on the unpacked zip): `client-transcript-download` is BUILT and PACKAGED, not uploaded, not live. A program drives 6 steps (identify, fetch, check, name, save, final): fetch routes Microsoft 365 then Zapier then Claude in Chrome, every try logged (the connector holds OnlineMeetingTranscript.Read.All; unproven until one real try); the transcript must be complete (last time stamp within 2 minutes of the meeting length, no gap over 10 minutes); the file name is derived; a text transcript from the connector is written as a .docx; the save is checked (client's own 2. Fact Find folder, listed size equals local, nothing overwritten); a SHORT audit of ticks and crosses ends the job and names the next skill. Rule-by-rule check: 105 old rules, 24 kept, 37 reworded, 44 dropped on record, 0 unaccounted. Lint PASS. Zip `releases/client-transcript-download-20261103-1125.zip` (11 files, 24,408 bytes). Backup of the old live file made (outside the repo). UPLOADED as v5 on 03/11/2026 by a Chrome chat (reported by that chat, pasted by Paul): before = v4, 1 file, "Last updated: 2026-10-14 14:41"; replace box "This saves a new version of client-transcript-download. Earlier versions stay available in the skill's version history. Current: 68 lines - This file: 60 lines."; after = v5, 11 files, still ONE entry (31 skills), "Last updated: 2026-11-03 11:25 (Athens time)" and first section "Index" (the test chat answered correctly; it labelled the loaded skill "(plugin)", which the before chat did not). NOT confirmed live by Paul (he runs it on a real client first). The first real run also decides which fetch route works (Microsoft 365, Zapier or Chrome). Yes/no list (2 questions): `client-transcript-download/history/CHANGES-FOR-PAUL.md`. Never say live before Paul confirms. | PHASES A TO F DONE (03/11/2026). v5 uploaded (reported); NOT confirmed live. NEXT: ask Paul whether he is ready for the next skill. Open: 2 yes/no design questions in `client-transcript-download/history/CHANGES-FOR-PAUL.md`. |
| `teams-meeting-setup-skill` | Operation Skill Restructure applied 03/11/2026 (Phases A to E, no helpers, ONE test passed on the source and on the unpacked zip): `teams-meeting-setup-skill` is BUILT and PACKAGED, not uploaded, not live. A program drives 7 steps (find client, facts, build, show, send, log, final): it reads the client's name and personal email from the Fact Find Transcript PDF (routes computer, Microsoft 365, Zapier, every try logged), builds the whole invite (subject in the fixed order, Africa/Johannesburg on start and end, exactly 1 hour, the client only, Teams on, date-aware opening line, no link or signature), shows it with the message to Sitamah and ONE question, and will not take Paul's yes unless he was shown exactly this invite; the checker compares what the Microsoft 365 tool returned with what he approved and prints a SHORT audit (ticks and crosses). A reschedule updates the existing event in place. Rule-by-rule check: 154 old sentences, 6 kept, 99 reworded, 49 dropped on record, 0 unaccounted. Zip `releases/teams-meeting-setup-skill-20261103-1209.zip` (13 files). 5 yes/no questions in `teams-meeting-setup-skill/history/CHANGES-FOR-PAUL.md`. | PACKAGED 03/11/2026 12:09; backup zip of the old file made; brief made 03/11/2026 (folder `teams-meeting-setup-skill`, as Paul confirmed). v8 UPLOADED 03/11/2026 (reported by a Chrome chat; v7 before; 13 files; test chat correct). NOT confirmed live by Paul: he runs it on a real client first. Open: 5 yes/no questions in `teams-meeting-setup-skill/history/CHANGES-FOR-PAUL.md`; the live Teams skill's Sitamah action line must change once this one is live. |
| `outlook-emails-skill` | Operation Skill Restructure applied 03/11/2026 (Phases A to E, no helpers, ONE test passed on the source and on the unpacked zip): `outlook-emails-skill` is BUILT and PACKAGED, not uploaded, not live. A program drives 6 steps (email, plan, show, create, readback, final): it records the email with its source, builds two scheduled-task files (an hourly weekday watcher, 08:00 to 17:00 South African time, that drops senders who replied and stops by itself after 5 business days; a one-time silence flag at 09:00 Athens time on the 2nd business day), shows the plan with no question (standing rule), and the checker compares what `list_triggers` shows with the plan and prints a SHORT audit. Both checks start a fresh chat and may use the Microsoft 365 connector only. Rule-by-rule check: 94 old sentences, 3 kept, 46 reworded, 45 dropped on record, 0 unaccounted. Zip `releases/outlook-emails-skill-20261103-1301.zip` (12 files). 3 yes/no questions in `outlook-emails-skill/history/CHANGES-FOR-PAUL.md`. The scheduled-task tool's acceptance of the settings is unproven until one real tracked email. | PACKAGED 03/11/2026 13:01; backup zip of the old file made; brief made 03/11/2026 (folder `outlook-emails-skill`, as Paul confirmed). v5 UPLOADED 03/11/2026 (reported by a Chrome chat; v4 before; 12 files; test chat correct). NOT confirmed live by Paul: he runs it on a real tracked email first. Open: 3 yes/no questions in `outlook-emails-skill/history/CHANGES-FOR-PAUL.md`; the scheduled-task tool's acceptance of the settings is unproven until then. |
| All other skills | NOT started. Paul names the next one. | |

## Skills still to do (sizes of the live copies, checked 03/11/2026; Paul names the next one)

| Skill (full name) | SKILL.md | Files | All files |
|---|---|---|---|
| `cameron-short-term-skill` | 100 lines | 1 | 17 KB |
| `complete-applications-skill` | 206 lines | 5 | 174 KB |
| `client-pipeline-board` | 245 lines | 11 | 105 KB |
| `om-optimal-ra-proposal` | 253 lines | 6 | 251 KB |
| `client-review-notes` | 297 lines | 1 | 19 KB |
| `om-tax-free-skill` | 333 lines | 4 | 77 KB |
| `investment-comparisons-skill` | 431 lines | 1 | 27 KB |
| `rgar-skill` | 434 lines | 4 | 98 KB |
| `wr-sroa-builder` | 534 lines | 6 | 189 KB |
| `life-policy-schedule-analyzer` | 874 lines | 1 | 56 KB |
| `wr-roa-builder` | 1,072 lines | 7 | 238 KB |
| `life-insurer-comparison` | 1,076 lines | 1 | 68 KB |
Others on Paul's list (not yet sized): `advicetech-website-knowledge`, `alpha-bank-statements`, `astute-summary-report-skill`, `managing-generali-checkups`, `nedbank-current-account-categorization`, `paul-email-signature`, `qb-monthly-budget`. Forgotten by Paul: `planner-interim-procedure`, `ff-to-ff-populate`.

## Practical notes learned (NOT part of the approved list; they only record what happened. Paul decides if any becomes a step.)
1. **Backup before an upload.** On 03/11/2026 the replace box for `fact-find-summary` (v17) said "What it overwrites can't be restored afterwards", unlike the other two uploads (which said earlier versions stay in the version history). From now on I make a backup zip of the live skill's files (from `/root/.claude/skills/synced/...`), outside the repo, and send it to Paul with the zip and the brief, unless he says not to.
2. **The brief's approval covers only the box that mentions the version history.** A different box means STOP and ask Paul (the Chrome chat did exactly that).
3. **Ask Paul for the real folder name** before making a brief. His folders are `<skill>-skill` (for example `ff-population-transcript-skill`, `fact-find-summary-skill`).
4. **The packager's self-test runs `run.py preflight`:** every program-driven skill needs that command.
5. **A skill whose program reads PDFs needs `pdfplumber`** in the chat's environment. The self-test at the start checks it; the first real run is the real test.
6. **Check old example scripts for a real person's details in Phase A** (13-digit numbers, emails, phone numbers). Never archive such a file in the repo; the claude.ai version history still holds it.
7. **The rule-by-rule check** uses `tools/inventory.py` with `history/changes.json` (reworded) and `history/decisions.json` (dropped, by line range). Build the prefixes with the tool's own `plain()` function, or they will not match.
8. **A `fact-find-summary` run ends with a SHORT audit** (ticks and crosses): that is the pattern for every skill built under this Operation.
9. **Paste the upload brief into the Chrome chat.** On 03/11/2026 the Chrome chat for `teams-meeting-setup-skill` found no brief in the folder (only the zip, the backup and the change list) and worked from Paul's request instead. It still did the right thing (one replace box naming only that skill, nothing deleted), but the brief is what pre-approves the replace box and sets the before/after test, so Paul pastes it.

## Running log
- 03/11/2026: `outlook-emails-skill` uploaded as v5 (reported by a Chrome chat; again no brief was pasted, the chat used Paul's request); not confirmed live. Operation Skill Restructure Phases A to F done for this skill. Asked Paul whether he is ready for the next skill.
- 03/11/2026: `outlook-emails-skill` brief made (folder `outlook-emails-skill`) and sent with the zip and the backup. Waiting for the upload report.
- 03/11/2026: `outlook-emails-skill` Phases C to E done in one pass (no helpers, ONE test, passed on the source and on the unpacked zip). Zip made (12 files); backup of the old file made. Asking Paul for the real folder name before the brief.
- 03/11/2026: `outlook-emails-skill` Phase B plan approved by Paul ("I approve", including the Microsoft 365 permission for the checks and no question per email). Building.
- 03/11/2026: `outlook-emails-skill` Phase A answers recorded (agree to all six). Phase B plan given; waiting for approval.
- 03/11/2026: `outlook-emails-skill` Phase A done (no helpers, no tests). Main finding: its Signatures section contradicts `paul-email-signature`, and its hourly never-ending check clashes with the board's daily per-client recipe. Waiting for Paul's answers.
- 03/11/2026: Progress table, sizes table and notes brought up to date (the two finished skills removed from "Skills still to do"). Next skill proposed to Paul: `outlook-emails-skill` (smallest not started); waiting for his yes.
- 03/11/2026: `teams-meeting-setup-skill` uploaded as v8 (reported by a Chrome chat; the chat had no brief and used Paul's request); not confirmed live. Operation Skill Restructure Phases A to F done for this skill. Asked Paul whether he is ready for the next skill.
- 03/11/2026: `teams-meeting-setup-skill` brief made (folder `teams-meeting-setup-skill`) and sent with the zip and the backup. Waiting for the upload report.
- 03/11/2026: `teams-meeting-setup-skill` Phases C to E done in one pass (no helpers, ONE test, passed on the source and on the unpacked zip). Zip made (13 files); backup of the old file made. Asking Paul for the real folder name before the brief.
- 03/11/2026: `teams-meeting-setup-skill` Phase B plan approved by Paul ("I approve"). Building.
- 03/11/2026: `teams-meeting-setup-skill` Phase A answers recorded (agree to all; logging stays as today). Phase B plan given; waiting for approval.
- 03/11/2026: `teams-meeting-setup-skill` Phase A done (no helpers, no tests). Main finding: two senders of the same follow-up invite (the skill and Sitamah's action). Waiting for Paul's answers.
- 03/11/2026: `client-transcript-download` uploaded as v5 (reported); not confirmed live. Operation Skill Restructure Phases A to F done for this skill. Asked Paul whether he is ready for the next skill.
- 03/11/2026: `client-transcript-download` brief made (folder `client-transcript-download-skill`) and sent with the zip and the backup. Waiting for the upload report.
- 03/11/2026: `client-transcript-download` Phases B to E done in one pass (no helpers, one test, passed on source and on the unpacked zip). Zip made (11 files); backup of the old file made. Asking Paul for the real folder name before the brief.
- 03/11/2026: `client-transcript-download` Phase A answers: Paul agreed to all five. Phase B plan given; waiting for approval.
- 03/11/2026: `client-transcript-download` Phase A done (no helpers, no tests). Main finding: the M365 connector now holds OnlineMeetingTranscript.Read.All, so the old 'Chrome only' rule is outdated (unproven until one real try). Waiting for Paul's answers.
- 03/11/2026: Paul said "Update MD doc. then next skill". This file updated (Progress row cleaned, sizes of the skills still to do, practical notes). Next skill: Paul names it; recommendation given.
- 03/11/2026: `fact-find-summary` uploaded as v18 (reported); not confirmed live. Operation Skill Restructure Phases A to F done for this skill. Asked Paul whether he is ready for the next skill.
- 03/11/2026: Paul approved replacing `fact-find-summary` (v17) at the can't-be-restored box after saving the backup zip. Instruction sent for the Chrome chat to finish the upload.
- 03/11/2026: `fact-find-summary` upload paused at an unexpected replace box (overwrite cannot be restored). Backup zip of the old 2 files sent to Paul. Do not click Upload and replace until Paul says so.
- 03/11/2026: `fact-find-summary` Phases B to E done in one pass (no helpers, one test, passed on source and on the unpacked zip). Zip `releases/fact-find-summary-20261103-0941.zip` and its brief sent; folder `fact-find-summary-skill`. Waiting for the upload report.
- 03/11/2026: `fact-find-summary` Phase A done (no helpers, no tests). Serious: the live skill says Dread Disease ABI 5% (Paul decided 3%), makes its own Teams message and Planner note (the Teams skill owns them), and its script holds a real person's details. Waiting for Paul's answers.
- 03/11/2026: Paul chose `fact-find-summary` as the next skill. Before Phase A: size and cost given, waiting for his go.
- 03/11/2026: procedure approved by Paul and saved. Lesson behind it: earlier work on `ff-population-transcript` ran six helper-driven review rounds and used far too many of Paul's tokens (see CHAT-NOTES.md). From now on: one test, no helpers.
