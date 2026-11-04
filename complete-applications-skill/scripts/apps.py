"""The form engine of the complete-applications-skill: the two real blank forms, the rules on every field, the names of the folder and the file,
the fill, the read-back of EVERY field, the proof that each filled box shows something, and the before and after of a correction.
No client data is kept in this file. Nothing here proves that a client's value is TRUE: only that it is in a document (or Paul's words), that it
passes the form's own rules, and that what was written reads back and shows.
"""
import copy
import datetime as dt
import glob
import hashlib
import os
import re
import subprocess
import tempfile
import warnings
from decimal import Decimal

import wrlib as w

warnings.filterwarnings("ignore")
ASSETS = os.path.join(w.SKILL_DIR, "assets")
FORMS = ("om", "general")
FORM_NAMES = {"om": "Old Mutual application", "general": "General Short Risk application"}


def _asset(name):
    return w.load_json(os.path.join(ASSETS, name))


def settings():
    return _asset("settings.json")


def spec():
    return _asset("forms.json")


def fspec(form):
    return spec()[form]


def template_path(form):
    return os.path.join(ASSETS, fspec(form)["template"])


# ------------------------------------------------------------------ the forms: fields, options, drift
def live_fields(path):
    from pypdf import PdfReader
    out = {}
    for k, v in (PdfReader(path).get_fields() or {}).items():
        d = {"type": "choice" if v.get("/FT") == "/Ch" else "text"}
        if d["type"] == "choice":
            d["options_raw"] = [str(o) for o in (v.get("/Opt") or [])]
        out[k] = d
    return out


def drift_problems(form, path=None):
    """Template drift: the shipped blank form against the frozen list (path None), or a filled form's fields against it. [str]"""
    sp = fspec(form)
    out = []
    if path is None:
        p = template_path(form)
        if w.sha256_file(p) != sp["sha256"]:
            out.append("the blank %s form is not the one this skill was built on (its checksum changed)" % FORM_NAMES[form])
        path = p
    live = live_fields(path)
    names, want = set(live), set(sp["fields"])
    if names != want:
        out.append("the field names differ: %d new, %d missing (for example %s)" % (len(names - want), len(want - names), sorted((names ^ want))[:3]))
    for k in sorted(names & want):
        a, b = live[k], sp["fields"][k]
        if a["type"] != b["type"]:
            out.append("field %s changed type" % k)
        elif a["type"] == "choice" and k != "Product" and a["options_raw"] != b["options_raw"]:
            out.append("the dropdown options of %s changed" % k)
        elif a["type"] == "choice" and k == "Product" and not set(b["options_raw"]) <= set(a["options_raw"]):
            out.append("a base option of Product was removed or changed")
    return out


def detect_form(path):
    """Which of the two forms a PDF is, by its field names; None if neither."""
    names = set(live_fields(path))
    for f in FORMS:
        if names == set(fspec(f)["fields"]):
            return f
    return None


def key_to_field(form, key):
    if form == "om":
        return key if key in fspec("om")["fields"] else None
    return fspec("general")["keys"].get(key)


def field_to_key(form, name):
    if form == "om":
        return name
    inv = {v: k for k, v in fspec("general")["keys"].items()}
    return inv.get(name)


def label(form, name):
    """What Paul reads for a field: the OM form's own field name, or the General form's meaning name (street_no, suburb ...)."""
    return (field_to_key(form, name) or name) if form == "general" else name


def options(form, name):
    """{stripped option: raw option} of a dropdown (the empty option left out)."""
    raw = fspec(form)["fields"][name].get("options_raw") or []
    return {o.strip(): o for o in raw if o.strip()}


def is_choice(form, name):
    return fspec(form)["fields"][name]["type"] == "choice"


# ------------------------------------------------------------------ small value rules
SENSITIVE = {"om": {"IDNumber", "BenIDNumber", "BenIDNumber_2", "BenIDNumber_3", "AccountNumber", "TaxNumber", "ForeignTaxNumber"},
             "general": {"id_number", "ben1_id", "ben2_id", "child1_id", "child2_id", "account_number"}}


