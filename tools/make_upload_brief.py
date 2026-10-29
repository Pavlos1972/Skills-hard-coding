#!/usr/bin/env python3
"""Write the upload brief for a Claude-in-Chrome chat (SKILL-STANDARDS.md S7).

  make_upload_brief.py <skill zip> [--folder "C:\\path\\to\\folder"] [--out DIR]

Every value in the brief (skill name, file name, size, file count, the "Last updated" line and the first section title)
is read from the zip itself, so nothing is typed by hand and the brief always matches what is being uploaded.
package_skill.py writes the brief next to the zip. Make the brief only when Paul has asked for that skill to be uploaded:
his request is the approval for the "Upload and replace" button the brief pre-approves.

How the upload works (observed 29/10/2026): claude.ai cannot hold two skills with one name, so uploading REPLACES the skill;
the older version stays in the skill's version history, which is the backup.
"""
import argparse
import os
import re
import sys
import zipfile

# Paul's folder for new skill zips on his Windows computer (his instruction, 29/10/2026).
DEFAULT_FOLDER = r"C:\Users\Paul\liferisk.co.za\Company - Paul\Claude\Claude Skills - New"

TEMPLATE = """Brief for a Claude chat that has Claude in Chrome: upload a new version of one skill and test it

You are helping Paul Kafentzis, a financial adviser who uses Skills in his claude.ai account. Another Claude (Claude Code) has rebuilt one of his skills and tested it on made-up data. Claude Code cannot save into his Skills, so Paul asks YOU to upload it for him in his browser, using Claude in Chrome. Paul asked for this upload himself and has approved it, including the "Upload and replace" button described in step 5. Do exactly the steps below, nothing more.

THE FACTS
- Skill name: %(skill)s
- File: %(zip)s (%(bytes)s bytes, %(files)d files)
- Where it is on Paul's Windows computer, in this folder:
  %(folder)s
  Full path of the file:
  %(fullpath)s
- What the NEW version says inside: the line "%(stamp)s", and its first section after the main title is called "%(first)s".
- Paul's account already has this skill (an older version). A zip with the same name REPLACES it: the account cannot hold two skills with one name. The older version is kept in the skill's version history (a dropdown on the skill's page, listing versions such as v32, v31 and so on). That history is the backup. Expect ONE entry before the upload and ONE entry after it.

HARD RULES
1. Work only in Paul's Skills settings page on claude.ai, plus the two test chats (steps 3 and 7). Do not open other pages. Do not change any other setting and do not touch any other skill. Do not switch the old skill off or on: that is not needed, because the upload turns the skill on.
2. NEVER delete anything. Never click Delete or Remove. Do not open, restore or change old versions.
3. The ONLY replace you may do is the one in step 5, and only if its box names exactly "%(skill)s". Paul has approved that one: click "Upload and replace" without waiting. If the box names any other skill, or shows anything you do not expect, STOP and ask Paul.
4. Do not unzip, edit or rename the zip. If the upload is refused for any reason other than the file-access message described in step 4, copy the error message exactly, show it to Paul and stop.
5. Do not run the skill on any client. Do not open any client file.
6. If code execution (shown as "Run code in the cloud" or "Code execution and file creation") is switched OFF on the settings page, tell Paul and stop. Do not switch it on yourself.
7. If the extension is not connected, a tool fails 2 or 3 times, or anything does not match what is written here, STOP, say what you tried, and ask Paul. Do not improvise.

STEPS
1. Start. Load the Claude in Chrome tools (the chrome-browser skill explains how). Look at the open tabs, then open a NEW tab and go to claude.ai. If the extension asks for site permission, tell Paul and wait.
2. Open the Skills page (Settings > Features in some versions, Customize > Skills in others; the skills Paul uploaded are under "Created by you"). Check that code execution is on (rule 6). Write down the BEFORE record: how many skills are on the page in total; how many entries are called %(skill)s (expected: exactly 1); whether it is switched on; its version label (for example v32); its date; its number of files.
3. BEFORE test. Open a new claude.ai chat in a new tab and type exactly: %(question)s
   Write down the answer word for word (an older skill may answer "none" for the first part).
4. Upload. Choose the button to upload or add a skill and give it the zip. The file-upload tool may refuse the first attempt with a message like "only files this session is allowed to read can be uploaded". That is expected, and this is the fix: tell Paul you need folder access to the folder named "Claude Skills - New" and ask him to approve it; then stage the zip from the computer into your workspace (it lands under /mnt/user-data/uploads/); check that the staged file is %(bytes)s bytes; then upload from that staged path. The Windows path itself may still be refused, so use the staged path. If you still cannot choose the file, tell Paul: "Please pick %(zip)s from the folder Claude Skills - New in the file window, then tell me when it is done," and wait. If the computer's file window is open, the full path above can be typed into its "File name" box.
5. The replace box. After you upload, the page shows a box like: Replace "%(skill)s" skill? ... Earlier versions stay available in the skill's version history. Current: N lines - This file: M lines. Write down the box text word for word, especially the two line counts. Paul has approved this: click "Upload and replace". (If the skill was switched off, the box says the upload will switch it on again. That is fine.)
6. AFTER record. Reload the Skills page. Expected: still ONE entry named %(skill)s, switched ON, a version label one higher than before, %(files)d files, and opening with "%(first)s". The old version is NOT a separate entry. Write down what you see.
7. AFTER test. Open a new chat and type exactly the same question as in step 3.
   Correct answer: "%(stamp)s" and "%(first)s".
   If the answer is different, STOP and tell Paul. Do not undo anything.
8. Report to Paul in plain, short words, as a before-and-after list: number of entries; version label; number of files; the two line counts from the replace box; the test answer before and after, quoted; what happened at the upload (any message word for word, whether folder access and staging were needed, whether Paul had to pick the file himself); anything unusual. Finish with: "Uploaded and tested. Not confirmed live until you confirm." Do not say it is live. Paul will confirm.
"""


