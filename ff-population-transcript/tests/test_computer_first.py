"""The computer comes first (Paul, 05/11/2026, after the first full real run): the program finds the client's OneDrive folder itself, stops at the start when it is not
there, proves every copy of a client file (byte for byte against the original on the computer, or by the connector's size), never reads a PDF as text or cut off,
lists the amounts only the form's PDF holds, and notices a ledger edited by hand. Invented data only."""
import os

from support import Chat, ENV, SCRIPTS, drv, sh, jdump, jload, slurp, spit


class ComputerFirst(Chat):
    def test_the_run_stops_at_the_start_when_the_computer_is_not_connected(self):
        self.s_start()
        ENV["WR_COMPUTER_ROOT"] = os.path.join(self.tmp, "no-such-folder")
        r = drv("computer", self.run_dir)
        self.assertEqual(r.returncode, 6, r.stdout + r.stderr)
        self.assertIn("STOP. This chat is not connected to your computer", r.stdout)
        r = self.refused("done", self.run_dir, "locate")
        self.assertIn("This chat is not connected to your computer", r.stdout)
        r = drv("access", self.run_dir, "--need", "form", "--route", "device", "--tool", "cp", "--result", "ok", "--file", self.form_path, "--original", self.form_path)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("has not found the computer", r.stdout + r.stderr)
        # only Paul's own words let the run go on without it
        self.refused("computer", self.run_dir, "--paul-go-on", "ok")
        self.ok("computer", self.run_dir, "--paul-go-on", "Go on without the computer")
        r = self.refused("done", self.run_dir, "locate")
        self.assertNotIn("This chat is not connected to your computer", r.stdout)

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
