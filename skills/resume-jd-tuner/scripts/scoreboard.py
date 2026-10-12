#!/usr/bin/env python3
"""Compute the numbers for the fit report, before and after tuning, the same way every time.

Usage:
  python3 scoreboard.py --asks work/jd_asks.json --after work/grades_after.json
                        [--before work/grades_before.json]
                        [--base-text work/base.txt] [--tuned-text work/tuned.txt] [--jd work/jd.txt]
                        [--checks work/pdf_checks.json] [--slop work/slop.json]
                        [--json work/scoreboard.json]

Prints a Markdown block to paste into fit_report.md. Formulas (see references/scoring.md):

  Overall fit   each ask graded clear = 1, weak = 0.5, none = 0; weights must 3, role 2, nice 1;
                fit = 100 x weighted sum / total weight.
                Bands: 85+ Strong, 70-84 Good, 55-69 Fair, below 55 Long shot.
                One must-have graded none caps the band at Good; two or more cap it at Fair.
  ATS alignment hard-term coverage in the posting's spelling, must-haves counted twice
                (coverage.py), with the honest ceiling: the best score possible without
                claiming anything untrue.
  Interview risk  High if any probed claim is high risk, Medium if any is medium, else Low.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from coverage import compute as coverage_compute  # noqa: E402
from coverage import load_asks
from relevance_score import score as keyword_score  # noqa: E402
from resume_text import utf8_stdio  # noqa: E402

VALUE = {"clear": 1.0, "weak": 0.5, "none": 0.0}
WEIGHT = {"must": 3, "role": 2, "nice": 1}
BANDS = [(85, "Strong"), (70, "Good"), (55, "Fair"), (0, "Long shot")]
ORDER = ["Long shot", "Fair", "Good", "Strong"]


def band_for(score):
    return next(name for floor, name in BANDS if score >= floor)


def fit(asks, grades_doc, warnings, label):
    grades = {str(g.get("id")): g for g in grades_doc.get("grades", [])}
    total = got = 0.0
    unmet, clear_musts, musts = [], 0, 0
    for a in asks:
        kind = a.get("type", "role")
        w = WEIGHT.get(kind, 2)
        g = grades.get(str(a.get("id")))
        if g is None:
            warnings.append(f"{label}: no grade for ask {a.get('id')} ({a.get('ask')}); counted as none")
            value = 0.0
        else:
            grade = str(g.get("grade", "none")).lower()
            if grade not in VALUE:
                warnings.append(f"{label}: unknown grade {grade!r} for {a.get('id')}; counted as none")
            value = VALUE.get(grade, 0.0)
        total += w
        got += w * value
        if kind == "must":
            musts += 1
            clear_musts += value == 1.0
            if value == 0.0:
                unmet.append(a.get("ask", a.get("id")))
    extra = set(grades) - {str(a.get("id")) for a in asks}
    if extra:
        warnings.append(f"{label}: grades for unknown ask ids ignored: {sorted(extra)}")
    if not total:
        return None
    score = round(100 * got / total)
    band = band_for(score)
    cap = None
    if len(unmet) >= 2 and ORDER.index(band) > ORDER.index("Fair"):
        band, cap = "Fair", f"{len(unmet)} must-haves not shown"
    elif len(unmet) == 1 and ORDER.index(band) > ORDER.index("Good"):
        band, cap = "Good", "one must-have not shown"
    return {"score": score, "band": band, "cap": cap, "musts_clear": clear_musts, "musts": musts,
            "musts_unmet": unmet}


def risk_level(risks):
    levels = [str(r.get("risk", "")).lower() for r in risks]
    if not levels:
        return "not assessed", {}
    counts = {k: levels.count(k) for k in ("high", "medium", "low")}
    level = "High" if counts["high"] else "Medium" if counts["medium"] else "Low"
    return level, counts


def load_json(path, warnings):
    if not path:
        return None
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as err:
        warnings.append(f"could not read {path}: {err}")
        return None


def read_text(path, warnings):
    if not path:
        return None
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError as err:
        warnings.append(f"could not read {path}: {err}")
        return None


def build(args):
    warnings = []
    data = load_asks(args.asks)
    asks = data["asks"]
    after_doc = load_json(args.after, warnings) or {}
    before_doc = load_json(args.before, warnings)
    result = {"warnings": warnings}
    result["fit_after"] = fit(asks, after_doc, warnings, "after")
    result["fit_before"] = fit(asks, before_doc, warnings, "before") if before_doc else None

    base, tuned, jd = (read_text(p, warnings) for p in (args.base_text, args.tuned_text, args.jd))
    if tuned is not None:
        result["ats_after"] = coverage_compute(data, tuned)["summary"]
    if base is not None:
        result["ats_before"] = coverage_compute(data, base)["summary"]
    if jd is not None:
        if tuned is not None:
            result["keywords_after"] = keyword_score(jd, tuned)[0]
        if base is not None:
            result["keywords_before"] = keyword_score(jd, base)[0]

    level, counts = risk_level(after_doc.get("risks", []))
    result["interview_risk"] = {"level": level, "counts": counts}
    result["recruiter"] = after_doc.get("recruiter", {})
    checks = load_json(args.checks, warnings)
    if checks:
        result["pdf_checks"] = {"verdict": checks.get("verdict"), "fails": checks.get("fails", []),
                                "fill": checks.get("fill", {}).get("status"),
                                "free_lines": checks.get("fill", {}).get("free_lines")}
    slop = load_json(args.slop, warnings)
    if slop:
        result["slop"] = {"verdict": slop.get("verdict"), "line": slop.get("verdict_line")}
    return result


def fmt_fit(f):
    if not f:
        return "-"
    return f"{f['score']} ({f['band']})"


def fmt_musts(f):
    return f"{f['musts_clear']} of {f['musts']}" if f and f["musts"] else "-"


def markdown(r):
    rows = ["| Measure | Before | After |", "|---|---|---|"]
    rows.append(f"| Overall fit (0-100) | {fmt_fit(r.get('fit_before'))} | {fmt_fit(r.get('fit_after'))} |")
    rows.append(f"| Must-haves shown clearly | {fmt_musts(r.get('fit_before'))} | {fmt_musts(r.get('fit_after'))} |")
    a_before, a_after = r.get("ats_before"), r.get("ats_after")
    if a_after and a_after.get("ats_alignment") is not None:
        before = f"{a_before['ats_alignment']}" if a_before else "-"
        after = f"{a_after['ats_alignment']} (honest ceiling {a_after['honest_ceiling']})"
        rows.append(f"| ATS alignment (0-100) | {before} | {after} |")
        mp, mt = a_after["must_terms_present"]
        mb = f"{a_before['must_terms_present'][0]} of {mt}" if a_before else "-"
        rows.append(f"| Must-have hard terms present | {mb} | {mp} of {mt} |")
    if "keywords_after" in r:
        rows.append(f"| Keyword overlap (secondary, no target) | {r.get('keywords_before', '-')} | "
                    f"{r['keywords_after']} |")
    lines = ["\n".join(rows), ""]
    fa = r.get("fit_after")
    if fa and fa.get("cap"):
        lines.append(f"Fit band capped at {fa['band']}: {fa['cap']} ({'; '.join(map(str, fa['musts_unmet']))}).")
    ir = r["interview_risk"]
    if ir["counts"]:
        c = ir["counts"]
        lines.append(f"Interview risk: {ir['level']} ({c['high']} high, {c['medium']} medium, {c['low']} low)")
    else:
        lines.append("Interview risk: not assessed")
    rec = r.get("recruiter") or {}
    if rec:
        lines.append(f"Recruiter screen: shortlist {rec.get('shortlist', '?')}; "
                     f"reads-as-human score {rec.get('slop_score', '?')}/10")
    quality = []
    if r.get("slop"):
        quality.append(f"slop gates {r['slop']['verdict']}")
    if r.get("pdf_checks"):
        pc = r["pdf_checks"]
        quality.append(f"PDF checks {pc['verdict']}")
        if pc.get("fill"):
            n = pc.get("free_lines")
            quality.append(f"page {pc['fill']}" + (f" ({n} free line{'s' if n != 1 else ''})" if n else ""))
    if quality:
        lines.append("Quality: " + "; ".join(quality))
    a_after = r.get("ats_after")
    if a_after and a_after.get("claimable_terms_missing"):
        lines.append("Claimable hard terms still missing: " + ", ".join(a_after["claimable_terms_missing"]))
    if a_after and a_after.get("unclaimable_terms_present"):
        lines.append("WARNING: terms marked not claimable are on the page: "
                     + ", ".join(a_after["unclaimable_terms_present"]) + " (confirm or remove)")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Fit, ATS alignment and interview-risk numbers for the report.")
    ap.add_argument("--asks", required=True, help="work/jd_asks.json")
    ap.add_argument("--after", required=True, help="grades of the tuned resume (hiring-manager agent)")
    ap.add_argument("--before", help="grades of the base resume")
    ap.add_argument("--base-text", help="text of the base resume")
    ap.add_argument("--tuned-text", help="text extracted from the tuned PDF")
    ap.add_argument("--jd", help="the scoring copy of the posting (work/jd.txt)")
    ap.add_argument("--checks", help="pdf_checks.py --json output")
    ap.add_argument("--slop", help="slop_scan.py --json output")
    ap.add_argument("--json", metavar="OUT", help="also write the numbers as JSON")
    args = ap.parse_args()
    try:
        result = build(args)
    except (OSError, json.JSONDecodeError) as err:
        sys.exit(f"scoreboard: {err}")
    if args.json:
        Path(args.json).write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(markdown(result))
    for w in result["warnings"]:
        print(f"warning: {w}", file=sys.stderr)


if __name__ == "__main__":
    utf8_stdio()
    try:
        main()
    except BrokenPipeError:
        sys.stderr.close()
