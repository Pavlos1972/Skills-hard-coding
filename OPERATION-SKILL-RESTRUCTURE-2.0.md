# Operation Skill Restructure 2.0 (Paul, 06/11/2026)

This replaces "Operation Skill Restructure" 1.0, which Paul had deleted. Read this before any skill work, follow it in order, and call it by this name. One skill at a time. No helpers. ONE test per skill. Ask Paul before starting the next skill. Update the Progress table after every phase.

## 1. The brief (Paul's own words, in plain form). That is ALL it is.
1. **Chats do not always read a skill fully or do it the same way every time.** Fix that with a program the chat cannot ignore: if a skill has TEN steps, all TEN are done, in order, every time. That is the brief.
2. **Look at the ORIGINAL skill, find the contradictions, remove them, remove the bloat, streamline it.** That is the brief.
3. **No permission requests.** The original skill had full access to the client's files in OneDrive on Paul's computer, and he has the Microsoft 365 connector on. Every chat is on Auto. Nothing may ask him for anything. **Paul, 06/11/2026: the skill itself carries his permission for the two folders below, and this is built into every skill from now on.**

Anything beyond these three is over-building. New features only when Paul asks for them in his own words.

## 2. What went wrong in 1.0 (never repeat)
- I added a shell command on Paul's laptop for every file (a fingerprint check). It caused approval prompts, failed on cloud-only files, and the original never needed it.
- I made a failed computer connection a hard STOP. The original carried on.
- I turned every worry into a refusal (ledger rules, review of soft lines, quote length, "none" logs). The chat spent its time satisfying the program, not doing the job. 16 steps, 44 minutes, not finished.
- I swung between two extremes (Microsoft 365 only, then computer with proofs) instead of putting back what already worked.
- I rebuilt from scratch and wrote 6,000 lines of code and 370 tests where about 300 lines of text needed tidying and its steps forcing.
- I ran long test and review rounds, which wasted Paul's tokens.
- **First real run of the 2.0 build (v38, 06/11/2026): I built on an access route I had never tested in Paul's own chat.** The chat asked for the whole `~/liferisk.co.za`; the Auto-mode safety check refused it with no box shown to Paul; everything fell back to Microsoft 365 text, the chat retyped the form's JSON (not a faithful copy: 31,539 bytes on disk), re-cut the flat transcript by hand and skipped the PDF. I also told the chat to "not ask Paul for permission", which is the opposite of what that check wants to see.
- **A program run as many separate shell commands asks for a click on each one** (6 "Allow once" boxes in steps 1 and 2 alone, part of them the chat's own improvised `cp`, `sed` and heredoc). Fewer, fixed commands are the only lever.
- I gave a padded time estimate without saying what it was made of.

## 3. The skeleton every skill becomes
- `SKILL.md`: a SHORT entry page (about 80 lines at most): name, description, Index, the program-stamped "Last updated" line, Recent changes, "Run it", the few standing rules, where the detail lives.
- `steps.json`: the ordered steps (the original's real steps, normally 5 to 10). Each has an id, a title, what to do, the page to show, and a cheap proof.
- `scripts/run.py`: the step runner (standard library only): `start`, `next`, `done <step>`, `status`. It shows ONE step at a time, refuses to show step N+1 until step N's proof is on file, and remembers where the job is up to (so a long chat or a compression cannot lose its place). It is run as it is and never edited during a run.
- `scripts/verify.py`: prints the SHORT audit (one line per check with ✅ or ❌, one closing "Only attested" line, RESULT). The full record goes to a file in the run folder.
- Small helpers ONLY for work a program does better than a chat (reading a PDF, adding up totals, drawing a fixed layout, serving a transcript in chunks).
- `references/`: the original text split by topic, EVERY RULE WRITTEN ONCE, shown by the program at its step.
- `history/`: the archived original (names removed), the list of what was removed and why, Paul's yes/no list, the stamp record.
- ONE test, on invented data.

## 4. The design rules
1. **Access is the original's, with Paul's permission written into the skill (Paul, 06/11/2026; every skill that touches client files carries this paragraph).** Folder 1 = `~/liferisk.co.za/Company - Paul`; Folder 2 = `~/liferisk.co.za/Company - WR Clients/Paul Kafentzis (Client Files)` (his Explorer shows them as OneDrive > liferisk.co.za > ...). The chat calls `get_device_info`; if the two folders are not connected it calls `device_request_folder_access` ONCE with exactly those two paths and a plain reason; NEVER the whole `~/liferisk.co.za` (refused on the first real run; the two named folders were granted in the test) and never another broker's folder. Then list, stage (exact copies) and commit. If refused: no retry; the Microsoft 365 connector (PDF and Word files in page ranges), then Zapier, then say plainly what is blocked. No shell commands on the laptop (`device_bash`), no fingerprints, no access log gates, no hard STOP, never "please attach the file", never retype a file (a file typed out from text is told to the program and shown in the audit). If the safety check refuses again, Paul's start message carries his own words: "You may connect to these two folders on my computer: Company - Paul, and Company - WR Clients / Paul Kafentzis (Client Files), both under liferisk.co.za."
2. **A proof is cheap, local and about the chat's own work:** a file exists, a chunk was served, a total adds up, a saved size matches the listing. Never a proof that needs Paul's machine or a new permission.
3. **The program refuses only when a step was skipped, not when wording is imperfect.** Judgment stays as text. A refusal costs a whole chat round, so keep them few.
4. **Each rule once.** Four copies of one rule drift apart.
5. **Start from the original and change only what Paul asked** (steps forced, contradictions and bloat removed). Keep the short true stories inside the rules, names removed.
6. **Short:** entry page about 80 lines; no more steps than the job really has.
7. **A quiet run:** one version sentence, short progress lines, no opening recap, nothing asked of Paul. The reply at the end is the outputs and the SHORT audit. The Sitamah message of the Fact Find chain is posted automatically through Zapier. Any other message or email waits for Paul's yes.
8. **Flexible:** if a file is not where expected, the chat tries the next route and goes on. STOP only when the job truly cannot be done, with one short line.
9. **No client data in the repo.** Tests use invented people only.
10. **Never say "live" before Paul confirms.** A reported upload is "uploaded (reported)".
11. **Commands:** the chat runs only the commands the program prints (`python3 .../run.py <step>`): no `cp`, `sed`, heredocs, no opening the program's own files. Keep the number of commands per run small. Permission boxes are counted on every real run and any box on a read is a failure to fix.

## 5. The procedure for each skill
**Phase 1: Read and report (change NOTHING).**
1. Name the skill and say what it does in two lines.
2. Read the ORIGINAL in full (the version before any 1.0 changes; Paul confirms which one), plus the inputs it works on (for a new input such as a new form, read a real example with Paul's say-so).
3. **Access test in Paul's own chat, in his usual Auto mode, on a harmless file (no client file opened): the exact tools, paths and results are written in the report. Never design on an access route that has not been tested there.**
3a. Report to Paul as ONE plain-English table: left column the problem, right column the solution. It must show what is good (keep), what is not good (remove), the contradictions, the bloat, how the skill reaches its files (no permission gates), and the proposed steps with what the program makes sure at each.
4. Explain it back to Paul and WAIT for his yes.

**Phase 2: Build, in one pass (no helpers).**
Archive the original in `history/`; split it into `references/`; write `steps.json`, `run.py`, `verify.py` and only the helpers that are needed; write the entry page; stamp (`tools/stamp_skill.py`); lint (`tools/lint_skill.py`); rule-by-rule check (`tools/inventory.py`: nothing lost without a record); ONE test on invented data, passed on the source and on the unpacked zip.

**Phase 3: Hand over.**
Package (`tools/package_skill.py`). Paul LOOKS at the real folder in Explorer and says its name (his screenshot decides, not memory). Make the brief (`tools/make_upload_brief.py <zip> --folder "<path>"`). Send the zip, the brief, the backup of the version uploaded now, and a short yes/no list. A chat with Claude in Chrome uploads it and reports. Record "uploaded (reported)". Test before and after as the brief says.

**Phase 4: First real run.**
Paul runs it on a real client. The chat reports every permission box (which tool, which step, and Paul's screenshots decide the count, because the chat cannot see his clicks), how many minutes it took, and every refusal. Fix only the faults found. A box on a read is a failure. Paul says when it is live.

## 6. Always
- Simple words. One recommended route with its honest catch. Short answers. One question at a time.
- Reports to Paul are a two-column table (problem | solution), plain English. Audits in the chat are SHORT (✅ or ❌ one-liners plus one "Only attested" line).
- Say what was checked and what was only attested. Never claim done without the checker's PASS.
- Explain back what Paul asked before building anything big, and wait for his yes.
- Side issues are written down and told to Paul, not chased.
- Update the memory files and the Progress table after every phase.
- Before deleting or moving anything in Paul's OneDrive: list the folder first, and delete only what he asked for (it goes to the Recycle Bin).

## 7. Progress (update after every phase)
| Skill | Base (the original) | 1 Report | 2 Build | 3 Hand over | 4 Real run |
|---|---|---|---|---|---|
| `ff-population-transcript` (FIRST, the model) | v32 (28/10/2026) plus Paul's 02/11 text decisions | done | done 06/11/2026; v39 (13:29, 20 files) fixes the first real run | v38 uploaded (reported); **v39 packaged, brief made, NOT uploaded yet**; NOT confirmed live | first real run of v38 (Roquelle Damir, 06/11/2026) STOPPED by Paul at step 2: computer request refused (whole root asked), JSON retyped, transcript flat, PDF unused, 6+ "Allow once" boxes. v39 fixes these; next: Paul's second real run |
| `fact-find-summary` | to be confirmed in its Phase 1 | not started | | | |
| `client-teams-transcript-skill` | to be confirmed (v35 was confirmed live 03/11/2026) | not started | | | |
| `client-transcript-download` | to be confirmed | not started | | | |
| `teams-meeting-setup-skill`, `outlook-emails-skill`, `astute-summary-report-skill` | to be confirmed | not started | | | |
| `wr-roa-builder`, `wr-sroa-builder`, `om-tax-free-skill`, `rgar-skill`, `om-optimal-ra-proposal` | to be confirmed | not started | | | |
| `investment-comparisons-skill`, `life-insurer-comparison`, `life-policy-schedule-analyzer` | to be confirmed | not started | | | |
| `client-pipeline-board`, `complete-applications-skill`, `client-review-notes`, `prospect-review-funnel-at-knowledge` | to be confirmed | not started | | | |

The 1.0 rebuilds of all of these are uploaded but are SUPERSEDED. The oldest archived text of each is in its own `history/` folder. Paul names the next skill after each one; the order above is only a suggestion.
Not in scope unless Paul says: `paul-email-signature`, `advicetech-website-knowledge`, `correcting-skills`, `master-skill-template`, `upload-skill-method`, `alpha-bank-statements`, `nedbank-current-account-categorization`, `qb-monthly-budget`, `managing-generali-checkups`, `cameron-short-term-skill` (set aside). FORGOTTEN by Paul's word, never convert: `planner-interim-procedure`, `ff-to-ff-populate`.

## 8. The first skill: `ff-population-transcript` (Paul's requirements, 06/11/2026)
- It reads BOTH the "Fact Find (Audio to Text)" files (the form's data file and its PDF) AND the "Teams meeting transcript", analyses both, and makes ONE report: the "Fact Find Transcript - DD.MM.YY - (Name Surname)" PDF, saved into the client's `2. Fact Find` folder. The Summary, the Planner note and the Sitamah message come after it, from that one report.
- Contradictions between the two are either SORTED (a clear rule settles it and says so in one line) or HIGHLIGHTED (both values quoted with where each came from). When no rule settles it, the form's value goes in the report and the difference is highlighted. Nothing is picked or dropped silently.
- Paul's decision 06/11/2026: he first said not to read the JSON; after the explanation that the retyping (not the JSON) was the problem he said to go ahead and read it. BOTH files of the Audio to Text are read, as exact copies from his computer.
- The form's file is already most of the Fact Find (about 270 fields, an 11-page PDF in the v3.0 layout with Paul's eight planning areas, totals worked out in the PDF only). The skill starts from it and applies the transcript's corrections. It reads the PDF as well as the data file. It does not rebuild the whole Fact Find.
- Paul's 02/11 decisions stay: the form's file is the first source; Dread Disease ABI 3%; check the form's schema version every run; ignore the form's parking list; check the company look-up text and replace chatter from the transcript; the follow-up appointment is an action for Sitamah; the 8:45am laptop window is dropped.
- Planned steps (8): find and stage the files; read the form (both files); read the transcript twice; contact details and lead source (D&R Outlook search); corrections list (each cites its transcript line, totals reconcile, standing values checked); build the PDF and look at it; save and list back; the Summary, Planner note (made by `client-teams-transcript-skill`) and the Sitamah message.
- One stop only: Paul reads the Fact Find PDF; everything after it runs by itself. (Recommended by me; Paul has not objected.)

## 9. Running log (newest first)
- 06/11/2026: `ff-population-transcript` v39 built (13:29) after Paul's first real run of v38 (Roquelle Damir): access test in his own chat PASSED with the two named folders and his words (`device_request_folder_access` granted both; the Damir `2. Fact Find` folder listed, five files, none opened); decision A (read the JSON and the PDF as exact copies). Changes: the skill carries Paul's permission and the two exact paths; a `.docx` is read by the program itself (no pandoc); `--copied` shows any file the chat typed out; fixed commands only. One test passed (source and unpacked zip), lint PASS, rule-by-rule 568 sentences: 247 kept, 94 reworded, 227 dropped, 0 unaccounted. Packaged `releases/ff-population-transcript-20261106-1329.zip` (20 files, 93,007 bytes), NOT uploaded. Not proven: the number of permission boxes, the real PDF through the program's reader.
- 06/11/2026: first real run of `ff-population-transcript` v38 (Roquelle Damir) stopped by Paul at step 2 of 8: no PDF, no audit, nothing saved, nothing sent. Faults: see section 2.
- 06/11/2026: `ff-population-transcript` UPLOADED as v38 on 06/11/2026 by a Chrome chat that had the brief (reported by that chat, pasted by Paul): before = v37, 24 files, 31 skills, ON, test answer "Last updated: 2026-11-05 17:11 (Athens time)" and "Index"; replace box "Current 78 lines - This file 75 lines" (it named exactly ff-population-transcript); after = v38, 20 files, still ONE entry, ON, "Last updated: 2026-11-06 11:25 (Athens time)" and "Index" (correct). The zip was staged from the computer, no refusal, Paul did not pick the file; access check 7b ran by itself, no permission box (count incomplete: 16 of 21 subfolders, the connector has no folder listing). The live copy equals the zip (all 20 files compared). NOT confirmed live by Paul. client-teams-transcript-skill-20261106-0920.zip stays NOT uploaded. Next: Phase 4, Paul's first real run.
- 06/11/2026: `ff-population-transcript` Phase 3: folder `ff-population-transcript-skill` named by Paul and confirmed by the Microsoft 365 folder search (it held CHANGES-FOR-PAUL.md, the v36 zip, the v37 zip and the v36 backup); the live copy equals the v37 zip (24 files); brief made; zip, brief and CHANGES-FOR-PAUL sent. Waiting for the upload report.
- 06/11/2026: `ff-population-transcript` Phase 2 DONE (06/11/2026 11:25): rebuilt from the ORIGINAL v32 plus Paul's 02/11 decisions, in one pass, no helpers: 8 programmed steps (find files the original way, read the form's two files, read the transcript twice, contact and lead source, combine into ONE report with contradictions SORTED or HIGHLIGHTED, build and look, save and list back with Paul's one OK, hand over to the Summary / Planner / Sitamah skills), a short audit, no shell commands on his laptop, no fingerprints, no hard STOP. Kept and trimmed from 1.0: the form reader, the combiner (compose.py), the PDF drawing and layout.json; new: run.py, verify.py, tx.py, 8 reference pages (SKILL.md 81 lines). ONE test (6 seconds) passed on the source and on the unpacked zip, lint PASS, rule-by-rule 568 sentences: 254 kept, 87 reworded, 227 dropped with a reason, 0 unaccounted. Packaged `releases/ff-population-transcript-20261106-1125.zip` (20 files, 91,967 bytes), NOT uploaded (v37, the heavy 1.0 build, is still the uploaded one). Next: Phase 3 (Paul LOOKS at the folder name; brief; zip, changes list and backup).
- 06/11/2026: Operation Skill Restructure 2.0 written and 1.0 deleted at Paul's request (the old file stays in the repo's git history). Phase 1 report for `ff-population-transcript` done (original v32 read in full, the new form read through the real files of a real client, nothing kept in the repo); Paul explained back and said yes to the combined-report rule. Waiting for Paul's go to start Phase 2.
- 06/11/2026: Paul stopped the work: the 1.0 `ff-population-transcript` (v37) needed many approvals and about 44 minutes without finishing. He asked for a report, then for the original to be the base.
