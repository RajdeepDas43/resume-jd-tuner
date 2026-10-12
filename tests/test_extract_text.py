import shutil
import zipfile

import pytest

from conftest import run_script
from extract_text import dewrap, html_text, tex_text

DOCX_DOC = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>
<w:p><w:r><w:t>EXPERIENCE</w:t></w:r></w:p>
<w:p><w:r><w:t xml:space="preserve">Built the R&amp;D </w:t></w:r><w:r><w:t>dashboard.</w:t></w:r></w:p>
</w:body></w:document>"""
DOCX_HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:hdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:p><w:r><w:t>Jane Doe · jane@example.com · +1 555 010 0199</w:t></w:r></w:p></w:hdr>"""


def make_docx(path):
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("[Content_Types].xml", "<Types/>")
        z.writestr("word/document.xml", DOCX_DOC)
        z.writestr("word/header1.xml", DOCX_HEADER)


def test_docx_text_and_header_warning(tmp_path):
    src = tmp_path / "cv.docx"
    make_docx(src)
    out = tmp_path / "cv.txt"
    proc = run_script("extract_text.py", src, "-o", out)
    text = out.read_text()
    assert "Built the R&D dashboard." in text
    assert "jane@example.com" in text
    assert "contact details sit only in the page header" in proc.stdout


def test_tex_text():
    tex = r"""\documentclass{article}
\usepackage{hyperref} % comment
\begin{document}
\section*{Experience}
\resumeSubheading{Acme Corp}{Jan 2020 -- Present}{Data Analyst}{Remote}
\begin{itemize}
  \item Built \textbf{Tableau} dashboards for 40\% of stores \& the CFO.
\end{itemize}
\href{https://github.com/jdoe}{GitHub}
\end{document}"""
    text = tex_text(tex)
    assert "Experience" in text
    assert "Acme Corp" in text and "Jan 2020 – Present" in text
    assert "• Built Tableau dashboards for 40% of stores & the CFO." in text
    assert "GitHub (https://github.com/jdoe)" in text
    assert "usepackage" not in text and "comment" not in text


def test_html_text():
    html = "<html><head><style>p{}</style><script>var x=1</script></head><body><h1>Data Analyst</h1>" \
           "<ul><li>SQL</li><li>Looker</li></ul></body></html>"
    text = html_text(html)
    assert "Data Analyst" in text and "• SQL" in text and "var x" not in text


def test_dewrap_joins_wrapped_bullets_but_keeps_skill_lines():
    raw = ("SUMMARY\nData analyst with five years in retail pricing and a long sentence that\n"
           "wraps onto a second line.\nEXPERIENCE\nAcme\nAnalyst\n• Rebuilt the weekly margin report so it\n"
           "runs in minutes.\n• Trained six managers.\nSKILLS\nLanguages: SQL, Python\nBI: Looker, Tableau\n")
    out = dewrap(raw).splitlines()
    assert "Data analyst with five years in retail pricing and a long sentence that wraps onto a second line." in out
    assert "• Rebuilt the weekly margin report so it runs in minutes." in out
    assert "Languages: SQL, Python" in out and "BI: Looker, Tableau" in out


def test_dewrap_splits_word_symbol_font_bullets():
    # Word's Symbol-font bullets extract as private-use characters, sometimes on lines of their own.
    raw = ("EXPERIENCE\nAcme\n\n\n\nBuilt a churn model that flags accounts likely to cancel in the next\n"
           "60 days.\n Analysed retention for the add-on and found that accounts\nretained better.\n"
           " Wrote SQL.\n(cid:127) Ran the tests.\n")
    out = dewrap(raw).splitlines()
    assert "Built a churn model that flags accounts likely to cancel in the next 60 days." in out
    assert "• Analysed retention for the add-on and found that accounts retained better." in out
    assert "• Wrote SQL." in out and "• Ran the tests." in out
    assert not any(line.strip() == "" for line in out)


@pytest.mark.skipif(not shutil.which("pdflatex"), reason="pdflatex not installed")
def test_glued_words_detected_and_fixed_by_latex_lines(tmp_path):
    body = (r"\begin{document}" "\n"
            r"I worked as a \textbf{Forward Deployment Engineer} working with clients on \textbf{automated}"
            r" evaluation of \textbf{databases} and the \textbf{comfort} reading code." "\n"
            r"\end{document}")
    safe = (r"\ifdefined\pdfgentounicode \input{glyphtounicode}\pdfgentounicode=1 \fi" "\n"
            r"\ifdefined\pdfinterwordspaceon \pdfinterwordspaceon \fi" "\n")
    results = {}
    for name, extra in (("plain", ""), ("safe", safe)):
        tex = tmp_path / f"{name}.tex"
        tex.write_text("\\documentclass{article}\n" + extra + body)
        import subprocess
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex.name],
                       cwd=tmp_path, capture_output=True, timeout=120)
        proc = run_script("pdf_checks.py", tmp_path / f"{name}.pdf", "--source", tex)
        results[name] = proc.stdout
    assert "glued" not in results["safe"].split("PDF CHECKS")[1]
    # pypdf glues the bold boundary without the safety lines; other readers may not.
    if "words glued together" in results["plain"]:
        assert "pypdf" in results["plain"]
