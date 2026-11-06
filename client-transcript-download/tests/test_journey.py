"""The ONE test of the client-transcript-download skill (Operation Skill Restructure: one end-to-end test on invented data).

It plays whole jobs through the program exactly as a chat would, on an invented client (Pat Samplecase, 05/11/2026) and an invented
transcript (tests/fixtures/transcript_invented.txt, turned into a .docx and a WebVTT text by the test). It proves:
  1. the driver refuses to skip a step, refuses a meeting with the wrong date, and stops at the start when the computer cannot be connected;
  2. a Chrome-style job (Microsoft 365 and Zapier tried and failed first, then a Teams .docx) ends with a short audit of green ticks, the finished file
     saved on the computer and proved by the computer's own fingerprint;
  3. a cut-off transcript is caught with a red cross and is never saved as complete;
  4. a file edited by hand after the build is caught by the final checker;
  5. a connector-style job (WebVTT text) is turned into a correct .docx and also passes, with the connector's size checked to the byte
     (a wrong size is refused);
  6. the save only goes to the computer (Microsoft 365 is refused), and a saved file whose fingerprint on the computer differs from the built file is caught.
"""
import hashlib
import os
import re
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
SCRIPTS = os.path.join(SKILL, "scripts")
sys.path.insert(0, SCRIPTS)
import trread as tr  # noqa: E402

FIXTURE = os.path.join(HERE, "fixtures", "transcript_invented.txt")
FOLDER = "C:\\Users\\Paul\\liferisk.co.za\\Company - Paul\\New Business\\Samplecase, Pat\\2. Fact Find"
NAME = "Teams meeting transcript - 05.11.26 - (Pat Samplecase).docx"
DEVICE = ("--device", "paul-kafentzis", "--folder", "C:\\Users\\Paul\\liferisk.co.za", "--listing",
          "Fact Find (Audio to Text) - 05.11.2026 - Pat Samplecase.json; Fact Find Transcript - 05.11.26 - (Pat Samplecase).pdf")


def run(script, *args, expect=0):
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS, script)] + list(args), capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == expect, "%s %s -> exit %d (wanted %d)\n%s\n%s" % (script, args, r.returncode, expect, r.stdout[-1500:], r.stderr[-800:])
    return r.stdout


def fingerprint(path):
    """What device_bash prints on the computer for sha256sum and stat -c %s of the saved file."""
    with open(path, "rb") as fh:
        data = fh.read()
    return "%s  /home/user/mnt/liferisk.co.za/Company - Paul/New Business/Samplecase, Pat/2. Fact Find/%s\n%d\n" % (hashlib.sha256(data).hexdigest(), os.path.basename(path), len(data))


def to_vtt(lines):
    out, i = ["WEBVTT", ""], 0
    while i < len(lines):
        m = re.match(r"^(\d+:\d{2}:\d{2}) (.+)$", lines[i])
        if m and i + 1 < len(lines):
            out += ["%s.000 --> %s.900" % (m.group(1), m.group(1)), "<v %s>%s</v>" % (m.group(2), lines[i + 1]), ""]
            i += 2
        else:
            i += 1
    return "\n".join(out)


