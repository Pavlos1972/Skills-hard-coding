# wr-roa-builder: Phase A findings (Operation Skill Restructure, 03/11/2026)

Read-only analysis of the LIVE skill (Paul's synced copy, 13/10/2026 14:50 build). **No client data is kept here** (the live files hold some: see flaw 1; the archived baseline is redacted). Nothing has been changed or built.

## Facts
- Live skill: `SKILL.md` 1,072 lines (78,967 bytes), plus `scripts/build_roa.py` (624 lines), `scripts/embed_email_images.py` (190), `references/roa_data_schema.md` (130), `references/dropdown_field_map.md` (169), `references/WR_Risk_Cover_Responses_24_07_26.docx` (the reason-text bank: 100 paragraphs, each under a scenario heading), `assets/ROA_Template_2026.docx` (the master template). 7 files, 268 KB. 1,055 single rules (sentences) in SKILL.md are the baseline for the rule-by-rule check (archived, redacted, in `SKILL.2026-10-13.redacted.md`).
- Job: build a Record and Confirmation of Advice (ROA, a compliance document under the General Code of Conduct s9) for ONE bundle (Risk, Retirement or Investment) from the template and the client's file: locate the documents, derive the setup answers (Step 0b, one confirmation table), read the quotes, fill the dropdowns, pick the reason text (a bank for Risk; the client's own reply email embedded as page images for Retirement/Investment), build the reference number and file name, run a 21-point audit, and save the .docx into the client's `ROA & Bus ROA` folder.
- Already has two scripts: `build_roa.py` (edits the template's XML: removes inactive tables, deletes Health Care and the RAR reference, sets Death/Dread overrides, next meeting date = ROA date + 12 months, filename builder) and `embed_email_images.py` (second pass: embeds the reply email as images). It also needs `wkhtmltopdf`, `pdftoppm`, `zip`/`unzip`, LibreOffice, `python-docx`/`lxml`, Pillow, and a `validate.py` at a path inside Claude's own environment.
- Receives from: `client-teams-transcript-skill` (Follow-Up Appointment Summary Notes), `fact-find-summary` (name and ID), the proposal-email skills (`om-optimal-ra-proposal`, `om-tax-free-skill`, `rgar-skill`) whose accepted email is embedded for Retirement/Investment, the Overview/quotes in the client's folder, and `client-pipeline-board` (ROA is part of its compliance gate). Hands over to nobody (saved in the client's folder). The Servicing ROA is a different skill (`wr-sroa-builder`).

## Flaws found
Client data (serious, S11):
1. **Real-looking client data is inside the live skill's files:** two client names and two 13-digit ID numbers sit in `references/roa_data_schema.md` (an example block and a filename example), one ID number in SKILL.md (the Step 2 example), and one client name in a comment in `scripts/build_roa.py`. They are not repeated here. The old versions also stay in claude.ai's version history (you would have to remove those yourself; I never delete).
Outdated or contradicting Paul's decisions and standards:
2. **Step 0 routes:** "local machine first, SharePoint only if the device is unreachable". No Zapier route, no log of tries (S4).
3. Rule 9 (changes through the `propose_skills` card) conflicts with S7 (changes only in Claude Code, uploaded as a zip).
4. **Delivery Path 1 builds the ROA as HTML** and pushes it as text. That is not the template, and the skill itself says "never build an ROA from scratch; always start from this file". For a compliance document this path should not exist.
5. It points at a skill that does not exist ("`pdf-reading`"; the skills list has `pdf`) and at a validator path inside Claude's own environment.
6. The sources still carry old names: "Fact Find Summary Report" (the Summary PDF is now made by `fact-find-summary` with the name `Fact Find Summary - DD.MM.YY - (First Surname).pdf`, and the Fact Find Transcript PDF by `ff-population-transcript`); the Follow-Up Notes are made by `client-teams-transcript-skill` v35.
Nothing forces the rules (text only):
7. **The scripts keep being rewritten and regressing.** The text carries five "recurring bug, re-verify before every build" warnings: the Retirement row reorder "found completely missing more than once", the embed script's hard-coded work folder "repeatedly regressed", the 4th argument that Retirement needs, the placeholder-grey fix, the 15 pt font rule. Claude is told to "extend the script and update this file", so the scripts change during runs. `build_roa.py` itself still uses a fixed `/tmp/roa_build_work` folder (not a fresh temporary one) and its comment still lists the removed `rar_reference` field.
8. **The 21-point pre-delivery audit is Claude reading rendered pages.** Most items are checkable by a program reading the finished .docx: one bundle active, no Health Care, Income After 24 months fixed sentence, valid Need Identified, no leftover "Choose an item.", ID has 13 digits, next meeting date, author, file name format, Retirement row order. Only a few need an eye (grey text, embedded page size, image borders near the footer).
9. **The script accepts any dropdown text.** It does not check an insurer, product or Need Identified against `dropdown_field_map.md`; Lump Sum Disability and Income Protection render BLANK if `need_identified` is not passed (the text says so, nothing stops it); the ID format and the premium are not checked.
10. **The reason text is copied by hand from a Word bank.** The bank has a paragraph for each cover type x FNA status x replacement scenario, with no placeholders, so the exact paragraph can be chosen by a program. Today Claude does it with "judgement", and nothing proves the text is verbatim from the bank.
11. **Every figure is typed from the quotes with no proof** (Recommended Amount, Taken Up Amount, premium). The method is validated for BrightRock only; other insurers are "flag it".
12. **Replacement is one document-level flag** while the wording is per cover type; the text itself lists this as a known open item. Nothing forces the flag and the paragraphs to agree.
13. Judgement steps with no way to prove them: the ROA date source, which sibling folder is the right transaction, which insurers were "considered", "visually compare at the same DPI".
Standards and clutter:
14. SKILL.md is 1,072 lines: the entry page is not short (the embed procedure alone is about 160 lines, delivery about 135); the universal rules are only about 15 of them. The stamp and the five-row changelog are typed by hand (S2); the full history lives in a project file outside the skill (could not be checked).
15. No access log, no run state, no tests, no checker. A named colleague appears in a rule ("never ... "), which is harmless but is a person's name.

