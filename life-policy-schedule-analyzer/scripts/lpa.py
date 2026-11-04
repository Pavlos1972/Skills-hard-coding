#!/usr/bin/env python3
"""The domain model of the life policy schedule analysis: the analysis file (every client figure proved by a verbatim line of the schedule, every product statement proved by a verbatim
line of a saved source), the 10-year premium table (never invented), the findings with their numbers, the client slides' data, the file names.

Everything here is a pure function of the analysis (analysis.json), the declared insurers (state.json) and the registered documents, so the checker can recompute it and refuse a
file edited by hand. The rules are Paul's (the old skill, kept) and his answers of 04/11/2026. Nothing here sends anything.

How a figure is proved: the chat enters the figure TOGETHER WITH a verbatim line of the document ("evidence"); the program proves the line is in the document's own text and the figure is
in the line. A product statement carries one or two saved sources (the insurer's own guide and an independent one), each with a verbatim line; one source is labelled SINGLE SOURCE. The
program cannot prove a saved source is the real page, cannot read a page that is an image (those are marked and attested) and cannot judge the critique itself.
"""
import calendar
import json
import os
import re
from decimal import ROUND_HALF_UP, Decimal

import docread
import wrlib as w

ASSETS = os.path.join(w.SKILL_DIR, "assets")
SETTINGS = os.path.join(ASSETS, "settings.json")
WORDING = os.path.join(ASSETS, "wording.json")
SLIDE_WORDS = os.path.join(ASSETS, "slide_words.json")

ROLES = ("schedule", "quote", "proposed", "payback_doc", "fact_find_summary", "intake_notes", "guide", "source")
POLICY_ROLES = ("schedule", "quote")
LABELLED = ("schedule", "quote", "proposed", "payback_doc", "intake_notes", "guide", "source")
OPTIONAL_ROLES = ("fact_find_summary", "intake_notes", "payback_doc", "guide", "source")
CLIENT_DOC_ROLES = POLICY_ROLES + ("proposed", "payback_doc", "fact_find_summary", "intake_notes")
BEN_CATS = ("life", "disability", "dread_disease", "income_protection", "other")
FOUR = BEN_CATS[:4]
BASES = ("document", "product", "inference", "absent")
DD_TOPICS = ("multiple_claims", "payout_structure", "duration", "exceed_100", "survival_period", "children", "trauma_equivalent", "severe_illness_scope", "accelerated_vs_standalone")
VIT_TOPICS = ("status_effect", "annual_checks", "medical_aid_claims", "upfront_discount_clawback")
PB_TOPICS = ("mechanism", "trigger", "guaranteed_or_estimate", "forfeiture", "standard_or_optional", "held_status")
TOPIC_NAMES = {"multiple_claims": "Multiple claims", "payout_structure": "Payout structure", "duration": "Duration", "exceed_100": "Can it pay more than 100%?", "survival_period": "Survival period",
               "children": "Children's cover", "trauma_equivalent": "Trauma IQ or equivalent", "severe_illness_scope": "Severe illness scope and triggers", "accelerated_vs_standalone": "Accelerated or standalone",
               "status_effect": "Vitality status and the yearly increase", "annual_checks": "Annual health checks", "medical_aid_claims": "Medical aid claims", "upfront_discount_clawback": "Upfront discount and clawbacks",
               "mechanism": "The mechanism", "trigger": "What triggers a payout", "guaranteed_or_estimate": "Guaranteed or an estimate", "forfeiture": "What reduces or forfeits it",
               "standard_or_optional": "Standard or optional", "held_status": "Does the policy held include it"}
CAT_NAMES = {"life": "Life", "disability": "Disability", "dread_disease": "Dread / Serious Illness", "income_protection": "Income Protection", "other": "Other"}
OUTCOMES = ("better_exists", "top_tier", "unsure")
REF_KINDS = ("cession", "second_life")

ANSWER_KEYS = {"client_full_name", "client_first_name", "client_surname", "plan_folder", "policies", "proposed_status", "proposed_said", "proposed", "left_out", "slides", "flags"}
POLICY_KEYS = {"label", "insurer", "found_in", "product_name", "tier", "policy_number", "life_assured", "owner", "payer", "start_date", "status", "life_cover_type", "benefits", "premium",
               "exclusions", "riders", "beneficiaries", "cession", "second_life", "dread_disease", "vitality", "payback", "benchmark", "findings", "verdict", "honest_opinion"}
PLACEHOLDER = re.compile(r"\[[A-Z][A-Z0-9 _%().,/&#-]*\]")
LEFTOVER = re.compile(r"\b(TBC|TODO|XXX|lorem ipsum)\b", re.I)


def _json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def settings():
    return _json(SETTINGS)


def wording():
    return _json(WORDING)


def slide_words():
    return _json(SLIDE_WORDS)


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
    return role in OPTIONAL_ROLES


def served_keys_order(docs):
    out = []
    for role in ROLES:
        out += sorted(k for k, d in docs["docs"].items() if d.get("role") == role)
    return out


def docs_of(docs, role):
    return {d["label"]: k for k, d in docs["docs"].items() if d.get("role") == role}


def policy_docs(docs):
    out = {}
    for r in POLICY_ROLES:
        out.update(docs_of(docs, r))
    return out


def declared(state):
    return list((state or {}).get("insurers") or [])


def insurer_names(state):
    return sorted({d["insurer"] for d in declared(state)})


def source_label(insurer, title):
    return "%s - %s" % (insurer.strip(), title.strip())


def has(e):
    return e is not None and e.has_text


def words(text):
    return len(str(text).split())


def pct_digits(v):
    return str(v).replace("%", "").strip().replace(" ", "").replace(",", ".")


def pct_str(d):
    return format(D(d).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), "f")


def money(v):
    d = w.parse_money(v) if not isinstance(v, Decimal) else v
    return w.fmt_money(d) if d is not None else str(v)


def pct_in(text, v):
    t = pct_digits(v)
    if not re.fullmatch(r"\d+(?:\.\d+)?", t):
        return False
    return bool(re.search(r"(?<![\d.,])" + re.escape(t).replace(r"\.", "[.,]") + r"(?!\d)", text))


