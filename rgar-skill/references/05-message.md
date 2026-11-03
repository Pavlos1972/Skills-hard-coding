# The Teams message to Sitamah (through Zapier)

As soon as the draft is saved, read back and checked, message Sitamah on Teams **through Zapier: `microsoft_teams_send_chat_message`**: never through Claude in Chrome / Teams web, and not the native `teams_send_chat_message` (it fails: missing `ChatMessage.Send` scope). Use `format: "markdown"` (it renders as real bold and a real numbered list in Teams). Do not use `plain` or `xml`. Paul's one yes at the confirmation table already covers this message; the program refuses to show it before the draft check has passed.

**The wording is the program's.** `run.py message --used-today yes|no` prints it. It always opens with a greeting: "Good morning Sitamah," before 12:00, "Good afternoon Sitamah," from 12:00 to 17:59, "Good evening Sitamah," after (South African time, set by the program from the clock). Only if that same time-of-day greeting has already been used **today in a message from Paul or Claude** in the 1:1 chat (read the chat with `read_resource` on `teams:///chats/{chatId}/messages`) say `--used-today yes` and the message opens "Hi Sitamah,". Other messages in the chat that carried no greeting do NOT remove the greeting.

The message asks her to attach the RGAR report to the draft and **email the client** (Sitamah sends the proposal email herself once she has attached the report). Never add "please do not send it", "leave it in Drafts" or "let me know once attached" lines, unless Paul has said he will send that particular email himself (then he tells you how to change the last line).

**How to send**
1. Resolve the chat with `list_dynamic_enum_values` (`tool_name` = `microsoft_teams_send_chat_message`, `property_name` = `chat`, `search` = "Sitamah Nathoo") and take the **1:1 chat** value the program prints (label "(1:1 Chat) Paul Kafentzis, Sitamah Nathoo"): never a meeting chat.
2. Call `microsoft_teams_send_chat_message` with that `chat`, `format: "markdown"` and `content` = the message exactly as printed (an `output_hint` is required by the tool).
3. **Read the posted message back** with `read_resource` on `teams:///chats/{chatId}/messages/{messageId}`, save it to a file, record `message.chat` (the chat value you used) and `message.format markdown`, and run `run.py messagecheck`. The program checks the greeting, the real `<strong>` bold labels, the `<ol>` numbered list, no literal `**` and no escaped tags, the RGAR file name and the folder, and the closing line.
4. Never report it as sent until read back. Only delete a message Claude itself posted, and only when Paul has asked for a redo; say so.
