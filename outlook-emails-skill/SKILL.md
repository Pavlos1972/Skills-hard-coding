---
name: "outlook-emails-skill"
description: "Tracks Paul Kafentzis's outbound Outlook emails that need a reply: a program builds two scheduled checks (an hourly weekday watcher that stops by itself, and a one-time silence flag), a checker compares what the tool returned with the plan, and Paul's phone is alerted when a reply arrives or someone stays silent. Use when sending or drafting an email that needs a reply."
---

# Outlook Emails - Response Tracking

## Index

| # | Section | What it covers |
|---|---|---|
| 1 | Run it | The one command that starts the job and how every step works |
| 2 | What a finished run contains | The two scheduled checks and the short audit |
| 3 | Standing rules | The rules that never bend, one line each |
| 4 | When something goes wrong | What to do instead of improvising |
| 5 | Where the detail lives | The pages the program shows at each step |

**Last updated: 2026-11-03 13:01 (Athens time)**

**Recent changes** (last 5, one line each; full history in the repo `history/` folder)

| When (Athens time) | What changed |
|---|---|
| 2026-11-03 13:01 | Removed a dated attribution from a reference page |
| 2026-11-03 12:58 | First program-driven version: a program builds an hourly weekday watcher and a one-time silence flag, a checker compares what the tool returned with the plan |
| - | - |

## Run it

This skill is a program that walks you through the job one step at a time. You do not work from memory of this page: the program shows everything below again, at the right moment.

1. Find this skill's folder (the "Base directory" shown when the skill loaded; it contains `scripts/run.py`). If you are unsure: `find /mnt /root /home /opt /tmp -path '*outlook-emails-skill/scripts/run.py' 2>/dev/null | head -1`
2. Choose a new run folder (one per tracked email), for example `/tmp/wr-oe-<DDMMYY>-<short name>`, and start: `python3 <skill folder>/scripts/run.py start <run folder>`. The program's first lines give you one sentence to say to Paul before anything else: which version of this skill is running.
3. Do exactly what the step says. When it says you are done, run `python3 <skill folder>/scripts/run.py done <run folder> <step>`. The program checks the proof and only then shows the next step. It refuses to skip a step.
4. After a long chat or a compression, run `python3 <skill folder>/scripts/run.py status <run folder>`.
5. The last step prints the SHORT AUDIT. Your reply to Paul is the tracking plan plus that audit, as it is.

Never rewrite, shorten or "improve" the programs during a run, and never type or edit the two task files yourself. If the self-test at the start fails, stop and tell Paul exactly what failed.

## What a finished run contains

- A **watcher**: a scheduled task that looks for a genuine reply every hour on weekdays 08:00 to 17:00 South African time, alerts Paul's phone with one line when one arrives, drops that sender, and stops for good at 17:00 on the 5th business day (one last message if anyone is still silent).
- A **silence flag**: one scheduled task at 09:00 Athens time on the 2nd business day after sending, alerting Paul's phone only if someone is still outstanding.
- Both run as a fresh chat each time, may use the Microsoft 365 connector (to read Outlook) and nothing else.
- The **short audit** (Paul, 03/11/2026): one line per check in point form, each with a green tick or a red cross, one closing line for what is only attested. No long printout.
- Nothing is sent to anyone. A run without a PASS audit is not finished: say so.

## Standing rules

1. Any email Claude sends, or drafts for Paul to send, that needs a reply from someone else is tracked, automatically, with no question each time.
2. The senders, subject, date and reason come from the sent email or Paul, each with its source. Never invent; if you cannot say why a reply is needed, do not track it.
3. Create each scheduled task ONCE with exactly the program's settings; if the tool refuses a setting, stop and show Paul the exact error.
4. A failed mail search is a failure, never "no reply". Never depend on read or unread.
5. No signature is typed into any draft; see `paul-email-signature`.
6. Changes to this skill are made only in Claude Code and uploaded by Paul. Never say a change is live until he confirms.

## When something goes wrong

- The program refuses a step: read what it says is missing, fix that, run `done` again.
- The tool refuses a setting, or warns that no connector is stored: show Paul the exact error and stop; nothing is tracked until he decides.
- The read-back shows a red cross: tell Paul exactly which line differs; do not delete or change a task to make it pass.
- The email is not in Sent Items: if it is a draft use today's date; otherwise ask Paul.

## Where the detail lives

The program prints the right page at the right step: `references/00-rules.md` (the rules), `01-email.md` (what to record and where to look), `02-create.md` (creating the two tasks), `03-readback.md` (reading them back), `04-handover.md` (the reply). `steps.json` is the list of steps; `deliverables.json` is the list of outputs.
