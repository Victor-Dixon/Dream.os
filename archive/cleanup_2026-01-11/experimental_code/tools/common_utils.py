#!/usr/bin/env python3
"""
Common Utilities
Shared utilities for status updates, git operations, and common patterns
"""

import json
import subprocess
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class StatusManager:
    """Manages agent status updates"""

    def __init__(self, agent_id: str = "Agent-7"):
        self.agent_id = agent_id
        self.status_file = Path(__file__).resolve().parents[1] / f"agent_workspaces/{agent_id}/status.json"

    def update_status(self, updates: Dict[str, Any]) -> bool:
        """
        Update status file with new information

        Args:
            updates: Dict of status updates

        Returns:
            Success status
        """
        try:
            # Load current status
            if self.status_file.exists():
                with open(self.status_file, 'r') as f:
                    status = json.load(f)
            else:
                status = self._get_default_status()

            # Apply updates
            status.update(updates)
            status["last_updated"] = datetime.now().isoformat()

            # Save updated status
            with open(self.status_file, 'w') as f:
                json.dump(status, f, indent=2)

            logger.info(f"✅ Status updated for {self.agent_id}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to update status: {e}")
            return False

    def _get_default_status(self) -> Dict[str, Any]:
        """Get default status structure"""
        return {
            "agent_id": self.agent_id,
            "agent_name": "Web Development Specialist",
            "status": "ACTIVE_AGENT_MODE",
            "current_phase": "TASK_EXECUTION",
            "last_updated": datetime.now().isoformat(),
            "current_mission": "Web Development & Integration",
            "mission_priority": "HIGH",
            "current_tasks": [],
            "completed_tasks": [],
            "achievements": [],
            "next_actions": []
        }

    def add_completed_task(self, task: str) -> bool:
        """Add a completed task"""
        return self.update_status({
            "completed_tasks": self._get_current_status().get("completed_tasks", []) + [task]
        })

    def add_achievement(self, achievement: str) -> bool:
        """Add an achievement"""
        return self.update_status({
            "achievements": self._get_current_status().get("achievements", []) + [achievement]
        })

    def _get_current_status(self) -> Dict[str, Any]:
        """Get current status"""
        try:
            if self.status_file.exists():
                with open(self.status_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return self._get_default_status()

class GitManager:
    """Manages git operations"""

    def __init__(self, repo_path: Optional[str] = None):
        self.repo_path = Path(repo_path) if repo_path else Path(__file__).resolve().parents[1]

    def add_files(self, files: list) -> bool:
        """
        Add files to git staging

        Args:
            files: List of file paths to add

        Returns:
            Success status
        """
        try:
            cmd = ["git", "add"] + files
            result = subprocess.run(cmd, cwd=self.repo_path, capture_output=True, text=True)

            if result.returncode == 0:
                logger.info(f"✅ Added {len(files)} files to git")
                return True
            else:
                logger.error(f"❌ Git add failed: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"❌ Git add error: {e}")
            return False

    def commit(self, message: str) -> bool:
        """
        Commit staged changes

        Args:
            message: Commit message

        Returns:
            Success status
        """
        try:
            cmd = ["git", "commit", "-m", message]
            result = subprocess.run(cmd, cwd=self.repo_path, capture_output=True, text=True)

            if result.returncode == 0:
                logger.info("✅ Changes committed to git")
                return True
            else:
                logger.error(f"❌ Git commit failed: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"❌ Git commit error: {e}")
            return False

    def push(self, remote: str = "origin", branch: str = "main") -> bool:
        """
        Push commits to remote

        Args:
            remote: Remote name
            branch: Branch name

        Returns:
            Success status
        """
        try:
            cmd = ["git", "push", remote, branch]
            result = subprocess.run(cmd, cwd=self.repo_path, capture_output=True, text=True)

            if result.returncode == 0:
                logger.info(f"✅ Pushed to {remote}/{branch}")
                return True
            else:
                logger.error(f"❌ Git push failed: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"❌ Git push error: {e}")
            return False

class ErrorHandler:
    """Common error handling utilities"""

    @staticmethod
    def handle_ssh_error(operation: str, error: Exception) -> str:
        """Handle SSH-related errors"""
        return f"SSH operation '{operation}' failed: {str(error)}"

    @staticmethod
    def handle_wp_cli_error(command: str, error: str) -> str:
        """Handle WordPress CLI errors"""
        return f"WP-CLI command '{command}' failed: {error}"

    @staticmethod
    def handle_http_error(url: str, error: Exception) -> str:
        """Handle HTTP request errors"""
        return f"HTTP request to '{url}' failed: {str(error)}"

    @staticmethod
    def log_and_continue(operation: str, error: Exception, level: str = "error") -> None:
        """Log error and continue execution"""
        message = f"{operation} encountered error: {str(error)}"

        if level == "error":
            logger.error(message)
        elif level == "warning":
            logger.warning(message)
        elif level == "info":
            logger.info(message)

def safe_execute(func, *args, **kwargs):
    """
    Safely execute a function with error handling

    Args:
        func: Function to execute
        *args: Positional arguments
        **kwargs: Keyword arguments

    Returns:
        Tuple of (success, result, error)
    """
    try:
        result = func(*args, **kwargs)
        return True, result, None
    except Exception as e:
        return False, None, str(e)

def validate_required_params(params: Dict[str, Any], required: List[str]) -> Tuple[bool, str]:
    """
    Validate required parameters are present

    Args:
        params: Parameters dict
        required: List of required parameter names

    Returns:
        Tuple of (valid, error_message)
    """
    missing = [key for key in required if key not in params or params[key] is None]

    if missing:
        return False, f"Missing required parameters: {', '.join(missing)}"

    return True, ""

# Convenience functions
def update_agent_status(agent_id: str, updates: Dict[str, Any]) -> bool:
    """Convenience function to update agent status"""
    manager = StatusManager(agent_id)
    return manager.update_status(updates)

def git_commit_and_push(files: list, message: str) -> bool:
    """Convenience function for git operations"""
    manager = GitManager()

    if not manager.add_files(files):
        return False

    if not manager.commit(message):
        return False

    return manager.push()