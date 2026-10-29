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
OUT = "out"
DOCS = "docs"

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

# area key -> (PDF heading, Planner-note heading)
AREAS = [
    ("risk", "Risk Planning", "Risk"),
    ("retirement", "Retirement Planning", "Retirement (incl. RGAR)"),
    ("investment", "Investment Planning", "Investment (incl. EGAR)"),
    ("medical", "Medical Aid", "Medical Aid / Will / Short-Term"),
    ("will", "Will", "Medical Aid / Will / Short-Term"),
    ("short_term", "Short-Term Insurance", "Medical Aid / Will / Short-Term"),
    ("other", "Other", "Other"),
]
COMBINED_LABEL = {"medical": "Medical aid", "will": "Will", "short_term": "Short-term"}


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
    return {"pdf_stem": stem, "pdf": (stem + ".pdf") if stem else None, "ff_summary_stem": ff}
