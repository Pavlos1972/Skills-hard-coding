"""The ONE test of the fact-find-summary skill (Operation Skill Restructure: one end-to-end test on invented data).

It plays a whole job through the program exactly as a chat would, on an invented client (Pat Samplecase, 05/11/2026) and an invented
Fact Find Transcript PDF: start, connect to the computer, locate, read, compose, build, check, deliver, final. On the way it proves:
  1. the driver refuses to skip a step;
  2. the computer comes first: no connection means a STOP; a PDF is never taken through Microsoft 365; a PDF taken from the computer needs the computer's own
     fingerprint (sha256 and size, pasted from device_bash); a cut-off copy is caught, and a text file or a cut-off file is never read as a PDF;
  3. the Summary saved on the computer must match the PDF built here (the computer's own fingerprint), and the finished run prints a SHORT audit of
     green ticks and RESULT: PASS;
  4. a Summary that was edited by hand is caught by the checker (a red cross), and the run no longer passes.
"""
import hashlib
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
DEVICE = ("--device", "paul-kafentzis", "--folder", "C:\\Users\\Paul\\liferisk.co.za", "--listing",
          "Fact Find Transcript - 05.11.26 - (Pat Samplecase).pdf; Teams meeting transcript - 05.11.26 - (Pat Samplecase).docx")


def run(script, *args, expect=0):
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS, script)] + list(args), capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == expect, "%s %s -> exit %d (wanted %d)\n%s\n%s" % (script, args, r.returncode, expect, r.stdout[-1500:], r.stderr[-800:])
    return r.stdout + r.stderr


def fingerprint(data, name):
    """What device_bash prints on the computer for sha256sum and stat -c %s."""
    return "%s  /home/user/mnt/liferisk.co.za/Company - Paul/New Business/Samplecase, Pat/2. Fact Find/%s\n%d\n" % (hashlib.sha256(data).hexdigest(), name, len(data))


class Journey(unittest.TestCase):
    def test_one_journey_on_invented_data(self):
        self.assertTrue(os.path.exists(FIXTURE), "the invented Fact Find Transcript PDF is missing from tests/fixtures")
        with open(FIXTURE, "rb") as fh:
            data = fh.read()
        name = os.path.basename(FIXTURE)
        good = fingerprint(data, name)
        d = tempfile.mkdtemp(prefix="wr-fs-test-")
        os.environ["WR_COMPUTER_ROOT"] = os.path.join(d, "no-such-folder")                 # nothing is mounted into this machine: the chat connects through the device tools
        R = os.path.join(d, "run")
        out = run("run.py", "start", R, "--client", "Pat Samplecase", "--date", "05/11/2026")
        self.assertIn("Using fact-find-summary, last updated", out)                       # the version is said first
        run("run.py", "done", R, "build", expect=3)                                       # 1. no step can be skipped
        # 2a. no connection: a STOP, and nothing can be logged on the computer
        self.assertIn("I could not connect this chat to your computer", run("run.py", "computer", R, "--none", "the request for folder access was refused", expect=6))
        run("run.py", "access", R, "--route", "device", "--result", "found", "--file", FIXTURE, "--device-output", good, expect=1)
        self.assertIn("could not connect this chat to your computer", run("run.py", "done", R, "locate", expect=3))
        self.assertIn("COMPUTER CONNECTED through the device tools", run("run.py", "computer", R, *DEVICE))
        # 2b. a PDF is never taken through Microsoft 365 or Zapier; the computer needs its proof
        for route in ("m365", "zapier"):
            run("run.py", "access", R, "--route", route, "--result", "found", "--note", "test", expect=1)
        run("run.py", "access", R, "--route", "device", "--result", "found", "--note", "test", expect=1)
        # 2c. a cut-off copy cannot match the computer's fingerprint; a text file is not a PDF even when its fingerprint matches its own bytes
        os.makedirs(os.path.join(d, "short"))
        short = os.path.join(d, "short", name)
        with open(short, "wb") as fh:
            fh.write(data[:1500])
        self.assertIn("logged as a FAIL", run("run.py", "access", R, "--route", "device", "--result", "found", "--file", short, "--device-output", good))
        run("run.py", "source", R, "--route", "device", "--file", short, expect=1)
        os.makedirs(os.path.join(d, "text"))
        textcopy = os.path.join(d, "text", name)
        with open(textcopy, "wb") as fh:
            fh.write(b"Fact Find Transcript Pat Samplecase 05/11/2026 (the connector's text copy)")
        run("run.py", "access", R, "--route", "device", "--result", "found", "--file", textcopy, "--device-output", fingerprint(b"Fact Find Transcript Pat Samplecase 05/11/2026 (the connector's text copy)", name))
        self.assertIn("not the whole PDF", run("run.py", "source", R, "--route", "device", "--file", textcopy, expect=4))
        # 2d. the whole file, proved identical to the computer's
        run("run.py", "access", R, "--route", "device", "--result", "found", "--note", "staged with device_stage_files", "--file", FIXTURE, "--device-output", good)
        run("run.py", "source", R, "--route", "device", "--file", FIXTURE)
        run("run.py", "done", R, "locate")
        run("run.py", "read", R)
        run("run.py", "done", R, "read")
        run("run.py", "compose", R)
        run("run.py", "done", R, "compose")
        run("run.py", "build", R)
        run("run.py", "done", R, "build")
        R2 = os.path.join(d, "run-passed")
        run("run.py", "start", R2, "--client", "Pat Samplecase", "--date", "05/11/2026")
        run("run.py", "computer", R2, *DEVICE)
        run("run.py", "access", R2, "--route", "passed", "--result", "found", "--note", "made by ff-population-transcript in this chat")
        run("run.py", "source", R2, "--file", FIXTURE, "--route", "passed")
        run("run.py", "done", R2, "locate")
        pre = run("verify.py", R, "pre")
        self.assertIn("RESULT: PASS", pre)
        run("run.py", "done", R, "check")
        pdf = os.path.join(R, "out", "Fact Find Summary - 05.11.26 - (Pat Samplecase).pdf")
        self.assertTrue(os.path.exists(pdf), "the Summary PDF was not drawn with its derived file name")
        with open(pdf, "rb") as fh:
            built = fh.read()
        pname = os.path.basename(pdf)
        listed = str(len(built))
        for k, v in (("pdf.sent", "yes"), ("pdf.saved_folder", FOLDER), ("pdf.listed_bytes", listed), ("images.looked", "yes")):
            run("run.py", "receipt", R, k, v)
        # 3. the Summary saved on the computer must be the PDF built here (the computer's own fingerprint)
        run("run.py", "receipt", R, "pdf.device_output", fingerprint(built[:-1] + b"X", pname))
        self.assertIn("is not the PDF built here", run("run.py", "done", R, "deliver", expect=3))
        run("run.py", "receipt", R, "pdf.device_output", fingerprint(built, pname))
        run("run.py", "done", R, "deliver")
        final = run("run.py", "done", R, "final")
        self.assertIn("RESULT: PASS", final)                                              # a short audit of green ticks
        audit = final[final.index("AUDIT"):].strip().splitlines()
        marks = [ln for ln in audit if ln.startswith("\u2705") or ln.startswith("\u274c")]
        self.assertLessEqual(len(audit), 30, "the audit must stay short")
        self.assertGreaterEqual(len(marks), 15)
        self.assertTrue(all(ln.startswith("\u2705") for ln in marks), "every check line must be a green tick:\n" + "\n".join(marks))
        self.assertTrue(any(ln.startswith("Only attested") for ln in audit), "the closing attested line is missing")
        # 4. a Summary edited by hand is caught
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
