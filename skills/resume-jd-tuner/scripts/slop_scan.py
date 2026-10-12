#!/usr/bin/env python3
"""Slop gates for a tuned resume. Run it on the text extracted from the compiled PDF.

Usage:
  python3 slop_scan.py work/tuned.txt [work/jd.txt] [--json work/slop.json]

It reads only the prose (summary, experience, projects); skills, education, headers,
role and date lines are skipped. It ends with one verdict line:

  SLOP GATES: PASS
  SLOP GATES: REVIEW (...)   judge every listed item; product names and real technical terms are fine
  SLOP GATES: FAIL (...)     rewrite before going further

The gates are suspects, not proof. The reviewer agents make the final call.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from resume_text import BULLET, NON_PROSE, clean, is_header, utf8_stdio  # noqa: E402

# Word stems that read as machine-written or as filler on a resume. Matched at a word start.
BANNED = [
    "leverag", "robust", "seamless", "spearhead", "drove adoption", "drive adoption", "drives adoption",
    "drove growth", "drive growth", "drives growth", "drove revenue", "drive revenue", "ensur",
    "foster", "empower", "elevat", "streamlin", "unlock", "holistic", "synerg", "cutting-edge",
    "state-of-the-art", "world-class", "best-in-class", "end-to-end", "passionate", "dynamic",
    "innovative", "impactful", "journey", "delve", "navigat", "trusted advisor",
    "technical advisor", "production-ready", "production-grade", "enterprise-grade",
    "cross-functional", "proven track record", "results-driven", "detail-oriented",
    "ambiguity", "stakeholders alike", "fluently", "game-changing", "transformative",
    "mission-critical", "tapestry", "testament", "pivotal", "meticulous",
]
WEAK_OPENERS = ("responsible for", "helped", "worked on", "assisted", "involved in",
                "participated in", "tasked with")
# -ing words that are usually nouns in a list (", onboarding processes"), not participle tails.
GERUND_NOUNS = {
    "onboarding", "offboarding", "routing", "pricing", "billing", "testing", "logging", "monitoring",
    "training", "hiring", "recruiting", "marketing", "engineering", "accounting", "banking",
    "computing", "networking", "processing", "rendering", "caching", "scheduling", "staffing",
    "sourcing", "tracking", "ticketing", "reporting", "budgeting", "forecasting", "planning",
    "learning", "mining", "scraping", "alerting", "auditing", "licensing", "messaging", "publishing",
    "streaming", "tooling", "underwriting", "nursing", "teaching", "consulting", "manufacturing",
    "packaging", "shipping", "housing", "lending", "trading", "advertising", "branding",
    "fundraising", "copywriting", "editing", "modeling", "modelling", "labeling", "labelling",
}
_MONTH = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?,?\s+"
_DATE = rf"(?:{_MONTH})?(?:\d{{1,2}}/)?\d{{4}}"
DATE_RANGE = re.compile(
    rf"\b{_DATE}\s*(?:–|—|-{{1,2}}|to)\s*(?:{_DATE}|Present|Current|Now|Ongoing|Today)\b", re.I)
BULLET_START = BULLET  # shared pattern, see resume_text.py


def prose_lines(text):
    """Return the prose lines of the resume, one bullet per item, headers and list sections removed."""
    lines = [BULLET_START.sub("• ", raw.strip()) if BULLET_START.match(raw.strip()) else raw.strip()
             for raw in clean(text).splitlines()]
    first = next((i for i, line in enumerate(lines) if is_header(line)), None)
    warnings = []
    if first is None:
        warnings.append("no section headers found: the whole text was treated as prose")
        first = 0
    out, section, prev_ended = [], "", True
    for line in lines[first:]:
        if not line:
            continue
        if is_header(line):
            section, prev_ended = line.upper(), True
            continue
        if any(word in section for word in NON_PROSE):
            continue
        if re.fullmatch(r"\[.*\]", line) or (" | " in line and not line.startswith("•")):
            continue
        line = DATE_RANGE.sub(" ", line).strip(" ,|")
        if not line:
            continue
        is_bullet = line.startswith("•")
        short = len(line.split()) <= 8 and not line.endswith((".", "!", "?"))
        if not is_bullet and prev_ended and short:
            continue  # an employer, title or location line, not prose
        out.append(line)
        prev_ended = line.endswith((".", "!", "?"))
    return out, warnings


def grams(text, n):
    words = re.findall(r"[\w+#/'\-]+", text.lower())
    return {" ".join(words[i:i + n]) for i in range(len(words) - n + 1)}


def scan(resume_text, jd_text=""):
    lines, warnings = prose_lines(resume_text)
    prose = re.sub(r"\s+", " ", " ".join(lines)).strip()
    bullets = [b.strip() for b in re.split(r"\s*•\s*", prose) if len(b.split()) > 4]
    sentences = [s for b in bullets for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", b)
                 if len(s.split()) > 3]
    lengths = [len(s.split()) for s in sentences] or [0]
    average, longest = sum(lengths) / len(lengths), max(lengths)

    dashes = prose.count("—") + prose.count(" – ") + prose.count(" -- ")
    semicolons = prose.count(";")
    colon_led = [b for b in bullets if re.match(r"^[^.:]{3,60}:\s", b)]
    lower = prose.lower()
    banned = {}
    for stem in BANNED:
        hits = len(re.findall(r"(?<![a-z])" + re.escape(stem), lower))
        if hits:
            banned[stem] = hits
    ing_tails = [w for w in re.findall(r", (?!including\b)(\w+ing)\b(?!\s*(?:,|and\b|or\b))", prose)
                 if w.lower() not in GERUND_NOUNS]
    weak = sorted({b.split(".")[0][:60] for b in bullets if b.lower().startswith(WEAK_OPENERS)})
    not_just = re.findall(r"\bnot (?:just|only)\b[^.]{0,80}\bbut\b", lower)
    openers = {}
    for b in bullets:
        first_word = re.sub(r"[^a-z]", "", b.split()[0].lower()) if b.split() else ""
        if first_word:
            openers[first_word] = openers.get(first_word, 0) + 1
    repeated_openers = {w: c for w, c in openers.items() if c > 3}
    shared4 = sorted(grams(prose, 4) & grams(jd_text, 4)) if jd_text else []
    shared5 = sorted(grams(prose, 5) & grams(jd_text, 5)) if jd_text else []
    metrics = re.findall(r"\d[\d,.]*\s?%|\b\d[\d,]*\+", prose)
    repeated_metrics = sorted({m for m in metrics if metrics.count(m) > 1})

    fails, review = [], []
    if dashes:
        fails.append("dashes in prose")
    if semicolons:
        fails.append("semicolons in prose")
    if len(colon_led) > 2:
        fails.append("more than 2 colon-led bullets")
    if len(ing_tails) > 3:
        fails.append("more than 3 ', -ing' tails")
    if average > 20:
        fails.append("average sentence over 20 words")
    if longest > 35:
        fails.append("a sentence over 35 words")
    if 0 < len(colon_led) <= 2:
        review.append("colon-led bullets")
    if banned:
        review.append("banned words")
    if shared4 or shared5:
        review.append("word runs shared with the JD")
    if 0 < len(ing_tails) <= 3:
        review.append("', -ing' tails")
    if weak:
        review.append("weak openers")
    if not_just:
        review.append("'not just X but Y'")
    if repeated_openers:
        review.append("same opening verb on more than 3 bullets")
    if repeated_metrics:
        review.append("a metric repeated")
    if fails:
        verdict = "FAIL (" + "; ".join(fails + review) + ")"
    elif review:
        verdict = "REVIEW (" + "; ".join(review) + ")"
    else:
        verdict = "PASS"
    return {
        "verdict": verdict.split(" ")[0],
        "verdict_line": "SLOP GATES: " + verdict,
        "warnings": warnings,
        "prose_words": len(prose.split()),
        "bullets": len(bullets),
        "sentences": len(sentences),
        "average_sentence_words": round(average, 1),
        "longest_sentence_words": longest,
        "long_sentences": [s for s in sentences if len(s.split()) > 30],
        "dashes": dashes,
        "semicolons": semicolons,
        "colon_led_bullets": colon_led,
        "banned_words": banned,
        "ing_tails": ing_tails,
        "weak_openers": weak,
        "not_just_but": not_just,
        "repeated_openers": repeated_openers,
        "metric_tokens": metrics,
        "repeated_metrics": repeated_metrics,
        "shared_4_word_runs": shared4,
        "shared_5_word_runs": shared5,
        "fails": fails,
        "review": review,
    }


def main():
    ap = argparse.ArgumentParser(description="Flag AI-slop suspects in resume prose.")
    ap.add_argument("resume_txt", help="text extracted from the compiled resume PDF")
    ap.add_argument("jd_txt", nargs="?", help="the job posting text (optional, enables echo checks)")
    ap.add_argument("--json", metavar="OUT", help="also write the full result as JSON")
    args = ap.parse_args()
    try:
        resume = Path(args.resume_txt).read_text(encoding="utf-8", errors="replace")
        jd = Path(args.jd_txt).read_text(encoding="utf-8", errors="replace") if args.jd_txt else ""
    except OSError as err:
        sys.exit(f"slop_scan: {err}")
    r = scan(resume, clean(jd))
    if args.json:
        Path(args.json).write_text(json.dumps(r, indent=2, ensure_ascii=False), encoding="utf-8")
    for w in r["warnings"]:
        print(f"warning: {w}")
    print(f"prose words: {r['prose_words']}, bullets: {r['bullets']}, sentences: {r['sentences']}")
    print(f"average sentence: {r['average_sentence_words']} words, longest: {r['longest_sentence_words']}")
    for s in r["long_sentences"]:
        print(f"   [{len(s.split())}] {s[:120]}")
    print(f"dashes in prose: {r['dashes']}, semicolons: {r['semicolons']}, "
          f"colon-led bullets: {len(r['colon_led_bullets'])}")
    print(f"banned words: {r['banned_words'] or 'none'}")
    print(f"', -ing' tails: {r['ing_tails'] or 'none'}")
    print(f"weak openers: {r['weak_openers'] or 'none'}")
    print(f"'not just X but Y': {len(r['not_just_but'])}")
    print(f"opening verbs used on more than 3 bullets: {r['repeated_openers'] or 'none'}")
    print(f"metric tokens ({len(r['metric_tokens'])}): {r['metric_tokens']}; "
          f"repeated: {r['repeated_metrics'] or 'none'}")
    if jd:
        print(f"4-word runs shared with the JD ({len(r['shared_4_word_runs'])}): {r['shared_4_word_runs']}")
        print(f"5-word runs shared with the JD ({len(r['shared_5_word_runs'])}): {r['shared_5_word_runs']}")
    print(r["verdict_line"])


if __name__ == "__main__":
    utf8_stdio()
    try:
        main()
    except BrokenPipeError:
        sys.stderr.close()
