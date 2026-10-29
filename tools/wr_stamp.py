"""What a skill ships, and a fingerprint of it. Shared by stamp_skill.py, lint_skill.py and package_skill.py (S2).

The "Last updated" date must move whenever the skill's real files change, and only then. So the stamp tool records a
fingerprint of everything the zip carries; lint and the packager compare against it. File times are not used: a fresh
copy of the repo gives every file a new time and would make the date meaningless.
"""
import hashlib
import json
import os
import re

INCLUDE_FILES = ("SKILL.md", "steps.json", "deliverables.json")
INCLUDE_DIRS = ("scripts", "references")
RECORD = os.path.join("history", "stamp.json")
STAMP_RE = re.compile(r"\*\*Last updated:[^*]*\*\*")


def shipped(skill):
    """Relative paths of everything the zip carries, sorted."""
    out = [f for f in INCLUDE_FILES if os.path.exists(os.path.join(skill, f))]
    for d in INCLUDE_DIRS:
        for root, dirs, files in os.walk(os.path.join(skill, d)):
            dirs[:] = [x for x in dirs if x != "__pycache__"]
            out += [os.path.relpath(os.path.join(root, f), skill) for f in files if not f.endswith(".pyc")]
    return sorted(out)


def changes_table(lines):
    """(separator row index, index after the last row) of the 'Recent changes' table, or None."""
    sep = next((i for i, l in enumerate(lines)
                if re.match(r"\|\s*-+\s*\|\s*-+\s*\|\s*$", l) and "when" in lines[i - 1].lower() and "what changed" in lines[i - 1].lower()), None)
    if sep is None:
        return None
    end = sep + 1
    while end < len(lines) and lines[end].startswith("|"):
        end += 1
    return sep, end


def normalised_skill_md(text):
    """SKILL.md without what the stamp tool itself rewrites: the stamp line and the rows of the Recent changes table."""
    text = STAMP_RE.sub("**Last updated: -**", text.replace("\r\n", "\n"), count=1)
    lines = text.split("\n")
    t = changes_table(lines)
    if t:
        del lines[t[0] + 1:t[1]]
    return "\n".join(lines)


def fingerprint(skill):
    h = hashlib.sha256()
    for rel in shipped(skill):
        with open(os.path.join(skill, rel), "rb") as f:
            data = f.read().replace(b"\r\n", b"\n")
        if rel == "SKILL.md":
            data = normalised_skill_md(data.decode("utf-8")).encode("utf-8")
        h.update(rel.replace(os.sep, "/").encode("utf-8") + b"\0" + hashlib.sha256(data).digest())
    return h.hexdigest()


def read_record(skill):
    try:
        with open(os.path.join(skill, RECORD), encoding="utf-8") as f:
            rec = json.load(f)
        return rec if isinstance(rec, dict) else None
    except (OSError, ValueError):
        return None


def write_record(skill, stamp, change, fp):
    path = os.path.join(skill, RECORD)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"stamp": stamp, "fingerprint": fp, "change": change}, f, indent=1, ensure_ascii=False)
        f.write("\n")
