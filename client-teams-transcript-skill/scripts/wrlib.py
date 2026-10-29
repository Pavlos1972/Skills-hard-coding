"""Shared helpers for the client-teams-transcript scripts (stdlib only)."""
import datetime as dt
import hashlib
import json
import os
import re
import sys

# Chunking: the skill asks for about 400-450 lines per read. The character cap
# keeps one chunk inside a tool-output limit, so a chunk is never silently cut.
CHUNK_LINES = int(os.environ.get("WR_CHUNK_LINES", "400"))
CHUNK_CHARS = int(os.environ.get("WR_CHUNK_CHARS", "24000"))

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TRANSCRIPT = "transcript.txt"
STATE = "state.json"
LEDGER = "ledger.json"
CONTENT = "content.json"
RECEIPT = "receipt.json"
SOURCES = "sources.json"
ACCESS = "access_log.json"
QUESTIONS = "questions.json"
RUN = "run.json"
OUT = "out"
DOCS = "docs"

# Access routes in the order they must be tried (SKILL-STANDARDS.md S4).
ROUTES = ("device", "m365", "zapier")
ROUTE_NAMES = {
    "device": "local drive / OneDrive through the device bridge",
    "m365": "Microsoft 365 connector (SharePoint/OneDrive, Outlook, Teams transcripts)",
    "zapier": "Zapier (Office 365 and Teams tools)",
}

# Kinds of client-file source and which meeting types must account for each (S3).
SOURCE_KINDS = ["Fact Find", "Fact Find Summary", "Earlier Note", "Overview", "Quote", "Application", "Correspondence"]
REQUIRED_SOURCE_KINDS = {
    "followup": SOURCE_KINDS,
    "whatsapp": SOURCE_KINDS,
    "first": [],
}

DOC_TYPES = [
    "Overview", "Quote", "Fact Find", "Fact Find Summary", "Earlier Note",
    "Application", "Correspondence", "Paul (chat)",
]

STATUS_WORDS = [
    "accepted (verbal)", "accepted (verbal + email", "pending - client deciding",
    "pending – client deciding", "changed:", "changed", "awaiting", "still open",
    "resolved", "requested", "on hold", "declined",
]
TAG_WORDS = ["resolved", "still open", "new", "changed"]
STATUS_WORDS += ["verbally confirmed - awaiting email reply to proposal", "verbally confirmed", "accepted"]

# A follow-up appointment is real only with a specific date/time; vague wording is not an appointment.
AGREED_RE = re.compile(
    r"\b\d{1,2}[/.]\d{1,2}(?:[/.]\d{2,4})?\b"
    r"|\b(?:mon|tues?|wed(?:nes)?|thu(?:rs)?|fri|sat(?:ur)?|sun)(?:day)?\b.*\b\d{1,2}(?::\d{2})?\s?(?:am|pm)\b"
    r"|\b\d{1,2}(?:st|nd|rd|th)?\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)", re.I)
VAGUE_RE = re.compile(
    r"date to be set|to be set|\btbc\b|to be confirmed|sometime|we'?ll chat|will chat|revisit|early next|later (?:this|next)|"
    r"next (?:week|month)|in (?:january|february|march|april|may|june|july|august|september|october|november|december)\b", re.I)

# Paul's eight planning areas (29/10/2026) plus "Other" (only when something notable was said).
# Each is its own heading, in this order, in the Planner note and the PDF.
# (area key, heading)
AREAS = [
    ("risk", "Risk"),
    ("ra", "RA"),
    ("investment", "Investment"),
    ("rgar", "RGAR"),
    ("egar", "EGAR"),
    ("medical", "Medical Aid"),
    ("will", "Will"),
    ("short_term", "Short-Term"),
    ("other", "Other"),
]
AREA_KEYS = [k for k, _ in AREAS]
AREA_HEADING = dict(AREAS)
EIGHT = [k for k, _ in AREAS if k != "other"]


CLIENT_STATUSES = ("Review Client", "Prospect")

# How short the outputs must be (Paul, after his first real-case trial: the Planner note was far too long).
# The Planner note shows only each bullet's one-line `short` text; the PDF shows its full `text`. verify.py fails a run that exceeds these.
LIMITS = {
    "planner_words": 20,        # words in one Planner one-liner (`short`), not counting its status word
    "planner_bullets": 3,       # one-liners per area in the Planner note
    "planner_actions": 8,       # actions for now in the Planner note
    "action_words": 25,         # words in one action
    "pdf_bullets": 4,           # bullets per area in the PDF
    "pdf_words": 45,            # words in one PDF bullet
    "since_words": 25,          # words in one "Since the last meeting" line
    "application_words": 30,    # words in one application line
    "opening_words": 40,        # words in the PDF's opening sentence
    "pdf_pages": 2,
}
ACTION_WHEN = ("now", "later")   # an action is for now, or it waits for something (its `trigger`)


def words(text):
    return len(str(text or "").split())


def parse_date(text):
    """DD/MM/YYYY -> date, or None."""
    try:
        return dt.datetime.strptime((text or "").strip(), "%d/%m/%Y").date()
    except ValueError:
        return None


