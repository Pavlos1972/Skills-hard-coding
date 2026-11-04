---
name: "life-policy-schedule-analyzer"
description: "Critically analyzes a client's life policy schedule or quote from any SA insurer for Paul Kafentzis: mistakes, better same-insurer options, premiums, paybacks, honest opinion. Use when asked to analyze a schedule."
---

# Life Policy Schedule Analyzer

## Index

| # | Section | What it covers |
|---|---|---|
| 1 | Universal operating rules + Delivery gate | The nine rules for every step, and what must be done before a run counts as complete |
| 2 | Last updated + Changelog | Athens-time stamp, last changes, standing edit note |
| 3 | Goal | A critique, not a transcription |
| 4 | Scope | What the skill produces; when to use life-insurer-comparison instead |
| 5 | Step 0 | Intake: the proposed-quote question and the payback document |
| 6 | Step 1 / 1b | Locate the source documents; pull Fact Find Summary context |
| 7 | Step 2 / 2a / 2b | Extract everything; verify against real product information; plain-language bullets |
| 8 | Step 2c | Benchmark against the same insurer's better current options |
| 9 | Step 2d | Dread disease / severe illness deep-dive |
| 10 | Step 2e / 2f / 2g | Premium escalation table; Vitality mechanics; payback research |
| 11 | Step 2h / 2i | Cession check; second life / joint life |
| 12 | Step 3 / 3a | Red flags in two tiers; Broker's Honest Opinion |
| 13 | Step 4 | Accuracy rules |
| 14 | Step 5 | Build the detailed PDF (palette, fixed report structure) |
| 15 | Step 6 | Save and deliver the detailed reports |
| 16 | Step 7 | Client-facing visual summary reports |
| 17 | What not to do | The standing prohibitions |

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

**Delivery gate for this skill (rules 5 and 6 applied):** a run is complete only when ALL of these are done and confirmed in one line each: (1) Step 0 intake was asked and answered, and the source document(s) were located and read in full (Steps 1-2); (2) the mandatory checks were done (Steps 2a-2i, 3, 3a) and the Step 4 accuracy rules were met; (3) one detailed analysis PDF per policy schedule/quote was built (Step 5), saved in the client's "Analysis & Comparison Reports" folder with the correct filename, and the folder listing was checked to confirm each PDF is there (Step 6); (4) each PDF was presented to Paul in the chat, and the tabulated chat summary was given (Step 6.7-6.8); (5) where the visual summaries (Step 7) apply, each report was built as a live design, rendered as a PDF copy, saved in the same folder and checked. After ANY correction, repeat (2) to (5) for every deliverable that changed.


**Last updated: 2026-10-14 15:21 Athens time (EEST)**

> **Standing rule — not optional:** any edit to this skill is not complete until the
> "Last updated" line above is also rewritten to the current Athens/Greece date-time,
> in the same response as the edit, and a line is added to the Changelog below.

## Changelog

- **2026-10-14 (15:21)** — Index added; description made plain; the long changelog moved word for word to the Project doc; client names in examples replaced with placeholders. No rule changed.
- **2026-10-08 (14:39)** — Rule 9 reworded: skill changes go forward with the propose_skills review card; never claim live until the user confirms they saved it.
- **2026-10-08 (14:15)** — Universal operating rules block and Delivery gate added at the top.
- **2026-09-30 (10:53)** — Proposed insurer's paybacks must always be included (Step 0, Step 2g, Step 7 Report 2).
- **2026-09-30 (10:44)** — Step 0 intake question and Step 7 visual summary reports added.

Older entries (2026-09-30 09:12 back to the initial version of 2026-09-22) are in `life-policy-schedule-analyzer-changelog.md` in the Project, word for word.

## Goal — this is a critique, not a transcription

**The point of this skill is to be critical of the Policy Schedule or Quote in
front of it, on the client's behalf.** Anyone can retype what a schedule says.
What makes this useful to Paul is catching what the schedule *doesn't* say plainly
enough, what looks like a mistake, and — most importantly — whether the same
insurer, today, would offer this client meaningfully better cover, a better
definition, or a better structure than what they actually have. Every step below
serves that goal. If a step only produces a neutral restatement of the document,
it hasn't done its job — push further into "is this actually good, and could it be
better with this same insurer" before calling the analysis finished.

This applies equally to an **existing in-force Policy Schedule** and to a **new
Quote being considered** — both get the same critical treatment; a Quote just has
no "in force" history behind it yet.

## Scope

This skill applies to **any** Life Policy Schedule or Quote, from **any** South
African insurer, for **any** client. It is insurer-agnostic — no product facts are
hardcoded here — every schedule/quote is read on its own terms, then checked
against real, current, multi-sourced product knowledge before being called
accurate, and then benchmarked against that same insurer's own better options.

The skill produces two kinds of output: (1) the **detailed internal analysis** —
one PDF per policy schedule/quote (Steps 1–6), for Paul only; and (2) the
**client-facing visual summary reports** (Step 7) — one combined summary per
insurer, plus a current-vs-proposed comparison when a proposed quote exists —
designed to be presented on screen to the client.

**This is not the life-insurer-comparison skill.** If Paul is comparing this
policy against a *different* insurer's policy or quote, or considering a
replacement, use `life-insurer-comparison` instead — that produces a client-facing
comparison document across insurers. This skill critiques a single insurer's own
schedule/quote against itself — what the client has vs. what that same insurer
could offer them — for Paul's own reference, one document at a time. (The Step 7
Report 2 current-vs-proposed slides are a short on-screen summary for the client
of a proposal Paul has already decided to put forward; they do not replace a full
`life-insurer-comparison` document.)

## Step 0 — Intake: ask about the proposed quote (mandatory, at the start of every new client analysis request)

Before doing any work on a new client analysis request, ask Paul (use the
AskUserQuestion tool where available) exactly:

> **"Provide details of the Proposed Life Cover Quote"**

with these options:

