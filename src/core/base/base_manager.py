#!/usr/bin/env python3
"""
Base Manager Class - Code Consolidation
========================================

<!-- SSOT Domain: core -->

Base class for Manager classes to consolidate duplicate initialization,
logging, and lifecycle patterns.

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


class BaseManager(ABC, InitializationMixin, ErrorHandlingMixin):
    """
    Base class for Manager classes.

    Consolidates common Manager patterns:
    - Logging initialization
    - Configuration loading
    - Lifecycle management
    - Error handling

    Usage:
        class MyManager(BaseManager):
            def __init__(self):
                super().__init__("MyManager")
                # Custom initialization
    """

    def __init__(self, manager_name: str, config_section: Optional[str] = None):
        """
        Initialize base manager.

        Uses InitializationMixin for consolidated initialization pattern.

        Args:
            manager_name: Name of the manager (for logging)
            config_section: Optional config section name
        """
        self.manager_name = manager_name
        self.config_section = config_section or manager_name.lower()

        # Use consolidated initialization pattern from InitializationMixin
        self.logger, config_dict = self.initialize_with_config(
            manager_name,
            self.config_section
        )

        # Store config for backward compatibility
        self.config = UnifiedConfigManager()
        self.manager_config = config_dict or {}

        # Lifecycle state
        self._initialized = False
        self._active = False

        self.logger.info(f"✅ {manager_name} initialized")

    def initialize(self) -> bool:
        """
        Initialize manager (called after __init__ if needed).

        Returns:
            True if initialization successful
        """
        if self._initialized:
            self.logger.warning(f"{self.manager_name} already initialized")
            return True

        return self.safe_execute(
            operation=lambda: self._do_initialize() or True,
            operation_name="initialize",
            default_return=False,
            logger=self.logger,
            component_name=self.manager_name
        ) and self._set_initialized()

    def _set_initialized(self) -> bool:
        """Set initialized state and log success."""
        self._initialized = True
        self.logger.info(f"✅ {self.manager_name} initialization complete")
        return True

    def _do_initialize(self) -> None:
        """
        Override this method for custom initialization logic.

        Called by initialize() method.
        """
        pass

    def activate(self) -> bool:
        """
        Activate manager (start operations).

        Returns:
            True if activation successful
        """
        if not self._initialized:
            self.logger.warning(
                f"{self.manager_name} not initialized, initializing now")
            if not self.initialize():
                return False

        if self._active:
            self.logger.warning(f"{self.manager_name} already active")
            return True

        try:
            self._do_activate()
            self._active = True
            self.logger.info(f"✅ {self.manager_name} activated")
            return True
        except Exception as e:
            self.handle_error(e, "activate", self.logger, self.manager_name)
            return False

    def _do_activate(self) -> None:
        """
        Override this method for custom activation logic.

        Called by activate() method.
        """
        pass

    def deactivate(self) -> bool:
        """
        Deactivate manager (stop operations).

        Returns:
            True if deactivation successful
        """
        if not self._active:
            self.logger.warning(f"{self.manager_name} not active")
            return True

        try:
            self._do_deactivate()
            self._active = False
            self.logger.info(f"✅ {self.manager_name} deactivated")
            return True
        except Exception as e:
            self.handle_error(e, "deactivate", self.logger, self.manager_name)
            return False

    def _do_deactivate(self) -> None:
        """
        Override this method for custom deactivation logic.

        Called by deactivate() method.
        """
        pass

    def get_status(self) -> dict[str, Any]:
        """
        Get manager status.

        Returns:
            Dict with status information
        """
        return {
            "manager_name": self.manager_name,
            "initialized": self._initialized,
            "active": self._active,
            "config_section": self.config_section,
        }

    def is_active(self) -> bool:
        """Check if manager is active."""
        return self._active

    def is_initialized(self) -> bool:
        """Check if manager is initialized."""
        return self._initialized
