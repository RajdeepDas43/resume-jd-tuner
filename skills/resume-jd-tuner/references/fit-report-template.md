# Fit report template

Write `fit_report.md` in exactly this order. Fill every section; write "None" rather than dropping one. Plain language, short sentences, no slop: this report is read by the candidate, and they will act on it. Paste numbers from `scoreboard.py`; never estimate them. Keep it scannable, about two screens: tables and short bullets over paragraphs.

````markdown
# Fit report: <posted job title> at <company>

<date> · Base résumé: <file name> · Posting: <URL, or "pasted text">

## Overall fit

<paste the scoreboard.py table here>

**Verdict:** <Two to four sentences. The band in words ("A good fit"), the two strongest reasons, the biggest gap, and whether a phone screen is likely and why. If the fit is weak, say so plainly and say what would change it.>

**Eligibility:** <the posting's eligibility rules (work authorisation, sponsorship, location limits, clearance, languages) and whether the sources settle them, or "None stated".>

## ATS alignment

- **ATS alignment:** <after>/100, honest ceiling <ceiling>, before <before>. The ceiling is the best score possible without claiming anything untrue; the gap between them is the terms the candidate does not have.
- **Must-have hard terms present:** <n> of <m>. Not on the page because they are not true: <terms or "none">. Left off by choice: <terms and why, e.g. "Java: only coursework, would invite questions">.
- **Spelling matched to the posting:** <terms switched, e.g. "Postgres to PostgreSQL", or "already matched">.
- **Job title:** <does the page carry the posting's core title ("data analyst") as the candidate's real title or function? If not, why not>.
- **Parse checks:** <one line from pdf_checks: pages, clean text layer, headers, email and phone, clickable links, fixed lines>.
- **Keyword overlap (secondary):** <before> to <after>. A page in the candidate's own words scores below a keyword-stuffed one; there is no target for this number.

## Interview risk: <Low | Medium | High>

| Claim on the page | Question it will trigger | Risk | How to prepare |
|---|---|---|---|
| <quote> | <question> | <low/medium/high> | <what a strong answer covers> |

<One sentence on anything softened or cut because it could not be defended.>

## Gaps to improve

**Not shown** (must-haves first, then responsibilities graded none)

| Gap | Type | Why it matters here | Before you apply | Longer term |
|---|---|---|---|---|
| <ask> | <must / responsibility> | <how central it is to the role> | <e.g. address it in the cover letter; prepare an adjacent example> | <e.g. a small project, a course, a certification> |

**Shown only weakly or in part** (must-haves and responsibilities graded weak): <each ask, the part that is missing (e.g. "cost per install shown, ROAS and CAC not"), and the one fact that would make it clear, or "None">

**Nice-to-haves not shown:** <short list, or "None">

**To confirm (could raise the fit if true):** <claims the sources didn't settle; tell me and I will re-tune>

## Quality check

| Check | Result |
|---|---|
| Slop gates (script) | <PASS / REVIEW items accepted and why> |
| Reads as human (recruiter agent) | <n>/10 |
| Recruiter shortlist | <yes / maybe / no> |
| Fact-check | <open items: 0> |
| Copy edit | <n fixes applied> |
| PDF checks | <PASS, or what failed and was fixed> |
| Page fill | <FULL, or the free lines left, why, and whether --fill or template spacing was used> |
| Review rounds | <n>, run as <separate agents / self-review> (details in work/review_log.md) |

<Checks that could not run, and why, or "All checks ran.">

## What changed

**Biggest rewrites**
1. Before: "<old line>"
   After: "<new line>"
   Why: <one line>
2. ...
3. ...

**Added from your other sources:** <facts brought in from notes or other résumé versions while writing, and the ask each proves, or "None">
**Added to fill the page:** <each step-7 addition and the ask it proves, plus any layout change (--fill, template spacing), or "None">
**Cut:** <bullets, skills or sections removed, and why>
**Numbers removed:** <each figure, so the candidate can restore any they can defend, or "None">
**Decisions for you:** <anything that needs the candidate's call, or "None">
````

## Notes on filling it in

- **Overall fit before and after** both come from the hiring manager in step 9, who grades the base and the tuned résumé in one pass without knowing which is which. The difference is what tuning achieved; honest gaps keep "after" below 100.
- **Interview risk** lists the hiring manager's questions. Keep high-risk rows only when the candidate can defend the claim and you have told them how; otherwise the claim should already be off the page.
- **Gaps:** must-haves first, then nice-to-haves. Be concrete and brief. "Learn Kubernetes" is not advice; "Deploy one service you already run to a managed Kubernetes cluster and write up what broke" is.
- If a step was skipped (no subagents, a missing package), say so in the quality section. Never mark a check as passed when it did not run.
