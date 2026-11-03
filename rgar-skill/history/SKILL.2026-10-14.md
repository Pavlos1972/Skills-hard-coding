<!-- The live skill text as of 14/10/2026 16:17 (Athens time), kept as the rule-by-rule baseline. -->
---
name: "rgar-skill"
description: "Builds the client proposal email for an RGAR from Alwyn for Paul Kafentzis (FSP45946), saves it, drafts it in Outlook and alerts Sitamah. Use when Paul asks for an RGAR proposal or Retirement Goal Analysis email."
---

# RGAR Proposal Email Builder

## Index

| Section | What it covers |
|---|---|
| Universal operating rules | Nine rules that apply to every step, and the Delivery gate (4 checks) |
| Last updated, standing rule, changelog | Athens stamp, the edit rule, five one-line rows |
| What this skill is not | The boundaries with the RGAR itself and the fact-find-summary skill |
| Step 1 - Setup checklist | What to collect first, in order, and what is derived automatically |
| Step 2 - Extract the RGAR figures | Exact fields from the RGAR PDF and the Fact Find; reading the raw Fact Find through OneDrive |
| Step 3 - Date calculations | Always run scripts/rgar_dates.py; the shortfall period rule |
| Step 4 - Build the email HTML | Template, placeholders, money format, attachments line, filename |
| Step 5 - Save to the RA transaction folder | Compulsory SharePoint save under Comparative Quotes |
| Step 6 - Outlook draft via Claude in Chrome | Draft shell, inject body, signature, High importance, verify; never sent by Claude |
| Step 7 - Teams message to Sitamah | Greeting rule, fixed wording, sending with real formatting through Chrome |
| Step 8 - Pre-delivery audit | Twelve checks before finishing |
| Reference material and scope | The template, the date script, and the signature source |

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

