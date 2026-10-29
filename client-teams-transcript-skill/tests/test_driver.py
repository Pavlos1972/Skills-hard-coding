"""Tests for the step driver (run.py), the client-file/access rules and the Planner page.

Run from the skill folder:  python3 -m unittest discover -s tests -v
Invented people and figures only.
"""
import json
import os
import shutil
import subprocess
import sys
import unittest

from test_gate import Base, ENV, FIXTURE, HERE, SCRIPTS, sh, slurp, spit


def drv(*args, env=None):
    return subprocess.run([sys.executable, os.path.join(SCRIPTS, "run.py")] + [str(a) for a in args],
                          capture_output=True, text=True, env=env or ENV)


class DriverBase(Base):
    def start(self, mt="followup"):
        r = drv("start", self.run_dir, "--type", mt)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return r

    def ok(self, *args):
        r = drv(*args)
        self.assertEqual(r.returncode, 0, "%s\n%s%s" % (args, r.stdout, r.stderr))
        return r

    def log_ok(self):
        self.ok("access", self.run_dir, "--need", "transcript", "--route", "device", "--tool", "device_stage_files", "--result", "ok")

    def read_pass(self, p):
        k = len(self.load("state.json")["chunks"])
        for n in range(1, k + 1):
            sh("tx.py", "chunk", self.run_dir, p, n, ok=True)

    def add_ledger(self):
        for e in self.ledger()["entries"]:
            self.ok("ledger", self.run_dir, "add", "--line", e["line"], "--kind", e["kind"], "--quote", e["quote"])

    def record_sources(self, kinds=None):
        for e in self.sources():
            if kinds and e["kind"] not in kinds:
                continue
            if "none" in e:
                self.ok("source", self.run_dir, "--kind", e["kind"], "--none", e["none"])
            else:
                self.ok("source", self.run_dir, "--kind", e["kind"], "--path", e["path"], "--date", e["date"], "--read", "yes")

    def cover_all(self):
        for e in self.ledger()["entries"]:
            if e["covered_by"]:
                self.ok("ledger", self.run_dir, "cover", e["id"], *e["covered_by"])
            else:
                self.ok("ledger", self.run_dir, "exclude", e["id"], e["excluded"])


