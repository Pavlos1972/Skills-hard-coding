# What changed in the Client Transcript download skill, in plain words

For Paul. **Not uploaded, not live.** This is the program-driven version of `client-transcript-download` (Operation Skill Restructure, 03/11/2026). The old version stays in the skill's version history in claude.ai, and a backup of its file is sent with the zip.

## What the skill does now
After a client meeting, a program drives the job: it identifies the meeting, fetches the Teams transcript, checks it is complete, builds the file under its derived name, and you (or the chat) save a copy into the client's `2. Fact Find` folder. A checker then prints a **short audit**: one line per check with a green tick or a red cross, one line for what is only attested, and one line for the next skill.

## What a program now does that Claude did by hand
- Forces the order of the steps (identify, fetch, check, name, save, final); none can be skipped.
- Tries the routes in order and checks the log: **Microsoft 365 connector first, then Zapier, then Claude in Chrome** (your answer, 03/11/2026). A later route is accepted only after the earlier ones failed on record.
- Reads the transcript itself: the header shows the meeting title and date, the **last time stamp is within 2 minutes of the meeting length**, and there is **no gap longer than 10 minutes** between two time stamps (your answer, 03/11/2026; the 10 minutes is my reading of the old "no gaps").
- Builds the file name: `Teams meeting transcript - DD.MM.YY - (First Surname).docx` (never typed). A Teams `.docx` is copied unchanged; text from the connector (WebVTT or plain text) is written as a `.docx` with a header made from the meeting record.
- Checks the save: the folder is this client's own `2. Fact Find` folder under `Company - Paul` or `Paul Kafentzis (Client Files)`, the listed size equals the local file's, and nothing was overwritten.
- Names the next skill: a first (Fact Find) meeting goes to `ff-population-transcript` then `fact-find-summary`; a follow-up goes to `client-teams-transcript-skill`.

## What left this skill
The copied generic rules, the "propose skills" rule, the "Chrome only" rule (Chrome is now the third route), the hand-typed stamp, and the copied client-folder wording. Your own sign-in address is no longer in the text.

## What stayed the same
Teams is for reading the recap and transcript only (no posting, deleting or settings), nothing is ever deleted, the file is copied and never moved or overwritten, the original download stays for you to delete, never touch another broker's folder, and the Chrome steps themselves (kept in `references/01-fetch-routes.md`).

A program (`tools/inventory.py`) went through all 105 rules of the old text: **17 are still there word for word, 44 are reworded (each with a written reason), 44 were dropped on purpose (each with a written reason), and none was lost without a record** (checked again after the strict changes of 05/11/2026; before them it was 24, 37 and 44). The records are in `history/changes.json` and `history/decisions.json`; the full list is `history/INVENTORY-REPORT.md`.

## Your yes/no list (anything I was not sure about)
1. **The 10-minute gap rule** is my reading of the old "no gaps". **Right? Yes / No.**
2. **Text from the connector becomes a .docx made by the program.** The other skills read .docx; the program writes a plain one with a header (title, start, length) from the meeting record. **OK? Yes / No.**

## What I could not do or check
- **The Microsoft 365 and Zapier routes are not proven.** The connector holds the transcript permission (checked 03/11/2026), but I cannot prove a tool can fetch a transcript without a real meeting, which is client data. The program supports all three routes, and the first real run decides which one works.
- **The real Teams .docx layout was not seen.** The test uses an invented transcript in the layout the other skills already read (a header with title, start and duration, then `H:MM:SS Speaker` lines). If a real file differs, the check will say what it could not read, and the reader is fixed once.
- **The clicking in Chrome cannot be proven by a program.** It stays attested, together with the folder save and listing as typed by Claude.
- **I could not run it inside your chat.** Only one test was run, as agreed: one end-to-end run on invented data (five parts, ending in a pass, a cut-off transcript caught, a hand-edited file caught, and a connector-style text file turned into a correct .docx).

## Strict changes, 05/11/2026 (your corrections after the first real run of the Fact Find chain)
This skill was still built the old way: it asked the computer for folder access and could end by asking you to do something. Changed:
- **Nothing is ever asked of you to reach a file.** No permission box, no folder-access request, no "attach/upload/drag the transcript". The chat finds and saves everything itself.
- **Saving into the client's `2. Fact Find` folder:** the computer only if the chat is already connected to it (never requested; if it is not, that is logged at once as "not connected; not requested"), then **Microsoft 365** (find the folder, list it, upload, list again and compare the size), then Zapier. The checker turns red if the computer try failed for any other reason, because that would mean a connection was requested.
- **Chrome route (third route for the transcript):** it no longer asks for folder access to your Downloads. If the chat is not already connected to the computer it reads the transcript text from the Teams page instead of downloading a file; the program writes the .docx from that text and checks the header, the length and the gaps itself.
- **Meeting length:** taken from the calendar or the Teams recap; you are asked only if neither holds it.
- **Size check:** when the connector reports the file's size, the program compares it to the byte and refuses a copy of a different size.
- **Quiet run:** the version sentence, one short progress line per step, then the short audit and one plain sentence. No long opening message, no analysis of what was read. If every route fails the reply is at most five lines.

**Only attested, not proven (unchanged by this correction):** that the Microsoft 365 connector can fetch a Teams transcript and upload to the client's folder (only folder listing is proven), that text read from the Teams page is word for word what Teams shows (the program checks the length and the gaps, not every word), and the Zapier route. The first real run decides.
