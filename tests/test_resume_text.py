from resume_text import core_sections_found, find_term, is_header, skills_and_prose


def test_short_terms_and_acronyms_are_case_sensitive():
    assert find_term("Go", "Built services in Go and Python.")
    assert not find_term("Go", "Ready to go live next week.")
    assert find_term("SQL", "Wrote SQL for the weekly report")
    assert not find_term("SQL", "nosql stores")


def test_word_boundaries_and_symbols():
    assert not find_term("C", "Wrote C++ and C# services")
    assert find_term("C++", "Wrote C++ services")
    assert find_term("C#", "Wrote C# services")
    assert find_term("Node.js", "APIs in Node.js and Go")
    assert not find_term("Java", "Wrote JavaScript tests")
    assert find_term("CI/CD", "Built the CI/CD pipeline")


def test_exact_spelling_vs_loose():
    text = "Ran microservices on K8s with a Postgres backend"
    assert not find_term("Kubernetes", text)
    assert not find_term("PostgreSQL", text)
    assert find_term("microservice", text)  # a simple plural counts as the same term
    assert find_term("A/B tests", "Ran an A/B test on onboarding")
    assert not find_term("SQL", "SQLs")  # acronyms stay exact
    assert find_term("machine learning", "machine-learning models", loose=True)
    assert not find_term("machine learning", "machine-learning models")


def test_hyphenated_line_break_is_joined():
    assert find_term("microservices", "split the monolith into micro-\nservices on AWS")


def test_ligatures_and_quotes_are_normalised():
    assert find_term("office", "back oﬃce work")  # "o" + the "ffi" ligature + "ce"
    assert find_term("o'brien", "Worked with O’Brien")


def test_headers():
    for header in ("EXPERIENCE", "Work Experience", "SKILLS & INTERESTS", "Professional Summary:",
                   "Technical Skills", "Projects"):
        assert is_header(header), header
    assert not is_header("Built the experience layer for the app.")


def test_core_sections_and_split():
    text = "Jane Doe\nSUMMARY\nAnalyst.\nEXPERIENCE\n• Built Tableau dashboards\nSKILLS\nTableau, SQL\nEDUCATION\nBSc"
    found = core_sections_found(text)
    assert all(found.values())
    skills, prose = skills_and_prose(text)
    assert "Tableau, SQL" in skills and "Built Tableau" in prose and "Tableau, SQL" not in prose
