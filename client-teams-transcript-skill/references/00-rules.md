# Standing rules for every run (shown once when the run starts; they apply to every step)

*These rules come before everything else in this skill. They apply from the first message to the last, not just at the start. If anything below seems to conflict with these rules, these rules win.*

1. **The program drives the job; do not work from memory.** Run `python3 {scripts}/run.py next {run}` to see the current step, and `python3 {scripts}/run.py status {run}` after any long chat or compression to see where the job is up to. Each step shows its own rules when it is needed. Never work from a summary of the rules or from memory of them.
2. **Source first - never invent.** Write only what is in the source material (transcript, quote, document, file) or in a named document this skill tells you to use. If a line is unclear, garbled or ambiguous, do not turn it into a fact: flag it to the user. "It seems implied", "it is usual" and "it would make sense" are not sources.
3. **Read before you write.** Read the source material completely and carefully - at least as many times as this skill requires - before drafting anything. Searching for keywords is not reading.
4. **Check before you claim.** Never tell the user something is done, saved, sent, visible or working until you have checked it yourself (open the file, list the folder, look at the screen). Say what you checked.
5. **Deliver everything this skill lists, every time.** A run is not finished until every deliverable this skill names has been produced AND handed over exactly the way this skill specifies (shown as a page, sent as a file in the chat, saved to the named folder). Before you reply, list each deliverable and confirm each was handed over.
6. **Every correction re-opens the whole task, not just the item.** When the user corrects anything: (a) go back to the source and re-check that point and everything related to it; (b) fix it everywhere it appears, in every deliverable; (c) re-run this skill's full checklist; (d) re-deliver every affected deliverable in full, as in rule 5. Never fix only the item named and stop.
7. **Never lower the standard.** A correction, a frustrated user, a short request or a "quick" task does not relax any rule in this skill.
8. **If a rule cannot be met, stop and say so.** State exactly which rule or step could not be completed and why. Never hand over partial work as if it were complete.
9. **Changes to this skill are made only in Claude Code** (SKILL-STANDARDS.md S7), tested there, and uploaded by Paul as a zip. Never edit the skill, its steps or its programs during a run, never create a second copy of the skill, and never say a change is live until Paul confirms he uploaded it.

10. **Say which version is running.** The first words of your first reply to Paul are the sentence the program prints under "SAY THIS TO PAUL FIRST" (this skill's name and its Last updated date and time, Athens time). It comes from the skill's own stamp, so it changes with every update; never type a date yourself. The final printout repeats it. If the sentence says NOT STAMPED, tell Paul.

11. **Short means short (Paul's rule).** The Planner note is one-line bullets and the actions for now; the PDF is two pages at most; every action is sorted `now` or `later` and put in order. The checker fails anything longer, unsorted or out of order. When you are not sure about an action, ask Paul (one message, every question with your suggestion) and record his words.

The names Step 1b, Step 4c, Step 6 and so on in these pages are the rule names from the original skill. The program's own numbering (STEP 3 of 14) is separate.

## Deliverables of a run (the run is finished only when all of these exist and `verify.py` prints PASS)

1. The **Planner note** as a copy-ready page (Artifact, with a Copy note button). Every meeting type.
2. The **PDF**: Follow-Up Appointment Summary Notes (Teams follow-up) or WhatsApp Call Summary. Sent in the chat, saved into the client's `2. Fact Find` folder, and the saved file listed back. Not for a first/Fact Find meeting (that meeting's PDF is the Fact Find Summary, made by `fact-find-summary`).
3. The **message to Sitamah** in Teams ("Teams Appointment Completed", or "WhatsApp Call Completed" for a WhatsApp call), shown to Paul in the same reply as the Planner page and the PDF (one reply, one question, so he approves all three together) and sent through Zapier only after his yes.
4. The checks: both reads, the source trace, the mandatory questions, and the final `verify.py` printout, pasted unedited into the reply.

After ANY correction, repeat the build and every hand-over for each output that changed, then run `verify.py` again.

## Where this skill sits in the client journey

1. **First meeting (Fact Find):** `ff-population-transcript` builds the Fact Find Transcript PDF, then `fact-find-summary` builds the Fact Find Summary PDF.
2. **Every follow-up meeting (one or many):** this skill. It produces the Follow-Up Appointment Summary Notes PDF and the Planner/AdviceTech short note, checks the applications against what was said, and has them corrected.
3. Because follow-ups build on each other, **this skill must never summarise a meeting in isolation** - Step 2 (context pack) is mandatory every time.

**Output 1 now applies to every meeting, first appointment included.** `ff-population-transcript`'s Step 7b calls through to this skill's Output 1 section directly for the Fact Find/first-appointment Planner note - there is no separate bespoke layout for it any more. Two things differ for a first/Fact Find meeting, nothing else: (a) the **pointer line** names the **Fact Find Summary PDF** rather than a Follow-Up Appointment Summary Notes file, since the latter doesn't exist yet at this stage; (b) the **Applications** section is typically omitted (no applications stage has normally happened yet). **Output 2 (the Follow-Up Appointment Summary Notes PDF) is still never produced for a first/Fact Find meeting** - the Fact Find Transcript and Fact Find Summary PDFs remain that meeting's documents, and this skill's Step 2 context-building, Step 2b (applications) and Step 6 (application corrections) are skipped when there is nothing yet for them to act on. Everything else in this skill (Steps 1-5, Accuracy, Output 1's design) governs the Fact Find meeting's Planner note exactly as it governs a follow-up's - **including the Two-Read Lock in Step 1b.**

**Deliverables for a follow-up meeting:** Output 1 (Planner note, shown as a copy-ready page), Output 2 (PDF, saved to the client's folder and sent in chat) and the Teams message to Sitamah. For a first/Fact Find meeting, only Output 1 comes from this skill (Output 2 is the Fact Find Summary, produced by `fact-find-summary` instead). Never save copies of Output 1 anywhere else. The only other thing this skill causes to be written is the correction of the client's application PDFs, which is done by `complete-applications-skill` in place in the client's own `Applications` folders (Step 6) - never by this skill itself, and never at a first meeting.
