# Changelog

## 1.0.0 (2026-10-12)

First public release.

- One workflow: a job link (or pasted posting) plus a résumé in, a one-page tuned résumé PDF and a fit report out.
- Fit report with six sections: overall fit before and after, ATS alignment with an honest ceiling, interview risk, gaps to improve, quality check, and what changed.
- Deterministic scoring (`scoreboard.py`, `coverage.py`) over graded evidence, documented in `references/scoring.md`.
- Page fill: measures the free lines at the bottom (`pdf_checks.py`), fills them with true, relevant experience and summary content, asks targeted questions when sources run out, and offers `--fill` as a last-resort layout step.
- Three quality reviewers (AI-slop screener, copy editor, fact-checker) and two recruiter-side verifiers (recruiter screen, hiring manager), with briefs in `references/reviewers.md`.
- Renderer embeds Liberation Serif, so bullets and accents extract as real characters. It also makes emails and profile URLs clickable and supports A4 and Letter, inline or right-aligned dates, and an automatic layout fill.
- PDF checks for garbled or glued words in every reader, dates detached from their role, headers, contact details, links, and required or forbidden text.
- LaTeX path keeps the user's template and adds ATS-safety lines that stop glued words ("Engineerworking") and bitmap bullets.
- Text extraction from PDF, DOCX (with header-only contact and table warnings), LaTeX, HTML and Markdown.
- Claude Code plugin and marketplace manifests, a zip for the Claude apps, unit tests, CI, evals and a worked example.
