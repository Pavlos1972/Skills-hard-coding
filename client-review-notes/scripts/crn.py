"""The model of the client-review-notes: the Client Record as ONE data file, the rules on it, the proof against the raw notes and the Markdown it is drawn as.
No client data is kept in this file. What it proves: the 18 fields and their order, the layout, that every verbatim item is character for character in the raw
notes, that every date, amount, percentage, number, contract-like code, email, link, name and abbreviation of each raw entry is in the record (or listed as
left out with a reason), the do-not-contact lines, the flags it can find, the glossary rule, the duplicate decision. What it cannot prove: that a sentence keeps
its MEANING, that the notes are complete or right.
"""
import json
import os
import re

import notes as N
import wrlib as w

ASSETS = os.path.join(w.SKILL_DIR, "assets")


def settings():
    return w.load_json(os.path.join(ASSETS, "settings.json"))


def _w(*a):
    return settings()["warn"]


def _html(s):
    return re.search(r"</?[A-Za-z][^>]*>", str(s)) is not None


def nrm(s):
    return w.norm(s)


def appears(value, raw):
    """A verbatim item appears in the raw notes (letters and digits only, case ignored)."""
    a, b = re.sub(r"[^0-9a-z]", "", str(value).lower()), re.sub(r"[^0-9a-z]", "", raw.lower())
    return bool(a) and a in b


def strings(o):
    """Every string value of a nested record structure (not the keys)."""
    if isinstance(o, str):
        return [o]
    if isinstance(o, dict):
        return [s for v in o.values() for s in strings(v)]
    if isinstance(o, (list, tuple)):
        return [s for v in o for s in strings(v)]
    return []


def mask_text(s):
    """In the audit and the block for Paul, digit runs of 8 or more (ID, account and contract numbers) show only their last four digits."""
    def rep(m):
        ds = w.digits(m.group(0))
        return "\u2022\u2022\u2022" + ds[-4:] if len(ds) >= 8 else m.group(0)
    return re.sub(r"\d[\d \-]{6,}\d", rep, str(s))


def as_lines(v):
    if v is None:
        return []
    if isinstance(v, str):
        return [v] if v.strip() else []
    return [str(x) for x in v if str(x).strip()]


def not_rec():
    return settings()["not_recorded"]