- **The quote is in the client's folder** — Paul names the quote (or it is found
  in the client's folder, e.g. a "Comparative Quotes" subfolder) and it is used as
  the proposed cover for Report 2.
- **I will attach / paste it** — Paul supplies the quote in the chat.
- **No proposed covers for now** — no proposed quote exists yet. Only the analysis
  of what the client has (and Report 1) is built; Report 2 is **not** built. Do not
  ask again in that request.

If the request already names the proposed quote, treat the question as answered
and say which quote is being used. The answer decides whether Step 7 builds one
visual report or two.

**Always look for the proposed insurer's payback document too.** When a proposed
quote is used, also look in the same folder for that insurer's companion payback/
loyalty document for the same quote number — e.g. for BrightRock, the "BR CMPO"
(Change Moment Pay-Out guide) filed beside the Cover Proposal, named with the same
quote number. Use it in Step 2g and Step 7. If none can be found, say so plainly
and ask Paul for it (or whether the quote has no payback) rather than leaving the
payback out silently.

## Step 1 — Locate the source document(s)

**Documents are retrieved automatically from the client's own folder — never ask
Paul to paste or type out figures into the chat.** Only fall back to asking him
directly if retrieval genuinely can't find or disambiguate a file.

1. **Local machine — always attempted first.** Connect via the device bridge to
   Paul's local machine and check **both** of these locations under `liferisk.co.za`
   for the client's folder: `Company - Paul` (New Business, but not limited to it)
   and `Company - WR Clients` → `Paul Kafentzis (Client Files)` (current/existing
   clients). Check both — a given client's material could sit under either.
2. **Within the client's folder, look in the "6. Policy Schedules" subfolder** —
   where schedules/quotes are normally filed. If a client's folder uses a different
   numbering/naming, or the document is filed elsewhere, use whatever is actually
   there — note in the output which subfolder it was found in.
3. **SharePoint — only if the local machine genuinely can't be reached.**
4. **Ask Paul to attach the file — last resort only**, or use one already attached
   to the chat if he's provided it that way himself.
5. **Never touch another broker's folder.** `Paul Kafentzis (Client Files)` is the
   only folder under `Company - WR Clients` this skill ever reads from.
6. **If more than one policy schedule/quote is found**, confirm with Paul which
   one(s) he wants analyzed, or — if asked generically — analyze every current,
   in-force schedule found and say plainly which were included/skipped.

**Before treating a retrieved document as complete**, verify every page is
actually present — a scanned schedule can appear as just its cover page, with the
real benefit table, premium detail, and terms missing. If a document looks
suspiciously short, check it directly:

```bash
file /path/to/schedule.pdf
unzip -l /path/to/schedule.pdf   # some "PDF" files are actually zipped page images
```

A file reporting as `Zip archive data` despite a `.pdf` extension is a page-image
bundle — extract and view every page. Never build the analysis from a document
missing its actual benefit table or premium detail; if something genuinely isn't
in the document after checking, say so explicitly rather than guessing.

## Step 1b — Pull client context from the Fact Find Summary

Before extracting the schedule, look in the client's folder for an existing
**Fact Find Summary** (e.g. `[FirstName]_[Surname]_Fact_Find_Summary - DD.MM.YY.pdf`) or a
completed WR Fact Find. If found, read it for income, dependants and their ages,
existing debt, and other risk cover held — this is what turns "cover looks low"
or "this benefit matters for this client" from a guess into a grounded finding.

If none is found, say so plainly in the Sources section and proceed without it —
don't stop the analysis or ask Paul to produce one just for this.

## Step 2 — Read and extract everything on the schedule/quote

Go through the document page by page and extract, for **every** benefit it
lists — not just the main life cover:

- **Policy identity:** insurer, product name and tier/range, policy/quote number,
  life assured, policy owner (if different), inception/start date (or quote date),
  policy status (in force / lapsed / paid-up / under review / new quote, as
  stated), premium payer.
- **Life Cover — always identify the structure explicitly:** is it **term cover**
  (expires at a set age/date), **whole-of-life (WOL)** (runs for life), or
  **accidental-death-only** cover (pays only on accidental death, not natural
  causes)? This distinction changes what the client is actually protected against
  and must never be left ambiguous — state it plainly even if the schedule doesn't
  use these exact words.
- **Every benefit on the policy, one at a time:** cover type (life, permanent
  disability — lump sum and/or income — dread disease/severe illness/critical
  illness, income protection, temporary disability, funeral, education,
  retrenchment, debt/loan cover, etc.), sum assured, whether accelerated (reduces
  another benefit on claim) or standalone/additional, and the specific definition
  set used where stated (e.g. own-occupation vs any-occupation for disability).
- **Premiums:** total monthly/annual premium, and per-benefit breakdown if
  itemized. Note any health/lifestyle loading, and the loaded vs base premium
  where both are shown.
- **Waiting periods and survival periods:** any waiting period before a benefit
  pays out, and any survival period on dread disease/critical illness claims.
- **Exclusions and special terms:** general exclusions (suicide clause, war,
  pre-existing conditions), and anything specific to this policy — special terms,
  loadings, or exclusions from underwriting (often on a separate addendum — check
  for one).
- **Riders/add-ons:** anything optional bolted on, and whether currently included
  or declined.
- **Beneficiaries:** who's nominated, and in what proportion, if stated.
- **Cover/buy-up facilities:** any facility to increase cover without new medical
  underwriting, and its stated limits.

**Only extract what's actually on the document.** If a benefit type is genuinely
absent (e.g. no income protection at all), record it as "not held" — a gap is
often exactly what Paul needs to see.

## Step 2a — Verify against real product information (mandatory, every time)

**This is what makes the analysis trustworthy rather than a transcription, and it
must never be skipped.** A schedule states figures and benefit names but rarely
explains what they mean in practice — and schedules do contain typos, outdated
tier names, or figures inconsistent with the product they claim to belong to.

