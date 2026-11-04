# Field mappings for the bundled application templates

Contents: 1. OM Application Template (every field, its type and dropdown options; adding a new Product value) | 2. General Short Risk Application (every field and its meaning).

Both templates in `assets/` are real, fillable PDF AcroForms — every box on the
page is backed by a named form field. Always fill these by writing values into
the actual named fields (pypdf, or an equivalent AcroForm library). Never
recreate the page from scratch with a drawing library (reportlab, etc.) — a
lookalike is not the firm's actual form and will not be accepted as the
compliance record.

The program checks the blank forms itself at the start of every run and again when it fills: `assets/forms.json` holds the checksum, every field, its type and every dropdown option of both forms, and the program stops if either form differs. The General form's key names used in `plan.json` (title, first_names, surname, id_number, cell, work, email, unit, complex, street_no, street_name, suburb, city, region, postal_code, best_time, best_day, doctor, doctor_tel, doctor_years, account_holder, bank, branch_name, branch_code, account_type, debit_date, account_number, payer_contact, payer_email, child1_name, child1_id, child2_name, child2_id, ben1_name, ben1_id, ben1_relation, ben1_share, ben2_name, ben2_id, ben2_relation, ben2_share, insolvent, debt_review, debt_assistance, quote_no, owner, owner_pays) map to the field names in the table in section 2; the program builds the insurer, cover line, replacement fields and the date itself.

---

## 1. OM Application Template (`OM_Application_Template.pdf`)

Old Mutual's application/capture-sheet AcroForm — used for RA (recurring and
lump sum / Section 14 transfer), Tax-Free (recurring and lump sum), and Flexi
Investment applications. One template, reused for every OM product; the
`Product` field's dropdown selects which product this instance is for.

| Field name | Type | Options (if a dropdown) |
|---|---|---|
| `Product` | dropdown | OM Flexi Investment Plan; OM RA – Xtra Max 8.5% - section 14 transfer; OM RA – Xtra Max 8.5%; OM RA – Xtra Max 5%; OM Optimal RA – Recurring; OM Tax Free recurring; OM Tax Free Lumpsum; OM RA – Wealth recurring |
| `DateOfEntry` | text | — |
| `DeferredPremiumFacility` | dropdown | Yes / No / N/A |
| `IsReplacement` | dropdown | Yes / No |
| `ReplacedPolicyNumbers` | text | — |
| `Title` | dropdown | Mr / Mrs / Ms / Miss / Dr |
| `FullName` | text | — |
| `IDNumber` | text | — |
| `CountryOfBirth` | text | — |
| `Nationality` | text | — |
| `CorrespondenceLanguage` | text | — |
| `MaritalStatus` | dropdown | Single / Married / Divorced / Widowed / Separated / Civil Union / Customary Marriage / Life Partner / Cohabiting |
| `MaritalDate` | text | — |
| `MaritalContractType` | dropdown | In Community of Property / Out of Community – with Accrual / Out of Community – without Accrual / Customary Marriage / Civil Union / Religious Marriage / Foreign Marriage / N/A |
| `TaxNumber` | text | — |
| `ForeignTaxObligation` | dropdown | Yes / No |
| `ForeignTaxNumber` | text | — |
| `TelH`, `TelW`, `TelCell` | text | — |
| `Email` | text | — |
| `PostalAddress`, `PostalCode` | text | — |
| `ResidentialAddress`, `ResidentialCode` | text | — |
| `Occupation`, `EmploymentPosition`, `EmploymentIndustry` | text | — |
| `HighestQualification` | dropdown | Matric / Matric & Diploma / 4-Year Diploma / 3-Year Degree / Postgraduate |
| `EducationOther` | text | — |
| `BenName`, `BenSurname`, `BenCellNumber`, `BenIDNumber`, `BenRelationship`, `BenShare` | text | beneficiary 1 |
| `BenName_2` … `BenShare_2` | text | beneficiary 2 (same fields, `_2` suffix) |
| `BenName_3` … `BenShare_3` | text | beneficiary 3 (same fields, `_3` suffix) |
| `NameOfBank` | dropdown | Absa Bank / Access Bank / African Bank / Albaraka Bank / Bank Zero / Bidvest Bank / Capitec Bank / Discovery Bank / FNB / FNB Namibia / GoTyme Bank (TymeBank) / Investec / Nedbank / OM Bank (Old Mutual) / Postbank / Sasfin Bank / Standard Bank / Other |
| `BranchCode`, `AccountHolder`, `AccountNumber` | text | — |
| `AccountType` | dropdown | Current / Savings / Cheque / Other |
| `SourceOfFunds`, `SourceOfIncome` | text | — |
| `KnownDays`, `KnownMonths`, `KnownYears` | text | how long the advisor has known the client, split across three fields — fill whichever unit applies, leave the other two blank |
| `FundsRaisedFrom` | text | — |
| `OwnKnowledge` | dropdown | Yes / No — does the advisor have personal knowledge of the source of funds? |
| `OriginateFrom` | text | only relevant when `OwnKnowledge` = No — "if not from own knowledge, where did the funds originate" |
| `Signature` | text | — |
| `SignatureDate` | text | — |

### Adding a new `Product` dropdown value

