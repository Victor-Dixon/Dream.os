"""
Status Service - Agent Cellphone V2
===================================

SSOT Domain: discord

Core service for reading and managing agent status files.

Features:
- Async/sync status file reading
- TTL-based caching with memory limits
- Data normalization and validation
- File existence and error handling

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import json
import logging
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

class StatusCache:
    """TTL-based cache for agent status data."""

    def __init__(self, ttl_seconds: int = 30, max_size: int = 20):
        self.ttl_seconds = ttl_seconds
        self.max_size = max_size
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.timestamps: Dict[str, datetime] = {}

    def is_expired(self, agent_id: str) -> bool:
        """Check if cached data for agent is expired."""
        if agent_id not in self.timestamps:
            return True

        expires_at = self.timestamps[agent_id] + timedelta(seconds=self.ttl_seconds)
        return datetime.now() > expires_at

    def get(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get cached data if not expired."""
        if self.is_expired(agent_id):
            return None
        return self.cache.get(agent_id)

    def set(self, agent_id: str, data: Dict[str, Any]) -> None:
        """Set cached data with timestamp."""
        # Implement LRU-style eviction if over max size
        if len(self.cache) >= self.max_size:
            oldest_agent = min(self.timestamps.keys(),
                             key=lambda k: self.timestamps[k])
            del self.cache[oldest_agent]
            del self.timestamps[oldest_agent]

        self.cache[agent_id] = data
        self.timestamps[agent_id] = datetime.now()

    def clear(self) -> None:
        """Clear all cached data."""
        self.cache.clear()
        self.timestamps.clear()

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "cached_agents": len(self.cache),
            "max_size": self.max_size,
            "ttl_seconds": self.ttl_seconds,
            "oldest_cache_age": self._get_oldest_age()
        }

    def _get_oldest_age(self) -> Optional[float]:
        """Get age of oldest cached item in seconds."""
        if not self.timestamps:
            return None

        oldest_time = min(self.timestamps.values())
        return (datetime.now() - oldest_time).total_seconds()

class StatusDataNormalizer:
    """Normalize and validate status data structure."""

    DEFAULT_STATUS = {
        "agent_id": "Unknown",
        "agent_name": "Unknown Agent",
        "status": "UNKNOWN",
        "current_phase": "UNKNOWN",
        "last_updated": "Unknown",
        "current_mission": "No active mission",
        "mission_priority": "LOW",
        "current_tasks": [],
        "completed_tasks": [],
        "achievements": [],
        "next_actions": []
    }

    @staticmethod
    def normalize(data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize status data to ensure consistent structure."""
        if not isinstance(data, dict):
            logger.warning(f"Invalid status data type: {type(data)}")
            return StatusDataNormalizer.DEFAULT_STATUS.copy()

        normalized = StatusDataNormalizer.DEFAULT_STATUS.copy()
        normalized.update(data)

        # Ensure lists are actually lists
        for list_field in ["current_tasks", "completed_tasks", "achievements", "next_actions"]:
            if not isinstance(normalized.get(list_field), list):
                normalized[list_field] = []

        # Validate and normalize status values
        if normalized.get("status") not in ["ACTIVE_AGENT_MODE", "INACTIVE", "UNKNOWN"]:
            normalized["status"] = "UNKNOWN"

        if normalized.get("mission_priority") not in ["CRITICAL", "HIGH", "ACTIVE", "MEDIUM", "LOW"]:
            normalized["mission_priority"] = "LOW"

        return normalized

class StatusFileReader:
    """Handle reading and parsing of status JSON files."""

    def __init__(self, workspace_dir: Path):
        self.workspace_dir = workspace_dir
        self.executor = ThreadPoolExecutor(max_workers=4)

    def read_file_sync(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Synchronously read status file for agent."""
        status_file = self.workspace_dir / agent_id / "status.json"

        if not status_file.exists():
            logger.debug(f"Status file not found: {status_file}")
            return None

        try:
            with open(status_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.debug(f"Successfully read status for {agent_id}")
                return data
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Error reading status file for {agent_id}: {e}")
            return None

    async def read_file_async(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Asynchronously read status file for agent."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self.read_file_sync, agent_id)

class StatusService:
    """
    Service for reading and managing agent status files.
    """

    def __init__(self, workspace_dir: str = "agent_workspaces", cache_ttl: int = 30):
        self.workspace_dir = Path(workspace_dir)
        self.cache = StatusCache(cache_ttl)
        self.reader = StatusFileReader(self.workspace_dir)
        self.normalizer = StatusDataNormalizer()

    async def read_agent_status_async(self, agent_id: str, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        """
        Read status for a specific agent asynchronously.

        Args:
            agent_id: Agent identifier (e.g., "Agent-1")
            force_refresh: Force cache refresh

        Returns:
            Normalized status data or None if not found
        """
        # Check cache first (unless forced refresh)
        if not force_refresh:
            cached_data = self.cache.get(agent_id)
            if cached_data:
                return cached_data

        # Read from file
        raw_data = await self.reader.read_file_async(agent_id)
        if not raw_data:
            return None

        # Normalize and cache
        normalized_data = self.normalizer.normalize(raw_data)
        self.cache.set(agent_id, normalized_data)

        return normalized_data

    def read_agent_status(self, agent_id: str, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        """
        Read status for a specific agent synchronously.

        Args:
            agent_id: Agent identifier (e.g., "Agent-1")
            force_refresh: Force cache refresh

        Returns:
            Normalized status data or None if not found
        """
        # Check cache first (unless forced refresh)
        if not force_refresh:
            cached_data = self.cache.get(agent_id)
            if cached_data:
                return cached_data

        # Read from file
        raw_data = self.reader.read_file_sync(agent_id)
        if not raw_data:
            return None

        # Normalize and cache
        normalized_data = self.normalizer.normalize(raw_data)
        self.cache.set(agent_id, normalized_data)

        return normalized_data

    async def read_all_statuses_async(self) -> Dict[str, Dict[str, Any]]:
        """
        Read status for all agents asynchronously.

        Returns:
            Dictionary mapping agent_id to status data
        """
        # Assume agents 1-8 exist (standard swarm)
        agent_ids = [f"Agent-{i}" for i in range(1, 9)]

        tasks = [self.read_agent_status_async(agent_id) for agent_id in agent_ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        all_statuses = {}
        for agent_id, result in zip(agent_ids, results):
            if isinstance(result, Exception):
                logger.warning(f"Error reading status for {agent_id}: {result}")
                continue
            if result:
                all_statuses[agent_id] = result

        return all_statuses

    def read_all_statuses(self) -> Dict[str, Dict[str, Any]]:
        """
        Read status for all agents synchronously.

        Returns:
            Dictionary mapping agent_id to status data
        """
        # Assume agents 1-8 exist (standard swarm)
        agent_ids = [f"Agent-{i}" for i in range(1, 9)]

        all_statuses = {}
        for agent_id in agent_ids:
            status = self.read_agent_status(agent_id)
            if status:
                all_statuses[agent_id] = status

        return all_statuses

    def clear_cache(self) -> None:
        """Clear all cached status data."""
        self.cache.clear()
        logger.info("Status cache cleared")

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return self.cache.get_stats()

# Global service instance
status_service = StatusService()

__all__ = [
    "StatusService",
    "StatusCache",
    "StatusDataNormalizer",
    "StatusFileReader",
    "status_service"
]