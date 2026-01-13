"""
Agent Status Cache
==================

Shared caching layer for agent status.json files.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Architecture: Agent-2 (Architecture & Design Specialist)
Created: 2025-12-31
V2 Compliant: Yes (<400 lines, functions <30 lines)

<!-- SSOT Domain: core -->
"""

import time
from pathlib import Path
from typing import Dict, Optional, Any
from datetime import datetime


class StatusCache:
    """Caching layer for agent status.json files."""
    
    def __init__(self, cache_ttl: float = 5.0):
        """
        Initialize status cache.
        
        Args:
            cache_ttl: Cache time-to-live in seconds (default: 5.0)
        """
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.cache_timestamps: Dict[str, float] = {}
        self.cache_ttl = cache_ttl
    
    def get(self, agent_id: str, status_file: Path) -> Optional[Dict[str, Any]]:
        """
        Get cached status or None if cache miss/expired.
        
        Args:
            agent_id: Agent ID (e.g., "Agent-1")
            status_file: Path to status.json file
        
        Returns:
            Cached status dict or None
        """
        cache_key = f"{agent_id}:{status_file}"
        current_time = time.time()
        
        # Check if cached and not expired
        if cache_key in self.cache:
            cache_time = self.cache_timestamps.get(cache_key, 0)
            if current_time - cache_time < self.cache_ttl:
                # Check if file hasn't changed
                try:
                    file_mtime = status_file.stat().st_mtime
                    if file_mtime <= cache_time:
                        return self.cache[cache_key]
                except (OSError, FileNotFoundError):
                    # File doesn't exist or can't be accessed
                    pass
        
        return None
    
    def set(self, agent_id: str, status_file: Path, status: Dict[str, Any]) -> None:
        """
        Cache status data.
        
        Args:
            agent_id: Agent ID (e.g., "Agent-1")
            status_file: Path to status.json file
            status: Status dictionary to cache
        """
        cache_key = f"{agent_id}:{status_file}"
        self.cache[cache_key] = status
        self.cache_timestamps[cache_key] = time.time()
    
    def invalidate(self, agent_id: Optional[str] = None) -> None:
        """
        Invalidate cache entries.
        
        Args:
            agent_id: Specific agent ID to invalidate, or None for all
        """
        if agent_id:
            # Invalidate all entries for this agent
            keys_to_remove = [
                key for key in self.cache.keys()
                if key.startswith(f"{agent_id}:")
            ]
            for key in keys_to_remove:
                self.cache.pop(key, None)
                self.cache_timestamps.pop(key, None)
        else:
            # Invalidate all
            self.cache.clear()
            self.cache_timestamps.clear()
    
    def clear(self) -> None:
        """Clear all cache entries."""
        self.invalidate()

