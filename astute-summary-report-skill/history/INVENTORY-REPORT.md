INVENTORY of the old skill: 173 sentences
  kept (word for word or nearly): 27
  reworded, with a recorded change: 103
  dropped, with a recorded decision: 43
  UNACCOUNTED: 0


REWORDED (each is covered by a recorded change):
- old line 27: If something is unclear, ask or flag it.
    now: If something is unclear, flag it.
    why: Shortened; the program now enforces it.
- old line 29: Never say something is done, saved, proposed or live until you have checked it.
    now: Never say a change is live until he confirms.
    why: Shortened; the program now enforces it.
- old line 31: re-check that point and everything related, fix it everywhere, re-run the Verification checklist, and re-deliver in full.
    now: "the tries are logged in order and the report is in the run folder as a real PDF"
    why: Shortened; the program now enforces it.
- old line 32: A frustrated user, a short request or a "quick" skill does not relax any rule here.
    now: %r is not a date (enter DD/MM/YYYY, or leave it empty if the report does not show it)" % (label, value)
    why: Shortened; the program now enforces it.
- old line 36: *Delivery gate for this skill (rules 5 and 6 applied):
    now: which version of this skill is running.
    why: The Delivery gate is now done by the checker.
- old line 36: a run is complete only when ALL of these are done and confirmed in one line each:
    now: acknowledge the page with a one-line note of what is on it:
    why: The Delivery gate is now done by the checker.
- old line 36: (1) the Astute report was located in the client's "5.
    now: "Find the client's Astute report (a PDF) in the client's 5.
    why: The Delivery gate is now done by the checker.
- old line 36: Astute" folder (or supplied by Paul) and every page was read;
    now: Astute folder the report was read from:
    why: The Delivery gate is now done by the checker.
