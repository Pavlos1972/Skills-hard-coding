#!/usr/bin/env python3
"""The one checker of the client-transcript-download skill.

  verify.py <run_dir> [pre|final] [--full]

It re-reads the received transcript and the built .docx itself, so nothing is taken on trust from a file Claude could have edited.
The reply to Paul carries the SHORT AUDIT it prints: one line per check with a green tick or a red cross, one closing line for what is only
attested, and one line saying which skill comes next (Paul, 03/11/2026). The full record is written to out/audit-full.txt (--full prints it).
"""
import os
import re
import sys

import trread as tr
import wrlib as w

OK, BAD = "✅", "❌"
STEP_IDS = ["identify", "fetch", "check", "name", "save", "final"]


class Results:
    def __init__(self):
        self.rows, self.attested, self.group = [], [], ""

    def add(self, ok, short, detail=""):
        self.rows.append((OK if ok else BAD, short, detail, self.group))

    @property
    def fails(self):
        return [r for r in self.rows if r[0] == BAD]


def log_of(run, purpose):
    return [e for e in w.load_opt(os.path.join(run, w.ACCESS), []) if e.get("purpose", "fetch") == purpose]


def order_problem(log, routes):
    """A route may be used only after every earlier route has been tried and failed."""
    failed = set()
    for e in log:
        if e.get("route") not in routes:
            return "route %r is not one of %s" % (e.get("route"), ", ".join(routes))
        i = routes.index(e["route"])
        if any(r not in failed for r in routes[:i]):
            return "route %r was used before the earlier routes (%s) were tried and failed" % (e["route"], ", ".join(routes[:i]))
        if e.get("result") == "failed":
            failed.add(e["route"])
    return ""


def meeting_of(run):
    return w.load_opt(os.path.join(run, w.MEETING), None)


def source_path(run, rj):
    s = rj.get("source") or {}
    return os.path.join(run, s["file"]) if s.get("file") else None


def run_checks(run, stage):
    R = Results()
    rj = w.load_json(os.path.join(run, w.RUN))
    client = rj["client"]
    m = meeting_of(run)
    # A. the meeting
    R.group = "meeting"
    if not m or not m.get("title") or not m.get("length_s"):
        R.add(False, "The meeting is not identified yet (title, date and length are needed)", "step 'identify': run.py meeting")
    else:
        ok = m.get("date") == rj["date"]
        R.add(ok, 'Meeting identified: "%s", %s, length %s' % (m["title"], m["date"], w.fmt_hms(m["length_s"])) if ok else
              "The meeting is dated %s but you asked for %s" % (m.get("date"), rj["date"]))
    # B. the fetch routes and the received file
    R.group = "fetch"
    flog = log_of(run, "fetch")
    prob = order_problem(flog, w.FETCH_ROUTES) if flog else "no fetch try is recorded"
    found = [e for e in flog if e.get("result") == "found"]
    src = rj.get("source") or {}
    R.add(not prob and bool(found) and src.get("route") == found[-1]["route"],
          "Fetch routes tried in order and logged (%s)" % (", ".join("%s %s" % (e["route"], e["result"]) for e in flog) or "none"), prob or "fetch log: %s" % flog)
    sp = source_path(run, rj)
    have = bool(sp) and os.path.exists(sp)
    R.add(have and os.path.getsize(sp) == src.get("size") and w.sha256_file(sp) == src.get("sha256"),
          "Transcript received through %s (%s bytes), fingerprint recorded%s" % (src.get("route"), src.get("size"), "; copy size equals the connector's" if src.get("size_checked") else "") if have else "The transcript has not been brought into the run folder (run.py source)")
    # C. the transcript itself, read by the program
    R.group = "transcript"
    a = None
    if have:
        kind, lines = tr.read_file(sp)
        a = tr.analyse(kind, lines, m)
        hp = tr.header_problems(a)
        R.add(not hp, "Header shows the meeting title and date (%s file)" % kind if not hp else "Header problem: " + hp[0], "; ".join(hp))
        cp = tr.completeness(a)
        comp = [p for p in cp if not p.startswith("gap")]
        gaps = [p for p in cp if p.startswith("gap")]
        length = a["length_s"] if a["length_s"] is not None else a["meeting_length_s"]
        R.add(not comp, "Complete: the last time stamp %s is within 2 minutes of the meeting length %s" % (w.fmt_hms(a["last_s"]), w.fmt_hms(length)) if not comp else
              "Not complete: " + comp[0], "; ".join(comp))
        R.add(not gaps, "No gap longer than 10 minutes between two time stamps (%d time stamps read)" % a["stamps"] if not gaps else "Gap in the transcript: " + gaps[0], "; ".join(gaps))
    # D. the built file
    R.group = "built"
    name = w.output_name(client["first"], client["surname"], rj["date"])
    out = os.path.join(run, w.OUT, name or "")
    outs = [f for f in os.listdir(os.path.join(run, w.OUT))] if os.path.isdir(os.path.join(run, w.OUT)) else []
    if stage == "final" or outs:
        built = bool(name) and os.path.exists(out) and outs == [name]
        good = False
        if built and a is not None:
            try:
                k2, l2 = tr.read_file(out)
                a2 = tr.analyse(k2, l2, m)
                good = k2 == "docx" and a2["stamps"] == a["stamps"] and a2["last_s"] == a["last_s"] and not tr.completeness(a2) and not tr.header_problems(a2)
                if a is not None and a["kind"] == "docx":
                    good = good and w.sha256_file(out) == w.sha256_file(sp)       # a .docx is copied, never rewritten
            except Exception:
                good = False
        R.add(built and good, "File name derived: %s; reads back as a .docx with the same time stamps and passes the same checks" % name if built and good else
              "The built file is missing, misnamed, altered or not a complete .docx (expected exactly one file: %s)" % name)
    if stage == "final":
        _final_checks(R, run, rj, client)
    return R, rj, m


