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

# Access routes (SKILL-STANDARDS.md S4). The COMPUTER comes first: the client's OneDrive folder, mounted into this chat, gives every file as real bytes
# and takes the finished PDF without any size limit. The program finds that folder itself (find_computer_root); the chat never requests the connection.
# Microsoft 365 returns files cut off and as text, so it is only a fallback for small text files, every copy proved by its size.
ROUTES = ("device", "m365", "zapier")
ROUTE_NAMES = {
    "device": "the computer: the client's OneDrive folder mounted into this chat (real bytes, no size limit)",
    "m365": "Microsoft 365 connector (SharePoint/OneDrive, Outlook, Teams transcripts)",
    "zapier": "Zapier (Office 365 and Teams tools)",
}

# Kinds of client-file source. The form's data file and the transcript are recorded through the access log and the
# form/prep steps; these are the documents read besides them.
SOURCE_KINDS = ["Overview", "Policy schedule", "Other document", "Correspondence", "Manual Fact Find"]
REQUIRED_SOURCE_KINDS = ["Overview"]
DOC_TYPES = SOURCE_KINDS + ["Paul (chat)"]
FILE_NEEDS = ("form", "formpdf", "transcript") + tuple(SOURCE_KINDS)       # access entries for these are files: every copy must be proved
COPY_ROUTES = ("device", "m365", "zapier")
LEDGER_LOCK = "ledger.lock"
COMPUTER_STOP = ("STOP. This chat is not connected to your computer, and the large client files (the form's PDF above all) cannot be read through Microsoft 365: "
                 "it returns them cut off. Connect this chat to your computer (the folder liferisk.co.za, with Company - Paul inside it), then tell me to go on.")


def find_computer_root():
    """The folder of the computer's OneDrive as this chat sees it (the one that holds 'Company - Paul'), or None. WR_COMPUTER_ROOT overrides the search (tests)."""
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


def under_root(path, root):
    rp, rr = os.path.realpath(path), os.path.realpath(root)
    return rp == rr or rp.startswith(rr.rstrip(os.sep) + os.sep)


def save_ledger(run, led):
    """The ledger is written only by the program; the lock file holds its fingerprint so a hand edit is seen by the checker."""
    save_json(os.path.join(run, LEDGER), led)
    with open(os.path.join(run, LEDGER_LOCK), "w", encoding="utf-8") as f:
        f.write(sha256_file(os.path.join(run, LEDGER)) + "\n")

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
    """'R 24 000.00' / 'R24,000.00' / '24000' / 'R 1.234,50' -> Decimal (2 places), or None when it is not an amount
    or when the way it is written is ambiguous (for example 'R 2.000': two rand or two thousand?)."""
    s = str(text or "").strip().replace("\u00a0", " ")
    if not s:
        return None
    neg = s.startswith("-") or s.startswith("(")
    s = re.sub(r"^[Rr]\s*", "", s.lstrip("-(").strip()).rstrip(")").strip()
    s = re.sub(r"^[Rr]\s*", "", s)
    if not re.fullmatch(r"\d[\d ,.]*", s):
        return None
    s = s.replace(" ", "")
    if "," in s and "." in s:
        if s.rfind(".") > s.rfind(","):
            s = s.replace(",", "")                   # 24,000.00
        else:
            s = s.replace(".", "").replace(",", ".")   # 1.234,50
    elif "," in s:
        head, _, tail = s.rpartition(",")
        if s.count(",") > 1 or len(tail) == 3:
            s = s.replace(",", "")                   # 2,000 or 1,234,567
        elif len(tail) in (1, 2):
            s = head + "." + tail                    # 1234,50
        else:
            return None
    elif "." in s:
        head, _, tail = s.rpartition(".")
        if s.count(".") > 1:
            s = s.replace(".", "")                   # 1.234.567
        elif len(tail) not in (1, 2):
            return None                              # 'R 2.000' could be 2 or 2000: refuse rather than guess
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


def same_person(first_a, surname_a, first_b, surname_b):
    """The same full name, whatever way it is split into first names and surname ('Pat Jo' + 'Samplecase' = 'Pat' + 'Jo Samplecase')."""
    return norm("%s %s" % (first_a, surname_a)) == norm("%s %s" % (first_b, surname_b)) and bool(norm(first_a)) and bool(norm(surname_a))


def last_name_token(surname):
    toks = norm(surname).split()
    return toks[-1] if toks else ""


