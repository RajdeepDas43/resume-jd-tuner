#!/usr/bin/env python3
"""Extract plain text from a resume or a saved job posting.

Reads PDF, DOCX, LaTeX (.tex), HTML, Markdown and plain text.

Usage:
  python3 extract_text.py INPUT -o OUT.txt [--dewrap OUT_ONE_LINE_PER_BULLET.txt]

PDF: uses pdftotext (poppler) when installed, with pypdf as a second reader. The second
reader's text goes to OUT with ".pypdf.txt" in place of ".txt", and the script warns when
the two readers disagree, which is a sign that an ATS parser may misread the file too.
It also reports the page count and paper size, and warns when a PDF has no text layer
(a scanned image: an ATS reads nothing from it).

DOCX: reads the XML directly (no extra packages). Warns when contact details sit only in
the page header, or when content sits in text boxes or tables, which some ATS skip.

--dewrap writes a second copy with one line per bullet or paragraph, for reviewers.
"""
import argparse
import html
import re
import shutil
import subprocess
import sys
import zipfile
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from resume_text import BULLET, NON_PROSE, clean, is_header  # noqa: E402

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE = re.compile(r"\+?\d[\d ()\-.]{7,}\d")
GARBLE = re.compile(r"\(cid:\d+\)|[\x00-\x08\x0b\x0e-\x1f\x7f\ufffd]|[\ue000-\uf8ff]")


# ------------------------------------------------------------------ PDF

def pdf_pdftotext(path):
    if not shutil.which("pdftotext"):
        return None
    try:
        out = subprocess.run(["pdftotext", "-enc", "UTF-8", str(path), "-"],
                             capture_output=True, timeout=60, check=True)
        return out.stdout.decode("utf-8", errors="replace")
    except (subprocess.SubprocessError, OSError):
        return None


def pdf_pypdf(path):
    try:
        from pypdf import PdfReader
    except ImportError:
        return None
    try:
        reader = PdfReader(str(path))
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    except Exception:  # a broken PDF should not stop the run
        return None


def pdf_info(path):
    try:
        from pypdf import PdfReader
        reader = PdfReader(str(path))
        box = reader.pages[0].mediabox
        w, h = float(box.width), float(box.height)
    except Exception:
        return None
    size = "custom"
    if abs(w - 612) < 6 and abs(h - 792) < 6:
        size = "Letter"
    elif abs(w - 595) < 6 and abs(h - 842) < 6:
        size = "A4"
    return {"pages": len(reader.pages), "width_pt": round(w), "height_pt": round(h), "paper": size}


def word_set(text):
    return set(re.findall(r"[a-z0-9]{3,}", text.lower()))


# ------------------------------------------------------------------ DOCX

_W_TEXT = re.compile(r"<w:t(?:\s[^>]*)?>(.*?)</w:t>|<w:tab/>|<w:br[^>]*/>|<w:cr/>|</w:p>", re.S)


def _docx_xml_text(xml):
    parts = []
    for m in _W_TEXT.finditer(xml):
        token = m.group(0)
        if m.group(1) is not None:
            parts.append(html.unescape(m.group(1)))
        elif token.startswith("<w:tab"):
            parts.append("\t")
        else:
            parts.append("\n")
    return "".join(parts)


def docx_paper(body_xml):
    """Paper size from the first section's <w:pgSz> (twentieths of a point)."""
    m = re.search(r'<w:pgSz[^>]*w:w="(\d+)"[^>]*w:h="(\d+)"', body_xml)
    if not m:
        return None
    w, h = int(m.group(1)) / 20, int(m.group(2)) / 20
    paper = "Letter" if abs(w - 612) < 6 and abs(h - 792) < 6 else "A4" if abs(w - 595) < 6 and abs(h - 842) < 6 \
        else "custom"
    return {"paper": paper, "width_pt": round(w), "height_pt": round(h)}


