#!/usr/bin/env python3
"""Opens the finished SROA (.pdf) and proves what a program can prove of the old skill's pre-delivery checks.

Returns a list of (ok, short sentence, detail). Left to the eye (attested by verify.py): how the pages look (the page images are made for Paul's chat),
whether the logo looks right, whether text is crowded.
"""
import re

import build_sroa as bs
import docread
import wrlib as w

TITLE = "FAIS ‘RECORD OF ADVICE’ FOR SERVICING CHANGES"
CONFIRM = ("I confirm that the above information is a correct reflection of the advice provided in respect of the requested servicing changes and a copy of this "
           "document was provided to me in writing.")


def heal_arrow(text):
    """The builder's Helvetica draws the arrow between an old and a new figure with a glyph that a text reader returns as the letters 'fi' (it looks like an arrow to the eye).
    Put the arrow back so the page text can be compared with the data: only between two figures (the second starts with R or a digit)."""
    return re.sub(r"(?<=\S) fi (?=[R\d])", " \u2192 ", text)


def A(s):
    return docread.alnum(s)


def expected_sequence(data):
    """The text of the document, in reading order, as the builder draws it (a list of strings)."""
    seq = [TITLE, "Insurer : " + data["insurer"], "Policy Number : " + data["policy_number"], "Owner : " + data["owner"], "ID Number : " + data["owner_id"]]
    for b in data.get("quote_blocks", []):
        seq.append("%s — %s" % (b.get("block_label", ""), b.get("title", "")))
        if not b.get("compiled", True):
            seq.append(b.get("not_compiled_note", "Not compiled for this client."))
            continue
        if b.get("cp_number"):
            seq.append("CP Number: " + b["cp_number"])
        for g in b["groups"]:
            seq.append(g["heading"])
            seq += g["bullets"]
    seq.append(("Block 4 — " if data.get("quote_blocks") else "") + "Requested Servicing Change/s:")
    if data.get("accepted_quote_cp_number"):
        seq.append("Policy Number: %s | Accepted Quote — CP Number: %s" % (data["policy_number"], data["accepted_quote_cp_number"]))
    if data.get("grouped_changes"):
        for g in data["grouped_changes"]:
            seq.append(g["heading"])
            seq += g["bullets"]
    else:
        seq += bs.build_requested_changes_text(data["servicing_changes"]).split("\n")
    seq += ["Record of Advice: (Financial Advisor to give a brief summary of the basis of recommending the requested servicing changes):", data["advice_narrative"],
            "Portfolio Changes", "Record of Advice: (Financial Advisor to provide a reason for portfolio change, in light of owner’s risk profile)",
            data["portfolio_changes_narrative"], CONFIRM, data["client_signature_name"], bs.FIXED_ADVISOR_NAME, "Signature of Owner/", "Signature of Financial Advisor",
            "Authorised Signatory", "Date :", "Financial Advisor:", "Code: " + bs.FIXED_ADVISOR_CODE, "Name : " + bs.FIXED_ADVISOR_NAME]
    return seq


def _sequence_problem(text, seq):
    """Find every expected string, in order, in the page text (compared on letters and digits only, so line wraps and bullets do not matter)."""
    t, pos = A(text), 0
    for s in seq:
        k = A(s)
        if not k:
            continue
        at = t.find(k, pos)
        if at < 0:
            return s
        pos = at + len(k)
    return None


