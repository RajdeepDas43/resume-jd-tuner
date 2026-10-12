# Contributing

Thanks for helping. Bug reports, fixes and new test cases are all welcome.

## Ground rules

The skill's four rules apply to changes too. A change that makes the résumé less honest, adds keyword stuffing or makes the writing sound more machine-made won't be merged, even if it raises a score.

## Set up

With Python 3.10 or later:

```bash
python3 -m pip install -r requirements.txt -r requirements-dev.txt
pytest -q
ruff check .
```

The skill itself also runs on Python 3.9, and CI tests that. To run the tests on 3.9, install `ci/python3.9/requirements-dev.txt` in place of `requirements-dev.txt`.

Optional: `poppler-utils` (for `pdftotext`) and a LaTeX engine let the full test suite run; tests that need them are skipped otherwise. Set `RJT_REQUIRE_TOOLS=1` to make those tests fail instead of skipping, as CI does on Linux.

## What CI checks

Every push to `main` and every pull request runs [`.github/workflows/ci.yml`](.github/workflows/ci.yml). It also runs once a week, so a new release of a dependency that breaks something shows up even when nothing here changed.

- **Lint:** ruff on the Python code, actionlint and zizmor on the workflow files, and a schema check of `.github/dependabot.yml`.
- **Tests:** the full suite on Linux with Python 3.9, 3.13, 3.14 and 3.15, with poppler and LaTeX installed; on Linux with the oldest dependency versions in `requirements.txt`; on macOS with poppler; and on Windows with neither tool, which also tests the fallbacks.
- **Plugin:** Claude Code's validator on `plugin.json`, `marketplace.json` and the skill, in strict mode. The CLI version is pinned in `tools/claude-code/package-lock.json`.
- **Package:** builds the upload zip, checks its layout and keeps it as a build artifact.

A pull request can be merged when the `CI passed` check is green. Dependabot opens weekly pull requests for the pinned tools and actions; merge them when CI passes.

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

1. Set the new version in `.claude-plugin/plugin.json` and in the `metadata` of `SKILL.md`, and add a `## X.Y.Z (date)` entry at the top of `CHANGELOG.md`. `python3 tools/release.py check` confirms they agree.
2. Merge to `main` and wait for CI to pass.
3. Tag the commit and push the tag: `git tag vX.Y.Z && git push origin vX.Y.Z`.

The tag starts [`.github/workflows/release.yml`](.github/workflows/release.yml). It runs the whole of CI on the tagged commit, checks that the tag matches the version in all three places, builds the zip, and publishes a GitHub release with the zip attached and the changelog entry as its notes. If any step fails, nothing is published; fix the problem, move the tag and push it again. To rehearse a release without publishing, run the Release workflow by hand from the Actions tab.