def today_str(d):
    return d.strftime("%d/%m/%Y")


def short(d):
    return d.strftime("%d.%m.%y")


def file_part(s):
    return re.sub(r"\s+", "_", w.safe_filename(s).strip())


# ------------------------------------------------------------------ evidence
def check_claim(label, cl, default_src, ev, docs, out, values=(), roles=None, images=None):
    """A claim is {"source": document key (optional when the default applies), "evidence": a verbatim line of that document}. The line must be in the document's text and every value
    (("amount", "R 1 000.00") or ("pct", "10")) must be in the line. A page with no readable text is marked "image_read": true with its "page" and cannot be proved."""
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


def source_ok(src, insurer, docs, out, label):
    d = docs["docs"].get(src)
    if d is None or d["role"] not in ("guide", "source"):
        out.append("%s: %r is not a registered product source (guide or source)" % (label, src))
        return None
    if not w.norm(d["label"]).startswith(w.norm(insurer) + " "):
        out.append("%s: the source %s is not about %s (its label starts with the insurer's name)" % (label, src, insurer))
        return None
    return d["role"]


def sources_problems(label, srcs, insurer, ev, docs, out, need=True):
    """[{source, evidence}] from saved product sources. Returns the set of roles that proved a line ('guide', 'source')."""
    roles = set()
    if not isinstance(srcs, list) or (need and not srcs):
        out.append("%s: sources are needed: [{\"source\": <guide or source key>, \"evidence\": <a verbatim line>}]" % label)
        return roles
    for j, s in enumerate(srcs, 1):
        r = source_ok((s or {}).get("source") if isinstance(s, dict) else None, insurer, docs, out, "%s source %d" % (label, j))
        if r is None:
            continue
        if check_claim("%s source %d" % (label, j), s, None, ev, docs, out):
            roles.add(r)
    return roles


def kind_of(st, roles=None):
    b = st.get("basis")
    if b == "product":
        return "product_verified" if roles and {"guide", "source"} <= roles else "product_single"
    return b


def stmt_problems(label, st, pol, ev, docs, out, images, max_words=None, counts=None):
    """A statement: {"text", "basis": document|product|inference|absent, ...}. document: a verbatim line of the policy's (or another client) document; product: saved sources;
    inference: shown 'to be confirmed'; absent: the document is silent (shown 'not on the document')."""
    if not isinstance(st, dict) or not isinstance(st.get("text"), str) or not st["text"].strip():
        out.append("%s: needs {text, basis ...}" % label)
        return None
    if max_words and words(st["text"]) > max_words:
        out.append("%s: %d words; the limit is %d (bullet points, never prose)" % (label, words(st["text"]), max_words))
    if PLACEHOLDER.search(st["text"]) or LEFTOVER.search(st["text"]):
        out.append("%s: a placeholder or leftover is in the text" % label)
    b = st.get("basis")
    if b not in BASES:
        out.append("%s: basis must be one of %s" % (label, ", ".join(BASES)))
        return None
    roles = None
    if b == "document":
        check_claim(label, st, pol["_key"], ev, docs, out, roles=CLIENT_DOC_ROLES, images=images)
    elif b == "product":
        roles = sources_problems(label, st.get("sources"), pol.get("insurer"), ev, docs, out)
    elif st.get("source") or st.get("evidence") or st.get("sources"):
        out.append("%s: a %s statement has no source" % (label, b))
    k = kind_of(st, roles)
    if counts is not None:
        counts[k] = counts.get(k, 0) + 1
    st["_kind"] = k
    return k


def prose_problems(label, text, out, max_words=None, allow_empty=False):
    if not isinstance(text, str) or not text.strip():
        if not allow_empty:
            out.append("%s: text is needed" % label)
        return
    if max_words and words(text) > max_words:
        out.append("%s: %d words; the limit is %d" % (label, words(text), max_words))
    if PLACEHOLDER.search(text) or LEFTOVER.search(text):
        out.append("%s: a placeholder or leftover is in the text" % label)


def banned_slide_words(text):
    low = text.lower()
    return [b for b in slide_words()["banned"] if re.search(r"(?<![a-z])" + re.escape(b) + r"(?![a-z])", low)]


def slide_text_problems(label, text, out, max_words=None):
    prose_problems(label, text, out, max_words)
    for b in banned_slide_words(text if isinstance(text, str) else ""):
        out.append("%s: %r must not appear on a client-facing slide" % (label, b))


