#!/usr/bin/env python3
"""Keyword overlap between a job posting and a resume: a deterministic 0-100 score.

Weights: job-title terms (line 1 of the posting) x4, terms under requirement headers x3,
other terms x2, preferred/nice-to-have terms x1, summed over repeats. The 60 heaviest one-
to three-word terms are kept; the score is the weighted share found in the resume.

This is a secondary signal. It rewards echoing the posting's wording, so a keyword-stuffed
resume outscores a better one. Use it to pick the best base resume among several, and use
its missing list to spot hard terms the candidate has but left out. Never chase the number.

Usage:
  python3 relevance_score.py --jd work/jd.txt --resume work/tuned.txt [--verbose] [--json OUT]

Both inputs are plain text: run extract_text.py on PDF or DOCX files first.
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

STOPWORDS = set("""a an the and or but if then else for while to of in on at by with from as is are was
were be been being have has had do does did will would can could should may might must shall not no nor
so than too very just about above after again against all am any because before below between both down
during each few further here how into it its itself more most other our ours out over own same she he
they them their theirs there these this those through under until up we what when where which who whom
why you your yours i me my myself him his her hers us who's you're we're they're
ability able across additional adept advantage applicants applicant apply application areas assist
background based basic bonus candidate candidates career company companies competitive compensation
consider culture currently day days demonstrated department description desire desired detail details
diverse dynamic e.g. eg employee employees employer environment etc equal equivalent excellent
exciting experience experiences familiar familiarity fast-paced field following full-time gain good
great growing help highly hire hiring ideal include includes including individual individuals industry
job join knowledge like looking love member minimum motivated must-have need needed needs new nice
offer opportunity opportunities orientation others part perks plus position preferred prior
qualification qualifications race related relevant religion required requirement requirements
responsibilities responsibility responsible role roles salary seeking sex skills solid someone strong
successful team teams time title understand understanding us using vision want we'll willing within
work working works world year years you'll""".split())

SECTION_MUST = re.compile(
    r"(requirement|qualification|must[- ]have|what you.ll need|what we.re looking for|"
    r"minimum|basic qualification|who you are|about you|you should have|you have|you bring|"
    r"what you.ll bring|what you bring|skills (?:and|&) experience|experience (?:and|&) skills|"
    r"essential|key skills|your profile)", re.I)
SECTION_NICE = re.compile(r"(preferred|nice[- ]to[- ]have|bonus|plus|desirable|extra credit)", re.I)
FRAGMENTS = {"re", "ll", "ve", "d", "s", "t", "m", "e.g", "i.e", "etc."}


def normalize(text):
    text = text.lower().replace("’", "'")
    text = re.sub(r"[^a-z0-9+#./\- ]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def tokens(text):
    out = []
    for t in normalize(text).split():
        t = t.strip(".").strip("-") or t  # trailing period or hyphen; keeps node.js
        if t in FRAGMENTS or re.fullmatch(r"\d+\+?", t):
            continue
        if len(t) > 1 or t in ("c", "r"):
            out.append(t)
    return out


def ngrams(toks, n):
    return [" ".join(toks[i:i + n]) for i in range(len(toks) - n + 1)]


def term_ok(term):
    parts = term.split()
    if any(p in STOPWORDS for p in parts):
        return False
    return not all(re.fullmatch(r"[\d.]+", p) for p in parts)


def extract_jd_terms(jd_text):
    """Return {term: weight} for the 60 heaviest terms."""
    weights = defaultdict(float)
    zone, zone_w = "general", {"must": 3.0, "nice": 1.0, "general": 2.0}
    title_done = company_skipped = False
    for line in jd_text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        is_header = len(stripped) < 70 and (stripped.endswith(":") or stripped.isupper()
                                            or len(stripped.split()) <= 6)
        if is_header and SECTION_NICE.search(stripped):
            zone = "nice"
            continue
        if is_header and SECTION_MUST.search(stripped):
            zone = "must"
            continue
        toks = tokens(stripped)
        if title_done and not company_skipped:
            company_skipped = True
            if len(toks) <= 6:  # the line right after the title is usually company or location
                continue
        line_terms = set()
        for segment in re.split(r"[,;•·|]", stripped):  # n-grams never span list items
            seg = tokens(segment)
            for n in (1, 2, 3):
                line_terms.update(g for g in ngrams(seg, n) if term_ok(g))
        w = zone_w[zone]
        if not title_done and len(toks) <= 8:  # the first real line is the job title
            w, title_done = 4.0, True
        for t in sorted(line_terms):  # sorted: set order is hash-randomised
            weights[t] += w
    ranked = sorted(weights.items(), key=lambda kv: (-kv[1], kv[0]))[:60]
    return dict(ranked)


def present(term, hay):
    variants = {term, term.replace("-", " "), term.replace(" ", "-"), term + "s"}
    if term.endswith("s") and len(term) > 3:
        variants.add(term[:-1])
    for v in variants:
        if re.search(r"(?:^| )" + re.escape(v) + r"(?:$| |[.,/)])", hay):
            return True
    return False


def score(jd_text, resume_text):
    terms = extract_jd_terms(jd_text)
    hay = " " + normalize(resume_text) + " "
    total = sum(terms.values())
    covered, missing = 0.0, []
    for term, w in sorted(terms.items(), key=lambda kv: (-kv[1], kv[0])):
        if present(term, hay):
            covered += w
        else:
            missing.append({"term": term, "weight": round(w, 1)})
    pct = 100.0 * covered / total if total else 0.0
    return round(pct, 1), missing, terms


def main():
    ap = argparse.ArgumentParser(description="Keyword overlap score (secondary signal, no target).")
    ap.add_argument("--jd", required=True)
    ap.add_argument("--resume", required=True)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", metavar="OUT", help="also write the result as JSON")
    args = ap.parse_args()
    for path in (args.jd, args.resume):
        try:
            head = Path(path).read_bytes()[:4]
        except OSError as err:
            sys.exit(f"relevance_score: {err}")
        if head.startswith(b"%PDF") or head.startswith(b"PK"):
            sys.exit(f"relevance_score: {path} is a PDF or DOCX. Extract its text first: "
                     f"python3 extract_text.py {path} -o {Path(path).stem}.txt")
    jd_text = Path(args.jd).read_text(encoding="utf-8", errors="ignore")
    resume_text = Path(args.resume).read_text(encoding="utf-8", errors="ignore")
    pct, missing, terms = score(jd_text, resume_text)
    if args.json:
        Path(args.json).write_text(json.dumps({"score": pct, "note": "secondary signal, no target",
                                               "terms_tracked": len(terms), "missing": missing[:25]},
                                              indent=2), encoding="utf-8")
    print(f"KEYWORD OVERLAP: {pct}/100 (a secondary signal with no target; never add posting prose to raise it)")
    if args.verbose:
        print(f"\nterms tracked: {len(terms)}, missing: {len(missing)}")
        if missing:
            print("\nTop missing terms (add only hard terms the candidate really has and a bullet or a "
                  "confirmed fact supports; never posting prose or adjectives):")
            for m in missing[:25]:
                print(f"  [{m['weight']:>5}]  {m['term']}")


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.stderr.close()
