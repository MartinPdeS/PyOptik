#!/usr/bin/env python3
from pathlib import Path
import argparse, os, re, subprocess, sys
ROOT = Path(__file__).resolve().parents[1]; VERSION_FILE = ROOT / "PyOptik/_version.py"; P = re.compile(r"v(\d+\.\d+\.\d+)$")
tag = argparse.ArgumentParser(); tag.add_argument("tag"); value = tag.parse_args().tag; match = P.fullmatch(value)
if not match: raise SystemExit("release aborted: tag must use vMAJOR.MINOR.PATCH")
def run(*args, **kwargs): return subprocess.run(args, cwd=ROOT, check=True, text=True, **kwargs)
try:
    if run("git", "status", "--porcelain", capture_output=True).stdout: raise RuntimeError("working tree is not clean")
    if run("git", "tag", "--list", value, capture_output=True).stdout: raise RuntimeError(f"tag {value} already exists")
    env = os.environ | {"SETUPTOOLS_SCM_PRETEND_VERSION": match.group(1)}
    run(sys.executable, "-m", "vcs_versioning", "--force-write-version-files", env=env)
    run("git", "add", str(VERSION_FILE.relative_to(ROOT))); run("git", "commit", "-m", f"Release {value}"); run("git", "tag", "-a", value, "-m", f"Release {value}")
except (RuntimeError, subprocess.CalledProcessError) as error: raise SystemExit(f"release aborted: {error}")
print(f"created release commit and annotated tag {value}")
