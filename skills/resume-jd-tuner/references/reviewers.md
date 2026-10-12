# Reviewer and recruiter agents

Five briefs: three quality reviewers (step 8) and two recruiter-side verifiers (step 9). Each runs as an independent agent that has not seen your reasoning or earlier drafts, which is the point: a fresh reader catches what the writer has stopped seeing.

## Contents

1. How to launch them
2. Brief 1: AI-slop screener
3. Brief 2: Copy editor
4. Brief 3: Fact-checker
5. Brief 4: Recruiter screen
6. Brief 5: Hiring manager
7. Applying the feedback
8. The review log

## 1. How to launch them

Reviewers need no tools. Paste everything they need into the prompt:

```text
<brief, copied from below>

THE JOB POSTING
<work/jd.txt>

THE RÉSUMÉ (text from the compiled PDF, one line per bullet)
<work/tuned_review.txt>

CONSTRAINTS
- Never add a fact, number, tool or skill. Suggest only cuts, reorders and rewordings.
- Space: <"the page is full: anything added must be paid for by a cut" or "N free lines at the bottom">
- Fixed lines that must stay word for word: <from the conventions file, or "none">
- Location: <what the résumé shows and why>
- The target company's name appears only inside product names.
- Spelling: <British or American>

[Fact-checker only] SOURCES
<the base résumé text in full, any other version used, the conventions file, and the user's
confirmations from this conversation, quoted exactly>

[Hiring manager only] THE ASKS (grade every one, using these ids)
<id | type | ask, one per line, from work/jd_asks.json>

[Hiring manager only] RÉSUMÉ A and RÉSUMÉ B
<the base résumé's text and the tuned résumé's text, one line per bullet, in random order;
note privately which is which>

Reply in the format given in the brief, about 600 words at most.
```

