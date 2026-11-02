"""Shared helpers for the ff-population-transcript scripts (stdlib only, except build.py which needs reportlab)."""
import datetime as dt
import hashlib
import json
import os
import re
import sys
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

# Chunking: about 400 lines per read; the character cap keeps one chunk inside a tool-output limit.
CHUNK_LINES = int(os.environ.get("WR_CHUNK_LINES", "400"))
CHUNK_CHARS = int(os.environ.get("WR_CHUNK_CHARS", "24000"))

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))

# files inside a run folder
TRANSCRIPT = "transcript.txt"
STATE = "state.json"
LEDGER = "ledger.json"
CONTENT = "content.json"
RECEIPT = "receipt.json"
SOURCES = "sources.json"
ACCESS = "access_log.json"
QUESTIONS = "questions.json"
RUN = "run.json"
FORM = "form_read.json"
CROSS = "crosscheck.json"
OVERLAY = "overlay.json"
CLAIMS = "claims.json"
LEAD = "lead.json"
FORMPDF = "form_pdf.json"
PARTS = "parts.json"
OUT = "out"
DOCS = "docs"

# Access routes in the order they must be tried (SKILL-STANDARDS.md S4). The time of day never changes this (Paul, 02/11/2026).
ROUTES = ("device", "m365", "zapier")
ROUTE_NAMES = {
    "device": "local drive / OneDrive through the device bridge",
    "m365": "Microsoft 365 connector (SharePoint/OneDrive, Outlook, Teams transcripts)",
    "zapier": "Zapier (Office 365 and Teams tools)",
}

# Kinds of client-file source. The form's data file and the transcript are recorded through the access log and the
# form/prep steps; these are the documents read besides them.
SOURCE_KINDS = ["Overview", "Policy schedule", "Other document", "Correspondence", "Manual Fact Find"]
REQUIRED_SOURCE_KINDS = ["Overview"]
DOC_TYPES = SOURCE_KINDS + ["Paul (chat)"]

# the word forms a quote request must carry (Paul, 15/10/2026: no default, ever)
MODE_WORDS = ("new business", "servicing")

SCHEMA = "3.0"

MONTHS_SHORT = None


def words(text):
    return len(str(text or "").split())


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def parse_date(text):
    """DD/MM/YYYY -> date, or None."""
    try:
        return dt.datetime.strptime((text or "").strip(), "%d/%m/%Y").date()
    except ValueError:
        return None


def short_date(d):
    """DD/MM/YYYY -> DD.MM.YY"""
    m = re.fullmatch(r"(\d{2})/(\d{2})/(\d{4})", d or "")
    if not m:
        return None
    return "%s.%s.%s" % (m.group(1), m.group(2), m.group(3)[2:])


# ------------------------------------------------------------------ version stamp (S2)
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
    shown = stamp_display(skill_stamp())
    if shown:
        return "%s, last updated %s" % (skill_name(), shown)
    return "%s, NOT STAMPED (this copy has no valid Last updated line)" % skill_name()


def version_line():
    return "Using " + version_short()


# ------------------------------------------------------------------ text helpers
def norm(s):
    """Lower-case, punctuation-free, single-spaced: for verbatim-quote matching."""
    s = str(s).lower()
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"')):
        s = s.replace(a, b)
    return " ".join(re.sub(r"[\W_]+", " ", s).split())


def digits(s):
    return re.sub(r"\D", "", str(s or ""))


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


def load_opt(path, default):
    return load_json(path) if os.path.exists(path) else default


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


def layout():
    return load_json(os.path.join(SCRIPTS_DIR, "layout.json"), "layout.json")


# ------------------------------------------------------------------ money (the form writes 'R 24 000.00')
CENT = Decimal("0.01")


def parse_money(text):
    """'R 24 000.00' / 'R24,000.00' / '24000' / 'R 1 234,50' -> Decimal (2 places), or None when it is not an amount."""
    s = str(text or "").strip()
    if not s:
        return None
    s = s.replace(" ", " ")
    neg = s.startswith("-") or s.startswith("(")
    s = re.sub(r"^[Rr]\s*", "", s.lstrip("-(").strip()).rstrip(")").strip()
    s = re.sub(r"^[Rr]\s*", "", s)
    if not re.fullmatch(r"\d[\d ,.]*", s):
        return None
    s = s.replace(" ", "")
    if "," in s and "." in s:
        s = s.replace(",", "")                       # 24,000.00
    elif "," in s:
        head, _, tail = s.rpartition(",")
        s = (head.replace(",", "") + "." + tail) if len(tail) in (1, 2) else s.replace(",", "")
    elif s.count(".") > 1:
        s = s.replace(".", "")
    try:
        d = Decimal(s).quantize(CENT, rounding=ROUND_HALF_UP)
    except InvalidOperation:
        return None
    return -d if neg else d


def fmt_money(d):
    """Decimal -> 'R 24 000.00' (the form's own style)."""
    d = Decimal(d).quantize(CENT, rounding=ROUND_HALF_UP)
    neg = d < 0
    whole, frac = ("%.2f" % abs(d)).split(".")
    groups = []
    while whole:
        groups.insert(0, whole[-3:])
        whole = whole[:-3]
    return "%sR %s.%s" % ("-" if neg else "", " ".join(groups) or "0", frac)


def parse_pct(text):
    m = re.fullmatch(r"\s*(\d+(?:[.,]\d+)?)\s*%?\s*", str(text or ""))
    if not m:
        return None
    return Decimal(m.group(1).replace(",", "."))


def fmt_pct(d):
    d = Decimal(d)
    return ("%d%%" % d) if d == d.to_integral() else ("%s%%" % d.normalize())


def safe_filename(s):
    return re.sub(r'[\\/:*?"<>|]+', "", s).strip()


def output_names(first, surname, date_completed):
    """The one deliverable's file name, derived (never typed): Fact Find Transcript - DD.MM.YY - (Name Surname).pdf"""
    sd = short_date(date_completed)
    first, surname = (first or "").strip(), (surname or "").strip()
    if not (first and surname and sd):
        return None
    stem = "Fact Find Transcript - %s - (%s %s)" % (sd, first, surname)
    return {"pdf_stem": safe_filename(stem), "pdf": safe_filename(stem) + ".pdf"}
