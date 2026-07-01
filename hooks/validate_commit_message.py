#!/usr/bin/env python3
"""Validate commit messages for local hooks and CI."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass


MESSAGE_PATTERN = re.compile(r"^#(?P<issue>\d+)\s*-\s+(?P<message>\S.*)$")


@dataclass(frozen=True)
class ValidationResult:
    issue_number: int
    message: str


def first_non_empty_line(text: str) -> str:
    for line in text.splitlines():
        candidate = line.strip()
        if candidate:
            return candidate
    return ""


def parse_commit_subject(subject: str) -> ValidationResult:
    match = MESSAGE_PATTERN.match(subject)
    if not match:
        raise ValueError("Commit messages must follow the format '#NUM_ISSUE - MESSAGE'.")

    return ValidationResult(
        issue_number=int(match.group("issue")),
        message=match.group("message").strip(),
    )


def resolve_repo_slug(repo_slug: str | None = None) -> str:
    if repo_slug:
        return repo_slug

    env_repo = os.environ.get("GITHUB_REPOSITORY")
    if env_repo:
        return env_repo

    try:
        remote = subprocess.check_output(
            ["git", "remote", "get-url", "origin"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ValueError("Could not determine the Git remote repository.") from exc

    match = re.search(r"github\.com[:/](?P<owner>[^/]+)/(?P<repo>[^/.]+)(?:\.git)?$", remote)
    if not match:
        raise ValueError("Could not extract owner/repo from the Git origin URL.")

    return f"{match.group('owner')}/{match.group('repo')}"


def github_request(url: str, token: str | None) -> object:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "sistema-bancario-commit-validator",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        raise RuntimeError(f"GitHub API request failed ({exc.code}).") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error while contacting GitHub API: {exc.reason}.") from exc


def issue_exists(repo_slug: str, issue_number: int, token: str | None) -> bool:
    url = f"https://api.github.com/repos/{repo_slug}/issues/{issue_number}"
    payload = github_request(url, token)
    if not payload:
        return False

    return "pull_request" not in payload


def validate_subject(subject: str, repo_slug: str, token: str | None) -> ValidationResult:
    parsed = parse_commit_subject(subject)
    if not issue_exists(repo_slug, parsed.issue_number, token):
        raise ValueError(f"Issue #{parsed.issue_number} does not exist in the GitHub repository.")
    return parsed


def validate_commit_message(message: str, repo_slug: str, token: str | None) -> ValidationResult:
    return validate_subject(first_non_empty_line(message), repo_slug, token)


def fetch_pull_request_commits(repo_slug: str, pr_number: int, token: str | None) -> list[str]:
    commits: list[str] = []
    page = 1

    while True:
        url = (
            f"https://api.github.com/repos/{repo_slug}/pulls/{pr_number}/commits"
            f"?per_page=100&page={page}"
        )
        payload = github_request(url, token)
        if payload is None:
            raise ValueError(f"Pull request #{pr_number} was not found.")
        if not isinstance(payload, list):
            raise RuntimeError("Unexpected response while fetching pull request commits.")

        if not payload:
            break

        for item in payload:
            message = item.get("commit", {}).get("message", "")
            if message:
                commits.append(message)

        if len(payload) < 100:
            break

        page += 1

    return commits


def validate_pull_request(repo_slug: str, pr_number: int, token: str | None) -> None:
    commits = fetch_pull_request_commits(repo_slug, pr_number, token)
    if not commits:
        raise ValueError(f"Pull request #{pr_number} does not contain commits to validate.")

    errors: list[str] = []
    for index, commit_message in enumerate(commits, start=1):
        subject = first_non_empty_line(commit_message)
        try:
            validate_subject(subject, repo_slug, token)
        except ValueError as exc:
            errors.append(f"Commit {index}: {exc}")

    if errors:
        raise ValueError("Invalid commit messages:\n" + "\n".join(f"- {error}" for error in errors))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", help="GitHub owner/repo.")
    parser.add_argument("--token", help="Token for the GitHub API.")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--message-file", help="File containing the commit message.")
    group.add_argument("--message", help="Commit message text.")
    group.add_argument("--pr-number", type=int, help="Pull request number.")

    args = parser.parse_args(argv)
    repo_slug = resolve_repo_slug(args.repo)
    token = args.token or os.environ.get("GITHUB_TOKEN")

    try:
        if args.message_file:
            validate_commit_message(read_text(args.message_file), repo_slug, token)
        elif args.message is not None:
            validate_commit_message(args.message, repo_slug, token)
        else:
            validate_pull_request(repo_slug, args.pr_number, token)
    except (ValueError, RuntimeError) as exc:
        print(exc, file=sys.stderr)
        return 1

    return 0


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


if __name__ == "__main__":
    raise SystemExit(main())
