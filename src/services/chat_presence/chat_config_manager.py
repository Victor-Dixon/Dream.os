"""
Chat Config Manager - V2 Coordinator Module
===========================================

SSOT Domain: integration

V2 Compliant: <100 lines, single responsibility
Configuration management for chat presence system.

Author: Agent-2 (dream.os)
Date: 2026-01-08
"""

import os
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass

from src.core.config.config_manager import UnifiedConfigManager


@dataclass
class ChatConfig:
    """Configuration for chat presence system"""
    twitch_enabled: bool = True
    twitch_channel: str = ""
    twitch_token: str = ""
    obs_enabled: bool = False
    obs_host: str = "localhost"
    obs_port: int = 4444
    obs_password: str = ""
    agent_coordination_enabled: bool = True
    message_queue_enabled: bool = True
    status_update_interval: int = 60
    max_reconnect_attempts: int = 5


class ChatConfigManager:
    """
    V2 Compliant Configuration Manager

    Handles all configuration loading and validation for chat presence system.
    Single responsibility: configuration management.
    """

    def __init__(self, config_manager: Optional[UnifiedConfigManager] = None):
        self.config_manager = config_manager or UnifiedConfigManager()
        self.logger = logging.getLogger("ChatConfigManager")

        # Load configuration
        self.config = self._load_config()

    def _load_config(self) -> ChatConfig:
        """Load configuration from environment and config files"""
        config = ChatConfig()

        # Load from environment variables
        config.twitch_channel = os.getenv("TWITCH_CHANNEL", "").strip()
        config.twitch_token = os.getenv("TWITCH_ACCESS_TOKEN", "").strip()
        config.obs_host = os.getenv("OBS_HOST", "localhost")
        config.obs_port = int(os.getenv("OBS_PORT", "4444"))
        config.obs_password = os.getenv("OBS_PASSWORD", "").strip()

        # Load from unified config if available
        try:
            chat_config = self.config_manager.get_config("chat_presence")
            if chat_config:
                config.twitch_enabled = chat_config.get("twitch_enabled", True)
                config.obs_enabled = chat_config.get("obs_enabled", False)
                config.agent_coordination_enabled = chat_config.get("agent_coordination_enabled", True)
                config.message_queue_enabled = chat_config.get("message_queue_enabled", True)
                config.status_update_interval = chat_config.get("status_update_interval", 60)
                config.max_reconnect_attempts = chat_config.get("max_reconnect_attempts", 5)
        except Exception as e:
            self.logger.warning(f"Could not load unified config: {e}")

        return config

    def get_config(self) -> ChatConfig:
        """Get current configuration"""
        return self.config

    def is_twitch_enabled(self) -> bool:
        """Check if Twitch integration is enabled"""
        return self.config.twitch_enabled and bool(self.config.twitch_channel)

    def is_obs_enabled(self) -> bool:
        """Check if OBS integration is enabled"""
        return self.config.obs_enabled

    def is_agent_coordination_enabled(self) -> bool:
        """Check if agent coordination is enabled"""
        return self.config.agent_coordination_enabled

    def validate_config(self) -> Dict[str, Any]:
        """
        Validate current configuration

        Returns:
            Dict with validation results and any issues found
        """
        issues = []

        # Validate Twitch config
        if self.config.twitch_enabled:
            if not self.config.twitch_channel:
                issues.append("Twitch enabled but no channel specified")
            if not self.config.twitch_token:
                issues.append("Twitch enabled but no token specified")
            elif not self.config.twitch_token.startswith("oauth:"):
                issues.append("Twitch token should start with 'oauth:'")

        # Validate OBS config
        if self.config.obs_enabled:
            if not self.config.obs_host:
                issues.append("OBS enabled but no host specified")
            if self.config.obs_port <= 0 or self.config.obs_port > 65535:
                issues.append("OBS port must be between 1-65535")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "config": self.config
        }

    def reload_config(self) -> None:
        """Reload configuration from sources"""
        self.config = self._load_config()
        self.logger.info("Chat configuration reloaded")