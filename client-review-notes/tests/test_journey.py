"""The ONE test of the client-review-notes (Operation Skill Restructure: one end-to-end test on invented data).

It plays three whole jobs through the program exactly as a chat would, on invented raw notes for Pat Samplecase (tests/sample.py) with today fixed at
05/11/2026 (WR_TODAY, for tests only). Nothing is sent anywhere: the receipts are typed in, as a chat would copy them. It proves:
  1. the driver refuses to skip a step, refuses a route that was not logged, and makes the notes be read part by part in order;
  2. a bad record is refused, each for its own reason: a field not in the raw notes, a verbatim item altered, an amount dropped from a summary (the scope of a
     request lost), a 'do not contact' line missing, an expanded abbreviation, notes out of date order, HTML, a wrong Planner link, an unknown field, a date
     that is not the entry's, a wrong commission title, a policy with no DOC date;
  3. a good record is drawn in the fixed layout (the 18 fields in order, bold labels, rules, BOLD ALL CAPS dates oldest first, the do-not-contact warning at the
     top of Notes) and ends in a short audit of green ticks; a Markdown file edited by hand is caught;
  4. an earlier record of the same client is shown to Paul, nothing is merged without his words, and a merged record must keep everything from both;
  5. notes with no recognisable dates are checked over the whole note and the audit says so; the program flags a one-character difference between two contract
     numbers, a number in scientific notation and an ID that fails its check digit.
"""
import copy
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
SCRIPTS = os.path.join(SKILL, "scripts")
sys.path.insert(0, SCRIPTS)
sys.path.insert(0, HERE)
import sample  # noqa: E402

ENV = dict(os.environ, WR_TODAY="05/11/2026", WR_NOW="10:15")
MD = "Client Record - 05.11.26 - Pat Samplecase.md"


def run(script, *args, expect=0):
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS, script)] + list(args), capture_output=True, text=True, encoding="utf-8", env=ENV)
    if expect == "refused":
        assert r.returncode != 0, "%s %s should have been refused\n%s" % (script, args, r.stdout[-1500:])
    else:
        assert r.returncode == expect, "%s %s -> exit %d (wanted %d)\n%s\n%s" % (script, args, r.returncode, expect, r.stdout[-2500:], r.stderr[-1200:])
    return r.stdout + r.stderr


