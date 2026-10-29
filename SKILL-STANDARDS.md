# Skill Standards: the rules every one of Paul's skills must follow

**Version 1.0 (draft for Paul to review)**
**Last updated: 2026-10-29 11:01 (Athens time)**

This file is the memory. If a chat, a session or a skill disagrees with it, this file wins.
Every future Claude Code session in this repo must read it before touching any skill
(`CLAUDE.md` points here and is loaded automatically).

Written in plain words. Each standard has three parts:
- **The rule**: what must always be true.
- **How it is locked in**: what stops it being skipped. A rule that only lives in words will be skipped again.
- **Status**: BUILT, TO BUILD, or NEEDS PAUL.

---

## 0. The one idea behind all of this

Claude reads a skill as words and then decides what to do. Sometimes it does only part of it.
Louder words do not fix that. So:

1. Anything that must happen is done by a small program (a script), not left to Claude's memory.
2. At the end, a checking program prints **PASS or FAIL** for every required item.
3. Claude must show that printout, unedited, in its reply.
4. **No PASS block in the reply, or any FAIL in it, means the job is not finished.** Paul can see this in two seconds.

Honest limit: nothing makes an AI 100% perfect. This makes a half-finished job very hard to get
through, and very easy to spot. It also labels what a program checked ("proven") and what only
Claude says it did ("attested").

---

## 1. The standards at a glance

| # | Standard | Status |
|---|---|---|
| S1 | Follow every instruction strictly; nothing skipped, nothing swapped | Built for 1 skill |
| S2 | Every skill carries a dated "Last updated" (Athens time), set by a program | TO BUILD |
| S3 | Client information comes from the client's file first; ask Paul only as a last resort, with proof | TO BUILD |
| S4 | Always use the access routes (local drive, Microsoft 365, Zapier); never say "I cannot access your files" without proof | TO BUILD |
| S5 | Instructions are clean, ordered and current; outdated text removed; the skill still works | Process written |
| S6 | Every output (reports, Planner note, Teams note to Sitamah) is hard-coded and checked | Built for 2 outputs |
| S7 | Skills are changed only in Claude Code, so scripts and text stay together | Process written |
| S8 | A run leaves its evidence on disk, so it survives a long or compressed chat | Built for 1 skill |
| S9 | Nothing is invented: every fact traces to the transcript or a named document | Built for 1 skill |
| S10 | Nothing is sent from Paul's accounts without his yes | Written |
| S11 | No client data in the repo or in skill text | Written |
| S12 | Every skill has tests on invented data; every real-life bug becomes a new test | Built for 1 skill |
| S13 | Same house conventions everywhere (dates, Rand, names, wording) | Written |
| S14 | Report honestly: say what was checked, what was only attested, and never say "live" until Paul confirms | Written |
| S15 | One skill at a time, finished and tested on a real case before the next | Written |

---

## 2. The standards in detail

### S1. Follow every instruction strictly
**Rule.** Do exactly what the skill says, in the order it says it. No skipping a step, no replacing a required
output with something easier (a text draft is not a PDF), no "I'll do the rest after you correct me",
and no lowering the standard because Paul is frustrated or the job looks small.
A correction from Paul re-opens the whole task, not just the item he named.

**How it is locked in.**
- Each skill lists its deliverables in a manifest (see S6). The checker fails if any is missing.
- The build program refuses to produce anything until the earlier steps are proven done (for the transcript skill: both full reads, the source check, and the mandatory questions answered).
- After any correction, the whole checker runs again and every changed output is rebuilt from one source file, so nothing is left out of date.

**Status.** Built and tested for the Teams transcript skill. To be copied to the others.

### S2. Every skill is dated
**Rule.** Every skill shows `Last updated: YYYY-MM-DD HH:MM (Athens time)` near the top, plus a short change list
(last 5 changes, one line each). The full history is kept in the repo under that skill's `history/` folder,
never in the skill text itself.

**How it is locked in.**
- The stamp is written by a program that reads the Athens clock. Claude never types it by hand.
- The lint tool fails a skill if the stamp is missing, badly formatted, or older than the last change to the files.
- The packaging tool refuses to build the upload zip if lint fails.

**Status.** TO BUILD (`tools/stamp_skill.py`, `tools/lint_skill.py`, `tools/package_skill.py`).

### S3. Client information comes from the client's file first
**Rule.** Everything about a client is looked up from the client's own file before anyone asks Paul:
- the `2. Fact Find` folder (Fact Find, transcripts, earlier follow-up notes, summaries),
- the latest client Overview,
- quotes (the `Comparative Quotes` folders), policy schedules, applications,
- Outlook correspondence for the current transactions.

