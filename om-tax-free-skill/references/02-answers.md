# The answers file (one JSON file, every answer with its source)

Write the file below and run `run.py answers`. The program refuses it (nothing saved) and says why if anything is missing or wrong. **Every figure and name you type must be in the right document's text**, copied exactly as that document shows it (the program shows rand with thousands commas, and cents only when the source figure had cents; percentages keep their own decimals: 0.733% is never 0.73%). Never take these from a previous client's proposal or from memory.

## What comes from the documents (never asked)
- **From the quote** ("DETAILS OF YOUR COMPREHENSIVE TAX FREE PLAN"): owner name and age; the regular contribution and the start date ("HOW WILL I CONTRIBUTE TO MY PLAN?"); the fund selection and allocations ("HOW MUCH WILL I PAY...", "HOW WILL MY MONEY BE INVESTED?"): ONE row per fund with its % allocation, every fund, not just the first; the fees. The four fees are usually spread over three sections: the asset management fee under "HOW MUCH WILL I PAY FOR THE MANAGEMENT OF MY INVESTMENT FUND(S)?", the advice fees under "WHAT IS PAID TO MY ADVISER?" and the administration fee under "HOW MUCH WILL I PAY FOR THE ADMINISTRATION OF MY PLAN?". Enter the four (asset management, net administration, ongoing advice, adviser remuneration account charge); **the program adds up the total**. If the quote shows an "as-and-when" advice line that is not in the total, flag it to Paul: never silently add or drop it.
- **From the Fact Find Summary:** employer, job title, gross monthly income, the client's full and first name, the email address. Ask Paul only if genuinely absent from both the Fact Find and the quote.
- **The Risk Profile** from the client's completed questionnaire (view the pages as images). If the Fact Find Summary also states one, put it in `ffs_risk_profile`: if the two differ it is a conflict and you STOP. Only when no completed questionnaire exists (or its result is unclear) ask Paul with buttons: "Cautious", "Moderate", "Moderate-Aggressive", "Aggressive", "Other, I'll type it" and record his words in `risk_paul_said`.
- **Weekdays are never typed and never trusted:** you give calendar dates (DD/MM/YYYY); the program computes every day name.

## What to ask Paul (these cannot come from the file)
1. **The start date: always ask, even though it is in the quote** (his own double-check, because the date can shift between the quote and the proposal). Buttons: "Use the start date from the Quote PDF" / "It's changed: let me give you a new date". Record his words in `start_date_choice`.
2. **The Teams meeting date(s) already held:** pre-fill from the file (the dates in the names of the `Teams meeting Transcript - DD.MM.YY` and Fact Find files in `2. Fact Find`), show them to Paul and ask him to confirm or add. Dates only.
3. **The next Teams meeting:** the date and the time (for example 17/07/2026 and 5pm). If Paul only says a day name, confirm the date.
Nothing else is asked: Cc is always Sitamah; uploads are not asked for; the risk profile, fees, contribution and fund allocation are read.

## Stops (never invented)
A plan in a **child's name**, a **lump sum** plan, a plan owner who is not the client, an owner under 18, or two sources that disagree: the program refuses and you STOP and ask Paul. There is no child or lump-sum wording yet.

## Layout
```
{
 "client_full_name": "<as in the Fact Find Summary>", "client_first_name": "<for the greeting>", "client_surname": "<surname>",
 "owner_full_name": "<owner as in the quote: must equal the client>", "owner_is_child": false, "plan_type": "monthly", "owner_age": 41,
 "employer": "<as in the Fact Find Summary>", "position": "<job title>", "gross_monthly_income": "R45 000.00",
 "contribution": "R 2 500.00", "start_date": "DD/MM/YYYY", "start_date_choice": {"choice": "quote", "paul_said": "<his words>"},
 "risk_profile": "Moderate", "risk_profile_source": "questionnaire", "risk_paul_said": "", "ffs_risk_profile": "",
 "funds": [{"name": "<fund exactly as in the quote>", "allocation": "60%"}, {"name": "...", "allocation": "40%"}],
 "fees": {"asset_management": "0.733%", "administration": "0.250%", "advice": "0.500%", "adviser_remuneration": "0.100%"},
 "fund_sheets": {"<fund name>": "fund_fact_sheet_1", "<fund name>": "fund_fact_sheet_2"},
 "client_email": "<address>", "email_source": "fact_find_summary", "email_note": "",
 "meetings_held": ["DD/MM/YYYY"], "next_meeting": {"date": "DD/MM/YYYY", "time": "5pm"},
 "plan_folder": "<the plan folder's name, for example Surname, First - (OM Tax-Free - R2500)>",
 "flags": [], "sources": {"quote": "...", "personal": "...", "risk": "...", "email": "...", "meetings": "...", "next_meeting": "...", "start_date": "..."}, "conflicts": []
}
```
- `email_source` is `fact_find_summary` (the address must then be in its text) or `other` with `email_note` saying where it came from.
- `fund_sheets` names the registered fact sheet for EVERY fund (one fact sheet for every fund in the quote). `"MISSING"` only when Paul said it does not exist (recorded with `doc --missing fund_fact_sheet --said ...`).
- `flags` holds the things Paul must hear in the final report: conflicts between Fact Find Summary versions, the Overview or the questionnaire, a blank-template file, a missing fact sheet or strategy summary, a fee-table assumption, a quote typo, a quote that expires before the start date, the saved copy having no logo.
- `sources` says where each answer came from (a document name, or Paul's words). `conflicts` must be empty.
