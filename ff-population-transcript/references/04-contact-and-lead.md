# Contact details and lead source

## Step 1c: Contact details & lead source (mandatory — complete before populating Client Info and before the report is finished)

Paul's rule (06/10/2026): the contact fields and Referral From must never come out blank or "Not discussed" when the information exists somewhere.

**A. Find the contact details** in the Audio to Text file first (cell, work number, home number, personal email, work email), then in the transcript, then in the client's documents on file (payslip, group risk statement, Overview). Record exactly what was said/written. If a number or address was read out on the call, transcribe it digit for digit once confirmed. If the sources disagree, the Audio to Text value is used and the disagreement flagged with both values. Only write "Not discussed" after this search AND part C have both been done and nothing was found.

**B. Establish the lead source: Referral or D&R Marketing?**
1. Take it from the Audio to Text file's Referral field and from what was said in the transcript.
2. **Always search Outlook** for a D&R Marketing appointment email for this client, before the Fact Find is finalised. Use Microsoft 365 email search: first the folder `Leads - D&R Marketing` under `Business` in Paul's Inbox, then the whole mailbox for the client's name + "Appointment from D & R Marketing" (sender Di Heath, `mwpalwyn@mweb.co.za`).
3. **If a D&R email is found:** set **Referral From = `D&R Marketing lead - [DD/MM/YYYY date the email was received]`**.
4. **If no D&R email exists**, use the Audio to Text file's Referral value (for example "Current client"), or the referrer named in the transcript, or `Referral - referrer not stated (please confirm)`.

**C. Populate Client Info from the D&R email (D&R leads only).** Map occupation title, company name, area, Tel/Cell, email, age (cross-check DOB), salary bracket (Notes only, never Gross Income). What is in the Audio to Text file or was said on the call always wins over the lead email.

The Fact Find Summary produced from this Fact Find (7a) must carry the same contact details and Referral From value.

**Program:** record the Outlook search with `run.py access --need lead --route m365 --tool <the Outlook search tool> --result ok --detail "<what you searched>"`, the email (when found) with `run.py source --kind Correspondence ... --text-file <its text>`, then `run.py lead` (folder result, mailbox result, the date received). The program writes `Referral From` itself. A salary bracket from the lead email goes in Notes only, never in Gross Income (the checker fails it). Contact details may be called `Not discussed` only after this step is done.