# ------------------------------------------------------------------ the record: checks
def check(record, raw, entries, recognised, dups, decision):
    """Returns dict(problems [str], flags [str], left_out [(token, reason)], dnc [str], merged bool). Nothing is invented: the flags come from the raw notes."""
    S = settings()
    P = []
    out = {"problems": P, "flags": [], "left_out": [], "dnc": []}
    rec = record or {}
    fields = rec.get("fields") or {}
    for k in fields:
        if k not in S["fields"]:
            P.append("'%s' is not one of the 18 fields (%s)" % (k, ", ".join(S["fields"])))
    # ---- the simple fields: verbatim in the raw notes
    for k in S["simple_fields"]:
        v = fields.get(k)
        if v in (None, "") or str(v).strip().rstrip(".").lower() == "not recorded":
            continue
        v = str(v).strip()
        if _html(v):
            P.append("%s: HTML is not allowed" % k)
        elif k in S["must_appear"] and not appears(v, raw):
            P.append("%s: '%s' is not in the raw notes (a field is reproduced exactly as the source gives it; if the source does not say, leave it out and it reads %s)" % (k, v, not_rec()))
    idv = str(fields.get("Client ID No") or "").strip()
    if idv and re.search(r"[A-Za-z\-]", idv):
        out["flags"].append("the Client ID No (%s) has letters or hyphens: it may be a policy or contract number, not an ID" % idv)
    elif idv and len(w.digits(idv)) != 13:
        out["flags"].append("the Client ID No has %d digits, not 13: possibly truncated or imprecise" % len(w.digits(idv)))
    elif idv and not N.id_check(w.digits(idv)):
        out["flags"].append("the Client ID No fails its check digit: possibly mistyped")
    for k in S["free_fields"] + S["list_fields"]:
        for ln in as_lines(fields.get(k)):
            if _html(ln):
                P.append("%s: HTML is not allowed" % k)
    # ---- Life & Investments
    li = fields.get("Life & Investments") or {}
    for g, _label in S["policy_groups"]:
        for i, pol in enumerate(li.get(g) or [], 1):
            who = "Life & Investments, %s policy %d" % (g, i)
            if not isinstance(pol, dict) or not all(str(pol.get(x) or "").strip() for x in ("contract", "product", "doc")):
                P.append("%s: contract, product and doc are needed" % who)
                continue
            for part in ("contract", "product", "doc", "premium", "status"):
                if str(pol.get(part) or "").strip() and not appears(pol[part], raw):
                    P.append("%s: %s '%s' is not in the raw notes (reproduced verbatim, never cleaned up)" % (who, part, pol[part]))
                if _html(pol.get(part) or ""):
                    P.append("%s: HTML is not allowed" % who)
    # ---- Commission
    for i, c in enumerate(fields.get("Commission") or [], 1):
        who = "Commission entry %d" % i
        if not isinstance(c, dict) or not re.fullmatch(r".+ – .+ \(.+\)", str(c.get("title") or "")):
            P.append("%s: the title must read `Insurer – Product Description (Month 'YY)`" % who)
            continue
        if not as_lines(c.get("lines")):
            P.append("%s: no lines" % who)
        for ln in as_lines(c.get("lines")) + [c["title"]]:
            if not appears(ln, raw):
                P.append("%s: '%s' is not in the raw notes (commission is reproduced verbatim)" % (who, ln))
    # ---- Notes blocks
    blocks = (rec.get("notes") or {}).get("blocks") or []
    by_n = {e["n"]: e for e in entries}
    keys = []
    all_keys = {k for _s, _e, k, _p in N.find_dates(raw)}
    for i, b in enumerate(blocks, 1):
        who = "Notes block %d" % i
        frm = b.get("from") or []
        if not frm or any(n not in by_n for n in frm):
            P.append("%s: 'from' must list entry numbers of the raw notes (1 to %d)" % (who, max(by_n)))
            continue
        key = b.get("date")
        ekeys = [by_n[n]["key"] for n in frm if by_n[n]["key"]]
        if key is None:
            key = ekeys[0] if ekeys else None
        elif recognised and ekeys and key not in ekeys:
            P.append("%s: the date %s is not the date of entry %s (%s)" % (who, key, frm, ", ".join(ekeys)))
        elif not recognised and key not in all_keys:
            P.append("%s: the date %s is not a date in the raw notes" % (who, key))
        keys.append(key)
        bl = as_lines(b.get("bullets"))
        if not bl:
            P.append("%s: no bullets" % who)
        for ln in bl:
            if _html(ln):
                P.append("%s: HTML is not allowed (no underline tags either)" % who)
            for u in re.findall(r"https?://[^\s)\]>]+", ln):
                if "planner" in u.lower() and not re.search(r"\[Planner – [^\]]+\]\(%s\)" % re.escape(u.rstrip(".,;")), ln):
                    P.append("%s: a Planner link must read `[Planner – Task Name](URL)`" % who)
    dated = [k for k in keys if k]
    if dated != sorted(dated):
        P.append("Notes: the blocks must run in date order, oldest first")
    # ---- do-not-contact lines: found by phrase search in the raw notes
    dnc = [ln.strip() for ln in raw.split("\n") if any(ph in ln.lower() for ph in S["do_not_contact"])]
    out["dnc"] = dnc
    bullets_all = nrm(" ".join(x for b in blocks for x in as_lines(b.get("bullets"))))
    for ln in dnc:
        segs = [s for s in re.split(r"(?<=[.!?])\s+", ln) if any(ph in s.lower() for ph in S["do_not_contact"])]
        if not all(nrm(s) in bullets_all for s in segs):
            P.append("a 'do not contact' line is in the raw notes but not reproduced in full in the Notes bullets: \"%s\"" % ln[:80])
    # ---- coverage: everything each raw entry holds must be kept
    left = {str(k): str(v).strip() for k, v in (rec.get("left_out") or {}).items()}
    for k, v in left.items():
        if len(v) < 5:
            P.append("left_out '%s' needs a reason" % k)
    drawn = " ".join(S["fields"]) + " Previous Replaced Policies Current Active Non-active Lapsed Contract DOC Not recorded Merged record"
    struct = "x ; " + " ; ".join(strings(fields)) + " ; " + drawn
    stop = S["name_stop"]
    miss_all = []
    for e in entries:
        scope = struct + "\n" + "\n".join(x for b in blocks if e["n"] in (b.get("from") or []) for x in as_lines(b.get("bullets")))
        need, have = N.tokens(e["text"], stop), N.tokens(scope, stop)
        if e["key"] and any(e["n"] in (b.get("from") or []) for b in blocks):
            need["date"].discard(e["key"])                      # the entry's own date is the block's heading, drawn by the program
        for kind in need:
            for tok in sorted(need[kind] - have[kind]):
                key = "%s: %s" % (kind, tok)
                if not any(key.lower() == k.lower() or tok.lower() == k.lower() or k.lower() in key.lower() for k in left):
                    miss_all.append((e["n"], key))
    for n, key in miss_all[:25]:
        P.append("entry %d: %s is in the raw notes but not in the record (keep it, or list it in left_out with a reason)" % (n, key))
    if len(miss_all) > 25:
        P.append("... and %d more tokens not covered" % (len(miss_all) - 25))
    out["left_out"] = sorted(left.items())
    # ---- the glossary: abbreviations are reproduced as given, never expanded
    text_all = struct + " ".join(x for b in blocks for x in as_lines(b.get("bullets")))
    for ab, ex in S["glossary"].items():
        if re.search(re.escape(ex), text_all, re.I) and not re.search(re.escape(ex), raw, re.I):
            P.append("the record expands %s to '%s'; abbreviations are reproduced as given" % (ab, ex))
    # ---- flags found in the raw notes (shown by the program at the top of Notes)
    out["flags"] += N.raw_flags(raw, entries, recognised, S["system_stamp_repeats"])
    # ---- duplicates: the program found earlier records of the same client (engine); Paul decided
    out["merged"] = decision == "merge"
    if out["merged"] and not as_lines(rec.get("merge_notes")):
        P.append("a merged record needs merge_notes: what each earlier version added")
    elif not out["merged"] and as_lines(rec.get("merge_notes")):
        P.append("merge_notes were entered but Paul did not decide to merge")
    return out


