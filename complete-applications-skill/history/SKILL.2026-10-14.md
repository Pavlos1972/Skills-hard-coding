<!-- The live skill text as of 14/10/2026 (last updated line in SKILL.md: 2026-10-14 14:46), kept as the rule-by-rule baseline: SKILL.md followed by references/field-mappings.md. No client data found, nothing replaced. The script scripts/fill_om_form.py is kept beside it as history/fill_om_form.2026-10-14.py. -->

<!-- FILE: SKILL.md -->

---
name: "complete-applications-skill"
description: "Fills in the real Old Mutual and General Short Risk application forms for a client, and corrects completed applications after a meeting. Use when Paul asks to complete or correct applications for a named client."
---

# Complete Applications Skill

## Index

| # | Section | What it covers |
|---|---|---|
| 1 | Universal operating rules + Delivery gate | The nine rules for every step, and what must be done before a run counts as complete |
| 2 | Last updated + Changelog | Athens-time stamp, last 5 changes, standing edit note |
| 3 | Why this skill exists | Real insurer forms, not lookalikes |
| 4 | How this skill is used | Pre-fill, live in the meeting, correct after |
| 5 | Step 1 - Which applications are needed | One per product and contribution type |
| 6 | Step 2 - Gather the client's bio data once | Shared personal fields |
| 7 | Step 3 - Transaction-specific fields | Product name, replacement, N/A rules, signature date, never invent data |
| 8 | Step 4 - Fill the template | Script for OM, named fields for General Short Risk |
| 9 | Step 5 - Verify before delivering | Field dump and visual render |
| 10 | Step 6 - Where the finished file goes | Chat, then the client's Applications folder; folder and file naming rules |
| 11 | Step 7 - Correction / Sync mode | Correct existing applications in place after a meeting |
| 12 | Field crosswalk | OM form to General Short Risk form |
| 13 | Reference | Bundled mappings, templates and script |

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

**Delivery gate for this skill (rules 5 and 6 applied):** a run is complete only when ALL of these are done and confirmed in one line each: (1) every application needed has been filled in from the current source documents (Steps 1-4), or in Correction / Sync mode every current application has been corrected (Step 7); (2) the Step 5 field dump and visual render are done for each file; (3) each finished file is sent in the chat (Step 6, delivery 1); (4) each finished file is saved in the client's own Applications folder and the saved file is checked (Step 6, delivery 2). After ANY correction, repeat (1) to (4) for every application that changed.

**Last updated: 2026-10-14 14:46 (Athens time)**

**Changelog** (last 5, one line each; full history with backstory is in the Project as `complete-applications-skill-changelog.md`)
| When (Athens time) | What changed |
|---|---|
| 2026-10-14 14:46 | Index added; description made plain; long changelog moved word for word to the archive; client names, policy numbers and amounts in examples replaced with placeholders. No rule changed. |
| 2026-10-08 14:30 | Rule 9 reworded: skill changes go forward with the propose_skills review card; never claim live until Paul confirms he saved. |
| 2026-10-08 13:05 | Universal operating rules block and Delivery gate added at the top of the skill. |
| 2026-10-08 09:05 | Transaction folder naming rule corrected: covers life cover, RA and investments, monthly premium or lump sum; no investment segment for life cover. |
| 2026-10-07 09:31 | One unified application filename pattern; the word "Application" is mandatory after the product type. |

> **Standing rule:** whenever this SKILL.md is edited, add a one-line row at the top of the table above (Athens time), keep the table to 5 rows (drop the oldest), and update "Last updated" in the same edit. Put any edit with real backstory (a live mistake, a ruled-out approach) in `complete-applications-skill-changelog.md` instead of growing this file.

## Why this skill exists

Insurers and the FSCA don't accept a lookalike PDF — they accept *their* form, filled in. Open the firm's real AcroForm template (bundled in `assets/`), write values into its real named fields, and hand back that same PDF — never a recreation. Do not push the finished PDF into SharePoint as inline base64; save it into the client's OneDrive folder on Paul's machine instead (Step 6).

## How this skill is used (the application life-cycle)

