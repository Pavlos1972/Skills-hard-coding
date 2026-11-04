# prospect-review-funnel-at-knowledge: what changed, and what I need from you (04/11/2026)

No client data is kept in the new skill. The test uses invented documents only; "Mr John Snow" is the AdviceTech test client your old skill already named.

## What it is now
A short entry page (about 1,500 tokens instead of about 17,000) and a program that walks every job one step at a time. The funnel itself is held in 14 pages that the program shows only when the work needs them, and the stage routes are held as data (90 stages, 147 routes) that the program checks for itself. The counts, the build phases and the open items live in ONE file (`assets/status.json`) and are drawn into the pages, so they cannot disagree.

The six kinds of work are: `question`, `move`, `build`, `test`, `docs`, `review`. Each starts with `run.py start`, and the first thing the chat says to you is which version is running.

## What I built from your 12 answers
- **A map and procedures (1).** The pages keep the stages, the routes, the decisions and the build rules; the six OneDrive documents are the source of truth. STREAMLINED wins on wording and logic, the Master Plan on AdviceTech detail (page 01).
- **Changes go through Claude Code (2).** The entry page says so. A chat can no longer edit this skill.
- **The split with `advicetech-website-knowledge` (3).** The board technique, the long-loop and bulk method, the many-lines-at-once panel and the tick-and-create method are now one-line pointers to that skill. I checked by search that it holds each of them; nothing was deleted there.
- **One status file (4).** The five-row change log is written by the stamp tool; the build plan became the phases in `status.json`; the backstory of the deletion requests is in the archive only.
- **Open items (5).** You named none as closed, so all four stay open with a date: MP15 #175, the auto-status "Closed" permission, "descriptions pre-fill each new Task" (not tested), and the release date with the end-to-end test.
- **Removals (6).** Rules 1 and 9, the typed stamp and change log, the Project pointers, "G5 → G6" (now "G5 → G5a → G5b → G6"), the "75 Sections" count and the dated forecasts.
- **Step driver (7).** Locate the six documents by the three routes in order (every try logged, Date Modified recorded), name the stages, read the pages in order, quote one line from the STREAMLINED and one from the Master Plan for every stage, then (for AdviceTech and document work) the plan, your one yes, documents first, the read-back of every object, and the short audit.
- **Never-touch guard (7).** A plan that names Charl's checklists #7, #8, #9 or Sections 15 and 16 is refused, whatever the reason.
- **Route checker (8).** It proves the 90 stages are consistent: every route leads to a real stage, every loop has an exit, no dead ends, nothing opens two exclusive stages together (A10a and A10b), and every stage code written on a page exists.
- **Register and AdviceTech audits left out (9).** The chat keeps doing them under the AdviceTech skill's methods; the program checks the read-back record the chat makes, not AdviceTech.
- **Reports (11).** The one-row-per-item table with running totals is kept for AdviceTech work; the short audit with ticks and crosses comes after it.
- **Names (12).** Kept as business contacts.

## Found while building (please read)
1. **Which document is changed first? The old text says two different things.** Page 10 (Using the skill, step 4) says "change the STREAMLINED document first, then the master plan, register, Logic & Flow, flow comparison and AUTOMATION". Page 09 (DOCUMENTS FIRST) says "the AT MASTER PLAN (and register) before anything is touched in AT; then the STREAMLINED document (where wording changes)...". I kept both sentences. The program enforces what both agree on: every document in the plan is changed after your yes and before the first AdviceTech change. It does not force an order between the documents.
2. **34 stages have no stated owner, and 12 have no stated name, in the old text.** I did not invent them (they show as "not stated" on the stage card). The owners are: A6a, A7, A8, A8a, A9, A10, A10a, A10b, A10c, A10e, A10g, A10h, A11, A11b, B7a, B7b, B7c, B8, B9b, B9c to B9h, B10, B10b, C1, C2, C4, C5ns, C4rt, C6, C7. The names are: A8, A10c, A10e, A11, A11a, B1, B2b, B3, B4, B6, B10, B10b. The audit says so on its closing line each time.
3. **The register and Master Plan layouts are unseen.** The program reads their text (a Word table row or an Excel row becomes one line) and only looks for the lines the chat quotes. I have never seen the real files, so the first real run may need one fix.

## Yes/No questions for you (recommended answer in brackets)
1. **Which document first (found 1).** Keep the program's rule as it is (all documents before AdviceTech, no order between them) and tell me which order you want written in the pages? (Yes; tell me STREAMLINED first or Master Plan first)
2. **Owners and names (found 2).** Send me the owner (SR, PK or CL) and the name of those stages, or I leave them as "not stated, read the Master Plan"? (Yes, leave them for now)
3. **The four scripts** `flowi.py`, `addnotes.py`, `tick.js`, `tick.css`: still not received. Until they arrive the pages say they live outside the skill. (Yes, I will send them)
4. **Open items.** Tell me which of the four are closed; the rest stay open with their dates.
5. **After the upload, the AdviceTech chats must stop editing this skill.** Whenever a decision changes the funnel, the change goes in the documents first and then to me, in Claude Code. Is that how you want it? (Yes)

## What is proven, what is only attested
Proven by the program and the one test: the stage routes are consistent; a quoted line really is in the document's text; Charl's items are refused; one owner per checklist; the line rules; documents changed after your yes and before the first AdviceTech change; every planned object read back with the right line count; the counts on the pages come from one file. Only attested: that the funnel logic is right; that a quoted line belongs to the stage it was quoted for; that the six documents (and AdviceTech) agree with each other; that the words recorded are yours.

## Not yet proven
The reading of your real Word and Excel files, the access routes to OneDrive in the chat (computer, Microsoft 365, Zapier), and a real AdviceTech build under the new steps. The first real run is the real test.
