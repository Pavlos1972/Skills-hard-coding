"""Draws the client's pipeline board from the board data: one fixed layout, the same every time, and NO script in it (a broken string
escape can no longer blank the page). The page is a pure read-out: no buttons, no inputs, no declared capabilities. The data travels inside it
as inert JSON (<script type="application/json" id="state-data">), so a later chat reads the board back from the published page.
"""
import html as _html
import json
import re

import board as b
import wrlib as w

CSS = """
:root{--bg:#f6f6f3;--card:#ffffff;--ink:#1c2230;--muted:#59627a;--line:#e1e4ec;--accent:#1f3a68;--chip:#e5edfb;--chip-ink:#1f3a68;
--claude-ink:#6a3a96;--claude-soft:#f0e7f8;--amber-bg:#fff3d0;--amber-ink:#5e4200;--amber-line:#efc65a;--warn-bg:#fdeaea;--warn-ink:#7a1f1f;--closed-bg:#ececf0}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#12151c;--card:#1b2030;--ink:#e8ebf3;--muted:#a3abc0;--line:#2c3348;--accent:#8fb0ee;--chip:#26324f;--chip-ink:#bcd0f7;
--claude-ink:#d6b8f2;--claude-soft:#33224a;--amber-bg:#3a2e0e;--amber-ink:#f6dd9a;--amber-line:#8a6a1a;--warn-bg:#3a1a1a;--warn-ink:#f4b8b8;--closed-bg:#262a38}}
:root[data-theme="dark"]{--bg:#12151c;--card:#1b2030;--ink:#e8ebf3;--muted:#a3abc0;--line:#2c3348;--accent:#8fb0ee;--chip:#26324f;--chip-ink:#bcd0f7;
--claude-ink:#d6b8f2;--claude-soft:#33224a;--amber-bg:#3a2e0e;--amber-ink:#f6dd9a;--amber-line:#8a6a1a;--warn-bg:#3a1a1a;--warn-ink:#f4b8b8;--closed-bg:#262a38}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:1080px; margin:0 auto; padding:0 1.5rem;}
@media (max-width:600px){.wrap{padding:0 16px}}
header{padding:1.6rem 0 .6rem}
h1{font-size:1.6rem;margin:0 0 .2rem;line-height:1.25}
.stamp{margin:0;color:var(--muted);font-size:.9rem}
.strip{display:flex;flex-wrap:wrap;gap:.6rem;margin:.9rem 0 .4rem}
.strip span{background:var(--chip);color:var(--chip-ink);border-radius:999px;padding:.2rem .8rem;font-size:.85rem}
.banner-closed{background:var(--closed-bg);border:2px solid var(--muted);border-radius:10px;padding:.8rem 1.2rem;margin:1.2rem 0 0;font-weight:700;letter-spacing:.02em}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:1.15rem 1.4rem 1.3rem;margin:1rem 0}
.card h2{font-size:1.15rem;margin:0 0 .5rem;display:flex;flex-wrap:wrap;align-items:center;gap:.6rem}
.card h3{font-size:.8rem;margin:1rem 0 .3rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);display:flex;align-items:center;gap:.5rem}
ul{margin:.2rem 0 0;padding-left:1.25rem;max-width:80ch}
li{margin:.2rem 0}
p{max-width:80ch;margin:.3rem 0}
.tag{background:var(--chip);color:var(--chip-ink);border-radius:6px;padding:.1rem .55rem;font-size:.78rem;font-weight:600}
.claude-tag{font-variant:small-caps;background:var(--claude-soft);color:var(--claude-ink);border-radius:999px;padding:.05rem .6rem;font-size:.78rem;font-weight:700;letter-spacing:.05em}
.prov{background:var(--amber-bg);color:var(--amber-ink);border-radius:6px;padding:0 .4rem;font-size:.75rem;font-weight:600;margin-left:.3rem}
.pending{background:var(--amber-bg);color:var(--amber-ink);border:1px solid var(--amber-line);border-radius:8px;padding:.6rem .9rem;margin:.9rem 0 0;max-width:80ch}
.pending b{display:block;font-size:.75rem;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.15rem}
.empty{color:var(--muted);font-style:italic}
.date{color:var(--muted);font-variant-numeric:tabular-nums;margin-right:.4rem}
.log-entry{border-top:1px solid var(--line);padding:.6rem 0}
.log-entry:first-of-type{border-top:0}
.log-entry h4{margin:0 0 .2rem;font-size:.95rem}
details summary{cursor:pointer;color:var(--accent);margin:.6rem 0 0}
footer{color:var(--muted);font-size:.8rem;padding:1rem 0 2rem}
"""