# ------------------------------------------------------------------ reasons and content words (a written reason must say something about THIS line or field)
STOP_WORDS = frozenset("""
that this with have from your what when they them then there here were been would could should about which their into just only some very more much than does done
also each such like make made take took come came back over after before while where these those other another because still really right know
think said says tell told give gave goes going good well yeah okay thanks thank please sure fine
""".split())
NUMBER_WORDS = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
                "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40,
                "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90, "hundred": 100}


def content_words(text, minlen=4):
    """The lower-case words of a text that carry meaning: letters only, at least `minlen` of them, not a filler word."""
    out = []
    for x in re.findall(r"[A-Za-z][A-Za-z'-]*", str(text or "")):
        x = x.lower().strip("'-")
        if len(x) >= minlen and x not in STOP_WORDS:
            out.append(x)
    return out


def _stem(x):
    return x[:5] if len(x) > 5 else x


def shared_content_words(a, b):
    """Content words that two texts share (a plural or an ending does not matter: the first five letters are compared)."""
    sb = {_stem(x): x for x in content_words(b)}
    return sorted({sb[_stem(x)] for x in content_words(a) if _stem(x) in sb})


def numbers_in(text):
    """Every number in a text, written in digits or in words (twenty five, eight), as a set of Decimals-as-strings without a trailing .0."""
    out = set()
    for m in re.finditer(r"\d+(?:[.,]\d+)?", str(text or "")):
        t = m.group(0).replace(",", ".")
        out.add(t.rstrip("0").rstrip(".") if "." in t else t)
    toks = re.findall(r"[a-z]+", str(text or "").lower())
    i = 0
    while i < len(toks):
        if toks[i] in NUMBER_WORDS:
            v = NUMBER_WORDS[toks[i]]
            if v >= 20 and v < 100 and i + 1 < len(toks) and toks[i + 1] in NUMBER_WORDS and 0 < NUMBER_WORDS[toks[i + 1]] < 10:
                v += NUMBER_WORDS[toks[i + 1]]
                i += 1
            out.add(str(v))
        i += 1
    return out


def reason_problem(reason, minchars=15):
    """None when a written reason could really be one; otherwise the plain reason it is refused (too short, one word, one repeated character)."""
    r = str(reason or "").strip()
    if len(r) < minchars:
        return "give a real reason (at least %d characters)" % minchars
    letters = [c for c in r.lower() if not c.isspace()]
    if letters and max(letters.count(c) for c in set(letters)) > 0.5 * len(letters):
        return "that reason is mostly one repeated character: say what you found"
    if len({x for x in re.findall(r"[a-z0-9]+", r.lower())}) < 3:
        return "a reason needs at least three different words"
    return None


def reason_hit_problem(reason, hit_lines, lines):
    """For a reason that overrides search hits: it must be a real reason, name at least one of the hit lines by number, and hold a content word from that line."""
    p = reason_problem(reason)
    if p or not hit_lines:
        return p
    r = str(reason)
    cited = [h for h in hit_lines if isinstance(h, int) and re.search(r"(?<![\d])%d(?![\d])" % h, r)]
    if not cited:
        return "the search found call line(s) %s: name at least one of them by number in the reason, and say why it does not answer this" % list(hit_lines)[:8]
    bare = re.sub(r"\d+", " ", r)
    if not any(1 <= h <= len(lines) and shared_content_words(bare, lines[h - 1]) for h in cited):
        return "the reason names line %s but holds no word (4 letters or more) from what that line says: quote its words" % cited[0]
    return None


FINGERPRINT_FILES = ("steps.json", "deliverables.json")


def program_fingerprint():
    """A fingerprint of everything that drives a run (the programs, the layout, the steps, the rule pages): it must not change during a run."""
    h = hashlib.sha256()
    paths = [os.path.join(SKILL_DIR, f) for f in FINGERPRINT_FILES]
    for d in ("scripts", "references"):
        for root, dirs, files in os.walk(os.path.join(SKILL_DIR, d)):
            dirs[:] = sorted(x for x in dirs if x != "__pycache__")
            paths += [os.path.join(root, f) for f in sorted(files) if not f.endswith(".pyc")]
    for path in sorted(paths):
        if not os.path.exists(path):
            continue
        with open(path, "rb") as f:
            data = f.read().replace(b"\r\n", b"\n")
        h.update(os.path.relpath(path, SKILL_DIR).replace(os.sep, "/").encode("utf-8") + b"\0" + hashlib.sha256(data).digest())
    return h.hexdigest()


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
