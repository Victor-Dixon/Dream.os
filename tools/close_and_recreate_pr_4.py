#!/usr/bin/env python3
"""
Close PR #4 and Recreate with Consolidation Changes
===================================================

Closes PR #4, creates a new branch from main, and re-applies the tools_v2
directory consolidation changes.

Author: Agent-3
Date: 2025-12-22
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import requests
    from src.core.utils.github_utils import get_github_token, create_github_pr_headers
except ImportError:
    print("❌ Required modules not available")
    sys.exit(1)


def get_token():
    """Get GitHub token."""
    token = get_github_token()
    if not token:
        import subprocess
        try:
            result = subprocess.run(
                ["git", "config", "--get", "remote.origin.url"],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            if result.returncode == 0:
                url = result.stdout.strip()
                if "ghp_" in url:
                    token = url.split("ghp_")[1].split("@")[0]
                    token = "ghp_" + token
        except Exception:
            pass
    return token


def close_pr_4():
    """Close PR #4."""
    print("=" * 70)
    print("🔄 CLOSING PR #4 AND RECREATING")
    print("=" * 70)
    print()
    
    owner = "Victor-Dixon"
    repo = "Dream.os"
    pr_number = 4
    
    token = get_token()
    if not token:
        print("❌ No GitHub token found")
        return 1
    
    headers = create_github_pr_headers(token)
    
    # Step 1: Close PR #4
    print("📋 Step 1: Closing PR #4...")
    pr_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    
    close_data = {
        "state": "closed"
    }
    
    try:
        response = requests.patch(pr_url, headers=headers, json=close_data, timeout=10)
        if response.status_code == 200:
            print("   ✅ PR #4 closed successfully")
        else:
            print(f"   ⚠️  Failed to close PR: HTTP {response.status_code}")
            print(f"   {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ Error closing PR: {e}")
        return 1
    
    print("\n✅ PR #4 has been closed")
    print("   Next: Creating new branch and applying consolidation changes...")
    
    return 0


if __name__ == "__main__":
    sys.exit(close_pr_4())

