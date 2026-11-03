Contents: creating the event, telling Sitamah, a reschedule, and what to do if a tool fails.

## Create the event (new invite)
1. Load the tool: `ToolSearch` with `select:mcp__Microsoft_365__outlook_create_event`.
2. Call `mcp__Microsoft_365__outlook_create_event` ONCE, with exactly the fields in `out/invite.json` and nothing added or changed. Microsoft makes the Teams meeting and appends its join block.
3. Copy what the tool returns (the event id, subject, start, end, the attendee and whether it is an online meeting) into the receipts. The program compares them with the invite Paul approved.

## Reschedule
Load `mcp__Microsoft_365__outlook_update_event` and call it ONCE with exactly the fields in `out/invite.json` (the existing event id, the new start and end). Never delete and recreate the meeting. The body is not changed, so its closing line still names the old date: tell Paul that.

## Tell Sitamah (once, after the invite is sent)
1. Load the Zapier tools in ONE `ToolSearch` call: `select:mcp__Zapier__microsoft_teams_send_chat_message,mcp__Zapier__list_dynamic_enum_values`.
2. Find the chat with `list_dynamic_enum_values` (`tool_name` = `microsoft_teams_send_chat_message`, `property_name` = `chat`, `search` = `Sitamah`) and choose the entry labelled **"(1:1 Chat) Paul Kafentzis, Sitamah Nathoo"**. Never post into any other chat.
3. Send `out/sitamah.txt` with `microsoft_teams_send_chat_message`: `chat` = that id, `format` = `markdown`, `content` = the text exactly. Record the message id or sent time.
4. Do NOT use the Microsoft 365 connector's `teams_send_chat_message`: it lacks the permission and fails with a 403.

## If a tool fails
Say so plainly and show Paul the exact error. Do not retry the create-event call blindly (a second call could send a second invite): first look in the calendar (`outlook_calendar_search`) to see whether the event exists. If the Sitamah message fails, give Paul its text to paste. Never claim something was sent when it was not.

## The signature
It is added automatically by an Exchange transport rule to every calendar invite from Paul's mailbox. Checking the organizer's own calendar entry never shows it: verify on a real third-party recipient (the first real invite). If a client reports it missing, see `paul-email-signature`.
