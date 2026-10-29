INVENTORY of the old skill: 466 sentences
  kept (word for word or nearly): 289
  reworded, with a recorded change: 47
  dropped, with a recorded decision: 130
  UNACCOUNTED: 0


REWORDED (each is covered by a recorded change):
- old line 35: *Output 1 now applies to every meeting, first appointment included (changed 07.10.26, reversing the 06.10.26 exception).
    now: *Output 1 now applies to every meeting, first appointment included.
    why: Dated attribution removed from the live page (standards S5); the original wording stays in history/SKILL.2026-10-08.redacted.md.
- old line 37: Output 1 (Planner note, shown in chat as formatted text) and Output 2 (PDF, saved to the client's folder and sent in chat).
    now: Output 1 (Planner note, shown as a copy-ready page), Output 2 (PDF, saved to the client's folder and sent in chat) and the Teams message to Sitamah.
    why: The Planner note is now a copy-ready page; the Teams message to Sitamah is a third deliverable (Paul 29/10/2026).
- old line 50: Stage it with device_stage_files, read with pandoc -t plain --wrap=none.
    now: Stage it with device_stage_files (or fetch it through the m365 route), then tx.py prep converts it with pandoc -t plain --wrap=none.
    why: The conversion is done by the program (tx.py prep) instead of by hand.
- old line 51: If that is not possible, ask:
    now: If that is not possible (all three routes logged as failed), ask:
    why: The conversion is done by the program (tx.py prep) instead of by hand.
- old line 65: Read the converted text in sequential chunks (about 400-450 lines each);
    now: the skill asks for about 400-450 lines per read.
    why: Chunking and ordering are done by the program.
- old line 66: Keep a decision ledger while reading Pass 1 (internal working list, not saved):
    now: Keep a decision ledger while reading Pass 1 (run.py ledger add, kept in the run folder, never saved to the client's folder):
    why: Chunking and ordering are done by the program.
- old line 69: Keyword scan (in addition to, never instead of, the two reads) - search the transcript for decision and change words - change, instead, rather, actually, for now, later, keep it, leave it, get back to
    now: Keyword scan (in addition to, never instead of, the two reads) - tx.py scan searches the transcript for decision and change words (the list below is built into it) - change, instead, rather, actually,
    why: Chunking and ordering are done by the program.
- old line 71: for EVERY bullet in Output 1/Output 2 and EVERY action point, identify (internally) the transcript timestamp(s) it comes from, or the named document it comes from (Overview, quote, Fact Find Summary, 
    now: every fact and every action traces to the transcript or a named document, and the program checks the quote.
    why: Chunking and ordering are done by the program.
- old line 73: walk the ledger entry by entry and confirm each one appears in Output 1 and/or Output 2 (every request/instruction in the ledger must map to a Sitamah action or a status line).
    now: verify.py fails any decision, request, change or hold that no item covers (every request/instruction in the ledger must map to a Sitamah action or a status line).
    why: Chunking and ordering are done by the program.
- old line 74: "Transcript read in full TWICE (Pass 1 and Pass 2, N lines each)", the number of ledger decisions/changes, confirmation that every action was source-traced, and any change-of-mind items reported as Ch
    now: verify.py prints it ("Transcript read in full TWICE (Pass 1 and Pass 2, N lines each)", the number of ledger entries, confirmation that every bullet and action was source-traced);
    why: Chunking and ordering are done by the program.
- old line 74: If this line cannot be truthfully written, the report must not be delivered.
    now: It is printed only when the checks pass, so if it is not there the report must not be delivered.
    why: Chunking and ordering are done by the program.
- old line 76: Correspondence check - CURRENT transactions only (Paul's rule, 06/10/2026) - follow-up meetings only
    now: Correspondence check - CURRENT transactions only - follow-up meetings only
    why: Dated attribution removed from the live page (standards S5); the original wording stays in history/SKILL.2026-10-08.redacted.md.
- old line 87: render pages as images if text extraction is empty):
    now: render pages as images if text extraction is empty), and record each document with run.py source:
    why: Standard S3: every client-file document read is logged.
- old line 119: add one line for the rest.
    now: the program adds one line naming the rest.
    why: The 'not discussed' line is now written by the program (Paul 29/10/2026: one line naming the areas not discussed).
- old line 150: Be resourceful - look beyond the quote (Paul's rule, 07/10/2026).
    now: Be resourceful - look beyond the quote.
    why: Dated attribution removed from the live page (standards S5); the original wording stays in history/SKILL.2026-10-08.redacted.md.
- old line 164: Add a short "Since the last meeting" block at the top of Output 2.
    now: Add a short "Since the last meeting" block at the top of Output 2 (since_last in content.json, each item tagged).
    why: Names where it lives.
- old line 180: ALL ACTION POINTS GO TO SITAMAH (Paul's rule, 06/10/2026).
    now: ALL ACTION POINTS GO TO SITAMAH.
    why: Dated attribution removed from the live page (standards S5); the original wording stays in history/SKILL.2026-10-08.redacted.md.
- old line 182: NO INFERENCE (Paul's rule, 08/10/2026).
    now: print("BUILT from content.json (hash %s...)" % build["content_sha"][:10])
    why: Dated attribution removed from the live page (standards S5); the original wording stays in history/SKILL.2026-10-08.redacted.md.
- old line 187: Planner / AdviceTech chat note (formatted text, NOT a code block)
    now: Planner / AdviceTech note (a copy-ready page, NOT a code block)
    why: Paul's standing rule 09/10/2026 (already in ff-population-transcript): the note is a copy-ready page, not chat text.
- old line 189: *Applies to every meeting - first/Fact Find appointment included (changed 07.10.26).
    now: *Applies to every meeting - first/Fact Find appointment included.
    why: The page template was missing from this skill (ff-population-transcript pointed to it); it is now generated by program from content.json.
- old line 189: Present the note in the chat reply as ordinary formatted text under a plain line such as "Planner note".
    now: in the reply that presents the message, say in one line what the Summary and Planner note say about the next appointment and therefore why the follow-up sentence is in or out.
    why: The page template was missing from this skill (ff-population-transcript pointed to it); it is now generated by program from content.json.
- old line 189: Design (approved by Paul 06/10/2026;
    now: *Sam Testcase – 05/10/2026
    why: The page template was missing from this skill (ff-population-transcript pointed to it); it is now generated by program from content.json.
- old line 189: extended to first/Fact Find meetings 07/10/2026):
    now: extended to first/Fact Find meetings):
    why: The page template was missing from this skill (ff-population-transcript pointed to it); it is now generated by program from content.json.
- old line 192: For a first/Fact Find meeting (changed 07.10.26), quote the Fact Find Summary PDF instead:
    now: For a first/Fact Find meeting, quote the Fact Find Summary PDF instead:
    why: Paul's decision 29/10/2026 (each of the eight its own heading; one line for those not discussed).
- old line 193: bold plain headings with no colons, in the Step 3 order, only areas discussed or still open:
    now: bold plain headings with no colons, in the Step 3 order, each of the eight its own heading and only if discussed or still open:
    why: Paul's decision 29/10/2026 (each of the eight its own heading; one line for those not discussed).
- old line 193: EGAR), Medical Aid / Will / Short-Term, Other (only when notable), Applications (only if something differed - rarely applicable at a first/Fact Find meeting), Actions, and last Next appointment:
    now: Risk, RA, Investment, RGAR, EGAR, Medical Aid, Will, Short-Term, Other (only when notable), then one line naming the areas not discussed, Applications (only if something differed - rarely applicable a
    why: Paul's decision 29/10/2026 (each of the eight its own heading; one line for those not discussed).
- old line 292: Built with reportlab (not Word), navy palette, Helvetica.
    now: Built by build.py with reportlab (not Word), navy palette, Helvetica.
    why: The layout lives in code (S6); the spec below describes what the code does.
- old line 292: Verify by rendering to PNG (pdftoppm) and looking at it before delivering.
    now: It also renders each page to a PNG (pdftoppm):
    why: The layout lives in code (S6); the spec below describes what the code does.
- old line 296: Since the Last Meeting, then the Step 3 areas that apply, then Applications (only if Step 6 found differences), then Action Points and Next Steps.
    now: Since the Last Meeting, then the Step 3 areas that apply (each of the eight its own heading, followed by one line naming those not discussed), then Applications (only if Step 6 found differences), the
    why: Paul's decision 29/10/2026.
- old line 302: (1) each area is its own bold navy heading;
    now: 1 | each area is its own bold navy heading | PROGRAM (build + headings present in the PDF text) |
    why: Each checklist item is kept; the table says whether the program or Claude's judgment covers it, so nothing is dropped and nothing is claimed as machine-checked that is not.
- old line 302: (2) every bullet is its own Paragraph, short, with hanging indent and spacing;
    now: 2 | every bullet is its own Paragraph, short, with hanging indent | PROGRAM (build) + Claude looks at the images |
    why: Each checklist item is kept; the table says whether the program or Claude's judgment covers it, so nothing is dropped and nothing is claimed as machine-checked that is not.
- old line 302: (3) quotes named with insurer, type, number and premium, never line-by-line;
    now: 3 | quotes named with insurer, type, number and premium, never line-by-line | Claude (judgment) |
    why: Each checklist item is kept; the table says whether the program or Claude's judgment covers it, so nothing is dropped and nothing is claimed as machine-checked that is not.
- old line 302: (4) every accepted quote states type, number and agreed premium;
    now: 4 | every accepted quote states type, number and agreed premium | Claude (judgment) |
    why: Each checklist item is kept; the table says whether the program or Claude's judgment covers it, so nothing is dropped and nothing is claimed as machine-checked that is not.
- old line 302: (5) resolved / open / changed items marked;
    now: 5 | resolved / open / changed items marked | PROGRAM (change must be marked CHANGED) |
    why: Each checklist item is kept; the table says whether the program or Claude's judgment covers it, so nothing is dropped and nothing is claimed as machine-checked that is not.
- old line 302: (9) no ID, account or tax numbers anywhere;
    now: No ID, account or tax numbers.
    why: Each checklist item is kept; the table says whether the program or Claude's judgment covers it, so nothing is dropped and nothing is claimed as machine-checked that is not.
- old line 302: (10) the Step 1b decision ledger was fully walked;
    now: 10 | the Step 1b decision ledger was fully walked | PROGRAM (every decision/request/change/hold covered) |
    why: Each checklist item is kept; the table says whether the program or Claude's judgment covers it, so nothing is dropped and nothing is claimed as machine-checked that is not.
- old line 302: (11) verification pass of the drafted outputs done;
    now: Then do a verification pass of the drafted outputs against the transcript:
    why: Each checklist item is kept; the table says whether the program or Claude's judgment covers it, so nothing is dropped and nothing is claimed as machine-checked that is not.
- old line 302: (12) current correspondence checked and any owner change has a revised-quote action;
    now: 12 | current correspondence checked and any owner change has a revised-quote action | PROGRAM (checks block) |
    why: Each checklist item is kept; the table says whether the program or Claude's judgment covers it, so nothing is dropped and nothing is claimed as machine-checked that is not.
- old line 302: (13) the Planner note is formatted text with the correct pointer line;
    now: 13 | the Planner note is the copy-ready page with the correct pointer line | PROGRAM |
    why: Each checklist item is kept; the table says whether the program or Claude's judgment covers it, so nothing is dropped and nothing is claimed as machine-checked that is not.
- old line 302: (15) credit life on every debt the new cover protects is reported;
    now: 15 | credit life on every debt the new cover protects is reported | PROGRAM (checks block, always) |
    why: Each checklist item is kept; the table says whether the program or Claude's judgment covers it, so nothing is dropped and nothing is claimed as machine-checked that is not.
- old line 302: (16) no "to confirm" left for a detail that is on file;
    now: 16 | no "to confirm" left for a detail that is on file | Claude (judgment);
    why: Each checklist item is kept; the table says whether the program or Claude's judgment covers it, so nothing is dropped and nothing is claimed as machine-checked that is not.
- old line 302: (17) no two independent actions worded as one waiting on the other;
    now: 17 | no two independent actions worded as one waiting on the other | PROGRAM warns on dependent wording;
    why: Each checklist item is kept; the table says whether the program or Claude's judgment covers it, so nothing is dropped and nothing is claimed as machine-checked that is not.
- old line 302: (18) the transcript was read in full TWICE (Pass 1 and Pass 2) and the delivery line says so;
    now: 18 | the transcript was read in full TWICE and the delivery line says so | PROGRAM |
    why: Each checklist item is kept; the table says whether the program or Claude's judgment covers it, so nothing is dropped and nothing is claimed as machine-checked that is not.
- old line 302: (19) every bullet and every action has a source in the transcript or a named document - no inferred facts, no invented actions, no chase actions for items left with the client;
    now: 19 | every bullet and every action has a source - no inferred facts, no invented actions, no chase actions for items left with the client | PROGRAM |
    why: Each checklist item is kept; the table says whether the program or Claude's judgment covers it, so nothing is dropped and nothing is claimed as machine-checked that is not.
- old line 302: (20) every request or instruction made on the call (what goes in the what's-next email, offers such as a spouse review, items on hold) is captured exactly as the client/Paul answered it;
    now: 20 | every request or instruction made on the call is captured exactly as the client/Paul answered it | PROGRAM (ledger coverage) + Claude (wording) |
    why: Each checklist item is kept; the table says whether the program or Claude's judgment covers it, so nothing is dropped and nothing is claimed as machine-checked that is not.
- old line 310: Output 1 stays in chat only (formatted text, not saved as a file), for every meeting type including a first/Fact Find meeting.
    now: Output 1 (the Planner page) is shown as the Artifact page only and is never saved into the client's folder, for every meeting type including a first/Fact Find meeting.
    why: Matches the page rule.
- old line 320: ask Paul for his recap/notes or recording and confirm the exact date and TIME of the call before drafting.
    now: ask Paul for his recap/notes or recording and confirm the exact date and TIME of the call before drafting (run run.py start --type whatsapp;
    why: Kept word for word; added the run type and a note that the Teams message does not apply (the old skill defines it only for Teams appointments).


DROPPED (each is covered by a recorded decision):
- UNIVERSAL OPERATING RULES - READ FIRST: Heading of the old rules block; the rules now live in references/00-rules.md and are shown by the program when a run starts.
- These rules come before everything else in this skill. They apply from the first: Lead-in kept in shortened form in 00-rules.md (see changes).
- Re-load this skill before you start, and again after any compression.: Rule 1 replaced: the program shows each step and `run.py status` recovers the position after a long chat (standards S8/S16).
- Changes to a skill: edit the existing skill, never create a new one.: Rule 9 replaced by standard S7: skills with programs are changed only in Claude Code and uploaded as a zip; the review card saves text only.
- Delivery gate for this skill (rules 5 and 6 applied): Now enforced by verify.py and listed as 'Deliverables of a run' in 00-rules.md, with the Planner page and Teams message added.
- Last updated: 2026-10-08 14:20: Replaced by the stamp the program sets (standards S2).
- Changelog (last 5 only: Change history belongs in history/ (redacted archive of the whole old skill is kept there), not in the live skill (standards S2, S5). Every rule these entries introduced is still in the reference pages.
- Local machine first via the device bridge.: Replaced by the three-route access ladder (standards S4); see references/01-access-and-locate.md.
- Paul looks at eight areas.: Replaced by Paul's eight areas confirmed 29/10/2026 (Risk, RA, Investment, RGAR, EGAR, Medical Aid, Will, Short-Term); see references/04-areas-and-quotes.md.
- Example ([client A], 05/10/2026, follow-up meeting): Two worked examples built on real client details are removed (standards S11, no client data). A model built from invented data replaces them: references/planner-note-example.txt and content-example.json.
