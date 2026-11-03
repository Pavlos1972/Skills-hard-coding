#!/usr/bin/env python3
"""Builds the Fact Find Summary content (nine fixed sections) from the Fact Find that ffread.py read. A pure function: the same Fact Find
always gives the same content.json, so the checker can recompose it and refuse a hand-edited file.

  compose.py <run_dir>

Rules built in (Paul): the nine sections and their order stay (28/10/2026); Section 8 sub-headings are fixed (15/10/2026); ABIs are the
standing ones, Dread Disease 3% (02/11/2026); every total is recomputed from its parts to the cent and debt is never left out because of
credit life; every flag of the Fact Find is carried into "Items Requiring Follow-Up"; the owner of an item comes from the routing list
(Cameron: short-term, CL: Will, Valerie: medical aid, Lizelle: gross income / ACI - Paul, 03/11/2026); nothing is invented.
"""
import os
import re
import sys
from decimal import Decimal

import wrlib as w

TITLES = ["Client Profile", "Occupation & Income", "Current Financial Arrangements", "Debt", "Children & Childcare", "Health",
          "What the Client Requires", "Action Plan — Cover Calculations", "Items Requiring Follow-Up"]
SEC8_HEADINGS = [("Life cover: fractured cover", "Life Cover - Fractured Cover"), ("Life cover: standard", "Standard Life Cover"),
                 ("Permanent disability: fractured cover", "Disability Cover - Fractured Cover"), ("Permanent disability: standard", "Standard Permanent Disability"),
                 ("Dread disease", "Dread Disease Cover"), ("Dread disease: standard", "Dread Disease Cover - Standard"),
                 ("Income protection / sickness benefit", "Income Protection / Sickness Benefit Cover"),
                 ("Income protection: standard", "Income Protection / Sickness Benefit Cover - Standard")]
# Standing ABIs (SKILL-STANDARDS.md): (Fact Find sub-heading, label, value)
STANDING_ABI = [("Life cover: fractured cover", "Life Cover (WOL) ABI", "3%"), ("Life cover: fractured cover", "Childcare ABI", "5%"),
                ("Permanent disability: fractured cover", "Household needs ABI", "5%"), ("Permanent disability: fractured cover", "Childcare ABI", "5%"),
                ("Dread disease", "ABI value", "3%"), ("Dread disease: standard", "ABI value", "3%")]
FORBIDDEN = [("Permanent disability: fractured cover", "Life Cover (WOL) ABI")]
ALWAYS = {"ID / passport number", "Cell number", "Work number", "Personal email", "Work email", "Referral from"}   # Paul's 'always include' list
BLANKS = ("not discussed", "n/a", "")
# which Fact Find blocks feed which owner (Paul, 03/11/2026)
OWNER_BY_SUB = {"Will": "CL", "Medical aid": "Valerie", "Gap cover": "Valerie", "Short-term insurance": "Cameron"}


class FF:
    def __init__(self, d):
        self.d = d
        self.secs = {s["num"]: s for s in d["sections"]}

    def blocks(self, num):
        return self.secs[num]["blocks"] if num in self.secs else []

    def block(self, num, sub):
        return next((b for b in self.blocks(num) if b["sub"] == sub), None)

    def row(self, num, sub, label):
        b = self.block(num, sub)
        return next((r for r in b["rows"] if r["label"] == label), None) if b else None

    def val(self, num, sub, label):
        r = self.row(num, sub, label)
        return " ".join(r["values"]) if r and r["values"] else ""

    def sub_of_label(self, num, label):
        for b in self.blocks(num):
            for r in b["rows"]:
                if r["label"] == label:
                    return b["sub"], r
        return None, None

    def closing_rows(self):
        c = self.d.get("closing")
        return [r for b in c["blocks"] for r in b["rows"]] if c else []


def blank(row):
    return not row["values"] or w.norm(" ".join(row["values"])) in BLANKS


def src(num, sub, label):
    return {"sec": num, "sub": sub, "label": label}


def copy_row(num, sub, row, label=None):
    return {"label": label or row["label"], "values": list(row["values"]), "flags": list(row["flags"]), "bullets": row["bullets"],
            "src": [src(num, sub, row["label"])]}