- With a tool that starts separate agents (Claude Code's Agent tool, formerly Task; not a to-do list tool): launch briefs 1 to 3 together in one message (step 8), and later briefs 4 and 5 together (step 9). Use fresh agents each round, and after material changes re-run both 4 and 5.
- Without subagents: play each brief yourself, one at a time. Start each from its brief and the materials only, write its full verdict before starting the next, and judge the draft as a stranger would.
- Give the fact-checker the full sources, never excerpts: excerpts produce false alarms. Older résumé versions are weaker sources than the user's own confirmations in this conversation.

## 2. Brief 1: AI-slop screener

> You are a senior recruiter for this kind of role. You read hundreds of résumés a week and you can tell when one was written or polished by an LLM. Read this résumé as a recruiter would and flag everything that reads machine-written or that a reader would stumble on: templated structure (bullets in the posting's order, every bullet the same length and rhythm), echoes of the posting's wording, buzzwords, stacked or decorative metrics, tool dumps, "-ing" tails ("..., resulting in"), lists of three used for rhythm, "not just X but Y", em dashes, colon lead-ins, and phrases nobody says out loud.
>
> For each problem: the exact quote, why it reads machine-written, and a plain rewrite that keeps every fact.
> Then: a score from 1 to 10 for "reads as if the candidate wrote it" (10 = fully human), the three changes worth the most, and what must NOT be changed because it already sounds like a real person.

## 3. Brief 2: Copy editor

> You are a plain-English copy editor. Check: unclear referents ("it", "this", "them"), misplaced modifiers, parallel structure, unexpanded abbreviations a recruiter outside the field would not know, repeated words, sentences over about 30 words, tense consistency (present for the summary, past for past work), grammar, punctuation and the spelling system.
>
> For each problem: the exact quote, the fix, and the reason in a few words. End with the five most important fixes.

## 4. Brief 3: Fact-checker

> You check a résumé against its sources. Compare every claim and every number with the sources provided. Flag anything that is:
> - unsupported (not in any source),
> - stronger than its source ("led" where the source says "worked on", "every" where it says "most", "built" where it says "ran"),
> - a number whose baseline or measurement is unclear,
> - against a fixed line, a never-mention term or another convention.
>
> For each: the quote, the problem, the source line it should match, and a fix that stays within the source. Then a table of every number on the page: number | where it appears | source line | supported (yes/no). End with "Open items: N".

## 5. Brief 4: Recruiter screen

> You are the recruiter who owns this job in an applicant tracking system. Do three things.
> 1. ATS searches: write the 8 to 12 keyword searches you would actually run to find candidates for this posting (exact terms in quotes, combined with AND/OR as you would type them). For each, say whether this résumé would come up, quoting the matching words, or what is missing.
> 2. The 30-second skim: what stands out, what raises an eyebrow, and anything confusing, in at most five sentences.
> 3. Decide: would you shortlist this candidate for a phone screen (yes, maybe or no), and why in two sentences. Score from 1 to 10 how much the page reads as if the candidate wrote it, and quote the lines that cost points.
>
> End with this JSON block and nothing after it:
> ```json
> {"shortlist": "yes|maybe|no", "slop_score": 0, "notes": "one sentence"}
> ```

## 6. Brief 5: Hiring manager

> You are the hiring manager for this exact role. You have two versions of one candidate's résumé, A and B. Grade each of them against every ask in the list, using the ids given, by the same standard:
> - **clear**: a line on the page proves it (quote the line),
> - **weak**: hinted at, only listed in Skills, or proven only for a smaller scope (say why),
> - **none**: not shown.
>
> Then, for each résumé: flag overclaims for the candidate's level, employer jargon an outsider won't understand, bullets you would cut or reorder, and whether you would phone-screen (yes/no). List the 5 to 8 interview questions it will trigger, aimed at its specific claims ("You cut refund errors to zero. How did you know?"). For each question: the claim, the question, the risk that the candidate struggles to back it up (low, medium or high), and what a strong answer covers.
>
> End with this JSON block and nothing after it (every ask id exactly once per résumé):
> ```json
> {"A": {"grades": [{"id": "M1", "grade": "clear|weak|none", "evidence": "quoted line or reason"}],
>        "risks": [{"claim": "...", "question": "...", "risk": "low|medium|high", "prep": "..."}]},
>  "B": {"grades": [...], "risks": [...]}}
> ```

Assign the labels at random (the tuned résumé is A or B) and don't tell the agent which is which. Map the reply back: the base résumé's grades go to `work/grades_before.json`; the tuned résumé's grades and risks go to `work/grades_after.json`, with the recruiter's JSON added there under a `"recruiter"` key. If a JSON block is malformed or misses ask ids, ask the same agent to resend it rather than repairing it by guesswork. When you play the brief yourself (no subagents), grade the base résumé first and the tuned one second, from the texts alone, by the same standard.

## 7. Applying the feedback

- **Reviewers may only cut, reorder or reword.** Never add a fact, number or tool a reviewer suggests unless the user confirms it.
- **When reviewers conflict,** this order wins: the user's conventions and confirmations, then the fact-checker, then the hiring manager on fit, then the recruiter, then the slop screener, then the copy editor. When fit and voice pull apart, keep the requirement and say it in plainer words.
- **A rewording or reorder for fit must still pass the writing rules.** Never reword toward the posting's phrasing, and never put the bullets in the posting's order, even when a reviewer asks for it.
- **High-risk interview claims:** if the candidate cannot back one up, soften it to what the sources support or cut it. If they can, keep it and put the prep note in the report.
- **Keep what the user explicitly asked for,** and note the reviewer's objection in the log.
- **If cuts leave the page short,** restore verified, relevant content using the fill order in SKILL.md step 7 before touching spacing. If a reviewer cut something added to fill the page, add a different true item instead of re-adding it.
- **List every number removed** in the report so the candidate can restore one they can defend.
- After applying, rebuild and re-run SKILL.md step 7.

## 8. The review log

`work/review_log.md`, one section per round:

```markdown
## Round 1 (quality)
| Reviewer | Verdict | Applied | Not applied (why) |
|---|---|---|---|
| AI-slop screener | 6/10; 9 items | 8 rewrites | "drove" kept: candidate led the migration (confirmed) |
| Copy editor | 7 items | 7 | - |
| Fact-checker | 2 open items | both fixed | - |

## Round 2 (recruiter verification)
...
```
