Contents: the three routes for fetching, and the Chrome route in detail.

## The routes, in this order
1. **m365 - the Microsoft 365 connector.** It holds the permission `OnlineMeetingTranscript.Read.All` (checked 03/11/2026), together with `OnlineMeetings.Read` and `OnlineMeetingRecording.Read.All`. Find the meeting (its calendar entry, `outlook_calendar_search`) and use the connector's tools to read the meeting's transcript. Save what comes back as a local file. This route is NOT proven yet: the first real run decides. If a tool is missing or returns an error, record the exact error as a failed try and go on.
2. **zapier - the Zapier Microsoft Teams tools** (the generic "API GET request" can ask Microsoft Graph for the meeting's transcripts). Also not proven. Record the result either way.
3. **chrome - Claude in Chrome.** Paul's own instruction for reading Teams in the browser: it has always worked. It needs nothing from Paul. Steps:
   - Load the Chrome tools in one ToolSearch call, `tabs_context_mcp`, and open a **new tab** on Teams web (teams.microsoft.com, already signed in as Paul). If Chrome shows a prompt you cannot clear yourself, log the try as failed with the exact words and stop with the five-line reply: never ask Paul to click it.
   - Open the meeting (Calendar or the meeting chat) and go to its Recap / Transcript tab. Confirm the meeting title and date match before reading.
   - **If it is not connected** (the usual case): read the transcript text from the Transcript tab with the page-text tool, scrolling until the last time stamp is shown. Write it into a local text file exactly as shown: every `H:MM:SS Speaker` line and the words under it, nothing added, nothing left out. Give that file to `run.py source`. The program writes the .docx from it and checks the header, the length and the gaps itself.
   - Close the Chrome tab when done.

## What the file may be
A Teams .docx (copied unchanged), or text from the connector or the Teams page (WebVTT or plain text). The program writes text as a .docx with a header made from the meeting record. Either way the program checks the result itself.

## If there is no transcript
If the Recap shows no transcript, or transcription was not started in the meeting, say exactly that. There is nothing to save and nothing to invent.
