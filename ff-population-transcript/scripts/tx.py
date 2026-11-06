#!/usr/bin/env python3
"""Reading lock for the Teams transcript(s): the program hands the transcript over in order, twice.

  tx.py prep   <run_dir> <transcript file> [<more files of the same meeting>] [--force]
  tx.py chunk  <run_dir> <pass 1|2> <n>
  tx.py status <run_dir>

prep    converts each file (a .docx is read with pandoc), checks each is complete (the last time stamp against the stated length, no
        gaps), joins several files of one meeting (a call that dropped and came back) and plans the chunks.
chunk   prints one numbered chunk and logs the read. Chunks are served in order; Pass 2 is refused until Pass 1 has served every chunk.
status  what has been read and what is next.

The log proves each chunk was put in front of Claude, in order, twice. It cannot prove the text was understood: the quote check
in `run.py compose` is what tests that a quoted fact is really in the transcript.
"""
import os
import re
import subprocess
import sys

import wrlib as w

TOLERANCE_S = 120   # the last time stamp may fall this far short of the stated length
JUMP_S = 600        # a silent jump bigger than this is a gap
TS_ARROW = re.compile(r"^\s*(\d{1,2}):(\d{1,2}):(\d{1,2})(?:[.,]\d+)?\s*-->")
TS_START = re.compile(r"^\s*(\d{1,2}):(\d{2})(?::(\d{2}))?(?:[.,]\d+)?(?!\d)")
NAME_WORD = r"(?:[A-Z][\w'’-]*|van|de|der|den|la|le|du|di|von)"
TS_END = re.compile(r"^" + NAME_WORD + r"(?:\s+" + NAME_WORD + r"){0,4}\s+(\d{1,2}):(\d{2})(?::(\d{2}))?\s*$")
DURATION = re.compile(r"(?i)duration\W{0,5}(?:(\d+)\s*h\w*)?\s*(?:(\d+)\s*m\w*)?\s*(?:(\d+)\s*s\w*)?")
CLOSING = re.compile(r"(?i)stopped transcription|transcription stopped|stopped recording|meeting ended")
SEP = "===== TRANSCRIPT %d OF %d ====="


def ts_seconds(line):
    m = TS_ARROW.match(line)
    if m:
        return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
    m = TS_START.match(line) or TS_END.match(line)
    if not m:
        return None
    a, b, c = int(m.group(1)), int(m.group(2)), m.group(3)
    return a * 60 + b if c is None else a * 3600 + b * 60 + int(c)


