# Header-Variant: full
# Owner: Dream.OS
# Purpose: git collector.
# SSOT: docs/recovery/recovery_registry.yaml#tools-cycle-snapshots-data-collectors-git-collector
# @registry docs/recovery/recovery_registry.yaml#tools-cycle-snapshots-data-collectors-git-collector

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


def analyze_git_activity(
    workspace_root: Path,
    since_timestamp: datetime | None = None,
) -> Dict[str, Any]:
    """Analyze git activity since specified timestamp."""
    since_timestamp = since_timestamp or (datetime.now() - timedelta(days=1))

    if not (Path(workspace_root) / ".git").exists():
        return {"error": "Not a git repository"}

    try:
        commits = get_commits_since(since_timestamp, workspace_root)
        metrics = calculate_git_metrics(commits)
        return {
            "commits_count": len(commits),
            "commits": commits,
            "metrics": metrics,
            "analysis_period_days": max(1, (datetime.now() - since_timestamp).days),
        }
    except Exception as e:
        logger.error(f"Git analysis failed: {e}")
        return {"error": str(e)}


def get_commits_since(since_timestamp: datetime, workspace_root: Path = Path(".")) -> List[Dict]:
    """Get all commits since specified timestamp."""
    try:
        since_str = since_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        cmd = [
            "git",
            "log",
            f'--since="{since_str}"',
            "--pretty=format:%H|%an|%ae|%ad|%s",
            "--date=iso",
            "--no-merges",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(workspace_root))

        if result.returncode != 0:
            logger.warning(f"Git command failed: {result.stderr}")
            return []

        commits: List[Dict[str, Any]] = []
        for line in result.stdout.strip().split("\n"):
            if not line.strip():
                continue
            parts = line.split("|", 4)
            if len(parts) < 5:
                continue
            author_name = parts[1]
            commits.append(
                {
                    "hash": parts[0],
                    "author_name": author_name,
                    "author": author_name,
                    "email": parts[2],
                    "date": parts[3],
                    "message": parts[4],
                    "agent_id": extract_agent_from_commit(parts[4]),
                }
            )

        return commits
    except Exception as e:
        logger.error(f"Failed to get commits: {e}")
        return []


def calculate_git_metrics(commits: List[Dict]) -> Dict[str, Any]:
    """Calculate metrics from commit data."""
    if not commits:
        return {
            "commits": 0,
            "files_changed": 0,
            "authors": {},
            "commit_messages": [],
            "total_commits": 0,
            "unique_authors": 0,
            "commits_per_day": 0,
            "agent_contributions": {},
            "most_active_agent": None,
        }

    authors: Dict[str, int] = {}
    commit_messages: List[str] = []
    for commit in commits:
        author_name = commit.get("author_name") or commit.get("author") or "unknown"
        authors[author_name] = authors.get(author_name, 0) + 1
        commit_messages.append(commit.get("message", ""))

    agent_contributions: Dict[str, int] = {}
    for commit in commits:
        agent = commit.get("agent_id")
        if agent:
            agent_contributions[agent] = agent_contributions.get(agent, 0) + 1

    dates = []
    for commit in commits:
        date_str = commit.get("date")
        if not date_str:
            continue
        try:
            dates.append(datetime.fromisoformat(date_str.replace(" +", "+").replace(" -", "-")))
        except ValueError:
            continue

    if len(dates) >= 2:
        days_span = max(1, (max(dates) - min(dates)).days)
    else:
        days_span = 1

    commits_count = len(commits)
    return {
        "commits": commits_count,
        "files_changed": 0,
        "authors": authors,
        "commit_messages": commit_messages,
        "total_commits": commits_count,
        "unique_authors": len(authors),
        "commits_per_day": round(commits_count / days_span, 2),
        "agent_contributions": agent_contributions,
        "most_active_agent": max(agent_contributions, key=agent_contributions.get, default=None),
    }


def extract_agent_from_commit(message: str) -> str:
    """Extract agent ID from commit message."""
    import re

    for pattern in (r"Agent-(\d+)", r"agent-(\d+)"):
        match = re.search(pattern, message)
        if match:
            return f"Agent-{match.group(1)}"
    return ""