Paul is asked only for something that is genuinely not in any of those places.

**How it is locked in.**
- Every run keeps a `sources.json`: each document found, its path, its date, and whether it was read.
- Every question to Paul is written into `questions.json` with a `searched` list of the places already checked.
  The checker fails a question with an empty or incomplete `searched` list.
- Each skill names the sources it must read (its "required sources"). The checker fails if one is missing from `sources.json` without a stated reason.

**Status.** TO BUILD (shared kit). The transcript skill already has this rule in words ("be resourceful before you ask").

### S4. Always use the access routes. Never say "I cannot access your files" without proof
**Rule.** Claude **has** access to Paul's files and mail. It must use the routes below, in this order, every time:

| Order | Route | Used for |
|---|---|---|
| 1 | Local drive through the device bridge (`device_stage_files`, `device_commit_files`), into OneDrive: `Company - Paul` and `Company - WR Clients\Paul Kafentzis (Client Files)` | Reading and saving client files |
| 2 | Microsoft 365 connector: SharePoint/OneDrive files, Outlook mail and calendar, Teams meeting transcripts | Same files when the local drive is not reachable; all email; transcripts |
| 3 | Zapier (Office 365 and Teams tools) | Anything the two routes above cannot do (for example, posting to Teams) |

Only after **all three** were tried may Claude ask Paul. When it does, it says exactly what it tried and the
exact error text of each attempt. "I cannot access your files" on its own is never acceptable.

**How it is locked in.**
- Every run keeps an `access_log.json`: route, tool, what was asked, result or error.
- The checker fails if Claude asked Paul for a file, or reported a file missing, while any of the three routes is untried in the log.
- The existing safety rule stays: never touch another broker's folder in `Company - WR Clients`.

