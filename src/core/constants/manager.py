"""
<!-- SSOT Domain: core -->

Single Source of Truth (SSOT) for Manager System Constants
Domain: core
Owner: Agent-2 (Architecture & Design)
Last Updated: 2025-12-08
Related SSOT: src/core/managers/base_manager.py, src/core/managers/manager_lifecycle.py
"""

import os
from pathlib import Path
from typing import Any

import yaml

"""Manager Constants - Manager Module Definitions"""

# Basic manager constants with environment overrides
DEFAULT_HEALTH_CHECK_INTERVAL = int(
    os.getenv("DEFAULT_HEALTH_CHECK_INTERVAL", 30))
DEFAULT_MAX_STATUS_HISTORY = int(os.getenv("DEFAULT_MAX_STATUS_HISTORY", 1000))
DEFAULT_AUTO_RESOLVE_TIMEOUT = int(
    os.getenv("DEFAULT_AUTO_RESOLVE_TIMEOUT", 3600))
STATUS_CONFIG_PATH = "config/status_manager.json"


def _load_messaging_config() -> dict[str, Any]:
    config_path = Path(__file__).resolve(
    ).parents[3] / "config" / "messaging.yml"
    try:
        with config_path.open("r", encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}
    except FileNotFoundError:
        return {}


COMPLETION_SIGNAL = _load_messaging_config().get(
    "COMPLETION_SIGNAL", "<unique-marker>")


def get_completion_signal() -> str:
    """Return the configured completion signal."""
    return COMPLETION_SIGNAL
