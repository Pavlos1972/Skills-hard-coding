# Interim update of the two Fact Find skills (02/11/2026)

Text edits only, made to Paul's decision 14 (SKILL-STANDARDS.md section 7). The three scripts here are the exact record of
every change: each one lists the old text and the new text, and stops if the old text is not found exactly once.

- `patch_ff.py`: `ff-population-transcript` (new form's data file first, schema check, parking list ignored, look-up check, Dread Disease ABI 3%, Planner note and Sitamah message handed to the Teams transcript program).
- `patch_fs.py`: `fact-find-summary` (same source order, Dread Disease ABI 3%, message handed to the Teams transcript program).
- `patch_teams.py`: `client-teams-transcript-skill` (the follow-up appointment IS an action for Sitamah; already applied in this repo).

The two Fact Find skills are not in this repo (they are not converted yet). Their zips and upload briefs are kept outside the
repo because `ff-population-transcript/scripts/build_fact_find.js` still holds a real client's data (it goes in the rebuild).
The previous versions stay in the claude.ai Skills version history (the backup). NOT uploaded, NOT live.