1. **Before a follow-up meeting** where the client may accept a quote (Life, RA, Invest, Risk), this skill pre-fills the applications (Steps 1–6) and saves them in the `Applications` folder of the correct transaction folder.
2. **In the meeting**, once the client accepts, Paul completes the same application form live with the client and saves it over the pre-filled one, so there is ONE copy per application. Paul's live-typed form is the accurate record.
3. **After the meeting**, `client-teams-transcript-skill` reads the applications, reports the differences, and calls this skill in **Correction / Sync mode** (Step 7).

## Step 1 — Work out which application(s) are needed

From the proposal, RGAR, fact find, or the client's own instruction, identify each product/transaction that needs its own application:

- one OM Application Template fill per product *and* per contribution type — a recurring RA and a lump-sum Section 14 transfer into the same plan are two separate applications.
- a short-term/risk product (with OM or any other insurer) uses the General Short Risk Application Template instead — see `references/field-mappings.md` §2. First used in production for a Brightrock application on 30.09.26 and again on 08.10.26; if the layout ever stops matching the documented mapping, flag it back and re-derive the mapping.

## Step 2 — Gather the client's bio data once

Every OM application for the same client shares one set of personal/bio fields (full list in `references/field-mappings.md` §1). Pull these once from the client's Fact Find, prior applications, or CRM record, and reuse the same dict across every product sheet for that client.

(This is the initial pre-fill before a meeting. The stricter "current application only" source rule in Step 7.3 applies to Correction / Sync mode, not to this step.)

## Step 3 — Get the transaction-specific fields right

**Product name always carries the amount.** Build the `Product` value as `"<base product> - R <amount> p.m."` for recurring, or `"<base product> - R <amount>"` for a lump sum — e.g. `"OM Tax Free recurring - R 1,000 p.m."`, `"OM RA - Lump Sum - R 100,000.00"`. `Product` is a closed dropdown, so add the new value first with `add_product_option()`.

**Every application needs a real answer on replacement, not a guess.**
- If it genuinely isn't a replacement, set `IsReplacement` = No and `ReplacedPolicyNumbers` = N/A.
- If it is a replacement, find the actual insurer name and policy number being replaced — search the client's proposal comparison documents, fact find, RGAR, or the policy schedule itself. Write it as `"<Insurer>, Policy No. <number>"`, separating several with `; `. **Check the policy number against the schedule document, not an older draft** (an earlier Brightrock draft once had the replaced Outsurance policy number typed with a digit missing).
- If the file is contradictory or silent, ask Paul rather than guessing.

**Foreign tax number follows foreign tax obligation.** When `ForeignTaxObligation` = No, `ForeignTaxNumber` = N/A.

**Any field with an N/A option that doesn't apply gets N/A, not blank.** E.g. `DeferredPremiumFacility` for a lump-sum transaction is N/A.

**Source-of-funds knowledge.** `OriginateFrom` is only filled when `OwnKnowledge` = No; otherwise N/A.

**Signature date is the meeting date, filled in by the advisor — never left blank.** Format `DD/MM/YY`.

**Never invent client data.** If a field (banking details, ID numbers, beneficiaries, doctor, debit date, address, declarations) isn't in the file and Paul hasn't supplied it, leave it blank and list it plainly in the hand-back message so he can supply it.

## Step 4 — Fill the template

Use `scripts/fill_om_form.py` for OM (`fill_om_application()`). For the General Short Risk form, write values into the named fields listed in `references/field-mappings.md` §2 with `PdfWriter` and `auto_regenerate=True` so appearances are generated. One output PDF per application, never one PDF covering two products.

## Step 5 — Verify before delivering

1. **Field dump.** Read back the field values from the saved PDF and compare against what was intended — at minimum `Product` / `INSURER`, `IsReplacement`, `ReplacedPolicyNumbers` / policy number, `ForeignTaxNumber`, `OriginateFrom`, `SignatureDate` / `DATE`.
2. **Visual render.** `pdftoppm -png -r 100 out.pdf page`, then read the PNGs. If a dropdown value (INSURER, COVER LINES, WILL THIS POLICY REPLACE) is set in the field dump but does not appear in the render, that is a viewer/appearance-stream issue, not necessarily a data error: say so plainly in the hand-back, do not claim the render passed, and ask Paul to confirm it displays in his own PDF viewer.