def fmt(sec):
    sec = int(sec)
    return "%d:%02d:%02d" % (sec // 3600, sec % 3600 // 60, sec % 60)


def read_source(path):
    if path.lower().endswith((".docx", ".doc", ".rtf", ".odt")):
        try:
            r = subprocess.run(["pandoc", "-t", "plain", "--wrap=none", path], capture_output=True, text=True)
        except FileNotFoundError:
            w.die("STOP: pandoc is not installed, so a .docx transcript cannot be read. Tell Paul in one line.", 4)
        if r.returncode:
            w.die("pandoc could not read %s: %s" % (path, r.stderr.strip()[:120]), 4)
        return r.stdout
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def plan_chunks(lines):
    """Chunks of at most CHUNK_LINES lines / CHUNK_CHARS characters, ending at a blank line when one sits in the back half (keeps a speaker with their words)."""
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


def check_part(text, name):
    """(notes, complete) for one transcript file."""
    lines = [ln.rstrip() for ln in text.split("\n")]
    raw = [(i, s) for i, s in ((i, ts_seconds(ln)) for i, ln in enumerate(lines, 1)) if s is not None]
    stamps, top = [], -1
    for i, s in raw:
        if s >= top:
            stamps.append((i, s))
            top = s
    notes, complete = [], True
    dur = None
    for m in DURATION.finditer(text):
        h, mi, s = (int(x) if x else 0 for x in m.groups())
        if h or mi or s:
            dur = h * 3600 + mi * 60 + s
            break
    if not stamps:
        return ["%s: no time stamps could be read, so completeness cannot be checked (first 15 lines: %r)" % (name, " | ".join(lines[:15])[:300])], False, None, None, dur
    last = stamps[-1][1]
    if dur is not None and last < dur - TOLERANCE_S:
        complete = False
        notes.append("%s: INCOMPLETE: stated length %s but the last time stamp is %s (%s missing)" % (name, fmt(dur), fmt(last), fmt(dur - last)))
    elif dur is None and not [1 for ln in lines if CLOSING.search(ln)]:
        complete = False
        notes.append("%s: INCOMPLETE?: no stated length and no closing marker, so it cannot be checked that it reaches the end" % name)
    for (i1, t1), (i2, t2) in zip(stamps, stamps[1:]):
        if t2 - t1 > JUMP_S:
            complete = False
            notes.append("%s: GAP of %s between line %d (%s) and line %d (%s)" % (name, fmt(t2 - t1), i1, fmt(t1), i2, fmt(t2)))
    return notes, complete, fmt(stamps[0][1]), fmt(last), dur


def cmd_prep(run, paths, force=False):
    if not paths:
        w.die("give the transcript file(s)")
    parts, all_lines, notes, complete = [], [], [], True
    for k, p in enumerate(paths, 1):
        if not os.path.exists(p):
            w.die("MISSING: %s" % p)
        text = read_source(p).replace("\r\n", "\n").replace("\r", "\n")
        body = [ln.rstrip() for ln in text.split("\n")]
        while body and not body[-1]:
            body.pop()
        if not body:
            w.die("STOP: %s is empty." % os.path.basename(p), 4)
        n_, c_, first, last, dur = check_part(text, os.path.basename(p))
        notes += n_
        complete = complete and c_
        if len(paths) > 1:
            all_lines.append(SEP % (k, len(paths)))
        all_lines += body
        parts.append({"source": os.path.basename(p), "lines": len(body), "first_ts": first, "last_ts": last, "stated_duration": fmt(dur) if dur else None, "complete": c_})
    forced = False
    if not complete and force:
        forced, complete = True, True
        notes.append("FORCED past the warnings above (Paul said to carry on)")
    os.makedirs(run, exist_ok=True)
    with open(os.path.join(run, w.TRANSCRIPT), "w", encoding="utf-8") as f:
        f.write("\n".join(all_lines))
    chunks = plan_chunks(all_lines)
    st = {"created": w.now(), "parts": parts, "total_lines": len(all_lines), "sha256": w.sha256_text("\n".join(all_lines)), "chunks": chunks,
          "complete": complete, "forced": forced, "notes": notes, "reads": []}
    w.save_json(os.path.join(run, w.STATE), st)
    print("TRANSCRIPT PREPARED: %d file(s), %d lines, %d chunks" % (len(parts), len(all_lines), len(chunks)))
    for p in parts:
        print("  %s: %d lines, times %s to %s, stated length %s" % (p["source"], p["lines"], p["first_ts"], p["last_ts"], p["stated_duration"] or "not stated"))
    for n in notes:
        print("  " + n)
    if not complete:
        print("\nSTOP. The transcript is not complete (above). Tell Paul in one line what is missing. Only if Paul says to carry on: add --force.")
        sys.exit(2)
    print("\nNEXT: read Pass 1, chunk 1:  python3 %s chunk %s 1 1" % (os.path.abspath(__file__), run))


def load_state(run):
    return w.load_json(os.path.join(run, w.STATE), "state.json (the transcript has not been prepared yet)")


def served(st, p):
    return sorted({r["chunk"] for r in st["reads"] if r["pass"] == p})


def passes_done(st):
    k = len(st["chunks"])
    return [served(st, p) == list(range(1, k + 1)) for p in (1, 2)]


def cmd_chunk(run, p, n):
    st = load_state(run)
    k = len(st["chunks"])
    if p not in (1, 2) or not 1 <= n <= k:
        w.die("REFUSED: pass must be 1 or 2 and chunk 1..%d." % k, 3)
    if p == 2 and not passes_done(st)[0]:
        w.die("REFUSED: Pass 2 starts only after Pass 1 has served every chunk (served so far: %s of %d)." % (served(st, 1) or "none", k), 3)
    if n > 1 and (n - 1) not in served(st, p):
        w.die("REFUSED: chunk %d of Pass %d has not been served yet: read the chunks in order." % (n - 1, p), 3)
    a, b = st["chunks"][n - 1]
    lines = w.read_lines(run)
    if w.sha256_text("\n".join(lines)) != st["sha256"]:
        w.die("REFUSED: transcript.txt changed after it was prepared.", 3)
    print("PASS %d, CHUNK %d OF %d  (lines %d to %d of %d)\n" % (p, n, k, a, b, len(lines)))
    for i in range(a, b + 1):
        print("%d| %s" % (i, lines[i - 1]))
    st["reads"].append({"pass": p, "chunk": n, "t": w.now()})
    w.save_json(os.path.join(run, w.STATE), st)
    print()
    if n < k:
        print("NEXT: python3 %s chunk %s %d %d" % (os.path.abspath(__file__), run, p, n + 1))
    elif p == 1:
        print("PASS 1 COMPLETE (all %d chunks). Now read the WHOLE transcript again: Pass 2, chunk 1." % k)
    else:
        print("PASS 2 COMPLETE (all %d chunks). The transcript has been read twice, in order." % k)


def cmd_status(run):
    st = load_state(run)
    k = len(st["chunks"])
    d1, d2 = passes_done(st)
    print("transcript: %d lines in %d chunks; Pass 1: %s; Pass 2: %s" % (st["total_lines"], k, "done" if d1 else "%d of %d" % (len(served(st, 1)), k), "done" if d2 else "%d of %d" % (len(served(st, 2)), k)))


def main():
    a = sys.argv[1:]
    if len(a) >= 3 and a[0] == "prep":
        force = "--force" in a
        paths = [x for x in a[2:] if x != "--force"]
        cmd_prep(os.path.abspath(a[1]), paths, force)
    elif len(a) == 4 and a[0] == "chunk" and a[2].isdigit() and a[3].isdigit():
        cmd_chunk(os.path.abspath(a[1]), int(a[2]), int(a[3]))
    elif len(a) == 2 and a[0] == "status":
        cmd_status(os.path.abspath(a[1]))
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
