#!/usr/bin/env python3
"""Interim text edits to ff-population-transcript (Paul's decision 14, 02/11/2026). Every edit must match exactly once."""
import os
import subprocess
import sys

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ff-population-transcript", "SKILL.md")
t = open(P, encoding="utf-8").read()
STAMP = subprocess.check_output(["date", "+%Y-%m-%d %H:%M"], env=dict(os.environ, TZ="Europe/Athens")).decode().strip()


def rep(old, new):
    global t
    n = t.count(old)
    if n != 1:
        sys.exit("EDIT FAILED (%d matches): %r" % (n, old[:90]))
    t = t.replace(old, new)


# --- front matter + index -------------------------------------------------
rep('description: "Builds the WR Fact Find from the Fact Find (Audio to Text) file and the Teams transcript, using the latest Overview as a reference,',
    'description: "Builds the WR Fact Find from the Fact Find form\'s data file (named Fact Find (Audio to Text)) and the Teams transcript, using the latest Overview as a reference,')
rep("| 5 | Step 1 / 1b / 1d | Source order; how to read the Audio to Text file; Manual Fact Find as last resort; two spouses in one meeting |",
    "| 5 | Step 1 / 1b / 1d | Source order; how to read the form's data file (the Audio to Text file) and its schema check; Manual Fact Find as last resort; two spouses in one meeting |")
rep("| 12 | Step 7 | Chain: Summary PDF and Planner note Artifact page |",
    "| 12 | Step 7 | Chain: Summary PDF; Planner note made by the Teams transcript program |")
rep("| 13 | Step 8 | Notify Sitamah in Teams |",
    "| 13 | Step 8 | The message to Sitamah (made once, by the Teams transcript program) |")

# --- rule 11 ---------------------------------------------------------------
rep("    1. **FIRST and primary: `Fact Find (Audio to Text) - [date] - [Name Surname]`** (the PDF and its JSON). Every field starts from this file.",
    "    1. **FIRST and primary: the Fact Find form's data file, `Fact Find (Audio to Text) - [date] - [Name Surname]`** (the JSON the new Fact Find form saves, and its PDF; the name stays as it was - Paul, 02/11/2026). Every field starts from this file. Check its `schema` version every run (Step 1b).")
rep("whatever its status (`confirmed`, `heard`, `verify`, `preset`).**",
    "whatever its status (`confirmed`, `preset`; `heard`, `verify` in an older file).**")

# --- delivery gate -----------------------------------------------------------
rep("(3) the Planner / AdviceTech note (Step 7b) presented as a copy-ready Artifact page (own window, Copy note button, exact planning-area formatting);",
    "(3) the Planner / AdviceTech note (Step 7b) made by the Teams transcript program and presented as its copy-ready page (own window, Copy note button);")
rep("(6) once (1) to (5) are approved and saved, the Teams message to Sitamah (Step 8) sent via the Zapier route and the send confirmed.",
    "(6) the Teams message to Sitamah (Step 8), made by the Teams transcript program, shown in the same reply as (1) to (3) once (1) to (5) are checked and saved, with one question, and sent via the Zapier route only after Paul's yes, the send confirmed.")

# --- stamp + changelog (keep the last 5 rows) ---------------------------------
rep("**Last updated:** 2026-10-28 10:45 (Athens/Greece time)", "**Last updated: %s (Athens time)**" % STAMP)
rep("| 2026-10-14 15:03 | Index added; description made plain; changelog archived; client names, policy numbers and beneficiary details in examples replaced with placeholders. No rule changed. |\n", "")
rep("| When (Athens time) | What changed |\n|---|---|\n",
    "| When (Athens time) | What changed |\n|---|---|\n"
    "| " + STAMP + " | Interim update (Paul, 02/11/2026): the new Fact Find form's data file is the first source (the name stays Fact Find (Audio to Text)); its schema version is checked every run; its parking list (`unplaced`) is not processed; the company look-up text is checked; Dread Disease ABI is 3% unless Paul states otherwise; setting up the follow-up appointment is an action for Sitamah; the Planner note and the Sitamah message are made once, by the Teams transcript program (Steps 7b and 8). |\n")

# --- out of scope pointer ------------------------------------------------------
rep("(now always produced via `client-teams-transcript-skill`'s Output 1 structure and presented as its copy-ready Artifact page, per Step 7b below)",
    "(always made by `client-teams-transcript-skill`'s program and presented as its copy-ready page, per Step 7b below)")

# --- Step 1 item 1 ---------------------------------------------------------------
rep("1. **The Fact Find (Audio to Text) file** — see Step 1b. This is the first and primary source.",
    "1. **The Fact Find form's data file (named `Fact Find (Audio to Text)`)** — see Step 1b. This is the first and primary source.")

