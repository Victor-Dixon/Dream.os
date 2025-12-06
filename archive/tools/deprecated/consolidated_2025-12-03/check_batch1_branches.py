#!/usr/bin/env python3
"""
Check Batch 1 Branch Status
============================

Checks if Batch 1 merge branches exist and their status.

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


def check_branch(token: str, owner: str, repo: str, branch: str) -> Dict[str, Any]:
    """Check if branch exists and get its status."""
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
                "name": branch_data.get("name")
            }
        elif response.status_code == 404:
            return {"exists": False, "error": "Branch not found"}
        else:
            return {"exists": False, "error": f"Status {response.status_code}: {response.text}"}
    except Exception as e:
        return {"exists": False, "error": str(e)}


def compare_branches(token: str, owner: str, repo: str, base: str, head: str) -> Dict[str, Any]:
    """Compare two branches to see if they differ."""
    if not REQUESTS_AVAILABLE:
        return {"error": "requests library not available"}
    
    url = f"https://api.github.com/repos/{owner}/{repo}/compare/{base}...{head}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            compare_data = response.json()
            return {
                "ahead_by": compare_data.get("ahead_by", 0),
                "behind_by": compare_data.get("behind_by", 0),
                "total_commits": compare_data.get("total_commits", 0),
                "status": compare_data.get("status", "unknown")
            }
        else:
            return {"error": f"Status {response.status_code}: {response.text}"}
    except Exception as e:
        return {"error": str(e)}


def main():
    """Check Batch 1 branch status."""
    token = get_github_token()
    if not token:
        print("❌ GITHUB_TOKEN not found.")
        return 1
    
    owner = "Dadudekc"
    
    batch1_merges = [
        {"repo": "Streamertools", "branch": "merge-streamertools-20251124"},
        {"repo": "DaDudekC", "branch": "merge-dadudekc-20251124"},
        {"repo": "LSTMmodel_trainer", "branch": "merge-LSTMmodel_trainer-20251124"},
        {"repo": "FocusForge", "branch": "merge-focusforge-20251124"},
        {"repo": "TBOWTactics", "branch": "merge-tbowtactics-20251124"},
        {"repo": "projectscanner", "branch": "merge-projectscanner-20251124"},
        {"repo": "TROOP", "branch": "merge-TROOP-20251124"}
    ]
    
    print(f"🔍 Checking status of {len(batch1_merges)} Batch 1 merge branches...\n")
    
    for merge in batch1_merges:
        print(f"📝 Checking {merge['repo']} ({merge['branch']})...")
        
        # Check if branch exists
        branch_status = check_branch(token, owner, merge["repo"], merge["branch"])
        if branch_status.get("exists"):
            print(f"  ✅ Branch exists: {merge['branch']}")
            print(f"  📌 SHA: {branch_status.get('sha', 'unknown')[:8]}...")
            
            # Compare with main
            compare = compare_branches(token, owner, merge["repo"], "main", merge["branch"])
            if "error" not in compare:
                print(f"  📊 Status: {compare.get('status', 'unknown')}")
                print(f"  📈 Ahead by: {compare.get('ahead_by', 0)} commits")
                print(f"  📉 Behind by: {compare.get('behind_by', 0)} commits")
                print(f"  📦 Total commits: {compare.get('total_commits', 0)}")
                
                if compare.get('total_commits', 0) == 0:
                    print(f"  ⚠️ WARNING: No commits between main and {merge['branch']} - branch may already be merged!")
            else:
                print(f"  ⚠️ Could not compare: {compare.get('error')}")
        else:
            print(f"  ❌ Branch does not exist: {merge['branch']}")
            print(f"  ⚠️ Error: {branch_status.get('error', 'Unknown')}")
        
        print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

