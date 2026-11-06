## Client File Access (standing rule - every read/save of a client file)

Claude HAS access to Paul's files, mail and Teams, and finds them BY ITSELF. The client's documents are whole files on Paul's computer (OneDrive, folder `liferisk.co.za`), reached through the device tools, so the chat connects to the computer ONCE, at step 1, and the finished PDF is saved there too. Nothing else is ever asked of Paul. Log every attempt with `run.py access` (or `run.py source` for a client document):

1. **device** - the computer, through the device tools (`get_device_info`, `device_request_folder_access` for `~/liferisk.co.za` only if the folder is not already connected, `device_list_dir`, `device_bash`, `device_stage_files`, `device_commit_files`). That one connection request is the only click Paul is ever asked for. If it is refused or the tools do not exist in this chat, record it with `run.py computer --none "<what happened>"`: the program prints a one-line STOP and your whole reply is that line. Every file is taken as a whole staged copy and PROVED identical to the original by the computer's own fingerprint (`sha256sum` and `stat -c %s` run with `device_bash`, compared by the program with the copy). Search BOTH `liferisk.co.za\Company - Paul` (New Business and more) and `Company - WR Clients\Paul Kafentzis (Client Files)` (current clients; same `[Segment]\[Surname], [First Name]\...` structure; use whichever holds the client).
2. **m365** - the Microsoft 365 connector, for what is not a file: Outlook mail and calendar (the correspondence), the Teams transcript itself (text; `tx.py prep` must say it is complete) and searching for a document. It returns a PDF or a Word file cut off, as text, so a client document is NEVER taken through it, and nothing is saved through it.
3. **zapier** - the Zapier Office 365 and Teams tools, when Microsoft 365 failed for a transcript or an email. The same limits.
4. **Never ask Paul** for permission, to click Allow (apart from the one connection request above), or to attach, upload or drag a file. If every route failed and is logged, say in at most five lines what failed and stop. Never say "I cannot access your files" without that log.
5. **Never touch another broker's folder** in `Company - WR Clients`. `Company - Paul` is Paul's own.

## Step 0: Locate the transcript

- If Paul's message reads `[Client] - Appointment transcript summary - DD/MM/YYYY`, that date is the meeting date. Look for `Teams meeting transcript - DD.MM.YY - ...` (.docx) in the client's `2. Fact Find` folder; match loosely (typos happen). Never fall back to the newest file when a date was given. Dates are always DD/MM/YYYY.
- No date given: take the newest unsummarised transcript and mention any older unprocessed ones.
- Take the file from the computer first (stage a whole copy and prove it with the computer's fingerprint: `run.py access --need transcript --route device ... --file ... --device-output ...`). Only when it is not in the folder, read the Teams transcript itself through Microsoft 365 (then Zapier) and save the text into the run folder. Then `tx.py prep` converts it with `pandoc -t plain --wrap=none` and checks it is complete; run it on the proved copy.
- Not in the folder yet: if the meeting has finished, use the `client-transcript-download` skill to fetch it, then continue. If every route is logged as failed, say so in at most five lines and stop. Never ask Paul to upload it. Never summarise from a title or memory.
- A WhatsApp call has no transcript file: ask Paul for his recap/notes or recording and confirm the exact date and TIME of the call before drafting (log it as route `user`; `tx.py prep` then needs `--notes`).
- **For a first/Fact Find meeting reached via `ff-population-transcript`'s Step 7b, the transcript is already in hand (passed in directly)** - skip the locating (log it with `--route passed`), but NOT the two reads: go straight to Step 1b and do both reads there.

## Step 1: Verify the transcript is complete

Compare the stated total duration with the last timestamp; check for jumps. If truncated or gapped, say exactly what is missing and stop. `tx.py prep` makes this check and stops by itself.
