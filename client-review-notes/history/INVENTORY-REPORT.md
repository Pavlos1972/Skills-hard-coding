INVENTORY of the old skill: 203 sentences
  kept (word for word or nearly): 12
  reworded, with a recorded change: 123
  dropped, with a recorded decision: 68
  UNACCOUNTED: 0


REWORDED (each is covered by a recorded change):
- old line 54: # Client Review Notes — Wealth Revolution (FSP45946)
    now: """The model of the client-review-notes:
    why: Kept; the core principle is now backed by program checks.
- old line 56: Format raw Outlook contact notes into a standardised, consistently structured client record for Paul Kafentzis.
    now: "Formats raw Outlook contact notes into a standard Client Record for Paul Kafentzis (FSP45946), delivered as a .md file.
    why: Kept; the core principle is now backed by program checks.
- old line 56: Every record must follow the same structure, regardless of how much or how little information is provided in the source.
    now: An earlier record of the same client is shown to Paul and he decides before anything is merged.
    why: Kept; the core principle is now backed by program checks.
- old line 58: this is reformatting with summarisation of narrative notes — not a lossy summary.
    now: reformatting with summarisation of the narrative notes, never a lossy summary.
    why: Kept; the core principle is now backed by program checks.
- old line 58: The Notes section must be condensed into concise, scannable bullets rather than reproduced word-for-word, but every material detail (facts, figures, dates, names, decisions, outstanding items, instruc
    now: The Notes section is condensed into concise, scannable bullets, but every material detail (facts, figures, dates, names, decisions, outstanding items, instructions) must still appear.
    why: Kept; the core principle is now backed by program checks.
- old line 58: Cut redundant wording, filler, and repetition — never cut information.
    now: Cut redundant wording, filler and repetition:
    why: Kept; the core principle is now backed by program checks.
- old line 58: Structured data fields (contract numbers, DOC dates, ID numbers, commission amounts, policy statuses) remain verbatim — these are audit-sensitive figures, not narrative, and must never be paraphrased 
    now: Contract numbers, DOC dates, premiums, status notes, IDs and commission are verbatim;
    why: Kept; the core principle is now backed by program checks.
- old line 58: Typos or inconsistencies found in those verbatim data fields are preserved and flagged with ⚠️, never silently corrected.
    now: Apparent typos or inconsistencies are preserved and flagged with a flag.
    why: Kept; the core principle is now backed by program checks.
- old line 62: When Paul supplies substantial new source material for a client that already has a formatted record, produce a full redo of the record incorporating the new material — don't just patch or append the d
    now: When Paul supplies substantial new source material for a client who already has a formatted record, produce a full redo of the record incorporating it:
    why: Kept; the no-confirmation rule stays, only a duplicate stops the record.
- old line 63: When Paul points out an error or supplies a correction, redeliver the corrected record itself.
    now: 2 | What a finished run contains | The .md record, the short audit and the block for Paul |
    why: Kept; the no-confirmation rule stays, only a duplicate stops the record.
- old line 63: Don't preface it with an explanation of what changed unless he asks — he expects the fixed deliverable, not a description of the fix.
    now: redeliver the corrected record itself, without prefacing it with an explanation of what changed unless he asks.
    why: Kept; the no-confirmation rule stays, only a duplicate stops the record.
- old line 64: In the Summarized Client Review notes project, Claude formats the record as soon as raw notes or a client record are supplied — no confirmation step before producing output.
    now: %s is in the raw notes but not in the record (keep it, or list it in left_out with a reason)" % (n, key))
    why: Kept; the no-confirmation rule stays, only a duplicate stops the record.
- old line 68: Begin the record with the client's full display name, category, and ID in parentheses:
    now: Send out/<file name>.md with the file-delivery tool and record chat.sent.
    why: Drawn by the program; the bracket shows the Categories field as written (Paul agreed, 04/11/2026).
- old line 70: Firstname Lastname (Client) (ID number)
    now: Pat Samplecase (Client / BrightRock Lead) (ID number)
    why: Drawn by the program; the bracket shows the Categories field as written (Paul agreed, 04/11/2026).
- old line 72: If the client has a known/preferred name, insert it in parentheses after the first name:
    now: Known As only if the source explicitly gives a nickname or preferred name.
    why: Drawn by the program; the bracket shows the Categories field as written (Paul agreed, 04/11/2026).
- old line 74: Firstname (Knownname) Lastname (Client) (ID number)
    now: Pat Samplecase (Client / BrightRock Lead) (ID number)
    why: Drawn by the program; the bracket shows the Categories field as written (Paul agreed, 04/11/2026).
- old line 76: ## Field order (always use this exact sequence)
    now: """The Client Record as Markdown, always in this layout:
    why: The 18 fields are drawn in this order and checked.
