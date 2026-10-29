#!/usr/bin/env python3
"""Rule-by-rule coverage check: did anything in the OLD skill get lost? (SKILL-STANDARDS.md S5)

  inventory.py <old SKILL.md> <skill_dir> [--changes history/changes.json] [--decisions history/decisions.json] [--report file.md]

Every sentence of the old skill must be one of:
  KEPT      found (almost) word for word in the new skill folder
  REWORDED  found in changed form, AND the paragraph is covered by a record in changes.json
  DROPPED   covered by a decision in decisions.json (with reason; needs_paul marks the ones Paul must approve)
Anything else is UNACCOUNTED and the check fails.
"""
import argparse
import difflib
import json
import os
import re
import sys

KEPT, REWORDED = 0.90, 0.55


def norm(s):
    s = s.lower().replace("’", "'").replace("‘", "'")
    return " ".join(re.sub(r"[\W_]+", " ", s).split())


def plain(line):
    """A line without list markers, bold and code marks, so prefixes match what a person reads."""
    return re.sub(r"^\s*(?:[-*]|\d+\.|\|)\s*", "", line).replace("**", "").replace("`", "").lstrip("*").strip()


def sentences(text):
    out = []
    for ln in text.split("\n"):
        plain = re.sub(r"^\s*(?:[-*]|\d+\.|\|)\s*", "", ln)
        plain = plain.replace("**", "").replace("`", "")
        for s in re.split(r"(?<=[.!?:;])\s+", plain):
            if len(norm(s).split()) >= 5:
                out.append(s.strip())
    return out


def blocks(lines):
    """Paragraph blocks: (first_line_index, last_line_index) of consecutive non-blank lines."""
    res, start = [], None
    for i, l in enumerate(lines + [""]):
        if l.strip() and start is None:
            start = i
        elif not l.strip() and start is not None:
            res.append((start, i - 1))
            start = None
    return res


def new_corpus(skill):
    texts = []
    for root, dirs, files in os.walk(skill):
        dirs[:] = [d for d in dirs if d not in ("history", "tests", "__pycache__", ".git")]
        for f in files:
            if f.endswith((".md", ".json", ".py", ".js", ".html", ".txt")):
                with open(os.path.join(root, f), encoding="utf-8", errors="replace") as fh:
                    texts.append(fh.read())
    return [s for t in texts for s in sentences(t)]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("old")
    ap.add_argument("skill")
    ap.add_argument("--changes")
    ap.add_argument("--decisions")
    ap.add_argument("--report")
    a = ap.parse_args()

    with open(a.old, encoding="utf-8") as f:
        old = f.read()
    old = re.sub(r"\A<!--.*?-->\s*", "", old, flags=re.S)
    old = re.sub(r"\A---\n.*?\n---\n", "", old, flags=re.S)
    lines = old.split("\n")
    changes = json.load(open(a.changes)) if a.changes and os.path.exists(a.changes) else []
    decisions = json.load(open(a.decisions)) if a.decisions and os.path.exists(a.decisions) else []

    # which lines are covered by a change record (whole paragraph) or a decision (line range)
    covered = {}
    for b0, b1 in blocks(lines):
        text = norm(" ".join(lines[b0:b1 + 1]))
        for i, c in enumerate(changes):
            key = norm(c["old"])[:45]
            if key and key in text:
                for n in range(b0, b1 + 1):
                    covered.setdefault(n, ("changed", c))
    for d in decisions:
        start = next((i for i, l in enumerate(lines) if norm(plain(l)).startswith(norm(d["from_prefix"]))), None)
        if start is None:
            print("WARN: decision matches no line: %r" % d["from_prefix"][:60])
            continue
        end = start
        if d.get("to_prefix"):
            end = next((i for i in range(start, len(lines)) if norm(plain(lines[i])).startswith(norm(d["to_prefix"]))), None)
            if end is None:
                print("WARN: decision end matches no line: %r" % d["to_prefix"][:60])
                continue
        for n in range(start, end + 1):
            covered[n] = ("dropped", d)

    corpus = new_corpus(a.skill)
    cn = [norm(s) for s in corpus]
    index = {}
    for i, s in enumerate(cn):
        for wd in set(s.split()):
            index.setdefault(wd, set()).add(i)

    res = {"kept": [], "reworded": [], "dropped": [], "unaccounted": []}
    for n, ln in enumerate(lines):
        for s in sentences(ln):
            ns = norm(s)
            words = set(ns.split())
            cand = {}
            for wd in words:
                for i in index.get(wd, ()):
                    cand[i] = cand.get(i, 0) + 1
            best, best_s = 0.0, ""
            for i, _ in sorted(cand.items(), key=lambda kv: -kv[1])[:12]:
                r = difflib.SequenceMatcher(None, ns, cn[i]).ratio()
                if r > best:
                    best, best_s = r, corpus[i]
            cov = covered.get(n)
            if cov and cov[0] == "dropped":
                res["dropped"].append((n + 1, s, cov[1]))
            elif best >= KEPT:
                res["kept"].append((n + 1, s))
            elif cov and cov[0] == "changed":
                res["reworded"].append((n + 1, s, round(best, 2), best_s, cov[1]))
            elif best >= REWORDED:
                res["unaccounted"].append((n + 1, s, round(best, 2), best_s))
            else:
                res["unaccounted"].append((n + 1, s, round(best, 2), ""))

    total = sum(len(v) for v in res.values())
    out = ["INVENTORY of the old skill: %d sentences" % total,
           "  kept (word for word or nearly): %d" % len(res["kept"]),
           "  reworded, with a recorded change: %d" % len(res["reworded"]),
           "  dropped, with a recorded decision: %d" % len(res["dropped"]),
           "  UNACCOUNTED: %d" % len(res["unaccounted"])]
    for n, s, r, best in res["unaccounted"]:
        out.append("\n  [old line %d] %s\n      closest in new (%.2f): %s" % (n, s[:220], r, best[:160] or "(nothing)"))
    text = "\n".join(out)
    print(text)
    if a.report:
        rep = [text, "\n\nREWORDED (each is covered by a recorded change):"]
        for n, s, r, best, c in res["reworded"]:
            rep.append("- old line %d: %s\n    now: %s\n    why: %s" % (n, s[:200], best[:200], c["why"]))
        rep.append("\n\nDROPPED (each is covered by a recorded decision):")
        seen = set()
        for n, s, d in res["dropped"]:
            if d["from_prefix"] in seen:
                continue
            seen.add(d["from_prefix"])
            rep.append("- %s: %s%s" % (d["from_prefix"][:80], d["reason"], "  [NEEDS PAUL]" if d.get("needs_paul") else ""))
        with open(a.report, "w", encoding="utf-8") as f:
            f.write("\n".join(rep) + "\n")
    sys.exit(1 if res["unaccounted"] else 0)


if __name__ == "__main__":
    main()
