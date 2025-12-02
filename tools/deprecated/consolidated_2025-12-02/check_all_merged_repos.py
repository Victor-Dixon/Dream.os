#!/usr/bin/env python3
"""
Check all repos that should be archived after merges.
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
    
    print("🔍 Checking ALL repos that should be archived...\n")
    
    # All repos that should be archived (from consolidation work)
    repos_to_check = [
        {"name": "MeTuber", "repo_num": 27, "merged_into": "Streamertools"},
        {"name": "streamertools", "repo_num": 31, "merged_into": "Streamertools"},
        {"name": "DaDudekC", "repo_num": 29, "merged_into": "DaDudeKC-Website"},
        {"name": "dadudekc", "repo_num": 36, "merged_into": "DaDudeKC-Website"},
        {"name": "content", "repo_num": 41, "merged_into": "Auto_Blogger"},
        {"name": "FreeWork", "repo_num": 71, "merged_into": "Auto_Blogger"},
        {"name": "DigitalDreamscape", "repo_num": 59, "merged_into": "DreamVault"},
        {"name": "Thea", "repo_num": 66, "merged_into": "DreamVault"},
        {"name": "contract-leads", "repo_num": 20, "merged_into": "trading-leads-bot"},
        {"name": "UltimateOptionsTradingRobot", "repo_num": 5, "merged_into": "trading-leads-bot"},
        {"name": "TheTradingRobotPlug", "repo_num": 38, "merged_into": "trading-leads-bot"},
    ]
    
    print("📊 Repo Archive Status:\n")
    
    archived_count = 0
    not_archived_count = 0
    not_found_count = 0
    
    for repo_info in repos_to_check:
        repo_name = repo_info["name"]
        repo_url = f"https://api.github.com/repos/{owner}/{repo_name}"
        
        try:
            response = requests.get(repo_url, headers=headers, timeout=30)
            if response.status_code == 200:
                repo_data = response.json()
                archived = repo_data.get("archived", False)
                
                if archived:
                    print(f"✅ {repo_name} (Repo #{repo_info['repo_num']}) - ARCHIVED")
                    archived_count += 1
                else:
                    print(f"⚠️ {repo_name} (Repo #{repo_info['repo_num']}) - NOT ARCHIVED")
                    print(f"   Merged into: {repo_info['merged_into']}")
                    print(f"   URL: {repo_data.get('html_url', 'N/A')}")
                    not_archived_count += 1
            elif response.status_code == 404:
                print(f"❌ {repo_name} (Repo #{repo_info['repo_num']}) - NOT FOUND (deleted)")
                not_found_count += 1
            else:
                print(f"⚠️ {repo_name} (Repo #{repo_info['repo_num']}) - Error: {response.status_code}")
        except Exception as e:
            print(f"❌ {repo_name} (Repo #{repo_info['repo_num']}) - Error: {e}")
        
        print()
    
    print("="*60)
    print(f"📊 Summary:")
    print(f"   Already Archived: {archived_count}")
    print(f"   Ready to Archive: {not_archived_count}")
    print(f"   Not Found (Deleted): {not_found_count}")
    print(f"   Total Checked: {len(repos_to_check)}")
    print()
    
    if not_archived_count > 0:
        print("⚠️ IMPORTANT: Archived repos still count in GitHub repo count!")
        print("   To reduce the count, repos must be DELETED (not just archived).")
        print("   However, deletion is PERMANENT - archive first as backup.")
        print()
        print(f"   {not_archived_count} repos need to be archived/deleted to reduce count.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

