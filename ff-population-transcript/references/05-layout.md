# The layout: fixed 11 sections plus Next Steps & Next Meeting

## Step 2: Follow the Audio to Text file's own layout (v3.0)

The Fact Find Transcript follows the layout of the Audio to Text file (WR Fact Find v3.0, October 2026): the same sections, the same labels and the same order, in the same two-column style. The program draws the 11 sections from `scripts/layout.json` in the same order every time (Paul, decision 15); the field labels in that file are this skill's own, because the form's label file could not be read, and Paul checks them on a sample PDF. The v3.0 sections, in order, are:

1. **Client Info** — Meeting (consent to record and transcribe, advisor, date completed, type of meeting, referral from); Client (name, surname, date of birth, age, ID or passport, number, gender, nationality, income tax number); Contact details (cell, work, home, personal email, work email); Background (smoker, highest education, qualification details, notes).
2. **Occupation** — Work (employed, employer, what the company does, business owner, occupation, full time or contract, years in this occupation); Duties split (all the percentages, total); brief description of duties; notes. Business-owner fields only if Business owner = Yes.
3. **Income & Household** — gross monthly income, direct net income, take-home net income, monthly expenses / budget, disposable income, marital status, spouse/partner fields if any, notes.
4. **Existing Cover & Retirement** — personal risk cover (has cover, joint cover with spouse, group risk through employer); existing personal risk policies table (provider, spend, broker on record, notes); retirement funding table (type, provider/administrator, value, monthly contribution, broker on record); notes.
5. **Investments** — each investment, notes.
6. **Medical, Will & Short-Term** — medical aid (provider, plan, broker, notes); gap cover; will (has a will, up to date, held with, broker, last updated, notes); short-term insurance (has, broker, car, household contents, structural, business, spends, notes).
7. **Debts** — each debt (type, provider, description, owner, payer, term left, instalment, balance, asset value, credit life with lender, surety signed, notes); totals (monthly, liabilities, assets); notes.
8. **Children** — each child (name, surname, gender, date of birth, age, education stage, monthly cost); total childcare; notes.
9. **Health** — general health good, diabetes/high sugar, high cholesterol, high blood pressure, high BMI, other health issues, health notes.
10. **Advisor Actions** — Personal risk quotes (FNA quote with type and insurer; Shortfall quote with type and insurer; reduced quotes; preferred monthly spend; notes); Retirement & investment quotes (RGAR, retirement age, net amount; retirement annuity quotes; EGAR; investment quotes; notes); Referrals & documents (short-term (Cameron), medical & gap (Valerie), will (Capital Legacy), others; documents to request; notes).
11. **Risk Calculation** — Life cover: fractured cover; Life cover: standard; Permanent disability: fractured cover; Permanent disability: standard; Dread disease; Income protection / sickness benefit; notes.

*The old 21-page v2.0 layout and its field map (`references/ff-field-map.md`) are retired for new runs. If a future form file has a different schema version, the program stops before building and the skill is updated once.*

**Meeting logistics** go in a final "Next Steps & Next Meeting" section after the Risk Calculation, separated from the numbered sections.

**Fields the layout has no place for:** a populated key or column that `layout.json` does not know is never dropped: it is printed in a closing block, "Other fields from the form", and put on Paul's glance list. **Parts that are hidden:** the business parts are filled only when Business owner is Yes; if the form holds values there anyway they are not printed and the glance list says so.
