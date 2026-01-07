#!/usr/bin/env python3
"""
Simple GitHub Manager for Dream.os Agent Integration
===================================================

A simplified GitHub manager designed specifically for Dream.os agent ecosystem.
Provides essential GitHub operations without complex dependencies.

Features:
- Repository analysis
- Issue creation
- Basic health checking
- Agent-friendly API

Author: Victor-Dixon (DaDudeKC)
"""

import os
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SimpleGitHubManager:
    """Simplified GitHub manager for Dream.os agents."""

    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv('GITHUB_TOKEN') or os.getenv('DISCORD_BOT_TOKEN')
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        } if self.token else {}

    def _make_request(self, method: str, url: str, **kwargs) -> Optional[Dict]:
        """Make API request with error handling."""
        try:
            response = requests.request(method, url, headers=self.headers, **kwargs)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ GitHub API error: {e}")
            return None

    def analyze_repository(self, repo_name: str) -> Dict:
        """Analyze repository health."""
        if not self.token:
            return {"error": "No GitHub token configured"}

        url = f"{self.base_url}/repos/{repo_name}"
        data = self._make_request("GET", url)

        if not data:
            return {"error": "Repository not found or access denied"}

        # Calculate simple health score
        health_score = 100

        if not data.get("description"):
            health_score -= 20

        if not data.get("has_readme", False):
            health_score -= 15

        if data.get("open_issues_count", 0) > 10:
            health_score -= 10

        return {
            "name": repo_name,
            "health_score": max(0, health_score),
            "description": data.get("description", "No description"),
            "stars": data.get("stargazers_count", 0),
            "issues": data.get("open_issues_count", 0),
            "language": data.get("language", "Unknown")
        }

    def create_issue(self, repo_name: str, title: str, body: str = "",
                    labels: List[str] = None) -> Dict:
        """Create a GitHub issue."""
        if not self.token:
            return {"error": "No GitHub token configured"}

        url = f"{self.base_url}/repos/{repo_name}/issues"
        data = {
            "title": title,
            "body": body
        }

        if labels:
            data["labels"] = labels

        result = self._make_request("POST", url, json=data)

        if result:
            return {
                "success": True,
                "issue_number": result.get("number"),
                "url": result.get("html_url")
            }
        else:
            return {"error": "Failed to create issue"}

    def list_repositories(self, username: str = None) -> List[Dict]:
        """List user repositories."""
        if not self.token:
            return []

        if not username:
            # Try to get from token
            user_data = self._make_request("GET", f"{self.base_url}/user")
            if user_data:
                username = user_data.get("login")

        if not username:
            return []

        url = f"{self.base_url}/users/{username}/repos"
        repos = self._make_request("GET", url)

        if repos:
            return [{"name": repo["name"], "full_name": repo["full_name"],
                    "description": repo.get("description", "")} for repo in repos[:10]]
        return []

    def get_status(self) -> Dict:
        """Get GitHub integration status."""
        status = {
            "token_configured": bool(self.token),
            "api_accessible": False,
            "rate_limit": None
        }

        if self.token:
            # Test API access
            rate_limit = self._make_request("GET", f"{self.base_url}/rate_limit")
            if rate_limit:
                status["api_accessible"] = True
                status["rate_limit"] = rate_limit.get("rate", {})

        return status

# Global instance
github_manager = SimpleGitHubManager()

def analyze_repo(repo_name: str) -> str:
    """Agent-friendly repository analysis."""
    result = github_manager.analyze_repository(repo_name)

    if "error" in result:
        return f"❌ {result['error']}"

    return f"""🏥 **{result['name']}** Health Analysis:
• Health Score: {result['health_score']}/100
• Language: {result['language']}
• Stars: {result['stars']}
• Open Issues: {result['issues']}
• Description: {result['description'] or 'None'}"""

def create_repo_issue(repo_name: str, title: str, body: str = "") -> str:
    """Agent-friendly issue creation."""
    result = github_manager.create_issue(repo_name, title, body)

    if "error" in result:
        return f"❌ {result['error']}"

    return f"✅ Issue created: {title} (#{result['issue_number']})\n{result['url']}"

def get_github_status() -> str:
    """Get GitHub integration status."""
    status = github_manager.get_status()

    response = "**GitHub Integration Status:**\n"
    response += f"• Token: {'✅' if status['token_configured'] else '❌'}\n"
    response += f"• API Access: {'✅' if status['api_accessible'] else '❌'}\n"

    if status['rate_limit']:
        remaining = status['rate_limit'].get('remaining', 0)
        limit = status['rate_limit'].get('limit', 0)
        response += f"• Rate Limit: {remaining}/{limit} remaining"

    return response

if __name__ == "__main__":
    # Test the integration
    print("🧪 Testing Simple GitHub Manager")
    print(get_github_status())
    print()

    # Test with a sample repo
    test_repo = "Victor-Dixon/AgentTools"
    print(f"Testing analysis of {test_repo}:")
    print(analyze_repo(test_repo))

