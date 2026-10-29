# What changed in the Teams transcript skill, in plain words

For Paul. Nothing here is live until you upload it and tell me.

## What stayed the same
Every rule the old skill had is still there, in the step where it applies. A program (`tools/inventory.py`) went through all 466
sentences of the old skill and checked each one: 297 are still there word for word, 39 are reworded (each with a recorded reason),
130 were dropped on purpose (listed below) and **none were lost without a record**. It also caught one sentence I had lost by
mistake (the rule that the eight-area structure applies to a first meeting too). I put it back.
The skill's name and its description (the words that make Claude pick it) are exactly as before.

## What is new
- **A program drives the job, one step at a time.** Claude cannot see step 6 until step 5 is proven.
- **Both reads of the transcript are enforced.** The text is handed over in order, twice. A quote that is not really in the transcript is refused the moment it is typed.
- **Your eight areas** each have their own heading, in your order, in the Planner note and the PDF: Risk, RA, Investment, RGAR, EGAR, Medical Aid, Will, Short-Term. "Other" appears only when something notable was said. One line names the areas not discussed.
- **The Planner note is a copy-ready page** with a Copy note button, made by the program, the same every time. I tested the button in a real browser: it copies bold text and bullets, no stray asterisks, and the page fits a phone.
- **The PDF is built by the program** and named by the program, so a text draft cannot take its place.
- **The Teams message to Sitamah** is the one from your Fact Find skill (same wording, "2nd", "3rd" and so on, follow-up sentence only for a real agreed date). It goes through Zapier only, after your yes. The program prints the exact Zapier steps.
- **Client file first, then Paul.** Every document read is logged. Every attempt to reach a file is logged, in order: local drive, Microsoft 365, Zapier. Claude can only ask you after all three failed, and the program hands it the exact words, with the errors.
- **The checklist at the end** says PASS or FAIL for every item. If it is not in the reply, the job is not finished.
- **A self-test at the start.** If the chat is missing something it needs, it stops and tells you instead of doing something easier.

## What I removed on purpose (your yes or no for each)

| # | Removed | Why | My advice |
|---|---|---|---|
| 1 | The long change history at the top of the old skill (about 14 lines of "what changed and why") | History does not belong in the instructions; it is saved in full in the repo | Yes, remove |
| 2 | The two worked examples that used real client details | Standard S11: no client data. Replaced by an example made from invented data | Yes, remove |
| 3 | Old rule 1 ("re-load this skill after any compression") and old rule 9 ("use the Update skill card") | Replaced: the program remembers where the job is up to, and skills with programs are changed in Claude Code and uploaded as a zip | Yes, remove |
| 4 | Dates in brackets after headings, such as "(Paul's rule, 06/10/2026)" | History again. 13 of them, all listed in `history/dated-attributions-removed.txt` | Yes, remove |
| 5 | The old 21-point checklist as one long sentence | Kept, but as a table that says which points the program checks and which are Claude's judgment | Keep the table |

## Two things I need you to decide
1. **WhatsApp calls.** Your Fact Find skill defines the Teams message only for Teams appointments ("Teams Appointment Completed"). I left it out for WhatsApp calls. Should a WhatsApp call also notify Sitamah, and in what words?
2. **Old stories inside the rules.** Some rules still carry a short "named precedent" story about a past client (with names removed). They help Claude see what a mistake looks like. Keep them, or remove them?

## What I could not do from here
- **I cannot save into your Skills.** From this session I can only list and search your skills, not write to them. I give you a ready zip (`releases/`); you upload it. Your skills show up as coming from a plugin, and the plugin list is empty on my side, so **I cannot tell whether uploading replaces the old one or adds a second copy.** After uploading, check that only one "client-teams-transcript-skill" is switched on, and switch the old one OFF (do not delete it: it is your backup).
- **I cannot run it inside your chat.** I tested everything here on invented data (98 tests, including a full run from start to PASS and the Copy button in a real browser). The first real use is the trial: run it on a meeting you already have a note for, and compare.
- **I could not check how a real Teams transcript file is laid out.** The program finds timestamps and the stated duration in a general way. If your real file looks different, the first step may stop and tell you what it could not read. Then I fix it.

## Your original, untouched
Your original skill text (with the real client names) was given to you as a file. It is not kept in the repo. The repo keeps the same text with names replaced by placeholders, in `history/`.
