## Teams message to Sitamah (Paul's rule - every Teams meeting, every time)

Rule taken from `ff-population-transcript` Step 8 so the follow-up skill sends the same message. It does not apply to a WhatsApp call.

**When:** only AFTER the Planner page, the PDF (follow-up only) and the hand-offs are produced, checked, approved by Paul and SAVED (saved files confirmed by listing the folder back). It is the very last thing in the run. If any output is still being corrected, do not send.

**The message** (one message to Sitamah in Teams, BOLD and in a much larger font than normal chat). `build.py` writes it to `out/teams_message.txt`; use it exactly as built:

`[Name Surname] - [1st / 2nd / 3rd ...] Teams Appointment Completed: [DD/MM/YYYY] - Please see instructions in Client / Prospect Task. [Please take note of Follow Up Appt.]`

- **Appointment number:** worked out from the client's file and earlier meetings (earlier Fact Find / Follow-Up Appointment Summary Notes files), recorded in `appointment_number` with its basis in `appointment_number_basis`. For a review of an existing client use `Review Teams Appointment`. If it genuinely cannot be worked out, ask Paul; never guess.
- **Follow-up sentence - CHECK BEFORE DRAFTING:** open the finished PDF/Summary and the Planner note's `Next appointment` line and decide from THOSE. `Please take note of Follow Up Appt.` is included ONLY when they show an actual follow-up appointment that was agreed or booked (a specific date/time, or Paul and the client clearly fixing the meeting). A vague intention ("we'll chat again in February", "date to be set", "revisit later") is NOT a follow-up appointment: leave the sentence out. When the two disagree, or it is unclear, ask Paul - never assume. This is recorded in `next_appointment.agreed` and `next_appointment.check`.
- **Show your check:** in the reply that presents the message, say in one line what the Summary and Planner note say about the next appointment and therefore why the follow-up sentence is in or out.
- The date is the meeting date, always DD/MM/YYYY.

**The route is hard-coded: Zapier only.** The driver prints the exact steps for this client's message. The Microsoft 365 connector cannot send Teams messages (no ChatMessage.Send permission: 403 confirmed). Post only into the 1:1 chat labelled "(1:1 Chat) Paul Kafentzis, Sitamah Nathoo", never into a client meeting chat or any other chat. If the Zapier call fails, say so plainly and give Paul the message text to paste himself; never claim it was sent.

**Check and report:** Zapier returns a message id and sent time; report both in one line ("Sent to Sitamah in Teams at HH:MM, message id ..."). Treat the send as unconfirmed until that result is seen. Record it with `run.py receipt`: `teams.status=sent`, `teams.message_id`, `teams.sent_time`, `teams.approved_by_paul` (his own words of yes). If Paul says no: `teams.status=declined`, `teams.paul_said`. If it fails: `teams.status=failed`, `teams.detail`, `teams.text_given_to_paul=true`.

**Permission:** sending a message for Paul needs his clear yes each time. Show him the exact message and send it only after his yes - he may give that yes in the same reply that approves the deliverables. Never send earlier, never twice for the same meeting (a correction does NOT trigger a resend unless Paul asks), and never for a client whose documents are not all saved.
