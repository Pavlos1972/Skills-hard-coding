"""The computer comes first (Paul, 05/11/2026, after the first full real run): the program finds the client's OneDrive folder itself, stops at the start when it is not
there, proves every copy of a client file (byte for byte against the original on the computer, or by the connector's size), never reads a PDF as text or cut off,
lists the amounts only the form's PDF holds, and notices a ledger edited by hand. Invented data only."""
import hashlib
import os

from support import Chat, ENV, SCRIPTS, drv, sh, jdump, jload, slurp, spit
import wrlib as w


class ComputerFirst(Chat):
    def test_the_run_stops_at_the_start_when_the_computer_cannot_be_connected(self):
        self.s_start()
        ENV["WR_COMPUTER_ROOT"] = os.path.join(self.tmp, "no-such-folder")          # no folder mounted into this machine either
        r = drv("computer", self.run_dir)
        self.assertEqual(r.returncode, 6, r.stdout + r.stderr)
        self.assertIn("No connection is recorded yet", r.stdout)
        r = drv("computer", self.run_dir, "--none", "the request for folder access was refused")
        self.assertEqual(r.returncode, 6, r.stdout + r.stderr)
        self.assertIn("I could not connect this chat to your computer", r.stdout)
        r = self.refused("done", self.run_dir, "locate")
        self.assertIn("could not connect this chat to your computer", r.stdout)
        r = drv("access", self.run_dir, "--need", "form", "--route", "device", "--tool", "cp", "--result", "ok", "--file", self.form_path, "--original", self.form_path)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("has not found the computer", r.stdout + r.stderr)
        # only Paul's own words let the run go on without it
        self.refused("computer", self.run_dir, "--paul-go-on", "ok")
        self.ok("computer", self.run_dir, "--paul-go-on", "Go on without the computer")
        r = self.refused("done", self.run_dir, "locate")
        self.assertNotIn("could not connect this chat to your computer", r.stdout)

    def test_the_computer_through_the_device_tools_and_the_computers_own_fingerprint(self):
        self.s_start()
        ENV["WR_COMPUTER_ROOT"] = os.path.join(self.tmp, "no-such-folder")
        self.refused("computer", self.run_dir, "--device", "paul-pc", "--folder", "C:\\Users\\Paul\\Documents", "--listing", "a file name and another file name here")
        self.refused("computer", self.run_dir, "--device", "paul-pc", "--folder", "C:\\Users\\Paul\\liferisk.co.za", "--listing", "short")
        r = self.ok("computer", self.run_dir, "--device", "paul-kafentzis", "--folder", "C:\\Users\\Paul\\liferisk.co.za", "--listing",
                    "Fact Find (Audio to Text) - 05.11.2026 - Pat Samplecase.json; Teams meeting transcript - 05.11.26 - (Pat Samplecase).docx")
        self.assertIn("COMPUTER CONNECTED through the device tools", r.stdout)
        self.assertEqual(jload(self.p("run.json"))["computer"]["mode"], "bridge")
        with open(self.form_path, "rb") as fh:
            data = fh.read()
        sha, name = hashlib.sha256(data).hexdigest(), os.path.basename(self.form_path)
        out = "%s  /home/user/mnt/liferisk.co.za/Company - Paul/New Business/Samplecase, Pat/2. Fact Find/%s\n%d\n" % (sha, name, len(data))
        args = ("access", self.run_dir, "--need", "form", "--route", "device", "--tool", "device_stage_files", "--result", "ok")
        # a whole copy matching the computer's own fingerprint is proved
        self.ok(*args, "--file", self.form_path, "--device-output", out)
        last = jload(self.p("access_log.json"))[-1]
        self.assertTrue(last["verified"])
        self.assertIn("identical to the file on the computer", last["detail"])
        # a cut-off copy cannot match it: logged as a failure
        short = os.path.join(self.tmp, name)
        os.makedirs(os.path.join(self.tmp, "short"), exist_ok=True)
        short = os.path.join(self.tmp, "short", name)
        with open(short, "wb") as fh:
            fh.write(data[:100])
        r = self.ok(*args, "--file", short, "--device-output", out)
        self.assertIn("logged as a FAIL", r.stdout)
        self.assertFalse(jload(self.p("access_log.json"))[-1]["verified"])
        # the fingerprint of ANOTHER file, or no size, is refused
        r = drv(*args, "--file", self.form_path, "--device-output", out.replace(name, "other.json"))
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("names 'other.json'", r.stdout + r.stderr)
        r = drv(*args, "--file", self.form_path, "--device-output", "%s  %s\n" % (sha, name))
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("paste the whole output", r.stdout + r.stderr)
        # the PDF through Microsoft 365 is still refused, and the parser is exact
        self.assertEqual(w.parse_device_output(out, name), (sha, len(data), None))
        self.assertIsNotNone(w.parse_device_output(out, "x.json")[2])

    def test_a_found_file_without_its_proof_is_refused(self):
        self.s_start()
        self.ensure_computer(self.run_dir)
        for route in ("device", "m365", "zapier"):
            r = drv("access", self.run_dir, "--need", "form", "--route", route, "--tool", "t", "--result", "ok")
            self.assertNotEqual(r.returncode, 0, route)
            self.assertIn("needs its proof", r.stdout + r.stderr)

    def test_a_copy_that_is_not_identical_to_the_original_is_a_failure(self):
        self.s_start()
        self.ensure_computer(self.run_dir)
        orig = os.path.join(self.comp_folder, os.path.basename(self.form_path))
        spit(orig, slurp(self.form_path))
        short = os.path.join(self.tmp, "short.json")
        spit(short, slurp(self.form_path)[:200])
        r = self.ok("access", self.run_dir, "--need", "form", "--route", "device", "--tool", "cp", "--result", "ok", "--file", short, "--original", orig)
        self.assertIn("logged as a FAIL", r.stdout)
        last = jload(self.p("access_log.json"))[-1]
        self.assertEqual(last["result"], "fail")
        self.assertFalse(last["verified"])
        # a file outside the computer's folder cannot be called an original
        r = drv("access", self.run_dir, "--need", "form", "--route", "device", "--tool", "cp", "--result", "ok", "--file", self.form_path, "--original", self.form_path)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("must be a file on the computer", r.stdout + r.stderr)

    def test_the_form_pdf_cannot_be_taken_through_microsoft_365_or_zapier(self):
        self.s_start()
        self.ensure_computer(self.run_dir)
        for route in ("m365", "zapier"):
            r = drv("access", self.run_dir, "--need", "formpdf", "--route", route, "--tool", "t", "--result", "ok", "--file", self.pdf_path, "--source-size", os.path.getsize(self.pdf_path))
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("cannot be taken through", r.stdout + r.stderr)

    def test_a_cut_off_pdf_and_a_text_copy_of_a_pdf_are_never_read(self):
        self.s_start()
        self.s_locate()
        self.ok("form", self.run_dir, self.form_path)
        with open(self.pdf_path, "rb") as fh_:
            whole = fh_.read()
        for name, data in (("cut.pdf", whole[:1500]), ("copy.txt", b"WR Fact Find v3.0 Pat Samplecase 05/11/2026")):
            copy = os.path.join(self.tmp, name)
            with open(copy, "wb") as fh:
                fh.write(data)
            orig = os.path.join(self.comp_folder, name)
            with open(orig, "wb") as fh:
                fh.write(data)
            self.ok("access", self.run_dir, "--need", "formpdf", "--route", "device", "--tool", "cp", "--result", "ok", "--file", copy, "--original", orig)
            r = drv("formpdf", self.run_dir, copy)
            self.assertEqual(r.returncode, 4, r.stdout + r.stderr)
            self.assertIn("not the whole PDF", r.stdout + r.stderr)
        # a PDF that was not proved identical to its original is refused too
        r = drv("formpdf", self.run_dir, self.pdf_path + ".other")
        self.assertNotEqual(r.returncode, 0)

    def test_a_ledger_edited_by_hand_is_seen_by_the_checker(self):
        self.through("pass1")
        led = jload(self.p("ledger.json"))
        led["entries"] = led["entries"][:-1]
        jdump(self.p("ledger.json"), led)
        out = self.verify("--stage", "pre", "--full")
        self.assertIn("ledger.json was changed outside the program", out.stdout)


