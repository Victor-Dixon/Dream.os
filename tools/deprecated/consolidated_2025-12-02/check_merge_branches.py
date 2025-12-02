#!/usr/bin/env python3
"""Check status of merge branches in Auto_Blogger repo."""

import sys
import requests
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from tools.merge_prs_via_api import get_github_token

def main():
    token = get_github_token()
    username = "dadudekc"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Check branches
    print("Checking branches in Auto_Blogger...")
    url = f"https://api.github.com/repos/{username}/Auto_Blogger/branches"
    response = requests.get(url, headers=headers, timeout=30)
    if response.status_code == 200:
        branches = response.json()
        merge_branches = [b for b in branches if "merge-content" in b["name"] or "merge-FreeWork" in b["name"]]
        print(f"\nMerge branches found: {len(merge_branches)}")
        for b in merge_branches:
            print(f"  - {b['name']}: {b['commit']['sha'][:7]}")
    else:
        print(f"Error: {response.status_code}")
        return 1
    
    # Check compare for merge-content-20251128
    print("\nChecking merge-content-20251128 vs main...")
    url = f"https://api.github.com/repos/{username}/Auto_Blogger/compare/main...merge-content-20251128"
    response = requests.get(url, headers=headers, timeout=30)
    if response.status_code == 200:
        data = response.json()
        print(f"  Commits ahead: {data.get('ahead_by', 0)}")
        print(f"  Commits behind: {data.get('behind_by', 0)}")
        print(f"  Total commits: {data.get('total_commits', 0)}")
        print(f"  Status: {'Identical' if data.get('ahead_by', 0) == 0 else 'Has commits'}")
    else:
        print(f"  Error: {response.status_code} - {response.text[:200]}")
    
    # Check compare for merge-FreeWork-20251128
    print("\nChecking merge-FreeWork-20251128 vs main...")
    url = f"https://api.github.com/repos/{username}/Auto_Blogger/compare/main...merge-FreeWork-20251128"
    response = requests.get(url, headers=headers, timeout=30)
    if response.status_code == 200:
        data = response.json()
        print(f"  Commits ahead: {data.get('ahead_by', 0)}")
        print(f"  Commits behind: {data.get('behind_by', 0)}")
        print(f"  Total commits: {data.get('total_commits', 0)}")
        print(f"  Status: {'Identical' if data.get('ahead_by', 0) == 0 else 'Has commits'}")
    else:
        print(f"  Error: {response.status_code} - {response.text[:200]}")
    
    # Check existing PRs
    print("\nChecking existing PRs...")
    url = f"https://api.github.com/repos/{username}/Auto_Blogger/pulls"
    response = requests.get(url, headers=headers, params={"state": "all"}, timeout=30)
    if response.status_code == 200:
        prs = response.json()
        merge_prs = [p for p in prs if "merge-content" in p.get("head", {}).get("ref", "") or "merge-FreeWork" in p.get("head", {}).get("ref", "")]
        print(f"  PRs found: {len(merge_prs)}")
        for pr in merge_prs:
            print(f"  - PR #{pr['number']}: {pr['head']['ref']} → {pr['base']['ref']} ({pr['state']})")
            print(f"    URL: {pr['html_url']}")
    else:
        print(f"  Error: {response.status_code}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

