"""End-to-end tests for the reading lock, build and delivery gate.

Run:  python3 -m unittest discover -s tests -v      (from the skill folder)

Each negative test starts from a run that passes the whole gate, breaks exactly one
thing, and checks the gate FAILS with the expected message. All people and figures
in the fixture are invented.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))


def spit(path, data, mode="w"):
    with open(path, mode, **({"encoding": "utf-8"} if "b" not in mode else {})) as f:
        f.write(data)


def slurp(path, mode="r"):
    with open(path, mode, **({"encoding": "utf-8"} if "b" not in mode else {})) as f:
        return f.read()


SCRIPTS = os.environ.get("WR_SCRIPTS") or os.path.join(os.path.dirname(HERE), "scripts")
FIXTURE = os.path.join(HERE, "fixtures", "transcript_sample.txt")
ENV = dict(os.environ, WR_CHUNK_LINES="20")
JUDGMENT_KEYS = ("quotes_named", "benefits_from_quote", "nothing_to_confirm_on_file", "independent_actions", "garbled_flagged")
HANDOVER_KEYS = ("planner_page", "pdf_sent_in_chat", "saved", "png_visual_check", "applications_handoff",
                 "independent_check", "judgment", "revised_quote_draft")

# text copies of the (invented) client documents; the figures in the report must come from here or the transcript
DOCS = {
    "Fact Find - Testcase": ("Fact Find", "Fact Find for Sam Testcase. Absa home loan. Lives in Johannesburg."),
    "Fact Find Summary": ("Fact Find Summary", "Fact Find Summary. Absa home loan credit life R500 p.m. (unconfirmed)."),
    "Follow-Up 01.09.26": ("Earlier Note", "Follow-up notes. Will with Capital Legacy in progress."),
    "WR Overview": ("Overview", "WR Overview. Absa home loan. BrightRock Instant Life."),
    "BrightRock quote 100000001": ("Quote", "BrightRock Revised Reduced Quote CP 100000001, R1,100.00 p.m. Instalment protector on the Absa home loan."),
    "OM Optimal RA quote 100000002": ("Quote", "OM Optimal RA Quote 100000002, R3,000 p.m. from 01/11/2026."),
    "Outlook proposal emails": ("Correspondence", "Sam replied to the proposal emails: happy with the proposals."),
}


def sh(script, *args, ok=None):
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS, script)] + [str(a) for a in args],
                       capture_output=True, text=True, env=ENV)
    if ok is not None:
        assert (r.returncode == 0) == ok, "%s %s -> exit %d\n%s\n%s" % (script, args, r.returncode, r.stdout, r.stderr)
    return r


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="wrtest-")
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.run_dir = os.path.join(self.tmp, "run")
        self.source = FIXTURE

    # ---- helpers
    def prep(self, source=None):
        return sh("tx.py", "prep", source or self.source, self.run_dir)

    def read(self, passes=(1, 2)):
        """Read every chunk of the given passes, acknowledging each chunk (the program will not serve the next one otherwise)."""
        k = len(self.load("state.json")["chunks"])
        for p in passes:
            for n in range(1, k + 1):
                sh("tx.py", "chunk", self.run_dir, p, n, ok=True)
                led = self.load("ledger.json") if os.path.exists(self.p("ledger.json")) else {"entries": [], "scan_reviewed": []}
                led.setdefault("chunk_acks", []).append({"pass": p, "chunk": n, "reason": "test: this chunk was read and checked in full", "t": "x"})
                self.write("ledger.json", led)

    def p(self, *a):
        return os.path.join(self.run_dir, *a)

    def L(self, text):
        for i, ln in enumerate(slurp(self.p("transcript.txt")).split("\n"), 1):
            if text in ln:
                return i
        raise AssertionError("fixture text not found: " + text)

    def src(self, quote):
        return {"line": self.L(quote), "quote": quote}

    def doc(self, ref, quote):
        return {"doc": DOCS[ref][0], "ref": ref, "quote": quote}

    def write(self, name, data):
        with open(self.p(name), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load(self, name):
        return json.loads(slurp(self.p(name)))

    def content(self):
        s, d = self.src, self.doc
        return {
            "meeting_type": "followup",
            "client": {"first": "Sam", "surname": "Testcase"},
            "meeting_date": "05/10/2026",
            "topic": "Follow-up appointment: Risk, RA and Tax-Free",
            "appointment_number": 2,
            "client_status": "Review Client",
            "client_status_basis": "the client's folder sits in Company - WR Clients\\Paul Kafentzis (Client Files)\\Testcase, Sam",
            "appointment_number_basis": "Fact Find and one earlier Follow-Up Appointment Summary Notes file are on the client's file",
            "opening": "This follow-up meeting covered the BrightRock quote, the Optimal RA quote and the Tax-Free investment.",
            "since_last": [
                {"id": "s1", "tag": "Changed", "text": "Tax-Free owner changed from Dana to Sam for now",
                 "src": [s("rather put it in my name for now")]},
            ],
            "areas": [
                {"key": "risk", "bullets": [
                    {"id": "b1", "text": "BrightRock Revised Reduced Quote CP 100000001, R1,100.00 p.m.", "status": "ACCEPTED (verbal)",
                     "src": [s("I'm happy to go ahead with the BrightRock one"), s("one thousand one hundred rand a month"),
                             d("BrightRock quote 100000001", "CP 100000001, R1,100.00 p.m.")]},
                    {"id": "b2", "text": "Instalment Protector on the Absa home loan: if retrenched, BrightRock pays the instalment to Absa once the home loan is ceded to Absa",
                     "status": "still open", "src": [s("the home loan must be ceded to Absa for the minimum period")]},
                    {"id": "b3", "text": "Credit life on the Absa home loan (about R500 p.m.) to be cancelled once the BrightRock policy is accepted and in force",
                     "status": "still open", "src": [s("credit life on the Absa home loan costing about five hundred rand a month"),
                                                     d("Fact Find Summary", "Absa home loan credit life R500 p.m.")]},
                ]},
                {"key": "ra", "bullets": [
                    {"id": "b4", "text": "OM Optimal RA Quote 100000002, R3,000 p.m.: the client will get back to us after speaking to his wife",
                     "status": "on hold", "src": [s("Let's leave it for now, I'll get back to you on the RA"),
                                                  d("OM Optimal RA quote 100000002", "OM Optimal RA Quote 100000002, R3,000 p.m.")]},
                ]},
                {"key": "investment", "bullets": [
                    {"id": "b5", "text": "owner now Sam (was Dana), for now", "status": "CHANGED:",
                     "src": [s("rather put it in my name for now")]},
                    {"id": "b6", "text": "Revised Tax-Free quote in Sam's name requested from Alwyn", "status": "awaiting",
                     "src": [s("We need Alwyn to give us a revised quote in your name")]},
                ]},
                {"key": "will", "bullets": [
                    {"id": "b7", "text": "Will: no change discussed on this call", "status": "still open",
                     "src": [d("Follow-Up 01.09.26", "Will with Capital Legacy in progress")]},
                ]},
            ],
            "applications": [],
            "actions": [
                {"id": "a1", "text": "Sitamah to put a review of Dana's portfolio in the what's-next email (Sam answered 'Alright, 100%')",
                 "src": [s("put a review of Dana's portfolio in your what's-next email"), s("Alright, 100%")]},
                {"id": "a2", "text": "Sitamah to arrange for the Absa home loan to be ceded to Absa and send Sam the cession documents to sign",
                 "src": [s("We will send you the cession documents to sign")]},
                {"id": "a3", "text": "Sitamah to get the credit-life details from Sam, ask whether he or WR will cancel it, and cancel only once the BrightRock policy is accepted and in force",
                 "src": [s("We cancel that only once the new policy is accepted and in force")]},
                {"id": "a4", "text": "Sitamah to request the revised Tax-Free quote in Sam's name from Alwyn",
                 "src": [s("We need Alwyn to give us a revised quote in your name")]},
                {"id": "a5", "text": "Sitamah to keep the old Instant Life policy in place until the BrightRock policy is in force",
                 "src": [s("please do not cancel the old Instant Life policy")]},
            ],
            "next_steps": [
                {"id": "n1", "text": "Sam to speak to Dana and come back on the RA",
                 "src": [s("I'll get back to you on the RA once I have spoken to Dana")]},
            ],
            "next_appointment": {"id": "next", "text": "Thu 15/10/2026 at 4pm (RA)", "agreed": True,
                                 "check": "Summary and Planner note both show Thu 15/10/2026 at 4pm: an agreed appointment",
                                 "src": [s("Thursday the fifteenth at four in the afternoon")]},
            "checks": {
                "correspondence": {"done": True, "looked_at": "Outlook: Sam's replies to the proposal emails and the BrightRock quote email"},
                "owner_change": {"occurred": True, "action_id": "a4"},
                "cession": {"needed": True, "action_id": "a2"},
                "credit_life": {"debts_protected": True, "debts": [{"lender": "Absa", "credit_life": "yes"}],
                                "bullet_id": "b3", "action_ids": ["a3"]},
                "applications": {"exist": False},
                "quotes_matched": True,
            },
        }

    def ledger(self):
        def e(i, kind, q, cov=None, **kw):
            return dict(id=i, kind=kind, line=self.L(q), quote=q, covered_by=cov or [], **kw)
        entries = [
            e("L1", "acceptance", "I'm happy to go ahead with the BrightRock one", ["b1"], pass_=1),
            e("L2", "figure", "one thousand one hundred rand a month", ["b1"], pass_=1),
            e("L3", "instruction", "the home loan must be ceded to Absa for the minimum period", ["b2", "a2"], pass_=1),
            e("L4", "fact", "credit life on the Absa home loan costing about five hundred rand a month", ["b3", "a3"], pass_=1),
            e("L5", "hold", "Let's leave it for now, I'll get back to you on the RA", ["b4", "n1"], pass_=1),
            e("L6", "change", "rather put it in my name for now", ["b5", "s1"], pass_=1),
            e("L7", "instruction", "We need Alwyn to give us a revised quote in your name", ["b6", "a4"], pass_=1),
            e("L8", "decision", "Thursday the fifteenth at four in the afternoon", ["next"], pass_=1),
            e("L9", "request", "put a review of Dana's portfolio in your what's-next email", ["a1"], pass_=1),
            e("L10", "offer", "I'll offer that and we can look at her portfolio", ["a1"], pass_=1),
            e("L11", "acceptance", "Alright, 100%", ["a1"], pass_=1),
            e("L12", "instruction", "please do not cancel the old Instant Life policy", ["a5"], pass_=1),
            e("L13", "fact", "I've got a medical condition that I know of", None, pass_=2,
              excluded="garbled line: could mean he has or has no known condition; flagged to Paul, left out"),
        ]
        for x in entries:
            x["pass"] = x.pop("pass_")
        return {"entries": entries, "scan_reviewed": [], "chunk_acks": self.acks()}

    def acks(self):
        k = len(self.load("state.json")["chunks"]) if os.path.exists(self.p("state.json")) else 4
        return [{"pass": p, "chunk": c, "reason": "test: this chunk was read and checked in full", "t": "x"} for p in (1, 2) for c in range(1, k + 1)]

    def sources(self):
        out = []
        for ref, (kind, _) in DOCS.items():
            out.append({"kind": kind, "path": "C:\\Clients\\Testcase, Sam\\" + ref + ".pdf", "date": "2026-10-01", "read": "yes", "ref": ref, "text": True})
        out.append({"kind": "Application", "none": "searched the Applications folder of both current transactions: none on file yet"})
        return out

    def access(self):
        acc = [{"need": "transcript", "route": "device", "tool": "device_stage_files", "result": "ok", "detail": ""}]
        acc += [{"need": "Application", "route": r, "tool": "t_" + r, "result": "fail", "detail": "nothing found"} for r in ("device", "m365")]
        return acc

    def run_json(self, mt="followup", done=None):
        steps = json.loads(slurp(os.path.join(os.path.dirname(SCRIPTS), "steps.json")))["steps"]
        mine = [s["id"] for s in steps if mt in s["applies"] and s["id"] != "final"]
        return {"skill": "client-teams-transcript-skill", "meeting_type": mt, "client": {"first": "Sam", "surname": "Testcase"},
                "date": "05/10/2026", "steps": {sid: {"state": "done"} for sid in (mine if done is None else done)}}

    def teams_text(self):
        p = self.p("out", "teams_message.txt")
        return slurp(p).strip() if os.path.exists(p) else ""

    def receipt(self, name=None):
        name = name or "Follow-Up Appointment Summary Notes - 05.10.26 - (Testcase, Sam).pdf"
        return {
            "planner_page": {"mode": "artifact", "url": "https://claude.ai/artifact/test-page"},
            "teams": {"status": "sent", "message_id": "1730200000000", "sent_time": "2026-10-29T11:30:00Z",
                      "approved_by_paul": "yes, send it", "body_as_stored": "<h1><b>%s</b></h1>" % self.teams_text()},
            "pdf_sent_in_chat": True,
            "saved": {"tool": "device_commit_files", "folder": "C:\\Clients\\Testcase, Sam\\2. Fact Find",
                      "filename": name, "tool_result": "committed 1 file",
                      "folder_listing_check": "Listing of 2. Fact Find: Fact Find - Testcase.pdf; %s" % name},
            "png_visual_check": "Page 1: navy title, grey subtitle, bold navy headings, bulleted points; page 2 matches.",
            "applications_handoff": "n/a: no applications exist for this client",
            "independent_check": "subagent: re-read the transcript against the outputs; every figure, name and status matched",
            "judgment": {k: "Checked, nothing to change: " + k.replace("_", " ") for k in JUDGMENT_KEYS},
            "revised_quote_draft": "shown to Paul: revised Tax-Free quote request to Alwyn, draft only, not sent",
        }

    def write_receipt(self, rc):
        """Receipts belong to the build they were recorded for (the program stamps them the same way)."""
        sha = self.load("state.json")["build"]["content_sha"]
        rc["_stamps"] = {k: sha for k in HANDOVER_KEYS if k in rc}
        self.write("receipt.json", rc)

    def to_ready(self, content=None, ledger=None):
        """Prep, read twice (acknowledging each chunk), scan, and write ledger, content, logs and documents (not built yet)."""
        self.prep()
        self.read()
        sh("tx.py", "scan", self.run_dir, ok=True)
        self.write("content.json", content or self.content())
        self.write("ledger.json", ledger or self.ledger())
        self.write_support()

    def write_support(self, mt="followup"):
        self.write("sources.json", self.sources())
        self.write("access_log.json", self.access())
        self.write("questions.json", [])
        os.makedirs(self.p("docs"), exist_ok=True)
        for ref, (_, text) in DOCS.items():
            spit(self.p("docs", ref + ".txt"), text)
        self.write("run.json", self.run_json(mt))

    def to_built(self, **kw):
        self.to_ready(**kw)
        sh("build.py", self.run_dir, ok=True)

    def to_final(self):
        self.to_built()
        self.write("run.json", self.run_json(self.load("content.json")["meeting_type"]))   # a build re-opens the hand-over steps; the driver then redoes them
        self.write_receipt(self.receipt())

    def verify(self, stage="final"):
        return sh("verify.py", self.run_dir, "--stage", stage)

    def assertFails(self, res, *needles):
        self.assertNotEqual(res.returncode, 0, res.stdout)
        for n in needles:
            self.assertIn(n, res.stdout)

    def mutate_content(self, fn, stage="pre"):
        self.to_ready()
        c = self.content()
        fn(c)
        self.write("content.json", c)
        return self.verify(stage)


class ReadingLock(Base):
    def test_pass2_refused_before_pass1(self):
        self.prep()
        r = sh("tx.py", "chunk", self.run_dir, 2, 1)
        self.assertEqual(r.returncode, 3)
        self.assertIn("Pass 2 cannot start", r.stderr)

    def test_skipping_a_chunk_is_refused(self):
        self.prep()
        r = sh("tx.py", "chunk", self.run_dir, 1, 3)
        self.assertEqual(r.returncode, 3)
        self.assertIn("none skipped", r.stderr)

    def test_next_chunk_is_refused_until_the_last_one_is_acknowledged(self):
        self.prep()
        sh("tx.py", "chunk", self.run_dir, 1, 1, ok=True)
        r = sh("tx.py", "chunk", self.run_dir, 1, 2)
        self.assertEqual(r.returncode, 3)
        self.assertIn("has no ledger entry and no acknowledgement", r.stderr)

    def test_scan_refused_until_both_passes(self):
        self.prep()
        self.read(passes=(1,))
        self.assertEqual(sh("tx.py", "scan", self.run_dir).returncode, 3)

    def test_build_refused_after_pass1_only(self):
        self.prep()
        self.read(passes=(1,))
        self.write("content.json", self.content())
        self.write("ledger.json", self.ledger())
        self.write_support()
        r = sh("build.py", self.run_dir)
        self.assertFails(r, "Pass 2 has NOT served every chunk", "BUILD REFUSED")
        self.assertFalse(os.path.exists(self.p("out")))

    def test_incomplete_transcript_stops(self):
        src = os.path.join(self.tmp, "short.txt")
        spit(src, slurp(FIXTURE).replace("Duration: 12m 40s", "Duration: 40m 0s"))
        r = self.prep(src)
        self.assertEqual(r.returncode, 2)
        self.assertIn("INCOMPLETE", r.stdout)
        self.assertEqual(sh("tx.py", "chunk", self.run_dir, 1, 1).returncode, 2)

    def test_gap_in_transcript_stops(self):
        src = os.path.join(self.tmp, "gap.txt")
        spit(src, slurp(FIXTURE).replace("0:05:15 Paul", "0:25:15 Paul"))
        r = self.prep(src)
        self.assertEqual(r.returncode, 2)
        self.assertIn("GAP", r.stdout)

    def test_force_is_recorded_and_warned(self):
        src = os.path.join(self.tmp, "short.txt")
        spit(src, slurp(FIXTURE).replace("Duration: 12m 40s", "Duration: 40m 0s"))
        sh("tx.py", "prep", src, self.run_dir, "--force", ok=True)
        self.assertTrue(self.load("state.json")["forced"])

    def test_no_stated_duration_and_no_closing_marker_cannot_be_checked(self):
        src = os.path.join(self.tmp, "nodur.txt")
        text = slurp(FIXTURE).replace("Duration: 12m 40s\n", "").replace("0:12:30 Paul Kafentzis stopped transcription", "0:12:30 Paul Kafentzis")
        spit(src, text)
        r = self.prep(src)
        self.assertEqual(r.returncode, 2)
        self.assertIn("states no total duration and has no closing marker", r.stdout)


class HappyPath(Base):
    def test_full_run_passes_every_stage(self):
        self.to_final()
        for stage in ("pre", "built", "final"):
            r = self.verify(stage)
            self.assertEqual(r.returncode, 0, r.stdout)
        out = self.verify().stdout
        self.assertIn("RESULT: PASS", out)
        self.assertIn("Transcript read in full TWICE", out)
        self.assertIn("WHAT PAUL SHOULD GLANCE AT", out)
        self.assertIn("ATTEST", out)

    def test_pdf_is_named_from_the_fields_and_both_outputs_agree(self):
        self.to_built()
        names = os.listdir(self.p("out"))
        self.assertIn("Follow-Up Appointment Summary Notes - 05.10.26 - (Testcase, Sam).pdf", names)
        self.assertIn("planner_note.txt", names)
        self.assertTrue(any(n.startswith("page") and n.endswith(".png") for n in names))
        note = slurp(self.p("out", "planner_note.txt"))
        self.assertNotIn("```", note)
        self.assertIn("**Sam Testcase \u2013 05/10/2026**", note)
        self.assertIn("**CHANGED:** owner now Sam", note)
        self.assertIn("Will: no change discussed", note)
        pdf = [n for n in names if n.endswith(".pdf")][0]
        text = subprocess.run(["pdftotext", self.p("out", pdf), "-"], capture_output=True, text=True).stdout
        for needle in ("Since the Last Meeting", "Risk", "RA", "Investment", "Not discussed this meeting: RGAR, EGAR, Medical Aid, Short-Term", "Action Points", "Next Steps", "Sitamah to arrange for the Absa home loan"):
            self.assertIn(needle, text)

    def test_first_meeting_has_note_but_no_pdf(self):
        self.prep()
        self.read()
        sh("tx.py", "scan", self.run_dir, ok=True)
        c = self.content()
        c["meeting_type"] = "first"
        c["since_last"] = []
        c["appointment_number"] = 1
        c["checks"]["correspondence"] = {"done": False, "reason": "first meeting: no proposal emails exist yet"}
        c["checks"]["quotes_matched"] = "n/a: first meeting, nothing quoted yet"
        led = self.ledger()
        for e in led["entries"]:
            e["covered_by"] = [x for x in e["covered_by"] if x != "s1"]
        self.write("content.json", c)
        self.write("ledger.json", led)
        self.write_support("first")
        sh("build.py", self.run_dir, ok=True)
        self.assertEqual([f for f in os.listdir(self.p("out")) if f.endswith(".pdf")], [])
        self.assertIn("Fact Find Summary - 05.10.26 - (Sam Testcase)", slurp(self.p("out", "planner_note.txt")))
        r = self.verify("built")
        self.assertEqual(r.returncode, 0, r.stdout)
        spit(self.p("out", "Follow-Up Appointment Summary Notes - 05.10.26 - (Testcase, Sam).pdf"), b"%PDF-1.4", "wb")
        self.assertFails(self.verify("built"), "must not produce a Follow-Up PDF")

    def test_whatsapp_variant_filename_and_note(self):
        self.prep()
        self.read()
        sh("tx.py", "scan", self.run_dir, ok=True)
        c = self.content()
        c["meeting_type"], c["meeting_time"] = "whatsapp", "14:30"
        self.write("content.json", c)
        self.write("ledger.json", self.ledger())
        self.write_support("whatsapp")
        sh("build.py", self.run_dir, ok=True)
        self.assertIn("WhatsApp Call Summary - 05.10.26 - (Testcase, Sam).pdf", os.listdir(self.p("out")))
        self.assertIn("*WhatsApp call, 14:30: Follow-up appointment", slurp(self.p("out", "planner_note.txt")))


class SourceTrace(Base):
    def test_fabricated_quote_fails(self):
        r = self.mutate_content(lambda c: c["areas"][0]["bullets"][0]["src"].append({"line": 10, "quote": "I have no medical conditions at all"}))
        self.assertFails(r, "source quote not found")

    def test_item_without_source_fails(self):
        r = self.mutate_content(lambda c: c["actions"][0].update(src=[]))
        self.assertFails(r, "has no source")

    def test_action_must_start_with_sitamah(self):
        r = self.mutate_content(lambda c: c["actions"][1].update(text="Paul to arrange the cession of the Absa home loan"))
        self.assertFails(r, "must start 'Sitamah to '", "names Paul")

    def test_asking_paul_to_approve_is_not_paul_owning_the_action(self):
        r = self.mutate_content(lambda c: c["actions"].append(
            {"id": "a9", "text": "Sitamah to ask Paul to approve the draft email before it goes out",
             "src": [self.src("put a review of Dana's portfolio in your what's-next email")]}))
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_chase_action_for_item_left_with_client_fails(self):
        def f(c):
            c["actions"].append({"id": "a9", "text": "Sitamah to chase Sam for his answer on the RA",
                                 "src": [self.src("Let's leave it for now, I'll get back to you on the RA")]})
        self.assertFails(self.mutate_content(f), "not a chase action")

    def test_wrong_document_source_shape_fails(self):
        r = self.mutate_content(lambda c: c["areas"][3]["bullets"][0].update(src=[{"doc": "Gossip", "ref": "x", "quote": "something here"}]))
        self.assertFails(r, "a document source needs")

    def test_document_quote_is_checked_against_the_recorded_text(self):
        self.to_ready()
        self.assertEqual(self.verify("pre").returncode, 0)
        spit(self.p("docs", "Follow-Up 01.09.26.txt"), "Something else entirely.")
        self.assertFails(self.verify("pre"), "quote not found in document")

    def test_a_document_that_was_never_recorded_as_read_fails(self):
        r = self.mutate_content(lambda c: c["areas"][3]["bullets"][0].update(
            src=[{"doc": "Overview", "ref": "zzz", "quote": "anything goes here"}]))
        self.assertFails(r, "was never recorded as read")

    def test_a_document_called_the_wrong_kind_fails(self):
        r = self.mutate_content(lambda c: c["areas"][3]["bullets"][0].update(
            src=[{"doc": "Overview", "ref": "Follow-Up 01.09.26", "quote": "Will with Capital Legacy in progress"}]))
        self.assertFails(r, "was recorded as a Earlier Note")

    def test_thirteen_digit_number_fails(self):
        r = self.mutate_content(lambda c: c["areas"][0]["bullets"][0].update(text="BrightRock quote for ID 8001015009087"))
        self.assertFails(r, "13-digit number")

    def test_non_winansi_character_fails(self):
        r = self.mutate_content(lambda c: c["areas"][0]["bullets"][0].update(text="Premium \u2192 R1,100 p.m."))
        self.assertFails(r, "outside WinAnsi")

    def test_dependent_wording_is_warned_not_failed(self):
        r = self.mutate_content(lambda c: c["actions"][3].update(text="Sitamah to request the revised quote once the report is received"))
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("worded as dependent", r.stdout)


class LedgerCoverage(Base):
    def mutate_ledger(self, fn, stage="pre"):
        self.to_ready()
        led = self.ledger()
        fn(led)
        self.write("ledger.json", led)
        return self.verify(stage)

    def test_uncovered_request_fails(self):
        r = self.mutate_ledger(lambda l: l["entries"][8].update(covered_by=[]))
        self.assertFails(r, "is not covered by any bullet or action")

    def test_ledger_quote_not_in_transcript_fails(self):
        r = self.mutate_ledger(lambda l: l["entries"][0].update(quote="I would like to decline everything"))
        self.assertFails(r, "quote not found at line")

    def test_covered_by_unknown_item_fails(self):
        r = self.mutate_ledger(lambda l: l["entries"][0].update(covered_by=["zzz"]))
        self.assertFails(r, "do not exist in content.json")

    def test_change_must_be_marked_changed(self):
        r = self.mutate_ledger(lambda l: l["entries"][5].update(covered_by=["b6"]))
        self.assertFails(r, "not recorded as CHANGED")

    def test_hold_cannot_be_only_a_task(self):
        r = self.mutate_ledger(lambda l: l["entries"][4].update(covered_by=["a5"]))
        self.assertFails(r, "reported as on hold, not as tasks")

    def test_empty_ledger_fails(self):
        self.assertFails(self.mutate_ledger(lambda l: l.update(entries=[])), "ledger.json has no entries")

    def test_unreasoned_exclusion_fails(self):
        r = self.mutate_ledger(lambda l: l["entries"][12].update(excluded=""))
        self.assertFails(r, "neither covered nor excluded")

    def test_unrelated_item_cannot_cover_a_request(self):
        # the spouse-portfolio request "covered" by the Will bullet: nothing in it cites that part of the call
        r = self.mutate_ledger(lambda l: l["entries"][8].update(covered_by=["b7"]))
        self.assertFails(r, "cites the transcript within", "not about the same thing")

    def test_a_chunk_without_entries_or_acknowledgement_fails(self):
        def f(l):
            l["chunk_acks"] = [a for a in l["chunk_acks"] if not (a["pass"] == 2 and a["chunk"] == 1)]
        self.assertFails(self.mutate_ledger(f), "chunks read without a ledger entry or acknowledgement", "(2, 1)")

    def test_unresolved_keyword_hit_anywhere_fails_not_just_in_the_closing_minutes(self):
        def f(l):
            l["entries"] = [e for e in l["entries"] if e["id"] not in ("L7", "L6", "L5")]
        r = self.mutate_ledger(f)
        self.assertFails(r, "keyword hits are not covered by a ledger entry within 3 lines or a recorded review")

    def test_closing_minutes_keyword_hit_must_be_covered(self):
        def f(l):
            l["entries"] = [e for e in l["entries"] if e["id"] not in ("L11", "L12", "L9", "L10")]
        r = self.mutate_ledger(f)
        self.assertFails(r, "keyword hits are not covered", "in the closing minutes")

    def test_a_reasoned_review_resolves_hits(self):
        self.to_ready()
        led = self.ledger()
        led["entries"] = [e for e in led["entries"] if e["id"] not in ("L11", "L12", "L9", "L10")]
        led["scan_reviewed"] = [{"from": 1, "to": 68, "reason": "the whole call reviewed in this test"}]
        self.write("ledger.json", led)
        self.assertNotIn("keyword hits are not covered", self.verify("pre").stdout)


class MandatoryChecks(Base):
    def drop(self, key):
        return self.mutate_content(lambda c: c["checks"].pop(key))

    def test_credit_life_must_always_be_answered(self):
        self.assertFails(self.drop("credit_life"), "checks.credit_life missing")

    def test_each_declared_check_is_required(self):
        for key, needle in (("correspondence", "checks.correspondence missing"), ("owner_change", "checks.owner_change missing"),
                            ("cession", "checks.cession missing"), ("applications", "checks.applications missing"),
                            ("quotes_matched", "checks.quotes_matched")):
            with self.subTest(key=key):
                shutil.rmtree(self.run_dir, ignore_errors=True)
                self.assertFails(self.drop(key), needle)

    def test_no_checks_block_fails(self):
        self.assertFails(self.mutate_content(lambda c: c.pop("checks")), "no `checks` block")

    def test_cession_declared_but_no_cession_action_fails(self):
        r = self.mutate_content(lambda c: c["actions"][1].update(text="Sitamah to send Sam the Absa documents to sign"))
        self.assertFails(r, "cession needed")

    def test_the_word_advanced_is_not_a_cession(self):
        r = self.mutate_content(lambda c: c["actions"][1].update(text="Sitamah to send Sam the advanced notice documents to sign"))
        self.assertFails(r, "cession needed")

    def test_owner_change_without_revised_quote_action_fails(self):
        r = self.mutate_content(lambda c: c["actions"][3].update(text="Sitamah to email Alwyn about Sam"))
        self.assertFails(r, "revised quote")

    def test_owner_change_declared_false_while_an_owner_is_marked_changed_fails(self):
        r = self.mutate_content(lambda c: c["checks"].update(owner_change={"occurred": False}))
        self.assertFails(r, "owner_change.occurred is false")

    def test_credit_life_declared_without_in_force_condition_fails(self):
        r = self.mutate_content(lambda c: c["actions"][2].update(text="Sitamah to cancel the credit life on the Absa home loan"))
        self.assertFails(r, "in force")

    def test_credit_life_needs_all_three_actions(self):
        r = self.mutate_content(lambda c: c["actions"][2].update(text="Sitamah to cancel the credit life only once the BrightRock policy is accepted and in force"))
        self.assertFails(r, "(a) get the credit-life details", "(b) ask the client")

    def test_credit_life_not_applicable_needs_a_reason(self):
        r = self.mutate_content(lambda c: c["checks"].update(credit_life={"debts_protected": False}))
        self.assertFails(r, "give the reason")

    def test_credit_life_declared_not_applicable_while_the_report_mentions_it_fails(self):
        r = self.mutate_content(lambda c: c["checks"].update(credit_life={"debts_protected": False, "reason": "no debt protected by this cover at all"}))
        self.assertFails(r, "mentions credit life")

    def test_correspondence_skipped_after_first_meeting_fails(self):
        r = self.mutate_content(lambda c: c["checks"].update(correspondence={"done": False, "reason": "did not get to it today"}))
        self.assertFails(r, "only allowed at a first meeting")

    def test_empty_carry_forward_needs_a_reason(self):
        r = self.mutate_content(lambda c: c.update(since_last=[]))
        self.assertFails(r, "since_last is empty")


class OutputsAndReceipt(Base):
    def test_content_edited_after_build_is_stale(self):
        self.to_final()
        c = self.content()
        c["actions"][3]["text"] = "Sitamah to request the revised Tax-Free quote from Alwyn today"
        self.write("content.json", c)
        self.assertFails(self.verify(), "content.json changed after the outputs were built")
        sh("build.py", self.run_dir, ok=True)           # rebuild re-opens the hand-over
        self.assertFails(self.verify(), "hand-over receipts recorded for an older build", "steps not completed through the driver")
        self.write("run.json", self.run_json("followup"))
        self.write_receipt(self.receipt())
        r = self.verify()
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_deleted_pdf_fails(self):
        self.to_final()
        for f in os.listdir(self.p("out")):
            if f.endswith(".pdf"):
                os.remove(self.p("out", f))
        self.assertFails(self.verify("built"), "PDF missing")

    def test_replaced_pdf_fails(self):
        self.to_final()
        pdf = [f for f in os.listdir(self.p("out")) if f.endswith(".pdf")][0]
        shutil.copy(os.path.join(SCRIPTS, "wrlib.py"), self.p("out", pdf))
        self.assertFails(self.verify("built"), "no extractable text")

    def test_a_pdf_with_other_text_fails_even_if_the_stored_hash_is_patched(self):
        self.to_final()
        pdf = [f for f in os.listdir(self.p("out")) if f.endswith(".pdf")][0]
        from reportlab.pdfgen import canvas
        c = canvas.Canvas(self.p("out", pdf))
        c.drawString(72, 700, "Sitamah to do something else entirely")
        c.save()
        st = self.load("state.json")
        st["build"]["pdf_sha"] = "0" * 64                       # patching the stored hash must not help
        self.write("state.json", st)
        self.assertFails(self.verify("built"), "PDF text is not what content.json produces")

    def test_hand_edited_planner_text_fails_even_if_the_hash_is_patched(self):
        self.to_final()
        with open(self.p("out", "planner_note.txt"), "a", encoding="utf-8") as f:
            f.write("\nSomething Claude typed by hand\n")
        st = self.load("state.json")
        st["build"]["files"]["planner_note.txt"] = "x"
        self.write("state.json", st)
        self.assertFails(self.verify("built"), "planner_note.txt is not what content.json produces")

    def test_missing_page_images_fail(self):
        self.to_final()
        for f in os.listdir(self.p("out")):
            if f.endswith(".png"):
                os.remove(self.p("out", f))
        self.assertFails(self.verify("built"), "page images")

    def test_missing_receipt_fails(self):
        self.to_built()
        self.assertFails(self.verify(), "receipt.json missing", "NOT COMPLETE")

    def test_receipt_with_wrong_filename_fails(self):
        self.to_built()
        self.write_receipt(self.receipt(name="Summary.pdf"))
        self.assertFails(self.verify(), "is not the expected")

    def test_receipt_without_folder_listing_fails(self):
        self.to_built()
        r = self.receipt()
        r["saved"]["folder_listing_check"] = ""
        self.write_receipt(r)
        self.assertFails(self.verify(), "must all be filled")

    def test_receipt_not_sent_in_chat_fails(self):
        self.to_built()
        r = self.receipt()
        r["pdf_sent_in_chat"] = False
        self.write_receipt(r)
        self.assertFails(self.verify(), "must be sent in the chat")

    def test_many_bullets_do_not_strand_a_heading(self):
        self.to_ready()
        c = self.content()
        for i in range(22):
            c["areas"][0]["bullets"].append({"id": "x%d" % i, "text": "Extra risk point number with some words to fill the line (%d)" % i,
                                             "status": "still open", "src": [self.src("one thousand one hundred rand a month")]})
        self.write("content.json", c)
        sh("build.py", self.run_dir, ok=True)
        r = self.verify("built")
        self.assertEqual(r.returncode, 0, r.stdout)


if __name__ == "__main__":
    unittest.main()