Only proceed to delivery once both checks pass (or the render gap is disclosed as above).

## Step 6 — Where the finished file goes

Two deliveries, both required:

1. **Send it in chat** with the file-delivery tool so Paul has it in the conversation immediately.
2. **Save it directly into the client's OneDrive folder on Paul's own machine** — the reliable path (do not push base64 into SharePoint).

To find the right local folder for a client:

1. `sharepoint_folder_search` for the client's surname. The `webUrl` reveals the advisor's site (`/Paul/`, `/Cameron/`, etc.) and the folder path, typically `New Business/<Surname, Firstname>/<transaction folder>/Applications`. Some clients have several transaction folders; use the one holding the current quote/proposal documents.
2. On Paul's machine the root is `C:\Users\Paul\liferisk.co.za\Company - Paul\New Business\` (grant access with `device_request_folder_access` if not already connected). The client's top folder can contain an older unnamed folder (`<Surname, Firstname>\<Surname, Firstname>\`, with archived applications) AND the current transaction folder. Use the current transaction folder; if ambiguous, ask Paul.
3. Confirm the `Applications` subfolder exists with `device_list_dir` before writing; if it doesn't, stop and ask rather than inventing a folder name.
4. Deliver the file: send it in chat first, then `device_commit_files` with the full Windows path, using the naming convention below.

   **TRANSACTION FOLDER NAMING RULE (mandatory, corrected 08/10/2026):** once a transaction is chosen (accepted, or the current quote being applied for), rename the current transaction folder to one of these two forms, depending on whether the amount is a monthly premium or a lump sum being invested:

   - Monthly premium: `"<Surname, Firstname> - (<Insurer> - <Investment name> - <Type> - R <premium> p.m.)"`
   - Lump sum being invested: `"<Surname, Firstname> - (<Insurer> - <Investment name> - <Type> - R <lump sum amount> - Lump Sum)"`

   - **Insurer** — the abbreviation used on the application (e.g. `BR` for Brightrock, `OM` for Old Mutual; for investment providers the provider name). Confirm with Paul if it's a new insurer or provider.
   - **Investment name** — the product or fund/portfolio name for RA and investment transactions (e.g. `Optimal RA`, `Tax-Free`, `Flexi`). **Life cover has no investment, so omit this segment entirely** — life cover uses `(<Insurer> - <Type> - R <premium> p.m.)`. Confirm with Paul when unsure.
   - **Type** — for life/risk cover exactly one of `Personal Covers`, `Buy & Sell`, `Contingent Liability` or `Keyman`. For RA/investment transactions use the transaction type Paul gives (e.g. `Recurring`, `Lump Sum`, `Section 14 transfer`) and confirm if it is not obvious.
   - **Premium / amount** — `R <premium> p.m.` for a monthly premium, or `R <lump sum amount> - Lump Sum` for a lump sum being invested, using the figures from the chosen quote.

   Examples:
   - Life cover: `Surname, Firstname - (BR - Personal Covers - R 1,000.00 p.m.)`
   - Monthly RA/investment: `Surname, Firstname - (OM - Optimal RA - Recurring - R 2,800 p.m.)`
   - Lump sum investment: `Surname, Firstname - (Ninety One - Flexi - Lump Sum - R 100,000.00 - Lump Sum)`

   Rename with `mv -n` inside the connected folder (`device_bash`), never by overwriting. If it is already renamed, leave it. Do not rename the older unnamed folder without asking Paul. Confirm the new path with `device_list_dir` before writing to it.

   **APPLICATION FILENAME RULE (mandatory): one unified pattern across every application type — the filename must always include the word "Application" directly after the product type.**

   `"<Insurer abbreviation> - <Product type> Application - <DD.MM.YY> - <R amount p.m. OR R amount - Lump Sum> - (<Client First Last>).pdf"`

   - **Insurer** — the abbreviation (e.g. `OM` for Old Mutual, `BR` for Brightrock); confirm with Paul if new.
   - **Product type** — for OM applications the base product name (e.g. `Optimal RA`, `Tax-Free`, `Flexi`); for Risk Cover applications the cover line matching the template's selector — `Personal Covers`, `Business Covers`, `Buy & Sell`, `Contingent Liability`, or `Keyman Cover`.
   - **Date** — `DD.MM.YY`, the application's signature/meeting date.
   - **Amount** — `R <amount> p.m.` for recurring, or `R <amount> - Lump Sum` for lump sum.
   - **Name** — first name then surname inside parentheses.

   Examples:
   - `"OM - Optimal RA Application - 27.08.26 - R 1,000 p.m. - (Client First Last).pdf"`
   - `"OM - Optimal RA Application - 27.08.26 - R 100,000.00 - Lump Sum - (Client First Last).pdf"`
   - `"BR - Personal Covers Application - 30.09.26 - R 1,000.00 p.m. - (Client First Last).pdf"`

5. **Superseded drafts.** When a new application replaces an older draft for the same transaction, the older draft is removed only after Paul approves: request delete permission with `device_request_delete_permission` for the connected root, name the file in the reason, and only then delete it.
6. If the write is rejected because the destination file is open in another application, tell Paul plainly and ask him to close it or confirm a different filename — don't force it or silently rename around the conflict.

Once saved into the OneDrive folder, it syncs up to SharePoint on its own.

## Step 7 — Correction / Sync mode (after a client meeting)

Use this mode when `client-teams-transcript-skill` calls this skill with a list of differences after a follow-up meeting, or when Paul says an application detail has changed. It corrects EXISTING applications; it never starts from a blank template unless an application for that transaction does not exist yet (then use Steps 1–6).

**7.1 Inputs.** Client; meeting date; the list of corrections (field, new value, which application it came from); and Paul's carry-across instruction if he gave one. Without an instruction, ask (7.4).

**7.2 Find every application for the client.** In each **current** transaction folder, list the `Applications` folder and pick the real applications (filename contains "Application"). Ignore blank templates and non-application documents unless Paul asks. Ignore earlier years and completed transactions unless Paul tells you to include them. Correct ALL the client's current applications, whether the quote was accepted or still pending.

**7.3 Source of truth.** Paul's live-completed application is the accurate record; the meeting transcript is only a cross-check. New values come from that application, not from the garbled transcript (account numbers, IDs, street names, child names). When carrying a detail from one application to another, take it ONLY from a **current application in a current transaction folder** — never from a previous year's application or an older transaction — unless Paul explicitly says to. Paul may direct you to the `4. FICA & POI` folder's Proof of Bank account for banking details; if older than 3 months, ask Paul first. If two current applications hold different values for the same field, STOP and ask Paul.

**7.4 Build the change plan and ask.** For each application, list the fields that differ or are blank against the new values (old -> new). Show Paul the plan and ask, per detail, whether to carry it across to all applications, only some, or none. Default is ASK. A standing carry-across instruction from Paul is followed without asking again for those details. Ask first if a value is garbled or ambiguous, the mapping is unclear, the application is for a different person, or sources conflict.

**Different person / payer.** Details only carry across where they belong to the same person for that role. Product-specific answers (replacement, DeferredPremiumFacility, source of funds, declarations, debit date, doctor, children) are never carried across unless Paul says so.

**7.5 Apply in place — one copy, overwrite.** Stage the existing file fresh from OneDrive immediately before editing. Change ONLY the planned fields, leave every other value untouched, and do not touch signature fields. Save over the same filename in the same `Applications` folder: ONE copy only, nothing deleted. Rename only if the correction makes the name wrong — then ask Paul first. Commit with `device_commit_files` using the `expectedMtimeMs` from staging so a newer edit by Paul is never overwritten. If the file is locked, tell Paul and ask him to close it.

**7.6 Verify.** (a) Field dump before vs after: only the planned fields changed; (b) visual render of each corrected application (see the Step 5 note on dropdown values); (c) values match the source application.

**7.7 Report back to Paul.** One short block per application: file name, fields changed (old -> new; mask account and ID numbers to the last 4 digits), fields still blank or needing input, anything skipped and why.

### Field crosswalk (OM form <-> General Short Risk form)

| Detail | OM field | General Short Risk field |
|---|---|---|
| Title | `Title` | `Text Box 3` |
| First names | `FullName` (split into names/surname) | `Text Box 4` (full names) |
| Surname | `FullName` | `Text Box 4_2` |
| ID number | `IDNumber` | `Text Box 4_3` |
| Cell | `TelCell` | `Text Box 4_4` |
| Work phone | `TelW` | `Text Box 4_5` |
| Email | `Email` | `Text Box 5` |
| Residential address | `ResidentialAddress` (one line) | `Text Box 4_6` unit, `4_7` complex, `4_8` street no., `4_9` street name, `5_2` suburb, `5_3` city, `4_10` region (split the address; ask if ambiguous) |
| Postal/residential code | `ResidentialCode` | `Text Box 4_11` |
| Account holder | `AccountHolder` | `Text Box 5_4` |
| Bank | `NameOfBank` (dropdown) | `Text Box 5_9` |
| Branch code | `BranchCode` | `Text Box 4_18` |
| Account type | `AccountType` (dropdown) | `Text Box 4_19` |
| Account number | `AccountNumber` | `Text Box 5_10` |
| Beneficiary 1 | `BenName` + `BenSurname`, `BenIDNumber`, `BenRelationship`, `BenShare` | `Text Box 5_15`, `5_16`, `4_23`, `4_24` |
| Beneficiary 2 | `BenName_2` + `BenSurname_2`, `BenIDNumber_2`, `BenRelationship_2`, `BenShare_2` | `Text Box 5_17`, `5_18`, `4_25`, `4_26` |

OM-only (carry OM -> OM only): `TaxNumber`, foreign tax fields, `MaritalStatus` group, occupation/employment fields, `HighestQualification`, `PostalAddress`/`PostalCode`, `Tel*`, `Beneficiary 3`, `Nationality`, `CountryOfBirth`, source-of-funds fields. Risk-only (carry Risk -> Risk only): doctor name/phone/years, debit date, children, insolvency/debt-review answers, existing-insurance fields, best phone time.

## Reference

- `references/field-mappings.md` — full field name/type/dropdown-option tables for both bundled templates, plus the General Short Risk field mapping.
- `assets/OM_Application_Template.pdf` — the real, blank OM AcroForm.
- `assets/General_Short_Risk_Application_Template.pdf` — the real, blank WR general short-term/risk AcroForm.
- `scripts/fill_om_form.py` — `fill_om_application()`, `add_product_option()`, `dump_filled_values()`.

<!-- FILE: references/field-mappings.md -->

# Field mappings for the bundled application templates

Both templates in `assets/` are real, fillable PDF AcroForms — every box on the
page is backed by a named form field. Always fill these by writing values into
the actual named fields (pypdf, or an equivalent AcroForm library). Never
recreate the page from scratch with a drawing library (reportlab, etc.) — a
lookalike is not the firm's actual form and will not be accepted as the
compliance record.

Dump a template's fields yourself at any time to confirm names/types/options
haven't changed:

```python
from pypdf import PdfReader
r = PdfReader("assets/OM_Application_Template.pdf")
for k, v in r.get_fields().items():
    print(k, v.get("/FT"), v.get("/Opt"))
```

---

## 1. OM Application Template (`OM_Application_Template.pdf`)

Old Mutual's application/capture-sheet AcroForm — used for RA (recurring and
lump sum / Section 14 transfer), Tax-Free (recurring and lump sum), and Flexi
Investment applications. One template, reused for every OM product; the
`Product` field's dropdown selects which product this instance is for.

| Field name | Type | Options (if a dropdown) |
|---|---|---|
| `Product` | dropdown | OM Flexi Investment Plan; OM RA – Xtra Max 8.5% - section 14 transfer; OM RA – Xtra Max 8.5%; OM RA – Xtra Max 5%; OM Optimal RA – Recurring; OM Tax Free recurring; OM Tax Free Lumpsum; OM RA – Wealth recurring |
| `DateOfEntry` | text | — |
| `DeferredPremiumFacility` | dropdown | Yes / No / N/A |
| `IsReplacement` | dropdown | Yes / No |
| `ReplacedPolicyNumbers` | text | — |
| `Title` | dropdown | Mr / Mrs / Ms / Miss / Dr |
| `FullName` | text | — |
| `IDNumber` | text | — |
| `CountryOfBirth` | text | — |
| `Nationality` | text | — |
| `CorrespondenceLanguage` | text | — |
| `MaritalStatus` | dropdown | Single / Married / Divorced / Widowed / Separated / Civil Union / Customary Marriage / Life Partner / Cohabiting |
| `MaritalDate` | text | — |
| `MaritalContractType` | dropdown | In Community of Property / Out of Community – with Accrual / Out of Community – without Accrual / Customary Marriage / Civil Union / Religious Marriage / Foreign Marriage / N/A |
| `TaxNumber` | text | — |
| `ForeignTaxObligation` | dropdown | Yes / No |
| `ForeignTaxNumber` | text | — |
| `TelH`, `TelW`, `TelCell` | text | — |
| `Email` | text | — |
| `PostalAddress`, `PostalCode` | text | — |
| `ResidentialAddress`, `ResidentialCode` | text | — |
| `Occupation`, `EmploymentPosition`, `EmploymentIndustry` | text | — |
| `HighestQualification` | dropdown | Matric / Matric & Diploma / 4-Year Diploma / 3-Year Degree / Postgraduate |
| `EducationOther` | text | — |
| `BenName`, `BenSurname`, `BenCellNumber`, `BenIDNumber`, `BenRelationship`, `BenShare` | text | beneficiary 1 |
| `BenName_2` … `BenShare_2` | text | beneficiary 2 (same fields, `_2` suffix) |
| `BenName_3` … `BenShare_3` | text | beneficiary 3 (same fields, `_3` suffix) |
| `NameOfBank` | dropdown | Absa Bank / Access Bank / African Bank / Albaraka Bank / Bank Zero / Bidvest Bank / Capitec Bank / Discovery Bank / FNB / FNB Namibia / GoTyme Bank (TymeBank) / Investec / Nedbank / OM Bank (Old Mutual) / Postbank / Sasfin Bank / Standard Bank / Other |
| `BranchCode`, `AccountHolder`, `AccountNumber` | text | — |
| `AccountType` | dropdown | Current / Savings / Cheque / Other |
| `SourceOfFunds`, `SourceOfIncome` | text | — |
| `KnownDays`, `KnownMonths`, `KnownYears` | text | how long the advisor has known the client, split across three fields — fill whichever unit applies, leave the other two blank |
| `FundsRaisedFrom` | text | — |
| `OwnKnowledge` | dropdown | Yes / No — does the advisor have personal knowledge of the source of funds? |
| `OriginateFrom` | text | only relevant when `OwnKnowledge` = No — "if not from own knowledge, where did the funds originate" |
| `Signature` | text | — |
| `SignatureDate` | text | — |

### Adding a new `Product` dropdown value

`Product` is a closed dropdown (`/Opt` array), not free text, and per the
premium-amount rule below every filled form needs a client- and
amount-specific value (e.g. `"OM Optimal RA – Recurring - R 2,800 p.m."`)
that won't already be in the list. Add it to the `/Opt` array before setting
the field value — see `scripts/fill_om_form.py`'s `add_product_option()` for
the exact AcroForm manipulation (inserts the new string next to the base
product it's a variant of, so the dropdown stays organised).

---

## 2. General Short Risk Application (`General_Short_Risk_Application_Template.pdf`)

Wealth Revolution's own generic short-term/risk application, used across
multiple insurers (Momentum, Brightrock, Discovery, Old Mutual, Liberty,
Sanlam, Stanlib — set via the Insurer dropdown). Single page. Unlike the OM
template, the field *names* in this PDF are generic (`Text Box 4_7`, `List
Box 3_3`, …) — they carry no meaning on their own. The mapping below was
built by reading each field's on-page position against the visible labels,
confirmed against a rendered image of the form. If Wealth Revolution ever
issues a revised version of this template, re-derive the mapping the same
way (dump field names + `/Rect` positions with pypdf, sort top-to-bottom then
left-to-right, render the page to PNG with `pdftoppm`, and read the two side
by side) rather than assuming field names carry meaning.

| Field name | Label on form |
|---|---|
| `List Box 1` | INSURER (dropdown: Momentum / Brightrock / Discovery / Old Mutual / Liberty / Sanlam / Stanlib) |
| `Text Box 1` | Quote No |
| `List Box 2` | Cover Lines (Business / Personal) |
| `Text Box 2` | OWNER OF THE POLICY |
| `List Box 3` | THE POLICY OWNER IS RESPONSIBLE FOR PAYING THE MONTHLY PREMIUM (Yes/No) |
| `Text Box 3` | TITLE |
| `Text Box 4` | FULL NAMES |
| `Text Box 4_2` | SURNAME |
| `Text Box 4_3` | ID NUMBER |
| `Text Box 4_4` | CELL |
| `Text Box 4_5` | WORK |
| `Text Box 5` | E-MAIL |
| `Text Box 4_6` | UNIT NUMBER |
| `Text Box 4_7` | COMPLEX NAME |
| `Text Box 4_8` | STREET NUMBER |
| `Text Box 4_9` | STR NAME |
| `Text Box 5_2` | SUBURB |
| `Text Box 5_3` | CITY |
| `Text Box 4_10` | REGION |
| `Text Box 4_11` | POSTAL CODE |
| `Text Box 4_12` | BEST TIME FOR US TO PHONE YOU |
| `Text Box 4_13` | BEST WORK DAY FOR US TO PHONE YOU |
| `Text Box 4_14` | DR (doctor's name) |
| `Text Box 4_15` | DR TEL NO |
| `Text Box 4_16` | YEARS (with the doctor) |
| `Text Box 5_4` | ACCOUNT HOLDER (premium-payer's banking details) |
| `Text Box 5_9` | BANK NAME |
| `Text Box 4_17` | BRANCH NAME |
| `Text Box 4_18` | BRANCH CODE |
| `Text Box 4_19` | ACCOUNT TYPE |
| `Text Box 4_20` | DEBIT DATE (any date except the 10th–14th) |
| `Text Box 5_10` | ACCOUNT NUMBER |
| `Text Box 4_21` | CONTACT NUMBER |
| `Text Box 4_22` | EMAIL ADDRESS |
| `Text Box 5_11` | CHILD 1 — NAME & SURNAME |
| `Text Box 5_12` | CHILD 1 — ID NUMBER |
| `Text Box 5_13` | CHILD 2 — NAME & SURNAME |
| `Text Box 5_14` | CHILD 2 — ID NUMBER |
| `Text Box 5_15` | BENEFICIARY 1 — NAME & SURNAME |
| `Text Box 5_16` | BENEFICIARY 1 — ID NUMBER |
| `Text Box 4_23` | BENEFICIARY 1 — RELATION |
| `Text Box 4_24` | BENEFICIARY 1 — % OF BENEFIT |
| `Text Box 5_17` | BENEFICIARY 2 — NAME & SURNAME |
| `Text Box 5_18` | BENEFICIARY 2 — ID NUMBER |
| `Text Box 4_25` | BENEFICIARY 2 — RELATION |
| `Text Box 4_26` | BENEFICIARY 2 — % OF BENEFIT |
| `List Box 3_2` | EVER BEEN INSOLVENT OR SEQUESTRATED? (Yes/No) |
| `List Box 3_3` | ARE YOU CURRENTLY UNDER DEBT REVIEW? (Yes/No) |
| `List Box 3_4` | HAVE YOU APPLIED FOR ASSISTANCE WITH DEBT? (Yes/No) |
| `List Box 3_5` | WILL THIS POLICY REPLACE AN EXISTING POLICY? (Yes/No) |
| `Text Box 5_5` | EXISTING INSURANCE — COMPANY (only if replacing) |
| `Text Box 5_6` | EXISTING INSURANCE — Policy Number (only if replacing) |
| `Text Box 5_7` | CLIENT'S SIGNATURE |
| `Text Box 5_8` | DATE |

This template hasn't been run through the fill workflow in production yet —
when the first real request for a general short-term application comes in,
apply the same rules as the OM form (replacement lookup, N/A discipline,
signature date = meeting date) using this mapping, verify visually, and flag
back if anything about the layout doesn't match this table.