def money_r(d):
    return "R {:,.2f}".format(Decimal(d))


def mask_text(s):
    """Digits of 8 or more are shown as ... and the last four (Paul's rule: ID and account numbers masked to the last 4)."""
    def rep(m):
        ds = w.digits(m.group(0))
        return "\u2022\u2022\u2022" + ds[-4:] if len(ds) >= 8 else m.group(0)
    return re.sub(r"\d[\d \-]{6,}\d", rep, str(s))


def id_flags(value):
    """Flags only (never a refusal): the date part and the check digit of a South African ID number."""
    d = w.digits(value)
    if len(d) != 13:
        return ["not 13 digits"]
    out = []
    try:
        yy, mm, dd = int(d[:2]), int(d[2:4]), int(d[4:6])
        dt.date(2000 + yy if yy < 30 else 1900 + yy, mm, dd)
    except ValueError:
        out.append("the date part is not a real date")
    tot = 0
    for i, ch in enumerate(d[:12]):
        x = int(ch)
        if i % 2:
            x *= 2
            x = x - 9 if x > 9 else x
        tot += x
    if (10 - tot % 10) % 10 != int(d[12]):
        out.append("the check digit does not match")
    return out


def value_in_line(value, line):
    v = str(value)
    if w.norm(v) and w.norm(v) in w.norm(line):
        return True
    dv = w.digits(v)
    return bool(dv) and len(dv) >= 3 and dv in w.digits(line) and len(dv) >= len(re.sub(r"[^\w]", "", v)) - 2


def day_of(text):
    m = re.search(r"\d{1,2}", str(text))
    return int(m.group(0)) if m else None


def ddmmyy(date_text):
    d = w.parse_date(date_text)
    return d.strftime("%d/%m/%y") if d else None


def parse_amount(x):
    try:
        d = Decimal(str(x).replace(",", "").replace(" ", "").replace("R", ""))
        return d if d > 0 else None
    except Exception:
        return None


# ------------------------------------------------------------------ names (built from fixed lists, never typed)
def kind_of(app):
    return app.get("kind")


def amount_text(app):
    a = parse_amount(app.get("amount"))
    return None if a is None else (money_r(a) + " p.m." if kind_of(app) == "recurring" else money_r(a) + " - Lump Sum")


def product_type(app):
    """The product type as the file name needs it: OM = the base product's short name, risk = the cover line."""
    s = settings()
    p = app.get("product") or {}
    if app["form"] == "general":
        return p.get("cover_line") if p.get("cover_line") in s["cover_lines"] else None
    return s["om_short"].get((p.get("option") or "").strip()) or (p.get("short") if len((p.get("short_paul_said") or "").strip()) >= 5 else None)


def abbr_of(app):
    s = settings()
    ins = app.get("insurer") or {}
    known = s["insurer_abbr"].get(ins.get("name"))
    if known:
        return known
    return ins.get("abbr") if ins.get("abbr") and len((ins.get("abbr_paul_said") or "").strip()) >= 5 else None


def file_name(app, client):
    t, ab, am = product_type(app), abbr_of(app), amount_text(app)
    d = w.parse_date(app.get("meeting_date"))
    if not (t and ab and am and d):
        return None
    return w.safe_filename("%s - %s Application - %s - %s - (%s %s).pdf" % (ab, t, d.strftime("%d.%m.%y"), am, client["first"], client["surname"]))


def folder_name(app, client):
    s = settings()
    p = app.get("product") or {}
    ab, am = abbr_of(app), amount_text(app)
    if not (ab and am):
        return None
    base = "%s, %s - (" % (client["surname"], client["first"])
    if app["form"] == "general":
        ty = s["folder_type_risk"].get(p.get("cover_line"))
        return w.safe_filename(base + "%s - %s - %s)" % (ab, ty, am)) if ty else None
    inv, ty = product_type(app), p.get("type")
    if not inv or ty not in s["om_types"]:
        return None
    return w.safe_filename(base + "%s - %s - %s - %s)" % (ab, inv, ty, am))


