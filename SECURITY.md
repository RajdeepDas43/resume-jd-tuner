# Security policy

## Reporting a vulnerability

Please report security problems privately: open this repository's **Security** tab and choose **Report a vulnerability**. Don't open a public issue for them.

If the problem is confirmed, the fix ships in a patch release with a security advisory, which credits you unless you'd rather stay anonymous.

## Supported versions

Fixes go into the latest release only.

## Scope

The skill's scripts run on your machine. They read the résumé and job posting you give them and write files next to them. They make no network requests: the agent's own web tool fetches job links. The only programs they start are `pdftotext` and `pdffonts` from poppler, when installed.

In scope:

- The scripts in `skills/resume-jd-tuner/scripts/`, for example unsafe handling of a crafted PDF, DOCX, LaTeX or HTML file.
- The GitHub Actions workflows and the release process, for example a way to change what a release contains.
