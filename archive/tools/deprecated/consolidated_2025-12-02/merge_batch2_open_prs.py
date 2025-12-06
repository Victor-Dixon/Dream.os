#!/usr/bin/env python3
"""
Merge Batch 2 Open PRs
======================

Merges the 2 open PRs from Batch 2 consolidation:
1. MeTuber → Streamertools (PR #13) - Ready to merge
2. DreamBank → DreamVault (PR #1) - Mark ready, then merge

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-11-29
Priority: HIGH
"""

import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.merge_prs_via_api import merge_pr, get_github_token
import requests


def mark_pr_ready(token: str, owner: str, repo: str, pr_number: int) -> bool:
    """Mark a draft PR as ready for review using the ready endpoint."""
    # Use the ready endpoint instead of patch
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/ready"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.put(url, headers=headers, timeout=30)
        if response.status_code == 204:
            print(f"✅ PR #{pr_number} marked as ready for review (204)")
            return True
        elif response.status_code == 200:
            print(f"✅ PR #{pr_number} marked as ready for review (200)")
            return True
        else:
            # Fallback: Try PATCH method
            url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
            data = {"draft": False}
            response = requests.patch(url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                print(f"✅ PR #{pr_number} marked as ready (PATCH fallback)")
                return True
            else:
                print(f"❌ Failed to mark PR #{pr_number} as ready: {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return False
    except Exception as e:
        print(f"❌ Error marking PR #{pr_number} as ready: {e}")
        return False


def main():
    """Merge Batch 2 open PRs."""
    token = get_github_token()
    if not token:
        print("❌ GITHUB_TOKEN not found. Set it in .env file or environment variable.")
        return 1

    owner = "Dadudekc"

    print("🚀 Merging Batch 2 Open PRs\n")
    print("=" * 70)

    # PR 1: MeTuber → Streamertools (PR #13) - Ready to merge
    print("\n📋 PR #1: MeTuber → Streamertools (PR #13)")
    print("   Status: Ready to merge")
    print("   Repository: Streamertools")
    
    success = merge_pr(
        token=token,
        owner=owner,
        repo="Streamertools",
        pr_number=13,
        merge_method="merge"
    )

    if success:
        print(f"✅ Successfully merged PR #13")
    else:
        print(f"❌ Failed to merge PR #13")
    
    time.sleep(2)  # Small delay between operations

    # PR 2: DreamBank → DreamVault (PR #1) - Mark ready, then merge
    print("\n📋 PR #2: DreamBank → DreamVault (PR #1)")
    print("   Status: Draft - marking as ready, then merging")
    print("   Repository: DreamVault")
    
    # Step 1: Mark PR as ready
    print("   Step 1: Marking PR as ready for review...")
    if mark_pr_ready(token, owner, "DreamVault", 1):
        time.sleep(2)  # Small delay after marking ready
        
        # Step 2: Merge PR
        print("   Step 2: Merging PR...")
        success = merge_pr(
            token=token,
            owner=owner,
            repo="DreamVault",
            pr_number=1,
            merge_method="merge"
        )

        if success:
            print(f"✅ Successfully merged PR #1")
        else:
            print(f"❌ Failed to merge PR #1")
    else:
        print("❌ Cannot merge PR #1 - failed to mark as ready")

    print("\n" + "=" * 70)
    print("🏁 Batch 2 Open PRs Merge Attempts Complete")
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

