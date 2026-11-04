# Skill Standards: the rules every one of Paul's skills must follow

**Version 4.6 (draft for Paul to review)**
**Last updated: 2026-11-03 09:12 (Athens time)**

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
| S2 | Every skill carries a dated "Last updated" (Athens time), set by a program | BUILT (`tools/stamp_skill.py`, `tools/lint_skill.py`) |
| S3 | Client information comes from the client's file first; ask Paul only as a last resort, with proof | Built for 1 skill |
| S4 | Always use the access routes (local drive, Microsoft 365, Zapier); never say "I cannot access your files" without proof | Built for 1 skill (logged, enforced); untested on real files |
| S5 | Instructions are clean, ordered and current; outdated text removed; the skill still works | BUILT (`tools/inventory.py`, `tools/lint_skill.py`) |
| S6 | Every output (reports, Planner note, Teams note to Sitamah) is hard-coded and checked | Built for 1 skill (page, PDF, Teams message) |
| S7 | Skills are changed only in Claude Code, so scripts and text stay together | BUILT (`tools/package_skill.py`) |
| S8 | A run leaves its evidence on disk, so it survives a long or compressed chat | Built for 1 skill |
| S9 | Nothing is invented: every fact traces to the transcript or a named document | Built for 1 skill |
| S10 | Nothing is sent from Paul's accounts without his yes | Written |
| S11 | No client data in the repo or in skill text | BUILT (lint scans a private name list kept outside the repo) |
| S12 | Every skill has tests on invented data; every real-life bug becomes a new test | Built for 1 skill |
| S13 | Same house conventions everywhere (dates, Rand, names, wording) | Written |
| S14 | Report honestly: say what was checked, what was only attested, and never say "live" until Paul confirms | Written |
| S15 | One skill at a time, finished and tested on a real case before the next | Written |
| S16 | A program drives the job step by step and shows the next step only when the last one is proven | APPROVED 29/10/2026; PROVEN in real chats on the Teams transcript skill (Paul, 30/10/2026: "Yes it is live"); next skills follow the same kit |

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
- **The date moves with the skill (Paul, 29/10/2026: "every time the skill is updated further, that date must change").** The stamp tool records a fingerprint of every file the zip carries (`history/stamp.json`). The lint tool fails a skill whose files changed after they were stamped, or whose date line was edited by hand, or that has no record. File times are not used (a fresh copy of the repo would make them meaningless). The stamp tool refuses to move the date when nothing changed.
- The packaging tool refuses to build the upload zip if lint fails, and names the zip after the stamp.
- **Every run says which version it is.** The skill's program prints one sentence, read from the stamp: "Using <skill name>, last updated DD/MM/YYYY HH:MM (Athens time)". Claude's first words to Paul are that sentence. The checker's final printout repeats it (heading and delivery line), and warns if the skill was updated while the run was in progress. The date is NOT put in the skill's name: names allow only lowercase letters, numbers and hyphens, other skills call this one by name, and a dated name would go stale at the next fix.

**Status.** BUILT and tested (`tools/stamp_skill.py`, `tools/lint_skill.py`, `tools/package_skill.py`).

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

**Status.** BUILT inside the Teams transcript skill (`run.py source`, `run.py ask`, group S of `verify.py`); to be lifted into a shared kit when the second skill is converted.

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
Two consequences (the first still to be tested on a real run):
1. The connector may be able to fetch Teams transcripts directly, which could replace the browser-based `client-transcript-download` step.
2. The connector's permission list has **no permission to send Teams chat messages**. This is already confirmed in real use: `ff-population-transcript` Step 8 records a 403 error on 09/10/2026 and says Zapier is the only working route for Teams messages.

**What I cannot promise.** This Claude Code session cannot see Paul's laptop on its own. The device-bridge tools
live in the chat where the skills run. A Claude Code session can attach a folder from Paul's computer through
Remote Control, but that needs his computer on and set up, and has not been tested. The standard forces every
route to be tried and logged. It cannot open a door that is genuinely locked.

**Status.** BUILT inside the Teams transcript skill (`run.py access`, enforced by `verify.py` group S and `run.py ask`). The routes themselves are untested on real files: routes 1 to 3 are tried for real on the first real-case trial.

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

**Status.** BUILT: process written, `tools/inventory.py` and `tools/lint_skill.py` working and tested. Used on the Teams transcript skill.

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
- **Planner / AdviceTech note** (Paul's standing rule, 09/10/2026, already in `ff-population-transcript`): always shown as a private HTML page (an Artifact, the right-hand pane) with a Copy note button that copies the bold, italics and bullets intact. Never as plain chat text and never inside a code block, because the Planner does not render markdown symbols. If the page tool is unavailable, say so and fall back to formatted chat text, stating it is the fallback.
- **The page is generated by a program from the same source file as everything else.** Claude's only job is to publish that file and report the link. Today's skills point to a page template that is missing from the Teams transcript skill, so each chat invents its own layout. That ends here.
- **Teams message to Sitamah** (rule from `ff-population-transcript` Step 8, 09/10/2026): one fixed line, `[Name Surname] - [1st/2nd/3rd...] Teams Appointment Completed: [DD/MM/YYYY] - Please see instructions in Client / Prospect Task.` plus `Please take note of Follow Up Appt.` only when the Summary and the Planner note show a real, agreed follow-up date. Sent through Zapier to the 1:1 chat with Sitamah, in bold and heading size, only after Paul's clear yes, once per meeting, as the very last step. Zapier returns a message id and sent time, which go in the receipt. If the send fails, Claude says so and gives Paul the text to paste; it never claims it was sent.

**Status.** Built and tested for two outputs (Planner note text, PDF) in the transcript skill. The Planner HTML page with Copy button (tested in a real browser) and the Teams message text with its Zapier receipt are BUILT. Publishing the page, the Zapier send and the folder save are attested by Claude, not machine-proven.

### S7. Skills are updated only in Claude Code
**Rule.** The repo is the one true copy of every skill: the text, the scripts and the tests together.
Any change is made here, tested here, and packaged here. Changes are **not** made through the claude.ai
"Update skill" card for any skill that has scripts, because that card saves the text only and would
split the text from its scripts.

**How it is locked in.**
- `package_skill.py` builds the upload zip. It runs lint and the tests first and refuses if either fails.
- The zip carries the Athens-time stamp (S2). Paul uploads it (one upload per change); Claude writes the step-by-step the first time.
- Claude never says a change is live until Paul confirms he uploaded it (S14).

**Replaces.** Rule 9 of the old "Universal operating rules" block, and the "only propose it with the card" guardrail in `correcting-skills`, for any skill that has scripts. Both skills need their wording updated (see section 6).

**Status.** BUILT: `tools/package_skill.py` refuses to package unless lint and all tests pass, and re-runs the tests against the unpacked zip.

**How a new version gets into Paul's claude.ai Skills (checked and observed 29/10/2026; do not research it again unless Anthropic's pages change).**
- Claude Code (cloud or local) can list and read Paul's claude.ai skills but has no tool that creates or replaces one. The skills folder in a cloud session is a one-way copy made when the session starts.
- Anthropic's Agent Skills overview says custom skills on claude.ai are uploaded by the user as zip files (Settings > Features, also called Customize), are individual to each user and "do not sync across surfaces". The Skills API (`/v1/skills`) needs a Console API key and its skills are not available on claude.ai. The GitHub-repo sync (Organization settings > Plugins & skills) is documented for Team and Enterprise owners only; Paul is on **Max**.
- **The method that works (first used 29/10/2026, reported by the Claude-in-Chrome chat):** Paul gives a chat that has Claude in Chrome the upload brief; that chat uploads the zip in his browser. `package_skill.py` writes the brief next to every zip (`<zip name>.upload-brief.md`, made by `tools/make_upload_brief.py` from the zip itself, nothing typed by hand). Make the brief only when Paul has asked for that skill to be uploaded: his request is the approval for the "Upload and replace" button.
- **Uploading REPLACES the skill.** claude.ai cannot hold two skills with one name. The upload shows a box ("Replace '<name>' skill? ... Earlier versions stay available in the skill's version history. Current: N lines - This file: M lines"). The old version is NOT a separate switched-off entry: it stays in the skill's **version history** (a dropdown of v1, v2 ... on the skill page), and that history is the backup. Switching the old skill off first changes nothing (a disabled skill is switched on again by the upload), so the brief says not to.
- **The first upload attempt may be refused** ("only files this session is allowed to read can be uploaded", and the Windows path may still be refused). The fix: the chat asks Paul to approve folder access to `Claude Skills - New`, stages the zip into its workspace (`/mnt/user-data/uploads/...`), checks the byte size, and uploads from the staged path. Paul did not have to pick the file himself.
- **Tested the same way every time:** before and after the upload a fresh chat is asked, with no client information, to quote the skill's "Last updated" line and its first section title; the chat records the old version's line count and "Last updated" line before, and compares after. The expected new values come from the zip.
- Paul keeps new zips in `C:\Users\Paul\liferisk.co.za\Company - Paul\Claude\Claude Skills - New` on his Windows computer (his instruction). A cloud session cannot put a file there: Paul saves the zip there himself.
- Paul's skills are ordinary skills in his account (each has its own skill id), not plugin skills.
- The upload rules are enforced by lint: frontmatter keys limited to name, description, license, compatibility, metadata, allowed-tools; name in lowercase letters, numbers and hyphens only.
- Every run says its version first (S2), so Paul sees at once whether the new upload is the one answering.
- Proven second case (the rebuilt skill, same method, no problems): replaced v33 by v34; the brief generated by `package_skill.py` worked without any change, the staging fix was not even needed (folder access already worked), and the test chat quoted the new Last updated line. Paul does not have to pick the file.
- Proven first case: the Teams transcript skill was replaced as version v33 (old SKILL.md 319 lines, new 65 lines plus 11 reference pages and the programs); a fresh chat quoted `Last updated: 2026-10-29 13:38 (Athens time)` and `Index`. This was reported by the Chrome chat, not seen by Claude Code.

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
**Status.** BUILT: lint scans for 13-digit numbers and, with a private names file kept outside the repo, for client names.

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