# ------------------------------------------------------------------ the Markdown
def heading_text(key, months):
    return N.heading(key, months) if key else "UNDATED NOTES"


def render(record, raw, entries, chk):
    """The Client Record as Markdown, always in this layout: a header line, then the 18 fields each with a bold label and its value on the line below,
    a horizontal rule between every section, Notes under BOLD ALL CAPS date headings (oldest first), no sign-off."""
    S = settings()
    NR = S["not_recorded"]
    f = (record or {}).get("fields") or {}
    ws = S["warn"]

    def val(k):
        v = f.get(k)
        return NR if v in (None, "") or str(v).strip().rstrip(".").lower() == "not recorded" else str(v).strip()
    first, last, known, cat, idn = val("First Name"), val("Last Name"), val("Known As"), val("Categories"), val("Client ID No")
    name = first + (" (%s)" % known if known != NR else "") + " " + last
    parts = ["%s (%s) (%s)\n" % (name, cat, idn)]
    for k in S["fields"]:
        if k in S["simple_fields"]:
            body = val(k)
            idflag = next((x for x in chk["flags"] if x.startswith("the Client ID No")), None)
            if k == "Client ID No" and idflag:
                body += " %s %s" % (ws, idflag)
            parts.append("**%s:**\n%s\n" % (k, body))
        elif k in S["free_fields"] or k in S["list_fields"]:
            ls = as_lines(f.get(k))
            if not ls:
                body = ("- " + NR) if k in S["list_fields"] else NR
            elif k in S["list_fields"] or len(ls) > 1:
                body = "\n".join("- " + x for x in ls)
            else:
                body = ls[0]
            parts.append("**%s:**\n%s\n" % (k, body))
        elif k == "Life & Investments":
            li = f.get(k) or {}
            groups = []
            for g, label in S["policy_groups"]:
                rows = []
                for p in li.get(g) or []:
                    line = "- Contract: %s (%s) DOC %s" % (str(p["contract"]).strip(), str(p["product"]).strip(), str(p["doc"]).strip())
                    if str(p.get("premium") or "").strip():
                        line += " / " + str(p["premium"]).strip()
                    if str(p.get("status") or "").strip():
                        line += " / " + str(p["status"]).strip()
                    if str(p.get("flag") or "").strip():
                        line += " %s %s" % (ws, str(p["flag"]).strip())
                    rows.append(line)
                groups.append("*%s*\n%s" % (label, "\n".join(rows) if rows else "- " + NR))
            parts.append("**%s:**\n\n%s\n" % (k, "\n\n".join(groups)))
        elif k == "Notes":
            warn = ['%s DO NOT CONTACT: "%s"' % (ws, ln) for ln in chk["dnc"]]
            warn += ["%s %s" % (ws, ln) for ln in chk["flags"] if not ln.startswith("the Client ID No")]
            warn += ["%s Merged record: %s" % (ws, ln) for ln in as_lines((record or {}).get("merge_notes"))]
            by_n = {e["n"]: e for e in entries}
            rows = []
            for b in ((record or {}).get("notes") or {}).get("blocks") or []:
                key = b.get("date") or next((by_n[n]["key"] for n in b["from"] if by_n[n]["key"]), None)
                rows.append("**%s**\n\n%s" % (heading_text(key, S["months"]), "\n".join("- " + x for x in as_lines(b["bullets"]))))
            seq = (["\n\n".join(warn)] if warn else []) + rows
            body = ("---\n\n" if not warn and rows else "") + "\n\n---\n\n".join(seq) if seq else "- " + NR
            parts.append("**%s:**\n\n%s\n" % (k, body))
        else:
            cs = f.get("Commission") or []
            body = "\n\n".join("%s\n%s" % (c["title"], "\n".join("- " + x for x in as_lines(c["lines"]))) for c in cs) if cs else "- " + NR
            parts.append("**%s:**\n\n%s\n" % (k, body))
    return ("\n---\n\n".join(parts)).rstrip("\n") + "\n"


