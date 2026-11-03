# Chat notes for Claude Code (written for Paul, 03/11/2026, so nothing is forgotten)

Read this together with CLAUDE.md, SKILL-STANDARDS.md and SKILL-TEMPLATE.md. If this file and SKILL-STANDARDS.md disagree, SKILL-STANDARDS.md wins.

## 0. The procedure: Operation Skill Restructure (Paul, 03/11/2026)
The fixed list of what is done for every skill is in `OPERATION-SKILL-RESTRUCTURE.md` (approved by Paul: "Yes, save it"). Follow it strictly; keep its Progress table current. Next skill: Paul names it; `fact-find-summary` is the candidate (decision 20) but nothing is started on it under the Operation yet.

## 1. The goal (Paul's words, in plain form)
Every one of Paul's claude.ai skills must be restructured so that **a program governs it**: the skill runs every step, every time, nothing skipped or swapped, and a checker proves the result. Measured against the 13-ingredient template (approved 02/11/2026). One skill at a time. Paul uploads the finished zip into his Skills; Claude Code cannot save into his Skills.

## 2. How Paul wants me to work (these are rules, not wishes)
- **NO HELPERS (subagents).** Paul, 03/11/2026: "We cannot do what you did for every skill, you have eaten all my tokens. No more helpers." Never start a helper, an independent reviewer or a build agent unless Paul asks for one in his own words. Work in one pass, in this chat.
- **No endless test rounds.** Paul, 03/11/2026: "we've done enough tests." One build, one lint, one full test run, one package. Do not start review-and-fix loops. Never say "last round" and then run another.
- **Tokens are a budget.** Before any big or long job, say roughly how big it is and wait for Paul's yes. Prefer the packager (it runs the tests itself) over running the suite by hand as well.
- Simple everyday words. One recommended route and its honest catch. Short answers. Ask one thing at a time.
- Explain back what I understood before building anything big, then wait for his yes.
- Say what was checked and what was only attested. Never say "live" until Paul confirms he uploaded it. Nothing is sent without his yes.
- No client names, ID numbers or real client documents in the repo (invented people only: Pat Samplecase, Robin Testcase).

## 3. The pipeline Paul confirmed (02/11/2026, his own words)
1. The Fact Find form saves `Fact Find (Audio to Text) - DD.MM.YYYY - Name Surname` (PDF and JSON data file) into the client's folder.
2. **`ff-population-transcript`** takes that as its FIRST source, adds the Teams transcript, the latest Overview and the client's other documents, and COMBINES them into the completed Fact Find: the **Fact Find Transcript PDF**, a saved report in its own right.
3. **`fact-find-summary`** takes that report and makes the Summary PDF.
4. The Planner note (private page) and the Teams message to Sitamah are made once, by **`client-teams-transcript-skill`** (`--type first`). Nothing is sent without Paul's yes; Zapier only.

