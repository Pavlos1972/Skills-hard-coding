<!-- The live skill text as of 14/10/2026 12:21 (Athens time), kept as the rule-by-rule baseline. -->
---
name: "astute-summary-report-skill"
description: "Builds a verified Astute Report Summary PDF for Paul at Wealth Revolution: risk covers, investments, group risk, retirement funds, paid-up policies. Use for 'summarize the Astute/CCP report'."
---

# Astute Summary Report Skill

## Index

| # | Section | What it covers |
|---|---|---|
| 1 | Universal operating rules | The nine rules that apply to every step |
| 2 | Delivery gate | What must be done before a run counts as complete |
| 3 | Last updated + Recent changes | Athens-time stamp and the last 5 changes |
| 4 | Purpose and when to use it | What the skill produces and what triggers it |
| 5 | Step 1: Locate the Astute report | Client folder "5. Astute", local machine first |
| 6 | Step 2: Read the whole report | Every page and every provider block |
| 7 | Step 3: Verify product descriptions | Online, multi-source, never invented |
| 8 | Step 4: Content and report structure | Header, Sections 1-3, Additional Notes, flags |
| 9 | Step 5: Build the PDF | ReportLab layout, colours, checks |
| 10 | Step 6: Save and deliver | Same "5. Astute" folder, filename, chat hand-over |
| 11 | Key contacts and tools | Tools used and what for |
| 12 | Standing rules | The rules that must always hold |
| 13 | Verification checklist | Run before saying it is done |

## UNIVERSAL OPERATING RULES - READ FIRST, APPLY TO EVERY STEP OF THE TASK

*These rules come before everything else in this skill. They apply from the first message to the last, not just at the start. If anything below seems to conflict with these rules, these rules win.*

1. **Re-load this skill before you start, and again after any compression.** Open it in full and re-read it before you produce or change any deliverable. Never work from a summary of the rules or from memory of them.
2. **Source first - never invent.** Write only what is in the Astute report, what Paul told you, or what the insurer's own current public product information says. If something is unclear, ask or flag it. "It seems implied" is not a source.
3. **Read before you write.** Read the Astute report and the relevant product pages completely before drafting.
4. **Check before you claim.** Never say something is done, saved, proposed or live until you have checked it. Say what you checked.
5. **Deliver everything this skill lists, every time.** A run is not finished until every item in the Delivery gate and in Step 6 is done.
6. **Every correction re-opens the whole task.** When Paul corrects anything: re-check that point and everything related, fix it everywhere, re-run the Verification checklist, and re-deliver in full.
7. **Never lower the standard.** A frustrated user, a short request or a "quick" skill does not relax any rule here.
8. **If a rule cannot be met, stop and say so.** Never hand over partial work as complete.
9. **Changes to a skill:** edit the existing skill, never create a duplicate. Update its "Last updated" stamp (Athens time) and changelog. Put the full SKILL.md forward with the propose_skills tool. Never say it is live until Paul confirms he saved it. If the card does not appear, say so plainly.

**Delivery gate for this skill (rules 5 and 6 applied):** a run is complete only when ALL of these are done and confirmed in one line each: (1) the Astute report was located in the client's "5. Astute" folder (or supplied by Paul) and every page was read; (2) product descriptions were verified online per Step 3, and every figure was checked against the report; (3) the summary PDF was built to the Step 4 structure, with every flag from the standing rules included, and checked page by page as images; (4) the PDF was saved in the same "5. Astute" folder with the correct filename and the folder listing was checked; (5) the PDF was sent in the chat with the short flag summary. After ANY correction, repeat (2) to (5) for every deliverable that changed.

**Last updated:** 2026-10-14 12:21 (Athens/Greece time)

**Recent changes** (last 5, one line each; full history with backstory goes in this Project as `astute-summary-report-skill-changelog.md`)
| When (Athens time) | What changed |
|---|---|
| 2026-10-14 12:21 | Skill created from Paul's Astute project instructions, the layout and lessons of two earlier client summaries in the Astute Reports project, and the Master Skill Template. |

> Whenever this skill is edited: add a new one-line row at the top of the table (Athens time), update "Last updated", and put any edit with real backstory in `astute-summary-report-skill-changelog.md`. Keep the table to 5 rows.

## Purpose and when to use it

