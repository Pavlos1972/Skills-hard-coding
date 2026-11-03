# The answers file (one JSON file, every answer with its source)

Write the file below and run `run.py answers`. The program refuses it (nothing saved) and says why if anything is missing or wrong. **Every figure and name you type must be in the right document's text**, copied exactly as that document shows it (the program shows rand with thousands commas, and cents only when the source figure had cents, for example "R 1,234,567" unless the RGAR itself shows cents). Never round or approximate, and never take a figure from a previous client's covering email.

## What comes from the RGAR (never asked)
- **Date of birth and Retirement Age** (page 1, "YOUR GOAL"). The date of birth does not set the age in the email: the program works out the client's age from it at the build date and compares it with the age in the Fact Find Summary. **A difference stops the run and you ask Paul which is right.**
- **Years until retirement** (page 1, "YOUR GOAL" table): a whole number, used for the shortfall period.
- **Expected monthly expenses in retirement: Current value** (the "gross" figure quoted in the email) and **Future value** (page 1).
- From **"WHAT YOU HAVE AGREED TO DO AND WHY"** (page 2): the once-off lump sum contribution required, the monthly recurring contribution required, the debit order escalation % and the sustainability age ("your income is projected to be sustainable until you are [X] years old"). These four values are recreated as formatted text in the email: never pasted in as an image, never reworded; the template's sentences are used with the client's figures.
- **The recurring investment** the RGAR assumes: enter it too. If it is R 0, or the RGAR otherwise does not seem to include the recurring contribution/RA being proposed, **the program raises a flag for Paul** (the sustainability age and shortfall may then not reflect the proposed product).
- **A lump sum or a monthly contribution of R 0:** the template prints both lines and there is no wording for R 0: the program STOPS and you ask Paul what to write. Never invent it.

## What comes from the Fact Find Summary (never asked)
- Employer, job title, gross monthly income, the client's full and first name, the age and the email address (sections "1. Client Profile" and "2. Occupation & Income").
- **The net monthly income target in today's terms:** the line labelled **"Net amount needed at retirement"** (the new Fact Find) or **"Net Amount Needed (today's terms)"** (the old wording), in "7. What the Client Requires" > "Personal Risk Cover & Retirement". The program requires the figure you type to be the FIRST figure after that label, so the Reduced Quote's monthly *contribution* target in the same table (a savings contribution, not an income need) can never be taken by mistake. If neither label is there, the program stops and you ask Paul: never derive it from the gross expense figure by assuming a tax rate, never leave it blank silently.
- Ask Paul only if something is genuinely absent from the Fact Find Summary.

## What to ask Paul (these cannot come from the file)
1. **The meeting date(s) already held** with the client: pre-fill from the file (the dates in the names of the transcript and Fact Find files in `2. Fact Find`), show them to Paul and ask him to confirm or add. Dates only (DD/MM/YYYY): never ask for the day of the week and never trust one a person types; the program computes every weekday (a hand-typed email once labelled 19/02/2022 a "Thursday" when it was a Saturday).
2. **The next Teams meeting date and time** (for example 02/07/2026 and 12pm). It drives the shortfall period, so confirm the date even if Paul only says a day name.
Use the button-selection tool for any question with a fixed or short set of options (none is expected here) and typed input for dates, names and figures.
Nothing else is asked: the shortfall start and end dates, the weekdays, the Cc (always Sitamah Nathoo) and every RGAR and Fact Find figure are derived.

**The shortfall period rule (fixed, not reconfirmed per client; checked against a worked example):** start = the 1st of the month immediately after the month of the next Teams meeting; end = the same day and month, `years until retirement` years later. For example a next meeting on 02/07/2026 and 18 years until retirement give 1 August 2026 to 1 August 2044. The program applies it; you never compute it.

## Layout
```
{
 "client_full_name": "<as in the Fact Find Summary>", "client_first_name": "<for the greeting>", "client_surname": "<surname>",
 "age": 41, "rgar_dob": "DD/MM/YYYY", "retirement_age": "65", "years_until_retirement": "24",
 "current_value": "R 30 000.00", "future_value": "R 61 000.00", "net_monthly_target": "R 25 000.00",
 "lump_sum": "R 150 000", "monthly": "R 4 200.00", "escalation": "6%", "sustainability_age": "85", "recurring_investment": "R 2 000.00",
 "employer": "<as in the Fact Find Summary>", "job_title": "<as in the Fact Find Summary>", "gross_monthly_income": "R 45 000.00",
 "client_email": "<address>", "email_source": "fact_find_summary", "email_note": "",
 "meetings_held": ["DD/MM/YYYY"], "next_meeting": {"date": "DD/MM/YYYY", "time": "12pm"},
 "plan_folder": "<the RA transaction folder's name, for example Surname, First - (OM RA - R2000)>",
 "flags": [], "sources": {"rgar": "...", "personal": "...", "net_target": "...", "email": "...", "meetings": "...", "next_meeting": "..."}, "conflicts": []
}
```
- `email_source` is `fact_find_summary` (the address must then be in its text) or `other` with `email_note` saying where it came from.
- `flags` holds the things Paul must hear in the final report: any figure not traceable to the Fact Find Summary, conflicts between Fact Find Summary versions, a no-logo SharePoint copy, anything assumed (for example which client). The R 0 recurring-investment flag is added by the program.
- `sources` says where each answer came from (a document name, or Paul's words). `conflicts` must be empty.