- **Search the web for the insurer's own current product/technical guide** for
  the exact product and tier printed on the document. Confirm what that product
  actually is, its normal benefit structure, and how its definitions are
  described.
- **Cross-check what the document states against what's researched.** Flag any
  inconsistency explicitly — e.g. *"schedule states X; [Insurer]'s current
  [Product] technical guide describes this benefit differently — worth confirming
  with the insurer."*
- **Never let researched general product knowledge override client-specific
  figures** (sum assured, premium, policy number, dates — always from the document
  itself). Research verifies terminology, structure, and plausibility, and feeds
  the plain-language explanations (2b), the benchmark (2c), and the dread disease/
  premium/Vitality/payback/cession/second-life deep-dives (2d–2i) — never a
  substitute for a client-specific figure.
- **If the exact product/tier can't be confirmed online**, say so plainly and rely
  on what the document states directly.
- Cite what was checked briefly in the Sources section.

## Step 2b — Explain product lines in plain language, as bullet points

Wherever a benefit or product line needs explaining to actually make sense —
what it does, when it pays out, how it interacts with other benefits — give a
short plain-language explanation directly alongside that benefit in the Benefits
Breakdown section, always as **bullet points, never prose**: one short bullet per
fact, two to four bullets per benefit is normal. Skip only for benefits that are
genuinely self-explanatory (e.g. a plain lump-sum life cover amount with no
add-ons).

## Step 2c — Benchmark against the insurer's own better current options

**This is the heart of the critique and must be done for every major benefit
category held (life, disability, dread disease/severe illness, income
protection).** Having confirmed via Step 2a what the client actually has, research
what that *same insurer* currently offers as its best or more comprehensive
version of that benefit — a higher tier, a broader definition, an additional
rider, a less restrictive payout structure — and ask plainly: **would this client
and their family have been better, more comprehensively covered on a different
current option from the same insurer?**

