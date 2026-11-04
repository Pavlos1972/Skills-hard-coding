#!/usr/bin/env python3
"""The one checker of the client-review-notes.

  verify.py <run_dir> [pre|final] [--full]

It REBUILDS the entries, the checks and the Markdown from the run folder, so nothing is taken on trust from a file Claude could have edited. The reply to Paul
carries the SHORT AUDIT it prints: one line per check with a green tick or a red cross, and one closing line for what is only attested (Paul, 03/11/2026).
The full record is written to out_record/audit-full.txt (--full prints it).
"""
import os
import sys

import crn
import engine as eng
import notes as N
import wrlib as w

OK, BAD = "✅", "❌"
STEP_IDS = ["source", "read", "duplicates", "record", "deliver", "final"]


class Results:
    def __init__(self):
        self.rows, self.attested, self.group = [], [], ""

    def add(self, ok, short, detail=""):
        self.rows.append((OK if ok else BAD, short, detail, self.group))

    @property
    def fails(self):
        return [r for r in self.rows if r[0] == BAD]


def _read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def run_checks(run, stage):
    R = Results()
    rj = w.load_json(os.path.join(run, w.RUN))
    st = w.load_opt(os.path.join(run, w.STATE), {})
    rc = w.load_opt(os.path.join(run, w.RECEIPT), {})
    log = w.load_opt(os.path.join(run, w.ACCESS), [])
    c = eng.compute(run)
    meta = c["meta"]
    # ---------------------------------------------------------------- source
    R.group = "source"
    if meta is None:
        R.add(False, "The raw notes are not registered yet", "step 'source': run.py notes")
    else:
        sha_ok = w.sha256_file(os.path.join(run, meta["text_file"])) == meta["sha"]
        bad = eng.route_order_problems(log)
        logged = meta["route"] == "pasted" or any(e["route"] == meta["route"] and e["result"] == "found" and e.get("purpose") == "notes" for e in log)
        ear_bad = [e["id"] for e in c["earlier"] if w.sha256_file(os.path.join(run, e["file"])) != next(x["sha"] for x in w.load_opt(os.path.join(run, "earlier.json"), []) if x["id"] == e["id"])]
        ok = sha_ok and logged and not bad and not ear_bad
        dated = len([e for e in c["entries"] if e["key"]])
        R.add(ok, "The raw notes are the only source (%s, %d characters, %s), unchanged%s; %s" % (
            meta["name"], meta["chars"], "pasted by Paul" if meta["route"] == "pasted" else "found by the %s route and logged in order" % meta["route"],
            ("; %d earlier record(s) registered" % len(c["earlier"])) if c["earlier"] else "",
            ("%d dated entries recognised, coverage is checked entry by entry" % dated) if c["recognised"] else "NO dated entries recognised: coverage is checked over the whole note (weaker)") if ok else
            "Source problem: %s" % ("the notes file changed" if not sha_ok else "no access try logged" if not logged else "routes out of order: %s" % ", ".join(bad) if bad else "an earlier record changed"))
        if not c["recognised"]:
            R.attested.append("that no fact was lost entry by entry (the notes carry no recognisable dates, so only the whole note was compared)")
    # ---------------------------------------------------------------- read
    R.group = "read"
    parts = N.parts(c["raw"], crn.settings()["entry_part_chars"]) if meta else []
    acked = (st.get("read") or {}).get("acked") or {}
    R.add(bool(meta) and len(acked) == len(parts) and bool(parts), "All %d part(s) of the raw notes were served in order and acknowledged" % len(parts) if meta and len(acked) == len(parts) else "The raw notes have not all been read and acknowledged (run.py read)")
    # ---------------------------------------------------------------- duplicates
    R.group = "duplicates"
    dec = st.get("duplicate") or {}
    if meta is None:
        R.add(False, "Duplicates cannot be checked before the notes are registered")
    elif not c["dups"]:
        R.add(True, "No earlier record of this client was given (%d checked): nothing to merge" % len(c["earlier"]) if c["earlier"] else "No earlier record was given: nothing to merge")
    else:
        okd = dec.get("decision") in ("merge", "separate") and len((dec.get("said") or "").strip()) >= 5 and set(dec.get("ids") or []) == {d["id"] for d in c["dups"]}
        R.add(okd, "%d earlier record(s) match this client; Paul decided to %s in his own words" % (len(c["dups"]), dec.get("decision")) if okd else "An earlier record matches this client: show both to Paul and record his decision (run.py duplicate)")
    # ---------------------------------------------------------------- record
    R.group = "record"
    if c["record"] is None:
        R.add(False, "The record has not been entered yet", "step 'record': run.py record")
    else:
        ch = c["chk"]
        pr = c["problems"]
        R.add(not pr, "The record follows every rule: the 18 fields in the fixed order, Not recorded. where the source is silent, the layout, no HTML, notes oldest first" if not pr else "Record problem: %s" % pr[0], "; ".join(pr))
        if not pr:
            nver = sum(1 for k in crn.settings()["must_appear"] if (c["record"].get("fields") or {}).get(k)) + sum(len(g) for g in ((c["record"].get("fields") or {}).get("Life & Investments") or {}).values()) * 4 + sum(len(x.get("lines") or []) + 1 for x in (c["record"].get("fields") or {}).get("Commission") or [])
            R.add(True, "Every verbatim item (names, categories, ID, tax number, each policy's contract, product, DOC date, premium and status, each commission line) is character for character in the raw notes")
            R.add(True, "Every date, amount, percentage, number, contract-like code, email, link, name and abbreviation of %d raw entr%s (%d items) is in the record%s" % (
                len(c["entries"]), "y" if len(c["entries"]) == 1 else "ies", c["tokens"], (", except %d listed as left out with a reason" % len(ch["left_out"])) if ch["left_out"] else ""))
            R.add(True, "%d 'do not contact' line(s) found in the raw notes and reproduced in full, flagged at the top of Notes" % len(ch["dnc"]) if ch["dnc"] else "No 'do not contact' line is in the raw notes")
            R.add(True, "%d flag(s) found in the raw notes are shown at the top of Notes: %s" % (len(ch["flags"]), "; ".join(ch["flags"])[:160]) if ch["flags"] else "No flag was found in the raw notes (typos, odd IDs, system timestamps)")
            R.add(True, "No abbreviation was expanded (the glossary rule)")
            md_path = os.path.join(run, w.OUT, c["file_name"])
            md = _read(md_path)
            R.add(md == c["md"], "The Markdown file is exactly what the program draws from the record (not edited by hand)" if md == c["md"] else "out/%s is missing or is not what the program draws" % c["file_name"])
    # ---------------------------------------------------------------- deliver
    R.group = "deliver"
    okc = (rc.get("chat.sent") or "").strip() != ""
    R.add(okc and c["md"] is not None, "%s was sent in the chat as a downloadable .md file (the file is the deliverable)" % c["file_name"] if okc else "The file is not recorded as sent in the chat (receipt chat.sent)")
    if (rc.get("save.paul_said") or "").strip():
        R.add(bool((st.get("save") or {}).get("ok")) and bool((rc.get("save.folder") or "").strip()), "A copy was saved in the client's folder because Paul asked, and the listing shows it" if (st.get("save") or {}).get("ok") else "Paul asked for a copy in the client's folder but the listing does not show it")
    if stage == "final":
        R.group = "final"
        done = [s for s in STEP_IDS[:-1] if (rj.get("steps", {}).get(s) or {}).get("state") == "done"]
        fpok = rj.get("program_fingerprint") == w.program_fingerprint()
        R.add(done == STEP_IDS[:-1] and fpok, "Every step done in order (%d of %d) and the programs did not change during the run" % (len(done), len(STEP_IDS) - 1) if done == STEP_IDS[:-1] and fpok else
              "Steps done: %s%s" % (", ".join(done) or "none", "; the programs changed during the run" if not fpok else ""))
        R.attested += ["that each summarised sentence keeps its MEANING (the program proves the figures, dates, names and links are kept, not the wording)", "that the Outlook notes are complete and right",
                       "that the chat really sent the file (the program checks the receipt)"]
    return R, rj


