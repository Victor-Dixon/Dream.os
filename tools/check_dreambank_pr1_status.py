#!/usr/bin/env python3
"""
<!-- SSOT Domain: infrastructure -->
Check DreamBank PR #1 status via GitHub API.

Author: Agent-3 (Infrastructure & DevOps Specialist)
"""

import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OWNER = "Dadudekc"
REPO = "DreamVault"
PR_NUMBER = 1

if not GITHUB_TOKEN:
    print("❌ GITHUB_TOKEN not found in environment")
    sys.exit(1)

url = f"https://api.github.com/repos/{OWNER}/{REPO}/pulls/{PR_NUMBER}"
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

print(f"🔍 Checking PR #{PR_NUMBER} status...")
print(f"URL: {url}")

try:
    response = requests.get(url, headers=headers, timeout=30)
    
    if response.status_code == 200:
        pr_data = response.json()
        print(f"\n✅ PR Information:")
        print(f"   State: {pr_data.get('state')}")
        print(f"   Draft: {pr_data.get('draft')}")
        print(f"   Merged: {pr_data.get('merged')}")
        print(f"   Mergeable: {pr_data.get('mergeable')}")
        print(f"   Mergeable State: {pr_data.get('mergeable_state')}")
        print(f"   Head Branch: {pr_data.get('head', {}).get('ref')}")
        print(f"   Base Branch: {pr_data.get('base', {}).get('ref')}")
        print(f"   URL: {pr_data.get('html_url')}")
        
        if pr_data.get('merged'):
            print("\n✅ PR is already merged!")
            sys.exit(0)
        elif pr_data.get('draft'):
            print("\n⚠️ PR is still in DRAFT status")
            print("   Action: Manual 'Ready for review' required via GitHub UI")
            sys.exit(1)
        elif pr_data.get('mergeable') is False:
            print("\n⚠️ PR has conflicts or is not mergeable")
            print(f"   State: {pr_data.get('mergeable_state')}")
            sys.exit(1)
        elif pr_data.get('mergeable') is True:
            print("\n✅ PR is mergeable (no conflicts)")
            print("   Action: Can be merged via API or GitHub UI")
            sys.exit(0)
        else:
            print("\n⏳ PR mergeability status is unknown")
            sys.exit(1)
    else:
        print(f"❌ Failed to get PR info: {response.status_code}")
        print(f"   {response.text}")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ Error checking PR status: {e}")
    sys.exit(1)