def merge_lost(md, dups, left_out):
    """A merged record must keep everything from both versions: the earlier record's dates, amounts, numbers, codes, links, names and abbreviations are in the
    new record as drawn (or listed in left_out with a reason). [str]"""
    stop = settings()["name_stop"]
    left = [k.lower() for k, _v in left_out]
    have = N.tokens(md, stop)
    out = []
    for e in dups:
        tk = N.tokens(e["text"], stop)
        for kind in tk:
            for tok in sorted(tk[kind] - have[kind]):
                key = "%s: %s" % (kind, tok)
                if not any(k in key.lower() for k in left):
                    out.append("earlier record %s: %s is not in the merged record (nothing from either version may be lost)" % (e["id"], key))
    return out


def layout_problems(md):
    """Checks the finished Markdown: the 18 labels in order, a rule between sections, no HTML, no sign-off. [str]"""
    S = settings()
    P = []
    labels = re.findall(r"^\*\*([^*]+):\*\*\s*$", md, re.M)
    labels = [x for x in labels if x in S["fields"]]
    if labels != S["fields"]:
        P.append("the 18 field labels are not all present, once each, in the fixed order")
    if _html(md):
        P.append("the record contains HTML")
    if md.count("\n---\n") < len(S["fields"]):
        P.append("a horizontal rule is missing between sections")
    if re.search(r"(?i)\b(kind regards|best regards|yours (sincerely|faithfully)|regards,)\s*$", md.strip()):
        P.append("the record ends with a sign-off line")
    return P
