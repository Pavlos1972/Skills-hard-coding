<!-- The live skill text as of 14/10/2026 16:29 (Athens time), kept as the rule-by-rule baseline. -->
---
name: "wr-sroa-builder"
description: "Builds a Servicing Record of Advice (SROA) PDF for Paul Kafentzis (FSP45946) comparing a client's current policy schedule with the accepted servicing quote. Use when Paul asks for an SROA or servicing record."
---

# WR SROA Builder

## Index

| Section | What it covers |
|---|---|
| Universal operating rules | Nine rules that apply to every step, and the Delivery gate (4 checks) |
| Last updated, standing rules, changelog | Athens stamp, the edit rule, four one-line rows, and the packaging rule for the installed skill |
| What an SROA is for | The three things the document records |
| Step 0 - Locate the source documents | SharePoint, OneDrive and Outlook search; several policies per client; the Fact Find labels-only problem |
| Step 1 - Which quotes were compiled and accepted | FNA, Shortfall and Alternative quotes; which one was accepted |
| Step 2 - Required source documents | Current Policy Schedule, one document per compiled quote, Fact Find Summary |
| Step 3 - Always ask | Reason for the change, investment-linked or not, client name, ID number, SROA date |
| Step 4 - Compare the two documents | Fixed line-item list, BrightRock grouped headings, R20 policy fee, CP number, the four blocks |
| Step 5 - Portfolio Changes section | A real narrative for investment-linked policies, otherwise "N/A" |
| Step 6 - Build the document | scripts/build_sroa.py, fixed formatting rules, the visual check list |
| Step 7 - Delivery | PDF only, exact filename convention, one SROA per policy |
| Reference material and scope | Schema, template, logo, build script; procedure only, no client data |

Trigger phrases: "let's do an SROA for [Name]", "servicing change for [Name]'s BrightRock policy", or a client's current Policy Schedule uploaded or mentioned alongside a Servicing Quote or an updated Policy Schedule reflecting servicing changes.

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

**Delivery gate for this skill (rules 5 and 6 applied):** a run is complete only when ALL of these are done and confirmed in one line each: (1) the source documents were located and read, and the Step 3 questions were asked, not inferred (Steps 0-3); (2) one SROA PDF was built for each policy being serviced, never combined; (3) each PDF was sent in the chat with the exact Step 7 filename; (4) each PDF was saved in the client's own folder located in Step 0 and the saved file was checked. After ANY correction, repeat (2) to (4) for every deliverable that changed.

**Last updated: 2026-10-14 16:29 (Athens time)**

> **Standing rule — not optional:** any edit to this skill (SKILL.md, the build
> script, or any reference file) is not complete until the "Last updated" line
> above is also rewritten to the current date/time in Athens/Greece time, in
> the same response as the edit. This is a required last step of every skill
> change, not a courtesy — treat a skill edit that skips it as unfinished.

## Changelog

Full original rows are archived word for word in claude/wr-sroa-builder-changelog.md.

