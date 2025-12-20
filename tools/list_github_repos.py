#!/usr/bin/env python3
"""List all repositories for a GitHub user/organization."""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import requests
except ImportError:
    print("❌ Error: 'requests' library not installed")
    print("   Install with: pip install requests")
    sys.exit(1)

from src.core.utils.github_utils import get_github_token


def list_repos(owner: str):
    """List all repositories for a GitHub user/organization."""
    token = get_github_token()
    if not token:
        print("❌ Error: GitHub token not found")
        sys.exit(1)
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    url = f"https://api.github.com/users/{owner}/repos"
    params = {"type": "all", "per_page": 100}
    
    repos = []
    page = 1
    
    while True:
        params["page"] = page
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"❌ Error fetching repos: {response.status_code}")
            print(f"   {response.text}")
            break
        
        page_repos = response.json()
        if not page_repos:
            break
        
        repos.extend(page_repos)
        
        if len(page_repos) < params["per_page"]:
            break
        
        page += 1
    
    return repos


def main():
    """Main function."""
    owner = "Victor-Dixon"
    
    print(f"📦 Fetching repositories for {owner}...\n")
    
    repos = list_repos(owner)
    
    # Filter out forks, only show owner's repos
    owner_repos = [r for r in repos if r.get("owner", {}).get("login") == owner]
    
    print(f"Found {len(owner_repos)} repositories:\n")
    
    for repo in sorted(owner_repos, key=lambda x: x["name"]):
        name = repo["name"]
        desc = repo.get("description") or "(no description)"
        private = "🔒" if repo.get("private") else "🌐"
        print(f"{private} {name}: {desc}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
