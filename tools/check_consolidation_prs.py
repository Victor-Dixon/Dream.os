#!/usr/bin/env python3
"""
Check GitHub Consolidation PR Status
====================================

Checks status of all PRs mentioned in consolidation work.
Author: Agent-4 (Captain)
Date: 2025-11-26
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.check_pr_status import check_pr_status
from tools.merge_prs_via_api import get_github_token
import requests


def check_all_consolidation_prs():
    """Check all consolidation PRs from Agent-2's work."""
    token = get_github_token()
    if not token:
        print("❌ GITHUB_TOKEN not found")
        return 1
    
    owner = "Dadudekc"
    
    # PRs from Agent-2's consolidation work
    prs_to_check = [
        {
            "repo": "DreamVault",
            "pr_number": 4,
            "description": "DigitalDreamscape → DreamVault",
            "phase": "Phase 1"
        },
        {
            "repo": "DreamVault",
            "pr_number": 3,
            "description": "Thea → DreamVault",
            "phase": "Phase 1"
        },
        {
            "repo": "trading-leads-bot",
            "description": "contract-leads → trading-leads-bot",
            "phase": "Phase 2",
            "check_branch": "merge-contract-leads-20251126"
        }
    ]
    
    print("🔍 Checking GitHub Consolidation PR Status\n")
    print("=" * 60)
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    for pr_info in prs_to_check:
        repo = pr_info["repo"]
        phase = pr_info["phase"]
        description = pr_info["description"]
        
        print(f"\n📋 {phase}: {description}")
        print(f"   Repo: {owner}/{repo}")
        
        # Check for PR number or branch
        if "pr_number" in pr_info:
            pr_number = pr_info["pr_number"]
            status = check_pr_status(owner, repo, pr_number)
            
            if status:
                print(f"   PR #{pr_number}: {status['state']}")
                print(f"   Merged: {status['merged']}")
                print(f"   Mergeable: {status['mergeable']}")
                print(f"   URL: {status['url']}")
                
                if status['merged']:
                    print(f"   ✅ MERGED!")
                elif status['state'] == 'open':
                    if status['mergeable']:
                        print(f"   ⏳ Open and mergeable")
                    else:
                        print(f"   ⚠️ Open but has conflicts")
                else:
                    print(f"   ❌ State: {status['state']}")
            else:
                print(f"   ❌ Could not check PR #{pr_number}")
        
        elif "check_branch" in pr_info:
            # Check for PR by branch name
            branch = pr_info["check_branch"]
            url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
            params = {"head": f"{owner}:{branch}", "state": "all"}
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                prs = response.json()
                if prs:
                    pr = prs[0]
                    print(f"   PR #{pr['number']}: {pr['state']}")
                    print(f"   Merged: {pr.get('merged', False)}")
                    print(f"   URL: {pr.get('html_url', 'N/A')}")
                    
                    if pr.get('merged'):
                        print(f"   ✅ MERGED!")
                    elif pr['state'] == 'open':
                        print(f"   ⏳ Open - ready for merge")
                    else:
                        print(f"   ❌ State: {pr['state']}")
                else:
                    print(f"   ⚠️ No PR found for branch: {branch}")
                    print(f"   💡 Merge may have been completed directly")
            else:
                print(f"   ❌ Error checking branch: {response.status_code}")
    
    print("\n" + "=" * 60)
    print("✅ PR status check complete")
    
    return 0


if __name__ == "__main__":
    sys.exit(check_all_consolidation_prs())

