"""Shared helpers for the outlook-emails-skill scripts (standard library only)."""
import datetime as dt
import hashlib
import json
import os
import re
import sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))

# file names inside a run folder
RUN = "run.json"
STATE = "state.json"
ACCESS = "access_log.json"
RECEIPT = "receipt.json"
FACTS = "facts.json"
OUT = "out"
WATCH = "watch.json"                    # the exact arguments for create_trigger: the hourly reply watcher
FLAG = "flag.json"                      # the exact arguments for create_trigger: the one-shot silence flag
PLAN_TXT = "plan.txt"                   # the plan in plain words, for Paul
SAST = dt.timezone(dt.timedelta(hours=2))
TZ_SA = "Africa/Johannesburg"           # the watcher's hours are South African business hours (SAST, UTC+2, no daylight saving)
OWN_MAILBOX = "paulk@liferisk.co.za"    # Paul's own mailbox: never a sender to wait for
CONNECTOR = "Microsoft 365"             # the only connector the scheduled checks may use (reads Outlook)

ROUTES = ("m365", "zapier", "device")
ROUTE_NAMES = {"m365": "the Microsoft 365 connector (Outlook search)", "zapier": "the Zapier Office 365 tools", "device": "the computer"}


def today():
    """Today's date in South Africa (WR_TODAY=DD/MM/YYYY is for tests only)."""
    env = os.environ.get("WR_TODAY")
    return parse_date(env) if env else dt.datetime.now(SAST).date()


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
