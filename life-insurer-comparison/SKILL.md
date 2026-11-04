---
name: "life-insurer-comparison"
description: "Builds a client-facing HTML comparison letter of two or more insurers' life/risk policies (e.g. BrightRock vs Discovery) plus a covering email, for Paul (FSP45946), then saves it, drafts the email in Outlook and alerts Sitamah. A program serves the documents page by page, proves the benefit scope from the client's own notes, checks every figure against the documents, works out the premium escalation, draws the letter from a fixed template and prints a short audit. Use when asked to compare existing cover with a proposal."
---

# Life Insurer Comparison Builder

## Index

| # | Section | What it covers |
|---|---|---|
| 1 | Run it | The one command that starts the job and how every step works |
| 2 | What a finished run contains | The letter, the saved copy, the draft, the Teams message and the short audit |
| 3 | Standing rules | The rules that never bend, one line each |
| 4 | When something goes wrong | What to do instead of improvising |
| 5 | Where the detail lives | The pages the program shows at each step |

**Last updated: 2026-11-04 11:27 (Athens time)**

**Recent changes** (last 5, one line each; full history in the repo `history/` folder)

| When (Athens time) | What changed |
|---|---|
| 2026-11-04 11:27 | First program-driven version: documents served page by page and the benefit scope proved from the client's own notes, every figure checked against the line of the document it cites, the premium escalation worked out by the program, the letter drawn from a fixed template, draft and Teams read-backs checked, short audit |
| 2026-11-04 11:18 | First program-driven version: documents served page by page and the benefit scope proved from the client's own notes, every figure checked against the line of the document it cites, the premium escalation worked out by the program, the letter drawn from a fixed template, draft and Teams read-backs checked, short audit |
| 2026-11-04 00:00 | First program-driven version: documents served page by page and the benefit scope proved from the client's own notes, every figure checked against the line of the document it cites, the premium escalation worked out by the program, the letter drawn from a fixed template, draft and Teams read-backs checked, short audit |
| - | - |

## Run it

This skill is a program that walks you through the job one step at a time. You do not work from memory of this page: the program shows everything below again, at the right moment.

1. Find this skill's folder (the "Base directory" shown when the skill loaded; it contains `scripts/run.py`). If you are unsure: `find /mnt /root /home /opt /tmp -path '*life-insurer-comparison/scripts/run.py' 2>/dev/null | head -1`
2. Choose a new run folder, for example `/tmp/lic-<Surname>-<DDMMYY>`, and start: `python3 <skill folder>/scripts/run.py start <run folder> --client "First Surname"` (the client exactly as Paul named them). The program's first lines give you one sentence to say to Paul before anything else: which version of this skill is running.
3. Do exactly what the step says. When it says you are done, run `python3 <skill folder>/scripts/run.py done <run folder> <step>`. The program checks the proof and only then shows the next step. It refuses to skip a step.
4. After a long chat or a compression, run `python3 <skill folder>/scripts/run.py status <run folder>`.
5. The last step prints the SHORT AUDIT. Your reply to Paul is where the letter was saved, the draft's status and who attaches the letter, that Sitamah was messaged, the flags, and that audit, as they are.

Never rewrite, shorten or "improve" a program or the template during a run, and never type a figure from memory, a total, a percentage, a file name or the Teams message. If the self-test at the start fails, stop and tell Paul exactly what failed.

## What a finished run contains

- The **comparison letter (.html)**, one standalone file drawn from the fixed template from answers Paul confirmed: sent to Paul in the chat and saved in the client's `Comparative Quotes` (never overwriting without Paul's yes).
- The **Outlook draft** with the covering email (made with the Microsoft 365 draft tool, never sent by Claude; Paul attaches the letter by hand and the Exchange rule adds his signature once), read back and checked by the program, and the **Teams message to Sitamah** (through Zapier, after Paul's one yes and a checked draft), read back and checked.
- The **short audit** (Paul, 03/11/2026): one line per check in point form, each with a green tick or a red cross, one closing line for what is only attested. A run without a PASS audit is not finished: say so.

## Standing rules

1. Every figure comes from a line of the client's own quote or schedule, every product statement from a line of the insurer's own guide saved for this comparison, or it is shown to the client as "to be confirmed". Never invent, never reuse another client's figures or wording.
2. The benefit scope comes from the client's own notes, never from what appears on a quote. A category outside the scope appears nowhere in the letter or the email, in any form.
3. Fixed or age-rated is decided by the document's own words, never by the size of the percentage. The program works out every year-on-year percentage from the printed rand figures and flags the odd ones.
4. Nothing is sent without Paul's yes: his one yes at the confirmation table covers the draft and the message to Sitamah, which goes only after the draft is checked. The Cc is always Sitamah Nathoo. Claude never sends the client email.
5. The letter speaks in Paul's own first person unless he says otherwise, and addresses the client as "you". No adviser-facing commentary and no quote-version history reaches the client.
6. The template and the scripts are fixed; never hand-patch the HTML; never overwrite a file without Paul's yes.
7. Changes to this skill are made only in Claude Code and uploaded by Paul. Never say a change is live until he confirms.

## When something goes wrong

- The program refuses a step or an answer: read what it says is missing or not found, fix that, run it again.
- A document cannot be found on any route: tell Paul exactly which were tried; never substitute the nearest document. An insurer's guide that cannot be found: ask Paul and record his words; never guess a feature.
- The notes are silent or conflict on a benefit category: ask Paul and record his words; never pick the more generous reading.
- A check shows a red cross: tell Paul exactly which line; fix the answers or the draft and run the check again; never hand-patch the HTML.
- The draft or the posted message does not read back right: do not message Sitamah (draft) or tell Paul exactly which line (message).

## Where the detail lives

The program prints the right page at the right step: `references/00-rules.md` (the rules), `01-locate.md` (the documents and the routes), `02-scope.md` (the scope, second life, basis, voice and sections), `03-research.md` and `09-insurer-hints.md` (the insurers' guides), `04-answers.md` (the answers file and what to extract), `05-check.md` (the escalation check and the flags), `06-build.md` (the letter), `07-draft-and-message.md` (the covering email and the Teams message), `08-handover.md` (the reply). `steps.json` is the list of steps; `deliverables.json` is the list of outputs; `assets/settings.json` (who attaches the letter, Paul's closing details, the word limits), `assets/wording.json` (the fixed sentences) and `assets/scope_terms.json` (the scope word lists) hold the things Paul may change later.
