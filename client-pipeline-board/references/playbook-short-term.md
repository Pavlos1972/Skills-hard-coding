# Short-Term Insurance — Stage Logic

> Loaded from `playbooks/short-term-insurance.md`, referenced by the core `SKILL.md`. This line delegates entirely to the standalone `cameron-short-term-skill` — this file exists only so the board's index has a pointer for STI, not because there's separate logic to hold.

### Short-Term Insurance
| Internal stage | What happens | Feeds the board as |
|---|---|---|
| Referral to Cameron Maritz | **Auto-built, chat-approved, then Claude-sent directly — delegated entirely to `cameron-short-term-skill`.** The moment the FF confirms an STI need, call that skill directly rather than drafting inline. It locates the FF and builds the complete referral itself (introduce client, confirm the FF's exact instruction, **full client contact details: name, ID, cell number, and email — never ID alone**), no upfront question. It then **presents the built email in chat** (To/CC/Subject/Body) as this card's pending question and waits for Paul's explicit approval — only once approved does it **send directly via `outlook_send_mail`**, CC'ing the client, Sitamah, **and Paul himself**; it never saves to Outlook Drafts. Once sent, Sitamah gets a Teams message with **no "watch for a reply" ask** — Cameron contacts the client directly, so there's nothing for her to do but be told it happened. This board's job is just to trigger the skill, surface its approval question, and log the result once sent. Receive outcome (new business/broker change/not interested) via outstanding-request tracking, save, update record. | STI card: Identified lists what's needed; **pending shows the built email awaiting Paul's send approval**; Actions Taken logs the confirmed send (via `cameron-short-term-skill`), CC'd to client + Sitamah + Paul. |