# ------------------------------------------------------------------ the values of one application
LABEL = {}


def _src(entry):
    if entry.get("from_app"):
        fa = entry["from_app"]
        return "carried from application %s (%s)" % (fa.get("id"), fa.get("key"))
    if entry.get("evidence"):
        return "%s: \"%s\"" % (entry["evidence"].get("doc"), entry["evidence"].get("line"))
    return "Paul: %s" % entry.get("paul_said")


def entry_problems(form, key, entry, evid, docs_known, label):
    """Proof for one entered value: [str]. A value needs a verbatim line of a registered document (its digits or words in that line) or Paul's words."""
    s = settings()
    if not isinstance(entry, dict) or not str(entry.get("value", "")).strip():
        return ["%s: a value and its proof are needed" % label]
    val = str(entry["value"]).strip()
    name = key_to_field(form, key)
    out = []
    ev, pa = entry.get("evidence"), (entry.get("paul_said") or "").strip()
    if ev:
        role, line = ev.get("doc"), (ev.get("line") or "").strip()
        if role in s["no_evidence_roles"]:
            out.append("%s: an older application is never a source unless Paul says so (use his words)" % label)
        elif role not in docs_known:
            out.append("%s: the document '%s' is not registered for this run" % (label, role))
        else:
            e = evid.get(role)
            if e is None or not e.has_text:
                out.append("%s: '%s' has no readable text; use Paul's words" % (label, role))
            elif e.name(label, line):
                out.append("%s: the evidence line is not in the document's text" % label)
            elif not is_choice(form, name) and not value_in_line(val, line):
                out.append("%s: the value is not in its evidence line" % label)
    elif len(pa) < 5:
        out.append("%s: no proof (a document line, or Paul's words)" % label)
    if is_choice(form, name):
        if val not in options(form, name):
            out.append("%s: '%s' is not one of the form's options (%s)" % (label, val, "; ".join(options(form, name))))
    elif len(val) > 200 or re.search(r"[\x00-\x1f]", val):
        out.append("%s: the value is too long or has control characters" % label)
    return out