- Compare like-for-like where possible (similar premium/affordability band isn't
  required — the point is to surface the option, not assume the client can afford
  it; note affordability as a caveat, don't use it to suppress the finding).
- Only raise a benchmark finding when a **genuinely current, real, materially
  better** option exists in that insurer's own range — sourced from the same
  research as Step 2a, never invented or assumed from general market knowledge.
  If nothing better currently exists for a given benefit, say so plainly ("current
  cover already reflects [Insurer]'s top tier/definition for this benefit") — this
  is itself a useful, positive finding, not a gap to fill with a manufactured one.
- State the comparison plainly: what they have vs. what's currently available,
  and in concrete terms what having the better option would actually mean for a
  claim (e.g. "would pay out on a broader disability definition", "would cover
  three severity tiers instead of a flat payout", "would extend cover to the
  client's children at no extra underwriting").
- Every benchmark finding feeds into Step 3's Action Required / For Your Awareness
  tiers — typically Action Required if it's a real coverage gap for this client's
  situation (per the Fact Find context from Step 1b), otherwise For Your
  Awareness.

## Step 2d — Dread Disease / Severe Illness deep-dive (mandatory whenever this benefit is held or quoted)

Dread disease/critical illness/severe illness benefits vary enormously in real
value even when the headline sum assured looks the same. Extract and state each
of the following explicitly — don't just note the sum assured and move on:

- **Multiple claims:** can the client claim more than once (for unrelated or even
  related conditions), or is it a single-claim benefit that then falls away?
- **Payout structure:** does it pay **100% of the claim amount upfront** on a
  qualifying diagnosis, or is it **severity-tiered** (e.g. 25% / 50% / 75% / 100%
  depending on diagnosis severity)? State plainly that a severity-tiered structure
  is generally a **lesser/inferior definition** for the client than a flat 100%
  payout on any qualifying condition, because a severity-tiered benefit can pay
  out far less than the full sum assured even on a genuine, serious diagnosis.
- **Duration:** is the benefit whole-of-life, or does it expire at a specific age?
- **Can it pay more than 100%?** Some products allow cumulative payouts exceeding
  the original sum assured across multiple/staged claims — check and state this.
- **Survival period:** is there a survival period (e.g. 14 days) the client must
  survive past diagnosis before the claim pays? State the exact number of days if
  given.
- **Children's cover:** are the client's children covered for dread disease under
  this policy, and if so, to what amount and under what conditions?
- **BrightRock Trauma IQ (or equivalent):** for BrightRock specifically, is the
  client (and their children) covered under the Trauma IQ benefit or not? For
  other insurers, check for and name any directly equivalent
  needs-matched/intelligent trauma benefit.
- **Severe Illness scope and triggers:** how extensive is the Severe Illness
  benefit's condition list (broad vs narrow), and can a Severe Illness diagnosis
  actually trigger a standalone claim on this policy, or is it folded entirely
  into the main dread disease benefit with no independent trigger?
- **Accelerated vs standalone (restated here for emphasis):** does a dread
  disease claim reduce the life cover sum assured (accelerated) or pay in
  addition to it (standalone)? State this plainly — clients very often assume the
  opposite of what's actually true.

Every item above that represents a materially weaker structure than what's
**currently, genuinely available from the same insurer** (per Step 2c) is a
benchmark finding, not just a neutral fact — flag it as such.

## Step 2e — Premium pattern and escalation analysis (mandatory, tabulated)

- **Identify the pattern precisely:** is the premium **age-rated/age-related**
  (increases as the client ages — the current rate is only a snapshot, and these
  patterns can become significantly more expensive over time, sometimes
  aggressively so in later years) or **fixed/level** (contractually fixed
  regardless of age)? Never assume either way — confirm from the document, and if
  genuinely unclear, flag it and recommend confirming with the insurer.
- **Break down what actually drives the increase.** Where the schedule/insurer
  states it as a formula (e.g. **ACI + ABI** — Annual Contribution Increase plus
  Annual Benefit Increase, or the insurer's own equivalent naming), state each
  component separately and what it's actually driven by (CPI, a fixed %, an
  age-rating table), not just the combined headline number.
- **Produce a tabulated year-by-year premium projection, minimum 10 years.**
  Columns: Year / Client Age / Projected Monthly Premium / % Increase on Prior
  Year. Base this on the insurer's own stated escalation rate/table where one
  exists in the document or was confirmed via Step 2a research — never a made-up
  growth rate. If the exact future rate isn't confirmable (e.g. a non-guaranteed
  age-rated table not provided), project using the best available stated basis
  and **label the table clearly as illustrative**, noting the source of the
  assumption.
- **State the premium guarantee period** for the current premium, if any.
- If a health/lifestyle loading applies, note whether/how it affects the
  escalation pattern, if determinable.

## Step 2f — Vitality / wellness-linked premium mechanics (Discovery and equivalents)

**Applies whenever the insurer is Discovery, or another insurer with an
equivalent wellness-linked pricing mechanism (e.g. a wellness-programme tie-in).**
This is a distinct and often underestimated driver of real long-term cost, so it
gets its own dedicated coverage, not a passing mention:

- **Vitality status and its effect on premium increases:** explain how the
  client's current Vitality status (Blue/Bronze/Silver/Gold/Diamond, or
  equivalent) affects their annual premium increase percentage — state the actual
  mechanism and, where the status is known or statable, the approximate effect.
- **Annual Vitality health/medical checks:** explain that Vitality status (and
  therefore the premium-increase outcome) depends on annual health assessment
  results, and what kind of outcomes move status up or down.
- **Medical-aid claims impact:** explain how the client's medical aid claims
  history can factor into Vitality status/points and therefore into the premium
  increase outcome, where this mechanism applies.
- **Upfront discounts and clawbacks:** state clearly whether an upfront premium
  discount was applied at inception, the conditions attached to keeping it, and
  whether/how it can be clawed back over time (and over how many years) if those
  conditions aren't maintained — this is a common source of "premium went up more
  than expected" surprises and must be spelled out plainly.
- If the insurer isn't Discovery and has no equivalent mechanism, state plainly
  that this section doesn't apply rather than omitting it silently — so it's clear
  the check was made, not skipped.

## Step 2g — Payback / loyalty benefit research (policy held AND proposed quote — always)

Research and state the specific payback/loyalty mechanism this insurer offers, if
any — e.g. **Discovery PayBack**, **BrightRock's Change Moment payout**, or the
equivalent on any other insurer. **This applies to the insurer of the policy the
client holds AND to the insurer of the proposed quote (Step 0). Paybacks from the
proposed insurer's quote must ALWAYS be included — never omitted, never reduced to
a passing mention.**

- **For a proposed quote, take the figures from the insurer's own payback
  document** (e.g. BrightRock's "BR CMPO" Change Moment Pay-Out guide for the same
  quote number — see Step 0), not from general knowledge. Extract: the total payback
  value today and projected value at pay-out; each component (e.g. retirement,
  childcare per child) with its amount, pay-out date, and how it is paid (lump sum
  or monthly instalments, for how long, and its yearly growth rate); and its
  guarantee period. Never estimate or infer these figures.
- What triggers a payout (staying claim-free, a review point, a specific policy
  anniversary, a "change moment" event, etc.).
- Whether it's guaranteed or an estimate/projection.
- What conditions cause partial or full forfeiture or reduction (e.g. death before
  the pay-out date, cancelling the cover, claims that reduce it, any cap linked to
  premiums paid).
- Whether it's standard/included or an optional add-on with its own premium.
- State plainly if the policy held doesn't actually include this benefit even
  though the insurer offers it generally — that's itself a finding, and feeds
  Step 2c's benchmark where relevant.
- If the proposed insurer genuinely has no payback on the quote, say so plainly
  rather than leaving the topic out.

## Step 2h — Cession (mandatory check, every time)

Cession is very easy for a client to forget about and changes who actually gets
paid on a claim — so this is always checked and always stated explicitly, never
left implicit:

- **Is the policy ceded, and to whom?** Most commonly a policy is ceded to a bank
  or other lender as security for a loan (e.g. a home loan/bond) — check the
  schedule for any cession, cessionary, or "security cession" field/endorsement.
- **State plainly what a cession actually means for this policy:** while a
  security cession is in place, the cessionary (e.g. the bank) has the first
  right to the claim proceeds up to the amount owed, before the nominated
  beneficiaries see anything — this is very often not front-of-mind for the
  client and worth stating clearly rather than assuming it's understood.
- **If ceded, note whether the cession still looks proportionate** to what it was
  originally securing, where that's determinable (e.g. a cession from years ago
  against a loan that may now be much smaller or settled) — flag this as worth
  confirming with the client/lender rather than asserting the loan balance, which
  this skill has no way to verify independently.
- **If not ceded**, state that plainly too ("no cession noted on this schedule") —
  this is itself a useful confirmation, not just an absence to skip past.

## Step 2i — Second life / joint life structure (mandatory check, every time)

Mirrors the equivalent check in `life-insurer-comparison` — always check for a
second life on the policy, not just the primary life assured:

- **Is there a second life assured** (typically a spouse/partner) on this policy,
  separate from any spousal cover written as an entirely different policy?
- **If yes, is their cover independent or a rider?** State plainly whether the
  second life's cover stands on its own (survives if the main life's policy
  lapses) or is structured as a rider/add-on that is entirely dependent on the
  main life's policy remaining in force — if it's a rider, say so clearly, since
  this means the second life's cover disappears if the main policy lapses for any
  reason, which is easy to overlook.
- **State the second life's own benefits and sums assured** the same way as the
  main life's, per Step 2, rather than folding them vaguely into the main life's
  figures.
- **If there's no second life on this policy**, state that plainly too — and note
  in the output whether the Fact Find Summary (Step 1b) suggests the client has a
  spouse/partner who might reasonably need their own cover, as a For Your
  Awareness item, not an assumption that they're covered elsewhere.

