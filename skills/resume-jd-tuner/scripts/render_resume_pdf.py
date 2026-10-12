#!/usr/bin/env python3
"""Render a resume JSON file into a clean, ATS-safe, Harvard-style one-page PDF.

Usage:
  python3 render_resume_pdf.py work/resume.json -o First_Last_Role.pdf
          [--paper letter|a4] [--font-size 10.5] [--spacing 1.0] [--dates right|inline] [--fill]

--spacing  scales the gaps between entries and, more gently, the line height (0.8 to 1.5).
--dates    right (default): location and dates right-aligned, the classic Harvard look.
           inline: "Role | Mon YYYY - Mon YYYY" on one line, which every PDF reader keeps in
           order. Use it when pdf_checks.py warns that dates come out detached from their role.
--fill     last resort for a page that is still short after every true, relevant line has
           been added: raises spacing (up to 1.5) and then the font (up to 11 pt) until the
           page is full, staying within the page count. It never adds or changes words.
--pages    allowed page count, 1 (default) or 2.

Layout choices can also live in the JSON, so every rebuild uses the same settings:
  "layout": {"paper": "a4", "font_size": 10.5, "spacing": 1.0, "dates": "inline", "fill": true, "pages": 1}
Command-line options override the JSON.

Input format: assets/resume_schema.json (example: assets/example_resume.json).
Needs reportlab (pip install reportlab).

The PDF uses the bundled Liberation Serif font (assets/fonts, SIL Open Font License), so the
text layer carries real Unicode: bullets, accents and dashes extract as themselves. PDFs
built with the PDF base fonts turn the bullet into a control character in common parsers,
which is the kind of silent ATS damage this renderer avoids. Emails and profile URLs in the
contact line become clickable links.

After writing the file it prints the page count and how much space is left at the bottom.
"""
import argparse
import json
import re
import sys
from pathlib import Path

try:
    from reportlab import rl_config
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT
    from reportlab.lib.pagesizes import A4, letter
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
except ImportError:
    sys.exit("render_resume_pdf: reportlab is missing. Run: pip install reportlab")

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from resume_text import utf8_stdio  # noqa: E402

FONT_DIR = HERE.parent / "assets" / "fonts"
FACES = {"regular": "Regular", "bold": "Bold", "italic": "Italic", "bolditalic": "BoldItalic"}
SYSTEM_FONTS = [  # tried when the bundled fonts are missing: (directory, file pattern)
    ("/usr/share/fonts/truetype/liberation", "LiberationSerif-{}.ttf"),
    ("/usr/share/fonts/liberation-serif", "LiberationSerif-{}.ttf"),
    ("/usr/share/fonts/truetype/liberation2", "LiberationSerif-{}.ttf"),
]


def register_fonts():
    """Register a Unicode serif family. Returns (regular, bold, italic, unicode_ok)."""
    candidates = [(FONT_DIR, "LiberationSerif-{}.ttf")] + [(Path(d), p) for d, p in SYSTEM_FONTS]
    for folder, pattern in candidates:
        paths = {k: Path(folder) / pattern.format(v) for k, v in FACES.items()}
        if all(p.exists() for p in paths.values()):
            try:
                for key, path in paths.items():
                    pdfmetrics.registerFont(TTFont(f"ResumeSerif-{key}", str(path)))
                pdfmetrics.registerFontFamily("ResumeSerif", normal="ResumeSerif-regular",
                                              bold="ResumeSerif-bold", italic="ResumeSerif-italic",
                                              boldItalic="ResumeSerif-bolditalic")
                rl_config.canvas_basefontname = "ResumeSerif-regular"  # keep Helvetica out of the PDF
                return "ResumeSerif-regular", "ResumeSerif-bold", "ResumeSerif-italic", True
            except Exception:  # a damaged font file: try the next candidate
                continue
    print("warning: Liberation Serif not found; falling back to the PDF base font Times. "
          "Bullets are drawn as '-' so the text layer stays clean.", file=sys.stderr)
    return "Times-Roman", "Times-Bold", "Times-Italic", False


