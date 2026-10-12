# Harvard-style layout (the default renderer)

The default output follows the Harvard résumé template: the plain, single-column layout most career offices teach, and the one ATS parsers read most reliably. `scripts/render_resume_pdf.py` produces it from `work/resume.json`. Where this file and SKILL.md disagree, SKILL.md wins.

## Layout

- **One page.** Two only for 10+ years of relevant experience when the base résumé is already two pages, or when the user asks.
- Serif font (the bundled Liberation Serif, metrically the same as Times New Roman), 10.5 pt body by default, margins 0.65 inch at the sides and 0.55 inch at top and bottom.
- **Name** centred at the top. Below it one centred contact line: location (if the base résumé shows one), email, phone, LinkedIn, and GitHub or a portfolio when relevant. Emails and URLs are clickable.
- Section headers in capitals, bold, with a thin rule under each.
- Employer or school in bold with its location on the right; job title or degree in italics with the dates on the right. Some PDF readers move right-aligned text of short entries after the bullets; when `pdf_checks.py` warns about detached dates, render with `--dates inline` ("Senior Analyst | Jun 2022 – Present", which every reader keeps in order).
- No photos, icons, graphics, text boxes or multi-column layouts: ATS parsers read top to bottom, left to right, and silently drop or scramble content placed in columns and boxes.

## Section order

Experienced candidates (3+ years of work):

1. Summary
2. Experience
3. Skills (`"skills_after": "Experience"`)
4. Education
5. Projects, Certifications or Awards, if they add relevant evidence

Students and new graduates:

1. Education (GPA if strong, relevant coursework only if it carries the job's hard terms)
2. Experience (internships, part-time work)
3. Projects
4. Skills

Career changers: Summary, then the most relevant evidence first, which may be Projects or a certification ahead of unrelated past roles.

## Entry format

```text
EMPLOYER NAME                                        City, Country
Job Title                                      Mon YYYY – Mon YYYY
  • bullet: one idea, one to three short sentences
  • up to about eight bullets for the main recent role, fewer for older ones
```

## Fitting one page

- Too long: cut the least relevant content first (old bullets, unrelated skills, a weak project), then tighten wording. `--font-size` may go down to 10 and `--spacing` to 0.9 only after that.
- Too short: add relevant, true content (SKILL.md step 7) and ask the user about the weak asks. Only when no more true content can come, `--fill` widens the spacing and then the font (up to 11 pt) until the page is full, without touching the words. Set it as `"fill": true` in the layout block and leave `spacing` and `font_size` at their defaults: the search then runs again on every rebuild, so the page still fits after a later edit.
- Paper: `--paper letter` for jobs in the US and Canada, `--paper a4` everywhere else.
