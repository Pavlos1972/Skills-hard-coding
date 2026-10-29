"""Paul's answers after his first real-case trial (29/10/2026): short notes, sorted actions, the message to Sitamah shown with the outputs.

Every rule here is something he removed or asked for. Invented people and figures only.
"""
import json
import os
import subprocess
import sys
import unittest

from test_gate import Base, SCRIPTS, sh, slurp

sys.path.insert(0, SCRIPTS)
import verify  # noqa: E402

SKILL_DIR = os.path.dirname(SCRIPTS)


def pdf_text(run_out):
    pdf = [f for f in os.listdir(run_out) if f.endswith(".pdf")][0]
    return subprocess.run(["pdftotext", os.path.join(run_out, pdf), "-"], capture_output=True, text=True).stdout


class ShortNotes(Base):
    def test_planner_note_shows_only_one_liners_and_the_actions_for_now(self):
        self.to_built()
        note = slurp(self.p("out", "planner_note.txt"))
        self.assertIn("Credit life on the Absa home loan, about R500 p.m.", note)               # the one-liner is shown
        self.assertNotIn("the details are still to be obtained from Sam", note)               # the long PDF line is not
        self.assertIn("Sitamah to get the credit-life details from Sam", note)                # an action for now is shown
        self.assertNotIn("send Sam the cession documents", note)                              # an action that waits is not

    def test_the_pdf_has_the_full_text_and_lists_the_waiting_action_under_coming_up(self):
        self.to_built()
        txt = pdf_text(self.p("out"))
        self.assertIn("the details are still to be obtained from Sam", txt)
        self.assertIn("Action Points", txt)
        self.assertIn("Coming up", txt)
        flat = " ".join(txt.split())                                   # the PDF wraps long lines
        self.assertIn("send Sam the cession documents to sign", flat)
        self.assertIn("once the BrightRock policy is issued", flat)
        self.assertLess(txt.index("Action Points"), txt.index("Coming up"))
        self.assertLess(txt.index("Coming up"), txt.index("Next Steps"))

    def test_a_planner_one_liner_over_twenty_words_fails(self):
        long = "BrightRock quote CP 100000001 at R1,100.00 p.m. " + "with a lot of extra words that make this much longer than one line " * 2
        r = self.mutate_content(lambda c: c["areas"][0]["bullets"][0].update(short=long))
        self.assertFails(r, "Planner one-liner b1 is", "at most 20")

    def test_more_than_three_one_liners_in_an_area_fails(self):
        def f(c):
            c["areas"][0]["bullets"].append({"id": "b9", "text": "Extra risk point", "short": "Extra risk point", "status": "still open",
                                             "src": [self.src("one thousand one hundred rand a month")]})
        self.assertFails(self.mutate_content(f), "4 Planner one-liners, at most 3")

    def test_an_area_with_bullets_but_no_one_liner_fails(self):
        r = self.mutate_content(lambda c: c["areas"][3]["bullets"][0].pop("short"))
        self.assertFails(r, "Will: no Planner one-liner")

    def test_a_pdf_bullet_over_forty_five_words_fails(self):
        r = self.mutate_content(lambda c: c["areas"][0]["bullets"][1].update(text="Instalment Protector on the Absa home loan " + "and some more plain words " * 12))
        self.assertFails(r, "PDF bullet b2 is", "at most 45")

    def test_more_than_four_bullets_in_an_area_in_the_pdf_fails(self):
        def f(c):
            for i in range(2):
                c["areas"][0]["bullets"].append({"id": "x%d" % i, "text": "Extra risk point %d" % i, "status": "still open",
                                                 "src": [self.src("one thousand one hundred rand a month")]})
        self.assertFails(self.mutate_content(f), "5 bullets in the PDF, at most 4")

    def test_an_application_needs_its_own_one_liner(self):
        def f(c):
            c["applications"].append({"id": "p1", "text": "BrightRock application is only partly filled", "status": "still open",
                                      "src": [self.src("one thousand one hundred rand a month")]})
        self.assertFails(self.mutate_content(f), "application p1 needs a `short`")

    def test_a_long_opening_sentence_fails(self):
        r = self.mutate_content(lambda c: c.update(opening="This follow-up meeting covered " + "many different and very long topics " * 10))
        self.assertFails(r, "the opening sentence is")

    def test_a_figure_in_a_one_liner_must_be_in_its_sources(self):
        r = self.mutate_content(lambda c: c["areas"][0]["bullets"][0].update(short="BrightRock Revised Reduced Quote CP 100000001, R9,999.00 p.m."))
        self.assertFails(r, "its Planner one-liner (short) states figures")

    def test_a_pdf_of_more_than_two_pages_fails(self):
        self.to_ready()
        c = self.content()
        for i in range(70):
            c["since_last"].append({"id": "s%d" % (i + 2), "tag": "Changed", "text": "Another change since the last meeting, point number %d" % i,
                                    "src": [self.src("rather put it in my name for now")]})
        self.write("content.json", c)
        sh("build.py", self.run_dir, ok=True)
        r = self.verify("built")
        self.assertFails(r, "the PDF is", "Paul wants at most 2")

    def test_the_sample_content_passes_the_new_group(self):
        self.to_ready()
        r = self.verify("pre")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("L. Short notes and sorted actions", r.stdout)
        self.assertIn("Planner note short", r.stdout)


