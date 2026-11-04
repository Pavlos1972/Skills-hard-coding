# client-review-notes: what changed, and what I need from you (04/11/2026)

No client data is kept in the new skill. Everything in it is invented (Pat Samplecase, Robin Testcase, the invented insurers Samplelife, Testco and Samplecover; every ID number in the test is computed, never typed). The old text is archived in `SKILL.2026-10-14.md` (no client data in it). The rule-by-rule check of the old skill against the new one: 203 rules, 0 unaccounted (12 kept word for word, 123 reworded, 68 dropped with a recorded reason; see `INVENTORY-REPORT.md`).

## What it is now
A program holds the Client Record as ONE data file and draws the `.md` itself, in the fixed layout, every time. The chat summarises; the program checks the summary against the raw notes. A checker rebuilds everything and compares, so a Markdown file edited by hand cannot pass. Nothing is invented: what the notes do not state reads `Not recorded.`. Your 12 Phase A answers are all built in.

## What I built into it (your Phase A answers)
- The raw notes are pasted or attached and registered as the ONLY source (a fetch through the routes is possible, logged, and unproven). They are served in parts, in order, and each part is acknowledged.
- The program draws the header and the 18 fields in the fixed order (bold label, value on the next line, a rule between sections, `Not recorded.` with a full stop everywhere, no sign-off, no HTML), the Life & Investments lists in the exact policy line format, Commission, and Notes under BOLD ALL CAPS date headings, oldest first (a day heading when the entry has a day, a month heading when it has only a month).
- It PROVES every verbatim item (names, categories, ID, tax number, each policy's contract, product, DOC date, premium and status, each commission line) is character for character in the raw notes.
- **"Zero facts dropped" is now a check:** every date, amount, percentage, number, contract-like code, email, link, name and abbreviation of each raw entry must be in the record, or listed in `left_out` with a reason you see. A request that names several contract numbers cannot lose them silently any more.
- Flags at the top of Notes, found by the program: two numbers one character apart (apparent typo), a number in scientific notation, an ID that fails its check digit or has the wrong length, timestamps that look system-generated. A "do not contact" or "do not call" line is found by phrase search, reproduced in full in its dated bullets, and a record without it is refused.
- Abbreviations are never expanded (the program refuses an expansion). Planner links must read `[Planner – Task Name](URL)`.
- Earlier records of the same client: you give the program the earlier `.md` files; a matching name or ID stops the run until you decide, in your own words, to merge or keep them apart; a merged record must keep everything from both and say what each version added.
- The file is delivered in the chat as `Client Record - DD.MM.YY - First Surname.md`; a copy goes into the client's folder only when you ask. No confirmation step, as today.
- The reply is the short audit (12 lines) and a block for you: what was left out on purpose, and the flags.

## Questions that came up while building (Yes / No, recommended answers in brackets)
1. **The coverage check is strict on names too:** capitalised words and abbreviations of each raw entry must appear in the record (or in `left_out` with a reason). On real notes this may ask for a few `left_out` lines at first. If a kind of word turns out to be noise, tell me and I will drop it from the check. (Yes)
2. **The "apparent typo" flag fires on ANY two numbers one character apart**, even an Income Tax Number and a contract number (it did exactly that on my invented client). It is only a flag at the top of Notes, never a refusal. (Yes)
3. **The record keeps the full ID and tax number** in the header and the fields (they are verbatim fields and always were); the audit and the block for you mask ID-like numbers to the last 4. (Yes)
4. **The "do not contact" warning shows the whole raw line** (with its date), not just the instruction. (Yes)
5. **Still open from Phase A (question 1):** I built the entry splitting for the usual date layouts (14/02/2022, 2022-02-14, 14 Feb 2022, MARCH 2024) with a whole-note fallback, because I have not seen what your raw notes look like. Please send ONE invented sample of a raw note; with it I can make the entry-by-entry check exact. (Send the sample)

## What no program can close
- That each summarised sentence keeps its MEANING (the program proves the figures, dates, names and links are kept, not the wording).
- That the Outlook notes are complete and right, and which facts count as filler.
- How a real conflict between two duplicate records should be resolved (it asks you).
- If the raw notes carry no recognisable dates, the program checks the whole note instead of entry by entry, and the audit says so.
- I have never seen a real set of raw notes, so the first real run may need one fix.
