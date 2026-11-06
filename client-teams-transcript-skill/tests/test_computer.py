"""Tests for the computer connection (Paul, 06/11/2026): the chat connects to Paul's computer once, every client file is a whole copy proved identical to the
original by the computer's own fingerprint, and the finished PDF is saved on the computer and fingerprinted there.

Invented people and figures only. The computer's own fingerprint is built here the way `sha256sum` and `stat -c %s` print it.
"""
import hashlib
import json
import os
import subprocess
import sys

from test_driver import CLIENT, DriverBase, drv
from test_gate import FIXTURE, SCRIPTS, sh, slurp, spit


def sha_of(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def fingerprint(path, shown_name=None):
    """What device_bash prints on the computer for this file: sha256sum, then stat -c %s."""
    sha = sha_of(path)
    return "%s  /home/paul/mnt/liferisk.co.za/Company - Paul/New Business/Testcase, Sam/2. Fact Find/%s\n%d\n" % (sha, shown_name or os.path.basename(path), os.path.getsize(path))


class Computer(DriverBase):
    def bridge(self):
        """Connect the way a cloud chat does: through the device tools (the program is told what they showed)."""
        ENV_KEEP = os.environ.get("WR_COMPUTER_ROOT")
        r = drv("computer", self.run_dir, "--device", "Paul-Laptop", "--folder", "C:\\Users\\Paul\\liferisk.co.za",
                "--listing", "Teams meeting transcript - 05.10.26 - (Sam Testcase).docx; Fact Find - Testcase.pdf")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("COMPUTER CONNECTED through the device tools", r.stdout)
        return ENV_KEEP

    def test_a_refused_connection_prints_the_one_line_stop_and_blocks_the_run(self):
        self.start()
        r = drv("computer", self.run_dir, "--none", "device_request_folder_access was refused")
        self.assertEqual(r.returncode, 6)
        self.assertIn("STOP. I could not connect this chat to your computer", r.stdout)
        self.assertIn("liferisk.co.za", r.stdout)
        copy, orig = self.pair("Teams meeting transcript - 05.10.26 - (Sam Testcase).txt", src=FIXTURE)
        # a microsoft 365 copy of the transcript is allowed (it is text; tx.py prep proves it complete), but the step still needs the connection
        self.ok("access", self.run_dir, "--need", "transcript", "--route", "m365", "--tool", "read_resource", "--result", "ok")
        r = drv("done", self.run_dir, "locate")
        self.assertEqual(r.returncode, 1)
        self.assertIn("the computer is not connected", r.stdout)

    def test_the_connection_needs_the_device_name_the_client_root_and_a_real_listing(self):
        self.start()
        self.assertEqual(drv("computer", self.run_dir, "--device", "Paul-Laptop").returncode, 1)
        r = drv("computer", self.run_dir, "--device", "Paul-Laptop", "--folder", "C:\\Users\\Paul\\Documents", "--listing", "some file names that are long enough")
        self.assertIn("must be the client files' root, liferisk.co.za", r.stderr)
        r = drv("computer", self.run_dir, "--device", "Paul-Laptop", "--folder", "C:\\Users\\Paul\\liferisk.co.za", "--listing", "ok")
        self.assertIn("not a summary", r.stderr)
        self.assertEqual(drv("computer", self.run_dir, "--none", "no").returncode, 1)          # a real reason is needed

    def test_a_file_from_the_computer_needs_its_proof(self):
        self.start()
        self.bridge()
        copy = os.path.join(self.tmp, "staged", "Teams meeting transcript - 05.10.26 - (Sam Testcase).txt")
        spit(copy, slurp(FIXTURE))
        base = ["access", self.run_dir, "--need", "transcript", "--route", "device", "--tool", "device_stage_files", "--result", "ok"]
        r = drv(*base)
        self.assertEqual(r.returncode, 1)
        self.assertIn("needs its proof", r.stderr)
        r = drv(*base, "--file", copy)
        self.assertIn("needs its proof", r.stderr)
        # the fingerprint of ANOTHER file cannot be passed off
        r = drv(*base, "--file", copy, "--device-output", fingerprint(copy, shown_name="Something else.docx"))
        self.assertIn("names 'Something else.docx'", r.stderr)
        r = drv(*base, "--file", copy, "--device-output", "everything looked fine")
        self.assertIn("paste the whole output of", r.stderr)
        # the right fingerprint is accepted
        r = self.ok(*base, "--file", copy, "--device-output", fingerprint(copy))
        self.assertIn("'transcript' obtained via device", r.stdout)
        e = json.loads(slurp(os.path.join(self.run_dir, "access_log.json")))[-1]
        self.assertIs(e["verified"], True)
        self.assertEqual(e["sha256"], sha_of(copy))
        self.assertIn("copy verified", e["detail"])
        self.ok("done", self.run_dir, "locate")

    def test_a_copy_that_differs_from_the_computers_file_is_a_fail_not_a_success(self):
        self.start()
        self.bridge()
        copy = os.path.join(self.tmp, "staged", "Fact Find - Testcase.txt")
        spit(copy, "Fact Find for Sam Testcase. Absa home loan.")
        cut = fingerprint(copy).replace(sha_of(copy), "0" * 64)       # the computer's file is not what we hold
        r = drv("source", self.run_dir, "--kind", "Fact Find", "--path", "C:\\x\\Fact Find - Testcase.txt", "--date", "2026-10-01", "--read", "yes",
                "--file", copy, "--device-output", cut)
        self.assertEqual(r.returncode, 1)
        self.assertIn("not identical to the file on the computer", r.stderr)
        e = json.loads(slurp(os.path.join(self.run_dir, "access_log.json")))[-1]
        self.assertEqual(e["result"], "fail")
        self.assertIs(e["verified"], False)
        self.assertEqual(json.loads(slurp(os.path.join(self.run_dir, "sources.json"))), [])             # nothing was recorded as read
        # a cut-off size is caught the same way
        short = fingerprint(copy).rsplit("\n", 2)[0] + "\n5\n"
        r = drv("access", self.run_dir, "--need", "Fact Find", "--route", "device", "--tool", "t", "--result", "ok", "--file", copy, "--device-output", short)
        self.assertIn("logged as a FAIL", r.stdout)

    def test_a_client_document_is_never_taken_through_microsoft_365_or_zapier(self):
        self.start()
        for route in ("m365", "zapier"):
            for kind in ("Fact Find", "Fact Find Summary", "Earlier Note", "Overview", "Quote", "Application"):
                r = drv("access", self.run_dir, "--need", kind, "--route", route, "--tool", "read_resource", "--result", "ok")
                self.assertEqual(r.returncode, 1, kind)
                self.assertIn("arrives there cut off, as text", r.stderr)
        # the transcript and the correspondence are text: allowed (the transcript is proved complete by tx.py prep)
        self.ok("access", self.run_dir, "--need", "transcript", "--route", "zapier", "--tool", "t", "--result", "ok")
        self.ok("access", self.run_dir, "--need", "Correspondence", "--route", "m365", "--tool", "outlook_email_search", "--result", "ok")
        # a failed try is just logged
        self.ok("access", self.run_dir, "--need", "Overview", "--route", "m365", "--tool", "sharepoint_search", "--result", "fail", "--detail", "nothing found")

    def test_a_document_is_recorded_only_with_its_copy_and_the_program_makes_the_text(self):
        self.start()
        self.bridge()
        copy = os.path.join(self.tmp, "staged", "WR Overview - Testcase.txt")
        spit(copy, "WR Overview. Absa home loan. BrightRock Instant Life.")
        base = ["source", self.run_dir, "--kind", "Overview", "--path", "C:\\Clients\\WR Overview - Testcase.txt", "--date", "2026-10-01", "--read", "yes"]
        r = drv(*base)
        self.assertEqual(r.returncode, 1)
        self.assertIn("needs its proof", r.stderr)
        # the path must name the file that was really copied
        r = drv("source", self.run_dir, "--kind", "Overview", "--path", "C:\\Clients\\Another file.txt", "--date", "2026-10-01", "--read", "yes",
                "--file", copy, "--device-output", fingerprint(copy))
        self.assertIn("--path names 'another file.txt'", r.stderr)
        # a text file of the chat's own is not needed (and not allowed) when the program can read the document
        tf = os.path.join(self.tmp, "mine.txt")
        spit(tf, "the chat's own version of the text")
        r = drv(*base, "--file", copy, "--device-output", fingerprint(copy), "--text-file", tf)
        self.assertIn("--text-file is not needed", r.stderr)
        r = self.ok(*base, "--file", copy, "--device-output", fingerprint(copy))
        self.assertEqual(slurp(os.path.join(self.run_dir, "docs", "WR Overview - Testcase.txt")), "WR Overview. Absa home loan. BrightRock Instant Life.")
        entry = json.loads(slurp(os.path.join(self.run_dir, "sources.json")))[0]
        self.assertEqual((entry["via"], entry["bytes"], entry["file"]), ("device", os.path.getsize(copy), "WR Overview - Testcase.txt"))
        # a client document cannot be recorded through the text-only door
        r = drv("source", self.run_dir, "--kind", "Correspondence", "--path", "Outlook", "--date", "2026-10-01", "--read", "yes", "--ref", "mail", "--file", copy, "--device-output", fingerprint(copy))
        self.assertIn("are for the client's documents", r.stderr)

    def test_a_real_pdf_is_read_whole_by_the_program(self):
        self.start()
        self.bridge()
        pdf = os.path.join(self.tmp, "staged", "BrightRock quote 100000001.pdf")
        from reportlab.pdfgen import canvas
        c = canvas.Canvas(pdf)
        c.drawString(72, 760, "BrightRock Revised Reduced Quote CP 100000001, R1,100.00 p.m.")
        c.drawString(72, 740, "Instalment protector on the Absa home loan.")
        c.showPage()
        c.save()
        self.ok("source", self.run_dir, "--kind", "Quote", "--path", "C:\\x\\BrightRock quote 100000001.pdf", "--date", "2026-10-01", "--read", "yes",
                "--file", pdf, "--device-output", fingerprint(pdf))
        text = slurp(os.path.join(self.run_dir, "docs", "BrightRock quote 100000001.txt"))
        self.assertIn("CP 100000001, R1,100.00 p.m.", text)
        self.assertIn("Instalment protector", text)

    def test_a_scan_with_no_text_is_flagged_and_the_chat_may_add_what_it_read(self):
        self.start()
        self.bridge()
        pdf = os.path.join(self.tmp, "staged", "Scanned application.pdf")
        from reportlab.pdfgen import canvas
        c = canvas.Canvas(pdf)
        c.rect(72, 600, 200, 100)
        c.showPage()
        c.save()
        base = ["source", self.run_dir, "--kind", "Application", "--path", "C:\\x\\Scanned application.pdf", "--date", "2026-10-01", "--read", "yes",
                "--file", pdf, "--device-output", fingerprint(pdf)]
        r = self.ok(*base)
        self.assertIn("holds no text the program can read", r.stdout)
        self.assertIn("cannot be machine-checked", r.stdout)
        self.assertFalse(os.path.exists(os.path.join(self.run_dir, "docs", "Scanned application.txt")))
        self.start_clean()
        self.bridge()
        tf = os.path.join(self.tmp, "ocr.txt")
        spit(tf, "Application for BrightRock cover, Sam Testcase.")
        self.ok(*base, "--text-file", tf)
        e = json.loads(slurp(os.path.join(self.run_dir, "sources.json")))[0]
        self.assertIn("the chat", e["text_from"])
        self.assertTrue(os.path.exists(os.path.join(self.run_dir, "docs", "Scanned application.txt")))

    def start_clean(self):
        import shutil
        shutil.rmtree(self.run_dir)
        self.start()

    # ---- the checker
    def test_the_checker_fails_a_document_with_no_proof_and_a_run_with_no_computer(self):
        self.to_ready()
        srcs = self.sources()
        for e in srcs:
            if e.get("kind") == "Overview":
                for k in ("via", "sha256", "bytes", "file"):
                    e.pop(k, None)
        self.write("sources.json", srcs)
        self.assertFails(self.verify("pre"), "was not taken from the computer with its proof")
        self.to_ready()
        rj = self.load("run.json")
        rj.pop("computer")
        self.write("run.json", rj)
        self.assertFails(self.verify("pre"), "the computer was never connected in this run")

    def test_the_checker_fails_a_copy_that_was_never_proved_or_came_through_microsoft_365(self):
        self.to_ready()
        acc = self.access()
        acc[0] = dict(acc[0], verified=False)
        self.write("access_log.json", acc)
        self.assertFails(self.verify("pre"), "has no proof that it is identical to the original")
        self.to_ready()
        self.write("access_log.json", self.access() + [{"need": "Quote", "route": "m365", "tool": "read_resource", "result": "ok", "detail": "text"}])
        self.assertFails(self.verify("pre"), "was taken through m365, which returns a PDF or Word file cut off")

    def test_the_checker_fails_when_the_transcript_that_was_prepared_is_not_the_proved_copy(self):
        self.to_ready()
        acc = self.access()
        acc[0] = dict(acc[0], sha256="1" * 64)
        self.write("access_log.json", acc)
        self.assertFails(self.verify("pre"), "not the copy proved identical to the file on the computer")
        # a transcript that came as text from Microsoft 365 is checked by tx.py prep instead
        self.write("access_log.json", [dict(acc[0], route="m365", verified=None, sha256=None)] + acc[1:])
        self.assertNotIn("not the copy proved identical", self.verify("pre").stdout)

    def test_the_saved_pdf_must_be_the_pdf_that_was_built_and_saved_on_the_computer(self):
        self.to_final()
        v = self.verify("final")
        self.assertEqual(v.returncode, 0, v.stdout)
        self.assertIn("the PDF saved on the computer has the same fingerprint and size as the PDF built here", v.stdout)
        good = self.load("receipt.json")
        # no fingerprint of the saved file
        rc = json.loads(json.dumps(good))
        rc["saved"]["device_output"] = ""
        self.write("receipt.json", rc)
        self.assertFails(self.verify("final"), "device_output")
        # a different PDF on the computer
        rc = json.loads(json.dumps(good))
        rc["saved"]["device_output"] = rc["saved"]["device_output"].replace(self.load("state.json")["build"]["pdf_sha"], "2" * 64)
        self.write("receipt.json", rc)
        self.assertFails(self.verify("final"), "the PDF on the computer is not the PDF built here")
        # a different size
        rc = json.loads(json.dumps(good))
        size = str(self.load("state.json")["build"]["pdf_size"])
        rc["saved"]["device_output"] = rc["saved"]["device_output"].replace("\n" + size + "\n", "\n1\n")
        self.write("receipt.json", rc)
        self.assertFails(self.verify("final"), "the PDF on the computer is not the PDF built here")
        # the fingerprint of another file
        rc = json.loads(json.dumps(good))
        rc["saved"]["device_output"] = rc["saved"]["device_output"].replace(self.load("state.json")["build"]["pdf"], "Another file.pdf")
        self.write("receipt.json", rc)
        self.assertFails(self.verify("final"), "names 'Another file.pdf'")
        # saved through Microsoft 365 is not a save
        rc = json.loads(json.dumps(good))
        rc["saved"]["tool"] = "sharepoint_upload_file"
        self.write("receipt.json", rc)
        self.assertFails(self.verify("final"), "saved.tool must be device_commit_files")

    def test_the_pdf_step_demands_the_computers_fingerprint_before_it_is_done(self):
        self.through_build()
        name = "Follow-Up Appointment Summary Notes - 05.10.26 - (Testcase, Sam).pdf"
        self.receipts("png_visual_check=Page 1 looked at: navy title, bold headings, bullets with hanging indent, nothing cut off",
                      "independent_check=subagent: re-read the transcript against both outputs; every figure, name and status matched",
                      *["judgment.%s=Checked, nothing to change: %s" % (k, k) for k in ("quotes_named", "benefits_from_quote", "nothing_to_confirm_on_file", "independent_actions", "garbled_flagged")])
        self.ok("done", self.run_dir, "check")
        self.receipts("planner_page.mode=artifact", "planner_page.url=https://claude.ai/artifact/abc")
        self.ok("done", self.run_dir, "planner")
        self.receipts("pdf_sent_in_chat=true", "saved.tool=device_commit_files", "saved.folder=C:\\Clients\\Testcase, Sam\\2. Fact Find",
                      "saved.filename=" + name, "saved.tool_result=committed 1 file", "saved.folder_listing_check=listing shows " + name)
        r = drv("done", self.run_dir, "pdf")
        self.assertEqual(r.returncode, 1)
        self.assertIn("saved.device_output", r.stdout)
        built = self.load("state.json")["build"]
        wrong = "%s  /home/paul/%s\n%d\n" % ("3" * 64, name, built["pdf_size"])
        self.receipts("saved.device_output=" + wrong)
        r = drv("done", self.run_dir, "pdf")
        self.assertEqual(r.returncode, 1)
        self.assertIn("the PDF on the computer is not the PDF built here", r.stdout)
        self.receipts("saved.device_output=" + self.device_print())
        self.assertEqual(drv("done", self.run_dir, "pdf").returncode, 0)
