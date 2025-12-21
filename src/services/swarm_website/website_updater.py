#!/usr/bin/env python3
"""
Swarm Website Updater
=====================

Automatically updates weareswarm.online WordPress site via REST API when agent events occur.

V2 Compliance | Author: Agent-7 (Web Development) | Date: 2025-12-14
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    logging.warning("requests library not available. Website updates will be disabled.")

logger = logging.getLogger(__name__)


class SwarmWebsiteUpdater:
    """
    Updates the Swarm website automatically via WordPress REST API.
    
    Automatically sends agent status updates and mission logs to weareswarm.online
    when agents complete tasks, update status, or log missions.
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize the website updater.
        
        Args:
            config_path: Optional path to config file. Defaults to .env file.
        """
        self.enabled = False
        self.base_url = None
        self.username = None
        self.password = None
        
        if not HAS_REQUESTS:
            logger.warning("⚠️ Website updater disabled: requests library not installed")
            return
        
        # Load configuration from environment variables
        self._load_config()
        
        if self.enabled:
            logger.info(f"✅ Website updater initialized: {self.base_url}")
        else:
            logger.info("⚠️ Website updater disabled: Configuration not found")
    
    def _load_config(self) -> None:
        """Load configuration from environment variables."""
        self.base_url = os.getenv('SWARM_WEBSITE_URL', '').rstrip('/')
        self.username = os.getenv('SWARM_WEBSITE_USERNAME', '')
        self.password = os.getenv('SWARM_WEBSITE_PASSWORD', '')
        
        # Check if configuration is present
        if self.base_url and self.username and self.password:
            self.enabled = True
        else:
            logger.debug("Website updater config missing. Set SWARM_WEBSITE_URL, SWARM_WEBSITE_USERNAME, SWARM_WEBSITE_PASSWORD")
    
    def test_connection(self) -> str:
        """
        Test connection to the website API.
        
        Returns:
            Status message
        """
        if not self.enabled:
            return "❌ Website updater not configured. Check environment variables."
        
        try:
            url = f"{self.base_url}/wp-json/swarm/v2/health"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                return "✅ Website connection successful!"
            else:
                return f"⚠️ Website connection returned status {response.status_code}"
        except Exception as e:
            return f"❌ Website connection failed: {str(e)}"
    
    def update_agent_status(
        self,
        agent_id: str,
        status: str,
        points: Optional[int] = None,
        current_mission: Optional[str] = None,
        **kwargs
    ) -> bool:
        """
        Update agent status on the website.
        
        Args:
            agent_id: Agent identifier (e.g., 'agent-1', 'agent-2')
            status: Agent status ('active', 'idle', 'paused')
            points: Current points earned
            current_mission: Current mission description
            **kwargs: Additional fields to update
        
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            logger.debug("Website updater disabled, skipping status update")
            return False
        
        try:
            url = f"{self.base_url}/wp-json/swarm/v2/agents/{agent_id}"
            
            payload = {
                "status": status,
            }
            
            if points is not None:
                payload["points"] = points
            if current_mission:
                payload["mission"] = current_mission
            
            # Add any additional fields
            payload.update(kwargs)
            
            response = requests.post(
                url,
                json=payload,
                auth=(self.username, self.password),
                timeout=10
            )
            
            if response.status_code in (200, 201):
                logger.info(f"✅ Updated {agent_id} status on website")
                return True
            else:
                logger.warning(f"⚠️ Failed to update {agent_id} status: HTTP {response.status_code}")
                logger.debug(f"Response: {response.text[:200]}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error updating {agent_id} status: {e}")
            return False
    
    def post_mission_log(
        self,
        agent: str,
        message: str,
        priority: str = "normal",
        tags: Optional[list] = None
    ) -> bool:
        """
        Post a mission log entry to the website.
        
        Args:
            agent: Agent name (e.g., 'Agent-1', 'Agent-2')
            message: Mission log message
            priority: Priority level ('normal', 'high', 'urgent')
            tags: Optional list of tags
        
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            logger.debug("Website updater disabled, skipping mission log")
            return False
        
        try:
            url = f"{self.base_url}/wp-json/swarm/v2/mission-log"
            
            payload = {
                "agent": agent,
                "message": message,
                "priority": priority,
            }
            
            if tags:
                payload["tags"] = tags
            
            response = requests.post(
                url,
                json=payload,
                auth=(self.username, self.password),
                timeout=10
            )
            
            if response.status_code in (200, 201):
                logger.info(f"✅ Posted mission log from {agent}")
                return True
            else:
                logger.warning(f"⚠️ Failed to post mission log: HTTP {response.status_code}")
                logger.debug(f"Response: {response.text[:200]}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error posting mission log: {e}")
            return False
    
    def update_agent_from_status_file(self, agent_id: str, status_file_path: Path) -> bool:
        """
        Update agent status from status.json file.
        
        Args:
            agent_id: Agent identifier
            status_file_path: Path to agent status.json file
        
        Returns:
            True if successful, False otherwise
        """
        if not status_file_path.exists():
            logger.debug(f"Status file not found: {status_file_path}")
            return False
        
        try:
            with open(status_file_path, 'r', encoding='utf-8') as f:
                status_data = json.load(f)
            
            return self.update_agent_status(
                agent_id=agent_id,
                status=status_data.get('status', 'idle').lower(),
                points=status_data.get('total_points', 0),
                current_mission=status_data.get('current_mission', ''),
                current_phase=status_data.get('current_phase', ''),
                last_updated=status_data.get('last_updated', ''),
            )
        except Exception as e:
            logger.error(f"❌ Error reading status file: {e}")
            return False


