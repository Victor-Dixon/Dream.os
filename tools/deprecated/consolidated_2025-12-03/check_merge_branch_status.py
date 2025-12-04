#!/usr/bin/env python3
"""
Check Merge Branch Status via GitHub API
========================================

Checks if a merge branch exists, has conflicts, and can be merged into main.
Uses GitHub API to avoid disk space issues.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-01-27
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("⚠️ requests library not available. Install with: pip install requests")


def get_github_token() -> Optional[str]:
    """Get GitHub token from environment or .env file."""
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if token:
        return token
    
    env_file = Path(".env")
    if env_file.exists():
        try:
            with open(env_file, "r") as f:
                for line in f:
                    if line.startswith("GITHUB_TOKEN="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
        except Exception:
            pass
    
    return None


def check_merge_branch(token: str, owner: str, repo: str, branch: str) -> Dict[str, Any]:
    """Check if merge branch exists and get its status."""
    if not REQUESTS_AVAILABLE:
        return {"error": "requests library not available"}
    
    url = f"https://api.github.com/repos/{owner}/{repo}/branches/{branch}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            branch_data = response.json()
            return {
                "exists": True,
                "sha": branch_data.get("commit", {}).get("sha"),
                "name": branch_data.get("name"),
                "protected": branch_data.get("protected", False)
            }
        elif response.status_code == 404:
            return {"exists": False, "error": "Branch not found"}
        else:
            return {"error": f"Status {response.status_code}: {response.text}"}
    except Exception as e:
        return {"error": str(e)}


def check_merge_status(token: str, owner: str, repo: str, base: str, head: str) -> Dict[str, Any]:
    """Check if merge can be performed (checks for conflicts using compare endpoint)."""
    if not REQUESTS_AVAILABLE:
        return {"error": "requests library not available"}
    
    # Use compare endpoint to check mergeability
    url = f"https://api.github.com/repos/{owner}/{repo}/compare/{base}...{head}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            compare_data = response.json()
            status = compare_data.get("status", "unknown")
            
            if status == "identical":
                return {
                    "mergeable": True,
                    "has_conflicts": False,
                    "already_merged": True,
                    "status": "identical"
                }
            elif status == "ahead" or status == "behind" or status == "diverged":
                # Check if there are merge conflicts by trying to create a PR
                return {
                    "mergeable": None,  # Unknown - need PR check
                    "has_conflicts": None,
                    "status": status,
                    "ahead_by": compare_data.get("ahead_by", 0),
                    "behind_by": compare_data.get("behind_by", 0),
                    "total_commits": compare_data.get("total_commits", 0)
                }
            else:
                return {
                    "mergeable": None,
                    "has_conflicts": None,
                    "status": status
                }
        elif response.status_code == 404:
            return {
                "mergeable": False,
                "has_conflicts": False,
                "error": "Branch not found"
            }
        else:
            return {
                "error": f"Status {response.status_code}: {response.text}"
            }
    except Exception as e:
        return {"error": str(e)}


def check_pr_status(token: str, owner: str, repo: str, branch: str) -> Dict[str, Any]:
    """Check if there's an open PR for this branch."""
    if not REQUESTS_AVAILABLE:
        return {"error": "requests library not available"}
    
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    params = {
        "head": f"{owner}:{branch}",
        "state": "open"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        if response.status_code == 200:
            prs = response.json()
            if prs:
                pr = prs[0]
                return {
                    "has_pr": True,
                    "pr_number": pr.get("number"),
                    "pr_url": pr.get("html_url"),
                    "mergeable": pr.get("mergeable"),
                    "mergeable_state": pr.get("mergeable_state"),
                    "has_conflicts": pr.get("mergeable") is False or pr.get("mergeable_state") == "dirty"
                }
            else:
                return {"has_pr": False}
        else:
            return {"error": f"Status {response.status_code}: {response.text}"}
    except Exception as e:
        return {"error": str(e)}


def main():
    """Check Merge #1 (DreamBank → DreamVault) status."""
    token = get_github_token()
    if not token:
        print("❌ GITHUB_TOKEN not found.")
        return 1
    
    owner = "Dadudekc"
    repo = "DreamVault"
    merge_branch = "merge-DreamBank-20251124"
    # Try main first, fallback to master
    base_branch = "main"
    
    print(f"🔍 Checking Merge #1 (DreamBank → DreamVault) status...\n")
    print(f"📋 Repository: {owner}/{repo}")
    print(f"📋 Merge Branch: {merge_branch}")
    print(f"📋 Base Branch: {base_branch}\n")
    
    # 1. Check if merge branch exists
    print("1️⃣ Checking if merge branch exists...")
    branch_status = check_merge_branch(token, owner, repo, merge_branch)
    if branch_status.get("exists"):
        print(f"  ✅ Merge branch exists (SHA: {branch_status.get('sha', 'N/A')[:8]}...)")
    else:
        print(f"  ❌ Merge branch does not exist: {branch_status.get('error', 'Unknown error')}")
        return 1
    
    # 2. Check if there's an open PR
    print("\n2️⃣ Checking for open PR...")
    pr_status = check_pr_status(token, owner, repo, merge_branch)
    if pr_status.get("has_pr"):
        print(f"  ✅ PR exists: #{pr_status.get('pr_number')} - {pr_status.get('pr_url')}")
        if pr_status.get("has_conflicts"):
            print(f"  ⚠️ PR has CONFLICTS - needs resolution!")
            print(f"  📊 Mergeable state: {pr_status.get('mergeable_state')}")
        else:
            print(f"  ✅ PR is mergeable (no conflicts)")
    else:
        print(f"  ⚠️ No open PR found for merge branch")
    
    # 3. Get main branch SHA for comparison
    print("\n3️⃣ Getting main branch SHA for comparison...")
    main_branch_status = check_merge_branch(token, owner, repo, base_branch)
    if not main_branch_status.get("exists"):
        # Try master branch
        print(f"  ⚠️ {base_branch} not found, trying master...")
        base_branch = "master"
        main_branch_status = check_merge_branch(token, owner, repo, base_branch)
    
    if main_branch_status.get("exists"):
        main_sha = main_branch_status.get("sha")
        merge_sha = branch_status.get("sha")
        print(f"  📋 Main branch SHA: {main_sha[:8] if main_sha else 'N/A'}...")
        print(f"  📋 Merge branch SHA: {merge_sha[:8] if merge_sha else 'N/A'}...")
        
        if main_sha and merge_sha:
            if main_sha == merge_sha:
                print(f"  ✅ Main and merge branch are IDENTICAL - merge already complete!")
                merge_status = {"mergeable": True, "has_conflicts": False, "already_merged": True}
            else:
                print(f"  ⚠️ Main and merge branch DIFFER - merge not yet merged into main")
                # Check merge status
                print("\n4️⃣ Checking merge status (compare)...")
                merge_status = check_merge_status(token, owner, repo, base_branch, merge_branch)
        else:
            merge_status = {"error": "Could not get branch SHAs"}
    else:
        print(f"  ❌ Main branch not found: {main_branch_status.get('error', 'Unknown error')}")
        merge_status = {"error": "Main branch not found"}
    if merge_status.get("mergeable"):
        if merge_status.get("already_merged"):
            print(f"  ✅ Already merged into {base_branch}")
        else:
            print(f"  ✅ Mergeable (no conflicts detected)")
    elif merge_status.get("has_conflicts"):
        print(f"  ⚠️ CONFLICTS DETECTED - merge cannot proceed")
    else:
        print(f"  ⚠️ Status: {merge_status.get('error', 'Unknown')}")
    
    # Summary
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    if branch_status.get("exists"):
        print(f"✅ Merge branch exists")
        if pr_status.get("has_pr"):
            if pr_status.get("has_conflicts"):
                print(f"⚠️ PR has CONFLICTS - needs resolution")
                print(f"🔧 ACTION REQUIRED: Resolve conflicts in PR #{pr_status.get('pr_number')}")
            else:
                print(f"✅ PR is mergeable (no conflicts)")
        else:
            if merge_status.get("has_conflicts"):
                print(f"⚠️ Merge has CONFLICTS - needs resolution")
                print(f"🔧 ACTION REQUIRED: Resolve conflicts before merging")
            elif merge_status.get("mergeable"):
                print(f"✅ Merge is ready (no conflicts)")
            else:
                print(f"⚠️ Status unclear: {merge_status.get('error', 'Unknown')}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

