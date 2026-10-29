"""Tests for the shared tools: stamp, lint, inventory (nothing lost), package. Invented content only."""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
TOOLS = os.path.join(os.path.dirname(SKILL), "tools")
sys.path.insert(0, TOOLS)

import inventory  # noqa: E402
import lint_skill  # noqa: E402
import stamp_skill  # noqa: E402
import wr_stamp  # noqa: E402


def tool(name, *args, env=None):
    return subprocess.run([sys.executable, os.path.join(TOOLS, name)] + list(args), capture_output=True, text=True,
                          env=dict(os.environ, **(env or {})))


SAMPLE = """---
name: "demo-skill"
description: "Does a demo."
---

# Demo Skill

## Index

| # | Section | What it covers |
|---|---|---|
| 1 | Run it | how |

**Last updated: 2000-01-01 00:00 (Athens time)**

**Recent changes** (last 5)

| When (Athens time) | What changed |
|---|---|
| 2000-01-01 00:00 | first |

## Run it

Do the thing.
"""


class Stamp(unittest.TestCase):
    def test_stamp_updates_the_changes_table_and_not_the_index(self):
        out = stamp_skill.stamp(SAMPLE, "second change", "2026-10-29 12:00")
        self.assertIn("**Last updated: 2026-10-29 12:00 (Athens time)**", out)
        self.assertIn("| 2026-10-29 12:00 | second change |", out)
        self.assertIn("| 1 | Run it | how |", out)                       # Index table untouched
        self.assertLess(out.index("second change"), out.index("| 2000-01-01 00:00 | first |"))

    def test_changes_table_is_capped_at_five_rows(self):
        text = SAMPLE
        for i in range(8):
            text = stamp_skill.stamp(text, "change %d" % i, "2026-10-29 12:0%d" % i)
        rows = [l for l in text.split("\n") if re.match(r"\| 2\d{3}-", l)]
        self.assertEqual(len(rows), 5)
        self.assertIn("change 7", rows[0])

    def test_athens_clock_format(self):
        self.assertRegex(stamp_skill.athens_now(), r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$")


class Lint(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="wrlint-")
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.dir = os.path.join(self.tmp, "demo-skill")
        shutil.copytree(SKILL, self.dir, ignore=shutil.ignore_patterns("__pycache__", "tests"))

    def fails(self):
        return [m for lvl, m in lint_skill.lint(self.dir) if lvl == "FAIL"]

    def edit(self, fn):
        p = os.path.join(self.dir, "SKILL.md")
        t = open(p, encoding="utf-8").read()
        open(p, "w", encoding="utf-8").write(fn(t))

    def test_the_real_skill_passes(self):
        # this test is about the other checks, so make sure the copy is stamped whatever state the repo is in
        stamp_skill.apply(self.dir, "test", "2026-10-29 12:00", even_if_unchanged=True)
        self.assertEqual(self.fails(), [])

    def test_disallowed_frontmatter_key_fails(self):
        self.edit(lambda t: t.replace('name: "client-teams-transcript-skill"', 'name: "client-teams-transcript-skill"\nlast-updated: today', 1))
        self.assertTrue(any("frontmatter keys not allowed" in f for f in self.fails()))

    def test_name_with_claude_in_it_fails(self):
        self.edit(lambda t: t.replace('name: "client-teams-transcript-skill"', 'name: "claude-helper"', 1))
        self.assertTrue(any("without 'anthropic' or 'claude'" in f for f in self.fails()))

    def test_missing_index_fails(self):
        self.edit(lambda t: t.replace("## Index", "## Contents", 1))
        self.assertTrue(any("Index" in f for f in self.fails()))

    def test_section_missing_from_index_fails(self):
        self.edit(lambda t: t + "\n## A new section\n\ntext\n")
        self.assertTrue(any("Index is missing sections" in f for f in self.fails()))

    # ---- the date moves with the skill, and only with the skill (S2)
    def stamped(self):
        stamp_skill.apply(self.dir, "first stamp", "2026-10-29 12:00", even_if_unchanged=True)
        self.assertFalse([f for f in self.fails() if "stamp" in f.lower() or "Last updated" in f])

    def test_a_hand_edited_date_fails(self):
        self.stamped()
        self.edit(lambda t: re.sub(r"\*\*Last updated:[^*]*\*\*", "**Last updated: 2030-01-01 00:00 (Athens time)**", t, 1))
        self.assertTrue(any("edited by hand" in f for f in self.fails()))

    def test_no_stamp_record_fails(self):
        self.stamped()
        os.remove(os.path.join(self.dir, wr_stamp.RECORD))
        self.assertTrue(any("no stamp record" in f for f in self.fails()))

    def test_changing_a_shipped_file_without_restamping_fails(self):
        self.stamped()
        with open(os.path.join(self.dir, "references", "00-rules.md"), "a", encoding="utf-8") as f:
            f.write("\nA new rule.\n")
        self.assertTrue(any("changed after they were stamped" in f for f in self.fails()))

    def test_changing_a_program_file_without_restamping_fails(self):
        self.stamped()
        with open(os.path.join(self.dir, "scripts", "page.py"), "a", encoding="utf-8") as f:
            f.write("\n# edited\n")
        self.assertTrue(any("changed after they were stamped" in f for f in self.fails()))

    def test_restamping_after_a_change_moves_the_date(self):
        self.stamped()
        with open(os.path.join(self.dir, "steps.json"), "a", encoding="utf-8") as f:
            f.write("\n")
        self.assertTrue(any("changed after they were stamped" in f for f in self.fails()))
        stamp_skill.apply(self.dir, "second change", "2026-11-02 09:15")
        self.assertFalse([f for f in self.fails() if "stamp" in f.lower()])
        self.assertIn("**Last updated: 2026-11-02 09:15 (Athens time)**", open(os.path.join(self.dir, "SKILL.md"), encoding="utf-8").read())
        self.assertEqual(wr_stamp.read_record(self.dir)["stamp"], "2026-11-02 09:15")

    def test_the_stamp_will_not_move_when_nothing_changed(self):
        self.stamped()
        with self.assertRaises(SystemExit) as ctx:
            stamp_skill.apply(self.dir, "no real change", "2026-11-02 09:15")
        self.assertIn("Nothing in the skill has changed", str(ctx.exception))
        self.assertIn("2026-10-29 12:00", open(os.path.join(self.dir, "SKILL.md"), encoding="utf-8").read())

    def test_files_that_are_not_shipped_do_not_move_the_date(self):
        self.stamped()
        with open(os.path.join(self.dir, "README.md"), "a", encoding="utf-8") as f:
            f.write("\nnote\n")
        with open(os.path.join(self.dir, "history", "notes.txt"), "w", encoding="utf-8") as f:
            f.write("history note")
        self.assertFalse([f for f in self.fails() if "stamp" in f.lower()])

    def test_file_times_do_not_matter(self):
        # a fresh copy of the repo gives every file a new time; the date must not care
        self.stamped()
        later = os.path.getmtime(os.path.join(self.dir, "SKILL.md")) + 86400 * 30
        for root, _, files in os.walk(self.dir):
            for f in files:
                os.utime(os.path.join(root, f), (later, later))
        self.assertFalse([f for f in self.fails() if "stamp" in f.lower()])

    def test_the_stamp_and_changes_table_themselves_do_not_count_as_a_change(self):
        self.stamped()
        before = wr_stamp.fingerprint(self.dir)
        self.edit(lambda t: t.replace("first stamp", "a reworded change line", 1))
        self.assertEqual(wr_stamp.fingerprint(self.dir), before)

    def test_thirteen_digit_number_fails(self):
        self.edit(lambda t: t + "\nID 8001015009087\n")
        self.assertTrue(any("13-digit" in f for f in self.fails()))

    def test_client_name_from_blocklist_fails(self):
        bl = os.path.join(self.tmp, "names.txt")
        open(bl, "w").write("Zebediah Testname\n")
        self.edit(lambda t: t + "\nExample: Zebediah Testname\n")
        old = os.environ.get("WR_NAME_BLOCKLIST")
        os.environ["WR_NAME_BLOCKLIST"] = bl
        try:
            self.assertTrue(any("client names found" in f for f in self.fails()))
        finally:
            os.environ.pop("WR_NAME_BLOCKLIST", None)
            if old:
                os.environ["WR_NAME_BLOCKLIST"] = old

    def test_step_pointing_at_missing_page_fails(self):
        os.remove(os.path.join(self.dir, "references", "07-teams-message.md"))
        self.assertTrue(any("missing reference page" in f for f in self.fails()))

    def test_deliverable_for_unknown_step_fails(self):
        p = os.path.join(self.dir, "deliverables.json")
        d = json.load(open(p))
        d["deliverables"][0]["step"] = "nonexistent"
        json.dump(d, open(p, "w"))
        self.assertTrue(any("names step 'nonexistent'" in f for f in self.fails()))


class Inventory(unittest.TestCase):
    def run_inv(self, old, new, changes=None):
        tmp = tempfile.mkdtemp(prefix="wrinv-")
        self.addCleanup(shutil.rmtree, tmp, True)
        open(os.path.join(tmp, "old.md"), "w").write(old)
        sk = os.path.join(tmp, "skill")
        os.makedirs(sk)
        open(os.path.join(sk, "SKILL.md"), "w").write(new)
        args = [os.path.join(tmp, "old.md"), sk]
        if changes is not None:
            json.dump(changes, open(os.path.join(tmp, "c.json"), "w"))
            args += ["--changes", os.path.join(tmp, "c.json")]
        return tool("inventory.py", *args)

    OLD = "- Always save the file into the client's Fact Find folder before telling anyone it is done.\n- Never write ID numbers in any output the client will see.\n"

    def test_everything_kept_passes(self):
        r = self.run_inv(self.OLD, self.OLD)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("UNACCOUNTED: 0", r.stdout)

    def test_a_silently_lost_rule_fails(self):
        r = self.run_inv(self.OLD, "- Always save the file into the client's Fact Find folder before telling anyone it is done.\n")
        self.assertEqual(r.returncode, 1)
        self.assertIn("UNACCOUNTED: 1", r.stdout)
        self.assertIn("Never write ID numbers", r.stdout)

    def test_a_reworded_rule_needs_a_recorded_change(self):
        new = "- Save the file in the folder first.\n- Never write ID numbers in any output the client will see.\n"
        self.assertEqual(self.run_inv(self.OLD, new).returncode, 1)
        ch = [{"old": "Always save the file into the client's Fact Find folder", "new": "Save the file in the folder first.", "why": "shorter", "needs_paul": False}]
        r = self.run_inv(self.OLD, new, ch)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("reworded, with a recorded change: 1", r.stdout)

    def test_the_real_old_skill_is_fully_accounted_for(self):
        r = tool("inventory.py", os.path.join(SKILL, "history", "SKILL.2026-10-08.redacted.md"), SKILL,
                 "--changes", os.path.join(SKILL, "history", "changes.json"), "--decisions", os.path.join(SKILL, "history", "decisions.json"))
        self.assertEqual(r.returncode, 0, r.stdout[-2500:])
        self.assertIn("UNACCOUNTED: 0", r.stdout)


class Package(unittest.TestCase):
    def test_zip_holds_exactly_what_runs_and_nothing_private(self):
        out = tempfile.mkdtemp(prefix="wrpkg-")
        self.addCleanup(shutil.rmtree, out, True)
        tmp = tempfile.mkdtemp(prefix="wrcopy-")
        self.addCleanup(shutil.rmtree, tmp, True)
        copy = os.path.join(tmp, "client-teams-transcript-skill")
        shutil.copytree(SKILL, copy, ignore=shutil.ignore_patterns("__pycache__"))      # never touch the real SKILL.md
        subprocess.run([sys.executable, os.path.join(TOOLS, "stamp_skill.py"), copy, "--change", "packaging test", "--even-if-unchanged"], check=True, capture_output=True)
        r = tool("package_skill.py", copy, "--out", out, "--skip-tests")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        z = [f for f in os.listdir(out) if f.endswith(".zip")]
        self.assertEqual(len(z), 1)
        names = zipfile.ZipFile(os.path.join(out, z[0])).namelist()
        top = {n.split("/")[0] for n in names}
        self.assertEqual(top, {"client-teams-transcript-skill"})
        self.assertIn("client-teams-transcript-skill/SKILL.md", names)
        self.assertIn("client-teams-transcript-skill/scripts/run.py", names)
        self.assertIn("client-teams-transcript-skill/references/07-teams-message.md", names)
        self.assertFalse([n for n in names if "/tests/" in n or "/history/" in n or "__pycache__" in n])

    def test_packaging_refuses_when_lint_fails(self):
        out = tempfile.mkdtemp(prefix="wrpkg-")
        self.addCleanup(shutil.rmtree, out, True)
        tmp = tempfile.mkdtemp(prefix="wrbad-")
        self.addCleanup(shutil.rmtree, tmp, True)
        bad = os.path.join(tmp, "client-teams-transcript-skill")
        shutil.copytree(SKILL, bad, ignore=shutil.ignore_patterns("__pycache__"))
        os.remove(os.path.join(bad, "deliverables.json"))
        r = tool("package_skill.py", bad, "--out", out, "--skip-tests")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("PACKAGING REFUSED", r.stdout + r.stderr)
        self.assertEqual(os.listdir(out), [])


if __name__ == "__main__":
    unittest.main()
