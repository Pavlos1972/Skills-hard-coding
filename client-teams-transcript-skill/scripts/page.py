"""Output 1 (Planner / AdviceTech note) and the Teams message to Sitamah, as code.

One note model is rendered three ways, so they can never disagree:
  - planner_note.html : the private page shown in the right-hand pane, with a Copy note button
  - planner_note.txt  : formatted text, used only if the page tool is unavailable (fallback)
  - the clipboard text/html carried by the Copy button

teams_message() builds the one-line message from `ff-population-transcript` Step 8.
"""
import html
import json

import wrlib as w

DASH = "–"
BULLET = "•"


def item_parts(it):
    """(bold_prefix, text, bold_suffix) for one bullet or action."""
    text = it["text"].strip()
    st = (it.get("status") or it.get("tag") or "").strip()
    if st.endswith(":"):
        return st, text, ""
    return "", text, st


def note_model(content, names):
    mt, c = content["meeting_type"], content["client"]
    topic = content["topic"].strip()
    if mt == "whatsapp":
        topic = "WhatsApp call, %s: %s" % (content["meeting_time"], topic)
    if mt == "first":
        pointer = ("Please view the ", names["ff_summary_stem"], " PDF in the client's Fact Find folder.")
    else:
        pointer = ("Please view the ", names["pdf_stem"], " file in the client's Fact Find folder.")
    by_key = {a["key"]: a.get("bullets") or [] for a in content.get("areas") or []}
    sections = [(w.AREA_HEADING[k], by_key[k]) for k in w.AREA_KEYS if by_key.get(k)]
    not_discussed = [w.AREA_HEADING[k] for k in w.EIGHT if not by_key.get(k)]
    return {
        "title": "%s %s %s %s" % (c["first"], c["surname"], DASH, content["meeting_date"]),
        "topic": topic, "pointer": pointer, "sections": sections, "not_discussed": not_discussed,
        "applications": content.get("applications") or [], "actions": content.get("actions") or [],
        "next": content["next_appointment"]["text"].strip(),
    }


# ------------------------------------------------------------------ text (markdown flavour)
def render_text(m, markdown=True):
    b = (lambda s: "**%s**" % s) if markdown else (lambda s: s)
    i = (lambda s: "*%s*" % s) if markdown else (lambda s: s)

    def bullet(it):
        pre, text, suf = item_parts(it)
        line = "%s %s%s" % (BULLET, (b(pre) + " ") if pre else "", text)
        return line + (" %s %s" % (DASH, b(suf)) if suf else "")

    out = [b(m["title"]), i(m["topic"]), "", m["pointer"][0] + b(m["pointer"][1]) + m["pointer"][2]]
    for heading, items in m["sections"]:
        out += ["", b(heading), ""] + [bullet(x) for x in items]
    if m["not_discussed"]:
        out += ["", "Not discussed this meeting: %s." % ", ".join(m["not_discussed"])]
    if m["applications"]:
        out += ["", b("Applications"), ""] + [bullet(x) for x in m["applications"]]
    if m["actions"]:
        out += ["", b("Actions"), ""] + [bullet(x) for x in m["actions"]]
    out += ["", "%s %s" % (b("Next appointment:"), m["next"])]
    return "\n".join(out) + "\n"


# ------------------------------------------------------------------ html page
def _esc(s):
    return html.escape(s, quote=False)


