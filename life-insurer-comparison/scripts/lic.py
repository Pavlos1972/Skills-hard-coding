#!/usr/bin/env python3
"""The domain model of the life insurer comparison: the scope (which benefit categories the client asked for, with the lines that prove it), the answers (every figure and every
statement checked against the right document's text), the premium escalation worked out from the printed figures, the flags for Paul.

Everything here is a pure function of the scope (scope.json), the answers (answers.json), the declared insurers (state.json) and the registered documents, so the checker can
recompute it and refuse a file edited by hand. The rules are Paul's (the old skill, kept) and his answers of 04/11/2026. Nothing here sends anything.

How a figure is proved: the chat enters the figure TOGETHER WITH a verbatim line of the document ("evidence"). The program proves that line is in the document's own text and that the
figure is in that line. It cannot prove the line was the right one to pick, and it cannot read a page that is an image (those are marked, shown to Paul and listed as attested).
"""
import calendar
import html
import json
import os
import re
from decimal import ROUND_HALF_UP, Decimal

import docread
import wrlib as w

ASSETS = os.path.join(w.SKILL_DIR, "assets")
TEMPLATE = os.path.join(ASSETS, "Life_Comparison_TEMPLATE.html")
SETTINGS = os.path.join(ASSETS, "settings.json")
WORDING = os.path.join(ASSETS, "wording.json")
TERMS = os.path.join(ASSETS, "scope_terms.json")

CC_NAME = "Sitamah Nathoo"
CC_EMAIL = "admin@liferisk.co.za"
SITAMAH_CHAT = "19:bd2a130a-35d9-459e-9025-55f356810236_e6901cee-de73-46d9-88a5-5e4a1c296418@unq.gbl.spaces"
CHAT_LABEL = "(1:1 Chat) Paul Kafentzis, Sitamah Nathoo"

ROLES = ("quote", "schedule", "intake_notes", "fact_find_summary", "overview", "broker_doc", "guide")
SIDE_ROLES = ("quote", "schedule")
INTAKE_ROLES = ("intake_notes", "fact_find_summary", "overview")
LABELLED = ("quote", "schedule", "intake_notes", "broker_doc", "guide")
OPTIONAL_ROLES = ("intake_notes", "fact_find_summary", "overview")
CATEGORIES = ("life", "severe_illness", "disability", "income_protection", "debt_cover", "childcare")
COVER_CATEGORIES = CATEGORIES + ("terminal_illness",)
SECTIONS = ("premium_snapshot", "cover_comparison", "escalation_table", "loyalty", "definitions", "verdict", "sources")
DEFAULT_SECTIONS = ("premium_snapshot", "cover_comparison", "escalation_table", "verdict", "sources")
ROLE_NAMES = ("proposal", "existing", "other")
BASES = ("client_document", "insurer_guide", "inference")
PALETTE = [("#B8860B", "#FBF1DE"), ("#2C3E70", "#E9ECF5"), ("#1B7A72", "#E4F3F1"), ("#6B4C9A", "#EFE7F5"), ("#1565C0", "#E3EFFB"), ("#5D6D7E", "#E9ECEE")]
HOUSE_GOLD = "#B08D57"
CHARCOAL = "#1A1A1A"
PLACEHOLDER = re.compile(r"\[[A-Z][A-Z0-9 _%().,/&#-]*\]")
LEFTOVER = re.compile(r"\b(TBC|TODO|XXX|lorem ipsum)\b", re.I)
AGE_CUE = re.compile(r"age[- ]?(?:rated|related|factor)|age rated premium pattern|rated for age", re.I)
FIXED_CUE = re.compile(r"yearly premium increase|compulsory|voluntary|fixed|level premium|contractual|guaranteed", re.I)
EXCLUDE_CUE = re.compile(r"\b(remov\w*|exclud\w*|not include\w*|did not include|budget|declin\w*|no need|do(?:es)? not want|don'?t want|without|opt(?:ed)? out)\b", re.I)

SCOPE_KEYS = {"categories", "second_life", "basis", "basis_source", "voice", "sections"}
ANSWER_KEYS = {"client_full_name", "client_first_name", "client_surname", "client_email", "email_source", "email_note", "plan_folder", "sides", "features", "definitions", "banner", "opening",
               "verdict", "email", "flags"}
SIDE_KEYS = {"label", "insurer", "role", "product_name", "tier", "reference", "document_date", "start_date", "rar_only", "premium", "escalation", "benefit_escalation", "guarantee", "covers",
             "projection", "loyalty", "second_life"}


def _json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def settings():
    return _json(SETTINGS)


def wording():
    return _json(WORDING)


def terms():
    return _json(TERMS)


def limits():
    return settings()["limits"]


def D(x):
    return x if isinstance(x, Decimal) else Decimal(str(x))


# ------------------------------------------------------------------ keys and roles
def slug(s):
    return re.sub(r"[^a-z0-9]+", "_", str(s).lower()).strip("_")


def dkey(role, label=None):
    return "%s_%s" % (role, slug(label)) if role in LABELLED else role


def valid_role(role):
    return role in ROLES