# ------------------------------------------------------------------ the analysis
def analysis_problems(a, ev, docs, today, run_client=None, state=None):
    out = []
    lim = limits()
    if not isinstance(a, dict):
        return ["the analysis file must be a JSON object"]
    if set(a) - ANSWER_KEYS or ANSWER_KEYS - set(a):
        return ["the analysis file has these keys exactly: %s (unknown: %s; missing: %s)" % (", ".join(sorted(ANSWER_KEYS)), ", ".join(sorted(set(a) - ANSWER_KEYS)) or "none", ", ".join(sorted(ANSWER_KEYS - set(a))) or "none")]
    full, first, sur = (a["client_full_name"] or "").strip(), (a["client_first_name"] or "").strip(), (a["client_surname"] or "").strip()
    if not full or not first or not sur or w.norm(full) != w.norm("%s %s" % (first, sur)):
        out.append("client_full_name must be the first name and the surname")
    if run_client and w.norm(full) != w.norm(run_client):
        out.append("client_full_name %r is not the client of this run (%r)" % (full, run_client))
    if not (a["plan_folder"] or "").strip():
        out.append("plan_folder: the client's folder name is needed")
    pdocs = policy_docs(docs)
    pols = a["policies"]
    if not isinstance(pols, list) or not pols:
        return out + ["policies: one entry per registered schedule or quote"]
    labels = [p.get("label") for p in pols if isinstance(p, dict)]
    if sorted(labels, key=str) != sorted(pdocs, key=str) or len(set(labels)) != len(labels):
        return out + ["the policies must be exactly the registered schedules and quotes, once each: %s" % "; ".join(sorted(pdocs))]
    dec = {d["label"]: d["insurer"] for d in declared(state)}
    images, counts = [], {}
    ff = "fact_find_summary" in docs["docs"]
    for i, p in enumerate(pols):
        if not isinstance(p, dict) or set(p) - POLICY_KEYS:
            out.append("policies[%d]: unknown keys %s" % (i, sorted(set(p) - POLICY_KEYS) if isinstance(p, dict) else ""))
            continue
        try:
            policy_problems(p, i, pdocs[p["label"]], dec, ev, docs, today, out, images, counts, lim, ff)
        except (KeyError, TypeError, AttributeError, ValueError, IndexError) as exc:
            out.append("%s: the analysis is malformed here (%s: %s); check the layout in the rules page" % (p.get("label"), type(exc).__name__, exc))
    for p in pols:
        if isinstance(p, dict):
            p.pop("_key", None)
    # the proposed quote
    ps = a["proposed_status"]
    if ps not in ("present", "none_for_now"):
        out.append("proposed_status must be 'present' or 'none_for_now'")
    elif ps == "none_for_now":
        if len((a["proposed_said"] or "").strip()) < 5:
            out.append("proposed_status none_for_now: put Paul's own words in proposed_said")
        if a["proposed"] is not None or docs_of(docs, "proposed"):
            out.append("none_for_now: no proposed quote may be entered or registered")
    else:
        proposed_problems(a, ev, docs, today, dec, out, images, lim, pols)
    # the client's own choices (a category left out on purpose)
    lo = a["left_out"]
    if not isinstance(lo, list):
        out.append("left_out is a list (it may be empty)")
        lo = []
    for j, x in enumerate(lo, 1):
        if not isinstance(x, dict) or x.get("category") not in FOUR:
            out.append("left_out %d: category must be one of %s" % (j, ", ".join(FOUR)))
        else:
            check_claim("left_out %d" % j, x, None, ev, docs, out, roles=("fact_find_summary", "intake_notes"))
    slides_problems(a, ev, docs, out, lim, pols, ff)
    fl = a["flags"]
    if not isinstance(fl, list) or any(not isinstance(x, str) or not x.strip() for x in fl):
        out.append("flags is a list of short texts for Paul (it may be empty)")
    return out


