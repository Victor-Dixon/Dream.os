#!/usr/bin/env python3
"""
Config Shim - Backward Compatibility Layer
==========================================

Maintains SystemPaths and ConfigManager compatibility.
Provides path accessor functions for backward compatibility.

Created: 2025-01-28
Agent: Agent-1 (Integration & Core Systems Specialist)
Phase: Phase 2 Agent_Cellphone Config Migration
"""

import warnings
from pathlib import Path
from typing import Optional

from src.core.config_ssot import get_config

# Deprecation warning
warnings.warn(
    "config module is deprecated. Use src.core.config_ssot instead. "
    "This shim will be removed in a future release.",
    DeprecationWarning,
    stacklevel=2
)


class SystemPaths:
    """SystemPaths compatibility shim."""
    
    def __init__(self):
        """Initialize SystemPaths from config_ssot."""
        config = get_config()
        
        # Map paths from config_ssot
        # These keys may need adjustment based on actual config_ssot structure
        self.repos_root = Path(config.get('repos_root', Path.cwd()))
        self.communications_root = Path(
            config.get('communications_root', Path.cwd() / 'communications')
        )
        self.agent_workspaces_root = Path(
            config.get('agent_workspaces_root', Path.cwd() / 'agent_workspaces')
        )
        self.owner_path = Path(config.get('owner_path', Path.cwd()))
        
        # Additional paths as needed
        self.config_root = Path(config.get('config_root', Path.cwd() / 'config'))
        self.data_root = Path(config.get('data_root', Path.cwd() / 'data'))
        self.logs_root = Path(config.get('logs_root', Path.cwd() / 'logs'))


class ConfigManager:
    """ConfigManager compatibility shim for path management."""
    
    def __init__(self):
        """Initialize ConfigManager from config_ssot."""
        self._config = get_config()
    
    def get_path(self, key: str) -> Optional[Path]:
        """Get path from config_ssot."""
        value = self._config.get(key)
        if value:
            return Path(value)
        return None
    
    def get_repos_root(self) -> Path:
        """Get repos root path."""
        return Path(self._config.get('repos_root', Path.cwd()))
    
    def get_owner_path(self) -> Path:
        """Get owner path."""
        return Path(self._config.get('owner_path', Path.cwd()))
    
    def get_communications_root(self) -> Path:
        """Get communications root path."""
        return Path(self._config.get('communications_root', Path.cwd() / 'communications'))


# Backward compatibility: Export path accessor functions
def get_repos_root() -> Path:
    """Get repos root path from config_ssot."""
    config = get_config()
    return Path(config.get('repos_root', Path.cwd()))


def get_owner_path() -> Path:
    """Get owner path from config_ssot."""
    config = get_config()
    return Path(config.get('owner_path', Path.cwd()))


def get_communications_root() -> Path:
    """Get communications root path from config_ssot."""
    config = get_config()
    return Path(config.get('communications_root', Path.cwd() / 'communications'))


__all__ = [
    "SystemPaths",
    "ConfigManager",
    "get_repos_root",
    "get_owner_path",
    "get_communications_root",
]

