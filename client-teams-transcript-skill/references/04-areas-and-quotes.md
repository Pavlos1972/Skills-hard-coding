## Step 3: The planning areas (structure of BOTH outputs)

Paul looks at eight areas. Each is its own heading, in this order, in BOTH outputs:

1. **Risk** - life, severe illness/dread disease, disability, income protection, retrenchment/instalment protectors.
2. **RA** - retirement annuities, pension/provident: the quotes, acceptances and status.
3. **Investment** - tax-free, endowments, unit trusts, savings.
4. **RGAR** - the retirement goal analysis (RGAR): what it showed and what is outstanding.
5. **EGAR** - the EGAR: what it showed and what is outstanding.
6. **Medical Aid**
7. **Will**
8. **Short-Term** - short-term insurance.

**Other** (debt, children, health, risk tolerance, general client information) is not one of the eight: show it only when something notable was said.

Show only areas that were discussed or still have something open; the program adds one line naming the rest. Never pad. The content.json `areas` keys are `risk`, `ra`, `investment`, `rgar`, `egar`, `medical`, `will`, `short_term`, `other`.

**This structure applies to a first/Fact Find meeting's Planner note exactly as it applies to a follow-up's** - map the Fact Find's own content into these headings rather than any other grouping.

## Step 4: Quote rules

- When a quote is discussed, name it once: **insurer, quote type, CP/quote number, premium**. Match what was said on the call against the quote register and the Overview; if two quotes could fit, say which one and why, and flag it.
- Non-CP quotes: use the quote number printed on the quote; if none exists, state "no quote number on file". **At a first/Fact Find meeting a quote/FNA is often only just being requested, with no number yet** - say "requested" and name the insurer/product.
- **Do not report quotes line by line** - but a benefit specifically discussed must be explained in one short bullet (Step 4c).
- **Acceptance:**
  - **Risk policy:** verbal acceptance in the Teams call is the acceptance.
  - **RA / Investment / Tax-Free:** verbal confirmation AND a reply to the proposal email. Record `Verbally confirmed - awaiting email reply to proposal` until seen.
  - Anything the client wants to think about is `Pending - client deciding`, never accepted.
  - **At a first/Fact Find meeting, nothing has been quoted yet, so most items are simply `requested` / `still open`.**

## Step 4b: Owner / life assured / contracting party changed -> REVISED QUOTE (any insurer) - follow-up meetings only

Not applicable at a first/Fact Find meeting (no quote exists yet to revise).

1. **Detect it:** flag every accepted or pending product whose owner, life assured or contracting party now differs from the name on the quote.
2. **Ask the provider for a revised quote in the new name.** Applies to ANY insurer or product provider.
3. **Draft, don't send.** Show Paul the draft and send only after his explicit yes.
4. **Track it:** record `Revised quote requested from [provider] on [date] - awaiting` and follow `outlook-emails-skill` tracking.
5. **Report it:** `Changed: owner [old] -> [new]` plus the action `Sitamah to request / chase revised quote`.

## Step 4c: Quote literacy and cession rule (Paul's rule - never miss a benefit that was explained on the call)

**At a first/Fact Find meeting there is usually no accepted quote yet to read** - this step applies once a quote exists; until then, note what was discussed as being requested/pending.

1. **Quote-literacy check.** For every product/benefit Paul explains, open the discussed quote in `Comparative Quotes` and read what it actually does: trigger, waiting period, months paid, conditions. Report it in ONE short plain-English bullet. If the quote does not state it, say "not stated in the quote" and flag it.
2. **Name the line items.** Name specific debts in words, never account numbers.
3. **Cession rule.** If a benefit needs ceding: (a) report in both outputs; (b) add the action `Sitamah to arrange for [the line items] to be ceded to [the bank] and send the cession documents to [client] to sign` as a LATER action with the trigger `once the policy is issued` (Paul: the cession waits for the policy, so it is listed in the PDF under Coming up and not in the Planner note); (c) check the application; (d) record `Still open` until the signed cession is back.
4. **Coverage check.** Every benefit Paul explained must map to a Step 4c bullet and a Sitamah action (a later one for a cession) where cession/signature is needed.
5. **Be resourceful - look beyond the quote.** Before flagging a detail as unknown, search: (a) the Fact Find Summary / Fact Find; (b) the latest WR Overview; (c) earlier Follow-Up Notes; (d) the applications; (e) current-transaction correspondence. Only if every source is silent or they conflict, flag it plainly.

## Step 4d: Credit life on a debt that new cover now protects (Paul's rule - ALWAYS add it)

Must ALWAYS appear in the report, even if nobody mentioned it on the call - including at a first/Fact Find meeting where this is often first discovered.

1. **Find it (Step 4c item 5 - be resourceful).** For every debt the new cover protects, check the Fact Find Summary / Fact Find, the latest WR Overview, earlier notes, applications. Record per debt: lender, whether credit life exists, the monthly cost or `unconfirmed`.
2. **Report it** one short bullet per debt. Mark it `Still open`.
3. **The ONE action (Paul's rule): `Sitamah to get the credit-life details from the client`, for now.** Asking the client what he wants to do, and cancelling the credit life, are NOT actions: his decision is reported as `PENDING - client deciding`.
4. **Never create a cancel-credit-life action.**
5. If the client has no credit life on a debt, say so only when the Fact Find records it explicitly; do not invent one.

## Step 5: Carry-forward against earlier meetings (follow-up meetings only - a first/Fact Find meeting has nothing to carry forward)

Using the area ledger, tag each point: **Resolved**, **Still open**, **New** (everything at a first/Fact Find meeting is `New` or simply `requested`/`still open`), **Changed** (before -> after). Add a short "Since the last meeting" block at the top of Output 2 (`since_last` in content.json, each item tagged). (Not applicable to a first/Fact Find meeting, which has no Output 2 of its own.)

## Step 6: Application differences and correction hand-off (follow-up meetings only; not applicable at a first/Fact Find meeting)

Using Step 2b, build the **application differences** list:
- **Differs from the meeting**, **Missing**, **Not yet captured**, **Wrong reference**.

Report it in both outputs: one short bullet per application naming the application and WHAT differs in words. Never write ID numbers, account numbers or tax numbers.

Then **call `complete-applications-skill` automatically after the report (step `handoffs`)** (Correction / Sync mode, its Step 7). The source of any detail to carry across is ONLY a current application in a current transaction folder, never an older one unless Paul explicitly says so. **If anything is unclear, ask Paul BEFORE any change is made.** Corrections are made in place. If no applications exist for the client, skip Step 2b and Step 6.
