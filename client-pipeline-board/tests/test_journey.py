"""The ONE test of the client-pipeline-board (Operation Skill Restructure: one end-to-end test on invented data).

It plays two whole jobs through the program exactly as a chat would, on an invented client (Pat Samplecase, example.invalid addresses, an invented
Fact Find Summary drawn by tests/sample.py) with today fixed at 05/11/2026 and the South African clock at 10:15 (WR_TODAY and WR_NOW, for tests only).
Nothing is sent anywhere: the tool results are typed in as receipts and read-backs, as a chat would copy them. It proves:
  1. the driver refuses to skip a step and refuses a route used before the earlier ones failed;
  2. bad changes are refused: a figure not in its evidence line, a tag Paul did not give, a tag on a line that cannot carry one, a bracket subject,
     a wrong Cc, a typed sign-off, a missing details block, a Sitamah message not on the list;
  3. a first board (three lines, a provisional point, a pending question, a follow-up, three emails, three messages, a check-in) is built, shown,
     approved, sent, published and read back, and ends in a short audit of green ticks;
  4. nothing is created before Paul's yes; a wrong draft, a Zapier-made draft and a message with no real bold tag are caught;
  5. a page edited by hand is caught by the final checker, and a base board edited by hand is refused;
  6. a second run reads the first board back, clears the question, adds an action and a new Change Log entry at the top.
"""
import copy
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
SCRIPTS = os.path.join(SKILL, "scripts")
sys.path.insert(0, SCRIPTS)
sys.path.insert(0, HERE)
import board as b  # noqa: E402
import boardhtml as bh  # noqa: E402
import sample  # noqa: E402

ENV = dict(os.environ, WR_TODAY="05/11/2026", WR_NOW="10:15")
SUBJ_DOC = "Pat Samplecase / Documents we need"
SUBJ_QUOTE = "Pat Samplecase / FNA quote request"


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


