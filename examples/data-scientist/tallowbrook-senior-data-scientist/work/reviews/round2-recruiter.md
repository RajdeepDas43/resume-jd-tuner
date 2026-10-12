# Round 2: Recruiter screen (raw reply)

**1. ATS searches**

1. `("data scientist" OR "data science") AND ("churn" OR "retention")`: **Miss.** Neither phrase appears, and neither does "senior". The titles are "Product Data Analyst" and "Business Intelligence Analyst", and they can't honestly change.
2. `"product analytics" OR "product analyst"`: **Miss.** "Product Data Analyst" doesn't match the exact phrase "product analyst". Calling the work "product analytics" in the summary is an honest rewording and the most useful fix.
3. `"Python" AND "SQL" AND ("scikit-learn" OR "statsmodels") AND "churn"`: **Hit:** "Built the Python churn model (pandas, scikit-learn)".
4. `"A/B test" OR "experimentation"`: **Hit:** "Designed and ran the checklist's A/B test", backed up by "power calculation". The word "experiment" never appears, though the posting asks for someone to "design and read experiments".
5. `("Snowflake" OR "BigQuery" OR "Redshift") AND ("Airflow" OR "dbt")`: **Hit:** "SQL transformations in Snowflake with Airflow". There's no dbt; leave it out.
6. `"data pipeline" OR "ETL"`: **Miss.** The only "pipeline" on the page is the credit union's "loan-pipeline report", even though the Snowflake/Airflow work is a data pipeline.
7. `"survival analysis" OR "causal inference"`: **Hit:** "survival analysis", "Cox survival model (lifelines)".
8. `("Segment" OR "Amplitude" OR "Mixpanel") AND "event tracking"`: **Miss.** "Segment" matches, but the bullet says "which Segment events to track". Searching "tracking" on its own only finds "time-tracking".
9. `("retention" OR "activation") AND "expansion"`: **Miss.** "Expansion" appears twice in the posting and never on the page, even though the seat-growth analysis is expansion work.
10. `("payroll" OR "workforce" OR "HR") AND "SaaS"`: **Hit:** "B2B SaaS at a payroll and time-tracking company".
11. `("mentored" OR "mentoring") AND "pull requests" AND "Git"`: **Hit:** "mentored a junior analyst", "Reviewed about five GitHub pull requests a week".

Five of these eleven searches miss someone who fits almost every line of the posting.

**2. The 30-second skim**

The fit is almost uncanny: payroll and time-tracking SaaS for customers with 5 to 200 employees, a nightly churn model that Customer Success works from (about 42% of its top 200 accounts cancelled, against a 6% base rate), and an A/B test sized with a power calculation that lifted activation from 41% to 47%. What raises an eyebrow is seniority: every title says Analyst and 2019–2022 was BI reporting, so the relevant experience is four and a half years, just over the bar, with no senior title. "A new onboarding checklist was built" and "pricing was changed afterwards" are passive, so I can't tell which results Jordan drove and which Jordan only saw happen. The seat-growth bullet doesn't say what the analysis found. The first-person summary is unusual but reads fine, and Jordan is local to Toronto.

**3. Decision**

**Shortlist: yes.** Every must-have is backed by evidence: SQL and Python, a churn model a business team uses, A/B tests Jordan designed, Snowflake and Airflow, code reviews in Git, and a presentation to the CEO and CFO. Three nice-to-haves are also there (survival analysis, Segment, payroll software), and the open question about seniority is exactly what a phone screen is for.

**Reads as the candidate's own writing: 8/10.** Plain verbs, specific numbers and an honest null result ("Neither showed a clear difference") sound like a real analyst. The lines that cost points:
- "All our analytics SQL and Python code is in Git." This line only exists to tick off the Git requirement. Cut it: Git and GitHub still appear in Skills and in the pull-request bullet.
- "Built and maintained the product team's Tableau dashboards." and "Supported the lending team's monthly reporting in SQL Server and Excel." Both are template filler with no outcome.

Fix "product analytics" and "expansion" first. Add the other missing phrases only where the sentence still reads naturally.

```json
{"shortlist": "yes", "slop_score": 8, "notes": "Every must-have is evidenced and the payroll-SaaS fit is near exact, but analyst-only titles and five missing posting phrases (product analytics, experiment, data pipeline, event tracking, expansion) hide the résumé from five of eleven searches; cut the Git box-ticking line."}
```
