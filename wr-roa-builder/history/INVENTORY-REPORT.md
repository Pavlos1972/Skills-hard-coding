INVENTORY of the old skill: 1055 sentences
  kept (word for word or nearly): 26
  reworded, with a recorded change: 940
  dropped, with a recorded decision: 89
  UNACCOUNTED: 0


REWORDED (each is covered by a recorded change):
- old line 32: Write only what is in the source material (transcript, quote, document, file) or in a named document this skill tells you to use.
    now: "the tries are logged in order and every required document is registered (or Paul said it does not exist)"
    why: Shortened; enforced by the program.
- old line 32: If a line is unclear, garbled or ambiguous, do not turn it into a fact:
    now: If a line is unclear, flag it.
    why: Shortened; enforced by the program.
- old line 32: flag it to the user.
    now: It refuses to skip a step.
    why: Shortened; enforced by the program.
- old line 32: "It seems implied", "it is usual" and "it would make sense" are not sources.
    now: if t is not None and t.text and 'RAR reference number:' in t.text:
    why: Shortened; enforced by the program.
- old line 34: Never tell the user something is done, saved, sent, visible or working until you have checked it yourself (open the file, list the folder, look at the screen).
    now: Never tell Paul the ROA is done or saved until the program's checks are all green and the folder listing matched.
    why: Shortened; enforced by the program.
- old line 36: Every correction re-opens the whole task, not just the item.
    now: Every correction re-opens the whole task.
    why: Shortened; enforced by the program.
- old line 36: When the user corrects anything:
    now: the program refuses anything else.
    why: Shortened; enforced by the program.
- old line 36: (a) go back to the source and re-check that point and everything related to it;
    now: 1 | Run it | The one command that starts the job and how every step works |
    why: Shortened; enforced by the program.
- old line 36: (b) fix it everywhere it appears, in every deliverable;
    now: the client's name appears in every place and the ID line reads "I, Name, (ID:
    why: Shortened; enforced by the program.
- old line 36: (c) re-run this skill's full checklist;
    now: %s), hereby confirm" % (nm, cid)) in full and re.fullmatch(r"\d{13}", cid) is not None,
    why: Shortened; enforced by the program.
- old line 36: (d) re-deliver every affected deliverable in full, as in rule 5.
    now: print("EVERY STEP IS DONE.\nPut this SHORT AUDIT in your reply, as it is (nothing longer):\n")
    why: Shortened; enforced by the program.
- old line 36: Never fix only the item named and stop.
    now: If anything is wrong, fix the answers or the email page and rebuild;
    why: Shortened; enforced by the program.
- old line 37: A correction, a frustrated user, a short request or a "quick" task does not relax any rule in this skill.
    now: A correction, a frustrated user or a "quick" task never lowers the standard.
    why: Shortened; enforced by the program.
- old line 38: State exactly which rule or step could not be completed and why.
    now: the page images could not be made (%s).
    why: Shortened; enforced by the program.
- old line 38: Never hand over partial work as if it were complete.
    now: never hand over partial work as complete.
    why: Shortened; enforced by the program.
