"""
Agent Status Reader
===================

Unified status.json reading with caching and error handling.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Architecture: Agent-2 (Architecture & Design Specialist)
Created: 2025-12-31
V2 Compliant: Yes (<400 lines, functions <30 lines)

<!-- SSOT Domain: core -->
"""

import json
import logging
import asyncio
from pathlib import Path
from typing import Dict, Optional, Any, List

from .cache import StatusCache

logger = logging.getLogger(__name__)


class AgentStatusReader:
    """Unified reader for agent status.json files."""
    
    def __init__(self, workspace_root: Optional[Path] = None, cache_ttl: float = 5.0):
        """
        Initialize agent status reader.
        
        Args:
            workspace_root: Root workspace path (defaults to current directory)
            cache_ttl: Cache time-to-live in seconds (default: 5.0)
        """
        if workspace_root is None:
            workspace_root = Path.cwd()
        self.workspace_root = Path(workspace_root)
        self.cache = StatusCache(cache_ttl=cache_ttl)
    
    def read_status(
        self,
        agent_id: str,
        use_cache: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        Read agent status.json file.
        
        Args:
            agent_id: Agent ID (e.g., "Agent-1", "Agent-2")
            use_cache: Whether to use cache (default: True)
        
        Returns:
            Status dictionary or None if not found/invalid
        """
        status_file = self.workspace_root / "agent_workspaces" / agent_id / "status.json"
        
        if not status_file.exists():
            logger.debug(f"Status file not found: {status_file}")
            return None
        
        # Check cache first
        if use_cache:
            cached = self.cache.get(agent_id, status_file)
            if cached is not None:
                return cached
        
        # Read from file
        try:
            with open(status_file, 'r', encoding='utf-8') as f:
                status = json.load(f)
            
            # Validate basic structure
            if not self._validate_status(status):
                logger.warning(f"Invalid status.json structure for {agent_id}")
                return None
            
            # Cache the result
            if use_cache:
                self.cache.set(agent_id, status_file, status)
            
            return status
        
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error for {agent_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error reading status for {agent_id}: {e}")
            return None
    
    def read_all_status(
        self,
        agent_ids: Optional[List[str]] = None,
        use_cache: bool = True
    ) -> Dict[str, Dict[str, Any]]:
        """
        Read status from all agents.
        
        Args:
            agent_ids: List of agent IDs (defaults to Agent-1 through Agent-8)
            use_cache: Whether to use cache (default: True)
        
        Returns:
            Dict mapping agent_id to status data
        """
        if agent_ids is None:
            agent_ids = [f"Agent-{i}" for i in range(1, 9)]
        
        agents = {}
        
        for agent_id in agent_ids:
            status = self.read_status(agent_id, use_cache=use_cache)
            if status:
                agents[agent_id] = status
        
        return agents
    
    def _validate_status(self, status: Dict[str, Any]) -> bool:
        """
        Validate status.json structure.
        
        Args:
            status: Status dictionary to validate
        
        Returns:
            True if valid, False otherwise
        """
        required_fields = ["agent_id", "agent_name", "status"]
        
        for field in required_fields:
            if field not in status:
                logger.warning(f"Missing required field: {field}")
                return False
        
        # Validate JSON is serializable
        try:
            json.dumps(status)
        except (TypeError, ValueError) as e:
            logger.error(f"Status not JSON serializable: {e}")
            return False
        
        return True
    
    def invalidate_cache(self, agent_id: Optional[str] = None) -> None:
        """
        Invalidate cache for agent(s).
        
        Args:
            agent_id: Specific agent ID or None for all
        """
        self.cache.invalidate(agent_id)
    
    async def read_status_async(
        self,
        agent_id: str,
        use_cache: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        Async version of read_status for use in async contexts.
        
        Args:
            agent_id: Agent ID (e.g., "Agent-1", "Agent-2")
            use_cache: Whether to use cache (default: True)
        
        Returns:
            Status dictionary or None if not found/invalid
        """
        # Use asyncio.to_thread for file I/O operations
        return await asyncio.to_thread(self.read_status, agent_id, use_cache)
    
    async def read_all_status_async(
        self,
        agent_ids: Optional[List[str]] = None,
        use_cache: bool = True
    ) -> Dict[str, Dict[str, Any]]:
        """
        Async version of read_all_status for use in async contexts.
        
        Args:
            agent_ids: List of agent IDs (defaults to Agent-1 through Agent-8)
            use_cache: Whether to use cache (default: True)
        
        Returns:
            Dict mapping agent_id to status data
        """
        if agent_ids is None:
            agent_ids = [f"Agent-{i}" for i in range(1, 9)]
        
        # Read all agents concurrently
        tasks = [
            self.read_status_async(agent_id, use_cache=use_cache)
            for agent_id in agent_ids
        ]
        results = await asyncio.gather(*tasks)
        
        agents = {}
        for agent_id, status in zip(agent_ids, results):
            if status:
                agents[agent_id] = status
        
        return agents


# Convenience functions for backward compatibility
def read_agent_status(
    agent_id: str,
    workspace_root: Optional[Path] = None
) -> Optional[Dict[str, Any]]:
    """
    Convenience function to read single agent status.
    
    Args:
        agent_id: Agent ID (e.g., "Agent-1")
        workspace_root: Root workspace path
    
    Returns:
        Status dictionary or None
    """
    reader = AgentStatusReader(workspace_root=workspace_root)
    return reader.read_status(agent_id)


def read_all_agent_status(
    workspace_root: Optional[Path] = None,
    agent_ids: Optional[List[str]] = None
) -> Dict[str, Dict[str, Any]]:
    """
    Convenience function to read all agent status.
    
    Args:
        workspace_root: Root workspace path
        agent_ids: List of agent IDs (defaults to Agent-1 through Agent-8)
    
    Returns:
        Dict mapping agent_id to status data
    """
    reader = AgentStatusReader(workspace_root=workspace_root)
    return reader.read_all_status(agent_ids=agent_ids)

