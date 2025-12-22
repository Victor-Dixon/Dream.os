#!/usr/bin/env python3
"""
Check PR Merge Status
=====================

Checks why PR #4 cannot be merged.

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


def check_pr_status():
    """Check PR merge status."""
    print("=" * 70)
    print("🔍 CHECKING PR #4 MERGE STATUS")
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
    
    print(f"📋 PR Details:")
    print(f"   Title: {pr['title']}")
    print(f"   State: {pr['state']}")
    print(f"   Draft: {pr.get('draft', False)}")
    print(f"   Mergeable: {pr.get('mergeable')}")
    print(f"   Mergeable State: {pr.get('mergeable_state')}")
    print(f"   Merged: {pr.get('merged', False)}")
    print(f"   Head: {pr['head']['ref']} ({pr['head']['sha'][:7]})")
    print(f"   Base: {pr['base']['ref']} ({pr['base']['sha'][:7]})")
    
    # Check for merge conflicts
    print(f"\n🔍 Checking for merge conflicts...")
    if pr.get('mergeable') is False:
        print("   ❌ PR has merge conflicts")
    elif pr.get('mergeable') is True:
        print("   ✅ No merge conflicts detected")
    else:
        print("   ⚠️  Merge status unknown (may need to wait for GitHub to calculate)")
    
    # Check mergeable_state
    mergeable_state = pr.get('mergeable_state', 'unknown')
    print(f"\n📊 Mergeable State: {mergeable_state}")
    
    state_explanations = {
        'clean': '✅ Ready to merge (no conflicts, checks passing)',
        'dirty': '❌ Has merge conflicts',
        'unstable': '⚠️  Checks are failing',
        'blocked': '🚫 Blocked by branch protection rules',
        'behind': '⚠️  Base branch has new commits (needs update)',
        'unknown': '❓ Status not yet calculated by GitHub'
    }
    
    if mergeable_state in state_explanations:
        print(f"   {state_explanations[mergeable_state]}")
    
    # Check status checks
    print(f"\n🔍 Checking status checks...")
    status_url = f"https://api.github.com/repos/{owner}/{repo}/commits/{pr['head']['sha']}/status"
    status_response = requests.get(status_url, headers=headers, timeout=10)
    
    if status_response.status_code == 200:
        status = status_response.json()
        print(f"   State: {status.get('state', 'unknown')}")
        if status.get('statuses'):
            print(f"   Checks: {len(status['statuses'])}")
            for check in status['statuses'][:5]:
                print(f"      - {check['context']}: {check['state']} ({check.get('description', 'N/A')})")
    
    # Check if PR needs to be updated
    print(f"\n🔄 Checking if PR needs update...")
    base_sha = pr['base']['sha']
    head_sha = pr['head']['sha']
    
    # Get base branch latest commit
    base_branch_url = f"https://api.github.com/repos/{owner}/{repo}/git/refs/heads/{pr['base']['ref']}"
    base_response = requests.get(base_branch_url, headers=headers, timeout=10)
    
    if base_response.status_code == 200:
        base_ref = base_response.json()
        latest_base_sha = base_ref['object']['sha']
        
        if latest_base_sha != base_sha:
            print(f"   ⚠️  Base branch has moved since PR was created")
            print(f"   PR base: {base_sha[:7]}")
            print(f"   Latest base: {latest_base_sha[:7]}")
            print(f"   💡 PR may need to be updated/rebased")
        else:
            print(f"   ✅ PR is up to date with base branch")
    
    # Check reviews
    print(f"\n👥 Checking reviews...")
    reviews_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/reviews"
    reviews_response = requests.get(reviews_url, headers=headers, timeout=10)
    
    if reviews_response.status_code == 200:
        reviews = reviews_response.json()
        approvals = [r for r in reviews if r.get('state') == 'APPROVED']
        changes_requested = [r for r in reviews if r.get('state') == 'CHANGES_REQUESTED']
        
        print(f"   Total reviews: {len(reviews)}")
        print(f"   Approvals: {len(approvals)}")
        print(f"   Changes requested: {len(changes_requested)}")
    
    return 0


if __name__ == "__main__":
    sys.exit(check_pr_status())

