#!/usr/bin/env python3
"""Lint one skill folder against SKILL-STANDARDS.md (S2, S5, S11).

  lint_skill.py <skill_dir>          exit 0 only when there is no FAIL

Set WR_NAME_BLOCKLIST=<file with one client name per line> (kept OUTSIDE the repo) to also scan for client names.
"""
import json
import os
import re
import sys

import wr_stamp

ALLOWED_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
TEXT_EXT = (".md", ".json", ".py", ".js", ".txt", ".html")
DATE_ATTR = re.compile(r"\((?:[^()]*\b)?(?:Paul'?s? (?:absolute |standing )?rule|changed|approved|reversed|confirmed|new Step)[^()]*\d{1,2}[./]\d{1,2}[./]\d{2,4}[^()]*\)", re.I)


def read(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def package_files(skill):
    for root, dirs, files in os.walk(skill):
        dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git")]
        for f in files:
            yield os.path.join(root, f)


def lint(skill):
    rows = []
    add = lambda lvl, msg: rows.append((lvl, msg))  # noqa: E731
    path = os.path.join(skill, "SKILL.md")
    if not os.path.exists(path):
        return [("FAIL", "SKILL.md is missing")]
    text = read(path)
    lines = text.split("\n")

    # frontmatter
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        add("FAIL", "SKILL.md has no frontmatter (--- name / description ---)")
        fm = {}
    else:
        fm = {}
        for ln in m.group(1).split("\n"):
            if ":" in ln:
                k, v = ln.split(":", 1)
                fm[k.strip()] = v.strip().strip('"')
        bad = sorted(set(fm) - ALLOWED_KEYS)
        if bad:
            add("FAIL", "frontmatter keys not allowed on upload: %s (allowed: %s)" % (bad, sorted(ALLOWED_KEYS)))
        name, desc = fm.get("name", ""), fm.get("description", "")
        if not re.fullmatch(r"[a-z0-9-]{1,64}", name) or "anthropic" in name or "claude" in name:
            add("FAIL", "name must be lowercase letters, numbers, hyphens, up to 64, without 'anthropic' or 'claude': %r" % name)
        if not desc or len(desc) > 1024:
            add("FAIL", "description must be present and at most 1,024 characters (is %d)" % len(desc))
        if name and name != os.path.basename(os.path.abspath(skill)):
            add("WARN", "folder name %r differs from skill name %r" % (os.path.basename(os.path.abspath(skill)), name))

    # Index right after the title, listing every ## heading
    headings = [l[3:].strip() for l in lines if l.startswith("## ") and l[3:].strip().lower() != "index"]
    idx = next((i for i, l in enumerate(lines) if l.strip().lower() == "## index"), None)
    title = next((i for i, l in enumerate(lines) if l.startswith("# ")), None)
    if idx is None or title is None or idx - title > 3:
        add("FAIL", "an '## Index' table must come directly after the title")
    else:
        block = []
        for l in lines[idx + 1:]:
            if l.startswith("## "):
                break
            block.append(l)
        miss = [h for h in headings if h.lower() not in " ".join(block).lower()]
        add("FAIL" if miss else "PASS", "Index lists every section heading" if not miss else "Index is missing sections: %s" % miss)

    # stamp (S2)
    sm = re.search(r"\*\*Last updated:\s*(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}) \(Athens time\)\*\*", text)
    if not sm:
        add("FAIL", "no '**Last updated: YYYY-MM-DD HH:MM (Athens time)**' line (set it with tools/stamp_skill.py)")
    else:
        shown = "%s %s" % (sm.group(1), sm.group(2))
        rec = wr_stamp.read_record(skill)
        if rec is None:
            add("FAIL", "no stamp record (history/stamp.json): run tools/stamp_skill.py")
        elif rec.get("stamp") != shown:
            add("FAIL", "the 'Last updated' line (%s) is not the one the stamp tool recorded (%s): it was edited by hand. Run tools/stamp_skill.py"
                % (shown, rec.get("stamp")))
        elif rec.get("fingerprint") != wr_stamp.fingerprint(skill):
            add("FAIL", "the skill's files changed after they were stamped (%s): run tools/stamp_skill.py so the date moves" % shown)
        else:
            add("PASS", "Last updated stamp matches the skill's files (%s Athens time)" % shown)
    sep = next((i for i, l in enumerate(lines) if re.match(r"\|\s*-+\s*\|\s*-+\s*\|", l) and "when" in lines[i - 1].lower()), None)
    if sep is not None:
        n = 0
        while sep + 1 + n < len(lines) and lines[sep + 1 + n].startswith("|"):
            n += 1
        if n > 5:
            add("FAIL", "'Recent changes' has %d rows: keep 5, move the rest to history/" % n)
    else:
        add("WARN", "no 'Recent changes' table found")

    # size
    tokens = len(text.encode("utf-8")) // 4
    if len(lines) >= 500:
        add("FAIL", "SKILL.md is %d lines (limit 500)" % len(lines))
    elif tokens > 5000:
        add("WARN", "SKILL.md is about %d tokens (target 5,000)" % tokens)
    else:
        add("PASS", "SKILL.md size %d lines, about %d tokens" % (len(lines), tokens))

    # steps / deliverables / references
    sp = os.path.join(skill, "steps.json")
    if os.path.exists(sp):
        steps = json.loads(read(sp))["steps"]
        sys.path.insert(0, os.path.join(skill, "scripts"))
        try:
            import run as driver
            checks = set(driver.CHECKS)
        except Exception as e:  # pragma: no cover
            checks, _ = set(), add("FAIL", "cannot import scripts/run.py: %s" % e)
        for s in steps:
            for r in ([s["ref"]] if isinstance(s.get("ref"), str) else s.get("ref") or []):
                if not os.path.exists(os.path.join(skill, "references", r)):
                    add("FAIL", "step %s points to a missing reference page %s" % (s["id"], r))
            if checks and s["check"] not in checks:
                add("FAIL", "step %s names an unknown check %r" % (s["id"], s["check"]))
        ids = {s["id"] for s in steps}
        dp = os.path.join(skill, "deliverables.json")
        if os.path.exists(dp):
            for d in json.loads(read(dp))["deliverables"]:
                if d.get("step") not in ids:
                    add("FAIL", "deliverable %r names step %r which does not exist" % (d.get("name"), d.get("step")))
        else:
            add("FAIL", "deliverables.json is missing (S6: every output is listed)")
        add("PASS", "%d steps, every reference page and check exists" % len(steps)) if not any(r[0] == "FAIL" and "step" in r[1] for r in rows) else None
    for f in package_files(os.path.join(skill, "references")) if os.path.isdir(os.path.join(skill, "references")) else []:
        t = read(f)
        if f.endswith(".md") and t.count("\n") > 100 and "contents" not in t[:600].lower():
            add("WARN", "%s is over 100 lines and does not open with a contents list" % os.path.relpath(f, skill))

    # S11: no client data; S5: no dated attributions in the live body
    blocklist = []
    if os.environ.get("WR_NAME_BLOCKLIST") and os.path.exists(os.environ["WR_NAME_BLOCKLIST"]):
        blocklist = [x.strip() for x in read(os.environ["WR_NAME_BLOCKLIST"]).split("\n") if x.strip()]
    else:
        add("WARN", "client-name check skipped: set WR_NAME_BLOCKLIST to a file of names kept outside the repo")
    found, ids13, dated = [], [], 0
    for f in package_files(skill):
        if not f.endswith(TEXT_EXT):
            continue
        t = read(f)
        rel = os.path.relpath(f, skill)
        for nm in blocklist:
            if re.search(r"\b%s\b" % re.escape(nm), t, re.I):
                found.append("%s in %s" % (nm, rel))
        if re.search(r"(?<!\d)\d{13}(?!\d)", t) and not rel.startswith("tests"):
            ids13.append(rel)
        if not rel.startswith(("history", "tests")):
            dated += len(DATE_ATTR.findall(t))
    if found:
        add("FAIL", "client names found: %s" % found[:8])
    elif blocklist:
        add("PASS", "no client names from the blocklist (%d names) anywhere in the folder" % len(blocklist))
    if ids13:
        add("FAIL", "13-digit numbers (ID numbers?) in: %s" % ids13)
    if dated:
        add("WARN", "%d dated attributions such as '(Paul's rule, 06/10/2026)' remain in the live pages: history belongs in history/" % dated)
    return rows


def main():
    skill = sys.argv[1] if len(sys.argv) > 1 else "."
    rows = lint(skill)
    for lvl, msg in rows:
        print("[%-4s] %s" % (lvl, msg))
    fails = sum(1 for r in rows if r[0] == "FAIL")
    print("LINT: %s (%d fail, %d warn)" % ("PASS" if not fails else "FAIL", fails, sum(1 for r in rows if r[0] == "WARN")))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