def build_values(app, client, evid, docs_known, today):
    """Prefill: the full value set of one application. Returns dict(values {pdf field: text}, sources {pdf field: text}, problems, flags, new_option)."""
    s = settings()
    form = app["form"]
    sp = fspec(form)
    R = {"values": {}, "sources": {}, "problems": [], "flags": [], "new_option": None}
    P, F = R["problems"], R["flags"]
    fields = app.get("fields") or {}
    tag = "%s (%s)" % (app.get("id"), FORM_NAMES.get(form, form))
    derived = set(sp["derived"])
    for key, entry in fields.items():
        name = key_to_field(form, key)
        if name is None:
            P.append("%s: '%s' is not a field of this form" % (tag, key))
        elif key in sp["never"] or name in sp["never"]:
            P.append("%s: %s is never written by the program (the client signs)" % (tag, key))
        elif key in derived and not _derived_allowed(form, key, fields, app):
            P.append("%s: %s is built by the program from the other answers; do not enter it" % (tag, key))
        else:
            pp = entry_problems(form, key, entry, evid, docs_known, "%s, %s" % (tag, key))
            P += pp
            if not pp:
                v = str(entry["value"]).strip()
                R["values"][name] = options(form, name).get(v, v) if is_choice(form, name) else v
                R["sources"][name] = _src(entry)
    d = w.parse_date(app.get("meeting_date"))
    if d is None:
        P.append("%s: the meeting date (DD/MM/YYYY) is needed: it is the signature date, never blank" % tag)
    if parse_amount(app.get("amount")) is None or kind_of(app) not in ("recurring", "lump"):
        P.append("%s: the amount (a number) and kind (recurring or lump) are needed" % tag)
    rep = app.get("replacement") or {}
    ans = rep.get("answer")
    if ans not in ("Yes", "No"):
        P.append("%s: replacement needs a real answer, Yes or No (never a guess)" % tag)
    else:
        src = rep.get("source") or {}
        if src.get("doc"):
            e = evid.get(src["doc"])
            if src["doc"] not in docs_known or e is None or not e.has_text or e.name("replacement", src.get("line") or ""):
                P.append("%s: the replacement answer's document line is not in a registered document" % tag)
        elif len((src.get("paul_said") or "").strip()) < 5:
            P.append("%s: the replacement answer needs a document line or Paul's words" % tag)
        pols = rep.get("policies") or []
        if ans == "Yes":
            if not pols:
                P.append("%s: a replacement needs the insurer and policy number of each replaced policy" % tag)
            for i, pl in enumerate(pols, 1):
                ev = pl.get("evidence") or {}
                e = evid.get(ev.get("doc")) if ev.get("doc") in docs_known else None
                ok = e is not None and e.has_text and not e.name("p", ev.get("line") or "")
                if ev.get("doc") != "policy_schedule" and len((pl.get("paul_said") or "").strip()) < 5:
                    P.append("%s: replaced policy %d: the number is checked against the policy schedule document, not an older draft (or Paul's words)" % (tag, i))
                elif ev.get("doc") == "policy_schedule" and (not ok or w.digits(pl.get("policy_no")) not in w.digits(ev.get("line"))):
                    P.append("%s: replaced policy %d: the policy number is not in its schedule line" % (tag, i))
                if not (pl.get("insurer") and pl.get("policy_no")):
                    P.append("%s: replaced policy %d needs insurer and policy_no" % (tag, i))
        elif pols:
            P.append("%s: no replacement, but replaced policies are listed" % tag)
    # ---- the fields the program builds
    V, S = R["values"], R["sources"]
    am = parse_amount(app.get("amount"))
    sd = ddmmyy(app.get("meeting_date")) if d else None
    if form == "om":
        base = ((app.get("product") or {}).get("option") or "").strip()
        opts = options("om", "Product")
        if base not in opts:
            P.append("%s: the product '%s' is not one of the form's products (%s)" % (tag, base, "; ".join(opts)))
        elif am is not None and kind_of(app) in ("recurring", "lump"):
            val = "%s - %s%s" % (base, money_r(am), " p.m." if kind_of(app) == "recurring" else "")
            V["Product"], S["Product"] = val, "program: the form's own product plus the amount"
            R["new_option"] = val
        if sd:
            V["SignatureDate"], S["SignatureDate"] = sd, "program: the meeting date"
        if ans in ("Yes", "No"):
            V["IsReplacement"], S["IsReplacement"] = ans, "replacement answer: " + _src(rep.get("source") or {})
            pols = rep.get("policies") or []
            V["ReplacedPolicyNumbers"] = "; ".join("%s, Policy No. %s" % (p_["insurer"], p_["policy_no"]) for p_ in pols if p_.get("insurer") and p_.get("policy_no")) if ans == "Yes" else "N/A"
            S["ReplacedPolicyNumbers"] = "program: from the replacement answer"
        ft = (fields.get("ForeignTaxObligation") or {}).get("value")
        if ft == "No":
            V["ForeignTaxNumber"], S["ForeignTaxNumber"] = "N/A", "program: no foreign tax obligation"
        ok_ = (fields.get("OwnKnowledge") or {}).get("value")
        if ok_ == "Yes":
            V["OriginateFrom"], S["OriginateFrom"] = "N/A", "program: the advisor knows the source of funds"
        if kind_of(app) == "lump":
            V["DeferredPremiumFacility"], S["DeferredPremiumFacility"] = "N/A", "program: a lump sum"
        ms = (fields.get("MaritalStatus") or {}).get("value")
        if ms in s["marital_na"]:
            V["MaritalContractType"], S["MaritalContractType"] = "N/A", "program: %s" % ms
    else:
        ins = (app.get("insurer") or {}).get("name")
        if ins not in s["insurer_options"]:
            P.append("%s: the insurer '%s' is not one of the form's insurers" % (tag, ins))
        else:
            V["List Box 1"], S["List Box 1"] = options("general", "List Box 1")[ins], "program: the insurer"
        cl = (app.get("product") or {}).get("cover_line")
        if cl not in s["cover_lines"]:
            P.append("%s: the cover line must be one of %s" % (tag, ", ".join(s["cover_lines"])))
        else:
            V["List Box 2"], S["List Box 2"] = options("general", "List Box 2")[s["cover_lines"][cl]], "program: %s counts as %s on the form" % (cl, s["cover_lines"][cl])
        if sd:
            V["Text Box 5_8"], S["Text Box 5_8"] = sd, "program: the meeting date"
        if ans in ("Yes", "No"):
            V["List Box 3_5"], S["List Box 3_5"] = options("general", "List Box 3_5")[ans], "replacement answer: " + _src(rep.get("source") or {})
            pols = rep.get("policies") or []
            if ans == "Yes":
                V["Text Box 5_5"] = "; ".join(dict.fromkeys(p_["insurer"] for p_ in pols if p_.get("insurer")))
                V["Text Box 5_6"] = "; ".join(p_["policy_no"] for p_ in pols if p_.get("policy_no"))
                S["Text Box 5_5"] = S["Text Box 5_6"] = "program: from the replaced policies"
    # ---- rules on the whole set
    P += consistency_problems(form, V, tag)
    F += value_flags(form, V, tag)
    return R