class Journey(DriverBase):
    def test_full_followup_journey_from_start_to_pass(self):
        out = self.start().stdout
        self.assertIn("SELF-TEST", out)
        self.assertIn("STEP 1 of 14", out)
        self.assertIn("Standing rules for the whole job", out)
        self.assertIn("run.py status %s" % self.run_dir, out)             # placeholders were filled in
        # steps cannot be done out of order, and a step without proof is refused
        r = drv("done", self.run_dir, "prep")
        self.assertEqual(r.returncode, 3)
        self.assertIn("finish step 'locate' first", r.stderr)
        r = drv("done", self.run_dir, "locate")
        self.assertEqual(r.returncode, 1)
        self.assertIn("no successful access entry", r.stdout)
        self.log_ok()
        self.assertIn("STEP 'locate' DONE", self.ok("done", self.run_dir, "locate").stdout)
        sh("tx.py", "prep", FIXTURE, self.run_dir, ok=True)
        self.ok("done", self.run_dir, "prep")
        # client file must be read (or explained) before the reading starts
        r = drv("done", self.run_dir, "context")
        self.assertEqual(r.returncode, 1)
        self.assertIn("not accounted for", r.stdout)
        self.record_sources()
        self.ok("done", self.run_dir, "context")
        # pass 1: needs reads and a ledger
        self.assertEqual(drv("done", self.run_dir, "pass1").returncode, 1)
        self.read_pass(1)
        self.assertEqual(drv("done", self.run_dir, "pass1").returncode, 1)  # still no ledger entries
        self.add_ledger()
        self.ok("done", self.run_dir, "pass1")
        self.assertEqual(drv("done", self.run_dir, "pass2").returncode, 1)
        self.read_pass(2)
        self.ok("done", self.run_dir, "pass2")
        self.assertEqual(drv("done", self.run_dir, "scan").returncode, 1)
        sh("tx.py", "scan", self.run_dir, ok=True)
        self.ok("done", self.run_dir, "scan")
        # content
        self.write("content.json", self.content())
        r = drv("done", self.run_dir, "content")
        self.assertEqual(r.returncode, 1)                                   # ledger not yet covered
        self.assertIn("is not covered", r.stdout)
        self.cover_all()
        self.ok("done", self.run_dir, "content")
        self.assertEqual(drv("done", self.run_dir, "build").returncode, 1)
        sh("build.py", self.run_dir, ok=True)
        self.ok("done", self.run_dir, "build")
        # hand-over
        self.assertEqual(drv("done", self.run_dir, "look").returncode, 1)
        self.ok("receipt", self.run_dir, "--set", "png_visual_check=Page 1 looked at: navy title, bold headings, bullets with hanging indent, nothing cut off")
        self.ok("done", self.run_dir, "look")
        self.assertEqual(drv("done", self.run_dir, "planner").returncode, 1)
        self.ok("receipt", self.run_dir, "--set", "planner_page.mode=artifact", "--set", "planner_page.url=https://claude.ai/artifact/abc")
        self.ok("done", self.run_dir, "planner")
        name = "Follow-Up Appointment Summary Notes - 05.10.26 - (Testcase, Sam).pdf"
        self.ok("receipt", self.run_dir, "--set", "pdf_sent_in_chat=true", "--set", "saved.tool=device_commit_files",
                "--set", "saved.folder=C:\\Clients\\Testcase, Sam\\2. Fact Find", "--set", "saved.filename=" + name,
                "--set", "saved.tool_result=committed 1 file", "--set", "saved.folder_listing_check=listing shows " + name)
        self.ok("done", self.run_dir, "pdf")
        self.ok("receipt", self.run_dir, "--set", "applications_handoff=n/a: no applications exist for this client")
        self.ok("done", self.run_dir, "handoffs")
        # Teams: shows the exact message and the Zapier route
        shown = drv("next", self.run_dir).stdout
        self.assertIn("2nd Teams Appointment Completed: 05/10/2026", shown)
        self.assertIn("Please take note of Follow Up Appt.", shown)
        self.assertIn("mcp__Zapier__microsoft_teams_send_chat_message", shown)
        self.assertIn("(1:1 Chat) Paul Kafentzis, Sitamah Nathoo", shown)
        self.assertIn("Do NOT use the Microsoft 365 connector", shown)
        self.assertEqual(drv("done", self.run_dir, "teams").returncode, 1)
        self.ok("receipt", self.run_dir, "--set", "teams.status=sent", "--set", "teams.message_id=1730200000000",
                "--set", "teams.sent_time=2026-10-29T11:30:00Z", "--set", "teams.approved_by_paul=yes, send it")
        self.ok("done", self.run_dir, "teams")
        final = drv("done", self.run_dir, "final")
        self.assertEqual(final.returncode, 0, final.stdout)
        # the final printout comes from `done final`? it prints the next step or the finish line; verify prints the block
        v = sh("verify.py", self.run_dir)
        self.assertEqual(v.returncode, 0, v.stdout)
        self.assertIn("RESULT: PASS", v.stdout)
        self.assertIn("DELIVERY LINE", v.stdout)
        st = drv("status", self.run_dir).stdout
        self.assertNotIn("waiting", st)

    def test_first_meeting_skips_what_does_not_apply(self):
        self.start("first")
        st = drv("status", self.run_dir).stdout
        for sid in ("context", "look", "pdf", "handoffs"):
            self.assertIn(sid, st.split("not applicable")[1])
        self.assertIn("teams", st.split("not applicable")[0])

    def test_whatsapp_has_no_teams_step(self):
        self.start("whatsapp")
        st = drv("status", self.run_dir).stdout
        self.assertIn("teams", st.split("not applicable")[1])

    def test_starting_twice_does_not_reset_the_run(self):
        self.start()
        self.log_ok()
        self.ok("done", self.run_dir, "locate")
        r = drv("start", self.run_dir, "--type", "followup")
        self.assertEqual(r.returncode, 0)
        self.assertIn("already exists", r.stdout)
        self.assertIn("STEP 2 of", r.stdout)

    def test_selftest_stops_instead_of_falling_back_to_text(self):
        env = dict(ENV, PATH="/nonexistent")
        r = drv("start", self.run_dir, "--type", "followup", env=env)
        self.assertEqual(r.returncode, 4)
        self.assertIn("pdftotext", r.stdout)
        self.assertIn("do NOT replace the PDF", r.stdout)
        self.assertFalse(os.path.exists(os.path.join(self.run_dir, "run.json")))

    def test_every_step_reference_page_exists(self):
        skill = os.path.dirname(SCRIPTS)
        steps = json.loads(slurp(os.path.join(skill, "steps.json")))["steps"]
        for s in steps:
            for r in ([s["ref"]] if isinstance(s["ref"], str) else s["ref"]):
                self.assertTrue(os.path.exists(os.path.join(skill, "references", r)), r)


