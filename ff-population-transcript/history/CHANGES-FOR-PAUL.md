# ff-population-transcript: what changed in v40 (06/11/2026)

Nothing here is live until you confirm it.

## What your second real run (Roquelle Damir, v39) showed, and what v40 does
| Problem in the run | What v40 does |
|---|---|
| Five "Allow once" boxes: four were the chat's own Python heredocs patching `overlay.json`, one was the pass-2 loop. | The skill says: change `overlay.json` with the Edit or Write tool, never a shell command; no loops. `run.py combine` already lists up to 25 problems in ONE go, and the rules that caused the rounds are now written BEFORE the chat writes (next row). |
| Too slow: about 75 tool calls, five combine rounds, two builds, about 55 notes rewritten. | The "one fact per bullet" rule moved from the build step to the combine step (written once). The overlay rules are listed before writing. A form-PDF quote may now have other columns' words between its words (the check was failing on column order). |
| The second transcript pass was a light check (`tail -n 3`). | **You decided: read once, but accurately.** The program shows each chunk in full and names a line from the MIDDLE of it; the next chunk is released only if the chat repeats the first 5 words of that line. A `tail`, `head` or `grep` shortcut cannot pass. The audit says "read once, every chunk checked". The program still cannot prove the text was understood: the quote check does that for what is quoted. |
| Lines of the real form were missing from the report: Lump Sum Disability household income, childcare and debt lines, the Instalment protector, Rental, Spousal and Child maintenance income, Total income, "Priorities to be focused on". | I compared the layout with the real 11-page PDF text and added those rows (the disability lines and Total income are worked out by the program the same way as the life-cover block). Anything else the layout does not know still appears under "Other fields from the form", so no value is lost. |
| The computer save failed once: it needs a staged path under `/mnt/user-data/outputs`. | `run.py build` copies the PDF there and prints the exact path to give `device_commit_files`. |

## Still true from v39
- Your permission and the two exact folders are written into the skill. The computer connection worked in the second real run.
- BOTH files of the Audio to Text (data file and PDF) are read as exact copies, plus the Teams transcript; a `.docx` is read by the program itself.

## Not proven until your next real run
- The number of "Allow once" boxes (the chat's own heredocs and loops were the cause last time; the skill now forbids them).
- That the reading check is accepted smoothly: each chunk needs one extra word-check on its next command.
- The new rows on a real form: the disability lines are worked out from take-home income, childcare and debts; the Instalment protector lines are filled from the form's PDF by the chat.

## The four Yes/No questions still open (from v38)
1. **One stop only:** the run pauses once, for you to read the Fact Find PDF; then the Summary, Planner note and Sitamah message run by themselves. Recommended: **Yes** (you did not object).
2. **"Not discussed":** the chat is shown the list of empty rows once and must search the call, the Overview and the documents before leaving any; the program no longer demands a written claim per row. Recommended: **Yes**.
3. **Amounts only the PDF holds** are printed in a block at the end of the report with the PDF's own labels (never lost). The chat may also place one in its proper row. Recommended: **Yes**, and we look at the first real PDF to see whether you want them placed in rows automatically.
4. **A couple in one meeting** is two runs, the second started with `--other-run <the first run folder>`. Recommended: **Yes** (no extra check program for the cross-search; it stays a written rule).
