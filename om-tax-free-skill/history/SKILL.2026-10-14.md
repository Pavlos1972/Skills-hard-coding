<!-- The live skill text as of 14/10/2026 15:54 (Athens time), kept as the rule-by-rule baseline. -->
---
name: "om-tax-free-skill"
description: "Builds an Old Mutual Tax-Free Investment client proposal email for Paul Kafentzis (FSP45946) from Alwyn's quote, then saves, drafts in Outlook and alerts Sitamah. Use when Paul asks for an OM Tax-Free proposal."
---

# OM Tax-Free Investment Proposal Email Builder

## Index

| # | Section | What it covers |
|---|---|---|
| 1 | Universal operating rules + Delivery gate | The nine rules for every step, and what must be done before a run counts as complete |
| 2 | Last updated + Changelog | Athens-time stamp, standing edit rule, last changes |
| 3 | Overview + What this skill is not | What the skill produces; Claude never sends the client email |
| 4 | Step 1 | Gather everything from the client's file; the "what I found" list; what is still asked in chat |
| 5 | Step 2 | Read the sources and extract the Quote figures precisely |
| 6 | Step 3 | Date calculations (always run the script) |
| 7 | Step 4 | Build the email HTML (Cc always Sitamah Nathoo, fixed table widths, naming) |
| 8 | Step 5 | Save the HTML into the client's Comparative Quotes folder (no-logo copy) |
| 9 | Step 6 | Create the Outlook draft with Claude in Chrome (never sent by Claude) |
| 10 | Step 7 | Teams message to Sitamah via Zapier (standard wording, read-back) |
| 11 | Step 8 | Pre-delivery audit (12 checks) |
| 12 | Reference material + scope | The template and date script; procedure only, no client data |

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

**Delivery gate for this skill (rules 5 and 6 applied):** a run is complete only when ALL of these are done and confirmed in one line each: (1) Step 1 was completed - the client's file was searched and every source document was found, opened and read (Steps 1-2), the "what I found" list was shown to Paul, and the Quote figures were extracted precisely; (2) the proposal email HTML was built (Step 4) and the Step 8 pre-delivery audit was completed; (3) the HTML was sent to Paul in the chat with the exact required filename; (4) Step 5 (saved into the client's folder under Comparative Quotes), Step 6 (Outlook draft, created with Claude in Chrome) and Step 7 (Teams message to Sitamah, sent via Zapier and read back) were each done and checked. After ANY correction, repeat (2) to (4) for every deliverable that changed.

**Last updated: 2026-10-14 15:54 Athens time (EEST)**

> **Standing rule — not optional:** any edit to this skill (SKILL.md, the
> template, or the date script) is not complete until the "Last updated" line
> above is also rewritten to the current date and time (Athens time), and a
> changelog row is added, in the same response as the edit.

## Changelog
| When (Athens time) | What changed |
|---|---|
| 2026-10-14 15:54 | Index added; description made plain; the long changelog rows moved word for word to the Project doc; client names and example amounts in the text replaced with placeholders. No rule changed. |
| 2026-10-13 17:12 | Aligned with the OM Optimal RA skill: Step 7 asks Sitamah to review the draft and attach the documents, fund fact sheets plural; Step 6 refinements; Step 5 saved copy always the no-logo copy; audit items 8, 9, 11 updated. |
| 2026-10-13 16:40 | Information is now gathered from the client's file, not from uploads: Step 1 rewritten, "what I found" list, source-reading rules, Step 7 Teams message now via Zapier with read-back. |
| 2026-10-08 14:36 | Rule 9 reworded: skill changes go forward with the propose_skills review card; never claim live until the user confirms they saved it. |
| 2026-10-08 14:00 | Universal operating rules block and Delivery gate added at the top. |

Older entries (2026-10-01 12:47 back to the previous version of 2026-08-04) and the full text of every row above are in `om-tax-free-skill-changelog.md` in the Project, word for word.

