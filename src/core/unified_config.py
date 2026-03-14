# Header-Variant: full
# Owner: Dream.OS
# Purpose: unified config.
# SSOT: docs/recovery/recovery_registry.yaml#core-unified-config-shim
# @registry docs/recovery/recovery_registry.yaml#core-unified-config-shim

"""
@file
@summary Keep legacy unified_config imports mapped to config SSOT exports.
@registry docs/recovery/recovery_registry.yaml#core-unified-config-shim
"""

from src.core.config_ssot import *  # noqa: F401,F403
from src.core.config_ssot import UnifiedConfigManager as UnifiedConfig