def _derived_allowed(form, key, fields, app):
    """A derived field may be entered only where the form needs an answer the program cannot work out."""
    g = lambda k: (fields.get(k) or {}).get("value")
    if form == "om":
        if key == "ForeignTaxNumber":
            return g("ForeignTaxObligation") == "Yes"
        if key == "OriginateFrom":
            return g("OwnKnowledge") == "No"
        if key == "DeferredPremiumFacility":
            return kind_of(app) == "recurring"
        if key == "MaritalContractType":
            return g("MaritalStatus") not in settings()["marital_na"]
    return False


def consistency_problems(form, V, tag):
    """The N/A discipline and the other rules on a full value set (used for a pre-fill AND after a correction): [str]."""
    P = []
    s = settings()
    g = lambda n: (V.get(n) or "").strip()
    if form == "om":
        if g("ForeignTaxObligation") == "No" and g("ForeignTaxNumber") != "N/A":
            P.append("%s: no foreign tax obligation, so ForeignTaxNumber must be N/A" % tag)
        if g("ForeignTaxObligation") == "Yes" and g("ForeignTaxNumber") in ("", "N/A"):
            P.append("%s: a foreign tax obligation needs the ForeignTaxNumber" % tag)
        if g("OwnKnowledge") == "Yes" and g("OriginateFrom") != "N/A":
            P.append("%s: the advisor knows the source of funds, so OriginateFrom must be N/A" % tag)
        if g("OwnKnowledge") == "No" and g("OriginateFrom") in ("", "N/A"):
            P.append("%s: OwnKnowledge is No, so OriginateFrom needs the place the funds came from" % tag)
        if g("IsReplacement") == "No" and g("ReplacedPolicyNumbers") != "N/A":
            P.append("%s: not a replacement, so ReplacedPolicyNumbers must be N/A" % tag)
        if g("IsReplacement") == "Yes" and g("ReplacedPolicyNumbers") in ("", "N/A"):
            P.append("%s: a replacement needs the replaced policy numbers" % tag)
        if g("DeferredPremiumFacility") == "" and "Lump" in g("Product"):
            P.append("%s: a lump sum needs DeferredPremiumFacility N/A" % tag)
        if not g("Product"):
            P.append("%s: Product is empty" % tag)
        if not _valid_yy(g("SignatureDate")):
            P.append("%s: SignatureDate must be the meeting date as DD/MM/YY, never blank" % tag)
        if g("DateOfEntry") and w.parse_date(g("DateOfEntry")) is None:
            P.append("%s: DateOfEntry must be DD/MM/YYYY" % tag)
    else:
        if not _valid_yy(g("Text Box 5_8")):
            P.append("%s: the DATE must be the meeting date as DD/MM/YY, never blank" % tag)
        rp = g("List Box 3_5")
        if rp == "Yes" and not (g("Text Box 5_5") and g("Text Box 5_6")):
            P.append("%s: a replacement needs the existing company and policy number" % tag)
        if rp == "No" and (g("Text Box 5_5") or g("Text Box 5_6")):
            P.append("%s: not a replacement, so the existing company and policy number stay blank" % tag)
        dd = g("Text Box 4_20")
        if dd and day_of(dd) in s["debit_days_refused"]:
            P.append("%s: the debit date cannot be the 10th to the 14th (the form says so)" % tag)
        elif dd and day_of(dd) is None:
            P.append("%s: the debit date must be a day of the month" % tag)
    return P


