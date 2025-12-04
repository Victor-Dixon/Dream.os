#!/usr/bin/env python3
"""Check DreamBank PR #1 status and resolve conflicts if needed."""

import os
import sys
import requests
from pathlib import Path

# Load token
token = os.getenv("GITHUB_TOKEN")
if not token:
    print("❌ GITHUB_TOKEN not found")
    sys.exit(1)

owner = "Dadudekc"
repo = "DreamVault"
pr_number = 1

url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

print(f"🔍 Checking PR #{pr_number} status...")
response = requests.get(url, headers=headers, timeout=30)

if response.status_code == 200:
    pr_data = response.json()
    print(f"✅ PR Information:")
    print(f"   Head Branch: {pr_data.get('head', {}).get('ref')}")
    print(f"   Base Branch: {pr_data.get('base', {}).get('ref')}")
    print(f"   Mergeable: {pr_data.get('mergeable')}")
    print(f"   Mergeable State: {pr_data.get('mergeable_state')}")
    print(f"   Merged: {pr_data.get('merged')}")
    print(f"   Draft: {pr_data.get('draft')}")
    
    if pr_data.get('merged'):
        print("\n✅ PR is already merged!")
    elif pr_data.get('mergeable') is False or pr_data.get('mergeable_state') in ['dirty', 'blocked']:
        print("\n⚠️ PR has conflicts or is not mergeable")
        print(f"   State: {pr_data.get('mergeable_state')}")
    elif pr_data.get('mergeable') is True:
        print("\n✅ PR is mergeable (no conflicts)")
    else:
        print("\n⏳ PR mergeability status is unknown (may need to wait)")
else:
    print(f"❌ Failed to get PR info: {response.status_code}")
    print(f"   {response.text}")


