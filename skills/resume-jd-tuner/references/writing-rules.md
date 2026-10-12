# Writing rules for the tuned résumé

Read this before step 5. Where it disagrees with an older note or template, this file and SKILL.md win.

## Contents

1. Bullets
2. Numbers
3. Voice: what reads as human, what reads as LLM
4. Summary
5. Skills
6. ATS alignment without stuffing
7. Location, company name, title
8. Layout basics

## 1. Bullets

- **One idea per bullet,** one to three short sentences. A bullet exists because it is a real piece of work, and one strong bullet often answers several asks. Never write one bullet per ask or follow the posting's order: a page that mirrors the posting's structure reads as generated.
- **Lead with the strongest stories for this job.** Order bullets within a role by relevance to the posting, not by date.
- **Vary the length.** Some bullets one line, the two or three best stories up to three lines. Identical shapes (result, metric, "by doing") on every line read as machine-written.
- **Plain past-tense verbs, varied:** built, ran, fixed, wrote, moved, cut, set up, designed, trained, sold, negotiated, taught. "Led", "owned" and "drove" only when the candidate truly led. No weak openers ("Responsible for", "Helped", "Worked on", "Involved in").
- **Keep the details only the person who did the work would know:** the cause of the bug, the trade-off taken, the design that was replaced, who used the result. They are what make a page read human, and they give the interviewer something real to ask about.
- **Count:** up to about eight bullets for the main recent role, two to four for older roles, one or two for roles more than ten years back. The main role may go past eight when the page has room and each extra bullet proves a different ask; never to repeat one.
- **Name things accurately.** A more specific term than the sources use ("learning-to-rank" for a ranking model, "ETL" for a script) is allowed only when it is the correct description of what was done. When unsure, keep the source's words and ask.
- Use `xyz-format.md` as a checklist for what a bullet carries (what was done, at what scale or with what result, how), never as a fill-in-the-blanks sentence.

## 2. Numbers

