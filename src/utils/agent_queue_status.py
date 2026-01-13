#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Agent Queue Status Manager - Cursor Queue Buildup Prevention
=============================================================

Manages agent queue status to prevent Cursor queue buildup.
When an agent has many messages queued, new messages should skip PyAutoGUI
and go directly to inbox to prevent the agent from falling behind.

IMPORTANT: PyAutoGUI doesn't fail when queue is full - it successfully queues.
The problem is queue buildup: Agent-4 receives 7 messages while others get 1,
causing Agent-4 to fall behind. This system prevents adding MORE messages
to an already-long queue.

Usage:
    from src.utils.agent_queue_status import AgentQueueStatus
    
    # Mark agent as full
    AgentQueueStatus.mark_full("Agent-4")
    
    # Check if agent is full
    if AgentQueueStatus.is_full("Agent-4"):
        # Skip PyAutoGUI, use inbox
        pass
    
    # Mark agent as available
    AgentQueueStatus.mark_available("Agent-4")

Author: Agent-4 (Captain)
Date: 2025-11-27
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class AgentQueueStatus:
    """Manages agent Cursor queue status to optimize message delivery."""
    
    # In-memory cache for quick lookups (updated from status.json)
    _queue_status_cache: dict[str, dict] = {}
    _cache_file = Path("runtime/agent_queue_status.json")
    
    @classmethod
    def _load_cache(cls) -> dict[str, dict]:
        """Load queue status cache from file."""
        if cls._cache_file.exists():
            try:
                with open(cls._cache_file, encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load queue status cache: {e}")
        return {}
    
    @classmethod
    def _save_cache(cls, cache: dict[str, dict]) -> None:
        """Save queue status cache to file."""
        try:
            cls._cache_file.parent.mkdir(parents=True, exist_ok=True)
            with open(cls._cache_file, "w", encoding="utf-8") as f:
                json.dump(cache, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save queue status cache: {e}")
    
    @classmethod
    def _get_status_file(cls, agent_id: str) -> Path:
        """Get agent status.json file path."""
        return Path(f"agent_workspaces/{agent_id}/status.json")
    
    @classmethod
    def mark_full(cls, agent_id: str, reason: str = "Cursor queue full") -> bool:
        """
        Mark agent's Cursor queue as full.
        
        Args:
            agent_id: Agent identifier (e.g., "Agent-4")
            reason: Reason for marking as full
            
        Returns:
            True if successfully marked, False otherwise
        """
        try:
            status_file = cls._get_status_file(agent_id)
            
            # Read existing status
            status_data = {}
            if status_file.exists():
                try:
                    with open(status_file, encoding="utf-8") as f:
                        status_data = json.load(f)
                except Exception as e:
                    logger.warning(f"Failed to read status.json for {agent_id}: {e}")
            
            # Update queue status
            if "cursor_queue_status" not in status_data:
                status_data["cursor_queue_status"] = {}
            
            status_data["cursor_queue_status"] = {
                "is_full": True,
                "marked_at": datetime.now().isoformat(),
                "reason": reason,
                "last_checked": datetime.now().isoformat()
            }
            
            # Update last_updated
            status_data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Write back to file
            status_file.parent.mkdir(parents=True, exist_ok=True)
            with open(status_file, "w", encoding="utf-8") as f:
                json.dump(status_data, f, indent=2)
            
            # Update cache
            cls._queue_status_cache[agent_id] = status_data["cursor_queue_status"]
            cls._save_cache(cls._queue_status_cache)
            
            logger.info(f"✅ Marked {agent_id} as FULL (reason: {reason})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to mark {agent_id} as full: {e}")
            return False
    
    @classmethod
    def mark_available(cls, agent_id: str) -> bool:
        """
        Mark agent's Cursor queue as available (not full).
        
        Args:
            agent_id: Agent identifier (e.g., "Agent-4")
            
        Returns:
            True if successfully marked, False otherwise
        """
        try:
            status_file = cls._get_status_file(agent_id)
            
            # Read existing status
            status_data = {}
            if status_file.exists():
                try:
                    with open(status_file, encoding="utf-8") as f:
                        status_data = json.load(f)
                except Exception as e:
                    logger.warning(f"Failed to read status.json for {agent_id}: {e}")
            
            # Update queue status
            if "cursor_queue_status" not in status_data:
                status_data["cursor_queue_status"] = {}
            
            status_data["cursor_queue_status"] = {
                "is_full": False,
                "marked_at": datetime.now().isoformat(),
                "reason": "Queue available",
                "last_checked": datetime.now().isoformat()
            }
            
            # Update last_updated
            status_data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Write back to file
            status_file.parent.mkdir(parents=True, exist_ok=True)
            with open(status_file, "w", encoding="utf-8") as f:
                json.dump(status_data, f, indent=2)
            
            # Update cache
            cls._queue_status_cache[agent_id] = status_data["cursor_queue_status"]
            cls._save_cache(cls._queue_status_cache)
            
            logger.info(f"✅ Marked {agent_id} as AVAILABLE")
            return True
            
        except Exception as e:
            logger.error(f"Failed to mark {agent_id} as available: {e}")
            return False
    
    @classmethod
    def is_full(cls, agent_id: str) -> bool:
        """
        Check if agent's Cursor queue is marked as full.
        
        Args:
            agent_id: Agent identifier (e.g., "Agent-4")
            
        Returns:
            True if queue is full, False otherwise
        """
        try:
            # Check cache first
            if agent_id in cls._queue_status_cache:
                cache_entry = cls._queue_status_cache[agent_id]
                # Check if cache is recent (within 5 minutes)
                if "last_checked" in cache_entry:
                    from datetime import datetime, timedelta
                    last_checked = datetime.fromisoformat(cache_entry["last_checked"])
                    if datetime.now() - last_checked < timedelta(minutes=5):
                        return cache_entry.get("is_full", False)
            
            # Read from status.json
            status_file = cls._get_status_file(agent_id)
            if not status_file.exists():
                return False
            
            with open(status_file, encoding="utf-8") as f:
                status_data = json.load(f)
            
            queue_status = status_data.get("cursor_queue_status", {})
            is_full = queue_status.get("is_full", False)
            
            # Update cache
            cls._queue_status_cache[agent_id] = queue_status
            cls._save_cache(cls._queue_status_cache)
            
            return is_full
            
        except Exception as e:
            logger.debug(f"Error checking queue status for {agent_id}: {e}")
            return False
    
    @classmethod
    def get_status(cls, agent_id: str) -> Optional[dict]:
        """
        Get full queue status for an agent.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            Dictionary with queue status or None if not found
        """
        try:
            status_file = cls._get_status_file(agent_id)
            if not status_file.exists():
                return None
            
            with open(status_file, encoding="utf-8") as f:
                status_data = json.load(f)
            
            return status_data.get("cursor_queue_status")
            
        except Exception as e:
            logger.debug(f"Error getting queue status for {agent_id}: {e}")
            return None
    
    @classmethod
    def refresh_cache(cls) -> None:
        """Refresh cache from all agent status files."""
        cls._queue_status_cache = {}
        for agent_id in [f"Agent-{i}" for i in range(1, 9)]:
            cls.is_full(agent_id)  # This will update cache