def can_be_missing(role):
    return role in OPTIONAL_ROLES or role == "guide"


def served_keys_order(docs):
    out = []
    for role in ROLES:
        out += sorted(k for k, d in docs["docs"].items() if d.get("role") == role)
    return out


def docs_of(docs, role):
    return {d["label"]: k for k, d in docs["docs"].items() if d.get("role") == role}


def side_docs(docs):
    """{label: key} of the quotes and schedules (the sides of the comparison)."""
    out = {}
    for r in SIDE_ROLES:
        out.update(docs_of(docs, r))
    return out


def declared(state):
    return list((state or {}).get("insurers") or [])


def guide_label(insurer, title):
    return "%s - %s" % (insurer.strip(), title.strip())


def has(e):
    return e is not None and e.has_text


def words(text):
    return len(str(text).split())


def pct_str(d):
    return format(D(d).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), "f")


def money_shown(v):
    d = w.parse_money(v) if not isinstance(v, Decimal) else v
    if d is None:
        return str(v)
    return w.fmt_money(d).replace("R ", "R ", 1)


def pct_digits(v):
    return str(v).replace("%", "").strip().replace(" ", "").replace(",", ".")


def distinct_insurers(a):
    out = []
    for s in a["sides"]:
        if s["insurer"] not in out:
            out.append(s["insurer"])
    return out


def subject(a):
    return html.unescape(wording()["subject"].format(name=a["client_full_name"].strip(), insurers=" vs ".join(distinct_insurers(a))))


def sent_text(clock):
    return "%s, %s %s" % (calendar.day_name[clock.weekday()], clock.strftime("%d/%m/%Y"), clock.strftime("%H:%M"))


def file_name(a, d):
    first = a["client_first_name"].strip().replace(" ", "_")
    sur = a["client_surname"].strip().replace(" ", "_")
    return w.safe_filename("%s_%s_Life_Insurance_Comparison - %s" % (first, sur, d.strftime("%d.%m.%y"))) + ".html"


def greeting_for(clock, used_today):
    if used_today:
        return "Hi"
    return "Good morning" if clock.hour < 12 else ("Good afternoon" if clock.hour < 18 else "Good evening")


def lead_side(a):
    return next((s for s in a["sides"] if s.get("role") == "proposal"), None)


# ------------------------------------------------------------------ evidence
def pct_in(text, v):
    """The percentage v (own decimals) appears in the text."""
    t = pct_digits(v)
    if not re.fullmatch(r"\d+(?:\.\d+)?", t):
        return False
    return bool(re.search(r"(?<![\d.,])" + re.escape(t).replace(r"\.", "[.,]") + r"(?!\d)", text))


def check_claim(label, cl, default_src, ev, docs, out, values=(), roles=None, images=None):
    """A claim is {"source": document key (optional when the default applies), "evidence": a verbatim line of that document}. The line must be in the document's text and every
    value (("amount", "R 1 000.00") or ("pct", "10")) must be in the line. A page with no readable text is marked "image_read": true with its "page" and cannot be proved."""
    if not isinstance(cl, dict):
        out.append("%s: needs {source, evidence} (a verbatim line of the document)" % label)
        return False
    src = cl.get("source") or default_src
    d = docs["docs"].get(src) if src else None
    if d is None:
        out.append("%s: the source %r is not a registered document" % (label, src))
        return False
    if roles and d["role"] not in roles:
        out.append("%s: the source %s is a %s; it must be one of: %s" % (label, src, d["role"], ", ".join(roles)))
        return False
    evd = (cl.get("evidence") or "").strip()
    if len(evd) < 6:
        out.append("%s: evidence is needed (a verbatim line of %s)" % (label, src))
        return False
    ok = True
    if cl.get("image_read"):
        pg = cl.get("page")
        if not isinstance(pg, int) or pg not in (d.get("image_only") or []):
            out.append("%s: image_read is only for a page with no readable text (those pages of %s: %s)" % (label, src, d.get("image_only") or "none"))
            return False
        if images is not None:
            images.append("%s (%s, page %d)" % (label, src, pg))
    else:
        e = ev.get(src)
        if not has(e):
            out.append("%s: %s has no readable text; if the line is on an image page mark it image_read with the page" % (label, src))
            return False
        if w.norm(evd) not in e.norm:
            hint = " (page(s) %s of this document are images: mark image_read if it is there)" % ", ".join(map(str, d["image_only"])) if d.get("image_only") else ""
            out.append("%s: the evidence line is not in the text of %s%s" % (label, src, hint))
            return False
    for kind, v in values:
        if v in (None, ""):
            continue
        if kind == "amount":
            dv = w.parse_money(v)
            if dv is None or dv not in docread.numbers_in(evd):
                out.append("%s: %s is not in the evidence line" % (label, v))
                ok = False
        elif not pct_in(evd, v):
            out.append("%s: %s%% is not in the evidence line" % (label, pct_digits(v)))
            ok = False
    return ok


