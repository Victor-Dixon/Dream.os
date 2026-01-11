#!/usr/bin/env python3
"""
Base Service Classes - Agent Cellphone V2
=========================================

Standardized service architecture to eliminate duplicate patterns
across service implementations.

<!-- SSOT Domain: core -->

Author: Agent-1 (Integration & Core Systems)
Date: 2026-01-11

Usage:
    # Replace service boilerplate with standardized base classes

    from core.service_base import BaseService, APIService

    class MyService(BaseService):
        async def initialize(self) -> bool:
            # Service-specific initialization
            return True

        async def shutdown(self) -> bool:
            # Service-specific cleanup
            return True

        # Inherits standard health_check(), logging, error handling
"""

import asyncio
import time
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field

from .logging_utils import get_logger, create_service_logger
from .error_handling import ErrorHandler, handle_errors


@dataclass
class ServiceConfig:
    """Standardized service configuration."""
    name: str
    version: str = "1.0.0"
    description: str = ""
    dependencies: List[str] = field(default_factory=list)
    health_check_interval: int = 30  # seconds
    max_startup_time: int = 30  # seconds
    enable_metrics: bool = True
    enable_health_checks: bool = True


@dataclass
class ServiceMetrics:
    """Service performance metrics."""
    requests_total: int = 0
    requests_success: int = 0
    requests_error: int = 0
    uptime_seconds: float = 0
    last_request_time: Optional[datetime] = None
    average_response_time: float = 0
    error_rate: float = 0


class ServiceState:
    """Enumeration of service states."""
    INITIALIZING = "initializing"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"
    DEGRADED = "degraded"


