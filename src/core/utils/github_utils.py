#!/usr/bin/env python3
"""
GitHub Utilities - SSOT for GitHub Operations
=============================================

⚠️  PARTIALLY DEPRECATED: Core utilities still used, but extended functionality
   available through GitHub Professional MCP Server for comprehensive operations.

Provides standardized GitHub API operations and token management.
Consolidates duplicate GitHub code across tools.

<!-- SSOT Domain: core -->
<!-- PARTIALLY DEPRECATED: Use github-professional MCP server for advanced operations -->

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-04
Updated: 2025-12-28 (GitHub Professional MCP Server available)
V2 Compliant: Yes (<300 lines)
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, Any

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

from src.core.config.timeout_constants import TimeoutConstants


TOKEN_ENV_KEYS = (
    "FG_PROFESSIONAL_DEVELOPMENT_ACCOUNT_GITHUB_TOKEN",
    "GITHUB_TOKEN",
    "GH_TOKEN",
)


def _find_project_root(start: Path) -> Path:
    """
    Heuristic project root detection.
    Prefers locating .env, then .git, then common project markers.
    """
    for parent in start.parents:
        if (parent / ".env").exists():
            return parent
    for parent in start.parents:
        if (parent / ".git").exists():
            return parent
        if (parent / "pyproject.toml").exists():
            return parent
        if (parent / "requirements.txt").exists():
            return parent
    # Fallback to the top-most parent we can reasonably reach
    return start.parents[-1] if start.parents else start


def _parse_env_line(line: str) -> tuple[Optional[str], Optional[str]]:
    """
    Parse a single .env style line safely.
    Supports:
      - KEY=VALUE
      - export KEY=VALUE
      - whitespace around '='
      - quoted values
      - ignores comments
    """
    raw = line.strip()
    if not raw or raw.startswith("#"):
        return None, None

    if raw.startswith("export "):
        raw = raw[len("export "):].strip()

    # Remove inline comments (simple heuristic)
    if " #" in raw:
        raw = raw.split(" #", 1)[0].strip()

    if "=" not in raw:
        return None, None

    key, value = raw.split("=", 1)
    key = key.strip()
    value = value.strip().strip('"').strip("'")
    if not key:
        return None, None
    return key, value


def get_github_token(project_root: Optional[Path] = None) -> Optional[str]:
    """
    Get GitHub token from environment or .env file.

    SSOT for GitHub token extraction - consolidates duplicate code from:
    - tools/repo_safe_merge.py
    - tools/git_based_merge_primary.py
    - tools/repo_safe_merge_v2.py

    Args:
        project_root: Optional project root path (defaults to detected root)

    Returns:
        GitHub token if found, None otherwise
    """
    # 1) Check environment variables first
    for key in TOKEN_ENV_KEYS:
        token = os.getenv(key)
        if token:
            return token

    # 2) Determine root
    if project_root is None:
        current = Path(__file__).resolve()
        project_root = _find_project_root(current)

    # 3) Check .env
    env_file = project_root / ".env"
    if env_file.exists():
        try:
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    key, value = _parse_env_line(line)
                    if key in TOKEN_ENV_KEYS and value:
                        return value
        except Exception:
            # Soft-fail by design for SSOT utility
            pass

    return None


def create_github_pr_headers(token: str) -> dict[str, str]:
    """
    Create standard GitHub API headers for PR operations.

    SSOT for GitHub API headers - consolidates duplicate code from:
    - tools/create_batch2_prs.py
    - tools/create_merge1_pr.py
    - tools/merge_prs_via_api.py

    Args:
        token: GitHub token

    Returns:
        Headers dictionary
    """
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
    }


def create_github_pr_url(owner: str, repo: str) -> str:
    """
    Create GitHub PR API URL.

    Args:
        owner: Repository owner
        repo: Repository name

    Returns:
        GitHub API URL for PRs
    """
    return f"https://api.github.com/repos/{owner}/{repo}/pulls"


def create_pr_data(title: str, body: str, head: str, base: str) -> dict[str, str]:
    """
    Create PR data payload.

    Args:
        title: PR title
        body: PR body
        head: Head branch name
        base: Base branch name

    Returns:
        PR data dictionary
    """
    return {
        "title": title,
        "body": body,
        "head": head,
        "base": base,
    }


def check_existing_pr(
    owner: str,
    repo: str,
    head: str,
    token: str,
    head_owner: Optional[str] = None,
    timeout: int = TimeoutConstants.HTTP_DEFAULT,
) -> Optional[dict[str, Any]]:
    """
    Check if PR already exists for given head branch.

    SSOT for PR existence checking - consolidates duplicate code from:
    - tools/create_batch2_prs.py
    - tools/create_merge1_pr.py
    - tools/merge_prs_via_api.py

    Args:
        owner: Repository owner
        repo: Repository name
        head: Head branch name
        token: GitHub token
        head_owner: Optional owner namespace for head (fork support)
        timeout: Request timeout (seconds)

    Returns:
        PR data if exists, None otherwise
    """
    if not REQUESTS_AVAILABLE:
        return None

    url = create_github_pr_url(owner, repo)
    headers = create_github_pr_headers(token)
    namespace = head_owner or owner

    try:
        response = requests.get(
            url,
            headers=headers,
            params={"head": f"{namespace}:{head}", "state": "open"},
            timeout=timeout,
        )
        if response.status_code == 200:
            prs = response.json()
            return prs[0] if prs else None
    except Exception:
        pass

    return None


def _print_token_info() -> None:
    """
    Minimal self-test for CLI usage.

    Prints whether a token is detected and its length without making any
    network calls to avoid consuming API rate limits.
    """
    token = get_github_token()
    print("token_detected", bool(token))
    print("token_length", len(token) if token else 0)


if __name__ == "__main__":
    _print_token_info()


__all__ = [
    "get_github_token",
    "create_github_pr_headers",
    "create_github_pr_url",
    "create_pr_data",
    "check_existing_pr",
    "REQUESTS_AVAILABLE",
]
