"""Shared helpers for the resume scripts: text clean-up, section headers and term matching.

Imported by the other scripts in this folder. Nothing here touches the network or the disk.
"""
import re

# Characters that PDF extraction and word processors produce in place of plain ASCII.
_REPLACEMENTS = {
    "‘": "'", "’": "'", "‚": "'", "‛": "'",
    "“": '"', "”": '"', "„": '"',
    " ": " ", " ": " ", " ": " ", "​": "",
    "‐": "-", "‑": "-",
    "ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl", "ﬃ": "ffi", "ﬄ": "ffl",
}


def clean(text):
    """Normalise quotes, ligatures, odd spaces and soft hyphens. Keeps line breaks."""
    for bad, good in _REPLACEMENTS.items():
        text = text.replace(bad, good)
    text = text.replace("­", "")  # soft hyphen
    text = re.sub(r"[ \t]+", " ", text)
    return text


# Bullet glyphs at the start of a line, including the private-use and control characters that
# Word's Symbol-font bullets and some PDF fonts turn into, and pdfminer's "(cid:N)" placeholders.
BULLET = re.compile(r"^(?:[•◦▪▫‣∙·●○■□♦❖➢►▶✓✔*\x7f\x88\uf0a7\uf0b7\uf076\uf0d8\uf0fc]"
                    r"|\(cid:\d+\)|[-–](?=\s))\s*")


# Section headers, matched against a whole line in any case ("EXPERIENCE", "Work Experience:",
# "SKILLS & INTERESTS", "Positions of Responsibility").
_HEADS = (r"SUMMARY|PROFESSIONAL SUMMARY|PROFILE|OBJECTIVE|ABOUT ME|ABOUT|EXPERIENCE|"
          r"EMPLOYMENT(?: HISTORY)?|WORK HISTORY|CAREER HISTORY|INTERNSHIPS?|PROJECTS?|"
          r"EDUCATION|SKILLS|TECHNICAL SKILLS|CERTIFICATIONS?|LICENSES|AWARDS|HONOU?RS|"
          r"ACHIEVEMENTS|ACCOMPLISHMENTS|PUBLICATIONS|PATENTS|LEADERSHIP|"
          r"POSITIONS? OF RESPONSIBILITY|EXTRA-?CURRICULARS?(?: ACTIVITIES)?|ACTIVITIES|"
          r"VOLUNTEERING|VOLUNTEER EXPERIENCE|COURSEWORK|LANGUAGES|INTERESTS|HOBBIES|"
          r"COMPETITIONS|TRAINING|REFERENCES")
_QUALS = (r"PROFESSIONAL|WORK|RELEVANT|TECHNICAL|KEY|CORE|ACADEMIC|SELECTED|OTHER|PERSONAL|"
          r"RESEARCH|INDUSTRY|ADDITIONAL|NOTABLE|VOLUNTEER")
_SECTION = re.compile(rf"(?:(?:{_QUALS})\s+)?(?:{_HEADS})"
                      rf"(?:\s*(?:&|AND|/)\s*(?:(?:{_QUALS})\s+)?(?:{_HEADS}))?\s*:?", re.I)

# Sections that hold lists rather than prose.
NON_PROSE = ("SKILL", "EDUCATION", "CERTIFICATION", "LICENSE", "AWARD", "HONOR", "HONOUR",
             "ACHIEVEMENT", "ACCOMPLISHMENT", "PUBLICATION", "PATENT", "COURSEWORK", "LANGUAGE",
             "INTEREST", "HOBBIES", "COMPETITION", "REFERENCE")

# The four headers an ATS expects to find, with the usual alternatives.
CORE_SECTIONS = {
    "summary": ("SUMMARY", "PROFILE", "ABOUT", "OBJECTIVE"),
    "experience": ("EXPERIENCE", "EMPLOYMENT", "WORK HISTORY", "CAREER HISTORY"),
    "education": ("EDUCATION",),
    "skills": ("SKILLS",),
}


def is_header(line):
    line = line.strip()
    return 0 < len(line) < 45 and _SECTION.fullmatch(line) is not None


def split_sections(text):
    """Return [(HEADER, [lines])]. Lines before the first header go under 'HEADER'."""
    sections = [("HEADER", [])]
    for raw in text.splitlines():
        line = raw.strip()
        if is_header(line):
            sections.append((line.rstrip(":").upper(), []))
        elif line:
            sections[-1][1].append(line)
    return sections


def core_sections_found(text):
    found = {key: False for key in CORE_SECTIONS}
    for raw in text.splitlines():
        line = raw.strip()
        if not is_header(line):
            continue
        upper = line.upper()
        for key, names in CORE_SECTIONS.items():
            if any(name in upper for name in names):
                found[key] = True
    return found


# ---------------------------------------------------------------- term matching

def _case_sensitive(term):
    """Short terms and acronyms ('Go', 'R', 'SQL', 'AWS') must match case to avoid
    false hits on ordinary words ('go', 'sql' inside prose is rare anyway)."""
    letters = re.sub(r"[^A-Za-z]", "", term)
    return len(term) <= 3 or (len(letters) >= 2 and letters.isupper())


def _pattern(term, loose):
    term = clean(term).strip()
    parts = re.split(r"(\s+|-)", term)
    out = []
    for part in parts:
        if not part:
            continue
        if part.isspace():
            out.append(r"[\s\-]+" if loose else r"\s+")
        elif part == "-":
            out.append(r"[\s\-]?" if loose else "-")
        else:
            out.append(re.escape(part))
    body = "".join(out)
    tail = ""
    if loose and re.search(r"[A-Za-z]{3,}$", term) and not _case_sensitive(term):
        tail = r"(?:s|es)?"  # 'microservice' ~ 'microservices'
    # A term ending in a letter or digit must not run into '+' or '#' ('C' is not 'C++').
    after = r"(?![A-Za-z0-9+#])" if re.search(r"[A-Za-z0-9]$", term) else r"(?![A-Za-z0-9])"
    before = r"(?<![A-Za-z0-9])"
    flags = 0 if _case_sensitive(term) else re.I
    return re.compile(before + body + tail + after, flags)


def _number_forms(term):
    """The term plus its simple singular or plural ('A/B tests' and 'A/B test')."""
    term = term.strip()
    forms = [term]
    if re.search(r"[a-z]{3,}$", term):  # lower-case word ending: 'tests', 'pipeline'
        if term.endswith("s") and not term.endswith("ss"):
            forms.append(term[:-1])
        else:
            forms.append(term + "s")
    return forms


def find_term(term, text, loose=False):
    """True if `term` appears in `text` as a whole word (or phrase).

    loose=False: the JD's spelling, ignoring case for normal words, whitespace runs and a
    simple singular or plural of a final lower-case word ('A/B tests' matches 'A/B test').
    loose=True: also accepts hyphen/space swaps.
    Words that a PDF hyphenated across a line break ('micro-' + newline + 'services')
    are matched in their joined form too.
    """
    if not term or not term.strip():
        return False
    text = clean(text)
    joined = re.sub(r"([a-z])-\s*\n\s*([a-z])", r"\1\2", text)
    for form in _number_forms(term):
        pattern = _pattern(form, loose)
        if pattern.search(text) or (joined != text and pattern.search(joined)):
            return True
    return False


def skills_and_prose(text):
    """Split résumé text into (skills_text, other_text) using the section headers."""
    skills, other = [], []
    for header, lines in split_sections(text):
        (skills if "SKILL" in header else other).append("\n".join(lines))
    return "\n".join(skills), "\n".join(other)