def gap(base, spacing):
    """Vertical gaps between blocks grow fastest with --spacing; that reads as air, not padding."""
    return base * (1 + 2.5 * (spacing - 1))


def styles(regular, bold, italic, size, spacing):
    lead = round(size * 1.22 * (1 + (spacing - 1) / 4), 2)  # line height grows gently
    return {
        "name": ParagraphStyle("name", fontName=bold, fontSize=size + 6.5, leading=size + 9.5,
                               alignment=TA_CENTER, spaceAfter=gap(2, spacing)),
        "contact": ParagraphStyle("contact", fontName=regular, fontSize=size - 0.5, leading=lead,
                                  alignment=TA_CENTER, spaceAfter=gap(5, spacing)),
        "section": ParagraphStyle("section", fontName=bold, fontSize=size + 0.5, leading=lead + 0.5,
                                  spaceBefore=gap(7, spacing), spaceAfter=0),
        "body": ParagraphStyle("body", fontName=regular, fontSize=size, leading=lead),
        "bullet": ParagraphStyle("bullet", fontName=regular, fontSize=size, leading=lead,
                                 leftIndent=14, bulletIndent=4, bulletFontName=regular,
                                 bulletFontSize=size, spaceAfter=gap(1, spacing)),
        "org": ParagraphStyle("org", fontName=bold, fontSize=size, leading=lead),
        "role": ParagraphStyle("role", fontName=italic, fontSize=size, leading=lead),
        "right": ParagraphStyle("right", fontName=regular, fontSize=size, leading=lead,
                                alignment=TA_RIGHT),
    }


_ALLOWED_TAGS = r"/?(?:b|i|u|br|super|sub|strike|font|a)\b"


def esc(text):
    """Escape bare '&' and stray '<' for reportlab's mini-markup.

    Without this, "R&D" prints as "R&D;" (a stray semicolon that also trips the slop scan).
    Real tags such as <b> and existing entities such as &amp; are left alone.
    """
    text = re.sub(r"&(?!(?:[a-zA-Z][a-zA-Z0-9]*|#[0-9]+|#x[0-9a-fA-F]+);)", "&amp;", str(text))
    return re.sub(rf"<(?!{_ALLOWED_TAGS})", "&lt;", text)


EMAIL = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")
URLISH = re.compile(r"^(?:https?://)?(?:www\.)?[\w-]+(?:\.[\w-]+)+(?:/\S*)?$", re.I)


def contact_item(item):
    """Make emails and URLs clickable; leave phone numbers and plain text alone."""
    text = str(item).strip()
    if EMAIL.match(text):
        return f'<a href="mailto:{esc(text)}">{esc(text)}</a>'
    if URLISH.match(text) and not re.fullmatch(r"[\d.\s+()-]+", text):
        href = text if text.lower().startswith("http") else "https://" + text
        return f'<a href="{esc(href)}">{esc(text)}</a>'
    return esc(text)


def two_col(left, right_text, width, st):
    t = Table([[left, Paragraph(esc(right_text or ""), st["right"])]],
              colWidths=[width * 0.70, width * 0.30])
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), st["body"].fontName),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


def section_header(title, story, st):
    story.append(Paragraph(esc(title.upper()), st["section"]))
    story.append(HRFlowable(width="100%", thickness=0.7, color=colors.black, spaceBefore=1, spaceAfter=3))


def add_skills(data, story, st):
    section_header(data.get("skills_title", "Skills"), story, st)
    skills = data["skills"]
    if isinstance(skills, dict):
        for group, items in skills.items():
            items = items if isinstance(items, list) else [items]
            story.append(Paragraph(f"<b>{esc(group)}:</b> {esc(', '.join(map(str, items)))}", st["body"]))
    else:
        for line in skills:
            story.append(Paragraph(esc(line), st["body"]))


