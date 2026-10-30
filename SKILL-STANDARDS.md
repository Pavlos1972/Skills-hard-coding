# Skill Standards: the rules every one of Paul's skills must follow

**Version 2.5 (draft for Paul to review)**
**Last updated: 2026-10-29 13:08 (Athens time)**

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
| S16 | A program drives the job step by step and shows the next step only when the last one is proven | APPROVED 29/10/2026; built for 1 skill; real-chat trial pending |

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

### S16. A program drives the job, one step at a time (approved 29/10/2026, on condition it works in a real chat)
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

**Still open**
1. Which skill comes after the Teams transcript skill (only after Paul's trial and his go)?
2. Paul's upload of the zip and the result of the real-case trial (his yes/no on the five removals is answered: see decision 11).

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

## 9. Skill tracker

| Skill | Status |
|---|---|
| client-teams-transcript-skill | REBUILT to these standards (step driver, reading lock, client-file and access logs, Planner page, PDF, Sitamah Teams message (Teams meetings and WhatsApp calls), PASS/FAIL checklist; 226 tests, hardened after an independent review; nothing from the old skill lost without a record). The Sitamah message also covers WhatsApp calls (Paul's yes). Uploaded 29/10/2026 by a Claude-in-Chrome chat as version v33 (reported by that chat). First real-case trial found the notes too long, the actions unsorted and the Teams message not offered; REBUILT the same day to Paul's answers (short Planner note, sorted and ordered actions, asks when unsure, message shown with the outputs); uploaded 30/10/2026 UTC by a Claude-in-Chrome chat as v34 (Last updated 2026-10-29 17:53; reported by that chat, its replace-box line counts 65 to 66 match the files); waiting for Paul's second real-case trial and his confirmation that it is live |
| client-pipeline-board, complete-applications-skill, fact-find-summary, ff-population-transcript, wr-roa-builder, wr-sroa-builder, rgar-skill, om-optimal-ra-proposal, om-tax-free-skill, investment-comparisons-skill, life-insurer-comparison, life-policy-schedule-analyzer, client-review-notes, client-transcript-download, teams-meeting-setup-skill, outlook-emails-skill, cameron-short-term-skill, advicetech-website-knowledge, alpha-bank-statements, nedbank-current-account-categorization, paul-email-signature, correcting-skills, master-skill-template | Not started |
| planner-interim-procedure | FORGET (Paul, 29/10/2026): an interim skill, retired with AdviceTech. Do not convert it, consider it, or build rules for it |

## 10. Changelog (last 5)

| When (Athens time) | What changed |
|---|---|
| 2026-10-30 09:02 | Version 2.5: the 17:53 build uploaded as v34 by the Chrome chat (reported); second proven use of the upload method |
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
