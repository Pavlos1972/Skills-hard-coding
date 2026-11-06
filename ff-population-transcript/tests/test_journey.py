"""The ONE test of the ff-population-transcript skill (Operation Skill Restructure 2.0): a whole run, start to finish, on an invented client.

Run from the skill folder:  python3 -m unittest discover -s tests -v
(WR_SCRIPTS=<folder of the programs> tests the programs of an unpacked zip instead.)

Invented people only (Pat Samplecase). The journey follows the eight steps exactly as the chat must, and on the way checks that the
program refuses what a careless chat would do: skip a step, read the transcript out of order, quote words that are not in the call,
use a stale report, and report a save that did not match.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.environ.get("WR_SCRIPTS") or os.path.join(os.path.dirname(HERE), "scripts")
sys.path.insert(0, HERE)
from fixtures import household  # noqa: E402

ENV = dict(os.environ, WR_CHUNK_LINES="30")


def sh(script, *args, env=None):
    return subprocess.run([sys.executable, os.path.join(SCRIPTS, script)] + [str(a) for a in args], capture_output=True, text=True, env=env or ENV, timeout=300)


def money_commas(v):
    m = re.fullmatch(r"R ([\d ]+)\.(\d\d)", v)
    return v if not m else "R" + format(int(m.group(1).replace(" ", "")), ",") + "." + m.group(2)


def make_form_pdf(path, form, extra_lines=()):
    """The form's saved PDF, made from the invented data file: every populated value printed, plus amounts the form works out itself."""
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(path, pagesize=A4)
    y = 800
    lines = ["CLIENT FACT FIND   Pat Samplecase Completed %s | Advisor Paul Kafentzis" % household.DATE, "WR Fact Find v3.0 (invented test client)"]
    for k, cell in form["f"].items():
        if k == "pa_actions" or not cell["v"].strip():
            continue
        lines.append("%s: %s" % (k, money_commas(cell["v"].strip())))
    for name, rows in form["l"].items():
        for i, row in enumerate(rows):
            for col, v in row["d"].items():
                if v:
                    lines.append("%s %d %s: %s" % (name, i + 1, col, money_commas(v)))
    lines += list(extra_lines)
    for ln in lines:
        if y < 40:
            c.showPage()
            y = 800
        c.drawString(40, y, ln[:110])
        y -= 13
    c.save()


