#!/usr/bin/env python3
"""
Update and Merge PR #4
======================

Updates PR #4 branch with latest main, then merges it.

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


def update_and_merge_pr():
    """Update PR branch and merge."""
    print("=" * 70)
    print("🔄 UPDATING AND MERGING PR #4")
    print("=" * 70)
    print()
    
    owner = "Victor-Dixon"
    repo = "Dream.os"
    pr_number = 4
    
    # Get token
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
    
    if not token:
        print("❌ No GitHub token found")
        return 1
    
    headers = create_github_pr_headers(token)
    
    # Step 1: Update PR branch with latest main
    print("📡 Step 1: Updating PR branch with latest main...")
    update_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/update-branch"
    
    try:
        update_response = requests.put(update_url, headers=headers, json={"expected_head_sha": None}, timeout=30)
        
        if update_response.status_code == 202:
            print("   ✅ Branch update initiated")
            print("   ⏳ Waiting for GitHub to process update...")
            time.sleep(5)  # Wait for GitHub to process
        elif update_response.status_code == 422:
            print("   ⚠️  Branch cannot be updated (may already be up to date or has conflicts)")
            print(f"   Response: {update_response.text[:200]}")
        else:
            print(f"   ⚠️  Update response: HTTP {update_response.status_code}")
            print(f"   {update_response.text[:200]}")
    except Exception as e:
        print(f"   ⚠️  Error updating branch: {e}")
    
    # Step 2: Check PR status again
    print(f"\n📡 Step 2: Checking PR status...")
    pr_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    response = requests.get(pr_url, headers=headers, timeout=10)
    
    if response.status_code != 200:
        print(f"❌ Failed to fetch PR: HTTP {response.status_code}")
        return 1
    
    pr = response.json()
    print(f"   Mergeable: {pr.get('mergeable')}")
    print(f"   Mergeable State: {pr.get('mergeable_state')}")
    
    # Step 3: Try to merge
    if pr.get('mergeable') is True:
        print(f"\n🔄 Step 3: Merging PR #{pr_number}...")
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
            print(f"   URL: {pr['html_url']}")
            return 0
        else:
            print(f"   ❌ Merge failed: HTTP {merge_response.status_code}")
            print(f"   {merge_response.text[:300]}")
            return 1
    else:
        print(f"\n❌ PR is not mergeable")
        print(f"   Mergeable: {pr.get('mergeable')}")
        print(f"   State: {pr.get('mergeable_state')}")
        print(f"\n💡 Options:")
        print(f"   1. Resolve conflicts manually on GitHub")
        print(f"   2. Use 'git merge' locally to resolve conflicts")
        print(f"   3. Rebase the PR branch onto main")
        return 1


if __name__ == "__main__":
    sys.exit(update_and_merge_pr())

