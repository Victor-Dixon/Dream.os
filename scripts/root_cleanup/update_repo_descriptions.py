#!/usr/bin/env python3
"""
Update GitHub repository descriptions to professional standards.
Updates all 3 repositories under Victor-Dixon account.
"""

import os
import json
import requests
from pathlib import Path

# Load token from .env file
env_file = Path(".env")
token = None
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            if line.startswith("FG_PROFESSIONAL_DEVELOPMENT_ACCOUNT_GITHUB_TOKEN="):
                token = line.split("=", 1)[1].strip()
                break

if not token:
    print("❌ Error: Token not found in .env file")
    exit(1)

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

# Professional descriptions
descriptions = {
    "Dream.os": "Self-optimizing operating system with AI agent coordination. Modular, adaptive, and autonomous workflow automation platform for creators and architects.",
    "MeTuber": "YouTube automation and management platform for content creators. Streamlines video operations, analytics integration, and channel management workflows.",
    "work-projects": "Innovation portfolio showcasing experimental projects, rapid prototypes, and proof-of-concept implementations across various domains."
}

def update_repo_description(repo_name, description):
    """Update repository description via GitHub API."""
    url = f"https://api.github.com/repos/Victor-Dixon/{repo_name}"
    data = {"description": description}
    
    try:
        response = requests.patch(url, headers=headers, json=data)
        if response.status_code == 200:
            repo_data = response.json()
            print(f"✅ Updated: {repo_name}")
            print(f"   New description: {description}")
            print(f"   URL: {repo_data['html_url']}\n")
            return True
        else:
            print(f"❌ Failed to update {repo_name}: {response.status_code}")
            print(f"   Response: {response.text}\n")
            return False
    except Exception as e:
        print(f"❌ Error updating {repo_name}: {e}\n")
        return False

def get_current_descriptions():
    """Fetch current repository descriptions."""
    print("📦 Current Repository Descriptions:\n")
    for repo_name in descriptions.keys():
        url = f"https://api.github.com/repos/Victor-Dixon/{repo_name}"
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                repo_data = response.json()
                current_desc = repo_data.get("description") or "(No description)"
                print(f"  {repo_name}:")
                print(f"    Current: '{current_desc}'")
                print(f"    Proposed: '{descriptions[repo_name]}'")
                print()
            else:
                print(f"  {repo_name}: ❌ Could not fetch (Status: {response.status_code})")
                print()
        except Exception as e:
            print(f"  {repo_name}: ❌ Error: {e}")
            print()

if __name__ == "__main__":
    print("=" * 70)
    print("GitHub Repository Description Updater")
    print("=" * 70)
    print()
    
    # Show current state
    get_current_descriptions()
    
    # Confirm before updating
    print("=" * 70)
    print("Ready to update descriptions. Proceeding...")
    print("=" * 70)
    print()
    
    # Update all repositories
    results = []
    for repo_name, description in descriptions.items():
        success = update_repo_description(repo_name, description)
        results.append((repo_name, success))
    
    # Summary
    print("=" * 70)
    print("Update Summary:")
    print("=" * 70)
    for repo_name, success in results:
        status = "✅ Success" if success else "❌ Failed"
        print(f"  {repo_name}: {status}")
    print()
    
    successful = sum(1 for _, success in results if success)
    print(f"✅ {successful}/{len(results)} repositories updated successfully!")
    print()
    print("View updated repositories:")
    for repo_name in descriptions.keys():
        print(f"  • https://github.com/Victor-Dixon/{repo_name}")

