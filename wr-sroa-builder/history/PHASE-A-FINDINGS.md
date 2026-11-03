# wr-sroa-builder: Phase A findings (Operation Skill Restructure, 03/11/2026)

Read-only analysis of the LIVE skill (Paul's synced copy, 14/10/2026 16:29 build). **No client data is kept here.** The live files hold some (flaw 1); the numbers are not repeated. Nothing has been changed or built.

## Facts
- Live skill: `SKILL.md` 534 lines (34,266 bytes), `scripts/build_sroa.py` (484 lines, reportlab), `references/sroa_data_schema.md` (138), `scripts/sample_data.json`, `assets/WR_Generic_Servicing_Record_of_Advice.pdf` (the original template, a layout reference only), `assets/WR_Logo.png`. 6 files, 220 KB. 477 single rules (sentences) in SKILL.md are the baseline for the rule-by-rule check (archived word for word in `SKILL.2026-10-14.md`; it holds no client data).
- Job: for a client whose EXISTING policy is being changed (cover, premium, portfolio, ...), build a standalone Servicing Record of Advice PDF: the Current Policy Schedule compared line by line with the accepted servicing quote (old -> new or "No change"), four blocks (Servicing FNA quote, Shortfall quote, Alternative quote, Requested Servicing Change/s), the advisor's reason in his own words, the Portfolio Changes narrative (investment-linked only, else "N/A"), the client's ID, a CP number, two blank date fields and two signature lines. One PDF per policy, filename `SROA - [Insurer]_[Policy Number] - [DD.MM.YY] - ([First]_[Surname]).pdf`. Fixed: FSP45946 and Paul Kafentzis; the Premium line always "incl. R20 policy fee".
- Receives from: `client-pipeline-board` (hands off the right documents when a Servicing line reaches Policy Issue; it deliberately does not source the SROA's date or reason), `fact-find-summary` (the Fact Find Summary), the Outlook thread of the servicing quote and its acceptance. Hands over to nobody (the PDF is saved in the client's Servicing folder). The new-policy document is `wr-roa-builder`.

## Flaws found
Client data (serious, S11):
1. **Two 13-digit ID-style numbers are inside the live files:** one in `scripts/sample_data.json`, one in `references/sroa_data_schema.md`. BOTH pass the South African ID checksum, so they may be real. The sample also carries a 9-digit CP number and amounts that look real. They are not repeated here. The old versions stay in claude.ai's version history (only you can remove them; I never delete).
Outdated or contradicting Paul's decisions and standards:
2. **Step 0 routes:** SharePoint search and Outlook search only. No computer route, no Zapier route, no log of tries (S4).
3. **Two contradictory ways to update the skill:** rule 9 (the `propose_skills` card) and a separate "standing rule" that says to package a `.skill` file and have Paul upload it. S7 settled this: changes only in Claude Code, uploaded as a zip.
4. **Everything is asked one question at a time** (quotes compiled, accepted quote, client name, ID, SROA date). S3 and Paul's approach for the ROA skill (Step 0b): derive from the client's documents first, show ONE confirmation table, ask last. The ID and the full name are also in the documents.
5. The Fact Find is called "Fact Find Summary" by its old name, and the labels-only workaround is copied from the ROA skill; the Fact Find Summary is now made by `fact-find-summary` with a fixed name.
6. A wrong cross-reference: "from what the advisor tells you in Step 2, point 2" (it is Step 3, point 2).
7. **The Delivery step has no save method at all:** "saved in the client's own folder located in Step 0" but no routes, no tools, no collision rule, no "never touch another broker's folder", and the example folder layout differs from the ROA skill's.
Nothing forces the rules (text only):
8. **The file name is typed by Claude** (the script has no filename function, unlike the ROA script): underscores, a DD.MM.YY date, "First_Surname" without middle names. Easy to get wrong.
9. **Every old and new figure is typed from the schedule and the quotes with no proof.** A combined Owner's Manual covers ALL of a client's policies: the text warns to take figures from the right policy's section, but nothing proves it.
10. **"No change" is a typed flag** that can disagree with the figures (`no_change` true while old and new differ). A program can compute it.
11. **The R20 fee check is a soft warning** the script prints and never enforces ("it doesn't block the build, so still check it yourself").
12. **The four-block structure, the standard "not compiled" wording, the accepted quote being one of the compiled ones, and the CP numbers** are all text rules the script only partly applies (it defaults the wording).
13. **The 18-point visual check is by eye.** Most of it can be proven by reading the PDF back: the ID field under Owner, the heading order, the premium label, the CP line, the narratives not cut off, "N/A", the two empty date form fields with their names, the typed names, FSP45946 and Paul Kafentzis, the page count. Only the look (logo overlap, signature-line spacing) needs an eye.
14. The script can be edited during a run ("extend this script and update this file").
Standards and clutter:
15. About 25% of the 534 lines are copied universal rules, the Delivery gate, two long standing-rule blockquotes and the changelog; the stamp and the changelog are typed by hand (S2); the full changelog lives in a project file outside the skill. A line of trigger phrases sits under the Index.
16. No run state, no tests, no checker. `build_sroa.py` has no input validation beyond that warning.

## Duplications between skills
- The routes, the client-folder wording and the "labels only" Fact Find workaround are repeated in the ROA skill and here (no output duplication).
- **Side issue, not this skill (noted, not chased):** `client-pipeline-board` says the ROA date for a Life Cover ROA is the date on the risk application found in the signing transcript, and for Investments the later of that and the client's reply email; `wr-roa-builder` says it is the date the client gave the go-ahead (the Follow-Up Notes for Risk, the client's own reply email for Retirement and Investment). These disagree. For the SROA the board correctly says it does not source the date; the SROA asks Paul.

