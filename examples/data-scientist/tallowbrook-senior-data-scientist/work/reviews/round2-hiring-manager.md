# Round 2: Hiring manager (raw reply)

Labels for this round, kept from the agent: A = tuned résumé, B = base résumé (`work/ab_key.json`).

## Résumé A

**Grades:** 19 of the 20 asks are clear. N2 (dbt) is none. Two of the clears are thin. R1's expansion part rests on one line that gives no result. R3's model feeds a monthly call list, and the posting says weekly.

**Overclaims:** none for the level. The title is "analyst", which is the only gap for a senior role, and the mentoring, code-review and offsite lines cover it. "The time-tracking add-on's pricing was changed afterwards" implies credit without claiming it, so be ready to say which part of the change was yours.

**Jargon:** none that an outsider would trip on.

**Cut or reorder** (there are 3 spare lines, so these changes are for signal, not space):
- Cut "Built and maintained the product team's Tableau dashboards." and "Supported the lending team's monthly reporting…". Both are duties with no result.
- Keep the two pricing tests with no clear result. Stated plainly, they show a testing habit rather than one test.
- Move the PR-review bullet up under the mentoring bullet, and move the seat-growth bullet next to the offsite bullet.
- Keep the retention bullet directly above the checklist test, because the test bullet refers back to it.

**Phone-screen: yes.** Every must is proven, most with numbers, in our own domain.

**Questions it will trigger** (the claim and what a strong answer covers are in the JSON):
1. Churn lift: over what window is the 6%, and did the Customer Success calls change the outcome you measured? *Medium.*
2. 81% vs 63%: is that selection or a real effect, and did 90-day retention move? *High.*
3. Power: a 4-point lift from 41% needs about 2,400 accounts per arm at 80% power and 5% two-sided. You had about 2,000. *Medium.*
4. Pricing change: what did you recommend, and how much of the change was yours? *Medium.*
5. Cox model: why Cox, and how did you check proportional hazards? *Medium.*
6. Health score: how were the weights set and checked? *Medium.*
7. PR reviews: what do you check, and what has a review caught? *Low.*

## Résumé B

**Grades:** clear: M1, M2, M3, M5, M6, M8, R3, R4, R5, N3. Weak: M7, R1, R6, N4, N5. None: M4, R2, R7, N1, N2. A/B testing is a must and a core duty, and it is missing.

**Overclaims:** Skills lists R, Jira, Confluence, Agile, Communication and Leadership, and no bullet backs any of them. "Leadership" on a page with no mentoring or code review invites a probe. "6+ years" undersells the dates, which show seven.

**Jargon:** "member records" is credit-union wording for customers. It is minor, and the line should go anyway.

**Cut or reorder:**
- Cut the summary, since "Results-driven… Passionate about turning complex datasets into actionable insights" says nothing a reader can check. Or reword it using the churn and retention facts already on the page.
- Bullet every line and open Clearwater with the churn model. Move the "Responsible for… Tableau dashboards" line to the end, or cut it.
- Cut "Helped with monthly reporting…" and "Assisted in a data quality project…". They describe duties with no results.
- Cut R, Jira, Confluence, Agile, Communication and Leadership from Skills. That also removes the line that holds only "Leadership".

**Phone-screen: no.** It misses a must completely and shows no senior scope: no mentoring, no code review and no executive audience. The payroll-software fit shows only in the employer's name.

**Questions it will trigger:**
1. Churn model: how many of the 200 flagged accounts cancel, and against what base rate? *Medium.*
2. 18-point gap: is it selection or a real effect, and did the new onboarding prompt work? *High.*
3. VP review: name one decision it changed. *Medium.*
4. Snowflake and Airflow: how do you test and monitor the jobs? *Low.*
5. Segment: walk me through a tracking plan. *Low.*
6. R and Leadership: where did you use them? *High.*

**Before either version goes out:** the two versions don't share the same facts. Only B has R, Jira, Confluence, Agile and the member-records project. Only A has the A/B test, the Cox model, the mentoring and most of the numbers. Check every line against the source résumé.

