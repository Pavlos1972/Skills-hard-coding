## Output 2: Follow-Up Appointment Summary Notes (PDF) - follow-up meetings only (not produced for a first/Fact Find meeting)

Built by `build.py` with **reportlab** (not Word), navy palette, Helvetica. It also renders each page to a PNG (`pdftoppm`): look at every image before delivering (step `look`).

- Title: `Follow-Up Appointment Summary Notes - DD.MM.YY - (Surname, First Name)`, navy `#1F3A5F` ~17-20pt. Subtitle (grey ~10pt): `[Client Name]   |   Wealth Revolution   |   Advisor: Paul Kafentzis   |   Meeting Date: DD/MM/YYYY`, then a navy `HRFlowable`.
- One plain opening sentence on what the meeting was and which quotes/areas it covered.
- Sections, each a bold navy heading followed by short point-form bullets: **Since the Last Meeting**, then the Step 3 areas that apply (each of the eight its own heading, followed by one line naming those not discussed), then **Applications** (only if Step 6 found differences), then **Action Points**, **Coming up** (only if something waits) and **Next Steps**.
- Inside each area, at most 4 bullets of at most 45 words each (Paul's rule): bullet 1 = the quote referenced or the topic; then short bullets on what it does, merged where they can be; each bullet carries its own status word. The opening sentence is at most 40 words.
- **Applications:** one bullet per application stating what differs or is missing. No ID, account or tax numbers.
- **Action Points:** the actions for now, every one assigned to **Sitamah**. **Coming up:** the actions that wait for something, each with what it waits for (a cession, for example, waits until the policy is issued). **Next Steps:** what the client must do and the next appointment - never Paul's own steps (Paul's rule).
- No tables, no nested bullets, no characters outside WinAnsi. Two pages at most: the program fails a longer PDF.

**Checklist before delivering - who checks each item now.** `verify.py` checks the ones marked PROGRAM; the rest are Claude's own judgment, shown to Paul for review.

| # | Item | Checked by |
|---|---|---|
| 1 | each area is its own bold navy heading | PROGRAM (build + headings present in the PDF text) |
| 2 | every bullet is its own Paragraph, short, with hanging indent | PROGRAM (build) + Claude looks at the images |
| 3 | quotes named with insurer, type, number and premium, never line-by-line | Claude (judgment) |
| 4 | every accepted quote states type, number and agreed premium | Claude (judgment) |
| 5 | resolved / open / changed items marked | PROGRAM (change must be marked CHANGED) |
| 6 | EVERY action names Sitamah as the owner | PROGRAM |
| 7 | no heading stranded at a page bottom | PROGRAM |
| 8 | rendered image checked | Claude, recorded in the receipt |
| 9 | no ID, account or tax numbers anywhere | PROGRAM (13-digit numbers fail; 10-digit warn) |
| 10 | the Step 1b decision ledger was fully walked | PROGRAM (every decision/request/change/hold covered) |
| 11 | verification pass of the drafted outputs done | PROGRAM (every quote found) + independent subagent re-check for acceptances, owner changes and money |
| 12 | current correspondence checked and any owner change has a revised-quote action | PROGRAM (checks block) |
| 13 | the Planner note is the copy-ready page with the correct pointer line | PROGRAM |
| 14 | every benefit explained is described from the actual quote and every cession has a `Sitamah to ...` action (a later one) | Claude (benefit wording) + PROGRAM (cession action) |
| 15 | credit life on every debt the new cover protects is reported | PROGRAM (checks block, always) |
| 16 | no "to confirm" left for a detail that is on file | Claude (judgment); PROGRAM logs what was searched |
| 17 | no two independent actions worded as one waiting on the other | PROGRAM warns on dependent wording; Claude decides |
| 18 | the transcript was read in full TWICE and the delivery line says so | PROGRAM |
| 19 | every bullet and every action has a source - no inferred facts, no invented actions, no chase actions for items left with the client | PROGRAM |
| 20 | every request or instruction made on the call is captured exactly as the client/Paul answered it | PROGRAM (ledger coverage) + Claude (wording) |
| 21 | no garbled line has been turned into a fact - ambiguous ones are flagged to Paul | Claude (judgment); the ledger records the line as excluded with a reason |
| 22 | the Planner note is short: 1-3 one-liners of at most 20 words per area, at most 8 actions for now | PROGRAM (group L) |
| 23 | the PDF is short: at most 4 bullets of at most 45 words per area, two pages at most | PROGRAM (group L, and the page count) |
| 24 | every action is sorted `now` or `later` (with its trigger), and none is a client decision, a credit-life cancellation, a quote or what's-next email, or a meeting set-up | PROGRAM (group L) |
| 25 | Next Steps lists only what the client must do | PROGRAM (group L) |
| 26 | action points are in order (earliest deadline first, nothing before what it depends on), what was left out is listed with its reason, and every open question was asked of Paul | PROGRAM checks the dates, the dependencies, the lists and Paul's recorded answers; Claude judges relevance |

