# Round 3: Fact-checker, re-check of the changed lines (raw reply)

**Flags**

**1. Churn validation: the time windows don't match (unclear how the numbers were measured)**
- Quote: "flags those likely to cancel within 60 days. In a held-out quarter, about 42% of the model's top 200 accounts cancelled, against a 6% base churn rate."
- Problem: The model predicts cancellations within 60 days. The 42% covers a quarter. The 6% has no period at all. If the 6% is a monthly rate, the comparable quarterly rate is much higher, and the gap is much smaller than a reader will assume. A second figure raises the same question: about 4,000 new accounts in six weeks is roughly 35,000 a year, beside 38,000 active accounts.
- Source: Q4 "On a held-out quarter: about 42% of the top 200 flagged accounts cancelled, against a 6% base churn rate." It gives no period for the 6%.
- Fix: The wording already matches Q4, so nothing needs cutting. Ask Jordan two things: what period the 6% covers, and whether the 42% cancelled within 60 days or within the quarter. If both figures cover the same quarter, say so ("…cancelled that quarter, against 6% of all accounts"). Until he answers, keep the current text.

**2. "the 60 core tables" now reads as the finance pipeline's tables**
- Quote: "…with scheduled SQL transformations. Documented the 60 core tables in a data dictionary."
- Problem: This sentence now comes straight after the finance pipeline sentence, so "the 60 core tables" reads as that pipeline's tables. In the source they are the core tables of the whole Snowflake warehouse.
- Source: notes "Wrote a data dictionary for the 60 core tables in Snowflake."
- Fix: "Wrote a data dictionary for the 60 core Snowflake tables." This adds 6 characters. Use it only if the line doesn't wrap; otherwise leave the sentence as it is.

**Checked, no change needed**
- "Built a Snowflake and Airflow data pipeline … with scheduled SQL transformations": the closing phrase keeps this to what the base line says ("Wrote and scheduled SQL transformations in Snowflake with Airflow").
- Tools "SQL Server, Excel": no bullet backs them since the lending bullet was cut, but both still have a source (the base Maple Ridge bullet and the base Skills line). Keep them, or cut them to free space.
- The pricing-review bullet sits right above "pricing was changed afterwards". That hints the seat analysis led to the price change, but it doesn't claim it. "Seat expansion" means the same as Q6's "seat growth".
- The page claims no effect from the Customer Success calls, which fits Q4. "Her" matches Q3.
- None of Redshift, BigQuery, dbt, Spark, the target company's name or the 2-billion figure appear. "Toronto, ON" and the Canadian spelling (Analysed, cancelled, Fitted) are correct.

**Numbers**

| Number | Where | Source | Supported |
|---|---|---|---|
| seven years | Summary | Jun 2019 – Present (7 yr 4 mo at Oct 2026) | yes |
| four and a half | Summary | Mar 2022 – Present (4 yr 7 mo) | yes |
| 5 to 200 employees | Summary | notes | yes |
| every quarter | Summary | base "quarterly retention review" | yes |
| Mar 2022 – Present | Clearwater | base | yes |
| 38,000; every night | Churn | Q10 | yes |
| 60 days | Churn | base | yes |
| held-out quarter; about 42%; top 200 | Churn | Q4 | yes |
| 6% base churn rate | Churn | Q4 | yes (period unclear, flag 1) |
| top 200 each month | Churn | base | yes |
| daily | Health score | notes | yes |
| about five a week; two other analysts | Pull requests | notes | yes |
| week one; 81%; 63%; 90 days | Retention | Q8; base "18 points" | yes |
| 4-point lift | A/B test | Q1 | yes |
| about 4,000; 50/50; six weeks | A/B test | notes; Q1 | yes |
| 41% to 47% | A/B test | notes | yes |
| two smaller tests | Pricing page | Q1 | yes |
| 2024 pricing review | Seat analysis | Q6 | yes |
| 2024 planning offsite | Offsite | notes | yes |
| 60 core tables | Pipeline | notes | yes (flag 2) |
| Jun 2019 – Feb 2022 | Maple Ridge | base | yes |
| weekly; about six hours to under one | Maple Ridge | base | yes |
| 2015 – 2019 | Education | base | yes |
| +1 416 555 0187 | Header | base | yes |

Open items: 2
