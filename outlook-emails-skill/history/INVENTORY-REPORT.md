INVENTORY of the old skill: 94 sentences
  kept (word for word or nearly): 3
  reworded, with a recorded change: 46
  dropped, with a recorded decision: 45
  UNACCOUNTED: 0


REWORDED (each is covered by a recorded change):
- old line 21: Write only what is in the source material (transcript, quote, document, file) or in a named document this skill tells you to use.
    now: Changes to this skill are made only in Claude Code and uploaded by Paul.
    why: Shortened to what applies; the program records the source and refuses a missing one.
- old line 21: If a line is unclear, garbled or ambiguous, do not turn it into a fact:
    now: If a result is unclear, look in list_triggers before anything else:
    why: Shortened to what applies; the program records the source and refuses a missing one.
- old line 21: flag it to the user.
    now: "the plan is shown to Paul (no question:
    why: Shortened to what applies; the program records the source and refuses a missing one.
- old line 21: "It seems implied", "it is usual" and "it would make sense" are not sources.
    now: "it seems implied" is not a source.
    why: Shortened to what applies; the program records the source and refuses a missing one.
- old line 23: Never tell the user something is done, saved, sent, visible or working until you have checked it yourself (open the file, list the folder, look at the screen).
    now: It REBUILDS the tracking plan from the recorded facts, so nothing is taken on trust from a file Claude could have edited, and compares what the
    why: Shortened to what applies; the program records the source and refuses a missing one.
- old line 25: Every correction re-opens the whole task, not just the item.
    now: Every correction re-opens the whole task.
    why: Shortened to what applies; the program records the source and refuses a missing one.
- old line 25: When the user corrects anything:
    now: print("SELF-TEST BEFORE ANYTHING ELSE:")
    why: Shortened to what applies; the program records the source and refuses a missing one.
- old line 25: (a) go back to the source and re-check that point and everything related to it;
    now: 1 | Run it | The one command that starts the job and how every step works |
    why: Shortened to what applies; the program records the source and refuses a missing one.
- old line 25: (b) fix it everywhere it appears, in every deliverable;
    now: 1 | Run it | The one command that starts the job and how every step works |
    why: Shortened to what applies; the program records the source and refuses a missing one.
- old line 25: (c) re-run this skill's full checklist;
    now: verify.py <run_dir> [pre|final] [--full]
    why: Shortened to what applies; the program records the source and refuses a missing one.
