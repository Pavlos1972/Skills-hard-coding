"""The ONE test of the prospect-review-funnel-at-knowledge (Operation Skill Restructure: one end-to-end test on invented data).

It plays whole jobs through the program exactly as a chat would, on invented documents (tests/sample.py). Nothing is sent or changed anywhere: the document
changes and the AdviceTech read-backs are typed in, as a chat would copy them. It proves:
  1. the driver refuses to skip a step, refuses a route that was not logged or tried out of order, and makes the pages be read in order;
  2. a quoted line that is not in the document, is too short or was already used for another stage is refused; a stage without both lines is not done;
  3. a plan is refused, each for its own reason: Charl's checklist, SR and PK lines mixed, a line with no owner, a wrong AUTOMATION ending, "Claude" in a name,
     a wrong line count, a Section name with no owner, a stage that was not named, a document that was not located;
  4. nothing is changed before Paul's yes; a plan changed after his yes loses it; documents come first (before the first read-back, after the yes), and a document
     changed late or not in this run is caught; a read-back with the wrong line count is caught; the audit ends in green ticks and the items table;
  5. a question is answered only with every stage's code, owner and route as the funnel data holds them, and a stage that does not exist is refused;
  6. a document edit with no stage runs without AdviceTech objects; the stage routes, the pages and the line rules are checked on invented defects.
"""
import copy
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
import funnel as F  # noqa: E402

ENV = dict(os.environ, WR_TODAY="05/11/2026", WR_NOW="10:15")


def run(script, *args, expect=0):
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS, script)] + list(args), capture_output=True, text=True, encoding="utf-8", env=ENV)
    if expect == "refused":
        assert r.returncode != 0, "%s %s should have been refused\n%s" % (script, args, r.stdout[-1500:])
    else:
        assert r.returncode == expect, "%s %s -> exit %d (wanted %d)\n%s\n%s" % (script, args, r.returncode, expect, r.stdout[-2500:], r.stderr[-1200:])
    return r.stdout + r.stderr