- old line 93: Previous/Replaced Policies | Current/Active Policies | Non-active/Lapsed Policies)
    now: [["previous", "Previous/Replaced Policies:"], ["current", "Current/Active Policies:"], ["inactive", "Non-active/Lapsed Policies:"]],
    why: The 18 fields are drawn in this order and checked.
- old line 100: Put the value on the line directly below the label — never inline on the same line as the label.
    now: "Put the short audit and the block for Paul it prints in your reply exactly as they are.
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 101: Insert a horizontal rule --- on its own line between every top-level section.
    now: P.append("a horizontal rule is missing between sections")
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 102: Insert a blank line between every field label+value pair and between each list block.
    now: a header line, then the 18 fields each with a bold label and its value on the line below,
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 103: Never let two sections run together with no visual gap.
    now: Never rewrite, shorten or "improve" the programs during a run, and never type the Markdown yourself.
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 107: If a field is absent from the source notes, write:
    now: '%s' is not in the raw notes (a field is reproduced exactly as the source gives it;
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 108: If notes appear lost or clearly incomplete, flag with ⚠️.
    now: If the notes appear lost or clearly incomplete, flag it with ⚠️ in the Notes and tell Paul;
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 109: Never invent, infer, or fill in information not explicitly stated in the source.
    now: Never invent, infer or fill in.
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 112: Only populate if the source explicitly references a nickname or preferred name.
    now: Known As only if the source explicitly gives a nickname or preferred name.
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 115: Reproduce exactly as stated in the source (e.g.
    now: Fields 1 to 12 are text exactly as the source gives it;
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 115: Client, Client / BrightRock Lead, Client / Non-Replacement).
    now: Categories exactly as stated (Client, Client / BrightRock Lead, Client / Non-Replacement).
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 118: If source says "not brokers yet" with a blank contract, reproduce as:
    now: If the source says "not brokers yet" with a blank contract:
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 122: List each family member as a bullet point:
    now: a list, one member per bullet:
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 123: If a dependant has linked policy details, include those under that family member's entry.
    now: A dependant's linked policy details go under that member's entry.
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 126: Always use these three sub-headings, in this order:
    now: """Answers 'is this in the report?' against the extracted text."""
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 130: Each policy entry on its own bullet line, in this format:
    now: python3 %s/run.py read %s --ack %d --note "one line on what is in this part"' % (SCRIPTS, a.run, nxt))
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 131: [number] ([Product / Insurer]) DOC [date] / [premium if stated] / [status notes in CAPS if present]
    now: [number] ([Product / Insurer]) DOC [date] / [premium if stated] / [STATUS].
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 132: Reproduce contract numbers, DOC dates, premiums, and status notes verbatim — do not reformat or clean up.
    now: Contract numbers, DOC dates, premiums and status notes are reproduced verbatim:
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 133: Preserve apparent typos or inconsistencies and flag with ⚠️ rather than silently correcting.
    now: Apparent typos or inconsistencies are preserved and flagged with a flag.
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 134: If a sub-section has no entries:
    now: if _edit1(a, b) and (a, b) not in shown:
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 138: Each date heading in BOLD ALL CAPS (e.g.
    now: The program draws the BOLD ALL CAPS heading:
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 138: MARCH 2024, 14 FEBRUARY 2022).
    now: '14 FEBRUARY 2022' (day) or 'MARCH 2024' (month only)."""
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 139: Separate each date block with a --- horizontal rule above it.
    now: P.append("a horizontal rule is missing between sections")
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 140: Under each date heading, condense the raw note into short, tight bullet points — strip filler, throat-clearing, and repeated wording — while retaining every fact:
    now: condense each entry into short, tight bullets, keeping every fact:
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 140: A reader should be able to reconstruct the full picture from the summary alone, just not the original sentence-by-sentence phrasing.
    now: %s is not in the merged record (nothing from either version may be lost)" % (e["id"], key))
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 141: When a client asks "which X should I do Y from" or requests guidance on choosing between options, ALWAYS capture:
    now: It REBUILDS the entries, the checks and the Markdown from the run folder, so nothing is taken on trust from a file Claude could have edited.
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 142: What the client is asking for (e.g.
    now: "Earlier Client Records of the same client that Paul gives you (for the duplicate check):
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 143: Which products/accounts are available (list by contract number and product type)
    now: who, what, which policy or contract number, amounts, dates, decisions made, next steps.
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 144: Which product(s) or option(s) the advisor recommended or is considering
    now: %s is in the raw notes but not in the record (keep it, or list it in left_out with a reason)" % (n, key))
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 145: Any supporting rationale (tax implications, fund values, withdrawal rules)
    now: "Client asked which OM products (RA (contract no.), Tax-Free (contract no.), Funeral (contract no.)) to withdraw R70k from.
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 146: What the client decided or what decision is pending
    now: An earlier record of the same client is shown to Paul and he decides before anything is merged.
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 147: client deciding which to use." NOT just "Client asked about OM withdrawal" (loses critical detail about which products are in scope).
    now: client deciding which to use." NOT "Client asked about OM withdrawal".
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 148: FNA breakdown, medical requirements, shareholding details) stay as indented bullets but should also be tightened — combine related line items where it doesn't lose information.
    now: Sub-lists (an FNA breakdown, medical requirements, shareholding details) stay as indented bullets, tightened where nothing is lost.
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 149: Quoted text from emails/messages:
    now: You do not work from memory of this page:
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 149: only quote verbatim when the exact wording is materially important (e.g.
    now: Quoted text from emails or messages only when the exact wording matters (an explicit instruction, a commitment, a "do not contact" request, anything that could matter in a dispute);
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 149: an explicit instruction, a commitment, a "do not contact" request, or language that could matter for compliance/dispute purposes).
    now: Quoted text from emails or messages only when the exact wording matters (an explicit instruction, a commitment, a "do not contact" request, anything that could matter in a dispute);
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 149: Otherwise, summarise the substance of the email/message instead of quoting it in full.
    now: The program adds, at the top of Notes, the warnings it finds in the raw notes:
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 149: When quoting, keep the quote short and still include the timestamp.
    now: Keep a quote short and include its timestamp.
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 150: render as [Planner – Task Name](URL) with anchor text matching the Planner task name exactly — links themselves are never summarised.
    now: MS Planner links are rendered [Planner – Task Name](URL) with the anchor text matching the Planner task name exactly;
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 151: always reproduce in full verbatim (never summarised) AND add a ⚠️ flag at the top of the Notes section.
    now: "Do not contact" lines are reproduced in full and flagged at the top of Notes.
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 152: Timestamps that look system-generated rather than actual event dates:
    now: it looks system-generated, not an event date" % (n, k))
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 152: flag with a ⚠️ note explaining the discrepancy.
    now: acknowledge the part with a one-line note of what is in it:
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 153: BOLD ALL CAPS only — no underline tags, no HTML, no <u> symbols.
    now: no underline tags and no HTML.
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 154: Do not omit an event, figure, or outstanding item to save space — if the summary is getting long because the source has a lot of distinct events, that's expected;
    now: Do not omit an event, figure or outstanding item to save space:
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 154: length should track the number of distinct facts, not be capped artificially.
    now: length follows the number of distinct facts.
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 157: Reproduce verbatim — no paraphrasing, no reformatting of amounts.
    now: There is no closing sign-off line at the end of the record.
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 158: Insurer – Product Description (Month 'YY) followed by bullet lines for each commission type.
    now: "Insurer – Product Description (Month 'YY)", "lines":
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 159: If no commission is recorded:
    now: "no earlier record matches, or Paul's decision is recorded in his own words"
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 163: Every formatted client record must be delivered as a downloadable .md file — never as chat-only text, even if the record is short.
    now: Every formatted client record is delivered as a downloadable .md file in the chat, never as chat-only text, even if the record is short (chat text is at most a preview).
    why: The file is the deliverable, with a program-built file name.
- old line 163: Chat text is a preview at most;
    now: This skill is a program that walks you through the job one step at a time.
    why: The file is the deliverable, with a program-built file name.
- old line 167: Before formatting any record, check whether a client with the same name or ID number has already been formatted in the current session.
    now: Before formatting a record, the program checks the earlier Client Records you registered:
    why: Earlier records are registered; Paul decides; a merged record must keep everything.
- old line 168: If a potential duplicate is identified, flag it explicitly before proceeding.
    now: Never say a skill change is live before Paul confirms he uploaded it.
    why: Earlier records are registered; Paul decides; a merged record must keep everything.
- old line 169: If confirmed as a duplicate, produce a single merged record combining all unique information from both versions, noting which version contributed which additional details.
    now: produce ONE merged record combining all the unique information of both versions, and enter merge_notes saying which version contributed which additional details.
    why: Earlier records are registered; Paul decides; a merged record must keep everything.
- old line 170: Never silently merge without flagging first.
    now: never say "I cannot access your files" without a log of all three.
    why: Earlier records are registered; Paul decides; a merged record must keep everything.
- old line 174: Contract numbers, DOC dates, policy details, ID numbers, and commission entries must be reproduced verbatim.
    now: Contract numbers, DOC dates, premiums and status notes are reproduced verbatim:
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 175: Preserve and flag (⚠️) apparent typos or inconsistencies rather than silently correcting them.
    now: Apparent typos or inconsistencies are preserved and flagged with a flag.
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 176: If a contract number in the source header looks like a policy number rather than a client ID, flag the discrepancy.
    now: notes that look lost, an outstanding item never actioned, a header number that looks like a policy number rather than a client ID.
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 177: Flag scientific notation or truncated ID numbers as potentially imprecise — do not present them as exact.
    now: out.append("a number in scientific notation (%s) is probably imprecise:
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 178: Context is a fact, not filler.
    now: w.die('This is not a run folder (no %s).
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 178: When a client requests guidance on choosing between options ("which product should I use?"), the available options themselves (by contract number and product type) are data-integrity items.
    now: """Reads a client document's text (PDF or HTML/text), page by page, and checks that what the chat entered really appears in it.
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 178: Omitting them ("client requested withdrawal") loses critical information that may drive subsequent advice or compliance decisions.
    now: "Earlier Client Records of the same client that Paul gives you (for the duplicate check):
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 178: which products are in play, what the advisor is considering, what decision is pending.
    now: Keep what the notes hold (condensed), or list it in left_out with a reason Paul will see."
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 179: "Do not call" / "Do not contact" instructions:
    now: out.append("DO NOT CONTACT lines reproduced in full:
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 179: always reproduce prominently with a ⚠️ flag at the top of the Notes section.
    now: "Do not contact" lines are reproduced in full and flagged at the top of Notes.
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 183: Recognise these abbreviations when they appear in source notes — reproduce them as given, don't expand or reinterpret them:
    now: reproduce them as given, never expand or reinterpret them (the program refuses a record that expands one).
    why: Kept as a leave-as-written list; four meanings marked not confirmed (Paul agreed).
- old line 187: RGAR — Retirement Goal Analysis Report
    now: "Retirement Goal Analysis Report", "NTU":
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 188: NTU — Not Taken Up (a proposed policy that never went into force)
    now: A dependant's linked policy details go under that member's entry.
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 189: DOC — Date of Commencement (of a policy)
    now: the date %s is not the date of entry %s (%s)" % (who, key, frm, ", ".join(ekeys)))
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 191: ECBU — Extended Cover Benefit Upgrade (BrightRock)
    now: "Extended Cover Benefit Upgrade", "ICB":
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 195: Section 14 transfer — statutory transfer of retirement fund benefits between funds
    now: FNA (Financial Needs Analysis), FF (Fact Find), RGAR (Retirement Goal Analysis Report), NTU (Not Taken Up:
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 196: Broker of record — the adviser/brokerage formally appointed on a policy with the insurer
    now: out.append("Left out of the record on purpose (with the reason):
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 197: Paid-up policy — a policy where premiums have stopped but reduced cover continues
    now: P.append("a 'do not contact' line is in the raw notes but not reproduced in full in the Notes bullets:
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 198: Msign — the practice's e-signature platform
    now: a copy in the client's folder only when Paul asks",
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 199: PMA report — a policy/portfolio management/analysis report
    now: "Retirement Goal Analysis Report", "NTU":
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 200: GPMR — a further portfolio/management report type used in reviews
    now: GPMR, PMA report, BSC Personalised, GCS monthly run.
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 202: IRR/ROR — Internal Rate of Return / Rate of Return
    now: the date %s is not the date of entry %s (%s)" % (who, key, frm, ", ".join(ekeys)))
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 203: BSC Personalised — a BrightRock personalised cover product/report
    now: Categories exactly as stated (Client, Client / BrightRock Lead, Client / Non-Replacement).
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 204: GCS monthly run — a recurring monthly commission/compliance run
    now: 2 | What a finished run contains | The .md record, the short audit and the block for Paul |
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 208: Recognise these names when they appear by first name or role only in source notes, and preserve their role context in the summary:
    now: *Key contacts (recognise them by first name or role only, and keep their role context in the summary):
    why: Kept.
- old line 210: handles follow-up and admin coordination
    now: if e["key"] and any(e["n"] in (b.get("from") or []) for b in blocks):
    why: Kept.
- old line 211: SR — support/service representative (internal shorthand)
    now: return "%sR %s.%s" % ("-" if d < 0 else "", " ".join(groups) or "0", frac)
    why: Kept.
- old line 212: Alwyn Van Tonder — Old Mutual BC (external)
    now: old = load_run(a.run)
    why: Kept.
- old line 214: Lizelle Cachado — BrightRock underwriting (external)
    now: Pat Samplecase (Client / BrightRock Lead) (ID number)
    why: Kept.
- old line 215: Cameron Maritz — Vision Insure, short-term insurance referrals (external)
    now: Medical Aid / Short Term Insurance:
    why: Kept.
- old line 216: Amber Strydom / Bianca Swart — Capital Legacy (external)
    now: follow-up and admin), SR (support or service representative, internal shorthand), Alwyn Van Tonder (Old Mutual BC, external), Martin Oelofse (BrightRock, external), Lizelle Cachado (BrightRock underwr
    why: Kept.
- old line 217: Valerie Swanepoel / Laura-May Strydom — medical aid administration at Hampshire (external)
    now: Medical Aid / Short Term Insurance:
    why: Kept.
- old line 219: The practice records/tracks across AdviceTech (CRM), Astute, Msign, Microsoft Planner (task tracking, embed Planner links in Notes entries per the rule above), and MyClient — recognise references to t
    now: Recognise references to them as platform names, not client-specific detail.
    why: Kept.
- old line 248: (...continue through all 18 fields in order...)*
    now: *Layout example (the program draws all 18 fields;
    why: Kept as a shape; the program draws the real record.
- old line 258: Paul took over as broker on BrightRock (contract no.), Sanlam Risk Cover, and Sanlam RA — broker change effective 19/02/2024.
    now: Paul took over as broker on BrightRock (contract no.), broker change effective 19/02/2024.
    why: Kept as a shape; the program draws the real record.
- old line 258: LOAs signed and sent for both.
    now: The last step prints the SHORT AUDIT and the block for Paul.
    why: Kept as a shape; the program draws the real record.
- old line 259: Feb 2024 approved request to add (family member) to the BrightRock policy was never actioned — BrightRock's records show zero servicing history on the policy.
    now: the Feb 2024 request to add (family member) to the policy was never actioned.
    why: Kept as a shape; the program draws the real record.
- old line 265: Old Mutual AML/compliance reminder ((reference no.)) — (Client) completed the required form to keep the portfolio active.
    now: An earlier record of the same client is shown to Paul and he decides before anything is merged.
    why: Kept as a shape; the program draws the real record.
- old line 267: (Note how each bullet is condensed to one line but still carries the contract number, effective date, and outstanding-item flag — nothing from the original is lost, it's just phrased tightly.)*
    now: The Notes section is condensed into concise, scannable bullets, but every material detail (facts, figures, dates, names, decisions, outstanding items, instructions) must still appear.
    why: Kept as a shape; the program draws the real record.
- old line 277: Old Mutual – Pension Preservation (March 2019)
    now: BrightRock – Personal Covers (March '20)
    why: Kept as a shape; the program draws the real record.
- old line 280: ## Final checklist before outputting any record
    now: An earlier record of the same client is shown to Paul and he decides before anything is merged.
    why: The 12 boxes ticked by eye became program checks.
- old line 282: [ ] All 18 fields present, in correct order
    now: P.append("the 18 field labels are not all present, once each, in the fixed order")
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 283: [ ] Every field label bolded, value on the line below
    now: a header line, then the 18 fields each with a bold label and its value on the line below,
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 284: [ ] Horizontal rules between all sections
    now: P.append("a horizontal rule is missing between sections")
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 285: [ ] All three Life & Investments sub-sections present
    now: li = fields.get("Life & Investments") or {}
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 286: [ ] Notes in chronological order with BOLD ALL CAPS date headings, condensed into concise bullets — with zero facts/figures/decisions dropped
    now: The Notes section is condensed into concise, scannable bullets, but every material detail (facts, figures, dates, names, decisions, outstanding items, instructions) must still appear.
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 287: [ ] Multi-part client requests captured with full context:
    now: Multi-part requests and advisor decision-points (CRITICAL).
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 287: what is being asked, which products/accounts are in scope (by contract number), what options the advisor is considering, and what decision is pending — DO NOT omit "which X to do Y from" details
    now: every date, amount, percentage, number, contract code, ID, email, link, name and abbreviation of each raw entry stays in the record, or is listed as left out with a reason Paul sees.
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 289: [ ] No invented or inferred information
    now: "no earlier record matches, or Paul's decision is recorded in his own words"
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 290: [ ] Missing fields stated as "Not recorded."
    now: A field the notes do not state reads Not recorded.;
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 293: [ ] No closing sign-off line
    now: There is no closing sign-off line at the end of the record.
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).
- old line 294: [ ] If this is a redo of an existing client record with new source material, it's a full redo — not a patch
    now: When Paul supplies substantial new source material for a client who already has a formatted record, produce a full redo of the record incorporating it:
    why: Each formatting rule is a program rule or check; Not recorded. everywhere (Paul agreed).


DROPPED (each is covered by a recorded decision):
- ## Index: Replaced by the new short Index (five sections).
- 2 | Last updated + Changelog | Athens-time stamp, last 5 changes, stan: The stamp is set by tools/stamp_skill.py, never typed (S2); the changelog is archived in this history folder and the pointer to the Project file client-review-notes-changelog.md is dropped (Paul agreed, 04/11/2026).