def esc(x):
    return _html.escape(str(x), quote=True)


def _identified(items):
    if not items:
        return '<p class="empty">Nothing recorded yet.</p>'
    out = ["<ul>"]
    for it in items:
        chip = '<span class="prov">Provisional</span>' if it.get("provisional") else ""
        out.append("<li>%s%s</li>" % (esc(it["text"]), chip))
    out.append("</ul>")
    return "\n".join(out)


def _pending(p):
    if not p:
        return ""
    return '<div class="pending"><b>Question for Paul</b>%s</div>' % esc(p["text"])


def _actions(items):
    out = ['<h3>%s <span class="claude-tag">%s</span></h3>' % (esc(b.wording()["card_labels"]["actions"]), esc(b.wording()["card_labels"]["claude_badge"]))]
    if not items:
        out.append('<p class="empty">Nothing done yet.</p>')
    else:
        out.append("<ul>")
        out += ["<li><span class=\"date\">%s</span>%s</li>" % (esc(a["date"]), esc(a["text"])) for a in items]
        out.append("</ul>")
    return "\n".join(out)


def na_text(na):
    """The next appointment for Paul's eyes: SA time first, the Greek time in brackets."""
    return "Next appointment: %s at %s SAST (%s Greek time)" % (na["date"], na["time"], w.sa_with_greek(na["date"], na["time"]).split("(")[1].rstrip(")"))


def render(board):
    """The whole page for a sealed board. board['stamp'] must be set."""
    lim = b.settings()["limits"]
    full = b.client_full(board)
    wd = b.wording()
    label = wd["prospect_label"][board["client"]["kind"]]
    ff = board["cards"]["fact_find"]
    n_q = sum(1 for cd in ["general"] + board["lines"] if board["cards"][cd].get("pending"))
    n_a = sum(len(board["cards"][cd]["actions"]) for cd in ["general"] + board["lines"])
    parts = ["<!doctype html>", '<html lang="en"><head><meta charset="utf-8">', '<meta name="viewport" content="width=device-width,initial-scale=1">',
             "<title>%s — Pipeline</title>" % esc(full), "<style>%s</style></head>" % CSS, '<body><div class="wrap">']
    if board.get("closed"):
        c = board["closed"]
        parts.append('<div class="banner-closed">%s</div>' % esc(wd["closed_banner"].format(status=c["status"], date=c["date"])))
    strip = ["<span>%d product line%s</span>" % (len(board["lines"]), "" if len(board["lines"]) == 1 else "s"),
             "<span>%d question%s for Paul</span>" % (n_q, "" if n_q == 1 else "s"), "<span>%d action%s taken</span>" % (n_a, "" if n_a == 1 else "s")]
    if ff["next_appointment"]:
        strip.append("<span>%s</span>" % esc(na_text(ff["next_appointment"])))
    parts.append('<header><h1>%s — Pipeline</h1><p class="stamp">Last updated: %s (Athens time)</p><div class="strip">%s</div></header>' % (esc(full), esc(board["stamp"]), "".join(strip)))
    # Prospect
    log = board["prospect_log"]
    pl = "<ul>" + "".join('<li><span class="date">%s</span>%s</li>' % (esc(x["date"]), esc(x["text"])) for x in log) + "</ul>" if log else '<p class="empty">No contact recorded yet.</p>'
    parts.append('<section class="card" id="prospect"><h2>%s</h2>%s</section>' % (esc(label), pl))
    # Fact Find
    na = ff["next_appointment"]
    parts.append('<section class="card" id="fact-find"><h2>Fact Find</h2><h3>%s</h3>%s%s</section>' % (
        esc(wd["card_labels"]["identified"]), _identified(ff["identified"]), "<p><b>%s</b></p>" % esc(na_text(na)) if na else ""))
    # General and the product lines
    for cd in ["general"] + board["lines"]:
        c = board["cards"][cd]
        tag = '<span class="tag">%s</span>' % esc(c["tag"]) if c.get("tag") else ""
        parts.append('<section class="card" id="%s"><h2>%s%s</h2><h3>%s</h3>%s%s%s</section>' % (
            cd.replace("_", "-"), esc(b.card_title(cd)), tag, esc(wd["card_labels"]["identified"]), _identified(c["identified"]), _pending(c.get("pending")), _actions(c["actions"])))
    # Change Log, at the very bottom
    entries = ['<article class="log-entry"><h4>%s</h4><ul>%s</ul></article>' % (esc(e["date"]), "".join("<li>%s</li>" % esc(x) for x in e["bullets"])) for e in board["change_log"]]
    if len(entries) > lim["log_fold_after"]:
        keep = lim["log_keep_open"]
        body = "".join(entries[:keep]) + "<details><summary>Show earlier changes</summary>%s</details>" % "".join(entries[keep:])
    else:
        body = "".join(entries)
    parts.append('<section class="card" id="change-log"><h2>Change Log</h2>%s</section>' % (body or '<p class="empty">No changes yet.</p>'))
    parts.append("<footer>Read-out only. Questions are answered in the chat.</footer></div>")
    data = json.dumps(board, ensure_ascii=False, sort_keys=True).replace("</", "<\\/")
    parts.append('<script type="application/json" id="state-data">%s</script>' % data)
    parts.append("</body></html>")
    return "\n".join(parts) + "\n"


