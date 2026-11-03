Contents: where the Fact Find Transcript PDF is, the three routes, saving.

## Where it is
- The client's folder is `[Business Segment]/[Surname], [First Name]/2. Fact Find`, under `liferisk.co.za` in **either** `Company - Paul` (used for New Business, but not limited to it) **or** `Company - WR Clients` -> `Paul Kafentzis (Client Files)` (current clients). A client's material could sit under either: check both and use whichever has the file.
- The file is `Fact Find Transcript - DD.MM.YY - (First Surname).pdf`. If there are several, use the one for the meeting date Paul gave.

## The three routes, in this order, every try logged
1. **device**: the computer, through the device bridge (local drive / OneDrive). Always attempted first, whatever the time of day. A failed attempt is an ordinary event: log it and go on.
2. **m365**: the Microsoft 365 connector (SharePoint / OneDrive), the same two locations.
3. **zapier**: the Zapier Office 365 tools.
Record each try with `run.py access`. Ask Paul to attach the file only once all three have been tried and failed. A project's file list is a convenience cache, not a substitute for the client's folder.

## Never touch another broker's folder
`Company - WR Clients` holds a separate `(Client Files)` folder for every broker. `Paul Kafentzis (Client Files)` is the only one under it this skill ever reads from or writes to. This restriction does not apply to `Company - Paul`, which is Paul's own folder.

## Two spouses in one meeting
Run this skill once per spouse, each from that spouse's own Fact Find Transcript PDF, each saved into that spouse's own `2. Fact Find` folder. Start the run with `--joint "Other Surname"` (and `--spouse-pdf` with the other spouse's PDF if you have it) so that the Summary opens with the one-line joint-meeting note.

## Saving
Save the Summary into the same `2. Fact Find` folder the PDF was found in. **After every save, list the folder and confirm the listed size equals the size of the local file (a new time with the old size means the copy lagged: commit again and re-list).**
