#!/usr/bin/env python3
"""
Error Handling Mixin - Code Consolidation
==========================================

<!-- SSOT Domain: core -->

Mixin class for common error handling patterns across base classes.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-12-04
License: MIT
"""

import logging
from typing import Any, Optional


class ErrorHandlingMixin:
    """
    Mixin for common error handling patterns.

    Provides:
    - Standardized error logging
    - Error response formatting
    - Error state management
    - Common error handling utilities

    Usage:
        class MyClass(ErrorHandlingMixin):
            def some_method(self):
                try:
                    # Operation
                    return self.format_success_response(result)
                except Exception as e:
                    return self.handle_error(e, "some_method")
    """

    def handle_error(
        self,
        error: Exception,
        context: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
        component_name: Optional[str] = None
    ) -> dict[str, Any]:
        """
        Handle error and format error response (consolidated pattern).

        This method consolidates the common error handling pattern used across
        BaseManager, BaseService, and BaseHandler classes.

        Args:
            error: Exception that occurred
            context: Optional context information (method name, operation, etc.)
            logger: Optional logger instance (if None, uses self.logger if available)
            component_name: Optional component name (if None, tries to get from self)

        Returns:
            Formatted error response dict
        """
        # Get logger
        if logger is None:
            logger = getattr(self, 'logger', None)
            if logger is None:
                logger = logging.getLogger(__name__)

        # Get component name
        if component_name is None:
            component_name = getattr(
                self,
                'manager_name',
                getattr(
                    self,
                    'service_name',
                    getattr(self, 'handler_name', 'Unknown')
                )
            )

        # Format error message
        error_msg = str(error)
        if context:
            error_msg = f"{context}: {error_msg}"

        # Log error
        logger.error(f"{component_name} error: {error_msg}")

        # Format error response
        return self.format_error_response(
            error_msg,
            component_name=component_name
        )

    def format_error_response(
        self,
        error_message: str,
        component_name: Optional[str] = None,
        additional_data: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """
        Format standardized error response.

        Args:
            error_message: Error message
            component_name: Optional component name
            additional_data: Optional additional error data

        Returns:
            Formatted error response dict
        """
        response = {
            "success": False,
            "error": error_message,
        }

        if component_name:
            response["component"] = component_name

        if additional_data:
            response.update(additional_data)

        return response

    def format_success_response(
        self,
        data: Any,
        component_name: Optional[str] = None,
        additional_data: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """
        Format standardized success response.

        Args:
            data: Result data
            component_name: Optional component name
            additional_data: Optional additional data

        Returns:
            Formatted success response dict
        """
        response = {
            "success": True,
            "data": data,
        }

        if component_name:
            response["component"] = component_name

        if additional_data:
            response.update(additional_data)

        return response

    def safe_execute(
        self,
        operation: callable,
        operation_name: str,
        default_return: Any = None,
        logger: Optional[logging.Logger] = None,
        component_name: Optional[str] = None
    ) -> Any:
        """
        Safely execute an operation with error handling (consolidated pattern).

        This method consolidates the common try/except pattern used across
        BaseManager, BaseService, and BaseHandler lifecycle methods.

        Args:
            operation: Callable to execute
            operation_name: Name of operation (for logging)
            default_return: Default return value on error
            logger: Optional logger instance
            component_name: Optional component name

        Returns:
            Operation result or default_return on error
        """
        try:
            return operation()
        except Exception as e:
            error_response = self.handle_error(
                e,
                context=operation_name,
                logger=logger,
                component_name=component_name
            )
            return default_return
