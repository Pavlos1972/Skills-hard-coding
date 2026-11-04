INVENTORY of the old skill: 983 sentences
  kept (word for word or nearly): 232
  reworded, with a recorded change: 577
  dropped, with a recorded decision: 174
  UNACCOUNTED: 0


REWORDED (each is covered by a recorded change):
- old line 85: Send/draft/ask logic for every client- or provider-facing email, referral, and calendar invite now lives in one place:
    now: its Identified list is exactly the documents WR needs from the client, gathered once across every product for one combined email, reconciled against the on-file check.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 85: Covers which items need Paul's go-ahead before Claude builds them, which build automatically, where each lands (Outlook Draft vs.
    now: Once Paul answers, Claude requests whatever's still needed and builds the comparison via life-insurer-comparison as soon as both sides are in hand.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 85: calendar event created directly), the Sitamah CC rule, the signature-deferral rule, and the Lizelle/BrightRock attachment exception.
    now: 2 | What a finished run contains | The board, the emails, the Sitamah messages, the check-in and the short audit |
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 85: Check it before drafting or sending anything — do not re-derive this logic per product line.
    now: print("\nSAY THIS TO PAUL FIRST, before anything else in your reply, in exactly these words:\n    %s.\n" % w.version_line())
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 86: Search Outlook for the last message in that thread first (mail from them, or mail we sent them) and create the draft with outlook_create_reply_all_draft on it.
    now: search Outlook for the last message in the thread first and create the draft with outlook_create_reply_all_draft.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 86: Note that editing the draft body afterwards can drop the quoted thread below the reply — re-check the draft.
    now: Editing the body afterwards can drop the quoted thread:
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 86: Paul sometimes sends the draft himself:
    now: "shown to Paul in the same reply as the board;
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 86: check Sent Items before telling Sitamah to send it, and don't ask her to send something already sent (ask her to chase instead).
    now: Check Sent Items before telling Sitamah to send something Paul may already have sent (ask her to chase instead).
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 87: Paul only does Teams meetings with clients.
    now: Client meetings are Teams meetings only.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 87: Paul lives and works in Greece;
    now: # ---- Athens time and the Greek time of an appointment (Paul lives in Greece;
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 87: clients, Sitamah and the office are in South Africa.
    now: the office is in South Africa, SAST = UTC+2 all year)
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 87: In summer Greece is 1 hour ahead of SA;
    now: for i, m in enumerate(msgs, 1):
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 87: Appointment times are always written SA time first, with Greek time in brackets for Paul only — e.g.
    now: The page shows it SA time first with the Greek time in brackets, for Paul only.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 87: 4pm (5pm) — so he doesn't get confused.
    now: """'4pm (5pm)' style for Paul only:
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 87: Never mention Paul's Greece location to a client, and never put the bracketed Greek time in anything a client sees (client invites are in SA time only).
    now: never mention Paul's location to a client and never put a bracketed Greek time in anything a client sees.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 89: Nothing else — no timestamped log, no restated facts, no stage code or stepper.
    now: No stage code, stepper or timestamped log is shown.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 89: Internal stage codes (LC-1, RA-2, etc.
    now: no stage codes, no internal jargon.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 89: — see the relevant playbooks/*.md file) drive what Claude does behind the scenes but are never shown.
    now: > Loaded from playbooks/rgar-egar.md, referenced by the core SKILL.md.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 89: The one exception is the New Business/Servicing tag (see below) — that does show.
    now: A new line gets the New Business / Servicing question immediately.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 90: Actions Taken is always Claude's own action, always multiple short bullets — never one merged sentence.
    now: Actions Taken is always Claude's own action and never restates an Identified fact.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 90: One fact per bullet, always.
    now: more than one fact in one bullet (one fact per bullet)" % label)
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 90: Every Actions Taken block carries a small CLAUDE badge (.claude-tag, styled off the Prospect-log claude color tokens) next to its label, on every card.
    now: add(html.count('class="claude-tag"') == n_act, "Every Actions Taken label carries the CLAUDE badge (%d)" % n_act)
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 92: Every Fact Find this board processes (intake, servicing re-look, or any transcript-driven update) must produce all three mandatory outputs before the job is done — a request that only names one ("summ
    now: Whenever a Fact Find is processed, all three outputs are delivered together in the same turn:
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 93: Fact Find Transcript, as a PDF (e.g.
    now: ["fact_find_summary", "fact_find_transcript", "policy_schedule", "quote", "statement", "other"],
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 93: Fact Find Transcript - 01.09.26 - (Client Name).pdf) — via ff-population-transcript (Word is the internal working format;
    now: the Fact Find Transcript PDF (ff-population-transcript), the Fact Find Summary PDF (fact-find-summary) and the Planner / AdviceTech note (client-teams-transcript-skill).
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 93: PDF is the delivered/saved output, never the .docx).
    now: that belongs only on the saved template, never on a real draft" % tag)
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 94: Fact Find Summary, as a PDF (e.g.
    now: Attach the client's Fact Find Summary PDF from {folder}", "3.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 94: Client_Name_Fact_Find_Summary - 01.09.26.pdf) — via fact-find-summary.
    now: Attach the client's Fact Find Summary PDF from {folder}", "3.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 95: Summarized Planner/AdviceTech Notes — plain chat text, via client-teams-transcript-skill, in ff-population-transcript's fixed 6-part structure (Meeting / Met / What They Currently Have / What They Req
    now: Zapier list_dynamic_enum_values (tool_name microsoft_teams_send_chat_message, property_name chat, search \"%s\") and take the 1:1 chat:\n  %s\n  (label %s) - never a meeting chat." % (s["name"], s["ch
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 95: (A follow-up appointment's transcript summary from client-teams-transcript-skill is what planner-interim-procedure pastes into the Task Chat.)
    now: once the transcript is uploaded run client-teams-transcript-skill and read it against every open line.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 96: All must be delivered together via present_files/chat in the same turn.
    now: Whenever a Fact Find is processed, all three outputs are delivered together in the same turn:
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 96: This board defers to fact-find-summary's own Mandatory rule rather than duplicating it.
    now: "Register every document a point of the board will quote (the Fact Find Summary first):
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 97: No transcript-derived field may be marked "Not discussed" without an actual re-check of the transcript.
    now: No field taken from a transcript may be marked "Not discussed" without an actual re-check of the transcript (see fact-find-summary's transcript-accuracy rule).
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 97: Hard rule — see fact-find-summary's "Mandatory:
    now: Please see attached Fact Find Summary for this client.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 97: transcript accuracy" section (re-search by keyword, read the full surrounding exchange, use a figure corrected live on the call over a first guess, flag genuine ambiguity rather than silently resolvin
    now: Paul said there is no board yet, and the search for one is logged" if (st.get("base") or {}).get("said") else "A first board needs Paul's words")
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 97: Applies to all three mandatory outputs.
    now: *The three outputs (every Fact Find processed).
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 98: This is a draft skill under active correction.
    now: '%s' is not a skill this board hands over to" % (who, via))
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 98: A live correction from Paul is authoritative over anything written here — note it in chat and prompt Paul to update this file via a skill proposal;
    now: A live correction from Paul is authoritative:
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 98: Claude cannot save skill files directly.
    now: Never say "I cannot access your files" without a log of all three.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 100: The board's display is always kept current, automatically, without asking.
    now: The board's primary job is document and email creation, not stage narration.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 100: Republish in the same reply as any state change.
    now: "published in the same reply as any change;
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 100: a genuine version conflict this session can't read back — that's a blocker, ask Paul.
    now: If the republish is rejected because a newer version exists that you cannot read back, STOP and tell Paul.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 101: Every email defers to paul-email-signature — never write a "Kind regards" sign-off into the body.
    now: the Exchange rule adds Paul's signature once (paul-email-signature);
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 101: Paul's real signature is applied automatically, server-side, by an Exchange Online transport rule keyed off the X-AI-Generated header, which Microsoft Graph stamps only on drafts created via the nativ
    now: if not (okap and es.get(e["id"], {}).get("ok") and tool in ("outlook_create_draft", "outlook_create_reply_all_draft", "outlook_create_reply_draft", "outlook_send_mail", "outlook_send_draft")
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 101: Every drafted email's body ends with the message content only — "Thanks," or nothing is fine, no typed signature block.
    now: end with the content, "Thanks," or nothing.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 101: The Zapier microsoft_office_365_* tools are confirmed unsuitable for Paul's email generally (not just attachments) — never use them;
    now: built by the chat, shown complete, sent after Paul's yes), not part of General's consolidated email.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 101: use only the native M365 tools listed above.
    now: drafts saved or emails sent only after his yes, with the native Microsoft 365 tools",
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 101: A separate, calendar-specific transport rule covers Teams meeting invites — a Teams meeting invite created via outlook_create_event doesn't carry the X-AI-Generated header (Graph's calendar /events en
    now: Once sent, Sitamah gets a Teams message with no "watch for a reply" ask — Cameron contacts the client directly, so there's nothing for her to do but be told it happened.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 101: Confirmed working end to end, logo included.
    now: "If confirmed, tell Paul in one short line:
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 101: See paul-email-signature and teams-meeting-setup-skill for the full mechanism.
    now: the event is created directly by teams-meeting-setup-skill after Paul's yes.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 102: Template library in Outlook Drafts — this is the mechanism for every provider referral, not a bespoke skill per insurer.
    now: Every request to an insurer or provider contact about a client is a reply to the most recent email in the mailbox to or from that contact about that client, never a fresh email:
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 102: Before building any provider/insurer-facing request, check Drafts for an existing template tagged [RECIPIENT-TAG - CATEGORY DESCRIPTION] - {Client Name} / {short description} (e.g.
    now: Before building any provider request, check Outlook Drafts for an existing template tagged [RECIPIENT-TAG - CATEGORY DESCRIPTION] - {Client Name} / {short description} (for example [ALWYN - RGAR - RET
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 102: [ALWYN - RGAR - RETIREMENT GOAL ANALYSIS REPORT NEEDED], [CAMERON - SHORT TERM INSURANCE REQUEST EMAIL], [VALERIE - MEDICAL AID REFERRAL], [AMBER - WILL / CAPITAL LEGACY REFERRAL]) for that recipient 
    now: {"op":"add_line","line":"life_cover|retirement_annuity|investments|rgar|egar|medical_aid|will|short_term"} a product line is created from the Fact Find's real values, or later when Paul reports a new 
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 102: If none exists, source the format from a precedent email in Inbox/Sent (typically one Sitamah sent to that recipient) and save the new draft under the same convention as the template for next time.
    now: If none exists, take the format from a precedent email in Inbox or Sent (typically one Sitamah sent) and save the new draft under the same convention.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 102: Paul explicitly ruled out building a standalone skill per provider (as was done once, before this convention was fully leaned on, for cameron-short-term-skill) — too time-consuming for too little payo
    now: Paul ruled out a standalone skill per provider (04/09/2026), except Cameron.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 102: New provider-specific behavior belongs directly in the relevant playbooks/*.md file, compiled from this template library, not in a new skill file, unless Paul explicitly asks for one.
    now: Referral to Valerie | Auto-built, chat-approved, then Claude-sent directly — built inline in this board from the Drafts template library, not a standalone skill (Paul's decision).
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 102: a quote-type request to an insurer (Life Cover/RA/Investments/RGAR/EGAR) CCs Sitamah only;
    now: The New Business / Servicing tag shows on Life Cover, RA and Investments only, and Paul gives it.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 102: a referral-type request that Claude sends directly (STI/Medical Aid/Will) CCs the client, Sitamah, and Paul;
    now: Actions Taken logs the request once sent, and — for a Lizelle request — logs that Sitamah was asked to attach and send.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 102: a proposal draft (client-facing) CCs Sitamah only — client is the To.
    now: auto-draft the client-facing RGAR proposal via rgar-skill, HTML body, straight to Outlook Drafts.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 103: The bracket-tag subject is for the saved template only — never on the real, client-specific draft.
    now: that belongs only on the saved template, never on a real draft" % tag)
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 103: The tagged subject exists so Paul can search Drafts for a reference example;
    now: if none exists, save two drafts (the tagged template, never sent, and the real one).
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 103: it must never reach a recipient or cc'd client.
    now: Use whenever a client or prospect is being worked through the sales or review pipeline."
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 103: The real draft always gets a plain, professional subject (e.g.
    now: the real draft always gets a plain, professional subject (the program refuses a bracket).
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 103: "[Client Name] / Retirement Goal Analysis Report needed"), no bracket prefix.
    now: name, ID, cell number, and email — never ID alone), no upfront question.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 103: If a template already exists for that recipient category, only the plain-subject real draft needs creating.
    now: If a template exists, only the plain-subject real draft is needed;
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 103: If none exists yet, save two drafts:
    now: if none exists, save two drafts (the tagged template, never sent, and the real one).
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 103: the tagged template (kept permanently, never sent) and the plain-subject real draft.
    now: If a template exists, only the plain-subject real draft is needed;
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 104: Where a decision depends on a document WR doesn't yet have (Group Risk Benefit Statement, existing policy schedule, RA/Pension statement, POI, investment statement), request it via General and keep th
    now: Where a decision depends on a document WR does not yet have (Group Risk Benefit Statement, existing policy schedule, RA or pension statement, proof of income, investment statement), request it through
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 105: General's Identified list is exactly the documents WR needs *from the client*, gathered once across every product for one combined email.
    now: its Identified list is exactly the documents WR needs from the client, gathered once across every product for one combined email, reconciled against the on-file check.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 105: A product card never asks the client for a document on its own Identified/Actions Taken — only requests to the insurer/provider (quote, report, referral, application, proposal).
    now: a product card never asks the client for a document, only the insurer or provider (quote, report, referral, application, proposal).
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 105: A document specific to one product can still route through General if it's client-facing — General is the one section that emails the client.
    now: A document specific to one product still goes through General if it is client-facing.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 106: New Business vs Servicing — Life Cover, RA, and Investments lines only.
    now: The New Business / Servicing tag shows on Life Cover, RA and Investments only, and Paul gives it.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 106: The moment one of these three line types is created, ask directly:
    now: continue                                  # the Artifact tool (reading the published board) is not one of the three file routes
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 106: RGAR/EGAR/Medical Aid/Will/STI never carry this tag (referrals/reports, not policies).
    now: RGAR, EGAR, Medical Aid, Will and Short-Term never carry the tag.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 106: A client can have lines of both kinds open at once.
    now: '%s' must be a list of lines naming the contact and what is outstanding" % (tid, k))
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 106: This flag decides which quote types get requested (Servicing FNA/Shortfall/Alternative per wr-sroa-builder's categories, vs.
    now: The tag decides the quote types and the document the line ends in (wr-roa-builder or wr-sroa-builder).
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 106: new-business FNA/Reduced/Standard) and which document the line ends in (wr-roa-builder vs wr-sroa-builder) — see the relevant playbooks/*.md file and "ROA vs SROA" below A Servicing line still starts 
    now: New Business -> wr-roa-builder (it needs the FNA Quote, the Reduced or Accepted Quote if it differs, the Fact Find Summary and a confirmed ROA date, which that skill asks for);
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 108: AdviceTech (AT) integration is out of scope for now.
    now: *Out of scope for now.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 108: Note where AT would eventually pick something up (see Deferred).
    now: Showing where it is up to.")
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 108: MS Planner is the interim stand-in (see the Planner ground rule above) and goes away when Paul says AdviceTech is permanent.
    now: it builds the invite, shows it to Paul, and sends it only after his yes (the client is emailed when it is created).
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 109: Sitamah gets a Teams message on every instance, in addition to her email CC.
    now: Sitamah Nathoo (admin@liferisk.co.za) is on the Cc line of every drafted or sent email.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 109: More is better here, not scoped to milestones only — see sitamah-messaging.md.
    now: "Every Teams message to Sitamah (sitamah-messaging.md) as data.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 109: If the native M365 Teams send fails with a missing ChatMessage.Send scope, use the Zapier Teams connector (microsoft_teams_send_chat_message, property content) — that is the route this board's Sitamah
    now: If the native Teams send fails for a missing scope, Zapier is the route.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 110: Outstanding requests are tracked automatically, not left to memory.
    now: do not rebuild from memory.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 110: The moment a provider/insurer-facing request goes out, log it against that product line — see outstanding-tracking.md.
    now: Log every outbound request against its product line the moment it goes out.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 111: Saving a found document — route by whether it's live or scheduled.
    now: %s, each found through a logged route and unchanged" % (len(log), ", ".join(sorted(docs["docs"])) or "none") if okacc else
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 111: While Paul's in this chat with his computer linked:
    now: the chat does, after Paul's yes, with exactly what the program printed or wrote.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 111: save via the device bridge to his local OneDrive (Paul - liferisk.co.za → Company → WR Clients → [Client] → [Subfolder] for an existing client, Company - Paul → New Business → [Client] for a prospect 
    now: (a) request a fresh like-for-like quote from the client's current insurer to compare directly against their existing policy, or (b) compare the new insurer's proposal (e.g.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 111: For an unattended scheduled check:
    now: an email sent that needs a reply watched for;
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 111: save via the Microsoft 365/SharePoint connector instead (same library, syncs on its own).
    now: "the Microsoft 365 connector (SharePoint / OneDrive)",
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 111: sharepoint_upload_file caps at 1MB per file — flag to Paul rather than silently fail on a larger scan.
    now: sharepoint_upload_file caps at 1 MB per file:
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 112: Pulling a file out of an email attachment is not yet confirmed to work — no dedicated attachment-download tool in the mailbox connector.
    now: Claude cannot attach a real file to a draft or a sent email (the tools have no attachment field, and the Zapier file field only takes a public URL;
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 112: First real case is the test;
    now: The first real run is Paul's.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 112: tell Paul plainly whether it worked.
    now: tell Paul plainly whether it worked, and fall back to asking him or Sitamah to save it.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 112: ask Paul to save/forward the attachment himself.
    now: RA and Investments Servicing quote types (ask Paul the first time one comes up;
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 113: ClickUp-specific plumbing is out of scope.
    now: *Out of scope for now.
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 113: The Master Context Document's 77-field ClickUp Client Card, ~30 automations, and two dashboards are a separate system build.
    now: AdviceTech sync (until Paul reconnects the AdviceTech connector and says it replaces this board) and the ClickUp build (the 77-field Client Card, about 30 automations and two dashboards are a separate
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 113: This board borrows the Master Doc's decision logic for accuracy, not to replicate ClickUp.
    now: this board borrows the decision logic only).
    why: Each rule is in the page where it is used and, where provable, a program check.
- old line 117: Product | Provider / Contact | What's requested there |
    now: a request to a provider contact is a reply to the latest thread:
    why: Contacts are typed once and the program fills To and Cc.
- old line 119: Life Cover | BrightRock — Lizelle Cachado, Lizelle.Cachado@brightrock.co.za (default;
    now: "Lizelle.Cachado@brightrock.co.za", "role":
    why: Contacts are typed once and the program fills To and Cc.
- old line 119: another insurer only if the FF names one, or Paul answers the chat insurer question with a different pick) | FNA / Shortfall / Reduced / Standard quotes (New Business) or Servicing FNA / Shortfall / A
    now: "Life Cover quote request (FNA / Shortfall / Reduced / Standard, or the Servicing types)",
    why: Contacts are typed once and the program fills To and Cc.
- old line 119: Needs the client's Fact Find Summary PDF attached — Claude still can't attach it, so the draft carries a note line and Sitamah completes the send (see send-decision-rules.md → the Lizelle/BrightRock a
    now: A quote request that needs the client's Fact Find Summary attached follows Step 1 and 2 (ask first, Outlook Draft) with one added line immediately before the closing urgency sentence:
    why: Contacts are typed once and the program fills To and Cc.
- old line 119: A re-quote/Revised Quote request on a client who already has Lizelle quotes is a reply-all to the last email in that thread (see Ground rules) and does not need the FF Summary line.
    now: A re-quote or Revised Quote request on a client who already has quotes is a reply-all to the last thread and does not need the line (revised_quote).
    why: Contacts are typed once and the program fills To and Cc.
- old line 120: Retirement Annuity | Old Mutual — Alwyn, alwyn.vantonder@oldmutual.com (default;
    now: "alwyn.vantonder@oldmutual.com", "role":
    why: Contacts are typed once and the program fills To and Cc.
- old line 120: another provider only if the FF names one) | Monthly and/or Lump Sum RA quotes — auto-draft:
    now: Standard quote from another insurer only if the FF names one outright — no question needed.
    why: Contacts are typed once and the program fills To and Cc.
- old line 121: RGAR | Old Mutual — Alwyn, alwyn.vantonder@oldmutual.com | Retirement Goal Analysis Report — auto-draft:
    now: "alwyn.vantonder@oldmutual.com", "role":
    why: Contacts are typed once and the program fills To and Cc.
- old line 121: yes, once RA/Pension statements are on file.
    now: need = settings()["on_file_folders"]
    why: Contacts are typed once and the program fills To and Cc.
- old line 121: Proposal to the client, once the report is back — auto-draft:
    now: a Claude-drafted proposal (Investment, RA, Tax-Free, RGAR) once the source quote or report is on file;
    why: Contacts are typed once and the program fills To and Cc.
- old line 121: yes (Claude-drafted, see Ground rules) |
    now: A Claude-drafted proposal and the RGAR request are auto lines:
    why: Contacts are typed once and the program fills To and Cc.
- old line 122: Investments | Old Mutual | Tax-Free Savings and/or General Investment quotes — auto-draft:
    now: "Investments quote request to Old Mutual (Tax-Free and/or General Investment)",
    why: Contacts are typed once and the program fills To and Cc.
- old line 122: Proposal to the client, once the quote is back — auto-draft:
    now: Proposal — Claude-drafted | Once the quote is back, auto-draft the client-facing proposal via om-optimal-ra-proposal, HTML body, straight to Outlook Drafts.
    why: Contacts are typed once and the program fills To and Cc.
- old line 122: yes (Claude-drafted, see Ground rules) |
    now: A Claude-drafted proposal and the RGAR request are auto lines:
    why: Contacts are typed once and the program fills To and Cc.
- old line 123: EGAR | Old Mutual — Alwyn, alwyn.vantonder@oldmutual.com | Education Goal Analysis Report — always a separate email from any RGAR request |
    now: "EGAR request to Old Mutual (always separate from any RGAR request, one per child)",
    why: Contacts are typed once and the program fills To and Cc.
- old line 124: Medical Aid | Valerie Swanepoel, valeries@hampshireind.co.za (also cc/to Hampshire intake, jhbhealthadmin@hampshireind.co.za) | Referral — review or new broker introduction — built automatically from 
    now: Valerie Swanepoel, valeries@hampshireind.co.za (also cc jhbhealthadmin@hampshireind.co.za).
    why: Contacts are typed once and the program fills To and Cc.
- old line 125: Will | Capital Legacy — Amber Strydom, amber@capitallegacy.co.za | Referral / broker-of-record takeover — built automatically from the Drafts template library, presented in chat for Paul's approval, t
    now: Referral to Capital Legacy | Auto-built, chat-approved, then Claude-sent directly — built inline in this board from the Drafts template library, not a standalone skill (Paul's decision).
    why: Contacts are typed once and the program fills To and Cc.
- old line 126: Short-Term Insurance | Cameron Maritz, cameron@visioninsure.co.za | Referral per the FF's exact instruction — built automatically via the standalone cameron-short-term-skill, presented in chat for Pau
    now: Referral to Valerie | Auto-built, chat-approved, then Claude-sent directly — built inline in this board from the Drafts template library, not a standalone skill (Paul's decision).
    why: Contacts are typed once and the program fills To and Cc.
- old line 127: Leads | DNR Marketing (mwpalwyn@mweb.co.za) | Lead source, not a request destination |
    now: "lead source, never a request destination"}
    why: Contacts are typed once and the program fills To and Cc.
- old line 128: All emails (client- and provider-facing) | Sitamah Nathoo — admin@liferisk.co.za | CC on every drafted or sent email this board produces (Cameron/STI, Valerie/Medical Aid, and Amber/Will also CC Paul 
    now: Sitamah Nathoo (admin@liferisk.co.za) is on the Cc line of every drafted or sent email.
    why: Contacts are typed once and the program fills To and Cc.
- old line 129: Sitamah — Teams | Sitamah Nathoo, via Microsoft Teams (Zapier connector) | Direct-messaged on every Actions Taken instance, every Paul-reported milestone, and every actually-sent email — see sitamah-m
    now: *Teams messages to Sitamah (Sitamah Nathoo, the 1:1 chat, through Zapier only, format markdown, after Paul's yes and the checked emails).
    why: Contacts are typed once and the program fills To and Cc.
- old line 129: Resolve her chat once via list_dynamic_enum_values on microsoft_teams_send_chat_message's chat property (or members on microsoft_teams_create_chat_and_send_message the first time) and reuse it.
    now: Resolve her chat once with list_dynamic_enum_values on microsoft_teams_send_chat_message's chat property and reuse it.
    why: Contacts are typed once and the program fills To and Cc.
- old line 133: *Prospect (client-level) — a short log of contact/booking activity.
    now: {"op":"prospect_log","date":"DD/MM/YYYY","text":".."} the short contact and booking log.
    why: The card shapes are checked by the program.
- old line 133: For a brand-new prospect this is a genuine intake log;
    now: is this a brand-new prospect, or an existing client?
    why: The card shapes are checked by the program.
- old line 133: for an existing client this section still appears but is labeled "Existing Client" rather than omitted.
    now: an existing client's is labelled "Existing Client".
    why: The card shapes are checked by the program.
- old line 133: No Identified/Actions Taken shape here — just a simple entry log.
    now: No pending question, no Actions Taken.
    why: The card shapes are checked by the program.
- old line 135: *Fact Find (client-level) — Identified only.
    now: add(set(ff) <= {"identified", "next_appointment"}, "The Fact Find card holds Identified only (and the next appointment)")
    why: The card shapes are checked by the program.
- old line 135: One plain point-form list of what the FF actually says, product by product.
    now: Identified only (what the form actually says, product by product, plus the confirmed follow-up date).
    why: The card shapes are checked by the program.
- old line 135: No "needed" split, no per-fact log entries, no Actions Taken on this card.
    now: | These document needs go on General, not this card.
    why: The card shapes are checked by the program.
- old line 135: Also captures the confirmed follow-up/2nd appointment date, if set — see "Follow-up appointment tracking" below.
    now: See "Follow-up appointment tracking" above.
    why: The card shapes are checked by the program.
- old line 137: *General (client-level, sits right after Fact Find) — the one section that talks to the client about documents:
    now: the one section that talks to the client about documents;
    why: The card shapes are checked by the program.
- old line 138: Before writing Identified, check what's already on file.
    now: Do not put anything on the client ask that is already signed or on file;
    why: The card shapes are checked by the program.
- old line 138: Look in the client's OneDrive folder, subfolders "3.
    now: Look in the client's folder, subfolders 3.
    why: The card shapes are checked by the program.
- old line 138: Policy Schedules" (device bridge, see /topics/tools.md) — 6.
    now: Policy Schedules (the last is mandatory:
    why: The card shapes are checked by the program.
- old line 138: Policy Schedules is mandatory, not optional (an existing RA statement has been missed there before).
    now: an existing RA statement has been missed there before).
    why: The card shapes are checked by the program.
- old line 138: Open each candidate PDF rather than trusting the filename — an MSIGN-signed document carries audit-trail pages (signer, completion date) that confirm it;
    now: an MSIGN-signed document carries audit-trail pages (signer, completion date);
    why: The card shapes are checked by the program.
- old line 138: a filename saying "signed" alone is not proof, and a same-named file with no audit trail is likely still the blank template.
    now: a file called "signed" with no audit trail is probably still the blank template.
    why: The card shapes are checked by the program.
- old line 138: Corrected 2026-09-16 — a password-protected statement is logged as found-but-locked, and Claude does not ask the client for the password.
    now: A password-protected statement is logged as found-but-locked:
    why: The card shapes are checked by the program.
- old line 138: Instead, message Sitamah (Action needed — see sitamah-messaging.md) that Claude needs access to check that policy schedule, and ask her to re-save it in the client's OneDrive folder without password p
    now: The moment the client's current policy schedule is saved to their OneDrive folder, ask Paul directly which comparison approach to take:
    why: The card shapes are checked by the program.
- old line 138: Anything confirmed on file goes in Identified, not the client ask (e.g.
    now: Anything not on this list is ask_first.",
    why: The card shapes are checked by the program.
- old line 138: "LOA + Disclosure — both on file, signed [dates].
    now: no Astute report until signed LOA back).
    why: The card shapes are checked by the program.
- old line 138: Anything on file but stale (POI/proof of address older than ~3 months) is logged as on file *and* flagged for a refresh.
    now: A password-protected statement is logged as found-but-locked:
    why: The card shapes are checked by the program.
- old line 138: A genuinely absent item goes on the ask normally.
    now: Ask only if the title genuinely does not make it clear.
    why: The card shapes are checked by the program.
- old line 139: every document the FF shows WR doesn't yet have, from every product, gathered into one list, reconciled against the OneDrive check above.
    now: its Identified list is exactly the documents WR needs from the client, gathered once across every product for one combined email, reconciled against the on-file check.
    why: The card shapes are checked by the program.
- old line 140: the single question — "Ready to send [Client] one email for [documents]?" — until Paul answers.
    now: Pending is the single question "Ready to send [Client] one email for [documents]?";
    why: The card shapes are checked by the program.
- old line 141: the moment Paul says yes, in the same reply, draft the consolidated email and save it to Outlook Drafts:
    now: when Paul says yes, in the same reply draft the consolidated email (To the client, Cc Sitamah, a plain list of documents, no typed sign-off) and save it to Outlook Drafts.
    why: The card shapes are checked by the program.
- old line 141: To the client's FF-captured email, CC Sitamah.
    now: the table's, that a referral email carries the client's full details block, that the Sitamah messages follow the tier rules.
    why: The card shapes are checked by the program.
- old line 141: Body lists the documents plainly.
    now: "Find the board, find the documents, log every try",
    why: The card shapes are checked by the program.
- old line 141: Corrected 2026-09-16 — the LOA/Disclosure signature request is no longer part of this email;
    now: The LOA signature request is NOT part of it.
    why: The card shapes are checked by the program.
- old line 141: it's its own dedicated auto-built, chat-approved, Claude-sent line (see core-ff-intake.md → LOA/Astute sequencing gate) — General's consolidated email covers the other client documents only (policy sc
    now: Referral to Capital Legacy | Auto-built, chat-approved, then Claude-sent directly — built inline in this board from the Drafts template library, not a standalone skill (Paul's decision).
    why: The card shapes are checked by the program.
- old line 141: Corrected 2026-09-16 — the moment the draft is saved, message Sitamah (Action needed, see sitamah-messaging.md):
    now: "Every Teams message to Sitamah (sitamah-messaging.md) as data.
    why: The card shapes are checked by the program.
- old line 141: she checks it and sends it herself if correct, and follows up with the client periodically before the next appointment.
    now: General's consolidated email drafted (check it, send it if correct, follow up with the client periodically before the next appointment);
    why: The card shapes are checked by the program.
- old line 141: This replaces Paul as the one who sends General's consolidated email — he's still CC'd and can see it, but Sitamah owns the actual send here.
    now: when Paul says yes, in the same reply draft the consolidated email (To the client, Cc Sitamah, a plain list of documents, no typed sign-off) and save it to Outlook Drafts.
    why: The card shapes are checked by the program.
- old line 141: Clear the pending question and log what was drafted as separate short bullets (e.g.
    now: This board's job is just to trigger the skill, surface its approval question, and log the result once sent.
    why: The card shapes are checked by the program.
- old line 141: "Document-request email drafted, saved to Outlook Drafts.
    now: "Investment proposal drafted ([skill used]), saved to Outlook Drafts.
    why: The card shapes are checked by the program.
- old line 141: To [Client], CC Sitamah.", "Requests:
    now: Actions Taken logs the confirmed send, CC'd to client + Sitamah + Paul.
    why: The card shapes are checked by the program.
- old line 141: [documents].", "Sitamah asked to check, send, and follow up.").
    now: The messages to Sitamah (Action needed, and one FYI), posted once through Zapier after his yes, and the same-day check-in for a follow-up appointment.
    why: The card shapes are checked by the program.
- old line 143: *Product lines (Life Cover, Retirement Annuity, Investments, RGAR, EGAR, Medical Aid, Will, Short-Term Insurance) — created from the Fact Find, one card per product need, each the same shape:
    now: {"op":"add_line","line":"life_cover|retirement_annuity|investments|rgar|egar|medical_aid|will|short_term"} a product line is created from the Fact Find's real values, or later when Paul reports a new 
    why: The card shapes are checked by the program.
- old line 144: New Business/Servicing tag (Life Cover, RA, Investments only):
    now: The New Business / Servicing tag shows on Life Cover, RA and Investments only, and Paul gives it.
    why: The card shapes are checked by the program.
- old line 144: the one internal flag that *does* show on the board — set by asking Paul directly the moment the line is created.
    now: {"op":"tag","line":"life_cover","tag":"New Business|Servicing","paul_said":".."} for Life Cover, RA and Investments only, the moment the line is created.
    why: The card shapes are checked by the program.
- old line 144: RGAR/EGAR/Medical Aid/Will/STI never carry it.
    now: RGAR, EGAR, Medical Aid, Will and Short-Term never carry the tag.
    why: The card shapes are checked by the program.
- old line 145: numbered, short — what the FF says this product needs, including any provisional/unclear item flagged plainly (e.g.
    now: Identified only (what the form actually says, product by product, plus the confirmed follow-up date).
    why: The card shapes are checked by the program.
- old line 145: "Group Risk unclear — client not sure, see General for the statement request").
    now: A re-quote or Revised Quote request on a client who already has quotes is a reply-all to the last thread and does not need the line (revised_quote).
    why: The card shapes are checked by the program.
- old line 146: the single next question to the provider/insurer.
    now: Pending is the single question "Ready to send [Client] one email for [documents]?";
    why: The card shapes are checked by the program.
- old line 146: For Life Cover specifically, this is one combined question covering everything answerable right now (which insurer for FNA, plus — if GR is still unclear — whether to proceed with a Reduced Quote now 
    now: For Life Cover it is ONE combined question covering everything answerable right now (which insurer for the FNA, and, if Group Risk is unclear, whether to proceed with a Reduced Quote now on an FNA bas
    why: The card shapes are checked by the program.
- old line 146: RGAR and every Claude-drafted proposal are auto-draft lines — no pending question;
    now: A Claude-drafted proposal and the RGAR request are auto lines:
    why: The card shapes are checked by the program.
- old line 146: Claude drafts straight to Actions Taken.
    now: no pending question, straight to Actions Taken.
    why: The card shapes are checked by the program.
- old line 146: Short-Term Insurance, Medical Aid, and Will are auto-*built* but not silent — each one's pending question is the built email itself, waiting on Paul's chat approval to send (see playbooks/short-term-i
    now: {"op":"add_line","line":"life_cover|retirement_annuity|investments|rgar|egar|medical_aid|will|short_term"} a product line is created from the Fact Find's real values, or later when Paul reports a new 
    why: The card shapes are checked by the program.
- old line 147: numbered, short — quote request, drafted proposal, pre-filled application, submitted application, referral, policy issued, ROA/SROA.
    now: Application Prep | Pre-filled automatically ahead of the 2nd/3rd meeting, once quote + FF + proposal give enough (complete-applications-skill — RA recurring, RA lump sum/Section 14).
    why: The card shapes are checked by the program.
- old line 147: The running record of the product's journey;
    now: ["An RAR is required for {client}'s {product}, and the email is drafted in Outlook Drafts, subject:
    why: The card shapes are checked by the program.
- old line 147: appended as work happens, never restating an Identified fact as an action.
    now: Actions Taken is always Claude's own action and never restates an Identified fact.
    why: The card shapes are checked by the program.
- old line 149: A new product line is created either from a Fact Find or later when Paul reports a new need.
    now: {"op":"add_line","line":"life_cover|retirement_annuity|investments|rgar|egar|medical_aid|will|short_term"} a product line is created from the Fact Find's real values, or later when Paul reports a new 
    why: The card shapes are checked by the program.
- old line 153: The moment a follow-up/2nd (or later) appointment is confirmed — from the transcript or Paul directly — record it on the Fact Find card (e.g.
    now: The moment a follow-up (2nd or later) appointment is confirmed, from the transcript or from Paul, record it with followup and hand over to teams-meeting-setup-skill:
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 153: [date] [time]") and note it in chat.
    now: one fixed layout, the same every time, and NO script in it (a broken string
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 153: Times are SA time first with Greek time in brackets for Paul only (see Ground rules);
    now: The page shows it SA time first with the Greek time in brackets, for Paul only.
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 153: the client-facing invite is SA time only.
    now: General is client-facing only;
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 154: Set up the actual Teams meeting — delegate to teams-meeting-setup-skill.
    now: the Teams invite is built by teams-meeting-setup-skill;
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 154: The moment a follow-up date (and time) is confirmed, hand off to that skill rather than building the calendar event inline — it owns the subject/topic convention ({Client Name} / {short topics}), the 
    now: The moment a follow-up (2nd or later) appointment is confirmed, from the transcript or from Paul, record it with followup and hand over to teams-meeting-setup-skill:
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 154: That skill gates the actual outlook_create_event call on Paul's explicit go-ahead, shown as this card's pending question — creating the event sends the invite to the client immediately, since there's 
    now: Then Sitamah opens that draft, attaches the Fact Find Summary PDF from the client's folder, sends it and follows up with Lizelle for the quotes back (message lizelle_attach, a genuine action request).
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 154: Log the confirmed meeting and message Sitamah once it's actually sent, per that skill's own steps.
    now: Claude creates and sends the COC appointment invite (fixed 30-minute duration), then messages Sitamah (Action needed) that it's been sent, asking her to watch for acceptance.
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 154: (While the Planner interim applies, the Task's appointment checklist line stays … - TO BE SET ❓ until the invite is sent, then follows planner-interim-procedure.)
    now: ["The 30-minute COC appointment invite is sent for {when}.", "Please watch for the client's acceptance."]},
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 155: Schedule a same-day proactive check-in.
    now: print("  same-day check-in:
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 155: Use create_trigger/send_later (never the local in-session cron tools, which don't survive) to create a one-shot check-in bound to this chat, timed for the morning of the appointment date.
    now: A scheduled task bound to this chat (create_trigger / send_later, never the local in-session cron tools, which do not survive), timed for the morning of the appointment:
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 155: check Paul's Outlook calendar (outlook_calendar_search) — is it still on for today, still accepted by the client?
    now: msg = ("Check Paul's Outlook calendar (outlook_calendar_search) for %s's follow-up Teams meeting today at %s SAST.
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 155: — then message Paul in this chat:
    now: If Paul names a second client in the same chat, ask whether he wants a separate chat.
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 155: confirmed → short "confirmed — [Client] at [time] today;
    now: 'Confirmed - %s at %s today;
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 155: moved or not accepted → flag plainly and ask Paul rather than assuming it happened.
    now: "If it was moved or not accepted, say so plainly and ask Paul;
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 156: If Paul reports a move, cancel the existing check-in (delete_trigger) and use teams-meeting-setup-skill's outlook_update_event step to update the existing invite in place — never delete-and-recreate t
    now: a reschedule cancels the old same-day check-in first (receipt checkin.deleted), and the existing invite is updated, never recreated" % who)
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 157: Multiple product lines, one transcript.
    now: # General and the product lines
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 158: Read what actually happened and what's needed next, then either ask the specific follow-up question or take the next permitted action (drafting a proposal, pre-filling an application, flagging a count
    now: read what happened, then ask the specific follow-up question or take the next permitted action.
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 162: the board only ever shows current state — no record of what it said last week, and no single time-ordered view across cards of what happened when (a card's own Actions Taken is organized by product, n
    now: a Client Overview skill (note "Client Overview update - pending skill" on a card's Actions Taken wherever the Master Document calls for it);
    why: One entry per republish, set by the program.
- old line 162: This section is the fix, and it's genuinely new information, not a duplicate of Actions Taken — it's the same facts organized by *when*, with a real date attached, instead of by *which card*.
    now: A card is Identified (facts and needs from the Fact Find, short point form, no commentary), one pending question only when something awaits Paul, and Actions Taken (what Claude actually produced or se
    why: One entry per republish, set by the program.
- old line 163: its own section at the very bottom of the page, below every product card, titled "Change Log."
    now: the board as ONE data file, the changes the chat enters, the rules on every card, the change log,
    why: One entry per republish, set by the program.
- old line 164: One entry per republish, always — since a republish only ever happens because something changed (see Publishing), every republish gets an entry;
    now: A republish only happens because something changed, so every republish has an entry.
    why: One entry per republish, set by the program.
- old line 164: there's no "quiet" republish to filter out.
    now: %s has no question to clear" % (who, card_title(cd)))
    why: One entry per republish, set by the program.
- old line 165: the date (Athens time, same convention as "Last updated"), then one or more short point-form bullets — same brevity discipline as Actions Taken, one fact per bullet — naming which card(s) changed and 
    now: date (Athens), short point-form bullets naming the card and what happened, newest first.
    why: One entry per republish, set by the program.
- old line 165: Cross-reference, don't duplicate:
    now: %s%% is not in the document's text" % (label, t)
    why: One entry per republish, set by the program.
- old line 165: FNA quote drafted, sent to Lizelle" is enough;
    now: Actions Taken logs the request once sent, and — for a Lizelle request — logs that Sitamah was asked to attach and send.
    why: One entry per republish, set by the program.
- old line 165: the full detail stays on that card's own Actions Taken.
    now: Internal stage codes here are Claude's own reference — never shown to Paul on the board.
    why: One entry per republish, set by the program.
- old line 166: Newest entry at the top.
    now: # Change Log, at the very bottom
    why: One entry per republish, set by the program.
- old line 167: No cap under normal use — a client's full journey realistically runs to a few dozen entries, trivial as plain text.
    now: R.add(not ep and not np_, "%d email(s) follow the send table (To and Cc exactly the table's, plain subject, no sign-off, details block where needed);
    why: One entry per republish, set by the program.
- old line 167: If a long-running Active client's log genuinely passes ~40 entries (several review cycles), collapse everything older than the most recent ~15 under a native <details>/<summary> fold ("Show earlier ch
    now: Past about 40 entries, those older than the most recent 15 fold under "Show earlier changes";
    why: One entry per republish, set by the program.
- old line 168: Populated automatically, same as the rest of the board — no separate go-ahead;
    now: The read-back has no board data (state-data).
    why: One entry per republish, set by the program.
- old line 168: it's part of the same republish that updates the card(s) it's logging.
    now: the program checks its checksum and that it is this client's.
    why: One entry per republish, set by the program.
- old line 172: Boards and chats currently accumulate forever — there's no step that ever says "this one's done." Most clients never need this:
    now: card shapes and tags, one fact per bullet, word limits, no stage codes, that every Identified point carries a line that
    why: Never auto-closed; Paul's words and the cancelled check-ins are required.
- old line 172: an Active client's board stays open indefinitely, since new servicing needs and annual reviews keep creating new activity on the same board — that's the model working as intended, not something to clo
    now: Is [Client] fully closed out (NTU or Inactive), or should the board stay open?" If he says stay open, do not ask again until something changes materially.
    why: Never auto-closed; Paul's words and the cancelled check-ins are required.
- old line 172: Close-out is only for the two genuinely terminal cases, using Paul's own existing classification language (see the Master Context Document's Client Classification):
    now: a Client Overview skill (note "Client Overview update - pending skill" on a card's Actions Taken wherever the Master Document calls for it);
    why: Never auto-closed; Paul's words and the cancelled check-ins are required.
- old line 172: NTU (declined everything at prospect stage, no policy ever placed) and Inactive (was an active client, relationship has ended — no active policies, may re-engage later).
    now: Close-out is only for NTU (declined everything at prospect stage, no policy placed) and Inactive (the relationship has ended).
    why: Never auto-closed; Paul's words and the cancelled check-ins are required.
- old line 173: Never auto-close — always ask, once.
    now: when every open line is resolved, ask Paul once:
    why: Never auto-closed; Paul's words and the cancelled check-ins are required.
- old line 173: The moment every open product line on a board has resolved to either NTU/declined or Complete-with-nothing-further-expected, and the client-level question hasn't been asked yet, ask Paul directly:
    now: Every point on the board comes from a registered document (a verbatim line the program can find) or Paul's own words;
    why: Never auto-closed; Paul's words and the cancelled check-ins are required.
- old line 173: "Every line here is resolved — is [Client] fully closed out (NTU or Inactive), or should the board stay open?" If he says stay open (e.g.
    now: Is [Client] fully closed out (NTU or Inactive), or should the board stay open?" If he says stay open, do not ask again until something changes materially.
    why: Never auto-closed; Paul's words and the cancelled check-ins are required.
- old line 173: he expects to re-approach an NTU prospect later, or an Inactive client may return), don't ask again until something changes materially — don't re-ask on every subsequent republish.
    now: Is [Client] fully closed out (NTU or Inactive), or should the board stay open?" If he says stay open, do not ask again until something changes materially.
    why: Never auto-closed; Paul's words and the cancelled check-ins are required.
- old line 174: What close-out actually does, once Paul confirms:
    now: close-out cancels the client's scheduled check-ins first;
    why: Never auto-closed; Paul's words and the cancelled check-ins are required.
- old line 175: Add an unmistakable banner at the very top of the board:
    now: add(bool(board.get("closed")) == ('class="banner-closed"' in html), "The CLOSED banner shows if, and only if, the board is closed")
    why: Never auto-closed; Paul's words and the cancelled check-ins are required.
- old line 175: "CLOSED — [NTU / Inactive] — [date]" (Athens time).
    now: {"op":"close","status":"NTU|Inactive","paul_said":".."} see Close-out below.
    why: Never auto-closed; Paul's words and the cancelled check-ins are required.
- old line 176: Cancel any scheduled triggers still running for this client — the daily outstanding-request check (outstanding-tracking.md), any follow-up check-in — via delete_trigger.
    now: The messages to Sitamah (Action needed, and one FYI), posted once through Zapier after his yes, and the same-day check-in for a follow-up appointment.
    why: Never auto-closed; Paul's words and the cancelled check-ins are required.
- old line 176: A closed client shouldn't still be polling Outlook every day.
    now: A document or an Outlook thread cannot be found:
    why: Never auto-closed; Paul's words and the cancelled check-ins are required.
- old line 177: Add a final Change Log entry recording the close-out and the reason, same as any other entry.
    now: add(ent == len(board["change_log"]), "Every Change Log entry is on the page (%d)" % ent)
    why: Never auto-closed; Paul's words and the cancelled check-ins are required.
- old line 178: Republish with the banner — this is the one time a republish happens specifically *because* of a status change rather than a card update.
    now: If the republish is rejected because a newer version exists that you cannot read back, STOP and tell Paul.
    why: Never auto-closed; Paul's words and the cancelled check-ins are required.
- old line 180: Close-out means clearly marked and inactive, not gone — the history stays available if the client re-engages or the NTU decision gets revisited.
    now: Is [Client] fully closed out (NTU or Inactive), or should the board stay open?" If he says stay open, do not ask again until something changes materially.
    why: Never auto-closed; Paul's words and the cancelled check-ins are required.
- old line 182: ## Setting up a client's board
    now: %s follow-up %s" % (client_full(board), na["date"])
    why: The layout is drawn by the program from one template.
- old line 184: Expect this flow to keep getting corrected as it's actually used on live clients.
    now: the Section 14 transfer sub-flow (flag it on the RA card);
    why: The layout is drawn by the program from one template.
- old line 186: Read it off the chat title (Paul always names the client/prospect there).
    now: Read the client's name off the chat title (Paul always names the client or prospect there).
    why: One entry per republish, set by the program.
- old line 186: Only ask directly if the title genuinely doesn't make it clear.
    now: Ask only if the title genuinely does not make it clear.
    why: One entry per republish, set by the program.
- old line 187: The only question asked before Claude starts working.
    now: The ONLY question asked before work starts:
    why: One entry per republish, set by the program.
- old line 187: Both get the Prospect section — new prospect gets a genuine intake log, existing client gets it labeled "Existing Client." For a test run, see the Ground rule.
    now: Once sent, Sitamah gets a Teams message with no "watch for a reply" ask — Cameron contacts the client directly, so there's nothing for her to do but be told it happened.
    why: One entry per republish, set by the program.
- old line 188: Locate the 1st appointment transcript automatically — don't ask if it's ready.
    now: Search the client's folder for the 1st appointment transcript yourself, without asking first.
    why: One entry per republish, set by the program.
- old line 188: Search the client's OneDrive/SharePoint folder (Sitamah will have saved it there).
    now: [filename] - from the client's OneDrive folder, [subfolder].
    why: One entry per republish, set by the program.
- old line 188: If found, run Fact Find intake from it directly in the same reply.
    now: Whenever a Fact Find is processed, all three outputs are delivered together in the same turn:
    why: One entry per republish, set by the program.
- old line 188: Only ask Paul to upload it if it genuinely isn't in the folder.
    now: Ask only if the title genuinely does not make it clear.
    why: One entry per republish, set by the program.
- old line 189: Product lines are created automatically from the Fact Find's real values — no upfront question to identify them;
    now: The moment the FF confirms a Will need, build the complete referral automatically (no upfront question):
    why: One entry per republish, set by the program.
- old line 189: see Fact Find intake below.
    now: for cd in ["fact_find", "general"] + board["lines"]:
    why: One entry per republish, set by the program.
- old line 189: For each Life Cover, RA, or Investments line, as it's created, ask directly:
    now: Life Cover, RA and Investments quote requests (always ask which insurer and on what basis);
    why: One entry per republish, set by the program.
- old line 189: "Is this a new policy, or a servicing change to something [Client] already has?" RGAR/EGAR/Medical Aid/Will/STI don't get this question.
    now: "Is this a new policy or product, or a servicing change to something [Client] already has?" Never infer it from documents.
    why: One entry per republish, set by the program.
- old line 190: Build the board as a self-contained HTML page (load artifact-design first) and publish via the Artifact tool, titled "<Client Name> — Pipeline".
    now: "The client's pipeline board (a self-contained read-out page, published as the Artifact titled '<Client Name> - Pipeline')", "file":
    why: One entry per republish, set by the program.
- old line 191: client name/title + Last updated timestamp (Athens time, bumped every republish) + a summary strip.
    now: Every republish carries the program's Last updated stamp (Athens time) and a new Change Log entry.
    why: One entry per republish, set by the program.
- old line 191: Then Prospect (labeled per point 2).
    now: Prospect, Fact Find, General, one card per product line, Change Log.
    why: One entry per republish, set by the program.
- old line 191: Then Fact Find (Identified only, plus the follow-up appointment date once known).
    now: add(set(ff) <= {"identified", "next_appointment"}, "The Fact Find card holds Identified only (and the next appointment)")
    why: One entry per republish, set by the program.
- old line 191: Then General (Identified + pending + Actions Taken).
    now: Identified/pending/Actions Taken as above.
    why: One entry per republish, set by the program.
- old line 191: Then one card per product line, each carrying its New Business/Servicing tag (Life Cover/RA/Investments only) plus Identified + pending + Actions Taken.
    now: The New Business / Servicing tag shows on Life Cover, RA and Investments only, and Paul gives it.
    why: One entry per republish, set by the program.
- old line 191: Then, at the very bottom, the Change Log — see "Board change log" above.
    now: the page then shows "CLOSED - [status] - [date]" at the top, the Change Log gets its final entry, and the page is republished.
    why: One entry per republish, set by the program.
- old line 191: No internal stage code, pill, or stepper anywhere.
    now: shows an internal stage code" % label)
    why: One entry per republish, set by the program.
- old line 192: padding:0 1.5rem;}, card padding around 1.15rem 1.4rem 1.3rem.
    now: header{padding:1.6rem 0 .6rem}
    why: One entry per republish, set by the program.
- old line 192: Cap text-bearing elements at roughly max-width:78-80ch.
    now: ul{margin:.2rem 0 0;padding-left:1.25rem;max-width:80ch}
    why: One entry per republish, set by the program.
- old line 193: every card's "Actions Taken" label carries a small CLAUDE badge (.claude-tag — small-caps pill, --claude-ink text on --claude-soft background, matching the Prospect log's claude color tokens).
    now: add(html.count('class="claude-tag"') == n_act, "Every Actions Taken label carries the CLAUDE badge (%d)" % n_act)
    why: One entry per republish, set by the program.
- old line 194: Tell Paul the board is up, ask him to confirm the setup looks right before logging real events.
    now: This board's job is to hand over the right documents at the right point and to log the result.
    why: One entry per republish, set by the program.
- old line 194: One-time setup check only — display updates are automatic afterward, but content decisions still get asked per-card.
    now: one line per check with a green tick or a red cross, one closing line for what is only attested", "checked_by":
    why: One entry per republish, set by the program.
- old line 198: Bump "Last updated" every time, and add the corresponding entry to the Change Log (see "Board change log" above) in the same republish.
    now: add(ent == len(board["change_log"]), "Every Change Log entry is on the page (%d)" % ent)
    why: One entry per republish, set by the program.
- old line 199: The board is a pure read-out — nothing on it is client- or Paul-editable.
    now: nothing on it is client- or Paul-editable.
    why: One entry per republish, set by the program.
- old line 199: No advance/back buttons, no on-page controls, no self-save, no declared runtime capabilities.
    now: no buttons, no inputs, no self-save, no declared runtime capabilities.
    why: One entry per republish, set by the program.
- old line 199: Every pending question, on every card including Life Cover, is kind:"text":
    now: add(not bad, "Every pending question is plain text, at most one per card" if not bad else "Pending problem on %s" % ", ".join(bad))
    why: One entry per republish, set by the program.
- old line 199: a plain amber banner, answered by Paul in chat.
    now: Every pending question is plain text in an amber banner and is answered in the chat.
    why: One entry per republish, set by the program.
- old line 199: (On-page interactive controls for Life Cover were tried once and reverted — see the archived changelog, 2026-09-01 17:00 — and that holds for every question added since.)
    now: (On-page controls for Life Cover were tried once and reverted.)
    why: One entry per republish, set by the program.
- old line 200: if a republish is rejected because a newer version exists that this session can't read back, stop and tell Paul rather than force-overwriting.
    now: If the republish is rejected because a newer version exists that you cannot read back, STOP and tell Paul.
    why: One entry per republish, set by the program.
- old line 203: ## Fact Find intake (client-level, shared, repeatable)
    now: ff-population-transcript, fact-find-summary, client-teams-transcript-skill.
    why: Kept; the Fact Find skills own the reading.
- old line 205: Trigger — search first, don't wait to be given the transcript.
    now: The program's first lines give you one sentence to say to Paul before anything else:
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 205: Once Paul confirms new-prospect-vs-existing-client, search the client's OneDrive/SharePoint folder for the 1st appointment transcript.
    now: Search the client's folder for the 1st appointment transcript yourself, without asking first.
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 205: If found, run ff-population-transcript against it directly, without asking first.
    now: run ff-population-transcript on it directly (also for a later or servicing Fact Find).
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 205: Only ask Paul to upload it if it genuinely isn't in the folder.
    now: Ask only if the title genuinely does not make it clear.
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 205: Applies to a later/servicing Fact Find too.
    now: run ff-population-transcript on it directly (also for a later or servicing Fact Find).
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 206: Intake isn't complete until all three mandatory outputs exist — see the Ground rule above;
    now: Whenever a Fact Find is processed, all three outputs are delivered together in the same turn:
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 206: every transcript-derived field in each must be actually re-checked against the source transcript, not assumed.
    now: No field taken from a transcript may be marked "Not discussed" without an actual re-check of the transcript (see fact-find-summary's transcript-accuracy rule).
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 207: run fact-find-summary directly against it.
    now: run fact-find-summary on it directly.
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 207: This reuse path is only for a genuinely new prospect's intake — a Servicing line never takes this shortcut, it always runs a fresh Fact Find from a current transcript even if a completed FF already ex
    now: a Servicing line always runs a fresh, full Fact Find from a current transcript.
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 208: LOA/Astute sequencing gate (flagged IMPORTANT in the Master Doc):
    now: *LOA and Astute (sequencing gate).
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 208: Corrected 2026-09-16 — this is its own auto-built, chat-approved, Claude-sent line, not part of General's consolidated client document-request email (see send-decision-rules.md).
    now: built by the chat, shown complete, sent after Paul's yes), not part of General's consolidated email.
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 208: Before asking Paul to approve it:
    now: (1) before building it, does Paul need to decide first?
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 208: (1) locate the client's LOA and Disclosure templates in their OneDrive folder — via the device bridge to Paul's local OneDrive when he's linked — and pre-populate both with the client's details from t
    now: locate the client's LOA and Disclosure templates in their folder and pre-populate both from the Fact Find;
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 208: (2) tailor the LOA explanatory email from the standing template in Outlook Drafts, per the Template library convention;
    now: tailor the LOA email from the standing template in Outlook Drafts.
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 208: Ask Paul for the go-ahead in chat, same as Medical Aid/Will/STI;
    now: "shown to Paul in the same reply as the board;
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 208: once approved, Claude sends it directly.
    now: Referral to Cameron Maritz | Auto-built, chat-approved, then Claude-sent directly — delegated entirely to cameron-short-term-skill.
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 208: In the same reply, message Sitamah (Action needed) that the email's gone out and ask her to prepare the pre-populated LOA/Disclosure MSIGN signing pack and send it to the client via MSIGN.
    now: it messages Sitamah (Action needed) that the LOA is signed and saved, and asks her to draw the Astute report herself.
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 208: For a review/existing client, an LOA already on file covers this — no need to re-gate or re-send.
    now: A re-quote or Revised Quote request on a client who already has quotes is a reply-all to the last thread and does not need the line (revised_quote).
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 208: Once the LOA is signed and saved, Sitamah draws the Astute report herself — Claude notifies her (Action needed), it doesn't draw it (see playbooks/life-cover.md → Info Gathering for the worked step).
    now: it messages Sitamah (Action needed) that the LOA is signed and saved, and asks her to draw the Astute report herself.
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 209: Pull the FF's real field values (see "Reading a WR Fact Find's actual values" below) — never build Identified from page labels alone.
    now: build the email exactly as before, then insert the line Please see attached Fact Find Summary for this client.
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 210: Write the Fact Find card's Identified list directly from those values:
    now: add(set(ff) <= {"identified", "next_appointment"}, "The Fact Find card holds Identified only (and the next appointment)")
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 210: one line per product area, plain point form.
    now: One FYI message per run, in point form.
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 210: Also capture the confirmed follow-up appointment date if established and hand off to teams-meeting-setup-skill (per "Follow-up appointment tracking" above), same reply.
    now: {"op":"followup","date":"DD/MM/YYYY","time":"HH:MM","source":"..","via":"teams-meeting-setup-skill","receipt":"KEY"} the confirmed follow-up or 2nd appointment (South African time).
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 211: From the same values, work out General's Identified list and each product card's own Identified list, per the decision logic in the relevant playbooks/*.md file.
    now: its Identified list is exactly the documents WR needs from the client, gathered once across every product for one combined email, reconciled against the on-file check.
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 211: Do the OneDrive on-file check before finalizing General's list — don't put anything on the client ask that's already signed/on file;
    now: Do not put anything on the client ask that is already signed or on file;
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 212: A genuine contradiction in the FF should be rare if it's built accurately from the transcript — it should simply reflect what was actually discussed.
    now: A genuine contradiction should be rare.
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 212: Corrected 2026-09-16 — if one turns up anyway (required but unaffordable, or a Yes/No disagreeing with its own note), don't silently decide the outcome:
    now: If one turns up (required but unaffordable, or a Yes/No disagreeing with its own note), do not silently decide:
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 212: flag it on the Fact Find card and ask Paul directly what action to take, per the document-in-hand and provisional-field rules, rather than skipping the product line unasked.
    now: flag it on the Fact Find card and ask Paul what to do.
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 213: Existing clients can re-enter this intake for a later review — Fact Find's Identified list gets rewritten from the fresh FF;
    now: run ff-population-transcript on it directly (also for a later or servicing Fact Find).
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 213: General and product cards pick up new needs.
    now: # General and the product lines
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 213: A Servicing line's Fact Find is always this kind of fresh, full re-look.
    now: A Servicing line starts from a fresh, full Fact Find.
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 215: ### Reading a WR Fact Find's actual values
    now: A Servicing line starts from a fresh, full Fact Find.
    why: The provisional rule is kept; the form-reading technique belongs to ff-population-transcript.
- old line 216: The WR Fact Find is a fillable AcroForm PDF — plain text extraction returns only static labels, never the client's actual answers, which live in form field objects with opaque names (dropdown_45oakx).
    now: When the insurer is BrightRock/Lizelle specifically, the quote request needs the client's Fact Find Summary PDF attached — confirmed 2026-09-04:
    why: The provisional rule is kept; the form-reading technique belongs to ff-population-transcript.
- old line 216: (1) read form fields directly, e.g.
    now: rb = _read(os.path.join(run, w.OUT, "readback_%s.txt" % e["id"]))
    why: The provisional rule is kept; the form-reading technique belongs to ff-population-transcript.
- old line 216: pypdf's PdfReader.get_fields() for each field's /V;
    now: allb += [("%s Identified" % card_title(cd), x.get("text"), lim["identified_words"]) for x in c.get("identified", [])]
    why: The provisional rule is kept; the form-reading technique belongs to ff-population-transcript.
- old line 216: (2) match each field to its on-page label by position — field rects via page annotations, label words via pdfplumber's extract_words(), nearest label to the left/above;
    now: R.attested.append("%d Identified point(s) rest on Paul's own words typed by the chat" % pa_n)
    why: The provisional rule is kept; the form-reading technique belongs to ff-population-transcript.
- old line 216: (3) cross-reference the resulting values against the per-service decision logic below and the Master Context Document;
    now: checked by scripts/board.py against the send table and scripts/contacts", "handover":
    why: The provisional rule is kept; the form-reading technique belongs to ff-population-transcript.
- old line 216: (4) do this once per Fact Find, automatically, not only when Paul asks a follow-up question.
    now: *Same-day check-in (only when a follow-up date was entered).
    why: The provisional rule is kept; the form-reading technique belongs to ff-population-transcript.
- old line 218: *A decision-driving field contradicted by its own note is provisional.
    now: *A field contradicted by its own note is provisional.
    why: The provisional rule is kept; the form-reading technique belongs to ff-population-transcript.
- old line 218: If a Yes/No feeding a decision (Group Risk Cover, a "does client require X" toggle, a named specialist-contact field) is contradicted by its adjacent note — box says Yes, note says "client not sure" —
    now: If a Yes/No that drives a decision (Group Risk Cover, a "does the client require X" toggle, a named specialist) is contradicted by its adjacent note, apply the literal answer so nothing is missed, but
    why: The provisional rule is kept; the form-reading technique belongs to ff-population-transcript.
- old line 218: "Group Risk unclear — FF says Yes, noted 'client not sure'").
    now: the form says Yes, the note says client not sure").
    why: The provisional rule is kept; the form-reading technique belongs to ff-population-transcript.
- old line 227: Needs the FNA Quote, the Reduced/Accepted Quote (if it differs), the Fact Find Summary Report, and a confirmed ROA date:
    now: New Business -> wr-roa-builder (it needs the FNA Quote, the Reduced or Accepted Quote if it differs, the Fact Find Summary and a confirmed ROA date, which that skill asks for);
    why: Kept without the ROA date rule, which wr-roa-builder owns.
- old line 230: Needs the Current Policy Schedule, a quote document per compiled quote type, and the Fact Find Summary.
    now: Servicing -> wr-sroa-builder (Current Policy Schedule, a quote document per compiled quote type, the Fact Find Summary;
    why: Kept without the ROA date rule, which wr-roa-builder owns.
- old line 230: Its date and its "reason for the servicing change" are not sourced by this board — wr-sroa-builder's own Step 1 and Step 3 always ask Paul directly for the quote selection, the reason (in his own word
    now: it asks Paul for the quote selection, the reason, the client's full legal name and ID number and the date).
    why: Kept without the ROA date rule, which wr-roa-builder owns.
- old line 230: This board's job is only to hand off the right documents at the right point.
    now: This board's job is to hand over the right documents at the right point and to log the result.
    why: Kept without the ROA date rule, which wr-roa-builder owns.
- old line 238: ClickUp-specific plumbing — explicitly out of scope;
    now: Pulling an attachment out of a reply email is also unconfirmed:
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 239: Client Overview skill — doesn't exist yet;
    now: once the transcript is uploaded run client-teams-transcript-skill and read it against every open line.
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 239: note in a product card's Actions Taken as "Client Overview update — pending skill" wherever the Master Doc calls for updating it.
    now: a Client Overview skill (note "Client Overview update - pending skill" on a card's Actions Taken wherever the Master Document calls for it);
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 240: Formal quote-request drafting skill — no dedicated skill yet for Life Cover/RA/Investments quote emails;
    now: a quote-request drafting skill (draft directly, consistent with Paul's other provider correspondence);
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 240: draft directly, consistent with Paul's other outbound provider correspondence, flagged informal.
    now: a quote-request drafting skill (draft directly, consistent with Paul's other provider correspondence);
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 241: client-review-notes timing across multiple completed lines — ask Paul the first time this comes up.
    now: the timing of client-review-notes across several completed lines (ask Paul the first time);
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 242: Section 14 transfer sub-flow (S14-1 through S14-6) — still TBC with Paul;
    now: the Section 14 transfer sub-flow (flag it on the RA card);
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 242: treat as a flagged item on the RA card.
    now: the Section 14 transfer sub-flow (flag it on the RA card);
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 243: RA/Investments servicing quote-type mapping — Life Cover's Servicing types trace to wr-sroa-builder's categories;
    now: RA and Investments Servicing quote types (ask Paul the first time one comes up;
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 243: RA/Investments servicing doesn't have an equivalent documented set yet — ask Paul the first time one comes up rather than guessing a parallel structure.
    now: RA and Investments Servicing quote types (ask Paul the first time one comes up;
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 244: EGAR proposal, still Paul-drafted — left as-is until Paul says otherwise.
    now: the EGAR proposal (still drafted by Paul).
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 245: Follow-up check-in accuracy depends on the appointment being in Paul's Outlook Calendar — since teams-meeting-setup-skill now creates the event directly in Outlook once Paul gives the go-ahead, this o
    now: {"op":"followup","date":"DD/MM/YYYY","time":"HH:MM","source":"..","via":"teams-meeting-setup-skill","receipt":"KEY"} the confirmed follow-up or 2nd appointment (South African time).
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 245: Paul booked it himself outside this flow);
    now: Paul decides this one BEFORE it is built;
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 245: if a meeting was booked outside Outlook, the scheduled check-in will find nothing to confirm against — flag plainly rather than assuming absence means it didn't happen.
    now: If a meeting was booked outside Outlook the check-in will find nothing to confirm:
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 247: Email attachment extraction is unconfirmed — see outstanding-tracking.md and the Ground rules above.
    now: "every email, message and check-in is done after the yes, and what the tools returned equals what was approved"
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 247: Verify against the first real reply that actually needs it.
    now: if a Reduced-on-FNA-basis request already went out, flag under Identified that it needs re-basing).
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 248: Outstanding-request tracking is untested on a live client — the daily trigger pattern mirrors outlook-emails-skill's proven inbox-check mechanics, but the folder-drop check and board-update-on-find lo
    now: Reply tracking is owned by outlook-emails-skill (an hourly weekday watcher per thread and a one-time silence flag, a fresh chat each time, a phone alert).
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 248: Expect correction on first real use.
    now: A live correction from Paul is authoritative:
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 252: # Send / Draft / Ask — Decision Rules
    now: "The send table (send-decision-rules.md Steps 1 and 2) as data.
    why: The send table is now data; Step 1 and Step 2 are printed by the program.
- old line 254: > Loaded from send-decision-rules.md, referenced by the core SKILL.md.
    now: > Loaded from playbooks/life-cover.md, referenced by the core SKILL.md.
    why: The send table is now data; Step 1 and Step 2 are printed by the program.
- old line 254: Single reference for what Claude does next, any time a client- or provider-facing email, referral, or calendar invite is about to be built or sent.
    now: Every referral or provider email is shown to Paul before anything is sent.
    why: The send table is now data; Step 1 and Step 2 are printed by the program.
- old line 254: Every product playbook defers to this file instead of repeating the logic — check it before drafting or sending anything.
    now: Every referral or provider email is shown to Paul before anything is sent.
    why: The send table is now data; Step 1 and Step 2 are printed by the program.
- old line 256: There are two separate questions, asked at two separate moments.
    now: Two separate questions, at two separate moments:
    why: The send table is now data; Step 1 and Step 2 are printed by the program.
- old line 256: Keep them separate — collapsing them is the single easiest way to send something Paul hasn't actually approved.
    now: Check Sent Items before telling Sitamah to send something Paul may already have sent (ask her to chase instead).
    why: The send table is now data; Step 1 and Step 2 are printed by the program.
- old line 258: does Paul need to make a decision first?
    now: (1) before building it, does Paul need to decide first?
    why: The send table is now data; Step 1 and Step 2 are printed by the program.
- old line 259: Before it reaches a recipient:
    now: a fresh yes right before it reaches a recipient.
    why: The send table is now data; Step 1 and Step 2 are printed by the program.
- old line 259: who actually presses send, and does that need a fresh chat approval?
    now: (2) before it reaches a recipient, who presses send, and does that need a fresh yes?
    why: The send table is now data; Step 1 and Step 2 are printed by the program.
- old line 261: Nothing in this skill ever reaches a real recipient without Paul's explicit go-ahead — the only thing that varies is *where* that checkpoint happens (a question in chat before building, or a review in
    now: Nothing reaches a real recipient without Paul's explicit go-ahead;
    why: The send table is now data; Step 1 and Step 2 are printed by the program.
- old line 263: ## Step 1 — Does building this need Paul's decision first?
    now: (1) before building it, does Paul need to decide first?
    why: Ask first or build automatically is a table the program checks (Paul agreed, 04/11/2026).
- old line 265: This item | Ask Paul first, before building anything | Build automatically, no upfront question |
    now: The moment the FF confirms a Will need, build the complete referral automatically (no upfront question):
    why: Ask first or build automatically is a table the program checks (Paul agreed, 04/11/2026).
- old line 267: Any email with a real judgment call in it (which insurer, hold vs.
    now: "An email with a real judgment call (which insurer, hold or proceed, a counter-offer reply)",
    why: Ask first or build automatically is a table the program checks (Paul agreed, 04/11/2026).
- old line 267: proceed, how to respond to a counter-offer) | ✅ | |
    now: any email with a real judgment call (which insurer, hold or proceed, how to answer a counter-offer);
    why: Ask first or build automatically is a table the program checks (Paul agreed, 04/11/2026).
- old line 268: Life Cover / RA / Investments quote requests | ✅ — always ask which insurer/basis | |
    now: Life Cover, RA and Investments quote requests (always ask which insurer and on what basis);
    why: Ask first or build automatically is a table the program checks (Paul agreed, 04/11/2026).
- old line 270: RGAR request to Old Mutual | | ✅ — fully FF-determined, no branching |
    now: the RGAR request to Old Mutual (fully determined by the Fact Find);
    why: Ask first or build automatically is a table the program checks (Paul agreed, 04/11/2026).
- old line 271: Investment / RA / Tax-Free / RGAR proposal (once the source quote/report is on file) | | ✅ |
    now: a Claude-drafted proposal (Investment, RA, Tax-Free, RGAR) once the source quote or report is on file;
    why: Ask first or build automatically is a table the program checks (Paul agreed, 04/11/2026).
- old line 272: STI referral (Cameron, via cameron-short-term-skill) | | ✅ |
    now: the Short-Term referral (cameron-short-term-skill);
    why: Ask first or build automatically is a table the program checks (Paul agreed, 04/11/2026).
- old line 275: Teams follow-up meeting invite (date already confirmed) | | ✅ |
    now: the Teams follow-up invite (date already confirmed);
    why: Ask first or build automatically is a table the program checks (Paul agreed, 04/11/2026).
- old line 276: LOA explanatory email *(added 2026-09-16)* | | ✅ — auto-built from the Outlook Drafts template, pre-populated LOA/Disclosure from the client's OneDrive folder |
    now: ["I've just sent {client} the LOA explanatory email.", "Please prepare the MSIGN signing pack from the LOA and Disclosure documents I pre-populated in {folder}, and send it to the client via MSIGN."]}
    why: Ask first or build automatically is a table the program checks (Paul agreed, 04/11/2026).
- old line 278: *Not on this list → ask first.
    now: Anything not on this list is ask_first.",
    why: Ask first or build automatically is a table the program checks (Paul agreed, 04/11/2026).
- old line 280: ## Step 2 — Once it's built (or approved to build), where does it go and who sends it?
    now: *Step 2 - where it lands and who sends.
    why: Where it lands and who sends is a table; proposals now follow the proposal skills (Sitamah sends).
- old line 282: Content type | Lands as | Who actually sends it | Separate chat approval needed right before it goes?
    now: where it lands, who sends, whether it needs a fresh yes) and each Sitamah message."
    why: Where it lands and who sends is a table; proposals now follow the proposal skills (Sitamah sends).
- old line 284: Insurer/provider quote or report request | Outlook Draft | Paul, himself | No — already asked in Step 1, or fully auto (RGAR) |
    now: Insurer or provider quote or report request:
    why: Where it lands and who sends is a table; proposals now follow the proposal skills (Sitamah sends).
- old line 285: Client-facing proposal (Investment/RA/Tax-Free/RGAR) | Outlook Draft, HTML body | Paul, himself | No |
    now: a Claude-drafted proposal (Investment, RA, Tax-Free, RGAR) once the source quote or report is on file;
    why: Where it lands and who sends is a table; proposals now follow the proposal skills (Sitamah sends).
- old line 286: General's client document-request email | Outlook Draft | Sitamah — checks it and sends if correct *(corrected 2026-09-16, was Paul)* | No — already asked in Step 1, but Sitamah gets an Action-needed 
    now: General's consolidated email drafted (check it, send it if correct, follow up with the client periodically before the next appointment);
    why: Where it lands and who sends is a table; proposals now follow the proposal skills (Sitamah sends).
- old line 287: STI / Medical Aid / Will referral | Not drafted — shown complete in chat | Claude, via outlook_send_mail | Yes, every time — built without asking in Step 1, but still stops here |
    now: Referral to Valerie | Auto-built, chat-approved, then Claude-sent directly — built inline in this board from the Drafts template library, not a standalone skill (Paul's decision).
    why: Where it lands and who sends is a table; proposals now follow the proposal skills (Sitamah sends).
- old line 288: Teams follow-up meeting invite | Not drafted — event created directly (no draft state exists for a calendar invite with an attendee) | Claude, via outlook_create_event | Yes, every time |
    now: sent by Claude with outlook_send_mail only after Paul's yes, every time.
    why: Where it lands and who sends is a table; proposals now follow the proposal skills (Sitamah sends).
- old line 289: LOA explanatory email *(added 2026-09-16)* | Not drafted — shown complete in chat | Claude, via outlook_send_mail | Yes, every time — see core-ff-intake.md → LOA/Astute sequencing gate for the full pr
    now: ["I've just sent {client} the LOA explanatory email.", "Please prepare the MSIGN signing pack from the LOA and Disclosure documents I pre-populated in {folder}, and send it to the client via MSIGN."]}
    why: Where it lands and who sends is a table; proposals now follow the proposal skills (Sitamah sends).
- old line 291: The four rows that build automatically in Step 1 (RGAR request, the four proposal types, STI/Medical Aid/Will, Teams invite) are not equivalent to each other in Step 2 — RGAR and the proposals still l
    now: A quote request that needs the client's Fact Find Summary attached follows Step 1 and 2 (ask first, Outlook Draft) with one added line immediately before the closing urgency sentence:
    why: Where it lands and who sends is a table; proposals now follow the proposal skills (Sitamah sends).
- old line 291: the referrals and the calendar invite still need a live "go ahead, send it" in chat even though nothing was asked before they were built.
    now: Actions Taken logs the request once sent, and — for a Lizelle request — logs that Sitamah was asked to attach and send.
    why: Where it lands and who sends is a table; proposals now follow the proposal skills (Sitamah sends).
- old line 291: Check both steps separately, every time.
    now: sent by Claude with outlook_send_mail only after Paul's yes, every time.
    why: Where it lands and who sends is a table; proposals now follow the proposal skills (Sitamah sends).
- old line 293: ## The one attachment exception — Lizelle / BrightRock
    now: the Lizelle attachment (four steps:
    why: The line and the message are checked by the program.
- old line 295: Claude cannot attach a real file to an Outlook Draft or a sent email (see "Why this exception exists" below).
    now: Claude cannot attach a real file to a draft or a sent email (the tools have no attachment field, and the Zapier file field only takes a public URL;
    why: The line and the message are checked by the program.
- old line 295: For quote requests to Lizelle Cachado that need the Fact Find Summary PDF attached, follow Step 1/Step 2 normally (ask first, land as an Outlook Draft) — then add one line before the closing urgency s
    now: A quote request that needs the client's Fact Find Summary attached follows Step 1 and 2 (ask first, Outlook Draft) with one added line immediately before the closing urgency sentence:
    why: The line and the message are checked by the program.
- old line 295: Message Sitamah on Teams asking her to open that draft, attach the client's Fact Find Summary PDF from OneDrive, and send it herself — a genuine action request to her, not the usual FYI.
    now: Then Sitamah opens that draft, attaches the Fact Find Summary PDF from the client's folder, sends it and follows up with Lizelle for the quotes back (message lizelle_attach, a genuine action request).
    why: The line and the message are checked by the program.
- old line 295: This is a completion step bolted onto the ordinary Draft pathway, not a fifth pathway of its own.
    now: A scheduled task bound to this chat (create_trigger / send_later, never the local in-session cron tools, which do not survive), timed for the morning of the appointment:
    why: The line and the message are checked by the program.
- old line 295: Extend it to another attachment-needing insurer only if Paul confirms that provider should work the same way.
    now: Extend the exception to another insurer only if Paul confirms it.
    why: The line and the message are checked by the program.
- old line 297: the M365 connector's draft tools have no attachment parameter, and the Zapier microsoft_office_365_send_email/create_draft_email file parameter was live-tested and only accepts a public URL — passing 
    now: Claude cannot attach a real file to a draft or a sent email (the tools have no attachment field, and the Zapier file field only takes a public URL;
    why: The line and the message are checked by the program.
- old line 297: Claude does not put client documents on a public URL to route around this.
    now: never put client documents on a public URL).
    why: The line and the message are checked by the program.
- old line 297: Confirmed dead end — don't retry the API route.
    now: Actions Taken logs the confirmed send, CC'd to client + Sitamah + Paul.
    why: The line and the message are checked by the program.
- old line 297: Every other proposal/quote draft that should carry a source file opens with:
    now: A draft that should carry a source file opens with Attach before sending:
    why: The line and the message are checked by the program.
- old line 299: ## Always true, regardless of pathway
    now: Always make clear it is Claude, not Paul.
    why: Cc Sitamah, no sign-off, native tools only: checked by the program.
- old line 301: CC Sitamah Nathoo (admin@liferisk.co.za) on every drafted or sent email, no exceptions.
    now: Sitamah Nathoo (admin@liferisk.co.za) is on the Cc line of every drafted or sent email.
    why: Cc Sitamah, no sign-off, native tools only: checked by the program.
- old line 301: Full CC pattern by content type (who else gets CC'd on referrals vs.
    now: add(ent == len(board["change_log"]), "Every Change Log entry is on the page (%d)" % ent)
    why: Cc Sitamah, no sign-off, native tools only: checked by the program.
- old line 301: proposals) — see Ground rules → Template library.
    now: Servicing → wr-sroa-builder — see "ROA vs SROA" below.
    why: Cc Sitamah, no sign-off, native tools only: checked by the program.
- old line 302: Every email defers to paul-email-signature — never type a "Kind regards" sign-off into the body.
    now: the Exchange rule adds Paul's signature once (paul-email-signature);
    why: Cc Sitamah, no sign-off, native tools only: checked by the program.
- old line 302: Full mechanism (the transport rules, the calendar-invite exception) — see Ground rules → the signature bullet.
    now: it asks Paul for the quote selection, the reason, the client's full legal name and ID number and the date).
    why: Cc Sitamah, no sign-off, native tools only: checked by the program.
- old line 303: The Lizelle exception above is the only attachment workaround that exists.
    now: Claude cannot attach a real file to a draft or a sent email (the tools have no attachment field, and the Zapier file field only takes a public URL;
    why: Cc Sitamah, no sign-off, native tools only: checked by the program.
- old line 304: Sitamah gets a Teams message on every instance this file covers, in addition to her email CC — see sitamah-messaging.md.
    now: "Every Teams message to Sitamah (sitamah-messaging.md) as data.
    why: Cc Sitamah, no sign-off, native tools only: checked by the program.
- old line 314: How Claude finds out a quote came back, a report's in, or a document landed — since a chat session doesn't stay open watching.
    now: a follow-up check-in that came back moved or not accepted.
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 314: only the last runs without Paul doing anything:
    now: it builds the invite, shows it to Paul, and sends it only after his yes (the client is emailed when it is created).
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 316: Paul tells Claude in chat.
    now: If Paul names a second client in the same chat, ask whether he wants a separate chat.
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 316: Always works, and the only channel for anything that happens face-to-face with a client.
    now: Once sent, Sitamah gets a Teams message with no "watch for a reply" ask — Cameron contacts the client directly, so there's nothing for her to do but be told it happened.
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 316: Log the moment Paul reports it.
    now: nothing further until Paul reports the call outcome.
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 317: A 2nd/3rd appointment transcript — via client-teams-transcript-skill, read against every open line once uploaded.
    now: once the transcript is uploaded run client-teams-transcript-skill and read it against every open line.
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 318: A scheduled check against Outlook and OneDrive/SharePoint — no chat input needed:
    now: While a scheduled check runs unattended there is no computer:
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 319: The moment a provider/insurer-facing request is sent — auto-draft or asked-first — record who it went to, what was asked, and the date, against that product line.
    now: The moment a follow-up (2nd or later) appointment is confirmed, from the transcript or from Paul, record it with followup and hand over to teams-meeting-setup-skill:
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 321: Finding something is a fact, not a decision — log it without asking.
    now: Finding something is a fact, not a decision:
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 321: Save it (routing per the Ground rule above), clear the outstanding item, log it under the relevant card's Actions Taken.
    now: search the client's folder for a matching new file, save it by the routes in 01-locate.md, clear the outstanding item and log it under Actions Taken.
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 321: If it also completes a downstream auto-draft (e.g.
    now: Raises ValueError if it is not a readable PDF."""
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 321: RA quote back → its proposal), do that in the same pass.
    now: Paul builds the proposal (not yet moved to Claude-drafted — revisit if he wants it wired the same way as RA/Investments/RGAR).
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 321: If it needs a decision from Paul (a counter-offer, an insurer's question), that still becomes the pending question — finding it doesn't skip that checkpoint, only *receiving* it does.
    now: if it needs a decision from Paul (a counter-offer, an insurer's question) it becomes the pending question.
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 322: End a run that found something with a clear summary and notifications:{"push":true};
    now: When something is found, tell Paul with a push notification.
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 322: end a quiet run unremarkably.
    now: save_run(a.run, rj)
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 322: Republish the board in the same run if anything changed.
    now: "shown to Paul in the same reply as the board;
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 323: Message Sitamah about anything still outstanding too, not just what was found.
    now: A message covering both resolved and still-outstanding items is Action needed overall;
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 323: If some items came back and others are still sitting with no reply, the Teams update to her covers both — and for the still-outstanding half, asks her to follow up with the named contact and states th
    now: ["Still waiting on:", "{@outstanding}", "Please follow up with each contact named above directly.", "I check again {cadence}."]},
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 323: See "Keeping Sitamah in the loop" → "How to write the message."
    now: "Create the drafts, send the emails, message Sitamah, set the check-in;
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 326: pulling the actual attachment bytes out of a reply email.
    now: Pulling an attachment out of a reply email is also unconfirmed:
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 326: the "save it automatically" step needs verifying against a real case — until then, log the find and flag plainly if the save couldn't be confirmed.
    now: search the client's folder for a matching new file, save it by the routes in 01-locate.md, clear the outstanding item and log it under Actions Taken.
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 330: # Keeping Sitamah in the Loop
    now: emails first, then the Sitamah messages, then the check-in.",
    why: Every trigger is kept as data; one message per event after Paul's yes.
- old line 334: ## Keeping Sitamah in the loop
    now: emails first, then the Sitamah messages, then the check-in.",
    why: Every trigger is kept as data; one message per event after Paul's yes.
- old line 336: Sitamah gets a Teams direct message for every instance below, in addition to — never instead of — her email CC and the board's own log.
    now: Once sent, Sitamah gets a Teams message with no "watch for a reply" ask — Cameron contacts the client directly, so there's nothing for her to do but be told it happened.
    why: Every trigger is kept as data; one message per event after Paul's yes.
- old line 336: More information is better here;
    now: more than one fact in one bullet (one fact per bullet)" % label)
    why: Every trigger is kept as data; one message per event after Paul's yes.
- old line 336: this list is deliberately not trimmed to "important" ones only.
    now: Only if it is genuinely not there, ask Paul to upload it.
    why: Every trigger is kept as data; one message per event after Paul's yes.
- old line 338: *Two tiers, so the messages that need her to actually do something don't get lost in the ones that don't.
    now: Two tiers, so the messages that need her to act do not get lost:
    why: Every trigger is kept as data; one message per event after Paul's yes.
- old line 338: Every trigger below is one or the other — never both, never neither:
    now: Neither answer depends on the other, so both go in the same chat message.
    why: Every trigger is kept as data; one message per event after Paul's yes.
- old line 340: Action needed — the message asks Sitamah to do something (now or "watch for X and follow up if it doesn't happen").
    now: Once sent, Sitamah gets a Teams message with no "watch for a reply" ask — Cameron contacts the client directly, so there's nothing for her to do but be told it happened.
    why: Every trigger is kept as data; one message per event after Paul's yes.
- old line 340: followed by a one-clause summary of what, before any other detail.
    now: and a one-clause summary (Teams often shows the opening words in the notification).
    why: Every trigger is kept as data; one message per event after Paul's yes.
- old line 340: This is deliberate — Teams often shows a message's opening words in the notification preview, so the tag surfaces there too, not just once she opens the chat.
    now: and a one-clause summary (Teams often shows the opening words in the notification).
    why: Every trigger is kept as data; one message per event after Paul's yes.
- old line 341: FYI — nothing for her to do;
    now: nothing for Sitamah to do but be told it happened.
    why: Every trigger is kept as data; one message per event after Paul's yes.
- old line 341: the message is purely so she stays current.
    now: "every email, message and check-in is done after the yes, and what the tools returned equals what was approved"
    why: Every trigger is kept as data; one message per event after Paul's yes.
- old line 341: No tag needed (its absence *is* the signal) — but it must still end with an explicit "nothing needed from you" line, same as before.
    now: no tag, and it ends 'Nothing needed from you.'")
    why: Every trigger is kept as data; one message per event after Paul's yes.
- old line 341: Never leave an FYI message ambiguous about which tier it is.
    now: They go straight to the provider contact, so Sitamah's message is an FYI with no reply-watch ask.
    why: Every trigger is kept as data; one message per event after Paul's yes.
- old line 343: *When to message her — Action needed:
    now: "Teams messages to Sitamah (Action needed, and one FYI)", "file":
    why: Every trigger is kept as data; one message per event after Paul's yes.
- old line 345: An email actually being sent that needs a reply watched for.
    now: "An email was actually sent that needs a reply watched for", "slots":
    why: The card shapes are checked by the program.
- old line 345: Fires once an email is genuinely sent — whether Claude sends it directly at Paul's go-ahead, or Paul reports he's sent a draft himself.
    now: Nothing is sent, posted or published without Paul's clear yes, in the same reply that shows it all with ONE question.
    why: The card shapes are checked by the program.
- old line 345: watch for the recipient's reply, and follow up with the client directly if nothing's come back after a few business days (same rough window as the Medical Aid/Will "follow up 5 business days" conventi
    now: {subject}.", "- Please watch for {recipient}'s reply", "- If nothing has come back after a few business days, please follow up with the client directly"]},
    why: The card shapes are checked by the program.
- old line 345: Exception — no tag, this one's FYI instead:
    now: no message '%s' in this run (ids:
    why: The card shapes are checked by the program.
- old line 345: the Cameron/STI, Valerie/Medical Aid, and Amber/Will referrals go straight to the client or the client's own provider contact, not back through Paul or Sitamah — nothing for her to watch for, so tag t
    now: They go straight to the provider contact, so Sitamah's message is an FYI with no reply-watch ask.
    why: The card shapes are checked by the program.
- old line 346: A daily outstanding-request check that still has items with no reply.
    now: "The outstanding-request check still has items with no reply", "slots":
    why: The card shapes are checked by the program.
- old line 346: Even though nothing new came in, this gets a message — see "Outstanding request tracking." The ask itself is what makes it Action needed:
    now: A message covering both resolved and still-outstanding items is Action needed overall;
    why: The card shapes are checked by the program.
- old line 346: name the contact (insurer/provider, or the client) for every item still outstanding and ask her to follow up with them directly.
    now: ["Still waiting on:", "{@outstanding}", "Please follow up with each contact named above directly.", "I check again {cadence}."]},
    why: The card shapes are checked by the program.
- old line 346: Never send this as a bare "still nothing" — see "still-outstanding" wording below.
    now: %s" % (r["lands"], r["sender"], "your yes covers the send" if r["yes_before_send"] else "saved as a draft, nothing is sent")))
    why: The card shapes are checked by the program.
- old line 347: The Lizelle/BrightRock attachment workaround.
    now: the Lizelle attachment (four steps:
    why: The card shapes are checked by the program.
- old line 347: The one case where she's doing something operational (open a draft, attach a file, send it), not just staying informed.
    now: search the client's folder for a matching new file, save it by the routes in 01-locate.md, clear the outstanding item and log it under Actions Taken.
    why: The card shapes are checked by the program.
- old line 347: Fires the moment the Lizelle quote-request draft (with the "Please see attached Fact Find Summary for this client." line already inserted) is saved to Outlook Drafts — see playbooks/life-cover.md → Qu
    now: build the email exactly as before, then insert the line Please see attached Fact Find Summary for this client.
    why: The card shapes are checked by the program.
- old line 347: Name the draft's exact subject line, name the OneDrive folder the PDF lives in, and be explicit about all four steps:
    now: once the LOA is signed and saved to the client's OneDrive folder, Claude does not draw the Astute report itself:
    why: The card shapes are checked by the program.
- old line 347: open, attach, send, and follow up with Lizelle for the quotes back *(added 2026-09-16)*.
    now: Follow up with Lizelle for the quotes back"]},
    why: The card shapes are checked by the program.
- old line 348: The LOA explanatory email being sent.
    now: "The LOA explanatory email has been sent", "slots":
    why: The card shapes are checked by the program.
- old line 348: *(Added 2026-09-16.)* Fires the moment the LOA email goes out — see core-ff-intake.md → LOA/Astute sequencing gate.
    now: *LOA and Astute (sequencing gate).
    why: The card shapes are checked by the program.
- old line 348: Ask her to prepare the MSIGN signing pack using the LOA and Disclosure documents Claude already pre-populated in the client's OneDrive folder, and send it to the client via MSIGN.
    now: ["I've just sent {client} the LOA explanatory email.", "Please prepare the MSIGN signing pack from the LOA and Disclosure documents I pre-populated in {folder}, and send it to the client via MSIGN."]}
    why: The card shapes are checked by the program.
- old line 349: *(Added 2026-09-16.)* Fires the moment the General on-file check finds a locked document it can't open — see "Board sections" → General.
    now: Every point on the board comes from a registered document (a verbatim line the program can find) or Paul's own words;
    why: The card shapes are checked by the program.
- old line 349: Name the exact file and folder, explain Claude needs to check it, and ask her to re-save it without password protection — not a request to the client.
    now: ["{file} in {folder} is password-protected and I can't open it.", "Please re-save it without password protection so I can check it.
    why: The card shapes are checked by the program.
- old line 350: *(Added 2026-09-16 — replaces the old "Paul sends it" pattern.)* Fires the moment the draft saves to Outlook Drafts — see "Board sections" → General.
    now: it builds the invite, shows it to Paul, and sends it only after his yes (the client is emailed when it is created).
    why: The card shapes are checked by the program.
- old line 350: Ask her to check it, send it herself if correct, and follow up with the client periodically before the next appointment — this is a standing ask, not a one-off.
    now: General's consolidated email drafted (check it, send it if correct, follow up with the client periodically before the next appointment);
    why: The card shapes are checked by the program.
- old line 351: The Astute report, once the LOA is signed and saved.
    now: no Astute report until signed LOA back).
    why: The card shapes are checked by the program.
- old line 351: *(Added 2026-09-16 — Sitamah draws this, Claude doesn't.)* Fires the moment the signed LOA is confirmed saved to the client's OneDrive folder — see core-ff-intake.md → LOA/Astute sequencing gate.
    now: once the LOA is signed and saved to the client's OneDrive folder, Claude does not draw the Astute report itself:
    why: The card shapes are checked by the program.
- old line 351: Tell her the LOA's signed and saved, and ask her to draw the Astute report.
    now: it messages Sitamah (Action needed) that the LOA is signed and saved, and asks her to draw the Astute report herself.
    why: The card shapes are checked by the program.
- old line 352: The COC invite being sent.
    now: "The COC invite has been sent", "slots":
    why: The card shapes are checked by the program.
- old line 352: *(Added 2026-09-16.)* Fires the moment Claude creates the 30-minute COC appointment — see playbooks/life-cover.md → COC.
    now: ["The 30-minute COC appointment invite is sent for {when}.", "Please watch for the client's acceptance."]},
    why: The card shapes are checked by the program.
- old line 352: Tell her it's sent and ask her to watch for acceptance.
    now: ["The 30-minute COC appointment invite is sent for {when}.", "Please watch for the client's acceptance."]},
    why: The card shapes are checked by the program.
- old line 353: *(Added 2026-09-16.)* Fires on the appointment date — ask her to call the client as a reminder that day.
    now: the day of the COC appointment (call the client as a reminder);
    why: The card shapes are checked by the program.
- old line 354: *(Added 2026-09-16.)* Ask her to confirm whether the appointment actually happened — Claude doesn't request the tele-underwriting transcript until she confirms.
    now: I will not ask for the tele-underwriting transcript until you do."]},
    why: The card shapes are checked by the program.
- old line 355: An RAR request drafted (replacement cases, Underwriting).
    now: RAR Process (replacement cases only):
    why: The card shapes are checked by the program.
- old line 355: *(Added 2026-09-16.)* Fires the moment the RAR request email is saved to Outlook Drafts — see playbooks/life-cover.md → Underwriting.
    now: ["An RAR is required for {client}'s {product}, and the email is drafted in Outlook Drafts, subject:
    why: The card shapes are checked by the program.
- old line 355: Name the client and product, confirm the email's drafted, and ask her to check it, attach the policy schedule(s) of the policy being replaced, and send it — then to watch for the completed RAR coming 
    now: ["An RAR is required for {client}'s {product}, and the email is drafted in Outlook Drafts, subject:
    why: The card shapes are checked by the program.
- old line 356: A follow-up appointment's check-in comes back moved or not accepted.
    now: "The follow-up appointment check-in came back moved or not accepted", "slots":
    why: The card shapes are checked by the program.
- old line 356: Unlike a plain confirmed result (FYI — see below), a moved or not-accepted appointment may mean she needs to re-prep documents or chase the client — flag it as Action needed rather than a passive stat
    now: ["{detail}", "You may need to re-prep the documents or chase the client."]}
    why: The card shapes are checked by the program.
- old line 358: *When to message her — FYI:
    now: When the signed LOA is saved, tell Sitamah (message astute_loa_signed) to draw the Astute report:
    why: Every trigger is kept as data; one message per event after Paul's yes.
- old line 360: Every ordinary Actions Taken entry, on every card.
    now: Actions Taken sits only on General or a product card" % who)
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 360: a quote/report requested or received back;
    now: Insurer or provider quote or report request:
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 360: a Claude-drafted proposal saved to Drafts;
    now: "RA proposal drafted (om-optimal-ra-proposal), saved to Outlook Drafts.
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 360: a two-insurer comparison built;
    now: Insurer Comparison (replacement scenarios) | Not a silent auto-build:
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 360: a Welcome Letter/policy/schedule received or issued;
    now: "A password-protected policy schedule was found on file", "slots":
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 360: a referral drafted, followed up, or concluded;
    now: a follow-up check-in that came back moved or not accepted.
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 360: a shortfall surfacing a new RA line.
    now: A surfaced shortfall can spawn a new RA line — note the link.
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 361: Every Paul-reported milestone — things only Paul knows:
    now: The New Business / Servicing tag shows on Life Cover, RA and Investments only, and Paul gives it.
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 361: client's decision at presentation;
    now: ["{client}'s COC appointment is today at {when}.", "Please call the client as a reminder."]},
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 361: an application dated and completed live;
    now: Accept → application (pre-filled, completed live), FICA pack, schedule + Welcome Letter, New Business → wr-roa-builder;
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 361: a counter-offer and how Paul responded;
    now: if it needs a decision from Paul (a counter-offer, an insurer's question) it becomes the pending question.
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 361: the policy confirmed in force;
    now: SA time first, the Greek time in brackets."""
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 361: the Risk Tolerance Questionnaire completed;
    now: Presentation/Application/Compliance | Present, complete Risk Tolerance Questionnaire, client decides.
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 361: the follow-up meeting having happened.
    now: "Teams follow-up meeting invite",
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 362: The Teams meeting invite actually being sent, and a check-in result that comes back confirmed (not moved, not declined — see Action needed above for those outcomes).
    now: a follow-up check-in that came back moved or not accepted.
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 363: The Cameron/STI, Valerie/Medical Aid, and Amber/Will referrals, once sent.
    now: Short-Term, Medical Aid and Will referrals, and the LOA email:
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 363: Confirm it went out, to whom, and that there's nothing for her to do beyond staying posted — these go straight to the client's own contact at the provider, so no reply-watch ask applies.
    now: They go straight to the provider contact, so Sitamah's message is an FYI with no reply-watch ask.
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 364: A daily outstanding-request check where everything came back with no items left outstanding.
    now: "The outstanding-request check still has items with no reply", "slots":
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 364: (A fully quiet run — nothing outstanding at all — still sends no message, per "Outstanding request tracking.")
    now: a file called "signed" with no audit trail is probably still the blank template.
    why: Reply tracking is owned by outlook-emails-skill (Paul agreed, 04/11/2026); the folder-drop check stays as a marked, unproven text rule.
- old line 366: *How to write the message:
    now: These rules apply from the first message to the last.
    why: Every trigger is kept as data; one message per event after Paul's yes.
- old line 368: Lead with the tier, right after the greeting.
    now: the first line after the greeting is Action needed:
    why: The published page is read back and compared.
- old line 368: Action needed messages open their first content line with Action needed:
    now: 'action' messages open with 'Action needed:' and a one-clause summary;
    why: The published page is read back and compared.
- old line 368: plus a one-clause summary.
    now: 'action' messages open with 'Action needed:' and a one-clause summary;
    why: The published page is read back and compared.
- old line 368: FYI messages carry no tag and close with an explicit "nothing needed from you" line — never let a message read ambiguously as to which tier it's in.
    now: the one 'fyi' message carries no tag and ends 'Nothing needed from you.' Slots in {braces};
    why: The published page is read back and compared.
- old line 369: Vary the greeting, every single time — rotate naturally ("Hey Sitamah!", "Morning Sitamah!", "Hi Sitamah, quick one for you", "Sitamah — Claude here again", "Hope your day's going well, Sitamah").
    now: add(pt.lstrip().startswith("%s Sitamah," % greeting), "It opens with the greeting '%s Sitamah,' and says it is Claude" % greeting)
    why: The published page is read back and compared.
- old line 370: Never use a time-of-day greeting ("Morning/Afternoon/Evening") without checking the actual current time in South Africa first (SAST, UTC+2) — e.g.
    now: the office is in South Africa, SAST = UTC+2 all year)
    why: The published page is read back and compared.
- old line 370: TZ='Africa/Johannesburg' date, since Sitamah and the office are in Fourways, Johannesburg.
    now: It REBUILDS the board, the emails, the Sitamah messages and the check-in from the run folder itself and compares them with what is on disk, so
    why: The published page is read back and compared.
- old line 370: This is deliberately a different zone from the Athens time this file's own changelog uses.
    now: Every republish carries the program's Last updated stamp (Athens time) and a new Change Log entry.
    why: The published page is read back and compared.
- old line 370: before ~12:00 SAST → "Morning";
    now: sent_before = [k for k, v in (st.get("messages") or {}).items() if v.get("posted_for_greeting")]
    why: The published page is read back and compared.
- old line 370: ~12:00–17:00 → "Afternoon";
    now: 2026-11-04 00:00 (Athens time)
    why: The published page is read back and compared.
- old line 370: When in doubt, use a time-neutral greeting instead — it never needs a check.
    now: Fix it in Outlook (never send a wrong draft), read it back and run this again.
    why: The published page is read back and compared.
- old line 371: Check SAST time as the very last step before the send call, not earlier in the same run.
    now: BASE = "base.json"                      # the board as it stood before this run (read back from the published page), or an empty start
    why: The published page is read back and compared.
- old line 371: A run can spend real hours between an early time check (Outlook searches, OneDrive checks, board republishing) and the moment the Teams message actually goes out — long enough to cross a greeting band
    now: print("Then microsoft_teams_send_chat_message with that chat, format \"markdown\" and content = the text above (an output_hint is required).
    why: The published page is read back and compared.
- old line 371: Re-run the SAST check immediately before microsoft_teams_send_chat_message/microsoft_teams_create_chat_and_send_message every time;
    now: Resolve her chat once with list_dynamic_enum_values on microsoft_teams_send_chat_message's chat property and reuse it.
    why: The published page is read back and compared.
- old line 371: never reuse a timestamp from earlier in the turn.
    now: Whenever a Fact Find is processed, all three outputs are delivered together in the same turn:
    why: The published page is read back and compared.
- old line 372: Plain, warm, conversational language — no stage codes, no internal jargon (LC-1, auto-draft, pendingQueue).
    now: no stage codes, no internal jargon.
    why: The published page is read back and compared.
- old line 372: Describe what happened the way Paul would say it out loud.
    now: flag it on the Fact Find card and ask Paul what to do.
    why: The published page is read back and compared.
- old line 373: tag (if Action needed) → what's been done → what happens next → what's expected of her, if anything.
    now: print("  message %s | %s | %s" % (m["id"], "Action needed" if m["tier"] == "action" else "FYI", m["trigger"]))
    why: The published page is read back and compared.
- old line 373: If nothing's expected, say so plainly.
    now: "If it was moved or not accepted, say so plainly and ask Paul;
    why: The published page is read back and compared.
- old line 374: Point form for anything with more than one fact — format:"markdown" bullets, same brevity discipline as the board's own Actions Taken.
    now: Publish out/board.html with the Artifact tool as it is, titled exactly as the page's title (<Client Name> - Pipeline), to the board's own address when one exists.
    why: The published page is read back and compared.
- old line 375: When an outstanding item is still unanswered, don't say "nothing needed from you." A daily outstanding-request check often finds some items resolved and others still sitting with no reply — that secon
    now: the daily outstanding check still has items with no reply (it names the contact for each, and states the real check cadence read off the scheduled task, never "regularly");
    why: The published page is read back and compared.
- old line 375: For every item still outstanding with no reply, name the contact (insurer/provider/referral contact, or the client) and ask her directly to follow up with them.
    now: Once sent, Sitamah gets a Teams message with no "watch for a reply" ask — Cameron contacts the client directly, so there's nothing for her to do but be told it happened.
    why: The published page is read back and compared.
- old line 375: Close by stating the actual check cadence — read it off the daily trigger's schedule (e.g.
    now: close-out cancels the client's scheduled check-ins first;
    why: The published page is read back and compared.
- old line 375: "once a day, around 8am SAST"), never a vague "regularly" or "keeping an eye on it." A message covering both resolved and still-outstanding items is Action needed overall (the outstanding half decides
    now: A message covering both resolved and still-outstanding items is Action needed overall;
    why: The published page is read back and compared.
- old line 392: > Loaded from verification-checklist.md, referenced by the core SKILL.md.
    now: > Loaded from playbooks/medical-aid-will.md, referenced by the core SKILL.md.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 392: Run through this before every board publish.
    now: "Publish the board in this reply and read the published page back",
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 396: Before every publish, check each card:
    now: Never send, post or publish before his clear yes.",
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 396: does it show only Identified + (a pending question, if awaiting Paul) + Actions Taken + (a New Business/Servicing tag, on product lines) — no internal stage code, no stepper, no timestamped log, no fa
    now: A card is Identified, one pending question if something awaits Paul, and Actions Taken.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 398: does its Identified list contain only documents needed *from the client*, nothing that should be a provider/insurer request on a product card instead?
    now: its Identified list is exactly the documents WR needs from the client, gathered once across every product for one combined email, reconciled against the on-file check.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 398: Was the OneDrive on-file check actually done (3.
    now: General's list is written only after the on-file check of %s;
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 398: Policy Schedules) before the ask was written?
    now: Policy Schedules (the last is mandatory:
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 398: If a locked document was found, was Sitamah asked to re-save it — never the client asked for the password?
    now: tell Sitamah (message locked_file) to re-save it without protection.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 398: Once the consolidated email is drafted, did Sitamah get an Action-needed message asking her to check it, send it if correct, and follow up with the client periodically — rather than the draft being le
    now: General's consolidated email drafted (check it, send it if correct, follow up with the client periodically before the next appointment);
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 400: does its Identified list trace to the FF's real field values (not page labels)?
    now: esc(wd["card_labels"]["identified"]), _identified(ff["identified"]), "<p><b>%s</b></p>" % esc(na_text(na)) if na else ""))
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 400: Is any provisional, note-contradicted field flagged plainly, not silently resolved?
    now: *A field contradicted by its own note is provisional.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 400: Does Actions Taken contain only things that actually happened, never a restatement of Identified?
    now: An Actions Taken line exists only for something that really happened, and it names its receipt.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 400: For Life Cover/RA/Investments:
    now: (On-page controls for Life Cover were tried once and reverted.)
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 400: was the New Business/Servicing question actually asked at line creation and is the tag showing?
    now: A new line gets the New Business / Servicing question immediately.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 400: RGAR/EGAR/Medical Aid/Will/STI should never carry this tag.
    now: RGAR, EGAR, Medical Aid, Will and Short-Term never carry the tag.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 402: was the client's name read from the chat title rather than asked (unless genuinely unclear)?
    now: Take the client's name from the chat title (ask only if it is truly unclear).",
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 402: Was the transcript search actually done against OneDrive/SharePoint before asking Paul to upload one?
    now: The program's first lines give you one sentence to say to Paul before anything else:
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 402: Was Fact Find intake run automatically the moment a transcript was found?
    now: a Servicing line always runs a fresh, full Fact Find from a current transcript.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 404: did all three mandatory outputs actually get produced and delivered in the same turn — Transcript PDF, Summary PDF, Planner/AdviceTech Notes?
    now: The Fact Find Transcript PDF, the Fact Find Summary PDF and the Planner / AdviceTech note, delivered together in the same turn.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 404: Was every transcript-derived field actually re-checked against the source transcript rather than left as "Not discussed" or copied from a possibly-stale document?
    now: Every request to an insurer or provider contact about a client is a reply to the most recent email in the mailbox to or from that contact about that client, never a fresh email:
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 404: Was any genuinely ambiguous figure flagged rather than silently resolved?
    now: flag plainly anything still missing rather than guessing.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 406: *Before any client-/provider-facing action that is NOT an auto-draft line:
    now: A quote request that needs the client's Fact Find Summary attached follows Step 1 and 2 (ask first, Outlook Draft) with one added line immediately before the closing urgency sentence:
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 406: was the underlying decision asked of Paul as the pending question, rather than derived from the FF and acted on directly?
    now: if it needs a decision from Paul (a counter-offer, an insurer's question) it becomes the pending question.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 406: Where a quote depends on a document, is that document actually in hand (logged received or found on file), not just ticked Yes on the FF?
    now: Do not put anything on the client ask that is already signed or on file;
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 408: *Every auto-draft line (RGAR, every Claude-drafted proposal):
    now: Sitamah Nathoo (admin@liferisk.co.za) is on the Cc line of every drafted or sent email.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 408: was a Drafts-folder template checked first and reused/created under the naming convention (proposals excepted)?
    now: search the client's folder for a matching new file, save it by the routes in 01-locate.md, clear the outstanding item and log it under Actions Taken.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 408: Is the cc line correct for the type (insurer-facing:
    now: Sitamah Nathoo (admin@liferisk.co.za) is on the Cc line of every drafted or sent email.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 408: Sitamah only, client is To)?
    now: General is client-facing only;
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 408: Did the draft go straight to Actions Taken with no pending question?
    now: Auto-draft — no pending question.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 408: Does the real draft have a plain subject with no bracket tag?
    now: the real draft always gets a plain, professional subject (the program refuses a bracket).
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 408: is the body HTML (bodyType:"html"), and does it open with the attach-before-sending note when a source file exists?
    now: Attach-before-sending note if a quote/fact-sheet file exists.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 408: Medical Aid and Will are no longer auto-draft lines — see the next check.
    now: Short-Term, Medical Aid and Will referrals, and the LOA email:
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 410: *Short-Term Insurance/Cameron, Medical Aid/Valerie, and Will/Amber — the auto-built-but-not-silent pattern:
    now: Short-Term, Medical Aid and Will referrals, and the LOA email:
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 410: was the email built inline in this board from the Drafts-folder template library ([CAMERON - SHORT TERM INSURANCE REQUEST EMAIL], [VALERIE - MEDICAL AID REFERRAL], [AMBER - WILL / CAPITAL LEGACY REFER
    now: Referral to Valerie | Auto-built, chat-approved, then Claude-sent directly — built inline in this board from the Drafts template library, not a standalone skill (Paul's decision).
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 410: Does the client's-details block carry name, ID, cell number, and email — never ID alone?
    now: the Medical Aid and Will emails carry the client's full details block (name, ID number, cell number and email, never the ID alone).
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 410: Was the complete built email (To/CC/Subject/Body) actually shown to Paul in chat as this card's pending question, with real approval received, before anything sent?
    now: Every referral or provider email is shown to Paul before anything is sent.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 410: Was it sent directly via outlook_send_mail — never saved to Outlook Drafts?
    now: it never saves to Outlook Drafts.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 410: Does the CC line carry all three of client + Sitamah + Paul?
    now: Actions Taken logs the confirmed send, CC'd to client + Sitamah + Paul.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 410: Was Sitamah's post-send Teams message informational only, with no "watch for a reply" ask?
    now: Once sent, message Sitamah on Teams — informational only, no "watch for a reply" ask, since Amber contacts the client directly, not Paul;
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 412: *Lizelle/BrightRock attachment workaround specifically:
    now: the Lizelle attachment (four steps:
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 412: does the drafted email contain the exact inserted line — "Please see attached Fact Find Summary for this client." — placed immediately before the closing urgency line?
    now: build the email exactly as before, then insert the line Please see attached Fact Find Summary for this client.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 412: Was it saved to Outlook Drafts as a genuine draft, not sent directly?
    now: {draft_subject}, and saved it in Outlook Drafts.", "Please:", "1.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 412: Was Sitamah's Teams message a real action request (name the draft's subject, name the OneDrive folder, ask her to attach and send) rather than an FYI?
    now: Once sent, Sitamah gets a Teams message with no "watch for a reply" ask — Cameron contacts the client directly, so there's nothing for her to do but be told it happened.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 412: Is this logged under Actions Taken as "Sitamah asked to attach FF Summary and send," not as a completed send?
    now: Actions Taken logs the request once sent, and — for a Lizelle request — logs that Sitamah was asked to attach and send.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 412: Does the Teams message also ask her to follow up with Lizelle for the quotes back, not just attach and send?
    now: Follow up with Lizelle for the quotes back"]},
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 414: was Paul actually asked which comparison approach to take (like-for-like vs.
    now: The moment the client's current policy schedule is saved to their OneDrive folder, ask Paul directly which comparison approach to take:
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 414: against the new proposal) the moment the current policy schedule landed on file, rather than the comparison being built silently?
    now: The moment the client's current policy schedule is saved to their OneDrive folder, ask Paul directly which comparison approach to take:
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 414: Is there real lead time before the 2nd appointment, or is this running too close to the deadline to have been requested and received in time?
    now: The comparison must be ready before the 2nd/follow-up appointment — this is exactly why getting the client's current policy schedule onto General's ask early matters so much;
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 416: was the 30-minute invite actually sent, and Sitamah told to watch for acceptance?
    now: the COC invite sent (watch for acceptance);
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 416: On the appointment day, was she asked to call as a reminder?
    now: the day of the COC appointment (call the client as a reminder);
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 416: One hour after the scheduled time, was she asked to confirm completion — and did the tele-underwriting transcript request wait for that confirmation rather than firing automatically?
    now: one hour after the COC (confirm whether it happened;
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 416: Was the submission to Lizelle built from Sitamah's existing Outlook template, not built from scratch?
    now: Actions Taken logs the request once sent, and — for a Lizelle request — logs that Sitamah was asked to attach and send.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 418: for Requirements Issued, did Claude correctly NOT send a "file's complete" notification to the insurer once requirements were met — is it just monitoring for their decision?
    now: Referral to Valerie | Auto-built, chat-approved, then Claude-sent directly — built inline in this board from the Drafts template library, not a standalone skill (Paul's decision).
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 418: For an RAR, was Sitamah asked to attach the replaced policy's schedule and send, rather than Claude sending it directly?
    now: Actions Taken logs the request once sent, and — for a Lizelle request — logs that Sitamah was asked to attach and send.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 418: For a Counter Offer Letter, was the insurer's written reason actually obtained and Paul's agreement checked before any client-facing COL communication was built, and did the client's written acceptanc
    now: "[Insurer]'s stated reason for the counter offer is [X] — do you agree with it?" Once Paul agrees and the client-facing COL is sent:
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 420: short, one fact, point form — never merged into one sentence.
    now: Point form for more than one fact.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 420: Check the actual rendered array length, not just that text is present.
    now: %s%% is not in the document's text" % (label, t)
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 420: Does the label carry the CLAUDE badge?
    now: add(html.count('class="claude-tag"') == n_act, "Every Actions Taken label carries the CLAUDE badge (%d)" % n_act)
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 424: Does "Last updated" reflect current Athens time?
    now: %s (Athens time)" % board["stamp"] in html, "The Last updated stamp is the program's (Athens time:
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 424: Has the board republished automatically, with this reply actually containing it?
    now: rows.append(("Board republished", "%s — Pipeline, in the same reply, only with what has a receipt" % b.client_full(c["board"]), "program page"))
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 424: Is the board a pure read-out — no capabilities declared, no on-page controls, every pendingQueue item kind:"text"?
    now: "the board and the page are exactly what the program builds, and every rule on a card holds"
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 426: does this republish add a new dated entry at the top of the Change Log, naming which card(s) changed and what happened, in the same short point-form style as Actions Taken?
    now: date (Athens), short point-form bullets naming the card and what happened, newest first.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 426: Is the date in Athens time, matching "Last updated"?
    now: Every republish carries the program's Last updated stamp (Athens time) and a new Change Log entry.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 426: If the log has passed roughly 40 entries, are the entries older than the most recent ~15 collapsed under a <details>/<summary> fold rather than left to grow unbounded?
    now: Past about 40 entries, those older than the most recent 15 fold under "Show earlier changes";
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 428: *Close-out (only relevant once every line on a board has resolved):
    now: Close-out is only for NTU (declined everything at prospect stage, no policy placed) and Inactive (the relationship has ended).
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 428: was Paul actually asked once, rather than the board closed on Claude's own judgment?
    now: closing needs the status NTU or Inactive and Paul's own words (never closed on Claude's own judgment)" % who)
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 428: If he confirmed NTU or Inactive, is the banner showing at the top, were any still-running scheduled triggers for this client actually cancelled, does the Change Log carry the close-out entry, and was 
    now: "The Change Log has today's entry at the top, newest first (%d entr%s)" % (len(cl), "y" if len(cl) == 1 else "ies") if cl else "The Change Log is empty")
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 430: *LOA email (Fact Find intake):
    now: "LOA explanatory email to the client",
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 430: were the LOA/Disclosure documents actually pre-populated from OneDrive before Paul was asked to approve, was Sitamah CC'd, did Paul actually approve in chat before it sent, and did Sitamah get an Acti
    now: Claude creates and sends the COC appointment invite (fixed 30-minute duration), then messages Sitamah (Action needed) that it's been sent, asking her to watch for acceptance.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 430: if a contradiction genuinely turned up, was Paul asked directly what to do, rather than the product line being silently skipped?
    now: If a meeting was booked outside Outlook the check-in will find nothing to confirm:
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 430: once the signed LOA is confirmed saved, did Claude notify Sitamah rather than drawing the report itself?
    now: once the LOA is signed and saved to the client's OneDrive folder, Claude does not draw the Astute report itself:
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 432: is Sitamah actually on the CC line?
    now: Sitamah Nathoo (admin@liferisk.co.za) is on the Cc line of every drafted or sent email.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 432: Was it created via a native M365 Outlook tool (never Zapier Office 365)?
    now: Use only the native Microsoft 365 draft and send tools, never the Zapier Office 365 tools.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 432: Does the body stop short of a typed "Kind regards"/sign-off?
    now: the body types a sign-off;
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 434: *Life Cover's insurer/GR questions:
    now: "BrightRock (the default Life Cover insurer)"},
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 434: is the standard insurer list (BrightRock first) offered, and is Reduced vs.
    now: (1) which insurer for the FNA quote (standard list, BrightRock first:
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 434: Shortfall correctly keyed to Group Risk's actual current status?
    now: The Shortfall question is genuinely later, once the Group Risk Benefit Statement is back.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 434: Everything answerable right now (FNA insurer, plus the Reduced-now-vs-hold decision and its insurer if applicable) asked as ONE combined message, not one question at a time — with the Shortfall questi
    now: pendingQueue asks one combined question covering everything currently answerable, with the Shortfall question as its own separate later item once the GR statement is back;
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 434: For a Servicing line, is the Servicing FNA/Shortfall/Alternative combination, plus insurer, confirmed with Paul together in one message rather than assumed or split across several?
    now: The moment a follow-up (2nd or later) appointment is confirmed, from the transcript or from Paul, record it with followup and hand over to teams-meeting-setup-skill:
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 436: once a follow-up date is confirmed, was teams-meeting-setup-skill actually invoked to set up the Teams meeting, gated on Paul's go-ahead before the invite was actually sent (never treated as an auto-d
    now: {"op":"followup","date":"DD/MM/YYYY","time":"HH:MM","source":"..","via":"teams-meeting-setup-skill","receipt":"KEY"} the confirmed follow-up or 2nd appointment (South African time).
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 436: Was a scheduled check-in actually created?
    now: # ------------------------------------------------------------------ the follow-up check-in (a scheduled task the chat creates)
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 436: If Paul reports a reschedule, was the old check-in actually cancelled, and was the existing invite updated in place via outlook_update_event rather than a duplicate created?
    now: a reschedule cancels the old same-day check-in first (receipt checkin.deleted), and the existing invite is updated, never recreated" % who)
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 438: does the line's New Business/Servicing tag match which builder was used?
    now: A new line gets the New Business / Servicing question immediately.
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 438: For Life Cover ROA, was the date pulled from the application-signing transcript?
    now: say where the confirmed date came from (the transcript, or Paul's words)" % who)
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 438: For an Investment ROA, was the later of the two candidate dates used?
    now: ["An RAR is required for {client}'s {product}, and the email is drafted in Outlook Drafts, subject:
    why: The checklist's questions are program checks where provable; the rest stay as rules in the pages.
- old line 453: Insurer Comparison (replacement scenarios) | Corrected 2026-09-16 — not a silent auto-build;
    now: Insurer Comparison (replacement scenarios) | Not a silent auto-build:
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 453: Corrected 2026-09-22 — wr-two-insurer-comparison has been superseded.
    now: life-insurer-comparison (any number of insurers);
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 453: Once Paul answers, Claude requests whatever's still needed and builds the comparison via life-insurer-comparison (the successor skill, generalized to any number of insurers) as soon as both sides are 
    now: Once Paul answers, Claude requests whatever's still needed and builds the comparison via life-insurer-comparison as soon as both sides are in hand.
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 453: Scoped to Life Cover only (not RA/Investments — investment-comparisons-skill instead).
    now: for RA and Investments see investment-comparisons-skill.
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 454: COC | Corrected 2026-09-16 — several steps added.
    now: return w.load_json(os.path.join(w.SKILL_DIR, "steps.json"))["steps"]
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 455: Corrected 2026-09-16 — once every requirement is submitted to the insurer, they underwrite the case on their own;
    now: Once every requirement is submitted to the insurer, they underwrite the case on their own;
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 455: RAR Process (replacement cases only) — corrected 2026-09-16:
    now: RAR Process (replacement cases only):
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 455: Counter Offer Letter — corrected 2026-09-16, full sequence:
    now: Counter Offer Letter — full sequence:
    why: The invite is built by teams-meeting-setup-skill; the check-in settings are printed by the program.
- old line 469: RA Lump Sum quote(s) only if amount(s) specified, up to two;
    now: an RA Lump Sum quote only if an amount is specified (one Plan 2:
    why: Kept; the lump sum line follows om-optimal-ra-proposal.
- old line 473: Section 14 (if required) | Still TBC with Paul (Master Doc itself flags this).
    now: Section 14 (if required) | Still TBC with Paul (Paul's ClickUp Master Document flags this too).
    why: Kept; the lump sum line follows om-optimal-ra-proposal.
- old line 523: playbooks/short-term-insurance.md -->
    now: # Short-Term Insurance — Stage Logic
    why: Kept.


DROPPED (each is covered by a recorded decision):
- description: "Runs a Wealth Revolution client or prospect through the : Replaced by SKILL.md 'Where the detail lives'. The rows for the Project-only changelog, the non-existent core-ff-intake.md and planner-interim-procedure are dropped (Paul agreed: dead pointers and the Planner lines, 04/11/2026).
- MS Planner is an INTERIM working surface — valid only until AdviceTech: Dropped: Paul said FORGET planner-interim-procedure and agreed to delete the Planner lines (04/11/2026).
- Testing the skill uses a real, dormant client — never fabricated. Pick: Dropped: the program is tested on an invented client; the first real run is Paul's (Paul agreed, 04/11/2026).
- Update the board index (board-index.md at the project level) — change : The cross-client board index (board-index.md) is a Project file whose location is not known; the program does not update it and the audit says so. Paul has not yet said where it is.  [NEEDS PAUL]
- Life Cover: the ROA date is the date the risk application was dated — : The ROA date rules are dropped from the board: wr-roa-builder asks for the date and owns the rule (Paul agreed, 04/11/2026).
- AdviceTech sync — out of scope until Paul reconnects the AT connector.: Replaced by references/05-publish.md (Out of scope for now), without the Planner deletion clause (Paul agreed, 04/11/2026).
- Planned rebuild of this skill's structure (not started) — Paul will re: Replaced by references/05-publish.md: the blueprint mirror is done later, when Paul says; the funnel skill owns the AdviceTech stage logic (Paul agreed, question 1, 04/11/2026).
- > Loaded from outstanding-tracking.md, referenced by the core SKILL.md: The page header note ('loaded from ... referenced by the core SKILL.md') is replaced by the program showing each page at its step.
- One recurring daily trigger per client, covering everything outstandin: Replaced: reply tracking is owned by outlook-emails-skill (an hourly weekday watcher and a one-time silence flag); Paul agreed (04/11/2026).
- Self-cleanup. Once every item on a client's outstanding list is resolv: Replaced by outlook-emails-skill, which stops its own watcher when every reply is in.
- > Loaded from sitamah-messaging.md, referenced by the core SKILL.md. F: The page header note ('loaded from ... referenced by the core SKILL.md') is replaced by the program showing each page at its step.
- Example (FYI, single fact): "Hey Sitamah! Claude here. Just completed : The worked examples are replaced by the program's fixed wording (assets/triggers.json), checked on every message; the example client names were invented (Paul, 04/11/2026).
- Before every publish, sanity-check the board's JS. A single broken str: The page has no script any more, so it cannot blank; the data is checked by the program (scripts/boardhtml.py html_problems).
