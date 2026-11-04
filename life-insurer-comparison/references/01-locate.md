# Step 1: Find and register the documents

**Where they are.** Look in the client's own folders, matched by the client's name.
- **The quotes** are in the risk transaction's `Comparative Quotes` folder. It is not always flat: the first folder with that name can hold unrelated documents (investment paperwork) while the life-insurance quotes sit one level deeper in a nested subfolder, sometimes with a near-identical name. If the first folder does not hold quotes matching the insurers, check one level deeper before concluding nothing is there. Take the most recent version unless told otherwise.
- **In-force policy schedules**: the client's folder and any dedicated `Policy Schedules` subfolder.
- **The client's own notes** (they decide the scope): the Follow-Up Appointment Summary Notes (EVERY dated version), the Fact Find Summary and the WR Overview, from the client's `2. Fact Find` folder first, then the main folder.
- A folder of earlier analyses (for example `Analysis & Comparison Reports`) is background only, never a primary source of figures.
- Folder layouts vary (a "New Business" area with a flat first-name-then-surname list, an alphabetised existing-client structure; a named subfolder nested inside the client's folder). If the first, most obvious place has nothing, broaden the search across Paul's known adviser folders and check the nesting; do not stop at the first miss.

**Access.** Computer first, then the Microsoft 365 connector, then Zapier. Log every try, failures too (`run.py access`). Ask Paul only after all three failed, saying plainly what was searched and what was not found.

**Registering.** One `--role quote` (a new proposal) or `--role schedule` (an in-force schedule) per policy or proposal, labelled with its own name; the schedule side is not always the client's original insurer, so name each side. At most 6. Then the notes (`--role intake_notes --label "<date>"`), `fact_find_summary`, `overview`. A background document from one insurer's broker consultant comparing both products is `--role broker_doc`: background only, never a figures source; any general product claim in it is checked against the insurer's own document and, if it cannot be verified, attributed in the letter as broker-sourced and adviser-confirmed, not independently verified.

**insurers.json** (the insurer behind each quote or schedule):
`[{"label": "Samplelife Quote", "insurer": "Samplelife"}, ...]` The name must be in the document's text.

**Before treating a document as complete, check you have every page.** A multi-page scanned schedule can appear as its first one or two pages, with the benefit table, the premium projections and the exclusions missing. A document that looks suspiciously short for what it should be (a cover letter and one summary page for a 15 to 20 page schedule) needs a direct check: `file <name>` and `unzip -l <name>`. A file that reports as a Zip archive despite a `.pdf` extension is a bundle of page images (`1.jpeg`, `2.jpeg` ...): extract and view every page. Never build a comparison from a schedule that lacks the benefit table. If a document genuinely lacks a figure, say so and ask for it.

**If the text cannot be read.** A page with no text must be viewed as an image: render it at high resolution, crop and enlarge the garbled table (a 3 to 5 times enlargement of a tightly cropped table usually turns garbled OCR into clean digits, then check it against a second pass), or open the document's own web address with Claude in Chrome and read it page by page (some pages render sideways or upside down independently of the others: use the viewer's rotate control and page-number jump). A figure read from an image is entered with `image_read` and the page; the program cannot prove it, shows it to Paul and lists it as only attested. "Illegible" is a starting point, not an end point.

**RAR only.** If only a RAR or replacement document is found for a side that should have a policy schedule, do not proceed on it by default: tell Paul and ask whether he wants the schedule requested. If he proceeds, mark that side `rar_only: true`; the letter and the email say so.

**Conflicts.** The WR Overview is Paul's own hand-made summary and can go stale or carry a typo. When it disagrees with the insurer's own quote or schedule on a figure, the insurer's document wins, and the conflict is named to Paul (which document said what, which figure the letter uses and why) so he can correct the Overview; never silently preferred, never silently dropped.