def readf(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def jread(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def draft_readback(e):
    return {"subject": e["subject"], "toRecipients": [{"emailAddress": {"address": a}} for a in e["to"]], "ccRecipients": [{"emailAddress": {"address": a}} for a in e["cc"]]}


def html_message(text):
    html = text.replace("**Action needed:**", "<strong>Action needed:</strong>").replace("\n", "<br>")
    return {"body": {"content": html}}


class Journey(unittest.TestCase):
    def test_journey(self):
        with tempfile.TemporaryDirectory() as d:
            self.first_run(d)
            self.second_run(d)
            self.third_run(d)

    # ------------------------------------------------------------------ small helpers
    def receipt(self, R, key, value):
        run("run.py", "receipt", R, key, value)

    def refused_change(self, R, d, mutate, needle):
        ch = sample.change_first(SUBJ_DOC, SUBJ_QUOTE)
        mutate(ch)
        path = os.path.join(d, "bad_change.json")
        jwrite(path, ch)
        out = run("run.py", "change", R, "--file", path, expect=5)
        self.assertIn(needle, out)

    # ------------------------------------------------------------------ the first board
    def first_run(self, d):
        pdf = os.path.join(d, "Fact Find Summary - 05.11.26 - (Pat Samplecase).pdf")
        sample.make_pdf(pdf, sample.FF_SUMMARY)
        R = os.path.join(d, "run1")
        out = run("run.py", "start", R, "--client", "Pat Samplecase")
        self.assertIn("Using client-pipeline-board, last updated", out)
        self.assertIn("STEP 1 of 8", out)
        # the driver refuses to skip a step
        self.assertIn("finish step 'locate' first", run("run.py", "done", R, "change", expect=3))
        # the routes are tried in order: Microsoft 365 before the computer failed is refused
        run("run.py", "access", R, "--purpose", "board", "--route", "artifact", "--result", "failed", "--note", "searched the Artifact list: no board for Pat Samplecase")
        run("run.py", "access", R, "--purpose", "docs", "--route", "m365", "--result", "found", "--note", "too early")
        self.assertIn("tried in order", run("run.py", "doc", R, "--role", "fact_find_summary", "--file", pdf, "--route", "m365", expect="refused"))
        # a fresh run folder with honest tries
        shutil.rmtree(R)
        run("run.py", "start", R, "--client", "Pat Samplecase")
        run("run.py", "access", R, "--purpose", "board", "--route", "artifact", "--result", "failed", "--note", "searched the Artifact list: no board for Pat Samplecase")
        for folder in b.settings()["on_file_folders"]:
            run("run.py", "access", R, "--purpose", "onfile", "--route", "device", "--result", "found", "--note", "%s: nothing signed yet" % folder)
        run("run.py", "access", R, "--purpose", "docs", "--route", "device", "--result", "found", "--note", "Fact Find Summary in 2. Fact Find")
        run("run.py", "base", R, "--first-board", "yes", "--said", "Paul: there is no board yet")
        run("run.py", "doc", R, "--role", "fact_find_summary", "--file", pdf, "--route", "device")
        run("run.py", "done", R, "locate")
        # bad changes are refused, each for its own reason
        self.receipt(R, "skill.teams.run", "PASS")
        self.refused_change(R, d, lambda c: c["ops"][7]["bullets"][0].update(text="Life cover needed: R9 999 000"), "not in its evidence line")
        self.refused_change(R, d, lambda c: c["ops"][3].pop("paul_said"), "Never inferred from documents")
        self.refused_change(R, d, lambda c: c["ops"].insert(5, {"op": "add_line", "line": "rgar"}) or c["ops"].insert(6, {"op": "tag", "line": "rgar", "tag": "Servicing", "paul_said": "service"}), "only Life Cover, Retirement Annuity and Investments")
        self.refused_change(R, d, lambda c: c["emails"][0].update(subject="[ALWYN - TEMPLATE] Pat Samplecase"), "bracket tag")
        self.refused_change(R, d, lambda c: c["emails"][1]["cc"].append("someone@example.invalid"), "Cc is")
        self.refused_change(R, d, lambda c: c["emails"][0].update(body_html=c["emails"][0]["body_html"] + "<p>Kind regards,</p>"), "types a sign-off")
        self.refused_change(R, d, lambda c: c["emails"][2]["client_details"].pop("cell"), "details block needs")
        self.refused_change(R, d, lambda c: c["notify"].append({"trigger": "made_up_message", "slots": {}}), "not a message on the list")
        self.refused_change(R, d, lambda c: c["ops"][8]["bullets"][0].update(text="Documents needed (see LC-1)"), "stage code")
        # the good change
        ch = sample.change_first(SUBJ_DOC, SUBJ_QUOTE)
        cpath = os.path.join(d, "change1.json")
        jwrite(cpath, ch)
        out = run("run.py", "change", R, "--file", cpath)
        self.assertIn("CHANGES APPLIED", out)
        self.assertIn("3 email(s) checked, 3 message(s) to Sitamah planned", out)
        run("run.py", "done", R, "change")
        out = run("run.py", "route", R)
        self.assertIn("ROUTING FOR PAT SAMPLECASE", out)
        self.assertIn("Life Cover [New Business]", out)
        self.assertIn("fresh yes before it goes: YES", out)            # the Medical Aid referral
        run("run.py", "done", R, "route")
        run("run.py", "build", R)
        run("run.py", "done", R, "build")
        page = readf(os.path.join(R, "out", "board.html"))
        for needle in ("Pat Samplecase — Pipeline", "New Business", "Provisional", "claude-tag", "Next appointment: 20/11/2026 at 16:00 SAST", "Question for Paul", "Change Log"):
            self.assertIn(needle, page)
        self.assertNotIn("<button", page)
        # nothing before Paul's yes
        self.assertIn("not been shown", run("run.py", "approve", R, "--said", "yes", expect="refused"))
        self.assertIn("before Paul's yes", run("run.py", "email", R, "--id", "e1", "--file", os.path.join(d, "none.json"), expect="refused"))
        out = run("run.py", "show", R)
        self.assertIn("Ready to republish Pat Samplecase's board, send 1 email", out)
        self.assertIn("save 2 drafts in Outlook", out)
        self.assertIn("message Sitamah on Teams (3)", out)
        self.assertIn("Please see attached Fact Find Summary for this client.", out)
        self.assertIn("Nothing needed from you.", out)
        run("run.py", "approve", R, "--said", "Yes, go ahead")
        run("run.py", "done", R, "confirm")
        # ---- send: emails
        msgs = jread(os.path.join(R, "out", "messages.json"))
        self.assertEqual([m["trigger"] for m in msgs], ["general_email_drafted", "lizelle_attach", "fyi"])
        mails = {e["id"]: e for e in ch["emails"]}
        for eid, tool, key in (("e1", "outlook_create_draft", "draft"), ("e2", "outlook_create_draft", "draft"), ("e3", "outlook_send_mail", "sent")):
            e = mails[eid]
            rb = os.path.join(d, "rb_%s.json" % eid)
            jwrite(rb, draft_readback(e))
            if eid == "e1":
                # Sitamah is not messaged before the emails are checked; a Zapier-made draft is refused; a wrong Cc read back is refused
                self.assertIn("only after the emails are checked", run("run.py", "message", R, "--id", "m1", expect="refused"))
                self.receipt(R, "email.e1.created_with", "zapier microsoft_office_365_create_draft_email")
                self.receipt(R, "email.e1.draft", "AAMkDraft1")
                self.assertIn("never Zapier", run("run.py", "email", R, "--id", "e1", "--file", rb, expect=5))
                bad = draft_readback(e)
                bad["ccRecipients"] = []
                jwrite(os.path.join(d, "rb_bad.json"), bad)
                self.receipt(R, "email.e1.created_with", tool)
                self.assertIn("equal the checked email", run("run.py", "email", R, "--id", "e1", "--file", os.path.join(d, "rb_bad.json"), expect=5))
            self.receipt(R, "email.%s.created_with" % eid, tool)
            self.receipt(R, "email.%s.%s" % (eid, key), "id-" + eid)
            out = run("run.py", "email", R, "--id", eid, "--file", rb)
            self.assertIn("Email %s is right" % eid, out)
        # ---- send: messages (the greeting comes from the clock: Good morning, then Hi)
        chat = b.settings()["sitamah"]["chat"]
        for n, (mid, greet) in enumerate((("m1", "Good morning"), ("m2", "Hi"), ("m3", "Hi")), 1):
            out = run("run.py", "message", R, "--id", mid)
            self.assertIn("%s Sitamah, Claude here" % greet, out)
            text = msgs[n - 1]["text"].replace(b.GREETING_MARK, greet)
            rbm = os.path.join(d, "rbm_%s.json" % mid)
            if mid == "m1":
                jwrite(rbm, {"body": {"content": text.replace("\n", "<br>")}})           # no real bold tag
                self.receipt(R, "message.m1.chat", chat)
                self.receipt(R, "message.m1.format", "markdown")
                self.assertIn("real bold", run("run.py", "messagecheck", R, "--id", "m1", "--file", rbm, expect=5))
            jwrite(rbm, html_message(text))
            self.receipt(R, "message.%s.chat" % mid, chat)
            self.receipt(R, "message.%s.format" % mid, "markdown")
            self.assertIn("reads right", run("run.py", "messagecheck", R, "--id", mid, "--file", rbm))
        self.assertIn("Nothing needed from you.", msgs[2]["text"])
        self.assertIn("Medical Aid: Medical aid referral sent to Valerie", msgs[2]["text"])
        self.assertNotIn("Follow-up Teams invite", msgs[2]["text"])           # the invite skill already told her itself
        out = run("run.py", "checkin", R)
        self.assertIn("2026-11-20T08:00:00[Africa/Johannesburg]", out)
        self.receipt(R, "checkin.trigger_id", "trig_test_1")
        run("run.py", "done", R, "send")
        # ---- publish: a page that is not the program's is refused, then the real one passes
        good = readf(os.path.join(R, "out", "board.html"))
        rbp = os.path.join(d, "published.html")
        with open(rbp, "w", encoding="utf-8", newline="") as f:
            f.write(good.replace("Life cover needed: R2 000 000", "Life cover needed: R3 000 000"))
        self.assertIn("NOT what the program built", run("run.py", "publish", R, "--url", "https://claude.ai/artifact/test-board", "--file", rbp, expect=5))
        with open(rbp, "w", encoding="utf-8", newline="") as f:
            f.write(good)
        run("run.py", "publish", R, "--url", "https://claude.ai/artifact/test-board", "--file", rbp)
        self.receipt(R, "publish.result", "published, version 1")
        run("run.py", "done", R, "publish")
        out = run("run.py", "done", R, "final")
        self.assertIn("RESULT: PASS", out)
        self.assertFalse([l for l in out.splitlines() if l.startswith("❌")], out)
        self.assertIn("Only attested (not proven):", out)
        self.assertEqual(run("verify.py", R).count("RESULT: PASS"), 1)
        # ---- a page edited by hand after the run is caught by the final checker
        R2x = os.path.join(d, "run1_tampered")
        shutil.copytree(R, R2x)
        p = os.path.join(R2x, "out", "board.html")
        with open(p, "a", encoding="utf-8") as f:
            f.write("<!-- edited by hand -->\n")
        out = run("verify.py", R2x, expect=1)
        self.assertIn("❌ The page is exactly what the program draws".replace("The page is exactly what the program draws", "out/board.html is missing or is not what the program draws"), out)
        # a board.json edited by hand is caught too
        R3x = os.path.join(d, "run1_tampered2")
        shutil.copytree(R, R3x)
        bj = jread(os.path.join(R3x, "board.json"))
        bj["cards"]["life_cover"]["identified"][0]["text"] = "Sum assured R5 000 000"
        jwrite(os.path.join(R3x, "board.json"), bj)
        self.assertIn("RESULT: FAIL", run("verify.py", R3x, expect=1))
        self.board_html = os.path.join(R, "out", "board.html")

    # ------------------------------------------------------------------ the second run: the board is read back and changed
    def second_run(self, d):
        R = os.path.join(d, "run2")
        run("run.py", "start", R, "--client", "Pat Samplecase")
        run("run.py", "access", R, "--purpose", "board", "--route", "artifact", "--result", "found", "--note", "the board is in the Artifact list")
        # a base edited by hand is refused
        html = readf(self.board_html)
        bad = os.path.join(d, "bad_base.html")
        with open(bad, "w", encoding="utf-8", newline="") as f:
            f.write(html.replace("Sum assured R2 000 000", "Sum assured R9 000 000"))
        self.assertIn("checksum", run("run.py", "base", R, "--file", bad, "--url", "https://claude.ai/artifact/test-board", expect=5))
        # a board of another client is refused
        other = os.path.join(d, "other_run")
        run("run.py", "start", other, "--client", "Robin Testcase")
        run("run.py", "access", other, "--purpose", "board", "--route", "artifact", "--result", "found", "--note", "x")
        self.assertIn("not Robin Testcase", run("run.py", "base", other, "--file", self.board_html, "--url", "https://claude.ai/artifact/test-board", expect=5))
        run("run.py", "base", R, "--file", self.board_html, "--url", "https://claude.ai/artifact/test-board")
        run("run.py", "done", R, "locate")
        self.receipt(R, "quote.life.received", "FNA quote PDF saved in Comparative Quotes")
        ch = {"ops": [{"op": "pending_clear", "card": "life_cover"},
                      {"op": "action", "card": "life_cover", "text": "FNA quote received from Lizelle", "receipt": "quote.life.received"}]}
        cpath = os.path.join(d, "change2.json")
        jwrite(cpath, ch)
        run("run.py", "change", R, "--file", cpath)
        run("run.py", "done", R, "change")
        run("run.py", "route", R)
        run("run.py", "done", R, "route")
        run("run.py", "build", R)
        run("run.py", "done", R, "build")
        out = run("run.py", "show", R)
        self.assertIn("message Sitamah on Teams (1)", out)
        run("run.py", "approve", R, "--said", "Yes")
        run("run.py", "done", R, "confirm")
        text = jread(os.path.join(R, "out", "messages.json"))[0]["text"]
        self.assertIn("Life Cover: FNA quote received from Lizelle", text)
        run("run.py", "message", R, "--id", "m1", "--used-today", "yes")
        chat = b.settings()["sitamah"]["chat"]
        rbm = os.path.join(d, "rbm2.json")
        jwrite(rbm, html_message(text.replace(b.GREETING_MARK, "Hi")))
        self.receipt(R, "message.m1.chat", chat)
        self.receipt(R, "message.m1.format", "markdown")
        run("run.py", "messagecheck", R, "--id", "m1", "--file", rbm)
        out = run("run.py", "checkin", R)
        self.assertIn("No follow-up date", out)
        run("run.py", "done", R, "send")
        page = os.path.join(R, "out", "board.html")
        run("run.py", "publish", R, "--url", "https://claude.ai/artifact/test-board", "--file", page)
        self.receipt(R, "publish.result", "published, version 2")
        run("run.py", "done", R, "publish")
        out = run("run.py", "done", R, "final")
        self.assertIn("RESULT: PASS", out)
        st = bh.extract_state(readf(page))
        self.assertEqual(len(st["change_log"]), 2)
        self.assertEqual(st["change_log"][0]["date"], "05/11/2026")
        self.assertIsNone(st["cards"]["life_cover"]["pending"])
        self.assertEqual(len(st["cards"]["life_cover"]["actions"]), 3)           # the invite, the quote request, the quote received
        self.assertEqual(st["cards"]["fact_find"]["next_appointment"]["date"], "20/11/2026")

    # ------------------------------------------------------------------ the third run: a reschedule needs its cancelled check-in; close-out
    def third_run(self, d):
        R = os.path.join(d, "run3")
        run("run.py", "start", R, "--client", "Pat Samplecase")
        run("run.py", "access", R, "--purpose", "board", "--route", "artifact", "--result", "found", "--note", "the board is in the Artifact list")
        run("run.py", "base", R, "--file", os.path.join(d, "run2", "out", "board.html"), "--url", "https://claude.ai/artifact/test-board")
        run("run.py", "done", R, "locate")
        self.receipt(R, "skill.teams.run2", "PASS")
        move = {"ops": [{"op": "followup", "date": "27/11/2026", "time": "10:00", "source": "Paul: the client asked to move it", "via": "teams-meeting-setup-skill",
                         "receipt": "skill.teams.run2", "reschedule": True}]}
        mpath = os.path.join(d, "move.json")
        jwrite(mpath, move)
        self.assertIn("checkin.deleted", run("run.py", "change", R, "--file", mpath, expect=5))
        self.receipt(R, "checkin.deleted", "trig_test_1 deleted")
        run("run.py", "change", R, "--file", mpath)
        # closing needs Paul's words and the cancelled check-ins
        close = {"ops": [{"op": "close", "status": "NTU", "paul_said": "Yes, close it, she declined everything"}]}
        cpath = os.path.join(d, "close.json")
        jwrite(cpath, close)
        self.assertIn("closeout.triggers_cancelled", run("run.py", "change", R, "--file", cpath, expect=5))
        self.receipt(R, "closeout.triggers_cancelled", "none left")
        run("run.py", "change", R, "--file", cpath)
        run("run.py", "done", R, "change")
        run("run.py", "route", R)
        run("run.py", "done", R, "route")
        run("run.py", "build", R)
        run("run.py", "done", R, "build")
        page = readf(os.path.join(R, "out", "board.html"))
        self.assertIn('class="banner-closed">CLOSED - NTU - 05/11/2026', page)
        out = run("run.py", "show", R)
        self.assertIn("Ready to republish Pat Samplecase's board?", out)
        run("run.py", "approve", R, "--said", "Yes")
        run("run.py", "done", R, "confirm")
        run("run.py", "done", R, "send")                  # no email, no message and no follow-up date in this run
        run("run.py", "publish", R, "--url", "https://claude.ai/artifact/test-board", "--file", os.path.join(R, "out", "board.html"))
        self.receipt(R, "publish.result", "published, version 3")
        run("run.py", "done", R, "publish")
        self.assertIn("RESULT: PASS", run("run.py", "done", R, "final"))
        # a closed board refuses any further change
        R4 = os.path.join(d, "run4")
        run("run.py", "start", R4, "--client", "Pat Samplecase")
        run("run.py", "access", R4, "--purpose", "board", "--route", "artifact", "--result", "found", "--note", "x")
        run("run.py", "base", R4, "--file", os.path.join(R, "out", "board.html"), "--url", "https://claude.ai/artifact/test-board")
        again = {"ops": [{"op": "prospect_log", "date": "05/11/2026", "text": "Called again"}]}
        apath = os.path.join(d, "again.json")
        jwrite(apath, again)
        self.assertIn("the board is closed", run("run.py", "change", R4, "--file", apath, expect=5))


if __name__ == "__main__":
    unittest.main()
