---
name: "investment-comparisons-skill"
description: "Builds client-facing comparisons of two or more providers' RA, Tax-Free, Endowment or Living Annuity quotes for Paul (FSP45946), using actual fees, not EAC. Use when asked to compare investment quotes."
---

# Investment Comparisons Skill

## Index

| # | Section | What it covers |
|---|---|---|
| 1 | Universal operating rules + Delivery gate | The nine rules for every step, and what must be done before a run counts as complete |
| 2 | Last updated + Changelog | Athens-time stamp, last changes, standing edit note |
| 3 | Core principles | Actual cost not EAC; plain English, not adviser jargon |
| 4 | Step 0 | Setup questions to run before building |
| 5 | Step 1 | Apples-to-apples checks |
| 6 | Step 2 | Every fee as a separate line item (Total Ongoing Fees table) |
| 7 | Step 3 | Boosters / loyalty bonuses, kept compact |
| 8 | Step 4 | Fund choice, risk alignment, live fund fact sheet research |
| 9 | Step 5 / 6 / 6a | Flexibility and terms; tax treatment; supplementary document conflicts |
| 10 | Step 7 | The four-table output structure |
| 11 | Step 8 | Pre-delivery check |

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

**Delivery gate for this skill (rules 5 and 6 applied):** a run is complete only when ALL of these are done and confirmed in one line each: (1) every applicable Step 0 setup question was answered by Paul before building started, and the apples-to-apples check (Step 1) was done; (2) the fees (Step 2), fund fact-sheet research (Step 4) and any Step 6a document conflicts were sourced and checked, nothing estimated or carried over from another client; (3) the client-facing comparison was built in the Step 7 structure (the four tables, unless Paul said otherwise); (4) the Step 8 pre-delivery check was completed item by item; (5) the finished comparison was handed to Paul in the chat. After ANY correction, repeat (2) to (5) for every part that changed.


**Last updated: 2026-10-14 15:07 Athens time (EEST)**

> **Standing rule — not optional:** any edit to this skill is not complete until the
> "Last updated" line above is also rewritten to the current Athens/Greece date-time,
> in the same response as the edit, and a line is added to the Changelog below.

## Changelog

Full history (word for word) is in the Project doc `investment-comparisons-skill-changelog.md`.

- **2026-10-14 (15:07)** — Index added; description made plain (its skill-boundary and example text moved into a "Not for" line in the body); changelog archived word for word. No rule changed.
- **2026-10-08 (14:38)** — Rule 9 reworded: skill changes go forward with the propose_skills review card; never claim live until the user confirms they saved.
- **2026-10-08 (14:10)** — Universal operating rules block and Delivery gate added at the top.
- **2026-09-23 (11:52)** — Cross-references renamed to `life-insurer-comparison`; Last-updated stamp switched to Athens time and Changelog added.

This skill builds client-facing comparisons between two or more investment
providers' quotes for the same product type (RA vs RA, TFSA vs TFSA, endowment
vs endowment, living annuity vs living annuity — never across product types).
The output is a client-facing document plus, if requested, a covering email,
following the same visual/tone conventions as `life-insurer-comparison` unless
told otherwise.

**Not for:** life/risk cover (use `life-insurer-comparison`), or a single provider's proposal (use `om-optimal-ra-proposal`, `om-tax-free-skill` or `rgar-skill`). Use this skill when two or more providers' investment quotes (RA, TFSA, endowment, living annuity) are being weighed against each other, e.g. Old Mutual vs Sanlam, Sanlam vs Momentum, Old Mutual vs Allan Gray.

**Core principle: actual cost, not EAC.** Every comparison in this skill breaks
fees into their real Rand and percentage line items at the client's actual
contribution/investment level. EAC (Effective Annual Cost) is never used as the
headline cost figure — it blends several different fee types into one number and
hides which specific line is driving the cost. If a source quote only shows EAC
and not the underlying fee breakdown, flag this to the adviser and ask for the
fee schedule/fund fact sheet that shows the components — do not back-calculate
or estimate a breakdown from an EAC figure.

**Core principle: plain English throughout, not adviser jargon.** The document
is written for the client to actually read and understand, not as an internal
compliance artefact. Every table, footnote, and explanatory note uses everyday
language:

- Industry shorthand (TER, TIC, EAC, "as-and-when commission," "payment layer,"
  "fund-based fee") is either replaced with a plain description or explained in
  parentheses the first time it appears — never left to stand alone as if the
  client already knows it.
