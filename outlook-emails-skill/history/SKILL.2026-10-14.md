<!-- The live skill text as of 14/10/2026 16:00 (Athens time), kept as the rule-by-rule baseline. -->
---
name: "outlook-emails-skill"
description: "Tracks Paul Kafentzis's outbound Outlook emails that need a reply: sets a scheduled check, tells Paul when a reply arrives and flags silence after a day or two. Use when sending or drafting such an email."
---

# Outlook Emails Skill — Response Tracking

Mailbox: paulk@liferisk.co.za (Paul Kafentzis).

## Index

| Section | What it covers |
|---|---|
| Universal operating rules | Nine rules that apply to every step, and the Delivery gate (5 checks) |
| Last updated and maintenance rule | Athens stamp, version, how to edit this skill |
| Signatures | Claude adds no signature; Paul pastes his own |
| Tracking emails that require a response | The rule, how to implement it with create_trigger, and its scope |
| Changelog | Five one-line rows; full history in claude/outlook-emails-skill-changelog.md |

## UNIVERSAL OPERATING RULES - READ FIRST, APPLY TO EVERY STEP OF THE TASK

*These rules come before everything else in this skill. They apply from the first message to the last, not just at the start, and they are repeated here at the top because long conversations get compressed and only the beginning of a skill survives. If anything below seems to conflict with these rules, these rules win.*

1. **Re-load this skill before you start, and again after any compression.** At the start of every run - and whenever the conversation has been summarised or compressed, or has run long - open this skill in full (Skill tool) and re-read it before you produce or change any deliverable. Never work from a summary of the rules or from memory of them.
2. **Source first - never invent.** Write only what is in the source material (transcript, quote, document, file) or in a named document this skill tells you to use. If a line is unclear, garbled or ambiguous, do not turn it into a fact: flag it to the user. "It seems implied", "it is usual" and "it would make sense" are not sources.
3. **Read before you write.** Read the source material completely and carefully - at least as many times as this skill requires - before drafting anything. Searching for keywords is not reading.
4. **Check before you claim.** Never tell the user something is done, saved, sent, visible or working until you have checked it yourself (open the file, list the folder, look at the screen). Say what you checked.
5. **Deliver everything this skill lists, every time.** A run is not finished until every deliverable this skill names has been produced AND handed over exactly the way this skill specifies (shown in chat, sent as a file in the chat, saved to the named folder). Before you reply, list each deliverable and confirm each was handed over.
6. **Every correction re-opens the whole task, not just the item.** When the user corrects anything: (a) go back to the source and re-check that point and everything related to it; (b) fix it everywhere it appears, in every deliverable; (c) re-run this skill's full checklist; (d) re-deliver every affected deliverable in full, as in rule 5. Never fix only the item named and stop.
7. **Never lower the standard.** A correction, a frustrated user, a short request or a "quick" task does not relax any rule in this skill.
8. **If a rule cannot be met, stop and say so.** State exactly which rule or step could not be completed and why. Never hand over partial work as if it were complete.
9. **Changes to a skill:** edit the existing skill, never create a new one. Update its "Last updated" stamp (Athens time) and changelog. Then put the full updated SKILL.md forward for the user to review and save using the propose_skills tool (the "Update skill" review card). Never say the change is live until the user confirms they saved it. If the card does not appear, say so plainly and ask the user how to proceed - do not claim it was delivered.

**Delivery gate for this skill (rules 5 and 6 applied):** whenever Claude sends, or drafts for Paul to send, an email that needs a reply, a run is complete only when ALL of these are done and confirmed in one line each: (1) the email was identified as needing a response, and the expected sender(s), the subject or thread and the date sent were noted; (2) tracking was set up with a scheduled task (create_trigger), not left to memory, and the scheduled task was confirmed as created; (3) Paul will be told as soon as a genuine reply arrives (not an auto-reply or out-of-office), with a one-line summary of what was said or provided; (4) Paul will be flagged if nothing substantive comes back within a business day or two; (5) no signature or sign-off block was added to the draft. After ANY correction, re-check all of (1) to (5) for the email concerned.