def policy_problems(p, i, key, dec, ev, docs, today, out, images, counts, lim, ff):
    L = p.get("label")
    p["_key"] = key
    e = ev.get(key)
    if p.get("insurer") != dec.get(L):
        out.append("%s: insurer %r is not the declared one (%r)" % (L, p.get("insurer"), dec.get(L)))
    if has(e):
        for f_ in ("insurer", "product_name", "life_assured"):
            m = e.name("%s %s" % (L, f_), p.get(f_))
            out.append(m) if m else None
        for f_ in ("tier", "owner", "payer"):
            if p.get(f_):
                m = e.name("%s %s" % (L, f_), p[f_])
                out.append(m) if m else None
        if not p.get("policy_number") or e.code("%s policy number" % L, p["policy_number"]):
            out.append("%s: policy_number %r is not in the document's text" % (L, p.get("policy_number")))
        if p.get("start_date"):
            m = e.date("%s start_date" % L, p["start_date"])
            out.append(m) if m else None
    else:
        out.append("%s: the document has no readable text; every figure must be marked image_read with its page" % L)
    for f_ in ("found_in", "status", "product_name"):
        if not (p.get(f_) or "").strip():
            out.append("%s: %s is needed" % (L, f_))
    # life cover type (term, whole of life or accidental death): always explicit
    has_life = any(isinstance(b, dict) and b.get("category") == "life" for b in (p.get("benefits") or []))
    lct = p.get("life_cover_type")
    if not has_life:
        if lct:
            out.append("%s: life_cover_type is only for a policy with a life cover benefit" % L)
    elif not isinstance(lct, dict) or lct.get("type") not in ("term", "whole_of_life", "accidental_death"):
        out.append("%s: life_cover_type.type must be term, whole_of_life or accidental_death (always explicit, even if the schedule does not use these words)" % L)
    else:
        lct.setdefault("text", {"term": "Term cover (expires at a set age or date)", "whole_of_life": "Whole of life (runs for life)", "accidental_death": "Accidental death only (not natural causes)"}[lct["type"]])
        stmt_problems("%s life cover type" % L, lct, p, ev, docs, out, images, counts=counts)
    # benefits
    bens = p.get("benefits")
    if not isinstance(bens, list) or not bens:
        out.append("%s: benefits are needed (every benefit on the document, one at a time)" % L)
        bens = []
    seen = set()
    for j, b in enumerate(bens, 1):
        BL = "%s benefit %d" % (L, j)
        if not isinstance(b, dict) or b.get("category") not in BEN_CATS:
            out.append("%s: category must be one of %s" % (BL, ", ".join(BEN_CATS)))
            continue
        life = b.get("life", "main")
        if life not in ("main", "second"):
            out.append("%s: life is 'main' or 'second'" % BL)
        if not (b.get("label") or "").strip():
            out.append("%s: label is needed" % BL)
            continue
        k = (b["category"], life, w.norm(b["label"]))
        if k in seen:
            out.append("%s: listed twice" % BL)
        seen.add(k)
        if not w.parse_money(b.get("sum_assured")):
            out.append("%s: sum_assured is needed" % BL)
        else:
            vals = [("amount", b["sum_assured"])] + ([("amount", b["premium"])] if b.get("premium") and not b.get("premium_evidence") else [])
            check_claim(BL, b, key, ev, docs, out, values=vals, roles=POLICY_ROLES, images=images)
            if b.get("premium") and b.get("premium_evidence"):
                check_claim(BL + " premium", {"evidence": b["premium_evidence"], "source": b.get("source")}, key, ev, docs, out, values=(("amount", b["premium"]),), roles=POLICY_ROLES, images=images)
        if b.get("accelerated") not in ("accelerated", "standalone", "not_applicable"):
            out.append("%s: accelerated is accelerated, standalone or not_applicable" % BL)
        if b.get("unit", "lump_sum") not in ("lump_sum", "monthly"):
            out.append("%s: unit is lump_sum or monthly" % BL)
        for r_ in (b.get("details") or []):
            stmt_problems("%s detail" % BL, r_, p, ev, docs, out, images, lim["row_words"], counts)
        bl = b.get("bullets") or []
        lo_n = 0 if b.get("self_explanatory") else lim["bullets_min"]
        if not isinstance(bl, list) or not lo_n <= len(bl) <= lim["bullets_max"]:
            out.append("%s: from %d to %d plain-language bullets (or self_explanatory: true for a plain lump sum)" % (BL, lo_n, lim["bullets_max"]))
        else:
            for r_ in bl:
                stmt_problems("%s bullet" % BL, r_, p, ev, docs, out, images, lim["bullet_words"], counts)
    # premium
    pr = p.get("premium") or {}
    if not w.parse_money(pr.get("monthly")):
        out.append("%s: premium.monthly (the document's own total) is needed" % L)
    else:
        check_claim("%s premium" % L, pr, key, ev, docs, out, values=(("amount", pr["monthly"]),), roles=POLICY_ROLES, images=images)
    pat = pr.get("pattern") or {}
    if pat.get("type") not in ("fixed", "age_rated"):
        out.append("%s: premium.pattern.type must be 'fixed' or 'age_rated' (from the document's own words)" % L)
    else:
        check_claim("%s premium pattern" % L, pat, key, ev, docs, out, values=(("pct", pat.get("rate")),) if pat.get("rate") else (), roles=POLICY_ROLES, images=images)
    g = pr.get("guarantee")
    if not isinstance(g, dict) or not (g.get("not_stated") is True or (g.get("text") or "").strip()):
        out.append("%s: premium.guarantee is {text, evidence} or {not_stated: true}" % L)
    elif not g.get("not_stated"):
        check_claim("%s guarantee" % L, g, key, ev, docs, out, roles=POLICY_ROLES, images=images)
    for r_ in (pr.get("components") or []):
        stmt_problems("%s premium component" % L, r_, p, ev, docs, out, images, lim["row_words"], counts)
    if pr.get("loading"):
        stmt_problems("%s loading" % L, pr["loading"], p, ev, docs, out, images, lim["row_words"], counts)
    if pr.get("age_start"):
        check_claim("%s age" % L, pr["age_start"], key, ev, docs, out, values=(("amount", pr["age_start"].get("value")),), roles=CLIENT_DOC_ROLES, images=images)
    pj = pr.get("projection")
    if pj:
        for j, row in enumerate(pj, 1):
            if not isinstance(row, dict) or row.get("n") != j or not w.parse_money(row.get("premium")):
                out.append("%s projection row %d: {n: %d (in order), premium, age, printed_pct}" % (L, j, j))
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
    asm = pr.get("assumption")
    if asm:
        if not (isinstance(asm, dict) and w.parse_money(asm.get("rate")) and (asm.get("text") or "").strip() and len((asm.get("said") or "").strip()) >= 5):
            out.append("%s: assumption is {rate, text, said (Paul's own words)}" % L)
        if pj or pat.get("rate"):
            out.append("%s: an assumption is only for a premium with no printed table and no stated rate" % L)
    # the fixed sections
    for name in ("exclusions", "riders", "beneficiaries"):
        rows = p.get(name)
        if not isinstance(rows, list):
            out.append("%s: %s is a list (it may be empty)" % (L, name))
            continue
        for r_ in rows:
            stmt_problems("%s %s" % (L, name), r_, p, ev, docs, out, images, lim["row_words"], counts)
    ce = p.get("cession") or {}
    if ce.get("status") not in ("ceded", "not_ceded"):
        out.append("%s: cession.status is ceded or not_ceded (checked every time, even when the answer is none)" % L)
    else:
        if ce["status"] == "ceded" and not (ce.get("to") or "").strip():
            out.append("%s: a cession needs 'to' (to whom it is ceded)" % L)
        ce.setdefault("text", "Ceded to %s" % ce.get("to") if ce["status"] == "ceded" else "No cession noted on this schedule")
        if ce["status"] == "not_ceded":
            ce.setdefault("basis", "absent")
        stmt_problems("%s cession" % L, ce, p, ev, docs, out, images, lim["row_words"], counts)
    sl = p.get("second_life") or {}
    if sl.get("status") not in ("none", "independent", "rider"):
        out.append("%s: second_life.status is none, independent or rider (checked every time)" % L)
    else:
        sl.setdefault("text", "No second life on this policy." if sl["status"] == "none" else "")
        if sl["status"] == "none":
            sl.setdefault("basis", "absent")
        stmt_problems("%s second life" % L, sl, p, ev, docs, out, images, lim["row_words"], counts)
        if sl["status"] != "none" and not any(isinstance(b, dict) and b.get("life") == "second" for b in bens):
            out.append("%s: a second life needs its own benefits (life: second) entered like the main life's" % L)
        if sl["status"] == "none" and any(isinstance(b, dict) and b.get("life") == "second" for b in bens):
            out.append("%s: second_life.status is none but a second-life benefit is entered" % L)
        if sl.get("ff_note"):
            stmt_problems("%s second life Fact Find note" % L, sl["ff_note"], p, ev, docs, out, images, lim["row_words"], counts)
    # dread disease deep-dive: required whenever the benefit is held
    has_dd = any(isinstance(b, dict) and b.get("category") == "dread_disease" for b in bens)
    dd = p.get("dread_disease")
    if has_dd:
        if not isinstance(dd, dict) or set(dd) != set(DD_TOPICS):
            out.append("%s: dread_disease needs exactly these topics, each a statement: %s" % (L, ", ".join(DD_TOPICS)))
        else:
            for t in DD_TOPICS:
                stmt_problems("%s dread disease: %s" % (L, t), dd[t], p, ev, docs, out, images, lim["row_words"], counts)
    elif dd:
        out.append("%s: dread_disease is entered but no dread disease benefit is held" % L)
    for name, topics, what in (("vitality", VIT_TOPICS, "wellness mechanism"), ("payback", PB_TOPICS, "payback / loyalty benefit")):
        v = p.get(name)
        if not isinstance(v, dict) or not isinstance(v.get("applicable"), bool):
            out.append("%s: %s is {applicable: false, note} or {applicable: true, rows: {topic: statement}}" % (L, name))
        elif not v["applicable"]:
            if not (v.get("note") or "").strip():
                out.append("%s: %s not applicable: say so in note (stated, never silently omitted)" % (L, name))
        else:
            rows = v.get("rows")
            if not isinstance(rows, dict) or set(rows) != set(topics):
                out.append("%s: %s.rows needs exactly these topics: %s" % (L, name, ", ".join(topics)))
            else:
                for t in topics:
                    stmt_problems("%s %s: %s" % (L, name, t), rows[t], p, ev, docs, out, images, lim["row_words"], counts)
    # benchmark: every major benefit category held
    held = {b.get("category") for b in bens if isinstance(b, dict) and b.get("category") in FOUR}
    bm = p.get("benchmark")
    if not isinstance(bm, list):
        out.append("%s: benchmark is a list with one row for every major benefit held (%s)" % (L, ", ".join(sorted(held))))
        bm = []
    got = set()
    for j, r_ in enumerate(bm, 1):
        RL = "%s benchmark %d" % (L, j)
        if not isinstance(r_, dict) or r_.get("category") not in FOUR or r_.get("outcome") not in OUTCOMES:
            out.append("%s: {category (one of the four), have, available, outcome (%s), meaning, sources}" % (RL, ", ".join(OUTCOMES)))
            continue
        got.add(r_["category"])
        for f_ in ("have", "meaning"):
            prose_problems("%s %s" % (RL, f_), r_.get(f_), out, lim["row_words"])
        if r_["outcome"] == "better_exists":
            prose_problems("%s available" % RL, r_.get("available"), out, lim["row_words"])
        if r_["outcome"] in ("better_exists", "top_tier"):
            roles = sources_problems(RL, r_.get("sources"), p.get("insurer"), ev, docs, out)
            r_["_kind"] = "product_verified" if {"guide", "source"} <= roles else "product_single"
            counts[r_["_kind"]] = counts.get(r_["_kind"], 0) + 1
        elif r_.get("sources"):
            out.append("%s: an 'unsure' row has no sources (say so plainly; never guess)" % RL)
    if held - got:
        out.append("%s: a benchmark row is needed for every major benefit held; missing: %s" % (L, ", ".join(sorted(held - got))))
    if got - held:
        out.append("%s: a benchmark row for a benefit that is not held: %s" % (L, ", ".join(sorted(got - held))))
    # findings, the verdict, the opinion
    fds = p.get("findings")
    if not isinstance(fds, list):
        out.append("%s: findings is a list (it may be empty)" % L)
        fds = []
    refs = set()
    for j, f_ in enumerate(fds, 1):
        FL = "%s finding %d" % (L, j)
        if not isinstance(f_, dict) or f_.get("tier") not in ("action", "awareness"):
            out.append("%s: {tier: action|awareness (action when unsure), headline, detail, refs}" % FL)
            continue
        prose_problems(FL + " headline", f_.get("headline"), out, lim["finding_headline_words"])
        prose_problems(FL + " detail", f_.get("detail"), out, lim["finding_detail_words"])
        for r_ in f_.get("refs") or []:
            refs.add(r_)
    for r_ in bm:
        if isinstance(r_, dict) and r_.get("outcome") == "better_exists" and "benchmark:%s" % r_.get("category") not in refs:
            out.append("%s: the benchmark finding for %s needs a finding with refs [\"benchmark:%s\"] (every benchmark finding feeds the findings)" % (L, r_.get("category"), r_.get("category")))
    if ce.get("status") == "ceded" and "cession" not in refs:
        out.append("%s: a cession needs a finding with refs [\"cession\"]" % L)
    if sl.get("status") == "rider" and "second_life" not in refs:
        out.append("%s: a rider-dependent second life needs a finding with refs [\"second_life\"]" % L)
    prose_problems("%s verdict" % L, p.get("verdict"), out, lim["verdict_words"])
    ho = p.get("honest_opinion") or {}
    if not isinstance(ho, dict) or set(ho) != {"assessment", "good", "better"}:
        out.append("%s: honest_opinion is {assessment, good: [..], better: [..]}" % L)
    else:
        prose_problems("%s opinion assessment" % L, ho["assessment"], out, lim["opinion_assessment_words"])
        for k_ in ("good", "better"):
            if not isinstance(ho[k_], list):
                out.append("%s: honest_opinion.%s is a list" % (L, k_))
            else:
                for x in ho[k_]:
                    prose_problems("%s opinion %s" % (L, k_), x, out, lim["opinion_item_words"])