class Builder:
    def __init__(self, ff):
        self.ff = ff
        self.left_out = []
        self.problems = []

    def take(self, num, sub, drop_blank=True, labels=None, keep_zero=True):
        """Rows of one Fact Find block -> Summary rows. Rows that say 'Not discussed' / 'N/A' are left out (and counted) unless they are on Paul's always-include list."""
        b = self.ff.block(num, sub)
        out = []
        for r in (b["rows"] if b else []):
            if labels and r["label"] not in labels:
                continue
            if drop_blank and blank(r) and r["label"] not in ALWAYS:
                self.left_out.append({"sec": num, "sub": sub, "label": r["label"], "value": " ".join(r["values"]) or "(empty)"})
                continue
            if not keep_zero and w.norm(" ".join(r["values"])) in ("0", "0%"):
                self.left_out.append({"sec": num, "sub": sub, "label": r["label"], "value": " ".join(r["values"])})
                continue
            out.append(copy_row(num, sub, r))
        return out

    def blk(self, sub, rows, level=3):
        return {"sub": sub, "level": level, "rows": rows}

    # ---------------------------------------------------------------- the nine sections
    def s1(self):
        ff = self.ff
        rows = []
        nm, sn = ff.row(1, "Client", "Name"), ff.row(1, "Client", "Surname")
        if nm and sn:
            rows.append({"label": "Name & Surname", "values": [" ".join(nm["values"] + sn["values"])], "flags": nm["flags"] + sn["flags"], "bullets": False,
                         "src": [src(1, "Client", "Name"), src(1, "Client", "Surname")]})
        for sub, labels in (("Client", ["Date of birth", "Age", "ID / passport number", "Nationality"]),
                            ("Contact details", ["Cell number", "Work number", "Personal email", "Work email"]),
                            ("Meeting", ["Referral from", "Type of meeting"]),
                            ("Background", ["Smoker", "Highest education"])):
            for lab in labels:
                r = ff.row(1, sub, lab)
                if r is None:
                    continue
                if blank(r) and lab not in ALWAYS:
                    self.left_out.append({"sec": 1, "sub": sub, "label": lab, "value": " ".join(r["values"]) or "(empty)"})
                    continue
                rows.append(copy_row(1, sub, r))
        r = ff.row(3, "Household", "Marital status")
        if r and not blank(r):
            rows.append(copy_row(3, "Household", r))
        return [self.blk(None, rows)]

    def s2(self):
        blocks = []
        occ = self.take(2, "Work") + self.take(2, "Business")
        if occ:
            blocks.append(self.blk("Occupation", occ))
        d = self.take(2, "Duties split (percentages)", keep_zero=False) + self.take(2, "Duties")
        if d:
            blocks.append(self.blk("Occupational duties", d))
        inc = self.take(3, "Income")
        if inc:
            blocks.append(self.blk("Income", inc))
        return blocks

    def s3(self):
        blocks = []
        groups = (("Risk Cover & Retirement", 4), ("Investments & Savings", 5), ("Medical, Legal & Short-Term Insurance", 6))
        for title, num in groups:
            inner = []
            for b in self.ff.blocks(num):
                rows = self.take(num, b["sub"])
                if rows:
                    inner.append(self.blk(b["sub"], rows))
            if inner:
                blocks.append(self.blk(title, [], level=2))
                blocks += inner
        return blocks

    def _list_section(self, num, marker, totals_labels, parts, title_total="Totals"):
        """Debts / children: copy each item block, then recompute the totals from the item rows (to the cent)."""
        blocks, sums = [], [Decimal("0.00")] * len(parts)
        seen = False
        for b in self.ff.blocks(num):
            if any(r["label"] == marker for r in b["rows"]):
                seen = True
                rows = self.take(num, b["sub"])
                blocks.append(self.blk(b["sub"], rows))
                for i, lab in enumerate(parts):
                    r = next((x for x in b["rows"] if x["label"] == lab), None)
                    amt = w.parse_money(" ".join(r["values"])) if r and r["values"] else None
                    if r and r["values"] and amt is None and w.norm(" ".join(r["values"])) not in BLANKS:
                        self.problems.append("%s: %s %r is not an amount" % (b["sub"], lab, " ".join(r["values"])))
                    sums[i] += amt or Decimal("0.00")
        notes = next((b for b in self.ff.blocks(num) if b["sub"].lower().endswith("notes")), None)
        trows = []
        for i, tl in enumerate(totals_labels):
            terms = [{"sec": num, "sub": b["sub"], "label": parts[i]} for b in self.ff.blocks(num) if any(r["label"] == marker for r in b["rows"])]
            trows.append({"label": tl, "values": [w.fmt_money(sums[i])], "flags": [], "bullets": False, "src": terms, "computed": "sum", "amount": str(sums[i])})
        if seen:
            blocks.append(self.blk(title_total, trows))
        if notes:
            nr = self.take(num, notes["sub"])
            if nr:
                blocks.append(self.blk("Notes", nr))
        return blocks, sums

    def s4(self):
        blocks, sums = self._list_section(7, "Monthly instalment", ["Total monthly repayments", "Total liabilities (balances)", "Total asset value"],
                                          ["Monthly instalment", "Outstanding balance", "Asset value"])
        self.debts = sums
        return blocks

    def s5(self):
        blocks, sums = self._list_section(8, "Monthly cost", ["Total childcare (monthly)"], ["Monthly cost"])
        self.kids = sums
        return blocks

    def s6(self):
        rows = self.take(9, "Health")
        return [self.blk("Health", rows)] if rows else []

    def s7(self):
        ff = self.ff
        blocks = []
        risk = [("Personal risk quotes"), ("Reduced quotes (bf)"), ("Reduced quotes"), ("Retirement & investment quotes"), ("Retirement annuity quotes"), ("Investment quotes")]
        inner = []
        for sub in risk:
            rows = self.take(10, sub)
            if rows:
                inner.append(self.blk(sub, rows))
        if inner:
            blocks.append(self.blk("Personal Risk Cover & Retirement", [], level=2))
            blocks += inner
        inner = []
        for sub in ("Referrals & documents", "Credit life", "Business assurance", "Key man", "Documents to request", "Priorities"):
            rows = self.take(10, sub)
            if rows:
                inner.append(self.blk(sub, rows))
        if inner:
            blocks.append(self.blk("Investment & Insurance Needs", [], level=2))
            blocks += inner
        return blocks

    def s8(self):
        blocks = []
        for sub, title in SEC8_HEADINGS:
            b = self.ff.block(11, sub)
            if b:
                blocks.append(self.blk(title, [copy_row(11, sub, r) for r in b["rows"]]))
        nb = self.ff.block(11, "Risk calculation notes")
        if nb:
            blocks.append(self.blk("Notes", [copy_row(11, "Risk calculation notes", r) for r in nb["rows"]]))
        return blocks

    # ---------------------------------------------------------------- Items Requiring Follow-Up
    def s9(self):
        ff = self.ff
        items = []

        def add(text, owner=None, rule="rule", srcs=None):
            items.append({"text": text, "owner": owner, "rule": rule, "src": srcs or []})

        title_of = {s["num"]: s["title"] for s in ff.d["sections"]}
        for s in ff.d["sections"]:
            for b in s["blocks"]:
                for r in b["rows"]:
                    for f in r["flags"]:
                        owner = OWNER_BY_SUB.get(b["sub"]) or ("Lizelle" if (s["num"] == 11 and "ACI" in r["label"]) or r["label"] == "Gross monthly income" else None)
                        add("%s – %s: %s" % (title_of[s["num"]], r["label"], f), owner, "flag", [src(s["num"], b["sub"], r["label"])])
        for r in ff.closing_rows():
            for f in r["flags"]:
                add("Next Steps – %s: %s" % (r["label"], f), None, "flag", [{"sec": 0, "sub": "", "label": r["label"]}])
        # rules from the Fact Find's own rows
        aci = [(b["sub"], r) for b in ff.blocks(11) for r in b["rows"] if "ACI" in r["label"] and "pending" in w.norm(" ".join(r["values"]))]
        if aci:
            add("ACI values still pending the FNA (%d fields in Section 8)" % len(aci), "Lizelle", "aci", [src(11, sb, r["label"]) for sb, r in aci])
        gross = ff.row(3, "Income", "Gross monthly income")
        if gross is not None and blank(gross):
            add("Gross monthly income not confirmed", "Lizelle", "gross", [src(3, "Income", "Gross monthly income")])
        for sub, label, text, owner in (("Will", "Has a will", "Will missing", "CL"), ("Will", "Will up to date", "Will not up to date", "CL"),
                                        ("Medical aid", "Has medical aid", "No medical aid on record", "Valerie"),
                                        ("Gap cover", "Has gap cover", "No gap cover on record", "Valerie"),
                                        ("Short-term insurance", "Has short-term insurance", "No short-term insurance on record", "Cameron")):
            if w.norm(ff.val(6, sub, label)) == "no":
                add(text, owner, "gate", [src(6, sub, label)])
        if w.norm(ff.val(4, "Retirement annuity", "Has retirement annuity")) == "no" and w.norm(ff.val(4, "Pension / provident fund", "Has pension / provident fund")) == "no":
            add("No retirement funding on record (no retirement annuity, no pension or provident fund)", None, "retirement",
                [src(4, "Retirement annuity", "Has retirement annuity"), src(4, "Pension / provident fund", "Has pension / provident fund")])
        if w.norm(ff.val(2, "Work", "Business owner")) == "yes":
            gaps = [r["label"] for r in (ff.block(2, "Business") or {"rows": []})["rows"] if blank(r)]
            if gaps:
                add("Business ownership details incomplete: %s" % ", ".join(gaps), None, "business", [src(2, "Business", g) for g in gaps])
        for r in (ff.block(10, "Documents to request") or {"rows": []})["rows"]:
            if not blank(r):
                add("Document to request: %s" % " ".join(r["values"]), None, "document", [src(10, "Documents to request", r["label"])])
        cl = {x["label"]: x for x in ff.closing_rows()}
        if "Letter of authority" in cl and not blank(cl["Letter of authority"]):
            add("Letter of authority: %s" % " ".join(cl["Letter of authority"]["values"]), None, "next", [{"sec": 0, "sub": "", "label": "Letter of authority"}])
        appt = [cl[k] for k in ("Next appointment", "Day", "Time") if k in cl and not blank(cl[k])]
        if appt:
            first = " ".join(appt[0]["values"]) if appt[0]["label"] == "Next appointment" else ""
            rest = " ".join("(%s)" % " ".join(a["values"]) if a["label"] == "Day" else " ".join(a["values"]) for a in appt if a["label"] != "Next appointment")
            add("Next appointment: %s" % " ".join(x for x in (first, rest) if x), None, "next", [{"sec": 0, "sub": "", "label": a["label"]} for a in appt])
        if "Next steps for the client" in cl and not blank(cl["Next steps for the client"]):
            add("Next steps for the client: %s" % " ".join(cl["Next steps for the client"]["values"]), None, "next", [{"sec": 0, "sub": "", "label": "Next steps for the client"}])
        # the Fact Find's own differences in a total are never explained away
        for p in self.problems:
            add("Cannot be added up: %s" % p, None, "problem")
        rows = []
        for it in items:
            rows.append({"label": "", "values": [it["text"] + ("   [Owner: %s]" % it["owner"] if it["owner"] else "")], "flags": [], "bullets": True,
                         "src": it["src"], "item": {"owner": it["owner"], "rule": it["rule"], "text": it["text"]}})
        return [self.blk(None, rows)]


