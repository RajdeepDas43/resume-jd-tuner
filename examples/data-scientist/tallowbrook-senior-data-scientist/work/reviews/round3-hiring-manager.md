# Round 3: Hiring manager, fresh agent (raw reply)

Labels for this round, kept from the agent: A = base résumé, B = tuned résumé (`work/ab_key.json`). These are the grades the report uses.

**Résumé A: 8 clear, 7 weak, 5 none.** Of the eight musts, five are clear, M7 (Git) and M8 (leaders) are weak, and M4 (A/B tests) is missing.

**Overclaims.** Few. This page undersells the candidate. "Communication" and "Leadership" are Skills labels with nothing behind them. The retention bullet implies cause. An 18-point gap for accounts that connected a tool is only a correlation, yet "The onboarding flow was changed" is offered as the payoff with no test behind it.

**Jargon.** "member records" is a credit-union word for customers. "retained 18 points better" means percentage points and reads awkwardly.

**Cut or reorder.**
- Replace the summary. "Results-driven … actionable insights for cross-functional stakeholders" is filler. Rebuild it only from lines already on the page. "6+ years" undersells dates that show seven.
- Make the churn-model paragraph the first bullet. It is the strongest line, and it isn't even bulleted.
- Move "Responsible for building and maintaining Tableau dashboards" to the end, or cut it. Opening with a duty makes the candidate read as a BI analyst, not a senior data scientist.
- Cut "Helped with monthly reporting…" and "Assisted in a data quality project…". Keep the six-hours-to-one bullet.
- In Skills, cut Communication, Leadership, Jira, Confluence and Agile. List pandas and scikit-learn, which the churn line already names.

**Phone screen: no, but it's close.** The payroll domain, a churn model Customer Success uses, and Snowflake, Airflow and Segment all fit. But this job runs on experiments, and the page shows none.

**Questions (details in the JSON):**
- High risk: the untested onboarding change, and "Leadership".
- Medium risk: how the churn model was validated, Git, the VP review, and dashboards versus modelling.
- Low risk: the pipeline.

**Résumé B: 19 clear, 1 none (dbt).** A line on the page proves every must and every role duty.

**Overclaims.** None for the candidate's level, and the work reads as senior. Three lines will get pressed:
- "The time-tracking add-on's pricing was changed afterwards" sits next to the offsite talk and implies credit for the change.
- The power calculation doesn't quite add up. Detecting a 4-point lift from a 41% base needs roughly 2,400 accounts per arm (80% power, two-sided 5% test). "About 4,000 … split 50/50" gives about 2,000 per arm. That works for a one-sided test, or at about 72% power. The candidate must know which.
- "41% to 47%" has no confidence interval. The 42%-versus-6% line gives no time window for churn. It also doesn't say how the held-out quarter stayed clear of Customer Success calls.

**Jargon.**
- "week-one activation" is an internal metric that is never defined.
- "6% base churn rate" has no time window.
- "weighted product-usage signals" is vague.
- "lifelines" (a Python library) in a bullet means nothing to a recruiter.

**Cut or reorder.**
- Follow the posting's order: churn model, retention analysis, checklist A/B test, pricing-page tests, CEO/CFO offsite, seat expansion, health score, Snowflake pipeline, Segment, Cox and mentoring, PR reviews. Right now the A/B test sits sixth and the executive talk ninth.
- Change "Worked out the Segment event tracking" to "Defined the Segment event tracking". That is the posting's verb, and A's.
- Keep the two pricing tests that found no difference. Honest null results read well to a data science manager.

**Phone screen: yes.**

**Questions (details in the JSON):**
- Medium risk: the power calculation, whether the activation lift carried through to retention, how the churn model was validated and whether the calls work, the Cox model, the health-score weights, and credit for the pricing change.
- Low risk: code review.

**One check outside the hiring manager's role:** B states many specifics A lacks, such as 38,000 accounts, the power calculation, the Cox model, and the CEO and CFO. I graded both as written. Before B goes out, confirm every number in it is in the candidate's source. Both keep "Toronto, ON" and Canadian spelling, and neither names Tallowbrook.

