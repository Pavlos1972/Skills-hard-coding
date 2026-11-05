## Client File Access (standing rule - every read/save of a client file)

Claude HAS access to Paul's files, mail and Teams, and finds them BY ITSELF, with no permission step and no help from Paul (the chat is on Auto and the Microsoft 365 connector is approved). Use these routes in this order and log every attempt with `run.py access`:

1. **device** - the local machine via the device bridge, ONLY if this chat is already connected to it. Never request the connection and never call a tool that opens a permission or folder-access box. If it is not connected, log it at once as a fail (`not connected; not requested`) and go straight to 2.
2. **m365** - the Microsoft 365 connector, the working route: `sharepoint_search`/folder search in BOTH `liferisk.co.za\Company - Paul` (New Business and more) and `Company - WR Clients\Paul Kafentzis (Client Files)` (current clients; same `[Segment]\[Surname], [First Name]\...` structure; use whichever holds the client), Outlook mail and calendar, and Teams meeting transcripts (the connector has permission to read them). Read each file through the connector and save what it returns into the run folder. To SAVE a file, the content goes in as base64 text (a large PDF may need lossless compression first).
3. **zapier** - the Zapier Office 365 and Teams tools, for anything the connector cannot do and as the next route when it fails.
4. **Never ask Paul** for permission, to click Allow, or to attach, upload or drag a file. If every route failed and is logged, say in at most five lines what failed and stop. Never say "I cannot access your files" without that log.
5. **Never touch another broker's folder** in `Company - WR Clients`. `Company - Paul` is Paul's own.

## Step 0: Locate the transcript

- If Paul's message reads `[Client] - Appointment transcript summary - DD/MM/YYYY`, that date is the meeting date. Look for `Teams meeting transcript - DD.MM.YY - ...` (.docx) in the client's `2. Fact Find` folder; match loosely (typos happen). Never fall back to the newest file when a date was given. Dates are always DD/MM/YYYY.
- No date given: take the newest unsummarised transcript and mention any older unprocessed ones.
- Read it through the m365 route (the Teams transcript itself, or the file in the client's folder) and save the text into the run folder, then `tx.py prep` converts it with `pandoc -t plain --wrap=none`.
- Not in the folder yet: if the meeting has finished, use the `client-transcript-download` skill to fetch it, then continue. If every route is logged as failed, say so in at most five lines and stop. Never ask Paul to upload it. Never summarise from a title or memory.
- A WhatsApp call has no transcript file: ask Paul for his recap/notes or recording and confirm the exact date and TIME of the call before drafting (log it as route `user`; `tx.py prep` then needs `--notes`).
- **For a first/Fact Find meeting reached via `ff-population-transcript`'s Step 7b, the transcript is already in hand (passed in directly)** - skip the locating (log it with `--route passed`), but NOT the two reads: go straight to Step 1b and do both reads there.

## Step 1: Verify the transcript is complete

Compare the stated total duration with the last timestamp; check for jumps. If truncated or gapped, say exactly what is missing and stop. `tx.py prep` makes this check and stops by itself.
