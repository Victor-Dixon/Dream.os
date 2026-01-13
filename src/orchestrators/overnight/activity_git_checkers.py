#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Activity Git Checkers - Modular Activity Detection
==================================================

Git activity detection components extracted from monolithic detector.

V2 Compliant: Modular git activity checking
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-08
"""

import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class GitActivityChecker:
    """Checks git activity indicators."""

    def __init__(self, workspace_root: Path):
        """Initialize git checker."""
        self.workspace_root = workspace_root

    def check_git_commits(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check recent git commits by agent."""
        try:
            # Run git log to find commits by this agent
            cmd = [
                "git", "log", "--oneline", "--since=1.day.ago",
                "--grep", f"Agent-{agent_id}",
                "--author", f"Agent-{agent_id}"
            ]

            result = subprocess.run(
                cmd,
                cwd=self.workspace_root,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0:
                # Try alternative patterns
                cmd = [
                    "git", "log", "--oneline", "--since=1.day.ago",
                    "--grep", agent_id
                ]

                result = subprocess.run(
                    cmd,
                    cwd=self.workspace_root,
                    capture_output=True,
                    text=True,
                    timeout=10
                )

            if result.returncode == 0 and result.stdout.strip():
                lines = result.stdout.strip().split('\n')
                commit_count = len(lines)

                # Get latest commit info
                latest_commit = lines[0] if lines else ""
                commit_hash = latest_commit.split()[0] if latest_commit else ""

                return {
                    'commit_count': commit_count,
                    'latest_commit_hash': commit_hash,
                    'latest_commit_summary': latest_commit,
                    'has_recent_commits': commit_count > 0
                }

        except subprocess.TimeoutExpired:
            logger.warning(f"Git log timeout for {agent_id}")
        except Exception as e:
            logger.error(f"Error checking git commits for {agent_id}: {e}")

        return None

    def check_git_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check git status for uncommitted changes."""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.workspace_root,
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                lines = result.stdout.strip().split('\n') if result.stdout.strip() else []
                modified_files = [line for line in lines if line.strip()]

                # Look for agent-specific files
                agent_files = [f for f in modified_files if agent_id in f]

                return {
                    'total_modified': len(modified_files),
                    'agent_modified': len(agent_files),
                    'has_uncommitted_changes': len(modified_files) > 0,
                    'agent_has_uncommitted': len(agent_files) > 0
                }

        except subprocess.TimeoutExpired:
            logger.warning(f"Git status timeout for {agent_id}")
        except Exception as e:
            logger.error(f"Error checking git status for {agent_id}: {e}")

        return None


__all__ = ["GitActivityChecker"]