<!-- The live skill text as of 14/10/2026 15:50 (Athens time), kept as the rule-by-rule baseline: SKILL.md followed by references/mcd_v6_3.md. Three real clients' names in the MCD were replaced by [client A], [client B], [client C] (the original is not kept in the repo). -->
---
name: "om-optimal-ra-proposal"
description: "Builds Old Mutual Optimal Retirement Annuity (RA) client proposal emails for Paul Kafentzis (FSP45946), then saves, drafts in Outlook and alerts Sitamah. Use when Paul asks for an OM Optimal RA proposal."
---

# OM Optimal RA Proposal Builder

## Index

| # | Section | What it covers |
|---|---|---|
| 1 | Universal operating rules + Delivery gate | The nine rules for every step, and what must be done before a run counts as complete |
| 2 | Last updated + Changelog | Athens-time stamp, standing edit rule, last changes |
| 3 | Overview + Why this exists | What the skill produces; Claude never sends the client email |
| 4 | Step 1 | The 12-item startup checklist (questions 9-12 mandatory) |
| 5 | Step 2 | Read the source documents carefully |
| 6 | Step 3 | Run the Tax Reform Tool (three scenarios) and its cell mapping |
| 7 | Step 4 | The three-table logic |
| 8 | Step 5 | The "what you can save" sentence; template defects to override |
| 9 | Step 6a | Populate the main proposal; fixed rules; conditional wording; RGAR never attached |
| 10 | Step 6b | The separate Lump Sum Investment proposal |
| 11 | Step 7 | Mandatory pre-delivery audit (12 checks) and the known edge case |
| 12 | Step 8 / 8a / 8b / 8c | Deliver: save to SharePoint; Outlook draft; Teams message to Sitamah via Zapier |
| 13 | Reference material + notes | The MCD, templates, tool; MCD version lag; scope |

## UNIVERSAL OPERATING RULES - READ FIRST, APPLY TO EVERY STEP OF THE TASK

*These rules come before everything else in this skill. They apply from the first message to the last, not just at the start, and they are repeated here at the top because long conversations get compressed and only the beginning of a skill survives. If anything below seems to conflict with these rules, these rules win.*

1. **Re-load this skill before you start, and again after any compression.** At the start of every run - and whenever the conversation has been summarised or compressed, or has run long - open this skill in full (Skill tool) and re-read it before you produce or change any deliverable. Never work from a summary of the rules or from memory of them.
2. **Source first - never invent.** Write only what is in the source material (transcript, quote, document, file) or in a named document this skill tells you to use. If a line is unclear, garbled or ambiguous, do not turn it into a fact: flag it to the user. "It seems implied", "it is usual" and "it would make sense" are not sources.
3. **Read before you write.** Read the source material completely and carefully - at least as many times as this skill requires - before drafting anything. Searching for keywords is not reading.
4. **Check before you claim.** Never tell the user something is done, saved, sent, visible or working until you have checked it yourself (open the file, list the folder, look at the screen). Say what you checked.
5. **Deliver everything this skill lists, every time.** A run is not finished until every deliverable this skill names has been produced AND handed over exactly the way this skill specifies (shown in chat, sent as a file in the chat, saved to the named folder). Before you reply, list each deliverable and confirm each was handed over.
6. **Every correction re-opens the whole task, not just the item.** When the user corrects anything: (a) go back to the source and re-check that point and everything related to it; (b) fix it everywhere it appears, in every deliverable; (c) re-run this skill's full checklist; (d) re-deliver every affected deliverable in full, as in rule 5. Never fix only the item named and stop.
7. **Never lower the standard.** A correction, a frustrated user, a short request or a "quick" task does not relax any rule in this skill.
8. **If a rule cannot be met, stop and say so.** State exactly which rule or step could not be completed and why. Never hand over partial work as if it were complete.
9. **Changes to a skill:** edit the existing skill, never create a new one. Update its "Last updated" stamp (Athens time) and changelog. Then put the full updated SKILL.md forward for the user to review and save using the propose_skills tool (the "Update skill" review card). Never say the change is live until the user confirms they saved it. If the card does not appear, say so plainly and ask the user how to proceed - do not claim it was delivered.

