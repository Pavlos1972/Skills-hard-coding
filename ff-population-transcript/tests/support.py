"""Test helpers for ff-population-transcript: runs the REAL programs as a chat would, on invented people only.

`Chat` plays Claude: it does exactly what each step's text tells Claude to do (run.py access / form / formpdf / source / ledger / cross /
claim / receipt ...), so a test can go from `start` to the final printout, or stop at any step and break one thing.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
SCRIPTS = os.environ.get("WR_SCRIPTS") or os.path.join(os.path.dirname(HERE), "scripts")
sys.path.insert(0, SCRIPTS)
REPO = os.path.dirname(os.path.dirname(HERE))
TEAMS_RUN_PY = os.path.join(REPO, "client-teams-transcript-skill", "scripts", "run.py")
FIXTURE = os.path.join(HERE, "fixtures", "transcript_ff.txt")
ENV = dict(os.environ, WR_CHUNK_LINES="25")
CLIENT = ["--client", "Pat Samplecase", "--date", "05/11/2026"]

from fixtures import household as H  # noqa: E402
import teams_driver  # noqa: E402


def spit(path, data):
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)


def slurp(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def jdump(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)


def jload(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def sh(script, *args, env=None, ok=None):
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS, script)] + [str(a) for a in args], capture_output=True, text=True, env=env or ENV)
    if ok is not None:
        assert (r.returncode == 0) == ok, "%s %s -> exit %d\n%s\n%s" % (script, args, r.returncode, r.stdout, r.stderr)
    return r


COMMAND_LOG = []          # every driver command the chat ran, with its exit code (shown in the dry-run report)


def drv(*args, ok=None, env=None):
    r = sh("run.py", *args, ok=ok, env=env)
    COMMAND_LOG.append((" ".join(str(a) for a in args if not str(a).startswith("/tmp/")), r.returncode))
    return r


def comma_money(v):
    """'R 24 000.00' -> 'R24,000.00' (another way of writing the same amount)."""
    import re
    m = re.fullmatch(r"R ([\d ]+)\.(\d\d)", v)
    return v if not m else "R" + format(int(m.group(1).replace(" ", "")), ",") + "." + m.group(2)


def make_form_pdf(path, form, drop=(), reformat=True, extra_lines=()):
    """The form's saved PDF, made from the invented data file: every populated value printed (amounts as R24,000.00 so the format differs)."""
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(path, pagesize=A4)
    y = 800
    lines = ["WR Fact Find v3.0 (invented test client)"]
    for k, cell in form["f"].items():
        if k in drop or k == "pa_actions" or not cell["v"].strip():
            continue
        v = cell["v"].strip()
        if reformat:
            v = comma_money(v)
        lines.append("%s: %s" % (k, v))
    for name, rows in form["l"].items():
        for i, row in enumerate(rows):
            for col, v in row["d"].items():
                if v:
                    lines.append("%s %d %s: %s" % (name, i + 1, col, comma_money(v) if reformat else v))
    lines += list(extra_lines)
    for ln in lines:
        if y < 40:
            c.showPage()
            y = 800
        c.drawString(40, y, ln[:110])
        y -= 13
    c.save()


OVERVIEW = ("WR Overview for Pat Samplecase (invented). BrightRock life cover, premium R 1 100.00 per month. Old Mutual retirement annuity, value R 150 000.00. "
            "Absa home loan. Employer Fakeco Logistics.")
PAYSLIP = "Payslip (invented): Pat Samplecase, Fakeco Logistics, gross R 45 000.00 per month."


