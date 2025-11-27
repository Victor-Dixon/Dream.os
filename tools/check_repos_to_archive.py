#!/usr/bin/env python3
"""
Check which repos are ready to archive after merges.
"""
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
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    print("🔍 Checking repos ready for archive...\n")
    
    # Repos that should be archived (from our merges)
    repos_to_check = [
        {"name": "DigitalDreamscape", "repo_num": 59, "merged_into": "DreamVault", "pr": 4},
        {"name": "Thea", "repo_num": 66, "merged_into": "DreamVault", "pr": 3},
        {"name": "contract-leads", "repo_num": 20, "merged_into": "trading-leads-bot", "pr": 5},
    ]
    
    print("📊 Repos Ready for Archive:\n")
    
    archived_count = 0
    not_archived_count = 0
    
    for repo_info in repos_to_check:
        repo_name = repo_info["name"]
        repo_url = f"https://api.github.com/repos/{owner}/{repo_name}"
        
        try:
            response = requests.get(repo_url, headers=headers, timeout=30)
            if response.status_code == 200:
                repo_data = response.json()
                archived = repo_data.get("archived", False)
                
                if archived:
                    print(f"✅ {repo_name} (Repo #{repo_info['repo_num']}) - ALREADY ARCHIVED")
                    archived_count += 1
                else:
                    print(f"⚠️ {repo_name} (Repo #{repo_info['repo_num']}) - NOT ARCHIVED")
                    print(f"   Merged into: {repo_info['merged_into']} (PR #{repo_info['pr']})")
                    print(f"   URL: {repo_data.get('html_url', 'N/A')}")
                    not_archived_count += 1
            elif response.status_code == 404:
                print(f"❌ {repo_name} (Repo #{repo_info['repo_num']}) - NOT FOUND (may be deleted)")
            else:
                print(f"⚠️ {repo_name} (Repo #{repo_info['repo_num']}) - Error: {response.status_code}")
        except Exception as e:
            print(f"❌ {repo_name} (Repo #{repo_info['repo_num']}) - Error: {e}")
        
        print()
    
    print("="*60)
    print(f"📊 Summary:")
    print(f"   Already Archived: {archived_count}")
    print(f"   Ready to Archive: {not_archived_count}")
    print(f"   Total Checked: {len(repos_to_check)}")
    print()
    
    if not_archived_count > 0:
        print("⚠️ These repos need to be archived to reduce the count!")
        print("   The PRs are merged, but the source repos still exist.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

