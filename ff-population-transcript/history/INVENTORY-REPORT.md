INVENTORY of the old skill: 568 sentences
  kept (word for word or nearly): 254
  reworded, with a recorded change: 87
  dropped, with a recorded decision: 227
  UNACCOUNTED: 0


REWORDED (each is covered by a recorded change):
- old line 61: Reads the client's Fact Find (Audio to Text) file (first and primary source), the Teams meeting transcript(s) (second, equally important source) and the client's latest Overview (reference), and build
    now: Write only what is in the source material (the Fact Find (Audio to Text) file, the transcript, the Overview, a client document or file) or in a named document this skill tells you to use.
    why: The introduction is shortened into the entry page (SKILL.md).
- old line 61: Built in Word for layout control, delivered as a PDF — see Step 5.
    now: print("  if one belongs in a row (for example a Risk Calculation line) add it as an overlay fill with the source {\"doc\":
    why: The introduction is shortened into the entry page (SKILL.md).
- old line 61: Every deliverable this skill produces is saved directly into the client's own folder — see Step 5a.
    now: Save per that skill's own filename convention, present it via present_files / SendUserFile, and save it directly into the client's own folder per the save rule (page 07).
    why: The introduction is shortened into the entry page (SKILL.md).
- old line 61: This is not optional and Paul should never have to ask for it.
    now: *This step is not optional, is never skipped, and is never something Paul should have to ask for.
    why: The introduction is shortened into the entry page (SKILL.md).
- old line 63: ## Client File Access (standing rule — applies to every step below that reads or saves a client file)
    now: every step that reads or saves a client file)
    why: Paul, 02/11/2026: the 8:45am laptop window is dropped; the access order (computer, then Microsoft 365, then Zapier, then say plainly what was tried) is kept, as are the two locations and the rule never to touch another broker's folder. Asking Paul to attach a file is replaced by saying plainly what was tried (Paul, 05/11/2026).
- old line 67: Paul's laptop is reachable ~8:45am on weekdays only;
    now: "the saved size equals the built PDF and Paul's OK is recorded",
    why: Paul, 02/11/2026: the 8:45am laptop window is dropped; the access order (computer, then Microsoft 365, then Zapier, then say plainly what was tried) is kept, as are the two locations and the rule never to touch another broker's folder. Asking Paul to attach a file is replaced by saying plainly what was tried (Paul, 05/11/2026).
- old line 67: if the bridge is down outside that window, say so plainly rather than treating it as a failure.
    now: If the file is locked/open, tell Paul plainly, ask him to close it, and retry - never report it as saved until the listing proves it.
    why: Paul, 02/11/2026: the 8:45am laptop window is dropped; the access order (computer, then Microsoft 365, then Zapier, then say plainly what was tried) is kept, as are the two locations and the rule never to touch another broker's folder. Asking Paul to attach a file is replaced by saying plainly what was tried (Paul, 05/11/2026).
- old line 68: SharePoint — only if the local machine genuinely can't be reached.
    now: SharePoint (the Microsoft 365 connector) - only if the local machine genuinely can't be reached.
    why: Paul, 02/11/2026: the 8:45am laptop window is dropped; the access order (computer, then Microsoft 365, then Zapier, then say plainly what was tried) is kept, as are the two locations and the rule never to touch another broker's folder. Asking Paul to attach a file is replaced by saying plainly what was tried (Paul, 05/11/2026).
- old line 68: This should be rare — treat a failed local connection as the exception, not the default path.
    now: List the whole folder, treat every file that could plausibly be the thing you need (similar name, dated the meeting date, same client) as a candidate, and OPEN each one before deciding.
    why: Paul, 02/11/2026: the 8:45am laptop window is dropped; the access order (computer, then Microsoft 365, then Zapier, then say plainly what was tried) is kept, as are the two locations and the rule never to touch another broker's folder. Asking Paul to attach a file is replaced by saying plainly what was tried (Paul, 05/11/2026).
