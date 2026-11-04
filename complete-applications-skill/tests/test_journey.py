"""The ONE test of the complete-applications-skill (Operation Skill Restructure: one end-to-end test on invented data).

It plays two whole jobs through the program exactly as a chat would, on the REAL blank forms in assets/ and an invented client (Pat Samplecase, with an
invented Fact Find Summary and an invented policy schedule drawn by tests/sample.py) with today fixed at 05/11/2026 (WR_TODAY, for tests only). Nothing is
saved anywhere: the folder listings and receipts are typed in, as a chat would copy them. It proves:
  1. the driver refuses to skip a step and refuses a route used before the earlier ones failed;
  2. bad plans are refused, each for its own reason: a value not in its evidence line, a value that is not one of the form's options, a field the program
     builds, a missing or unproved replacement answer, a debit date from the 10th to the 14th, a file that already exists, a new insurer with no
     abbreviation, a product that is not on the form, a signature field, a value with no proof, a transaction folder that is not the current one;
  3. a pre-fill of an Old Mutual and a General Short Risk application is built (names from fixed lists, the N/A rules, the replacement answer, the signature
     date), shown, approved, filled, read back field by field, proved to draw, saved, a transaction folder renamed, and ends in a short audit of green ticks
     with a hand-back that masks ID and account numbers;
  4. nothing is filled before Paul's yes; a save with no receipt or no file in the listing, and a rename that left the old folder behind, are caught;
  5. a PDF edited by hand after the run, and a form that has changed, are caught;
  6. a correction reads the current applications, refuses a product-specific detail, a signature field and a conflict between two current applications,
     carries an account number only with Paul's words, changes ONLY the planned fields, and needs the same staged and committed modified time.
"""
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
import apps as A  # noqa: E402
import sample  # noqa: E402
import wrlib as w  # noqa: E402

ENV = dict(os.environ, WR_TODAY="05/11/2026", WR_NOW="10:15")
A1 = "OM - Optimal RA Application - 20.11.26 - R 2,800.00 p.m. - (Pat Samplecase).pdf"
A2 = "BR - Personal Covers Application - 20.11.26 - R 1,000.00 p.m. - (Pat Samplecase).pdf"
F1 = "Samplecase, Pat - (OM - Optimal RA - Recurring - R 2,800.00 p.m.)"


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
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


