"""The ONE test of the wr-sroa-builder (Operation Skill Restructure: one end-to-end test on invented data).

It plays whole jobs through the program exactly as a chat would, on invented documents (Pat Samplecase, BrightRock-style and flat-list quotes, an
invented acceptance email), with today fixed by WR_TODAY. Nothing is saved or sent anywhere: the folder listing is typed in as receipts. It proves:
  1. the driver refuses to skip a step, and the routes must be tried in order;
  2. only the pages of THIS policy are taken from a combined Owner's Manual (the other policy's figures never reach the chat and cannot be used);
  3. bad answers are refused (nothing saved): a figure from the other policy or not in the quote, an ID or a name not in the documents, a CP number or a
     date not in the documents, a premium line without the R20 label, a missing ACI/ABI, headings out of order, an accepted quote that was not compiled,
     a quote that was not compiled but has figures, a one-sided item nobody confirmed, a conflict, a future date, a wrong policy;
  4. nothing is built before Paul's yes, a changed answer voids it, and the data the program builds EQUALS the old skill's JSON form, line for line
     ("No change" worked out by the program, the premium label, the accepted quote marked, the CP lines, N/A for Portfolio Changes);
  5. the finished PDF is read back and every check is a green tick; a hand-edited PDF is caught; an existing file is never overwritten without a yes;
  6. a flat-layout case (another insurer, the FNA declined, items entered out of order) is put in the fixed order with "No change" computed.
"""
import json
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
sys.path.insert(0, HERE)
import sample  # noqa: E402

PREM = sample.PREM
ARROW = "\u2192"
DASH = "\u2014"


def run(script, *args, expect=0, env=None):
    e = dict(os.environ, WR_TODAY="05/11/2026")
    e.update(env or {})
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS, script)] + list(args), capture_output=True, text=True, encoding="utf-8", env=e)
    if expect == "refused":
        assert r.returncode != 0, "%s %s should have been refused\n%s" % (script, args, r.stdout[-1200:])
    else:
        assert r.returncode == expect, "%s %s -> exit %d (wanted %d)\n%s\n%s" % (script, args, r.returncode, expect, r.stdout[-1800:], r.stderr[-800:])
    return r.stdout + r.stderr


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)


