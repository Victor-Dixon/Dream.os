#!/usr/bin/env python3
"""Verify repository merge branch status."""

import os
import requests
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def verify_branch_status():
    """Verify merge branch status for FocusForge and TBOWTactics."""
    token = os.getenv('GITHUB_TOKEN') or os.getenv('GH_TOKEN')
    headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'} if token else {'Accept': 'application/vnd.github.v3+json'}
    
    repos = [
        ('FocusForge', 'merge-Dadudekc/focusforge-20251203'),
        ('TBOWTactics', 'merge-Dadudekc/tbowtactics-20251203')
    ]
    
    print("=" * 60)
    print("🔍 REPOSITORY MERGE BRANCH VERIFICATION")
    print("=" * 60)
    print()
    
    for repo_name, branch_name in repos:
        print(f"📦 {repo_name}")
        print(f"   Branch: {branch_name}")
        
        # Compare branch to main
        url = f'https://api.github.com/repos/Dadudekc/{repo_name}/compare/main...{branch_name}'
        r = requests.get(url, headers=headers, timeout=10)
        
        if r.status_code == 200:
            data = r.json()
            ahead_by = data.get('ahead_by', 0)
            behind_by = data.get('behind_by', 0)
            status = data.get('status', 'unknown')
            
            print(f"   Status: {status}")
            print(f"   Commits ahead of main: {ahead_by}")
            print(f"   Commits behind main: {behind_by}")
            
            if ahead_by == 0:
                print("   ✅ Branch is identical to main (merge already complete)")
            else:
                print(f"   ⚠️ Branch has {ahead_by} unique commits")
        else:
            error = r.json().get('message', 'Unknown error')
            print(f"   ❌ Error: {r.status_code} - {error}")
        
        print()
    
    print("=" * 60)

if __name__ == '__main__':
    verify_branch_status()