### S16. A program drives the job, one step at a time (approved 29/10/2026; condition met 30/10/2026: it works in real chats)
**Rule.** The skill's text is short. It says: run the driver command, do exactly what it prints, run it again. The driver
shows the next step only after the proof for the previous step is on file. At the very start it runs a self-test (right tools
present? python, PDF tools, Zapier, Microsoft 365 reachable?) and stops with a plain message if something is missing,
so a chat can never quietly fall back to a text draft.
**Why.** Long skills get skimmed or forgotten after a long chat. A step Claude has not been shown cannot be skipped.
**How it is locked in.** `steps.json` per skill (the ordered steps, the proof each needs); one driver program shared by all skills.
**Condition set by Paul.** "As long as it works." So: tested here on invented data first, then tried by Paul in a real chat on one
real client, with the old skill kept as a backup. Nothing is called finished before that real trial passes.
**Status.** Approved. Built for the Teams transcript skill (`scripts/run.py`, `steps.json`); to be proven in a real chat. The shared parts (access log, sources, questions, receipts) are inside that skill's scripts and will be lifted into a shared kit when the second skill is converted.

---

## 3. Where the program lives (plain words)

- **Inside the skill itself.** A skill is a folder: the instructions (SKILL.md) plus the programs, packed together as one zip.
  Paul uploads the zip once, and Claude receives both together. Eight of Paul's skills already work this way
  (for example `wr-roa-builder`, `wr-sroa-builder`, `fact-find-summary`, `rgar-skill`, `ff-population-transcript`).
- **In each chat.** When the skill starts, the chat gets its own temporary copy of that folder, like a toolbox put on a desk.
  Claude runs the program from there. The program keeps its notes (what is done, what is next) in the chat's workspace.
  When the chat ends, the workspace is cleared. The finished files live in the client's folder, saved through the connections.
- **The master copy** is this GitHub repo. Changes are made here (S7), tested here, and the zip is made from here.
- **How it governs.** The skill's first instruction is "run the program". The program then says what to do next, remembers
  where the job is up to, builds the outputs and does the final checking.
- **A difference from today.** In the Fact Find skill, Claude treats its script as "a starting template" it may change.
  In the new standard the program is run as it is, never rewritten by Claude during a run.
- **What I cannot see from here.** I cannot run anything inside Paul's claude.ai chat, so how the chat's workspace behaves is
  proven only by a real trial. The program's first action is a self-test that stops with a plain message if something it needs is missing.
- **Packaging.** Anthropic's own `skill-creator` skill contains a `package_skill.py`; the standard packaging tool (S7) starts from that idea.

---

## 4. The standard kit (how every skill is built)

