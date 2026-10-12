#!/usr/bin/env python3
"""Check a compiled resume PDF the way an ATS parser and a recruiter will meet it.

Usage:
  python3 pdf_checks.py RESUME.pdf [--pages 1] [--require "exact text" ...] [--forbid "term" ...]
                        [--link URL ...] [--source work/resume.json] [--json work/pdf_checks.json]

Checks
  pages     the page count equals --pages (default 1)
  fill      empty space left at the bottom of the last page, in points and in body lines:
            FULL (at most one free line), UNDERFILLED (two or more), OVERFLOW (too many pages)
  text      garbled characters, (cid:N) codes, ligatures, fonts without a Unicode map,
            and whether two PDF readers agree on the words
  headers   Summary / Experience / Education / Skills come out as their own lines
  contact   an email and a phone number appear in the extracted text; clickable links listed
  links     every --link URL is a clickable link in the PDF
  strings   every --require text extracts exactly as written; no --forbid term appears
  source    words you wrote (--source: the resume JSON, .tex or .txt) that are missing from
            the PDF text, usually words glued together where bold meets regular text

Ends with:  PDF CHECKS: PASS  or  PDF CHECKS: FAIL (...)  followed by the FILL line.
"""
import argparse
import json
import math
import re
import shutil
import statistics
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from resume_text import clean, core_sections_found, find_term  # noqa: E402

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE = re.compile(r"\+?\d[\d ()\-.]{7,}\d")
GARBLE = re.compile(r"\(cid:\d+\)|[\x00-\x08\x0b\x0e-\x1f\x7f�]|[-]")
LIGATURE = re.compile(r"[ﬀ-ﬆ]")


# ------------------------------------------------------------------ layout and fill

def _pdfminer_pages(pdf_path):
    from pdfminer.high_level import extract_pages
    from pdfminer.layout import LTChar, LTFigure, LTTextContainer, LTTextLine

    def chars_in(obj):
        for child in obj:
            if isinstance(child, LTChar):
                yield child
            elif isinstance(child, LTFigure):
                yield from chars_in(child)

    pages = []
    for page in extract_pages(str(pdf_path)):
        lines = []
        for element in page:
            if isinstance(element, LTTextContainer):
                children = [element] if isinstance(element, LTTextLine) else list(element)
                for line in children:
                    if isinstance(line, LTTextLine) and line.get_text().strip():
                        lines.append((line.x0, line.y0, line.x1, line.y1, line.get_text().strip()))
            elif isinstance(element, LTFigure):  # text drawn inside a form object
                rows = {}
                for ch in chars_in(element):
                    if ch.get_text().strip():
                        rows.setdefault(round(ch.y0), []).append(ch)
                for chars in rows.values():
                    lines.append((min(c.x0 for c in chars), min(c.y0 for c in chars),
                                  max(c.x1 for c in chars), max(c.y1 for c in chars),
                                  "".join(c.get_text() for c in chars).strip()))
        pages.append({"width": float(page.width), "height": float(page.height), "lines": lines})
    return pages


def _pypdf_pages(pdf_path):
    from pypdf import PdfReader
    pages = []
    for page in PdfReader(str(pdf_path)).pages:
        found = []

        def visit(text, cm, tm, font_dict, font_size, found=found):
            if text and text.strip():
                y = tm[5] * cm[3] + cm[5]
                x = tm[4] * cm[0] + cm[4]
                size = abs(font_size * tm[3] * cm[3]) or 10.0
                found.append((x, y - 0.22 * size, x + 1, y + 0.8 * size, text.strip()))

        page.extract_text(visitor_text=visit)
        box = page.mediabox
        pages.append({"width": float(box.width), "height": float(box.height), "lines": found})
    return pages


def layout(pdf_path):
    try:
        return _pdfminer_pages(pdf_path), "pdfminer"
    except ImportError:
        return _pypdf_pages(pdf_path), "pypdf"