def proposed_problems(a, ev, docs, today, dec, out, images, lim, pols):
    pd = a["proposed"]
    pk = docs_of(docs, "proposed")
    if len(pk) != 1:
        out.append("proposed_status present: exactly one proposed quote must be registered (role proposed)")
        return
    plabel, key = next(iter(pk.items()))
    if not isinstance(pd, dict):
        out.append("proposed: the proposed quote's details are needed")
        return
    keys = {"label", "insurer", "abbrev", "versus", "product_name", "quote_number", "quote_date", "valid_until", "premium", "categories", "projection", "assumption", "payback"}
    if set(pd) - keys:
        out.append("proposed: unknown keys %s" % sorted(set(pd) - keys))
        return
    if pd.get("label") != plabel:
        out.append("proposed: label must be the registered one (%r)" % plabel)
    if pd.get("insurer") != dec.get(plabel):
        out.append("proposed: insurer %r is not the declared one (%r)" % (pd.get("insurer"), dec.get(plabel)))
    abv = pd.get("abbrev") or ""
    if not re.fullmatch(r"[A-Za-z]{2,8}", abv):
        out.append("proposed: abbrev is the proposed insurer's short name in letters (for the file name, for example BR)")
    cur = sorted({p["insurer"] for p in pols if isinstance(p, dict)})
    if pd.get("versus") not in cur:
        out.append("proposed: versus must be the current insurer compared against: %s" % ", ".join(cur))
    e = ev.get(key)
    if has(e):
        for f_ in ("insurer", "product_name"):
            m = e.name("proposed %s" % f_, pd.get(f_))
            out.append(m) if m else None
        if e.code("proposed quote number", pd.get("quote_number")):
            out.append("proposed: quote_number %r is not in the quote's text" % pd.get("quote_number"))
        for f_ in ("quote_date", "valid_until"):
            if pd.get(f_):
                m = e.date("proposed %s" % f_, pd[f_])
                out.append(m) if m else None
    pr = pd.get("premium") or {}
    if not w.parse_money(pr.get("monthly")):
        out.append("proposed: premium.monthly is needed")
    else:
        check_claim("proposed premium", pr, key, ev, docs, out, values=(("amount", pr["monthly"]),), roles=("proposed",), images=images)
    cats = pd.get("categories")
    if not isinstance(cats, dict) or set(cats) != set(FOUR):
        out.append("proposed: categories needs exactly the four: %s, each {held: false} or {held: true, amount, premium (optional), evidence}" % ", ".join(FOUR))
    else:
        for c_ in FOUR:
            v = cats[c_]
            if not isinstance(v, dict) or not isinstance(v.get("held"), bool):
                out.append("proposed %s: {held: false} or {held: true, amount, evidence}" % c_)
            elif v["held"]:
                if not w.parse_money(v.get("amount")):
                    out.append("proposed %s: amount is needed" % c_)
                else:
                    check_claim("proposed %s" % c_, v, key, ev, docs, out, values=(("amount", v["amount"]), ("amount", v.get("premium"))), roles=("proposed",), images=images)
    pj = pd.get("projection")
    if pj:
        for j, row in enumerate(pj, 1):
            if not isinstance(row, dict) or row.get("n") != j or not w.parse_money(row.get("premium")):
                out.append("proposed projection row %d: {n: %d, premium, age, printed_pct}" % (j, j))
                break
            if has(e):
                m = e.number("proposed projection year %d" % j, row["premium"])
                if m:
                    out.append(m)
                    break
    if pd.get("assumption") and pj:
        out.append("proposed: an assumption is only for a quote with no printed table")
    pb = pd.get("payback")
    pbk = docs_of(docs, "payback_doc")
    if not isinstance(pb, dict) or not isinstance(pb.get("present"), bool):
        out.append("proposed.payback is {present: false, said (Paul's words)} or {present: true, ...}")
    elif pb["present"]:
        if len(pbk) != 1:
            out.append("proposed.payback present: register the insurer's own payback document (role payback_doc)")
        else:
            pkey = next(iter(pbk.values()))
            for f_ in ("today_value", "projected_value"):
                v_ = pb.get(f_)
                if not isinstance(v_, dict) or not w.parse_money(v_.get("amount")):
                    out.append("proposed.payback: %s is {amount, evidence} (the insurer's own payback document)" % f_)
                else:
                    check_claim("proposed payback %s" % f_, v_, pkey, ev, docs, out, values=(("amount", v_["amount"]),), roles=("payback_doc",), images=images)
            if pb.get("pay_out_date"):
                e2 = ev.get(pkey)
                m = e2.date("proposed payback pay_out_date", pb["pay_out_date"]) if has(e2) else None
                out.append(m) if m else None
            comps = pb.get("components")
            if not isinstance(comps, list) or not comps:
                out.append("proposed.payback: components are needed (each with name, amount, pay_out_date, how_paid, evidence)")
            else:
                for j, c_ in enumerate(comps, 1):
                    if not isinstance(c_, dict) or not (c_.get("name") or "").strip() or not (c_.get("how_paid") or "").strip() or not w.parse_money(c_.get("amount")):
                        out.append("proposed payback component %d: {name, amount, pay_out_date, how_paid, evidence}" % j)
                        continue
                    check_claim("proposed payback component %d" % j, c_, pkey, ev, docs, out, values=(("amount", c_["amount"]),), roles=("payback_doc",), images=images)
                    if c_.get("pay_out_date") and has(ev.get(pkey)):
                        m = ev[pkey].date("proposed payback component %d pay_out_date" % j, c_["pay_out_date"])
                        out.append(m) if m else None
            slide_text_problems("proposed payback name", pb.get("name"), out, 10)
            if isinstance(pb.get("guarantee"), dict):
                check_claim("proposed payback guarantee", pb["guarantee"], pkey, ev, docs, out, roles=("payback_doc",), images=images)
            else:
                out.append("proposed.payback: guarantee is {text, evidence}")
            if isinstance(pb.get("conditions"), dict):
                check_claim("proposed payback conditions", pb["conditions"], pkey, ev, docs, out, roles=("payback_doc",), images=images)
                slide_text_problems("proposed payback conditions", pb["conditions"].get("text"), out, lim["slide_bullet_words"])
            else:
                out.append("proposed.payback: conditions is {text (one short plain line), evidence}")
    else:
        if len((pb.get("said") or "").strip()) < 5:
            out.append("proposed.payback not present: put Paul's words in said (the quote has no payback)")
        if pbk:
            out.append("proposed.payback: a payback document is registered but payback is marked absent")
    vu = w.parse_date(pd.get("valid_until"))
    if pd.get("valid_until") and vu is None:
        out.append("proposed.valid_until must be DD/MM/YYYY")


