# wr-sroa-builder: what changed, and your Yes/No list (03/11/2026)

No client data is kept in the new skill. Everything in it is invented (Pat Samplecase). The old text is archived word for word in `SKILL.2026-10-14.md`. The rule-by-rule check of the old skill against the new one: 477 rules, 0 unaccounted (8 kept word for word, 367 reworded, 102 dropped with a recorded reason; see `INVENTORY-REPORT.md`).

## What the skill does now, in plain words
- A program walks the chat through 8 steps and refuses to skip one: find the documents (computer, then Microsoft 365, then Zapier, every try logged), read them page by page, enter the answers, show you ONE confirmation table and ask ONE question, build, check, save, final audit.
- From a combined Owner's Manual only the pages of THIS policy are taken. One run per policy.
- Every figure, name, ID number, CP number and date the chat types must be in the right document's text: old figures in the Current Policy Schedule (this policy's pages), new figures in the accepted quote, each quote block's figures in its own quote. A figure that is not there is refused.
- "No change" is worked out by the program (old equals new); it can no longer disagree with the figures.
- The premium line must be "Premium (incl. R20 policy fee)"; a quote that does not state a total "including the policy fee" is refused (the old skill only printed a warning).
- The PDF is drawn by the same script as before (fixed during a run), then read back by the program: ID line under Owner, the four blocks in order, CP lines, the premium label, your reason word for word, "N/A" when the policy is not investment-linked, FSP45946 and Paul Kafentzis, no "Signed at", the two empty date fields, nothing clipped, the logo, the two signature lines. The file name is made by the program.
- The reply to you is the short audit: one line per check with a tick or a cross.

## A bug I found and fixed
In the flat list (any insurer except BrightRock's grouped layout), the line "Premium (incl. R20 policy fee)" was not recognised by the script's fixed order, so it landed at the end of the list instead of after Income Protection. The script now matches the name before the bracket. (Nothing for you to decide.)

## Your Yes/No list (my recommended answer in brackets)
1. **"No change" now shows the figure:** an unchanged line reads `ACI (Automatic Cover Increase): No change (5%)` instead of just `No change`, so the reader sees what stayed the same. (Yes. If No, it is a one-line change.)
2. **"(Accepted)" goes on whichever quote the client accepted** (FNA, Shortfall or Alternative). Before, only the Alternative Quote was named in the rules. (Yes)
3. **The Fact Find Summary is now one of the documents the program asks for and serves** (the old skill asked for it "up front" but did not require it). If you do not have one, you say so and your words are recorded. (Yes)
4. **The question "do you want the non-accepted quote(s) referenced for completeness?" is dropped.** Blocks 1 to 3 already show every compiled quote. (Yes. If No, I put the question back.)
5. **The grouped headings are for BrightRock only.** For another insurer the program uses the flat list (Life Cover, Disability Cover, Dread Disease, Income Protection, Premium, ACI, ABI, Retrenchment Cover) or stops and asks you. (Yes)
6. **The old template file `WR_Generic_Servicing_Record_of_Advice.pdf` is removed.** It was not a PDF but a zipped picture of the blank form, the script never used it, and the picture is kept in `history/original-template-layout.jpeg`. (Yes)
7. **The SROA date must be in the accepted quote or the acceptance email** (the signed or sent date), unless you choose another date and your words are recorded. Never today's date. (Yes)
8. **The client's everyday first name may differ from the legal name** (Pat for Patricia); the surname must be part of the legal name. (Yes)
9. **Is R20 still the monthly policy fee?** You did not say it changed, so the skill still uses R20. (Yes, unless it changed)

## What a program cannot prove (still your eye or your judgement)
- That a figure sits in the right row or column of its document: the program proves it appears in that document, not where.
- A scanned page with no readable text: the program says so and the chat must view it as an image.
- Your reason for the change, the SROA date's choice, which quote was accepted, whether a debt is renamed or new (the program stops and asks you).
- How the pages look: the logo, spacing, crowding. The program saves page images for the chat to look at.
- That the saved file really sits in the folder (the chat types the folder listing in).
- Not yet proven on a real client: a real Owner's Manual and a real BrightRock quote may word things differently from my invented ones; the first real run may need one fix. In the PDF the arrow between old and new figures looks right to the eye but a text reader sees it as "fi" (the old script did the same); the checker allows for that.

## The old versions
The old versions of this skill stay in claude.ai's version history and hold two real-looking 13-digit ID numbers and a CP number. Only you can remove them.
