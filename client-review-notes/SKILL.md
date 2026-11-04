---
name: "client-review-notes"
description: "Formats raw Outlook contact notes into a standard Client Record for Paul Kafentzis (FSP45946), delivered as a .md file. A program registers the notes as the only source, draws the record in the fixed layout from one data file, proves every verbatim item is in the notes, checks that every date, amount, number, contract code, ID, link and name of each entry is kept, flags typos and do-not-contact lines, checks duplicates and prints a short audit. Use for 'format a client record', 'compile client review notes', or merging duplicate records."
---

# Client Review Notes

## Index

| # | Section | What it covers |
|---|---|---|
| 1 | Run it | The one command that starts the job and how every step works |
| 2 | What a finished run contains | The .md record, the short audit and the block for Paul |
| 3 | Standing rules | The rules that never bend, one line each |
| 4 | When something goes wrong | What to do instead of improvising |
| 5 | Where the detail lives | The pages the program shows at each step |

**Last updated: 2026-11-04 15:32 (Athens time)**

**Recent changes** (last 5, one line each; full history in the repo `history/` folder)

| When (Athens time) | What changed |
|---|---|
| 2026-11-04 15:32 | First program-driven version: the Client Record is one data file drawn by a program in the fixed layout, every verbatim item and every date, amount, number, code, link and name of the raw notes is checked, and a checker rebuilds everything and compares |
| - | - |

## Run it

This skill is a program that walks you through the job one step at a time. You do not work from memory of this page: the program shows everything below again, at the right moment.

1. Find this skill's folder (the "Base directory" shown when the skill loaded; it contains `scripts/run.py`). If you are unsure: `find /mnt /root /home /opt /tmp -path '*client-review-notes/scripts/run.py' 2>/dev/null | head -1`
2. Choose a new run folder, for example `/tmp/wr-crn-<Surname>-<DDMMYY>`, and start: `python3 <skill folder>/scripts/run.py start <run folder> --client "First Surname"`. The program's first lines give you one sentence to say to Paul before anything else: which version of this skill is running.
3. Do exactly what the step says. When it says you are done, run `python3 <skill folder>/scripts/run.py done <run folder> <step>`. The program checks the proof and only then shows the next step. It refuses to skip a step.
4. After a long chat or a compression, run `python3 <skill folder>/scripts/run.py status <run folder>`.
5. The last step prints the SHORT AUDIT and the block for Paul. Your reply to Paul is those, as they are, plus one plain sentence.

Never rewrite, shorten or "improve" the programs during a run, and never type the Markdown yourself. If the self-test at the start fails, stop and tell Paul exactly what failed. Client data stays in the run folder, never in a repo.

## What a finished run contains

- The **Client Record**: a downloadable `.md` file (`Client Record - DD.MM.YY - First Surname.md`) drawn by the program from one data file: a header, the 18 fields in the fixed order, Life & Investments in three lists, Notes in BOLD ALL CAPS date blocks (oldest first), Commission. Sent in the chat as a file; a copy in the client's folder only when Paul asks.
- The **short audit** (Paul, 03/11/2026): one line per check, each with a green tick or a red cross, one closing line for what is only attested, and a block for Paul: what was left out of the record on purpose (with the reason) and the flags at the top of Notes.

## Standing rules

1. The raw notes Paul gave are the only source. Nothing is invented: what the notes do not state reads `Not recorded.`
2. This is reformatting with summarisation, never a lossy summary: every date, amount, percentage, number, contract code, ID, email, link, name and abbreviation of each raw entry stays in the record, or is listed as left out with a reason Paul sees.
3. Contract numbers, DOC dates, premiums, status notes, IDs and commission are verbatim; apparent typos are kept and flagged, never silently corrected. "Do not contact" lines are reproduced in full and flagged at the top of Notes.
4. An earlier record of the same client is shown to Paul and he decides before anything is merged.
5. The file is the deliverable, never chat-only text. There is no confirmation step: the record is built as soon as the notes are registered.
6. Changes to this skill are made only in Claude Code and uploaded by Paul. Never say a change is live until he confirms.

## When something goes wrong

- The program refuses a step: read what it says is missing, fix that, run `done` again.
- It says no dated entries were recognised: the coverage check is over the whole note; tell Paul, and ask him for a sample of the layout if it keeps happening.
- It lists something the notes hold that the record lacks: keep it (condensed) or list it in `left_out` with a reason; never delete the notes' fact to make the check pass.
- The notes look lost or incomplete: flag it with ⚠️ and tell Paul; never fill the gap.

## Where the detail lives

The program prints the right page at the right step: `references/00-rules.md` (the rules), `01-source.md` (the raw notes), `02-record.md` (the record file and every rule on the fields and the Notes), `03-duplicates.md`, `04-deliver.md`, `05-handover.md` (the reply), `06-reference.md` (abbreviations, contacts, systems, the layout). `assets/settings.json` holds the field list, the glossary and the layout settings. `steps.json` is the list of steps; `deliverables.json` is the list of outputs.
