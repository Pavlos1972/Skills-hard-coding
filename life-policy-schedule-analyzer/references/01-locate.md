# Step 1: Find and register the documents

**Where they are.** In the client's own folders, found by the client's name. Check BOTH places under `liferisk.co.za`: `Company - Paul` (New Business, but not limited to it) and `Company - WR Clients` > `Paul Kafentzis (Client Files)` (current clients). A given client's material could sit under either.
- **The schedules and quotes to analyse:** the client's `6. Policy Schedules` subfolder. If a client's folder uses different numbering or the document is filed elsewhere, use what is actually there and note which subfolder it was found in (it goes in the report: `found_in`).
- **The proposed quote** (for Report 2): the client's `Comparative Quotes` subfolder (it can sit one level deeper), and **always look for the proposed insurer's own payback document in the same folder**, for the same quote number: for BrightRock the "BR CMPO" (Change Moment Pay-Out guide) filed beside the Cover Proposal. If none is found, say so plainly and ask Paul for it (or whether the quote has no payback); never leave the payback out silently.
- **The Fact Find Summary** (`Fact Find Summary - DD.MM.YY - (First Surname).pdf`, saved in `2. Fact Find`) or a completed WR Fact Find: income, dependants and their ages, existing debt, other risk cover held. It turns "cover looks low" from a guess into a finding. If none is found, say so plainly in the Sources and carry on; do not stop or ask Paul to produce one.
- The client's **meeting notes** (also in `2. Fact Find`) if you need to show that a category was left out on purpose.
- If the request already names the proposed quote, treat the question as answered and say which quote is used. If no proposed quote can be found, ask Paul, and only then: he points to it, attaches it, or says **"No proposed covers for now"** (then only the analysis and Report 1 are built; do not ask again in that request).
- If more than one schedule or quote is found, confirm with Paul which he wants analysed, or, if asked generically, analyse every current in-force schedule found and say plainly which were included or skipped.

**Access.** Computer first, then the Microsoft 365 connector, then Zapier. Log every try, failures too (`run.py access`). Ask Paul to attach a file only after all three failed.

**Registering.** `--role schedule` (in force) or `--role quote` (a quote being analysed), one per policy, labelled with its own name; `--role proposed` (one), `--role payback_doc` (one), `--role fact_find_summary`, `--role intake_notes --label "<date>"`.

**insurers.json:** `[{"label": "Samplelife Life Plan", "insurer": "Samplelife"}, ...]` for every schedule, quote and the proposed quote. The name must be in the document's text.

**Before treating a document as complete, check you have every page.** A scanned schedule can appear as just its cover page, with the benefit table, the premium detail and the terms missing. A document that looks suspiciously short needs a direct check: `file <name>` and `unzip -l <name>`. A file that reports as a Zip archive despite a `.pdf` extension is a bundle of page images: extract and view every page. Never build the analysis from a document that lacks the benefit table or the premium detail. If something genuinely is not in the document after checking, say so; do not guess.

**If the text cannot be read.** A page with no text must be viewed as an image: render it at high resolution, crop and enlarge just the garbled table (a 3 to 5 times enlargement of a tightly cropped table usually turns garbled OCR into clean digits), check it against a second read. A figure read from an image is entered with `image_read` and the page; the program cannot prove it, shows it to Paul and lists it as only attested. "Illegible" is a starting point, not an end point.