# ------------------------------------------------------------------ prose rules
def scope_hits(text, scope):
    """(category, term) for every word of an out-of-scope category found in the text."""
    t = terms()
    hits = []
    low = text.lower()
    for cat in CATEGORIES:
        if (scope["categories"].get(cat) or {}).get("status") == "out":
            for term in t.get(cat, []):
                if re.search(r"(?<![a-z])" + re.escape(term.lower()) + r"(?![a-z])", low):
                    hits.append((cat, term))
    return hits


def voice_problems(text, voice, client_name):
    wd = wording()
    out = []
    if voice == "first_person":
        out += ["institutional phrase %r" % x for x in wd["first_person_banned"] if x.lower() in text.lower()]
    else:
        m = re.search(wd["third_person_banned_regex"], text)
        if m:
            out.append("first-person word %r in a third-person document" % m.group(0))
    m = re.search(wd["client_slip_regex"], text, re.I)
    if m:
        out.append("the client is written about in the third person (%r): write 'you'" % m.group(0))
    return out


def version_problems(text):
    wd = wording()
    return ["quote-version history (%r): describe only the current version's own facts" % x for x in wd["version_hard"] if x.lower() in text.lower()]


def soft_version_words(text):
    wd = wording()
    return [x for x in wd["version_soft"] if re.search(r"\b" + re.escape(x) + r"\b", text, re.I)]


def prose_problems(label, text, scope, client_name, out, max_words=None, allow_empty=False):
    if not isinstance(text, str) or not text.strip():
        if not allow_empty:
            out.append("%s: text is needed" % label)
        return
    if max_words and words(text) > max_words:
        out.append("%s: %d words; the limit is %d (short means short)" % (label, words(text), max_words))
    if PLACEHOLDER.search(text) or LEFTOVER.search(text):
        out.append("%s: a placeholder or leftover is in the text" % label)
    for cat, term in scope_hits(text, scope):
        out.append("%s: %r belongs to a category that is out of scope (%s): remove it entirely" % (label, term, cat))
    out += ["%s: %s" % (label, x) for x in voice_problems(text, scope["voice"], client_name)]
    out += ["%s: %s" % (label, x) for x in version_problems(text)]
    if client_name and w.norm(client_name) in w.norm(text):
        out.append("%s: the client's full name is in the prose; write 'you'" % label)


# ------------------------------------------------------------------ the scope
def intake_lines(docs, ev):
    """[(doc key, line)] of the intake documents' text, line by line."""
    out = []
    for k in served_keys_order(docs):
        if docs["docs"][k]["role"] in INTAKE_ROLES and has(ev.get(k)):
            for ln in ev[k].text.splitlines():
                if len(ln.split()) >= 3:
                    out.append((k, ln.strip()))
    return out


def scope_suggestions(docs, ev):
    """For each category the intake lines that mention it, with a mark where the line has exclusion language (a hint for the chat, never a verdict)."""
    t = terms()
    res = {}
    lines = intake_lines(docs, ev)
    for cat in CATEGORIES:
        words_ = t.get(cat) or (["life cover", "life assured", "death benefit"] if cat == "life" else [])
        hits = []
        for k, ln in lines:
            if any(re.search(r"(?<![a-z])" + re.escape(x) + r"(?![a-z])", ln.lower()) for x in words_):
                hits.append((k, ln, bool(EXCLUDE_CUE.search(ln))))
        res[cat] = hits
    return res


def scope_problems(s, ev, docs):
    out = []
    if not isinstance(s, dict) or set(s) - SCOPE_KEYS or SCOPE_KEYS - set(s):
        return ["the scope file has these keys exactly: %s" % ", ".join(sorted(SCOPE_KEYS))]
    cats = s["categories"]
    if not isinstance(cats, dict) or set(cats) != set(CATEGORIES):
        return ["categories must have exactly: %s" % ", ".join(CATEGORIES)]
    for cat in CATEGORIES:
        c = cats[cat]
        if not isinstance(c, dict) or c.get("status") not in ("in", "out"):
            out.append("category %s: status must be 'in' or 'out'" % cat)
            continue
        said = (c.get("paul_said") or "").strip()
        if said:
            if len(said) < 5:
                out.append("category %s: Paul's words are too short" % cat)
        else:
            check_claim("category %s" % cat, c, None, ev, docs, out, roles=INTAKE_ROLES)
    if (cats.get("life") or {}).get("status") != "in":
        out.append("life cover must be in scope (this skill compares life/risk policies)")
    sl = s["second_life"]
    if not isinstance(sl, dict) or not isinstance(sl.get("present"), bool):
        out.append("second_life must be {\"present\": false} or {\"present\": true, \"name\", \"source\", \"evidence\"}")
    elif sl["present"]:
        if not (sl.get("name") or "").strip():
            out.append("second_life: the second life's first name is needed")
        elif not (sl.get("paul_said") or "").strip():
            check_claim("second_life", sl, None, ev, docs, out)
    if s["basis"] not in ("like-for-like", "against-proposal"):
        out.append("basis must be 'like-for-like' or 'against-proposal'")
    if len((s["basis_source"] or "").strip()) < 5:
        out.append("basis_source: say where the basis comes from (the board's answer, Paul's words)")
    if s["voice"] not in ("first_person", "third_person"):
        out.append("voice must be 'first_person' (Paul's default) or 'third_person'")
    secs = s["sections"]
    if not isinstance(secs, list) or not secs or set(secs) - set(SECTIONS) or len(set(secs)) != len(secs):
        out.append("sections must be a non-empty list without duplicates, from: %s" % ", ".join(SECTIONS))
    return out


