# Jordan's answers to the skill's questions (step 4)

Fictional, written for this example to show the interactive path.

1. Did you design the onboarding-checklist A/B test? How was it set up, and with whom?
   Yes. I designed it with the onboarding product manager and one engineer: a 50/50 split by account, sized with a power calculation for a 4-point lift, with week-one activation as the decision metric. I've also run two smaller pricing-page tests; both were inconclusive.
2. Did the test come out of your add-on retention analysis?
   Yes, the checklist was built to push the week-one scheduling connection.
3. Did you fit the survival models yourself?
   I fitted the Cox model myself first. The junior analyst then extended it to the add-on segment, and I reviewed her work.
4. How did you validate the churn model?
   On a held-out quarter: about 42% of the top 200 flagged accounts cancelled, against a 6% base churn rate. We never ran a controlled test of the Customer Success calls.
5. Is Clearwater's product SaaS?
   Yes, subscription software billed monthly per employee.
6. Any expansion analysis?
   I analysed seat growth for accounts that added the time-tracking add-on. It went into the deck for the 2024 pricing review. No upsell model.
7. Have you used statsmodels?
   Yes, for logistic regression and t-tests.
8. What was the 18-point retention gap compared against?
   Add-on accounts that did not connect their scheduling tool in week one: 81% against 63% at 90 days.

# Second batch (step 7: the page still had about three free lines)

9. How large are the tables behind your SQL work?
   The time-punch events table in Snowflake holds about 2 billion rows.
10. How often does the churn model run, and on how many accounts?
   Every night, on all 38,000 active accounts.