def _lines_html(m, cls):
    """List of (css class, inner html) for the visible note; cls=False gives clipboard html."""
    rows = [("t", "<b>%s</b>" % _esc(m["title"])), ("topic", "<i>%s</i>" % _esc(m["topic"])), ("sp", ""),
            ("p", "%s<b>%s</b>%s" % (_esc(m["pointer"][0]), _esc(m["pointer"][1]), _esc(m["pointer"][2])))]

    def bullet(it):
        pre, text, suf = item_parts(it)
        inner = BULLET + " " + ("<b>%s</b> " % _esc(pre) if pre else "") + _esc(text)
        if suf:
            inner += " %s <b>%s</b>" % (DASH, _esc(suf))
        return ("b", inner)

    for heading, items in m["sections"]:
        rows += [("sp", ""), ("h", "<b>%s</b>" % _esc(heading))] + [bullet(x) for x in items]
    if m["not_discussed"]:
        rows += [("sp", ""), ("p", _esc("Not discussed this meeting: %s." % ", ".join(m["not_discussed"])))]
    if m["applications"]:
        rows += [("sp", ""), ("h", "<b>Applications</b>")] + [bullet(x) for x in m["applications"]]
    if m["actions"]:
        rows += [("sp", ""), ("h", "<b>Actions</b>")] + [bullet(x) for x in m["actions"]]
    rows += [("sp", ""), ("p", "<b>Next appointment:</b> %s" % _esc(m["next"]))]
    return rows


PAGE = """<title>%(title)s</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* Layout: one narrow reading column; a bar with the Copy button above one white card holding the note. */
:root{--bg:#f4f6f9;--card:#ffffff;--fg:#1c2430;--muted:#5b6675;--border:#d6dce5;--accent:#1f3a5f;--accent-fg:#ffffff;--ok:#1d6b3a}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#11151b;--card:#1a2029;--fg:#e8ecf2;--muted:#9aa5b4;--border:#2c3542;--accent:#8fb3e8;--accent-fg:#0f1a2b;--ok:#6fd49a;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#11151b;--card:#1a2029;--fg:#e8ecf2;--muted:#9aa5b4;--border:#2c3542;--accent:#8fb3e8;--accent-fg:#0f1a2b;--ok:#6fd49a;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
main{max-width:760px;margin:0 auto;padding-block:16px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.bar{display:flex;flex-wrap:wrap;align-items:center;gap:12px;margin-bottom:12px}
.bar h1{font-size:1.1rem;margin:0;flex:1 1 auto;min-width:0;color:var(--accent)}
button{font:inherit;font-weight:600;background:var(--accent);color:var(--accent-fg);border:0;border-radius:8px;padding:10px 18px;cursor:pointer;min-height:44px}
button:focus-visible{outline:3px solid var(--fg);outline-offset:2px}
#msg{flex:1 1 100%%;min-height:1.5em;color:var(--ok);font-size:.9rem}
article{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px;overflow-wrap:anywhere;min-width:0}
article p{margin:0}
article .t{font-size:1.05rem}
article .topic{color:var(--muted)}
article .h{margin-top:2px}
article .b{padding-left:1.1em;text-indent:-1.1em}
article .sp{height:.75em}
</style>
<main>
<div class="bar"><h1>Planner note</h1><button type="button" id="copy-note">Copy note</button><div id="msg" role="status" aria-live="polite"></div></div>
<article id="note">
%(body)s
</article>
</main>
<script>
const CLIP_HTML = %(clip_html)s;
const CLIP_TEXT = %(clip_text)s;
const msg = document.getElementById("msg");
function done(text){ msg.textContent = text; }
function selectNote(){
  const r = document.createRange(); r.selectNodeContents(document.getElementById("note"));
  const s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
}
async function copyNote(){
  // 1. best: bold, italics and bullets on the clipboard (some viewers refuse this)
  try {
    if (navigator.clipboard && window.ClipboardItem) {
      await navigator.clipboard.write([new ClipboardItem({
        "text/html": new Blob([CLIP_HTML], {type: "text/html"}),
        "text/plain": new Blob([CLIP_TEXT], {type: "text/plain"})})]);
      done("Copied with bold and bullets. Paste it into the Planner / AdviceTech task chat.");
      return;
    }
  } catch (e) { /* try the next way */ }
  // 2. select the note and copy the selection (keeps the formatting)
  selectNote();
  let ok = false; try { ok = document.execCommand("copy"); } catch (e) {}
  if (ok) { done("Copied. Paste it into the Planner / AdviceTech task chat."); return; }
  // 3. plain text only (no bold), then 4. leave the note selected for Ctrl+C
  try {
    await navigator.clipboard.writeText(CLIP_TEXT);
    done("Copied as plain text (bold is lost). Paste it into the Planner / AdviceTech task chat.");
    return;
  } catch (e) { /* last resort */ }
  selectNote();
  done("The note is selected. Press Ctrl+C to copy it.");
}
document.getElementById("copy-note").addEventListener("click", copyNote);
</script>
"""