class LedgerAndLogs(DriverBase):
    def prepped(self):
        self.start()
        sh("tx.py", "prep", FIXTURE, self.run_dir, ok=True)

    def test_wrong_quote_is_refused_when_added(self):
        self.prepped()
        r = drv("ledger", self.run_dir, "add", "--line", 10, "--kind", "request", "--quote", "please email me everything")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("not found at transcript line", r.stderr)

    def test_a_request_cannot_be_excluded(self):
        self.prepped()
        self.ok("ledger", self.run_dir, "add", "--line", self.L("put a review of Dana"), "--kind", "request",
                "--quote", "put a review of Dana's portfolio in your what's-next email")
        r = drv("ledger", self.run_dir, "exclude", "L1", "not important at all really")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("cannot be excluded", r.stderr)

    def test_cover_refuses_unknown_items(self):
        self.prepped()
        self.ok("ledger", self.run_dir, "add", "--line", self.L("put a review of Dana"), "--kind", "request",
                "--quote", "put a review of Dana's portfolio")
        self.write("content.json", self.content())
        r = drv("ledger", self.run_dir, "cover", "L1", "zzz")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("not in content.json", r.stderr)

    def test_asking_paul_needs_all_three_routes_tried(self):
        self.start()
        a = lambda route, res="fail": self.ok("access", self.run_dir, "--need", "overview", "--route", route,
                                              "--tool", "t_" + route, "--result", res, "--detail", "not found")
        r = drv("ask", self.run_dir, "--need", "overview", "--question", "Please send the Overview", "--searched", "OneDrive and SharePoint")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("no access attempts", r.stderr)
        self.assertIn("NEXT ROUTE TO TRY for 'overview': m365", a("device").stdout)
        r = drv("ask", self.run_dir, "--need", "overview", "--question", "Please send the Overview", "--searched", "OneDrive and SharePoint")
        self.assertIn("have not been tried", r.stderr)
        self.assertIn("zapier", r.stderr)
        a("m365")
        self.assertIn("All three routes have now failed", a("zapier").stdout)
        r = drv("ask", self.run_dir, "--need", "overview", "--question", "Please send the Overview", "--searched", "OneDrive and SharePoint")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("ask Paul, in plain words, exactly this", r.stdout)

    def test_gate_fails_when_a_route_was_never_tried(self):
        self.to_ready()
        log = self.access() + [{"need": "overview", "route": "device", "tool": "t", "result": "fail", "detail": "not found"}]
        self.write("access_log.json", log)
        r = self.verify("pre")
        self.assertFails(r, "never tried", "m365", "zapier")

    def test_gate_fails_when_all_failed_but_paul_was_never_given_the_question(self):
        self.to_ready()
        log = self.access() + [{"need": "overview", "route": rt, "tool": "t", "result": "fail", "detail": "x"} for rt in ("device", "m365", "zapier")]
        self.write("access_log.json", log)
        self.assertFails(self.verify("pre"), "nothing was recorded for Paul")

    def test_gate_fails_when_client_file_kinds_are_missing(self):
        self.to_ready()
        self.write("sources.json", [e for e in self.sources() if e["kind"] not in ("Overview", "Quote")])
        self.assertFails(self.verify("pre"), "not accounted for", "Overview", "Quote")

    def test_a_none_reason_must_say_what_was_searched(self):
        self.start()
        r = drv("source", self.run_dir, "--kind", "Overview", "--none", "none")
        self.assertNotEqual(r.returncode, 0)

    def test_receipt_cli_stores_nested_values_and_booleans(self):
        self.start()
        self.ok("receipt", self.run_dir, "--set", "pdf_sent_in_chat=true", "--set", "saved.tool=device_commit_files")
        rc = self.load("receipt.json")
        self.assertIs(rc["pdf_sent_in_chat"], True)
        self.assertEqual(rc["saved"]["tool"], "device_commit_files")


