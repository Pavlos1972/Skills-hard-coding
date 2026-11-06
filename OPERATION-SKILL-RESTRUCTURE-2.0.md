# Operation Skill Restructure 2.0 (Paul, 06/11/2026)

This replaces "Operation Skill Restructure" 1.0, which Paul had deleted. Read this before any skill work, follow it in order, and call it by this name. One skill at a time. No helpers. ONE test per skill. Ask Paul before starting the next skill. Update the Progress table after every phase.

## 1. The brief (Paul's own words, in plain form). That is ALL it is.
1. **Chats do not always read a skill fully or do it the same way every time.** Fix that with a program the chat cannot ignore: if a skill has TEN steps, all TEN are done, in order, every time. That is the brief.
2. **Look at the ORIGINAL skill, find the contradictions, remove them, remove the bloat, streamline it.** That is the brief.
3. **No permission requests.** The original skill had full access to the client's files in OneDrive on Paul's computer, and he has the Microsoft 365 connector on. Every chat is on Auto. Nothing may ask him for anything.

Anything beyond these three is over-building. New features only when Paul asks for them in his own words.

## 2. What went wrong in 1.0 (never repeat)
- I added a shell command on Paul's laptop for every file (a fingerprint check). It caused approval prompts, failed on cloud-only files, and the original never needed it.
- I made a failed computer connection a hard STOP. The original carried on.
- I turned every worry into a refusal (ledger rules, review of soft lines, quote length, "none" logs). The chat spent its time satisfying the program, not doing the job. 16 steps, 44 minutes, not finished.
- I swung between two extremes (Microsoft 365 only, then computer with proofs) instead of putting back what already worked.
- I rebuilt from scratch and wrote 6,000 lines of code and 370 tests where about 300 lines of text needed tidying and its steps forcing.
- I ran long test and review rounds, which wasted Paul's tokens.

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
1. **Access is the original's:** the device bridge first (get_device_info, request the folder once only if it is not connected, list, stage, commit), then the Microsoft 365 connector, then Zapier, then say plainly what is blocked. No shell commands on the laptop (`device_bash`), no fingerprints, no access log gates, no hard STOP, never "please attach the file". If a request is refused, the chat goes to the next route and carries on.
2. **A proof is cheap, local and about the chat's own work:** a file exists, a chunk was served, a total adds up, a saved size matches the listing. Never a proof that needs Paul's machine or a new permission.
3. **The program refuses only when a step was skipped, not when wording is imperfect.** Judgment stays as text. A refusal costs a whole chat round, so keep them few.
4. **Each rule once.** Four copies of one rule drift apart.
5. **Start from the original and change only what Paul asked** (steps forced, contradictions and bloat removed). Keep the short true stories inside the rules, names removed.
6. **Short:** entry page about 80 lines; no more steps than the job really has.
7. **A quiet run:** one version sentence, short progress lines, no opening recap, nothing asked of Paul. The reply at the end is the outputs and the SHORT audit. The Sitamah message of the Fact Find chain is posted automatically through Zapier. Any other message or email waits for Paul's yes.
8. **Flexible:** if a file is not where expected, the chat tries the next route and goes on. STOP only when the job truly cannot be done, with one short line.
9. **No client data in the repo.** Tests use invented people only.
10. **Never say "live" before Paul confirms.** A reported upload is "uploaded (reported)".

## 5. The procedure for each skill
**Phase 1: Read and report (change NOTHING).**
1. Name the skill and say what it does in two lines.
2. Read the ORIGINAL in full (the version before any 1.0 changes; Paul confirms which one), plus the inputs it works on (for a new input such as a new form, read a real example with Paul's say-so).
3. Report to Paul as ONE plain-English table: left column the problem, right column the solution. It must show what is good (keep), what is not good (remove), the contradictions, the bloat, how the skill reaches its files (no permission gates), and the proposed steps with what the program makes sure at each.
4. Explain it back to Paul and WAIT for his yes.

**Phase 2: Build, in one pass (no helpers).**
Archive the original in `history/`; split it into `references/`; write `steps.json`, `run.py`, `verify.py` and only the helpers that are needed; write the entry page; stamp (`tools/stamp_skill.py`); lint (`tools/lint_skill.py`); rule-by-rule check (`tools/inventory.py`: nothing lost without a record); ONE test on invented data, passed on the source and on the unpacked zip.

**Phase 3: Hand over.**
Package (`tools/package_skill.py`). Paul LOOKS at the real folder in Explorer and says its name (his screenshot decides, not memory). Make the brief (`tools/make_upload_brief.py <zip> --folder "<path>"`). Send the zip, the brief, the backup of the version uploaded now, and a short yes/no list. A chat with Claude in Chrome uploads it and reports. Record "uploaded (reported)". Test before and after as the brief says.

**Phase 4: First real run.**
Paul runs it on a real client. The chat reports how many approval prompts there were, how many minutes it took, and every refusal. Fix only the faults found. Paul says when it is live.

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
| `ff-population-transcript` (FIRST, the model) | v32 (28/10/2026) plus Paul's 02/11 text decisions | done, waiting for Paul's go | not started | not started | not started |
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
- The form's file is already most of the Fact Find (about 270 fields, an 11-page PDF in the v3.0 layout with Paul's eight planning areas, totals worked out in the PDF only). The skill starts from it and applies the transcript's corrections. It reads the PDF as well as the data file. It does not rebuild the whole Fact Find.
- Paul's 02/11 decisions stay: the form's file is the first source; Dread Disease ABI 3%; check the form's schema version every run; ignore the form's parking list; check the company look-up text and replace chatter from the transcript; the follow-up appointment is an action for Sitamah; the 8:45am laptop window is dropped.
- Planned steps (8): find and stage the files; read the form (both files); read the transcript twice; contact details and lead source (D&R Outlook search); corrections list (each cites its transcript line, totals reconcile, standing values checked); build the PDF and look at it; save and list back; the Summary, Planner note (made by `client-teams-transcript-skill`) and the Sitamah message.
- One stop only: Paul reads the Fact Find PDF; everything after it runs by itself. (Recommended by me; Paul has not objected.)

## 9. Running log (newest first)
- 06/11/2026: Operation Skill Restructure 2.0 written and 1.0 deleted at Paul's request (the old file stays in the repo's git history). Phase 1 report for `ff-population-transcript` done (original v32 read in full, the new form read through the real files of a real client, nothing kept in the repo); Paul explained back and said yes to the combined-report rule. Waiting for Paul's go to start Phase 2.
- 06/11/2026: Paul stopped the work: the 1.0 `ff-population-transcript` (v37) needed many approvals and about 44 minutes without finishing. He asked for a report, then for the original to be the base.
