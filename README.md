# GitHub PR Analyzer — MVP 0.1

Small, read-only Python CLI for analyzing **public GitHub Pull Requests**.

## Purpose

Started as a response to real coordination and review friction in a collaborative C terminal project. The long-term idea is to support developers by collecting evidence and identifying review priorities. Version 0.1 is intentionally small and does **not** use artificial intelligence.

## Current functionality

- Retrieves Pull Request metadata via the GitHub REST API.
- Lists the first 100 changed files and their change counts.
- Flags missing descriptions, draft status, and PRs with more than 10 changed files as simple workflow warnings. These rules do **not** detect code defects.
- Does not modify repositories, merge Pull Requests, execute code, or request secrets.

## How to run

Requires Python 3.10+; no third-party packages or API key are necessary for public Pull Requests.

```bash
python main.py marcoamllongo terminal-c-PI2 3
```

On Windows, `py main.py marcoamllongo terminal-c-PI2 3` also works when the Python launcher is installed.

For offline unit tests:

```bash
python -m unittest discover -s tests -v
```

## Limitations

- Only public repositories, unauthenticated requests; GitHub's anonymous API rate limit applies.
- Retrieves only the first 100 changed files for each PR.
- Basic warnings are examples of workflow checks, not reliable code-quality judgments.
- Live GitHub API functionality should be tested locally; included unit tests cover rule logic only.

## Planned improvements (not implemented)

- Structured JSON reports and better handling of pagination.
- Checks for commit/status information and improved validations.
- Optional LLM-assisted analysis with citations to PR evidence and human approval.
- Repeatable evaluation cases, logging, CI and container packaging when useful.

## Security

Read-only by design. Treat all PR descriptions, comments and diffs as untrusted input, especially before introducing an LLM. Do not store tokens in source code.