def slides_problems(a, ev, docs, out, lim, pols, ff):
    sl = a["slides"]
    if not isinstance(sl, dict) or set(sl) != {"by_insurer", "report2"}:
        out.append("slides is {by_insurer: {<insurer>: {how_it_works, key_things, shortfalls}}, report2: null or {...}}")
        return
    insurers = sorted({p["insurer"] for p in pols if isinstance(p, dict)})
    bi = sl["by_insurer"]
    if not isinstance(bi, dict) or sorted(bi) != insurers:
        out.append("slides.by_insurer must have exactly one entry per current insurer: %s" % ", ".join(insurers))
        return
    by_label = {p["label"]: p for p in pols if isinstance(p, dict)}
    for ins, s in bi.items():
        if not isinstance(s, dict) or set(s) != {"how_it_works", "key_things", "shortfalls"}:
            out.append("slides %s: {how_it_works, key_things, shortfalls}" % ins)
            continue
        hw = s["how_it_works"]
        if not isinstance(hw, list) or not 1 <= len(hw) <= lim["slide_bullets_max"]:
            out.append("slides %s how_it_works: from 1 to %d bullets" % (ins, lim["slide_bullets_max"]))
        else:
            for x in hw:
                slide_text_problems("slides %s how_it_works" % ins, x, out, lim["slide_bullet_words"])
        for j, k in enumerate(s["key_things"] or [], 1):
            KL = "slides %s key thing %d" % (ins, j)
            if not isinstance(k, dict):
                out.append("%s: {text, policy, n}" % KL)
                continue
            slide_text_problems(KL, k.get("text"), out, lim["slide_bullet_words"])
            pol = by_label.get(k.get("policy"))
            fn = finding_numbers(pol) if pol else []
            if pol is None or not any(n == k.get("n") and t == "action" for n, t, _h, _d in fn):
                out.append("%s: policy and n must point at an Action Required finding of that policy" % KL)
        sf = s["shortfalls"] or []
        if sf and not ff:
            out.append("slides %s shortfalls: no Fact Find Summary is registered, so there is nothing to base a shortfall on" % ins)
        for j, k in enumerate(sf, 1):
            slide_text_problems("slides %s shortfall %d" % (ins, j), (k or {}).get("text"), out, lim["slide_bullet_words"])
            check_claim("slides %s shortfall %d" % (ins, j), k, "fact_find_summary", ev, docs, out, roles=("fact_find_summary",))
    r2 = sl["report2"]
    if a["proposed_status"] == "present":
        if not isinstance(r2, dict) or set(r2) != {"gains", "know", "detail", "next_steps", "payback_current"}:
            out.append("slides.report2 is {gains, know, detail, next_steps, payback_current}")
            return
        for k_ in ("gains", "know", "detail"):
            if not isinstance(r2[k_], list) or not 1 <= len(r2[k_]) <= lim["slide_bullets_max"]:
                out.append("slides.report2.%s: from 1 to %d bullets" % (k_, lim["slide_bullets_max"]))
            else:
                for x in r2[k_]:
                    slide_text_problems("slides.report2 %s" % k_, x, out, lim["slide_bullet_words"])
        ns = r2["next_steps"]
        if not isinstance(ns, list) or not 1 <= len(ns) <= lim["next_steps_max"]:
            out.append("slides.report2.next_steps: from 1 to %d, each {text, timing}" % lim["next_steps_max"])
        else:
            for x in ns:
                if not isinstance(x, dict):
                    out.append("slides.report2.next_steps: each {text, timing}")
                    continue
                slide_text_problems("slides.report2 next step", x.get("text"), out, lim["slide_bullet_words"])
                slide_text_problems("slides.report2 next step timing", x.get("timing"), out, 6)
        pc = r2["payback_current"]
        if not isinstance(pc, dict) or not isinstance(pc.get("present"), bool):
            out.append("slides.report2.payback_current is {present: false} or {present: true, name, text, source, evidence}")
        elif pc["present"]:
            slide_text_problems("slides.report2 current payback name", pc.get("name"), out, 10)
            slide_text_problems("slides.report2 current payback", pc.get("text"), out, lim["slide_bullet_words"])
            check_claim("slides.report2 current payback", pc, None, ev, docs, out, roles=POLICY_ROLES)
    elif r2 is not None:
        out.append("slides.report2 must be null when no proposed quote exists (Report 2 is not built)")


