import json

from conftest import ASSETS, run_script
from coverage import compute, load_asks
from scoreboard import band_for, fit, risk_level

TEXT = """Alex Rivera
SUMMARY
Backend engineer with six years building payment services in Go.
EXPERIENCE
• Split the order monolith into Go services on Kubernetes on AWS.
• Rebuilt refunds as an idempotent workflow on Postgres.
SKILLS
Go, Kubernetes, AWS, Terraform, Kafka
"""


def test_coverage_counts_exact_spelling_only():
    data = load_asks(ASSETS / "example_jd_asks.json")
    r = compute(data, TEXT)
    terms = {t["term"].split(" / ")[0]: t for t in r["hard_terms"]}
    assert terms["Go"]["present"] and terms["Go"]["matched"] == "Go"
    assert "experience/summary" in terms["Go"]["where"]
    assert not terms["PostgreSQL"]["present"]
    assert terms["PostgreSQL"]["other_spelling"] in ("PostgreSQL", "Postgres")
    assert terms["Kafka"]["where"] == ["skills"]
    s = r["summary"]
    assert "PostgreSQL" in s["claimable_terms_missing"]
    assert s["unclaimable_terms_present"] == ["Terraform"]
    # must: Go, PostgreSQL, Kubernetes, AWS, Terraform (x2); nice: Kafka, PCI DSS, gRPC (x1)
    assert s["ats_alignment"] == round(100 * (2 * 4 + 1) / (2 * 5 + 3), 1)
    assert s["honest_ceiling"] == round(100 * (2 * 4 + 1) / (2 * 5 + 3), 1)


def test_variant_in_a_bullet_counts_as_in_use():
    data = {"asks": [], "hard_terms": [{"term": "Git", "type": "must", "variants": ["GitHub"]}]}
    text = "EXPERIENCE\n• Reviewed about five GitHub pull requests a week.\nSKILLS\nGit, SQL\n"
    row = compute(load_asks_dict(data), text)["hard_terms"][0]
    assert row["present"] and row["matched"] == "Git"
    assert row["where"] == ["skills", "experience/summary"]
    text_skills_only = "EXPERIENCE\n• Reviewed analysts' SQL every week.\nSKILLS\nGit, SQL\n"
    assert compute(load_asks_dict(data), text_skills_only)["hard_terms"][0]["where"] == ["skills"]


def test_alternatives_count_once():
    data = {"asks": [], "hard_terms": [{"term": "PyTorch", "type": "must", "alternatives": ["TensorFlow"]},
                                       {"term": "Spark", "type": "nice"}]}
    r = compute(load_asks_dict(data), "Trained models in TensorFlow on GPUs.")
    rows = r["hard_terms"]
    assert rows[0]["present"] and rows[0]["matched"] == "TensorFlow" and rows[0]["term"] == "PyTorch / TensorFlow"
    assert r["summary"]["ats_alignment"] == round(100 * 2 / 3, 1)


def load_asks_dict(data):
    data.setdefault("role", {})
    data.setdefault("do_not_echo", [])
    return data


def test_legacy_list_format(tmp_path):
    legacy = [{"ask": "Kafka streaming", "type": "nice", "alts": ["Kafka"]},
              {"ask": "PCI DSS", "type": "gap", "alts": ["PCI"]}]
    path = tmp_path / "asks.json"
    path.write_text(json.dumps(legacy), encoding="utf-8")
    data = load_asks(path)
    assert data["asks"][1]["claimable"] is False
    r = compute(data, TEXT)
    assert r["asks"][0]["found"] and not r["asks"][1]["found"]


def test_fit_formula_bands_and_caps():
    asks = [{"id": "M1", "type": "must"}, {"id": "M2", "type": "must"},
            {"id": "R1", "type": "role"}, {"id": "N1", "type": "nice"}]
    grades = {"grades": [{"id": "M1", "grade": "clear"}, {"id": "M2", "grade": "clear"},
                         {"id": "R1", "grade": "weak"}, {"id": "N1", "grade": "none"}]}
    warnings = []
    f = fit(asks, grades, warnings, "t")
    assert f["score"] == round(100 * (3 + 3 + 1) / 9)  # 78
    assert f["band"] == "Good" and f["cap"] is None and not warnings

    all_clear_but_one_must = {"grades": [{"id": "M1", "grade": "none"}, {"id": "M2", "grade": "clear"},
                                         {"id": "R1", "grade": "clear"}, {"id": "N1", "grade": "clear"}]}
    f = fit(asks, all_clear_but_one_must, warnings, "t")
    assert f["musts_unmet"] and f["band"] in ("Good", "Fair", "Long shot")

    missing = fit(asks, {"grades": []}, warnings, "t")
    assert missing["score"] == 0 and warnings


def test_band_edges_and_risk():
    assert band_for(85) == "Strong" and band_for(84) == "Good"
    assert band_for(55) == "Fair" and band_for(54) == "Long shot"
    assert risk_level([{"risk": "low"}, {"risk": "high"}])[0] == "High"
    assert risk_level([{"risk": "low"}, {"risk": "medium"}])[0] == "Medium"
    assert risk_level([])[0] == "not assessed"


def test_scoreboard_cli(tmp_path):
    tuned = tmp_path / "tuned.txt"
    tuned.write_text(TEXT, encoding="utf-8")
    jd = tmp_path / "jd.txt"
    jd.write_text("Senior Backend Engineer\nHarborline\nRequirements:\n- Go\n- PostgreSQL\n- Kubernetes\n",
                  encoding="utf-8")
    out = tmp_path / "sb.json"
    proc = run_script("scoreboard.py", "--asks", ASSETS / "example_jd_asks.json",
                      "--after", ASSETS / "example_grades.json", "--before", ASSETS / "example_grades.json",
                      "--base-text", tuned, "--tuned-text", tuned, "--jd", jd, "--json", out)
    assert "| Overall fit (0-100) |" in proc.stdout
    assert "Interview risk: High" in proc.stdout
    assert "terms marked not claimable are on the page: Terraform" in proc.stdout
    result = json.loads(out.read_text(encoding="utf-8"))
    assert result["fit_after"]["score"] == result["fit_before"]["score"]
    assert result["fit_after"]["band"] == "Good"  # capped: M6 graded none