def compose(ffd, run):
    """ffd: the dict from ffread.read_pdf; run: {'client': {first, surname}, 'date', 'joint': name or None}."""
    ff = FF(ffd)
    B = Builder(ff)
    secs = []
    for i, fn in enumerate((B.s1, B.s2, B.s3, B.s4, B.s5, B.s6, B.s7, B.s8, B.s9)):
        secs.append({"num": i + 1, "title": TITLES[i], "blocks": fn()})
    date = ff.val(1, "Meeting", "Date completed") or ffd.get("meeting_date") or run.get("date")
    first, surname = ff.val(1, "Client", "Name"), ff.val(1, "Client", "Surname")
    content = {"version": 1, "title": "Client Fact Find Summary", "advisor": w.ADVISOR,
               "client": {"first": first, "surname": surname}, "date_completed": date,
               "joint": run.get("joint"), "file_name": w.output_name(first, surname, date),
               "sections": secs, "left_out": B.left_out, "problems": B.problems,
               "totals": {"debts_monthly": str(B.debts[0]), "debts_balances": str(B.debts[1]), "debts_assets": str(B.debts[2]), "kids_monthly": str(B.kids[0])}}
    return content


def main():
    run = os.path.abspath(sys.argv[1])
    rj = w.load_json(os.path.join(run, w.RUN))
    ffd = w.load_json(os.path.join(run, w.FACTFIND), "fact_find.json (run read first)")
    content = compose(ffd, rj)
    w.save_json(os.path.join(run, w.CONTENT), content)
    n = sum(len(b["rows"]) for s in content["sections"] for b in s["blocks"])
    fu = [r for r in content["sections"][8]["blocks"][0]["rows"]]
    print("COMPOSED %d rows in 9 sections; %d rows left out (Not discussed / N/A / 0%%); %d follow-up items; file name: %s"
          % (n, len(content["left_out"]), len(fu), content["file_name"]))
    for p in content["problems"]:
        print("PROBLEM:", p)


if __name__ == "__main__":
    main()