def _final_checks(R, run, rj, client):
    R.group = "save"
    slog = log_of(run, "save")
    prob = order_problem(slog, w.SAVE_ROUTES) if slog else "no save try is recorded"
    asked = [e for e in slog if e.get("route") == "device" and e.get("result") == "failed" and "not connected" not in (e.get("note") or "").lower()]
    if asked and not prob:
        prob = "the computer try failed for a reason other than 'not connected; not requested' (a connection may have been requested, which is never allowed): %r" % asked[0].get("note")
    sfound = [e for e in slog if e.get("result") == "found"]
    sok = not prob and bool(sfound)
    R.add(sok, "Save routes tried in order and logged (%s)" % (", ".join("%s %s" % (e["route"], e["result"]) for e in slog) or "none") if sok else
          "Save routes problem: %s" % (prob or "no save try found the folder"), prob)
    rc = w.load_opt(os.path.join(run, w.RECEIPT), {})
    name = w.output_name(client["first"], client["surname"], rj["date"])
    out = os.path.join(run, w.OUT, name or "")
    size = os.path.getsize(out) if name and os.path.exists(out) else None
    folder = rc.get("save.folder", "")
    parts = [p.strip().lower() for p in re.split(r"[\\/]+", folder) if p.strip()]
    want = "%s, %s" % (client["surname"], client["first"])
    root_ok = ("company - paul" in parts[:5]) or ("company - wr clients" in parts[:5] and "paul kafentzis (client files)" in parts[:7])
    folder_ok = bool(parts) and parts[-1] == "2. fact find" and len(parts) > 1 and w.norm(want) == w.norm(parts[-2]) and root_ok
    size_ok = size is not None and str(rc.get("save.listed_bytes")) == str(size)
    fresh = rc.get("save.already_existed") == "no"
    ok = folder_ok and size_ok and fresh
    R.add(ok, "Saved as a COPY in the client's own 2. Fact Find folder, nothing overwritten; listed size equals the local file (%s bytes)" % size if ok else
          "Save not proven: %s" % "; ".join(x for x, bad in (("folder %r is not ...\\%s\\2. Fact Find under Company - Paul or Paul Kafentzis (Client Files)" % (folder, want), not folder_ok),
                                                          ("listed size %r vs local %r" % (rc.get("save.listed_bytes"), size), not size_ok),
                                                          ("a file with that name already existed or this was not recorded (save.already_existed)", not fresh)) if bad))
    done = [s for s in STEP_IDS[:-1] if (rj.get("steps", {}).get(s) or {}).get("state") == "done"]
    fp = rj.get("program_fingerprint") == w.program_fingerprint()
    R.add(done == STEP_IDS[:-1] and fp, "Every step done in order (%d of %d) and the programs did not change during the run" % (len(done), len(STEP_IDS) - 1)
          if done == STEP_IDS[:-1] and fp else "Steps done: %s%s" % (", ".join(done) or "none", "; the programs changed during the run" if not fp else ""))
    R.attested += ["what was seen in Chrome, and that text read from the Teams page is word for word (if the Chrome route was used)", "the folder save and its listing (typed by Claude)",
                   "that a downloaded original stays in Downloads for Paul to delete (only if the computer was already connected)"]


def next_line(rj):
    t = rj.get("type")
    if t == "first":
        return "Next: this was a first (Fact Find) meeting, so run `ff-population-transcript`, then `fact-find-summary`."
    if t == "follow-up":
        return "Next: this was a follow-up meeting, so run `client-teams-transcript-skill`."
    return "Next: a first (Fact Find) meeting goes to `ff-population-transcript` (then `fact-find-summary`), a follow-up to `client-teams-transcript-skill`: ask Paul which this was."


def print_audit(R, rj, stage, run, full=False):
    lines = ["AUDIT   %s" % w.version_line()]
    for mark, short, detail, _g in R.rows:
        lines.append("%s %s" % (mark, short))
    if R.attested:
        lines.append("Only attested (not proven): " + "; ".join(R.attested) + ".")
    if stage == "final":
        lines.append(next_line(rj))
    ok = len([r for r in R.rows if r[0] == OK])
    bad = len(R.fails)
    lines.append("RESULT: %s   (%d %s, %d %s)" % ("PASS" if not bad else "FAIL", ok, OK, bad, BAD))
    text = "\n".join(lines)
    print(text)
    fulltext = text + "\n\nFULL RECORD\n" + "\n".join("%s %s\n    %s" % (m, s, d) for m, s, d, _g in R.rows if d)
    try:
        os.makedirs(os.path.join(run, w.OUT + "_record"), exist_ok=True)       # kept outside out/ so the one deliverable stays alone there
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
    R, rj, m = run_checks(run, stage)
    ok = print_audit(R, rj, stage, run, full="--full" in sys.argv)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
