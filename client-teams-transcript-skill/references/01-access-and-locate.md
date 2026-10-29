## Client File Access (standing rule - every read/save of a client file)

Claude HAS access to Paul's files, mail and Teams. Use these routes in this order and log every attempt with `run.py access`:

1. **device** - the local machine via the device bridge (`device_stage_files`, `device_commit_files`). Check BOTH `liferisk.co.za\Company - Paul` (New Business and more) and `Company - WR Clients\Paul Kafentzis (Client Files)` (current clients); same `[Segment]\[Surname], [First Name]\...` structure; use whichever holds the client.
2. **m365** - the Microsoft 365 connector: `sharepoint_search`/folder search in the same two locations, Outlook mail and calendar, and Teams meeting transcripts (the connector has permission to read them). Use it when the local machine genuinely cannot be reached.
3. **zapier** - the Zapier Office 365 and Teams tools, for anything the two routes above cannot do.
4. **Ask Paul to attach only after all three routes failed and are logged** (`run.py ask` records the question and the errors). Never say "I cannot access your files" without that log.
5. **Never touch another broker's folder** in `Company - WR Clients`. `Company - Paul` is Paul's own.

## Step 0: Locate the transcript

- If Paul's message reads `[Client] - Appointment transcript summary - DD/MM/YYYY`, that date is the meeting date. Look for `Teams meeting transcript - DD.MM.YY - ...` (.docx) in the client's `2. Fact Find` folder; match loosely (typos happen). Never fall back to the newest file when a date was given. Dates are always DD/MM/YYYY.
- No date given: take the newest unsummarised transcript and mention any older unprocessed ones.
- Stage it with `device_stage_files` (or fetch it through the m365 route), then `tx.py prep` converts it with `pandoc -t plain --wrap=none`.
- Not in the folder yet: if the meeting has finished, use the `client-transcript-download` skill to fetch it (Claude in Chrome), then continue. If that is not possible (all three routes logged as failed), ask: "Please upload this client's Teams Meeting Transcript". Never summarise from a title or memory.
- A WhatsApp call has no transcript file: ask Paul for his recap/notes or recording and confirm the exact date and TIME of the call before drafting (log it as route `user`; `tx.py prep` then needs `--notes`).
- **For a first/Fact Find meeting reached via `ff-population-transcript`'s Step 7b, the transcript is already in hand (passed in directly)** - skip the locating (log it with `--route passed`), but NOT the two reads: go straight to Step 1b and do both reads there.

## Step 1: Verify the transcript is complete

Compare the stated total duration with the last timestamp; check for jumps. If truncated or gapped, say exactly what is missing and stop. `tx.py prep` makes this check and stops by itself.
