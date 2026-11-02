#!/usr/bin/env python3
"""Interim text edits to fact-find-summary (Paul's decision 14, 02/11/2026). Every edit must match exactly once."""
import os
import subprocess
import sys

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fact-find-summary", "SKILL.md")
t = open(P, encoding="utf-8").read()
STAMP = subprocess.check_output(["date", "+%Y-%m-%d %H:%M"], env=dict(os.environ, TZ="Europe/Athens")).decode().strip()


def rep(old, new):
    global t
    n = t.count(old)
    if n != 1:
        sys.exit("EDIT FAILED (%d matches): %r" % (n, old[:90]))
    t = t.replace(old, new)


# --- front matter + index ------------------------------------------------------------
rep("from a completed WR Client Fact Find (v3.0 layout, built from the Audio to Text file and transcript), plus the other two outputs",
    "from a completed WR Client Fact Find (v3.0 layout, built from the Fact Find form's data file - named Audio to Text - and the transcript), plus the other two outputs")
rep("| 11 | Step 8: notify Sitamah in Teams | Message format, Zapier route, Paul's yes |",
    "| 11 | Step 8: the message to Sitamah | Made once, by the Teams transcript program; shown with the outputs; Paul's yes |")

# --- rule 10 ---------------------------------------------------------------------------------
rep("(1) the client's `Fact Find (Audio to Text) - [date] - [Name Surname]` PDF and JSON is the first and primary source;",
    "(1) the Fact Find form's data file, `Fact Find (Audio to Text) - [date] - [Name Surname]` (the JSON the new Fact Find form saves, and its PDF; the name stays as it was - Paul, 02/11/2026), is the first and primary source;")
rep("Whatever is populated in the Audio to Text file is used, whatever its status (confirmed, heard, verify, preset).",
    "Whatever is populated in the Audio to Text file is used, whatever its status (confirmed or preset; heard or verify in an older file). **The form's data file, three standing rules (Paul, 02/11/2026):** its `schema` value is checked every run and must be `3.0` (if not, stop and tell Paul in one line); the `unplaced` list (facts the form heard but did not place) is not processed, because the recorded transcript supplies the extra context; and where the Fact Find replaced chatter in the company look-up text with the transcript's words (`ff-population-transcript` Step 1b, point 10), that is deliberate and not a difference to flag.")

# --- delivery gate (5) and (6) -------------------------------------------------------------------
rep("the Planner note delivered ONLY as the rendered Artifact page in the window on the right with the Copy button (never pasted in the chat, a code block, or a raw .html/.txt/.md file); (6) once (1) to (5) are approved and saved, the Teams message to Sitamah (Step 8) was shown to Paul, sent via the Zapier route only after his yes (or confirmed already sent for this meeting by `ff-population-transcript`), and the send confirmed.",
    "the Planner note made by the Teams transcript program and delivered ONLY as its rendered copy-ready page in the window on the right with the Copy button (never pasted in the chat, a code block, or a raw .html/.txt/.md file); (6) the Teams message to Sitamah (Step 8), made by the same program, was shown to Paul in the same reply as the outputs once (1) to (5) were checked and saved, sent via the Zapier route only after his yes (or confirmed already sent for this meeting), and the send confirmed.")

# --- stamp + changelog (keep the last 5 rows) -------------------------------------------------------
rep("**Last Updated:** 28 October 2026, 10:58 (Athens/Greece time)", "**Last updated: %s (Athens time)**" % STAMP)
rep("| 2026-10-14 13:55 | New Step 8: notify Sitamah in Teams after all three outputs are approved (Zapier route, Paul's yes, once per meeting); Delivery gate (6) added. |\n", "")
rep("| When (Athens time) | What changed |\n|---|---|\n",
    "| When (Athens time) | What changed |\n|---|---|\n"
    "| " + STAMP + " | Interim update (Paul, 02/11/2026): the new Fact Find form's data file is the first source (the name stays Fact Find (Audio to Text)); its schema version is checked every run; its parking list (`unplaced`) is not processed; Dread Disease ABI is 3% unless Paul states otherwise (was 5%); the Planner note and the Sitamah message are made once, by the Teams transcript program (Step 8). |\n")

# --- transcript accuracy ------------------------------------------------------------------------------
rep("Whatever is populated in the Audio to Text file (confirmed, heard, verify or preset) is a populated value and belongs in the Summary.",
    "Whatever is populated in the Audio to Text file (confirmed or preset; heard or verify in an older file) is a populated value and belongs in the Summary.")

