# The WR skill template (APPROVED by Paul, 02/11/2026, as it is)

Every skill we convert is measured against these 13 ingredients. A skill with an ingredient missing is not finished.
Source: `SKILL-STANDARDS.md` (S1 to S16) and what Paul asked for while the Teams transcript skill was built and trialled (29/10/2026 and 30/10/2026).
The Teams transcript skill has all 13 and is the working model: `client-teams-transcript-skill/`.

## The 13 ingredients

| # | Group | Ingredient | In plain words | Proven by |
|---|---|---|---|---|
| 1 | Starts right | Short entry page | SKILL.md is short: Index, "Last updated" stamp set by a program, last 5 changes, standing rules one line each. Detail lives in pages shown at the step that needs them. | lint |
| 2 | Starts right | Inputs from the file first | The client's file first, found AUTOMATICALLY the way the original skills did: the device bridge to Paul's computer first (list, stage, commit; no shell commands), then the Microsoft 365 connector, then Zapier (changed 06/11/2026, Operation Skill Restructure 2.0). Paul is never asked to click, attach, upload or drag anything; he is asked only for what no file holds. | access log, checker, the upload chat's access check |
| 3 | Does the work | Step driver | A program shows one step at a time, refuses to skip, keeps the run on disk, says the skill's version first. | driver tests |
| 4 | Does the work | Reading lock | Long sources are served in order, read twice, each part acknowledged before the next. | reader tests |
| 5 | Does the work | Evidence | Every item cites its source (quote or document), every figure is traced, differences are flagged, nothing is invented. | checker, group C |
| 6 | Produces | Built by program | Every output (document, page, message) is built from one data file, never hand-written. Names are derived. No client data inside the skill. | build tests, privacy scan |
| 7 | Produces | Short means short | Size limits are enforced (words per line, bullets per area, pages). | checker, group L |
| 8 | Produces | Sorted actions | Each action is now or later, in order (earliest deadline first, then logical), sifted for relevance, with a never-list; when unsure the skill asks Paul and records his words. | checker, group L |
| 9 | Proves and ships | One checker | PASS/FAIL, a "what Paul should glance at" list, and an honest split between proven and only attested. | checker tests |
| 10 | Proves and ships | One reply, a quiet run | One version sentence, short progress lines while working, no opening recap; the reply holds the outputs and the SHORT audit. A question only for what no file holds. Nothing is sent without Paul's yes, except what he made automatic in writing (the message to Sitamah of the Fact Find chain, posted through Zapier). | step texts, receipt checks |
| 11 | Proves and ships | Tests | Tests on invented data; every real bug becomes a test. | the test suite |
| 12 | Proves and ships | History outside | Old rules archived, a program proves no old rule was lost, removals go to Paul as a yes/no list. | inventory = 0 |
| 13 | Proves and ships | Package and upload | A zip made only if lint and tests pass, an upload brief for the Chrome chat, a before and after test, "live" only when Paul says so. | packaging, brief tests |

## Scorecard (mark each ingredient: full / partial / missing)

| Skill | Full | Partial | Missing | Notes |
|---|---|---|---|---|
| client-teams-transcript-skill | 13 | 0 | 0 | live since 30/10/2026 |
| ff-population-transcript (studied 30/10/2026) | 0 | 4 (1, 2, 5, 12) | 9 (3, 4, 6, 7, 8, 9, 10, 11, 13) | before the rebuild; see SKILL-STANDARDS.md section 8b |
| ff-population-transcript (program-driven build, 03/11/2026) | 11 (1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12) | 1 (13, until packaged and uploaded) | 0 | ingredient 8 (sorted actions) does not apply: this PDF has no action list; the follow-up appointment is carried and checked in the Teams run. 5 and 10 are full for what a program can check; what only Claude can attest is printed on every run. NOT live |

## Settled once, applies to every skill (do not ask Paul again)

- The eight planning areas and their order; "Other" only when notable. Each its own heading.
- The Planner note is a private copy-ready page, never a code block, built by program. One-line bullets (3 per area at most, 20 words), only the actions for now.
- The PDF: 4 bullets per area (45 words), two pages at most. Next Steps are the client's only.
- Actions are all `Sitamah to ...`. Never an action: what the client decides, cancelling credit life, sending quotes or the what's-next email, Paul's own steps. A cession is a later action. Setting up the follow-up appointment IS an action for Sitamah at every meeting (Paul, 02/11/2026: she books it, or sends the Teams meeting request).
- The message to Sitamah: `Name Surname (Review Client|Prospect) - Nth Teams Appointment Completed: DD/MM/YYYY ...` (WhatsApp: `WhatsApp Call Completed`), label from where the client's folder sits, shown with the outputs in the one reply, **posted automatically through Zapier in the Fact Find chain (Paul, 05/11/2026)**, once per meeting. In every other skill a message or email is sent only after Paul's yes until he says otherwise.
- Client facts come from the client's file first, ask Paul last. Files are found automatically the way the original skills did: the device bridge to Paul's computer first (no shell commands, no fingerprints, no hard STOP), then Microsoft 365, then Zapier. Never a permission gate, never "attach the file" (Paul, 06/11/2026, replacing the 05/11/2026 wording).
- A quiet run and the SHORT audit as the program's own final printout, in every skill (Paul, 05/11/2026).
- Outdated text: dropped when clearly replaced, a yes/no list to Paul for anything uncertain. The short true stories in the rules stay (names removed).
- A skill says its version first; the date moves only when the skill really changes.
- A new version is uploaded by a Chrome chat using the brief the packaging program writes: the skill is replaced, the old version stays in its version history, tested before and after.
- `planner-interim-procedure` is forgotten.
