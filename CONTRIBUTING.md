# Contributing

Thanks for helping. Bug reports, fixes and new test cases are all welcome.

## Ground rules

The skill's four rules apply to changes too. A change that makes the résumé less honest, adds keyword stuffing or makes the writing sound more machine-made won't be merged, even if it raises a score.

## Set up

```bash
python3 -m pip install -r requirements.txt pytest pyyaml jsonschema ruff
pytest -q
ruff check .
```

Optional: `poppler-utils` (for `pdftotext`) and a LaTeX engine let the full test suite run; tests that need them are skipped otherwise.

## Changing a script

- Keep scripts standard-library Python plus `reportlab`, `pypdf` and `pdfminer.six`. No network calls.
- Every script needs `--help`, clear error messages, and a `--json` output where other scripts read its result.
- Add or update a test in `tests/` for the behaviour you change. Fixtures must be fictional.

## Changing SKILL.md or a reference

- Explain the reason behind an instruction, not just the instruction. The model follows reasons better than rules.
- Keep `SKILL.md` under 500 lines; detail belongs in `references/`.
- Write in plain English. The repository holds itself to the same no-slop standard as the résumés it writes.
- Run the end-to-end evals before and after, and compare.

## Running the evals

`evals/evals.json` holds the test prompts; `evals/files/` holds the fictional résumés and postings. In Claude Code, ask Claude to run each prompt with the skill and save the outputs to a scratch folder outside the repository. Then check them against the expectations in `evals.json`. The skill-creator skill can do this and also show the results side by side with a previous version.

Eval 1 uses a live job link that will close one day. Swap in any open data scientist or data analyst posting on Greenhouse or Lever; its expectations don't depend on the specific job. Eval 4 should end with no résumé and a request for the pasted posting.

## Releasing

1. Update the version in `.claude-plugin/plugin.json` and in the `metadata` of `SKILL.md`, and add a `CHANGELOG.md` entry.
2. Run `python3 tools/build_zip.py` and attach `dist/resume-jd-tuner.zip` to the GitHub release.
