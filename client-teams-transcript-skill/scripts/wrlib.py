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
