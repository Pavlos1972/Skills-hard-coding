<!-- The live skill text as of 13/10/2026 14:50 (Athens time), kept as the rule-by-rule baseline. REDACTED: a client ID number in the Step 2 example was replaced by a placeholder. -->
---
name: "wr-roa-builder"
description: "Builds a Record and Confirmation of Advice (ROA) for Paul Kafentzis (FSP45946) from the ROA Template 2026, taking the answers from the client's file. Use when Paul asks for an ROA or Record of Advice."
---

# WR ROA Builder

## Index

| # | Section | What it covers |
|---|---|---|
| 1 | Universal operating rules + Delivery gate | The nine rules for every step, and what must be done before a run counts as complete |
| 2 | Last updated + Changelog | Athens-time stamp, last 5 changes, standing edit note, skill saving |
| 3 | Core principle: one ROA = one bundle | Risk, Retirement or Investment, never mixed; Health Care never produced |
| 4 | Step 0 - Locate the client's source documents | Local machine first, then SharePoint/Outlook; failure signatures |
| 5 | ROA date | Always the date the client gave the go-ahead |
| 6 | Step 0b - Auto-derive the Step 1 answers | Sources and rules per answer; one confirmation table |
| 7 | Step 1 - Run the setup checklist first | Questions per bundle, Status defaults, declined vs FNA-not-accepted, insurer notes |
| 8 | Step 2 - Read the source documents | Figures, client name and ID; reading a BrightRock quote |
| 9 | Step 3 - Fill in the dropdown fields | Fixed rules for each Need Identified and insurer field |
| 10 | Document construction | Building the .docx with build_roa.py |
| 11 | Step 4 - Reason text | Risk response bank; Retirement/Investment embedded reply email and image procedure |
| 12 | Step 5 - ROA Reference No. | Risk and Retirement/Investment formats; Old Mutual Tax-Free shortcut |
| 13 | Delivery filename | Required file name for every bundle |
| 14 | Step 6 - Fixed constants | Planner, FSP number, next review date |
| 15 | Step 7 - Mandatory pre-delivery audit | The 21 checks before delivery |
| 16 | Delivery | Path 0 (local device), Path 1 (content text), Path 2 (manual) |
| 17 | Reference material | The bundled files and what each is for |
| 18 | A note on scope | The skill carries no client data |

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

**Delivery gate for this skill (rules 5 and 6 applied):** a run is complete only when ALL of these are done and confirmed in one line each: (1) the source documents were located and read and the setup answers derived (Steps 0, 0b and 1-2); (2) the ROA .docx was built per Document construction, with the Step 7 mandatory pre-delivery audit completed; (3) the finished ROA was sent in the chat with the exact required delivery filename; (4) the same file was saved in the client's folder per the Delivery section, and the tool result was checked (the full path appears in the written list and nothing was rejected). After ANY correction, repeat (2) to (4) for every deliverable that changed.

**Last updated: 2026-10-13 14:50 (Athens time)**

**Changelog** (last 5, one line each; full history with backstory is in the Project as `wr-roa-builder-changelog.md`)
| When (Athens time) | What changed |
|---|---|
| 2026-10-13 14:50 | Index added; description made plain; long changelog entries moved word for word to the archive; client names replaced with placeholders; dated wording tidied. No rule or behaviour changed. |
| 2026-10-08 14:29 | Rule 9 reworded: changes are put forward with propose_skills and never called live until Paul confirms he saved them. |
| 2026-10-08 13:20 | Universal operating rules block and Delivery gate added at the top. |
| 2026-10-06 16:25 | Step 0b added (answers auto-derived from the client's file); Insurers Considered default; premium taken from inside the accepted quote; verbal acceptance valid for the Risk ROA date; bundled template and responses bank are the masters; Step 0 local machine first; Step 4 wording for a new Risk cover type; Disability and Income Protection Need Identified options. |
| 2026-09-25 | Previous version (see `wr-roa-builder-changelog.md`). |

> **Standing rule - not optional:** whenever this skill is edited (SKILL.md, the build script or any reference file), add a new one-line row at the top of the table above (Athens time), keep the table to 5 rows (drop the oldest), and rewrite "Last updated" to the current Athens date and time in the same response as the edit. Put any edit with real backstory (a caught mistake, a ruled-out approach, a reversed decision) in `wr-roa-builder-changelog.md` instead of growing this file.

> **Skill saving:** skill edits are saved by Paul from a `propose_skills` review card (full SKILL.md each time). Never tell him an edit is live until he confirms he saved it.

This skill packages Paul Kafentzis's process for completing a Record and Confirmation
of Advice (ROA) for Wealth Revolution clients, using `assets/ROA_Template_2026.docx`.
This is a compliance document required under the General Code of Conduct (s9) — a
wrong dropdown selection, a mismatched reason paragraph, or a guessed figure is a
real-world compliance error, not a cosmetic slip.

## Core principle: one ROA = one bundle, per transaction

Every ROA covers **exactly one** of three bundles. Never mix bundles in the same
document.

| Bundle | Sections actively completed | All other sections |
|---|---|---|
| **Risk** | Death (Life), Lump Sum Disability, Income Protection (1st 24 months + After 24 months), Dread Disease | Marked "Do not Review" |
| **Retirement** | Retirement Planning only | Marked "Do not Review" |
| **Investment** | Investment Planning only | Marked "Do not Review" |

**Health Care is never produced as an ROA.** Its Status dropdown stays at its default
("DO NOT REVIEW") and is never actively touched.

For sections marked "Do not Review" because they're outside the current bundle, the
"Reason this product suits your needs (required — s9(1)(c))" textbox always reads:
> "This need was not considered in this Review meeting."

## Step 0 — Locate the client's source documents (local machine first, SharePoint only if the device is unreachable)

**Local machine first** via the device bridge: `liferisk.co.za\Company - Paul\New Business\[Surname, First Name]\...` (also check `Company - WR Clients\Paul Kafentzis (Client Files)`). Use the SharePoint/Outlook search below only if the local machine cannot be reached.

Client documents almost never arrive as chat uploads — they live in the client's own
folder under `Paul/New Business/[Surname, First Name (...)]/` in SharePoint. Locate
them there first; only ask the user to upload something if it genuinely can't be
found.

1. **Find the client folder** with `Microsoft 365:sharepoint_search`, querying the
   client's surname. A client can have **multiple sibling folders** for different
   products/transactions at once (e.g. an OM Optimal RA folder alongside an OM Tax
   Free folder and an on-hold Risk Covers folder) — confirm which one matches the
   bundle/product actually being built before pulling documents from it; don't assume
   the first result is the right one.
2. **Pull the specific documents needed** — Fact Find Summary Report, FNA/comparative
   quote, Email Proposal, etc. — via `sharepoint_search` (optionally scoped with
   `folderName`) or by browsing the client folder's subfolder listing
   (`1. Overview`, `2. Fact Find`, `Comparative Quotes`, `Applications`,
   `ROA & Bus ROA`, etc.) using `read_resource` on the folder's `file:///` URI. Always
   follow up with `read_resource` on a search hit's `uri` — the search result itself
   is only a short content snippet, not the full document.
   - **`folderName` filtering is not fully reliable** — a query can silently return
     zero hits even when the file is genuinely inside a folder by that name. If a
     targeted search comes up empty, retry with a broader folder name (e.g. drop the
     leading number, just `"Fact Find"`) or drop the folder filter entirely before
     concluding the document doesn't exist.
3. **Verify every required document from the Step 1 checklist is actually present and
   current** before proceeding — don't build from whatever happens to be sitting in
   the folder. Flag gaps explicitly (e.g. only a raw KYC/intake form on file, not the
   summarized Fact Find Summary Report; or a proposal on file for a different amount
   than what's actually being advised on) and ask the user how to proceed (generate
   the missing summary, request an updated proposal, confirm the old one still
   applies) rather than silently substituting the nearest document you found. Full
   example: `wr-roa-builder-changelog.md` (2026-08-14 entry).
4. **Check Outlook when a proposal isn't already saved to SharePoint as a PDF** — via
   `Microsoft 365:outlook_email_search` / `read_resource`, since an accepted proposal
   sometimes only exists in the Sent Items thread. If found only as an email, save or
   convert it to the Email Proposal PDF the document-construction step needs (see
   "Embedding the proposal email" below) rather than referencing the live email
   directly.
5. **Fact Find / KYC PDFs read via SharePoint's `read_resource` often come back as
   labels only, with none of the client's actual answers.** This is a real,
   recognizable failure signature, not a fluke: these forms have an interactive/visual
   answer layer that SharePoint's text-extraction doesn't capture, so the page reads
   as an empty template even though it's genuinely filled in. **Do not conclude the
   document is blank, and do not ask the user to manually retype values off their own
   screen.** The fix is to read the PDF from the local machine (stage it and render the
   pages visually), or, if the device is unreachable, ask the user to upload that
   specific PDF directly into the chat — once it's a local file (not a SharePoint
   reference), it can be rasterized page-by-page and read visually (see the
   `pdf-reading` skill), which does pick up values in that answer layer. Recognize this
   pattern immediately (multiple pages of field labels with zero filled values is the
   tell) rather than retrying the same SharePoint read with different page ranges or
   search queries first.

