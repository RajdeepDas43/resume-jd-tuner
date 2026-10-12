from conftest import run_script
from slop_scan import scan

CLEAN = """Jane Doe
jane@example.com
SUMMARY
Data analyst with five years in retail pricing. I build the weekly margin report for 300 stores.
EXPERIENCE
Larkspur Foods
Senior Analyst
Jan 2021 – Present
• Rebuilt the weekly margin report in dbt and Looker. It now runs in 20 minutes instead of a day.
• Found a promo-pricing bug that cost about $40K a month and worked with IT on the fix.
• Trained six store managers to read the new dashboard.
SKILLS
SQL, dbt, Looker, Python
"""

SLOPPY = """Jane Doe
SUMMARY
Results-driven analyst passionate about leveraging data to drive adoption — and to unlock value.
EXPERIENCE
Larkspur Foods
Senior Analyst
2021 - Present
• Spearheaded a robust, end-to-end pricing transformation; delivering seamless insights, ensuring alignment.
• Responsible for dashboards, resulting in 45% efficiency gains, improving morale, boosting retention.
• Leveraged cutting-edge tools to elevate reporting, fostering collaboration.
"""


def test_clean_text_passes():
    r = scan(CLEAN, "We need a pricing analyst with SQL and Looker.")
    assert r["verdict"] == "PASS", r
    assert r["bullets"] >= 3


def test_sloppy_text_fails():
    r = scan(SLOPPY)
    assert r["verdict"] == "FAIL"
    assert r["dashes"] >= 1 and r["semicolons"] >= 1
    assert "leverag" in r["banned_words"] and "robust" in r["banned_words"]
    assert r["weak_openers"]
    assert r["ing_tails"]


def test_employer_and_date_lines_are_not_prose():
    r = scan(CLEAN)
    assert all("Larkspur" not in s for s in r["long_sentences"])
    assert r["dashes"] == 0, "date ranges must not count as dashes"


def test_posting_echoes_are_flagged():
    jd = "You will own the weekly margin report for all of our stores."
    r = scan(CLEAN, jd)
    assert "build the weekly margin report" not in r["shared_4_word_runs"]
    assert "the weekly margin report" in r["shared_4_word_runs"]
    assert r["verdict"] == "REVIEW"


def test_no_headers_warns_but_scans():
    r = scan("• Built a dashboard for sales. It saved time.\n• Wrote SQL for finance.")
    assert r["warnings"]
    assert r["bullets"] >= 1


def test_word_symbol_font_bullets_are_recognised():
    text = CLEAN.replace("• ", " ")
    r = scan(text)
    assert r["bullets"] >= 3 and r["verdict"] == "PASS"


def test_output_is_utf8_on_a_non_utf8_console(tmp_path):
    # Windows pipes default to the ANSI code page; "→" and "ł" are not in cp1252.
    phrase = "Built the Łódź → Kraków pricing model with the regional finance team"
    resume = tmp_path / "resume.txt"
    jd = tmp_path / "jd.txt"
    resume.write_text(f"Ann Lee\nEXPERIENCE\nAcme\nAnalyst\n• {phrase}.\n", encoding="utf-8")
    jd.write_text(f"Data Analyst\nAcme\nYou will: {phrase}.\n", encoding="utf-8")
    proc = run_script("slop_scan.py", resume, jd, check=False, env={"PYTHONIOENCODING": "cp1252"})
    assert "Traceback" not in proc.stderr, proc.stderr
    assert "łódź kraków" in proc.stdout.lower()  # the shared run, printed with its accents