class BaseService(ABC):
    """
    Base class for all services providing common functionality.

    Eliminates duplicate service initialization, health checks, and lifecycle management.
    """

    def __init__(
        self,
        config: ServiceConfig,
        instance_id: Optional[str] = None
    ):
        """Initialize base service with standardized setup."""
        self.config = config
        self.instance_id = instance_id or f"{config.name}-{id(self)}"

        # Initialize logging
        self.logger = create_service_logger(
            service_name=config.name,
            service_version=config.version,
            instance_id=self.instance_id
        )

        # Service state management
        self._state = ServiceState.INITIALIZING
        self._start_time: Optional[datetime] = None
        self._stop_time: Optional[datetime] = None
        self._last_health_check: Optional[datetime] = None
        self._health_status = "unknown"

        # Metrics tracking
        self.metrics = ServiceMetrics()

        # Dependencies tracking
        self._dependencies_ready = False
        self._dependency_states: Dict[str, bool] = {}

        # Lifecycle hooks
        self._startup_tasks: List[callable] = []
        self._shutdown_tasks: List[callable] = []

        self.logger.info(f"Service {config.name} v{config.version} initialized")

    @property
    def state(self) -> str:
        """Get current service state."""
        return self._state

    @property
    def is_running(self) -> bool:
        """Check if service is running."""
        return self._state == ServiceState.RUNNING

    @property
    def uptime(self) -> Optional[timedelta]:
        """Get service uptime."""
        if self._start_time and not self._stop_time:
            return datetime.utcnow() - self._start_time
        return None

    async def start(self) -> bool:
        """
        Start the service with standardized lifecycle.

        This replaces duplicate startup patterns across services.
        """
        if self._state != ServiceState.INITIALIZING:
            self.logger.warning(f"Service already in state {self._state}")
            return False

        self.logger.info(f"Starting service {self.config.name}")
        self._state = ServiceState.STARTING
        self._start_time = datetime.utcnow()

        try:
            # Check dependencies
            if not await self._check_dependencies():
                self.logger.error("Dependencies not ready, aborting startup")
                self._state = ServiceState.ERROR
                return False

            # Run startup tasks
            for task in self._startup_tasks:
                await ErrorHandler.safe_execute_async(
                    task(),
                    log_errors=True,
                    context=f"startup task in {self.config.name}"
                )

            # Service-specific initialization
            if not await self.initialize():
                self.logger.error("Service-specific initialization failed")
                self._state = ServiceState.ERROR
                return False

            # Start health check loop if enabled
            if self.config.enable_health_checks:
                asyncio.create_task(self._health_check_loop())

            # Start metrics collection if enabled
            if self.config.enable_metrics:
                asyncio.create_task(self._metrics_loop())

            self._state = ServiceState.RUNNING
            self._health_status = "healthy"
            self.logger.info(f"Service {self.config.name} started successfully")

            return True

        except Exception as e:
            self.logger.error(f"Failed to start service: {e}", exc_info=True)
            self._state = ServiceState.ERROR
            self._health_status = "error"
            return False

    async def stop(self) -> bool:
        """
        Stop the service with graceful shutdown.

        This replaces duplicate shutdown patterns across services.
        """
        if self._state in [ServiceState.STOPPING, ServiceState.STOPPED]:
            return True

        self.logger.info(f"Stopping service {self.config.name}")
        self._state = ServiceState.STOPPING

        try:
            # Run shutdown tasks in reverse order
            for task in reversed(self._shutdown_tasks):
                await ErrorHandler.safe_execute_async(
                    task(),
                    log_errors=True,
                    context=f"shutdown task in {self.config.name}"
                )

            # Service-specific shutdown
            await self.shutdown()

            self._state = ServiceState.STOPPED
            self._stop_time = datetime.utcnow()
            self._health_status = "stopped"

            uptime = self.uptime
            uptime_str = f"{uptime.total_seconds():.1f}s" if uptime else "unknown"
            self.logger.info(f"Service {self.config.name} stopped (uptime: {uptime_str})")

            return True

        except Exception as e:
            self.logger.error(f"Error during service shutdown: {e}", exc_info=True)
            self._state = ServiceState.ERROR
            return False

    @abstractmethod
    async def initialize(self) -> bool:
        """
        Service-specific initialization logic.

        Subclasses must implement this method.
        """
        pass

    @abstractmethod
    async def shutdown(self) -> bool:
        """
        Service-specific shutdown logic.

        Subclasses must implement this method.
        """
        pass

    def health_check(self) -> Dict[str, Any]:
        """
        Standardized health check implementation.

        This replaces duplicate health check patterns across services.
        """
        uptime = self.uptime
        uptime_seconds = uptime.total_seconds() if uptime else 0

        health_data = {
            "service": self.config.name,
            "version": self.config.version,
            "instance_id": self.instance_id,
            "state": self._state,
            "status": self._health_status,
            "uptime_seconds": uptime_seconds,
            "last_health_check": self._last_health_check.isoformat() if self._last_health_check else None,
            "timestamp": datetime.utcnow().isoformat(),
        }

        # Add metrics if enabled
        if self.config.enable_metrics:
            health_data.update({
                "metrics": {
                    "requests_total": self.metrics.requests_total,
                    "requests_success": self.metrics.requests_success,
                    "requests_error": self.metrics.requests_error,
                    "error_rate": self.metrics.error_rate,
                    "average_response_time": self.metrics.average_response_time,
                }
            })

        # Add dependency status
        if self.config.dependencies:
            health_data["dependencies"] = self._dependency_states

        return health_data

    def add_startup_task(self, task: callable) -> None:
        """Add a startup task to be executed during service start."""
        self._startup_tasks.append(task)

    def add_shutdown_task(self, task: callable) -> None:
        """Add a shutdown task to be executed during service stop."""
        self._shutdown_tasks.append(task)

    async def _check_dependencies(self) -> bool:
        """Check if all service dependencies are ready."""
        if not self.config.dependencies:
            self._dependencies_ready = True
            return True

        self.logger.info(f"Checking {len(self.config.dependencies)} dependencies")

        # In a real implementation, this would check actual service health
        # For now, we'll simulate dependency checking
        for dependency in self.config.dependencies:
            # Simulate dependency check
            self._dependency_states[dependency] = True  # Assume all dependencies are ready

        self._dependencies_ready = all(self._dependency_states.values())
        return self._dependencies_ready

    async def _health_check_loop(self) -> None:
        """Background health check loop."""
        while self._state == ServiceState.RUNNING:
            try:
                # Perform health check
                health = self.health_check()
                self._last_health_check = datetime.utcnow()

                # Update health status based on checks
                if health["state"] == ServiceState.RUNNING:
                    self._health_status = "healthy"
                else:
                    self._health_status = "degraded"

            except Exception as e:
                self.logger.error(f"Health check failed: {e}")
                self._health_status = "error"

            await asyncio.sleep(self.config.health_check_interval)

    async def _metrics_loop(self) -> None:
        """Background metrics collection loop."""
        while self._state == ServiceState.RUNNING:
            try:
                # Update uptime metrics
                if self._start_time:
                    self.metrics.uptime_seconds = (datetime.utcnow() - self._start_time).total_seconds()

                # Calculate error rate
                if self.metrics.requests_total > 0:
                    self.metrics.error_rate = self.metrics.requests_error / self.metrics.requests_total

            except Exception as e:
                self.logger.error(f"Metrics collection failed: {e}")

            await asyncio.sleep(60)  # Update every minute


