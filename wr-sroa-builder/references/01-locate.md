# Find and register the client's documents

Servicing documents almost never arrive as chat uploads. They live in the client's folders (and the accepted quote often only in an Outlook thread). Look there first; ask Paul to upload something only when it genuinely cannot be found by any of the three routes (computer, then Microsoft 365, then Zapier; every try logged).

**Where to look**
- The **Current Policy Schedule** (the "before" figures): usually under the client's Reviews folder, in a `Policy schedules & Tax-Certificates` folder, often inside a combined "Owner's Manual" that covers ALL of the client's policies. Search on the surname, then open the actual hit: a search result is only a snippet.
- The finished SROA is delivered into the policy's own `Servicing` subfolder in the client's file (see step save).
- The **accepted Servicing Quote and the client's acceptance** are often only an email thread. Pull the exact CP (proposal) number and the signed/accepted date from it; do not leave them for Paul to dig up if they are there.

**Documents by role** (ROLE for `run.py doc`)
| ROLE | What | Needed |
|---|---|---|
| `current_ps` | The Current Policy Schedule: the policy as it stood BEFORE the change. A combined Owner's Manual is fine: register it with `--policy <this run's policy number>`; the program takes only the pages that carry that number (if the policy's own pages do not all print the number, view them and add `--pages 3-5`). | always |
| `fna_quote` | The Servicing FNA Quote document | if compiled |
| `shortfall_quote` | The Shortfall Quote document (only compiled when the client has Group Risk cover: FNA cover minus Group Risk cover) | if compiled |
| `alternative_quote` | The Alternative Quote document (only compiled when affordability holds the client below the Shortfall/FNA figures) | if compiled |
| `acceptance_email` | The client's acceptance of the quote (email or note), which shows the accepted/signed date and the CP number | always |
| `fact_find_summary` | The client's Fact Find Summary (full legal name, ID number, the needs and affordability behind the change) | always |

A file may be a PDF, or an email saved as .html or .txt. A scanned page is viewed as an image by you; the program tells you which pages have no text.

**Rules**
- One policy per run. A client with more than one policy under service gets one run each; confirm which policy number a document belongs to. Figures come from the section for THIS policy number, never assumed to apply to the client's other policies.
- Do not silently substitute the nearest thing in the folder: not an older pre-reduction quote, and not a Policy Schedule dated before the change took effect. Flag a gap and ask Paul.
- A compiled quote needs its own document: never make up a quote's figures from the accepted quote's document. If the client declined the FNA entirely there is no FNA document: that is recorded in the answers, not "missing".
- **Fact Find PDFs read through SharePoint can come back as labels only, with none of the client's answers.** That is a known failure of the text reader, not a blank document. Do not conclude it is empty and do not ask Paul to retype it: ask him to put that PDF in the chat so you can read it as page images.