def check(path, data, a=None):
    """The checks, as [(ok, short, detail)]."""
    R = []

    def add(ok, short, detail=""):
        R.append((bool(ok), short, detail))
    try:
        rep = docread.read_pdf(path)
    except Exception as e:
        return [(False, "The SROA does not open as a PDF: %s" % e, "")]
    import pdfplumber
    with open(path, "rb") as f:
        raw = f.read()
    add(True, "The SROA opens as a valid PDF (%d page%s)" % (rep["page_count"], "" if rep["page_count"] == 1 else "s"))
    for pg in rep["pages"]:
        pg["text"] = heal_arrow(pg["text"])
    text = "\n".join(p["text"] for p in rep["pages"])
    # ---- the whole document, in order
    miss = _sequence_problem(text, expected_sequence(data))
    add(miss is None, "Every heading, figure, narrative and fixed line is on the page in the right order (title, insurer, policy, owner, ID, four blocks, narratives, signatures)" if miss is None
        else "Missing or out of order in the PDF: %r" % (miss[:90]))
    lines = [ln.strip() for ln in rep["pages"][0]["text"].splitlines() if ln.strip()]
    # ---- the header lines
    want = ["Insurer : %s" % data["insurer"], "Policy Number : %s" % data["policy_number"], "Owner : %s" % data["owner"], "ID Number : %s" % data["owner_id"]]
    idx = []
    for ln in want:
        idx.append(next((i for i, l in enumerate(lines) if A(l) == A(ln)), None))
    add(None not in idx and idx == sorted(idx) and (idx[3] == idx[2] + 1), "The ID number is printed on its own line directly under the Owner, and Insurer, Policy Number, Owner and ID read exactly as entered"
        if (None not in idx and idx == sorted(idx) and idx[3] == idx[2] + 1) else "The Insurer / Policy Number / Owner / ID lines are not as expected")
    # ---- block headings
    heads = ["%s — %s" % (b["block_label"], b["title"]) for b in data["quote_blocks"]]
    pos = [next((i for i, l in enumerate(text.splitlines()) if A(l) == A(h)), None) for h in heads]
    add(None not in pos and pos == sorted(pos), "The three quote blocks are in the fixed order (%s)" % "; ".join(b["title"] for b in data["quote_blocks"]),
        "found at line %s" % pos)
    cps = [b.get("cp_number") for b in data["quote_blocks"] if b.get("cp_number")]
    add(all(("CP Number: " + c) and A("CP Number: " + c) in A(text) for c in cps) and (not data.get("accepted_quote_cp_number") or A("Accepted Quote — CP Number: " + data["accepted_quote_cp_number"]) in A(text)),
        "Every CP number is printed on its quote and on the Requested Servicing Change/s line")
    acc = [b for b in data["quote_blocks"] if b["title"].endswith("(Accepted)")]
    add(len(acc) == 1 and acc[0].get("compiled", True), "Exactly one quote is marked (Accepted), and it is a compiled one")
    # ---- premium rule, bullets
    prem = [b for g in (data.get("grouped_changes") or []) for b in g["bullets"] if b.lower().startswith("premium")]
    prem += [x.split(": ")[0] + ": " for x in bs.build_requested_changes_text(data.get("servicing_changes", [])).split("\n") if x.lower().startswith("premium")]
    add(prem and all(p.startswith("Premium (incl. R20 policy fee)") for p in prem), "The premium line reads 'Premium (incl. R20 policy fee)' in the Requested Servicing Change/s block"
        if prem and all(p.startswith("Premium (incl. R20 policy fee)") for p in prem) else "The premium line is missing or not labelled 'Premium (incl. R20 policy fee)'")
    # ---- narratives
    inv = data["portfolio_changes_narrative"]
    add(A(data["advice_narrative"]) in A(text) and A(inv) in A(text), "The Record of Advice is exactly Paul's reason, and Portfolio Changes reads %s" % ("'N/A'" if inv == "N/A" else "his portfolio reason"))
    # ---- fixed lines and signatures
    ok_fixed = (A("Code: FSP45946") in A(text) and A("Name : Paul Kafentzis") in A(text) and A(data["client_signature_name"]) in A(text) and A(CONFIRM) in A(text))
    add(ok_fixed, "The advisor is FSP45946 / Paul Kafentzis, the client's typed name is %s, and the confirmation paragraph is word for word" % data["client_signature_name"])
    add("signed at" not in text.lower(), "There is no 'Signed at' line")
    pages_with = [i for i, p in enumerate(rep["pages"], 1) if A("I confirm that the above information") in A(p["text"])]
    pages_adv = [i for i, p in enumerate(rep["pages"], 1) if A("Name : Paul Kafentzis") in A(p["text"])]
    add(pages_with and pages_with == pages_adv and pages_with[-1] == rep["page_count"], "The confirmation paragraph, both signature lines and the Financial Advisor block sit together on the last page")
    # ---- the two date fields (AcroForm), by the raw bytes
    flds, blank = {}, True
    for nm in ("sroa_date_client", "sroa_date_advisor"):
        m = re.search(rb"/T \(%s\)([^>]*)" % nm.encode(), raw)
        flds[nm] = bool(m)
        v = re.search(rb"/V \(([^)]*)\)", m.group(1)) if m else None
        if v and v.group(1).strip():
            blank = False
    add(all(flds.values()) and blank, "The two date fields (client, advisor) exist as fillable fields and are empty" if all(flds.values()) and blank else
        "The two fillable date fields are missing or already filled (%s)" % flds)
    # ---- geometry: pdfplumber
    problems, logo_ok, sig_ok = [], False, False
    with pdfplumber.open(path) as pdf:
        for n, pg in enumerate(pdf.pages, 1):
            for wd in pg.extract_words():
                if wd["x0"] < bs.MARGIN_L - 3 or wd["x1"] > bs.PAGE_W - bs.MARGIN_R + 3 or wd["bottom"] > bs.PAGE_H - 40:
                    problems.append("page %d: %r runs outside the margins" % (n, wd["text"]))
                    break
        p1 = pdf.pages[0]
        words = p1.extract_words()
        title_top = min((wd["top"] for wd in words if wd["text"] == "FAIS"), default=None)
        imgs = p1.images
        logo_ok = bool(imgs) and title_top is not None and abs(imgs[0]["x0"] - bs.MARGIN_L) < 3 and imgs[0]["bottom"] <= title_top + 1 and imgs[0]["top"] < 60
        last = pdf.pages[-1]
        ln = sorted([l for l in last.lines if abs(l["y0"] - l["y1"]) < 0.5 and (l["x1"] - l["x0"]) > 150], key=lambda l: l["x0"])
        if len(ln) >= 2:
            l1, l2 = ln[0], ln[1]
            wl = [wd for wd in last.extract_words()]
            above = [wd for wd in wl if l1["top"] - 28 < wd["bottom"] <= l1["top"] + 1]
            below = [wd for wd in wl if l1["bottom"] < wd["top"] < l1["bottom"] + 20]
            sig_ok = abs(l1["top"] - l2["top"]) < 1 and l1["x1"] < l2["x0"] and not above and any(data["client_signature_name"].split()[0] == wd["text"] for wd in below)
    add(not problems, "Nothing is clipped or runs outside the margins on any page" if not problems else problems[0])
    add(logo_ok, "The logo is at the top left of page 1 and does not touch the title")
    add(sig_ok, "Two separate signature lines on the same level, clear blank space above each, the typed names below them")
    return R
