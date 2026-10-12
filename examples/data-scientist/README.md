# Example: a product data analyst applies for a senior data scientist role

Everything here is fictional: the candidate (Jordan Lee), both employers on the résumé, the hiring company (Tallowbrook) and Jordan's answers to the skill's questions.

This is one complete run in Claude Code. The reviewers, the recruiter and the hiring manager each ran as a separate agent, and Jordan's side of the conversation is in [`input/answers.md`](input/answers.md).

![Before and after](before-after.png)

## Input

- [`input/Jordan_Lee_Resume.pdf`](input/Jordan_Lee_Resume.pdf): the résumé as written. It is a Word document exported to PDF. Its bullets come out of the PDF as a private-use character (the Symbol-font bullet), which is what an ATS sees, and it fills about half the page.
- [`input/notes.md`](input/notes.md): Jordan's notes on work that isn't on the résumé.
- [`input/job_posting.txt`](input/job_posting.txt): the posting, pasted into the chat.
- [`input/answers.md`](input/answers.md): Jordan's answers. Questions 1 to 8 are the skill's first batch (step 4). Questions 9 and 10 came in step 7, when the page still had free lines.

The prompt:

> Tailor my résumé to this job and tell me how well I fit. My résumé is Jordan_Lee_Resume.pdf, and notes.md has more detail on my work. Here's the posting: …

## Output

```text
tallowbrook-senior-data-scientist/
├── Jordan_Lee_Senior_Data_Scientist.pdf   the tuned résumé
├── fit_report.md                          the fit report
├── job_posting.txt                        the posting as pasted
└── work/                                  every intermediate file
    ├── jd_asks.json, gap_map.json         the decoded posting and the first gap map
    ├── resume.json                        what the PDF is rendered from
    ├── grades_before.json, grades_after.json, scoreboard.json
    ├── pdf_checks.json, slop.json, coverage_*.json
    ├── review_log.md                      what each reviewer said and what was done about it
    ├── review_packet_*.txt                exactly what each agent was given
    └── reviews/                           each agent's full reply
```

The review packets and the agents' full replies were kept for this example so you can read exactly what each agent saw and said. A normal run keeps the review log and the grade files.

| Measure | Before | After |
|---|---|---|
| Overall fit (0-100) | 63 (Fair) | 98 (Strong) |
| Must-haves shown clearly | 5 of 8 | 8 of 8 |
| ATS alignment (0-100) | 73.7 | 94.7 (honest ceiling 94.7) |
| Must-have hard terms present | 6 of 7 | 7 of 7 |
| Keyword overlap (secondary, no target) | 32.8 | 51.3 |

Interview risk: Medium. The recruiter agent shortlisted the page and scored it 8/10 for reading as human.

The reply in the chat:

> Fit 63 (Fair) → 98 (Strong). ATS alignment 73.7 → 94.7, which is the honest ceiling: only dbt is missing, and you haven't used it.
> Gaps that matter: every title says Analyst for a Senior Data Scientist role, and the seat-expansion line gives no result.
> Riskiest question: "A 4-point lift from 41% needs about 2,400 accounts per arm, and you had about 2,000. What did you assume?" Prep is in the report.
> Please confirm what period the 6% base churn rate covers, and whether the finance pipeline reads the 2-billion-row time-punch table.
> Files: tallowbrook-senior-data-scientist/Jordan_Lee_Senior_Data_Scientist.pdf and fit_report.md.

## What to notice

- **Nothing was invented.** Every line comes from the résumé, the notes or Jordan's answers. The fact-checker took "about 2 billion time-punch events" off the finance-pipeline line, because Jordan gave the table's size but never said that pipeline reads it. The report lists it under "Numbers removed" so Jordan can put it back where it belongs.
- **Space went to evidence first.** When the first draft left lines free, the skill asked two more questions (9 and 10) and used the answers. Later the reviewers cut three lines that described duties with no result. By then every requirement was graded clear and no true material was left, so the line spacing was widened. The report says so and lists the questions that would fill that space instead.
- **The reviewers disagreed, and the precedence rules settled it.** The fact-checker outranks everyone, so a reorder that made "the churn work" read as the analysis behind the CEO presentation was undone. The hiring manager wanted the posting's verb "Defined", but the writing rules don't reword toward the posting's phrasing, so the line kept its own wording. Each case is in [`work/review_log.md`](tallowbrook-senior-data-scientist/work/review_log.md).
- **The hiring manager graded both versions blind.** In each round one agent graded the original and the tuned résumé as A and B, in random order (`work/ab_key.json`), so before and after come from the same judge on the same scale.
- **The interview prep is specific.** The hiring manager checked the A/B test's arithmetic. The report gives Jordan the numbers to have ready: a one-sided test fits about 4,000 accounts, and a two-sided test at that size has about 72% power.
