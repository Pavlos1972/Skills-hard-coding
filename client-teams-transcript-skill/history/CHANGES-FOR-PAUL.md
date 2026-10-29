# What changed in the Teams transcript skill, in plain words

For Paul. Nothing here is live until you upload it and tell me.

## What stayed the same
Every rule the old skill had is still there, in the step where it applies. A program (`tools/inventory.py`) went through all 466
sentences of the old skill and checked each one: 290 are still there word for word, 46 are reworded (each with a recorded reason),
130 were dropped on purpose (listed below), and **none were lost without a record**. It also caught two sentences I had lost by
mistake while editing, and I put them back. The skill's name and its description (the words that make Claude pick it) are exactly as before.

## What is new
- **A program drives the job, one step at a time.** Claude cannot see step 6 until step 5 is proven.
- **Both reads of the transcript are enforced.** The text is handed over in order, twice. After each chunk Claude must record what is in it (or say in its own words why nothing needs recording) before the next chunk is shown. A quote that is not really in the transcript is refused the moment it is typed.
- **Nothing can be invented quietly.** Every bullet must quote the call or a document Claude actually recorded as read, and every figure (rand amount, quote number, percentage) must appear in one of those sources.
- **The run is tied to your request.** Claude must start it with the client and meeting date from your message. A transcript that never mentions the client, a report for the wrong client, or a wrong date all fail.
- **Your eight areas** each have their own heading, in your order, in the Planner note and the PDF: Risk, RA, Investment, RGAR, EGAR, Medical Aid, Will, Short-Term. "Other" appears only when something notable was said. One line names the areas not discussed.
- **The Planner note is a copy-ready page** with a Copy note button, made by the program, the same every time. Tested in a real browser: it copies bold text and bullets, no stray asterisks, and the page fits a phone.
- **The PDF is built and named by the program**, so a text draft cannot take its place.
- **The message to Sitamah** (for a Teams meeting or a WhatsApp call) is the `fact-find-summary` one, with (Review Client) or (Prospect) after the name as you said, decided from where the client's folder sits (and checked against the folders Claude actually read). Sent through Zapier only. The program shows it only when everything else has passed, so it can never go out and then the run fail. It records what Zapier stored, and your own words of yes.
- **Client file first, then Paul.** Every document read is logged, with a text copy so quotes can be checked. "Nothing on file" is accepted only after the searches are logged. Claude can ask you only after all three routes failed, and the program hands it the exact words.
- **A correction re-opens everything.** If anything is rebuilt, the page, PDF, checks and hand-over must all be done again; old receipts no longer count.
- **Every run says which version it is, and the date moves by itself.** The first words Claude says are: "Using client-teams-transcript-skill, last updated DD/MM/YYYY HH:MM (Athens time)". The date is read from the skill's own stamp, not typed anywhere. The final checklist repeats it, and warns if the skill was updated while a run was going. Whenever a skill is changed in future, the checker and the packager refuse it until it is re-stamped, so the date always changes with the skill and never otherwise. I did not put the date in the skill's name (names allow only lowercase letters, numbers and hyphens, five of your skills call this one by name, and it would go stale at the next fix).
- **A self-test at the start.** If the chat is missing something it needs (including the tool that reads Word transcripts), it stops and tells you.
- **The final printout** says PASS or FAIL for every item, plus a short "what Paul should glance at" list: the document with no text copy, the plain facts left out of the report and why, and your own words if you declined or approved the Teams message.

## An independent review, and what I did about it
After I built it, a separate reviewer tried to get round it as a careless AI would. It found real weaknesses; I fixed each one and added a test for it:
an invented fact with an unrelated quote could pass; a run could pass for the wrong client or date; a very careless run could reach PASS; a correction did not re-open the hand-over; the Teams message could go out and the run then fail; some declarations were never cross-checked against the text; and malformed input could crash the checker. All fixed (176 tests now).

