#!/usr/bin/env python3
"""Set a skill's "Last updated" stamp from the Athens clock (SKILL-STANDARDS.md S2).

  stamp_skill.py <skill_dir> --change "one line saying what changed"

Never type the time by hand. This rewrites the `**Last updated: ... (Athens time)**` line, adds one row to the top
of the "Recent changes" table (keeping at most 5 rows) and records a fingerprint of the skill's files in
history/stamp.json. Lint and the packager refuse a skill whose files changed after they were stamped, so the date
always moves with the skill. If nothing in the skill changed since the last stamp, the date is NOT moved.
Full history stays in the skill's history/ folder.
"""
import argparse
import datetime as dt
import os
import re
import sys
import zoneinfo

import wr_stamp


def athens_now():
    return dt.datetime.now(zoneinfo.ZoneInfo("Europe/Athens")).strftime("%Y-%m-%d %H:%M")


def stamp(text, change, now):
    new, n = re.subn(r"\*\*Last updated:[^*]*\*\*", "**Last updated: %s (Athens time)**" % now, text, count=1)
    if n != 1:
        sys.exit("SKILL.md has no '**Last updated: ...**' line to update")
    lines = new.split("\n")
    # the 'Recent changes' table is the one whose header row says "When" and "What changed" (not the Index table)
    t = wr_stamp.changes_table(lines)
    if t is None:
        sys.exit("SKILL.md has no 'Recent changes' table (header '| When ... | What changed |', then |---|---|, then rows)")
    sep, end = t
    rows = ["| %s | %s |" % (now, change.strip().replace("|", "/"))] + lines[sep + 1:end]
    lines[sep + 1:end] = rows[:5]
    return "\n".join(lines)


def apply(skill_dir, change, now, even_if_unchanged=False):
    path = os.path.join(skill_dir, "SKILL.md")
    with open(path, encoding="utf-8") as f:
        text = f.read()
    fp = wr_stamp.fingerprint(skill_dir)          # the stamp rewrites only what the fingerprint ignores
    rec = wr_stamp.read_record(skill_dir)
    if rec and rec.get("fingerprint") == fp and not even_if_unchanged:
        sys.exit("Nothing in the skill has changed since it was last stamped (%s), so the date is NOT moved. "
                 "Edit the skill first, then stamp it." % rec.get("stamp"))
    new = stamp(text, change, now)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new)
    wr_stamp.write_record(skill_dir, now, change.strip(), fp)
    return "stamped %s: Last updated %s (Athens time)" % (path, now)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("skill_dir")
    ap.add_argument("--change", required=True)
    ap.add_argument("--even-if-unchanged", action="store_true", help="move the date although no shipped file changed (tests only)")
    a = ap.parse_args()
    print(apply(a.skill_dir, a.change, athens_now(), a.even_if_unchanged))


if __name__ == "__main__":
    main()
