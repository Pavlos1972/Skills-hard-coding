# ff-population-transcript: what changed in v39 (Operation Skill Restructure 2.0, 06/11/2026)

Nothing here is live until you confirm it.

## What your first real run (Roquelle Damir, v38) showed, and what v39 does about it
| Problem in the run | What v39 does |
|---|---|
| The chat asked for your whole `liferisk.co.za` folder and the Auto-mode safety check refused it, so everything went through Microsoft 365 as text. | The skill carries your permission and names your two folders: **Folder 1** `~/liferisk.co.za/Company - Paul`, **Folder 2** `~/liferisk.co.za/Company - WR Clients/Paul Kafentzis (Client Files)`. One request, exactly those two paths, never the root. In the test you ran, the same two paths were granted. |
| The chat typed out the form's JSON itself (4+ minutes, and not a faithful copy: the real file is 31,539 bytes). | The files are staged from your computer as exact copies, so nothing is retyped. If the computer is refused, the chat says so with `--copied` and the audit shows "typed out by the chat, not byte-checked". |
| The Teams transcript arrived as one flat block and the program called it "not complete"; the chat re-cut it by hand. | With the real `.docx` staged, the program reads it itself (no pandoc needed) and keeps every paragraph as a line. |
| The form PDF was not used, so amounts only the PDF holds were missing. | The real PDF is staged too, so the program reads it whole. (The Microsoft 365 route reads a PDF in page ranges, which I proved on the real one.) |
| The chat improvised commands (`cp`, `sed`, a heredoc, opening the program's own file), each asking for a click. | The skill says: run only the commands the program shows. |
| "Not discussed" and the other open points | Unchanged: the four questions below. |

## Your decision on the JSON (06/11/2026)
You first said not to read the JSON. After I explained that the retyping was the problem and not the JSON, you said to go ahead and read it. So: BOTH files of the Audio to Text are read, as exact copies from your computer. Reading the JSON gives the exact fields and the confirmed / heard / preset / verify marks, which the PDF text does not show.

## If the safety check refuses again
Start your message with this sentence (your own words reach the check; the skill's text may not): "You may connect to these two folders on my computer: Company - Paul, and Company - WR Clients / Paul Kafentzis (Client Files), both under liferisk.co.za."

## Not proven until your next real run
- How many "Allow once" boxes a real chat shows. In v38 your screenshots showed one per command; v39 has fewer and simpler commands, but I cannot switch the check off. The next run counts them.
- That the real PDF's text reads cleanly through the program's PDF reader on your computer's exact copy (tested only on an invented PDF).
- If a transcript ever arrives flat (Microsoft 365 route), the program still stops; I did not build a re-cutter without a real sample.

## The four Yes/No questions still open (from v38)
1. **One stop only:** the run pauses once, for you to read the Fact Find PDF; then the Summary, Planner note and Sitamah message run by themselves. Recommended: **Yes** (you did not object).
2. **"Not discussed":** the chat is shown the list of empty rows once and must search the call, the Overview and the documents before leaving any; the program no longer demands a written claim per row. Recommended: **Yes**.
3. **Amounts only the PDF holds** are printed in a block at the end of the report with the PDF's own labels (never lost). The chat may also place one in its proper row. Recommended: **Yes**, and we look at the first real PDF to see whether you want them placed in rows automatically.
4. **A couple in one meeting** is two runs, the second started with `--other-run <the first run folder>`. Recommended: **Yes** (no extra check program for the cross-search; it stays a written rule).