def canonical_sections(scope):
    return [x for x in SECTIONS if x in scope["sections"]]


def scope_flags(scope, docs, ev):
    """Exclusion language in the intake notes about a category that is IN scope (a hint for Paul)."""
    out = []
    sug = scope_suggestions(docs, ev)
    for cat in CATEGORIES:
        if scope["categories"][cat]["status"] == "in" and cat != "life":
            for k, ln, ex in sug[cat]:
                if ex:
                    out.append("the intake notes contain exclusion language about %s (%s: \"%s\") but it is in scope: confirm" % (cat, k, ln[:80]))
                    break
    return out


# ------------------------------------------------------------------ the answers
def _prose(label, v, scope, a, lim, out, key=None, allow_empty=False):
    prose_problems(label, v, scope, a.get("client_full_name"), out, lim.get(key) if key else None, allow_empty)


def _statement(label, st, a, scope, ev, docs, out, images):
    """A statement with a basis: client_document (a line of a policy document), insurer_guide (a line of a saved guide) or inference (shown as 'to be confirmed')."""
    basis = st.get("basis")
    if basis not in BASES:
        out.append("%s: basis must be one of %s" % (label, ", ".join(BASES)))
        return
    if basis == "client_document":
        check_claim(label, st, None, ev, docs, out, roles=SIDE_ROLES + ("broker_doc",), images=images)
    elif basis == "insurer_guide":
        check_claim(label, st, None, ev, docs, out, roles=("guide",))
    elif st.get("source") or st.get("evidence"):
        out.append("%s: an inference has no source (it is shown as 'to be confirmed')" % label)