- Keep a figure only if the candidate can explain it in one sentence: the baseline and how it was measured. When you are unsure, keep it and ask (step 4) rather than deleting it silently.
- Drop decorative or unmeasured percentages ("operational efficiency up 45%").
- One metric per clause. Don't stack "manual work -65%, efficiency +45%" into one line.
- Don't reuse one "N+" figure for unrelated things, and don't present someone else's scale as the candidate's result ("an app with 100,000+ users" is the company's number, not theirs).
- Prefer modest, specific numbers ("about 83% against an 80% bar") over round, impressive ones.
- Six to ten numbers on a page is usually plenty.
- List every number you removed in the report's "What changed", so the candidate can restore one they can defend.

## 3. Voice: what reads as human, what reads as LLM

Hard limits (`slop_scan.py` checks the measurable ones on the PDF text; the reviewers judge the rest):

- Average sentence 20 words or fewer; none over about 35.
- No em dashes in prose, no semicolons, no "Bold lead-in: detail" bullets, at most one colon-introduced list per section. Em dashes and bold colon lead-ins are among the patterns readers now associate with LLM-written text.
- No run of four or more words copied from the posting, except names of products, tools, certifications and degrees.
- No "-ing" tails hung on a clause ("..., resulting in", "..., ensuring", "..., leveraging"), no lists of three used for rhythm, no "not just X but Y".
- Avoid absolutes (every, each, all, zero, no) unless literally true and checkable.

Banned words and phrases (all forms): leverage, robust, seamless, spearhead, drive or drove (adoption, growth), ensure, foster, empower, elevate, streamline, unlock, holistic, synergy, cutting-edge, state-of-the-art, world-class, best-in-class, end-to-end (except as a real technical term, e.g. "end-to-end tests"), passionate, dynamic, innovative, impactful, journey, delve, navigate, trusted advisor, production-ready, production-grade, enterprise-grade, mission-critical, cross-functional, proven track record, results-driven, detail-oriented, game-changing, transformative, pivotal, meticulous, testament, tapestry, thrive in ambiguity, "stakeholders alike", "communicate fluently".

Consistency: clear referents ("it", "them", "those"), summary in present tense and past roles in past tense (the current role may use present tense for ongoing work, but pick one and keep it), one number style, one spelling system throughout. The one exception: a hard term keeps the posting's spelling ("modeling" in an American posting) because ATS searches are literal.

## 4. Summary

- Two to four sentences, about 40 to 90 words. It opens with the candidate's real title or function, then what they do and for whom. If the real function matches the job's core title, say it plainly ("Data analyst with five years in retail pricing"); never adopt the posting's exact title with its team or level qualifiers.
- It may name the one or two products or methods the job centres on, if the candidate really uses them.
- No tool lists, no objective or "Target:" line, no "seeking a role at", no restating the internships listed below it.
- When the page has room (step 7), the summary may gain one sentence that ties real experience to the job's central asks. It must add something the bullets don't say (scope, domain, the kind of customers or team); a sentence that replays a bullet reads as padding.
- Students and new graduates may skip the summary when the page is full without it.

## 5. Skills

- Three to six lines with plain category labels that fit the candidate's field ("Languages", "Data and BI", "Cloud", "Design tools", "Clinical systems", "CRM and sales tools").
- Tools, languages, platforms, frameworks, methods with proper names, certifications. Practices and soft skills ("stakeholder management", "attention to detail") belong in bullets, if anywhere.
- Choose by relevance to this job, the claimable hard terms first, and leave out true skills the role does not care about. Name each tool once.
- List only what the candidate could discuss for five minutes, preferring items a bullet shows in use. A term that only sits in Skills is weak evidence (graded "weak") and a common interview trap.
- No lines that restate bullets, no labels lifted from the posting, no posting adjectives glued onto product names ("serverless Cloud Run").
- Aim for each line to fit on one printed line.

## 6. ATS alignment without stuffing

What actually helps an ATS, all of it honest:

- **Exact spelling of hard terms.** ATS keyword search is mostly literal: "Kubernetes" does not match "K8s", "PostgreSQL" may not match "Postgres". Use the posting's spelling for every hard term the candidate truly has. Spell out an acronym once ("search engine optimisation (SEO)") only when the posting uses one form and the field commonly uses the other.
- **Terms in context.** A hard term inside a bullet that shows it in use counts for the ATS and convinces the recruiter. The same term in Skills too is fine.
- **Standard section headers:** Summary, Experience (or Work Experience), Skills, Education, Projects, Certifications. Creative headers ("Where I've Been") break parsers.
- **Readable dates:** "Mon YYYY – Mon YYYY" or "YYYY – YYYY", consistent throughout.
- **Contact details in the body text,** not in a Word header or footer, which many ATS skip.
- **No tables, columns, text boxes, icons or images** carrying content.
- **The job's core title** appears on the page only if it is the candidate's real title or function.

What never goes in: hidden or white text, keyword blocks, terms the candidate does not have, the posting's sentences. Recruiters read the page the ATS ranked, and stuffing shows.

## 7. Location, company name, title

- **Location:** keep what the base résumé shows (usually city and country in the contact line), unless the conventions file says to hide or change it. When the job is in another city or country and the user confirmed they would move, the summary carries one short sentence ("Open to relocating to Berlin."), adding "with visa sponsorship" only if they said they need it. Never invent a location or a work authorisation.
- **Target company name:** never on the page, alone or possessive ("Acme's"), except inside the name of a product the candidate really used ("Google Analytics", "Salesforce Service Cloud"). A résumé addressed to one employer reads as a mass-tailored template.
- **Job titles** on past roles are the titles the candidate actually held. A clarifying word in brackets is fine when the real title is opaque ("Member of Technical Staff (backend)") if the candidate agrees.

## 8. Layout basics

- One page; two only for 10+ years of relevant experience when the base résumé is already two pages, or when the user asks.
- Body text 10 to 11.5 pt, margins 0.5 to 0.8 inch.
- Section order: Summary, Experience, Skills, Education for experienced candidates; Education first for students and new graduates (`harvard-template.md`).
- Fill the page with relevant truth (SKILL.md step 7). Cut irrelevant content before shrinking anything.
