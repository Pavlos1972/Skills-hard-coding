Contents: sending and saving, the receipts, the short audit.

1. **Send the PDF in the chat** as a file. Do not describe the Summary in chat text instead.
2. **Save it** into the client's own `2. Fact Find` folder on the computer (`device_commit_files`), then **list the folder** (`device_list_dir`) and fingerprint the saved file on the computer (`device_bash`: `sha256sum` and `stat -c %s`).
3. **Look at the page images** the build step made.
4. **Record the receipts** with `run.py receipt` (the step shows the exact commands). The checker compares the computer's fingerprint and the listed size with the local file's and checks that the folder is this client's own `2. Fact Find` folder under `Company - Paul` or `Paul Kafentzis (Client Files)`.
5. **The reply** is the SHORT AUDIT that `run.py done <run> final` prints, exactly as it is:
   - one line per check, point form, a green tick or a red cross;
   - one closing line, "Only attested (not proven): ...", for what the program cannot prove (that the PDF was sent in the chat, that the fingerprints pasted from the computer's shell are the computer's, the page images looked at, Paul's yes);
   - the result, PASS or FAIL.
   Nothing longer. The full record stays on disk in `out/audit-full.txt`.
6. This skill makes and sends no message. The Planner note and the message to Sitamah are made once, by `client-teams-transcript-skill`.
