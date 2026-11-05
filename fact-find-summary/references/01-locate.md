Contents: where the Fact Find Transcript PDF is, the three routes, saving.

## Where it is
- The client's folder is `[Business Segment]/[Surname], [First Name]/2. Fact Find`, under `liferisk.co.za` in **either** `Company - Paul` (used for New Business, but not limited to it) **or** `Company - WR Clients` -> `Paul Kafentzis (Client Files)` (current clients). A client's material could sit under either: check both and use whichever has the file.
- The file is `Fact Find Transcript - DD.MM.YY - (First Surname).pdf`. If there are several, use the one for the meeting date Paul gave.

## How the PDF is reached (nothing is asked of Paul except the one connection click)
In a cloud chat the computer is a separate machine reached through the device tools. Load them (ToolSearch, `select:mcp__remote-devices__get_device_info,...`), call `get_device_info`, and if `liferisk.co.za` is not in `connectedFolders` call `device_request_folder_access` for `~/liferisk.co.za`: that one request is the only click Paul is ever asked for. `device_list_dir` the client's folder and record it with `run.py computer`. If the request is refused or the tools do not exist, `run.py computer --none "<what happened>"`: its STOP text is your whole reply.
0. **passed**: in the Fact Find chain `ff-population-transcript` has just made this PDF in the same chat. Use that file directly (`run.py access --route passed --result found`, then `run.py source --route passed`). The connection is still recorded first, because the Summary is saved on the computer.
1. **device**: `device_bash` gives the file's fingerprint and size on the computer (`sha256sum` and `stat -c %s` at `$HOME/mnt/liferisk.co.za/...`), `device_stage_files` (Windows path, backslashes) puts a whole copy under `/mnt/user-data/uploads/liferisk.co.za/...`, and `run.py access --route device --device-output` compares the two.
Microsoft 365 and Zapier are never used for this PDF: it arrives there cut off, as text. If the PDF cannot be found, say in at most five lines what failed and stop: never ask Paul to attach, upload or drag a file. A project's file list is a convenience cache, not a substitute for the client's folder.

## Never touch another broker's folder
`Company - WR Clients` holds a separate `(Client Files)` folder for every broker. `Paul Kafentzis (Client Files)` is the only one under it this skill ever reads from or writes to. This restriction does not apply to `Company - Paul`, which is Paul's own folder.

## Two spouses in one meeting
Run this skill once per spouse, each from that spouse's own Fact Find Transcript PDF, each saved into that spouse's own `2. Fact Find` folder. Start the run with `--joint "Other Surname"` (and `--spouse-pdf` with the other spouse's PDF if you have it) so that the Summary opens with the one-line joint-meeting note.

## Saving
Save the Summary into the same `2. Fact Find` folder the PDF was found in, ON THE COMPUTER: copy it to `/mnt/user-data/outputs/`, then `device_commit_files` (no force). **After every save, prove it with the computer's own eyes:** `device_list_dir` the folder and run `sha256sum` and `stat -c %s` on the saved file with `device_bash`; the program compares them with the PDF it built.
