# Investments — Stage Logic

> Loaded from `playbooks/investments.md`, referenced by the core `SKILL.md`.

### Investments
| Internal stage | What happens | Feeds the board as |
|---|---|---|
| Info Gathering | Existing investment statement(s), TFSA statement if one exists. | Document needs go on **General**. |
| Quote Prep | Email Old Mutual: Tax-Free Savings quote only if TFSA required (with monthly contribution); General Investment quote only if required (monthly and/or lump sum). | Investments card: Identified/pending/Actions Taken as above. |
| Investment Proposal — Claude-drafted | Once the quote is back, auto-draft the client-facing proposal via `om-tax-free-skill` (Tax-Free) or `investment-comparisons-skill` (cross-provider), HTML body, straight to Outlook Drafts. Attach-before-sending note if a quote/fact-sheet file exists. | Actions Taken: "Investment proposal drafted ([skill used]), saved to Outlook Drafts. To [Client], CC Sitamah." |
| Application Prep | **Pre-filled automatically ahead of the 2nd/3rd meeting**, once quote + FF + proposal give enough (`complete-applications-skill` — Tax-Free recurring or lump sum). Flags what's still missing. | Actions Taken logs the pre-fill, missing items noted. |
| Presentation/Application/Compliance | Present, complete Risk Tolerance Questionnaire, client decides. Accept → application (pre-filled, completed live), FICA pack, schedule + Welcome Letter, **New Business → `wr-roa-builder`; Servicing → `wr-sroa-builder`**, Welcome Email, confirm in force, 16-point audit including Risk Tolerance Q. Decline → done. | Pending on decision; Actions Taken logs each step. |

