#!/usr/bin/env python3
"""
Archive repos via GitHub REST API
"""
import os
import sys
import requests
from pathlib import Path
from datetime import datetime

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


def archive_repo(token, owner, repo):
    """Archive a repository via GitHub REST API."""
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
    data = {
        "archived": True
    }
    
    try:
        response = requests.patch(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            repo_data = response.json()
            print(f"✅ {repo} archived successfully!")
            return True
        elif response.status_code == 403:
            print(f"❌ {repo} - Permission denied (may need admin access)")
            return False
        elif response.status_code == 404:
            print(f"❌ {repo} - Repository not found")
            return False
        else:
            print(f"❌ {repo} - Archive failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error archiving {repo}: {e}")
        return False


def main():
    token = get_github_token()
    if not token:
        print("❌ GITHUB_TOKEN not found")
        return 1
    
    owner = "Dadudekc"
    
    # Repos ready to archive
    repos_to_archive = [
        {"name": "TheTradingRobotPlug", "repo_num": 38, "merged_into": "trading-leads-bot"},
        {"name": "DreamBank", "repo_num": 3, "merged_into": "DreamVault"},
    ]
    
    print(f"🚀 Archiving {len(repos_to_archive)} repos via GitHub REST API...\n")
    
    results = []
    for repo_info in repos_to_archive:
        repo_name = repo_info["name"]
        print(f"📦 Archiving {repo_name} (Repo #{repo_info['repo_num']})...")
        success = archive_repo(token, owner, repo_name)
        results.append({
            "repo": repo_name,
            "repo_num": repo_info["repo_num"],
            "success": success
        })
        print()
    
    # Summary
    print("="*60)
    print("📊 ARCHIVING SUMMARY")
    print("="*60)
    
    successful = sum(1 for r in results if r["success"])
    failed = len(results) - successful
    
    print(f"✅ Successful: {successful}/{len(results)}")
    print(f"❌ Failed: {failed}/{len(results)}")
    print()
    
    if successful > 0:
        print("✅ Successfully archived:")
        for r in results:
            if r["success"]:
                print(f"  - {r['repo']} (Repo #{r['repo_num']})")
        print()
    
    if failed > 0:
        print("❌ Failed to archive:")
        for r in results:
            if not r["success"]:
                print(f"  - {r['repo']} (Repo #{r['repo_num']})")
        print()
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

