<!-- The live skill text as of 14/10/2026 14:41 (Athens time), kept as the rule-by-rule baseline. -->
---
name: "client-transcript-download"
description: "Downloads a client's Teams meeting transcript via Claude in Chrome and copies it into the client's 2. Fact Find folder on OneDrive. Use after a client meeting or when Paul asks to save a transcript."
---

# Client Transcript download

## Index

| # | Section | What it covers |
|---|---|---|
| 1 | Universal operating rules + Delivery gate | The nine rules for every step, and what must be done before a run counts as complete |
| 2 | Last updated + Changelog | Athens-time stamp, last changes, standing edit note |
| 3 | When this applies | When Paul asks for a transcript to be saved |
| 4 | Standing rules | Chrome only, never delete, copy not move |
| 5 | Steps (1-8) | Identify, download in Teams, find in Downloads, locate client folder, copy, verify, report |
| 6 | If it fails | Stop after 2-3 attempts and say what happened |
| 7 | Related | Hand-off to client-teams-transcript-skill |

## UNIVERSAL OPERATING RULES - READ FIRST, APPLY TO EVERY STEP OF THE TASK

*These rules come before everything else in this skill. They apply from the first message to the last, not just at the start, and they are repeated here at the top because long conversations get compressed and only the beginning of a skill survives. If anything below seems to conflict with these rules, these rules win.*

1. **Re-load this skill before you start, and again after any compression.** At the start of every run - and whenever the conversation has been summarised or compressed, or has run long - open this skill in full (Skill tool) and re-read it before you produce or change any deliverable. Never work from a summary of the rules or from memory of them.
2. **Source first - never invent.** Write only what is in the source material (transcript, quote, document, file) or in a named document this skill tells you to use. If a line is unclear, garbled or ambiguous, do not turn it into a fact: flag it to the user. "It seems implied", "it is usual" and "it would make sense" are not sources.
3. **Read before you write.** Read the source material completely and carefully - at least as many times as this skill requires - before drafting anything. Searching for keywords is not reading.
4. **Check before you claim.** Never tell the user something is done, saved, sent, visible or working until you have checked it yourself (open the file, list the folder, look at the screen). Say what you checked.
5. **Deliver everything this skill lists, every time.** A run is not finished until every deliverable this skill names has been produced AND handed over exactly the way this skill specifies (shown in chat, sent as a file in the chat, saved to the named folder). Before you reply, list each deliverable and confirm each was handed over.
6. **Every correction re-opens the whole task, not just the item.** When the user corrects anything: (a) go back to the source and re-check that point and everything related to it; (b) fix it everywhere it appears, in every deliverable; (c) re-run this skill's full checklist; (d) re-deliver every affected deliverable in full, as in rule 5. Never fix only the item named and stop.
7. **Never lower the standard.** A correction, a frustrated user, a short request or a "quick" task does not relax any rule in this skill.
8. **If a rule cannot be met, stop and say so.** State exactly which rule or step could not be completed and why. Never hand over partial work as if it were complete.
9. **Changes to a skill:** edit the existing skill, never create a new one. Update its "Last updated" stamp (Athens time) and changelog. Then put the full updated SKILL.md forward for the user to review and save using the propose_skills tool (the "Update skill" review card). Never say the change is live until the user confirms they saved it. If the card does not appear, say so plainly and ask the user how to proceed - do not claim it was delivered.

**Delivery gate for this skill (rules 5 and 6 applied):** a run is complete only when ALL of these are done and confirmed in one line each: (1) the client and the meeting date were identified (Step 1); (2) the transcript was downloaded through Claude in Chrome from Teams (the route this skill requires); (3) the file was COPIED (never moved, never overwritten) into the client's "2. Fact Find" folder with the exact filename "Teams meeting transcript - DD.MM.YY - (First Last).docx", and the folder was checked to confirm it is there (Steps 5-6); (4) the .docx was read back and checked for the meeting title, date and length, and a last timestamp near the end, with anything missing reported to Paul exactly (Step 7); (5) Paul was told the client folder and file name, and that the original remains in Downloads for him to delete (Step 8). After ANY correction, repeat (3) to (5) for every file that changed.


**Last updated: 2026-10-14 14:41 (Athens time)**