def structure(actions=None, next_steps=None):
    R = verify.Results()
    verify.check_structure({"meeting_type": "followup", "areas": [], "applications": [], "since_last": [],
                            "actions": actions or [], "next_steps": next_steps or []}, R)
    return R


def act(text, when="now", trigger=None, i="a1"):
    a = {"id": i, "text": text, "when": when}
    if trigger:
        a["trigger"] = trigger
    return a


class SortedActions(Base):
    """Paul's ten answers on the household's action list, with invented stand-ins for each action."""

    def test_the_four_actions_paul_kept_pass(self):
        for text in ("Sitamah to follow up with Capital Legacy: the clients say it never called them",         # 1: yes
                     "Sitamah to get the full policy schedules from the insurer",                                # 3: yes
                     "Sitamah to get the credit-life details from the clients",                                  # 5: yes
                     "Sitamah to get updated BrightRock quotes with the settled loan removed"):                  # 8: yes
            R = structure([act(text)])
            self.assertEqual(R.fails, [], text)

    def test_the_cession_waits_until_the_policy_is_issued(self):                                                  # 4: after policy issue
        R = structure([act("Sitamah to arrange for the instalment protectors to be ceded to the lenders", "later", "once the policy is issued")])
        self.assertEqual(R.fails, [])

    def test_a_client_decision_is_not_an_action(self):                                                           # 6: remove
        R = structure([act("Sitamah to ask the clients what they want to do about the credit life")])
        self.assertTrue(any("what the client decides" in m for _, _, m in R.fails), R.rows)

    def test_cancelling_credit_life_is_not_an_action(self):                                                      # 7: remove
        R = structure([act("Sitamah to cancel the credit life once the new policy is in force")])
        self.assertTrue(any("cancelling credit life" in m for _, _, m in R.fails), R.rows)

    def test_sending_the_updated_quotes_is_not_an_action(self):                                                  # 9: remove, another step does it
        R = structure([act("Sitamah to send the updated quotes to the clients")])
        self.assertTrue(any("sending quotes" in m for _, _, m in R.fails), R.rows)

    def test_setting_up_the_next_appointment_is_not_an_action(self):                                             # 10: remove
        R = structure([act("Sitamah to set up another evening appointment for early next week")])
        self.assertTrue(any("setting up the next meeting" in m for _, _, m in R.fails), R.rows)

    def test_a_what_if_question_to_a_provider_is_warned_about(self):                                             # 2: remove (no stated reason)
        R = structure([act("Sitamah to check with the insurer whether the income protector would still pay on a lower income")])
        self.assertEqual(R.fails, [])
        self.assertTrue(any(lvl == "WARN" and "what-if" in m for lvl, _, m in R.rows), R.rows)

    def test_the_rules_do_not_catch_ordinary_actions(self):
        for text in ("Sitamah to put a review of Dana's portfolio in the what's-next email",
                     "Sitamah to send Sam the cession documents to sign",
                     "Sitamah to arrange for Valerie to contact the client about the medical aid",
                     "Sitamah to ask Paul to approve the draft email before it goes out",
                     "Sitamah to request the revised Tax-Free quote from Alwyn",
                     "Sitamah to email Alwyn to request a revised quote in Sam's name",
                     "Sitamah to send the revised quote request to Alwyn"):
            self.assertEqual(structure([act(text)]).fails, [], text)

    def test_more_ways_of_writing_the_removed_actions_are_caught(self):
        for text in ("Sitamah to send the what's-next email to Sam",
                     "Sitamah to book the meeting invite for Thursday",
                     "Sitamah to ask Sam whether he wants the Tax-Free in his name",
                     "Sitamah to cancel the credit life on the Absa home loan",
                     "Sitamah to email the proposals to the clients",
                     "Sitamah to forward the updated quotes to Sam and Dana"):
            self.assertTrue(structure([act(text)]).fails, text)

    def test_an_action_without_when_fails(self):
        R = structure([{"id": "a1", "text": "Sitamah to get the policy schedules"}])
        self.assertTrue(any("must say when" in m for _, _, m in R.fails))

    def test_a_later_action_needs_its_trigger(self):
        R = structure([act("Sitamah to arrange for the loan to be ceded to the bank", "later")])
        self.assertTrue(any("say what it waits for" in m for _, _, m in R.fails))

    def test_at_most_eight_actions_for_now(self):
        R = structure([act("Sitamah to get document number %d from the insurer" % i, i="a%d" % i) for i in range(9)])
        self.assertTrue(any("9 actions for now, at most 8" in m for _, _, m in R.fails))

    def test_an_action_over_twenty_five_words_fails(self):
        R = structure([act("Sitamah to get the schedules " + "and many more plain words " * 8)])
        self.assertTrue(any("at most 25" in m for _, _, m in R.fails))

    def test_the_cession_action_must_be_a_later_action(self):
        r = self.mutate_content(lambda c: c["actions"][1].update(when="now"))
        self.assertFails(r, "AFTER the policy is issued")

    def test_next_steps_are_the_clients_only(self):
        R = structure(next_steps=[{"id": "n1", "text": "Paul will send the updated quotes and phone Sam on Friday", "owner": "client"}])
        self.assertTrue(any("names Paul as the owner" in m for _, _, m in R.fails))
        R = structure(next_steps=[{"id": "n1", "text": "Sam to speak to Dana"}])
        self.assertTrue(any('needs owner "client"' in m for _, _, m in R.fails))
        R = structure(next_steps=[{"id": "n1", "text": "Sam to speak to Dana", "owner": "paul"}])
        self.assertTrue(any('needs owner "client"' in m for _, _, m in R.fails))