def docx_text(path, warnings, info=None):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        body_xml = z.read("word/document.xml").decode("utf-8", errors="replace")
        header_text = "".join(_docx_xml_text(z.read(n).decode("utf-8", errors="replace"))
                              for n in names if re.match(r"word/(header|footer)\d*\.xml$", n))
    if info is not None:
        info.update(docx_paper(body_xml) or {})
    body = _docx_xml_text(body_xml)
    if "<w:txbxContent" in body_xml:
        warnings.append("the DOCX has text boxes: some ATS skip their content")
    if "<w:tbl>" in body_xml or "<w:tbl " in body_xml:
        warnings.append("the DOCX uses tables for layout: some ATS read tables out of order")
    contact_in_header = bool(EMAIL.search(header_text) or PHONE.search(header_text))
    contact_in_body = bool(EMAIL.search(body) or PHONE.search(body))
    if contact_in_header and not contact_in_body:
        warnings.append("contact details sit only in the page header: many ATS ignore headers")
    text = (header_text.strip() + "\n\n" + body) if header_text.strip() else body
    return text


# ------------------------------------------------------------------ LaTeX

_DROP_WITH_ARGS = ("vspace", "hspace", "setlength", "addtolength", "usepackage", "documentclass",
                   "newcommand", "renewcommand", "providecommand", "input", "include", "pagestyle",
                   "thispagestyle", "titleformat", "titlespacing", "geometry", "color",
                   "definecolor", "includegraphics", "fontsize", "linespread", "setlist",
                   "pdfgentounicode", "hypersetup", "urlstyle", "raggedright", "label", "ref",
                   "setcounter", "newenvironment", "renewenvironment", "def", "let",
                   "selectfont", "fontfamily", "begin", "end")


def tex_text(source, keep_urls=True):
    """Rough plain text of a LaTeX document body. keep_urls=False drops link targets."""
    text = re.sub(r"(?<!\\)%.*", "", source)
    m = re.search(r"\\begin\{document\}(.*?)\\end\{document\}", text, re.S)
    if m:
        text = m.group(1)
    text = re.sub(r"\\href\{([^}]*)\}\{([^}]*)\}", r"\2 (\1)" if keep_urls else r"\2", text)
    text = re.sub(r"\\url\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\(?:sub)*section\*?\{([^}]*)\}", r"\n\1\n", text)
    text = re.sub(r"\\item\b(?:\[[^\]]*\])?", "\n• ", text)
    text = re.sub(r"\\\\\*?(?:\[[^\]]*\])?", "\n", text).replace("\\newline", "\n")  # \\ and \\[3pt]
    for cmd in _DROP_WITH_ARGS:
        text = re.sub(rf"\\{cmd}\*?(?:\[[^\]]*\])?(?:\{{[^{{}}]*\}})*", " ", text)
    for a, b in (("\\&", "&"), ("\\%", "%"), ("\\$", "$"), ("\\#", "#"), ("\\_", "_"),
                 ("\\textbar", "|"), ("$|$", "|"), ("---", "—"), ("--", "–"), ("~", " "),
                 ("\\ ", " "), ("``", '"'), ("''", '"')):
        text = text.replace(a, b)
    text = re.sub(r"\\[a-zA-Z@]+\*?(?:\[[^\]]*\])?", " ", text)  # remaining commands, keep their {args}
    text = re.sub(r"\$([^$]*)\$", r"\1", text)
    text = text.replace("{", " ").replace("}", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


# ------------------------------------------------------------------ HTML

class _HTMLText(HTMLParser):
    BLOCK = {"p", "div", "br", "li", "ul", "ol", "h1", "h2", "h3", "h4", "h5", "h6", "tr",
             "section", "article", "header", "footer", "table"}

    def __init__(self):
        super().__init__()
        self.parts, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript", "svg"):
            self.skip += 1
        elif tag == "li":
            self.parts.append("\n• ")
        elif tag in self.BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "svg"):
            self.skip = max(0, self.skip - 1)
        elif tag in self.BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def html_text(source):
    parser = _HTMLText()
    parser.feed(source)
    text = "".join(parser.parts)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


# ------------------------------------------------------------------ de-wrapping

_BULLET = BULLET


