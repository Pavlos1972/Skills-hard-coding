# Where the files are, and what to do when the form's file is missing

Reads the client's **Fact Find (Audio to Text) file** (first and primary source), the **Teams meeting transcript(s)** (second, equally important source) and the client's **latest Overview** (reference), and builds the Wealth Revolution Client Fact Find as a completed document that follows the Audio to Text file's own layout (WR Fact Find v3.0), section by section, in its exact order. Drawn by a program and delivered as a PDF — see Step 5. **Every deliverable this skill produces is saved directly into the client's own folder — see Step 5a. This is not optional and Paul should never have to ask for it.**

## Client File Access (standing rule — applies to every step below that reads or saves a client file)

Every time this skill needs a client's document, or needs to save a newly produced deliverable into the client's folder, follow this exact order, every time, without asking first:

1. **Local machine — always attempted first.** Connect via the device bridge to Paul's local machine and check **both** of these locations under `liferisk.co.za` for the client's folder (same `[Business Segment]/[Surname], [First Name]/Fact Find` structure under each): `Company - Paul` (used for New Business, but not limited to it) and `Company - WR Clients` → `Paul Kafentzis (Client Files)` (used for current/existing clients). A given client's material could sit under either — check both and use whichever one actually has the file. This connection is expected to succeed and must be tried first, every time — never skip straight to asking Paul to attach something. If this session has no live device-bridge connection to Paul's computer yet, request it before doing anything else that depends on client files. **The time of day never changes this: always try all three routes, log every try with `run.py access`, and never skip a route or comment on a failure because of the time of day.**
2. **SharePoint — only if the local machine genuinely can't be reached.** If, and only if, the device bridge cannot connect to Paul's computer this session, fall back to the identical two-location check via SharePoint. This should be rare — treat a failed local connection as the exception, not the default path. Be aware this path requires embedding the file's content as base64 text in one message when saving, which has a real practical ceiling — a large PDF may need lossless compression first (e.g. `qpdf --recompress-flate --object-streams=generate` followed by `gs -dPDFSETTINGS=/ebook`). Always visually re-verify a compressed PDF before treating it as the deliverable.
3. **Zapier — the Office 365 and Teams tools — the third route.** Use it for whatever the two routes above cannot do.
3b. **Ask Paul to attach the file — last resort only.** Only once the local machine, Microsoft 365 and Zapier have all genuinely been tried and logged, and none works does this skill ask Paul to upload the Audio to Text file, transcript or other source directly, or say plainly what's blocking the folder save.
4. **Never touch another broker's folder.** `Company - WR Clients` holds a separate `(Client Files)` folder for every broker at the firm. `Paul Kafentzis (Client Files)` is the only one under `Company - WR Clients` this skill ever reads from or writes to. This restriction does not apply to `Company - Paul`, which is Paul's own folder.

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
