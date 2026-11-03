# What changed in the WR ROA Builder skill, in plain words

For Paul. **Not uploaded, not live.** This is the program-driven version of `wr-roa-builder` (Operation Skill Restructure, 03/11/2026). The old version stays in the skill's version history in claude.ai, and a backup of its file is sent with the zip.

## What the skill does now
A program walks the chat through 9 steps: find the client's documents, read them page by page, enter the setup answers, show you a confirmation table (ONE question), the email page (Retirement and Investment only), build, check, save, final. It ends with the saved file's name, the `.docx`, and a **short audit** (green ticks and red crosses). Nothing is sent to anyone.

## What a program now does that Claude did by hand
- **The two scripts are fixed.** `build_roa.py` and `embed_email_images.py` keep their logic but can no longer be rewritten during a run, so the "recurring bug, re-verify before every build" list (the Retirement row order, the embed heading, the fixed work folder) can no longer come back. `build_roa.py` now uses a fresh temporary folder every time.
- **Documents are served page by page** and each page is acknowledged in order.
- **Every name, ID and figure is looked up in the documents' own text** (the quotes, application, Fact Find Summary, emails). What is not found is refused.
- **The answers are checked against the template's own dropdown lists** (read from the template, not from memory). A disability or income cover with no Need Identified is refused (it used to render blank). Reasons that disagree with the replacement flag are refused.
- **The reason text is picked by the program from your response bank, word for word,** by cover type, FNA status and replacement. A new cover type while another is replaced gets the bank paragraph cut before its replacement sentence plus your verbatim "other Risk Cover in force" sentence. If nothing fits, the chat must bring your own wording; it is marked CUSTOM in the table and the audit.
- **The program builds the data, the reference number and the file name** (never typed), and the next review date.
- **The finished `.docx` is reopened and checked** (18 checks for Retirement and Investment, 15 for Risk): one bundle only, no Health Care, the fixed sentences, valid dropdowns, reasons word for word, amounts, name and ID line, reference number, replacement wording, next review date, author, no placeholder text, no RAR field, no grey fields, and the embedded pages (count, place, captions, no spacer, width).
- **Nothing is built before your yes** to the confirmation table, and a changed answer voids it.
- **Email embedding is as before and now forced:** the chat still writes the one HTML page (the client's reply, then the quoted proposal); the program rewrites the font sizes to 15 pt, renders with wkhtmltopdf at the fixed page size (never LibreOffice, never zoom), makes the 150 dpi pages, embeds them before "Investment Planning" (Retirement) or "POLICY REPLACEMENT" (Investment), and reads the first rendered page: it must open on the client's own reply.
- **Saving:** computer, Microsoft 365, Zapier in order, every try logged, a file with the same name is never overwritten without your yes.

## What left this skill
The nine copied generic rules and the Delivery gate, the "propose skills card" rule, the hand-typed stamp and changelog, the "pdf-reading skill" (it never existed), and **Delivery Path 1 (building the ROA as HTML)**: the ROA is always the `.docx` from your template. **All client data:** the old files held two client names and two ID numbers (not repeated anywhere); the rebuilt skill holds none and its tests use an invented person only.

## What stayed the same
The template, the response bank and the dropdown map (copied unchanged), every rule about the bundles, the ROA date, the insurers, replacement per cover type, declined versus not-accepted needs, the fixed sentences, the reference number and file name formats, the embedded-email rules, and the logic of both scripts.

A program (`tools/inventory.py`) went through all 1,055 sentences of the old text: **26 are still there word for word, 940 are moved or reworded (each section has a written reason), 89 were dropped on purpose (each with a written reason), and none was lost without a record.** The records are `history/changes.json` and `history/decisions.json`; the full list is `history/INVENTORY-REPORT.md`.

## Your yes/no list
1. **The pointer line** in the Retirement/Investment reason box now reads "The client's email reply confirming **their** go-ahead on this proposal ([date]) ..." (the old example said "his"). **OK? Yes / No.**
2. **The two reference-number styles follow your examples exactly:** Risk `BrightRock Personal Cover - R1,172.80 p.m.` (no space after R) and Retirement/Investment `Old Mutual Retirement Annuity Xtra Max - R 1,500.00 p.m.` (a space after R). They differ in the old text. **Keep both as they are? Yes / No.**
3. **A cover the client did not take up after an FNA** (not accepted) uses the bank's "FNA DONE / BENEFIT NOT ACCEPTED" paragraph. That paragraph exists for Income Protection only; for Life, Disability and Dread the chat must bring your own wording (marked CUSTOM). **OK? Yes / No.**
4. **The email page's font size:** the program takes the most common font size in the page as the body size and scales everything so it becomes 15 pt; the chat can give the body size instead (`--base-pt`). **OK? Yes / No.**
5. **Only the quotes, application, follow-up notes and the two emails are read page by page;** the Fact Find Summary is used to check the name and ID. **OK? Yes / No.**

## What I could not do or check
- **The real `wkhtmltopdf` is not installable where I built this, and the system blocked me from running a downloaded copy.** The test uses a stand-in that refuses any command line without the fixed page size or with `--zoom`; the font rewrite, the page images, the embedding, the position and the first-page check all ran for real. **How the real wkhtmltopdf renders your real email is proven only on your first real Retirement or Investment ROA.** The program stops at the start of a Retirement or Investment job if wkhtmltopdf is missing.
- **How the pages look to the eye** (filled fields black on screen, the embedded pages the same size as the ROA's text, no border touching a footer) stays with the chat: the program saves page images for it to look at.
- **A figure in the right column of the quote** is only proven to appear in the document, not to sit in the right column. Only BrightRock quotes are accepted, as before.
- **I never saw a real quote, application or reply email.** The test uses invented ones in the layout your skill describes; if a real one differs (a date or amount in a form the program does not know), the audit names it.
- **The old versions in claude.ai's version history still hold the two client names and ID numbers.** You can remove those versions yourself if you wish; I never delete.
- Only one test was run, as agreed: one end-to-end run on invented data (Risk, Retirement and Investment, bad answers refused, a hand-edited file caught, an existing file never overwritten, the embedding checked). Nothing was saved or sent anywhere.
