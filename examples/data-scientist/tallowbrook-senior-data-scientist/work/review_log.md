# Review log

Every reviewer ran as a separate agent with no access to the drafting conversation. Each agent's full reply is in `work/reviews/`.

## Round 1 (quality)

| Reviewer | Verdict | Applied | Not applied (why) |
|---|---|---|---|
| AI-slop screener | 7/10; 7 items | All 7: bullets grouped by project; Segment, Git and Tableau lines reworded; the 42% and 81% sentences fixed; the Skills "Workflow" line merged into "Tools" | Its Git rewrite used a semicolon, which fails the slop gate, so the line was split into two sentences instead. "Built and maintained the product team's Tableau dashboards" was kept while the page had room (the screener named it as the first cut if space ran short; it was cut in round 2) |
| Copy editor | 14 items | 12 | "A/B testing, churn modelling" in Skills: kept the posting's spelling "A/B tests" (changed to "A/B testing" in round 3 at the recruiter's request). "Kaplan–Meier" with an en dash: a hyphen is what people search for. Its fix 1 ("at a B2B SaaS") created a 4-word run shared with the posting, so the line became "in B2B SaaS at a …" |
| Fact-checker | 7 open items | 6 rewordings to the sources' words ("run A/B tests", "Designed and ran", "the variant raised", "mentored", the 42% and 81% sentences). "On tables that include about 2 billion time-punch events" cut: the answer gives the table's size but doesn't tie it to the finance work | None |

After round 1, the A/B test bullet gained two facts from answer 1 (the power calculation and the decision metric) to use the line the cut freed. Step 7 re-run: all checks pass, 3 free lines.

## Round 2 (recruiter verification)

| Reviewer | Verdict | Applied | Not applied (why) |
|---|---|---|---|
| Recruiter screen | Shortlist yes; reads as human 8/10; 5 of 11 searches missed | "product analytics" in the summary; "data pipeline", "event tracking" and "seat expansion" in the lines that describe that work (each is an accurate name for it); cut "All our analytics SQL and Python code is in Git." | "data scientist" / "data science": not the candidate's title or function (writing rules). "experiment": "A/B test" is the more specific term and is on the page |
| Hiring manager (A = tuned, B = base) | Tuned: 19 clear, 1 none (dbt), phone screen yes. Base: 10 clear, 5 weak, 5 none, phone screen no | Cut "Built and maintained the product team's Tableau dashboards" and "Supported the lending team's monthly reporting" (duties with no result; the recruiter agreed); pull-request bullet moved up under the mentoring bullet | None |

These were material changes (claims reworded, top bullets reordered), so step 7 ran again. The cuts left 6 free lines and no true material was left to add (every ask was graded clear), so `"fill": true` widened the line spacing to 1.32. Round 3 used fresh agents.

## Round 3 (recruiter verification, fresh agents)

| Reviewer | Verdict | Applied | Not applied (why) |
|---|---|---|---|
| Fact-checker (changed lines) | 2 open items | "Documented the 60 core tables in a data dictionary" became "Wrote a data dictionary for the 60 core Snowflake tables" (the old wording read as the finance pipeline's tables) | Churn validation windows (the period of the 6% base rate; the 42% is over a quarter, the model predicts 60 days): the page states it exactly as answer 4 does, so it stays and goes to the candidate under "To confirm" |
| Recruiter screen | Shortlist yes; reads as human 8/10; 11 of 12 searches hit | "A/B testing" in Skills (the form recruiters search; the bullets keep the posting's "A/B tests") | "data scientist": as in round 2. "Neither showed a clear difference" kept (the round-1 screener and both hiring managers asked to keep it). Maple Ridge stays at one bullet (round 2 cut the other as filler). The pull-request and seat-expansion lines stay (they prove M7, R7 and R1) |
| Hiring manager (A = base, B = tuned) | Tuned: 19 clear, 1 none (dbt), phone screen yes. Base: 8 clear, 7 weak, 5 none, phone screen no | "(lifelines)" cut from the Cox bullet (a library name means nothing to a recruiter; it stays in Skills) | Reorder to the posting's order: not applied as asked, because the writing rules don't allow the posting's order. A smaller move of the A/B test and the offsite talk up the page was tried, then undone after the final fact-check below. "Defined" for "Worked out": that rewords toward the posting's verb, and R4 is graded clear as written |

## After round 3

| Reviewer | Verdict | Applied | Not applied (why) |
|---|---|---|---|
| Fact-checker (last edits) | 2 open items | The reorder was undone: below the offsite bullet, "for the churn work" read as the analysis behind the offsite. The bullets are back in the order round 3 graded | Churn validation windows: as above |

Final step 7: PDF checks PASS, slop gates PASS, FILL FULL. The scores in the report come from the round-3 hiring manager. The page it graded differs from the final page only in the three edits checked above.
