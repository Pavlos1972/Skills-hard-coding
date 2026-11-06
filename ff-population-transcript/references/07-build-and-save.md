# Build, look, save, show Paul

## Formatting conventions (the program draws exactly this; these came from direct advisor feedback)

- **Font:** Aptos, 12pt, throughout the entire document.
- **Every field value is point-form** (the rule is on the combine page, written once): one fact per line, in field table cells, Notes and flags.
- **Prior-year information is shown only if it's genuinely still true today — never carried forward by default.** Where genuinely unclear, split into two explicit lines: `[year]: [old value]` then `[year]: [current value/status]`. **Named precedent:** [client A], 07.10.26.
- **No page-number or "Page N" labels anywhere in the document.**
- **No forced page breaks between sections.** A heading is kept with the first rows of its table, and a table row is never split across pages.
- **Two-column field tables:** left column = field label (bold, light-blue shading `EAF1F8`), right column = value, bulleted per the point-form rule. Section headings in navy (`1F3A5F`), sub-headings smaller navy bold. Repeating items (debts, children, policies) are shown as one table per item, or as a table with the Audio to Text file's own columns.
- **Client ID / Passport Number and other identifiers:** transcribe exactly as given, digit for digit, once confirmed.

The font is Aptos when it is installed where the skill runs; otherwise the program uses a named substitute and prints which one. Say so in your reply and never say Aptos when it was not used.

## Looking at the pages
Open every page image and confirm: no orphaned headings, no split table rows, notes are bulleted, every field cell is point-form, no stale prior-year figures presented as current, no leftover page-number labels, and no two independent actions wrongly worded as conditional on each other.

## The source report (in the reply that presents the PDF; `run.py report` prints it)
(a) which sources were found and used (the form's data file and PDF, the transcript, the Overview, any other document; the Manual Fact Find only if it was used as the last resort); (b) the form's fields by status, with every `preset` (or `heard` or `verify`) value and what was done with it (kept, filled in from the transcript, flagged); (c) every contradiction found between the form and the transcript, Overview or documents, SORTED or HIGHLIGHTED, quoting both values; (d) anything left "Not discussed" or "Requested" and why. Add the glance list the program prints.

## save into the client's own folder (ABSOLUTE MUST)
**This step is not optional, is never skipped, and is never something Paul should have to ask for.** Presenting the PDF only in chat is not complete: the file must also land in the client's actual folder, every single time, per the Client File Access order (page 01).

- **Why this exists:** on 14 September 2026 ([client E]), both PDFs were built, verified, and presented in chat - and then simply left there. Paul had to explicitly ask why they hadn't been saved. This must never happen again.
- **How to save it:** write the finished PDF straight into the client's `2. Fact Find` folder using the device-bridge file tools. Request folder access proactively if not already granted. `run.py build` copies the PDF to `/mnt/user-data/outputs/` (when that folder exists) and prints the exact `stagedPath` to give `device_commit_files`: the computer save fails without a staged path under that folder. Present it in the chat too (`present_files` / `SendUserFile`).
- **Verify every save by reading the folder back.** After every save (and every overwrite), list the folder and confirm the file's size AND modified time are the new file's: the listed size must equal the size of the local file you sent (`run.py saved` compares them). A write call that reports success is not proof: if the old PDF is open on Paul's computer the write can be refused or the old copy can remain, and the staging copy can lag. If the size does not match, wait briefly and commit the file again, then list again. If the file is locked/open, tell Paul plainly, ask him to close it, and retry - never report it as saved until the listing proves it. **Named precedent:** [client B], 09.10.26 - an overwrite of the Fact Find Transcript PDF was reported saved, but the folder still held the old 10-page version.
- **The form's files are read-only:** never edit or overwrite the Fact Find (Audio to Text) PDF or JSON, or the Manual Fact Find - they are Paul's own records.

## The one stop: Paul reads the Fact Find
Treat the first pass as a draft for review. Common corrections seen so far: contact details, template defaults, fields resolvable from other documents on file, a policy number resolved from the actual schedule, an FNA/Shortfall/Reduced quote with the wrong insurer or wrongly labelled Servicing instead of New Business, a wrong ABI, two independent actions wrongly worded as conditional on each other, cluttered multi-fact paragraphs broken into point form, stale prior-year figures, DOB/ID corrections, and a form value replaced by the transcript's without a flag. Show Paul the PDF and the source report in ONE reply and WAIT for his OK. A correction re-opens the whole task: change `overlay.json`, combine, build, look, save and show again.
