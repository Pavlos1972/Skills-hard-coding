INVENTORY of the old skill: 420 sentences
  kept (word for word or nearly): 10
  reworded, with a recorded change: 204
  dropped, with a recorded decision: 206
  UNACCOUNTED: 0


REWORDED (each is covered by a recorded change):
- old line 55: This skill builds the client-facing proposal email Paul sends after receiving a
    now: This skill builds the client-facing proposal email Paul sends after he has received a Retirement Goal Analysis Report (RGAR) from Alwyn.
    why: Kept.
- old line 56: Retirement Goal Analysis Report (RGAR) from Alwyn.
    now: return "%s / Retirement Goal Analysis Report" % a["client_full_name"].strip()
    why: Kept.
- old line 57: client's shortfall and sets up the next Teams meeting to discuss it.
    now: The email introduces the client's shortfall and sets up the next Teams meeting to discuss it.
    why: Kept.
- old line 58: an HTML file, saved to SharePoint, plus an unsent Outlook draft (client To,
    now: The output is an HTML file, saved to SharePoint, plus an unsent Outlook draft (client To, Sitamah Cc).
    why: Kept.
- old line 60: (unless she can't, or Paul chooses to send it).
    now: Sitamah attaches the RGAR report and emails the client from Drafts (unless she cannot, or Paul chooses to send it).
    why: Kept.
- old line 60: Claude never sends the email itself.
    now: Claude never sends the client email.
    why: Kept.
- old line 62: ## What this skill is not
    now: which version of this skill is running.
    why: Kept in the rules page.
- old line 64: It does not calculate or generate the RGAR itself — that always comes from Alwyn
    now: It does not calculate or generate the RGAR itself:
    why: Kept in the rules page.
- old line 66: It is not the Fact Find Summary skill — that's a separate skill
    now: It is not the Fact Find Summary skill (fact-find-summary), but that skill's output is a required input here.
    why: Kept in the rules page.
- old line 67: (fact-find-summary), but its output is a required input here (see Step 1).
    now: It is not the Fact Find Summary skill (fact-find-summary), but that skill's output is a required input here.
    why: Kept in the rules page.
- old line 69: ## Step 1 — Setup checklist (always ask/collect before building, in this order)
    now: print("\nSAY THIS TO PAUL FIRST, before anything else in your reply, in exactly these words:\n    %s.\n" % w.version_line())
    why: The upload-or-locate and raw-Fact-Find routes are replaced by the standard route order and the Fact Find Summary first (Paul's answer 2); the questions are the table-and-one-question pattern (Paul's answer 4).
- old line 71: Every new RGAR proposal chat should open with these requests, in the order below.
    now: Try the routes IN THIS ORDER and record EVERY try, failures too:",
    why: The upload-or-locate and raw-Fact-Find routes are replaced by the standard route order and the Fact Find Summary first (Paul's answer 2); the questions are the table-and-one-question pattern (Paul's answer 4).
- old line 72: Do not build a partial email — if something below is missing, ask for it and wait.
    now: Do not build until nothing essential is missing.
    why: The upload-or-locate and raw-Fact-Find routes are replaced by the standard route order and the Fact Find Summary first (Paul's answer 2); the questions are the table-and-one-question pattern (Paul's answer 4).
- old line 77: Meeting date(s) already held with the client (one or several) — typed.
    now: The meeting date(s) already held with the client:
    why: The upload-or-locate and raw-Fact-Find routes are replaced by the standard route order and the Fact Find Summary first (Paul's answer 2); the questions are the table-and-one-question pattern (Paul's answer 4).
- old line 78: Collect just the calendar dates (DD/MM/YYYY) — never ask the user for the
    now: """The ways a DD/MM/YYYY date may be printed in the report."""
    why: The upload-or-locate and raw-Fact-Find routes are replaced by the standard route order and the Fact Find Summary first (Paul's answer 2); the questions are the table-and-one-question pattern (Paul's answer 4).
- old line 79: day-of-week, and never trust a day-of-week they type;
    now: never ask for the day of the week and never trust one a person types;
    why: The upload-or-locate and raw-Fact-Find routes are replaced by the standard route order and the Fact Find Summary first (Paul's answer 2); the questions are the table-and-one-question pattern (Paul's answer 4).
- old line 80: a previous hand-typed version of this email labelled
    now: an earlier hand-typed version of this email said "Thursday, 19/02/2022",
    why: The upload-or-locate and raw-Fact-Find routes are replaced by the standard route order and the Fact Find Summary first (Paul's answer 2); the questions are the table-and-one-question pattern (Paul's answer 4).
- old line 81: 19/02/2022 as a "Thursday" when it was actually a Saturday.
    now: the program computes every weekday (a hand-typed email once labelled 19/02/2022 a "Thursday" when it was a Saturday).
    why: The upload-or-locate and raw-Fact-Find routes are replaced by the standard route order and the Fact Find Summary first (Paul's answer 2); the questions are the table-and-one-question pattern (Paul's answer 4).
- old line 82: Next Teams meeting date and time (e.g.
    now: The next Teams meeting date and time (for example 02/07/2026 and 12pm).
    why: The upload-or-locate and raw-Fact-Find routes are replaced by the standard route order and the Fact Find Summary first (Paul's answer 2); the questions are the table-and-one-question pattern (Paul's answer 4).
- old line 82: "Thursday, 02/07/2026 @ 12pm") —
    now: one date   -> "Thursday, 02/07/2026"
    why: The upload-or-locate and raw-Fact-Find routes are replaced by the standard route order and the Fact Find Summary first (Paul's answer 2); the questions are the table-and-one-question pattern (Paul's answer 4).
- old line 83: This drives the shortfall start date (see Step 3), so confirm the date
    now: It drives the shortfall period, so confirm the date even if Paul only says a day name.
    why: The upload-or-locate and raw-Fact-Find routes are replaced by the standard route order and the Fact Find Summary first (Paul's answer 2); the questions are the table-and-one-question pattern (Paul's answer 4).
- old line 84: component even if the user only says a day name.
    now: It drives the shortfall period, so confirm the date even if Paul only says a day name.
    why: The upload-or-locate and raw-Fact-Find routes are replaced by the standard route order and the Fact Find Summary first (Paul's answer 2); the questions are the table-and-one-question pattern (Paul's answer 4).
- old line 85: The RGAR PDF from Alwyn (e.g.
    now: Put a copy of the RGAR PDF from Alwyn in the same folder:
    why: The upload-or-locate and raw-Fact-Find routes are replaced by the standard route order and the Fact Find Summary first (Paul's answer 2); the questions are the table-and-one-question pattern (Paul's answer 4).
- old line 85: "[Client Full Name] - Retirement Goal
    now: you)." % (a["client_full_name"].strip(), a["client_email"].strip()), "",
    why: The upload-or-locate and raw-Fact-Find routes are replaced by the standard route order and the Fact Find Summary first (Paul's answer 2); the questions are the table-and-one-question pattern (Paul's answer 4).
- old line 86: Analysis - 24.06.26.pdf").
    now: return "%s / Retirement Goal Analysis Report" % a["client_full_name"].strip()
    why: The upload-or-locate and raw-Fact-Find routes are replaced by the standard route order and the Fact Find Summary first (Paul's answer 2); the questions are the table-and-one-question pattern (Paul's answer 4).
- old line 86: Upload, or locate it in the client's SharePoint
    now: Claude finds and reads the source documents itself from the client's file on Paul's OneDrive/SharePoint:
    why: The upload-or-locate and raw-Fact-Find routes are replaced by the standard route order and the Fact Find Summary first (Paul's answer 2); the questions are the table-and-one-question pattern (Paul's answer 4).
- old line 87: folder (often under an "(OM RGA)" / RGAR transaction folder > Comparative
    now: often under an "(OM RGA)" / RGA transaction folder > Comparative Quotes, or already in the RA transaction folder.
    why: The upload-or-locate and raw-Fact-Find routes are replaced by the standard route order and the Fact Find Summary first (Paul's answer 2); the questions are the table-and-one-question pattern (Paul's answer 4).
- old line 88: DOB/age check, retirement age, "Current
    now: "DD/MM/YYYY", "retirement_age":
    why: The upload-or-locate and raw-Fact-Find routes are replaced by the standard route order and the Fact Find Summary first (Paul's answer 2); the questions are the table-and-one-question pattern (Paul's answer 4).
- old line 89: value" / "Future value" expenses, Years until retirement, and the shortfall
    now: out.append("years_until_retirement must be a whole number (it drives the shortfall end date)")
    why: The upload-or-locate and raw-Fact-Find routes are replaced by the standard route order and the Fact Find Summary first (Paul's answer 2); the questions are the table-and-one-question pattern (Paul's answer 4).
- old line 90: figures (lump sum, monthly recurring, escalation %, sustainability age).
    now: "net_monthly_target", "lump_sum", "monthly", "escalation", "sustainability_age", "recurring_investment", "employer", "job_title", "gross_monthly_income",
    why: The upload-or-locate and raw-Fact-Find routes are replaced by the standard route order and the Fact Find Summary first (Paul's answer 2); the questions are the table-and-one-question pattern (Paul's answer 4).
- old line 91: The client's Fact Find Summary or raw Fact Find.
    now: # ---- the client's own facts (Fact Find Summary)
    why: The upload-or-locate and raw-Fact-Find routes are replaced by the standard route order and the Fact Find Summary first (Paul's answer 2); the questions are the table-and-one-question pattern (Paul's answer 4).
- old line 91: If the user uploads a
    now: "If a file with the same name exists the program stops:
    why: The upload-or-locate and raw-Fact-Find routes are replaced by the standard route order and the Fact Find Summary first (Paul's answer 2); the questions are the table-and-one-question pattern (Paul's answer 4).
- old line 92: Fact Find Summary (output of the fact-find-summary skill), use it directly.
    now: out.append("client_email is not in the Fact Find Summary's text (email_source says it is)")
    why: The upload-or-locate and raw-Fact-Find routes are replaced by the standard route order and the Fact Find Summary first (Paul's answer 2); the questions are the table-and-one-question pattern (Paul's answer 4).
- old line 93: Otherwise, locate and read the client's raw Fact Find yourself — do not stop
    now: never substitute the nearest document and never read the raw Fact Find instead of the Fact Find Summary.
    why: The upload-or-locate and raw-Fact-Find routes are replaced by the standard route order and the Fact Find Summary first (Paul's answer 2); the questions are the table-and-one-question pattern (Paul's answer 4).
- old line 94: and ask the user to upload something you can go and get.
    now: R.add(False, "The message must go to the 1:1 chat with Sitamah (record message.chat and message.format = markdown)")
    why: The upload-or-locate and raw-Fact-Find routes are replaced by the standard route order and the Fact Find Summary first (Paul's answer 2); the questions are the table-and-one-question pattern (Paul's answer 4).
- old line 95: job title, gross monthly income, the client's full name/first name for the
    now: Employer, job title, gross monthly income, the client's full and first name, the age and the email address (sections "1.
    why: The upload-or-locate and raw-Fact-Find routes are replaced by the standard route order and the Fact Find Summary first (Paul's answer 2); the questions are the table-and-one-question pattern (Paul's answer 4).
- old line 96: greeting, the client's personal email address (the To:
    now: To = the client's email address;
    why: The upload-or-locate and raw-Fact-Find routes are replaced by the standard route order and the Fact Find Summary first (Paul's answer 2); the questions are the table-and-one-question pattern (Paul's answer 4).
- old line 96: recipient), and the net monthly income target — this last one is the "Net
    now: The net monthly income target in today's terms:
    why: The upload-or-locate and raw-Fact-Find routes are replaced by the standard route order and the Fact Find Summary first (Paul's answer 2); the questions are the table-and-one-question pattern (Paul's answer 4).
- old line 97: Amount Needed (today's terms)" field under "6.
    now: ["Net amount needed at retirement", "Net Amount Needed (today's terms)"],
    why: The upload-or-locate and raw-Fact-Find routes are replaced by the standard route order and the Fact Find Summary first (Paul's answer 2); the questions are the table-and-one-question pattern (Paul's answer 4).
- old line 98: "Personal Risk Cover & Retirement" (not the Reduced Quote's monthly
    now: What the Client Requires" > "Personal Risk Cover & Retirement".
    why: The upload-or-locate and raw-Fact-Find routes are replaced by the standard route order and the Fact Find Summary first (Paul's answer 2); the questions are the table-and-one-question pattern (Paul's answer 4).
- old line 220: ## Step 3 — Date calculations (always run the script, never hand-compute)
    now: the date is set by tools/stamp_skill.py, never typed
    why: The script is applied by the program, never by hand.
- old line 222: Use scripts/rgar_dates.py for every date in the email.
    now: the shortfall start and end dates, the weekdays, the Cc (always Sitamah Nathoo) and every RGAR and Fact Find figure are derived.
    why: The script is applied by the program, never by hand.
- old line 223: day-of-week or the shortfall period by hand or from memory of a calendar — it is
    now: Never hand-compute the day-of-week or the shortfall period.
    why: The script is applied by the program, never by hand.
- old line 224: easy to get the day-of-week wrong (this happened in a real Paul email once — see
    now: never ask for the day of the week and never trust one a person types;
    why: The script is applied by the program, never by hand.
- old line 225: the script's self-check).
    now: The program's own check of the built email failed:
    why: The script is applied by the program, never by hand.
- old line 230: sys.path.insert(0, "scripts")
    now: groups.insert(0, whole[-3:])
    why: The script is applied by the program, never by hand.
- old line 231: from rgar_dates import format_meeting_dates_list, format_date_with_day, shortfall_period
    now: formatted = [format_date_with_day(d) for d in dates]
    why: The script is applied by the program, never by hand.
- old line 233: # Opening line's meeting date(s):
    now: out.append("the next meeting date %s is in the past" % nm["date"])
    why: The script is applied by the program, never by hand.
- old line 234: meeting_line = format_meeting_dates_list([date(2026, 6, 24)])  # -> "Wednesday, 24/06/2026"
    now: assert format_date_with_day(date(2026, 7, 2)) == "Thursday, 02/07/2026"
    why: The script is applied by the program, never by hand.
- old line 237: next_meeting = format_date_with_day(date(2026, 7, 2)) + " @ 12pm"
    now: assert format_date_with_day(date(2026, 7, 2)) == "Thursday, 02/07/2026"
    why: The script is applied by the program, never by hand.
- old line 239: # Shortfall coverage period — pass the NEXT meeting date and the RGAR's
    now: def shortfall_period(next_meeting_date:
    why: The script is applied by the program, never by hand.
- old line 244: The shortfall period rule, stated plainly:
    now: *The shortfall period rule (fixed, not reconfirmed per client;
    why: The script is applied by the program, never by hand.
- old line 244: start = the 1st of the month
    now: Start = 1st of the month FOLLOWING the next Teams meeting date.
    why: The script is applied by the program, never by hand.
- old line 245: immediately after the month of the next Teams meeting;
    now: start = the 1st of the month immediately after the month of the next Teams meeting;
    why: The script is applied by the program, never by hand.
- old line 246: month/day, but years_until_retirement years later.
    now: end = the same day and month, years until retirement years later.
    why: The script is applied by the program, never by hand.
- old line 246: This is fixed and not
    now: w.die('This is not a run folder (no %s).
    why: The script is applied by the program, never by hand.
- old line 247: reconfirmed per client — it was explicitly confirmed against a worked example
    now: checked against a worked example):
    why: The script is applied by the program, never by hand.
- old line 248: (next meeting 02/07/2026 + 18 years until retirement → 1 August 2026 to
    now: For example a next meeting on 02/07/2026 and 18 years until retirement give 1 August 2026 to 1 August 2044.
    why: The script is applied by the program, never by hand.
- old line 251: ## Step 4 — Build the email HTML
    now: w.die("Build the email first (run.py build).")
    why: The template is filled by the program, so no placeholder can remain; the table-count-only sanity check is replaced by program checks (Paul's answer 5).
- old line 253: Copy assets/RGAR_Proposal_Email_TEMPLATE.html to the working directory.
    now: TEMPLATE = os.path.join(ASSETS, "RGAR_Proposal_Email_TEMPLATE.html")
    why: The script is applied by the program, never by hand.
- old line 254: Replace every [BRACKETED PLACEHOLDER] with the client's actual values —
    now: the template's sentences are used with the client's figures.
    why: The script is applied by the program, never by hand.
- old line 255: never leave a placeholder in the delivered file.
    now: Never overwrite a file in the client's folder without Paul's clear yes in this chat.
    why: The script is applied by the program, never by hand.
- old line 256: Sitamah Nathoo (always — replaces the
    now: Sitamah Nathoo (admin@liferisk.co.za), always.
    why: The script is applied by the program, never by hand.
- old line 257: [Client Full Name] / Retirement Goal Analysis Report.
    now: return "%s / Retirement Goal Analysis Report" % a["client_full_name"].strip()
    why: The script is applied by the program, never by hand.
- old line 258: R + thousands-comma format + no decimals unless the source
    now: R and a space, thousands commas, no decimals unless the source document shows decimals.
    why: The script is applied by the program, never by hand.
- old line 259: document shows decimals (match the RGAR PDF's own formatting for each figure,
    now: cents only when the source figure showed cents ('match the document's own formatting')."""
    why: The script is applied by the program, never by hand.
- old line 260: "R 1,234,567" not "R 1234567" or "R 1,234,567.00" unless the RGAR itself
    now: It does not calculate or generate the RGAR itself:
    why: The script is applied by the program, never by hand.
- old line 262: The "Attachments:" header line uses the real filename of the RGAR PDF
    now: Attachments = the real file name of the RGAR PDF as saved by Alwyn (never the made-up pattern);
    why: The script is applied by the program, never by hand.
- old line 263: as saved by Alwyn (e.g.
    now: Returns (start_str, end_str) already formatted e.g.
    why: The script is applied by the program, never by hand.
- old line 263: Retirement Goal Analysis - 10.01.26 - [Initial] [Surname].pdf);
    now: return "%s / Retirement Goal Analysis Report" % a["client_full_name"].strip()
    why: The script is applied by the program, never by hand.
- old line 264: only fall back to [Client Full Name] - Retirement Goal Analysis - [DD.MM.YY].pdf
    now: This skill builds the client-facing proposal email Paul sends after he has received a Retirement Goal Analysis Report (RGAR) from Alwyn.
    why: The script is applied by the program, never by hand.
- old line 265: if there is no real file name.
    now: If the HTML is revised, re-save over the same file name only with Paul's yes and tell him.
    why: The script is applied by the program, never by hand.
- old line 269: content = open('output.html').read()
    now: "markdown" and content = the message exactly as printed (an output_hint is required by the tool).
    why: The script is applied by the program, never by hand.
- old line 270: print('tables open/close:', content.count('<table'), content.count('</table>'))
    now: add(h.count("<table") == h.count("</table>"), "Tables open = close in the %s (%d)" % (nm, h.count("<table")))
    why: The script is applied by the program, never by hand.
- old line 273: Save as [FirstName]_[Surname]_RGAR_Proposal_Email - [DD.MM.YY].html
    now: The full email (with the logo), named [FirstName]_[Surname]_RGAR_Proposal_Email - [DD.MM.YY].html (the build date;
    why: The script is applied by the program, never by hand.
- old line 274: (date = today's build date).
    now: elif any(w.parse_date(x) > today for x in mh):
    why: The script is applied by the program, never by hand.
- old line 274: Deliver to Paul via the outputs folder / SendUserFile
    now: print("Name to use in the RA transaction folder's Comparative Quotes:
    why: The script is applied by the program, never by hand.
- old line 275: and tell him plainly it is the HTML copy of what is in his Drafts.
    now: Send it to Paul through the chat and tell him plainly it is the HTML copy of what is in his Drafts.
    why: The script is applied by the program, never by hand.
- old line 277: save to the client's RA transaction folder
    now: The saved (no-logo) copy goes into the client's RA transaction folder > Comparative Quotes:
    why: The save and the RGAR copy are proven by the folder listing.
- old line 279: Every RGAR proposal HTML is saved to SharePoint — never skipped:
    now: Paul's rule is that the proposal email is saved to Drafts, To = the client's email, Cc = Sitamah Nathoo.
    why: The save and the RGAR copy are proven by the folder listing.
- old line 281: the client's folder under Paul/New Business/{Surname, First}/ →
    now: Look first in the client's Paul/New Business/{Surname, First}/ folder:
    why: The save and the RGAR copy are proven by the folder listing.
- old line 282: the RA transaction folder (e.g.
    now: *The RA transaction folder (for the saved copy and the RGAR copy):
    why: The save and the RGAR copy are proven by the folder listing.
- old line 282: {Surname, First} - (OM RA - R[amount])) →
    now: "<the RA transaction folder's name, for example Surname, First - (OM RA - R2000)>",
    why: The save and the RGAR copy are proven by the folder listing.
- old line 283: All RGARs are filed under the RA transaction folder,
    now: All RGARs are filed under the RA transaction folder, not under a separate RGAR folder.
    why: The save and the RGAR copy are proven by the folder listing.
- old line 284: not under a separate RGAR folder.
    now: All RGARs are filed under the RA transaction folder, not under a separate RGAR folder.
    why: The save and the RGAR copy are proven by the folder listing.
- old line 285: The RGAR PDF from Alwyn:
    now: Put a copy of the RGAR PDF from Alwyn in the same folder:
    why: The save and the RGAR copy are proven by the folder listing.
- old line 285: if it sits in an "(OM RGA)" / RGA folder,
    now: "It is in %s's folder:
    why: The save and the RGAR copy are proven by the folder listing.
- old line 286: sharepoint_copy_item a copy into the RA transaction folder's Comparative Quotes
    now: print("Name to use in the RA transaction folder's Comparative Quotes:
    why: The save and the RGAR copy are proven by the folder listing.
- old line 288: if the device bridge/local folder is not available, use
    now: if a local folder from Paul's computer is connected, write the file there;
    why: The save and the RGAR copy are proven by the folder listing.
- old line 289: sharepoint_upload_file (content ≤ 1 MB).
    now: otherwise use sharepoint_upload_file (content up to 1 MB) with the expectedBytes check, which detects truncation.
    why: The save and the RGAR copy are proven by the folder listing.
- old line 289: Use the expectedBytes check — it
    now: "pasted into the reply as it is:
    why: The save and the RGAR copy are proven by the folder listing.
- old line 290: The template carries a very long base64 logo that cannot
    now: The template carries a very long base64 logo that cannot be retyped or uploaded reliably, so the copy saved in the client's folder is ALWAYS the no-logo copy:
    why: The save and the RGAR copy are proven by the folder listing.
- old line 291: in that case upload a no-logo copy (signature table
    now: "Tell Paul in plain words that the saved copy has no logo (the Outlook draft gets Paul's signature and logo separately)."
    why: The save and the RGAR copy are proven by the folder listing.
- old line 292: logo removed) and say so — the Outlook draft takes the logo from Paul's
    now: Tell Paul plainly that the saved copy has no logo (the Outlook draft takes the logo from Paul's Outlook signature).
    why: The save and the RGAR copy are proven by the folder listing.
- old line 294: Confirm the folder listing afterwards (read_resource on the folder).
    now: Confirm by listing the folder afterwards (read_resource on the folder).
    why: The save and the RGAR copy are proven by the folder listing.
- old line 296: ## Step 6 — Outlook draft via Claude in Chrome (never sent by Claude)
    now: "The Outlook draft (never sent by Claude)",
    why: The read-back is checked by the program.
- old line 298: the proposal email is saved to Drafts, To = client email,
    now: Paul's rule is that the proposal email is saved to Drafts, To = the client's email, Cc = Sitamah Nathoo.
    why: The read-back is checked by the program.
- old line 301: Create the draft shell with outlook_create_draft:
    now: (1) create the draft shell with the Outlook connector's outlook_create_draft (to, cc, subject, a placeholder body such as BODY_PLACEHOLDER):
    why: The script is applied by the program, never by hand.
- old line 302: Cc = admin@liferisk.co.za (Sitamah Nathoo), subject exactly as in the HTML
    now: CC_EMAIL = "admin@liferisk.co.za"
    why: The script is applied by the program, never by hand.
- old line 303: header, body = a placeholder word such as BODY_PLACEHOLDER.
    now: (1) create the draft shell with the Outlook connector's outlook_create_draft (to, cc, subject, a placeholder body such as BODY_PLACEHOLDER):
    why: The script is applied by the program, never by hand.
- old line 304: are set reliably this way;
    now: insert (the setting today, this skill's way):
    why: The script is applied by the program, never by hand.
- old line 304: typing into the compose fields by coordinates
    now: Do not type into Outlook's compose fields by coordinates:
    why: The script is applied by the program, never by hand.
- old line 306: Open OWA in Chrome (new tab via tabs_context_mcp → tabs_create_mcp):
    now: "Make the Outlook draft with Claude in Chrome (never sent by Claude) and read it back for the program",
    why: The script is applied by the program, never by hand.
- old line 307: navigate to https://outlook.office365.com/mail/ first and wait, *then*
    now: go to outlook.office365.com/mail/ first, wait, then the draft's webLink and wait about 8 seconds:
    why: The script is applied by the program, never by hand.
- old line 308: navigate to the draft's webLink and wait ~8 s (going straight to the deep
    now: go to outlook.office365.com/mail/ first, wait, then the draft's webLink and wait about 8 seconds:
    why: The script is applied by the program, never by hand.
- old line 309: link returns a "browser-internal URL" error).
    now: going straight to the deep link returns a "browser-internal URL" error;
    why: The script is applied by the program, never by hand.
- old line 309: Click the edit pencil (≈ top right
    now: click the edit pencil, roughly top right of the read view, to open compose:
    why: The script is applied by the program, never by hand.
- old line 310: of the read view) to open compose — "Continue editing" can leave it in read view.
    now: "Continue editing" can leave it in read view);
    why: The script is applied by the program, never by hand.
- old line 311: run JS on [aria-label="Message body"] that selects all
    now: %s is not the figure that follows its label (%s) in the Fact Find Summary:
    why: The script is applied by the program, never by hand.
- old line 312: and dispatches a ClipboardEvent('paste') with text/html (the email body
    now: The text to paste is the draft_body.html the program built.
    why: The script is applied by the program, never by hand.
- old line 313: only — from "Dear {First name}," to the bold next-meeting line;
    now: everything from "Dear {First name}," to the bold next-meeting line:
    why: The script is applied by the program, never by hand.
- old line 314: header table, no template signature, no "Kind regards").
    now: no header, no signature block, no 'Kind regards,', no logo" % a["client_first_name"].strip())
    why: The script is applied by the program, never by hand.
- old line 315: <p style="font-size:12pt;margin:0;"> </p> between paragraphs and use
    now: <p style="font-size:12pt;margin:0;">Hoping the above is in order.</p>
    why: The script is applied by the program, never by hand.
- old line 316: <b> for bold (Paul's blank-line spacing preference).
    now: no header block, no template signature, no "Kind regards,", <b> not font-weight, a blank line between paragraphs (Paul's blank-line spacing preference).
    why: The script is applied by the program, never by hand.
- old line 317: click at the end of the body, then Insert > Signature >
    now: Then put a copy of the RGAR PDF in the same folder (sharepoint_copy_item with destinationParentItemId;
    why: The script is applied by the program, never by hand.
- old line 318: It supplies "Kind regards,", the logo and the disclaimer —
    now: no header, no signature block, no 'Kind regards,', no logo" % a["client_first_name"].strip())
    why: The script is applied by the program, never by hand.
- old line 319: confirm there is exactly one "Kind regards,".
    now: includes its own "Kind regards," line) -->
    why: The script is applied by the program, never by hand.
- old line 320: Don't trust aria-pressed;
    now: t = str(value).replace("%", "").strip().replace(" ", "")
    why: The script is applied by the program, never by hand.
- old line 322: Never press Ctrl+S (it inserts a Loop component).
    now: Do not press Ctrl+S in the compose window (it can insert a stray Loop component);
    why: The script is applied by the program, never by hand.
- old line 324: Verify with read_resource on mail:///messages/{id}:
    now: read_resource on mail:///messages/{id} (the result is large:
    why: The script is applied by the program, never by hand.
- old line 325: email, Cc = Sitamah Nathoo, subject correct, body text/figures match the
    now: the shortfall start and end dates, the weekdays, the Cc (always Sitamah Nathoo) and every RGAR and Fact Find figure are derived.
    why: The script is applied by the program, never by hand.
- old line 326: HTML, single signature with logo (inline image), importance:
    now: no header, no signature block, no 'Kind regards,', no logo" % a["client_first_name"].strip())
    why: The script is applied by the program, never by hand.
- old line 327: Loop component, no BODY_PLACEHOLDER.
    now: add(not re.search(r"\bLoop\b", flat), "No Loop component is in the draft")
    why: The script is applied by the program, never by hand.
- old line 328: Close the Chrome tab you opened;
    now: never through Claude in Chrome / Teams web, and not the native teams_send_chat_message (it fails:
    why: The script is applied by the program, never by hand.
- old line 328: delete any stray drafts with
    now: delete any stray blank drafts Claude itself created while doing this (outlook_delete_draft) and say so;
    why: The script is applied by the program, never by hand.
- old line 329: The draft is left unsent — Sitamah attaches the
    now: "left in Drafts for Sitamah to review, attach the three documents and send",
    why: The script is applied by the program, never by hand.
- old line 330: RGAR report and sends it (Step 7).
    now: Sitamah attaches the report and sends.
    why: The script is applied by the program, never by hand.
- old line 332: ## Step 7 — Teams message to Sitamah (always;
    now: "The Teams message to Sitamah",
    why: The wording and greeting are the program's; the message is sent only after Paul's yes and a checked draft (Paul's answer 1).
- old line 336: Greeting — check first, never repeat.
    now: "The Outlook draft (never sent by Claude)",
    why: The wording and greeting are the program's; the message is sent only after Paul's yes and a checked draft (Paul's answer 1).
- old line 336: Read today's earlier messages in the 1:1 chat (read_resource on teams:///chats/{chatId}/messages) and check real SAST time (TZ=Africa/Johannesburg date).
    now: "the message went to the 1:1 chat as markdown and its read-back passes every program check"
    why: The wording and greeting are the program's; the message is sent only after Paul's yes and a checked draft (Paul's answer 1).
- old line 336: Use a time-appropriate greeting:
    now: shows ONE step at a time, refuses to skip, keeps the run on disk.
    why: The wording and greeting are the program's; the message is sent only after Paul's yes and a checked draft (Paul's answer 1).
- old line 336: "Good morning Sitamah," before 12:00 SAST, "Good afternoon Sitamah," 12:00–17:59, "Good evening Sitamah," after.
    now: "Good morning Sitamah," before 12:00, "Good afternoon Sitamah," from 12:00 to 17:59, "Good evening Sitamah," after (South African time, set by the program from the clock).
    why: The wording and greeting are the program's; the message is sent only after Paul's yes and a checked draft (Paul's answer 1).
- old line 336: If a greeting of that kind was already sent that day (by Paul or Claude), do not repeat it — use a different, neutral greeting instead ("Hi Sitamah," or "Hey Sitamah,").
    now: "Look in the 1:1 chat for whether the same time-of-day greeting was already used today by Paul or Claude, then run:
    why: The wording and greeting are the program's; the message is sent only after Paul's yes and a checked draft (Paul's answer 1).
- old line 336: Never open every message the same way.
    now: "the message went to the 1:1 chat as markdown and its read-back passes every program check"
    why: The wording and greeting are the program's; the message is sent only after Paul's yes and a checked draft (Paul's answer 1).
- old line 338: Standard wording and format — fixed layout, only the client/product details change;
    now: assets/settings.json and assets/net_target_labels.json hold the two things Paul may change later.
    why: The wording and greeting are the program's; the message is sent only after Paul's yes and a checked draft (Paul's answer 1).
- old line 338: real Teams formatting (bold "Action needed:" and "Drafts", numbered list), never raw HTML tags or markdown symbols, no emojis:
    now: greeting, bold labels, numbered list, no raw tags (%d checks)" % len(res), ";
    why: The wording and greeting are the program's; the message is sent only after Paul's yes and a checked draft (Paul's answer 1).
- old line 343: The RGAR report ({RGAR file name without .pdf})
    now: The RGAR report (%s)" % rgar_name_no_ext(docs), "",
    why: The wording and greeting are the program's; the message is sent only after Paul's yes and a checked draft (Paul's answer 1).
- old line 345: > It is in {Client}'s folder:
    now: "It is in %s's folder:
    why: The wording and greeting are the program's; the message is sent only after Paul's yes and a checked draft (Paul's answer 1).
- old line 345: {RA transaction folder name} > Comparative Quotes.
    now: print("Name to use in the RA transaction folder's Comparative Quotes:
    why: The wording and greeting are the program's; the message is sent only after Paul's yes and a checked draft (Paul's answer 1).
- old line 348: Do not add "please do not send it", "leave it in Drafts" or "let me know once attached" lines.
    now: Never add "please do not send it", "leave it in Drafts" or "let me know once attached" lines, unless Paul has said he will send that particular email himself (then he tells you how to change the last 
    why: The wording and greeting are the program's; the message is sent only after Paul's yes and a checked draft (Paul's answer 1).
- old line 358: ## Step 8 — Pre-delivery audit
    now: The last step prints the SHORT AUDIT.
    why: The audit is done by the program.
- old line 360: Before calling the work finished, check every item:
    now: Any red cross means the job is not finished:
    why: The audit is done by the program.
- old line 362: No [BRACKETED PLACEHOLDER] text remains anywhere in the output.
    now: add(not PLACEHOLDER.search(h) and "@@" not in h, "No [PLACEHOLDER] text is left in the %s" % nm)
    why: The script is applied by the program, never by hand.
- old line 363: Every meeting date (opening line and next-meeting line) shows a
    now: ("Next Teams meeting", next_line(a), s.get("next_meeting")),
    why: The script is applied by the program, never by hand.
- old line 364: *computed day-of-week, not one the user typed or one copied from a
    now: Always trust the computed day, not a typed one.
    why: The script is applied by the program, never by hand.
- old line 366: The shortfall start/end dates were produced by shortfall_period(), not
    now: Weekdays and the shortfall dates are computed by the program, never typed.
    why: The script is applied by the program, never by hand.
- old line 367: estimated — re-run the script and diff if there's any doubt.
    now: """Save the chat's read-back next to the run, check it, and record the result."""
    why: The script is applied by the program, never by hand.
- old line 368: The four shortfall figures (lump sum, monthly, escalation %, sustainability
    now: the RGAR shows a lump sum or a monthly contribution of R 0:
    why: The script is applied by the program, never by hand.
- old line 369: age) match the RGAR PDF's "WHAT YOU HAVE AGREED TO DO AND WHY" section
    now: From "WHAT YOU HAVE AGREED TO DO AND WHY" (page 2):
    why: The script is applied by the program, never by hand.
- old line 370: exactly — recheck against the PDF, not against what was typed into an
    now: Always trust the computed day, not a typed one.
    why: The script is applied by the program, never by hand.
- old line 371: earlier draft in this same conversation.
    now: an earlier hand-typed version of this email said "Thursday, 19/02/2022",
    why: The script is applied by the program, never by hand.
- old line 372: The recreated shortfall paragraph is formatted text, not a pasted image.
    now: The recreated shortfall text is formatted text, not an image;
    why: The script is applied by the program, never by hand.
- old line 373: Personal circumstances (employer, job title, gross income, net monthly
    now: for k in ("gross_monthly_income", "net_monthly_target"):
    why: The script is applied by the program, never by hand.
- old line 374: income target, client name) trace to the Fact Find Summary or the raw Fact
    now: never substitute the nearest document and never read the raw Fact Find instead of the Fact Find Summary.
    why: The script is applied by the program, never by hand.
- old line 375: Find you read directly (via OneDrive if SharePoint text extraction failed —
    now: run.py read <run> [--ack ROLE:PAGE --note TEXT]                 the documents' text, one page at a time
    why: The script is applied by the program, never by hand.
- old line 376: see Step 2) — not to a guess, an assumed tax rate applied to the gross
    now: never derive it from the gross expense figure by assuming a tax rate, never leave it blank silently.
    why: The script is applied by the program, never by hand.
- old line 377: figure, or a previous client's data.
    now: Never round or approximate, and never take a figure from a previous client's covering email.
    why: The script is applied by the program, never by hand.
- old line 378: Header fields are filled in:
    now: pages are acknowledged in order.
    why: The script is applied by the program, never by hand.
- old line 378: To = client email (never invent one;
    now: Claude never sends the client email.
    why: The script is applied by the program, never by hand.
- old line 379: a placeholder only if genuinely unknown), Cc = Sitamah Nathoo (always),
    now: Never invent one (mark it a placeholder only if genuinely unknown, and then the run cannot finish).
    why: The script is applied by the program, never by hand.
- old line 380: Subject = {Client} / Retirement Goal Analysis Report, Attachments = the
    now: return "%s / Retirement Goal Analysis Report" % a["client_full_name"].strip()
    why: The script is applied by the program, never by hand.
- old line 382: Signature block, WR logo, and disclaimer footer in the HTML file are
    now: "Send the full copy (with the logo) to Paul in the chat with the exact file name the program gives."
    why: The script is applied by the program, never by hand.
- old line 383: unchanged from the template (Step 4 never edits these).
    now: ## What comes from the RGAR (never asked)
    why: The script is applied by the program, never by hand.
- old line 384: match Paul's confirmed ground-truth signature exactly (Verdana font;
    now: both keep Paul's signature block")
    why: The script is applied by the program, never by hand.
- old line 387: logo 473×169px) — if it doesn't,
    now: Raises ValueError if it is not a readable PDF."""
    why: The script is applied by the program, never by hand.
- old line 388: the template asset has drifted and needs re-pulling from source (see
    now: Every figure, name, date and address comes from the client's own RGAR and Fact Find Summary or Paul's words, with its source;
    why: The script is applied by the program, never by hand.
- old line 389: Reference material below), not hand-patching in this conversation.
    now: "Find the documents the page below lists in the client's own folders.
    why: The script is applied by the program, never by hand.
- old line 390: The file was saved with the correct filename convention, saved to the
    now: (3) the HTML was sent to Paul in the chat with its exact file name;
    why: The script is applied by the program, never by hand.
- old line 391: client's RA transaction folder > Comparative Quotes, and the RGAR PDF is
    now: print("Name to use in the RA transaction folder's Comparative Quotes:
    why: The script is applied by the program, never by hand.
- old line 393: The Outlook draft exists in Drafts, verified (To, Cc Sitamah, subject, body,
    now: Paul's rule is that the proposal email is saved to Drafts, To = the client's email, Cc = Sitamah Nathoo.
    why: The script is applied by the program, never by hand.
- old line 394: one signature with logo, High importance), and was not sent by Claude.
    now: "Make the Outlook draft with Claude in Chrome (never sent by Claude) and read it back for the program",
    why: The script is applied by the program, never by hand.
- old line 395: Sitamah was messaged on Teams via Chrome with real formatting, and the posted message was seen rendering correctly (no raw HTML tags), with the standard wording (Step 7) — greeting
    now: "Message Sitamah on Teams through Zapier (the wording is the program's) and read the posted message back",
    why: The script is applied by the program, never by hand.
- old line 396: not already used that day, RGAR report listed, folder named, ending "Once
    now: """Roles still not registered (the RGAR report and the Fact Find Summary can never be missing)."""
    why: The script is applied by the program, never by hand.
- old line 397: attached, please email the client - Thank you!" (no "do not send" line).
    now: "It ends 'Once attached, please email the client - Thank you!' with no 'do not send' line")
    why: The script is applied by the program, never by hand.
- old line 398: The final message to Paul flags:
    now: # The final reply to Paul
    why: The script is applied by the program, never by hand.
- old line 398: RGAR recurring investment R 0 / mismatch
    now: The recurring investment the RGAR assumes:
    why: The script is applied by the program, never by hand.
- old line 399: with the proposed RA, any figure not traceable to the raw Fact Find, a
    now: any figure not traceable to the Fact Find Summary, conflicts between Fact Find Summary versions, a no-logo SharePoint copy, anything assumed (for example which client).
    why: The script is applied by the program, never by hand.
- old line 400: no-logo SharePoint copy, and anything assumed (e.g.
    now: any figure not traceable to the Fact Find Summary, conflicts between Fact Find Summary versions, a no-logo SharePoint copy, anything assumed (for example which client).
    why: The script is applied by the program, never by hand.
- old line 404: assets/RGAR_Proposal_Email_TEMPLATE.html — the fixed email template
    now: "The RGAR proposal email (.html), built from the fixed template",
    why: The script is applied by the program, never by hand.
- old line 405: (header, opening, personal circumstances, recreated shortfall text, closing,
    now: These four values are recreated as formatted text in the email:
    why: The script is applied by the program, never by hand.
- old line 406: Paul's signature block with embedded WR logo, and the standard confidentiality
    now: "Tell Paul in plain words that the saved copy has no logo (the Outlook draft gets Paul's signature and logo separately)."
    why: The script is applied by the program, never by hand.
- old line 407: Only the bracketed placeholders change between clients — the
    now: # ---- the programs must not change during a run
    why: The script is applied by the program, never by hand.
- old line 408: surrounding copy and styling are fixed and were sourced directly from a real
    now: add("<strong>Action needed:</strong>" in flat and "<strong>Drafts</strong>" in flat, "'Action needed:' and 'Drafts' are bold (real <strong> tags)")
    why: The script is applied by the program, never by hand.
- old line 409: The signature block (from the <!-- SIGNATURE
    now: "The RGAR proposal email (.html), built from the fixed template",
    why: The script is applied by the program, never by hand.
- old line 410: -> comment to the closing </table> just before it) is pulled verbatim
    now: Never say the skill is "live" before Paul confirms he uploaded it.
    why: The script is applied by the program, never by hand.
- old line 411: from Paul's own ground-truth signature file —
    now: if a local folder from Paul's computer is connected, write the file there;
    why: The script is applied by the program, never by hand.
- old line 412: liferisk.co.za\Company - Paul\Email Signature\Paul Kafentzis Signature.html
    now: the Exchange rule of paul-email-signature adds the signature at send time and Claude inserts nothing.
    why: The script is applied by the program, never by hand.
- old line 413: on his OneDrive (a mirror of his real Outlook signature at
    now: (2) open the draft in Outlook on the web with Claude in Chrome (a new tab;
    why: The script is applied by the program, never by hand.
- old line 414: AppData\Roaming\Microsoft\Signatures\Paul K New (paulk@liferisk.co.za).htm)
    now: text-decoration:underline;">paulk@liferisk.co.za</a>
    why: The script is applied by the program, never by hand.
- old line 415: — not from the om-optimal-ra-proposal skill's asset, which was found on
    now: It was found on that day that the om-optimal-ra-proposal asset held an older, visually different copy.
    why: The script is applied by the program, never by hand.
- old line 416: 2026-09-25 to be an older, visually different copy (wrong font, wrong
    now: It was found on that day that the om-optimal-ra-proposal asset held an older, visually different copy.
    why: The script is applied by the program, never by hand.
- old line 417: colors, wrong logo format/size).
    now: the saved copy is the no-logo copy;
    why: The script is applied by the program, never by hand.
- old line 417: If Paul ever updates his real signature,
    now: If Paul ever updates his real signature, re-pull it from that file and re-splice it into the template:
    why: The script is applied by the program, never by hand.
- old line 418: re-pull it from that OneDrive file (or the AppData original) and re-splice
    now: If Paul ever updates his real signature, re-pull it from that file and re-splice it into the template:
    why: The script is applied by the program, never by hand.
- old line 419: it into this template rather than editing the colors/fonts by hand.
    now: *Fixed by the template and the program
    why: The script is applied by the program, never by hand.
- old line 420: scripts/rgar_dates.py — the validated date-math helper (day-of-week,
    now: out.append("rgar_dob %r is not a date (DD/MM/YYYY, as the RGAR's date of birth)" % a.get("rgar_dob"))
    why: The script is applied by the program, never by hand.
- old line 421: meeting-date list formatting, shortfall period calculation).
    now: start, end = shortfall_period(date(2026, 7, 2), 18)
    why: The script is applied by the program, never by hand.
- old line 422: and use this rather than reasoning about calendars manually.
    now: (6) let it autosave (wait about 8 seconds) and confirm.
    why: The script is applied by the program, never by hand.
- old line 423: directly (python3 rgar_dates.py) re-runs its self-checks, including the
    now: python3 {scripts}/run.py messagecheck {run} --file <the saved read-back>"
    why: The script is applied by the program, never by hand.
- old line 424: worked example from this skill's design conversation.
    now: # Self-check against the worked example from the training conversation:
    why: The script is applied by the program, never by hand.
- old line 428: This skill is about the *procedure*, not any specific client's data.
    now: %s is not in the document's text" % (label, w.fmt_money(d))
    why: Kept.
- old line 429: proposal should start fresh from that client's own RGAR PDF and Fact
    now: Every figure, name, date and address comes from the client's own RGAR and Fact Find Summary or Paul's words, with its source;
    why: Kept.
- old line 430: Find Summary in that conversation — never reused or inferred from a previous
    now: Never round or approximate, and never take a figure from a previous client's covering email.
    why: Kept.
- old line 431: client's figures or a prior session's memory.
    now: Never invent, never reuse another client's figures.
    why: Kept.


DROPPED (each is covered by a recorded decision):
- Universal operating rules | Nine rules that apply to every step, and t: The preamble is replaced by the short intro of references/00-rules.md; the program shows the rules at the start and the right page at each step.
- Last updated, standing rule, changelog | Athens stamp, the edit rule, : The hand-typed stamp, the maintenance rule and the changelog are replaced by the stamp program (S2); the full history is in the repo's history folder.
- Interaction format: use the button-selection tool for any question wit: The 'use the button-selection tool for fixed-option questions' line is kept in references/02-answers.md (reworded: none is expected now).
- contribution target in the same table — that's a different figure). Se: The pointer to the raw Fact Find section, the flag 'whether you used a Fact Find Summary or read the raw Fact Find directly' and the caveat about a net amount that comes only from Paul's request to Alwyn are REPLACED (Paul, 03/11/2026, answer 2): the Fact Find Summary is the only source and the net target must follow its label. The warning that the Reduced Quote's contribution target is a different figure is kept (references/02-answers.md).  [NEEDS PAUL]
- "Reading the raw Fact Find — go straight to OneDrive" below for how to: The whole 'Reading the raw Fact Find: go straight to OneDrive' section is REPLACED (Paul, 03/11/2026, answer 2): the 8:45am laptop window was already dropped on 02/11/2026; the device-bridge visual read of the raw fillable Fact Find is no longer used because the Fact Find Summary (made by program, with a readable text layer) is the source; with no Fact Find Summary the skill stops and asks Paul. Three routes, every try logged, replace the single bridge route.  [NEEDS PAUL]
- Run the structural sanity check before presenting:: The structural sanity check (a one-line python test that only counted tables) is REPLACED by the program's checks of the built email: no [PLACEHOLDER] in the full copy, the saved copy and the pasted body, tables open = close, the header, the weekdays, every figure.  [NEEDS PAUL]
- After the draft is verified, send Sitamah the Teams message below thro: The paragraph that sends the Sitamah message through Teams in Chrome and warns that Zapier posts plain text is REPLACED (Paul, 03/11/2026, answer 1): the Tax-Free skill found on 13/10/2026 that Zapier with format markdown renders real bold and a real numbered list, and Paul's standing rule is Teams through Zapier only. What stays: Sitamah sends the proposal email herself, never tell her to leave it in Drafts for Paul unless Paul says so, Claude never sends the client email, the native tool lacks the scope (references/05-message.md).  [NEEDS PAUL]
- 3. How to send — formatting method (Claude in Chrome on Teams web):: The Chrome-on-Teams-web typing method (ctrl+b, shift+Return, the stray numbered item, the zoom check) is REPLACED by the Zapier markdown send and the program's read-back check (references/05-message.md); the rules to read the posted message back before saying it is sent, only delete a message Claude itself posted and only when Paul asked for a redo are kept there.  [NEEDS PAUL]
