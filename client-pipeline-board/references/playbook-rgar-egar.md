# RGAR / EGAR — Stage Logic

> Loaded from `playbooks/rgar-egar.md`, referenced by the core `SKILL.md`.

### RGAR
| Internal stage | What happens | Feeds the board as |
|---|---|---|
| Request & Receive | Triggered when FF confirms RGAR required. **Auto-draft — no pending question.** Needs first: POI (if Pension/Provident exists), existing RA statement(s), Pension/Provident statement(s) — check General AND the OneDrive "6. Policy Schedules" folder first. Once available, auto-draft the request to Alwyn (CC Sitamah) using the ALWYN — RGAR template convention, pulling ID/age/retirement-age target from the FF and fund value/contribution from the statement; flag plainly anything still missing rather than guessing. | RGAR card: Identified lists what's required and what's on file/confirmed; no pending banner; Actions Taken logs the draft. |
| Proposal — Claude-drafted | On receipt of the report back from Alwyn: auto-draft the client-facing RGAR proposal via `rgar-skill`, HTML body, straight to Outlook Drafts. Attach-before-sending note if the RGAR PDF or a fund fact sheet should accompany it. A surfaced shortfall can spawn a new RA line — note the link. | Actions Taken logs the report's receipt, then the proposal draft, as separate bullets. |

### EGAR
| Internal stage | What happens | Feeds the board as |
|---|---|---|
| Request/Receive/Present | Triggered only when the FF confirms children exist **and** education investment is required. Email Alwyn, always separate from any RGAR request, per child. On receipt: notify Paul; Paul builds the proposal (not yet moved to Claude-drafted — revisit if he wants it wired the same way as RA/Investments/RGAR). | EGAR card: Identified/pending/Actions Taken as above, per child. |

