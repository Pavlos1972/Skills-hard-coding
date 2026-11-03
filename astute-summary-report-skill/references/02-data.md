Contents: the data file you write, field by field. Write ONE JSON file in exactly this layout; the program refuses anything else.

Every figure, policy number, date and name must be copied exactly as the report prints it (dates as DD/MM/YYYY). The program looks for each one in the report's own text. If the report does not show something, use an empty string "" (it is then flagged); never guess.

```
{
 "header": {"client_name": "First Surname (as Paul named the client)", "astute_name": "the name Astute holds, only if different",
            "id_number": "...", "date_of_birth": "DD/MM/YYYY", "report_reference": "...", "report_date": "DD/MM/YYYY", "requested_by": "..."},
 "providers": [ {"name": "Insurer A", "result": "data"},
                {"name": "Insurer B", "result": "not_found"} ],          // EVERY provider block: data | not_found | unable_to_match | no_row
 "policies": [
  {"provider": "Insurer A", "policy_number": "...", "product_name": "...", "status": "Active", "start_date": "DD/MM/YYYY", "kind": "risk",
   "owner": "...", "life_assured": "...", "premium_payer": "...", "beneficiaries": [{"name": "...", "percent": "100"}],
   "benefits": [{"name": "Life cover", "cover_amount": "R 1 000 000.00", "type": "stand-alone"}],      // type: stand-alone | accelerated | unable
   "premium": "R 350.00", "premium_frequency": "monthly", "premium_pattern": "ACI", "pattern_text": "e.g. funding pattern plus annual benefit increase 5%"},
  {"provider": "Insurer A", "policy_number": "...", "product_name": "...", "status": "Active", "start_date": "...", "kind": "investment",
   "owner": "...", "life_assured": "...", "premium_payer": "...", "beneficiaries": [],
   "values": {"premiums_paid": "R ...", "fund_value": "R ...", "surrender_value": "R ...", "two_pot": {"savings": "R ...", "retirement": "R ..."}},
   "premium": "R 1 000.00", "premium_frequency": "monthly", "premium_pattern": "fixed", "pattern_text": "escalation 6%",
   "fund_allocation": [{"fund": "Fund name", "percent": "60"}], "note": "optional"}
 ],
 "section2": {"group_risk": {"reflected": false}, "retirement_fund": {"reflected": true, "details": ["Insurer, employer, fund name, membership start, salary, retirement age and date, allocation, values, contributions, each group risk benefit with cover amount and termination age, beneficiaries"]}},
 "report_totals": {"monthly_premiums": "only if the report prints a total", "fund_value": "only if the report prints a total"}
}
```
Rules the program applies:
- **status** is copied exactly as Astute shows it. It decides the section: a status containing "paid up" goes to Section 3; lapsed, surrendered, inactive, cancelled, terminated, matured and similar go to Additional Notes; "active", "in force", "premium paying" go to Section 1; anything else goes to Additional Notes with a flag.
- **premium_pattern** is ACI, ABI, age-rated, fixed or other (use the insurer's own naming in pattern_text, with the stated escalation percentage). **premium_frequency** is monthly, annual or single.
- A provider whose result is not `data` cannot have policies. A policy's provider must be in the providers list.
- **Totals are added up by the program** from the active policies. `report_totals` is only the total the REPORT prints; a difference raises a flag.
- An investment must have `values` with at least `fund_value`. Include owner, life assured, premium payer and beneficiaries (with percentages) wherever the report shows them.
- Policy descriptions are NOT in this file: they come from the products step.