Turns a client's Astute Consolidated Client Portfolio (CCP) report into a polished, verified, tabulated PDF summary for Paul Kafentzis at Wealth Revolution (FSP45946). Use it whenever Paul asks to summarize, break down or redo an Astute report or CCP report for a named client. It does not analyze, critique or compare policies (that is `life-policy-schedule-analyzer`).

## Step 1: Locate the Astute report (exact to the letter)

Follow this order every time, without asking first:

1. **Local machine first.** Through the device bridge, check both locations under `liferisk.co.za` for the client's folder: `Company - Paul` and `Company - WR Clients` -> `Paul Kafentzis (Client Files)`. The report sits in the client's **"5. Astute"** subfolder. Use whichever location actually holds it.
2. **SharePoint only if the local machine cannot be reached** (it is normally reachable only around 8:45 Athens time on weekdays, so an unreachable machine outside that window is expected, not a fault). Run the same two-location check there.
3. **Ask Paul to attach the report** only after both have genuinely been tried, or use a report he has already attached.
4. **Never touch another broker's folder** under `Company - WR Clients`.
5. If "5. Astute" holds more than one report, use the most recent by report date unless Paul names another, and say which one you used.
6. Check the file really is a complete PDF (`file`, page count). Some "PDF" files are zipped page images: extract and view every page. If pages are missing, say so.

## Step 2: Read the whole report (exact to the letter)

Read every page. Record the report reference, report date, client name (and the name Astute holds if different), ID number and date of birth, and every provider block, including providers that returned "client record not found", "unable to match", or no row at all. Use the pdf-reading skill if the content is not already in view.

## Step 3: Verify product descriptions (judgment, within the rules)

For every product, search the web for the insurer's own current product page or guide, and cross-check with a second independent source before stating what the product is. Research confirms product names, structure and terminology only; every client-specific figure (cover amount, premium, dates, policy number, fund values) comes from the report itself. If a product cannot be confirmed online, say so in the table and rely on what the report states.

## Step 4: Content and report structure (fixed section order)

Header: title, client name, ID number, date of birth, report reference and date, requested by, and a one-paragraph note that descriptions were cross-checked against public provider information and that orange flags need verification.

**Section 1: Active Policies - Personal Risk Covers and Investments.** Risk Covers first, then Investments. One gold heading band per insurer. One table per policy group with these columns:
- Risk covers: Policy Number / Product Name (verified) with a short accurate description / Status and start date / Benefit(s) and cover amount / Stand-alone or Accelerated / Premium and Premium Pattern.
- Investments: Policy Number / Product Name (verified) with description / Status and start date / Values (premiums paid, fund value, surrender value, Two-Pot pots where shown) / Premium Pattern / Fund allocation. Add owner, life assured, premium payer and beneficiaries (with percentages) under each policy.
- For every benefit state **Stand-alone** or **Accelerated**; if the report does not allow it, write "Unable to determine - verify with insurer".
- For every policy state the premium pattern: **ACI**, **ABI**, **age-rated**, **fixed**, or **other** (for example single payment, or a fixed escalation rate). Use the insurer's own naming (for example funding pattern plus annual benefit increase) and the stated escalation percentage.

**Section 2: Group Risk and Retirement Funds.** Table: Category / Reflected on Astute? / Details. State plainly whether Group Risk cover exists and whether a Pension or Provident Fund is reflected. If present, give all details: insurer, employer, fund name, membership start, salary, retirement age and date, investment allocation, values, company and member contributions, each group risk benefit with cover amount and termination age, and beneficiaries.

**Section 3: Paid-Up Policies.** List every policy Astute labels paid-up, with full details. If none, say so plainly.

**Additional Notes: Inactive, Lapsed or Surrendered Policies.** Policies that are neither active nor labelled paid-up, with the same full details.

**General Verification Notes.** Always include the cession note (see standing rules), and one line naming providers that returned "not found" or "unable to match".

**Flag boxes (orange).** Place a flag directly above the affected table for: an unknown or thinly described product, an RA versus endowment wrapper ambiguity, a status contradiction between package and underlying policies, a provider that returned no data, and any zero or missing values.

## Step 5: Build the PDF (a pattern to follow)

