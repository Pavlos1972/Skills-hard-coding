"""The model of the funnel skill: the stage routes as data, the checks on them, the stage cards, the rules a plan for AdviceTech must follow.

Everything here is a rule that can be proved on text and data. What it cannot prove: that the funnel logic is right (that is Paul's), and that AdviceTech holds
what the register says (the chat reads AdviceTech with the AdviceTech skill's methods and records the read-back; the program checks the record).
"""
import os
import re

import wrlib as w

ASSETS = os.path.join(w.SKILL_DIR, "assets")
ROLES = ("streamlined", "master_plan", "register", "logic_flow", "flow_comparison", "automation")
KINDS = ("question", "move", "build", "test", "docs", "review")
OBJECT_TYPES = ("checklist", "section", "board", "category", "subcategory")
LINE_KINDS = ("action", "received", "yesno", "applicable", "question", "automation", "subheading", "outcome")

_cache = {}


def _load(name):
    if name not in _cache:
        _cache[name] = w.load_json(os.path.join(ASSETS, name))
    return _cache[name]


def funnel():
    return _load("funnel.json")


def status():
    return _load("status.json")


def settings():
    return _load("settings.json")


def stages():
    return {s["id"]: s for s in funnel()["stages"]}


# ------------------------------------------------------------------ the routes
def route_problems(d=None):
    """The consistency of the stage routes. [] = consistent."""
    d = d or funnel()
    out = []
    ids = [s["id"] for s in d["stages"]]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        out.append("stage code(s) listed twice: %s" % ", ".join(dup))
    S = {s["id"]: s for s in d["stages"]}
    for s in d["stages"]:
        if s.get("owner") not in (None,) + tuple(d["owners"]):
            out.append("%s: owner %r is not SR, PK or CL" % (s["id"], s.get("owner")))
        for o in s["outcomes"]:
            for t in o["to"]:
                if t not in S:
                    out.append("%s: the route '%s' leads to %s, which is not a stage" % (s["id"], o["label"], t))
            if len(o["to"]) > 1 and not set(o["to"]) <= set(d.get("parallel_ok") or []):
                out.append("%s: the route '%s' opens several stages together (%s)" % (s["id"], o["label"], ", ".join(o["to"])))
        if not s["outcomes"] and not s.get("end"):
            out.append("%s: dead end (no route out and not an end state)" % s["id"])
    for pair in d.get("exclusive") or []:
        for s in d["stages"]:
            for o in s["outcomes"]:
                if set(pair) <= set(o["to"]):
                    out.append("%s: the route '%s' opens mutually exclusive stages %s together" % (s["id"], o["label"], " and ".join(pair)))
    # reachable from the entry stages
    seen, todo = set(), [s["id"] for s in d["stages"] if s.get("entry")]
    if not todo:
        out.append("no entry stage is marked")
    while todo:
        x = todo.pop()
        if x in seen or x not in S:
            continue
        seen.add(x)
        todo += [t for o in S[x]["outcomes"] for t in o["to"]]
    miss = [i for i in ids if i not in seen]
    if miss:
        out.append("not reachable from any entry stage: %s" % ", ".join(miss))
    # every loop has a way out (strongly connected parts with a cycle must leave or end)
    for comp in _sccs(S):
        cyc = len(comp) > 1 or any(x in [t for o in S[x]["outcomes"] for t in o["to"]] for x in comp)
        if not cyc:
            continue
        leaves = any(t not in comp for x in comp for o in S[x]["outcomes"] for t in o["to"] if t in S) or any(S[x].get("end") for x in comp)
        if not leaves:
            out.append("loop without an exit: %s" % ", ".join(sorted(comp)))
    return out


