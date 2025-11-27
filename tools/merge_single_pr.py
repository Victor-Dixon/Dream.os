#!/usr/bin/env python3
"""
Merge Single PR via GitHub REST API
===================================

Merges a single PR using GitHub REST API (bypasses GraphQL rate limit).

Usage:
    python tools/merge_single_pr.py <owner> <repo> <pr_number>

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-01-27
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from tools.merge_prs_via_api import merge_pr, get_github_token


def main():
    """Merge a single PR."""
    if len(sys.argv) != 4:
        print("Usage: python tools/merge_single_pr.py <owner> <repo> <pr_number>")
        print("Example: python tools/merge_single_pr.py dadudekc trading-leads-bot 3")
        return 1
    
    owner = sys.argv[1]
    repo = sys.argv[2]
    try:
        pr_number = int(sys.argv[3])
    except ValueError:
        print(f"❌ Invalid PR number: {sys.argv[3]}")
        return 1
    
    token = get_github_token()
    if not token:
        print("❌ GITHUB_TOKEN not found. Set it in .env file or environment variable.")
        return 1
    
    print(f"🚀 Merging PR #{pr_number} in {owner}/{repo}...")
    print(f"📋 Using REST API (bypasses GraphQL rate limit)\n")
    
    success = merge_pr(token, owner, repo, pr_number)
    
    if success:
        print(f"\n✅ PR #{pr_number} merged successfully!")
        return 0
    else:
        print(f"\n❌ PR #{pr_number} merge failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

