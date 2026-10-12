"""Repository-level checks: skill metadata, referenced files, plugin manifests, JSON assets,
the release checks and the upload zip."""
import json
import os
import re
import shutil
import sys
import zipfile

import pytest
import yaml

from check_env import installed_version, is_older, version_tuple
from conftest import ASSETS, ROOT, SKILL, run_script
from relevance_score import score

sys.path.insert(0, str(ROOT / "tools"))
import build_zip  # noqa: E402
import release  # noqa: E402

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
    plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
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
        jsonschema.validate(json.loads((ASSETS / example).read_text(encoding="utf-8")),
                            json.loads((ASSETS / schema).read_text(encoding="utf-8")))


def test_example_grades_cover_every_ask():
    asks = json.loads((ASSETS / "example_jd_asks.json").read_text(encoding="utf-8"))["asks"]
    grades = json.loads((ASSETS / "example_grades.json").read_text(encoding="utf-8"))["grades"]
    assert sorted(a["id"] for a in asks) == sorted(g["id"] for g in grades)


def test_relevance_score_is_deterministic():
    jd = "Data Analyst\nAcme\nRequirements:\n- SQL and Looker\n- dbt models\nNice to have:\n- Python"
    resume = "Analyst. Built Looker dashboards on dbt models with SQL."
    assert score(jd, resume) == score(jd, resume)
    assert 0 < score(jd, resume)[0] <= 100


def test_check_env_runs():
    proc = run_script("check_env.py")
    assert "ENV:" in proc.stdout


def test_check_env_compares_versions():
    assert version_tuple("5.1.0") == (5, 1, 0) and version_tuple("20221105") == (20221105,)
    assert version_tuple("6.0.0rc1") == (6, 0, 0) and version_tuple("") == ()
    assert is_older("4.3.1", "5.1") and is_older("5.0.1", "5.1")
    assert not is_older("5.1.0", "5.1") and not is_older("6.20.0", "5.1")
    assert not is_older("20260107", "20221105") and is_older("20211012", "20221105")
    assert not is_older("", "5.1")  # unknown version: don't block


def test_check_env_finds_installed_versions():
    import pdfminer
    import pypdf
    import reportlab
    # pdfminer.six records its name as "pdfminer_six" in newer releases; Python 3.9 doesn't normalise it.
    for module, name in ((pdfminer, "pdfminer.six"), (pypdf, "pypdf"), (reportlab, "reportlab")):
        assert version_tuple(installed_version(module, name)), name

    class Placeholder:
        __version__ = "0.0"
    assert installed_version(Placeholder, "not-a-real-package-name") == ""


@pytest.mark.skipif(not os.environ.get("RJT_REQUIRE_TOOLS"), reason="set RJT_REQUIRE_TOOLS=1 to require them")
def test_optional_tools_are_installed_when_required():
    missing = [tool for tool in ("pdftotext", "pdffonts", "pdflatex") if not shutil.which(tool)]
    assert not missing, f"CI expects these tools: {missing}"


def test_versions_agree_and_changelog_has_an_entry():
    assert release.check() == [], release.check()
    version = release.versions()[".claude-plugin/plugin.json"]
    assert release.changelog_section(version).strip()


def test_release_check_rejects_a_wrong_tag(tmp_path):
    version = release.versions()[".claude-plugin/plugin.json"]
    assert release.check(f"v{version}") == []
    assert any("does not match" in p for p in release.check("v99.0.0"))
    assert any("not of the form" in p for p in release.check(version))  # missing the v


def test_release_check_catches_drift(tmp_path):
    for rel in (".claude-plugin/plugin.json", "skills/resume-jd-tuner/SKILL.md", "CHANGELOG.md"):
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(ROOT / rel, tmp_path / rel)
    plugin = tmp_path / ".claude-plugin" / "plugin.json"
    data = json.loads(plugin.read_text(encoding="utf-8"))
    data["version"] = "9.9.9"
    plugin.write_text(json.dumps(data), encoding="utf-8")
    assert any("disagree" in p for p in release.check(root=tmp_path))


def test_release_notes_have_install_steps_and_the_changelog_entry():
    notes = release.notes()
    version = release.versions()[".claude-plugin/plugin.json"]
    assert "/plugin marketplace add RajdeepDas43/resume-jd-tuner" in notes
    assert f"What's new in {version}" in notes
    assert release.changelog_section(version).splitlines()[0] in notes


def test_upload_zip_has_the_right_layout(tmp_path):
    out = tmp_path / "resume-jd-tuner.zip"
    count = build_zip.build(out)
    assert count > 20 and build_zip.check(out) == []
    with zipfile.ZipFile(out) as z:
        names = z.namelist()
    assert "resume-jd-tuner/SKILL.md" in names
    assert "resume-jd-tuner/assets/fonts/LiberationSerif-Regular.ttf" in names
    assert all("\\" not in n for n in names)  # forward slashes on every platform
    with zipfile.ZipFile(out, "a") as z:
        z.writestr("resume-jd-tuner/scripts/__pycache__/x.pyc", b"")
    assert any("caches" in p for p in build_zip.check(out))
