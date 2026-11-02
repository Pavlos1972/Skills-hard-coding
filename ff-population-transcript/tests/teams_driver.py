"""Drives a REAL client-teams-transcript-skill run (type first) up to the step where it shows the message to Sitamah, on the invented call.

Used by the dry run: the Fact Find skill hands over to that program, and its checker looks at that run. Nothing of the Teams skill is changed;
its own scripts are run in their own folder, with their own environment (never this skill's WR_SCRIPTS).
"""
import json
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEAMS_DIR = os.path.join(REPO, "client-teams-transcript-skill")
TEAMS_RUN = os.path.join(TEAMS_DIR, "scripts", "run.py")
TEAMS_TX = os.path.join(TEAMS_DIR, "scripts", "tx.py")
TEAMS_VERIFY = os.path.join(TEAMS_DIR, "scripts", "verify.py")


def available():
    return os.path.exists(TEAMS_RUN)


def env():
    e = dict(os.environ, WR_CHUNK_LINES="25")
    e.pop("WR_SCRIPTS", None)
    return e


def run(script, *args, check=True):
    r = subprocess.run([sys.executable, script] + [str(a) for a in args], capture_output=True, text=True, env=env())
    if check and r.returncode != 0:
        raise AssertionError("%s %s -> %d\n%s\n%s" % (os.path.basename(script), args, r.returncode, r.stdout[-1500:], r.stderr[-800:]))
    return r


