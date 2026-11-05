---
name: "ff-population-transcript"
description: "Builds the WR Fact Find from the Fact Find form's data file (named Fact Find (Audio to Text)) and the Teams transcript, using the latest Overview as a reference, and finds contact details and the lead source (Referral or D&R Marketing). Use after a Fact Find meeting."
---

# Fact Find Population from the Audio to Text file and Transcript

## Index

| # | Section | What it covers |
|---|---|---|
| 1 | Run it | The one command that starts the job and how every step works |
| 2 | What a finished run contains | The deliverable and the proof that ends the job |
| 3 | Standing rules | The rules that never bend, one line each |
| 4 | When something goes wrong | What to do instead of improvising |
| 5 | Where the detail lives | The pages the program shows at each step |

**Last updated: 2026-11-05 15:59 (Athens time)**

**Recent changes** (last 5, one line each; full history in the repo `history/` folder)

| When (Athens time) | What changed |
|---|---|
| 2026-11-05 15:59 | Computer first: the program finds the client's OneDrive folder and stops at the start if it is not there; every copy proved byte for byte; a PDF only as whole real bytes; amounts only the PDF holds; the PDF saved on the computer; the ledger locked |
| 2026-11-05 14:20 | Fix: the form's summary lines that only repeat a row's own label and form value are no leak (row-by-row check); tests added |
| 2026-11-05 10:43 | Comment tidy |
| 2026-11-05 10:43 | Dated notes moved out of the live pages |
| 2026-11-05 10:42 | Strict changes after the first real run: files found automatically through Microsoft 365 (no permission step, no attach), a quiet run, the short audit as the program's own printout, the message to Sitamah posted automatically |

## Run it

This skill is a program that walks you through the job one step at a time. You do not work from memory of this page. Everything below is shown again, at the right moment, by the program.