def jwrite(path, data):
    import json
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def readf(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


class Journey(unittest.TestCase):
    def test_journey(self):
        with tempfile.TemporaryDirectory() as d:
            self.first_run(d)
            self.duplicate_run(d)
            self.no_dates_run(d)

    def refused(self, R, d, mutate, needle):
        rec = sample.record()
        mutate(rec)
        path = os.path.join(d, "bad_record.json")
        jwrite(path, rec)
        self.assertIn(needle, run("run.py", "record", R, "--file", path, expect=5))

    # ------------------------------------------------------------------ the first job
    def first_run(self, d):
        raw = os.path.join(d, "raw.txt")
        write(raw, sample.raw_notes())
        R = os.path.join(d, "run1")
        out = run("run.py", "start", R, "--client", "Pat Samplecase")
        self.assertIn("Using client-review-notes, last updated", out)
        self.assertIn("STEP 1 of 6", out)
        self.assertIn("finish step 'source' first", run("run.py", "done", R, "read", expect=3))
        self.assertIn("record the access try first", run("run.py", "notes", R, "--file", raw, "--route", "m365", expect="refused"))
        out = run("run.py", "notes", R, "--file", raw, "--route", "pasted")
        self.assertIn("3 dated entries recognised", out)
        run("run.py", "done", R, "source")
        self.assertIn("missing its proof", run("run.py", "done", R, "read", expect=3))
        self.assertIn("RAW NOTES - PART 1 of 1", run("run.py", "read", R))
        self.assertIn("acknowledged in order", run("run.py", "read", R, "--ack", "2", "--note", "x", expect="refused"))
        self.assertIn("one-line note", run("run.py", "read", R, "--ack", "1", "--note", "", expect="refused"))
        run("run.py", "read", R, "--ack", "1", "--note", "header fields, policies, commission and three dated entries")
        run("run.py", "done", R, "read")
        self.assertIn("nothing to decide", run("run.py", "duplicate", R, "--decision", "merge", "--said", "Paul: merge them"))
        run("run.py", "done", R, "duplicates")
        # ---- bad records are refused, each for its own reason
        self.refused(R, d, lambda r: r["fields"].update({"Full Name": "Patricia Samplecase"}), "is not in the raw notes")
        self.refused(R, d, lambda r: r["fields"]["Life & Investments"]["previous"][0].update(contract="SL-123457"), "is not in the raw notes")
        self.refused(R, d, lambda r: r["notes"]["blocks"][0].update(bullets=["Client asked which OM products (RA 123456789, Tax-Free 987654321) to withdraw. Called Alwyn Van Tonder."]), "amount: r70k")
        self.refused(R, d, lambda r: r["notes"]["blocks"][1].update(bullets=["Old Mutual AML reminder REF 5566778 completed."]), "do not contact")
        self.refused(R, d, lambda r: r["notes"]["blocks"][0]["bullets"].append("A Financial Needs Analysis was discussed."), "expands FNA")
        self.refused(R, d, lambda r: r["notes"]["blocks"].reverse(), "oldest first")
        self.refused(R, d, lambda r: r["notes"]["blocks"][1]["bullets"].append("<u>MARCH</u> was busy"), "HTML is not allowed")
        self.refused(R, d, lambda r: r["notes"]["blocks"][2].update(bullets=["Review task created: https://planner.cloud.microsoft/webui/task/AbC123. LOA sent to 4455667."]), "Planner link must read")
        self.refused(R, d, lambda r: r["fields"].update(Nickname="Patty"), "is not one of the 18 fields")
        self.refused(R, d, lambda r: r["notes"]["blocks"][0].update(date="2023-01-01"), "is not the date of entry")
        self.refused(R, d, lambda r: r["fields"]["Commission"][0].update(title="BrightRock Personal Covers"), "the title must read")
        self.refused(R, d, lambda r: r["fields"]["Life & Investments"]["current"][0].pop("doc"), "contract, product and doc are needed")
        # ---- the good record
        good = os.path.join(d, "record1.json")
        jwrite(good, sample.record())
        out = run("run.py", "record", R, "--file", good)
        self.assertIn("RECORD BUILT: out/" + MD, out)
        self.assertIn("Left out on purpose: nothing", out)
        md = readf(os.path.join(R, "out", MD))
        self.assertTrue(md.startswith("Pat (Patty) Samplecase (Client / BrightRock Lead) (%s)" % sample.PAT_ID))
        labels = [l for l in md.splitlines() if l.startswith("**") and l.endswith(":**")]
        self.assertEqual(labels[:4], ["**Full Name:**", "**Last Name:**", "**First Name:**", "**Known As:**"])
        self.assertEqual(labels[-3:], ["**Life & Investments:**", "**Notes:**", "**Commission:**"])
        self.assertEqual(len(labels), 18)
        self.assertIn("**Life & Investments:**\n\n*Previous/Replaced Policies:*\n- Contract: SL-123456 (Samplelife Risk Cover) DOC 01/06/2015 / R 950.00 / REPLACED", md)
        self.assertIn("*Non-active/Lapsed Policies:*\n- Contract: 4455667 (Testco Endowment) DOC 15/09/2012 / R 500.00 / LAPSED", md)
        self.assertIn('⚠️ DO NOT CONTACT: "MARCH 2024 Old Mutual AML reminder REF 5566778 completed. Do not contact the client by phone before 10:00."', md)
        self.assertLess(md.index("**14 FEBRUARY 2022**"), md.index("**MARCH 2024**"))
        self.assertLess(md.index("**MARCH 2024**"), md.index("**5 NOVEMBER 2026**"))
        self.assertIn("[Planner – Review task](%s)" % sample.URL, md)
        self.assertNotIn("<", md.replace("<u>", ""))
        run("run.py", "done", R, "record")
        self.assertIn("missing its proof", run("run.py", "done", R, "deliver", expect=3))
        run("run.py", "receipt", R, "chat.sent", "yes")
        run("run.py", "done", R, "deliver")
        out = run("run.py", "done", R, "final")
        self.assertIn("RESULT: PASS", out)
        self.assertFalse([l for l in out.splitlines() if l.startswith("❌")], out)
        self.assertIn("Only attested (not proven):", out)
        self.assertIn("FOR PAUL", out)
        self.assertIn("3 dated entries recognised", out)
        self.assertNotIn(sample.PAT_ID, out)
        self.assertIn("\u2022\u2022\u2022", out + run("run.py", "record", R, "--file", good))
        self.assertEqual(run("verify.py", R).count("RESULT: PASS"), 1)
        # ---- a Markdown file edited by hand is caught
        T = os.path.join(d, "run1_tampered")
        shutil.copytree(R, T)
        write(os.path.join(T, "out", MD), md.replace("R 950.00", "R 960.00"))
        self.assertIn("RESULT: FAIL", run("verify.py", T, expect=1))
        self.run1_md = os.path.join(R, "out", MD)

    # ------------------------------------------------------------------ an earlier record of the same client
    def duplicate_run(self, d):
        raw = os.path.join(d, "raw2.txt")
        write(raw, sample.raw_notes())
        R = os.path.join(d, "run2")
        run("run.py", "start", R, "--client", "Pat Samplecase")
        run("run.py", "notes", R, "--file", raw, "--route", "pasted")
        run("run.py", "earlier", R, "--id", "e1", "--file", self.run1_md, "--route", "pasted")
        run("run.py", "done", R, "source")
        run("run.py", "read", R, "--ack", "1", "--note", "everything")
        run("run.py", "done", R, "read")
        self.assertIn("missing its proof", run("run.py", "done", R, "duplicates", expect=3))
        self.assertIn("own words", run("run.py", "duplicate", R, "--decision", "merge", "--said", "ok", expect="refused"))
        run("run.py", "duplicate", R, "--decision", "merge", "--said", "Paul: yes merge it into one record")
        run("run.py", "done", R, "duplicates")
        rec = sample.record()
        path = os.path.join(d, "record2.json")
        jwrite(path, rec)
        self.assertIn("merge_notes", run("run.py", "record", R, "--file", path, expect=5))
        rec["merge_notes"] = ["the earlier record added nothing the new notes lack; both versions agree"]
        jwrite(path, rec)
        run("run.py", "record", R, "--file", path)
        md = readf(os.path.join(R, "out", MD))
        self.assertIn("⚠️ Merged record: the earlier record added nothing", md)
        run("run.py", "done", R, "record")
        run("run.py", "receipt", R, "chat.sent", "yes")
        run("run.py", "done", R, "deliver")
        out = run("run.py", "done", R, "final")
        self.assertIn("RESULT: PASS", out)
        self.assertIn("Paul decided to merge", out)

    # ------------------------------------------------------------------ notes with no dates, and what the program flags
    def no_dates_run(self, d):
        bad_id = sample.make_id("800101" + "5009" + "08", ok=False)
        raw = "\n".join(["Pat Samplecase notes", "Client ID No: " + bad_id, "Contract 4455667 premium R 500.00; later notes say contract 4455668.", "Imprecise ID 8.0E+12 in the old system."]) + "\n"
        rawf = os.path.join(d, "raw3.txt")
        write(rawf, raw)
        R = os.path.join(d, "run3")
        run("run.py", "start", R, "--client", "Pat Samplecase")
        out = run("run.py", "notes", R, "--file", rawf, "--route", "pasted")
        self.assertIn("no recognisable dated entries", out)
        run("run.py", "done", R, "source")
        run("run.py", "read", R, "--ack", "1", "--note", "four short lines")
        run("run.py", "done", R, "read")
        run("run.py", "done", R, "duplicates")
        rec = {"fields": {"Full Name": "Pat Samplecase", "First Name": "Pat", "Last Name": "Samplecase", "Client ID No": bad_id},
               "notes": {"blocks": [{"from": [1], "bullets": ["Contract 4455667 premium R 500.00; later notes say contract 4455668.", "Imprecise ID 8.0E+12 in the old system."]}]}}
        path = os.path.join(d, "record3.json")
        jwrite(path, rec)
        out = run("run.py", "record", R, "--file", path)
        self.assertIn("FLAG", out)
        md = readf(os.path.join(R, "out", MD))
        self.assertIn("⚠️ apparent typo: the numbers 4455667 and 4455668 differ by one character", md)
        self.assertIn("scientific notation", md)
        self.assertIn("fails its check digit", md)
        self.assertIn("**UNDATED NOTES**", md)
        self.assertIn("**Known As:**\nNot recorded.", md)
        self.assertIn("- Not recorded.", md)
        run("run.py", "done", R, "record")
        run("run.py", "receipt", R, "chat.sent", "yes")
        run("run.py", "done", R, "deliver")
        out = run("run.py", "done", R, "final")
        self.assertIn("RESULT: PASS", out)
        self.assertIn("NO dated entries recognised", out)
        self.assertIn("only the whole note was compared", out)


if __name__ == "__main__":
    unittest.main()