- A short intro line sits above each table explaining what it shows and why it
  matters, in one or two plain sentences — not a section heading with no framing.
- Fee rows are labelled by what they're actually for ("Admin fee — for running
  the plan day-to-day") rather than just the provider's internal term.
- Numbers stay exact and are never rounded away, but the words wrapped around
  them are simple, short sentences — favour "this rate drops as the fund grows"
  over "this is a tiered fee structure subject to banded reduction."
- Any mechanism that isn't self-explanatory from a single sentence (see Step 3
  below on boosters/bonuses) gets its own short, plain-language explanation
  block before the numbers are shown, not just a table row.

## Step 0 — Always run the setup questions first

Before building anything, confirm the items below are available. Item 1 and
item 2 are derived directly from the uploaded quotes, not asked — only fall
back to asking if the quotes genuinely don't state them. Everything else, ask
for and wait if missing — do not build a partial comparison on assumed or
missing information.

**About the client and product — derive, don't ask**

1. **Client full name** — read directly off the uploaded quote/illustration
   documents (every quote states the client's name). Only ask if it's genuinely
   unclear or the quotes disagree with each other.
2. **Product type being compared** — RA, TFSA, Endowment, or Living Annuity —
   also read directly off the quotes (every quote states its own product type).
   Must be the same type across every quote (see Step 1); if the quotes show
   different product types, flag this rather than asking the adviser to
   pre-confirm it.

**About the client — ask**

3. Client's risk profile, from the Fact Find (needed to check fund alignment
   in Step 4). Ask the adviser if it isn't already available in this
   conversation.

**About the quotes being compared**

4. **The actual quote/illustration document for every provider being
   compared**, uploaded in full — not a summary email or a single screenshot
   of one page. Each quote must show, at minimum: premium/contribution amount,
   escalation, term/retirement age, fund(s) selected, and the full fee
   disclosure (asset management fee, administration fee, advice fee, any
   commission) — not only a blended EAC figure. If a quote only shows EAC and
   no fee breakdown, flag this back to the adviser and ask for the fee
   schedule or fund fact sheet that shows the components.
5. Confirmation that all quotes are for the **same contribution
   amount/structure** (recurring premium vs recurring premium, lump sum vs
   lump sum) — if they aren't, say so up front rather than discovering it
   partway through building the fee table. This can usually also be read
   directly off the quotes; only ask if it's ambiguous.
6. Confirmation of whether a **lump sum** forms part of any of the quotes, and
   if so, whether it's a Section 14 transfer or voluntary funds (affects
   whether a separate lump sum quote is also needed). Also usually readable
   off the quotes; only ask if unclear.

**About the output**

