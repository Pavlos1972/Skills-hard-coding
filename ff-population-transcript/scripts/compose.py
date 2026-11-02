#!/usr/bin/env python3
"""Builds content.json (the one source for the PDF) from the form's data file, Claude's overlay and the standing rules.

  compose.py <run_dir>          write content.json

content.json is a pure function of: layout.json + form_read.json + overlay.json + crosscheck.json + claims.json + lead.json
(+ run.json, sources.json and the other spouse's form when there is one). verify.py composes it again and compares, so a
content.json edited by hand is caught. Every value carries its source (`src`); every difference carries both values.

Claude writes the OVERLAY (what the call and the documents add: gap fills, notes, flags, quote insurers, policy numbers ...),
never the form's values: those are copied by this program.
"""
import argparse
import os
import re
import sys
from decimal import Decimal

import ffform
import wrlib as w

YES = {"yes", "y", "true", "requested", "required", "1", "tick", "ticked", "x"}
NO = {"no", "n", "false", "none", "0", "nil"}
PENDING = "Pending – FNA"
ABBREV = {"mr", "mrs", "ms", "dr", "prof", "st", "no", "pty", "ltd", "vs", "etc", "approx", "ca", "incl", "est", "tel", "cell", "nr", "ave", "rd"}
OVERLAY_LISTS = ("fills", "rows_add", "notes", "flags", "diffs", "quotes", "policy_numbers", "abi_override", "documents_to_request",
                 "next_steps", "joint", "asked_paul")
KIND_ID = ("id",)


# ------------------------------------------------------------------ text -> one fact per line
def facts(text):
    """Split a value into one fact per line: newlines, bullets, semicolons and sentence ends (not inside amounts or after Mr./Dr.)."""
    t = str(text or "").replace("\r", "")
    out = []
    for chunk in re.split(r"\n+|\s*[•·▪]\s*|;\s+", t):
        chunk = re.sub(r"^\s*[-*–]\s+", "", chunk).strip()
        if not chunk:
            continue
        start = 0
        for m in re.finditer(r"\.\s+(?=[A-Z0-9])", chunk):
            before = re.findall(r"[A-Za-z]+$", chunk[:m.start()])
            if before and before[0].lower() in ABBREV:
                continue
            if chunk[start:m.start()].strip():
                out.append(chunk[start:m.start() + 1].strip())
            start = m.end()
        tail = chunk[start:].strip()
        if tail:
            out.append(tail)
    return out or []


def is_yes(v):
    return w.norm(v) in YES


def is_no(v):
    return w.norm(v) in NO


def prettify(col):
    return col.replace("_", " ").strip().capitalize()


def pct_equal(a, b):
    pa, pb = w.parse_pct(a), w.parse_pct(b)
    return pa is not None and pa == pb


# ------------------------------------------------------------------ overlay shape
def validate_overlay(ov):
    errs = []
    if not isinstance(ov, dict):
        return ["overlay.json must be an object"]
    seen = set()
    for name in OVERLAY_LISTS:
        v = ov.get(name, [])
        if not isinstance(v, list) or not all(isinstance(i, dict) for i in v):
            errs.append("overlay.%s must be a list of objects" % name)
            continue
        for it in v:
            iid = it.get("id")
            if not isinstance(iid, str) or not iid:
                errs.append("every entry of overlay.%s needs a plain-text `id`" % name)
            elif iid in seen:
                errs.append("overlay id %r is used twice" % iid)
            else:
                seen.add(iid)
            if "src" in it and not (isinstance(it["src"], list) and all(isinstance(s, dict) for s in it["src"])):
                errs.append("overlay %s: `src` must be a list like [{\"line\": 12, \"quote\": \"exact words\"}]" % iid)
    lk = ov.get("lookup")
    if lk is not None and not isinstance(lk, dict):
        errs.append("overlay.lookup must be an object")
    return errs


def overlay_items(ov):
    for name in OVERLAY_LISTS:
        for it in ov.get(name) or []:
            if isinstance(it, dict):
                yield name, it
    if isinstance(ov.get("lookup"), dict):
        yield "lookup", ov["lookup"]


