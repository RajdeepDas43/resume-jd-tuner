# Round 1: Fact-checker (raw reply)

Line numbers refer to `work/review_packet_round1.txt`.

**Flags**

1. **Summary (l.39):** "design A/B tests with the product team"
   - Problem: Stronger than the source. Jordan designed one test. For the two pricing tests he only says he "run" them.
   - Source: answers l.148.
   - Fix: "…and run A/B tests with the product team."

2. **Churn bullet (l.45):** "Customer Success calls the top 200 each month, and in a held-out quarter about 42% of those accounts cancelled, against a 6% base rate."
   - Problem: "Those accounts" makes the 42% read as a result of the calls. The source gives it as a check of the model and says the calls were never tested.
   - Source: answers l.154.
   - Fix: "In a held-out quarter, about 42% of the top 200 flagged accounts cancelled, against a 6% base churn rate. Customer Success calls the top 200 each month."

3. **A/B bullet (l.47):** "Designed and analysed"
   - Problem: "Analysed" is not in any source.
   - Source: answers l.148 ("designed"), notes l.134 ("Ran").
   - Fix: "Designed and ran" (also the JD's verb).

4. **A/B bullet (l.47):** "week-one activation rose from 41% to 47%"
   - Problem: Reads as a before/after change. The source compares the variant with the control.
   - Source: notes l.134 ("The variant raised week-one activation from 41% to 47%").
   - Fix: "…and the variant raised week-one activation from 41% to 47%."

5. **Retention bullet (l.46):** "kept 81% at 90 days, against 63%"
   - Problem: "Kept 81%" doesn't say 81% of what, and it could be read as revenue kept. The source means the share of add-on accounts retained.
   - Source: answers l.162; base l.100–101.
   - Fix: "81% of add-on accounts that connected their scheduling tool in week one were retained at 90 days, against 63% of those that did not, so…"

6. **SQL bullet (l.53):** "on tables that include about 2 billion time-punch events"
   - Problem: The source gives the size of the time-punch table behind Jordan's SQL work in general. It doesn't say the finance transformations read that table.
   - Source: answers l.167.
   - Fix: Confirm with Jordan. If he doesn't confirm, cut the clause.

7. **Survival bullet (l.55):** "taught a junior analyst survival analysis"
   - Problem: Slightly stronger than the source's verb.
   - Source: notes l.133 ("Mentored a junior analyst on survival analysis").
   - Fix: "then mentored a junior analyst on survival analysis and reviewed…" (also the JD's verb).

**Conventions:** All clean.
- "Toronto, ON" appears in the header and for both jobs.
- Spelling is British throughout (Analysed, cancelled, Fitted).
- No "Tallowbrook".
- No Redshift, BigQuery, dbt or Spark.
- No upsell model is claimed (answers l.158).

All fixes are rewordings or cuts. Items 2, 4, 5 and 7 add a few words each. Cutting the clause in item 6 would make up for them.

**Numbers**

| Number | Where | Source line | Supported |
|---|---|---|---|
| +1 416 555 0187 | Header | base l.84 | yes |
| seven years | Summary | worked out from Jun 2019 to now (base l.107); base l.87 said "6+" | yes (about 7 y 4 m) |
| four and a half years | Summary | worked out from Mar 2022 to now (base l.92) | yes (about 4 y 7 m) |
| 5 to 200 employees | Summary | notes l.137 | yes |
| every quarter | Summary | base l.105 | yes |
| 38,000 accounts, nightly | Churn | answers l.170 | yes |
| 60 days | Churn | base l.98–99 | yes |
| top 200 each month | Churn | base l.99 | yes |
| about 42% | Churn | answers l.154 | yes (reword, item 2) |
| 6% | Churn | answers l.154 | yes |
| 81% vs 63% at 90 days | Retention | answers l.162 | yes (reword, item 5) |
| week one | Retention, A/B | base l.101; answers l.148 | yes |
| about 4,000 accounts | A/B | notes l.134 | yes |
| 50/50 | A/B | answers l.148 | yes |
| six weeks | A/B | notes l.134 | yes |
| 4-point lift | A/B | answers l.148 | yes |
| 41% → 47% | A/B | notes l.134 | yes (reword, item 4) |
| two pricing tests | Pricing | answers l.148 | yes |
| 2024 offsite | Offsite | notes l.138 | yes |
| 2024 pricing review | Seat growth | answers l.158 | yes |
| daily refresh | Health score | notes l.135 | yes |
| about 2 billion | SQL | answers l.167 | number yes; tie to the finance work no (item 6) |
| 60 core tables | SQL | notes l.136 | yes |
| about five PRs a week | Reviews | notes l.132 | yes |
| two other analysts | Reviews | notes l.132 | yes |
| about six hours → under one | Maple Ridge | base l.114–115 | yes |
| Mar 2022 – Present | Clearwater | base l.92 | yes |
| Jun 2019 – Feb 2022 | Maple Ridge | base l.107 | yes |
| 2015 – 2019 | Education | base l.119 | yes |

Open items: 7