```
skills-hard-coding/
  CLAUDE.md                  read-first memory for Claude Code (points here)
  SKILL-STANDARDS.md         this file
  tools/                     shared programs (BUILT): stamp_skill, inventory, lint_skill, package_skill
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

## 5. How to correct any skill (the checklist Claude Code follows)

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

## 6. What this replaces in the older rules (to be updated in the skills themselves)

| Old rule | Now |
|---|---|
| "Re-load the skill after any compression" | `status` command plus the checker output show the next required step (S8) |
| Rule 9: edit the skill, then use the `propose_skills` card | Only for skills with no scripts. Skills with scripts are changed in Claude Code and uploaded as a zip (S7) |
| `correcting-skills` "Route 1: single page only, never touch bundled files" | Not for skills that carry scripts. A zip upload is part of the standard route |
| `correcting-skills` "never remove a rule" | Still true, with one addition: rules the skill's own change list says were reversed are dropped, and uncertain ones go to Paul as a removal list |
| Full change history inside the skill text | Moves to `history/` in the repo; the skill keeps the last 5 lines |

`correcting-skills` and `master-skill-template` are themselves skills and must be brought up to this standard.

---

## 7. Decisions by Paul (29/10/2026) and what is still open

**Decided**
1. **Right-hand pane** = the Planner note as a private HTML page with a Copy button (same as his 28/10/2026 page). Hard-coded by program (S6).
2. **Teams message to Sitamah**: use the one in `ff-population-transcript` Step 8, posted through Zapier to her chat, with Paul's yes. The follow-up (transcript) skill uses the same message with the right ordinal (2nd, 3rd...).
3. **Removing outdated text**: clearly replaced rules are dropped automatically; anything uncertain goes to Paul as a short yes/no list. Approved.
4. **The eight planning areas**: Risk, RA, Investment, RGAR, EGAR, Medical Aid, Will, Short-Term. "Other" (debt, children, health, general) is shown only when something notable was said.
5. **Headings**: each of the eight is its own heading, in that order, in the Planner note and the PDF, shown only when discussed or still open, with one line naming the ones not discussed.
6. **S16 approved** (program drives the job step by step), on condition that it works in a real chat first.
7. **Teams message wording (Paul, 29/10/2026: "it depends on whether it is a Prospect or a Review client")**: the `fact-find-summary` wording, with `(Review Client)` or `(Prospect)` after the name, decided from where the client's folder sits (Company - WR Clients\Paul Kafentzis (Client Files) = Review Client; Company - Paul\New Business = Prospect; ask Paul if unclear), and a plain count (1st, 2nd, 3rd) of the Teams meetings with that client.
8. **WhatsApp calls also notify Sitamah (Paul, 29/10/2026: "Yes")**: same message, with "WhatsApp Call Completed" in place of "Teams Appointment Completed". Assumption stated to Paul: the count (1st, 2nd, 3rd) is every meeting and call on file plus this one; built in until he says otherwise. A WhatsApp call is a call on WhatsApp instead of a Teams meeting; there is no Teams transcript, so Paul gives his own recap.
9. **The short true stories ("named precedents") inside the rules stay (Paul, 29/10/2026: "Keep")**: they help Claude recognise the mistake. Names are removed from them (S11).
10. **Go for the Teams transcript skill given (29/10/2026).** The NEXT skill does not start until Paul has trialled this one and says go.
11. **The five removals (Paul, 29/10/2026: "Yes to removals 1-4, keep the table")**: the long change history, the two worked examples with real client details, old rules 1 and 9, and the dated attributions after headings are removed for good; the 21-point checklist stays as a table. Nothing further to change in the skill.

12. **Structure after the first real-case trial (Paul, 29/10/2026).** Planner note: per area 1 to 3 one-line bullets (at most 20 words), the actions for now (at most 8), nothing else; the PDF: at most 4 bullets per area (45 words each), two pages at most, the actions for now under Action Points, the waiting ones under Coming up with their trigger, Next Steps for the client only. Paul's answers on the ten actions of his trial: follow up with a third party (yes), get full policy schedules (yes), get credit-life details (yes), get updated quotes (yes); cession (after the policy is issued, so later); remove: what-if question to a provider, asking the clients what they want to do about credit life, cancelling credit life, sending the updated quotes ("she will do that in another step"), setting up the next appointment. The message to Sitamah is shown with the outputs in one reply with one question.
13. **Action points (Sitamah's checklist) must be thought about intelligently (Paul, 29/10/2026).** Chronological order (earliest deadline first), then logical order (what must happen first comes first); sift out what is not relevant and show what was left out; and when the skill is not sure it ASKS Paul instead of deciding. Paul said to forget the separate skill `planner-interim-procedure`: the rules apply to this skill's action points only.
14. **The new Fact Find form (Paul, 02/11/2026).** Its data file is the first and primary source of both Fact Find skills (`ff-population-transcript`, `fact-find-summary`), then the Teams transcript, the latest Overview and the client's other documents. The original naming stays: `Fact Find (Audio to Text) - DD.MM.YYYY - Name Surname`. The Dread Disease ABI is **3% always unless Paul states otherwise** (this replaces the 5% of 15/10/2026; the form's preset is 3%). The skills check the form's schema version every run. The form's "parking list" of facts it heard but did not place is deliberate (only crucial facts go in a field; the rest is in the recorded Teams call, so the transcript supplies the extra context): the skills do not process that list. Paul corrects a wrong field in the form himself: the skills use the saved value. **The follow-up appointment IS an action for Sitamah at every meeting** (she books it for a physical appointment, or sends the Teams meeting request): one line in the Actions list. This REVERSES the 29/10/2026 removal of "Sitamah to set up another evening appointment" in the Teams transcript skill, which must be changed. **The company look-up text** (the form's web look-up of "what does the company do") is checked by the skill: text that talks to the reader (for example "try again", "I found no...", a question, very long) is thrown out and replaced from the transcript; a clean look-up that nobody confirmed is shown marked "web look-up, not confirmed with the client"; Paul is told the form's look-up should say "to verify" and never "confirmed" (to fix in the form). "Number of years": Paul says the form has been corrected; the skills can still work it out from a year (meeting year minus the year, shown as "since YYYY").

15. **Fact Find Transcript layout (Paul, 02/11/2026, question 3 of the ff-population-transcript questions):** fixed 11 sections plus Next Steps, drawn by a program in the same order every time (the new form's sections: Client Info, Occupation, Income & Household, Existing Cover & Retirement, Investments, Medical/Will/Short-Term, Debts, Children, Health, Advisor Actions, Risk Calculation). The form's schema-version check stops the skill if the form's layout changes, and the skill is then updated once.

16. **ff-population-transcript: look, missing form file, laptop window (Paul, 02/11/2026, questions 4 to 6):** (a) the look of the Fact Find Transcript PDF stays exactly as now: Aptos 12pt, navy headings (1F3A5F), light-blue label column (EAF1F8), one fact per line, no page numbers, and Paul checks one sample; (b) if the form's data file is missing for a meeting (searched on all three routes), the skill STOPS and ASKS Paul whether to use the filled-in Manual Fact Find PDF or the transcript alone, and records his words; (c) the 8:45am laptop window is dropped: every run tries the computer first, then Microsoft 365, then Zapier, logs each try, and never skips or comments because of the time of day.

17. **WITHDRAWN (Paul, 02/11/2026, same day) - a misunderstanding of mine.** I had recorded that the form's own saved PDF IS the Fact Find and that the skill builds no second PDF. Paul corrected me: the pipeline is (1) the form saves its `Fact Find (Audio to Text)` PDF (and data file) into the client's folder; (2) `ff-population-transcript` takes that saved file as its FIRST source, adds the Teams transcript and the other sources (Overview, the client's other documents) and COMBINES them into the completed Fact Find, **which is a saved report in its own right** (the Fact Find Transcript PDF, saved into the client's folder); (3) `fact-find-summary` takes the report that the population skill produced and creates the Summary PDF. So the form's PDF is an INPUT, the combining stays, and decisions 15 and 16 stand. Lesson: before dropping a deliverable, say it back to Paul; before building one, ask whether it is still needed.

18. **No bigger rebuild of the two Fact Find skills for now (Paul, 02/11/2026).** The interim text update (decision 14) is all he wants now: he uploads it when he chooses and runs it on a real client first. The program-driven rebuild of `ff-population-transcript` waits until a real run shows what is needed. The helper's unfinished work was removed from the working tree (kept in git history: commit 62cb4e1).

19. **The 13-ingredient template is APPROVED as it is (Paul, 02/11/2026).** `SKILL-TEMPLATE.md` is the measure for every skill from now on. Changes to it are added only when Paul asks. The structure questions for each next skill are asked when Paul names that skill and says go (S15).

20. **Build the program for `ff-population-transcript` now (Paul, 02/11/2026, after he asked whether the two Fact Find skills had been verified).** This SUPERSEDES decision 18. Order: `ff-population-transcript` first, then `fact-find-summary` (one at a time, S15). Paul's words: "Make sure it executes as intended", so the build ends with a full end-to-end run of the program on made-up data, the checker, the tests, lint and the rule-by-rule check, and an independent review, and the real test is still a run on a real client. Decisions 15 and 16 stand (fixed 11-section report built by program, look unchanged, stop and ask when the form file is missing, no 8:45am rule). The helper's unfinished work was restored from commit 62cb4e1 and was continued. **STATUS 03/11/2026: the program-driven `ff-population-transcript` is BUILT** (step driver, checker, PDF drawn by program, tests on invented data, lint, inventory 0 unaccounted) and was attacked by an independent reader in four rounds (fixes after each, every attack now a test). It is NOT uploaded and NOT live. The real test is still a run on a real client. What no program can prove is listed in `ff-population-transcript/history/CHANGES-FOR-PAUL.md` (the chat typing Paul's words, chat-made text copies, a doctored Teams copy, the truth of a written reason, request lines with none of the listed words). The next skill is `fact-find-summary`, when Paul says go.

21. **No helpers and no more test rounds (Paul, 03/11/2026).** After six fix-and-review rounds with helpers on `ff-population-transcript` Paul said: "we've done enough tests", "you have eaten all my tokens. No more helpers." Claude Code does NOT start helpers, subagents or independent reviewers unless Paul asks in his own words, and does not run review loops. One build, one lint, one full test run, one package per skill; say roughly how big a job is first. The finished `ff-population-transcript` (round 5, commit d434670) goes to packaging as it is; the unproven round 6 is set aside (commit d3cbb19). The real test is a run on a real client. See `CHAT-NOTES.md`.

22. **Operation Skill Restructure (Paul, 03/11/2026).** The fixed procedure applied to every skill, one at a time: Phase A read and analyse (flaws, duplications, 13-ingredient score, Findings Report and yes/no list), Phase B plan (one route, Paul approves), Phase C build in one pass, Phase D prove with ONE test only (lint, rule-by-rule check, one end-to-end test on invented data), Phase E package and hand over, Phase F close out and ask Paul for the next skill. No helpers. Saved in `OPERATION-SKILL-RESTRUCTURE.md` (with a Progress table) and pointed to from CLAUDE.md.

23. **Short audit reports in the chat (Paul, 03/11/2026).** After a skill has run, the audit posted in the chat is SHORT: one-liners in point form, each with a green tick or a red cross, and one closing line for what is only attested. The program writes that short audit and keeps the full record on disk. Applies to every skill built under Operation Skill Restructure; the Teams and Fact Find Transcript skills (built earlier) keep their long printout until they are revisited.

**Still open**
1. Which skill comes after the Teams transcript skill (Paul names it and says go; one skill at a time, S15)?
2. (Closed 30/10/2026) The Teams transcript skill is LIVE: Paul uploaded the 17:53 build (v34), ran it on real meetings and confirmed.

## 8. Known gaps found in the Teams transcript skill (to fix in its rewrite)

- Step 3 says "eight areas" but lists seven. Resolved: the eight are Risk, RA, Investment, RGAR, EGAR, Medical Aid, Will, Short-Term (decision 4).
- No Teams message to Sitamah deliverable. Resolved: add the Step 8 message from `ff-population-transcript` (decision 2).
- **Missing page template.** `ff-population-transcript` Step 7b says to use the Planner page template and publishing steps in this skill's Output 1 section. They are not there. Each chat invents its own page. The rewrite generates the page by program.
- **Teams message wording differs between two skills.** Paul decided on 29/10/2026 that the label (Review Client / Prospect) belongs in the message. `fact-find-summary` already has it; `ff-population-transcript` Step 8 does not and still says `Review Teams Appointment` for a review. To be aligned when that skill is converted. Both send it for a first meeting, "once per meeting"; the Teams transcript skill records `already_sent`.
- `ff-population-transcript` Step 7b still names the old combined Planner-note headings (Retirement incl. RGAR, Investment incl. EGAR, Medical Aid / Will / Short-Term). To be aligned when that skill is converted.
- Other skills already carry scripts: `alpha-bank-statements`, `complete-applications-skill`, `fact-find-summary`, `ff-population-transcript` (JavaScript), `om-tax-free-skill`, `rgar-skill`, `wr-roa-builder`, `wr-sroa-builder`. The standard must work with these; it does not start from zero. Several treat the script as a template Claude may adapt, which the new standard does not allow during a run.
- Examples contain real client names (S11).
- Change history is longer than the rules and sits at the top of the file (S2, S5).
- The "first-meeting exception" (06.10.26) was reversed on 07.10.26 but its backstory is still in the text.

### Found in Paul's first real-case trial (29/10/2026, two clients of one household; no client data kept here)
- **Planner notes far too long.** Paul's original rule (approved 06/10/2026) was 1 to 4 short bullets per area and a PDF of two pages at most. The rebuild made ONE set of bullets feed both the Planner note and the PDF and put no length limit or check on either, so the note carried everything (one area had 7 bullets of 40 to 70 words each, packed with figures). The checker proved nothing was missed, never that it was short. Paul wants the Planner note to give only: which areas were discussed, one-line bullets, and the relevant action points.
- **Action points were not sorted.** Paul: some are for now, some are not for the here and now, some should not be actions at all. The program checks only that an action has a source. The old credit-life and cession rules (07/10 and 06/10) were copied literally and produce actions that are later steps ("cancel the credit life once the new policy is in force", "arrange the cession" while the quote is still only pending) or the client's own decision ("ask the clients what they want to do"). The PDF also let Paul own a next step ("Paul will send the updated quotes") next to a Sitamah action to send the same quotes.
- **The Teams message to Sitamah was not offered.** In the program it is the very last step, shown only after Paul has approved the other deliverables; Paul expected it together with them (as `fact-find-summary` does). The end of that chat was not seen, so whether the step was skipped or never reached is not known.
- **Status: BUILT (29/10/2026) after Paul agreed the structure and sorted the ten actions (decision 12).** Limits live in `wrlib.LIMITS` and are enforced by group L of `verify.py`; the Teams message is shown with the outputs. Waiting for Paul to see a sample and upload; the next real run is the test.

## 8b. ff-population-transcript: findings of the study (30/10/2026, no client data kept here)

Purpose: builds the completed WR Fact Find (11 sections, v3.0 layout) as a PDF from the Fact Find (Audio to Text) file (primary), the Teams transcript and the latest Overview; finds contact details and the lead source; hands over to `fact-find-summary` and to the Planner note; saves into the client's folder; notifies Sitamah. Used after the first meeting with a prospect or a review client.
- **Strengths:** clear source order with "Audio to Text wins, differences flagged"; "Not discussed is a claim"; totals to the cent; policy numbers from the schedule; standing ABIs; quote requests must name insurer and New Business or Servicing (no default); save proven by listing the folder (size equal); spouse rules; lead-source search in Outlook; a delivery gate.
- **Weaknesses:** (1) 300 lines, 60 KB, nothing enforced by a program: no step driver, no reading lock, no source trace, a 13-point re-check done by hand. (2) `scripts/build_fact_find.js` still holds a REAL client's name, ID number, emails and income (S11 breach, and a cross-client leak risk because the chat must overwrite every row by hand). (3) The script and `references/ff-field-map.md` still follow the retired v2.0 layout while the skill says the layout is v3.0. (4) Step 7b names the old Planner headings and points at a text section of the Teams skill that no longer exists (it is a program now). (5) Step 8 (Teams message) has no (Review Client)/(Prospect) label, says `Review Teams Appointment`, and is sent only after everything is approved (the flaw that stopped the message being offered); `fact-find-summary` has the same step, so two skills own the Planner note and the message. (6) Rules 1 and 9 are the old method (reload after compression; the Update skill card). (7) The stamp is typed by hand. (8) Dated attributions and a changelog at the top.
- **Not checked:** the skill was read, not run; the script was not run; no real Audio to Text file or finished Fact Find was seen.

## 8c. The new Fact Find form (studied 02/11/2026; no client data kept here)

Where: `Company - Paul > Claude > Fact Find Documents > WR Fact Find - ZIP > WR Fact Find` (SharePoint, read through the Microsoft 365 connector; route 1, the computer, was not connected). Voice logs sit in `Fact Find Documents > Save Log Reports`.
- **What it is:** a Chrome page (index.html + js, css, assets, vendor; started by `Start Fact Find.bat` / `FactFindServer.ps1`). Paul uses it in the meeting: Listen (microphone: Whisper on the computer, Chrome speech, or OpenAI transcription), Voice mode (a Claude model decides which box each heard fact belongs in), meeting timer, Save, Save as, Preview PDF, Save PDF, progress counts (filled, to verify, not asked) and checks. App version 3.0, October 2026.
- **What it saves:** (1) the Fact Find data file (JSON, `app: wr-fact-find`, `schema: 3.0`): `f` = every field as `{v, st}` with st `confirmed`, `preset`, `empty` (older files also `heard`, `verify`); `l` = repeating lists (risk, grp, ret_ra, ret_pp, inv, bizpol, shares, debts, kids, bfred, redq, raq, invq) as rows `{d, st}`; `sum` = a short summary per area (life, ra, rgar, inv, egar, med, will, st); `pa`/`pa_actions` = an action list drafted by Claude; `unplaced` = facts heard but not placed in any box, with the reason; cost counters. (2) A PDF (Save PDF). (3) A voice log per session (lines heard, who spoke, what the page did with each).
- **File names seen:** `Fact Find (Audio to Text) - DD.MM.YYYY - Name Surname.json` (client folder), `Fact Find - DD.MM.YYYY - Name Surname.json` (new form, test client), and Paul's planned `Fact Find (Voice to Text) - dd.mm.yy - (name surname)`. No "Voice to Text" file exists yet. So the skills must find the file by content (`app` = `wr-fact-find`), not by name.
- **Findings to handle in the skills:** `unplaced` facts must be read and handled, not ignored; a heard answer can lose to an older confirmed one; the form's own action list breaks three settled rules (it names the client where Sitamah is the owner, includes setting up the next appointment, and asks the client things); a preset Dread Disease ABI of 3% differs from the standing 5%; the company look-up wrote the model's own chatter into the "what does the company do" field and marked it confirmed; "Number of years" held a year; a trailing space in the first name; keys are kept in the browser as plain text and the page says its address is shared with other pages under the same GitHub Pages site; the form's `.js` files were changed today, so the schema version must be checked each run.
- **Not seen:** `schema.js` and the other `.js`, `.bat` and `.ps1` files (the connector cannot read those types), the form's PDF, any real "Voice to Text" file.

## 9. Skill tracker

| Skill | Status |
|---|---|
| client-teams-transcript-skill | REBUILT to these standards (step driver, reading lock, client-file and access logs, Planner page, PDF, Sitamah Teams message (Teams meetings and WhatsApp calls), PASS/FAIL checklist; 226 tests, hardened after an independent review; nothing from the old skill lost without a record). The Sitamah message also covers WhatsApp calls (Paul's yes). Uploaded 29/10/2026 by a Claude-in-Chrome chat as version v33 (reported by that chat). First real-case trial found the notes too long, the actions unsorted and the Teams message not offered; REBUILT the same day to Paul's answers (short Planner note, sorted and ordered actions, asks when unsure, message shown with the outputs); uploaded 30/10/2026 UTC by a Claude-in-Chrome chat as v34 (Last updated 2026-10-29 17:53; reported by that chat, its replace-box line counts 65 to 66 match the files); **LIVE: Paul confirmed on 30/10/2026 ("Yes it is live")** after running the 17:53 build (v34) on real meetings; the old version is v33 in its version history. **02/11/2026:** the 15:55 build (follow-up appointment is an action for Sitamah; this skill makes the first-meeting Planner note and Sitamah message; 228 tests) uploaded by a Claude-in-Chrome chat as **v35** (reported by that chat: Last updated 2026-11-02 15:55, 21 files, replace-box line counts 66 to 67, which match the zips' SKILL.md plus one line; the before and after test chats answered as expected); **LIVE: Paul confirmed 03/11/2026 ("Yes, v35 is live")** (v34 stays in the version history as the backup) |
| client-pipeline-board, complete-applications-skill, wr-roa-builder, wr-sroa-builder, rgar-skill, om-tax-free-skill, life-policy-schedule-analyzer, client-review-notes, client-transcript-download, teams-meeting-setup-skill, outlook-emails-skill, cameron-short-term-skill, advicetech-website-knowledge, alpha-bank-statements, nedbank-current-account-categorization, paul-email-signature, correcting-skills, master-skill-template | Not started |
| ff-population-transcript | **PROGRAM-DRIVEN BUILD DONE 03/11/2026 (decision 20)**: step driver `scripts/run.py` (16 steps), checker `scripts/verify.py`, the form's data file and saved PDF read by program (schema 3.0 checked), the Fact Find Transcript PDF drawn by program in the fixed 11 sections (look unchanged; Carlito stands in where Aptos is missing and the checker says so), reading lock vendored from the Teams skill, claims and covers checked, Teams hand-over proven against the Teams program's own records. Tests on invented data (Pat Samplecase, Robin Testcase), every reviewer attack kept as a test, mutation runs. Inventory against the 28/10 text: 568 sentences, 391 kept, 68 reworded, 109 dropped on record, 0 unaccounted. Four independent review rounds; remaining limits are listed for Paul in `history/CHANGES-FOR-PAUL.md`. Questions waiting for Paul are in the same file (Yes/No list). Not run in a real chat. Packaged 03/11/2026 (zip `releases/ff-population-transcript-20261103-0612.zip`, lint PASS, made with `--skip-tests` on Paul's instruction; the end-to-end journey test passed on the unpacked zip); UPLOADED as v33 by a Chrome chat on 03/11/2026 (reported: before v32, 3 files, "Last updated 2026-10-28 10:45"; after v33, 24 files, still one entry, "Last updated 2026-11-03 06:12" and "Index", test chat correct; replace box 296 lines to 76 lines, the rest moved into the program and references, inventory 0 unaccounted); NOT confirmed live by Paul (he runs it on a real client first). The upload replaced the older version, which stays in his version history. Paul's real upload subfolder is `ff-population-transcript-skill` (with `-skill`). Scorecard in SKILL-TEMPLATE.md |
| fact-find-summary | **PROGRAM-DRIVEN BUILD DONE 03/11/2026 (Operation Skill Restructure, decision 22)**. A program reads the Fact Find Transcript PDF (`scripts/ffread.py`, needs `pdfplumber`), composes the nine sections with totals and follow-up owners (Cameron, CL, Valerie, Lizelle; Lizelle replaces Martin), draws an A4 PDF and a checker prints a SHORT audit of green ticks and red crosses. The Planner note and the Sitamah message left this skill (the Teams skill owns them). Rule-by-rule check: 392 old rules, 13 kept, 93 reworded, 286 dropped on record, 0 unaccounted. Lint PASS. ONE end-to-end test on invented data passed on the source and on the unpacked zip. Zip: `releases/fact-find-summary-20261103-0941.zip` (15 files, 38,533 bytes). The older interim text-update zip and brief are SUPERSEDED: do not upload them. UPLOADED as v18 on 03/11/2026 by a Chrome chat (reported by that chat, pasted by Paul): before = v17, 2 files, "Last Updated: 28 October 2026, 10:58"; the first replace box was a different one ("This overwrites fact-find-summary with this file. What it overwrites can't be restored afterwards."), so the chat stopped; Paul saved a backup zip of the old 2 files and approved; the second box read "This saves a new version of fact-find-summary. Earlier versions stay available in the skill's version history. Current: 218 lines - This file: 67 lines."; after = v18, 15 files, still ONE entry (31 skills), "Last updated: 2026-11-03 09:41 (Athens time)" and first section "Index" (the test chat answered correctly). NOT confirmed live by Paul (he runs it on a real client first). Yes/no list for Paul: `fact-find-summary/history/CHANGES-FOR-PAUL.md`. Never say live before Paul confirms. The earlier interim text update of both Fact Find skills (02/11/2026) is superseded for `fact-find-summary`; the interim `ff-population-transcript` text update is superseded by the uploaded v33. |
| client-transcript-download | **PROGRAM-DRIVEN BUILD DONE 03/11/2026 (Operation Skill Restructure)**. A program drives 6 steps (identify, fetch, check, name, save, final): fetch routes Microsoft 365 then Zapier then Claude in Chrome, every try logged (the connector holds OnlineMeetingTranscript.Read.All; unproven until one real try); the transcript must be complete (last time stamp within 2 minutes of the meeting length, no gap over 10 minutes); the file name is derived; a text transcript from the connector is written as a .docx; the save is checked (client's own 2. Fact Find folder, listed size equals local, nothing overwritten); a SHORT audit of ticks and crosses ends the job and names the next skill. Rule-by-rule check: 105 old rules, 24 kept, 37 reworded, 44 dropped on record, 0 unaccounted. Lint PASS. Zip `releases/client-transcript-download-20261103-1125.zip` (11 files, 24,408 bytes). Backup of the old live file made (outside the repo). UPLOADED as v5 on 03/11/2026 by a Chrome chat (reported by that chat, pasted by Paul): before = v4, 1 file, "Last updated: 2026-10-14 14:41"; replace box "This saves a new version of client-transcript-download. Earlier versions stay available in the skill's version history. Current: 68 lines - This file: 60 lines."; after = v5, 11 files, still ONE entry (31 skills), "Last updated: 2026-11-03 11:25 (Athens time)" and first section "Index" (the test chat answered correctly; it labelled the loaded skill "(plugin)", which the before chat did not). NOT confirmed live by Paul (he runs it on a real client first). The first real run also decides which fetch route works (Microsoft 365, Zapier or Chrome). Yes/no list (2 questions): `client-transcript-download/history/CHANGES-FOR-PAUL.md`. Never say live before Paul confirms. |
| teams-meeting-setup-skill | **PROGRAM-DRIVEN BUILD DONE 03/11/2026 (Operation Skill Restructure)**. A program drives 7 steps (find client, facts, build, show, send, log, final): it reads the client's name and personal email from the Fact Find Transcript PDF (routes computer, Microsoft 365, Zapier, every try logged), builds the whole invite (subject in the fixed order, Africa/Johannesburg on start and end, exactly 1 hour, the client only, Teams on, date-aware opening line, no link or signature), shows it with the message to Sitamah and ONE question, and will not take Paul's yes unless he was shown exactly this invite; the checker compares what the Microsoft 365 tool returned with what he approved and prints a SHORT audit (ticks and crosses). A reschedule updates the existing event in place. Rule-by-rule check: 154 old sentences, 6 kept, 99 reworded, 49 dropped on record, 0 unaccounted. Zip `releases/teams-meeting-setup-skill-20261103-1209.zip` (13 files). 5 yes/no questions in `teams-meeting-setup-skill/history/CHANGES-FOR-PAUL.md`. UPLOADED as v8 on 03/11/2026 (reported by a Chrome chat; v7 before, 13 files, test chat correct); NOT confirmed live by Paul. |
| outlook-emails-skill | **PROGRAM-DRIVEN BUILD DONE 03/11/2026 (Operation Skill Restructure)**. A program drives 6 steps (email, plan, show, create, readback, final): it records the email with its source, builds two scheduled-task files (an hourly weekday watcher, 08:00 to 17:00 South African time, that drops senders who replied and stops by itself after 5 business days; a one-time silence flag at 09:00 Athens time on the 2nd business day), shows the plan with no question (standing rule), and the checker compares what `list_triggers` shows with the plan and prints a SHORT audit. Both checks start a fresh chat and may use the Microsoft 365 connector only. Rule-by-rule check: 94 old sentences, 3 kept, 46 reworded, 45 dropped on record, 0 unaccounted. Zip `releases/outlook-emails-skill-20261103-1301.zip` (12 files). 3 yes/no questions in `outlook-emails-skill/history/CHANGES-FOR-PAUL.md`. The scheduled-task tool's acceptance of the settings is unproven until one real tracked email. UPLOADED as v5 on 03/11/2026 (reported by a Chrome chat; v4 before, 12 files, test chat correct); NOT confirmed live by Paul. |
| astute-summary-report-skill | **PROGRAM-DRIVEN BUILD DONE 03/11/2026 (Operation Skill Restructure)**. A program drives 8 steps (locate, read, data, products, flags, build, save, final): the report is served page by page (reading lock); the chat enters the data in a fixed layout and the program checks every policy number, figure, date and name against the report's own text (pdfplumber), adds up the totals, decides the section from the Astute status, raises the computable flags, draws the landscape A4 PDF (reportlab) in the old look and reads it back; the file name is derived and never overwritten ((2), (3)); a numbered flag list and a SHORT audit end the job. Rule-by-rule check: 173 old sentences, 27 kept, 103 reworded, 43 dropped on record, 0 unaccounted. Zip `releases/astute-summary-report-skill-20261103-1350.zip` (15 files; needs pdfplumber, reportlab, pdftoppm in the chat). 4 yes/no questions in `astute-summary-report-skill/history/CHANGES-FOR-PAUL.md`. No real Astute report was ever seen: the data layout is a guess from the skill text, so the first real run may need one fix. UPLOADED as v2 on 03/11/2026 (reported by a Chrome chat; v1 before, 15 files, test chat correct); NOT confirmed live by Paul. |
| wr-roa-builder | **PROGRAM-DRIVEN BUILD DONE 03/11/2026 (Operation Skill Restructure)**. A program drives 9 steps (locate, read, answers, confirm, email, build, check, save, final): documents are served page by page; the chat enters the setup answers with their sources and the program checks every name, ID and figure against the documents' text and every dropdown choice against the template's own lists; the program picks the Risk reason text from the response bank word for word (custom wording marked); Paul gets ONE confirmation table and nothing is built before his yes; the two scripts (`build_roa.py`, `embed_email_images.py`) keep their logic and are fixed during a run; for Retirement/Investment the client's own reply email page is embedded as before (font rewrite to 15 pt, wkhtmltopdf at the fixed geometry, pages before 'Investment Planning' or 'POLICY REPLACEMENT') and the first rendered page must open on the client's reply; the finished .docx is reopened and checked (15 or 18 checks); the file name is derived and a file is never overwritten without Paul's yes; the 'ROA as HTML' delivery path is removed; all client data removed. Rule-by-rule check: 1,055 old sentences, 26 kept, 940 moved or reworded (section-level reasons), 89 dropped on record, 0 unaccounted. Zip `releases/wr-roa-builder-20261103-1437.zip` (22 files; needs pdfplumber, python-docx, lxml, Pillow, zip/unzip, pdftoppm, and wkhtmltopdf for Retirement/Investment; LibreOffice for the page images). 5 yes/no questions in `wr-roa-builder/history/CHANGES-FOR-PAUL.md`. The real wkhtmltopdf could not be installed or run where this was built: its real render of a real email is unproven until the first real Retirement or Investment ROA (the test used a stand-in that enforces the fixed command line). UPLOADED as v7 on 03/11/2026 (reported by a Chrome chat; v6 before, 22 files, test chat correct); NOT confirmed live by Paul. |
| wr-sroa-builder | **PROGRAM-DRIVEN BUILD DONE 03/11/2026 (Operation Skill Restructure)**. A program drives 8 steps (locate, read, answers, confirm, build, check, save, final): documents are served page by page (only the policy's own pages of an Owner's Manual); the chat enters the answers and the program checks every name, ID, CP number, date and old/new figure against the right document's text, works out "No change", enforces the R20 premium label, shows one confirmation table (sha-bound yes), builds with the fixed `build_sroa.py`, reads the PDF back (`pdfcheck.py`), derives the file name and saves into the Servicing folder; the SHORT audit is printed. One test (`tests/test_journey.py`, invented Pat Samplecase, BrightRock grouped case and a flat case) passes on the source and on the unpacked zip. Lint PASS, inventory 0 unaccounted. Packaged `releases/wr-sroa-builder-20261103-1515.zip`; UPLOADED as v5 (reported by a Chrome chat, 03/11/2026; v4 before, 6 files to 17 files; test chat correct); NOT confirmed live. Paul's yes/no list: `wr-sroa-builder/history/CHANGES-FOR-PAUL.md`. |
| om-tax-free-skill | **PROGRAM-DRIVEN BUILD DONE 03/11/2026 (Operation Skill Restructure)**. A program drives 9 steps (locate, read, answers, confirm, build, save, draft, message, final): documents served page by page; every name, age, employer, income, contribution, start date, fund, allocation and fee is checked against the right document's text (percentages exact), the fee total is added up; a child's plan, a lump sum or a conflict stops the run; one confirmation table (sha-bound yes, with the subject and the Teams message); the fixed template is filled by program (the broken placeholder check of the old skill is replaced); the draft read-back and the posted-message read-back are checked; the Teams message goes only after Paul's yes and a checked draft. One test (`tests/test_journey.py`, invented Pat Samplecase) passes on the source and on the unpacked zip. Lint PASS, inventory 0 unaccounted. Packaged `releases/om-tax-free-skill-20261103-1613.zip`; UPLOADED as v11 (reported by a Chrome chat, 03/11/2026; v10 before, 4 files to 19 files; test chat correct); NOT confirmed live. Open: signature once or twice (settings.json), tax facts not verified, Paul's yes/no list in `om-tax-free-skill/history/CHANGES-FOR-PAUL.md`. |
| rgar-skill | **PROGRAM-DRIVEN BUILD DONE 03/11/2026 (Operation Skill Restructure)**. A program drives 9 steps (locate, read, answers, confirm, build, save, draft, message, final): only the RGAR report and the Fact Find Summary are needed (without a Fact Find Summary the skill stops and asks Paul); every RGAR figure is checked against the report's text, the net target must be the first figure after its label in the Fact Find Summary, the age must agree with the RGAR's date of birth, R 0 stops the run, the shortfall dates and weekdays are computed, the fixed template is filled by program, the draft and posted-message read-backs are checked, the RGAR copy must be in the folder listing; the Teams message goes through Zapier only after Paul's yes and a checked draft. One test (`tests/test_journey.py`, invented Pat Samplecase) passes on the source and on the unpacked zip. Lint PASS, inventory 0 unaccounted. Packaged `releases/rgar-skill-20261103-1727.zip`; UPLOADED as v10 (reported by a Chrome chat, 04/11/2026; v9 before, 4 files to 19 files; test chat correct); NOT confirmed live. Open: signature once or twice (settings.json), Paul's yes/no list in `rgar-skill/history/CHANGES-FOR-PAUL.md`. |
| om-optimal-ra-proposal | **PROGRAM-DRIVEN BUILD DONE 04/11/2026 (Operation Skill Restructure)**. A program drives 10 steps (locate, read, answers, tax, confirm, build, save, draft, message, final): documents served page by page; every figure, name, date, fund, allocation and fee is checked against the right document's text; **the program runs the Tax Reform Tool itself** (`scripts/taxtool.py`: the workbook copy is recalculated in LibreOffice for four scenarios, every figure is recomputed independently from `assets/tax_facts.json` and a difference stops the run; tax-year guard from 01/03/2027); audit checks 1 to 3 and 6 to 8 proved, 4 and 5 computed and flagged with both figures; the blended fee, the weekdays, the three tables' rows (fund rows in all three), the scenario sentence, the orange messages and the bar chart come from the program; the fixed templates (fixed once: 'You are working at', placeholders added, fees read from the quote, any number of funds) are filled by program; the separate Lump Sum Investment email is a second run (`--document lump_sum`: Section 14 net values or voluntary with Paul's tax note); the Teams message goes through Zapier after Paul's yes and a checked draft. Lint PASS, inventory 834 rules / 0 unaccounted, ONE test passed on the source and on the unpacked zip (real LibreOffice run). Zip `releases/om-optimal-ra-proposal-20261104-0931.zip` (25 files) + upload brief (real folder `om-optimal-ra-proposal-skill`; UPLOADED as v7 on 04/11/2026 by a Chrome chat, reported; NOT confirmed live). Open: signature once or twice (settings.json); Paul's 8 Yes/No questions (`om-optimal-ra-proposal/history/CHANGES-FOR-PAUL.md`). |
| investment-comparisons-skill | **PROGRAM-DRIVEN BUILD DONE 04/11/2026 (Operation Skill Restructure)**. A program drives 10 steps (locate, read, answers, check, confirm, build, save, draft, message, final): the quotes (2 to 6 providers), the Fact Find and each fund's current fact sheet (fetched from the web by the chat, SAVED as text with its address and date) are served page by page; every fee, premium, term, fund, allocation, loyalty figure, fund-sheet figure and date is checked against the right document's text (percentages exact and next to their label); a blended or total fee line and a quote that is not the product are refused; descriptions copied from the fact sheet are refused; the program works out the comparison (apples-to-apples across the quotes: a mismatch stops the run unless Paul says to go on and the email then labels it; fee totals added up as shown; stale and missing fact sheets; the Tax-Free room; risk-fit flags for Paul only); the four fixed tables are built from a template with a plain-English intro each, every fee row explained, each fund's own fact sheet date, a 'Things to know' box only when something must be flagged, the optional parts only when Paul asks; checks: no EAC headline, every industry term explained, tables in order; the Teams message goes through Zapier after Paul's yes and a checked draft. Lint PASS, inventory 387 rules / 0 unaccounted, ONE test passed on the source and on the unpacked zip. Zip `releases/investment-comparisons-skill-20261104-1014.zip` (22 files) + upload brief (folder `investment-comparisons-skill` confirmed by Paul; UPLOADED as v6 on 04/11/2026 by a Chrome chat, reported; NOT confirmed live). Open: Tax-Free limits (`assets/tax_facts.json` says confirmed false: R36,000 in the old text vs R46,000 in `om-tax-free-skill`: a Tax-Free comparison stops and asks until Paul confirms), signature once or twice, his Yes/No questions (`investment-comparisons-skill/history/CHANGES-FOR-PAUL.md`), no real quote or fact sheet ever seen, the web fetch of fact sheets unproven. |
| life-insurer-comparison | **PROGRAM-DRIVEN BUILD DONE 04/11/2026 (Operation Skill Restructure)**. A program drives 12 steps (locate, read, scope, research, answers, check, confirm, build, save, draft, message, final): the quotes, schedules, the client's notes, the Fact Find Summary and each insurer's own guide (fetched from the web by the chat, SAVED as text with its address and date) are served page by page; the benefit scope is proved by a verbatim line of the client's own notes for every category (or Paul's words) and every out-of-scope word is scanned over the letter and the email; every figure is entered with the verbatim line of its document and the program proves the line is in the text and the figure in the line; the premium escalation is worked out from the printed rand figures (calculated percentages, anchor, outliers, printed against calculated); the letter is drawn from a fixed template; the covering email is plain and made with the Microsoft 365 draft tool (the Exchange rule adds Paul's signature once; Paul attaches the HTML by hand); the Teams message goes through Zapier after Paul's yes and a checked draft. Lint PASS, inventory 953 rules / 0 unaccounted, ONE test passed on the source and on the unpacked zip. Zip `releases/life-insurer-comparison-20261104-1127.zip` (23 files). UPLOADED as v10 on 04/11/2026 by a Chrome chat (reported by that chat, pasted by Paul; the chat had the brief): before = v9 (Oct 14), 1 file, 31 skills, ON, test answer "2026-10-14 15:14 Athens time (EEST)" and "Index"; replace box "Replace life-insurer-comparison skill? This saves a new version of life-insurer-comparison. Earlier versions stay available in the skill's version history. Current: 1,072 lines, This file: 62 lines." (it named only this skill); after = v10, 23 files, still ONE entry (31 skills), ON, test answer "Last updated: 2026-11-04 11:27 (Athens time)" and "Index" (correct). The zip (80,523 bytes) was staged from Claude Skills - New, no manual file pick. Unusual: both test chats labelled the skill "(plugin)"; **the real folder is `life-insurer-comparison-skill` (with `-skill`), although Paul confirmed `life-insurer-comparison`; the brief's path was wrong but the chat found the real folder** (the second time: ask Paul to look at the folder name in Explorer, not answer from memory). Nothing deleted; the old versions hold no client name. NOT confirmed live by Paul (he runs it on a real client first; I have never seen a real insurer schedule, quote or guide, so the first real run may need one fix). The HTML letter is attached by Paul by hand (`attach_by` paul); the covering email is made with the Microsoft 365 draft tool and the Exchange rule adds his signature once; the Teams message goes through Zapier after his yes and a checked draft. |
| planner-interim-procedure | FORGET (Paul, 29/10/2026): an interim skill, retired with AdviceTech. Do not convert it, consider it, or build rules for it |
| ff-to-ff-populate | FORGET (Paul, 02/11/2026): he runs it by hand when needed. Do not convert it, build on it, or count on its Audio to Text file being there |

## 10. Changelog (last 5)

| When (Athens time) | What changed |
|---|---|
| 2026-11-03 09:12 | Version 4.6: decision 22, Operation Skill Restructure approved and saved (OPERATION-SKILL-RESTRUCTURE.md) |
| 2026-11-03 08:31 | Version 4.5: Teams skill v35 confirmed LIVE by Paul ("Yes, v35 is live") |
| 2026-11-03 08:30 | Version 4.4: `ff-population-transcript` uploaded as v33 by a Chrome chat (reported); not confirmed live; the real upload subfolder is `ff-population-transcript-skill` |
| 2026-11-03 07:17 | Version 4.3: decision 21 (no helpers, no more test rounds); round 6 set aside; `CHAT-NOTES.md` written; round-5 `ff-population-transcript` goes to packaging |
| 2026-11-03 05:47 | Version 4.2: `ff-population-transcript` program-driven build recorded (decision 20 status, tracker row): four independent review rounds, 319 tests, lint PASS, inventory 0 unaccounted; packaged-not-uploaded, not live |
| 2026-10-30 09:02 | Version 2.5: the 17:53 build uploaded as v34 by the Chrome chat (reported); second proven use of the upload method |
| 2026-10-30 14:49 | Version 2.6: Paul's second real-case trial recorded ("It seems to be working now"); not yet confirmed live |
| 2026-10-30 14:50 | Version 2.7: Teams transcript skill confirmed LIVE by Paul; S16 condition met (proven in real chats); next skill to be named by Paul |
| 2026-10-30 15:05 | Version 2.8: SKILL-TEMPLATE.md drafted (13 ingredients and a scorecard) and the study of ff-population-transcript recorded in section 8b; waiting for Paul's answers |
| 2026-11-02 17:05 | Version 3.5: decision 17 recorded (the form's own saved PDF is the Fact Find); the helper's build stopped |
| 2026-11-02 20:10 | Version 4.1: decision 20 (build the program for ff-population-transcript now; supersedes decision 18); the helper's earlier work restored |
| 2026-11-02 19:30 | Version 4.0: rule-by-rule check of the two interim Fact Find skills run and recorded (nothing lost by accident; two minor items for the next Teams change); lint, tests and a real run still not done |
| 2026-11-02 18:40 | Version 3.9: decision 19, the 13-ingredient template approved by Paul as it is |
| 2026-11-02 18:20 | Version 3.8: Teams skill 15:55 build uploaded as v35 by the Chrome chat (reported); waiting for Paul to confirm it is live; the two Fact Find zips still to upload, one at a time |
| 2026-11-02 17:55 | Version 3.7: decision 18 (no bigger rebuild of the two Fact Find skills for now; the helper's unfinished work removed from the tree, kept in git history) |
| 2026-11-02 17:40 | Version 3.6: decision 17 WITHDRAWN after Paul's correction (the form's PDF is an input; the population skill combines it with the transcript and other sources into a saved report; the summary skill summarises that report); decisions 15 and 16 stand |
| 2026-11-02 16:25 | Version 3.4: decisions 15 and 16 (fixed 11-section layout, look unchanged, ask Paul when the form file is missing, laptop window dropped); all six ff-population-transcript questions answered; proposal for the rebuild next |
| 2026-11-02 16:05 | Version 3.3: interim text update of `ff-population-transcript` and `fact-find-summary` made (zips outside the repo, not uploaded); Teams transcript skill changed so the follow-up appointment IS an action (228 tests, lint PASS, inventory 0 unaccounted; packaged, not uploaded, not live) |
| 2026-11-02 15:43 | Version 3.2: decision 14 completed (parked facts not processed; follow-up appointment IS an action at every meeting, reversing 29/10 in the Teams skill; look-up text checked and replaced) |
| 2026-11-02 15:24 | Version 3.1: decision 14 (new Fact Find form is the primary source; Audio to Text naming stays; Dread Disease ABI 3% always; follow-up appointment is not an action; version check) |
| 2026-11-02 09:11 | Version 2.9: ff-to-ff-populate forgotten at Paul's word (he deploys it by hand); the Audio to Text file may or may not exist when ff-population-transcript runs |
| 2026-11-02 15:13 | Version 3.0: the new Fact Find form studied and recorded in section 8c (route 2 worked, route 1 not connected) |
| 2026-10-29 17:47 | Version 2.4: planner-interim-procedure forgotten at Paul's word; decision 13 narrowed to this skill's action points |
| 2026-10-29 17:42 | Version 2.3: Paul's request recorded (decision 13): action points and checklist items ordered chronologically then logically, irrelevant ones sifted out, the skill asks when unsure; not built yet |
| 2026-10-29 17:21 | Version 2.2: the skill rebuilt to Paul's answers after the first real-case trial (short Planner note, PDF limits, actions sorted now/later, message to Sitamah shown with the outputs); decision 12 recorded |
| 2026-10-29 16:57 | Version 2.1: findings of the first real-case trial recorded in section 8 (notes too long, actions not sorted, Teams message not offered); structure to be agreed with Paul |
| 2026-10-29 15:46 | Version 2.0: the upload method is recorded as it really works (the Chrome chat uploads, the skill is REPLACED, the old version stays in its version history); the upload brief is now written by a program next to every zip |
| 2026-10-29 14:23 | Version 1.9: S7 records why the upload is by hand (no write route for Claude Code; Paul is on Max; org sync is Team/Enterprise only) |
| 2026-10-29 13:38 | Version 1.8: S2 now makes the date move with the skill (fingerprint record) and requires every run to say its version (Paul's request); built into the Teams transcript skill |
| 2026-10-29 13:27 | Version 1.7: Paul's yes to removals 1 to 4 and keep the table recorded; no change to the skill |
| 2026-10-29 13:17 | Version 1.6: Paul's answers recorded (WhatsApp calls also notify Sitamah with "WhatsApp Call Completed"; the true stories in the rules stay; go given for the Teams transcript skill); the skill now builds that message for WhatsApp calls |
| 2026-10-29 11:22 | Version 1.2: S16 approved on condition of a real-chat trial; each of the eight areas is its own heading; section 3 explains where the program lives; existing skills with scripts listed |
| 2026-10-29 13:08 | Version 1.5: Teams message gets the (Review Client)/(Prospect) label, decided from where the client's folder sits (Paul's answer); known gaps updated |
| 2026-10-29 12:27 | Version 1.4: Teams transcript skill hardened after an independent review (157 tests); divergent Teams message wording and sibling-skill headings recorded as gaps |
| 2026-10-29 11:53 | Version 1.3: Teams transcript skill rebuilt to the standards; tools built (stamp, lint, inventory, package); tracker and status updated |
| 2026-10-29 (between 11:01 and 11:22; first typed by hand as 12:00 in error) | Version 1.1: Paul's answers recorded (pane, Teams message via Zapier, removal approach, eight areas); Planner page and Teams message rules taken from `ff-population-transcript`; S16 proposed; missing page template recorded as a gap |
| 2026-10-29 11:01 | Version 1.0 written from Paul's seven rules plus eight additions (S8 to S15); Microsoft 365 permissions recorded; open questions and known gaps listed |
