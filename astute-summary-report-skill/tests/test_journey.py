"""The ONE test of the astute-summary-report-skill (Operation Skill Restructure: one end-to-end test on invented data).

It plays whole jobs through the program exactly as a chat would, on an INVENTED Astute-style report (tests/sample.py: Pat Samplecase, invented
insurers, invented numbers) that the test draws itself. Nothing is saved or sent anywhere: the folder listing is typed in as receipts, as a chat
would copy it. It proves:
  1. the driver refuses to skip a step; a file that is not a PDF, a route used out of order and a page acknowledged out of order are refused;
  2. bad data is refused (a missing pattern or label, an unknown field, a policy under a provider that returned no data, the wrong client) and an
     entry that is not in the report's text (a figure, a policy number, a date) is caught;
  3. the good job ends in a short audit of green ticks; the PDF has the five headings in order, only the paid-up policy in Section 3, the totals added
     up by the program, the flags in their fixed order, landscape A4 and the footer;
  4. a correction re-opens the later steps; a content file edited by hand is caught; an existing file is never overwritten (it is numbered);
  5. a scanned report (no readable text) is said to be attested; totals that differ from the report's own total and an unrecognised status are flagged.
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
sys.path.insert(0, SCRIPTS)
sys.path.insert(0, HERE)
import model  # noqa: E402
import sample  # noqa: E402

PRODUCTS = {"Alpha Life Plan": "Whole-of-life risk plan with level premiums.", "Alpha Growth Fund": "Flexible investment with a choice of funds.",
            "Alpha Old Endowment": "Closed endowment policy."}


def run(script, *args, expect=0):
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS, script)] + list(args), capture_output=True, text=True, encoding="utf-8")
    if expect == "refused":
        assert r.returncode != 0, "%s %s should have been refused\n%s" % (script, args, r.stdout[-1200:])
    else:
        assert r.returncode == expect, "%s %s -> exit %d (wanted %d)\n%s\n%s" % (script, args, r.returncode, expect, r.stdout[-1800:], r.stderr[-800:])
    return r.stdout + r.stderr


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)


def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


class Journey(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="wr-as-test-")
        self.pdf = os.path.join(self.d, "report.pdf")
        sample.make_pdf(self.pdf)

    def start(self, name, client="Pat Samplecase", pdf=None):
        R = os.path.join(self.d, name)
        out = run("run.py", "start", R, "--client", client)
        self.assertIn("Using astute-summary-report-skill, last updated", out)
        run("run.py", "access", R, "--purpose", "locate", "--route", "device", "--result", "found", "--note", "test")
        run("run.py", "source", R, "--file", pdf or self.pdf, "--route", "device")
        run("run.py", "done", R, "locate")
        return R

    def read_all(self, R, pages=4):
        for n in range(1, pages + 1):
            run("run.py", "read", R)
            run("run.py", "read", R, "--ack", str(n), "--note", "page %d read" % n)
        run("run.py", "done", R, "read")

    def datafile(self, data, name="data.json"):
        path = os.path.join(self.d, name)
        write_json(path, data)
        return path

    def products_and_flags(self, R, extra_flag=True):
        for n, desc in PRODUCTS.items():
            run("run.py", "product", R, "--name", n, "--source", "https://example.invalid/" + n.replace(" ", "-"), "--desc", desc)
        run("run.py", "product", R, "--name", "Beta Cover", "--unconfirmed")
        run("run.py", "done", R, "products")
        if extra_flag:
            run("run.py", "flag", R, "--kind", "status_contradiction", "--text", "the package is Active but its underlying policy BC-77 is Lapsed", "--policy", "BC-77")
        run("run.py", "done", R, "flags")

    def build_and_save(self, R, existing=""):
        run("run.py", "build", R)
        run("run.py", "done", R, "build")
        out = run("run.py", "name", R, "--existing", existing)
        name = [ln for ln in out.splitlines() if ln.startswith("SAVE THIS FILE:")][0].split("SAVE THIS FILE: ")[1]
        run("run.py", "access", R, "--purpose", "save", "--route", "device", "--result", "found", "--note", "test")
        run("run.py", "receipt", R, "save.folder", "C:\\Users\\x\\Company - Paul\\Samplecase, Pat\\5. Astute")
        run("run.py", "receipt", R, "save.listed_bytes", str(os.path.getsize(name)))
        run("run.py", "done", R, "save")
        return name

    def full(self, name):
        R = self.start(name)
        self.read_all(R)
        run("run.py", "data", R, "--file", self.datafile(sample.data()))
        run("run.py", "done", R, "data")
        self.products_and_flags(R)
        return R

    def test_one_journey_on_invented_data(self):
        # 1. no step is skipped; a non-PDF, an out-of-order route and an out-of-order page are refused
        R0 = os.path.join(self.d, "run0")
        run("run.py", "start", R0, "--client", "Pat Samplecase")
        run("run.py", "done", R0, "data", expect=3)
        run("run.py", "build", R0, expect="refused")
        notpdf = os.path.join(self.d, "notes.pdf")
        with open(notpdf, "w") as f:
            f.write("this is not a pdf")
        run("run.py", "access", R0, "--purpose", "locate", "--route", "zapier", "--result", "found", "--note", "test")
        run("run.py", "source", R0, "--file", self.pdf, "--route", "zapier", expect="refused")                 # the computer and Microsoft 365 were not tried first
        run("run.py", "access", R0, "--purpose", "locate", "--route", "device", "--result", "found", "--note", "test")
        run("run.py", "source", R0, "--file", self.pdf, "--route", "device", expect="refused")                  # still: device found AFTER zapier in the log is out of order
        R1 = os.path.join(self.d, "run1")
        run("run.py", "start", R1, "--client", "Pat Samplecase")
        run("run.py", "access", R1, "--purpose", "locate", "--route", "device", "--result", "found", "--note", "test")
        self.assertIn("STOP", run("run.py", "source", R1, "--file", notpdf, "--route", "device", expect=5))
        run("run.py", "source", R1, "--file", self.pdf, "--route", "device", "--folder-count", "2", expect="refused")   # two reports: say which one and why
        run("run.py", "source", R1, "--file", self.pdf, "--route", "device", "--folder-count", "2", "--chosen", "most recent by report date")
        run("run.py", "done", R1, "locate")
        run("run.py", "read", R1, "--ack", "2", "--note", "x page", expect="refused")                           # page 1 comes first
        run("run.py", "read", R1, "--ack", "1", "--note", "", expect="refused")                                 # a note is needed
        run("run.py", "done", R1, "read", expect=3)
        self.read_all(R1)
        # 2. bad data is refused; entries not in the report's text are caught
        base = sample.data()
        bad = []
        d1 = sample.data(); del d1["policies"][0]["premium_pattern"]; bad.append(d1)
        d2 = sample.data(); d2["policies"][0]["benefits"][0]["type"] = "maybe"; bad.append(d2)
        d3 = sample.data(); d3["policies"][0]["colour"] = "red"; bad.append(d3)
        d4 = sample.data(); d4["policies"][0]["provider"] = "Insurer B Assurance"; bad.append(d4)
        d5 = sample.data(); d5["header"]["client_name"] = "Someone Else"; bad.append(d5)
        d6 = sample.data(); d6["policies"][1]["values"].pop("fund_value"); bad.append(d6)
        for i, b in enumerate(bad):
            self.assertIn("REFUSED", run("run.py", "data", R1, "--file", self.datafile(b, "bad%d.json" % i), expect=5))
        e1 = sample.data(); e1["policies"][0]["benefits"][0]["cover_amount"] = "R 999 999.00"
        self.assertIn("not in the report's text", run("run.py", "data", R1, "--file", self.datafile(e1, "e1.json"), expect=3))
        run("run.py", "done", R1, "data", expect=3)                                                              # the not-found entry is saved but the step is not done
        e2 = sample.data(); e2["policies"][1]["policy_number"] = "AL-1099"
        self.assertIn("AL-1099", run("run.py", "data", R1, "--file", self.datafile(e2, "e2.json"), expect=3))
        e3 = sample.data(); e3["policies"][0]["start_date"] = "02/03/2019"
        self.assertIn("02/03/2019", run("run.py", "data", R1, "--file", self.datafile(e3, "e3.json"), expect=3))
        # 3. the good job
        run("run.py", "data", R1, "--file", self.datafile(base))
        run("run.py", "done", R1, "data")
        run("run.py", "done", R1, "products", expect=3)                                                          # no product has a source yet
        run("run.py", "product", R1, "--name", "Alpha Life Plan", "--source", "not a web address", "--desc", "x", expect="refused")
        run("run.py", "product", R1, "--name", "Unknown Product", "--unconfirmed", expect="refused")
        self.products_and_flags(R1)
        pdfpath = self.build_and_save(R1)
        final = run("run.py", "done", R1, "final")
        self.assertIn("RESULT: PASS", final)
        audit = final[final.index("AUDIT   "):].strip().splitlines()
        marks = [ln for ln in audit if ln.startswith("\u2705") or ln.startswith("\u274c")]
        self.assertLessEqual(len(audit), 20, "the audit must stay short")
        self.assertTrue(all(ln.startswith("\u2705") for ln in marks), "every check line must be a green tick:\n" + "\n".join(marks))
        self.assertTrue(any(ln.startswith("Only attested") for ln in audit))
        flags = final[final.index("FLAGS TO VERIFY"):final.index("AUDIT   ")].strip().splitlines()[1:]
        self.assertTrue(flags[0].startswith("1. Status contradiction"), flags)                                   # the most important flag first
        self.assertTrue(any("Insurer B Assurance" in f and "not proof of no cover" in f for f in flags))
        import pdfplumber
        with pdfplumber.open(pdfpath) as pdf:
            text = "\n".join((p.extract_text() or "") for p in pdf.pages)
        order = [text.find(h) for h in ["Section 1: Active Policies", "Section 2: Group Risk", "Section 3: Paid-Up Policies", "Additional Notes: Inactive", "General Verification Notes"]]
        self.assertEqual(order, sorted(order))
        self.assertTrue(all(x >= 0 for x in order))
        s3 = text[order[2]:order[3]]
        self.assertIn("AL-0900", s3)                                                                              # only the paid-up policy is in Section 3
        self.assertNotIn("BC-77", s3)
        self.assertIn("BC-77", text[order[3]:order[4]])                                                           # the lapsed policy is in Additional Notes
        self.assertIn("monthly premiums R 1 350.00", text)                                                        # 350.00 + 1 000.00, added up by the program
        self.assertIn("Cession status is not held in Astute's data", text)
        self.assertNotIn("E+", text)                                                                              # no scientific notation in percentages
        self.assertIn("(100%)", text)
        # 4. a correction re-opens the later steps; a content file edited by hand is caught; an existing file is never overwritten
        fixed = sample.data(); fixed["policies"][0]["benefits"][1]["cover_amount"] = "R 1 000 000.00"
        self.assertIn("RE-OPENED", run("run.py", "data", R1, "--file", self.datafile(fixed, "fixed.json")))
        self.assertIn("Now: products", run("run.py", "status", R1))
        run("run.py", "done", R1, "products")
        run("run.py", "done", R1, "flags")
        pdf2 = self.build_and_save(R1, existing="Astute Report Summary - 05.11.26 - (Pat Samplecase).pdf")
        self.assertTrue(pdf2.endswith("(Pat Samplecase) (2).pdf"), pdf2)
        self.assertIn("RESULT: PASS", run("run.py", "done", R1, "final"))
        content = read_json(os.path.join(R1, "content.json"))
        content["s1_risk"][0]["policies"][0]["benefits"][0] = "Life cover: R 9 999 999.00"
        write_json(os.path.join(R1, "content.json"), content)
        self.assertIn("RESULT: FAIL", run("verify.py", R1, expect=1))
        # 5. a scanned report is attested; totals that differ and an unrecognised status are flagged
        from reportlab.pdfgen import canvas
        blank = os.path.join(self.d, "scanned.pdf")
        c = canvas.Canvas(blank)
        for _ in range(2):
            c.showPage()
        c.save()
        R2 = self.start("run2", pdf=blank)
        self.assertIn("NO READABLE TEXT", run("run.py", "read", R2))
        run("run.py", "read", R2, "--ack", "1", "--note", "viewed the image")
        run("run.py", "read", R2, "--ack", "2", "--note", "viewed the image")
        run("run.py", "done", R2, "read")
        self.assertIn("nothing could be checked", run("run.py", "data", R2, "--file", self.datafile(base, "scanned.json")))
        run("run.py", "done", R2, "data")
        self.assertEqual(model.section_of({"status": "Paid Up"}), "paid_up")
        self.assertEqual(model.section_of({"status": "Inactive"}), "inactive")
        self.assertEqual(model.section_of({"status": "Premium paying"}), "active")
        self.assertEqual(model.section_of({"status": "Pending"}), "unrecognised")
        mism = sample.data(); mism["report_totals"] = {"monthly_premiums": "R 350.00"}
        kinds = [f["kind"] for f in model.computed_flags(mism, {})]
        self.assertIn("total_mismatch", kinds)
        self.assertIn("unconfirmed", [f["kind"] for f in model.computed_flags(base, {"beta cover": {"state": "unconfirmed"}})])
        odd = sample.data(); odd["policies"][3]["status"] = "Pending"
        self.assertTrue(any(f["kind"] == "other" and "not recognised" in f["text"] for f in model.computed_flags(odd, {})))


if __name__ == "__main__":
    unittest.main()
