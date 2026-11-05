"""Shared helpers for the fact-find-summary scripts (standard library only, except ffread.py / build.py, which need pdfplumber and reportlab)."""
import datetime as dt
import hashlib
import json
import os
import re
import sys
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))

# file names inside a run folder
RUN = "run.json"
STATE = "state.json"
ACCESS = "access_log.json"
RECEIPT = "receipt.json"
FACTFIND_PDF = "fact_find.pdf"
FACTFIND = "fact_find.json"
CONTENT = "content.json"
OUT = "out"

ROUTES = ("device", "m365", "zapier")
SOURCE_ROUTES = ROUTES + ("passed",)          # "passed": the PDF was handed over by ff-population-transcript in the same chat
ROUTE_NAMES = {"device": "the computer, only if this chat is ALREADY connected to it (checked, never requested)",
               "m365": "the Microsoft 365 connector (SharePoint / OneDrive)",
               "zapier": "the Zapier Office 365 tools"}
OWNERS = ("Cameron", "CL", "Valerie", "Lizelle")          # Paul, 03/11/2026: Lizelle replaces Martin
ADVISOR = "Paul Kafentzis"


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def parse_date(text):
    try:
        return dt.datetime.strptime((text or "").strip(), "%d/%m/%Y").date()
    except ValueError:
        return None


def short_date(d):
    m = re.fullmatch(r"(\d{2})/(\d{2})/(\d{4})", d or "")
    return "%s.%s.%s" % (m.group(1), m.group(2), m.group(3)[2:]) if m else None


# ---- version stamp (S2): the date is set by tools/stamp_skill.py, never typed
def skill_stamp():
    try:
        with open(os.path.join(SKILL_DIR, "SKILL.md"), encoding="utf-8") as f:
            m = re.search(r"\*\*Last updated:\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2})", f.read())
        return m.group(1) if m else None
    except OSError:
        return None


def skill_name():
    try:
        with open(os.path.join(SKILL_DIR, "SKILL.md"), encoding="utf-8") as f:
            m = re.search(r'^name:\s*"?([a-z0-9-]+)"?\s*$', f.read(), re.M)
        return m.group(1) if m else os.path.basename(SKILL_DIR)
    except OSError:
        return os.path.basename(SKILL_DIR)


def stamp_display(stamp):
    try:
        return dt.datetime.strptime(stamp, "%Y-%m-%d %H:%M").strftime("%d/%m/%Y %H:%M") + " (Athens time)"
    except (TypeError, ValueError):
        return None


def version_short():
    shown = stamp_display(skill_stamp())
    return "%s, last updated %s" % (skill_name(), shown) if shown else "%s, NOT STAMPED (no valid Last updated line)" % skill_name()


def version_line():
    return "Using " + version_short()


# ---- text and file helpers
def norm(s):
    s = str(s).lower()
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("–", "-"), ("—", "-")):
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


def content_hash(content):
    return sha256_text(json.dumps(content, sort_keys=True, ensure_ascii=False))


# ---- money: the Fact Find writes 'R 24 000.00'
CENT = Decimal("0.01")


def parse_money(text):
    """'R 24 000.00' / 'R24,000.00' / '24000' -> Decimal (2 places), or None when it is not an amount or is ambiguous ('R 2.000')."""
    s = str(text or "").strip().replace(" ", " ")
    if not s:
        return None
    neg = s.startswith("-") or s.startswith("(")
    s = re.sub(r"^[Rr]\s*", "", s.lstrip("-(").strip()).rstrip(")").strip()
    s = re.sub(r"^[Rr]\s*", "", s)
    if not re.fullmatch(r"\d[\d ,.]*", s):
        return None
    s = s.replace(" ", "")
    if "," in s and "." in s:
        s = s.replace(",", "") if s.rfind(".") > s.rfind(",") else s.replace(".", "").replace(",", ".")
    elif "," in s:
        head, _, tail = s.rpartition(",")
        if s.count(",") > 1 or len(tail) == 3:
            s = s.replace(",", "")
        elif len(tail) in (1, 2):
            s = head + "." + tail
        else:
            return None
    elif "." in s:
        head, _, tail = s.rpartition(".")
        if s.count(".") > 1:
            s = s.replace(".", "")
        elif len(tail) not in (1, 2):
            return None
    try:
        d = Decimal(s).quantize(CENT, rounding=ROUND_HALF_UP)
    except InvalidOperation:
        return None
    return -d if neg else d


def fmt_money(d):
    d = Decimal(d).quantize(CENT, rounding=ROUND_HALF_UP)
    whole, frac = ("%.2f" % abs(d)).split(".")
    groups = []
    while whole:
        groups.insert(0, whole[-3:])
        whole = whole[:-3]
    return "%sR %s.%s" % ("-" if d < 0 else "", " ".join(groups) or "0", frac)


# ---- the programs must not change during a run
FINGERPRINT_FILES = ("steps.json", "deliverables.json")


def program_fingerprint():
    h = hashlib.sha256()
    paths = [os.path.join(SKILL_DIR, f) for f in FINGERPRINT_FILES]
    for d in ("scripts", "references"):
        for root, dirs, files in os.walk(os.path.join(SKILL_DIR, d)):
            dirs[:] = sorted(x for x in dirs if x != "__pycache__")
            paths += [os.path.join(root, f) for f in sorted(files) if not f.endswith(".pyc")]
    for path in sorted(paths):
        if os.path.exists(path):
            with open(path, "rb") as f:
                data = f.read().replace(b"\r\n", b"\n")
            h.update(os.path.relpath(path, SKILL_DIR).replace(os.sep, "/").encode("utf-8") + b"\0" + hashlib.sha256(data).digest())
    return h.hexdigest()


def safe_filename(s):
    return re.sub(r'[\\/:*?"<>|]+', "", s).strip()


def output_name(first, surname, date_completed):
    """Derived, never typed: Fact Find Summary - DD.MM.YY - (First Surname).pdf  (date = the Fact Find's Date Completed)."""
    sd = short_date(date_completed)
    first, surname = (first or "").strip(), (surname or "").strip()
    if not (first and surname and sd):
        return None
    return safe_filename("Fact Find Summary - %s - (%s %s)" % (sd, first, surname)) + ".pdf"
