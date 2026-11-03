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
| `fact-find-summary` | Operation Skill Restructure applied 03/11/2026 (Phases A to E): the program-driven `fact-find-summary` is BUILT and PACKAGED, not uploaded, not live. A program reads the Fact Find Transcript PDF (`scripts/ffread.py`, needs `pdfplumber`), composes the nine sections with totals and follow-up owners (Cameron, CL, Valerie, Lizelle; Lizelle replaces Martin), draws an A4 PDF and a checker prints a SHORT audit of green ticks and red crosses. The Planner note and the Sitamah message left this skill (the Teams skill owns them). Rule-by-rule check: 392 old rules, 13 kept, 93 reworded, 286 dropped on record, 0 unaccounted. Lint PASS. ONE end-to-end test on invented data passed on the source and on the unpacked zip. Zip: `releases/fact-find-summary-20261103-0941.zip` (15 files, 38,533 bytes). The older interim text-update zip and brief are SUPERSEDED: do not upload them. Waiting for Paul to give the real upload folder name, then the upload brief is made. Yes/no list for Paul: `fact-find-summary/history/CHANGES-FOR-PAUL.md`. Never say live before Paul confirms. | PHASES A TO E DONE. Real folder `fact-find-summary-skill` confirmed by Paul 03/11/2026; upload brief made and sent with the zip. UPLOAD PAUSED 03/11/2026: the Chrome chat stopped at a DIFFERENT replace box ("This overwrites fact-find-summary with this file. What it overwrites can't be restored afterwards.", no line counts, no version-history note; the live skill is v17, 2 files). The brief's approval covered only the version-history box, so nothing was clicked. A backup zip of the old live skill's 2 files (outside the repo; its script holds a real person's details) was sent to Paul. WAITING for Paul's decision. |
| All other skills | NOT started. Paul names the next one. | |

## Running log
- 03/11/2026: `fact-find-summary` upload paused at an unexpected replace box (overwrite cannot be restored). Backup zip of the old 2 files sent to Paul. Do not click Upload and replace until Paul says so.
- 03/11/2026: `fact-find-summary` Phases B to E done in one pass (no helpers, one test, passed on source and on the unpacked zip). Zip `releases/fact-find-summary-20261103-0941.zip` and its brief sent; folder `fact-find-summary-skill`. Waiting for the upload report.
- 03/11/2026: `fact-find-summary` Phase A done (no helpers, no tests). Serious: the live skill says Dread Disease ABI 5% (Paul decided 3%), makes its own Teams message and Planner note (the Teams skill owns them), and its script holds a real person's details. Waiting for Paul's answers.
- 03/11/2026: Paul chose `fact-find-summary` as the next skill. Before Phase A: size and cost given, waiting for his go.
- 03/11/2026: procedure approved by Paul and saved. Lesson behind it: earlier work on `ff-population-transcript` ran six helper-driven review rounds and used far too many of Paul's tokens (see CHAT-NOTES.md). From now on: one test, no helpers.
