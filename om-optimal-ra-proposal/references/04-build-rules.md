# What the program builds, and the rules that never change

The program fills the fixed template from your confirmed answers and the tool results; you never edit the HTML. The layout is fully table-based and Outlook-compatible (`bgcolor` on every cell, `nowrap` on value cells, spacer rows, no flexbox, grid or divs). **Two files**: `OM_Optimal_RA_Proposal_TEMPLATE.html` (the recurring premium, Plan 1, only) and `OM_Optimal_RA_LumpSum_Proposal_TEMPLATE.html` (the lump sum, Plan 2, only).

**Files**: the full copy (with the logo) is sent to Paul in the chat as `[FirstName]_[Surname]_OM_Optimal_RA_Proposal_Email - DD.MM.YY.html` (the lump sum email: `..._OM_Optimal_RA_LumpSum_Proposal_Email - DD.MM.YY.html`); the no-logo copy is saved in the RA transaction folder's Comparative Quotes; `draft_body.html` is pasted into the Outlook draft (from "Dear X," down to the bold next-meeting line, with no header, no "Kind regards," and no signature).

**Fixed for every client**
- Risk profile is always "Moderate". The ACI is always 10% p.a. The transaction admin charge is always R 300.00. The tax cap is R 430,000 and 27.5%.
- "You are working at [employer] in the position of [position]." (never "You will be working"). Never an end date on the pension or provident fund line.
- Populated fields stay black (no orange). Font matches the surrounding body text.
- Conditional sentences, exactly: no existing RAs: "You have no active or Paid-Up Retirement Annuities."; no fund: "You have no Pension or Provident Fund with your employer."; no RGAR: "You did not request for a Retirement Goal Analysis Report."
- **The RGAR is never an attachment of this email.** The attachments list is always exactly the 4 standard items (RA Quote, Fund Fact Sheets, RA Booster Value, Wealth Investment Strategy Summary), whether or not an RGAR was requested; the RGAR goes separately through `rgar-skill`.
- The "what you can save" sentence always uses [TOTAL CAP MONTHLY] (never the remaining RA room), in the wording of the client's scenario: pension fund, provident fund, or self-employed / no fund (an existing RA does not change the wording).
- The table row label of the new RA: "Monthly Retirement Annuity Contribution (New OM Optimal RA)". The orange message under a table says how much deduction is left, or that it is maximised.
- Fees: the asset management fee is the blend of the funds weighted by their allocation; the total ongoing fees add up the figures as shown. The monthly fixed administration fee comes from the quote.
- The "once off lump sum" lines in Tables 1 and 3 are the Tax Reform Tool's own figure (the lump sum that would use up the deduction), present on every proposal. They are NOT the Section 14 or voluntary lump sum of the separate email.
- The lump sum email: heading "Your Lump Sum Investment:"; exactly one of the two approved sentences (Section 14 transfer, or voluntary funds), never paraphrased; no tax tables, bar chart or "what you can save" sentence; its own funds and fees from the Lump Sum Quote; attachments: the Lump Sum Quote and its fund fact sheet(s). Both emails go out separately, each with its own draft and Teams message.
- Weekdays are computed by the program, never typed. The meetings already held are written "Thursday, 29/10/2026" (several: "A, B & C"); the closing line is the bold next-meeting line.

The program checks the built email (no placeholder, tables open = close, header, weekdays, every figure and fixed sentence, the tool's tax figures and bar chart, fees add up, logo only in the full copy) before it lets the run continue.

**The save.** Save exactly the file the program names. Never truncate or retype the logo (base64) by hand. Use `sharepoint_upload_file` (driveId + parentItemId, `expectedBytes` = the file size, `conflictBehavior: "replace"` only after Paul's yes). Tell Paul the folder and the file name in plain words, and that the saved copy has no logo.
