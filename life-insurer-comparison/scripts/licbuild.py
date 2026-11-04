#!/usr/bin/env python3
"""Builds the comparison letter (one standalone HTML file), the covering email body and the Teams message from the confirmed answers and the fixed template, and checks what it built
and what comes back from Outlook and Teams. Nothing here is typed by the chat and nothing here sends anything."""
import html
import json
import re
from decimal import Decimal

import lic as c
import wrlib as w

E = html.escape
STRUCTURAL = {"html", "head", "body", "meta", "title", "style"}


def money(v):
    return w.fmt_money(w.parse_money(v))


def pcs(v):
    return c.pct_str(v) + "%"


def doc_word(s, docs):
    return docs["docs"][c.side_docs(docs)[s["label"]]]["role"]          # "quote" or "schedule"


def cls(i):
    return "s%d" % (i + 1)


def chip(a, i):
    return '<span class="chip %s">%s</span>' % (cls(i), E(a["sides"][i]["insurer"]))


def text_of(h):
    h = re.sub(r"(?is)<(script|style).*?</\1>", " ", h)
    h = re.sub(r"(?i)<br\s*/?>|</p>|</li>|</tr>|</h\d>|</div>|</td>|</th>", "\n", h)
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", h)).split())


# ------------------------------------------------------------------ sections of the letter
def pattern_text(s):
    wd = c.wording()
    return wd["pattern_fixed"] if s["escalation"]["type"] == "fixed" else wd["pattern_age_rated"]


def sec_snapshot(a, scope, docs):
    wd = c.wording()
    cards = []
    for i, s in enumerate(a["sides"]):
        lead = " lead" if s["role"] == "proposal" else ""
        esc = s["escalation"]
        rows = [(wd["monthly_label"], "<strong>%s</strong>" % E(money(s["premium"]["monthly"]))),
                (wd["pattern_label"], "%s%s" % (E(pattern_text(s)), (" (%s)" % E(pcs(esc["rate"]))) if esc.get("rate") else ""))]
        if s.get("benefit_escalation"):
            rows.append((wd["benefit_label"], E(pcs(s["benefit_escalation"]["rate"]))))
        g = s["guarantee"]
        rows.append((wd["guarantee_label"], E(g["text"]) if not g.get("not_stated") else E(wd["guarantee_not_stated"].format(insurer=s["insurer"]))))
        cards.append('<div class="card %s%s"><div class="cardhead">%s%s</div><div class="prod">%s</div><dl>%s</dl></div>' % (
            cls(i), lead, chip(a, i), ' <span class="lead-note">%s</span>' % E(wd["lead_note"]) if lead else "", E(s["product_name"]),
            "".join("<dt>%s</dt><dd>%s</dd>" % (E(k), v) for k, v in rows)))
    return '<div class="cards">%s</div>' % "".join(cards)


def cover_rows(a, scope):
    """[(life order, category order, key, display label)]: the main life first, by category, then the second life; first-seen order inside a category."""
    order = {x: n for n, x in enumerate(c.COVER_CATEGORIES)}
    seen, rows = {}, []
    for s in a["sides"]:
        for cv in s["covers"]:
            life = cv.get("life", "main")
            k = (life, cv["category"], w.norm(cv["label"]))
            if k not in seen:
                seen[k] = len(seen)
                rows.append((0 if life == "main" else 1, order[cv["category"]], seen[k], k, cv["label"].strip()))
    rows.sort(key=lambda r: r[:3])
    return [(r[0], r[1], r[3], r[4]) for r in rows]


def sec_cover(a, scope, docs):
    wd = c.wording()
    head = "".join('<th class="%s">%s<br><small>%s</small></th>' % (cls(i), E(s["label"]), E(s["product_name"])) for i, s in enumerate(a["sides"]))
    body = []
    sec = scope["second_life"]
    last_life = None
    for life_ord, _o, k, label in cover_rows(a, scope):
        if life_ord == 1 and last_life != 1:
            body.append('<tr class="sub"><td colspan="%d">%s</td></tr>' % (len(a["sides"]) + 1, E(wd["second_life_label"].format(name=sec["name"]))))
        last_life = life_ord
        cells = []
        for i, s in enumerate(a["sides"]):
            cv = next((x for x in s["covers"] if (x.get("life", "main"), x["category"], w.norm(x["label"])) == k), None)
            if cv is None:
                cells.append('<td class="na">%s</td>' % E(wd["not_on"][doc_word(s, docs)]))
            else:
                monthly = "<br><small>%s a month</small>" % E(money(cv["monthly"])) if cv.get("monthly") else ""
                cells.append("<td>%s%s</td>" % (E(money(cv["amount"])), monthly))
        body.append("<tr><th scope=\"row\">%s</th>%s</tr>" % (E(label), "".join(cells)))
    body.append('<tr class="total"><th scope="row">%s</th>%s</tr>' % (E(wd["total_row"]), "".join("<td>%s</td>" % E(money(s["premium"]["monthly"])) for s in a["sides"])))
    out = ['<div class="scroll"><table class="cmp" style="min-width:%dpx"><thead><tr><th>Benefit</th>%s</tr></thead><tbody>%s</tbody></table></div>' % (180 + 170 * len(a["sides"]), head, "".join(body))]
    if sec["present"]:
        items = []
        for i, s in enumerate(a["sides"]):
            sl = s["second_life"]
            txt = {"independent": wd["second_life_independent"], "rider": wd["second_life_rider"],
                   "none": wd["second_life_none"].format(name=sec["name"], doc=doc_word(s, docs))}[sl["status"]]
            items.append("<li>%s %s</li>" % (chip(a, i), E(txt)))
        out.append("<ul class=\"plain\">%s</ul>" % "".join(items))
    out.append(features_block(a, scope, docs))
    return "".join(out)


