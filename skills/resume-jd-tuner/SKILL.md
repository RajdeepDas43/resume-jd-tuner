---
name: resume-jd-tuner
description: Tailor a résumé to one job posting and report how well it fits. Takes a job link (or the pasted job text when the link will not load) and the user's résumé (PDF, DOCX, LaTeX or text). Returns a one-page tuned résumé PDF and a fit report covering ATS alignment, interview risk, gaps to close, a quality check and the overall fit before and after tuning. Every claim stays true and the page reads like a person wrote it; reviewer agents screen the draft for AI slop and errors, then recruiter agents verify it against the job before delivery. Use whenever someone shares a job posting, job link or JD with a résumé or CV, asks to tailor, tune, target, optimize or rewrite a résumé or CV for a role, wants an ATS or keyword match check, or asks whether they fit a job, even if they never say "résumé".
license: Apache-2.0
compatibility: Python 3.9+ with reportlab, pypdf and pdfminer.six (scripts/check_env.py checks). A web fetch tool for job links; pasted text works without one. Subagents are optional. LaTeX résumés need pdflatex, xelatex or lualatex.
metadata:
  version: "1.0.0"
  author: Rajdeep Das
  repository: https://github.com/RajdeepDas43/resume-jd-tuner
---

# Résumé ↔ JD Tuner

Turn the user's résumé into a one-page résumé for one specific job, and tell them honestly how well they fit it.

Two readers must accept the page. An ATS parses the PDF and matches the job's exact terms; then a recruiter or hiring manager skims the page for 30 seconds. The person is the one who rejects keyword stuffing and machine-sounding text, so the page has to make sense to a person first and carry the job's real keywords second.

**You need:** a job posting (a link, or pasted text) and the user's résumé.
**You deliver,** in one folder per application:

| File | What it is |
|---|---|
| `First_Last_Role.pdf` | The tuned résumé: one full page, clean text layer, clickable links. Plus the `.tex` when the user's résumé is LaTeX |
| `fit_report.md` | Overall fit, ATS alignment, interview risk, gaps to improve, quality check, what changed |
| `job_posting.txt` | The posting exactly as fetched or pasted |
| `work/` | Intermediate files: decoded asks, grades, check results, review log |

## Four rules that override everything else

1. **Never fabricate.** Reword, reorder, cut and quantify what the candidate actually did. Never invent an employer, title, date, degree, metric, tool or skill, and never upgrade one ("used" to "led", "familiar with" to "expert"). A résumé that lies gets the candidate rejected in the interview, which is the opposite of the goal. If the job needs something the candidate's sources don't show, report it as a gap.
2. **Tune, don't stuff.** Match the job by showing real work that answers its requirements, in the candidate's own plain words. The job's hard terms (tools, platforms, languages, certifications) appear in the posting's exact spelling wherever the candidate truly has them. The posting's sentences, adjectives, values and title never get copied in to raise a score.
3. **No AI slop.** The page should read as if a strong candidate wrote it about their own work: short sentences, plain verbs, concrete details, numbers they can explain. Recruiters increasingly recognise LLM polish, and it makes them doubt the content.
4. **Use the whole page.** A page that stops halfway reads as a thin profile and wastes room that could prove fit. Fill it with true, relevant detail in the experience and summary sections first (step 7). Layout changes come last, and the report says when they were needed.

## Setup and where files go

- Scripts live in this skill's `scripts/` folder. Call them by full path, written below as `<skill>/scripts/...` (the folder that holds this SKILL.md). Use `python3`, or `python` on Windows.
- Run `python3 <skill>/scripts/check_env.py` once. Install anything it reports missing (`python3 -m pip install reportlab pypdf pdfminer.six`). If a check cannot run, say which one was skipped in the report rather than pretending it passed.
- Create the application folder, `<company>-<role>/` (lowercase, hyphens), in the user's working folder or wherever they ask, with `work/` inside it. In a chat app without a working folder, use the session's output folder and attach the files at the end.
- If the folder already holds a build for this job, move the old PDF and report into `work/previous-<date>/` first, so nothing the user approved is lost.
- Keep every intermediate file, including any helper script you write, inside `work/`. Never use a shared temp folder: parallel runs overwrite each other there.
- A run is **unattended** when nobody can answer questions: you have no question tool and no reply comes, the run is scheduled or headless, or the user said not to ask. The steps below say what changes then.
- If the user keeps a conventions file (`resume-conventions.md` in their résumé folder; template in `assets/conventions_template.md`), read it first. Its fixed wordings, never-mention list, spelling and location choices win over the job, the template and older résumés.