class Journey(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="wr-sroa-test-")
        self.docs = sample.make_docs(self.d)

    def load(self, path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def afile(self, data, name="answers.json"):
        path = os.path.join(self.d, name)
        write_json(path, data)
        return path

    def refused(self, R, data, fragment):
        out = run("run.py", "answers", R, "--file", self.afile(data), expect="refused")
        self.assertIn(fragment, out)
        self.assertFalse(os.path.exists(os.path.join(R, "answers.json")), "a refused answers file must not be saved")

    def read_all(self, R):
        seen = []
        for _ in range(20):
            out = run("run.py", "read", R)
            seen.append(out)
            m = re.search(r"--ack ([a-z_]+:\d+)", out)
            if not m:
                break
            run("run.py", "read", R, "--ack", m.group(1), "--note", "read " + m.group(1))
        run("run.py", "done", R, "read")
        return "\n".join(seen)

    def register(self, R, files, policy, ps_key="current_ps"):
        run("run.py", "access", R, "--purpose", "locate", "--route", "device", "--result", "found", "--note", "test")
        run("run.py", "doc", R, "--role", "current_ps", "--file", self.docs[ps_key], "--route", "device", "--policy", policy)
        for role, key in files.items():
            run("run.py", "doc", R, "--role", role, "--file", self.docs[key], "--route", "device")

    def audit_lines(self, text):
        return [ln for ln in text.splitlines() if ln.startswith(("\u2705", "\u274c"))]

    def test_whole_journey(self):
        self.grouped_case()
        self.flat_case()

    # ------------------------------------------------------------------ BrightRock, grouped headings
    def grouped_case(self):
        A = sample.answers_grouped()
        R0 = os.path.join(self.d, "order-test")
        run("run.py", "start", R0, "--client", "Pat Samplecase", expect="refused")           # no --policy
        run("run.py", "start", R0, "--client", "Pat", "--policy", sample.POLICY, expect="refused")   # surname missing
        out = run("run.py", "start", R0, "--client", "Pat Samplecase", "--policy", sample.POLICY)
        self.assertIn("Using wr-sroa-builder, last updated", out)
        run("run.py", "done", R0, "answers", expect="refused")                              # no skipping
        run("run.py", "doc", R0, "--role", "current_ps", "--file", self.docs["current_ps"], "--route", "device", "--policy", sample.POLICY, expect="refused")  # no access try logged
        run("run.py", "access", R0, "--purpose", "locate", "--route", "m365", "--result", "found")
        out = run("run.py", "doc", R0, "--role", "current_ps", "--file", self.docs["current_ps"], "--route", "m365", "--policy", sample.POLICY, expect="refused")
        self.assertIn("in order", out)

        R = os.path.join(self.d, "run1")
        run("run.py", "start", R, "--client", "Pat Samplecase", "--policy", sample.POLICY)
        run("run.py", "access", R, "--purpose", "locate", "--route", "device", "--result", "found", "--note", "test")
        run("run.py", "doc", R, "--role", "current_ps", "--file", self.docs["current_ps"], "--route", "device", expect="refused")                 # no --policy
        run("run.py", "doc", R, "--role", "current_ps", "--file", self.docs["current_ps"], "--route", "device", "--policy", sample.OTHER, expect="refused")  # another policy
        out = run("run.py", "doc", R, "--role", "current_ps", "--file", self.docs["current_ps"], "--route", "device", "--policy", sample.POLICY)
        self.assertIn("page 2 of 3 taken", out)
        docs = self.load(os.path.join(R, "docs.json"))
        self.assertEqual(docs["docs"]["current_ps"]["served"], [2])
        for role, key in (("fna_quote", "fna_quote"), ("alternative_quote", "alternative_quote"), ("acceptance_email", "acceptance_email")):
            run("run.py", "doc", R, "--role", role, "--file", self.docs[key], "--route", "device")
        out = run("run.py", "done", R, "locate", expect=3)                                 # the Fact Find Summary is still missing
        self.assertIn("fact_find_summary", out)
        run("run.py", "doc", R, "--role", "fact_find_summary", "--file", self.docs["fact_find_summary"], "--route", "device")
        run("run.py", "done", R, "locate")
        served = self.read_all(R)
        self.assertNotIn(sample.OTHER, served, "the other policy's page must never be served")
        self.assertNotIn("750 000", served)
        self.assertEqual(len(re.findall(r"- PAGE \d+ of \d+ -", served)), 5)

        # ---- bad answers are refused, nothing saved
        self.refused(R, sample.bad(A, **{"changes.groups.0.items.0.old": "R750,000"}), "not in the Current Policy Schedule")
        self.refused(R, sample.bad(A, **{"changes.groups.0.items.0.new": "R999,000"}), "not in the quote")
        self.refused(R, sample.bad(A, **{"blocks.fna.groups.0.items.0.value": "R1,000,000"}), "not in the quote")
        self.refused(R, sample.bad(A, owner_id="2222222222222"), "ID number is not in")
        self.refused(R, sample.bad(A, owner_id="12345"), "13 digits")
        self.refused(R, sample.bad(A, owner="Patricia Beth Samplecase"), "owner's name")
        self.refused(R, sample.bad(A, **{"changes.groups.4.items.0.label": "Premium"}), "Premium (incl. R20 policy fee)")
        self.refused(R, sample.bad(A, **{"changes.groups.4.items": A["changes"]["groups"][4]["items"][:1]}), "ACI")
        swapped = sample.bad(A)
        swapped["changes"]["groups"][0], swapped["changes"]["groups"][1] = swapped["changes"]["groups"][1], swapped["changes"]["groups"][0]
        self.refused(R, swapped, "fixed order")
        self.refused(R, sample.bad(A, accepted="shortfall"), "compiled")
        self.refused(R, sample.bad(A, **{"blocks.shortfall": {"groups": A["blocks"]["fna"]["groups"]}}), "not compiled")
        self.refused(R, sample.bad(A, **{"cp_numbers.alternative": "CP999999"}), "CP number")
        self.refused(R, sample.bad(A, sroa_date="10/11/2026"), "future")
        self.refused(R, sample.bad(A, sroa_date="04/11/2026"), "SROA date")
        self.refused(R, sample.bad(A, investment_linked=sample.DELETE), "investment_linked")
        self.refused(R, sample.bad(A, portfolio_reason="Moved the fund because the client's risk profile is now cautious."), "N/A")
        self.refused(R, sample.bad(A, conflicts=[{"what": "premium", "a": "x", "b": "y"}]), "conflict")
        self.refused(R, sample.bad(A, policy_number="TEST-000000"), "policy")
        self.refused(R, sample.bad(A, insurer="Otherinsurer"), "BrightRock")
        one_sided = sample.bad(A)
        one_sided["changes"]["groups"][0]["items"].append({"label": "Debt cover (new)", "old": "", "new": "R50,000", "unit": "amount"})
        self.refused(R, one_sided, "confirm with Paul")
        self.refused(R, sample.bad(A, reason="Short."), "reason")
        self.refused(R, sample.bad(A, **{"sources.cp": ""}), "sources.cp")
        run("run.py", "done", R, "answers", expect=3)

        # ---- good answers; Paul's yes
        run("run.py", "answers", R, "--file", self.afile(A))
        run("run.py", "done", R, "answers")
        run("run.py", "approve", R, "--said", "yes", expect="refused")                    # not shown yet
        run("run.py", "build", R, expect="refused")                                         # no yes yet
        out = run("run.py", "show", R)
        for frag in ("No change (5%)", "Block 4", "Alternative Quote (accepted)", "CP333444", "03/11/2026", "Are these answers right"):
            self.assertIn(frag, out)
        changed = sample.bad(A, reason="Pat asked for a lower premium because her income dropped a lot; the Alternative Quote keeps her cover in line with what she can afford.")
        run("run.py", "approve", R, "--said", "Yes, those are right")
        run("run.py", "answers", R, "--file", self.afile(changed))                         # a changed answer voids the yes
        run("run.py", "build", R, expect="refused")
        run("run.py", "show", R)
        run("run.py", "approve", R, "--said", "Yes, those are right")
        run("run.py", "done", R, "confirm")
        out = run("run.py", "build", R)
        self.assertNotIn("WARNED", out)
        run("run.py", "done", R, "build")

        # ---- the data equals the old skill's JSON form
        data = self.load(os.path.join(R, "sroa_data.json"))
        want = {
            "insurer": "BrightRock", "policy_number": sample.POLICY, "owner": sample.OWNER, "owner_id": sample.ID,
            "quote_blocks": [
                {"block_label": "Block 1", "title": "Servicing FNA Quote", "compiled": True, "cp_number": "CP111222", "groups": [
                    {"heading": "Life Cover", "bullets": ["Cover caused by death: R1,500,000"]},
                    {"heading": "Lump Sum Disability Cover", "bullets": ["Permanent cover: R700,000"]},
                    {"heading": "Income Protector / Sickness Benefit", "bullets": ["Recoverable income: R30,000 p.m."]},
                    {"heading": "Additional Expense Needs / Dread Disease", "bullets": ["Additional expense needs: R350,000"]},
                    {"heading": "Policy Details", "bullets": ["%s: R1,650.00 p.m." % PREM, "ACI (Automatic Cover Increase): 5%", "ABI (Automatic Benefit Increase): 5%"]}]},
                {"block_label": "Block 2", "title": "Shortfall Quote", "compiled": False},
                {"block_label": "Block 3", "title": "Alternative Quote (Accepted)", "compiled": True, "cp_number": "CP333444", "groups": [
                    {"heading": "Life Cover", "bullets": ["Cover caused by death: R1,000,000"]},
                    {"heading": "Lump Sum Disability Cover", "bullets": ["Permanent cover: R400,000"]},
                    {"heading": "Income Protector / Sickness Benefit", "bullets": ["Recoverable income: R20,000 p.m."]},
                    {"heading": "Additional Expense Needs / Dread Disease", "bullets": ["Additional expense needs: R250,000"]},
                    {"heading": "Policy Details", "bullets": ["%s: R1,172.80 p.m." % PREM, "ACI (Automatic Cover Increase): 5%", "ABI (Automatic Benefit Increase): 5%"]}]}],
            "accepted_quote_cp_number": "CP333444",
            "grouped_changes": [
                {"heading": "Life Cover", "bullets": ["Cover caused by death: R1,200,000 %s R1,000,000" % ARROW]},
                {"heading": "Lump Sum Disability Cover", "bullets": ["Permanent cover: R600,000 %s R400,000" % ARROW]},
                {"heading": "Income Protector / Sickness Benefit", "bullets": ["Recoverable income: R25,000 p.m. %s R20,000 p.m." % ARROW]},
                {"heading": "Additional Expense Needs / Dread Disease", "bullets": ["Additional expense needs: R300,000 %s R250,000" % ARROW]},
                {"heading": "Policy Details", "bullets": ["%s: R1,300.00 p.m. %s R1,172.80 p.m." % (PREM, ARROW), "ACI (Automatic Cover Increase): No change (5%)",
                                                         "ABI (Automatic Benefit Increase): No change (5%)"]}],
            "advice_narrative": changed["reason"], "portfolio_changes_narrative": "N/A", "client_signature_name": sample.OWNER}
        self.assertEqual(data, want)

        # ---- the PDF, read back
        out = run("run.py", "check", R)
        self.assertNotIn("\u274c", out)
        self.assertGreaterEqual(len(self.audit_lines(out)), 3)
        self.assertTrue(os.listdir(os.path.join(R, "out", "pages")), "page images were not made")
        name = "SROA - BrightRock_%s - 03.11.26 - (Pat_Samplecase).pdf" % sample.POLICY
        pdf = os.path.join(R, "out", name)
        self.assertTrue(os.path.exists(pdf))
        import docread
        text = docread.full_text(docread.read_pdf(pdf))
        for frag in ("ID Number : " + sample.ID, "Block 2 %s Shortfall Quote" % DASH, "Not compiled for this client.", "Block 3 %s Alternative Quote (Accepted)" % DASH, "CP Number: CP333444",
                     "Portfolio Changes", "N/A", "Code: FSP45946", "Name : Paul Kafentzis", "ACI (Automatic Cover Increase): No change (5%)"):
            self.assertIn(frag, text.replace("\n", " ") if " " in frag and "\n" not in frag else text)
        self.assertNotIn("Signed at", text)
        run("run.py", "done", R, "check")

        # ---- save: never overwrite without a yes
        run("run.py", "name", R, "--existing", "x.pdf;" + name, expect=5)
        run("run.py", "name", R, "--existing", "x.pdf;" + name, "--overwrite-yes", "Yes, replace it")
        run("run.py", "access", R, "--purpose", "save", "--route", "device", "--result", "found")
        size = os.path.getsize(pdf)
        run("run.py", "receipt", R, "save.folder", r"C:\Clients\Samplecase, Pat (CL)\Risk - TEST-100200\Servicing")
        run("run.py", "receipt", R, "save.listed_bytes", str(size + 1))
        run("run.py", "done", R, "save", expect=3)                                          # the listed size does not match
        run("run.py", "name", R, "--existing", "x.pdf")
        run("run.py", "receipt", R, "save.listed_bytes", str(size))
        run("run.py", "done", R, "save")
        out = run("run.py", "done", R, "final")
        self.assertIn("RESULT: PASS", out)
        self.assertFalse([ln for ln in out.splitlines() if ln.startswith("\u274c")])
        self.assertTrue(os.path.exists(os.path.join(R, "out_record", "audit-full.txt")))
        out = run("verify.py", R)
        self.assertIn("RESULT: PASS", out)
        with open(pdf, "ab") as f:                                                          # a hand-edited PDF is caught
            f.write(b"\n% edited by hand\n")
        out = run("verify.py", R, expect=1)
        self.assertIn("\u274c", out)
        self.assertIn("RESULT: FAIL", out)

    # ------------------------------------------------------------------ another insurer, flat list
    def flat_case(self):
        A = sample.answers_flat()
        R = os.path.join(self.d, "run2")
        run("run.py", "start", R, "--client", "Pat Samplecase", "--policy", sample.FLAT_POLICY)
        self.register(R, {"shortfall_quote": "flat_shortfall", "alternative_quote": "flat_alternative", "acceptance_email": "flat_email", "fact_find_summary": "fact_find_summary"},
                      sample.FLAT_POLICY, ps_key="flat_ps")
        run("run.py", "done", R, "locate")
        self.read_all(R)
        self.refused(R, sample.bad(A, fna_declined=sample.DELETE), "fna_declined")
        self.refused(R, sample.bad(A, **{"changes.items.0.label": "Waiting Period"}), "fixed list")
        self.refused(R, sample.bad(A, **{"changes.items.4.new": "R899.00"}), "not in the")
        run("run.py", "answers", R, "--file", self.afile(A))
        run("run.py", "done", R, "answers")
        run("run.py", "show", R)
        run("run.py", "approve", R, "--said", "Yes")
        run("run.py", "done", R, "confirm")
        run("run.py", "build", R)
        run("run.py", "done", R, "build")
        data = self.load(os.path.join(R, "sroa_data.json"))
        self.assertEqual([b["title"] for b in data["quote_blocks"]], ["Servicing FNA Quote", "Shortfall Quote", "Alternative Quote (Accepted)"])
        self.assertEqual(data["quote_blocks"][0]["not_compiled_note"], "Not compiled %s declined by the client." % DASH)
        self.assertEqual(data["accepted_quote_cp_number"], "CP555222")
        import build_sroa as bs
        lines = bs.build_requested_changes_text(data["servicing_changes"]).split("\n")
        self.assertEqual(lines, [
            "Life Cover: R500,000 %s R450,000" % ARROW, "Disability Cover: No change (R400,000)", "Dread Disease: No change (R200,000)", "Income Protection: No change (R15,000 p.m.)",
            "%s: R900.00 p.m. %s R800.00 p.m." % (PREM, ARROW), "ACI (Automatic Cover Increase): No change (6%)", "ABI (Automatic Benefit Increase): No change (6%)"])
        self.assertNotIn("Retrenchment", "\n".join(lines))
        out = run("run.py", "check", R)
        self.assertNotIn("\u274c", out)
        run("run.py", "done", R, "check")
        name = "SROA - Sampleinsurer_%s - 02.11.26 - (Pat_Samplecase).pdf" % sample.FLAT_POLICY
        run("run.py", "name", R, "--existing", "")
        size = os.path.getsize(os.path.join(R, "out", name))
        run("run.py", "access", R, "--purpose", "save", "--route", "device", "--result", "found")
        run("run.py", "receipt", R, "save.folder", r"C:\Clients\Samplecase, Pat (CL)\Risk - TEST-555666\Servicing")
        run("run.py", "receipt", R, "save.listed_bytes", str(size))
        run("run.py", "done", R, "save")
        out = run("run.py", "done", R, "final")
        self.assertIn("RESULT: PASS", out)


if __name__ == "__main__":
    unittest.main()