def _sccs(S):
    index, low, on, stack, res, counter = {}, {}, set(), [], [], [0]
    import sys
    sys.setrecursionlimit(5000)

    def strong(v):
        index[v] = low[v] = counter[0]
        counter[0] += 1
        stack.append(v)
        on.add(v)
        for o in S[v]["outcomes"]:
            for t in o["to"]:
                if t not in S:
                    continue
                if t not in index:
                    strong(t)
                    low[v] = min(low[v], low[t])
                elif t in on:
                    low[v] = min(low[v], index[t])
        if low[v] == index[v]:
            comp = set()
            while True:
                x = stack.pop()
                on.discard(x)
                comp.add(x)
                if x == v:
                    break
            res.append(comp)

    for v in S:
        if v not in index:
            strong(v)
    return res


def stats(d=None):
    d = d or funnel()
    return len(d["stages"]), sum(len(s["outcomes"]) for s in d["stages"]), len([s for s in d["stages"] if s.get("owner") is None])


# ------------------------------------------------------------------ codes in text
CODE = re.compile(r"(?<![\w-])(?:G\d+[ab]?|R\d|[ABC]\d{1,2}[a-h]?t?|D1)(?![\w-])")


def valid_code(code, S=None):
    S = S or stages()
    return code in S or any(i.startswith(code) for i in S)


def split_codes(text):
    return [c.strip() for c in re.split(r"[,\s]+", text or "") if c.strip()]


def stage_card(code):
    s = stages()[code]
    nm = s["name"] or "(name not stated in the skill: read it in the AT MASTER PLAN)"
    lines = ["%s  %s%s" % (code, nm, ("   [%s]" % s["note"]) if s.get("note") else ""),
             "   owner: %s    page: references/%s%s" % (s["owner"] or "not stated in the skill (read it in the AT MASTER PLAN)", s["page"], "    END STATE: " + s["end"] if s.get("end") else "")]
    for o in s["outcomes"]:
        lines.append("   - %s -> %s" % (o["label"], " + ".join(o["to"])))
    return "\n".join(lines)


def page_names():
    d = os.path.join(w.SKILL_DIR, "references")
    return sorted(f for f in os.listdir(d) if f.endswith(".md")) if os.path.isdir(d) else []


def read_page(name):
    with open(os.path.join(w.SKILL_DIR, "references", name), encoding="utf-8") as f:
        return expand(f.read())


def expand(text):
    """Draws the numbers of assets/status.json into a page: {counts.NAME} and {as_of}."""
    st = status()

    def rep(m):
        if m.group(2):
            return st["as_of"]
        v = st["counts"].get(m.group(1))
        return m.group(0) if v is None else format(v, ",")
    return re.sub(r"\{counts\.(\w+)\}|(\{as_of\})", rep, text)


def pages_problems(skill_dir=None):
    """Checks of the skill's own pages: every stage code exists, no count is typed by hand, every placeholder has a value."""
    skill_dir = skill_dir or w.SKILL_DIR
    S = stages()
    out = []
    st = status()
    files = [os.path.join(skill_dir, "SKILL.md")]
    rd = os.path.join(skill_dir, "references")
    if os.path.isdir(rd):
        files += [os.path.join(rd, f) for f in sorted(os.listdir(rd)) if f.endswith(".md")]
    for path in files:
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            text = f.read()
        name = os.path.relpath(path, skill_dir)
        body = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
        body = re.sub(r"\*\*Last updated:.*", "", body)
        bad = sorted({c for c in CODE.findall(body) if not valid_code(c, S)})
        if bad:
            out.append("%s: stage code(s) not in the funnel data: %s" % (name, ", ".join(bad)))
        for m in re.finditer(r"\b(\d{1,3}(?:,\d{3})+|\d{3,})\s+(?:item\s+rows|lines|checklists|triggers)\b|\b\d+\s+of\s+\d+\s+checklists\b", body):
            out.append("%s: a count typed by hand ('%s'): counts live in assets/status.json and pages use {counts.NAME}" % (name, m.group(0)))
        for m in re.finditer(r"\{counts\.(\w+)\}", body):
            if m.group(1) not in st["counts"]:
                out.append("%s: placeholder %s has no value in status.json" % (name, m.group(0)))
    return out