def extract_state(html):
    """The board data inside a page, or None."""
    m = re.search(r'<script type="application/json" id="state-data">(.*?)</script>', html, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1).replace("<\\/", "</"))
    except ValueError:
        return None


def html_problems(html, board):
    """The checks on the page: [(ok, short, detail)]."""
    R = []

    def add(ok, short, detail=""):
        R.append((bool(ok), short, detail))
    st = extract_state(html)
    add(st is not None and st == board and b.state_sha(st) == st.get("state_sha"), "The page's data parses, matches the board and its checksum is right")
    no_state = re.sub(r'<script type="application/json" id="state-data">.*?</script>', "", html, flags=re.S)
    bad = [t for t in ("<script", "<button", "<input", "<form", "<select", "onclick", "onload", "window.claude", "javascript:") if t in no_state.lower()]
    add(not bad, "A pure read-out: no script, no buttons, no inputs, no declared capabilities" if not bad else "The page contains %s" % ", ".join(bad))
    full = b.client_full(board)
    add("<title>%s — Pipeline</title>" % esc(full) in html and html.count("<h1>") == 1, "The page is titled '%s — Pipeline'" % full)
    add("Last updated: %s (Athens time)" % board["stamp"] in html, "The Last updated stamp is the program's (Athens time: %s)" % board["stamp"])
    cards = ["prospect", "fact-find", "general"] + [ln.replace("_", "-") for ln in board["lines"]] + ["change-log"]
    pos = [html.find('id="%s"' % c) for c in cards]
    add(all(p > 0 for p in pos) and pos == sorted(pos), "The cards run in order: Prospect, Fact Find, General, the product lines, Change Log last")
    n_act = 1 + len(board["lines"])
    add(html.count('class="claude-tag"') == n_act, "Every Actions Taken label carries the CLAUDE badge (%d)" % n_act)
    add("max-width:1080px" in html and "prefers-color-scheme: dark" in html and 'name="viewport"' in html, "Width standard 1080px, dark mode and phone width are in the page")
    add(bool(board.get("closed")) == ('class="banner-closed"' in html), "The CLOSED banner shows if, and only if, the board is closed")
    ent = html.count('class="log-entry"')
    add(ent == len(board["change_log"]), "Every Change Log entry is on the page (%d)" % ent)
    lim = b.settings()["limits"]
    add((len(board["change_log"]) <= lim["log_fold_after"]) == ("<details>" not in no_state), "Older Change Log entries fold under a details block only past %d entries" % lim["log_fold_after"])
    miss = [x["text"] for cd in ["fact_find", "general"] + board["lines"] for x in board["cards"][cd].get("identified", []) if esc(x["text"]) not in html]
    add(not miss, "Every Identified point is on the page")
    return R