def answers_problems(a, scope, ev, docs, today, run_client=None, state=None):
    out = []
    lim = limits()
    if not isinstance(a, dict):
        return ["the answers file must be a JSON object"]
    if set(a) - ANSWER_KEYS or ANSWER_KEYS - set(a):
        return ["the answers file has these keys exactly: %s (unknown: %s; missing: %s)" % (", ".join(sorted(ANSWER_KEYS)), ", ".join(sorted(set(a) - ANSWER_KEYS)) or "none", ", ".join(sorted(ANSWER_KEYS - set(a))) or "none")]
    full = (a["client_full_name"] or "").strip()
    first, sur = (a["client_first_name"] or "").strip(), (a["client_surname"] or "").strip()
    if not full or not first or not sur or w.norm(full) != w.norm("%s %s" % (first, sur)):
        out.append("client_full_name must be the first name and the surname")
    if run_client and w.norm(full) != w.norm(run_client):
        out.append("client_full_name %r is not the client of this run (%r)" % (full, run_client))
    sdocs = side_docs(docs)
    sides = a["sides"]
    if not isinstance(sides, list) or not lim["sides_min"] <= len(sides) <= lim["sides_max"]:
        return out + ["sides: from %d to %d, one per quote or schedule" % (lim["sides_min"], lim["sides_max"])]
    labels = [s.get("label") for s in sides if isinstance(s, dict)]
    if sorted(labels, key=str) != sorted(sdocs, key=str) or len(set(labels)) != len(labels):
        return out + ["the sides must be exactly the registered quotes and schedules, once each: %s" % "; ".join(sorted(sdocs))]
    dec = {d["label"]: d["insurer"] for d in declared(state)}
    # surname in every readable policy document
    for lab, k in sdocs.items():
        if has(ev.get(k)) and w.norm(sur) not in ev[k].norm:
            out.append("the client's surname %r is not in the text of %s" % (sur, k))
    # email
    es = a["email_source"]
    em = (a["client_email"] or "").strip().lower()
    if not re.fullmatch(r"[\w.+-]+@[\w-]+\.[\w.-]+", em):
        out.append("client_email is not an email address")
    elif es == "fact_find_summary":
        e = ev.get("fact_find_summary")
        if not has(e):
            out.append("email_source fact_find_summary: the Fact Find Summary is not registered or has no text")
        elif em not in e.text.lower():
            out.append("client_email %s is not in the Fact Find Summary's text" % em)
    elif es == "paul":
        if len((a["email_note"] or "").strip()) < 5:
            out.append("email_source paul: put Paul's words in email_note")
    else:
        out.append("email_source must be 'fact_find_summary' or 'paul'")
    if not (a["plan_folder"] or "").strip():
        out.append("plan_folder: the client's folder name is needed")
    secs = scope["sections"]
    images = []
    leads = [s for s in sides if isinstance(s, dict) and s.get("role") == "proposal"]
    if len(leads) > 1:
        out.append("only one side can be the proposal")
    cats_in = [c for c in CATEGORIES if scope["categories"][c]["status"] == "in"] + ["terminal_illness"]
    for i, s in enumerate(sides):
        if not isinstance(s, dict) or set(s) - SIDE_KEYS:
            out.append("sides[%d]: unknown keys %s" % (i, sorted(set(s) - SIDE_KEYS) if isinstance(s, dict) else ""))
            continue
        lab = s.get("label")
        k = sdocs[lab]
        role_doc = docs["docs"][k]["role"]
        L = "%s" % lab
        e = ev.get(k)
        if s.get("insurer") != dec.get(lab):
            out.append("%s: insurer %r is not the declared one (%r)" % (L, s.get("insurer"), dec.get(lab)))
        if s.get("role") not in ROLE_NAMES:
            out.append("%s: role must be one of %s" % (L, ", ".join(ROLE_NAMES)))
        if has(e):
            for f_, chk in (("insurer", e.name), ("product_name", e.name)):
                m = chk("%s %s" % (L, f_), s.get(f_))
                if m:
                    out.append(m)
            if s.get("tier"):
                m = e.name("%s tier" % L, s["tier"])
                out.append(m) if m else None
            if s.get("reference"):
                m = e.code("%s reference" % L, s["reference"])
                out.append(m) if m else None
            for f_ in ("document_date", "start_date"):
                if s.get(f_):
                    m = e.date("%s %s" % (L, f_), s[f_])
                    out.append(m) if m else None
        elif not (s.get("premium") or {}).get("image_read"):
            out.append("%s: the document has no readable text; every figure must be marked image_read with its page" % L)
        if not s.get("product_name"):
            out.append("%s: product_name is needed" % L)
        if s.get("rar_only") not in (None, True, False):
            out.append("%s: rar_only is true or false" % L)
        # premium
        pr = s.get("premium") or {}
        if not w.parse_money(pr.get("monthly")):
            out.append("%s: premium.monthly (the document's own total monthly premium) is needed" % L)
        else:
            check_claim("%s premium" % L, pr, k, ev, docs, out, values=(("amount", pr["monthly"]),), roles=SIDE_ROLES, images=images)
        # premium pattern
        es_ = s.get("escalation") or {}
        if es_.get("type") not in ("fixed", "age_rated"):
            out.append("%s: escalation.type must be 'fixed' or 'age_rated' (from the document's own words)" % L)
        else:
            check_claim("%s escalation wording" % L, es_, k, ev, docs, out, values=(("pct", es_.get("rate")),) if es_.get("rate") else (), roles=SIDE_ROLES, images=images)
        be = s.get("benefit_escalation")
        if be:
            check_claim("%s benefit escalation" % L, be, k, ev, docs, out, values=(("pct", be.get("rate")),), roles=SIDE_ROLES, images=images)
        g = s.get("guarantee")
        if not isinstance(g, dict) or not (g.get("not_stated") is True or (g.get("text") or "").strip()):
            out.append("%s: guarantee is {\"text\", \"evidence\"} or {\"not_stated\": true}" % L)
        elif not g.get("not_stated"):
            check_claim("%s guarantee period" % L, g, k, ev, docs, out, roles=SIDE_ROLES, images=images)
        # covers
        covers = s.get("covers")
        if not isinstance(covers, list) or not covers:
            out.append("%s: covers are needed (every benefit a separate row)" % L)
            covers = []
        seen = set()
        for j, c in enumerate(covers):
            CL = "%s cover %d" % (L, j + 1)
            if not isinstance(c, dict):
                out.append("%s: must be an object" % CL)
                continue
            if c.get("category") not in COVER_CATEGORIES:
                out.append("%s: category must be one of %s" % (CL, ", ".join(COVER_CATEGORIES)))
            elif c["category"] not in cats_in:
                out.append("%s: the category %s is out of scope: it must not appear at all (Step 0b)" % (CL, c["category"]))
            if not (c.get("label") or "").strip():
                out.append("%s: label is needed" % CL)
                continue
            for cat, term in scope_hits(c["label"], scope):
                out.append("%s: the label %r is an out-of-scope word (%s)" % (CL, c["label"], cat))
            life = c.get("life", "main")
            if life not in ("main", "second") or (life == "second" and not scope["second_life"]["present"]):
                out.append("%s: life is 'main' or 'second' (second only when the scope has a second life)" % CL)
            key = (c.get("category"), life, w.norm(c["label"]))
            if key in seen:
                out.append("%s: listed twice" % CL)
            seen.add(key)
            if not w.parse_money(c.get("amount")):
                out.append("%s: amount is needed" % CL)
            else:
                check_claim(CL, c, k, ev, docs, out, values=(("amount", c["amount"]), ("amount", c.get("monthly"))), roles=SIDE_ROLES, images=images)
        if not any(c.get("category") == "life" for c in covers if isinstance(c, dict)):
            out.append("%s: a life cover row is needed" % L)
        # projection
        pj = s.get("projection") or []
        if pj:
            if not isinstance(pj, list):
                out.append("%s: projection is a list" % L)
                pj = []
            for j, row in enumerate(pj, 1):
                if not isinstance(row, dict) or row.get("n") != j or not w.parse_money(row.get("premium")):
                    out.append("%s projection row %d: {n: %d (in order), premium, label, age, printed_pct}" % (L, j, j))
                    break
                if has(e):
                    m = e.number("%s projection year %d" % (L, j), row["premium"])
                    if m:
                        out.append(m)
                        break
                    if row.get("printed_pct"):
                        m = e.exact_percent("%s projection year %d printed %%" % (L, j), row["printed_pct"])
                        if m:
                            out.append(m)
                            break
                if row.get("age") is not None and not isinstance(row["age"], int):
                    out.append("%s projection year %d: age is a whole number" % (L, j))
                    break
        elif "escalation_table" in secs:
            pass
        # loyalty
        ly = s.get("loyalty")
        if ly:
            if "loyalty" not in secs:
                out.append("%s: a loyalty benefit is entered but the loyalty section is not in the scope sections" % L)
            v = str(ly.get("amount_or_pct") or "")
            kind = "amount" if v.strip().upper().startswith("R") else ("pct" if v.strip().endswith("%") else None)
            if kind is None or not (ly.get("name") or "").strip() or not (ly.get("when") or "").strip():
                out.append("%s loyalty: {name, amount_or_pct (a rand figure or a percentage), when, evidence}" % L)
            else:
                if words(ly["when"]) > lim["loyalty_when_words"]:
                    out.append("%s loyalty: 'when' is a phrase of at most %d words" % (L, lim["loyalty_when_words"]))
                check_claim("%s loyalty" % L, ly, k, ev, docs, out, values=((kind, v.replace("%", "")),), roles=SIDE_ROLES, images=images)
        # second life
        sl = s.get("second_life")
        if scope["second_life"]["present"]:
            if not isinstance(sl, dict) or sl.get("status") not in ("independent", "rider", "none"):
                out.append("%s: second_life {status: independent|rider|none} is needed (the scope has a second life)" % L)
            elif sl["status"] != "none":
                check_claim("%s second life" % L, sl, k, ev, docs, out, roles=SIDE_ROLES, images=images)
        elif sl:
            out.append("%s: the scope has no second life" % L)
    if "loyalty" in secs and not any(isinstance(s, dict) and s.get("loyalty") for s in sides):
        out.append("the loyalty section is ticked but no side has a loyalty benefit")
    if "escalation_table" in secs and not any(isinstance(s, dict) and s.get("projection") for s in sides):
        out.append("the escalation section is ticked but no side has a projection table")
    # features
    feats = a["features"]
    if not isinstance(feats, list):
        out.append("features is a list (it may be empty)")
        feats = []
    by_label = {s.get("label"): s for s in sides if isinstance(s, dict)}
    for j, f in enumerate(feats, 1):
        FL = "feature %d" % j
        if not isinstance(f, dict) or by_label.get(f.get("side")) is None:
            out.append("%s: side must be one of the labels" % FL)
            continue
        if f.get("category") not in cats_in:
            out.append("%s: category %r is out of scope or unknown" % (FL, f.get("category")))
        _prose(FL + " text", f.get("text"), scope, a, lim, out, "feature_words")
        _statement(FL, f, a, scope, ev, docs, out, images)
        if f.get("badge") not in (None, "wins", "tradeoff"):
            out.append("%s: badge is null, 'wins' or 'tradeoff'" % FL)
        if f.get("badge") == "wins" and f.get("basis") == "inference":
            out.append("%s: a 'wins' badge cannot rest on an inference" % FL)
        if f.get("not_on_proposal"):
            if f.get("basis") != "insurer_guide" or not (f.get("conditions") or "").strip():
                out.append("%s: a feature that is not on the proposal comes from the insurer's guide and says what the client must do (conditions)" % FL)
        if f.get("exclusive"):
            others = [x for x in distinct_insurers(a) if x != by_label[f["side"]]["insurer"]]
            chk = f.get("exclusive_checks") or []
            covered = set()
            for c in chk:
                if not isinstance(c, dict):
                    continue
                CLb = "%s exclusive check (%s)" % (FL, c.get("insurer"))
                if c.get("insurer") not in others:
                    out.append("%s: not another insurer in this comparison" % CLb)
                    continue
                src = docs["docs"].get(c.get("source"))
                own_side = src is not None and src["role"] in SIDE_ROLES and any(x["insurer"] == c["insurer"] and sdocs.get(x["label"]) == c["source"] for x in sides if isinstance(x, dict))
                own_guide = src is not None and src["role"] == "guide" and w.norm(src["label"]).startswith(w.norm(c["insurer"]))
                if not (own_side or own_guide):
                    out.append("%s: the source must be that insurer's own document or guide" % CLb)
                    continue
                if check_claim(CLb, c, None, ev, docs, out):
                    covered.add(c["insurer"])
            if set(others) - covered:
                out.append("%s: 'exclusive' needs a checked source for every other insurer; missing: %s" % (FL, ", ".join(sorted(set(others) - covered))))
    # definitions
    defs = a["definitions"]
    if "definitions" in secs:
        if not isinstance(defs, list) or not defs:
            out.append("the definitions section is ticked: definitions needs rows")
            defs = []
    elif defs:
        out.append("definitions has rows but the section is not ticked")
        defs = []
    for j, d_ in enumerate(defs or [], 1):
        DL = "definition %d" % j
        if not isinstance(d_, dict) or by_label.get(d_.get("side")) is None:
            out.append("%s: side must be one of the labels" % DL)
            continue
        if d_.get("category") not in cats_in:
            out.append("%s: category %r is out of scope or unknown" % (DL, d_.get("category")))
        if not (d_.get("set") or "").strip():
            out.append("%s: the definition set's name is needed" % DL)
        _prose(DL + " note", d_.get("note"), scope, a, lim, out, "definition_note_words", allow_empty=True)
        _statement(DL, d_, a, scope, ev, docs, out, images)
    # prose
    _prose("banner", a["banner"], scope, a, lim, out, "banner_words")
    _prose("opening", a["opening"], scope, a, lim, out, "opening_words")
    if "verdict" in secs:
        vd = a["verdict"]
        if not isinstance(vd, list) or not lim["verdict_min"] <= len(vd) <= lim["verdict_max"]:
            out.append("verdict: from %d to %d points, each {headline, detail}" % (lim["verdict_min"], lim["verdict_max"]))
        else:
            for j, v in enumerate(vd, 1):
                if not isinstance(v, dict):
                    out.append("verdict %d: {headline, detail}" % j)
                    continue
                _prose("verdict %d headline" % j, v.get("headline"), scope, a, lim, out, "verdict_headline_words")
                _prose("verdict %d detail" % j, v.get("detail"), scope, a, lim, out, "verdict_detail_words")
    elif a["verdict"]:
        out.append("verdict has points but the section is not ticked")
    em_ = a["email"]
    if not isinstance(em_, dict) or set(em_) - {"opening", "concern", "bullets"} or not {"opening", "bullets"} <= set(em_):
        out.append("email: {opening, concern (optional), bullets}")
    else:
        _prose("email opening", em_["opening"], scope, a, lim, out, "email_opening_words")
        _prose("email concern", em_.get("concern"), scope, a, lim, out, "email_opening_words", allow_empty=True)
        bl = em_["bullets"]
        if not isinstance(bl, list) or not lim["email_bullets_min"] <= len(bl) <= lim["email_bullets_max"]:
            out.append("email bullets: from %d to %d" % (lim["email_bullets_min"], lim["email_bullets_max"]))
        else:
            for j, b_ in enumerate(bl, 1):
                _prose("email bullet %d" % j, b_, scope, a, lim, out, "email_bullet_words")
    fl = a["flags"]
    if not isinstance(fl, list) or any(not isinstance(x, str) or not x.strip() for x in fl):
        out.append("flags is a list of short texts for Paul (it may be empty)")
    a_ = a  # noqa
    return out


