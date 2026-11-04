---
name: "complete-applications-skill"
description: "Fills in the real Old Mutual and General Short Risk application forms for a client, and corrects completed applications after a meeting, for Paul Kafentzis (FSP45946). A program fills the real blank forms from one plan file in which every value has a document line or Paul's words, reads back every field, proves each filled box shows something, builds the file and folder names and prints a short audit. Use when Paul asks to complete or correct applications for a named client."
---

# Complete Applications

## Index

| # | Section | What it covers |
|---|---|---|
| 1 | Run it | The one command that starts the job and how every step works |
| 2 | What a finished run contains | The filled forms, the saved folder, the short audit and the hand-back |
| 3 | Standing rules | The rules that never bend, one line each |
| 4 | When something goes wrong | What to do instead of improvising |
| 5 | Where the detail lives | The pages the program shows at each step |

**Last updated: 2026-11-04 14:56 (Athens time)**

**Recent changes** (last 5, one line each; full history in the repo `history/` folder)

| When (Athens time) | What changed |
|---|---|
| 2026-11-04 14:56 | First program-driven version: the real forms are filled by program from one plan file with a source for every value, every field is read back, each filled box is proved to draw, and a checker rebuilds everything and compares |
| - | - |

## Run it

This skill is a program that walks you through the job one step at a time. You do not work from memory of this page: the program shows everything below again, at the right moment.

1. Find this skill's folder (the "Base directory" shown when the skill loaded; it contains `scripts/run.py`). If you are unsure: `find /mnt /root /home /opt /tmp -path '*complete-applications-skill/scripts/run.py' 2>/dev/null | head -1`
2. Choose a new run folder, for example `/tmp/wr-ca-<Surname>-<DDMMYY>`, and start: `python3 <skill folder>/scripts/run.py start <run folder> --client "First Surname" --mode prefill` (new applications before a meeting) or `--mode correct` (after a meeting). The program's first lines give you one sentence to say to Paul before anything else: which version of this skill is running.
3. Do exactly what the step says. When it says you are done, run `python3 <skill folder>/scripts/run.py done <run folder> <step>`. The program checks the proof and only then shows the next step. It refuses to skip a step.
4. After a long chat or a compression, run `python3 <skill folder>/scripts/run.py status <run folder>`.
5. The last step prints the SHORT AUDIT and the hand-back. Your reply to Paul is those, as they are, plus one plain sentence.

Never rewrite, shorten or "improve" the programs during a run, and never type or edit a PDF yourself. If the self-test at the start fails (a missing module, or a blank form that has changed), stop and tell Paul exactly what failed. These forms hold the most sensitive client data: it stays in the run folder, never in a repo.

## What a finished run contains

- One **filled real form per application** (the Old Mutual form or the General Short Risk form), made by the program from your plan and the real blank form, every field read back and every filled box shown to draw something. A correction changes only the planned fields of the existing file, in place.
- The files **sent in the chat and saved** in the client's `Applications` folder after Paul's one yes, the transaction folder renamed only when planned and approved, each checked in a saved listing.
- The **short audit** (Paul, 03/11/2026): one line per check, each with a green tick or a red cross, one closing line for what is only attested, and one short **hand-back** block per application (what was filled or changed, what is still blank, flags, ID and account numbers masked to the last 4).

## Standing rules

1. Every value comes from a verbatim line of a registered document or Paul's own words. Nothing is invented: what is not in the file is left blank and listed.
2. Nothing is filled, saved, renamed or overwritten without Paul's clear yes for exactly the table he was shown. Nothing is ever deleted. A form Paul completed live is never overwritten without a fresh yes.
3. The real insurer or firm form is filled, never a lookalike; the program refuses a form that has changed.
4. Replacement is a real answer with the replaced policy numbers checked against the schedule; every N/A field that does not apply says N/A; the signature date is the meeting date, never blank; the client's signature is never written.
5. A correction changes ONLY the planned fields, carries a detail only from a CURRENT application in a CURRENT folder, and stops when two current applications disagree.
6. Changes to this skill are made only in Claude Code and uploaded by Paul. Never say a change is live until he confirms.

## When something goes wrong

- The program refuses a step: read what it says is missing, fix that, run `done` again.
- A blank form or a current application is not the form this skill knows: stop and tell Paul; never fill an unknown form.
- A folder, document or listing cannot be found: tell Paul exactly which routes were tried (computer, Microsoft 365, Zapier); never guess a folder.
- A dropdown value does not draw in the render: say so plainly, do not claim the render passed, and ask Paul to look in his own viewer.
- The destination file is open elsewhere: tell Paul and ask him to close it; never force it or rename around it.

## Where the detail lives

The program prints the right page at the right step: `references/00-rules.md` (the rules), `01-locate.md` (the folders, the routes, the documents), `02-plan.md` (the plan file and the rules on every field), `03-confirm.md` (the table and the yes), `04-fill.md` (filling and the checks), `05-save.md` (saving, the folder and file names, a correction's save), `06-handover.md` (the reply), and `field-mappings.md` (every field of both forms). `assets/` holds the two real blank forms, their frozen field lists and the settings. `steps.json` is the list of steps; `deliverables.json` is the list of outputs.