def fill_report(pdf_path, expected_pages=1):
    """Measure the empty space at the bottom of the last page."""
    pages, engine = layout(pdf_path)
    n = len(pages)
    report = {"pages": n, "expected_pages": expected_pages, "engine": engine}
    if n == 0 or not pages[-1]["lines"]:
        report.update(status="EMPTY", message="no text found on the last page")
        return report
    first, last = pages[0], pages[-1]
    height = last["height"]
    lines = last["lines"]
    top_gap_first = first["height"] - max(ln[3] for ln in first["lines"]) if first["lines"] else 36.0
    margin = min(max(top_gap_first, 18.0), 108.0)  # bottom margin taken to match the top one
    baselines = sorted({round(ln[1], 1) for ln in lines}, reverse=True)
    steps = [a - b for a, b in zip(baselines, baselines[1:]) if 4.0 <= a - b <= 40.0]
    pitch = statistics.median(steps) if steps else 12.0
    bottom = min(ln[1] for ln in lines)

    # A footer (page number, a closing line) far below the content is not content.
    footer = None
    below = sorted(lines, key=lambda ln: -ln[1])
    for i in range(len(below) - 1):
        gap = below[i][1] - below[i + 1][3]
        tail = below[i + 1:]
        if gap > 3 * pitch and len(tail) <= 2 and tail[0][1] < 1.25 * 72:
            footer = " / ".join(t[4] for t in tail)
            content_bottom = below[i][1]
            free_space = content_bottom - max(t[3] for t in tail) - pitch
            break
    else:
        free_space = bottom - margin

    free_lines = max(0, math.floor(free_space / pitch)) if free_space > 0 else 0
    top_of_text = max(ln[3] for ln in lines)
    usable = height - (height - top_of_text) - margin if n == 1 else height - 2 * margin
    used = top_of_text - (bottom if footer is None else content_bottom)
    report.update(
        page_height_pt=round(height, 1), bottom_margin_estimate_pt=round(margin, 1),
        lowest_text_pt=round(bottom, 1), line_pitch_pt=round(pitch, 1),
        free_space_pt=round(max(0.0, free_space), 1), free_lines=free_lines,
        fill_percent=round(100 * min(1.0, used / usable), 1) if usable > 0 else None,
        footer=footer,
    )
    if n > expected_pages:
        report.update(status="OVERFLOW",
                      message=f"{n} pages, {expected_pages} allowed: cut the least relevant content")
    elif free_lines >= 2:
        report.update(status="UNDERFILLED",
                      message=f"about {free_lines} free lines ({report['free_space_pt']:.0f} pt) at the "
                              "bottom: add that much relevant, true content")
    else:
        report.update(status="FULL", message="the page is full")
    if n < expected_pages:
        report["message"] += f" (note: {n} page(s), {expected_pages} expected)"
    return report


def fill_line(report):
    return f"FILL: {report['status']} - {report.get('message', '')}"


# ------------------------------------------------------------------ text, links, fonts

def read_texts(pdf_path):
    texts = {}
    if shutil.which("pdftotext"):
        try:
            out = subprocess.run(["pdftotext", "-enc", "UTF-8", str(pdf_path), "-"],
                                 capture_output=True, timeout=60, check=True)
            texts["pdftotext"] = out.stdout.decode("utf-8", errors="replace")
        except (subprocess.SubprocessError, OSError):
            pass
    try:
        from pypdf import PdfReader
        texts["pypdf"] = "\n".join((p.extract_text() or "") for p in PdfReader(str(pdf_path)).pages)
    except Exception:
        pass
    return texts


def link_uris(pdf_path):
    try:
        from pypdf import PdfReader
    except ImportError:
        return None
    uris = []
    for page in PdfReader(str(pdf_path)).pages:
        for annot in page.get("/Annots") or []:
            obj = annot.get_object()
            action = obj.get("/A")
            if action is not None:
                uri = action.get_object().get("/URI")
                if uri:
                    uris.append(str(uri))
    return uris


def _norm_url(url):
    url = url.strip().lower()
    url = re.sub(r"^(mailto:|https?://)?(www\.)?", "", url)
    return url.rstrip("/")


def font_report(pdf_path):
    if not shutil.which("pdffonts"):
        return None
    try:
        out = subprocess.run(["pdffonts", str(pdf_path)], capture_output=True, timeout=30,
                             check=True).stdout.decode("utf-8", errors="replace")
    except (subprocess.SubprocessError, OSError):
        return None
    fonts = []
    for row in out.splitlines()[2:]:
        cols = row.split()
        if len(cols) >= 5 and cols[-5] in ("yes", "no"):
            fonts.append({"name": cols[0], "type": " ".join(cols[1:-6]) or cols[1],
                          "embedded": cols[-5] == "yes", "unicode": cols[-3] == "yes"})
    return fonts


def source_text(path):
    path = Path(path)
    raw = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() == ".json":
        strings = []

        def walk(node):
            if isinstance(node, str):
                strings.append(node)
            elif isinstance(node, dict):
                for key, value in node.items():
                    if key not in ("skills_after", "paper", "location", "layout", "link"):
                        walk(value)
            elif isinstance(node, list):
                for item in node:
                    walk(item)
        walk(json.loads(raw))
        return "\n".join(strings)
    if path.suffix.lower() == ".tex":
        from extract_text import tex_text
        return tex_text(raw, keep_urls=False)
    return raw


