## Step 1c: Correspondence check - CURRENT transactions only - follow-up meetings only

Emails back and forth with the client and the providers are part of the evidence, so check them - but only the ones about the transactions in this advice cycle. Not applicable at a first/Fact Find meeting (no prior proposal emails exist yet).

1. **What to check (Outlook, via the Microsoft 365 tools; record it with `run.py source --kind Correspondence`):** (a) the client's replies to the proposal emails sent for the current quotes; (b) the provider/insurer quote emails for the current quotes and any email requesting or chasing a quote; (c) our own sent emails for these transactions, and any reply or acknowledgement; (d) anything sent or received since the previous meeting that concerns these products.
2. **What NOT to check:** historical correspondence from earlier years, unless Paul explicitly asks.
3. **Use it:** confirm acceptances (Step 4), confirm what was sent and when, spot anything outstanding and report it as Still open. Follow `outlook-emails-skill` tracking.
4. Never send an email from this skill. Where an email should be sent (e.g. a revised-quote request, Step 4b), prepare a DRAFT, show it to Paul and only send after his explicit yes.

## Step 2: Build the context pack (mandatory, every follow-up run; not applicable at a first/Fact Find meeting)

Inside the client's folder, read in this order (all PDFs; render pages as images if text extraction is empty), and record each document with `run.py source`:

1. `2. Fact Find\Fact Find Transcript - ... .pdf` and `Fact Find - ... .pdf` (the client's baseline).
2. The Fact Find Summary PDF.
3. **Every** earlier `Follow-Up Appointment Summary Notes - ... .pdf` (and any `WhatsApp Call Summary`), oldest to newest.
4. **The most recent** `1. Overview\2026\WR Overview - ... .pdf`.
5. **Quotes:** open `Comparative Quotes` in each transaction folder. Record insurer, type, CP/quote number, date and premium.
6. If something is missing, say so in one line and continue with what exists.

From this build two working lists (not saved anywhere):
- **Quote register:** every quote on file with insurer, type, number, premium, date.
- **Area ledger:** for each planning area, what was previously discussed, decided, requested and still outstanding. **At a first/Fact Find meeting, the area ledger is simply the Fact Find's own content, reorganised under the eight planning areas** - everything is `New` (nothing to carry forward yet).

## Step 2b: Read the applications (mandatory when applications exist; not applicable at a first/Fact Find meeting)

1. In every **current** transaction folder, list `Applications` and pick the real applications. List the folders on the client's own machine/OneDrive for the real state.
2. Stage them and read the filled field values. Note each file's last-modified date against the meeting date.
3. Compare each application against the transcript and against each other for shared details, and against the accepted quote and meeting date.
4. Applications are only ever compared and reported here; they are changed in Step 6 via `complete-applications-skill`.
