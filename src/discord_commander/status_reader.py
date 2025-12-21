"""
Discord Status Reader
=====================

Reads and parses agent status.json files for Discord display.

Features:
- Read all agent status files
- Cache with TTL (30 seconds)
- Normalize data structure
- Handle missing/malformed files

Author: Agent-5
Created: 2025-10-11
License: MIT
"""

import json
import logging
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class StatusReader:
    """Read and cache agent status.json files."""

    def __init__(self, workspace_dir: str = "agent_workspaces", cache_ttl: int = 30):
        """Initialize status reader with memory leak prevention.

        Args:
            workspace_dir: Directory containing agent workspaces
            cache_ttl: Cache time-to-live in seconds
        """
        self.workspace_dir = Path(workspace_dir)
        self.cache_ttl = cache_ttl
        self.cache: dict[str, dict[str, Any]] = {}
        self.cache_timestamps: dict[str, datetime] = {}
        self.max_cache_size = 20  # Max 20 agents (8 main + 12 buffer)

    async def read_agent_status_async(self, agent_id: str, force_refresh: bool = False) -> dict[str, Any] | None:
        """Read status for a specific agent (async version).

        Args:
            agent_id: Agent identifier (e.g., "Agent-1")
            force_refresh: If True, bypass cache and read from file

        Returns:
            Agent status data or None if not found
        """
        status_file = self.workspace_dir / agent_id / "status.json"
        
        # Use asyncio.to_thread for file existence check
        try:
            exists = await asyncio.to_thread(status_file.exists)
            if not exists:
                logger.warning(f"Status file not found for {agent_id}: {status_file}")
                return None
        except Exception as e:
            logger.error(f"Error checking file existence for {agent_id}: {e}")
            return None
        
        # Check file modification time if cached
        if not force_refresh and agent_id in self.cache:
            cached_time = self.cache_timestamps.get(agent_id)
            if cached_time:
                # Check if file was modified since cache
                try:
                    # Use asyncio.to_thread for file stat
                    file_stat = await asyncio.to_thread(status_file.stat)
                    file_mtime = datetime.fromtimestamp(file_stat.st_mtime)
                    if (datetime.now() - cached_time).total_seconds() < self.cache_ttl:
                        # File not modified, return cache
                        if file_mtime <= cached_time:
                            return self.cache[agent_id]
                        # File was modified, need to refresh
                        logger.debug(f"Status file modified for {agent_id}, refreshing cache")
                except Exception:
                    pass  # If can't check mtime, continue to read file

        # Read from file using asyncio.to_thread
        try:
            # Use asyncio.to_thread for file I/O
            def _read_file():
                with open(status_file, encoding="utf-8") as f:
                    return json.load(f)
            
            data = await asyncio.to_thread(_read_file)

            # Normalize data
            normalized = self._normalize_status(data)

            # Update cache with size limit (prevent memory leak)
            if len(self.cache) >= self.max_cache_size and agent_id not in self.cache:
                # Evict oldest cached agent
                oldest_agent = min(self.cache_timestamps, key=self.cache_timestamps.get)
                del self.cache[oldest_agent]
                del self.cache_timestamps[oldest_agent]

            self.cache[agent_id] = normalized
            self.cache_timestamps[agent_id] = datetime.now()

            return normalized

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {status_file}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error reading {status_file}: {e}")
            return None

    def read_agent_status(self, agent_id: str, force_refresh: bool = False) -> dict[str, Any] | None:
        """Read status for a specific agent (synchronous version for backward compatibility).

        Args:
            agent_id: Agent identifier (e.g., "Agent-1")
            force_refresh: If True, bypass cache and read from file

        Returns:
            Agent status data or None if not found
        """
        status_file = self.workspace_dir / agent_id / "status.json"
        
        if not status_file.exists():
            logger.warning(f"Status file not found for {agent_id}: {status_file}")
            return None
        
        # Check file modification time if cached
        if not force_refresh and agent_id in self.cache:
            cached_time = self.cache_timestamps.get(agent_id)
            if cached_time:
                # Check if file was modified since cache
                try:
                    file_mtime = datetime.fromtimestamp(status_file.stat().st_mtime)
                    if (datetime.now() - cached_time).total_seconds() < self.cache_ttl:
                        # File not modified, return cache
                        if file_mtime <= cached_time:
                            return self.cache[agent_id]
                        # File was modified, need to refresh
                        logger.debug(f"Status file modified for {agent_id}, refreshing cache")
                except Exception:
                    pass  # If can't check mtime, continue to read file

        # Read from file
        try:
            with open(status_file, encoding="utf-8") as f:
                data = json.load(f)

            # Normalize data
            normalized = self._normalize_status(data)

            # Update cache with size limit (prevent memory leak)
            if len(self.cache) >= self.max_cache_size and agent_id not in self.cache:
                # Evict oldest cached agent
                oldest_agent = min(self.cache_timestamps, key=self.cache_timestamps.get)
                del self.cache[oldest_agent]
                del self.cache_timestamps[oldest_agent]

            self.cache[agent_id] = normalized
            self.cache_timestamps[agent_id] = datetime.now()

            return normalized

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {status_file}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error reading {status_file}: {e}")
            return None

    async def read_all_statuses_async(self) -> dict[str, dict[str, Any]]:
        """Read status for all agents (async version - only main 8 agents, not role workspaces).

        Returns:
            Dictionary of agent_id -> status_data
        """
        statuses = {}

        # Check if workspace directory exists using asyncio.to_thread
        try:
            exists = await asyncio.to_thread(self.workspace_dir.exists)
            if not exists:
                logger.error(f"Workspace directory not found: {self.workspace_dir}")
                return statuses
        except Exception as e:
            logger.error(f"Error checking workspace directory: {e}")
            return statuses

        # Read only the 8 main agent workspaces (Agent-1 through Agent-8)
        # Skip specialized role workspaces (Agent-SRC-1, Agent-SDA-3, etc.)
        for i in range(1, 9):
            agent_id = f"Agent-{i}"
            agent_dir = self.workspace_dir / agent_id

            # Use asyncio.to_thread for directory checks
            try:
                exists = await asyncio.to_thread(agent_dir.exists)
                is_dir = await asyncio.to_thread(agent_dir.is_dir) if exists else False
                
                if exists and is_dir:
                    status = await self.read_agent_status_async(agent_id)
                    if status:
                        statuses[agent_id] = status
            except Exception as e:
                logger.error(f"Error checking directory for {agent_id}: {e}")
                continue

        return statuses

    def read_all_statuses(self) -> dict[str, dict[str, Any]]:
        """Read status for all agents (synchronous version for backward compatibility).

        Returns:
            Dictionary of agent_id -> status_data
        """
        statuses = {}

        # Check if workspace directory exists
        if not self.workspace_dir.exists():
            logger.error(f"Workspace directory not found: {self.workspace_dir}")
            return statuses

        # Read only the 8 main agent workspaces (Agent-1 through Agent-8)
        # Skip specialized role workspaces (Agent-SRC-1, Agent-SDA-3, etc.)
        for i in range(1, 9):
            agent_id = f"Agent-{i}"
            agent_dir = self.workspace_dir / agent_id

            if agent_dir.exists() and agent_dir.is_dir():
                status = self.read_agent_status(agent_id)
                if status:
                    statuses[agent_id] = status

        return statuses

    def _normalize_status(self, data: dict[str, Any]) -> dict[str, Any]:
        """Normalize status data to standard format.

        Args:
            data: Raw status.json data

        Returns:
            Normalized status data
        """
        # Extract common fields with defaults
        normalized = {
            "agent_id": data.get("agent_id", "Unknown"),
            "agent_name": data.get("agent_name", "Unknown Agent"),
            "status": data.get("status", "UNKNOWN"),
            "current_phase": data.get("current_phase", "N/A"),
            "last_updated": data.get("last_updated", "Unknown"),
            "current_mission": data.get("current_mission", "No mission assigned"),
            "mission_priority": data.get("mission_priority", "NORMAL"),
            "current_tasks": data.get("current_tasks", []),
            "completed_tasks": data.get("completed_tasks", []),
            "achievements": data.get("achievements", []),
            "next_actions": data.get("next_actions", []),
        }

        # Add optional fields if present
        if "sprint_info" in data:
            normalized["sprint_info"] = data["sprint_info"]

        if "points_summary" in data:
            normalized["points_summary"] = data["points_summary"]

        if "coordinate_position" in data:
            normalized["coordinate_position"] = data["coordinate_position"]

        if "team_assignment" in data:
            normalized["team_assignment"] = data["team_assignment"]

        # Extract points from various possible locations
        points = None
        if "points_summary" in data and isinstance(data["points_summary"], dict):
            points = data["points_summary"].get("legendary_total") or data["points_summary"].get(
                "total_points"
            )
        elif "sprint_info" in data and isinstance(data["sprint_info"], dict):
            points = data["sprint_info"].get("points_earned") or data["sprint_info"].get(
                "points_completed"
            )

        if points:
            normalized["points"] = points

        return normalized

    def clear_cache(self):
        """Clear the status cache."""
        self.cache.clear()
        self.cache_timestamps.clear()
        logger.info("Status cache cleared")

    def get_cache_stats(self) -> dict[str, Any]:
        """Get cache statistics.

        Returns:
            Cache statistics
        """
        return {
            "cached_agents": len(self.cache),
            "cache_ttl": self.cache_ttl,
            "oldest_cache": min(self.cache_timestamps.values()) if self.cache_timestamps else None,
            "newest_cache": max(self.cache_timestamps.values()) if self.cache_timestamps else None,
        }
