# Find and register the documents

Claude finds and reads the source documents itself from the client's file on Paul's OneDrive/SharePoint: Paul does not upload them. Try the three routes in order (computer, Microsoft 365, Zapier), every try logged; if a route fails, log it and try the next. Confirming that something does not exist ("there is none") is an answer; silently skipping it is not. Do not build a partial comparison: if a required source cannot be found or read, ask Paul and wait.

**Documents by role** (ROLE for `run.py doc`)
| ROLE | What | Needed |
|---|---|---|
| `quote` (label = the provider's name, for example `Old Mutual`) | The actual quote or illustration of EACH provider, uploaded in full: not a summary email or a screenshot of one page. Each quote must show at least the premium or contribution, the yearly increase, the term or retirement age, the fund(s) selected and the FULL fee disclosure (asset management fee, administration fee, advice fee, any commission), not only a blended EAC figure. A quote that only shows EAC is refused: ask Paul for the fee schedule or fund fact sheet that shows the components. Every quote states the client's name and its own product type; both are read off the quote, not asked. If the quotes show different product types, flag it. | at least two, at most six |
| `fact_find` | The client's Fact Find (the Fact Find Transcript PDF or the Fact Find Summary): the client's name, personal email address and **risk profile**. | registered, or Paul's words that there is none |
| `supplement` (label = for example `Testco Booster Illustrator`) | A second document a provider supplies after the formal quote (a booster or growth illustrator, a projection tool, an updated benefit statement) that may use different assumptions. | optional |
| `tfsa_statement` | The client's existing TFSA statement (contributions already made this tax year and in total), for a Tax-Free comparison. | optional (or the Fact Find, or Paul's words) |
| `factsheet` (label = `<Provider> - <Fund>`) | The CURRENT fact sheet of every fund named on a quote, fetched from the web for this comparison, its text saved to a file. | one per fund, or Paul's words that it could not be found |

**The funds and their fact sheets (mandatory, every time).** For every fund actually named on a quote, search online and pull its current fact sheet before anything is entered. Name the funds with `run.py funds`; the program refuses a fund that is not in its provider's quote and then prints the exact registration command for each fund. Never estimate, recall from memory or reuse figures from a previous client's comparison: fund performance, benchmarks and target returns change every time a fact sheet is reissued (usually monthly or quarterly).
- Search for the fund's name plus "fact sheet" (for example "Old Mutual Albaraka Balanced Fund B1 fact sheet") and fetch the provider's own, or a recognised fund-data platform's (for example Morningstar or ProfileData), most recent version. Routes: the search and fetch tools first, then Claude in Chrome; log every try (`--purpose factsheet`), failures too.
- **Save the fact sheet's text to a file and register it** with `--url` (where it came from) and `--fetched-at` (the date). The program reads that text and checks every figure you enter for the fund against it. It cannot prove that the saved text is the real page: that stays attested.
- If a fund cannot be found, or the fact sheet is clearly outdated (more than one quarter old: the program flags 92 days) with no more recent version available, say so: ask Paul, then record his words with `run.py doc --missing factsheet --label "<Provider> - <Fund>" --said "..."`. The email then shows "Fact sheet not found" or the old date and says why. Never leave a blank cell and never guess a figure.
- If two funds are blended in a proposal (for example "50% Fund X + 50% Fund Y"), fetch and report each fund individually: do not average or blend the benchmark, target or performance figures yourself.
- Never quote fact sheet wording beyond a few words: paraphrase the descriptions (the program refuses a description that repeats 8 or more words in a row from the fact sheet).

**The client's email address** comes from the Fact Find; if absent: `microsoft_office_365_find_a_contact` via Zapier, then an Outlook email search for the client's own emails; ask Paul only if all of these fail. Never invent one. State where it came from.

**The client's folder** (for the saved copy): the client's folder for this product, then `Comparative Quotes`. Its name goes in the answers (`plan_folder`); if it does not exist, ask Paul.

**Show Paul a "what I found" list before building:** one line per source: the file name, its date and the folder or web address it came from, plus anything missing, conflicting or unreadable. Do not build until nothing essential is missing.