class Journey(unittest.TestCase):
    def start(self, d, name):
        R = os.path.join(d, name)
        out = run("run.py", "start", R, "--client", "Pat Samplecase", "--date", "05/11/2026", "--type", "first")
        self.assertIn("Using client-transcript-download, last updated", out)
        run("run.py", "computer", R, *DEVICE)
        run("run.py", "meeting", R, "--title", "Fact Find - Pat Samplecase", "--started", "05/11/2026, 17:00", "--length", "16m 30s", "--via", "chrome")
        run("run.py", "done", R, "identify")
        return R

    def finish(self, R, route_log, src, size=None, bad_fingerprint=False):
        for r, res in route_log:
            run("run.py", "access", R, "--purpose", "fetch", "--route", r, "--result", res, "--note", "test")
        extra = ["--source-size", str(size)] if size is not None else []
        run("run.py", "source", R, "--file", src, "--route", route_log[-1][0], *extra)
        run("run.py", "done", R, "fetch")
        run("run.py", "check", R)
        run("run.py", "done", R, "check")
        run("run.py", "name", R)
        run("run.py", "done", R, "name")
        out = os.path.join(R, "out", NAME)
        self.assertTrue(os.path.exists(out), "the file was not built under its derived name")
        # the save goes to the computer only; Microsoft 365 is refused
        run("run.py", "access", R, "--purpose", "save", "--route", "m365", "--result", "found", "--note", "test", expect=1)
        run("run.py", "access", R, "--purpose", "save", "--route", "device", "--result", "found", "--note", "device_commit_files")
        for k, v in (("save.folder", FOLDER), ("save.already_existed", "no"), ("save.listed_bytes", str(os.path.getsize(out)))):
            run("run.py", "receipt", R, k, v)
        if bad_fingerprint:
            run("run.py", "receipt", R, "save.device_output", fingerprint(out).replace(fingerprint(out).split("  ")[0], "0" * 64))
            self.assertIn("is not the file built here", run("run.py", "done", R, "save", expect=3))
            return out
        run("run.py", "done", R, "save", expect=3)                                         # no fingerprint from the computer yet: not proven
        run("run.py", "receipt", R, "save.device_output", fingerprint(out))
        run("run.py", "done", R, "save")
        final = run("run.py", "done", R, "final")
        self.assertIn("RESULT: PASS", final)
        audit = final[final.index("AUDIT"):].strip().splitlines()
        marks = [ln for ln in audit if ln.startswith("\u2705") or ln.startswith("\u274c")]
        self.assertLessEqual(len(audit), 20, "the audit must stay short")
        self.assertTrue(all(ln.startswith("\u2705") for ln in marks), "every check line must be a green tick:\n" + "\n".join(marks))
        self.assertTrue(any(ln.startswith("Only attested") for ln in audit))
        self.assertTrue(any(ln.startswith("Next:") for ln in audit))
        return out

    def test_one_journey_on_invented_data(self):
        d = tempfile.mkdtemp(prefix="wr-td-test-")
        with open(FIXTURE, encoding="utf-8") as f:
            lines = f.read().split("\n")
        docx = os.path.join(d, "Fact Find - Pat Samplecase.docx")
        tr.write_docx(docx, lines)
        os.environ["WR_COMPUTER_ROOT"] = os.path.join(d, "no-such-folder")                 # nothing is mounted into this machine: the chat connects through the device tools
        # 1. no step can be skipped; no connection means a STOP; a meeting on the wrong date is refused
        R0 = os.path.join(d, "run0")
        run("run.py", "start", R0, "--client", "Pat Samplecase", "--date", "05/11/2026")
        run("run.py", "done", R0, "fetch", expect=3)
        self.assertIn("I could not connect this chat to your computer", run("run.py", "computer", R0, "--none", "the request for folder access was refused", expect=6))
        warn = run("run.py", "meeting", R0, "--title", "Fact Find - Pat Samplecase", "--started", "06/11/2026, 17:00", "--length", "16m 30s", "--via", "chrome")
        self.assertIn("WARNING", warn)
        self.assertIn("could not connect this chat to your computer", run("run.py", "done", R0, "identify", expect=3))
        run("run.py", "computer", R0, *DEVICE)
        run("run.py", "done", R0, "identify", expect=3)                                    # connected now, but the date is still wrong
        # 2. a Chrome-style job: Microsoft 365 and Zapier tried first and failed, then a Teams .docx
        R1 = self.start(d, "run1")
        out = self.finish(R1, [("m365", "failed"), ("zapier", "failed"), ("chrome", "found")], docx)
        # 3. a cut-off transcript is caught and never saved as complete
        cut = os.path.join(d, "cut.docx")
        tr.write_docx(cut, lines[:60])
        R2 = self.start(d, "run2")
        run("run.py", "access", R2, "--purpose", "fetch", "--route", "m365", "--result", "found", "--note", "test")
        run("run.py", "source", R2, "--file", cut, "--route", "m365")
        bad = run("run.py", "check", R2, expect=5)
        self.assertIn("\u274c Not complete", bad)
        run("run.py", "done", R2, "check", expect=3)
        # 4. a file edited by hand after the build is caught by the final checker
        tr.write_docx(out, lines[:-8] + ["0:16:15 Someone Else", "Edited by hand."])
        self.assertIn("RESULT: FAIL", run("verify.py", R1, expect=1))
        # 5. a connector-style job: WebVTT text becomes a correct .docx and also passes
        vtt = os.path.join(d, "meeting.vtt")
        with open(vtt, "w", encoding="utf-8") as f:
            f.write(to_vtt(lines))
        R3 = self.start(d, "run3")
        run("run.py", "access", R3, "--purpose", "fetch", "--route", "m365", "--result", "found", "--note", "test")
        refused = subprocess.run([sys.executable, os.path.join(SCRIPTS, "run.py"), "source", R3, "--file", vtt, "--route", "m365", "--source-size", str(os.path.getsize(vtt) + 1)], capture_output=True, text=True, encoding="utf-8")
        self.assertNotEqual(refused.returncode, 0, "a copy of a different size must be refused")
        self.assertIn("REFUSED: the copy is", refused.stdout + refused.stderr)
        out3 = self.finish(R3, [("m365", "found")], vtt, size=os.path.getsize(vtt))
        kind, l3 = tr.read_file(out3)
        self.assertEqual(kind, "docx")
        self.assertTrue(l3[0].startswith("Meeting title: Fact Find - Pat Samplecase"))
        # 6. a saved file whose fingerprint on the computer differs from the built file is caught (the save to Microsoft 365 was refused inside finish)
        R4 = self.start(d, "run4")
        self.finish(R4, [("m365", "found")], docx, bad_fingerprint=True)


if __name__ == "__main__":
    unittest.main()
