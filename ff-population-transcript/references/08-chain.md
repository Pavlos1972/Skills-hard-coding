# Hand-overs: the Summary, the Planner note and the message to Sitamah

## Chain into the two downstream skills — every completed Fact Find produces three outputs

Once the Fact Find Transcript (the PDF from step 6) is finalized and approved, continue automatically and produce the other two deliverables from the same meeting:

**The Fact Find Summary (via the `fact-find-summary` skill)**
- `fact-find-summary` reads a Fact Find as a **PDF**. Step 6 already produced and verified that PDF — reuse it rather than converting the docx a second time. Follow that skill's own SKILL.md exactly, including its transcript-accuracy re-check, totals-reconciliation rule and its fixed Section 8 sub-headings (Life Cover - Fractured Cover, Disability Cover - Fractured Cover, Dread Disease Cover, Income Protection / Sickness Benefit Cover: the words "Action Plan" are not used in the Summary). The contact details, Referral From value, and the point-form / prior-year / insurer-and-New-Business-vs-Servicing / standing-ABI / parallel-actions rules above all apply to the Summary too. **Note (28/10/2026):** the Fact Find Transcript now follows the v3.0 layout; if `fact-find-summary` still refers to v2.0 page numbers, follow its content rules and tell Paul in one line that that skill needs aligning.
- Save per that skill's own filename convention, present it via `present_files` / `SendUserFile`, **and save it directly into the client's own folder per the save rule (page 07)**.

**The Planner / AdviceTech note and the message to Sitamah (made once, by `client-teams-transcript-skill`'s program)**
- Do not write the Planner note or the message to Sitamah by hand in this skill. Open `client-teams-transcript-skill` and run its step driver for this meeting with `--type first` (a WhatsApp call: `--type whatsapp`). The program reads the transcript, builds the short Planner note page (one-line bullets per planning area, only the actions for now, in order), checks it, and builds the message to Sitamah. The fixed layouts this skill used to describe here are retired: the program's output is the only note.
- Facts that the Fact Find settled (and the transcript did not) are taken from the approved Fact Find, so the note matches it. The pointer line in the note names the Fact Find Summary PDF just produced above.
- Setting up the follow-up appointment IS an action for Sitamah at every meeting (she books it, or sends the Teams meeting request): "Sitamah to set up the follow-up appointment". Any FNA / Shortfall / Reduced quote line names the insurer and says New Business or Servicing (the mapping rules), and two independent actions are separate, unconditional lines (the mapping rules).
- For two spouses (the two-spouses page) the program is run once per spouse.

**Delivering all three:** present the Fact Find Transcript **PDF** and the Fact Find Summary PDF together via `present_files` / `SendUserFile`, **confirm both have also been saved directly into the client's own folder per the save rule (page 07) (never chat-only; verified by listing the folder back)**, then present the Planner note as its copy-ready page, with one short sentence in the reply saying what the page is, and show the message to Sitamah that was posted (below). All three outputs come from one trigger — the advisor shouldn't have to ask for the summary, the Planner note, or the folder save separately once the Fact Find itself is approved.

## The message to Sitamah (made once, by the Teams transcript program)

The message is made and sent only by `client-teams-transcript-skill`: its program builds it, and its page `references/07-teams-message.md` holds the wording (with `(Review Client)` or `(Prospect)` after the name), the 1st / 2nd / 3rd count, the follow-up sentence check and the Zapier-only route (the Microsoft 365 connector cannot send Teams messages: 403). This skill does not word, show or send a second message.

- It is POSTED AUTOMATICALLY through Zapier (Paul's rule: no question, no waiting for a yes), in the final step, once the PDFs are saved and the folder listing has been checked; the reply shows the message that was posted.
- It is posted once per meeting, and never again for a correction unless Paul asks. For two spouses in one meeting there is one message per spouse, each posted automatically. The Teams skill's own wording "only with Paul's yes" is satisfied in this chain by Paul's standing instruction (when that skill is run on its own, it still asks).