## Score against the 13 ingredients
Full 0. Partial 6 (1 short entry page, 2 inputs, 5 evidence, 6 built by program, 10 one reply one question, 12 history outside). Missing 5 (3 step driver, 4 reading lock, 9 one checker, 11 tests, 13 package and upload). Not applicable 2 (7 short means short, 8 sorted actions).

## What a program CAN and CANNOT do here (honest)
- CAN: force the steps; serve the schedule and quotes page by page; check each old figure appears in the Current Policy Schedule (the right policy's section) and each new figure in the accepted quote, each block's figures in its own quote; compute "No change"; refuse a Premium line that is not "incl. R20 policy fee" or whose figure is not in the quote; keep `build_sroa.py` fixed; read the finished PDF back and prove most of the 18 visual checks; derive the file name; log the routes and never overwrite without your yes.
- CANNOT: decide the advice, the reason, which debt is renamed or new (it stops and asks you), BrightRock's category mapping (Claude's own interpretation, confirmed rules only), or that a figure sits in the right place on the page (only that it appears); see the logo and the signature-line spacing; prove the file reached the folder beyond the listing the chat reports.

## Yes/No list for Paul (recommended answers in brackets)
1. **Client data in the live files:** the rebuild removes every real-looking name, ID and CP number and uses invented people only. The old versions stay in claude.ai's version history for you to remove if you wish. (Yes)
2. **Derive first, one confirmation table, one question** (as for the ROA): the quotes compiled and the accepted one, the policy number, the CP numbers, the client's full name and ID, the Current Policy Schedule figures come from the documents with their source. You are asked only for: the reason for the change in your own words, whether it is investment-linked (and the portfolio reason), the SROA date (confirmed against the signed quote), and anything the program cannot settle (for example a debt that may be renamed or new). (Yes)
3. **Figures are proven, "No change" is computed, the R20 rule is enforced:** the chat types the old and new figures and the program checks each appears in the right document's text and that "No change" really means old = new. A Premium line that is not "Premium (incl. R20 policy fee)", or whose figure is not in the quote's own "including the policy fee" total, is refused (today only a soft warning). **Is R20 still the monthly policy fee?** (Yes; please say if it changed)
4. **Fixed script, PDF checked:** keep `build_sroa.py`'s logic as the base, make it unchangeable during a run, and have the checker read the finished PDF back and prove what it can. Only the look stays with the chat's eye. (Yes)
5. **The file name is derived by the program, one run per policy,** never combined. (Yes)
6. **Saving:** the PDF goes into the client's Servicing folder through the computer, then Microsoft 365, then Zapier, every try logged, never overwriting without your yes, never touching another broker's folder, and it is sent in the chat. (Yes)

## Status
Phase A report given to Paul 03/11/2026.

## Paul's answers (03/11/2026)
"Agree to all - as long as the skill works as it was intended to execute": yes to 1 to 6 as recommended, with one condition: the rebuilt skill must produce the same SROA as it was meant to. (1) No real-looking client data in the rebuilt skill. (2) Derive from the documents, ONE confirmation table, one question. (3) Figures proven against the documents, "No change" computed, the R20 rule enforced (Paul did not say R20 had changed). (4) `build_sroa.py` stays the fixed base; the checker reads the PDF back. (5) The file name derived by the program, one run per policy. (6) Saving through computer, Microsoft 365, Zapier in order, never overwriting without his yes.

Next: Phase B (plan) given to Paul 03/11/2026, waiting for his approval.
