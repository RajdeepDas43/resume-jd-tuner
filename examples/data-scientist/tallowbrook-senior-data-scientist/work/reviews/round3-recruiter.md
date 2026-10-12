# Round 3: Recruiter screen, fresh agent (raw reply)

**1. ATS searches**

1. `"data scientist" OR "data science"`: **No.** Neither phrase appears anywhere. The title is "Product Data Analyst" and "senior" is missing too. This is the first search I'd run. The job title can't change, so the gap stays unless the summary can honestly call the modelling data science.
2. `"product analytics" AND ("B2B" OR "SaaS")`: **Yes.** "in product analytics for a B2B SaaS payroll and time-tracking company".
3. `"SQL" AND "Python" AND ("pandas" OR "scikit-learn" OR "statsmodels")`: **Yes.** "Python churn model (pandas, scikit-learn)" and "SQL, Python (pandas, scikit-learn, statsmodels, lifelines)".
4. `"A/B testing" OR "experimentation" OR "experiment design"`: **Only if the ATS stems words.** The page says "A/B tests" and "A/B test", never "A/B testing" or "experimentation". Changing "Methods: A/B tests" to "A/B testing" is a free reword.
5. `"churn model" OR "propensity model"`: **Yes.** "Built the Python churn model".
6. `("Snowflake" OR "BigQuery" OR "Redshift") AND ("Airflow" OR "dbt")`: **Yes.** "Built a Snowflake and Airflow data pipeline". There is no dbt, which is a nice-to-have and can't be added.
7. `"survival analysis" OR "causal inference"`: **Yes.** "survival analysis (Kaplan-Meier, Cox)".
8. `("Segment" OR "Amplitude" OR "Mixpanel") AND "event tracking"`: **Yes.** "the Segment event tracking".
9. `"payroll" OR "workforce" OR "scheduling"`: **Yes.** "Clearwater Payroll" and "their scheduling tool".
10. `"retention" AND "activation" AND "expansion"`: **Yes.** "Analysed retention", "week-one activation" and "seat expansion".
11. `"Git" AND ("code review" OR "pull requests")`: **Yes**, through "Git, GitHub" and "GitHub pull requests". The phrase "code review" never appears.
12. `"mentored" AND "presented"`: **Yes.** "mentored a junior analyst" and "Presented churn drivers to the CEO, CFO and VP of Product".

**2. The 30-second skim**

The domain and scale are close to ours: payroll and time-tracking SaaS for firms with "5 to 200 employees", 38,000 accounts scored every night (we serve 40,000), and a churn model whose top 200 accounts cancelled at about 42% against a 6% base rate. The retention story is the best thing on the page: a gap of 81% vs 63%, then a properly sized A/B test that raised activation from 41% to 47%. Two things raise an eyebrow: the title "Product Data Analyst", with no "senior", for a Senior Data Scientist role, and nearly three years at Maple Ridge covered by a single bullet. Two things are confusing: there are two churn models (scikit-learn and Cox) with no word on how they relate, and "A new onboarding checklist was built" doesn't say who built it. "Neither showed a clear difference" is honest but spends a line on a full page, and the 2024 pricing-review bullet gives no result.

**3. Decision**

**Shortlist: yes.** Every must-have is backed by a specific bullet: 4.5 years of B2B SaaS product analytics, scikit-learn, Snowflake, Airflow, a properly sized A/B test, a churn model Customer Success acts on, pull-request review and presentations to executives, plus three of the four nice-to-haves. The open question is level, not fit: the phone screen should check whether the work behind an analyst title matches a senior data scientist's scope, and what level and pay the candidate expects.

**Reads as the candidate's own: 8/10** (10 means it is entirely their voice). It uses plain verbs and real numbers, admits a test with no clear result, and has no "leveraged" or "data-driven". These lines cost points:
- "Worked out the Segment event tracking for new features with product managers before launch": this nearly repeats our posting's "define event tracking before features ship".
- "Reviewed about five GitHub pull requests a week": a line on its own that reads like ticking the code-review requirement.
- "For the 2024 pricing review, analysed seat expansion…": it seems to be there to say "expansion" and gives no finding.
- "The time-tracking add-on's pricing was changed afterwards.": it hints at impact without saying what the candidate did.

```json
{"shortlist": "yes", "slop_score": 8, "notes": "Near-exact domain and skills match backed by specific numbers; the main risks are the analyst title missing every 'data scientist' search and a few lines that echo the posting."}
```
