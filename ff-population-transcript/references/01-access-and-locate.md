# Client File Access (standing rule: every step that reads or saves a client file)

Every time this skill needs a client's document, or needs to save a newly produced deliverable into the client's folder, follow this exact order, every time, without asking first:

1. **Local machine - always attempted first.** Connect via the device bridge to Paul's local machine and check **both** of these locations under `liferisk.co.za` for the client's folder (same `[Business Segment]/[Surname], [First Name]/Fact Find` structure under each): `Company - Paul` (used for New Business, but not limited to it) and `Company - WR Clients` -> `Paul Kafentzis (Client Files)` (used for current/existing clients). A given client's material could sit under either - check both and use whichever one actually has the file. This connection is expected to succeed and must be tried first, every time - never skip straight to asking Paul to attach something. If this session has no live device-bridge connection to Paul's computer yet, request it before doing anything else that depends on client files. Use the file tools only: list the folder, stage the files, commit the finished PDF. Never run shell commands on his computer.
2. **SharePoint (the Microsoft 365 connector) - only if the local machine genuinely can't be reached.** If, and only if, the device bridge cannot connect to Paul's computer this session (or a request was refused), fall back to the identical two-location check via SharePoint. A PDF read this way arrives cut off, as text, so do not trust it as the whole file. Saving through it needs the file's content as base64 text in one message, which has a real practical ceiling: a large PDF may need lossless compression first (for example `qpdf --recompress-flate --object-streams=generate` followed by `gs -dPDFSETTINGS=/ebook`). Always visually re-verify a compressed PDF before treating it as the deliverable.
3. **Zapier (the Office 365 tools)** for what the connector cannot do.
4. **Say plainly what is blocking - last resort only.** Only once all of these have genuinely been tried and none works, say in at most five lines what was tried and what failed. Never ask Paul to attach or upload a file, and never say "I cannot access your files" without that list.
5. **Never touch another broker's folder.** `Company - WR Clients` holds a separate `(Client Files)` folder for every broker at the firm. `Paul Kafentzis (Client Files)` is the only one under `Company - WR Clients` this skill ever reads from or writes to. This restriction does not apply to `Company - Paul`, which is Paul's own folder.

This applies to locating the form's files, the transcript and the Overview (step 1), to checking the client's other documents for a field that can't otherwise be resolved (step 5), and to saving every deliverable this skill chain produces (step 7), same order, every time.

## Out of scope: no transcript, but a Fact Find already exists

If the client already has a **completed** Fact Find document and there is **no accompanying meeting transcript** to populate from, this skill does not apply. Go straight to the `fact-find-summary` skill against the existing completed FF instead.

## What to look for

- **The form's files** in the client's `2. Fact Find` folder: `Fact Find (Audio to Text) - DD.MM.YYYY - Name Surname` as a `.json` and a `.pdf`.
- **The transcript(s)**, usually `.docx`, sometimes text despite the extension: `Teams meeting transcript - DD.MM.YY - (Client Name)_ Annual Review [year]` (or `... - FF`, or another suffix). Search the client's `2. Fact Find` folder for the meeting date and client name; identify by content, not only by name.
- **The client's latest Overview** in the `1. Overview` folder. Reference only.
- **Multiple transcripts for one meeting:** if the client's Teams call dropped and reconnected, there will be two (or more) transcript files for the same date. Give all of them to `run.py files` (one `--transcript` each): the program joins them and checks each one. **Verify continuity before summarizing anything.** Check that the last exchange of transcript N and the opening exchange of transcript N+1 pick up the same topic/figure. If there's a real gap, flag it rather than silently filling it in.
- If the form's files and the transcript are both missing after checking the client's folder, say so (step 1's `--missing`) - unless a completed FF already exists with no transcript (see Out of scope).
