"""
Error Handler Pattern - Converted from Express middleware
==========================================================

Centralized error handling with environment-aware error details.
"""
import logging
from typing import Optional
import os

logger = logging.getLogger(__name__)


class ErrorHandler:
    """Centralized error handler for Auto_Blogger services."""
    
    def __init__(self, show_stack_trace: Optional[bool] = None):
        """
        Initialize error handler.
        
        Args:
            show_stack_trace: If None, auto-detect from NODE_ENV/PYTHON_ENV
        """
        if show_stack_trace is None:
            env = os.getenv("PYTHON_ENV", os.getenv("NODE_ENV", "development"))
            self.show_stack_trace = env != "production"
        else:
            self.show_stack_trace = show_stack_trace
    
    def handle_error(self, error: Exception, context: Optional[dict] = None) -> dict:
        """
        Handle error and return formatted error response.
        
        Args:
            error: Exception to handle
            context: Additional context information
            
        Returns:
            Dictionary with error details
        """
        logger.error(f"Error: {error}", exc_info=True)
        
        error_response = {
            "message": str(error) or "Server Error",
            "error_type": type(error).__name__
        }
        
        if context:
            error_response["context"] = context
        
        if self.show_stack_trace:
            import traceback
            error_response["stack_trace"] = traceback.format_exc()
        
        return error_response
    
    def format_error_response(self, error: Exception, status_code: int = 500) -> dict:
        """
        Format error for API response.
        
        Args:
            error: Exception to format
            status_code: HTTP status code
            
        Returns:
            Formatted error dictionary
        """
        return {
            "status_code": status_code,
            "error": self.handle_error(error)
        }


# Global error handler instance
_error_handler = None


def get_error_handler() -> ErrorHandler:
    """Get global error handler instance."""
    global _error_handler
    if _error_handler is None:
        _error_handler = ErrorHandler()
    return _error_handler

