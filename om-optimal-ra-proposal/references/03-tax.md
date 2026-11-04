# The Tax Reform Tool (the program runs it; you never type a tax figure)

`assets/Tax_Reform_Tool_TEMPLATE_4.xlsm` is the only correct version (earlier versions had stale values and wrong tax brackets). It holds the **2026/2027** SARS tables (effective 1 March 2026), valid until 28/02/2027: from 01/03/2027 the program STOPS and asks Paul to confirm the workbook (and `assets/tax_facts.json`) has been updated in Claude Code.

**How the program runs it.** For each scenario it saves a copy of the workbook, writes the inputs, lets LibreOffice recalculate it, and reads the outputs. The macros are only for the radio buttons; the employment type is the text in `Calcs!B2` (`Tax Monthly` = self-employed or no fund; `DEDUCTION LIMITS` = pension fund; `Max %` = provident fund). Then it recomputes **every** figure itself from the tax facts; any difference stops the run. If LibreOffice is missing the run stops: say so, never type a figure.

Inputs on `Maximise Allowance Tool`: C15 monthly remuneration (the gross monthly income), C17 age, C20 to C23 the employer and member pension and provident contributions **as a share of the remuneration**, C24 the monthly RA. Outputs: C28 annual tax saved from the RA deduction, C29 pension, C30 provident, C31 annual tax payable after deductions and rebate, C34 maximum deduction left to use, C36 additional monthly premium, C37 once-off lump sum to maximise. `Calcs!C15` is the binding allowance = MIN(R430,000, 27.5% x `Calcs!B35`), where `Calcs!B35` = annual remuneration + the employer fund contributions (a fringe benefit added back). `Reinvest Calcs!H41:Q41` are the ten bar values (the RA escalating at 10%). (Note: "C15" means two cells on two sheets: the remuneration input and, as `Calcs!C15`, the cap.)

**The four scenarios and the three tables**
| Run | RA input | Used for |
|---|---|---|
| baseline | R 0 | [MAXIMUM RA CONTRIBUTION] = the tool's additional monthly premium at an RA of R 0 |
| Table 1, your current situation | the TOTAL of the existing RAs' monthly contributions (R 0 only if the client has none) | the tax saved on the existing RAs is shown, never R - unless the client has no RA at all |
| Table 2, the full deduction | [MAXIMUM RA CONTRIBUTION] = (cap - the yearly fund contributions) / 12 | one new OM Optimal RA row; existing RAs never appear |
| Table 3, what is proposed | the proposed premium (replace), or the existing total + the proposed premium (keep) | replace: the new RA row only; keep: the existing rows + the new row |

The pension or provident rows appear in **all three tables**, identical in amount; only the RA rows change. The label is "Provident Fund" for a provident client and "Pension Fund" for a pension client, never mixed; with no fund the rows and the fund tax line do not appear. [TOTAL CAP MONTHLY] = cap / 12 (used only in the "what you can save" sentence). The ACI is always 10%.

**The audit checks the program proves (old Step 7 and MCD 8.6)**: 1 [TOTAL CAP MONTHLY] = cap / 12; 2 [MAXIMUM RA CONTRIBUTION]; 3 the tax payable of Tables 1, 2 and 3 all differ; **4 and 5 are computed and, when the two figures differ, flagged to Paul with BOTH figures, never forced** (the known edge case: tax saved is the tool's own figure; it can differ from a difference of payables when the extra deduction straddles a tax bracket or in a keep-some-replace-some case); 6 Table 2's fund rows + RA row = [TOTAL CAP MONTHLY]; 7 Table 3's % left; 8 the bar chart's year 1 = Table 3's tax saved from the RA; 9 the "what you can save" sentence carries [TOTAL CAP MONTHLY] in the right scenario wording. Always use the tool's own native "tax saved" cells, never back-calculate them.
