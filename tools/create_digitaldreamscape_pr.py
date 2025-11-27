#!/usr/bin/env python3
"""
Create DigitalDreamscape Pull Request
=====================================

Creates a PR for DigitalDreamscape → DreamVault merge using GitHub API.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-01-27
"""

import os
import requests
import sys
from pathlib import Path
from typing import Optional, Dict, Any

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

def get_github_token() -> Optional[str]:
    """Get GitHub token from environment or .env file."""
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if token:
        return token
    
    env_file = Path(".env")
    if env_file.exists():
        try:
            with open(env_file, "r") as f:
                for line in f:
                    if line.startswith("GITHUB_TOKEN="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
        except Exception:
            pass
    
    return None


def create_pr(
    token: str,
    owner: str,
    repo: str,
    title: str,
    body: str,
    head: str,
    base: str = "master"
) -> Dict[str, Any] | None:
    """Create a GitHub Pull Request."""
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
    data = {
        "title": title,
        "body": body,
        "head": head,
        "base": base
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 201:
            pr_data = response.json()
            print(f"✅ PR created: {pr_data.get('html_url')}")
            return pr_data
        elif response.status_code == 422:
            error_data = response.json()
            if "already exists" in str(error_data).lower():
                print(f"⚠️ PR already exists for {repo}: {head} → {base}")
                list_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
                list_response = requests.get(list_url, headers=headers, params={"head": f"{owner}:{head}", "state": "open"}, timeout=30)
                if list_response.status_code == 200:
                    prs = list_response.json()
                    if prs:
                        print(f"✅ Found existing PR: {prs[0].get('html_url')}")
                        return prs[0]
            print(f"❌ PR creation failed for {repo}: {error_data}")
            return None
        else:
            print(f"❌ PR creation failed for {repo}: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error creating PR for {repo}: {e}")
        return None


def main():
    """Create PR for DigitalDreamscape → DreamVault merge."""
    token = get_github_token()
    if not token:
        print("❌ GITHUB_TOKEN not found.")
        return 1
    
    owner = "Dadudekc"
    target_repo = "DreamVault"
    source_repo = "DigitalDreamscape"
    merge_branch = "merge-DigitalDreamscape-20251124"
    base_branch = "master"

    title = f"Merge {source_repo} into {target_repo}"
    body = f"Repository consolidation merge - Dream Projects consolidation from Batch 2. Conflicts resolved using 'ours' strategy (kept {target_repo} versions). D:/Temp configuration used to bypass C: drive disk space issues."

    print(f"🔗 Creating PR for {source_repo} → {target_repo}...")
    print(f"📁 Repository: {owner}/{target_repo}")
    print(f"📤 Merge Branch: {merge_branch}")
    print(f"🔗 Base Branch: {base_branch}\n")
    
    pr_result = create_pr(token, owner, target_repo, title, body, merge_branch, base_branch)
    
    if pr_result:
        print(f"✅ PR creation result: {pr_result.get('html_url', 'Success')}")
        return 0
    else:
        print(f"⚠️ PR creation result: Failed or already exists")
        return 1


if __name__ == "__main__":
    sys.exit(main())

