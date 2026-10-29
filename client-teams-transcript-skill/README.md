# client-teams-transcript-skill: hard-coded delivery gate (draft, first slice)

Moves the parts of the skill that must happen every time out of prose and into code.
The live SKILL.md is untouched. Nothing here changes how the skill behaves until a
rewritten SKILL.md that calls these scripts is proposed and approved.

## Run protocol (one run = one folder, e.g. `run/`)

| # | Command | What it enforces |
|---|---|---|
| 1 | `tx.py prep <transcript.docx> run/` | Converts, checks duration vs last timestamp and gaps (Step 1). Stops if incomplete. |
| 2 | `tx.py chunk run/ 1 <n>` for n = 1..K | Pass 1: every chunk, in order, none skipped. Logged. |
| 3 | write `run/ledger.json` | Decision ledger: every entry carries a verbatim quote and a line number. |
| 4 | `tx.py chunk run/ 2 <n>` for n = 1..K | Pass 2 is refused until Pass 1 is complete. |
| 5 | `tx.py scan run/` | Keyword scan; refused until both passes are done. |
| 6 | write `run/content.json` | One source for both outputs. Every item has `src`; the `checks` block answers every conditional rule. |
| 7 | `build.py run/` | Refuses to draft anything until reading, ledger, source trace and checks pass. Builds the Planner note and the PDF together, names the PDF from the client fields, renders page images. |
| 8 | hand-over, then write `run/receipt.json` | Chat display, PDF sent in chat, `device_commit_files`, folder listing, image check. |
| 9 | `verify.py run/` | PASS or FAIL per item. The reply must contain this output unedited. |

`verify.py run/ --stage pre|built|final` runs the gate up to that point.
`tx.py status run/` shows where a run stands, which also covers recovery after the chat is compressed.

## What is machine-checked

Both passes served in order; every ledger and source quote found verbatim in the transcript; no item without a source;
every request, instruction, change and hold in the ledger covered by an item (a change must be marked CHANGED, a hold must not become a task);
closing-minute keyword hits resolved; every action starts "Sitamah to"; no chase action sourced from "I'll get back to you";
credit life, cession, owner change, applications and correspondence each answered explicitly, with their consequences present;
no ID numbers; PDF-safe characters; PDF filename; every item and heading present in the PDF text; no stranded heading;
outputs not stale against `content.json`; PDF and Planner note not hand-edited; no PDF at a first/Fact Find meeting.

## What is attested, not proven

What Claude shows in the chat and what the device bridge saved to the laptop. `receipt.json` records the evidence
(pasted tool result, folder listing line) and `verify.py` labels those rows ATTEST. The scripts prove the text was put in
front of Claude twice and that every claim is traceable to the transcript; they cannot prove it was understood.

## Not done yet

- Tuned only on a synthetic transcript. The timestamp/duration parser needs one real (anonymised) Teams `.docx`.
- SKILL.md has not been rewritten to call these scripts (needs Paul's approval; bundled scripts need a zip upload).
- Other skills (ROA, SROA, Fact Find, applications, proposals) are not converted.

## Tests

`python3 -m unittest discover -s tests`: 47 tests, one passing end-to-end run and the rest each break one thing and
check the gate fails with the right message. All people and figures in the fixture are invented.
