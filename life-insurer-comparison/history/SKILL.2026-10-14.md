---
name: "life-insurer-comparison"
description: "Builds a client-facing HTML comparison of two or more insurers' life/risk policies (e.g. BrightRock vs Discovery) plus a covering email, for Paul (FSP45946). Use when asked to compare existing cover with a proposal."
---

# Life Insurer Comparison Builder

## Index

| # | Section | What it covers |
|---|---|---|
| 1 | Universal operating rules + Delivery gate | The nine rules for every step, and what must be done before a run counts as complete |
| 2 | Last updated + Changelog | Athens-time stamp, last changes, standing edit note |
| 3 | Scope | Any number of insurers; no client data held in the skill |
| 4 | Step 0 / 0a / 0b | Opening conversation; section checklist and document voice; client's actual benefit scope (mandatory gate) |
| 5 | Step 1 | Locate and retrieve source documents from OneDrive automatically |
| 6 | Step 2 | Product knowledge research and known traps (fixed vs age-rated, ACI/ABI) |
| 7 | Step 3 | Verify key facts from source documents |
| 8 | Step 4 | Premium pattern and the year-on-year percentage rule |
| 9 | Step 5 | Accuracy rules, escalation-percentage verification, OCR discipline |
| 10 | Step 6 | Loyalty / payback / bonus table (one minimal table) |
| 11 | Step 7 / 8 / 9 | Unique features; definitions and claim quality; spouse / second life |
| 12 | Step 10 | Document format, visual design (CSS palette), structure of the letter |
| 13 | Step 11 | What not to do |
| 14 | Step 12 | Pre-delivery checks (with grep commands) |
| 15 | Companion email | The covering email from Paul |

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

**Delivery gate for this skill (rules 5 and 6 applied):** a run is complete only when ALL of these are done and confirmed in one line each: (1) the source documents were retrieved and the key facts verified (Steps 1-3); (2) the comparison document was built to the Step 10 format; (3) every Step 12 pre-delivery check was run, including the benefit-scope check and the escalation-accuracy check; (4) the finished document was handed over to the user the way Step 10 specifies; (5) the companion email was drafted and shown in the chat. After ANY correction, repeat (2) to (5) for every deliverable that changed.

**Last updated: 2026-10-14 15:14 Athens time (EEST)**

> **Standing rule — not optional:** any edit to this skill is not complete until the
> "Last updated" line above is also rewritten to the current Athens/Greece date-time,
> in the same response as the edit, and a line is added to the Changelog below.

## Changelog

- **2026-10-14 (15:14)** — Index added; description made plain; the long changelog moved word for word to the Project doc; client names, amounts and dates in examples replaced with placeholders. No rule changed.
- **2026-10-08 (14:35)** — Rule 9 reworded: skill changes go forward with the propose_skills review card; never claim live until the user confirms they saved.
- **2026-10-08 (13:10)** — Universal operating rules block and Delivery gate added at the top.
- **2026-10-07 (19:15)** — Step 11 extended: never describe a newer quote against an earlier version of it; Step 12 gained a matching check.
- **2026-10-07 (18:20)** — Section 4 (Loyalty/Payback) cut to one minimal table; Step 5 point 4: confirmed figure plus at most one short clause; Definition Quality off by default.

Older entries (2026-10-07 17:40 back to the initial version of 2026-07-31) are in `life-insurer-comparison-changelog.md` in the Project, word for word.

## Scope

This skill applies to **any** comparison between **two or more** life/risk cover
policies, across **any** insurers — a straight two-way switch comparison, a
second opinion, or a client's whole existing spread of policies (any number,
across any number of insurers) weighed against one new proposal. Follow it in
full for every comparison, regardless of how many insurers or policies are
involved. It is deliberately insurer-agnostic: no insurer's product facts are
ever hardcoded here — they are researched and verified fresh, every time, for
whichever insurers are actually being compared.

This skill carries no client data. Every comparison starts fresh from that
client's own documents, retrieved and verified using the steps below — never
reused or inferred from a prior client's numbers or a previous session's
memory.

**Working with Paul:** he corrects errors directly and expects the fix
applied immediately — don't re-argue the point or re-explain the reasoning
back to him first.

## Step 0 — Opening conversation

Start every new comparison with a short, natural conversation, not a form. Ask,
in this order:

1. **What's this comparison about, and which insurers/products are being
   compared?** Let Paul describe it in his own words (e.g. "client's worried
   about his BrightRock premium going up, want to see it against a Discovery
   quote", or "compare [client]'s five existing policies against the BrightRock
   proposal"). Capture the full list of insurers/policies involved — this is
   **not** limited to two; a comparison can run BrightRock against one existing
   policy, or against five. Capture the client's name from this answer, or ask
   directly if it isn't mentioned — the name is what's used to locate the
   client's folder in Step 1.
2. **Is there a second life on any policy?** (a joint-life / second-life-assured
   structure on any side, not necessarily a separate spouse policy). If yes,
   get that person's details too — this drives Step 9 (Spouse/Partner Cover).
3. **For each insurer/policy named in Q1, is it a quote or does a policy
   schedule apply?** Sometimes every side is a new quote/proposal with nothing
   in force yet; sometimes some are in-force policy schedules and others are new
   quotes. Ask it that way round rather than assuming a schedule is always
   involved, and go through the list rather than assuming they're all the same
   type.
   - If **every side is a quote**, that settles it — move straight to Step 0b.
   - If **any schedule is involved**, follow up in the same conversation,
     confirming by insurer name which side(s) are in-force schedules and which
     are new quotes/proposals — the schedule side isn't always the client's
     original/existing insurer, and with more than two insurers involved it's
     worth confirming each one rather than assuming a pattern.

Do not ask about the Header or Key Facts Banner at this stage, or anywhere else —
they are standard on every comparison, not optional (see Step 0a).

Once these are answered, move to Step 0b (benefit scope) before retrieving
anything else. Only circle back to ask about start date, reference numbers,
health/lifestyle loadings, or what should headline the Key Facts Banner if the
retrieved documents don't already answer them.

### Step 0a — Section checklist and document voice

Immediately after the opening conversation (and before starting Step 0b/Step 1
document retrieval), present two quick choices.

**Sections** — a tick-box choice of which sections to include in this
particular comparison. Use multi-select so more than one can be ticked at once.
Options:

- Section 1 — Premium Snapshot
- Section 2 — Cover Comparison
- Section 3 — Premium Escalation Table
- Section 4 — Loyalty/Payback/Bonus Comparison
- Section 5 — Definition Quality
- Summary / Verdict
- Disclaimer / Sources

**Header and Key Facts Banner are never on this list — they are built into every
comparison regardless of what's ticked here, and must never be asked about.** Only
build the sections actually ticked; skip the corresponding step's content entirely
for anything not selected, but Steps 0b–2 (benefit scope, document retrieval,
product research) and Step 5 (accuracy rules) still apply in full to whatever
content is included. **Step 0b's benefit-scope restriction overrides a ticked
section, never the other way round** — a ticked section only ever shows benefit
categories the client actually requested (see Step 0b); ticking "Section 2" is not
permission to show excluded categories inside it.

**Document voice** — ask whether the Key Facts Banner, section commentary, and
Summary/Verdict should be written in **Paul's own first-person voice**
("I've put together...", "I recommend...", "my proposal") or in an
**institutional third-person voice** ("Wealth Revolution's Verdict",
"Wealth Revolution recommends"). **Default to Paul's own first-person voice**
unless he says otherwise for a particular comparison — this is his standing
preference as of 2026-09-23. Either way, the document stays addressed to the
client in the **second person** throughout ("your policy", "your cover") — the
voice choice only affects who is speaking, never who is being spoken to. Apply
the chosen voice consistently across every section, not just the Verdict —
including the banner, section ledes/footnotes, the letter's salutation and
signed closing (Step 10).

Paul deliberately limits how much reaches the client to avoid overload. Build
only the sections ticked above, and within them include additional detail or
comparison criteria only when they're genuinely material to this client's
decision — don't pad a section back out with technically-true but non-material
detail just because it's available.

### Step 0b — Determine the client's actual requested benefit scope (mandatory gate)

**This step is not optional and runs before any quote figure is used to decide
what the document compares.** A client very often requests only a subset of the
benefit categories that happen to appear on an insurer's quote (e.g. life cover
only, with severe illness or disability deliberately excluded for budget or
personal reasons) — the quotes themselves will frequently still show R0 or
"not selected" lines for the excluded categories, or simply omit them, and
neither of those is a safe signal on its own for what to build. **Never infer
scope from which categories merely appear with non-zero values across the
quotes being compared** — confirm it from what the client actually asked for.