Use ReportLab Platypus in the workspace (`pip install reportlab --break-system-packages` if missing; `pdftoppm` for previews). Do not draw from memory of an earlier client: build from this run's report only.
- Landscape A4, 15 mm margins, column widths in millimetres, `repeatRows=1` on every table.
- Custom `ParagraphStyle` objects for all cell text (default styles do not render correctly in table cells). Escape `&` as `&amp;` and use `<br/>` for line breaks inside paragraphs.
- Colours: navy `#1B2A4A` for the title, section bars and table headers; gold `#9C7A28` for insurer bands; light grey `#F2F2F2` row stripes with `#DADADA` grid; flag boxes as a nested Table with background `#FFF4E5`, border `#C97A1A`, bold title in `#C97A1A` and text in `#5A3E00`.
- Footer and page numbers through `onFirstPage` and `onLaterPages`: "Astute Report Summary - [Client name] - Confidential" and "Page N".
- Copy every figure to the cent. Any total shown is added up in code from its components and must equal what the report shows; if it does not, flag it.
- Convert every page to PNG with `pdftoppm`, look at each one, and fix overflow, clipped text or a stranded heading before delivering.

## Step 6: Save and deliver (exact to the letter)

1. **Filename:** `Astute Report Summary - DD.MM.YY - (FirstName Surname).pdf` (date = the Astute report's own date; name = client first name then surname).
2. **Save into the same "5. Astute" folder** the report was read from: local machine first through the device bridge, SharePoint (`Microsoft_365:sharepoint_upload_file`) only if the machine is unreachable. Never overwrite an existing file without checking; if one exists, keep both with a version suffix and tell Paul.
   If the report was found elsewhere in the client's folder, save the summary beside it and tell Paul. If Paul attached the report and the client's folder cannot be found, deliver in the chat only and say plainly that it was not saved.
3. **List the folder** and confirm the PDF is there before saying it is saved.
4. **Send the PDF in the chat** (SendUserFile) as well. The chat copy never replaces the saved copy.
5. **Chat summary:** one line saying where it was saved, then a short numbered list of every flag Paul should verify, most important first.

## Key contacts and tools

No named contacts. Paul requests the summary and reviews it.

| Tool | Used for |
|---|---|
| Device bridge (`mcp__remote-devices__` tools) | Reading the report from, and saving the PDF to, the client's "5. Astute" folder |
| `Microsoft_365:sharepoint_*` tools | Same, only when the local machine is unreachable |
| Web search and fetch | Verifying product descriptions (Step 3) |
| pdf-reading skill, ReportLab, `pdftoppm` | Reading the report, building the PDF, checking pages as images |
| SendUserFile | Delivering the PDF in the chat |

## Standing rules

- The deliverable is always a PDF, never chat text alone.
- Never write a figure that is not in the report. A figure that is unclear is flagged, not guessed.
- Cession status is not in Astute's data: never state that a policy is or is not ceded. Always include the general cession note, and flag any policy held with a bank's insurance arm for direct verification with the insurer.
- Contradictions in the report (for example a package marked Active whose underlying policies are Inactive) are flagged in the document, never silently resolved.
- Missing or zero values returned by a provider are flagged as absent data needing verification, not treated as real zeros.
- An unknown product type is flagged prominently, never assumed.
- Only policies Astute labels paid-up go in Section 3. A policy with zero values but no paid-up label is flagged, not declared paid-up. Surrendered and lapsed policies go in Additional Notes.
- A provider that returned no row at all is not proof of no cover: say so in the flag.
- Every benefit carries a stand-alone or accelerated label and every policy a premium pattern.

## Verification checklist (run before saying it is done)

- [ ] Every page of the report was read, and the file was complete.
- [ ] Every product description was verified online, or marked as unverified.
- [ ] Every figure matches the report to the cent; every total was added up in code.
- [ ] Sections 1 to 3, Additional Notes (where applicable) and General Verification Notes are present in order.
- [ ] Risk covers come before investments, with one heading band per insurer.
- [ ] Every benefit has stand-alone or accelerated; every policy has a premium pattern.
- [ ] All required flags are in the document, including the cession note.
- [ ] Every page was viewed as an image with no clipping or overflow.
- [ ] Saved in "5. Astute" with the correct filename, and the folder listing was checked.
- [ ] PDF sent in the chat with the numbered flag list.