class Chat(unittest.TestCase):
    """A test case that can play the whole chat. Subclasses call self.through('<step>') and then break one thing."""

    form_json = None          # override to change the form
    pdf_drop = ()

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="wrff-")
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.run_dir = os.path.join(self.tmp, "run")
        self.form_path = os.path.join(self.tmp, "Fact Find (Audio to Text) - 05.11.2026 - Pat Samplecase.json")
        self.pdf_path = os.path.join(self.tmp, "Fact Find (Audio to Text) - 05.11.2026 - Pat Samplecase.pdf")
        self.form = self.form_json() if callable(self.form_json) else H.pat_form()
        jdump(self.form_path, self.form)
        make_form_pdf(self.pdf_path, self.form, drop=self.pdf_drop)
        self.transcript = FIXTURE

    # ---- plumbing
    def p(self, *a):
        return os.path.join(self.run_dir, *a)

    def ok(self, *args):
        r = drv(*args)
        self.assertEqual(r.returncode, 0, "run.py %s\n%s%s" % (" ".join(map(str, args)), r.stdout, r.stderr))
        return r

    def refused(self, *args, text=None):
        r = drv(*args)
        self.assertNotEqual(r.returncode, 0, "expected a refusal:\n%s%s" % (r.stdout, r.stderr))
        if text:
            self.assertIn(text, r.stdout + r.stderr)
        return r

    def load(self, name):
        return jload(self.p(name))

    def write(self, name, data):
        jdump(self.p(name), data)

    def L(self, text):
        for i, ln in enumerate(slurp(self.p("transcript.txt")).split("\n"), 1):
            if text.lower() in ln.lower():
                return i
        raise AssertionError("fixture text not found: " + text)

    def access(self, need, route="device", result="ok", tool="device_stage_files", detail=""):
        self.ok("access", self.run_dir, "--need", need, "--route", route, "--tool", tool, "--result", result, "--detail", detail)

    # ---- the journey, one step at a time (each does exactly what the step's text says)
    def s_start(self):
        r = self.ok("start", self.run_dir, *CLIENT)
        self.assertIn("SELF-TEST", r.stdout)
        return r

    def s_locate(self):
        for need in ("form", "formpdf", "transcript", "Overview"):
            self.access(need)
        self.ok("done", self.run_dir, "locate")

    def s_form(self):
        self.ok("form", self.run_dir, self.form_path)
        r = self.ok("formpdf", self.run_dir, self.pdf_path)
        for line in r.stdout.splitlines():             # a value the program cannot find in the PDF is looked at and recorded
            if line.strip().startswith("NOT IN THE PDF"):
                key = line.split("(")[-1].split(")")[0]
                self.ok("pdfreview", self.run_dir, "--key", key, "--result", "format_only", "--quote", self.pdf_quote_for(key))
        self.ok("done", self.run_dir, "form")

    def pdf_quote_for(self, key):
        """The words of the form's saved PDF that show this field's value (written differently): the line of the PDF text that holds it."""
        import re
        val = (self.load("form_read.json")["fields"].get(key) or {}).get("v", "")
        digs = re.sub(r"\D", "", val)
        with open(self.p("form_pdf.txt"), encoding="utf-8") as f:
            for ln in f.read().splitlines():
                if (len(digs) >= 2 and digs in re.sub(r"\D", "", ln)) or (len(digs) < 2 and val.lower() in ln.lower()):
                    return ln.strip()
        return "WR Fact Find v3.0"

    def s_prep(self):
        r = sh("tx.py", "prep", self.transcript, self.run_dir)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.ok("done", self.run_dir, "prep")

    def s_documents(self):
        for ref, kind, text in (("WR Overview Pat Samplecase", "Overview", OVERVIEW), ("Payslip Oct 2026", "Other document", PAYSLIP)):
            tf = os.path.join(self.tmp, ref + ".txt")
            spit(tf, text)
            self.ok("source", self.run_dir, "--kind", kind, "--path", "C:\\liferisk.co.za\\Company - Paul\\New Business\\Samplecase, Pat\\1. Overview\\" + ref + ".pdf",
                    "--date", "2026-10-30", "--read", "yes", "--ref", ref, "--text-file", tf)
        self.ok("done", self.run_dir, "documents")

    LEDGER = [   # what the call adds (line text, kind, quote)
        ("cell number is 082", "contact", "your cell number is 082 555 0100"),
        ("one-year diploma", "difference", "I did a one-year diploma after school"),
        ("we move freight", "gap", "we move freight for retailers"),
        ("credit life with Absa", "gap", "there is credit life with Absa on the home loan"),
        ("new business FNA", "quote_request", "ask BrightRock for a new business FNA quote"),
        ("Thursday the twelfth at four works", "next_step", "Thursday the twelfth at four works"),
        ("send us your latest payslip", "next_step", "send us your latest payslip"),
        ("letter of authority", "request", "we also need a letter of authority from you"),
    ]

    def read_pass(self, p_):
        st = self.load("state.json")
        mine = [(self.L(t), k, q) for t, k, q in self.LEDGER]
        for n, (a, b) in enumerate(st["chunks"], 1):
            sh("tx.py", "chunk", self.run_dir, p_, n, ok=True)
            here = [(ln, k, q) for ln, k, q in mine if a <= ln <= b]
            if p_ == 1:
                for ln, k, q in here:
                    self.ok("ledger", self.run_dir, "add", "--line", ln, "--kind", k, "--quote", q)
            if p_ == 2 or not here:
                self.ok("ledger", self.run_dir, "ack", "--pass", p_, "--chunk", n, "--reason", "read this chunk in full again and checked every entry against the words; nothing new to add")

    def s_pass1(self):
        self.read_pass(1)
        self.ok("done", self.run_dir, "pass1")

    def s_pass2(self):
        self.read_pass(2)
        self.ok("done", self.run_dir, "pass2")

    def s_scan(self):
        r = sh("tx.py", "scan", self.run_dir, ok=True)
        for ln in r.stdout.splitlines():
            if " *" in ln[:3] or ln[:2] in ("C*", " *"):
                n = int(ln.split()[1])
                led = self.load("ledger.json")
                if not any(abs(e["line"] - n) <= 3 for e in led["entries"]):
                    self.ok("ledger", self.run_dir, "review", "--line", n, "--reason", "plain talk, nothing decided here")
        self.ok("done", self.run_dir, "scan")

    def s_contact(self):
        self.access("lead", "m365", "ok", "outlook_email_search", "searched Leads - D&R Marketing and the whole mailbox for Pat Samplecase")
        self.ok("lead", self.run_dir, "--folder-result", "none", "--mailbox-result", "none")
        self.ok("done", self.run_dir, "contact")

    def answers(self):
        L = self.L
        return {
            "fname": {"r": "same", "line": L("Your name is Pat Samplecase"), "quote": "Your name is Pat Samplecase"},
            "cell": {"r": "same", "line": L("Correct, 082 555 0100"), "quote": "Correct, 082 555 0100"},
            "edu": {"r": "differs", "line": L("one-year diploma after school"), "quote": "I did a one-year diploma after school", "value": "a one-year diploma"},
            "employer": {"r": "same", "line": L("I work at Fakeco Logistics"), "quote": "I work at Fakeco Logistics"},
            "occ": {"r": "same", "line": L("operations manager"), "quote": "I'm an operations manager"},
            "years": {"r": "same", "line": L("I started in 2015"), "quote": "I started in 2015"},
            "fna_req": {"r": "same", "line": L("new business FNA quote"), "quote": "ask BrightRock for a new business FNA quote"},
            "fna_type": {"r": "same", "line": L("new business FNA quote"), "quote": "for a new business FNA quote"},
            "fna_ins": {"r": "same", "line": L("new business FNA quote"), "quote": "I will ask BrightRock for a new"},
            "loa": {"r": "same", "line": L("letter of authority"), "quote": "we also need a letter of authority from you"},
            "next_appt": {"r": "same", "line": L("Thursday the twelfth at four works"), "quote": "Thursday the twelfth at four works"},
            "next_day": {"r": "same", "line": L("Thursday the twelfth at four works"), "quote": "Thursday the twelfth at four works"},
            "next_time": {"r": "same", "line": L("Thursday the twelfth at four works"), "quote": "Thursday the twelfth at four works"},
        }

    # what the call says about the fields the program leaves for the chat after `cross --rest` (the program found the call mentioning them)
    REST_SAME = {
        "has_kids": ("the children, Sam is in primary school", "And the children, Sam is in primary school"),
        "will": ("Do you have a will", "Do you have a will"),
        "will_where": ("it is with an attorney", "it is with an attorney"),
        "smoker": ("I do not smoke", "I am healthy and I do not smoke"),
        "ret_age": ("At sixty-five", "At sixty-five, and I would need about"),
        "has_risk": ("You have the BrightRock life cover", "You have the BrightRock life cover"),
        "ps_risk": ("You have the BrightRock life cover", "You have the BrightRock life cover"),
        "has_debts": ("credit life with Absa", "there is credit life with Absa on the home loan"),
    }

    def s_crosscheck(self, rest_reason="read the lines the program found for this field; they are about something else, the field itself is not discussed on the call"):
        af = os.path.join(self.tmp, "answers.json")
        have = {i["key"] for i in self.load("crosscheck.json")}
        jdump(af, {k: v for k, v in self.answers().items() if k in have})
        r = self.ok("cross", self.run_dir, "--file", af, "--rest", "not_on_call")
        left = [ln.strip()[2:].split(":")[0].strip() for ln in r.stdout.splitlines() if ln.strip().startswith("- ") and ":" in ln]
        extra = {}
        for k in left:
            if k in self.REST_SAME and self.try_line(self.REST_SAME[k][0]):
                where, quote = self.REST_SAME[k]
                extra[k] = {"r": "same", "line": self.L(where), "quote": quote}
            else:
                extra[k] = {"r": "not_on_call", "reviewed": rest_reason}
        if extra:
            jdump(af, extra)
            self.ok("cross", self.run_dir, "--file", af)
        self.ok("done", self.run_dir, "crosscheck")

    def try_line(self, text):
        try:
            self.L(text)
            return True
        except AssertionError:
            return False

    def s_joint(self):
        self.ok("joint", self.run_dir, "--answer", "no", "--evidence", "Only Pat and Paul spoke on the call; no spouse took part")
        self.ok("done", self.run_dir, "joint")

    def overlay(self):
        L = self.L
        return {
            "fills": [
                {"id": "o1", "key": "debts.0.cl", "value": "Yes", "src": [{"line": L("credit life with Absa"), "quote": "there is credit life with Absa on the home loan"}]},
                {"id": "o6", "key": "cl_req", "value": "Yes", "src": [{"line": L("credit life with Absa"), "quote": "there is credit life with Absa on the home loan"}]},
                {"id": "o7", "key": "cl_lender", "value": "Absa", "src": [{"line": L("credit life with Absa"), "quote": "there is credit life with Absa on the home loan"}]},
            ],
            "notes": [
                {"id": "o2", "section": "medical", "text": "The will has not been updated since before the children were born",
                 "src": [{"line": L("not been updated since before"), "quote": "it has not been updated since before the children were born"}]},
            ],
            "lookup": {"id": "o3", "text": "Moves freight for retailers", "src": [{"line": L("we move freight"), "quote": "we move freight for retailers"}], "client_confirmed": True},
            "documents_to_request": [
                {"id": "o4", "text": "Latest payslip from the client", "src": [{"line": L("send us your latest payslip"), "quote": "send us your latest payslip"}]},
            ],
            "next_steps": [
                {"id": "o5", "text": "Email the latest payslip tomorrow", "src": [{"line": L("I will email it tomorrow"), "quote": "I will email it tomorrow"}]},
            ],
        }

    # fields the search finds call lines for, but whose lines are about something else: each gets its own written reason
    CLAIM_REASONS = {
        "bf_fna_req": "line 66 is the FNA quote already recorded under the FNA quote request; nothing is said about this second (bf) quote",
        "bf_fna_type": "line 66 is the FNA quote already recorded under the FNA quote request; nothing is said about this second (bf) quote type",
        "bf_sf_req": "line 66 is about the FNA quote, no shortfall (group risk) quote is mentioned on the call at all",
        "bf_sf_type": "line 66 is about the FNA quote, no shortfall (group risk) quote is mentioned on the call at all",
        "egar_req": "line 18 is Paul asking about the client's own highest education, not an education goal analysis for the children",
        "h_oth": "lines 60 and 63 only say no conditions and not a smoker; the form's health ticks already say No, no other issue is named",
        "pr_life": "lines 36 and 66 mention the cover and the FNA quote, but the client never ranks any area as his priority",
        "pr_rgar": "line 72 is Paul saying he will ask for the RGAR; the client does not rank it as a priority",
        "pr_will": "line 54 only asks whether there is a will; no priority rank is given for it",
        "cl_bal": "the call says credit life exists with Absa but gives no balance covered by it",
        "cl_life": "the call says credit life exists with Absa but gives no cover amount for it",
    }

    def s_content(self, overlay=None):
        self.ok("compose", self.run_dir)
        r = self.ok("claim", self.run_dir, "--all-empty")
        for key, why in self.CLAIM_REASONS.items():
            if key in r.stdout:
                self.ok("claim", self.run_dir, "--key", key, "--as", "Not discussed", "--reviewed", why)
        self.write("overlay.json", overlay if overlay is not None else self.overlay())
        self.ok("compose", self.run_dir)
        return r

    def cover_all(self):
        """Cover each ledger entry with the kind of item that really can (a fill, an answered field, a request) - the checker refuses anything else."""
        led = self.load("ledger.json")
        by_text = {"cell number is 082": ["cell"], "one-year diploma": ["edu"], "we move freight": ["o3"], "credit life with Absa": ["o1"],
                   "new business FNA": ["fna_req"], "Thursday the twelfth": ["next_appt"], "send us your latest payslip": ["o4"], "letter of authority": ["loa"]}
        for e in led["entries"]:
            for frag, items in by_text.items():
                if frag.lower() in e["quote"].lower():
                    self.ok("ledger", self.run_dir, "cover", e["id"], *items)

    def s_content_done(self):
        self.s_content()
        self.cover_all()
        r = self.ok("done", self.run_dir, "content")
        return r

    def s_build(self):
        r = sh("build.py", self.run_dir)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.ok("done", self.run_dir, "build")
        return r

    def s_check(self):
        self.ok("receipt", self.run_dir, "--set", "png_visual_check=Looked at every page: navy headings, light-blue label column, bullets one per line, red flags readable, nothing cut off",
                "--set", "independent_check=subagent: re-read the transcript against the PDF text; every figure, name and difference matched",
                *["--set", "judgment.not_discussed_rechecked=Re-checked every Not discussed against the form, the call and the Overview",
                  "--set", "judgment.independent_actions_parallel=The FNA request and the payslip request are separate lines",
                  "--set", "judgment.prior_year_current=No prior-year figure is shown as current",
                  "--set", "judgment.garbled_flagged=Nothing garbled on this call, nothing turned into a fact",
                  "--set", "judgment.overview_compared=The Overview premium and fund value match the form",
                  "--set", "judgment.other_documents_checked=The payslip was read; nothing else on file"])
        self.ok("done", self.run_dir, "check")

    def s_pdf(self, listed_size=None, expect_refusal=False, folder="C:\\liferisk.co.za\\Company - Paul\\New Business\\Samplecase, Pat\\2. Fact Find"):
        st = self.load("state.json")
        name, size = st["build"]["pdf"], st["build"]["pdf_size"]
        self.ok("receipt", self.run_dir, "--set", "pdf_sent_in_chat=true", "--set", "saved.tool=device_commit_files", "--set", "saved.folder=" + folder,
                "--set", "saved.filename=" + name, "--set", "saved.tool_result=committed 1 file", "--set", "saved.folder_listing_check=listing shows " + name,
                "--set", "saved.listed_size=%s" % (size if listed_size is None else listed_size))
        if listed_size is not None or expect_refusal:
            return drv("done", self.run_dir, "pdf")           # a wrong listing or folder is refused here
        return self.ok("done", self.run_dir, "pdf")

    def s_handoffs(self, teams_run=None):
        teams_run = teams_run or os.path.join(self.tmp, "teams-run")
        teams_driver.drive(teams_run, self.transcript)
        self.ok("receipt", self.run_dir, "--set", "summary.invoked=fact-find-summary run on the saved PDF: Summary built and saved",
                "--set", "summary.abi_same=Section 8 shows Life Cover (WOL) ABI 3%, Childcare ABI 5%, Household needs ABI 5% and Dread Disease ABI 3%",
                "--set", "teams.run_folder=" + teams_run, "--set", "teams.skill_dir=" + teams_driver.TEAMS_DIR,
                "--set", "teams.next_appointment_carried=Thursday 12/11/2026 at 16:00 (action for Sitamah)")
        self.ok("done", self.run_dir, "handoffs")

    def s_final(self):
        """The last step: the checker's whole printout, then the driver closes the run."""
        return self.ok("done", self.run_dir, "final")

    ORDER = ["start", "locate", "form", "prep", "documents", "pass1", "pass2", "scan", "contact", "crosscheck", "joint", "content", "build", "check", "pdf", "handoffs"]

    def through(self, last):
        """Play the chat up to and including the named step."""
        for name in self.ORDER:
            if name == "content":
                self.s_content_done()
            else:
                getattr(self, "s_" + name)()
            if name == last:
                return
        raise AssertionError("unknown step " + last)

    def verify(self, *extra):
        return sh("verify.py", self.run_dir, *extra)