# ------------------------------------------------------------------ the rules a plan for AdviceTech must follow
OWNER_PREFIX = re.compile(r"^(SR|PK|CL) – ")
ENDINGS = {"received": ("— Received",), "yesno": ("– YES / NO?",), "applicable": ("— if applicable",), "question": ("TICK DONE = YES / SKIP = NO",),
           "automation": ("— TICK DONE TO OPEN BELOW", "— IF THE ANSWER BELOW IS YES", "— WHATEVER THE ANSWER BELOW")}


def _caps_ok(text):
    outside = re.sub(r'"[^"]*"', "", text)
    return outside == outside.upper()


def line_problems(line):
    t = (line.get("text") or "").strip()
    k = line.get("kind")
    if k not in LINE_KINDS:
        return ["line kind %r is not one of %s" % (k, ", ".join(LINE_KINDS))]
    out = []
    if not t:
        return ["a line is empty"]
    if k in ("subheading", "outcome"):
        if not _caps_ok(t):
            out.append("'%s' is a %s and must be typed in CAPITALS" % (t[:60], k))
        return out
    if not OWNER_PREFIX.match(t):
        out.append("'%s' must start with 'SR – ', 'PK – ' or 'CL – ' (en dash)" % t[:60])
    if k in ENDINGS and not any(t.endswith(e) for e in ENDINGS[k]):
        out.append("'%s' is a %s line and must end with %s" % (t[:60], k, " or ".join("'%s'" % e for e in ENDINGS[k])))
    if k == "question" and "QUESTION:" not in t:
        out.append("'%s' is a question line and must contain 'QUESTION:'" % t[:60])
    if k == "automation":
        if "AUTOMATION" not in t:
            out.append("'%s' is an AUTOMATION row and must contain 'AUTOMATION'" % t[:60])
        if not _caps_ok(t):
            out.append("'%s' is an AUTOMATION row and must be typed in CAPITALS (names inside quotes excepted)" % t[:60])
    return out


def object_key(o):
    return "%s:%s" % (o.get("type"), o.get("id"))