# ------------------------------------------------------------------ the premium escalation, worked out from the printed figures
def proj_rows(s):
    """[{n, label, age, premium, printed, calc, pct, kind}]: pct is the printed percentage if the insurer prints one, else our own year-on-year calculation."""
    rows, prev = [], None
    for r in s.get("projection") or []:
        prem = w.parse_money(r["premium"])
        printed = w.parse_money(r["printed_pct"]) if r.get("printed_pct") else None
        calc = ((prem - prev) / prev * 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) if prev else None
        kind = "printed" if printed is not None else ("calculated" if calc is not None else None)
        rows.append({"n": r["n"], "label": r.get("label"), "age": r.get("age"), "premium": prem, "printed": printed, "calc": calc,
                     "pct": printed if printed is not None else calc, "kind": kind})
        prev = prem
    return rows


def esc_summary(s):
    rows = proj_rows(s)
    pcts = [r["pct"] for r in rows if r["pct"] is not None and r["n"] >= 2]
    outliers = []
    for i, r in enumerate(rows):
        if r["n"] < 2 or r["pct"] is None:
            continue
        nb = [x["pct"] for x in (rows[i - 1] if i >= 2 else None, rows[i + 1] if i + 1 < len(rows) else None) if x and x["pct"] is not None and x["n"] >= 2]
        avg = sum(nb) / len(nb) if nb else None
        if r["pct"] < 0 or (avg is not None and avg > 0 and r["pct"] >= Decimal("1.8") * avg and r["pct"] - avg >= 1):
            outliers.append((r["n"], r["pct"]))
    mism = [(r["n"], r["printed"], r["calc"]) for r in rows if r["printed"] is not None and r["calc"] is not None and abs(r["printed"] - r["calc"]) > Decimal("0.06")]
    cur = w.parse_money(s["premium"]["monthly"])
    anchor = next((r["n"] for r in rows if r["premium"] == cur), None) if rows else None
    kinds = {r["kind"] for r in rows if r["n"] >= 2 and r["kind"]}
    mode = "printed" if kinds == {"printed"} else ("calculated" if kinds == {"calculated"} else "mixed") if kinds else None
    return {"avg": (sum(pcts) / len(pcts)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) if pcts else None, "outliers": outliers, "mismatch": mism, "anchor": anchor, "mode": mode,
            "years": len(rows)}