- old line 41: *Delivery gate for this skill (rules 5 and 6 applied):
    now: which version of this skill is running.
    why: The audit is done by the program (Paul's answer 2).
- old line 41: a run is complete only when ALL of these are done and confirmed in one line each:
    now: Read each page fully, then acknowledge it with a one-line note (run.py read {run} --ack ROLE:PAGE --note \"...\").
    why: The audit is done by the program (Paul's answer 2).
- old line 41: (1) the source documents were located and read and the setup answers derived (Steps 0, 0b and 1-2);
    now: run.py answers <run> --file answers.json                                      the setup answers (Step 0b), each with its source
    why: The audit is done by the program (Paul's answer 2).
- old line 41: (2) the ROA .docx was built per Document construction, with the Step 7 mandatory pre-delivery audit completed;
    now: """Opens the finished ROA (.docx) and proves what a program can prove of the old skill's 21-point pre-delivery audit.
    why: The audit is done by the program (Paul's answer 2).
- old line 41: (3) the finished ROA was sent in the chat with the exact required delivery filename;
    now: """Build the required delivery filename:
    why: The audit is done by the program (Paul's answer 2).
- old line 41: (4) the same file was saved in the client's folder per the Delivery section, and the tool result was checked (the full path appears in the written list and nothing was rejected).
    now: confirm from the tool's result that the full path is in written and rejected is empty.
    why: The audit is done by the program (Paul's answer 2).
- old line 41: After ANY correction, repeat (2) to (4) for every deliverable that changed.
    now: Every correction re-opens the whole task.
    why: The audit is done by the program (Paul's answer 2).
- old line 58: This skill packages Paul Kafentzis's process for completing a Record and Confirmation
    now: It is a bank paragraph word for word, one of the fixed sentences, the specific reason Paul gave for a declined need, or (Retirement and Investment) the pointer line to the client's own reply email.
    why: Shortened.
- old line 59: of Advice (ROA) for Wealth Revolution clients, using assets/ROA_Template_2026.docx.
    now: TEMPLATE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "ROA_Template_2026.docx")
    why: Shortened.
- old line 60: This is a compliance document required under the General Code of Conduct (s9) — a
    now: A Record and Confirmation of Advice (ROA) is a compliance document under the General Code of Conduct (s9).
    why: Shortened.
- old line 61: wrong dropdown selection, a mismatched reason paragraph, or a guessed figure is a
    now: A wrong dropdown, a mismatched reason paragraph or a guessed figure is a real-world compliance error, not a cosmetic slip.
    why: Shortened.
- old line 62: real-world compliance error, not a cosmetic slip.
    now: A wrong dropdown, a mismatched reason paragraph or a guessed figure is a real-world compliance error, not a cosmetic slip.
    why: Shortened.
- old line 66: Every ROA covers exactly one of three bundles.
    now: """The one checker of the wr-roa-builder.
    why: Moved; the program enforces one bundle.
- old line 66: Never mix bundles in the same
    now: if b not in BUNDLES:
    why: Moved; the program enforces one bundle.
- old line 69: Bundle | Sections actively completed | All other sections |
    now: # income_after24 is NEVER actively completed, even within the risk bundle — BR's
    why: Moved; the program enforces one bundle.
- old line 71: Risk | Death (Life), Lump Sum Disability, Income Protection (1st 24 months + After 24 months), Dread Disease | Marked "Do not Review" |
    now: Risk (Death, Lump Sum Disability, Income Protection 1st 24 months, Dread Disease), Retirement, or Investment.
    why: Moved; the program enforces one bundle.
- old line 72: Retirement | Retirement Planning only | Marked "Do not Review" |
    now: set_sdt_plain_text(status_sdt, "DO NOT REVIEW")
    why: Moved; the program enforces one bundle.
- old line 73: Investment | Investment Planning only | Marked "Do not Review" |
    now: set_sdt_plain_text(status_sdt, "DO NOT REVIEW")
    why: Moved; the program enforces one bundle.
- old line 75: Its Status dropdown stays at its default
    now: this Status field untouched at its default.
    why: Moved; the program enforces one bundle.
- old line 76: ("DO NOT REVIEW") and is never actively touched.
    now: if s["status"] != "DO NOT REVIEW" or has_tbl:
    why: Moved; the program enforces one bundle.
- old line 78: For sections marked "Do not Review" because they're outside the current bundle, the
    now: R.attested.append("entries written as text because they are not in the template's dropdown lists (%s)" % ";
    why: Moved; the program enforces one bundle.
- old line 79: "Reason this product suits your needs (required — s9(1)(c))" textbox always reads:
    now: if children[j].tag == _q('p') and 'Reason this product suits' in ''.join(children[j].itertext()):
    why: Moved; the program enforces one bundle.
- old line 80: > "This need was not considered in this Review meeting."
    now: NOT_CONSIDERED = "This need was not considered in this Review meeting."
    why: Moved; the program enforces one bundle.
- old line 82: ## Step 0 — Locate the client's source documents (local machine first, SharePoint only if the device is unreachable)
    now: Every answer comes from the client's own documents or from Paul's words and is recorded with its source.
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 84: *Local machine first via the device bridge:
    now: "the computer (local drive / OneDrive through the device bridge)",
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 84: liferisk.co.za\Company - Paul\New Business\[Surname, First Name]\...
    now: the client's own folder, liferisk.co.za\Company - Paul\New Business\[Surname, First Name]\...
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 84: Use the SharePoint/Outlook search below only if the local machine cannot be reached.
    now: if the accepted proposal is not saved as a PDF, find it in Outlook (outlook_email_search / read_resource, match on the subject thread:
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 86: Client documents almost never arrive as chat uploads — they live in the client's own
    now: Client documents almost never arrive as chat uploads.
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 87: folder under Paul/New Business/[Surname, First Name (...)]/ in SharePoint.
    now: the client's own folder, liferisk.co.za\Company - Paul\New Business\[Surname, First Name]\...
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 88: only ask the user to upload something if it genuinely can't be
    now: Ask Paul to upload something only after all three were tried and failed.
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 91: Find the client folder with Microsoft 365:sharepoint_search, querying the
    now: 1 the computer (device bridge), 2 the Microsoft 365 connector (sharepoint_search, then read_resource on the hit's uri:
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 92: A client can have multiple sibling folders for different
    now: A client can have several sibling folders for different products at once:
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 93: products/transactions at once (e.g.
    now: Recognise this failure at once:
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 93: an OM Optimal RA folder alongside an OM Tax
    now: Planning" (optionally "Saving for Retirement" as an alternate wording), the same
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 94: Free folder and an on-hold Risk Covers folder) — confirm which one matches the
    now: confirm which one matches the bundle being built before pulling documents from it;
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 95: bundle/product actually being built before pulling documents from it;
    now: confirm which one matches the bundle being built before pulling documents from it;
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 96: the first result is the right one.
    now: never assume the first result is the right one.
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 97: Pull the specific documents needed — Fact Find Summary Report, FNA/comparative
    now: a different document, and the ROA needs both), fact_find_summary.
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 98: — via sharepoint_search (optionally scoped with
    now: a search result is only a snippet), 3 Zapier.
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 99: folderName) or by browsing the client folder's subfolder listing
    now: R.attested.append("that the file really sits in the client's folder (the listing is typed by the chat)")
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 100: Fact Find, Comparative Quotes, Applications,
    now: Fact Find, Comparative Quotes, Applications, ROA & Bus ROA.
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 101: ROA & Bus ROA, etc.) using read_resource on the folder's file:/// URI.
    now: 1 the computer (device bridge), 2 the Microsoft 365 connector (sharepoint_search, then read_resource on the hit's uri:
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 102: follow up with read_resource on a search hit's uri — the search result itself
    now: "the page opens on the client's own reply with their acceptance wording, then the quoted proposal (or this is a Risk ROA)"
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 103: is only a short content snippet, not the full document.
    now: add("RAR reference number:" not in full, "The RAR reference number field is gone")
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 104: folderName filtering is not fully reliable — a query can silently return
    now: Raises ValueError if it is not a readable PDF."""
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 105: zero hits even when the file is genuinely inside a folder by that name.
    now: One line saying where the ROA was saved (the file name and the folder), or that it was NOT saved and why.
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 106: targeted search comes up empty, retry with a broader folder name (e.g.
    now: If a targeted search with a folder name finds nothing, retry with a broader folder name or without the filter before concluding the document does not exist.
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 107: leading number, just "Fact Find") or drop the folder filter entirely before
    now: Find this skill's folder (the "Base directory" shown when the skill loaded;
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 108: concluding the document doesn't exist.
    now: "A required document that really does not exist:
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 109: Verify every required document from the Step 1 checklist is actually present and
    now: Verify every required document is present and current before going on:
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 110: current before proceeding — don't build from whatever happens to be sitting in
    now: do not build from whatever is in the folder.
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 111: Flag gaps explicitly (e.g.
    now: existing list entries (e.g.
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 111: only a raw KYC/intake form on file, not the
    now: Flag gaps (only a raw intake form on file, a proposal for a different amount than the one advised on) and ask Paul rather than silently substituting the nearest document.
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 112: summarized Fact Find Summary Report;
    now: ("proposal_email", "client_reply_email", "fact_find_summary"),
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 112: or a proposal on file for a different amount
    now: A client can have several sibling folders for different products at once:
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 113: than what's actually being advised on) and ask the user how to proceed (generate
    now: """Opens the finished ROA (.docx) and proves what a program can prove of the old skill's 21-point pre-delivery audit.
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 114: the missing summary, request an updated proposal, confirm the old one still
    now: the client's own reply email with the proposal quoted beneath (one HTML page)",
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 115: applies) rather than silently substituting the nearest document you found.
    now: never substitute the nearest document.
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 116: wr-roa-builder-changelog.md (2026-08-14 entry).
    now: WR ROA Builder — construction script.
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 117: Check Outlook when a proposal isn't already saved to SharePoint as a PDF — via
    now: Has a Status dropdown only (same 9-option list as above), defaulting to
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 118: Microsoft 365:outlook_email_search / read_resource, since an accepted proposal
    now: 1 the computer (device bridge), 2 the Microsoft 365 connector (sharepoint_search, then read_resource on the hit's uri:
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 119: sometimes only exists in the Sent Items thread.
    now: A file named %r already exists in the client's folder.
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 119: If found only as an email, save or
    now: If anything is wrong, fix the answers or the email page and rebuild;
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 120: convert it to the Email Proposal PDF the document-construction step needs (see
    now: "that each figure sits in the right column of the quote (it is only proven to appear in the document)"]
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 121: "Embedding the proposal email" below) rather than referencing the live email
    now: """Insert the accepted-proposal email pages (as images) into the Investment
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 123: Fact Find / KYC PDFs read via SharePoint's read_resource often come back as
    now: a Fact Find or KYC PDF read through SharePoint often comes back as field labels with none of the client's answers (the filled-in layer is not extracted).
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 124: labels only, with none of the client's actual answers.
    now: Multiple pages of labels with no values is the tell.
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 125: recognizable failure signature, not a fluke:
    now: "A required document that really does not exist:
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 125: these forms have an interactive/visual
    now: These rules apply from the first message to the last.
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 126: answer layer that SharePoint's text-extraction doesn't capture, so the page reads
    now: # blank literal text after "Date:"), so append the ROA date directly onto that
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 127: as an empty template even though it's genuinely filled in.
    now: the skill's programs, steps, rule pages or template changed while this run was in progress.
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 128: document is blank, and do not ask the user to manually retype values off their own
    now: Do not conclude the document is blank and do not ask Paul to retype values.
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 129: The fix is to read the PDF from the local machine (stage it and render the
    now: Read the PDF from the computer, or ask Paul to attach that PDF.
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 130: pages visually), or, if the device is unreachable, ask the user to upload that
    now: Read the PDF from the computer, or ask Paul to attach that PDF.
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 131: specific PDF directly into the chat — once it's a local file (not a SharePoint
    now: raise ValueError("this file is not a PDF (some 'PDF' files are zipped page images:
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 132: reference), it can be rasterized page-by-page and read visually (see the
    now: """Reads a client document's text (PDF or HTML/text), page by page, and checks that what the chat entered really appears in it.
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 133: pdf-reading skill), which does pick up values in that answer layer.
    now: a Fact Find or KYC PDF read through SharePoint often comes back as field labels with none of the client's answers (the filled-in layer is not extracted).
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 134: pattern immediately (multiple pages of field labels with zero filled values is the
    now: Multiple pages of labels with no values is the tell.
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 135: tell) rather than retrying the same SharePoint read with different page ranges or
    now: # both rows entirely rather than leaving them blank or "N/A"
    why: Local-first rule replaced by the standard route order (Paul's answer 5).
- old line 138: ## ROA date — always the date the client gave the go-ahead, never today's date or the proposal-send date
    now: The ROA date is the date the client gave the go-ahead, never today's date, never the date the document is built, never the date the proposal was first sent.
    why: The date and its source are entered and checked by the program.
- old line 140: *Standing rule, applies to every bundle (Risk, Retirement, Investment):
    now: run.py start <run> --client "First Surname" --bundle risk|retirement|investment
    why: The date and its source are entered and checked by the program.
- old line 141: date is the date the client gave their go-ahead on the specific proposal actually
    now: it is the date the client gave the go-ahead" % a["roa_date"])
    why: The date and its source are entered and checked by the program.
- old line 142: It is never today's date, never the date the ROA document happens to
    now: The ROA date is the date the client gave the go-ahead, never today's date, never the date the document is built, never the date the proposal was first sent.
    why: The date and its source are entered and checked by the program.
- old line 143: get built, and never the date the original proposal email was first sent — only the
    now: The ROA date is the date the client gave the go-ahead, never today's date, never the date the document is built, never the date the proposal was first sent.
    why: The date and its source are entered and checked by the program.
- old line 144: date the client actually committed.
    now: it is the date the client gave the go-ahead" % a["roa_date"])
    why: The date and its source are entered and checked by the program.
- old line 146: If the client replied in writing (email, WhatsApp, etc.) confirming acceptance,
    now: "If the client accepted the FNA in full:
    why: The date and its source are entered and checked by the program.
- old line 147: the ROA date is the date of that reply.
    now: The ROA date is the date the client gave the go-ahead.
    why: The date and its source are entered and checked by the program.
- old line 147: Search for this first — it always takes
    now: the date of the client's written reply (it always takes priority);
    why: The date and its source are entered and checked by the program.
- old line 148: priority over the fallback below if it exists.
    now: if two sources disagree (other than the premium rule and the verbal-acceptance date rule), list it under conflicts:
    why: The date and its source are entered and checked by the program.
- old line 149: If the go-ahead was given verbally (a phone call or in-person conversation) with
    now: if the go-ahead was verbal, the date of the adviser's recap email.
    why: The date and its source are entered and checked by the program.
- old line 150: no written reply from the client, look for an adviser follow-up email that recaps
    now: ("client_reply_email", "recap_email", "follow_up_notes"), "retirement":
    why: The date and its source are entered and checked by the program.
- old line 151: what was agreed (e.g.
    now: as stored in the dropdown (e.g.
    why: The date and its source are entered and checked by the program.
- old line 151: "Great to have spoken to you today...
    now: looks next to the ROA's own text, an image border near the footer):
    why: The date and its source are entered and checked by the program.
- old line 152: When no later written client reply
    now: the embedded email must open on the client's own reply.
    why: The date and its source are entered and checked by the program.
- old line 153: exists, the ROA date is the date of that recap email — it's the only dated
    now: if the go-ahead was verbal, the date of the adviser's recap email.
    why: The date and its source are entered and checked by the program.
- old line 154: record of the go-ahead.
    now: ("ROA date (the date the client gave the go-ahead)", "%s (%s:
    why: The date and its source are entered and checked by the program.
- old line 155: A transaction can go through several proposed amounts before the client commits
    now: A transaction can go through several proposed amounts:
    why: The date and its source are entered and checked by the program.
- old line 156: — always use the date the client agreed to the specific figure the ROA is actually
    now: use the date the client agreed to the figure the ROA is built for.
    why: The date and its source are entered and checked by the program.
- old line 157: being built for, never an earlier round's date.
    now: R.add(ok_a, "Setup answers valid and sourced (%s ROA for %s, ROA date %s);
    why: The date and its source are entered and checked by the program.
- old line 158: Risk bundle exception (confirmed by Paul):
    now: the Risk Tolerance questionnaire, confirmed by the Follow-Up Notes.
    why: The date and its source are entered and checked by the program.
- old line 158: verbal acceptance in the Teams meeting is sufficient for the ROA date;
    now: verbal acceptance in the Teams meeting is enough:
    why: The date and its source are entered and checked by the program.
- old line 158: take it from the latest Follow-Up Appointment Summary Notes.
    now: the latest Follow-Up Appointment Summary Notes (what was accepted and when, replacement context, risk tolerance, insurers compared);
    why: The date and its source are entered and checked by the program.
- old line 158: If a written client reply or recap email exists with a different date, use the written one and tell Paul.
    now: take the date from the latest Follow-Up Notes, but if a written client reply or recap email has a different date use the written one and tell Paul.
    why: The date and its source are entered and checked by the program.
- old line 159: Get this date right before building anything else — it determines the "Next
    now: print("\nSAY THIS TO PAUL FIRST, before anything else in your reply, in exactly these words:\n    %s.\n" % w.version_line())
    why: The date and its source are entered and checked by the program.
- old line 160: review/meeting date" too, since that's always ROA date + 12 months (Step 6).
    now: # --- Next meeting date = ROA date + 12 months ---
    why: The date and its source are entered and checked by the program.
- old line 162: wr-roa-builder-changelog.md (2026-08-25 entry, "ROA date sourced
    now: WR ROA Builder — construction script.
    why: The date and its source are entered and checked by the program.
- old line 163: from a verbal go-ahead recap email").
    now: if the go-ahead was verbal, the date of the adviser's recap email.
    why: The date and its source are entered and checked by the program.
- old line 165: ## Step 0b — Auto-derive the Step 1 answers (do this BEFORE asking Paul anything)
    now: how to derive each answer (Step 0b), the answers file, and the rules the program applies.
    why: Step 0b is run by the program (Paul's answer 6).
- old line 167: Read these sources, in this order, then show Paul ONE confirmation table (question | derived answer | source file) and ask only about genuine gaps or conflicts.
    now: Then the program shows Paul ONE confirmation table (question | answer | source).
    why: Step 0b is run by the program (Paul's answer 6).
- old line 169: Latest "WR Overview" PDF in 1.
    now: the latest "WR Overview" PDF;
    why: Step 0b is run by the program (Paul's answer 6).
- old line 169: Overview\2026 (newest by date in the filename):
    now: out.append("roa_date %s is in the future:
    why: Step 0b is run by the program (Paul's answer 6).
- old line 169: quotes presented, existing policies, products.
    now: Existing policies being replaced are not "considered".
    why: Step 0b is run by the program (Paul's answer 6).
- old line 170: The insurer application (e.g.
    now: Insurer not in the 9-option list (e.g.
    why: Step 0b is run by the program (Paul's answer 6).
- old line 170: BrightRock General Short Risk Application) in the transaction folder's Applications folder:
    now: the Follow-Up Notes, the application's cover-lines selection and the transaction folder name.
    why: Step 0b is run by the program (Paul's answer 6).
- old line 170: client name/ID, personal vs business cover lines, replacement section (replaced policy numbers), accepted benefits.
    now: the insurer application (client name and ID, personal or business cover lines, the replacement section, accepted benefits);
    why: Step 0b is run by the program (Paul's answer 6).
- old line 171: Latest "Follow-Up Appointment Summary Notes" in 2.
    now: the latest Follow-Up Appointment Summary Notes (what was accepted and when, replacement context, risk tolerance, insurers compared);
    why: Step 0b is run by the program (Paul's answer 6).
- old line 171: what was accepted, when, replacement context, risk tolerance outcome, insurers compared.
    now: the latest Follow-Up Appointment Summary Notes (what was accepted and when, replacement context, risk tolerance, insurers compared);
    why: Step 0b is run by the program (Paul's answer 6).
- old line 172: Client email confirmation (Outlook, matched on subject thread), if one exists.
    now: the client's email confirmation (Outlook, matched on the subject thread);
    why: Step 0b is run by the program (Paul's answer 6).
- old line 173: Risk Tolerance questionnaire (WR - New Risk Tolerance - ...
    now: the Risk Tolerance questionnaire (WR - New Risk Tolerance - ..., the "Calculated category";
    why: Step 0b is run by the program (Paul's answer 6).
- old line 173: the client's risk profile ("Calculated category").
    now: bundle, client_name_id, risk_profile, insurers, roa_date, and Risk:
    why: Step 0b is run by the program (Paul's answer 6).
- old line 173: If no Risk Tolerance has been completed, ASK Paul before building.
    now: if none was completed, ASK Paul before building);
    why: Step 0b is run by the program (Paul's answer 6).
- old line 174: Quotes in the transaction folder's Comparative Quotes (FNA, Reduced/Revised, other insurers).
    now: the quotes in Comparative Quotes.
    why: Step 0b is run by the program (Paul's answer 6).
- old line 178: default = the recommended insurer ONLY.
    now: default = the recommended insurer ONLY (1 to 3, never padded).
    why: Step 0b is run by the program (Paul's answer 6).
- old line 178: Add another insurer only if (a) the Overview lists it, (b) the Risk transaction's Comparative Quotes folder genuinely holds a quote from it, or (c) the Follow-Up Notes state it was compared.
    now: Add another only if the Overview lists it, the Comparative Quotes folder genuinely holds a quote from it, or the Follow-Up Notes say it was compared.
    why: Step 0b is run by the program (Paul's answer 6).
- old line 179: from the application's replacement section (replaced policy numbers), matched to cover types using the Overview's "Current personal covers" and the policy schedules.
    now: per cover type, from the application's replacement section matched to cover types using the Overview and the policy schedules.
    why: Step 0b is run by the program (Paul's answer 6).
- old line 179: Remember an application holds one replacement section, but the ROA needs it per cover type.
    now: per cover type, from the application's replacement section matched to cover types using the Overview and the policy schedules.
    why: Step 0b is run by the program (Paul's answer 6).
- old line 180: Taken Up = the LATEST accepted quote (Reduced or Revised, whichever is the most recent), per cover type, read from the Summary block (Step 2).
    now: Taken Up = the LATEST accepted quote (Reduced or Revised), per cover type, both read from the top-level "Summary" block ("Value of your cover").
    why: Step 0b is run by the program (Paul's answer 6).
- old line 180: The premium used in the ROA Reference No.
    now: the "Your ROA reference number is X"
    why: Step 0b is run by the program (Paul's answer 6).
- old line 180: and the filename is the figure printed INSIDE the accepted quote document ("Total premium" on the Summary page) — not the quote's filename, the Overview or the application if they differ (Example:
    now: The premium for the reference number and the file name is the "Total premium" printed INSIDE the accepted quote, not the quote's file name, the Overview or the application.
    why: Step 0b is run by the program (Paul's answer 6).
- old line 180: the filename said R1172.79 while the quote document says R1,172.80).
    now: R.attested.append("the document(s) Paul said are not available:
    why: Step 0b is run by the program (Paul's answer 6).
- old line 181: verbal acceptance on the Teams call is sufficient;
    now: verbal acceptance in the Teams meeting is enough:
    why: Step 0b is run by the program (Paul's answer 6).
- old line 181: take the date from the Follow-Up Notes.
    now: the Risk Tolerance questionnaire, confirmed by the Follow-Up Notes.
    why: Step 0b is run by the program (Paul's answer 6).
- old line 181: If a written client reply or recap email exists with a different date, use the written one and mention it.
    now: take the date from the latest Follow-Up Notes, but if a written client reply or recap email has a different date use the written one and tell Paul.
    why: Step 0b is run by the program (Paul's answer 6).
- old line 181: the client's own reply email is still required (see Step 4).
    now: out.append("reply_email.%s is missing (the client's own reply email must be embedded)" % f)
    why: Step 0b is run by the program (Paul's answer 6).
- old line 182: from the application, cross-checked with the quote and the Fact Find Summary.
    now: from the application, cross-checked with the Fact Find Summary and the quote.
    why: Step 0b is run by the program (Paul's answer 6).
- old line 182: The ROA keeps the client's ID in the confirmation line (this skill has always required it).
    now: The ROA keeps the ID in the confirmation line.
    why: Step 0b is run by the program (Paul's answer 6).
- old line 185: if two sources disagree (other than the quote-premium rule and the verbal-acceptance date rule above), STOP and ask Paul, quoting both values and their sources.
    now: if two sources disagree (other than the premium rule and the verbal-acceptance date rule), list it under conflicts:
    why: Step 0b is run by the program (Paul's answer 6).
- old line 187: the ROA template and responses bank bundled in THIS skill (assets/, references/) are ALWAYS the masters.
    now: The template and the reason-text bank in this skill are the masters.
    why: Step 0b is run by the program (Paul's answer 6).
- old line 187: Never use copies sitting in a client's ROA & Bus ROA folder.
    now: Never use copies sitting in a client's ROA & Bus ROA folder, and never build an ROA from scratch or as HTML.
    why: Step 0b is run by the program (Paul's answer 6).
- old line 189: After Paul confirms the table, continue with Step 1's "Documents" check and Step 2 onward.
    now: Every answer and figure comes from the client's own documents or Paul's words, with its source;
    why: Step 0b is run by the program (Paul's answer 6).
- old line 189: Step 1 below lists what must be known;
    now: "Every line must be a green tick.
    why: Step 0b is run by the program (Paul's answer 6).
- old line 189: Step 0b is how to find it.
    now: Showing where it is up to.")
    why: Step 0b is run by the program (Paul's answer 6).
- old line 191: ## Step 1 — Run the setup checklist first
    now: "Enter the setup answers (Step 0b) with their sources;
    why: The setup checklist is the answers file, validated by the program.
- old line 193: Before building anything, confirm all of these are available — answered from the client's file per Step 0b wherever possible (ask Paul only what Step 0b could not answer).
    now: "Builds a Record and Confirmation of Advice (ROA) for Paul Kafentzis (FSP45946) from the ROA Template 2026, taking the answers from the client's file.
    why: The setup checklist is the answers file, validated by the program.
- old line 193: If any are genuinely missing after
    now: if any(r not in failed for r in w.ROUTES[:i]):
    why: The setup checklist is the answers file, validated by the program.
- old line 194: that search, ask the user for them and wait — do not build a partial ROA.
    now: the data assembled for build_roa.py, the reference number and the file name.
    why: The setup checklist is the answers file, validated by the program.
- old line 195: is for a single client only — this is a fixed rule, never ask about
    now: Every ROA is for a single client only:
    why: The setup checklist is the answers file, validated by the program.
- old line 198: use the button-selection tool for any question with a fixed
    now: one line per check in point form, each with a green tick or a red cross, one closing line for what is only attested.
    why: The setup checklist is the answers file, validated by the program.
- old line 199: set of options, rather than asking as open text.
    now: overrides (set_sdt_plain_text(..., strip_databinding=True)), rather than forcing a
    why: The setup checklist is the answers file, validated by the program.
- old line 199: Reserve typed input for things that
    now: matches the insurer and cover type recommended for that need.
    why: The setup checklist is the answers file, validated by the program.
- old line 200: genuinely have no fixed list.
    now: page(s) %s have no readable text.
    why: The setup checklist is the answers file, validated by the program.
- old line 201: bundle (Risk/Retirement/Investment), Personal/Business (Risk only),
    now: one bundle only (Risk, Retirement or Investment), a single client, never Health Care.
    why: The setup checklist is the answers file, validated by the program.
- old line 202: replacement yes/no, taken up/declined (Risk cover types), risk profile
    now: """The paragraph up to its replacement sentence, then the verbatim 'other Risk Cover in force' sentence (Paul's rule).
    why: The setup checklist is the answers file, validated by the program.
- old line 204: Investment's Need Identified choice (Children Education Planning / General
    now: need_identified is Children Education Planning or General Investment Planning.
    why: The setup checklist is the answers file, validated by the program.
- old line 205: Investment Planning), lump sum vs.
    now: Retirement and Investment [Product Provider] [Product Name] - R [amount][ - Lump Sum | p.m.] (examples:
    why: The setup checklist is the answers file, validated by the program.
- old line 205: recurring/monthly (Retirement/Investment only).
    now: raise ValueError("only Retirement and Investment ROAs embed the email")
    why: The setup checklist is the answers file, validated by the program.
- old line 206: insurer(s) considered, product provider and product name
    now: return "%s %s - R %s%s" % (a["product_provider"].strip(), a["product_name"].strip(), format(w.parse_money(a["amount"]), ",.2f"),
    why: The setup checklist is the answers file, validated by the program.
- old line 207: (Retirement/Investment only), ROA date, document uploads, and the specific reason
    now: A Retirement or Investment ROA needs wkhtmltopdf and the program says it is missing:
    why: The setup checklist is the answers file, validated by the program.
- old line 210: *Always ask first (unless Step 0b already answered it):
    now: run.py answers <run> --file answers.json                                      the setup answers (Step 0b), each with its source
    why: The setup checklist is the answers file, validated by the program.
- old line 211: Which bundle is this ROA for — Risk, Retirement, or Investment?
    now: This session cannot build a Retirement or Investment ROA.")
    why: The setup checklist is the answers file, validated by the program.
- old line 212: Personal or Business assurance cover?
    now: rows.insert(1, ("Personal or Business", a["scope"].title(), s.get("scope")))
    why: The setup checklist is the answers file, validated by the program.
- old line 216: Which insurer(s) were considered?
    now: out.append("insurer %s" % x)
    why: The setup checklist is the answers file, validated by the program.
- old line 216: (Even when only one is ultimately recommended,
    now: add(not bad_sec, "Only the %s bundle is completed;
    why: The setup checklist is the answers file, validated by the program.
- old line 217: s9(1)(b) requires documenting what was actually considered — don't assume it's
    now: several dropdowns (2 tabs before Insurers Considered/Recommended Insurer, 1 tab
    why: The setup checklist is the answers file, validated by the program.
- old line 218: only the insurer the quote happens to be from;
    now: The quote is not from BrightRock:
    why: The setup checklist is the answers file, validated by the program.
- old line 218: Step 0b gives the default.)
    now: The last step prints the SHORT AUDIT.
    why: The setup checklist is the answers file, validated by the program.
- old line 219: Is this transaction a replacement of an existing policy, or not?
    now: 'Investment Planning' for a Retirement ROA, 'POLICY REPLACEMENT' for an Investment ROA."""
    why: The setup checklist is the answers file, validated by the program.
- old line 220: *per cover type in the active bundle (e.g.
    now: # A cover type can be in the active bundle but still declined by the client —
    why: The setup checklist is the answers file, validated by the program.
- old line 220: Life Cover, Lump Sum Disability,
    now: That's permanent = Lump Sum Disability;
    why: The setup checklist is the answers file, validated by the program.
- old line 221: Income Protection, Dread) — never as a single blanket answer for the whole
    now: Claude runs these programs as they are and never rewrites them during a run (the two scripts included).
    why: The setup checklist is the answers file, validated by the program.
- old line 222: ROA, since one cover type can be a replacement while another isn't in the same
    now: out.append("at least one cover type must be active in a Risk ROA")
    why: The setup checklist is the answers file, validated by the program.
- old line 224: For each cover type in the active bundle:
    now: # A cover type can be in the active bundle but still declined by the client —
    why: The setup checklist is the answers file, validated by the program.
- old line 224: is the client taking this up, or
    now: A cover type that is NEW while the client's other cover is replaced or stays in force:
    why: The setup checklist is the answers file, validated by the program.
- old line 225: If declining, ask for the specific reason to record in the "Reason
    now: data_tbl = next((el for m, el in tables if reason_at is None or m < reason_at), None)
    why: The setup checklist is the answers file, validated by the program.
- old line 226: this product suits your needs" textbox — there's no generic default sentence for
    now: out.append("the checker has no result yet for '%s'" % g)
    why: The setup checklist is the answers file, validated by the program.
- old line 227: it must be a real, asked-for reason.
    now: Every choice must be a real option;
    why: The setup checklist is the answers file, validated by the program.
- old line 228: ROA date — the date the client gave the go-ahead, not today's date — see the
    now: ("ROA date (the date the client gave the go-ahead)", "%s (%s:
    why: The setup checklist is the answers file, validated by the program.
- old line 229: "ROA date" rule above for how to determine this.
    now: Use when Paul asks for an ROA or Record of Advice."
    why: The setup checklist is the answers file, validated by the program.
- old line 230: FNA Quote, Reduced/Accepted Quote (if it differs from the FNA Quote —
    now: the accepted quote is the FNA quote")
    why: The setup checklist is the answers file, validated by the program.
- old line 232: Fact Find Summary Report (not the raw Fact Find).
    now: against a real delivered ROA), not the raw template look.
    why: The setup checklist is the answers file, validated by the program.
- old line 235: Retirement and Investment ROAs are never "Personal" or "Business" cover — skip that
    now: Retirement and Investment extras (asked, never inferred):
    why: The setup checklist is the answers file, validated by the program.
- old line 236: question entirely for these two bundles (it's Risk-only) and ask these instead:
    now: "Put the whole table it prints in your reply and ask exactly the one question it gives.
    why: The setup checklist is the answers file, validated by the program.
- old line 237: Which insurer(s) were considered?
    now: out.append("insurer %s" % x)
    why: The setup checklist is the answers file, validated by the program.
- old line 238: Which is the Recommended Insurer?
    now: also ask which is the Recommended Insurer, as its own question.
    why: The setup checklist is the answers file, validated by the program.
- old line 238: Asked as its own explicit question, separate
    now: # but it must carry its own explicit reason (no generic "not considered in
    why: The setup checklist is the answers file, validated by the program.
- old line 239: from point 4 — for Risk, the recommended insurer can usually be read off the
    now: LABELS = ("Need Identified", "Recommended Amount", "Taken Up Amount", "Insurers Considered", "Recommended Insurer", "Recommendation for Identified Need")
    why: The setup checklist is the answers file, validated by the program.
- old line 240: Accepted Quote itself, but Retirement/Investment have no Accepted Quote document,
    now: ("accepted_quote", "overview", "risk_tolerance"), "retirement":
    why: The setup checklist is the answers file, validated by the program.
- old line 241: so this must always be asked directly rather than inferred.
    now: f"asked for directly rather than defaulted."
    why: The setup checklist is the answers file, validated by the program.
- old line 242: Who is the product provider and what is the product name?
    now: rows += [("Product provider and name", "%s %s" % (a["product_provider"], a["product_name"]), s.get("product")),
    why: The setup checklist is the answers file, validated by the program.
- old line 243: never inferred from the insurer field alone.
    now: out.append("%s is missing (asked, never inferred from the insurer)" % f)
    why: The setup checklist is the answers file, validated by the program.
- old line 243: Product provider is often but not
    now: A run without a PASS audit is not finished:
    why: The setup checklist is the answers file, validated by the program.
- old line 244: always the same as the recommended insurer;
    now: also ask which is the Recommended Insurer, as its own question.
    why: The setup checklist is the answers file, validated by the program.
- old line 244: product name is the specific plan
    now: field's text directly with "[Provider] - [Product Name]" in the same style as the
    why: The setup checklist is the answers file, validated by the program.
- old line 245: "Retirement Annuity Xtra Max", "Xtra Max Investment Plan").
    now: Old Mutual Retirement Annuity Xtra Max - R 158,192.00 - Lump Sum and ...
    why: The setup checklist is the answers file, validated by the program.
- old line 246: and delivery filename — see Step 5.
    now: The program checks the proof and only then shows the next step.
    why: The setup checklist is the answers file, validated by the program.
- old line 247: Is the amount a lump sum or a recurring/monthly amount?
    now: ("Amount", "%s, %s" % (a["amount"], "lump sum" if a["frequency"] == "lump_sum" else "recurring (monthly)"), s.get("amount")),
    why: The setup checklist is the answers file, validated by the program.
- old line 248: directly rather than assuming — Retirement/Investment transactions can be either
    now: a Retirement or Investment ROA cannot be built here;
    why: The setup checklist is the answers file, validated by the program.
- old line 249: a Section 14 lump-sum transfer vs.
    now: if a.get("frequency") not in ("lump_sum", "monthly"):
    why: The setup checklist is the answers file, validated by the program.
- old line 250: determines whether the reference number ends in "- Lump Sum" or "p.m." — see
    now: add("RAR reference number:" not in full, "The RAR reference number field is gone")
    why: The setup checklist is the answers file, validated by the program.
- old line 252: Is this a replacement of an existing policy — asked once, since only one need
    now: 'Investment Planning' for a Retirement ROA, 'POLICY REPLACEMENT' for an Investment ROA."""
    why: The setup checklist is the answers file, validated by the program.
- old line 253: type (Retirement or Investment) is ever active in this bundle, unlike Risk where
    now: one bundle only (Risk, Retirement or Investment), a single client, never Health Care.
    why: The setup checklist is the answers file, validated by the program.
- old line 254: it's established per cover type.
    now: replacement must be true or false, per cover type" % tag)
    why: The setup checklist is the answers file, validated by the program.
- old line 255: When the client has other Risk Cover in force that is NOT being replaced by
    now: When the client has other Risk Cover in force that this transaction does NOT replace, set other_risk_cover_in_force true:
    why: The setup checklist is the answers file, validated by the program.
- old line 256: this transaction, the reason text must state, verbatim:
    now: The template and the reason-text bank in this skill are the masters.
    why: The setup checklist is the answers file, validated by the program.
- old line 257: has other Risk Cover in force, this transaction does not constitute a
    now: OTHER_COVER_SENTENCE = "Although the client has other Risk Cover in force, this transaction does not constitute a replacement of that cover."
    why: The setup checklist is the answers file, validated by the program.
- old line 259: Known open item — verify before relying on it:
    now: # KNOWN RECURRING BUG (must be re-verified before every Retirement build):
    why: The setup checklist is the answers file, validated by the program.
- old line 260: times been implemented in build_roa.py/roa_data_schema.md as a single
    now: the data assembled for build_roa.py, the reference number and the file name.
    why: The setup checklist is the answers file, validated by the program.
- old line 261: document-level flag rather than a genuinely independent value per cover type,
    now: # both rows entirely rather than leaving them blank or "N/A"
    why: The setup checklist is the answers file, validated by the program.
- old line 262: even though point 5 above requires it per cover type for Risk
    now: replacement must be true or false, per cover type" % tag)
    why: The setup checklist is the answers file, validated by the program.
- old line 263: Before building a Risk ROA where replacement status actually differs
    now: before 'Investment Planning' for a Retirement ROA, before 'POLICY REPLACEMENT' for an Investment ROA.
    why: The setup checklist is the answers file, validated by the program.
- old line 264: across cover types, confirm the data schema and script currently carry an
    now: You never edit a script, the data or the .docx."
    why: The setup checklist is the answers file, validated by the program.
- old line 265: independent replacement flag per cover type — if they don't, flag this to Paul
    now: replacement must be true or false, per cover type" % tag)
    why: The setup checklist is the answers file, validated by the program.
- old line 266: rather than silently building a document where one cover type's replacement
    now: Policy Replacement wording is replace when ANY cover type is a replacement, not replace otherwise.
    why: The setup checklist is the answers file, validated by the program.
- old line 267: wording leaks into another's.
    now: bad.append("the client's own acceptance wording is not in the page")
    why: The setup checklist is the answers file, validated by the program.
- old line 267: (The per-section reason_text is independent;
    now: Minimum 1 of the 3 slots must be filled per section that is
    why: The setup checklist is the answers file, validated by the program.
- old line 268: document-level policy_replacement flag drives only the "replace / not replace"
    now: set_sdt_plain_text(pr_sdt, 'replace' if data.get('policy_replacement') else 'not replace')
    why: The setup checklist is the answers file, validated by the program.
- old line 269: wording in the Policy Replacement section — set it true when ANY cover type is a
    now: Policy Replacement wording is replace when ANY cover type is a replacement, not replace otherwise.
    why: The setup checklist is the answers file, validated by the program.
- old line 271: is the Need Identified "Children Education Planning" or
    now: need_identified is Children Education Planning or General Investment Planning.
    why: The setup checklist is the answers file, validated by the program.
- old line 272: (Retirement's Need Identified has no equivalent
    now: if b == "retirement" and a.get("need_identified"):
    why: The setup checklist is the answers file, validated by the program.
- old line 273: choice — it's always fixed, see Step 3.)
    now: # is always folded into Lump Sum Disability instead (see INCOME_AFTER_24_FIXED).
    why: The setup checklist is the answers file, validated by the program.
- old line 274: ROA date — the date the client gave the go-ahead, not today's date — see the
    now: ("ROA date (the date the client gave the go-ahead)", "%s (%s:
    why: The setup checklist is the answers file, validated by the program.
- old line 275: "ROA date" rule above for how to determine this.
    now: Use when Paul asks for an ROA or Record of Advice."
    why: The setup checklist is the answers file, validated by the program.
- old line 276: both the Email Proposal PDF (what was sent to the client) and the
    now: proposal_email (what was sent to the client), client_reply_email (the client's own reply confirming the go-ahead:
    why: The setup checklist is the answers file, validated by the program.
- old line 277: client's own reply email confirming go-ahead on it — these are two different
    now: The document embedded in the ROA must be, or include, the client's own reply email confirming the go-ahead, with the original proposal quoted beneath it.
    why: The setup checklist is the answers file, validated by the program.
- old line 278: documents and the ROA needs both (see the "Non-negotiable" rule right below and
    now: a different document, and the ROA needs both), fact_find_summary.
    why: The setup checklist is the answers file, validated by the program.
- old line 279: Step 4 for what gets embedded and why) — and the Fact Find Summary Report
    now: from the application, cross-checked with the Fact Find Summary and the quote.
    why: The setup checklist is the answers file, validated by the program.
- old line 280: (still needed for client name and ID, exactly as with Risk).
    now: # 8 client name and ID line
    why: The setup checklist is the answers file, validated by the program.
- old line 280: There is no FNA Quote
    now: the accepted quote is the FNA quote")
    why: The setup checklist is the answers file, validated by the program.
- old line 281: or Accepted Quote for these two bundles — only Risk uses those — but the Fact
    now: There is no FNA quote or accepted quote for these bundles.
    why: The setup checklist is the answers file, validated by the program.
- old line 282: Find Summary Report is required for every bundle, since client name/ID always
    now: if not any(e.name("x", a.get("client_name")) is None for e in ident):
    why: The setup checklist is the answers file, validated by the program.
- old line 283: comes from it regardless of which bundle the ROA is for.
    now: A Retirement or Investment ROA needs wkhtmltopdf and the program says it is missing:
    why: The setup checklist is the answers file, validated by the program.
- old line 285: finding the original Email Proposal is not enough — you must also
    now: finding the original proposal is not enough.
    why: The setup checklist is the answers file, validated by the program.
- old line 286: find the specific email where the client themself replied to give the go-ahead on
    now: it is the date the client gave the go-ahead" % a["roa_date"])
    why: The setup checklist is the answers file, validated by the program.
- old line 287: that proposal (see the "ROA date" rule above, which already requires this same email
    now: R.attested += ["the advice itself, the ROA date's source and that this is the right transaction folder (judgement, recorded with sources)",
    why: The setup checklist is the answers file, validated by the program.
- old line 288: to source the ROA date).
    now: print("Name to use in the client's ROA & Bus ROA folder:
    why: The setup checklist is the answers file, validated by the program.
- old line 288: The document embedded in the ROA must be (or include) the
    now: The document embedded in the ROA must be, or include, the client's own reply email confirming the go-ahead, with the original proposal quoted beneath it.
    why: The setup checklist is the answers file, validated by the program.
- old line 289: client's own reply, not just the proposal it responds to.
    now: it opens on the client's own reply, then the quoted proposal.")
    why: The setup checklist is the answers file, validated by the program.
- old line 289: In practice the client's
    now: print("Name to use in the client's ROA & Bus ROA folder:
    why: The setup checklist is the answers file, validated by the program.
- old line 290: reply email usually already quotes the full original proposal beneath it (a normal
    now: the client's own reply email with the proposal quoted beneath (one HTML page)",
    why: The setup checklist is the answers file, validated by the program.
- old line 291: reply-in-thread), so embedding the reply email as it actually appears in Outlook
    now: """Reads a client document's text (PDF or HTML/text), page by page, and checks that what the chat entered really appears in it.
    why: The setup checklist is the answers file, validated by the program.
- old line 292: (header block + the client's own acceptance wording + the quoted proposal beneath)
    now: "the page opens on the client's own reply with their acceptance wording, then the quoted proposal (or this is a Risk ROA)"
    why: The setup checklist is the answers file, validated by the program.
- old line 293: satisfies both needs in one document — see Step 4 for exactly how to build this.
    now: print("\nSAY THIS TO PAUL FIRST, before anything else in your reply, in exactly these words:\n    %s.\n" % w.version_line())
    why: The setup checklist is the answers file, validated by the program.
- old line 294: not embed a standalone proposal-only HTML/PDF that never shows the client's own words
    now: An embed that opens on the adviser's proposal, with the client's acceptance nowhere in the document, is an incomplete ROA and must be rebuilt.
    why: The setup checklist is the answers file, validated by the program.
- old line 295: wr-roa-builder-changelog.md (2026-08-27 entry).
    now: WR ROA Builder — construction script.
    why: The setup checklist is the answers file, validated by the program.
- old line 297: *No longer asked — derived automatically, do not ask these:
    now: if s["status"] != "DO NOT REVIEW" or has_tbl:
    why: The setup checklist is the answers file, validated by the program.
- old line 298: Whether a need was taken up or declined can usually be seen directly by comparing
    now: # A cover type can be in the active bundle but still declined by the client —
    why: The setup checklist is the answers file, validated by the program.
- old line 299: the FNA Quote to the Reduced/Accepted Quote (present with an amount = taken up;
    now: accepted_quote (the latest Reduced, Revised or accepted quote;
    why: The setup checklist is the answers file, validated by the program.
- old line 300: absent or zero = a candidate for the declined question above) — but the explicit
    now: # A cover type can be in the active bundle but still declined by the client —
    why: The setup checklist is the answers file, validated by the program.
- old line 301: decline reason still must be asked per point 6.
    now: return (c.get("declined_reason") or "").strip(), "asked", ""
    why: The setup checklist is the answers file, validated by the program.
- old line 302: The FNA scenario (accepted in full vs.
    now: "If the client accepted the FNA in full:
    why: The setup checklist is the answers file, validated by the program.
- old line 302: reduced) is a straightforward comparison
    now: A ROA is a compliance document:
    why: The setup checklist is the answers file, validated by the program.
- old line 303: between the FNA Quote and the Accepted Quote, per cover type — there is always an
    now: There is no FNA quote or accepted quote for these bundles.
    why: The setup checklist is the answers file, validated by the program.
- old line 304: FNA and always an Accepted Quote, so no separate "no FNA" question is needed.
    now: the accepted quote is the FNA quote")
    why: The setup checklist is the answers file, validated by the program.
- old line 305: RAR reference number — removed as a question entirely.
    now: # --- ROA Reference Number (appears at top;
    why: The setup checklist is the answers file, validated by the program.
- old line 306: number on a RAR, so this field is deleted from the delivered document (see Step 3).
    now: A figure that is not in the text cannot have come from the document, so it is a red cross.
    why: The setup checklist is the answers file, validated by the program.
- old line 308: *Status dropdown defaults, driven by point 6 above:
    now: # Status dropdown lives in heading_p
    why: The setup checklist is the answers file, validated by the program.
- old line 309: Every considered cover type in the active bundle defaults to IMPORTANT...
    now: # A cover type can be in the active bundle but still declined by the client —
    why: The setup checklist is the answers file, validated by the program.
- old line 310: ...unless the client declined it, in which case Status = DO NOT REVIEW,
    now: # treat it the same as an inactive section (table removed, "Do not Review"),
    why: The setup checklist is the answers file, validated by the program.
- old line 311: the data table is removed (same treatment as a section outside the active bundle),
    now: # (Investment is the last active section before that block).
    why: The setup checklist is the answers file, validated by the program.
- old line 312: and the reason textbox holds the specific reason given in answer to point 6 — never
    now: It is a bank paragraph word for word, one of the fixed sentences, the specific reason Paul gave for a declined need, or (Retirement and Investment) the pointer line to the client's own reply email.
    why: The setup checklist is the answers file, validated by the program.
- old line 315: FNA-analyzed-but-not-accepted — these are two different states, do not
    now: FNA done but benefit not accepted means taken_up_amount is R 0" % tag)
    why: The setup checklist is the answers file, validated by the program.
- old line 317: true is reserved for a need declined outright, without ever being
    now: taken-up amount R 0, section stays IMPORTANT) | declined (declined outright without an FNA:
    why: The setup checklist is the answers file, validated by the program.
- old line 318: properly analyzed via an FNA.
    now: "If the client accepted the FNA in full:
    why: The setup checklist is the answers file, validated by the program.
- old line 318: Status = "Do not Review", data table removed, reason
    now: if s["status"] != "DO NOT REVIEW" or has_tbl:
    why: The setup checklist is the answers file, validated by the program.
- old line 319: textbox holds the specific reason asked for in point 6 above.
    now: a declined need needs the specific reason Paul gave (asked for, never generic)" % tag)
    why: The setup checklist is the answers file, validated by the program.
- old line 320: FNA-analyzed but the client didn't take up the recommended amount:
    now: FNA done but benefit not accepted means taken_up_amount is R 0" % tag)
    why: The setup checklist is the answers file, validated by the program.
- old line 321: different* state, not a decline.
    now: a different document, and the ROA needs both), fact_find_summary.
    why: The setup checklist is the answers file, validated by the program.
- old line 322: 0, and use the response bank's "FNA DONE / BENEFIT NOT ACCEPTED"
    now: FNA done but benefit not accepted means taken_up_amount is R 0" % tag)
    why: The setup checklist is the answers file, validated by the program.
- old line 323: paragraph (references/WR_Risk_Cover_Responses_24_07_26.docx) as the reason text —
    now: BANK = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "references", "WR_Risk_Cover_Responses_24_07_26.docx")
    why: The setup checklist is the answers file, validated by the program.
- old line 324: the section stays IMPORTANT and its data table stays in the document (showing the
    now: "the tries are logged in order and every required document is registered (or Paul said it does not exist)"
    why: The setup checklist is the answers file, validated by the program.
- old line 325: FNA-recommended amount against a zero taken-up amount), it is not treated like an
    now: Recommended Amount and Taken Up Amount rows are removed entirely (never blank or "N/A").
    why: The setup checklist is the answers file, validated by the program.
- old line 327: build_roa.py enforces this for Disability specifically:
    now: build_roa.py <template.docx> <data.json> <output.docx>")
    why: The setup checklist is the answers file, validated by the program.
- old line 328: with no explicit income_after24.reason_text override supplied, the script raises a
    now: f"reason_text — a declined need must carry an explicit reason, "
    why: The setup checklist is the answers file, validated by the program.
- old line 329: ValueError rather than silently falling back to default text — treat that error as
    now: # both rows entirely rather than leaving them blank or "N/A"
    why: The setup checklist is the answers file, validated by the program.
- old line 330: a signal you're missing a real answer to point 6, not a bug to work around.
    now: against a real delivered ROA), not the raw template look.
    why: The setup checklist is the answers file, validated by the program.
- old line 332: *A note on insurer coverage:
    now: if not (a.get("recommended_insurer") or "").strip():
    why: The setup checklist is the answers file, validated by the program.
- old line 332: the quote-reading method below (Step 2) is currently
    now: The quote-reading method is validated for BrightRock proposals only.
    why: The setup checklist is the answers file, validated by the program.
- old line 333: validated only for BrightRock proposals.
    now: The quote-reading method is validated for BrightRock proposals only.
    why: The setup checklist is the answers file, validated by the program.
- old line 333: If a client's quote comes from a
    now: Never use copies sitting in a client's ROA & Bus ROA folder, and never build an ROA from scratch or as HTML.
    why: The setup checklist is the answers file, validated by the program.
- old line 334: different insurer, flag this before proceeding — the reading method for that
    now: matches the insurer and cover type recommended for that need.
    why: The setup checklist is the answers file, validated by the program.
- old line 335: insurer's document format needs to be worked out and added to this skill, the same
    now: The template and the reason-text bank in this skill are the masters.
    why: The setup checklist is the answers file, validated by the program.
- old line 336: way BrightRock's was, rather than guessed at.
    now: Paul at build time so it's a deliberate choice, not a silent guess — this is a
    why: The setup checklist is the answers file, validated by the program.
- old line 338: *A note on the insurer dropdown's fixed list:
    now: out.append("%s %r must be in CAPITALS (as in the dropdown list, e.g.
    why: The setup checklist is the answers file, validated by the program.
- old line 339: Insurer fields are native dropdowns limited to 9 options (ALTRISK, CAPITAL LEGACY,
    now: fill_insurer_dropdowns(merged_tbl, 0, data.get('insurers_considered', []))
    why: The setup checklist is the answers file, validated by the program.
- old line 340: DISCOVERY, MOMENTUM, LIBERTY, SANLAM, OLD MUTUAL, BRIGHTROCK, STANLIB) — this list has
    now: The fixed list is ALTRISK, CAPITAL LEGACY, DISCOVERY, MOMENTUM, LIBERTY, SANLAM, OLD MUTUAL, BRIGHTROCK, STANLIB.
    why: The setup checklist is the answers file, validated by the program.
- old line 341: never been extended for Investment/Retirement business, where providers like
    now: and for Retirement and Investment the embedded pages (count, place, captions, no spacer, width).
    why: The setup checklist is the answers file, validated by the program.
- old line 342: Ninety-One, Allan Gray, or Coronation are common.
    now: Ninety-One, Allan Gray, Coronation):
    why: The setup checklist is the answers file, validated by the program.
- old line 342: When the recommended insurer isn't
    now: string for 'Recommended Insurer' row.
    why: The setup checklist is the answers file, validated by the program.
- old line 343: on the list, flag it, then write the correct name directly into the field as an
    now: write the ONE html page exactly as before (the page below says how) and register it:
    why: The setup checklist is the answers file, validated by the program.
- old line 344: override (same technique as the Need Identified overrides) rather than forcing the
    now: prob.append("%s Need Identified is not an option of the template" % k)
    why: The setup checklist is the answers file, validated by the program.
- old line 345: nearest dropdown option or leaving it blank.
    now: selection from the fixed list or leaving it blank.
    why: The setup checklist is the answers file, validated by the program.
- old line 345: See dropdown_field_map.md for the
    now: dropdown_field_map.md lists every dropdown option.
    why: The setup checklist is the answers file, validated by the program.
- old line 348: ## Step 2 — Read the source documents;
    now: Overview (the latest "WR Overview" PDF), 2.
    why: Figures are proven to appear in the documents (Paul's answer 4).
- old line 350: Every figure (Recommended Amount, Taken Up Amount, premium) comes from the client's
    now: for lab, v in (("Recommended Amount", s["recommended_amount"]), ("Taken Up Amount", s["taken_up_amount"])):
    why: Figures are proven to appear in the documents (Paul's answer 4).
- old line 351: actual quote documents — never carried over from a previous client, never estimated.
    now: Every figure comes from the client's actual quote or email, never from a previous client, never estimated.
    why: Figures are proven to appear in the documents (Paul's answer 4).
- old line 352: Client name and ID come from the application and Fact Find Summary Report.
    now: from the application, cross-checked with the Fact Find Summary and the quote.
    why: Figures are proven to appear in the documents (Paul's answer 4).
- old line 353: spaces, no dashes (e.g.
    now: 13 digits, no spaces, no dashes.
    why: Figures are proven to appear in the documents (Paul's answer 4).
- old line 354: For Retirement/Investment proposal emails specifically:
    now: and for Retirement and Investment the embedded pages (count, place, captions, no spacer, width).
    why: Figures are proven to appear in the documents (Paul's answer 4).
- old line 354: the figure that goes into the
    now: 3 | Standing rules | The rules that never bend, one line each |
    why: Figures are proven to appear in the documents (Paul's answer 4).
- old line 355: document is always the confirmed accepted amount from the client's own reply,
    now: the amount is the confirmed accepted amount from the client's own reply, never the amount first proposed if the go-ahead was for a different figure;
    why: Figures are proven to appear in the documents (Paul's answer 4).
- old line 356: never the amount originally proposed if the client's go-ahead was for a different
    now: the amount is the confirmed accepted amount from the client's own reply, never the amount first proposed if the go-ahead was for a different figure;
    why: Figures are proven to appear in the documents (Paul's answer 4).
- old line 357: figure — same principle as Risk's FNA-vs-Accepted-Quote distinction, just sourced
    now: fna, acc = need("fna_quote"), ev.get("accepted_quote") or ev.get("fna_quote")
    why: Figures are proven to appear in the documents (Paul's answer 4).
- old line 358: from the email thread instead of two separate quote documents.
    now: # from its sentence, keeping the rest of the s9(1)(d)/Rule 19 explanation intact.
    why: Figures are proven to appear in the documents (Paul's answer 4).
- old line 360: ### Reading a BrightRock quote specifically
    now: The quote-reading method is validated for BrightRock proposals only.
    why: Kept; only BrightRock is accepted.
- old line 361: Always draw cover amounts from the top-level "Summary" block near the start of the
    now: Taken Up = the LATEST accepted quote (Reduced or Revised), per cover type, both read from the top-level "Summary" block ("Value of your cover").
    why: Kept; only BrightRock is accepted.
- old line 362: proposal (the "Value of your cover" table) — not the later "About your cover"
    now: # treat it the same as an inactive section (table removed, "Do not Review"),
    why: Kept; only BrightRock is accepted.
- old line 363: need-by-need breakdowns further into the document, which split totals out by
    now: INCOME_AFTER_24_FIXED = "This need has been worked into the client's Lump Sum Disability Cover Benefit."
    why: Kept; only BrightRock is accepted.
- old line 364: rather than giving one total per cover type.
    now: replacement must be true or false, per cover type" % tag)
    why: Kept; only BrightRock is accepted.
- old line 366: Column/heading mapping in that Summary block:
    now: the heading of the section that immediately follows
    why: Kept; only BrightRock is accepted.
- old line 367: "That's caused by death" → Life Cover (always a lump sum)
    now: That's caused by death = Life Cover;
    why: Kept; only BrightRock is accepted.
- old line 368: "That's permanent" → Lump Sum Disability (always a lump sum)
    now: That's permanent = Lump Sum Disability;
    why: Kept; only BrightRock is accepted.
- old line 370: "Additional expense needs" → Dread Disease / Severe Illness (always a lump sum)
    now: Additional expense needs = Dread Disease.
    why: Kept; only BrightRock is accepted.
- old line 372: The FNA Quote gives the Recommended Amount;
    now: m = fna.number("%s recommended amount" % COVER_NAMES[k], c.get("recommended_amount"))
    why: Kept; only BrightRock is accepted.
- old line 372: the Reduced/Revised/Accepted Quote gives the
    now: accepted_quote (the latest Reduced, Revised or accepted quote;
    why: Kept; only BrightRock is accepted.
- old line 373: *Taken Up Amount — both read from this same Summary block, per cover type,
    now: Taken Up = the LATEST accepted quote (Reduced or Revised), per cover type, both read from the top-level "Summary" block ("Value of your cover").
    why: Kept; only BrightRock is accepted.
- old line 374: The "Total premium (including the policy fee)" on the same Summary page is the premium for the Reference No.
    now: add(rep in full, "The policy replacement wording is '%s' (it follows the cover types)" % ("replace" if data["policy_replacement"] else "not replace"))
    why: Kept; only BrightRock is accepted.
- old line 376: ## Step 3 — Fill in the dropdown fields
    now: as stored in the dropdown (e.g.
    why: Dropdown rules are enforced against the template's own lists.
- old line 378: The template's dropdowns are native Word content controls, not free text — the exact
    now: The template's dropdowns are native Word content controls.
    why: Dropdown rules are enforced against the template's own lists.
- old line 379: option lists (verified from the document XML) are in
    now: # ROA Template — Dropdown Field Map (verified from ROA_Template_2026.docx XML)
    why: Dropdown rules are enforced against the template's own lists.
- old line 380: references/dropdown_field_map.md.
    now: dropdown_field_map.md lists every dropdown option.
    why: Dropdown rules are enforced against the template's own lists.
- old line 380: Read that file before filling any section;
    now: insert_before_heading is the heading of the section that
    why: Dropdown rules are enforced against the template's own lists.
- old line 381: contains the full 81-item product list and every field's valid options.
    now: confirm from the tool's result that the full path is in written and rejected is empty.
    why: Dropdown rules are enforced against the template's own lists.
- old line 384: hardcoded to "Retirement Planning" (optionally
    now: Need Identified is hardcoded to "Retirement
    why: Dropdown rules are enforced against the template's own lists.
- old line 385: "Saving for Retirement" as an alternate wording) — not a dropdown selection.
    now: Planning" (optionally "Saving for Retirement" as an alternate wording), the same
    why: Dropdown rules are enforced against the template's own lists.
- old line 386: of the three real dropdown options (preserve / Retirement Annuity / retirement)
    now: preserve / Retirement Annuity / retirement — none of these three
    why: Dropdown rules are enforced against the template's own lists.
- old line 388: hardcoded to one of two fixed values, asked per
    now: fixed values, asked per client:
    why: Dropdown rules are enforced against the template's own lists.
- old line 390: of the two real dropdown options (child's education / defined need) is used.
    now: child's education / defined need — neither of these dropdown
    why: Dropdown rules are enforced against the template's own lists.
- old line 391: Retirement and Investment → Recommended Amount / Taken Up Amount:
    now: for f in ("recommended_amount", "taken_up_amount"):
    why: Dropdown rules are enforced against the template's own lists.
- old line 392: for these two sections when active — both rows are removed from the table
    now: sections in the active bundle (see build_section for shape)
    why: Dropdown rules are enforced against the template's own lists.
- old line 393: entirely (never left blank or "N/A").
    now: # both rows entirely rather than leaving them blank or "N/A"
    why: Dropdown rules are enforced against the template's own lists.
- old line 394: Recommended Insurer, and Recommendation for Identified Need all remain.
    now: Need Identified, Insurers Considered, Recommended Insurer and Recommendation for Identified Need remain.
    why: Dropdown rules are enforced against the template's own lists.
- old line 395: always "Life Cover" — this is a hardcoded override,
    now: override technique as Death → "Life Cover" — this is a direct text override, not a
    why: Dropdown rules are enforced against the template's own lists.
- old line 396: not a dropdown selection, since "Life Cover" isn't even one of the four listed
    now: template gap (the dropdown list has never been extended past the original 9), not a
    why: Dropdown rules are enforced against the template's own lists.
- old line 398: Lump Sum Disability and Income Protection (1st 24 months) → Need Identified:
    now: Lump Sum Disability and Income Protection (1st 24 months) must be given:
    why: Dropdown rules are enforced against the template's own lists.
- old line 398: NOT hardcoded by the script — you must pass need_identified in the data for both, or the field renders blank.
    now: need_identified must be one of %s (it renders BLANK otherwise)" % (tag, ";
    why: Dropdown rules are enforced against the template's own lists.
- old line 398: "Sickness and/or Income Protection Cover" / "Lump Sum Disability Cover" / "Retrenchment Cover".
    now: Sickness and/or Income Protection Cover / Lump Sum
    why: Dropdown rules are enforced against the template's own lists.
- old line 398: Use "Lump Sum Disability Cover" for Lump Sum Disability and "Sickness and/or Income Protection Cover" for Income Protection (1st 24 months).
    now: "Lump Sum Disability Cover" and "Sickness and/or Income Protection Cover".
    why: Dropdown rules are enforced against the template's own lists.
- old line 399: always "Comprehensive Severe Illness" (the only real
    now: Discovery - Comprehensive Plus Severe Illness Benefit
    why: Dropdown rules are enforced against the template's own lists.
- old line 401: minimum 1 of the 3 slots, up to all 3, matching what was
    now: Minimum 1 of the 3 slots must be filled per section that is
    why: Dropdown rules are enforced against the template's own lists.
- old line 402: genuinely compared for that client — never pad with unused slots, and leave unused
    now: Every answer and figure comes from the client's own documents or Paul's words, with its source;
    why: Dropdown rules are enforced against the template's own lists.
- old line 403: slots visually blank (not "Choose an item.").
    now: unused slots stay visually blank.
    why: Dropdown rules are enforced against the template's own lists.
- old line 405: Insurer/provider override text (Ninety-One, Allan Gray, Coronation, etc.):
    now: Ninety-One, Allan Gray, Coronation):
    why: Dropdown rules are enforced against the template's own lists.
- old line 406: the insurer name in ALL CAPS to match the style of the fixed dropdown list
    now: "NINETY-ONE", all caps to match the existing list's style).
    why: Dropdown rules are enforced against the template's own lists.
- old line 407: NINETY-ONE, not Ninety-One) when using the set_sdt_plain_text override.
    now: set_sdt_plain_text(sdt, val)
    why: Dropdown rules are enforced against the template's own lists.
- old line 408: always PAUL KAFENTZIS, never Gareth Saffy.
    now: PAUL KAFENTZIS, never Gareth Saffy, regardless of client.
    why: Dropdown rules are enforced against the template's own lists.
- old line 409: never produced at all — see "Document construction" below;
    now: Never overwrite a compliance document silently:
    why: Dropdown rules are enforced against the template's own lists.
- old line 410: entire section is deleted from every ROA, not just left inactive.
    now: # (heading + reason table + surrounding spacer paragraphs), not just left inactive ---
    why: Dropdown rules are enforced against the template's own lists.
- old line 411: Retirement → Recommendation for Identified Need, when the product is an Old
    now: Recommendation for Identified Need, Old Mutual retirement annuity:
    why: Dropdown rules are enforced against the template's own lists.
- old line 412: type the client's actual product name (e.g.
    now: (No fixed default — source from the client's actual risk questionnaire result, unlike
    why: Dropdown rules are enforced against the template's own lists.
- old line 413: "Old Mutual Retirement Annuity Xtra Max") — a direct text override, not a
    now: Old Mutual Retirement Annuity Xtra Max - R 158,192.00 - Lump Sum and ...
    why: Dropdown rules are enforced against the template's own lists.
- old line 414: selection from the 81-item master product list (the list has no dedicated Old
    now: selection from the fixed list or leaving it blank.
    why: Dropdown rules are enforced against the template's own lists.
- old line 415: Mutual RA entry at all;
    now: # --- ROA Reference Number (appears at top;
    why: Dropdown rules are enforced against the template's own lists.
- old line 415: "Old Mutual - Max Investment" is a poor semantic match
    now: Old Mutual Tax-Free Investment shortcut:
    why: Dropdown rules are enforced against the template's own lists.
- old line 416: and is no longer used for this product).
    now: every Need Identified is filled and valid, no blank or "." insurer or product;
    why: Dropdown rules are enforced against the template's own lists.
- old line 416: Never hardcode a literal "Old Mutual
    now: it's overwhelmingly BrightRock/Old Mutual/Sanlam/etc.
    why: Dropdown rules are enforced against the template's own lists.
- old line 417: Optimal Retirement Annuity" string here — that was tried and explicitly
    now: Old Mutual Retirement Annuity Xtra Max - R 158,192.00 - Lump Sum and ...
    why: Dropdown rules are enforced against the template's own lists.
- old line 418: this field must reflect the specific product actually sold.
    now: Select the specific product that
    why: Dropdown rules are enforced against the template's own lists.
- old line 419: override technique as Death/Dread/Retirement Need Identified above.
    now: override technique as Death → "Life Cover" — this is a direct text override, not a
    why: Dropdown rules are enforced against the template's own lists.
- old line 420: regression — re-verify this before every Old Mutual RA build;
    now: # KNOWN RECURRING BUG (must be re-verified before every Retirement build):
    why: Dropdown rules are enforced against the template's own lists.
- old line 421: wr-roa-builder-changelog.md (2026-08-10 entry).
    now: WR ROA Builder — construction script.
    why: Dropdown rules are enforced against the template's own lists.
- old line 423: ## Document construction — build the actual .docx, don't hand-edit text
    now: never hand-patch the .docx.
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 425: *Do not treat this as a fill-in-the-blanks text exercise.
    now: scenario %r is not a heading in the response bank for this cover (headings:
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 426: structurally different from the raw template — inactive sections have their entire
    now: against a real delivered ROA), not the raw template look.
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 427: data table *removed* (not left with "Choose an item." showing), and Health Care is
    now: Never enter income_after24 (always Do not Review with a fixed sentence) or health care.
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 428: Getting this right requires editing word/document.xml directly,
    now: root = etree.fromstring(z.read("word/document.xml"))
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 429: not just typing over placeholder text.
    now: no "Choose an item." or other placeholder text;
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 431: Use scripts/build_roa.py, which already encodes all of this correctly (validated
    now: "scripts/run.py build (scripts/roa.py assembles the data, scripts/build_roa.py builds, scripts/embedpipe.py + embed_email_images.py embed the email pages for Retirement and Investment)",
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 432: against a real delivered ROA).
    now: against a real delivered ROA), not the raw template look.
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 432: Build a data dict per references/roa_data_schema.md
    now: See references/roa_data_schema.md in the skill for the full data shape.
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 436: python3 scripts/build_roa.py assets/ROA_Template_2026.docx data.json output.docx
    now: build_roa.py <template.docx> <data.json> <output.docx>")
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 439: What the script does automatically, so you don't have to reason about XML each time:
    now: The program shows the right page at each step, so you do not work from memory of them.
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 440: Removes the entire data table (Need Identified/Amounts/Insurers/Product) for any
    now: No Need Identified, Insurer, or Product dropdowns exist for this
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 441: section outside the active bundle, leaving only the heading and the reason text.
    now: sections in the active bundle (see build_section for shape)
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 442: Removes the entire data table the same way for any cover type within the
    now: matches the insurer and cover type recommended for that need.
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 443: active bundle that the client declined (declined:
    now: # the active bundle's own section in document order.
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 443: true in that section's data) —
    now: # the active bundle's own section in document order.
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 444: Status is set to "Do not Review" and the reason textbox holds the specific reason
    now: add(ia.get("status") == "DO NOT REVIEW" and (ia.get("reason") or [[""]])[0][0] == br.INCOME_AFTER_24_FIXED,
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 445: given for declining, which must be supplied explicitly (the script raises an error
    now: w.die('--client must be the first name and surname, for example --client "Pat Samplecase"')
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 446: if a declined section has no reason_text — there is no generic default for this).
    now: every other section (and any declined need) shows only its heading and reason text" % b if not bad_sec else "Section problem:
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 447: Deletes the Health Care section from the document entirely, every time.
    now: add("health care" not in full.lower(), "Health Care does not appear anywhere in the document")
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 448: Deletes the RAR reference number field from its sentence entirely, every time —
    now: the RAR reference number is gone;
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 449: there is no reference number on a RAR, so the rest of the s9(1)(d)/Rule 19
    now: # from its sentence, keeping the rest of the s9(1)(d)/Rule 19 explanation intact.
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 450: sentence is kept but the "RAR reference number:
    now: Strip the trailing "RAR reference number:
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 451: than filled with N/A.
    now: # both rows entirely rather than leaving them blank or "N/A"
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 452: Forces Income Protector Planning After 24 Months to "Do not Review" with the fixed
    now: "Income Protector Planning After 24 Months is Do not Review with the fixed sentence")
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 453: BR sentence, regardless of what's passed in for other risk-bundle sections.
    now: sections in the active bundle (see build_section for shape)
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 454: Applies the Death → "Life Cover" and Dread → "Comprehensive Severe Illness"
    now: need_override='Comprehensive Severe Illness'),
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 456: Collapses dual lump-sum/monthly amount fields to a single clean value (e.g.
    now: # whether its amount fields are single (lump sum only) or dual (lump/monthly),
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 457: "R 37,000 monthly") instead of leaving unused scaffolding text in place.
    now: never leave the unused lump/monthly scaffolding in place."""
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 458: Retirement section's merged table row order:
    now: if section.get('merged_table'):
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 459: places the Reason row *before* the Insurers Considered/Recommended
    now: several dropdowns (2 tabs before Insurers Considered/Recommended Insurer, 1 tab
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 460: Insurer/Recommendation rows (row0=reason, rows1-3=insurer fields) — the wrong
    now: # in this merged table (row0=reason, rows1-3=insurers/recinsurer/recommendation).
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 461: order for filling s9(1)(b)/(c) content sensibly.
    now: for kk in set(c) - COVER_KEYS:
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 461: build_roa.py reorders the
    now: build_roa.py <template.docx> <data.json> <output.docx>")
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 462: <w:tr> elements (moves the reason row to the end) before filling, so the
    now: # Move the reason row to the end so the fill order matches s9(1)(c)/(b) intent:
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 463: final document reads Need Identified → Insurers Considered → Recommended
    now: "The Retirement section reads Need Identified, Insurers Considered, Recommended Insurer, Recommendation, then Reason")
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 464: Insurer → Recommendation for Identified Need → Reason.
    now: Recommendation for Identified Need — same gap applies:
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 465: reorder step has been found completely missing more than once.
    now: Paul has not been shown exactly these answers.
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 466: reorder code is present in build_section() before every Retirement build;
    now: # KNOWN RECURRING BUG (must be re-verified before every Retirement build):
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 467: wr-roa-builder-changelog.md (2026-08-10 entry).
    now: WR ROA Builder — construction script.
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 468: Sets the next-meeting date to ROA date + 12 months.
    now: # --- Next meeting date = ROA date + 12 months ---
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 469: Formats the client ID confirmation line as "I, [Name], (ID:
    now: The ROA keeps the ID in the confirmation line.
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 470: hereby confirm" with clean single commas, and strips the literal "(Name)" label.
    now: Send the file with SendUserFile, then device_commit_files with its file_uuid and the exact file name;
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 471: Strips the unreliable <w:dataBinding> on the Client Name and ROA Reference
    now: print("Name to use in the client's ROA & Bus ROA folder:
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 472: Number controls before setting their text directly.
    now: rest = t.text.lstrip()  # drop leading run of spaces before "(ID)"
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 473: Every set_sdt_plain_text / override call strips both the <w:dataBinding>
    now: def set_sdt_plain_text(sdt, new_text, strip_databinding=False):
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 474: element and the PlaceholderText character style reference
    now: # Strip the "PlaceholderText" character style (grey #808080) — real
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 475: (<w:rStyle w:val="PlaceholderText">) on the affected run — stripping only the
    now: if rstyle is not None and rstyle.get(_q('val')) == 'PlaceholderText':
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 476: data binding and leaving the style reference in place is a known way this has gone
    now: add("RAR reference number:" not in full, "The RAR reference number field is gone")
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 477: the field fills correctly but renders in placeholder grey instead of
    now: no filled field in placeholder grey;
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 478: black, which is easy to miss on a quick read and only shows up when zoomed in or
    now: one line per check in point form, each with a green tick or a red cross, one closing line for what is only attested.
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 479: Check filled fields aren't grey during the visual audit.
    now: Then look at EVERY page image it saves (filled fields black not grey;
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 480: Every paragraph property block (pPr) built or edited by the script follows the
    now: """The data dict for build_roa.build_roa, built by the program from the answers."""
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 481: Word schema's required child element order (CT_PPrBase) — spacing before jc,
    now: Verify every required document is present and current before going on:
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 482: rPr always last — rather than whatever order feels natural to write;
    now: # both rows entirely rather than leaving them blank or "N/A"
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 483: silently reject or reflow a pPr with elements out of schema order.
    now: that a figure sits in the right place or column (attested), and anything on a page with no text (a scanned page):
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 484: Strips leading/trailing <w:tab/> runs and stray whitespace the template bakes in
    now: strip a purely-whitespace leading run — the template has these baked in before
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 486: before most Recommendation for Identified Need fields) — these silently push text
    now: or a stray space before most Recommendation for Identified Need fields), which
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 487: away from the left edge and are not fixed by setting paragraph alignment alone.
    now: pushes the filled-in text away from the left edge using default tab stops.
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 488: Forces explicit left alignment on every field it fills in, and adds cell padding
    now: """Force explicit left alignment on a paragraph, overriding any inherited
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 489: to reason textboxes so text doesn't touch the borders.
    now: # Move the reason row to the end so the fill order matches s9(1)(c)/(b) intent:
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 490: Chains keepNext/keepLines through the entire accept/decline decision block (the
    now: 'pStyle', 'keepNext', 'keepLines', 'pageBreakBefore', 'framePr', 'widowControl',
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 491: "I hereby accept..." / "My final decision..." / "I decline...
    now: # --- The entire client decision block — "I hereby accept...", "My final
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 492: the blank input lines beneath) so a page break can never split it.
    now: # SIGNATORIES" so no page break can fall inside this block.
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 493: Trims the template's ~11 trailing blank paragraphs after the signature line down
    now: # template ships with ~11 blank paragraphs after the signature line, which is
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 494: to 2, removing the extra blank final page they otherwise cause.
    now: # enough to push out an extra, entirely blank final page.
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 496: After building, always validate and visually check before delivering — see the
    now: Death is always "Life Cover" and Dread always "Comprehensive Severe Illness" (hard-coded by the script);
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 497: commands in references/roa_data_schema.md.
    now: See references/roa_data_schema.md in the skill for the full data shape.
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 497: Don't skip the visual render;
    now: tmpd = tempfile.mkdtemp(prefix="roa_render_")
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 498: correctness doesn't guarantee the document isn't structurally broken.
    now: out.append("the document %r is not registered" % role)
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 500: If a client's situation needs something the script doesn't yet handle, extend the
    now: A situation they do not handle is a change for Claude Code, not for the chat.
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 501: script rather than hand-editing XML ad hoc for that one ROA — and note the change in
    now: One line saying where the ROA was saved (the file name and the folder), or that it was NOT saved and why.
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 502: this file so it's permanent.
    now: That's permanent = Lump Sum Disability;
    why: The script stays the base, fixed and unchangeable during a run (Paul's answer 2).
- old line 504: ## Step 4 — Reason text for the "Reason this product suits your needs (required — s9(1)(c))" box
    now: reason_at = next((m for m, el in enumerate(seg) if _local(el) == "p" and "Reason this product suits" in _txt(el)), None)
    why: The reason text is picked by the program from the bank word for word (Paul's answer 3).
- old line 506: This box's content differs by bundle.
    now: template changes, re-run this extraction rather than editing the option lists by hand
    why: The reason text is picked by the program from the bank word for word (Paul's answer 3).
- old line 509: For Life, Lump Sum Disability, Dread Disease, and Income Protection (1st 24
    now: Lump Sum Disability and Income Protection (1st 24 months) must be given:
    why: The program picks the paragraph (Paul's answer 3).
- old line 510: months), select the matching scenario paragraph from
    now: """Set the plain paragraph text of a single-cell reason-box table row, with
    why: The program picks the paragraph (Paul's answer 3).
- old line 511: references/WR_Risk_Cover_Responses_24_07_26.docx, evaluated independently per
    now: BANK = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "references", "WR_Risk_Cover_Responses_24_07_26.docx")
    why: The program picks the paragraph (Paul's answer 3).
- old line 512: cover type (FNA status × Replacement status — see that document's full scenario
    now: per cover type, from the application's replacement section matched to cover types using the Overview and the policy schedules.
    why: The program picks the paragraph (Paul's answer 3).
- old line 513: Life, Disability, Dread, Income Protection each have their own
    now: Lump Sum Disability and Income Protection (1st 24 months) must be given:
    why: The program picks the paragraph (Paul's answer 3).
- old line 514: Copy the paragraph in, substituting only client-specific details (needs
    now: # Find the containing paragraph (may be several levels up if wrapped in
    why: The program picks the paragraph (Paul's answer 3).
- old line 515: considered, pronouns) where the paragraph requires it.
    now: # the dropdown sits in the paragraph right after the RISK PROFILE heading
    why: The program picks the paragraph (Paul's answer 3).
- old line 517: If a client's actual scenario doesn't cleanly match one canned paragraph (e.g.
    now: Every figure comes from the client's actual quote or email, never from a previous client, never estimated.
    why: The program picks the paragraph (Paul's answer 3).
- old line 518: accepted per the FNA in full, but Income Protection reduced to a different amount),
    now: if the client accepted the FNA in full, the FNA quote serves as both:
    why: The program picks the paragraph (Paul's answer 3).
- old line 519: word each cover type's box accurately and independently — use judgement to stay
    now: how to derive each answer (Step 0b), the answers file, and the rules the program applies.
    why: The program picks the paragraph (Paul's answer 3).
- old line 520: factually correct rather than forcing a mismatched paragraph.
    now: f"asked for directly rather than defaulted."
    why: The program picks the paragraph (Paul's answer 3).
- old line 522: *A cover type that is NEW (not replacing anything) while the client's OTHER cover is being replaced or stays in force:
    now: A cover type that is NEW while the client's other cover is replaced or stays in force:
    why: The program picks the paragraph (Paul's answer 3).
- old line 522: the response bank's "NON-REPLACEMENT" paragraphs say "the client has no Risk Cover currently in force", which would be false.
    now: the program ends the paragraph with the verbatim "other Risk Cover in force" sentence.
    why: The program picks the paragraph (Paul's answer 3).
- old line 522: Use the matching FNA paragraph (accepted or reduced) up to the replacement sentence, then end with the verbatim sentence:
    now: """The paragraph up to its replacement sentence, then the verbatim 'other Risk Cover in force' sentence (Paul's rule).
    why: The program picks the paragraph (Paul's answer 3).
- old line 522: "Although the client has other Risk Cover in force, this transaction does not constitute a replacement of that cover." (Example:
    now: OTHER_COVER_SENTENCE = "Although the client has other Risk Cover in force, this transaction does not constitute a replacement of that cover."
    why: The program picks the paragraph (Paul's answer 3).
- old line 522: Life and Lump Sum Disability replaced Instant Life policies;
    now: dict(key='disability', heading='Lump Sum Disability Planning', amount_type='single'),
    why: The program picks the paragraph (Paul's answer 3).
- old line 522: Income Protection and Severe Illness were new.)
    now: # Income Protection only ever covers the first 24 months;
    why: The program picks the paragraph (Paul's answer 3).
- old line 524: Additional fixed rules layered on top of the response bank:
    now: A document cannot be found on any of the three routes:
    why: The program picks the paragraph (Paul's answer 3).
- old line 525: A need exists but the client doesn't want to pursue it:
    now: A need that exists but the client will not pursue:
    why: The program picks the paragraph (Paul's answer 3).
- old line 525: "The client did not want
    now: "The client did not want to consider this need at this time."
    why: The program picks the paragraph (Paul's answer 3).
- old line 526: to consider this need at this time."
    now: "The client did not want to consider this need at this time."
    why: The program picks the paragraph (Paul's answer 3).
- old line 527: Income Protector Planning After 24 Months (BrightRock structural rule — BR's
    now: "Income Protector Planning After 24 Months is Do not Review with the fixed sentence")
    why: The program picks the paragraph (Paul's answer 3).
- old line 529: worked into the Lump Sum Disability benefit instead):
    now: # is always folded into Lump Sum Disability instead (see INCOME_AFTER_24_FIXED).
    why: The program picks the paragraph (Paul's answer 3).
- old line 529: "This need has been worked
    now: print("THIS PAGE HAS NO READABLE TEXT.
    why: The program picks the paragraph (Paul's answer 3).
- old line 530: into the client's Lump Sum Disability Cover Benefit." This applies regardless of
    now: INCOME_AFTER_24_FIXED = "This need has been worked into the client's Lump Sum Disability Cover Benefit."
    why: The program picks the paragraph (Paul's answer 3).
- old line 531: what the client decided on their other covers.
    now: it must open on the client's own reply.
    why: The program picks the paragraph (Paul's answer 3).
- old line 534: No response bank exists for these, and there's no FNA Quote or Accepted Quote — but
    now: There is no FNA quote or accepted quote for these bundles.
    why: Kept as before; now forced and checked.
- old line 535: the Fact Find Summary Report is still required, the same as Risk, for client name
    now: ident = [e for e in (ev.get("application"), ev.get("fact_find_summary")) if e is not None and e.has_text]
    why: Kept as before; now forced and checked.
- old line 536: The substantiation source is the client's own reply email confirming
    now: the embedded email must open on the client's own reply.
    why: Kept as before; now forced and checked.
- old line 537: go-ahead on the proposal — not the outbound proposal email by itself.
    now: PROVIDER_POINTER = ("The client's email reply confirming their go-ahead on this proposal (%s), with the original proposal email quoted in full beneath it, "
    why: Kept as before; now forced and checked.
- old line 539: *Non-negotiable (see Step 1 point 9 above):
    now: one line per check, point form, a green tick or a red cross;
    why: Kept as before; now forced and checked.
- old line 539: the document you embed must be, or
    now: out.append("replacement must be true or false")
    why: Kept as before; now forced and checked.
- old line 540: include, the client's own written acceptance — never a proposal-only document that
    now: "the page opens on the client's own reply with their acceptance wording, then the quoted proposal (or this is a Risk ROA)"
    why: Kept as before; now forced and checked.
- old line 541: never shows the client's own words agreeing to it.
    now: Every answer comes from the client's own documents or from Paul's words and is recorded with its source.
    why: Kept as before; now forced and checked.
- old line 541: In practice the client's reply
    now: it opens on the client's own reply, then the quoted proposal.")
    why: Kept as before; now forced and checked.
- old line 542: almost always quotes the full original proposal beneath it (a normal reply-in-thread),
    now: padding-left:16px), so the reply-versus-quote structure reads like a real email thread.
    why: Kept as before; now forced and checked.
- old line 543: so build one composite "email as it actually appears" document:
    now: build_roa.py and embed_email_images.py are run as they are, never rewritten or patched during a run.
    why: Kept as before; now forced and checked.
- old line 544: A header block for the reply itself — From (the client's own address)/Sent
    now: A header block for the reply itself in the same styled table as the proposal's own header:
    why: Kept as before; now forced and checked.
- old line 545: (the reply's actual sent time)/To/Cc/Subject (usually "Re:
    now: From (the client's own address), Sent (the reply's actual local sent time:
    why: Kept as before; now forced and checked.
- old line 546: — followed by the client's own acceptance wording verbatim (e.g.
    now: bad.append("the client's own acceptance wording is not in the page")
    why: Kept as before; now forced and checked.
- old line 548: Beneath that, the quoted chain exactly as Outlook shows it — an "On [date] at
    now: if the accepted proposal is not saved as a PDF, find it in Outlook (outlook_email_search / read_resource, match on the subject thread:
    why: Kept as before; now forced and checked.
- old line 549: [time], [sender] wrote:" line for each intermediate forward, then the original
    now: ## Per-section fields (repeats for each of the 7 product sections below)
    why: Kept as before; now forced and checked.
- old line 550: proposal's own header block (From/Sent/To/Cc/Subject/Importance) and full body,
    now: bad.append("the page must OPEN with the reply's own header block (From:
    why: Kept as before; now forced and checked.
- old line 551: reusing the same styling as the reply's own header so the whole thing reads as
    now: bad.append("the page must OPEN with the reply's own header block (From:
    why: Kept as before; now forced and checked.
- old line 552: one continuous, real email thread rather than two stitched-together documents.
    now: template changes, re-run this extraction rather than editing the option lists by hand
    why: Kept as before; now forced and checked.
- old line 553: See "Embedding the proposal email images" below for the concrete HTML-composition
    now: """Insert the accepted-proposal email pages (as images) into the Investment
    why: Kept as before; now forced and checked.
- old line 554: method (reuse the already-built proposal HTML as the quoted portion, prepend a
    now: Take the already-built proposal HTML and its <body> inner content as the quoted portion.
    why: Kept as before; now forced and checked.
- old line 555: new reply header + body + "On ...
    now: bad.append("the page must OPEN with the reply's own header block (From:
    why: Kept as before; now forced and checked.
- old line 555: wrote:" divider ahead of it).
    now: it is the date the client gave the go-ahead" % a["roa_date"])
    why: Kept as before; now forced and checked.
- old line 557: *Do not paste the email's text into the reason textbox as a dense wall of prose —
    now: "The email embedding was not done as the skill requires (%s)" % (emb or "not done"))
    why: Kept as before; now forced and checked.
- old line 558: it renders cluttered and is hard to audit against the source.
    now: Your reply to Paul is the saved file's name and folder, the .docx, and that audit, as they are.
    why: Kept as before; now forced and checked.
- old line 559: In the reason textbox itself (the existing bordered table cell), put one short
    now: A header block for the reply itself in the same styled table as the proposal's own header:
    why: Kept as before; now forced and checked.
- old line 560: line naming what's reproduced, e.g.:
    now: existing list entries (e.g.
    why: Kept as before; now forced and checked.
- old line 560: "The client's email reply confirming his
    now: proposal_email (what was sent to the client), client_reply_email (the client's own reply confirming the go-ahead:
    why: Kept as before; now forced and checked.
- old line 561: go-ahead on this proposal ([date]), with the original proposal email quoted in
    now: PROVIDER_POINTER = ("The client's email reply confirming their go-ahead on this proposal (%s), with the original proposal email quoted in full beneath it, "
    why: Kept as before; now forced and checked.
- old line 562: full beneath it, is reproduced on the following pages." The pointer line must name
    now: "is reproduced on the following pages.")
    why: Kept as before; now forced and checked.
- old line 563: the *reply* as what's being shown, not just the proposal it responds to — see
    now: A header block for the reply itself in the same styled table as the proposal's own header:
    why: Kept as before; now forced and checked.
- old line 564: wr-roa-builder-changelog.md (2026-08-27 entry) for why this wording matters.
    now: WR ROA Builder — construction script.
    why: Kept as before; now forced and checked.
- old line 565: Convert the composite (reply + quoted proposal) HTML's pages to images
    now: the reply email + quoted proposal as one HTML page, as before
    why: Kept as before; now forced and checked.
- old line 566: (pdftoppm -jpeg -r 150) and
    now: r = subprocess.run(["pdftoppm", "-jpeg", "-r", "150", pdf, os.path.join(images, "page")], capture_output=True, text=True)
    why: Kept as before; now forced and checked.
- old line 567: insert them as standalone paragraphs immediately after the section's data table
    now: bordered picture paragraphs after the section's data/reason table, never
    why: Kept as before; now forced and checked.
- old line 568: after the Insurers Considered / Recommended Insurer / Recommendation
    now: a["insurers_considered"], "recommended_insurer":
    why: Kept as before; now forced and checked.
- old line 569: for Identified Need rows) — not inside any table cell.
    now: Recommendation for Identified Need — same gap applies:
    why: Kept as before; now forced and checked.
- old line 569: Give each image its own
    now: If none fits, give custom_reason in Paul's own wording" %
    why: Kept as before; now forced and checked.
- old line 570: paragraph with a picture-level border (<a:ln> on the pic:spPr, not a table or
    now: Reason text is a bank paragraph word for word, a fixed sentence, the reason Paul gave, or the pointer line;
    why: Kept as before; now forced and checked.
- old line 571: paragraph border) and a small italic caption ("page X of Y").
    now: """Set the plain paragraph text of a single-cell reason-box table row, with
    why: Kept as before; now forced and checked.
- old line 572: ≤ 5,000,000 EMU wide (≈5.5in) so a full-page screenshot plus its caption
    now: <=5,000,000 EMU wide.
    why: Kept as before; now forced and checked.
- old line 573: comfortably fits within one page's usable height.
    now: If none fits, give custom_reason in Paul's own wording" %
    why: Kept as before; now forced and checked.
- old line 574: Why not inside the table cell:
    now: """Entries that are not an option of the template's dropdowns:
    why: Kept as before; now forced and checked.
- old line 574: a table row containing several full-page-tall
    now: that a figure sits in the right place or column (attested), and anything on a page with no text (a scanned page):
    why: Kept as before; now forced and checked.
- old line 575: images will span multiple pages, and when a table row splits across a page break
    now: *You look at the page images the program saves for what a program cannot see:
    why: Kept as before; now forced and checked.
- old line 576: its cell borders can render incorrectly — bleeding into or striking through the
    now: never shrink the image), no picture border bleeding into a page footer.
    why: Kept as before; now forced and checked.
- old line 577: Standalone paragraphs don't have this failure mode:
    now: Recognise this failure at once:
    why: Kept as before; now forced and checked.
- old line 578: that doesn't fit moves as a whole to the next page, so the border always wraps
    now: never shrink the image), no picture border bleeding into a page footer.
    why: Kept as before; now forced and checked.
- old line 579: just that one image cleanly.
    now: 3 | Standing rules | The rules that never bend, one line each |
    why: Kept as before; now forced and checked.
- old line 581: Retirement and Investment are never both active in the same ROA — whichever one
    now: A Retirement or Investment ROA needs wkhtmltopdf and the program says it is missing:
    why: Kept as before; now forced and checked.
- old line 582: isn't the active bundle is treated exactly like any other out-of-bundle section (see
    now: sections in the active bundle (see build_section for shape)
    why: Kept as before; now forced and checked.
- old line 583: Status = "Do not Review", data table removed, reason text =
    now: if s["status"] != "DO NOT REVIEW" or has_tbl:
    why: Kept as before; now forced and checked.
- old line 584: "This need was not considered in this Review meeting." No special-case wording is
    now: NOT_CONSIDERED = "This need was not considered in this Review meeting."
    why: Kept as before; now forced and checked.
- old line 585: needed for this — it's the same standard out-of-bundle treatment every section gets.
    now: This is the exact, verified inventory of every native Word dropdown (content control)
    why: Kept as before; now forced and checked.
- old line 587: ### Embedding the proposal email images — working procedure
    now: """Insert the accepted-proposal email pages (as images) into the Investment
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 588: build_roa.py does not do this step;
    now: build_roa.py <template.docx> <data.json> <output.docx>")
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 588: it must be done as a second pass on the
    now: it must open on the client's own reply.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 589: script's output, using a separate embedding script (build one per the template
    now: never hand-patch the .docx, never build an ROA as HTML, never overwrite a file without Paul's yes.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 590: below if it doesn't already exist as a saved asset).
    now: Raises ValueError if it is not a readable PDF."""
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 592: *Step 0 of this procedure — build the composite reply+quote HTML first, not just
    now: Find the reply by matching the subject line, not just the sender and date.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 594: Find the client's own reply email (per Step 1 point 9 and the "ROA date" rule —
    now: out.append("reply_email.%s is missing (the client's own reply email must be embedded)" % f)
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 595: this is the same email that sourced the ROA date, found via
    now: the embedded email pages the same size as the ROA's own text;
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 596: Microsoft 365:outlook_email_search / read_resource on the specific proposal's
    now: if the accepted proposal is not saved as a PDF, find it in Outlook (outlook_email_search / read_resource, match on the subject thread:
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 597: subject thread — beware sibling threads for other transactions with near-identical
    now: beware sibling threads for other transactions with near-identical reply text) and save it as a PDF or HTML page.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 598: reply text sent around the same time;
    now: field's text directly with "[Provider] - [Product Name]" in the same style as the
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 598: match on subject line, not just sender/date).
    now: Find the reply by matching the subject line, not just the sender and date.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 599: Take the already-built proposal HTML (the one used for the proposal-only embed)
    now: Take the already-built proposal HTML and its <body> inner content as the quoted portion.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 600: and extract its <body> inner content — this becomes the "quoted" portion.
    now: Take the already-built proposal HTML and its <body> inner content as the quoted portion.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 601: Prepend a new top section:
    now: """Insert a new child element into parent at the schema-correct position,
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 601: a header table for the reply (From:
    now: A header block for the reply itself in the same styled table as the proposal's own header:
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 602: reply's actual local sent time, To/Cc, Subject) in the same styled-table
    now: From (the client's own address), Sent (the reply's actual local sent time:
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 603: format as the proposal's own header, then the client's own message body verbatim
    now: The client's own message body verbatim (for example "kindly proceed with the attached").
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 604: "Hi All, As per our meeting today, [date], kindly proceed with the
    now: The client's own message body verbatim (for example "kindly proceed with the attached").
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 605: Regards, [Client Name]"), then a plain divider line ("On [day, date] at
    now: "The client's name appears in all places and the ID line reads 'I, Name, (ID:
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 606: [time], [forwarder] wrote:") before the quoted proposal content — indenting the
    now: the client's reply header and words, then the quoted proposal).")
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 607: quoted portion with a left border (e.g.
    now: A plain divider line "On [day, date] at [time], [forwarder] wrote:", then the quoted proposal with a left border (for example border-left:3px solid #cccccc;
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 607: border-left:3px solid #cccccc;
    now: def force_left_align(p):
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 608: padding-left:16px) makes the reply-vs-quote structure visually clear, matching
    now: padding-left:16px), so the reply-versus-quote structure reads like a real email thread.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 609: how a real email client renders a reply-in-thread.
    now: out.append("amount %r is not a positive amount (the figure the client confirmed in their own reply)" % a.get("amount"))
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 610: Convert sentDateTime (UTC) to local time (SAST = UTC+2) for the reply's own
    now: convert sentDateTime from UTC to SAST, UTC+2, and format it as Outlook does, for example "Wednesday, 12 August 2026 10:46"), To, Cc, Subject (usually "Re:
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 611: "Sent:" line, same as point 3 further below for the proposal's header.
    now: bad.append("the client's reply must come BEFORE the quoted proposal's header")
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 612: Feed this composite HTML into the wkhtmltopdf/pdftoppm pipeline below exactly as
    now: INCOME_AFTER_24_FIXED = "This need has been worked into the client's Lump Sum Disability Cover Benefit."
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 613: you would the proposal alone — same page geometry, same font-size rewrite
    now: the reply email + quoted proposal as one HTML page, as before
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 614: (point 2 below — rewrite every font-size value in the *composite* file, reply
    now: rewrite every font-size so the body text maps to 15 pt, render with wkhtmltopdf at a known page geometry
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 615: header included, not just the quoted portion) and no --zoom.
    now: Find the reply by matching the subject line, not just the sender and date.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 616: reply header → reply body → quoted original proposal (with
    now: the reply + quoted proposal page
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 617: its own header) → proposal's own closing/signature — which is what actually
    now: An embed that opens on the adviser's proposal, with the client's acceptance nowhere in the document, is an incomplete ROA and must be rebuilt.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 618: gets embedded as images, not the proposal in isolation.
    now: """Insert the accepted-proposal email pages (as images) into the Investment
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 620: *Recurring bug to check first, every time:
    now: # KNOWN RECURRING BUG (must be re-verified before every Retirement build):
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 620: scripts/embed_email_images.py's
    now: embed_email_images.py <built.docx> <images_dir> <out.docx> [heading to insert before]")
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 621: main() has repeatedly regressed to a hardcoded, client-specific work directory left
    now: (The Retirement heading has regressed before:
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 622: over from whichever client it was last edited for.
    now: file that was edited by hand.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 622: This breaks the next client's
    now: "Find the documents the page below lists for this bundle in the client's own folder.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 623: build if their session reuses stale files from that path.
    now: paths += [os.path.join(root, f) for f in sorted(files) if not f.endswith(".pyc")]
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 626: src_docx = os.path.abspath(sys.argv[1])
    now: src_docx = os.path.abspath(src_docx)
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 627: images_dir = os.path.abspath(sys.argv[2])
    now: images_dir = os.path.abspath(images_dir)
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 628: out_docx = os.path.abspath(sys.argv[3])
    now: out_docx = os.path.abspath(out_docx)
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 632: All three path arguments must be resolved to absolute paths on entry, and work
    now: the ROA is incomplete and must be rebuilt")
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 633: must always come from tempfile.mkdtemp() — never a literal path.
    now: tmpd = tempfile.mkdtemp(prefix="roa_run_")
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 634: wr-roa-builder-changelog.md (2026-08-08 entry).
    now: WR ROA Builder — construction script.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 636: Render the source HTML to PDF with wkhtmltopdf, never LibreOffice/soffice.
    now: never render the email with anything else.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 637: Converting an embedded-proposal HTML file via soffice --headless --convert-to pdf
    now: r = subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", tmpd, docx], capture_output=True, text=True, timeout=240)
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 638: silently bakes in visible thin lines under nearly every line of text (a
    now: """Names, ID and every figure must appear in the documents' own text.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 639: proofing/spell-check artifact of LibreOffice's headless HTML import) — this is
    now: python3 %s/run.py read %s --ack %s:%d --note "one line on what is on this page"' % (SCRIPTS, a.run, role, n))
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 640: invisible until you actually rasterize and look at the page, so always visually
    now: print("\nWhen every line above is a green tick and you have looked at the pages:
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 641: check at least one embedded page before delivering.
    now: *What you write (one HTML page, as before).
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 642: output.pdf renders the identical HTML cleanly with no such artifact and should be
    now: that a figure sits in the right place or column (attested), and anything on a page with no text (a scanned page):
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 643: the default tool for this step.
    now: print("\nRULES FOR THIS STEP (references/%s):\n" % r)
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 643: Then pdftoppm -jpeg -r 150 the resulting PDF as
    now: subprocess.run(["pdftoppm", "-jpeg", "-r", "70", os.path.join(tmpd, pdfs[0]), os.path.join(pages, "page")], capture_output=True)
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 645: Font size of the embedded email must match the ROA's own body text (11pt
    now: the embedded email pages the same size as the ROA's own text;
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 646: Aptos), not the source HTML's nominal size.
    now: add(not bad_sec, "Only the %s bundle is completed;
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 646: The embedded image is always
    now: The date is always the ROA date.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 647: displayed at a fixed width of 5,000,000 EMU (≈5.468in) regardless of the source
    now: the embedded image is shown at 5,000,000 EMU wide (about 5.468 in);
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 648: page's pixel dimensions, so if the source HTML is rendered at a normal document
    now: the page content is 7.5 in wide, so the scale is 0.729 and a
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 649: width, the text shrinks noticeably once placed at that fixed display width.
    now: run.py read <run> [--ack ROLE:PAGE --note TEXT]                               the documents' text, one page at a time
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 650: Compensate by rendering the source HTML at a known, explicit page geometry and
    now: rewrite every font-size so the body text maps to 15 pt, render with wkhtmltopdf at a known page geometry
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 651: a larger base font-size, calculated as:
    now: return "font-size:%.2fpt" % (v * factor)
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 653: scale = (5,000,000 / 914,400) / content_width_in   # display width ÷ source content width
    now: "Write ONE answers file in the layout the page below describes, every answer with its source, then run:
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 654: source_font_pt = 11 / scale
    now: def rescale_fonts(html, base_pt=None):
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 656: With wkhtmltopdf --page-width 8.5in --page-height 11in --margin-left 0.5in
    now: WK_FLAGS = ["--page-width", "8.5in", "--page-height", "11in", "--margin-left", "0.5in", "--margin-right", "0.5in", "--margin-top", "0.5in", "--margin-bottom", "0.5in"]
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 657: -margin-right 0.5in --margin-top 0.5in --margin-bottom 0.5in (content width
    now: WK_FLAGS = ["--page-width", "8.5in", "--page-height", "11in", "--margin-left", "0.5in", "--margin-right", "0.5in", "--margin-top", "0.5in", "--margin-bottom", "0.5in"]
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 658: 5in), this works out to 15pt as the source HTML's base font-size — use
    now: the listing shows %d bytes, equal to the local file%s" % (size, " (Paul said to overwrite)" if sv.get("overwrite") else "")
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 659: this figure unless the page geometry is deliberately changed, in which case
    now: "Find the documents the page below lists for this bundle in the client's own folder.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 660: recompute from the formula rather than reusing 15pt blindly.
    now: template changes, re-run this extraction rather than editing the option lists by hand
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 661: margin/page-width flags explicitly rather than relying on wkhtmltopdf defaults,
    now: f"asked for directly rather than defaulted."
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 662: so the scale factor is actually known and reproducible rather than assumed.
    now: Your reply to Paul is the saved file's name and folder, the .docx, and that audit, as they are.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 664: *Do not substitute wkhtmltopdf --zoom for this.
    now: You do not work from memory of this page:
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 664: Applying a zoom factor on top
    now: A document cannot be found on any of the three routes:
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 665: of the proposal HTML's own as-authored font sizes (which are chosen for on-screen
    now: base font of 15 pt shows as the ROA's own 11 pt Aptos.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 666: email reading, not for this formula) produces a displayed size close to but not
    now: raise ValueError("this file is not a PDF (some 'PDF' files are zipped page images:
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 667: exactly matching the target — it's an approximation layered on an assumption
    now: Only the checks that need an eye are left out (placeholder grey on screen, how an embedded page
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 668: rather than the calculation itself.
    now: f"asked for directly rather than defaulted."
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 668: The only correct method is to rewrite every
    now: The quote-reading method is validated for BrightRock proposals only.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 669: font-size value in the source HTML directly, scaled so that whatever the
    now: # blank literal text after "Date:"), so append the ROA date directly onto that
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 670: dominant/normal body text* size is in that HTML maps exactly to source_font_pt
    now: "that each figure sits in the right column of the quote (it is only proven to appear in the document)"]
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 671: (15pt at the standard geometry above) — e.g.
    now: you look at the pages",
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 671: if the proposal HTML's normal
    now: if the go-ahead was verbal, the date of the adviser's recap email.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 672: paragraphs are authored at 12pt, multiply every font-size value in the file by
    now: every font-size value rewritten by one factor so the dominant body size becomes 15 pt."""
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 673: 15/12, preserving the original relative hierarchy (headers, fine print,
    now: finding the original proposal is not enough.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 674: disclaimers all scale by the same factor).
    now: the date is set by tools/stamp_skill.py, never typed
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 674: Do this with a script (regex over every
    now: Never enter income_after24 (always Do not Review with a fixed sentence) or health care.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 675: font-size:Npt occurrence), not by eyeballing one or two values.
    now: every font-size value rewritten by one factor so the dominant body size becomes 15 pt."""
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 676: unset (or 1) when rendering — zoom scales spacing, borders and images too, which
    now: Try the routes IN THIS ORDER and record EVERY try, failures too:",
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 677: is not what this correction is about.
    now: Do not guess at options — this list is authoritative.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 677: Always visually compare a rendered embedded
    now: "the ROA is exactly what the program builds from the confirmed answers, and the email pages were rendered and embedded as required"
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 678: page against a rendered native ROA page at the same DPI before delivering, to
    now: R.add(good, "The email pages were rendered with wkhtmltopdf at the fixed geometry (no --zoom, no LibreOffice), fonts scaled to 15 pt, and embedded before '%s'" % emb.get("heading") if good else
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 679: confirm the two actually look the same size side by side.
    now: the embedded email pages the same size as the ROA's own text;
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 680: wr-roa-builder-changelog.md (2026-08-25 and 2026-08-27 entries).
    now: WR ROA Builder — construction script.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 681: The reproduced email must open with a proper header block for the actual
    now: bad.append("the page must OPEN with the reply's own header block (From:
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 682: message being embedded — From/Sent/To/Cc/Subject — showing the real sent
    now: for f in ("from", "sent", "to", "subject", "acceptance_text"):
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 683: date and time, not just the quoted messages beneath it.
    now: the chat writes ONE html page as before (the client's own reply header + body + the quoted proposal beneath it);
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 684: further down the thread naturally carry their own "From/Sent/To/Subject" lines
    now: for f in ("from", "sent", "to", "subject", "acceptance_text"):
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 685: (Outlook writes these into the quoted body text) — but the top/most-recent
    now: it opens on the client's own reply, then the quoted proposal.")
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 686: message's own metadata lives in the mailbox item's fields (sentDateTime, sender,
    now: # the active bundle's own section in document order.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 687: recipients), not in its body text, so it has to be added explicitly.
    now: A figure that is not in the text cannot have come from the document, so it is a red cross.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 688: sentDateTime (UTC) to local time (SAST = UTC+2) before writing it in, and format
    now: convert sentDateTime from UTC to SAST, UTC+2, and format it as Outlook does, for example "Wednesday, 12 August 2026 10:46"), To, Cc, Subject (usually "Re:
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 689: it the same way Outlook would (e.g.
    now: Insurer not in the 9-option list (e.g.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 689: "Wednesday, 12 August 2026 10:46").
    now: The short audit (Paul, 03/11/2026):
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 690: as its own header block ahead of the message body, styled consistently with the
    now: The client's own message body verbatim (for example "kindly proceed with the attached").
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 692: Use generous paragraph and section spacing that matches the original email's
    now: Use generous spacing (for example line-height:1.35, about 14 px paragraph margins), never compressed.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 693: visual rhythm — do not compress it to save space or render time.
    now: if s["status"] != "DO NOT REVIEW" or has_tbl:
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 694: markup for reliable rendering is fine and encouraged;
    now: reason_tbl = next((el for m, el in tables if reason_at is not None and m > reason_at), None)
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 695: the way is not — keep generous margins (e.g.
    now: The quote is not from BrightRock:
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 696: paragraph margins, extra top margin before bold section headings) so the
    now: insert_before_heading is the heading of the section that
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 697: embedded proposal reads with the same breathing room as the real email did.
    now: the embedded email pages the same size as the ROA's own text;
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 698: pdftoppm -jpeg -r 150 the Email Proposal PDF into one JPEG per page.
    now: the reply email + quoted proposal as one HTML page, as before
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 699: Copy each JPEG into word/media/, add an image relationship for each in
    now: Copy images into word/media with distinct names
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 700: word/_rels/document.xml.rels, and make sure [Content_Types].xml has a
    now: rels_path = os.path.join(work, 'word', '_rels', 'document.xml.rels')
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 701: Default Extension="jpg" ContentType="image/jpeg" entry (add it if missing).
    now: default.set('ContentType', 'image/jpeg')
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 702: Build one standalone paragraph per image:
    now: def build_image_paragraphs(rid, cx, cy, page_num, total_pages):
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 702: an inline w:drawing with a
    now: <w:drawing xmlns:wp="{NS['wp']}">
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 703: pic:spPr/a:ln picture border (not a table border), width capped at 5,000,000
    now: never shrink the image), no picture border bleeding into a page footer.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 704: EMU, height computed from the source image's own aspect ratio.
    now: say where the declined reason came from (declined_source, for example Paul's own words)" % tag)
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 705: small italic caption paragraph ("page X of Y").
    now: """Return (picture_paragraph_xml, caption_paragraph_xml) as lxml elements."""
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 706: Put <w:keepNext/><w:keepLines/> on the *picture* paragraph's pPr (before
    now: <w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="120" w:after="40"/><w:jc w:val="center"/></w:pPr>
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 707: spacing, per the standard element order in PPR_ORDER).
    now: the routes are tried in order (computer, Microsoft 365, Zapier);
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 708: image doesn't leave quite enough room on the current page for its caption, Word/
    now: python3 {scripts}/run.py doc {run} --role ROLE --file <local copy> --route <the route>   (ROLE is on the page below)",
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 709: LibreOffice orphans the caption alone onto the next page while the image stays
    now: looks next to the ROA's own text, an image border near the footer):
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 710: behind — the caption ends up separated from its image by a page break.
    now: "Read the quotes, application, follow-up notes and emails, one page at a time",
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 711: keepNext on the image paragraph, the pair is forced onto the same page as a
    now: never shrink the image), no picture border bleeding into a page footer.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 712: Verify this by checking that every "page X of Y" caption in the rendered
    now: R.attested.append("that the file really sits in the client's folder (the listing is typed by the chat)")
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 713: PDF lands at the same relative page position (i.e.
    now: """Insert a new child element into parent at the schema-correct position,
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 714: right after a full-page image) — if any caption turns up near the *top* of a
    now: never shrink the image), no picture border bleeding into a page footer.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 715: page, the image before it got orphaned and this fix is missing.
    now: A Retirement or Investment ROA needs wkhtmltopdf and the program says it is missing:
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 716: Do not insert blank spacer <w:p> paragraphs between an image paragraph and its
    now: pic_p, cap_p = build_image_paragraphs(rid, cx, cy, i, total_pages)
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 717: caption, or between successive image/caption pairs.
    now: # the lone spacer run between the Name SDT and the "(ID)" run —
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 718: fills a full page at the fixed display width, so an extra spacer paragraph forces an
    now: *You look at the page images the program saves for what a program cannot see:
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 719: additional blank page rather than adding breathing room — let keepNext/
    now: # both rows entirely rather than leaving them blank or "N/A"
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 720: keepLines (point 8 above) and the paragraphs' own spacing do that job instead.
    now: 1 | Run it | The one command that starts the job and how every step works |
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 721: Insert the paragraphs as siblings in word/body, positioned right after the
    now: Insert paragraphs into document.xml right after Investment's reason table,
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 722: active bundle section's reason table and before the next heading (e.g.
    now: # the active bundle's own section in document order.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 723: "POLICY REPLACEMENT" for an Investment bundle, or before "Investment Planning"
    now: Defaults to "POLICY REPLACEMENT" for Investment bundles
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 724: for a Retirement bundle — see the CLI 4th-argument note below) —
    now: "Find the documents the page below lists for this bundle in the client's own folder.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 725: *never inside the reason table cell itself.
    now: # find the reason heading and merged table after it
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 726: insert_before.addprevious(el) inserts elements in the order called, so iterate
    now: insert_before_heading is the heading of the section that
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 727: the paragraphs in their intended final order (image1, caption1, image2,
    now: """Embed the page images (JPEG files in images_dir, in name order) into the ROA.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 728: caption2, ...) — do not reverse the list first, or the pages render in reverse
    now: out.append("the ID number is not in the application or the Fact Find text")
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 729: order (Y, Y-1, ..., 1).
    now: return n.strftime("%Y-%m-%d")
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 730: Rezip and re-validate/re-render exactly as with the main build.
    now: never render the email with anything else.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 731: count increased by roughly one page per embedded image and that no caption is
    now: and for Retirement and Investment the embedded pages (count, place, captions, no spacer, width).
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 732: orphaned per the check in step 8.
    now: one line per check with a green tick or a red
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 734: *Recurring bug — insertion heading for Retirement bundles:
    now: # KNOWN RECURRING BUG (must be re-verified before every Retirement build):
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 735: images right before a target heading, read from an optional 4th CLI argument
    now: # right before that heading, i.e.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 736: (sys.argv[4]), defaulting to 'POLICY REPLACEMENT'.
    now: a["risk_profile"], "policy_replacement":
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 737: correct for Investment bundles (Investment is the last active section before
    now: # (Investment is the last active section before that block).
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 738: Retirement bundles must always pass "Investment Planning"
    now: Retirement is always "Retirement Planning";
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 739: as the 4th argument — otherwise the images land after the (inactive) Investment
    now: # is immediately followed by the (inactive) Investment section, not by
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 740: section instead of directly after Retirement's own table.
    now: base font of 15 pt shows as the ROA's own 11 pt Aptos.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 741: handling is still present before every Retirement build — full history:
    now: # KNOWN RECURRING BUG (must be re-verified before every Retirement build):
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 742: wr-roa-builder-changelog.md (2026-08-10 entry).
    now: WR ROA Builder — construction script.
    why: The recurring bugs (heading by bundle, fixed work folder, fonts) are now the program's job, as before in effect.
- old line 744: ## Step 5 — ROA Reference No.
    now: the "Your ROA reference number is X"
    why: Built by the program.
- old line 747: Personal, type of Business assurance] Cover - R
    now: scope (personal | business), premium ("R 1 172.80"), covers:
    why: The program picks the paragraph (Paul's answer 3).
- old line 752: The premium is the "Total premium" printed inside the accepted quote document (Step 0b).
    now: out.append("premium %r is not an amount (the 'Total premium' printed inside the accepted quote)" % a.get("premium"))
    why: The program picks the paragraph (Paul's answer 3).
- old line 755: These are never "Personal"/"Business" cover — do not use the Risk format above.
    now: Risk [Insurer] [Personal|Business] Cover - R[premium] p.m.
    why: Kept as before; now forced and checked.
- old line 756: [Product Provider] [Product Name] - R [amount][ - Lump Sum | p.m.],
    now: Retirement and Investment [Product Provider] [Product Name] - R [amount][ - Lump Sum | p.m.] (examples:
    why: Kept as before; now forced and checked.
- old line 757: using the answers to Step 1 questions 5a (product provider/name) and 5b (lump sum vs.
    now: Retirement and Investment [Product Provider] [Product Name] - R [amount][ - Lump Sum | p.m.] (examples:
    why: Kept as before; now forced and checked.
- old line 760: Old Mutual Retirement Annuity Xtra Max - R 1,500.00 p.m.
    now: Old Mutual Retirement Annuity Xtra Max - R 158,192.00 - Lump Sum and ...
    why: Kept as before; now forced and checked.
- old line 762: *Standing shortcut — Old Mutual Tax-Free Investment products:
    now: Old Mutual Tax-Free Investment shortcut:
    why: Kept as before; now forced and checked.
- old line 763: proposal is an Old Mutual Tax-Free Investment Plan (an Investment-bundle product),
    now: product provider Old Mutual, product name Tax-Free Investment Plan, recommended product Old Mutual - Max Investment;
    why: Kept as before; now forced and checked.
- old line 764: don't ask 5a/5b as open questions — these are fixed:
    now: with open(sys.argv[2]) as f:
    why: Kept as before; now forced and checked.
- old line 766: Tax-Free Investment Plan (so the combined reference reads "Old
    now: "Ninety-One - Tax-Free Investment Plan"), rather than
    why: Kept as before; now forced and checked.
- old line 767: Mutual Tax-Free Investment Plan - R [amount] p.m.")
    now: Old Mutual Tax-Free Investment shortcut:
    why: Kept as before; now forced and checked.
- old line 768: Recommendation for Identified Need dropdown:
    now: Recommendation for Identified Need — same gap applies:
    why: Kept as before; now forced and checked.
- old line 768: Old Mutual - Max Investment — the
    now: Old Mutual Tax-Free Investment shortcut:
    why: Kept as before; now forced and checked.
- old line 769: master product list (references/dropdown_field_map.md) has no separate
    now: The exact option lists are in dropdown_field_map.md (and the program reads them from the template itself).
    why: Kept as before; now forced and checked.
- old line 770: "Tax-Free" entry for Old Mutual;
    now: it's overwhelmingly BrightRock/Old Mutual/Sanlam/etc.
    why: Kept as before; now forced and checked.
- old line 770: "Max Investment" is the correct match since it's
    now: # bundles MUST pass "Investment Planning" here, since Retirement's section
    why: Kept as before; now forced and checked.
- old line 771: the underlying platform the client's quote/fact sheet documents reference.
    now: Every answer comes from the client's own documents or from Paul's words and is recorded with its source.
    why: Kept as before; now forced and checked.
- old line 772: Still ask 5b's underlying question (lump sum vs.
    now: That's permanent = Lump Sum Disability;
    why: Kept as before; now forced and checked.
- old line 773: Tax-Free product could in principle be funded either way, but in practice these
    now: # A cover type can be in the active bundle but still declined by the client —
    why: Kept as before; now forced and checked.
- old line 774: are almost always monthly/recurring contributions.
    now: out.append("frequency must be lump_sum or monthly (asked directly)")
    why: Kept as before; now forced and checked.
- old line 776: ## Delivery filename — every finished ROA must be named this way
    now: "Every line must be a green tick.
    why: Derived, never typed.
- old line 782: ROA - BR Personal Cover - R 4097.96 p.m.
    now: Old Mutual Personal Cover - R1,555.10 p.m.);
    why: The program picks the paragraph (Paul's answer 3).
- old line 782: - 26.05.26 - (Client Full Name)
    now: - [DD.MM.YY] - ([Client Full Name]);
    why: The program picks the paragraph (Paul's answer 3).
- old line 784: Rules (distinct from the in-document ROA Reference No.
    now: ref_sdts = [s for s in get_all_sdts(body) if sdt_alias(s) == 'ROA Reference Number']
    why: The program picks the paragraph (Paul's answer 3).
- old line 786: Insurer is title case (Old Mutual, Discovery, Sanlam, Liberty, Momentum, Altrisk,
    now: Recommendation for Identified Need, Old Mutual retirement annuity:
    why: The program picks the paragraph (Paul's answer 3).
- old line 787: Capital Legacy, Stanlib) — except BrightRock, which is always shortened to "BR"
    now: title case for the filename, except BrightRock which is always shortened to 'BR'.
    why: The program picks the paragraph (Paul's answer 3).
- old line 790: R 91555.10 p.m., not R 91,555.10 p.m.
    now: - R 1,500.00 p.m.).
    why: The program picks the paragraph (Paul's answer 3).
- old line 791: Date is always the ROA date (never today's date or the print date), formatted
    now: The date is always the ROA date.
    why: The program picks the paragraph (Paul's answer 3).
- old line 793: Client name is the full name, in parentheses, at the end.
    now: out.append("client_name must be the full name")
    why: The program picks the paragraph (Paul's answer 3).
- old line 795: Use build_filename() in scripts/build_roa.py to generate this automatically
    now: "scripts/run.py build (scripts/roa.py assembles the data, scripts/build_roa.py builds, scripts/embedpipe.py + embed_email_images.py embed the email pages for Retirement and Investment)",
    why: The program picks the paragraph (Paul's answer 3).
- old line 796: rather than constructing it by hand — call it with the same insurer/premium/date/
    now: the date is set by tools/stamp_skill.py, never typed
    why: The program picks the paragraph (Paul's answer 3).
- old line 797: client values used to build the document, then use that string (plus .docx) as the
    now: Do not conclude the document is blank and do not ask Paul to retype values.
    why: The program picks the paragraph (Paul's answer 3).
- old line 801: build_filename() hardcodes " p.m." and a Personal/Business cover scope, neither of
    now: rows.insert(1, ("Personal or Business", a["scope"].title(), s.get("scope")))
    why: Kept as before; now forced and checked.
- old line 802: which applies here — build the filename by hand instead:
    now: *What the program does (fixed, never by hand).
    why: Kept as before; now forced and checked.
- old line 803: ROA - [Product Provider] [Product Name] - R [amount][ - Lump Sum | p.m.] -
    now: Retirement and Investment [Product Provider] [Product Name] - R [amount][ - Lump Sum | p.m.] (examples:
    why: Kept as before; now forced and checked.
- old line 806: ROA - Old Mutual Retirement Annuity Xtra Max - R 158192.00 -
    now: Old Mutual Retirement Annuity Xtra Max - R 158,192.00 - Lump Sum and ...
    why: Kept as before; now forced and checked.
- old line 807: Lump Sum - 09.03.26 - (Client Full Name)
    now: - [DD.MM.YY] - ([Client Full Name]);
    why: Kept as before; now forced and checked.
- old line 809: Same numeric formatting rules as the Risk filename (no thousands comma, 2 decimals,
    now: 4097.96) — formatted with no thousands comma, 2 decimals
    why: Kept as before; now forced and checked.
- old line 810: space after "R", date always DD.MM.YY from the ROA date).
    now: The date is always the ROA date.
    why: Kept as before; now forced and checked.
- old line 812: ## Step 6 — Fixed constants (never vary by client)
    now: *What the program does (fixed, never by hand).
    why: Constants live in the script and the template page.
- old line 816: always ROA date + 12 months (the build script computes
    now: always the ROA date plus 12 months, computed by the script.
    why: Constants live in the script and the template page.
- old line 817: this automatically — never source it from the quotes or ask separately).
    now: Read the PDF from the computer, or ask Paul to attach that PDF.
    why: Constants live in the script and the template page.
- old line 819: ## Step 7 — Mandatory pre-delivery audit
    now: "The program opens the finished ROA and proves the pre-delivery checks;
    why: The audit is done by the program (Paul's answer 2).
- old line 821: Before calling an ROA finished, check every item below.
    now: "every program check on the finished .docx is a green tick"
    why: The audit is done by the program (Paul's answer 2).
- old line 821: Do this by actually reading
    now: the date is set by tools/stamp_skill.py, never typed
    why: The audit is done by the program (Paul's answer 2).
- old line 822: the rendered PDF pages (via the visual-check step in references/roa_data_schema.md),
    now: See references/roa_data_schema.md in the skill for the full data shape.
    why: The audit is done by the program (Paul's answer 2).
- old line 823: not just by re-reading the data dict you built.
    now: dict keyed by section key -> section data dict, only needed for
    why: The audit is done by the program (Paul's answer 2).
- old line 825: Only one bundle (Risk / Retirement / Investment) is actively completed;
    now: one bundle only (Risk, Retirement or Investment), a single client, never Health Care.
    why: The program picks the paragraph (Paul's answer 3).
- old line 826: other section shows only its heading and reason text — the data table is fully
    now: every other section (and any declined need) shows only its heading and reason text" % b if not bad_sec else "Section problem:
    why: The program picks the paragraph (Paul's answer 3).
- old line 827: gone, not left showing "Choose an item."
    now: items = [i.strip() for i in items if i and i.strip() not in ("Choose an item.", ".")]
    why: The program picks the paragraph (Paul's answer 3).
- old line 828: Health Care does not appear anywhere in the document at all.
    now: add("health care" not in full.lower(), "Health Care does not appear anywhere in the document")
    why: The program picks the paragraph (Paul's answer 3).
- old line 830: sentence, even when Income Protection (1st 24 months) is active.
    now: "Income Protection (1st 24 months)", "dread":
    why: The program picks the paragraph (Paul's answer 3).
- old line 831: Every dropdown selection matches an option that genuinely exists in
    now: every dropdown choice is a real option of the template;
    why: The program picks the paragraph (Paul's answer 3).
- old line 832: references/dropdown_field_map.md — no invented options, no selection of the "."
    now: dropdown_field_map.md lists every dropdown option.
    why: The program picks the paragraph (Paul's answer 3).
- old line 833: insurer error-option, no "preserve"/"retirement" selected for Retirement's Need
    now: matches the insurer and cover type recommended for that need.
    why: The program picks the paragraph (Paul's answer 3).
- old line 834: Lump Sum Disability and Income Protection (1st 24 months) Need Identified fields are filled (not blank).
    now: Lump Sum Disability and Income Protection (1st 24 months) must be given:
    why: The program picks the paragraph (Paul's answer 3).
- old line 835: Death shows "Life Cover" and Dread shows "Comprehensive Severe Illness" as Need
    now: Death is always "Life Cover" and Dread always "Comprehensive Severe Illness" (hard-coded by the script);
    why: The program picks the paragraph (Paul's answer 3).
- old line 836: Identified, regardless of what the source documents call them.
    now: the program refuses what it cannot find in the documents' text.
    why: The program picks the paragraph (Paul's answer 3).
- old line 837: Replacement status was set independently per cover type within the Risk bundle,
    now: replacement must be true or false, per cover type" % tag)
    why: The program picks the paragraph (Paul's answer 3).
- old line 838: not copied uniformly across all four.
    now: if a.role not in roa.ALL_ROLES:
    why: The program picks the paragraph (Paul's answer 3).
- old line 839: Every reason-textbox paragraph traces to either the response bank (risk bundle),
    now: paragraph}} read from the response bank (Word) exactly as written."""
    why: The program picks the paragraph (Paul's answer 3).
- old line 840: the fixed rule sentences (declined need / BR after-24-months / new-cover-type wording in Step 4), or a pasted client
    now: "Income Protector Planning After 24 Months is Do not Review with the fixed sentence")
    why: The program picks the paragraph (Paul's answer 3).
- old line 841: proposal email (Retirement/Investment) — never free-written from scratch.
    now: EMAIL_HTML = "email.html"               # Retirement / Investment:
    why: The program picks the paragraph (Paul's answer 3).
- old line 842: declined cover type has its own specific, asked-for reason — never a generic
    now: a declined need needs the specific reason Paul gave (asked for, never generic)" % tag)
    why: The program picks the paragraph (Paul's answer 3).
- old line 844: Any cover type the client declined shows "Do not Review" with its data table
    now: Income After 24 months is Do not Review with the fixed sentence;
    why: The program picks the paragraph (Paul's answer 3).
- old line 845: removed, even though it's within the active bundle — declined is not the same as
    now: add(not bad_sec, "Only the %s bundle is completed;
    why: The program picks the paragraph (Paul's answer 3).
- old line 846: "outside the bundle," but gets the same document treatment.
    now: # the active bundle's own section in document order.
    why: The program picks the paragraph (Paul's answer 3).
- old line 847: The RAR reference number field does not appear anywhere in the document.
    now: add("health care" not in full.lower(), "Health Care does not appear anywhere in the document")
    why: The program picks the paragraph (Paul's answer 3).
- old line 848: Every Recommended Amount / Taken Up Amount figure traces to the correct Summary
    now: for f in ("recommended_amount", "taken_up_amount"):
    why: The program picks the paragraph (Paul's answer 3).
- old line 849: block column in the correct uploaded quote (FNA Quote → Recommended;
    now: the accepted quote is the FNA quote")
    why: The program picks the paragraph (Paul's answer 3).
- old line 850: Accepted Quote → Taken Up), and dual lump/monthly fields show one clean value, not
    now: Recommended and Taken Up amounts show one clean value (a not-accepted cover shows R 0);
    why: The program picks the paragraph (Paul's answer 3).
- old line 852: Client name appears correctly in both places, the ID confirmation line reads
    now: "The client's name appears in all places and the ID line reads 'I, Name, (ID:
    why: The program picks the paragraph (Paul's answer 3).
- old line 853: <13-digit ID>), hereby confirm" with clean single commas, and the
    now: %s), hereby confirm" % (nm, cid)) in full and re.fullmatch(r"\d{13}", cid) is not None,
    why: The program picks the paragraph (Paul's answer 3).
- old line 854: ID is 13 digits with no spaces or dashes.
    now: 13 digits, no spaces, no dashes.
    why: The program picks the paragraph (Paul's answer 3).
- old line 857: No "Choose an item.", "Click here to enter amount.", or other template
    now: no "Choose an item." or other placeholder text;
    why: The program picks the paragraph (Paul's answer 3).
- old line 858: placeholder text remains in any field that should have been completed for the
    now: A figure that is not in the text cannot have come from the document, so it is a red cross.
    why: The program picks the paragraph (Paul's answer 3).
- old line 860: The delivered file's name follows the required convention exactly — see
    now: the saved file's name and folder, the .docx in the chat, then the short audit.
    why: The program picks the paragraph (Paul's answer 3).
- old line 861: "Delivery filename" above — not the in-document ROA Reference No.
    now: A figure that is not in the text cannot have come from the document, so it is a red cross.
    why: The program picks the paragraph (Paul's answer 3).
- old line 862: not a generic/default filename.
    now: raise ValueError("this file is not a PDF (some 'PDF' files are zipped page images:
    why: The program picks the paragraph (Paul's answer 3).
- old line 864: Product Provider + Product Name format ending in "- Lump Sum" or "p.m." as
    now: Retirement and Investment [Product Provider] [Product Name] - R [amount][ - Lump Sum | p.m.] (examples:
    why: The program picks the paragraph (Paul's answer 3).
- old line 865: appropriate — never the Risk bundle's "[Insurer] Personal/Business Cover" format.
    now: Risk [Insurer] [Personal|Business] Cover - R[premium] p.m.
    why: The program picks the paragraph (Paul's answer 3).
- old line 866: For Retirement/Investment ROAs with an embedded proposal email:
    now: and for Retirement and Investment the embedded pages (count, place, captions, no spacer, width).
    why: The program picks the paragraph (Paul's answer 3).
- old line 867: textbox itself holds only the short pointer line, the actual email pages are
    now: The reason box itself holds only the pointer line:
    why: The program picks the paragraph (Paul's answer 3).
- old line 868: standalone bordered image paragraphs after the data table (not inside any table
    now: bordered picture paragraphs after the section's data/reason table, never
    why: The program picks the paragraph (Paul's answer 3).
- old line 869: cell), and no image's border bleeds into a page footer on the rendered PDF —
    now: never shrink the image), no picture border bleeding into a page footer.
    why: The program picks the paragraph (Paul's answer 3).
- old line 870: check this visually, not just via validate.py.
    now: w.die('This is not a run folder (no %s).
    why: The program picks the paragraph (Paul's answer 3).
- old line 871: document is the client's own reply email (with the proposal quoted beneath it),
    now: the client's own reply email with the proposal quoted beneath (one HTML page)",
    why: The program picks the paragraph (Paul's answer 3).
- old line 872: not the proposal email alone — the first embedded page must show a header
    now: "The combined reply-and-proposal email page is not registered:
    why: The program picks the paragraph (Paul's answer 3).
- old line 873: block naming the client as sender and the client's own acceptance wording (e.g.
    now: bad.append("the client's own acceptance wording is not in the page")
    why: The program picks the paragraph (Paul's answer 3).
- old line 874: "kindly proceed with the attached"), not the adviser's proposal header as the
    now: A header block for the reply itself in the same styled table as the proposal's own header:
    why: The program picks the paragraph (Paul's answer 3).
- old line 875: This is non-negotiable — an embed that opens directly on
    now: # blank literal text after "Date:"), so append the ROA date directly onto that
    why: The program picks the paragraph (Paul's answer 3).
- old line 876: the adviser's proposal, with the client's acceptance email nowhere in the
    now: An embed that opens on the adviser's proposal, with the client's acceptance nowhere in the document, is an incomplete ROA and must be rebuilt.
    why: The program picks the paragraph (Paul's answer 3).
- old line 877: document, is treated as an incomplete ROA and must be rebuilt.
    now: the ROA is incomplete and must be rebuilt")
    why: The program picks the paragraph (Paul's answer 3).
- old line 878: For the Retirement section specifically:
    now: sections in the active bundle (see build_section for shape)
    why: The program picks the paragraph (Paul's answer 3).
- old line 879: Considered / Recommended Insurer / Recommendation for Identified Need, then
    now: for lab in ("Insurers Considered", "Recommended Insurer", "Recommendation for Identified Need"):
    why: The program picks the paragraph (Paul's answer 3).
- old line 880: The raw template has Retirement's Reason row before the
    now: # the raw template physically places the Reason row BEFORE the insurer rows
    why: The program picks the paragraph (Paul's answer 3).
- old line 881: insurer rows (unlike every other section);
    now: # 1 one bundle, every other section only heading and reason;
    why: The program picks the paragraph (Paul's answer 3).
- old line 881: build_roa.py reorders this
    now: build_roa.py <template.docx> <data.json> <output.docx>")
    why: The program picks the paragraph (Paul's answer 3).
- old line 882: automatically, but confirm it visually since this is the one section where the
    now: R.attested += ["the advice itself, the ROA date's source and that this is the right transaction folder (judgement, recorded with sources)",
    why: The program picks the paragraph (Paul's answer 3).
- old line 883: template's native order is wrong and easy to regress if the script changes.
    now: The ROA is saved into the client's folder and given to Paul in the chat.
    why: The program picks the paragraph (Paul's answer 3).
- old line 884: Embedded email font size actually matches the surrounding ROA body text —
    now: the embedded email pages the same size as the ROA's own text;
    why: The program picks the paragraph (Paul's answer 3).
- old line 885: verify this visually, side by side, not just by trusting the command used.
    now: Find the reply by matching the subject line, not just the sender and date.
    why: The program picks the paragraph (Paul's answer 3).
- old line 886: Render one native ROA page and one embedded-email page at the same DPI and
    now: the embedded email pages the same size as the ROA's own text;
    why: The program picks the paragraph (Paul's answer 3).
- old line 887: If the embedded text reads noticeably larger or smaller than
    now: filled fields black on screen, the embedded email pages the same size as the ROA's own text at the same resolution (if they read larger or smaller, tell Paul:
    why: The program picks the paragraph (Paul's answer 3).
- old line 888: the surrounding document at a glance, the font-size rewrite was skipped, done on
    now: A document cannot be found on any of the three routes:
    why: The program picks the paragraph (Paul's answer 3).
- old line 889: the wrong baseline value, or --zoom was used — fix the HTML and rebuild rather
    now: If anything is wrong, fix the answers or the email page and rebuild;
    why: The program picks the paragraph (Paul's answer 3).
- old line 890: than adjusting the display width or shrinking the image.
    now: If anything is wrong, fix the answers or the email page and rebuild;
    why: The program picks the paragraph (Paul's answer 3).
- old line 892: Any FNA-analyzed-but-not-accepted cover type (as opposed to an outright decline)
    now: state = accepted | not_accepted (FNA done but the benefit was not taken up:
    why: The audit is done by the program (Paul's answer 2).
- old line 893: still shows Status = IMPORTANT with its data table intact (Recommended Amount
    now: bad_sec.append("%s should be IMPORTANT with its table (is %s)" % (k, s["status"]))
    why: The audit is done by the program (Paul's answer 2).
- old line 894: from the FNA, Taken Up Amount = 0) and the "FNA DONE / BENEFIT NOT ACCEPTED"
    now: Recommended and Taken Up amounts show one clean value (a not-accepted cover shows R 0);
    why: The audit is done by the program (Paul's answer 2).
- old line 895: response-bank paragraph — it has not been mistakenly treated as a decline.
    now: Reason text is a bank paragraph word for word, a fixed sentence, the reason Paul gave, or the pointer line;
    why: The audit is done by the program (Paul's answer 2).
- old line 896: No filled field renders in placeholder grey instead of black (a sign the
    now: no filled field in placeholder grey;
    why: The audit is done by the program (Paul's answer 2).
- old line 897: PlaceholderText style reference wasn't stripped alongside the data binding).
    now: set_sdt_plain_text(s, data['roa_reference_no'], strip_databinding=True)
    why: The audit is done by the program (Paul's answer 2).
- old line 899: If any check fails, fix it in the data dict and rebuild — don't hand-patch the output
    now: If anything is wrong, fix the answers or the email page and rebuild;
    why: The audit is done by the program (Paul's answer 2).
- old line 900: .docx directly, or the fix won't carry forward to the next client.
    now: If no route can carry a .docx, give it to Paul in the chat and name the folder to drop it in.
    why: The audit is done by the program (Paul's answer 2).
- old line 902: ## Delivery — pushing the finished file into the client's SharePoint folder
    now: print("Name to use in the client's ROA & Bus ROA folder:
    why: Reworded to the standard routes.
- old line 904: tool availability is per-session, not guaranteed by this skill.
    now: which version of this skill is running.
    why: Reworded to the standard routes.
- old line 905: the local device bridge (mcp__remote-devices__* tools) is connected, whether
    now: 1 the computer (device bridge), 2 the Microsoft 365 connector (sharepoint_search, then read_resource on the hit's uri:
    why: Reworded to the standard routes.
- old line 906: Microsoft 365:sharepoint_upload_file exposes a plain-text content parameter (in
    now: "the Microsoft 365 connector (SharePoint / OneDrive)",
    why: Reworded to the standard routes.
- old line 907: addition to contentBase64), and whether the M365 connector is fully authorized in
    now: add("PAUL KAFENTZIS" in full and "GARETH" not in full.upper(), "The financial planner is PAUL KAFENTZIS")
    why: Reworded to the standard routes.
- old line 908: this specific chat, can all differ from one session to the next — this is connector/
    now: "NINETY-ONE", all caps to match the existing list's style).
    why: Reworded to the standard routes.
- old line 909: device/infrastructure state, not something a skill file controls.
    now: if not a.file or not os.path.isfile(a.file):
    why: Reworded to the standard routes.
- old line 910: today's tool shape based on a description pasted from another chat, a prior
    now: If the quote is from another insurer, tell Paul before going on;
    why: Reworded to the standard routes.
- old line 911: session's summary, or what worked last time.
    now: %s (%s)" % (what or os.path.basename(path), path))
    why: Reworded to the standard routes.
- old line 911: Always check what's actually
    now: run.py check <run> [--no-render]                                              prove what the program can;
    why: Reworded to the standard routes.
- old line 912: available right now in this session before deciding which path below applies.
    now: # right before that heading, i.e.
    why: Reworded to the standard routes.
- old line 914: ### Step A — Check what's actually available, every time, in this order
    now: """Reads a client document's text (PDF or HTML/text), page by page, and checks that what the chat entered really appears in it.
    why: Replaced by the standard route order.
- old line 915: Call mcp__remote-devices__get_device_info.
    now: "the computer (local drive / OneDrive through the device bridge)",
    why: Replaced by the standard route order.
- old line 916: []), Paul's own computer is reachable from
    now: "the page opens on the client's own reply with their acceptance wording, then the quoted proposal (or this is a Risk ROA)"
    why: Replaced by the standard route order.
- old line 917: this session — go to Path 0, the preferred delivery method whenever it's
    now: if the go-ahead was verbal, the date of the adviser's recap email.
    why: Replaced by the standard route order.
- old line 918: available, since it writes a real uncorrupted .docx with no manual step.
    now: R.attested.append("figures in a document with no readable text")
    why: Replaced by the standard route order.
- old line 919: call errors or the tools aren't present in this session's tool list at all, no
    now: "NINETY-ONE", all caps to match the existing list's style).
    why: Replaced by the standard route order.
- old line 920: device is connected this session — skip to step 2.
    now: It refuses to skip a step.
    why: Replaced by the standard route order.
- old line 921: Confirm Microsoft 365:sharepoint_upload_file is loaded and inspect its real
    now: "the Microsoft 365 connector (SharePoint / OneDrive)",
    why: Replaced by the standard route order.
- old line 922: If it has a content (plain text) parameter, go to Path 1.
    now: field is a native content control, so it can still hold arbitrary text — write the
    why: Replaced by the standard route order.
- old line 923: *only has contentBase64, go to Path 2.
    now: the program refuses to go on.
    why: Replaced by the standard route order.
- old line 924: If any upload attempt (test or real) returns an auth/consent error like
    now: If a tool returns an authorisation error such as "No approval received", that is a stuck connector:
    why: Replaced by the standard route order.
- old line 925: "No approval received" rather than a content/size problem, that is a different
    now: # both rows entirely rather than leaving them blank or "N/A"
    why: Replaced by the standard route order.
- old line 926: issue — a stuck or missing connector authorization — and no amount of format
    now: that a figure sits in the right place or column (attested), and anything on a page with no text (a scanned page):
    why: Replaced by the standard route order.
- old line 927: change (HTML, smaller file, etc.) will fix it.
    now: run.py email <run> --file email.html [--base-pt N]                            Retirement / Investment:
    why: Replaced by the standard route order.
- old line 927: Tell the user plainly that the
    now: 1 | Run it | The one command that starts the job and how every step works |
    why: Replaced by the standard route order.
- old line 928: connector itself needs their attention (check for a pending approval prompt, or
    now: If a tool returns an authorisation error such as "No approval received", that is a stuck connector:
    why: Replaced by the standard route order.
- old line 929: reconnect the M365 connector), rather than continuing to retry uploads.
    now: template changes, re-run this extraction rather than editing the option lists by hand
    why: Replaced by the standard route order.
- old line 931: ### Path 0 — Local device bridge connected:
    now: "the computer (local drive / OneDrive through the device bridge)",
    why: Kept as the computer route.
- old line 931: write directly into the client's OneDrive-synced folder (preferred whenever available)
    now: print("Name to use in the client's ROA & Bus ROA folder:
    why: Kept as the computer route.
- old line 933: When this session can reach Paul's own computer, the finished .docx can be written
    now: "the page opens on the client's own reply with their acceptance wording, then the quoted proposal (or this is a Risk ROA)"
    why: Kept as the computer route.
- old line 934: directly into the exact same folder the ROA was sourced from in SharePoint, via that
    now: insurer name directly via the same text-override technique used for Need Identified
    why: Kept as the computer route.
- old line 935: folder's local OneDrive-for-Business sync mirror — no base64, no HTML conversion, no
    now: the client's own folder, liferisk.co.za\Company - Paul\New Business\[Surname, First Name]\...
    why: Kept as the computer route.
- old line 936: manual drag-and-drop, and it becomes the live SharePoint copy automatically the next
    now: # visual breathing room and drop the rest — this only removes empty paragraphs,
    why: Kept as the computer route.
- old line 937: This sidesteps the entire binary-upload problem Path 1/Path 2
    now: Find this skill's folder (the "Base directory" shown when the skill loaded;
    why: Kept as the computer route.
- old line 938: exist to work around, so prefer it over both whenever get_device_info succeeds.
    now: the listing shows %d bytes, equal to the local file%s" % (size, " (Paul said to overwrite)" if sv.get("overwrite") else "")
    why: Kept as the computer route.
- old line 940: Find the OneDrive-for-Business sync root — discover it fresh, never hardcode
    now: "Find the documents the page below lists for this bundle in the client's own folder.
    why: Kept as the computer route.
- old line 941: Call get_device_info and read homeDirectories:
    now: if r.get('Id', '').startswith('rId') and r.get('Id')[3:].isdigit()
    why: Kept as the computer route.
- old line 941: look for a folder named
    now: Choose a new run folder, for example /tmp/wr-roa-<Surname>-<DDMMYY>, and start:
    why: Kept as the computer route.
- old line 942: after the firm's tenant domain (liferisk.co.za, the local mirror of the whole
    now: """The domain model of the ROA:
    why: Kept as the computer route.
- old line 943: liferisk.sharepoint.com tenant Paul's documents live on — the same tenant
    now: # sentence near the bottom is a plain-text mail-merge field on the same binding,
    why: Kept as the computer route.
- old line 944: Microsoft 365:sharepoint_search results point to).
    now: "the Microsoft 365 connector (SharePoint / OneDrive)",
    why: Kept as the computer route.
- old line 945: per-session/per-machine from homeDirectories, never assumed from a previous
    now: Every figure comes from the client's actual quote or email, never from a previous client, never estimated.
    why: Kept as the computer route.
- old line 947: Request access to that tenant-root folder, not a client subfolder, and only
    now: A need that exists but the client will not pursue:
    why: Kept as the computer route.
- old line 948: Use device_request_folder_access with one clear, specific
    now: one line per check with a green tick or a red
    why: Kept as the computer route.
- old line 949: "to save [Client]'s ROA into their SharePoint client folder, synced
    now: print("Name to use in the client's ROA & Bus ROA folder:
    why: Kept as the computer route.
- old line 950: This spends one of Paul's confirmation-dialog interactions — asking for
    now: (question, answer, source) for Paul's ONE question (Step 0b)."""
    why: Kept as the computer route.
- old line 951: the narrow client folder means asking again for every future client, so always
    now: run answers again so every entry is re-checked against it.")
    why: Kept as the computer route.
- old line 952: request the tenant root itself.
    now: The reason box itself holds only the pointer line:
    why: Kept as the computer route.
- old line 952: Check get_device_info.connectedFolders first
    now: def check(path, a, data, rs, lists, embed_info=None):
    why: Kept as the computer route.
- old line 953: — if it already covers this root (granted earlier in the session), do not
    now: if k not in COVERS or c.get("state") not in ("accepted", "not_accepted"):
    why: Kept as the computer route.
- old line 954: access persists for the rest of the session once granted.
    now: ## Per-section fields (repeats for each of the 7 product sections below)
    why: Kept as the computer route.
- old line 955: Identify the SharePoint library folder underneath the tenant root.
    now: "List the client's ROA & Bus ROA folder (computer first, then Microsoft 365, then Zapier;
    why: Kept as the computer route.
- old line 956: SharePoint document library appears locally as Company - [Library] (e.g.
    now: out.append("%s %r must be in CAPITALS (as in the dropdown list, e.g.
    why: Kept as the computer route.
- old line 957: Company - Paul is the local mirror of the Paul library at
    now: This skill is a program that walks you through the job one step at a time.
    why: Kept as the computer route.
- old line 958: https://liferisk.sharepoint.com/Paul/...).
    now: "the Microsoft 365 connector (SharePoint / OneDrive)",
    why: Kept as the computer route.
- old line 958: Use device_list_dir on the tenant
    now: Send the file with SendUserFile, then device_commit_files with its file_uuid and the exact file name;
    why: Kept as the computer route.
- old line 959: root to confirm the exact folder name before assuming it matches the SharePoint
    now: Your reply to Paul is the saved file's name and folder, the .docx, and that audit, as they are.
    why: Kept as the computer route.
- old line 960: URL segment verbatim — don't guess this across different machines/tenants.
    now: A client can have several sibling folders for different products at once:
    why: Kept as the computer route.
- old line 961: Everything after the library segment in the SharePoint URL maps directly to the
    now: # blank literal text after "Date:"), so append the ROA date directly onto that
    why: Kept as the computer route.
- old line 962: local path, folder-for-folder.
    now: local = os.path.join(run, w.OUT, sv["name"])
    why: Kept as the computer route.
- old line 962: SharePoint's Paul/New Business/[Surname,
    now: the client's own folder, liferisk.co.za\Company - Paul\New Business\[Surname, First Name]\...
    why: Kept as the computer route.
- old line 963: First Name]/[Surname, First Name] (Product - Amount)/ROA & Bus ROA is locally
    now: ("bundle", "client_name_id", "risk_profile", "insurers", "roa_date", "product", "amount", "replacement"),
    why: Kept as the computer route.
- old line 964: Company - Paul\New Business\[Surname, First Name]\[Surname, First Name] (Product
    now: the client's own folder, liferisk.co.za\Company - Paul\New Business\[Surname, First Name]\...
    why: Kept as the computer route.
- old line 965: Walk this with device_list_dir one level at a time to
    now: "Read the quotes, application, follow-up notes and emails, one page at a time",
    why: Kept as the computer route.
- old line 966: find the client's specific transaction subfolder and confirm each name exactly
    now: "Find the client's documents (three routes, every try logged) and register each one",
    why: Kept as the computer route.
- old line 967: (commas, parentheses, and premium amounts in folder names must match precisely) —
    now: "If no route can carry a .docx, give the file to Paul in the chat and tell him exactly which folder to drop it in;
    why: Kept as the computer route.
- old line 968: never construct the full path blind from memory of the SharePoint URL alone.
    now: The program shows the right page at each step, so you do not work from memory of them.
    why: Kept as the computer route.
- old line 969: List the destination ROA & Bus ROA folder before writing.
    now: "Save the ROA in the client's ROA & Bus ROA folder, never overwriting without Paul's yes",
    why: Kept as the computer route.
- old line 970: file with the exact delivery filename (see "Delivery filename" above) already
    now: name = roa.delivery_filename(ans)
    why: Kept as the computer route.
- old line 971: an earlier draft rebuilt during the same session, or a stale
    now: """A whole-rand amount from 'R 1 000 000' (the template shows whole rands) as an int, or None."""
    why: Kept as the computer route.
- old line 972: file left by a previous adviser.
    now: File name (derived by the program, never typed):
    why: Kept as the computer route.
- old line 972: If one exists, confirm with Paul whether to
    now: If no route can carry a .docx, give it to Paul in the chat and name the folder to drop it in.
    why: Kept as the computer route.
- old line 973: true to device_commit_files;
    now: total_pages = len(image_files)
    why: Kept as the computer route.
- old line 974: silently over an existing file in a client's compliance folder.
    now: Never overwrite a file in a client's compliance folder without Paul's yes.
    why: Kept as the computer route.
- old line 975: Deliver in exactly two calls, in this order:
    now: The reply, in this order:
    why: Kept as the computer route.
- old line 976: locally-built .docx (this returns a file_uuid), then
    now: raise ValueError("this file is not a PDF (some 'PDF' files are zipped page images:
    why: Kept as the computer route.
- old line 977: mcp__remote-devices__device_commit_files with that file_uuid and the full
    now: Send the file with SendUserFile, then device_commit_files with its file_uuid and the exact file name;
    why: Kept as the computer route.
- old line 978: devicePath built from steps 3–4, using the exact required delivery filename
    now: """Build the required delivery filename:
    why: Kept as the computer route.
- old line 979: as the final path component — never a generic name like output.docx or
    now: You never edit a script, the data or the .docx."
    why: Kept as the computer route.
- old line 980: device_commit_files only accepts a file_uuid from a prior
    now: Send the file with SendUserFile, then device_commit_files with its file_uuid and the exact file name;
    why: Kept as the computer route.
- old line 981: SendUserFile call in this same session;
    now: The reply, in this order:
    why: Kept as the computer route.
- old line 981: it cannot take a raw container path.
    now: against a real delivered ROA), not the raw template look.
    why: Kept as the computer route.
- old line 982: Confirm success from the tool's actual result, not just the absence of a thrown
    now: confirm from the tool's result that the full path is in written and rejected is empty.
    why: Kept as the computer route.
- old line 983: Check that the written array contains the expected full path and that
    now: 2 | What a finished run contains | The saved ROA and the short audit |
    why: Kept as the computer route.
- old line 984: A rejection includes the device file's current
    now: Your reply to Paul is the saved file's name and folder, the .docx, and that audit, as they are.
    why: Kept as the computer route.
- old line 985: mtimeMs/size — use that to tell a genuine conflict (a newer file already there)
    now: record every try with --purpose save) and note the file names already there.
    why: Kept as the computer route.
- old line 986: from a plain permissions problem before deciding how to proceed.
    now: before 'Investment Planning' for a Retirement ROA, before 'POLICY REPLACEMENT' for an Investment ROA.
    why: Kept as the computer route.
- old line 987: Tell Paul plainly what happened and exactly where, using the right verb.
    now: "If no route can carry a .docx, give the file to Paul in the chat and tell him exactly which folder to drop it in;
    why: Kept as the computer route.
- old line 988: the file was saved to his computer in [folder], and that it will sync back
    now: Say the file was saved to Paul's computer and will sync to SharePoint by itself (not "uploaded to SharePoint").
    why: Kept as the computer route.
- old line 989: to SharePoint on its own — do not say "uploaded to SharePoint," since what
    now: Say the file was saved to Paul's computer and will sync to SharePoint by itself (not "uploaded to SharePoint").
    why: Kept as the computer route.
- old line 990: actually happened is a local write via OneDrive sync, a different mechanism from
    now: take the date from the latest Follow-Up Notes, but if a written client reply or recap email has a different date use the written one and tell Paul.
    why: Kept as the computer route.
- old line 1021: ### Path 2 — Only contentBase64 is available:
    now: add(not bad_sec, "Only the %s bundle is completed;
    why: Kept as the manual fallback.
- old line 1021: fall back to manual delivery
    now: It refuses to skip a step.
    why: Kept as the manual fallback.
- old line 1022: This is the older/more limited case.
    now: """Answers 'is this in the report?' against the extracted text."""
    why: Kept as the manual fallback.
- old line 1022: Do not attempt to force a docx or HTML file
    now: if s["status"] != "DO NOT REVIEW" or has_tbl:
    why: Kept as the manual fallback.
- old line 1023: through contentBase64 by typing it out as base64 — for anything beyond a trivial
    now: The ROA (.docx), built from the template by the fixed scripts from answers Paul confirmed, with the client's own reply email embedded for a Retirement or Investment ROA;
    why: Kept as the manual fallback.
- old line 1024: size this fails structurally, not just for large files (full history:
    now: paths += [os.path.join(root, f) for f in sorted(files) if not f.endswith(".pyc")]
    why: Kept as the manual fallback.
- old line 1025: wr-roa-builder-changelog.md, 2026-08-14 entry).
    now: WR ROA Builder — construction script.
    why: Kept as the manual fallback.
- old line 1026: Build and audit the ROA as normal (.docx, per the standard pipeline above), save
    now: the data assembled for build_roa.py, the reference number and the file name.
    why: Kept as the manual fallback.
- old line 1027: it to /mnt/user-data/outputs/ with the required delivery filename, and share it
    now: """Build the required delivery filename:
    why: Kept as the manual fallback.
- old line 1029: Tell the user plainly that this session's upload tool can't carry the file, and
    now: Your reply to Paul is the saved file's name and folder, the .docx, and that audit, as they are.
    why: Kept as the manual fallback.
- old line 1030: give them the exact destination folder so they can drag it in themselves.
    now: If no route can carry a .docx, give it to Paul in the chat and name the folder to drop it in.
    why: Kept as the manual fallback.
- old line 1031: A small plain-text test file (e.g.
    now: # sentence near the bottom is a plain-text mail-merge field on the same binding,
    why: Kept as the manual fallback.
- old line 1031: a one-line _permission_test.txt, deleted
    now: one line per check with a green tick or a red
    why: Kept as the manual fallback.
- old line 1032: immediately after) is fine for confirming write *permissions* are granted — that's
    now: Your reply to Paul is the saved file's name and folder, the .docx, and that audit, as they are.
    why: Kept as the manual fallback.
- old line 1033: a different question from whether the transfer mechanism can carry a real
    now: a different document, and the ROA needs both), fact_find_summary.
    why: Kept as the manual fallback.
- old line 1034: document, and in this path, it can't, at any size.
    now: """Remove any direct-child run in this paragraph that is a bare <w:tab/>, and
    why: Kept as the manual fallback.
- old line 1038: references/dropdown_field_map.md — full verified dropdown option lists for every
    now: dropdown_field_map.md lists every dropdown option.
    why: The program picks the paragraph (Paul's answer 3).
- old line 1039: field in the template, including the 81-item master product list.
    now: across all insurers (full list in "Master Product List" below)
    why: The program picks the paragraph (Paul's answer 3).
- old line 1041: references/roa_data_schema.md — the exact data shape scripts/build_roa.py
    now: See references/roa_data_schema.md in the skill for the full data shape.
    why: The program picks the paragraph (Paul's answer 3).
- old line 1042: expects, plus the validate/render commands to run before delivering.
    now: View the .docx yourself before delivering.")
    why: The program picks the paragraph (Paul's answer 3).
- old line 1044: references/WR_Risk_Cover_Responses_24_07_26.docx — the response bank for the risk
    now: BANK = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "references", "WR_Risk_Cover_Responses_24_07_26.docx")
    why: The program picks the paragraph (Paul's answer 3).
- old line 1045: bundle's reason-text paragraphs (Life, Disability, Dread, Income Protection — each
    now: Lump Sum Disability and Income Protection (1st 24 months) must be given:
    why: The program picks the paragraph (Paul's answer 3).
- old line 1046: with their own FNA-status × Replacement-status scenario list).
    now: new_while_other_replaced true with a NON-REPLACEMENT scenario;
    why: The program picks the paragraph (Paul's answer 3).
- old line 1047: scripts/build_roa.py — the validated construction script.
    now: run.py build <run>                                                            assemble, build the ROA, embed the email pages
    why: The program picks the paragraph (Paul's answer 3).
- old line 1048: removal, Health Care deletion, Death/Dread overrides, amount-field collapsing,
    now: Each product section (except Health Care) has this same field set:
    why: The program picks the paragraph (Paul's answer 3).
- old line 1049: and date rules described above.
    now: Rules are Paul's (the old skill, kept) and his answers of 03/11/2026.
    why: The program picks the paragraph (Paul's answer 3).
- old line 1049: Extend this script (and update this file) rather
    now: it only (1) extracts the text of each page with pdfplumber, and (2) answers "does this figure / date / name
    why: The program picks the paragraph (Paul's answer 3).
- old line 1050: than hand-editing XML for a one-off case.
    now: one line per check with a green tick or a red cross, one closing line for what is only attested",
    why: The program picks the paragraph (Paul's answer 3).
- old line 1051: scripts/embed_email_images.py — second-pass script for Retirement/Investment
    now: run.py email <run> --file email.html [--base-pt N]                            Retirement / Investment:
    why: The program picks the paragraph (Paul's answer 3).
- old line 1052: converts the accepted proposal email PDF to images and embeds them as
    now: """Insert the accepted-proposal email pages (as images) into the Investment
    why: The program picks the paragraph (Paul's answer 3).
- old line 1053: standalone, bordered, keepNext-linked picture+caption pairs after the active
    now: bordered picture paragraphs after the section's data/reason table, never
    why: The program picks the paragraph (Paul's answer 3).
- old line 1054: Run this after build_roa.py, not instead of it.
    now: w.die("Build the ROA first (run.py build).")
    why: The program picks the paragraph (Paul's answer 3).
- old line 1055: assets/ROA_Template_2026.docx — the base ROA template.
    now: build_roa('ROA_Template_2026.docx', 'output.docx', data)
    why: The program picks the paragraph (Paul's answer 3).
- old line 1055: Never build an ROA from
    now: # --- Health Care is never produced as an ROA:
    why: The program picks the paragraph (Paul's answer 3).
- old line 1056: always start from this file.
    now: You do not work from memory of this page:
    why: The program picks the paragraph (Paul's answer 3).
- old line 1057: wr-roa-builder-changelog.md (in the Analyze Skills Project) — the full,
    now: See references/roa_data_schema.md in the skill for the full data shape.
    why: The program picks the paragraph (Paul's answer 3).
- old line 1058: verbatim caught-mistake history behind every "recurring bug" and "non-negotiable"
    now: # 1 one bundle, every other section only heading and reason;
    why: The program picks the paragraph (Paul's answer 3).
- old line 1059: Add any new caught-mistake story there, not back into this file.
    now: add(ia.get("status") == "DO NOT REVIEW" and (ia.get("reason") or [[""]])[0][0] == br.INCOME_AFTER_24_FIXED,
    why: The program picks the paragraph (Paul's answer 3).
- old line 1063: This skill is about the *procedure*.
    now: This skill is a program that walks you through the job one step at a time.
    why: Kept; the rebuilt skill's files hold no client data.
- old line 1063: It doesn't carry any specific client's data —
    now: it must open on the client's own reply.
    why: Kept; the rebuilt skill's files hold no client data.
- old line 1064: each ROA should start from that client's own documents (FNA Quote, Reduced/Accepted
    now: Every answer comes from the client's own documents or from Paul's words and is recorded with its source.
    why: Kept; the rebuilt skill's files hold no client data.
- old line 1065: Quote, Fact Find), located via Step 0 (local machine first, then SharePoint/Outlook) or, failing that,
    now: a Fact Find or KYC PDF read through SharePoint often comes back as field labels with none of the client's answers (the filled-in layer is not extracted).
    why: Kept; the rebuilt skill's files hold no client data.
- old line 1066: uploaded directly into the conversation.
    now: field in assets/ROA_Template_2026.docx, extracted directly from the document's
    why: Kept; the rebuilt skill's files hold no client data.
- old line 1066: If a new client's documents can't be found
    now: A document cannot be found on any of the three routes:
    why: Kept; the rebuilt skill's files hold no client data.
- old line 1067: either way, ask for them via the Step 1 checklist rather than reusing figures or
    now: f"asked for directly rather than defaulted."
    why: Kept; the rebuilt skill's files hold no client data.
- old line 1068: wording from an earlier client in the same chat or from memory of a previous
    now: Every figure comes from the client's actual quote or email, never from a previous client, never estimated.
    why: Kept; the rebuilt skill's files hold no client data.


DROPPED (each is covered by a recorded decision):
- ## Index: Replaced by the new short Index (five sections).
- ## UNIVERSAL OPERATING RULES - READ FIRST, APPLY TO EVERY STEP OF THE : The preamble is replaced by the short intro of references/00-rules.md; the program shows the rules at the start and the right page at each step.
- Re-load this skill before you start, and again after any compression. : Rule 1 (re-load this skill) is replaced by the program: it shows the standing rules at the start and the right page at each step, and `run.py status` tells a chat where the job is up to after a compression.
- Read before you write. Read the source material completely and careful: Rule 3 (read before you write) is replaced by the reading lock: the program serves the documents page by page and each page is acknowledged.
- Deliver everything this skill lists, every time. A run is not finished: Rule 5 (deliver everything) is replaced by deliverables.json and the checker: a run is finished only with a PASS audit.
- Changes to a skill: edit the existing skill, never create a new one. U: Rule 9 (changes through the propose_skills card) is replaced by standard S7: skills are changed only in Claude Code and uploaded as a zip by Paul; the 'never say it is live' part is standing rule 7 in SKILL.md.
- Last updated: 2026-10-13 14:50 (Athens time): The hand-typed stamp, the five-row changelog, the maintenance rule and the skill-saving note are replaced by the stamp program (S2); the full history is in the repo's history folder.
- Path 1's direct SharePoint API upload, even though the destination is : Delivery Path 1 (building the ROA as HTML and pushing it as text) is REMOVED (Paul's answer 5, 03/11/2026): the ROA is always the .docx built from the template. If no route can carry a .docx, it is given to Paul in the chat (Path 2).
