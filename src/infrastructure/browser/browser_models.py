
"""
Browser Models - Unified Browser Service
=========================================

Configuration and data models for browser operations.

<!-- SSOT Domain: infrastructure -->

Author: Agent-6 (VSCode Forking & Quality Gates Specialist) - Refactored from Agent-3
License: MIT
"""

"""
⚠️ DEPRECATED - BrowserConfig is deprecated.

This class has been consolidated into src/core/config/config_dataclasses.py as SSOT.
Please update imports to use the SSOT location instead.

Migration:
  OLD: from config.config_dataclasses import BrowserConfig
  NEW: from core.config.config_dataclasses import BrowserConfig

This module/class will be removed in a future release.
"""

import warnings
warnings.warn(
    "BrowserConfig is deprecated. Use src/core/config/config_dataclasses.py instead.",
    DeprecationWarning,
    stacklevel=2
)


import time

from typing import Optional
from dataclasses import dataclass, field

try:
    from ...core.config_ssot import get_unified_config

    _unified_config = get_unified_config()
except ImportError:
    _unified_config = None

from ...core.config.timeout_constants import TimeoutConstants


@dataclass
class BrowserConfig:
    """Configuration for browser operations with enhanced config integration."""

    headless: bool = False
    user_data_dir: str | None = None
    window_size: tuple[int, int] = (1920, 1080)
    timeout: float = 30.0
    implicit_wait: float = 10.0
    page_load_timeout: float = TimeoutConstants.HTTP_LONG

    def __post_init__(self):
        """Initialize from unified config if available."""
        if _unified_config and hasattr(_unified_config, "get_timeout_config"):
            timeout_config = _unified_config.get_timeout_config()
            self.timeout = timeout_config.get("SCRAPE_TIMEOUT", self.timeout)
            self.implicit_wait = timeout_config.get("QUALITY_CHECK_INTERVAL", self.implicit_wait)
            self.page_load_timeout = timeout_config.get(
                "RESPONSE_WAIT_TIMEOUT", self.page_load_timeout
            )


@dataclass
class TheaConfig:
    """Configuration for Thea Manager interactions with enhanced config integration."""

    conversation_url: str = (
        "https://chatgpt.com/g/g-68fd74b31d84819190eb2588b5c649f6-swarm-commander-thea"
    )
    cookie_file: str = "data/thea_cookies.json"
    encrypted_cookie_file: Optional[str] = None
    key_file: Optional[str] = None
    auto_save_cookies: bool = True
    rate_limit_requests_per_minute: int = 10
    rate_limit_burst_limit: int = 5
    cache_dir: str = "data/cache/thea"


@dataclass
class SessionInfo:
    """Session information."""

    session_id: str
    service_name: str
    status: str
    created_at: float = field(default_factory=time.time)
    last_activity: float = field(default_factory=time.time)
    request_count: int = 0


@dataclass
class RateLimitStatus:
    """Rate limit status information."""

    requests_remaining: int
    reset_time: float | None = None
    is_rate_limited: bool = False

