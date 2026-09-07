#!/usr/bin/env python3
from pathlib import Path
import argparse, re, subprocess
ROOT = Path(__file__).resolve().parents[1]
P = re.compile(r"v(\d+)\.(\d+)\.(\d+)$")
parser = argparse.ArgumentParser(); parser.add_argument("kind", choices=("major", "minor", "patch")); kind = parser.parse_args().kind
versions = [tuple(map(int, m.groups())) for tag in subprocess.check_output(["git", "tag", "--list", "v*"], cwd=ROOT, text=True).splitlines() if (m := P.fullmatch(tag))]
if not versions: raise SystemExit("no semantic-version tag was found")
major, minor, patch = max(versions)
if kind == "major": major, minor, patch = major + 1, 0, 0
elif kind == "minor": minor, patch = minor + 1, 0
else: patch += 1
print(f"v{major}.{minor}.{patch}")
