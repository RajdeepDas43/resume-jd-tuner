#!/usr/bin/env python3
"""Package the skill as dist/resume-jd-tuner.zip.

Upload the zip in the Claude apps (Customize > Skills > + > Create skill > Upload a skill, with
code execution turned on in Settings > Capabilities), or unzip it into any folder your agent
loads skills from. The zip holds one top-level folder, resume-jd-tuner/,
with SKILL.md at its root. Tests, evals and examples are left out.

Usage:  python3 tools/build_zip.py
"""
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "resume-jd-tuner"
SKIP_DIRS = {"__pycache__", ".pytest_cache", ".ruff_cache"}
SKIP_FILES = {".DS_Store", "Thumbs.db"}


def main():
    if not (SKILL / "SKILL.md").exists():
        raise SystemExit(f"SKILL.md not found in {SKILL}")
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    out = dist / "resume-jd-tuner.zip"
    count = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for path in sorted(SKILL.rglob("*")):
            rel = path.relative_to(SKILL)
            if path.is_dir() or path.name in SKIP_FILES or path.suffix == ".pyc":
                continue
            if any(part in SKIP_DIRS for part in rel.parts):
                continue
            z.write(path, Path("resume-jd-tuner") / rel)
            count += 1
    print(f"wrote {out} ({count} files, {out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
