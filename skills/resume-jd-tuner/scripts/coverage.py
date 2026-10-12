#!/usr/bin/env python3
"""How much of a job posting a resume covers.

Two views:
  hard terms  tools, platforms, languages, certifications and other exact names an ATS keyword
              search looks for. Counted only in the posting's own spelling ("Kubernetes" is
              not "K8s"). A term found only in another spelling is listed so you can switch
              to the posting's spelling where it is true.
  asks        the posting's requirements and responsibilities, matched through their "alts"
              phrases (case-insensitive, simple suffixes). A rough pointer for the writer;
              the hiring-manager agent's grading is the real measure of fit.

Usage:
  python3 coverage.py work/jd_asks.json work/tuned.txt [--json work/coverage_after.json]

ATS alignment = 100 x (2 x must-have terms present + nice-to-have terms present)
                    / (2 x must-have terms + nice-to-have terms)
Honest ceiling = the same formula counting only the terms the candidate can truthfully claim.
A score above the ceiling means a term marked not claimable is on the page: check it.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from resume_text import clean, find_term, skills_and_prose  # noqa: E402

WEIGHT = {"must": 2, "nice": 1}


def load_asks(path):
    """Read work/jd_asks.json. A bare list is read as the older asks-only format."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, list):  # older format: [{"ask", "type", "alts"}], type "gap" = not claimable
        asks = []
        for i, a in enumerate(data, 1):
            kind = a.get("type", "must")
            asks.append({"id": a.get("id", f"A{i}"), "ask": a.get("ask", ""),
                         "type": "must" if kind == "gap" else kind,
                         "alts": a.get("alts", []), "claimable": kind != "gap"})
        return {"role": {}, "asks": asks, "hard_terms": [], "do_not_echo": []}
    data.setdefault("role", {})
    data.setdefault("asks", [])
    data.setdefault("hard_terms", [])
    data.setdefault("do_not_echo", [])
    return data


def ask_found(phrase, text):
    phrase = clean(phrase).strip()
    if not phrase:
        return False
    body = r"[\s\-]+".join(re.escape(p) for p in phrase.split())
    pattern = r"(?<![A-Za-z0-9])" + body + r"(?:s|es|ed|d|ing)?(?![A-Za-z0-9])"
    return re.search(pattern, clean(text), re.I) is not None


def compute(data, text):
    skills_text, prose_text = skills_and_prose(text)
    terms = []
    for t in data["hard_terms"]:
        term = t.get("term", "").strip()
        if not term:
            continue
        kind = t.get("type", "must") if t.get("type") in WEIGHT else "nice"
        # "PyTorch or TensorFlow": one requirement, met by any of the named alternatives.
        options = [term] + [a for a in t.get("alternatives", []) if a and a.strip()]
        matched = next((o for o in options if find_term(o, text)), None)
        variant = None
        if not matched:
            for v in options + list(t.get("variants", [])):
                if find_term(v, text, loose=True):
                    variant = v
                    break
        where = []
        if matched and find_term(matched, skills_text):
            where.append("skills")
        # In use in a bullet or the summary under any of its names ("GitHub pull requests" for Git).
        spellings = [matched] + [v for v in options + list(t.get("variants", [])) if v != matched]
        if matched and any(find_term(v, prose_text, loose=v != matched) for v in spellings):
            where.append("experience/summary")
        label = term + "".join(f" / {a}" for a in options[1:])
        terms.append({"term": label, "type": kind, "claimable": bool(t.get("claimable", True)),
                      "present": matched is not None, "matched": matched, "other_spelling": variant,
                      "where": where})

    def score(rows):
        total = sum(WEIGHT[r["type"]] for r in rows)
        got = sum(WEIGHT[r["type"]] for r in rows if r["present"])
        ceiling = sum(WEIGHT[r["type"]] for r in rows if r["claimable"])
        if not total:
            return None, None
        return round(100 * got / total, 1), round(100 * ceiling / total, 1)

    ats, ceiling = score(terms)
    asks = []
    for a in data["asks"]:
        alts = [x for x in a.get("alts", []) if x] or [a.get("ask", "")]
        asks.append({"id": a.get("id", ""), "ask": a.get("ask", ""), "type": a.get("type", "role"),
                     "claimable": bool(a.get("claimable", True)),
                     "found": any(ask_found(x, text) for x in alts)})

    def tally(rows, kind, key):
        sub = [r for r in rows if r["type"] == kind]
        return sum(1 for r in sub if r[key]), len(sub)

    summary = {
        "ats_alignment": ats,
        "honest_ceiling": ceiling,
        "must_terms_present": tally(terms, "must", "present"),
        "nice_terms_present": tally(terms, "nice", "present"),
        "claimable_terms_missing": [r["term"] for r in terms if r["claimable"] and not r["present"]],
        "unclaimable_terms_present": [r["term"] for r in terms if not r["claimable"] and r["present"]],
        "terms_only_in_skills": [r["term"] for r in terms if r["where"] == ["skills"]],
        "asks_found": {k: tally(asks, k, "found") for k in ("must", "role", "nice")},
    }
    return {"summary": summary, "hard_terms": terms, "asks": asks}


def main():
    ap = argparse.ArgumentParser(description="Hard-term and ask coverage of a resume against a posting.")
    ap.add_argument("jd_asks_json")
    ap.add_argument("resume_txt")
    ap.add_argument("--json", metavar="OUT", help="also write the full result as JSON")
    args = ap.parse_args()
    try:
        data = load_asks(args.jd_asks_json)
        text = Path(args.resume_txt).read_text(encoding="utf-8", errors="replace")
    except (OSError, json.JSONDecodeError) as err:
        sys.exit(f"coverage: {err}")
    r = compute(data, text)
    if args.json:
        Path(args.json).write_text(json.dumps(r, indent=2, ensure_ascii=False), encoding="utf-8")
    s = r["summary"]
    if s["ats_alignment"] is None:
        print("no hard terms in jd_asks.json: add the posting's tools, platforms and certifications")
    else:
        mp, mt = s["must_terms_present"]
        np_, nt = s["nice_terms_present"]
        print(f"ATS alignment: {s['ats_alignment']}/100 (honest ceiling {s['honest_ceiling']}); "
              f"must-have terms {mp}/{mt}, nice-to-have terms {np_}/{nt}")
    for t in r["hard_terms"]:
        if t["present"] and not t["claimable"]:
            mark = "CHECK  "
        elif t["present"]:
            mark = "ok     "
        elif t["other_spelling"]:
            mark = "SPELL  "
        elif t["claimable"]:
            mark = "MISSING"
        else:
            mark = "gap    "
        note = ""
        if t["present"] and not t["claimable"]:
            note = "  (on the page but marked not claimable: confirm it is true or remove it)"
        elif t["other_spelling"]:
            note = f"  (found as {t['other_spelling']!r}: use the posting's spelling if true)"
        elif t["where"] == ["skills"]:
            note = "  (only in Skills: show it in use in a bullet if you can)"
        print(f"  {mark} [{t['type']}] {t['term']}{note}")
    found = s["asks_found"]
    print("asks matched by phrase: " + ", ".join(f"{k} {v[0]}/{v[1]}" for k, v in found.items() if v[1]))
    for a in r["asks"]:
        if not a["found"]:
            tag = "" if a["claimable"] else " (not claimable)"
            print(f"  not matched [{a['type']}] {a['id']} {a['ask']}{tag}")


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.stderr.close()
