# rgar-skill: Phase A findings (Operation Skill Restructure, 03/11/2026)

Read-only analysis of the LIVE skill (Paul's synced copy, 14/10/2026 16:17 build). **No client data is kept here.** Nothing has been changed or built.

## Facts
- Live skill: `SKILL.md` 434 lines (31,618 bytes), `scripts/rgar_dates.py` (84 lines), `assets/RGAR_Proposal_Email_TEMPLATE.html` (114 lines, with Paul's signature block and the WR logo as base64), `assets/wr_logo.png`. 4 files, about 98 KB. 420 single rules (sentences) in SKILL.md are the baseline (archived word for word in `SKILL.2026-10-14.md`).
- Job: after Alwyn's Retirement Goal Analysis Report (RGAR, a PDF) is back, build the client proposal email (HTML, from a fixed template) that recreates the shortfall paragraph as text, save a no-logo copy plus a copy of the RGAR PDF in the client's RA transaction folder > Comparative Quotes, put the body into an Outlook DRAFT (Claude in Chrome; never sent by Claude) and message Sitamah on Teams so she can attach the RGAR report and email the client.
- Receives from: `client-pipeline-board` (starts it once the report is back), `fact-find-summary` (the Fact Find Summary), Alwyn's RGAR PDF. Hands over to: Sitamah (Teams). Related, not touched: `om-tax-free-skill` (just rebuilt: same draft, message and save steps), `om-optimal-ra-proposal` (same steps again), `paul-email-signature` (owns the signature).

## Flaws found
Client data (S11): **none found** in the SKILL.md, the script or the template (no names, no 13-digit numbers, no email other than Paul's own). The script's "19/02/2022 was a Saturday" example is a date, not a client.
Contradictions with other skills, Paul's decisions and standards:
1. **Step 7 sends the Teams message by typing into Teams web with Claude in Chrome** (ctrl+b, shift+Return, remove the stray "2." item) and says Zapier posts plain text with raw tags (seen 01/10/2026). The Tax-Free skill (13/10/2026) found Zapier with `format: "markdown"` renders real bold and a real numbered list, and Paul's standing rule is Teams through Zapier only. The Chrome method is slow, fragile and out of date.
2. **The "reachability window" (Paul's laptop is only on at about 8:45am on weekdays) and the device-bridge visual read of the raw Fact Find** (Step 2): Paul's decision of 02/11/2026 dropped the 8:45am window (always try computer, Microsoft 365, Zapier, log each), and the Fact Find Summary is now drawn by program with a readable text layer, so the raw fillable-PDF route is no longer the main one.
3. **The net monthly target is looked up by an old label and section number:** "Net Amount Needed (today's terms)" under "6. What the Client Requires". The Fact Find Summary now numbers it "7. What the Client Requires" and the new Fact Find layout calls the field "Net amount needed at retirement".
4. **Signature:** Step 6 inserts "Paul K New" through Outlook web; `paul-email-signature` says the server adds it and Claude must not (it would appear twice). Same unreconciled question as in `om-tax-free-skill`.
5. **Who sends the client email:** this skill says Sitamah attaches the RGAR report and emails the client; `client-pipeline-board` says the proposal lands in Drafts and Paul sends it himself.
6. **Step 7 sends the Teams message to Sitamah as soon as the draft is verified, with no yes from Paul** (S10).
7. **The template disagrees with the rules:** its header "To:" shows `[CLIENT FULL NAME]` (the rules say To = the client's email address); its "Attachments:" line is a placeholder name pattern (the rules say use the real RGAR file name); "Sent:" is `[DAY], [DD MONTH YYYY] [HH:MM]` with no rule saying what to put there.
Nothing forces the rules (text only):
8. **Every figure is typed by Claude with no proof:** age, retirement age, years until retirement, current and future value of the expenses, the lump sum, the monthly contribution, the escalation %, the sustainability age, the net monthly target, gross income, employer, job title, the RGAR file name. A program can check each against the RGAR's and the Fact Find Summary's text, and that the net target sits on the labelled line (not the Reduced Quote's contribution target, a mix-up the skill itself warns about).
9. **The age rule is vague:** "age comes from the Fact Find Summary / what the user confirms" while the RGAR's date of birth is "only a sanity check". A program can compute the age from the RGAR's date of birth at the build date and compare it with the Fact Find Summary's age.
10. **The shortfall start/end dates** come from `rgar_dates.py` only if Claude runs it; nothing forces it, and the audit says "re-run the script and diff if there is any doubt". The program can apply it itself.
11. **The "structural sanity check" only counts tables.** It does not look for placeholders, the Cc, the subject or the weekdays; the 12-point audit is by eye.
12. **The flag "RGAR recurring investment R 0 / mismatch with the proposed RA"** depends on Claude noticing. A program can raise it from the typed value.
13. **The copy of the RGAR PDF into Comparative Quotes** (`sharepoint_copy_item`) has no check that it happened.
14. **No access log:** Microsoft 365 plus the device bridge only; no computer-first order, no log of tries (S4).
15. **The Teams greeting rule** (morning/afternoon/evening, "Hi" if already used today) depends on Claude reading the clock and the chat.
Vague or missing:
16. **A lump sum or a monthly contribution of R 0:** the template always prints both lines ("Once-off lump sum contribution required ... R x. Monthly recurring contribution required ... R y."). No wording exists for R 0, an absent lump sum or an absent monthly amount.
17. **The Outlook paste body** (blank lines, `<b>`, no header, no signature) is described in text only; the template has no marker where the body starts and ends.
Standards and clutter:
18. About 30% of the 434 lines are the copied universal rules, the Delivery gate, the propose_skills rule (replaced by S7), the standing-rule block, the changelog and a long Chrome-Teams typing method; the stamp and changelog are typed by hand (S2). No run state, no tests, no checker; the script can be rewritten during a run.

## Duplications between skills
- **Three skills carry copies of the same steps:** `rgar-skill`, `om-tax-free-skill` (rebuilt today) and `om-optimal-ra-proposal`: the Outlook draft method, the Sitamah message (greeting rule, send method, read-back), the no-logo copy and save, the audit. Only the product text and figures differ. Recommendation: reuse the code written for `om-tax-free-skill` unchanged (each zip stays self-contained), so the draft check, the message check, the greeting and the save are identical. One owner per output: this skill owns the RGAR proposal email; `paul-email-signature` owns the signature.
- The universal rules block is copied in every skill (handled by the standard entry page).
- **Side issue, not this skill (noted, not chased):** this skill says Paul's real signature block (Verdana, #27A8E0 name at 18pt, logo 473x169) was pulled from his own signature file on 25/09/2026 because the `om-optimal-ra-proposal` asset was an older, visually different copy. The `om-tax-free-skill` template was "aligned with the Optimal RA skill" and carries a different signature block (Calibri-style, smaller logo): it may be the older copy. It only shows in the HTML copy and the saved copy, not in the Outlook draft.

## Score against the 13 ingredients
Full 0. Partial 6 (1 short entry page, 2 inputs, 5 evidence, 6 built by program, 10 one reply one question, 12 history outside). Missing 5 (3 step driver, 4 reading lock, 9 one checker, 11 tests, 13 package and upload). Not applicable 2 (7 short means short, 8 sorted actions).

## What a program CAN and CANNOT do here (honest)
- CAN: force the steps; serve the RGAR and the Fact Find Summary page by page; check every figure, name, age and the RGAR file name against their text, the net target against its labelled line, the age against the date of birth; compute every weekday and the shortfall period; build the email from the fixed template (no placeholder can remain), the no-logo copy, the paste body, the subject, the file name and the Teams message; check the read-back of the draft and of the posted message; check the RGAR copy sits in the folder listing; keep the template and scripts fixed during a run.
- CANNOT: read a scanned page; paste into Outlook; prove the draft really sits in Drafts or the Teams message arrived beyond the read-backs the chat gives it; decide which RGAR version is current (it asks); judge whether the RGAR matches the product being proposed (it flags R 0 and asks).

## Yes/No list for Paul (recommended answers in brackets)
1. **Teams message to Sitamah through Zapier with real formatting (markdown), not typed into Teams web,** shown to you in the confirmation table and sent only after your ONE yes and a checked draft (as for Tax-Free). (Yes)
2. **Drop the 8:45am laptop window and the device-bridge visual read of the raw Fact Find.** Sources: the Fact Find Summary first (made by `fact-find-summary`); if there is none the skill STOPS and asks you. Routes: computer, Microsoft 365, Zapier, every try logged. (Yes)
3. **The net monthly target:** the new Fact Find calls it "Net amount needed at retirement" (the old skill says "Net Amount Needed (today's terms)"). Is it the same figure? The program will require the typed figure to sit on that labelled line in the Fact Find Summary. (Please confirm the label)
4. **Derive first, one confirmation table, one question** (as for Tax-Free): you are asked only for the meetings already held (pre-filled from the file names) and the next meeting day, date and time. (Yes)
5. **The template's header:** To shows the client's email address (not the name), Attachments shows the real RGAR file name, and Sent is the build date and time in South African time. (Yes)
6. **The client's age is worked out from the RGAR's date of birth at the build date and compared with the Fact Find Summary's age;** a difference stops the run and asks you. (Yes)
7. **A lump sum or monthly contribution of R 0 (or no recurring investment) stops the run and asks you what wording to use;** no wording is invented. The "recurring investment R 0" flag to you stays. (Yes)
8. **Who sends and the signature:** the rebuild follows this skill (Sitamah attaches the report and sends; the board is another skill, noted for its turn), and the signature stays a one-word setting (`insert` today, `server` later), the same open question as in the Tax-Free skill: does the client see your signature once or twice? (Yes, and one answer will settle both skills)

## Paul's answers (03/11/2026)
"Agree to all": yes to 1 to 8 as recommended. Two were not plain yes/no, so they are handled like this (and told to Paul in the Phase B plan):
- Q3 (the net target's label): the program accepts BOTH labels, "Net amount needed at retirement" (the new Fact Find) and "Net Amount Needed (today's terms)" (the old text), and the typed figure must sit on that labelled line in the Fact Find Summary; the audit says which label matched. If neither label is found the run stops and asks Paul.
- Q8 (the signature): the rebuild keeps this skill's way (Claude inserts "Paul K New") as a one-word setting, the same open question as in `om-tax-free-skill`. STILL OPEN: does the client see the signature once or twice?

## Status
Phase A report given to Paul 03/11/2026, answers recorded. Phase B plan given 03/11/2026, waiting for his approval. Nothing built.
