# client-pipeline-board: what changed, and what I need from you (04/11/2026)

No client data is kept in the new skill. Everything in it is invented (Pat Samplecase, example.invalid addresses, an invented Fact Find Summary). The old text is archived in `SKILL.2026-10-14.redacted.md` (three example client names and one email address replaced; you said the names are invented). The rule-by-rule check of the old skill against the new one: 983 rules, 0 unaccounted (232 kept word for word, 577 reworded, 174 dropped with a recorded reason; see `INVENTORY-REPORT.md`).

## What it is now
A program holds each client's board as ONE data file. The chat writes down what changed in this run (one file); the program applies it to the old board (read back from the published page), checks every rule on every card, applies the send table, builds the Sitamah messages, draws the page and checks the emails. A checker then REBUILDS everything and compares, so a file edited by hand cannot pass. Nothing is sent, posted or published without your one yes. Your 13 answers from Phase A are all built in.

## What I built into it (your Phase A answers)
- The board's card rules are checked: the New Business / Servicing tag only on Life Cover, RA and Investments (and only in your words), the Fact Find card Identified only, one plain question per card, short one-fact bullets (25 words to identify, 30 for an action), no stage codes, every Identified point proved by a verbatim line of a registered document (its figures too) or your words, every Actions Taken line tied to a receipt.
- The send table is data (`assets/routes.json`): ask first or build, where it lands, who sends, fresh yes needed. Proposals follow the proposal skills (Sitamah checks, attaches, sends); quote and report requests stay yours; the Medical Aid and Will referrals and the LOA email are shown complete and sent only after your yes.
- To and Cc come from one contacts table (`assets/contacts.json`). The program refuses a wrong Cc, a bracket-tag subject, a typed sign-off, a placeholder, a missing client details block (name, ID, cell, email) and a request that is not a reply to the latest thread.
- The Sitamah messages are data (`assets/triggers.json`): all twelve Action-needed messages and the FYI, with the greeting taken from the South African clock. Each is shown to you and posted after your yes.
- The page is drawn by the program, with no script in it (it cannot blank), SA time first with the Greek time in brackets for you only. The Change Log entry and the Athens-time stamp are set by the program.
- Follow-up appointment: the Teams invite is built by `teams-meeting-setup-skill` on your yes; the program prints the exact same-day check-in settings.
- Reply tracking now belongs to `outlook-emails-skill`; the Planner lines, `core-ff-intake.md`, the Project-only pointers and "device bridge" are gone; the ROA date rule is left to `wr-roa-builder`; the comparison line says any number of insurers; the RA lump sum line follows `om-optimal-ra-proposal`; one line for `life-policy-schedule-analyzer`.

## Questions that came up while building (Yes / No, recommended answers in brackets)
1. **One message per event, read as:** each Action-needed event gets its own message, and all the ordinary "something was done" items of one run are grouped into ONE FYI message in point form (what the old text called "FYI, multi-fact"), not one message each. A product skill that already messages Sitamah for the same event means the board sends none. (Yes)
2. **The Change Log** is written by the program, one short bullet per change ("Life Cover: tagged New Business"). A first run lists 15 or so lines; later runs are short. (Yes)
3. **The look of the page** is built from the written rules (1080px width, the CLAUDE badge, the card shape, an amber question banner), because I have never seen a real board. Please look at the sample attached and tell me what to change. (Look at the sample)
4. **Still open from Phase A (question 8):** does `board-index.md` (the list of all client boards and their status) exist, and where? Until you tell me, the program does not update it and the audit says so when a board is closed.
5. **Emails not on the send table** (for example an RAR request to the insurer) use one catch-all route: ask you first, saved as a draft for you to send, Sitamah copied. (Yes)
6. **Still open from the Teams meeting skill list:** the live Teams transcript skill (v35) still tells Sitamah to book the follow-up appointment. That line has to change once `teams-meeting-setup-skill` is live. A later job, not part of this upload. (Later)
7. **Evidence:** the Fact Find Summary PDF (drawn by `fact-find-summary`) is read as text, so Identified points can quote it. A scanned page cannot be proven by the program: such a point rests on your words and the audit lists it as attested. (Yes)

## What no program can close
- That the published page really read back from claude.ai is the one the chat built is checked (the program compares them), but that the chat really called the Artifact, Microsoft 365 and Zapier tools is only attested by what they returned.
- The Zapier-to-Teams message shows bold in the read-back only if Teams turns the markdown into a real bold tag; the check asks for the real tag. Unproven until one real message.
- The wording of the Medical Aid, Will and LOA emails stays in your Drafts templates (I cannot read them); the program checks the finished email, not that it matches the template.
- I have never seen a real board page, a real Drafts template or a real Fact Find Summary of a client, so the first real run may need one fix.
- The folder-drop check (a quote PDF or signed LOA dropped into the client's folder) and pulling an attachment out of a reply email are still unproven text rules.
