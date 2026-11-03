Contents: the Retirement and Investment email page, and what the program does with it. A Risk ROA embeds no email.

**Non-negotiable:** finding the original proposal is not enough. The document embedded in the ROA must be, or include, **the client's own reply email confirming the go-ahead**, with the original proposal quoted beneath it. An embed that opens on the adviser's proposal, with the client's acceptance nowhere in the document, is an incomplete ROA and must be rebuilt. The program refuses such a page.

**What you write (one HTML page, as before).** Take the already-built proposal HTML and its `<body>` inner content as the quoted portion. Put above it:
1. A header block for the reply itself in the same styled table as the proposal's own header: From (the client's own address), Sent (the reply's actual local sent time: convert `sentDateTime` from UTC to SAST, UTC+2, and format it as Outlook does, for example "Wednesday, 12 August 2026 10:46"), To, Cc, Subject (usually "Re: ...").
2. The client's own message body verbatim (for example "kindly proceed with the attached").
3. A plain divider line "On [day, date] at [time], [forwarder] wrote:", then the quoted proposal with a left border (for example `border-left:3px solid #cccccc; padding-left:16px`), so the reply-versus-quote structure reads like a real email thread.
Use generous spacing (for example `line-height:1.35`, about 14 px paragraph margins), never compressed. Simplifying markup is fine. Find the reply by matching the subject line, not just the sender and date.

**What the program does (fixed, never by hand).**
- Rewrites every `font-size` value in the page by one factor so the dominant body size becomes **15 pt** (the embedded image is shown at 5,000,000 EMU wide, so 15 pt displays as the ROA's own 11 pt Aptos). Never `--zoom`.
- Renders it with **wkhtmltopdf**, never LibreOffice (which bakes thin lines under the text), at page 8.5 x 11 in with 0.5 in margins on every side, then turns each page into a 150 dpi JPEG.
- Embeds the pages as standalone, bordered picture paragraphs, each kept with a small italic "page X of Y" caption, no blank spacer between them, width at most 5,000,000 EMU, **never inside a table cell** (a table row holding full-page images splits and its borders bleed into the footer).
- Inserts them right after the active section's table: before "Investment Planning" for a Retirement ROA, before "POLICY REPLACEMENT" for an Investment ROA. (The Retirement heading has regressed before: the program decides it from the bundle.)
- The reason box itself holds only the pointer line: "The client's email reply confirming their go-ahead on this proposal ([date]), with the original proposal email quoted in full beneath it, is reproduced on the following pages." The checker reads the rendered first page: it must open on the client's own reply.
