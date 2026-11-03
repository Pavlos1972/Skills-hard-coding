# What changed in the Astute Summary Report skill, in plain words

For Paul. **Not uploaded, not live.** This is the program-driven version of `astute-summary-report-skill` (Operation Skill Restructure, 03/11/2026). The old version stays in the skill's version history in claude.ai, and a backup of its file is sent with the zip.

## What the skill does now
A program walks the chat through 8 steps: find the report, read it page by page, enter the data, check each product online, add the judgement flags, build the PDF, save it, final check. It ends with the saved file's name, a **numbered flag list** (most important first), the PDF, and a **short audit** (green ticks and red crosses). Nothing is sent to anyone and no message to Sitamah is built.

## What a program now does that Claude did by hand
- **The PDF is drawn by the program** in the look your skill described (landscape A4, 15 mm margins, navy and gold, orange flag boxes above the affected table, footer and page numbers). Claude no longer writes drawing code on every run.
- **The report is served page by page**; each page has to be acknowledged in order (a page with no readable text must be viewed as an image).
- **Every figure, policy number, date and name the chat enters is looked up in the report's own text.** What is not found is a red cross. The totals are added up by the program, never typed. The program refuses a benefit with no stand-alone/accelerated label and a policy with no premium pattern.
- **Sections are decided by the status Astute shows:** only "paid-up" goes in Section 3; lapsed, surrendered, inactive and anything unrecognised go in Additional Notes.
- **Orange flags the program raises itself:** a provider with no data, zero or missing values, a policy with zero values but no paid-up label, an unconfirmed product, a total that differs from the report's own, an unrecognised status, a bank insurance arm. The chat adds the judgement ones (status contradiction, unknown product, RA versus endowment) with a reason.
- **Online product checking:** one search per distinct product, the web address recorded, a description of at most 30 words. A product that cannot be confirmed says so and is flagged.
- **Routes:** computer, then Microsoft 365, then Zapier, every try logged. The 8:45 window is gone.
- **The file name is derived**, never typed. An existing file is never overwritten: the new one is numbered (2), (3).

## What left this skill
The nine copied generic rules and the Delivery gate (the program and the checker do their work), the "propose skills card" rule (changes are made only in Claude Code), the hand-typed stamp and changelog, the "pdf-reading skill" (it never existed), and the key-tools table (the steps name what is needed).

## What stayed the same
Every rule about content: figures only from the report, the cession note, contradictions flagged, missing or zero values are absent data, only paid-up policies in Section 3, a provider with no row is not proof of no cover, every benefit labelled, every policy with a premium pattern, risk covers before investments, one gold band per insurer.

A program (`tools/inventory.py`) went through all 173 sentences of the old text: **27 are still there word for word, 103 are reworded (each with a written reason), 43 were dropped on purpose (each with a written reason), and none was lost without a record.** The records are `history/changes.json` and `history/decisions.json`; the full list is `history/INVENTORY-REPORT.md`.

## Your yes/no list
1. **The data layout is my guess.** I have never seen a real Astute report. The layout the chat fills in (header, providers, policies with benefits, values, beneficiaries, fund allocation; group risk and retirement fund lines) follows your skill's text. **If the first real report does not fit it, tell me what is awkward and I fix it once. OK? Yes / No.**
2. **The description limit is 30 words** per product (the old text said "short"). **OK? Yes / No.**
3. **Flag order in the chat list** (most important first): status contradiction, unknown product, RA/endowment ambiguity, provider with no data, zero or missing values, total mismatch, unconfirmed product, bank insurance arm, other. **OK? Yes / No.**
4. **The audit is about 15 lines** (one per check). It is longer than the others because there are more things to prove. **OK, or shorter? Yes / Shorter.**

## What I could not do or check
- **I have never seen a real Astute report.** The first real run is the real test of the data layout and of the figure check (dates in a format the program does not know will show as "not found"; the audit names each one).
- **Only the text of the report can be checked.** That a figure sits on the right policy is only attested (a real figure on the wrong policy passes the check). A scanned report with no text has nothing to check against: the program says so and the figure check stays attested.
- **Entering the figures costs tokens** (the chat types every policy). That is the price of the figure check.
- **Online product checking is not provable beyond the recorded web address.** Whether a description is true stays attested.
- **How the pages look to the eye** is the chat's to view (the program saves page images). It checks only that the PDF is landscape A4, has the footer on every page, and contains every policy number and the five headings in order.
- Only one test was run, as agreed: one end-to-end run on an invented report (bad data refused, a figure or policy number or date not in the report caught, a correction re-opening later steps, a hand-edited file caught, an existing file numbered, a scanned report). Nothing was saved or sent anywhere.
