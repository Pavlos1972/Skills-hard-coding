---
name: "fact-find-summary"
description: "Builds the Fact Find Summary PDF for Paul Kafentzis (FSP45946) from the completed Fact Find Transcript PDF (the report made by ff-population-transcript). A program reads that PDF, composes the nine fixed sections, recomputes the totals and draws an A4 PDF; a checker prints a short audit, one line per check with a green tick or a red cross. Use when asked to summarize a fact find."
---

# Fact Find Summary

## Index

| # | Section | What it covers |
|---|---|---|
| 1 | Run it | The one command that starts the job and how every step works |
| 2 | What a finished run contains | The deliverable and the short audit that ends the job |
| 3 | Standing rules | The rules that never bend, one line each |
| 4 | When something goes wrong | What to do instead of improvising |
| 5 | Where the detail lives | The pages the program shows at each step |

**Last updated: 2026-11-03 09:41 (Athens time)**

**Recent changes** (last 5, one line each; full history in the repo `history/` folder)

| When (Athens time) | What changed |
|---|---|
| 2026-11-03 09:41 | Added the self-test command the packager needs (run.py preflight) |
| 2026-11-03 09:41 | Added the reference page of true stories, the one end-to-end test, the rule-by-rule records and the list for Paul |
| 2026-11-03 09:38 | First program-driven version: a program reads the Fact Find Transcript PDF, composes the nine sections, recomputes totals and draws an A4 PDF; a checker prints a short audit with green ticks and red crosses |
| - | - |

## Run it

This skill is a program that walks you through the job one step at a time. You do not work from memory of this page: the program shows everything below again, at the right moment.

1. Find this skill's folder (the "Base directory" shown when the skill loaded; it contains `scripts/run.py`). If you are unsure: `find /mnt /root /home /opt /tmp -path '*fact-find-summary/scripts/run.py' 2>/dev/null | head -1`
2. Choose a new run folder, for example `/tmp/wr-fs-<Surname>-<DDMMYY>`, and start: `python3 <skill folder>/scripts/run.py start <run folder> --client "First Surname" --date DD/MM/YYYY`. The client and the meeting date are taken exactly from Paul's message; the program checks the Fact Find PDF against them. For a spouse seen in the same meeting add `--joint "Other Surname"`. The program's first lines give you one sentence to say to Paul before anything else: which version of this skill is running.
3. Do exactly what the step says. When it says you are done, run `python3 <skill folder>/scripts/run.py done <run folder> <step>`. The program checks the proof and only then shows the next step. It refuses to skip a step.
4. After a long chat or a compression, run `python3 <skill folder>/scripts/run.py status <run folder>`.
5. The last step prints the SHORT AUDIT. Your reply to Paul is that audit, as it is.

Never rewrite, shorten or "improve" the programs during a run, and never replace the PDF with a text draft or a Word file. If the self-test at the start fails, stop and tell Paul exactly what failed.

## What a finished run contains

- The **Fact Find Summary PDF** (`Fact Find Summary - DD.MM.YY - (First Surname).pdf`), drawn by the program in the fixed nine sections, sent in the chat, saved into the client's `2. Fact Find` folder and listed back (the listed size must equal the local file's).
- The **short audit** (Paul, 03/11/2026): one line per check in point form, each with a green tick or a red cross, and one closing line for what is only attested. No long printout.
- No message and no Planner note: `client-teams-transcript-skill` makes those once. Nothing is sent without Paul's yes.
- A run without a PASS audit is not finished: say so.

## Standing rules

1. The source is the Fact Find Transcript PDF made by `ff-population-transcript`; the Summary never has a value the Fact Find does not have.
2. Never invent: the checker compares every Summary value with its Fact Find value.
3. Client facts come from the client's file first: computer, then Microsoft 365, then Zapier, every try logged; Paul is asked last.
4. Totals reconcile to the cent and debt is never left out because of credit life.
5. The standing ABIs are fixed: Life Cover (WOL) 3%, Childcare 5%, Household needs 5%, Dread Disease 3%.
6. The nine sections and the Section 8 sub-headings are fixed.
7. Every flag of the Fact Find is carried into Items Requiring Follow-Up; owners are Cameron (short-term), CL (Will), Valerie (medical aid), Lizelle (gross income, ACI) only.
8. One PDF only (A4), never a Word file; the file name is derived by the program.
9. Every correction re-opens the whole task: fix the Fact Find, run this skill again from the read step.
10. If a rule cannot be met, stop and say exactly which one and why. Never hand over partial work as complete.
11. Changes to this skill are made only in Claude Code and uploaded by Paul. Never say a change is live until he confirms.

## When something goes wrong

- The program refuses a step: read what it says is missing, fix that, run `done` again.
- The program says STOP at the read step (the PDF is not the program-drawn Fact Find, or it is for another client or date): tell Paul in one line. Do not guess.
- You cannot reach the file: try all three routes and log each, then ask Paul.
- A red cross in the audit: fix its cause. If the Fact Find itself is wrong, tell Paul; do not edit the Summary.
- Paul corrects something: rule 9 above.

## Where the detail lives

The program prints the right page at the right step, so you do not need to open them yourself: `references/00-rules.md` (the rules), `01` where the file is and how to save, `02` what the reader and the composer do and the follow-up owners, `03` the nine sections, the standing values and the look, `04` the hand-over and the short audit. `steps.json` is the list of steps; `deliverables.json` is the list of outputs.
