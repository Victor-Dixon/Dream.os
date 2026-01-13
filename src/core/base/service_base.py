#!/usr/bin/env python3
"""
Service Base Class - SSOT Implementation
========================================

Single Source of Truth for service layer patterns.

<!-- SSOT Domain: service-architecture -->

Provides:
- Standardized logging setup
- Error handling patterns
- Configuration management
- Lifecycle management
- Metrics collection

V2 Compliant: Eliminates 552+ duplicate logger setups
Author: Agent-8 (SSOT & System Integration)
Date: 2026-01-12
"""

import logging
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from contextlib import contextmanager


@dataclass
class ServiceMetrics:
    """Standardized metrics collection for services."""
    service_name: str
    start_time: float = field(default_factory=time.time)
    operations_completed: int = 0
    errors_encountered: int = 0
    average_operation_time: float = 0.0
    last_operation_time: float = 0.0

    def record_operation(self, duration: float) -> None:
        """Record a completed operation."""
        self.operations_completed += 1
        self.last_operation_time = duration
        # Rolling average calculation
        if self.operations_completed == 1:
            self.average_operation_time = duration
        else:
            self.average_operation_time = (
                (self.average_operation_time * (self.operations_completed - 1) + duration)
                / self.operations_completed
            )

    def record_error(self) -> None:
        """Record an error occurrence."""
        self.errors_encountered += 1


class ServiceError(Exception):
    """Base exception for service operations."""
    def __init__(self, service_name: str, operation: str, details: str = ""):
        self.service_name = service_name
        self.operation = operation
        self.details = details
        super().__init__(f"Service '{service_name}' failed on '{operation}': {details}")


class ConfigurationError(ServiceError):
    """Configuration-related service error."""
    pass


class OperationError(ServiceError):
    """Operation-related service error."""
    pass


