#!/usr/bin/env python3
"""
Config Manager Shim - Backward Compatibility Layer
===================================================

This shim maintains backward compatibility while migrating to config_ssot.
All imports of config_manager will continue to work.

Created: 2025-01-28
Agent: Agent-1 (Integration & Core Systems Specialist)
Phase: Phase 2 Agent_Cellphone Config Migration
"""

import warnings
from typing import Any

# Import from config_ssot
from src.core.config_ssot import (
    ConfigEnvironment,
    ConfigSource,
    UnifiedConfigManager,
    get_config,
    get_agent_config,
)

# Backward compatibility: Export ConfigManager as alias
ConfigManager = UnifiedConfigManager

# Backward compatibility: Create enum shims
# Map old enums to config_ssot equivalents
class ConfigValidationLevel:
    """ConfigValidationLevel enum compatibility shim."""
    BASIC = "basic"
    STRICT = "strict"
    ENTERPRISE = "enterprise"

class ConfigReloadMode:
    """ConfigReloadMode enum compatibility shim."""
    MANUAL = "manual"
    AUTO = "auto"
    WATCH = "watch"

class ConfigFormat:
    """ConfigFormat enum compatibility shim."""
    JSON = "json"
    YAML = "yaml"
    INI = "ini"
    ENV = "env"

# Backward compatibility: Create dataclass shims
from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class ConfigSection:
    """ConfigSection dataclass compatibility shim."""
    name: str
    data: Dict[str, Any]
    source: Optional[str] = None

@dataclass
class ConfigValidationResult:
    """ConfigValidationResult dataclass compatibility shim."""
    is_valid: bool
    errors: list[str]
    warnings: list[str]

# Deprecation warning
warnings.warn(
    "core.config_manager is deprecated. Use src.core.config_ssot instead. "
    "This shim will be removed in a future release.",
    DeprecationWarning,
    stacklevel=2
)

__all__ = [
    "ConfigManager",
    "ConfigValidationLevel",
    "ConfigReloadMode",
    "ConfigFormat",
    "ConfigSection",
    "ConfigValidationResult",
    "UnifiedConfigManager",
    "get_config",
    "get_agent_config",
    "ConfigEnvironment",
    "ConfigSource",
]

