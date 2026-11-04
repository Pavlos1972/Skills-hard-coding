# The answers file

Write ONE JSON file, every answer with its source. The program checks each figure, name, date and fee against the text of the right document and refuses what it cannot find. **Ask Paul only for what the documents cannot tell you:** replace or keep the existing RA(s) (his answer), whether the lump sum goes in (yes or no) and its kind and source, the meetings already held (pre-fill them from the file names) and the next meeting. Items 1 to 6 of the old checklist are documents to find in the client's file, not questions.

## The main proposal (`"document": "main"`, which is the default)

```json
{
 "client_full_name": "...", "client_first_name": "...", "client_surname": "...",
 "client_email": "...", "email_source": "fact_find_summary", "email_note": "",
 "age": 41, "employer": "...", "position": "...", "gross_monthly_income": "R 50 000.00",
 "fund": {"type": "pension", "employer_monthly": "R 2 500.00", "employer_pct": "5%", "member_monthly": "R 3 750.00", "member_pct": "7.5%", "value": "R 150 000.00", "value_date": "30/09/2026"},
 "existing_ras": [{"insurer": "...", "policy_number": "...", "monthly": "R 1 500.00", "gross_value": "R 90 000.00", "value_date": "30/09/2026", "no_penalties": false}],
 "ra_decision": "keep",
 "rgar": {"shortfall": "R 4 200.00", "years": "24", "current_value": "R 30 000.00", "future_value": "R 61 000.00", "retirement_age": "65"},
 "proposed_premium": "R 3 000.00", "start_date": "01/12/2026",
 "funds": [{"name": "...", "allocation": "60", "asset_mgmt_fee": "0.85%"}, {"name": "...", "allocation": "40", "asset_mgmt_fee": "0.90%"}],
 "net_admin_fee": "3.05%", "advice_fee": "0.575%", "adviser_charge": "0.00%", "monthly_admin_fee": "R 36.50",
 "lump_sum_applies": false,
 "meetings_held": ["29/10/2026"], "next_meeting": {"date": "12/11/2026", "time": "12pm"},
 "plan_folder": "Surname, First - (OM RA - R3000)", "flags": [], "conflicts": [],
 "sources": {"personal": "...", "income": "...", "fund": "...", "existing_ras": "...", "ra_decision": "Paul, in chat", "rgar": "...", "quote": "...", "funds_fees": "...", "email": "...", "meetings": "...", "next_meeting": "Paul, in chat"}
}
```
- `fund.type` is `none` (self-employed or employed with no fund; then leave the other fund fields out), `pension` or `provident`. **A client with BOTH a pension and a provident fund: the tool takes one fund type at a time: STOP and ask Paul.** Never include an end date for the fund.
- `existing_ras` is `[]` when the client has none (then `ra_decision` is `none`); otherwise one entry per policy and Paul's `replace` or `keep`. `no_penalties` is `true` only on Paul's word that the policy is too new for surrender penalties (it prints the italic note "No penalties apply - policy is too new").
- `rgar` is `null` when none was requested (the email then says "You did not request for a Retirement Goal Analysis Report."). The shortfall is the SECOND shortfall table (after the proposed RA is factored in), never the first.
- `gross_monthly_income` is also the tool's monthly remuneration. The fund statement's rand amounts are checked in its text; the tool is given each as a share of the gross income.
- Fees are read from THIS quote every time: the asset management fee of each fund, the net administration fee, the ongoing advice fee (under "PAYABLE FROM THE PLAN'S FUND VALUE - Asset advice fees", usually 0.575%), the adviser remuneration account charge (usually 0.00%), the monthly fixed administration fee in rand. The blended asset management fee and the total are worked out by the program.
- `flags`: short sentences for Paul that the documents show but the program cannot judge (a quote that expires before the start date, a discrepancy between the quote and the booster document, an assumed time or email). Never leave a known discrepancy out.

- **What else the quote shows:** the ACI (always 10% p.a.; it must match the RGAR and the quote), the first increase date, the commitment term in years and the booster schedule. The template's wording for these is fixed: if the quote shows an ACI other than 10% or booster values that differ from the template's booster table, put it in `flags` for Paul.
- **The RGAR** is sent to the client in a separate email before this proposal (by `rgar-skill`); this email refers to it. Alwyn must always set its ACI at 10% p.a.: flag it if the RGAR shows anything else.

## The separate Lump Sum Investment email (`"document": "lump_sum"`, a second run)

```json
{
 "document": "lump_sum",
 "client_full_name": "...", "client_first_name": "...", "client_surname": "...", "client_email": "...", "email_source": "fact_find_summary", "email_note": "",
 "lump": {"type": "section14", "amount": "R 120 000.00", "policies": [{"name": "...", "net_value": "R 120 000.00"}]},
 "start_date": "01/12/2026",
 "funds": [{"name": "...", "allocation": "100", "asset_mgmt_fee": "0.85%"}],
 "ls_fees": {"admin_fee": "0.90%", "advice_fee": "0.575%", "as_and_when": "None"},
 "meetings_held": ["29/10/2026"], "next_meeting": {"date": "12/11/2026", "time": "12pm"}, "plan_folder": "...", "flags": [], "conflicts": [],
 "sources": {"personal": "...", "lump": "Paul, in chat, and the Client Overview", "quote": "the Lump Sum Quote", "email": "...", "meetings": "...", "next_meeting": "Paul, in chat"}
}
```
- Section 14 or voluntary is **Paul's answer, never inferred**. For Section 14 the amount is the sum of the source policies' **NET** fund values (never gross), each policy named. For voluntary funds: `{"type": "voluntary", "amount": "...", "source_of_funds": "...", "tax_note": "Paul's words"}`. **A voluntary lump sum has no approved tax-treatment wording: ask Paul for the note and enter it in his words (the program stops without it).** If Paul says the voluntary lump sum is meant to use up unused annual deduction room, flag it to him.
- Plan 2's funds and fees are read from the Lump Sum Quote on its own: they are often different from Plan 1 (a single fund at 100%, a tiered administration fee: copy the band or rate as the quote shows it). A lump sum (Section 14 or voluntary) never counts toward the 27.5% / R430,000 limit and is never added to the Tax Reform Tool's inputs.