## 4. Where each skill stands (03/11/2026)
| Skill | State |
|---|---|
| `client-teams-transcript-skill` | LIVE v34 (Paul confirmed 30/10/2026). The 02/11/2026 15:55 build (follow-up appointment IS an action for Sitamah) was uploaded as v35 by a Chrome chat and is **LIVE: Paul confirmed 03/11/2026 ("Yes, v35 is live")**. The new Fact Find skill needs v35 (it is there). |
| `ff-population-transcript` | **Program-driven build finished (round 5, commit d434670, stamp 2026-11-03 06:12).** Lint PASS, inventory 0 unaccounted (568 old sentences: 391 kept, 68 reworded, 109 dropped on record), 356 tests (builder's count; the packager reruns them). NOT uploaded, NOT live. **Packaged 03/11/2026 on Paul's instruction WITHOUT the packager's two test runs (`--skip-tests`)**: lint PASS, zip `releases/ff-population-transcript-20261103-0612.zip` (165,944 bytes, 24 files) and its upload brief. Proof on the zip itself: unpacked it elsewhere and the end-to-end journey test (invented data, with the real Teams program) passed against its scripts. The full suite was NOT rerun on the zip or on this final code by me (the builder reported 356 passing). |
| `fact-find-summary` | Operation Skill Restructure applied 03/11/2026 (Phases A to E): the program-driven `fact-find-summary` is BUILT, PACKAGED and UPLOADED as v8 (reported by a Chrome chat, 03/11/2026), NOT confirmed live. A program reads the Fact Find Transcript PDF (`scripts/ffread.py`, needs `pdfplumber`), composes the nine sections with totals and follow-up owners (Cameron, CL, Valerie, Lizelle; Lizelle replaces Martin), draws an A4 PDF and a checker prints a SHORT audit of green ticks and red crosses. The Planner note and the Sitamah message left this skill (the Teams skill owns them). Rule-by-rule check: 392 old rules, 13 kept, 93 reworded, 286 dropped on record, 0 unaccounted. Lint PASS. ONE end-to-end test on invented data passed on the source and on the unpacked zip. Zip: `releases/fact-find-summary-20261103-0941.zip` (15 files, 38,533 bytes). The older interim text-update zip and brief are SUPERSEDED: do not upload them. UPLOADED as v18 on 03/11/2026 by a Chrome chat (reported by that chat, pasted by Paul): before = v17, 2 files, "Last Updated: 28 October 2026, 10:58"; the first replace box was a different one ("This overwrites fact-find-summary with this file. What it overwrites can't be restored afterwards."), so the chat stopped; Paul saved a backup zip of the old 2 files and approved; the second box read "This saves a new version of fact-find-summary. Earlier versions stay available in the skill's version history. Current: 218 lines - This file: 67 lines."; after = v18, 15 files, still ONE entry (31 skills), "Last updated: 2026-11-03 09:41 (Athens time)" and first section "Index" (the test chat answered correctly). NOT confirmed live by Paul (he runs it on a real client first). Yes/no list for Paul: `fact-find-summary/history/CHANGES-FOR-PAUL.md`. Never say live before Paul confirms. |
| `teams-meeting-setup-skill` | Operation Skill Restructure applied 03/11/2026 (Phases A to E, no helpers, ONE test passed on the source and on the unpacked zip): `teams-meeting-setup-skill` is BUILT and PACKAGED, not uploaded, not live. A program drives 7 steps (find client, facts, build, show, send, log, final): it reads the client's name and personal email from the Fact Find Transcript PDF (routes computer, Microsoft 365, Zapier, every try logged), builds the whole invite (subject in the fixed order, Africa/Johannesburg on start and end, exactly 1 hour, the client only, Teams on, date-aware opening line, no link or signature), shows it with the message to Sitamah and ONE question, and will not take Paul's yes unless he was shown exactly this invite; the checker compares what the Microsoft 365 tool returned with what he approved and prints a SHORT audit (ticks and crosses). A reschedule updates the existing event in place. Rule-by-rule check: 154 old sentences, 6 kept, 99 reworded, 49 dropped on record, 0 unaccounted. Zip `releases/teams-meeting-setup-skill-20261103-1209.zip` (13 files). 5 yes/no questions in `teams-meeting-setup-skill/history/CHANGES-FOR-PAUL.md`. |
| `planner-interim-procedure`, `ff-to-ff-populate` | FORGET (Paul). Never convert them. |

## 5. What was done in this chat and why it went wrong
- Done (good): studied the new form's data file, updated both Fact Find skills as text, changed the Teams skill (follow-up appointment is an action), approved the 13-ingredient template, then built the program-driven `ff-population-transcript` (step driver, checker, PDF drawn by program, tests on invented data, history, inventory, upload method).
- **Mistake (mine):** after the build I started an independent reviewer and ran SIX fix-and-review rounds with helpers, calling several of them "the last". Early rounds found real holes. Later rounds found only holes where a chat has to cheat on purpose. It cost Paul a very large number of tokens and a night. Do not repeat this for any skill.
- Round 6 (show the written values on the glance list, refuse a bare "No" on a request line) was half done when Paul stopped it. It is **set aside, not proven**; it is kept in git history (commit d3cbb19). If a real client run shows it is needed, add it then, by hand, without helpers.

## 6. Known limits of `ff-population-transcript` (all listed for Paul in `ff-population-transcript/history/CHANGES-FOR-PAUL.md`)
- The chat can still type Paul's own words itself (`run.py answer`): only attested.
- The chat chooses the kind of each ledger entry and the value of a fill; the glance list shows which field covers a request line but not the value written (round 6 would have added that). A request recorded as "No" is visible only on the PDF.
- A doctored Teams skill copy, a self-patched fingerprint and chat-made text copies of documents pass; the fingerprints are printed for Paul to compare.
- Requests worded with none of the listed words are not required by the program.
- Not run in a real chat. No real form, real transcript or Aptos was seen (the PDF uses Carlito where Aptos is missing and says so). **The real test is the first run on a real client.**
- Paul's open yes/no questions (items 1 to 17 in CHANGES-FOR-PAUL.md): labels written by me, Aptos substitute, header sizes, "Not discussed" tick-box rows, request words, dismissal limits, credit life as a hard word, keep/remove a business contact's address in references/04.

## 7. What happens next (in this order, one thing at a time)
1. DONE: the zip is packaged (see section 4) and its brief made with `tools/make_upload_brief.py <zip> --folder ...`. Paul's real folder is `...\Claude Skills - New\ff-population-transcript-skill` (with `-skill`); my brief named it without `-skill` and the Chrome chat used the real one. Check the folder name first next time.
2. DONE 03/11/2026: UPLOADED as v33 by a Chrome chat on 03/11/2026 (reported by that chat, pasted by Paul): before = v32, 3 files, "Last updated: 2026-10-28 10:45"; replace box "Current: 296 lines - This file: 76 lines"; after = v33, 24 files, still ONE entry, "Last updated: 2026-11-03 06:12 (Athens time)" and "Index" (the test chat gave the correct answer). 31 skills in the account. NOT confirmed live by Paul yet (he runs it on a real client first).
3. DONE: Paul confirmed v35 of the Teams skill is live (03/11/2026). NEXT: Paul runs the new Fact Find skill on a real client and tells me how it went, then confirms it is live. Never say "live" before that. If the real run shows a gap, fix it by hand, in one pass, no helpers (round 6 is in commit d3cbb19).
4. DONE 03/11/2026: `fact-find-summary` (program-driven, built under Operation Skill Restructure) uploaded as v18 (reported); not confirmed live. The older interim text-update zip is superseded.
5. DONE 03/11/2026: `teams-meeting-setup-skill` uploaded as v8 (reported by a Chrome chat; v7 before; 13 files; test chat correct); not confirmed live. NOW: ask Paul whether he is ready for the next skill; his 5 yes/no questions for this skill are still open. After the Chrome report, ask if he is ready for the next skill. (`fact-find-summary` is uploaded as v18; next skill only when Paul says go.) Plan it small, ask him first how much work it is, no helpers.

## 8. Commands
- Lint: `WR_NAME_BLOCKLIST=/tmp/wr-blocklist.txt python3 tools/lint_skill.py ff-population-transcript` (the names file lives OUTSIDE the repo; recreate it if the container was reset).
- Tests: `cd ff-population-transcript && python3 -W error::ResourceWarning -m unittest discover -s tests` (about 10 to 12 minutes: background only).
- Package: `WR_NAME_BLOCKLIST=... python3 tools/package_skill.py ff-population-transcript --out releases` (background, about 30 minutes).
- After editing a skill: `python3 tools/stamp_skill.py <skill> --change "..."` first. Never type the date. Athens time: `TZ=Europe/Athens date '+%Y-%m-%d %H:%M'`.
- Commit and push when the stop hook asks (branch `claude/skill-delivery-gate`).