def words_of(text):
    text = re.sub(r"([a-z])-\s*\n\s*([a-z])", r"\1\2", clean(text))
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&(?:[a-zA-Z]+|#\d+);", " ", text)
    return re.findall(r"[a-z]+", text.lower())


# ------------------------------------------------------------------ main

def run(args):
    pdf = Path(args.pdf)
    result = {"pdf": str(pdf), "fails": [], "warnings": []}
    fails, warns = result["fails"], result["warnings"]

    fill = fill_report(pdf, args.pages)
    result["fill"] = fill
    if fill["pages"] != args.pages:
        fails.append(f"{fill['pages']} pages (expected {args.pages})")

    texts = read_texts(pdf)
    if not texts:
        sys.exit("pdf_checks: no PDF text reader available. Install poppler-utils or pip install pypdf.")
    primary = texts.get("pdftotext") or texts.get("pypdf") or ""
    result["readers"] = sorted(texts)
    garbled = {name: len(GARBLE.findall(t)) for name, t in texts.items()}
    result["garbled_characters"] = garbled
    if any(garbled.values()):
        fails.append("garbled characters in the text layer " + str(garbled))
    ligatures = sum(len(LIGATURE.findall(t)) for t in texts.values())
    result["ligatures"] = ligatures
    if ligatures:
        warns.append(f"{ligatures} ligature characters (e.g. 'ﬁ'): some parsers misread words that contain them")
    if len(texts) == 2:
        a = set(re.findall(r"[a-z0-9]{3,}", clean(texts["pdftotext"]).lower()))
        b = set(re.findall(r"[a-z0-9]{3,}", clean(texts["pypdf"]).lower()))
        agreement = len(a & b) / max(1, len(a | b))
        result["reader_agreement"] = round(agreement, 3)
        if agreement < 0.9:
            warns.append(f"the two PDF readers agree on only {agreement:.0%} of words")

    fonts = font_report(pdf)
    result["fonts"] = fonts
    if fonts:
        no_map = sorted({f["name"] for f in fonts if not f["unicode"]})
        if no_map:
            warns.append("fonts without a Unicode map (text may extract badly): " + ", ".join(no_map))
        bitmap = sorted({f["name"] for f in fonts if f.get("type", "").startswith("Type 3")})
        if bitmap:
            warns.append("Type 3 (bitmap) fonts, usually LaTeX T1 encoding without a Type 1 font "
                         "package such as lmodern: " + ", ".join(bitmap))

    headers = core_sections_found(primary)
    result["headers"] = headers
    missing = [k for k, v in headers.items() if not v]
    if sum(headers.values()) < 2:
        fails.append("section headers not found in the text layer: " + ", ".join(missing))
    elif missing:
        warns.append("no header found for: " + ", ".join(missing))

    head = "\n".join(clean(primary).splitlines()[:12])
    result["email_found"] = bool(EMAIL.search(head))
    result["phone_found"] = bool(PHONE.search(head))
    if not result["email_found"]:
        fails.append("no email address near the top of the text layer")
    if not result["phone_found"]:
        warns.append("no phone number near the top of the text layer")

    uris = link_uris(pdf)
    result["links"] = uris
    if uris is not None:
        have = {_norm_url(u.replace("mailto:", "")) for u in uris}
        for want in args.link or []:
            if _norm_url(want) not in have:
                fails.append(f"link missing or different: {want}")
        if not uris and re.search(r"linkedin\.com|github\.com|https?://", primary, re.I):
            warns.append("profile URLs are printed but not clickable")

    flat = re.sub(r"\s+", " ", clean(primary))
    for text in args.require or []:
        if re.sub(r"\s+", " ", clean(text)).strip() not in flat:
            fails.append(f"required text not found exactly: {text!r}")
    for term in args.forbid or []:
        if find_term(term, primary) or find_term(term, primary, loose=True):
            fails.append(f"forbidden term present: {term!r}")

    if args.source:
        # Check every reader: parsers differ, and a word glued in one of them ("Engineerworking")
        # is a word some ATS will miss.
        wrote = {w for w in words_of(source_text(args.source)) if len(w) >= 4}
        lost, glued = {}, {}
        for name, text in texts.items():
            got = set(words_of(text))
            for w in sorted(wrote - got):
                hits = [g for g in got if w in g and g != w]
                (glued if hits else lost).setdefault(w, set()).add(name)
        result["glued_words"] = {w: sorted(v) for w, v in sorted(glued.items())[:40]}
        result["lost_words"] = {w: sorted(v) for w, v in sorted(lost.items())[:40]}
        if glued:
            fails.append("words glued together in the text layer: "
                         + ", ".join(f"{w} ({'/'.join(sorted(v))})" for w, v in list(glued.items())[:8]))
        if lost:
            warns.append("words from the source not found in the PDF text: "
                         + ", ".join(f"{w} ({'/'.join(sorted(v))})" for w, v in list(lost.items())[:8]))

    if args.source and str(args.source).lower().endswith(".json"):
        detached = date_order(json.loads(Path(args.source).read_text(encoding="utf-8")), texts)
        result["detached_dates"] = detached
        if detached:
            warns.append("dates come out after the entry's bullets or past the next entry in: "
                         + "; ".join(f"{d['org']} ({'/'.join(d['readers'])})" for d in detached[:5])
                         + ". Re-render with --dates inline")

    result["verdict"] = "FAIL" if fails else "PASS"
    return result


def date_order(data, texts):
    """Entries whose dates a reader places after their bullets or beyond the next entry."""
    entries = [e for sec in data.get("sections", []) for e in sec.get("entries", [])
               if e.get("org") and e.get("dates")]
    problems = {}
    for name, text in texts.items():
        flat = re.sub(r"\s+", " ", clean(text))
        pos = 0
        for i, e in enumerate(entries):
            start = flat.find(e["org"], pos)
            if start < 0:
                continue
            pos = start + len(e["org"])
            nxt = flat.find(entries[i + 1]["org"], pos) if i + 1 < len(entries) else -1
            end = nxt if nxt >= 0 else len(flat)
            date_at = flat.find(re.sub(r"\s+", " ", e["dates"]), start)
            first_bullet = flat.find(e["bullets"][0][:30], start) if e.get("bullets") else -1
            if date_at < 0 or date_at > end or (0 <= first_bullet < date_at):
                problems.setdefault(e["org"], set()).add(name)
    return [{"org": org, "readers": sorted(r)} for org, r in problems.items()]


def main():
    ap = argparse.ArgumentParser(description="ATS and page-fill checks for a resume PDF.")
    ap.add_argument("pdf")
    ap.add_argument("--pages", type=int, default=1, help="allowed page count (default 1)")
    ap.add_argument("--require", action="append", metavar="TEXT", help="text that must extract exactly")
    ap.add_argument("--forbid", action="append", metavar="TERM", help="term that must not appear")
    ap.add_argument("--link", action="append", metavar="URL", help="URL that must be a clickable link")
    ap.add_argument("--source", help="what you wrote: resume JSON, .tex or .txt (finds glued words)")
    ap.add_argument("--json", metavar="OUT", help="also write the full result as JSON")
    args = ap.parse_args()
    if not Path(args.pdf).exists():
        sys.exit(f"pdf_checks: {args.pdf} not found")
    r = run(args)
    if args.json:
        Path(args.json).write_text(json.dumps(r, indent=2, ensure_ascii=False), encoding="utf-8")
    f = r["fill"]
    print(f"pages: {f['pages']} (expected {f['expected_pages']})")
    if "free_lines" in f:
        print(f"fill: {f.get('fill_percent')}% of the usable page; lowest text {f['lowest_text_pt']} pt "
              f"from the bottom edge; about {f['free_lines']} free lines "
              f"(line pitch {f['line_pitch_pt']} pt)" + (f"; footer: {f['footer']!r}" if f.get("footer") else ""))
    print(f"readers: {', '.join(r['readers'])}; garbled characters: {r['garbled_characters']}"
          + (f"; reader agreement {r['reader_agreement']:.0%}" if "reader_agreement" in r else ""))
    print(f"headers: {r['headers']}")
    print(f"email: {'yes' if r['email_found'] else 'NO'}, phone: {'yes' if r['phone_found'] else 'no'}, "
          f"links: {r['links'] if r['links'] is not None else 'unknown (pypdf missing)'}")
    if r.get("glued_words") or r.get("lost_words"):
        print(f"glued words: {r.get('glued_words') or 'none'}; other missing words: {r.get('lost_words') or 'none'}")
    for w in r["warnings"]:
        print(f"warning: {w}")
    print("PDF CHECKS: " + (r["verdict"] if not r["fails"] else "FAIL (" + "; ".join(r["fails"]) + ")"))
    print(fill_line(f))


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.stderr.close()
