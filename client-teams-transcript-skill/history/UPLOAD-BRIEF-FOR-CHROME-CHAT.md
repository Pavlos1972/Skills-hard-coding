# Brief for a Claude chat that has Claude in Chrome: upload one skill and switch the old copy off

You are helping Paul Kafentzis, a financial adviser. He uses "Skills" in his claude.ai account. Another Claude (Claude Code) rebuilt one of his skills, `client-teams-transcript-skill`, and tested it on made-up data (176 tests passed). Claude Code cannot save into his Skills, so Paul has asked YOU to do the upload for him in his browser, using Claude in Chrome. Paul asked for this himself. Do exactly the steps below, nothing more.

## The facts
- Skill name: `client-teams-transcript-skill`
- File to upload: `client-teams-transcript-skill-20261029-1338.zip` (81,540 bytes, 21 files). It is on Paul's computer in this folder: **[PAUL: WRITE THE FOLDER HERE, for example Downloads]**
- NEW version: its SKILL.md contains the line `Last updated: 2026-10-29 13:38 (Athens time)` and its first section is called `Index`.
- OLD version (already in Paul's account, switched on): its SKILL.md contains `Last updated: 2026-10-08 14:20` and its first section is called `UNIVERSAL OPERATING RULES - READ FIRST`.
- Both have the SAME name and the SAME description, so you cannot tell them apart by name. Use the "before" list (step 3) and the test (step 7).

## Hard rules
1. Work only in Paul's Skills settings page on claude.ai. Do not open other pages. Do not change any other setting, and do not touch any other skill.
2. NEVER delete anything. Never click Delete, Remove, Replace or Overwrite. If the page offers to replace the old skill, STOP and ask Paul. The old copy is meant to stay as a backup, switched off.
3. Do not unzip, edit or rename the zip file. If the upload is refused, copy the error message exactly, show it to Paul, and stop.
4. Do not run the skill on any client. Do not open any client file.
5. If "code execution" (or "code execution and file creation") is switched OFF on the same settings page, tell Paul and stop. Do not switch it on yourself.
6. If the extension is not connected, a tool fails 2 or 3 times, or anything does not match what is written here, STOP, explain what you tried, and ask Paul. Do not improvise.

## Steps
1. **Start.** Load the Claude in Chrome tools (the chrome-browser skill explains how). Look at the open tabs, then open a NEW tab and go to claude.ai. If the extension asks for site permission, tell Paul and wait.
2. **Open the Skills page.** In Paul's settings, find Skills (it is called Settings > Features in some versions and Customize > Skills in others). Check that code execution is on (rule 5).
3. **"Before" list.** Write down every skill name and whether it is on or off. Write down how many entries are called `client-teams-transcript-skill` (expected: exactly 1, switched on) and anything the page shows for it (dates, description).
4. **Upload.** Click the button to upload or add a skill and choose the zip file named above. A browser helper often cannot operate the computer's own file-picker window. Try your file-upload tool first. If you cannot choose the file, tell Paul: "Please pick `client-teams-transcript-skill-20261029-1338.zip` in the file window, then tell me when it is done," and wait. Then finish any confirm step. If it asks to replace the existing skill, follow rule 2.
5. **"After" list.** Reload the page and list the skills again. One of these happened:
   - (a) Two entries named `client-teams-transcript-skill`: go to step 6.
   - (b) Still one entry: it may have replaced the old one. Tell Paul in plain words that the old copy is no longer in the account as a backup (Paul still has his original saved as a file). Go to step 7.
   - (c) An error: rule 3.
6. **Switch the old one OFF.** The OLD one is the one that was in the "before" list, or the one with the older date. Use its on/off switch to turn it OFF. Leave the NEW one ON. Never turn both off. Never delete. If you cannot tell which is which, open each one if the page lets you and look for the `Last updated` line above; if you still cannot tell, ask Paul.
7. **Test, using a new chat.** Open a new claude.ai chat in a new tab and type exactly: `Do not run any task and do not use any client information. Open the skill client-teams-transcript-skill and tell me only (1) the line that starts with "Last updated" and (2) the title of the first section after the main title.`
   - Correct answer: `Last updated: 2026-10-29 13:38 (Athens time)` and `Index`.
   - If it quotes `2026-10-08 14:20` or `UNIVERSAL OPERATING RULES`, the old skill is the one switched on. Swap the switches (new ON, old OFF) and test once more. If it is still wrong, stop and tell Paul.
8. **Report to Paul in plain, short words:**
   - the "before" list (how many entries, on or off);
   - what happened at the upload, with any message word for word, and whether Paul had to pick the file himself;
   - the "after" list, and which entry you switched off;
   - what the test chat answered, quoted;
   - anything unusual.
   Finish with: "Uploaded and tested. Not confirmed live until you confirm." Do not say it is live. Paul will confirm.
