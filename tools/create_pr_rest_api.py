#!/usr/bin/env python3
"""
Create GitHub PR using REST API
================================

Creates GitHub pull requests using REST API (bypasses GraphQL rate limits).

Author: Agent-7
Date: 2025-11-26
"""

import os
import sys
import requests
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


def get_github_token() -> str:
    """Get GitHub token from environment."""
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN or GH_TOKEN environment variable required")
    return token


def create_pr_rest_api(
    owner: str,
    repo: str,
    title: str,
    body: str,
    head: str,
    base: str = "main"
) -> dict:
    """
    Create GitHub PR using REST API.
    
    Args:
        owner: Repository owner (e.g., "Dadudekc")
        repo: Target repository name
        title: PR title
        body: PR description
        head: Source branch (format: "owner:branch" or "branch")
        base: Target branch (default: "main")
    
    Returns:
        PR data dict with URL
    """
    token = get_github_token()
    
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
    
    payload = {
        "title": title,
        "body": body,
        "head": head,
        "base": base
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    if response.status_code == 201:
        pr_data = response.json()
        return {
            "success": True,
            "pr_url": pr_data.get("html_url"),
            "pr_number": pr_data.get("number"),
            "data": pr_data
        }
    elif response.status_code == 422:
        error_data = response.json()
        return {
            "success": False,
            "error": error_data.get("message", "Validation failed"),
            "errors": error_data.get("errors", [])
        }
    else:
        return {
            "success": False,
            "error": f"HTTP {response.status_code}: {response.text}",
            "status_code": response.status_code
        }


def main():
    """Main entry point."""
    if len(sys.argv) < 6:
        print("Usage: python tools/create_pr_rest_api.py <owner> <repo> <title> <head> <body_file>")
        print("\nExample:")
        print("  python tools/create_pr_rest_api.py Dadudekc FocusForge 'Merge focusforge' 'Dadudekc:focusforge:main' body.txt")
        sys.exit(1)
    
    owner = sys.argv[1]
    repo = sys.argv[2]
    title = sys.argv[3]
    head = sys.argv[4]
    body_file = Path(sys.argv[5])
    
    if not body_file.exists():
        body = f"Repository consolidation merge: {head}"
    else:
        body = body_file.read_text(encoding="utf-8")
    
    result = create_pr_rest_api(owner, repo, title, body, head)
    
    if result["success"]:
        print(f"✅ PR created: {result['pr_url']}")
        print(f"   PR #{result['pr_number']}")
        sys.exit(0)
    else:
        print(f"❌ PR creation failed: {result.get('error')}")
        if "errors" in result:
            for error in result["errors"]:
                print(f"   - {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()

