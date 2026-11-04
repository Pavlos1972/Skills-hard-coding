**Publish in the same reply as any change, automatically.** Every republish carries the program's Last updated stamp (Athens time) and a new Change Log entry. A republish only happens because something changed, so every republish has an entry. Do not ask first.

**How.** Load the `artifact-design` skill first. Publish `out/board.html` with the Artifact tool as it is, titled exactly as the page's title (`<Client Name> - Pipeline`), to the board's own address when one exists. Read the published page back, save it to a file and run `run.py publish`: the program compares it with the board it built. Then record `publish.result`.

**The page is a pure read-out.** Nothing on it is client- or Paul-editable: no buttons, no inputs, no self-save, no declared runtime capabilities. Every pending question is plain text in an amber banner and is answered in the chat. (On-page controls for Life Cover were tried once and reverted.)

**The page shows only what happened.** Actions Taken lines exist only with a receipt; the program refuses to verify a page that claims anything else.

**Conflicts.** If the republish is rejected because a newer version exists that you cannot read back, STOP and tell Paul. Never force-overwrite; force is acceptable only for confirmed disposable test data.

**The Change Log** is the last section: date (Athens), short point-form bullets naming the card and what happened, newest first. Past about 40 entries, those older than the most recent 15 fold under "Show earlier changes"; nothing is deleted.

**Out of scope for now.** AdviceTech sync (until Paul reconnects the AdviceTech connector and says it replaces this board) and the ClickUp build (the 77-field Client Card, about 30 automations and two dashboards are a separate system; this board borrows the decision logic only). Items not built yet: a Client Overview skill (note "Client Overview update - pending skill" on a card's Actions Taken wherever the Master Document calls for it); a quote-request drafting skill (draft directly, consistent with Paul's other provider correspondence); the Section 14 transfer sub-flow (flag it on the RA card); RA and Investments Servicing quote types (ask Paul the first time one comes up; do not guess a parallel structure); the timing of `client-review-notes` across several completed lines (ask Paul the first time); the EGAR proposal (still drafted by Paul).
