#!/usr/bin/env python3
"""
Agent Mode Manager - SSOT for Agent Operating Modes
===================================================

<!-- SSOT Domain: core -->

Manages different agent operating modes (4-agent, 5-agent, 6-agent, 8-agent).
Provides mode-aware agent lists, processing orders, and coordinate filtering.

V2 Compliance: <300 lines, single responsibility
Author: Agent-4 (Captain)
Date: 2025-12-13
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class AgentModeManager:
    """Manages agent operating modes and provides mode-aware utilities."""

    def __init__(self, config_path: Path | str | None = None):
        """Initialize agent mode manager.
        
        Args:
            config_path: Path to agent_mode_config.json (default: project root)
        """
        if config_path is None:
            # Default to project root
            project_root = Path(__file__).resolve().parent.parent.parent
            config_path = project_root / "agent_mode_config.json"
        
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self._validate_config()
    
    def _load_config(self) -> dict[str, Any]:
        """Load agent mode configuration from JSON file."""
        try:
            if not self.config_path.exists():
                logger.error(f"❌ Agent mode config not found: {self.config_path}")
                return self._get_default_config()
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            logger.info(f"✅ Loaded agent mode config: {config.get('current_mode', 'unknown')}")
            return config
        except Exception as e:
            logger.error(f"❌ Failed to load agent mode config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> dict[str, Any]:
        """Get default configuration (4-agent mode)."""
        return {
            "current_mode": "4-agent",
            "modes": {
                "4-agent": {
                    "active_agents": ["Agent-1", "Agent-2", "Agent-3", "Agent-4"],
                    "processing_order": ["Agent-1", "Agent-2", "Agent-3", "Agent-4"],
                    "monitor_setup": "single"
                }
            }
        }
    
    def _validate_config(self) -> None:
        """Validate configuration structure."""
        if "current_mode" not in self.config:
            logger.warning("⚠️ No current_mode in config, defaulting to 4-agent")
            self.config["current_mode"] = "4-agent"
        
        if "modes" not in self.config:
            logger.error("❌ No modes defined in config!")
            self.config["modes"] = self._get_default_config()["modes"]
        
        current_mode = self.config["current_mode"]
        if current_mode not in self.config["modes"]:
            logger.error(f"❌ Current mode '{current_mode}' not found in modes!")
            self.config["current_mode"] = "4-agent"
    
    def get_current_mode(self) -> str:
        """Get current agent mode name."""
        return self.config.get("current_mode", "4-agent")
    
    def get_mode_info(self, mode_name: str | None = None) -> dict[str, Any]:
        """Get mode information.
        
        Args:
            mode_name: Mode name (default: current mode)
        
        Returns:
            Mode configuration dictionary
        """
        mode_name = mode_name or self.get_current_mode()
        modes = self.config.get("modes", {})
        
        if mode_name not in modes:
            logger.warning(f"⚠️ Mode '{mode_name}' not found, using current mode")
            mode_name = self.get_current_mode()
        
        return modes.get(mode_name, {})
    
    def get_active_agents(self, mode_name: str | None = None) -> list[str]:
        """Get list of active agents for specified mode.
        
        Args:
            mode_name: Mode name (default: current mode)
        
        Returns:
            List of active agent IDs
        """
        mode_info = self.get_mode_info(mode_name)
        return mode_info.get("active_agents", [])
    
    def get_processing_order(self, mode_name: str | None = None) -> list[str]:
        """Get agent processing order for specified mode.
        
        Args:
            mode_name: Mode name (default: current mode)
        
        Returns:
            List of agent IDs in processing order
        """
        mode_info = self.get_mode_info(mode_name)
        return mode_info.get("processing_order", self.get_active_agents(mode_name))
    
    def get_monitor_setup(self, mode_name: str | None = None) -> str:
        """Get monitor setup type for specified mode.
        
        Args:
            mode_name: Mode name (default: current mode)
        
        Returns:
            Monitor setup type: "single" or "dual"
        """
        mode_info = self.get_mode_info(mode_name)
        return mode_info.get("monitor_setup", "single")
    
    def is_agent_active(self, agent_id: str, mode_name: str | None = None) -> bool:
        """Check if agent is active in specified mode.
        
        Args:
            agent_id: Agent ID to check
            mode_name: Mode name (default: current mode)
        
        Returns:
            True if agent is active, False otherwise
        """
        active_agents = self.get_active_agents(mode_name)
        return agent_id in active_agents
    
    def get_available_modes(self) -> list[str]:
        """Get list of available mode names.
        
        Returns:
            List of available mode names
        """
        return list(self.config.get("modes", {}).keys())
    
    def set_mode(self, mode_name: str, save: bool = True) -> bool:
        """Set current agent mode.
        
        Args:
            mode_name: Mode name to set
            save: Whether to save to config file
        
        Returns:
            True if mode set successfully, False otherwise
        """
        if mode_name not in self.config.get("modes", {}):
            logger.error(f"❌ Mode '{mode_name}' not found in available modes: {self.get_available_modes()}")
            return False
        
        old_mode = self.config.get("current_mode")
        self.config["current_mode"] = mode_name
        
        logger.info(f"✅ Agent mode changed: {old_mode} → {mode_name}")
        logger.info(f"   Active agents: {len(self.get_active_agents())} ({', '.join(self.get_active_agents())})")
        logger.info(f"   Monitor setup: {self.get_monitor_setup()}")
        
        if save:
            self._save_config()
        
        return True
    
    def _save_config(self) -> None:
        """Save configuration to file."""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
            logger.info(f"✅ Saved agent mode config: {self.config_path}")
        except Exception as e:
            logger.error(f"❌ Failed to save agent mode config: {e}")
    
    def get_all_agents_by_mode(self) -> dict[str, list[str]]:
        """Get all agents organized by mode.
        
        Returns:
            Dictionary mapping mode names to active agent lists
        """
        result = {}
        for mode_name in self.get_available_modes():
            result[mode_name] = self.get_active_agents(mode_name)
        return result


# Global mode manager instance
_mode_manager: AgentModeManager | None = None


def get_mode_manager(config_path: Path | str | None = None) -> AgentModeManager:
    """Get global agent mode manager instance.
    
    Args:
        config_path: Optional path to config file
    
    Returns:
        AgentModeManager instance
    """
    global _mode_manager
    if _mode_manager is None:
        _mode_manager = AgentModeManager(config_path)
    return _mode_manager


def get_active_agents(mode_name: str | None = None) -> list[str]:
    """Get active agents for specified mode (convenience function).
    
    Args:
        mode_name: Mode name (default: current mode)
    
    Returns:
        List of active agent IDs
    """
    return get_mode_manager().get_active_agents(mode_name)


def get_processing_order(mode_name: str | None = None) -> list[str]:
    """Get processing order for specified mode (convenience function).
    
    Args:
        mode_name: Mode name (default: current mode)
    
    Returns:
        List of agent IDs in processing order
    """
    return get_mode_manager().get_processing_order(mode_name)


def is_agent_active(agent_id: str, mode_name: str | None = None) -> bool:
    """Check if agent is active (convenience function).
    
    Args:
        agent_id: Agent ID to check
        mode_name: Mode name (default: current mode)
    
    Returns:
        True if agent is active, False otherwise
    """
    return get_mode_manager().is_agent_active(agent_id, mode_name)


def set_agent_mode(mode_name: str, save: bool = True) -> bool:
    """Set agent mode (convenience function).
    
    Args:
        mode_name: Mode name to set
        save: Whether to save to config file
    
    Returns:
        True if mode set successfully, False otherwise
    """
    return get_mode_manager().set_mode(mode_name, save)


__all__ = [
    "AgentModeManager",
    "get_mode_manager",
    "get_active_agents",
    "get_processing_order",
    "is_agent_active",
    "set_agent_mode",
]


