# om-tax-free-skill: Phase A findings (Operation Skill Restructure, 03/11/2026)

Read-only analysis of the LIVE skill (Paul's synced copy, 14/10/2026 15:54 build). **No client data is kept here.** Nothing has been changed or built.

## Facts
- Live skill: `SKILL.md` 333 lines (33,839 bytes), `scripts/tax_free_dates.py` (45 lines), `assets/OM_TaxFree_Proposal_TEMPLATE.html` (206 lines, with Paul's signature block and the WR logo as base64), `assets/wr_logo.png`. 4 files, about 77 KB. 375 single rules (sentences) in SKILL.md are the baseline (archived word for word in `SKILL.2026-10-14.md`).
- Job: after Alwyn's Old Mutual Tax-Free Investment quote is back, build the client proposal email (HTML, from a fixed template), save a no-logo copy in the client's Comparative Quotes folder, put the body into an Outlook DRAFT (Claude in Chrome; never sent by Claude), and message Sitamah on Teams (Zapier) to review, attach the three documents and email the client.
- Receives from: `client-pipeline-board` (starts it once the quote is back), `fact-find-summary` (the Fact Find Summary is a source), Alwyn's quote PDF, the Risk Tolerance questionnaire, the Overview. Hands over to: Sitamah (Teams). Related, not touched: `om-optimal-ra-proposal`, `rgar-skill`, `investment-comparisons-skill` (other proposal outputs), `complete-applications-skill` (the Tax-Free application), `paul-email-signature` (owns the signature).

## Flaws found
Client data (S11):
1. **A real client's name is inside `scripts/tax_free_dates.py`** (its self-check and comments). Not repeated here. The old versions stay in claude.ai's version history; only Paul can remove them.
Contradictions with other skills and standards:
2. **Signature:** Step 6 inserts Paul's signature through Outlook web (Insert > Signature "Paul K New"). `paul-email-signature` says the server adds the signature by Exchange rules and Claude must NOT type or insert one (it would appear twice). Both were last edited within minutes of each other on 14/10/2026 and never reconciled. `rgar-skill` has the same insertion step.
3. **Who sends the client email:** this skill (since 13/10) says Sitamah reviews, attaches and EMAILS the client. `client-pipeline-board` (send-decision-rules.md and the Investments playbook) still says the proposal lands in Drafts and Paul sends it himself.
4. **Step 7 sends the Teams message to Sitamah as soon as the draft is verified, with no yes from Paul.** S10 and Paul's rule: nothing is sent without his yes in that conversation.
Nothing forces the rules (text only):
5. **Every figure is typed by Claude from the quote** (contribution, start date, fund names and allocations, four fee percentages and their total, owner name and age) with no proof it matches the quote. The total fee is added up by hand. A program can check each against the quote's text and add the total.
6. **The "structural sanity check" in Step 4 is broken:** its placeholder test (`'[' in content and '@@' in content`) can never be true, so it reports "placeholders left: False" even when placeholders remain (proved with a one-line test).
7. **Placeholders are replaced by hand** in a copy of the template; the no-logo copy is made by hand (remove the logo paragraph); the file name is typed. All can be done by program.
8. **Dates:** the script exists but nothing forces its use; "Sent:" in the header must be "filled in" but no rule says with what.
9. **The 12-point audit and the "what I found" list are checked by eye.** Most of it a program can prove (placeholders, Cc is Sitamah, subject equals the draft's, weekday computed, tables open = close, figures match the quote, one "Kind regards,", the read-back of the draft and of the Teams message).
10. **The Teams greeting rule** (morning / afternoon / evening by South African time, "Hi" only if the same greeting was already used today) depends on Claude reading the clock and the chat.
11. **Access:** SharePoint tools only (Zapier for a contact lookup). No computer route, no log of tries (S4).
Vague or missing:
12. **Child's plan:** only "word it so the plan is clearly in the child's name". The template says "You work at [EMPLOYER] in the position of [POSITION]" and "You intend to save monies", which do not fit a child. No template wording for it.
13. **Lump sum:** the template is a monthly contribution ("R x p.m."). `om-optimal-ra-proposal` has a separate lump-sum template; this skill has none, yet the pipeline playbook mentions Tax-Free recurring OR lump sum.
14. **Typos in the client-facing template** (copied from a real sent email): "where you can contribute of R ..." and "The funds that are recommend are as follows".
15. **Fixed tax facts in the email** (R46,000 per tax year, R500,000 lifetime, 40% on excess) have no source and no review date; they change with the tax year.
16. Step 2 tells Claude to "use the `pdf-reading` skill": no skill of that name exists in the account (the PDF skill is `pdf`).
Standards and clutter:
17. About 25% of the 333 lines are the copied universal rules, the Delivery gate, the propose_skills rule (replaced by S7), the standing-rule block and the changelog; the stamp and changelog are typed by hand (S2). The Step 6 Chrome method (long, fragile, no way to check it ran) lives in a paragraph.
18. No run state, no tests, no checker. The script can be rewritten during a run.

## Duplications between skills
- **The same output is built by three skills with copied steps:** `om-tax-free-skill`, `om-optimal-ra-proposal` and `rgar-skill` each carry their own copy of: the Outlook draft method (shell + Chrome paste + signature + High importance + read-back), the Sitamah Teams message (greeting rule, Zapier send, markdown, read-back), the save-a-no-logo-copy step and the audit. Only the product text, the figures and the attachments differ. Recommendation: build the shared parts once, as code, and reuse the same code unchanged when the other two are rebuilt (each zip stays self-contained). One owner per output: this skill owns the Tax-Free proposal; `paul-email-signature` owns the signature.
- The universal rules block is copied in every skill (handled by the standard entry page).

## Score against the 13 ingredients
Full 0. Partial 6 (1 short entry page, 2 inputs, 5 evidence, 6 built by program, 10 one reply one question, 12 history outside). Missing 5 (3 step driver, 4 reading lock, 9 one checker, 11 tests, 13 package and upload). Not applicable 2 (7 short means short, 8 sorted actions).

## What a program CAN and CANNOT do here (honest)
- CAN: force the steps; serve the quote, the Fact Find Summary and the other documents page by page; check every figure, name, age, fund, allocation, fee and the start date against the quote's text, add the total, check the 100% allocation; compute every weekday and the greeting; build the email from the fixed template (no placeholder can remain), the no-logo copy, the subject, the file name and the Teams message; check the read-back of the Outlook draft and of the Teams message; derive file names; log the routes; keep the template and script fixed during a run.
- CANNOT: read a scanned page (the Risk Tolerance answers are often image-only; the chat views it and it stays attested); paste into Outlook (the Chrome step stays with the chat; the program builds the exact HTML and checks the read-back it is given); prove the draft is really in Drafts or that the Teams message arrived beyond what the chat reports; decide which quote version is current (it asks).

## Yes/No list for Paul (recommended answers in brackets)
1. **Client data in the live script:** the rebuild removes the real name and uses invented people only. (Yes)
2. **The Teams message to Sitamah** is shown to you with the draft details and sent only after your ONE yes (today it goes automatically). (Yes)
3. **Derive first, one confirmation table, one question** (as for the ROA and SROA): everything from the client's file with its source; you are asked only for the next meeting day, date and time, to confirm the meetings already held (pre-filled from the file names), the start date (your own double-check stays) and the Risk Profile only when no completed questionnaire exists. (Yes)
4. **Who sends the client email:** the rebuild follows this skill as it is now (Sitamah reviews, attaches and sends). The board says Paul sends: that is another skill, noted for its turn. (Yes, unless Paul sends these himself)
5. **The signature in the Outlook draft:** does the client's email show Paul's signature ONCE or TWICE when it goes out? If once: which is right today, the signature skill (the server adds it, Claude inserts nothing) or this skill (Claude inserts "Paul K New")? (Your answer decides. Until you answer I keep this skill's way and flag it in the audit.)
6. **Typos in the template** ("contribute of R" and "recommend are"): fix them to "contribute R" and "recommended". (Yes)
7. **The fixed tax facts** (R46,000 a year, R500,000 lifetime, 40% on excess): are they right for the current tax year? The rebuild prints them from one place so next March is one edit. (Please confirm the figures)
8. **Child's plan and lump sum:** the rebuild STOPS and asks you when the quote is for a child or a lump sum (no wording invented), until you give the fixed wording or a template. (Yes)

## Paul's answers (03/11/2026)
"Agree to all": yes to 1 to 8 as recommended. Two of them were not a plain yes/no, so they are handled like this (and told to Paul in the Phase B plan):
- Q5 (signature once or twice): not answered with a fact. The rebuild keeps this skill's way (Claude inserts "Paul K New" in the draft), the audit says so on its attested line, and one setting in the skill switches it to the signature skill's way when Paul tells me what he sees. STILL OPEN.
- Q7 (the tax facts R46,000 / R500,000 / 40%): kept exactly as in Paul's current template, printed from one place, NOT verified by me. Paul agreed; the audit lists them as attested.

## Status
Phase A report given to Paul 03/11/2026, answers recorded. Phase B plan given 03/11/2026, waiting for his approval. Nothing built.
