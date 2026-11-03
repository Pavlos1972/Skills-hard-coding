---
name: "wr-roa-builder"
description: "Builds a Record and Confirmation of Advice (ROA) for Paul Kafentzis (FSP45946) from the ROA Template 2026, taking the answers from the client's file. A program serves the documents page by page, checks every figure against their text, picks the reason text from the bank, builds the .docx with fixed scripts (embedding the client's reply email for Retirement and Investment), opens the result to prove the checks and prints a short audit. Use when Paul asks for an ROA or Record of Advice."
---

# WR ROA Builder

## Index

| # | Section | What it covers |
|---|---|---|
| 1 | Run it | The one command that starts the job and how every step works |
| 2 | What a finished run contains | The saved ROA and the short audit |
| 3 | Standing rules | The rules that never bend, one line each |
| 4 | When something goes wrong | What to do instead of improvising |
| 5 | Where the detail lives | The pages the program shows at each step |

**Last updated: 2026-11-03 14:37 (Athens time)**

**Recent changes** (last 5, one line each; full history in the repo `history/` folder)

| When (Athens time) | What changed |
|---|---|
| 2026-11-03 14:37 | Removed an ID-number example from a script comment; added a contents line to the dropdown map |
| 2026-11-03 14:36 | The bundle is chosen when a run starts; the audit lists the .docx checks on one line |
| 2026-11-03 14:30 | First program-driven version: documents served page by page, answers checked against their text, reason text picked from the bank, fixed scripts, the finished ROA opened and checked, email embedding forced and checked |
| - | - |

## Run it

This skill is a program that walks you through the job one step at a time. You do not work from memory of this page: the program shows everything below again, at the right moment.

1. Find this skill's folder (the "Base directory" shown when the skill loaded; it contains `scripts/run.py`). If you are unsure: `find /mnt /root /home /opt /tmp -path '*wr-roa-builder/scripts/run.py' 2>/dev/null | head -1`
2. Choose a new run folder, for example `/tmp/wr-roa-<Surname>-<DDMMYY>`, and start: `python3 <skill folder>/scripts/run.py start <run folder> --client "First Surname" --bundle risk|retirement|investment` (the client exactly as Paul named them; ask Paul which bundle if the file does not say). The program's first lines give you one sentence to say to Paul before anything else: which version of this skill is running.
3. Do exactly what the step says. When it says you are done, run `python3 <skill folder>/scripts/run.py done <run folder> <step>`. The program checks the proof and only then shows the next step. It refuses to skip a step.
4. After a long chat or a compression, run `python3 <skill folder>/scripts/run.py status <run folder>`.
5. The last step prints the SHORT AUDIT. Your reply to Paul is the saved file's name and folder, the .docx, and that audit, as they are.

Never rewrite, shorten or "improve" a program during a run, the two scripts `build_roa.py` and `embed_email_images.py` included, and never type a reason text, a reference number, a file name or a date. If the self-test at the start fails, stop and tell Paul exactly what failed.

## What a finished run contains

- The **ROA (.docx)**, built from the template by the fixed scripts from answers Paul confirmed, with the client's own reply email embedded for a Retirement or Investment ROA; opened again by the program, which proves the pre-delivery checks it can; saved in the client's `ROA & Bus ROA` folder (never overwriting without Paul's yes) and sent in the chat.
- The **short audit** (Paul, 03/11/2026): one line per check in point form, each with a green tick or a red cross, one closing line for what is only attested. No long printout.
- Nothing is sent to anyone. A run without a PASS audit is not finished: say so.

## Standing rules

1. A ROA is a compliance document: one bundle only (Risk, Retirement or Investment), a single client, never Health Care.
2. Every answer and figure comes from the client's own documents or Paul's words, with its source; the program refuses what it cannot find in the documents' text. Never invent, never reuse another client's figures.
3. The ROA date is the date the client gave the go-ahead. Two sources that disagree: stop and ask Paul.
4. Reason text is a bank paragraph word for word, a fixed sentence, the reason Paul gave, or the pointer line; anything else is Paul's custom wording and is marked.
5. The template, the bank and the two scripts are fixed; never hand-patch the .docx, never build an ROA as HTML, never overwrite a file without Paul's yes.
6. Retirement and Investment: the embedded email must open on the client's own reply.
7. Changes to this skill are made only in Claude Code and uploaded by Paul. Never say a change is live until he confirms.

## When something goes wrong

- The program refuses a step or an answer: read what it says is missing or not found, fix that, run it again.
- A document cannot be found on any of the three routes: tell Paul exactly which were tried; never substitute the nearest document.
- A Retirement or Investment ROA needs `wkhtmltopdf` and the program says it is missing: stop and tell Paul; never render the email with anything else.
- A check shows a red cross: tell Paul exactly which line; fix the answers and rebuild; never hand-patch the .docx.
- The quote is not from BrightRock: tell Paul before going on.

## Where the detail lives

The program prints the right page at the right step: `references/00-rules.md` (the rules), `01-locate.md` (the documents and the routes), `02-answers.md` (how to derive the answers and the answers file), `03-template-rules.md` (the template's fixed rules, the reference number and the file name), `04-email.md` (the Retirement and Investment email), `05-check-save.md` (the checks and the save), `06-handover.md` (the reply); `dropdown_field_map.md` lists every dropdown option. `steps.json` is the list of steps; `deliverables.json` is the list of outputs.