def _valid_yy(text):
    try:
        dt.datetime.strptime(text, "%d/%m/%y")
        return True
    except ValueError:
        return False


def value_flags(form, V, tag):
    """Flags only (Paul: never a refusal): ID date part and check digit, beneficiary shares, email and phone shape."""
    F = []
    ids = {"om": ["IDNumber", "BenIDNumber", "BenIDNumber_2", "BenIDNumber_3"], "general": ["Text Box 4_3", "Text Box 5_16", "Text Box 5_18", "Text Box 5_12", "Text Box 5_14"]}[form]
    for n in ids:
        if (V.get(n) or "").strip():
            for fl in id_flags(V[n]):
                F.append("%s: %s: %s" % (tag, mask_text(V[n]), fl))
    shares = {"om": ["BenShare", "BenShare_2", "BenShare_3"], "general": ["Text Box 4_24", "Text Box 4_26"]}[form]
    got = [V[n] for n in shares if (V.get(n) or "").strip()]
    if got:
        try:
            tot = sum(Decimal(re.sub(r"[^\d.]", "", x)) for x in got)
            if tot != 100:
                F.append("%s: the beneficiary shares add up to %s%%, not 100%%" % (tag, tot))
        except Exception:
            F.append("%s: a beneficiary share is not a number" % tag)
    mail = {"om": ["Email"], "general": ["Text Box 5", "Text Box 4_22"]}[form]
    for n in mail:
        if (V.get(n) or "").strip() and not re.fullmatch(r"[\w.+-]+@[\w-]+\.[\w.-]+", V[n].strip()):
            F.append("%s: the email address does not look right" % tag)
    ph = {"om": ["TelH", "TelW", "TelCell"], "general": ["Text Box 4_4", "Text Box 4_5"]}[form]
    for n in ph:
        if (V.get(n) or "").strip() and not 9 <= len(w.digits(V[n])) <= 12:
            F.append("%s: a phone number does not have 9 to 12 digits" % tag)
    return F


# ------------------------------------------------------------------ a correction: the before and after
def read_values(path):
    from pypdf import PdfReader
    out = {}
    for k, v in (PdfReader(path).get_fields() or {}).items():
        x = v.get("/V")
        out[k] = "" if x is None else str(x)
    return out


def never_carry(form, key):
    return key in spec()["never_carry"][form]


def carry_source(form, key, fa, currents):
    """The value another current application holds for `key`, as (value, hard problem, soft problem). A soft problem (a product-specific answer)
    can be waived by Paul's words; a hard one cannot. currents: {id: {"form", "values"}}."""
    src = currents.get(fa.get("id"))
    if src is None:
        return None, "application %s is not a registered current application" % fa.get("id"), None
    sform, skey = src["form"], fa.get("key")
    soft = None
    if sform == form:
        if key_to_field(sform, skey) is None:
            return None, "%s is not a field of application %s" % (skey, fa.get("id")), None
        if never_carry(form, key) or never_carry(form, skey):
            soft = "%s is product-specific: never carried across unless Paul says so" % key
    else:
        pair = next((p_ for p_ in spec()["crosswalk"] if (form == "om" and p_[0] == key and p_[1] == skey) or (form == "general" and p_[1] == key and p_[0] == skey)), None)
        if pair is None:
            return None, "%s and %s are not a one-to-one pair between the two forms (ask Paul)" % (key, skey), None
    v = (src["values"].get(key_to_field(sform, skey)) or "").strip()
    return (v, None, soft) if v else (None, "the source application holds nothing for %s" % skey, None)


