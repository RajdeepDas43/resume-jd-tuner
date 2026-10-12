import json

import pytest
from pypdf import PdfReader

from conftest import ASSETS, make_resume, run_script
from pdf_checks import fill_report


def test_renders_one_page_with_clean_text_and_links(example_pdf):
    reader = PdfReader(str(example_pdf))
    assert len(reader.pages) == 1
    text = reader.pages[0].extract_text()
    assert "•" in text, "the bullet must extract as a real bullet, not a control character"
    assert "\x7f" not in text
    uris = [a.get_object()["/A"]["/URI"] for a in reader.pages[0]["/Annots"]]
    assert "mailto:alex.rivera@example.com" in uris
    assert "https://linkedin.com/in/alex-rivera-example" in uris


def test_pdf_checks_pass_and_report_fill(example_pdf, tmp_path):
    out = tmp_path / "checks.json"
    proc = run_script("pdf_checks.py", example_pdf, "--source", ASSETS / "example_resume.json",
                      "--link", "linkedin.com/in/alex-rivera-example", "--require", "B.S. in Computer Science",
                      "--forbid", "Harborline", "--json", out)
    assert "PDF CHECKS: PASS" in proc.stdout
    result = json.loads(out.read_text())
    assert result["fill"]["status"] == "UNDERFILLED"  # the example covers about 60% of the page
    assert result["fill"]["free_lines"] >= 10
    assert not result["glued_words"]


def test_forbid_and_require_fail(example_pdf):
    proc = run_script("pdf_checks.py", example_pdf, "--forbid", "Austin", "--require", "M.S. in Physics")
    assert "forbidden term present: 'Austin'" in proc.stdout
    assert "required text not found exactly" in proc.stdout
    assert "PDF CHECKS: FAIL" in proc.stdout


def test_overflow_and_full(tmp_path):
    src = tmp_path / "r.json"
    pdf = tmp_path / "r.pdf"
    # Far too much content: two pages.
    src.write_text(json.dumps(make_resume(bullets_per_role=30, roles=2)))
    run_script("render_resume_pdf.py", src, "-o", pdf)
    assert fill_report(pdf, 1)["status"] == "OVERFLOW"
    # Find the largest number of one-line bullets that still fits: the page must then be FULL.
    low, high = 1, 60
    while low < high:
        mid = (low + high + 1) // 2
        src.write_text(json.dumps(make_resume(bullets_per_role=mid, roles=1)))
        run_script("render_resume_pdf.py", src, "-o", pdf)
        if fill_report(pdf, 1)["pages"] == 1:
            low = mid
        else:
            high = mid - 1
    src.write_text(json.dumps(make_resume(bullets_per_role=low, roles=1)))
    run_script("render_resume_pdf.py", src, "-o", pdf)
    report = fill_report(pdf, 1)
    assert report["pages"] == 1
    assert report["status"] == "FULL", report


def test_renderer_rejects_bad_input(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"name": "", "contact": "x", "sections": [{"entries": []}]}))
    proc = run_script("render_resume_pdf.py", bad, "-o", tmp_path / "x.pdf", check=False)
    assert proc.returncode != 0
    assert "invalid resume JSON" in proc.stderr


def test_unicode_names_render(tmp_path):
    data = json.loads((ASSETS / "example_resume.json").read_text())
    data["name"] = "Łukasz Żółć-Müller"
    src, pdf = tmp_path / "u.json", tmp_path / "u.pdf"
    src.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    run_script("render_resume_pdf.py", src, "-o", pdf, "--paper", "a4")
    reader = PdfReader(str(pdf))
    assert "Łukasz Żółć-Müller" in reader.pages[0].extract_text()
    box = reader.pages[0].mediabox
    assert round(float(box.width)) == 595


@pytest.mark.parametrize("size", ["9", "12"])
def test_font_size_is_bounded(tmp_path, size):
    proc = run_script("render_resume_pdf.py", ASSETS / "example_resume.json", "-o", tmp_path / "x.pdf",
                      "--font-size", size, check=False)
    assert proc.returncode != 0


def test_inline_dates_stay_with_their_role(tmp_path):
    pdf = tmp_path / "inline.pdf"
    run_script("render_resume_pdf.py", ASSETS / "example_resume.json", "-o", pdf, "--dates", "inline")
    text = PdfReader(str(pdf)).pages[0].extract_text()
    assert "Senior Software Engineer | Jun 2022 – Present" in text
    assert "Larkspur Commerce, Austin, TX" in text


def test_fill_option_uses_more_of_the_page_without_changing_words(tmp_path):
    plain, filled = tmp_path / "plain.pdf", tmp_path / "filled.pdf"
    run_script("render_resume_pdf.py", ASSETS / "example_resume.json", "-o", plain)
    proc = run_script("render_resume_pdf.py", ASSETS / "example_resume.json", "-o", filled, "--fill")
    assert "fill: font" in proc.stdout
    before, after = fill_report(plain, 1), fill_report(filled, 1)
    assert after["pages"] == 1
    assert after["free_space_pt"] < before["free_space_pt"]
    words = lambda p: PdfReader(str(p)).pages[0].extract_text().split()  # noqa: E731
    assert words(plain) == words(filled)


def test_detached_dates_are_reported(tmp_path):
    data = json.loads((ASSETS / "example_resume.json").read_text())
    # A short entry with one short bullet: some readers move its right-aligned dates after the bullet.
    data["sections"][0]["entries"].append({"org": "Casa Verde Foods", "location": "Porto, Portugal",
                                           "role": "Marketing Assistant", "dates": "Sep 2019 – Mar 2021",
                                           "bullets": ["Ran the shop's social media accounts."]})
    src, pdf = tmp_path / "d.json", tmp_path / "d.pdf"
    src.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    run_script("render_resume_pdf.py", src, "-o", pdf)
    out = tmp_path / "c.json"
    run_script("pdf_checks.py", pdf, "--source", src, "--json", out)
    detached = json.loads(out.read_text())["detached_dates"]
    run_script("render_resume_pdf.py", src, "-o", pdf, "--dates", "inline")
    run_script("pdf_checks.py", pdf, "--source", src, "--json", out)
    assert json.loads(out.read_text())["detached_dates"] == []
    assert isinstance(detached, list)


def test_fill_reports_the_file_it_wrote(tmp_path):
    # Regression: --fill once rounded the spacing up past the last value that fit, so it printed
    # FULL while the file on disk had a blank second page.
    src = ASSETS.parent.parent.parent / "tests" / "fixtures" / "jordan_resume.json"
    pdf = tmp_path / "jordan.pdf"
    proc = run_script("render_resume_pdf.py", src, "-o", pdf, "--fill")
    fresh = fill_report(pdf, 1)
    assert fresh["pages"] == 1
    assert f"FILL: {fresh['status']}" in proc.stdout