- **2026-10-14 16:29** — Index added after the title, plain description (the trigger phrases moved to a line under the Index), client policy and CP numbers, example amounts and example client name replaced with placeholders, changelog shortened to one-line rows (Route 1 streamlining at Paul's request); no rule changed.
- **2026-10-08** — Rule 9 now names the propose_skills review card and says never claim a change is live until Paul confirms.
- **2026-10-08** — UNIVERSAL OPERATING RULES block and Delivery gate added at the top.
- **2026-09-25** — Folded in refinements confirmed with Paul in live sessions: the FNA Quote can be declined (Block 1 "not compiled"); minimal "not compiled" wording; each of Blocks 1-3 can carry its own CP number; confirm with Paul before treating a debt item as renamed vs new; Athens-time stamp. Still open: whether "Reduction Quote" becomes a formal variant term alongside "Alternative Quote".

> **Standing rule — not optional:** editing the SKILL.md file directly only
> changes this sandbox-local copy. It does **not** update the version
> installed in Settings → Capabilities → Skills, and it does **not**
> propagate to any other chat until that installed version is replaced. A
> skill edit is not complete until:
> 1. it has been packaged into a `.skill` file (`python3 -m
>    scripts.package_skill` from the `skill-creator` directory),
> 2. that `.skill` file has been delivered to the user, and
> 3. the user has been told plainly, in the same response, that they need to
>    upload it via the Skills panel to replace the installed version — never
>    described as "already live" or as needing no further action.

This skill packages Paul Kafentzis's process for completing a Servicing Record
of Advice (SROA) for Wealth Revolution clients whose existing policy is
undergoing a servicing change (as opposed to a new policy — that's the ROA
skill, `wr-roa-builder`, a different document). This is a FAIS compliance
document — a wrong comparison figure or an invented rationale is a real
compliance error, not a cosmetic slip.

## What an SROA is for

A client already has a policy in force. Something about it is being changed —
cover amounts, premium, portfolio/fund allocation, waiting period,
retrenchment cover, etc. The SROA is the advisor's documented record of:
1. Exactly what changed, line by line, versus what stayed the same.
2. Why the advisor recommended the change.
3. (Where relevant) why the underlying investment portfolio was adjusted.

## Step 0 — Locate the client's source documents in SharePoint/OneDrive/Outlook

Servicing documents almost never arrive as chat uploads — they live in the
client's existing SharePoint/OneDrive folders, and the accepted Servicing
Quote is often only in an Outlook email thread. Locate them there first; only
ask the advisor to upload something if it genuinely can't be found.

1. **Find the client's folders.** Two different SharePoint locations are
   typically involved, and they hold different things — don't assume one
   folder has everything:
   - The **Current Policy Schedule** (the "before" figures) usually lives
     under the client's Reviews folder, e.g. `Company - Paul\Reviews\[Year]\
     [Surname, First Name]\...\Policy schedules & Tax-Certificates` — often
     inside a combined "Owner's Manual" document that covers *all* of that
     client's policies at once, not just the one being serviced.
   - The **finished SROA is delivered** into the client's own Servicing
     subfolder, e.g. `Company - WR Clients\Paul Kafentzis (Client Files)\
     [Letter] - Files\[Surname, First] (CL)\[Product] - [Policy Number]\
     Servicing\` — see Step 7.
   Search both with `Microsoft 365:sharepoint_search` on the client's
   surname, and follow up with `read_resource` on the actual hit — a search
   result is only a short snippet, not the full document.
2. **Handle multiple policies per client.** One client can have more than one
   policy under service at the same time (e.g. two separate BrightRock policy
   numbers reviewed together). Each policy gets its own Current PS, its own
   accepted Servicing Quote, and — per Step 7 — its own separate SROA output.
   Confirm which policy number a given document actually belongs to before
   using it; a combined Owner's Manual covering multiple policies is not the
   same as a single-policy Policy Schedule, and figures must be pulled from
   the section for the correct policy number, never assumed to apply
   uniformly across all of a client's policies.
3. **Check Outlook for the Servicing Quote and its acceptance.** The accepted
   Servicing Quote — and the client's acceptance of it — frequently exists
   only as an email thread (e.g. a subject like "[Client] / [Insurer]
   Reduction Quotes") rather than a standalone SharePoint PDF. Search with
   `Microsoft 365:outlook_email_search` and `read_resource`. Pull the exact
   CP/proposal number and the signed/accepted date from that thread — Step 3
   needs the accepted date and Step 4 needs the CP number, and neither should
   be guessed or left for the advisor to dig up if it's already in the
   thread.
4. **Verify every Step 2 document is actually present and current** before
   building — the Current PS, a quote document for every quote type marked as
   compiled, and the Fact Find Summary. Don't silently substitute the nearest
   thing sitting in the folder — e.g. an older, pre-reduction quote, or a
   Policy Schedule dated before the servicing change actually took effect.
   Flag any gap explicitly and ask the advisor how to proceed (locate the
   right version, confirm an older one still applies, etc.) rather than
   guessing.
5. **Fact Find / KYC PDFs read via SharePoint's `read_resource` can come back
   as labels only, with none of the client's actual answers filled in.**
   This is a known failure signature — an interactive/visual answer layer
   that SharePoint's text-extraction doesn't capture — not evidence the
   document is genuinely blank. Do not conclude the Fact Find Summary is
   empty, and do not ask the advisor to manually retype their own answers.
   The fix is to ask the advisor to upload that specific PDF directly into
   the chat, where it can be rasterized page-by-page and read visually
   instead. Recognize the pattern immediately (multiple pages of field labels
   with zero filled values) rather than retrying the same SharePoint read
   with different queries first.

## Step 1 — Which quotes were compiled, and which was accepted

Always ask this first, before requesting documents — it determines exactly
what to ask for next (sourced via Step 0 wherever possible). Use
button-select questions, not free text, since these are fixed categories:

1. **Which quote types were compiled for this servicing change?**
   - **Servicing FNA Quote** — compiled for most servicing reviews, but not
     guaranteed: a client can decline an FNA entirely. Don't assume it was
     compiled just because that's the common case — ask, the same as the
     other two.
   - **Shortfall Quote** — only compiled when the client has Group Risk
     cover (it represents FNA cover minus Group Risk cover).
   - **Alternative Quote** — only compiled when affordability constrains the
     client below the Shortfall/FNA figures.
   Any combination is possible, including a case with no FNA Quote at all.
   Don't assume — ask.
2. **Which quote did the client accept?** The accepted quote is whichever
   one's figures the "Requested Servicing Change/s" block's "new" values
   must trace to — even if multiple quotes were presented to the client
   side by side, only one was accepted, and getting this wrong means the
   whole comparison is sourced from the wrong figures.

If the advisor's stated reason for the change references affordability
(e.g. "client requested a reduced quote in line with affordability"), that's
a strong signal the accepted quote is the **Alternative Quote** specifically,
not just "the quote" generically — confirm this explicitly rather than
assuming genericly which one it was.

## Step 2 — Required source documents

Always require **all** of these before starting; don't build a partial SROA.
Source them via Step 0's SharePoint/Outlook search wherever possible, and
fall back to asking the advisor to upload directly only for what genuinely
can't be found that way:

1. **Current Client Policy Schedule (PS)** — the policy as it stood before the
   change.
2. **A quote document for every quote type marked as compiled in Step 1** —
   the FNA Quote document (if compiled), the Shortfall Quote document (if
   compiled), and the Alternative Quote document (if compiled). Each
   compiled quote populates its own block (Blocks 1-3) — don't fabricate a
   quote's figures from the accepted quote's document, ask for the actual
   document for each one. If the client declined the FNA entirely, there's
   no FNA document to request — see Block 1 below.

If more than one quote type was compiled (Step 1), also ask whether the
advisor wants the non-accepted quote(s) referenced in the SROA for
completeness (e.g. noting that a Shortfall Quote was also presented) —
don't fabricate that reference without asking, and don't assume the advisor
wants it just because a second quote existed.

Also always ask for the client's **Fact Find Summary**. It isn't required to
start the comparison itself, but request it up front alongside the two
policy documents above — it gives the needs/affordability context behind the
servicing change and should be on hand before the Record of Advice narrative
is finalised. If the advisor doesn't have one to hand, ask explicitly rather
than silently proceeding without it.

Documents may arrive as PDFs or as marked-up/annotated copies. If a document
is a scan, OCR or visually inspect it rather than guessing values.

## Step 3 — Always ask (never infer or invent)

Ask these directly — do not guess or auto-generate answers for any of them:

1. **Reason for the servicing change.** There is no default sentence for
   this. Typical categories the advisor may cite: New FNA done, affordability
   review, life stage change, CPI increase, cover gap identified — but always
   ask for the actual reason in the advisor's own words for this specific
   client, and write the "Record of Advice" narrative from that answer, not a
   template.
2. **Is this an investment-linked risk policy** (e.g. BrightRock's Flexible
   Cover with an investment component)? This determines whether the
   "Portfolio Changes" section gets a real narrative or "N/A" — see Step 5.
   If yes, also ask for the reason behind any portfolio/fund allocation
   change, in light of the client's risk profile.
3. Confirm the **client's full name** as it should appear typed on the
   signature line (normally the same as the Owner field, but confirm — don't
   assume for joint or business-owned policies). Confirm the full legal name
   against source documents rather than any shortened or informal name used
   in conversation — the two can differ.
4. Confirm the **client's ID number**. This is always included on the SROA as
   a new "ID Number :" field directly under "Owner :". Never take it from
   memory or infer it — confirm it explicitly, cross-checked against the
   source policy documents.
5. **Confirm the date the SROA should be dated for.** This must always be
   asked — never default to today's date or the date of generation. It
   should align with the date the Servicing Quote (the accepted quote) was
   signed — cross-check against the signed quote document if one is
   available (e.g. a signature/acceptance date on the accepted Cover
   Proposal) and confirm that date with the advisor rather than assuming it.
   This confirmed date is what populates the `[SROA date]` in the output
   filename — see Step 7.

## Step 4 — Compare the two documents

Compare the Current PS against the Servicing Quote/updated PS across the
following line items, in this fixed order. This fixed comparison list applies
whenever the servicing change is a **Life Cover servicing change**:

1. Life Cover
2. Disability Cover
3. Dread Disease
4. Income Protection
5. Premium
6. ACI (Automatic Cover Increase — the yearly cover/base growth rate, e.g.
   BrightRock's "Yearly base increase")
7. ABI (Automatic Benefit Increase — the yearly premium growth rate, e.g.
   BrightRock's "Yearly premium increase")
8. Retrenchment Cover

Always compare ACI and ABI between the Current PS and the Servicing
Quote/updated PS, even when they haven't changed — these increase mechanisms
directly affect how cover and premium will grow going forward, so they're
part of the standard comparison, not optional detail. Source them from
whatever the insurer's document calls its yearly cover-growth and
yearly-premium-growth fields (terminology varies by insurer — confirm the
mapping with the advisor if it's ever unclear which field is which).

"Waiting Period" is deliberately not part of the fixed list — do not include
it unless the advisor specifically asks for it as a one-off item for a given
case (see the "falls outside this fixed list" rule below).

For every line item in this list that's actually part of the policy's cover
structure:
- If the value changed, record it as `"Life Cover: R[old amount] → R[new amount]"`
  style (old value, arrow, new value) — exact figures from the source
  documents, never rounded or estimated.
- If the value did **not** change, still list it explicitly as
  `"[Item]: No change"` — every applicable line item appears every time,
  changed or not.
- If a fixed-list item **isn't part of this policy's cover at all** (e.g. no
  Retrenchment Cover benefit exists on the policy, as is often the case for
  BrightRock needs-based structures), omit that line entirely rather than
  writing "No change" — "No change" implies the benefit exists and is
  unchanged, which would misstate the cover. Only ask the advisor if it's
  unclear whether a benefit is absent vs. genuinely unchanged at zero.

If a change falls outside this fixed list (e.g. a one-off change unique to a
particular product), still record it in the same "Item: old → new" or "Item:
No change" style, appended after the fixed list.

### BrightRock needs-based policies: grouped headings

BrightRock's needs-based structure (household/debt/death-related/additional
expense needs, each split into recoverable/permanent/death columns) doesn't
map cleanly onto a flat list. For these policies, use `grouped_changes`
instead of the flat `servicing_changes` list — bold section headings with
indented bullet lines underneath, in this fixed order:

1. **Life Cover** — everything "caused by death": standalone death-related
   needs, plus the death-cover portion of each debt.
2. **Lump Sum Disability Cover** — everything "permanent": household
   permanent needs, plus the permanent-cover portion of each debt.
3. **Income Protector / Sickness Benefit** — the "recoverable"/temporary
   household needs cover.
4. **Additional Expense Needs / Dread Disease** — BrightRock's Additional
   Expense Needs cover *is* its dread disease cover — in BrightRock's
   product structure these are the same benefit, not two separate ones.
   Always use this combined heading (never "Dread Disease" as its own
   separate heading, and never invent a distinct dread disease figure) and
   populate it with the policy's Additional Expense Needs figures, as-is.
5. **Policy Details** — Premium (see R20 rule below), ACI, ABI.

Debt cover items appear as their own bullet under both Life Cover and Lump
Sum Disability Cover (once for the death portion, once for the permanent
portion) — a single debt is not one bullet, it's two.

When a debt on the Current PS doesn't obviously match a debt on the new
quote — a different description, a different creditor label, a changed
amount — don't guess whether it's the same debt renamed or a genuinely new
one added at servicing. Matching amounts alone isn't enough to assume it's a
rename. Confirm with Paul which it is before writing the comparison either
way, since treating a new debt as a rename (or vice versa) would misstate
what actually changed.

This mapping is Claude's interpretation of how BrightRock's own categories
correspond to conventional risk cover terminology, not a value stated
anywhere in BrightRock's documents — confirm it with the advisor if a
mapping question arises. The Additional Expense Needs / Dread Disease
equivalence, however, is a confirmed hard rule for BrightRock policies, not
an open question — don't re-litigate it per client.

### R20 policy fee

The Premium line — whether in the flat list or under Policy Details in the
grouped layout — must always be **inclusive of the R20 monthly policy fee**.
Insurer source documents usually state this directly (e.g. BrightRock's
"Total premium (including the policy fee)" field) — use that figure rather
than doing the R20 arithmetic by hand, and label the item
`"Premium (incl. R20 policy fee)"` so it's unambiguous. `build_sroa.py`
prints a build-time warning if the Premium line doesn't look like it
mentions the fee, as a safety net — it doesn't block the build, so still
check it yourself.

### CP number

BrightRock (and similarly-structured insurers) issue each servicing quote
with its own reference/proposal number — the "CP number". When the advisor
provides one for the accepted quote, include it via the `accepted_quote_cp_number`
field: it renders as a line directly above the Requested Servicing Change/s
box, alongside the policy number (`"Policy Number: [Policy Number] | Accepted
Quote — CP Number: [CP Number]"`). The in-force Current PS is not itself a
quote and typically has no CP number of its own — leave the field out
entirely (don't write "N/A") if the advisor confirms none applies.

Each of Blocks 1-3 can carry its own CP number too, via that block's
`cp_number` field in `quote_blocks` (see the schema doc) — a compiled FNA,
Shortfall, or Alternative Quote is its own proposal with its own reference
number, separate from whichever quote was ultimately accepted. Ask for it
alongside that block's other figures whenever the advisor has it, and it
renders at the top of that block the same way the accepted quote's CP number
renders above Block 4.

### Four-block structure

Every SROA is structured as four blocks, in this fixed order:

- **Block 1 — Servicing FNA Quote.** Present in every SROA's JSON, but not
  guaranteed to be compiled — a client can decline an FNA entirely (see Step
  1). When it was compiled, shows that quote's own cover figures under the
  standard grouped headings (Life Cover, Lump Sum Disability Cover, Income
  Protector / Sickness Benefit, Additional Expense Needs / Dread Disease,
  Policy Details) — standalone figures, not an old→new comparison. When the
  client declined it, render the same short one-line treatment Blocks 2-3
  use for "not compiled" — e.g. `"Not compiled — declined by the client."` —
  never omit Block 1 entirely and never invent FNA figures that weren't
  actually produced.
- **Block 2 — Shortfall Quote.** Only present as a full grouped breakdown if
  a Shortfall Quote was actually compiled (i.e. the client has Group Risk
  cover). If not compiled, render a short one-line note instead of a full
  block. Keep it minimal — `"Not compiled for this client."` is the standard
  wording (it's also what `build_sroa.py` falls back to by default); don't
  add an elaborated explanation of why it wasn't applicable. Never omit
  Block 2 entirely, and never invent Shortfall figures.
- **Block 3 — Alternative Quote.** Same rule as Block 2: full grouped
  breakdown if compiled (affordability constrained the client below
  Shortfall/FNA figures), otherwise a one-line "not compiled" note. Title it
  `"Alternative Quote (Accepted)"` when it's also the accepted quote, since
  that's the common case.
- **Block 4 — Requested Servicing Change/s.** The Current PS → Accepted
  Quote comparison (old → new), same grouped-headings format as before.
  This is the block that was, until this structure was added, the entire
  report — it doesn't change in content, only in being labelled as Block 4
  and following Blocks 1-3.

Implemented via the `quote_blocks` field (Blocks 1-3) plus the existing
`grouped_changes`/`servicing_changes` field (Block 4) — see the schema doc
for the exact shape. Don't use the older approach of inline
`"(FNA Quote reference: ...)"` parentheticals on Block 4's bullets — Block 1
is where FNA figures belong; Block 4 stays a clean two-column old→new
comparison.

## Step 5 — Portfolio Changes section

- **Investment-linked risk policy**: write a short Record of Advice narrative
  explaining the portfolio/fund reallocation reason, in light of the client's
  risk profile — from what the advisor tells you in Step 2, point 2.
- **Any other policy** (e.g. straightforward risk-only servicing change):
  this section is always the literal text **"N/A"** — never leave it blank,
  never invent a portfolio rationale that wasn't asked for.

## Step 6 — Build the document

Use `scripts/build_sroa.py` to generate a fresh PDF (this skill always
generates a new PDF styled like the original WR template — it does not fill
the original fillable form). See `references/sroa_data_schema.md` for the
exact JSON shape the script expects, including full field-by-field notes.

```bash
python scripts/build_sroa.py data.json output.pdf
```

Key formatting rules baked into the script — don't override these by hand:
- **Financial Advisor Code and Name are always fixed**: `FSP45946` and
  `Paul Kafentzis`. Never ask for these, never take them from the source
  documents.
- **"Signed at" is removed entirely** — this SROA convention has no signing
  location field, only a date.
- **Two separate date fields, one per signatory** — the client and the
  advisor do not necessarily sign on the same day, so each gets their own
  fillable "Date :" field, positioned directly under their own signature.
  Both are real fillable PDF form fields, not static text — left blank at
  build time; filled in when signed.
- **Client name and "Paul Kafentzis" are pre-typed as static text**, printed
  directly below each signature line (this is a freshly generated PDF, not a
  document the client fills in interactively, so the names are known at
  build time and typed directly rather than left as blank fillable fields).
- **Two distinct signature lines, side by side**, each with genuine blank
  space directly above it left clear for a physical/wet signature — the
  typed name and "Signature of Owner/Authorised Signatory" or "Signature of
  Financial Advisor" caption sit below the line, never on or above it. The
  two lines are visually separated by a clear gap in the middle of the page,
  not touching or crowding each other.

After building, always render to PNG and visually check the page before
delivering — box heights auto-size to their text, but very long content can
still push the page taller than expected, so confirm nothing overlaps or
gets crowded:

```bash
pdftoppm -png -r 120 output.pdf /tmp/sroa_check
```

View `/tmp/sroa_check-1.png` and confirm:
- The WR logo appears top-left, doesn't overlap the title, and isn't the
  faded circular watermark variant.
- The "ID Number :" field appears directly under "Owner :" and shows the
  correct ID number.
- All fixed line items that genuinely apply to this policy's cover structure
  appear (with "No change" where applicable) — and no item is shown for a
  benefit that doesn't exist on this policy (e.g. no "Retrenchment Cover:
  No change" line on a policy with no retrenchment benefit). For BrightRock
  policies using `grouped_changes`, all five headings appear in order
  (Life Cover, Lump Sum Disability Cover, Income Protector / Sickness
  Benefit, Additional Expense Needs / Dread Disease, Policy Details), each
  with its bullets fully visible (not cut off mid-list).
- The Premium line reads "Premium (incl. R20 policy fee)" and the figures
  actually include it.
- If a CP number was provided, it appears directly above the Requested
  Servicing Change/s box alongside the policy number.
- Neither narrative box is visibly truncated.
- Portfolio Changes shows either a real narrative or "N/A" — never blank.
- Date field renders as an empty box (not pre-filled).
- **Two separate date fields are present**, one under each signature — not a
  single shared date field.
- Two distinct signature lines are visible side by side, clearly separated,
  each with blank space above it (not text sitting on the line itself), and
  the correct typed name and caption below each line.
- Financial Advisor block shows Code: FSP45946, Name: Paul Kafentzis, and is
  fully visible — not clipped or cut off at the bottom of the page. Long
  content (e.g. a 9-10 line item BrightRock comparison) may legitimately push
  the signature block onto a second page; check that page too if so, and
  confirm nothing is missing or overlapping.

## Step 7 — Delivery

- **Output**: a standalone PDF only — no covering email for this document
  type (unlike some of the other WR proposal skills).
- **Filename** (uniform convention for every SROA, no exceptions):
  `SROA - [Insurer]_[Policy Number] - [SROA date] - ([First name]_[Surname]).pdf`
  - `[Insurer]_[Policy Number]` — underscore between insurer and policy
    number, no spaces around the underscore.
  - `[SROA date]` is the date confirmed in Step 3, point 5 — the date this
    SROA should be dated for, aligned with when the Servicing Quote (the
    accepted quote) was signed. Always ask for and confirm this date with
    the advisor rather than defaulting to today's date or the date of
    generation — never assume the two are the same. Format as `DD.MM.YY`
    (dots, not hyphens). It is not a signature date — those are left blank
    for the client/advisor to fill in.
  - `([First name]_[Surname])` — underscore between first name and surname,
    in parentheses. Uses the client's everyday first name and surname, not
    the full legal name with middle names (that full legal name still
    belongs in the `owner` field inside the document itself).
  - Illustrative shape only (do not reuse this literal date):
    `SROA - BrightRock_[Policy Number] - [DD.MM.YY] - ([First name]_[Surname]).pdf`
- **One SROA per policy.** If a client has multiple policies being serviced
  in the same session, build a separate SROA (and separate output file) for
  each policy — never combine multiple policy numbers into one document.

## Reference material

- `references/sroa_data_schema.md` — exact JSON schema for
  `build_sroa.py`, plus the render/inspect commands to run before
  delivering.
- `assets/WR_Generic_Servicing_Record_of_Advice.pdf` — the original WR
  template this skill's output is styled after (layout reference only; the
  build script does not fill this file directly).
- `assets/WR_Logo.png` — the WR logo, cropped to exclude the faint circular
  watermark variant present in the original upload. Drawn at the top-left of
  every generated SROA by `build_sroa.py`. If this file is ever missing, the
  script falls back to a plain text header rather than failing outright —
  but always keep this asset in place for real deliverables.
- `scripts/build_sroa.py` — the validated construction script. Extend this
  (and update this file) rather than hand-editing PDF bytes for a one-off
  case.

## A note on scope

This skill is about the *procedure*. It doesn't carry any specific client's
data — each SROA should start from that client's own documents (Current
Policy Schedule, Servicing Quote/updated PS, Fact Find Summary), located via
the Step 0 SharePoint/OneDrive/Outlook search or, failing that, uploaded
directly into the conversation, plus the reason the advisor gives in Step 2.
If a new client's documents can't be found either way, ask for them per Step
1/Step 2 rather than reusing figures or wording from an earlier client in the
same chat or from memory of a previous session.