def page_title(content):
    sur = content["client"]["surname"].split()
    return "%s Planner Note" % (sur[-1] if sur else "Client")


def render_page(m, content):
    rows = _lines_html(m, True)
    body = "\n".join('<p class="%s">%s</p>' % (cls, inner or "&nbsp;") for cls, inner in rows)
    clip = "".join("<div>%s</div>" % (inner or "<br>") for _, inner in rows)
    # JSON strings are valid JS; escape "</" so the script block cannot be closed early
    js = lambda s: json.dumps(s, ensure_ascii=False).replace("</", "<\\/")
    return PAGE % {"title": _esc(page_title(content)), "body": body, "clip_html": js(clip),
                   "clip_text": js(render_text(m, markdown=False))}


# ------------------------------------------------------------------ Teams message to Sitamah
FOLLOW_UP_SENTENCE = "Please take note of Follow Up Appt."
CHAT_LABEL = "(1:1 Chat) Paul Kafentzis, Sitamah Nathoo"


def teams_message(content):
    """The one-line message (ff-population-transcript Step 8). None for a WhatsApp call."""
    if content["meeting_type"] == "whatsapp":
        return None
    c = content["client"]
    kind = "%s Teams Appointment" % w.ordinal(content["appointment_number"])
    text = "%s %s (%s) %s %s Completed: %s %s Please see instructions in Client / Prospect Task." % (
        c["first"], c["surname"], content["client_status"], DASH, kind, content["meeting_date"], DASH)
    if content["next_appointment"].get("agreed") is True:
        text += " " + FOLLOW_UP_SENTENCE
    return text


def teams_xml(text):
    return "<h1><b>%s</b></h1>" % html.escape(text, quote=False)


def zapier_steps(text):
    """The exact Zapier route, printed by the driver so nothing is recalled from memory."""
    return [
        "1. Load the tools in ONE ToolSearch call: select:mcp__Zapier__microsoft_teams_send_chat_message,mcp__Zapier__list_dynamic_enum_values",
        "2. list_dynamic_enum_values: tool_name=microsoft_teams_send_chat_message, property_name=chat, search=Sitamah. "
        "Choose the entry labelled \"%s\". Never post into any other chat." % CHAT_LABEL,
        "3. mcp__Zapier__microsoft_teams_send_chat_message: chat=<that id>, format=xml, content=%s, "
        "output_hint=message id, sent time and the body content as stored" % teams_xml(text),
        "4. Do NOT use the Microsoft 365 connector's teams_send_chat_message (no send permission: a 403 error was confirmed in real use).",
        "5. Record what Zapier returned: run.py receipt RUN --set teams.status=sent --set teams.message_id=<id> --set teams.sent_time=<time> "
        "--set teams.body_as_stored=\"<the body text Zapier says it stored>\" --set teams.approved_by_paul=\"<Paul's own words of yes>\"",
        "If Paul says no: --set teams.status=declined --set teams.paul_said=\"<his words>\". If it was already sent for this meeting by another skill: "
        "--set teams.status=already_sent --set teams.already_sent_evidence=\"<which skill, when, message id>\".",
        "If the Zapier call fails: say so plainly, give Paul the message text to paste himself, and record --set teams.status=failed --set teams.detail=\"<the error>\" --set teams.text_given_to_paul=true. Never claim it was sent.",
    ]