def validate(data):
    errors = []
    if not isinstance(data, dict):
        return ["the top level must be an object"]
    if not isinstance(data.get("name"), str) or not data["name"].strip():
        errors.append('"name" must be a non-empty string')
    if not isinstance(data.get("contact", []), list):
        errors.append('"contact" must be a list of strings')
    for i, section in enumerate(data.get("sections", [])):
        if not isinstance(section, dict) or "title" not in section:
            errors.append(f"sections[{i}] needs a title")
            continue
        for j, entry in enumerate(section.get("entries", [])):
            if not isinstance(entry, dict):
                errors.append(f"sections[{i}].entries[{j}] must be an object")
            elif not isinstance(entry.get("bullets", []), list):
                errors.append(f"sections[{i}].entries[{j}].bullets must be a list of strings")
    skills = data.get("skills")
    if skills is not None and not isinstance(skills, (dict, list)):
        errors.append('"skills" must be an object of lists or a list of lines')
    if data.get("paper") and str(data["paper"]).lower() not in ("letter", "a4"):
        errors.append('"paper" must be "letter" or "a4"')
    return errors


def entry_lines(e, st, width, inline):
    """The org line and the role line of one entry, as flowables."""
    out = []
    org = esc(e.get("org", ""))
    if org and e.get("link"):
        org = f'<a href="{esc(e["link"])}">{org}</a>'
    if inline:
        if org:
            loc = f", {esc(e['location'])}" if e.get("location") else ""
            out.append(Paragraph(f"<b>{org}</b>{loc}", st["body"]))
        role, dates = esc(e.get("role", "")), esc(e.get("dates", ""))
        if role or dates:
            joined = f"<i>{role}</i>" + (f" | {dates}" if role and dates else dates)
            out.append(Paragraph(joined, st["body"]))
        return out
    if org:
        out.append(two_col(Paragraph(org, st["org"]), e.get("location", ""), width, st))
    if e.get("role"):
        out.append(two_col(Paragraph(esc(e["role"]), st["role"]), e.get("dates", ""), width, st))
    elif e.get("dates") and org:
        out.append(two_col(Paragraph("", st["role"]), e["dates"], width, st))
    return out


def render(data, out_path, paper=None, font_size=10.5, spacing=1.0, dates="right"):
    regular, bold, italic, unicode_ok = register_fonts()
    st = styles(regular, bold, italic, font_size, spacing)
    bullet_char = "•" if unicode_ok else "-"
    separator = " • " if unicode_ok else " | "
    page = A4 if (paper or data.get("paper") or "letter").lower() == "a4" else letter
    side, top = 0.65 * inch, 0.55 * inch
    doc = SimpleDocTemplate(str(out_path), pagesize=page, leftMargin=side, rightMargin=side,
                            topMargin=top, bottomMargin=top, title=data["name"], author=data["name"])
    width = page[0] - 2 * side - 12  # the frame pads 6 pt on each side; tables must match paragraphs
    story = [Paragraph(esc(data["name"]), st["name"])]
    if data.get("contact"):
        story.append(Paragraph(separator.join(contact_item(c) for c in data["contact"]), st["contact"]))

    if data.get("summary"):
        section_header(data.get("summary_title", "Summary"), story, st)
        story.append(Paragraph(esc(data["summary"]), st["body"]))

    # Skills follow the section named in "skills_after" (Harvard order for experienced
    # candidates: Experience, Skills, Education). Without it they come last.
    skills_after = (data.get("skills_after") or "").strip().lower()
    skills_done = not data.get("skills")
    for section in data.get("sections", []):
        section_header(section["title"], story, st)
        for e in section.get("entries", []):
            story.extend(entry_lines(e, st, width, dates == "inline"))
            for b in e.get("bullets", []):
                story.append(Paragraph(esc(b), st["bullet"], bulletText=bullet_char))
            if e.get("text"):
                story.append(Paragraph(esc(e["text"]), st["body"]))
            story.append(Spacer(1, gap(3, spacing)))
        if not skills_done and section["title"].strip().lower() == skills_after:
            add_skills(data, story, st)
            skills_done = True
    if not skills_done:
        add_skills(data, story, st)
    doc.build(story)


