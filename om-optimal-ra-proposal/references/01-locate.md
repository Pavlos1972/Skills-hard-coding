# Find and register the client's documents

Claude finds and reads the source documents itself from the client's file on Paul's OneDrive/SharePoint (`Paul` site > `New Business` > `{Surname}, {FirstName}`): Paul does not upload them. Try the three routes in order (computer, Microsoft 365, Zapier), every try logged; if a route fails, log it and try the next. Confirming that something does not exist ("there is none") is an answer; silently skipping it is not. Do not build a partial email: if a required source cannot be found or read, ask Paul and wait.

**Documents by role** (ROLE for `run.py doc`)
| ROLE | What | Needed |
|---|---|---|
| `quote` | Alwyn's **OM Optimal RA Quote** (Plan 1), usually in the RA transaction folder > Comparative Quotes. New quotes are titled "Old Mutual Savings and Income - Optimal Retirement Annuity Plan Quote Report". Its REAL file name goes into the Teams message. Source of the premium, start date, funds, allocations and every fee. If several versions are on file, use the most recent, list the others and ask Paul if there is doubt. | main: always |
| `fact_find_summary` | The client's Fact Find Summary (`fact-find-summary`), in `2. Fact Find`: personal details, age, employer, position, start date, gross income, retirement goal, risk profile, the personal email address. Register the most recent. **With no Fact Find Summary the skill STOPS and asks Paul.** | always |
| `booster_doc` | The **Optimal Illustrator / RA Booster Value** document (attachment 3), in the same Comparative Quotes folder. Its REAL file name goes into the Teams message. | main: always |
| `astute_ccp` | The **Astute CCP report** or the existing policy schedules: each existing RA's insurer, policy number, monthly contribution, gross fund value and date. | optional: registered, or Paul's words (for example "the client has no retirement annuities") |
| `client_overview` | The **Client Overview** showing "Current Investments": gross fund value, penalties, net fund value and monthly premium of each existing policy at a glance. Needed for a Section 14 lump sum (the NET fund values). | optional (as above) |
| `fund_statement` | The **Pension / Provident Fund statement**: fund type, employer and member contributions (rand and %), fund value and date. | optional: registered, or Paul's words ("no pension or provident fund"); REQUIRED when the client has a fund |
| `poi` | **Proof of income / payslip** (the gross monthly income, the fund contributions). Often scanned: view image pages yourself. | optional (as above) |
| `rgar` | The **RGAR PDF from Alwyn** (the SECOND shortfall table, "WHAT YOU HAVE AGREED TO DO AND WHY", is the one used). Often filed in the RA transaction folder. | optional: registered, or Paul's words ("no RGAR was requested") |
| `lump_sum_quote` | The separate **OM Lump Sum Quote (Plan 2)** from Alwyn. | lump sum run: always |

For the lump sum run (`--document lump_sum`) the required documents are `lump_sum_quote` and `fact_find_summary`; `astute_ccp` and `client_overview` are optional (needed for a Section 14 transfer).

**The client's email address** comes from the Fact Find Summary; if absent: `microsoft_office_365_find_a_contact` via Zapier, then an Outlook email search for the client's own emails; ask Paul only if all of these fail. Never invent one. State where it came from.

**The RA transaction folder** (for the saved copy): the client's folder under `New Business/{Surname, First}/` > the RA transaction folder (for example `{Surname, First} - (OM RA - R{premium})`) > `Comparative Quotes`. If that path does not exist, create the folders under the client's existing W-Files client folder and tell Paul. Its name goes in the answers (`plan_folder`).

**Show Paul a "what I found" list before building:** one line per source: the file name, its date and the folder it came from, plus anything missing, conflicting or unreadable. Do not build until nothing essential is missing. Remember to tell Paul about any discrepancy between the quote and the booster document, and a quote that expires before the start date.