# --- Step 1b A ----------------------------------------------------------------------
rep("1. **Locate it - by content as well as name.** It is normally `Fact Find (Audio to Text) - DD.MM.YYYY - [Name Surname].pdf` plus a `.json` with the same name, in the client's `2. Fact Find` folder (both locations per the Client File Access order). List the whole folder, open the candidates, and use the one dated the meeting date for this client.",
    "1. **Locate it - by content as well as name.** Paul's new Fact Find form saves a data file (`.json`) and a PDF. The name stays as it always was (Paul, 02/11/2026: keep \"Audio to Text\"): `Fact Find (Audio to Text) - DD.MM.YYYY - [Name Surname].json` plus the same name as `.pdf`, in the client's `2. Fact Find` folder (both locations per the Client File Access order). The form's own test files may be called `Fact Find - DD.MM.YYYY - [Name Surname].json`, and a `Fact Find (Voice to Text)` name may appear, so list the whole folder, open the candidates, and recognise the data file by what is inside it (`app` is `wr-fact-find`), not by its name. Use the one dated the meeting date for this client.")
rep("2. **Read both the PDF and the JSON.** The PDF is the readable Fact Find (WR Fact Find v3.0). The JSON holds every field with a value `v` and a status `st`: `confirmed`, `heard`, `verify`, `preset` or `empty`; repeating lists (risk policies, retirement funding, debts, children and so on) sit under `l`. Extract both programmatically AND render the PDF pages and look at them. If the PDF and the JSON disagree on a field, flag it and quote both.",
    "2. **Read both the JSON and the PDF.** The JSON is the first source: every field sits under `f` as a value `v` with a status `st` (`confirmed`, `preset` or `empty`; files from the older form also use `heard` and `verify`), and the repeating lists (risk policies, retirement funding, debts, children and so on) sit under `l` as rows. The PDF is the readable copy of the same Fact Find (WR Fact Find v3.0). Extract both programmatically AND render the PDF pages and look at them. If the PDF and the JSON disagree on a field, flag it and quote both. The form's own area summaries (`sum`) and drafted action list (`pa`, `pa_actions`) are not sources: the facts come from the fields and lists, and the actions for Sitamah come from the Planner note (Step 7b).")
rep("`confirmed`, `heard`, `verify` and `preset` values are all populated values and all go into the Fact Find.",
    "`confirmed` and `preset` values (and `heard` and `verify` values in an older file) are all populated values and all go into the Fact Find.")
rep("6. **Say what you did.** The source report (Step 5) states what the Audio to Text file contributed, with every `heard`, `verify` and `preset` entry listed, as well as every difference found.\n",
    "6. **Say what you did.** The source report (Step 5) states what the Audio to Text file contributed, with every `preset` entry (and every `heard` and `verify` entry in an older file) listed, as well as every difference found.\n"
    "7. **Check the form's schema version every run (Paul, 02/11/2026).** Read `schema` at the top of the JSON. This skill knows `3.0`. If it says anything else (the form's code is changed from time to time), stop before building and tell Paul in one line which version you found; never guess how a new version lays out its fields.\n"
    "8. **Do not process the parking list (Paul, 02/11/2026).** The JSON's `unplaced` list holds facts the form heard but did not place in a box. That is deliberate: only the crucial facts go into a field. The Teams call is recorded, so the transcript carries everything else; use the transcript for the extra context. Do not read `unplaced` as a source and do not list its entries.\n"
    "9. **Use the saved value.** If a field in the file is wrong, Paul corrects it in the form himself and saves again. Never change a value because the transcript sounds different; flag the difference under point 4 as always.\n"
    "10. **Check the company look-up text (Paul, 02/11/2026).** The form can look up on the web what a company does and write it into the 'what does the company do' field. Read that text before using it. Throw it out if it talks to the reader (for example \"try again\", \"I found no...\", a question) or is much longer than a short description (more than about 40 words), and replace it from what the client said in the transcript; if the transcript does not say, show `Not stated` and list it for Paul. A clean look-up that nobody confirmed is shown marked \"web look-up, not confirmed with the client\". If the file marks such a look-up `confirmed`, tell Paul in the hand-over message that the form's look-up should say \"to verify\", never \"confirmed\".\n")

# --- Step 3 ------------------------------------------------------------------------------
rep("- **Derive fields the layout implies but nobody stated outright.** E.g. Date of Birth and gender from a South African ID number (first 6 digits YYMMDD; the next four digits below 5000 mean female) - and cross-check against the Audio to Text file.",
    "- **Derive fields the layout implies but nobody stated outright.** E.g. Date of Birth and gender from a South African ID number (first 6 digits YYMMDD; the next four digits below 5000 mean female) - and cross-check against the Audio to Text file. If a 'number of years' field holds a year (for example 2015) instead of a count, work out the years (the meeting year minus that year) and show it as \"since 2015\".")
rep("  - **Dread Disease ABI Value = 5%.**",
    "  - **Dread Disease ABI Value = 3% always, unless Paul states otherwise for that client (Paul, 02/11/2026; this replaces the 5% of 15/10/2026 - the new form presets 3%).**")

