INVENTORY of the old skill: 105 sentences
  kept (word for word or nearly): 24
  reworded, with a recorded change: 37
  dropped, with a recorded decision: 44
  UNACCOUNTED: 0


REWORDED (each is covered by a recorded change):
- old line 21: Write only what is in the source material (transcript, quote, document, file) or in a named document this skill tells you to use.
    now: "When a route gives you the transcript as a file (.docx, .vtt or text), bring a copy into the run folder:
    why: Shortened to what applies to a download.
- old line 21: If a line is unclear, garbled or ambiguous, do not turn it into a fact:
    now: If the folder is not found or is ambiguous, ask Paul.
    why: Shortened to what applies to a download.
- old line 21: flag it to the user.
    now: "pasted into the reply as it is:
    why: Shortened to what applies to a download.
- old line 21: "It seems implied", "it is usual" and "it would make sense" are not sources.
    now: R.add(False, "The meeting is not identified yet (title, date and length are needed)", "step 'identify':
    why: Shortened to what applies to a download.
- old line 24: Deliver everything this skill lists, every time.
    now: which version of this skill is running.
    why: Shortened to what applies to a download.
- old line 24: A run is not finished until every deliverable this skill names has been produced AND handed over exactly the way this skill specifies (shown in chat, sent as a file in the chat, saved to the named fol
    now: "When a route gives you the transcript as a file (.docx, .vtt or text), bring a copy into the run folder:
    why: Shortened to what applies to a download.
- old line 24: Before you reply, list each deliverable and confirm each was handed over.
    now: print("\nSAY THIS TO PAUL FIRST, before anything else in your reply, in exactly these words:\n    %s.\n" % w.version_line())
    why: Shortened to what applies to a download.
- old line 25: When the user corrects anything:
    now: # ---------------------------------------------------------------- writing a plain .docx (from a .vtt, when the connector gives text)
    why: Shortened to what applies to a download.
- old line 25: (a) go back to the source and re-check that point and everything related to it;
    now: 1 | Run it | The one command that starts the job and how every step works |
    why: Shortened to what applies to a download.
- old line 25: (b) fix it everywhere it appears, in every deliverable;
    now: Three routes, in order, every try logged.
    why: Shortened to what applies to a download.
- old line 25: (c) re-run this skill's full checklist;
    now: m = re.search(r'^name:\s*"?([a-z0-9-]+)"?\s*$', f.read(), re.M)
    why: Shortened to what applies to a download.
- old line 25: (d) re-deliver every affected deliverable in full, as in rule 5.
    now: print("EVERY STEP IS DONE.\nPut this SHORT AUDIT in your reply, as it is (it is the whole report;
    why: Shortened to what applies to a download.
- old line 46: Paul asks for a client's Teams meeting transcript to be saved to the client's file (e.g.
    now: "Teams meeting transcript (.docx) in the client's 2.
    why: Moved into the description and the routes page.
- old line 46: "save his transcript to his FF folder"), or a client meeting has just been completed and he asks for the transcript.
    now: Use after a client meeting or when Paul asks to save a transcript."
    why: Moved into the description and the routes page.
- old line 46: Only for transcripts that exist in Teams for that meeting.
    now: "If all three fail, tell Paul exactly what happened (for example transcription was not started in the meeting).
    why: Moved into the description and the routes page.
- old line 49: This skill is Paul's explicit instruction to use Claude in Chrome for Teams.
    now: This is Paul's explicit instruction for reading Teams in the browser:
    why: Chrome is now the third route, after the Microsoft 365 connector and Zapier (Paul, 03/11/2026).
- old line 49: Do not use it for anything else in Teams:
    now: if any(r not in failed for r in routes[:i]):
    why: Chrome is now the third route, after the Microsoft 365 connector and Zapier (Paul, 03/11/2026).
- old line 49: read the meeting recap/transcript only.
    now: Teams is for reading the meeting recap and its transcript only.
    why: Chrome is now the third route, after the Microsoft 365 connector and Zapier (Paul, 03/11/2026).
- old line 50: The downloaded file is copied into the client folder;
    now: The transcript is copied into the client folder, never moved and never overwritten;
    why: Chrome is now the third route, after the Microsoft 365 connector and Zapier (Paul, 03/11/2026).
- old line 50: the original stays in Downloads (tell Paul he can delete it).
    now: the original download stays where it is (tell Paul he can delete it).
    why: Chrome is now the third route, after the Microsoft 365 connector and Zapier (Paul, 03/11/2026).
- old line 54: Identify the client and the meeting date (Paul's message;
    now: The client and the meeting date are taken exactly from Paul's message.
    why: The eight steps are replaced by a program that shows one step at a time; the Python read of the .docx is replaced by the checker (2 minutes, 10-minute gap).
- old line 54: otherwise the most recent completed client meeting on his calendar via outlook_calendar_search).
    now: If it does not, take the most recent completed client meeting on his calendar (outlook_calendar_search through the Microsoft 365 connector).",
    why: The eight steps are replaced by a program that shows one step at a time; the Python read of the .docx is replaced by the checker (2 minutes, 10-minute gap).
- old line 54: Dates are DD/MM/YYYY.
    now: Teams meeting transcript - DD.MM.YY - (First Surname).docx"""
    why: The eight steps are replaced by a program that shows one step at a time; the Python read of the .docx is replaced by the checker (2 minutes, 10-minute gap).
- old line 57: Find the file with device_bash (ls -lat $HOME/mnt/Downloads | head) - newest .docx matching the meeting title.
    now: Find the file with device_bash (ls -lat $HOME/mnt/Downloads | head):
    why: The eight steps are replaced by a program that shows one step at a time; the Python read of the .docx is replaced by the checker (2 minutes, 10-minute gap).
- old line 58: Locate the client's folder under liferisk.co.za (both locations, per the Client File Access order in client-teams-transcript-skill):
    now: Find the client's folder under liferisk.co.za, in both locations:
    why: The eight steps are replaced by a program that shows one step at a time; the Python read of the .docx is replaced by the checker (2 minutes, 10-minute gap).
- old line 59: Fact Find folder, using the name:
    now: Fact Find folder, nothing overwritten;
    why: The eight steps are replaced by a program that shows one step at a time; the Python read of the .docx is replaced by the checker (2 minutes, 10-minute gap).
- old line 61: Teams meeting transcript - 05.10.26 - (First Last).docx.
    now: Teams meeting transcript - DD.MM.YY - (First Surname).docx.
    why: The eight steps are replaced by a program that shows one step at a time; the Python read of the .docx is replaced by the checker (2 minutes, 10-minute gap).
- old line 62: Verify with a short python read of the .docx (word/document.xml):
    now: root = ET.fromstring(z.read("word/document.xml"))
    why: The eight steps are replaced by a program that shows one step at a time; the Python read of the .docx is replaced by the checker (2 minutes, 10-minute gap).
- old line 62: header shows the meeting title/date and length (e.g.
    now: "Identify the client's meeting (title, date and length)",
    why: The eight steps are replaced by a program that shows one step at a time; the Python read of the .docx is replaced by the checker (2 minutes, 10-minute gap).
- old line 62: 1h 36m 2s) and the last timestamp is near the end of that length;
    now: TOLERANCE_S = 120                                # the last time stamp may fall this far short of the stated length (Paul, 03/11/2026)
    why: The eight steps are replaced by a program that shows one step at a time; the Python read of the .docx is replaced by the checker (2 minutes, 10-minute gap).
- old line 62: If it looks truncated, tell Paul exactly what is missing.
    now: "If it prints a red cross, tell Paul exactly what it says and what is missing.
    why: The eight steps are replaced by a program that shows one step at a time; the Python read of the .docx is replaced by the checker (2 minutes, 10-minute gap).
- old line 63: Tell Paul in one or two sentences:
    now: Your reply to Paul is that audit, as it is, plus one plain sentence.
    why: The eight steps are replaced by a program that shows one step at a time; the Python read of the .docx is replaced by the checker (2 minutes, 10-minute gap).
- old line 63: the client folder and file name saved, that the transcript is complete (length), and that the original copy is still in Downloads for him to delete.
    now: the client folder and file name saved and, if the Chrome route was used, that the original is still in Downloads for Paul to delete.",
    why: The eight steps are replaced by a program that shows one step at a time; the Python read of the .docx is replaced by the checker (2 minutes, 10-minute gap).
- old line 66: If Teams will not open, Paul is not signed in, or the Recap shows no transcript, stop after 2-3 attempts and say exactly what happened (e.g.
    now: If the Recap shows no transcript, or transcription was not started in the meeting, say exactly that.
    why: Now one rule per route instead of a single Chrome-only rule.
- old line 66: transcription was not started in the meeting).
    now: If the Recap shows no transcript, or transcription was not started in the meeting, say exactly that.
    why: Now one rule per route instead of a single Chrome-only rule.
- old line 66: Do not switch to other routes without asking.
    now: Do not switch to other methods without asking.
    why: Now one rule per route instead of a single Chrome-only rule.
- old line 69: After saving, Paul may ask for the summary - use client-teams-transcript-skill (it looks for this file in 2.
    now: this was a follow-up meeting, so run client-teams-transcript-skill."
    why: Paul, 03/11/2026, question 5: yes.


DROPPED (each is covered by a recorded decision):
- 1 | Universal operating rules + Delivery gate | The nine rul: Replaced by the new short Index (five sections).
- ## UNIVERSAL OPERATING RULES - READ FIRST, APPLY TO EVERY ST: The preamble is replaced by the short intro of references/00-rules.md; the program shows the rules at the start and the right page at each step.
- Re-load this skill before you start, and again after any com: Rule 1 (re-load this skill) is replaced by the program: it shows the standing rules at the start and the right page at each step, and `run.py status` tells a chat where the job is up to after a compression.
- Read before you write. Read the source material completely a: Rule 3 (read before you write) concerned drafting from a source. This skill drafts nothing: it saves what Teams gave, and the program reads the file itself.
- Changes to a skill: edit the existing skill, never create a : Rule 9 (changes go through the propose_skills card) is replaced by standard S7: skills are changed only in Claude Code and uploaded as a zip by Paul.
- Delivery gate for this skill (rules 5 and 6 applied): a run : The Delivery gate is replaced by the program: the six steps in order and the checker's short audit prove each item (identified, fetched, complete, named, saved and listed).
- Last updated: 2026-10-14 14:41 (Athens time): The hand-typed Last updated line, the changelog paragraphs and the changelog table are replaced by the stamp the tool sets (S2) and the Recent changes table; the full history lives in the repo history/ folder.
- Do not try Graph/Zapier/MS365 connector routes first - they : Replaced (Paul, 03/11/2026, question 1: yes): the Microsoft 365 connector now holds OnlineMeetingTranscript.Read.All, so it is tried first, then Zapier, then Chrome, every try logged (S4).