class MessageShownWithTheOutputs(Base):
    """The first real run never offered the Teams message: the rules said to show it only after Paul had approved everything."""

    def steps(self):
        return {s["id"]: s for s in json.loads(slurp(os.path.join(SKILL_DIR, "steps.json")))["steps"]}

    def test_the_chat_must_not_end_its_reply_before_the_message_is_shown(self):
        st = self.steps()
        for sid in ("planner", "pdf", "handoffs"):
            self.assertIn("Do NOT end your reply here", st[sid]["do"][0], sid)
        joined = " ".join(st["teams"]["do"])
        self.assertIn("Never end a reply without the message in it", joined)
        self.assertIn("Shall I post this message to Sitamah in Teams?", joined)
        self.assertIn("one question", joined.lower().replace("ONE question".lower(), "one question"))
        self.assertNotIn("Only after every deliverable is approved", joined)

    def test_the_rules_page_no_longer_says_to_wait_for_approval_first(self):
        text = slurp(os.path.join(SKILL_DIR, "references", "07-teams-message.md"))
        self.assertNotIn("approved by Paul and SAVED", text)
        self.assertIn("SHOWN in the same reply as the Planner page and the PDF", text)
        self.assertIn("It is SENT only after his yes", text)

    def test_the_entry_page_and_rules_say_it_too(self):
        self.assertIn("same reply as the page and the PDF", slurp(os.path.join(SKILL_DIR, "SKILL.md")))
        self.assertIn("same reply as the Planner page and the PDF", slurp(os.path.join(SKILL_DIR, "references", "00-rules.md")))

    def test_the_content_step_teaches_the_new_structure(self):
        joined = " ".join(self.steps()["content"]["do"])
        for must in ("`short`", "at most 45 words", "at most 20 words", '"when": "now"', '"when": "later"', '"trigger"',
                     "what the client decides", "cancelling credit life", "owner\": \"client\""):
            self.assertIn(must, joined)


if __name__ == "__main__":
    unittest.main()
