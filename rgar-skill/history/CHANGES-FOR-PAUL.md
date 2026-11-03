# rgar-skill: what changed, and your Yes/No list (03/11/2026)

No client data is kept in the new skill. Everything in it is invented (Pat Samplecase, an invented RGAR and Fact Find Summary). The old text is archived word for word in `SKILL.2026-10-14.md`. The rule-by-rule check of the old skill against the new one: 420 rules, 0 unaccounted (10 kept word for word, 205 reworded, 205 dropped with a recorded reason; see `INVENTORY-REPORT.md`).

## What the skill does now, in plain words
- A program walks the chat through 9 steps and refuses to skip one: find the documents (computer, then Microsoft 365, then Zapier, every try logged), read them page by page, enter the answers, show you ONE confirmation table and ask ONE question, build, save, draft, message Sitamah, final audit.
- Only two documents are needed: the RGAR from Alwyn and the Fact Find Summary. With no Fact Find Summary the skill stops and asks you (no raw Fact Find, no 8:45am window, no device-bridge visual read).
- Every RGAR figure (date of birth, retirement age, years until retirement, current and future expense values, lump sum, monthly amount, escalation, sustainability age, recurring investment) must be in the RGAR's text, and next to its label where the label can be found. Employer, job title, gross income, name, age and email must be in the Fact Find Summary.
- **The net monthly target** must be the first figure after the label "Net amount needed at retirement" (or the old wording "Net Amount Needed (today's terms)") in the Fact Find Summary: the Reduced Quote's contribution target can never be taken by mistake. No label found: the run stops.
- **The age** in the email is checked against the date of birth in the RGAR: a difference stops the run and asks you.
- **A lump sum or monthly amount of R 0** stops the run and asks you for wording. A recurring investment of R 0 raises a flag to you.
- The weekdays and the shortfall period (the 1st of the month after the next meeting, and the same day "years until retirement" later) are worked out by the program.
- The email is filled from the fixed template by the program: no placeholder can remain, To is the client's email, Attachments is the real RGAR file name, Sent is the build date and time. The full copy has the logo, the saved copy does not. The program also makes the exact text to paste into the Outlook draft.
- After you say yes: the no-logo copy and a copy of the RGAR PDF are saved in the RA transaction folder's Comparative Quotes (never overwriting without your yes), the chat makes the Outlook draft with Chrome and gives the program the read-back (To the client, Cc Sitamah, exact subject, High importance, tables open = close, one "Kind regards,", no placeholder, no Loop box, every figure and date). Only then does the Teams message go, through Zapier with real formatting (greeting by the clock, wording by the program), and its read-back is checked too.
- The reply to you is the short audit: one line per check with a tick or a cross.

## Fixed while building (nothing for you to decide)
- **"as a Analyst":** the template said "as a [JOB TITLE]", so a job title starting with a vowel read wrongly in a client email. The program now writes "as an Analyst" (a or an by the first letter, with exceptions for words like University). A title such as "Hour..." would still read "a Hour": say so if you ever see one.
- The template header's "To:" showed the client's name; it now shows the email address, as the old rules said. "Attachments:" shows the real RGAR file name, not a made-up pattern. The placeholder `[MEETING_DATES_LIST]` was renamed so the program can check for leftovers.
- The old sanity check only counted tables; the program now checks every copy for leftover placeholders and checks the header, the weekdays and every figure.
- `assets/wr_logo.png` was removed: the template carries its own logo (a different image) and nothing used the file. The date script stays unchanged.

## Your new Yes/No list (my recommended answer in brackets)
1. **Match-by-label for the RGAR figures is "soft":** the program refuses a figure that is in the RGAR but next to a different label, but only when it can find the label. I have never seen a real RGAR, so a label I guessed ("Current value", "Future value", "lump sum", "monthly recurring", "years until retirement", "sustainable until") may be worded differently; then the program only proves the figure is somewhere in the report and says so. (Yes)
2. **The "a / an" fix before the job title.** (Yes)
3. **The Sent line is the build date and time** in the form "Thursday, 05/11/2026 10:15" (the old template had "[DAY], [DD MONTH YYYY] [HH:MM]"). (Yes)
4. **The Teams message names the client in full in the first line and by first name in "It is in {first name}'s folder"**; the old text said {Client} in both places. (Yes)
5. **STILL OPEN from Phase A, question 8 (the signature):** when one of these emails reaches a client, does your signature show once or twice? The skill keeps today's way (Claude inserts "Paul K New") and says so in the audit. If you tell me the server adds it, it is one word to change in `assets/settings.json`: the same word as in the Tax-Free skill.

## What a program cannot prove (still your eye or your judgement)
- That a figure sits in the right row of its document where the label was not found.
- A scanned page with no readable text: the program says so and the chat must view it as an image.
- The paste into Outlook and the Zapier send themselves: the program builds the exact text and checks the read-back the chat gives it, but it cannot see Outlook or Teams.
- That the draft looks right in Outlook (bold, blank lines): the program checks the text and the tags.
- That the files really sit in the folder and the message really arrived: the chat types the listing and the read-back.
- That the RGAR matches the product being proposed (the program only flags a recurring investment of R 0).
- **Not yet proven on a real client.** I have never seen a real RGAR or a real Outlook read-back. The checks search for the values rather than assuming a layout, but the first real run may need one fix.

## The old versions
The old versions of this skill stay in claude.ai's version history. They hold no client name.
