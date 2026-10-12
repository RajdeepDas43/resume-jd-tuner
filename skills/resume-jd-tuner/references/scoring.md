# How the numbers work

`scripts/scoreboard.py` computes every number in the fit report. This file explains the formulas so you can explain them to the user, and says what each number does not mean.

## Overall fit (0-100)

Each ask in `work/jd_asks.json` gets a grade from the hiring-manager agent (step 9), which grades the base and the tuned résumé in the same pass without being told which is which:

| Grade | Value | Meaning |
|---|---|---|
| clear | 1 | A line on the page proves it |
| weak | 0.5 | Hinted at, only listed in Skills, or shown at a smaller scope |
| none | 0 | Not shown |

Weights: must-have 3, responsibility 2, nice-to-have 1.

fit = 100 × Σ(weight × value) / Σ(weight)

| Score | Band |
|---|---|
| 85-100 | Strong |
| 70-84 | Good |
| 55-69 | Fair |
| below 55 | Long shot |

Caps: one must-have graded "none" caps the band at Good, two or more cap it at Fair, whatever the score. Recruiters filter on must-haves first, and the band should say so.

What it means: how clearly this page proves what this posting asks for. What it does not mean: the probability of an interview. Referrals, timing, location and the applicant pool matter as much, and none of them is on the page.

Tuning raises the score by making true evidence visible. It cannot raise it past what the candidate has done: honest gaps stay at "none".

## ATS alignment (0-100) and the honest ceiling

From `scripts/coverage.py`, over the hard terms in `work/jd_asks.json`:

ATS alignment = 100 × (2 × must-have terms present + nice-to-have terms present) / (2 × all must-have terms + all nice-to-have terms)

A term counts as present only in the posting's own spelling, as a whole word, anywhere in the PDF's text layer. That is how most ATS keyword searches behave: literal, case-insensitive matching on the parsed text. A term with `alternatives` ("PyTorch or TensorFlow") counts once and is met by any of them.

The **honest ceiling** is the same formula counting only the terms the candidate can truthfully claim. The tuned résumé should reach it. When it falls short, the report says which claimable terms are missing and why. A score above the ceiling means a term marked not claimable is on the page, which must be confirmed with the user or removed.

What it does not mean: the score a particular ATS (Workday, Greenhouse, Lever, iCIMS, Taleo and others) computes. Those systems differ, many only parse and let recruiters search, and some rank with their own models. This number estimates how many of the posting's exact terms a keyword search would find on the page, which is the part a résumé controls.

## Keyword overlap (secondary)

From `scripts/relevance_score.py`: the weighted share of the posting's 60 heaviest one- to three-word terms found in the résumé (title terms ×4, requirement-section terms ×3, other terms ×2, nice-to-have terms ×1). It is deterministic and useful for choosing between several base résumés.

It rewards echoing the posting's prose, so a stuffed résumé beats an honest one. There is no target. Report it, and explain that difference if the user asks why it is not higher.

## Interview risk

From the hiring manager's risks list:

- **High** if any claim on the page is rated high risk (the candidate would struggle to back it up),
- **Medium** if any is medium,
- **Low** otherwise.

A high-risk claim should normally be softened or cut before delivery (step 9). If one stays because the candidate can defend it, the report says how to prepare.

## Page fill

From `scripts/pdf_checks.py`: the free space between the lowest line of text and the bottom margin (taken to equal the top margin), divided by the body line spacing. FULL means at most one free line; UNDERFILLED means two or more; OVERFLOW means more pages than allowed. A footer far below the content (a page number, a closing line) is measured separately, so it does not hide empty space.
