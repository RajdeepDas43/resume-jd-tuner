import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "resume-jd-tuner"
SCRIPTS = SKILL / "scripts"
ASSETS = SKILL / "assets"
sys.path.insert(0, str(SCRIPTS))


def run_script(name, *args, check=True, env=None):
    """Run a skill script the way the agent does and return the completed process.

    The scripts write UTF-8 whatever the platform, so their output is decoded as UTF-8 here.
    `env` adds variables to the inherited environment.
    """
    full_env = {**os.environ, **env} if env else None
    proc = subprocess.run([sys.executable, str(SCRIPTS / name), *map(str, args)],
                          capture_output=True, text=True, encoding="utf-8", errors="replace",
                          timeout=180, env=full_env)
    if check and proc.returncode != 0:
        raise AssertionError(f"{name} failed ({proc.returncode}):\n{proc.stdout}\n{proc.stderr}")
    return proc


def make_resume(bullets_per_role=3, roles=2, bullet="Built a small internal tool in Python for the finance team."):
    """A synthetic resume dict for the renderer."""
    data = json.loads((ASSETS / "example_resume.json").read_text(encoding="utf-8"))
    entries = []
    for i in range(roles):
        entries.append({"org": f"Company {i + 1}", "location": "Austin, TX", "role": "Engineer",
                        "dates": f"Jan {2015 + i} – Dec {2015 + i}", "bullets": [bullet] * bullets_per_role})
    data["sections"][0]["entries"] = entries
    return data


@pytest.fixture
def example_pdf(tmp_path):
    out = tmp_path / "Alex_Rivera_Backend_Engineer.pdf"
    run_script("render_resume_pdf.py", ASSETS / "example_resume.json", "-o", out)
    return out