def correction_values(app, current, currents, evid, docs_known, today):
    """A correction: the current application's values with ONLY the planned changes. currents: every registered current application {id: {"form","values"}}.
    Returns dict(values, old, changes [(field, old, new, source)], problems, flags)."""
    form = current["form"]
    old = dict(current["values"])
    R = {"values": dict(old), "old": old, "changes": [], "problems": [], "flags": [], "new_option": None}
    P = R["problems"]
    tag = "%s (%s)" % (app.get("id"), FORM_NAMES[form])
    ch = app.get("changes") or {}
    if not ch:
        P.append("%s: no change was entered" % tag)
    sp = fspec(form)
    others = {i: c for i, c in currents.items() if i != app.get("id")}
    for key, entry in ch.items():
        name = key_to_field(form, key)
        label = "%s, %s" % (tag, key)
        if name is None:
            P.append("%s: not a field of this form" % label)
            continue
        if name in sp["never"] or key in sp["never"]:
            P.append("%s: signature fields are never touched" % label)
            continue
        if isinstance(entry, dict) and entry.get("from_app"):
            fa = entry["from_app"]
            val, hard, soft = carry_source(form, key, fa, others)
            said = len((entry.get("paul_said") or "").strip()) >= 5
            if hard:
                P.append("%s: %s" % (label, hard))
                continue
            if soft and not said:
                P.append("%s: %s" % (label, soft))
                continue
            for i, c in others.items():
                if i == fa.get("id"):
                    continue
                ek = key if c["form"] == form else _pair_key(form, key, c["form"])
                if not ek or never_carry(c["form"], ek):
                    continue
                alt = (c["values"].get(key_to_field(c["form"], ek)) or "").strip()
                if alt and alt != val and not said:
                    P.append("%s: current applications %s and %s hold different values for this detail: STOP and ask Paul which is right" % (label, fa.get("id"), i))
            entry = dict(entry, value=val)
        else:
            pp = entry_problems(form, key, entry, evid, docs_known, label)
            P += pp
            if pp:
                continue
            val = str(entry["value"]).strip()
        new = options(form, name).get(val, val) if is_choice(form, name) else val
        if new != old.get(name, ""):
            R["values"][name] = new
            R["changes"].append((name, old.get(name, ""), new, _src(entry)))
    P += consistency_problems(form, R["values"], tag)
    R["flags"] += value_flags(form, {k: v for k, v in R["values"].items() if v != old.get(k, "")}, tag)
    return R


def _pair_key(form, key, other_form):
    for a, b in spec()["crosswalk"]:
        if form == "om" and a == key and other_form == "general":
            return b
        if form == "general" and b == key and other_form == "om":
            return a
    return None


# ------------------------------------------------------------------ fill, read back, render
def add_option(writer, name, new_value):
    """One rule: a new Product option goes right after the base option it is a variant of (or at the end)."""
    from pypdf.generic import ArrayObject, NameObject, TextStringObject
    for f in writer._root_object["/AcroForm"]["/Fields"]:
        obj = f.get_object()
        if obj.get("/T") == name:
            vals = [str(o) for o in (obj.get("/Opt") or [])]
            if new_value in vals:
                return
            base = new_value.split(" - R ")[0].strip()
            at = next((i + 1 for i, v in enumerate(vals) if v.strip() == base), len([v for v in vals if v.strip()]))
            vals.insert(at, new_value)
            obj[NameObject("/Opt")] = ArrayObject([TextStringObject(v) for v in vals])
            return
    raise RuntimeError("%s not found in the form: has the form changed?" % name)


def fill(form, values, out_path, new_option=None, start_path=None):
    """Write values into a copy of the real blank form (or of a current application for a correction). Never recreates the page."""
    from pypdf import PdfReader, PdfWriter
    reader = PdfReader(start_path or template_path(form))
    writer = PdfWriter()
    writer.append(reader)
    if new_option:
        add_option(writer, "Product", new_option)
    for page in writer.pages:
        writer.update_page_form_field_values(page, {k: v for k, v in values.items() if v is not None}, auto_regenerate=False)
    _select_options(writer, values)
    writer.set_need_appearances_writer(True)
    with open(out_path, "wb") as fh:
        writer.write(fh)
    return out_path


