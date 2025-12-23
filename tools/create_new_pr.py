#!/usr/bin/env python3
"""
Create New PR for Tools Consolidation
=====================================

Creates a new pull request for the tools_v2 consolidation.

Author: Agent-3
Date: 2025-12-22
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import requests
    from src.core.utils.github_utils import get_github_token, create_github_pr_headers, create_pr_data
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


def create_pr():
    """Create new PR."""
    print("=" * 70)
    print("🔄 CREATING NEW PR FOR TOOLS CONSOLIDATION")
    print("=" * 70)
    print()
    
    owner = "Victor-Dixon"
    repo = "Dream.os"
    
    token = get_token()
    if not token:
        print("❌ No GitHub token found")
        return 1
    
    headers = create_github_pr_headers(token)
    
    # PR details
    title = "Tools v2 directory consolidation"
    body = """## Consolidate `tools_v2` into `tools`

This PR consolidates the `tools_v2` directory into `tools` to unify the tool directory structure.

### Changes
- ✅ Moved all files from `tools_v2/` to `tools/`
- ✅ Merged `categories/`, `adapters/`, and `core/` subdirectories
- ✅ Updated all imports from `tools_v2` to `tools` across the codebase
- ✅ Updated 26 config files (JSON/YAML) with new paths
- ✅ Removed `tools_v2` directory

### Files Changed
- Moved 67 category files
- Moved 3 adapter files
- Moved 3 core files
- Updated imports in 3+ Python files
- Updated 26 config files

### Benefits
- Unified tool directory structure
- Simplified imports
- Reduced duplication
- Cleaner codebase organization

This replaces the previous PR #4 which had merge conflicts.
"""
    
    head = "consolidate-tools-v2-into-tools"
    base = "main"
    
    pr_data = create_pr_data(title, body, head, base)
    
    print(f"📋 Creating PR: {title}")
    print(f"   Head: {head}")
    print(f"   Base: {base}")
    print()
    
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    
    try:
        response = requests.post(url, headers=headers, json=pr_data, timeout=30)
        
        if response.status_code == 201:
            pr = response.json()
            print("   ✅ PR created successfully!")
            print(f"   PR #{pr['number']}: {pr['title']}")
            print(f"   URL: {pr['html_url']}")
            print(f"   State: {pr['state']}")
            return 0
        else:
            print(f"   ❌ Failed to create PR: HTTP {response.status_code}")
            print(f"   {response.text[:500]}")
            return 1
    except Exception as e:
        print(f"   ❌ Error creating PR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(create_pr())

