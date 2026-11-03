# The final re-verification pass

## Step 3a: Mandatory final re-verification pass — the whole transcript and the whole Audio to Text file, not just the flagged fields

**This is a required checkpoint, not an optional quality pass.** Before moving to Step 6, re-read the **entire** source transcript(s) start to finish at least once more, and re-read the **entire** Audio to Text file (PDF and JSON) against the draft, checking:

1. **Every field marked "Not discussed"** — re-confirm against the Audio to Text file, the transcript and the Overview, and check the client's other documents.
2. **Every "see flag" / "see notes" cross-reference** — confirm it exists.
3. **Any new ambiguity flag** — be sure a source itself supports it.
4. **Client Info contact fields and Referral From** — confirm Step 1c was done against the Audio to Text file, the transcript and the documents.
5. **Point form and prior-year currency (Step 4)** — confirm no field value is a dense multi-fact paragraph, and no prior-year figure is shown as current without reconfirmation.
6. **Any policy number appearing in more than one source document** — confirm it was resolved against the actual policy schedule.
7. **Any FNA, Shortfall, or Reduced quote** — confirm it names the insurer AND says New Business or Servicing explicitly, that both came from the Audio to Text file/Paul (or his answer to the question in Step 3) and not from a default, and that the word "Servicing" appears only where Paul actually asked for it.
8. **Any quote/report request paired with a separate document request** — confirm neither is wrongly worded as conditional on the other unless the transcript/Paul actually said so (per Step 3's rule).
9. **The Planner note (Step 7b)** — confirm it was made by the Teams transcript program (its checker says PASS), that every action is written as `Sitamah to ...`, that setting up the follow-up appointment is an action when one was asked for, and that it is presented as its copy-ready page (not chat text or a code block).
10. **Audio to Text cross-check** — go through the Audio to Text file field by field, PDF and JSON: every populated value (whatever its status) must appear in the Fact Find, or be flagged as a difference with the transcript/Overview/documents; no `empty` field has been mistaken for an answer; every `preset` entry (and every `heard` and `verify` entry in an older file) is listed in the source report; the schema version was checked (Step 1b, point 7); the `unplaced` list was not processed; and the company look-up text was checked (Step 1b, point 10).
11. **Standing ABIs (Step 3)** — confirm the Life cover fractured block reads Life Cover (WOL) ABI 3% and Childcare ABI 5%; the Permanent disability fractured block has NO Life Cover (WOL) ABI line, reads Household needs ABI 5% and Childcare ABI 5%; Dread Disease ABI is 3% (unless Paul stated otherwise); and the Summary's Section 8 shows the same.
12. **Two spouses (Step 1d)** — confirm each spouse's set contains only that spouse's own information plus the common debts, children and joint policies, that the cross-check search was done, and that each set was saved to that spouse's own folder.
13. **Overview cross-check** — policies, numbers, premiums, cover amounts and group risk/retirement figures compared with the latest Overview; every difference flagged.

**Named precedent — a caution against overcorrecting, not a caught fabrication:** [client E], 14 September 2026. This step exists to catch genuinely missed, fabricated, or dangling content, not to relitigate a value that's simply unfamiliar or briefly unclear elsewhere in the recording. Only flag a specific, already-stated value when a source gives a concrete reason to doubt it.

This pass is in addition to, not a replacement for, the transcript-accuracy re-check that `fact-find-summary` performs later in the chain (Step 7a).

## What the program proves and what only you attest

Proved by `verify.py` (PASS or FAIL): items 1 (every Not discussed is searched again; an override of the search rests on a written reason that the program checks only for length, a cited hit line and a word from it), 2 (every see flag or see notes points at something that exists), 4 (contact fields and Referral From), 5 (one fact per line, prior-year pairs), 6 (policy numbers only from a policy schedule), 7 (insurer and New Business or Servicing), 10 (every populated form value is in the Fact Find or flagged), 11 (the standing ABIs), 12 (the other spouse's data) and 13 as far as a recorded document has a text copy (the copy is made by the chat: the program checks that it names the client and that quoted words and figures are in it, not that it is the real document). Attested by you, in your own words, in `run.py receipt` (the judgment sentences): items 3, 8 and 9, the Overview comparison and the other documents.
