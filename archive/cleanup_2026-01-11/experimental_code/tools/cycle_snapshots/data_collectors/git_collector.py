"""
Git Collector for Cycle Snapshot System
======================================

Analyzes git activity since last snapshot.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Architecture: Agent-2 (Architecture & Design Specialist)
Created: 2026-01-08
V2 Compliant: Yes (<400 lines, functions <30 lines)
"""

import logging
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


def analyze_git_activity(workspace_root: Path, since_timestamp: datetime) -> Dict[str, Any]:
    """
    Analyze git activity since specified timestamp.

    Args:
        workspace_root: Path to workspace root directory
        since_timestamp: Timestamp to analyze from

    Returns:
        Dict with git activity metrics
    """
    try:
        commits = get_commits_since(since_timestamp)
        metrics = calculate_git_metrics(commits)

        return {
            "commits_count": len(commits),
            "commits": commits,
            "metrics": metrics,
            "analysis_period_days": (datetime.now() - since_timestamp).days
        }
    except Exception as e:
        logger.error(f"Git analysis failed: {e}")
        return {"error": str(e)}


def get_commits_since(since_timestamp: datetime) -> List[Dict]:
    """
    Get all commits since specified timestamp.

    Args:
        since_timestamp: Timestamp to get commits from

    Returns:
        List of commit dictionaries
    """
    try:
        # Format timestamp for git command
        since_str = since_timestamp.strftime('%Y-%m-%d %H:%M:%S')

        # Run git log command
        cmd = [
            'git', 'log',
            f'--since="{since_str}"',
            '--pretty=format:%H|%an|%ae|%ad|%s',
            '--date=iso',
            '--no-merges'
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, cwd='.')

        if result.returncode != 0:
            logger.warning(f"Git command failed: {result.stderr}")
            return []

        commits = []
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                parts = line.split('|', 4)
                if len(parts) >= 5:
                    commit = {
                        "hash": parts[0],
                        "author": parts[1],
                        "email": parts[2],
                        "date": parts[3],
                        "message": parts[4],
                        "agent_id": extract_agent_from_commit(parts[4])
                    }
                    commits.append(commit)

        return commits

    except Exception as e:
        logger.error(f"Failed to get commits: {e}")
        return []


def calculate_git_metrics(commits: List[Dict]) -> Dict[str, Any]:
    """
    Calculate metrics from commit data.

    Args:
        commits: List of commit dictionaries

    Returns:
        Dict with calculated metrics
    """
    if not commits:
        return {
            "total_commits": 0,
            "unique_authors": 0,
            "commits_per_day": 0,
            "agent_contributions": {},
            "most_active_agent": None
        }

    # Basic metrics
    total_commits = len(commits)
    unique_authors = len(set(commit["author"] for commit in commits))

    # Calculate commits per day
    if commits:
        earliest = min(datetime.fromisoformat(commit["date"].replace(' +', '+').replace(' -', '-'))
                      for commit in commits)
        latest = max(datetime.fromisoformat(commit["date"].replace(' +', '+').replace(' -', '-'))
                    for commit in commits)
        days_span = max(1, (latest - earliest).days)
        commits_per_day = total_commits / days_span
    else:
        commits_per_day = 0

    # Agent contributions
    agent_contributions = {}
    for commit in commits:
        agent = commit.get("agent_id")
        if agent:
            agent_contributions[agent] = agent_contributions.get(agent, 0) + 1

    # Most active agent
    most_active_agent = max(agent_contributions.items(), key=lambda x: x[1], default=(None, 0))[0]

    return {
        "total_commits": total_commits,
        "unique_authors": unique_authors,
        "commits_per_day": round(commits_per_day, 2),
        "agent_contributions": agent_contributions,
        "most_active_agent": most_active_agent
    }


def extract_agent_from_commit(message: str) -> str:
    """
    Extract agent ID from commit message.

    Args:
        message: Commit message

    Returns:
        Agent ID if found, empty string otherwise
    """
    # Look for patterns like "Agent-3:", "feat: Agent-2", etc.
    import re

    patterns = [
        r'Agent-(\d+)',
        r'agent-(\d+)',
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*):'  # Name patterns like "Agent-3:"
    ]

    for pattern in patterns:
        match = re.search(pattern, message)
        if match:
            agent_part = match.group(1)
            # If it's a number, format as Agent-X
            if agent_part.isdigit():
                return f"Agent-{agent_part}"
            # Otherwise return as-is (for name matches)
            return agent_part

    return ""