# What changed in the Fact Find Transcript skill, in plain words

For Paul. **Not uploaded, not live.** This is the program-driven version of `ff-population-transcript` (your decision 20, 02/11/2026). Your older version stays in the skill's version history in claude.ai (that is the backup).

## Fix round 1 (an outside reader attacked the first build)
A second reader tried to get a wrong or empty Fact Find through the checker, and found real holes. Those were closed in round 1, each with a test that must refuse; a second reader then found more (see Fix round 2 below). The big three: (1) a request or next step on the call could be "covered" by pointing at the lead search, so it never reached the PDF; (2) "Not discussed" was written after a search nobody could pass (only the field's label), so a call that said "ask BrightRock for an FNA quote" printed "FNA quote: Not discussed"; (3) an overlay entry with a wrong section or list name vanished without a word. The rest: the Teams hand-over is now proven against the Teams program's own records, a made-up Overview or Paul's words can no longer be typed in, the form's saved PDF is matched by exact amounts and whole words, the save folder must be the client's own, a run folder, form, PDF or transcript of another client or date is refused, and a change to the programs during a run is detected (unless someone also changes the checker). Details are in the lists below.

## Fix round 2 (a second reader attacked the program again)
The second reader said most of round 1 held. One big hole and several smaller ones were left. I closed the ones it named, each with a test that must refuse; a third reader then found more routes to the same hole (see Fix round 3 below). In plain words:

**The big hole**
- Claude could file the call's "ask BrightRock for an FNA quote" as a plain "fact", set it aside, and give every flagged field a nonsense reason such as "xxxxxxxxxxxxxxxxxxxx". The run still passed, and the PDF said "FNA quote: Not discussed".
- Now a line with a request, decision, change or quote word cannot be filed as a plain fact, and cannot be set aside as plain talk.
- Such a line must be next to a real entry, or dismissed with a reason that quotes some of the line's own words.
- Every line dismissed by a review is named on your glance list, with its line number and the reason (round 3 adds how every request line was handled).
- A "Not discussed" that goes against what the search found needs a reason that names a found line by number and quotes a word from it.
- The program refuses a reason that is one repeated character, or has fewer than three different words.
- The printout counts how many "Not discussed" went against the search and how many rest on a weak search.

**Smaller holes**
- A cover must be about the same thing: a fill "sti_car = No" can no longer cover "credit life with Absa", and a note "Noted" can no longer cover "letter of authority".
- Claude could answer its own question to you. Now a question says what it is about, and your answer can be used only for that. A number Claude uses must be in your words.
- "Not a joint meeting" is refused when the form's spouse, or anyone else, speaks on the call, unless Claude gives a reason that is shown to you.
- The Teams skill folder is named by Claude, so a fake folder could say PASS. Now the program checks it looks like the real one (its steps, its size, its marks). It prints a fingerprint of the Teams checker, driver and steps for you to compare. The Teams run must also have been made from this run's transcript.
- The save folder: the path must start (after the drive and liferisk.co.za) with Company - Paul or Company - WR Clients\Paul Kafentzis (Client Files). A different spelling of the client's folder needs a real sentence that names the surname, and it is shown to you.
- Dismissing the call: three reviews of 40 lines, or one entry with every other line dismissed one by one, no longer get through. More than a quarter of the call, or more than 60% of the request lines, dismissed stops the step unless you say to go on.
- A note with "policy AB1234" (a short code, no "number" word) must now be in a recorded schedule.
- If the form's saved PDF does not match and the program stops, there is now a way on: Claude asks you, records your words, and the data file alone is used. This is shown to you.
- The search words had gaps ("will updated" was missing for "Will last updated"). I added 497 words across 155 fields: plurals, stems ("diabet*"), South African wording, the lender and insurer names, "creditor life", "short term", "medical scheme", and similar. The list of what was added is in the summary at the end of this file. The search now also finds plurals by itself.
- The printout's wording is more careful. It says the kind of each ledger entry is chosen by Claude, that the Teams folder and the document text copies are made by Claude, and exactly what the save-folder check covers.

**Two contacts I looked at (reader's question)**
- `references/04-contact-and-lead.md` names the sender of the D&R Marketing lead emails (Di Heath, with a mweb.co.za address). It is a business contact your old skill used to recognise the lead emails. It is not client data. I left it. **Is it right to keep a named person's own address in the skill? Keep / Remove.**
- `history/SKILL.2026-10-28.redacted.md` line 295 holds the Teams chat id of your chat with Sitamah (used for the Zapier send). It is the skill's own operating detail, not client data, and the live Teams skill carries it too. I left it. It is in `history/`, which is not in the zip.

## Fix round 3 (a third reader went after the same hole)
The third reader said the FNA request could still be dropped, in two cheap ways. Both are closed now, with the smaller ones. In plain words:

**The two cheap ways**
- Claude could file the FNA line under the wrong kind (a "gap"), then "cover" it with an unrelated fill that shared one word with a field's label.
- Now a line with FNA, quote, shortfall, RGAR, EGAR, goal analysis or reduced must be filed as a quote request. The program refuses any other kind.
- A fill covers an entry only if the field's own search words are found in the entry's line, or the fill's own value or text shares a word with the entry. The field's label no longer counts.
- Claude could also "cover" a gap or a contact with a "Not discussed" claim. A claim that the call did NOT discuss something cannot cover something the call DID say. Claims no longer cover gaps or contacts at all. (A client who says "I don't have a work number" is recorded as a plain fact.)

**Request lines**
- A request line used to count as handled if ANY entry was within 3 lines. Now that entry must also share a word with the line (a line like "OK, please do that" with no real word is handled by any entry next to it).
- Lines with FNA, quote, shortfall, RGAR, EGAR, goal analysis, reduced, authority, payslip, appointment, next meeting, set up or follow up cannot be dismissed by a review at all. They must be an entry.
- If such a line really is not a request (for example "as the quote said last year"), Claude must ask you. Your recorded answer names the line. The line is then shown on your glance list as dismissed on your answer.
- Softer words can still be dismissed with a reason that quotes the line: ask, request, sign, send, email, and the new ones (can you, could you, would you, please, I'd like, I will need, organise, arrange, book, prepare, run the numbers, come back to me, get back to me, send me, email me, let me know).
- A fact is refused when a request word is on the line or one or two lines next to it, not only on the line itself.
- The glance list now shows how EVERY request line was handled, for example "line 66 -> entry L5 (quote_request, covered by fna_req)" or "line 81 dismissed: <reason>". It shows 15, then the count.

**Your answers**
- A question could name all 223 fields, and then your one answer could fill a tax number and change an ABI. Now a question about a field names at most 10 ids, and each one must be written in the question text (as its id or its label).
- This was true for questions about fields. It was NOT yet true for the question that frees a request line (the "dismissals" question). Round 4 below closes that.

## Fix round 4 (the confirmation pass found three more routes)
The fourth reader said every round-3 attack was closed. Three fresh ones still got through. All three are closed now. In plain words:

**The wrong product's quote row**
- The FNA line could be "covered" by a quote row for the SHORTFALL product, because both rows have the word "quote" in their label.
- Now a quote request is covered only by the row or request field of the product its own line names: FNA, shortfall, reduced quote, RGAR or EGAR.
- The program refuses any other product, and its message names both.
- "Not discussed" on a product's request, type or insurer field is refused while the ledger records a quote request for that product.
- A second (bf) FNA quote is a different thing: it is not blocked by the main FNA request.

**Your answer to a question about a request line**
- A question like "Is this fine?" with your answer "yes" could free a request line, and a wide range could free hundreds of lines.
- Now the question must quote at least 4 words (4 letters or more) of EVERY line it names. The program checks that against the call. A line with fewer such words must be quoted in full.
- One answer can free at most 5 lines in all. A wider range frees nothing.
- The glance list shows, next to each freed line, the full question the chat recorded and your recorded words.
- The checker fails, and says so, when a recorded answer does not meet these rules.

**A request line next to an unrelated entry**
- A line like "Can you also send me what BrightRock says about the cover?" counted as handled by an entry that shared only the word "send".
- Now the shared word must be a topic word. A request verb or filler (send, email, ask, sign, need, please, would, could, your, with, that, this, have, will, also, what, says, about and a few more) does not count.
- Otherwise the line needs its own entry, or a review that quotes it.

**The glance list**
- It now shows the TEXT of every request line (cut at 60 characters) with how it was handled.
- With 40 request lines or fewer it shows all of them. With more, it shows every line that is not directly on an entry, plus every line of the closing minutes, and counts the rest.

**Still true (I cannot close these with a program)**
- Claude types your words itself with `run.py answer`, so "Paul said yes" is attested.
- A doctored copy of the Teams skill, or a self-patched fingerprint, needs an outside anchor (for example the released fingerprint in the upload brief).
- The text copies of an Overview or schedule are made by Claude.
- A written reason is checked for form, never for truth.
- A request worded with none of the listed words is not required by the program.

## What the skill does now
After a Fact Find meeting it builds the **Fact Find Transcript PDF** from, in this order: the form's data file (and the form's own saved PDF), the Teams transcript, the latest Overview, and the client's other documents. A program does the work step by step; Claude cannot skip a step, and at the end the checker prints PASS or FAIL for every item. The PDF has your fixed 11 sections in your order, then "Next Steps & Next Meeting". The Fact Find Summary, the Planner note and the message to Sitamah are still made by the other two skills (once, not twice).

## What a program now does that Claude used to do by hand
- **Reads the form's data file** (it finds the right file by what is inside it, not by its name). It stops with one line for you if the form's version is not 3.0. It ignores the form's own summaries, its drafted action list, its parking list and its cost counters, never prints them, and uses the saved value of every field.
- **Reads the form's saved PDF too** and checks that every value of the data file is in it; a value it cannot find is looked at, and a real disagreement is shown with both values.
- **Throws out the company look-up text** when it talks to the reader (for example "try again", "I found no..."), asks a question, or is more than about 40 words, and uses what the client said on the call instead (or "Not stated"). A clean look-up that nobody confirmed is marked "web look-up, not confirmed with the client", and you are told the form should say "to verify".
- **Works out** date of birth and gender from the ID number (and warns if the ID's check digit is wrong), "number of years" when the form holds a year ("11 years (since 2015)"), and every total from its parts, to the cent. **Debt is never left out**, whatever credit life says: if the form's own risk-calculation figure leaves a debt out, the PDF shows both figures and says so.
- **Writes the standing values itself**: Life cover (WOL) ABI 3% and Childcare ABI 5%; under Permanent disability fractured, no Life Cover (WOL) line but Household needs ABI 5% (the form has no line for it, so the program adds it and says so) and Childcare ABI 5%; Dread Disease ABI 3% always (both places in the form), Dread Disease cover R 500 000.00 unless the form deliberately says otherwise. A different value in the form is overwritten and mentioned in one line. A "?" in an ACI field shows "Pending – FNA".
- **Refuses "Not discussed" until it has searched** the call, the documents and the form's own related fields. Every field has its own written list of search words (in `scripts/layout.json`), so the search is never just the field's label. A field the search finds something for is never called "Not discussed" without a reason written for that field. A field that only has its label to search for is called a **weak search**: it is never accepted on its own and is put on your glance list. The checker repeats every search. A debt detail can be "Requested" only after the form, the call, the Overview, other documents and a recorded Outlook search (`run.py lead`) were checked.
- **Compares every populated form field with the call** (same / differs / not on the call). The program itself searches the call for each field and writes "not on the call" only where it finds nothing; every field it does find in the call is left for Claude to answer with the exact words. A difference is printed with both values and the line of the call.
- **Checks that everything the call adds is really in the document.** Every gap, difference, contact detail, quote request, next step and request on the call is a ledger entry, and each must be covered by the right kind of item that cites the same part of the call (within 8 lines): a quote request only by a quote row or an answered request field, a gap only by a fill or a search-backed "Not discussed", and so on. The lead search and a "Not discussed" can no longer be used to tick off a request or a next step.
- **Every entry in the overlay must land.** The program lists the valid section, list, group and field names and refuses a name that does not exist (a note in a section that does not exist used to disappear without a word); a valid entry that still ends up nowhere in the document fails the checker.
- **Paul's own words are recorded only by the program** (`run.py ask`, then `run.py answer`). The overlay can only point at them; words typed into the overlay are refused. An ABI you changed is always put on your glance list with your recorded words.
- **A document is accepted only with a text copy that can be checked.** An Overview or a Policy schedule needs a text copy that mentions the client's surname or ID number. The copy is made by Claude, so the program checks that it names the client and that quotes and figures are in it, not that it is the real document; Claude says so and the printout shows a fingerprint of each copy. Any number of six or more digits printed in the document must be in a recorded schedule or Overview; the insurer and New Business / Servicing of a quote request must be in a source that the entry cites.
- **The Teams hand-over is checked, not just written down.** The program runs the Teams program's own checker on the Teams run, and fails unless every Teams step before its message step is done, its Planner page and message exist, and the follow-up appointment is carried as an action for Sitamah.
- **A change to the programs during a run is detected.** A fingerprint of the programs, the layout, the steps and the rule pages is taken at the start and compared at every step and at the end. It is NOT proof: someone who also changes the checker could hide it. So the fingerprint is printed in the last line for you to compare with the released one.
- **Refuses a quote request without an insurer and New Business or Servicing**, and never lets "Servicing" appear unless the form, the call or you said it. It then tells Claude to ask you.
- **Takes policy numbers only from a policy schedule.**
- **Fills the business parts only when Business owner = Yes** (otherwise nothing is printed there and the glance list says so).
- **A populated form field the layout has no place for** is printed in a closing block, "Other fields from the form", and put on your glance list. Nothing is dropped silently.
- **Two spouses in one meeting:** one run per spouse; only the common debts, children and joint policies are shared; a program searches each document for the other spouse's ID, phone numbers, emails and policy numbers and fails if it finds any.
- **Draws the PDF** (reportlab) from one data file: the same look every time, no page numbers, no forced page breaks, a heading kept with its table, a row never split across pages, one fact per line. The checker rebuilds the PDF from the data and fails if the file is not identical, or if there is a page number, a stranded heading, a split row or a Word file next to it.
- **Names the font really used.** See question 3 below.
- **Proves the save**: the folder listing's size must equal the local file's size (the program compares the two numbers), and the folder must be this client's own `2. Fact Find` folder under Company - Paul or Company - WR Clients\Paul Kafentzis (Client Files) (never another client's or another broker's).
- **Stops on the wrong paperwork.** A form or saved PDF of another client or date, a transcript dated another day, a run folder that already belongs to another client, and a saved PDF with more than a quarter of the values missing all stop the job with one line.
- **One question about the spouse.** Before the content step the chat must answer "is this a joint meeting with a spouse?" (`run.py joint`); a joint meeting means one run per spouse, and every statement taken from the call needs a line saying why it belongs to this spouse.

## When the form's file is missing
The program tries the computer, Microsoft 365 and Zapier (every try logged, whatever the time of day: the 8:45am laptop note is gone), then STOPS and asks you: "use the filled-in Manual Fact Find PDF, or work from the transcript alone?". It carries on only after your own words are recorded, and the final printout says which you chose.

## What stayed the same
Every rule of the old skill is still there. A program (`tools/inventory.py`) went through all 568 sentences of the original: **391 are still there word for word, 68 are reworded (each with a written reason), 109 were dropped on purpose (each with a written reason) and none was lost without a record.** On your 02/11/2026 text (550 sentences) it found 455 kept, 61 reworded and 34 dropped, also with none unaccounted. The short true stories in the rules stay, with names removed. The skill's name and description are as before. The records are in `history/changes.json` and `history/decisions.json`; the full list is in `history/INVENTORY-REPORT.md`.

## Your yes/no list (anything I was not sure about)
1. **The old Step 6 pause.** The old text said: show the first draft, and do not go on to the Summary until you confirm the Fact Find. The new job shows the PDF, the Summary hand-over, the Planner note page and the message to Sitamah together in one reply with ONE question ("Shall I post this message to Sitamah in Teams?"), and any correction re-opens everything. I reworded the sentence that way. **Keep it this way? Yes / No.**
2. **Look.** The old script's real sizes were 9.5 to 10 pt for table text and 13 pt for headings, although the written rule says Aptos 12 pt throughout. I used **12 pt everywhere** (headings 14 pt, title 18 pt) as written. A4 paper (the old script used Letter). A value with one fact is plain text, two or more facts are bullets. **OK? Yes / No.** (If you want smaller text, it is one number in `scripts/layout.json`.)
3. **Aptos.** Aptos is not installed where I built this, so the sample PDF is set in **Carlito** (a look-alike) and the checker says so on every run; it will use Aptos by itself wherever Aptos is installed. I never saw Aptos itself. **Is a substitute acceptable when Aptos is missing in your chat? Yes / No.**
4. **The field labels are my own.** The form's label file could not be read, so I wrote every label in `scripts/layout.json` from the form's field names. The least certain: the `bf_` quote fields ("FNA quote (bf): requested"), the `pr_...` pairs (I called them "priority" and "comment"), `profile` ("Client profile"), the duties split names (desk work, supervising from an office, travelling, supervising on site, light, moderate and heavy manual), `lc_hh / lc_cc / lc_dr / lc_need` in the risk calculation, and the three referral lines (Cameron, Valerie, Capital Legacy, taken from the old text). The final printout reminds you to check them until you say they are right. **Please check one sample PDF.**
5. **Three risk-calculation checks are my reading, not yours.** The program flags (never changes) a difference when: childcare in the risk calculation is not the total of the children's monthly costs; debt repayments are not the total of all the debts' monthly instalments; and total household income needed is not take-home income minus childcare minus debt repayments (your old spouse rule). It says on the glance list that these are my reading. **Are those the right meanings? Yes / No.**
6. **Empty fields.** An empty field whose search of the call finds nothing prints "Not discussed". Some empty fields are left out of the table instead (comments, "other" lines, the provider pick-lists and notes columns). Fields that cannot apply print "N/A" (for example the medical aid provider when medical aid is "No", the spouse lines for a single person). **OK? Yes / No.**
7. **Short means short.** Anything Claude writes (notes, differences, fills) is one fact per line, at most 25 words, at most 6 notes per section. Text copied from the form is never rewritten, even if it is longer: the checker only warns. **OK? Yes / No.**
8. **Date check.** The form's "Date completed" must equal the meeting date in your message, otherwise the program asks you which is right. **OK? Yes / No.**
9. **Overview.** The latest Overview is required: read it, or record that none exists after two routes were tried. **OK? Yes / No.**
10. **Rules that are only text or only a warning (nothing stops a run if they are broken).** I listed every one so that nothing is claimed as checked when it is not. **OK to leave them like this? Yes / No.**
    - *Only text, no check at all:* correcting a source document on file when a policy number conflicts (for example the Overview spreadsheet); the "Out of scope" rule (a completed Fact Find with no transcript goes straight to `fact-find-summary`); "pending items stay pending"; "a prior-year figure is never shown as current"; "a garbled line is flagged, not turned into a fact"; "compare the Overview and the client's other documents"; the visual look at the page images; the independent re-check by a second reader; that the Planner page was really published and you said yes to the message.
    - *Only a warning (the run can still pass):* a transcript that states no meeting date; a gap between joined transcripts; reading forced past a completeness warning; no ledger entry from the closing minutes; a form text longer than 25 words (never rewritten); a flag longer than 45 words; a PDF of more than 16 pages; the font being a substitute for Aptos (or plain Helvetica); a Yes/No value or a one-character value of the form, which is never compared with the form's saved PDF (known limit: the PDF could show the opposite and nobody would be told); the skill being updated while a run is going; a document read without a text copy (only possible for kinds other than the Overview and a Policy schedule); two requests worded as one waiting on the other.
11. **Decided for now, tell me if wrong.** (a) A text copy of the Overview and of any Policy schedule is REQUIRED, otherwise the checker fails the run (before, the program only warned). (b) A different ABI is accepted only if your own words are recorded through the program, and it is always on your glance list. (c) The checker counts how much of the call was dismissed as "plain talk" in the keyword scan: one dismissal covers at most 40 lines, each needs its own reason, and more than a quarter of the call dismissed is put in front of you. (d) A "Not discussed" that rests on a weak search is always on your glance list. **OK? Yes / No.**
12. **The "Not discussed" tick-box rows.** About 30 empty tick-box and detail rows in sections 10 and 11 print "Not discussed" (for example the provider pick-lists and the detail rows under a "No"). I left them as they are. The sample PDF shows them. **Keep them printing, or hide them? Keep / Hide.**
13. **Two small header sizes.** The title block at the top of page 1 has a brand line at 11 pt and a tag line at 8 pt, smaller than the 12 pt body, because that is how the old script drew it. **Make them 12 pt like everything else? Yes / No.**

14. **Request words.** The checker now treats these words as marking a request line, besides the scan's own list. HARD (cannot be dismissed; must be an entry, or you must say it is not a request): FNA, quote, shortfall, RGAR, EGAR, goal analysis, reduced, authority, payslip, appointment, next meeting, set up, follow up. SOFT (can be dismissed with a reason that quotes the line): ask, request, sign, can you, could you, would you, please, I'd like, I will need, organise, arrange, book, prepare, run the numbers, come back to me, get back to me, send me, email me, let me know. Each such line must be next to an entry that shares a word with it or be dismissed with a reason. That means a few more lines to record on a real call. **OK? Yes / No.**
15. **The 25% / 60% limits.** If more than 25% of the call's lines, or more than 60% of its request lines, are dismissed, the step stops unless you say to go on. **Are those the right limits? Yes / No.**
16. **Freeing a request line.** One answer of yours can free at most 5 lines, and the question must quote at least 4 words of each. Is that the right size? Yes / No.

## What I could not do or check
- **I have not seen the form's label file, its saved PDF, or a finished PDF from the new form.** The tests use an invented form with the real field names, and a PDF I generated from it. The real first run is the real test.
- **No real client file, real transcript or real Overview was used.**
- **I could not run it inside your chat.** The access routes (computer, Microsoft 365, Zapier), the folder save, the page tool, the Agent tool and the other two skills are only attested in the checker, not proven.
- **Several transcripts for one meeting** are joined and each part checked, but I have only seen the layouts the Teams skill already reads.
- **Claude still chooses the kind of each ledger entry** (a request, a gap, a next step ...). The program cannot tell if a request was filed under the right kind. It makes every request line be next to an entry or dismissed with a reason that quotes it, and a cover must share a word with the entry. That is strict, but it is not understanding.
- **Inherent limits (a program cannot close them; the printout says so):** (1) Claude types your words itself with `run.py answer`, so "Paul said yes" is attested. (2) A doctored copy of the Teams skill, or someone who also patches the program's own fingerprint, needs an outside anchor, for example the released fingerprint printed in the upload brief. That is a change to the packaging tool, not to this skill; I have not made it. (3) The text copies of an Overview or schedule are made by Claude. (4) A written reason is checked for form, never for truth. (5) A request worded with none of the listed words is not required by the program.
- **A "Not discussed" reason is checked only for form**: length, three different words, a named found line and a word from it. The program cannot tell whether the reason is true. Every override is counted and named on your glance list for that reason.
- **The Teams skill folder and the text copies of documents are made or named by Claude.** The program checks they look real (and prints fingerprints), not that they are the real ones.
- **The Teams skill has no program fingerprint of its own.** Its programs can be edited during one of its runs without its checker noticing (this skill now guards its own programs). I did not touch the Teams skill: this is **to fix in the next Teams change**.
- **The follow-up appointment in the Teams hand-over** is checked from the Teams program's own records. That the page was published in a window you could see and that you said yes are things only Claude can attest.
- The 13-ingredient scorecard is in the report that came with this change.

## Search words added in round 2 (every field's new words; the plural of a word is found automatically)

- age: how old, turning
- bf_fna_req: fna quote, needs analysis quote
- bf_sf_req: shortfall quote, group risk quote
- bfred.req: reduced
- biz_assur: shareholder protection
- biz_loans: business debt, company loan
- biz_name: registered name
- biz_partners: co director, shareholders
- biz_pct: per cent of the business
- biz_struct: ltd, limited, company
- bizowner: my company, director, self employed
- bs_req: shareholder protection
- cell: cell, mobile, reach you on, call you on, whatsapp number
- cl_bal: creditor life, outstanding balance
- cl_lender: creditor life
- cl_life: creditor life, life cover on the
- cl_req: creditor life, life cover on the, insured on the bond, bond cover
- co_does: what do they do, what the company, your company
- consent: recorded, transcribed, okay to record, fine to record
- d_desc: your job involves, tell me about work, role involves, describe your
- d_desk: behind a desk, office work, sitting
- d_heavy: heavy duties, physical work
- d_light: light duties
- d_supo: managing
- d_sups: site manager, on the floor
- d_trav: driving, visits, client sites
- date: date of today
- dd_cover: stroke, severe illness
- dds_cover: stroke, severe illness
- debts.asset: market value, value of the house, value of the car
- debts.bal: owing, settlement
- debts.cl: creditor life, life cover on the, insured on the bond, bond cover
- debts.desc: house, flat, motor
- debts.inst: repayments, monthly payment, debit order
- debts.owner: bond is in, whose name
- debts.payer: pays the bond, paying the
- debts.prov: firstrand, investec, discovery bank, tyme, african bank, mfc, toyota finance, vw financial, bmw finance
- debts.surety: suretyship, guarantor, co signed, signed surety
- debts.term: years remaining, paid off
- debts.type: home loan, mortgage, car finance, personal loan, student loan, store account
- disp: left each month, surplus
- dnet: nett, take home pay
- dob: birth date, when were you born, how old
- edu: qualifications, studied, university, college, honours, masters, certificate, highest education
- edu_notes: major, certificate, honours, masters
- egar_req: education goal analysis, education analysis, education fund for the children
- employed: employed, unemployed, retired, permanent, part time
- employer: company i work, works for, employed at
- exp: living costs, monthly spend, you spend
- fna_ins: bright rock, outsurance, clientele, assupol, metropolitan, generali
- fna_req: fna quote, needs analysis quote
- fname: name is, spell your
- ft: part time, freelance, temporary, on contract
- gap: gap policy
- gap_prov: gap policy
- gender: male, female
- gross: before tax, salary, package, you earn
- h_bmi: weight, obese
- h_bp: high blood
- h_dia: diabetes, diabetic
- h_gen: no conditions, any conditions, health issues, medical history
- h_oth: condition, conditions, doctor, hospital, chronic, operations
- has_debts: mortgage, car finance, credit card, you owe, debts
- has_group: work benefits, death benefit, funeral benefit, company scheme
- has_inv: unit trusts, tfsa, investment, shares, etf, money market, offshore, savings
- has_kids: daughters, sons, baby, toddler, boy, girl
- has_pp: pension, provident, umbrella fund, preservation fund
- has_ra: retirement annuities, ra with, annuity
- has_risk: life insurance, dread disease, critical illness, income protection, assurance, policy
- home: landline number
- idno: identity, id document, south african id
- idtype: identity, id book, id document, south african id
- inv.prem: contributions, monthly, debit order
- inv.prov: investment, tfsa, etf, money market
- inv.type: unit trusts, tfsa, investment, shares, etf, money market, offshore
- inv.val: fund value, balance
- ip_age: until retirement, to age
- ip_amt: disability income, monthly amount
- ip_wait: wait for
- ips_age: until retirement, to age
- ips_amt: disability income, monthly amount
- ips_wait: wait for
- kids.age: how old
- kids.cost: extra murals, tuition, fees
- kids.dob: born in
- kids.name: daughters, sons
- kids.stage: primary school, grade r, preschool, pre school, nursery, matric, tertiary, varsity
- lc_dr: debt repayment
- lc_need: total needed
- lc_sa: lump sum
- lc_term: until retirement, to age
- lc_termv: until retirement, to age
- loa: authority, authorise, authorize, letter of appointment
- ma: medical scheme, momentum health, fedhealth, bestmed, medshield, profmed, medihelp
- ma_broker: broker for the medical aid, medical aid consultant
- ma_plan: hospital plan, network plan, medical aid savings, comprehensive
- ma_prov: medical scheme, momentum health, fedhealth, bestmed, medshield, profmed, medihelp
- marital: engaged, life partner, separated, widower, spouse
- marr_date: marriage, anniversary, married since
- meet: zoom, phone call, in person
- nat: south african, permanent resident, foreign
- net: nett, in the bank, after deductions
- next_appt: follow-up, see you, next week, come back to you, diary
- next_day: sunday, tomorrow, next week, weekend
- next_time: pm, p m, at one, at two, at three, at four, at five, at six, at seven, at eight, at nine, at ten, at eleven, at twelve
- occ: profession, what is your job, your job
- pd_sa: disability cover
- pemail: email, e mail, outlook, dot co dot za, dot com
- pr_egar: education goal analysis, education analysis, education fund
- pr_inv: unit trusts, investments, savings
- pr_life: life insurance, funeral cover, premium
- pr_med: medical scheme, gap policy
- pr_ra: retirement annuities, ra priority
- pr_rgar: retirement goal analysis
- pr_st: short term insurance, vehicle insurance
- pr_will: update the will, new will, draw up a will, wills
- pref_spend: budget for cover, spend on cover, per month on cover
- ps_risk: bright rock, hollard, outsurance, clientele, assupol, metropolitan, generali, pps, cardinal, absa life, fnb life, discovery
- ref: referred, recommended, heard about, a friend, colleague, advert, facebook, d r marketing, marketing
- ret_age: retire, retiring
- ret_net: net a month, a month net, income at retirement, live on at retirement
- ret_pp.contrib: contributions, monthly
- ret_pp.prov: pension, provident, umbrella fund
- ret_pp.type: pension, provident, umbrella fund, preservation fund
- ret_pp.val: fund value, balance
- ret_ra.contrib: contributions, monthly, debit order
- ret_ra.prov: annuity, ra with
- ret_ra.status: paid-up, stopped
- ret_ra.val: fund value, balance
- rgar_req: retirement analysis
- risk.prov: bright rock, hollard, outsurance, discovery, momentum, sanlam, old mutual, liberty
- risk.spend: premiums, monthly, costs me
- sf_req: shortfall quote, group risk quote
- smoker: smokes, vape, vaping, tobacco, cigarettes
- sname: name is
- sp_name: wife, husband
- sp_occ: she works, he works, wife is a, husband is a
- sp_tel: wife's cell, husband's cell, her number, his number, spouse number
- sti: short term, insurance on, all risk, buildings, vehicle cover, comprehensive
- sti_biz: commercial insurance, business assets
- sti_biz_spend: commercial insurance
- sti_broker: cameron, short term broker
- sti_car: insure the car, vehicle cover, comprehensive
- sti_house: contents, household
- sti_personal: jewelry, laptop, cellphone insurance
- sti_struct: buildings, structure
- tax: tax reference, tax ref
- wemail: work address, company email
- will: wills, last will, will and testament, executor, estate
- will_broker: capital legacy
- will_date: updated, last updated, not updated, been updated, drawn up, signed, last time, when was your will
- will_up: up to date, updated, outdated, out of date, not been updated, needs updating, update the will, not updated
- will_where: lawyer, safe, kept, held by, executor
- work: office phone, direct line
- years: years with, been there, been working, since 20