class TeamsMessage(Base):
    def built(self, mutate=None):
        self.to_ready()
        c = self.content()
        if mutate:
            mutate(c)
        self.write("content.json", c)
        sh("build.py", self.run_dir, ok=True)

    def message(self):
        return slurp(self.p("out", "teams_message.txt")).strip()

    def test_wording_and_follow_up_sentence(self):
        self.built()
        self.assertEqual(self.message(),
                         "Sam Testcase \u2013 2nd Teams Appointment Completed: 05/10/2026 \u2013 Please see instructions in Client / Prospect Task. Please take note of Follow Up Appt.")

    def test_vague_next_appointment_leaves_the_sentence_out(self):
        self.built(lambda c: c["next_appointment"].update(agreed=False, text="Early next month, date to be set",
                                                           check="Summary says date to be set: a vague intention, not an agreed appointment"))
        self.assertTrue(self.message().endswith("Please see instructions in Client / Prospect Task."))
        self.assertNotIn("Follow Up Appt", self.message())

    def test_review_wording_and_third_appointment(self):
        self.built(lambda c: c.update(appointment_number="review"))
        self.assertIn("Review Teams Appointment Completed", self.message())
        self.tearDown_run()
        self.built(lambda c: c.update(appointment_number=3))
        self.assertIn("3rd Teams Appointment", self.message())

    def tearDown_run(self):
        shutil.rmtree(self.run_dir, ignore_errors=True)

    def test_appointment_number_must_be_justified_and_valid(self):
        self.to_ready()
        c = self.content()
        c["appointment_number"] = 0
        c["appointment_number_basis"] = "x"
        self.write("content.json", c)
        self.assertFails(self.verify("pre"), "appointment_number must be", "appointment_number_basis")

    def test_agreed_flag_and_check_line_are_required(self):
        self.to_ready()
        c = self.content()
        del c["next_appointment"]["agreed"]
        c["next_appointment"]["check"] = ""
        self.write("content.json", c)
        self.assertFails(self.verify("pre"), "next_appointment.agreed", "next_appointment.check")

    def test_a_message_edited_by_hand_fails(self):
        self.built()
        spit(self.p("out", "teams_message.txt"), "Sam Testcase \u2013 1st Teams Appointment Completed: 05/10/2026 \u2013 Please see instructions in Client / Prospect Task.\n")
        self.assertFails(self.verify("built"), "teams_message.txt was edited by hand")

    def test_whatsapp_produces_no_teams_message(self):
        self.built(lambda c: c.update(meeting_type="whatsapp", meeting_time="14:30"))
        self.assertFalse(os.path.exists(self.p("out", "teams_message.txt")))

    def receipt_with(self, **teams):
        self.to_built()
        rc = self.receipt()
        rc["teams"] = teams
        self.write("receipt.json", rc)
        return self.verify()

    def test_teams_sent_needs_the_zapier_result_and_pauls_yes(self):
        self.assertFails(self.receipt_with(status="sent", message_id="", sent_time="", approved_by_paul=""), "status=sent needs message_id")

    def test_teams_not_recorded_fails(self):
        self.assertFails(self.receipt_with(), "teams.status must be sent, declined or failed")

    def test_teams_failed_must_hand_the_text_to_paul(self):
        self.assertFails(self.receipt_with(status="failed", detail="Zapier returned 500 on the send"), "text_given_to_paul")
        self.tearDown_run()
        r = self.receipt_with(status="failed", detail="Zapier returned 500 on the send", text_given_to_paul=True)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("not claimed as sent", r.stdout)

    def test_teams_declined_is_recorded(self):
        r = self.receipt_with(status="declined", paul_said="no, I will message her myself")
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_planner_page_receipt_rules(self):
        self.to_built()
        rc = self.receipt()
        rc["planner_page"] = {"mode": "artifact", "url": "see above"}
        self.write("receipt.json", rc)
        self.assertFails(self.verify(), "planner_page.url must be the link")
        rc["planner_page"] = {"mode": "fallback_text", "reason": ""}
        self.write("receipt.json", rc)
        self.assertFails(self.verify(), "the fallback must be stated")
        rc["planner_page"] = {"mode": "fallback_text", "reason": "the Artifact tool is not available in this chat"}
        self.write("receipt.json", rc)
        r = self.verify()
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("FALLBACK", r.stdout)