def action_line(a):
    """The action as shown: its text, plus its due date when the text does not already carry it (one place, so both outputs agree)."""
    t = (a.get("text") or "").strip()
    due = (a.get("due") or "").strip()
    return t if not due or due in t else "%s \u2013 due %s" % (t, due)


def status_from_paths(sources):
    """Where the client's folder sits decides the label: Company - WR Clients = Review Client; Company - Paul\\New Business = Prospect."""
    paths = " ".join(str(e.get("path") or "") for e in sources if isinstance(e, dict) and e.get("read") == "yes").lower().replace("/", "\\")
    review = "company - wr clients" in paths or "paul kafentzis (client files)" in paths
    prospect = "company - paul" in paths and "new business" in paths
    return "Review Client" if review and not prospect else ("Prospect" if prospect and not review else None)


def ordinal(n):
    n = int(n)
    if 10 <= n % 100 <= 20:
        suf = "th"
    else:
        suf = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return "%d%s" % (n, suf)


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def skill_stamp():
    """'YYYY-MM-DD HH:MM' from the Last updated line of SKILL.md (set by tools/stamp_skill.py), or None."""
    try:
        with open(os.path.join(SKILL_DIR, "SKILL.md"), encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return None
    m = re.search(r"\*\*Last updated:\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2})", text)
    return m.group(1) if m else None


def skill_name():
    try:
        with open(os.path.join(SKILL_DIR, "SKILL.md"), encoding="utf-8") as f:
            m = re.search(r'^name:\s*"?([a-z0-9-]+)"?\s*$', f.read(), re.M)
        return m.group(1) if m else os.path.basename(SKILL_DIR)
    except OSError:
        return os.path.basename(SKILL_DIR)


def stamp_display(stamp):
    """'2026-10-29 13:18' -> '29/10/2026 13:18 (Athens time)' (house style, S13)."""
    try:
        return dt.datetime.strptime(stamp, "%Y-%m-%d %H:%M").strftime("%d/%m/%Y %H:%M") + " (Athens time)"
    except (TypeError, ValueError):
        return None


def version_short():
    """'client-teams-transcript-skill, last updated 29/10/2026 13:18 (Athens time)': taken from the stamp, never typed."""
    shown = stamp_display(skill_stamp())
    if shown:
        return "%s, last updated %s" % (skill_name(), shown)
    return "%s, NOT STAMPED (this copy has no valid Last updated line)" % skill_name()


def version_line():
    return "Using " + version_short()


def norm(s):
    """Lower-case, punctuation-free, single-spaced: for verbatim-quote matching."""
    s = s.lower()
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"')):
        s = s.replace(a, b)
    return " ".join(re.sub(r"[\W_]+", " ", s).split())


def sha256_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def die(msg, code=1):
    print(msg, file=sys.stderr)
    sys.exit(code)


def load_json(path, what=None):
    if not os.path.exists(path):
        die("MISSING: %s (%s)" % (what or os.path.basename(path), path))
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except ValueError as e:
        die("INVALID JSON in %s: %s" % (path, e))


def save_json(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def read_lines(run):
    with open(os.path.join(run, TRANSCRIPT), encoding="utf-8") as f:
        return f.read().split("\n")


def content_hash(content):
    return sha256_text(json.dumps(content, sort_keys=True, ensure_ascii=False))


def all_items(content):
    """Yield (list_name, item) for every sourced item in content.json."""
    for name in ("since_last", "applications", "actions", "next_steps"):
        for it in content.get(name) or []:
            if isinstance(it, dict):
                yield name, it
    for area in content.get("areas") or []:
        if not isinstance(area, dict):
            continue
        for it in area.get("bullets") or []:
            if isinstance(it, dict):
                yield "areas:" + str(area.get("key")), it
    na = content.get("next_appointment")
    if isinstance(na, dict):
        yield "next_appointment", na


def short_date(d):
    """DD/MM/YYYY -> DD.MM.YY"""
    m = re.fullmatch(r"(\d{2})/(\d{2})/(\d{4})", d or "")
    if not m:
        return None
    return "%s.%s.%s" % (m.group(1), m.group(2), m.group(3)[2:])


def output_names(content):
    """Exact deliverable filename + planner-note pointer, derived (never typed)."""
    c = content.get("client") or {}
    first, sur = (c.get("first") or "").strip(), (c.get("surname") or "").strip()
    sd = short_date(content.get("meeting_date"))
    mt = content.get("meeting_type")
    if not (first and sur and sd):
        return None
    if mt == "followup":
        stem = "Follow-Up Appointment Summary Notes - %s - (%s, %s)" % (sd, sur, first)
    elif mt == "whatsapp":
        stem = "WhatsApp Call Summary - %s - (%s, %s)" % (sd, sur, first)
    elif mt == "first":
        stem = None
    else:
        return None
    ff = "Fact Find Summary - %s - (%s %s)" % (sd, first, sur)
    return {"pdf_stem": stem, "pdf": (stem + ".pdf") if stem else None, "ff_summary_stem": ff,
            "page": "planner_note.html", "note_txt": "planner_note.txt", "teams": "teams_message.txt"}
