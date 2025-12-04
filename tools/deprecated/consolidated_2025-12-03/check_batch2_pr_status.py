#!/usr/bin/env python3
"""
Check Batch 2 PR Status
========================

Checks status of Batch 2 PRs that need coordination:
- UltimateOptionsTradingRobot PR #3 (needs merge)
- MeTuber PR #13 (location verification)
- DaDudekC PR #1 (location verification)

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-01-27
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.check_pr_status import check_pr_status
from tools.merge_prs_via_api import get_github_token
import requests


def check_batch2_prs():
    """Check Batch 2 PR statuses."""
    token = get_github_token()
    if not token:
        print("❌ GITHUB_TOKEN not found")
        return 1
    
    owner = "Dadudekc"
    
    # Batch 2 PRs to check
    prs_to_check = [
        {
            "target_repo": "trading-leads-bot",
            "source_repo": "UltimateOptionsTradingRobot",
            "pr_number": 3,
            "description": "UltimateOptionsTradingRobot → trading-leads-bot",
            "status": "needs_merge"
        },
        {
            "target_repo": "Streamertools",
            "source_repo": "MeTuber",
            "pr_number": 13,
            "description": "MeTuber → Streamertools",
            "status": "verify_location"
        },
        {
            "target_repo": "DaDudeKC-Website",
            "source_repo": "DaDudekC",
            "pr_number": 1,
            "description": "DaDudekC → DaDudeKC-Website",
            "status": "verify_location"
        }
    ]
    
    print("🔍 Checking Batch 2 PR Status\n")
    print("=" * 70)
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    results = []
    
    for pr_info in prs_to_check:
        target_repo = pr_info["target_repo"]
        source_repo = pr_info["source_repo"]
        pr_number = pr_info["pr_number"]
        description = pr_info["description"]
        expected_status = pr_info["status"]
        
        print(f"\n📋 {description}")
        print(f"   Target: {owner}/{target_repo}")
        print(f"   Source: {owner}/{source_repo}")
        print(f"   Expected PR: #{pr_number}")
        
        # Check PR in target repo
        status = check_pr_status(owner, target_repo, pr_number)
        
        if status:
            print(f"   ✅ PR #{pr_number} found in {target_repo}")
            print(f"   State: {status['state']}")
            print(f"   Merged: {status['merged']}")
            print(f"   Mergeable: {status['mergeable']}")
            print(f"   URL: {status['url']}")
            print(f"   Title: {status['title']}")
            
            if status['merged']:
                print(f"   ✅ ALREADY MERGED!")
                results.append({
                    "description": description,
                    "status": "merged",
                    "pr_number": pr_number,
                    "url": status['url']
                })
            elif status['state'] == 'open':
                if status['mergeable']:
                    print(f"   ⏳ Open and mergeable - READY FOR MERGE")
                    results.append({
                        "description": description,
                        "status": "ready",
                        "pr_number": pr_number,
                        "url": status['url']
                    })
                else:
                    print(f"   ⚠️ Open but has conflicts - NEEDS RESOLUTION")
                    results.append({
                        "description": description,
                        "status": "conflicts",
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
            # PR not found in target repo - check if it's in source repo
            print(f"   ⚠️ PR #{pr_number} not found in {target_repo}")
            print(f"   Checking source repo {source_repo}...")
            
            source_status = check_pr_status(owner, source_repo, pr_number)
            
            if source_status:
                print(f"   ✅ PR #{pr_number} found in {source_repo} (source repo)")
                print(f"   State: {source_status['state']}")
                print(f"   URL: {source_status['url']}")
                results.append({
                    "description": description,
                    "status": "found_in_source",
                    "pr_number": pr_number,
                    "url": source_status['url'],
                    "location": source_repo
                })
            else:
                # Check all PRs in target repo to find matching PR
                print(f"   🔍 Searching for PR in {target_repo}...")
                url = f"https://api.github.com/repos/{owner}/{target_repo}/pulls"
                params = {"state": "all", "per_page": 100}
                
                response = requests.get(url, headers=headers, params=params, timeout=10)
                if response.status_code == 200:
                    prs = response.json()
                    matching_prs = [
                        pr for pr in prs 
                        if source_repo.lower() in pr.get('title', '').lower() 
                        or source_repo.lower() in pr.get('head', {}).get('ref', '').lower()
                    ]
                    
                    if matching_prs:
                        print(f"   ✅ Found {len(matching_prs)} matching PR(s):")
                        for pr in matching_prs:
                            print(f"      PR #{pr['number']}: {pr['title']} ({pr['state']})")
                            print(f"      URL: {pr.get('html_url', 'N/A')}")
                        results.append({
                            "description": description,
                            "status": "found_alternate",
                            "prs": matching_prs
                        })
                    else:
                        print(f"   ❌ No matching PR found in {target_repo}")
                        results.append({
                            "description": description,
                            "status": "not_found",
                            "target_repo": target_repo
                        })
                else:
                    print(f"   ❌ Error searching PRs: {response.status_code}")
                    results.append({
                        "description": description,
                        "status": "error",
                        "error": f"HTTP {response.status_code}"
                    })
    
    print("\n" + "=" * 70)
    print("📊 BATCH 2 PR STATUS SUMMARY")
    print("=" * 70)
    
    ready_to_merge = [r for r in results if r.get("status") == "ready"]
    already_merged = [r for r in results if r.get("status") == "merged"]
    needs_attention = [r for r in results if r.get("status") not in ["ready", "merged"]]
    
    print(f"\n✅ Ready to merge: {len(ready_to_merge)}")
    for r in ready_to_merge:
        print(f"   - {r['description']}: {r['url']}")
    
    print(f"\n✅ Already merged: {len(already_merged)}")
    for r in already_merged:
        print(f"   - {r['description']}: {r['url']}")
    
    print(f"\n⚠️ Needs attention: {len(needs_attention)}")
    for r in needs_attention:
        status = r.get("status", "unknown")
        print(f"   - {r['description']}: {status}")
        if "url" in r:
            print(f"     URL: {r['url']}")
        if "location" in r:
            print(f"     Found in: {r['location']}")
    
    print("\n" + "=" * 70)
    print("✅ PR status check complete")
    
    return 0


if __name__ == "__main__":
    sys.exit(check_batch2_prs())



