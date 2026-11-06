#!/usr/bin/env python3
"""Reading lock for the Teams transcript(s): the program hands the transcript over once, in order, and checks that each chunk was really read.

  tx.py prep   <run_dir> <transcript file> [<more files of the same meeting>] [--force]
  tx.py chunk  <run_dir> <n> [--seen "<first words of the check line>"]
  tx.py status <run_dir>

prep    converts each file (a .docx is read by this program itself, no other tool needed), checks each is complete (the last time stamp
        against the stated length, no gaps), joins several files of one meeting (a call that dropped and came back) and plans the chunks.
chunk   prints one numbered chunk in full and logs the read. Chunks are served in order. At the end of each chunk the program names a line from the
        MIDDLE of it; the next chunk is released only with --seen and the first words of that line. After the last chunk, `chunk <last+1> --seen ...`
        closes the reading ("READING COMPLETE"). Paul, 06/11/2026: the transcript is read once, but accurately.
status  what has been read and what is next.

The log proves each chunk was put in front of Claude, in full and in order, and that a line from the middle of it was seen. It cannot prove the text was understood: the quote check
in `run.py compose` is what tests that a quoted fact is really in the transcript.
"""
import os
import re
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET

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


W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def read_docx(path):
    """The text of a .docx, one line per paragraph, with the standard library only (no pandoc)."""
    try:
        with zipfile.ZipFile(path) as z:
            root = ET.fromstring(z.read("word/document.xml"))
    except (zipfile.BadZipFile, KeyError, ET.ParseError) as e:
        w.die("STOP: %s could not be read as a Word file (%s). Tell Paul in one line." % (os.path.basename(path), e), 4)
    lines = []
    for para in root.iter(W_NS + "p"):
        parts = []
        for el in para.iter():
            if el.tag == W_NS + "t":
                parts.append(el.text or "")
            elif el.tag == W_NS + "tab":
                parts.append("\t")
            elif el.tag in (W_NS + "br", W_NS + "cr"):
                parts.append("\n")
        lines.append("".join(parts))
    return "\n".join(lines)


def read_source(path):
    low = path.lower()
    if low.endswith(".docx") and zipfile.is_zipfile(path):        # a ".docx" that is really plain text is read as text below
        return read_docx(path)
    if low.endswith((".doc", ".rtf", ".odt")):
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
    print("\nNEXT: read chunk 1 (the whole transcript, once, accurately):  python3 %s chunk %s 1" % (os.path.abspath(__file__), run))


def load_state(run):
    return w.load_json(os.path.join(run, w.STATE), "state.json (the transcript has not been prepared yet)")


def served(st):
    return sorted({r["chunk"] for r in st["reads"]})


def read_done(st):
    """True only when every chunk was served in order and every reading check passed (the closing `chunk <last+1>` command)."""
    return bool(st.get("read_complete")) and served(st) == list(range(1, len(st["chunks"]) + 1))


def check_line(st, lines, n):
    """A line from the middle of chunk n (at least 6 words, not a time-stamp line), the same every time for the same transcript."""
    a, b = st["chunks"][n - 1]
    span = b - a + 1
    lo, hi = a + span // 4, b - span // 4
    cand = [i for i in range(lo, hi + 1) if len(lines[i - 1].split()) >= 6 and ts_seconds(lines[i - 1]) is None]
    if not cand:
        cand = [i for i in range(a, b + 1) if len(lines[i - 1].split()) >= 3 and ts_seconds(lines[i - 1]) is None]
    if not cand:
        cand = [i for i in range(a, b + 1) if lines[i - 1].strip()] or [a]
    h = int(w.sha256_text("%s:%d" % (st["sha256"], n))[:8], 16)
    return cand[h % len(cand)]


def first_words(line, k=5):
    return w.norm(" ".join(line.split()[:k]))


def cmd_chunk(run, n, seen=None):
    st = load_state(run)
    k = len(st["chunks"])
    if not 1 <= n <= k + 1:
        w.die("REFUSED: chunk must be 1..%d (chunk %d only closes the reading)." % (k, k + 1), 3)
    lines = w.read_lines(run)
    if w.sha256_text("\n".join(lines)) != st["sha256"]:
        w.die("REFUSED: transcript.txt changed after it was prepared.", 3)
    if n > 1:
        if (n - 1) not in served(st):
            w.die("REFUSED: chunk %d has not been served yet: read the chunks in order." % (n - 1), 3)
        ln = check_line(st, lines, n - 1)
        want = first_words(lines[ln - 1])
        got = w.norm(seen or "")
        if not got:
            w.die("REFUSED: to get chunk %d, repeat the first 5 words of line %d (chunk %d's reading check) with --seen \"...\" . Read the whole chunk; the check line is in the middle of it." % (n, ln, n - 1), 3)
        if got != want and not (len(got.split()) >= 4 and want.startswith(got)):
            w.die("REFUSED: those are not the first words of line %d. Look at line %d of chunk %d again (python3 %s chunk %s %d) and copy its first 5 words exactly." % (ln, ln, n - 1, os.path.abspath(__file__), run, n - 1), 3)
        st.setdefault("checks", {})[str(n - 1)] = {"line": ln, "ok": True}
    if n == k + 1:
        st["read_complete"] = True
        w.save_json(os.path.join(run, w.STATE), st)
        print("READING COMPLETE: all %d chunks were served in order and every reading check passed. The transcript has been read once, in full." % k)
        return
    a, b = st["chunks"][n - 1]
    print("CHUNK %d OF %d  (lines %d to %d of %d)\n" % (n, k, a, b, len(lines)))
    for i in range(a, b + 1):
        print("%d| %s" % (i, lines[i - 1]))
    st["reads"].append({"chunk": n, "t": w.now()})
    w.save_json(os.path.join(run, w.STATE), st)
    ln = check_line(st, lines, n)
    print()
    print("READING CHECK: the next command needs --seen with the first 5 words of line %d (copy them exactly from this chunk)." % ln)
    print("NEXT: python3 %s chunk %s %d --seen \"<first 5 words of line %d>\"%s" % (os.path.abspath(__file__), run, n + 1, ln, "   (this one closes the reading)" if n == k else ""))


def cmd_status(run):
    st = load_state(run)
    k = len(st["chunks"])
    print("transcript: %d lines in %d chunks; served %d of %d; reading %s" % (st["total_lines"], k, len(served(st)), k, "COMPLETE" if read_done(st) else "not complete"))


def main():
    a = sys.argv[1:]
    if len(a) >= 3 and a[0] == "prep":
        force = "--force" in a
        paths = [x for x in a[2:] if x != "--force"]
        cmd_prep(os.path.abspath(a[1]), paths, force)
    elif len(a) in (3, 5) and a[0] == "chunk" and a[2].isdigit() and (len(a) == 3 or a[3] == "--seen"):
        cmd_chunk(os.path.abspath(a[1]), int(a[2]), a[4] if len(a) == 5 else None)
    elif len(a) == 2 and a[0] == "status":
        cmd_status(os.path.abspath(a[1]))
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
