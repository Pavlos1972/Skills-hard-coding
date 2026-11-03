# The answers file (one JSON file, every answer with its source)

Write the file below and run `run.py answers`. The program refuses it (nothing saved) and says why if anything is missing or wrong. **Every figure, name, ID, CP number and date you type must be in the right document's text**: old figures in the Current Policy Schedule pages of THIS policy, new figures in the accepted quote, each quote block's figures in its own quote. Typing a figure from memory, or one from another client, is a red cross.

## What to ask Paul (never infer, no default sentence)
1. **Which quotes were compiled, and which did the client accept.** Ask with buttons. The FNA can be declined entirely (`fna_declined: true`). The accepted quote is whichever one the "new" figures must trace to. If Paul's reason mentions affordability, that points to the Alternative Quote: confirm it, do not assume it.
2. **The reason for the servicing change, in his own words, for this client.** Typical reasons he may cite: new FNA done, affordability review, life-stage change, CPI increase, cover gap found. The Record of Advice is written from his answer, never from a template.
3. **Is it an investment-linked risk policy** (for example BrightRock Flexible Cover with an investment component)? If yes, also ask the reason for the portfolio or fund change in light of the client's risk profile. If no, the Portfolio Changes section is the literal text `N/A` (the program does that; never blank, never an invented rationale).
4. **The SROA date.** Never today's date and never the date of generation. It should match the date the accepted Servicing Quote was signed: take it from the signed quote or the acceptance email, and have Paul confirm it in the table. If he chooses a date that is in neither document, record his words in `sroa_date_source.paul_said`.
5. **The client's full legal name** for the signature line (normally the Owner; confirm for joint or business-owned policies; take it from the documents, not the everyday name) and the **13-digit ID number** (from the documents, never from memory).
6. **A debt on the old schedule that does not obviously match one on the new quote** (different description, different creditor label, a changed amount): do NOT guess whether it is the same debt renamed or a new one. Matching amounts alone is not enough. Ask Paul and put his words in that item's `confirmed`. A benefit on one side only (new or removed) is entered with only `old` or only `new` and needs `confirmed`.

## Layout
```
{
 "insurer": "BrightRock",
 "policy_number": "<this run's policy number>",
 "owner": "<full legal name, as in the documents>",
 "owner_id": "<13 digits, no spaces>",
 "client_first_name": "<everyday first name>", "client_surname": "<surname>",
 "client_signature_name": "<full legal name typed under the signature line>",
 "sroa_date": "DD/MM/YYYY", "sroa_date_source": {"file": "acceptance_email", "paul_said": ""},
 "compiled": {"fna": true, "shortfall": false, "alternative": true},
 "fna_declined": false,
 "accepted": "alternative",
 "cp_numbers": {"fna": "CP...", "alternative": "CP..."},
 "layout": "grouped",
 "blocks": {"fna": {"groups": [{"heading": "Life Cover", "items": [{"label": "Death cover", "value": "R1,000,000", "unit": "amount"}]}]}, "alternative": {"groups": [...]}},
 "changes": {"groups": [{"heading": "Life Cover", "items": [{"label": "Death cover", "old": "R1,200,000", "new": "R1,000,000", "unit": "amount"}]},
                        {"heading": "Policy Details", "items": [{"label": "Premium (incl. R20 policy fee)", "old": "R1,300.00", "new": "R1,172.80", "unit": "premium"},
                                                              {"label": "ACI (Automatic Cover Increase)", "old": "5%", "new": "5%", "unit": "percent"},
                                                              {"label": "ABI (Automatic Benefit Increase)", "old": "5%", "new": "5%", "unit": "percent"}]}]},
 "reason": "<Paul's reason, in his words>", "reason_source": "Paul, DD/MM: <where he said it>",
 "investment_linked": false, "portfolio_reason": "", "portfolio_source": "",
 "sources": {"quotes": "...", "accepted_quote": "...", "owner_id": "...", "sroa_date": "...", "signature_name": "...", "cp": "...", "investment_linked": "..."},
 "conflicts": []
}
```
- `unit` is `amount` (whole rand: R1,500,000), `monthly` (whole rand per month: R25,000 p.m.), `premium` (rand and cents per month: R1,850.00 p.m.) or `percent` (3%). The program writes every figure in that one form and works out **"No change (value)" itself** when old and new are equal. Never type "No change".
- Flat list (any insurer except BrightRock's needs-based policies): `"layout": "flat"` and `"changes": {"items": [ ...old/new items... ]}`. The program puts them in the fixed order: Life Cover, Disability Cover, Dread Disease, Income Protection, Premium, ACI, ABI, Retrenchment Cover; anything else (a one-off change) follows, only if Paul asked for it (put his words in `extra_asked`).
- **A benefit that is not part of this policy's cover at all is left out entirely** (for example no Retrenchment Cover line when the policy has none): "No change" says the benefit exists and is unchanged. Ask Paul only if it is unclear whether a benefit is absent or genuinely unchanged at zero.
- **ACI and ABI are always compared**, changed or not (they steer how cover and premium grow). ACI is the yearly cover/base growth (BrightRock: "Yearly base increase"); ABI is the yearly premium growth ("Yearly premium increase"). Other insurers name them differently: confirm the mapping with Paul if unclear. **Waiting Period is deliberately not in the list**: only when Paul asks for it, as a one-off item.
- **BrightRock needs-based policies use `"layout": "grouped"`**, five headings in this fixed order, each with its own bullets: (1) **Life Cover**: everything "caused by death", including the death portion of each debt; (2) **Lump Sum Disability Cover**: everything "permanent", including the permanent portion of each debt; (3) **Income Protector / Sickness Benefit**: the "recoverable"/temporary household needs; (4) **Additional Expense Needs / Dread Disease**: BrightRock's Additional Expense Needs IS its dread disease cover, one benefit, always this combined heading, never a separate "Dread Disease" heading and never an invented dread-disease figure; (5) **Policy Details**: Premium, ACI, ABI. A debt is two bullets (death portion under Life Cover, permanent portion under Lump Sum Disability Cover). This mapping is an interpretation of BrightRock's categories, not a value in its documents: confirm with Paul if a mapping question arises; the Additional Expense / Dread Disease equivalence is settled, do not re-ask it.
- **The R20 policy fee.** The premium line is always inclusive of the R20 monthly policy fee, labelled exactly `Premium (incl. R20 policy fee)`. Use the insurer's own total ("Total premium (including the policy fee)"), not your arithmetic. The program refuses any other label, a premium figure not in the quote, and a quote that does not state a total including the policy fee.
- **CP numbers.** Each compiled quote has its own CP (proposal) number, printed at the top of its block; the accepted quote's CP number is also printed above Block 4 beside the policy number. Give one entry per compiled quote; leave it `""` only when the document or Paul says that quote has none (never write "N/A"). The in-force Current Policy Schedule is not a quote and has no CP number.
- `blocks` holds only the compiled quotes' OWN figures under the same headings (not an old-to-new comparison). A quote that was not compiled has no figures: never invent any. The wording for a quote not compiled is fixed by the program ("Not compiled for this client."; for a declined FNA "Not compiled — declined by the client.").
- `sources`: say where each answer came from (a document name, or Paul's words). `conflicts` must be empty: if two sources disagree, stop and ask Paul.
