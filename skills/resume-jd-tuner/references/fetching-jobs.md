# Getting the job posting from a link

Read this in step 1 when the user gives a link. The goal is the full posting text: title, about the role, responsibilities, requirements and preferred qualifications. Fetch the link; if that fails and the link is on Greenhouse, Lever, Ashby or Workday, make one retry through the board's public API (table below). If you still don't have it, ask the user to paste it. A posting rebuilt from memory, a search snippet or the company's website is not the posting.

## Get the words, not a summary

The checks compare the résumé with the posting's exact words, so the closer you get to the original text, the better.

- A tool that returns the raw page or the API's JSON gives the exact text. Convert HTML with `extract_text.py`.
- Some fetch tools pass the page through a model and return an answer about it (Claude Code's WebFetch works this way), and some decline to quote long pages. Ask for the posting section by section, keeping every requirement line and every named tool, product and certification exactly as written. Check the result: an ellipsis, "etc.", "and more" or a suspiciously short requirements list means it was condensed.
- A faithful section-by-section paraphrase that keeps every requirement and every named term is usable. Save it, mark `job_posting.txt` as "paraphrased by the fetch tool", say so in the report, and tell the user that pasting the exact posting would make the keyword checks exact.
- If sections or requirements are missing, ask the user to paste the posting.

## Is this a real posting?

Accept fetched text only if all of these hold:

- it names one job title;
- it has responsibilities or requirements (or both), not just a company blurb;
- it is longer than about 150 words;
- it is not a login wall ("Sign in to view"), a JavaScript notice ("Please enable JavaScript"), a cookie banner, a search-results page, an "apply" form with no description, or an error page;
- it is still open: "no longer accepting applications", "this job has expired" or a redirect to a job list means closed. Tell the user before doing any work; they may still want the résumé tuned, as practice or for a similar role.

If the page lists several jobs, ask which one, unless the URL clearly points to one.

## Job boards that often fail, and their public APIs

Many careers sites draw the posting with JavaScript, so a plain fetch returns an empty shell. The large applicant tracking systems publish the same posting through public, read-only job-board APIs meant for exactly this kind of reuse. Try the matching one once; other sites get no retry.

| URL looks like | Try | Text is in |
|---|---|---|
| `boards.greenhouse.io/<board>/jobs/<id>` or `job-boards.greenhouse.io/<board>/jobs/<id>` | `https://boards-api.greenhouse.io/v1/boards/<board>/jobs/<id>` | `title`, `content` (HTML, entity-escaped) |
| `jobs.lever.co/<site>/<id>` | `https://api.lever.co/v0/postings/<site>/<id>?mode=json` (EU accounts: `api.eu.lever.co`) | `text` (title), `descriptionPlain`, `lists[]` (requirements as HTML), `additionalPlain` |
| `jobs.ashbyhq.com/<org>/<id>` | `https://api.ashbyhq.com/posting-api/job-board/<org>` and pick the job whose `id` matches | `title`, `descriptionPlain` |
| `<tenant>.wd<N>.myworkdayjobs.com/<locale>/<site>/job/...` | `https://<tenant>.wd<N>.myworkdayjobs.com/wday/cxs/<tenant>/<site>/job/...` (drop the locale; needs an `Accept: application/json` header, so it may not work with every fetch tool) | `jobPostingInfo.jobDescription` (HTML) |
| A company careers page with `?gh_jid=<id>` | The Greenhouse API above, if you can find the board name on the page | as above |

If the response is HTML, save it and convert it: `python3 <skill>/scripts/extract_text.py page.html -o work/posting_raw.txt`.

Sites that need a login or block automated access, such as LinkedIn, Indeed and Glassdoor: no retry, and don't try to get around the block. Ask the user to paste the posting, or to open it and copy the "About the job" section. A browser tool the user can see and is signed in to is fine in an interactive session; in an unattended run, just ask.

Eligibility rules (work authorisation, sponsorship, "must be based in" a region, clearances) sometimes sit in the application form rather than the description. If the page shows application questions, read them too.

## What to ask for when it fails

Keep it to one line, for example:

> I couldn't open that link (it needs a sign-in). Could you paste the full job posting here: the title, the responsibilities and the requirements?

## Saving it

- `job_posting.txt`: first line `Source: <URL> (fetched <date>)` or `Source: pasted by the user (<date>)`, then the posting exactly as received.
- `work/jd.txt`: the scoring copy described in SKILL.md step 1: line 1 the posted title only, then the description, responsibilities and requirements, with salary, benefits, EEO and legal text and page chrome removed. Keep the "about the company" lines; they help the summary say the right thing.