def type_cue_flag(s):
    ev_ = (s["escalation"].get("evidence") or "")
    t = s["escalation"]["type"]
    if t == "fixed" and AGE_CUE.search(ev_):
        return "%s: the wording says age-rated (%s) but the pattern was entered as FIXED: check the reading" % (s["label"], AGE_CUE.search(ev_).group(0))
    if t == "age_rated" and not AGE_CUE.search(ev_) and FIXED_CUE.search(ev_):
        return "%s: the wording looks fixed (%s) but the pattern was entered as AGE-RATED: check the reading" % (s["label"], FIXED_CUE.search(ev_).group(0))
    return None


def check_summary(a, scope, today):
    """What the check step proves and shows (a pure function of the answers and the scope): bound to the step by its hash."""
    per = {}
    for s in a["sides"]:
        sm = esc_summary(s)
        per[s["label"]] = {"avg": str(sm["avg"]) if sm["avg"] is not None else None, "outliers": [[n, str(p)] for n, p in sm["outliers"]],
                           "mismatch": [[n, str(p), str(c)] for n, p, c in sm["mismatch"]], "anchor": sm["anchor"], "mode": sm["mode"], "years": sm["years"]}
    avgs = [(lab, Decimal(v["avg"])) for lab, v in per.items() if v["avg"] is not None]
    gap = None
    if len(avgs) >= 2:
        hi, lo = max(avgs, key=lambda x: x[1]), min(avgs, key=lambda x: x[1])
        if lo[1] > 0 and hi[1] >= 2 * lo[1] and hi[1] - lo[1] >= 3:
            gap = "%s averages %s%% a year but %s only %s%%: confirm both are read right (mechanism: an age-rated increase stacks with a separately chosen cover increase)" % (hi[0], pct_str(hi[1]), lo[0], pct_str(lo[1]))
    return {"per_side": per, "gap": gap, "type_flags": [f for f in (type_cue_flag(s) for s in a["sides"]) if f],
            "basis_counts": {b: sum(1 for f in a["features"] + (a["definitions"] or []) if f.get("basis") == b) for b in BASES}}