- old line 25: (d) re-deliver every affected deliverable in full, as in rule 5.
    now: print("EVERY STEP IS DONE.\nPut this SHORT AUDIT in your reply, as it is (it is the whole report;
    why: Shortened to what applies; the program records the source and refuses a missing one.
- old line 25: Never fix only the item named and stop.
    now: show Paul the exact error and stop;
    why: Shortened to what applies; the program records the source and refuses a missing one.
- old line 26: A correction, a frustrated user, a short request or a "quick" task does not relax any rule in this skill.
    now: A correction, a frustrated user or a "quick" task never lowers the standard.
    why: Shortened to what applies; the program records the source and refuses a missing one.
- old line 30: *Delivery gate for this skill (rules 5 and 6 applied):
    now: which version of this skill is running.
    why: The Delivery gate is now done by the checker.
- old line 30: whenever Claude sends, or drafts for Paul to send, an email that needs a reply, a run is complete only when ALL of these are done and confirmed in one line each:
    now: Any email Claude sends, or drafts for Paul to send, that needs a reply from someone else is tracked, automatically, with no question each time.
    why: The Delivery gate is now done by the checker.
- old line 30: (1) the email was identified as needing a response, and the expected sender(s), the subject or thread and the date sent were noted;
    now: %s, sent %s, reply expected from %d sender(s), reason and source given" % (facts["subject"].strip()[:50], facts["sent"], len(facts["senders"]))) if not fp
    why: The Delivery gate is now done by the checker.
- old line 30: (2) tracking was set up with a scheduled task (create_trigger), not left to memory, and the scheduled task was confirmed as created;
    now: Never tell Paul tracking is set up until both scheduled tasks were created, read back with list_triggers and compared with the plan by the checker.
    why: The Delivery gate is now done by the checker.
- old line 30: (3) Paul will be told as soon as a genuine reply arrives (not an auto-reply or out-of-office), with a one-line summary of what was said or provided;
    now: A genuine reply alerts your phone with one line and that sender is dropped.
    why: The Delivery gate is now done by the checker.
- old line 30: (4) Paul will be flagged if nothing substantive comes back within a business day or two;
    now: the flag        once, 09:00 Athens time on the 2nd business day after sending (never in the past), a phone alert if anyone is outstanding;
    why: The Delivery gate is now done by the checker.
- old line 30: (5) no signature or sign-off block was added to the draft.
    now: No signature is typed into any draft;
    why: The Delivery gate is now done by the checker.
- old line 30: After ANY correction, re-check all of (1) to (5) for the email concerned.
    now: Every correction re-opens the whole task.
    why: The Delivery gate is now done by the checker.
- old line 41: ## Tracking emails that require a response
    now: "Tracks Paul Kafentzis's outbound Outlook emails that need a reply:
    why: The section heading became the skill's own title and the first rule.
- old line 43: Paul routinely sends or has Claude send emails that need someone else to act — insurers asked for quotes, clients asked for documents/decisions, colleagues chased for information.
    now: It covers quote requests, chases for documents or sign-off, "please confirm by X" emails and colleagues chased for information.
    why: Shortened: it is Paul's standing rule, so there is no question each time.
- old line 43: Left alone, these go silent in his inbox and nothing surfaces the silence back to him.
    now: this is his standing rule and nothing is sent to anyone.
    why: Shortened: it is Paul's standing rule, so there is no question each time.
- old line 43: Paul has asked that this be a standing rule, not something he has to request each time.
    now: Paul made this a standing rule and nothing is sent to anyone.
    why: Shortened: it is Paul's standing rule, so there is no question each time.
- old line 45: any time Claude sends, or drafts for Paul to send, an email that requires a response from someone else, Claude must:
    now: any time Claude sends, or drafts for Paul to send, an email that needs a reply from someone else, the reply is tracked.
    why: Now a six-step program.
- old line 47: Identify the sender(s) whose reply is expected, the subject/thread, and the date sent.
    now: %s, sent %s, reply expected from %d sender(s), reason and source given" % (facts["subject"].strip()[:50], facts["sent"], len(facts["senders"]))) if not fp
    why: 1. Track it: who, which thread, the date sent, now recorded with a reason and a source. 2. Tell Paul as soon as a response comes in: the watcher's instruction. 3. Flag it if nothing comes back: the silence flag.
- old line 48: Tell Paul as soon as a response comes in.
    now: Never tell Paul nobody has replied because a search failed.
    why: 1. Track it: who, which thread, the date sent, now recorded with a reason and a source. 2. Tell Paul as soon as a response comes in: the watcher's instruction. 3. Flag it if nothing comes back: the silence flag.
- old line 48: Check the relevant sender(s) for a genuine reply (not an auto-reply/out-of-office) and notify Paul promptly when one arrives, with a one-line summary of what they said or provided.
    now: A genuine reply alerts your phone with one line and that sender is dropped.
    why: 1. Track it: who, which thread, the date sent, now recorded with a reason and a source. 2. Tell Paul as soon as a response comes in: the watcher's instruction. 3. Flag it if nothing comes back: the silence flag.
- old line 49: Flag it if nothing comes back within a day or two.
    now: if it is a draft use today's date;
    why: 1. Track it: who, which thread, the date sent, now recorded with a reason and a source. 2. Tell Paul as soon as a response comes in: the watcher's instruction. 3. Flag it if nothing comes back: the silence flag.
- old line 49: If a business day or two has passed with no substantive response, tell Paul it's still outstanding — as a proactive notification, or folded into his next daily brief — rather than letting it sit silen
    now: Otherwise end with a clear message for Paul (this alerts his phone) naming each sender still outstanding, what was asked and since when, one line each.",
    why: 1. Track it: who, which thread, the date sent, now recorded with a reason and a source. 2. Tell Paul as soon as a response comes in: the watcher's instruction. 3. Flag it if nothing comes back: the silence flag.
- old line 51: *How to implement this in practice, since a chat session doesn't stay open waiting:
    now: for label, t, keys in (("watcher", watch, {"name", "prompt", "cron_expression", "create_new_session_on_fire", "notifications", "connectors", "initiation"}),
    why: Moved into the steps and reference pages.
- old line 53: Use create_trigger (the scheduled-task tool) to set up the tracking — never rely on remembering to check manually in a later turn, since Claude has no persistent memory of "check this later" without a
    now: If a result warns that the scheduled task stores no connectors, the check could not read Outlook:
    why: The recurring check, the one-shot check, several senders in one task, self-deletion and the standalone instruction are now fixed by the program.
- old line 54: A recurring check (e.g.
    now: fails = CHECKS[step["check"]](a.run, rj)
    why: The recurring check, the one-shot check, several senders in one task, self-deletion and the standalone instruction are now fixed by the program.
- old line 54: "0 * * * *") works well for "notify me the moment a response arrives":
    now: the checker proves they are well formed and that the plan follows from them, not that they are true.
    why: The recurring check, the one-shot check, several senders in one task, self-deletion and the standalone instruction are now fixed by the program.
- old line 54: search the relevant sender(s) for new/unread mail on the thread, and only push a notification when something genuinely new and substantive is found (rely on the email's read/unread status so the same 
    now: "The program refuses a missing or bad address, Paul's own address, a date in the future, an email so old that the watching time is over, and a missing reason or source.
    why: The recurring check, the one-shot check, several senders in one task, self-deletion and the standalone instruction are now fixed by the program.
- old line 54: true} on the trigger so a noteworthy finish actually reaches Paul's phone;
    now: out.append("the %s must start a fresh chat each time with the phone alert on (create_new_session_on_fire true, push true)" % label)
    why: The recurring check, the one-shot check, several senders in one task, self-deletion and the standalone instruction are now fixed by the program.
- old line 54: end quiet runs (nothing new) with an unremarkable one-line message so it doesn't push.
    now: If nothing new and genuine has arrived, end with one short unremarkable line and no summary, so nothing alerts his phone.",
    why: The recurring check, the one-shot check, several senders in one task, self-deletion and the standalone instruction are now fixed by the program.
- old line 55: A one-shot check (run_once_at, roughly 24–48 hours out, landing at a sensible morning time) covers "tell me if nothing's come back within a day or two" — it fires once, checks whether a substantive re
    now: one scheduled task at 09:00 Athens time on the 2nd business day after sending, alerting Paul's phone only if someone is still outstanding.
    why: The recurring check, the one-shot check, several senders in one task, self-deletion and the standalone instruction are now fixed by the program.
- old line 56: When there are several senders being chased at once (e.g.
    now: Call create_trigger for the FLAG with exactly the fields in {flag} (it has run_once_at instead of cron_expression).
    why: The recurring check, the one-shot check, several senders in one task, self-deletion and the standalone instruction are now fixed by the program.
- old line 56: multiple insurers for one client), one recurring trigger can watch all of them together — have it drop each sender from future notifications once they've replied, and have it self-delete (delete_trigg
    now: Otherwise end with a clear message for Paul (this alerts his phone) naming each sender still outstanding, what was asked and since when, one line each.",
    why: The recurring check, the one-shot check, several senders in one task, self-deletion and the standalone instruction are now fixed by the program.
- old line 57: Write the trigger's prompt as a fully standalone instruction (who's being chased, why, since when, what counts as a real response vs.
    now: out.append("the %s instruction is missing %s" % (label, what))
    why: The recurring check, the one-shot check, several senders in one task, self-deletion and the standalone instruction are now fixed by the program.
- old line 57: a non-answer) — the fired session starts with no memory of the conversation that created it.
    now: If a result warns that the scheduled task stores no connectors, the check could not read Outlook:
    why: The recurring check, the one-shot check, several senders in one task, self-deletion and the standalone instruction are now fixed by the program.
- old line 59: this applies to outbound emails where a reply is actually expected/needed to move something forward — quote requests, chases for documents or sign-off, "please confirm by X" emails.
    now: It covers quote requests, chases for documents or sign-off, "please confirm by X" emails and colleagues chased for information.
    why: Kept in the rules page.
- old line 59: It does not apply to routine correspondence that doesn't need tracking (e.g.
    now: without a reason the email does not need tracking")
    why: Kept in the rules page.
- old line 59: a purely informational note, or a reply that closes out a thread).
    now: It does not cover a purely informational note or a reply that closes a thread.
    why: Kept in the rules page.