class Staged(Chat):
    """A Chat whose first part (up to STAGE) is played ONCE for the whole class; each test works on its own copy of that finished state.

    Keeps the regression tests fast: a test breaks one thing at the stage where that thing is done, and asserts the program REFUSES it.
    """
    STAGE = "joint"

    @classmethod
    def setUpClass(cls):
        class Maker(cls):
            def runTest(self):
                pass
        m = Maker()
        Chat.setUp(m)
        m.through(cls.STAGE)
        cls._base = m.tmp

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls._base, True)

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="wrff-")
        shutil.rmtree(self.tmp)
        shutil.copytree(self._base, self.tmp)
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.run_dir = os.path.join(self.tmp, "run")
        self.form_path = os.path.join(self.tmp, "Fact Find (Audio to Text) - 05.11.2026 - Pat Samplecase.json")
        self.pdf_path = os.path.join(self.tmp, "Fact Find (Audio to Text) - 05.11.2026 - Pat Samplecase.pdf")
        self.form = self.form_json() if callable(self.form_json) else H.pat_form()
        self.transcript = FIXTURE

    def fresh_overlay(self, ov=None):
        """Rebuild content from an overlay (the claims already made stay)."""
        self.write("overlay.json", ov if ov is not None else {})
        return drv("compose", self.run_dir)
