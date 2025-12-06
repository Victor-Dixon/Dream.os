#!/usr/bin/env python3
"""Check PR status via REST API."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from tools.merge_prs_via_api import get_github_token
import requests

def check_pr_status(owner: str, repo: str, pr_number: int):
    """Check PR status."""
    token = get_github_token()
    if not token:
        print("❌ GITHUB_TOKEN not found")
        return None
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    response = requests.get(url, headers=headers, timeout=10)
    
    if response.status_code == 200:
        pr_data = response.json()
        return {
            "state": pr_data.get("state", "unknown"),
            "merged": pr_data.get("merged", False),
            "mergeable": pr_data.get("mergeable", None),
            "url": pr_data.get("html_url", ""),
            "title": pr_data.get("title", ""),
            "head": pr_data.get("head", {}).get("ref", ""),
            "base": pr_data.get("base", {}).get("ref", "")
        }
    else:
        print(f"❌ Error checking PR: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python tools/check_pr_status.py <owner> <repo> <pr_number>")
        sys.exit(1)
    
    owner = sys.argv[1]
    repo = sys.argv[2]
    pr_number = int(sys.argv[3])
    
    status = check_pr_status(owner, repo, pr_number)
    if status:
        print(f"PR #{pr_number} Status:")
        print(f"  State: {status['state']}")
        print(f"  Merged: {status['merged']}")
        print(f"  Mergeable: {status['mergeable']}")
        print(f"  URL: {status['url']}")
        print(f"  Title: {status['title']}")
        print(f"  Head: {status['head']}")
        print(f"  Base: {status['base']}")
