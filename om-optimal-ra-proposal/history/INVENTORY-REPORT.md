INVENTORY of the old skill: 834 sentences
  kept (word for word or nearly): 24
  reworded, with a recorded change: 605
  dropped, with a recorded decision: 205
  UNACCOUNTED: 0


REWORDED (each is covered by a recorded change):
- old line 27: Write only what is in the source material (transcript, quote, document, file) or in a named document this skill tells you to use.
    now: Write only what is in the client's own documents or in Paul's own words (recorded with the words).
    why: Kept.
- old line 27: If a line is unclear, garbled or ambiguous, do not turn it into a fact:
    now: If a line is unclear, garbled or ambiguous, flag it to Paul instead of turning it into a fact.
    why: Kept.
- old line 27: flag it to the user.
    now: flag it if the RGAR shows anything else.
    why: Kept.
- old line 28: Read the source material completely and carefully - at least as many times as this skill requires - before drafting anything.
    now: R.add(True, "Sitamah's message went to the 1:1 chat as markdown and was read back:
    why: Kept.
- old line 29: Never tell the user something is done, saved, sent, visible or working until you have checked it yourself (open the file, list the folder, look at the screen).
    now: """(all the strings of a saved read-back joined, the parsed object or None, the list of strings)."""
    why: Kept.
- old line 30: Deliver everything this skill lists, every time.
    now: which version of this skill is running.
    why: Kept.
- old line 30: A run is not finished until every deliverable this skill names has been produced AND handed over exactly the way this skill specifies (shown in chat, sent as a file in the chat, saved to the named fol
    now: "out/[FirstName]_[Surname]_OM_Optimal_RA_Proposal_Email - DD.MM.YY.html (with logo, sent to Paul in the chat) and out/saved/<same name> (no logo, saved in the RA transaction folder's Comparative Quote
    why: Kept.
- old line 30: Before you reply, list each deliverable and confirm each was handed over.
    now: Your reply to Paul is where the copy was saved, the draft's status, that Sitamah was messaged, the flags, and that audit, as they are.
    why: Kept.
- old line 31: Every correction re-opens the whole task, not just the item.
    now: A correction from Paul re-opens the task:
    why: Kept.
- old line 31: When the user corrects anything:
    now: amp="&amp;" when the result goes into HTML."""
    why: Kept.
- old line 31: (a) go back to the source and re-check that point and everything related to it;
    now: """Save the chat's read-back next to the run, check it, and record the result."""
    why: Kept.
- old line 31: (b) fix it everywhere it appears, in every deliverable;
    now: Fix it in Outlook (never send it), read it back again and run this again.
    why: Kept.
- old line 31: (c) re-run this skill's full checklist;
    now: insert (the setting today, this skill's way):
    why: Kept.
- old line 31: (d) re-deliver every affected deliverable in full, as in rule 5.
    now: print("EVERY STEP IS DONE.\nPut this SHORT AUDIT in your reply, as it is (nothing longer):\n")
    why: Kept.
- old line 31: Never fix only the item named and stop.
    now: The program checks the proof and only then shows the next step.
    why: Kept.
- old line 32: A correction, a frustrated user, a short request or a "quick" task does not relax any rule in this skill.
    now: a correction, a frustrated user, a short request or a "quick" task relaxes no rule here.
    why: Kept.
- old line 33: If a rule cannot be met, stop and say so.
    now: If a rule cannot be met, stop and say exactly which and why.
    why: Kept.
- old line 33: State exactly which rule or step could not be completed and why.
    now: if not isinstance(fe, dict) or set(fe) != {"admin_fee", "advice_fee", "as_and_when"}:
    why: Kept.
- old line 33: Never hand over partial work as if it were complete.
    now: Never hand over partial work as complete.
    why: Kept.
- old line 36: *Delivery gate for this skill (rules 5 and 6 applied):
    now: Changes to this skill are made only in Claude Code and uploaded by Paul.
    why: Proved by the checker.
- old line 36: a run is complete only when ALL of these are done and confirmed in one line each:
    now: A run is finished only when ALL of these are done and the program's final audit has no red cross:
    why: Proved by the checker.
- old line 36: (1) the startup checklist, source reading and Tax Reform Tool were completed (Steps 1-3);
    now: (1) the documents were found and read, the questions only Paul can answer were asked, not inferred (the startup checklist), and the Tax Reform Tool was run by the program;
    why: Proved by the checker.
- old line 36: (2) the proposal HTML was built and the Step 7 mandatory pre-delivery audit was completed;
    now: (2) the proposal email was built and the program's checks and the old audit passed;
    why: Proved by the checker.
- old line 36: (3) the HTML was sent in the chat with the exact required filename;
    now: (3) the HTML was sent to Paul in the chat with its exact file name;
    why: Proved by the checker.
- old line 36: (4) Step 8a (saved into the client's folder), Step 8b (Outlook draft, never sent by Claude) and Step 8c (Teams message to Sitamah, sent via Zapier) were each done and checked;
    now: The Outlook draft (never sent by Claude), read back and checked by the program, and the Teams message to Sitamah (through Zapier, after Paul's one yes and a checked draft), read back and checked.
    why: Proved by the checker.
- old line 36: (5) where a lump sum applies, (2) to (4) were repeated for the separate Lump Sum Investment proposal.
    now: (5) where a lump sum applies, (2) to (4) were repeated for the separate Lump Sum Investment email (a second run).
    why: Proved by the checker.
- old line 53: This skill packages Paul Kafentzis's proposal-building process for Old Mutual Optimal Retirement Annuity (OM Optimal RA) client emails.
    now: This skill builds the client-facing proposal emails for an Old Mutual Optimal Retirement Annuity (OM Optimal RA) for Paul Kafentzis (FSP45946), after Alwyn's OM Optimal RA Quote is back.
    why: Kept.
- old line 53: These are client-facing financial documents — precision matters more than speed.
    now: R.add(good, "The client's documents are registered (%s), unchanged;
    why: Kept.
- old line 53: A wrong figure or an inconsistent sentence is a real-world error in front of a client, not a cosmetic slip.
    now: add(not miss, "Every figure and fixed sentence of the email is there as the rules phrase it" if not miss else "Missing from the email:
    why: Kept.
- old line 53: The output is an HTML file that is (a) saved into the client's folder, (b) put into an Outlook draft by Claude, and (c) flagged to Sitamah on Teams so she can attach the 4 documents and email the clie
    now: (4) the no-logo copy was saved in the RA transaction folder's Comparative Quotes, the Outlook draft was made and read back, and Sitamah was messaged on Teams via Zapier and the posted message read bac
    why: Kept.
- old line 53: Claude never sends the email to the client itself — Sitamah sends it from Drafts once the documents are attached (unless she can't, or Paul chooses to send it).
    now: The message asks her to attach the documents to the draft and email the client (Sitamah sends the proposal email herself once she has attached them).
    why: Kept.
- old line 57: Every proposal follows the same three-table tax logic, the same HTML template, and the same client-scenario wording rules — but each client's underlying numbers are different, and it's easy to acciden
    now: Never rewrite, shorten or "improve" a program, the workbook or the template during a run, and never type a figure from memory, a tax figure, a weekday, a file name or the Teams message.
    why: Kept; enforced by the program.
- old line 57: This skill exists so that discipline travels with Claude automatically, in any chat, without Paul having to re-explain it or manually clear out old client files first.
    now: Never overwrite a file in the client's folder without Paul's clear yes in this chat.
    why: Kept; enforced by the program.
- old line 59: ## Step 1 — Always run the startup checklist first
    now: run.py done <run> STEP                                          prove the step, then show the next one
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 61: Before building anything, confirm all 12 items below are available.
    now: rows.append((True, "python module pdfplumber is available"))
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 61: If any are missing, ask for them and wait — do not build a partial proposal.
    now: Do not build a partial email:
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 63: Client Fact Find (personal details, age, employer, position, start date, gross income, retirement goal, risk profile)
    now: personal details, age, employer, position, start date, gross income, retirement goal, risk profile, the personal email address.
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 64: Astute CCP Report or existing policy schedules (or confirmation there are none)
    now: "Astute CCP report or the policy schedules", "client_overview":
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 65: Pension/Provident Fund Statement (or confirmation there is none)
    now: "Pension / Provident Fund statement", "poi":
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 66: Proof of Income (POI) / Payslip
    now: "Proof of income / payslip", "rgar":
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 67: RGAR PDF from Alwyn (or confirmation none was requested)
    now: "RGAR report (from Alwyn)", "lump_sum_quote":
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 68: OM Optimal RA Quote from Alwyn
    now: "OM Optimal RA Quote (Plan 1)", "fact_find_summary":
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 69: Date(s) of Teams meeting(s) already held with the client
    now: add(("Teams Meeting on %s," % o.meetings_line(a)) in bt, "The meetings already held read '%s', the weekdays computed" % o.meetings_line(a))
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 70: Date, day and time of the next scheduled Teams meeting
    now: return "%s @ %s" % (fmt_date_with_day(next_date(a)), a["next_meeting"]["time"].strip())
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 71: Is the client's existing RA being replaced by the new OM Optimal RA, or kept in force alongside it?
    now: This skill builds the client-facing proposal emails for an Old Mutual Optimal Retirement Annuity (OM Optimal RA) for Paul Kafentzis (FSP45946), after Alwyn's OM Optimal RA Quote is back.
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 71: (Not applicable if the client has no existing RA.)
    now: out.append("the client has existing RAs:
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 72: Confirmation that all current RAs (active/paid-up) have been uploaded, or a statement that there are none.
    now: "You have no active or Paid-Up Retirement Annuities.",
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 73: Lump Sum Investment — broken into four sub-questions:
    now: "The separate Lump Sum Investment email (.html), only when a lump sum applies",
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 73: (a) will a lump sum be going into the new OM Optimal RA, in addition to the recurring premium (Yes/No)?
    now: "A lump sum amount of R {amount} will be transferred into your new OM Optimal RA via a Section 14 transfer from your existing {sources} policy/policies.
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 73: (b) if Yes, is it a Section 14 transfer or voluntary funds?
    now: exactly one of the two approved sentences (Section 14 transfer, or voluntary funds), never paraphrased;
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 73: (c) if Section 14 — which policy/policies and the Net Fund Value;
    now: Needed for a Section 14 lump sum (the NET fund values).
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 73: if voluntary — source of funds and Rand amount;
    now: if set(lp) != {"type", "amount", "source_of_funds", "tax_note"}:
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 73: (d) upload the separate OM Lump Sum Quote (Plan 2).
    now: lump_sum_quote | The separate OM Lump Sum Quote (Plan 2) from Alwyn.
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 73: If (a) is No, (b)–(d) don't apply.
    now: if nxt is None or a.ack != "%s:%d" % nxt:
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 74: Client Overview document showing the "Current Investments" section — gross fund value, penalties, net fund value and monthly premium for each existing policy at a glance.
    now: gross fund value, penalties, net fund value and monthly premium of each existing policy at a glance.
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 76: Questions 9, 10, 11 and 12 are mandatory and must be answered before any proposal is built — they are not optional even if the other items are complete.
    now: If several versions are on file, use the most recent, list the others and ask Paul if there is doubt.
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 76: Question 9's answer drives the Recommendation wording, the structure of Table 3, and whether the penalty note applies.
    now: "Message Sitamah on Teams through Zapier (the wording is the program's) and read the posted message back",
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 76: Question 11a's answer determines whether a second, separate HTML document (the Lump Sum Investment proposal) needs to be built alongside the main proposal — see Step 6b and references/mcd_v6_3.md Sect
    now: checks on the tool's results, the two emails built from the fixed templates (the main proposal and the separate Lump Sum Investment proposal), the Teams message to
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 78: ## Step 2 — Read the source documents carefully
    now: "Read the registered documents, one page at a time",
    why: Reading is locked by the program.
- old line 80: Read the Fact Find, CCP report, fund statement, POI, RGAR, and Quote directly — don't assume values.
    now: ("astute_ccp", "client_overview", "fund_statement", "poi", "rgar"), "lump_sum":
    why: Reading is locked by the program.
- old line 81: If a Fact Find or other PDF has scanned/image pages, visually read the page images rather than relying only on extracted text — text layers often capture field labels but miss the client's actual fill
    now: "Find the documents the page below lists in the client's own folders.
    why: Reading is locked by the program.
- old line 82: Fund selection, fees, ACI, and premium amounts always come from the specific client's quote — never assume they match a previous client's proposal, even if similar.
    now: Fund selection, fees, the ACI and premium amounts always come from THIS client's quote, never from a previous client's proposal, even if similar.
    why: Reading is locked by the program.
- old line 84: ## Step 3 — Run the Tax Reform Tool (three scenarios)
    now: """The Tax Reform Tool, run by the program:
    why: The tool is run by the program, never by hand.
- old line 88: B35 = annual remuneration + (employer fund contributions × 12)
    now: Calcs!C15 is the binding allowance = MIN(R430,000, 27.5% x Calcs!B35), where Calcs!B35 = annual remuneration + the employer fund contributions (a fringe benefit added back).
    why: The tool is run by the program, never by hand.
- old line 89: C15 = MIN(R430,000, 27.5% × B35) — the binding SARS allowance
    now: The tax cap is R 430,000 and 27.5%.
    why: The tool is run by the program, never by hand.
- old line 91: [MAXIMUM RA CONTRIBUTION] = (C15 − total annual fund contributions) ÷ 12 — used in Table 1's savings-opportunity row and as the Table 2 RA input
    now: Table 2, the full deduction | [MAXIMUM RA CONTRIBUTION] = (cap - the yearly fund contributions) / 12 | one new OM Optimal RA row;
    why: The tool is run by the program, never by hand.
- old line 93: If the client has no Pension/Provident Fund, or fund contributions are excluded from this proposal, select "Self Employed" in the tool (write directly to Calcs!B2) so all fund-contribution rows zero o
    now: pension fund, provident fund, or self-employed / no fund (an existing RA does not change the wording).
    why: The tool is run by the program, never by hand.
- old line 93: Never touch the VBA radio button controls with openpyxl — edit the underlying xlsm zip/XML directly if a value needs to change, since disturbing the radio buttons breaks the workbook.
    now: (1) create the draft shell with the Outlook connector's outlook_create_draft (to, cc, subject, a placeholder body such as BODY_PLACEHOLDER):
    why: The tool is run by the program, never by hand.
- old line 95: To force full recalculation and read results reliably:
    now: """Save the chat's read-back next to the run, check it, and record the result."""
    why: The tool is run by the program, never by hand.
- old line 95: convert headless with LibreOffice (soffice --headless --calc --convert-to xlsx) and then read output cells with openpyxl (data_only=True).
    now: r = subprocess.run([soffice, "--headless", "-env:UserInstallation=file://" + profile, "--calc", "--convert-to", "xlsx", "--outdir", out, src],
    why: The tool is run by the program, never by hand.
- old line 95: Cells on the Maximise Allowance Tool sheet (corrected 01/10/2026 against the actual workbook — the previous mapping was wrong):
    now: SHEET, CALCS, REINVEST = "Maximise Allowance Tool", "Calcs", "Reinvest Calcs"
    why: The tool is run by the program, never by hand.
- old line 95: inputs C15 (monthly remuneration), C17 (age), C20–C23 (fund contributions — set to 0 when the client has no Pension/Provident Fund), C24 (monthly RA);
    now: C15 monthly remuneration (the gross monthly income), C17 age, C20 to C23 the employer and member pension and provident contributions as a share of the remuneration, C24 the monthly RA.
    why: The tool is run by the program, never by hand.
- old line 95: outputs C28 = annual tax saved from RA, C29 = tax saved from pension, C30 = tax saved from provident, C31 = annual tax payable after deductions and rebate, C34 = % deduction left, C36 = additional mon
    now: C28 annual tax saved from the RA deduction, C29 pension, C30 provident, C31 annual tax payable after deductions and rebate, C34 maximum deduction left to use, C36 additional monthly premium, C37 once-
    why: The tool is run by the program, never by hand.
- old line 95: Reinvest Calcs H41:Q41 gives the bar chart values for years 1–10;
    now: Reinvest Calcs!H41:Q41 are the ten bar values (the RA escalating at 10%).
    why: The tool is run by the program, never by hand.
- old line 95: Calcs!C15 is the cap.
    now: the remuneration input and, as Calcs!C15, the cap.)
    why: The tool is run by the program, never by hand.
- old line 95: Always read the label next to a cell before trusting a mapping.
    now: """Save the chat's read-back next to the run, check it, and record the result."""
    why: The tool is run by the program, never by hand.
- old line 97: A client with no Pension/Provident Fund and no existing RA is handled by leaving C20–C23 at 0 (Table 1:
    now: A client with BOTH a pension and a provident fund:
    why: The tool is run by the program, never by hand.
- old line 97: RA = R–, tax saved R–;
    now: tax saved from the RA", "R %s;
    why: The tool is run by the program, never by hand.
- old line 97: pension row removed from all three tables).
    now: Pension and provident rows appear in all three tables;
    why: The tool is run by the program, never by hand.
- old line 99: Run this three times per client — once per table scenario (Table 1:
    now: """Run the scenarios (identical ones once).
    why: The tool is run by the program, never by hand.
- old line 99: RA=0 / current situation, Table 2:
    now: <!-- YOUR CURRENT SITUATION — TABLE 1 -->
    why: The tool is run by the program, never by hand.
- old line 99: RA=proposed premium) — and keep the outputs straight;
    now: Table 3, what is proposed | the proposed premium (replace), or the existing total + the proposed premium (keep) | replace:
    why: The tool is run by the program, never by hand.
- old line 99: mixing them up is the single easiest mistake to make.
    now: print("\nTHE ONE QUESTION TO PAUL (show the whole table in the reply, then ask exactly this):\n    Are these answers right, so that I build %s for %s, save the copy, make the Outlook draft "
    why: The tool is run by the program, never by hand.
- old line 101: ## Step 4 — The three-table logic (read this carefully — it is the part most likely to go wrong)
    now: The three-table logic is fixed:
    why: The table logic is enforced by the program.
- old line 103: Table | Shows | RA row(s) |
    now: 6 Table 2's fund rows + RA row = [TOTAL CAP MONTHLY];
    why: The table logic is enforced by the program.
- old line 105: Table 1 — current situation | The client's exact position today.
    now: <!-- YOUR CURRENT SITUATION — TABLE 1 -->
    why: The table logic is enforced by the program.
- old line 105: | Pension/Provident row(s) if applicable, plus one named row per existing RA showing its current contribution.
    now: pension fund, provident fund, or self-employed / no fund (an existing RA does not change the wording).
    why: The table logic is enforced by the program.
- old line 105: Tax saved on existing RA contributions must be shown as a real number — never R– unless the client truly has no RA and no fund.
    now: flags.append("The client has an existing RA but the tool shows no tax saved from it in Table 1 (the income may be below the tax threshold).")
    why: The table logic is enforced by the program.
- old line 106: Table 2 — full tax deduction opportunity | The maximum 27.5% SARS room, using only the new OM Optimal RA.
    now: Table 2, the full deduction | [MAXIMUM RA CONTRIBUTION] = (cap - the yearly fund contributions) / 12 | one new OM Optimal RA row;
    why: The table logic is enforced by the program.
- old line 106: | Pension/Provident row(s) if applicable, plus a single new OM Optimal RA row = [MAXIMUM RA CONTRIBUTION].
    now: "A lump sum amount of R {amount} will be invested into your new OM Optimal RA from your own savings ({source}).",
    why: The table logic is enforced by the program.
- old line 106: Existing RA rows never appear here, regardless of the client's situation.
    now: existing_ras is [] when the client has none (then ra_decision is none);
    why: The table logic is enforced by the program.
- old line 107: Table 3 — what's being proposed | The proposed new OM Optimal RA premium, structured by the Question 9 answer.
    now: Table 3, what is proposed | the proposed premium (replace), or the existing total + the proposed premium (keep) | replace:
    why: The table logic is enforced by the program.
- old line 107: Pension/Provident row(s) if applicable, plus a single new OM Optimal RA row only.
    now: "A lump sum amount of R {amount} will be invested into your new OM Optimal RA from your own savings ({source}).",
    why: The table logic is enforced by the program.
- old line 107: Pension/Provident row(s) if applicable, plus the existing RA row(s), plus the new OM Optimal RA row — combined tax saving shown.
    now: pension fund, provident fund, or self-employed / no fund (an existing RA does not change the wording).
    why: The table logic is enforced by the program.
- old line 109: Pension/Provident rows are identical in amount across all three tables — only the RA line(s) change.
    now: Pension and provident rows appear in all three tables;
    why: The table logic is enforced by the program.
- old line 109: Use the label "Provident Fund Deduction" for provident-fund clients and "Pension Fund Deduction" for pension-fund clients — never mix them up.
    now: The label is "Provident Fund" for a provident client and "Pension Fund" for a pension client, never mixed;
    why: The table logic is enforced by the program.
- old line 111: ## Step 5 — The "what you can save" sentence
    now: no tax tables, bar chart or "what you can save" sentence;
    why: The template defects found 01/10/2026 are fixed in the template.
- old line 113: Always uses [TOTAL CAP MONTHLY] (C15 ÷ 12) — never the remaining RA room alone.
    now: The "what you can save" sentence always uses [TOTAL CAP MONTHLY] (never the remaining RA room), in the wording of the client's scenario:
    why: The template defects found 01/10/2026 are fixed in the template.
- old line 113: Pick the sentence variant matching the client's actual retirement-vehicle combination (Provident only, Pension only, both, existing RA + fund, or self-employed/no fund).
    now: pension fund, provident fund, or self-employed / no fund (an existing RA does not change the wording).
    why: The template defects found 01/10/2026 are fixed in the template.
- old line 113: See references/mcd_v6_3.md Section 8.5 for the exact wording of each variant — copy it verbatim and only substitute the figure and vehicle names.
    now: it only (1) extracts the text of each page with pdfplumber, and (2) answers "does this figure / date / name
    why: The template defects found 01/10/2026 are fixed in the template.
- old line 115: *Template defects to override (found 01/10/2026):
    now: "The 2026/27 SARS tables the Tax Reform Tool holds (Paul's skill, 14/10/2026).
    why: The template defects found 01/10/2026 are fixed in the template.
- old line 115: the template's static text for "What you can save" and "You will be working…" is stale.
    now: the 'what you can save' sentence is missing or not the scenario's wording")
    why: The template defects found 01/10/2026 are fixed in the template.
- old line 115: Always use the MCD Section 8.5 variant sentence for the client's scenario and the wording "You are working at [employer]…".
    now: the 'what you can save' sentence is missing or not the scenario's wording")
    why: The template defects found 01/10/2026 are fixed in the template.
- old line 115: When the client has no Pension/Provident Fund, remove the pension/provident tax row from all three tables (do not leave an empty row).
    now: The pension or provident rows appear in all three tables, identical in amount;
    why: The template defects found 01/10/2026 are fixed in the template.
- old line 115: Table row label for the new RA in Tables 2 and 3:
    now: The table row label of the new RA:
    why: The template defects found 01/10/2026 are fixed in the template.
- old line 117: ## Step 6a — Populate the main proposal (always built)
    now: """The step driver of the om-optimal-ra-proposal skill:
    why: Filled by the program, checked by the program.
- old line 119: Use assets/OM_Optimal_RA_Proposal_TEMPLATE.html as the base for every proposal — never build the HTML from scratch.
    now: os.path.join(ASSETS, "OM_Optimal_RA_Proposal_TEMPLATE.html"), "lump_sum":
    why: Filled by the program, checked by the program.
- old line 119: It's a fully table-based, Outlook-compatible layout:
    now: The layout is fully table-based and Outlook-compatible (bgcolor on every cell, nowrap on value cells, spacer rows, no flexbox, grid or divs).
    why: Filled by the program, checked by the program.
- old line 119: keep bgcolor= attributes on every cell, nowrap on value cells, table-row spacers instead of CSS margins, and don't introduce flexbox, CSS grid, or <div>-based layout.
    now: The layout is fully table-based and Outlook-compatible (bgcolor on every cell, nowrap on value cells, spacer rows, no flexbox, grid or divs).
    why: Filled by the program, checked by the program.
- old line 121: This template covers the recurring monthly premium (Plan 1) only.
    now: OM_Optimal_RA_Proposal_TEMPLATE.html (the recurring premium, Plan 1, only) and OM_Optimal_RA_LumpSum_Proposal_TEMPLATE.html (the lump sum, Plan 2, only).
    why: Filled by the program, checked by the program.
- old line 121: As of MCD V6.3 it contains no lump sum content at all — the old [LUMP_SUM_BLOCK]/[LUMP_SUM_FUND_FEE_BLOCK] placeholders were removed from this template in the V6.3 restructure.
    now: items = ["The OM Optimal RA Lump Sum Quote (%s)" % o.no_ext(o.doc_name(docs, "lump_sum_quote")), "The relevant fund fact sheet(s) as per the Lump Sum Quote (%s)" % fact_sheet_names(a)]
    why: Filled by the program, checked by the program.
- old line 121: Do not add lump sum wording here even if Question 11a is Yes — that goes in the separate document built in Step 6b.
    now: %s\n" % (rj["client"], "the main RA proposal" if document == "main" else "the separate Lump Sum Investment proposal"))
    why: Filled by the program, checked by the program.
- old line 123: Fixed rules that never change between clients:
    now: # What the program builds, and the rules that never change
    why: Filled by the program, checked by the program.
- old line 126: Transaction admin fee is always R300.
    now: The transaction admin charge is always R 300.00.
    why: Filled by the program, checked by the program.
- old line 127: Personal circumstances wording is always "You are working at [employer]..." — never "You will be working."
    now: "You are working at [employer] in the position of [position]." (never "You will be working").
    why: Filled by the program, checked by the program.
- old line 129: Font should match the surrounding body text — do not colour populated fields orange;
    now: Font matches the surrounding body text.
    why: Filled by the program, checked by the program.
- old line 129: To be determined if there are" line is deliberately orange per MCD Section 7.1 — a distinct styling convention from populated client data fields, which stay black.)
    now: "The lump sum is R %s, %s" % (o.money_shown(lp["amount"]), "from the named source policies (Section 14)" if lp["type"] == "section14" else "from the client's own savings"))
    why: Filled by the program, checked by the program.
- old line 131: Conditional wording (use exactly, when the underlying fact applies):
    now: Find this skill's folder (the "Base directory" shown when the skill loaded;
    why: Filled by the program, checked by the program.
- old line 132: No existing RAs → "You have no active or Paid-Up Retirement Annuities."
    now: "You have no active or Paid-Up Retirement Annuities.",
    why: Filled by the program, checked by the program.
- old line 133: No Pension/Provident Fund → "You have no Pension or Provident Fund with your employer."
    now: "You have no Pension or Provident Fund with your employer.",
    why: Filled by the program, checked by the program.
- old line 134: No RGAR requested → "You did not request for a Retirement Goal Analysis Report."
    now: "You did not request for a Retirement Goal Analysis Report.",
    why: Filled by the program, checked by the program.
- old line 136: *The RGAR is never listed as an attachment on the OM Optimal RA Proposal email — this is a permanent rule, not a per-client judgment call.
    now: The RGAR is never an attachment of this email.
    why: Filled by the program, checked by the program.
- old line 136: The attachments list under "Please see attached:" always stays at exactly the 4 standard items (RA Quote, Fund Fact Sheets, RA Booster Value, Wealth Investment Strategy Summary), regardless of whether
    now: The attachments list is always exactly the 4 standard items (RA Quote, Fund Fact Sheets, RA Booster Value, Wealth Investment Strategy Summary), whether or not an RGAR was requested;
    why: Filled by the program, checked by the program.
- old line 136: The RGAR is sent to the client separately, on its own, via the rgar-skill — never bundled as attachment #5 here.
    now: The RGAR is sent to the client in a separate email before this proposal (by rgar-skill);
    why: Filled by the program, checked by the program.
- old line 136: Do not add an RGAR line to this list under any circumstance.
    now: The RGAR is never an attachment of this email.
    why: Filled by the program, checked by the program.
- old line 138: Placeholder notes worth double-checking:
    now: PLACEHOLDER = re.compile(r"\[[A-Z][A-Z0-9 _%().,/&#-]*\]")
    why: Filled by the program, checked by the program.
- old line 139: italic "No penalties apply – policy is too new" if applicable, otherwise blank.
    now: no_penalties must be true or false (true only on Paul's word that the policy is too new for penalties)" % r["policy_number"])
    why: Filled by the program, checked by the program.
- old line 140: always the single new-RA row — see Step 4.
    now: the new RA row only;
    why: Filled by the program, checked by the program.
- old line 141: depends on replace vs keep — see Step 4.
    now: if dec not in ("none", "replace", "keep") or (dec == "none") != (not ras):
    why: Filled by the program, checked by the program.
- old line 142: Pension/Provident block for Table 1 — omit entirely (leave blank) if the client has no Pension/Provident Fund.
    now: python3 {scripts}/run.py doc {run} --missing ROLE --said \"Paul's words\" (for example 'the client has no pension fund').
    why: Filled by the program, checked by the program.
- old line 143: the Personal Retirement Savings narrative block — see conditional wording above.
    now: <p style="font-size:12pt;font-weight:bold;margin:0;">Personal Retirement Savings:</p>
    why: Filled by the program, checked by the program.
- old line 144: [T1 PCT REMAINING] and [T3 PCT REMAINING] each appear twice in the template — replace both instances.
    now: R.add(done == STEP_IDS[:-1] and fpok, "Every step done in order (%d of %d) and the programs, the template and the tax facts did not change during the run" % (len(done), len(STEP_IDS) - 1) if done == S
    why: Filled by the program, checked by the program.
- old line 145: [T1 LUMP SUM] / [T3 LUMP SUM]:
    now: o.rand_cell(t1o["lump_sum"]), "[T1 MESSAGE]":
    why: Filled by the program, checked by the program.
- old line 145: NOT related to Question 11 — these are the Tax Reform Tool's own "once-off lump sum to maximise deduction" output cells (C36), present on every proposal regardless of whether an actual Section 14/volu
    now: Table 2 fund rows R %s + RA row R %s = [TOTAL CAP MONTHLY] R %s, and the tool shows 0%% left, no extra premium and no extra lump sum (the fixed lines of Table 2 are true)" %
    why: Filled by the program, checked by the program.
- old line 147: The full placeholder-to-source mapping is in references/mcd_v6_3.md, Section 5.3 — check it if a placeholder's source is unclear.
    now: "The lump sum is R %s, %s" % (o.money_shown(lp["amount"]), "from the named source policies (Section 14)" if lp["type"] == "section14" else "from the client's own savings"))
    why: Filled by the program, checked by the program.
- old line 149: ## Step 6b — Build the Lump Sum Investment proposal (only if Startup Question 11a is Yes)
    now: the Lump Sum Investment proposal for %s (R %s, %s);
    why: Built by the program.
- old line 151: *Governance decision (V6.3, superseding the single-email approach in V6.0–V6.2):
    now: "left in Drafts for Sitamah to attach the documents and email the client",
    why: Built by the program.
- old line 151: whenever a lump sum applies, produce a second, separate HTML document — never a section bolted onto the main proposal.
    now: "If the lump sum applies (the answers say so), start a SECOND run for the separate Lump Sum Investment email:
    why: Built by the program.
- old line 153: Use assets/OM_Optimal_RA_LumpSum_Proposal_TEMPLATE.html as the base.
    now: os.path.join(ASSETS, "OM_Optimal_RA_LumpSum_Proposal_TEMPLATE.html")}
    why: Built by the program.
- old line 153: This document covers the lump sum (Plan 2) only:
    now: lump_sum_quote | The separate OM Lump Sum Quote (Plan 2) from Alwyn.
    why: Built by the program.
- old line 154: Heading is always "Your Lump Sum Investment:"
    now: heading "Your Lump Sum Investment:";
    why: Built by the program.
- old line 155: Contains NO tax tables, no bar chart, and no "what you can save" sentence — those belong only in the main proposal, since the lump sum has no bearing on the 27.5%/R430,000 annual deduction calculation
    now: no tax tables, bar chart or "what you can save" sentence;
    why: Built by the program.
- old line 156: Shares the same signature block, adviser contact details, and branding as the main proposal.
    now: add(not miss, "The draft carries the client's name, the dates and every figure as the email phrases it" if not miss else "Missing from the draft:
    why: Built by the program.
- old line 157: Both documents should be sent together (or in close succession) as two separate emails, each with their own attachment set.
    now: Both emails go out separately, each with its own draft and Teams message.
    why: Built by the program.
- old line 159: Use exactly one of these two verbatim wordings — never paraphrase (there is no "no lump sum" variant here;
    now: exactly one of the two approved sentences (Section 14 transfer, or voluntary funds), never paraphrased;
    why: Built by the program.
- old line 159: if Question 11a is No, simply don't build this document at all):
    now: "NOLABEL" = no label was found in the text at all
    why: Built by the program.
- old line 160: Section 14 transfer → "A lump sum amount of R [LUMP SUM AMOUNT] will be transferred into your new OM Optimal RA via a Section 14 transfer from your existing [SOURCE POLICY NAME(S)] policy/policies.
    now: "A lump sum amount of R {amount} will be transferred into your new OM Optimal RA via a Section 14 transfer from your existing {sources} policy/policies.
    why: Built by the program.
- old line 161: Voluntary funds → "A lump sum amount of R [LUMP SUM AMOUNT] will be invested into your new OM Optimal RA from your own savings ([SOURCE OF FUNDS])."
    now: "A lump sum amount of R {amount} will be invested into your new OM Optimal RA from your own savings ({source}).",
    why: Built by the program.
- old line 163: [LUMP SUM AMOUNT] is always the Net Fund Value (never Gross) of the transferring polic(y/ies) — sum them if there's more than one, and name each policy.
    now: For Section 14 the amount is the sum of the source policies' NET fund values (never gross), each policy named.
    why: Built by the program.
- old line 163: Old Mutual quotes the lump sum as a separate Plan 2 under the same contract number as the recurring premium (Plan 1);
    now: lump_sum_quote | The separate OM Lump Sum Quote (Plan 2) from Alwyn.
    why: Built by the program.
- old line 163: Alwyn issues a separate Lump Sum Quote for it — read its fund selection, allocation and fees independently via [LS_FUND_FEE_BLOCK], never assume they match Plan 1.
    now: for the lump sum email, the Lump Sum Quote and its fund fact sheet(s).
    why: Built by the program.
- old line 163: A lump sum (Section 14 or voluntary) never counts toward the 27.5%/R430,000 annual deduction limit and is never added to the Tax Reform Tool's contribution inputs used for the main proposal.
    now: A lump sum (Section 14 or voluntary) never counts toward the 27.5% / R430,000 limit and is never added to the Tax Reform Tool's inputs.
    why: Built by the program.
- old line 165: Other placeholders in this template:
    now: Other messages in the chat that carried no greeting do NOT remove the greeting.
    why: Built by the program.
- old line 165: [LS_TAX_TREATMENT_NOTE] (tax-neutral confirmation for Section 14, or a flag-to-adviser note for voluntary funds — see MCD Section 6.5.2), [PRODUCT START DATE] (Plan 2 start date from the Lump Sum Quot
    now: out.append("start_date must be DD/MM/YYYY (the Plan 2 start date in the Lump Sum Quote)")
    why: Built by the program.
- old line 167: references/mcd_v6_3.md Sections 6.5, 6.5.1–6.5.5, and 10.3.
    now: "Paul's approved sentences, verbatim from the old skill (SKILL.md and the Master Context Document V6.3, sections 6.1 to 6.5 and 8.5).
    why: Built by the program.
- old line 169: ## Step 7 — Mandatory pre-delivery audit
    now: step '%s' is missing its proof:" % a.step)
    why: Proved by the checker.
- old line 171: Before calling anything finished, verify all of the following (from MCD Section 8.6):
    now: A run is finished only when ALL of these are done and the program's final audit has no red cross:
    why: Proved by the checker.
- old line 173: [TOTAL CAP MONTHLY] = C15 ÷ 12, traceable to the Tax Reform Tool
    now: [TOTAL CAP MONTHLY] = cap / 12 (used only in the "what you can save" sentence).
    why: Proved by the checker.
- old line 174: [MAXIMUM RA CONTRIBUTION] = (C15 − total annual fund contributions) ÷ 12
    now: Table 2, the full deduction | [MAXIMUM RA CONTRIBUTION] = (cap - the yearly fund contributions) / 12 | one new OM Optimal RA row;
    why: Proved by the checker.
- old line 175: Table 1, 2 and 3 tax-payable figures all genuinely differ from each other
    now: 3 the tax payable of Tables 1, 2 and 3 all differ;
    why: Proved by the checker.
- old line 176: Table 2 tax saved (RA) = Table 1 tax payable − Table 2 tax payable
    now: Table %s tax saved from the RA is R %s and Table 1 tax payable minus Table %s tax payable is R %s%s" %
    why: Proved by the checker.
- old line 177: Table 3 tax saved (RA) = Table 1 tax payable − Table 3 tax payable
    now: Table %s tax saved from the RA is R %s and Table 1 tax payable minus Table %s tax payable is R %s%s" %
    why: Proved by the checker.
- old line 178: Table 2's Pension/Provident rows + RA row monthly total = [TOTAL CAP MONTHLY]
    now: 6 Table 2's fund rows + RA row = [TOTAL CAP MONTHLY];
    why: Proved by the checker.
- old line 179: Table 3's % remaining = (C15 − Table 3 total annual contributions) ÷ C15 × 100
    now: [TOTAL CAP MONTHLY] R %s = the tool's cap (Calcs!C15, R %s) divided by 12, and the cap equals MIN(R 430,000, 27.5%% of the annual remuneration plus the employer contributions)" %
    why: Proved by the checker.
- old line 180: Bar chart Year 1 saving = Table 3's RA tax saving
    now: 8 the bar chart's year 1 = Table 3's tax saved from the RA;
    why: Proved by the checker.
- old line 181: The "what you can save" sentence uses [TOTAL CAP MONTHLY] with the correct scenario wording
    now: 9 the "what you can save" sentence carries [TOTAL CAP MONTHLY] in the right scenario wording.
    why: Proved by the checker.
- old line 182: No placeholder tags [LIKE THIS] remain.
    now: rows.append((ok, "the template carries every placeholder and marker the program fills"))
    why: Proved by the checker.
- old line 182: The header "To:" is the client's real email address (never invented) and "Cc:" is always "Sitamah Nathoo" — never blank.
    now: To = the client's email, Cc = Sitamah Nathoo.
    why: Proved by the checker.
- old line 183: The HTML is saved in the client's RA Comparative Quotes folder and the upload was confirmed (Step 8a);
    now: record the save tries in order, the folder (the RA transaction folder, then Comparative Quotes) and the listed size (%d bytes)" % size)
    why: Proved by the checker.
- old line 183: the Outlook draft exists with To = client, Cc = Sitamah, subject identical to the HTML, bold headings and bordered tables, a single "Kind regards,", signature/logo present, importance High, not sent b
    now: R.add(True, "The Outlook draft was read back and passed all %d checks (To the client, Cc Sitamah, exact subject, High importance, tables open = close, 'Kind regards,' %s, no placeholder, no Loop, ever
    why: Proved by the checker.
- old line 184: Sitamah was messaged on Teams via Zapier and the posted message was read back and confirmed to render correctly (no raw HTML tags, no literal ):
    now: (4) the no-logo copy was saved in the RA transaction folder's Comparative Quotes, the Outlook draft was made and read back, and Sitamah was messaged on Teams via Zapier and the posted message read bac
    why: Proved by the checker.
- old line 184: it opens with a greeting ("Good morning/afternoon/evening Sitamah," by SAST time — see Step 8c), standard wording, the 4 attachments listed (never the RGAR), folder named, ending "Once attached, pleas
    now: %s" % (i, x) for i, x in enumerate(items, 1)] + ["", where, "", "Once attached, please email the client - Thank you!"]
    why: Proved by the checker.
- old line 186: If any check fails, fix it before delivering — don't flag it and hand it over half-checked (except the known edge case below, which is flagged, not forced).
    now: 4 and 5 are computed and, when the two figures differ, flagged to Paul with BOTH figures, never forced (the known edge case:
    why: Proved by the checker.
- old line 188: *Known edge case (checks 4 & 5):
    now: the known edge case, flagged to Paul, not forced)"))
    why: Proved by the checker.
- old line 188: these can legitimately fail to hold exactly, or even go negative, in a "keep some, replace some" scenario where the proposed RA total is close to or lower than the client's current combined RA contrib
    now: The "what you can save" sentence always uses [TOTAL CAP MONTHLY] (never the remaining RA room), in the wording of the client's scenario:
    why: Proved by the checker.
- old line 188: It also appears at the maximum-contribution table when the extra deduction straddles a tax bracket (seen 01/10/2026:
    now: it can differ from a difference of payables when the extra deduction straddles a tax bracket or in a keep-some-replace-some case);
    why: Proved by the checker.
- old line 188: native tax saved R[amount] versus a R[amount] payable difference;
    now: Table %s tax saved from the RA is R %s and Table 1 tax payable minus Table %s tax payable is R %s%s" %
    why: Proved by the checker.
- old line 188: native R[amount] versus R[amount]).
    now: out.append("lump.amount %r is not an amount" % lp.get("amount"))
    why: Proved by the checker.
- old line 188: This is not a calculation error — flag it to Paul as a finding rather than forcing the figures to reconcile artificially.
    now: Your reply to Paul is where the copy was saved, the draft's status, that Sitamah was messaged, the flags, and that audit, as they are.
    why: Proved by the checker.
- old line 188: Always use the Tax Reform Tool's own native output cells for "tax saved" rather than back-calculating from the payable difference.
    now: Always use the tool's own native "tax saved" cells, never back-calculate them.
    why: Proved by the checker.
- old line 192: Deliver the finished HTML to Paul in the chat (SendUserFile), then complete Steps 8a–8c — the build is not finished until all three are done.
    now: print("\nTHE ONE QUESTION TO PAUL (show the whole table in the reply, then ask exactly this):\n    Are these answers right, so that I build %s for %s, save the copy, make the Outlook draft "
    why: Kept.
- old line 192: Name the file [FirstName]_[Surname]_OM_Optimal_RA_Proposal_Email - [DD.MM.YY].html.
    now: "out/[FirstName]_[Surname]_OM_Optimal_RA_LumpSum_Proposal_Email - DD.MM.YY.html (a second run with --document lump_sum)",
    why: Kept.
- old line 192: To = the client's email, Cc = Sitamah Nathoo (admin@liferisk.co.za) always, Importance High.
    now: Sitamah Nathoo (admin@liferisk.co.za), always.
    why: Kept.
- old line 194: *If a lump sum applies (Question 11a = Yes):
    now: if not isinstance(a.get("lump_sum_applies"), bool):
    why: Kept.
- old line 194: build the second, separate Lump Sum Investment HTML (Step 6b) and run Steps 8a–8c for it too, as its own draft and its own Teams message (Lump Sum Quote Plan 2 + its fund fact sheet(s) as the attachme
    now: for the lump sum email, the Lump Sum Quote and its fund fact sheet(s).
    why: Kept.
- old line 194: If no lump sum applies:
    now: if not isinstance(a.get("lump_sum_applies"), bool):
    why: Kept.
- old line 194: one HTML, one draft, one Teams message.
    now: "as the main email, with its own draft and its own Teams message",
    why: Kept.
- old line 196: Never deliver the .xlsm working file to the client-facing output in either case.
    now: Never the .xlsm working file to the client.
    why: Kept.
- old line 198: save the HTML into the client's folder
    now: Never overwrite a file in the client's folder without Paul's clear yes in this chat.
    why: Proved by the folder listing and the receipts.
- old line 200: Paul SharePoint site > New Business > {Surname}, {FirstName} > {Surname}, {FirstName} - (OM RA - R{premium}) > Comparative Quotes (folder found with sharepoint_folder_search, parameter name).
    now: the client's folder under New Business/{Surname, First}/ > the RA transaction folder (for example {Surname, First} - (OM RA - R{premium})) > Comparative Quotes.
    why: Proved by the folder listing and the receipts.
- old line 200: It already holds the OM Optimal RA Quote, the fund fact sheets, the Optimal Illustrator (RA Booster Value) and the "OM Wealth Investment Strategy Summary" (and often the RGAR PDF — which is never atta
    now: It lists the 4 documents (the quote, the fund fact sheets, the Optimal Illustrator booster document, the Wealth Investment Strategy Summary);
    why: Proved by the folder listing and the receipts.
- old line 201: The signature logo is a long base64 string:
    now: no header, no signature block, no 'Kind regards,', no logo" % a["client_first_name"].strip())
    why: Proved by the folder listing and the receipts.
- old line 201: save a no-logo copy (logo <p> removed) rather than risk a corrupt image, and tell Paul the saved copy has no logo (the Outlook draft takes the logo from Paul's signature).
    now: "Tell Paul in plain words that the saved copy has no logo (the Outlook draft gets Paul's signature and logo separately)."
    why: Proved by the folder listing and the receipts.
- old line 201: Never truncate or retype base64 by hand.
    now: Never truncate or retype the logo (base64) by hand.
    why: Proved by the folder listing and the receipts.
- old line 202: Tell Paul the folder and file name in plain words.
    now: Tell Paul the folder and the file name in plain words, and that the saved copy has no logo.
    why: Proved by the folder listing and the receipts.
- old line 204: Outlook draft with Claude in Chrome (never sent by Claude)
    now: "Make the Outlook draft with Claude in Chrome (never sent by Claude) and read it back for the program",
    why: The read-back is checked by the program.
- old line 206: To client, Cc Sitamah Nathoo, Subject exactly as in the HTML.
    now: To = the client's email, Cc = Sitamah Nathoo.
    why: The read-back is checked by the program.
- old line 207: (1) outlook_create_draft for the shell (to, cc, subject, placeholder body);
    now: (1) create the draft shell with the Outlook connector's outlook_create_draft (to, cc, subject, a placeholder body such as BODY_PLACEHOLDER):
    why: The read-back is checked by the program.
- old line 207: new tab, navigate to outlook.office365.com/mail/ first, wait, then the draft's webLink, click the edit pencil;
    now: go to outlook.office365.com/mail/ first, wait, then the draft's webLink and wait about 8 seconds:
    why: The read-back is checked by the program.
- old line 207: (3) dispatch a paste event (ClipboardEvent('paste') with DataTransfer text/html) on [aria-label="Message body"] with the body only — "Dear {Client}," down to the bold next-meeting line;
    now: (3) replace the body with the contents of draft_body.html by dispatching a paste event that carries the HTML (ClipboardEvent('paste') with a DataTransfer holding text/html) on the [aria-label="Message
    why: The read-back is checked by the program.
- old line 207: no header table, no "Kind regards,", no signature (the signature supplies "Kind regards,");
    now: no header, no signature block, no 'Kind regards,', no logo" % a["client_first_name"].strip())
    why: The read-back is checked by the program.
- old line 207: use <b>, borders on td, <p> </p> spacers;
    now: You will pay zero taxes on your investment whilst in the retirement fund.</p>
    why: The read-back is checked by the program.
- old line 207: (4) Insert > Signature > "Paul K New";
    now: (4) add Paul's signature:
    why: The read-back is checked by the program.
- old line 207: wait ~8 s for autosave.
    now: print("\nRULES FOR THIS STEP (references/%s):\n" % r)
    why: The read-back is checked by the program.
- old line 208: Verify with read_resource on mail:///messages/{id} (result is large — parse the saved JSON file with python):
    now: read_resource on mail:///messages/{id} (the result is large:
    why: The read-back is checked by the program.
- old line 208: To, Cc, subject, importance high, tables open = close, exactly one "Kind regards", no placeholder text.
    now: R.add(True, "The Outlook draft was read back and passed all %d checks (To the client, Cc Sitamah, exact subject, High importance, tables open = close, 'Kind regards,' %s, no placeholder, no Loop, ever
    why: The read-back is checked by the program.
- old line 208: If DOM edits made after the paste don't persist, make the change through the editor (e.g.
    now: If DOM edits made after the paste do not persist, make the change through the editor (for example execCommand) so Outlook registers it, then check again.
    why: The read-back is checked by the program.
- old line 208: execCommand) so Outlook registers it, then re-verify.
    now: If DOM edits made after the paste do not persist, make the change through the editor (for example execCommand) so Outlook registers it, then check again.
    why: The read-back is checked by the program.
- old line 209: Close the tab afterwards and delete any stray drafts Claude created.
    now: delete any stray blank drafts Claude itself created while doing this (outlook_delete_draft) and say so;
    why: The read-back is checked by the program.
- old line 209: Attachments are not added by Claude — Sitamah attaches them and sends.
    now: Attachments are NOT added by Claude:
    why: The read-back is checked by the program.
- old line 211: Teams message to Sitamah (sent via Zapier;
    now: # The Teams message to Sitamah (through Zapier)
    why: Closes the old gap: the message used to be sent with no yes from Paul.
- old line 211: Sitamah attaches and sends the email)
    now: Sitamah attaches them and then sends the email.
    why: Closes the old gap: the message used to be sent with no yes from Paul.
- old line 213: microsoft_teams_send_chat_message — never through Claude in Chrome / Teams web, and not the native teams_send_chat_message (it fails:
    now: never through Claude in Chrome / Teams web, and not the native teams_send_chat_message (it fails:
    why: Closes the old gap: the message used to be sent with no yes from Paul.
- old line 213: "markdown" (it renders as real bold and a real numbered list in Teams — confirmed on Paul's run of 13/10/2026).
    now: "markdown" (it renders as real bold and a real numbered list in Teams).
    why: Closes the old gap: the message used to be sent with no yes from Paul.
- old line 215: Check real SAST time (TZ=Africa/Johannesburg date):
    now: return ({"[DATE AND TIME SENT]":
    why: Closes the old gap: the message used to be sent with no yes from Paul.
- old line 215: "Good morning Sitamah," before 12:00, "Good afternoon Sitamah," 12:00–17:59, "Good evening Sitamah," after.
    now: "Good morning Sitamah," before 12:00, "Good afternoon Sitamah," from 12:00 to 17:59, "Good evening Sitamah," after (South African time, set by the program from the clock).
    why: Closes the old gap: the message used to be sent with no yes from Paul.
- old line 215: Only if that same time-of-day greeting has already been used today in a message from Paul or Claude in the 1:1 chat, use "Hi Sitamah," or "Hey Sitamah," instead.
    now: Only if that same time-of-day greeting has already been used today in a message from Paul or Claude in the 1:1 chat (read the chat with read_resource on teams:///chats/{chatId}/messages) say --used-to
    why: Closes the old gap: the message used to be sent with no yes from Paul.
- old line 215: Other messages in the chat that carried no greeting do NOT remove the greeting — never start the message without one.
    now: Other messages in the chat that carried no greeting do NOT remove the greeting.
    why: Closes the old gap: the message used to be sent with no yes from Paul.
- old line 217: *Standard wording (only client/product details change;
    now: only the RA rows change.
    why: Closes the old gap: the message used to be sent with no yes from Paul.
- old line 217: bold "Action needed:" and "Drafts", numbered list;
    now: "markdown" (it renders as real bold and a real numbered list in Teams).
    why: Closes the old gap: the message used to be sent with no yes from Paul.
- old line 217: no emojis, no "do not send"/"leave in Drafts"/"let me know" lines):
    now: add(plain.rstrip().endswith("Once attached, please email the client - Thank you!") and "do not send" not in plain.lower() and "leave it in drafts" not in plain.lower(),
    why: Closes the old gap: the message used to be sent with no yes from Paul.
- old line 222: The OM Optimal RA Quote ({quote file name without .pdf})
    now: items = ["The OM Optimal RA Quote (%s)" % o.no_ext(o.doc_name(docs, "quote")), "The relevant fund fact sheets as per the quote (%s)" % fact_sheet_names(a),
    why: Closes the old gap: the message used to be sent with no yes from Paul.
- old line 223: The relevant fund fact sheets as per the quote ({fund names})
    now: items = ["The OM Optimal RA Quote (%s)" % o.no_ext(o.doc_name(docs, "quote")), "The relevant fund fact sheets as per the quote (%s)" % fact_sheet_names(a),
    why: Closes the old gap: the message used to be sent with no yes from Paul.
- old line 224: The OM Optimal RA Booster Value document ({Optimal Illustrator file name without .pdf})
    now: "The OM Optimal RA Booster Value document (%s)" % o.no_ext(o.doc_name(docs, "booster_doc")), "The \"OM Wealth Investment Strategy Summary\" document"]
    why: Closes the old gap: the message used to be sent with no yes from Paul.
- old line 225: The "OM Wealth Investment Strategy Summary" document
    now: Old Mutual Wealth Investment Strategy Summary</td></tr>
    why: Closes the old gap: the message used to be sent with no yes from Paul.
- old line 227: > All four are in {Client}'s folder:
    now: where = "All four are in %s's folder:
    why: Closes the old gap: the message used to be sent with no yes from Paul.
- old line 227: {RA folder name} > Comparative Quotes.
    now: print("Name to use in the RA transaction folder's Comparative Quotes:
    why: Closes the old gap: the message used to be sent with no yes from Paul.
- old line 228: > Once attached, please email the client - Thank you!
    now: "It ends 'Once attached, please email the client - Thank you!' with no 'do not send' line")
    why: Closes the old gap: the message used to be sent with no yes from Paul.
- old line 230: *The RGAR is never listed or mentioned (permanent rule).
    now: The RGAR is never listed or mentioned.
    why: Closes the old gap: the message used to be sent with no yes from Paul.
- old line 230: adapt the list to the Plan 2 documents.
    now: lump_sum_quote | The separate OM Lump Sum Quote (Plan 2) from Alwyn.
    why: Closes the old gap: the message used to be sent with no yes from Paul.
- old line 232: (1) Resolve the chat with list_dynamic_enum_values (tool_name = microsoft_teams_send_chat_message, property_name = chat, search = "Sitamah Nathoo") and take the 1:1 chat value 19:bd2a130a-35d9-459e-90
    now: Resolve the chat with list_dynamic_enum_values (tool_name = microsoft_teams_send_chat_message, property_name = chat, search = "Sitamah Nathoo") and take the 1:1 chat value the program prints (label "(
    why: Closes the old gap: the message used to be sent with no yes from Paul.
- old line 232: "markdown", content = the message in Markdown (bold, a blank line between paragraphs, 1.
    now: "the message went to the 1:1 chat as markdown and its read-back passes every program check"
    why: Closes the old gap: the message used to be sent with no yes from Paul.
- old line 232: list items, an output_hint is required by the tool).
    now: "markdown" and content = the message exactly as printed (an output_hint is required by the tool).
    why: Closes the old gap: the message used to be sent with no yes from Paul.
- old line 232: (3) Read the posted message back with read_resource on teams:///chats/{chatId}/messages/{messageId} and confirm the body shows <strong> bold labels, an <ol> numbered list, the greeting, and no literal
    now: Read the posted message back with read_resource on teams:///chats/{chatId}/messages/{messageId}, save it to a file, record message.chat (the chat value you used) and message.format markdown, and run r
    why: Closes the old gap: the message used to be sent with no yes from Paul.
- old line 232: Paul can also confirm in the Teams window.
    now: 9 the "what you can save" sentence carries [TOTAL CAP MONTHLY] in the right scenario wording.
    why: Closes the old gap: the message used to be sent with no yes from Paul.
- old line 234: *Final report to Paul states:
    now: # The final reply to Paul
    why: Closes the old gap: the message used to be sent with no yes from Paul.
- old line 234: where the HTML was saved, the draft's status, that Sitamah was messaged (and will attach + send), and flags (audit edge cases, quote/booster document discrepancies, quote expiry before the start date,
    now: Your reply to Paul is where the copy was saved, the draft's status, that Sitamah was messaged, the flags, and that audit, as they are.
    why: Closes the old gap: the message used to be sent with no yes from Paul.
- old line 250: This skill is about the *procedure*.
    now: This skill is a program that walks you through the job one step at a time.
    why: Kept.
- old line 250: It doesn't carry any specific client's data — each proposal should start from the client's own uploaded documents in that conversation.
    now: Every figure, name, date, fee and address comes from the client's own documents or Paul's words, with its source;
    why: Kept.
- old line 250: If a new client's documents aren't in this conversation yet, ask for them via the Step 1 checklist rather than reusing anything from earlier in the chat or from memory of a previous client.
    now: """Reads a client document's text (PDF or HTML/text), page by page, and checks that what the chat entered really appears in it.
    why: Kept.
- old line 252: <!-- ===== references/mcd_v6_3.md (Master Context Document V6.3) ===== -->
    now: "Paul's approved sentences, verbatim from the old skill (SKILL.md and the Master Context Document V6.3, sections 6.1 to 6.5 and 8.5).
    why: Kept.
- old line 256: *OM Optimal Retirement Annuity Proposal
    now: "Monthly Retirement Annuity Contribution (New OM Optimal RA)".
    why: Kept.
- old line 260: *Version 6.3 | July 2026
    now: "Paul's approved sentences, verbatim from the old skill (SKILL.md and the Master Context Document V6.3, sections 6.1 to 6.5 and 8.5).
    why: Kept.
- old line 280: This document is the definitive reference for producing an Old Mutual Optimal Retirement Annuity (OM Optimal RA) proposal email for any client.
    now: I have compiled the draft Old Mutual Optimal Retirement Annuity (RA) proposal email to %s and saved it in Drafts (To:
    why: Kept; enforced by the program.
- old line 280: It covers every section of the proposal, all data sources, all calculations, all tools used, the correct format, and the complete startup checklist.
    now: add(not miss, "Every figure and fixed sentence of the email is there as the rules phrase it" if not miss else "Missing from the email:
    why: Kept; enforced by the program.
- old line 280: Every future proposal must follow this document exactly.
    now: the FIRST figure after the label must be this one (a neighbouring figure does not count)
    why: Kept; enforced by the program.
- old line 282: ⚠ Before producing any proposal, Claude must perform a full figure audit — verifying that every number in the proposal traces back correctly to the Tax Reform Tool calculations, and that every sentenc
    now: R.attested.append("that the client's income, age and fund inputs sit in the right row of the tool (the tool is run with the confirmed answers, nobody re-types a figure)")
    why: Kept; enforced by the program.
- old line 297: PRODUCT OVERVIEW — OM OPTIMAL RA
    now: "Monthly Retirement Annuity Contribution (New OM Optimal RA)".
    why: Fixed text lives in the template.
- old line 299: ## 3.1 What It Is
    now: read what it says is missing or not found, fix that, run it again.
    why: Fixed text lives in the template.
- old line 301: The Old Mutual Optimal Investment Plan is the client’s certificate of membership of the South African Retirement Annuity Fund (SARAF), an approved Retirement Annuity Fund.
    now: <p style="font-size:12pt;margin:0;">The Optimal Investment Plan is your certificate of membership of the South African Retirement Annuity Fund (SARAF), an approved Retirement Annuity Fund.
    why: Fixed text lives in the template.
- old line 303: ## 3.2 Key Product Features
    now: def find_key(obj, names):
    why: Fixed text lives in the template.
- old line 305: up to 27.5% of the greater of remuneration or taxable income, in respect of ALL retirement vehicle contributions combined (RA + pension + provident), subject to a maximum of R430,000 per annum (effect
    now: C15 monthly remuneration (the gross monthly income), C17 age, C20 to C23 the employer and member pension and provident contributions as a share of the remuneration, C24 the monthly RA.
    why: Fixed text lives in the template.
- old line 307: zero income tax, capital gains tax, or dividend withholding tax while invested.
    now: got = (tax.get("runs") or {}).get(name)
    why: Fixed text lives in the template.
- old line 309: Two-Pot System (effective 1 September 2024):
    now: <p style="font-size:12pt;font-weight:bold;margin:0;">Two-Pot System as of the 1<sup>st</sup> September 2024:</p>
    why: Fixed text lives in the template.
- old line 309: 1/3 to Savings Component (accessible once per tax year, min R2,000, taxed at marginal rate);
    now: Withdrawal amount will be taxed at your marginal Tax Rate for that year.</p>
    why: Fixed text lives in the template.
- old line 309: 2/3 to Retirement Component (preserved until retirement).
    now: will go into The Retirement Component.</td></tr>
    why: Fixed text lives in the template.
- old line 309: At retirement (min age 55):
    now: "R 61 000.00", "retirement_age":
    why: Fixed text lives in the template.
- old line 309: up to 1/3 as lump sum;
    now: R.add(True, "Sitamah's message went to the 1:1 chat as markdown and was read back:
    why: Fixed text lives in the template.
- old line 311: No penalties for stopping, reducing or pausing premiums.
    now: <p style="font-size:12pt;margin:0;">There are no reduction fees for early termination or reducing / stopping premium contributions.
    why: Fixed text lives in the template.
- old line 311: Admin charge of R300 only.
    now: The transaction admin charge is always R 300.00.
    why: Fixed text lives in the template.
- old line 313: always set at 10% p.a.
    now: Alwyn must always set its ACI at 10% p.a.:
    why: Fixed text lives in the template.
- old line 317: 2.5% of fund value paid on the day before the 5th anniversary, plan must be active.
    now: A document cannot be found on any of the three routes:
    why: Fixed text lives in the template.
- old line 319: Monthly Boosters from year 6:
    now: The monthly fixed administration fee comes from the quote.
    why: Fixed text lives in the template.
- old line 323: ⚠ The Risk Profile is ALWAYS ‘Moderate’ for ALL clients on the Optimal RA proposal.
    now: The risk profile is always Moderate, the ACI 10%, the admin charge R 300.
    why: Fixed text lives in the template.
- old line 323: This is fixed and never changes.
    now: The RGAR is never an attachment of this email.
    why: Fixed text lives in the template.
- old line 328: Fund selection is determined entirely by Alwyn (OM Broker Consultant) and shown in the quote.
    now: quote | Alwyn's OM Optimal RA Quote (Plan 1), usually in the RA transaction folder > Comparative Quotes.
    why: Enforced by the program.
- old line 328: Claude reads fund names and allocation percentages directly from the quote.
    now: Plan 2's funds and fees are read from the Lump Sum Quote on its own:
    why: Enforced by the program.
- old line 328: Fund selection is NOT always 50/50 — it varies per client.
    now: Fund selection, fees, the ACI and premium amounts always come from THIS client's quote, never from a previous client's proposal, even if similar.
    why: Enforced by the program.
- old line 328: Always read from the quote.
    now: Fees are read from THIS quote every time:
    why: Enforced by the program.
- old line 330: ## 3.6 Fees — Always Read from Quote
    now: Fees are read from THIS quote every time:
    why: Computed by the program.
- old line 334: Asset management fee | Blended weighted average of selected funds — calculate from allocation %.
    now: the asset management fee is the blend of the funds weighted by their allocation;
    why: Computed by the program.
- old line 335: Net administration fee | Read from quote — typically 3.05% but verify each time.
    now: Fees are read from THIS quote every time:
    why: Computed by the program.
- old line 336: Ongoing advice fee | Read from quote under ‘PAYABLE FROM THE PLAN’S FUND VALUE — Asset advice fees’ — typically 0.575% p.a.
    now: items = ["The OM Optimal RA Quote (%s)" % o.no_ext(o.doc_name(docs, "quote")), "The relevant fund fact sheets as per the quote (%s)" % fact_sheet_names(a),
    why: Computed by the program.
- old line 337: Adviser remuneration account charge | Read from quote — typically 0.00%.
    now: ("adviser_charge", "adviser remuneration account charge", [r"adviser remuneration"])):
    why: Computed by the program.
- old line 338: Total ongoing fees | Sum of all above.
    now: the total ongoing fees add up the figures as shown.
    why: Computed by the program.
- old line 339: Monthly fixed admin fee (rand) | Read from quote — varies per quote.
    now: The monthly fixed administration fee comes from the quote.
    why: Computed by the program.
- old line 345: 1 | Client Fact Find — personal details, age, employer, position, start date, gross income, retirement goal, risk profile.
    now: personal details, age, employer, position, start date, gross income, retirement goal, risk profile, the personal email address.
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 346: 2 | Astute CCP Report OR existing policy schedules — existing RA details.
    now: astute_ccp | The Astute CCP report or the existing policy schedules:
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 346: If no existing RAs, adviser confirms.
    now: if not a["existing_ras"]:
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 347: 3 | Pension or Provident Fund Statement — fund value, employer/employee contribution % and rand amounts.
    now: ["Employer Provident Fund Contribution", "Member Provident Fund Contribution"]},
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 347: If no fund, adviser confirms.
    now: if "fund_statement" not in docs["docs"]:
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 348: 4 | Proof of Income (POI) / Payslip — gross monthly remuneration and fund contribution percentages.
    now: poi | Proof of income / payslip (the gross monthly income, the fund contributions).
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 349: 5 | RGAR PDF from Alwyn — Alwyn must set ACI at 10% p.a.
    now: Alwyn must always set its ACI at 10% p.a.:
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 349: If no RGAR requested, adviser confirms.
    now: registered, or Paul's words ("no RGAR was requested") |
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 350: 6 | OM Optimal RA Quote from Alwyn — new format (‘Old Mutual Savings and Income — Optimal Retirement Annuity Plan Quote Report’).
    now: New quotes are titled "Old Mutual Savings and Income - Optimal Retirement Annuity Plan Quote Report".
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 351: 7 | Date(s) of Teams Meeting(s) held with client — for opening line of proposal.
    now: nlx = "Teams Meeting on %s @ %s." % (o.fmt_date_with_day(o.next_date(a)), a["next_meeting"]["time"].strip())
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 352: 8 | Date, day and time of next scheduled Teams Meeting with client — for closing paragraph.
    now: return "%s @ %s" % (fmt_date_with_day(next_date(a)), a["next_meeting"]["time"].strip())
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 353: 9 | Is the client’s existing RA being replaced by the new OM Optimal RA, or will it be kept in force alongside it?
    now: "OM Optimal RA proposal", "Optimal RA proposal for [Name]", or Alwyn's OM Optimal RA Quote being back for a client.
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 353: (a) the Recommendation column in the Personal RA table, (b) the row structure of Table 3, and (c) whether the [RA_PENALTY_NOTE] applies.
    now: that a figure sits in the right place or column (attested), and anything on a page with no text (a scanned page):
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 353: If the client has no existing RA, this question does not apply.
    now: existing_ras is [] when the client has none (then ra_decision is none);
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 354: 10 | Please upload all current RA’s (active / paid up).
    now: "You have no active or Paid-Up Retirement Annuities.",
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 354: If there are no RA’s, please state that there are none.
    now: items = ["The OM Optimal RA Quote (%s)" % o.no_ext(o.doc_name(docs, "quote")), "The relevant fund fact sheets as per the quote (%s)" % fact_sheet_names(a),
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 354: This must be answered before any proposal is built.
    now: The RGAR is sent to the client in a separate email before this proposal (by rgar-skill);
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 355: Will a lump sum be going into the new OM Optimal RA, in addition to the recurring premium?
    now: "A lump sum amount of R {amount} will be invested into your new OM Optimal RA from your own savings ({source}).",
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 355: *(if Yes)* Is it a Section 14 transfer from an existing retirement fund, or voluntary funds from personal savings?
    now: exactly one of the two approved sentences (Section 14 transfer, or voluntary funds), never paraphrased;
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 355: *(if Section 14)* Which policy/policies are transferring, and what is the Net Fund Value?
    now: out.append("each source policy needs exactly name and net_value (the NET fund value, never the gross)")
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 355: *(if voluntary funds)* What is the source of the funds, and what is the Rand amount?
    now: out.append("a voluntary lump sum needs exactly type, amount, source_of_funds, tax_note")
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 355: Please upload the separate OM Lump Sum Quote (Plan 2) covering this amount.
    now: lump_sum_quote | The separate OM Lump Sum Quote (Plan 2) from Alwyn.
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 355: If 11a is No, 11b–11d do not apply.
    now: if nd is None or not re.fullmatch(r"\d{1,2}(:\d{2})?\s?(am|pm)", str(nm.get("time") or "").strip(), re.I):
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 356: 12 | Please provide the Client Overview document showing the ‘Current Investments’ section — gross fund value, penalties, net fund value and monthly premium for each existing policy at a glance.
    now: gross fund value, penalties, net fund value and monthly premium of each existing policy at a glance.
    why: The 12 startup items are documents the program registers or answers it checks; Paul is asked only the real questions.
- old line 358: The proposed monthly RA premium is read directly from the quotation — do not ask the adviser separately.
    now: m = _near_any([q], "proposed premium in the quote", [r"regular contribution", r"premium", r"monthly contribution"], prem, window=60)
    why: Documents are found by the chat, Paul is asked only the real questions.
- old line 358: If Question 11 is answered Yes, the Lump Sum Quote is read separately from the recurring-premium quote — see Section 10.3.*
    now: "The lump sum is R %s, %s" % (o.money_shown(lp["amount"]), "from the named source policies (Section 14)" if lp["type"] == "section14" else "from the client's own savings"))
    why: Documents are found by the chat, Paul is asked only the real questions.
- old line 360: THE HTML TEMPLATE — HOW TO USE IT
    now: You never edit a script, the template or the HTML.",
    why: Heading replaced.
- old line 446: ## 6.1 Personal Retirement Savings Section
    now: <p style="font-size:12pt;font-weight:bold;margin:0;">Personal Retirement Savings:</p>
    why: Built by the program.
- old line 448: Scenario | What Goes in Email |
    now: %s" % (i, x) for i, x in enumerate(items, 1)] + ["", where, "", "Once attached, please email the client - Thank you!"]
    why: Built by the program.
- old line 450: Client HAS existing RAs | Show full RA details for each policy:
    now: out.append("the client has existing RAs:
    why: Built by the program.
- old line 450: insurer name, policy number, monthly contributions, gross fund value + date, recommendation, penalties (always orange:
    now: each existing RA's insurer, policy number, monthly contribution, gross fund value and date.
    why: Built by the program.
- old line 450: ‘To be determined if there are’), net fund value.
    now: e.number("net fund value of %s" % pl["name"], d))
    why: Built by the program.
- old line 451: Client has NO existing RAs | Replace entire section content with:
    now: out.append("the client has existing RAs:
    why: Built by the program.
- old line 451: ‘You have no active or Paid-Up Retirement Annuities.’ — nothing else under this heading.
    now: "You have no active or Paid-Up Retirement Annuities.",
    why: Built by the program.
- old line 453: ## 6.2 Pension/Provident Retirement Savings Section
    now: <p style="font-size:12pt;font-weight:bold;margin:0;">Pension/Provident Retirement Savings:</p>
    why: Built by the program; the block wording is now fixed.
- old line 455: Scenario | What Goes in Email |
    now: %s" % (i, x) for i, x in enumerate(items, 1)] + ["", where, "", "Once attached, please email the client - Thank you!"]
    why: Built by the program.
- old line 457: Client HAS a Pension/Provident Fund | Line reads:
    now: the client has BOTH a pension and a provident fund:
    why: Built by the program.
- old line 457: ‘You have a [Pension/Provident] Fund with your employer [Employer Name]’ — NO end date.
    now: "You have no Pension or Provident Fund with your employer.",
    why: Built by the program.
- old line 457: Then employer contributions (R amount + %), employee contributions (R amount + %), current fund value + date.
    now: fund type, employer and member contributions (rand and %), fund value and date.
    why: Built by the program.
- old line 458: Client has NO Pension/Provident Fund | Replace entire section content with:
    now: the client has BOTH a pension and a provident fund:
    why: Built by the program.
- old line 458: ‘You have no Pension or Provident Fund with your employer.’ — nothing else under this heading.
    now: "You have no Pension or Provident Fund with your employer.",
    why: Built by the program.
- old line 460: ⚠ Never include an end date in the pension/provident line.
    now: Never an end date on the pension or provident fund line.
    why: Built by the program; the block wording is now fixed.
- old line 460: The [client B] end date was a one-off exception and must NOT be treated as standard.
    now: "According to the Retirement Goal Analysis Report that was sent to you on a previous email, over and above your current savings, you would be required to personally save <u>an additional</u> amount of
    why: Built by the program; the block wording is now fixed.
- old line 463: ## 6.3 Retirement Goal Analysis Section
    now: "You did not request for a Retirement Goal Analysis Report.",
    why: Built by the program.
- old line 465: Scenario | What Goes in Email |
    now: %s" % (i, x) for i, x in enumerate(items, 1)] + ["", where, "", "Once attached, please email the client - Thank you!"]
    why: Built by the program.
- old line 467: RGAR was requested and received | Show full shortfall paragraph:
    now: rgar is null when none was requested (the email then says "You did not request for a Retirement Goal Analysis Report.").
    why: Built by the program.
- old line 467: R [FUTURE VALUE] p.m.
    now: "R 30 000.00", "future_value":
    why: Built by the program.
- old line 468: RGAR was NOT requested | Replace entire section content with:
    now: ("Retirement Goal Analysis", "not requested" if a["rgar"] is None else "shortfall R %s a month for %s years, goal R %s (future value R %s) at age %s" % (
    why: Built by the program.
- old line 468: ‘You did not request for a Retirement Goal Analysis Report.’ — nothing else under this heading.
    now: "You did not request for a Retirement Goal Analysis Report.",
    why: Built by the program.
- old line 470: ## 6.4 Tax Reform Tool — Employment Type Scenarios
    now: R.add(not stale, "The Tax Reform Tool (%s, %s) was recalculated by LibreOffice for the 4 scenarios;
    why: The program sets the employment type.
- old line 472: Employment Type | Effect on Tax Reform Tables |
    now: the employment type is the text in Calcs!B2 (Tax Monthly = self-employed or no fund;
    why: The program sets the employment type.
- old line 474: Self Employed | No fund contributions.
    now: "self-employed / no fund"}[o.fund_of(a)["type"]]
    why: The program sets the employment type.
- old line 474: Full C15 ÷ 12 available for RA.
    now: for nm, h in (("full copy", full), ("saved copy", nologo)):
    why: The program sets the employment type.
- old line 474: All three tables show no pension/provident rows — only the RA contribution row, which changes across the three tables.
    now: pension fund, provident fund, or self-employed / no fund (an existing RA does not change the wording).
    why: The program sets the employment type.
- old line 475: Employed (Pension Fund) | Employer + employee pension contribution rows appear in ALL THREE tables.
    now: Pension and provident rows appear in all three tables;
    why: The program sets the employment type.
- old line 475: Both count toward the 27.5% limit.
    now: A lump sum (Section 14 or voluntary) never counts toward the 27.5% / R430,000 limit and is never added to the Tax Reform Tool's inputs.
    why: The program sets the employment type.
- old line 475: RA row changes across the three tables.
    now: *The four scenarios and the three tables
    why: The program sets the employment type.
- old line 476: Employed (Provident Fund) | Same as pension fund logic but rows labelled ‘Employer Provident Fund Contribution’ and ‘Member Provident Fund Contribution’.
    now: ["Employer Provident Fund Contribution", "Member Provident Fund Contribution"]},
    why: The program sets the employment type.
- old line 476: Both count toward the 27.5% limit.
    now: A lump sum (Section 14 or voluntary) never counts toward the 27.5% / R430,000 limit and is never added to the Tax Reform Tool's inputs.
    why: The program sets the employment type.
- old line 476: RA row changes across the three tables.
    now: *The four scenarios and the three tables
    why: The program sets the employment type.
- old line 478: ## 6.5 Lump Sum Investment — Two-Document Structure
    now: ## The separate Lump Sum Investment email ("document":
    why: Built by the program as a separate run.
- old line 480: *Governance decision (22/07/26, superseding the earlier single-email approach in V6.0–V6.2):
    now: "left in Drafts for Sitamah to attach the documents and email the client",
    why: Built by the program as a separate run.
- old line 480: whenever Startup Question 11a is Yes, Claude produces TWO separate HTML documents instead of one combined email:
    now: what = "the RA proposal email" if document_of(rj) == "main" else "the separate Lump Sum Investment email"
    why: Built by the program as a separate run.
- old line 482: The main proposal (unchanged template, OM_Optimal_RA_Proposal_CLAUDE_TEMPLATE_22_07_26.html) — covers the recurring monthly premium (Plan 1) only.
    now: os.path.join(ASSETS, "OM_Optimal_RA_Proposal_TEMPLATE.html"), "lump_sum":
    why: Built by the program as a separate run.
- old line 482: It does NOT contain any lump sum content.
    now: if not isinstance(a.get("lump_sum_applies"), bool):
    why: Built by the program as a separate run.
- old line 482: The three tax tables, “what you can save” sentence, RGAR, and all other sections relate ONLY to the recurring contribution, since the lump sum has no bearing on the 27.5%/R430,000 annual deduction cal
    now: "Based on your current earnings, you can save a total of <strong>R {total}</strong> per month towards a Retirement Annuity to take full advantage of the tax-deductible benefit offered to you by SARS."
    why: Built by the program as a separate run.
- old line 484: A separate Lump Sum Investment proposal (new template, OM_Optimal_RA_LumpSum_Proposal_TEMPLATE.html) — covers the lump sum (Plan 2) only:
    now: OM_Optimal_RA_Proposal_TEMPLATE.html (the recurring premium, Plan 1, only) and OM_Optimal_RA_LumpSum_Proposal_TEMPLATE.html (the lump sum, Plan 2, only).
    why: Built by the program as a separate run.
- old line 484: the Section 14 transfer or voluntary funds facts, the Plan 2 fund/fee detail, risk profile, and product description.
    now: exactly one of the two approved sentences (Section 14 transfer, or voluntary funds), never paraphrased;
    why: Built by the program as a separate run.
- old line 484: It contains NO tax tables (a lump sum transfer/investment does not generate an RA tax deduction calculation the way a recurring contribution does).
    now: This is a tax-neutral transfer between approved retirement funds and does not attract any tax at the point of transfer.",
    why: Built by the program as a separate run.
- old line 486: the recurring premium and lump sum are answers to two different client questions (“how much should I contribute monthly and why” vs “what happens to my existing RA money”), are quoted separately by Al
    now: Should you at any point need to stop the RA or cancel the premium, there are no penalties to you as the client, only an admin charge of R 300.00</p>
    why: Built by the program as a separate run.
- old line 486: Two focused documents are clearer for the client and the adviser.
    now: Sitamah attaches the documents and emails the client.
    why: Built by the program as a separate run.
- old line 488: the same signature block, adviser contact details, and Wealth Revolution branding/footer.
    now: the Exchange rule of paul-email-signature adds the signature at send time and Claude inserts nothing.
    why: Built by the program as a separate run.
- old line 488: Both should be sent together (or in close succession) as they relate to the same overall recommendation, and both quotes (recurring + lump sum) are attached across the two emails as appropriate.
    now: the full copy (with the logo) is sent to Paul in the chat as [FirstName]_[Surname]_OM_Optimal_RA_Proposal_Email - DD.MM.YY.html (the lump sum email:
    why: Built by the program as a separate run.
- old line 490: ### 6.5.1 Background — How OM Structures a Lump Sum Alongside a Recurring Premium
    now: kind = "OM_Optimal_RA_LumpSum_Proposal_Email" if doc_of(a) == "lump_sum" else "OM_Optimal_RA_Proposal_Email"
    why: Built by the program as a separate run.
- old line 492: When a client starts an OM Optimal RA with both a recurring monthly premium AND a lump sum contribution, Old Mutual treats these as two separate quoted plans under the SAME contract/policy number:
    now: items = ["The OM Optimal RA Lump Sum Quote (%s)" % o.no_ext(o.doc_name(docs, "lump_sum_quote")), "The relevant fund fact sheet(s) as per the Lump Sum Quote (%s)" % fact_sheet_names(a)]
    why: Built by the program as a separate run.
- old line 494: Plan 1 — the recurring monthly premium (covered in the main proposal document).
    now: run.py start <run> --client "First Surname" [--document main|lump_sum]     main = the RA proposal (default);
    why: Built by the program as a separate run.
- old line 496: Plan 2 — the once-off lump sum amount (covered in the separate Lump Sum Investment proposal document).
    now: %s\n" % (rj["client"], "the main RA proposal" if document == "main" else "the separate Lump Sum Investment proposal"))
    why: Built by the program as a separate run.
- old line 498: Alwyn will issue two separate OM quotes when a lump sum applies:
    now: "The separate Lump Sum Investment email (.html), only when a lump sum applies",
    why: Built by the program as a separate run.
- old line 498: the standard recurring-premium quote (Plan 1) and a separate Lump Sum Quote (Plan 2).
    now: lump_sum_quote | The separate OM Lump Sum Quote (Plan 2) from Alwyn.
    why: Built by the program as a separate run.
- old line 498: Do NOT assume Plan 2’s fund selection, fees, or allocation are identical to Plan 1 — always read the Lump Sum Quote directly, the same as any other quote.
    now: Plan 2's funds and fees are read from the Lump Sum Quote on its own:
    why: Built by the program as a separate run.
- old line 500: ### 6.5.2 The Lump Sum Investment Proposal Document — Structure
    now: the Lump Sum Investment proposal for %s (R %s, %s);
    why: Built by the program as a separate run.
- old line 502: The OM_Optimal_RA_LumpSum_Proposal_TEMPLATE.html document follows the same visual/HTML conventions as the main template (Outlook-compatible table layout, same fonts/colours, same signature block) but 
    now: "out/[FirstName]_[Surname]_OM_Optimal_RA_Proposal_Email - DD.MM.YY.html (with logo, sent to Paul in the chat) and out/saved/<same name> (no logo, saved in the RA transaction folder's Comparative Quote
    why: Built by the program as a separate run.
- old line 504: Opening — same “Following our Teams Meeting…” opening line as the main proposal.
    now: <p style="font-size:12pt;margin:0;">Following our Teams Meeting on <strong>[MEETING DATES LIST]</strong>, herewith please find my recommendations:</p>
    why: Built by the program as a separate run.
- old line 506: Your Lump Sum Investment — the approved verbatim wording (Section 6.5.3 below) stating the amount, Section 14 source policy/policies (or voluntary funds source), and the tax-neutral confirmation.
    now: exactly one of the two approved sentences (Section 14 transfer, or voluntary funds), never paraphrased;
    why: Built by the program as a separate run.
- old line 508: The product & start date — Plan 2 start date, read from the Lump Sum Quote.
    now: e.date("Plan 2 start date in the Lump Sum Quote", a["start_date"]))
    why: Built by the program as a separate run.
- old line 510: Risk profile — always “Moderate” (same fixed rule as the main proposal).
    now: The risk profile is always Moderate, the ACI 10%, the admin charge R 300.
    why: Built by the program as a separate run.
- old line 512: Investment Fund Details (Plan 2) — fund selection and fee mini-table (Section 6.5.5 below).
    now: <!-- INVESTMENT FUND DETAILS (PLAN 2) -->
    why: Built by the program as a separate run.
- old line 512: Always read directly from the Lump Sum Quote — never assume it matches Plan 1.
    now: Plan 2's funds and fees are read from the Lump Sum Quote on its own:
    why: Built by the program as a separate run.
- old line 514: Tax treatment of the transfer — for Section 14:
    now: # ------------------------------------------------------------------ the figures for the Tax Reform Tool
    why: Built by the program as a separate run.
- old line 514: confirm the transfer is tax-neutral and does not use up the client’s annual deduction limit.
    now: It is tax-neutral and does not use up your annual tax deduction limit.",
    why: Built by the program as a separate run.
- old line 514: note that the amount invested is from after-tax savings and does not attract an additional RA tax deduction (a lump sum contribution to a retirement annuity may still be tax-deductible up to the 27.5%
    now: A lump sum (Section 14 or voluntary) never counts toward the 27.5% / R430,000 limit and is never added to the Tax Reform Tool's inputs.
    why: Built by the program as a separate run.
- old line 516: Attachments line — lists the Lump Sum Quote and its fund fact sheet(s).
    now: the Lump Sum Quote and its fund fact sheet(s).
    why: Built by the program as a separate run.
- old line 518: Closing / next meeting line — same as main proposal.
    now: def next_meeting_line(a):
    why: Built by the program as a separate run.
- old line 520: Signature block — identical to the main proposal.
    now: The RGAR is sent to the client in a separate email before this proposal (by rgar-skill);
    why: Built by the program as a separate run.
- old line 522: No tax tables, no bar chart, and no “what you can save” sentence appear in this document — those belong only in the main recurring-premium proposal.
    now: no tax tables, bar chart or "what you can save" sentence;
    why: Built by the program as a separate run.
- old line 524: ### 6.5.3 Scenario Table — Approved Verbatim Wording (use exactly, do not paraphrase)
    now: "Paul's approved sentences, verbatim from the old skill (SKILL.md and the Master Context Document V6.3, sections 6.1 to 6.5 and 8.5).
    why: Built by the program as a separate run.
- old line 526: The heading above the lump sum paragraph is always:
    now: A lump sum is never added to the tool's inputs;
    why: Built by the program as a separate run.
- old line 526: “Your Lump Sum Investment:” in the Lump Sum Investment proposal document.
    now: add("Your Lump Sum Investment:" in bt and "tax" in bt.lower() and "Retirement Goal" not in bt and "Maximum Deduction" not in bt,
    why: Built by the program as a separate run.
- old line 528: Scenario | What Goes in Email (verbatim) |
    now: %s" % (i, x) for i, x in enumerate(items, 1)] + ["", where, "", "Once attached, please email the client - Thank you!"]
    why: Built by the program.
- old line 530: Section 14 transfer | ‘A lump sum amount of R [LUMP SUM AMOUNT] will be transferred into your new OM Optimal RA via a Section 14 transfer from your existing [SOURCE POLICY NAME(S)] policy/policies.
    now: "A lump sum amount of R {amount} will be transferred into your new OM Optimal RA via a Section 14 transfer from your existing {sources} policy/policies.
    why: Built by the program.
- old line 530: This is a tax-neutral transfer between approved retirement funds and does not attract any tax at the point of transfer.’ Repeat/list [SOURCE POLICY NAME(S)] for each transferring policy if more than o
    now: This is a tax-neutral transfer between approved retirement funds and does not attract any tax at the point of transfer.",
    why: Built by the program.
- old line 531: Voluntary funds | ‘A lump sum amount of R [LUMP SUM AMOUNT] will be invested into your new OM Optimal RA from your own savings ([SOURCE OF FUNDS]).’ |
    now: "A lump sum amount of R {amount} will be invested into your new OM Optimal RA from your own savings ({source}).",
    why: Built by the program.
- old line 533: These wordings were reviewed and approved by Paul (22/07/26, revised for the two-document structure) — use them exactly as written, substituting only the bracketed figures/names.
    now: 4 and 5 are computed and, when the two figures differ, flagged to Paul with BOTH figures, never forced (the known edge case:
    why: Built by the program as a separate run.
- old line 533: This document is only produced at all when a lump sum applies — there is no “no lump sum” variant here (in that case, simply don’t produce this second document).
    now: When a lump sum goes in, a second, separate Lump Sum Investment email in a second run.
    why: Built by the program as a separate run.
- old line 537: The Section 14 vs voluntary funds distinction is never inferred — it must come directly from the adviser’s answer to Startup Question 11b.
    now: A lump sum (Section 14 or voluntary) never counts toward the 27.5% / R430,000 limit and is never added to the Tax Reform Tool's inputs.
    why: Built by the program as a separate run.
- old line 539: [LUMP SUM AMOUNT] for a Section 14 transfer is always the Net Fund Value of the transferring policy/policies (as shown on the Client Overview / Astute CCP report) — never the Gross Fund Value.
    now: out.append("a Section 14 lump sum needs the Client Overview or the Astute report registered (the net fund values)")
    why: Built by the program as a separate run.
- old line 541: If multiple policies are being transferred via Section 14, sum their Net Fund Values for [LUMP SUM AMOUNT] and name each source policy individually in [SOURCE POLICY NAME(S)].
    now: For Section 14 the amount is the sum of the source policies' NET fund values (never gross), each policy named.
    why: Built by the program as a separate run.
- old line 543: A lump sum being transferred via Section 14 does NOT count toward the client’s annual 27.5%/R430,000 tax-deductible contribution limit (it is a fund-to-fund transfer, not a new contribution) and must 
    now: A lump sum (Section 14 or voluntary) never counts toward the 27.5% / R430,000 limit and is never added to the Tax Reform Tool's inputs.
    why: Built by the program as a separate run.
- old line 545: Voluntary funds invested as a lump sum also do not affect the Tax Reform Tool’s monthly contribution inputs in the main proposal — but if the adviser indicates the voluntary lump sum is itself intende
    now: If Paul says the voluntary lump sum is meant to use up unused annual deduction room, flag it to him.
    why: Built by the program as a separate run.
- old line 547: ### 6.5.5 Plan 2 Fund & Fee Detail — [LS_FUND_FEE_BLOCK]
    now: E(a["start_date"].strip()), "[LS_FUND_FEE_BLOCK]":
    why: Built by the program as a separate run.
- old line 549: The Lump Sum Investment proposal document must show Plan 2’s fund selection and fee structure, using a mini table in the same visual style as the main proposal’s Investment Fund Details table.
    now: add(bold >= 2 and ("Your Lump Sum Investment:" in bt if o.doc_of(a) == "lump_sum" else "Your personal circumstances:" in bt), "The section headings and the next-meeting line are bold (%d bold tags)" %
    why: Built by the program as a separate run.
- old line 549: Always read Plan 2’s fund selection and fees directly from the Lump Sum Quote — never assume they match Plan 1.
    now: Plan 2's funds and fees are read from the Lump Sum Quote on its own:
    why: Built by the program as a separate run.
- old line 549: They are frequently different (different fund count, different allocation, different fee tiers), since Plan 2 is a separate quoted plan under the same contract.
    now: they are often different from Plan 1 (a single fund at 100%, a tiered administration fee:
    why: Built by the program as a separate run.
- old line 551: Required content of [LS_FUND_FEE_BLOCK]:
    now: E(a["start_date"].strip()), "[LS_FUND_FEE_BLOCK]":
    why: Built by the program as a separate run.
- old line 553: A fund allocation table — one row per fund in the Lump Sum Quote, with fund name and allocation % (Plan 2 may hold a single fund at 100%, or multiple funds — read directly from the quote, do not assum
    now: replace or keep the existing RA(s) (his answer), whether the lump sum goes in (yes or no) and its kind and source, the meetings already held (pre-fill them from the file names) and the next meeting.
    why: Built by the program as a separate run.
- old line 555: A fee table for Plan 2 — asset management fee (blended if more than one fund), administration fee (may be tiered by fund value band — state the applicable band or the initial rate), asset advice fee, 
    now: rows = [("Asset management fee", o.fee_shown(o.blended_fee(a)) + "%"), ("Administration fee", ls_fee_value(fe["admin_fee"])), ("Asset advice fee", ls_fee_value(fe["advice_fee"])),
    why: Built by the program as a separate run.
- old line 559: ## 7.1 FIXED Lines — Same for Every Client
    now: nm = [nm[0]] + ["the " + n for n in nm[1:]]
    why: Fixed text lives in the templates.
- old line 567: ‘You are working at [employer] in the position of [position].’ — NEVER ‘You will be working.’ The wording is always present tense.
    now: "You are working at [employer] in the position of [position]." (never "You will be working").
    why: Fixed text lives in the templates.
- old line 569: To be determined if there are’ (always in orange)
    now: out.append("flags must be a list of short sentences (empty list if there is nothing to flag)")
    why: Fixed text lives in the templates.
- old line 571: ‘…increasing at 10% per annum…’ (ACI always 10%)
    now: The ACI is always 10%.
    why: Fixed text lives in the templates.
- old line 573: ‘You can elect to start a Retirement Annuity with Old Mutual called The Optimal Investment Plan…’
    now: <p style="font-size:12pt;margin:0;">You can elect to start a Retirement Annuity with Old Mutual called The Optimal Investment Plan where you can make monthly contributions of <strong>R [PROPOSED PREMI
    why: Fixed text lives in the templates.
- old line 577: ‘The Optimal Investment Plan is your certificate of membership of SARAF… It is a disciplined vehicle to provide for retirement capital.’
    now: It is a disciplined vehicle to provide for retirement capital.</p>
    why: Fixed text lives in the templates.
- old line 579: ‘…tax deductible up to 27.5% of remuneration capped at R430,000 per annum.’
    now: Contributions to a retirement fund are tax deductible up to 27,5% of remuneration capped at <strong>R 430,000 per annum</strong>.</p>
    why: Fixed text lives in the templates.
- old line 581: All Two-Pot System bullet points
    now: <p style="font-size:12pt;font-weight:bold;margin:0;">Two-Pot System as of the 1<sup>st</sup> September 2024:</p>
    why: Fixed text lives in the templates.
- old line 583: All Tax Reform table headings and structure
    now: 3 the tax payable of Tables 1, 2 and 3 all differ;
    why: Fixed text lives in the templates.
- old line 585: ‘RE-INVESTING YOUR RECLAIMED DEDUCTION:
    now: svd = re.findall(r"Annual Tax Saved from RA Deduction R (\d[\d,]*|–)", bt)
    why: Fixed text lives in the templates.
- old line 585: HOW MUCH OF YOUR RA CONTRIBUTION SARS WILL PAY’
    now: <p style="text-align:center;font-weight:bold;font-size:10pt;margin:0 0 10px 0;">RE-INVESTING YOUR RECLAIMED DEDUCTION:<br>HOW MUCH OF YOUR RA CONTRIBUTION SARS WILL PAY</p>
    why: Fixed text lives in the templates.
- old line 587: All Booster text and Booster table values
    now: if any(e is not None and not e.has_text for e in ev.values()):
    why: Fixed text lives in the templates.
- old line 589: ‘You have access to a wide range of funds.’
    now: <p style="font-size:12pt;margin:0;">You have access to a wide range of funds.</p>
    why: Fixed text lives in the templates.
- old line 591: All Tax Implication section text
    now: 3 the tax payable of Tables 1, 2 and 3 all differ;
    why: Fixed text lives in the templates.
- old line 593: ‘There are no reduction fees… only an admin charge of R300.00’
    now: The transaction admin charge is always R 300.00.
    why: Fixed text lives in the templates.
- old line 595: All Savings Component withdrawal text
    now: will go into a Savings Pot.</td></tr>
    why: Fixed text lives in the templates.
- old line 597: Personal Investment Target description paragraphs (inflation plus 4–5%, 5–7 years, diversified portfolio)
    now: <p style="font-size:12pt;margin:0;">Although the Personal Investment Target targets specific inflation-beating returns, these returns are not guaranteed.</p>
    why: Fixed text lives in the templates.
- old line 599: ‘Although the Personal Investment Target targets specific inflation-beating returns, these returns are not guaranteed.’
    now: <p style="font-size:12pt;margin:0;">Although the Personal Investment Target targets specific inflation-beating returns, these returns are not guaranteed.</p>
    why: Fixed text lives in the templates.
- old line 601: Fees table structure and headings
    now: a["ls_fees"]["as_and_when"]), s.get("quote")),
    why: Fixed text lives in the templates.
- old line 603: ‘Please see attached:’ heading and items 1, 3 and 4
    now: " not in bt.split("Please see attached:")[1].split("Hoping")[0],
    why: Fixed text lives in the templates.
- old line 605: ‘Hoping that above is in order.’ | ‘Kind regards,’ | Full signature block
    now: <p style="font-size:12pt;margin:0;">Hoping that above is in order.</p>
    why: Fixed text lives in the templates.
- old line 607: ## 7.2 VARIABLE Lines — Client-Specific, Must Change Every Proposal
    now: run.py start <run> --client "First Surname" [--document main|lump_sum]     main = the RA proposal (default);
    why: Every variable has a source in the answers file.
- old line 611: TO / CC email addresses | Left as placeholders — adviser fills in before sending |
    now: R.add(True, "The built email passed all %d program checks (no placeholder left, tables open = close, header To/Cc/Subject/Importance, weekdays computed, every figure and fixed sentence, "
    why: Every variable has a source in the answers file.
- old line 612: Subject line | Client name + premium from quote |
    now: return html.unescape(wd["subject_main"].format(name=a["client_full_name"].strip(), premium=premium_of(a)))
    why: Every variable has a source in the answers file.
- old line 613: Date/time sent | Date proposal is produced |
    now: v = {"[DATE AND TIME SENT]":
    why: Every variable has a source in the answers file.
- old line 614: Teams meeting date(s) (opening) | Startup Question 7 |
    now: out.append("the next meeting date %s is in the past" % nm["date"])
    why: Every variable has a source in the answers file.
- old line 615: Client first name | Fact Find |
    now: E(a["client_first_name"].strip()), "[MEETING DATES LIST]":
    why: Every variable has a source in the answers file.
- old line 617: Employer, position, division | Fact Find |
    now: %s" % (a["age"], a["employer"], a["position"]), s.get("personal")),
    why: Every variable has a source in the answers file.
- old line 618: Gross monthly income | Fact Find / POI |
    now: e.number("gross monthly income in the Fact Find Summary / proof of income", inc))
    why: Every variable has a source in the answers file.
- old line 619: Existing RA details (or no RAs statement) | Astute CCP / policy schedule |
    now: astute_ccp | The Astute CCP report or the existing policy schedules:
    why: Every variable has a source in the answers file.
- old line 620: Replace vs keep decision | Startup Question 9 — determines Recommendation column, Table 3 structure, and [RA_PENALTY_NOTE] |
    now: replace or keep the existing RA, the lump sum (yes or no, Section 14 or voluntary, the source), the meetings already held and the next meeting.
    why: Every variable has a source in the answers file.
- old line 621: Pension/Provident details (or no fund statement) | POI + Fund Statement |
    now: "Pension / Provident Fund statement", "poi":
    why: Every variable has a source in the answers file.
- old line 622: ‘What you can save’ sentence | Constructed dynamically per client scenario — see Section 8.5 |
    now: the 'what you can save' sentence is missing or not the scenario's wording")
    why: Every variable has a source in the answers file.
- old line 623: RGAR shortfall figures (or no RGAR statement) | RGAR second shortfall table |
    now: The shortfall is the SECOND shortfall table (after the proposed RA is factored in), never the first.
    why: Every variable has a source in the answers file.
- old line 624: Proposed premium (‘What you have chosen’) | Quote |
    now: e.number("proposed premium in the quote", prem))
    why: Every variable has a source in the answers file.
- old line 626: All three Tax Reform table figures | Tax Reform Tool — calculated per client |
    now: # ------------------------------------------------------------------ the figures for the Tax Reform Tool
    why: Every variable has a source in the answers file.
- old line 627: Bar chart values (years 1–10) | Tax Reform Tool — Reinvest Calcs sheet |
    now: 8 the bar chart's year 1 = Table 3's tax saved from the RA;
    why: Every variable has a source in the answers file.
- old line 628: ‘By contributing R[X] per month’ headings (Tables 2 & 3) | Tax Reform Tool outputs |
    now: "The 2026/27 SARS tables the Tax Reform Tool holds (Paul's skill, 14/10/2026).
    why: Every variable has a source in the answers file.
- old line 629: Fund names and allocations | Quote — fund selection table |
    now: """The funds, their allocations and fees against the quote's text;
    why: Every variable has a source in the answers file.
- old line 630: ‘Funds recommended’ sentence | Quote — fund names |
    now: funds_sentence(a), "[FUND_ROWS]":
    why: Every variable has a source in the answers file.
- old line 631: Attachment point 2 fund names | Quote — fund names |
    now: the Lump Sum Quote and its fund fact sheet(s).
    why: Every variable has a source in the answers file.
- old line 632: All fee percentages and rand amounts | Quote |
    now: a["ls_fees"]["as_and_when"]), s.get("quote")),
    why: Every variable has a source in the answers file.
- old line 633: Next Teams meeting details (closing) | Startup Question 8 |
    now: nlx = "Teams Meeting on %s @ %s." % (o.fmt_date_with_day(o.next_date(a)), a["next_meeting"]["time"].strip())
    why: Every variable has a source in the answers file.
- old line 635: TAX REFORM TOOL — HOW TO USE IT
    now: the Tax Reform Tool is not used for it")
    why: Heading replaced.
- old line 639: Tax_Reform_ToolV3__2026__2027__TEMPLATE_4.xlsm (project files) — ONLY this version
    now: The workbook (assets/Tax_Reform_Tool_TEMPLATE_4.xlsm) is never changed:
    why: The facts are held in one file and checked by the program.
- old line 641: 2026/2027 — SARS tables effective 1 March 2026
    now: It holds the 2026/2027 SARS tables (effective 1 March 2026), valid until 28/02/2027:
    why: The facts are held in one file and checked by the program.
- old line 643: R0–R237,100 (18%) | R237,101–R370,500 (26%) | R370,501–R512,800 (31%) | R512,801–R673,000 (36%) | R673,001–R857,900 (39%) | R857,901–R1,817,000 (41%) | Above R1,817,000 (45%)
    now: [[0, 0.18], [237100, 0.26], [370500, 0.31], [512800, 0.36], [673000, 0.39], [857900, 0.41], [1817000, 0.45]],
    why: The facts are held in one file and checked by the program.
- old line 645: R430,000 | 27.5% limit
    now: "R 30 000.00", "future_value":
    why: The facts are held in one file and checked by the program.
- old line 647: B35 = annual remuneration + employer fund contributions (fringe benefit added back per SARS)
    now: Calcs!C15 is the binding allowance = MIN(R430,000, 27.5% x Calcs!B35), where Calcs!B35 = annual remuneration + the employer fund contributions (a fringe benefit added back).
    why: The tool is run by the program, never by hand.
- old line 649: C15 = MIN(R430,000, 27.5% × B35) — this is the binding SARS allowance
    now: Calcs!C15 is the binding allowance = MIN(R430,000, 27.5% x Calcs!B35), where Calcs!B35 = annual remuneration + the employer fund contributions (a fringe benefit added back).
    why: The facts are held in one file and checked by the program.
- old line 651: radio buttons on Maximise Allowance Tool sheet
    now: Inputs on Maximise Allowance Tool:
    why: The facts are held in one file and checked by the program.
- old line 653: ## 8.2 Three Scenarios — Purpose and Input Rules
    now: *The four scenarios and the three tables
    why: The inputs of each table are set by the program.
- old line 655: Table | Purpose | PAY YOURSELF FIRST Rows |
    now: The shortfall is the SECOND shortfall table (after the proposed RA is factored in), never the first.
    why: The inputs of each table are set by the program.
- old line 657: Table 1 — Your current situation | Shows the client’s exact tax position today.
    now: <!-- YOUR CURRENT SITUATION — TABLE 1 -->
    why: The inputs of each table are set by the program.
- old line 657: Every existing RA the client currently holds appears as its own named row.
    now: existing_ras is [] when the client has none (then ra_decision is none);
    why: The inputs of each table are set by the program.
- old line 657: The tax saved on those existing contributions is shown.
    now: tax saved is the tool's own figure;
    why: The inputs of each table are set by the program.
- old line 657: This is the true baseline.
    now: """The last row whose first column is <= key (what the workbook's VLOOKUP(..., TRUE) does)."""
    why: The inputs of each table are set by the program.
- old line 657: Pension/Provident rows also shown if applicable.
    now: Pension and provident rows appear in all three tables;
    why: The inputs of each table are set by the program.
- old line 657: | Pension/Provident rows (if applicable) + one named row per existing RA showing current monthly contribution.
    now: pension fund, provident fund, or self-employed / no fund (an existing RA does not change the wording).
    why: The inputs of each table are set by the program.
- old line 657: Tax saved on existing RA contributions must be shown — never R–.
    now: tax saved from the RA", "R %s;
    why: The inputs of each table are set by the program.
- old line 658: Table 2 — Taking advantage of the full tax deduction | Shows the maximum 27.5% SARS opportunity using only the new OM Optimal RA.
    now: Table 2, the full deduction | [MAXIMUM RA CONTRIBUTION] = (cap - the yearly fund contributions) / 12 | one new OM Optimal RA row;
    why: The inputs of each table are set by the program.
- old line 658: No existing RA rows appear here — ever.
    now: ra_rows(a) if a["existing_ras"] else "", "[PENSION_BLOCK]":
    why: The inputs of each table are set by the program.
- old line 658: Single RA row shows [MAXIMUM RA CONTRIBUTION] = full remaining SARS room.
    now: [MAXIMUM RA CONTRIBUTION]", "R %s;
    why: The inputs of each table are set by the program.
- old line 658: Together with any fund rows, equals full C15.
    now: with no fund the rows and the fund tax line do not appear.
    why: The inputs of each table are set by the program.
- old line 658: | Pension/Provident rows (if applicable) + single new OM Optimal RA row = [MAXIMUM RA CONTRIBUTION].
    now: return (existing_rows(a) if a.get("ra_decision") == "keep" else "") + new_ra_row(ctx["proposed"])
    why: The inputs of each table are set by the program.
- old line 658: No existing RA rows regardless of client situation.
    now: ra_rows(a) if a["existing_ras"] else "", "[PENSION_BLOCK]":
    why: The inputs of each table are set by the program.
- old line 659: Table 3 — What you have requested | Shows the proposed new OM Optimal RA premium.
    now: Table 3, what is proposed | the proposed premium (replace), or the existing total + the proposed premium (keep) | replace:
    why: The inputs of each table are set by the program.
- old line 659: Structure depends on the replace vs keep decision (Startup Question 9).
    now: ("Replace or keep the existing RA(s)", {"none":
    why: The inputs of each table are set by the program.
- old line 659: single new OM RA row only.
    now: the new RA row only;
    why: The inputs of each table are set by the program.
- old line 659: existing RA row(s) + new OM RA row — combined tax saving shown.
    now: return (existing_rows(a) if a.get("ra_decision") == "keep" else "") + new_ra_row(ctx["proposed"])
    why: The inputs of each table are set by the program.
- old line 659: Pension/Provident rows (if applicable) + single new OM Optimal RA row only.
    now: "Monthly Retirement Annuity Contribution (New OM Optimal RA)".
    why: The inputs of each table are set by the program.
- old line 659: Pension/Provident rows (if applicable) + existing RA row(s) + new OM Optimal RA row.
    now: pension fund, provident fund, or self-employed / no fund (an existing RA does not change the wording).
    why: The inputs of each table are set by the program.
- old line 661: Pension/Provident rows appear in ALL THREE tables — not Table 1 only.
    now: Pension and provident rows appear in all three tables;
    why: The inputs of each table are set by the program.
- old line 661: Fund amounts are identical across all three tables.
    now: Pension and provident rows appear in all three tables;
    why: The inputs of each table are set by the program.
- old line 661: Only the RA contribution line(s) change across tables.
    now: only the RA rows change.
    why: The inputs of each table are set by the program.
- old line 664: Table 2 RA contribution = (C15 − total annual fund contributions) ÷ 12.
    now: Table 2, the full deduction | [MAXIMUM RA CONTRIBUTION] = (cap - the yearly fund contributions) / 12 | one new OM Optimal RA row;
    why: The inputs of each table are set by the program.
- old line 664: The fund and RA together must equal C15.
    now: Alwyn is the Old Mutual broker consultant who generates the RGAR and the OM Optimal RA Quote (he must always set the RGAR's ACI at 10% p.a.).
    why: The inputs of each table are set by the program.
- old line 664: The RA is NOT a separate allowance on top of the fund.
    now: the fund contributions already use the whole yearly allowance (the maximum RA is R %s a month):
    why: The inputs of each table are set by the program.
- old line 664: No existing client RA rows ever appear in Table 2.
    now: No client data is ever kept in the skill.
    why: The inputs of each table are set by the program.
- old line 667: Table 1 must always show the tax saved on the client’s existing RA contributions.
    now: Table %s tax saved from the RA is R %s and Table 1 tax payable minus Table %s tax payable is R %s%s" %
    why: The inputs of each table are set by the program.
- old line 667: Never show R– for tax saved if the client currently has an RA contributing.
    now: tax saved from the RA", "R %s;
    why: The inputs of each table are set by the program.
- old line 667: R– only appears if the client genuinely has no existing RA and no fund.
    now: existing_ras is [] when the client has none (then ra_decision is none);
    why: The inputs of each table are set by the program.
- old line 670: ## 8.3 Label Rule — Pension vs Provident
    now: elif ft not in ("none", "pension", "provident"):
    why: Enforced by the program.
- old line 672: Client’s Fund Type | Correct Label |
    now: e.name("fund in the %s" % label, f["name"]))
    why: Enforced by the program.
- old line 674: Pension Fund client | Tax Saved from Pension Fund Deduction |
    now: "Tax Saved from Pension Fund Deduction", "provident":
    why: Enforced by the program.
- old line 675: Provident Fund client | Tax Saved from Provident Fund Deduction |
    now: "Tax Saved from Provident Fund Deduction"},
    why: Enforced by the program.
- old line 676: No fund (self-employed or no employer fund) | This row does not appear |
    now: pension fund, provident fund, or self-employed / no fund (an existing RA does not change the wording).
    why: Enforced by the program.
- old line 678: *Never use ‘Pension Fund’ label when the client has a Provident Fund.
    now: REQUIRED when the client has a fund |
    why: Enforced by the program.
- old line 680: ## 8.4 How Tables Appear in Email
    now: Pension and provident rows appear in all three tables;
    why: Kept.
- old line 682: All three tables recreated in HTML — dark green headers, light green input cells, white output rows, orange message box.
    now: one line per check in point form, each with a green tick or a red cross, one closing line for what is only attested.
    why: Kept.
- old line 684: Pension/Provident rows use the same light green styling as all other input rows.
    now: Pension and provident rows appear in all three tables;
    why: Kept.
- old line 686: ## 8.5 ‘What You Can Save’ Sentence — Construction Rules
    now: the 'what you can save' sentence is missing or not the scenario's wording")
    why: Chosen by the program.
- old line 688: *The figure is always C15 ÷ 12 — the total monthly SARS allowable cap across ALL retirement vehicles.
    now: The "what you can save" sentence always uses [TOTAL CAP MONTHLY] (never the remaining RA room), in the wording of the client's scenario:
    why: Chosen by the program.
- old line 688: Never use the remaining RA room alone.
    now: print("Name to use in the RA transaction folder's Comparative Quotes:
    why: Chosen by the program.
- old line 690: The sentence is constructed dynamically based on the client’s actual retirement vehicle situation:
    now: registered, or Paul's words (for example "the client has no retirement annuities") |
    why: Chosen by the program.
- old line 692: Client Scenario | Sentence to Use |
    now: The program's first lines give you one sentence to say to Paul before anything else:
    why: Chosen by the program.
- old line 694: Employed with Provident Fund only (no existing RA) | “Based on your current earnings, you can save a total of R [TOTAL CAP MONTHLY] per month across all retirement vehicles (Provident Fund and Retirem
    now: "Based on your current earnings, you can save a total of <strong>R {total}</strong> per month towards a Retirement Annuity to take full advantage of the tax-deductible benefit offered to you by SARS."
    why: Chosen by the program.
- old line 695: Employed with Pension Fund only (no existing RA) | “Based on your current earnings, you can save a total of R [TOTAL CAP MONTHLY] per month across all retirement vehicles (Pension Fund and Retirement 
    now: "Based on your current earnings, you can save a total of <strong>R {total}</strong> per month towards a Retirement Annuity to take full advantage of the tax-deductible benefit offered to you by SARS."
    why: Chosen by the program.
- old line 696: Employed with both Pension AND Provident Fund | “Based on your current earnings, you can save a total of R [TOTAL CAP MONTHLY] per month across all retirement vehicles (Pension Fund, Provident Fund an
    now: "Based on your current earnings, you can save a total of <strong>R {total}</strong> per month towards a Retirement Annuity to take full advantage of the tax-deductible benefit offered to you by SARS."
    why: Chosen by the program.
- old line 697: Self-employed OR employed with no pension or provident fund | “Based on your current earnings, you can save a total of R [TOTAL CAP MONTHLY] per month towards a Retirement Annuity to take full advanta
    now: "Based on your current earnings, you can save a total of <strong>R {total}</strong> per month towards a Retirement Annuity to take full advantage of the tax-deductible benefit offered to you by SARS."
    why: Chosen by the program.
- old line 698: Employed with existing RA and Provident Fund | “Based on your current earnings, you can save a total of R [TOTAL CAP MONTHLY] per month across all retirement vehicles (Provident Fund and Retirement An
    now: "Based on your current earnings, you can save a total of <strong>R {total}</strong> per month towards a Retirement Annuity to take full advantage of the tax-deductible benefit offered to you by SARS."
    why: Chosen by the program.
- old line 699: Employed with existing RA and Pension Fund | “Based on your current earnings, you can save a total of R [TOTAL CAP MONTHLY] per month across all retirement vehicles (Pension Fund and Retirement Annuit
    now: "Based on your current earnings, you can save a total of <strong>R {total}</strong> per month towards a Retirement Annuity to take full advantage of the tax-deductible benefit offered to you by SARS."
    why: Chosen by the program.
- old line 701: *[TOTAL CAP MONTHLY] calculation steps:
    now: 1 [TOTAL CAP MONTHLY] = cap / 12;
    why: Chosen by the program.
- old line 703: B35 = annual remuneration + (employer fund contributions × 12)
    now: Calcs!C15 is the binding allowance = MIN(R430,000, 27.5% x Calcs!B35), where Calcs!B35 = annual remuneration + the employer fund contributions (a fringe benefit added back).
    why: The tool is run by the program, never by hand.
- old line 705: C15 = MIN(R430,000, 27.5% × B35)
    now: The tax cap is R 430,000 and 27.5%.
    why: Chosen by the program.
- old line 709: [MAXIMUM RA CONTRIBUTION] = (C15 − total annual fund contributions) ÷ 12 — use this in Table 1 SAVINGS OPPORTUNITIES rows and Table 2 RA input only
    now: Table 2, the full deduction | [MAXIMUM RA CONTRIBUTION] = (cap - the yearly fund contributions) / 12 | one new OM Optimal RA row;
    why: Chosen by the program.
- old line 711: ## 8.6 Pre-Delivery Figure Audit — Mandatory
    now: (6) let it autosave (wait about 8 seconds) and confirm.
    why: Proved by the program.
- old line 713: Before delivering any proposal, Claude must verify ALL of the following:
    now: out.append("the surname must be part of the client's full name")
    why: Proved by the program.
- old line 717: 1 | [TOTAL CAP MONTHLY] = C15 ÷ 12 — traces back to Tax Reform Tool |
    now: 1 [TOTAL CAP MONTHLY] = cap / 12;
    why: Chosen by the program.
- old line 718: 2 | [MAXIMUM RA CONTRIBUTION] = (C15 − total annual fund contributions) ÷ 12 — traces back to Tax Reform Tool |
    now: Table 2, the full deduction | [MAXIMUM RA CONTRIBUTION] = (cap - the yearly fund contributions) / 12 | one new OM Optimal RA row;
    why: Chosen by the program.
- old line 719: 3 | Table 1, 2 and 3 tax payable figures all differ correctly from each other |
    now: 3 the tax payable of Tables 1, 2 and 3 all differ;
    why: Chosen by the program.
- old line 720: 4 | Tax saved (RA) in Table 2 = Table 1 tax payable − Table 2 tax payable |
    now: Table %s tax saved from the RA is R %s and Table 1 tax payable minus Table %s tax payable is R %s%s" %
    why: Chosen by the program.
- old line 721: 5 | Tax saved (RA) in Table 3 = Table 1 tax payable − Table 3 tax payable |
    now: Table %s tax saved from the RA is R %s and Table 1 tax payable minus Table %s tax payable is R %s%s" %
    why: Chosen by the program.
- old line 722: 6 | Table 2 PF rows + RA row monthly total = [TOTAL CAP MONTHLY] (full cap used) |
    now: 6 Table 2's fund rows + RA row = [TOTAL CAP MONTHLY];
    why: Chosen by the program.
- old line 723: 7 | Table 3 % remaining = (C15 − Table 3 total annual contributions) ÷ C15 × 100 |
    now: 6 Table 2's fund rows + RA row = [TOTAL CAP MONTHLY];
    why: Chosen by the program.
- old line 724: 8 | Bar chart Year 1 saving = Table 3 RA tax saving (same RA amount in year 1) |
    now: 8 the bar chart's year 1 = Table 3's tax saved from the RA;
    why: Chosen by the program.
- old line 725: 9 | ‘What you can save’ sentence figure = [TOTAL CAP MONTHLY] — correct scenario sentence used |
    now: 9 the "what you can save" sentence carries [TOTAL CAP MONTHLY] in the right scenario wording.
    why: Chosen by the program.
- old line 726: 10 | Zero placeholder tags [LIKE THIS] remain in the document (except [CLIENT EMAIL] and [CC EMAIL]) |
    now: """Reads a client document's text (PDF or HTML/text), page by page, and checks that what the chat entered really appears in it.
    why: Chosen by the program.
- old line 728: *Note on Checks 4 & 5:
    now: R.add(True, "%d other program checks on the built email passed" % (len(res) - len(badr)))
    why: Proved by the program.
- old line 728: these two checks can legitimately fail to hold exactly, or even go negative, in a ‘keep some, replace some’ scenario where the new proposed RA total is close to or lower than the client’s current comb
    now: The "what you can save" sentence always uses [TOTAL CAP MONTHLY] (never the remaining RA room), in the wording of the client's scenario:
    why: Proved by the program.
- old line 728: an existing RA is kept in force and the replacement premium is similar in size to the RA(s) it replaces).
    now: flags.append("The client has an existing RA but the tool shows no tax saved from it in Table 1 (the income may be below the tax threshold).")
    why: Proved by the program.
- old line 728: This is not a calculation error — flag it to the adviser as a finding rather than forcing the figures to reconcile artificially.
    now: %r is not a date (enter DD/MM/YYYY, or leave it empty if the report does not show it)" % (label, value)
    why: Proved by the program.
- old line 728: Use the Tax Reform Tool’s own native output cells for ‘tax saved’ in all cases rather than back-calculating from the payable difference.
    now: Always use the tool's own native "tax saved" cells, never back-calculate them.
    why: Proved by the program.
- old line 730: THE RGAR — HOW TO USE IT
    now: 1 | Run it | The one command that starts the job and how every step works |
    why: Kept.
- old line 732: Always use the SECOND shortfall figure — from ‘WHAT YOU HAVE AGREED TO DO AND WHY’.
    now: rgar | The RGAR PDF from Alwyn (the SECOND shortfall table, "WHAT YOU HAVE AGREED TO DO AND WHY", is the one used).
    why: Kept.
- old line 732: NOT the first ‘WHAT YOU NEED TO DO’ figure.
    now: The program's first lines give you one sentence to say to Paul before anything else:
    why: Kept.
- old line 736: monthly shortfall amount, years to retirement, current monthly expenses, future value, retirement age.
    now: out.append("rgar needs exactly shortfall, years, current_value, future_value, retirement_age")
    why: Kept.
- old line 738: The RGAR is sent to the client in a separate email before the OM Optimal RA proposal.
    now: The RGAR is sent to the client in a separate email before this proposal (by rgar-skill);
    why: Kept.
- old line 740: THE OM OPTIMAL RA QUOTE — HOW TO USE IT
    now: Use when Paul asks for an OM Optimal RA proposal."
    why: Heading replaced.
- old line 742: ## 10.1 New Quote Format
    now: "OM Optimal RA Quote (Plan 1)", "fact_find_summary":
    why: Kept.
- old line 744: All new quotes from Alwyn use the format:
    now: "RGAR report (from Alwyn)", "lump_sum_quote":
    why: Kept.
- old line 744: ‘Old Mutual Savings and Income — Optimal Retirement Annuity Plan Quote Report’.
    now: New quotes are titled "Old Mutual Savings and Income - Optimal Retirement Annuity Plan Quote Report".
    why: Kept.
- old line 744: The ongoing advice fee (0.575%) is explicitly stated under ‘PAYABLE FROM THE PLAN’S FUND VALUE — Asset advice fees’.
    now: the tool's own tax saved from the RA is R %s but Table 1 tax payable minus Table %s tax payable is R %s:
    why: Kept.
- old line 746: ## 10.2 What to Extract
    now: """What Paul's yes is bound to:
    why: Every figure is checked against the quote's text.
- old line 748: Monthly premium and start date
    now: Source of the premium, start date, funds, allocations and every fee.
    why: Every figure is checked against the quote's text.
- old line 750: ACI rate (always 10%) and first increase date
    now: The ACI is always 10% p.a.
    why: Every figure is checked against the quote's text.
- old line 754: Fund names and allocation percentages — for Investment Fund Details table AND ‘funds recommended’ sentence AND attachment point 2
    now: <!-- INVESTMENT FUND DETAILS (PLAN 2) -->
    why: Every figure is checked against the quote's text.
- old line 756: 3.05% — verify each time)
    now: 2000-01-01 00:00 (Athens time)
    why: Every figure is checked against the quote's text.
- old line 758: Monthly fixed admin fee rand amount (varies — verify each time)
    now: out.append("monthly_admin_fee %r is not an amount" % a.get("monthly_admin_fee"))
    why: Every figure is checked against the quote's text.
- old line 760: Asset management fees per fund — calculate blended average based on allocation %
    now: the asset management fee is the blend of the funds weighted by their allocation;
    why: Every figure is checked against the quote's text.
- old line 762: Ongoing advice fee % (under ‘PAYABLE FROM THE PLAN’S FUND VALUE’)
    now: Old Mutual Fund Fact Sheet(s) for the Plan 2 fund selection above</td></tr>
    why: Every figure is checked against the quote's text.
- old line 768: ## 10.3 The Lump Sum Quote (Plan 2) — When Startup Question 11 Is Yes
    now: "OM Lump Sum Quote (Plan 2)"}
    why: Kept.
- old line 770: When a lump sum (Section 14 transfer or voluntary funds) is going into the new OM Optimal RA, Alwyn issues a SEPARATE quote for this amount, in addition to the standard recurring-premium quote.
    now: A lump sum (Section 14 or voluntary) never counts toward the 27.5% / R430,000 limit and is never added to the Tax Reform Tool's inputs.
    why: Kept.
- old line 770: Both share the same contract/policy number once issued (Plan 1 = recurring premium, Plan 2 = lump sum) but are quoted, and must be read, independently.
    now: OM_Optimal_RA_Proposal_TEMPLATE.html (the recurring premium, Plan 1, only) and OM_Optimal_RA_LumpSum_Proposal_TEMPLATE.html (the lump sum, Plan 2, only).
    why: Kept.
- old line 772: Do not assume the Lump Sum Quote uses the same fund selection, allocation, or fee structure as the recurring-premium quote — read it directly, exactly as with any other quote.
    now: Should you at any point need to stop the RA or cancel the premium, there are no penalties to you as the client, only an admin charge of R 300.00</p>
    why: Kept.
- old line 774: Extract from the Lump Sum Quote:
    now: its own funds and fees from the Lump Sum Quote;
    why: Kept.
- old line 774: the lump sum amount, fund selection and allocation, and any fees specific to the lump sum investment.
    now: its own funds and fees from the Lump Sum Quote;
    why: Kept.
- old line 776: This information populates the separate Lump Sum Investment proposal document (Section 6.5) — never merged into the Plan 1 fund/fee tables in the main proposal.
    now: the main proposal and the separate Lump Sum Investment proposal built from the fixed templates, the checks on what was built, the
    why: Kept.
- old line 778: The Lump Sum Quote must be uploaded to the project files and attached to the SEPARATE Lump Sum Investment proposal email — not the main proposal email.
    now: (5) where a lump sum applies, (2) to (4) were repeated for the separate Lump Sum Investment email (a second run).
    why: Kept.
- old line 780: The lump sum amount itself is never added to the Tax Reform Tool’s monthly RA contribution input — see Section 6.5.3.
    now: A lump sum is never added to the tool's inputs;
    why: Kept.
- old line 786: 1 | Main proposal email as HTML file — populated from OM_Optimal_RA_Proposal_CLAUDE_TEMPLATE_22_07_26.html.
    now: "scripts/run.py build (scripts/oriemail.py fills assets/OM_Optimal_RA_LumpSum_Proposal_TEMPLATE.html)",
    why: Kept.
- old line 786: All three tax tables (with correct Pension/Provident rows in every table), bar chart, fees table, and Investment Fund Details table embedded — Plan 1 (recurring premium) only.
    now: The pension or provident rows appear in all three tables, identical in amount;
    why: Kept.
- old line 786: Ready to Ctrl+A, Ctrl+C, paste into Outlook.
    now: print("  text to paste into the Outlook draft:
    why: Kept.
- old line 787: 2 | If Startup Question 11a is Yes:
    now: n = 2 if o.doc_of(a) == "lump_sum" else 4
    why: Kept.
- old line 787: a SECOND, separate Lump Sum Investment proposal email as HTML file — populated from OM_Optimal_RA_LumpSum_Proposal_TEMPLATE.html.
    now: os.path.join(ASSETS, "OM_Optimal_RA_LumpSum_Proposal_TEMPLATE.html")}
    why: Kept.
- old line 787: Covers Plan 2 (the lump sum) only — no tax tables.
    now: w.die("The lump sum email has no tax tables:
    why: Kept.
- old line 787: Ready to Ctrl+A, Ctrl+C, paste into a separate Outlook email.
    now: print("  text to paste into the Outlook draft:
    why: Kept.
- old line 789: Adviser workflow (no lump sum):
    now: "advice_fee", "adviser_charge", "monthly_admin_fee", "lump_sum_applies"},
    why: Kept.
- old line 789: open the main proposal HTML in Chrome → Ctrl+A → Ctrl+C → new Outlook email → Ctrl+V → fill in TO and CC → attach 4 PDFs → send.*
    now: (2) open the draft in Outlook on the web with Claude in Chrome (a new tab;
    why: Kept.
- old line 791: Adviser workflow (lump sum applies):
    now: "advice_fee", "adviser_charge", "monthly_admin_fee", "lump_sum_applies"},
    why: Kept.
- old line 791: repeat the above for the main proposal (attach the standard recurring-premium quote + fund fact sheets + booster value doc + strategy summary), THEN separately open the Lump Sum Investment proposal HT
    now: The attachments list is always exactly the 4 standard items (RA Quote, Fund Fact Sheets, RA Booster Value, Wealth Investment Strategy Summary), whether or not an RGAR was requested;
    why: Kept.
- old line 791: Two emails, two attachments sets, sent together or in close succession.*
    now: to_set, cc_set = set().union(*[_emails(x) for x in to_v]) if to_v else set(), set().union(*[_emails(x) for x in cc_v]) if cc_v else set()
    why: Kept.
- old line 793: *Permanent rule (added post-V6.3, correction logged 04/08/26):
    now: never forced (Paul, 04/11/2026:
    why: Kept.
- old line 793: the "Please see attached:" list on the main OM Optimal RA Proposal email is always exactly the 4 standard items above — never 5.
    now: "The attachments list has exactly the 4 standard items and never the RGAR" if not att else "Attachments problem:
    why: Kept.
- old line 793: The RGAR is NOT attached to this email even when the client requested one, even when the RGAR PDF has been uploaded to the conversation, and even when the RGAR paragraph in the body is populated with 
    now: add(client in flat.lower() and o.CC_EMAIL in flat.lower(), "The client (%s) and %s are on the draft (the read-back has no separate To and Cc fields)" % (a["client_email"].strip(), o.CC_NAME))
    why: Kept.
- old line 793: The RGAR is delivered to the client separately and independently via the rgar-skill workflow.
    now: The RGAR is sent to the client in a separate email before this proposal (by rgar-skill);
    why: Kept.
- old line 793: Do not add "Old Mutual Retirement Goal Analysis Report" (or any equivalent wording) as an attachment line on this template under any circumstance.
    now: add(not att and bt.count("Retirement Goal Analysis Report") <= 1 and "5.
    why: Kept.
- old line 799: Tax deductibility cap | Always R430,000 p.a.
    now: the ACI (always 10% p.a.;
    why: Fixed text lives in the templates.
- old line 800: Transaction Admin Fee | Always R300 maximum (NOT R345).
    now: The transaction admin charge is always R 300.00.
    why: Fixed text lives in the templates.
- old line 801: Monthly fixed admin fee | Varies per quote.
    now: The monthly fixed administration fee comes from the quote.
    why: Fixed text lives in the templates.
- old line 801: Always read directly from quote.
    now: Fees are read from THIS quote every time:
    why: Fixed text lives in the templates.
- old line 802: RGAR shortfall figure | Always use SECOND shortfall (after proposed RA factored in).
    now: The shortfall is the SECOND shortfall table (after the proposed RA is factored in), never the first.
    why: Fixed text lives in the templates.
- old line 803: ACI | Always 10% p.a.
    now: the ACI (always 10% p.a.;
    why: Fixed text lives in the templates.
- old line 803: Must match RGAR and quotation.
    now: it must match the RGAR and the quote), the first increase date, the commitment term in years and the booster schedule.
    why: Fixed text lives in the templates.
- old line 804: Ongoing advice fee | Always 0.575% p.a.
    now: <tr><td style="font-size:10pt;padding:5px 14px;">Ongoing advice fee</td><td style="font-size:10pt;text-align:right;padding:5px 14px;">[ADVICE FEE]%</td></tr>
    why: Fixed text lives in the templates.
- old line 804: Stated explicitly in new quote format.
    now: Start again in a new run folder.", 3)
    why: Fixed text lives in the templates.
- old line 806: Pension end date | Never include.
    now: Never include an end date for the fund.
    why: Fixed text lives in the templates.
- old line 806: [client B] end date was a one-off exception.
    now: the tool was given the rand amounts as a share of the gross income." %
    why: Fixed text lives in the templates.
- old line 807: CPI line in Risk Profile section | Removed.
    now: text = "\n".join(" ".join(line.split()) for line in raw.splitlines() if line.strip())
    why: Fixed text lives in the templates.
- old line 808: Product description sentences | Both sentences in one paragraph:
    now: exactly one of the two approved sentences (Section 14 transfer, or voluntary funds), never paraphrased;
    why: Fixed text lives in the templates.
- old line 808: It is a disciplined vehicle…’ |
    now: It is a disciplined vehicle to provide for retirement capital.</p>
    why: Fixed text lives in the templates.
- old line 809: Font | Aptos 11pt throughout the entire email body.
    now: Font matches the surrounding body text.
    why: Fixed text lives in the templates.
- old line 810: Pension/Provident rows in tax tables | Must appear in ALL THREE tables — not Table 1 only.
    now: Pension and provident rows appear in all three tables;
    why: Fixed text lives in the templates.
- old line 810: Amounts identical across all three.
    now: """Run the scenarios (identical ones once).
    why: Fixed text lives in the templates.
- old line 811: Pension vs Provident label | Output row must say ‘Provident Fund Deduction’ for Provident Fund clients.
    now: The label is "Provident Fund" for a provident client and "Pension Fund" for a pension client, never mixed;
    why: Fixed text lives in the templates.
- old line 811: Never ‘Pension Fund’ label for a Provident Fund client.
    now: Never an end date on the pension or provident fund line.
    why: Fixed text lives in the templates.
- old line 812: RA remaining room calculation | (C15 − total annual fund contributions) ÷ 12.
    now: Table 2, the full deduction | [MAXIMUM RA CONTRIBUTION] = (cap - the yearly fund contributions) / 12 | one new OM Optimal RA row;
    why: Fixed text lives in the templates.
- old line 812: Fund and RA together must stay within C15.
    now: Alwyn is the Old Mutual broker consultant who generates the RGAR and the OM Optimal RA Quote (he must always set the RGAR's ACI at 10% p.a.).
    why: Fixed text lives in the templates.
- old line 813: ‘What you can save’ figure | Always C15 ÷ 12.
    now: the 'what you can save' sentence is missing or not the scenario's wording")
    why: Fixed text lives in the templates.
- old line 813: Never the remaining RA room alone.
    now: The "what you can save" sentence always uses [TOTAL CAP MONTHLY] (never the remaining RA room), in the wording of the client's scenario:
    why: Fixed text lives in the templates.
- old line 813: Sentence wording varies by client scenario — see Section 8.5.
    now: the 'what you can save' sentence is missing or not the scenario's wording")
    why: Fixed text lives in the templates.
- old line 814: Personal circumstances wording | Always ‘You are working at [employer]…’ — never ‘You will be working.’ |
    now: "You are working at [employer] in the position of [position]." (never "You will be working").
    why: Fixed text lives in the templates.
- old line 815: Table 1 tax saved on existing RA | Must always be shown if the client currently has an RA contributing.
    now: out.append("existing_ras must be a list (empty when the client has none)")
    why: Fixed text lives in the templates.
- old line 815: Never R– unless the client genuinely has no RA at all.
    now: R.add(True, "The lump sum email has no tax tables:
    why: Fixed text lives in the templates.
- old line 816: Table 2 RA rows | A single new OM Optimal RA row showing [MAXIMUM RA CONTRIBUTION] only.
    now: 6 Table 2's fund rows + RA row = [TOTAL CAP MONTHLY];
    why: Fixed text lives in the templates.
- old line 816: Existing client RA rows never appear in Table 2 under any circumstances.
    now: flags.append("The client has an existing RA but the tool shows no tax saved from it in Table 1 (the income may be below the tax threshold).")
    why: Fixed text lives in the templates.
- old line 817: Table 3 RA rows — replace scenario | Single new OM Optimal RA row only.
    now: "Monthly Retirement Annuity Contribution (New OM Optimal RA)".
    why: Fixed text lives in the templates.
- old line 817: Existing RA does not appear.
    now: "keeping the existing RA"}.get(a["ra_decision"], "?"))
    why: Fixed text lives in the templates.
- old line 818: Table 3 RA rows — keep scenario | Existing RA row(s) + new OM Optimal RA row.
    now: ("Replace or keep the existing RA(s)", {"none":
    why: Fixed text lives in the templates.
- old line 818: Combined tax saving must be shown.
    now: the fund statement must be registered" % ft)
    why: Fixed text lives in the templates.
- old line 819: Replace vs keep question | Mandatory Startup Question 9.
    now: ("Replace or keep the existing RA(s)", {"none":
    why: Fixed text lives in the templates.
- old line 819: Must be answered before any proposal is built.
    now: The RGAR is sent to the client in a separate email before this proposal (by rgar-skill);
    why: Fixed text lives in the templates.
- old line 820: Upload existing RAs | Mandatory Startup Question 10.
    now: ra_rows(a) if a["existing_ras"] else "", "[PENSION_BLOCK]":
    why: Fixed text lives in the templates.
- old line 820: Client must upload all current RAs (active/paid up), or confirm there are none, before any proposal is built.
    now: The RGAR is sent to the client in a separate email before this proposal (by rgar-skill);
    why: Fixed text lives in the templates.
- old line 821: Tax Reform Tool version | Always use TEMPLATE_4.
    now: WORKBOOK = os.path.join(ASSETS, "Tax_Reform_Tool_TEMPLATE_4.xlsm")
    why: Fixed text lives in the templates.
- old line 821: Never use earlier versions — they contain wrong brackets and stale cached values.
    now: assets/Tax_Reform_Tool_TEMPLATE_4.xlsm is the only correct version (earlier versions had stale values and wrong tax brackets).
    why: Fixed text lives in the templates.
- old line 822: Pre-delivery audit | Mandatory for every proposal.
    now: Use when Paul asks for an OM Optimal RA proposal."
    why: Fixed text lives in the templates.
- old line 822: All 10 audit checks in Section 8.6 must pass before delivery.
    now: *The audit checks the program proves (old Step 7 and MCD 8.6):
    why: Fixed text lives in the templates.
- old line 828: Alwyn | OM Broker Consultant — generates RGAR and OM Optimal RA Quote.
    now: Alwyn is the Old Mutual broker consultant who generates the RGAR and the OM Optimal RA Quote (he must always set the RGAR's ACI at 10% p.a.).
    why: Kept.
- old line 828: Must always set RGAR ACI at 10% p.a.
    now: Alwyn must always set its ACI at 10% p.a.:
    why: Kept.
- old line 829: Astute FSE | Electronic financial data exchange platform — provides Consolidated Client Portfolio (CCP) showing all existing policies across all major SA life insurers.
    now: Astute FSE is the electronic data-exchange platform that provides the Consolidated Client Portfolio (CCP):
    why: Kept.
- old line 831: Version 5.0 — July 2026 | This document must be updated whenever any product details, tax rules, fees, processes or template changes are agreed.
    now: out.append("document must be %r in this run" % document)
    why: Kept.
- old line 831: Always use the latest version.*
    now: Always use the tool's own native "tax saved" cells, never back-calculate them.
    why: Kept.


DROPPED (each is covered by a recorded decision):
- # OM Optimal RA Proposal Builder: Replaced by the new short title.
- ## Index: Replaced by the new short Index (five sections).
- ## UNIVERSAL OPERATING RULES - READ FIRST, APPLY TO EVERY STEP OF THE : Heading replaced by 'Rules that apply to every step' in references/00-rules.md.
- These rules come before everything else in this skill. They apply from: Replaced: the new skill is a program that shows its rules again at every step (the 'long chats get compressed' worry no longer applies).
- Re-load this skill before you start, and again after any compression. : Replaced by the program: the version line is said first and the steps are shown again at the right moment, so nothing is worked from memory.
- Changes to a skill: edit the existing skill, never create a new one. U: Replaced by S7: skills are changed only in Claude Code and uploaded as a zip (the propose_skills card is not used).
- Last updated: 2026-10-14 15:50 Athens time (EEST): The stamp is set by tools/stamp_skill.py, never typed (S2).
- > Standing rule — not optional: any edit to this skill (SKILL.md, the : Replaced by the stamp program (S2): the date moves on every real change.
- ## Changelog: The changelog is archived in this history folder (SKILL.2026-10-14.redacted.md); the new skill keeps the last 5 changes.
- ## Reference material: Replaced by SKILL.md 'Where the detail lives' and the new assets list (the .xlsm, the two templates, wording.json, tax_facts.json, settings.json). wr_logo.png is removed (unused: both templates carry their own embedded logo).  [NEEDS PAUL]
- ## A note on the MCD's own internal version lag: Stale (the old file names and 'Version 5.0' cited in the old reference file): the reference file is replaced by short pages, nothing is left to be out of step.
- # VERSION HISTORY: The reference file's version history is archived here (SKILL.2026-10-14.redacted.md); every rule in it that is still true is kept in the new pages.
- # 2. PROJECT FILES REFERENCE: Replaced: the old template file names are stale and the example quote and RGAR were two real clients' files (S11). What is kept: only TEMPLATE_4 of the Tax Reform Tool is correct (references/03-tax.md).  [NEEDS PAUL]
- ## 5.1 Template File: Replaced: the template file names are stale and the templates now live in assets/ with the program.
- ## 5.2 How Claude Uses the Template: Replaced by the program: it fills the templates; the 'Ctrl+A, Ctrl+C, paste into Outlook' workflow is not used any more (Claude in Chrome makes the draft).
- ## 5.3 Complete List of Placeholders: Replaced by the program: every placeholder is filled by scripts/oriemail.py from the confirmed answers and the tool results; the old list was out of step with the template (nine placeholders missing, twelve not listed, two of them described as 'left for the adviser to fill in').  [NEEDS PAUL]