## ROA date — always the date the client gave the go-ahead, never today's date or the proposal-send date

**Standing rule, applies to every bundle (Risk, Retirement, Investment):** the ROA
date is the date **the client** gave their go-ahead on the specific proposal actually
being advised on. It is never today's date, never the date the ROA document happens to
get built, and never the date the original proposal email was first sent — only the
date the client actually committed.

- **If the client replied in writing** (email, WhatsApp, etc.) confirming acceptance,
  the ROA date is the date of that reply. Search for this first — it always takes
  priority over the fallback below if it exists.
- **If the go-ahead was given verbally** (a phone call or in-person conversation) with
  no written reply from the client, look for an adviser follow-up email that recaps
  what was agreed (e.g. "Great to have spoken to you today... you have requested to
  go ahead with... Please confirm the above"). When no later written client reply
  exists, the ROA date is the date of **that recap email** — it's the only dated
  record of the go-ahead.
- **A transaction can go through several proposed amounts before the client commits**
  — always use the date the client agreed to the specific figure the ROA is actually
  being built for, never an earlier round's date.
- **Risk bundle exception (confirmed by Paul):** verbal acceptance in the Teams meeting is sufficient for the ROA date; take it from the latest Follow-Up Appointment Summary Notes. If a written client reply or recap email exists with a different date, use the written one and tell Paul. (Retirement/Investment still need the client's own reply email.)
- Get this date right before building anything else — it determines the "Next
  review/meeting date" too, since that's always ROA date + 12 months (Step 6).

Worked example: `wr-roa-builder-changelog.md` (2026-08-25 entry, "ROA date sourced
from a verbal go-ahead recap email").

## Step 0b — Auto-derive the Step 1 answers (do this BEFORE asking Paul anything)

Do not ask the Step 1 questions one by one when the client's file already answers them. Read these sources, in this order, then show Paul ONE confirmation table (question | derived answer | source file) and ask only about genuine gaps or conflicts.

1. **Latest "WR Overview" PDF** in `1. Overview\2026` (newest by date in the filename): quotes presented, existing policies, products.
2. **The insurer application** (e.g. BrightRock General Short Risk Application) in the transaction folder's `Applications` folder: client name/ID, personal vs business cover lines, replacement section (replaced policy numbers), accepted benefits.
3. **Latest "Follow-Up Appointment Summary Notes"** in `2. Fact Find`: what was accepted, when, replacement context, risk tolerance outcome, insurers compared.
4. **Client email confirmation** (Outlook, matched on subject thread), if one exists.
5. **Risk Tolerance questionnaire** (`WR - New Risk Tolerance - ...` in `2. Fact Find`): the client's risk profile ("Calculated category"). If no Risk Tolerance has been completed, ASK Paul before building.
6. Quotes in the transaction folder's `Comparative Quotes` (FNA, Reduced/Revised, other insurers).

**Source rules per answer**
- **Bundle and Personal/Business:** Follow-Up Notes plus the application's cover-lines selection and the transaction folder name.
- **Insurers Considered:** default = the recommended insurer ONLY. Add another insurer only if (a) the Overview lists it, (b) the Risk transaction's `Comparative Quotes` folder genuinely holds a quote from it, or (c) the Follow-Up Notes state it was compared. Existing policies being replaced are not "considered" insurers.
- **Replacement, per cover type:** from the application's replacement section (replaced policy numbers), matched to cover types using the Overview's "Current personal covers" and the policy schedules. If a replaced policy cannot be matched to a cover type, ask. Remember an application holds one replacement section, but the ROA needs it per cover type.
- **Recommended vs Taken Up:** Recommended = the FNA quote; Taken Up = the LATEST accepted quote (Reduced or Revised, whichever is the most recent), per cover type, read from the Summary block (Step 2). **The premium used in the ROA Reference No. and the filename is the figure printed INSIDE the accepted quote document ("Total premium" on the Summary page)** — not the quote's filename, the Overview or the application if they differ (Example: the filename said R1172.79 while the quote document says R1,172.80).
- **ROA date (Risk bundle):** verbal acceptance on the Teams call is sufficient; take the date from the Follow-Up Notes. If a written client reply or recap email exists with a different date, use the written one and mention it. **Retirement/Investment:** the client's own reply email is still required (see Step 4).
- **Client name and ID:** from the application, cross-checked with the quote and the Fact Find Summary. The ROA keeps the client's ID in the confirmation line (this skill has always required it).
- **Risk profile:** Risk Tolerance questionnaire, confirmed by the Follow-Up Notes.

**Conflict rule:** if two sources disagree (other than the quote-premium rule and the verbal-acceptance date rule above), STOP and ask Paul, quoting both values and their sources. Never choose silently.

**Masters:** the ROA template and responses bank bundled in THIS skill (`assets/`, `references/`) are ALWAYS the masters. Never use copies sitting in a client's `ROA & Bus ROA` folder.

After Paul confirms the table, continue with Step 1's "Documents" check and Step 2 onward. Step 1 below lists what must be known; Step 0b is how to find it.

## Step 1 — Run the setup checklist first

Before building anything, confirm all of these are available — answered from the client's file per Step 0b wherever possible (ask Paul only what Step 0b could not answer). If any are genuinely missing after
that search, ask the user for them and wait — do not build a partial ROA. Every ROA
is for a **single client only** — this is a fixed rule, never ask about
joint/multiple clients.

**Interaction format:** use the button-selection tool for any question with a fixed
set of options, rather than asking as open text. Reserve typed input for things that
genuinely have no fixed list.
- **Buttons**: bundle (Risk/Retirement/Investment), Personal/Business (Risk only),
  replacement yes/no, taken up/declined (Risk cover types), risk profile
  (Conservative/Moderately Conservative/Moderate/Moderately Aggressive/Aggressive),
  Investment's Need Identified choice (Children Education Planning / General
  Investment Planning), lump sum vs. recurring/monthly (Retirement/Investment only).
- **Typed**: insurer(s) considered, product provider and product name
  (Retirement/Investment only), ROA date, document uploads, and the specific reason
  for any declined need.

**Always ask first (unless Step 0b already answered it):**
1. Which bundle is this ROA for — Risk, Retirement, or Investment?
2. Personal or Business assurance cover?
3. Client's risk profile

**If Risk:**
4. Which insurer(s) were considered? (Even when only one is ultimately recommended,
   s9(1)(b) requires documenting what was actually considered — don't assume it's
   only the insurer the quote happens to be from; Step 0b gives the default.)
5. Is this transaction a replacement of an existing policy, or not? Establish this
   **per cover type** in the active bundle (e.g. Life Cover, Lump Sum Disability,
   Income Protection, Dread) — never as a single blanket answer for the whole
   ROA, since one cover type can be a replacement while another isn't in the same
   document.
6. For each cover type in the active bundle: is the client taking this up, or
   declining it? If declining, ask for the specific reason to record in the "Reason
   this product suits your needs" textbox — there's no generic default sentence for
   this; it must be a real, asked-for reason.
7. ROA date — **the date the client gave the go-ahead, not today's date** — see the
   "ROA date" rule above for how to determine this.
8. Documents: FNA Quote, Reduced/Accepted Quote (if it differs from the FNA Quote —
   if the client accepted the FNA in full, the FNA Quote serves as both), and the
   Fact Find Summary Report (not the raw Fact Find).

**If Retirement or Investment:**
Retirement and Investment ROAs are never "Personal" or "Business" cover — skip that
question entirely for these two bundles (it's Risk-only) and ask these instead:
4. Which insurer(s) were considered?
5. **Which is the Recommended Insurer?** Asked as its own explicit question, separate
   from point 4 — for Risk, the recommended insurer can usually be read off the
   Accepted Quote itself, but Retirement/Investment have no Accepted Quote document,
   so this must always be asked directly rather than inferred.
5a. **Who is the product provider and what is the product name?** Asked explicitly —
   never inferred from the insurer field alone. Product provider is often but not
   always the same as the recommended insurer; product name is the specific plan
   (e.g. "Retirement Annuity Xtra Max", "Xtra Max Investment Plan"). Both feed the
   ROA Reference No. and delivery filename — see Step 5.
5b. **Is the amount a lump sum or a recurring/monthly amount?** Always ask this
   directly rather than assuming — Retirement/Investment transactions can be either
   (e.g. a Section 14 lump-sum transfer vs. an ongoing monthly contribution). This
   determines whether the reference number ends in "- Lump Sum" or "p.m." — see
   Step 5.
6. Is this a replacement of an existing policy — asked once, since only one need
   type (Retirement or Investment) is ever active in this bundle, unlike Risk where
   it's established per cover type.
   - **When the client has other Risk Cover in force that is NOT being replaced by
     this transaction**, the reason text must state, verbatim: "Although the client
     has other Risk Cover in force, this transaction does not constitute a
     replacement of that cover."
   - **Known open item — verify before relying on it:** policy replacement has at
     times been implemented in `build_roa.py`/`roa_data_schema.md` as a single
     document-level flag rather than a genuinely independent value per cover type,
     even though point 5 above requires it per cover type for Risk
     bundles. Before building a Risk ROA where replacement status actually differs
     across cover types, confirm the data schema and script currently carry an
     independent replacement flag per cover type — if they don't, flag this to Paul
     rather than silently building a document where one cover type's replacement
     wording leaks into another's. (The per-section `reason_text` is independent; the
     document-level `policy_replacement` flag drives only the "replace / not replace"
     wording in the Policy Replacement section — set it true when ANY cover type is a
     replacement.)
7. **Investment only**: is the Need Identified "Children Education Planning" or
   "General Investment Planning"? (Retirement's Need Identified has no equivalent
   choice — it's always fixed, see Step 3.)
8. ROA date — **the date the client gave the go-ahead, not today's date** — see the
   "ROA date" rule above for how to determine this.
9. Documents: **both** the Email Proposal PDF (what was sent to the client) **and the
   client's own reply email confirming go-ahead on it** — these are two different
   documents and the ROA needs both (see the "Non-negotiable" rule right below and
   Step 4 for what gets embedded and why) — **and the Fact Find Summary Report**
   (still needed for client name and ID, exactly as with Risk). There is no FNA Quote
   or Accepted Quote for these two bundles — only Risk uses those — but the Fact
   Find Summary Report is required for every bundle, since client name/ID always
   comes from it regardless of which bundle the ROA is for.

**Non-negotiable:** finding the original Email Proposal is not enough — you must also
find **the specific email where the client themself replied to give the go-ahead** on
that proposal (see the "ROA date" rule above, which already requires this same email
to source the ROA date). The document embedded in the ROA must be (or include) **the
client's own reply**, not just the proposal it responds to. In practice the client's
reply email usually already quotes the full original proposal beneath it (a normal
reply-in-thread), so embedding the reply email as it actually appears in Outlook
(header block + the client's own acceptance wording + the quoted proposal beneath)
satisfies both needs in one document — see Step 4 for exactly how to build this. Do
not embed a standalone proposal-only HTML/PDF that never shows the client's own words
accepting it. Full history: `wr-roa-builder-changelog.md` (2026-08-27 entry).

**No longer asked — derived automatically, do not ask these:**
- Whether a need was taken up or declined can usually be seen directly by comparing
  the FNA Quote to the Reduced/Accepted Quote (present with an amount = taken up;
  absent or zero = a candidate for the declined question above) — but the explicit
  decline reason still must be asked per point 6.
- The FNA scenario (accepted in full vs. reduced) is a straightforward comparison
  between the FNA Quote and the Accepted Quote, per cover type — there is always an
  FNA and always an Accepted Quote, so no separate "no FNA" question is needed.
- RAR reference number — removed as a question entirely. There is no reference
  number on a RAR, so this field is deleted from the delivered document (see Step 3).

**Status dropdown defaults, driven by point 6 above:**
- Every considered cover type in the active bundle defaults to **IMPORTANT**...
- ...**unless the client declined it**, in which case Status = **DO NOT REVIEW**,
  the data table is removed (same treatment as a section outside the active bundle),
  and the reason textbox holds the specific reason given in answer to point 6 — never
  a generic placeholder sentence.

**Declined vs. FNA-analyzed-but-not-accepted — these are two different states, do not
collapse them:**
- **`declined: true`** is reserved for a need declined outright, without ever being
  properly analyzed via an FNA. Status = "Do not Review", data table removed, reason
  textbox holds the specific reason asked for in point 6 above.
- **FNA-analyzed but the client didn't take up the recommended amount**: this is a
  *different* state, not a decline. Set `declined: false`, `status: "IMPORTANT"`,
  `taken_up_amount: 0`, and use the response bank's "FNA DONE / BENEFIT NOT ACCEPTED"
  paragraph (`references/WR_Risk_Cover_Responses_24_07_26.docx`) as the reason text —
  the section stays IMPORTANT and its data table stays in the document (showing the
  FNA-recommended amount against a zero taken-up amount), it is not treated like an
  out-of-bundle or declined section.
- `build_roa.py` enforces this for Disability specifically: if Disability is declined
  with no explicit `income_after24.reason_text` override supplied, the script raises a
  `ValueError` rather than silently falling back to default text — treat that error as
  a signal you're missing a real answer to point 6, not a bug to work around.

**A note on insurer coverage:** the quote-reading method below (Step 2) is currently
validated only for **BrightRock** proposals. If a client's quote comes from a
different insurer, flag this before proceeding — the reading method for that
insurer's document format needs to be worked out and added to this skill, the same
way BrightRock's was, rather than guessed at.

**A note on the insurer dropdown's fixed list:** the Insurers Considered / Recommended
Insurer fields are native dropdowns limited to 9 options (ALTRISK, CAPITAL LEGACY,
DISCOVERY, MOMENTUM, LIBERTY, SANLAM, OLD MUTUAL, BRIGHTROCK, STANLIB) — this list has
never been extended for Investment/Retirement business, where providers like
Ninety-One, Allan Gray, or Coronation are common. When the recommended insurer isn't
on the list, flag it, then write the correct name directly into the field as an
override (same technique as the Need Identified overrides) rather than forcing the
nearest dropdown option or leaving it blank. See `dropdown_field_map.md` for the
implementation note.

## Step 2 — Read the source documents; never assume values

- Every figure (Recommended Amount, Taken Up Amount, premium) comes from the client's
  actual quote documents — never carried over from a previous client, never estimated.
- Client name and ID come from the application and Fact Find Summary Report. ID format: 13 digits, no
  spaces, no dashes (e.g. `[13-digit ID]`).
- For Retirement/Investment proposal emails specifically: the figure that goes into the
  document is always **the confirmed accepted amount from the client's own reply**,
  never the amount originally proposed if the client's go-ahead was for a different
  figure — same principle as Risk's FNA-vs-Accepted-Quote distinction, just sourced
  from the email thread instead of two separate quote documents.

### Reading a BrightRock quote specifically
Always draw cover amounts from the **top-level "Summary" block** near the start of the
proposal (the "Value of your cover" table) — not the later "About your cover"
need-by-need breakdowns further into the document, which split totals out by
household/childcare/debt/etc. rather than giving one total per cover type.

Column/heading mapping in that Summary block:
- **"That's caused by death"** → Life Cover (always a lump sum)
- **"That's permanent"** → Lump Sum Disability (always a lump sum)
- **"That you can recover from"** → Income Protection (always monthly)
- **"Additional expense needs"** → Dread Disease / Severe Illness (always a lump sum)

The FNA Quote gives the **Recommended Amount**; the Reduced/Revised/Accepted Quote gives the
**Taken Up Amount** — both read from this same Summary block, per cover type,
independently. The "Total premium (including the policy fee)" on the same Summary page is the premium for the Reference No. and filename.

## Step 3 — Fill in the dropdown fields

The template's dropdowns are native Word content controls, not free text — the exact
option lists (verified from the document XML) are in
`references/dropdown_field_map.md`. Read that file before filling any section; it
contains the full 81-item product list and every field's valid options. Key fixed
rules:

- **Retirement → Need Identified**: hardcoded to "Retirement Planning" (optionally
  "Saving for Retirement" as an alternate wording) — not a dropdown selection. None
  of the three real dropdown options (preserve / Retirement Annuity / retirement)
  are used.
- **Investment → Need Identified**: hardcoded to one of two fixed values, asked per
  client — "Children Education Planning" or "General Investment Planning". Neither
  of the two real dropdown options (child's education / defined need) is used.
- **Retirement and Investment → Recommended Amount / Taken Up Amount**: not relevant
  for these two sections when active — both rows are removed from the table
  entirely (never left blank or "N/A"). Need Identified, Insurers Considered,
  Recommended Insurer, and Recommendation for Identified Need all remain.
- **Death → Need Identified**: always "Life Cover" — this is a hardcoded override,
  not a dropdown selection, since "Life Cover" isn't even one of the four listed
  options (pass away / key person / Estate Duties / children's education).
- **Lump Sum Disability and Income Protection (1st 24 months) → Need Identified**: NOT hardcoded by the script — you must pass `need_identified` in the data for both, or the field renders blank. Valid options: "Sickness and/or Income Protection Cover" / "Lump Sum Disability Cover" / "Retrenchment Cover". Use "Lump Sum Disability Cover" for Lump Sum Disability and "Sickness and/or Income Protection Cover" for Income Protection (1st 24 months).
- **Dread → Need Identified**: always "Comprehensive Severe Illness" (the only real
  option).
- **Insurers Considered**: minimum 1 of the 3 slots, up to all 3, matching what was
  genuinely compared for that client — never pad with unused slots, and leave unused
  slots visually blank (not "Choose an item.").
- **The "." insurer option**: a template error. Never select it.
- **Insurer/provider override text (Ninety-One, Allan Gray, Coronation, etc.)**: write
  the insurer name in **ALL CAPS** to match the style of the fixed dropdown list
  (e.g. `NINETY-ONE`, not `Ninety-One`) when using the `set_sdt_plain_text` override.
- **Financial Planner (author)**: always PAUL KAFENTZIS, never Gareth Saffy.
- **Health Care**: never produced at all — see "Document construction" below; the
  entire section is deleted from every ROA, not just left inactive.
- **Retirement → Recommendation for Identified Need, when the product is an Old
  Mutual retirement annuity**: type the client's **actual product name** (e.g.
  "Old Mutual Retirement Annuity Xtra Max") — a direct text override, not a
  selection from the 81-item master product list (the list has no dedicated Old
  Mutual RA entry at all; "Old Mutual - Max Investment" is a poor semantic match
  and is no longer used for this product). **Never hardcode a literal "Old Mutual
  Optimal Retirement Annuity" string here** — that was tried and explicitly
  rejected; this field must reflect the specific product actually sold. Same
  override technique as Death/Dread/Retirement Need Identified above. **Recurring
  regression — re-verify this before every Old Mutual RA build**; full history:
  `wr-roa-builder-changelog.md` (2026-08-10 entry).

## Document construction — build the actual .docx, don't hand-edit text

**Do not treat this as a fill-in-the-blanks text exercise.** The delivered ROA looks
structurally different from the raw template — inactive sections have their entire
data table *removed* (not left with "Choose an item." showing), and Health Care is
deleted outright. Getting this right requires editing `word/document.xml` directly,
not just typing over placeholder text.

Use `scripts/build_roa.py`, which already encodes all of this correctly (validated
against a real delivered ROA). Build a data dict per `references/roa_data_schema.md`
and run:

```bash
python3 scripts/build_roa.py assets/ROA_Template_2026.docx data.json output.docx
```

What the script does automatically, so you don't have to reason about XML each time:
- Removes the entire data table (Need Identified/Amounts/Insurers/Product) for any
  section outside the active bundle, leaving only the heading and the reason text.
- Removes the entire data table the same way for any cover type **within** the
  active bundle that the client declined (`declined: true` in that section's data) —
  Status is set to "Do not Review" and the reason textbox holds the specific reason
  given for declining, which must be supplied explicitly (the script raises an error
  if a declined section has no `reason_text` — there is no generic default for this).
- Deletes the Health Care section from the document entirely, every time.
- Deletes the RAR reference number field from its sentence entirely, every time —
  there is no reference number on a RAR, so the rest of the s9(1)(d)/Rule 19
  sentence is kept but the "RAR reference number: ___" portion is removed rather
  than filled with N/A.
- Forces Income Protector Planning After 24 Months to "Do not Review" with the fixed
  BR sentence, regardless of what's passed in for other risk-bundle sections.
- Applies the Death → "Life Cover" and Dread → "Comprehensive Severe Illness"
  overrides.
- Collapses dual lump-sum/monthly amount fields to a single clean value (e.g.
  "R 37,000 monthly") instead of leaving unused scaffolding text in place.
- **Retirement section's merged table row order:** the raw template physically
  places the Reason row *before* the Insurers Considered/Recommended
  Insurer/Recommendation rows (row0=reason, rows1-3=insurer fields) — the wrong
  order for filling s9(1)(b)/(c) content sensibly. `build_roa.py` reorders the
  `<w:tr>` elements (moves the reason row to the end) before filling, so the
  final document reads Need Identified → Insurers Considered → Recommended
  Insurer → Recommendation for Identified Need → Reason. **Recurring bug — this
  reorder step has been found completely missing more than once.** Re-verify the
  reorder code is present in `build_section()` before every Retirement build; full
  history: `wr-roa-builder-changelog.md` (2026-08-10 entry).
- Sets the next-meeting date to ROA date + 12 months.
- Formats the client ID confirmation line as "I, [Name], (ID: 1234567890123),
  hereby confirm" with clean single commas, and strips the literal "(Name)" label.
- Strips the unreliable `<w:dataBinding>` on the Client Name and ROA Reference
  Number controls before setting their text directly.
- Every `set_sdt_plain_text` / override call strips **both** the `<w:dataBinding>`
  element **and** the `PlaceholderText` character style reference
  (`<w:rStyle w:val="PlaceholderText">`) on the affected run — stripping only the
  data binding and leaving the style reference in place is a known way this has gone
  wrong before: the field fills correctly but renders in placeholder grey instead of
  black, which is easy to miss on a quick read and only shows up when zoomed in or
  printed. Check filled fields aren't grey during the visual audit.
- Every paragraph property block (`pPr`) built or edited by the script follows the
  Word schema's required child element order (`CT_PPrBase`) — `spacing` before `jc`,
  `rPr` always last — rather than whatever order feels natural to write; Word can
  silently reject or reflow a `pPr` with elements out of schema order.
- Strips leading/trailing `<w:tab/>` runs and stray whitespace the template bakes in
  before several dropdowns (2 tabs before Insurers Considered/Recommended Insurer, 1
  before most Recommendation for Identified Need fields) — these silently push text
  away from the left edge and are not fixed by setting paragraph alignment alone.
- Forces explicit left alignment on every field it fills in, and adds cell padding
  to reason textboxes so text doesn't touch the borders.
- Chains `keepNext`/`keepLines` through the entire accept/decline decision block (the
  "I hereby accept..." / "My final decision..." / "I decline... reasons:" lines and
  the blank input lines beneath) so a page break can never split it.
- Trims the template's ~11 trailing blank paragraphs after the signature line down
  to 2, removing the extra blank final page they otherwise cause.

After building, **always validate and visually check** before delivering — see the
commands in `references/roa_data_schema.md`. Don't skip the visual render; text-level
correctness doesn't guarantee the document isn't structurally broken.

If a client's situation needs something the script doesn't yet handle, extend the
script rather than hand-editing XML ad hoc for that one ROA — and note the change in
this file so it's permanent.

## Step 4 — Reason text for the "Reason this product suits your needs (required — s9(1)(c))" box

This box's content differs by bundle.

### Risk bundle
For **Life, Lump Sum Disability, Dread Disease, and Income Protection (1st 24
months)**, select the matching scenario paragraph from
`references/WR_Risk_Cover_Responses_24_07_26.docx`, evaluated **independently per
cover type** (FNA status × Replacement status — see that document's full scenario
list per cover type: Life, Disability, Dread, Income Protection each have their own
set). Copy the paragraph in, substituting only client-specific details (needs
considered, pronouns) where the paragraph requires it.

If a client's actual scenario doesn't cleanly match one canned paragraph (e.g. Life
accepted per the FNA in full, but Income Protection reduced to a different amount),
word each cover type's box accurately and independently — use judgement to stay
factually correct rather than forcing a mismatched paragraph.

**A cover type that is NEW (not replacing anything) while the client's OTHER cover is being replaced or stays in force:** the response bank's "NON-REPLACEMENT" paragraphs say "the client has no Risk Cover currently in force", which would be false. Use the matching FNA paragraph (accepted or reduced) up to the replacement sentence, then end with the verbatim sentence: "Although the client has other Risk Cover in force, this transaction does not constitute a replacement of that cover." (Example: Life and Lump Sum Disability replaced Instant Life policies; Income Protection and Severe Illness were new.)

Additional fixed rules layered on top of the response bank:
- **A need exists but the client doesn't want to pursue it**: "The client did not want
  to consider this need at this time."
- **Income Protector Planning After 24 Months** (BrightRock structural rule — BR's
  Income Protection only ever covers the first 24 months; permanence beyond that is
  worked into the Lump Sum Disability benefit instead): "This need has been worked
  into the client's Lump Sum Disability Cover Benefit." This applies regardless of
  what the client decided on their other covers.

### Retirement / Investment bundles
No response bank exists for these, and there's no FNA Quote or Accepted Quote — but
the **Fact Find Summary Report is still required**, the same as Risk, for client name
and ID. The substantiation source is **the client's own reply email confirming
go-ahead** on the proposal — not the outbound proposal email by itself.

**Non-negotiable (see Step 1 point 9 above): the document you embed must be, or
include, the client's own written acceptance — never a proposal-only document that
never shows the client's own words agreeing to it.** In practice the client's reply
almost always quotes the full original proposal beneath it (a normal reply-in-thread),
so build one composite "email as it actually appears" document:
1. A header block for the **reply itself** — From (the client's own address)/Sent
   (the reply's actual sent time)/To/Cc/Subject (usually "Re: ..." or "Re: FW: ...")
   — followed by the client's own acceptance wording verbatim (e.g. "kindly proceed
   with the attached").
2. Beneath that, the quoted chain exactly as Outlook shows it — an "On [date] at
   [time], [sender] wrote:" line for each intermediate forward, then the original
   proposal's own header block (From/Sent/To/Cc/Subject/Importance) and full body,
   reusing the same styling as the reply's own header so the whole thing reads as
   one continuous, real email thread rather than two stitched-together documents.
   See "Embedding the proposal email images" below for the concrete HTML-composition
   method (reuse the already-built proposal HTML as the quoted portion, prepend a
   new reply header + body + "On ... wrote:" divider ahead of it).

**Do not paste the email's text into the reason textbox as a dense wall of prose** —
it renders cluttered and is hard to audit against the source. Instead:
1. In the reason textbox itself (the existing bordered table cell), put one short
   line naming what's reproduced, e.g.: "The client's email reply confirming his
   go-ahead on this proposal ([date]), with the original proposal email quoted in
   full beneath it, is reproduced on the following pages." The pointer line must name
   the *reply* as what's being shown, not just the proposal it responds to — see
   `wr-roa-builder-changelog.md` (2026-08-27 entry) for why this wording matters.
2. Convert the composite (reply + quoted proposal) HTML's pages to images
   (`pdftoppm -jpeg -r 150`) and
   insert them as standalone paragraphs **immediately after the section's data table
   closes** (i.e. after the Insurers Considered / Recommended Insurer / Recommendation
   for Identified Need rows) — not inside any table cell. Give each image its own
   paragraph with a picture-level border (`<a:ln>` on the `pic:spPr`, not a table or
   paragraph border) and a small italic caption ("page X of Y"). Keep each image
   ≤ 5,000,000 EMU wide (≈5.5in) so a full-page screenshot plus its caption
   comfortably fits within one page's usable height.
   - **Why not inside the table cell:** a table row containing several full-page-tall
     images will span multiple pages, and when a table row splits across a page break
     its cell borders can render incorrectly — bleeding into or striking through the
     page footer. Standalone paragraphs don't have this failure mode: a paragraph
     that doesn't fit moves as a whole to the next page, so the border always wraps
     just that one image cleanly.

Retirement and Investment are never both active in the same ROA — whichever one
isn't the active bundle is treated exactly like any other out-of-bundle section (see
"Core principle" above): Status = "Do not Review", data table removed, reason text =
"This need was not considered in this Review meeting." No special-case wording is
needed for this — it's the same standard out-of-bundle treatment every section gets.

### Embedding the proposal email images — working procedure
`build_roa.py` does not do this step; it must be done as a **second pass** on the
script's output, using a separate embedding script (build one per the template
below if it doesn't already exist as a saved asset).

**Step 0 of this procedure — build the composite reply+quote HTML first, not just
the proposal HTML.**
1. Find the client's own reply email (per Step 1 point 9 and the "ROA date" rule —
   this is the same email that sourced the ROA date, found via
   `Microsoft 365:outlook_email_search` / `read_resource` on the specific proposal's
   subject thread — beware sibling threads for other transactions with near-identical
   reply text sent around the same time; match on subject line, not just sender/date).
2. Take the already-built proposal HTML (the one used for the proposal-only embed)
   and extract its `<body>` inner content — this becomes the "quoted" portion.
3. Prepend a new top section: a header table for the reply (From: client's address,
   Sent: reply's actual local sent time, To/Cc, Subject) in the same styled-table
   format as the proposal's own header, then the client's own message body verbatim
   (e.g. "Hi All, As per our meeting today, [date], kindly proceed with the
   attached. Regards, [Client Name]"), then a plain divider line ("On [day, date] at
   [time], [forwarder] wrote:") before the quoted proposal content — indenting the
   quoted portion with a left border (e.g. `border-left:3px solid #cccccc;
   padding-left:16px`) makes the reply-vs-quote structure visually clear, matching
   how a real email client renders a reply-in-thread.
4. Convert `sentDateTime` (UTC) to local time (SAST = UTC+2) for the reply's own
   "Sent:" line, same as point 3 further below for the proposal's header.
5. Feed this composite HTML into the wkhtmltopdf/pdftoppm pipeline below exactly as
   you would the proposal alone — same page geometry, same font-size rewrite
   (point 2 below — rewrite every `font-size` value in the *composite* file, reply
   header included, not just the quoted portion) and no `--zoom`. The result is one
   continuous document: reply header → reply body → quoted original proposal (with
   its own header) → proposal's own closing/signature — which is what actually
   gets embedded as images, not the proposal in isolation.

**Recurring bug to check first, every time:** `scripts/embed_email_images.py`'s
`main()` has repeatedly regressed to a hardcoded, client-specific work directory left
over from whichever client it was last edited for. This breaks the next client's
build if their session reuses stale files from that path. The correct, permanent form
is:
```python
src_docx = os.path.abspath(sys.argv[1])
images_dir = os.path.abspath(sys.argv[2])
out_docx = os.path.abspath(sys.argv[3])
import tempfile
work = tempfile.mkdtemp(prefix='embed_work_')
```
All three path arguments must be resolved to absolute paths on entry, and `work`
must always come from `tempfile.mkdtemp()` — never a literal path. Full history:
`wr-roa-builder-changelog.md` (2026-08-08 entry).

1. **Render the source HTML to PDF with `wkhtmltopdf`, never LibreOffice/`soffice`.**
   Converting an embedded-proposal HTML file via `soffice --headless --convert-to pdf`
   silently bakes in visible thin lines under nearly every line of text (a
   proofing/spell-check artifact of LibreOffice's headless HTML import) — this is
   invisible until you actually rasterize and look at the page, so always visually
   check at least one embedded page before delivering. `wkhtmltopdf input.html
   output.pdf` renders the identical HTML cleanly with no such artifact and should be
   the default tool for this step. Then `pdftoppm -jpeg -r 150` the resulting PDF as
   usual.
2. **Font size of the embedded email must match the ROA's own body text (11pt
   Aptos), not the source HTML's nominal size.** The embedded image is always
   displayed at a fixed width of 5,000,000 EMU (≈5.468in) regardless of the source
   page's pixel dimensions, so if the source HTML is rendered at a normal document
   width, the text shrinks noticeably once placed at that fixed display width.
   Compensate by rendering the source HTML at a **known, explicit** page geometry and
   a **larger** base font-size, calculated as:
   ```
   scale = (5,000,000 / 914,400) / content_width_in   # display width ÷ source content width
   source_font_pt = 11 / scale
   ```
   With `wkhtmltopdf --page-width 8.5in --page-height 11in --margin-left 0.5in
   --margin-right 0.5in --margin-top 0.5in --margin-bottom 0.5in` (content width
   7.5in), this works out to **15pt** as the source HTML's base `font-size` — use
   this figure unless the page geometry is deliberately changed, in which case
   recompute from the formula rather than reusing 15pt blindly. Always pass the
   margin/page-width flags explicitly rather than relying on `wkhtmltopdf` defaults,
   so the scale factor is actually known and reproducible rather than assumed.

   **Do not substitute `wkhtmltopdf --zoom` for this.** Applying a zoom factor on top
   of the proposal HTML's own as-authored font sizes (which are chosen for on-screen
   email reading, not for this formula) produces a displayed size close to but not
   exactly matching the target — it's an approximation layered on an assumption
   rather than the calculation itself. **The only correct method is to rewrite every
   `font-size` value in the source HTML directly**, scaled so that whatever the
   *dominant/normal body text* size is in that HTML maps exactly to `source_font_pt`
   (15pt at the standard geometry above) — e.g. if the proposal HTML's normal
   paragraphs are authored at 12pt, multiply every font-size value in the file by
   `15/12`, preserving the original relative hierarchy (headers, fine print,
   disclaimers all scale by the same factor). Do this with a script (regex over every
   `font-size:Npt` occurrence), not by eyeballing one or two values. Leave `--zoom`
   unset (or `1`) when rendering — zoom scales spacing, borders and images too, which
   is not what this correction is about. Always visually compare a rendered embedded
   page against a rendered native ROA page at the same DPI before delivering, to
   confirm the two actually look the same size side by side. Full history:
   `wr-roa-builder-changelog.md` (2026-08-25 and 2026-08-27 entries).
3. **The reproduced email must open with a proper header block for the actual
   message being embedded — From/Sent/To/Cc/Subject — showing the real sent
   date and time, not just the quoted messages beneath it.** Quoted sub-messages
   further down the thread naturally carry their own "From/Sent/To/Subject" lines
   (Outlook writes these into the quoted body text) — but the top/most-recent
   message's own metadata lives in the mailbox item's fields (`sentDateTime`, sender,
   recipients), not in its body text, so it has to be added explicitly. Convert
   `sentDateTime` (UTC) to local time (SAST = UTC+2) before writing it in, and format
   it the same way Outlook would (e.g. "Wednesday, 12 August 2026 10:46"). Build this
   as its own header block ahead of the message body, styled consistently with the
   quoted headers below it.
4. **Use generous paragraph and section spacing that matches the original email's
   visual rhythm — do not compress it to save space or render time.** Simplifying
   markup for reliable rendering is fine and encouraged; compressing spacing along
   the way is not — keep generous margins (e.g. `line-height: 1.35`, ~14px/section
   paragraph margins, extra top margin before bold section headings) so the
   embedded proposal reads with the same breathing room as the real email did.
5. `pdftoppm -jpeg -r 150` the Email Proposal PDF into one JPEG per page.
6. Copy each JPEG into `word/media/`, add an `image` relationship for each in
   `word/_rels/document.xml.rels`, and make sure `[Content_Types].xml` has a
   `Default Extension="jpg" ContentType="image/jpeg"` entry (add it if missing).
7. Build one standalone paragraph per image: an inline `w:drawing` with a
   `pic:spPr/a:ln` picture border (not a table border), width capped at 5,000,000
   EMU, height computed from the source image's own aspect ratio. Follow it with a
   small italic caption paragraph ("page X of Y").
8. **Put `<w:keepNext/><w:keepLines/>` on the *picture* paragraph's `pPr`** (before
   `spacing`, per the standard element order in `PPR_ORDER`). Without this, when an
   image doesn't leave quite enough room on the current page for its caption, Word/
   LibreOffice orphans the caption alone onto the next page while the image stays
   behind — the caption ends up separated from its image by a page break. With
   `keepNext` on the image paragraph, the pair is forced onto the same page as a
   unit. Verify this by checking that every "page X of Y" caption in the rendered
   PDF lands at the same relative page position (i.e. consistently near the bottom,
   right after a full-page image) — if any caption turns up near the *top* of a
   page, the image before it got orphaned and this fix is missing.
8a. **Do not insert blank spacer `<w:p>` paragraphs between an image paragraph and its
   caption, or between successive image/caption pairs.** Each embedded image already
   fills a full page at the fixed display width, so an extra spacer paragraph forces an
   additional blank page rather than adding breathing room — let `keepNext`/
   `keepLines` (point 8 above) and the paragraphs' own spacing do that job instead.
9. Insert the paragraphs as siblings in `word/body`, positioned right after the
   active bundle section's reason table and before the next heading (e.g. before
   "POLICY REPLACEMENT" for an Investment bundle, or before "Investment Planning"
   for a Retirement bundle — see the CLI 4th-argument note below) —
   **never inside the reason table cell itself**.
   `insert_before.addprevious(el)` inserts elements in the order called, so iterate
   the paragraphs in their intended final order (image1, caption1, image2,
   caption2, ...) — do **not** reverse the list first, or the pages render in reverse
   order (Y, Y-1, ..., 1).
10. Rezip and re-validate/re-render exactly as with the main build. Confirm the page
    count increased by roughly one page per embedded image and that no caption is
    orphaned per the check in step 8.

**Recurring bug — insertion heading for Retirement bundles:** the script inserts
images right before a target heading, read from an optional 4th CLI argument
(`sys.argv[4]`), defaulting to `'POLICY REPLACEMENT'`. That default is only
correct for Investment bundles (Investment is the last active section before
Policy Replacement). **Retirement bundles must always pass `"Investment Planning"`
as the 4th argument** — otherwise the images land after the (inactive) Investment
section instead of directly after Retirement's own table. Verify this argv[4]
handling is still present before every Retirement build — full history:
`wr-roa-builder-changelog.md` (2026-08-10 entry).

## Step 5 — ROA Reference No.

### Risk bundle
Format: `[Insurer] [type of cover: Personal, type of Business assurance] Cover - R
[premium amount] p.m.`

Example: `Old Mutual Personal Cover - R1,555.10 p.m.`

The premium is the "Total premium" printed inside the accepted quote document (Step 0b).

### Retirement / Investment bundles
These are never "Personal"/"Business" cover — do not use the Risk format above.
Format: `[Product Provider] [Product Name] - R [amount][ - Lump Sum | p.m.]`,
using the answers to Step 1 questions 5a (product provider/name) and 5b (lump sum vs.
recurring):
- Lump sum: `Old Mutual Retirement Annuity Xtra Max - R 158,192.00 - Lump Sum`
- Recurring/monthly: `Old Mutual Retirement Annuity Xtra Max - R 1,500.00 p.m.`

**Standing shortcut — Old Mutual Tax-Free Investment products:** when the client's
proposal is an Old Mutual Tax-Free Investment Plan (an Investment-bundle product),
don't ask 5a/5b as open questions — these are fixed:
- Product Provider: `Old Mutual`
- Product Name: `Tax-Free Investment Plan` (so the combined reference reads "Old
  Mutual Tax-Free Investment Plan - R [amount] p.m.")
- Recommendation for Identified Need dropdown: `Old Mutual - Max Investment` — the
  master product list (`references/dropdown_field_map.md`) has no separate
  "Tax-Free" entry for Old Mutual; "Max Investment" is the correct match since it's
  the underlying platform the client's quote/fact sheet documents reference.
- Still ask 5b's underlying question (lump sum vs. recurring) directly, since a
  Tax-Free product could in principle be funded either way, but in practice these
  are almost always monthly/recurring contributions.

## Delivery filename — every finished ROA must be named this way

### Risk bundle
Format: `ROA - [Insurer] [Personal/Business] Cover - R [premium] p.m. - [DD.MM.YY] -
([Client Full Name])`

Example: `ROA - BR Personal Cover - R 4097.96 p.m. - 26.05.26 - (Client Full Name)`

Rules (distinct from the in-document ROA Reference No. formatting above — don't
confuse the two):
- Insurer is title case (Old Mutual, Discovery, Sanlam, Liberty, Momentum, Altrisk,
  Capital Legacy, Stanlib) — **except BrightRock, which is always shortened to "BR"**
  in the filename specifically.
- Premium has no thousands comma, 2 decimals, a space after "R" — e.g.
  `R 91555.10 p.m.`, not `R 91,555.10 p.m.`
- Date is always the ROA date (never today's date or the print date), formatted
  DD.MM.YY.
- Client name is the full name, in parentheses, at the end.

Use `build_filename()` in `scripts/build_roa.py` to generate this automatically
rather than constructing it by hand — call it with the same insurer/premium/date/
client values used to build the document, then use that string (plus `.docx`) as the
actual delivered filename.

### Retirement / Investment bundles
`build_filename()` hardcodes " p.m." and a Personal/Business cover scope, neither of
which applies here — build the filename by hand instead:
Format: `ROA - [Product Provider] [Product Name] - R [amount][ - Lump Sum | p.m.] -
[DD.MM.YY] - ([Client Full Name])`

Example (lump sum): `ROA - Old Mutual Retirement Annuity Xtra Max - R 158192.00 -
Lump Sum - 09.03.26 - (Client Full Name)`

Same numeric formatting rules as the Risk filename (no thousands comma, 2 decimals,
space after "R", date always DD.MM.YY from the ROA date).

## Step 6 — Fixed constants (never vary by client)

- Financial Planner: Paul Kafentzis
- FSP Number: 45946
- Next review/meeting date: always ROA date + 12 months (the build script computes
  this automatically — never source it from the quotes or ask separately).

## Step 7 — Mandatory pre-delivery audit

Before calling an ROA finished, check every item below. Do this by actually reading
the rendered PDF pages (via the visual-check step in `references/roa_data_schema.md`),
not just by re-reading the data dict you built.

1. Only one bundle (Risk / Retirement / Investment) is actively completed; every
   other section shows only its heading and reason text — the data table is fully
   gone, not left showing "Choose an item."
2. Health Care does not appear anywhere in the document at all.
3. Income Protector Planning After 24 Months is "Do not Review" with the fixed
   sentence, even when Income Protection (1st 24 months) is active.
4. Every dropdown selection matches an option that genuinely exists in
   `references/dropdown_field_map.md` — no invented options, no selection of the "."
   insurer error-option, no "preserve"/"retirement" selected for Retirement's Need
   Identified. Lump Sum Disability and Income Protection (1st 24 months) Need Identified fields are filled (not blank).
5. Death shows "Life Cover" and Dread shows "Comprehensive Severe Illness" as Need
   Identified, regardless of what the source documents call them.
6. Replacement status was set independently per cover type within the Risk bundle,
   not copied uniformly across all four.
7. Every reason-textbox paragraph traces to either the response bank (risk bundle),
   the fixed rule sentences (declined need / BR after-24-months / new-cover-type wording in Step 4), or a pasted client
   proposal email (Retirement/Investment) — never free-written from scratch. Any
   declined cover type has its own specific, asked-for reason — never a generic
   placeholder.
8. Any cover type the client declined shows "Do not Review" with its data table
   removed, even though it's within the active bundle — declined is not the same as
   "outside the bundle," but gets the same document treatment.
9. The RAR reference number field does not appear anywhere in the document.
10. Every Recommended Amount / Taken Up Amount figure traces to the correct Summary
   block column in the correct uploaded quote (FNA Quote → Recommended; Reduced/Revised/
   Accepted Quote → Taken Up), and dual lump/monthly fields show one clean value, not
   both placeholders.
11. Client name appears correctly in both places, the ID confirmation line reads
   "I, [Name], (ID: 1234567890123), hereby confirm" with clean single commas, and the
   ID is 13 digits with no spaces or dashes.
12. Next meeting date = ROA date + 12 months exactly.
13. Author is Paul Kafentzis.
14. No "Choose an item.", "Click here to enter amount.", or other template
    placeholder text remains in any field that should have been completed for the
    active bundle.
15. The delivered file's name follows the required convention exactly — see
    "Delivery filename" above — not the in-document ROA Reference No. format, and
    not a generic/default filename.
16. For Retirement/Investment ROAs: the ROA Reference No. and filename use the
    Product Provider + Product Name format ending in "- Lump Sum" or "p.m." as
    appropriate — never the Risk bundle's "[Insurer] Personal/Business Cover" format.
17. For Retirement/Investment ROAs with an embedded proposal email: the reason
    textbox itself holds only the short pointer line, the actual email pages are
    standalone bordered image paragraphs after the data table (not inside any table
    cell), and no image's border bleeds into a page footer on the rendered PDF —
    check this visually, not just via validate.py. **Also confirm the embedded
    document is the client's own reply email (with the proposal quoted beneath it),
    not the proposal email alone** — the first embedded page must show a header
    block naming the client as sender and the client's own acceptance wording (e.g.
    "kindly proceed with the attached"), not the adviser's proposal header as the
    very first thing shown. This is non-negotiable — an embed that opens directly on
    the adviser's proposal, with the client's acceptance email nowhere in the
    document, is treated as an incomplete ROA and must be rebuilt.
18. For the **Retirement** section specifically: Need Identified, then Insurers
    Considered / Recommended Insurer / Recommendation for Identified Need, then
    Reason — in that order. The raw template has Retirement's Reason row before the
    insurer rows (unlike every other section); `build_roa.py` reorders this
    automatically, but confirm it visually since this is the one section where the
    template's native order is wrong and easy to regress if the script changes.
19. **Embedded email font size actually matches the surrounding ROA body text —
    verify this visually, side by side, not just by trusting the command used.**
    Render one native ROA page and one embedded-email page at the same DPI and
    compare directly. If the embedded text reads noticeably larger or smaller than
    the surrounding document at a glance, the font-size rewrite was skipped, done on
    the wrong baseline value, or `--zoom` was used — fix the HTML and rebuild rather
    than adjusting the display width or shrinking the image.

20. Any FNA-analyzed-but-not-accepted cover type (as opposed to an outright decline)
    still shows Status = IMPORTANT with its data table intact (Recommended Amount
    from the FNA, Taken Up Amount = 0) and the "FNA DONE / BENEFIT NOT ACCEPTED"
    response-bank paragraph — it has not been mistakenly treated as a decline.
21. No filled field renders in placeholder grey instead of black (a sign the
    `PlaceholderText` style reference wasn't stripped alongside the data binding).

If any check fails, fix it in the data dict and rebuild — don't hand-patch the output
.docx directly, or the fix won't carry forward to the next client.

## Delivery — pushing the finished file into the client's SharePoint folder

**Critical: tool availability is per-session, not guaranteed by this skill.** Whether
the local device bridge (`mcp__remote-devices__*` tools) is connected, whether
`Microsoft 365:sharepoint_upload_file` exposes a plain-text `content` parameter (in
addition to `contentBase64`), and whether the M365 connector is fully authorized in
this specific chat, can all differ from one session to the next — this is connector/
device/infrastructure state, not something a skill file controls. **Never assume
today's tool shape based on a description pasted from another chat, a prior
session's summary, or what worked last time.** Always check what's actually
available right now in this session before deciding which path below applies.

### Step A — Check what's actually available, every time, in this order
1. **Local device bridge first.** Call `mcp__remote-devices__get_device_info`. If it
   succeeds (even with `connectedFolders: []`), Paul's own computer is reachable from
   this session — go to **Path 0**, the preferred delivery method whenever it's
   available, since it writes a real uncorrupted `.docx` with no manual step. If the
   call errors or the tools aren't present in this session's tool list at all, no
   device is connected this session — skip to step 2.
2. Confirm `Microsoft 365:sharepoint_upload_file` is loaded and inspect its real
   parameters. If it has a **`content` (plain text) parameter**, go to Path 1. If it
   **only has `contentBase64`**, go to Path 2.
3. If any upload attempt (test or real) returns an auth/consent error like
   `"No approval received"` rather than a content/size problem, that is a **different
   issue** — a stuck or missing connector authorization — and no amount of format
   change (HTML, smaller file, etc.) will fix it. Tell the user plainly that the
   connector itself needs their attention (check for a pending approval prompt, or
   reconnect the M365 connector), rather than continuing to retry uploads.

### Path 0 — Local device bridge connected: write directly into the client's OneDrive-synced folder (preferred whenever available)

When this session can reach Paul's own computer, the finished `.docx` can be written
directly into the exact same folder the ROA was sourced from in SharePoint, via that
folder's local OneDrive-for-Business sync mirror — no base64, no HTML conversion, no
manual drag-and-drop, and it becomes the live SharePoint copy automatically the next
time OneDrive syncs. This sidesteps the entire binary-upload problem Path 1/Path 2
exist to work around, so prefer it over both whenever `get_device_info` succeeds.

1. **Find the OneDrive-for-Business sync root — discover it fresh, never hardcode
   it.** Call `get_device_info` and read `homeDirectories`: look for a folder named
   after the firm's tenant domain (`liferisk.co.za`, the local mirror of the whole
   `liferisk.sharepoint.com` tenant Paul's documents live on — the same tenant
   `Microsoft 365:sharepoint_search` results point to). This name is discovered
   per-session/per-machine from `homeDirectories`, never assumed from a previous
   build.
2. **Request access to that tenant-root folder, not a client subfolder, and only
   once per session.** Use `device_request_folder_access` with one clear, specific
   reason (e.g. "to save [Client]'s ROA into their SharePoint client folder, synced
   locally"). This spends one of Paul's confirmation-dialog interactions — asking for
   the narrow client folder means asking again for every future client, so always
   request the tenant root itself. **Check `get_device_info.connectedFolders` first**
   — if it already covers this root (granted earlier in the session), do not
   re-request; access persists for the rest of the session once granted.
3. **Identify the SharePoint library folder underneath the tenant root.** Each
   SharePoint document library appears locally as `Company - [Library]` (e.g.
   `Company - Paul` is the local mirror of the `Paul` library at
   `https://liferisk.sharepoint.com/Paul/...`). Use `device_list_dir` on the tenant
   root to confirm the exact folder name before assuming it matches the SharePoint
   URL segment verbatim — don't guess this across different machines/tenants.
4. **Everything after the library segment in the SharePoint URL maps directly to the
   local path, folder-for-folder.** E.g. SharePoint's `Paul/New Business/[Surname,
   First Name]/[Surname, First Name] (Product - Amount)/ROA & Bus ROA` is locally
   `Company - Paul\New Business\[Surname, First Name]\[Surname, First Name] (Product
   - Amount)\ROA & Bus ROA`. Walk this with `device_list_dir` one level at a time to
   find the client's specific transaction subfolder and confirm each name exactly
   (commas, parentheses, and premium amounts in folder names must match precisely) —
   never construct the full path blind from memory of the SharePoint URL alone.
5. **List the destination `ROA & Bus ROA` folder before writing.** Check whether a
   file with the exact delivery filename (see "Delivery filename" above) already
   exists there — e.g. an earlier draft rebuilt during the same session, or a stale
   file left by a previous adviser. If one exists, confirm with Paul whether to
   overwrite before passing `force: true` to `device_commit_files`; never force
   silently over an existing file in a client's compliance folder.
6. **Deliver in exactly two calls, in this order:** first `SendUserFile` on the
   locally-built `.docx` (this returns a `file_uuid`), then
   `mcp__remote-devices__device_commit_files` with that `file_uuid` and the full
   `devicePath` built from steps 3–4, using the **exact required delivery filename**
   as the final path component — never a generic name like `output.docx` or
   `output_final.docx`. `device_commit_files` only accepts a `file_uuid` from a prior
   `SendUserFile` call in this same session; it cannot take a raw container path.
7. **Confirm success from the tool's actual result, not just the absence of a thrown
   error.** Check that the `written` array contains the expected full path and that
   `rejected` is empty. A rejection includes the device file's current
   `mtimeMs`/size — use that to tell a genuine conflict (a newer file already there)
   from a plain permissions problem before deciding how to proceed.
8. **Tell Paul plainly what happened and exactly where, using the right verb.** Say
   the file was **saved to his computer** in `[folder]`, and that it will sync back
   to SharePoint on its own — do not say "uploaded to SharePoint," since what
   actually happened is a local write via OneDrive sync, a different mechanism from
   Path 1's direct SharePoint API upload, even though the destination is the same
   file in the same place once sync completes.

Once the tenant root is granted, steps 1–3 don't repeat for later clients in the same
session — only steps 4–8 (locate the specific client subfolder, check for a
collision, deliver, confirm, report) repeat per ROA. If the client's document library
isn't synced locally on Paul's machine (its folder doesn't appear under the tenant
root when listed), fall back to Path 1 or Path 2 below for that specific client.

### Path 1 — `content` (text) parameter is available: build the ROA as HTML
Because a `content` text field takes literal text with no size-driven encoding
overhead, an HTML-built ROA can be pasted directly into it and pushed straight into
SharePoint — no manual drag-and-drop needed. This sidesteps the whole binary/base64
problem rather than working around it.
1. Build the ROA's compliance content as clean HTML instead of a .docx — pull the
   exact required wording (paragraph text, field labels, s9(1)(c)/(2) disclosure
   language) from `assets/ROA_Template_2026.docx` via `python-docx` first, so the
   HTML uses identical legal wording rather than paraphrasing it.
2. For the active bundle's Reason section, embed the client-accepted proposal as
   **real HTML markup** (pulled from wherever it already exists as HTML — e.g. an
   OM Optimal RA proposal email, which is itself built as HTML) directly into the
   ROA's body — not a screenshot, not an image.
3. Run the same Step 7 audit (placeholder check, cross-referenced figures) against
   the HTML output.
4. Upload directly via `sharepoint_upload_file`'s `content` parameter to the client's
   `ROA & Bus ROA` folder item ID.
5. Also save a local copy to `/mnt/user-data/outputs/` and share it via
   `present_files`, so the user has an in-chat copy to review even though it's
   already live in SharePoint.

### Path 2 — Only `contentBase64` is available: fall back to manual delivery
This is the older/more limited case. **Do not attempt to force a docx or HTML file
through `contentBase64` by typing it out as base64** — for anything beyond a trivial
size this fails structurally, not just for large files (full history:
`wr-roa-builder-changelog.md`, 2026-08-14 entry).
1. Build and audit the ROA as normal (.docx, per the standard pipeline above), save
   it to `/mnt/user-data/outputs/` with the required delivery filename, and share it
   via `present_files`.
2. Tell the user plainly that this session's upload tool can't carry the file, and
   give them the exact destination folder so they can drag it in themselves.
3. A small plain-text test file (e.g. a one-line `_permission_test.txt`, deleted
   immediately after) is fine for confirming write *permissions* are granted — that's
   a different question from whether the transfer mechanism can carry a real
   document, and in this path, it can't, at any size.

## Reference material

- `references/dropdown_field_map.md` — full verified dropdown option lists for every
  field in the template, including the 81-item master product list. Read before
  filling any dropdown.
- `references/roa_data_schema.md` — the exact data shape `scripts/build_roa.py`
  expects, plus the validate/render commands to run before delivering. Read before
  building any ROA.
- `references/WR_Risk_Cover_Responses_24_07_26.docx` — the response bank for the risk
  bundle's reason-text paragraphs (Life, Disability, Dread, Income Protection — each
  with their own FNA-status × Replacement-status scenario list).
- `scripts/build_roa.py` — the validated construction script. Encodes the table
  removal, Health Care deletion, Death/Dread overrides, amount-field collapsing,
  and date rules described above. Extend this script (and update this file) rather
  than hand-editing XML for a one-off case.
- `scripts/embed_email_images.py` — second-pass script for Retirement/Investment
  ROAs: converts the accepted proposal email PDF to images and embeds them as
  standalone, bordered, keepNext-linked picture+caption pairs after the active
  section's reason table. Run this after `build_roa.py`, not instead of it.
- `assets/ROA_Template_2026.docx` — the base ROA template. Never build an ROA from
  scratch; always start from this file.
- `wr-roa-builder-changelog.md` (in the Analyze Skills Project) — the full,
  verbatim caught-mistake history behind every "recurring bug" and "non-negotiable"
  rule above. Add any new caught-mistake story there, not back into this file.

## A note on scope

This skill is about the *procedure*. It doesn't carry any specific client's data —
each ROA should start from that client's own documents (FNA Quote, Reduced/Accepted
Quote, Fact Find), located via Step 0 (local machine first, then SharePoint/Outlook) or, failing that,
uploaded directly into the conversation. If a new client's documents can't be found
either way, ask for them via the Step 1 checklist rather than reusing figures or
wording from an earlier client in the same chat or from memory of a previous
session.