- old line 68: Be aware this path requires embedding the file's content as base64 text in one message when saving, which has a real practical ceiling — a large PDF may need lossless compression first (e.g.
    now: Saving through it needs the file's content as base64 text in one message, which has a real practical ceiling:
    why: Paul, 02/11/2026: the 8:45am laptop window is dropped; the access order (computer, then Microsoft 365, then Zapier, then say plainly what was tried) is kept, as are the two locations and the rule never to touch another broker's folder. Asking Paul to attach a file is replaced by saying plainly what was tried (Paul, 05/11/2026).
- old line 68: qpdf --recompress-flate --object-streams=generate followed by gs -dPDFSETTINGS=/ebook).
    now: a large PDF may need lossless compression first (for example qpdf --recompress-flate --object-streams=generate followed by gs -dPDFSETTINGS=/ebook).
    why: Paul, 02/11/2026: the 8:45am laptop window is dropped; the access order (computer, then Microsoft 365, then Zapier, then say plainly what was tried) is kept, as are the two locations and the rule never to touch another broker's folder. Asking Paul to attach a file is replaced by saying plainly what was tried (Paul, 05/11/2026).
- old line 69: Ask Paul to attach the file — last resort only.
    now: Never ask Paul to attach a file.
    why: Paul, 02/11/2026: the 8:45am laptop window is dropped; the access order (computer, then Microsoft 365, then Zapier, then say plainly what was tried) is kept, as are the two locations and the rule never to touch another broker's folder. Asking Paul to attach a file is replaced by saying plainly what was tried (Paul, 05/11/2026).
- old line 69: Only once both the local machine and SharePoint have genuinely been tried and neither works does this skill ask Paul to upload the Audio to Text file, transcript or other source directly, or say plain
    now: Only once all of these have genuinely been tried and none works, say in at most five lines what was tried and what failed.
    why: Paul, 02/11/2026: the 8:45am laptop window is dropped; the access order (computer, then Microsoft 365, then Zapier, then say plainly what was tried) is kept, as are the two locations and the rule never to touch another broker's folder. Asking Paul to attach a file is replaced by saying plainly what was tried (Paul, 05/11/2026).
- old line 72: This applies to locating the Audio to Text file, transcript and Overview (Steps 1 and 1b below), to checking the client's other documents for a field that can't otherwise be resolved (Step 3 below), a
    now: When a field can't be resolved from the Audio to Text file, the transcript or the Overview, check the client's other documents on file before marking it unconfirmed.
    why: Paul, 02/11/2026: the 8:45am laptop window is dropped; the access order (computer, then Microsoft 365, then Zapier, then say plainly what was tried) is kept, as are the two locations and the rule never to touch another broker's folder. Asking Paul to attach a file is replaced by saying plainly what was tried (Paul, 05/11/2026).
