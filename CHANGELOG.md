# Changelog

## 1.0.1 (2026-10-12)

- The minimum versions are now pypdf 5.1 and reportlab 4.0.4. Older pypdf glues words together when it extracts text, so the PDF checks reported words as glued on PDFs that were fine. reportlab 4.0.0 also installs pycairo, which has to be compiled against the cairo C library on Linux, so it failed to install on a machine without it. `check_env.py` now flags packages that are too old and exits with an error until they are upgraded.
- The scripts write UTF-8 on Windows. Before, printing a character such as "ﬁ" or "→" from a résumé into a pipe that uses the Windows code page stopped the script with an error.
- Words with accents or in other scripts, such as "Zürich" or "Łódź", now count as whole words when the slop scan looks for phrases copied from the posting and when the PDF checks look for glued words.
- CI runs the tests on Linux (Python 3.9, 3.13, 3.14 and 3.15, plus the oldest supported versions of the dependencies), macOS and Windows. It also checks the plugin manifests and the skill with Claude Code's validator, lints the workflows, and checks the layout of the upload zip. Actions are pinned to commit SHAs, and Dependabot proposes updates.
- Pushing a `vX.Y.Z` tag runs CI, checks that the tag, `plugin.json`, `SKILL.md` and this changelog agree, builds the zip and publishes the release.

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
