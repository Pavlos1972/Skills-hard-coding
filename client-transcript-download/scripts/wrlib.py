"""Shared helpers for the client-transcript-download scripts (standard library only)."""
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
MEETING = "meeting.json"
CHECK = "transcript_check.json"
SOURCE = "source"                       # the received transcript, kept with its own extension (source.docx / source.vtt / source.txt)
OUT = "out"

FETCH_ROUTES = ("m365", "zapier", "chrome")      # how the transcript is fetched (Paul, 03/11/2026: connector first, Chrome as the fallback)
SAVE_ROUTES = ("device",)                         # the finished file is saved ON THE COMPUTER (device tools) and fingerprinted there: Microsoft 365 and Zapier would have to carry it as base64 in one call
PURPOSES = {"fetch": FETCH_ROUTES, "save": SAVE_ROUTES}
COMPUTER_STOP = ("STOP. I could not connect this chat to your computer (the connection was refused or did not go through), so the transcript cannot be saved into the client's 2. Fact Find folder. "
                 "Please allow the connection to the folder liferisk.co.za, then tell me to go on.")
TOLERANCE_S = 120                                # the last time stamp may fall this far short of the stated length (Paul, 03/11/2026)
JUMP_S = 600                                     # no gap longer than this between two time stamps


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


def output_name(first, surname, meeting_date):
    """Derived, never typed: Teams meeting transcript - DD.MM.YY - (First Surname).docx"""
    sd = short_date(meeting_date)
    first, surname = (first or "").strip(), (surname or "").strip()
    if not (first and surname and sd):
        return None
    return safe_filename("Teams meeting transcript - %s - (%s %s)" % (sd, first, surname)) + ".docx"


def fmt_hms(sec):
    sec = int(sec)
    return "%d:%02d:%02d" % (sec // 3600, sec % 3600 // 60, sec % 60)


def find_computer_root():
    """The folder of the computer's OneDrive when it is mounted into THIS machine (a test, or a chat running on the computer), or None. WR_COMPUTER_ROOT overrides the search."""
    env = os.environ.get("WR_COMPUTER_ROOT")
    if env:
        return os.path.realpath(env) if os.path.isdir(env) else None
    for base in (os.path.expanduser("~/mnt"), "/mnt"):
        if not os.path.isdir(base):
            continue
        for d, dirs, _files in os.walk(base):
            if d[len(base):].count(os.sep) >= 3:
                dirs[:] = []
                continue
            if "Company - Paul" in dirs or "Company - WR Clients" in dirs:
                return os.path.realpath(d)
            if os.path.basename(d) in ("Company - Paul", "Company - WR Clients"):
                return os.path.realpath(os.path.dirname(d))
    return None


def parse_device_output(text, name):
    """The output of `sha256sum FILE` and `stat -c %s FILE` run ON THE COMPUTER (device_bash), pasted whole: (sha256, size, None), or (None, None, what is wrong).
    The file name in the sha256sum line must be the saved file's own name, so a hash of another file cannot be passed off."""
    sha, size = None, None
    for ln in (text or "").splitlines():
        m = re.match(r"^\s*([0-9a-fA-F]{64})\s+[*]?(.+?)\s*$", ln)
        if m:
            base = os.path.basename(m.group(2).replace("\\", "/"))
            if base != name:
                return None, None, "the sha256sum line names %r, not %r" % (base, name)
            sha = m.group(1).lower()
        elif re.fullmatch(r"\s*\d+\s*", ln):
            size = int(ln)
    if not sha or size is None:
        return None, None, "paste the whole output of: sha256sum \"<file>\" && stat -c %%s \"<file>\" (run with device_bash on the computer): a 64-character fingerprint with the file's name, and its size on its own line"
    return sha, size, None
