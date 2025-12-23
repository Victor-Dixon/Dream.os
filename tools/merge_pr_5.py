#!/usr/bin/env python3
"""
Merge Pull Request #5
====================

Merges PR #5 (Tools v2 directory consolidation).

Author: Agent-3
Date: 2025-12-22
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import requests
    from src.core.utils.github_utils import get_github_token, create_github_pr_headers
except ImportError:
    print("❌ Required modules not available")
    sys.exit(1)


def get_token():
    """Get GitHub token."""
    token = get_github_token()
    if not token:
        import subprocess
        try:
            result = subprocess.run(
                ["git", "config", "--get", "remote.origin.url"],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            if result.returncode == 0:
                url = result.stdout.strip()
                if "ghp_" in url:
                    token = url.split("ghp_")[1].split("@")[0]
                    token = "ghp_" + token
        except Exception:
            pass
    return token


def merge_pr_5():
    """Merge PR #5."""
    print("=" * 70)
    print("🔄 MERGING PULL REQUEST #5")
    print("=" * 70)
    print()
    
    owner = "Victor-Dixon"
    repo = "Dream.os"
    pr_number = 5
    
    token = get_token()
    if not token:
        print("❌ No GitHub token found")
        return 1
    
    headers = create_github_pr_headers(token)
    
    # Check PR status
    print(f"📡 Checking PR #{pr_number} status...")
    pr_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    
    try:
        response = requests.get(pr_url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"❌ Failed to fetch PR: HTTP {response.status_code}")
            return 1
        
        pr = response.json()
        print(f"   Title: {pr['title']}")
        print(f"   State: {pr['state']}")
        print(f"   Mergeable: {pr.get('mergeable')}")
        print(f"   Mergeable State: {pr.get('mergeable_state')}")
        
        if pr['state'] != 'open':
            print(f"❌ PR is not open (state: {pr['state']})")
            return 1
        
        # Wait a moment for GitHub to calculate mergeability
        if pr.get('mergeable') is None:
            print("   ⏳ Waiting for GitHub to calculate mergeability...")
            time.sleep(3)
            response = requests.get(pr_url, headers=headers, timeout=10)
            pr = response.json()
            print(f"   Mergeable: {pr.get('mergeable')}")
        
        if pr.get('mergeable') is False:
            print("❌ PR has merge conflicts")
            return 1
        
        # Merge the PR
        print(f"\n🔄 Merging PR #{pr_number}...")
        merge_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/merge"
        
        merge_data = {
            "commit_title": f"Merge PR #{pr_number}: {pr['title']}",
            "commit_message": f"Merged via automation\n\n{pr.get('body', '')[:500]}",
            "merge_method": "merge"
        }
        
        merge_response = requests.put(merge_url, headers=headers, json=merge_data, timeout=30)
        
        if merge_response.status_code == 200:
            result = merge_response.json()
            print("   ✅ PR merged successfully!")
            print(f"   SHA: {result.get('sha', 'N/A')}")
            print(f"   Merged: {result.get('merged', False)}")
            print(f"   URL: {pr['html_url']}")
            return 0
        else:
            print(f"   ❌ Failed to merge: HTTP {merge_response.status_code}")
            print(f"   {merge_response.text[:300]}")
            return 1
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(merge_pr_5())

