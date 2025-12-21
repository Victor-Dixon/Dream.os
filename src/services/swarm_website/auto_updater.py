#!/usr/bin/env python3
"""
Swarm Website Auto-Updater Plugin
==================================

Automatically monitors agent events and updates the website in real-time.

V2 Compliance | Author: Agent-7 (Web Development) | Date: 2025-12-14
"""

import json
import logging
import time
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import hashlib

from .website_updater import SwarmWebsiteUpdater

logger = logging.getLogger(__name__)


class SwarmWebsiteAutoUpdater:
    """
    Automatically monitors agent status files and mission logs,
    then updates the website when changes are detected.
    """
    
    def __init__(self, workspace_root: Optional[Path] = None):
        """
        Initialize the auto-updater.
        
        Args:
            workspace_root: Root directory containing agent_workspaces/
        """
        if workspace_root is None:
            workspace_root = Path(__file__).resolve().parent.parent.parent.parent
        
        self.workspace_root = workspace_root
        self.agent_workspaces = workspace_root / "agent_workspaces"
        self.updater = SwarmWebsiteUpdater()
        
        # Track last known state to detect changes
        self.last_status_hashes: Dict[str, str] = {}
        self.last_update_times: Dict[str, float] = {}
        
        # Minimum time between updates (seconds) to prevent spam
        self.update_cooldown = 5.0
        
        logger.info("✅ Website auto-updater initialized")
    
    def _get_status_file_hash(self, status_file: Path) -> str:
        """Get hash of status file contents."""
        if not status_file.exists():
            return ""
        
        try:
            content = status_file.read_text(encoding='utf-8')
            return hashlib.md5(content.encode()).hexdigest()
        except Exception as e:
            logger.warning(f"Error reading status file {status_file}: {e}")
            return ""
    
    def _should_update(self, agent_id: str) -> bool:
        """Check if enough time has passed since last update."""
        last_update = self.last_update_times.get(agent_id, 0)
        return (time.time() - last_update) >= self.update_cooldown
    
    def check_and_update_agent(self, agent_id: str) -> bool:
        """
        Check if agent status has changed and update website if needed.
        
        Args:
            agent_id: Agent identifier (e.g., 'Agent-1', 'Agent-2')
        
        Returns:
            True if updated, False otherwise
        """
        if not self.updater.enabled:
            return False
        
        # Convert Agent-1 to agent-1 for API
        agent_id_api = agent_id.lower().replace('agent-', 'agent-')
        
        status_file = self.agent_workspaces / agent_id / "status.json"
        
        if not status_file.exists():
            return False
        
        # Check if status changed
        current_hash = self._get_status_file_hash(status_file)
        last_hash = self.last_status_hashes.get(agent_id, "")
        
        if current_hash == last_hash:
            # No changes detected
            return False
        
        # Check cooldown
        if not self._should_update(agent_id):
            return False
        
        try:
            # Read status file
            with open(status_file, 'r', encoding='utf-8') as f:
                status_data = json.load(f)
            
            # Update website
            success = self.updater.update_agent_status(
                agent_id=agent_id_api,
                status=status_data.get('status', 'idle').lower(),
                points=status_data.get('total_points', 0),
                current_mission=status_data.get('current_mission', ''),
                current_phase=status_data.get('current_phase', ''),
                last_updated=status_data.get('last_updated', ''),
            )
            
            if success:
                # Update tracking
                self.last_status_hashes[agent_id] = current_hash
                self.last_update_times[agent_id] = time.time()
                logger.info(f"✅ Auto-updated {agent_id} on website")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Error auto-updating {agent_id}: {e}")
            return False
    
    def check_all_agents(self) -> int:
        """
        Check all active agents and update website if needed.
        
        Returns:
            Number of agents updated
        """
        updated_count = 0
        
        # Get active agents from mode config
        try:
            from src.core.agent_mode_manager import get_active_agents
            active_agents = get_active_agents()
        except Exception:
            # Fallback to default 4-agent mode
            active_agents = ['Agent-1', 'Agent-2', 'Agent-3', 'Agent-4']
        
        for agent_id in active_agents:
            if self.check_and_update_agent(agent_id):
                updated_count += 1
        
        return updated_count
    
    def monitor_agent_status_files(self, interval: float = 10.0) -> None:
        """
        Continuously monitor agent status files and update website.
        
        Args:
            interval: Seconds between checks
        """
        logger.info(f"🔍 Starting website auto-update monitor (interval: {interval}s)")
        
        try:
            while True:
                updated = self.check_all_agents()
                if updated > 0:
                    logger.info(f"📤 Updated {updated} agent(s) on website")
                
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info("⏹️ Website auto-update monitor stopped")
        except Exception as e:
            logger.error(f"❌ Error in monitor loop: {e}")


# Convenience function for easy import
def auto_update_agent_status(agent_id: str) -> bool:
    """
    Convenience function to check and update a single agent.
    
    Args:
        agent_id: Agent identifier
    
    Returns:
        True if updated
    """
    updater = SwarmWebsiteAutoUpdater()
    return updater.check_and_update_agent(agent_id)