def plan_problems(plan, kind, declared, registered_roles, test_client=None):
    """Everything about a plan that a program can prove. [] = nothing wrong."""
    st = status()
    out = []
    if not isinstance(plan, dict):
        return ["the plan file must be a JSON object"]
    if len((plan.get("decision") or "").strip()) < 5:
        out.append("decision: give the change a name (for example 'Decision 56 – ...')")
    if len((plan.get("paul_request") or "").strip()) < 5:
        out.append("paul_request: Paul's own words that asked for this")
    S = stages()
    for c in plan.get("stages") or []:
        if c not in declared:
            out.append("stages: %s was not declared with 'run.py stages' (so no read proof exists for it)" % c)
        elif c not in S:
            out.append("stages: %s is not a stage" % c)
    docs = plan.get("documents") or []
    seen = set()
    for dct in docs:
        r = dct.get("role")
        if r not in ROLES:
            out.append("documents: role %r is not one of %s" % (r, ", ".join(ROLES)))
        elif r in seen:
            out.append("documents: %s is listed twice" % r)
        elif r not in registered_roles:
            out.append("documents: %s was not located (run.py doc ... --role %s)" % (r, r))
        seen.add(r)
        if len((dct.get("change") or "").strip()) < 5:
            out.append("documents: say what changes in %s" % r)
    if kind in ("docs", "review") and not docs:
        out.append("documents: a document edit lists the documents it changes")
    if kind == "build" and not docs and not (plan.get("documents_unchanged_reason") or "").strip():
        out.append("documents: documents first. List the documents that change before AdviceTech is touched, or give documents_unchanged_reason")
    objs = plan.get("objects") or []
    if kind in ("build",) and not objs:
        out.append("objects: a build lists the AdviceTech objects it changes")
    if kind in ("docs", "review") and objs:
        out.append("objects: a document edit or a review does not touch AdviceTech (AdviceTech comes after the documents, as its own build run)")
    keys = []
    nt = st["never_touch"]
    for o in objs:
        key = object_key(o)
        keys.append(key)
        t, i = o.get("type"), o.get("id")
        if t not in OBJECT_TYPES:
            out.append("%s: type must be one of %s" % (key, ", ".join(OBJECT_TYPES)))
        if not isinstance(i, int):
            out.append("%s: the AdviceTech id must be a number" % key)
        if (t == "checklist" and i in nt["checklists"]) or (t == "section" and i in nt["sections"]):
            out.append("%s: REFUSED. This is %s's item and is never touched (checklists %s, Sections %s)" % (key, nt["owner"], ", ".join("#%d" % x for x in nt["checklists"]), ", ".join(str(x) for x in nt["sections"])))
        title = (o.get("title") or "").strip()
        if not title:
            out.append("%s: a title is needed" % key)
        if "claude" in title.lower():
            out.append("%s: no 'Claude' in any AdviceTech name (the title has it)" % key)
        if t == "section" and not re.search(r"\((SR|PK|CL)\)\s*$", title):
            out.append("%s: a Section name ends with its owner, for example 'A1 — Info Gathering (SR)'" % key)
        if t in ("checklist", "section"):
            sc = o.get("stage")
            if sc not in S and not (sc and valid_code(sc, S)):
                out.append("%s: stage %r is not a stage of the funnel" % (key, sc))
            elif sc not in declared:
                out.append("%s: stage %s was not declared with 'run.py stages'" % (key, sc))
        if t == "checklist":
            lines = o.get("lines")
            if not isinstance(lines, list) or not lines:
                out.append("%s: list its lines (text and kind)" % key)
                continue
            if o.get("expect_lines") != len(lines):
                out.append("%s: expect_lines is %r but %d line(s) are listed" % (key, o.get("expect_lines"), len(lines)))
            owners = set()
            for ln in lines:
                out += ["%s: %s" % (key, p) for p in line_problems(ln)]
                m = OWNER_PREFIX.match((ln.get("text") or "").strip())
                if m and m.group(1) in ("SR", "PK"):
                    owners.add(m.group(1))
            if len(owners) > 1:
                out.append("%s: SR and PK lines are mixed in one checklist (one owner per checklist, Decision 37; CL lines excepted)" % key)
    if len(set(keys)) != len(keys):
        out.append("objects: an object is listed twice")
    if kind == "test":
        if (plan.get("client") or "").strip().lower() != (test_client or "").strip().lower():
            out.append("client: a test runs on %s only (Paul's approval first); the plan names %r" % (test_client, plan.get("client")))
        path = plan.get("tick_path") or []
        if not path:
            out.append("tick_path: a test lists the ticks (module, line, opens)")
        for n, tk in enumerate(path, 1):
            if not (tk.get("module") and tk.get("line") and tk.get("opens")):
                out.append("tick_path %d: give module, line and opens" % n)
    elif plan.get("tick_path"):
        out.append("tick_path: only a test has a tick path")
    return out


def planned_keys(plan, kind):
    ks = [object_key(o) for o in plan.get("objects") or []]
    if kind == "test":
        ks += ["tick:%d" % n for n in range(1, len(plan.get("tick_path") or []) + 1)]
    return ks


def expected_lines(plan, key):
    for o in plan.get("objects") or []:
        if object_key(o) == key:
            return o.get("expect_lines")
    return None


def title_of(plan, key):
    for o in plan.get("objects") or []:
        if object_key(o) == key:
            return "%s #%s %s" % (o.get("type"), o.get("id"), o.get("title") or "")
    if key.startswith("tick:"):
        n = int(key.split(":")[1])
        tk = (plan.get("tick_path") or [{}])[n - 1]
        return "tick %d: %s -> opens %s" % (n, tk.get("module"), tk.get("opens"))
    return key