```json
{"A": {"grades": [
{"id": "M1", "grade": "clear", "evidence": "'Product Data Analyst | Mar 2022 – Present': over four and a half years in product analytics, with Maple Ridge before it."},
{"id": "M2", "grade": "clear", "evidence": "'Wrote and scheduled SQL transformations in Snowflake with Airflow, replacing spreadsheets the finance team updated by hand.'"},
{"id": "M3", "grade": "clear", "evidence": "'Built a churn model in Python (pandas, scikit-learn) that flags small-business accounts likely to cancel in the next 60 days'"},
{"id": "M4", "grade": "none", "evidence": "No A/B test or experiment anywhere on the page, not even in Skills."},
{"id": "M5", "grade": "clear", "evidence": "'Built a churn model in Python (pandas, scikit-learn)...; customer success now calls the top 200 accounts each month.'"},
{"id": "M6", "grade": "clear", "evidence": "'Wrote and scheduled SQL transformations in Snowflake with Airflow'"},
{"id": "M7", "grade": "weak", "evidence": "Git appears only in Skills; no line shows code review."},
{"id": "M8", "grade": "weak", "evidence": "'Presented the quarterly retention review to the VP of Product.' One product leader and no decision tied to it; 'Communication' is only a Skills label."},
{"id": "R1", "grade": "weak", "evidence": "'Analysed retention for the time-tracking add-on and found that accounts which connected their scheduling tool in week one retained 18 points better at 90 days.' Retention, with activation implied; no expansion."},
{"id": "R2", "grade": "none", "evidence": "No A/B test with product managers or engineers."},
{"id": "R3", "grade": "weak", "evidence": "'customer success now calls the top 200 accounts each month.' One churn model feeding a monthly call list; weekly use and expansion not shown."},
{"id": "R4", "grade": "clear", "evidence": "'Worked with product managers to define event tracking (Segment) for new features before launch.' Engineering not named."},
{"id": "R5", "grade": "clear", "evidence": "'Wrote and scheduled SQL transformations in Snowflake with Airflow, replacing spreadsheets the finance team updated by hand.'"},
{"id": "R6", "grade": "weak", "evidence": "'Presented the quarterly retention review to the VP of Product.' One VP and findings only; no directors, executive team or recommendations."},
{"id": "R7", "grade": "none", "evidence": "No mentoring or review of others' code; 'Leadership' in Skills has no line behind it."},
{"id": "N1", "grade": "none", "evidence": "No survival or causal method; the 18-point gap is a raw comparison."},
{"id": "N2", "grade": "none", "evidence": "dbt not mentioned."},
{"id": "N3", "grade": "clear", "evidence": "'Worked with product managers to define event tracking (Segment) for new features before launch.'"},
{"id": "N4", "grade": "weak", "evidence": "'Clearwater Payroll' and 'time-tracking add-on' imply payroll software, but the page never says what the company sells."},
{"id": "N5", "grade": "weak", "evidence": "'small-business accounts likely to cancel' and an 'add-on' suggest B2B subscription software; SaaS is never stated."}
],
"risks": [
{"claim": "Built a churn model in Python (pandas, scikit-learn) that flags small-business accounts likely to cancel in the next 60 days; customer success now calls the top 200 accounts each month.", "question": "How good is the model? What share of the top 200 actually cancel, and how did you validate it?", "risk": "medium", "prep": "Out-of-time validation; cancellation rate in the top 200 against the base rate; recall; leakage checks; why 200 (team capacity); whether the calls save accounts, ideally measured against an uncalled holdout."},
{"claim": "accounts which connected their scheduling tool in week one retained 18 points better at 90 days. The onboarding flow was changed to prompt that step.", "question": "Engaged accounts connect tools anyway. How do you know prompting the step improves retention, and was the change A/B tested?", "risk": "high", "prep": "Names the selection bias; what was controlled for; a test with a pre-set decision metric, a power calculation and a result; whether 90-day retention moved after the change."},
{"claim": "Skills: Leadership", "question": "You list leadership. Whom have you mentored, and whose SQL and Python do you review?", "risk": "high", "prep": "A named mentee and what was taught; review cadence; one review comment that changed an analysis."},
{"claim": "Skills: Git", "question": "How does your analysis code reach production? Do you use branches and pull requests, and who reviews your work?", "risk": "medium", "prep": "Branch and pull-request flow; what a review checks (join grain, leakage, tests); how Airflow DAGs and model code are versioned."},
{"claim": "Wrote and scheduled SQL transformations in Snowflake with Airflow, replacing spreadsheets the finance team updated by hand.", "question": "Walk me through that pipeline. How do you test the SQL, and what happens when a run fails?", "risk": "low", "prep": "DAG structure; incremental versus full loads; safe reruns; data tests and alerts; who maintains it; how finance signed off on the numbers."},
{"claim": "Presented the quarterly retention review to the VP of Product.", "question": "What did you recommend in the last review, and what did the VP do with it?", "risk": "medium", "prep": "One concrete recommendation, the evidence behind it, the decision that followed, and how it was pitched to a non-technical audience."},
{"claim": "Responsible for building and maintaining Tableau dashboards for the product team.", "question": "How much of your week is dashboards versus models and experiments? This is a senior data scientist role.", "risk": "medium", "prep": "An honest time split; modelling and experiment work that shipped; evidence of senior scope such as designing tests and reviewing others' work."}
]},
"B": {"grades": [
{"id": "M1", "grade": "clear", "evidence": "'Product data analyst with seven years in analytics, the last four and a half in product analytics for a B2B SaaS payroll and time-tracking company'"},
{"id": "M2", "grade": "clear", "evidence": "'Built a Snowflake and Airflow data pipeline that replaced the finance team's hand-updated spreadsheets with scheduled SQL transformations.'"},
{"id": "M3", "grade": "clear", "evidence": "'Built the Python churn model (pandas, scikit-learn) that scores all 38,000 active accounts every night'"},
{"id": "M4", "grade": "clear", "evidence": "'Designed and ran the checklist's A/B test... Sized it with a power calculation to detect a 4-point lift in week-one activation, the decision metric.'"},
{"id": "M5", "grade": "clear", "evidence": "'In a held-out quarter, about 42% of the model's top 200 accounts cancelled, against a 6% base churn rate. Customer Success calls the top 200 each month.'"},
{"id": "M6", "grade": "clear", "evidence": "'Built a Snowflake and Airflow data pipeline that replaced the finance team's hand-updated spreadsheets'"},
{"id": "M7", "grade": "clear", "evidence": "'Reviewed about five GitHub pull requests a week from the team's two other analysts.'"},
{"id": "M8", "grade": "clear", "evidence": "'Presented churn drivers to the CEO, CFO and VP of Product at the 2024 planning offsite. The time-tracking add-on's pricing was changed afterwards.'"},
{"id": "R1", "grade": "clear", "evidence": "Retention: 'Of the add-on accounts that connected their scheduling tool in week one, 81% were retained at 90 days, against 63%'; activation: 'the variant raised activation from 41% to 47%'; expansion: 'analysed seat expansion among accounts that added the time-tracking add-on.'"},
{"id": "R2", "grade": "clear", "evidence": "'Designed and ran the checklist's A/B test with the onboarding product manager and an engineer.'"},
{"id": "R3", "grade": "clear", "evidence": "'scores all 38,000 active accounts every night' and 'Built the account health score for Customer Success... refreshed daily by an Airflow job and shown in Tableau.' No expansion model."},
{"id": "R4", "grade": "clear", "evidence": "'Worked out the Segment event tracking for new features with product managers before launch.' Engineering not named."},
{"id": "R5", "grade": "clear", "evidence": "'Built a Snowflake and Airflow data pipeline that replaced the finance team's hand-updated spreadsheets with scheduled SQL transformations. Documented the 60 core tables in a data dictionary.'"},
{"id": "R6", "grade": "clear", "evidence": "'Presented churn drivers to the CEO, CFO and VP of Product at the 2024 planning offsite.'"},
{"id": "R7", "grade": "clear", "evidence": "'mentored a junior analyst on survival analysis and reviewed her extension of the model to add-on accounts'; 'Reviewed about five GitHub pull requests a week from the team's two other analysts.'"},
{"id": "N1", "grade": "clear", "evidence": "'Fitted a Cox survival model (lifelines) for the churn work'"},
{"id": "N2", "grade": "none", "evidence": "dbt not mentioned."},
{"id": "N3", "grade": "clear", "evidence": "'Worked out the Segment event tracking for new features with product managers before launch.'"},
{"id": "N4", "grade": "clear", "evidence": "'a B2B SaaS payroll and time-tracking company whose customers have 5 to 200 employees'"},
{"id": "N5", "grade": "clear", "evidence": "'product analytics for a B2B SaaS payroll and time-tracking company'"}
],
"risks": [
{"claim": "Sized it with a power calculation to detect a 4-point lift in week-one activation, the decision metric. About 4,000 new accounts were split 50/50 over six weeks", "question": "A 4-point lift off a 41% base, at 80% power and a two-sided 5% test, needs roughly 2,400 accounts per arm. You had about 2,000. What did your calculation assume?", "risk": "medium", "prep": "Baseline, minimum detectable effect, alpha, power and sidedness (one-sided fits about 1,900 per arm; two-sided gives about 72% power); a fixed six-week horizon with no peeking; a sample-ratio check; the interval on the 6-point lift (roughly 3 to 9 points)."},
{"claim": "the variant raised activation from 41% to 47%", "question": "How is week-one activation defined, and did the lift carry through to 90-day retention?", "risk": "medium", "prep": "The exact metric definition and why it was the decision metric; 90-day retention of both test arms; recognising that the 81% versus 63% gap was observational and the test was the causal check."},
{"claim": "In a held-out quarter, about 42% of the model's top 200 accounts cancelled, against a 6% base churn rate. Customer Success calls the top 200 each month.", "question": "Over what window is the 6%? Once Customer Success started calling, how did you keep the evaluation clean, and do the calls save anyone?", "risk": "medium", "prep": "Out-of-time split and churn window; precision and lift (about 7x) in the top 200; recall; leakage checks; why 200 (team capacity); an uncalled holdout or uplift measure for the calls."},
{"claim": "Fitted a Cox survival model (lifelines) for the churn work", "question": "What did the Cox model add over the classifier, and how did you check proportional hazards?", "risk": "medium", "prep": "Time-to-cancel framing and censoring; hazard ratios as explainable churn drivers; Schoenfeld residual checks; time-varying usage covariates; concordance; how it fed the offsite talk."},
{"claim": "Built the account health score for Customer Success from weighted product-usage signals.", "question": "How were the weights chosen, how do you know the score tracks churn, and why keep it beside the churn model?", "risk": "medium", "prep": "How weights were set (fitted or judgement); churn rate by score band; agreement with the model; what Customer Success uses each one for; drift monitoring."},
{"claim": "Presented churn drivers to the CEO, CFO and VP of Product at the 2024 planning offsite. The time-tracking add-on's pricing was changed afterwards.", "question": "What did you recommend, how much did your analysis drive the pricing change, and what happened after it?", "risk": "medium", "prep": "The specific recommendation and its evidence, including the seat-expansion analysis; honest attribution among other inputs; framing for a CFO; churn and expansion tracked after the change."},
{"claim": "Reviewed about five GitHub pull requests a week from the team's two other analysts.", "question": "What do you look for in an analyst's pull request? Give one review that changed a result.", "risk": "low", "prep": "Join grain, leakage, reproducibility, tests and readability; a concrete catch; how the survival-analysis mentoring was structured and what the junior analyst's extension found."}
]}}
```
