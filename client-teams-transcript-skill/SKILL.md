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

**Last updated: 2026-11-06 09:20 (Athens time)**

**Recent changes** (last 5, one line each; full history in the repo `history/` folder)

| When (Athens time) | What changed |
|---|---|
| 2026-11-06 09:20 | Computer through the device tools: the chat connects once at step 1 (one STOP line if refused); the transcript and every client document are whole copies proved by the computer's own fingerprint, the program makes their text; Microsoft 365 and Zapier only for emails and the Teams transcript text; the PDF is saved on the computer and fingerprinted there |
| 2026-11-05 11:37 | Strict changes after the first real run: files found automatically through Microsoft 365 (no permission step), the Sitamah message posted automatically, a quiet run, the short audit as the program's own printout |
| 2026-11-02 15:55 | The follow-up appointment is now an action for Sitamah at every meeting where one was agreed (the program no longer refuses it and fails an agreed appointment with no such action); the first-meeting message to Sitamah is made by this skill only (Paul, 02/11/2026) |
| 2026-10-29 17:53 | Action points are put in order (earliest deadline first, then logical), what is not relevant is left out and listed, and the skill asks Paul in one message when it is not sure |
| 2026-10-29 17:22 | Dated notes taken out of the live pages (the dates stay in the history files) |

## Run it

This skill is a program that walks you through the job one step at a time. You do not work from memory of this page. Everything below is shown again, at the right moment, by the program.

**A quiet run, and nothing is asked of Paul (Paul's rule).** Start your reply with the one version sentence the program gives you, then work. You may show ONE short progress line per step (for example "Step 4 of 14: reading the transcript, first pass"). Never write an opening recap of this skill, its rules, the files found or the information read; do not read the reference pages yourself (the program shows each page at its step). Never ask Paul for permission, to attach, upload or drag a file, or to say "go": connect to his computer yourself at step 1 (the one connection request is the only click he is ever asked for) and take the files from it. The reply at the end is the outputs, the message that was posted and the SHORT audit.

1. Find this skill's folder (the "Base directory" shown when the skill loaded; it contains `scripts/run.py`). If you are unsure: `find /mnt /root /home /opt /tmp -path '*client-teams-transcript-skill/scripts/run.py' 2>/dev/null | head -1`
2. Choose a new run folder, for example `/tmp/wr-run-<Surname>-<DDMMYY>`, and start: `python3 <skill folder>/scripts/run.py start <run folder> --type followup --client "First Surname" --date DD/MM/YYYY` (use `first` for a Fact Find / first appointment, `whatsapp` for a WhatsApp call). The client and the meeting date are taken exactly from Paul's message; the program checks every later file against them. The program's first lines give you one sentence to say to Paul before anything else: which version of this skill is running. It comes from the Last updated line above, so it moves with every update.
3. Do exactly what the step says. When it says you are done, run `python3 <skill folder>/scripts/run.py done <run folder> <step>`. The program checks the proof and only then shows the next step. It refuses to skip a step.
4. After a long chat or a compression, run `python3 <skill folder>/scripts/run.py status <run folder>`. It tells you where the job is up to.
5. The last step prints a PASS/FAIL checklist, including a short list of what Paul should glance at. Your reply to Paul must contain that printout, unedited.

Never rewrite, shorten or "improve" the programs during a run, and never replace an output with a text draft. If the self-test at the start fails, stop and tell Paul exactly what failed.

## What a finished run contains

- The **Planner note** as a copy-ready page with a Copy note button (every meeting type): short, one-line bullets per area and only the actions for now.
- The **PDF**: Follow-Up Appointment Summary Notes, or WhatsApp Call Summary, two pages at most. Sent in the chat, saved on the computer into the client's `2. Fact Find` folder, and fingerprinted there (the program compares it with the PDF it built). Not for a first/Fact Find meeting.
- The **message to Sitamah** in Teams ("Teams Appointment Completed" or, for a WhatsApp call, "WhatsApp Call Completed"), POSTED AUTOMATICALLY through Zapier (Paul's standing instruction: no question) and shown in the same reply as the page and the PDF.
- The short audit saying `RESULT: PASS`. No PASS in your reply means the job is not finished: say so.

## Standing rules

1. Source first, never invent: every fact and every action traces to the transcript or a named document, and the program checks the quote.
2. Read the whole transcript twice, in order, before anything is drafted. The program enforces it.
3. Client information comes from the client's file first, taken from Paul's computer (connected once at step 1; every file proved identical by the computer's own fingerprint; the finished PDF is saved there too). Microsoft 365 and Zapier are for emails and the Teams transcript only, never for a PDF or a Word file. Log each try. If the computer cannot be connected, the program prints one STOP line and that is the whole reply. Never ask Paul to attach, upload or drag a file.
4. Every action point is for Sitamah. Paul is never the owner of an action.
5. Emails and invites are drafts until Paul says yes. The one exception is the message to Sitamah in Teams, which Paul made automatic: posted through Zapier, once per meeting.
6. Never write ID, account or tax numbers.
7. After any correction from Paul, re-open the whole task: fix it in `content.json`, rebuild, redo the hand-over of every output that changed, run the final check again.
8. If a rule cannot be met, stop and say exactly which one and why. Never hand over partial work as complete.
9. Changes to this skill are made only in Claude Code and uploaded by Paul. Never say a change is live until he confirms it.
10. Short means short: the Planner note is one-line bullets and the actions for now, the PDF is two pages at most, and every action is sorted now or later and put in order (earliest deadline first, then logical). Leave out what is not relevant and list it; when you are not sure, ask Paul in one message. The program fails anything longer, unsorted or unanswered.
11. Setting up the follow-up appointment is an action for Sitamah at every meeting where one was agreed (she books it, or sends the Teams meeting request). The program fails a run that has an agreed appointment and no such action.

## When something goes wrong

- The program refuses a step: read what it says is missing, fix that, run `done` again.
- A tool is unavailable (for example the page tool): say so, use the fallback the step names, and record that it was a fallback.
- Paul corrects something: rule 7 above.
- You cannot reach a file: follow rule 3 and use `run.py ask`, which gives you the exact words for Paul.

## Where the detail lives

The program prints the right page at the right step, so you do not need to open them yourself: `references/00-rules.md` (standing rules and deliverables), `01` access and locating, `02` the two-read lock, `03` the client's file and correspondence, `04` areas, quotes, credit life, cession and carry-forward, `05` accuracy, `06a` the Planner note, `06b` the PDF and file names, `06c` hand-offs, `07` the Teams message. `steps.json` is the list of steps; `deliverables.json` is the list of outputs.
