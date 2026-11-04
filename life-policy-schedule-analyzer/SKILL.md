---
name: "life-policy-schedule-analyzer"
description: "Critically analyzes a client's life policy schedule or quote from any SA insurer for Paul Kafentzis (FSP45946): mistakes, better same-insurer options, premiums, paybacks, honest opinion. A program serves the documents page by page, checks every figure against the schedule and every product statement against saved sources, works out the premium table, draws the internal PDF report and the client slide decks and prints a short audit. Use when asked to analyze a schedule."
---

# Life Policy Schedule Analyzer

## Index

| # | Section | What it covers |
|---|---|---|
| 1 | Run it | The one command that starts the job and how every step works |
| 2 | What a finished run contains | The internal report, the client slides, the saved files, the chat summary and the short audit |
| 3 | Standing rules | The rules that never bend, one line each |
| 4 | When something goes wrong | What to do instead of improvising |
| 5 | Where the detail lives | The pages the program shows at each step |

**Last updated: 2026-11-04 12:02 (Athens time)**

**Recent changes** (last 5, one line each; full history in the repo `history/` folder)

| When (Athens time) | What changed |
|---|---|
| 2026-11-04 12:02 | First program-driven version: documents served page by page, every client figure checked against a verbatim line of the schedule, product statements against two saved sources, the premium table never invented, the internal report and the client slides drawn from one confirmed analysis and read back, short audit |
| 2026-11-04 11:55 | First program-driven version: documents served page by page, every client figure checked against a verbatim line of the schedule, product statements against two saved sources, the premium table never invented, the internal report and the client slides drawn from one confirmed analysis and read back, short audit |
| 2026-11-04 00:00 | First program-driven version: documents served page by page, every client figure checked against a verbatim line of the schedule, product statements against two saved sources, the premium table never invented, the internal report and the client slides drawn from one confirmed analysis and read back, short audit |
| - | - |

## Run it

This skill is a program that walks you through the job one step at a time. You do not work from memory of this page: the program shows everything below again, at the right moment.

1. Find this skill's folder (the "Base directory" shown when the skill loaded; it contains `scripts/run.py`). If you are unsure: `find /mnt /root /home /opt /tmp -path '*life-policy-schedule-analyzer/scripts/run.py' 2>/dev/null | head -1`
2. Choose a new run folder, for example `/tmp/lpa-<Surname>-<DDMMYY>`, and start: `python3 <skill folder>/scripts/run.py start <run folder> --client "First Surname"` (the client exactly as Paul named them). The program's first lines give you one sentence to say to Paul before anything else: which version of this skill is running.
3. Do exactly what the step says. When it says you are done, run `python3 <skill folder>/scripts/run.py done <run folder> <step>`. The program checks the proof and only then shows the next step. It refuses to skip a step.
4. After a long chat or a compression, run `python3 <skill folder>/scripts/run.py status <run folder>`.
5. The last step prints the tabulated chat summary and the SHORT AUDIT. Your reply to Paul is those two, as they are.

Never rewrite, shorten or "improve" a program during a run, and never type a figure from memory, a premium number, a total, a file name or a finding's number. If the self-test at the start fails, stop and tell Paul exactly what failed.

## What a finished run contains

- One **internal analysis PDF per policy** (A4, for Paul only, labelled INTERNAL on every page) and the **client slide decks** (one per current insurer, plus Report 2 only when a proposed quote exists), all drawn by the program from ONE analysis Paul confirmed, presented to Paul in the chat and saved in the client's `Analysis & Comparison Reports` folder (never overwriting without Paul's yes).
- The **tabulated chat summary**: the Verdict line, the Benefit Summary Table, the numbered Action Required list and the folder, for each policy.
- The **short audit** (Paul, 03/11/2026): one line per check in point form, each with a green tick or a red cross, one closing line for what is only attested. A run without a PASS audit is not finished: say so. Nothing is emailed or messaged: this skill sends nothing.

## Standing rules

1. A critique, not a transcription: be critical of the schedule on the client's behalf, above all about whether the SAME insurer today would offer meaningfully better cover. Never manufacture a finding; never invent a "better option".
2. Every client figure is a verbatim line of the client's own document; every product statement is a verbatim line of a saved source (two sources, the insurer's own guide and an independent one, or it is labelled SINGLE SOURCE). Never invent, never reuse another client's figures.
3. The premium table is the insurer's own, or computed from a stated fixed rate, or from Paul's assumption in his words, or "not provided": never an invented number.
4. The cession check and the second life check are done every time, even when the answer is "none". Every finding is Action Required or For Your Awareness (Action Required when unsure).
5. The internal report is for Paul only. The client slides carry no Honest Opinion, no INTERNAL wording and no internal jargon, always show the four categories ("Not held" where the client does not have one) and always include the proposed insurer's payback in Report 2, from the insurer's own payback document.
6. Reports are saved only in the client's `Analysis & Comparison Reports` folder and never overwritten without Paul's yes. Never touch another broker's folder.
7. Changes to this skill are made only in Claude Code and uploaded by Paul. Never say a change is live until he confirms.

## When something goes wrong

- The program refuses a step or an analysis: read what it says is missing or not found, fix that, run it again.
- A document cannot be found on any route: tell Paul exactly which were tried; never substitute the nearest document. A product source or the payback document that cannot be found: ask Paul and record his words; never guess a feature or a payback figure.
- A slide does not fit: shorten that text in the analysis; never clip it.
- A check shows a red cross: tell Paul exactly which line; fix the analysis and run the check again; never hand-patch a PDF.

## Where the detail lives

The program prints the right page at the right step: `references/00-rules.md` (the rules), `01-locate.md` (the documents and the routes), `02-research.md` and `08-product-hints.md` (the product sources and the benchmark), `03-analysis.md` (the analysis file, what to extract, the findings, the Honest Opinion, the client slides), `04-check.md` (what the program works out), `05-build.md` (the two documents), `06-save.md` (the folder and the names), `07-handover.md` (the reply). `steps.json` is the list of steps; `deliverables.json` is the list of outputs; `assets/settings.json` (the limits and the folder name), `assets/wording.json` (the fixed sentences) and `assets/slide_words.json` (the words a client slide must never carry) hold the things Paul may change later.
