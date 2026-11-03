# Find and register the client's documents

Claude finds and reads the source documents itself from the client's file on Paul's OneDrive/SharePoint: Paul does not upload them. Do not build a partial email: if a source below cannot be found or read, ask Paul and wait. Confirming that something does not exist ("there is none") is an answer; silently skipping it is not. Try the three routes in order (computer, Microsoft 365, Zapier), every try logged. There is no "reachability window": if a route fails, log it and try the next.

**Documents by role** (ROLE for `run.py doc`)
| ROLE | What | Needed |
|---|---|---|
| `rgar_report` | The RGAR PDF from Alwyn, for example "[Client Full Name] - Retirement Goal Analysis - 24.06.26.pdf" or `Retirement Goal Analysis - 10.01.26 - [Initial] [Surname].pdf`. Look first in the client's `Paul/New Business/{Surname, First}/` folder: often under an "(OM RGA)" / RGA transaction folder > Comparative Quotes, or already in the RA transaction folder. The RGAR is a flat generated report with a text layer. Its REAL file name is used for the email's attachment line and the Teams message: it is never typed. If several versions are on file, use the most recent, list the others and ask Paul if there is doubt. | always |
| `fact_find_summary` | The client's Fact Find Summary (made by `fact-find-summary`), in `2. Fact Find`: `Fact Find Summary - {DD.MM.YY} - ({Name}).pdf`. Read EVERY file; register the most recent by its date as `fact_find_summary` and an older one as `fact_find_summary_older`, and flag any difference between versions to Paul. Source of: employer, job title, gross monthly income, the client's full name and first name (the greeting), the age, the personal email address (the To:) and the net monthly income target. The manual Fact Find, transcripts and older fact finds are not used. **With no Fact Find Summary the skill STOPS and asks Paul** (never read the raw fillable Fact Find by a visual route instead). | always |

**The client's email address** comes from the Fact Find Summary; if absent: `microsoft_office_365_find_a_contact` via Zapier, then an Outlook email search for the client's own emails; ask Paul only if all of these fail. Never invent one (mark it a placeholder only if genuinely unknown, and then the run cannot finish). State where it came from.

**The RA transaction folder** (for the saved copy and the RGAR copy): the client's folder under `Paul/New Business/{Surname, First}/` > the **RA transaction folder** (for example `{Surname, First} - (OM RA - R[amount])`) > **`Comparative Quotes`**. All RGARs are filed under the RA transaction folder, not under a separate RGAR folder. Its name goes in the answers (`plan_folder`).

**Show Paul a "what I found" list before building:** one line per source: the file name, its date and the folder it came from, plus anything missing, conflicting or unreadable. Do not build until nothing essential is missing.
