"""Repository-level checks: skill metadata, referenced files, plugin manifests, JSON assets."""
import json
import re

import yaml

from conftest import ASSETS, ROOT, SKILL, run_script
from relevance_score import score

ALLOWED_KEYS = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}


def frontmatter():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert m, "SKILL.md needs YAML frontmatter"
    return yaml.safe_load(m.group(1)), text


def test_skill_frontmatter():
    fm, body = frontmatter()
    assert set(fm) <= ALLOWED_KEYS, set(fm) - ALLOWED_KEYS
    assert fm["name"] == "resume-jd-tuner" == SKILL.name
    assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", fm["name"])
    assert 100 < len(fm["description"]) <= 1024
    assert "<" not in fm["description"] and ">" not in fm["description"]
    assert len(fm.get("compatibility", "")) <= 500
    assert len(body.splitlines()) < 500


def test_every_referenced_file_exists():
    _, body = frontmatter()
    paths = set(re.findall(r"`((?:references|assets)/[\w./-]+)`", body))
    paths |= {f"scripts/{m}" for m in re.findall(r"scripts/([\w]+\.py)", body)}
    for ref in (SKILL / "references").glob("*.md"):
        text = ref.read_text(encoding="utf-8")
        paths |= {f"references/{m}" for m in re.findall(r"`([\w-]+\.md)`", text)
                  if (SKILL / "references" / m).exists() or m.endswith("-rules.md")}
    missing = [p for p in sorted(paths) if not (SKILL / p).exists()]
    assert not missing, missing


def test_plugin_manifests_agree():
    plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
    market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
    fm, _ = frontmatter()
    assert plugin["name"] == market["plugins"][0]["name"] == "resume-jd-tuner"
    assert market["plugins"][0]["source"] in (".", "./")
    assert plugin["license"] == fm["license"] == "Apache-2.0"
    assert plugin["version"] == fm["metadata"]["version"]


def test_json_assets_parse_and_examples_match_schemas():
    for path in ASSETS.glob("*.json"):
        json.loads(path.read_text(encoding="utf-8"))
    try:
        import jsonschema
    except ImportError:
        return
    pairs = [("resume_schema.json", "example_resume.json"), ("jd_asks_schema.json", "example_jd_asks.json"),
             ("grades_schema.json", "example_grades.json")]
    for schema, example in pairs:
        jsonschema.validate(json.loads((ASSETS / example).read_text()), json.loads((ASSETS / schema).read_text()))


def test_example_grades_cover_every_ask():
    asks = json.loads((ASSETS / "example_jd_asks.json").read_text())["asks"]
    grades = json.loads((ASSETS / "example_grades.json").read_text())["grades"]
    assert sorted(a["id"] for a in asks) == sorted(g["id"] for g in grades)


def test_relevance_score_is_deterministic():
    jd = "Data Analyst\nAcme\nRequirements:\n- SQL and Looker\n- dbt models\nNice to have:\n- Python"
    resume = "Analyst. Built Looker dashboards on dbt models with SQL."
    assert score(jd, resume) == score(jd, resume)
    assert 0 < score(jd, resume)[0] <= 100


def test_check_env_runs():
    proc = run_script("check_env.py")
    assert "ENV:" in proc.stdout