def facts(zip_path):
    """Everything the brief says about the skill, read from the zip."""
    with zipfile.ZipFile(zip_path) as z:
        names = [n for n in z.namelist() if not n.endswith("/")]
        tops = {n.split("/")[0] for n in names}
        if len(tops) != 1:
            sys.exit("The zip must hold exactly one top-level skill folder, found: %s" % sorted(tops))
        top = tops.pop()
        md_name = "%s/SKILL.md" % top
        if md_name not in names:
            sys.exit("%s has no SKILL.md" % os.path.basename(zip_path))
        md = z.read(md_name).decode("utf-8")
    m = re.search(r'^name:\s*"?([a-z0-9-]+)"?\s*$', md, re.M)
    skill = m.group(1) if m else top
    s = re.search(r"\*\*(Last updated:[^*]+)\*\*", md)
    if not s:
        sys.exit("SKILL.md has no 'Last updated' line: stamp the skill first (tools/stamp_skill.py)")
    lines = md.split("\n")
    title = next((i for i, l in enumerate(lines) if l.startswith("# ")), None)
    first = next((l[3:].strip() for l in lines[(title or 0) + 1:] if l.startswith("## ")), None) if title is not None else None
    if not first:
        sys.exit("SKILL.md has no section heading ('## ...') after its main title")
    return {"skill": skill, "zip": os.path.basename(zip_path), "bytes": os.path.getsize(zip_path), "files": len(names),
            "stamp": s.group(1).strip(), "first": first}


def build(zip_path, folder=DEFAULT_FOLDER):
    f = facts(zip_path)
    f["bytes"] = "{:,}".format(f["bytes"])
    f["folder"] = folder
    f["fullpath"] = folder.rstrip("\\") + "\\" + f["zip"]
    f["question"] = ('Do not run any task and do not use any client information. Open the skill %s and tell me only (1) the line that starts with '
                     '"Last updated" (say "none" if there is no such line) and (2) the title of the first section after the main title.' % f["skill"])
    return TEMPLATE % f


def write(zip_path, out_dir=None, folder=DEFAULT_FOLDER):
    out_dir = out_dir or os.path.dirname(os.path.abspath(zip_path))
    path = os.path.join(out_dir, os.path.splitext(os.path.basename(zip_path))[0] + ".upload-brief.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(build(zip_path, folder))
    return path


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("zip")
    ap.add_argument("--folder", default=DEFAULT_FOLDER)
    ap.add_argument("--out", default=None, help="folder to write into (default: next to the zip)")
    a = ap.parse_args()
    print(write(a.zip, a.out, a.folder))


if __name__ == "__main__":
    main()