class BaseService(ABC):
    """
    Single Source of Truth for all service implementations.

    Eliminates repetitive patterns:
    - Logger setup (552+ duplications)
    - Error handling patterns
    - Configuration management
    - Lifecycle management
    - Metrics collection

    Usage:
        class MyService(BaseService):
            def __init__(self, config: Dict[str, Any]):
                super().__init__("my_service", config)

            @BaseService.operation_handler
            def do_work(self) -> bool:
                # Work implementation
                return True
    """

    def __init__(self, service_name: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize service with standardized setup.

        Args:
            service_name: Unique identifier for this service instance
            config: Service configuration dictionary
        """
        self.service_name = service_name
        self.config = config or {}
        self.metrics = ServiceMetrics(service_name)

        # SSOT Logger Setup - eliminates 552+ duplicate patterns
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        self.logger.setLevel(getattr(logging, self.config.get('log_level', 'INFO').upper()))

        # Configure handler if none exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                f'%(asctime)s | %(levelname)s | {service_name} | %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        self.logger.info(f"🚀 Service '{service_name}' initialized")

    @abstractmethod
    def validate_config(self) -> bool:
        """
        Validate service configuration.

        Returns:
            True if configuration is valid, False otherwise
        """
        pass

    @abstractmethod
    async def start(self) -> bool:
        """
        Start the service.

        Returns:
            True if service started successfully, False otherwise
        """
        pass

    @abstractmethod
    async def stop(self) -> bool:
        """
        Stop the service.

        Returns:
            True if service stopped successfully, False otherwise
        """
        pass

    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """
        Perform health check.

        Returns:
            Dictionary with health status information
        """
        pass

    @staticmethod
    def operation_handler(operation_name: Optional[str] = None):
        """
        Decorator for standardized operation handling.

        Provides:
        - Timing metrics
        - Error handling
        - Logging
        - Metrics collection

        Usage:
            @BaseService.operation_handler
            def my_operation(self):
                # Operation implementation
                pass

            @BaseService.operation_handler("custom_name")
            def another_operation(self):
                # Operation implementation
                pass
        """
        def decorator(func: Callable):
            op_name = operation_name or func.__name__

            def wrapper(self, *args, **kwargs):
                start_time = time.time()
                try:
                    self.logger.debug(f"Starting operation: {op_name}")
                    result = func(self, *args, **kwargs)
                    duration = time.time() - start_time
                    self.metrics.record_operation(duration)
                    self.logger.debug(f"Completed operation: {op_name} in {duration:.3f}s")
                    return result
                except Exception as e:
                    duration = time.time() - start_time
                    self.metrics.record_error()
                    self.logger.error(f"Operation '{op_name}' failed after {duration:.3f}s: {e}")
                    raise OperationError(self.service_name, op_name, str(e)) from e

            return wrapper
        return decorator

    @contextmanager
    def error_context(self, operation: str):
        """
        Context manager for error handling in operations.

        Usage:
            with self.error_context("database_operation"):
                # Risky operation
                pass
        """
        try:
            yield
        except Exception as e:
            self.metrics.record_error()
            self.logger.error(f"Error in {operation}: {e}")
            raise OperationError(self.service_name, operation, str(e)) from e

    def get_metrics(self) -> Dict[str, Any]:
        """
        Get current service metrics.

        Returns:
            Dictionary with service metrics
        """
        return {
            'service_name': self.service_name,
            'uptime_seconds': time.time() - self.metrics.start_time,
            'operations_completed': self.metrics.operations_completed,
            'errors_encountered': self.metrics.errors_encountered,
            'average_operation_time': self.metrics.average_operation_time,
            'last_operation_time': self.metrics.last_operation_time,
            'error_rate': (
                self.metrics.errors_encountered / max(self.metrics.operations_completed, 1)
            ),
        }

    def reset_metrics(self) -> None:
        """Reset service metrics."""
        self.metrics = ServiceMetrics(self.service_name)
        self.logger.info(f"Metrics reset for service '{self.service_name}'")


class ServiceRegistry:
    """
    Registry for managing service instances.

    Provides centralized service management and coordination.
    """

    def __init__(self):
        self.services: Dict[str, BaseService] = {}
        self.logger = logging.getLogger(__name__)

    def register(self, service: BaseService) -> None:
        """
        Register a service instance.

        Args:
            service: Service instance to register
        """
        if service.service_name in self.services:
            raise ValueError(f"Service '{service.service_name}' already registered")

        self.services[service.service_name] = service
        self.logger.info(f"Registered service: {service.service_name}")

    def unregister(self, service_name: str) -> None:
        """
        Unregister a service.

        Args:
            service_name: Name of service to unregister
        """
        if service_name in self.services:
            del self.services[service_name]
            self.logger.info(f"Unregistered service: {service_name}")

    def get_service(self, service_name: str) -> Optional[BaseService]:
        """
        Get a registered service.

        Args:
            service_name: Name of service to retrieve

        Returns:
            Service instance or None if not found
        """
        return self.services.get(service_name)

    def get_all_services(self) -> List[BaseService]:
        """
        Get all registered services.

        Returns:
            List of all registered service instances
        """
        return list(self.services.values())

    async def start_all(self) -> Dict[str, bool]:
        """
        Start all registered services.

        Returns:
            Dictionary mapping service names to start success status
        """
        results = {}
        for service in self.services.values():
            try:
                results[service.service_name] = await service.start()
            except Exception as e:
                self.logger.error(f"Failed to start service '{service.service_name}': {e}")
                results[service.service_name] = False
        return results

    async def stop_all(self) -> Dict[str, bool]:
        """
        Stop all registered services.

        Returns:
            Dictionary mapping service names to stop success status
        """
        results = {}
        for service in reversed(list(self.services.values())):  # Reverse order for dependencies
            try:
                results[service.service_name] = await service.stop()
            except Exception as e:
                self.logger.error(f"Failed to stop service '{service.service_name}': {e}")
                results[service.service_name] = False
        return results

    def health_check_all(self) -> Dict[str, Dict[str, Any]]:
        """
        Perform health check on all services.

        Returns:
            Dictionary mapping service names to health check results
        """
        results = {}
        for service in self.services.values():
            try:
                results[service.service_name] = service.health_check()
            except Exception as e:
                self.logger.error(f"Health check failed for '{service.service_name}': {e}")
                results[service.service_name] = {'status': 'error', 'error': str(e)}
        return results


# Global service registry instance
service_registry = ServiceRegistry()


__all__ = [
    "BaseService",
    "ServiceMetrics",
    "ServiceError",
    "ConfigurationError",
    "OperationError",
    "ServiceRegistry",
    "service_registry",
]