def dewrap(text):
    """Join wrapped lines so each bullet or paragraph sits on one line."""
    items, current, section = [], "", ""
    for raw in clean(text).splitlines():
        line = raw.strip()
        if not line:
            if current:
                items.append(current)
                current = ""
            continue
        if _BULLET.fullmatch(line):
            # A bullet glyph on a line of its own: pdftotext often splits Word bullets from their
            # text. It still marks the end of the item before it.
            if current:
                items.append(current)
                current = ""
            continue
        if is_header(line):
            section = line.upper()
        in_list = any(word in section for word in NON_PROSE)  # skills, education: keep lines as they are
        starts_new = (in_list or is_header(line) or is_header(current) or _BULLET.match(line) is not None
                      or not current
                      or (current.endswith((".", "!", "?", ":")) and line[:1].isupper())
                      or (len(current.split()) <= 6 and not current.endswith(",")))
        if starts_new:
            if current:
                items.append(current)
            current = _BULLET.sub("• ", line) if _BULLET.match(line) else line
        elif current.endswith("-") and line[:1].islower():
            current = current[:-1] + line
        else:
            current += " " + line
    if current:
        items.append(current)
    return "\n".join(items) + "\n"


# ------------------------------------------------------------------ main

def extract(path, warnings, info):
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        meta = pdf_info(path)
        if meta:
            info.update(meta)
        primary, second = pdf_pdftotext(path), pdf_pypdf(path)
        info["reader"] = "pdftotext" if primary is not None else "pypdf"
        text = primary if primary is not None else second
        if text is None:
            sys.exit("extract_text: no PDF reader available. Install poppler-utils (pdftotext) or "
                     "run: pip install pypdf")
        if len(text.split()) < 30:
            warnings.append("almost no text layer: this PDF is probably a scanned image, which an "
                            "ATS cannot read. Ask for a text-based PDF or DOCX.")
        if primary is not None and second is not None:
            a, b = word_set(primary), word_set(second)
            agreement = len(a & b) / max(1, len(a | b))
            info["second_reader"] = "pypdf"
            info["reader_agreement"] = round(agreement, 3)
            if agreement < 0.9:
                warnings.append(f"the two PDF readers agree on only {agreement:.0%} of words: check "
                                "for columns, tables or unusual fonts")
            info["_second_text"] = second
        return text
    if suffix == ".docx":
        return docx_text(path, warnings, info)
    if suffix == ".doc":
        sys.exit("extract_text: old .doc files are not supported. Save it as .docx or PDF first.")
    raw = path.read_text(encoding="utf-8", errors="replace")
    if suffix == ".tex":
        return tex_text(raw)
    if suffix in (".html", ".htm"):
        return html_text(raw)
    return raw


def main():
    ap = argparse.ArgumentParser(description="Extract text from a resume or job posting file.")
    ap.add_argument("input")
    ap.add_argument("-o", "--output", required=True, help="where to write the text")
    ap.add_argument("--dewrap", metavar="OUT", help="also write one line per bullet or paragraph")
    args = ap.parse_args()
    path = Path(args.input)
    if not path.exists():
        sys.exit(f"extract_text: {path} not found")
    warnings, info = [], {}
    text = clean(extract(path, warnings, info))
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    second = info.pop("_second_text", None)
    if second is not None:
        second_path = out.with_name(out.stem + ".pypdf.txt")
        second_path.write_text(clean(second), encoding="utf-8")
        info["second_reader_file"] = str(second_path)
    garbled = GARBLE.findall(text)
    if garbled:
        warnings.append(f"{len(garbled)} garbled characters in the extracted text "
                        f"(e.g. {sorted(set(garbled))[:5]}): an ATS will see the same garbage")
    if args.dewrap:
        Path(args.dewrap).write_text(dewrap(text), encoding="utf-8")
    words = len(text.split())
    summary = [f"wrote {out} ({words} words)"]
    if "pages" in info:
        summary.append(f"pages: {info['pages']} ({info['paper']}, {info['width_pt']}x{info['height_pt']} pt)")
    elif "paper" in info:
        summary.append(f"paper: {info['paper']} ({info['width_pt']}x{info['height_pt']} pt)")
    if "reader" in info:
        summary.append(f"reader: {info['reader']}")
    if "reader_agreement" in info:
        summary.append(f"second reader: pypdf, word agreement {info['reader_agreement']:.0%}")
    print("; ".join(summary))
    for w in warnings:
        print(f"warning: {w}")


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:  # output piped into head: the files are already written
        sys.stderr.close()
