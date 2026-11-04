<!-- The live skill text as of 14/10/2026 (last updated line: 2026-10-14 14:15), kept as the rule-by-rule baseline: SKILL.md only (the skill has no other file). No client data found, nothing replaced. -->

---
name: "client-review-notes"
description: "Formats raw Outlook contact notes into a standard Client Record for Paul Kafentzis (FSP45946), delivered as a .md file. Use for 'format a client record', 'compile client review notes', or merging duplicate records."
---

## Index

| # | Section | What it covers |
|---|---|---|
| 1 | Universal operating rules + Delivery gate | The nine rules for every step, and what must be done before a record counts as delivered |
| 2 | Last updated + Changelog | Athens-time stamp, last 5 changes, standing edit note |
| 3 | Working with Paul | Clean redos, direct corrections, no permission step |
| 4 | Header format | Name line with category and ID |
| 5 | Field order | The 18 fields, always in this sequence |
| 6 | Formatting rules | Layout, missing fields, Life & Investments, Notes (summarise, don't transcribe), Commission |
| 7 | Delivery format | Always a downloadable .md file |
| 8 | Duplicate checking | Flag first, then merge |
| 9 | Data integrity rules | Verbatim fields, flag typos, context is a fact |
| 10 | Reference: domain terminology | Abbreviations to recognise |
| 11 | Reference: key contacts | Names, roles, broker code, systems |
| 12 | Example | Layout example with placeholders |
| 13 | Final checklist before outputting any record | Tick-list to run before delivery |

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

**Delivery gate for this skill (rules 5 and 6 applied):** a run is complete only when ALL of these are done and confirmed in one line each: (1) all the raw notes supplied were read in full and the record built to the Header format, Field order and Data integrity rules; (2) the "Final checklist before outputting any record" was run; (3) the record was delivered as a downloadable .md file in the chat (the Delivery format rule). After ANY correction, repeat (1) to (3) and re-deliver the corrected record file.

**Last updated: 2026-10-14 14:15 (Athens time)**

## Changelog

(last 5, one line each; full history with backstory is in the Project as `client-review-notes-changelog.md`)

| When (Athens time) | What changed |
|---|---|
| 2026-10-14 14:15 | Index added; description made plain; long changelog moved word for word to the archive; client names, contract numbers and amounts in the examples replaced with placeholders. No rule changed. |
| 2026-10-08 | Rule 9 reworded: skill changes go forward with the propose_skills review card; never claim live until Paul confirms he saved. |
| 2026-10-08 | Universal operating rules block and Delivery gate added at the top of the skill. |
| 2026-09-25 | Added Working with Paul, domain terminology, key contacts, broker code and system names (previously only in project memory). |
| 2026-09-18 | Multi-part client requests (which product to withdraw from, etc.) must be captured with full context; added Data Integrity rule "Context is a fact, not filler" and a checklist item. |

> **Standing rule:** whenever this SKILL.md is edited, add a one-line row at the top of the table above (Athens time), keep the table to 5 rows (drop the oldest), and update "Last updated" in the same edit. Put any edit with real backstory (a live mistake, a ruled-out approach) in `client-review-notes-changelog.md` instead of growing this file.

---

# Client Review Notes — Wealth Revolution (FSP45946)

Format raw Outlook contact notes into a standardised, consistently structured client record for Paul Kafentzis. Every record must follow the same structure, regardless of how much or how little information is provided in the source.

**Core principle: this is reformatting with summarisation of narrative notes — not a lossy summary.** The Notes section must be condensed into concise, scannable bullets rather than reproduced word-for-word, but every material detail (facts, figures, dates, names, decisions, outstanding items, instructions) must still appear. Cut redundant wording, filler, and repetition — never cut information. Structured data fields (contract numbers, DOC dates, ID numbers, commission amounts, policy statuses) remain **verbatim** — these are audit-sensitive figures, not narrative, and must never be paraphrased or rounded. Typos or inconsistencies found in those verbatim data fields are preserved and flagged with ⚠️, never silently corrected.

## Working with Paul

- **Clean redos over patches.** When Paul supplies substantial new source material for a client that already has a formatted record, produce a full redo of the record incorporating the new material — don't just patch or append the delta onto the existing output.
- **Corrections are direct.** When Paul points out an error or supplies a correction, redeliver the corrected record itself. Don't preface it with an explanation of what changed unless he asks — he expects the fixed deliverable, not a description of the fix.
- **No permission needed.** In the Summarized Client Review notes project, Claude formats the record as soon as raw notes or a client record are supplied — no confirmation step before producing output.

## Header format

Begin the record with the client's full display name, category, and ID in parentheses:

`Firstname Lastname (Client) (ID number)`

If the client has a known/preferred name, insert it in parentheses after the first name:

`Firstname (Knownname) Lastname (Client) (ID number)`

## Field order (always use this exact sequence)

1. Full Name
2. Last Name
3. First Name
4. Known As
5. Categories
6. First meeting
7. First policy signed
8. Portfolio Review Month
9. Got details from
10. Client ID No
11. Income Tax Number
12. Adviser Allocation
13. Medical Aid
14. Short Term Insurance
15. Family Information
16. Life & Investments (subdivided: Previous/Replaced Policies | Current/Active Policies | Non-active/Lapsed Policies)
17. Notes
18. Commission

## Formatting rules

**General layout**
- Bold every field label. Put the value on the line directly below the label — never inline on the same line as the label.
- Insert a horizontal rule `---` on its own line between every top-level section.
- Insert a blank line between every field label+value pair and between each list block.
- Never let two sections run together with no visual gap.
- No closing sign-off line at the end of the record.

**Missing or unrecorded fields**
- If a field is absent from the source notes, write: `Not recorded.`
- If notes appear lost or clearly incomplete, flag with ⚠️.
- Never invent, infer, or fill in information not explicitly stated in the source.

**Known As**
- Only populate if the source explicitly references a nickname or preferred name. Otherwise `Not recorded.`

**Categories**
- Reproduce exactly as stated in the source (e.g. `Client`, `Client / BrightRock Lead`, `Client / Non-Replacement`).

**Medical Aid / Short Term Insurance**
- If source says "not brokers yet" with a blank contract, reproduce as: `Contract: Not recorded / not brokers yet.`
- If there is substantive detail (insurer, premium, coverage notes), reproduce in full.

**Family Information**
- List each family member as a bullet point: name, relationship, and any additional detail given (ID numbers, "also a client", contact numbers).
- If a dependant has linked policy details, include those under that family member's entry.

**Life & Investments**
- Always use these three sub-headings, in this order:
  - *Previous/Replaced Policies:*
  - *Current/Active Policies:*
  - *Non-active/Lapsed Policies:*
- Each policy entry on its own bullet line, in this format:
  `- Contract: [number] ([Product / Insurer]) DOC [date] / [premium if stated] / [status notes in CAPS if present]`
- Reproduce contract numbers, DOC dates, premiums, and status notes verbatim — do not reformat or clean up.
- Preserve apparent typos or inconsistencies and flag with ⚠️ rather than silently correcting.
- If a sub-section has no entries: `- Not recorded.`

**Notes**
- Organise in chronological order.
- Each date heading in **BOLD ALL CAPS** (e.g. **MARCH 2024**, **14 FEBRUARY 2022**).
- Separate each date block with a `---` horizontal rule above it.
- **Summarise, don't transcribe.** Under each date heading, condense the raw note into short, tight bullet points — strip filler, throat-clearing, and repeated wording — while retaining every fact: who, what, which policy/contract number, amounts, dates, decisions made, and next steps. A reader should be able to reconstruct the full picture from the summary alone, just not the original sentence-by-sentence phrasing.
- **CRITICAL: Multi-part requests and advisor decision-points.** When a client asks "which X should I do Y from" or requests guidance on choosing between options, ALWAYS capture:
  - What the client is asking for (e.g. "R70k withdrawal")
  - Which products/accounts are available (list by contract number and product type)
  - Which product(s) or option(s) the advisor recommended or is considering
  - Any supporting rationale (tax implications, fund values, withdrawal rules)
  - What the client decided or what decision is pending
  - Example (DO capture): "Client asked which OM products (RA (contract no.), Tax-Free (contract no.), Funeral (contract no.)) to withdraw R70k from. Paul advised on options; client deciding which to use." NOT just "Client asked about OM withdrawal" (loses critical detail about which products are in scope).
- Sub-lists (e.g. FNA breakdown, medical requirements, shareholding details) stay as indented bullets but should also be tightened — combine related line items where it doesn't lose information.
- Quoted text from emails/messages: only quote verbatim when the exact wording is materially important (e.g. an explicit instruction, a commitment, a "do not contact" request, or language that could matter for compliance/dispute purposes). Otherwise, summarise the substance of the email/message instead of quoting it in full. When quoting, keep the quote short and still include the timestamp.
- MS Planner links: render as `[Planner – Task Name](URL)` with anchor text matching the Planner task name exactly — links themselves are never summarised.
- "Do not contact" instructions: always reproduce in full verbatim (never summarised) AND add a ⚠️ flag at the top of the Notes section.
- Timestamps that look system-generated rather than actual event dates: flag with a ⚠️ note explaining the discrepancy.
- Month/year headings: **BOLD ALL CAPS** only — no underline tags, no HTML, no `<u>` symbols.
- Do not omit an event, figure, or outstanding item to save space — if the summary is getting long because the source has a lot of distinct events, that's expected; length should track the number of distinct facts, not be capped artificially.

**Commission**
- Reproduce verbatim — no paraphrasing, no reformatting of amounts.
- Format: `Insurer – Product Description (Month 'YY)` followed by bullet lines for each commission type.
- If no commission is recorded: `- Not recorded.`

## Delivery format — MANDATORY

Every formatted client record must be delivered as a downloadable `.md` file — never as chat-only text, even if the record is short. Chat text is a preview at most; the file is the deliverable.

## Duplicate checking

Before formatting any record, check whether a client with the same name or ID number has already been formatted in the current session.
- If a potential duplicate is identified, flag it explicitly before proceeding.
- If confirmed as a duplicate, produce a single merged record combining all unique information from both versions, noting which version contributed which additional details.
- Never silently merge without flagging first.

## Data integrity rules

- Contract numbers, DOC dates, policy details, ID numbers, and commission entries must be reproduced verbatim.
- Preserve and flag (⚠️) apparent typos or inconsistencies rather than silently correcting them.
- If a contract number in the source header looks like a policy number rather than a client ID, flag the discrepancy.
- Flag scientific notation or truncated ID numbers as potentially imprecise — do not present them as exact.
- **Context is a fact, not filler.** When a client requests guidance on choosing between options ("which product should I use?"), the available options themselves (by contract number and product type) are data-integrity items. Omitting them ("client requested withdrawal") loses critical information that may drive subsequent advice or compliance decisions. Capture the scope: which products are in play, what the advisor is considering, what decision is pending.
- "Do not call" / "Do not contact" instructions: always reproduce prominently with a ⚠️ flag at the top of the Notes section.

## Reference: domain terminology

Recognise these abbreviations when they appear in source notes — reproduce them as given, don't expand or reinterpret them:

- **FNA** — Financial Needs Analysis
- **FF** — Fact Find
- **RGAR** — Retirement Goal Analysis Report
- **NTU** — Not Taken Up (a proposed policy that never went into force)
- **DOC** — Date of Commencement (of a policy)
- **ACI** — Annual Contribution Increase
- **ECBU** — Extended Cover Benefit Upgrade (BrightRock)
- **ICB** — Income Continuation Benefit
- **COC** — Certificate of Compliance
- **DRO** — Debt Review Order
- **Section 14 transfer** — statutory transfer of retirement fund benefits between funds
- **Broker of record** — the adviser/brokerage formally appointed on a policy with the insurer
- **Paid-up policy** — a policy where premiums have stopped but reduced cover continues
- **Msign** — the practice's e-signature platform
- **PMA report** — a policy/portfolio management/analysis report
- **GPMR** — a further portfolio/management report type used in reviews
- **LOA** — Letter of Authority
- **IRR/ROR** — Internal Rate of Return / Rate of Return
- **BSC Personalised** — a BrightRock personalised cover product/report
- **GCS monthly run** — a recurring monthly commission/compliance run

## Reference: key contacts

Recognise these names when they appear by first name or role only in source notes, and preserve their role context in the summary:

- **Sitamah Nathoo** — Paul's personal assistant; handles follow-up and admin coordination
- **SR** — support/service representative (internal shorthand)
- **Alwyn Van Tonder** — Old Mutual BC (external)
- **Martin Oelofse** — BrightRock (external)
- **Lizelle Cachado** — BrightRock underwriting (external)
- **Cameron Maritz** — Vision Insure, short-term insurance referrals (external)
- **Amber Strydom / Bianca Swart** — Capital Legacy (external)
- **Valerie Swanepoel / Laura-May Strydom** — medical aid administration at Hampshire (external)

Paul's own broker code is **721077**. The practice records/tracks across AdviceTech (CRM), Astute, Msign, Microsoft Planner (task tracking, embed Planner links in Notes entries per the rule above), and MyClient — recognise references to these systems in source notes as platform names, not client-specific detail.

## Example

**Full Name:**
(Client Full Name)

---

**Last Name:**
(Last Name)

---

**First Name:**
(First Name)

---

**Known As:**
Not recorded

---

**Categories:**
Client / BrightRock Lead

---

*(...continue through all 18 fields in order...)*

---

**Notes:**

---

**FEBRUARY 2024**

- Paul took over as broker on BrightRock (contract no.), Sanlam Risk Cover, and Sanlam RA — broker change effective 19/02/2024. LOAs signed and sent for both.
- ⚠️ Outstanding: Feb 2024 approved request to add (family member) to the BrightRock policy was never actioned — BrightRock's records show zero servicing history on the policy.

---

**MARCH 2025**

- Old Mutual AML/compliance reminder ((reference no.)) — (Client) completed the required form to keep the portfolio active.

*(Note how each bullet is condensed to one line but still carries the contract number, effective date, and outstanding-item flag — nothing from the original is lost, it's just phrased tightly.)*

---

**Commission:**

BrightRock – Personal Covers (March '20)
- 1st year comm: R(amount)
- 2nd year comm: R(amount)

Old Mutual – Pension Preservation (March 2019)
- 1st year comm: R(amount)

## Final checklist before outputting any record

- [ ] All 18 fields present, in correct order
- [ ] Every field label bolded, value on the line below
- [ ] Horizontal rules between all sections
- [ ] All three Life & Investments sub-sections present
- [ ] Notes in chronological order with BOLD ALL CAPS date headings, condensed into concise bullets — with zero facts/figures/decisions dropped
- [ ] Multi-part client requests captured with full context: what is being asked, which products/accounts are in scope (by contract number), what options the advisor is considering, and what decision is pending — DO NOT omit "which X to do Y from" details
- [ ] Commission reproduced verbatim
- [ ] No invented or inferred information
- [ ] Missing fields stated as "Not recorded."
- [ ] Duplicate check performed
- [ ] ⚠️ flags applied where appropriate
- [ ] No closing sign-off line
- [ ] If this is a redo of an existing client record with new source material, it's a full redo — not a patch