# --- standing ABIs -----------------------------------------------------------------------------------------
rep("## Standing ABIs in Section 8 (Paul, 15 October 2026)", "## Standing ABIs in Section 8 (Paul, 15 October 2026; Dread Disease changed 2 November 2026)")
rep("- **Dread Disease ABI = 5%.**",
    "- **Dread Disease ABI = 3% always, unless Paul states otherwise for that client (Paul, 02/11/2026; this replaces the 5% of 15 October 2026, and the new Fact Find form presets 3%).**")
rep("(named precedent: [client H], 27.10.26 — the Audio to Text file showed a Dread Disease ABI of 3% and had no Household needs ABI line under Permanent disability fractured; 5% was written, the Household needs ABI line was added, and both were mentioned to Paul in one line)",
    "(named precedent: [client H], 27.10.26 — the Audio to Text file had no Household needs ABI line under Permanent disability fractured; the line was added at 5% and mentioned to Paul in one line. That file's Dread Disease ABI of 3% was then overwritten with 5%; since 02/11/2026 3% is the standard, so that case no longer arises)")

# --- output 3 ------------------------------------------------------------------------------------------------
a = t.index("3. **The summarized Planner / AdviceTech Notes of the client meeting**")
b = t.index("\n", a)
t = t[:a] + (
    "3. **The summarized Planner / AdviceTech Notes of the client meeting** — made by `client-teams-transcript-skill`'s program (run with `--type first`; it builds the short note - one-line bullets per planning area and Sitamah-only action points, only those for now, in order - and checks it) from the same source meeting transcript(s), with the pointer line naming this Fact Find Summary PDF. Setting up the follow-up appointment is an action for Sitamah (Paul, 02/11/2026). **It is delivered ONLY as the rendered copy-ready page in the window on the right** (with its \"Copy planner note\" button) — **never pasted into the chat, never in a code block, never as a raw .html file, never as a .txt/.md file, and never saved into the client's folder** (Paul's strict rule, 14/10/2026). Corrections are re-published to the same page."
) + t[b:]

# --- workflow step 1 and step 8 ---------------------------------------------------------------------------------
rep("Also open the client's `Fact Find (Audio to Text)` PDF and JSON and the Teams transcript, which the accuracy check in step 3 needs,",
    "Also open the client's `Fact Find (Audio to Text)` JSON and PDF (the Fact Find form's data file: recognise it by what is inside, `app` is `wr-fact-find`, and check that `schema` is `3.0` per rule 10) and the Teams transcript, which the accuracy check in step 3 needs,")
rep("8. **Notify Sitamah in Teams — the very last step (Paul's rule, 14/10/2026).** Only AFTER the Fact Find Transcript PDF, this Summary PDF (sent in chat and saved, folder listing checked) and the Planner note page have all been produced, checked and approved by Paul. Details below.",
    "8. **The message to Sitamah (Paul's rule, 14/10/2026; made once, by the Teams transcript program, since 02/11/2026).** Shown in the same reply as the Fact Find Transcript PDF, this Summary PDF (sent in chat and saved, folder listing checked) and the Planner note page, with one question; sent only after Paul's yes. Details below.")

c = t.index("### Step 8: Notify Sitamah in Teams after the meeting")
d = t.index("## Report Structure (fixed section order)")
t = t[:c] + (
    "### Step 8: The message to Sitamah (made once, by the Teams transcript program - Paul, 02/11/2026)\n\n"
    "The message is made and sent only by `client-teams-transcript-skill`: its program builds it, and its page `references/07-teams-message.md` holds the wording (with `(Review Client)` or `(Prospect)` after the name), the 1st / 2nd / 3rd count, the follow-up sentence check and the Zapier-only route (the Microsoft 365 connector cannot send Teams messages: 403). This skill does not word, show or send a second message.\n\n"
    "- It is shown in the same reply as the Fact Find Transcript PDF, this Summary PDF and the Planner note page, with one question (\"Shall I post this message to Sitamah in Teams?\"), once the PDFs are saved and the folder listing has been checked.\n"
    "- It is sent only after Paul's clear yes, once per meeting (if `ff-population-transcript` already got the yes and sent it for this meeting in this chat, say so with its sent time and do not send again), and never again for a correction unless Paul asks. For two spouses in one meeting there is one message per spouse, each with its own yes. For a purely incremental update to an existing Fact Find with no new meeting, send nothing.\n\n"
) + t[d:]

# --- report structure -----------------------------------------------------------------------------------------------
rep("with no Life Cover (WOL) ABI there; Dread Disease ABI 5%)", "with no Life Cover (WOL) ABI there; Dread Disease ABI 3%)")

open(P, "w", encoding="utf-8").write(t)
print("OK fact-find-summary patched; stamp", STAMP, "; lines", t.count("\n") + 1)
