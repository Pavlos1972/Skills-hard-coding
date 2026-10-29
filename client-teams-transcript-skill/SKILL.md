---
name: "client-teams-transcript-skill"
description: "Summarize a client's Teams meeting transcript (or WhatsApp call) in the context of all earlier meetings, quotes and applications, organised by Paul's planning areas, into a Planner short note and a Follow-Up Appointment Summary Notes PDF saved to the client's folder."
---

# Client Teams Transcript Skill

## Index

| # | Section | What it covers |
|---|---|---|
| 1 | Run it | The one command that starts the job and how every step works |
| 2 | What a finished run contains | The deliverables and the proof that ends the job |
| 3 | Standing rules | The rules that never bend, one line each |
| 4 | When something goes wrong | What to do instead of improvising |
| 5 | Where the detail lives | The pages the program shows at each step |

**Last updated: 2026-10-29 17:53 (Athens time)**

**Recent changes** (last 5, one line each; full history in the repo `history/` folder)

| When (Athens time) | What changed |
|---|---|
| 2026-10-29 17:53 | Action points are put in order (earliest deadline first, then logical), what is not relevant is left out and listed, and the skill asks Paul in one message when it is not sure |
| 2026-10-29 17:22 | Dated notes taken out of the live pages (the dates stay in the history files) |
| 2026-10-29 17:21 | Planner note is now short (one-liners and actions for now), PDF limited to 4 bullets per area and two pages, actions sorted now/later, message to Sitamah shown with the outputs (Paul's answers after his first real-case trial) |
| 2026-10-29 13:38 | Every run now begins by saying which version it is (read from this stamp), the final checklist repeats it, and the date can only move when the skill's files really change |
| 2026-10-29 13:18 | The message to Sitamah is now also built, checked and sent for WhatsApp calls ("WhatsApp Call Completed"), as Paul decided |

## Run it

This skill is a program that walks you through the job one step at a time. You do not work from memory of this page. Everything below is shown again, at the right moment, by the program.

1. Find this skill's folder (the "Base directory" shown when the skill loaded; it contains `scripts/run.py`). If you are unsure: `find /mnt /root /home /opt /tmp -path '*client-teams-transcript-skill/scripts/run.py' 2>/dev/null | head -1`
2. Choose a new run folder, for example `/tmp/wr-run-<Surname>-<DDMMYY>`, and start: `python3 <skill folder>/scripts/run.py start <run folder> --type followup --client "First Surname" --date DD/MM/YYYY` (use `first` for a Fact Find / first appointment, `whatsapp` for a WhatsApp call). The client and the meeting date are taken exactly from Paul's message; the program checks every later file against them. The program's first lines give you one sentence to say to Paul before anything else: which version of this skill is running. It comes from the Last updated line above, so it moves with every update.
3. Do exactly what the step says. When it says you are done, run `python3 <skill folder>/scripts/run.py done <run folder> <step>`. The program checks the proof and only then shows the next step. It refuses to skip a step.
4. After a long chat or a compression, run `python3 <skill folder>/scripts/run.py status <run folder>`. It tells you where the job is up to.
5. The last step prints a PASS/FAIL checklist, including a short list of what Paul should glance at. Your reply to Paul must contain that printout, unedited.

Never rewrite, shorten or "improve" the programs during a run, and never replace an output with a text draft. If the self-test at the start fails, stop and tell Paul exactly what failed.

## What a finished run contains

- The **Planner note** as a copy-ready page with a Copy note button (every meeting type): short, one-line bullets per area and only the actions for now.
- The **PDF**: Follow-Up Appointment Summary Notes, or WhatsApp Call Summary, two pages at most. Sent in the chat, saved into the client's `2. Fact Find` folder, and listed back. Not for a first/Fact Find meeting.
- The **message to Sitamah** in Teams ("Teams Appointment Completed" or, for a WhatsApp call, "WhatsApp Call Completed"), shown to Paul in the same reply as the page and the PDF (one question, one yes for all three) and sent through Zapier only after his yes.
- The final printout saying `RESULT: PASS`. No PASS in your reply means the job is not finished: say so.

## Standing rules

1. Source first, never invent: every fact and every action traces to the transcript or a named document, and the program checks the quote.
2. Read the whole transcript twice, in order, before anything is drafted. The program enforces it.
3. Client information comes from the client's file first; use the access routes in order (local drive, Microsoft 365, Zapier) and log each try. Ask Paul only after all three failed.
4. Every action point is for Sitamah. Paul is never the owner of an action.
5. Nothing is sent for Paul without his yes: emails and Teams messages are drafts until he approves.
6. Never write ID, account or tax numbers.
7. After any correction from Paul, re-open the whole task: fix it in `content.json`, rebuild, redo the hand-over of every output that changed, run the final check again.
8. If a rule cannot be met, stop and say exactly which one and why. Never hand over partial work as complete.
9. Changes to this skill are made only in Claude Code and uploaded by Paul. Never say a change is live until he confirms it.
10. Short means short: the Planner note is one-line bullets and the actions for now, the PDF is two pages at most, and every action is sorted now or later and put in order (earliest deadline first, then logical). Leave out what is not relevant and list it; when you are not sure, ask Paul in one message. The program fails anything longer, unsorted or unanswered.

## When something goes wrong

- The program refuses a step: read what it says is missing, fix that, run `done` again.
- A tool is unavailable (for example the page tool): say so, use the fallback the step names, and record that it was a fallback.
- Paul corrects something: rule 7 above.
- You cannot reach a file: follow rule 3 and use `run.py ask`, which gives you the exact words for Paul.

## Where the detail lives

The program prints the right page at the right step, so you do not need to open them yourself: `references/00-rules.md` (standing rules and deliverables), `01` access and locating, `02` the two-read lock, `03` the client's file and correspondence, `04` areas, quotes, credit life, cession and carry-forward, `05` accuracy, `06a` the Planner note, `06b` the PDF and file names, `06c` hand-offs, `07` the Teams message. `steps.json` is the list of steps; `deliverables.json` is the list of outputs.