```json
{"A": {"grades": [
  {"id": "M1", "grade": "clear", "evidence": "Product data analyst with seven years in analytics, the last four and a half in B2B SaaS (Product Data Analyst, Mar 2022 – Present)"},
  {"id": "M2", "grade": "clear", "evidence": "Wrote and scheduled SQL transformations in Snowflake with Airflow to replace the finance team's hand-updated spreadsheets. Documented the 60 core tables in a data dictionary."},
  {"id": "M3", "grade": "clear", "evidence": "Built the Python churn model (pandas, scikit-learn) that scores all 38,000 active accounts every night"},
  {"id": "M4", "grade": "clear", "evidence": "Sized it with a power calculation to detect a 4-point lift in week-one activation, the decision metric. About 4,000 new accounts were split 50/50 over six weeks, and the variant raised activation from 41% to 47%."},
  {"id": "M5", "grade": "clear", "evidence": "In a held-out quarter, about 42% of the model's top 200 accounts cancelled, against a 6% base churn rate. Customer Success calls the top 200 each month."},
  {"id": "M6", "grade": "clear", "evidence": "Wrote and scheduled SQL transformations in Snowflake with Airflow"},
  {"id": "M7", "grade": "clear", "evidence": "Reviewed about five GitHub pull requests a week from the team's two other analysts. All our analytics SQL and Python code is in Git."},
  {"id": "M8", "grade": "clear", "evidence": "Presented churn drivers to the CEO, CFO and VP of Product at the 2024 planning offsite. The time-tracking add-on's pricing was changed afterwards."},
  {"id": "R1", "grade": "clear", "evidence": "Retention: 81% were retained at 90 days, against 63% of those that did not. Activation: the variant raised activation from 41% to 47%. Expansion: analysed seat growth among accounts that added the time-tracking add-on (thinnest; no result given)."},
  {"id": "R2", "grade": "clear", "evidence": "Designed and ran the checklist's A/B test with the onboarding product manager and an engineer."},
  {"id": "R3", "grade": "clear", "evidence": "scores all 38,000 active accounts every night and flags those likely to cancel within 60 days … Customer Success calls the top 200 each month. (Churn only; the list is worked monthly, not weekly.)"},
  {"id": "R4", "grade": "clear", "evidence": "Decided with product managers which Segment events to track for new features before launch."},
  {"id": "R5", "grade": "clear", "evidence": "Wrote and scheduled SQL transformations in Snowflake with Airflow; health score: It is refreshed daily by an Airflow job"},
  {"id": "R6", "grade": "clear", "evidence": "Presented churn drivers to the CEO, CFO and VP of Product at the 2024 planning offsite."},
  {"id": "R7", "grade": "clear", "evidence": "mentored a junior analyst on survival analysis and reviewed her extension of the model to add-on accounts; Reviewed about five GitHub pull requests a week from the team's two other analysts."},
  {"id": "N1", "grade": "clear", "evidence": "Fitted a Cox survival model (lifelines) for the churn work"},
  {"id": "N2", "grade": "none", "evidence": "dbt appears nowhere on the page."},
  {"id": "N3", "grade": "clear", "evidence": "Decided with product managers which Segment events to track for new features before launch."},
  {"id": "N4", "grade": "clear", "evidence": "B2B SaaS at a payroll and time-tracking company whose customers have 5 to 200 employees"},
  {"id": "N5", "grade": "clear", "evidence": "the last four and a half in B2B SaaS"}],
 "risks": [
  {"claim": "In a held-out quarter, about 42% of the model's top 200 accounts cancelled, against a 6% base churn rate. Customer Success calls the top 200 each month.", "question": "The model predicts 60-day churn but you validated on a quarter, and Customer Success calls the top 200. Over what window is the 6%, and how did you keep the calls from changing the outcome you measured?", "risk": "medium", "prep": "A label window matched to the 60-day target; a validation period before calls began, or a holdout group that was not called; precision at 200 against the base rate (about 7x lift), plus recall and calibration; features cut off at the scoring date to avoid leakage."},
  {"claim": "Of the add-on accounts that connected their scheduling tool in week one, 81% were retained at 90 days, against 63% of those that did not.", "question": "Accounts that connect early may simply be more committed. How did you separate selection from effect, and did the checklist move 90-day retention or only activation?", "risk": "high", "prep": "Likely confounders (size, plan, intent) and any controls; why the A/B test isolates the checklist's effect on activation but not on retention; whether the test cohorts were followed to 90 days and what they showed; what is still unknown."},
  {"claim": "Sized it with a power calculation to detect a 4-point lift in week-one activation … About 4,000 new accounts were split 50/50 over six weeks", "question": "From a 41% baseline, a 4-point lift needs roughly 2,400 accounts per arm at 80% power and 5% two-sided, and you had about 2,000. What alpha, power and sidedness did you use, and why six weeks?", "risk": "medium", "prep": "The exact inputs and the resulting sample size; the one- or two-sided choice; a fixed end date with no peeking; the confidence interval on the 6-point lift; the unit of assignment and a sample-ratio check."},
  {"claim": "Presented churn drivers to the CEO, CFO and VP of Product at the 2024 planning offsite. The time-tracking add-on's pricing was changed afterwards.", "question": "What exactly did you recommend, and how much of the pricing change came from your analysis rather than other inputs?", "risk": "medium", "prep": "The specific recommendation and its evidence; who decided and what else they weighed; how the story was framed for a CEO and CFO; what happened after the change, if it was measured."},
  {"claim": "Fitted a Cox survival model (lifelines) for the churn work", "question": "Why a Cox model alongside a 60-day classifier, and how did you check the proportional-hazards assumption?", "risk": "medium", "prep": "Censoring and the time-to-cancel framing; Schoenfeld-residual or log-log checks and the fix when they fail; time-varying covariates; hazard ratios to explain drivers versus the scikit-learn model to rank accounts; what the junior analyst's add-on extension changed."},
  {"claim": "Built the account health score for Customer Success from weighted product-usage signals.", "question": "How were the weights set, and how do you know the score predicts anything the churn model does not?", "risk": "medium", "prep": "Whether the weights came from judgement or were fitted; checks against later churn; why Customer Success needs both a score and a model; what happens when the two disagree."},
  {"claim": "Reviewed about five GitHub pull requests a week from the team's two other analysts.", "question": "What do you check in an analyst's SQL or Python pull request? Tell me about a review that caught a real problem.", "risk": "low", "prep": "Join fan-out, NULL handling, date filters and time zones, tests or data checks, readability and reproducibility; one concrete catch; how feedback is given to a junior."}]},
 "B": {"grades": [
  {"id": "M1", "grade": "clear", "evidence": "Product Data Analyst | Mar 2022 – Present (about 4.5 years; the summary claims 6+ years overall)"},
  {"id": "M2", "grade": "clear", "evidence": "Wrote and scheduled SQL transformations in Snowflake with Airflow, replacing spreadsheets the finance team updated by hand."},
  {"id": "M3", "grade": "clear", "evidence": "Built a churn model in Python (pandas, scikit-learn) that flags small-business accounts likely to cancel in the next 60 days"},
  {"id": "M4", "grade": "none", "evidence": "No A/B test anywhere on the page, not even in Skills."},
  {"id": "M5", "grade": "clear", "evidence": "Built a churn model in Python (pandas, scikit-learn) … customer success now calls the top 200 accounts each month."},
  {"id": "M6", "grade": "clear", "evidence": "Wrote and scheduled SQL transformations in Snowflake with Airflow"},
  {"id": "M7", "grade": "weak", "evidence": "Git appears only in Skills; no code review is shown."},
  {"id": "M8", "grade": "clear", "evidence": "Presented the quarterly retention review to the VP of Product."},
  {"id": "R1", "grade": "weak", "evidence": "Retention only: Analysed retention for the time-tracking add-on and found that accounts which connected their scheduling tool in week one retained 18 points better at 90 days. Activation is only implied; expansion is absent."},
  {"id": "R2", "grade": "none", "evidence": "No experiment of any kind is shown, with product managers, engineers or anyone else."},
  {"id": "R3", "grade": "clear", "evidence": "flags small-business accounts likely to cancel in the next 60 days; customer success now calls the top 200 accounts each month. (Churn only; monthly, not weekly; no scale or accuracy given.)"},
  {"id": "R4", "grade": "clear", "evidence": "Worked with product managers to define event tracking (Segment) for new features before launch."},
  {"id": "R5", "grade": "clear", "evidence": "Wrote and scheduled SQL transformations in Snowflake with Airflow, replacing spreadsheets the finance team updated by hand."},
  {"id": "R6", "grade": "weak", "evidence": "Presented the quarterly retention review to the VP of Product. One VP only; no executive team, and no recommendation or decision is shown."},
  {"id": "R7", "grade": "none", "evidence": "No mentoring or code review is shown; Leadership in Skills is not evidence of either."},
  {"id": "N1", "grade": "none", "evidence": "No survival analysis or causal inference is shown."},
  {"id": "N2", "grade": "none", "evidence": "dbt appears nowhere on the page."},
  {"id": "N3", "grade": "clear", "evidence": "Worked with product managers to define event tracking (Segment) for new features before launch."},
  {"id": "N4", "grade": "weak", "evidence": "Only the employer name Clearwater Payroll signals payroll; the page never says what the company sells."},
  {"id": "N5", "grade": "weak", "evidence": "Never stated; small-business accounts and a time-tracking add-on only hint at B2B SaaS."}],
 "risks": [
  {"claim": "Built a churn model in Python (pandas, scikit-learn) that flags small-business accounts likely to cancel in the next 60 days; customer success now calls the top 200 accounts each month.", "question": "Of the 200 accounts you flag each month, how many actually cancel, against what base rate, and how did you validate the model before customer success used it?", "risk": "medium", "prep": "The label window and features, with a leakage cut-off; validation on a later time period; precision at 200 against base churn, plus recall and calibration; how the calls affect the churn you later measure."},
  {"claim": "accounts which connected their scheduling tool in week one retained 18 points better at 90 days. The onboarding flow was changed to prompt that step.", "question": "Accounts that connect early may just be more committed. How did you separate selection from effect, and how did you test whether the new prompt worked?", "risk": "high", "prep": "Confounders and controls; how the change was evaluated (a controlled test, if one was run), with its decision metric and result; whether 90-day retention moved; what is still unknown."},
  {"claim": "Presented the quarterly retention review to the VP of Product.", "question": "Name one decision that came out of a review. What did you recommend, and what changed?", "risk": "medium", "prep": "The review's core metrics; one recommendation, the decision it drove and the outcome; how the message was shaped for a non-technical leader."},
  {"claim": "Wrote and scheduled SQL transformations in Snowflake with Airflow, replacing spreadsheets the finance team updated by hand.", "question": "How do you test and monitor those transformations, and what happens when a run fails before finance needs the numbers?", "risk": "low", "prep": "Runs that are safe to repeat or load only new data, data tests, alerts and retries, backfills, and how the new tables were matched against the old spreadsheets."},
  {"claim": "Worked with product managers to define event tracking (Segment) for new features before launch.", "question": "Walk me through a tracking plan you wrote: event names, properties, account versus user identity, and how you caught broken events after launch.", "risk": "low", "prep": "Naming conventions, required properties, identify and group calls for business accounts, QA before release, and monitoring event volumes after launch."},
  {"claim": "SQL, Python, R, Tableau, Power BI, Excel, Snowflake, Airflow, Git, Segment, Jira, Confluence, Agile, Communication, Leadership", "question": "No bullet uses R or shows leadership. What have you built in R, and whom have you mentored or led?", "risk": "high", "prep": "A concrete R project and its outcome, or an honest admission of light use; specific mentoring or code-review examples behind Leadership; otherwise drop both from the page."}]}}
```
