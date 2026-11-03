Contents: what to record about the email, where to look it up, and what counts as tracked.

- **One email per run folder.** Several people replying to the same email are one run (list all of them in --senders). A different email is a different run.
- **Look it up first, and log the try.** Search Paul's Sent Items with the Microsoft 365 connector (`outlook_email_search` with the `recipient` filter and no folder name). The Zapier Office 365 tools can create a draft or send but cannot search, and the computer has nothing to look in: log those honestly only if you tried them. If the email is a draft Paul has not sent yet there is nothing to find: log the Microsoft 365 try as failed ("draft, not sent yet") and use TODAY as the date sent.
- **--senders:** the full address(es) a reply is expected from, comma-separated. The program refuses Paul's own address and anything that is not a real address.
- **--subject:** exactly as in the email.
- **--sent:** DD/MM/YYYY, South African date. Never in the future.
- **--why:** one line, for example "waiting for the revised quote before the follow-up". It is the reason the email needs a reply.
- **--source:** where you got the sender, subject and date, for example "Sent Items search (Microsoft 365)" or "Paul said, draft".
- **--folder** (optional): the client's folder on OneDrive/SharePoint if a reply may arrive as a dropped file instead of an email. The checks then also look there.
- The senders, subject, date and reason are typed by you, so they stay attested: the checker proves they are well formed and that the plan follows from them, not that they are true.
