---
name: "ff-population-transcript"
description: "Builds the WR Fact Find from the Fact Find form's data file (named Fact Find (Audio to Text)) and the Teams transcript, using the latest Overview as a reference, and finds contact details and the lead source (Referral or D&R Marketing). Use after a Fact Find meeting."
---

# Fact Find Population from the Audio to Text file and Transcript

## Index

| # | Section | What it covers |
|---|---|---|
| 1 | Run it | The one command that starts the job and how every step works |
| 2 | The eight steps | What the program walks you through, in order |
| 3 | What a finished run contains | The deliverables and the proof that ends the job |
| 4 | Standing rules | The rules that never bend, one line each |
| 5 | When something goes wrong | What to do instead of improvising |
| 6 | Where the detail lives | The pages the program shows at each step |

**Last updated: 2026-11-06 14:32 (Athens time)**

**Recent changes** (last 5, one line each; full history in the repo `history/` folder)

| When (Athens time) | What changed |
|---|---|
| 2026-11-06 14:32 | v40: transcript read once, every chunk checked by a line from its middle; form rows added (rental, spousal, maintenance, total income, disability household lines, instalment protector, priorities); overlay rules before writing; Edit tool for the overlay; form-PDF quote check tolerates column order; staged copy for the computer save |
| 2026-11-06 13:29 | access: Paul's permission and his two exact folders in the skill; files staged as exact copies; a .docx is read by the program itself (no pandoc); --copied shows any file the chat typed out; fixed commands only |
| 2026-11-06 11:25 | steps name their checks; deliverables.json added |
| 2026-11-06 11:24 | Operation Skill Restructure 2.0 rebuild from the original: 8 programmed steps; the form's two files and the transcript combined into ONE report (contradictions sorted or highlighted); files found the original way (computer first, no shell commands, no fingerprints, no hard STOP); one stop for Paul's OK; short audit |
| 2026-11-05 17:11 | placeholder, replaced by the stamp tool |

## Run it

This skill is a program that walks you through the job one step at a time. You do not work from memory of this page. Everything below is shown again, at the right moment, by the program.

**A quiet run, and nothing is asked of Paul (Paul's rule).** Start your reply with the one version sentence the program gives you, then work. You may show ONE short progress line per step. Never write an opening recap of this skill, its rules, the files found or the information read; do not read the reference pages yourself (the program shows each page at its step). Never ask Paul for permission, to attach, upload or drag a file, or to say "go". The reply at the end is the outputs and the SHORT audit.

1. Find this skill's folder (the "Base directory" shown when the skill loaded; it contains `scripts/run.py`). If you are unsure: `find /mnt /root /home /opt /tmp -path '*ff-population-transcript/scripts/run.py' 2>/dev/null | head -1`
2. Choose a new run folder, for example `/tmp/wr-run-<Surname>-<DDMMYY>`, and start: `python3 <skill folder>/scripts/run.py start <run folder> --client "First Surname" --date DD/MM/YYYY` (the client and the meeting date exactly as in Paul's message; a couple in one meeting is two runs, see the rules page). The program's first lines give you one sentence to say to Paul before anything else: which version of this skill is running.
3. Do exactly what the step says. When it says you are done, run `python3 <skill folder>/scripts/run.py done <run folder> <step>`. The program checks the proof and only then shows the next step. It refuses to skip a step.
4. After a long chat or a compression, run `python3 <skill folder>/scripts/run.py status <run folder>`. It tells you where the job is up to.
5. The last step prints the SHORT audit (a line per check with a green tick or a red cross). Your reply to Paul contains it, unedited.

Run only the commands the program shows you: no `cp`, `sed`, loops or heredocs, and never open the program's own files. Change `overlay.json` with your Edit or Write tool, never with a shell command. Never rewrite, shorten or "improve" the programs during a run, and never replace the PDF with a text draft. If the self-test at the start fails, tell Paul in one line which item failed and stop.

## The eight steps

1. **Find the files** (the computer first, as the original did) and register them: the form's data file and PDF, the transcript(s), the Overview.
2. **Read the form**: the program reads both files and prints what you must act on.
3. **Read the transcript once, accurately**: the program hands it over chunk by chunk and checks that each chunk was really read.
4. **Contact details and the lead source** (the D&R Marketing email search).
5. **Combine the form and the call into ONE report**: you write what the call adds and every contradiction; the program checks your quotes and makes the report.
6. **Build the PDF and look at it.**
7. **Save it into the client's folder, list it back, show Paul and wait for his OK.**
8. **Summary, Planner note and the message to Sitamah** (made by the other two skills), then the audit.

## What a finished run contains

- The **Fact Find Transcript PDF**: ONE report that combines the form (data file and PDF) and the Teams transcript, saved into the client's `2. Fact Find` folder.
- The **source report** and the SHORT audit saying `RESULT: PASS`. No PASS in your reply means the job is not finished: say so.
- The hand-overs made by the other skills from that one report: the Fact Find Summary, the Planner note page, and the message to Sitamah (posted automatically, once).

## Standing rules

1. **ONE report from BOTH sources.** The form's data file and the transcript are both read in full and combined. The Audio to Text file wins where they differ, and every contradiction is either SORTED (a rule settles it) or HIGHLIGHTED (both values and where each came from).
2. Source first, never invent: every fact traces to the form, the transcript or a named document; the program checks that quoted call lines are really in the transcript.
3. Read before you write: the form's two files, and the whole transcript, once, completely (Paul, 06/11/2026: once, but accurately).
4. Paul's permission is given here: connect to his two folders `~/liferisk.co.za/Company - Paul` and `~/liferisk.co.za/Company - WR Clients/Paul Kafentzis (Client Files)` (one request with exactly those two paths, never the whole `liferisk.co.za`), list, stage (exact copies) and commit; if refused, Microsoft 365, then Zapier. No shell commands on his computer, never retype a file, never ask Paul to attach a file.
5. "Not discussed" is a claim: search the call, the Overview and the documents before leaving a row empty.
6. One stop only: Paul reads the Fact Find PDF and says it is right; everything after that runs by itself.
7. Never lower the standard; a correction re-opens the whole task (the program re-opens the later steps by itself).
8. Changes to this skill are made only in Claude Code and uploaded by Paul. Never say a change is live until he confirms.

## When something goes wrong

- The program refuses a step: read what it says is missing, fix that, run `done` again.
- The form's schema is not 3.0, the transcript is incomplete, or the file is for another client: the program prints one STOP line; give Paul that line and stop.
- A file cannot be found on any route: say in at most five lines what was tried (step 1's `--missing`), and carry on with what exists.
- Paul corrects something: change `overlay.json`, run combine, build, look, save and show again.

## Where the detail lives

The program prints the right page at the right step, so you do not need to open them yourself: `references/00-rules.md` (standing rules), `01` access and locating, `02` the form's two files and the other sources, `03` two spouses, `04` contact details and the lead source, `05` how the form and the call are combined (the overlay), `06` the mapping rules (quotes, debts, totals, ABIs), `07` build, look, save and the one stop, `08` the hand-overs. `steps.json` is the list of steps.