def feature_label(a, f, docs):
    wd = c.wording()
    s = next(x for x in a["sides"] if x["label"] == f["side"])
    if f["basis"] == "client_document":
        return wd["basis_label"]["client_document"] if not s.get("rar_only") else "From the RAR, not the policy schedule"
    return wd["basis_label"][f["basis"]].format(insurer=s["insurer"])


def features_block(a, scope, docs):
    wd = c.wording()
    if not a["features"]:
        return ""
    items, wins, trade = [], {}, 0
    for f in a["features"]:
        i = next(n for n, x in enumerate(a["sides"]) if x["label"] == f["side"])
        s = a["sides"][i]
        badge = ""
        if f.get("badge") == "wins":
            badge = ' <span class="badge win">%s</span>' % E(wd["badge_wins"].format(insurer=s["insurer"]))
            wins[s["insurer"]] = wins.get(s["insurer"], 0) + 1
        elif f.get("badge") == "tradeoff":
            badge = ' <span class="badge trade">%s</span>' % E(wd["badge_tradeoff"])
            trade += 1
        extra = ""
        if f.get("not_on_proposal"):
            extra = '<br><em class="np">%s</em>' % E(wd["not_on_proposal"].format(conditions=f["conditions"].strip()))
        items.append('<li>%s %s%s<br><small class="src">%s</small>%s</li>' % (chip(a, i), E(f["text"].strip()), badge, E(feature_label(a, f, docs)), extra))
    ahead = wd["ahead_line"].format(wins=", ".join("%s (%d)" % kv for kv in wins.items()) or "none", tradeoffs=str(trade)) if (wins or trade) else wd["ahead_none"]
    return '<h3>%s</h3><ul class="plain features">%s</ul><p class="ahead">%s</p>' % (E(wd["features_heading"]), "".join(items), E(ahead))


def esc_rows(a):
    lim = c.limits()["min_projection_years"]
    return max([lim] + [len(s.get("projection") or []) for s in a["sides"]])


def sec_escalation(a, scope, docs):
    wd = c.wording()
    pj = [c.proj_rows(s) for s in a["sides"]]
    head = "".join('<th class="%s">%s</th>' % (cls(i), E(s["label"])) for i, s in enumerate(a["sides"]))
    body = []
    outl = {}
    for i, s in enumerate(a["sides"]):
        outl[i] = {n for n, _p in c.esc_summary(s)["outliers"]}
    for n in range(1, esc_rows(a) + 1):
        age = next((r["age"] for rows in pj for r in rows if r["n"] == n and r["age"] is not None), None)
        lab = next((r["label"] for rows in pj for r in rows if r["n"] == n and r["label"]), None)
        cells = []
        for i, rows in enumerate(pj):
            r = next((x for x in rows if x["n"] == n), None)
            if r is None:
                cells.append('<td class="na" data-s="%d" data-n="%d">%s</td>' % (i, n, E(wd["na"])))
                continue
            badge = ""
            if r["pct"] is not None:
                mark = "" if r["kind"] == "printed" else "&dagger;"
                css = "pct %s%s" % (r["kind"], " warn" if n in outl[i] else "")
                badge = ' <span class="%s" data-badge="1">%s%s</span>' % (css, E(c.pct_str(r["pct"])) + "%", mark)
            cells.append('<td data-s="%d" data-n="%d">%s%s</td>' % (i, n, E(w.fmt_money(r["premium"])), badge))
        body.append("<tr><th scope=\"row\">%s%s</th><td>%s</td>%s</tr>" % ("Year %d" % n, " <small>%s</small>" % E(lab) if lab else "", E(str(age)) if age is not None else "&ndash;", "".join(cells)))
    notes = []
    printed = [s["label"] for s, v in zip(a["sides"], (c.esc_summary(s) for s in a["sides"])) if v["mode"] in ("printed", "mixed")]
    calcd = [s["label"] for s, v in zip(a["sides"], (c.esc_summary(s) for s in a["sides"])) if v["mode"] in ("calculated", "mixed")]
    if printed:
        notes.append(wd["esc_foot_printed"].format(sides=", ".join(printed)))
    if calcd:
        notes.append(wd["esc_foot_calculated"].format(sides=", ".join(calcd)))
    notes.append(wd["esc_foot_start"])
    if any(len(rows) < esc_rows(a) for rows in pj):
        notes.append(wd["esc_foot_na"])
    for i, s in enumerate(a["sides"]):
        for n, p in c.esc_summary(s)["outliers"]:
            notes.append(wd["esc_foot_outlier"].format(side=s["label"], n=n, pct=c.pct_str(p), insurer=s["insurer"]))
    return '<div class="scroll"><table class="cmp" style="min-width:%dpx"><thead><tr><th>Year</th><th>%s</th>%s</tr></thead><tbody>%s</tbody></table></div><p class="foot">%s</p>' % (
        200 + 160 * len(a["sides"]), E(wd["esc_cols"][1]), head, "".join(body), E(" ".join(notes)))


