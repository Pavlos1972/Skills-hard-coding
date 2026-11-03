#!/usr/bin/env python3
"""Opens the finished ROA (.docx) and proves what a program can prove of the old skill's 21-point pre-delivery audit.

Returns a list of (ok, short sentence, detail). Only the checks that need an eye are left out (placeholder grey on screen, how an embedded page
looks next to the ROA's own text, an image border near the footer): those stay with the chat and are listed as attested by verify.py.
"""
import re
import zipfile

from lxml import etree

import build_roa as br
import roa
import wrlib as w

NS = dict(br.NS, wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing")
Wn = br.W
LABELS = ("Need Identified", "Recommended Amount", "Taken Up Amount", "Insurers Considered", "Recommended Insurer", "Recommendation for Identified Need")


def _txt(el):
    return " ".join("".join(el.itertext()).split())


def _local(el):
    return etree.QName(el).localname


def load(path):
    z = zipfile.ZipFile(path)
    bad = z.testzip()
    root = etree.fromstring(z.read("word/document.xml"))
    return z, root, bad


def parse_sections(body):
    """{key: {status, tables, data_rows, reason_rows, heading_idx}} for the seven sections of the template."""
    kids = list(body)
    idxs = {}
    for s in br.SECTIONS:
        try:
            idxs[s["key"]] = br.find_heading_index(kids, s["heading"])
        except ValueError:
            idxs[s["key"]] = None
    order = sorted((i, k) for k, i in idxs.items() if i is not None)
    try:
        end_all = br.find_heading_index(kids, "POLICY REPLACEMENT")
    except ValueError:
        end_all = len(kids)
    out = {}
    for n, (i, k) in enumerate(order):
        j = order[n + 1][0] if n + 1 < len(order) else end_all
        seg = kids[i + 1:j]
        reason_at = next((m for m, el in enumerate(seg) if _local(el) == "p" and "Reason this product suits" in _txt(el)), None)
        tables = [(m, el) for m, el in enumerate(seg) if _local(el) == "tbl"]
        data_tbl = next((el for m, el in tables if reason_at is None or m < reason_at), None)
        reason_tbl = next((el for m, el in tables if reason_at is not None and m > reason_at), None)

        def rows(t):
            return [[_txt(c) for c in r.findall("w:tc", NS)] for r in t.findall(".//w:tr", NS)] if t is not None else []
        out[k] = {"status": _txt(kids[i]).split(" - ")[-1].strip(), "data": rows(data_tbl), "reason": rows(reason_tbl), "heading": i, "end": j,
                  "heading_text": _txt(kids[i]), "tables": len(tables)}
    return out, kids


def _value(rows, label):
    for r in rows:
        if r and r[0].rstrip(":").strip().lower() == label.lower() and len(r) > 1:
            return r[1].strip()
    return None


def _fmt_amount(n, monthly):
    return "R %s%s" % (format(n, ",d"), " monthly" if monthly else "")


def check(path, a, data, rs, lists, embed_info=None):
    """The checks, as [(ok, short, detail)]."""
    R = []

    def add(ok, short, detail=""):
        R.append((bool(ok), short, detail))
    z, root, bad = load(path)
    body = root.find("w:body", NS)
    full = _txt(body)
    secs, kids = parse_sections(body)
    b = a["bundle"]
    add(bad is None, "The .docx opens as a valid package and its XML parses", str(bad or ""))
    active_key = {"risk": None, "retirement": "retirement", "investment": "investment"}[b]
    # 1 one bundle, every other section only heading and reason; declined sections too
    want_active = {k for k, s in data["sections"].items() if not s.get("declined")}
    bad_sec = []
    for k, s in secs.items():
        has_tbl = bool(s["data"]) and any(r and r[0].rstrip(":").strip() in LABELS for r in s["data"])
        if k in want_active:
            if s["status"] != "IMPORTANT" or not has_tbl:
                bad_sec.append("%s should be IMPORTANT with its table (is %s)" % (k, s["status"]))
        else:
            if s["status"] != "DO NOT REVIEW" or has_tbl:
                bad_sec.append("%s should be DO NOT REVIEW with no table (is %s%s)" % (k, s["status"], ", table present" if has_tbl else ""))
    add(not bad_sec, "Only the %s bundle is completed; every other section (and any declined need) shows only its heading and reason text" % b if not bad_sec else "Section problem: " + bad_sec[0], "; ".join(bad_sec))
    # 2 health care
    add("health care" not in full.lower(), "Health Care does not appear anywhere in the document")
    # 3 income after 24
    ia = secs.get("income_after24") or {}
    add(ia.get("status") == "DO NOT REVIEW" and (ia.get("reason") or [[""]])[0][0] == br.INCOME_AFTER_24_FIXED,
        "Income Protector Planning After 24 Months is Do not Review with the fixed sentence")
    # 4/5 dropdown values and fixed Need Identified
    prob = []
    for k, s in data["sections"].items():
        sec = secs[k]
        if k in want_active:
            need = _value(sec["data"], "Need Identified")
            exp = {"death": "Life Cover", "dread": "Comprehensive Severe Illness", "retirement": "Retirement Planning"}.get(k) or s.get("need_identified")
            if need != exp or not need:
                prob.append("%s Need Identified is %r, expected %r" % (k, need, exp))
            if k in ("disability", "income_1st24") and need not in lists["need"]["5B1"]:
                prob.append("%s Need Identified is not an option of the template" % k)
            rows = sec["data"] if k != "retirement" else sec["data"] + sec["reason"]
            for lab in ("Insurers Considered", "Recommended Insurer", "Recommendation for Identified Need"):
                v = _value(rows, lab)
                if not v or v == ".":
                    prob.append("%s %s is blank or the template-error option" % (k, lab))
    add(not prob, "Every Need Identified is filled and valid (Death = Life Cover, Dread = Comprehensive Severe Illness); no blank or '.' insurer or product" if not prob else "Dropdown problem: " + prob[0], "; ".join(prob))
    # 6 reasons
    rprob = []
    for k, (text, mode, head) in rs.items():
        sec = secs[k]
        got = (sec["reason"][-1][-1] if sec["reason"] else "")
        if " ".join(got.split()) != " ".join((text or "").split()):
            rprob.append("%s reason text differs from what the program expects" % k)
    custom = [roa.COVER_NAMES[k] for k, (t, m, h) in rs.items() if m == "custom"]
    add(not rprob, "Every reason text is exactly the bank paragraph, the fixed sentence, the reason Paul gave or the pointer line%s" % ((" (CUSTOM, not from the bank: %s)" % ", ".join(custom)) if custom else "")
        if not rprob else "Reason text problem: " + rprob[0], "; ".join(rprob))
    # 7 amounts
    aprob = []
    for k, s in data["sections"].items():
        if s.get("declined") or b != "risk":
            continue
        monthly = bool(s.get("is_monthly"))
        d = secs[k]["data"]
        for lab, v in (("Recommended Amount", s["recommended_amount"]), ("Taken Up Amount", s["taken_up_amount"])):
            if _value(d, lab) != _fmt_amount(v, monthly):
                aprob.append("%s %s is %r, expected %r" % (k, lab, _value(d, lab), _fmt_amount(v, monthly)))
    if b == "risk":
        add(not aprob, "Every Recommended and Taken Up Amount shows one clean value (a not-accepted cover shows R 0)" if not aprob else "Amount problem: " + aprob[0], "; ".join(aprob))
    # 8 client name and ID line
    nm, cid = data["client_name"], data["client_id"]
    add(full.count(nm) >= 3 and ("I, %s, (ID: %s), hereby confirm" % (nm, cid)) in full and re.fullmatch(r"\d{13}", cid) is not None,
        "The client's name appears in all places and the ID line reads 'I, Name, (ID: 13 digits), hereby confirm'")
    # 9 next meeting
    add(("diarised for the %s" % roa.next_review(data["roa_date"])) in full, "The next meeting date is the ROA date plus 12 months (%s)" % roa.next_review(data["roa_date"]))
    # 10 author
    add("PAUL KAFENTZIS" in full and "GARETH" not in full.upper(), "The financial planner is PAUL KAFENTZIS")
    # 11 placeholders
    leftovers = [p for p in ("Choose an item.", "Click here to enter", "[Comments]", "[Abstract]", "(Name)") if p in full]
    add(not leftovers, "No template placeholder text is left (the client's own signature date is deliberately blank)" if not leftovers else "Placeholder text left: %s" % ", ".join(leftovers))
    # 12 RAR reference
    add("RAR reference number:" not in full, "The RAR reference number field is gone")
    # 13 reference and replacement
    add(("ROA Reference No: %s" % data["roa_reference_no"]) in full, "The ROA reference number is exactly %s" % data["roa_reference_no"])
    rep = "The product recommended will %s existing" % ("replace" if data["policy_replacement"] else "not replace")
    add(rep in full, "The policy replacement wording is '%s' (it follows the cover types)" % ("replace" if data["policy_replacement"] else "not replace"))
    # 14 Retirement order
    if b == "retirement":
        labels = [r[0].rstrip(":") for r in secs["retirement"]["reason"][:3]]
        add(labels == ["Insurers Considered", "Recommended Insurer", "Recommendation for Identified Need"] and len(secs["retirement"]["reason"]) == 4,
            "The Retirement section reads Need Identified, Insurers Considered, Recommended Insurer, Recommendation, then Reason")
    # 15 no placeholder grey on filled controls
    grey = 0
    for sdt in root.iter(Wn + "sdt"):
        t = _txt(sdt)
        if t and t not in ("Click to select a date.", "Choose an item.") and sdt.findall(".//w:rStyle[@w:val='PlaceholderText']", NS):
            grey += 1
    add(grey == 0, "No filled field is set in placeholder grey" if not grey else "%d filled field(s) are still in placeholder grey" % grey)
    # 16 embedded email pages
    if b != "risk":
        pics = [(i, el) for i, el in enumerate(kids) if _local(el) == "p" and any((d.get("name") or "").startswith("Proposal Email Page") for d in el.findall(".//wp:docPr", NS))]
        n = embed_info["pages"] if embed_info else 0
        sec = secs[b]
        pos_ok = bool(pics) and all(sec["heading"] < i < sec["end"] for i, _ in pics)
        caps = all(_txt(kids[i + 1]) == "page %d of %d" % (m + 1, len(pics)) for m, (i, _) in enumerate(pics)) if pics else False
        keep = all(el.find("w:pPr/w:keepNext", NS) is not None for _, el in pics)
        no_blank = all(pics[m + 1][0] == pics[m][0] + 2 for m in range(len(pics) - 1))
        wide = all(int(el.find(".//wp:extent", NS).get("cx")) <= 5000000 for _, el in pics)
        add(len(pics) == n and n > 0, "%d email page image(s) are embedded (one per rendered page)" % len(pics) if len(pics) == n and n > 0 else "Embedded images %d, rendered pages %d" % (len(pics), n))
        add(pos_ok, "The pages sit right after the %s section's table, never inside a table cell" % b if pos_ok else "The embedded pages are not directly after the %s section" % b)
        add(caps and keep and no_blank and wide, "Each page is a bordered picture paragraph kept with its 'page X of Y' caption, no blank spacer, width within 5,000,000 EMU" if caps and keep and no_blank and wide else
            "Picture/caption problem (captions %s, keepNext %s, no spacer %s, width %s)" % (caps, keep, no_blank, wide))
    return R
