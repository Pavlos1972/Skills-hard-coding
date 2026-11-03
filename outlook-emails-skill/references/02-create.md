Contents: creating the two scheduled tasks.

The scheduled-task tool is `create_trigger` (with `list_triggers`, `update_trigger` and `delete_trigger`). On some surfaces the names carry a prefix; use the ones your chat shows.

1. Call `create_trigger` for the WATCHER with exactly the fields in `{watch}`: name, prompt, cron_expression, create_new_session_on_fire, notifications, connectors, initiation. Nothing added, nothing dropped, nothing reworded.
2. Call `create_trigger` for the FLAG with exactly the fields in `{flag}` (it has run_once_at instead of cron_expression).
3. Each call ONCE. Copy from each result the id of the new task, and whether it warned that the task stores no connectors.
4. **If the tool refuses a field** (the phone alert, the connector list, the fresh-chat setting or the South African time zone in the schedule), STOP. Show Paul the exact error and say which field. Never drop the field, never swap it for something else, never "make it work": the plan was approved with those settings. Nothing is set up until he decides.
5. **If a result warns that the scheduled task stores no connectors**, the check could not read Outlook: record `connector_ok no`, tell Paul, and stop.
6. **Why a fresh chat each time, and why the connector:** the phone alert only works for tasks that start a fresh chat, and a fresh chat can only read Outlook if the task is allowed to use the Microsoft 365 connector (approved by Paul: that connector only).