def jl(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def line_of(lines, text):
    for i, ln in enumerate(lines, 1):
        if text.lower() in ln.lower():
            return i
    raise AssertionError("fixture text not found: " + text)


def drive(run_dir, transcript, client=("Pat", "Samplecase"), date="05/11/2026", stop_before_teams=True):
    """Start the Teams run and take it through locate .. planner; it then shows the message (its `teams` step)."""
    first, sur = client
    run(TEAMS_RUN, "start", run_dir, "--type", "first", "--client", "%s %s" % (first, sur), "--date", date)
    run(TEAMS_RUN, "access", run_dir, "--need", "transcript", "--route", "passed", "--tool", "passed in by ff-population-transcript", "--result", "ok")
    run(TEAMS_RUN, "done", run_dir, "locate")
    run(TEAMS_TX, "prep", transcript, run_dir)
    run(TEAMS_RUN, "done", run_dir, "prep")
    with open(os.path.join(run_dir, "transcript.txt"), encoding="utf-8") as f:
        lines = f.read().split("\n")
    L = lambda t: line_of(lines, t)  # noqa: E731
    state = jl(os.path.join(run_dir, "state.json"))
    entries = [
        (L("ask BrightRock for a new business FNA quote"), "instruction", "ask BrightRock for a new business FNA quote", ["b1", "a1"]),
        (L("Retirement Goal Analysis"), "instruction", "ask for the Retirement Goal Analysis", ["b2", "a2"]),
        (L("letter of authority from you"), "request", "we also need a letter of authority from you", ["a3"]),
        (L("Thursday the twelfth at four works"), "decision", "Thursday the twelfth at four works", ["next", "a5"]),
        (L("I will email it tomorrow"), "acceptance", "I will email it tomorrow", ["n1"]),
        (L("credit life with Absa"), "fact", "there is credit life with Absa on the home loan", ["b3", "a4"]),
    ]
    # pass 1: each chunk gets its entries, or a reasoned acknowledgement
    for p_ in (1, 2):
        for n, (a, b) in enumerate(state["chunks"], 1):
            run(TEAMS_TX, "chunk", run_dir, p_, n)
            mine = [e for e in entries if a <= e[0] <= b]
            if p_ == 1 and mine:
                for ln, kind, quote, _ in mine:
                    run(TEAMS_RUN, "ledger", run_dir, "add", "--line", ln, "--kind", kind, "--quote", quote)
            else:
                run(TEAMS_RUN, "ledger", run_dir, "ack", "--pass", p_, "--chunk", n, "--reason", "read this chunk in full and checked it against the words; nothing more to record from it")
        run(TEAMS_RUN, "done", run_dir, "pass%d" % p_)
    scan = run(TEAMS_TX, "scan", run_dir).stdout
    led = jl(os.path.join(run_dir, "ledger.json"))
    near = [e["line"] for e in led["entries"]]
    for ln in scan.splitlines():
        parts = ln.split()
        if len(ln) > 3 and ln[:2] in ("C*", " *") and parts[1].isdigit():
            n = int(parts[1])
            if not any(abs(n - x) <= 3 for x in near):
                run(TEAMS_RUN, "ledger", run_dir, "review", "--line", n, "--reason", "plain talk at line %d, nothing was decided or asked here" % n)
    run(TEAMS_RUN, "done", run_dir, "scan")

    def s(text, min_len=10):
        return {"line": L(text), "quote": text}
    content = {
        "meeting_type": "first", "client": {"first": first, "surname": sur}, "meeting_date": date, "topic": "Fact Find: Risk, RA and next steps",
        "appointment_number": 1, "client_status": "Prospect", "client_status_basis": "the client's folder sits in Company - Paul\\New Business\\Samplecase, Pat",
        "appointment_number_basis": "no earlier meeting or file is on record for this prospect, so this is the first",
        "since_last": [],
        "areas": [
            {"key": "risk", "bullets": [
                {"id": "b1", "text": "BrightRock New Business FNA quote to be requested", "short": "BrightRock New Business FNA quote to be requested", "status": "requested",
                 "src": [s("ask BrightRock for a new business FNA quote")]},
                {"id": "b3", "text": "Credit life on the Absa home loan: details still to be obtained", "short": "Credit life on the Absa home loan: details to be obtained", "status": "still open",
                 "src": [s("there is credit life with Absa on the home loan")]},
            ]},
            {"key": "rgar", "bullets": [
                {"id": "b2", "text": "Retirement Goal Analysis to be requested", "short": "Retirement Goal Analysis to be requested", "status": "requested",
                 "src": [s("ask for the Retirement Goal Analysis") if False else s("I will also ask for the Retirement Goal Analysis")]},
            ]},
        ],
        "applications": [],
        "actions": [
            {"id": "a1", "when": "now", "text": "Sitamah to request the BrightRock New Business FNA quote for Pat", "src": [s("ask BrightRock for a new business FNA quote")]},
            {"id": "a2", "when": "now", "text": "Sitamah to request the Retirement Goal Analysis for Pat", "src": [s("I will also ask for the Retirement Goal Analysis")]},
            {"id": "a3", "when": "now", "text": "Sitamah to send Pat the letter of authority to sign", "src": [s("we also need a letter of authority from you")]},
            {"id": "a4", "when": "now", "text": "Sitamah to get the credit-life details from Pat", "src": [s("there is credit life with Absa on the home loan")]},
            {"id": "a5", "when": "now", "text": "Sitamah to set up the follow-up appointment for Thu 12/11/2026 at 4pm (send Pat the Teams meeting request)",
             "src": [s("Thursday the twelfth at four works")]},
        ],
        "next_steps": [{"id": "n1", "owner": "client", "text": "Pat to email the latest payslip", "src": [s("I will email it tomorrow")]}],
        "next_appointment": {"id": "next", "text": "Thu 12/11/2026 at 4pm", "agreed": True, "check": "Fact Find form and call both show Thu 12/11/2026 at 4pm: an agreed appointment",
                             "src": [s("Thursday the twelfth at four works")]},
        "checks": {
            "correspondence": {"done": False, "reason": "first meeting: no correspondence for this prospect yet"},
            "owner_change": {"occurred": False}, "cession": {"needed": False},
            "credit_life": {"debts_protected": True, "debts": [{"lender": "Absa", "credit_life": "yes"}], "bullet_id": "b3", "action_ids": ["a4"]},
            "applications": {"exist": False}, "quotes_matched": "n/a: no quotes exist yet at a first meeting",
        },
    }
    with open(os.path.join(run_dir, "content.json"), "w", encoding="utf-8") as f:
        json.dump(content, f, indent=1)
    for e in led["entries"]:
        for ln, kind, quote, items in entries:
            if e["line"] == ln:
                run(TEAMS_RUN, "ledger", run_dir, "cover", e["id"], *items)
    run(TEAMS_RUN, "done", run_dir, "content")
    run(TEAMS_VERIFY.replace("verify.py", "build.py"), run_dir)
    run(TEAMS_RUN, "done", run_dir, "build")
    sets = ["--set", "independent_check=subagent: re-read the call against both outputs; every name, figure and request matched"]
    for k in ("quotes_named", "benefits_from_quote", "nothing_to_confirm_on_file", "independent_actions", "garbled_flagged"):
        sets += ["--set", "judgment.%s=Checked, nothing to change: %s" % (k, k.replace("_", " "))]
    run(TEAMS_RUN, "receipt", run_dir, *sets)
    run(TEAMS_RUN, "done", run_dir, "check")
    run(TEAMS_RUN, "receipt", run_dir, "--set", "planner_page.mode=artifact", "--set", "planner_page.url=https://claude.ai/artifact/abc")
    run(TEAMS_RUN, "done", run_dir, "planner")          # the next step is `teams`: the message is shown, Paul has not answered yet
    return run_dir