**A quiet run, and nothing is asked of Paul (Paul's rule).** Start your reply with the one version sentence the program gives you, then work. You may show ONE short progress line per step (for example "Step 3 of 16: preparing the transcript"). Never write an opening recap of this skill, its rules, the files found or the information read; do not read the reference pages yourself (the program shows each page at its step). Never ask Paul for permission, to click Allow, to attach, upload or drag a file: find the files yourself, from the computer first (the program checks the connection in step 1: if it prints STOP, your whole reply is that text). The reply at the end is the outputs and the SHORT audit.

1. Find this skill's folder (the "Base directory" shown when the skill loaded; it contains `scripts/run.py`). If you are unsure: `find /mnt /root /home /opt /tmp -path '*ff-population-transcript/scripts/run.py' 2>/dev/null | head -1`
2. Choose a new run folder, for example `/tmp/wr-ff-<Surname>-<DDMMYY>`, and start: `python3 <skill folder>/scripts/run.py start <run folder> --client "First Surname" --date DD/MM/YYYY`. The client and the meeting date are taken exactly from Paul's message; the program checks every later file against them. For two spouses in one meeting start one run per spouse (`--spouse "Other Surname" --spouse-run <their run folder>`). The program's first lines give you one sentence to say to Paul before anything else: which version of this skill is running. It comes from the Last updated line above, so it moves with every update.
3. Do exactly what the step says. When it says you are done, run `python3 <skill folder>/scripts/run.py done <run folder> <step>`. The program checks the proof and only then shows the next step. It refuses to skip a step.
4. After a long chat or a compression, run `python3 <skill folder>/scripts/run.py status <run folder>`. It tells you where the job is up to.
5. The last step prints the SHORT AUDIT (a line per group with ✅ or ❌, one line for what is only attested, the sources used, what to glance at, the delivery line). Your reply to Paul contains that printout, unedited, and the outputs. The full report is a file in the run folder.

Never rewrite, shorten or "improve" the programs during a run, and never replace the PDF with a text draft or a Word file. If the self-test at the start fails, stop and tell Paul exactly what failed.

## What a finished run contains

- The **Fact Find Transcript PDF** (`Fact Find Transcript - DD.MM.YY - (Name Surname).pdf`), drawn by the program in the fixed 11 sections plus Next Steps & Next Meeting, sent in the chat, saved into the client's `2. Fact Find` folder and listed back (the listed size must equal the local file's).
- The **short audit** printed by the checker, with the font that was really used (Aptos, or a named substitute: say which). The full report is the file `out_record/audit-full.txt`; it is never pasted into the chat.
- The hand-overs made by the other two skills: the Fact Find Summary (`fact-find-summary`), and the Planner note page and the message to Sitamah (`client-teams-transcript-skill`, started with `--type first`). They are shown in the same reply. The message to Sitamah is POSTED AUTOMATICALLY through Zapier (Paul's rule): no question, once per meeting.
- The short audit saying `RESULT: PASS`. No PASS in your reply means the job is not finished: say so.

## Standing rules

1. Source order: the form's data file first (and its saved PDF), the Teams transcript second, the latest Overview as a reference, the Manual Fact Find only if Paul says so after the program asked him; where they differ the form wins and the difference is flagged with both values.
2. Never invent: every value in the PDF traces to its source, and the program checks the quote or the figure.
3. Read the whole transcript twice, in order, before anything is drafted. The program enforces it.
4. Client information comes from the client's file first, read from the COMPUTER (the client's OneDrive folder, real bytes, every copy proved identical to its original); Microsoft 365 and Zapier serve small text files only and never a PDF. The finished PDF is saved on the computer. Log each try. Never ask Paul for permission, to click Allow, or to attach, upload or drag a file.
5. If the form's data file is missing on all three routes, STOP and ask Paul: the Manual Fact Find PDF, or the transcript alone? Record his words.
6. The form's schema must be 3.0; anything else stops the run with one line for Paul. The form's summaries, drafted actions, parking list and cost counters are never a source.
7. `Not discussed` is a claim: the program searches the call, the documents and the form's own related fields first, with search words written for each field. A field the search finds something for is never called `Not discussed` without your written reason that names a found call line and quotes some of its words. Never write it as a default.
8. Totals reconcile to the cent and debt is never left out of a calculation, whatever credit life says.
9. The standing ABIs and the Dread Disease default are written by the program; only Paul can state otherwise.
10. An FNA, Shortfall or Reduced quote names the insurer and says New Business or Servicing. There is no default: if neither source says, ask Paul.
11. A policy number comes only from the policy schedule.
12. One fact per line; short bullets; no page numbers; a row is never split across pages.
13. The Fact Find Summary, the Planner note and the message to Sitamah are made by the other two skills, once. The message to Sitamah is posted automatically through Zapier (Paul's rule); nothing else is sent.
14. After any correction from Paul, re-open the whole task: fix it in the overlay, compose, build, redo the hand-overs that changed, run the final check again.
15. If a rule cannot be met, stop and say exactly which one and why. Never hand over partial work as complete.
16. Changes to this skill are made only in Claude Code and uploaded by Paul. Never say a change is live until he confirms it.
17. Paul's own words are recorded only with `run.py ask` (say what it is about: at most 10 ids, each named in the question; to free a request line, at most 5 lines, each quoted in the question) and `run.py answer`. The overlay points at them; it never contains them, and a number you use must be in his words.
18. An Overview or a Policy schedule counts only with a text copy that names the client, and a number of six or more digits is printed only when a recorded document shows it.
19. The programs run as they are. A fingerprint of the programs, the layout, the steps and the rule pages is checked at every step and printed in the final line; if they change during a run, start again (a change is detected unless someone also changes the checker, so Paul compares the printed fingerprint).

## When something goes wrong

- The program refuses a step: read what it says is missing, fix that, run `done` again.
- A tool is unavailable (for example the page tool or the Agent tool): say so, use the fallback the step names, and record that it was a fallback.
- The form file is missing or its schema is not 3.0: stop, tell Paul in one line, and follow the step.
- You cannot reach a file: go to the next route at once; when every route has failed, say in at most five lines what failed and stop. Never ask Paul to attach or click anything (`run.py ask` is only for the content question when the form's data file is missing).
- Paul corrects something: rule 14 above.

## Where the detail lives

The program prints the right page at the right step, so you do not need to open them yourself: `references/00-rules.md` (standing rules, delivery gate, deliverables), `01` where the files are and the missing-form stop, `02` the form's data file and the Manual Fact Find, `03` two spouses, `04` contact details and lead source, `05` the layout, `06` and `07` the mapping rules (quotes, debts, totals, ABIs), `08` the final pass, `09` the formatting, `10` build, save and iterate, `11` the hand-overs, `12` the two reads. `steps.json` is the list of steps; `deliverables.json` is the list of outputs; `scripts/layout.json` holds the 11 sections and their labels.
