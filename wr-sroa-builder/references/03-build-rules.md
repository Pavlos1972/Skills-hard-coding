# What the build does (nothing here is typed by you)

`run.py build` assembles the data from your confirmed answers and draws the PDF with the fixed script `build_sroa.py` (reportlab; styled like the original Wealth Revolution template, a freshly generated PDF, not the original fillable form). You never edit the script, the data or the PDF. If something is wrong, fix the answers and rebuild.

**The four blocks, always in this order**
1. **Block 1: Servicing FNA Quote.** That quote's own cover figures under the standard grouped headings (standalone figures, not old-to-new). If the client declined the FNA: the one-line note "Not compiled — declined by the client." Never omitted, never invented figures.
2. **Block 2: Shortfall Quote.** Full block only if one was compiled; otherwise the one-line "Not compiled for this client." (minimal wording, no explanation of why). Never omitted.
3. **Block 3: Alternative Quote.** Same rule as Block 2. The accepted quote's block carries " (Accepted)" in its title (the common case is "Alternative Quote (Accepted)").
4. **Block 4: Requested Servicing Change/s.** The Current Policy Schedule to the accepted quote, old → new or "No change (value)", with the line "Policy Number: ... | Accepted Quote — CP Number: ..." above it when there is a CP number. No inline "(FNA Quote reference: ...)" notes in Block 4: FNA figures belong in Block 1.

**Fixed by the script**
- Financial Advisor Code `FSP45946` and Name `Paul Kafentzis`, always.
- The ID number is its own line "ID Number :" directly under "Owner :".
- **No "Signed at" line**; this SROA has only dates.
- **Two separate fillable date fields, one under each signature** (client and advisor may sign on different days). Real fillable PDF fields, left empty.
- The client's name and "Paul Kafentzis" are typed as static text below their signature lines.
- **Two distinct signature lines side by side**, a clear gap between them, genuine blank space above each for a wet signature; the typed name and the caption ("Signature of Owner/Authorised Signatory", "Signature of Financial Advisor") sit below the line, never on or above it.
- Box heights size to their text. Long content (a 9-10 line BrightRock comparison) may legitimately push the signature block onto a second page, as one unit.
- The confirmation paragraph is fixed: "I confirm that the above information is a correct reflection of the advice provided in respect of the requested servicing changes and a copy of this document was provided to me in writing."
- Output: a standalone PDF only. No covering email for this document type.

**File name (derived by the program, never typed):** `SROA - [Insurer]_[Policy Number] - [DD.MM.YY] - ([First]_[Surname]).pdf`: an underscore between insurer and policy number; the SROA date confirmed with Paul, with dots; the client's everyday first name and surname (no middle names) in brackets with an underscore. The full legal name stays inside the document. The date in the name is the SROA date, not a signature date: the two signature dates are left blank for the client and the advisor to fill in.