## What I removed on purpose (your answer, 29/10/2026: yes to 1 to 4, keep the table in 5)

| # | Removed | Why | Your answer |
|---|---|---|---|
| 1 | The long change history at the top of the old skill (six long entries) | History does not belong in the instructions; it is saved in full in the repo | **Yes, remove** |
| 2 | The two worked examples that used real client details | Standard S11: no client data. Replaced by an example made from invented data | **Yes, remove** |
| 3 | Old rule 1 ("re-load this skill after any compression") and old rule 9 ("use the Update skill card") | Replaced: the program remembers where the job is up to, and skills with programs are changed in Claude Code and uploaded as a zip | **Yes, remove** |
| 4 | Dates in brackets after headings, such as "(Paul's rule, 06/10/2026)" | History again. 13 of them, all listed in `history/dated-attributions-removed.txt` | **Yes, remove** |
| 5 | The old 21-point checklist as one long sentence | Kept, but as a table that says which points the program checks and which are Claude's judgment | **Keep the table** |

## Your answers of 29/10/2026, all built in
- **The Sitamah message wording depends on Prospect or Review client.** Built in: (Review Client) or (Prospect) after the name.
- **WhatsApp calls also tell Sitamah (you said yes).** A WhatsApp call is when you speak to a client on WhatsApp instead of in a Teams meeting. There is no Teams transcript, so you give Claude your own recap and the skill makes a "WhatsApp Call Summary" PDF. The message to Sitamah is now the same as for a Teams meeting, but says "WhatsApp Call Completed" instead of "Teams Appointment Completed". **One thing I decided for you:** the 1st / 2nd / 3rd count for a WhatsApp call counts every meeting and call on file, plus this one. If you want it counted differently, tell me.
- **The old true stories inside the rules stay (you said keep).** Names are removed from them.

## What to expect, and what I could not do
- **It asks more of Claude than the old skill did.** The first real run will feel longer: a text copy of each document, a note per chunk, a reason for each dismissed keyword. That is the price of checking; if it is too heavy, tell me which part and I will ease it without losing the check.
- **A document without a text copy** is not blocked; it is flagged to you at the end, and the checks on its quotes and figures are skipped. Better than refusing outright when a PDF is only a scan, but it means you should glance at those items.
- **I cannot save into your Skills.** From this session I can only list and search your skills, not write to them. I give you a ready zip (`releases/`); you upload it. Your skills show up as coming from a plugin, and the plugin list is empty on my side, so **I cannot tell whether uploading replaces the old one or adds a second copy.** After uploading, check that only one "client-teams-transcript-skill" is switched on, and switch the old one OFF (do not delete it: it is your backup).
- **I cannot run it inside your chat.** I tested everything here on invented data (176 tests, including a full run from start to PASS and the Copy button in a real browser). The first real use is the trial: run it on a meeting you already have a note for, and compare.
- **I have not seen a real Teams transcript file.** The program reads the usual layouts (time before the name, time after the name, `0:00:05.000 -->` style) and stops loudly if it cannot read any times. If your real file looks different, I need the first 15 lines to fix the reader.
- **Try the Copy button yourself.** I published a sample Planner note, made by the new program from invented data, as a private page: https://claude.ai/artifact/UXLdZN66XernnbTBXV4Yej . Click Copy note, then paste into the Planner / AdviceTech task chat (or Word) and tell me if the bold and bullets came through. The page tool accepted the program's page, so publishing works. The page window may restrict rich copying, so the page has three ways to copy, best first (bold and bullets; select-and-copy; plain text), and it says which one worked. The note can also be shown as plain formatted text if the page tool is unavailable.
- **Two sibling skills still use the old headings.** `ff-population-transcript` (its Planner-note instructions) still names the old combined headings. They will be brought in line when those skills are converted.

## Your original, untouched
Your original skill text (with the real client names) was given to you as a file. It is not kept in the repo. The repo keeps the same text with names replaced by placeholders, in `history/`.