- old line 76: That skill has its own rule for this exact case:
    now: Open client-teams-transcript-skill and run its step driver for this meeting with --type first (a WhatsApp call:
    why: Paul, 02/11/2026: the 8:45am laptop window is dropped; the access order (computer, then Microsoft 365, then Zapier, then say plainly what was tried) is kept, as are the two locations and the rule never to touch another broker's folder. Asking Paul to attach a file is replaced by saying plainly what was tried (Paul, 05/11/2026).
- old line 76: it still produces the summary PDF, but the Planner note (now always produced via client-teams-transcript-skill's Output 1 structure and presented as its copy-ready Artifact page, per Step 7b below) ca
    now: If the form's files and the transcript are both missing after checking the client's folder, say so (step 1's --missing) - unless a completed FF already exists with no transcript (see Out of scope).
    why: Paul, 02/11/2026: the 8:45am laptop window is dropped; the access order (computer, then Microsoft 365, then Zapier, then say plainly what was tried) is kept, as are the two locations and the rule never to touch another broker's folder. Asking Paul to attach a file is replaced by saying plainly what was tried (Paul, 05/11/2026).
- old line 78: Gather inputs (source order — rule 11)
    now: How the sources combine (rule 11):
    why: Reworded: step names now follow the program's eight steps; the rule is kept (references/01 and 02).
- old line 80: Gather in this order, per the Client File Access order above:
    now: Fact Find folder (both locations per the Client File Access order).
    why: Reworded: step names now follow the program's eight steps; the rule is kept (references/01 and 02).
- old line 82: The Fact Find (Audio to Text) file — see Step 1b.
    now: The Manual Fact Find — last resort, only if the Audio to Text file is absent.
    why: Reworded: step names now follow the program's eight steps; the rule is kept (references/01 and 02).
- old line 82: This is the first and primary source.
    now: The Audio to Text file — first and primary source.
    why: Reworded: step names now follow the program's eight steps; the rule is kept (references/01 and 02).
- old line 83: The file is named Teams meeting transcript - DD.MM.YY - (Client Name)_ Annual Review [year] (or ...
    now: Teams meeting transcript - DD.MM.YY - (Client Name)_ Annual Review [year] (or ...
    why: Reworded: step names now follow the program's eight steps; the rule is kept (references/01 and 02).
- old line 83: - FF, or with another suffix) — search the client's 2.
    now: Search the client's 2.
    why: Reworded: step names now follow the program's eight steps; the rule is kept (references/01 and 02).
- old line 84: Overview folder (see Step 1b).
    now: Overview folder, if there is one, as a point of reference.
    why: Reworded: step names now follow the program's eight steps; the rule is kept (references/01 and 02).
- old line 85: The Manual Fact Find — only if the Audio to Text file is absent (see Step 1b).
    now: The Manual Fact Find — last resort, only if the Audio to Text file is absent.
    why: Reworded: step names now follow the program's eight steps; the rule is kept (references/01 and 02).
- old line 87: If the Audio to Text file and the transcript are both missing after checking the client's folder, ask for them — unless a completed FF already exists with no transcript (see Out of scope).
    now: If the form's files and the transcript are both missing after checking the client's folder, say so (step 1's --missing) - unless a completed FF already exists with no transcript (see Out of scope).
    why: Reworded: step names now follow the program's eight steps; the rule is kept (references/01 and 02).
- old line 89: Read all of them and treat them as one continuous meeting.
    now: Give all of them to run.py files (one --transcript each):
    why: Reworded: step names now follow the program's eight steps; the rule is kept (references/01 and 02).
- old line 94: The Audio to Text file — first and primary source (Paul's rule, 28/10/2026).
    now: The Audio to Text file — first and primary source.
    why: Reworded for the new form (Paul, 02/11/2026): the form's data file first, the schema check, the parking list ignored, the look-up text checked; the rule is kept (references/02).
- old line 95: It is normally Fact Find (Audio to Text) - DD.MM.YYYY - [Name Surname].pdf plus a .json with the same name, in the client's 2.
    now: Fact Find (Audio to Text) - DD.MM.YYYY - [Name Surname].json plus the same name as .pdf, in the client's 2.
    why: Reworded for the new form (Paul, 02/11/2026): the form's data file first, the schema check, the parking list ignored, the look-up text checked; the rule is kept (references/02).
- old line 95: List the whole folder, open the candidates, and use the one dated the meeting date for this client.
    now: Use the one dated the meeting date for this client.
    why: Reworded for the new form (Paul, 02/11/2026): the form's data file first, the schema check, the parking list ignored, the look-up text checked; the rule is kept (references/02).
- old line 96: Read both the PDF and the JSON.
    now: the PDF and the spreadsheet both count).
    why: Reworded for the new form (Paul, 02/11/2026): the form's data file first, the schema check, the parking list ignored, the look-up text checked; the rule is kept (references/02).
- old line 96: The PDF is the readable Fact Find (WR Fact Find v3.0).
    now: The PDF is the readable copy of the same Fact Find (WR Fact Find v3.0).
    why: Reworded for the new form (Paul, 02/11/2026): the form's data file first, the schema check, the parking list ignored, the look-up text checked; the rule is kept (references/02).
- old line 96: The JSON holds every field with a value v and a status st:
    now: every field sits under f as a value v with a status st (confirmed, preset or empty;
    why: Reworded for the new form (Paul, 02/11/2026): the form's data file first, the schema check, the parking list ignored, the look-up text checked; the rule is kept (references/02).
- old line 96: confirmed, heard, verify, preset or empty;
    now: STATUSES = ("confirmed", "preset", "empty", "heard", "verify")
    why: Reworded for the new form (Paul, 02/11/2026): the form's data file first, the schema check, the parking list ignored, the look-up text checked; the rule is kept (references/02).
- old line 96: repeating lists (risk policies, retirement funding, debts, children and so on) sit under l.
    now: files from the older form also use heard and verify), and the repeating lists (risk policies, retirement funding, debts, children and so on) sit under l as rows.
    why: Reworded for the new form (Paul, 02/11/2026): the form's data file first, the schema check, the parking list ignored, the look-up text checked; the rule is kept (references/02).
- old line 96: Extract both programmatically AND render the PDF pages and look at them.
    now: extract form-field values AND render the pages and look at them.
    why: Reworded for the new form (Paul, 02/11/2026): the form's data file first, the schema check, the parking list ignored, the look-up text checked; the rule is kept (references/02).
- old line 96: If the PDF and the JSON disagree on a field, flag it and quote both.
    now: If the PDF and the JSON disagree on a field, the program lists it.
    why: Reworded for the new form (Paul, 02/11/2026): the form's data file first, the schema check, the parking list ignored, the look-up text checked; the rule is kept (references/02).
- old line 97: confirmed, heard, verify and preset values are all populated values and all go into the Fact Find.
    now: confirmed and preset values (and heard and verify values in an older file) are all populated values and all go into the Fact Find.
    why: Reworded for the new form (Paul, 02/11/2026): the form's data file first, the schema check, the parking list ignored, the look-up text checked; the rule is kept (references/02).
- old line 100: The source report (Step 5) states what the Audio to Text file contributed, with every heard, verify and preset entry listed, as well as every difference found.
    now: The source report (page 07) states what the Audio to Text file contributed, with every preset entry (and every heard and verify entry in an older file) listed, as well as every difference found.
    why: Reworded for the new form (Paul, 02/11/2026): the form's data file first, the schema check, the parking list ignored, the look-up text checked; the rule is kept (references/02).
- old line 107: If, and only if, no Audio to Text file exists for this meeting (both locations checked, the whole folder listed, every candidate opened), look for the Manual Fact Find:
    now: If, and only if, no Audio to Text file exists for this meeting (both locations checked, the whole folder listed, every candidate opened) AND Paul says to use the Manual Fact Find , look for the Manual
    why: Reworded for the new form (Paul, 02/11/2026): the form's data file first, the schema check, the parking list ignored, the look-up text checked; the rule is kept (references/02).
- old line 112: Two spouses in one meeting (Paul's rule, 15/10/2026)
    now: # Two spouses in one meeting
    why: Reworded: step names and program mechanics updated; the rule is kept (references/03 and 04).
- old line 116: Two Fact Find Transcript PDFs, two Fact Find Summary PDFs, two Planner note Artifact pages (one per spouse) and two Teams messages (one per spouse, each only after Paul's yes).
    now: Two Fact Find Transcript PDFs, two Fact Find Summary PDFs, two Planner note pages (one per spouse) and two Teams messages (one per spouse, each posted automatically).
    why: Reworded: step names and program mechanics updated; the rule is kept (references/03 and 04).
- old line 131: Only write "Not discussed" after this search AND part C have both been done and nothing was found.
    now: Only leave a contact row "Not discussed" after this search AND part C have both been done and nothing was found.
    why: Reworded: step names and program mechanics updated; the rule is kept (references/03 and 04).
- old line 175: the WR Overview spreadsheet), correct it directly — see Step 5a.
    now: the WR Overview spreadsheet), correct it directly (the save rule is on page 07).
    why: Reworded: step names updated, dated attributions removed, Dread Disease ABI 3% (Paul, 02/11/2026, replacing 5%); the rule is kept (references/06).
- old line 177: There is no default (Paul, 15/10/2026:
    now: There is no default (Paul:
    why: Reworded: step names updated, dated attributions removed, Dread Disease ABI 3% (Paul, 02/11/2026, replacing 5%); the rule is kept (references/06).
- old line 179: Debt details are captured in full, every debt (Paul's rule, 07/10/2026).
    now: Debt details are captured in full, every debt.
    why: Reworded: step names updated, dated attributions removed, Dread Disease ABI 3% (Paul, 02/11/2026, replacing 5%); the rule is kept (references/06).
- old line 181: See Step 3a for the precedent behind this caution.
    now: """Read the form's data file for this run (writes form_read.json and a saved copy).
    why: Reworded: step names updated, dated attributions removed, Dread Disease ABI 3% (Paul, 02/11/2026, replacing 5%); the rule is kept (references/06).
- old line 190: Dread Disease ABI Value = 5%.
    now: Life Cover (WOL) ABI = 3% and Childcare ABI = 5%.
    why: Reworded: step names updated, dated attributions removed, Dread Disease ABI 3% (Paul, 02/11/2026, replacing 5%); the rule is kept (references/06).
- old line 214: *Named precedent — a caution against overcorrecting, not a caught fabrication:
    now: [client A], 07.10.26 (review) — Paul specified a BrightRock Servicing FNA against the existing policy ([policy no.
    why: Step 3a (the 13-point re-check) is replaced by the program's own checks and the audit; each rule it re-checked stays once, where it applies (references/06-mapping-rules.md, 02, 03, 04).
- old line 214: This step exists to catch genuinely missed, fabricated, or dangling content, not to relitigate a value that's simply unfamiliar or briefly unclear elsewhere in the recording.
    now: If no D&R email exists, use the Audio to Text file's Referral value (for example "Current client"), or the referrer named in the transcript, or Referral - referrer not stated (please confirm).
    why: Step 3a (the 13-point re-check) is replaced by the program's own checks and the audit; each rule it re-checked stays once, where it applies (references/06-mapping-rules.md, 02, 03, 04).
- old line 214: Only flag a specific, already-stated value when a source gives a concrete reason to doubt it.
    now: Don't manufacture ambiguity that isn't there — a specific, plausible value should only be flagged when a source itself contains a genuine contradiction or nonsense reading.
    why: Step 3a (the 13-point re-check) is replaced by the program's own checks and the audit; each rule it re-checked stays once, where it applies (references/06-mapping-rules.md, 02, 03, 04).
- old line 218: Formatting conventions (apply exactly — these came from direct advisor feedback)
    now: these came from direct advisor feedback)
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 224: Only keepNext on headings and cantSplit:
    now: The only overlap allowed is the common debts, the children and the joint policies.
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 224: true on every table row.
    now: 1 | Run it | The one command that starts the job and how every step works |
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 228: Build, verify, and write the source report
    now: Show Paul the PDF and the source report in ONE reply and WAIT for his OK.
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 230: Use scripts/build_fact_find.js as the starting template for the styling helpers (it already implements all Step 4 conventions, including a fieldTable cell renderer that accepts either a single string 
    now: if words_ and words_[-1].lower().strip(".,;:") in ("the", "a", "an", "and", "to", "of", "for", "with", "in", "on", "at", "by", "from", "is", "are", "was", "or", "that", "this") \
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 230: Replace its client-specific content with the sections of Step 2, in the Audio to Text file's order;
    now: The form's value stays in the report either way (the Audio to Text file wins);
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 230: don't rewrite the styling helpers or numbering config.
    now: Each one must end up in the document or be reviewed (a missed one is a missed fact)."""
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 230: When populating any field that is itself a total, compute it from the same named component values used elsewhere in the document.
    now: The Audio to Text file wins where they differ, and every contradiction is either SORTED (a rule settles it) or HIGHLIGHTED (both values and where each came from).
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 232: *The .docx built here is the internal working format only — it is never the delivered Fact Find Transcript.
    now: any other text from them in a row still is.) The form's data file and PDF, and the Manual Fact Find, are read-only for this skill.
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 232: The file saved to the client's folder is a PDF.
    now: The form saves its Fact Find (Audio to Text) PDF and data file into the client's folder.
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 235: Render to PDF and rasterize every page to visually confirm:
    now: Open every page image and confirm:
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 236: Once the render checks out, that same PDF is the deliverable.
    now: out.append("the form's Date completed (%s) is not in the PDF's text" % d)
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 236: Save it as /mnt/user-data/outputs/Fact Find Transcript - DD.MM.YY - ([Name Surname]).pdf and present it via present_files / SendUserFile.
    now: Fact Find Transcript - DD.MM.YY - ([Name Surname]).pdf, and the same pattern for the Summary.
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 237: Source report (in the hand-over message, Paul's rule 28/10/2026).
    now: Paul's rule (06/10/2026):
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 237: In the reply that presents the PDF, state in a short list:
    now: "in the reply that presents the PDF (the report), and in the final reply (the audit, unedited)",
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 237: (a) which sources were found and used (Audio to Text file, transcript, Overview, any other document;
    now: (a) which sources were found and used (the form's data file and PDF, the transcript, the Overview, any other document;
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 237: (b) every Audio to Text field that was populated with status heard, verify or preset, with what was done with it (kept, filled in from the transcript, flagged) - confirmed fields can be counted rather
    now: (b) the form's fields by status, with every preset (or heard or verify) value and what was done with it (kept, filled in from the transcript, flagged);
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 237: (c) every difference found between the Audio to Text file and the transcript, Overview or documents, quoting both values;
    now: (c) every contradiction found between the form and the transcript, Overview or documents, SORTED or HIGHLIGHTED, quoting both values;
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 239: ABSOLUTE MUST — save every deliverable directly into the client's own folder
    now: ## save into the client's own folder (ABSOLUTE MUST)
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 241: *This step is not optional, is never skipped, and is never something Paul should have to ask for or remind Claude about.
    now: *This step is not optional, is never skipped, and is never something Paul should have to ask for.
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 241: Presenting a deliverable only in chat is not considered complete — the file must also land in the client's actual folder, every single time, per the Client File Access order above.
    now: the file must also land in the client's actual folder, every single time, per the Client File Access order (page 01).
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 245: the listed size must equal the size of the local file you sent.
    now: the listed size must equal the size of the local file you sent (run.py saved compares them).
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 245: if the old PDF is open on Paul's computer the write can be refused or the old copy can remain, and the staging copy can lag (the folder then shows a new time but the old size).
    now: if the old PDF is open on Paul's computer the write can be refused or the old copy can remain, and the staging copy can lag.
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 245: 15.10.26 - a Summary overwrite showed a new time but the previous size;
    now: After every save (and every overwrite), list the folder and confirm the file's size AND modified time are the new file's:
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 245: a second commit fixed it.
    now: if it does not, commit it again and list again.",
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 246: Correcting a source document already on file:
    now: The program shows one step at a time and will not show the next until the proof for this one is on file.
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 246: stage, edit narrowly, commit back to the exact same path.
    now: list the folder, stage the files, commit the finished PDF.
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 246: Never edit or overwrite the Fact Find (Audio to Text) PDF or JSON, or the Manual Fact Find - they are Paul's own records and are read-only for this skill.
    now: never edit or overwrite the Fact Find (Audio to Text) PDF or JSON, or the Manual Fact Find - they are Paul's own records.
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 247: This applies to the Fact Find Summary PDF (Step 7a) too.
    now: Source order - this order applies to every Fact Find run:
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 247: The Planner note (Step 7b) has no durable file form — this rule doesn't apply to it.
    now: Do not write the Planner note or the message to Sitamah by hand in this skill.
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 248: Confirm the save, don't just attempt it.
    now: Never save one spouse's reports into the other's folder.
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 252: contact details, template defaults, fields resolvable from other documents on file or from the Audio to Text file, a policy number resolved from the actual schedule, an FNA/Shortfall/Reduced quote wit
    now: contact details, template defaults, fields resolvable from other documents on file, a policy number resolved from the actual schedule, an FNA/Shortfall/Reduced quote with the wrong insurer or wrongly 
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 254: Do not proceed to Step 7 until the advisor confirms the Fact Find itself is correct.
    now: else "Paul's OK of this version of the Fact Find is not recorded")
    why: Reworded: the program draws the PDF, so the build helper script and the Word step are gone; the save-and-list-back rule and the source report are kept (references/07).
- old line 265: Feed the original client meeting transcript(s) (not the Fact Find) to client-teams-transcript-skill's own reading/verification steps (Step 1/1b, including its Two-Read Lock).
    now: This skill takes them as the FIRST source, adds the Teams transcript, the latest Overview and the client's other documents, and combines them into the completed Fact Find:
    why: Moved to client-teams-transcript-skill (Paul, 02/11/2026 and 06/11/2026): that skill makes the Planner note page and the message to Sitamah once, and posts the message automatically; this skill only hands over to it (references/08-chain.md).
- old line 265: If the call dropped and reconnected, run that skill's own "verify the transcript is complete" check across all files together.
    now: if the client's Teams call dropped and reconnected, there will be two (or more) transcript files for the same date.
    why: Moved to client-teams-transcript-skill (Paul, 02/11/2026 and 06/11/2026): that skill makes the Planner note page and the message to Sitamah once, and posts the message automatically; this skill only hands over to it (references/08-chain.md).
- old line 273: verified by listing the folder back), then present the Planner note as its copy-ready Artifact page, in client-teams-transcript-skill's Output 1 planning-area structure, with one short sentence in the
    now: The program reads the transcript, builds the short Planner note page (one-line bullets per planning area, only the actions for now, in order), checks it, and builds the message to Sitamah.
    why: Moved to client-teams-transcript-skill (Paul, 02/11/2026 and 06/11/2026): that skill makes the Planner note page and the message to Sitamah once, and posts the message automatically; this skill only hands over to it (references/08-chain.md).
- old line 273: Only after all three are approved and saved, finish with Step 8 (the Teams message to Sitamah).
    now: the Fact Find Summary (fact-find-summary), and the Planner note page and the message to Sitamah (client-teams-transcript-skill).
    why: Moved to client-teams-transcript-skill (Paul, 02/11/2026 and 06/11/2026): that skill makes the Planner note page and the message to Sitamah once, and posts the message automatically; this skill only hands over to it (references/08-chain.md).


DROPPED (each is covered by a recorded decision):
- ---|---|: The Last updated line and the Recent changes table are kept by the stamp tool; the full history is in the repo's history/ folder (the old changelog pointed to a project document that no longer exists).
- ## Step 2: Follow the Audio to Text file's own layout (v3.0): Replaced by scripts/layout.json: the program draws the 11 sections, with these labels and in this order, every time (Paul's decision 15, kept).
- ## Step 3a: Mandatory final re-verification pass — the whole transcrip: Step 3a (the 13-point re-check) is replaced by the program's own checks and the audit; each rule it re-checked stays once, where it applies (references/06-mapping-rules.md, 02, 03, 04).
- This pass is in addition to, not a replacement for, the transcript-acc: Step 3a (the 13-point re-check) is replaced by the program's own checks and the audit; each rule it re-checked stays once, where it applies (references/06-mapping-rules.md, 02, 03, 04).
- 7b. Planner / AdviceTech note (via client-teams-transcript-skill's Out: Moved to client-teams-transcript-skill (Paul, 02/11/2026 and 06/11/2026): that skill makes the Planner note page and the message to Sitamah once, and posts the message automatically; this skill only hands over to it (references/08-chain.md).
- As of 07.10.26, the Fact Find/first-appointment Planner note is produc: Moved to client-teams-transcript-skill (Paul, 02/11/2026 and 06/11/2026): that skill makes the Planner note page and the message to Sitamah once, and posts the message automatically; this skill only hands over to it (references/08-chain.md).
- ## Step 8: Notify Sitamah in Teams (Paul's rule, 09/10/2026 - every cl: Moved to client-teams-transcript-skill (Paul, 02/11/2026 and 06/11/2026): that skill makes the Planner note page and the message to Sitamah once, and posts the message automatically; this skill only hands over to it (references/08-chain.md).