class APIService(BaseService):
    """
    Base class for API services (FastAPI, Flask, etc.).

    Provides common API service functionality.
    """

    def __init__(self, config: ServiceConfig, host: str = "0.0.0.0", port: int = 8000):
        super().__init__(config)
        self.host = host
        self.port = port
        self._server = None

    async def initialize(self) -> bool:
        """Initialize API service."""
        try:
            # Create API application (subclass must implement)
            self._app = await self.create_app()

            # Add common middleware
            await self._setup_middleware()

            # Add health check routes
            await self._add_health_routes()

            self.logger.info(f"API service initialized on {self.host}:{self.port}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize API service: {e}")
            return False

    async def shutdown(self) -> bool:
        """Shutdown API service."""
        try:
            if self._server:
                await self._server.shutdown()
                self.logger.info("API server shut down gracefully")
            return True
        except Exception as e:
            self.logger.error(f"Error shutting down API service: {e}")
            return False

    @abstractmethod
    async def create_app(self):
        """Create the API application (FastAPI, Flask, etc.)."""
        pass

    async def _setup_middleware(self) -> None:
        """Setup common middleware for API services."""
        # CORS, logging, error handling middleware would be added here
        # Implementation depends on the specific API framework
        pass

    async def _add_health_routes(self) -> None:
        """Add health check routes to the API."""
        # Implementation depends on the specific API framework
        pass

    async def start_server(self) -> None:
        """Start the API server."""
        # Implementation depends on the specific API framework
        pass


class BackgroundService(BaseService):
    """
    Base class for background services (workers, processors, etc.).

    Provides common background service functionality.
    """

    def __init__(self, config: ServiceConfig):
        super().__init__(config)
        self._background_tasks: List[asyncio.Task] = []

    async def initialize(self) -> bool:
        """Initialize background service."""
        try:
            # Start background processing tasks
            await self.start_background_tasks()
            self.logger.info("Background service initialized")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize background service: {e}")
            return False

    async def shutdown(self) -> bool:
        """Shutdown background service."""
        try:
            # Cancel all background tasks
            for task in self._background_tasks:
                if not task.done():
                    task.cancel()

            # Wait for tasks to complete
            await asyncio.gather(*self._background_tasks, return_exceptions=True)

            self.logger.info("Background service shut down gracefully")
            return True
        except Exception as e:
            self.logger.error(f"Error shutting down background service: {e}")
            return False

    @abstractmethod
    async def start_background_tasks(self) -> None:
        """Start the background processing tasks."""
        pass

    def add_background_task(self, task: asyncio.Task) -> None:
        """Add a background task to track."""
        self._background_tasks.append(task)


# Factory functions for easy service creation
def create_basic_service(
    name: str,
    version: str = "1.0.0",
    description: str = "",
    dependencies: Optional[List[str]] = None
) -> ServiceConfig:
    """Factory function to create a basic service configuration."""
    return ServiceConfig(
        name=name,
        version=version,
        description=description,
        dependencies=dependencies or []
    )


def create_api_service(
    name: str,
    host: str = "0.0.0.0",
    port: int = 8000,
    version: str = "1.0.0",
    dependencies: Optional[List[str]] = None
) -> tuple[ServiceConfig, str, int]:
    """Factory function to create an API service configuration."""
    config = ServiceConfig(
        name=name,
        version=version,
        dependencies=dependencies or []
    )
    return config, host, port


# Migration helper
def migrate_service_patterns():
    """
    Helper function to assist with migrating existing service patterns.

    This can be used to find and replace old service patterns.
    """
    print("🔍 Service Migration Helper")
    print("Replace these patterns:")
    print()
    print("OLD SERVICE PATTERN:")
    print("  class MyService:")
    print("      def __init__(self):")
    print("          self.logger = logging.getLogger(__name__)")
    print("          self.healthy = True")
    print()
    print("      def health_check(self):")
    print("          return {'status': 'ok' if self.healthy else 'error'}")
    print()
    print("      async def start(self):")
    print("          # Custom startup logic")
    print("          pass")
    print()
    print("NEW SERVICE PATTERN:")
    print("  from core.service_base import BaseService, create_basic_service")
    print()
    print("  class MyService(BaseService):")
    print("      def __init__(self):")
    print("          config = create_basic_service(")
    print("              name='my-service',")
    print("              version='1.0.0',")
    print("              description='My service description'")
    print("          )")
    print("          super().__init__(config)")
    print()
    print("      async def initialize(self) -> bool:")
    print("          # Custom startup logic")
    print("          return True")
    print()
    print("      async def shutdown(self) -> bool:")
    print("          # Custom cleanup logic")
    print("          return True")
    print()
    print("      # Inherits health_check(), logging, error handling")
    print()
    print("Benefits:")
    print("  ✅ Standardized service lifecycle")
    print("  ✅ Automatic health checks and metrics")
    print("  ✅ Consistent error handling and logging")
    print("  ✅ Dependency management")
    print("  ✅ Background task management")


__all__ = [
    "BaseService",
    "APIService",
    "BackgroundService",
    "ServiceConfig",
    "ServiceMetrics",
    "ServiceState",
    "create_basic_service",
    "create_api_service",
    "migrate_service_patterns",
]