def sec_loyalty(a, scope, docs):
    wd = c.wording()
    rows = []
    for i, s in enumerate(a["sides"]):
        ly = s.get("loyalty")
        if ly:
            rows.append("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (chip(a, i), E(ly["name"]), E(ly["amount_or_pct"]), E(ly["when"])))
        else:
            rows.append('<tr><td>%s</td><td>&ndash;</td><td class="na">%s</td><td>&ndash;</td></tr>' % (chip(a, i), E(wd["not_on"][doc_word(s, docs)])))
    return '<div class="scroll"><table class="cmp"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div><p class="foot">%s</p>' % (
        "".join("<th>%s</th>" % E(x) for x in wd["loyalty_cols"]), "".join(rows), E(wd["loyalty_closing"]))


def sec_definitions(a, scope, docs):
    wd = c.wording()
    rows = []
    for d in a["definitions"]:
        i = next(n for n, x in enumerate(a["sides"]) if x["label"] == d["side"])
        rows.append("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s <small class=\"src\">%s</small></td></tr>" % (
            chip(a, i), E(terms_name(d["category"])), E(d["set"]), E(d.get("note") or ""), E(feature_label(a, d, docs))))
    return '<div class="scroll"><table class="cmp"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % ("".join("<th>%s</th>" % E(x) for x in wd["definitions_cols"]), "".join(rows))


def terms_name(cat):
    return c.terms()["category_names"].get(cat, "Terminal illness" if cat == "terminal_illness" else cat)


def sec_verdict(a, scope, docs):
    return '<div class="verdict"><ul>%s</ul></div>' % "".join("<li><strong>%s</strong> %s</li>" % (E(v["headline"].strip()), E(v["detail"].strip())) for v in a["verdict"])


def sec_sources(a, scope, docs, today=None):
    wd = c.wording()
    items = []
    for s in a["sides"]:
        d = docs["docs"][c.side_docs(docs)[s["label"]]]
        bits = [s["label"], d["name"]]
        if s.get("reference"):
            bits.append("document number %s" % s["reference"])
        bits.append("dated %s" % s["document_date"] if s.get("document_date") else "date not stated")
        items.append("<li>%s</li>" % E(" - ".join(bits)))
    for k in c.served_keys_order(docs):
        d = docs["docs"][k]
        if d["role"] in ("intake_notes", "fact_find_summary", "overview", "broker_doc"):
            items.append("<li>%s (%s)</li>" % (E(d["name"]), E({"intake_notes": "meeting notes", "fact_find_summary": "Fact Find Summary", "overview": "WR Overview", "broker_doc": "background document, not a figures source"}[d["role"]])))
    guides = ["<li>%s - %s, read on %s</li>" % (E(d["label"]), E(d["url"]), E(d["fetched_at"])) for k in c.served_keys_order(docs) for d in [docs["docs"][k]] if d["role"] == "guide"]
    return "<p>%s</p><ul class=\"plain\">%s</ul>%s" % (E(wd["disclaimer"]), "".join(items), ("<p>%s</p><ul class=\"plain\">%s</ul>" % (E(wd["sources_guides"]), "".join(guides))) if guides else "")


def closing(a, scope):
    ad = c.settings()["adviser"]
    return ('<div class="closing"><p>%s</p><p><strong>%s</strong><br>%s<br>%s<br>WhatsApp %s<br>Office %s<br>Email %s</p></div>' %
            (E(c.wording()["closing_line"]), E(ad["name"]), E(ad["company"]), E(ad["fsp"]), E(ad["whatsapp"]), E(ad["office"]), E(ad["email"])))


SECTION_BUILDERS = {"premium_snapshot": sec_snapshot, "cover_comparison": sec_cover, "escalation_table": sec_escalation, "loyalty": sec_loyalty, "definitions": sec_definitions,
                    "verdict": sec_verdict}


def header(a, scope, docs, today):
    wd = c.wording()
    ad = c.settings()["adviser"]
    chips = []
    for i, s in enumerate(a["sides"]):
        d = doc_word(s, docs)
        chips.append('<li>%s <strong>%s</strong>%s <small>(%s%s)</small></li>' % (chip(a, i), E(s["product_name"]), " &ndash; " + E(s["tier"]) if s.get("tier") else "",
                                                                                     "quote" if d == "quote" else "in-force policy schedule", ", ref. " + E(s["reference"]) if s.get("reference") else ""))
    return ('<header class="top"><h1>%s</h1><p class="lede">Prepared for %s &middot; %s</p><ul class="plain chips">%s</ul><p class="adviser">%s, %s, %s</p></header>' %
            (E(wd["title"]), E(a["client_full_name"].strip()), today.strftime("%d/%m/%Y"), "".join(chips), E(ad["name"]), E(ad["company"]), E(ad["fsp"])))


def build_letter(a, scope, docs, today):
    wd = c.wording()
    with open(c.TEMPLATE, encoding="utf-8") as f:
        t = f.read()
    parts = [header(a, scope, docs, today), '<div class="banner">%s</div>' % E(a["banner"].strip()),
             '<div class="salutation"><p>Dear %s,</p><p>%s</p></div>' % (E(a["client_first_name"].strip()), E(a["opening"].strip()))]
    last = None
    for sec in c.canonical_sections(scope):
        if sec == "sources":
            continue
        parts.append('<section id="sec-%s"><h2>%s</h2>%s</section>' % (sec, E(wd["section_titles"][sec]), SECTION_BUILDERS[sec](a, scope, docs)))
    parts.append(closing(a, scope))
    if "sources" in scope["sections"]:
        parts.append('<section id="sec-sources"><h2>%s</h2>%s</section>' % (E(wd["section_titles"]["sources"]), sec_sources(a, scope, docs)))
    t = t.replace("[TITLE]", E("%s - %s" % (wd["title"], a["client_full_name"].strip()))).replace("[CONTENT]", "\n".join(parts))
    return t


def build_body(a, scope, docs):
    wd = c.wording()
    em = a["email"]
    cta = wd["email_cta_first"] if scope["voice"] == "first_person" else wd["email_cta_third"]
    p = ["<p>Dear %s,</p>" % E(a["client_first_name"].strip()), "<p>%s</p>" % E(em["opening"].strip())]
    if (em.get("concern") or "").strip():
        p.append("<p>%s</p>" % E(em["concern"].strip()))
    p.append("<p><b>%s</b></p>" % E(wd["email_findings"]))
    p.append("<ul>%s</ul>" % "".join("<li>%s</li>" % E(b.strip()) for b in em["bullets"]))
    rar = [s["label"] for s in a["sides"] if s.get("rar_only")]
    if rar:
        p.append("<p>%s</p>" % E(wd["email_rar"].format(sides=", ".join(rar))))
    p += ["<p>%s</p>" % E(wd["email_chrome"]), "<p>%s</p>" % E(cta)]
    return "\n".join(p) + "\n"


def build_all(a, scope, docs, today):
    return build_letter(a, scope, docs, today), build_body(a, scope, docs)


# ------------------------------------------------------------------ the Teams message to Sitamah
def teams_text(a, scope, docs, greeting, file):
    wd = c.wording()
    key = "teams_paul" if c.settings()["attach_by"] == "paul" else "teams_sitamah"
    return wd[key].format(greeting=greeting, client=a["client_full_name"].strip(), insurers=" vs ".join(c.distinct_insurers(a)), basis=wd["basis_text"][scope["basis"]],
                          email=a["client_email"].strip(), folder=a["plan_folder"].strip(), file=file)


# ------------------------------------------------------------------ checks on what was built
NUM_TOKEN = re.compile(r"\d[\d ]*\d(?:[.,]\d+)?|\d(?:[.,]\d+)?")


def number_of(tok):
    d = w.parse_money(tok)
    if d is not None:
        return d
    try:
        return Decimal(re.sub(r"\D", "", tok)) if re.sub(r"\D", "", tok) else None
    except Exception:
        return None


def allowed_numbers(a):
    """Every number the answers hold (amounts, rates, percentages, ages, years, the percentages the program works out): the covering email may use no other number."""
    out = set()

    def walk(x):
        if isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
        elif isinstance(x, str):
            for tok in NUM_TOKEN.findall(x):
                v = number_of(tok)
                if v is not None:
                    out.add(v)
        elif isinstance(x, (int, float)) and not isinstance(x, bool):
            out.add(Decimal(str(x)))
    for s in a["sides"]:
        walk(s)
        for r in c.proj_rows(s):
            for v in (r["pct"], r["calc"], r["printed"]):
                if v is not None:
                    out.add(v)
        sm = c.esc_summary(s)
        if sm["avg"] is not None:
            out.add(sm["avg"])
        out.add(Decimal(sm["years"]))
    return out


def html_problems(letter, body, a, scope, docs, today, file=None):
    """[(ok, short, detail)]: every check on the built letter and the email body."""
    R = []

    def add(ok, short, detail=""):
        R.append((bool(ok), short, detail))
    wd = c.wording()
    lim = c.limits()
    add(not c.PLACEHOLDER.search(re.sub(r"(?is)<style.*?</style>", "", letter)) and not c.PLACEHOLDER.search(body) and "@@" not in letter, "No placeholder or leftover text in the letter or the email")
    add(letter.count("<table") == letter.count("</table>") and letter.count("<div") == letter.count("</div>") and letter.count("<section") == letter.count("</section>") and
        letter.count("<ul") == letter.count("</ul>") and letter.count("<tr") == letter.count("</tr>"), "Tables, rows, lists, sections and divs open = close")
    want = c.canonical_sections(scope)
    got = re.findall(r'<section id="sec-([a-z_]+)">', letter)
    add(got == [x for x in want if x != "sources"] + (["sources"] if "sources" in want else []), "The letter has exactly the sections that were ticked, in the fixed order (%s)" % ", ".join(got))
    iban, isal, iclo = letter.find('class="banner"'), letter.find('class="salutation"'), letter.find('class="closing"')
    isrc = letter.find('id="sec-sources"')
    first_sec = letter.find("<section")
    between = letter[iban:isal] if iban >= 0 < isal else ""
    last_other = max([m.start() for m in re.finditer(r'<section id="sec-(?!sources)', letter)] or [-1])
    add(0 < letter.find("<header") < iban < isal < (first_sec if first_sec >= 0 else iclo) and "<section" not in between,
        "Letter format: header, Key Facts Banner, then the salutation straight after it, then the sections")
    ad = c.settings()["adviser"]
    add(iclo > last_other and (isrc < 0 or iclo < isrc) and all(x in letter[iclo:iclo + 700] for x in (wd["closing_line"], ad["name"], ad["fsp"], ad["whatsapp"], ad["office"], ad["email"])),
        "Letter format: the signed closing (Kind regards, name, company, FSP, WhatsApp, office, email) sits after the last section and before Disclaimer/Sources")
    add(("<p>Dear %s,</p>" % E(a["client_first_name"].strip())) in letter[isal:isal + 200], "The salutation is 'Dear %s,' (the first name)" % a["client_first_name"].strip())
    # the scope: nothing from an out-of-scope category anywhere (the product and file names in the header and the sources are facts and are not scanned)
    scan = re.sub(r"(?is)<head>.*?</head>", " ", letter)
    scan = re.sub(r'(?is)<header class="top">.*?</header>', " ", scan)
    scan = re.sub(r'(?is)<section id="sec-sources">.*?</section>', " ", scan)
    hits = c.scope_hits(text_of(scan), scope) + c.scope_hits(text_of(body), scope)
    add(not hits, "Benefit scope: no word of an out-of-scope category (%s) anywhere in the letter or the email" % (", ".join(k for k in c.CATEGORIES if scope["categories"][k]["status"] == "out") or "none out") if not hits else
        "Out-of-scope words found: %s" % "; ".join("%s (%s)" % (t_, k) for k, t_ in hits))
    # voice, version history
    prose = text_of(re.sub(r'(?is)<div class="closing">.*?</div>', " ", scan)) + " " + text_of(body)
    vp = c.voice_problems(prose, scope["voice"], a["client_full_name"]) + c.version_problems(prose)
    add(not vp, "Voice: %s throughout, no slip into the third person about the client, no quote-version history" % ("Paul's first person" if scope["voice"] == "first_person" else "the institutional voice") if not vp else "Voice or history problem: %s" % "; ".join(vp))
    add(w.norm(a["client_full_name"]) not in w.norm(prose.replace("Prepared for", "")), "The client is addressed as 'you': the full name appears only in the header")
    # figures: every premium and every cover amount is in the letter
    plain = text_of(letter)
    missing = []
    for s in a["sides"]:
        for v in [s["premium"]["monthly"]] + [cv["amount"] for cv in s["covers"]]:
            if money(v) not in plain:
                missing.append("%s %s" % (s["label"], money(v)))
    add(not missing, "Every monthly premium and cover amount from the answers is in the letter" if not missing else "Missing from the letter: %s" % ", ".join(missing[:4]))
    # the escalation table
    if "escalation_table" in want:
        bad, nrows = [], esc_rows(a)
        for i, s in enumerate(a["sides"]):
            rows = c.proj_rows(s)
            for n in range(2, nrows + 1):
                r = next((x for x in rows if x["n"] == n), None)
                cell = re.search(r'<td[^>]*data-s="%d" data-n="%d"[^>]*>(.*?)</td>' % (i, n), letter, re.S)
                if cell is None:
                    bad.append("%s year %d: no cell" % (s["label"], n))
                elif r is None:
                    if wd["na"] not in cell.group(1):
                        bad.append("%s year %d: a gap must read '%s'" % (s["label"], n, wd["na"]))
                elif r["pct"] is not None and 'data-badge="1"' not in cell.group(1):
                    bad.append("%s year %d: no percentage badge" % (s["label"], n))
        add(not bad and nrows >= lim["min_projection_years"], "Premium Escalation: %d years, a percentage badge on every year that has a rand figure after the first, gaps read '%s'" % (nrows, wd["na"]) if not bad else "Escalation table: %s" % "; ".join(bad[:3]))
        foot = re.search(r'<p class="foot">(.*?)</p>', letter[letter.find('id="sec-escalation_table"'):], re.S)
        names = [s["label"] for s in a["sides"] if c.esc_summary(s)["mode"]]
        add(foot is not None and all(n_ in html.unescape(foot.group(1)) for n_ in names), "The footnote names, for every insurer, whether its percentages are printed or our own calculation")
        marks = letter.count("&dagger;")
        add(marks == 0 or "our own calculation" in html.unescape(foot.group(1) if foot else ""), "Every dagger in the escalation table has its explanatory note below the table")
    # the covering email
    tags = set(re.findall(r"<\s*/?\s*([a-zA-Z0-9]+)", body))
    add(tags <= set(wd["allowed_email_tags"]), "The email body uses only tags the Microsoft 365 draft tool allows (%s)" % ", ".join(sorted(tags)) if tags <= set(wd["allowed_email_tags"]) else
        "Tags not allowed in the draft: %s" % ", ".join(sorted(tags - set(wd["allowed_email_tags"]))))
    btxt = text_of(body)
    add("Kind regards" not in btxt and ad["email"] not in btxt and ad["whatsapp"] not in btxt and ad["office"] not in btxt and not re.search(r"\b0\d{2}[ ]\d{3}[ ]\d{4}\b", btxt),
        "The email carries no typed signature, sign-off or contact details (the Exchange rule adds the signature once, at send time)")
    nb = len(a["email"]["bullets"])
    add(lim["email_bullets_min"] <= nb <= lim["email_bullets_max"] and body.count("<li>") == nb and "Google Chrome" in btxt, "The email has %d finding bullets (4 to 6), tells the client to open the document in Google Chrome and has the call-or-WhatsApp line" % nb)
    allowed = allowed_numbers(a)
    bad = []
    for b_ in [text_of(x) for x in re.findall(r"<(?:p|li)>(.*?)</(?:p|li)>", body, re.S)]:
        for tok in NUM_TOKEN.findall(b_):
            v = number_of(tok)
            if v is not None and v not in allowed:
                bad.append(tok)
    add(not bad, "Every number in the email is a figure from the confirmed answers (the same figures as the letter)" if not bad else "In the email but not among the confirmed figures: %s" % ", ".join(bad[:5]))
    add(len(re.findall(r"<script|<iframe|onclick=|<img", letter, re.I)) == 0 and letter.count("fonts.googleapis.com") <= 1, "The letter has no script, no image and no outside link except the Google Fonts stylesheet")
    return R


def flatten(text):
    try:
        obj = json.loads(text)
    except ValueError:
        return text, None, [text]
    out = []

    def walk(x):
        if isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
        elif isinstance(x, str):
            out.append(x)
    walk(obj)
    return "\n".join(out), obj, out


def find_key(obj, names):
    names = {n.lower() for n in names}
    found = []

    def walk(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if k.lower() in names:
                    found.append(v)
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(obj)
    return found


def _emails(x):
    return {e.lower() for e in re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", json.dumps(x))}


def draft_problems(text, a, scope, docs, today):
    """What came back from Outlook after the Microsoft 365 draft tool made the draft: every line is a check."""
    flat, obj, leaves = flatten(text)
    R = []

    def add(ok, short):
        R.append((bool(ok), short))
    wd = c.wording()
    ad = c.settings()["adviser"]
    to_v = find_key(obj, ("toRecipients", "to")) if obj is not None else []
    cc_v = find_key(obj, ("ccRecipients", "cc")) if obj is not None else []
    client = a["client_email"].strip().lower()
    if to_v or cc_v:
        to_set, cc_set = set().union(*[_emails(x) for x in to_v]) if to_v else set(), set().union(*[_emails(x) for x in cc_v]) if cc_v else set()
        add(client in to_set and c.CC_EMAIL in cc_set and c.CC_EMAIL not in to_set, "To = the client (%s) and Cc = %s, read back from the saved draft" % (a["client_email"].strip(), c.CC_NAME))
    else:
        add(client in flat.lower() and c.CC_EMAIL in flat.lower(), "The client (%s) and %s are on the draft (the read-back has no separate To and Cc fields)" % (a["client_email"].strip(), c.CC_NAME))
    subs = [x for x in (find_key(obj, ("subject",)) if obj is not None else []) if isinstance(x, str)]
    add((c.subject(a) in subs) if subs else (c.subject(a) in flat), "The subject is exactly the one the program built")
    cands = [x for x in leaves if "Dear " in x]
    body = max(cands, key=len) if cands else flat
    bt = text_of(body)
    tags = set(t.lower() for t in re.findall(r"<\s*/?\s*([a-zA-Z0-9]+)", body)) - STRUCTURAL
    add(tags <= set(wd["allowed_email_tags"]), "The saved body uses only allowed tags (no image, no span, no script)")
    need = ["Dear %s," % a["client_first_name"].strip(), a["email"]["opening"].strip()] + [b.strip() for b in a["email"]["bullets"]] + [wd["email_chrome"]]
    miss = [x for x in need if " ".join(x.split()) not in bt]
    add(not miss, "The draft carries the greeting, the opening, every finding bullet and the Chrome line exactly as built" if not miss else "Missing from the draft: %s" % miss[0][:80])
    add("Kind regards" not in bt and ad["email"] not in bt and ad["whatsapp"] not in bt and ad["office"] not in bt, "No typed signature, 'Kind regards,' or contact details in the draft (the server adds the signature at send time)")
    add(not c.PLACEHOLDER.search(body) and "BODY_PLACEHOLDER" not in body and not re.search(r"\bLoop\b", flat), "No placeholder text and no Loop component in the draft")
    att = find_key(obj, ("hasAttachments",)) if obj is not None else []
    add(not any(att), "The draft has no attachment yet (the HTML letter is attached by %s)" % ("Paul" if c.settings()["attach_by"] == "paul" else "Sitamah"))
    return R


def message_problems(text, a, scope, docs, greeting, file):
    flat, _obj, leaves = flatten(text)
    R = []

    def add(ok, short):
        R.append((bool(ok), short))
    cands = [x for x in leaves if "Sitamah" in x]
    flat = max(cands, key=len) if cands else flat
    plain = text_of(flat)
    sit = c.settings()["attach_by"] == "sitamah"
    add(plain.startswith("%s Sitamah," % greeting), "The message opens with the greeting '%s Sitamah,'" % greeting)
    add("<strong>Drafts</strong>" in flat and ("<strong>Action needed:</strong>" in flat if sit else "<strong>FYI:</strong>" in flat), "'%s' and 'Drafts' are bold (real <strong> tags)" % ("Action needed:" if sit else "FYI:"))
    add("**" not in flat and "&lt;" not in flat and "\\u003c" not in flat, "No literal ** and no escaped tags show")
    add(file in plain and ("%s > Comparative Quotes" % a["plan_folder"].strip()) in plain, "The message names the saved file and the folder (%s > Comparative Quotes)" % a["plan_folder"].strip())
    add(all(i in plain for i in c.distinct_insurers(a)) and c.wording()["basis_text"][scope["basis"]] in plain, "It names every insurer and the basis (%s)" % c.wording()["basis_text"][scope["basis"]])
    add(plain.rstrip().endswith("Thank you!"), "It ends with 'Thank you!'")
    return R


# ------------------------------------------------------------------ the confirmation table
GREETING_MARK = "<greeting by the clock>"


def table_rows(a, scope, docs, ev, today):
    wd = c.wording()
    ad = c.settings()["adviser"]
    st = scope
    rows = [("Client (greeting, full name)", "%s (%s)" % (a["client_full_name"], a["client_first_name"]), "the documents"),
            ("Client email (To)", a["client_email"], a["email_source"]),
            ("Basis", st["basis"], st["basis_source"]),
            ("Voice", "Paul's first person" if st["voice"] == "first_person" else "institutional third person", "your standing preference unless you say otherwise"),
            ("Sections (the Header, Key Facts Banner, salutation and signed closing are always included)", ", ".join(wd["section_titles"][x] for x in c.canonical_sections(st)), "the scope step")]
    for cat in c.CATEGORIES:
        cs = st["categories"][cat]
        rows.append(("Benefit scope: %s" % c.terms()["category_names"][cat], cs["status"].upper() + (" (Paul: %s)" % cs["paul_said"] if cs.get("paul_said") else ' - "%s"' % cs["evidence"][:90]), cs.get("source") or "Paul's words"))
    if st["second_life"]["present"]:
        rows.append(("Second life", st["second_life"]["name"], st["second_life"].get("source") or "Paul's words"))
    for i, s in enumerate(a["sides"]):
        sm = c.esc_summary(s)
        rows.append(("%s (%s, %s): premium and pattern" % (s["label"], s["role"], doc_word(s, docs)), "%s a month; %s%s; guarantee: %s" % (money(s["premium"]["monthly"]), pattern_text(s), " at %s" % pcs(s["escalation"]["rate"]) if s["escalation"].get("rate") else "",
                                                                                                       s["guarantee"].get("text") or "not stated"), "wording: \"%s\"" % s["escalation"]["evidence"][:100]))
        rows.append(("%s: covers" % s["label"], "; ".join("%s%s %s" % ("(second life) " if cv.get("life") == "second" else "", cv["label"], money(cv["amount"])) for cv in s["covers"]), "the document"))
        if s.get("projection"):
            rows.append(("%s: escalation" % s["label"], "%d years; average %s%% a year (%s)" % (sm["years"], c.pct_str(sm["avg"]) if sm["avg"] is not None else "-", sm["mode"] or "-"), "the document's projection table"))
        if s.get("loyalty"):
            rows.append(("%s: loyalty" % s["label"], "%s %s - %s" % (s["loyalty"]["name"], s["loyalty"]["amount_or_pct"], s["loyalty"]["when"]), "the document"))
    for f in a["features"]:
        rows.append(("Statement (%s, %s)" % (f["side"], f["basis"]), "%s%s%s" % (f["text"], " [%s]" % ("%s wins" % f["side"] if f["badge"] == "wins" else "fair trade-off") if f.get("badge") else "", " [exclusive: checked against every other insurer]" if f.get("exclusive") else ""),
                     (f.get("source") or "inference: shown as 'to be confirmed'")))
    for d in a["definitions"] or []:
        rows.append(("Definition (%s)" % d["side"], "%s: %s - %s" % (terms_name(d["category"]), d["set"], d.get("note") or ""), d.get("source") or "inference"))
    rows.append(("Key Facts Banner", a["banner"], "the chat's words: your judgement"))
    for v in a["verdict"] or []:
        rows.append(("Verdict point", "%s %s" % (v["headline"], v["detail"]), "the chat's words: your judgement"))
    rows += [("Covering email: opening and findings", " / ".join([a["email"]["opening"]] + a["email"]["bullets"]), "the chat's words"),
             ("Subject", c.subject(a), "built by the program"), ("Cc", "%s (%s)" % (c.CC_NAME, c.CC_EMAIL), "fixed"),
             ("Closing contact details in the letter", "WhatsApp %s, Office %s, Email %s" % (ad["whatsapp"], ad["office"], ad["email"]), "your signature (assets/settings.json)"),
             ("Signature in the Outlook draft", "added once by the Exchange rule when the email is sent; Claude types none", "paul-email-signature"),
             ("Attachment", "the saved HTML letter is attached by %s" % ("you (Paul), by hand" if c.settings()["attach_by"] == "paul" else "Sitamah"), "assets/settings.json"),
             ("Client's folder for the saved letter", "%s > Comparative Quotes" % a["plan_folder"], "the client's file")]
    fl = c.paul_flags(a, st, docs, ev, today)
    own = len(a.get("flags") or [])
    rows += [("Flag", x, "the chat" if i >= len(fl) - own else "the program") for i, x in enumerate(fl)]
    rows.append(("Teams message to Sitamah (sent only after the draft is checked; the greeting is set by the clock when it is sent)", teams_text(a, st, docs, GREETING_MARK, "<file name built by the program>"), "fixed wording"))
    return rows
