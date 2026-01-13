"""
Engine Base Helpers - SSOT for Common Engine Patterns
=====================================================

<!-- SSOT Domain: integration -->

Single Source of Truth for common engine initialization, error handling,
and lifecycle management patterns used across all core engines.

Consolidates duplicate patterns found in 14 engine implementations:
- Duplicate initialization logic
- Repeated error handling
- Common cleanup patterns
- Standard status reporting

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-03
V2 Compliant: Yes (<300 lines)
"""

from __future__ import annotations

from typing import Any, Callable

from .contracts import EngineContext, EngineResult


class EngineBaseMixin:
    """
    Base mixin providing common engine functionality.
    
    SSOT for:
    - Initialization state management
    - Standard error handling
    - Common lifecycle methods
    """
    
    def __init__(self):
        """Initialize engine with common state."""
        self.is_initialized = False
    
    def _standard_initialize(
        self, 
        context: EngineContext, 
        engine_name: str
    ) -> bool:
        """
        Standard initialization pattern - SSOT for all engines.
        
        Args:
            context: Engine context
            engine_name: Name of engine for logging
            
        Returns:
            True if initialized successfully
        """
        try:
            self.is_initialized = True
            context.logger.info(f"{engine_name} initialized")
            return True
        except Exception as e:
            context.logger.error(f"Failed to initialize {engine_name}: {e}")
            return False
    
    def _standard_cleanup(
        self, 
        context: EngineContext, 
        engine_name: str
    ) -> bool:
        """
        Standard cleanup pattern - SSOT for all engines.
        
        Args:
            context: Engine context
            engine_name: Name of engine for logging
            
        Returns:
            True if cleaned up successfully
        """
        try:
            self.is_initialized = False
            context.logger.info(f"{engine_name} cleaned up")
            return True
        except Exception as e:
            context.logger.error(f"Failed to cleanup {engine_name}: {e}")
            return False
    
    def _handle_operation_error(
        self, 
        error: Exception, 
        operation: str = "operation"
    ) -> EngineResult:
        """
        Standard error handling - SSOT for all engines.
        
        Args:
            error: Exception that occurred
            operation: Name of operation that failed
            
        Returns:
            Standard error EngineResult
        """
        return EngineResult(
            success=False,
            data={},
            metrics={},
            error=f"{operation} failed: {str(error)}",
        )
    
    def _route_operation(
        self,
        context: EngineContext,
        payload: dict[str, Any],
        operation_map: dict[str, Callable[[EngineContext, dict[str, Any]], EngineResult]],
        default_error: str = "Unknown operation"
    ) -> EngineResult:
        """
        Standard operation routing - SSOT for all engines.
        
        Args:
            context: Engine context
            payload: Operation payload
            operation_map: Map of operation names to handler functions
            default_error: Error message for unknown operations
            
        Returns:
            EngineResult from operation handler
        """
        try:
            operation = payload.get("operation", "unknown")
            handler = operation_map.get(operation)
            
            if handler:
                return handler(context, payload)
            else:
                return EngineResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"{default_error}: {operation}",
                )
        except Exception as e:
            return self._handle_operation_error(e, operation)


def create_error_result(error: str, operation: str = "operation") -> EngineResult:
    """
    Create standard error result - SSOT utility function.
    
    Args:
        error: Error message
        operation: Operation name
        
    Returns:
        Standard error EngineResult
    """
    return EngineResult(
        success=False,
        data={},
        metrics={},
        error=f"{operation}: {error}",
    )

