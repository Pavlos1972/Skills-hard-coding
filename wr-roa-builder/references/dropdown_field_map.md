Contents: the risk profile list, the per-section fields (status, insurers, products), Need Identified by section, the Health Care section, the document-level fields, the 81-item master product list, and how the lists were verified.

# ROA Template — Dropdown Field Map (verified from ROA_Template_2026.docx XML)

This is the exact, verified inventory of every native Word dropdown (content control)
field in `assets/ROA_Template_2026.docx`, extracted directly from the document's
`document.xml`. Do not guess at options — this list is authoritative. If the template
is ever updated, re-extract with the method in "How this was verified" below before
trusting this file again.

Document order, top to bottom: **Risk Profile → Death → Disability → Sickness/Income
Protector (1st 24 months) → Income Protector (After 24 months) → Dread → Retirement →
Investment → Health Care → Policy Replacement → Author**.

## Risk Profile (top of document)
Options: Choose an item. / Conservative / Moderately Conservative / **Moderate** /
Moderately Aggressive / Aggressive
(No fixed default — source from the client's actual risk questionnaire result, unlike
the OM RA proposal skill where risk profile is always fixed to Moderate. Confirm
per-client with the adviser if not otherwise evidenced.)

## Per-section fields (repeats for each of the 7 product sections below)

Each product section (except Health Care) has this same field set:
- **Status**: Choose an item. / CRITICAL / HIGH IMPORTANCE / IMPORTANT / REVIEW LATER /
  COULD NOT REVIEW / NOT LICENSED / ADEQUATELY COVERED / **DO NOT REVIEW**
- **Need Identified**: section-specific list, see below
- **Insurers Considered** — three separate dropdown slots, each using the same list:
  ALTRISK / CAPITAL LEGACY / DISCOVERY / MOMENTUM / LIBERTY / SANLAM / OLD MUTUAL /
  BRIGHTROCK / STANLIB
  (A "." option also exists in the raw dropdown — this is a template error and must
  never be selected. Minimum 1 of the 3 slots must be filled per section that is
  actively being reviewed; use only as many as were genuinely considered — never pad.)
