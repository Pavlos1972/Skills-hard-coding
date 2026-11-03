---
name: "rgar-skill"
description: "Builds the client proposal email for an RGAR from Alwyn for Paul Kafentzis (FSP45946), saves it, drafts it in Outlook and alerts Sitamah. A program serves the RGAR and the Fact Find Summary page by page, checks every figure against their text, works out the age check and the shortfall dates, fills the fixed template, checks the draft and the Teams message read-backs and prints a short audit. Use when Paul asks for an RGAR proposal or Retirement Goal Analysis email."
---

# RGAR Proposal Email Builder

## Index

| # | Section | What it covers |
|---|---|---|
| 1 | Run it | The one command that starts the job and how every step works |
| 2 | What a finished run contains | The email, the saved copy, the RGAR copy, the draft, the Teams message and the short audit |
| 3 | Standing rules | The rules that never bend, one line each |
| 4 | When something goes wrong | What to do instead of improvising |
| 5 | Where the detail lives | The pages the program shows at each step |

**Last updated: 2026-11-03 17:27 (Athens time)**

**Recent changes** (last 5, one line each; full history in the repo `history/` folder)

| When (Athens time) | What changed |
|---|---|
| 2026-11-03 17:27 | First program-driven version: documents served page by page, answers checked against their text, age and net target checked, shortfall dates computed, fixed template filled by program, draft and Teams message read-backs checked, short audit |
| - | - |

## Run it

This skill is a program that walks you through the job one step at a time. You do not work from memory of this page: the program shows everything below again, at the right moment.

1. Find this skill's folder (the "Base directory" shown when the skill loaded; it contains `scripts/run.py`). If you are unsure: `find /mnt /root /home /opt /tmp -path '*rgar-skill/scripts/run.py' 2>/dev/null | head -1`
2. Choose a new run folder, for example `/tmp/rgar-<Surname>-<DDMMYY>`, and start: `python3 <skill folder>/scripts/run.py start <run folder> --client "First Surname"` (the client exactly as Paul named them). The program's first lines give you one sentence to say to Paul before anything else: which version of this skill is running.
3. Do exactly what the step says. When it says you are done, run `python3 <skill folder>/scripts/run.py done <run folder> <step>`. The program checks the proof and only then shows the next step. It refuses to skip a step.
4. After a long chat or a compression, run `python3 <skill folder>/scripts/run.py status <run folder>`.
5. The last step prints the SHORT AUDIT. Your reply to Paul is where the copy was saved, the draft's status, that Sitamah was messaged, the flags, and that audit, as they are.

Never rewrite, shorten or "improve" a program or the template during a run, and never type a figure from memory, a weekday, a shortfall date, a file name or the Teams message. If the self-test at the start fails, stop and tell Paul exactly what failed.

## What a finished run contains

- The **proposal email (.html)** built from the fixed template by the program from answers Paul confirmed: the full copy sent to Paul in the chat, the no-logo copy saved in the RA transaction folder's `Comparative Quotes` together with a copy of the RGAR PDF (never overwriting without Paul's yes).
- The **Outlook draft** (never sent by Claude), read back and checked by the program, and the **Teams message to Sitamah** (through Zapier, after Paul's one yes and a checked draft), read back and checked. Sitamah attaches the RGAR report and emails the client.
- The **short audit** (Paul, 03/11/2026): one line per check in point form, each with a green tick or a red cross, one closing line for what is only attested. No long printout. A run without a PASS audit is not finished: say so.

## Standing rules

1. Every figure, name, date and address comes from the client's own RGAR and Fact Find Summary or Paul's words, with its source; the program refuses what it cannot find in the right document's text. Never invent, never reuse another client's figures.
2. The net monthly target is the figure after its label in the Fact Find Summary, never the Reduced Quote's contribution target and never a gross figure with an assumed tax rate. With no Fact Find Summary the skill stops and asks Paul.
3. The age must agree with the RGAR's date of birth; a lump sum or monthly amount of R 0, or two sources that disagree: stop and ask Paul. No wording is invented.
4. Weekdays and the shortfall dates are computed by the program, never typed. The Cc is always Sitamah Nathoo. Claude never sends the client email: Sitamah sends it from Drafts.
5. Nothing is sent without Paul's yes: his one yes at the confirmation table covers the draft and the message to Sitamah, which goes only after the draft is checked.
6. The template and the scripts are fixed; never hand-patch the HTML; never overwrite a file without Paul's yes.
7. Changes to this skill are made only in Claude Code and uploaded by Paul. Never say a change is live until he confirms.

## When something goes wrong

- The program refuses a step or an answer: read what it says is missing or not found, fix that, run it again.
- A document cannot be found on any of the three routes: tell Paul exactly which were tried; never substitute the nearest document and never read the raw Fact Find instead of the Fact Find Summary.
- A check shows a red cross: tell Paul exactly which line; fix the answers or the draft and run the check again; never hand-patch the HTML.
- The draft or the posted message does not read back right: do not message Sitamah (draft) or tell Paul exactly which line (message).

## Where the detail lives

The program prints the right page at the right step: `references/00-rules.md` (the rules), `01-locate.md` (the documents and the routes), `02-answers.md` (what comes from the RGAR and the Fact Find Summary, what Paul is asked, the answers file), `03-build-rules.md` (the template's fixed rules, the files and the save), `04-draft.md` (the Outlook draft with Claude in Chrome), `05-message.md` (the Teams message through Zapier), `06-handover.md` (the reply). `steps.json` is the list of steps; `deliverables.json` is the list of outputs; `assets/settings.json` and `assets/net_target_labels.json` hold the two things Paul may change later.
