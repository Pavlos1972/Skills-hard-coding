---
name: "investment-comparisons-skill"
description: "Builds a client-facing comparison of two or more providers' RA, Tax-Free, Endowment or Living Annuity quotes for Paul Kafentzis (FSP45946), using the actual fees and never EAC, then saves it, drafts it in Outlook and alerts Sitamah. A program checks every figure against the quotes and the saved fund fact sheets, compares the quotes, builds the four fixed tables and prints a short audit. Use when asked to compare investment quotes."
---

# Investment Comparisons Builder

## Index

| # | Section | What it covers |
|---|---|---|
| 1 | Run it | The one command that starts the job and how every step works |
| 2 | What a finished run contains | The email, the saved copy, the draft, the Teams message and the short audit |
| 3 | Standing rules | The rules that never bend, one line each |
| 4 | When something goes wrong | What to do instead of improvising |
| 5 | Where the detail lives | The pages the program shows at each step |

**Last updated: 2026-11-04 10:14 (Athens time)**

**Recent changes** (last 5, one line each; full history in the repo `history/` folder)

| When (Athens time) | What changed |
|---|---|
| 2026-11-04 10:14 | First program-driven version: quotes and fund fact sheets served page by page and every figure checked against their text, the comparison worked out by the program, four fixed tables built from a template, draft and Teams read-backs checked, short audit |
| - | - |

## Run it

This skill is a program that walks you through the job one step at a time. You do not work from memory of this page: the program shows everything below again, at the right moment.

1. Find this skill's folder (the "Base directory" shown when the skill loaded; it contains `scripts/run.py`). If you are unsure: `find /mnt /root /home /opt /tmp -path '*investment-comparisons-skill/scripts/run.py' 2>/dev/null | head -1`
2. Choose a new run folder, for example `/tmp/cmp-<Surname>-<DDMMYY>`, and start: `python3 <skill folder>/scripts/run.py start <run folder> --client "First Surname"` (the client exactly as Paul named them). The program's first lines give you one sentence to say to Paul before anything else: which version of this skill is running.
3. Do exactly what the step says. When it says you are done, run `python3 <skill folder>/scripts/run.py done <run folder> <step>`. The program checks the proof and only then shows the next step. It refuses to skip a step.
4. After a long chat or a compression, run `python3 <skill folder>/scripts/run.py status <run folder>`.
5. The last step prints the SHORT AUDIT. Your reply to Paul is where the copy was saved, the draft's status, that Sitamah was messaged, the flags, and that audit, as they are.

Never rewrite, shorten or "improve" a program or the template during a run, and never type a figure from memory, a total, a weekday, a file name or the Teams message. If the self-test at the start fails, stop and tell Paul exactly what failed.

## What a finished run contains

- The **comparison email (.html)** built from the fixed template by the program from answers Paul confirmed: the four tables in a fixed order, the full copy sent to Paul in the chat, the no-logo copy saved in the client's `Comparative Quotes` (never overwriting without Paul's yes).
- The **Outlook draft** (never sent by Claude), read back and checked by the program, and the **Teams message to Sitamah** (through Zapier, after Paul's one yes and a checked draft), read back and checked. Sitamah attaches the quotes and the fund fact sheets and emails the client.
- The **short audit** (Paul, 03/11/2026): one line per check in point form, each with a green tick or a red cross, one closing line for what is only attested. A run without a PASS audit is not finished: say so.

## Standing rules

1. Every figure, name, date and fee comes from the client's own quotes, the fund fact sheets saved for this comparison or Paul's words, with its source; the program refuses what it cannot find in the right document's text. Never invent, never reuse another client's figures or wording.
2. Actual cost, never EAC: every fee is its own line from the quote; a quote that shows only a blended cost is refused. The totals are added up by the program.
3. Only quotes for the same product type are compared. The program compares the contribution structure, amount, yearly increase and term: a mismatch stops the run unless Paul says to go on, and the email then labels it.
4. Every fund's figures come from its CURRENT fact sheet, fetched for this comparison, saved as text and registered; each fund shows its own fact sheet date; a sheet more than a quarter old or missing is flagged in the email.
5. Plain English: every industry term is explained where it is used; every table has an intro line; the four tables are in the fixed order; the optional parts (tax note, flexibility, fees-only comparison) only when Paul asks. The Tax-Free limits are not typed: they come from `assets/tax_facts.json` once Paul confirms them.
6. Nothing is sent without Paul's yes: his one yes at the confirmation table covers the draft and the message to Sitamah, which goes only after the draft is checked. The Cc is always Sitamah Nathoo. Claude never sends the client email.
7. The template and the scripts are fixed; never hand-patch the HTML; never overwrite a file without Paul's yes.
8. Changes to this skill are made only in Claude Code and uploaded by Paul. Never say a change is live until he confirms.

## When something goes wrong

- The program refuses a step or an answer: read what it says is missing or not found, fix that, run it again.
- A document cannot be found on any route: tell Paul exactly which were tried; never substitute the nearest document. A fund fact sheet that cannot be found: ask Paul and record his words; never guess a figure.
- The quotes do not match (amount, term, structure): do not go on unless Paul says so.
- A check shows a red cross: tell Paul exactly which line; fix the answers or the draft and run the check again; never hand-patch the HTML.
- The draft or the posted message does not read back right: do not message Sitamah (draft) or tell Paul exactly which line (message).

## Where the detail lives

The program prints the right page at the right step: `references/00-rules.md` (the rules), `01-locate.md` (the documents, the fund fact sheets and the routes), `02-answers.md` (the answers file, fees, loyalty benefits, fund sheets, supplementary documents), `03-comparison.md` (apples-to-apples, tax, the optional parts), `04-build-rules.md` (the four tables, the plain-English checks, the files and the save), `05-draft.md` (the Outlook draft with Claude in Chrome), `06-message.md` (the Teams message through Zapier), `07-handover.md` (the reply). `steps.json` is the list of steps; `deliverables.json` is the list of outputs; `assets/settings.json` (the signature setting), `assets/wording.json` (the fixed sentences), `assets/plain_terms.json` (the plain-English terms) and `assets/tax_facts.json` (the Tax-Free limits, unconfirmed) hold the things Paul may change later.
