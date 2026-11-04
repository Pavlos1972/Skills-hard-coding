# Step 3: The scope, the second life, the basis, the voice and the sections

**Run `run.py scope`.** It prints the lines of the client's own notes that mention each benefit category (the program found them; a hint, never the verdict). Then write `scope.json` and run `run.py scope --file scope.json`.

**The benefit scope is a mandatory gate.** A client very often asks for only some of the benefit categories on an insurer's quote (life cover only, with severe illness or disability deliberately left out for budget or personal reasons). The quotes themselves still show R0 or "not selected" lines for the left-out categories, or omit them: neither is a safe signal. Never infer scope from which categories merely appear with non-zero values. Read ALL the Follow-Up Appointment Summary Notes (more than one, across different meeting dates), the Fact Find Summary and the WR Overview, and decide for each category (life cover, severe illness / dread disease, disability, income protection, debt cover, childcare / education) whether the client asked for it. Look for language saying a category was deliberately excluded ("elected to remove disability from his proposed option", "did not include this due to budget constraints"): it is a stronger signal than any quote's own R0 line. The program marks such lines `[EXCLUSION LANGUAGE]`.
- The confirmed scope governs every section without exception. A category outside it appears nowhere: not as a comparison row, not as "not selected on this proposal", not as an R0 entry, not in definitions, not in the verdict, not in the email.
- If the notes are silent on a category, do not guess: ask Paul which to include, saying what was and was not found, and put his own words in `paul_said`.
- If the notes conflict (one meeting note against a later one, or the Fact Find against the follow-up notes), name the conflict to Paul and ask him to confirm; never silently pick the more recent or more generous reading.
- **Terminal illness** is intrinsic to the death benefit, not a separate category: it stays in scope even when severe illness and disability are out.

**scope.json**
```
{"categories": {"life":            {"status": "in",  "source": "intake_notes_2026_10_02", "evidence": "<a verbatim line of that document>"},
                "severe_illness":  {"status": "out", "source": "...", "evidence": "..."},
                "disability":      {"status": "out", "paul_said": "Paul's own words"},
                "income_protection": {...}, "debt_cover": {...}, "childcare": {...}},
 "second_life": {"present": false}   or   {"present": true, "name": "Robin", "source": "...", "evidence": "..."},
 "basis": "like-for-like" | "against-proposal", "basis_source": "where this comes from (the board's question, Paul's words)",
 "voice": "first_person" | "third_person",
 "sections": ["premium_snapshot", "cover_comparison", "escalation_table", "loyalty", "definitions", "verdict", "sources"]}
```
All six categories are always listed. Life cover is always in.

**Second life.** Is there a second life on any policy (a joint-life or second-life-assured structure on any side, not necessarily a separate spouse policy)? If yes, every side must say whether the second life has independent cover or is a rider on the main policy; a rider is entirely dependent on the main life's policy staying in force. Compare the second life's cover across every insurer, even where an insurer provides nothing for them (say so), restricted to the in-scope categories. It is folded into the cover comparison, not given its own heading.

**Basis.** `like-for-like` (a fresh quote from the client's current insurer against the existing policy) or `against-proposal` (the new insurer's proposal against the existing policy). The board asks Paul which; record his answer. It goes in the Teams message for the board's Actions Taken line.

**Voice.** Default: Paul's own first person ("I've put together...", "I recommend...", "my proposal"), his standing preference since 23/09/2026. The alternative is the institutional third person. Either way the document is addressed to the client in the second person ("your policy", "your cover"): the voice only decides who is speaking. It applies to the banner, the commentary, the verdict, the salutation, the closing and the covering email alike.

**Sections.** Default: `premium_snapshot`, `cover_comparison`, `escalation_table`, `verdict`, `sources`. Add `loyalty` only when a quote has a loyalty/payback/bonus benefit. `definitions` is off unless Paul specifically wants definitions compared. The Header, the Key Facts Banner, the salutation and the signed closing are always built and are never asked about. Paul deliberately limits how much reaches the client to avoid overload: include extra detail only when it is genuinely material to this client's decision. A ticked section only shows in-scope categories; ticking "Cover Comparison" is no permission to show excluded ones.
