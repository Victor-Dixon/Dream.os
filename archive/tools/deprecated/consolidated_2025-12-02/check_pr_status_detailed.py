#!/usr/bin/env python3
"""Check PR status in detail."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from tools.merge_prs_via_api import get_github_token
import requests

token = get_github_token()
owner = "Dadudekc"
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

print("Checking Streamertools PRs...")
r = requests.get(f"https://api.github.com/repos/{owner}/Streamertools/pulls?state=all", headers=headers, timeout=10)
if r.status_code == 200:
    prs = r.json()
    print(f"Found {len(prs)} PRs:")
    for p in prs:
        print(f"  PR #{p['number']}: {p['state']} (draft={p.get('draft', False)}, merged={p.get('merged', False)}) - {p['title']}")
        if 'MeTuber' in p['title'] or 'metuber' in p['title'].lower():
            print(f"    URL: {p['html_url']}")
            print(f"    Head: {p.get('head', {}).get('ref')}")
            print(f"    Base: {p.get('base', {}).get('ref')}")

print("\nChecking DreamVault PRs...")
r = requests.get(f"https://api.github.com/repos/{owner}/DreamVault/pulls?state=all", headers=headers, timeout=10)
if r.status_code == 200:
    prs = r.json()
    print(f"Found {len(prs)} PRs:")
    for p in prs:
        print(f"  PR #{p['number']}: {p['state']} (draft={p.get('draft', False)}, merged={p.get('merged', False)}) - {p['title']}")
        if 'DreamBank' in p['title'] or 'dreambank' in p['title'].lower():
            print(f"    URL: {p['html_url']}")
            print(f"    Head: {p.get('head', {}).get('ref')}")
            print(f"    Base: {p.get('base', {}).get('ref')}")