DROPPED (each is covered by a recorded decision):
- # Outlook Emails Skill — Response Tracking: Replaced by the new short title.
- Mailbox: paulk@liferisk.co.za (Paul Kafentzis).: Paul's own address is no longer in the text (the connector knows the mailbox). It stays in the program only to refuse it as a sender to wait for (scripts/wrlib.py).
- ## Index: Replaced by the new short Index (five sections).
- ## UNIVERSAL OPERATING RULES - READ FIRST, APPLY TO EVERY STEP OF THE : The preamble and heading are replaced by the short intro of references/00-rules.md; the program shows the rules at the start and the right page at each step.
- Re-load this skill before you start, and again after any compression. : Rule 1 (re-load this skill) is replaced by the program: it shows the standing rules at the start and the right page at each step, and `run.py status` tells a chat where the job is up to after a compression.
- Read before you write. Read the source material completely and careful: Rule 3 (read before you write) concerned drafting from a source. This skill drafts nothing: the chat records the email and the program builds the plan.
- Deliver everything this skill lists, every time. A run is not finished: Rule 5 (deliver everything) is replaced by deliverables.json and the checker: a run is finished only with a PASS audit.
- Changes to a skill: edit the existing skill, never create a new one. U: Rule 9 (changes through the propose_skills card) is replaced by standard S7: skills are changed only in Claude Code and uploaded as a zip by Paul; the 'never say it is live' part is standing rule 6 in SKILL.md.
- Last updated: 2026-10-14 16:00 (Athens/Greece time, EEST, UTC+3) — v7: The hand-typed stamp, version and maintenance rule are replaced by the stamp program (S2).
- ## Signatures — no longer handled by Claude: The Signatures section is dropped (Paul's answer 5, 03/11/2026): `paul-email-signature` says an Exchange rule adds the signature. One line remains (references/00-rules.md rule 7).
- Full original rows are archived word for word in claude/outlook-emails: The changelog table is replaced by the stamp program: the last five changes are in SKILL.md and the full history is in the repo's history folder.
