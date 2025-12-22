#!/usr/bin/env python3
"""
Merge Pull Request #4
=====================

Merges PR #4 (Tools v2 directory consolidation) in Victor-Dixon/Dream.os.

Author: Agent-3
Date: 2025-12-22
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import requests
    from src.core.utils.github_utils import get_github_token, create_github_pr_headers
except ImportError:
    print("❌ Required modules not available")
    sys.exit(1)


def merge_pr_4():
    """Merge PR #4."""
    print("=" * 70)
    print("🔄 MERGING PULL REQUEST #4")
    print("=" * 70)
    print()
    
    owner = "Victor-Dixon"
    repo = "Dream.os"
    pr_number = 4
    
    # Get token
    token = get_github_token()
    if not token:
        # Try extracting from git config
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
    
    if not token:
        print("❌ No GitHub token found")
        return 1
    
    print(f"✅ Using GitHub token (length: {len(token)})")
    headers = create_github_pr_headers(token)
    
    # First, check PR status
    print(f"📡 Checking PR #{pr_number} status...")
    pr_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    
    try:
        response = requests.get(pr_url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"❌ Failed to fetch PR: HTTP {response.status_code}")
            print(f"   {response.text[:200]}")
            return 1
        
        pr = response.json()
        print(f"   Title: {pr['title']}")
        print(f"   State: {pr['state']}")
        print(f"   Mergeable: {pr.get('mergeable', 'Unknown')}")
        print(f"   Mergeable State: {pr.get('mergeable_state', 'Unknown')}")
        
        if pr['state'] != 'open':
            print(f"❌ PR is not open (state: {pr['state']})")
            return 1
        
        if pr.get('mergeable') is False:
            print("❌ PR has merge conflicts and cannot be merged")
            return 1
        
        if pr.get('mergeable_state') == 'dirty':
            print("❌ PR has merge conflicts")
            return 1
        
        # Merge the PR
        print(f"\n🔄 Merging PR #{pr_number}...")
        merge_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/merge"
        
        merge_data = {
            "commit_title": f"Merge PR #{pr_number}: {pr['title']}",
            "commit_message": f"Merged via automation\n\n{pr.get('body', '')[:500]}",
            "merge_method": "merge"  # Options: merge, squash, rebase
        }
        
        merge_response = requests.put(merge_url, headers=headers, json=merge_data, timeout=30)
        
        if merge_response.status_code == 200:
            result = merge_response.json()
            print("   ✅ PR merged successfully!")
            print(f"   SHA: {result.get('sha', 'N/A')}")
            print(f"   Merged: {result.get('merged', False)}")
            print(f"   Message: {result.get('message', 'N/A')}")
            print(f"\n   URL: {pr['html_url']}")
            return 0
        elif merge_response.status_code == 405:
            print("❌ PR cannot be merged (method not allowed)")
            print("   This usually means the PR has conflicts or is not mergeable")
            print(f"   Response: {merge_response.text[:300]}")
            return 1
        elif merge_response.status_code == 409:
            print("❌ Merge conflict detected")
            print(f"   Response: {merge_response.text[:300]}")
            return 1
        else:
            print(f"❌ Failed to merge PR: HTTP {merge_response.status_code}")
            print(f"   Response: {merge_response.text[:300]}")
            return 1
            
    except Exception as e:
        print(f"❌ Error merging PR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(merge_pr_4())

