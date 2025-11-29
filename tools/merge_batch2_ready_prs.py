#!/usr/bin/env python3
"""
Merge Batch 2 Ready PRs
========================

Merges Batch 2 PRs that are ready for merge.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-01-27
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.merge_prs_via_api import merge_pr, get_github_token


def merge_ready_prs():
    """Merge Batch 2 PRs that are ready."""
    token = get_github_token()
    if not token:
        print("❌ GITHUB_TOKEN not found")
        return 1
    
    owner = "Dadudekc"
    
    # PRs ready to merge
    ready_prs = [
        {
            "repo": "DaDudeKC-Website",
            "pr_number": 1,
            "description": "DaDudekC → DaDudeKC-Website"
        }
    ]
    
    print("🚀 Merging Batch 2 Ready PRs\n")
    print("=" * 70)
    
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
    
    print("\n" + "=" * 70)
    print("📊 MERGE SUMMARY")
    print("=" * 70)
    
    merged = [r for r in results if r["status"] == "merged"]
    failed = [r for r in results if r["status"] == "failed"]
    
    print(f"\n✅ Merged: {len(merged)}")
    for r in merged:
        print(f"   - {r['description']} (PR #{r['pr_number']})")
    
    if failed:
        print(f"\n❌ Failed: {len(failed)}")
        for r in failed:
            print(f"   - {r['description']} (PR #{r['pr_number']})")
    
    print("\n" + "=" * 70)
    print("✅ Merge operation complete")
    
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(merge_ready_prs())



