# Build, verify, save, and iterate

## Step 5: Build, verify, and write the source report

The PDF is drawn by `scripts/build.py` from `content.json` alone. **When populating any field that is itself a total, compute it from the same named component values used elsewhere in the document** (the program does this and the checker recomputes it).

**The deliverable is a PDF only.** No Word file is made.

After generating:
1. Render to PDF and rasterize every page to visually confirm: no orphaned headings, no split table rows, notes are bulleted, every field cell is point-form, no stale prior-year figures presented as current, no leftover page-number labels, and no two independent actions wrongly worded as conditional on each other.
2. Once the render checks out, that same PDF **is** the deliverable. The program names it `Fact Find Transcript - DD.MM.YY - (Name Surname).pdf`; present it via `present_files` / `SendUserFile` (copy it to `/mnt/user-data/outputs/` first when that folder exists).
3. **Source report (in the hand-over message).** In the reply that presents the PDF, state in a short list: (a) which sources were found and used (Audio to Text file, transcript, Overview, any other document; and the Manual Fact Find only if it was used as the last resort); (b) every Audio to Text field that was populated with status `preset` (or `heard` or `verify` in an older file), with what was done with it (kept, filled in from the transcript, flagged) - `confirmed` fields can be counted rather than listed; (c) every difference found between the Audio to Text file and the transcript, Overview or documents, quoting both values; (d) anything left "Not discussed" or "Requested" and why.

## Step 5a: ABSOLUTE MUST — save every deliverable directly into the client's own folder

**This step is not optional, is never skipped, and is never something Paul should have to ask for or remind Claude about.** Presenting a deliverable only in chat is **not** considered complete — the file must also land in the client's actual folder, every single time, per the Client File Access order above.

- **Why this exists:** on 14 September 2026 ([client E]), both PDFs were built, verified, and presented in chat — and then simply left there. Paul had to explicitly ask why they hadn't been saved. This must never happen again.
- **How to save it:** copy the finished PDF into the client's `2. Fact Find` folder ON THE COMPUTER (`cp -n`, in the mounted OneDrive folder; OneDrive uploads it by itself), without asking Paul for anything. Never upload it through Microsoft 365: a PDF has to travel as base64 inside one call, which is impractical above a few tens of KB. If the computer was not connected the run stopped at the start.
- **Verify every save by reading the folder back.** After every save (and every overwrite), list the folder and confirm the file's size AND modified time are the new file's: the listed size must equal the size of the local file you sent. A write call that reports success is not proof: if the old PDF is open on Paul's computer the write can be refused or the old copy can remain, and the staging copy can lag (the folder then shows a new time but the old size). If the size does not match, wait briefly and commit the file again, then list again. If the file is locked/open, tell Paul plainly, ask him to close it, and retry - never report it as saved until the listing proves it. **Named precedent:** [client B], 09.10.26 - an overwrite of the Fact Find Transcript PDF was reported saved, but the folder still held the old 10-page version. 15.10.26 - a Summary overwrite showed a new time but the previous size; a second commit fixed it.
- **Correcting a source document already on file:** copy it from the computer, edit narrowly, copy it back to the exact same path. Never edit or overwrite the Fact Find (Audio to Text) PDF or JSON, or the Manual Fact Find - they are Paul's own records and are read-only for this skill.
- **This applies to the Fact Find Summary PDF (Step 7a) too.** The Planner note (Step 7b) has no durable file form — this rule doesn't apply to it.
- **Confirm the save, don't just attempt it.**

## Step 6: Iterate with the advisor

Treat the first pass as a draft for review. Common corrections seen so far: contact details, template defaults, fields resolvable from other documents on file or from the Audio to Text file, a policy number resolved from the actual schedule, an FNA/Shortfall/Reduced quote with the wrong insurer or wrongly labelled Servicing instead of New Business, a wrong ABI (see the standing ABIs in Step 3), a Summary Section 8 heading that still says "Action Plan", two independent actions wrongly worded as conditional on each other, cluttered multi-fact paragraphs broken into point form, stale prior-year figures, DOB/ID corrections, and an Audio to Text value replaced by the transcript's without a flag.

Do not make the hand-overs final until the advisor confirms the Fact Find itself is correct: the program-driven job shows the PDF, the Summary hand-over, the Planner note page and the message to Sitamah in the same reply with ONE question, nothing is sent without his yes, and any correction re-opens the whole task.
