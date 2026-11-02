# Standing rules for every run (shown once when the run starts; they apply to every step)

*These rules come before everything else in this skill. They apply from the first message to the last, not just at the start, and they are repeated here at the top because long conversations get compressed and only the beginning of a skill survives. If anything below seems to conflict with these rules, these rules win.*


1. **The program drives the job; do not work from memory.** Run `python3 {scripts}/run.py next {run}` to see the current step, and `python3 {scripts}/run.py status {run}` after any long chat or compression to see where the job is up to. Each step shows its own rules when it is needed. Never work from a summary of the rules or from memory of them.
2. **Source first - never invent.** Write only what is in the source material (the Fact Find (Audio to Text) file, the transcript, the Overview, a client document or file) or in a named document this skill tells you to use. If a line is unclear, garbled or ambiguous, do not turn it into a fact: flag it to the user. "It seems implied", "it is usual" and "it would make sense" are not sources.
3. **Read before you write.** Read the source material completely and carefully - at least as many times as this skill requires - before drafting anything. Searching for keywords is not reading.
4. **Check before you claim.** Never tell the user something is done, saved, sent, visible or working until you have checked it yourself (open the file, list the folder, look at the screen). Say what you checked.
5. **Deliver everything this skill lists, every time.** A run is not finished until every deliverable this skill names has been produced AND handed over exactly the way this skill specifies (shown in chat, sent as a file in the chat, saved to the named folder). Before you reply, list each deliverable and confirm each was handed over.
6. **Every correction re-opens the whole task, not just the item.** When the user corrects anything: (a) go back to the source and re-check that point and everything related to it; (b) fix it everywhere it appears, in every deliverable; (c) re-run this skill's full checklist; (d) re-deliver every affected deliverable in full, as in rule 5. Never fix only the item named and stop.
7. **Never lower the standard.** A correction, a frustrated user, a short request or a "quick" task does not relax any rule in this skill.
8. **If a rule cannot be met, stop and say so.** State exactly which rule or step could not be completed and why. Never hand over partial work as if it were complete.
9. **Changes to this skill are made only in Claude Code** (SKILL-STANDARDS.md S7), tested there, and uploaded by Paul as a zip. Never edit the skill, its steps or its programs during a run, never create a second copy of the skill, and never say a change is live until Paul confirms he uploaded it.
10. **Identify files by what they are, not only by what they are called - and open everything you stage.** File names vary. List the whole folder, treat every file that could plausibly be the thing you need (similar name, dated the meeting date, same client) as a candidate, and OPEN each one before deciding. Never conclude "it does not exist" from a name mismatch, and never stage or download a file without reading it. If you are unsure what a file is, open it and look.
11. **Source order - this order applies to every Fact Find run:**
    1. **FIRST and primary: the Fact Find form's data file, `Fact Find (Audio to Text) - [date] - [Name Surname]`** (the JSON the new Fact Find form saves, and its PDF; the name stays as it was). Every field starts from this file. Check its `schema` version every run (Step 1b).
    2. **SECOND, and just as important: `Teams meeting transcript - [date] - ([Name Surname])_ Annual Review [year]`** (or the client's equivalent transcript file name).
    3. **Also: the client's latest Overview** in the `1. Overview` folder, if there is one, as a point of reference.
    4. **LAST RESORT, only if the Audio to Text file (point 1) is absent: the `Fact Find (Manual)` PDF** (Paul's filled-in copy of the template, whatever its file name). If the Audio to Text file exists, do not go looking for a Manual Fact Find at all.
    **When the Audio to Text file and the transcript/recording differ, the Audio to Text file wins, and the difference is always flagged** (quote both values and where each came from). **Whatever is populated in the Audio to Text file is used and recorded in the report, whatever its status (`confirmed`, `preset`; `heard`, `verify` in an older file).**
12. **Say which version is running.** The first words of your first reply to Paul are the sentence the program prints under "SAY THIS TO PAUL FIRST" (this skill's name and its Last updated date and time, Athens time). It comes from the skill's own stamp, so it changes with every update; never type a date yourself. The final printout repeats it. If the sentence says NOT STAMPED, tell Paul.
13. **Say which font was really used.** The PDF is set in Aptos when Aptos is installed where the skill runs. If it is not, the program uses a named substitute and prints which one; tell Paul in your reply and never say Aptos when it was not used.
14. **Never print or edit what is not yours.** The form's own summaries, its drafted action list, its parking list and its cost counters are never a source and never printed. The form's data file and PDF, and the Manual Fact Find, are read-only for this skill.

The names Step 1b, Step 3, Step 5a and so on in these pages are the rule names from the original skill. The program's own numbering (STEP 3 of 15) is separate.

## Delivery gate for this skill (rules 5 and 6 applied)

A run is complete only when ALL of these are done and confirmed in one line each: (1) the Fact Find Transcript PDF (Step 5) was drawn by the program from content.json, verified and sent in the chat; (2) the same PDF was saved in the client's own `2. Fact Find` folder per Step 5a and the saved file checked (listed back, size equal to the local file); (3) the final re-verification pass (Step 3a) was completed, including the form cross-check and the source report; (4) the Fact Find Summary (Step 7a) was handed to `fact-find-summary`; (5) the Planner / AdviceTech note and the message to Sitamah (Steps 7b and 8) were handed to the Teams transcript program, which makes them once, and are shown in the same reply with one question; (6) `verify.py` printed `RESULT: PASS` and its whole printout is in the reply. **For two spouses in one meeting (Step 1d) every item above is done once per spouse.** After ANY correction, repeat (1) to (5) for every deliverable that changed (the Teams message is not resent unless Paul asks).

## Deliverables of a run

1. The **Fact Find Transcript PDF**, `Fact Find Transcript - DD.MM.YY - (Name Surname).pdf` (the date is the form's Date completed): one file, a PDF only (never a Word file), saved into the client's `2. Fact Find` folder.
2. The **source report and the glance list**, printed by `verify.py` and pasted into the reply.
3. The hand-overs, made by the other two skills from this PDF and this meeting: the Fact Find Summary (`fact-find-summary`), and the Planner note page and the message to Sitamah (`client-teams-transcript-skill`). This skill never writes a second message and never builds a Planner note.

## Where this skill sits in the client journey

The form saves its `Fact Find (Audio to Text)` PDF and data file into the client's folder. This skill takes them as the FIRST source, adds the Teams transcript, the latest Overview and the client's other documents, and combines them into the completed Fact Find: the Fact Find Transcript PDF, a saved report in its own right. `fact-find-summary` then takes that report and makes the Summary PDF.
