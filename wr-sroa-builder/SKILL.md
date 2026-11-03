---
name: "wr-sroa-builder"
description: "Builds a Servicing Record of Advice (SROA) PDF for Paul Kafentzis (FSP45946) comparing a client's current policy schedule with the accepted servicing quote. A program serves the documents page by page, checks every figure against their text, works out 'No change' itself, draws the PDF with a fixed script, reads the result back to prove the checks and prints a short audit. Use when Paul asks for an SROA or servicing record."
---

# WR SROA Builder

## Index

| # | Section | What it covers |
|---|---|---|
| 1 | Run it | The one command that starts the job and how every step works |
| 2 | What a finished run contains | The saved SROA and the short audit |
| 3 | Standing rules | The rules that never bend, one line each |
| 4 | When something goes wrong | What to do instead of improvising |
| 5 | Where the detail lives | The pages the program shows at each step |

**Last updated: 2026-11-03 15:15 (Athens time)**

**Recent changes** (last 5, one line each; full history in the repo `history/` folder)

| When (Athens time) | What changed |
|---|---|
| 2026-11-03 15:15 | First program-driven version: documents served page by page, answers checked against their text, 'No change' computed, R20 label enforced, fixed script, the finished PDF read back, short audit |
| - | - |

## Run it

This skill is a program that walks you through the job one step at a time. You do not work from memory of this page: the program shows everything below again, at the right moment.

1. Find this skill's folder (the "Base directory" shown when the skill loaded; it contains `scripts/run.py`). If you are unsure: `find /mnt /root /home /opt /tmp -path '*wr-sroa-builder/scripts/run.py' 2>/dev/null | head -1`
2. Choose a new run folder, for example `/tmp/wr-sroa-<Surname>-<DDMMYY>`, and start: `python3 <skill folder>/scripts/run.py start <run folder> --client "First Surname" --policy "POLICY NUMBER"` (the client exactly as Paul named them; one run per policy; ask Paul which policy if the client has several). The program's first lines give you one sentence to say to Paul before anything else: which version of this skill is running.
3. Do exactly what the step says. When it says you are done, run `python3 <skill folder>/scripts/run.py done <run folder> <step>`. The program checks the proof and only then shows the next step. It refuses to skip a step.
4. After a long chat or a compression, run `python3 <skill folder>/scripts/run.py status <run folder>`.
5. The last step prints the SHORT AUDIT. Your reply to Paul is the saved file's name and folder, the PDF, and that audit, as they are.

Never rewrite, shorten or "improve" a program during a run, `build_sroa.py` included, and never type a figure from memory, a "No change", a file name or a date. If the self-test at the start fails, stop and tell Paul exactly what failed.

## What a finished run contains

- The **SROA (.pdf)**, one per policy, built by the fixed script from answers Paul confirmed; opened again by the program, which proves the pre-delivery checks it can; saved in the policy's `Servicing` folder (never overwriting without Paul's yes) and sent in the chat.
- The **short audit** (Paul, 03/11/2026): one line per check in point form, each with a green tick or a red cross, one closing line for what is only attested. No long printout.
- Nothing is sent to anyone. A run without a PASS audit is not finished: say so.

## Standing rules

1. An SROA is a FAIS compliance document for an EXISTING policy being changed; a wrong figure or an invented reason is a real compliance error. A new policy is wr-roa-builder.
2. Every figure, name, ID, CP number and date comes from the client's own documents or Paul's words, with its source; the program refuses what it cannot find in the right document's text. Never invent, never reuse another client's figures.
3. The reason for the change is Paul's own words; there is no default sentence. Portfolio Changes is a real narrative only for an investment-linked policy, otherwise the program writes N/A.
4. The premium line is always "Premium (incl. R20 policy fee)". ACI and ABI are always compared. The SROA date is the accepted quote's signed date confirmed with Paul, never today's.
5. A debt that may be renamed or new, or a source conflict: stop and ask Paul. One SROA per policy, never combined.
6. The script and the logo are fixed; never hand-patch the PDF; never overwrite a file without Paul's yes.
7. Changes to this skill are made only in Claude Code and uploaded by Paul. Never say a change is live until he confirms.

## When something goes wrong

- The program refuses a step or an answer: read what it says is missing or not found, fix that, run it again.
- A document cannot be found on any of the three routes: tell Paul exactly which were tried; never substitute the nearest document.
- A check shows a red cross: tell Paul exactly which line; fix the answers and rebuild; never hand-patch the PDF.
- The insurer is not BrightRock: the grouped headings are BrightRock's; use the flat list or ask Paul.

## Where the detail lives

The program prints the right page at the right step: `references/00-rules.md` (the rules), `01-locate.md` (the documents and the routes), `02-answers.md` (what to ask Paul and the answers file), `03-build-rules.md` (the four blocks, the fixed layout and the file name), `04-check-save.md` (the checks and the save), `05-handover.md` (the reply). `steps.json` is the list of steps; `deliverables.json` is the list of outputs.
