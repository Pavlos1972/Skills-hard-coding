#!/usr/bin/env python3
"""Set a skill's "Last updated" stamp from the Athens clock (SKILL-STANDARDS.md S2).

  stamp_skill.py <skill_dir> --change "one line saying what changed"

Never type the time by hand. This rewrites the `**Last updated: ... (Athens time)**` line and adds one row to the top
of the "Recent changes" table, keeping at most 5 rows. Full history stays in the skill's history/ folder.
"""
import argparse
import datetime as dt
import os
import re
import sys
import zoneinfo


def athens_now():
    return dt.datetime.now(zoneinfo.ZoneInfo("Europe/Athens")).strftime("%Y-%m-%d %H:%M")


def stamp(text, change, now):
    new, n = re.subn(r"\*\*Last updated:[^*]*\*\*", "**Last updated: %s (Athens time)**" % now, text, count=1)
    if n != 1:
        sys.exit("SKILL.md has no '**Last updated: ...**' line to update")
    lines = new.split("\n")
    # the 'Recent changes' table is the one whose header row says "When" and "What changed" (not the Index table)
    sep = next((i for i, l in enumerate(lines)
                if re.match(r"\|\s*-+\s*\|\s*-+\s*\|\s*$", l) and "when" in lines[i - 1].lower() and "what changed" in lines[i - 1].lower()), None)
    if sep is None:
        sys.exit("SKILL.md has no 'Recent changes' table (header '| When ... | What changed |', then |---|---|, then rows)")
    end = sep + 1
    while end < len(lines) and lines[end].startswith("|"):
        end += 1
    rows = ["| %s | %s |" % (now, change.strip().replace("|", "/"))] + lines[sep + 1:end]
    lines[sep + 1:end] = rows[:5]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("skill_dir")
    ap.add_argument("--change", required=True)
    a = ap.parse_args()
    path = os.path.join(a.skill_dir, "SKILL.md")
    now = athens_now()
    with open(path, encoding="utf-8") as f:
        text = f.read()
    with open(path, "w", encoding="utf-8") as f:
        f.write(stamp(text, a.change, now))
    print("stamped %s: Last updated %s (Athens time)" % (path, now))


if __name__ == "__main__":
    main()
