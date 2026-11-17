"""Read-only CLI for basic GitHub Pull Request metadata analysis."""

import json
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API = "https://api.github.com/repos"


def fetch_json(path):
    request = Request(
        f"{API}/{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "github-pr-analyzer-mvp",
        },
    )
    with urlopen(request, timeout=12) as response:
        return json.load(response)


def analyze(pr, files):
    warnings = []
    if not (pr.get("body") or "").strip():
        warnings.append("Missing PR description")
    if pr.get("draft"):
        warnings.append("PR is still a draft")
    if pr.get("changed_files", len(files)) > 10:
        warnings.append("Large PR: consider reviewing smaller changes")
    return warnings


def main():
    if len(sys.argv) != 4 or not sys.argv[3].isdigit():
        print("Usage: python main.py OWNER REPOSITORY PR_NUMBER")
        return 2

    owner, repo, number = sys.argv[1:]
    path = f"{owner}/{repo}/pulls/{number}"
    try:
        pr = fetch_json(path)
        files = fetch_json(f"{path}/files?per_page=100")
    except HTTPError as error:
        print(f"GitHub API error: HTTP {error.code} (check repository, PR or rate limit)")
        return 1
    except (URLError, TimeoutError, ValueError) as error:
        print(f"Could not fetch GitHub data: {error}")
        return 1

    status = "merged" if pr.get("merged_at") else pr.get("state", "unknown")
    print(f"\nPR #{number}: {pr.get('title', '(untitled)')}")
    print(f"Status: {status} | Changed files: {pr.get('changed_files', len(files))}")
    print(f"URL: {pr.get('html_url', '(unavailable)')}\n")
    print("Files (first 100):")
    for file in files:
        print(f"  - {file['filename']} ({file['status']}; +{file['additions']}/-{file['deletions']})")
    warnings = analyze(pr, files)
    print("\nBasic checks:")
    if warnings:
        for warning in warnings:
            print(f"  [!] {warning}")
    else:
        print("  No warnings from the current simple rules.")
    print("\nNote: this is not AI analysis or a comprehensive code review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
