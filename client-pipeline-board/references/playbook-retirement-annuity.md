# Retirement Annuity — Stage Logic

> Loaded from `playbooks/retirement-annuity.md`, referenced by the core `SKILL.md`.

### Retirement Annuity
| Internal stage | What happens | Feeds the board as |
|---|---|---|
| Info Gathering | Existing RA statement(s), Pension/Provident statement(s) if they exist. | Document needs go on **General**. |
| Quote Prep | Email Alwyn: OM Optimal RA Quote (Monthly) only if a monthly contribution is specified; an RA Lump Sum quote only if an amount is specified (one Plan 2: `om-optimal-ra-proposal` handles one); another provider if named. Pension/Provident funds are never quoted directly. Servicing: request the equivalent servicing quote from Alwyn — ask Paul what's changing before drafting. | RA card: Identified lists the quote(s) needed; pending asks to send; Actions Taken logs it. |
| Proposal — Claude-drafted | Once the quote is back, auto-draft the client-facing proposal via `om-optimal-ra-proposal`, HTML body, straight to Outlook Drafts. Attach-before-sending note if a quote/fact-sheet file exists in OneDrive. | Actions Taken: "RA proposal drafted (om-optimal-ra-proposal), saved to Outlook Drafts. To [Client], CC Sitamah." |
| Application Prep | **Pre-filled automatically ahead of the 2nd/3rd meeting**, once quote + FF + proposal give enough (`complete-applications-skill` — RA recurring, RA lump sum/Section 14). Flags what's still missing. | Actions Taken logs the pre-fill, missing items noted. |
| Presentation/Application/Compliance | Present at the follow-up appointment. Accept → application (pre-filled, completed live), Section 14 flag if applicable, FICA, send to provider, debit order, schedule + Welcome Letter, **New Business → `wr-roa-builder`; Servicing → `wr-sroa-builder`**, Welcome Email, confirm in force, 16-point compliance audit, update record. Decline → done. | Pending on decision, then Section 14 flag if a transfer's involved. Actions Taken logs each step. |
| Section 14 (if required) | Still TBC with Paul (Paul's ClickUp Master Document flags this too). 180-day countdown from Transfer Start Date; warning at 150 days. | Treat as a flagged item under the RA card's Identified until Paul gives it real shape. |

