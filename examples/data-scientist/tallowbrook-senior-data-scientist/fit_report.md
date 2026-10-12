# Fit report: Senior Data Scientist, Product Analytics at Tallowbrook

2026-10-12 · Base résumé: Jordan_Lee_Resume.pdf · Posting: pasted text

## Overall fit

| Measure | Before | After |
|---|---|---|
| Overall fit (0-100) | 63 (Fair) | 98 (Strong) |
| Must-haves shown clearly | 5 of 8 | 8 of 8 |
| ATS alignment (0-100) | 73.7 | 94.7 (honest ceiling 94.7) |
| Must-have hard terms present | 6 of 7 | 7 of 7 |
| Keyword overlap (secondary, no target) | 32.8 | 51.3 |

Interview risk: Medium (0 high, 6 medium, 1 low)
Recruiter screen: shortlist yes; reads-as-human score 8/10
Quality: slop gates PASS; PDF checks PASS; page FULL

**Verdict:** A strong fit. You work in the same domain (payroll and time-tracking SaaS for small businesses), and the page now proves the two things this job centres on: a churn model Customer Success works from, and an A/B test you designed and sized. The biggest gap is level, not skills. Every title on the page says Analyst and the role is Senior Data Scientist, so the phone screen will test whether your scope is senior. Both the recruiter and the hiring manager agents would phone-screen this page. Neither would screen the original, which showed no A/B testing.

**Eligibility:** Hybrid, two days a week in the King West office in Toronto. You live in Toronto, so this is met. The posting doesn't mention work authorisation or sponsorship.

## ATS alignment

- **ATS alignment:** 94.7/100, honest ceiling 94.7, before 73.7. The ceiling is the best score possible without claiming anything untrue. The only term between it and 100 is dbt, which you haven't used.
- **Must-have hard terms present:** 7 of 7. Not on the page because they aren't true: dbt (a nice-to-have). Left off by choice: none.
- **Spelling matched to the posting:** new terms use the posting's spelling: "A/B tests", "survival analysis" and "B2B SaaS". Skills also says "A/B testing", the form recruiters often search for.
- **Job title:** the posting's core title, "data scientist", is not on the page, because your title is Product Data Analyst. The page says "product data analyst" and "product analytics", which is both your field and the posting's. Searches for "data scientist" won't find it, so make the case for your level in a cover note and in the phone screen.
- **Parse checks:** 1 page (Letter). Two PDF readers extract the same text (100% agreement), with no garbled characters. All four section headers, the email and the phone were found, and the email and LinkedIn links are clickable. In your original PDF, the bullets came out as garbled characters.
- **Keyword overlap (secondary):** 32.8 to 51.3. A page in your own words scores below a keyword-stuffed one, and there is no target for this number.

## Interview risk: Medium

| Claim on the page | Question it will trigger | Risk | How to prepare |
|---|---|---|---|
| "Sized it with a power calculation to detect a 4-point lift … About 4,000 new accounts were split 50/50" | A 4-point lift from 41% needs about 2,400 accounts per arm (80% power, two-sided 5%), and you had about 2,000. What did you assume? | medium | Know your inputs. A one-sided test needs about 1,900 per arm, which fits. Two-sided at 2,000 per arm gives about 72% power. Also: a fixed six-week horizon with no peeking, a sample-ratio check, and the interval on the 6-point lift (roughly 3 to 9 points). |
| "the variant raised activation from 41% to 47%" | How is week-one activation defined, and did the lift carry through to 90-day retention? | medium | The metric's exact definition and why it was the decision metric. Whether both arms were followed to 90 days. The 81% vs 63% gap was observational, and the test was the causal check. |
| "about 42% of the model's top 200 accounts cancelled, against a 6% base churn rate" | Over what window is the 6%? How did you keep the evaluation clean once Customer Success started calling, and do the calls save anyone? | medium | The out-of-time split and the churn window. Precision in the top 200 (about 7 times the base rate) and recall. Leakage checks. Why 200 (team capacity). Say plainly that the calls were never tested against an uncalled group. |
| "Fitted a Cox survival model for the churn work" | What did the Cox model add over the classifier, and how did you check proportional hazards? | medium | Time-to-cancel framing and censoring. Hazard ratios as drivers you can explain, while the scikit-learn model ranks accounts. Schoenfeld residual checks. What the junior analyst's add-on extension found. |
| "Built the account health score … from weighted product-usage signals" | How were the weights set, how do you know the score tracks churn, and why keep it beside the churn model? | medium | Whether the weights were fitted or set by judgement. Churn rate by score band. When the score and the model disagree, and what Customer Success does with each. |
| "Presented churn drivers to the CEO, CFO and VP of Product … pricing was changed afterwards" | What did you recommend, and how much of the pricing change came from your analysis? | medium | Your specific recommendation and its evidence. Who decided, and what else they weighed. Keep "afterwards", not "because", unless you can name your part. |
| "Reviewed about five GitHub pull requests a week" | What do you look for in an analyst's pull request? Give one review that changed a result. | low | Join grain, leakage, reproducibility, tests. One concrete catch, and how you gave the feedback. |

Nothing was softened or cut for interview risk. The fact-checker had one figure taken off the page because no source tied it to that line (see "Numbers removed").

## Gaps to improve

**Not shown** (must-haves first, then responsibilities graded none)

None. The hiring manager graded every must-have and every responsibility clear.

