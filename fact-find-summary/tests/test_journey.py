"""The ONE test of the fact-find-summary skill (Operation Skill Restructure: one end-to-end test on invented data).

It plays a whole job through the program exactly as a chat would, on an invented client (Pat Samplecase, 05/11/2026) and an invented
Fact Find Transcript PDF: start, locate, read, compose, build, check, deliver, final. On the way it proves three things:
  1. the driver refuses to skip a step;
  2. the finished run prints a SHORT audit of green ticks and RESULT: PASS;
  3. a Summary that was edited by hand is caught by the checker (a red cross), and the run no longer passes.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
SCRIPTS = os.path.join(SKILL, "scripts")
FIXTURE = os.path.join(HERE, "fixtures", "Fact Find Transcript - 05.11.26 - (Pat Samplecase).pdf")
FOLDER = "C:\\Users\\Paul\\liferisk.co.za\\Company - Paul\\New Business\\Samplecase, Pat\\2. Fact Find"


def run(script, *args, expect=0):
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS, script)] + list(args), capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == expect, "%s %s -> exit %d (wanted %d)\n%s\n%s" % (script, args, r.returncode, expect, r.stdout[-1500:], r.stderr[-800:])
    return r.stdout


class Journey(unittest.TestCase):
    def test_one_journey_on_invented_data(self):
        self.assertTrue(os.path.exists(FIXTURE), "the invented Fact Find Transcript PDF is missing from tests/fixtures")
        d = tempfile.mkdtemp(prefix="wr-fs-test-")
        R = os.path.join(d, "run")
        out = run("run.py", "start", R, "--client", "Pat Samplecase", "--date", "05/11/2026")
        self.assertIn("Using fact-find-summary, last updated", out)                       # the version is said first
        run("run.py", "done", R, "build", expect=3)                                       # 1. no step can be skipped
        # the way in (Paul, 05/11/2026): the computer is logged at once as not connected, Microsoft 365 finds the PDF, the copy must have the connector's size
        run("run.py", "access", R, "--route", "device", "--result", "failed", "--note", "not connected; not requested")
        run("run.py", "access", R, "--route", "m365", "--result", "found", "--note", "test")
        size = str(os.path.getsize(FIXTURE))
        run("run.py", "source", R, "--file", FIXTURE, "--route", "m365", "--source-size", str(int(size) - 1), expect=1)   # a copy of the wrong size is refused
        run("run.py", "source", R, "--file", FIXTURE, "--route", "m365", "--source-size", size)
        run("run.py", "done", R, "locate")
        run("run.py", "read", R)
        run("run.py", "done", R, "read")
        run("run.py", "compose", R)
        run("run.py", "done", R, "compose")
        run("run.py", "build", R)
        run("run.py", "done", R, "build")
        R2 = os.path.join(d, "run-passed")
        run("run.py", "start", R2, "--client", "Pat Samplecase", "--date", "05/11/2026")
        run("run.py", "access", R2, "--route", "passed", "--result", "found", "--note", "made by ff-population-transcript in this chat")
        run("run.py", "source", R2, "--file", FIXTURE, "--route", "passed")
        run("run.py", "done", R2, "locate")
        pre = run("verify.py", R, "pre")
        self.assertIn("RESULT: PASS", pre)
        run("run.py", "done", R, "check")
        pdf = os.path.join(R, "out", "Fact Find Summary - 05.11.26 - (Pat Samplecase).pdf")
        self.assertTrue(os.path.exists(pdf), "the Summary PDF was not drawn with its derived file name")
        for k, v in (("pdf.sent", "yes"), ("pdf.saved_folder", FOLDER), ("pdf.listed_bytes", str(os.path.getsize(pdf))), ("images.looked", "yes")):
            run("run.py", "receipt", R, k, v)
        run("run.py", "done", R, "deliver")
        final = run("run.py", "done", R, "final")
        self.assertIn("RESULT: PASS", final)                                              # 2. a short audit of green ticks
        audit = final[final.index("AUDIT"):].strip().splitlines()
        marks = [ln for ln in audit if ln.startswith("\u2705") or ln.startswith("\u274c")]
        self.assertLessEqual(len(audit), 30, "the audit must stay short")
        self.assertGreaterEqual(len(marks), 15)
        self.assertTrue(all(ln.startswith("\u2705") for ln in marks), "every check line must be a green tick:\n" + "\n".join(marks))
        self.assertTrue(any(ln.startswith("Only attested") for ln in audit), "the closing attested line is missing")
        # 3. a Summary edited by hand is caught
        cpath = os.path.join(R, "content.json")
        with open(cpath, encoding="utf-8") as f:
            c = json.load(f)
        c["sections"][0]["blocks"][0]["rows"][0]["values"] = ["Someone Else"]
        with open(cpath, "w", encoding="utf-8") as f:
            json.dump(c, f)
        bad = run("verify.py", R, expect=1)
        self.assertIn("\u274c content.json is exactly what the program composes", bad)
        self.assertIn("RESULT: FAIL", bad)


if __name__ == "__main__":
    unittest.main()
