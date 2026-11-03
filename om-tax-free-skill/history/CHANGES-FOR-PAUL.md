# om-tax-free-skill: what changed, and your Yes/No list (03/11/2026)

No client data is kept in the new skill. Everything in it is invented (Pat Samplecase, invented funds and numbers). The old text is archived word for word in `SKILL.2026-10-14.md`. The rule-by-rule check of the old skill against the new one: 375 rules, 0 unaccounted (49 kept word for word, 259 reworded, 67 dropped with a recorded reason; see `INVENTORY-REPORT.md`).

## What the skill does now, in plain words
- A program walks the chat through 9 steps and refuses to skip one: find the documents (computer, then Microsoft 365, then Zapier, every try logged), read them page by page, enter the answers, show you ONE confirmation table and ask ONE question, build, save, draft, message Sitamah, final audit.
- Every figure, name, age, employer, income, contribution, start date, fund, allocation and fee the chat types must be in the right document's text. Percentages keep their own decimals (0.73% is refused when the quote says 0.733%). The program adds up the fee total and checks the allocations add up to 100%.
- You are asked only for: the start date (always, your own double-check), the meetings already held (pre-filled from the file names), the next meeting date and time, and the Risk Profile only when no completed questionnaire exists.
- The email is filled from the fixed template by the program: no placeholder can remain, every weekday is computed, the full copy has the logo, the saved copy does not. The program also makes the exact text to paste into the Outlook draft.
- After you say yes: the no-logo copy is saved in Comparative Quotes (never overwriting without your yes), the chat makes the Outlook draft with Chrome and gives the program the read-back (it must show To the client, Cc Sitamah, the exact subject, High importance, tables open = close, one "Kind regards,", no placeholder, no Loop box, every fund, fee and date). Only then does the Teams message to Sitamah go (through Zapier, greeting by the clock, wording by the program) and its read-back is checked too.
- A child's plan, a lump sum, a plan owner under 18 or who is not the client, or two sources that disagree: the program refuses and the chat stops and asks you. No wording is invented.
- The reply to you is the short audit: one line per check with a tick or a cross.

## Fixed while building (nothing for you to decide)
- The placeholder check in the old Step 4 could never fire (it looked for "@@"). The program now checks all three copies properly.
- The real client's name was removed from the date script; the script stays.
- The template's two typos were fixed ("contribute of R" is now "contribute R"; "recommend are" is now "recommended"), as you agreed.
- The tax facts in the email (R 46,000.00 a year, R 500,000.00 lifetime, 40%) now live in ONE place, `assets/tax_facts.json`, so next March is one edit. They are kept exactly as in your template. I have NOT verified them.

## Your new Yes/No list (my recommended answer in brackets)
1. **The "Sent:" line in the saved copy and the chat copy** is the build date and time in South African time, for example "Thursday, 05/11/2026 10:15". The old text only said it must be "filled in". (Yes)
2. **The fund fact sheets and the Strategy Summary are checked for being there** (and each fact sheet must show its fund's name) but are not read page by page. Only the quote, the Fact Find Summary (and an older version), the questionnaire and the Overview are served page by page. (Yes)
3. **Next meeting must be today or later, and meetings already held must not be in the future.** (Yes)
4. **`assets/wr_logo.png` was removed.** The template carries its own logo (a different image) and nothing used the file. (Yes)
5. **The Teams message to Sitamah goes only after your one yes and a checked draft.** Today's text sent it automatically as soon as the draft was verified. (Already agreed in the Phase A list; listed here so you see it in the build.)
6. **STILL OPEN from Phase A, question 5 (the signature):** when one of these emails reaches a client, does your signature show once or twice? The skill keeps today's way (Claude inserts "Paul K New" in the draft) and says so in the audit. If you tell me the server adds it, it is one word to change in `assets/settings.json`.

## What a program cannot prove (still your eye or your judgement)
- That a figure sits in the right row of its document: the program proves it appears in the document, not where.
- A scanned page with no readable text (often the Risk Tolerance answers): the program says so and the chat must view it as an image.
- The paste into Outlook and the Zapier send themselves: the program builds the exact text and checks the read-back the chat gives it, but it cannot see Outlook or Teams.
- That the draft looks right in Outlook (bold, table borders, blank lines): the program checks the text and the tags.
- That the file really sits in the folder and the message really arrived: the chat types the listing and the read-back.
- The fixed tax facts in the email and the signature question above.
- **Not yet proven on a real client.** I have never seen a real Outlook read-back or a real OM quote. The checks search for the values rather than assuming a layout, but the first real run may need one fix.

## The old versions
The old versions of this skill stay in claude.ai's version history and hold a real client's name (in the date script). Only you can remove them.
