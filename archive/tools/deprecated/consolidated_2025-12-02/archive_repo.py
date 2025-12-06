#!/usr/bin/env python3
"""
Archive GitHub Repository
=========================

Archives a GitHub repository using REST API.

Usage:
    python tools/archive_repo.py <owner> <repo>

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-01-27
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from tools.merge_prs_via_api import get_github_token
import requests


def archive_repo(owner: str, repo: str) -> bool:
    """Archive a GitHub repository."""
    token = get_github_token()
    if not token:
        print("❌ GITHUB_TOKEN not found")
        return False
    
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
    data = {
        "archived": True
    }
    
    try:
        response = requests.patch(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            print(f"✅ Repository {owner}/{repo} archived successfully!")
            return True
        else:
            print(f"❌ Archive failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error archiving repository: {e}")
        return False


def main():
    """Archive repository."""
    if len(sys.argv) != 3:
        print("Usage: python tools/archive_repo.py <owner> <repo>")
        print("Example: python tools/archive_repo.py dadudekc UltimateOptionsTradingRobot")
        return 1
    
    owner = sys.argv[1]
    repo = sys.argv[2]
    
    print(f"📦 Archiving repository: {owner}/{repo}...")
    print(f"📋 Using REST API\n")
    
    success = archive_repo(owner, repo)
    
    if success:
        print(f"\n✅ Repository archived successfully!")
        return 0
    else:
        print(f"\n❌ Archive failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