- **Recommended Insurer** — same 9-option list as above (one slot only)
- **Insurer not in the 9-option list (e.g. Ninety-One, Allan Gray, Coronation)**: the
  field is a native content control, so it can still hold arbitrary text — write the
  insurer name directly via the same text-override technique used for Need Identified
  overrides (`set_sdt_plain_text(..., strip_databinding=True)`), rather than forcing a
  selection from the fixed list or leaving it blank. Use the insurer's correct display
  form (e.g. "NINETY-ONE", all caps to match the existing list's style). Flag this to
  Paul at build time so it's a deliberate choice, not a silent guess — this is a
  template gap (the dropdown list has never been extended past the original 9), not a
  data-entry error.
- **Recommendation for Identified Need — same gap applies**: the 81-item Master
  Product List below has no Ninety-One (or Allan Gray/Coronation) entries either —
  it's overwhelmingly BrightRock/Old Mutual/Sanlam/etc. skewed. Same fix: override the
  field's text directly with "[Provider] - [Product Name]" in the same style as the
  existing list entries (e.g. "Ninety-One - Tax-Free Investment Plan"), rather than
  picking the nearest listed product.
- **Recommendation for Identified Need** — one shared master list of 81 named products
  across all insurers (full list in "Master Product List" below)

### Need Identified — by section
- **Death**: pass away / key person / Estate Duties / children's education
- **Lump Sum Disability**: Sickness and/or Income Protection Cover / Lump Sum
  Disability Cover / Retrenchment Cover
- **Sickness Benefit OR Income Protector (1st 24 months)**: same 3 options as Disability
- **Income Protector (After 24 months)**: same 3 options as Disability
- **Dread Disease**: only one real option — "Comprehensive Severe Illness"
- **Retirement**: preserve / Retirement Annuity / retirement — **none of these three
  dropdown options are actually used.** Need Identified is hardcoded to "Retirement
  Planning" (optionally "Saving for Retirement" as an alternate wording), the same
  override technique as Death → "Life Cover" — this is a direct text override, not a
  dropdown selection.
- **Investment**: child's education / defined need — **neither of these dropdown
  options is actually used either.** Need Identified is hardcoded to one of two
  fixed values, asked per client: "Children Education Planning" or "General
  Investment Planning".

## Health Care section
Has a **Status** dropdown only (same 9-option list as above), defaulting to
"DO NOT REVIEW". No Need Identified, Insurer, or Product dropdowns exist for this
section. Per standing instruction, an ROA is never produced for Health Care — leave
this Status field untouched at its default.

## Document-level fields (not per-section)
- **Policy Replacement**: replace / not replace
- **Financial Planner (author)**: PAUL KAFENTZIS / GARETH SAFFY — **always select
  PAUL KAFENTZIS**, never Gareth Saffy, regardless of client.

## Master Product List (81 items — "Recommendation for Identified Need")
Shared across every section's product dropdown. Select the specific product that
matches the insurer and cover type recommended for that need.

Altrisk - Comprehensive Disability
Altrisk - Comprehensive Critical Illness
Altrisk - Life Cover
Brightrock - Cover for illnesses or injuries with a financial impact that's permanent (Disability)
Brightrock - Cover for Childcare needs
Brightrock - Cover for an illness or injury with a financial impact caused by death (Life)
Brightrock - Cover for additional expense needs (Dread Disease)
Brightrock - Cover for an illness or injury with a financial impact that you can recover from (Temporary Sickness)
Capital Legacy Plan – Core
Capital Legacy Plan - Extended Immediate Liquidity Benefit
Capital Legacy Plan - Family Funeral Benefit
Capital Legacy Plan - Parent Funeral Benefit
Capital Legacy Plan - Retrenchment Protection Benefit
Discovery - Comprehensive Plus Capital Disability Benefit
Discovery - Comprehensive Plus Severe Illness Benefit
Discovery - Core Flexible Investment Plan
Discovery - Endowment Plan
Discovery - Global Education Protector
Discovery - Income Continuation Benefit
Discovery - Life Cover
Discovery - Life Time Plus Capital Disability
Discovery - Life Time Plus Capital Disability - Pays 200%
Discovery - Life Time Plus Severe Illness Benefit
Discovery - Life Time Plus Severe Illness Benefit with Extender
Discovery - Overhead Expense Benefit
Discovery - Retirement Optimiser
Discovery - Temporary Income Continuation Benefit
Liberty - Income Protector: Comprehensive Layer / Retrenchment Protector
Liberty - Absolute Protector
Liberty - Capital Disability (OOD/OD)
Liberty – Educator
Liberty - Evolve Investment
Liberty - Evolve Provident Fund Preserver
Liberty - Funeral Benefit
Liberty - Guaranteed Investment Plan
Liberty - Income Protector: Core Layer
Liberty - Income Protector: Extended Layer
Liberty - Investment Builder
Liberty - Life Cover
Liberty - Living Lifestyle Plus (WOL) / Top-Up & Extended
Liberty - Premium Protector / Disability
Liberty - Renewable Life Cover
Liberty - Retirement Annuity
Liberty - The Gateway Investment Plan
Momentum - Business Overheads Protector
Momentum - Comprehensive Critical Illness Plus Benefit
Momentum - Comprehensive Disability Benefit
Momentum - Education Protector for Death and Disability
Momentum - Elevated Comprehensive Critical Illness Plus Benefit
Momentum - Funeral Benefit
Momentum - Income Protector: Core
Momentum - Income Protector: Extended
Momentum - Life Cover
Old Mutual - Comprehensive Disability (Own) Benefit
Old Mutual - Extensive Illness Plus Benefit
Old Mutual - Life Cover
Old Mutual - Max Investment
Old Mutual - Severe Illness Plus Comprehensive Benefit
Old Mutual - Temporary Income Benefit: Core
Old Mutual - Temporary Income Benefit: Extended
One Third Lump Sum Pay Out
Sanlam - Cumulus Echo Provident Preserver
Sanlam - Cumulus R.A.
Sanlam - Disability Income
Sanlam - Extended Disability Income
Sanlam - Functional Impairment Plus Disability for regular occupation
Sanlam - Future Cover Comprehensive
Sanlam - Glacier Investment Plan
Sanlam - Glacier Living Annuity
Sanlam - Life Cover
Sanlam - R.A. (Cumulus Echo)
Sanlam - Sickness Benefit (1 month waiting)
Sanlam - Sickness Benefit (7 day waiting)
Sanlam - Stratus Endowment.
Sanlam - Tax Free Investment
Sanlam - Temporary Disability Income
Sanlam - Unit Trusts
Sanlam - Whole of Life Comprehensive Dread Disease
Stanlib - Classic Investment
Stanlib - Classic Pension Preservation Fund

## How this was verified
Extracted directly from `document.xml` inside the unzipped `.docx` using lxml,
walking every `<w:sdt>` element and reading `<w:dropDownList>/<w:listItem
w:displayText="...">` values — not inferred from the flattened text export. If the
template changes, re-run this extraction rather than editing the option lists by hand
from memory.
