# ff-population-transcript (program-driven)

Builds the Fact Find Transcript PDF after a Fact Find meeting. See `SKILL.md` for the short entry page and `history/CHANGES-FOR-PAUL.md` for what changed, in plain words.

| Program | What it does |
|---|---|
| `scripts/run.py` | The step driver: shows one step at a time, refuses to skip, keeps the run on disk, logs the access routes, records Paul's answers, runs the claim/cross-check/lead/join/receipt commands |
| `scripts/ffform.py` | Reads the Fact Find form's data file (`app` = `wr-fact-find`, schema 3.0) and checks its saved PDF |
| `scripts/tx.py` | The two-pass reading lock for the transcript (the Teams skill's, plus a check of each part of a joined transcript) |
| `scripts/compose.py` | Writes `content.json` from the form, the overlay Claude writes and the recorded answers; applies the standing rules |
| `scripts/build.py` | Draws the PDF with reportlab and renders the page images; reports the font really used |
| `scripts/verify.py` | The one checker: PASS/FAIL per group, source report, glance list, proven versus attested |
| `scripts/layout.json` | The 11 sections, their labels, the standing values and the reconcile rules (program data) |
| `steps.json`, `deliverables.json` | The steps with their proofs, and the list of outputs |
| `references/` | The rule pages the driver shows at the step that needs them |
| `tests/` | Tests on invented people only (`python3 -m unittest discover -s tests`) |
| `history/` | The old skill text, the records that prove no rule was lost, the change list for Paul |
