#!/usr/bin/env python3
"""
GitHub Agent Commands for Dream.os Discord Integration
======================================================

Enables AI agents to interact with GitHub through Discord commands.
Integrates the Ultimate GitHub Manager with Dream.os agent ecosystem.

Commands:
- /github setup: Professional repository setup
- /github analyze <repo>: Repository health analysis
- /github issue <repo> <title> <body>: Create issue
- /github ci <repo> <language>: Setup CI/CD
- /github bulk <operation> <repos>: Bulk operations

Author: Victor-Dixon (DaDudeKC)
Integration: Dream.os Agent Ecosystem
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Add tools to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent / "tools"))

try:
    from github.github_manager import GitHubManager
    GITHUB_AVAILABLE = True
except ImportError:
    GITHUB_AVAILABLE = False
    print("⚠️ GitHub Manager not available")

from src.core.messaging_core import send_message
from src.services.messaging.service_adapters import DiscordServiceAdapter

class GitHubAgentCommands:
    """GitHub operations for Dream.os agents via Discord."""

    def __init__(self):
        self.github = None
        self.discord_adapter = DiscordServiceAdapter()
        self._init_github()

    def _init_github(self):
        """Initialize GitHub Manager with token."""
        if not GITHUB_AVAILABLE:
            return

        token = os.getenv('GITHUB_TOKEN') or os.getenv('DISCORD_BOT_TOKEN')
        if token:
            try:
                self.github = GitHubManager(token=token)
                print("✅ GitHub Manager initialized for agents")
            except Exception as e:
                print(f"❌ Failed to initialize GitHub Manager: {e}")
        else:
            print("⚠️ No GitHub token found - set GITHUB_TOKEN in environment")

    async def cmd_github_setup(self, repo_names: List[str] = None) -> str:
        """
        Professional GitHub repository setup.

        Args:
            repo_names: List of repositories to set up (optional)

        Returns:
            Setup results message
        """
        if not self.github:
            return "❌ GitHub Manager not initialized. Check GITHUB_TOKEN."

        try:
            if repo_names:
                results = self.github.setup_all_repositories_professional()
                return f"✅ Professional setup completed for {len(repo_names)} repositories"
            else:
                # Setup all repositories
                results = self.github.setup_all_repositories_professional()
                return "✅ Professional setup completed for all repositories"
        except Exception as e:
            return f"❌ Setup failed: {str(e)}"

    async def cmd_github_analyze(self, repo_name: str) -> str:
        """
        Analyze repository health.

        Args:
            repo_name: Repository name (owner/repo format)

        Returns:
            Health analysis results
        """
        if not self.github:
            return "❌ GitHub Manager not initialized."

        try:
            health = self.github.analyze_repository_health(repo_name)
            score = health['health_score']
            recommendations = health['recommendations']

            response = f"🏥 **{repo_name} Health Score: {score}/100**\n\n"

            if recommendations:
                response += "**Recommendations:**\n"
                for rec in recommendations[:3]:  # Top 3
                    response += f"• {rec}\n"
            else:
                response += "✅ Repository is healthy!"

            return response
        except Exception as e:
            return f"❌ Analysis failed: {str(e)}"

    async def cmd_github_issue(self, repo_name: str, title: str, body: str = "",
                              labels: List[str] = None) -> str:
        """
        Create a GitHub issue.

        Args:
            repo_name: Repository name
            title: Issue title
            body: Issue description
            labels: Issue labels

        Returns:
            Issue creation result
        """
        if not self.github:
            return "❌ GitHub Manager not initialized."

        try:
            issue = self.github.create_issue(repo_name, title, body, labels)
            if issue:
                issue_url = issue.get('html_url', 'URL not available')
                return f"✅ Issue created: **{title}** (#{issue.get('number')})\n{issue_url}"
            else:
                return "❌ Failed to create issue"
        except Exception as e:
            return f"❌ Issue creation failed: {str(e)}"

    async def cmd_github_ci(self, repo_name: str, language: str = "python") -> str:
        """
        Set up CI/CD workflow.

        Args:
            repo_name: Repository name
            language: Programming language

        Returns:
            CI/CD setup result
        """
        if not self.github:
            return "❌ GitHub Manager not initialized."

        try:
            success = self.github.setup_basic_ci_cd(repo_name, language)
            if success:
                return f"✅ CI/CD workflow created for {repo_name} ({language})"
            else:
                return f"❌ Failed to create CI/CD workflow for {repo_name}"
        except Exception as e:
            return f"❌ CI/CD setup failed: {str(e)}"

    async def cmd_github_bulk(self, operation: str, repo_names: List[str],
                             **kwargs) -> str:
        """
        Perform bulk operations on multiple repositories.

        Args:
            operation: Operation type (health_check, setup_ci, update_descriptions)
            repo_names: List of repository names
            **kwargs: Additional operation parameters

        Returns:
            Bulk operation results
        """
        if not self.github:
            return "❌ GitHub Manager not initialized."

        try:
            results = self.github.bulk_operations(operation, repo_names, **kwargs)
            successful = results.get('successful_operations', 0)
            total = results.get('total_repositories', len(repo_names))

            return f"✅ Bulk {operation}: {successful}/{total} operations successful"
        except Exception as e:
            return f"❌ Bulk operation failed: {str(e)}"

    async def cmd_github_status(self) -> str:
        """
        Check GitHub integration status.

        Returns:
            Status information
        """
        status = []

        if GITHUB_AVAILABLE:
            status.append("✅ GitHub Manager library available")
        else:
            status.append("❌ GitHub Manager library not found")

        if self.github:
            status.append("✅ GitHub Manager initialized")
            try:
                repos = self.github.list_repositories()
                status.append(f"✅ GitHub API accessible ({len(repos)} repositories)")
            except:
                status.append("⚠️ GitHub API access may have issues")
        else:
            status.append("❌ GitHub Manager not initialized")

        token = os.getenv('GITHUB_TOKEN')
        if token:
            status.append("✅ GitHub token configured")
        else:
            status.append("⚠️ No GITHUB_TOKEN found")

        return "\n".join(status)

# Global instance for Discord commands
github_commands = GitHubAgentCommands()

# Discord command handlers
async def handle_github_setup(interaction, repo_names=None):
    """Handle /github setup command."""
    await interaction.response.defer()

    if repo_names:
        result = await github_commands.cmd_github_setup(repo_names.split(','))
    else:
        result = await github_commands.cmd_github_setup()

    await interaction.followup.send(result)

async def handle_github_analyze(interaction, repo_name):
    """Handle /github analyze command."""
    await interaction.response.defer()
    result = await github_commands.cmd_github_analyze(repo_name)
    await interaction.followup.send(result)

async def handle_github_issue(interaction, repo_name, title, body="", labels=""):
    """Handle /github issue command."""
    await interaction.response.defer()

    label_list = [l.strip() for l in labels.split(',')] if labels else None
    result = await github_commands.cmd_github_issue(repo_name, title, body, label_list)
    await interaction.followup.send(result)

async def handle_github_ci(interaction, repo_name, language="python"):
    """Handle /github ci command."""
    await interaction.response.defer()
    result = await github_commands.cmd_github_ci(repo_name, language)
    await interaction.followup.send(result)

async def handle_github_status(interaction):
    """Handle /github status command."""
    await interaction.response.defer()
    result = await github_commands.cmd_github_status()
    await interaction.followup.send(f"```\n{result}\n```")

# Export command handlers
__all__ = [
    'handle_github_setup',
    'handle_github_analyze',
    'handle_github_issue',
    'handle_github_ci',
    'handle_github_status',
    'github_commands'
]