def print_audit(R, rj, stage, run, full=False):
    lines = ["AUDIT   %s" % w.version_line()]
    for mark, short, detail, _g in R.rows:
        lines.append("%s %s" % (mark, crn.mask_text(short)))
    if R.attested:
        lines.append("Only attested (not proven): " + "; ".join(dict.fromkeys(R.attested)) + ".")
    ok = len([r for r in R.rows if r[0] == OK])
    bad = len(R.fails)
    lines.append("RESULT: %s   (%d %s, %d %s)" % ("PASS" if not bad else "FAIL", ok, OK, bad, BAD))
    text = "\n".join(lines)
    print(text)
    fulltext = text + "\n\nFULL RECORD\n" + "\n".join("%s %s\n    %s" % (m, crn.mask_text(s), crn.mask_text(d)) for m, s, d, _g in R.rows if d)
    try:
        os.makedirs(os.path.join(run, w.OUT + "_record"), exist_ok=True)
        with open(os.path.join(run, w.OUT + "_record", "audit-full.txt"), "w", encoding="utf-8") as f:
            f.write(fulltext + "\n")
    except OSError:
        pass
    if full:
        print("\n" + fulltext.split("FULL RECORD", 1)[1])
    return not bad


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    run = os.path.abspath(args[0])
    stage = args[1] if len(args) > 1 and args[1] in ("pre", "final") else "final"
    R, rj = run_checks(run, stage)
    ok = print_audit(R, rj, stage, run, full="--full" in sys.argv)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