# ------------------------------------------------------------------ the composer
class Ctx:
    def __init__(self, inp):
        self.lay = inp.get("layout") or w.layout()
        self.run = inp.get("run") or {}
        self.form = inp.get("form") or {"fields": {}, "lists": {}, "presets": [], "unknown_fields": [], "unknown_lists": [], "unknown_cols": {}, "mode": "none"}
        self.ov = inp.get("overlay") or {}
        self.cross = {i["key"]: i["answer"] for i in inp.get("cross") or [] if isinstance(i, dict) and isinstance(i.get("answer"), dict)}
        self.claims = inp.get("claims") or {}
        self.pdf_reviews = (inp.get("formpdf") or {}).get("reviews") or {}
        self.lead = inp.get("lead") or {}
        self.common = inp.get("common")
        self.meeting = w.parse_date(self.run.get("date")) or w.parse_date(self.form.get("date")) or dt_today()
        self.fills = {i["key"]: i for i in self.ov.get("fills") or [] if isinstance(i, dict) and i.get("key")}
        self.flags_all = []
        self.glance = []
        self.unsettled = []
        self.report = {"differences": [], "not_discussed": [], "requested": [], "presets": [], "filled": [], "standing": [], "derived": []}
        self.totals = {}
        self.rows_by_key = {}
        self.hidden = []
        self.rules = {}
        for r in self.lay["reconcile"]:
            self.rules.setdefault(r["target"], []).append(r)
        self.abi = {a["key"]: a for a in self.lay["standing"]["abi"]}
        self.abi_override = {i.get("key"): i for i in self.ov.get("abi_override") or [] if isinstance(i, dict)}
        self.quotes = [i for i in self.ov.get("quotes") or [] if isinstance(i, dict)]
        self.lists_eff = {}
        self._prepare_lists()

    # ---- raw access
    def fcell(self, key):
        c = self.form["fields"].get(key)
        return c if c and c.get("populated") else None

    def fv(self, key):
        c = self.fcell(key)
        return c["v"] if c else ""

    def eff(self, key):
        """The value in force for a field: the form's, else a gap fill from the call or a document."""
        v = self.fv(key)
        if v:
            return v
        f = self.fills.get(key)
        return f["value"].strip() if f and isinstance(f.get("value"), str) else ""

    def num(self, key, kind="money"):
        v = self.eff(key)
        return (w.parse_money(v) if kind == "money" else w.parse_pct(v)) if v else None

    # ---- lists (with the other spouse's common debts and children when this form has none)
    def _prepare_lists(self):
        lists = {k: [dict(r) for r in v] for k, v in self.form["lists"].items()}
        self.common_used = []
        if self.common:
            for name in ("debts", "kids"):
                other = (self.common.get("lists") or {}).get(name) or []
                if other and not lists.get(name):
                    lists[name] = [dict(r, index=i, common=True) for i, r in enumerate(other)]
                    self.common_used.append(name)
        for it in self.ov.get("rows_add") or []:
            if isinstance(it, dict) and it.get("list"):
                lst = lists.setdefault(it["list"], [])
                lst.append({"index": len(lst), "d": {c: str(v).strip() for c, v in (it.get("cells") or {}).items()}, "st": "filled", "added": it})
        self.lists_eff = lists
        for g in (g for s in self.lay["sections"] for g in s["groups"] if g.get("list") and g.get("totals")):
            for t in g["totals"]:
                tot, missing = sum_col(lists.get(g["list"], []), t["col"])
                self.totals[t["id"]] = tot
                self.totals[t["id"] + "_missing"] = missing

    # ---- flags
    def flag(self, row, text, kind, src=None):
        row["flags"].append({"text": text, "kind": kind, "src": src or []})
        self.flags_all.append((row["id"], kind, text))

    # ---- rows
    def row(self, rid, label, bullets, src, status="", kind="text", style=""):
        r = {"id": rid, "label": label, "bullets": bullets, "src": src, "status": status, "flags": [], "kind": kind}
        if style:
            r["style"] = style
        self.rows_by_key[rid] = r
        return r

    def bullets_for(self, text, kind):
        if kind in ("money", "pct", "id", "date", "int", "yn"):
            return [text] if text else []
        return facts(text)

    def settle(self, rid, label, kind, spec_terms=None, na=False):
        """A field with no value anywhere: N/A by rule, a claim recorded by `run.py claim`, or UNSETTLED (the checker fails it)."""
        if na:
            return self.row(rid, label, ["N/A"], [{"rule": "not_applicable"}], "na", kind)   # the gate question was answered No (or the person is single)
        cl = self.claims.get(rid)
        if cl:
            word = cl.get("as", "")
            if word == "Not discussed":
                self.report["not_discussed"].append((rid, label))
            elif word == "Requested":
                self.report["requested"].append((rid, label))
            return self.row(rid, label, [word], [{"claim": rid}], "claim", kind)
        self.unsettled.append(rid)
        return self.row(rid, label, ["UNSETTLED"], [], "unsettled", kind)

    def apply_cross(self, row, key, form_value):
        pr = self.pdf_reviews.get(key)
        if pr and pr.get("result") == "disagree":
            self.flag(row, "Difference: the form's data file says %s; the form's saved PDF says %s." % (form_value, pr.get("pdf_value")), "difference",
                      [{"formpdf": key, "quote": pr.get("quote", "")}])
            self.report["differences"].append({"key": key, "label": row["label"], "form": form_value, "other": str(pr.get("pdf_value")), "where": "the form's saved PDF"})
        a = self.cross.get(key)
        if not a:
            return
        r = a.get("r")
        if r in ("same", "differs") and a.get("quote"):
            row["src"].append({"line": a["line"], "quote": a["quote"]})
        if r == "differs":
            call = str(a.get("value") or "").strip()
            self.flag(row, "Difference: the form says %s; on the call: %s (line %s)." % (form_value, call, a.get("line")), "difference",
                      [{"line": a["line"], "quote": a["quote"]}])
            self.report["differences"].append({"key": key, "label": row["label"], "form": form_value, "other": call, "where": "the call, line %s" % a.get("line")})

    def apply_diffs(self, row, key, form_value):
        for d in self.ov.get("diffs") or []:
            if isinstance(d, dict) and d.get("key") == key:
                where = d.get("label") or "a document"
                self.flag(row, "Difference: the form says %s; %s says %s." % (form_value, where, d.get("other")), "difference", d.get("src") or [])
                self.report["differences"].append({"key": key, "label": row["label"], "form": form_value, "other": str(d.get("other")), "where": where})

    def apply_rules(self, row, key):
        for rule in self.rules.get(key, []):
            expected = self.expected(rule)
            shown = None
            if rule["kind"] == "money":
                shown = w.parse_money(" ".join(row["bullets"]))
            else:
                shown = w.parse_pct(" ".join(row["bullets"]))
            if expected is None:
                continue
            if shown is None:
                if not rule["assumed"] and row["status"] in ("claim", "unsettled"):
                    row["_expected"] = expected
                continue
            if shown == expected:
                continue
            fmt = w.fmt_money if rule["kind"] == "money" else w.fmt_pct
            if rule.get("never_exclude_debt") and shown < expected:
                txt = ("Check: debt repayments here (%s) are less than the monthly repayments of ALL the debts (%s). "
                       "Debt is never left out because of credit life: Paul decides." % (fmt(shown), fmt(expected)))
            else:
                txt = "Totals check: the form says %s; %s works out to %s." % (fmt(shown), rule["means"], fmt(expected))
            self.flag(row, txt, "reconcile", [{"total_of": rule["terms"]}])
            self.report["differences"].append({"key": key, "label": row["label"], "form": fmt(shown), "other": fmt(expected), "where": "recomputed: " + rule["means"]})
            if rule["assumed"]:
                self.glance.append("The check '%s' is my reading of the form (I could not read its labels): %s." % (rule["id"], rule["means"]))

    def expected(self, rule):
        vals = []
        for t in rule["terms"]:
            if t.startswith("@"):
                v = self.totals.get(t[1:])
            else:
                v = self.num(t, rule["kind"])
            vals.append(v)
        if rule["op"] == "sum":
            got = [v for v in vals if v is not None]
            return sum(got, Decimal(0)) if got else None
        if any(v is None for v in vals):
            return None
        if rule["op"] == "equals":
            return vals[0]
        if rule["op"] == "diff":
            return vals[0] - sum(vals[1:], Decimal(0))
        return None

    # ---- the field dispatcher
    def field(self, spec, na=False):
        key, label, kind = spec.get("key") or spec.get("const"), spec["label"], spec.get("kind", "text")
        special = spec.get("special")
        if spec.get("const") == "advisor":
            return self.row("advisor", label, [self.lay["advisor"]], [{"standing": "advisor"}], "standing", kind)
        if special == "abi":
            return self.abi_row(key, label, kind)
        form_v = self.fv(key) if spec.get("key") else ""
        cell = self.fcell(key) if spec.get("key") else None
        row = None
        if special == "aci":
            if form_v and form_v != "?":
                row = self.row(key, label, self.bullets_for(form_v, kind), [{"form": key}], cell["st"], kind)
            else:
                row = self.row(key, label, [PENDING], [{"rule": "aci_pending"}], "rule", kind)
        elif special == "ddcover":
            dflt = self.lay["standing"]["dd_cover"]["value"]
            if not form_v:
                row = self.row(key, label, [dflt], [{"standing": "dd_cover"}], "standing", kind)
            else:
                row = self.row(key, label, [form_v], [{"form": key}], cell["st"], kind)
                if w.parse_money(form_v) != w.parse_money(dflt):
                    self.flag(row, "This is not the standing default of %s: it is a deliberate entry in the form, shown as saved." % dflt, "standing", [{"form": key}])
        elif special == "lookup":
            row = self.lookup_row(key, label, kind, cell)
        elif special == "years":
            yr = ffform.years_from(form_v, self.meeting.year) if form_v else None
            if yr:
                row = self.row(key, label, ["%d years (since %d)" % yr], [{"derived": "years_from_year", "from": [key], "meeting_year": self.meeting.year}], "derived", kind)
                self.report["derived"].append("%s: the form holds the year %d; worked out as %d years" % (label, yr[1], yr[0]))
        elif special == "dob":
            row = self.dob_row(key, label, kind, cell)
        elif special == "gender":
            row = self.gender_row(key, label, kind, cell)
        elif special == "age":
            row = self.age_row(key, label, kind, cell)
        elif special == "referral":
            row = self.referral_row(key, label, kind, cell)
        elif special == "duty" and not form_v and key not in self.fills:
            pops = [self.num(k, "pct") for k in ("d_desk", "d_supo", "d_trav", "d_sups", "d_light", "d_mod", "d_heavy") if self.eff(k)]
            if pops and all(p is not None for p in pops) and sum(pops, Decimal(0)) == Decimal(100):
                row = self.row(key, label, ["0%"], [{"rule": "duties_remainder"}], "rule", kind)
        elif special == "duties_total":
            terms = [t for t in self.rules[key][0]["terms"]]
            comp = self.expected(self.rules[key][0])
            if comp is not None:
                row = self.row(key, label, [w.fmt_pct(comp)], [{"total_of": terms}], "derived", kind)
                if form_v and not pct_equal(form_v, w.fmt_pct(comp)):
                    self.flag(row, "Totals check: the form says %s; the percentages above add up to %s." % (form_v, w.fmt_pct(comp)), "reconcile", [{"form": key}])
                    self.report["differences"].append({"key": key, "label": label, "form": form_v, "other": w.fmt_pct(comp), "where": "recomputed from the duties split"})
        elif special == "disposable" and not form_v:
            comp = self.expected(self.rules[key][0])
            if comp is not None:
                row = self.row(key, label, [w.fmt_money(comp)], [{"total_of": self.rules[key][0]["terms"]}], "derived", kind)
        if row is None and form_v:
            row = self.row(key, label, self.bullets_for(form_v, kind), [{"form": key}], cell["st"], kind)
            if cell["st"] == "preset":
                row["preset"] = True
        if row is None and key in self.fills:
            row = self.fill_row(key, label, kind)
        if row is None and spec.get("optional") and not na:
            return None
        if row is None:
            row = self.settle(key, label, kind, spec.get("terms"), na=na)
        if form_v and any(s.get("form") == key for s in row["src"]):
            self.apply_cross(row, key, form_v)
            self.apply_diffs(row, key, form_v)
        if spec.get("key") and (special in (None, "calc", "disposable", "duties_total")):
            self.apply_rules(row, key)
        return row

    def fill_row(self, key, label, kind):
        f = self.fills[key]
        row = self.row(key, label, self.bullets_for(f["value"].strip(), kind), list(f.get("src") or []), "filled", kind)
        self.report["filled"].append((key, label))
        if kind == "id" and not f.get("confirmed") and not any("doc" in s for s in f.get("src") or []):
            self.flag(row, "Read out on the call and not yet confirmed: check it digit for digit.", "unclear", f.get("src") or [])
        return row

    # ---- special fields
    def abi_row(self, key, label, kind):
        std = self.abi[key]
        form_v = self.fv(key) if not std.get("added") else ""
        ov = self.abi_override.get(key)
        if ov:
            row = self.row(key, label, [str(ov["value"]).strip()], [{"paul": ov.get("paul_said", ""), "ref": ov.get("id")}], "paul", kind)
            self.flag(row, "Paul stated this ABI for this client: %s (the standing value is %s)." % (str(ov["value"]).strip(), std["value"]), "standing", [{"paul": ov.get("paul_said", "")}])
            self.report["standing"].append("%s: %s, as Paul stated" % (std["block"] + " / " + label, ov["value"]))
            return row
        row = self.row(key, label, [std["value"]], [{"standing": "abi:" + key}], "standing", kind)
        if std.get("added"):
            self.flag(row, "Added by the standing rule: the form has no Household needs ABI line.", "standing", [{"standing": "abi:" + key}])
            self.report["standing"].append("Permanent disability fractured: Household needs ABI %s added (the form has no line for it)" % std["value"])
        elif form_v and not pct_equal(form_v, std["value"]):
            self.flag(row, "The form has %s; the standing value %s is written." % (form_v, std["value"]), "standing", [{"form": key}])
            self.report["standing"].append("%s: the form had %s, the standing value %s is written" % (label, form_v, std["value"]))
        return row

    def lookup_row(self, key, label, kind, cell):
        lk = self.form.get("lookup") or {"verdict": "empty"}
        ov = self.ov.get("lookup") if isinstance(self.ov.get("lookup"), dict) else {}
        v = lk["verdict"]
        if v == "empty":
            if ov.get("text"):
                return self.row(key, label, facts(ov["text"]), list(ov.get("src") or []), "filled", kind)
            return None
        if v == "thrown_out":
            if ov.get("text"):
                row = self.row(key, label, facts(ov["text"]), list(ov.get("src") or []), "filled", kind)
                self.report["derived"].append("%s: the form's web look-up text was thrown out (%s); replaced from the call" % (label, "; ".join(lk["reasons"])))
            else:
                row = self.row(key, label, ["Not stated"], [{"rule": "lookup_not_stated"}], "rule", kind)
                self.glance.append("%s: the form's web look-up text was thrown out (%s) and the call does not say what the company does: shown as Not stated." % (label, "; ".join(lk["reasons"])))
            return row
        row = self.row(key, label, facts(cell["v"]), [{"form": key}], cell["st"], kind)
        if ov.get("client_confirmed") and ov.get("src"):
            row["src"] += list(ov["src"])
        else:
            row["bullets"].append("(web look-up, not confirmed with the client)")
            if cell["st"] == "confirmed":
                self.glance.append("The form marked the company look-up 'confirmed'. Tell the form's maker that its look-up should say 'to verify', never 'confirmed'.")
        return row

    def id_info(self):
        idno = self.eff("idno")
        if not idno or (self.eff("idtype") and "passport" in w.norm(self.eff("idtype"))):
            return None
        age = self.eff("age")
        hint = int(age) if age.isdigit() else None
        return ffform.id_facts(idno, self.meeting, hint)

    def dob_row(self, key, label, kind, cell):
        info = self.id_info()
        form_v = self.fv(key)
        if form_v:
            row = self.row(key, label, [form_v], [{"form": key}], cell["st"], kind)
            if info and info["dob"] and w.parse_date(form_v) and w.parse_date(form_v) != info["dob"]:
                self.flag(row, "Difference: the form says %s; the ID number gives %s." % (form_v, info["dob"].strftime("%d/%m/%Y")), "difference", [{"derived": "dob_from_id", "from": ["idno"]}])
                self.report["differences"].append({"key": key, "label": label, "form": form_v, "other": info["dob"].strftime("%d/%m/%Y"), "where": "the ID number"})
            return row
        if key in self.fills:
            return None
        if info and info["dob"]:
            d = info["dob"].strftime("%d/%m/%Y")
            row = self.row(key, label, ["%s (worked out from the ID number)" % d], [{"derived": "dob_from_id", "from": ["idno"]}], "derived", kind)
            self.report["derived"].append("Date of birth worked out from the ID number")
            for p in info["problems"]:
                self.flag(row, "ID number: " + p + ".", "unclear", [{"form": "idno"}])
            return row
        return None

    def gender_row(self, key, label, kind, cell):
        info = self.id_info()
        form_v = self.fv(key)
        if form_v:
            row = self.row(key, label, [form_v], [{"form": key}], cell["st"], kind)
            if info and info["gender"] and w.norm(form_v) not in (w.norm(info["gender"]), w.norm(info["gender"])[:1]):
                self.flag(row, "Difference: the form says %s; the ID number gives %s." % (form_v, info["gender"]), "difference", [{"derived": "gender_from_id", "from": ["idno"]}])
                self.report["differences"].append({"key": key, "label": label, "form": form_v, "other": info["gender"], "where": "the ID number"})
            return row
        if key in self.fills:
            return None
        if info and info["gender"]:
            self.report["derived"].append("Gender worked out from the ID number")
            return self.row(key, label, ["%s (worked out from the ID number)" % info["gender"]], [{"derived": "gender_from_id", "from": ["idno"]}], "derived", kind)
        return None

    def age_row(self, key, label, kind, cell):
        form_v = self.fv(key)
        if form_v:
            return self.row(key, label, [form_v], [{"form": key}], cell["st"], kind)
        if key in self.fills:
            return None
        d = w.parse_date(self.eff("dob"))
        if not d:
            info = self.id_info()
            d = info["dob"] if info and info["dob"] else None
        if d:
            return self.row(key, label, [str(ffform.age_on(d, self.meeting))], [{"derived": "age_from_dob", "from": ["dob"], "on": self.meeting.strftime("%d/%m/%Y")}], "derived", kind)
        return None

    def referral_row(self, key, label, kind, cell):
        form_v = self.fv(key)
        if self.lead.get("found") and w.parse_date(self.lead.get("received")):
            val = "D&R Marketing lead - %s" % self.lead["received"]
            row = self.row(key, label, [val], [{"doc": "Correspondence", "ref": self.lead.get("ref", ""), "quote": self.lead.get("quote", "")}], "lead", kind)
            if form_v and "d&r" not in w.norm(form_v).replace(" and ", " & "):
                self.flag(row, "The form says %s; a D&R Marketing appointment email was found, so the lead source is D&R Marketing." % form_v, "difference", [{"form": key}])
            return row
        if form_v:
            return self.row(key, label, facts(form_v), [{"form": key}], cell["st"], kind)
        if key in self.fills:
            return None
        if self.lead.get("searched"):
            return self.row(key, label, ["Referral - referrer not stated (please confirm)"], [{"rule": "lead_default"}], "rule", kind)
        return None

    # ---- groups and lists
    def cond(self, c):
        if not c:
            return True
        return w.norm(self.eff(c["key"])) in [w.norm(x) for x in c["in"]]

    def group_rows(self, g):
        na_keys = set(g.get("na_keys") or []) if self.cond(g.get("na_when")) and g.get("na_when") else set()
        gate = g.get("gate")
        gated_off = bool(gate) and is_no(self.eff(gate))
        rows = []
        for spec in g["rows"]:
            if gated_off and spec.get("key") != gate and not spec.get("notes"):
                na_keys.add(spec.get("key"))
            if spec.get("needs") and is_no(self.eff(spec["needs"])):
                na_keys.add(spec.get("key"))
            if spec.get("notes"):
                v = self.fv(spec["key"])
                if v:
                    r = self.row(spec["key"], spec["label"], facts(v), [{"form": spec["key"]}], self.fcell(spec["key"])["st"])
                    self.apply_cross(r, spec["key"], v)
                    rows.append(r)
                elif spec["key"] in self.fills:
                    rows.append(self.fill_row(spec["key"], spec["label"], "text"))
                continue
            rows.append(self.field(spec, na=spec.get("key") in na_keys))
        return rows

    def group_block(self, g):
        if not self.cond(g.get("when")):
            pop = [r["key"] for r in g["rows"] if r.get("key") and self.fcell(r["key"])]
            if pop:
                self.hidden.append((g["sub"], pop))
                self.glance.append("%s: the form holds values (%s) but the rule says to fill this part only when Business owner is Yes. Not printed." % (g["sub"], ", ".join(pop)))
            return None
        rows = self.group_rows(g)
        rows = [r for r in rows if r]
        return {"kind": "fields", "sub": g["sub"], "rows": rows} if rows else None

    def list_blocks(self, g):
        name = g["list"]
        if not self.cond(g.get("when")):
            if self.lists_eff.get(name):
                self.hidden.append((g["sub"], [name]))
                self.glance.append("%s: the form holds rows but Business owner is not Yes. Not printed." % g["sub"])
            return []
        rows = self.lists_eff.get(name, [])
        blocks = []
        has_key = {"debts": "has_debts", "kids": "has_kids", "risk": "has_risk", "ret_ra": "has_ra", "ret_pp": "has_pp", "inv": "has_inv", "grp": "has_group"}.get(name)
        if not rows and g.get("optional"):
            return []
        if not rows:
            rid = "list." + name
            if has_key and is_no(self.eff(has_key)):
                r = self.row(rid, g["sub"], ["None (the form says: %s)" % self.eff(has_key)], [{"form": has_key}], "form", "text")
            else:
                r = self.settle(rid, g["sub"], "text")
            return [{"kind": "fields", "sub": g["sub"], "rows": [r]}]
        cols = g["cols"]
        if cols == "generic":
            seen = []
            for row in rows:
                for c in row["d"]:
                    if c not in seen:
                        seen.append(c)
            cols = [{"col": c, "label": prettify(c)} for c in seen]
        known_cols = {c["col"] for c in cols}
        for row in rows:
            i = row["index"]
            item_rows = []
            for c in cols:
                rid = "%s.%d.%s" % (name, i, c["col"])
                v = row["d"].get(c["col"], "")
                kind = c.get("kind", "text")
                if v:
                    r = self.row(rid, c["label"], self.bullets_for(v, kind), [{"form": "%s.%d.%s" % (name, i, c["col"])}] if not row.get("added") else list(row["added"].get("src") or []), row["st"], kind)
                    if row.get("common"):
                        r["src"] = [{"form": "%s.%d.%s" % (name, i, c["col"]), "from_spouse": True}]
                    self.apply_cross(r, "%s.%d.%s" % (name, i, c["col"]), v)
                    self.apply_diffs(r, "%s.%d.%s" % (name, i, c["col"]), v)
                elif rid in self.fills:
                    r = self.fill_row(rid, c["label"], kind)
                elif c["col"] == "notes":
                    continue
                else:
                    r = self.settle(rid, c["label"], kind)
                item_rows.append(r)
            for c, v in row["d"].items():
                if c not in known_cols and v:
                    item_rows.append(self.row("%s.%d.%s" % (name, i, c), prettify(c), facts(v), [{"form": "%s.%d.%s" % (name, i, c)}], row["st"]))
            for j in self.ov.get("joint") or []:
                if isinstance(j, dict) and j.get("list") == name and j.get("index") == i:
                    item_rows.append(self.row("joint.%s.%d" % (name, i), "Joint policy", ["Joint policy with %s" % j.get("with")], list(j.get("src") or []), "filled"))
            if row.get("common"):
                self.flag(item_rows[0], "Common to both spouses: taken from the other spouse's form.", "common", [{"form": "%s.%d" % (name, i), "from_spouse": True}])
            blocks.append({"kind": "item", "sub": "%s %d" % (g["item"], i + 1), "list": name, "index": i, "rows": item_rows})
        if g.get("totals"):
            trows = []
            for t in g["totals"]:
                comps = ["%s.%d.%s" % (name, r["index"], t["col"]) for r in rows]
                tr = self.row("total." + t["id"], t["label"], [w.fmt_money(self.totals[t["id"]])], [{"total_of": comps}], "derived", "money")
                miss = self.totals[t["id"] + "_missing"]
                if miss:
                    self.flag(tr, "%d item(s) have no amount yet, so this total is not complete; none is left out on purpose." % miss, "reconcile", [{"total_of": comps}])
                trows.append(tr)
            blocks.append({"kind": "fields", "sub": "Totals", "rows": trows})
        return blocks

    def quote_rows(self):
        """For every quote request: the insurer and New Business or Servicing, from the form or from what was said/Paul decided (never a default)."""
        out = []
        for qg in self.lay["quote_groups"]:
            if qg.get("list"):
                for row in self.lists_eff.get(qg["list"], []):
                    if any(row["d"].values()) and not is_no(row["d"].get(qg["req"], "")):
                        out.append(self.quote_row(qg, row["index"], row["d"].get(qg["req"], ""), row["d"].get(qg["type"], ""), ""))
            elif is_yes(self.eff(qg["req"])):
                out.append(self.quote_row(qg, None, self.eff(qg["req"]), self.eff(qg["type"]), self.eff(qg["ins"]) if qg.get("ins") else ""))
        return out

    def quote_row(self, qg, idx, req, mode_form, ins_form):
        title = qg["title"] + ("" if idx is None else " %d" % (idx + 1))
        rid = "quote.%s%s" % (qg["id"], "" if idx is None else ".%d" % idx)
        ov = next((q for q in self.quotes if q.get("group") == qg["id"] and q.get("row") in (None, idx)), None)
        ins, mode, srcs = ins_form, "", []
        if ins_form:
            srcs.append({"form": qg["ins"]})
        if mode_form and any(m in w.norm(mode_form) for m in w.MODE_WORDS):
            mode = "New Business" if "new business" in w.norm(mode_form) else "Servicing"
            srcs.append({"form": qg["type"] if idx is None else "%s.%d.%s" % (qg["list"], idx, qg["type"])})
        if ov:
            if not ins and ov.get("insurer"):
                ins = str(ov["insurer"]).strip()
            if not mode and ov.get("mode"):
                mode = str(ov["mode"]).strip()
            srcs += list(ov.get("src") or [])
        bullets = ["Insurer: %s" % ins if ins else "Insurer: NOT KNOWN", "Basis: %s" % mode if mode else "Basis: NOT KNOWN"]
        r = self.row(rid, title + ": insurer and basis", bullets, srcs, "quote" if ins and mode else "unsettled", "text")
        if not (ins and mode):
            self.unsettled.append(rid)
        return r

    # ---- whole document
    def build(self):
        sections = []
        for sec in self.lay["sections"]:
            blocks = []
            for g in sec["groups"]:
                if g.get("overlay") == "documents_to_request":
                    items = [i for i in self.ov.get("documents_to_request") or [] if isinstance(i, dict)]
                    if items:
                        r = self.row("docs_to_request", "To request from the client", [i["text"].strip() for i in items], [s for i in items for s in (i.get("src") or [])], "filled")
                        blocks.append({"kind": "fields", "sub": g["sub"], "rows": [r]})
                    continue
                if g.get("list"):
                    blocks += self.list_blocks(g)
                else:
                    b = self.group_block(g)
                    if b:
                        blocks.append(b)
            if sec["id"] == "advisor":
                qr = self.quote_rows()
                if qr:
                    blocks.append({"kind": "fields", "sub": "Quote requests: insurer and basis", "rows": qr})
            extra = self.section_extras(sec["id"])
            if extra:
                blocks.append({"kind": "fields", "sub": "Added from the call and documents", "rows": extra})
            sections.append({"id": sec["id"], "num": sec["num"], "title": sec["title"], "blocks": blocks})
        closing_rows = [self.field(spec) for spec in self.lay["closing"]["rows"]]
        ns = [i for i in self.ov.get("next_steps") or [] if isinstance(i, dict)]
        if ns:
            closing_rows.append(self.row("next_steps", "Next steps for the client", [i["text"].strip() for i in ns], [s for i in ns for s in (i.get("src") or [])], "filled"))
        extra = self.section_extras("next")
        closing = {"title": self.lay["closing"]["title"], "rows": closing_rows + extra}
        self.policy_numbers([r for s in sections for b in s["blocks"] for r in b["rows"]] + closing["rows"])
        other = self.other_fields()
        content = {
            "skill": w.skill_name(), "client": {"first": self.form.get("client", {}).get("first") or (self.run.get("client") or {}).get("first", ""),
                                                  "surname": self.form.get("client", {}).get("surname") or (self.run.get("client") or {}).get("surname", "")},
            "meeting_date": self.form.get("date") or self.run.get("date", ""),
            "form": {"mode": self.form.get("mode", "form"), "file": self.form.get("file"), "sha256": self.form.get("sha256"), "schema": self.form.get("schema"),
                     "modified": self.form.get("modified")},
            "sections": sections, "closing": closing, "other_fields": other, "unsettled": sorted(set(self.unsettled)),
            "spouse": self.run.get("spouse"), "common_used": self.common_used,
        }
        names = w.output_names(content["client"]["first"], content["client"]["surname"], content["meeting_date"])
        content["file_name"] = names["pdf"] if names else None
        content["report"] = self.make_report()
        content["glance"] = self.make_glance(other)
        return content

    def section_extras(self, sid):
        rows = []
        notes = [n for n in self.ov.get("notes") or [] if isinstance(n, dict) and n.get("section") == sid]
        if notes:
            rows.append(self.row("notes." + sid, "Notes", [n["text"].strip() for n in notes], [s for n in notes for s in (n.get("src") or [])], "filled", "text", "added"))
        for f in self.ov.get("flags") or []:
            if isinstance(f, dict) and f.get("section") == sid:
                r = self.row("flag." + f["id"], "Flag", [f["text"].strip()], list(f.get("src") or []), "flag", "text", "flag")
                self.flags_all.append((r["id"], "check", f["text"]))
                rows.append(r)
        return rows

    def policy_numbers(self, rows):
        for pn in self.ov.get("policy_numbers") or []:
            if not isinstance(pn, dict):
                continue
            found, resolved = str(pn.get("found", "")), str(pn.get("resolved", ""))
            hit = False
            for r in rows:
                if any(found and found in b for b in r["bullets"]):
                    hit = True
                    r["bullets"] = [b.replace(found, resolved) for b in r["bullets"]]
                    r["src"].append({"doc": "Policy schedule", "ref": pn.get("ref", ""), "quote": pn.get("quote", "")})
                    if found != resolved:
                        self.flag(r, "Policy number: the form or Overview says %s; the policy schedule says %s (the schedule is the source of truth)." % (found, resolved), "policy",
                                  [{"doc": "Policy schedule", "ref": pn.get("ref", ""), "quote": pn.get("quote", "")}])
                        self.report["differences"].append({"key": r["id"], "label": r["label"], "form": found, "other": resolved, "where": "the policy schedule"})
            pn["_used"] = hit

    def other_fields(self):
        rows = []
        for k in self.form.get("unknown_fields") or []:
            c = self.form["fields"][k]
            rows.append(self.row("other." + k, k, facts(c["v"]), [{"form": k}], c["st"]))
        for name in self.form.get("unknown_lists") or []:
            for row in self.form["lists"].get(name, []):
                for c, v in row["d"].items():
                    if v:
                        rows.append(self.row("other.%s.%d.%s" % (name, row["index"], c), "%s row %d: %s" % (name, row["index"] + 1, c), facts(v), [{"form": "%s.%d.%s" % (name, row["index"], c)}], row["st"]))
        for name, cs in (self.form.get("unknown_cols") or {}).items():
            if name in (self.form.get("unknown_lists") or []):
                continue
            for row in self.form["lists"].get(name, []):
                for c in cs:
                    v = row["d"].get(c, "")
                    if v:
                        rows.append(self.row("other.%s.%d.%s" % (name, row["index"], c), "%s row %d: %s" % (name, row["index"] + 1, c), facts(v), [{"form": "%s.%d.%s" % (name, row["index"], c)}], row["st"]))
        return rows

    def make_report(self):
        pre = []
        for k in self.form.get("presets") or []:
            a = self.cross.get(k)
            row = self.rows_by_key.get(k)
            if row is not None and row.get("status") == "standing":
                done = "replaced by the standing rule"
            elif a and a.get("r") == "differs":
                done = "kept and flagged: the call differs (line %s)" % a.get("line")
            elif a and a.get("r") == "same":
                done = "kept: the call agrees (line %s)" % a.get("line")
            else:
                done = "kept: not mentioned on the call"
            pre.append({"key": k, "label": row["label"] if row else k, "done": done})
        r = dict(self.report)
        r["presets"] = pre
        r["statuses"] = self.form.get("statuses") or {}
        r["form_file"] = self.form.get("file")
        return r

    def make_glance(self, other):
        g = list(dict.fromkeys(self.glance))
        if other:
            g.append("The form holds %d value(s) the layout has no place for (printed under 'Other fields from the form'): %s." % (len(other), ", ".join(r["label"] for r in other[:8])))
        if self.form.get("other_statuses"):
            g.append("Older-style statuses (heard or verify) in the file: %s." % ", ".join(self.form["other_statuses"]))
        if self.form.get("odd"):
            g.append("Odd entries in the form's file: %s." % "; ".join(self.form["odd"][:5]))
        if self.form.get("top_unknown"):
            g.append("The form's file has top-level keys this skill does not know: %s." % ", ".join(self.form["top_unknown"]))
        nd = ["%s (%s)" % (lbl, rid) for rid, lbl in self.report["not_discussed"]]
        if nd:
            g.append("Left as Not discussed after a search of the call and the documents: %s." % ", ".join(nd[:12]) + (" ..." if len(nd) > 12 else ""))
        rq = ["%s (%s)" % (lbl, rid) for rid, lbl in self.report["requested"]]
        if rq:
            g.append("Marked Requested (missing after the search): %s." % ", ".join(rq[:12]))
        if self.common_used:
            g.append("Taken from the other spouse's form because this form has none: %s." % ", ".join(self.common_used))
        if not self.lay.get("labels_checked"):
            g.append("The field labels were written by this skill (the form's own label file could not be read): check them on this PDF.")
        return list(dict.fromkeys(g))


