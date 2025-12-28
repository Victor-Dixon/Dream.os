#!/usr/bin/env python3
"""
GitHub Repository Description Updater
======================================

Updates repository descriptions on GitHub using the GitHub API.
Supports updating description, topics, and homepage for any accessible repo.

Usage:
    python tools/update_github_repo_description.py --owner <owner> --repo <repo> --description "New description"
    python tools/update_github_repo_description.py --owner Victor-Dixon --repo Mods --description "Cities: Skylines 2 modding workspace"
    python tools/update_github_repo_description.py --owner Victor-Dixon --repo flowr --description "Description" --homepage "https://example.com"

Requirements:
    - GITHUB_TOKEN environment variable set (or GH_TOKEN)
    - Token must have 'repo' scope for private repos, 'public_repo' for public

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-12-27
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional

try:
    import requests
except ImportError:
    print("❌ requests library not installed. Run: pip install requests")
    sys.exit(1)


def get_github_token() -> Optional[str]:
    """Get GitHub token from environment variables."""
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if not token:
        # Try loading from .env file
        env_path = Path(__file__).parent.parent / ".env"
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    if line.startswith("GITHUB_TOKEN="):
                        token = line.split("=", 1)[1].strip().strip('"').strip("'")
                        break
                    elif line.startswith("GH_TOKEN="):
                        token = line.split("=", 1)[1].strip().strip('"').strip("'")
                        break
    return token


def update_repo_description(
    owner: str,
    repo: str,
    description: Optional[str] = None,
    homepage: Optional[str] = None,
    topics: Optional[list] = None,
    private: Optional[bool] = None,
    token: Optional[str] = None,
) -> dict:
    """
    Update GitHub repository metadata.
    
    Args:
        owner: Repository owner (user or organization)
        repo: Repository name
        description: New repository description
        homepage: New homepage URL
        topics: List of topics/tags
        private: Whether repo should be private
        token: GitHub token (optional, uses env var if not provided)
    
    Returns:
        dict with success status and message
    """
    if token is None:
        token = get_github_token()
    
    if not token:
        return {
            "success": False,
            "error": "No GitHub token found. Set GITHUB_TOKEN or GH_TOKEN environment variable.",
        }
    
    # Build update payload
    payload = {}
    if description is not None:
        payload["description"] = description
    if homepage is not None:
        payload["homepage"] = homepage
    if private is not None:
        payload["private"] = private
    
    if not payload and not topics:
        return {
            "success": False,
            "error": "No updates specified. Provide at least one of: description, homepage, topics, private",
        }
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Agent-1-GitHub-Updater",
    }
    
    results = {"success": True, "updates": []}
    
    # Update repo metadata (description, homepage, private)
    if payload:
        url = f"https://api.github.com/repos/{owner}/{repo}"
        response = requests.patch(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            results["updates"].append({
                "type": "metadata",
                "status": "success",
                "updated_fields": list(payload.keys()),
            })
            print(f"✅ Updated {owner}/{repo} metadata: {list(payload.keys())}")
        else:
            results["success"] = False
            results["updates"].append({
                "type": "metadata",
                "status": "failed",
                "error": response.text,
                "status_code": response.status_code,
            })
            print(f"❌ Failed to update metadata: {response.status_code} - {response.text}")
    
    # Update topics (separate API endpoint)
    if topics:
        url = f"https://api.github.com/repos/{owner}/{repo}/topics"
        headers["Accept"] = "application/vnd.github.mercy-preview+json"
        response = requests.put(url, headers=headers, json={"names": topics})
        
        if response.status_code == 200:
            results["updates"].append({
                "type": "topics",
                "status": "success",
                "topics": topics,
            })
            print(f"✅ Updated {owner}/{repo} topics: {topics}")
        else:
            results["success"] = False
            results["updates"].append({
                "type": "topics",
                "status": "failed",
                "error": response.text,
                "status_code": response.status_code,
            })
            print(f"❌ Failed to update topics: {response.status_code} - {response.text}")
    
    return results


def get_repo_info(owner: str, repo: str, token: Optional[str] = None) -> dict:
    """Get current repository information."""
    if token is None:
        token = get_github_token()
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Agent-1-GitHub-Updater",
    }
    if token:
        headers["Authorization"] = f"token {token}"
    
    url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return {
            "success": True,
            "name": data.get("name"),
            "full_name": data.get("full_name"),
            "description": data.get("description"),
            "homepage": data.get("homepage"),
            "topics": data.get("topics", []),
            "private": data.get("private"),
            "html_url": data.get("html_url"),
        }
    else:
        return {
            "success": False,
            "error": response.text,
            "status_code": response.status_code,
        }


def main():
    parser = argparse.ArgumentParser(
        description="Update GitHub repository description and metadata"
    )
    parser.add_argument("--owner", "-o", required=True, help="Repository owner")
    parser.add_argument("--repo", "-r", required=True, help="Repository name")
    parser.add_argument("--description", "-d", help="New repository description")
    parser.add_argument("--homepage", help="Repository homepage URL")
    parser.add_argument("--topics", "-t", nargs="+", help="Repository topics/tags")
    parser.add_argument("--private", action="store_true", help="Make repository private")
    parser.add_argument("--public", action="store_true", help="Make repository public")
    parser.add_argument("--info", "-i", action="store_true", help="Show current repo info only")
    parser.add_argument("--token", help="GitHub token (optional, uses GITHUB_TOKEN env var)")
    
    args = parser.parse_args()
    
    # Show current info if requested
    if args.info:
        info = get_repo_info(args.owner, args.repo, args.token)
        if info["success"]:
            print(f"\n📦 Repository: {info['full_name']}")
            print(f"   Description: {info['description'] or '(none)'}")
            print(f"   Homepage: {info['homepage'] or '(none)'}")
            print(f"   Topics: {', '.join(info['topics']) if info['topics'] else '(none)'}")
            print(f"   Private: {info['private']}")
            print(f"   URL: {info['html_url']}")
        else:
            print(f"❌ Failed to get repo info: {info.get('error')}")
        return
    
    # Determine private flag
    private = None
    if args.private:
        private = True
    elif args.public:
        private = False
    
    # Update repository
    result = update_repo_description(
        owner=args.owner,
        repo=args.repo,
        description=args.description,
        homepage=args.homepage,
        topics=args.topics,
        private=private,
        token=args.token,
    )
    
    if result["success"]:
        print(f"\n✅ Successfully updated {args.owner}/{args.repo}")
    else:
        print(f"\n❌ Update failed: {result.get('error', 'Unknown error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()

