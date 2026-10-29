# client-teams-transcript-skill (hard-coded version)

The rebuilt skill. The live skill in Paul's account is unchanged until Paul uploads the zip from `releases/` and confirms.
The rules for every skill are in `../SKILL-STANDARDS.md`. Plain-language summary of what changed: `history/CHANGES-FOR-PAUL.md`.

## What is in this folder

| Path | What it is | In the upload zip? |
|---|---|---|
| `SKILL.md` | Short entry page: how to start, what a finished run contains, the standing rules | yes |
| `steps.json` | The ordered steps the program shows one at a time | yes |
| `deliverables.json` | Every output, who makes it, how it is handed over and checked | yes |
| `references/` | The rule pages the program prints at the step where they apply, plus model examples (invented data) | yes |
| `scripts/` | `run.py` (the step driver), `tx.py` (reading lock), `build.py` + `page.py` (outputs), `verify.py` (PASS/FAIL), `wrlib.py` | yes |
| `tests/` | 157 tests on invented data, including a full run from start to PASS, the Copy button in a real browser, and one test for each weakness an independent review found | no |
| `history/` | The old skill (client names replaced), every change with its reason, every drop with its decision, the coverage report | no |

## One run

`run.py start RUN --type followup|first|whatsapp`, then `run.py next` / `run.py done RUN <step>` until the last step prints the PASS/FAIL checklist.
Steps: locate (access log) > prep (completeness check) > context (client file read and logged) > pass1 (read + ledger) > pass2 > scan >
content (content.json, every item sourced, every conditional rule answered) > build (Planner page, PDF, Teams message) > look (page images) >
planner (publish the page) > pdf (send, save, list back) > handoffs > teams (only with Paul's yes, Zapier only) > final (verify.py).

## What the program proves, and what it cannot

Proven by program: both reads served in order; every quote found in the transcript or a named document; every request, decision, change and hold covered;
closing-minute keyword hits resolved; actions all for Sitamah; the mandatory questions answered (credit life, cession, owner change, applications,
correspondence); the eight-area headings; outputs built from `content.json` and not edited by hand; the Teams message in its fixed wording.
Only attested (Claude records the real tool output; the checklist labels these ATTEST): publishing the page, sending and saving the PDF, the Zapier send, the look at the page images.
Cannot be proven by anyone: that the transcript was understood. Paul stays the final reviewer.

## Tools (in `../tools/`)

`stamp_skill.py` sets the Athens-time "Last updated" stamp (never typed by hand), `lint_skill.py` checks the skill against the standards,
`inventory.py` checks that no sentence of the old skill was lost without a record, `package_skill.py` builds the zip only if lint and every test pass,
then runs the tests again against the unpacked zip.

## Changing this skill

Only in Claude Code (standard S7): edit, run `stamp_skill.py --change "..."`, run the tests, run `package_skill.py`, give Paul the zip.
Set `WR_NAME_BLOCKLIST` to a file of client names kept OUTSIDE the repo so lint can scan for them.
