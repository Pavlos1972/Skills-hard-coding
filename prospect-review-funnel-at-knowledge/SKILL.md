---
name: "prospect-review-funnel-at-knowledge"
description: "Wealth Revolution's Prospect & Review funnel in AdviceTech: stages, owners, decision gates, routes, modules. A program drives the work step by step: it locates the six funnel documents by the three routes, serves only the pages the work needs, proves each stage was read in the STREAMLINED document and the AT MASTER PLAN, checks every AdviceTech plan against the rules, records documents first, and prints a short audit. Use for AT pipeline builds or tests, funnel questions, pipeline document edits, reviews on the flow page and moving clients."
---

# Prospect & Review Funnel - AT Knowledge

## Index

| # | Section | What it covers |
|---|---|---|
| 1 | Run it | The one command that starts the job and how every step works |
| 2 | The six kinds of work | Funnel question, moving a client, AdviceTech build, AdviceTech test, document edit, review on the flow page |
| 3 | What a finished run contains | The short audit and the items table |
| 4 | Standing rules | The rules that never bend, one line each |
| 5 | When something goes wrong | What to do instead of improvising |
| 6 | Where the detail lives | The pages the program shows at each step |

**Last updated: 2026-11-04 16:53 (Athens time)**

**Recent changes** (last 5, one line each; full history in the repo `history/` folder)

| When (Athens time) | What changed |
|---|---|
| 2026-11-04 16:53 | Shorter audit lines |
| 2026-11-04 16:52 | Pages and data moved out of the entry page; route checker, quoted-line proof, documents-first receipt and never-touch guard |
| 2026-11-04 16:45 | First program-driven version: stage routes as data and checked, only the pages the work needs, a quoted line from each of the two documents for every stage, plan rules, documents first, one status file, short audit |
| - | - |

## Run it

This skill is a program that walks you through the job one step at a time. You do not work from memory of this page or load the whole funnel: the program shows only the pages the work needs, at the right moment.

1. Find this skill's folder (the "Base directory" shown when the skill loaded; it contains `scripts/run.py`). If you are unsure: `find /mnt /root /home /opt /tmp -path '*prospect-review-funnel-at-knowledge/scripts/run.py' 2>/dev/null | head -1`
2. Choose a new run folder, for example `/tmp/wr-funnel-<DDMMYY>-<kind>`, and start: `python3 <skill folder>/scripts/run.py start <run folder> --kind <kind> --request "Paul's own words"`. The program's first lines give you one sentence to say to Paul before anything else: which version of this skill is running.
3. Do exactly what the step says. When it says you are done, run `python3 <skill folder>/scripts/run.py done <run folder> <step>`. The program checks the proof and only then shows the next step. It refuses to skip a step.
4. After a long chat or a compression, run `python3 <skill folder>/scripts/run.py status <run folder>`. For the open items, the build phases and the counts: `python3 <skill folder>/scripts/run.py info`.
5. The last step prints the SHORT AUDIT (and the items table for AdviceTech work). Your reply to Paul is those, as they are, plus the one question it ends with.

Never rewrite, shorten or "improve" the programs during a run. If the self-test at the start fails, stop and tell Paul exactly what failed.

## The six kinds of work

| Kind | Use it for | Steps |
|---|---|---|
| `question` | A question about the funnel: answer with the stage code, owner and route | locate, stages, read, proof, answer, final |
| `move` | Working a client through the stages: the stage, the open items, the outcome options, the line to tick | locate, stages, read, proof, answer, final |
| `build` | An AdviceTech build or correction | locate, stages, read, proof, plan, confirm, record, final |
| `test` | An AdviceTech test (Mr John Snow only) | the same as build |
| `docs` | A change to the funnel documents | the same as build (documents only) |
| `review` | Applying Paul's notes from the working flow page | the same as docs |

## What a finished run contains

- The **short audit** (Paul, 03/11/2026): one line per check with a green tick or a red cross, one closing line for what is only attested.
- For AdviceTech work and document work, the **items table** (one row per item with running totals) and the one question "Go ahead with <next>?".
- The full record stays in the run folder (`out_record/audit-full.txt`); the run folder holds no client data.

## Standing rules

1. Source first, never invent: write only what the six documents say or Paul told you; where the documents disagree the STREAMLINED wins on wording and logic and the AT MASTER PLAN on AdviceTech detail, and the difference is flagged to Paul.
2. Read before you write: every stage touched is read in both documents and a line from each is quoted; the program checks it.
3. Documents first, always: every change, including every deletion, is written into the documents before AdviceTech is touched.
4. Check before you claim: never say it is done until the audit is on screen.
5. Paul approves every AdviceTech change and watches in Chrome; Claude never deletes anything in AdviceTech; tests run on Mr John Snow only; Charl's items are never touched.
6. Changes to this skill are made only in Claude Code and uploaded by Paul. Never edit it inside a chat, and never say a change is live until he confirms.

## When something goes wrong

- The program refuses a step: read what it says is missing, fix that, run `done` again.
- A document cannot be found: the access log must show all three routes tried; then ask Paul. Never answer from memory of the pages.
- The pages and a document disagree: the document wins; tell Paul where.
- A quoted line is refused: it is not in the document's text. Find the real block; never paraphrase.

## Where the detail lives

The program prints the right page at the right step: `references/00-rules.md` (the rules), `01-documents.md` (the six documents and which wins), `02-roles.md`, `03-parents.md`, `04-family-a.md`, `05-family-b.md`, `06-family-cd.md`, `07-gates.md` (gates and decisions), `08-at-map.md`, `09-build-rules.md`, `10-procedures.md`, `11-checks.md`, `12-handover.md`, `13-plan-file.md`. `assets/funnel.json` holds the stage routes, `assets/status.json` the counts, build phases and open items, `assets/settings.json` the pages and steps of each kind of work.