**Anti-pattern (wrong):** one long paragraph with typed bullets, granular quote breakdowns, topics blended into one block, a quote described without its insurer/type/number, reporting an earlier-in-the-call state as final when the client changed it later, giving Paul an action point, putting the Planner note in a code block, leaving out a benefit/cession explained on the call, telling Sitamah/Paul to "confirm" something already on file, leaving out credit life, wording two independent actions as one gated on the other (e.g. "request the FNA once the psychiatric report is received" when the two are actually independent), reverting - for a first/Fact Find meeting - to the old fixed 6-part layout instead of this skill's own planning-area structure, **or: producing a report after a single read, keyword-searching instead of reading, writing a garbled line up as a fact (e.g. a health condition the client may not have), inventing a chase action for something the client said he would get back to us on, writing "not agreed" when the client said yes, or missing a request made in the closing minutes (e.g. the client asking for his wife's portfolio review to be put in the what's-next email).** **And (Paul's rule): a Planner note that repeats the PDF or runs past one line per bullet, an action that is for later or is not an action at all, Paul's own step listed under Next Steps.**

## Filenames and saving (mandatory) - follow-up meetings only

- Teams meeting: `Follow-Up Appointment Summary Notes - DD.MM.YY - (Surname, First Name).pdf`. WhatsApp call: `WhatsApp Call Summary - DD.MM.YY - (Surname, First Name).pdf`. Always PDF, never docx.
- Save every time into the client's `2. Fact Find` folder via `device_commit_files`. Confirm the folder and file name to Paul in one line. If the file is locked/open, say so plainly and retry when he confirms; never silently skip.
- Output 1 (the Planner page) is shown as the Artifact page only and is never saved into the client's folder, for every meeting type including a first/Fact Find meeting.

## WhatsApp call variant

No transcript file exists: ask Paul for his recap/notes or recording and confirm the exact date and TIME of the call before drafting (run `run.py start --type whatsapp`; the message to Sitamah is sent for a WhatsApp call too, worded "WhatsApp Call Completed"). **The Two-Read Lock applies to whatever source Paul supplies (recap, notes or recording transcript): it is read in full twice before any output.** Still run Step 1b, Step 1c, Step 2, Step 2b and Steps 3-6. Lead with the medium, name both parties with roles, include date and time. Output 1 title: `**[Client] – DD/MM/YYYY**` then italic line `WhatsApp call, [time]: [topic]`, pointer line names the WhatsApp Call Summary file. Output 2 title `WhatsApp Call Summary - DD.MM.YY - (Surname, First Name)`; subtitle `[Client] (Client)   |   Paul Kafentzis (Broker)   |   Wealth Revolution   |   Call Date: DD/MM/YYYY   |   Call Time: HH:MM`.
