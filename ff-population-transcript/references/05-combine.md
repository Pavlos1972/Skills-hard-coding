# Combining the form and the call into ONE report

The Fact Find Transcript is ONE report made from BOTH sources: the form's data file and PDF, and the Teams transcript (with the Overview and the client's documents as reference). The program copies the form's values; you write only what the call and the documents ADD, in `{run}/overlay.json`. `run.py combine` checks it and makes `content.json`; run it as often as you like.

## Rules for writing the overlay (the program checks them; read them BEFORE you write)
- **Every note, flag and fill is point-form: ONE fact per entry. Never run several facts together in one note.** This is a hard, universal rule across every output this skill chain produces, with no exceptions. **Named precedent:** [client A], 07.10.26: the first draft packed multiple facts into single paragraph cells; Paul called it out as "cluttered".
- Every entry needs an `id` and a `src` (a call line with the exact words, or a named document). `documents_to_request` and `next_steps` are lists of objects: `{"id": "n1", "text": "...", "src": [...]}`. A diff `key` must be a field of the form (the program lists the valid ones). A quote `group` must be one of the listed groups.
- **Change `overlay.json` with the Edit or Write tool, never with a Python heredoc or any other shell command** (every such command asks Paul for a click). `run.py combine` lists up to 25 problems in ONE go: fix them all, then run it again.
- A quote taken from the form's PDF (`{"doc": "form PDF", "quote": "..."}`) may have other columns' words between its words; keep the words in their order.

## What you write (every entry has an `id` and a `src`)
A `src` is the call's exact words, `[{"line": 12, "quote": "the exact words"}]` (the program checks they are in the transcript), or a document, `[{"doc": "Overview", "quote": "..."}]` (not machine-checked: it is counted on the audit).

- `fills`: a gap the form leaves empty. `{"id": "f1", "key": "edu_notes", "value": "...", "src": [...]}`. `key` is a form field (`edu_notes`) or `list.row.column` (`debts.0.notes`; numbering starts at 0). The program tells you the valid keys when one is wrong.
- `rows_add`: a list row the form lacks (a debt, a child, a policy): `{"id": "r1", "list": "debts", "cells": {"type": "...", "prov": "..."}, "src": [...]}`.
- `diffs`: a CONTRADICTION between the form and the call or a document. `{"id": "d1", "key": "edu", "other": "what the call/document says", "label": "the call", "src": [...]}`. Add `"settled": "<the rule that settles it>"` and it is SORTED (for example: "the policy schedule decides"); leave it out and it is HIGHLIGHTED: the report shows both values and where each came from, and Paul decides. The form's value stays in the report either way (the Audio to Text file wins); only a standing rule changes a value.
- `notes`: the call's extra context for a section (`"section": "income"`, `"text": "..."`): reasons, who pays what, timing, plans. `flags`: something Paul must check (`"section"`, `"text"`).
- `clean`: a line of a form note that is chatter, not a fact: `{"id": "c1", "key": "n_will", "drop": "<the exact line>", "reason": "chatter"}`. (Lines that only repeat another field are dropped by the program; a note cut off in the middle of a sentence is flagged.)
- `quotes`: for every FNA, Shortfall or Reduced quote request whose insurer or basis the form does not hold: `{"id": "q1", "group": "fna", "insurer": "...", "mode": "New Business", "src": [...]}`. If neither the form nor the call says which, ASK Paul in one message and use his words.
- `policy_numbers`: `{"id": "p1", "found": "<the number in the form>", "resolved": "<the number on the policy schedule>", "ref": "<the schedule>", "quote": "..."}`.
- `abi_override`: only when Paul states a different ABI for this client: `{"id": "a1", "key": "dd_abiv", "value": "5%", "paul_said": "his exact words"}`.
- `documents_to_request`, `next_steps` (what the CLIENT must do), `joint` (a joint policy: `{"id": "j1", "list": "risk", "index": 0, "with": "Robin", "src": [...]}`), and `lookup` (the replacement text for a thrown-out company look-up, from the call).

## Sorted or highlighted
Every contradiction is settled by a rule or shown with both values. Never pick the call's value silently and never drop the difference. A difference only in spelling, format or level of detail is not a contradiction: use the fuller, cleaner value and do not record it.