7. Whether the adviser wants the standard four-table document only (see
   Step 8), or wants any of the optional extras added (apples-to-apples flag
   section, tax treatment note, flexibility/terms detail, or a verdict/"Why
   [Provider]" section).
8. Whether a covering client email is also needed alongside the document.

Items 1 and 2 are derived from the quotes automatically. Item 4 is always
mandatory and must be actively obtained if missing. Items 3, 5, 6, 7, and 8 are
confirmed where applicable — either read off the quotes where possible, or
asked — but never silently skipped.

## Step 1 — Confirm apples-to-apples before comparing anything

Do not build a comparison table until all of the following match across every
quote being compared:

- **Same product type.** RA vs RA, TFSA vs TFSA, endowment vs endowment, living
  annuity vs living annuity. Never compare an RA against a preservation fund or
  a TFSA against a discretionary investment — the tax treatment alone makes the
  comparison misleading.
- **Same contribution structure.** Recurring premium vs recurring premium, lump
  sum vs lump sum. If one quote is a lump sum and the other a recurring premium,
  say so explicitly and do not force them into the same fee table.
- **Same term/retirement age assumption**, where the product is term-dependent.
- **Same investment amount.** Admin/platform fees are usually tiered by Rand
  value — if the quotes were generated at different investment amounts, the
  fee percentages are not directly comparable. Either request quotes at the same
  amount, or clearly label the mismatch in the output rather than silently
  comparing tiered percentages side by side.

If any of these don't match and can't be resolved by asking the adviser, say so
and do not proceed with a table that implies a false equivalence.

## Step 2 — Extract every fee as a separate line item

Read each provider's actual quote/fee schedule (not a marketing brochure) and
pull out these components individually. Never accept a single blended cost
figure as a substitute for this breakdown.

**Standard output format — "Total Ongoing Fees – Per Annum (Excluding EAC)".**
Confirmed against a real Sanlam quote's own fee disclosure table, so this is the
default layout for every future comparison unless the source quotes present fees
differently:

| Fee Component | Provider A | Provider B | ... |
|---|---|---|---|
| Asset management fee | x.xxx% | x.xxx% | |
| Net administration fee | x.xxx% | x.xxx% | |
| Ongoing advice fee | x.xxx% | x.xxx% | |
| Adviser remuneration account charge | x.xxx% | x.xxx% | |
| **Total ongoing fees** | **x.xxx% p.a.** | **x.xxx% p.a.** | |

Notes on populating this table:

- **"Net administration fee" is the line most likely to be doing quiet, heavy
  lifting** — it has appeared as low as ~0.5% and as high as ~3% between
  providers in practice. Never assume it's a minor line; always pull the actual
  figure from the quote's fee disclosure section.
- Use the source quote's own fee category labels where they map cleanly onto
  the four rows above. If a provider's quote uses different category names or
  splits fees differently (e.g. separate initial vs ongoing platform fees, or a
  standalone fund manager TER not folded into "asset management fee"), keep the
  source's own line items rather than forcing them into these four labels —
  fidelity to the actual quote always wins over a tidy template.
- **Performance fees**, where present on a specific fund, are flagged as an
  additional line below the table (not folded into the total) since they're
  variable and fund-specific, not a fixed annual charge.
- **Initial fees** (once-off advice/admin fees, initial commission) are shown
  separately, in the summary comparison table (Step 8, item 1) — not mixed into
  this ongoing-fee-per-annum table.
- Where useful for the client, an actual Rand-per-month conversion at their real
  contribution level can be added as a secondary column — but the % breakdown
  above is the primary, required output, not optional narrative.

## Step 3 — Boosters / loyalty bonuses (keep this compact, not the headline)

Following the same discipline as `life-insurer-comparison`'s treatment of
loyalty features: booster/bonus mechanisms (e.g. OM boosters, Sanlam Wealth
Bonus, Momentum loyalty bonus) are a minor, secondary factor — not the reason to
recommend one provider over another. For each provider, note in one line:

- What triggers it (term completed, no missed premiums, minimum investment period)
- Whether it's contractually guaranteed or discretionary/marketing
- When it pays out (maturity/retirement only, vs periodic)

Do not let the comparison's banner, verdict, or opening paragraph lead with a
booster/bonus Rand figure. The real anchor is the fee comparison from Step 2 and
the fund/risk alignment in Step 4.

**If a mechanism can't be understood from one line, give it its own plain-language
explanation block before the table, not just a table row.** A percentage or
Rand figure on its own doesn't tell the client how the mechanism actually
behaves. Worked example — Sanlam's Wealth Bonus shows two different percentages
(a rate on the client's first contribution, and a lower blended average across
every subsequent escalation), and a client reading only the numbers has no way
to know why they differ or which one actually applies to their outcome. Before
presenting numbers like this, explain in plain terms:

- **How the mechanism actually works mechanically** (e.g. "nothing is added
  along the way — instead, one bonus is promised at the end, and it only pays
  out when the plan ends").
- **Why more than one percentage might be quoted for the same benefit**, if
  that's the case (e.g. each annual contribution increase is treated as a new
  slice of money that starts building its own bonus from scratch, so a rate on
  the very first contribution and a blended average across all contributions
  are genuinely different numbers, not a typo or a range).
- **What the mechanism is actually compensating for, if the source document
  says so.** If a provider's own quote describes a bonus as offsetting a
  specific fee (e.g. "the function of the Wealth Bonus is to reduce the effect
  of the marketing and administration charge"), say this plainly — it reframes
  a headline bonus percentage as a partial refund of an already-priced-in cost,
  not pure additional value, and the client should know that distinction.
- **How it compares in shape, not just size, to the other providers' loyalty
  mechanisms** — e.g. paid periodically and resilient to a paused contribution,
  versus paid once at the end and dependent on staying the full course.

## Step 4 — Fund choice & risk alignment, with live fund fact sheet research

- Confirm the proposed fund(s) on each quote match the client's risk profile as
  recorded in their Fact Find — never assume the adviser's fund choice is
  automatically aligned without checking.
- Note fund range breadth: is the client restricted to that provider's own house
  funds, or does the platform offer open-architecture access.

**Mandatory: for every fund actually named on an uploaded investment quote,
search online and pull its current fact sheet before building the Investment
Fund Comparison table.** Never estimate, recall from memory, or reuse figures
from a previous client's comparison — fund performance, benchmarks, and target
returns change every time a fact sheet is reissued (usually monthly/quarterly),
so a figure that was correct last month may already be stale.

For each fund, source and record:

- **Benchmark** — the fund's stated benchmark (e.g. STeFI Composite, CPI,
  ASISA category average, a blended benchmark). Use the fact sheet's own
  wording, don't paraphrase into a different benchmark name.
- **Target/objective** — usually expressed as ACI (average comparable
  inflation) or CPI **+ 4–5%**, or whatever the fund's own stated return
  objective actually is. Use the fact sheet's exact stated target — do not
  default to "+4-5%" if the fact sheet states a different figure.
- **Performance — 1 year, 3 years, 5 years** — annualised, and net of fees
  where the fact sheet distinguishes gross vs net. Note the fact sheet's "as at"
  date directly under the table (e.g. "Fund data as at 30 June 2026") so the
  client knows exactly how current the figures are.
- **One-line description** — a single plain-language sentence on the fund's
  strategy/mandate (e.g. "A moderate-risk balanced fund investing across
  equities, bonds, and cash to deliver inflation-beating growth"). Written in
  your own words from the fact sheet's stated mandate — never copied verbatim
  (see copyright handling below), and never longer than one line — this is for
  a client audience, not a technical fund analysis.

**Sourcing discipline:**

- Search for the fund's name plus "fact sheet" (e.g. "Old Mutual Albaraka
  Balanced Fund B1 fact sheet") and fetch the provider's or a recognised
  fund-data platform's (e.g. Morningstar, ProfileData) most recent version.
- If a fund can't be found, or the fact sheet is clearly outdated (e.g. more
  than one quarter stale with no more recent version available), say so
  explicitly in the document rather than silently leaving a blank cell or
  guessing a figure.
- Never quote fact sheet wording verbatim beyond a few words — paraphrase
  performance commentary and fund descriptions in your own words, per standard
  copyright handling for any web-sourced content.
- If two funds are blended in a proposal (e.g. "50% Fund X + 50% Fund Y"),
  research and report each fund individually — do not average or blend the
  benchmark/target/performance figures yourself.

- Do not use past fund performance as the primary differentiator in the overall
  comparison's conclusion. It's useful, sourced supporting context in this
  table — never the headline of the document, and never a substitute for the
  fee comparison as the main cost-driven anchor.

## Step 5 — Flexibility & contract terms

- Can contributions be increased, decreased, or paused without penalty.
- Transfer-out terms: Section 14 friction, exit penalties on older-style
  (non-LISP) contracts.
- Ad hoc/additional lump sum contribution allowance.

## Step 6 — Tax treatment (state explicitly, don't let it imply a fake advantage)

- **RA comparisons:** tax deductibility (27.5% of remuneration, capped at the
  current SARS annual limit) is identical in law across every provider. State
  this explicitly in the document so the client doesn't infer that one
  provider's RA is "more tax efficient" than another's — the deduction is a
  function of SARS rules, not the product.
- **TFSA comparisons:** confirm the client's remaining annual (R36,000) and
  lifetime (R500,000) contribution limits against what each quote proposes, and
  flag clearly if a quote would push the client over either limit. Source the
  client's already-used contributions from their Fact Find or existing TFSA
  statements — never assume the limit is untouched without checking.

## Step 6a — When a supplementary document disagrees with the formal quote

A provider sometimes supplies a second document after the formal quote — a
booster/growth illustrator, a projection tool, an updated benefit statement —
that uses different assumptions (a different booster %, different fee bands, a
different fund split) to the original quote. Treat this as new information to
reconcile, not as an automatic replacement:

- **Never silently merge the two.** Don't quietly swap the formal quote's
  figures for the supplementary document's figures in Table 1/2, and don't
  quietly average them. Add the supplementary document's content (e.g. a
  projected-value table) as its own clearly-sourced addition, and flag the
  numeric disagreement explicitly in the document's opening notes.
