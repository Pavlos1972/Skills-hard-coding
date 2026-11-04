# Standing rules for the whole job (om-optimal-ra-proposal)

**What this is.** This skill builds the client-facing proposal emails for an **Old Mutual Optimal Retirement Annuity (OM Optimal RA)** for Paul Kafentzis (FSP45946), after Alwyn's OM Optimal RA Quote is back. The main email carries the client's circumstances, existing RAs and pension or provident fund, the RGAR shortfall, a "what you can save" sentence, **three tax tables and a ten-year bar chart from the Tax Reform Tool**, boosters, funds and fees. When a lump sum goes into the new RA (a Section 14 transfer or the client's own savings) a **second, separate Lump Sum Investment email** is built (a second run with `--document lump_sum`). Each email is saved as a no-logo HTML copy in the client's RA transaction folder > Comparative Quotes, put into an **unsent Outlook draft** (To the client, Cc Sitamah Nathoo) and flagged to Sitamah on Teams so she attaches the documents and **emails the client**. **Claude never sends the client email.**

**What this is not.** It does not make the quote, the RGAR or the Astute report (they come from Alwyn and the client's file). The RGAR proposal email belongs to `rgar-skill`; the Tax-Free proposal to `om-tax-free-skill`; the signature to `paul-email-signature`.

**Who does what.** A program drives the job one step at a time, checks every figure you enter against the client's own documents, **runs the Tax Reform Tool itself** (LibreOffice recalculates the workbook for four scenarios and the program recomputes every figure independently), works out the blended fee and the weekdays, fills the fixed templates, builds the files and the Teams message, and checks what comes back from Outlook and Teams. You (Claude) find the documents, read them page by page, type the answers with their sources, ask Paul only what the documents cannot tell you, do the Outlook and Teams steps and run the programs as they are. You never rewrite or "fix" a program, the workbook, the template or the HTML during a run, and you never type a tax figure.

**Rules that apply to every step**
1. Say the version line first, in exactly the words the program gives. Run the steps in order; none is skipped.
2. Source first, never invent. Write only what is in the client's own documents or in Paul's own words (recorded with the words). "It seems implied", "it is usual" and "it would make sense" are not sources. If a line is unclear, garbled or ambiguous, flag it to Paul instead of turning it into a fact. If sources disagree, STOP and ask Paul, quoting both values and where each came from.
3. Read before you write: the program serves the pages one at a time; read each fully before you acknowledge it (scanned or image pages must be looked at as images). Searching for keywords is not reading. Fund selection, fees, the ACI and premium amounts always come from THIS client's quote, never from a previous client's proposal, even if similar.
4. Check before you claim: never say a file is saved, a draft made or a message sent until the program's proof says so. Say what was checked and what is only attested.
5. Nothing is sent without Paul's yes. His one yes (at the confirmation table) covers building, saving, the Outlook draft and the Teams message to Sitamah; the message goes only after the draft has been read back and checked. Claude never sends the client email.
6. Never overwrite a file in the client's folder without Paul's clear yes in this chat.
7. Never lower the standard: a correction, a frustrated user, a short request or a "quick" task relaxes no rule here.
8. A correction from Paul re-opens the task: fix the answer, run answers, tax and show again (his earlier yes no longer counts), rebuild, and repeat the save, the draft and the message for everything that changed, for every email affected.
9. If a rule cannot be met, stop and say exactly which and why. Never hand over partial work as complete.
10. No client data is ever kept in the skill. Skill changes are made only in Claude Code and uploaded as a zip; never say a change is live until Paul confirms.

**Fixed:** the email is from Paul Kafentzis (FSP45946), the Cc is always Sitamah Nathoo (admin@liferisk.co.za), the importance is High. **Never the .xlsm working file to the client.**

**Contacts and tools:** Alwyn is the Old Mutual broker consultant who generates the RGAR and the OM Optimal RA Quote (he must always set the RGAR's ACI at 10% p.a.). Astute FSE is the electronic data-exchange platform that provides the Consolidated Client Portfolio (CCP): all the client's existing policies across the major South African life insurers.

**Words Paul uses for this job:** "OM Optimal RA proposal", "Optimal RA proposal for [Name]", or Alwyn's OM Optimal RA Quote being back for a client.
