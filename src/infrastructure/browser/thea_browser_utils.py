"""
Thea Browser Utilities
======================

Utility functions for Thea browser service: cookie management, selector caching.

<!-- SSOT Domain: infrastructure -->

Author: Agent-3 (Infrastructure & DevOps) - V2 Refactoring
License: MIT
"""



import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class TheaBrowserUtils:
    """Utility functions for Thea browser operations."""

    def __init__(self, thea_config: Any):
        """Initialize utilities with Thea configuration."""
        self.thea_config = thea_config

            logger.debug(f"Legacy cookie save failed: {e}")


    def get_selector_cache_file(self) -> Path:
        """Get selector success cache file path."""
        return Path(self.thea_config.cache_dir) / "selector_success.json"

    def load_selector_cache(self) -> dict[str, Any]:
        """Load selector success cache from file."""
        try:
            cache_file = self.get_selector_cache_file()
            if cache_file.exists():
                with open(cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            logger.debug(f"Selector cache load failed: {e}")
        return {}

    def save_selector_cache(self, cache_data: dict[str, Any]) -> None:
        """Save selector success cache to file."""
        try:
            cache_file = self.get_selector_cache_file()
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, indent=2)
        except Exception as e:
            logger.debug(f"Selector cache save failed: {e}")

    def record_successful_selector(self, selector: str) -> None:
        """Record successful selector usage in cache (matches original implementation)."""
        try:
            from datetime import datetime

            cache_file = self.get_selector_cache_file()
            cache_file.parent.mkdir(parents=True, exist_ok=True)

            success_data = self.load_selector_cache()

            # Update success metrics (match original format)
            if selector not in success_data:
                success_data[selector] = {"attempts": 0, "successes": 0}

            success_data[selector]["attempts"] = success_data[selector].get("attempts", 0) + 1
            success_data[selector]["successes"] = success_data[selector].get("successes", 0) + 1
            success_data[selector]["success_rate"] = (
                success_data[selector]["successes"] / success_data[selector]["attempts"]
            )
            success_data[selector]["last_success"] = datetime.now().isoformat()

            self.save_selector_cache(success_data)

        except Exception as e:
            logger.debug(f"Could not record selector success: {e}")


__all__ = ["TheaBrowserUtils"]

