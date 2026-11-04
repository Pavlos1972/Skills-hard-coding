# complete-applications-skill: what changed, and what I need from you (04/11/2026)

No client data is kept in the new skill. Everything in it is invented (Pat Samplecase, Robin Testcase, example.invalid addresses, the invented insurer Samplelife; every ID number in the test is computed, never typed). The two blank insurer forms in `assets/` are the real blank forms, unchanged. The old text is archived in `SKILL.2026-10-14.md` (no client data in it) and the old script in `fill_om_form.2026-10-14.py`. The rule-by-rule check of the old skill against the new one: 365 rules, 0 unaccounted (126 kept word for word, 164 reworded, 75 dropped with a recorded reason; see `INVENTORY-REPORT.md`).

## What it is now
A program holds each application as ONE plan file: every field with its value and its source (a verbatim line of a registered document, or your own words). It fills the REAL blank form, reads back EVERY field and proves each filled box shows something. A checker then rebuilds everything and compares, so a PDF edited by hand cannot pass. Nothing is filled, saved, renamed or overwritten without your one yes; nothing is deleted. Your 12 Phase A answers are all built in.

## What I built into it (your Phase A answers)
- Both real forms are filled by program; the blank forms are frozen by checksum, every field, type and dropdown option, and the program stops if either one changes. The General form's field meanings (a table made once by hand) are frozen the same way.
- Every value needs a document line (its words or digits must be in that line) or your words; the order of preference is the Fact Find, the FICA documents, current applications, you. "CRM record" is gone. A previous year's application is never a source unless you say so.
- The N/A discipline, the replacement answer (`<Insurer>, Policy No. <number>` checked against the schedule document), the Product value (the form's own product plus the amount, added to the closed dropdown), the signature date (the meeting date, DD/MM/YY, never blank), `DateOfEntry` DD/MM/YYYY and the debit date (refused from the 10th to the 14th) are program rules.
- Flags only, never refusals: an ID number with a wrong date part or check digit, beneficiary shares that do not add up to 100%, an email or phone number that does not look right.
- The file name and the transaction folder name are built by the program from fixed lists; the folder is renamed only with your yes (`mv -n`); an existing file with the same name is never overwritten without your fresh yes; nothing is deleted (a possible older draft is only listed).
- A correction reads your live-completed application, shows old to new with the source, changes ONLY the planned fields, never touches a signature field, carries a detail only between the one-to-one pairs (or within the same form for anything not product-specific), refuses a product-specific detail unless you say so, and STOPS when two current applications disagree. It is saved in place with the same modified time you staged.
- The reply is the short audit (11 lines) and one short hand-back block per application, with ID and account numbers masked to the last 4.

## Questions that came up while building (Yes / No, recommended answers in brackets)
1. **Amounts are always written `R 2,800.00 p.m.`** (thousands commas, two decimals) in the Product value, the folder name and the file name. Your old examples mixed `R 1,000 p.m.` and `R 1,000.00 p.m.`. One rule, no guessing. (Yes)
2. **The risk cover names:** the file name uses Personal Covers, Business Covers, Buy & Sell, Contingent Liability and Keyman Cover; the folder name uses the same words except `Keyman` (as your old text had it). On the form, Personal Covers counts as Personal and the other four as Business. (Yes)
3. **Known abbreviations and short names:** Old Mutual = OM, Brightrock = BR; the product short names Optimal RA, Tax-Free and Flexi. Any other insurer or OM product needs your words before the program builds a name. (Yes)
4. **A Single, Divorced, Widowed or Separated client's marriage contract type is filled N/A by the program** (my reading of "any field with an N/A option that does not apply gets N/A, not blank"). (Yes)
5. **The hand-back's "still blank" list** leaves out the fields that are usually blank (the second and third beneficiary, postal address, home and work phone, children on the General form and so on). The lists are in `assets/forms.json` (`not_expected`); they only change what is listed, never what is refused. (Yes, tell me what to add or remove)
6. **A dropdown on the General form showed nothing in the render** until the chosen option was also marked selected. The program now does that for both forms, so every dropdown value draws and is checked. What stays attested is that the text is right in your own viewer. (Yes)
7. **Still to do later, one line each:** the proposal skills (`om-optimal-ra-proposal`, `om-tax-free-skill`, `rgar-skill`) must find the transaction folder by either the old or the new name; and `client-teams-transcript-skill` could call this skill's reader instead of reading applications itself. Neither is part of this upload.

## What no program can close
- That a client's value is TRUE: only that it is in a document or in your words, and that it was written and reads back.
- That the General form's field meanings are right (a table made once by hand from positions and labels; it was never proved by an insurer). The program only proves the form has not changed since.
- That the text in a box is the right text in your own viewer (the render proves something is drawn, not what).
- Which transaction folder is current, whether a form you completed live is the real record, and whether the insurer accepts the form.
- I have never seen a real filled application of a client, so the first real run may need one fix.