**Changelog** (one line each; full history with backstory is in the Project as `client-transcript-download-changelog.md`)
| When (Athens time) | What changed |
|---|---|
| 2026-10-14 14:41 | Index added; description made plain; long changelog moved word for word to the archive; client name in the Step 6 example replaced with a placeholder. No rule changed. |
| 2026-10-08 14:42 | Rule 9 reworded: skill changes go forward with the propose_skills review card; never claim live until Paul confirms he saved. |
| 2026-10-08 14:30 | Universal operating rules block and Delivery gate added at the top of the skill. |
| 2026-10-06 | Created. Paul chose the Claude in Chrome route because the Microsoft 365 connector and Zapier cannot fetch Teams transcripts and computer use was declined. |

> **Standing rule:** whenever this SKILL.md is edited, add a one-line row at the top of the table above (Athens time), keep the table to 5 rows (drop the oldest), and update "Last updated" in the same edit. Put any edit with real backstory (a live mistake, a ruled-out approach) in `client-transcript-download-changelog.md` instead of growing this file.

## When this applies
Paul asks for a client's Teams meeting transcript to be saved to the client's file (e.g. "save his transcript to his FF folder"), or a client meeting has just been completed and he asks for the transcript. Only for transcripts that exist in Teams for that meeting.

## Standing rules
- This skill is Paul's explicit instruction to use **Claude in Chrome** for Teams. Do not use it for anything else in Teams: read the meeting recap/transcript only. Do not post, delete, change settings or open other chats.
- Never delete anything. The downloaded file is **copied** into the client folder; the original stays in Downloads (tell Paul he can delete it).
- Do not try Graph/Zapier/MS365 connector routes first - they are known not to work for transcripts. Go straight to Chrome.

## Steps
1. Identify the client and the meeting date (Paul's message; otherwise the most recent completed client meeting on his calendar via outlook_calendar_search). Dates are DD/MM/YYYY.
2. Chrome: load the Chrome tools in one ToolSearch call, `tabs_context_mcp`, open a **new tab** on Teams web (teams.microsoft.com, already signed in as paulk@liferisk.co.za). Open the meeting (Calendar or the meeting chat) and go to its Recap / Transcript tab. Confirm the meeting title and date match before downloading.
3. Download the transcript as **.docx** (Download > Download as .docx). It saves to Paul's Windows Downloads folder with a name like `{Meeting title with / replaced by _}.docx`. Wait for the download to finish. Close the Chrome tab when done.
4. Grant Downloads access on the device: `device_request_folder_access` for `C:\Users\Paul\Downloads` if not already connected (the folder mounts as `$HOME/mnt/Downloads`). Find the file with `device_bash` (`ls -lat $HOME/mnt/Downloads | head`) - newest .docx matching the meeting title.
5. Locate the client's folder under `liferisk.co.za` (both locations, per the Client File Access order in client-teams-transcript-skill): `Company - Paul\New Business\{Surname}, {First name}\2. Fact Find\` or `Company - WR Clients\Paul Kafentzis (Client Files)\...\{Surname}, {First name}\2. Fact Find\`. Never touch another broker's folder. If the folder is not found or is ambiguous, ask Paul.
6. Copy (not move) with `cp -n` into that `2. Fact Find` folder, using the name:
   `Teams meeting transcript - DD.MM.YY - (First Last).docx`
   e.g. `Teams meeting transcript - 05.10.26 - (First Last).docx`. If a file with that name already exists, do not overwrite - tell Paul.
7. Verify with a short python read of the .docx (`word/document.xml`): header shows the meeting title/date and length (e.g. 1h 36m 2s) and the last timestamp is near the end of that length; no gaps. If it looks truncated, tell Paul exactly what is missing.
8. Tell Paul in one or two sentences: the client folder and file name saved, that the transcript is complete (length), and that the original copy is still in Downloads for him to delete.

## If it fails
If Teams will not open, Paul is not signed in, or the Recap shows no transcript, stop after 2-3 attempts and say exactly what happened (e.g. transcription was not started in the meeting). Do not switch to other routes without asking.

## Related
After saving, Paul may ask for the summary - use client-teams-transcript-skill (it looks for this file in `2. Fact Find`).