#!/usr/bin/env python3
"""
Resolve PR Blockers - Agent-1
=============================

Resolves PR blockers:
1. MeTuber PR #13: Verify and merge (Streamertools repo)
2. DreamBank PR #1: Remove draft status and merge (DreamVault repo)

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-11-30
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.merge_prs_via_api import get_github_token, merge_pr
import requests


def remove_draft_status(token: str, owner: str, repo: str, pr_number: int) -> bool:
    """Remove draft status from a PR."""
    # Use the correct endpoint for readying a draft PR
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/ready"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
    
    try:
        # Try the ready endpoint first (if available)
        response = requests.put(url, headers=headers, timeout=30)
        if response.status_code == 204 or response.status_code == 200:
            print(f"✅ PR #{pr_number} marked as ready (draft removed)!")
            return True
        elif response.status_code == 404:
            # Fallback to PATCH method
            patch_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
            patch_data = {"draft": False}
            patch_response = requests.patch(patch_url, headers=headers, json=patch_data, timeout=30)
            if patch_response.status_code == 200:
                print(f"✅ PR #{pr_number} draft status removed successfully!")
                return True
            else:
                print(f"❌ Failed to remove draft status: {patch_response.status_code}")
                print(f"   Response: {patch_response.text}")
                return False
        else:
            print(f"❌ Failed to ready PR: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error removing draft status: {e}")
        return False


def main():
    """Resolve PR blockers."""
    token = get_github_token()
    if not token:
        print("❌ GITHUB_TOKEN not found")
        return 1
    
    owner = "Dadudekc"
    
    print("=" * 70)
    print("🔧 RESOLVING PR BLOCKERS")
    print("=" * 70)
    
    # 1. MeTuber PR #13 (Streamertools)
    print("\n📋 PR #1: MeTuber → Streamertools (PR #13)")
    print("   Target: Streamertools")
    print("   Action: Verify status, then merge PR")
    
    # First verify PR status
    verify_url = f"https://api.github.com/repos/{owner}/Streamertools/pulls/13"
    verify_headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    verify_response = requests.get(verify_url, headers=verify_headers, timeout=10)
    
    if verify_response.status_code == 200:
        pr_data = verify_response.json()
        print(f"   PR State: {pr_data.get('state')}")
        print(f"   PR Merged: {pr_data.get('merged')}")
        print(f"   PR Draft: {pr_data.get('draft')}")
        print(f"   PR Mergeable: {pr_data.get('mergeable')}")
        
        if pr_data.get('merged'):
            print("   ✅ MeTuber PR #13 already merged!")
            success1 = True
        elif pr_data.get('state') == 'closed' and not pr_data.get('merged'):
            print("   ⚠️ MeTuber PR #13 is closed but not merged")
            success1 = False
        else:
            # Try merging via GitHub CLI first (more reliable)
            import subprocess
            print("   Attempting merge via GitHub CLI...")
            result = subprocess.run(
                ["gh", "pr", "merge", "13", "--repo", f"{owner}/Streamertools", "--merge", "--delete-branch"],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                print("   ✅ MeTuber PR #13 merged successfully via GitHub CLI!")
                success1 = True
            else:
                # Fallback to API
                print(f"   GitHub CLI failed, trying API... ({result.stderr[:100]})")
                success1 = merge_pr(token, owner, "Streamertools", 13, "merge")
                if success1:
                    print("   ✅ MeTuber PR #13 merged successfully via API!")
                else:
                    print("   ⚠️ MeTuber PR #13 merge failed - check logs above")
    else:
        print(f"   ❌ Failed to verify PR status: {verify_response.status_code}")
        success1 = False
    
    # 2. DreamBank PR #1 (DreamVault)
    print("\n📋 PR #2: DreamBank → DreamVault (PR #1)")
    print("   Target: DreamVault")
    print("   Action: Remove draft status, then merge")
    
    # Remove draft status
    print("\n   Step 1: Removing draft status...")
    draft_removed = remove_draft_status(token, owner, "DreamVault", 1)
    
    # Wait a moment for GitHub to process
    import time
    if draft_removed:
        print("   Waiting 2 seconds for GitHub to process draft removal...")
        time.sleep(2)
        
        # Verify draft status was removed
        verify_url = f"https://api.github.com/repos/{owner}/DreamVault/pulls/1"
        verify_headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        verify_response = requests.get(verify_url, headers=verify_headers, timeout=10)
        if verify_response.status_code == 200:
            pr_data = verify_response.json()
            if pr_data.get('draft'):
                print("   ⚠️ PR still shows as draft - trying alternative method...")
                # Try PATCH directly
                patch_url = f"https://api.github.com/repos/{owner}/DreamVault/pulls/1"
                patch_data = {"draft": False}
                patch_response = requests.patch(patch_url, headers=verify_headers, json=patch_data, timeout=30)
                if patch_response.status_code == 200:
                    print("   ✅ Draft status removed via PATCH")
                    time.sleep(2)  # Wait again
                else:
                    print(f"   ⚠️ PATCH also failed: {patch_response.status_code}")
            else:
                print("   ✅ Draft status confirmed removed")
    
    if draft_removed:
        print("\n   Step 2: Waiting longer for GitHub to process draft removal...")
        import time
        time.sleep(5)  # Wait longer
        
        # Verify draft status again
        verify_response = requests.get(verify_url, headers=verify_headers, timeout=10)
        if verify_response.status_code == 200:
            pr_data = verify_response.json()
            if pr_data.get('draft'):
                print("   ⚠️ PR still shows as draft - trying force ready...")
                # Try the ready endpoint again
                ready_url = f"https://api.github.com/repos/{owner}/DreamVault/pulls/1/ready"
                ready_response = requests.put(ready_url, headers=verify_headers, timeout=30)
                if ready_response.status_code in [204, 200]:
                    print("   ✅ PR marked as ready!")
                    time.sleep(3)
                else:
                    print(f"   ⚠️ Ready endpoint failed: {ready_response.status_code}")
            else:
                print("   ✅ Draft status confirmed removed")
        
        print("\n   Step 3: Merging PR...")
        # Try GitHub CLI first
        import subprocess
        result = subprocess.run(
            ["gh", "pr", "merge", "1", "--repo", f"{owner}/DreamVault", "--merge", "--delete-branch"],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            print("   ✅ DreamBank PR #1 merged successfully via GitHub CLI!")
            success2 = True
        else:
            # Fallback to API
            print(f"   GitHub CLI failed, trying API... ({result.stderr[:100]})")
            success2 = merge_pr(token, owner, "DreamVault", 1, "merge")
            if success2:
                print("   ✅ DreamBank PR #1 merged successfully via API!")
            else:
                print("   ⚠️ DreamBank PR #1 merge failed - check logs above")
    else:
        print("   ⚠️ Failed to remove draft status - cannot merge")
        success2 = False
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 PR BLOCKER RESOLUTION SUMMARY")
    print("=" * 70)
    
    if success1:
        print("✅ MeTuber PR #13: MERGED")
    else:
        print("❌ MeTuber PR #13: FAILED")
    
    if draft_removed and success2:
        print("✅ DreamBank PR #1: DRAFT REMOVED & MERGED")
    elif draft_removed:
        print("⚠️ DreamBank PR #1: DRAFT REMOVED, MERGE FAILED")
    else:
        print("❌ DreamBank PR #1: FAILED")
    
    print("=" * 70)
    
    if success1 and draft_removed and success2:
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())