class PdfOnlyAmounts(Chat):
    pdf_extra = ("Risk Calculation: Total household income needed R 6 200.00",)

    def test_an_amount_only_the_pdf_holds_is_listed_and_can_be_reviewed(self):
        self.s_start()
        self.s_locate()
        self.ok("form", self.run_dir, self.form_path)
        r = self.ok("formpdf", self.run_dir, self.pdf_path)
        self.assertIn("WHOLE PDF READ", r.stdout)
        self.assertIn("AMOUNTS ONLY THE PDF HOLDS", r.stdout)
        fp = jload(self.p("form_pdf.json"))
        self.assertEqual(len(fp["pdf_only"]), 1)
        amt = fp["pdf_only"][0]
        self.assertIn("6200", amt)
        self.assertGreater(fp["bytes"], 1000)
        self.assertGreaterEqual(fp["pages"], 1)
        r = self.refused("pdfreview", self.run_dir, "--key", "pdf-only:" + amt, "--result", "not_printed", "--quote", "Total household income needed R 6 200.00", "--reason", "short")
        r = self.ok("pdfreview", self.run_dir, "--key", "pdf-only:" + amt, "--result", "not_printed", "--quote", "Total household income needed R 6 200.00",
                    "--reason", "the layout has no row for this form-computed figure")
        self.assertIn("recorded pdf-only:", r.stdout)
        self.assertEqual(jload(self.p("form_pdf.json"))["reviews"]["pdf-only:" + amt]["result"], "not_printed")


if __name__ == "__main__":
    import unittest
    unittest.main()
