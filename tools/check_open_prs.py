#!/usr/bin/env python3
"""
Check Open Pull Requests
========================

Checks for open pull requests in the Victor-Dixon/Dream.os repository.

Author: Agent-3
Date: 2025-12-22
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import requests
    from src.core.utils.github_utils import get_github_token, create_github_pr_headers
except ImportError:
    print("❌ Required modules not available")
    sys.exit(1)


def check_open_prs():
    """Check for open pull requests."""
    print("=" * 70)
    print("🔍 CHECKING OPEN PULL REQUESTS")
    print("=" * 70)
    print()
    
    owner = "Victor-Dixon"
    repo = "Dream.os"
    
    # Get token
    token = get_github_token()
    if not token:
        # Try extracting from git config
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
    
    if not token:
        print("⚠️  No GitHub token found")
        print("   Checking without authentication (rate limited)...")
        headers = {"Accept": "application/vnd.github.v3+json"}
    else:
        print(f"✅ Using GitHub token (length: {len(token)})")
        headers = create_github_pr_headers(token)
    
    # Check open PRs
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    params = {"state": "open", "per_page": 100}
    
    try:
        print(f"📡 Fetching open PRs from {owner}/{repo}...")
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            prs = response.json()
            print(f"\n✅ Found {len(prs)} open pull request(s)\n")
            
            if prs:
                for pr in prs:
                    print(f"  #{pr['number']}: {pr['title']}")
                    print(f"     State: {pr['state']}")
                    print(f"     Branch: {pr['head']['ref']} -> {pr['base']['ref']}")
                    print(f"     Author: {pr['user']['login']}")
                    print(f"     Created: {pr['created_at']}")
                    print(f"     Updated: {pr['updated_at']}")
                    print(f"     Files changed: {pr.get('changed_files', 'N/A')}")
                    print(f"     Additions: +{pr.get('additions', 0)}")
                    print(f"     Deletions: -{pr.get('deletions', 0)}")
                    print(f"     Mergeable: {pr.get('mergeable', 'Unknown')}")
                    if pr.get('body'):
                        body_preview = pr['body'][:200].replace('\n', ' ')
                        print(f"     Description: {body_preview}...")
                    print(f"     URL: {pr['html_url']}")
                    print()
            else:
                print("  ℹ️  No open pull requests found")
        elif response.status_code == 401:
            print("❌ Authentication failed")
            print("   Token may be invalid or expired")
        elif response.status_code == 404:
            print("❌ Repository not found or access denied")
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(f"   {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ Error checking PRs: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(check_open_prs())