1. Before retrieving quotes in Step 1 (or in the same pass, if it's more
   efficient to retrieve everything from the client's OneDrive folder at once),
   locate and read the client's own intake records: the **Follow-Up Appointment
   Summary Notes** (there may be more than one, across different meeting dates —
   read all of them), the **Fact Find Summary**, and the **WR Overview**
   document. These typically live in the client's main OneDrive folder, not the
   Risk Transaction/Comparative Quotes subfolder where the quotes themselves sit.
2. From these documents, determine explicitly which benefit categories the
   client asked to be compared/quoted for — Life Cover, Severe Illness/Dread
   Disease, Lump Sum Disability, Income Protection, debt cover, childcare/
   education benefits, etc. Look specifically for language stating a category
   was deliberately excluded (e.g. "elected to remove disability from his
   proposed option", "did not include this due to budget constraints") — this
   is a stronger and more reliable signal than any quote's own R0 line.
3. **The confirmed scope governs every section of the document, without
   exception.** A benefit category outside the confirmed scope must not appear
   anywhere in the deliverable — not as a comparison row, not as a "not
   selected on this proposal" line, not as an R0 entry, not in the Definition
   Quality section, not in the Verdict. If it isn't something the client asked
   for, it isn't mentioned at all. This applies however many insurers are being
   compared and whichever sections were ticked in Step 0a.
4. If the intake documents are genuinely silent on scope for a particular
   category (neither confirming nor excluding it), do not guess either way —
   ask Paul directly which categories to include, stating plainly what was and
   wasn't found in the intake records.
5. If, after reading the intake documents, a genuine ambiguity or conflict
   remains (e.g. one meeting note says something different from a later one, or
   the Fact Find and the Follow-Up notes disagree), flag it to Paul by name and
   ask him to confirm scope before building — never silently pick the more
   recent or more generous reading.

## Step 1 — Locate and retrieve source documents (OneDrive, automatic)

**This is a hard, non-optional rule: this skill must locate the client's
OneDrive folder and retrieve every source document itself. Never ask Paul to
paste, upload, or type out figures from a quote or schedule into the chat as
the default path** — that is a last resort only, used exclusively when
automatic retrieval has genuinely been tried and failed (see "If retrieval
fails" below). This applies to every side of the comparison, however many
insurers are involved, and to the intake documents required by Step 0b, not
just the quotes/schedules.

1. Locate the client's folder in OneDrive, matched by the client name captured in
   Step 0. (Use whichever access this session has to Paul's OneDrive — a synced
   local folder via the device bridge, or the Microsoft 365/SharePoint connector —
   depending on what's available in that session.)
2. Retrieve the **intake documents required by Step 0b** (Follow-Up Appointment
   Summary Notes — all dated versions, Fact Find Summary, WR Overview) from the
   client's main folder before or alongside the quotes/schedules — these are not
   optional extras, they are required inputs to Step 0b's scope gate.
3. Within the client's folder, for **every** insurer/policy named in Step 0:
   - For any side identified in Step 0 Q3 as a **quote**, search the **Risk
     Transaction** subfolder for the relevant comparative quote(s) — match by
     insurer/product name and take the most recent version unless told otherwise.
     **Comparative quote subfolders are not always flat** — a "Comparative
     Quotes" folder sometimes contains an unrelated set of documents (e.g.
     investment paperwork) while the actual life-insurance comparative quotes
     sit one level deeper in a nested subfolder, sometimes with a near-identical
     name (e.g. "Comparative quotes" nested inside "Comparative Quotes"). If the
     first matching folder doesn't contain quotes that match what Step 0
     described, check one level deeper before concluding nothing is there.
   - For any side identified as a **policy schedule**, search the client's folder
     (and any dedicated policy-schedule location within it, e.g. a "Policy
     Schedules" subfolder) for the current in-force schedule for that insurer.
   - If Paul also references a folder of prior analyses or reports (e.g. an
     "Analysis & Comparison Reports" subfolder) as cross-check material, locate
     and retrieve that too — treat it as background/cross-check context per
     Step 1's broker-document handling below, not as a primary figures source
     unless it's itself one of the primary documents named in Step 0.
4. Confirm with Paul, briefly, which specific files you found and are using
   (filename and date is enough) before starting Step 2 research — this is a
   quick confirmation, not a request to upload anything.

**If retrieval fails** — the client folder can't be found by name, a subfolder
doesn't contain a matching quote, no schedule can be found, or more than one
candidate document exists and it's unclear which is current: stop and ask Paul
directly, stating plainly what was searched and what wasn't found, rather than
guessing or proceeding on an unconfirmed document.

**If only a RAR or replacement document is found for a side that should have a
policy schedule** (i.e. it's in force, not a fresh quote), don't just proceed
on the RAR by default — flag this to Paul explicitly and ask whether he'd like
the client's actual policy schedule/quotation requested before the comparison
is built, alongside the RAR-sourced caveats required by Step 2 and Step 5 if
he chooses to proceed without it.

**Note on this session's access:** this step needs either a connected local device
with the OneDrive-synced folder available, or a working Microsoft 365/SharePoint
connection. If neither is available in the current session, say so plainly and ask
Paul to connect one rather than silently asking him to paste documents instead.

**A client's folder structure isn't always uniform.** OneDrive layouts vary —
some clients are filed under a "New Business" area with a flat first-name-then-
surname listing, others under an alphabetised existing-client structure; a named
subfolder (e.g. a BrightRock-specific quotes folder) is sometimes nested inside
the client's own folder rather than a sibling of it. If the first, most obvious
location doesn't have the file, broaden the search across Paul's known adviser
folders and re-check nesting before concluding a document can't be found — don't
stop at the first miss.

**Before treating any retrieved document as complete**, verify you actually have
every page — this is the single most common intake error. A multi-page scanned
policy schedule can appear as just its first 1–2 pages, with the actual benefit
table, premium projections, and exclusions missing. A document that looks
suspiciously short for what it should be (e.g. a cover letter + one summary page
for what should be a 15–20 page schedule) needs a direct check:

```bash
file /mnt/project/<filename>
unzip -l /mnt/project/<filename>   # some "PDF" files are actually zipped page images
```

A file reporting as `Zip archive data` despite a `.pdf` extension is a page-image
bundle (`1.jpeg`, `2.jpeg`, ... `N.jpeg`) — extract and view every page before
concluding the document lacks the data you need. Never build a comparison from a
schedule missing the actual benefit/cover table. If, after checking, a document
genuinely lacks a needed figure, say so explicitly and ask for it — never estimate
or research a substitute (see Step 5).

**If a schedule is scanned/image-based and OCR of the full page comes back thin
or garbled on a specific table** (this happens especially with premium/benefit
projection tables and multi-column adjustment tables), don't stop at "illegible"
— render that page to a high-resolution image and view it directly to transcribe
the table by eye, or crop and upscale just that region before re-running OCR (see
the OCR discipline note under Step 5). A table that OCR garbles is very often
perfectly readable to the eye at higher resolution.

**If a document's text genuinely can't be extracted at all** (a canvas-rendered
or fully image-based PDF where even the per-page OCR approach above comes back
unusable, not merely one garbled table) — fall back to visual reading via
Claude-in-Chrome: navigate directly to the document's own webUrl (this uses
Paul's already-authenticated browser session, so it opens directly) and read it
visually page by page with screenshots/zoom, rather than declaring the figures
unavailable. **Watch for inconsistent per-page rotation** on this kind of PDF —
some pages render sideways or upside-down independently of others — use the PDF
viewer's own rotate control and the page-number jump field to straighten and
navigate each page individually rather than assuming one rotation fix applies
to the whole document.

**Broker/insurer-supplied competitor comparison documents:** if a third document
turns up alongside the quote/schedule, typically from one insurer's own broker
consultant comparing both products, treat it as **background context only**, never
a client-specific figures source — it does not carry the same weight as each
insurer's own document. Every general product claim in it must still be
cross-checked against the relevant insurer's own source documents. Where a specific
claim can't be independently verified, flag it and attribute it in the document as
broker-sourced and adviser-confirmed, not independently verified.

**WR Overview vs. an insurer's own quote — resolving a conflict.** The WR Overview
sheet is Paul's own internal summary, assembled by hand, and it can go stale or
carry a typo relative to the insurer's own quote document (e.g. an outdated
escalation rate from an earlier version of the quote). **When the two disagree on
a figure, the insurer's own quote/schedule document wins** — it's the primary,
contractual source. Never silently prefer the WR Overview's figure, and never
silently drop the conflict either: name it to Paul directly (which document said
what, and which figure the document uses and why) so he can correct the Overview
sheet if it's simply out of date.

## Step 2 — Product knowledge research (mandatory, every time, for every insurer)

This step is non-negotiable regardless of how many insurers are being compared.

- **Exact product name and tier.** Insurer ranges are frequently tiered (e.g.
  Premier/Classic/Express) and features on one tier don't apply to another — confirm
  the exact product name and tier as stated in the source document, and never assume
  a feature is included without checking it applies to that specific tier.
- **Authoritative sources only.** For each insurer, read the insurer's own Technical
  Guide, product guide, or policy wording, and official product pages. Treat
  handwritten RAR notes or adviser summaries as descriptive only, not authoritative.
  Where sources conflict, the insurer's own Technical Guide or policy wording wins.
- **Specific features to always research and verify before stating anything about
  them:**
  - Survival period on severe illness/critical illness benefits, and whether it
    varies by condition.
  - Whether severe illness cover is accelerated (reduces life cover on claim) or
    standalone.
  - The disability definition set used — exact name and what it covers.
  - Income protection waiting period and benefit term.
  - Whether any cashback/loyalty/bonus/premium-return benefit is optional or
    included, and its conditions.
  - **Annual premium increase type: fixed/contractual or age-related/age-rated —
    determined from the insurer's own literal wording on that specific client's
    document, never from the size of the percentage or from general familiarity
    with the insurer.** A flat stated rate like "Yearly premium increase: 10.0%"
    or "Compulsory: 10.00% / Voluntary: 0.00% / Total: 10.00%" printed as a single
    contractual figure is fixed, even though 10% might intuitively "feel like" an
    age-rated magnitude — read what the document actually says the mechanism is,
    not just the number. Conversely, wording like "age factor", "Age Rated
    Premium Pattern", or a rate that recalculates against the client's current
    age at each review is age-rated regardless of how small the current figure
    looks. Never describe an age-related pattern as fixed, and never describe a
    stated-fixed pattern as age-rated because its number happens to be large —
    see Step 4 and Step 5 for the mandatory verification routine this feeds.
  - The premium guarantee period.
  - Maximum payout percentage on severe illness/critical illness benefits, and
    whether multiple/unrelated claims are capped.
  - Any cover increase/buy-up facility without new medical underwriting, and its
    limits.
  - **Whether the severe illness/critical illness payout is a flat percentage or
    severity-tiered** (varies by diagnosis severity) — always confirm which applies.
  - **Whether a loyalty/discount mechanism has more than one moving part** — e.g.
    an upfront discount plus a separate ongoing, engagement-linked adjustment.
    Understanding this still matters for picking the single most relevant figure
    for Step 6's table, even though the document itself now only shows that one
    figure.
  - **Whether an upfront discount is time-limited (a promotional/"New Business
    Special Offer" rate) or standing** — see Step 6.
- **Never state without confirmation:** specific sub-product/rider/tier names not in
  the source document; optional riders described as included unless the source
  specifically includes them; a "broader trigger" for income protection/disability
  unless explicitly confirmed; a temporary or partial disability layer unless
  confirmed.
- **Flag everything unconfirmed.** Anything based on general product knowledge
  rather than the client's specific documents must be explicitly flagged, e.g.
  *"Based on the [Insurer] [Tier] product range — to be confirmed against the actual
  policy schedule."*

**Known hard-won traps — check for these specifically whenever the relevant
insurer appears, but still verify fresh against that client's own documents
each time, never from memory of a prior comparison:**

- **Discovery's ACI already incorporates the cost of its ABI.** ACI and ABI
  are not additive — never add them together when stating Discovery's premium
  or cover cost.
- **BrightRock's ACI is contractually fixed for the life of the policy;
  Discovery's is age-rated and accelerates over time.** Never describe the two
  as working the same way, or imply BrightRock's is a headline rate that can
  drift like Discovery's. **BrightRock's own quote states this as a flat
  "Yearly premium increase" figure — do not relabel it age-rated just because
  the percentage is a round, sizeable number; read the document's own wording.**
- **Momentum's premium increase is also commonly printed as a flat
  Compulsory/Voluntary/Total breakdown (e.g. "Compulsory: 10.00%") — this is a
  fixed contractual figure on Momentum's own document, not an age-rated one,
  unless that specific client's document states otherwise.**
- **Liberty and Discovery commonly use a genuinely age-rated pattern** — confirm
  against the specific document's own wording (Liberty's own term is typically
  "Age Rated Premium Pattern"; Discovery's ACI is age-rated and calculated as a
  factor against a standard age-based table) — and note that a client-selected
  **Automatic/Annual Benefit Increase (cover growth) stacks multiplicatively,
  not additively, with an age-rated cost-of-insurance increase** — e.g. a ~9–10%
  age-rated cost increase combined with a separately-selected 10% Automatic
  Benefit Increase can produce a combined effective premium increase around
  19–21% in a given year — (1+a)×(1+b)−1, not a+b. A high combined figure of
  this kind is not necessarily wrong; see Step 5's mandatory verification
  routine before accepting or rejecting it.

## Step 3 — Verify key facts from source documents

Extract and verify the following for each insurer (include only what's genuinely
present/material — don't force items into every comparison, and never extract or
present a figure for a benefit category outside the scope confirmed in Step 0b):

Policy/proposal number and start date · current or quoted monthly premium (total,
including riders/add-ons/fees) · annual premium increase rate and type · annual
benefit/cover increase rate · life cover amount · permanent disability cover amount
and definition set (**only if disability is within the Step 0b scope**) · severe
illness/critical illness/dread disease cover amount, accelerated or standalone,
survival period (**only if severe illness is within the Step 0b scope**) · income
protection amount, waiting period, benefit term (**only if income protection is
within the Step 0b scope**) · debt cover components (each debt listed separately
with term and cover option, where structured that way) · childcare/family benefits
(listed per child if structured that way) · any cashback/loyalty/bonus/premium-
return benefit and all its conditions, including every moving part per Step 6 ·
any cover increase/buy-up facility and its limits · any cover conversion/
restructuring facility and its conditions · beneficiary details, where relevant ·
whether a spouse/partner has independent cover or is a rider · health/lifestyle
loadings applied (percentage and unloaded premium).

Where the source document states a total for lump-sum cover, use that figure
directly rather than summing components yourself.

**Include only where applicable:** terminal illness benefit (accelerated payout
ahead of death — this is intrinsic to the death benefit, not a separate
requested category, so it stays in scope even when severe illness/disability are
excluded); standard policy exclusions where materially relevant (e.g. suicide
clause); claims-paying reputation/insurer financial strength, where researched
and citable.

**Deliberately excluded from this checklist — do not add them:** waiver of
premium, underwriting basis, and cession.

**Where a Cash Conversion / guaranteed-value benefit exists**, distinguish
clearly between what is illustrated (projected, not guaranteed) and what is
contractually guaranteed, and state plainly when any guaranteed floor
crystallises — never present an illustrated value as if it were guaranteed.

## Step 4 — Premium pattern — how to explain it correctly

The critical distinction for every policy is whether the premium pattern is
**age-rated/age-related** (increases as the client ages — the current rate is only
a snapshot) or **fixed/level** (contractually fixed regardless of age). **Confirm
which applies to each insurer from that insurer's own literal wording on the
specific document being used — never from the size of the percentage, never from
general familiarity with the insurer, and never assumed either way.** A fixed rate
can be a large round number (10%); an age-rated rate can look modest in its first
year and still be age-rated. If the pattern or guarantee period is unclear, flag
it and recommend confirming with the insurer.

- Always present a year-by-year premium projection table covering at least 10
  years for every insurer in the comparison (only if Section 3 was ticked in Step 0a).
- Always state the premium guarantee period for every insurer.
- If a health/lifestyle loading applies to any policy, note that the premium gap
  narrows or widens accordingly, if determinable.
- **If an insurer's premium pattern includes an ongoing, engagement-linked
  adjustment layered on top of its base escalation** (e.g. Discovery's
  Vitality/Health Integrator adjustment on top of AcceleRater age-rating), state
  plainly that the printed/projected figures already include that adjustment at
  the client's *current* status, and that it can move in either direction as the
  client's engagement or claims experience changes in future years — see Step 6.
- **Do not quietly accept, suppress, or round away a surprising escalation
  figure just because it happens to come straight from the source document.** A
  figure that looks high or low against Paul's own stated industry baseline, or
  against the other insurers in the same comparison, is a prompt to run Step 5's
  mandatory escalation-verification routine before it goes in the document, not
  a reason to quietly present it either as-is without comment or to adjust it.

**Every insurer's row in the Premium Escalation Table must show a year-on-year
percentage badge, for every year it has a rand figure — never rand amounts alone
for one insurer while another gets percentages.** This is not optional and applies
whether or not the source document itself prints a percentage:

- If the source document *states* the escalation rate (e.g. Old Mutual's 5%,
  BrightRock's guaranteed ACI), use that stated rate as the badge.
- If the source document only prints rand amounts year by year with no stated
  percentage (this is the normal case for most insurers' own projection tables —
  e.g. Discovery, Standard Bank Flexi Life), **calculate the year-on-year %
  yourself** from those printed rand figures: `(this year − prior year) / prior
  year × 100`, to two decimal places. This is a calculation performed on
  source-sourced figures, not an invented or estimated figure, and Step 5's "never
  estimate a figure" rule does not block it — carrying an insurer's own printed
  rand progression without also surfacing what it works out to as a percentage
  leaves the client unable to compare escalation rates across insurers at a
  glance, which is the entire point of this table.
- Where a rand figure is missing for a given year (`.na` "not provided"), there is
  of course no percentage badge for that year either.
- If an insurer prints no year-by-year table at all (e.g. a policy whose schedule
  just says premiums are "reviewable"), there is nothing to calculate — leave it
  `.na`, as already covered by Step 5.
- **Disclose which badges are printed-by-the-insurer versus calculated by you**,
  in the section's footnote — one sentence naming which insurers' percentages are
  sourced directly and which are your own year-on-year calculation off their
  printed rand figures. Never let a calculated percentage sit next to a printed
  one with no distinction drawn between the two.
- **If a calculated year-on-year % is a clear outlier against the surrounding
  pattern for that same insurer** (e.g. one year jumping to roughly double the
  neighbouring years' rate, or a negative/declining figure), flag it explicitly in
  the footnote as worth confirming with the insurer — don't silently smooth it
  into the table or drop the badge for that year. A calculated outlier is exactly
  the kind of thing this table exists to surface, not hide.

**Watch for base-year/anchor mismatches.** An insurer's stated "current premium"
and the *first row* of that insurer's own separate illustrative projection table
are not automatically the same year — the current premium can actually match the
projection table's *prior* year. Before building any escalation table: locate the
insurer's own projection/illustration table (not just the summary), read its year
labels literally, and confirm which year the "current confirmed premium" actually
corresponds to by matching it against the projection table's own figures — never
insert it at whatever row feels like "now." If a projected year-on-year change
looks unusually large against the surrounding pattern, treat that as a signal to
re-verify the underlying figures via a tighter OCR crop (see Step 5) before
publishing a percentage.

## Step 5 — Accuracy rules — non-negotiable

- Every figure must be sourced directly from a retrieved document. Never estimate,
  research, or infer a substitute for a missing figure.
- Never invent totals — use only totals as presented in the source document.
- If a figure cannot be verified, it must not appear — flag it as "not available in
  source documents" instead.
- Never combine figures from different quote or schedule versions.
- Premium projections must come directly from the insurer's own projection table
  where one exists.
- Cross-check every figure against the source document one final time before
  finalising.
- Where a RAR is the only source for one side, every feature description on that
  side must be flagged as RAR-sourced, not schedule-confirmed.
- **Do not remove or alter a figure that looks anomalous or surprising without
  confirming with Paul first.**

### Escalation-percentage verification — mandatory, every insurer, every build

This is a hard gate, not a spot-check: run it for **every** insurer's premium
escalation figure in **every** comparison, not only when something looks
questionable, because the two things most likely to be wrong — fixed vs.
age-rated labelling, and the exact percentage — are also the two things a
client or Paul is most likely to scrutinise directly.

1. **Recompute every percentage from the source document's own figures.** Never
   carry forward a percentage from memory, a prior comparison, or an internal
   summary sheet without independently recalculating it from that specific
   document's own printed rand or percentage figures.
2. **Treat Paul's internal adviser sheets (e.g. the WR Overview) as a secondary
   cross-check only, never a primary source.** If an internal sheet's figure
   disagrees with the insurer's own quote/schedule, the insurer's own document
   wins — and the conflict is flagged to Paul by name (which document, which
   figure), never silently resolved either way (see Step 1's WR Overview
   handling).
3. **When a figure looks unusually high or low** — against Paul's own stated
   industry baseline, against the other insurers in the same comparison, or
   simply on its face — do the research, don't just reassure:
   - Re-derive the arithmetic by hand from the source document's own numbers
     (e.g. recompute several year-over-year percentages from a multi-year
     projection table) to confirm the raw figure itself is correct.
   - Look for an actuarially plausible mechanism (e.g. a multiplicative stack
     of an age-rated cost-of-insurance increase with a separately-selected
     Automatic/Annual Benefit Increase — see Step 2's traps list) and check
     whether the client's specific document shows the components that would
     produce it.
   - Search for external corroboration: the insurer's own public technical
     guide, brochure, or product page, and reputable general coverage, for the
     mechanism in question — not just the headline number.
4. **Report what was and wasn't independently confirmed, honestly — but keep the
   client document itself short.** The full tiered answer (what's confirmed, what's
   reasoned inference, what's externally sourced, what to do next) is for the
   conversation with Paul — see Step 12's Honesty check — not for the client-facing
   letter. In the document itself:
   - State the verified percentage as fact, directly, once step 1 above confirms it
     — no hedging language needed for a figure that's been recomputed and checked.
   - If the figure is a genuine outlier worth a client-facing caveat at all, add
     **at most one short clause** naming that the mechanism is worth confirming
     with the insurer (e.g. "worth confirming the exact mechanism with [Insurer]")
     — never a paragraph walking through the arithmetic or the candidate
     explanation. If there's nothing material enough to say in one clause, leave
     the figure to stand on its own rather than manufacturing a caveat.
   - Never present a reasoned-but-unconfirmed mechanism as externally verified
     fact — the fix for that is stating less about the mechanism in the document,
     not writing more hedged prose about it.

**OCR discipline — "illegible" is a starting point, not an endpoint.** A figure
marked illegible on a first-pass full-page OCR is often readable after cropping and
upscaling just that region, or by rendering the page to a high-resolution image and
viewing it directly (this matters especially for multi-column adjustment tables,
which OCR often garbles worse than plain prose). Before telling the adviser or
client a figure "could not be confirmed":

```bash
python3 -c "
from PIL import Image
img = Image.open('page.jpeg')
crop = img.crop((x0, y0, x1, y1))          # isolate just the table
crop = crop.resize((crop.width*4, crop.height*4), Image.LANCZOS)
crop.save('crop.png')
"
tesseract crop.png - --psm 6
```

Check the crop coordinates against a `view` of the full page first; a 3–5x upscale
on a tightly-cropped table is usually enough to turn garbled OCR into clean digits.
Cross-check against another OCR pass of the same region before trusting a recovered
figure. **When you recover a previously-illegible figure, grep the whole document
for every place the old placeholder value or its downstream calculations
(percentages, gaps, "R[amount] more/month" style figures) were used, and fix all of
them together** — a single misread premium can silently propagate into a banner, a
verdict, and a premium-snapshot card if not caught everywhere at once.

**Never promote a hypothetical into an asserted fact.** If an adviser gives an
illustrative example to explain how a mechanism works (e.g. "let's say Blue"
tier), keep the explanation general — do not write it into the document as the
client's confirmed actual status. If a client-specific value is needed and isn't
confirmed in a retrieved document, say so and ask, rather than treating the most
recently-mentioned example as settled. If this kind of error is found, grep the
whole document for the term — the same wrong assumption tends to repeat in more
than one section once introduced.

**When a document has two similarly-labelled status fields, confirm which one a
table actually uses before stating a figure.** Some insurers record more than one
status for the same client on the same schedule (e.g. a general "Vitality status"
and a separate "Vitality Money status", using the same tier names but for
different purposes) — check the exact field label the mechanism's own table
references before picking which of the client's recorded values applies, and if
the document genuinely doesn't disambiguate, say so explicitly rather than
picking one silently.

**When a client fact changes mid-build** (e.g. a new start date agreed after a
signed document): state plainly that the signed document says something different,
so it's clear you're recording new information, not misreading the old document.
Update every affected place (header, summary cards, projection tables, date
labels) — grep for the old value across the whole file. Flag once, briefly, that
figures anchored to the old date/version should ideally be reconfirmed with the
insurer; don't repeat the caveat more than once.

## Step 6 — Loyalty/payback/bonus/cashback benefits

Only relevant if Section 4 was ticked in Step 0a. **Keep this section as simple as
possible — one compact table, nothing else.** Paul's own instruction, direct: "provide
payback amounts if applicable and when, or provide simple payback percentages and
when." Never a headline, never a multi-paragraph justification, never let the
banner or verdict lead with a payout figure as the reason to switch.

**The entire section is one table, four columns, one row per insurer:**

| Insurer | Benefit (its name) | Amount or % | When |
|---|---|---|---|

- **Amount or %** — whichever the source document actually states: a rand figure
  (e.g. "R[amount] today, growing to R[amount]") or a percentage (e.g. "25%", "15%"). If
  a benefit isn't confirmed on this quote, the cell reads **"Not on this quote"** —
  nothing more.
- **When** — one short phrase: an upfront discount's duration/expiry if time-limited
  (e.g. "Upfront, ends [date]"), or a payout's date/trigger if it's a future
  pay-out (e.g. "At [client]'s change-moment date, [date]"). Not a sentence, a
  phrase.
- **Do not add** a conditions column, a forfeiture column, a guarantee-period
  column, a dual-mechanism breakdown, an "Honest Position" box, or any narrative
  paragraph below the table beyond, at most, one short closing line if genuinely
  needed (e.g. "All of these require the policy to stay in force to keep the
  value.") — that single sentence is the ceiling, not a starting point to build
  back up from.
- This still relies on Step 2's research to get the right benefit name and figure
  for each insurer, and Step 5's accuracy rules still apply to every figure in the
  table — simplifying the *presentation* is not licence to skip verifying the
  number. It just means the verified number goes straight into the table without
  the surrounding explanation the old version carried.
- If an insurer's mechanism has more than one component (an upfront discount and a
  separate ongoing adjustment, say), pick the single figure that's most relevant to
  the client today (usually the upfront one) for the table, and leave the rest for
  Paul in conversation if he wants the detail — it does not belong in the client
  document by default any more.

## Step 7 — Insurer-specific unique features (dynamic section)

Feeds into Section 2 (Cover Comparison) and Section 5 (Definition Quality) if
ticked in Step 0a — **and only for benefit categories confirmed in scope by Step
0b.** Every insurer has genuine differentiators; never hardcode any insurer's
features as universal. Look for: proprietary claim-assessment mechanisms or
broader trigger definitions not offered by other insurers in the comparison;
survival period differences on severe illness claims; maximum payout percentage
and claim caps; cover conversion/restructuring/"change of need" facilities; cover
buy-up facilities without medical underwriting; needs-matched vs fixed-block cover
structuring; any benefit genuinely exclusive to one insurer.

Each unique feature must be verified against Step 2 research (never assumed from
familiarity with any insurer), stated with a plain-language explanation of what
it means for the client practically, and where genuinely advantageous marked with a
green "Insurer X wins" badge (amber for a fair trade-off, per the colour system in
Step 10).

**Features relevant to the client but absent from their specific document:**
general product research sometimes surfaces a feature (e.g. retrenchment/instalment
protection) that's genuinely material to the client's decision but not present on
their specific proposal. Surface it anyway if it's material to their stated
concern — sourced from the insurer's own public product materials, not assumption,
and **only if it relates to a benefit category within the Step 0b scope.** State
plainly what conditions would need to be met for the client to access it, mark
it clearly as "not on this proposal / not confirmed for this client" so it's never
mistaken for something they currently have, and note in Disclaimer/Sources that it
was sourced from general product materials rather than the client's own document.

Include a summarised "who's ahead" assessment across the key dimensions at the end
of this section, if Section 2 is included.

## Step 8 — Definitions and claim quality

**This is the section most likely to end up carrying more detail than the client
actually needs.** Don't tick Section 5 by habit — only include it when Paul
specifically wants definitions/claim-quality compared for this client, and if it's
included anyway, keep it as lean as Step 6's table (name the definition set and
the one material difference, if any — not every clause). Only relevant if Section
5 was ticked in Step 0a, **and only for the benefit
categories confirmed in scope by Step 0b** (e.g. if severe illness and disability
are out of scope, this section covers life cover claim quality only — do not add
severe illness or disability definition rows because they happen to exist on an
insurer's product range). State the definition set used for permanent disability
and severe illness on every policy, **where those categories are in scope**. Note
whether severe illness/critical illness is accelerated or standalone, where in
scope. Explain in plain language that broader, more client-friendly definitions
generally increase the likelihood of a successful claim. Where one insurer's
definitions are materially broader or narrower than the others, highlight this
clearly with supporting detail. Where a benefit is tier-restricted, state this
explicitly.

## Step 9 — Spouse/partner cover (second life)

Triggered by Step 0 Q2. Always check whether the second life has independent cover
or is a rider/add-on on the main life's policy. If a rider, make clear their cover
is entirely dependent on the main life's policy remaining in force. Compare the
second life's cover across every insurer involved, even where an insurer provides
nothing for them — say so explicitly, **but restricted to the benefit categories
confirmed in scope by Step 0b, same as the main life.** This is folded into
Section 2 (Cover Comparison) rather than given its own heading.

## Step 10 — Document format, visual design and tone

**Format:** output as a standalone HTML file, designed to open cleanly in Google
Chrome and be sent as a client deliverable, convertible to PDF on request. **The
document must read as an actual letter written to the client**, not a report that
happens to address them in second person — see the Structure list below for where
the salutation and signed closing sit. Write with the client always addressed
in second person throughout ("your policy", "your cover", "you will receive") — the
speaker's own voice (Paul's first person, or an institutional third person) is set
by the Step 0a document-voice choice and applies to the narrator, never to how the
client is addressed. Use tables for all side-by-side comparisons with clearly
labelled totals rows sourced from the documents. **Where a table cell, caveat, or
explanatory note conveys more than 2–3 distinct facts, default to a short bullet
sub-list inside that cell rather than a dense paragraph** — this is a firm rule,
not a style preference.

**Visual design — neutral, insurer-agnostic palette, sized for N insurers.**
Colours are assigned by position (order the insurer was mentioned/introduced in
Step 0), never by brand, so the same palette is reused for every comparison
regardless of which insurers are involved. The house gold accent is reserved for
Wealth Revolution framing (banner, section underlines, highlight rows) and is
never assigned to an insurer:

```css
:root{
  --house-gold: #B08D57;        /* Wealth Revolution house accent — banner, underlines, highlight rows. Never assign to an insurer. */
  --house-gold-light: #F3ECE0;
  --charcoal: #1A1A1A;           /* header / dark panels / totals rows */
  --bg: #F9F7F4;                  /* base background, warm off-white */
  --white: #FFFFFF;

  /* Positional insurer palette — assign in order encountered, up to six.
     For a two-insurer comparison, use only ins-1 and ins-2 (this is the old
     --ins-a/--ins-b pair, renamed for the general N-insurer case). */
  --ins-1: #B8860B; --ins-1-light: #FBF1DE;   /* e.g. a proposed/BrightRock-style slot: reserve a distinct dark/amber treatment if that insurer should visually anchor the comparison (see card styling below) */
  --ins-2: #2C3E70; --ins-2-light: #E9ECF5;
  --ins-3: #1B7A72; --ins-3-light: #E4F3F1;
  --ins-4: #6B4C9A; --ins-4-light: #EFE7F5;
  --ins-5: #1565C0; --ins-5-light: #E3EFFB;
  --ins-6: #5D6D7E; --ins-6-light: #E9ECEE;

  --green: #2E7D32;              /* advantage / "wins" badge, on --green-light #E8F5E9 */
  --green-light: #E8F5E9;
  --red: #C62828;                /* disadvantage / unfavourable condition, on --red-light #FFEBEE */
  --red-light: #FFEBEE;
  --amber: #E65100;              /* comparable / conditional / nuanced, on --amber-light #FFF3E0 */
  --amber-light: #FFF3E0;
  --text: #2C2C2C;
  --muted: #666666;
  --border: #E0DDD8;
}
```

If more than six insurers/policies genuinely need to appear in one comparison
(rare), extend the pattern with additional visually-distinct hues rather than
reusing an existing slot — never let two different insurers share a colour.

Totals rows: charcoal background, each insurer's values shown in a lightened
version of their colour. Highlight rows: a subtle gold tint. **Fonts:** headings in
Playfair Display (serif), body in Source Sans 3 (sans-serif) — both loaded via
Google Fonts. The proposed/lead insurer (typically BrightRock, when it's the
proposal being built toward) gets a dark card treatment (charcoal background,
`--ins-1` accent text) to visually anchor it as the recommendation; every other
insurer gets a light card in its own assigned colour. In the header, each
insurer's name/chip gets a background chip in its own assigned colour.

**Scaling tables and cards for more than two or three insurers:**

- **Premium snapshot / summary cards:** use a responsive grid —
  `grid-template-columns: repeat(auto-fit, minmax(200px, 1fr))` — so cards wrap
  cleanly whether there are 2 or 6 insurers, rather than forcing a fixed
  two-column layout.
- **Comparison tables:** wrap every table in a horizontally-scrollable container
  (`overflow-x: auto`) once there are more than 3–4 insurer columns, with the
  header row and first (row-label) column both set `position: sticky` so the
  row label and column headers stay visible while scrolling sideways — this is
  essential once a table is wider than the page. Give the table a sensible
  `min-width` so columns don't get uncomfortably cramped.
- Every other visual rule in this step (badge colours, `.na` treatment, totals
  row styling, bullet sub-lists in cells) applies unchanged regardless of how
  many insurers are being compared.

**Handling a gap in one insurer's premium projection data** (e.g. their table stops
short of the full 10-year window): use a dedicated `.na` style — visually distinct
from a real R0 value, never left blank or implying zero — and label the cell
plainly (e.g. "not provided") rather than omitting the row.

**Structure:** the **Header** and **Key Facts Banner** are built into every
comparison, always, in that order, first — never optional and never asked about.
A **salutation** follows immediately after the Key Facts Banner, and a **signed
closing** appears immediately before Disclaimer/Sources (or at the very end if
Disclaimer/Sources wasn't ticked) — these two are as non-negotiable as the Header
and Key Facts Banner, since the whole document is a letter to the client, not a
standalone report. Everything else after the salutation follows in this order,
but **only include what was ticked in Step 0a, and only for benefit categories
confirmed in scope by Step 0b**:

1. **Header** *(always included)* — client names, policy/proposal reference
   numbers, dates, adviser details.
2. **Key Facts Banner** *(always included)* — gold-highlighted box addressing the
   single most important issue specific to this client. Never generic.
3. **Salutation** *(always included)* — e.g. "Dear [ClientFirstName]," — opens
   the body of the letter immediately after the Key Facts Banner, followed by a
   brief, warm opening line in the voice chosen in Step 0a before moving into the
   sections below.
4. **Section 1 — Premium Snapshot** *(if ticked)* — side-by-side premium cards
   for every insurer: monthly premium, escalation rate and type, benefit
   escalation rate, guarantee period.
5. **Section 2 — Cover Comparison** *(if ticked)* — full line-by-line benefit
   table with totals rows, every benefit a separate row, cover amount and monthly
   equivalent where applicable, debt cover broken out per debt where structured
   that way, second-life cover per Step 9 where relevant — **restricted entirely
   to categories confirmed in scope by Step 0b.**
6. **Section 3 — Premium Escalation Table** *(if ticked)* — minimum 10-year
   year-by-year projection. Columns: Year/Date, Age, one column per insurer in
   the comparison. Use the `.na` treatment above for any gap in an insurer's
   data, and the sticky-header/scrollable pattern once there are more than 3–4
   insurer columns. **Every insurer's rand figures must carry a year-on-year %
   badge (printed or calculated per Step 4) — no insurer's column is rand-only
   while another shows percentages**, and the footnote must say which badges are
   printed by the insurer and which are your own calculation, per the mandatory
   verification routine in Step 5.
7. **Section 4 — Loyalty/Payback/Bonus Comparison** *(if ticked)* — Step 6's
   single minimal table (Insurer / Benefit / Amount or % / When), nothing more.
8. **Section 5 — Definition Quality** *(if ticked — and only if Paul specifically
   wants it; don't tick by default, see Step 8)* — disability and severe illness
   definitions compared across every insurer **(only where those categories are
   in scope per Step 0b)**, kept as lean as Step 6's table.
9. **Summary / Verdict** *(if ticked)* — dark background, bullet points, client
   addressed by name in second person throughout, narrated in the voice chosen
   in Step 0a. Each point: bold headline statement first, supporting detail
   after.
10. **Signed closing** *(always included)* — a closing line (e.g. "Kind regards,")
    followed by Paul's name, Wealth Revolution (Pty) Ltd, FSP 45946, and contact
    details, in the voice chosen in Step 0a, immediately before Disclaimer/Sources.
11. **Disclaimer / Sources** *(if ticked)* — every source document listed with
    document number and date; state that calculated projections are illustrative,
    not guaranteed, unless the insurer's own table states otherwise.

## Step 11 — What not to do

Do not fabricate, estimate, or carry over figures from memory or a previous
comparison. Do not present a conditional benefit as unconditional. Do not add the
premium escalation rate and benefit escalation rate together to produce a combined
figure. Do not use a superseded quote/schedule version, or mix figures from
different versions in the same document. Do not begin building until Step 0, Step
0a, Step 0b, and Step 1 are complete. Do not make claims about cover, definitions, or
benefits not explicitly stated in the source documents, or use names/tiers not
confirmed in them. Do not state a feature is exclusive to one insurer without
Step 2 research confirming it against every other insurer in the comparison. Do
not describe a premium pattern as fixed or age-rated based on the size of the
percentage — confirm it from the insurer's own literal wording every time (Step 2,
Step 4). Do not build Section 4 as anything other than Step 6's single minimal
table — no conditions column, no forfeiture column, no "Honest Position" box, no
dual-mechanism breakdown; that level of detail was explicitly removed at Paul's
request and reintroducing it piece by piece is exactly the drift this rule exists
to block. Do not default to favouring whichever insurer you built the last
comparison for — every comparison starts neutral unless Step 0 says otherwise. Do
not ask Paul to paste or upload source documents — retrieve them per Step 1's hard
rule, and only ask him directly if retrieval genuinely fails. Do not silently
default to an institutional third-person voice — Step 0a's default is Paul's own
first-person voice unless he says otherwise for that comparison. **Do not leave
one insurer's premium escalation row as rand-amounts-only while another insurer's
row shows percentages — every insurer needs a year-on-year % badge, calculated
from its own printed rand figures if the source doesn't state one (Step 4).**

**Do not compare, mention, or show a "not selected"/R0 line for any benefit
category outside the scope confirmed in Step 0b** — inferring scope from which
categories merely appear on a quote, rather than from the client's own intake
records, is exactly the mistake Step 0b exists to prevent. If severe illness,
disability, or income protection were not requested, they do not appear anywhere
in the document, in any form.

**Do not state an escalation mechanism as independently confirmed when it is a
reasoned inference** — but also do not write a multi-sentence explanation of that
reasoning into the client document. Step 5's mandatory verification routine
requires recomputing every percentage and researching unusual figures, and the
full honest tiered answer belongs in conversation with Paul; the document itself
gets the confirmed figure and, at most, one short clause.

**Do not ship the document as an unaddressed report.** Every document is a letter
to the client — a salutation after the Key Facts Banner and a signed closing
before Disclaimer/Sources are both mandatory (Step 10), not optional polish.

**Adviser-facing content does not belong in the client deliverable.**
Self-correction commentary ("an earlier version of this mistakenly showed X") is
useful in conversation with Paul but must never ship in the client-facing document.
Fix the substance silently; if a paragraph reads as internal reasoning rather than
something written for the client, remove it or move it into the chat response
instead. **This also covers quote-version history:** when any insurer's quote or
schedule is swapped for a newer version mid-engagement, describe only the current
version's own facts — never frame anything against what an earlier version
included, excluded, dropped, or changed (e.g. "no longer includes," "previously
had," "the updated quote removes"). The client never saw the earlier version and
has no use for its history, however factually accurate the comparison would be.
If a benefit simply isn't on the current quote, it's treated exactly like any
other absent feature (`.na` / "Not on this quote" per the existing patterns) —
not called out as something that used to be there.

## Step 12 — Pre-delivery checks

Run these before presenting the finished document.

**Benefit-scope check** *(mandatory, every build)* — confirm the document contains
no mention whatsoever of any benefit category outside the scope confirmed in Step
0b, not even as an excluded/"not selected"/R0 line:

```bash
grep -n -i "severe illness\|dread disease\|critical illness\|lump sum disability\|income protection" output.html
```

Every match must be investigated — if any category outside the confirmed scope
appears anywhere (including inside a cell that otherwise looks like "not
selected"), remove it entirely before delivery.

**Escalation-accuracy check** *(mandatory, every build)* — confirm Step 5's
verification routine was actually run for every insurer's escalation figure:
every percentage has been independently recomputed from source figures, every
fixed-vs-age-rated label has been checked against that insurer's own literal
wording (not inferred from the number), and any internal-sheet conflict has been
resolved in favour of the insurer's own document and flagged to Paul by name.
Also confirm the document itself stayed short about it — the verified figure,
and at most one short clause, never a paragraph walking through the mechanism
(Step 5).

**Section 4 simplicity check** *(mandatory, every build where Section 4 is
included)* — confirm Section 4 is exactly Step 6's one table (Insurer / Benefit /
Amount or % / When) and nothing else — no conditions column, no forfeiture
column, no guarantee-period row, no "Honest Position" box, no dual-mechanism
paragraph. If Section 5 is included, confirm it stayed similarly lean.

**Letter-format check** *(mandatory, every build)* — confirm a salutation
immediately follows the Key Facts Banner and a signed closing (Paul's name,
Wealth Revolution (Pty) Ltd, FSP 45946, contact details) immediately precedes
Disclaimer/Sources (or closes the document if that section wasn't ticked).

**Personalization pass** — grep for third-person slips before treating a
client-facing document as done. This matters for both the client-address check
(always second person) and, when Paul's first-person voice was chosen in Step 0a,
for stray institutional phrasing that should have been rewritten:

```bash
grep -n "\bhis \|\bhe \|\bhe's\|\bhim \|<ClientName>" output.html
grep -n -i "Wealth Revolution's Verdict\|Wealth Revolution recommends\|Paul would like\|Paul has\|worth discussing with Paul" output.html
```

Confirm every match is either metadata (a header "Client:" row) or an intentional
direct-address use ("Hi [client first name]," / "you, [client first name],") — narrative prose to the
client should be second person throughout, and where Paul's own voice was chosen,
narration should read as him speaking ("I've put together..."), not as the firm
speaking about him in the third person.

**Structural integrity check** — catches malformed edits (a broken `rowspan`, an
orphaned footnote marker, mismatched tags) before the adviser sees them:

```bash
python3 -c "
content = open('output.html').read()
print('tables open/close:', content.count('<table'), content.count('</table'))
print('divs open/close:', content.count('<div'), content.count('</div'))
"
```

Also grep for any footnote symbol (†, ‡, *) used in a table header and confirm a
matching explanatory note still exists below the table.

**Section-selection check** — confirm the finished document contains exactly the
Header, Key Facts Banner, salutation, the sections ticked in Step 0a (scope-
restricted per Step 0b), the signed closing, and nothing else from Step 10's
structure list.

**Premium Escalation Table % check** *(if Section 3 is included)* — confirm every
insurer column with rand figures also carries a % badge on every row that has a
rand figure (Step 4), and that the footnote states which badges are printed vs.
calculated.

**Quote-version-history check** *(mandatory whenever a quote/schedule was swapped
mid-engagement)* — confirm the document never frames the current figures against
an earlier version of the same insurer's quote:

```bash
grep -n -i "previous\|no longer\|updated quote\|removed\|used to\|old quote\|not included here" output.html
```

Every match must be investigated — the document states only what the current
quote shows, never what changed from a prior version (see Step 11).

**Honesty check.** If the adviser asks directly whether the document is accurate,
give a genuinely tiered answer rather than blanket reassurance: what's directly
sourced and arithmetic-checked; what's reasonable inference applied to a gap
(stated explicitly as inference); what's sourced externally and should be
reconfirmed with the insurer; and concrete next steps to close any remaining gap.
Treat this question as an invitation to re-verify, not just to reassure.

## Companion email

Every finished comparison is accompanied by a covering email from Paul Kafentzis.
The email must:

- Open with a personal, warm acknowledgement of the client relationship.
- Where relevant, acknowledge respectfully (neither accusatory nor dismissive) if
  the client has already raised a concern this comparison addresses.
- Summarise the 4–6 most critical findings in plain-language bullet points (numbers
  only where they matter), drawn only from sections actually included, and
  restricted to the benefit categories confirmed in scope by Step 0b.
- Where one or more sides is RAR-only, state clearly that the comparison used the
  RAR and general product knowledge, not a full schedule, for that side.
- Include a direct call to action (call or WhatsApp).
- Stay concise — the email directs the client to the document, it does not
  duplicate it. Keep it brief when the adviser signals a low-pressure handoff (e.g.
  "we'll discuss next week"). Natural, non-AI-generated tone throughout; tight
  preambles — no unnecessary caveats or reconfirmation notes.
- State plainly that the document is HTML and should be opened in Google Chrome.
- Written in whichever voice was chosen in Step 0a for the document itself, so the
  email and document read consistently.
- Sign off with full contact details: Paul Kafentzis, Wealth Revolution (Pty) Ltd,
  FSP 45946, phone and email — leave as clearly-marked placeholders if not provided
  in the conversation, rather than inventing them.

This is the standing baseline for all future life cover comparisons, regardless of
how many insurers are involved.