**Delivery gate for this skill (rules 5 and 6 applied):** a run is complete only when ALL of these are done and confirmed in one line each: (1) the Step 1 setup checklist was completed and the RGAR figures extracted precisely (Steps 1-3); (2) the proposal email HTML was built (Step 4) and the Step 8 pre-delivery audit was completed; (3) the HTML was delivered to Paul in the chat (Step 4); (4) Step 5 (saved into the client's RA transaction folder under Comparative Quotes, with a copy of the RGAR PDF), Step 6 (Outlook draft, created with Claude in Chrome) and Step 7 (Teams message to Sitamah) were each done and checked. After ANY correction, repeat (2) to (4) for every deliverable that changed.


**Last updated: 2026-10-14 16:17 Athens/Greece time (EEST)**

> **Standing rule — not optional:** any edit to this skill (SKILL.md, the template,
> or the date script) is not complete until the "Last updated" line above is also
> rewritten to the current Athens/Greece date/time, in the same response as the edit,
> and a changelog row is added.

## Changelog

Full original rows are archived word for word in claude/rgar-skill-changelog.md.

- **2026-10-14 16:17** — Index added after the title, plain description, client names and example amounts replaced with placeholders, changelog shortened to one-line rows (Route 1 streamlining at Paul's request); no rule changed.
- **2026-10-08 14:37** — Rule 9 now names the propose_skills review card and says never claim a change is live until Paul confirms.
- **2026-10-08 14:05** — UNIVERSAL OPERATING RULES block and Delivery gate added at the top.
- **2026-10-01 12:12 to 12:45** — Aligned with the OM Tax-Free workflow: Sitamah always Cc'd and she sends the email; To = client email; compulsory RA-folder save; Outlook draft via Claude in Chrome; standard Teams wording sent with real formatting via Chrome (Zapier plain text shows raw tags).
- **2026-09-25** — Signature block replaced with Paul's ground-truth signature; Athens-time stamp and changelog introduced.

This skill builds the client-facing proposal email Paul sends after receiving a
Retirement Goal Analysis Report (RGAR) from Alwyn. The email introduces the
client's shortfall and sets up the next Teams meeting to discuss it. The output is
an **HTML file**, saved to SharePoint, plus an **unsent Outlook draft** (client To,
Sitamah Cc). Sitamah attaches the RGAR report and **emails the client** from Drafts
(unless she can't, or Paul chooses to send it). Claude never sends the email itself.

## What this skill is not

- It does not calculate or generate the RGAR itself — that always comes from Alwyn
  as a PDF.
- It is not the Fact Find Summary skill — that's a separate skill
  (`fact-find-summary`), but its output is a required input here (see Step 1).

## Step 1 — Setup checklist (always ask/collect before building, in this order)

Every new RGAR proposal chat should open with these requests, in the order below.
Do not build a partial email — if something below is missing, ask for it and wait.

**Interaction format:** use the button-selection tool for any question with a
fixed/short set of options; use typed input for dates, names, and figures.

1. **Meeting date(s)** already held with the client (one or several) — typed.
   Collect just the calendar dates (DD/MM/YYYY) — never ask the user for the
   day-of-week, and never trust a day-of-week they type; always compute it (see
   Step 3). This matters: a previous hand-typed version of this email labelled
   19/02/2022 as a "Thursday" when it was actually a Saturday.
2. **Next Teams meeting date and time** (e.g. "Thursday, 02/07/2026 @ 12pm") —
   typed. This drives the shortfall start date (see Step 3), so confirm the date
   component even if the user only says a day name.
3. **The RGAR PDF** from Alwyn (e.g. "[Client Full Name] - Retirement Goal
   Analysis - 24.06.26.pdf"). Upload, or locate it in the client's SharePoint
   folder (often under an "(OM RGA)" / RGAR transaction folder > Comparative
   Quotes). Source of: DOB/age check, retirement age, "Current
   value" / "Future value" expenses, Years until retirement, and the shortfall
   figures (lump sum, monthly recurring, escalation %, sustainability age).
4. **The client's Fact Find Summary or raw Fact Find.** If the user uploads a
   Fact Find Summary (output of the `fact-find-summary` skill), use it directly.
   Otherwise, locate and read the client's raw Fact Find yourself — do not stop
   and ask the user to upload something you can go and get. Source of: employer,
   job title, gross monthly income, the client's full name/first name for the
   greeting, **the client's personal email address (the To: recipient)**, and the net monthly income target — this last one is the **"Net
   Amount Needed (today's terms)"** field under "6. What the Client Requires" →
   "Personal Risk Cover & Retirement" (not the Reduced Quote's monthly
   contribution target in the same table — that's a different figure). See
   **"Reading the raw Fact Find — go straight to OneDrive"** below for how to
   find and read it reliably; flag in your response whether you used a Fact Find
   Summary or read the raw Fact Find directly. If the net amount comes only from
   Paul's request to Alwyn and not from the raw Fact Find, say so.

**No longer asked — derived automatically, do not ask these:**
- Day-of-week for any date — always computed, see Step 3.
- The shortfall coverage period (start/end dates) — always calculated, see Step 3.
- Age, retirement age, expense/future values, shortfall amounts, escalation %,
  sustainability age — all read directly from the RGAR PDF.
- Employer, job title, gross income, net monthly income target, client name and
  email — all read directly from the Fact Find Summary / Fact Find.
- **Cc recipient — fixed: Sitamah Nathoo (admin@liferisk.co.za) is ALWAYS Cc'd.**
  Never ask, never leave blank, never remove.

## Step 2 — Extract the RGAR figures precisely

Read the RGAR PDF (use the `pdf-reading` skill if the content isn't already
visible in context) and pull these exact fields — do not round or approximate:

- **DOB and Retirement Age** (page 1, "YOUR GOAL") — used to sanity-check the
  client's current age against what's stated elsewhere, not to compute the age
  used in the email (age comes from the Fact Find Summary / what the user
  confirms, since the RGAR's DOB alone doesn't account for the exact "as at"
  date).
- **Years until retirement** (page 1, "YOUR GOAL" table) — the integer used in
  the shortfall period calculation (Step 3).
- **Expected monthly expenses in retirement — Current value** (page 1) — this is
  the "gross" figure quoted in the email's personal-circumstances paragraph.
- **Expected monthly expenses in retirement — Future value** (page 1) — the
  Future Value figure quoted in the same paragraph.
- From the **"WHAT YOU HAVE AGREED TO DO AND WHY"** section (page 2): the
  once-off lump sum contribution required, the monthly recurring contribution
  required, the debit order escalation %, and the sustainability age ("your
  income is projected to be sustainable until you are [X] years old"). These
  four values are what get *recreated as formatted text* in the email — never
  paste this section in as an image/screenshot, and never reword or summarise
  the sentences; reproduce them with the client's own figures substituted in,
  exactly matching the phrasing in
  `assets/RGAR_Proposal_Email_TEMPLATE.html`.
- **Flag to Paul** (in the final message, not in the email): if the RGAR shows a
  recurring investment of R 0, or otherwise does not appear to include the
  recurring contribution/RA being proposed to the client, say so — the
  sustainability age and shortfall may then not reflect the proposed product.

Never take these figures from the covering email of a previous client as a
formatting shortcut — always re-read them from that specific client's RGAR PDF.

Also read the **Fact Find Summary** for: employer, job title, gross monthly
income, and client full name/first name (section "2. Occupation & Income" /
"1. Client Profile"), plus the **net monthly income target in today's terms**
— this is the **"Net Amount Needed (today's terms)"** field, found under
"6. What the Client Requires" → "Personal Risk Cover & Retirement", alongside
Retirement Age and the RGAR line. Read it from that field exactly — never
confuse it with the Reduced Quote's monthly *contribution* target in the same
table, which is a different figure entirely (a savings contribution, not an
income need). If "Net Amount Needed (today's terms)" is missing or blank in a
given client's Fact Find Summary, say so explicitly and ask the user for it —
don't derive it from the gross expense figure by assuming a tax rate, and
don't leave it blank silently.

### Reading the raw Fact Find — go straight to OneDrive

No Fact Find Summary uploaded? Don't dead-end on SharePoint text extraction —
go straight to the client's OneDrive via the local-machine device bridge. This
was learned the hard way on a real client (Aug 2026): a lot of
turns were burned trying to pull his Fact Find through the Microsoft 365
connector before this route was found.

**Why SharePoint text extraction doesn't work for this document.** The
"New WR Fact Find Template" PDF is a fillable form — the labels ("Gross Income
(R)", "Name of Company", "Net Amount (Today's Terms) (R)", etc.) are real text,
but the values Paul actually typed into each field are stored as form-field
content, not page text. Every text-based read comes back with only the blank
labels, never the answers — this is true of **both**:
- `mcp__Microsoft_365__read_resource` on the file, full document or paginated,
  every page.
- `mcp__Microsoft_365__sharepoint_search` snippets, however the query is
  worded — a few fields (name, ID, phone, email) may show real values because
  they happen to sit in a plain-text part of the form, but income, occupation,
  and retirement-needs fields will not.

Don't spend more than one confirming check on either of these before switching
routes — repeating the same search with different wording doesn't help, this
is a structural limitation of text extraction, not a query problem.

**What does work: read the PDF visually through the device bridge.**

> **Reachability window:** Paul's laptop (the device this bridge reaches) is
> only on/reachable at around 8:45am on weekdays. Outside that window,
> `get_device_info` / `device_list_dir` / `device_stage_files` calls will just
> fail to find the device — that's expected, not a bug to retry around. If the
> device isn't reachable and no Fact Find Summary was uploaded, say so plainly
> and ask Paul to either upload the Fact Find Summary/raw Fact Find directly,
> or come back once his laptop is on.

1. Confirm the device is reachable: `mcp__remote-devices__get_device_info`.
2. If no folder is connected yet, request the client's OneDrive sync root —
   ask the user which top-level folder name matches their organisation if
   unsure (Paul's is `~/liferisk.co.za`):
   `mcp__remote-devices__device_request_folder_access`.
3. Navigate to the client's folder — the path mirrors the SharePoint library
   structure, e.g. `...\liferisk.co.za\Company - WR Clients\Paul Kafentzis
   (Client Files)\B - Files\{Surname, First}\2. Fact Find\` — using
   `mcp__remote-devices__device_list_dir`.
4. Stage the Fact Find PDF into the workspace:
   `mcp__remote-devices__device_stage_files`.
5. Read it with the `Read` tool and a `pages` range covering the whole
   document (e.g. `"1-18"`). This renders each page as an image, so the
   filled-in field values are visible exactly as Paul sees them on screen —
   this is the only reliable way to get them, since it doesn't depend on the
   PDF's text layer at all.

Extract every field you need directly off the rendered pages (employer, job
title, gross income, Net Amount Needed today's terms, client name/ID, etc.).
This same OneDrive-and-visual-read route also works for the RGAR PDF itself if
SharePoint text extraction is ever unreliable for a particular file, though in
practice the RGAR (a flat generated report, not a fillable form) has not shown
this problem.

## Step 3 — Date calculations (always run the script, never hand-compute)

Use `scripts/rgar_dates.py` for every date in the email. Do not compute
day-of-week or the shortfall period by hand or from memory of a calendar — it is
easy to get the day-of-week wrong (this happened in a real Paul email once — see
the script's self-check).

```python
from datetime import date
import sys
sys.path.insert(0, "scripts")
from rgar_dates import format_meeting_dates_list, format_date_with_day, shortfall_period

# Opening line's meeting date(s):
meeting_line = format_meeting_dates_list([date(2026, 6, 24)])  # -> "Wednesday, 24/06/2026"

# Next meeting line:
next_meeting = format_date_with_day(date(2026, 7, 2)) + " @ 12pm"

# Shortfall coverage period — pass the NEXT meeting date and the RGAR's
# "Years until retirement" figure:
start, end = shortfall_period(date(2026, 7, 2), 18)
```

The shortfall period rule, stated plainly: **start = the 1st of the month
immediately after the month of the next Teams meeting**; **end = start's
month/day, but `years_until_retirement` years later**. This is fixed and not
reconfirmed per client — it was explicitly confirmed against a worked example
(next meeting 02/07/2026 + 18 years until retirement → 1 August 2026 to
1 August 2044).

## Step 4 — Build the email HTML

1. Copy `assets/RGAR_Proposal_Email_TEMPLATE.html` to the working directory.
2. Replace every `[BRACKETED PLACEHOLDER]` with the client's actual values —
   never leave a placeholder in the delivered file. Header block: **To:** the
   client's email address; **Cc:** `Sitamah Nathoo` (always — replaces the
   `[CC NAME(S)]` placeholder); **Subject:** `[Client Full Name] / Retirement Goal Analysis Report`.
3. Money figures: `R` + thousands-comma format + no decimals unless the source
   document shows decimals (match the RGAR PDF's own formatting for each figure,
   e.g. "R 1,234,567" not "R 1234567" or "R 1,234,567.00" unless the RGAR itself
   shows cents).
4. The "Attachments:" header line uses the **real filename of the RGAR PDF**
   as saved by Alwyn (e.g. `Retirement Goal Analysis - 10.01.26 - [Initial] [Surname].pdf`);
   only fall back to `[Client Full Name] - Retirement Goal Analysis - [DD.MM.YY].pdf`
   if there is no real file name.
5. Run the structural sanity check before presenting:
   ```bash
   python3 -c "
   content = open('output.html').read()
   print('tables open/close:', content.count('<table'), content.count('</table>'))
   "
   ```
6. Save as `[FirstName]_[Surname]_RGAR_Proposal_Email - [DD.MM.YY].html`
   (date = today's build date). Deliver to Paul via the outputs folder / `SendUserFile`
   and tell him plainly it is the HTML copy of what is in his Drafts.

## Step 5 — COMPULSORY: save to the client's RA transaction folder

Every RGAR proposal HTML is saved to SharePoint — never skipped:

- **Location:** the client's folder under `Paul/New Business/{Surname, First}/` →
  the **RA transaction folder** (e.g. `{Surname, First} - (OM RA - R[amount])`) →
  **`Comparative Quotes`**. All RGARs are filed under the RA transaction folder,
  not under a separate RGAR folder.
- **The RGAR PDF** from Alwyn: if it sits in an "(OM RGA)" / RGA folder,
  `sharepoint_copy_item` a copy into the RA transaction folder's Comparative Quotes
  too (use `destinationParentItemId`; the original stays where it is).
- **Saving the HTML:** if the device bridge/local folder is not available, use
  `sharepoint_upload_file` (content ≤ 1 MB). Use the `expectedBytes` check — it
  detects truncation. The template carries a very long base64 logo that cannot
  be retyped reliably; in that case upload a **no-logo copy** (signature table
  logo removed) and say so — the Outlook draft takes the logo from Paul's
  Outlook signature anyway.
- Confirm the folder listing afterwards (`read_resource` on the folder).

## Step 6 — Outlook draft via Claude in Chrome (never sent by Claude)

Paul's rule: the proposal email is saved to **Drafts**, To = client email,
Cc = Sitamah Nathoo. Claude never sends; Sitamah attaches the report and sends.

1. **Create the draft shell** with `outlook_create_draft`: To = client email,
   Cc = `admin@liferisk.co.za` (Sitamah Nathoo), subject exactly as in the HTML
   header, body = a placeholder word such as `BODY_PLACEHOLDER`. To/Cc/subject
   are set reliably this way; typing into the compose fields by coordinates
   scrambles them.
2. **Open OWA in Chrome** (new tab via `tabs_context_mcp` → `tabs_create_mcp`):
   navigate to `https://outlook.office365.com/mail/` first and wait, *then*
   navigate to the draft's `webLink` and wait ~8 s (going straight to the deep
   link returns a "browser-internal URL" error). Click the edit pencil (≈ top right
   of the read view) to open compose — "Continue editing" can leave it in read view.
3. **Inject the body:** run JS on `[aria-label="Message body"]` that selects all
   and dispatches a `ClipboardEvent('paste')` with `text/html` (the email body
   only — from "Dear {First name}," to the bold next-meeting line; **no**
   header table, **no** template signature, **no** "Kind regards"). Keep a blank
   `<p style="font-size:12pt;margin:0;"> </p>` between paragraphs and use
   `<b>` for bold (Paul's blank-line spacing preference).
4. **Signature:** click at the end of the body, then Insert > Signature >
   **"Paul K New"**. It supplies "Kind regards,", the logo and the disclaimer —
   confirm there is exactly one "Kind regards,".
5. **Importance:** Options > **High importance**. Don't trust `aria-pressed`;
   confirm in step 7.
6. **Never press Ctrl+S** (it inserts a Loop component). Let autosave run
   ("Draft saved at …").
7. **Verify** with `read_resource` on `mail:///messages/{id}`: To = client
   email, Cc = Sitamah Nathoo, subject correct, body text/figures match the
   HTML, single signature with logo (inline image), `importance: "high"`, no
   Loop component, no `BODY_PLACEHOLDER`.
8. Close the Chrome tab you opened; delete any stray drafts with
   `outlook_delete_draft`. **The draft is left unsent** — Sitamah attaches the
   RGAR report and sends it (Step 7).

## Step 7 — Teams message to Sitamah (always; standard wording; Sitamah sends the email)

After the draft is verified, send Sitamah the Teams message below **through Teams in Claude in Chrome so the formatting is real** (see "How to send — formatting method" after the wording). **Do NOT use Zapier `microsoft_teams_send_chat_message` for this:** it posts plain text only, so HTML tags (`<p>`, `<strong>`, `<ol>`) show up literally in the chat (confirmed 01/10/2026 — result `contentType: text`). The native `teams_send_chat_message` tool fails (missing `ChatMessage.Send` scope). Zapier is acceptable only for a one-line plain-text message with no formatting. **Sitamah sends the proposal email herself once she has attached the RGAR report** — so the message asks her to email the client. Never tell her to leave it in Drafts for Paul, unless Paul has said he will send that particular email himself (then adapt the last line on his instruction). Claude never sends the client email.

**1. Greeting — check first, never repeat.** Read today's earlier messages in the 1:1 chat (`read_resource` on `teams:///chats/{chatId}/messages`) and check real SAST time (`TZ=Africa/Johannesburg date`). Use a time-appropriate greeting: "Good morning Sitamah," before 12:00 SAST, "Good afternoon Sitamah," 12:00–17:59, "Good evening Sitamah," after. **If a greeting of that kind was already sent that day (by Paul or Claude), do not repeat it** — use a different, neutral greeting instead ("Hi Sitamah," or "Hey Sitamah,"). Never open every message the same way.

**2. Standard wording and format — fixed layout, only the client/product details change; real Teams formatting (bold "Action needed:" and "Drafts", numbered list), never raw HTML tags or markdown symbols, no emojis:**

> {Greeting} Sitamah,
> **Action needed:** I have compiled the draft Retirement Goal Analysis (RGAR) proposal email to {Client} and saved it in **Drafts** (To: {client email}, Cc: you).
> Please kindly attach the following to that draft:
> 1. The RGAR report ({RGAR file name without .pdf})
>
> It is in {Client}'s folder: {RA transaction folder name} > Comparative Quotes.
> Once attached, please email the client - Thank you!

Do **not** add "please do not send it", "leave it in Drafts" or "let me know once attached" lines.

**3. How to send — formatting method (Claude in Chrome on Teams web):**
1. `tabs_context_mcp` → new tab → `https://teams.cloud.microsoft/` (wait ~15–25 s for it to load; open the 1:1 chat with Sitamah Nathoo — chat id `19:bd2a130a-35d9-459e-9025-55f356810236_e6901cee-de73-46d9-88a5-5e4a1c296418@unq.gbl.spaces`).
2. Click the composer ("Type a message") and type with real formatting: `ctrl+b` toggles bold (type "Action needed:", `ctrl+b` off; same for "Drafts"), `shift+Return` = new line (plain Return SENDS), type `1. ` at the start of a line for the numbered list. Type the greeting first, then each line, using `shift+Return` between lines. Add the folder line and the closing line after the list item.
3. Quirk: after a numbered list, further lines stay inside the list block (indented, un-numbered) and Return adds an empty "2." item — press BackSpace to remove it. That layout is accepted.
4. **Check the composer (zoom screenshot) before sending**, then click the **Send button** (not Return) and scroll down to confirm the posted message shows bold labels and the numbered list — no `<p>`/`<strong>` text and no literal `**`.
5. Never report the message as sent until you have seen it rendered correctly. If Teams will not load after two attempts, stop and tell Paul rather than falling back to a broken plain-text send.
6. Close the Chrome tab afterwards. Only delete a message Claude itself posted (Teams: hover > More options > Delete) and only when Paul has asked for a redo; say so.

## Step 8 — Pre-delivery audit

Before calling the work finished, check every item:

1. No `[BRACKETED PLACEHOLDER]` text remains anywhere in the output.
2. Every meeting date (opening line and next-meeting line) shows a
   **computed** day-of-week, not one the user typed or one copied from a
   previous client's email.
3. The shortfall start/end dates were produced by `shortfall_period()`, not
   estimated — re-run the script and diff if there's any doubt.
4. The four shortfall figures (lump sum, monthly, escalation %, sustainability
   age) match the RGAR PDF's "WHAT YOU HAVE AGREED TO DO AND WHY" section
   exactly — recheck against the PDF, not against what was typed into an
   earlier draft in this same conversation.
5. The recreated shortfall paragraph is **formatted text**, not a pasted image.
6. Personal circumstances (employer, job title, gross income, net monthly
   income target, client name) trace to the Fact Find Summary or the raw Fact
   Find you read directly (via OneDrive if SharePoint text extraction failed —
   see Step 2) — not to a guess, an assumed tax rate applied to the gross
   figure, or a previous client's data.
7. Header fields are filled in: **To = client email (never invent one; mark as
   a placeholder only if genuinely unknown), Cc = Sitamah Nathoo (always),**
   Subject = `{Client} / Retirement Goal Analysis Report`, Attachments = the
   real RGAR filename.
8. Signature block, WR logo, and disclaimer footer in the HTML file are
   unchanged from the template (Step 4 never edits these). The signature must
   match Paul's confirmed ground-truth signature exactly (Verdana font; name/phone in
   `#27A8E0` at 18pt; title line in `#333233` with `#7CE3FD` pipes; "Office"/
   "Email" labels `#27A8E0`; "Direct line"/"Website" labels `#00B0F0`;
   disclaimer 10pt Calibri Light italic; logo 473×169px) — if it doesn't,
   the template asset has drifted and needs re-pulling from source (see
   Reference material below), not hand-patching in this conversation.
9. The file was saved with the correct filename convention, **saved to the
   client's RA transaction folder > Comparative Quotes**, and the RGAR PDF is
   in that folder too.
10. The Outlook draft exists in Drafts, verified (To, Cc Sitamah, subject, body,
    one signature with logo, High importance), and was **not sent by Claude**.
11. Sitamah was messaged on Teams **via Chrome with real formatting, and the posted message was seen rendering correctly (no raw HTML tags)**, with the standard wording (Step 7) — greeting
    not already used that day, RGAR report listed, folder named, ending "Once
    attached, please email the client - Thank you!" (no "do not send" line).
12. The final message to Paul flags: RGAR recurring investment R 0 / mismatch
    with the proposed RA, any figure not traceable to the raw Fact Find, a
    no-logo SharePoint copy, and anything assumed (e.g. which client).

## Reference material

- `assets/RGAR_Proposal_Email_TEMPLATE.html` — the fixed email template
  (header, opening, personal circumstances, recreated shortfall text, closing,
  Paul's signature block with embedded WR logo, and the standard confidentiality
  disclaimer). Only the bracketed placeholders change between clients — the
  surrounding copy and styling are fixed and were sourced directly from a real
  sent Paul Kafentzis email. **The signature block (from the `<!-- SIGNATURE
  -->` comment to the closing `</table>` just before it) is pulled verbatim
  from Paul's own ground-truth signature file** —
  `liferisk.co.za\Company - Paul\Email Signature\Paul Kafentzis Signature.html`
  on his OneDrive (a mirror of his real Outlook signature at
  `AppData\Roaming\Microsoft\Signatures\Paul K New (paulk@liferisk.co.za).htm`)
  — not from the `om-optimal-ra-proposal` skill's asset, which was found on
  2026-09-25 to be an older, visually different copy (wrong font, wrong
  colors, wrong logo format/size). If Paul ever updates his real signature,
  re-pull it from that OneDrive file (or the AppData original) and re-splice
  it into this template rather than editing the colors/fonts by hand.
- `scripts/rgar_dates.py` — the validated date-math helper (day-of-week,
  meeting-date list formatting, shortfall period calculation). Always import
  and use this rather than reasoning about calendars manually. Running the file
  directly (`python3 rgar_dates.py`) re-runs its self-checks, including the
  worked example from this skill's design conversation.

## A note on scope

This skill is about the *procedure*, not any specific client's data. Every RGAR
proposal should start fresh from that client's own RGAR PDF and Fact
Find Summary in that conversation — never reused or inferred from a previous
client's figures or a prior session's memory.