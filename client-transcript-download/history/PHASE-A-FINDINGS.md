# client-transcript-download: Phase A findings (Operation Skill Restructure, 03/11/2026)

Read-only analysis of the LIVE skill (Paul's synced copy, 14/10/2026 14:41 build). No client data is kept here. Nothing has been changed or built.

## Facts
- Live skill: `SKILL.md` 72 lines, 9,369 bytes, about 1,600 words, ONE file, no script. 108 single rules (sentences) are the baseline for the rule-by-rule check.
- Job: after a client meeting, fetch the Teams meeting transcript (today only through Claude in Chrome), save a COPY as `Teams meeting transcript - DD.MM.YY - (First Last).docx` into the client's `2. Fact Find` folder, check the file, and tell Paul. It deletes nothing; the original stays in Downloads.
- Feeds: `ff-population-transcript` (first meeting) and `client-teams-transcript-skill` (follow-ups) both read the saved file. Nothing feeds this skill except Teams and Paul's message.
- Client data scan: none (the only hit is Paul's own sign-in address in Step 2, not a client's).

## Flaws found
Contradicts the facts or other skills (serious):
1. **The central claim is outdated.** It says the Microsoft 365 connector and Zapier cannot fetch Teams transcripts, so "go straight to Chrome". The connector now holds `OnlineMeetingTranscript.Read.All`, `OnlineMeetingRecording.Read.All`, `OnlineMeetings.Read` and `Files.ReadWrite.All` (checked 03/11/2026 with get_granted_scopes), and `client-teams-transcript-skill/references/01-access-and-locate.md` already says the connector can read transcripts. Whether a connector tool can really fetch the transcript needs one real try on a real meeting (client data), so it is NOT proven.
2. It forbids trying the connector routes first. Standard S4 says: three routes in order (computer, Microsoft 365, Zapier), every try logged.
3. Rule 9 (changes go through the `propose_skills` card) conflicts with S7 (changes only in Claude Code, uploaded as a zip).
4. The Related section says only `client-teams-transcript-skill` follows. Since 02/11/2026 a first (Fact Find) meeting goes to `ff-population-transcript`, then `fact-find-summary`.
Nothing forces the rules (text only):
5. The delivery gate is "confirm in one line each" (self-report). The 8 steps can be skipped or done from memory.
6. The completeness check (Step 7) says "last timestamp near the end", with no number and no program.
7. "The folder was checked" is not a size comparison (S: the listed size must equal the local file).
8. The file name is built by hand each time.
Standards and clutter:
9. About half of the 72 lines are the generic "universal rules" copied into every skill (re-load, read before you write, source first). Rules 2 and 3 are about drafting from a source: they do not apply to a download.
10. The stamp is typed by hand (S2) and the changelog archive `client-transcript-download-changelog.md` is a project document outside the skill (could not be checked).
11. Chrome and the Downloads folder live on Paul's laptop: if the laptop is off the whole skill fails, with no second route.
12. The saved transcript is named without the meeting type (the other skills also see `... - FF` and `..._ Annual Review [year]`); they identify the file by content, so this works, but it is not written down.

## Duplications between skills
- Client File Access (the two folder roots, never another broker's folder, `[Surname], [First]\2. Fact Find`) is written in this skill, in `client-teams-transcript-skill`, in `ff-population-transcript` and in the old `fact-find-summary`.
- The transcript file name pattern is defined here and re-described in the other skills.
- The statement about the Microsoft 365 route contradicts `client-teams-transcript-skill` (see flaw 1).

## Score against the 13 ingredients
Full 0. Partial 4 (1 short entry page, 5 evidence, 10 one reply one question, 12 history outside). Missing 6 (2 inputs and three routes, 3 step driver, 6 built by program, 9 one checker, 11 tests, 13 package and upload). Not applicable 3 (4 reading lock, 7 short means short, 8 sorted actions).

## Yes/No list for Paul (recommended answers in brackets)
1. Fetch the transcript through the Microsoft 365 connector FIRST, with Claude in Chrome as the fallback, every try logged. The catch: I cannot prove the connector route works until one real try; the program builds both. (Yes)
2. Drop the generic universal rules and rule 9; keep the standing rules (Chrome or connector only for Teams, never delete, copy not move). (Yes)
3. Keep the file name `Teams meeting transcript - DD.MM.YY - (First Surname).docx` as it is (the other skills identify the file by content). (Yes)
4. A transcript counts as complete only when its header shows the meeting title, date and length and its last time stamp is within 2 minutes of that length; otherwise the program says what is missing. (Yes)
5. After saving, the reply tells Paul which skill comes next: a first (Fact Find) meeting goes to `ff-population-transcript`, a follow-up to `client-teams-transcript-skill`. (Yes)

## Status
Phase A report given to Paul 03/11/2026.

## Paul's answers (03/11/2026)
"Agree to all": yes to questions 1 to 5 as recommended (connector first with Chrome as fallback, every try logged; drop the generic rules and rule 9; keep the file name; complete = last time stamp within 2 minutes of the meeting length; the reply names the next skill).

Next: Phase B (plan) given to Paul 03/11/2026, waiting for his approval.