class Journey(unittest.TestCase):
    def test_journey(self):
        with tempfile.TemporaryDirectory() as d:
            self.first_run(d)
            self.second_run(d)
            self.form_drift(d)

    def receipt(self, R, key, value):
        run("run.py", "receipt", R, key, value)

    def refused_plan(self, R, d, mutate, needle):
        pl = sample.plan_prefill()
        mutate(pl)
        path = os.path.join(d, "bad_plan.json")
        jwrite(path, pl)
        out = run("run.py", "plan", R, "--file", path, expect=5)
        self.assertIn(needle, out)

    # ------------------------------------------------------------------ the pre-fill
    def first_run(self, d):
        ff = os.path.join(d, "Fact Find Summary.pdf")
        sch = os.path.join(d, "Policy Schedule.pdf")
        sample.make_pdf(ff, sample.FF)
        sample.make_pdf(sch, sample.SCHEDULE)
        R = os.path.join(d, "run1")
        out = run("run.py", "start", R, "--client", "Pat Samplecase", "--mode", "prefill")
        self.assertIn("Using complete-applications-skill, last updated", out)
        self.assertIn("STEP 1 of 6", out)
        self.assertIn("the blank Old Mutual application form is the one this skill knows", out)
        self.assertIn("finish step 'locate' first", run("run.py", "done", R, "plan", expect=3))
        run("run.py", "access", R, "--purpose", "docs", "--route", "m365", "--result", "found", "--note", "too early")
        self.assertIn("tried in order", run("run.py", "doc", R, "--role", "fact_find", "--file", ff, "--route", "m365", expect="refused"))
        shutil.rmtree(R)
        run("run.py", "start", R, "--client", "Pat Samplecase", "--mode", "prefill")
        run("run.py", "access", R, "--purpose", "folder", "--route", "device", "--result", "found", "--note", "New Business\\Samplecase, Pat and its Applications folder")
        run("run.py", "access", R, "--purpose", "docs", "--route", "device", "--result", "found", "--note", "Fact Find Summary and policy schedule")
        run("run.py", "doc", R, "--role", "fact_find", "--file", ff, "--route", "device")
        run("run.py", "doc", R, "--role", "policy_schedule", "--file", sch, "--route", "device")
        run("run.py", "done", R, "locate")
        # ---- bad plans are refused, each for its own reason
        self.refused_plan(R, d, lambda p: p["apps"][0]["fields"]["IDNumber"].update(value=sample.make_id("800101" + "5009" + "09")), "not in its evidence line")
        self.refused_plan(R, d, lambda p: p["apps"][0]["fields"]["Title"].update(value="Lord"), "not one of the form's options")
        self.refused_plan(R, d, lambda p: p["apps"][0]["fields"].update(ForeignTaxNumber={"value": "123", "paul_said": "typed by hand"}), "built by the program")
        self.refused_plan(R, d, lambda p: p["apps"][0].pop("replacement"), "real answer")
        self.refused_plan(R, d, lambda p: p["apps"][1]["replacement"]["policies"][0]["evidence"].update(line="Monthly premium R 950.00"), "not in its schedule line")
        self.refused_plan(R, d, lambda p: p["apps"][1]["fields"]["debit_date"].update(value="12th"), "10th to the 14th")
        self.refused_plan(R, d, lambda p: p["listing"]["applications"].append(A1), "already exists")
        self.refused_plan(R, d, lambda p: p["apps"][1].update(insurer={"name": "Liberty"}), "file name cannot be built")
        self.refused_plan(R, d, lambda p: p["apps"][0]["product"].update(option="OM Nonsense"), "not one of the form's products")
        self.refused_plan(R, d, lambda p: p["apps"][0]["fields"].update(Signature={"value": "x", "paul_said": "she signs"}), "never written")
        self.refused_plan(R, d, lambda p: p["apps"][0]["fields"]["Occupation"].pop("evidence"), "no proof")
        self.refused_plan(R, d, lambda p: p["apps"][0]["txn_folder"].pop("is_current_transaction"), "txn_folder needs")
        self.refused_plan(R, d, lambda p: p["apps"][0]["product"].update(type="Monthly"), "folder name cannot be built")
        # ---- the good plan
        ppath = os.path.join(d, "plan1.json")
        jwrite(ppath, sample.plan_prefill())
        out = run("run.py", "plan", R, "--file", ppath)
        self.assertIn("PLAN APPLIED", out)
        self.assertIn(A1, out)
        self.assertIn("check digit", out)                                     # the invented beneficiary's ID is flagged, not refused
        run("run.py", "done", R, "plan")
        self.assertIn("not been shown", run("run.py", "approve", R, "--said", "yes", expect="refused"))
        self.assertIn("before Paul's yes", run("run.py", "fill", R, expect="refused"))
        out = run("run.py", "show", R)
        self.assertIn("Transaction folder rename", out)
        self.assertIn(F1, out)
        self.assertIn("Possible older draft", out)
        self.assertIn("•••", out)                               # ID and account numbers are masked
        self.assertNotIn(sample.ACCOUNT, out)
        self.assertNotIn(sample.PAT_ID, out)
        self.assertIn("Ready to fill and save 2 new applications for Pat Samplecase", out)
        run("run.py", "approve", R, "--said", "Yes, go ahead")
        run("run.py", "done", R, "confirm")
        # ---- fill
        out = run("run.py", "fill", R)
        self.assertEqual(out.count("✅"), 2)
        v1 = A.read_values(os.path.join(R, "out", A1))
        self.assertEqual(v1["Product"], "OM Optimal RA – Recurring - R 2,800.00 p.m.")
        self.assertEqual((v1["SignatureDate"], v1["IsReplacement"], v1["ReplacedPolicyNumbers"], v1["ForeignTaxNumber"], v1["OriginateFrom"], v1["MaritalContractType"]),
                         ("20/11/26", "No", "N/A", "N/A", "N/A", "N/A"))
        self.assertEqual(v1["Signature"], "")
        v2 = A.read_values(os.path.join(R, "out", A2))
        self.assertEqual((v2["Text Box 5_8"], v2["List Box 1"], v2["List Box 2"].strip(), v2["List Box 3_5"].strip(), v2["Text Box 5_5"], v2["Text Box 5_6"]),
                         ("20/11/26", "Brightrock", "Personal", "Yes", "Samplelife", "SL-123456"))
        self.assertEqual(v2["Text Box 5_7"], "")
        run("run.py", "done", R, "fill")
        # ---- save and rename: caught when wrong
        self.receipt(R, "chat.a1.sent", "yes")
        write(os.path.join(d, "x.txt"), "x\n")
        self.assertIn("save.a1.folder", run("run.py", "save", R, "--id", "a1", "--file", os.path.join(d, "x.txt"), expect=5))
        self.receipt(R, "save.a1.folder", "New Business\\Samplecase, Pat\\" + F1 + "\\Applications")
        size1 = os.path.getsize(os.path.join(R, "out", A1))
        write(os.path.join(d, "list_bad.txt"), "Notes.pdf   1,204\n")
        self.assertIn("does not show", run("run.py", "save", R, "--id", "a1", "--file", os.path.join(d, "list_bad.txt"), expect=5))
        write(os.path.join(d, "list1.txt"), "Notes.pdf   1,204\n%s   %s\n" % (A1, "{:,}".format(size1)))
        self.assertIn("is in the client's Applications folder (listing shows", run("run.py", "save", R, "--id", "a1", "--file", os.path.join(d, "list1.txt")))
        self.receipt(R, "rename.a1.done", "mv -n done")
        write(os.path.join(d, "ren_bad.txt"), "Samplecase, Pat - (OM RA - R2800)\n%s\n" % F1)
        self.assertIn("still listed", run("run.py", "rename", R, "--id", "a1", "--file", os.path.join(d, "ren_bad.txt"), expect=5))
        write(os.path.join(d, "ren_ok.txt"), "%s\nSamplecase, Pat\n" % F1)
        self.assertIn("the transaction folder is now", run("run.py", "rename", R, "--id", "a1", "--file", os.path.join(d, "ren_ok.txt")))
        self.assertIn("no rename is planned", run("run.py", "rename", R, "--id", "a2", "--file", os.path.join(d, "ren_ok.txt"), expect="refused"))
        self.receipt(R, "chat.a2.sent", "yes")
        self.receipt(R, "save.a2.folder", "New Business\\Samplecase, Pat\\Samplecase, Pat - (BR - Personal Covers - R 1,000.00 p.m.)\\Applications")
        size2 = os.path.getsize(os.path.join(R, "out", A2))
        write(os.path.join(d, "list2.txt"), "%s %d bytes\n" % (A2, size2))
        run("run.py", "save", R, "--id", "a2", "--file", os.path.join(d, "list2.txt"))
        run("run.py", "done", R, "save")
        out = run("run.py", "done", R, "final")
        self.assertIn("RESULT: PASS", out)
        self.assertFalse([l for l in out.splitlines() if l.startswith("❌")], out)
        self.assertIn("Only attested (not proven):", out)
        self.assertIn("HAND-BACK", out)
        self.assertIn("•••", out)
        self.assertNotIn(sample.ACCOUNT, out)
        self.assertEqual(run("verify.py", R).count("RESULT: PASS"), 1)
        # ---- a PDF edited by hand after the run is caught
        T = os.path.join(d, "run1_tampered")
        shutil.copytree(R, T)
        A.fill("om", {"AccountNumber": sample.NEW_ACCOUNT}, os.path.join(T, "out", A1), start_path=os.path.join(R, "out", A1))
        out = run("verify.py", T, expect=1)
        self.assertIn("RESULT: FAIL", out)
        self.run1_out = {A1: os.path.join(R, "out", A1), A2: os.path.join(R, "out", A2)}

    # ------------------------------------------------------------------ the correction
    def second_run(self, d):
        for sub in ("staged1", "staged2", "staged3"):
            os.makedirs(os.path.join(d, sub))
        live = os.path.join(d, "staged1", A1)                   # what Paul typed live: a new account number (staged copies keep their real names)
        A.fill("om", {"AccountNumber": sample.NEW_ACCOUNT}, live, start_path=self.run1_out[A1])
        other = os.path.join(d, "staged3", A1)                 # another current application that disagrees
        A.fill("om", {"AccountNumber": sample.ACCOUNT3}, other, start_path=self.run1_out[A1])
        gen = os.path.join(d, "staged2", A2)
        shutil.copyfile(self.run1_out[A2], gen)
        ff = os.path.join(d, "Fact Find Summary.pdf")
        R = os.path.join(d, "run2")
        run("run.py", "start", R, "--client", "Pat Samplecase", "--mode", "correct")
        run("run.py", "access", R, "--purpose", "folder", "--route", "device", "--result", "found", "--note", "current transaction folders, Applications listed")
        run("run.py", "access", R, "--purpose", "docs", "--route", "device", "--result", "found", "--note", "staged fresh copies")
        self.assertIn("neither of the two forms", run("run.py", "current", R, "--id", "x", "--file", ff, "--route", "device", expect=5))
        for cid, f in (("a1", live), ("a2", gen), ("a3", other)):
            self.assertIn("registered", run("run.py", "current", R, "--id", cid, "--file", f, "--route", "device"))
        run("run.py", "done", R, "locate")

        def plan(changes_a2, extra=None):
            pl = {"mode": "correct", "apps": [{"id": "a2", "current_id": "a2", "meeting_date": "20/11/2026", "changes": changes_a2}] + (extra or [])}
            path = os.path.join(d, "plan2.json")
            jwrite(path, pl)
            return path
        carry = {"from_app": {"id": "a1", "key": "AccountNumber"}}
        self.assertIn("not a one-to-one pair", run("run.py", "plan", R, "--file", plan({"debit_date": {"from_app": {"id": "a1", "key": "DateOfEntry"}}}), expect=5))
        self.assertIn("signature fields are never touched", run("run.py", "plan", R, "--file", plan({"client_signature": {"value": "x", "paul_said": "no"}}), expect=5))
        self.assertIn("product-specific", run("run.py", "plan", R, "--file", plan({}, [{"id": "a3", "current_id": "a3", "changes": {"DateOfEntry": {"from_app": {"id": "a1", "key": "DateOfEntry"}}}}]), expect=5))
        self.assertIn("STOP and ask Paul", run("run.py", "plan", R, "--file", plan({"account_number": carry}), expect=5))
        self.receipt(R, "stage.a2.mtime", "1762330000000")
        ok_changes = {"account_number": dict(carry, paul_said="Use the live application's number, she changed banks"), "cell": {"value": "082 555 0199", "paul_said": "She gave a new number at the meeting"}}
        out = run("run.py", "plan", R, "--file", plan(ok_changes))
        self.assertIn("PLAN APPLIED", out)
        run("run.py", "done", R, "plan")
        out = run("run.py", "show", R)
        self.assertIn("CORRECTION in place", out)
        self.assertIn("•••" + sample.NEW_ACCOUNT[-4:], out)
        self.assertNotIn(sample.NEW_ACCOUNT, out)
        self.assertIn("Ready to correct 1 application for Pat Samplecase in place", out)
        run("run.py", "approve", R, "--said", "Yes")
        run("run.py", "done", R, "confirm")
        out = run("run.py", "fill", R)
        self.assertIn("✅", out)
        before, after = A.read_values(gen), A.read_values(os.path.join(R, "out", A2))
        diff = sorted(k for k in after if after[k] != before[k])
        self.assertEqual(diff, ["Text Box 4_4", "Text Box 5_10"])         # ONLY the planned fields changed
        self.assertEqual(after["Text Box 5_10"], sample.NEW_ACCOUNT)
        run("run.py", "done", R, "fill")
        self.receipt(R, "chat.a2.sent", "yes")
        self.receipt(R, "save.a2.folder", "New Business\\Samplecase, Pat\\Samplecase, Pat - (BR - Personal Covers - R 1,000.00 p.m.)\\Applications")
        self.receipt(R, "commit.a2.expected_mtime", "1762339999999")
        write(os.path.join(d, "list3.txt"), "%s\n" % A2)
        self.assertIn("expectedMtimeMs", run("run.py", "save", R, "--id", "a2", "--file", os.path.join(d, "list3.txt"), expect=5))
        self.receipt(R, "commit.a2.expected_mtime", "1762330000000")
        run("run.py", "save", R, "--id", "a2", "--file", os.path.join(d, "list3.txt"))
        run("run.py", "done", R, "save")
        out = run("run.py", "done", R, "final")
        self.assertIn("RESULT: PASS", out)
        self.assertIn("Only the planned fields changed", out)
        self.assertIn("corrected in place (one copy); 2 field(s) changed", out)

    # ------------------------------------------------------------------ a form that has changed is caught
    def form_drift(self, d):
        from pypdf import PdfReader, PdfWriter
        from pypdf.generic import ArrayObject, NameObject, TextStringObject
        w_ = PdfWriter()
        w_.append(PdfReader(A.template_path("om")))
        for f in w_._root_object["/AcroForm"]["/Fields"]:
            o = f.get_object()
            if o.get("/T") == "Title":
                o[NameObject("/Opt")] = ArrayObject([TextStringObject("Mr"), TextStringObject("Lord")])
        p = os.path.join(d, "changed_om.pdf")
        with open(p, "wb") as fh:
            w_.write(fh)
        probs = A.drift_problems("om", p)
        self.assertTrue(any("dropdown options of Title changed" in x for x in probs), probs)
        self.assertEqual(A.drift_problems("om"), [])
        self.assertEqual(A.drift_problems("general"), [])


if __name__ == "__main__":
    unittest.main()
