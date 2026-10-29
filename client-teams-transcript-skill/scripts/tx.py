#!/usr/bin/env python3
"""Reading lock for the transcript (Step 1, 1b of the skill).

  tx.py prep   <source.docx|.txt|.md> <run_dir> [--force] [--notes]
  tx.py chunk  <run_dir> <pass 1|2> <n>
  tx.py scan   <run_dir>
  tx.py status <run_dir>

prep    converts the source, checks it is complete, and plans the chunks.
chunk   prints one numbered chunk and logs the read. Chunks are served in order;
        Pass 2 is refused until Pass 1 has served every chunk.
scan    the keyword scan from Step 1b. Refused until both passes are done.
status  what has been read and what the next required step is.

The log proves each chunk was put in front of Claude, in order, twice. It cannot
prove the text was understood; the ledger and source-trace checks in verify.py
are what test that.
"""
import argparse
import os
import re
import subprocess
import sys

import wrlib as w

TOLERANCE_S = 120   # last timestamp may fall this far short of the stated duration
JUMP_S = 600        # a silent jump bigger than this is treated as a gap
CLOSING_FRACTION = 0.15
CLOSING_SECONDS = 600

TS_ARROW = re.compile(r"^\s*(\d{1,2}):(\d{1,2}):(\d{1,2})(?:[.,]\d+)?\s*-->")
TS_START = re.compile(r"^\s*(\d{1,2}):(\d{2})(?::(\d{2}))?(?:[.,]\d+)?(?!\d)")
# some Teams exports put the time after the speaker's name: "Paul Kafentzis   0:05". Only lines that look like a
# name count, so a spoken time such as "see you at 4:30" is never read as a timestamp.
NAME_WORD = r"(?:[A-Z][\w'\u2019-]*|van|de|der|den|la|le|du|di|von)"
TS_END = re.compile(r"^" + NAME_WORD + r"(?:\s+" + NAME_WORD + r"){0,4}\s+(\d{1,2}):(\d{2})(?::(\d{2}))?\s*$")
DURATION = re.compile(
    r"(?i)duration\W{0,5}(?:(\d+)\s*h\w*)?\s*(?:(\d+)\s*m\w*)?\s*(?:(\d+)\s*s\w*)?")
CLOSING = re.compile(r"(?i)stopped transcription|transcription stopped|stopped recording|meeting ended")

# Word lists from Step 1b item 5 of the skill. HIGH = decision/change/request words: every hit in the
# closing minutes must be covered by a ledger entry or a recorded review (verify.py fails otherwise).
# LOW = the rest of the skill's list (figures, days, products): reported, and warned about in the closing minutes.
HIGH_WORDS = [
    "change", "changed", "instead", "rather", "actually", "for now", "later",
    "keep it", "leave it", "get back to you", "in your name", "his name", "her name",
    "owner", "beneficiary", "payer", "address", "spell", "wrong", "correct", "sort that out", "tomorrow",
    "think about", "go ahead", "happy", "not happy", "agree", "decline", "cancel", "increase",
    "reduce", "put it in", "email", "send", "wife", "husband", "partner", "credit life", "retrench",
    "instalment", "installment", "protector", "cede", "ceded", "cession", "payback", "payout",
    "on hold", "hold off",
]
LOW_WORDS = ["bank", "bond", "card", "waiting period", "months", "pays", "covers", "date",
             "monday", "tuesday", "wednesday", "thursday", "friday"]
HIGH_RE = re.compile(r"\b(?:" + "|".join(re.escape(x) for x in HIGH_WORDS) + r")\w*", re.I)
LOW_RE = re.compile(r"\b(?:" + "|".join(re.escape(x) for x in LOW_WORDS) + r")\w*|\bR\s?\d|\brands?\b", re.I)


def ts_seconds(line):
    m = TS_ARROW.match(line)
    if m:
        return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
    m = TS_START.match(line) or TS_END.match(line)
    if not m:
        return None
    a, b, c = int(m.group(1)), int(m.group(2)), m.group(3)
    if c is None:                      # M:SS
        return a * 60 + b
    return a * 3600 + b * 60 + int(c)  # H:MM:SS