**What was checked on 2026-10-29 (Microsoft 365 connector, Paul's account).** Granted permissions include:
read and write on all files (`Files.ReadWrite.All`), read on all SharePoint sites (`Sites.Read.All`),
mail read/write/send, calendars, Teams chat read, **Teams meeting transcripts read
(`OnlineMeetingTranscript.Read.All`)**, recordings and AI insights read.
Two consequences, both still to be tested on a real run:
1. The connector may be able to fetch Teams transcripts directly, which could replace the browser-based `client-transcript-download` step.
2. The connector's permission list has **no permission to send Teams chat messages**, so posting to Teams probably has to go through Zapier's Teams tool (route 3). Until tested, treat a Teams send via route 2 as likely to fail.

**What I cannot promise.** This Claude Code session cannot see Paul's laptop on its own. The device-bridge tools
live in the chat where the skills run. A Claude Code session can attach a folder from Paul's computer through
Remote Control, but that needs his computer on and set up, and has not been tested. The standard forces every
route to be tried and logged. It cannot open a door that is genuinely locked.

**Status.** TO BUILD (access ladder in the shared kit). Routes 2 and 3 to be tested on the first real run.

### S5. Instructions are clean, ordered and current. Outdated text is removed. The skill still works
**Rule.** Each SKILL.md is short, in order, and states each rule once, plainly. It has an Index at the top.
Anything outdated is removed, but removal is done safely:

1. **Inventory first.** List every rule, step, contact, tool name, other-skill name, file-name pattern, number and output in the old skill.
2. **Archive.** Copy the old text, word for word, into `history/` before anything is removed.
3. **Rebuild.** Write the new text. Obviously replaced rules (for example a rule that the skill's own change list says was reversed) are dropped.
   Anything uncertain goes on a **removal list** for Paul's yes/no. Nothing uncertain is dropped silently.
4. **Compare.** Every inventory item must be in the new text or on the approved removal list with its reason. Anything missing is a bug.
5. **Test.** Run the tests, then one real case, before the skill is called finished.

**How it is locked in.** `lint_skill.py` checks the structure (Index, allowed header keys, size, stamp, no client names or ID numbers in examples).
A separate inventory comparison list is kept per skill in `history/`.

**Status.** Process written. Lint tool TO BUILD.

### S6. Every output is hard-coded, so nothing is skipped
**Rule.** A skill that makes several things must make **all** of them every time. Typical set:
- the reports (for example a PDF),
- the **Planner / AdviceTech note**, shown so Paul can copy and paste it from the right-hand pane,
- the **Teams meeting note to Sitamah**, shown so Paul can paste it into the Teams chat,
- email drafts, saved files, and hand-overs to other skills.

**How it is locked in.**
- Each skill has a manifest, `deliverables.json`, listing every deliverable: what it is, which program makes it, how it is handed over (right-hand pane, chat, file in chat, saved to a named folder, Outlook draft), and how it is checked.
- One build command makes all of them from the same source file, so they cannot disagree.
- The checker confirms each one exists, is not empty, contains every action point, and matches the source. Missing one is a FAIL.
- Hand-over steps that only Claude can do (showing it in the pane, sending the file, saving through the device bridge) are recorded in `receipt.json` with the real tool output pasted in. The checker labels them ATTEST.
- Planner and Teams notes are shown as formatted text, never inside a code block, because the Planner does not render markdown symbols. They must appear formatted (bold as bold), not as raw text with asterisks.

**Status.** Built and tested for two outputs (Planner note, PDF) in the transcript skill. TO BUILD: the Teams note to Sitamah, and the right-hand-pane hand-over (see Open questions).

### S7. Skills are updated only in Claude Code
**Rule.** The repo is the one true copy of every skill: the text, the scripts and the tests together.
Any change is made here, tested here, and packaged here. Changes are **not** made through the claude.ai
"Update skill" card for any skill that has scripts, because that card saves the text only and would
split the text from its scripts.

**How it is locked in.**
- `package_skill.py` builds the upload zip. It runs lint and the tests first and refuses if either fails.
- The zip carries the Athens-time stamp (S2). Paul uploads it (one upload per change); Claude writes the step-by-step the first time.
- Claude never says a change is live until Paul confirms he uploaded it (S14).

**Replaces.** Rule 9 of the old "Universal operating rules" block, and the "only propose it with the card" guardrail in `correcting-skills`, for any skill that has scripts. Both skills need their wording updated (see section 5).

**Status.** Process written. Packaging tool TO BUILD.

### S8. A run leaves its evidence on disk
**Rule.** Each run works in its own folder with a state file, so a long or compressed conversation cannot make
Claude forget where it was. The `status` command always says what is done and what the next required step is.
This replaces "re-load the skill after any compression" with something that actually works.
**Status.** Built for the transcript skill.

### S9. Nothing is invented
**Rule.** Every fact and every action point in an output must trace to a quote in the transcript (with its line number) or to a named document.
A garbled line is never turned into a fact. Anything the client left with himself ("I'll get back to you") is not a chase action.
**How it is locked in.** Each output item carries its source; the checker finds the quote in the real text. No match is a FAIL.
**Status.** Built for the transcript skill.

### S10. Nothing is sent without Paul's yes
**Rule.** By default Claude prepares drafts (email, Teams message, invite) and shows them. It sends only after Paul says yes in that conversation.
A skill may send on its own only if its own rules say so and Paul has approved that wording.
**Status.** Written. To be copied into each skill's rules.

### S11. No client data in the repo or in skill text
**Rule.** The repo holds scripts, tests and skill text only. Tests use invented people and figures.
Skill examples use placeholders such as "(Client Name)". Never write ID numbers, account numbers or tax numbers in an output.
Client working files stay on Paul's drive and in his Microsoft 365.
**How it is locked in.** Lint scans for 13-digit numbers and, once Paul supplies a name list, for client names. The commit step checks the same.
**Known problem.** The current transcript skill's examples contain three real client names. They must go in the rewrite.
**Status.** Written. Lint TO BUILD.

### S12. Tests on invented data, and every real bug becomes a test
**Rule.** A skill is not finished until its tests pass. When a real run goes wrong, the first thing done is to add a test that fails the same way, then fix the skill until it passes.
**Status.** Built for the transcript skill (47 tests).

### S13. House conventions (the same everywhere)
- Dates are DD/MM/YYYY in text. File names use DD.MM.YY where the skill says so.
- Money is written with R (R1,172.79), exactly as stated.
- Stamps and "Last updated" use Athens time.
- Every action point is owned by Sitamah. Paul is never the owner of an action.
- Plain words. The same word for the same thing throughout.

### S14. Report honestly
**Rule.** Say what was checked and how. Say what a program proved and what Claude only attested.
If a rule cannot be met, stop and say which rule and why; never hand over partial work as if complete.
Never say a skill change is live until Paul confirms he uploaded it.

### S15. One skill at a time
**Rule.** Finish one skill, test it on a real case, get Paul's yes, then start the next. After a skill goes live, there is a watch period: Paul reports anything that behaves differently, and each report becomes a test (S12).

---

## 3. The standard kit (how every skill is built)

```
skills-hard-coding/
  CLAUDE.md                  read-first memory for Claude Code (points here)
  SKILL-STANDARDS.md         this file
  tools/                     shared programs (TO BUILD): stamp_skill, lint_skill, package_skill, access ladder
  <skill-name>/
    SKILL.md                 short: Index, Last updated, run protocol, standing rules
    deliverables.json        every output and how it is made, handed over and checked
    scripts/                 programs that do the must-happen work and the checking
    tests/                   tests on invented data
    history/                 old text word for word, inventory list, full change history
    README.md                what this skill's programs do
```

Every run (one client, one meeting) keeps in its own run folder:
`state.json` (what has been done), `sources.json` and `questions.json` (S3), `access_log.json` (S4),
`ledger.json` and `content.json` (the facts and outputs, each with its source), `out/` (the deliverables),
`receipt.json` (hand-over evidence).

---

## 4. How to correct any skill (the checklist Claude Code follows)

1. Read this file and the skill's whole folder. Say back to Paul, in plain words, what will change. Wait for his yes.
2. Take the inventory (S5 step 1). Archive the old text (step 2).
3. Find the steps that must always happen. Move them into scripts. List every output in `deliverables.json` (S6).
4. Rewrite SKILL.md: Index, Last updated (by program), short run protocol, standing rules, no client names, no outdated text.
5. Add the standard parts: sources and questions (S3), access ladder (S4), receipts (S6), state (S8).
6. Write tests, including one for every known past failure (S12). Run them.
7. Compare inventory against the new text (S5 step 4). Show Paul the removal list.
8. Package (S7), then give Paul the upload steps. Do not call it live until he confirms.
9. Watch period on a real case (S15). Update this file's tracker.

---

## 5. What this replaces in the older rules (to be updated in the skills themselves)

| Old rule | Now |
|---|---|
| "Re-load the skill after any compression" | `status` command plus the checker output show the next required step (S8) |
| Rule 9: edit the skill, then use the `propose_skills` card | Only for skills with no scripts. Skills with scripts are changed in Claude Code and uploaded as a zip (S7) |
| `correcting-skills` "Route 1: single page only, never touch bundled files" | Not for skills that carry scripts. A zip upload is part of the standard route |
| `correcting-skills` "never remove a rule" | Still true, with one addition: rules the skill's own change list says were reversed are dropped, and uncertain ones go to Paul as a removal list |
| Full change history inside the skill text | Moves to `history/` in the repo; the skill keeps the last 5 lines |

`correcting-skills` and `master-skill-template` are themselves skills and must be brought up to this standard.

---

## 6. Open questions for Paul

1. **Right-hand pane.** I understand "the right-hand pane" to be the side panel where a document or file opens, so the Planner note and the Teams note appear there ready to copy. The current skill says "show in the chat". Is the side panel what you want, in addition to or instead of the chat? Either way the note must show as formatted text, not raw asterisks.
2. **Teams note to Sitamah.** The Teams transcript skill has no such note today. Does it need one? Which other skills do, and what must each contain?
3. **Removing outdated text.** I propose: clearly replaced rules are dropped automatically, anything uncertain comes to you as a short yes/no list. Is that right?
4. **Which skill after the transcript skill?** Suggested next: the one that fails most often after that one.

## 7. Known gaps found in the Teams transcript skill (to fix in its rewrite)

- Step 3 says "eight areas" but lists seven. Which is right?
- No Teams note to Sitamah deliverable (question 2 above).
- Examples contain real client names (S11).
- Change history is longer than the rules and sits at the top of the file (S2, S5).
- The "first-meeting exception" (06.10.26) was reversed on 07.10.26 but its backstory is still in the text.

## 8. Skill tracker

| Skill | Status |
|---|---|
| client-teams-transcript-skill | First slice built and tested (reading lock, source check, PDF + Planner note, checker, 47 tests). SKILL.md rewrite waiting for Paul's OK of this file |
| client-pipeline-board, complete-applications-skill, fact-find-summary, ff-population-transcript, wr-roa-builder, wr-sroa-builder, rgar-skill, om-optimal-ra-proposal, om-tax-free-skill, investment-comparisons-skill, life-insurer-comparison, life-policy-schedule-analyzer, client-review-notes, client-transcript-download, teams-meeting-setup-skill, outlook-emails-skill, planner-interim-procedure, cameron-short-term-skill, advicetech-website-knowledge, alpha-bank-statements, nedbank-current-account-categorization, paul-email-signature, correcting-skills, master-skill-template | Not started |

## 9. Changelog (last 5)

| When (Athens time) | What changed |
|---|---|
| 2026-10-29 11:01 | Version 1.0 written from Paul's seven rules plus eight additions (S8 to S15); Microsoft 365 permissions recorded; open questions and known gaps listed |