def annotate(a, ev, docs, today, run_client=None, state=None):
    """(a deep copy of the analysis carrying the kind of every statement, the problems). The saved file is never changed by the checks."""
    import copy
    b = copy.deepcopy(a)
    return b, analysis_problems(b, ev, docs, today, run_client, state)


# ------------------------------------------------------------------ computations
def finding_numbers(p):
    """[(n, tier, headline, detail)]: Action Required first, then For Your Awareness; the same numbers at the top of the report and in the full section."""
    fds = [f for f in ((p or {}).get("findings") or []) if isinstance(f, dict) and f.get("tier") in ("action", "awareness") and isinstance(f.get("headline"), str) and isinstance(f.get("detail"), str)]
    acts = [f for f in fds if f["tier"] == "action"]
    awr = [f for f in fds if f["tier"] == "awareness"]
    return [(i, f["tier"], f["headline"].strip(), f["detail"].strip()) for i, f in enumerate(acts + awr, 1)]


def projection_table(p, years=None):
    """{"mode": printed|computed|assumption|none, "rows": [{n, age, premium, pct, kind}], "rate"}: the insurer's own printed table, or computed from the stated yearly increase, or from Paul's
    assumption, or nothing: a number is never invented."""
    years = years or limits()["projection_years"]
    pr = p["premium"]
    start = w.parse_money(pr["monthly"])
    age0 = int(w.parse_money(pr["age_start"]["value"])) if pr.get("age_start") else None
    pj = pr.get("projection")
    rows, mode, rate = [], "none", None
    if pj:
        mode = "printed"
        prev = None
        for r in pj[:years]:
            prem = w.parse_money(r["premium"])
            calc = ((prem - prev) / prev * 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) if prev else None
            printed = w.parse_money(r["printed_pct"]) if r.get("printed_pct") else None
            rows.append({"n": r["n"], "age": r.get("age", (age0 + r["n"] - 1) if age0 is not None else None), "premium": prem, "pct": printed if printed is not None else calc,
                         "kind": "printed" if printed is not None else ("calculated" if calc is not None else None)})
            prev = prem
    else:
        pat = pr["pattern"]
        if pat["type"] == "fixed" and pat.get("rate"):
            mode, rate = "computed", w.parse_money(pat["rate"])
        elif pr.get("assumption"):
            mode, rate = "assumption", w.parse_money(pr["assumption"]["rate"])
        if rate is not None:
            prem = start
            for n in range(1, years + 1):
                if n > 1:
                    prem = (prem * (1 + rate / 100)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                rows.append({"n": n, "age": (age0 + n - 1) if age0 is not None else None, "premium": prem, "pct": rate if n > 1 else None, "kind": "computed" if n > 1 else None})
    return {"mode": mode, "rows": rows, "rate": rate}


def benefits_held(p):
    return [b for b in p["benefits"]]


def category_entries(pols, cat):
    """[(policy, benefit)] for one of the four categories across a set of policies (the main life and the second life)."""
    return [(p, b) for p in pols for b in p["benefits"] if b["category"] == cat]


def combined_premium(pols):
    return sum((w.parse_money(p["premium"]["monthly"]) for p in pols), Decimal("0.00"))


def benefit_rows(p):
    """The Benefit Summary Table rows for the internal report: (label, sum assured text, premium text)."""
    out = []
    for b in p["benefits"]:
        lab = b["label"].strip() + (" (second life)" if b.get("life") == "second" else "")
        sa = money(b["sum_assured"]) + (" per month" if b.get("unit") == "monthly" else "")
        out.append((lab, sa, money(b["premium"]) if b.get("premium") else "-"))
    return out


def not_held_types(p):
    held = {b["category"] for b in p["benefits"]}
    return [CAT_NAMES[c] for c in FOUR if c not in held]


def internal_name(a, p, d):
    same = [x for x in a["policies"] if x["insurer"] == p["insurer"]]
    mid = "%s_%s_%s" % (file_part(a["client_first_name"]), file_part(a["client_surname"]), file_part(p["insurer"]))
    if len(same) > 1:
        mid += "_" + file_part(p["product_name"])
    return "%s_Policy_Analysis - %s.pdf" % (mid, short(d))


def slide_names(a, d):
    """[(kind, insurer or None, file name)]: Report 1 per current insurer, Report 2 only when a proposed quote exists."""
    base = "%s_%s" % (file_part(a["client_first_name"]), file_part(a["client_surname"]))
    out = []
    for ins in sorted({p["insurer"] for p in a["policies"]}):
        out.append(("report1", ins, "%s_%s_Policy_Analysis_Slide - %s.pdf" % (base, file_part(ins), short(d))))
    if a["proposed_status"] == "present":
        pd = a["proposed"]
        out.append(("report2", pd["versus"], "%s_%s_VS_%s_Policy_Analysis_Slide - %s.pdf" % (base, file_part(pd["abbrev"]), file_part(pd["versus"]), short(d))))
    return out


def all_names(a, d):
    return [internal_name(a, p, d) for p in a["policies"]] + [n for _k, _i, n in slide_names(a, d)]


def statement_counts(a):
    c = {}
    for p in a["policies"]:
        def walk(x):
            if isinstance(x, dict):
                if x.get("_kind"):
                    c[x["_kind"]] = c.get(x["_kind"], 0) + 1
                for v in x.values():
                    walk(v)
            elif isinstance(x, list):
                for v in x:
                    walk(v)
        walk(p)
    return c


def program_flags(a, docs, ev, today):
    out = []
    lim = limits()
    n_single = n_inf = 0
    for p in a["policies"]:
        L = p["label"]
        tbl = projection_table(p)
        if tbl["mode"] == "none":
            out.append("%s: no projection table and no stated yearly increase: the 10-year table reads 'not provided' (no number is invented)" % L)
        elif tbl["mode"] in ("computed", "assumption"):
            out.append("%s: the 10-year table is %s (labelled illustrative)" % (L, "computed from the stated yearly increase" if tbl["mode"] == "computed" else "computed from Paul's assumption"))
        elif len(tbl["rows"]) < lim["projection_years"]:
            out.append("%s: the printed table has only %d year(s): the rest read 'not provided'" % (L, len(tbl["rows"])))
        if p["premium"]["guarantee"].get("not_stated"):
            out.append("%s: the premium guarantee period is not stated on the document: confirm it with the insurer" % L)
        prem = [w.parse_money(b["premium"]) for b in p["benefits"] if b.get("premium")]
        if prem and len(prem) == len(p["benefits"]) and sum(prem) != w.parse_money(p["premium"]["monthly"]):
            out.append("%s: the benefit premiums add up to %s but the document's total is %s (loadings, fees or rounding?): the document's total is used" % (L, money(sum(prem)), p["premium"]["monthly"]))
        for r_ in p["benchmark"]:
            if r_.get("_kind") == "product_single":
                n_single += 1
        cnt = {}

        def walk(x):
            if isinstance(x, dict):
                if x.get("_kind"):
                    cnt[x["_kind"]] = cnt.get(x["_kind"], 0) + 1
                for v in x.values():
                    walk(v)
            elif isinstance(x, list):
                for v in x:
                    walk(v)
        walk({k: v for k, v in p.items() if k != "benchmark"})
        n_single += cnt.get("product_single", 0)
        n_inf += cnt.get("inference", 0)
    if n_single:
        out.append("%d product statement(s) rest on a SINGLE source: they are labelled SINGLE SOURCE in the report" % n_single)
    if n_inf:
        out.append("%d statement(s) are inferences, labelled 'to be confirmed' in the report" % n_inf)
    if "fact_find_summary" not in docs["docs"]:
        out.append("No Fact Find Summary: whether the cover is adequate cannot be fully assessed (the report says so)")
    if a["proposed_status"] == "present":
        vu = w.parse_date(a["proposed"].get("valid_until"))
        if vu is not None:
            if vu < today:
                out.append("The proposed quote's validity date (%s) has passed" % a["proposed"]["valid_until"])
            elif (vu - today).days <= lim["quote_expiry_warning_days"]:
                out.append("The proposed quote is valid only until %s (within %d days)" % (a["proposed"]["valid_until"], lim["quote_expiry_warning_days"]))
        elif a["proposed"] and not a["proposed"].get("valid_until"):
            out.append("The proposed quote shows no validity date")
    return out


def paul_flags(a, docs, ev, today):
    return program_flags(a, docs, ev, today) + list(a.get("flags") or [])


def check_summary(a, today):
    """What the check step proves and shows (a pure function of the analysis): bound to the step by its hash."""
    per = {}
    for p in a["policies"]:
        t = projection_table(p)
        per[p["label"]] = {"mode": t["mode"], "years": len(t["rows"]), "findings": [[n, tier, h] for n, tier, h, _d in finding_numbers(p)],
                           "benchmark": {r_["category"]: r_["outcome"] for r_ in p["benchmark"]}, "combined": str(combined_premium([p]))}
    return {"per_policy": per, "counts": statement_counts(a), "proposed": a["proposed_status"]}