**Last updated:** 2026-10-14 16:00 (Athens/Greece time, EEST, UTC+3) — v7

> **Maintenance rule:** every time this skill file is created or edited, update the "Last updated" line above to the current date and time in Athens, Greece (use `TZ=Europe/Athens date` or equivalent — do not guess), bump the version number, and add a dated entry to the Changelog section at the bottom describing what changed and why. Never edit this file silently.

## Signatures — no longer handled by Claude

Claude does **not** append a signature to Outlook drafts. Paul pastes his own signature into any draft Claude compiles before sending. Do not add a sign-off block, and do not re-raise the earlier signature/logo-limitation discussion — that's closed.

## Tracking emails that require a response

**Why this exists:** Paul routinely sends or has Claude send emails that need someone else to act — insurers asked for quotes, clients asked for documents/decisions, colleagues chased for information. Left alone, these go silent in his inbox and nothing surfaces the silence back to him. Paul has asked that this be a standing rule, not something he has to request each time.

**The rule:** any time Claude sends, or drafts for Paul to send, an email that requires a response from someone else, Claude must:

1. **Track it.** Identify the sender(s) whose reply is expected, the subject/thread, and the date sent.
2. **Tell Paul as soon as a response comes in.** Check the relevant sender(s) for a genuine reply (not an auto-reply/out-of-office) and notify Paul promptly when one arrives, with a one-line summary of what they said or provided.
3. **Flag it if nothing comes back within a day or two.** If a business day or two has passed with no substantive response, tell Paul it's still outstanding — as a proactive notification, or folded into his next daily brief — rather than letting it sit silently.

**How to implement this in practice**, since a chat session doesn't stay open waiting:

- Use `create_trigger` (the scheduled-task tool) to set up the tracking — never rely on remembering to check manually in a later turn, since Claude has no persistent memory of "check this later" without a scheduled task.
- A recurring check (e.g. hourly, `cron_expression: "0 * * * *"`) works well for "notify me the moment a response arrives": search the relevant sender(s) for new/unread mail on the thread, and only push a notification when something genuinely new and substantive is found (rely on the email's read/unread status so the same reply isn't reported twice — open it via the read resource tool once reported, which marks it read). Set `notifications: {"push": true}` on the trigger so a noteworthy finish actually reaches Paul's phone; end quiet runs (nothing new) with an unremarkable one-line message so it doesn't push.
- A one-shot check (`run_once_at`, roughly 24–48 hours out, landing at a sensible morning time) covers "tell me if nothing's come back within a day or two" — it fires once, checks whether a substantive reply has arrived, and if not, flags the outstanding sender(s) clearly as part of Paul's daily brief.
- When there are several senders being chased at once (e.g. multiple insurers for one client), one recurring trigger can watch all of them together — have it drop each sender from future notifications once they've replied, and have it self-delete (`delete_trigger` on its own trigger_id) once everyone being tracked has responded, rather than continuing to run indefinitely.
- Write the trigger's prompt as a fully standalone instruction (who's being chased, why, since when, what counts as a real response vs. a non-answer) — the fired session starts with no memory of the conversation that created it.

**Scope:** this applies to outbound emails where a reply is actually expected/needed to move something forward — quote requests, chases for documents or sign-off, "please confirm by X" emails. It does not apply to routine correspondence that doesn't need tracking (e.g. a purely informational note, or a reply that closes out a thread).

## Changelog

Full original rows are archived word for word in claude/outlook-emails-skill-changelog.md.

- **v7 — 2026-10-14 16:00 Athens time:** Index added after the title, plain description, changelog shortened to one-line rows (Route 1 streamlining at Paul's request); no rule changed.
- **v6 — 2026-10-08 14:49:** Rule 9 now names the propose_skills review card and says never claim a change is live until Paul confirms.
- **v5 — 2026-10-08 15:00:** UNIVERSAL OPERATING RULES block and Delivery gate added at the top.
- **v4 — 2026-08-27 10:49:** Signature rule removed at Paul's request; skill now covers response tracking only.
- **v1 to v3 — 2026-08-27:** Created; added the Last updated stamp and changelog; added the response-tracking rule using scheduled tasks.