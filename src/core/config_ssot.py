# Header-Variant: full
# Owner: Dream.os Platform
# Purpose: Config ssot.
# SSOT: docs/recovery/recovery_registry.yaml

"""
@file
@summary Provide backward-compatible SSOT config imports for core modules.
@registry docs/recovery/recovery_registry.yaml#core-config-ssot-shim

@file Config ssot.
"""

from src.core.config.config_accessors import (
    get_agent_config,
    get_browser_config,
    get_config,
    get_file_pattern_config,
    get_report_config,
    get_test_config,
    get_threshold_config,
    get_timeout_config,
    get_unified_config,
    reload_config,
    validate_config,
)
from src.core.config.config_dataclasses import (
    AgentConfig,
    BrowserConfig,
    FilePatternConfig,
    ReportConfig,
    TestConfiguration,
    ThresholdConfig,
    TimeoutConfig,
)
from src.core.config.config_enums import ConfigEnvironment, ConfigSource, ReportFormat
from src.core.config.config_manager import UnifiedConfigManager

TestConfig = TestConfiguration

__all__ = [
    "UnifiedConfigManager",
    "get_config",
    "get_unified_config",
    "get_timeout_config",
    "get_agent_config",
    "get_browser_config",
    "get_threshold_config",
    "get_file_pattern_config",
    "get_test_config",
    "get_report_config",
    "validate_config",
    "reload_config",
    "ConfigEnvironment",
    "ConfigSource",
    "ReportFormat",
    "TimeoutConfig",
    "AgentConfig",
    "BrowserConfig",
    "ThresholdConfig",
    "FilePatternConfig",
    "TestConfiguration",
    "TestConfig",
    "ReportConfig",
]