- old line 36: (2) product descriptions were verified online per Step 3, and every figure was checked against the report;
    now: ("Product descriptions were cross-checked against the insurers' own public product information where a source could be found;
    why: The Delivery gate is now done by the checker.
- old line 36: (3) the summary PDF was built to the Step 4 structure, with every flag from the standing rules included, and checked page by page as images;
    now: The Astute Report Summary PDF, drawn by the program from the data you entered, saved into the client's 5.
    why: The Delivery gate is now done by the checker.
- old line 36: (4) the PDF was saved in the same "5.
    now: "Save the PDF in the client's 5.
    why: The Delivery gate is now done by the checker.
- old line 36: Astute" folder with the correct filename and the folder listing was checked;
    now: One line saying where the summary was saved (the file name and the folder), or that it was NOT saved and why.
    why: The Delivery gate is now done by the checker.
- old line 36: (5) the PDF was sent in the chat with the short flag summary.
    now: the PDF is sent in the chat as well, and the chat copy never replaces the saved copy.
    why: The Delivery gate is now done by the checker.
- old line 36: After ANY correction, repeat (2) to (5) for every deliverable that changed.
    now: """A correction re-opens every later step (Paul:
    why: The Delivery gate is now done by the checker.
- old line 47: ## Purpose and when to use it
    now: print("Name to use in the client's 5.
    why: The section heading became part of the description and the rules.
- old line 49: Turns a client's Astute Consolidated Client Portfolio (CCP) report into a polished, verified, tabulated PDF summary for Paul Kafentzis at Wealth Revolution (FSP45946).
    now: The Astute (Consolidated Client Portfolio) report is a PDF.
    why: Shortened and moved.
- old line 49: Use it whenever Paul asks to summarize, break down or redo an Astute report or CCP report for a named client.
    now: Use for 'summarize the Astute/CCP report'."
    why: Shortened and moved.
- old line 49: It does not analyze, critique or compare policies (that is life-policy-schedule-analyzer).
    now: This skill does not draw the Astute report (Sitamah does) and does not analyse policies (life-policy-schedule-analyzer).
    why: Shortened and moved.
- old line 51: Locate the Astute report (exact to the letter)
    now: R.add(False, "The Astute report is not in the run folder yet", "step 'locate':
    why: Step 1 is now the locate step.
- old line 53: Follow this order every time, without asking first:
    now: Try the routes IN THIS ORDER and record EVERY try, failures too:",
    why: The 8:45 window is dropped and Zapier is added (Paul's answer 3, 03/11/2026).
- old line 55: Through the device bridge, check both locations under liferisk.co.za for the client's folder:
    now: Astute subfolder under liferisk.co.za, in either Company - Paul or Company - WR Clients -> Paul Kafentzis (Client Files).
    why: Local-first rule replaced by the standard route order; the PDF check is done by the program.
- old line 55: Company - Paul and Company - WR Clients -> Paul Kafentzis (Client Files).
    now: Astute subfolder under liferisk.co.za, in either Company - Paul or Company - WR Clients -> Paul Kafentzis (Client Files).
    why: Local-first rule replaced by the standard route order; the PDF check is done by the program.
- old line 55: Use whichever location actually holds it.
    now: Check both and use whichever holds it.
    why: Local-first rule replaced by the standard route order; the PDF check is done by the program.
- old line 56: SharePoint only if the local machine cannot be reached (it is normally reachable only around 8:45 Athens time on weekdays, so an unreachable machine outside that window is expected, not a fault).
    now: "If the client's folder cannot be found (the report was attached by Paul), deliver in the chat only and say plainly that it was not saved."
    why: Local-first rule replaced by the standard route order; the PDF check is done by the program.
- old line 56: Run the same two-location check there.
    now: the figure check is then attested, not proven.
    why: Local-first rule replaced by the standard route order; the PDF check is done by the program.
- old line 57: Ask Paul to attach the report only after both have genuinely been tried, or use a report he has already attached.
    now: Ask Paul to attach the report only after all three were tried and failed, or use a report he has already attached.
    why: Local-first rule replaced by the standard route order; the PDF check is done by the program.
- old line 59: Astute" holds more than one report, use the most recent by report date unless Paul names another, and say which one you used.
    now: use the most recent by report date unless Paul names another, and say which one you used and why (--folder-count and --chosen).
    why: Local-first rule replaced by the standard route order; the PDF check is done by the program.
- old line 60: Check the file really is a complete PDF (file, page count).
    now: raise ValueError("this file is not a PDF (some 'PDF' files are zipped page images:
    why: Local-first rule replaced by the standard route order; the PDF check is done by the program.
- old line 60: Some "PDF" files are zipped page images:
    now: raise ValueError("this file is not a PDF (some 'PDF' files are zipped page images:
    why: Local-first rule replaced by the standard route order; the PDF check is done by the program.
- old line 60: If pages are missing, say so.
    now: If a rule cannot be met, stop and say so;
    why: Local-first rule replaced by the standard route order; the PDF check is done by the program.
- old line 62: Read the whole report (exact to the letter)
    now: R.add(False, "The report could not be read:
    why: Step 2 is now the read step with a reading lock.
- old line 64: Record the report reference, report date, client name (and the name Astute holds if different), ID number and date of birth, and every provider block, including providers that returned "client record 
    now: the report reference, report date, the client's name (and the name Astute holds, if different), ID number, date of birth, who requested it, and EVERY provider block, including providers that returned 
    why: The reading lock replaces 'read every page'.
- old line 64: Use the pdf-reading skill if the content is not already in view.
    now: A figure that is not in the
    why: The reading lock replaces 'read every page'.
- old line 66: Verify product descriptions (judgment, within the rules)
    now: "that each product description is true (only the recorded source is checked)"]
    why: Step 3 is now the products step.
- old line 68: For every product, search the web for the insurer's own current product page or guide, and cross-check with a second independent source before stating what the product is.
    now: "For EACH distinct product the program listed, search the insurer's own current product page (one search per product name, not per policy).
    why: Paul's answer 2: one search per distinct product, source recorded.
- old line 68: If a product cannot be confirmed online, say so in the table and rely on what the report states.
    now: If a rule cannot be met, stop and say so;
    why: Paul's answer 2: one search per distinct product, source recorded.
- old line 70: Content and report structure (fixed section order)
    now: "Enter the report's data in the fixed layout;
    why: Step 4 is now the data, flags and build steps.
- old line 72: title, client name, ID number, date of birth, report reference and date, requested by, and a one-paragraph note that descriptions were cross-checked against public provider information and that orange
    now: the header (client, ID number, date of birth, report reference and date, requested by, and a short note that descriptions were cross-checked and orange flags need verification);
    why: Built by the program.
- old line 74: Risk Covers first, then Investments.
    now: Section 1 Active Policies (risk covers first, then investments);
    why: Built by the program from the entered data.
- old line 74: One gold heading band per insurer.
    now: head = (lead if k == 0 else []) + [insurer_band(g["provider"])]
    why: Built by the program from the entered data.
- old line 74: One table per policy group with these columns:
    now: one line per check with a green tick or a red cross, and one
    why: Built by the program from the entered data.
- old line 75: Policy Number / Product Name (verified) with a short accurate description / Status and start date / Benefit(s) and cover amount / Stand-alone or Accelerated / Premium and Premium Pattern.
    now: out.append(table(["Policy number / Product (verified)", "Status and start date", "Benefit(s) and cover amount", "Stand-alone or Accelerated", "Premium and premium pattern"],
    why: Built by the program from the entered data.
- old line 76: Policy Number / Product Name (verified) with description / Status and start date / Values (premiums paid, fund value, surrender value, Two-Pot pots where shown) / Premium Pattern / Fund allocation.
    now: out.append(table(["Policy number / Product (verified)", "Status and start date", "Values", "Premium pattern", "Fund allocation"],
    why: Built by the program from the entered data.
- old line 76: Add owner, life assured, premium payer and beneficiaries (with percentages) under each policy.
    now: Include owner, life assured, premium payer and beneficiaries (with percentages) wherever the report shows them.
    why: Built by the program from the entered data.
- old line 77: For every benefit state Stand-alone or Accelerated;
    now: BENEFIT_TYPES = ("stand-alone", "accelerated", "unable")
    why: Built by the program from the entered data.
- old line 77: if the report does not allow it, write "Unable to determine - verify with insurer".
    now: "Unable to determine - verify with insurer"}[b["type"]] for b in p["benefits"]]
    why: Built by the program from the entered data.
- old line 78: For every policy state the premium pattern:
    now: Every benefit is labelled stand-alone or accelerated and every policy has a premium pattern.
    why: Built by the program from the entered data.
- old line 78: ACI, ABI, age-rated, fixed, or other (for example single payment, or a fixed escalation rate).
    now: premium_pattern is ACI, ABI, age-rated, fixed or other (use the insurer's own naming in pattern_text, with the stated escalation percentage).
    why: Built by the program from the entered data.
- old line 78: Use the insurer's own naming (for example funding pattern plus annual benefit increase) and the stated escalation percentage.
    now: premium_pattern is ACI, ABI, age-rated, fixed or other (use the insurer's own naming in pattern_text, with the stated escalation percentage).
    why: Built by the program from the entered data.
- old line 80: Group Risk and Retirement Funds.
    now: Section 2 Group Risk and Retirement Funds;
    why: Built by the program.
- old line 80: State plainly whether Group Risk cover exists and whether a Pension or Provident Fund is reflected.
    now: for key, label in (("group_risk", "Group Risk cover"), ("retirement_fund", "Pension or Provident Fund")):
    why: Built by the program.
- old line 80: If present, give all details:
    now: if s2[k]["reflected"] and not s2[k].get("details"):
    why: Built by the program.
- old line 82: List every policy Astute labels paid-up, with full details.
    now: """Only a policy Astute labels paid-up goes in Section 3;
    why: Decided by the program from the status as Astute shows it.
- old line 82: If none, say so plainly.
    now: If none apply, say so with a reason.
    why: Decided by the program from the status as Astute shows it.
- old line 84: Inactive, Lapsed or Surrendered Policies.
    now: Inactive, Lapsed or Surrendered Policies", "General Verification Notes"],
    why: Decided by the program.
- old line 84: Policies that are neither active nor labelled paid-up, with the same full details.
    now: a policy with zero values that Astute does not label paid-up (it is NOT shown as paid-up);
    why: Decided by the program.
- old line 86: Always include the cession note (see standing rules), and one line naming providers that returned "not found" or "unable to match".
    now: gen.append(("Providers that returned no data (not found, unable to match or no row):
    why: Built by the program.
- old line 88: Place a flag directly above the affected table for:
    now: A flag sits above the table of the policy (or product) it is about."""
    why: The computable flags are raised by the program; the judgement ones are added with a reason.
- old line 88: an unknown or thinly described product, an RA versus endowment wrapper ambiguity, a status contradiction between package and underlying policies, a provider that returned no data, and any zero or miss
    now: status contradictions, unknown products, wrapper ambiguities, providers with no data, zero or missing values, mismatched totals, unconfirmed products, bank insurance arms, other.
    why: The computable flags are raised by the program; the judgement ones are added with a reason.
- old line 90: Build the PDF (a pattern to follow)
    now: w.die("The PDF has not been built yet (run.py build).")
    why: Step 5 is now the build step.
- old line 92: Use ReportLab Platypus in the workspace (pip install reportlab --break-system-packages if missing;
    now: If the report was found elsewhere in the client's folder, save the summary beside it and tell Paul.
    why: The drawing code is fixed in the skill instead of rewritten each run.
- old line 92: Do not draw from memory of an earlier client:
    now: You do not work from memory of this page:
    why: The drawing code is fixed in the skill instead of rewritten each run.
- old line 92: build from this run's report only.
    now: a total that differs from the report's own total;
    why: The drawing code is fixed in the skill instead of rewritten each run.
- old line 93: Landscape A4, 15 mm margins, column widths in millimetres, repeatRows=1 on every table.
    now: t = Table([[P(h, th) for h in head]] + rows, colWidths=cw, repeatRows=1)
    why: The drawing code is fixed in the skill instead of rewritten each run.
- old line 94: Custom ParagraphStyle objects for all cell text (default styles do not render correctly in table cells).
    now: foot = all(content["footer"] in p["text"] and ("Page %d" % (i + 1)) in p["text"] for i, p in enumerate(pages))
    why: The drawing code is fixed in the skill instead of rewritten each run.
- old line 94: and use <br/> for line breaks inside paragraphs.
    now: for line in step["do"]:
    why: The drawing code is fixed in the skill instead of rewritten each run.
- old line 95: navy #1B2A4A for the title, section bars and table headers;
    now: landscape A4, 15 mm margins, navy title, section bars and table headers (#1B2A4A), gold insurer bands (#9C7A28), light grey row stripes
    why: The drawing code is fixed in the skill instead of rewritten each run.
- old line 95: gold #9C7A28 for insurer bands;
    now: search for the insurer's own current product page or guide.
    why: The drawing code is fixed in the skill instead of rewritten each run.
- old line 95: light grey #F2F2F2 row stripes with #DADADA grid;
    now: A provider that returned no row at all is not proof of no cover:
    why: The drawing code is fixed in the skill instead of rewritten each run.
- old line 95: flag boxes as a nested Table with background #FFF4E5, border #C97A1A, bold title in #C97A1A and text in #5A3E00.
    now: (#F2F2F2) with a #DADADA grid, orange flag boxes (background #FFF4E5, border #C97A1A, title #C97A1A, text #5A3E00), repeatRows=1 on every table, and a
    why: The drawing code is fixed in the skill instead of rewritten each run.
- old line 96: Footer and page numbers through onFirstPage and onLaterPages:
    now: doc.build(story, onFirstPage=footer, onLaterPages=footer)
    why: The drawing code is fixed in the skill instead of rewritten each run.
- old line 96: "Astute Report Summary - [Client name] - Confidential" and "Page N".
    now: footer "Astute Report Summary - [Client name] - Confidential" with "Page N".
    why: The drawing code is fixed in the skill instead of rewritten each run.
- old line 97: Copy every figure to the cent.
    now: Every figure comes from the Astute report.
    why: The drawing code is fixed in the skill instead of rewritten each run.
- old line 97: Any total shown is added up in code from its components and must equal what the report shows;
    now: Its description is only what the report says." % n})
    why: The drawing code is fixed in the skill instead of rewritten each run.
- old line 97: if it does not, flag it.
    now: If something is unclear, flag it.
    why: The drawing code is fixed in the skill instead of rewritten each run.
- old line 98: Convert every page to PNG with pdftoppm, look at each one, and fix overflow, clipped text or a stranded heading before delivering.
    now: Look at every page image for clipped text or a stranded heading;
    why: The drawing code is fixed in the skill instead of rewritten each run.
- old line 100: Save and deliver (exact to the letter)
    now: say plainly that it was not saved and deliver in the chat only.
    why: Step 6 is now the save and final steps.
- old line 102: name = client first name then surname).
    now: run.py start <run> --client "First Surname"
    why: Local-first rule replaced by the standard route order; the PDF check is done by the program.
- old line 103: local machine first through the device bridge, SharePoint (Microsoft_365:sharepoint_upload_file) only if the machine is unreachable.
    now: 1 the computer (device bridge), 2 the Microsoft 365 connector (SharePoint / OneDrive), 3 Zapier.
    why: Local-first rule replaced by the standard route order; the PDF check is done by the program.
- old line 103: Never overwrite an existing file without checking;
    now: Never rewrite one during a run, and never type the file name, a total or the content.
    why: Local-first rule replaced by the standard route order; the PDF check is done by the program.
- old line 103: if one exists, keep both with a version suffix and tell Paul.
    now: If text is clipped or a heading is stranded, tell Paul;
    why: Local-first rule replaced by the standard route order; the PDF check is done by the program.
- old line 104: If Paul attached the report and the client's folder cannot be found, deliver in the chat only and say plainly that it was not saved.
    now: "If the client's folder cannot be found (the report was attached by Paul), deliver in the chat only and say plainly that it was not saved."
    why: Local-first rule replaced by the standard route order; the PDF check is done by the program.
- old line 105: List the folder and confirm the PDF is there before saying it is saved.
    now: Then list the folder and record what it shows;
    why: Local-first rule replaced by the standard route order; the PDF check is done by the program.
- old line 106: Send the PDF in the chat (SendUserFile) as well.
    now: The PDF in the chat.
    why: Local-first rule replaced by the standard route order; the PDF check is done by the program.
- old line 106: The chat copy never replaces the saved copy.
    now: the PDF is sent in the chat as well, and the chat copy never replaces the saved copy.
    why: Local-first rule replaced by the standard route order; the PDF check is done by the program.
- old line 107: one line saying where it was saved, then a short numbered list of every flag Paul should verify, most important first.
    now: "The numbered flag list (most important first)",
    why: Local-first rule replaced by the standard route order; the PDF check is done by the program.
- old line 124: A figure that is unclear is flagged, not guessed.
    now: A figure that is unclear or absent is left empty and flagged, not guessed.
    why: Kept, shortened.
- old line 125: Always include the general cession note, and flag any policy held with a bank's insurance arm for direct verification with the insurer.
    now: The cession note is always in the General Verification Notes, and a policy held with a bank's insurance arm is flagged for direct verification with the insurer.
    why: Kept, shortened.
- old line 129: Surrendered and lapsed policies go in Additional Notes.
    now: Surrendered, lapsed and other inactive policies go in Additional Notes.
    why: Kept, shortened.
- old line 131: Every benefit carries a stand-alone or accelerated label and every policy a premium pattern.
    now: Every benefit is labelled stand-alone or accelerated and every policy has a premium pattern.
    why: Kept, shortened.
- old line 133: ## Verification checklist (run before saying it is done)
    now: "pasted into the reply as it is:
    why: The checklist is now the checker.
- old line 135: [ ] Every page of the report was read, and the file was complete.
    now: print("Every policy number, figure, date and name entered was found in the report's own text.")
    why: Done by the checker.
- old line 136: [ ] Every product description was verified online, or marked as unverified.
    now: "every product has a recorded source, or is recorded as unconfirmed (which raises an orange flag)"
    why: Done by the checker.
- old line 137: [ ] Every figure matches the report to the cent;
    now: Every figure comes from the Astute report.
    why: Done by the checker.
- old line 137: every total was added up in code.
    now: "every page was served in order and acknowledged"
    why: Done by the checker.
- old line 138: [ ] Sections 1 to 3, Additional Notes (where applicable) and General Verification Notes are present in order.
    now: The cession note is always in the General Verification Notes, and a policy held with a bank's insurance arm is flagged for direct verification with the insurer.
    why: Done by the checker.
- old line 139: [ ] Risk covers come before investments, with one heading band per insurer.
    now: risk covers, investments, group risk, retirement funds, paid-up policies.
    why: Done by the checker.
- old line 140: [ ] Every benefit has stand-alone or accelerated;
    now: BENEFIT_TYPES = ("stand-alone", "accelerated", "unable")
    why: Done by the checker.
- old line 140: every policy has a premium pattern.
    now: Every benefit is labelled stand-alone or accelerated and every policy has a premium pattern.
    why: Done by the checker.
- old line 141: [ ] All required flags are in the document, including the cession note.
    now: """[{provider, flags, policies}] in the order the providers appear in the report.
    why: Done by the checker.
- old line 142: [ ] Every page was viewed as an image with no clipping or overflow.
    now: a page with no readable text must be viewed as an image by you.",
    why: Done by the checker.
- old line 143: Astute" with the correct filename, and the folder listing was checked.
    now: One line saying where the summary was saved (the file name and the folder), or that it was NOT saved and why.
    why: Done by the checker.
- old line 144: [ ] PDF sent in the chat with the numbered flag list.
    now: "The final check, the numbered flag list and the SHORT AUDIT for Paul",
    why: Done by the checker.


DROPPED (each is covered by a recorded decision):
- # | Section | What it covers |: Replaced by the new short Index (five sections).
- ## UNIVERSAL OPERATING RULES - READ FIRST, APPLY TO EVERY STEP OF THE : The preamble and heading are replaced by the short intro of references/00-rules.md; the program shows the rules at the start and the right page at each step.
- Re-load this skill before you start, and again after any compression. : Rule 1 (re-load this skill) is replaced by the program: it shows the standing rules at the start and the right page at each step, and `run.py status` tells a chat where the job is up to after a compression.
- Read before you write. Read the Astute report and the relevant product: Rule 3 (read before you write) is replaced by the reading lock: the program serves the report page by page and each page is acknowledged.
- Deliver everything this skill lists, every time. A run is not finished: Rule 5 (deliver everything) is replaced by deliverables.json and the checker: a run is finished only with a PASS audit.
- Changes to a skill: edit the existing skill, never create a duplicate.: Rule 9 (changes through the propose_skills card) is replaced by standard S7: skills are changed only in Claude Code and uploaded as a zip by Paul; the 'never say it is live' part is standing rule 6 in SKILL.md.
- Last updated: 2026-10-14 12:21 (Athens/Greece time): The hand-typed stamp, the Recent changes table and the maintenance note are replaced by the stamp program (S2); the full history is in the repo's history folder.
- ## Key contacts and tools: The Key contacts and tools section is replaced by the steps: the routes are in references/01-locate.md, and the program needs pdfplumber, reportlab and pdftoppm (checked at the start). The pdf-reading skill never existed; web search is used in the products step; the chat sends the PDF itself.