# --- Step 3a ---------------------------------------------------------------------------------
rep("9. **The Planner note (Step 7b)** — confirm it uses `client-teams-transcript-skill`'s Output 1 planning-area structure (Risk / Retirement / Investment / Medical Aid-Will-Short-Term / Applications / Actions / Next appointment), not the retired fixed 6-part layout, that every action is written as `Sitamah to ...`, and that it is presented as the copy-ready Artifact page (not chat text or a code block).",
    "9. **The Planner note (Step 7b)** — confirm it was made by the Teams transcript program (its checker says PASS), that every action is written as `Sitamah to ...`, that setting up the follow-up appointment is an action when one was asked for, and that it is presented as its copy-ready page (not chat text or a code block).")
rep("every `heard`, `verify` and `preset` entry is listed in the source report.",
    "every `preset` entry (and every `heard` and `verify` entry in an older file) is listed in the source report; the schema version was checked (Step 1b, point 7); the `unplaced` list was not processed; and the company look-up text was checked (Step 1b, point 10).")
rep("Dread Disease ABI is 5%; and the Summary's Section 8 shows the same.",
    "Dread Disease ABI is 3% (unless Paul stated otherwise); and the Summary's Section 8 shows the same.")

# --- Step 5 source report -----------------------------------------------------------------------
rep("(b) every Audio to Text field that was populated with status `heard`, `verify` or `preset`, with what was done with it",
    "(b) every Audio to Text field that was populated with status `preset` (or `heard` or `verify` in an older file), with what was done with it")

# --- Step 7b + Step 8 rewritten (clearly replaced by the Teams transcript program) -------------------
a = t.index("**7b. Planner / AdviceTech note")
b = t.index("**Delivering all three:**")
new7b = (
    "**7b. Planner / AdviceTech note and the message to Sitamah (made once, by `client-teams-transcript-skill`'s program - Paul, 02/11/2026)**\n"
    "- Do not write the Planner note or the message to Sitamah by hand in this skill. Open `client-teams-transcript-skill` and run its step driver for this meeting with `--type first` (a WhatsApp call: `--type whatsapp`). The program reads the transcript, builds the short Planner note page (one-line bullets per planning area, only the actions for now, in order), checks it, and builds the message to Sitamah. The old fixed layouts and the \"Output 1\" text this skill used to point to no longer exist.\n"
    "- Facts that the Fact Find settled (and the transcript did not) are taken from the approved Fact Find, so the note matches it. The pointer line in the note names the Fact Find Summary PDF just produced in 7a.\n"
    "- Setting up the follow-up appointment IS an action for Sitamah at every meeting (she books it, or sends the Teams meeting request): \"Sitamah to set up the follow-up appointment\". Any FNA / Shortfall / Reduced quote line names the insurer and says New Business or Servicing (Step 3), and two independent actions are separate, unconditional lines (Step 3).\n"
    "- For two spouses (Step 1d) the program is run once per spouse.\n\n"
)
t = t[:a] + new7b + t[b:]

rep("then present the Planner note as its copy-ready Artifact page, in `client-teams-transcript-skill`'s Output 1 planning-area structure, with one short sentence in the reply saying what the page is. All three outputs come from one trigger — the advisor shouldn't have to ask for the summary, the Planner note, or the folder save separately once the Fact Find itself is approved. **Only after all three are approved and saved, finish with Step 8 (the Teams message to Sitamah).**",
    "then present the Planner note as its copy-ready page, with one short sentence in the reply saying what the page is, and show the message to Sitamah with its one question (Step 8). All three outputs come from one trigger — the advisor shouldn't have to ask for the summary, the Planner note, or the folder save separately once the Fact Find itself is approved.")

c = t.index("## Step 8: Notify Sitamah in Teams")
new8 = (
    "## Step 8: The message to Sitamah (made once, by the Teams transcript program - Paul, 02/11/2026)\n\n"
    "The message is made and sent only by `client-teams-transcript-skill`: its program builds it, and its page `references/07-teams-message.md` holds the wording (with `(Review Client)` or `(Prospect)` after the name), the 1st / 2nd / 3rd count, the follow-up sentence check and the Zapier-only route (the Microsoft 365 connector cannot send Teams messages: 403). This skill does not word, show or send a second message.\n\n"
    "- It is shown in the same reply as the two PDFs and the Planner note page, with one question (\"Shall I post this message to Sitamah in Teams?\"), once the PDFs are saved and the folder listing has been checked.\n"
    "- It is sent only after Paul's clear yes, once per meeting, and never again for a correction unless Paul asks. For two spouses in one meeting there is one message per spouse, each with its own yes.\n"
)
t = t[:c] + new8

open(P, "w", encoding="utf-8").write(t)
print("OK ff-population-transcript patched; stamp", STAMP, "; lines", t.count("\n") + 1)