**Delivery gate for this skill (rules 5 and 6 applied):** a run is complete only when ALL of these are done and confirmed in one line each: (1) the startup checklist, source reading and Tax Reform Tool were completed (Steps 1-3); (2) the proposal HTML was built and the Step 7 mandatory pre-delivery audit was completed; (3) the HTML was sent in the chat with the exact required filename; (4) Step 8a (saved into the client's folder), Step 8b (Outlook draft, never sent by Claude) and Step 8c (Teams message to Sitamah, sent via Zapier) were each done and checked; (5) where a lump sum applies, (2) to (4) were repeated for the separate Lump Sum Investment proposal. After ANY correction, repeat (2) to (5) for every deliverable that changed.

**Last updated: 2026-10-14 15:50 Athens time (EEST)**

> **Standing rule — not optional:** any edit to this skill (SKILL.md, the template, the MCD reference or an asset) is not complete until the "Last updated" line above is rewritten to the current date and time (Athens time), and a changelog row is added, in the same response as the edit.

## Changelog
| When (Athens time) | What changed |
|---|---|
| 2026-10-14 15:50 | Index added; description made plain; the long changelog rows moved word for word to the Project doc; client names and example amounts in the text replaced with placeholders. No rule changed. |
| 2026-10-13 15:50 | Step 8c changed: the Teams message to Sitamah is now posted via Zapier (`microsoft_teams_send_chat_message`, format "markdown"), not Claude in Chrome; greeting always included. |
| 2026-10-08 14:34 | Rule 9 reworded: skill changes go forward with the propose_skills review card; never claim live until the user confirms they saved it. |
| 2026-10-08 13:55 | Universal operating rules block and Delivery gate added at the top. |
| 2026-10-01 14:05 | Brought in line with the OM Tax-Free skill: Sitamah always Cc; Steps 8a, 8b, 8c compulsory; Tax Reform Tool output cells corrected; audit items 11-12 added. |

Older entries (the "earlier" row) and the full text of every row above are in `om-optimal-ra-proposal-changelog.md` in the Project, word for word.

This skill packages Paul Kafentzis's proposal-building process for Old Mutual Optimal Retirement Annuity (OM Optimal RA) client emails. These are client-facing financial documents — precision matters more than speed. A wrong figure or an inconsistent sentence is a real-world error in front of a client, not a cosmetic slip. The output is an **HTML file** that is (a) saved into the client's folder, (b) put into an Outlook **draft** by Claude, and (c) flagged to Sitamah on Teams so she can attach the 4 documents **and email the client**. **Claude never sends the email to the client itself — Sitamah sends it from Drafts once the documents are attached (unless she can't, or Paul chooses to send it).**

## Why this exists

Every proposal follows the same three-table tax logic, the same HTML template, and the same client-scenario wording rules — but each client's underlying numbers are different, and it's easy to accidentally carry over a detail (a figure, a fund name, a wording choice) from a previous client if the rules aren't followed exactly. This skill exists so that discipline travels with Claude automatically, in any chat, without Paul having to re-explain it or manually clear out old client files first.

## Step 1 — Always run the startup checklist first

Before building anything, confirm all 12 items below are available. If any are missing, ask for them and wait — do not build a partial proposal.

1. Client Fact Find (personal details, age, employer, position, start date, gross income, retirement goal, risk profile)
2. Astute CCP Report or existing policy schedules (or confirmation there are none)
3. Pension/Provident Fund Statement (or confirmation there is none)
4. Proof of Income (POI) / Payslip
5. RGAR PDF from Alwyn (or confirmation none was requested)
6. OM Optimal RA Quote from Alwyn
7. Date(s) of Teams meeting(s) already held with the client
8. Date, day and time of the next scheduled Teams meeting
9. **Is the client's existing RA being replaced by the new OM Optimal RA, or kept in force alongside it?** (Not applicable if the client has no existing RA.)
10. **Confirmation that all current RAs (active/paid-up) have been uploaded, or a statement that there are none.**
11. **Lump Sum Investment** — broken into four sub-questions: (a) will a lump sum be going into the new OM Optimal RA, in addition to the recurring premium (Yes/No)? (b) if Yes, is it a Section 14 transfer or voluntary funds? (c) if Section 14 — which policy/policies and the Net Fund Value; if voluntary — source of funds and Rand amount; (d) upload the separate OM Lump Sum Quote (Plan 2). If (a) is No, (b)–(d) don't apply.
12. **Client Overview document** showing the "Current Investments" section — gross fund value, penalties, net fund value and monthly premium for each existing policy at a glance.

Questions 9, 10, 11 and 12 are mandatory and must be answered before any proposal is built — they are not optional even if the other items are complete. Question 9's answer drives the Recommendation wording, the structure of Table 3, and whether the penalty note applies. Question 11a's answer determines whether a **second, separate HTML document** (the Lump Sum Investment proposal) needs to be built alongside the main proposal — see Step 6b and `references/mcd_v6_3.md` Section 6.5.

## Step 2 — Read the source documents carefully

- Read the Fact Find, CCP report, fund statement, POI, RGAR, and Quote directly — don't assume values.
- If a Fact Find or other PDF has scanned/image pages, visually read the page images rather than relying only on extracted text — text layers often capture field labels but miss the client's actual filled-in answers.
- Fund selection, fees, ACI, and premium amounts always come from the specific client's quote — never assume they match a previous client's proposal, even if similar.

## Step 3 — Run the Tax Reform Tool (three scenarios)

Use `assets/Tax_Reform_Tool_TEMPLATE_4.xlsm` — this is the only correct version (earlier versions had stale cached values and wrong tax brackets).

- **B35** = annual remuneration + (employer fund contributions × 12)
- **C15** = MIN(R430,000, 27.5% × B35) — the binding SARS allowance
- **[TOTAL CAP MONTHLY]** = C15 ÷ 12 — used only in the "what you can save" sentence
- **[MAXIMUM RA CONTRIBUTION]** = (C15 − total annual fund contributions) ÷ 12 — used in Table 1's savings-opportunity row and as the Table 2 RA input

If the client has no Pension/Provident Fund, or fund contributions are excluded from this proposal, select "Self Employed" in the tool (write directly to `Calcs!B2`) so all fund-contribution rows zero out correctly. Never touch the VBA radio button controls with `openpyxl` — edit the underlying xlsm zip/XML directly if a value needs to change, since disturbing the radio buttons breaks the workbook.

To force full recalculation and read results reliably: convert headless with LibreOffice (`soffice --headless --calc --convert-to xlsx`) and then read output cells with `openpyxl` (`data_only=True`). Cells on the Maximise Allowance Tool sheet (**corrected 01/10/2026 against the actual workbook — the previous mapping was wrong**): inputs C15 (monthly remuneration), C17 (age), C20–C23 (fund contributions — set to 0 when the client has no Pension/Provident Fund), C24 (monthly RA); outputs **C28 = annual tax saved from RA**, C29 = tax saved from pension, C30 = tax saved from provident, **C31 = annual tax payable after deductions and rebate**, **C34 = % deduction left**, **C36 = additional monthly premium**, **C37 = once-off lump sum to maximise the deduction**. Reinvest Calcs `H41:Q41` gives the bar chart values for years 1–10; `Calcs!C15` is the cap. Always read the label next to a cell before trusting a mapping.

A client with **no Pension/Provident Fund and no existing RA** is handled by leaving C20–C23 at 0 (Table 1: RA = R–, tax saved R–; pension row removed from all three tables).

Run this three times per client — once per table scenario (Table 1: RA=0 / current situation, Table 2: RA=maximum, Table 3: RA=proposed premium) — and keep the outputs straight; mixing them up is the single easiest mistake to make.

## Step 4 — The three-table logic (read this carefully — it is the part most likely to go wrong)

| Table | Shows | RA row(s) |
|---|---|---|
| **Table 1** — current situation | The client's exact position today. | Pension/Provident row(s) if applicable, **plus one named row per existing RA** showing its current contribution. Tax saved on existing RA contributions must be shown as a real number — never R– unless the client truly has no RA and no fund. |
| **Table 2** — full tax deduction opportunity | The maximum 27.5% SARS room, using only the new OM Optimal RA. | Pension/Provident row(s) if applicable, **plus a single new OM Optimal RA row** = [MAXIMUM RA CONTRIBUTION]. Existing RA rows never appear here, regardless of the client's situation. |
| **Table 3** — what's being proposed | The proposed new OM Optimal RA premium, structured by the Question 9 answer. | **Replacing:** Pension/Provident row(s) if applicable, plus a single new OM Optimal RA row only. **Keeping:** Pension/Provident row(s) if applicable, plus the existing RA row(s), plus the new OM Optimal RA row — combined tax saving shown. |

Pension/Provident rows are identical in amount across all three tables — only the RA line(s) change. Use the label "Provident Fund Deduction" for provident-fund clients and "Pension Fund Deduction" for pension-fund clients — never mix them up.

## Step 5 — The "what you can save" sentence

Always uses [TOTAL CAP MONTHLY] (C15 ÷ 12) — never the remaining RA room alone. Pick the sentence variant matching the client's actual retirement-vehicle combination (Provident only, Pension only, both, existing RA + fund, or self-employed/no fund). See `references/mcd_v6_3.md` Section 8.5 for the exact wording of each variant — copy it verbatim and only substitute the figure and vehicle names.

**Template defects to override (found 01/10/2026):** the template's static text for "What you can save" and "You will be working…" is stale. Always use the MCD Section 8.5 variant sentence for the client's scenario and the wording "You are working at [employer]…". When the client has no Pension/Provident Fund, remove the pension/provident tax row from all three tables (do not leave an empty row). Table row label for the new RA in Tables 2 and 3: "Monthly Retirement Annuity Contribution (New OM Optimal RA)".

## Step 6a — Populate the main proposal (always built)

Use `assets/OM_Optimal_RA_Proposal_TEMPLATE.html` as the base for every proposal — never build the HTML from scratch. It's a fully table-based, Outlook-compatible layout: keep `bgcolor=` attributes on every cell, `nowrap` on value cells, table-row spacers instead of CSS margins, and don't introduce flexbox, CSS grid, or `<div>`-based layout.

This template covers the recurring monthly premium (Plan 1) **only**. As of MCD V6.3 it contains no lump sum content at all — the old `[LUMP_SUM_BLOCK]`/`[LUMP_SUM_FUND_FEE_BLOCK]` placeholders were removed from this template in the V6.3 restructure. Do not add lump sum wording here even if Question 11a is Yes — that goes in the separate document built in Step 6b.

Fixed rules that never change between clients:
- Risk profile is always "Moderate."
- ACI is always 10% p.a.
- Transaction admin fee is always R300.
- Personal circumstances wording is always "You are working at [employer]..." — never "You will be working."
- Never include an end date on the Pension/Provident Fund line.
- Font should match the surrounding body text — do not colour populated fields orange; keep them black. (Exception: the fixed "Penalties: To be determined if there are" line is deliberately orange per MCD Section 7.1 — a distinct styling convention from populated client data fields, which stay black.)

Conditional wording (use exactly, when the underlying fact applies):
- No existing RAs → "You have no active or Paid-Up Retirement Annuities."
- No Pension/Provident Fund → "You have no Pension or Provident Fund with your employer."
- No RGAR requested → "You did not request for a Retirement Goal Analysis Report."

**The RGAR is never listed as an attachment on the OM Optimal RA Proposal email — this is a permanent rule, not a per-client judgment call.** The attachments list under "Please see attached:" always stays at exactly the 4 standard items (RA Quote, Fund Fact Sheets, RA Booster Value, Wealth Investment Strategy Summary), regardless of whether an RGAR was requested, whether the RGAR PDF was uploaded to this conversation, or whether the RGAR paragraph itself is populated with real figures in the body. The RGAR is sent to the client separately, on its own, via the `rgar-skill` — never bundled as attachment #5 here. Do not add an RGAR line to this list under any circumstance.

Placeholder notes worth double-checking:
- `[RA_PENALTY_NOTE]`: italic "No penalties apply – policy is too new" if applicable, otherwise blank.
- `[T2_RA_ROWS]`: always the single new-RA row — see Step 4.
- `[T3_RA_ROWS]`: depends on replace vs keep — see Step 4.
- `[T1_FUND_ROWS]`: Pension/Provident block for Table 1 — omit entirely (leave blank) if the client has no Pension/Provident Fund.
- `[PENSION_BLOCK]`: the Personal Retirement Savings narrative block — see conditional wording above.
- `[T1 PCT REMAINING]` and `[T3 PCT REMAINING]` each appear **twice** in the template — replace both instances.
- `[T1 LUMP SUM]` / `[T3 LUMP SUM]`: NOT related to Question 11 — these are the Tax Reform Tool's own "once-off lump sum to maximise deduction" output cells (C36), present on every proposal regardless of whether an actual Section 14/voluntary lump sum applies.

The full placeholder-to-source mapping is in `references/mcd_v6_3.md`, Section 5.3 — check it if a placeholder's source is unclear.

## Step 6b — Build the Lump Sum Investment proposal (only if Startup Question 11a is Yes)

**Governance decision (V6.3, superseding the single-email approach in V6.0–V6.2):** whenever a lump sum applies, produce a **second, separate HTML document** — never a section bolted onto the main proposal.

Use `assets/OM_Optimal_RA_LumpSum_Proposal_TEMPLATE.html` as the base. This document covers the lump sum (Plan 2) only:
- Heading is always "Your Lump Sum Investment:"
- Contains NO tax tables, no bar chart, and no "what you can save" sentence — those belong only in the main proposal, since the lump sum has no bearing on the 27.5%/R430,000 annual deduction calculation.
- Shares the same signature block, adviser contact details, and branding as the main proposal.
- Both documents should be sent together (or in close succession) as two separate emails, each with their own attachment set.

Use exactly one of these two verbatim wordings — never paraphrase (there is no "no lump sum" variant here; if Question 11a is No, simply don't build this document at all):
- Section 14 transfer → "A lump sum amount of R [LUMP SUM AMOUNT] will be transferred into your new OM Optimal RA via a Section 14 transfer from your existing [SOURCE POLICY NAME(S)] policy/policies. This is a tax-neutral transfer between approved retirement funds and does not attract any tax at the point of transfer."
- Voluntary funds → "A lump sum amount of R [LUMP SUM AMOUNT] will be invested into your new OM Optimal RA from your own savings ([SOURCE OF FUNDS])."

For Section 14: `[LUMP SUM AMOUNT]` is always the **Net Fund Value** (never Gross) of the transferring polic(y/ies) — sum them if there's more than one, and name each policy. Old Mutual quotes the lump sum as a separate Plan 2 under the same contract number as the recurring premium (Plan 1); Alwyn issues a separate Lump Sum Quote for it — read its fund selection, allocation and fees independently via `[LS_FUND_FEE_BLOCK]`, never assume they match Plan 1. A lump sum (Section 14 or voluntary) never counts toward the 27.5%/R430,000 annual deduction limit and is never added to the Tax Reform Tool's contribution inputs used for the main proposal.

Other placeholders in this template: `[LS_TAX_TREATMENT_NOTE]` (tax-neutral confirmation for Section 14, or a flag-to-adviser note for voluntary funds — see MCD Section 6.5.2), `[PRODUCT START DATE]` (Plan 2 start date from the Lump Sum Quote).

Full detail: `references/mcd_v6_3.md` Sections 6.5, 6.5.1–6.5.5, and 10.3.

## Step 7 — Mandatory pre-delivery audit

Before calling anything finished, verify all of the following (from MCD Section 8.6):

1. [TOTAL CAP MONTHLY] = C15 ÷ 12, traceable to the Tax Reform Tool
2. [MAXIMUM RA CONTRIBUTION] = (C15 − total annual fund contributions) ÷ 12
3. Table 1, 2 and 3 tax-payable figures all genuinely differ from each other
4. Table 2 tax saved (RA) = Table 1 tax payable − Table 2 tax payable
5. Table 3 tax saved (RA) = Table 1 tax payable − Table 3 tax payable
6. Table 2's Pension/Provident rows + RA row monthly total = [TOTAL CAP MONTHLY]
7. Table 3's % remaining = (C15 − Table 3 total annual contributions) ÷ C15 × 100
8. Bar chart Year 1 saving = Table 3's RA tax saving
9. The "what you can save" sentence uses [TOTAL CAP MONTHLY] with the correct scenario wording
10. No placeholder tags `[LIKE THIS]` remain. The header "To:" is the client's real email address (never invented) and **"Cc:" is always "Sitamah Nathoo"** — never blank.
11. The HTML is **saved in the client's RA Comparative Quotes folder** and the upload was confirmed (Step 8a); the **Outlook draft exists** with To = client, Cc = Sitamah, subject identical to the HTML, bold headings and bordered tables, a single "Kind regards,", signature/logo present, importance High, **not sent by Claude** — verified by reading it back (Step 8b).
12. **Sitamah was messaged on Teams via Zapier and the posted message was read back and confirmed to render correctly** (no raw HTML tags, no literal `**`): it opens with a greeting ("Good morning/afternoon/evening Sitamah," by SAST time — see Step 8c), standard wording, the 4 attachments listed (never the RGAR), folder named, ending "Once attached, please email the client - Thank you!" (Step 8c).

If any check fails, fix it before delivering — don't flag it and hand it over half-checked (except the known edge case below, which is flagged, not forced).

**Known edge case (checks 4 & 5):** these can legitimately fail to hold exactly, or even go negative, in a "keep some, replace some" scenario where the proposed RA total is close to or lower than the client's current combined RA contribution. It also appears at the **maximum-contribution table when the extra deduction straddles a tax bracket** (seen 01/10/2026: native tax saved R[amount] versus a R[amount] payable difference; seen 13/10/2026: native R[amount] versus R[amount]). This is not a calculation error — flag it to Paul as a finding rather than forcing the figures to reconcile artificially. Always use the Tax Reform Tool's own native output cells for "tax saved" rather than back-calculating from the payable difference.

## Step 8 — Deliver

Deliver the finished HTML to Paul in the chat (`SendUserFile`), then complete Steps 8a–8c — **the build is not finished until all three are done.** Name the file `[FirstName]_[Surname]_OM_Optimal_RA_Proposal_Email - [DD.MM.YY].html`. Header: **To** = the client's email, **Cc = Sitamah Nathoo** (admin@liferisk.co.za) always, Importance High.

**If a lump sum applies (Question 11a = Yes):** build the second, separate Lump Sum Investment HTML (Step 6b) and run Steps 8a–8c for it too, as its own draft and its own Teams message (Lump Sum Quote Plan 2 + its fund fact sheet(s) as the attachments). **If no lump sum applies:** one HTML, one draft, one Teams message.

Never deliver the `.xlsm` working file to the client-facing output in either case.

### Step 8a — COMPULSORY: save the HTML into the client's folder

- **Location:** `Paul` SharePoint site > `New Business` > `{Surname}, {FirstName}` > `{Surname}, {FirstName} - (OM RA - R{premium})` > `Comparative Quotes` (folder found with `sharepoint_folder_search`, parameter `name`). It already holds the OM Optimal RA Quote, the fund fact sheets, the Optimal Illustrator (RA Booster Value) and the "OM Wealth Investment Strategy Summary" (and often the RGAR PDF — which is never attached). If that path does not exist, create the folders under the client's existing W-Files client folder and tell Paul (seen 13/10/2026).
- **How:** `sharepoint_upload_file` (driveId + parentItemId, `expectedBytes` = file size, `conflictBehavior: "replace"` when re-saving). The signature logo is a long base64 string: save a **no-logo copy** (logo `<p>` removed) rather than risk a corrupt image, and tell Paul the saved copy has no logo (the Outlook draft takes the logo from Paul's signature). Never truncate or retype base64 by hand.
- Tell Paul the folder and file name in plain words.

### Step 8b — COMPULSORY: Outlook draft with Claude in Chrome (never sent by Claude)

- **To** client, **Cc** Sitamah Nathoo, **Subject** exactly as in the HTML.
- Method: (1) `outlook_create_draft` for the shell (to, cc, subject, placeholder body); (2) Chrome: new tab, navigate to `outlook.office365.com/mail/` first, wait, then the draft's webLink, click the edit pencil; (3) dispatch a **paste event** (`ClipboardEvent('paste')` with `DataTransfer` `text/html`) on `[aria-label="Message body"]` with the body only — "Dear {Client}," down to the bold next-meeting line; **no header table, no "Kind regards,", no signature** (the signature supplies "Kind regards,"); use `<b>`, borders on `td`, `<p> </p>` spacers; (4) **Insert > Signature > "Paul K New"**; (5) **Options > High importance**; (6) never Ctrl+S; wait ~8 s for autosave.
- **Verify** with `read_resource` on `mail:///messages/{id}` (result is large — parse the saved JSON file with python): To, Cc, subject, importance high, tables open = close, exactly one "Kind regards", no placeholder text. If DOM edits made after the paste don't persist, make the change through the editor (e.g. `execCommand`) so Outlook registers it, then re-verify.
- Close the tab afterwards and delete any stray drafts Claude created. Attachments are **not** added by Claude — Sitamah attaches them and sends.

### Step 8c — COMPULSORY: Teams message to Sitamah (sent via Zapier; Sitamah attaches and sends the email)

Send it **through Zapier: `microsoft_teams_send_chat_message`** — **never through Claude in Chrome / Teams web**, and not the native `teams_send_chat_message` (it fails: missing `ChatMessage.Send` scope). Use `format: "markdown"` (it renders as real bold and a real numbered list in Teams — confirmed on Paul's run of 13/10/2026). Do not use `plain` or `xml`.

**Greeting — ALWAYS include one.** Check real SAST time (`TZ=Africa/Johannesburg date`): "Good morning Sitamah," before 12:00, "Good afternoon Sitamah," 12:00–17:59, "Good evening Sitamah," after. Only if that same time-of-day greeting has already been used **today in a message from Paul or Claude** in the 1:1 chat, use "Hi Sitamah," or "Hey Sitamah," instead. Other messages in the chat that carried no greeting do NOT remove the greeting — never start the message without one.

**Standard wording (only client/product details change; bold "Action needed:" and "Drafts", numbered list; no emojis, no "do not send"/"leave in Drafts"/"let me know" lines):**

> {Greeting} Sitamah,
> **Action needed:** I have compiled the draft Old Mutual Optimal Retirement Annuity (RA) proposal email to {Client} and saved it in **Drafts** (To: {client email}, Cc: you).
> Please kindly attach the following to that draft:
> 1. The OM Optimal RA Quote ({quote file name without .pdf})
> 2. The relevant fund fact sheets as per the quote ({fund names})
> 3. The OM Optimal RA Booster Value document ({Optimal Illustrator file name without .pdf})
> 4. The "OM Wealth Investment Strategy Summary" document
>
> All four are in {Client}'s folder: {RA folder name} > Comparative Quotes.
> Once attached, please email the client - Thank you!

**The RGAR is never listed or mentioned** (permanent rule). Lump sum run: adapt the list to the Plan 2 documents.

**How to send (Zapier):** (1) Resolve the chat with `list_dynamic_enum_values` (`tool_name` = `microsoft_teams_send_chat_message`, `property_name` = `chat`, `search` = "Sitamah Nathoo") and take the **1:1 chat** value `19:bd2a130a-35d9-459e-9025-55f356810236_e6901cee-de73-46d9-88a5-5e4a1c296418@unq.gbl.spaces` (label "(1:1 Chat) Paul Kafentzis, Sitamah Nathoo") — never a meeting chat. (2) Call `microsoft_teams_send_chat_message` with that `chat`, `format: "markdown"`, `content` = the message in Markdown (`**bold**`, a blank line between paragraphs, `1.` list items, an `output_hint` is required by the tool). (3) **Read the posted message back** with `read_resource` on `teams:///chats/{chatId}/messages/{messageId}` and confirm the body shows `<strong>` bold labels, an `<ol>` numbered list, the greeting, and no literal `**` or escaped tags; Paul can also confirm in the Teams window. (4) Never report it as sent until read back. (5) Only delete a message Claude itself posted, and only when Paul has asked for a redo.

**Final report to Paul** states: where the HTML was saved, the draft's status, that Sitamah was messaged (and will attach + send), and flags (audit edge cases, quote/booster document discrepancies, quote expiry before the start date, saved copy without logo, assumptions such as meeting time or email address carried over).

## Reference material

- `references/mcd_v6_3.md` — the full Master Context Document (V6.3). It contains the complete placeholder table, all client-scenario wording variants (including the two-document Lump Sum Investment structure in Section 6.5), the full tax bracket tables, fee-sourcing rules, and the version history of corrections that produced these rules. Read it whenever a rule above isn't specific enough for the situation in front of you (e.g. an unusual client scenario, a wording variant not summarized above).
- `assets/OM_Optimal_RA_Proposal_TEMPLATE.html` — base template for the main proposal (Plan 1, recurring premium).
- `assets/OM_Optimal_RA_LumpSum_Proposal_TEMPLATE.html` — base template for the separate Lump Sum Investment proposal (Plan 2), used only when Question 11a is Yes.
- `assets/Tax_Reform_Tool_TEMPLATE_4.xlsm` — the only correct version of the tax calculation tool.
- `assets/wr_logo.png` — Wealth Revolution logo, already embedded in both templates; kept here for reference if it ever needs re-inserting.

## A note on the MCD's own internal version lag

The MCD document's footer (last line) and a couple of early references (Sections 2 and 5.1) still cite the pre-V6.3 template filename (`..._02_07_26.html`) and say "Version 5.0" in the closing line, even though the version history and Sections 6.5 / 11 correctly describe V6.3 and the `_22_07_26.html` filenames. Trust the version history table and Sections 6.5/11 (the substantive, most-recently-edited content) over these stale footer/early-section references, and flag this inconsistency to Paul next time the MCD itself is revised, since it's a genuine drafting error in the source document rather than a skill error.

## A note on scope

This skill is about the *procedure*. It doesn't carry any specific client's data — each proposal should start from the client's own uploaded documents in that conversation. If a new client's documents aren't in this conversation yet, ask for them via the Step 1 checklist rather than reusing anything from earlier in the chat or from memory of a previous client.

<!-- ===== references/mcd_v6_3.md (Master Context Document V6.3) ===== -->

**MASTER CONTEXT DOCUMENT**

**OM Optimal Retirement Annuity Proposal**

Wealth Revolution — Paul Kafentzis

**Version 6.3 | July 2026**

*Supersedes Version 6.2*

# VERSION HISTORY

| **Version** | **Changes** |
| --- | --- |
| V1.0 — May 2026 | Initial Master Context Document produced during training session. |
| V2.0 — May 2026 | Updated to include: HTML proposal template reference, line-by-line fixed vs variable analysis, client scenario rules, risk profile fixed as Moderate, fund selection rules, corrections to penalties (R300), tax cap (R430,000), end date removal from pension section, CPI line removal, product sentence merge, font confirmed as Aptos 11pt. |
| V3.0 — May 2026 | Tax Reform Tool table structure overhauled: Pension/Provident Fund rows now appear in ALL THREE tables. Three-table logic defined. Label correction: Pension → Provident where applicable. Three-table purpose statements formalised. Deliverables list updated (HTML only). |
| V4.0 — May 2026 | ‘What you can save’ sentence completely overhauled: figure changed from remaining RA room to total SARS cap (C15 ÷ 12). New placeholder [TOTAL CAP MONTHLY] introduced. Sentence construction rules defined for ALL client scenarios. Tax Reform Tool file reference updated to TEMPLATE_4. Stale cache warning added. [MAXIMUM RA CONTRIBUTION] redefined as Table 2 RA figure only. Mandatory pre-delivery figure audit (10 checks) added in Section 8.6. |
| V5.0 — July 2026 | Three tax table rules fully redefined: T1 now shows client’s current situation with ALL existing RAs as named PAY YOURSELF FIRST rows and tax saved shown (not R0). T2 shows a single new OM Optimal RA row for full remaining SARS room only — no existing RA rows ever. T3 shows new OM RA only if existing RA is being replaced; shows both if existing RA is being kept. Startup checklist extended to 10 items: new mandatory Question 9 — replace vs keep; new mandatory Question 10 — upload all current RAs (active/paid up) or confirm none exist. Personal circumstances wording changed from ‘You will be working’ to ‘You are working’. Template filename updated to OM_Optimal_RA_Proposal_CLAUDE_TEMPLATE_02_07_26.html. Personal RA table updated to 5-column layout with [RA_PENALTY_NOTE] placeholder. [T2_RA_ROWS] and [T3_RA_ROWS] placeholders introduced for conditional RA row population in Tables 2 and 3. Section 6.1 updated with replace vs keep rules. Section 8.2 three-table purpose statements fully rewritten. |
| V6.0 — July 2026 | Startup checklist extended to 12 items: new mandatory Question 11 — Lump Sum Investment (Section 14 transfer OR voluntary funds into the new OM Optimal RA), requiring a separate Lump Sum Quote to be uploaded; new mandatory Question 12 — Client Overview document (‘Current Investments’ section) for at-a-glance gross/net fund values, penalties and monthly premiums. New Section 6.5 — Lump Sum Investment Section — defines the client-scenario wording rules for Section 14 transfers vs voluntary funds, and the OM Plan 1 (recurring premium) / Plan 2 (lump sum) same-contract-number convention. New placeholder [LUMP_SUM_BLOCK] added to the HTML template (new ‘Lump Sum Investment’ paragraph section). Bug fix: [T1 ANNUAL TAX SAVED RA] placeholder — previously missing from both the template and this document, causing Table 1’s ‘Annual Tax Saved from RA Deduction’ row to render as a static dash on every proposal — now formally defined and added to the template. |
| V6.1 — July 2026 | Question 11 reworded and broken into four sub-questions (11a–11d) for clarity, replacing the single cluttered question: 11a — does a lump sum apply (Yes/No); 11b — Section 14 or voluntary funds; 11c — source policy/policies + Net Fund Value (Section 14) OR source of funds + Rand amount (voluntary); 11d — upload the Lump Sum Quote (Plan 2). No change to underlying rules or Section 6.5 wording — this is a checklist-presentation clarification only. |
| V6.2 — July 2026 | New Section 6.5.4 and placeholder [LUMP_SUM_FUND_FEE_BLOCK]: whenever a lump sum applies, the email must also show Plan 2’s fund selection and fee structure in a mini table immediately below [LUMP_SUM_BLOCK] — read directly from the Lump Sum Quote, never assumed to match Plan 1 (Plan 2 is frequently a different fund mix and fee structure entirely). Prompted by the [client C] build, where Plan 2 used a single fund (100% Albaraka Balanced) and a different tiered admin fee structure to Plan 1’s 50/50 split. |
| V6.3 — July 2026 | **Major restructure:** the combined single-email Lump Sum Investment section (V6.0–V6.2) is superseded. Whenever a lump sum applies, Claude now produces TWO separate HTML documents: (1) the main proposal, covering the recurring premium (Plan 1) only, with no lump sum content and no changes otherwise; (2) a new, separate Lump Sum Investment proposal, built from a new template (OM_Optimal_RA_LumpSum_Proposal_TEMPLATE.html), covering the lump sum (Plan 2) only — Section 14/voluntary funds wording, Plan 2 fund/fee detail, risk profile, product description — with no tax tables. [LUMP_SUM_BLOCK] and [LUMP_SUM_FUND_FEE_BLOCK] are deprecated from the main template; the new document uses its own placeholder, [LS_FUND_FEE_BLOCK]. Both documents share the same signature block and branding, and are sent together as two separate emails. Section 6.5 rewritten in full to reflect this. |

# 1. PURPOSE OF THIS DOCUMENT

This document is the definitive reference for producing an Old Mutual Optimal Retirement Annuity (OM Optimal RA) proposal email for any client. It covers every section of the proposal, all data sources, all calculations, all tools used, the correct format, and the complete startup checklist. Every future proposal must follow this document exactly.

| **⚠**** Before**** producing any proposal, Claude must perform a full figure audit — verifying that every number in the proposal traces back correctly to the Tax Reform Tool calculations, and that every sentence referencing a figure is cohesive with every other sentence and table in the document. Zero errors are acceptable.** |
| --- |

# 2. PROJECT FILES REFERENCE

| **File** | **Purpose** |
| --- | --- |
| OM_Optimal_RA_Proposal_CLAUDE_TEMPLATE_02_07_26.html | The HTML proposal email template. Base file for every new proposal. All sections, styling, WR logo, and placeholders. Claude populates this for each new client. |
| Tax_Reform_ToolV3__2026__2027__TEMPLATE_4.xlsm | The Tax Reform Tool for 2026/2027 SARS tables. This is the ONLY correct version. No stale cached values, fullCalcOnLoad set, all brackets correct. DO NOT use any earlier version. |
| [client A]__Old_Mutual_Savings_and_Income__Optimal_RA__R4000__26_05_26.pdf | Example of the NEW OM Optimal RA quote format. Used as reference for reading all future quotes. |
| [client B]__Retirement_Goal_Analysis__17_02_26.pdf | Example RGAR. Used as reference for identifying the correct second shortfall figure. |

| **⚠**** Tax**** Reform Tool file integrity: Always use TEMPLATE_4. Earlier versions contained stale cached values from previous clients, wrong tax brackets (2021/2022 and 2025/2026 figures), ****and an incorrect rand cap of R350,000 in Reinvest Calcs. These produced wrong outputs (89% remaining, R31,833 additional monthly) even with correct inputs. TEMPLATE_4 has ****all of**** these fixed.** |
| --- |

# 3. PRODUCT OVERVIEW — OM OPTIMAL RA

## 3.1 What It Is

The Old Mutual Optimal Investment Plan is the client’s certificate of membership of the South African Retirement Annuity Fund (SARAF), an approved Retirement Annuity Fund. It is a disciplined vehicle to provide for retirement capital accumulation.

## 3.2 Key Product Features

- Tax-deductible contributions: up to 27.5% of the greater of remuneration or taxable income, in respect of ALL retirement vehicle contributions combined (RA + pension + provident), subject to a maximum of R430,000 per annum (effective 1 March 2026).

- Tax-free growth: zero income tax, capital gains tax, or dividend withholding tax while invested.

- Two-Pot System (effective 1 September 2024): 1/3 to Savings Component (accessible once per tax year, min R2,000, taxed at marginal rate); 2/3 to Retirement Component (preserved until retirement). At retirement (min age 55): up to 1/3 as lump sum; balance purchases income annuity.

- No penalties for stopping, reducing or pausing premiums. Admin charge of R300 only.

- Annual Contribution Increase (ACI): always set at 10% p.a. on all proposals.

## 3.3 Investment Boosters

- Optimal Booster: 2.5% of fund value paid on the day before the 5th anniversary, plan must be active.

- Monthly Boosters from year 6: Years 6–10: 1.000% p.a. | Years 11–15: 1.250% p.a. | Years 16–20: 1.500% p.a. | Years 21–25: 1.750% p.a.

## 3.4 Risk Profile

| **⚠**** The**** Risk Profile is ALWAYS ‘Moderate’ for ALL clients on the Optimal RA proposal. This is fixed and never changes.** |
| --- |

## 3.5 Fund Selection

Fund selection is determined entirely by Alwyn (OM Broker Consultant) and shown in the quote. Claude reads fund names and allocation percentages directly from the quote. Fund selection is NOT always 50/50 — it varies per client. Always read from the quote.

## 3.6 Fees — Always Read from Quote

| **Fee** | **Source ****&**** Notes** |
| --- | --- |
| Asset management fee | Blended weighted average of selected funds — calculate from allocation %. |
| Net administration fee | Read from quote — typically 3.05% but verify each time. |
| Ongoing advice fee | Read from quote under ‘PAYABLE FROM THE PLAN’S FUND VALUE — Asset advice fees’ — typically 0.575% p.a. |
| Adviser remuneration account charge | Read from quote — typically 0.00%. |
| Total ongoing fees | Sum of all above. |
| Monthly fixed admin fee (rand) | Read from quote — varies per quote. Never assume. |

# 4. STARTUP CHECKLIST — DOCUMENTS REQUIRED

| **#** | **Document / Information Required** |
| --- | --- |
| 1 | Client Fact Find — personal details, age, employer, position, start date, gross income, retirement goal, risk profile. |
| 2 | Astute CCP Report OR existing policy schedules — existing RA details. If no existing RAs, adviser confirms. |
| 3 | Pension or Provident Fund Statement — fund value, employer/employee contribution % and rand amounts. If no fund, adviser confirms. |
| 4 | Proof of Income (POI) / Payslip — gross monthly remuneration and fund contribution percentages. |
| 5 | RGAR PDF from Alwyn — Alwyn must set ACI at 10% p.a. If no RGAR requested, adviser confirms. |
| 6 | OM Optimal RA Quote from Alwyn — new format (‘Old Mutual Savings and Income — Optimal Retirement Annuity Plan Quote Report’). |
| 7 | Date(s) of Teams Meeting(s) held with client — for opening line of proposal. |
| 8 | Date, day and time of next scheduled Teams Meeting with client — for closing paragraph. |
| 9 | Is the client’s existing RA being replaced by the new OM Optimal RA, or will it be kept in force alongside it? This answer determines: (a) the Recommendation column in the Personal RA table, (b) the row structure of Table 3, and (c) whether the [RA_PENALTY_NOTE] applies. If the client has no existing RA, this question does not apply. |
| 10 | Please upload all current RA’s (active / paid up). If there are no RA’s, please state that there are none. This must be answered before any proposal is built. |
| 11 | **Lump Sum Investment:** 11a. Will a lump sum be going into the new OM Optimal RA, in addition to the recurring premium? (Yes/No) 11b. *(if Yes)* Is it a Section 14 transfer from an existing retirement fund, or voluntary funds from personal savings? 11c. *(if Section 14)* Which policy/policies are transferring, and what is the Net Fund Value? *(if voluntary funds)* What is the source of the funds, and what is the Rand amount? 11d. Please upload the separate OM Lump Sum Quote (Plan 2) covering this amount. If 11a is No, 11b–11d do not apply. |
| 12 | Please provide the Client Overview document showing the ‘Current Investments’ section — gross fund value, penalties, net fund value and monthly premium for each existing policy at a glance. |

*Note: The proposed monthly RA premium is read directly from the quotation — do not ask the adviser separately. If Question 11 is answered Yes, the Lump Sum Quote is read separately from the recurring-premium quote — see Section 10.3.*

# 5. THE HTML TEMPLATE — HOW TO USE IT

## 5.1 Template File

**Template Filename: **OM_Optimal_RA_Proposal_CLAUDE_TEMPLATE_02_07_26.html — Stored permanently in the Claude Project files.

## 5.2 How Claude Uses the Template

- Open the template file from the project

- Read all client documents from the startup checklist

- Perform all Tax Reform Tool calculations (Section 8)

- Complete the mandatory pre-delivery figure audit (Section 8.6) before populating any field

- Replace every placeholder [LIKE THIS] with the correct client-specific value

- Construct the ‘What you can save’ sentence using the correct scenario template (Section 8.5)

- Ensure all sentences referencing figures are cohesive with the tables throughout

- Deliver the completed HTML file — ready for adviser to Ctrl+A, Ctrl+C, paste into Outlook

## 5.3 Complete List of Placeholders

| **Placeholder** | **Source** |
| --- | --- |
| [CLIENT FIRST NAME] | Fact Find |
| [CLIENT FULL NAME] | Fact Find |
| [CLIENT EMAIL] | Left as placeholder — adviser fills in before sending |
| [CC EMAIL] | Left as placeholder — adviser fills in before sending |
| [DATE AND TIME SENT] | Date/time when proposal is produced |
| [PREMIUM] | Quote — regular contribution amount |
| [DAY] [DD/MM/YYYY] | Startup Question 7 — Teams meeting date(s) |
| [AGE] | Fact Find |
| [EMPLOYER NAME] | Fact Find |
| [POSITION] | Fact Find |
| [START DATE] | Fact Find / Quote |
| [GROSS MONTHLY INCOME] | Fact Find / POI |
| [INSURER NAME] [POLICY NUMBER] | Astute CCP / policy schedule — repeat for each existing RA |
| [MONTHLY CONTRIBUTION] | Astute CCP / policy schedule |
| [GROSS FUND VALUE] [DATE] | Astute CCP / policy schedule |
| [RECOMMENDATION] | Adviser’s recommendation — either ‘Replace with OM Optimal RA’ or ‘Keep in force’ |
| [RA_PENALTY_NOTE] | Conditional italic note in the Recommendation cell of the Personal RA table. Populate with ‘No penalties apply – policy is too new’ if the existing RA is new and carries no surrender penalties. Leave blank otherwise. |
| [T2_RA_ROWS] | Table 2 PAY YOURSELF FIRST RA row(s). Always a single row: new OM Optimal RA contribution = [MAXIMUM RA CONTRIBUTION]. No existing RA rows ever appear in Table 2. |
| [T3_RA_ROWS] | Table 3 PAY YOURSELF FIRST RA row(s). If existing RA is being replaced: single row for new OM Optimal RA only. If existing RA is being kept: one labelled row per existing RA + one row for new OM Optimal RA. |
| [NET FUND VALUE] | Astute CCP / policy schedule |
| [PENSION/PROVIDENT] | Fund statement — type of fund |
| [AMOUNT] [%] | POI / Fund statement — employer & employee contributions |
| [FUND VALUE] [DATE] | Fund statement |
| [TOTAL CAP MONTHLY] | Tax Reform Tool — C15 ÷ 12. Total SARS allowable cap per month across ALL retirement vehicles. Used ONLY in the ‘What you can save’ sentence. |
| [MAXIMUM RA CONTRIBUTION] | Tax Reform Tool Table 1 — ‘Additional Monthly Premium’ output. Remaining RA room after existing fund contributions subtracted from C15. Used in Table 1 SAVINGS OPPORTUNITIES rows and Table 2 RA input row only. |
| [SHORTFALL AMOUNT] | RGAR — second shortfall table (‘WHAT YOU HAVE AGREED TO DO AND WHY’) |
| [X] years | RGAR — years to retirement |
| [CURRENT VALUE] | RGAR — current monthly expenses |
| [FUTURE VALUE] | RGAR — future value at retirement |
| [RETIREMENT AGE] | RGAR — retirement age |
| [PROPOSED PREMIUM] | Quote — regular contribution amount |
| [MAXIMUM CONTRIBUTION] | Tax Reform Tool Table 2 — RA contribution (= [MAXIMUM RA CONTRIBUTION]) |
| [TAX SAVED PENSION] | Tax Reform Tool Table 1 — tax saved from pension fund deduction (pension fund clients only) |
| [TAX SAVED PROVIDENT] | Tax Reform Tool Table 1 — tax saved from provident fund deduction (provident fund clients only) |
| [T1 ANNUAL TAX SAVED RA] | Tax Reform Tool Table 1 — annual tax saved from RA deduction. **Bug fix (V6):** this placeholder was missing from the template prior to V6, causing the row to render as a static dash on every proposal. Must never be left as a dash — the figure is always present, even if small. |
| [T1 ANNUAL TAX PAYABLE] | Tax Reform Tool Table 1 — annual tax payable |
| [T2 ANNUAL TAX SAVED RA] | Tax Reform Tool Table 2 — annual tax saved from RA deduction |
| [T2 ANNUAL TAX PAYABLE] | Tax Reform Tool Table 2 — annual tax payable |
| [T3 ANNUAL TAX SAVED RA] | Tax Reform Tool Table 3 — annual tax saved from RA deduction |
| [T3 ANNUAL TAX PAYABLE] | Tax Reform Tool Table 3 — annual tax payable |
| [T1 PCT REMAINING] | Tax Reform Tool Table 1 — maximum deduction left to use (%) |
| [T1 ADDITIONAL MONTHLY PREMIUM] | Tax Reform Tool Table 1 — additional monthly RA possible |
| [T1 LUMP SUM] | Tax Reform Tool Table 1 — once-off lump sum to maximise deduction |
| [T3 PCT REMAINING] | Tax Reform Tool Table 3 — maximum deduction left to use (%) |
| [T3 ADDITIONAL MONTHLY PREMIUM] | Tax Reform Tool Table 3 — additional monthly RA still possible |
| [T3 LUMP SUM] | Tax Reform Tool Table 3 — once-off lump sum still available |
| [BAR_1] through [BAR_10] | Tax Reform Tool Reinvest Calcs sheet — annual tax saved for years 1–10 as RA escalates at 10% ACI |
| [FUND NAME 1] [FUND NAME 2] | Quote — fund selection table |
| [ALLOCATION 1%] [ALLOCATION 2%] | Quote — fund allocation percentages |
| [ASSET MGMT FEE] | Quote — blended average of fund management fees (weighted by allocation %) |
| [TOTAL ONGOING FEES] | Calculated: sum of all fee components |
| [MONTHLY ADMIN FEE] | Quote — monthly fixed administration fee rand amount |
| [NEXT MEETING LINE] | Startup Question 8 — next Teams meeting details |
| [LUMP_SUM_BLOCK] | **Deprecated in V6.3** — the lump sum content now lives in its own separate document. See Section 6.5. |
| [LS_FUND_FEE_BLOCK] | Lump Sum Investment proposal document only. Startup Question 11d — Lump Sum Quote (Plan 2). Fund selection and fee mini-table. Always read directly from the Lump Sum Quote — never assume it matches Plan 1. See Section 6.5.5. |

# 6. CLIENT SCENARIO RULES

## 6.1 Personal Retirement Savings Section

| **Scenario** | **What Goes in Email** |
| --- | --- |
| Client HAS existing RAs | Show full RA details for each policy: insurer name, policy number, monthly contributions, gross fund value + date, recommendation, penalties (always orange: ‘To be determined if there are’), net fund value. |
| Client has NO existing RAs | Replace entire section content with: ‘You have no active or Paid-Up Retirement Annuities.’ — nothing else under this heading. |

## 6.2 Pension/Provident Retirement Savings Section

| **Scenario** | **What Goes in Email** |
| --- | --- |
| Client HAS a Pension/Provident Fund | Line reads: ‘You have a [Pension/Provident] Fund with your employer [Employer Name]’ — NO end date. Then employer contributions (R amount + %), employee contributions (R amount + %), current fund value + date. All in bold. |
| Client has NO Pension/Provident Fund | Replace entire section content with: ‘You have no Pension or Provident Fund with your employer.’ — nothing else under this heading. |

| **⚠**** Never**** include an end date in the pension/provident line. The [client B] end date was a one-off exception and must NOT be treated as standard.** |
| --- |

## 6.3 Retirement Goal Analysis Section

| **Scenario** | **What Goes in Email** |
| --- | --- |
| RGAR was requested and received | Show full shortfall paragraph: ‘According to the Retirement Goal Analysis Report that was sent to you on a previous email, over and above your current savings, you would be required to personally save an additional amount of: R [SHORTFALL AMOUNT] per month, increasing at 10% per annum, over the next [X] years, to reach your desired gross income goal of R [CURRENT VALUE] p.m. (Future Value: R [FUTURE VALUE] p.m. at age [RETIREMENT AGE]).’ |
| RGAR was NOT requested | Replace entire section content with: ‘You did not request for a Retirement Goal Analysis Report.’ — nothing else under this heading. |

## 6.4 Tax Reform Tool — Employment Type Scenarios

| **Employment Type** | **Effect on Tax Reform Tables** |
| --- | --- |
| Self Employed | No fund contributions. Full C15 ÷ 12 available for RA. All three tables show no pension/provident rows — only the RA contribution row, which changes across the three tables. |
| Employed (Pension Fund) | Employer + employee pension contribution rows appear in ALL THREE tables. Both count toward the 27.5% limit. RA row changes across the three tables. |
| Employed (Provident Fund) | Same as pension fund logic but rows labelled ‘Employer Provident Fund Contribution’ and ‘Member Provident Fund Contribution’. Both count toward the 27.5% limit. RA row changes across the three tables. |

## 6.5 Lump Sum Investment — Two-Document Structure

**Governance decision (22/07/26, superseding the earlier single-email approach in V6.0–V6.2):** whenever Startup Question 11a is Yes, Claude produces **TWO separate HTML documents** instead of one combined email:

- **The main proposal** (unchanged template, OM_Optimal_RA_Proposal_CLAUDE_TEMPLATE_22_07_26.html) — covers the recurring monthly premium (Plan 1) only. It does NOT contain any lump sum content. The three tax tables, “what you can save” sentence, RGAR, and all other sections relate ONLY to the recurring contribution, since the lump sum has no bearing on the 27.5%/R430,000 annual deduction calculation.

- **A separate Lump Sum Investment proposal** (new template, OM_Optimal_RA_LumpSum_Proposal_TEMPLATE.html) — covers the lump sum (Plan 2) only: the Section 14 transfer or voluntary funds facts, the Plan 2 fund/fee detail, risk profile, and product description. It contains NO tax tables (a lump sum transfer/investment does not generate an RA tax deduction calculation the way a recurring contribution does).

**Rationale:** the recurring premium and lump sum are answers to two different client questions (“how much should I contribute monthly and why” vs “what happens to my existing RA money”), are quoted separately by Alwyn, frequently use different funds and fees, and combining them into one document made the tax-table narrative harder to follow. Two focused documents are clearer for the client and the adviser.

**Both documents share:** the same signature block, adviser contact details, and Wealth Revolution branding/footer. Both should be sent together (or in close succession) as they relate to the same overall recommendation, and both quotes (recurring + lump sum) are attached across the two emails as appropriate.

### 6.5.1 Background — How OM Structures a Lump Sum Alongside a Recurring Premium

When a client starts an OM Optimal RA with both a recurring monthly premium AND a lump sum contribution, Old Mutual treats these as two separate quoted plans under the SAME contract/policy number:

- **Plan 1** — the recurring monthly premium (covered in the main proposal document).

- **Plan 2** — the once-off lump sum amount (covered in the separate Lump Sum Investment proposal document).

Alwyn will issue two separate OM quotes when a lump sum applies: the standard recurring-premium quote (Plan 1) and a separate Lump Sum Quote (Plan 2). Do NOT assume Plan 2’s fund selection, fees, or allocation are identical to Plan 1 — always read the Lump Sum Quote directly, the same as any other quote.

### 6.5.2 The Lump Sum Investment Proposal Document — Structure

The OM_Optimal_RA_LumpSum_Proposal_TEMPLATE.html document follows the same visual/HTML conventions as the main template (Outlook-compatible table layout, same fonts/colours, same signature block) but with its own content sections, in order:

- **Opening** — same “Following our Teams Meeting…” opening line as the main proposal.

- **Your Lump Sum Investment** — the approved verbatim wording (Section 6.5.3 below) stating the amount, Section 14 source policy/policies (or voluntary funds source), and the tax-neutral confirmation.

- **The product ****&**** start date** — Plan 2 start date, read from the Lump Sum Quote.

- **Risk profile** — always “Moderate” (same fixed rule as the main proposal).

- **Investment Fund Details (Plan 2)** — fund selection and fee mini-table (Section 6.5.5 below). Always read directly from the Lump Sum Quote — never assume it matches Plan 1.

- **Tax treatment of the transfer** — for Section 14: confirm the transfer is tax-neutral and does not use up the client’s annual deduction limit. For voluntary funds: note that the amount invested is from after-tax savings and does not attract an additional RA tax deduction (a lump sum contribution to a retirement annuity may still be tax-deductible up to the 27.5%/R430,000 limit if the client has unused room — flag this to the adviser rather than assuming either way).

- **Attachments line** — lists the Lump Sum Quote and its fund fact sheet(s).

- **Closing / next meeting line** — same as main proposal.

- **Signature block** — identical to the main proposal.

No tax tables, no bar chart, and no “what you can save” sentence appear in this document — those belong only in the main recurring-premium proposal.

### 6.5.3 Scenario Table — Approved Verbatim Wording (use exactly, do not paraphrase)

The heading above the lump sum paragraph is always: **“Your Lump Sum Investment:”** in the Lump Sum Investment proposal document.

| **Scenario** | **What Goes in Email (verbatim)** |
| --- | --- |
| Section 14 transfer | ‘A lump sum amount of R [LUMP SUM AMOUNT] will be transferred into your new OM Optimal RA via a Section 14 transfer from your existing [SOURCE POLICY NAME(S)] policy/policies. This is a tax-neutral transfer between approved retirement funds and does not attract any tax at the point of transfer.’ Repeat/list [SOURCE POLICY NAME(S)] for each transferring policy if more than one. |
| Voluntary funds | ‘A lump sum amount of R [LUMP SUM AMOUNT] will be invested into your new OM Optimal RA from your own savings ([SOURCE OF FUNDS]).’ |

These wordings were reviewed and approved by Paul (22/07/26, revised for the two-document structure) — use them exactly as written, substituting only the bracketed figures/names. This document is only produced at all when a lump sum applies — there is no “no lump sum” variant here (in that case, simply don’t produce this second document).

### 6.5.4 Rules

- The Section 14 vs voluntary funds distinction is never inferred — it must come directly from the adviser’s answer to Startup Question 11b.

- [LUMP SUM AMOUNT] for a Section 14 transfer is always the **Net Fund Value** of the transferring policy/policies (as shown on the Client Overview / Astute CCP report) — never the Gross Fund Value.

- If multiple policies are being transferred via Section 14, sum their Net Fund Values for [LUMP SUM AMOUNT] and name each source policy individually in [SOURCE POLICY NAME(S)].

- A lump sum being transferred via Section 14 does NOT count toward the client’s annual 27.5%/R430,000 tax-deductible contribution limit (it is a fund-to-fund transfer, not a new contribution) and must never be added into the Tax Reform Tool inputs used for the main proposal.

- Voluntary funds invested as a lump sum also do not affect the Tax Reform Tool’s monthly contribution inputs in the main proposal — but if the adviser indicates the voluntary lump sum is itself intended to use up available annual deduction room, flag this to the adviser rather than assuming.

### 6.5.5 Plan 2 Fund & Fee Detail — [LS_FUND_FEE_BLOCK]

The Lump Sum Investment proposal document must show Plan 2’s fund selection and fee structure, using a mini table in the same visual style as the main proposal’s Investment Fund Details table. **Always read Plan 2’s fund selection and fees directly from the Lump Sum Quote — never assume they match Plan 1.** They are frequently different (different fund count, different allocation, different fee tiers), since Plan 2 is a separate quoted plan under the same contract.

Required content of [LS_FUND_FEE_BLOCK]:

- A fund allocation table — one row per fund in the Lump Sum Quote, with fund name and allocation % (Plan 2 may hold a single fund at 100%, or multiple funds — read directly from the quote, do not assume a 50/50 split).

- A fee table for Plan 2 — asset management fee (blended if more than one fund), administration fee (may be tiered by fund value band — state the applicable band or the initial rate), asset advice fee, and any as-and-when advice fee (state ‘None’ if the client has agreed not to pay one, as shown on the quote).

# 7. LINE-BY-LINE: FIXED VS VARIABLE

## 7.1 FIXED Lines — Same for Every Client

- FROM: Paul Kafentzis

- IMPORTANCE: High

- ‘You intend to save for retirement.’

- ‘You are working at [employer] in the position of [position].’ — NEVER ‘You will be working.’ The wording is always present tense.

- ‘Penalties: To be determined if there are’ (always in orange)

- ‘…increasing at 10% per annum…’ (ACI always 10%)

- ‘You can elect to start a Retirement Annuity with Old Mutual called The Optimal Investment Plan…’

- Risk Profile: always ‘Moderate’

- ‘The Optimal Investment Plan is your certificate of membership of SARAF… It is a disciplined vehicle to provide for retirement capital.’

- ‘…tax deductible up to 27.5% of remuneration capped at R430,000 per annum.’

- All Two-Pot System bullet points

- All Tax Reform table headings and structure

- Bar chart title: ‘RE-INVESTING YOUR RECLAIMED DEDUCTION: HOW MUCH OF YOUR RA CONTRIBUTION SARS WILL PAY’

- All Booster text and Booster table values

- ‘You have access to a wide range of funds.’

- All Tax Implication section text

- ‘There are no reduction fees… only an admin charge of R300.00’

- All Savings Component withdrawal text

- Personal Investment Target description paragraphs (inflation plus 4–5%, 5–7 years, diversified portfolio)

- ‘Although the Personal Investment Target targets specific inflation-beating returns, these returns are not guaranteed.’

- Fees table structure and headings

- ‘Please see attached:’ heading and items 1, 3 and 4

- ‘Hoping that above is in order.’ | ‘Kind regards,’ | Full signature block

## 7.2 VARIABLE Lines — Client-Specific, Must Change Every Proposal

| **Variable Element** | **Source** |
| --- | --- |
| TO / CC email addresses | Left as placeholders — adviser fills in before sending |
| Subject line | Client name + premium from quote |
| Date/time sent | Date proposal is produced |
| Teams meeting date(s) (opening) | Startup Question 7 |
| Client first name | Fact Find |
| Age | Fact Find |
| Employer, position, division | Fact Find |
| Gross monthly income | Fact Find / POI |
| Existing RA details (or no RAs statement) | Astute CCP / policy schedule |
| Replace vs keep decision | Startup Question 9 — determines Recommendation column, Table 3 structure, and [RA_PENALTY_NOTE] |
| Pension/Provident details (or no fund statement) | POI + Fund Statement |
| ‘What you can save’ sentence | Constructed dynamically per client scenario — see Section 8.5 |
| RGAR shortfall figures (or no RGAR statement) | RGAR second shortfall table |
| Proposed premium (‘What you have chosen’) | Quote |
| Product start date | Quote |
| All three Tax Reform table figures | Tax Reform Tool — calculated per client |
| Bar chart values (years 1–10) | Tax Reform Tool — Reinvest Calcs sheet |
| ‘By contributing R[X] per month’ headings (Tables 2 & 3) | Tax Reform Tool outputs |
| Fund names and allocations | Quote — fund selection table |
| ‘Funds recommended’ sentence | Quote — fund names |
| Attachment point 2 fund names | Quote — fund names |
| All fee percentages and rand amounts | Quote |
| Next Teams meeting details (closing) | Startup Question 8 |

# 8. TAX REFORM TOOL — HOW TO USE IT

## 8.1 Tool Details

- File: Tax_Reform_ToolV3__2026__2027__TEMPLATE_4.xlsm (project files) — ONLY this version

- Tax year: 2026/2027 — SARS tables effective 1 March 2026

- 2026/2027 brackets: R0–R237,100 (18%) | R237,101–R370,500 (26%) | R370,501–R512,800 (31%) | R512,801–R673,000 (36%) | R673,001–R857,900 (39%) | R857,901–R1,817,000 (41%) | Above R1,817,000 (45%)

- Primary rebate: R17,820 | Rand cap: R430,000 | 27.5% limit

- B35 = annual remuneration + employer fund contributions (fringe benefit added back per SARS)

- C15 = MIN(R430,000, 27.5% × B35) — this is the binding SARS allowance

- Employment type: radio buttons on Maximise Allowance Tool sheet

## 8.2 Three Scenarios — Purpose and Input Rules

| **Table** | **Purpose** | **PAY YOURSELF FIRST Rows** |
| --- | --- | --- |
| Table 1 — Your current situation | Shows the client’s exact tax position today. Every existing RA the client currently holds appears as its own named row. The tax saved on those existing contributions is shown. This is the true baseline. Pension/Provident rows also shown if applicable. | Pension/Provident rows (if applicable) + one named row per existing RA showing current monthly contribution. Tax saved on existing RA contributions must be shown — never R–. |
| Table 2 — Taking advantage of the full tax deduction | Shows the maximum 27.5% SARS opportunity using only the new OM Optimal RA. No existing RA rows appear here — ever. Single RA row shows [MAXIMUM RA CONTRIBUTION] = full remaining SARS room. Together with any fund rows, equals full C15. | Pension/Provident rows (if applicable) + single new OM Optimal RA row = [MAXIMUM RA CONTRIBUTION]. No existing RA rows regardless of client situation. |
| Table 3 — What you have requested | Shows the proposed new OM Optimal RA premium. Structure depends on the replace vs keep decision (Startup Question 9). If replacing: single new OM RA row only. If keeping: existing RA row(s) + new OM RA row — combined tax saving shown. | REPLACE scenario: Pension/Provident rows (if applicable) + single new OM Optimal RA row only. KEEP scenario: Pension/Provident rows (if applicable) + existing RA row(s) + new OM Optimal RA row. |

| **⚠**** CRITICAL: Pension/Provident rows appear in ALL THREE tables — not Table 1 only. Fund amounts are identical across all three tables. Only the RA contribution line(s) change across tables.** |
| --- |

| **⚠**** CRITICAL: Table 2 RA contribution = (C15 − total annual fund contributions) ÷ 12. The fund and RA together must equal C15. The RA is NOT a separate allowance on top of the fund. No existing client RA rows ever appear in Table 2.** |
| --- |

| **⚠**** CRITICAL: Table 1 must always show the tax saved on the client’s existing RA contributions. Never show R– for tax saved if the client currently has an RA contributing. R– only appears if the client genuinely has no existing RA and no fund.** |
| --- |

## 8.3 Label Rule — Pension vs Provident

| **Client’s Fund Type** | **Correct Label** |
| --- | --- |
| Pension Fund client | Tax Saved from Pension Fund Deduction |
| Provident Fund client | Tax Saved from Provident Fund Deduction |
| No fund (self-employed or no employer fund) | This row does not appear |

**Never use ‘Pension Fund’ label when the client has a Provident Fund.**

## 8.4 How Tables Appear in Email

- All three tables recreated in HTML — dark green headers, light green input cells, white output rows, orange message box.

- Pension/Provident rows use the same light green styling as all other input rows.

## 8.5 ‘What You Can Save’ Sentence — Construction Rules

**The figure is always C15 ÷ 12 — the total monthly SARS allowable cap across ALL retirement vehicles. Never use the remaining RA room alone.**

The sentence is constructed dynamically based on the client’s actual retirement vehicle situation:

| **Client Scenario** | **Sentence to Use** |
| --- | --- |
| Employed with Provident Fund only (no existing RA) | “Based on your current earnings, you can save a total of R [TOTAL CAP MONTHLY] per month across all retirement vehicles (Provident Fund and Retirement Annuity combined) to take full advantage of the tax-deductible benefit offered to you by SARS.” |
| Employed with Pension Fund only (no existing RA) | “Based on your current earnings, you can save a total of R [TOTAL CAP MONTHLY] per month across all retirement vehicles (Pension Fund and Retirement Annuity combined) to take full advantage of the tax-deductible benefit offered to you by SARS.” |
| Employed with both Pension AND Provident Fund | “Based on your current earnings, you can save a total of R [TOTAL CAP MONTHLY] per month across all retirement vehicles (Pension Fund, Provident Fund and Retirement Annuity combined) to take full advantage of the tax-deductible benefit offered to you by SARS.” |
| Self-employed OR employed with no pension or provident fund | “Based on your current earnings, you can save a total of R [TOTAL CAP MONTHLY] per month towards a Retirement Annuity to take full advantage of the tax-deductible benefit offered to you by SARS.” |
| Employed with existing RA and Provident Fund | “Based on your current earnings, you can save a total of R [TOTAL CAP MONTHLY] per month across all retirement vehicles (Provident Fund and Retirement Annuity combined) to take full advantage of the tax-deductible benefit offered to you by SARS.” |
| Employed with existing RA and Pension Fund | “Based on your current earnings, you can save a total of R [TOTAL CAP MONTHLY] per month across all retirement vehicles (Pension Fund and Retirement Annuity combined) to take full advantage of the tax-deductible benefit offered to you by SARS.” |

**[TOTAL CAP MONTHLY] calculation steps:**

- Step 1: B35 = annual remuneration + (employer fund contributions × 12)

- Step 2: C15 = MIN(R430,000, 27.5% × B35)

- Step 3: [TOTAL CAP MONTHLY] = C15 ÷ 12 — use this in the ‘What you can save’ sentence

- [MAXIMUM RA CONTRIBUTION] = (C15 − total annual fund contributions) ÷ 12 — use this in Table 1 SAVINGS OPPORTUNITIES rows and Table 2 RA input only

## 8.6 Pre-Delivery Figure Audit — Mandatory

Before delivering any proposal, Claude must verify ALL of the following:

| **Check #** | **Verification Required** |
| --- | --- |
| 1 | [TOTAL CAP MONTHLY] = C15 ÷ 12 — traces back to Tax Reform Tool |
| 2 | [MAXIMUM RA CONTRIBUTION] = (C15 − total annual fund contributions) ÷ 12 — traces back to Tax Reform Tool |
| 3 | Table 1, 2 and 3 tax payable figures all differ correctly from each other |
| 4 | Tax saved (RA) in Table 2 = Table 1 tax payable − Table 2 tax payable |
| 5 | Tax saved (RA) in Table 3 = Table 1 tax payable − Table 3 tax payable |
| 6 | Table 2 PF rows + RA row monthly total = [TOTAL CAP MONTHLY] (full cap used) |
| 7 | Table 3 % remaining = (C15 − Table 3 total annual contributions) ÷ C15 × 100 |
| 8 | Bar chart Year 1 saving = Table 3 RA tax saving (same RA amount in year 1) |
| 9 | ‘What you can save’ sentence figure = [TOTAL CAP MONTHLY] — correct scenario sentence used |
| 10 | Zero placeholder tags [LIKE THIS] remain in the document (except [CLIENT EMAIL] and [CC EMAIL]) |

**Note on Checks 4 ****&**** 5:** these two checks can legitimately fail to hold exactly, or even go negative, in a ‘keep some, replace some’ scenario where the new proposed RA total is close to or lower than the client’s current combined RA contribution (e.g. an existing RA is kept in force and the replacement premium is similar in size to the RA(s) it replaces). This is not a calculation error — flag it to the adviser as a finding rather than forcing the figures to reconcile artificially. Use the Tax Reform Tool’s own native output cells for ‘tax saved’ in all cases rather than back-calculating from the payable difference.

# 9. THE RGAR — HOW TO USE IT

- Always use the SECOND shortfall figure — from ‘WHAT YOU HAVE AGREED TO DO AND WHY’. NOT the first ‘WHAT YOU NEED TO DO’ figure.

- Alwyn MUST always set ACI at 10% p.a. when generating the RGAR.

- Extract: monthly shortfall amount, years to retirement, current monthly expenses, future value, retirement age.

- The RGAR is sent to the client in a separate email before the OM Optimal RA proposal. The proposal references it.

# 10. THE OM OPTIMAL RA QUOTE — HOW TO USE IT

## 10.1 New Quote Format

All new quotes from Alwyn use the format: ‘Old Mutual Savings and Income — Optimal Retirement Annuity Plan Quote Report’. The ongoing advice fee (0.575%) is explicitly stated under ‘PAYABLE FROM THE PLAN’S FUND VALUE — Asset advice fees’.

## 10.2 What to Extract

- Monthly premium and start date

- ACI rate (always 10%) and first increase date

- Commitment term (years)

- Fund names and allocation percentages — for Investment Fund Details table AND ‘funds recommended’ sentence AND attachment point 2

- Admin fee % (initial: 3.05% — verify each time)

- Monthly fixed admin fee rand amount (varies — verify each time)

- Asset management fees per fund — calculate blended average based on allocation %

- Ongoing advice fee % (under ‘PAYABLE FROM THE PLAN’S FUND VALUE’)

- Adviser remuneration account charge %

- Booster schedule

## 10.3 The Lump Sum Quote (Plan 2) — When Startup Question 11 Is Yes

When a lump sum (Section 14 transfer or voluntary funds) is going into the new OM Optimal RA, Alwyn issues a SEPARATE quote for this amount, in addition to the standard recurring-premium quote. Both share the same contract/policy number once issued (Plan 1 = recurring premium, Plan 2 = lump sum) but are quoted, and must be read, independently.

- Do not assume the Lump Sum Quote uses the same fund selection, allocation, or fee structure as the recurring-premium quote — read it directly, exactly as with any other quote.

- Extract from the Lump Sum Quote: the lump sum amount, fund selection and allocation, and any fees specific to the lump sum investment.

- This information populates the separate Lump Sum Investment proposal document (Section 6.5) — never merged into the Plan 1 fund/fee tables in the main proposal.

- The Lump Sum Quote must be uploaded to the project files and attached to the SEPARATE Lump Sum Investment proposal email — not the main proposal email.

- The lump sum amount itself is never added to the Tax Reform Tool’s monthly RA contribution input — see Section 6.5.3.

# 11. DELIVERABLES FOR EACH PROPOSAL

| **#** | **Deliverable** |
| --- | --- |
| 1 | Main proposal email as HTML file — populated from OM_Optimal_RA_Proposal_CLAUDE_TEMPLATE_22_07_26.html. All three tax tables (with correct Pension/Provident rows in every table), bar chart, fees table, and Investment Fund Details table embedded — Plan 1 (recurring premium) only. Ready to Ctrl+A, Ctrl+C, paste into Outlook. |
| 2 | **If Startup Question 11a is Yes:** a SECOND, separate Lump Sum Investment proposal email as HTML file — populated from OM_Optimal_RA_LumpSum_Proposal_TEMPLATE.html. Covers Plan 2 (the lump sum) only — no tax tables. Ready to Ctrl+A, Ctrl+C, paste into a separate Outlook email. |

*Adviser workflow (no lump sum): open the main proposal HTML in Chrome → ****Ctrl+A**** → ****Ctrl+C**** → new Outlook email → ****Ctrl+V**** → fill in TO and CC → attach 4 PDFs → send.*

*Adviser workflow (lump sum applies): repeat the above for the main proposal (attach the standard recurring-premium quote + fund fact sheets + booster value doc + strategy summary), THEN separately open the Lump Sum Investment proposal HTML → Ctrl+A → Ctrl+C → new Outlook email → Ctrl+V → attach the Lump Sum Quote + its fund fact sheet(s) → send. Two emails, two attachments sets, sent together or in close succession.*

**Permanent rule (added post-V6.3, correction logged 04/08/26):** the "Please see attached:" list on the main OM Optimal RA Proposal email is always exactly the 4 standard items above — never 5. The RGAR is NOT attached to this email even when the client requested one, even when the RGAR PDF has been uploaded to the conversation, and even when the RGAR paragraph in the body is populated with real shortfall figures. The RGAR is delivered to the client separately and independently via the `rgar-skill` workflow. Do not add "Old Mutual Retirement Goal Analysis Report" (or any equivalent wording) as an attachment line on this template under any circumstance.

# 12. ACCURACY RULES & KNOWN CORRECTIONS

| **Item** | **Rule** |
| --- | --- |
| Tax deductibility cap | Always R430,000 p.a. (NOT R350,000). Effective 1 March 2026. |
| Transaction Admin Fee | Always R300 maximum (NOT R345). Verified from OM quotation. |
| Monthly fixed admin fee | Varies per quote. Always read directly from quote. Never assume. |
| RGAR shortfall figure | Always use SECOND shortfall (after proposed RA factored in). Never use first shortfall. |
| ACI | Always 10% p.a. Non-negotiable. Must match RGAR and quotation. |
| Ongoing advice fee | Always 0.575% p.a. Stated explicitly in new quote format. |
| Risk Profile | Always ‘Moderate’. Fixed for all clients. |
| Pension end date | Never include. [client B] end date was a one-off exception. |
| CPI line in Risk Profile section | Removed. Not included in proposal. |
| Product description sentences | Both sentences in one paragraph: ‘…approved Retirement Annuity Fund. It is a disciplined vehicle…’ |
| Font | Aptos 11pt throughout the entire email body. |
| Pension/Provident rows in tax tables | Must appear in ALL THREE tables — not Table 1 only. Amounts identical across all three. Only RA line changes. |
| Pension vs Provident label | Output row must say ‘Provident Fund Deduction’ for Provident Fund clients. Never ‘Pension Fund’ label for a Provident Fund client. |
| RA remaining room calculation | (C15 − total annual fund contributions) ÷ 12. Fund and RA together must stay within C15. |
| ‘What you can save’ figure | Always C15 ÷ 12. Never the remaining RA room alone. Sentence wording varies by client scenario — see Section 8.5. |
| Personal circumstances wording | Always ‘You are working at [employer]…’ — never ‘You will be working.’ |
| Table 1 tax saved on existing RA | Must always be shown if the client currently has an RA contributing. Never R– unless the client genuinely has no RA at all. |
| Table 2 RA rows | A single new OM Optimal RA row showing [MAXIMUM RA CONTRIBUTION] only. Existing client RA rows never appear in Table 2 under any circumstances. |
| Table 3 RA rows — replace scenario | Single new OM Optimal RA row only. Existing RA does not appear. |
| Table 3 RA rows — keep scenario | Existing RA row(s) + new OM Optimal RA row. Combined tax saving must be shown. |
| Replace vs keep question | Mandatory Startup Question 9. Must be answered before any proposal is built. |
| Upload existing RAs | Mandatory Startup Question 10. Client must upload all current RAs (active/paid up), or confirm there are none, before any proposal is built. |
| Tax Reform Tool version | Always use TEMPLATE_4. Never use earlier versions — they contain wrong brackets and stale cached values. |
| Pre-delivery audit | Mandatory for every proposal. All 10 audit checks in Section 8.6 must pass before delivery. |

# 13. KEY CONTACTS & TOOLS

| **Contact / Tool** | **Role** |
| --- | --- |
| Alwyn | OM Broker Consultant — generates RGAR and OM Optimal RA Quote. Must always set RGAR ACI at 10% p.a. |
| Astute FSE | Electronic financial data exchange platform — provides Consolidated Client Portfolio (CCP) showing all existing policies across all major SA life insurers. |

*Version 5.0 — July 2026 | This document must be updated whenever any product details, tax rules, fees, processes or template changes are agreed. Always use the latest version.*