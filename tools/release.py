#!/usr/bin/env python3
"""Release checks and notes, used by the Release workflow and the tests.

Usage:
  python3 tools/release.py check [vX.Y.Z]   the version in plugin.json, SKILL.md and the top entry
                                             of CHANGELOG.md agree (and match the tag, if given)
  python3 tools/release.py notes             release notes for the current version, from CHANGELOG.md
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = "RajdeepDas43/resume-jd-tuner"
SEMVER = re.compile(r"\d+\.\d+\.\d+")
HEADING = re.compile(r"^## (\S+)", re.M)

INSTALL = f"""## Install

- **Claude apps (claude.ai, Desktop, Cowork):** download `resume-jd-tuner.zip` below, turn on code \
execution in Settings → Capabilities, then go to Customize → Skills → + → Upload a skill.
- **Claude Code:** `/plugin marketplace add {REPO}`, then `/plugin install resume-jd-tuner@resume-jd-tuner`.
"""


def versions(root=ROOT):
    """Every place the version is written, as {source: version}."""
    plugin = json.loads((root / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    skill = (root / "skills" / "resume-jd-tuner" / "SKILL.md").read_text(encoding="utf-8")
    front = re.match(r"^---\n(.*?)\n---\n", skill, re.S)
    meta = re.search(r'^\s+version:\s*"?([^"\s]+)"?\s*$', front.group(1), re.M) if front else None
    changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    top = HEADING.search(changelog)
    return {
        ".claude-plugin/plugin.json": plugin.get("version", ""),
        "SKILL.md metadata.version": meta.group(1) if meta else "",
        "CHANGELOG.md (top entry)": top.group(1) if top else "",
    }


def check(tag=None, root=ROOT):
    """Problems that should stop a release, or an empty list."""
    found = versions(root)
    problems = [f"{source}: '{v}' is not a version like 1.2.3" for source, v in found.items()
                if not SEMVER.fullmatch(v)]
    if len(set(found.values())) > 1:
        problems.append("versions disagree: " + ", ".join(f"{s} = {v}" for s, v in found.items()))
    if tag is not None:
        if not re.fullmatch(r"v\d+\.\d+\.\d+", tag):
            problems.append(f"tag '{tag}' is not of the form vX.Y.Z")
        elif tag[1:] != found[".claude-plugin/plugin.json"]:
            problems.append(f"tag {tag} does not match version {found['.claude-plugin/plugin.json']}")
    return problems


def changelog_section(version, root=ROOT):
    """The body of the CHANGELOG entry for this version, without its heading."""
    text = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    heads = list(HEADING.finditer(text))
    for i, head in enumerate(heads):
        if head.group(1) == version:
            end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
            return text[head.end():end].split("\n", 1)[-1].strip()
    raise SystemExit(f"CHANGELOG.md has no entry for {version}")


def notes(root=ROOT):
    version = versions(root)[".claude-plugin/plugin.json"]
    return f"{INSTALL}\n## What's new in {version}\n\n{changelog_section(version, root)}\n"


def main():
    parser = argparse.ArgumentParser(description="Release checks and notes.")
    sub = parser.add_subparsers(dest="command", required=True)
    c = sub.add_parser("check", help="check that the versions agree (and match the tag)")
    c.add_argument("tag", nargs="?", default=None)
    sub.add_parser("notes", help="print the release notes for the current version")
    args = parser.parse_args()
    if args.command == "notes":
        sys.stdout.reconfigure(encoding="utf-8")
        print(notes(), end="")
        return 0
    problems = check(args.tag or None)
    for source, version in versions().items():
        print(f"{source}: {version}")
    for problem in problems:
        print(f"RELEASE CHECK: {problem}")
    print("RELEASE CHECK: " + ("FAIL" if problems else "PASS"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
