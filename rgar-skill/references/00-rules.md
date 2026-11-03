# Standing rules for the whole job (rgar-skill)

**What this is.** This skill builds the client-facing proposal email Paul sends after he has received a Retirement Goal Analysis Report (RGAR) from Alwyn. The email introduces the client's shortfall and sets up the next Teams meeting to discuss it. The output is an **HTML file**, saved to SharePoint, plus an **unsent Outlook draft** (client To, Sitamah Cc). Sitamah attaches the RGAR report and **emails the client** from Drafts (unless she cannot, or Paul chooses to send it). **Claude never sends the client email.**

**What this is not.** It does not calculate or generate the RGAR itself: that always comes from Alwyn as a PDF. It is not the Fact Find Summary skill (`fact-find-summary`), but that skill's output is a required input here. The signature belongs to `paul-email-signature`.

**Who does what.** A program drives the job one step at a time, checks every figure you enter against the client's own documents, works out the age check and the shortfall dates, fills the fixed template, builds the files and the Teams message, and checks what comes back from Outlook and Teams. You (Claude) find the documents, read them page by page, type the answers with their sources, ask Paul only what the documents cannot tell you, do the Outlook and Teams steps and run the programs as they are. You never rewrite or "fix" a program, the template or the HTML during a run.

**Rules that apply to every step**
1. Say the version line first, in exactly the words the program gives. Run the steps in order; none is skipped.
2. Source first, never invent. Every fact comes from the client's own file or from Paul's own words (recorded with the words). "It seems implied", "it is usual" and "it would make sense" are not sources. If sources disagree, STOP and ask Paul, quoting both values and where each came from.
3. Read before you write: the program serves the pages one at a time; read each fully before you acknowledge it. The figures come from THIS client's own RGAR and Fact Find Summary, never from the covering email of a previous client as a formatting shortcut.
4. Check before you claim: never say a file is saved, a draft made or a message sent until the program's proof says so. Say what was checked and what is only attested.
5. Nothing is sent without Paul's yes. His one yes (at the confirmation table) covers building, saving, the Outlook draft and the Teams message to Sitamah; the message goes only after the draft has been read back and checked. Claude never sends the client email.
6. Never overwrite a file in the client's folder without Paul's clear yes in this chat.
7. Never lower the standard: a correction, a frustrated user, a short request or a "quick" task relaxes no rule here.
8. A correction from Paul re-opens the task: fix the answer, run answers and show again (his earlier yes no longer counts), rebuild, and repeat the save, the draft and the message for everything that changed.
9. If a rule cannot be met, stop and say exactly which and why. Never hand over partial work as complete.
10. Never read the raw, fillable Fact Find as a workaround, never assume a tax rate to get a net figure from a gross one, and never read a net target off the Reduced Quote's contribution target: with no Fact Find Summary, or no net-target line in it, STOP and ask Paul.
11. No client data is ever kept in the skill. Skill changes are made only in Claude Code and uploaded as a zip; never say a change is live until Paul confirms.

**Fixed:** the email is from Paul Kafentzis (FSP45946), the Cc is always Sitamah Nathoo (admin@liferisk.co.za), the importance is High.

**Words Paul uses for this job:** "RGAR proposal", "Retirement Goal Analysis email for [Name]", or the RGAR report from Alwyn being back for a client.
