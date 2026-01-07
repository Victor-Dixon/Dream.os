#!/usr/bin/env python3
"""
Unified Service Base - Phase 4 Service Consolidation
====================================================

PHASE 4 CONSOLIDATION: Consolidates redundant service patterns across:
- Message Queue, Discord Bot, Twitch Bot, Auto Gas Pipeline

Reduces from 4+ different service base patterns to 1 unified base class.
Consolidates initialization, logging, lifecycle, configuration, and error handling.

Features:
- Standardized service initialization
- Unified configuration loading (env vars + files)
- Consistent logging interface
- Standardized lifecycle management
- Consolidated error handling
- Health monitoring interface

V2 Compliance: <400 lines
Author: Agent-2 (Architecture & Design) - Phase 4 Consolidation 2026-01-06
<!-- SSOT Domain: core -->
"""

import logging
import os
import json
import time
import threading
import psutil
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional, Callable
from datetime import datetime, timedelta

from .base.base_service import BaseService
from .unified_logging_system import UnifiedLoggingSystem


class UnifiedServiceConfig:
    """Unified configuration system for all services."""

    @staticmethod
    def load_config(service_name: str, schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Load configuration with unified approach."""
        config = {}

        # Load from environment variables (prefixed with service name)
        config.update(UnifiedServiceConfig._load_env_config(service_name))

        # Load from config files
        config.update(UnifiedServiceConfig._load_file_config(service_name))

        # Apply defaults from schema
        if schema and 'defaults' in schema:
            for key, default_value in schema['defaults'].items():
                if key not in config:
                    config[key] = default_value

        # Validate against schema if provided
        if schema:
            UnifiedServiceConfig._validate_config(config, schema)

        return config

    @staticmethod
    def _load_env_config(service_name: str) -> Dict[str, Any]:
        """Load configuration from environment variables."""
        config = {}
        prefix = f"{service_name.upper()}_"

        for key, value in os.environ.items():
            if key.startswith(prefix):
                config_key = key[len(prefix):].lower()
                # Try to parse as JSON first, then fallback to string
                try:
                    config[config_key] = json.loads(value)
                except (json.JSONDecodeError, TypeError):
                    config[config_key] = value

        return config

    @staticmethod
    def _load_file_config(service_name: str) -> Dict[str, Any]:
        """Load configuration from files."""
        config = {}

        # Look for service-specific config files
        config_paths = [
            Path.cwd() / f"{service_name}.json",
            Path.cwd() / f"{service_name}.yaml",
            Path.cwd() / "config" / f"{service_name}.json",
            Path.cwd() / "config" / f"{service_name}.yaml",
        ]

        for config_path in config_paths:
            if config_path.exists():
                try:
                    if config_path.suffix == '.json':
                        with open(config_path, 'r') as f:
                            file_config = json.load(f)
                    elif config_path.suffix == '.yaml':
                        import yaml
                        with open(config_path, 'r') as f:
                            file_config = yaml.safe_load(f)
                    else:
                        continue

                    config.update(file_config)
                    break  # Use first config file found

                except Exception as e:
                    logging.warning(f"Failed to load config from {config_path}: {e}")

        return config

    @staticmethod
    def _validate_config(config: Dict[str, Any], schema: Dict[str, Any]) -> None:
        """Validate configuration against schema."""
        if 'required' in schema:
            for required_key in schema['required']:
                if required_key not in config:
                    raise ValueError(f"Required config key missing: {required_key}")

        if 'types' in schema:
            for key, expected_type in schema['types'].items():
                if key in config:
                    if not isinstance(config[key], expected_type):
                        raise TypeError(f"Config key {key} has wrong type. Expected {expected_type}, got {type(config[key])}")


class ServiceLifecycleManager:
    """Unified lifecycle management for all services."""

    def __init__(self, service: 'UnifiedServiceBase'):
        self.service = service
        self._running = False
        self._start_time: Optional[float] = None
        self._thread: Optional[threading.Thread] = None
        self._process: Optional[psutil.Process] = None
        self._health_check_interval = 30  # seconds
        self._last_health_check = 0
        self._restart_count = 0
        self._max_restarts = 3

    def start(self, mode: str = "foreground") -> bool:
        """Start service with specified mode."""
        try:
            if mode == "background":
                return self._start_background()
            else:
                return self._start_foreground()
        except Exception as e:
            self.service.logger.error(f"Failed to start service: {e}")
            return False

    def stop(self) -> bool:
        """Stop service gracefully."""
        try:
            self._running = False

            if self._thread and self._thread.is_alive():
                self._thread.join(timeout=10)

            if self._process:
                try:
                    self._process.terminate()
                    self._process.wait(timeout=5)
                except psutil.TimeoutExpired:
                    self._process.kill()

            self.service.logger.info("Service stopped successfully")
            return True

        except Exception as e:
            self.service.logger.error(f"Error stopping service: {e}")
            return False

    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive service status."""
        status = {
            "name": self.service.service_name,
            "running": self._running,
            "uptime": self._get_uptime(),
            "restart_count": self._restart_count,
        }

        # Add health information
        health_status = self._check_health()
        status.update(health_status)

        # Add resource usage if running
        if self._running and self._process:
            try:
                status["resources"] = {
                    "cpu_percent": self._process.cpu_percent(),
                    "memory_mb": self._process.memory_info().rss / 1024 / 1024,
                    "threads": self._process.num_threads(),
                }
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                status["resources"] = None

        return status

    def _start_foreground(self) -> bool:
        """Start service in foreground thread."""
        self._running = True
        self._start_time = time.time()

        try:
            self._process = psutil.Process()
            self.service.on_start()
            self._thread = threading.Thread(target=self._run_service_loop, daemon=True)
            self._thread.start()
            self.service.logger.info("Service started in foreground mode")
            return True
        except Exception as e:
            self._running = False
            self.service.logger.error(f"Failed to start foreground service: {e}")
            return False

    def _start_background(self) -> bool:
        """Start service in background process."""
        # For background mode, we'd typically use subprocess
        # For now, implement as foreground with background flag
        self.service.logger.info("Background mode requested - starting as foreground service")
        return self._start_foreground()

    def _run_service_loop(self) -> None:
        """Main service execution loop."""
        try:
            while self._running:
                try:
                    self.service.run_once()
                except Exception as e:
                    self.service.logger.error(f"Error in service loop: {e}")
                    if self._should_restart():
                        self._restart_service()
                    else:
                        break

                # Health check interval
                time.sleep(self.service.loop_interval)

        except Exception as e:
            self.service.logger.error(f"Fatal error in service loop: {e}")
        finally:
            self.service.on_stop()

    def _check_health(self) -> Dict[str, Any]:
        """Check service health."""
        current_time = time.time()

        # Only check health periodically
        if current_time - self._last_health_check < self._health_check_interval:
            return {"health_status": "cached"}

        self._last_health_check = current_time

        try:
            # Call service-specific health check
            if hasattr(self.service, 'check_health'):
                health_result = self.service.check_health()
                if isinstance(health_result, dict):
                    return health_result
                elif isinstance(health_result, bool):
                    return {"healthy": health_result, "status": "healthy" if health_result else "unhealthy"}
                else:
                    return {"healthy": True, "status": "unknown"}
            else:
                # Basic health check - service is running
                return {"healthy": self._running, "status": "running" if self._running else "stopped"}

        except Exception as e:
            return {"healthy": False, "status": "error", "error": str(e)}

    def _get_uptime(self) -> Optional[float]:
        """Get service uptime in seconds."""
        if self._start_time:
            return time.time() - self._start_time
        return None

    def _should_restart(self) -> bool:
        """Determine if service should be restarted."""
        return self._restart_count < self._max_restarts

    def _restart_service(self) -> None:
        """Restart the service."""
        self._restart_count += 1
        self.service.logger.info(f"Restarting service (attempt {self._restart_count})")

        try:
            self.stop()
            time.sleep(2)  # Brief pause before restart
            self.start()
        except Exception as e:
            self.service.logger.error(f"Failed to restart service: {e}")


class UnifiedServiceBase(BaseService, ABC):
    """
    Unified base class for all services consolidating common patterns.

    PHASE 4 CONSOLIDATION: Consolidates redundant patterns from:
    - MessageQueue, DiscordBot, TwitchBot, AutoGasPipelineSystem

    Features:
    - Standardized initialization with configuration schema
    - Unified logging via UnifiedLoggingSystem
    - Consistent lifecycle management
    - Health monitoring interface
    - Error handling with recovery
    - Configuration hot-reload capability
    """

    def __init__(
        self,
        service_name: str,
        config_schema: Optional[Dict[str, Any]] = None,
        loop_interval: float = 1.0
    ):
        """Initialize unified service base."""
        # Initialize BaseService first
        super().__init__(service_name)

        # Service configuration
        self.service_name = service_name
        self.config_schema = config_schema or {}
        self.loop_interval = loop_interval

        # Load configuration
        self.config = UnifiedServiceConfig.load_config(service_name, config_schema)

        # Setup unified logging
        self.logger = self._setup_unified_logging()

        # Initialize lifecycle manager
        self.lifecycle_manager = ServiceLifecycleManager(self)

        # Service state
        self._initialized = False

        # Initialize service-specific components
        self._initialize_service()

        self._initialized = True
        self.logger.info(f"✅ {service_name} initialized with unified patterns")

    def _setup_unified_logging(self) -> logging.Logger:
        """Setup unified logging for the service."""
        try:
            # Try unified logging system first
            return UnifiedLoggingSystem.get_logger(self.service_name)
        except Exception:
            # Fallback to standard logging
            logger = logging.getLogger(self.service_name)
            if not logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter(
                    f'%(asctime)s | %(name)s | %(levelname)s | %(message)s'
                )
                handler.setFormatter(formatter)
                logger.addHandler(handler)
                logger.setLevel(logging.INFO)
            return logger

    def _initialize_service(self) -> None:
        """Initialize service-specific components. Override in subclasses."""
        pass

    def start(self, mode: str = "foreground") -> bool:
        """Start the service."""
        self.logger.info(f"🚀 Starting {self.service_name} in {mode} mode")
        success = self.lifecycle_manager.start(mode)
        if success:
            self.on_start()
        return success

    def stop(self) -> bool:
        """Stop the service."""
        self.logger.info(f"🛑 Stopping {self.service_name}")
        success = self.lifecycle_manager.stop()
        if success:
            self.on_stop()
        return success

    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive service status."""
        return self.lifecycle_manager.get_status()

    def check_health(self) -> Dict[str, Any]:
        """Check service health. Override in subclasses for custom health checks."""
        return {
            "healthy": True,
            "status": "operational",
            "timestamp": datetime.now().isoformat()
        }

    def on_start(self) -> None:
        """Called when service starts. Override in subclasses."""
        self.logger.info(f"✅ {self.service_name} started successfully")

    def on_stop(self) -> None:
        """Called when service stops. Override in subclasses."""
        self.logger.info(f"🛑 {self.service_name} stopped")

    @abstractmethod
    def run_once(self) -> None:
        """Main service execution logic. Must be implemented by subclasses."""
        pass

    def reload_config(self) -> bool:
        """Reload service configuration."""
        try:
            old_config = self.config.copy()
            self.config = UnifiedServiceConfig.load_config(
                self.service_name, self.config_schema
            )

            # Log configuration changes
            if old_config != self.config:
                self.logger.info("🔄 Configuration reloaded")
                return True
            else:
                self.logger.info("🔄 Configuration unchanged")
                return False

        except Exception as e:
            self.logger.error(f"Failed to reload configuration: {e}")
            return False

    def get_config_value(self, key: str, default: Any = None) -> Any:
        """Get configuration value with fallback."""
        return self.config.get(key, default)

    def set_config_value(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self.config[key] = value
        self.logger.debug(f"Configuration updated: {key} = {value}")

    def cleanup_resources(self) -> None:
        """Cleanup service resources. Override in subclasses."""
        pass

    def __del__(self):
        """Destructor - ensure cleanup."""
        try:
            self.cleanup_resources()
        except Exception:
            pass  # Ignore errors during cleanup


# Export unified components
__all__ = [
    "UnifiedServiceBase",
    "UnifiedServiceConfig",
    "ServiceLifecycleManager",
]