"""Tests for reading different transcript layouts (invented data). The completeness check must never be skipped quietly."""
import os
import re
import shutil
import unittest

from test_gate import Base, FIXTURE, sh, slurp, spit


def name_then_time(text):
    """Teams layout where the time comes AFTER the speaker's name: 'Paul Kafentzis   0:05'."""
    out = []
    for ln in text.split("\n"):
        m = re.match(r"^(\d+):(\d{2}):(\d{2}) (.+)$", ln)
        out.append("%s   %d:%02d" % (m[4], int(m[1]) * 60 + int(m[2]), int(m[3])) if m else ln)
    return "\n".join(out)


class Layouts(Base):
    def prep_text(self, text, *flags):
        src = os.path.join(self.tmp, "t.txt")
        spit(src, text)
        return sh("tx.py", "prep", src, self.run_dir, *flags)

    def test_time_after_the_speaker_name_is_read(self):
        r = self.prep_text(name_then_time(slurp(FIXTURE)))
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("timestamps: 0:00:05 ->", r.stdout)
        self.assertNotIn("no timestamps", r.stdout)

    def test_truncation_is_caught_in_that_layout_too(self):
        text = name_then_time(slurp(FIXTURE)).replace("Duration: 12m 40s", "Duration: 40m 0s")
        r = self.prep_text(text)
        self.assertEqual(r.returncode, 2)
        self.assertIn("INCOMPLETE", r.stdout)

    def test_no_timestamps_stops_loudly(self):
        r = self.prep_text("Recap line one.\nRecap line two with a decision.\n")
        self.assertEqual(r.returncode, 2)
        self.assertIn("cannot be checked that the transcript is complete", r.stdout)
        self.assertIn("--notes", r.stdout)

    def test_notes_flag_allows_a_recap_and_says_so(self):
        r = self.prep_text("Recap line one.\nRecap line two with a decision.\n", "--notes")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("completeness cannot be checked", r.stdout)

    def test_force_is_still_recorded(self):
        self.prep_text("Recap line one.\nRecap line two.\n", "--force")
        self.assertTrue(self.load("state.json")["forced"])

    def test_a_spoken_time_is_not_a_timestamp(self):
        text = "Duration: 1m 0s\n\n0:00:05 Paul Kafentzis\nsee you at 4:30\n\n0:00:50 Sam Testcase\nbye\n"
        r = self.prep_text(text)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("0:00:05 -> 0:00:50", r.stdout)

    @unittest.skipUnless(shutil.which("pandoc"), "pandoc not installed")
    def test_docx_with_arrow_timestamps_is_read(self):
        md = os.path.join(self.tmp, "t.md")
        rows = []
        for ln in slurp(FIXTURE).split("\n"):
            m = re.match(r"^(\d+):(\d{2}):(\d{2}) (.+)$", ln)
            rows.append("%d:%02d:%02d.000 --> %d:%02d:%02d.900\n%s" % (int(m[1]), int(m[2]), int(m[3]), int(m[1]), int(m[2]), int(m[3]) + 1, m[4]) if m else ln)
        spit(md, "\n".join(rows))
        docx = os.path.join(self.tmp, "t.docx")
        import subprocess
        subprocess.run(["pandoc", md, "-o", docx], check=True)
        r = sh("tx.py", "prep", docx, self.run_dir)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("0:00:05 -> 0:12:", r.stdout)


if __name__ == "__main__":
    unittest.main()