def sum_col(rows, col):
    total, missing = Decimal(0), 0
    for r in rows:
        v = w.parse_money(r["d"].get(col, ""))
        if v is None:
            missing += 1
        else:
            total += v
    return total, missing


def dt_today():
    import datetime as dt
    return dt.date.today()


def compose(inp):
    return Ctx(inp).build()


def load_inputs(run):
    j = lambda name, default: w.load_opt(os.path.join(run, name), default)  # noqa: E731
    rj = j(w.RUN, {})
    form = j(w.FORM, None) or {"fields": {}, "lists": {}, "presets": [], "unknown_fields": [], "unknown_lists": [], "unknown_cols": {}, "mode": rj.get("form_mode", "none"),
                               "client": rj.get("client", {}), "date": rj.get("date", ""), "lookup": {"verdict": "empty"}, "statuses": {}}
    form.setdefault("mode", rj.get("form_mode", "form"))
    common = None
    sp = rj.get("spouse") or {}
    if sp.get("run") and os.path.exists(os.path.join(sp["run"], w.FORM)):
        common = w.load_json(os.path.join(sp["run"], w.FORM))
    return {"layout": w.layout(), "run": rj, "form": form, "overlay": j(w.OVERLAY, {}), "cross": j(w.CROSS, []), "claims": j(w.CLAIMS, {}), "lead": j(w.LEAD, {}), "common": common, "formpdf": j(w.FORMPDF, {})}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    a = ap.parse_args()
    run = os.path.abspath(a.run)
    inp = load_inputs(run)
    errs = validate_overlay(inp["overlay"])
    if errs:
        print("COMPOSE REFUSED. overlay.json has the wrong shape:")
        for e in errs:
            print("  - " + e)
        sys.exit(1)
    content = compose(inp)
    w.save_json(os.path.join(run, w.CONTENT), content)
    n = sum(len(b["rows"]) for s in content["sections"] for b in s["blocks"])
    print("COMPOSED content.json: %d sections, %d rows, %d flags, %d unsettled" % (len(content["sections"]), n, sum(len(r["flags"]) for s in content["sections"] for b in s["blocks"] for r in b["rows"]), len(content["unsettled"])))
    if content["unsettled"]:
        print("  UNSETTLED (empty, and not N/A, not filled, not claimed): " + ", ".join(content["unsettled"][:40]))
        print("  Settle them: run.py claim (searches the call and the documents), or add a fill to overlay.json with its source.")
    if content["glance"]:
        print("  WHAT PAUL SHOULD GLANCE AT SO FAR:")
        for g in content["glance"]:
            print("   - " + g)


if __name__ == "__main__":
    main()
