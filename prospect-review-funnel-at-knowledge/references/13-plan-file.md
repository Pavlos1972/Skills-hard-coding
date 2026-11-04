The plan file is one JSON file you write; the program checks it. Every value comes from the documents or from Paul's words; nothing is invented.

```
{
 "decision": "Decision 56 – short name of the change",
 "paul_request": "Paul's own words that asked for it",
 "stages": ["A6d"],
 "documents": [ {"role": "streamlined", "change": "what changes in it"}, {"role": "master_plan", "change": "..."}, {"role": "register", "change": "..."} ],
 "documents_unchanged_reason": "only when no document changes",
 "objects": [
   {"type": "checklist", "id": 233, "title": "MP35 – exact AdviceTech title", "stage": "G5b", "expect_lines": 2,
    "lines": [ {"text": "SR – Monitor progress on all open sub-tasks", "kind": "action"},
               {"text": "SR – AUTOMATION: MOVE THE TASK TO COLUMN \"G6\" — TICK DONE TO OPEN BELOW", "kind": "automation"} ]},
   {"type": "section", "id": 104, "title": "G5b — Sub-tasks Running (SR)", "stage": "G5b"} ],
 "tick_path": [ {"module": "MP35", "line": "the line to tick", "opens": "MP5", "expect_lines": 12} ],
 "client": "Mr John Snow",
 "next": "what comes after this batch"
}
```

- Kinds of run: build uses `documents` and `objects`; test uses `client` (Mr John Snow only) and `tick_path`; docs and review use `documents` only.
- `type` is checklist, section, board, category or subcategory; `id` is the AdviceTech number. Charl's checklists #7, #8, #9 and Sections 15 and 16 are refused.
- A checklist lists every line, with `expect_lines` equal to the number of lines. Line kinds: action, received (ends "— Received"), yesno (ends "– YES / NO?"), applicable (ends "— if applicable"), question (contains "QUESTION:" and ends "TICK DONE = YES / SKIP = NO"), automation (contains "AUTOMATION", in CAPITALS outside quotation marks, ends "— TICK DONE TO OPEN BELOW", "— IF THE ANSWER BELOW IS YES" or "— WHATEVER THE ANSWER BELOW"), subheading and outcome (in CAPITALS, no owner).
- Every line except a subheading or an outcome starts with "SR – ", "PK – " or "CL – " (en dash). SR and PK lines are never mixed in one checklist (CL lines excepted).
- No "Claude" in any AdviceTech name. A Section name ends with its owner in brackets.
- Every stage in `stages` and in an object must have been named with `run.py stages`, so its quoted lines exist.
