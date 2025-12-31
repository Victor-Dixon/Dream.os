"""
Agent Status File Watcher
=========================

File change detection for agent status.json files.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Architecture: Agent-2 (Architecture & Design Specialist)
Created: 2025-12-31
V2 Compliant: Yes (<400 lines, functions <30 lines)

<!-- SSOT Domain: core -->
"""

import logging
import time
from pathlib import Path
from typing import Dict, Optional, Callable, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class StatusFileWatcher:
    """
    Watches agent status.json files for changes.
    
    Uses polling-based detection (mtime comparison) for cross-platform
    compatibility. Pure utility - no async, no Discord dependencies.
    """
    
    def __init__(
        self,
        workspace_root: Optional[Path] = None,
        check_interval: float = 5.0,
        agent_ids: Optional[List[str]] = None
    ):
        """
        Initialize file watcher.
        
        Args:
            workspace_root: Root workspace path (defaults to current directory)
            check_interval: Polling interval in seconds (default: 5.0)
            agent_ids: List of agent IDs to watch (default: Agent-1 through Agent-8)
        """
        if workspace_root is None:
            workspace_root = Path.cwd()
        self.workspace_root = Path(workspace_root)
        self.check_interval = check_interval
        self.last_modified: Dict[str, float] = {}
        self.last_status: Dict[str, Dict[str, Any]] = {}
        self.callbacks: Dict[str, List[Callable]] = {}
        
        # Default agent IDs if not specified
        if agent_ids is None:
            agent_ids = [f"Agent-{i}" for i in range(1, 9)]
        self.agent_ids = agent_ids
    
    def register_callback(
        self,
        agent_id: str,
        callback: Callable[[str, Dict[str, Any], Dict[str, Any]], None]
    ) -> None:
        """
        Register callback for agent status changes.
        
        Args:
            agent_id: Agent ID to watch (e.g., "Agent-1")
            callback: Function(agent_id, new_status, changes) -> None
        """
        if agent_id not in self.callbacks:
            self.callbacks[agent_id] = []
        self.callbacks[agent_id].append(callback)
    
    def unregister_callback(
        self,
        agent_id: str,
        callback: Optional[Callable] = None
    ) -> None:
        """
        Unregister callback(s) for agent.
        
        Args:
            agent_id: Agent ID
            callback: Specific callback to remove, or None to remove all
        """
        if agent_id in self.callbacks:
            if callback:
                if callback in self.callbacks[agent_id]:
                    self.callbacks[agent_id].remove(callback)
            else:
                self.callbacks[agent_id].clear()
    
    def check_changes(self) -> Dict[str, Dict[str, Any]]:
        """
        Check all watched files for changes.
        
        Returns:
            Dict mapping agent_id -> {"status": dict, "changes": dict}
        """
        changes_detected: Dict[str, Dict[str, Any]] = {}
        
        for agent_id in self.agent_ids:
            status_file = self.workspace_root / agent_id / "status.json"
            
            if not status_file.exists():
                continue
            
            try:
                current_mtime = status_file.stat().st_mtime
                last_mtime = self.last_modified.get(agent_id, 0)
                
                if current_mtime > last_mtime:
                    # File changed - read new status
                    new_status = self._read_status_file(status_file)
                    if not new_status:
                        continue
                    
                    old_status = self.last_status.get(agent_id, {})
                    changes = self._detect_changes(old_status, new_status)
                    
                    if changes:
                        changes_detected[agent_id] = {
                            "status": new_status,
                            "changes": changes
                        }
                        
                        # Trigger callbacks
                        self._trigger_callbacks(agent_id, new_status, changes)
                    
                    self.last_modified[agent_id] = current_mtime
                    self.last_status[agent_id] = new_status.copy()
            
            except (OSError, FileNotFoundError) as e:
                logger.debug(f"Error checking {agent_id}: {e}")
            except Exception as e:
                logger.warning(f"Unexpected error checking {agent_id}: {e}")
        
        return changes_detected
    
    def _read_status_file(self, status_file: Path) -> Optional[Dict[str, Any]]:
        """Read status.json file with error handling."""
        try:
            import json
            with open(status_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.warning(f"JSON decode error in {status_file}: {e}")
            return None
        except Exception as e:
            logger.warning(f"Error reading {status_file}: {e}")
            return None
    
    def _detect_changes(
        self,
        old_status: Dict[str, Any],
        new_status: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Detect significant status changes.
        
        Args:
            old_status: Previous status dict
            new_status: Current status dict
        
        Returns:
            Dict of detected changes
        """
        changes: Dict[str, Any] = {}
        
        # Track key fields
        key_fields = ["status", "current_phase", "current_mission", "points_earned"]
        for field in key_fields:
            old_val = old_status.get(field)
            new_val = new_status.get(field)
            if old_val != new_val:
                changes[field.replace("current_", "")] = {
                    "old": old_val,
                    "new": new_val
                }
        
        # Track list changes (completed_tasks, current_tasks)
        for list_field in ["completed_tasks", "current_tasks"]:
            old_set = set(old_status.get(list_field, []))
            new_set = set(new_status.get(list_field, []))
            added = new_set - old_set
            removed = old_set - new_set
            if added or removed:
                changes[list_field] = {
                    "added": list(added),
                    "removed": list(removed)
                }
        
        return changes
    
    def _trigger_callbacks(
        self,
        agent_id: str,
        new_status: Dict[str, Any],
        changes: Dict[str, Any]
    ) -> None:
        """Trigger registered callbacks for agent."""
        if agent_id in self.callbacks:
            for callback in self.callbacks[agent_id]:
                try:
                    callback(agent_id, new_status, changes)
                except Exception as e:
                    logger.error(f"Error in callback for {agent_id}: {e}")
    
    def initialize_baselines(self) -> None:
        """
        Initialize baselines by reading current status of all agents.
        
        Call this before starting to watch to establish baseline state.
        """
        for agent_id in self.agent_ids:
            status_file = self.workspace_root / agent_id / "status.json"
            
            if not status_file.exists():
                continue
            
            try:
                current_mtime = status_file.stat().st_mtime
                status = self._read_status_file(status_file)
                if status:
                    self.last_modified[agent_id] = current_mtime
                    self.last_status[agent_id] = status.copy()
            except Exception as e:
                logger.debug(f"Error initializing baseline for {agent_id}: {e}")
    
    def get_last_modified(self, agent_id: str) -> Optional[float]:
        """
        Get last modified timestamp for agent.
        
        Args:
            agent_id: Agent ID
        
        Returns:
            Unix timestamp or None if not tracked
        """
        return self.last_modified.get(agent_id)
    
    def get_last_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Get last known status for agent.
        
        Args:
            agent_id: Agent ID
        
        Returns:
            Status dict or None if not tracked
        """
        return self.last_status.get(agent_id)
    
    def reset(self, agent_id: Optional[str] = None) -> None:
        """
        Reset tracking state for agent(s).
        
        Args:
            agent_id: Specific agent ID, or None for all agents
        """
        if agent_id:
            self.last_modified.pop(agent_id, None)
            self.last_status.pop(agent_id, None)
        else:
            self.last_modified.clear()
            self.last_status.clear()


def create_watcher(
    workspace_root: Optional[Path] = None,
    check_interval: float = 5.0,
    agent_ids: Optional[List[str]] = None
) -> StatusFileWatcher:
    """
    Create and initialize a status file watcher.
    
    Args:
        workspace_root: Root workspace path
        check_interval: Polling interval in seconds
        agent_ids: List of agent IDs to watch
    
    Returns:
        Initialized watcher with baselines set
    """
    watcher = StatusFileWatcher(
        workspace_root=workspace_root,
        check_interval=check_interval,
        agent_ids=agent_ids
    )
    watcher.initialize_baselines()
    return watcher

