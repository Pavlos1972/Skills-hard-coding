---
name: "om-optimal-ra-proposal"
description: "Builds the Old Mutual Optimal Retirement Annuity (RA) client proposal email for Paul Kafentzis (FSP45946), and the separate Lump Sum Investment email when a lump sum applies, then saves, drafts in Outlook and alerts Sitamah. A program serves the documents page by page, checks every figure against their text, runs the Tax Reform Tool itself and proves the old audit checks, fills the fixed templates, checks the draft and Teams read-backs and prints a short audit. Use when Paul asks for an OM Optimal RA proposal."
---

# OM Optimal RA Proposal Builder

## Index

| # | Section | What it covers |
|---|---|---|
| 1 | Run it | The one command that starts the job and how every step works |
| 2 | What a finished run contains | The email(s), the saved copy, the draft, the Teams message and the short audit |
| 3 | Standing rules | The rules that never bend, one line each |
| 4 | When something goes wrong | What to do instead of improvising |
| 5 | Where the detail lives | The pages the program shows at each step |

**Last updated: 2026-11-04 09:31 (Athens time)**

**Recent changes** (last 5, one line each; full history in the repo `history/` folder)

| When (Athens time) | What changed |
|---|---|
| 2026-11-04 09:31 | First program-driven version: documents served page by page, the Tax Reform Tool run by the program (checked against the tax facts), answers checked against their text, fixed templates filled by program (main and lump sum), draft and Teams read-backs checked, short audit |
| - | - |

## Run it

This skill is a program that walks you through the job one step at a time. You do not work from memory of this page: the program shows everything below again, at the right moment.

1. Find this skill's folder (the "Base directory" shown when the skill loaded; it contains `scripts/run.py`). If you are unsure: `find /mnt /root /home /opt /tmp -path '*om-optimal-ra-proposal/scripts/run.py' 2>/dev/null | head -1`
2. Choose a new run folder, for example `/tmp/ra-<Surname>-<DDMMYY>`, and start: `python3 <skill folder>/scripts/run.py start <run folder> --client "First Surname"` (the client exactly as Paul named them). For the separate Lump Sum Investment email add `--document lump_sum` (a second run, its own folder). The program's first lines give you one sentence to say to Paul before anything else: which version of this skill is running.
3. Do exactly what the step says. When it says you are done, run `python3 <skill folder>/scripts/run.py done <run folder> <step>`. The program checks the proof and only then shows the next step. It refuses to skip a step.
4. After a long chat or a compression, run `python3 <skill folder>/scripts/run.py status <run folder>`.
5. The last step prints the SHORT AUDIT. Your reply to Paul is where the copy was saved, the draft's status, that Sitamah was messaged, the flags, and that audit, as they are.

Never rewrite, shorten or "improve" a program, the workbook or the template during a run, and never type a figure from memory, a tax figure, a weekday, a file name or the Teams message. If the self-test at the start fails (for example LibreOffice is missing), stop and tell Paul exactly what failed.

## What a finished run contains

- The **proposal email (.html)** built from the fixed template by the program from answers Paul confirmed and from the Tax Reform Tool's own results: the full copy sent to Paul in the chat, the no-logo copy saved in the RA transaction folder's `Comparative Quotes` (never overwriting without Paul's yes). When a lump sum goes in, a **second, separate Lump Sum Investment email** in a second run.
- The **Outlook draft** (never sent by Claude), read back and checked by the program, and the **Teams message to Sitamah** (through Zapier, after Paul's one yes and a checked draft), read back and checked. Sitamah attaches the documents and emails the client.
- The **short audit** (Paul, 03/11/2026): one line per check in point form, each with a green tick or a red cross, one closing line for what is only attested. A run without a PASS audit is not finished: say so.

## Standing rules

1. Every figure, name, date, fee and address comes from the client's own documents or Paul's words, with its source; the program refuses what it cannot find in the right document's text. Never invent, never reuse another client's figures or wording.
2. The Tax Reform Tool is run by the program (four scenarios recalculated in LibreOffice, every figure recomputed independently). Nobody types, copies or adjusts a tax figure. From 01/03/2027 the tax tables are out of date: stop and ask Paul.
3. The three-table logic is fixed: Table 1 = today (every existing RA named, tax saved shown), Table 2 = the full deduction (one new RA row), Table 3 = what is proposed (replace: the new RA only; keep: existing + new). Pension and provident rows appear in all three tables; never mix the labels.
4. The RGAR is never an attachment of this email. The risk profile is always Moderate, the ACI 10%, the admin charge R 300. The Cc is always Sitamah Nathoo. Claude never sends the client email: Sitamah sends it from Drafts.
5. A lump sum is never added to the tool's inputs; its email is separate and uses one of two verbatim sentences. Section 14 or voluntary is Paul's answer, never inferred; a voluntary lump sum needs Paul's tax note.
6. Nothing is sent without Paul's yes: his one yes at the confirmation table covers the draft and the message to Sitamah, which goes only after the draft is checked.
7. The templates, the workbook and the scripts are fixed; never hand-patch the HTML; never overwrite a file without Paul's yes.
8. Changes to this skill are made only in Claude Code and uploaded by Paul. Never say a change is live until he confirms.

## When something goes wrong

- The program refuses a step or an answer: read what it says is missing or not found, fix that, run it again.
- A document cannot be found on any of the three routes: tell Paul exactly which were tried; never substitute the nearest document.
- The tool results disagree with the tax facts, or LibreOffice is missing: tell Paul exactly this; never type a tax figure.
- A check shows a red cross: tell Paul exactly which line; fix the answers or the draft and run the check again; never hand-patch the HTML.
- The draft or the posted message does not read back right: do not message Sitamah (draft) or tell Paul exactly which line (message).

## Where the detail lives

The program prints the right page at the right step: `references/00-rules.md` (the rules), `01-locate.md` (the documents and the routes), `02-answers.md` (what comes from the documents, what Paul is asked, the answers files), `03-tax.md` (the Tax Reform Tool, the scenarios and the audit checks), `04-build-rules.md` (the template's fixed rules, the files and the save), `05-draft.md` (the Outlook draft with Claude in Chrome), `06-message.md` (the Teams message through Zapier), `07-handover.md` (the reply). `steps.json` is the list of steps; `deliverables.json` is the list of outputs; `assets/settings.json` (the signature setting), `assets/wording.json` (Paul's approved sentences) and `assets/tax_facts.json` (the tax tables) hold the things Paul may change later.
