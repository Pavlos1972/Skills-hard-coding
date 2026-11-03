---
name: "astute-summary-report-skill"
description: "Builds a verified Astute Report Summary PDF for Paul at Wealth Revolution: risk covers, investments, group risk, retirement funds, paid-up policies. A program serves the report page by page, checks every figure entered against the report's own text, adds up the totals, draws the PDF and prints a short audit. Use for 'summarize the Astute/CCP report'."
---

# Astute Summary Report

## Index

| # | Section | What it covers |
|---|---|---|
| 1 | Run it | The one command that starts the job and how every step works |
| 2 | What a finished run contains | The saved PDF, the flag list and the short audit |
| 3 | Standing rules | The rules that never bend, one line each |
| 4 | When something goes wrong | What to do instead of improvising |
| 5 | Where the detail lives | The pages the program shows at each step |

**Last updated: 2026-11-03 13:50 (Athens time)**

**Recent changes** (last 5, one line each; full history in the repo `history/` folder)

| When (Athens time) | What changed |
|---|---|
| 2026-11-03 13:50 | First program-driven version: a program serves the report page by page, checks every entry against the report's text, adds up the totals, draws the PDF and prints a short audit |
| 2026-11-03 13:49 | First program-driven version: a program serves the report page by page, checks every entry against the report's text, adds up the totals, draws the PDF and prints a short audit |
| - | - |

## Run it

This skill is a program that walks you through the job one step at a time. You do not work from memory of this page: the program shows everything below again, at the right moment.

1. Find this skill's folder (the "Base directory" shown when the skill loaded; it contains `scripts/run.py`). If you are unsure: `find /mnt /root /home /opt /tmp -path '*astute-summary-report-skill/scripts/run.py' 2>/dev/null | head -1`
2. Choose a new run folder, for example `/tmp/wr-as-<Surname>-<DDMMYY>`, and start: `python3 <skill folder>/scripts/run.py start <run folder> --client "First Surname"` (the client exactly as Paul named them). The program's first lines give you one sentence to say to Paul before anything else: which version of this skill is running.
3. Do exactly what the step says. When it says you are done, run `python3 <skill folder>/scripts/run.py done <run folder> <step>`. The program checks the proof and only then shows the next step. It refuses to skip a step.
4. After a long chat or a compression, run `python3 <skill folder>/scripts/run.py status <run folder>`.
5. The last step prints the numbered flag list and the SHORT AUDIT. Your reply to Paul is those, with the PDF, as they are.

Never rewrite, shorten or "improve" the programs during a run, and never write drawing code, type a total or type the file name. If the self-test at the start fails, stop and tell Paul exactly what failed (it needs `pdfplumber`, `reportlab` and `pdftoppm`).

## What a finished run contains

- The **Astute Report Summary PDF**, drawn by the program from the data you entered, saved into the client's `5. Astute` folder beside the report (never overwriting) and sent in the chat.
- The **numbered flag list**, most important first, so Paul knows what to verify.
- The **short audit** (Paul, 03/11/2026): one line per check in point form, each with a green tick or a red cross, one closing line for what is only attested. No long printout.
- Nothing is sent to anyone. A run without a PASS audit is not finished: say so.

## Standing rules

1. Every client figure comes from the report; the program refuses an entry it cannot find in the report's text. Never guess; leave it empty and it is flagged.
2. Cession status is never stated; the cession note is always included.
3. Contradictions, missing or zero values, unknown products and providers with no data are flagged, never silently resolved. Only policies Astute labels paid-up go in Section 3.
4. Every benefit is labelled stand-alone or accelerated and every policy has a premium pattern.
5. The programs draw the PDF and derive the file name; you never write code or type a total.
6. Changes to this skill are made only in Claude Code and uploaded by Paul. Never say a change is live until he confirms.

## When something goes wrong

- The program refuses a step or an entry: read what it says is missing or not found, fix that, run it again.
- The report cannot be found on any of the three routes: tell Paul exactly which were tried; never invent a report.
- The report is scanned (no readable text): the program says so; view every such page as an image; the figure check is then attested, not proven.
- The folder cannot be found or the save cannot be listed: say plainly that it was not saved and deliver in the chat only.

## Where the detail lives

The program prints the right page at the right step: `references/00-rules.md` (the rules), `01-locate.md` (the folder and the routes), `02-data.md` (the data file, field by field), `03-products-flags.md` (products and flags), `04-build-save.md` (the look, the sections and the save), `05-handover.md` (the reply). `steps.json` is the list of steps; `deliverables.json` is the list of outputs.
