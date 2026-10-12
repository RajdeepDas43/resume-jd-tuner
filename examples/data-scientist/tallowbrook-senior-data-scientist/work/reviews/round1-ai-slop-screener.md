# Round 1: AI-slop screener (raw reply)

## Recruiter read: Jordan Lee for Senior Data Scientist, Product Analytics

**Problems**

1. **Bullet order.** There are twelve bullets, roughly one per line of the posting, and related work is split apart:
   - The churn model is bullet 1 but the health score is bullet 7.
   - "the new onboarding checklist" (bullet 2) appears before "a new onboarding checklist" (bullet 3).
   - "pricing was changed afterwards" (5) comes before the seat-growth analysis "for the 2024 pricing review" (6).

   **Why:** It reads like the posting turned into bullets.
   **Fix (reorder only):** churn model, Cox model, health score; add-on retention, checklist test, pricing-page tests; seat growth, offsite; Snowflake, Segment, dashboards; reviews.

2. "Defined Segment event tracking with product managers for new features before launch."
   **Why:** It's almost a copy of the posting's "define event tracking before features ship."
   **Rewrite:** "Worked out with product managers which Segment events to track for new features before launch."

3. "All analytics SQL and Python at Clearwater lives in Git." and the skills line "Workflow: Git, GitHub pull requests"
   **Why:** Both are written to tick "Version control with Git." Nobody writes that sentence unprompted, and nobody lists pull requests as a skill.
   **Rewrite:** "Reviewed about five GitHub pull requests a week from the team's two other analysts; all our analytics SQL and Python is in Git." Move "Git, GitHub" onto the tools line, rename it "Tools," and drop the Workflow line.

4. "An Airflow job refreshes it daily and Tableau shows it."
   **Why:** The sentence exists to place two tool names, and nobody says "Tableau shows it."
   **Rewrite:** "Built the account health score for Customer Success from weighted product-usage signals, refreshed daily by an Airflow job and shown in Tableau."

5. "Customer Success calls the top 200 each month, and in a held-out quarter about 42% of those accounts cancelled"
   **Why:** It reads as if the calls failed, with 42% of the accounts CS phoned cancelling anyway.
   **Rewrite:** "In a held-out quarter, about 42% of its top 200 accounts cancelled, against a 6% base rate. Customer Success calls the top 200 each month."

6. "Accounts that connected their scheduling tool in week one kept 81% at 90 days"
   **Why:** Kept 81% of what? The reader has to go back.
   **Rewrite:** "Of accounts that connected their scheduling tool in week one, 81% were retained at 90 days, against 63% of those that did not, so a new onboarding checklist was built to push that step." Bullet 3 then says "…the A/B test of that checklist…"

7. "Replaced spreadsheets the finance team updated by hand with SQL transformations in Snowflake, scheduled in Airflow, on tables that include about 2 billion time-punch events."
   **Why:** It misleads on first read (did finance update them "by hand with SQL"?), and then tools and a size figure are tacked on with commas.
   **Rewrite:** "Replaced the finance team's hand-updated spreadsheets with SQL transformations in Snowflake that Airflow runs on a schedule, over tables holding about 2 billion time-punch events."

**Score: 7/10**

The wording is plain and specific. What gives it away is the order that follows the posting, a few lines that exist only to place keywords, and a repeated bullet shape: a long sentence followed by a short, flat one.

**Three changes worth the most**

1. Group the bullets by project (item 1). This also fixes the checklist and pricing mix-ups.
2. Rewrite the Segment, Git and Tableau lines (items 2–4).
3. Fix the 42% and 81% sentences (items 5–6). They're in the first two bullets, which every reader gets to.

**Space**

- Each rewrite is about as long as the line it replaces.
- Dropping the Workflow line frees one more line.
- If the page still runs long, cut "Built and maintained the product team's Tableau dashboards." first. It's the only bullet with no detail, and it repeats the posting's "Build and maintain."

**Do not change**

- "Ran two smaller A/B tests on the pricing page. Neither showed a clear difference." Admitting tests that found nothing is the most human line on the page.
- The first-person summary and the real title "Product data analyst." Also keep "customers have 5 to 200 employees" and "Every quarter I present a retention review to the VP of Product."
- "taught a junior analyst survival analysis and reviewed her extension of the model to add-on accounts"
- "the onboarding product manager and an engineer" and "a sample sized for a 4-point lift."
- "The time-tracking add-on's pricing was changed afterwards," because it doesn't claim credit.
- "time-punch events" and "from about six hours to under one."
- There are no em dashes and no "-ing" endings like "resulting in." Don't add any while editing.
