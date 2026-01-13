"""
Git Collector
=============

Analyzes git activity since last snapshot.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Architecture: Agent-2 (Architecture & Design Specialist)
Created: 2025-12-31
V2 Compliant: Yes (<400 lines, functions <30 lines)

<!-- SSOT Domain: tools -->
"""

import subprocess
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


def get_commits_since(
    since_timestamp: datetime,
    workspace_root: Path
) -> List[Dict[str, Any]]:
    """
    Get git commits since specified timestamp.
    
    Args:
        since_timestamp: Timestamp to get commits since
        workspace_root: Root workspace path (git repository root)
    
    Returns:
        List of commit dictionaries
    """
    commits = []
    
    try:
        # Format timestamp for git log
        since_str = since_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        
        # Run git log command
        result = subprocess.run(
            [
                "git",
                "log",
                f"--since={since_str}",
                "--pretty=format:%H|%an|%ae|%ad|%s",
                "--date=iso",
            ],
            cwd=workspace_root,
            capture_output=True,
            text=True,
            timeout=30,
        )
        
        if result.returncode != 0:
            logger.warning(f"Git log command failed: {result.stderr}")
            return commits
        
        # Parse commit lines
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            
            parts = line.split("|", 4)
            if len(parts) == 5:
                commits.append({
                    "hash": parts[0],
                    "author_name": parts[1],
                    "author_email": parts[2],
                    "date": parts[3],
                    "message": parts[4],
                })
    
    except subprocess.TimeoutExpired:
        logger.error("Git log command timed out")
    except FileNotFoundError:
        logger.warning("Git not available")
    except Exception as e:
        logger.error(f"Error getting git commits: {e}")
    
    return commits


def calculate_git_metrics(commits: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate git activity metrics from commits.
    
    Args:
        commits: List of commit dictionaries
    
    Returns:
        Dict with git metrics
    """
    if not commits:
        return {
            "commits": 0,
            "files_changed": 0,
            "lines_added": 0,
            "lines_removed": 0,
            "authors": {},
        }
    
    # Count commits per author
    authors = {}
    for commit in commits:
        author = commit.get("author_name", "Unknown")
        authors[author] = authors.get(author, 0) + 1
    
    # Note: Getting file changes and line stats requires additional git commands
    # For Phase 1, we'll focus on commit count and authors
    # File stats can be added in Phase 2 if needed
    
    return {
        "commits": len(commits),
        "files_changed": 0,  # TODO: Add in Phase 2
        "lines_added": 0,    # TODO: Add in Phase 2
        "lines_removed": 0,   # TODO: Add in Phase 2
        "authors": authors,
        "commit_messages": [c.get("message", "") for c in commits[:10]],  # First 10
    }


def analyze_git_activity(
    workspace_root: Path,
    since_timestamp: Optional[datetime] = None
) -> Dict[str, Any]:
    """
    Analyze git activity since last snapshot.
    
    Args:
        workspace_root: Root workspace path
        since_timestamp: Timestamp to analyze since (defaults to 24 hours ago)
    
    Returns:
        Dict with git activity data
    """
    if since_timestamp is None:
        from datetime import timedelta
        since_timestamp = datetime.now() - timedelta(hours=24)
    
    # Check if workspace is a git repository
    git_dir = workspace_root / ".git"
    if not git_dir.exists():
        logger.warning(f"Not a git repository: {workspace_root}")
        return {
            "error": "Not a git repository",
            "metrics": {},
        }
    
    try:
        commits = get_commits_since(since_timestamp, workspace_root)
        metrics = calculate_git_metrics(commits)
        
        return {
            "since_timestamp": since_timestamp.isoformat(),
            "metrics": metrics,
            "commits": commits,
        }
    
    except Exception as e:
        logger.error(f"Error analyzing git activity: {e}")
        return {
            "error": str(e),
            "metrics": {},
        }

