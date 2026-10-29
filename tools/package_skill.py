#!/usr/bin/env python3
"""Build the upload zip for one skill (SKILL-STANDARDS.md S7).

  package_skill.py <skill_dir> [--out releases] [--skip-tests]

Refuses to build unless lint passes and every test passes. After zipping it unpacks the zip somewhere else and
runs the preflight self-test and the same tests against the PACKAGED scripts, so what Paul uploads is what was tested.
The zip holds only what Claude needs at run time: SKILL.md, steps.json, deliverables.json, scripts/, references/.
"""
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

import make_upload_brief
import wr_stamp

HERE = os.path.dirname(os.path.abspath(__file__))
INCLUDE_FILES, INCLUDE_DIRS = wr_stamp.INCLUDE_FILES, wr_stamp.INCLUDE_DIRS


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("skill_dir")
    ap.add_argument("--out", default="releases")
    ap.add_argument("--skip-tests", action="store_true")
    a = ap.parse_args()
    skill = os.path.abspath(a.skill_dir)
    name = os.path.basename(skill)

    r = run([sys.executable, os.path.join(HERE, "lint_skill.py"), skill])
    print(r.stdout.strip())
    if r.returncode:
        sys.exit("PACKAGING REFUSED: lint failed. Fix the FAIL lines above (stamp the skill with tools/stamp_skill.py after editing).")

    tests = os.path.join(skill, "tests")
    if not a.skip_tests:
        r = run([sys.executable, "-m", "unittest", "discover", "-s", tests], cwd=skill)
        print(r.stderr.strip().split("\n")[-1])
        if r.returncode:
            print(r.stderr[-3000:])
            sys.exit("PACKAGING REFUSED: the tests failed.")

    text = open(os.path.join(skill, "SKILL.md"), encoding="utf-8").read()
    m = re.search(r"\*\*Last updated:\s*(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})", text)
    version = "".join(m.groups()[:3]) + "-" + "".join(m.groups()[3:])
    os.makedirs(a.out, exist_ok=True)
    zpath = os.path.abspath(os.path.join(a.out, "%s-%s.zip" % (name, version)))
    members = []
    for f in INCLUDE_FILES:
        members.append(f)
    for d in INCLUDE_DIRS:
        for root, dirs, files in os.walk(os.path.join(skill, d)):
            dirs[:] = [x for x in dirs if x != "__pycache__"]
            members += [os.path.relpath(os.path.join(root, f), skill) for f in sorted(files) if not f.endswith(".pyc")]
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for rel in members:
            z.write(os.path.join(skill, rel), "%s/%s" % (name, rel.replace(os.sep, "/")))

    # prove the package works from where it will live
    tmp = tempfile.mkdtemp(prefix="pkgcheck-")
    try:
        with zipfile.ZipFile(zpath) as z:
            z.extractall(tmp)
        pkg = os.path.join(tmp, name)
        r = run([sys.executable, os.path.join(pkg, "scripts", "run.py"), "preflight"])
        print(r.stdout.strip())
        if r.returncode:
            sys.exit("PACKAGING REFUSED: the packaged copy fails its own self-test.")
        if not a.skip_tests:
            env = dict(os.environ, WR_SCRIPTS=os.path.join(pkg, "scripts"))
            r = run([sys.executable, "-m", "unittest", "discover", "-s", tests], cwd=skill, env=env)
            last = r.stderr.strip().split("\n")[-1]
            print("tests against the PACKAGED scripts: " + last)
            if r.returncode:
                print(r.stderr[-3000:])
                sys.exit("PACKAGING REFUSED: the tests fail against the packaged copy.")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    sha = hashlib.sha256(open(zpath, "rb").read()).hexdigest()
    print("\nPACKAGED: %s\n  %d files, %d bytes, sha256 %s" % (zpath, len(members), os.path.getsize(zpath), sha))
    for rel in members:
        print("   " + rel)
    print("\nUPLOAD BRIEF for the Claude-in-Chrome chat (give it to Paul): %s" % make_upload_brief.write(zpath))


if __name__ == "__main__":
    main()
