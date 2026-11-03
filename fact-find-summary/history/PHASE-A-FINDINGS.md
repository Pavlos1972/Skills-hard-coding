# fact-find-summary: Phase A findings (Operation Skill Restructure, 03/11/2026)

Read-only analysis of the LIVE skill (Paul's synced copy, 28/10/2026 10:58 build). No client data is kept here. Nothing has been changed or built.

## Facts
- Live skill: `SKILL.md` 222 lines, 47,897 bytes, about 7,800 words, plus ONE script `scripts/build_report.py` (178 lines). 2 files.
- Baseline: 394 single rules (sentences) in SKILL.md (the rule-by-rule check in Phase D will account for every one).
- Job: builds the Fact Find Summary PDF (fixed nine sections) from the completed Fact Find (Fact Find Transcript PDF), saves it in the client's `2. Fact Find` folder and sends it in the chat. The live text ALSO checks the other two outputs, makes its own Planner note and makes/sends its own Teams message to Sitamah.
- Receives from: `ff-population-transcript` (Fact Find Transcript PDF), the form's data file (Audio to Text), the Teams transcript, the latest Overview. Used as an input by `client-pipeline-board`, `rgar-skill`, `om-tax-free-skill` (so the nine-section structure and the filename pattern must not change).

## Flaws found
Contradicts Paul's decisions or other skills (serious):
1. Dread Disease ABI is written as 5% in three places; Paul decided 3% always (02/11/2026) and the new `ff-population-transcript` writes 3%. Today the Summary and the Fact Find disagree.
2. Written for the old form: statuses "confirmed, heard, verify, preset", no schema check, no parking-list rule, no look-up-chatter rule.
3. Makes its own Planner note (Output 3) and its own Teams message (Step 8, Delivery gate 6): `client-teams-transcript-skill` v35 owns both now. Its "already sent" check only knows `ff-population-transcript`.
4. Refers to the old `ff-population-transcript` structure (hand off first, sign-off, Step 8) that no longer exists.
5. The 8:45am laptop-window note: dropped by Paul (02/11/2026).
6. Rule 9 says changes go through the `propose_skills` card; standard S7 says changes are made in Claude Code and uploaded as a zip.
Nothing forces the rules (text only):
7. The ten universal rules, the Delivery gate, the accuracy rule and the totals rule are all text. The delivery gate is "confirm in one line each" (self-report).
8. The totals rule demands named variables, computed totals and `assert` checks and says "see the script", but the script has none (0 asserts, no sums, no totals). All values are typed in by hand.
9. Each run Claude "copies the script and replaces the data rows" = rewrites the program during the run.
10. The "re-search every keyword, re-verify the whole Fact Find" accuracy step is a large manual job with no proof, and it repeats what the new Fact Find program already proves.
Standards:
11. Client data inside the skill: the example script holds a real person's details (name, ID number, phone numbers, emails, job). S11 violation, live today. (Not repeated here.) The old version stays in the claude.ai version history after an upload.
12. The script's output filename does not match the required pattern `Fact Find Summary - DD.MM.YY - (First Last).pdf`.
13. Page size is US Letter; the new Fact Find Transcript PDF is A4.
14. The "Last updated" stamp is typed by hand (S2 wants a program); the changelog archive `claude/fact-find-summary-changelog.md` is a project document outside the skill (could not be checked).
15. Client File Access has local, SharePoint, ask: S4 needs three routes (computer or OneDrive, Microsoft 365, Zapier), each logged.
16. 222 lines on one page, with the rules repeated at the top "because long conversations get compressed" (template wants a short entry page).
17. No source per value (S9): the Summary's values are not tied to where they came from.
18. Repeated inside the skill: the ABIs are stated three times, "Not discussed is a claim" three times, the two-spouse rules in four places.

## Duplications between skills
- The Sitamah message (wording, label, 1st/2nd/3rd count, follow-up sentence, Zapier route, 403 note, once per meeting) and the Planner note: in BOTH this skill and `client-teams-transcript-skill`. Owner: `client-teams-transcript-skill`.
- Standing rules copied in both this skill and `ff-population-transcript` (source order, file access, accuracy, totals, ABIs, quote requests, two spouses): kept in two places and already drifted (Dread Disease 5% vs 3%).

## Score against the 13 ingredients
Full 0. Partial 4 (2 inputs, 5 evidence, 10 one reply one question, 12 history outside). Missing 7 (1 short entry page, 3 step driver, 4 reading lock, 6 built by program, 9 one checker, 11 tests, 13 package and upload). Not applicable 2 (7 short means short, 8 sorted actions: to confirm).

## Yes/No list for Paul (recommended answers in brackets)
1. The skill's job: build the Summary from the completed Fact Find Transcript PDF and prove the Summary matches it; drop the "re-verify everything against the recording again" step because the Fact Find skill's checker does it. (Yes)
2. Remove the Planner note and the Sitamah message from this skill; `client-teams-transcript-skill` owns them. (Yes)
3. A4 page size, like the Fact Find Transcript PDF. (Yes)
4. Drop the 8:45am note and the `propose_skills` rule. (Yes)
5. Replace the example script's real person with an invented person and build from data by program. (Yes)
6. Routing names (Cameron: short-term, CL: Will, Valerie: medical aid, Martin: gross income): still correct? (Paul to say)
7. Drop reading the old v2.0 Fact Find layout and the "PDF that is really a zip of JPEG images" case. (Yes, the new form is the only source.)
Decided already (apply, no question): Dread Disease ABI 3%; the new form's rules; the nine-section structure, colours and filename pattern stay.

## Status
Phase A report given to Paul 03/11/2026.

## Paul's answers (03/11/2026)
- 1 to 5 and 7: YES, as recommended (job = build the Summary from the finished Fact Find Transcript PDF and prove it matches, no full re-verification against the recording; Planner note and Sitamah message removed from this skill; A4; drop the 8:45am note and `propose_skills`; invented example person and build by program; drop v2.0 layout and the zip-of-images case).
- 6 (routing names): "they are correct. Valerie and Cameron are correct BUT Brightrock is Lizelle". CLARIFIED by Paul (03/11/2026, chosen option "Lizelle replaces Martin"): the new routing list is Cameron = short-term insurance, CL = Will, Valerie = medical aid, **Lizelle = confirms gross income / ACI items (BrightRock), replacing Martin**. Martin is removed.

Next: Phase B (plan): given to Paul 03/11/2026, waiting for his approval.
