"""Rebuilds, from the run folder, everything the program is responsible for: the entries of the raw notes, the duplicate candidates, the checks on the record,
the Markdown and its file name. run.py uses it to build, verify.py REBUILDS and compares, so a file edited by hand cannot pass.
"""
import os
import re

import crn
import notes as N
import wrlib as w


def p(run, name):
    return os.path.join(run, name)


def load_notes(run):
    meta = w.load_opt(p(run, w.NOTES), None)
    if meta is None:
        return None, "", [], False
    with open(p(run, meta["text_file"]), encoding="utf-8") as f:
        raw = f.read()
    entries, recognised = N.split_entries(raw)
    return meta, raw, entries, recognised


def load_earlier(run):
    out = []
    for e in w.load_opt(p(run, "earlier.json"), []):
        path = p(run, e["file"])
        with open(path, encoding="utf-8") as f:
            text = f.read()
        m1 = re.search(r"\*\*Full Name:\*\*\s*\n(.+)", text)
        m2 = re.search(r"\*\*Client ID No:\*\*\s*\n(.+)", text)
        out.append({"id": e["id"], "file": e["file"], "name": e["name"], "text": text, "full_name": m1.group(1).strip() if m1 else "", "id_no": m2.group(1).strip() if m2 else ""})
    return out


def route_order_problems(log):
    bad, failed = [], {}
    for e in log:
        if e["route"] not in w.ROUTES:
            continue
        pur = e.get("purpose", "notes")
        f = failed.setdefault(pur, set())
        i = w.ROUTES.index(e["route"])
        if any(r not in f for r in w.ROUTES[:i]):
            bad.append("%s (%s)" % (e["route"], pur))
        if e["result"] == "failed":
            f.add(e["route"])
    return bad


def duplicates(rj, raw, earlier):
    """Earlier records of the same client: the same name as Paul named, or an ID number that appears in the raw notes."""
    want = w.norm("%s %s" % (rj["client"]["first"], rj["client"]["surname"]))
    ids = {m.group(0) for m in re.finditer(r"\b\d{13}\b", raw)}
    out = []
    for e in earlier:
        if (e["full_name"] and w.norm(e["full_name"]) == want) or (w.norm(e["name"]) == want) or (w.digits(e["id_no"]) in ids and w.digits(e["id_no"])):
            out.append(e)
    return out


def file_name(rj):
    s = crn.settings()
    return w.safe_filename(s["file_name"].format(date=w.today().strftime("%d.%m.%y"), first=rj["client"]["first"], surname=rj["client"]["surname"]))


def compute(run):
    rj = w.load_json(p(run, w.RUN))
    st = w.load_opt(p(run, w.STATE), {})
    meta, raw, entries, recognised = load_notes(run)
    earlier = load_earlier(run)
    out = {"rj": rj, "st": st, "meta": meta, "raw": raw, "entries": entries, "recognised": recognised, "earlier": earlier, "dups": [], "record": None, "chk": None,
           "md": None, "file_name": file_name(rj), "problems": [], "tokens": 0}
    if meta is None:
        return out
    out["dups"] = duplicates(rj, raw, earlier)
    stop = crn.settings()["name_stop"]
    out["tokens"] = sum(len(v) for e in entries for v in N.tokens(e["text"], stop).values())
    rec = w.load_opt(p(run, w.RECORD), None)
    out["record"] = rec
    if rec is None:
        return out
    decision = (st.get("duplicate") or {}).get("decision")
    chk = crn.check(rec, raw, entries, recognised, out["dups"], decision)
    f = (rec.get("fields") or {})
    rec_name = w.norm("%s %s" % (f.get("First Name") or "", f.get("Last Name") or ""))
    if rec_name.strip() and rec_name != w.norm("%s %s" % (rj["client"]["first"], rj["client"]["surname"])):
        chk["flags"].append("the record is for %s %s but Paul named %s %s" % (f.get("First Name"), f.get("Last Name"), rj["client"]["first"], rj["client"]["surname"]))
    out["chk"] = chk
    out["problems"] = list(chk["problems"])
    if not out["problems"]:
        out["md"] = crn.render(rec, raw, entries, chk)
        out["problems"] += crn.layout_problems(out["md"])
        if decision == "merge":
            out["problems"] += crn.merge_lost(out["md"], out["dups"], chk["left_out"])
        if out["problems"]:
            out["md"] = None
    return out