This skill builds the client-facing proposal email Paul sends after receiving
an Old Mutual Tax-Free Investment Quote from Alwyn. The email introduces the
client's personal circumstances, the Tax-Free product, its fund allocation
and fees, and sets up the next Teams meeting to discuss it. The output is an
**HTML file** that is (a) saved into the client's folder, (b) pasted into an
Outlook **draft** by Claude, and (c) flagged to Sitamah on Teams so she can
review the draft, attach the documents **and email the client**. **Claude never sends the email
to the client itself — Sitamah sends it from Drafts once the documents are attached
(unless she can't, or Paul chooses to send it).**

## What this skill is not

- It does not generate the OM Tax-Free Quote itself — that always comes from
  Alwyn as a PDF.
- It is not the Fact Find Summary skill — that's a separate skill
  (`fact-find-summary`). The finished Fact Find Summary is a source here and is
  read from the client's file (Step 1).

## Step 1 — Gather everything from the client's file (always first, in this order)

Every new OM Tax-Free proposal chat starts here. **Claude finds and reads the
source documents itself from the client's file on Paul's OneDrive/SharePoint —
Paul does not upload them.** Do not build a partial email: if a source below
cannot be found or read, ask Paul and wait (rule 8). Confirming that something
does not exist ("there is none") is an answer; silently skipping it is not.

**Where to look (Microsoft 365 SharePoint tools; Zapier where a Microsoft tool
cannot do the job):**
- Primary: library **"WR Clients" > "Paul Kafentzis (Client Files)" > "{Initial} - Files" > "{Surname}, {FirstName(s)}"** (e.g. `W - Files/[Surname], [FirstName(s)]`). Also check **"Company - Paul"** and the **Paul** site's `New Business > {Surname}, {FirstName}` folder when something is not in the client's Client Files folder.
- Find the client folder with `sharepoint_folder_search` (parameter `name`, e.g. "[Surname], [FirstName(s)]"). The search is a noisy partial match (it also returns sub-folders and other people's folders) — pick the folder whose name matches the client exactly and confirm by listing it with `read_resource` (`file:///{driveId}/{path or itemId}`). Read PDFs with `read_resource`.
- The client folder holds numbered sub-folders (observed 13/10/2026): `1. Overview`, `2. Fact Find`, `3. LOA & Disclosure`, `4. FICA & POI`, `5. Astute`, `6. Policy Schedules`, plus the transaction/product folders (e.g. `{Surname}, {FirstName} - (OM RA - R[amount])`).

**Collect, in this order:**

1. **Fact Find Summary** — in `2. Fact Find`. File names look like `Fact Find Summary - {DD.MM.YY} - ({Name}).pdf`; there may be more than one. Read **every** Fact Find Summary file, use the most recent by its date, and flag any difference between versions to Paul. Source of: employer, job title, gross monthly income, client full/first name for the greeting, email address, and anything else personal. Other files in that folder (the manual Fact Find, transcripts, older fact finds) are **not** used unless an item the proposal needs is missing from the summary — then say which document you used and why.
2. **Risk Tolerance questionnaire** — in `2. Fact Find`, file name `WR - New Risk Tolerance - {date} - ({name}).pdf`. Read the client's own completed result (visually read the pages — the filled-in answers are often not in the text layer) and take the **Risk Profile** from it. A file whose name still shows the literal placeholders `[date]` / `(name, surname)` is the **blank template**, not a source — never read a Risk Profile from it; flag it. If no completed questionnaire exists for this client, or its result is unclear, then (and only then) ask Paul with a button select ("Cautious", "Moderate", "Moderate-Aggressive", "Aggressive", "Other — I'll type it"). If the Fact Find Summary also states a Risk Profile, check the two agree and flag any conflict.
3. **Client Overview** — in `1. Overview`, file `WR Overview - {DD.MM.YY} - ({Surname}, {FirstName}).pdf` (an .xlsx of the same name may also be there). Read the most recent one for the client's current investments (in particular any existing Tax-Free Investment). It is a cross-check: it never replaces the Fact Find Summary as the source for personal circumstances. Report to Paul anything in it that conflicts with the Fact Find Summary or the Quote.
4. **The Tax-Free transaction folder > Comparative Quotes** — the folder whose name contains "Tax-Free" (Step 5 gives the naming: `{Surname}, {FirstName} - (OM Tax-Free - R{amount})` or, for a child's plan, `{Child's name} - (OM Tax-Free - R{amount})`), looked for first in the client's Client Files folder and then in `New Business` on the Paul site. Inside `Comparative Quotes` find and read:
   - the **OM Tax-Free Quote PDF** from Alwyn (e.g. "[Client name] - Old Mutual Savings and Income - Tax Free Plan - R[amount].pdf"), the source of client name/age, contribution amount, start date, fund allocation table and all fee/EAC figures (Step 2);
   - the **fund fact sheet(s)** for the fund(s) named in the quote;
   - the **"OM Wealth Investment Strategy Summary"** document.
   All three are attached to the email by Sitamah (Step 7), so confirm they are present and tell Paul if any is missing. If several quote versions are in the folder, use the most recent, list the others and ask Paul which is current if there is any doubt. If no Tax-Free transaction folder or no Quote can be found anywhere, stop and ask Paul where it is or to upload it — never build without the Quote.
5. **Client's email address** — from the Fact Find Summary; if absent, from the manual Fact Find or the Overview; if still absent, `microsoft_office_365_find_a_contact` via Zapier, then an Outlook email search for the client's own emails; ask Paul only if all of these fail. Never invent one. It is needed for the To line of both the HTML and the Outlook draft. State where it came from.

**Show Paul a "what I found" list before building** — one line per source: the file name, its date and the folder it came from, plus anything missing, conflicting, blank-template or unreadable. Do not build until nothing essential is missing.

**Still asked in the chat (typed, or with buttons where stated) — these cannot come from the file:**

1. **Teams meeting date(s) already held** with the client — pre-fill from the file where possible (e.g. the dates in the names of the `Teams meeting Transcript - DD.MM.YY …` / Fact Find files in `2. Fact Find`), show them to Paul and ask him to confirm or add. Collect just the calendar dates (DD/MM/YYYY) — never ask the user for the day-of-week, and never trust a day-of-week they type; always compute it (see Step 3).
2. **Next Teams meeting: day, date & time** — typed (e.g. "Friday, 17/07/2026 @ 5pm"). Confirm the date component even if the user only says a day name; the day-of-week is always computed, never typed.
3. **Confirm the policy start date** — button select, always ask even though it also appears in the Quote PDF:
   - Options: "Use the start date from the Quote PDF" / "It's changed — let me give you a new date"
   This is a deliberate double-check (per Paul's explicit instruction) since the start date can shift between when the quote was pulled and when the proposal is actually sent — never assume the Quote PDF's date is still correct without this confirmation.

**Interaction format:** use the button-selection tool for the fixed-option questions (policy start date; Risk Profile when it has to be asked); use typed input for dates and names.

**No longer asked — derived automatically, do not ask these:**
- Uploads of the Quote, Fact Find Summary, Risk questionnaire or Overview — read from the client's file instead.
- Risk Profile — read from the questionnaire (asked only as described in item 2 above).
- Day-of-week for any date — always computed, see Step 3.
- Fund allocation %, contribution amount, admin/asset management/advice fees, EAC figures — all read directly from the Quote PDF, never typed by Paul.
- Employer, job title, gross monthly income, client name — read from the Fact Find Summary; ask directly only if genuinely absent from both the Fact Find and the Quote.
- Cc — always Sitamah Nathoo (see Step 4).

## Step 2 — Read the sources and extract the Quote figures precisely

**Source-reading rules (apply to every document gathered in Step 1):**
- Read each document directly and in full — don't assume values and don't rely on file names or keyword searches.
- If a PDF has scanned/image pages (the Risk Tolerance questionnaire and manual Fact Finds often do), visually read the page images rather than relying only on extracted text — text layers often capture field labels but miss the client's actual filled-in answers. Use the `pdf-reading` skill if the content isn't already visible in context.
- Fund selection, fees, ACI and premium amounts always come from this client's own Quote — never from a previous client's proposal or from memory, even if they look similar.
- A file that is an unfilled template is not a source (see Step 1, item 2).

Then pull these exact fields from the OM Tax-Free Quote PDF — do not round
or approximate:

- **Owner name and age** ("DETAILS OF YOUR COMPREHENSIVE TAX FREE PLAN"). If
  the plan is in a child's name with the parent contracting (e.g. [Child name]
  / [Parent name]), word the personal-circumstances and product
  paragraphs so the plan is clearly in the child's name for the child's
  benefit, and name the child in the subject line, e.g. "[Parent name] (for
  [Child name]) / Old Mutual Tax Free Investment Proposal – R [amount] p.m.".
- **Regular contribution amount and start date** ("HOW WILL I CONTRIBUTE TO
  MY PLAN?").
- **Fund selection and allocations** table ("HOW WILL MY MONEY BE INVESTED?")
  — one row per fund, with its % allocation. Reproduce every fund listed,
  not just the first.
- **Total Ongoing Fees table** — asset management fee, net administration
  fee, ongoing advice fee, adviser remuneration account charge, and the
  total. These are usually spread across two sections of the quote (the
  asset management fee under "HOW MUCH WILL I PAY FOR THE MANAGEMENT OF MY
  INVESTMENT FUND(S)?", the advice fees under "WHAT IS PAID TO MY ADVISER?",
  and admin fees under "HOW MUCH WILL I PAY FOR THE ADMINISTRATION OF MY
  PLAN?") — assemble them into the single combined "Total Ongoing Fees"
  table exactly as shown in the proposal email example, not as a copy of the
  quote's own layout. If the quote shows an "as-and-when" advice line that
  is not in the total, flag it to Paul rather than silently adding or
  dropping it.

Never take these figures from a previous client's proposal email as a
formatting shortcut — always re-read them from that specific client's Quote
PDF.

Also read the **Fact Find Summary** (Step 1, item 1) for: employer, job
title, gross monthly income, and client full name/first name.

## Step 3 — Date calculations (always run the script, never hand-compute)

Use `scripts/tax_free_dates.py` for every date in the email. Do not compute
day-of-week by hand or from memory of a calendar.

```python
from datetime import date
import sys
sys.path.insert(0, "scripts")
from tax_free_dates import format_meeting_dates_list, format_date_with_day

# Opening line's meeting date(s):
meeting_line = format_meeting_dates_list([date(2026, 7, 10)])  # -> "Friday, 10/07/2026"

# Next meeting line:
next_meeting = format_date_with_day(date(2026, 7, 17)) + " @ 5pm"
```

## Step 4 — Build the email (HTML)

1. Copy `assets/OM_TaxFree_Proposal_TEMPLATE.html` to the working directory.
2. Replace every `[BRACKETED PLACEHOLDER]` with the client's actual values —
   never leave a placeholder in the delivered file.
3. **Header block — Cc is ALWAYS "Sitamah Nathoo".** Replace the template's
   `[CC EMAIL]` placeholder with `Sitamah Nathoo` in every email, every time.
   Never leave the Cc blank and never remove it. The header "To:" is the
   client's email address; the "Subject:" is the exact subject line that will
   be used on the Outlook draft in Step 6 (character for character, including
   the en dash).
4. Money figures: `R` + thousands-comma format + no decimals unless the
   source document shows decimals (match the Quote PDF's own formatting,
   e.g. "R [amount].00" if the quote shows cents, "R [amount]" if it doesn't).
5. Percentages: match the Quote PDF's own decimal precision exactly (e.g.
   "0.733%", "3.208% p.a.") — never round.
6. The fund allocation table: add one row per fund listed in the Quote PDF's
   "Fund selection and allocations" table — don't assume a single-fund
   portfolio.
7. The Personal Investment Target paragraph is fixed text, not per-client:
   "inflation plus 4-5% after asset management fees" and a "recommended
   minimum investment period" of "5-7 years" — never derive these from the
   Quote PDF or ask the user for them.
8. The "Attachments:" list follows the fixed three-line convention from the
   worked example (Tax-Free Investment Quote / Fund Fact Sheets / Wealth
   Investment Strategy Summary) — adjust only if the user tells you the
   attachment set differs for this client.
9. The fund allocation table and the Total Ongoing Fees table use a fixed
   `width="624"` (not `width="100%"`) — this is deliberate. A percentage
   width on these bordered tables loses its 680px-wrapper constraint when
   pasted into Outlook and stretches edge-to-edge across the compose window.
   Never change these back to a percentage width.
10. Run the structural sanity check before presenting:
    ```bash
    python3 -c "
    content = open('output.html').read()
    print('tables open/close:', content.count('<table'), content.count('</table>'))
    print('Sitamah in Cc:', 'Sitamah Nathoo' in content, '| placeholders left:', '[' in content and '@@' in content)
    "
    ```
11. Save the file as `[FirstName]_[Surname]_OM_TaxFree_Proposal_Email -
    [DD.MM.YY].html` (date = today's build date) and deliver it to Paul in
    the chat. Then continue with Steps 5-7 — the build is **not finished**
    until all three are done.

## Step 5 — COMPULSORY: save the HTML into the client's folder

Every proposal HTML **must** be saved into the client's transaction folder, under **Comparative Quotes** — never only shown in the chat.

- **Location:** `Paul` SharePoint site > `New Business` > `{Surname}, {FirstName}` > `{Plan owner} - (OM Tax-Free - R{amount})` > `Comparative Quotes`. Example: `New Business/[Surname], [FirstName]/[Plan owner surname], [Plan owner first name] - (OM Tax-Free - R[amount])/Comparative Quotes`. This folder already holds the OM Tax-Free Quote PDF, the fund fact sheet(s) and "OM Wealth Investment Strategy Summary"; it syncs to Paul's computer ("One" drive). Use the same folder the sources were read from in Step 1, item 4, when that was the client's Client Files transaction folder. **If the path does not exist, create the folders under the client's existing Client Files folder (`WR Clients > Paul Kafentzis (Client Files) > {Initial} - Files > {Surname}, {FirstName}`) and tell Paul** (seen with the Optimal RA run, 13/10/2026).
- **How:** if a local folder from Paul's computer is connected to the session, write the file there. If no local folder is connected (the usual case in a cloud session), find the folder with `sharepoint_folder_search` (parameter is `name`), then upload with `sharepoint_upload_file` (driveId + parentItemId of that folder, `expectedBytes` = file size, `conflictBehavior: "replace"` if re-saving after a revision). Confirm the upload by reading the folder listing.
- **No-logo copy (always):** the signature logo is a long base64 string that cannot be uploaded reliably. The copy saved to the client's folder is therefore **always the no-logo copy** (the logo `<p>` removed) — never risk a corrupt image, and never truncate or retype base64 by hand. Tell Paul plainly that the saved copy has no logo (the Outlook draft gets the logo from Paul's own Outlook signature, see Step 6). The full HTML with the logo is still the version sent to Paul in the chat (Step 4, item 11).
- If the HTML is revised (e.g. a Cc or wording fix), re-save over the same file name and tell Paul.
- Tell Paul the folder and file name in plain words when done.

## Step 6 — COMPULSORY: create the Outlook draft with Claude in Chrome

After saving, Claude puts the proposal into an Outlook **draft** (never sent by Claude):

- **To:** the client's email address. **Cc:** Sitamah Nathoo (admin@liferisk.co.za) — always. **Subject:** exactly the "Subject:" in the HTML.
- **Recommended method (most reliable):** (1) create the draft shell with the Outlook connector's `outlook_create_draft` (to, cc, subject, simple placeholder body) — this guarantees the recipients and subject; (2) open the draft in Outlook on the web with Claude in Chrome (new tab; navigate to `outlook.office365.com/mail/` first, wait, then the draft's webLink; click the edit pencil); (3) replace the body with the proposal content (everything from "Dear {Client}," to the closing line — not the header block) by dispatching a **paste event** carrying the HTML (`ClipboardEvent('paste')` with a `DataTransfer` holding `text/html`) on the `[aria-label="Message body"]` element — plain `innerHTML` assignment loses bold and table borders; use `<b>` not `font-weight`, put borders on the `td` cells, and use blank-line spacing between paragraphs (Paul's Outlook shows no gap with bare paragraph tags); (4) add Paul's signature with **Insert > Signature > "Paul K New"** (it already contains the logo, "Kind regards," and the disclaimer) — so do not include a second "Kind regards," or the template signature block in the pasted body; (5) Options > **High importance**; (6) let it autosave (wait about 8 seconds) and confirm.
- **If DOM edits made after the paste do not persist,** make the change through the editor (e.g. `execCommand`) so Outlook registers it, then re-verify.
- **Do not type into Outlook's compose fields by coordinates** — the compose pane re-lays-out as it loads and text lands in the wrong field; use element refs, and only ever one compose window. Do not press Ctrl+S in the compose window (it can insert a stray Loop component); if a Loop box appears, remove it before finishing.
- **Verify** by reading the saved draft back with `read_resource` on `mail:///messages/{id}` (the result is large — parse the saved JSON file with python): To, Cc = Sitamah, exact subject, importance high, all sections present with bold headings and bordered tables, tables open = close, exactly one "Kind regards,", signature and logo present, no Loop component and no leftover placeholder text.
- Close the Chrome tab afterwards. Delete any stray blank drafts Claude itself created while doing this (`outlook_delete_draft`) and say so.
- Attachments are **not** added by Claude — Sitamah reviews the draft, attaches them and then sends the email (Step 7).

## Step 7 — COMPULSORY: message Sitamah on Teams via Zapier (standard wording; Sitamah reviews, attaches and sends the email)

As soon as the draft is saved and verified, send Sitamah the Teams message below **through Zapier: `microsoft_teams_send_chat_message`** — **never through Claude in Chrome / Teams web**, and not the native `teams_send_chat_message` (it fails: missing `ChatMessage.Send` scope). Use `format: "markdown"` (it renders as real bold and a real numbered list in Teams — confirmed on Paul's run of 13/10/2026). Do not use `plain` or `xml`. **Sitamah reviews the draft, attaches the documents and sends the proposal email herself** — so the message asks her to review the draft and email the client. Never tell her to leave it in Drafts for Paul, unless Paul has said he will send that particular email himself (then adapt the last line on his instruction). Claude never sends the client email.

**1. Greeting — ALWAYS include one.** Check real SAST time (`TZ=Africa/Johannesburg date`): "Good morning Sitamah," before 12:00, "Good afternoon Sitamah," 12:00–17:59, "Good evening Sitamah," after. Only if that same time-of-day greeting has already been used **today in a message from Paul or Claude** in the 1:1 chat (read the chat with `read_resource` on `teams:///chats/{chatId}/messages`), use "Hi Sitamah," or "Hey Sitamah," instead. Other messages in the chat that carried no greeting do NOT remove the greeting — never start the message without one.

**2. Standard wording and format — fixed layout, only the client/product details change; bold "Action needed:" and "Drafts", numbered list, no emojis:**

> {Greeting} Sitamah,
> **Action needed:** I have compiled the draft Old Mutual Tax-Free proposal email to {Client} {(for his son/daughter {Child}, if applicable)} and saved it in **Drafts** (To: {client email}, Cc: you).
> Please kindly review that draft and attach the following to it:
> 1. The OM Tax-Free Quote ({quote file name without .pdf})
> 2. The relevant fund fact sheets as per the quote ({fund names — one fact sheet for every fund in the quote})
> 3. The "OM Wealth Investment Strategy Summary" document
>
> All three are in {Client}'s folder: {plan folder name} > Comparative Quotes.
> Once attached, please email the client - Thank you!

Example: "All three are in [Client first name]'s folder: [Plan owner name] - (OM Tax-Free - R[amount]) > Comparative Quotes." Do **not** add "please do not send it", "leave it in Drafts" or "let me know once attached" lines.

**3. How to send (Zapier):**
1. Resolve the chat with `list_dynamic_enum_values` (`tool_name` = `microsoft_teams_send_chat_message`, `property_name` = `chat`, `search` = "Sitamah Nathoo") and take the **1:1 chat** value `19:bd2a130a-35d9-459e-9025-55f356810236_e6901cee-de73-46d9-88a5-5e4a1c296418@unq.gbl.spaces` (label "(1:1 Chat) Paul Kafentzis, Sitamah Nathoo") — never a meeting chat.
2. Call `microsoft_teams_send_chat_message` with that `chat`, `format: "markdown"`, `content` = the message in Markdown (`**bold**`, a blank line between paragraphs, `1.` list items; an `output_hint` is required by the tool).
3. **Read the posted message back** with `read_resource` on `teams:///chats/{chatId}/messages/{messageId}` and confirm the body shows `<strong>` bold labels, an `<ol>` numbered list, the greeting, and no literal `**` or escaped tags; Paul can also confirm in the Teams window.
4. Never report it as sent until read back.
5. Only delete a message Claude itself posted, and only when Paul has asked for a redo; say so.

## Step 8 — Pre-delivery audit

Before calling the work finished, check every item:

1. No `[BRACKETED PLACEHOLDER]` text remains anywhere in the output.
2. Every meeting date (opening line and next-meeting line) shows a
   **computed** day-of-week, not one the user typed.
3. The policy start date was explicitly confirmed with the user in this
   conversation (Step 1, "Still asked in the chat" item 3) — not silently taken from the Quote PDF.
4. Contribution amount, fund allocation %, and every fee/EAC figure match
   the Quote PDF exactly — recheck against the PDF in the client's Comparative Quotes folder, not against what was
   typed into an earlier draft in this same conversation.
5. Personal circumstances (employer, job title, gross income, client name)
   trace to the client's own Fact Find Summary file (named in the "what I found" list), not to a guess or a previous client's
   data.
6. Risk Profile matches the client's completed WR - New Risk Tolerance questionnaire (not the blank template), or — only if none exists — what the user
   explicitly confirmed via the button prompt — never invented. Any conflict with the Fact Find Summary was flagged.
7. Header fields: "To:" is the client's real email address (never invented), its source was stated,
   "Sent:" is filled in, "Subject:" is final, and **"Cc:" shows Sitamah
   Nathoo** — never blank.
8. Signature block, WR logo, and disclaimer footer are unchanged from the
   template in the HTML sent to Paul (Step 4 never edits these); the saved copy in the client's folder is the deliberate no-logo copy.
9. The no-logo HTML copy is **saved in the client's Comparative Quotes folder** (Step 5)
   and the upload was confirmed by reading the folder listing — not merely shown in the chat.
10. The **Outlook draft exists** with To = client, Cc = Sitamah, subject
    identical to the HTML, body formatted correctly, signature/logo present,
    importance High, **not sent by Claude** (Step 6) — verified by reading it back, tables open = close, one "Kind regards,", Chrome tab closed, stray drafts deleted.
11. **Sitamah was messaged on Teams via Zapier and the posted message was read back and confirmed to render correctly** (no raw HTML tags, no literal `**`) (Step 7): it opens with a greeting, asks her to review the draft and attach the three items (Quote, fund fact sheets for every fund in the quote, Strategy Summary), names the folder, and
    ends "Once attached, please email the client - Thank you!" (no "do not send" line).
12. The final report to Paul states: which source files were read (names and dates), where the HTML was saved, the draft's
    status, that Sitamah was messaged (and will review, attach + send), and any flags
    (conflicts between Fact Find Summary versions, Overview or Risk questionnaire; blank-template files; missing fact sheet or strategy summary; fee-table assumptions, quote typos, quote expiry before the start date,
    saved copy without logo).

## Reference material

- `assets/OM_TaxFree_Proposal_TEMPLATE.html` — the fixed email template
  (header, opening, personal circumstances, product/start date, risk
  profile, product description, tax implication, penalties, personal
  investment target with fund allocation table, costs and fees table,
  attachments, closing, Paul's signature block with embedded WR logo, and
  the standard confidentiality disclaimer). Only the bracketed placeholders
  change between clients — the surrounding copy, styling, and signature
  block are fixed and were sourced directly from a real sent Paul Kafentzis
  email (a client example) for exact visual consistency with the other
  Wealth Revolution proposal emails (RGAR, OM Optimal RA). The template's
  `[CC EMAIL]` placeholder is always replaced by "Sitamah Nathoo" (Step 4,
  item 3).
- `scripts/tax_free_dates.py` — the validated date-math helper (day-of-week,
  meeting-date list formatting). Always import and use this rather than
  reasoning about calendars manually.

## A note on scope

This skill is about the *procedure*, not any specific client's data. Every
OM Tax-Free proposal should start fresh from that client's own file (Step 1)
— never reused or inferred from a previous client's figures or a prior
session's memory. If the client's documents cannot be found in the file, ask
Paul where they are rather than reusing anything from earlier in the chat.