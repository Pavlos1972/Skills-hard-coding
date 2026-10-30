# What changed in the Teams transcript skill, in plain words

For Paul. The 17:53 version was uploaded as v34 (reported by the Chrome chat; the line counts in its replace box match my files). Nothing is called live until you have tried it on a real meeting and told me.

## After your first real-case trial (29/10/2026): what I changed, in plain words
You ran the skill on two real clients and told me four things. Here is what is now different. This version is **not uploaded yet**: you have the sample to look at first.

1. **The Planner note is short.** Each area you discussed has 1 to 3 one-line bullets (about 20 words at most), and only the actions for now. The detail stays in the PDF. If a note is longer, the program refuses it and the chat has to shorten it.
2. **The PDF has limits too:** at most 4 bullets per area, each at most 45 words, and two pages at most. I tested this on the content of your household PDF: it fits in two pages.
3. **Actions are sorted, using your ten answers.** An action is for **now** (Sitamah can do it today), or for **later** with what it waits for (a cession waits until the policy is issued; it is listed in the PDF under "Coming up", not in the Planner note). These are never actions, and the program refuses them: what the client decides (it is shown as "PENDING - client deciding"), cancelling credit life, sending quotes or the what's-next email, setting up the next meeting, and Paul's own steps. The one credit-life action left is "get the credit-life details". Your row 2 (checking with Liberty what the income protector would pay) I could not turn into a rule because you gave no reason, so the program now ASKS you whenever that kind of action comes up.
4. **"Next Steps" in the PDF lists only what the client must do.** Before, it also said "Paul will send the updated quotes" while Sitamah had the same action.
5. **Action points are put in order, sifted, and the skill asks when it is not sure (your words).** The actions are listed in the order Sitamah would do them: the earliest deadline first (the due date is shown after the action), then logical order, so nothing comes before what it depends on. What is not relevant is left out and listed at the end, with the reason, so you can see it. When the skill is not sure (is it relevant, is it for now or later, is it an action at all, what comes first), it stops and asks you in ONE message with every question and its own suggested answer, and it writes down your words. I did not touch `planner-interim-procedure`, as you said.
6. **The message to Sitamah is now shown together with the Planner page and the PDF, in one reply, with one question:** "Shall I post this message to Sitamah in Teams?". I found why it was never offered: my own instructions said to show it only after you had approved everything else. That is gone, and the steps now tell the chat not to end its reply before the message is in it. I could not see the end of that chat, so I cannot tell if it also skipped the step.

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
an invented fact with an unrelated quote could pass; a run could pass for the wrong client or date; a very careless run could reach PASS; a correction did not re-open the hand-over; the Teams message could go out and the run then fail; some declarations were never cross-checked against the text; and malformed input could crash the checker. All fixed (226 tests now).

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
- **I cannot save into your Skills, so a chat with Claude in Chrome uploads it for you.** From this session I can only list and read your skills. What works (first done 29/10/2026): you give that chat the upload instructions that the packaging program now writes next to every zip. **Uploading replaces the skill. It does not make a second copy.** Your old version stays in the skill's version history (a dropdown of v32, v31 and so on), and that history is the backup. So there is nothing to switch off. Your first upload became version v33, and a fresh chat quoted the new "Last updated" line, which proves the new version is the one answering. The Chrome chat reported this; I did not see it myself.
- **I cannot run it inside your chat.** I tested everything here on invented data (226 tests, including a full run from start to PASS and the Copy button in a real browser). The first real use is the trial: run it on a meeting you already have a note for, and compare.
- **I have not seen a real Teams transcript file.** The program reads the usual layouts (time before the name, time after the name, `0:00:05.000 -->` style) and stops loudly if it cannot read any times. If your real file looks different, I need the first 15 lines to fix the reader.
- **Try the Copy button yourself.** I published a sample Planner note, made by the new program from invented data, as a private page: https://claude.ai/artifact/UXLdZN66XernnbTBXV4Yej . Click Copy note, then paste into the Planner / AdviceTech task chat (or Word) and tell me if the bold and bullets came through. The page tool accepted the program's page, so publishing works. The page window may restrict rich copying, so the page has three ways to copy, best first (bold and bullets; select-and-copy; plain text), and it says which one worked. The note can also be shown as plain formatted text if the page tool is unavailable.
- **Two sibling skills still use the old headings.** `ff-population-transcript` (its Planner-note instructions) still names the old combined headings. They will be brought in line when those skills are converted.

## Your original, untouched
Your original skill text (with the real client names) was given to you as a file. It is not kept in the repo. The repo keeps the same text with names replaced by placeholders, in `history/`.
