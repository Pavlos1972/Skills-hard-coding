---
name: "client-pipeline-board"
description: "Runs a Wealth Revolution client or prospect through the pipeline board: Fact Find, each product line (Life Cover, Retirement Annuity, Investments, RGAR/EGAR, Medical Aid, Will, Short-Term Insurance), referrals, follow-up appointments, Sitamah updates and ROA/SROA hand-overs. A program holds the board as one data file, checks every card against the rules, applies the send table, builds the Sitamah messages, draws the page and prints a short audit. Use whenever a client or prospect is being worked through the sales or review pipeline."
---

# Client Pipeline Board

## Index

| # | Section | What it covers |
|---|---|---|
| 1 | Run it | The one command that starts the job and how every step works |
| 2 | What a finished run contains | The board, the emails, the Sitamah messages, the check-in and the short audit |
| 3 | Standing rules | The rules that never bend, one line each |
| 4 | When something goes wrong | What to do instead of improvising |
| 5 | Where the detail lives | The pages the program shows at each step |

**Last updated: 2026-11-04 13:53 (Athens time)**

**Recent changes** (last 5, one line each; full history in the repo `history/` folder)

| When (Athens time) | What changed |
|---|---|
| 2026-11-04 13:53 | First program-driven version: the board is one data file, a program checks every card, applies the send table, builds the Sitamah messages and the page, and a checker rebuilds everything and compares |
| - | - |

## Run it

This skill is a program that walks you through the job one step at a time. You do not work from memory of this page: the program shows everything below again, at the right moment.

1. Find this skill's folder (the "Base directory" shown when the skill loaded; it contains `scripts/run.py`). If you are unsure: `find /mnt /root /home /opt /tmp -path '*client-pipeline-board/scripts/run.py' 2>/dev/null | head -1`
2. Choose a new run folder, for example `/tmp/wr-cpb-<Surname>-<DDMMYY>`, and start: `python3 <skill folder>/scripts/run.py start <run folder> --client "First Surname"`. The program's first lines give you one sentence to say to Paul before anything else: which version of this skill is running.
3. Do exactly what the step says. When it says you are done, run `python3 <skill folder>/scripts/run.py done <run folder> <step>`. The program checks the proof and only then shows the next step. It refuses to skip a step.
4. After a long chat or a compression, run `python3 <skill folder>/scripts/run.py status <run folder>`.
5. The last step prints the SHORT AUDIT. Your reply to Paul is that audit, as it is, plus one plain sentence.

Never rewrite, shorten or "improve" the programs during a run, and never type or edit the board, the page, the messages or the check-in yourself. If the self-test at the start fails, stop and tell Paul exactly what failed.

## What a finished run contains

- The **board**, one data file applied by the program to the old board (read back from the published page) and drawn as a read-out page: Prospect, Fact Find, General, one card per product line, Change Log. Published in the same reply, and the published page read back and compared.
- The **emails** this board builds itself (provider requests, the client document request, the LOA email, the Medical Aid and Will referrals): checked against the send table, saved as drafts or sent only after Paul's yes, read back from Outlook.
- The **messages to Sitamah** (Action needed, and one FYI), posted once through Zapier after his yes, and the same-day **check-in** for a follow-up appointment.
- The **short audit** (Paul, 03/11/2026): one line per check, each with a green tick or a red cross, one closing line for what is only attested. No long printout.

## Standing rules

1. Every point on the board comes from a registered document (a verbatim line the program can find) or Paul's own words; nothing is invented, and an Actions Taken line names its receipt.
2. Nothing is sent, posted or published without Paul's clear yes, in the same reply that shows it all with ONE question. Teams goes through Zapier only.
3. The send table decides: ask Paul first, or build automatically; where it lands; who sends; whether a fresh yes is needed. Not on the table: ask first.
4. A card is Identified, one pending question if something awaits Paul, and Actions Taken. No stage codes. The New Business / Servicing tag shows on Life Cover, RA and Investments only, and Paul gives it.
5. One client, one chat, one board. A correction re-opens the whole task and the earlier yes no longer counts.
6. Changes to this skill are made only in Claude Code and uploaded by Paul. Never say a change is live until he confirms.

## When something goes wrong

- The program refuses a step: read what it says is missing, fix that, run `done` again.
- The board cannot be read back, or its checksum is wrong: stop and tell Paul; never rebuild a board from memory.
- A document or an Outlook thread cannot be found: tell Paul exactly which routes were tried (computer, Microsoft 365, Zapier); never guess.
- A tool fails or returns something different from what was approved: show Paul the exact error; never send twice.
- A newer version of the published board exists that you cannot read: stop and tell Paul; never force-overwrite.

## Where the detail lives

The program prints the right page at the right step: `references/00-rules.md` (the rules), `01-locate.md` (the client, the board, the documents, the three routes), `02-change.md` (the change file and the card rules), `03-route.md` (the send table and the hand-overs), `04-send.md` (emails, the Sitamah messages, the check-in), `05-publish.md` (publishing), `06-handover.md` (the reply), and one `playbook-*.md` page per product line. `assets/` holds the data tables (contacts, send table, Sitamah messages, wording, settings). `steps.json` is the list of steps; `deliverables.json` is the list of outputs.
