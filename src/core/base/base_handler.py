#!/usr/bin/env python3
"""
Base Handler Class - Code Consolidation
=======================================

<!-- SSOT Domain: core -->

Base class for Handler classes to consolidate duplicate initialization,
error handling, and validation patterns.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-12-02
License: MIT
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Optional

from ..config.config_manager import UnifiedConfigManager
from ..unified_logging_system import UnifiedLoggingSystem
from .initialization_mixin import InitializationMixin
from .error_handling_mixin import ErrorHandlingMixin


class BaseHandler(ABC, InitializationMixin, ErrorHandlingMixin):
    """
    Base class for Handler classes.

    Consolidates common Handler patterns:
    - Logging initialization
    - Error handling
    - Input validation
    - Response formatting

    Usage:
        class MyHandler(BaseHandler):
            def __init__(self):
                super().__init__("MyHandler")

            def handle(self, request: dict) -> dict:
                self.validate_request(request)
                # Handle logic
                return self.format_response(result)
    """

    def __init__(self, handler_name: str, config_section: Optional[str] = None):
        """
        Initialize base handler.

        Uses InitializationMixin for consolidated initialization pattern.

        Args:
            handler_name: Name of the handler (for logging)
            config_section: Optional config section name
        """
        self.handler_name = handler_name
        self.config_section = config_section or handler_name.lower()

        # Use consolidated initialization pattern from InitializationMixin
        self.logger, config_dict = self.initialize_with_config(
            handler_name,
            self.config_section
        )

        # Store config for backward compatibility
        self.config = UnifiedConfigManager()
        self.handler_config = config_dict or {}

        self.logger.info(f"✅ {handler_name} initialized")

    def validate_request(self, request: Any) -> bool:
        """
        Validate request (override for custom validation).

        Args:
            request: Request to validate

        Returns:
            True if valid
        """
        if request is None:
            self.logger.error(f"{self.handler_name}: Request is None")
            return False
        return True

    def format_response(self, result: Any, success: bool = True, error: Optional[str] = None) -> dict[str, Any]:
        """
        Format handler response.

        Args:
            result: Result data
            success: Whether operation was successful
            error: Optional error message

        Returns:
            Formatted response dict
        """
        response = {
            "success": success,
            "handler": self.handler_name,
        }

        if success:
            response["data"] = result
        else:
            response["error"] = error or "Unknown error"

        return response

    def format_error(self, error_message: str, status_code: int = 400) -> tuple:
        """
        Format error response as Flask tuple (response, status_code).

        Args:
            error_message: Error message
            status_code: HTTP status code (default: 400)

        Returns:
            Tuple of (jsonified response, status_code)
        """
        from flask import jsonify
        error_response = self.format_response(
            result=None,
            success=False,
            error=error_message
        )
        return jsonify(error_response), status_code

    def handle_error(self, error: Exception, context: Optional[str] = None) -> dict[str, Any]:
        """
        Handle error and format error response.

        Uses ErrorHandlingMixin for consolidated error handling pattern.

        Args:
            error: Exception that occurred
            context: Optional context information

        Returns:
            Formatted error response
        """
        # Use consolidated error handling from ErrorHandlingMixin
        error_response = super().handle_error(
            error,
            context=context,
            logger=self.logger,
            component_name=self.handler_name
        )

        # Format as handler response
        return self.format_response(
            result=None,
            success=False,
            error=error_response.get("error", str(error))
        )

    def log_request(self, request: Any, level: str = "info") -> None:
        """
        Log request (override for custom logging).

        Args:
            request: Request to log
            level: Log level (info, debug, warning)
        """
        log_method = getattr(self.logger, level, self.logger.info)
        log_method(f"{self.handler_name} request: {request}")
