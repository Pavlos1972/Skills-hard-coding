---
name: "om-tax-free-skill"
description: "Builds an Old Mutual Tax-Free Investment client proposal email for Paul Kafentzis (FSP45946) from Alwyn's quote, then saves it, drafts it in Outlook and alerts Sitamah. A program serves the documents page by page, checks every figure against their text, fills the fixed template, checks the draft and the Teams message read-backs and prints a short audit. Use when Paul asks for an OM Tax-Free proposal."
---

# OM Tax-Free Investment Proposal Email Builder

## Index

| # | Section | What it covers |
|---|---|---|
| 1 | Run it | The one command that starts the job and how every step works |
| 2 | What a finished run contains | The email, the saved copy, the draft, the Teams message and the short audit |
| 3 | Standing rules | The rules that never bend, one line each |
| 4 | When something goes wrong | What to do instead of improvising |
| 5 | Where the detail lives | The pages the program shows at each step |

**Last updated: 2026-11-03 16:13 (Athens time)**

**Recent changes** (last 5, one line each; full history in the repo `history/` folder)

| When (Athens time) | What changed |
|---|---|
| 2026-11-03 16:13 | First program-driven version: documents served page by page, answers checked against their text, fixed template filled by program, draft and Teams message read-backs checked, short audit |
| - | - |

## Run it

This skill is a program that walks you through the job one step at a time. You do not work from memory of this page: the program shows everything below again, at the right moment.

1. Find this skill's folder (the "Base directory" shown when the skill loaded; it contains `scripts/run.py`). If you are unsure: `find /mnt /root /home /opt /tmp -path '*om-tax-free-skill/scripts/run.py' 2>/dev/null | head -1`
2. Choose a new run folder, for example `/tmp/om-tf-<Surname>-<DDMMYY>`, and start: `python3 <skill folder>/scripts/run.py start <run folder> --client "First Surname"` (the client exactly as Paul named them). The program's first lines give you one sentence to say to Paul before anything else: which version of this skill is running.
3. Do exactly what the step says. When it says you are done, run `python3 <skill folder>/scripts/run.py done <run folder> <step>`. The program checks the proof and only then shows the next step. It refuses to skip a step.
4. After a long chat or a compression, run `python3 <skill folder>/scripts/run.py status <run folder>`.
5. The last step prints the SHORT AUDIT. Your reply to Paul is where the copy was saved, the draft's status, that Sitamah was messaged, the flags, and that audit, as they are.

Never rewrite, shorten or "improve" a program or the template during a run, and never type a figure from memory, a weekday, a total, a file name or the Teams message. If the self-test at the start fails, stop and tell Paul exactly what failed.

## What a finished run contains

- The **proposal email (.html)** built from the fixed template by the program from answers Paul confirmed: the full copy sent to Paul in the chat, the no-logo copy saved in the client's `Comparative Quotes` folder (never overwriting without Paul's yes).
- The **Outlook draft** (never sent by Claude), read back and checked by the program, and the **Teams message to Sitamah** (through Zapier, after Paul's one yes and a checked draft), read back and checked. Sitamah reviews the draft, attaches the three documents and emails the client.
- The **short audit** (Paul, 03/11/2026): one line per check in point form, each with a green tick or a red cross, one closing line for what is only attested. No long printout. A run without a PASS audit is not finished: say so.

## Standing rules

1. Every figure, name, date and address comes from the client's own file or Paul's words, with its source; the program refuses what it cannot find in the right document's text. Never invent, never reuse another client's figures.
2. The start date is always confirmed with Paul, even though the quote shows it. Weekdays are computed by the program, never typed.
3. A child's plan, a lump sum, a plan owner who is not the client, or two sources that disagree: stop and ask Paul. No wording is invented.
4. The Cc is always Sitamah Nathoo. Claude never sends the client email: Sitamah sends it from Drafts.
5. Nothing is sent without Paul's yes: his one yes at the confirmation table covers the draft and the message to Sitamah, which goes only after the draft is checked.
6. The template, the tax facts and the scripts are fixed; never hand-patch the HTML; never overwrite a file without Paul's yes.
7. Changes to this skill are made only in Claude Code and uploaded by Paul. Never say a change is live until he confirms.

## When something goes wrong

- The program refuses a step or an answer: read what it says is missing or not found, fix that, run it again.
- A document cannot be found on any of the three routes: tell Paul exactly which were tried; never substitute the nearest document and never build without the quote.
- A check shows a red cross: tell Paul exactly which line; fix the answers or the draft and run the check again; never hand-patch the HTML.
- The draft or the posted message does not read back right: do not message Sitamah (draft) or tell Paul exactly which line (message).

## Where the detail lives

The program prints the right page at the right step: `references/00-rules.md` (the rules), `01-locate.md` (the documents and the routes), `02-answers.md` (what comes from the file, what Paul is asked, the answers file), `03-build-rules.md` (the template's fixed rules, the files and the save), `04-draft.md` (the Outlook draft with Claude in Chrome), `05-message.md` (the Teams message through Zapier), `06-handover.md` (the reply). `steps.json` is the list of steps; `deliverables.json` is the list of outputs; `assets/tax_facts.json` and `assets/settings.json` hold the two things Paul may change later.
