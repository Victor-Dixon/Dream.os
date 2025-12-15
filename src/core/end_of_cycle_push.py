"""
End of Cycle Push Protocol - Prepare and push changes before overnight runs
<!-- SSOT Domain: infrastructure -->


Ensures all work is committed and pushed at end of each day cycle
before autonomous overnight runs begin.

Author: Agent-1 (Integration & Core Systems)
Date: 2025-01-27
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime, timezone, date
from typing import Dict, Any, List, Optional
from .daily_cycle_tracker import DailyCycleTracker


class EndOfCyclePush:
    """
    Manages end-of-cycle push protocol.
    
    Ensures all changes are committed and pushed before overnight runs.
    """
    
    def __init__(self, agent_id: str):
        """
        Initialize end-of-cycle push handler.
        
        Args:
            agent_id: Agent identifier (e.g., "Agent-1")
        """
        self.agent_id = agent_id
        self.workspace = Path(f"agent_workspaces/{agent_id}")
        self.tracker = DailyCycleTracker(agent_id)
    
    def prepare_for_push(self) -> Dict[str, Any]:
        """
        Prepare for end-of-cycle push.
        
        Returns:
            Dictionary with push preparation status
        """
        today = date.today().isoformat()
        self.tracker.start_new_day()
        
        # Check git status
        status_result = self._check_git_status()
        
        # Check for uncommitted changes
        uncommitted = self._get_uncommitted_files()
        
        # Check for unpushed commits
        unpushed = self._get_unpushed_commits()
        
        # Mark ready for push
        self.tracker.mark_ready_for_push()
        
        return {
            "date": today,
            "uncommitted_files": uncommitted,
            "unpushed_commits": unpushed,
            "has_changes": len(uncommitted) > 0 or len(unpushed) > 0,
            "ready_for_push": True,
            "status": status_result
        }
    
    def execute_push(self, commit_message: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute end-of-cycle push.
        
        Args:
            commit_message: Optional custom commit message
            
        Returns:
            Dictionary with push results
        """
        today = date.today().isoformat()
        summary = self.tracker.get_today_summary()
        
        # Stage all changes
        try:
            subprocess.run(['git', 'add', '-A'], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            return {
                "success": False,
                "error": f"Failed to stage changes: {e}",
                "stage": "staging"
            }
        
        # Commit if there are changes
        uncommitted = self._get_uncommitted_files()
        if uncommitted:
            commit_msg = commit_message or (
                f"Cycle {today}: {summary.get('tasks_completed', 0)} tasks, "
                f"{summary.get('points_earned', 0)} pts, "
                f"{summary.get('interactions', 0)} interactions"
            )
            
            try:
                subprocess.run(
                    ['git', 'commit', '-m', commit_msg],
                    check=True,
                    capture_output=True
                )
                self.tracker.record_commit()
            except subprocess.CalledProcessError as e:
                return {
                    "success": False,
                    "error": f"Failed to commit: {e}",
                    "stage": "committing"
                }
        
        # Push to remote
        unpushed = self._get_unpushed_commits()
        if unpushed:
            try:
                subprocess.run(
                    ['git', 'push'],
                    check=True,
                    capture_output=True
                )
                self.tracker.mark_pushed()
            except subprocess.CalledProcessError as e:
                return {
                    "success": False,
                    "error": f"Failed to push: {e}",
                    "stage": "pushing"
                }
        
        return {
            "success": True,
            "date": today,
            "committed": len(uncommitted) > 0,
            "pushed": len(unpushed) > 0,
            "summary": summary
        }
    
    def _check_git_status(self) -> str:
        """Check git status."""
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return "Error checking git status"
    
    def _get_uncommitted_files(self) -> List[str]:
        """Get list of uncommitted files."""
        try:
            result = subprocess.run(
                ['git', 'diff', '--name-only'],
                capture_output=True,
                text=True,
                check=True
            )
            staged = subprocess.run(
                ['git', 'diff', '--cached', '--name-only'],
                capture_output=True,
                text=True,
                check=True
            )
            return list(set(result.stdout.strip().split('\n') + 
                          staged.stdout.strip().split('\n'))) if result.stdout.strip() or staged.stdout.strip() else []
        except subprocess.CalledProcessError:
            return []
    
    def _get_unpushed_commits(self) -> List[str]:
        """Get list of unpushed commits."""
        try:
            result = subprocess.run(
                ['git', 'log', '--oneline', 'origin/main..HEAD'],
                capture_output=True,
                text=True,
                check=True
            )
            return [line for line in result.stdout.strip().split('\n') if line]
        except subprocess.CalledProcessError:
            return []

