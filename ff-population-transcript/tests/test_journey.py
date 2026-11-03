"""The whole chat, start to the final printout, on the invented household (Pat Samplecase). The program is run exactly as a chat runs it."""
import json
import os
import unittest

from support import Chat, COMMAND_LOG, drv, jload, slurp, sh


class Journey(Chat):
    def test_full_journey_from_start_to_pass(self):
        r = self.s_start()
        self.assertIn("SAY THIS TO PAUL FIRST", r.stdout)
        self.assertIn("Using ff-population-transcript, last updated", r.stdout)
        self.assertIn("STEP 1 of 16", r.stdout)
        for step in self.ORDER[1:]:
            if step == "content":
                self.s_content_done()
            else:
                getattr(self, "s_" + step)()
        r = self.s_final()                                          # the last step prints the checker's whole printout
        out = r.stdout
        print(out[-5000:])
        self.assertIn("RESULT: PASS", out)
        self.assertIn("SOURCE REPORT", out)
        self.assertIn("WHAT PAUL SHOULD GLANCE AT", out)
        self.assertIn("DELIVERY LINE", out)
        self.assertIn("EVERY STEP IS DONE", out)
        self.assertIn("FONT:", out)
        self.assertIn("PROVEN BY THE PROGRAM", out)
        self.assertIn("ONLY ATTESTED BY CLAUDE", out)
        # the hand-over was proven against a REAL Teams run driven on the same invented call (A4), not just a folder that was started
        teams_run = os.path.join(self.tmp, "teams-run")
        self.assertTrue(os.path.exists(os.path.join(teams_run, "out", "teams_message.txt")))
        self.assertTrue(os.path.exists(os.path.join(teams_run, "out", "planner_note.html")))
        self.assertIn("has every step before its message step done", out)
        self.assertIn("verify.py --skip-teams, in the Teams skill folder the chat named) printed RESULT: PASS", out)
        self.assertIn("Teams program fingerprint", out)                       # N4: the fingerprint of the named Teams folder is printed for Paul to compare
        self.assertIn("program fingerprint", out)                            # N9
        st = jload(self.p("state.json"))
        pdf = os.path.join(self.p("out"), st["build"]["pdf"])
        self.assertEqual(os.path.getsize(pdf), st["build"]["pdf_size"])
        rc = jload(self.p("receipt.json"))
        self.assertEqual(str(rc["saved"]["listed_size"]), str(st["build"]["pdf_size"]))        # the PDF was saved and listed back at the same size
        self.assertEqual(st["build"]["pdf"], "Fact Find Transcript - 05.11.26 - (Pat Samplecase).pdf")
        rj = jload(self.p("run.json"))
        self.assertEqual([s for s in rj["steps"] if rj["steps"][s]["state"] == "done"].__len__(), 16)
        # the run folder holds the evidence a recovered chat needs
        for name in ("state.json", "ledger.json", "sources.json", "access_log.json", "form_read.json", "crosscheck.json", "claims.json", "overlay.json", "content.json", "receipt.json"):
            self.assertTrue(os.path.exists(self.p(name)), name)
        s = drv("status", self.run_dir)
        self.assertNotIn("NEXT ->", s.stdout)


if __name__ == "__main__":
    unittest.main()
