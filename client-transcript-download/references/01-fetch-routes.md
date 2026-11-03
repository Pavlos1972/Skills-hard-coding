Contents: the three routes for fetching, and the Chrome route in detail.

## The routes, in this order
1. **m365 - the Microsoft 365 connector.** It holds the permission `OnlineMeetingTranscript.Read.All` (checked 03/11/2026), together with `OnlineMeetings.Read` and `OnlineMeetingRecording.Read.All`. Find the meeting (its calendar entry, `outlook_calendar_search`) and use the connector's tools to read the meeting's transcript. Save what comes back as a local file. This route is NOT proven yet: the first real run decides. If a tool is missing or returns an error, record the exact error as a failed try and go on.
2. **zapier - the Zapier Microsoft Teams tools** (the generic "API GET request" can ask Microsoft Graph for the meeting's transcripts). Also not proven. Record the result either way.
3. **chrome - Claude in Chrome.** This is Paul's explicit instruction for reading Teams in the browser: it has always worked. Steps:
   - Load the Chrome tools in one ToolSearch call, `tabs_context_mcp`, and open a **new tab** on Teams web (teams.microsoft.com, already signed in as Paul).
   - Open the meeting (Calendar or the meeting chat) and go to its Recap / Transcript tab. Confirm the meeting title and date match before downloading.
   - Download the transcript as **.docx** (Download > Download as .docx). It saves to Paul's Windows Downloads folder with a name like `{Meeting title with / replaced by _}.docx`. Wait for the download to finish. Close the Chrome tab when done.
   - Grant Downloads access on the device: `device_request_folder_access` for `C:\Users\Paul\Downloads` if not already connected (the folder mounts as `$HOME/mnt/Downloads`). Find the file with `device_bash` (`ls -lat $HOME/mnt/Downloads | head`): the newest .docx matching the meeting title.
   - Make a local copy of that file for `run.py source`. The original stays in Downloads.

## What the file may be
A Teams .docx (copied unchanged), or text from the connector (WebVTT or plain text). The program writes text as a .docx with a header made from the meeting record. Either way the program checks the result itself.

## If there is no transcript
If the Recap shows no transcript, or transcription was not started in the meeting, say exactly that. There is nothing to save and nothing to invent.