- **Name the specific discrepancies**, not just "these documents differ" — e.g.
  "this projection shows a 3.50% booster, the formal quote states 2.5%" — so
  the adviser can see exactly what to query with the provider.
- **Note if the supplementary document's underlying assumptions differ**, e.g.
  a single-fund allocation shown where the actual quote split contributions
  across two funds — this changes what the projected values actually represent.
- **Attribute every added figure to its source document by name and date** (e.g.
  "Source: Old Mutual's Booster Illustrator, dated 06/07/2026") so the client
  and adviser can see it's not from the formal quote already cited elsewhere.
- Recommend the adviser confirm with the provider which figures are current
  before the client relies on the supplementary document's projections.

## Step 7 — Structure the output

Unless told otherwise, the client-facing document is always built as **four
short tables, in this fixed order** — confirmed with the adviser as the simple,
understandable default. No extra narrative sections bolted between them unless
specifically requested:

1. **Retirement Annuity Comparison** (or TFSA/Endowment/Living Annuity
   Comparison, as applicable) — the summary table: premium, escalation,
   retirement age, investment fund, initial commission, ongoing commission.
   This is the client's first orientation to the comparison — keep it short,
   one row per feature, no EAC row.
2. **Total Ongoing Fees – Per Annum (Excluding EAC)** — the Step 2 fee
   breakdown table. This is the visual and analytical anchor of the whole
   document; it carries the real cost story and should not be shortened or
   buried lower in the document.
