#!/usr/bin/env python3
"""
Check All Batch 2 PRs Status
============================

Checks status of all 7 Batch 2 PRs for complete monitoring.

Author: Agent-6 (Coordination & Communication Specialist)
Date: 2025-11-29
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.check_pr_status import check_pr_status
from tools.merge_prs_via_api import get_github_token
import requests


def check_all_batch2_prs():
    """Check all 7 Batch 2 PR statuses."""
    token = get_github_token()
    if not token:
        print("❌ GITHUB_TOKEN not found")
        return 1
    
    owner = "Dadudekc"
    
    # All 7 Batch 2 PRs
    all_prs = [
        {
            "target_repo": "DreamVault",
            "source_repo": "Thea",
            "pr_number": 3,
            "description": "Thea → DreamVault",
            "pr_location": "source"  # PR is in source repo
        },
        {
            "target_repo": "trading-leads-bot",
            "source_repo": "UltimateOptionsTradingRobot",
            "pr_number": 3,
            "description": "UltimateOptionsTradingRobot → trading-leads-bot",
            "pr_location": "target"
        },
        {
            "target_repo": "trading-leads-bot",
            "source_repo": "TheTradingRobotPlug",
            "pr_number": 4,
            "description": "TheTradingRobotPlug → trading-leads-bot",
            "pr_location": "source"
        },
        {
            "target_repo": "Streamertools",
            "source_repo": "MeTuber",
            "pr_number": 13,
            "description": "MeTuber → Streamertools",
            "pr_location": "target"
        },
        {
            "target_repo": "DaDudeKC-Website",
            "source_repo": "DaDudekC",
            "pr_number": 1,
            "description": "DaDudekC → DaDudeKC-Website",
            "pr_location": "target"
        },
        {
            "target_repo": "MachineLearningModelMaker",
            "source_repo": "LSTMmodel_trainer",
            "pr_number": 2,
            "description": "LSTMmodel_trainer → MachineLearningModelMaker",
            "pr_location": "source"
        },
        {
            "target_repo": "DreamVault",
            "source_repo": "DreamBank",
            "pr_number": 1,
            "description": "DreamBank → DreamVault",
            "pr_location": "target"
        }
    ]
    
    print("🔍 Checking All 7 Batch 2 PRs\n")
    print("=" * 70)
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    results = []
    
    for pr_info in all_prs:
        target_repo = pr_info["target_repo"]
        source_repo = pr_info["source_repo"]
        pr_number = pr_info["pr_number"]
        description = pr_info["description"]
        pr_location = pr_info["pr_location"]
        
        print(f"\n📋 {description}")
        print(f"   Target: {owner}/{target_repo}")
        print(f"   Source: {owner}/{source_repo}")
        print(f"   PR #{pr_number} (in {pr_location} repo)")
        
        # Check PR in appropriate repo
        if pr_location == "target":
            status = check_pr_status(owner, target_repo, pr_number)
        else:
            status = check_pr_status(owner, source_repo, pr_number)
        
        if status:
            print(f"   ✅ PR #{pr_number} found")
            print(f"   State: {status['state']}")
            print(f"   Merged: {status['merged']}")
            if status.get('mergeable') is not None:
                print(f"   Mergeable: {status['mergeable']}")
            print(f"   URL: {status['url']}")
            print(f"   Title: {status['title']}")
            
            if status['merged']:
                print(f"   ✅ MERGED!")
                results.append({
                    "description": description,
                    "status": "merged",
                    "pr_number": pr_number,
                    "url": status['url']
                })
            elif status['state'] == 'open':
                if status.get('mergeable') is True:
                    print(f"   ⏳ Open and mergeable - READY FOR MERGE")
                    results.append({
                        "description": description,
                        "status": "ready",
                        "pr_number": pr_number,
                        "url": status['url']
                    })
                elif status.get('mergeable') is False:
                    print(f"   ⚠️ Open but has conflicts - NEEDS RESOLUTION")
                    results.append({
                        "description": description,
                        "status": "conflicts",
                        "pr_number": pr_number,
                        "url": status['url']
                    })
                else:
                    print(f"   ⏳ Open (mergeable status unknown)")
                    results.append({
                        "description": description,
                        "status": "open",
                        "pr_number": pr_number,
                        "url": status['url']
                    })
            else:
                print(f"   ❌ State: {status['state']}")
                results.append({
                    "description": description,
                    "status": status['state'],
                    "pr_number": pr_number,
                    "url": status['url']
                })
        else:
            print(f"   ❌ PR #{pr_number} not found")
            results.append({
                "description": description,
                "status": "not_found",
                "pr_number": pr_number
            })
    
    print("\n" + "=" * 70)
    print("📊 ALL BATCH 2 PR STATUS SUMMARY")
    print("=" * 70)
    
    merged = [r for r in results if r.get("status") == "merged"]
    ready = [r for r in results if r.get("status") == "ready"]
    open_prs = [r for r in results if r.get("status") == "open"]
    conflicts = [r for r in results if r.get("status") == "conflicts"]
    other = [r for r in results if r.get("status") not in ["merged", "ready", "open", "conflicts"]]
    
    print(f"\n✅ Merged: {len(merged)}/{len(all_prs)} ({len(merged)*100//len(all_prs)}%)")
    for r in merged:
        print(f"   - {r['description']}: {r['url']}")
    
    print(f"\n⏳ Ready to merge: {len(ready)}")
    for r in ready:
        print(f"   - {r['description']}: {r['url']}")
    
    if open_prs:
        print(f"\n⏳ Open (status unknown): {len(open_prs)}")
        for r in open_prs:
            print(f"   - {r['description']}: {r['url']}")
    
    if conflicts:
        print(f"\n⚠️ Has conflicts: {len(conflicts)}")
        for r in conflicts:
            print(f"   - {r['description']}: {r['url']}")
    
    if other:
        print(f"\n⚠️ Other status: {len(other)}")
        for r in other:
            print(f"   - {r['description']}: {r.get('status', 'unknown')}")
    
    print("\n" + "=" * 70)
    print(f"✅ Total: {len(merged)} merged, {len(ready)} ready, {len(open_prs)} open, {len(conflicts)} conflicts")
    print("=" * 70)
    
    return results


if __name__ == "__main__":
    results = check_all_batch2_prs()
    sys.exit(0)

