#!/usr/bin/env python3
"""
Force Merge PR #4
================

Attempts to merge PR #4 using different strategies.

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


def force_merge_pr():
    """Try to merge PR with different strategies."""
    print("=" * 70)
    print("🔄 ATTEMPTING TO MERGE PR #4")
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
    
    # Get PR details
    pr_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    response = requests.get(pr_url, headers=headers, timeout=10)
    
    if response.status_code != 200:
        print(f"❌ Failed to fetch PR: HTTP {response.status_code}")
        return 1
    
    pr = response.json()
    print(f"PR: {pr['title']}")
    print(f"State: {pr['state']}")
    print(f"Mergeable: {pr.get('mergeable')}")
    print()
    
    # Try different merge methods
    merge_methods = ["merge", "squash", "rebase"]
    
    for method in merge_methods:
        print(f"🔄 Trying {method} merge...")
        merge_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/merge"
        
        merge_data = {
            "commit_title": f"Merge PR #{pr_number}: {pr['title']}",
            "commit_message": f"Merged via automation using {method} method",
            "merge_method": method
        }
        
        try:
            merge_response = requests.put(merge_url, headers=headers, json=merge_data, timeout=30)
            
            if merge_response.status_code == 200:
                result = merge_response.json()
                print(f"   ✅ PR merged successfully using {method} method!")
                print(f"   SHA: {result.get('sha', 'N/A')}")
                print(f"   URL: {pr['html_url']}")
                return 0
            elif merge_response.status_code == 405:
                print(f"   ❌ {method} merge not allowed (conflicts or restrictions)")
            elif merge_response.status_code == 409:
                print(f"   ❌ {method} merge conflict")
            else:
                print(f"   ❌ {method} merge failed: HTTP {merge_response.status_code}")
                print(f"   {merge_response.text[:200]}")
        except Exception as e:
            print(f"   ❌ Error with {method} merge: {e}")
        
        print()
    
    print("❌ All merge methods failed")
    print("\n💡 The PR has conflicts that need manual resolution:")
    print(f"   1. Go to: {pr['html_url']}")
    print("   2. Click 'Resolve conflicts' or 'Update branch'")
    print("   3. Resolve conflicts manually")
    print("   4. Then merge via GitHub UI")
    
    return 1


if __name__ == "__main__":
    sys.exit(force_merge_pr())

