Contents: where the client's folder is, and how to save without overwriting.

1. **Find the client's folder** under `liferisk.co.za`, in both locations: `Company - Paul\New Business\{Surname}, {First name}\2. Fact Find\` or `Company - WR Clients\Paul Kafentzis (Client Files)\...\{Surname}, {First name}\2. Fact Find\`. A client's material could sit under either: check both and use whichever has the client.
2. **Routes, in order, every try logged:** the computer (device bridge) first, then the Microsoft 365 connector (SharePoint / OneDrive), then Zapier. Ask Paul only after all three have failed.
3. **Never touch another broker's folder.** `Paul Kafentzis (Client Files)` is the only one under `Company - WR Clients` this skill reads from or writes to. If the folder is not found or is ambiguous, ask Paul.
4. **Copy (not move)**, with `cp -n`, into that `2. Fact Find` folder, using the file the program built in out/ (its name is derived, never typed): `Teams meeting transcript - DD.MM.YY - (First Surname).docx`. If a file with that name already exists, do not overwrite it: record `save.already_existed yes` and tell Paul.
5. **After every save, list the folder and confirm the listed size equals the size of the local file (a new time with the old size means the copy lagged: commit again and re-list).** The program compares the two numbers.
