#!/usr/bin/env python3
"""Verify DreamVault PR #3 current status."""
import os
import sys
import requests
from pathlib import Path

try:
    from dotenv import load_dotenv
    env_path = Path('.env')
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass


def get_github_token():
    token = os.getenv("GITHUB_TOKEN")
    if token:
        return token
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, "r") as f:
            for line in f:
                if line.startswith("GITHUB_TOKEN="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def main():
    token = get_github_token()
    if not token:
        print("❌ GITHUB_TOKEN not found")
        return 1
    
    owner = "Dadudekc"
    repo = "DreamVault"
    pr_number = 3
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    print(f"🔍 Checking DreamVault PR #3 status...\n")
    
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    response = requests.get(url, headers=headers, timeout=30)
    
    if response.status_code == 200:
        pr = response.json()
        
        print(f"📊 PR #3 Status:")
        print(f"   State: {pr.get('state')}")
        print(f"   Merged: {pr.get('merged')}")
        print(f"   Mergeable: {pr.get('mergeable')}")
        print(f"   Mergeable State: {pr.get('mergeable_state')}")
        print(f"   Base: {pr.get('base', {}).get('ref')}")
        print(f"   Head: {pr.get('head', {}).get('ref')}")
        print(f"   URL: {pr.get('html_url', 'N/A')}")
        
        if pr.get('merged'):
            print(f"\n✅ PR #3 is ALREADY MERGED!")
            print(f"   Merge SHA: {pr.get('merge_commit_sha', 'N/A')}")
            print(f"   Merged at: {pr.get('merged_at', 'N/A')}")
        elif pr.get('mergeable') == False:
            print(f"\n⚠️ PR #3 has conflicts or is not mergeable")
            print(f"   Mergeable State: {pr.get('mergeable_state', 'unknown')}")
            if pr.get('mergeable_state') == 'dirty':
                print(f"   Action: Resolve conflicts using 'ours' strategy")
        else:
            print(f"\n✅ PR #3 is mergeable and ready to merge")
    else:
        print(f"❌ Failed to get PR status: {response.status_code}")
        print(f"   Response: {response.text}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

