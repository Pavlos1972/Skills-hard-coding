---
name: "teams-meeting-setup-skill"
description: "Creates the follow-up Teams meeting invite in Outlook Calendar for a Wealth Revolution client once the date is confirmed (or moves an existing one). A program builds the exact invite from the Fact Find and the facts, shows it to Paul with one question, and a checker compares what the tool returned with what he approved. Use when client-pipeline-board chains to it or Paul says 'set up the follow-up meeting'."
---

# Teams Meeting Setup

## Index

| # | Section | What it covers |
|---|---|---|
| 1 | Run it | The one command that starts the job and how every step works |
| 2 | What a finished run contains | The invite, the message to Sitamah and the short audit |
| 3 | Standing rules | The rules that never bend, one line each |
| 4 | When something goes wrong | What to do instead of improvising |
| 5 | Where the detail lives | The pages the program shows at each step |

**Last updated: 2026-11-03 12:09 (Athens time)**

**Recent changes** (last 5, one line each; full history in the repo `history/` folder)

| When (Athens time) | What changed |
|---|---|
| 2026-11-03 12:09 | First program-driven version: a program builds the exact invite and the message to Sitamah, Paul approves with one question, a checker compares what the tool returned |
| - | - |

## Run it

This skill is a program that walks you through the job one step at a time. You do not work from memory of this page: the program shows everything below again, at the right moment.

1. Find this skill's folder (the "Base directory" shown when the skill loaded; it contains `scripts/run.py`). If you are unsure: `find /mnt /root /home /opt /tmp -path '*teams-meeting-setup-skill/scripts/run.py' 2>/dev/null | head -1`
2. Choose a new run folder, for example `/tmp/wr-tm-<Surname>-<DDMMYY>`, and start: `python3 <skill folder>/scripts/run.py start <run folder> --client "First Surname"` (to MOVE an existing invite add `--mode reschedule --event-id <the existing event id>`). The program's first lines give you one sentence to say to Paul before anything else: which version of this skill is running.
3. Do exactly what the step says. When it says you are done, run `python3 <skill folder>/scripts/run.py done <run folder> <step>`. The program checks the proof and only then shows the next step. It refuses to skip a step.
4. After a long chat or a compression, run `python3 <skill folder>/scripts/run.py status <run folder>`.
5. The last step prints the SHORT AUDIT. Your reply to Paul is that audit, as it is, plus one plain sentence.

The invite is a REAL SEND (the client is emailed the moment it is created), so the program shows Paul the full invite and the message to Sitamah, asks ONE question and records his yes before anything is sent. Never rewrite, shorten or "improve" the programs during a run, and never type or edit the invite yourself. If the self-test at the start fails, stop and tell Paul exactly what failed.

## What a finished run contains

- The **invite**, built by the program from the client's Fact Find and the recorded facts, created ONCE through the Microsoft 365 tool with exactly the approved arguments (or the existing event updated in place for a reschedule), and the returned event compared with it.
- The **message to Sitamah** (an FYI, sent once through Zapier after Paul's yes) and the lines logged on the board's Fact Find card, as today.
- The **short audit** (Paul, 03/11/2026): one line per check in point form, each with a green tick or a red cross, one closing line for what is only attested. No long printout.
- Nothing is sent without Paul's yes. A run without a PASS audit is not finished: say so.

## Standing rules

1. The invite is a real send: Paul's clear yes comes first, in the same reply that shows the full invite and the message to Sitamah.
2. The client's name and personal email come from the Fact Find; the date, time, topics and anything the client owes come from Paul or the follow-up summary, each with its source. Never invent or guess.
3. Create the event ONCE with exactly the program's arguments; if a result is unclear, look in the calendar before anything else. A reschedule updates the existing event in place, never delete and recreate.
4. Time zone `Africa/Johannesburg` on start and end, exactly 1 hour, the client as the only attendee, Teams on, no hand-written link, meeting ID, passcode or signature.
5. Sitamah is told through Zapier only (the Microsoft 365 connector cannot send Teams messages); never touch another broker's folder.
6. Changes to this skill are made only in Claude Code and uploaded by Paul. Never say a change is live until he confirms.

## When something goes wrong

- The program refuses a step: read what it says is missing, fix that, run `done` again.
- The Fact Find PDF cannot be found or read: tell Paul exactly which routes were tried (computer, Microsoft 365, Zapier); never guess a name or an address.
- A tool fails or returns something that differs from the invite: show Paul the exact error; never send a second invite without first checking the calendar.
- Anything in the invite has to change: run `build` and `show` again; the earlier yes then no longer counts.

## Where the detail lives

The program prints the right page at the right step: `references/00-rules.md` (the rules), `01-find-client.md` (the Fact Find and the three routes), `02-facts.md` (the facts and what the program builds from them), `03-send.md` (creating the event, telling Sitamah, rescheduling), `04-handover.md` (the reply). `steps.json` is the list of steps; `deliverables.json` is the list of outputs.
