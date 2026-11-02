#!/usr/bin/env python3
"""Teams transcript skill: the follow-up appointment IS an action for Sitamah (Paul, 02/11/2026). Each edit must match exactly once."""
import json
import os
import sys

ROOT = "/home/user/Skills-hard-coding/client-teams-transcript-skill"


def edit(rel, pairs):
    p = os.path.join(ROOT, rel)
    t = open(p, encoding="utf-8").read()
    for old, new in pairs:
        n = t.count(old)
        if n != 1:
            sys.exit("EDIT FAILED in %s (%d matches): %r" % (rel, n, old[:100]))
        t = t.replace(old, new)
    open(p, "w", encoding="utf-8").write(t)
    print("patched", rel)


# ---- the program: drop the ban, add the required action --------------------------------------------------
edit("scripts/verify.py", [
    ('''    ("setting up the next meeting", re.compile(r"\\b(set up|arrange|book|schedule|diarise|diarize|organi[sz]e)\\b[^.]{0,40}\\b(appointment|meeting|invite)\\b|\\b(meeting|calendar) invite\\b", re.I),
     "setting up the next meeting is done in another step (teams-meeting-setup-skill): leave it out, the Next appointment line shows it"),
)
WHAT_IF =''',
     ''')
# The follow-up appointment IS an action (Paul, 02/11/2026, reversing the 29/10/2026 removal): Sitamah books it (a physical
# appointment) or sends the Teams meeting request. When one was agreed, the run must carry that action.
FOLLOWUP_ACTION = re.compile(r"\\b(set up|arrange|book|schedule|diarise|diarize|organi[sz]e|send)\\b[^.]{0,60}\\b(appointment|meeting|invite)\\b", re.I)
WHAT_IF ='''),
    ('''    # ORDER (Paul): the earliest deadline first, and nothing before what it depends on
    pos =''',
     '''    na = content.get("next_appointment") or {}
    if na.get("agreed") is True and not any(FOLLOWUP_ACTION.search(S(a.get("text"))) for a in actions):
        fail("a follow-up appointment was agreed (%r) but no action sets it up: add `Sitamah to set up the follow-up appointment` (book it, or send the Teams meeting request) as an action (Paul, 02/11/2026)" % S(na.get("text"))[:50])
    # ORDER (Paul): the earliest deadline first, and nothing before what it depends on
    pos ='''),
])

# ---- the step text Claude is shown while writing content.json ---------------------------------------------
edit("steps.json", [
    ("sending quotes, proposals or the what's-next email, and setting up the next meeting (other steps of the pipeline do those); Paul's own steps.",
     "sending quotes, proposals or the what's-next email (another step of the pipeline does that); Paul's own steps. SETTING UP THE FOLLOW-UP APPOINTMENT IS an action (Paul, 02/11/2026): when a follow-up appointment was agreed (next_appointment.agreed is true), write Sitamah to set up the follow-up appointment (book it, or send the Teams meeting request) as an action; the program fails an agreed appointment with no such action."),
])

# ---- the rule pages ------------------------------------------------------------------------------------------------
edit("references/05-accuracy.md", [
    ("Not quotes, proposals or the what's-next email (another step sends those) and not meeting invites or the next appointment (another step sets those up): Paul, 29/10/2026.",
     "Not quotes, proposals or the what's-next email (another step sends those): Paul, 29/10/2026. **Setting up the follow-up appointment IS an action for Sitamah at every meeting (Paul, 02/11/2026, reversing his 29/10/2026 removal):** she books it for a physical appointment, or sends the Teams meeting request. Write `Sitamah to set up the follow-up appointment ...` whenever one was agreed (`next_appointment.agreed` is true); the program fails a run that has an agreed appointment and no such action."),
    ("sending quotes or the what's-next email, setting up the next meeting, a what-if question to a provider,",
     "sending quotes or the what's-next email, a what-if question to a provider,"),
])
edit("references/07-teams-message.md", [
    ("Rule taken from `fact-find-summary` / `ff-population-transcript` Step 8 so the follow-up skill sends the same message.",
     "This skill makes and sends this message for every meeting type, first/Fact Find meetings included (Paul, 02/11/2026: `ff-population-transcript` and `fact-find-summary` hand over to this skill and no longer make a message of their own)."),
    ("**Once per meeting:** `ff-population-transcript` and `fact-find-summary` send this same message for a first/Fact Find meeting. If it was already sent for this meeting in this chat,",
     "**Once per meeting:** for a first/Fact Find meeting this skill is run from `ff-population-transcript` Step 7b, and those two skills no longer send their own message. If it was already sent for this meeting in this chat (for example by an earlier version of them),"),
])
edit("references/00-rules.md", [
    ("For a first/Fact Find meeting, only Output 1 comes from this skill (Output 2 is the Fact Find Summary, produced by `fact-find-summary` instead).",
     "For a first/Fact Find meeting, Output 1 and the Teams message to Sitamah come from this skill (there is no Output 2 here: the Fact Find Summary, produced by `fact-find-summary`, is that meeting's PDF)."),
])

# ---- the entry page: one more standing rule -----------------------------------------------------------------------------
p = os.path.join(ROOT, "SKILL.md")
t = open(p, encoding="utf-8").read()
i = t.index("10. Short means short:")
j = t.index("\n", i)
assert "11. " not in t[j:j + 8]
t = t[:j] + "\n11. Setting up the follow-up appointment is an action for Sitamah at every meeting where one was agreed (she books it, or sends the Teams meeting request). The program fails a run that has an agreed appointment and no such action." + t[j:]
open(p, "w", encoding="utf-8").write(t)
print("patched SKILL.md")

# ---- the example content + model note --------------------------------------------------------------------------------------
p = os.path.join(ROOT, "references", "content-example.json")
c = json.load(open(p, encoding="utf-8"))
ids = [a["id"] for a in c["actions"]]
assert "a6" not in ids
src = c["next_appointment"]["src"][0]
new = {"id": "a6", "when": "now", "text": "Sitamah to set up the follow-up appointment for Thu 15/10/2026 at 4pm (send Sam the Teams meeting request)",
       "src": [dict(src)]}
k = ids.index("a5") + 1
c["actions"].insert(k, new)
raw = open(p, encoding="utf-8").read()
indent = 2 if raw.startswith("{\n  ") else None
open(p, "w", encoding="utf-8").write(json.dumps(c, indent=indent, ensure_ascii=False) + ("\n" if raw.endswith("\n") else ""))
print("patched content-example.json (indent=%s)" % indent)
edit("references/planner-note-example.txt", [
    ("• Sitamah to keep the old Instant Life policy in place until the BrightRock policy is in force\n",
     "• Sitamah to keep the old Instant Life policy in place until the BrightRock policy is in force\n• Sitamah to set up the follow-up appointment for Thu 15/10/2026 at 4pm (send Sam the Teams meeting request)\n"),
])