def _select_options(writer, values):
    """A dropdown shows its value in a viewer only when the chosen option is also marked selected (/I): without it the value is set but the box looks empty
    (the viewer issue the old text warned about). One rule for both forms."""
    from pypdf.generic import ArrayObject, NameObject, NumberObject
    for f in writer._root_object["/AcroForm"]["/Fields"]:
        o = f.get_object()
        n = o.get("/T")
        if n in values and o.get("/FT") == "/Ch" and o.get("/Opt") is not None:
            opts = [str(x) for x in o["/Opt"]]
            if values[n] in opts:
                o[NameObject("/I")] = ArrayObject([NumberObject(opts.index(values[n]))])


def readback_problems(form, path, expected):
    """EVERY field of the saved PDF against what was intended (a field not in `expected` must be empty): [str]."""
    got = read_values(path)
    out = []
    for name in fspec(form)["fields"]:
        want = (expected.get(name) or "").strip()
        have = (got.get(name) or "").strip()
        if have != want:
            out.append("%s: reads back '%s', wanted '%s'" % (name, mask_text(have), mask_text(want)))
    extra = sorted(set(got) - set(fspec(form)["fields"]))
    if extra:
        out.append("fields not in the form: %s" % extra[:3])
    return out


def field_rects(path):
    from pypdf import PdfReader
    r = PdfReader(path)
    out = {}
    for pi, page in enumerate(r.pages):
        h = float(page.mediabox.height)
        for a in page.get("/Annots") or []:
            o = a.get_object()
            name = o.get("/T") or (o.get("/Parent").get_object().get("/T") if o.get("/Parent") else None)
            if name and o.get("/Rect") is not None:
                x0, y0, x1, y1 = [float(v) for v in o["/Rect"]]
                out[str(name)] = (pi, (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)), h)
    return out


def _render(pdf, prefix, dpi):
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", pdf, prefix], check=True, capture_output=True)
    files = glob.glob(prefix + "-*.png")
    return sorted(files, key=lambda f: int(re.search(r"-(\d+)\.png$", f).group(1)))


def render_proof(filled_pdf, base_pdf, names):
    """Each field in `names` must LOOK different in the render of the filled form than in the render of the base form (the blank, or the application
    before a correction). Returns [field names that show nothing]. This proves something is drawn in the box, not that the text is the right text."""
    from PIL import Image, ImageChops
    cfg = settings()["render"]
    k = cfg["dpi"] / 72.0
    rects = field_rects(filled_pdf)
    with tempfile.TemporaryDirectory() as d:
        a = _render(filled_pdf, os.path.join(d, "f"), cfg["dpi"])
        b = _render(base_pdf, os.path.join(d, "b"), cfg["dpi"])
        miss = []
        for n in names:
            if n not in rects:
                miss.append(n)
                continue
            pi, (x0, y0, x1, y1), h = rects[n]
            box = (int(x0 * k) + 2, int((h - y1) * k) + 2, max(int(x1 * k) - 2, int(x0 * k) + 4), max(int((h - y0) * k) - 2, int((h - y1) * k) + 4))
            ia = Image.open(a[pi]).convert("L").crop(box)
            ib = Image.open(b[pi]).convert("L").crop(box)
            diff = ImageChops.difference(ia, ib)
            changed = sum(1 for v in diff.getdata() if v > 40)
            if changed < cfg["min_changed_pixels"]:
                miss.append(n)
        return miss


def blanks(form, values):
    """The fields still empty that a hand-back lists (informational): every empty field except those not expected."""
    skip = {key_to_field(form, k) or k for k in (set(fspec(form)["not_expected"]) | set(fspec(form)["never"]))}
    return [n for n in fspec(form)["fields"] if n not in skip and not (values.get(n) or "").strip()]