def program_flags(a, scope, docs, ev, today):
    cs = check_summary(a, scope, today)
    out = list(cs["type_flags"])
    for lab, v in cs["per_side"].items():
        for n, p in v["outliers"]:
            out.append("%s: the increase in year %d is %s%%, an outlier against the surrounding years: it is flagged in the letter's footnote" % (lab, n, p))
        for n, pr, ca in v["mismatch"]:
            out.append("%s: year %d printed %s%% but the printed rand figures work out to %s%%: the printed one is shown" % (lab, n, pr, ca))
        s = next(x for x in a["sides"] if x["label"] == lab)
        if v["years"] and v["anchor"] != 1:
            out.append("%s: the current premium %s %s in the projection table: check which year it is" % (lab, s["premium"]["monthly"], "is year %d" % v["anchor"] if v["anchor"] else "is NOT"))
        if not v["years"] and "escalation_table" in scope["sections"]:
            out.append("%s: no projection table: its column shows 'not provided'" % lab)
        elif v["years"] and v["years"] < limits()["min_projection_years"] and "escalation_table" in scope["sections"]:
            out.append("%s: the projection table has %d year(s): the rest show 'not provided'" % (lab, v["years"]))
        if s["guarantee"].get("not_stated"):
            out.append("%s: the premium guarantee period is not stated on the document: the letter says to confirm it with the insurer" % lab)
        if s.get("rar_only"):
            out.append("%s is RAR-sourced, not schedule-confirmed: say so to the client (the email does) and consider requesting the schedule" % lab)
    if cs["gap"]:
        out.append(cs["gap"])
    inf = [f for f in a["features"] if f.get("basis") == "inference"]
    if inf:
        out.append("%d statement(s) are inferences, shown to the client as 'to be confirmed': %s" % (len(inf), "; ".join(f["text"][:50] for f in inf)))
    out += scope_flags(scope, docs, ev)
    lyvals = [str(s["loyalty"]["amount_or_pct"]) for s in a["sides"] if s.get("loyalty")]
    lead_text = " ".join([a["banner"]] + [v["headline"] for v in (a["verdict"] or [])])
    if any(x and x in lead_text for x in lyvals):
        out.append("the banner or a verdict headline leads with a loyalty/payback figure: the old rule says never lead with a payout as the reason to switch")
    if not re.search(r"\d", a["banner"]) and w.norm(a["client_first_name"]) not in w.norm(a["banner"]):
        out.append("the banner may be generic: it has no figure and does not use the client's name")
    for x in soft_version_words(" ".join([a["banner"], a["opening"]] + [f["text"] for f in a["features"]] + [v["detail"] for v in (a["verdict"] or [])])):
        out.append("the word %r is in the prose: make sure it does not describe an earlier version of a quote" % x)
    return out


def paul_flags(a, scope, docs, ev, today):
    return program_flags(a, scope, docs, ev, today) + list(a.get("flags") or [])