3. **Investment Fund Comparison** — one row per fund (not per provider, if a
   provider proposes more than one fund), showing: Fund Name, Benchmark,
   Target/Objective (e.g. ACI/CPI + 4–5%, per the fact sheet), 1 Year
   Performance, 3 Year Performance, 5 Year Performance, and a one-line
   description. All performance data sourced live per Step 4 — include the
   fact sheet "as at" date once, directly under the table, rather than
   repeating it in every cell. Fund structure/allocation/Regulation 28 detail
   from earlier versions of this table can still be included as a compact
   second sub-table underneath if the adviser wants it, but the performance
   table is the default, required version of this section now.
4. **Loyalty and Value-Add Benefits** — loyalty benefit and additional rewards
   only (Step 3 content). Keep this table small — two or three rows per
   provider, not a paragraph per provider.

Apples-to-apples flags (Step 1), tax treatment notes (Step 6), and any
flexibility/terms detail (Step 5) are included only if the adviser asks for
them (see Step 0, item 7) or if something genuinely needs flagging (e.g. a
mismatched investment amount, or a TFSA quote that would breach a contribution
limit) — otherwise the four tables above are the complete, simple deliverable.
A verdict/"Why [Provider]" section is only added if the adviser explicitly asks
for one, and if added it must be grounded in the actual fee-total difference
from table 2, never in EAC, past fund performance, or the loyalty bonus figure
alone.

Match the client-facing visual system (colour conventions, section framing,
tone) already established in `life-insurer-comparison`, unless the adviser
specifies a different format for this particular comparison.

## Step 8 — Pre-delivery check

Before sending anything to the adviser:

- All applicable Step 0 setup questions were actually answered before building
  started — none assumed, defaulted, or silently skipped.
- Every fee figure traces to an actual quote/fee schedule/fund fact sheet — none
  estimated, backed out of an EAC figure, or carried over from a previous
  client's comparison.
- Every fund's benchmark, target, and 1/3/5-year performance figures were
  sourced live from that fund's current fact sheet for this specific
  comparison — none reused from a previous client's document or recalled from
  memory. The fact sheet "as at" date is shown in the document.
- No EAC figure appears anywhere as a standalone headline cost.
- The apples-to-apples confirmation (Step 1) genuinely holds for the comparison
  as built — if a mismatch was flagged, it's still visible in the final
  document, not quietly dropped during formatting.
- Booster/bonus content stays proportionate (Step 3) and doesn't dominate the
  verdict.
- Tax wording doesn't imply one provider has a legal tax advantage over another
  on an RA comparison.
- Every table has a short plain-language intro line, and every industry term
  (TER, TIC, EAC, commission types, etc.) is either avoided or explained in
  plain words the first time it appears — read the document as if seeing it
  for the first time with no financial background.
- Any booster/bonus mechanism with more than one quoted percentage, or that
  isn't self-explanatory from a single line, has its own plain-language
  explanation block before the numbers, per Step 3.
- If a supplementary document (illustrator, projection tool, updated statement)
  was used alongside the formal quote, any numeric disagreement between the two
  is named explicitly and sourced by document name/date, not silently merged.