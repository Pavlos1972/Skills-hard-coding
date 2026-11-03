# astute-summary-report-skill: Phase A findings (Operation Skill Restructure, 03/11/2026)

Read-only analysis of the LIVE skill (Paul's synced copy, 14/10/2026 12:21 build). No client data is kept here. Nothing has been changed or built.

## Facts
- Live skill: `SKILL.md` 148 lines, 14,530 bytes, ONE file, no script. 173 single rules (sentences) are the baseline for the rule-by-rule check (archived word for word in `SKILL.2026-10-14.md`).
- Job: turn a client's Astute Consolidated Client Portfolio (CCP) report (a PDF in the client's `5. Astute` folder) into a verified, tabulated summary PDF: Section 1 active risk covers and investments (one gold band per insurer), Section 2 group risk and retirement funds, Section 3 paid-up policies, Additional Notes (inactive, lapsed, surrendered), General Verification Notes (cession note), orange flag boxes. Saved beside the report as `Astute Report Summary - DD.MM.YY - (First Surname).pdf`, sent in the chat with a numbered list of flags.
- Receives from: the report is drawn by Sitamah once the LOA is signed (`client-pipeline-board`, `prospect-review-funnel-at-knowledge`); the funnel task is "CL - Compile Astute Summary Report if Astute drawn & save". Hands over to nobody (Paul reads it). It does NOT analyse policies (that is `life-policy-schedule-analyzer`).
- Tools it relies on: the device bridge, `Microsoft_365:sharepoint_*`, web search, "the pdf-reading skill", ReportLab, `pdftoppm`, SendUserFile.
- Client data scan: none (no names, emails, ID or phone numbers). The summary it BUILDS carries the client's ID number and date of birth in its header (as today); none of that goes in the repo.
- I have no real Astute report to look at, so I do not know the layout of the real report.

## Flaws found
Outdated or contradicting Paul's later decisions:
1. **Step 1 routes are out of date.** "Local machine first, SharePoint only if the machine is unreachable (normally only around 8:45 Athens time)". Paul dropped the 8:45 window on 02/11/2026 for the Fact Find skills; standard S4 is computer, then Microsoft 365, then Zapier, every try logged. This skill has no Zapier route and no log.
2. **It points at a skill that does not exist:** "the pdf-reading skill". The skills list has `pdf`.
3. Rule 9 (changes through the `propose_skills` card) conflicts with S7 (changes only in Claude Code, uploaded as a zip).
Nothing forces the rules (text only):
4. **Claude writes new ReportLab code on every run** ("a pattern to follow"; `pip install reportlab`). The look (landscape A4, 15 mm margins, navy/gold/grey, orange flag boxes) rests on Claude copying it correctly each time. This is the biggest flaw.
5. **Nothing proves a figure came from the report.** "Copy every figure to the cent" and "Never write a figure that is not in the report" are promises. A mistyped cover amount or policy number would go into the PDF unnoticed.
6. "Read every page" and "check every page as an image" cannot be proven; "any total is added up in code" is left to whatever code Claude writes that day.
7. **Step 3 is expensive and vague.** For EVERY product: search the insurer's page and cross-check a second independent source. Nothing records the sources, nothing says how many searches are enough, and it spends tokens on every run. "A short accurate description" has no size limit.
8. The orange-flag rules are a list of judgements ("unknown or thinly described product", "RA versus endowment ambiguity", "status contradiction") with no way to check that every one that applies was raised. Some are computable (a provider with no row, a zero or missing value, a policy with zero values but no paid-up label, a total that does not match); some are the chat's judgement.
9. The "version suffix" for an existing file is not defined ("keep both with a version suffix").
10. The hand-over mentions `SendUserFile`, which is a Claude Code tool; whether it exists in your claude.ai chats is unproven.
Standards and clutter:
11. About 30% of the 148 lines are the copied "universal rules" and the Delivery gate; the Verification checklist then repeats the Delivery gate and the Standing rules repeat Step 4's flag rules.
12. The stamp and the five-row changelog are typed by hand (S2); the full changelog is said to live in a project file outside the skill (could not be checked).
13. No access log, no run state on disk, no tests, no checker. "Requested by" in the header has no stated source.

## Duplications between skills
- The "which folder is the client's folder" wording (`Company - Paul` or `Company - WR Clients` -> `Paul Kafentzis (Client Files)`, never another broker's) is repeated in every skill. Not an output duplication.
- No other skill makes this PDF. The Astute report itself is drawn by Sitamah (board skill), not by Claude; this skill must not draw it.

## Score against the 13 ingredients
Full 0. Partial 5 (1 short entry page, 2 inputs, 5 evidence, 10 one reply one question, 12 history outside). Missing 6 (3 step driver, 4 reading lock, 6 built by program, 9 one checker, 11 tests, 13 package and upload). Not applicable 2 (7 short means short, 8 sorted actions).

## What a program CAN and CANNOT do here (honest)
- CAN: force the steps; build the PDF the same way every time from one data file (look, fixed section order, tables, flag boxes, footer); add up every total itself; refuse a policy without a stand-alone/accelerated label or a premium pattern; raise the computable flags itself; check that every figure and policy number the chat entered appears in the report's own text (if the PDF has a text layer); print the short audit.
- CANNOT: read a layout it has never seen. Without a real report I cannot build or prove a reader. It cannot prove the report was read page by page, that the pages look right to a human eye (attested), or that a product description is true (it only records the sources the chat found). A scanned, image-only report has no text to check figures against; the program says so and that check stays attested.

## Yes/No list for Paul (recommended answers in brackets)
1. **How do the figures get out of the report?** (A) The chat reads the report and enters every policy and figure through the program; the program then checks each figure and policy number against the report's own text, adds up the totals, and draws the PDF. A figure not found in the report is a red cross. (B) A reader built for the layout, like `fact-find-summary` has. (A) The catch: entering the figures costs tokens, and a scanned report cannot be checked that way. (B) cannot be proven without a real report, so its first real run would very likely fail. (A, Yes)
2. **Online product checking (Step 3).** Today: every product, two sources, nothing recorded. Recommend: one search per distinct product name (not per policy), the source address recorded for each; a product that cannot be confirmed says "not confirmed online" and gets an orange flag. The program refuses a description with no source unless it is marked unconfirmed. (Yes) The other choice is to drop online checking and rely on the report's own product names, all marked unconfirmed (cheaper). 
3. **Access routes:** computer, then Microsoft 365, then Zapier, every try logged; the 8:45 window is dropped, as for the Fact Find skills. (Yes)
4. **Look stays exactly as today** (landscape A4, 15 mm margins, navy/gold/grey, orange flag boxes, footer), drawn by the program. File name stays `Astute Report Summary - DD.MM.YY - (First Surname).pdf`; an existing file is never overwritten: the new one gets `(2)`, `(3)` and you are told. (Yes) The suffix style is mine.
5. **The reply:** the PDF, the numbered flag list (most important first), as today, then the SHORT audit. Nothing is sent to anyone and no message to Sitamah is built (the funnel task only says compile and save). (Yes)

## Status
Phase A report given to Paul 03/11/2026. Waiting for his answers.
