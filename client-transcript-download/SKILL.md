---
name: "client-transcript-download"
description: "Downloads a client's Teams meeting transcript (Microsoft 365 connector first, then Zapier, then Claude in Chrome) and saves a copy into the client's 2. Fact Find folder, finding and saving everything by itself with no permission step. A program drives the steps, checks the transcript is complete and prints a short audit with green ticks and red crosses. Use after a client meeting or when Paul asks to save a transcript."
---

# Client Transcript download

## Index

| # | Section | What it covers |
|---|---|---|
| 1 | Run it | The one command that starts the job and how every step works |
| 2 | What a finished run contains | The saved file and the short audit that ends the job |
| 3 | Standing rules | The rules that never bend, one line each |
| 4 | When something goes wrong | What to do instead of improvising |
| 5 | Where the detail lives | The pages the program shows at each step |

**Last updated: 2026-11-05 12:36 (Athens time)**

**Recent changes** (last 5, one line each; full history in the repo `history/` folder)

| When (Athens time) | What changed |
|---|---|
| 2026-11-05 12:36 | Strict changes: files found and saved automatically through Microsoft 365, the computer only if already connected, no permission step, quiet run, size check |
| 2026-11-03 11:25 | Added the rule that a correction re-opens the task, the rule-by-rule records and the list for Paul |
| 2026-11-03 11:24 | First program-driven version: a program fetches (Microsoft 365, Zapier, Chrome), checks the transcript is complete and saves a copy under a derived name; a checker prints a short audit with green ticks and red crosses |
| - | - |

## Run it

This skill is a program that walks you through the job one step at a time. You do not work from memory of this page: the program shows everything below again, at the right moment.

1. Find this skill's folder (the "Base directory" shown when the skill loaded; it contains `scripts/run.py`). If you are unsure: `find /mnt /root /home /opt /tmp -path '*client-transcript-download/scripts/run.py' 2>/dev/null | head -1`
2. Choose a new run folder, for example `/tmp/wr-td-<Surname>-<DDMMYY>`, and start: `python3 <skill folder>/scripts/run.py start <run folder> --client "First Surname" --date DD/MM/YYYY` (add `--type first` for a first Fact Find meeting or `--type follow-up` when Paul says which it was). The client and the meeting date are taken exactly from Paul's message. The program's first lines give you one sentence to say to Paul before anything else: which version of this skill is running. Then work quietly: one short progress line per step at most, no opening recap.
3. Do exactly what the step says. When it says you are done, run `python3 <skill folder>/scripts/run.py done <run folder> <step>`. The program checks the proof and only then shows the next step. It refuses to skip a step.
4. After a long chat or a compression, run `python3 <skill folder>/scripts/run.py status <run folder>`.
5. The last step prints the SHORT AUDIT. Your reply to Paul is that audit, as it is, plus one plain sentence.

Never rewrite, shorten or "improve" the programs during a run, and never type the file name. If the self-test at the start fails, stop and tell Paul exactly what failed.

## What a finished run contains

- The **transcript** as `Teams meeting transcript - DD.MM.YY - (First Surname).docx`, built by the program, copied (never moved, never overwritten) into the client's `2. Fact Find` folder and listed back (the listed size must equal the local file's).
- The **short audit** (Paul, 03/11/2026): one line per check in point form, each with a green tick or a red cross, one line for what is only attested, one line for the next skill. No long printout.
- Nothing is deleted and nothing is sent. A run without a PASS audit is not finished: say so.

## Standing rules

1. Save only what Teams gave you; never edit, summarise or complete a transcript.
2. Fetch through the Microsoft 365 connector first, then Zapier, then Claude in Chrome; save through the computer only if this chat is already connected to it, then Microsoft 365, then Zapier; every try logged, all found automatically.
3. Teams is for reading the recap and transcript only: do not post, delete, change settings or open other chats.
4. The transcript is copied into the client folder, never moved and never overwritten; the original stays where it is.
5. A transcript is complete only when its last time stamp is within 2 minutes of the meeting length and no gap between two time stamps is longer than 10 minutes.
6. Never touch another broker's folder.
7. Changes to this skill are made only in Claude Code and uploaded by Paul. Never say a change is live until he confirms.
8. Never a permission step: no permission box, no folder-access request, never ask Paul to click, attach, upload or drag a file, and never call a tool that opens such a box.
9. A quiet run: the version sentence, one short progress line per step, then the SHORT AUDIT and one plain sentence. Never a long opening message or an analysis of what was read.

## When something goes wrong

- The program refuses a step: read what it says is missing, fix that, run `done` again.
- A route fails: record the exact error as a failed try and go to the next route at once; stop after 2 or 3 attempts on a route. If every route fails, your reply is at most five lines: what failed and the log of the tries.
- The check shows a red cross (cut-off transcript, wrong date): tell Paul exactly what it says; never save an incomplete transcript as complete.
- No transcript exists (transcription was not started): say exactly that.

## Where the detail lives

The program prints the right page at the right step: `references/00-rules.md` (the rules), `01-fetch-routes.md` (the three routes, with the Chrome route in detail), `02-save.md` (the client's folder and how to save without overwriting), `03-handover.md` (the reply). `steps.json` is the list of steps; `deliverables.json` is the list of outputs.
