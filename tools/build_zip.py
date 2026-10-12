#!/usr/bin/env python3
"""Package the skill as dist/resume-jd-tuner.zip.

Upload the zip in the Claude apps (Customize > Skills > + > Create skill > Upload a skill, with
code execution turned on in Settings > Capabilities), or unzip it into any folder your agent
loads skills from. The zip holds one top-level folder, resume-jd-tuner/,
with SKILL.md at its root. Tests, evals and examples are left out.

Usage:  python3 tools/build_zip.py [--out PATH] [--check]

--check re-opens the zip and fails unless it holds exactly the skill's files under one
resume-jd-tuner/ folder, with SKILL.md at its root and no caches. CI and the release use it.
"""
import argparse
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "resume-jd-tuner"
TOP = "resume-jd-tuner"
SKIP_DIRS = {"__pycache__", ".pytest_cache", ".ruff_cache"}
SKIP_FILES = {".DS_Store", "Thumbs.db"}


def skill_files():
    """The files that belong in the zip, as (path on disk, path inside the zip) pairs."""
    for path in sorted(SKILL.rglob("*")):
        rel = path.relative_to(SKILL)
        if path.is_dir() or path.name in SKIP_FILES or path.suffix == ".pyc":
            continue
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        yield path, f"{TOP}/{rel.as_posix()}"


def build(out):
    if not (SKILL / "SKILL.md").exists():
        raise SystemExit(f"SKILL.md not found in {SKILL}")
    out.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for path, arcname in skill_files():
            z.write(path, arcname)
            count += 1
    return count


def check(out):
    """Problems with the zip's layout, or an empty list."""
    problems = []
    with zipfile.ZipFile(out) as z:
        names = [n for n in z.namelist() if not n.endswith("/")]
        bad = z.testzip()
    if bad:
        problems.append(f"corrupt entry: {bad}")
    outside = [n for n in names if not n.startswith(TOP + "/")]
    if outside:
        problems.append(f"entries outside {TOP}/: {outside[:5]}")
    if f"{TOP}/SKILL.md" not in names:
        problems.append(f"{TOP}/SKILL.md is missing")
    junk = [n for n in names if any(part in SKIP_DIRS or part in SKIP_FILES for part in n.split("/"))
            or n.endswith(".pyc")]
    if junk:
        problems.append(f"caches or OS files: {junk[:5]}")
    expected = {arcname for _, arcname in skill_files()}
    missing, extra = sorted(expected - set(names)), sorted(set(names) - expected)
    if missing:
        problems.append(f"skill files missing from the zip: {missing[:5]}")
    if extra:
        problems.append(f"files in the zip that are not in the skill: {extra[:5]}")
    return problems


def main():
    parser = argparse.ArgumentParser(description="Package the skill for the Claude apps.")
    parser.add_argument("--out", type=Path, default=ROOT / "dist" / "resume-jd-tuner.zip")
    parser.add_argument("--check", action="store_true", help="verify the zip's layout after building it")
    args = parser.parse_args()
    count = build(args.out)
    print(f"wrote {args.out} ({count} files, {args.out.stat().st_size // 1024} KB)")
    if args.check:
        problems = check(args.out)
        for problem in problems:
            print(f"ZIP CHECK: {problem}")
        print("ZIP CHECK: " + ("FAIL" if problems else "PASS"))
        return 1 if problems else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