## Step 3 — Red flags, mistakes, and things Paul should notice

After extracting and verifying the full picture (2–2i), identify everything that
stands out — mistakes on the document, inferior benefits/definitions versus what
Step 2c found currently available, and anything else genuinely visible on this
specific document, never a generic list applied blindly to every policy:

- **Mistakes on the document itself** — inconsistent figures, a definition name
  that doesn't match the insurer's real terminology, a total that doesn't add up,
  a benefit combination that product doesn't normally offer.
- Every genuine benchmark finding from Step 2c (a materially better current
  option exists with the same insurer).
- Anything from the Dread Disease deep-dive (2d) that represents a materially
  weaker structure than what's currently available.
- A common benefit type that's simply absent (e.g. no disability cover on an
  income earner, no dread disease cover at all).
- Cover that looks low relative to the client's income, debt, or dependants —
  using the Fact Find Summary context from Step 1b where available; otherwise say
  plainly adequacy can't be fully assessed without it.
- An active waiting period that hasn't yet lapsed.
- A premium pattern (2e) that's age-rated and will keep climbing where the client
  may be expecting it to stay flat, or vice versa — and any Vitality clawback risk
  (2f) the client may not be aware of.
- A rider that was declined at application and never revisited.
- Any special term, loading, or exclusion from underwriting that materially
  narrows the cover.
- Signs the policy may be at lapse risk (e.g. a "grace period"/arrears note).
- A benefit whose accelerated/standalone status means a dread disease claim would
  reduce the life cover — clients often assume the opposite.
- **A cession the client may not be actively thinking about (2h)**, especially
  one that looks disproportionate to what it's likely still securing.
- **A second life whose cover is entirely rider-dependent on the main policy (2i)**
  — or the absence of any cover at all for a spouse/partner the Fact Find
  indicates exists.
- Any inconsistency between the document and another client document on file
  (e.g. Fact Find Summary) — mismatched income, marital status, or other facts.