## Duplications between skills
- The client-folder wording and the routes are repeated in every skill (not an output duplication).
- The proposal emails embedded for Retirement/Investment come from other skills; their layout is not described here, only embedded as images.
- `client-pipeline-board` names the ROA in its compliance gate; this skill owns the ROA itself.
- No other skill produces an ROA. The SROA is `wr-sroa-builder` (separate).

## Score against the 13 ingredients
Full 0. Partial 6 (1 short entry page, 2 inputs, 5 evidence, 6 built by program, 10 one reply one question, 12 history outside). Missing 5 (3 step driver, 4 reading lock, 9 one checker, 11 tests, 13 package and upload). Not applicable 2 (7 short means short, 8 sorted actions).

## What a program CAN and CANNOT do here (honest)
- CAN: force the steps; keep the two scripts fixed and unchangeable during a run; check the data against the dropdown lists and the data schema before building; pick the reason paragraph verbatim from the response bank; check every figure appears in the quote's text (BrightRock PDFs have text); open the finished .docx and prove most of the 21 audit checks; derive the reference number and file name; log the routes; refuse to overwrite a file.
- CANNOT: decide the advice, the ROA date's source or which transaction folder is right (judgement, recorded with a source and attested); prove a figure sits in the right column of the quote (only that it appears); prove how the pages look (grey text, image borders, embedded page size) or that the email pages were rendered right; prove the file reached SharePoint beyond the folder listing the chat reports. In this container `wkhtmltopdf` is not installed, so the embed pipeline can be proven only in part here.

## Yes/No list for Paul (recommended answers in brackets)
1. **Client data in the live files:** the rebuild removes every client name and ID number and uses invented people only. The old versions stay in claude.ai's version history (you can remove them there yourself if you wish). (Yes)
2. **Fix the two scripts and let the program prove the result.** Keep `build_roa.py` and `embed_email_images.py` as the base (their logic stays), fix the fixed work folder and the old comment, make them unchangeable during a run, and have the checker open the finished .docx to prove the audit checks it can (only the picture checks stay with you). (Yes)
3. **The program picks the reason text.** For Risk it chooses the exact paragraph from the response bank by cover type, FNA status and replacement, word for word. If the real situation fits none, it stops and asks you for your own wording; that text is then marked "custom, not from the bank" in the audit. (Yes) The catch: you review any custom wording.
4. **Figures are checked against the quote's text.** The chat types each amount and premium; the program checks each appears in the quote. Only BrightRock quotes are accepted as today; for any other insurer the program stops and asks you. (Yes)
5. **Saving:** the .docx goes into the client's `ROA & Bus ROA` folder through the routes in order (computer, Microsoft 365, Zapier), every try logged, and a file with the same name is never overwritten without your yes. The "ROA as HTML" path is removed: if no route can carry a .docx, the file is given to you in the chat to drop in yourself. (Yes)
6. **Step 0b stays, run by the program:** it prints the confirmation table from the answers the chat recorded, each with its source file, asks you ONE question, and stops on any conflict between sources, as today. The button questions stay. (Yes)
7. **Replacement:** the program sets the document-level replacement flag to true whenever any cover type is a replacement, and refuses a reason text that says "no Risk Cover currently in force" for a cover type marked new while another is replaced. (Yes)

## Status
Phase A report given to Paul 03/11/2026.

## Paul's answers (03/11/2026)
"Agree to all - BUT make sure that the skill works FULLY as intended including email embedding as before": yes to 1 to 7 as recommended, with one condition: the Retirement/Investment email embedding must keep working exactly as before. (1) No client data in the rebuilt skill. (2) The two scripts stay as the base, fixed and unchangeable during a run; the checker opens the finished .docx. (3) The program picks the Risk reason paragraph word for word from the bank; custom wording is marked. (4) Figures are checked against the quote's text; BrightRock only, other insurers stop and ask. (5) Saving through computer, Microsoft 365, Zapier, never overwriting; the HTML path is removed. (6) Step 0b run by the program with one question. (7) The replacement flag follows the cover types.

Found while planning: `wkhtmltopdf` (which the embed step needs) is not installed in this container, no installable package exists for it here, and the system blocked running a copy downloaded from the internet. So the HTML-to-PDF render cannot be proven in this container; the rest of the embedding (font rewrite, images, insertion point per bundle, captions, order) can.

Next: Phase B (plan) given to Paul 03/11/2026, waiting for his approval.
