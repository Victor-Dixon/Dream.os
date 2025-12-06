#!/usr/bin/env python3
"""
Merge Batch 2 Remaining PRs
============================

Merges 2 remaining Batch 2 PRs that are ready for merge:
- MeTuber → Streamertools (PR #13)
- DreamBank → DreamVault (PR #1)

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-11-29
"""

import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.merge_prs_via_api import merge_pr, get_github_token


def main():
    """Merge remaining Batch 2 PRs."""
    token = get_github_token()
    if not token:
        print("❌ GITHUB_TOKEN not found. Set it in .env file or environment variable.")
        return 1
    
    owner = "Dadudekc"
    
    print("🚀 Merging Batch 2 Remaining PRs\n")
    print("=" * 70)
    
    # PRs ready to merge (per Agent-6 coordination)
    ready_prs = [
        {
            "repo": "Streamertools",
            "pr_number": 13,
            "description": "MeTuber → Streamertools"
        },
        {
            "repo": "DreamVault",
            "pr_number": 1,
            "description": "DreamBank → DreamVault"
        }
    ]
    
    results = []
    
    for pr_info in ready_prs:
        repo = pr_info["repo"]
        pr_number = pr_info["pr_number"]
        description = pr_info["description"]
        
        print(f"\n📋 {description}")
        print(f"   Repo: {owner}/{repo}")
        print(f"   PR: #{pr_number}")
        
        success = merge_pr(token, owner, repo, pr_number, merge_method="merge")
        
        if success:
            print(f"   ✅ PR #{pr_number} merged successfully!")
            results.append({
                "description": description,
                "status": "merged",
                "pr_number": pr_number
            })
        else:
            print(f"   ❌ PR #{pr_number} merge failed")
            results.append({
                "description": description,
                "status": "failed",
                "pr_number": pr_number
            })
        
        time.sleep(1)  # Rate limit protection
    
    print("\n" + "=" * 70)
    print("📊 MERGE SUMMARY")
    print("=" * 70)
    
    merged = [r for r in results if r["status"] == "merged"]
    failed = [r for r in results if r["status"] == "failed"]
    
    print(f"\n✅ Merged: {len(merged)}/{len(results)}")
    print(f"❌ Failed: {len(failed)}/{len(results)}")
    
    if merged:
        print("\n✅ Successfully merged:")
        for r in merged:
            print(f"  - {r['description']} (PR #{r['pr_number']})")
    
    if failed:
        print("\n❌ Failed:")
        for r in failed:
            print(f"  - {r['description']} (PR #{r['pr_number']})")
    
    print()
    
    return 0 if len(failed) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

