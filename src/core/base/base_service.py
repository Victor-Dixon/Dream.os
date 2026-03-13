#!/usr/bin/env python3
"""
Base Service Class - Code Consolidation
========================================

<!-- SSOT Domain: core -->

Base class for Service classes to consolidate duplicate initialization,
lifecycle, and error handling patterns.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-12-02
License: MIT
"""

import logging
from abc import ABC
from typing import Any, Optional

from ..config.config_manager import UnifiedConfigManager
from ..unified_logging_system import UnifiedLoggingSystem
from .initialization_mixin import InitializationMixin
from .error_handling_mixin import ErrorHandlingMixin


class BaseService(ABC, InitializationMixin, ErrorHandlingMixin):
    """
    Base class for Service classes.

    Consolidates common Service patterns:
    - Logging initialization
    - Configuration loading
    - Lifecycle management
    - Error handling

    Usage:
        class MyService(BaseService):
            def __init__(self):
                super().__init__("MyService")
                # Custom initialization
    """

    def __init__(self, service_name: str, config_section: Optional[str] = None):
        """
        Initialize base service.

        Uses InitializationMixin for consolidated initialization pattern.

        Args:
            service_name: Name of the service (for logging)
            config_section: Optional config section name
        """
        self.service_name = service_name
        self.config_section = config_section or service_name.lower()

        # Use consolidated initialization pattern from InitializationMixin
        self.logger, config_dict = self.initialize_with_config(
            service_name,
            self.config_section
        )

        # Store config for backward compatibility
        self.config = UnifiedConfigManager()
        self.service_config = config_dict or {}

        # Lifecycle state
        self._initialized = False
        self._running = False

        self.logger.info(f"✅ {service_name} initialized")

    def initialize(self) -> bool:
        """
        Initialize service (called after __init__ if needed).

        Returns:
            True if initialization successful
        """
        if self._initialized:
            self.logger.warning(f"{self.service_name} already initialized")
            return True

        return self.safe_execute(
            operation=lambda: self._do_initialize() or True,
            operation_name="initialize",
            default_return=False,
            logger=self.logger,
            component_name=self.service_name
        ) and self._set_initialized()

    def _set_initialized(self) -> bool:
        """Set initialized state and log success."""
        self._initialized = True
        self.logger.info(f"✅ {self.service_name} initialization complete")
        return True

    def _do_initialize(self) -> None:
        """
        Override this method for custom initialization logic.

        Called by initialize() method.
        """
        pass

    def start(self) -> bool:
        """
        Start service (begin operations).

        Returns:
            True if start successful
        """
        if not self._initialized:
            self.logger.warning(
                f"{self.service_name} not initialized, initializing now")
            if not self.initialize():
                return False

        if self._running:
            self.logger.warning(f"{self.service_name} already running")
            return True

        try:
            self._do_start()
            self._running = True
            self.logger.info(f"✅ {self.service_name} started")
            return True
        except Exception as e:
            self.handle_error(e, "start", self.logger, self.service_name)
            return False

    def _do_start(self) -> None:
        """
        Override this method for custom start logic.

        Called by start() method.
        """
        pass

    def stop(self) -> bool:
        """
        Stop service (end operations).

        Returns:
            True if stop successful
        """
        if not self._running:
            self.logger.warning(f"{self.service_name} not running")
            return True

        try:
            self._do_stop()
            self._running = False
            self.logger.info(f"✅ {self.service_name} stopped")
            return True
        except Exception as e:
            self.handle_error(e, "stop", self.logger, self.service_name)
            return False

    def _do_stop(self) -> None:
        """
        Override this method for custom stop logic.

        Called by stop() method.
        """
        pass

    def get_status(self) -> dict[str, Any]:
        """
        Get service status.

        Returns:
            Dict with status information
        """
        return {
            "service_name": self.service_name,
            "initialized": self._initialized,
            "running": self._running,
            "config_section": self.config_section,
        }

    def is_running(self) -> bool:
        """Check if service is running."""
        return self._running

    def is_initialized(self) -> bool:
        """Check if service is initialized."""
        return self._initialized