class PlannerPage(Base):
    def test_page_has_copy_button_title_and_all_eight_areas(self):
        self.to_ready()
        c = self.content()
        for key, text in (("rgar", "RGAR: retire at 55, R40k net p.m. needs R24,921 p.m."), ("egar", "EGAR: school fees goal R1m by 2035"),
                          ("medical", "Medical aid: Discovery Classic, broker-of-record to move to WR"),
                          ("short_term", "Short-term: vehicle schedule sent to the broker")):
            c["areas"].append({"key": key, "bullets": [{"id": "x_" + key, "text": text, "status": "still open",
                                                         "src": [self.src("one thousand one hundred rand a month")]}]})
        self.write("content.json", c)
        sh("build.py", self.run_dir, ok=True)
        page = slurp(self.p("out", "planner_note.html"))
        self.assertIn("<title>Testcase Planner Note</title>", page)
        self.assertIn('id="copy-note"', page)
        order = [page.index("<b>%s</b>" % h) for h in ("Risk", "RA", "Investment", "RGAR", "EGAR", "Medical Aid", "Will", "Short-Term")]
        self.assertEqual(order, sorted(order))
        self.assertNotIn("Not discussed this meeting", page)
        pdf_txt = subprocess.run(["pdftotext", self.p("out", [f for f in os.listdir(self.p("out")) if f.endswith(".pdf")][0]), "-"],
                                 capture_output=True, text=True).stdout
        for h in ("RGAR", "EGAR", "Medical Aid", "Short-Term"):
            self.assertIn(h, pdf_txt)

    def test_unknown_area_key_fails(self):
        self.to_ready()
        c = self.content()
        c["areas"].append({"key": "retirement", "bullets": []})
        self.write("content.json", c)
        self.assertFails(self.verify("pre"), "areas keys must be unique and from")

    def test_page_is_the_only_home_and_has_no_code_fence(self):
        self.to_built()
        self.assertNotIn("```", slurp(self.p("out", "planner_note.txt")))
        self.assertNotIn("```", slurp(self.p("out", "planner_note.html")))

    def test_edited_page_fails(self):
        self.to_built()
        spit(self.p("out", "planner_note.html"), slurp(self.p("out", "planner_note.html")) + "<!-- typed by hand -->", "w")
        self.assertFails(self.verify("built"), "planner_note.html was edited by hand")

    @unittest.skipUnless(shutil.which("node"), "node not installed")
    def test_copy_button_works_in_a_real_browser(self):
        self.to_built()
        shot = os.path.join(self.tmp, "page.png")
        r = subprocess.run(["node", os.path.join(HERE, "browser_copy_test.js"), self.p("out", "planner_note.html"), shot],
                           capture_output=True, text=True, timeout=120)
        if r.returncode != 0 and "Cannot find module" in r.stderr:
            self.skipTest("playwright not installed")
        self.assertEqual(r.returncode, 0, r.stderr)
        res = json.loads(r.stdout)
        self.assertEqual(res["errors"], [])
        self.assertFalse(res["horizontalScroll"])
        self.assertTrue(res["htmlHasBold"] and res["htmlHasBullet"] and res["plainHasAction"])
        self.assertFalse(res["plainHasMarkdownStars"])
        self.assertIn("Copied", res["status"])


if __name__ == "__main__":
    unittest.main()
