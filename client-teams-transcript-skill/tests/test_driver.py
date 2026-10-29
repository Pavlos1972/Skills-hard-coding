"""Tests for the step driver (run.py), the client-file/access rules, the Teams message and the Planner page.

Run from the skill folder:  python3 -m unittest discover -s tests -v
Invented people and figures only.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import unittest

from test_gate import Base, DOCS, ENV, FIXTURE, HERE, JUDGMENT_KEYS, SCRIPTS, sh, slurp, spit

CLIENT = ["--client", "Sam Testcase", "--date", "05/10/2026"]


def drv(*args, env=None):
    return subprocess.run([sys.executable, os.path.join(SCRIPTS, "run.py")] + [str(a) for a in args],
                          capture_output=True, text=True, env=env or ENV)


class DriverBase(Base):
    def start(self, mt="followup"):
        r = drv("start", self.run_dir, "--type", mt, *CLIENT)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return r

    def ok(self, *args):
        r = drv(*args)
        self.assertEqual(r.returncode, 0, "%s\n%s%s" % (args, r.stdout, r.stderr))
        return r

    def log_ok(self):
        self.ok("access", self.run_dir, "--need", "transcript", "--route", "device", "--tool", "device_stage_files", "--result", "ok")

    def read_pass(self, p):
        """Read each chunk, then record its entries (or acknowledge it), exactly as Claude has to."""
        st = self.load("state.json")
        for n, (a, b) in enumerate(st["chunks"], 1):
            sh("tx.py", "chunk", self.run_dir, p, n, ok=True)
            mine = [e for e in self.ledger()["entries"] if e["pass"] == p and a <= e["line"] <= b]
            for e in mine:
                self.ok("ledger", self.run_dir, "add", "--line", e["line"], "--kind", e["kind"], "--quote", e["quote"])
            if not mine:
                self.ok("ledger", self.run_dir, "ack", "--pass", p, "--chunk", n, "--reason", "read this chunk in full; it holds no decision, request or figure to record")

    def record_sources(self):
        for ref, (kind, text) in DOCS.items():
            tf = os.path.join(self.tmp, ref + ".txt")
            spit(tf, text)
            self.ok("source", self.run_dir, "--kind", kind, "--path", "C:\\Clients\\Testcase, Sam\\" + ref + ".pdf",
                    "--date", "2026-10-01", "--read", "yes", "--ref", ref, "--text-file", tf)
        for route in ("device", "m365"):
            self.ok("access", self.run_dir, "--need", "Application", "--route", route, "--tool", "t_" + route, "--result", "fail", "--detail", "nothing found")
        self.ok("source", self.run_dir, "--kind", "Application", "--none", "searched the Applications folder of both current transactions: none on file yet")

    def cover_all(self):
        want = {e["quote"]: e for e in self.ledger()["entries"]}
        for e in self.load("ledger.json")["entries"]:
            w_ = want[e["quote"]]
            if w_["covered_by"]:
                self.ok("ledger", self.run_dir, "cover", e["id"], *w_["covered_by"])
            else:
                self.ok("ledger", self.run_dir, "exclude", e["id"], w_["excluded"])

    def receipts(self, *pairs):
        self.ok("receipt", self.run_dir, *[x for p in pairs for x in ("--set", p)])

    def through_build(self):
        """start .. build, all done through the driver."""
        self.start()
        self.log_ok()
        self.ok("done", self.run_dir, "locate")
        sh("tx.py", "prep", FIXTURE, self.run_dir, ok=True)
        self.ok("done", self.run_dir, "prep")
        self.record_sources()
        self.ok("done", self.run_dir, "context")
        self.read_pass(1)
        self.ok("done", self.run_dir, "pass1")
        self.read_pass(2)
        self.ok("done", self.run_dir, "pass2")
        sh("tx.py", "scan", self.run_dir, ok=True)
        self.ok("done", self.run_dir, "scan")
        self.write("content.json", self.content())
        self.cover_all()
        self.ok("done", self.run_dir, "content")
        sh("build.py", self.run_dir, ok=True)
        self.ok("done", self.run_dir, "build")

    def handover_receipts(self):
        name = "Follow-Up Appointment Summary Notes - 05.10.26 - (Testcase, Sam).pdf"
        self.receipts("png_visual_check=Page 1 looked at: navy title, bold headings, bullets with hanging indent, nothing cut off",
                      "independent_check=subagent: re-read the transcript against both outputs; every figure, name and status matched",
                      *["judgment.%s=Checked, nothing to change: %s" % (k, k.replace("_", " ")) for k in JUDGMENT_KEYS])
        self.ok("done", self.run_dir, "check")
        self.receipts("planner_page.mode=artifact", "planner_page.url=https://claude.ai/artifact/abc")
        self.ok("done", self.run_dir, "planner")
        self.receipts("pdf_sent_in_chat=true", "saved.tool=device_commit_files", "saved.folder=C:\\Clients\\Testcase, Sam\\2. Fact Find",
                      "saved.filename=" + name, "saved.tool_result=committed 1 file", "saved.folder_listing_check=listing shows " + name)
        self.ok("done", self.run_dir, "pdf")
        self.receipts("applications_handoff=n/a: no applications exist for this client",
                      "revised_quote_draft=shown to Paul: revised Tax-Free quote request to Alwyn, draft only, not sent")
        self.ok("done", self.run_dir, "handoffs")


class Journey(DriverBase):
    def test_full_followup_journey_from_start_to_pass(self):
        out = self.start().stdout
        self.assertIn("SELF-TEST", out)
        self.assertIn("STEP 1 of 14", out)
        self.assertIn("Standing rules for the whole job", out)
        self.assertIn("client: Sam Testcase   meeting date: 05/10/2026", out)
        self.assertIn("run.py status %s" % self.run_dir, out)             # placeholders were filled in with the absolute path
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
        # the client file must be read (or explained) before the reading starts
        r = drv("done", self.run_dir, "context")
        self.assertEqual(r.returncode, 1)
        self.assertIn("not accounted for", r.stdout)
        self.record_sources()
        self.ok("done", self.run_dir, "context")
        # pass 1: needs reads, ledger entries and acknowledged chunks
        self.assertEqual(drv("done", self.run_dir, "pass1").returncode, 1)
        self.read_pass(1)
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
        # check, planner, pdf, hand-offs
        self.assertEqual(drv("done", self.run_dir, "check").returncode, 1)
        self.handover_receipts()
        # Teams: shows the exact message and the Zapier route, only now that everything else passes
        shown = drv("next", self.run_dir).stdout
        self.assertIn("Sam Testcase (Review Client) \u2013 2nd Teams Appointment Completed: 05/10/2026", shown)
        self.assertIn("Please take note of Follow Up Appt.", shown)
        self.assertIn("mcp__Zapier__microsoft_teams_send_chat_message", shown)
        self.assertIn("(1:1 Chat) Paul Kafentzis, Sitamah Nathoo", shown)
        self.assertIn("Do NOT use the Microsoft 365 connector", shown)
        self.assertIn("teams.approved_by_paul", shown)
        self.assertIn("teams.body_as_stored", shown)
        self.assertEqual(drv("done", self.run_dir, "teams").returncode, 1)
        msg = self.teams_text()
        self.receipts("teams.status=sent", "teams.message_id=1730200000000", "teams.sent_time=2026-10-29T11:30:00Z",
                      "teams.body_as_stored=<h1><b>%s</b></h1>" % msg, "teams.approved_by_paul=yes, send it")
        self.ok("done", self.run_dir, "teams")
        v = sh("verify.py", self.run_dir)
        self.assertEqual(v.returncode, 0, v.stdout)
        self.assertIn("RESULT: PASS", v.stdout)
        self.assertIn("DELIVERY LINE", v.stdout)
        final = drv("done", self.run_dir, "final")
        self.assertEqual(final.returncode, 0, final.stdout)
        self.assertIn("RESULT: PASS", final.stdout)                          # the printout reaches the transcript through `done final` too
        self.assertNotIn("waiting", drv("status", self.run_dir).stdout)

    def test_first_meeting_skips_what_does_not_apply(self):
        self.start("first")
        st = drv("status", self.run_dir).stdout
        for sid in ("context", "pdf", "handoffs"):
            self.assertIn(sid, st.split("not applicable")[1])
        self.assertIn("teams", st.split("not applicable")[0])
        self.assertIn("check", st.split("not applicable")[0])

    def test_whatsapp_has_the_teams_step(self):
        # Paul, 29/10/2026: a WhatsApp call also notifies Sitamah
        self.start("whatsapp")
        st = drv("status", self.run_dir).stdout
        self.assertIn("teams ", st)
        self.assertNotIn("not applicable", st)

    # ---- the version sentence (Paul, 29/10/2026): it comes from the stamp, so it moves with every update
    def real_version_sentence(self):
        stamp = re.search(r"\*\*Last updated: (\d{4})-(\d{2})-(\d{2}) (\d{2}:\d{2})", slurp(os.path.join(os.path.dirname(SCRIPTS), "SKILL.md")))
        return "Using client-teams-transcript-skill, last updated %s/%s/%s %s (Athens time)" % (stamp.group(3), stamp.group(2), stamp.group(1), stamp.group(4))

    def test_start_tells_claude_to_say_the_version_first(self):
        r = self.start()
        self.assertIn("SAY THIS TO PAUL FIRST", r.stdout)
        self.assertIn(self.real_version_sentence() + ".", r.stdout)
        self.assertLess(r.stdout.index("SAY THIS TO PAUL FIRST"), r.stdout.index("Standing rules for the whole job"))

    def test_the_version_sentence_follows_the_stamp_and_is_not_written_into_the_program(self):
        copy = os.path.join(self.tmp, "client-teams-transcript-skill")
        shutil.copytree(os.path.dirname(SCRIPTS), copy, ignore=shutil.ignore_patterns("__pycache__", "tests", "history"))
        md = os.path.join(copy, "SKILL.md")
        spit(md, re.sub(r"\*\*Last updated:[^*]*\*\*", "**Last updated: 2027-01-02 03:04 (Athens time)**", slurp(md), 1))
        r = subprocess.run([sys.executable, os.path.join(copy, "scripts", "run.py"), "start", os.path.join(self.tmp, "run2"), "--type", "followup", *CLIENT],
                           capture_output=True, text=True, env=ENV)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("Using client-teams-transcript-skill, last updated 02/01/2027 03:04 (Athens time).", r.stdout)
        self.assertNotIn(self.real_version_sentence(), r.stdout)

    def test_an_unstamped_skill_says_so(self):
        copy = os.path.join(self.tmp, "client-teams-transcript-skill")
        shutil.copytree(os.path.dirname(SCRIPTS), copy, ignore=shutil.ignore_patterns("__pycache__", "tests", "history"))
        md = os.path.join(copy, "SKILL.md")
        spit(md, re.sub(r"\*\*Last updated:[^*]*\*\*\n", "", slurp(md), 1))
        r = subprocess.run([sys.executable, os.path.join(copy, "scripts", "run.py"), "start", os.path.join(self.tmp, "run3"), "--type", "followup", *CLIENT],
                           capture_output=True, text=True, env=ENV)
        self.assertIn("NOT STAMPED", r.stdout)

    def test_starting_twice_does_not_reset_the_run(self):
        self.start()
        self.log_ok()
        self.ok("done", self.run_dir, "locate")
        r = drv("start", self.run_dir, "--type", "followup", *CLIENT)
        self.assertEqual(r.returncode, 0)
        self.assertIn("already exists", r.stdout)
        self.assertIn("STEP 2 of", r.stdout)

    def test_start_needs_the_client_and_date_from_pauls_message(self):
        r = drv("start", self.run_dir, "--type", "followup")
        self.assertEqual(r.returncode, 2)
        r = drv("start", self.run_dir, "--type", "followup", "--client", "Sam Testcase", "--date", "31/02/2026")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("real date", r.stderr)
        r = drv("start", self.run_dir, "--type", "followup", "--client", "Sam", "--date", "05/10/2026")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("first name and surname", r.stderr)

    def test_selftest_stops_instead_of_falling_back_to_text(self):
        env = dict(ENV, PATH="/nonexistent")
        r = drv("start", self.run_dir, "--type", "followup", *CLIENT, env=env)
        self.assertEqual(r.returncode, 4)
        self.assertIn("pdftotext", r.stdout)
        self.assertIn("pandoc", r.stdout)
        self.assertIn("do NOT replace the PDF", r.stdout)
        self.assertFalse(os.path.exists(os.path.join(self.run_dir, "run.json")))

    def test_every_step_reference_page_exists(self):
        skill = os.path.dirname(SCRIPTS)
        steps = json.loads(slurp(os.path.join(skill, "steps.json")))["steps"]
        for s in steps:
            for r in ([s["ref"]] if isinstance(s["ref"], str) else s["ref"]):
                self.assertTrue(os.path.exists(os.path.join(skill, "references", r)), r)

    def test_a_rebuild_reopens_the_hand_over_steps(self):
        self.through_build()
        self.handover_receipts()
        c = self.content()
        c["actions"][3]["text"] = "Sitamah to request the revised Tax-Free quote in Sam's name from Alwyn today"
        self.write("content.json", c)
        r = sh("build.py", self.run_dir, ok=True)
        self.assertIn("HAND-OVER RE-OPENED", r.stdout)
        st = drv("status", self.run_dir).stdout
        for sid in ("check", "planner", "pdf", "handoffs"):
            self.assertRegex(st, r"\[(waiting|NEXT ->)\] %s" % sid)
        self.assertIn("NEXT: python3", st)

    def test_the_teams_message_is_held_back_while_anything_else_fails(self):
        self.through_build()
        self.handover_receipts()
        c = self.content()
        c["actions"][3]["text"] = "Sitamah to request the revised Tax-Free quote in Sam's name from Alwyn today"
        self.write("content.json", c)                       # edited after the build: the outputs are stale
        shown = drv("next", self.run_dir).stdout
        self.assertIn("NOT YET", shown)
        self.assertIn("content.json changed after the outputs were built", shown)
        self.assertNotIn("mcp__Zapier__microsoft_teams_send_chat_message", shown)


class LedgerAndLogs(DriverBase):
    def prepped(self):
        self.start()
        sh("tx.py", "prep", FIXTURE, self.run_dir, ok=True)

    def test_wrong_quote_is_refused_when_added(self):
        self.prepped()
        r = drv("ledger", self.run_dir, "add", "--line", 10, "--kind", "request", "--quote", "please email me everything")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("not found at transcript line", r.stderr)

    def test_ledger_add_before_prep_is_a_clear_refusal(self):
        self.start()
        r = drv("ledger", self.run_dir, "add", "--line", 3, "--kind", "fact", "--quote", "something said here")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("has not been prepared", r.stderr)
        self.assertNotIn("Traceback", r.stderr)

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

    def test_the_next_chunk_waits_for_an_entry_or_a_reasoned_acknowledgement(self):
        self.prepped()
        sh("tx.py", "chunk", self.run_dir, 1, 1, ok=True)
        self.assertEqual(sh("tx.py", "chunk", self.run_dir, 1, 2).returncode, 3)
        r = drv("ledger", self.run_dir, "ack", "--pass", 1, "--chunk", 1, "--reason", "nothing")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("at least 20 characters", r.stderr)
        r = drv("ledger", self.run_dir, "ack", "--pass", 1, "--chunk", 2, "--reason", "this chunk has not been read yet but here is a long reason")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("has not been read yet", r.stderr)
        self.ok("ledger", self.run_dir, "ack", "--pass", 1, "--chunk", 1, "--reason", "greetings and the first quote only; nothing to record yet")
        self.assertEqual(sh("tx.py", "chunk", self.run_dir, 1, 2).returncode, 0)

    def test_an_entry_in_the_chunk_also_unlocks_the_next_one(self):
        self.prepped()
        sh("tx.py", "chunk", self.run_dir, 1, 1, ok=True)
        ln = 12
        self.ok("ledger", self.run_dir, "add", "--line", ln, "--kind", "fact", "--quote", "instalment protector on your Absa home loan")
        self.assertEqual(sh("tx.py", "chunk", self.run_dir, 1, 2).returncode, 0)

    def test_entry_pass_label_follows_the_chunks_actually_read(self):
        self.prepped()
        self.read_pass(1)
        self.ok("ledger", self.run_dir, "add", "--line", 12, "--kind", "fact", "--quote", "instalment protector on your Absa home loan")
        self.assertEqual(self.load("ledger.json")["entries"][-1]["pass"], 1)      # still Pass 1: no Pass 2 chunk has been served yet

    def test_asking_paul_needs_all_three_routes_tried(self):
        self.start()
        a = lambda route, res="fail": self.ok("access", self.run_dir, "--need", "bank letter", "--route", route,
                                              "--tool", "t_" + route, "--result", res, "--detail", "not found")
        r = drv("ask", self.run_dir, "--need", "bank letter", "--question", "Please send the bank letter", "--searched", "OneDrive and SharePoint")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("no access attempts", r.stderr)
        self.assertIn("NEXT ROUTE TO TRY for 'bank letter': m365", a("device").stdout)
        r = drv("ask", self.run_dir, "--need", "bank letter", "--question", "Please send the bank letter", "--searched", "OneDrive and SharePoint")
        self.assertIn("have not been tried", r.stderr)
        self.assertIn("zapier", r.stderr)
        a("m365")
        self.assertIn("All three routes have now failed", a("zapier").stdout)
        r = drv("ask", self.run_dir, "--need", "bank letter", "--question", "Please send the bank letter", "--searched", "OneDrive and SharePoint")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("ask Paul, in plain words, exactly this", r.stdout)

    def test_none_on_file_needs_the_searches_to_be_logged(self):
        self.start()
        r = drv("source", self.run_dir, "--kind", "Overview", "--none", "searched OneDrive, nothing there")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("at least two routes", r.stderr)
        self.ok("access", self.run_dir, "--need", "Overview", "--route", "device", "--tool", "device_stage_files", "--result", "fail", "--detail", "nothing found")
        self.assertNotEqual(drv("source", self.run_dir, "--kind", "Overview", "--none", "searched OneDrive, nothing there").returncode, 0)
        self.ok("access", self.run_dir, "--need", "Overview", "--route", "m365", "--tool", "sharepoint_search", "--result", "fail", "--detail", "nothing found")
        self.ok("source", self.run_dir, "--kind", "Overview", "--none", "searched OneDrive and SharePoint, nothing there")

    def test_gate_fails_when_none_on_file_was_never_searched(self):
        self.to_ready()
        srcs = [e for e in self.sources() if e["kind"] != "Application"] + [{"kind": "Application", "none": "searched everywhere I could think of"}]
        self.write("sources.json", srcs)
        self.write("access_log.json", [e for e in self.access() if e["need"] == "transcript"])
        self.assertFails(self.verify("pre"), "recorded as 'none on file' but the searches are not logged")

    def test_a_text_copy_of_a_document_is_stored_for_checking(self):
        self.start()
        tf = os.path.join(self.tmp, "t.txt")
        spit(tf, "Quote CP 555555 R2,000 p.m.")
        r = self.ok("source", self.run_dir, "--kind", "Quote", "--path", "C:\\x\\My Quote.pdf", "--date", "2026-10-01", "--read", "yes", "--text-file", tf)
        self.assertEqual(slurp(os.path.join(self.run_dir, "docs", "My Quote.txt")), "Quote CP 555555 R2,000 p.m.")
        r = self.ok("source", self.run_dir, "--kind", "Quote", "--path", "C:\\y\\Other.pdf", "--date", "2026-10-01", "--read", "yes")
        self.assertIn("cannot be machine-checked", r.stdout)
        r = drv("source", self.run_dir, "--kind", "Quote", "--path", "C:\\z\\My Quote.pdf", "--date", "2026-10-01", "--read", "yes")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("already recorded", r.stderr)

    def test_gate_fails_when_none_of_the_clients_files_were_read(self):
        self.to_ready()
        self.write("sources.json", [])
        self.assertFails(self.verify("pre"), "client-file sources not accounted for")

    def test_gate_fails_when_a_route_was_never_tried(self):
        self.to_ready()
        self.write("access_log.json", self.access() + [{"need": "bank letter", "route": "device", "tool": "t", "result": "fail", "detail": "not found"}])
        self.assertFails(self.verify("pre"), "never tried", "m365", "zapier")

    def test_gate_fails_when_all_failed_but_paul_was_never_given_the_question(self):
        self.to_ready()
        self.write("access_log.json", self.access() + [{"need": "bank letter", "route": rt, "tool": "t", "result": "fail", "detail": "x"} for rt in ("device", "m365", "zapier")])
        self.assertFails(self.verify("pre"), "nothing was recorded for Paul")

    def test_receipt_cli_stores_nested_values_booleans_and_stamps(self):
        self.through_build()
        self.ok("receipt", self.run_dir, "--set", "pdf_sent_in_chat=true", "--set", "saved.tool=device_commit_files")
        rc = self.load("receipt.json")
        self.assertIs(rc["pdf_sent_in_chat"], True)
        self.assertEqual(rc["saved"]["tool"], "device_commit_files")
        self.assertEqual(rc["_stamps"]["saved"], self.load("state.json")["build"]["content_sha"])


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
                         "Sam Testcase (Review Client) \u2013 2nd Teams Appointment Completed: 05/10/2026 \u2013 Please see instructions in Client / Prospect Task. Please take note of Follow Up Appt.")

    def test_vague_next_appointment_leaves_the_sentence_out(self):
        self.built(lambda c: c["next_appointment"].update(agreed=False, text="Early next month, date to be set",
                                                           check="Summary says date to be set: a vague intention, not an agreed appointment"))
        self.assertTrue(self.message().endswith("Please see instructions in Client / Prospect Task."))
        self.assertNotIn("Follow Up Appt", self.message())

    def test_a_vague_text_cannot_be_flagged_as_agreed(self):
        self.to_ready()
        c = self.content()
        c["next_appointment"].update(agreed=True, text="We will chat again in February, date to be set")
        self.write("content.json", c)
        self.assertFails(self.verify("pre"), "does not show a specific agreed date/time")

    def test_a_prospect_gets_the_prospect_label_and_the_count_is_a_plain_number(self):
        self.built(lambda c: c.update(client_status="Prospect", client_status_basis="the client's folder sits in Company - Paul\\New Business\\Testcase, Sam", appointment_number=3))
        self.assertIn("Sam Testcase (Prospect) \u2013 3rd Teams Appointment Completed", self.message())

    def test_the_label_is_required_and_must_be_one_of_the_two(self):
        self.to_ready()
        c = self.content()
        c["client_status"] = "Client"
        self.write("content.json", c)
        self.assertFails(self.verify("pre"), 'client_status must be "Review Client" or "Prospect"')
        c = self.content()
        del c["client_status_basis"]
        self.write("content.json", c)
        self.assertFails(self.verify("pre"), "client_status_basis")

    def test_the_label_is_checked_against_where_the_clients_folder_sits(self):
        self.to_ready()
        srcs = self.sources()
        for e in srcs:
            if e.get("read") == "yes":
                e["path"] = "C:\\Users\\Paul\\OneDrive\\Company - WR Clients\\Paul Kafentzis (Client Files)\\Testcase, Sam\\" + e["ref"] + ".pdf"
        self.write("sources.json", srcs)
        c = self.content()
        c.update(client_status="Prospect", client_status_basis="the client is new this month, so a prospect")
        self.write("content.json", c)
        self.assertFails(self.verify("pre"), "client_status is Prospect but the folders read for this client sit where a Review Client's would")
        c.update(client_status="Review Client")
        self.write("content.json", c)
        self.assertEqual(self.verify("pre").returncode, 0, self.verify("pre").stdout)

    def test_appointment_number_must_be_justified_and_valid(self):
        self.to_ready()
        c = self.content()
        c["appointment_number"] = 0
        c["appointment_number_basis"] = "x"
        self.write("content.json", c)
        self.assertFails(self.verify("pre"), "appointment_number must be", "appointment_number_basis")
        c["appointment_number"] = "review"
        c["appointment_number_basis"] = "the label says it is a review, so no number is needed"
        self.write("content.json", c)
        self.assertFails(self.verify("pre"), "appointment_number must be 1, 2, 3")

    def test_appointment_number_cannot_exceed_what_the_file_supports(self):
        self.to_ready()
        c = self.content()
        c["appointment_number"] = 99
        self.write("content.json", c)
        self.assertFails(self.verify("pre"), "is more than the client's file supports")

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
        self.assertFails(self.verify("built"), "teams_message.txt is not what content.json produces")

    def whatsapp_built(self, status="Review Client", number=3):
        self.prep()
        self.read()
        sh("tx.py", "scan", self.run_dir, ok=True)
        c = self.content()
        c.update(meeting_type="whatsapp", meeting_time="14:30", client_status=status, appointment_number=number)
        self.write("content.json", c)
        self.write("ledger.json", self.ledger())
        self.write_support("whatsapp")
        sh("build.py", self.run_dir, ok=True)

    def test_whatsapp_message_says_whatsapp_call_completed(self):
        self.whatsapp_built()
        msg = slurp(self.p("out", "teams_message.txt")).strip()
        self.assertEqual(msg, "Sam Testcase (Review Client) \u2013 3rd WhatsApp Call Completed: 05/10/2026 \u2013 Please see instructions in Client / Prospect Task. Please take note of Follow Up Appt.")
        self.assertNotIn("Teams Appointment", msg)

    def test_whatsapp_message_for_a_prospect_keeps_the_label(self):
        self.whatsapp_built("Prospect", 2)
        self.assertIn("Sam Testcase (Prospect) \u2013 2nd WhatsApp Call Completed:", slurp(self.p("out", "teams_message.txt")))

    def test_a_whatsapp_run_with_the_teams_wording_fails(self):
        self.whatsapp_built()
        spit(self.p("out", "teams_message.txt"), "Sam Testcase (Review Client) \u2013 3rd Teams Appointment Completed: 05/10/2026 \u2013 Please see instructions in Client / Prospect Task.\n")
        self.assertFails(self.verify("built"), "teams_message.txt is not what content.json produces")

    def test_a_teams_meeting_cannot_use_the_whatsapp_wording(self):
        self.built()
        spit(self.p("out", "teams_message.txt"), "Sam Testcase (Review Client) \u2013 1st WhatsApp Call Completed: 05/10/2026 \u2013 Please see instructions in Client / Prospect Task.\n")
        self.assertFails(self.verify("built"), "teams_message.txt is not what content.json produces")

    def test_a_whatsapp_run_reaches_pass_with_the_message_sent(self):
        self.whatsapp_built()
        name = "WhatsApp Call Summary - 05.10.26 - (Testcase, Sam).pdf"
        self.write("run.json", self.run_json("whatsapp"))   # a build re-opens the hand-over steps; the driver then redoes them
        self.write_receipt(self.receipt(name))
        r = self.verify()
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("3rd WhatsApp Call", r.stdout)
        # the final printout carries the skill version, taken from the stamp
        sentence = re.search(r"\*\*Last updated: (\d{4})-(\d{2})-(\d{2}) (\d{2}:\d{2})", slurp(os.path.join(os.path.dirname(SCRIPTS), "SKILL.md")))
        shown = "last updated %s/%s/%s %s (Athens time)" % (sentence.group(3), sentence.group(2), sentence.group(1), sentence.group(4))
        self.assertIn("SKILL VERSION: Using client-teams-transcript-skill, " + shown, r.stdout)
        self.assertIn("Skill version: client-teams-transcript-skill, " + shown + ". Transcript read in full TWICE", r.stdout)

    def test_a_skill_updated_during_the_run_is_flagged(self):
        self.whatsapp_built()
        rj = self.run_json("whatsapp")
        rj["skill_stamp"] = "2020-01-01 00:00"
        self.write("run.json", rj)
        self.write_receipt(self.receipt("WhatsApp Call Summary - 05.10.26 - (Testcase, Sam).pdf"))
        r = self.verify()
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("the skill was updated while this run was in progress (the run started under 01/01/2020 00:00 (Athens time)", r.stdout)

    def test_whatsapp_needs_the_teams_receipt_too(self):
        self.whatsapp_built()
        rc = self.receipt("WhatsApp Call Summary - 05.10.26 - (Testcase, Sam).pdf")
        del rc["teams"]
        self.write_receipt(rc)
        self.assertFails(self.verify(), "teams.status must be sent")

    def receipt_with(self, **teams):
        self.to_built()
        self.write("run.json", self.run_json("followup"))
        rc = self.receipt()
        rc["teams"] = teams
        self.write_receipt(rc)
        return self.verify()

    def test_teams_sent_needs_the_zapier_result_and_pauls_yes(self):
        self.assertFails(self.receipt_with(status="sent", message_id="", sent_time="", approved_by_paul="", body_as_stored=""), "status=sent needs message_id")

    def test_what_zapier_stored_must_be_the_message_that_was_meant(self):
        self.assertFails(self.receipt_with(status="sent", message_id="1730200000001", sent_time="2026-10-29T11:31:00Z", approved_by_paul="yes please",
                                           body_as_stored="<h1><b>Hello Sitamah, a different message entirely, nothing to do with it</b></h1>"),
                         "does not match")

    def test_teams_not_recorded_fails(self):
        self.assertFails(self.receipt_with(), "teams.status must be sent")

    def test_teams_failed_must_hand_the_text_to_paul(self):
        self.assertFails(self.receipt_with(status="failed", detail="Zapier returned 500 on the send"), "text_given_to_paul")
        shutil.rmtree(self.run_dir, ignore_errors=True)
        r = self.receipt_with(status="failed", detail="Zapier returned 500 on the send", text_given_to_paul=True)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("not claimed as sent", r.stdout)

    def test_teams_declined_is_recorded_with_pauls_words(self):
        r = self.receipt_with(status="declined", paul_said="no, I will message her myself")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("I will message her myself", r.stdout)

    def test_already_sent_by_another_skill_needs_evidence(self):
        self.assertFails(self.receipt_with(status="already_sent"), "already_sent_evidence")
        shutil.rmtree(self.run_dir, ignore_errors=True)
        r = self.receipt_with(status="already_sent", already_sent_evidence="fact-find-summary sent it at 10:42 today, message id 1730")
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_planner_page_receipt_rules(self):
        self.to_built()
        self.write("run.json", self.run_json("followup"))
        rc = self.receipt()
        rc["planner_page"] = {"mode": "artifact", "url": "see above"}
        self.write_receipt(rc)
        self.assertFails(self.verify(), "planner_page.url must be the link")
        rc["planner_page"] = {"mode": "fallback_text", "reason": ""}
        self.write_receipt(rc)
        self.assertFails(self.verify(), "the fallback must be stated")
        rc["planner_page"] = {"mode": "fallback_text", "reason": "the Artifact tool is not available in this chat"}
        self.write_receipt(rc)
        r = self.verify()
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("FALLBACK", r.stdout)


class PlannerPage(Base):
    def test_page_has_copy_button_title_and_all_eight_areas(self):
        self.to_ready()
        c = self.content()
        for key, text in (("rgar", "RGAR: the retirement goal analysis was discussed in outline only"),
                          ("egar", "EGAR: the goal analysis is still to be requested"),
                          ("medical", "Medical aid: broker-of-record to move to WR"),
                          ("short_term", "Short-term: vehicle schedule sent to the broker")):
            c["areas"].append({"key": key, "bullets": [{"id": "x_" + key, "text": text, "short": text, "status": "still open",
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

    def test_page_follows_the_page_tools_contract(self):
        """The page tool wraps the file in its own skeleton, so the file must not bring its own, and must theme and gutter as asked."""
        self.to_built()
        page = slurp(self.p("out", "planner_note.html"))
        for banned in ("<!doctype", "<!DOCTYPE", "<html", "<head", "<body"):
            self.assertNotIn(banned, page)
        self.assertLess(page.index("<title>"), 200)
        self.assertIn('<meta name="claude:viewport-fit-sides" content="cover">', page)
        self.assertIn("padding-left:max(16px,env(safe-area-inset-left,0px))", page)
        self.assertIn("padding-right:max(16px,env(safe-area-inset-right,0px))", page)
        self.assertIn("color-scheme:dark", page)
        self.assertIn(":root:not([data-theme=\"light\"])", page)
        self.assertIn("body{margin:0;background:var(--bg)", page)
        for fallback in ("navigator.clipboard.write(", "document.execCommand(\"copy\")", "navigator.clipboard.writeText("):
            self.assertIn(fallback, page)                       # three ways to copy, best first
        self.assertNotIn("https://", page.replace("https://claude.ai", ""))   # nothing is loaded from outside

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
        self.assertFails(self.verify("built"), "planner_note.html is not what content.json produces")

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