def main():
    ap = argparse.ArgumentParser(description="Render resume JSON to a Harvard-style PDF.")
    ap.add_argument("resume_json")
    ap.add_argument("-o", "--output", default="resume.pdf")
    ap.add_argument("--paper", choices=["letter", "a4"],
                    help="default: the JSON's layout or 'paper' field, else letter")
    ap.add_argument("--font-size", type=float, help="body size in points, 10 to 11.5 (default 10.5)")
    ap.add_argument("--spacing", type=float, help="vertical spacing factor, 0.8 to 1.5 (default 1.0)")
    ap.add_argument("--dates", choices=["right", "inline"],
                    help="right-aligned dates (default) or inline after the role")
    ap.add_argument("--fill", action="store_true", default=None,
                    help="last resort: grow spacing, then font size, until the page is full")
    ap.add_argument("--pages", type=int, choices=[1, 2], help="allowed page count (default 1)")
    args = ap.parse_args()
    try:
        data = json.loads(Path(args.resume_json).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as err:
        sys.exit(f"render_resume_pdf: cannot read {args.resume_json}: {err}")
    errors = validate(data)
    if errors:
        sys.exit("render_resume_pdf: invalid resume JSON:\n  " + "\n  ".join(errors))
    layout = data.get("layout") or {}
    args.paper = args.paper or layout.get("paper") or data.get("paper")
    args.font_size = float(args.font_size if args.font_size is not None else layout.get("font_size", 10.5))
    args.spacing = float(args.spacing if args.spacing is not None else layout.get("spacing", 1.0))
    args.dates = args.dates or layout.get("dates", "right")
    args.fill = bool(args.fill if args.fill is not None else layout.get("fill", False))
    args.pages = int(args.pages or layout.get("pages", 1))
    if not 10 <= args.font_size <= 11.5:
        sys.exit("render_resume_pdf: font size must be between 10 and 11.5")
    if not 0.8 <= args.spacing <= 1.5:
        sys.exit("render_resume_pdf: spacing must be between 0.8 and 1.5")
    if args.dates not in ("right", "inline") or args.pages not in (1, 2):
        sys.exit("render_resume_pdf: layout.dates must be right or inline, and layout.pages 1 or 2")
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    render(data, out, args.paper, args.font_size, args.spacing, args.dates)
    try:
        from pdf_checks import fill_line, fill_report
    except Exception as err:  # the check is a convenience; pdf_checks.py runs it fully
        print(f"wrote {out}\n(page-fill check skipped: {err})")
        return
    report = fill_report(out, args.pages)
    if args.fill and report["status"] == "UNDERFILLED":
        size, spacing, report = autofill(data, out, args, fill_report)
        print(f"fill: font {size} pt, spacing {spacing} (keep \"fill\": true in the JSON's layout block, "
              "not these numbers, so a rebuild after any edit fits the page again)")
    print(f"wrote {out}")
    print(fill_line(report))


def autofill(data, out, args, fill_report):
    """Largest spacing (then font size) that keeps one page; stop as soon as the page is FULL.

    Spacing moves in steps of 0.01 and is always rounded down, and the file on disk is the
    last thing rendered and measured, so the reported status is the status of that file.
    """
    def one_page(size, spacing):  # "fits": within the allowed page count
        render(data, out, args.paper, size, spacing, args.dates)
        return fill_report(out, args.pages)["pages"] <= args.pages

    sizes = sorted({args.font_size, max(args.font_size, min(11.0, args.font_size + 0.5))})
    best = (args.font_size, args.spacing)
    for size in sizes:
        low, high = int(round(args.spacing * 100)), 150  # in hundredths
        if not one_page(size, low / 100):
            break  # even the starting spacing overflows at this size
        if one_page(size, high / 100):
            low = high
        else:
            while high - low > 1:
                mid = (low + high) // 2
                if one_page(size, mid / 100):
                    low = mid
                else:
                    high = mid
        best = (size, low / 100)
        render(data, out, args.paper, size, low / 100, args.dates)
        if fill_report(out, args.pages)["status"] == "FULL":
            break
    size, spacing = best
    render(data, out, args.paper, size, spacing, args.dates)
    report = fill_report(out, args.pages)
    return size, spacing, report


if __name__ == "__main__":
    utf8_stdio()
    main()