def fmt(sec):
    sec = int(sec)
    return "%d:%02d:%02d" % (sec // 3600, sec % 3600 // 60, sec % 60)


def read_source(path):
    if path.lower().endswith((".docx", ".doc", ".rtf", ".odt")):
        try:
            r = subprocess.run(["pandoc", "-t", "plain", "--wrap=none", path],
                               capture_output=True, text=True)
        except FileNotFoundError:
            w.die("STOP: pandoc is not installed, so a .docx transcript cannot be read. Tell Paul exactly this; do not summarise from anything else.", 4)
        if r.returncode:
            w.die("pandoc failed: " + r.stderr.strip())
        return r.stdout
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def plan_chunks(lines):
    """Greedy chunks of <= CHUNK_LINES lines / CHUNK_CHARS characters, ending at a blank
    line when one sits in the back half of the chunk (keeps a speaker with their words)."""
    chunks, start, chars = [], 1, 0
    for i, ln in enumerate(lines, 1):
        n = i - start + 1
        if n > w.CHUNK_LINES or (chars + len(ln) > w.CHUNK_CHARS and n > 1):
            end = i - 1
            for j in range(end, start + (end - start) // 2, -1):
                if not lines[j - 1].strip():
                    end = j
                    break
            chunks.append([start, end])
            start = end + 1
            chars = sum(len(x) + 8 for x in lines[start - 1:i])
            continue
        chars += len(ln) + 8
    chunks.append([start, len(lines)])
    return chunks


def load_state(run):
    return w.load_json(os.path.join(run, w.STATE), "state.json (run `tx.py prep` first)")


def cmd_prep(a):
    if not os.path.exists(a.source):
        w.die("Source not found: " + a.source)
    text = read_source(a.source).replace("\r\n", "\n").replace("\r", "\n")
    lines = [ln.rstrip() for ln in text.split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    if not lines:
        w.die("STOP: the source is empty.")
    os.makedirs(a.run, exist_ok=True)
    with open(os.path.join(a.run, w.TRANSCRIPT), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    raw = [(i, sec) for i, sec in ((i, ts_seconds(ln)) for i, ln in enumerate(lines, 1)) if sec is not None]
    stamps, top = [], -1
    for i, sec in raw:
        if sec >= top:
            stamps.append((i, sec))
            top = sec
    notes, complete = [], True
    last_ts = stamps[-1][1] if stamps else None
    dur = None
    for m in DURATION.finditer(text):
        h, mi, s = (int(x) if x else 0 for x in m.groups())
        if h or mi or s:
            dur = h * 3600 + mi * 60 + s
            break
    if not stamps:
        if a.notes:
            notes.append("WARN: notes or a recap, not a transcript: completeness cannot be checked, so tell Paul that.")
        else:
            complete = False
            notes.append("INCOMPLETE?: no timestamps could be read, so it cannot be checked that the transcript is complete. "
                         "Tell Paul what the file looks like (the first 15 lines) so the reader can be fixed. "
                         "If the source is notes or a recap use --notes; use --force only if Paul says to carry on.")
    else:
        if dur is not None and last_ts < dur - TOLERANCE_S:
            complete = False
            notes.append("INCOMPLETE: stated duration %s but the last timestamp is %s (%s missing)."
                         % (fmt(dur), fmt(last_ts), fmt(dur - last_ts)))
        elif dur is None:
            notes.append("WARN: no stated duration found; only the gap check was run.")
            if not [i for i, ln in enumerate(lines, 1) if CLOSING.search(ln)]:
                complete = False
                notes.append("INCOMPLETE?: the file states no total duration and has no closing marker ('stopped transcription'), "
                             "so it cannot be checked that the transcript reaches the end. Tell Paul; use --force only if he says to carry on.")
        for (i1, t1), (i2, t2) in zip(stamps, stamps[1:]):
            if t2 - t1 > JUMP_S:
                complete = False
                notes.append("GAP: %s between line %d (%s) and line %d (%s)."
                             % (fmt(t2 - t1), i1, fmt(t1), i2, fmt(t2)))
    closing = [i for i, ln in enumerate(lines, 1) if CLOSING.search(ln)]
    if not closing:
        notes.append("WARN: no closing marker ('stopped transcription') found near the end.")

    forced = False
    if not complete and a.force:
        forced, complete = True, True
        notes.append("FORCED past the warnings above (Paul told us to continue).")

    chunks = plan_chunks(lines)
    state = {
        "source": os.path.basename(a.source), "created": w.now(),
        "total_lines": len(lines), "sha256": w.sha256_text("\n".join(lines)),
        "chunks": chunks, "complete": complete, "forced": forced, "notes": notes,
        "first_ts": fmt(stamps[0][1]) if stamps else None,
        "last_ts": fmt(last_ts) if stamps else None,
        "stated_duration": fmt(dur) if dur is not None else None,
        "closing_marker_line": closing[-1] if closing else None,
        "reads": [], "scan": None, "build": None,
    }
    w.save_json(os.path.join(a.run, w.STATE), state)

    print("PREP  %s  ->  %s" % (a.source, a.run))
    print("  lines: %d   chunks: %d   timestamps: %s -> %s   stated duration: %s"
          % (len(lines), len(chunks), state["first_ts"], state["last_ts"], state["stated_duration"]))
    for n in notes:
        print("  " + n)
    if not complete:
        print("\nSTOP. Tell Paul exactly what is missing (above) and do not continue. "
              "Re-run with --force only if Paul says to carry on.")
        sys.exit(2)
    print("\nNEXT: read Pass 1, chunks 1..%d in order:  tx.py chunk %s 1 1" % (len(chunks), a.run))


def cmd_chunk(a):
    st = load_state(a.run)
    if not st["complete"]:
        w.die("STOP: the transcript is incomplete (see `tx.py status`).", 2)
    p, n, k = a.pass_, a.n, len(st["chunks"])
    if p not in (1, 2):
        w.die("pass must be 1 or 2")
    if not 1 <= n <= k:
        w.die("chunk must be 1..%d" % k)
    lines = w.read_lines(a.run)
    if w.sha256_text("\n".join(lines)) != st["sha256"]:
        w.die("STOP: transcript.txt changed since prep. Re-run prep.", 2)
    done = {r["chunk"] for r in st["reads"] if r["pass"] == p}
    if p == 2:
        missing = [c for c in range(1, k + 1) if c not in {r["chunk"] for r in st["reads"] if r["pass"] == 1}]
        if missing:
            w.die("REFUSED: Pass 2 cannot start until Pass 1 has read every chunk. "
                  "Pass 1 still needs: %s" % missing, 3)
    if n > 1 and (n - 1) not in done:
        w.die("REFUSED: read chunk %d of Pass %d first. Chunks are read in order, none skipped." % (n - 1, p), 3)
    led = load_ledger(a.run)
    if n > 1 and not chunk_acked(st, led, p, n - 1):
        w.die("REFUSED: chunk %d of Pass %d has no ledger entry and no acknowledgement. Record what it contains first "
              "(run.py ledger %s add ...), or say in your own words why it holds no decisions, requests or figures: "
              "run.py ledger %s ack --pass %d --chunk %d --reason \"...\" (at least 20 characters)." % (n - 1, p, a.run, a.run, p, n - 1), 3)
    if p == 2 and n == 1:
        unacked = [c for c in range(1, len(st["chunks"]) + 1) if not chunk_acked(st, led, 1, c)]
        if unacked:
            w.die("REFUSED: Pass 1 chunks %s have no ledger entry or acknowledgement; finish Pass 1 properly before Pass 2." % unacked, 3)

    s, e = st["chunks"][n - 1]
    body = "\n".join("%6d  %s" % (i, lines[i - 1]) for i in range(s, e + 1))
    print("===== PASS %d  CHUNK %d/%d  lines %d-%d of %d =====" % (p, n, k, s, e, len(lines)))
    print(body)
    print("===== END OF CHUNK %d/%d (pass %d) =====" % (n, k, p))
    if n not in done:
        st["reads"].append({"pass": p, "chunk": n, "t": w.now(), "lines": [s, e],
                            "sha256": w.sha256_text(body)})
        w.save_json(os.path.join(a.run, w.STATE), st)
    print("BEFORE THE NEXT CHUNK: record what this chunk contains (run.py ledger %s add ...) or, if it holds no decisions, requests or "
          "figures, acknowledge it in your own words: run.py ledger %s ack --pass %d --chunk %d --reason \"...\"" % (a.run, a.run, p, n))
    if n < k:
        print("NEXT: tx.py chunk %s %d %d" % (a.run, p, n + 1))
    elif p == 1:
        print("PASS 1 COMPLETE (all %d chunks). Write ledger.json entries now, then read Pass 2: "
              "tx.py chunk %s 2 1" % (k, a.run))
    else:
        print("PASS 2 COMPLETE (all %d chunks). Check every ledger entry against the words, add "
              "anything Pass 1 missed, then run: tx.py scan %s" % (k, a.run))


def chunk_acked(st, ledger, p, c):
    """A chunk counts as worked through only when it produced a ledger entry (in that pass) or a reasoned acknowledgement."""
    s, e = st["chunks"][c - 1]
    for en in (ledger or {}).get("entries", []):
        if isinstance(en, dict) and en.get("pass") == p and isinstance(en.get("line"), int) and s <= en["line"] <= e:
            return True
    return any(isinstance(a, dict) and a.get("pass") == p and a.get("chunk") == c and len(str(a.get("reason", "")).strip()) >= 20
               for a in (ledger or {}).get("chunk_acks", []))


def load_ledger(run):
    path = os.path.join(run, w.LEDGER)
    return w.load_json(path) if os.path.exists(path) else {"entries": [], "scan_reviewed": [], "chunk_acks": []}


def passes_done(st):
    k = len(st["chunks"])
    return [all(c in {r["chunk"] for r in st["reads"] if r["pass"] == p} for c in range(1, k + 1))
            for p in (1, 2)]


def cmd_scan(a):
    st = load_state(a.run)
    if not all(passes_done(st)):
        w.die("REFUSED: the keyword scan runs in addition to the two reads, not instead of them. "
              "Finish Pass 1 and Pass 2 first.", 3)
    led = load_ledger(a.run)
    unacked = [(p_, c) for p_ in (1, 2) for c in range(1, len(st["chunks"]) + 1) if not chunk_acked(st, led, p_, c)]
    if unacked:
        w.die("REFUSED: chunks without a ledger entry or acknowledgement (pass, chunk): %s" % unacked[:10], 3)
    lines = w.read_lines(a.run)
    total = len(lines)
    closing_from = int(total * (1 - CLOSING_FRACTION)) + 1
    # the closing minutes: the last 15% of the lines OR the last 10 minutes of the call, whichever reaches further back
    stamps_ = [(i, ts_seconds(ln)) for i, ln in enumerate(lines, 1) if ts_seconds(ln) is not None]
    if stamps_:
        last = max(sec for _, sec in stamps_)
        by_time = next((i for i, sec in stamps_ if sec >= last - CLOSING_SECONDS), closing_from)
        closing_from = min(closing_from, by_time)
    hits = [i for i, ln in enumerate(lines, 1) if HIGH_RE.search(ln)]
    low = [i for i, ln in enumerate(lines, 1) if i not in set(hits) and LOW_RE.search(ln)]
    print("KEYWORD SCAN: %d lines with decision/change/request words, %d more with figures/days/products "
          "(closing zone = lines %d-%d)" % (len(hits), len(low), closing_from, total))
    for i in sorted(hits + low):
        mark = ("C" if i >= closing_from else " ") + ("*" if i in hits else " ")
        print("%s %6d  %s" % (mark, i, lines[i - 1].strip()[:150]))
    st["scan"] = {"t": w.now(), "hits": hits, "low_hits": low, "closing_from": closing_from}
    w.save_json(os.path.join(a.run, w.STATE), st)
    print("\nC = closing minutes, * = decision/change/request word. Every hit marked C* must be covered by a ledger entry "
          "(within 3 lines) or recorded with: run.py ledger RUN review --line N --reason R. Other hits are warnings in verify.py.")


def cmd_status(a):
    st = load_state(a.run)
    k = len(st["chunks"])
    p1, p2 = passes_done(st)
    r1 = sorted(r["chunk"] for r in st["reads"] if r["pass"] == 1)
    r2 = sorted(r["chunk"] for r in st["reads"] if r["pass"] == 2)
    print("RUN %s   source: %s   lines: %d   chunks: %d" % (a.run, st["source"], st["total_lines"], k))
    print("  complete: %s%s" % (st["complete"], "  (FORCED)" if st["forced"] else ""))
    print("  Pass 1 read: %s  %s" % (r1, "DONE" if p1 else "NOT DONE"))
    print("  Pass 2 read: %s  %s" % (r2, "DONE" if p2 else "NOT DONE"))
    led = load_ledger(a.run)
    pend = [(p_, c) for p_ in (1, 2) for c in range(1, k + 1) if c in {r["chunk"] for r in st["reads"] if r["pass"] == p_}
            and not chunk_acked(st, led, p_, c)]
    print("  chunks read but not yet acknowledged in the ledger (pass, chunk): %s" % (pend or "none"))
    print("  keyword scan: %s" % ("run, %d hits" % len(st["scan"]["hits"]) if st["scan"] else "NOT RUN"))
    print("  outputs built: %s" % ("yes" if st["build"] else "no"))
    if not p1:
        nxt = "tx.py chunk %s 1 %d" % (a.run, (max(r1) + 1) if r1 else 1)
    elif not p2:
        nxt = "tx.py chunk %s 2 %d" % (a.run, (max(r2) + 1) if r2 else 1)
    elif not st["scan"]:
        nxt = "tx.py scan %s" % a.run
    elif not st["build"]:
        nxt = "write ledger.json and content.json, then build.py %s" % a.run
    else:
        nxt = "verify.py %s" % a.run
    print("NEXT: " + nxt)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prep")
    p.add_argument("source")
    p.add_argument("run")
    p.add_argument("--force", action="store_true")
    p.add_argument("--notes", action="store_true", help="the source is notes or a recap with no timestamps (WhatsApp call)")
    p.set_defaults(fn=cmd_prep)
    p = sub.add_parser("chunk")
    p.add_argument("run")
    p.add_argument("pass_", type=int, metavar="pass")
    p.add_argument("n", type=int)
    p.set_defaults(fn=cmd_chunk)
    p = sub.add_parser("scan")
    p.add_argument("run")
    p.set_defaults(fn=cmd_scan)
    p = sub.add_parser("status")
    p.add_argument("run")
    p.set_defaults(fn=cmd_status)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
