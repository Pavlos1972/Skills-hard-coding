Run `run.py fill`. The program fills a copy of the real blank form (or, for a correction, a copy of the current application with ONLY the planned fields changed), sets NeedAppearances so every viewer draws the values, writes `out/<file name>.pdf`, and then checks its own work:

1. **Read-back of EVERY field.** Each field of the saved PDF is compared with what was intended; a field that was not filled must be empty.
2. **The render.** The filled form and the blank form (or the application before the correction) are drawn and compared box by box: every filled box must look different. This proves something is drawn in the box; it does not read the text. If a dropdown value is set but does not draw, that is a viewer or appearance issue, not necessarily a data error: say so plainly in the hand-back, do not claim the render passed, and ask Paul to confirm it displays in his own viewer.
3. **A correction** also proves that only the planned fields changed and the signature fields are untouched.

If the blank form has changed (its checksum, a field, a type or a dropdown option), the program stops: tell Paul. Never fill an unknown form and never re-derive the General form's field meanings during a run (that table was made once by hand from positions and labels).