class Journey(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="wrff-")
        if os.environ.get("WR_KEEP"):                    # keep the run folder to look at it (not used by the test itself)
            print("run folder kept: " + self.tmp)
        else:
            self.addCleanup(shutil.rmtree, self.tmp, True)
        self.run_dir = os.path.join(self.tmp, "run")
        self.form_path = os.path.join(self.tmp, "Fact Find (Audio to Text) - 05.11.2026 - Pat Samplecase.json")
        self.pdf_path = os.path.join(self.tmp, "Fact Find (Audio to Text) - 05.11.2026 - Pat Samplecase.pdf")
        self.call_path = os.path.join(self.tmp, "Teams meeting transcript - 05.11.26 - Pat Samplecase.txt")
        self.overview_path = os.path.join(self.tmp, "WR Overview - Pat Samplecase.txt")
        form = household.pat_form()
        with open(self.form_path, "w", encoding="utf-8") as f:
            json.dump(form, f)
        make_form_pdf(self.pdf_path, form, extra_lines=["Direct Net Income (R p.m.)   R 36 111.11   Total Income   R 99 999.00"])
        shutil.copyfile(os.path.join(HERE, "fixtures", "transcript_ff.txt"), self.call_path)
        with open(self.overview_path, "w", encoding="utf-8") as f:
            f.write("WR Overview (invented): BrightRock life cover R 1 100.00 per month. Classic Smart plan.")

    # ---- helpers
    def ok(self, script, *args):
        r = sh(script, *args)
        self.assertEqual(r.returncode, 0, "%s %s\n%s%s" % (script, args, r.stdout, r.stderr))
        return r

    def refused(self, script, *args, text=None):
        r = sh(script, *args)
        self.assertNotEqual(r.returncode, 0, "expected a refusal: %s %s\n%s%s" % (script, args, r.stdout, r.stderr))
        if text:
            self.assertIn(text, r.stdout + r.stderr)
        return r

    def load(self, name):
        with open(os.path.join(self.run_dir, name), encoding="utf-8") as f:
            return json.load(f)

    def line_of(self, words):
        with open(os.path.join(self.run_dir, "transcript.txt"), encoding="utf-8") as f:
            for i, ln in enumerate(f.read().split("\n"), 1):
                if words in ln:
                    return i
        raise AssertionError(words)

    def overlay(self, **extra):
        ov = {
            "fills": [{"id": "f1", "key": "edu_notes", "value": "One-year diploma after school", "src": [{"line": self.line_of("one-year diploma"), "quote": "I did a one-year diploma after school"}]}],
            "diffs": [
                {"id": "d1", "key": "edu", "other": "a one-year diploma", "label": "the call",
                 "src": [{"line": self.line_of("one-year diploma"), "quote": "I did a one-year diploma after school, nothing more"}]},
                {"id": "d2", "key": "ma_plan", "other": "Classic Smart", "label": "the Overview", "settled": "the Overview is a spreadsheet; the plan name on the schedule decides, so the form's value is kept",
                 "src": [{"doc": "Overview", "quote": "Classic Smart plan"}]},
            ],
        }
        ov.update(extra)
        with open(os.path.join(self.run_dir, "overlay.json"), "w", encoding="utf-8") as f:
            json.dump(ov, f)

    # ---- the journey
    def test_a_whole_run_from_start_to_the_audit(self):
        run = self.run_dir
        # step 0: the run starts, says its version, shows the rules and step 1
        out = self.ok("run.py", "start", run, "--client", "Pat Samplecase", "--date", "05/11/2026").stdout
        self.assertIn("SELF-TEST", out)
        self.assertIn("SAY THIS TO PAUL FIRST", out)
        self.assertIn("STEP 1 of 8", out)
        self.assertNotIn("sha256sum", out)                                   # no shell command on Paul's laptop, no fingerprint gate
        # a step cannot be skipped, and a step without its proof is refused
        self.refused("run.py", "done", run, "read", text="finish step 'find' first")
        r = sh("run.py", "done", run, "find")
        self.assertEqual(r.returncode, 1)
        self.assertIn("no files registered", r.stdout)
        # step 1: the files are recognised by their content; a wrong client is refused
        other = os.path.join(self.tmp, "other.json")
        bad = household.pat_form()
        bad["f"]["fname"]["v"] = "Someone"
        with open(other, "w", encoding="utf-8") as f:
            json.dump(bad, f)
        self.refused("run.py", "files", run, "--form", other, "--transcript", self.call_path, text="not the right form file")
        self.ok("run.py", "files", run, "--form", self.form_path, "--formpdf", self.pdf_path, "--transcript", self.call_path, "--overview", self.overview_path)
        self.assertTrue(self.load("form_pdf.json")["used"])
        self.assertTrue(self.load("state.json")["complete"])
        self.assertIn("STEP 'find' DONE", self.ok("run.py", "done", run, "find").stdout)
        # step 2: the program reads both form files and prints the list to act on
        form_out = self.ok("run.py", "form", run).stdout
        self.assertIn("PRESET values", form_out)
        self.assertIn("COMPANY LOOK-UP TEXT: THROWN OUT", form_out)           # the look-up wrote chatter into the field
        self.assertIn("AMOUNTS ONLY THE PDF HOLDS", form_out)
        self.assertIn("99999.00", form_out.replace(" ", ""))
        self.ok("run.py", "done", run, "form")
        # step 3: the transcript is handed over in order, twice
        k = len(self.load("state.json")["chunks"])
        self.assertGreater(k, 1)
        self.refused("tx.py", "chunk", run, 1, 2, text="read the chunks in order")
        self.refused("tx.py", "chunk", run, 2, 1, text="Pass 2 starts only after Pass 1")
        self.refused("run.py", "done", run, "read", text="Pass 1 has not served every chunk")
        for p in (1, 2):
            for n in range(1, k + 1):
                self.ok("tx.py", "chunk", run, p, n)
        self.ok("run.py", "done", run, "read")
        # step 4: contact details and the lead source
        self.ok("run.py", "lead", run, "--none", "searched Leads - D&R Marketing and the whole mailbox: no appointment email for this client")
        self.ok("run.py", "done", run, "lead")
        # step 5: ONE combined report. An empty overlay first: the program lists what is still empty
        first = self.ok("run.py", "combine", run).stdout
        self.assertIn("COMBINED content.json", first)
        self.assertIn("rows still 'Not discussed'", first)
        self.refused("run.py", "done", run, "build", text="finish step 'combine' first")
        # an invented quote is refused (the program checks the words are really in the call)
        self.overlay(fills=[{"id": "f1", "key": "edu_notes", "value": "Invented", "src": [{"line": 5, "quote": "Pat told us she has a pilot licence"}]}])
        self.refused("run.py", "combine", run, text="not in the transcript")
        self.overlay()
        out = self.ok("run.py", "combine", run).stdout
        self.assertIn("2 (1 SORTED by a rule, 1 HIGHLIGHTED for Paul)", out)
        c = self.load("content.json")
        self.assertEqual(c["report"]["sorted"], 1)
        self.assertEqual(c["report"]["highlighted"], 1)
        self.assertTrue(c["pdf_fields"], "the amounts only the PDF holds are printed under their own heading")
        rows = {r["id"]: r for s in c["sections"] for b in s["blocks"] for r in b["rows"]}
        self.assertEqual(rows["dd_abiv"]["bullets"], ["3%"])                  # the standing Dread Disease ABI
        self.assertEqual(rows["lc_wol"]["bullets"], ["3%"])                    # the form's preset 5% is replaced by the standing 3%
        self.assertTrue(any("Difference: the form says 3-year degree" in f["text"] for f in rows["edu"]["flags"]))
        self.assertTrue(any("Settled:" in f["text"] for f in rows["ma_plan"]["flags"]))
        self.assertEqual(rows["fname"]["bullets"], ["Pat"])                    # the trailing space of the form is tidied
        self.ok("run.py", "done", run, "combine")
        # step 6: build, then look at the pages
        self.refused("run.py", "done", run, "build", text="not built from the current report")
        out = self.ok("run.py", "build", run).stdout
        self.assertIn("BUILT", out)
        pdf = os.path.join(run, "out", "Fact Find Transcript - 05.11.26 - (Pat Samplecase).pdf")
        self.assertTrue(os.path.getsize(pdf) > 3000)
        self.refused("run.py", "done", run, "build", text="were not looked at")
        self.refused("run.py", "look", run, "--saw", "ok", text="at least 20 characters")
        self.ok("run.py", "look", run, "--saw", "every page: navy headings, two-column tables, notes in point form, nothing cut off")
        self.ok("run.py", "done", run, "build")
        # step 7: a save that does not match is refused; the right size is recorded; Paul's OK is recorded
        size = os.path.getsize(pdf)
        self.refused("run.py", "saved", run, "--folder", "C:\\x\\2. Fact Find", "--listed-size", size - 1000, text="NOT THE SAME SIZE")
        self.ok("run.py", "saved", run, "--folder", "C:\\x\\2. Fact Find", "--listed-size", size)
        self.refused("run.py", "chain", run, "--summary", "s", "--planner", "p", "--sitamah", "m", text="Paul's OK")
        self.refused("run.py", "done", run, "save", text="OK of this version is not recorded")
        rep = self.ok("run.py", "report", run).stdout
        self.assertIn("Contradictions: 2 (1 sorted, 1 highlighted)", rep)
        self.ok("run.py", "ok", run, "--paul-said", "Yes, that is right")
        self.ok("run.py", "done", run, "save")
        # a correction re-opens everything after it
        self.overlay(notes=[{"id": "n1", "section": "income", "text": "Pat will email the latest payslip", "src": [{"line": self.line_of("email it tomorrow"), "quote": "I will email it tomorrow"}]}])
        again = self.ok("run.py", "combine", run).stdout
        self.assertIn("RE-OPENED because the report changed", again)
        r = sh("run.py", "done", run, "build")
        self.assertEqual(r.returncode, 1)                                      # the driver is back at the build step: the old PDF is not accepted
        self.assertIn("not built from the current report", r.stdout)
        r = sh("run.py", "done", run, "save")
        self.assertEqual(r.returncode, 3)                                      # and the later steps are closed again
        self.assertIn("finish step 'build' first", r.stderr)
        self.ok("run.py", "build", run)
        self.ok("run.py", "look", run, "--saw", "every page again: headings, tables, the new note under Income, nothing cut off")
        self.ok("run.py", "done", run, "build")
        pdf = os.path.join(run, "out", "Fact Find Transcript - 05.11.26 - (Pat Samplecase).pdf")
        self.ok("run.py", "saved", run, "--folder", "C:\\x\\2. Fact Find", "--listed-size", os.path.getsize(pdf))
        self.ok("run.py", "ok", run, "--paul-said", "Yes, send it on")
        self.ok("run.py", "done", run, "save")
        # step 8: the three outputs are recorded and the short audit is printed
        final = self.ok("run.py", "chain", run, "--summary", "Fact Find Summary - 05.11.26 - (Pat Samplecase).pdf", "--planner", "https://claude.ai/artifact/x",
                        "--sitamah", "posted: message id 123").stdout
        self.assertIn("recorded the three outputs", final)
        done = self.ok("run.py", "done", run, "chain").stdout
        self.assertIn("RESULT: PASS", done)
        self.assertIn("ONE combined report", done)
        self.assertIn("DELIVERY LINE", done)
        self.assertLessEqual(len(done.split("DELIVERY LINE")[0].splitlines()), 40)     # a SHORT audit, never a long printout
        self.assertTrue(os.path.exists(os.path.join(run, "out_record", "audit-full.txt")))
        # the programs must not be edited during a run: the run remembers their fingerprint and the audit checks it
        self.assertTrue(self.load("run.json")["program_fp"])


if __name__ == "__main__":
    unittest.main()