## Workflow

Track these ten steps in your task list and finish each before starting the next.

### 1. Get the job posting

- **A link:** fetch it with your web fetch tool. Accept the result only if it reads like a job posting: a job title plus responsibilities or requirements, more than about 150 words. Login walls, "enable JavaScript" pages, cookie notices, search results and "no longer accepting applications" pages are failures. If the tool summarises pages, ask for the posting section by section with every requirement and every named tool kept exactly. `references/fetching-jobs.md` covers this, the job boards that often fail (LinkedIn, Workday, Greenhouse, Lever, Ashby) and the public alternatives worth one try.
- **If the link fails** (a login wall, a blocked or robots-disallowed fetch, an error, or text that isn't the posting): for a Greenhouse, Lever, Ashby or Workday link, make one retry through that board's public API (`references/fetching-jobs.md`); for any other site, don't retry. Then say so in one line and ask the user to paste the full posting (title, responsibilities, requirements). Check that the résumé is readable first, so one message asks for everything that's missing. Never reconstruct a posting from the company name or job title. Unattended: stop there and explain what is needed.
- **A closed posting** ("no longer accepting applications"): tell the user before doing any work, and go on only if they still want it. Unattended: stop and say so.
- **Pasted text:** use it as given.

Save the posting verbatim as `job_posting.txt`, with the source URL and today's date on the first line. Then write the scoring copy `work/jd.txt`: line 1 is the posted job title only (no company or location, which live in `jd_asks.json`), followed by the description, responsibilities and requirements. Strip salary bands, benefits, EEO and legal text, recruiter boilerplate and page chrome. No honest résumé can match those words, and leaving them in invites stuffing.

### 2. Decode the posting

Read it the way the recruiter will, and write `work/jd_asks.json` (schema `assets/jd_asks_schema.json`, example `assets/example_jd_asks.json`):

- **role:** title, the plain job noun a recruiter searches for (`title_core`, e.g. "data analyst"), company, seniority, location and work mode, plus any `eligibility` rules (work authorisation, "no sponsorship", "must live in Ontario", a clearance, a required language). Eligibility goes in the report, not on the résumé, unless the user's conventions say to state it.
- **asks:** every requirement and responsibility as a short phrase, usually 12 to 35 of them, typed `must` (required), `nice` (preferred) or `role` (responsibilities). For each, list `alts`: specific phrases a résumé would use when it shows the ask (two words or more, or a distinctive term), not the posting's wording. A generic alt like "review" matches "retention review" and hides a gap.
- **hard_terms:** the exact names an ATS keyword search would use (tools, languages, platforms, products, named methods, certifications, licences, degrees), spelled as the posting spells them, typed `must` or `nice`, with other spellings in `variants` ("K8s" for "Kubernetes"). When the posting offers a choice ("PyTorch or TensorFlow", "Snowflake, Redshift or BigQuery"), record one term with the others in `alternatives`: any one of them meets it, unless the posting also requires one of them on its own. Terms named only under responsibilities are `nice` unless the requirements name them too. Hard terms are proper names and established technical terms the posting uses ("A/B testing", "vector search"); ordinary words ("complex", "scalable") are not.
- **do_not_echo:** posting prose that must never reach the résumé: mission lines, adjectives ("robust", "world-class"), stock phrases ("fast-paced", "end-to-end ownership", "thrive in ambiguity").

### 3. Read the résumé and map the gaps

- **Find the base résumé:** a file attached in the conversation, then a path the user names, then a résumé folder in the working folder. If there are several versions, extract each one's text (next bullet) and score it with `python3 <skill>/scripts/relevance_score.py --jd work/jd.txt --resume <version>.txt` as a rough first filter. Read the top two or three, pick the one whose real work best answers the asks, and tell the user which and why. If there is no résumé at all, ask for one (a LinkedIn PDF export works). A résumé cannot be written from a posting alone.
- **Extract it:** `python3 <skill>/scripts/extract_text.py <résumé> -o work/base.txt`. It reads PDF, DOCX, LaTeX, HTML, Markdown and text, reports the paper size, and warns about problems an ATS will also hit (a scanned PDF with no text, contact details only in a Word header, text boxes). Mention those warnings in the report.
- **Collect every source of truth:** the base résumé, other versions describing the same jobs, notes or a brag document the user points to, the conventions file, and anything the user tells you in this conversation. Content from another version may be borrowed only when it describes the same real experience.
- **Map the gaps:** grade the base résumé against every ask as `clear` (a line proves it), `weak` (hinted at, only listed in Skills, or only partly shown) or `none`, and quote the evidence for each. Save it as `work/gap_map.json` (same format as `assets/grades_schema.json`). It is your working map for the rewrite and the page fill; the reported before-and-after scores come from the hiring manager in step 9.
- **Mark honest gaps in `work/jd_asks.json`:** set `"claimable": false` on each ask and hard term that nothing in the sources supports, and update these after the user's answers in step 4. An ask the sources support only in part (cost per install, but no ROAS) stays claimable; it can reach `weak`, and the report names the missing part.

### 4. Ask the user, in one batch

Before writing, send one batch of questions (use AskUserQuestion if you have it, otherwise one short message). Ask only what changes the résumé:

- Things the job centres on that the sources don't settle ("Have you used dbt in production, or only read about it?").
- Detail on the asks graded weak: one or two facts would turn each into clear evidence ("How large were the tables behind that SQL work?"). These answers are also what fills the page in step 7.
- Numbers you want to use but cannot explain (what the baseline was, how it was measured).
- Location, only when the job is in another city or country than the base résumé shows: are they open to relocating, and do they need visa sponsorship? Never assume either way.

Unanswered or unattended: claims that appear nowhere in the user's sources stay off the page (mark them not claimable); numbers and claims already in their own sources stay, flagged under "To confirm" when you couldn't check them. Add no relocation line, keep going, and list everything unconfirmed under "To confirm" in the report's gaps.

### 5. Write the tuned résumé

Read `references/writing-rules.md` before writing; it holds the full rules for bullets, numbers, the summary, skills and layout, with the reasons. The core of it:

- Lead with the candidate's strongest stories for this job. One idea per bullet, one to three short sentences, plain past-tense verbs, no em dashes, no semicolons. Use `references/xyz-format.md` as a checklist for what a bullet carries (what was done, at what scale or with what result, how), not as a sentence template.
- Name a method or tool more specifically than the sources do only when the name is accurate for what was done ("LightGBM ranker" may not be "learning-to-rank"). When unsure, keep the source's words and ask, or list it under "To confirm".
- **Highest honest ATS alignment:** every claimable hard term appears at least once in the posting's exact spelling (including American or British spelling, "modeling" or "modelling", for that term), ideally inside a bullet that shows it in use and again in Skills. When no natural sentence can carry a term, Skills alone is fine; never force a term into a bullet. Use standard section headers (Summary, Experience, Skills, Education). No terms the candidate does not have, no white-text tricks, no keyword lists in the summary.
- Never echo `do_not_echo` phrases or any four-word run from the posting except names of products, tools and certifications. Never order bullets in the posting's order, and never write one bullet per ask.
- The summary names the candidate's real title or function, what they do and for whom, in two to four sentences. No objective line, no "Target:" line, and no target company name anywhere on the page: a résumé addressed to one employer reads as a mass-tailored template.
- **Location:** keep what the base résumé shows, unless the conventions file says otherwise. Add a relocation sentence ("Open to relocating to London.") only when the job is elsewhere and the user confirmed it, with "with visa sponsorship" only if they said they need it.
- Spelling: the conventions file's choice, otherwise the base résumé's (British or American), used consistently.

### 6. Build the PDF

- **The user's résumé is LaTeX** (a `.tex` was given or sits in their folder): edit a copy of their file, change content only, keep their preamble, macros, font, font size, paper size and section order, and add the ATS-safety lines from `references/latex.md` if they are missing (they fix glued words, garbled ligatures and bitmap bullets without changing the look). Compile with the engine the template needs, twice. No TeX engine available: deliver the `.tex` with Overleaf instructions, or fall back to the default renderer if the user prefers.
- **Otherwise (default):** write `work/resume.json` (schema `assets/resume_schema.json`, example `assets/example_resume.json`) and render it: `python3 <skill>/scripts/render_resume_pdf.py work/resume.json -o <folder>/First_Last_Role.pdf`. Keep every layout choice in the JSON's `layout` block (`paper`, `dates`, `font_size`, `spacing`, `fill`, `pages`) rather than only on the command line, so every rebuild comes out the same. Paper: letter for jobs in the US and Canada, A4 everywhere else, because recruiters print on their local paper. The layout follows `references/harvard-template.md`. The renderer embeds a Unicode font and makes emails and profile URLs clickable.

On the LaTeX path the template's paper size and section order win over these defaults; if the template is Letter and the job is outside the US and Canada, mention A4 in the report as the user's call.

Name the file after the candidate and the role applied for, never the target company (`Priya_Shah_Data_Analyst.pdf`).

### 7. Check the PDF and fill the page

Run every check on the compiled PDF, because that is what the ATS receives:

```bash
python3 <skill>/scripts/extract_text.py <pdf> -o work/tuned.txt --dewrap work/tuned_review.txt
python3 <skill>/scripts/pdf_checks.py <pdf> --source work/resume.json --json work/pdf_checks.json \
    [--link <each real profile URL>] [--require "<each fixed line>"] [--forbid "<each never-mention term>"]
python3 <skill>/scripts/slop_scan.py work/tuned.txt work/jd.txt --json work/slop.json
python3 <skill>/scripts/coverage.py work/jd_asks.json work/tuned.txt --json work/coverage_after.json
```

(On the LaTeX path pass the `.tex` to `--source`. For a two-page résumé add `--pages 2` to pdf_checks and set `"pages": 2` in the layout block.) After any edit to the résumé, however small, re-render and re-run these checks: they must always describe the file you deliver. Fix every `FAIL` from pdf_checks (page count, garbled or glued text, missing headers, email, links, fixed lines), and read its warnings: dates that come out detached from their role in a reader are fixed with `--dates inline` on the default renderer. (On the LaTeX path the check can't map entries, so read `work/tuned.txt` around each role; if dates land away from their roles, note it in the report as a property of the template.) Fix every `FAIL` and `REVIEW` item from slop_scan, except product, tool and certification names, the candidate's fixed lines, and real technical terms ("end-to-end tests"). In coverage, act on `MISSING` (a claimable hard term left out: add it where it is true), `SPELL` (use the posting's spelling) and `CHECK` (a term marked not claimable is on the page: confirm it or remove it).

**Fill the page.** The last line of pdf_checks reads `FILL: FULL`, `FILL: UNDERFILLED` (two or more free lines at the bottom) or `FILL: OVERFLOW` (more than one page).

- **UNDERFILLED:** the free lines are room to prove more fit. Spend them on the asks that `work/gap_map.json` grades weak, or none but claimable, and that coverage.py still lists as not matched, in this order:
  1. **Experience:** a bullet, or a fuller existing bullet, about real work that proves one of those asks: material cut from the base résumé, other versions of it, or facts the user confirmed. Prefer the most recent role. The usual cap of about eight bullets for the main role can stretch when each extra bullet proves a different ask.
  2. **Summary:** one more sentence that adds something the bullets don't say (scope, domain, the kind of customers or team) and ties it to the job's central asks, up to four sentences and about 90 words in all. A sentence that replays a bullet will be cut in review.
  3. A relevant project, certification, award or course that carries the job's hard terms.
  4. True lines cut earlier that still say something relevant to this role.

  Each addition must pass every rule above; extra room is never a license to inflate. Re-render and re-check after each change. Stop when FILL says FULL, or when the next relevant line would spill onto a second page (then take that line back out). If a reviewer later cuts an addition, fill the gap with a different true item rather than re-adding it.

  **When true, relevant material runs out** with space left, and step 4 did not already cover it, ask the user two to four targeted questions about the weak asks ("What was the largest table your SQL ran on, and how long did it take?"). Their answers raise the fit and fill the page at the same time; this is the best use of the space. Only when no more material can come (the user has nothing to add, or nobody can answer), use layout: `"fill": true` in the layout block on the default renderer (it widens spacing, then the font up to 11 pt, and never touches the words), or the template's own spacing on the LaTeX path. Report the leftover space and the questions that would fill it.
- **OVERFLOW:** cut the least relevant content first (old roles' bullets, skills the job doesn't use, the weakest bullet), then tighten wording. Never shrink the font below 10 pt or the template's size, and never set margins under 0.5 inch.
- Two pages are acceptable only for 10+ years of relevant experience when the base résumé is already two pages, or when the user asks (`--pages 2`); the second page should then be at least half full.

### 8. Quality review agents: AI slop, language, facts

Have three independent reviewers critique the build before the user sees it. Briefs, inputs and reply formats are in `references/reviewers.md`:

1. **AI-slop screener**: a senior recruiter who spots LLM-written résumés.
2. **Copy editor**: plain English, grammar, referents, consistency.
3. **Fact-checker**: every claim and number against the full sources.

If you have a tool that starts a separate agent (in Claude Code, the Agent tool, formerly called Task; to-do list tools such as TaskCreate don't count), start all three in one message so they run in parallel and none of them sees your reasoning. If you cannot, run each brief yourself, one at a time, starting each from its brief and the materials only, and write its full verdict before starting the next. Don't go easy on the draft because you wrote it, and say in the report that the reviews were self-run.

Apply the feedback following the precedence and rules in `references/reviewers.md` (reviewers may only cut, reorder or reword; a new fact needs the user's confirmation). Rebuild, then re-run step 7.

### 9. Recruiter verification agents: does it fit the job?

With the quality fixes in, launch two fresh agents that have not seen any draft, in parallel (or play them in turn, as above):

4. **Recruiter screen**: the ATS searches they would run for this job, whether the page passes them, the 30-second impression, a shortlist decision and a reads-as-human score.
5. **Hiring manager**: grades two résumés against every ask, labelled A and B at random without saying which is which: the base résumé and the tuned one. One grader with one rubric makes the before and after scores comparable. For each it also flags overclaims and lists the interview questions the page will trigger, with a risk level for each. Map A and B back and save `work/grades_before.json` (base) and `work/grades_after.json` (tuned, with its risks).

Fix what they find that can be fixed honestly: a claimable must-have shown only weakly gets said more clearly; an overclaim gets softened or cut; a high-risk claim the candidate cannot defend comes off the page. If anything changed materially (a claim added, removed or reworded, or the order of the top bullets changed; polish to wording alone is not material), rebuild, re-run step 7, have the fact-checker check the changed lines, and re-run both the recruiter and the hiring manager (fresh agents). Two rounds at most. Anything changed after the last round, such as a line added to refill the page, still goes through step 7 and a fact-check of the changed lines before delivery.

**Pass bar:** reads-as-human score 8/10 or better, no open fact-check items, every step 7 check passing, the page FULL (or every true, relevant item already on it, with the leftover space and the questions that would fill it in the report), and every claimable must-have graded clear or its absence explained. If the bar cannot be met honestly, stop iterating and say why in the report; a weaker true page beats a stronger false one.

Record each round in `work/review_log.md`: reviewer, verdict, what was applied, what was not and why.

### 10. Score, report, deliver

Re-run the checks on the final PDF, then compute the numbers with the script, so they come from fixed formulas rather than estimates:

```bash
python3 <skill>/scripts/extract_text.py <pdf> -o work/tuned.txt
python3 <skill>/scripts/pdf_checks.py <pdf> --source work/resume.json --json work/pdf_checks.json
python3 <skill>/scripts/slop_scan.py work/tuned.txt work/jd.txt --json work/slop.json
python3 <skill>/scripts/scoreboard.py --asks work/jd_asks.json --before work/grades_before.json \
    --after work/grades_after.json --base-text work/base.txt --tuned-text work/tuned.txt \
    --jd work/jd.txt --checks work/pdf_checks.json --slop work/slop.json --json work/scoreboard.json
```

Write `fit_report.md` exactly as laid out in `references/fit-report-template.md`, and paste the scoreboard table in. The report covers, in this order: **Overall fit** (before and after, with a plain verdict), **ATS alignment**, **Interview risk**, **Gaps to improve**, **Quality check** and **What changed**. `references/scoring.md` explains what each number means and what it does not.

Then reply in the chat with five lines at most: the overall fit before and after, the two or three gaps that matter most, the riskiest interview question, and where the files are. The report holds the rest.

## When something goes wrong

| Problem | What to do |
|---|---|
| The job link won't load or returns a login page | For Greenhouse, Lever, Ashby or Workday links, one retry through the public API in `references/fetching-jobs.md`; for any other site, no retry. Then ask for the pasted text (unattended: stop) |
| The posting has closed | Tell the user before doing any work (unattended: stop) |
| No résumé anywhere | Ask for one; offer the LinkedIn "Save to PDF" export |
| Scanned résumé (no text layer) | Ask for a text-based PDF or DOCX; warn that ATS cannot read the scan either |
| The candidate is a weak fit | Tune honestly and say so plainly in the report's verdict, with what would close the gap |
| The page is still short after every true, relevant line | Ask about the weak asks; if nothing more can come, `--fill` (default renderer) or the template's spacing, and report the leftover |
| No subagents | Run the five briefs yourself, one at a time (steps 8 and 9), and say so in the report |
| reportlab or pdfminer.six missing and cannot be installed | Write the résumé text, explain the missing package, and skip only the checks that need it, saying so |
| No TeX engine on the LaTeX path | Deliver the `.tex` for Overleaf, or render with the default renderer if the user agrees |
| The user asks for keyword stuffing, invented experience or a fake title | Decline that part and explain why it backfires at the interview; keep tuning honestly |

## Scripts

| Script | What it does |
|---|---|
| `check_env.py` | Lists the tools available and how to install what's missing |
| `extract_text.py` | Text from PDF, DOCX, LaTeX, HTML, Markdown or text; flags scanned PDFs, header-only contact details and reader disagreement; `--dewrap` gives one line per bullet for reviewers |
| `render_resume_pdf.py` | Résumé JSON to a Harvard-style PDF with an embedded Unicode font and clickable links; prints the FILL status. `--dates inline` for parser-proof dates, `--fill` as the last-resort layout fill |
| `pdf_checks.py` | Page count, page fill (free lines at the bottom), garbled or glued text, dates detached from their role, headers, contact, links, required and forbidden text |
| `slop_scan.py` | AI-slop suspects in the prose: dashes, semicolons, long sentences, banned words, "-ing" tails, weak or repeated openers, phrases shared with the posting |
| `coverage.py` | Hard-term coverage in the posting's spelling (ATS alignment and honest ceiling) and ask coverage by phrase |
| `relevance_score.py` | Keyword overlap score; a secondary signal for picking a base résumé, never a target |
| `scoreboard.py` | The report's numbers: fit before and after, ATS alignment, interview risk, quality verdicts |

Every script above prints `--help`, uses only the standard library plus the three packages above, and makes no network calls. `resume_text.py` is the shared helper module they import.