def jwrite(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


class Journey(unittest.TestCase):
    def test_journey(self):
        with tempfile.TemporaryDirectory() as d:
            self.docs = sample.write_docs(d)
            self.model_checks(d)
            self.build_run(d)
            self.docs_first_run(d)
            self.question_run(d)
            self.docs_run(d)

    # ------------------------------------------------------------------ helpers
    def register(self, R, roles, route="device"):
        for r in roles:
            run("run.py", "access", R, "--purpose", r, "--route", route, "--result", "found")
            run("run.py", "doc", R, "--role", r, "--file", self.docs[r], "--route", route, "--modified", "2026-11-04 16:00")

    def read_pages(self, R):
        out = run("run.py", "read", R)
        n = int(re.search(r"PAGE 1 of (\d+)", out).group(1))
        for i in range(1, n + 1):
            run("run.py", "read", R, "--ack", str(i), "--note", "read page %d" % i)
        return n

    def quote(self, R, codes):
        for c in codes:
            for doc in ("streamlined", "master_plan"):
                run("run.py", "evidence", R, "--stage", c, "--doc", doc, "--line", sample.EV[(c, doc)])

    def to_plan(self, d, name, kind="build", codes=("A6d", "G5b"), roles=("streamlined", "master_plan", "register")):
        R = os.path.join(d, name)
        run("run.py", "start", R, "--kind", kind, "--request", "Please add the monitor line to G5b and the servicing question to A6d")
        self.register(R, roles)
        run("run.py", "done", R, "locate")
        run("run.py", "stages", R, "--codes", ",".join(codes))
        run("run.py", "done", R, "stages")
        self.read_pages(R)
        run("run.py", "done", R, "read")
        self.quote(R, codes)
        run("run.py", "done", R, "proof")
        return R

    # ------------------------------------------------------------------ the full build
    def build_run(self, d):
        R = os.path.join(d, "run0")
        out = run("run.py", "start", R, "--kind", "build", "--request", "Please add the monitor line to G5b and the servicing question to A6d")
        self.assertIn("Using prospect-review-funnel-at-knowledge, last updated", out)
        self.assertIn("STEP 1 of 8", out)
        self.assertIn("DOCUMENTS THIS WORK NEEDS", out)
        run("run.py", "done", R, "stages", expect="refused")                      # steps cannot be skipped
        run("run.py", "done", R, "locate", expect="refused")                      # nothing registered yet
        # routes: a document by a route that was never logged is refused; Microsoft 365 before the computer failed is refused (in a run of its own: the log keeps the mistake)
        Ra = os.path.join(d, "run0a")
        run("run.py", "start", Ra, "--kind", "build", "--request", "Please add the monitor line to G5b")
        run("run.py", "doc", Ra, "--role", "streamlined", "--file", self.docs["streamlined"], "--route", "m365", "--modified", "2026-11-04 16:00", expect="refused")
        run("run.py", "access", Ra, "--purpose", "streamlined", "--route", "m365", "--result", "found")
        self.assertIn("tried in order", run("run.py", "doc", Ra, "--role", "streamlined", "--file", self.docs["streamlined"], "--route", "m365", "--modified", "2026-11-04 16:00", expect="refused"))
        run("run.py", "access", R, "--purpose", "master_plan", "--route", "device", "--result", "failed")
        run("run.py", "access", R, "--purpose", "master_plan", "--route", "m365", "--result", "found")
        run("run.py", "doc", R, "--role", "master_plan", "--file", self.docs["master_plan"], "--route", "m365", "--modified", "2026-11-04 16:00")
        run("run.py", "doc", R, "--role", "register", "--file", self.docs["register"], "--route", "pasted", "--modified", "not a time", expect="refused")
        out = run("run.py", "doc", R, "--role", "register", "--file", self.docs["register"], "--route", "pasted", "--modified", "2026-11-04 16:00")
        self.assertIn("NOTE: this document was modified after this skill's status date", out)
        self.assertIn("NOT DONE", run("run.py", "done", R, "locate", expect=3))   # the streamlined document was never registered
        # ---------------- the main run, routes in order
        R = self.to_plan(d, "run1")
        # ---------------- quoted lines
        R2 = os.path.join(d, "run1c")
        run("run.py", "start", R2, "--kind", "build", "--request", "Please add the monitor line to G5b")
        self.register(R2, ("streamlined", "master_plan", "register"))
        run("run.py", "done", R2, "locate")
        run("run.py", "stages", R2, "--codes", "A6e", expect="refused")           # not a stage
        run("run.py", "stages", R2, "--general", "no stage", expect="refused")    # only a document edit or a review may
        run("run.py", "stages", R2, "--codes", "A6d,G5b")
        run("run.py", "done", R2, "stages")
        run("run.py", "read", R2, "--ack", "2", "--note", "x", expect="refused")  # pages are acknowledged in order
        self.read_pages(R2)
        run("run.py", "done", R2, "read")
        run("run.py", "done", R2, "proof", expect=3)                              # nothing quoted yet
        run("run.py", "evidence", R2, "--stage", "A6d", "--doc", "streamlined", "--line", "A line that the document does not hold at all.", expect="refused")
        run("run.py", "evidence", R2, "--stage", "A6d", "--doc", "streamlined", "--line", "A6d Acceptance", expect="refused")      # too short
        run("run.py", "evidence", R2, "--stage", "A12", "--doc", "streamlined", "--line", sample.EV[("A12", "streamlined")], expect="refused")  # not declared
        run("run.py", "evidence", R2, "--stage", "A6d", "--doc", "master_plan", "--line", sample.EV[("A6d", "master_plan")])
        self.assertIn("each stage needs its own line", run("run.py", "evidence", R2, "--stage", "G5b", "--doc", "master_plan", "--line", sample.EV[("A6d", "master_plan")], expect="refused"))
        run("run.py", "evidence", R2, "--stage", "A6d", "--doc", "streamlined", "--line", sample.EV[("A6d", "streamlined")])
        run("run.py", "done", R2, "proof", expect=3)                              # G5b still has no lines
        # ---------------- the plan rules (each mutation of a good plan is refused for its own reason)
        good = sample.plan()
        gp = os.path.join(d, "plan_good.json")

        def refused(mutate, needle):
            pl = copy.deepcopy(good)
            mutate(pl)
            path = os.path.join(d, "plan_bad.json")
            jwrite(path, pl)
            self.assertIn(needle, run("run.py", "plan", R, "--file", path, expect=5))
        refused(lambda p: p["objects"][0].update(id=8), "Charl")
        refused(lambda p: p["objects"][2].update(type="section", id=15, title="C — Claims (PK)"), "never touched")
        refused(lambda p: p["objects"][0]["lines"].append({"text": "PK – Phone the client", "kind": "action"}) or p["objects"][0].update(expect_lines=4), "mixed")
        refused(lambda p: p["objects"][0]["lines"][1].update(text="Update Task Notes for this stage"), "must start with")
        refused(lambda p: p["objects"][0]["lines"][1].update(text="SR – Update Task Notes for this stage", kind="received"), "must end with")
        refused(lambda p: p["objects"][0]["lines"][2].update(text="SR – AUTOMATION: move the task to column \"G6\" — TICK DONE TO OPEN BELOW"), "CAPITALS")
        refused(lambda p: p["objects"][0]["lines"][2].update(text="SR – AUTOMATION: MOVE THE TASK TO COLUMN \"G6\""), "must end with")
        refused(lambda p: p["objects"][0].update(title="MP35 – Claude monitor"), "no 'Claude'")
        refused(lambda p: p["objects"][0].update(expect_lines=4), "expect_lines")
        refused(lambda p: p["objects"][2].update(title="G5b — Sub-tasks Running"), "ends with its owner")
        refused(lambda p: p["objects"][0].update(stage="A12"), "was not declared")
        refused(lambda p: p["documents"].append({"role": "automation", "change": "wording"}), "was not located")
        refused(lambda p: p["documents"].append({"role": "register", "change": "again"}), "listed twice")
        refused(lambda p: p.update(documents=[]), "documents first")
        refused(lambda p: p["objects"][1]["lines"][1].update(text="PK – SERVICING CASE?"), "QUESTION:")
        refused(lambda p: p.update(tick_path=[{"module": "MP35", "line": "x", "opens": "MP5"}]), "only a test has a tick path")
        jwrite(gp, good)
        run("run.py", "plan", R, "--file", gp)
        # ---------------- the plan, confirm, approve
        run("run.py", "done", R, "plan")
        run("run.py", "done", R, "confirm", expect=3)                             # no yes yet
        out = run("run.py", "confirm", R)
        self.assertIn("Nothing has been changed yet", out)
        self.assertIn("ASK PAUL", out)
        self.assertIn("DOCUMENTS (changed first, before AdviceTech)", out)
        run("run.py", "changed", R, "--role", "streamlined", "--modified", sample.now_iso(), expect="refused")   # nothing before Paul's yes
        run("run.py", "result", R, "--key", "checklist:233", "--lines", "3", "--ok", "yes", expect="refused")
        run("run.py", "approve", R, "--said", "ok", expect="refused")                                          # his own words, not a bare 'ok'
        run("run.py", "approve", R, "--said", "Yes, go ahead with Decision 56")
        run("run.py", "done", R, "confirm")
        # ---------------- the work: documents first, then the read-backs
        run("run.py", "changed", R, "--role", "automation", "--modified", sample.now_iso(), expect="refused")    # not a document of the plan
        run("run.py", "changed", R, "--role", "streamlined", "--modified", "yesterday", expect="refused")
        run("run.py", "changed", R, "--role", "streamlined", "--modified", sample.now_iso(), "--note", "G5b wording")
        run("run.py", "result", R, "--key", "checklist:233", "--lines", "3", "--ok", "yes", expect="refused")   # documents first: two are still unchanged
        run("run.py", "changed", R, "--role", "master_plan", "--modified", sample.now_iso(), "--note", "MP35, MA32")
        run("run.py", "changed", R, "--role", "register", "--modified", sample.now_iso(), "--note", "rows 233, 234")
        run("run.py", "result", R, "--key", "checklist:999", "--lines", "3", "--ok", "yes", expect="refused")    # not planned
        run("run.py", "result", R, "--key", "checklist:233", "--lines", "2", "--ok", "yes")                        # wrong line count
        run("run.py", "result", R, "--key", "checklist:234", "--lines", "6", "--ok", "yes")
        run("run.py", "result", R, "--key", "section:104", "--lines", "0", "--ok", "yes")
        self.assertIn("plan expects 3", run("run.py", "done", R, "record", expect=3))
        run("run.py", "result", R, "--key", "checklist:233", "--lines", "3", "--ok", "yes", "--note", "read back = register")
        run("run.py", "done", R, "record")
        out = run("run.py", "done", R, "final")
        self.assertIn("RESULT: PASS", out)
        self.assertIn("0 ❌", out)
        self.assertFalse([ln for ln in out.splitlines() if ln.startswith("❌")])
        for needle in ("Using prospect-review-funnel-at-knowledge", "The stage routes are consistent", "located and registered", "Every stage touched (A6d, G5b)", "No planned object is one of Charl's",
                       "The plan follows every rule", "Paul's go-ahead is recorded", "Documents first", "All 3 planned item(s) were read back", "Only attested (not proven)", "ITEMS (one row per item",
                       "Go ahead with the Family A starters?"):
            self.assertIn(needle, out)
        self.assertIn("3 of 3", out)
        full = run("verify.py", R)
        self.assertIn("RESULT: PASS", full)
        # ---------------- hand-edits are caught, because the checker rebuilds from the run folder
        planp = os.path.join(R, "plan.json")
        with open(planp, encoding="utf-8") as fh:
            pl = json.load(fh)
        pl["objects"][0]["title"] = "MP35 – changed after the yes"
        jwrite(planp, pl)
        out = run("verify.py", R, expect=1)
        self.assertIn("go-ahead is missing, or the plan changed after it", out)
        jwrite(planp, good)
        run("verify.py", R)
        txt = os.path.join(R, "docs", "streamlined.txt")
        with open(txt, encoding="utf-8") as fh:
            keep = fh.read()
        write(txt, keep + " edited by hand")
        self.assertIn("a registered text changed", run("verify.py", R, expect=1))
        write(txt, keep)
        run("verify.py", R)

    # ------------------------------------------------------------------ documents first
    def docs_first_run(self, d):
        R = self.to_plan(d, "run2")
        gp = os.path.join(d, "plan_good2.json")
        jwrite(gp, sample.plan())
        run("run.py", "plan", R, "--file", gp)
        run("run.py", "done", R, "plan")
        run("run.py", "confirm", R)
        run("run.py", "approve", R, "--said", "Yes, go ahead")
        run("run.py", "done", R, "confirm")
        # a document that was NOT changed in this run (its Date Modified is older than the yes) and one changed AFTER the first read-back
        run("run.py", "changed", R, "--role", "streamlined", "--modified", "2020-01-01T00:00:00Z")
        run("run.py", "changed", R, "--role", "master_plan", "--modified", sample.now_iso())
        run("run.py", "changed", R, "--role", "register", "--modified", sample.now_iso(60))
        for k, n in (("checklist:233", 3), ("checklist:234", 6), ("section:104", 0)):
            run("run.py", "result", R, "--key", k, "--lines", str(n), "--ok", "yes")
        out = run("run.py", "done", R, "record", expect=3)
        self.assertIn("before Paul's go-ahead", out)
        self.assertIn("AFTER the first AdviceTech change", out)
        run("run.py", "changed", R, "--role", "streamlined", "--modified", sample.now_iso())
        run("run.py", "changed", R, "--role", "register", "--modified", sample.now_iso())
        run("run.py", "done", R, "record")
        self.assertIn("RESULT: PASS", run("run.py", "done", R, "final"))
        # a read-back that is not OK is not done
        R3 = self.to_plan(d, "run3")
        run("run.py", "plan", R3, "--file", gp)
        run("run.py", "done", R3, "plan")
        run("run.py", "approve", R3, "--said", "Yes, go ahead")
        for r in ("streamlined", "master_plan", "register"):
            run("run.py", "changed", R3, "--role", r, "--modified", sample.now_iso())
        run("run.py", "result", R3, "--key", "checklist:233", "--lines", "3", "--ok", "no", "--note", "line 2 differs")
        run("run.py", "result", R3, "--key", "checklist:234", "--lines", "6", "--ok", "yes")
        run("run.py", "result", R3, "--key", "section:104", "--lines", "0", "--ok", "yes")
        run("run.py", "done", R3, "confirm")
        self.assertIn("read-back is not OK", run("run.py", "done", R3, "record", expect=3))

    # ------------------------------------------------------------------ a question
    def question_run(self, d):
        R = self.to_plan(d, "run4", kind="question", codes=("A6d", "A12"), roles=("streamlined", "master_plan"))
        bad = os.path.join(d, "a_bad.txt")
        write(bad, "Too short.")
        run("run.py", "answer", R, "--file", bad, expect=5)
        write(bad, "A6d is the acceptance stage and A12 is the audit, and A6e comes after them. The owner of both is not given here, and neither leads anywhere in particular according to this text.")
        out = run("run.py", "answer", R, "--file", bad, expect=5)
        self.assertIn("A6e, which is not a stage", out)
        self.assertIn("does not give its owner", out)
        write(bad, "Stage A6d is the Acceptance stage, owned by PK. It leads to A8 once the application, DOC, COC and RAR answers are done. Stage A12 is the Compliance Audit, owned by SR; it is an end state (case issued).")
        run("run.py", "answer", R, "--file", bad)
        run("run.py", "done", R, "answer")
        out = run("run.py", "done", R, "final")
        self.assertIn("RESULT: PASS", out)
        self.assertIn("The answer names each stage with its owner and where it leads", out)
        self.assertNotIn("ITEMS (one row", out)
        run("run.py", "plan", R, "--file", bad, expect="refused")                  # a question has no plan
        # a move must say what is open and which line to tick
        R5 = self.to_plan(d, "run5", kind="move", codes=("G5b",), roles=("streamlined", "master_plan"))
        write(bad, "The client is in G5b, a stage owned by SR; once every sub-task has ended the owner ticks the last line and the task moves on to G6.")
        self.assertIn("which line to tick", run("run.py", "answer", R5, "--file", bad, expect=5))
        write(bad, "The client is in G5b, a stage owned by SR. The items still open are the sub-tasks; when every sub-task has ended the owner ticks the last line, which opens G6.")
        run("run.py", "answer", R5, "--file", bad)

    # ------------------------------------------------------------------ a document edit with no stage and no AdviceTech
    def docs_run(self, d):
        R = os.path.join(d, "run6")
        run("run.py", "start", R, "--kind", "docs", "--request", "Tidy the wording of the standing rules in all documents")
        self.register(R, ("streamlined", "master_plan", "flow_comparison"))
        run("run.py", "done", R, "locate")
        run("run.py", "stages", R, "--codes", "", expect="refused")
        run("run.py", "stages", R, "--general", "a wording change in the standing rules; no stage is touched")
        run("run.py", "done", R, "stages")
        self.read_pages(R)
        run("run.py", "done", R, "read")
        run("run.py", "done", R, "proof")                                         # no stage, no quoted lines needed
        pl = {"decision": "Decision 57 – invented wording tidy", "paul_request": "Tidy the wording of the standing rules in all documents", "stages": [],
              "documents": [{"role": "streamlined", "change": "standing rules wording"}, {"role": "master_plan", "change": "standing rules wording"}], "next": "the flow page"}
        bad = dict(pl, objects=[{"type": "checklist", "id": 233, "title": "MP35", "stage": "G5b", "expect_lines": 1, "lines": [{"text": "SR – x", "kind": "action"}]}])
        p = os.path.join(d, "plan_docs.json")
        jwrite(p, bad)
        self.assertIn("does not touch AdviceTech", run("run.py", "plan", R, "--file", p, expect=5))
        jwrite(p, pl)
        run("run.py", "plan", R, "--file", p)
        run("run.py", "done", R, "plan")
        run("run.py", "confirm", R)
        run("run.py", "approve", R, "--said", "Yes, tidy it")
        run("run.py", "done", R, "confirm")
        run("run.py", "changed", R, "--role", "streamlined", "--modified", sample.now_iso())
        run("run.py", "done", R, "record", expect=3)                              # the master plan is still unchanged
        run("run.py", "changed", R, "--role", "master_plan", "--modified", sample.now_iso())
        run("run.py", "done", R, "record")
        out = run("run.py", "done", R, "final")
        self.assertIn("RESULT: PASS", out)
        self.assertIn("Documents changed (documents first)", out)
        self.assertIn("Go ahead with the flow page?", out)

    # ------------------------------------------------------------------ the model: routes, pages, lines
    def model_checks(self, d):
        self.assertEqual(F.route_problems(), [], "the real stage routes must be consistent")
        data = F.funnel()

        def probs(mutate):
            x = copy.deepcopy(data)
            mutate(x)
            return " | ".join(F.route_problems(x))
        S = lambda x, i: next(s for s in x["stages"] if s["id"] == i)  # noqa: E731
        self.assertIn("which is not a stage", probs(lambda x: S(x, "A6d")["outcomes"][0].update(to=["A99"])))
        self.assertIn("dead end", probs(lambda x: S(x, "A6d").update(outcomes=[])))
        self.assertIn("not reachable", probs(lambda x: x["stages"].append({"id": "Z1", "name": "x", "owner": "SR", "outcomes": [], "end": "NTU", "page": "x.md"})))
        self.assertIn("loop without an exit", probs(lambda x: [S(x, "A10c").update(outcomes=[{"label": "x", "to": ["A10d"]}]), S(x, "A10d").update(outcomes=[{"label": "x", "to": ["A10c"]}])]))
        self.assertIn("opens mutually exclusive stages", probs(lambda x: S(x, "A10").update(outcomes=[{"label": "both", "to": ["A10a", "A10b"]}])))
        self.assertIn("opens several stages together", probs(lambda x: S(x, "A10").update(outcomes=[{"label": "two", "to": ["A10a", "A11"]}])))
        self.assertIn("listed twice", probs(lambda x: x["stages"].append(copy.deepcopy(S(x, "A1")))))
        self.assertIn("is not SR, PK or CL", probs(lambda x: S(x, "A1").update(owner="Sitamah")))
        # the pages: a stage that does not exist and a count typed by hand are caught
        sk = os.path.join(d, "skillcopy")
        os.makedirs(os.path.join(sk, "references"))
        write(os.path.join(sk, "references", "x.md"), "Stage A6e leads on. The register holds 1,487 lines and 189 of 189 checklists. Good: {counts.lines} and G5b and A2 and B9c.\n")
        pr = " | ".join(F.pages_problems(sk))
        self.assertIn("A6e", pr)
        self.assertIn("a count typed by hand ('1,487 lines')", pr)
        self.assertIn("189 of 189 checklists", pr)
        self.assertNotIn("A2,", pr)
        self.assertEqual(F.expand("{counts.lines} lines as at {as_of}"), "1,487 lines as at %s" % F.status()["as_of"])
        # the line rules
        self.assertEqual(F.line_problems({"text": "SR – Do the thing", "kind": "action"}), [])
        self.assertTrue(F.line_problems({"text": "SR - Do the thing", "kind": "action"}))                     # a hyphen is not the en dash
        self.assertTrue(F.line_problems({"text": "Do the thing", "kind": "action"}))
        self.assertTrue(F.line_problems({"text": "Mixed Case Heading", "kind": "subheading"}))
        self.assertEqual(F.line_problems({"text": "SR – AUTOMATION: MOVE THE TASK TO COLUMN \"G5b\" — IF THE ANSWER BELOW IS YES", "kind": "automation"}), [])
        self.assertTrue(F.line_problems({"text": "SR – x", "kind": "weird"}))
        # a test runs on Mr John Snow only
        tp = copy.deepcopy(sample.plan())
        tp["objects"] = []
        tp.update(client="A Real Client", tick_path=[{"module": "MP35", "line": "x", "opens": "MP5"}])
        tp["documents"] = []
        self.assertTrue(any("Mr John Snow only" in x for x in F.plan_problems(tp, "test", ["A6d", "G5b"], set(), "Mr John Snow")))
        tp["client"] = "Mr John Snow"
        self.assertEqual(F.plan_problems(tp, "test", ["A6d", "G5b"], set(), "Mr John Snow"), [])
        # the documents are read as text
        import doctext
        self.assertIn("MP35 | SR – Monitor progress on all open sub-tasks", doctext.read(self.docs["master_plan"]))
        self.assertIn("233 | MP35 | G5b", doctext.read(self.docs["register"]))
        self.assertIn("Flow comparison", doctext.read(self.docs["flow_comparison"]))


if __name__ == "__main__":
    unittest.main()
