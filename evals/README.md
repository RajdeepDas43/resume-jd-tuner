# Evals

End-to-end test cases for the skill. Every candidate, employer and posting here is fictional, except the live job link in eval 1, which will close one day: swap in any open data scientist or data analyst posting on Greenhouse or Lever.

| Eval | Input | What it checks |
|---|---|---|
| 1. `data-scientist-from-link` | A live job link, a résumé PDF and a notes file | Fetching (or the fallback), eligibility rules in the report, using notes to fill the page, fixing a PDF whose bullets come out as garbage characters |
| 2. `marketing-pasted-docx` | A pasted posting and a DOCX with contact details only in the Word header | DOCX warnings, contact details moved into the body, British spelling, A4 paper, no relocation line without the candidate's say-so, honest gaps |
| 3. `ml-engineer-latex` | A LaTeX résumé and a pasted posting | Keeping the user's template, the ATS-safety lines (glued words, bitmap bullets), no claims of tools the candidate hasn't used |
| 4. `linkedin-link-fails` | A LinkedIn job link and a résumé | The fetch fails; the skill stops, invents nothing and asks for the pasted posting |

`files/` holds the inputs. To run an eval, ask Claude Code (with the skill installed) to carry out the prompt from `evals.json`, using the files above and saving to a scratch folder outside this repository. Then check the output against `expected_output`, and make sure every check in the skill's step 7 passes on the PDF.
