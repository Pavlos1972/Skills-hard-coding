# What changed in the Fact Find Summary skill, in plain words

For Paul. **Not uploaded, not live.** This is the program-driven version of `fact-find-summary` (Operation Skill Restructure, 03/11/2026). The old version stays in the skill's version history in claude.ai (that is the backup).

## What the skill does now
After the Fact Find Transcript PDF exists, a program reads that PDF, builds the nine fixed Summary sections from it, recomputes the totals to the cent and draws the **Fact Find Summary PDF** (A4). A checker then prints a **short audit**: one line per check with a green tick or a red cross, and one closing line for what is only attested. The program cannot skip a step, and it stops when the PDF is not the program-drawn Fact Find Transcript.

## What a program now does that Claude did by hand
- Reads the Fact Find PDF by its fixed layout (and stops with one line for you if it is another kind of PDF, for another client or for another meeting date).
- Builds all nine sections by a fixed mapping, row by row. Every Summary value points to the Fact Find row it came from, and the checker compares the two.
- Recomputes the debt totals and the childcare total from the items. Section 8's childcare and debt repayments must equal Sections 5 and 4 (debt is never left out because of credit life), and the total needed must add up.
- Checks the standing ABIs: Life Cover (WOL) 3%, Childcare 5%, Household needs 5% under Disability with no Life Cover (WOL) line there, Dread Disease 3%.
- Carries every flag of the Fact Find into Items Requiring Follow-Up and names the owner: Cameron (short-term), CL (Will), Valerie (medical aid and gap cover), Lizelle (gross income and ACI). Lizelle replaces Martin (your answer, 03/11/2026).
- Draws the PDF, derives the file name (`Fact Find Summary - DD.MM.YY - (First Surname).pdf`) and checks that the PDF can be rebuilt identically from its data.
- Writes the short audit (you asked for this on 03/11/2026).

## What left this skill (your yes answers, 03/11/2026)
- The Planner note and the Sitamah Teams message: `client-teams-transcript-skill` makes them once. This ends the double message for a first appointment.
- Re-checking the whole Fact Find against the recording: the Fact Find Transcript skill's checker does that. This skill proves the Summary equals the Fact Find.
- Reading old v2.0 Fact Finds and the "PDF that is really a zip of images" case.
- The 8:45am laptop note and the "propose skills" rule.
- The example script. It held a real person's details; it is not carried over. (Your claude.ai version history still holds the old version.)

## What stayed the same
The nine sections and their order, the Section 8 sub-headings, the look (navy, light blue, red flags), the file name pattern, the "always include" list (ID or passport, cell, work number, both emails, referral from), the ABIs (Dread Disease now 3%), the rule that debt is never left out, the quote rule (insurer and New Business or Servicing), and the three short true stories (kept in `references/05-why.md`, names removed).

A program (`tools/inventory.py`) went through all 392 rules of the old text: **13 are still there word for word, 93 are reworded (each with a written reason), 286 were dropped on purpose (each with a written reason), and none was lost without a record.** The records are in `history/changes.json` and `history/decisions.json`; the full list is `history/INVENTORY-REPORT.md`.

## Your yes/no list (anything I was not sure about)
1. **The "toggle against notes" rule.** The old text said: if a field says "No" but its Notes name a condition, show what the Notes say and flag the difference. This skill now copies the Fact Find's rows and flags as they are. **Is that OK? Yes / No.** (If no, I add a check.)
2. **Section 8 shows every row,** including "Not discussed" ones, because they show what is still pending. Other sections leave out "Not discussed" and "N/A" rows (the audit counts them). **Keep it like that? Yes / No.**
3. **Length.** The Summary for the invented client is 8 pages (the Fact Find itself is 10). Most of it is Section 8 and the existing-cover lists. **Is that acceptable? Yes / No.**
4. **The follow-up list is made by fixed rules** (flags, pending ACI, no will, no medical aid, no gap cover, no short-term insurance, no retirement funding, incomplete business details, documents to request, next steps). Anything else you want in it? **Yes (list) / No.**
5. **Font.** The PDF uses Helvetica (a standard font, as the old Summary did), not Aptos. **OK? Yes / No.**

## What I could not do or check
- **No real Fact Find Transcript PDF was used.** The test uses an invented one drawn by the Fact Find skill's own program. The real first run is the real test. If the Fact Find skill's layout changes later, this skill's reader needs the same change.
- **I could not run it inside your chat.** The access routes (computer, Microsoft 365, Zapier), the folder save and listing, and sending the PDF are only attested in the audit, not proven.
- **The reader needs the `pdfplumber` program** in the chat's environment. The self-test at the start says so if it is missing, and the job stops.
- Only one test was run, as agreed: one end-to-end run on invented data, which also proves that a hand-edited Summary is caught.

## Strict changes of 05/11/2026 (Paul, after the first real run of the Fact Find chain)
- **The PDF is found automatically.** In the Fact Find chain the PDF that `ff-population-transcript` has just made is used directly (route `passed`). Otherwise Microsoft 365 is the working route: the chat reads the PDF through the connector, saves it, and the program refuses a copy whose size differs from the connector's. The computer is used only if the chat is already connected to it; it is never requested and is logged at once as "not connected, not requested". Zapier is next.
- **Nothing is asked of Paul:** no permission, no Allow, no attaching, uploading or dragging a file. If every route fails, the chat says in at most five lines what failed and stops.
- **A quiet run:** the version sentence, then work, with one short progress line per step; no opening recap; the chat does not read the pages itself. The reply is the PDF and the short audit (this skill already ended in the short audit).
- **Saving:** the Summary PDF goes into the client's `2. Fact Find` folder through Microsoft 365 (SharePoint upload), then the folder is listed and the size compared.
- **Not changed:** this skill still sends nothing; the Sitamah message is made and posted by `client-teams-transcript-skill`.
