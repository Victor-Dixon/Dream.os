#!/usr/bin/env python3
"""
Base Handler Class - Code Consolidation
=======================================

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

from src.core.config.config_manager import UnifiedConfigManager
from src.core.logging.unified_logging_system import UnifiedLoggingSystem


class BaseHandler(ABC):
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
        
        Args:
            handler_name: Name of the handler (for logging)
            config_section: Optional config section name
        """
        self.handler_name = handler_name
        self.config_section = config_section or handler_name.lower()
        
        # Initialize logging
        self.logger = UnifiedLoggingSystem(handler_name).get_logger()
        
        # Load configuration
        self.config = UnifiedConfigManager()
        self.handler_config = self.config.get_section(self.config_section, {})
        
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
    
    def handle_error(self, error: Exception, context: Optional[str] = None) -> dict[str, Any]:
        """
        Handle error and format error response.
        
        Args:
            error: Exception that occurred
            context: Optional context information
        
        Returns:
            Formatted error response
        """
        error_msg = str(error)
        if context:
            error_msg = f"{context}: {error_msg}"
        
        self.logger.error(f"{self.handler_name} error: {error_msg}")
        
        return self.format_response(
            result=None,
            success=False,
            error=error_msg
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