If nothing notable turns up, say so plainly ("no obvious gaps, mistakes, or
inferior benefits found on this schedule") rather than manufacturing a flag.

**Every finding must be sorted into one of two tiers (mandatory):**

- **Action Required** — something Paul or the client actually needs to do or
  decide: disclose a change, chase a missing document, confirm an inconsistency
  with the insurer, revisit inadequate cover, confirm a cession still makes sense,
  arrange independent cover for an uncovered second life, or seriously consider a
  materially better current option from Step 2c. If left alone, this has a real
  consequence.
- **For Your Awareness** — true and worth knowing, but nothing to chase right
  now: a minor filing inconsistency, a premium review clause, a benchmark finding
  that's real but marginal, a feature worth remembering for later.

When genuinely unsure which tier a finding belongs in, default to **Action
Required**.

## Step 3a — Broker's Honest Opinion (mandatory, closing section)

After all findings are laid out, give a genuine, reasoned, honest opinion of the
product — written for Paul as a fellow professional, not a hedge-everything
disclaimer. Structure it as:

- **Overall assessment in one or two sentences** — is this good, adequate, or
  poor cover for what it is, and why, in plain terms.
- **What's genuinely good about it** — don't manufacture criticism where the
  product is actually solid; say so plainly when it is.
- **What would make it materially better**, drawing directly on the Step 2c
  benchmark findings and the Action Required list — stated as a professional
  recommendation, not just a repeated list of facts.
- Keep this section honest and direct — it's the one place in the document where
  Paul gets Claude's actual read on the product, not just the facts.

## Step 4 — Accuracy rules — non-negotiable, no exceptions

Accuracy is the entire point of this skill. A wrong figure, a misdescribed
benefit, or an invented "better option" in an internal reference document is
worse than no document at all — Paul will trust it and may act on it in front of
a client. **There is no tolerance for errors here.**

- Every client-specific figure (sum assured, premium, dates, policy number) must
  come directly from the retrieved document. Never estimate, infer, or fill in a
  plausible-looking number.
- **Every general product claim — what the product is, its benefit structure,
  what a "better" current option looks like — must be checked against real,
  current, multiple independent sources before being stated as fact.** A single
  page or a single search result is not enough for anything going into the
  benchmark (2c), dread disease (2d), Vitality (2f), or payback (2g) sections —
  cross-check against at least a second source (the insurer's own technical
  guide/product page plus, where available, a second independent confirmation)
  before asserting it. Where sources genuinely disagree, state both and flag the
  disagreement rather than picking one silently.
- If a figure or field is illegible or missing, say so explicitly ("not stated on
  schedule" / "illegible — recommend requesting a clean copy") rather than
  guessing.
- Before treating a figure as "illegible", try a tighter crop and upscale on just
  that region:

```bash
python3 -c "
from PIL import Image
img = Image.open('page.jpeg')
crop = img.crop((x0, y0, x1, y1))
crop = crop.resize((crop.width*4, crop.height*4), Image.LANCZOS)
crop.save('crop.png')
"
tesseract crop.png - --psm 6
```

- Never carry over a figure from a different client, policy, or previous session.
- **Never present a benchmark "could have had better" finding (2c) that isn't
  sourced from real, current, verified product information.** If genuinely unsure
  whether a better option currently exists, say so — don't guess to fill the
  section.
- **Never assert a cession or loan-balance figure (2h) that isn't stated on the
  schedule itself** — this skill has no independent way to verify a loan balance,
  so any comment on proportionality is framed as "worth confirming", never as a
  stated fact.
- Cross-check every figure against the source document, and every product claim
  against the multi-source research, one final time before finalizing the PDF.
- **No detail extracted in Step 2 (or researched in 2a–2i) may be dropped to
  achieve a cleaner layout.** The Verdict, Benefit Summary Table, and tiered
  Action Required / For Your Awareness lists are additive — fast ways in — never a
  replacement for the full detail elsewhere in the document.

## Step 5 — Build the PDF — clean, tiered, professional, never confusing

The whole point of this document is that Paul can glance at it and immediately
understand the policy, what's inferior about it if anything, and what (if
anything) needs doing — not decode a wall of prose, and not wade through
repetition to find what matters. Use reportlab (`SimpleDocTemplate`, letter page
size, ~18-20mm margins), designed to look like a **polished, professional
internal document** rather than a plain reference sheet:

**Colour palette (professional, warm-neutral base with a confident accent — not
client-branded, but not a bare grey document either):**

```
--navy:        #1F3A5F   /* section headings, table header bands */
--navy-light:  #EAF1F8   /* shaded label columns */
--gold:        #B08D57   /* accent rule under the title, Verdict box border */
--gold-light:  #F3ECE0   /* Verdict box background */
--green:       #2E7D32   /* "as good as it gets" / positive finding, on #E8F5E9 */
--amber:       #E65100   /* For Your Awareness marker, on #FFF3E0 */
--red:         #B0271A   /* Action Required marker, Red Flags text, on #FDECEA */
--text:        #2C2C2C
--muted:       #666666
--border:      #E0DDD8
```

- **Every section is a table**, not a paragraph, wherever content is naturally
  field/value pairs. Two-column tables: left column bold label (shaded
  `--navy-light`), right column value, 0.5pt grey grid lines.
- Navy section headings with a thin gold rule underneath, clearly separating each
  section so the document can be scanned by heading alone.
- A clear **"INTERNAL — NOT FOR CLIENT DISTRIBUTION"** label near the top of the
  first page.
- **Verdict (mandatory, directly under the header):** a single boxed callout
  (gold-bordered, `--gold-light` background), one to two sentences, letting Paul
  triage the policy without reading further — what it is, and the single most
  important thing about it. A summary of what follows, never a new claim.
- **Benefit Summary Table (mandatory, directly under the Verdict):** wide table
  titled with insurer, product name, policy number, client name; columns
  **Benefit / Sum Assured / Premium**, one row per benefit actually held
  (including each dependant's/second life's own benefit where relevant). Navy-
  shaded header row. Common benefit types not held get one compact footer
  caption, never their own row.
- **Action Required / For Your Awareness (mandatory, directly under the Benefit
  Summary Table):** the Step 3 findings, numbered, tiered, Action Required in red,
  For Your Awareness in amber. Headline only here — full explanation in the Red
  Flags & Observations section later, under the same number.
- Plain-language explanations from Step 2b sit as bullet points directly under
  the relevant benefit's table row in the Benefits Breakdown section.
- **Policy Identity table:** fold "Policy owner"/"Premium payer" into the life
  assured row as a parenthetical when identical to the life assured; only break
  out as separate rows when they genuinely differ. Add a **Cession** field to this
  table (ceded/not ceded, and to whom if ceded) so it's visible at a glance
  alongside the other identity facts.
- **Dread Disease Deep-Dive** gets its own clearly headed sub-section within the
  Benefits Breakdown for that benefit — a compact table or tight bullet list
  covering every item from Step 2d, not folded silently into the general benefit
  description.
- **Second Life / Joint Life** (Step 2i) gets its own clearly headed sub-section
  when a second life exists, with its own mini Benefit table (same three columns)
  — or a one-line "no second life on this policy" statement when there isn't one.
- **Premium Escalation Table (mandatory, in the Premiums section):** the full
  10-year Year / Age / Premium / % Increase table from Step 2e, clearly labelled
  illustrative where applicable, with the ACI/ABI (or equivalent) breakdown stated
  above it.
- **Vitality/Wellness Mechanics** (Step 2f) and **Payback/Loyalty Benefit**
  (Step 2g) each get their own clearly headed sub-section when applicable — state
  plainly "not applicable — no such mechanism with this insurer" when they aren't,
  rather than omitting the heading.
- **Broker's Honest Opinion (mandatory, final content section before Sources):**
  set apart visually (e.g. a light navy-tinted box), written in first person as
  Paul's own internal note to himself, per Step 3a.
- Red Flags & Observations section: Action Required items in red, For Your
  Awareness items in amber, bold the headline clause of each bullet, same
  numbering as the top-of-document summary.
- **Keep it simple.** Don't add sub-sub-sections, nested tables, or nice-to-have
  extra columns that aren't needed — a compact table beats an elaborate layout.

### Report structure (fixed section order)

1. **Header** — "Life Policy Schedule Analysis (Internal)", client name, insurer
   and product name, policy/quote number, date of analysis, internal-use label.
2. **Verdict** — one boxed callout (see Step 5).
3. **Benefit Summary Table** — Benefit / Sum Assured / Premium, held benefits
   only, footer line for common types checked and not held.
4. **Action Required / For Your Awareness** — numbered, tiered headline bullets.
5. **1. Policy Identity** — table including Life Cover Type (term/WOL/accidental)
   and Cession status (2h).
6. **2. Benefits Breakdown** — one table per benefit type, each with sum assured,
   accelerated/standalone status, definition set, waiting/survival period, and a
   bullet-point plain-language explanation (2b). The Dread Disease benefit's
   entry includes the full Deep-Dive sub-section (2d).
7. **3. Second Life / Joint Life** — per Step 2i, or "no second life on this
   policy".
8. **4. Premiums** — total/per-benefit premium, loading, escalation type and
   rate, the ACI/ABI-style breakdown, guarantee period, and the mandatory 10-year
   Premium Escalation Table (2e).
9. **5. Vitality / Wellness Mechanics** — per Step 2f, or "not applicable".
10. **6. Payback / Loyalty Benefit** — per Step 2g, or "not applicable".
11. **7. Benchmark — Could the Client Be Better Covered?** — the full Step 2c
    findings, benefit by benefit, stated plainly (what they have vs. what's
    currently available, and what it would mean for a claim).
12. **8. Exclusions & Special Terms.**
13. **9. Riders & Add-Ons.**
14. **10. Beneficiaries.**
15. **11. Red Flags & Observations** — full detail per Step 3, tiered, same
    numbering as item 4.
16. **Broker's Honest Opinion** — per Step 3a.
17. **Sources** — document filename/date used; Fact Find Summary used (or noted
    absent); every product source checked per Step 2a/4 (insurer technical
    guide, second independent source); a one-line note that this is an internal
    reference document, not verified against the insurer's live system, and
    should be reconfirmed with the insurer before being relied on for a claim or
    compliance purpose.

## Step 6 — Save and deliver (detailed analysis reports)

**Every completed analysis report MUST be saved in the "Analysis & Comparison
Reports" folder of the client's file. No exceptions.** Never leave a report in the
source-document subfolder ("6. Policy Schedules" root) or drop it loose in the
client's folder root or anywhere else. This applies equally to the Step 7 visual
summary reports.

1. **Find the folder.** Connect via the device bridge (local machine first, per
   the same order as Step 1; SharePoint only if the local machine is genuinely
   unreachable) and locate the folder named exactly **"Analysis & Comparison
   Reports"** inside the client's own folder. Look where it actually sits — for
   one client it is inside "6. Policy Schedules"
   (`Company - Paul/New Business/[Surname], [FirstName]/6. Policy Schedules/Analysis &
   Comparison Reports`), but folder numbering can differ between clients, so check
   the client's subfolders rather than assuming the path.
2. **If the folder doesn't exist yet**, create it in the same place the client's
   other report folders/policy schedules sit (normally inside "6. Policy
   Schedules"), save the report in it, and tell Paul in the chat summary that the
   folder had to be created. Never fall back to saving somewhere else instead.
3. **Filename:** `[FirstName]_[Surname]_[Insurer]_Policy_Analysis - DD.MM.YY.pdf`
   (date = today's date, formatted DD.MM.YY), e.g.
   `[FirstName]_[Surname]_Discovery_Policy_Analysis - 28.09.26.pdf`. When one insurer has
   more than one policy for the client, add the product before `_Policy_Analysis`,
   e.g. `[FirstName]_[Surname]_Instant_Life_Life_Cover_Policy_Analysis - 30.09.26.pdf`.
4. **One PDF per policy schedule/quote for the detailed analysis.** If multiple
   documents were analyzed for the same client in one request, produce a separate
   detailed PDF for each — never merge them into a single combined detailed
   analysis document. (The client-facing summary in Step 7 is the one place where
   same-insurer policies ARE combined.) All of them go into the same "Analysis &
   Comparison Reports" folder.
5. **Save straight into the final folder.** Write/commit each PDF directly to the
   "Analysis & Comparison Reports" path, not first into another folder to be moved
   later. Never overwrite an existing file with the same name without checking
   first; if one exists, keep both by adding a version suffix and tell Paul.
6. **Verify after saving.** List the folder and confirm each PDF is actually there
   before telling Paul it's saved.
7. Present each PDF to Paul in the chat too (`present_files`, SendUserFile, or
   this session's equivalent file-delivery tool) — the chat summary is never a
   substitute for the saved PDF, and the chat copy never replaces the saved copy.
8. **Also give a tabulated chat summary** — lead with the same Verdict line, then
   the Benefit Summary Table, then the numbered Action Required list, then a
   one-line pointer to the Broker's Honest Opinion in the PDF, and a line saying
   which folder the report(s) were saved in — so Paul gets the gist, including
   anything he needs to worry about or reconsider, immediately without opening the
   PDF.

## Step 7 — Visual Summary Reports (client-facing, for presenting on screen)

After the detailed per-policy analyses (Steps 1–6) are done, build the
client-facing visual summaries. These are short, simplified, colourful decks Paul
can present on screen in a Teams meeting — sections, point form, plain English.
They are **separate from and much lighter than** the internal analysis PDFs, and
they are built **from** them (never from new, unchecked figures).

**Combine same-insurer policies into ONE summary.** Where the client holds more
than one policy with the same insurer (e.g. an Instant Life Life Cover policy and
an Instant Life Work Disability policy), the visual summary combines them into a
single report — one deck per insurer, not one per policy. The detailed analysis
PDFs stay separate, one per policy (Step 6.4).

**Cover the four standard categories, always.** A life policy is generally made up
of Life, Disability, Dread/Serious Illness, and Income Protection (ICB). Every
visual summary shows all four, and shows **"Not held"** (visibly, e.g. an amber
tile) for any category the client does not have — a gap is exactly what the client
needs to see.

**Report 1 — what the client has (always built).** Only a summary of the client's
current cover. Suggested sections (keep it to about six slides): title; at a glance
(the four categories as tiles, with sum assured and premium, combined premium);
how the policies work in plain English (bullets, including the current insurer's
cash back/payback); how the cost changes over time; key things to sort out (from
the Action Required items, reworded for the client); where the cover falls short
against the client's needs (from the Fact Find).

**Report 2 — current vs proposed (built ONLY when a proposed quote was provided at
Step 0).** A direct, side-by-side comparison of what the client has against the
proposed quote. Suggested sections (about seven slides): title; side-by-side table
(the four categories, today vs proposed, **a Payback row**, plus monthly cost); what
the client gains and what to know; the proposed cover in detail; cost comparison
over time; **a "Paybacks compared" slide**; next steps. If the answer at Step 0 was
**"No proposed covers for now"**, do **not** build Report 2 — say plainly in the
chat that it was skipped for that reason.

**Paybacks are ALWAYS in Report 2 (mandatory).** Include the proposed insurer's
payback (e.g. BrightRock's Change Moment pay-out) in **both** the side-by-side
table (a "Payback" row: the current insurer's cash back vs the proposed insurer's
payback) **and** on its own "Paybacks compared" slide. That slide puts the current
insurer's cash back next to the proposed insurer's payback, with the headline
figures from Step 2g (today's value, projected value at pay-out, each component's
amount, pay-out date and how it is paid), plus one short plain-English line on the
key conditions (must be alive at the pay-out date, keep the cover in place, lost if
the policy is cancelled, reduced by certain claims, any cap tied to premiums paid).
Label every projected/illustrative payback figure as such. Never quote a payback as
a percentage of premiums unless the insurer's own document states it. Do not refer
to the payback in the proposal slide or the cost slide without pointing to the
Paybacks compared slide.

**Recommendations must be brief, simple and uncomplicated.** A short list of
next steps with a timing chip, not an essay. The proposed cover is presented as
the recommended way forward only when Paul has supplied it as such.

**Client-facing wording rules (the decks are shown to the client):**

- Leave out the Broker's Honest Opinion, any internal filing notes, and any
  "INTERNAL" wording. Do not carry over internal jargon or benchmark language.
- Reword findings that expose internal record-keeping or Fact Find contradictions
  as neutral client-friendly actions (e.g. "our records did not show them, so we
  will check they are still active").
- Every figure comes from the source schedules/quote/payback document or from the
  analysis PDFs. Anything illustrative or estimated (e.g. projected premiums) is
  labelled "estimate" on the slide with the assumption stated in small print. Never
  present an estimate as a contractual figure.
- Note the proposed quote's expiry/validity date in the next steps when it has one.

**Format and delivery.**

1. Build each report as a **live design** using the Artifact tool's Design type
   (1280×720 slides joined by Next/Back links, launched focused on slide 1), so
   Paul opens the link and screen-shares it in Teams. Follow the type's own
   instructions for files and publishing. Names of the design canvases follow the
   filename convention below (without the date).
2. Also render a **PDF copy** of each report (one slide per 1280×720 page) so a
   static copy lives in the client's file and can be used if the live link is
   unavailable. Check the PDF pages visually for overflow or missing fonts before
   saving.
3. **Filenames (short, agreed):**
   - Report 1: `[FirstName]_[Surname]_[Insurer]_Policy_Analysis_Slide - DD.MM.YY`
     e.g. `[FirstName]_[Surname]_Instant_Life_Policy_Analysis_Slide - 30.09.26`
   - Report 2: `[FirstName]_[Surname]_[ProposedInsurerAbbrev]_VS_[CurrentInsurer]_Policy_Analysis_Slide - DD.MM.YY`
     e.g. `[FirstName]_[Surname]_BR_VS_Instant_Life_Policy_Analysis_Slide - 30.09.26`
4. **Save to "Analysis & Comparison Reports"** (Step 6.1–6.2 rules apply): the PDF
   copies go straight into that folder; verify by listing the folder. If an
   updated version is saved while the earlier file is open or locked, keep both by
   adding a version suffix (Step 6.5) and tell Paul. Also give Paul the link to each
   live design in the chat summary. The designs are private until Paul shares them
   from the page's Share menu — tell him so if the client needs to open them
   himself.
5. **Chat summary:** one or two lines per report — what it is, where the PDF is
   saved — plus any assumptions and items Paul should confirm before presenting
   (e.g. estimates used, quote expiry, mismatches between the quote and the Fact
   Find).

## What not to do

Do not fabricate, estimate, or carry over a figure from memory, a different
client, or a previous analysis. Do not present the detailed analysis as a
client-facing document — it is Paul's internal reference only (only the Step 7
visual summaries are client-facing). Do not skip the Client File Access
retrieval steps and ask Paul to paste in figures unless retrieval has genuinely
been tried and failed. Do not merge multiple documents into one detailed analysis
PDF. **Do not save a completed report anywhere other than the client's "Analysis &
Comparison Reports" folder — not alongside the source documents in "6. Policy
Schedules", not in the client's folder root, and not in the chat only.** Do not
skip Step 2a's or Step 4's multi-source product research — an unverified
transcription, or a single-source claim, is not what this skill is for. Do not skip
Step 2c's benchmark against the same insurer's better current options — this is the
core critique, not an optional extra, and it must never be invented or assumed
without real sourcing. Do not skip the Dread Disease deep-dive (2d) whenever that
benefit is present. Do not present a premium pattern without the tabulated 10-year
projection (2e), or skip the Vitality (2f) / payback (2g) sections without at
least stating "not applicable". Do not skip the cession check (2h) or the second
life check (2i) — both are mandatory every time, even when the answer is simply
"none". Do not assert a loan balance or claim a cession is disproportionate
without flagging it as something to confirm, never as a stated fact. Do not end
the detailed report without the Broker's Honest Opinion (3a) — findings alone
aren't the deliverable, a genuine professional read is. Do not silently drop a
benefit type that's absent — record the absence as a compact footer line, not its
own full row. Do not bury the analysis in dense prose when a clean table would say
it more clearly. Do not write plain-language product explanations as prose
paragraphs — bullet points only. Do not leave a finding out of the top-of-document
summary — every numbered item there must also appear, same number, in the full Red
Flags section. Do not flatten every finding into one undifferentiated list — sort
into Action Required or For Your Awareness, defaulting to Action Required when
unsure. None of this trims actual content: every figure, source, and finding in the
document before a presentation pass must still be in it after.

**Visual summary rules (Step 7):** Do not start a new client analysis without
asking Step 0's "Provide details of the Proposed Life Cover Quote" question. Do not
build Report 2 when Paul chose "No proposed covers for now". Do not build separate
visual summaries for policies from the same insurer — combine them into one. Do not
leave out any of the four categories (Life, Disability, Dread/Serious Illness,
Income Protection) — show "Not held" instead. Do not put the Broker's Honest
Opinion, internal filing notes or "INTERNAL" wording in a client-facing deck. Do
not present an estimate as a contractual figure. Do not overcomplicate the
recommendations — brief and simple. Do not save the PDF copies anywhere but
"Analysis & Comparison Reports". **Do not leave the proposed insurer's payback
(e.g. BrightRock's Change Moment pay-out) out of Report 2, and do not build the
payback figures from anything other than the insurer's own payback document — if
that document has not been found, ask Paul for it.**