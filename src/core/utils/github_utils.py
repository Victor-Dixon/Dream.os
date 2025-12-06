#!/usr/bin/env python3
"""
GitHub Utilities - SSOT for GitHub Operations
=============================================

Provides standardized GitHub API operations and token management.
Consolidates duplicate GitHub code across tools.

<!-- SSOT Domain: core -->

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-04
V2 Compliant: Yes (<300 lines)
"""

import os
from pathlib import Path
from typing import Optional, Any

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


def get_github_token(project_root: Optional[Path] = None) -> Optional[str]:
    """
    Get GitHub token from environment or .env file.
    
    SSOT for GitHub token extraction - consolidates duplicate code from:
    - tools/repo_safe_merge.py
    - tools/git_based_merge_primary.py
    - tools/repo_safe_merge_v2.py
    
    Args:
        project_root: Optional project root path (defaults to repo root)
        
    Returns:
        GitHub token if found, None otherwise
    """
    # Check environment variables first
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if token:
        return token
    
    # Check .env file
    if project_root is None:
        # Find project root (directory containing .env)
        # Start from this file and go up to find .env
        current = Path(__file__)
        for parent in current.parents:
            if (parent / ".env").exists():
                project_root = parent
                break
        else:
            # Fallback: assume repo root is 4 levels up from core/utils
            project_root = current.parent.parent.parent.parent
    
    env_file = project_root / ".env"
    if env_file.exists():
        try:
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if line.startswith("GITHUB_TOKEN=") or line.startswith("GH_TOKEN="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
        except Exception:
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
    timeout: int = 30,
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
        timeout: Request timeout (seconds)
        
    Returns:
        PR data if exists, None otherwise
    """
    if not REQUESTS_AVAILABLE:
        return None
    
    url = create_github_pr_url(owner, repo)
    headers = create_github_pr_headers(token)
    
    try:
        response = requests.get(
            url,
            headers=headers,
            params={"head": f"{owner}:{head}", "state": "open"},
            timeout=timeout,
        )
        if response.status_code == 200:
            prs = response.json()
            return prs[0] if prs else None
    except Exception:
        pass
    
    return None


__all__ = [
    "get_github_token",
    "create_github_pr_headers",
    "create_github_pr_url",
    "create_pr_data",
    "check_existing_pr",
    "REQUESTS_AVAILABLE",
]


