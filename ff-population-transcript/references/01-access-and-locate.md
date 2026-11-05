# Where the files are, and what to do when the form's file is missing

Reads the client's **Fact Find (Audio to Text) file** (first and primary source), the **Teams meeting transcript(s)** (second, equally important source) and the client's **latest Overview** (reference), and builds the Wealth Revolution Client Fact Find as a completed document that follows the Audio to Text file's own layout (WR Fact Find v3.0), section by section, in its exact order. Drawn by a program and delivered as a PDF — see Step 5. **Every deliverable this skill produces is saved directly into the client's own folder — see Step 5a. This is not optional and Paul should never have to ask for it.**

## Client File Access (standing rule — applies to every step below that reads or saves a client file)

Files are found and saved by YOU, the computer first, without asking Paul to do anything with a file:

1. **The computer: the working route, and the first thing the run does.** Run `run.py computer <run>`: the program looks for the client's OneDrive folder mounted into this chat. Not found: your WHOLE reply is the STOP text it prints (no question, no analysis); Paul connects the computer and tells you to go on. Found: every client file is read from there as real bytes (copied with `cp` into the run folder and logged with `--original`, the program compares the two byte for byte) and the finished PDF is saved there. No file is ever read cut off, and there is no size limit. Never request the connection yourself and never call a tool that opens a permission box.
2. **Microsoft 365 (SharePoint / OneDrive): a fallback for SMALL TEXT files only** (the form's `.json`, a transcript as text), used when Paul has said to go on without the computer or a file is not on the computer. It returns files cut off and a PDF as text, so the form's saved PDF is NEVER taken through it. Every copy is logged with `--file` and `--source-size` and the program refuses a copy of a different size. Search the client's folder in BOTH locations under `liferisk.co.za` (`Company - Paul`, and `Company - WR Clients` → `Paul Kafentzis (Client Files)`) and use whichever has the file.
3. **Zapier — the Office 365 and Teams tools.** The next route when Microsoft 365 fails for a file, and the route for whatever Microsoft 365 cannot do (posting to Teams).
4. **Never ask Paul** for permission, to click Allow, to attach, upload or drag a file, or to say "go". If every route failed for a file, say in at most five lines what failed (the log of the tries) and stop. The only question this skill may put to Paul about files is the content question in "When the form's data file is missing" below.
5. **Never touch another broker's folder.** `Company - WR Clients` holds a separate `(Client Files)` folder for every broker at the firm. `Paul Kafentzis (Client Files)` is the only one under `Company - WR Clients` this skill ever reads from or writes to. This restriction does not apply to `Company - Paul`, which is Paul's own folder.

This applies to **locating the Audio to Text file, transcript and Overview** (Steps 1 and 1b below), to **checking the client's other documents for a field that can't otherwise be resolved** (Step 3 below), and to **saving every deliverable this skill chain produces** (Step 5a below) — same order, every time.

## Out of scope: no transcript, but a Fact Find already exists

If the client already has a **completed** Fact Find document and there is **no accompanying meeting transcript** to populate from, this skill does not apply. Go straight to the `fact-find-summary` skill against the existing completed FF instead. That skill has its own rule for this exact case: it still produces the summary PDF, but the Planner note (always made by `client-teams-transcript-skill`'s program and presented as its copy-ready page, per Step 7b below) can't be produced with no transcript to summarize — say so explicitly rather than silently omitting it.

## Step 1: Gather inputs (source order — rule 11)

Gather in this order, per the Client File Access order above:

1. **The Fact Find form's data file (named `Fact Find (Audio to Text)`)** — see Step 1b. This is the first and primary source.
2. **The transcript(s)** — usually `.docx`, sometimes text despite the extension. The file is named `Teams meeting transcript - DD.MM.YY - (Client Name)_ Annual Review [year]` (or `... - FF`, or with another suffix) — search the client's `2. Fact Find` folder for the meeting date and client name; identify by content, not only by name (rule 10).
3. **The client's latest Overview** in the `1. Overview` folder (see Step 1b). Reference only.
4. **The Manual Fact Find — only if the Audio to Text file is absent** (see Step 1b).

If the Audio to Text file and the transcript are both missing after checking the client's folder, ask for them — unless a completed FF already exists with no transcript (see Out of scope).

- **Multiple transcripts for one meeting:** if the client's Teams call dropped and reconnected, there will be two (or more) transcript files for the same date. Read all of them and treat them as one continuous meeting.
  - **Verify continuity before summarizing anything.** Check that the last exchange of transcript N and the opening exchange of transcript N+1 pick up the same topic/figure. If there's a real gap, flag it rather than silently filling it in.

## When the form's data file is missing (Paul's rule: stop and ask)

If the form's data file is not found on the computer, in Microsoft 365 or through Zapier (all three tried, in that order, each try logged), the program STOPS and ASKS Paul. It never carries on quietly. Run `run.py ask {run} --need form --searched "<where you looked>"`: it prints the exact question, "use the filled-in Manual Fact Find PDF as the first source, or work from the transcript alone?". Wait for Paul's answer, then record his own words: `run.py answer {run} --need form --said "<his words>" --choice manual|transcript`. From then on every value comes from that source (the Manual Fact Find, or the transcript alone), each with its source, and the final printout says so.

## The form's saved PDF

The form also saves a PDF of the same Fact Find (`Fact Find (Audio to Text) - DD.MM.YYYY - Name Surname.pdf`) in the client's `2. Fact Find` folder. It is a source too: `run.py formpdf` reads its text and checks that every populated value of the data file is in it. A value the program cannot find is reviewed by eye (`run.py pdfreview`); a real disagreement is flagged with both values and the data file's value is used.