**Shown only weakly or in part** (must-haves and responsibilities graded weak): none graded weak, but the hiring manager called two of the clear grades thin:
- **Expansion analysis (R1):** the page says you analysed seat expansion, but not what you found. One sentence with the finding would make it strong.
- **Models used every week (R3):** the page shows a nightly churn score, a monthly call list and a daily health score. If Customer Success works from the health score weekly, say so. There's no expansion model, because you said there was no upsell model.

**Nice-to-haves not shown:** dbt.

**To confirm (could raise the fit if true):**
1. The churn validation windows. What period does the 6% base rate cover, and is the 42% cancellations within 60 days or within the quarter? The page states it the way you did.
2. Do the finance transformations read the time-punch events table (about 2 billion rows)? If they do, that size can go back on the pipeline line.
3. What did the seat-expansion analysis find, and what did the 2024 pricing review decide?
4. Does Customer Success use the health score or the churn list every week?
5. Be ready to explain "about 4,000 new accounts in six weeks" next to "38,000 active accounts". At that pace the base turns over quickly, and a sharp interviewer will notice.

## Quality check

| Check | Result |
|---|---|
| Slop gates (script) | PASS |
| Reads as human (recruiter agent) | 8/10 (the first draft scored 7/10 with the slop screener) |
| Recruiter shortlist | yes |
| Fact-check | 0 open items on the page, and 1 question for you (To confirm, item 1) |
| Copy edit | 12 of 14 fixes applied |
| PDF checks | PASS |
| Page fill | FULL. The reviewers cut three lines with no result and the fact-checker cut one clause. Every ask was then graded clear, and no true material was left, so `"fill": true` widened the line spacing to 1.32 (the font stayed at 10.5 pt). Answers to To confirm items 2 to 4 would fill that space with evidence instead. |
| Review rounds | 3 rounds plus a final fact-check, all as separate agents: 3 quality reviewers, then a recruiter and a hiring manager twice (fresh agents each time). Details in work/review_log.md |

All checks ran.

## What changed

**Biggest rewrites**
1. Before: "Results-driven data professional with 6+ years of experience leveraging data to drive business decisions. Passionate about turning complex datasets into actionable insights for cross-functional stakeholders."
   After: "Product data analyst with seven years in analytics, the last four and a half in product analytics for a B2B SaaS payroll and time-tracking company whose customers have 5 to 200 employees. I build the churn model and account health score that Customer Success works from, and I run A/B tests with the product team. Every quarter I present a retention review to the VP of Product."
   Why: it says what you do and for whom, in the posting's domain, without stock phrases. Your dates show seven years, not "6+".
2. Before: "Built a churn model in Python (pandas, scikit-learn) that flags small-business accounts likely to cancel in the next 60 days; customer success now calls the top 200 accounts each month."
   After: "Built the Python churn model (pandas, scikit-learn) that scores all 38,000 active accounts every night and flags those likely to cancel within 60 days. In a held-out quarter, about 42% of the model's top 200 accounts cancelled, against a 6% base churn rate. Customer Success calls the top 200 each month."
   Why: it adds the scale and the validation from your answers. The 42% now reads as a test of the model, not of the calls.
3. Before: "Analysed retention for the time-tracking add-on and found that accounts which connected their scheduling tool in week one retained 18 points better at 90 days. The onboarding flow was changed to prompt that step."
   After: "Analysed retention for the time-tracking add-on. Of the add-on accounts that connected their scheduling tool in week one, 81% were retained at 90 days, against 63% of those that did not. A new onboarding checklist was built to push that step." The A/B test of that checklist comes next.
   Why: "18 points better" became the two rates you gave, and the test that followed covers a must-have the old page never showed.

**Added from your other sources** (your notes and answers):
- the checklist A/B test and the two pricing-page tests (M4, R2)
- the Cox model and the mentoring (N1, R7)
- pull-request reviews (M7, R7)
- the account health score (R3, R5)
- the CEO, CFO and VP of Product offsite (M8, R6)
- the seat-expansion analysis (R1)
- the data dictionary (R5)
- B2B SaaS and the customers' size (N4, N5)

**Added to fill the page:**
- From your second batch of answers: the churn model scores all 38,000 accounts every night (R3).
- From your first answers: the power calculation and decision metric on the A/B test line (M4).
- Layout: `"fill": true`, line spacing 1.32.

**Cut:**
- "Responsible for building and maintaining Tableau dashboards", "Helped with monthly reporting…" and "Assisted in a data quality project…": duties with no result. Tableau stays in the health-score line.
- "All analytics SQL and Python … is in Git": it read as box-ticking, and the pull-request line already shows it.
- From Skills: R, Jira, Confluence, Agile, Communication and Leadership. Nothing on the page backs them, and the hiring manager marked "Leadership" with nothing behind it as a high-risk question.

**Numbers removed:**
- "about 2 billion" (the time-punch events table): your answer gave its size but not that the finance pipeline reads it. Put it back on the line where it belongs (To confirm, item 2).
- "18 points" became 81% vs 63% (the same fact).
- "6+ years" became "seven years".

**Decisions for you:**
- Level: the page never calls you a data scientist, because that isn't your title. If you see your modelling work as data science, say so in a cover note rather than on the page.
- "Worked out the Segment event tracking…": the hiring manager preferred your original verb, "Defined". The recruiter thought both versions sat close to the posting's wording. Either is true.
