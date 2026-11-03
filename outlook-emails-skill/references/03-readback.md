Contents: reading the tasks back and what is compared.

1. Call `list_triggers`. Find the two tasks by the names in `{watch}` and `{flag}` (they end in a short code, so they are not mixed up with any other task).
2. Record what the list shows for each, with `run.py receipt`:
   - watcher: `watch.name`, `watch.cron` (its cron expression), `watch.enabled` (yes or no), `watch.next_run`, `watch.new_session` (yes when it is NOT tied to this chat, that is when it has no bound session)
   - flag: `flag.name`, `flag.run_once_at`, `flag.enabled`, `flag.next_run`, `flag.new_session`
3. Save each task's stored instruction text exactly as the list shows it into a text file and run `run.py promptfile`. The program compares it with the plan word for word.
4. The program compares everything with the plan. A red cross names the line that differs. Do not delete or change a task to make the check pass: tell Paul exactly which line is red and let him decide.
5. The list does not show the phone-alert setting or the connector list. Those two are proven only by the create call having been accepted with them, which stays attested.
