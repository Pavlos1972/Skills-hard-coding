# Interim update of the two Fact Find skills (02/11/2026)

Text edits only, made to Paul's decision 14 (SKILL-STANDARDS.md section 7). The three scripts here are the exact record of
every change: each one lists the old text and the new text, and stops if the old text is not found exactly once.

- `patch_ff.py`: `ff-population-transcript` (new form's data file first, schema check, parking list ignored, look-up check, Dread Disease ABI 3%, Planner note and Sitamah message handed to the Teams transcript program).
- `patch_fs.py`: `fact-find-summary` (same source order, Dread Disease ABI 3%, message handed to the Teams transcript program).
- `patch_teams.py`: `client-teams-transcript-skill` (the follow-up appointment IS an action for Sitamah; already applied in this repo).

The two Fact Find skills are not in this repo (they are not converted yet). Their zips and upload briefs are kept outside the
repo because `ff-population-transcript/scripts/build_fact_find.js` still holds a real client's data (it goes in the rebuild).
The previous versions stay in the claude.ai Skills version history (the backup). NOT uploaded, NOT live.

## Rule-by-rule check (02/11/2026, run after Paul asked whether the two skills had been verified)
`old/` holds the two original SKILL.md files (before the interim edits). `rule-check/` holds, for each skill, the change records, the decision records and the report of
`python3 tools/inventory.py old/<skill>.SKILL.md <the interim skill folder> --changes ... --decisions ...`.

| Skill | Old sentences | Kept | Reworded (recorded) | Dropped (recorded: moved to the Teams skill) | Unaccounted |
|---|---|---|---|---|---|
| ff-population-transcript | 568 | 464 | 27 | 76 | 1 (a false alarm: "The Audio to Text file." is the bold lead-in of Step 1d point 6, still in the text) |
| fact-find-summary | 392 | 323 | 16 | 53 | 0 |

Two small rules in the old Step 8 are NOT carried by the Teams skill (found by reading the dropped text against it): the literal chat id of the Sitamah 1:1 chat (the Teams program finds the chat by its label, so the id is not needed), and the note "do not use the Microsoft 365 connector's `search_people` (no People.Read permission)". Both are minor; add the second to `references/07-teams-message.md` in the next change to the Teams skill.
Not done for these two skills: lint (it FAILS on the pre-existing real client number inside `scripts/build_fact_find.js` and on size), tests (none exist: they are text-only skills), the 13-ingredient score, and a real run.