`Product` is a closed dropdown (`/Opt` array), not free text, and per the
premium-amount rule below every filled form needs a client- and
amount-specific value (e.g. `"OM Optimal RA – Recurring - R 2,800 p.m."`)
that won't already be in the list. Add it to the `/Opt` array before setting
the field value — see `scripts/fill_om_form.py`'s `add_product_option()` for
the exact AcroForm manipulation (inserts the new string next to the base
product it's a variant of, so the dropdown stays organised).

---

## 2. General Short Risk Application (`General_Short_Risk_Application_Template.pdf`)

Wealth Revolution's own generic short-term/risk application, used across
multiple insurers (Momentum, Brightrock, Discovery, Old Mutual, Liberty,
Sanlam, Stanlib — set via the Insurer dropdown). Single page. Unlike the OM
template, the field *names* in this PDF are generic (`Text Box 4_7`, `List
Box 3_3`, …) — they carry no meaning on their own. The mapping below was
built by reading each field's on-page position against the visible labels,
confirmed against a rendered image of the form. If Wealth Revolution ever
issues a revised version of this template, re-derive the mapping the same
way (dump field names + `/Rect` positions with pypdf, sort top-to-bottom then
left-to-right, render the page to PNG with `pdftoppm`, and read the two side
by side) rather than assuming field names carry meaning.

| Field name | Label on form |
|---|---|
| `List Box 1` | INSURER (dropdown: Momentum / Brightrock / Discovery / Old Mutual / Liberty / Sanlam / Stanlib) |
| `Text Box 1` | Quote No |
| `List Box 2` | Cover Lines (Business / Personal) |
| `Text Box 2` | OWNER OF THE POLICY |
| `List Box 3` | THE POLICY OWNER IS RESPONSIBLE FOR PAYING THE MONTHLY PREMIUM (Yes/No) |
| `Text Box 3` | TITLE |
| `Text Box 4` | FULL NAMES |
| `Text Box 4_2` | SURNAME |
| `Text Box 4_3` | ID NUMBER |
| `Text Box 4_4` | CELL |
| `Text Box 4_5` | WORK |
| `Text Box 5` | E-MAIL |
| `Text Box 4_6` | UNIT NUMBER |
| `Text Box 4_7` | COMPLEX NAME |
| `Text Box 4_8` | STREET NUMBER |
| `Text Box 4_9` | STR NAME |
| `Text Box 5_2` | SUBURB |
| `Text Box 5_3` | CITY |
| `Text Box 4_10` | REGION |
| `Text Box 4_11` | POSTAL CODE |
| `Text Box 4_12` | BEST TIME FOR US TO PHONE YOU |
| `Text Box 4_13` | BEST WORK DAY FOR US TO PHONE YOU |
| `Text Box 4_14` | DR (doctor's name) |
| `Text Box 4_15` | DR TEL NO |
| `Text Box 4_16` | YEARS (with the doctor) |
| `Text Box 5_4` | ACCOUNT HOLDER (premium-payer's banking details) |
| `Text Box 5_9` | BANK NAME |
| `Text Box 4_17` | BRANCH NAME |
| `Text Box 4_18` | BRANCH CODE |
| `Text Box 4_19` | ACCOUNT TYPE |
| `Text Box 4_20` | DEBIT DATE (any date except the 10th–14th) |
| `Text Box 5_10` | ACCOUNT NUMBER |
| `Text Box 4_21` | CONTACT NUMBER |
| `Text Box 4_22` | EMAIL ADDRESS |
| `Text Box 5_11` | CHILD 1 — NAME & SURNAME |
| `Text Box 5_12` | CHILD 1 — ID NUMBER |
| `Text Box 5_13` | CHILD 2 — NAME & SURNAME |
| `Text Box 5_14` | CHILD 2 — ID NUMBER |
| `Text Box 5_15` | BENEFICIARY 1 — NAME & SURNAME |
| `Text Box 5_16` | BENEFICIARY 1 — ID NUMBER |
| `Text Box 4_23` | BENEFICIARY 1 — RELATION |
| `Text Box 4_24` | BENEFICIARY 1 — % OF BENEFIT |
| `Text Box 5_17` | BENEFICIARY 2 — NAME & SURNAME |
| `Text Box 5_18` | BENEFICIARY 2 — ID NUMBER |
| `Text Box 4_25` | BENEFICIARY 2 — RELATION |
| `Text Box 4_26` | BENEFICIARY 2 — % OF BENEFIT |
| `List Box 3_2` | EVER BEEN INSOLVENT OR SEQUESTRATED? (Yes/No) |
| `List Box 3_3` | ARE YOU CURRENTLY UNDER DEBT REVIEW? (Yes/No) |
| `List Box 3_4` | HAVE YOU APPLIED FOR ASSISTANCE WITH DEBT? (Yes/No) |
| `List Box 3_5` | WILL THIS POLICY REPLACE AN EXISTING POLICY? (Yes/No) |
| `Text Box 5_5` | EXISTING INSURANCE — COMPANY (only if replacing) |
| `Text Box 5_6` | EXISTING INSURANCE — Policy Number (only if replacing) |
| `Text Box 5_7` | CLIENT'S SIGNATURE |
| `Text Box 5_8` | DATE |

The General form's insurer is chosen with the Insurer dropdown; Cover Lines offers Business or Personal, so Business Covers, Buy & Sell, Contingent Liability and Keyman Cover count as Business and Personal Covers as Personal. The form was used in production for a Brightrock application on 30.09.26 and again on 08.10.26.
