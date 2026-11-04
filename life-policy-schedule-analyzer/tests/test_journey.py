"""The ONE test of the life-policy-schedule-analyzer skill (Operation Skill Restructure: one end-to-end test on invented data).

It plays a whole job through the program exactly as a chat would, on invented documents (Pat Samplecase; two Samplelife schedules, one with a page that is only an image; a Testco proposed
quote with its payback document; a Fact Find Summary; meeting notes; the saved product sources), with today fixed by WR_TODAY. Nothing is saved or sent anywhere: the folder listing is typed in
as receipts. It proves:
  1. the driver refuses to skip a step; the routes must be tried in order; a schedule can never be missing; the insurers must be declared and each needs a saved guide with its address and date;
  2. bad analyses are refused (nothing saved): a figure that is not in its evidence line, an evidence line that is not in the document, a product statement with no source or a source about
     another insurer or a line that is not in the saved source, an invented premium table, a missing mandatory section (dread disease topics, a benchmark row for every benefit held), a benchmark,
     cession or second-life finding with no finding behind it, a text over its limit, internal wording on a client slide, a key thing that does not point at an Action Required finding, a payback
     figure that is not in the payback document, image_read on a page that has text, a wrong pattern;
  3. the premium table is the insurer's, computed from a stated rate, computed from Paul's assumption, or 'not provided'; a changed analysis voids the check and Paul's yes; nothing is drawn
     before his yes;
  4. the internal report and the client slides are drawn and READ BACK: the INTERNAL label on every page, the sections in order, the numbered findings in both places, SINGLE SOURCE and
     'Verified: 2 sources' tags, 'Not held (your choice)', the payback row and the 'Paybacks compared' slide, estimates labelled; a slide whose text does not fit stops the build;
  5. the save never overwrites without a yes and must list every file with its size; the final audit is short and every line is a green tick; a hand-edited PDF is caught.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
SCRIPTS = os.path.join(SKILL, "scripts")
sys.path.insert(0, SCRIPTS)
sys.path.insert(0, HERE)
import sample  # noqa: E402

OK, BAD = "\u2705", "\u274c"
URL = "https://example.invalid/source"
TODAY = date(2026, 11, 5)


def run(script, *args, expect=0, env=None):
    e = dict(os.environ, WR_TODAY="05/11/2026", WR_NOW="10:15")
    e.update(env or {})
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS, script)] + list(args), capture_output=True, text=True, encoding="utf-8", env=e)
    if expect == "refused":
        assert r.returncode != 0, "%s %s should have been refused\n%s" % (script, args, r.stdout[-1200:])
    else:
        assert r.returncode == expect, "%s %s -> exit %d (wanted %d)\n%s\n%s" % (script, args, r.returncode, expect, r.stdout[-2400:], r.stderr[-800:])
    return r.stdout + r.stderr


class Journey(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="wr-lpa-test-")
        self.docs = sample.make_docs(self.d)

    def afile(self, data, name="analysis.json"):
        path = os.path.join(self.d, name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        return path

    def refused(self, R, data, fragment):
        out = run("run.py", "analysis", R, "--file", self.afile(data), expect="refused")
        self.assertIn(fragment, out)
        self.assertFalse(os.path.exists(os.path.join(R, "analysis.json")), "a refused analysis must not be saved")

    def read_all(self, R, done=None):
        seen = []
        for _ in range(80):
            out = run("run.py", "read", R)
            seen.append(out)
            m = re.search(r"--ack ([a-z_0-9]+:\d+)", out)
            if not m:
                break
            run("run.py", "read", R, "--ack", m.group(1), "--note", "read " + m.group(1))
        if done:
            run("run.py", "done", R, done)
        return "\n".join(seen)

    def register(self, R, via="device"):
        run("run.py", "access", R, "--purpose", "locate", "--route", via, "--result", "found", "--note", "test")
        for lab, (role, key) in sample.LABELS.items():
            run("run.py", "doc", R, "--role", role, "--label", lab, "--file", self.docs[key], "--route", via)
        run("run.py", "doc", R, "--role", "fact_find_summary", "--file", self.docs["fact_find_summary"], "--route", via)
        run("run.py", "doc", R, "--role", "intake_notes", "--label", "2026-10-02", "--file", self.docs["intake_notes_2026_10_02"], "--route", via)

    def test_whole_journey(self):
        self.main_case()
        self.small_cases()

    # ------------------------------------------------------------------ the whole job
    def main_case(self):
        import lpa as c
        # --- a separate run: the routes must be tried in order, a schedule can never be missing
        R0 = os.path.join(self.d, "run0")
        run("run.py", "start", R0, "--client", "Pat Samplecase")
        run("run.py", "access", R0, "--purpose", "locate", "--route", "m365", "--result", "found")
        out = run("run.py", "doc", R0, "--role", "schedule", "--label", "Samplelife Life Plan", "--file", self.docs["schedule_samplelife_life_plan"], "--route", "m365", expect="refused")
        self.assertIn("tried in order", out)
        out = run("run.py", "doc", R0, "--missing", "schedule", "--label", "Samplelife Life Plan", "--said", "could not find it", expect="refused")
        self.assertIn("can never be missing", out)

        R = os.path.join(self.d, "run")
        out = run("run.py", "start", R, "--client", "Pat Samplecase")
        self.assertIn("Using life-policy-schedule-analyzer, last updated", out)
        self.assertIn("STEP 1 of 9", out)
        self.assertIn("refused", run("run.py", "done", R, "research", expect="refused").lower())
        # --- locate
        self.register(R)
        out = run("run.py", "insurers", R, "--file", self.afile([{"label": "Samplelife Life Plan", "insurer": "Nobody"}, {"label": "Samplelife Disability Plan", "insurer": "Samplelife"},
                                                                  {"label": "Testco Proposal", "insurer": "Testco"}], "insurers.json"), expect="refused")
        self.assertIn("is not in the text", out)
        out = run("run.py", "insurers", R, "--file", self.afile(sample.INSURERS, "insurers.json"))
        self.assertIn("Testco - <title>", out)
        run("run.py", "done", R, "locate")
        # --- read (the image-only page is flagged)
        out = self.read_all(R, "read")
        self.assertIn("NO READABLE TEXT", out)
        # --- research: a source needs an address and a date, its label starts with a declared insurer, every insurer needs a guide
        run("run.py", "access", R, "--purpose", "research", "--route", "web", "--result", "found", "--note", "test")
        g = self.docs["guide_samplelife_technical_guide"]
        out = run("run.py", "doc", R, "--role", "guide", "--label", "Samplelife - Technical Guide", "--file", g, "--route", "web", expect="refused")
        self.assertIn("--url", out)
        out = run("run.py", "doc", R, "--role", "guide", "--label", "Nobody - Guide", "--file", g, "--route", "web", "--url", URL, "--fetched-at", "04/11/2026", expect="refused")
        self.assertIn("declare the insurers first", out)
        for key in ("guide_samplelife_technical_guide", "source_samplelife_independent_review"):
            role, lab = sample.SOURCE_LABELS[key]
            run("run.py", "doc", R, "--role", role, "--label", lab, "--file", self.docs[key], "--route", "web", "--url", URL, "--fetched-at", "04/11/2026")
        out = run("run.py", "done", R, "research", expect=3)
        self.assertIn("no guide", out)
        role, lab = sample.SOURCE_LABELS["guide_testco_product_guide"]
        run("run.py", "doc", R, "--role", role, "--label", lab, "--file", self.docs["guide_testco_product_guide"], "--route", "web", "--url", URL, "--fetched-at", "04/11/2026")
        self.read_all(R, "research")
        # --- the analysis: every refusal
        a = sample.analysis()
        B = sample.bad
        self.refused(R, B(a, **{"policies.0.premium.monthly": "R 1 451.00"}), "not in the evidence line")
        self.refused(R, B(a, **{"policies.0.benefits.0.evidence": "Life cover R 1 500 000.00 monthly cost R 900.00 payable yearly"}), "not in the text of")
        self.refused(R, B(a, **{"policies.0.dread_disease.exceed_100": {"text": "No more than the cover.", "basis": "product"}}), "sources are needed")
        self.refused(R, B(a, **{"policies.0.dread_disease.exceed_100.sources.0.source": "guide_testco_product_guide"}), "not about Samplelife")
        self.refused(R, B(a, **{"policies.0.dread_disease.exceed_100.sources.0.evidence": "A staged claim pays double."}), "not in the text of")
        self.refused(R, B(a, **{"policies.0.premium.assumption": {"rate": "7", "text": "7%", "said": ""}}), "assumption is {rate, text, said")
        self.refused(R, B(a, **{"policies.1.premium.assumption": {"rate": "7", "text": "7%", "said": "Assume seven percent"}}), "an assumption is only for a premium with no printed table")
        self.refused(R, B(a, **{"policies.0.premium.projection": [{"n": 1, "premium": "R 9 999.00"}]}), "not in the document's text")
        self.refused(R, B(a, **{"policies.0.benchmark.0": sample.DELETE}), "a benchmark row is needed for every major benefit held")
        self.refused(R, B(a, **{"policies.0.findings.0.refs": []}), "needs a finding with refs")
        self.refused(R, B(a, **{"policies.0.findings.1.refs": []}), "a cession needs a finding")
        self.refused(R, B(a, **{"policies.0.dread_disease.duration": sample.DELETE}), "needs exactly these topics")
        self.refused(R, B(a, **{"policies.1.dread_disease": a["policies"][0]["dread_disease"]}), "no dread disease benefit is held")
        self.refused(R, B(a, **{"policies.1.second_life": {"status": "rider", "text": "A rider.", "basis": "inference"}}), "needs its own benefits")
        self.refused(R, B(a, **{"policies.0.verdict": "word " * 60}), "the limit is 45")
        self.refused(R, B(a, **{"slides.by_insurer.Samplelife.how_it_works.0": "Our benchmark shows more."}), "must not appear on a client-facing slide")
        self.refused(R, B(a, **{"slides.by_insurer.Samplelife.key_things.0.n": 4}), "must point at an Action Required finding")
        self.refused(R, B(a, **{"proposed_status": "none_for_now"}), "no proposed quote may be entered or registered")
        self.refused(R, B(a, **{"proposed.payback.components.0.amount": "R 61 000.00"}), "not in the evidence line")
        self.refused(R, B(a, **{"proposed.categories.life.amount": "R 1 600 000.00"}), "not in the evidence line")
        self.refused(R, B(a, **{"unexpected": 1}), "keys exactly")
        self.refused(R, B(a, **{"left_out.0.evidence": "Income protection was never discussed."}), "not in the text of")
        self.refused(R, B(a, **{"policies.1.benefits.0.details.0.page": 1}), "image_read is only for a page")
        self.refused(R, B(a, **{"policies.0.benefits.0.bullets.0": {"text": "Pays a lump sum.", "basis": "inference", "evidence": "some line here"}}), "has no source")
        self.refused(R, B(a, **{"policies.0.premium.pattern.type": "annual"}), "must be 'fixed' or 'age_rated'")
        self.refused(R, B(a, **{"policies.0.benefits.0.bullets.0.text": "word " * 40}), "the limit is 30")
        self.refused(R, B(a, **{"policies.0.life_cover_type": None}), "life_cover_type.type must be")
        # --- the good analysis
        out = run("run.py", "analysis", R, "--file", self.afile(a))
        self.assertIn("analysis saved", out)
        run("run.py", "done", R, "analysis")
        # --- check, show, approve
        out = run("run.py", "show", R, expect="refused")
        self.assertIn("run.py check first", out)
        out = run("run.py", "check", R)
        self.assertIn("premium table none (0 rows)", out)
        self.assertIn("premium table computed (10 rows)", out)
        self.assertIn("SINGLE source", out)
        self.assertIn("3 statement(s) are inferences", out)
        self.assertIn("guarantee period is not stated", out)
        run("run.py", "done", R, "check")
        out = run("run.py", "approve", R, "--said", "yes", expect="refused")
        self.assertIn("not been shown", out)
        out = run("run.py", "build", R, expect="refused")
        self.assertIn("REFUSED", out)
        out = run("run.py", "show", R)
        self.assertIn("THE ONE QUESTION TO PAUL", out)
        self.assertIn("FIGURES READ FROM PAGE IMAGES", out)
        self.assertIn("Proposed quote (Report 2)", out)
        self.assertIn("Honest Opinion", out)
        self.assertIn("Left out on purpose", out)
        names = c.all_names(self.loadj(os.path.join(R, "analysis.json")), TODAY)
        for n in names:
            self.assertIn(n, out)
        # a changed analysis voids the check and the yes
        run("run.py", "analysis", R, "--file", self.afile(B(a, **{"policies.0.verdict": "Solid whole of life cover, but the dread disease benefit pays by severity bands."})))
        out = run("run.py", "show", R, expect="refused")
        self.assertIn("run.py check first", out)
        run("run.py", "analysis", R, "--file", self.afile(a))
        run("run.py", "done", R, "analysis")
        run("run.py", "check", R)
        run("run.py", "done", R, "check")
        run("run.py", "show", R)
        run("run.py", "approve", R, "--said", "Yes, draw them")
        run("run.py", "done", R, "confirm")
        # --- build
        out = run("run.py", "build", R)
        self.assertIn("program checks passed", out)
        outdir = os.path.join(R, "out")
        for n in names:
            self.assertTrue(os.path.exists(os.path.join(outdir, n)), n)
        self.check_pdfs(outdir, names)
        run("run.py", "done", R, "build")
        # --- save
        out = run("run.py", "name", R, "--existing", names[0], expect=5)
        self.assertIn("already exist", out)
        out = run("run.py", "name", R, "--existing", "something else.pdf")
        self.assertIn("SAVE THESE FILES", out)
        run("run.py", "access", R, "--purpose", "save", "--route", "device", "--result", "found", "--note", "test")
        folder = "C:\\Clients\\%s\\6. Policy Schedules\\Analysis & Comparison Reports" % sample.FOLDER
        run("run.py", "receipt", R, "save.folder", folder)
        out = run("run.py", "done", R, "save", expect=3)
        run("run.py", "receipt", R, "save.listed", ";".join("%s=%d" % (n, os.path.getsize(os.path.join(outdir, n))) for n in names))
        run("run.py", "done", R, "save")
        out = run("run.py", "done", R, "final")
        self.assertIn("RESULT: PASS", out)
        self.assertEqual([l for l in out.splitlines() if l.startswith(BAD)], [])
        self.assertIn("THE TABULATED CHAT SUMMARY", out)
        self.assertIn("Action Required:", out)
        self.assertIn("Only attested (not proven):", out)
        audit = out.split("AUDIT", 1)[1].split("THE TABULATED", 1)[0] if out.index("AUDIT") < out.index("THE TABULATED") else ""
        self.assertLess(len(audit.splitlines()), 30, "the audit must be short")
        # --- a hand-edited PDF is caught
        with open(os.path.join(outdir, names[0]), "ab") as f:
            f.write(b"\n%edited by hand")
        r = subprocess.run([sys.executable, os.path.join(SCRIPTS, "verify.py"), R], capture_output=True, text=True, encoding="utf-8", env=dict(os.environ, WR_TODAY="05/11/2026"))
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("edited by hand?", r.stdout)
        self.R = R

    def loadj(self, path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def check_pdfs(self, outdir, names):
        import lpapdf
        pdf = {n: lpapdf.read_pdf(os.path.join(outdir, n)) for n in names}
        life, dis = (pdf[n] for n in names[:2])
        t0 = lpapdf.flat(life)
        label = "INTERNAL - NOT FOR CLIENT DISTRIBUTION"
        self.assertTrue(all(label in pg["text"] for pg in life + dis))
        for frag in ("SINGLE SOURCE", "Verified: 2 sources", "Inference - to be confirmed", "Not applicable: Samplelife has no wellness-linked pricing mechanism.", "not provided",
                     "Dread Disease Deep-Dive", "Ceded to Samplebank", "Severity-tiered", "Broker's Honest Opinion", "Sources"):
            self.assertIn(frag, t0, frag)
        t1 = lpapdf.flat(dis)
        self.assertIn("Illustrative: computed from the stated yearly increase of 8%", t1)
        self.assertIn("R 324.00", t1)                                             # year 2: 300 x 1.08
        self.assertIn("Waiting period 30 days", t1)
        r1, r2 = pdf[names[2]], pdf[names[3]]
        self.assertEqual(len(r1), 6)
        self.assertEqual(len(r2), 7)
        glance = r1[1]["text"]
        self.assertIn("Not held (your choice)", glance)                           # income protection was left out on purpose
        for cat in ("Life", "Disability", "Dread / Serious Illness", "Income Protection"):
            self.assertIn(cat, glance)
        self.assertIn("Combined monthly premium", glance)
        t2 = lpapdf.flat(r2)
        for frag in ("Paybacks compared", "Change Moment Pay-Out", "R 95 000.00", "estimate", "28/11/2026", "(est.)", "R 2 071.00"):   # R 2 071.00 = 1 900 x 1.09
            self.assertIn(frag, t2, frag)
        for t in (lpapdf.flat(r1), t2):
            self.assertNotIn("INTERNAL", t)
            self.assertNotIn("Honest Opinion", t)

    # ------------------------------------------------------------------ small model-level checks
    def small_cases(self):
        import lpa as c
        import lpapdf
        import verify
        a = sample.analysis()
        docs, ev = verify.load_docs(self.R)
        ann, probs = c.annotate(a, ev, docs, TODAY, "Pat Samplecase", {"insurers": sample.INSURERS})
        self.assertEqual(probs, [])
        p0, p1 = ann["policies"]
        t0, t1 = c.projection_table(p0), c.projection_table(p1)
        self.assertEqual((t0["mode"], len(t0["rows"])), ("none", 0))                # age-rated and no printed table: no number invented
        self.assertEqual((t1["mode"], len(t1["rows"]), str(t1["rows"][1]["premium"])), ("computed", 10, "324.00"))
        printed = {"premium": {"monthly": "R 1 000.00", "pattern": {"type": "age_rated"}, "projection": [{"n": 1, "premium": "R 1 000.00"}, {"n": 2, "premium": "R 1 100.00", "printed_pct": "10.00"}], "age_start": None}}
        tp = c.projection_table(printed)
        self.assertEqual((tp["mode"], str(tp["rows"][1]["pct"]), tp["rows"][1]["kind"]), ("printed", "10.00", "printed"))
        asm = {"premium": {"monthly": "R 1 000.00", "pattern": {"type": "age_rated"}, "projection": None, "assumption": {"rate": "5"}, "age_start": None}}
        self.assertEqual((c.projection_table(asm)["mode"], str(c.projection_table(asm)["rows"][2]["premium"])), ("assumption", "1102.50"))
        # the findings are numbered Action Required first, the same numbers everywhere
        fn = c.finding_numbers(p0)
        self.assertEqual([(n, t) for n, t, _h, _d in fn], [(1, "action"), (2, "action"), (3, "action"), (4, "awareness")])
        self.assertEqual(c.combined_premium([p0, p1]), c.combined_premium([p1, p0]))
        # the words a client slide must never carry
        self.assertTrue(set(c.banned_slide_words("Our benchmark and the Honest Opinion")) >= {"benchmark", "honest opinion"})
        self.assertEqual(c.banned_slide_words("Your cover pays a lump sum."), [])
        # a slide whose text does not fit stops the build (never clipped silently)
        long_ann = c.annotate(a, ev, docs, TODAY, "Pat Samplecase", {"insurers": sample.INSURERS})[0]
        long_ann["slides"]["by_insurer"]["Samplelife"]["how_it_works"] = ["A very long sentence about your cover. " * 120]
        with self.assertRaises(lpapdf.SlideOverflow):
            lpapdf.build_slides(long_ann, "report1", "Samplelife", docs, ev, TODAY, os.path.join(self.d, "overflow.pdf"))
        # no proposed quote: Report 2 is not built and is not named
        none = sample.bad(a, **{"proposed_status": "none_for_now", "proposed_said": "No proposed covers for now", "proposed": None, "slides.report2": None})
        kinds = [k for k, _i, _n in c.slide_names(none, TODAY)]
        self.assertEqual(kinds, ["report1"])
        self.assertEqual(c.settings()["folder_name"], "Analysis & Comparison Reports")


if __name__ == "__main__":
    unittest.main()
