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

# Import GitHub Bypass System (Local-First Architecture)
try:
    from src.core.synthetic_github import get_synthetic_github
    from src.core.deferred_push_queue import get_deferred_push_queue
    GITHUB_BYPASS_AVAILABLE = True
except ImportError as e:
    GITHUB_BYPASS_AVAILABLE = False
    print(f"⚠️ GitHub Bypass System not available - using legacy method: {e}")
    # Fallback to legacy imports
    from tools.check_pr_status import check_pr_status
    from tools.merge_prs_via_api import get_github_token
    import requests


def check_all_consolidation_prs():
    """Check all consolidation PRs from Agent-2's work using Local-First Architecture."""
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
    
    print("🔍 Checking GitHub Consolidation PR Status (Local-First Architecture)\n")
    print("=" * 60)
    
    # Use GitHub Bypass System if available
    if GITHUB_BYPASS_AVAILABLE:
        try:
            github = get_synthetic_github()
            queue = get_deferred_push_queue()
            
            # Check deferred queue for pending operations
            pending_ops = queue.get_pending_operations()
            if pending_ops:
                print(f"\n📦 Found {len(pending_ops)} pending operations in deferred queue")
            
            for pr_info in prs_to_check:
                repo = pr_info["repo"]
                phase = pr_info["phase"]
                description = pr_info["description"]
                
                print(f"\n📋 {phase}: {description}")
                print(f"   Repo: {owner}/{repo}")
                
                # Check for PR number or branch
                if "pr_number" in pr_info:
                    pr_number = pr_info["pr_number"]
                    # Use SyntheticGitHub (non-blocking)
                    success, pr_data = github.get_pr(owner, repo, pr_number)
                    
                    if success and pr_data:
                        state = pr_data.get('state', 'unknown')
                        merged = pr_data.get('merged', False)
                        mergeable = pr_data.get('mergeable', None)
                        url = pr_data.get('html_url', pr_data.get('url', 'N/A'))
                        
                        print(f"   PR #{pr_number}: {state}")
                        print(f"   Merged: {merged}")
                        if mergeable is not None:
                            print(f"   Mergeable: {mergeable}")
                        print(f"   URL: {url}")
                        
                        if merged:
                            print(f"   ✅ MERGED!")
                        elif state == 'open':
                            if mergeable:
                                print(f"   ⏳ Open and mergeable")
                            else:
                                print(f"   ⚠️ Open but has conflicts")
                        else:
                            print(f"   ❌ State: {state}")
                    else:
                        print(f"   ⚠️ Could not check PR #{pr_number} (may be in deferred queue)")
                        # Check deferred queue for this PR
                        for op in pending_ops:
                            if op.get('repo') == repo and op.get('pr_number') == pr_number:
                                print(f"   📦 Found in deferred queue: {op.get('status', 'pending')}")
                
                elif "check_branch" in pr_info:
                    branch = pr_info["check_branch"]
                    # Use SyntheticGitHub to find PR by branch (non-blocking)
                    success, prs_data = github.get_prs_by_branch(owner, repo, branch)
                    
                    if success and prs_data:
                        if prs_data:
                            pr = prs_data[0] if isinstance(prs_data, list) else prs_data
                            pr_num = pr.get('number', 'N/A')
                            state = pr.get('state', 'unknown')
                            merged = pr.get('merged', False)
                            url = pr.get('html_url', 'N/A')
                            
                            print(f"   PR #{pr_num}: {state}")
                            print(f"   Merged: {merged}")
                            print(f"   URL: {url}")
                            
                            if merged:
                                print(f"   ✅ MERGED!")
                            elif state == 'open':
                                print(f"   ⏳ Open - ready for merge")
                            else:
                                print(f"   ❌ State: {state}")
                        else:
                            print(f"   ⚠️ No PR found for branch: {branch}")
                            print(f"   💡 Merge may have been completed directly or in deferred queue")
                    else:
                        print(f"   ⚠️ Could not check branch: {branch} (may be in deferred queue)")
            
            print("\n" + "=" * 60)
            print("✅ PR status check complete (Local-First Architecture)")
            
            return 0
            
        except Exception as e:
            print(f"⚠️ Error using GitHub Bypass System: {e}")
            print("   Falling back to legacy method...")
            # Fall through to legacy method
    
    # Legacy fallback method
    if not GITHUB_BYPASS_AVAILABLE:
        token = get_github_token()
        if not token:
            print("❌ GITHUB_TOKEN not found")
            return 1
        
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
        print("✅ PR status check complete (Legacy Method)")
    
    return 0


if __name__ == "__main__":
    sys.exit(check_all_consolidation_prs())



