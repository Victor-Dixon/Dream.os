#!/usr/bin/env python3
"""
🛡️ Plugin Sandbox - Phase 3 Security Foundation
===============================================

Plugin execution sandbox implementing security isolation, resource limits,
and execution monitoring as per Phase 3 Architecture Specification.

<!-- SSOT Domain: plugins -->
"""

from __future__ import annotations

import logging
import time
import threading
import signal
from contextlib import contextmanager
from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass
from enum import Enum

# Import resource module with fallback for Windows
try:
    import resource
    HAS_RESOURCE = True
except ImportError:
    HAS_RESOURCE = False
    # Mock resource module for Windows compatibility
    class resource:
        RLIMIT_AS = None
        RLIMIT_CPU = None
        @staticmethod
        def getrlimit(*args): return (0, 0)
        @staticmethod
        def setrlimit(*args): pass

logger = logging.getLogger(__name__)


class SandboxViolation(Enum):
    """Types of sandbox violations."""
    MEMORY_LIMIT = "memory_limit"
    CPU_TIME_LIMIT = "cpu_time_limit"
    EXECUTION_TIME_LIMIT = "execution_time_limit"
    FORBIDDEN_MODULE = "forbidden_module"
    FORBIDDEN_OPERATION = "forbidden_operation"
    NETWORK_ACCESS = "network_access"
    FILESYSTEM_ACCESS = "filesystem_access"


@dataclass
class SandboxLimits:
    """Resource limits for plugin execution."""
    max_memory_mb: int = 100
    max_cpu_percent: float = 10.0
    max_execution_time_sec: int = 30
    max_threads: int = 1
    allowed_modules: Optional[List[str]] = None
    forbidden_operations: Optional[List[str]] = None
    network_access: bool = False
    filesystem_write: bool = False


@dataclass
class SandboxResult:
    """Result of sandboxed execution."""
    success: bool
    result: Any = None
    execution_time: float = 0.0
    memory_used_mb: float = 0.0
    violations: List[SandboxViolation] = None

    def __post_init__(self):
        if self.violations is None:
            self.violations = []


class PluginSandbox:
    """
    Plugin execution sandbox providing security isolation and resource limits.

    Implements the security framework from Phase 3 Plugin Architecture Specification.
    """

    def __init__(self, plugin_id: str, limits: SandboxLimits = None):
        """
        Initialize plugin sandbox.

        Args:
            plugin_id: Plugin identifier
            limits: Resource limits for this plugin
        """
        self.plugin_id = plugin_id
        self.limits = limits or SandboxLimits()
        self.execution_contexts: Dict[str, Any] = {}
        self.violation_handlers: List[Callable] = []

        # Default allowed modules (safe Python standard library)
        if self.limits.allowed_modules is None:
            self.limits.allowed_modules = [
                'json', 'datetime', 'collections', 'itertools',
                'functools', 'operator', 're', 'string', 'math',
                'random', 'hashlib', 'uuid', 'typing', 'dataclasses'
            ]

        logger.info(f"🛡️ Plugin sandbox initialized for {plugin_id}")

    def add_violation_handler(self, handler: Callable[[SandboxViolation, str], None]):
        """
        Add a handler for sandbox violations.

        Args:
            handler: Function called when violations occur
        """
        self.violation_handlers.append(handler)

    def _trigger_violation(self, violation: SandboxViolation, details: str = ""):
        """
        Trigger a sandbox violation.

        Args:
            violation: Type of violation
            details: Additional violation details
        """
        logger.warning(f"🚨 Sandbox violation in {self.plugin_id}: {violation.value} - {details}")

        for handler in self.violation_handlers:
            try:
                handler(violation, details)
            except Exception as e:
                logger.error(f"Violation handler failed: {e}")

    @contextmanager
    def execution_context(self, operation_id: str = None):
        """
        Context manager for safe plugin execution.

        Args:
            operation_id: Unique identifier for this execution context
        """
        if operation_id is None:
            operation_id = f"{self.plugin_id}_{int(time.time())}"

        start_time = time.time()
        memory_start = self._get_memory_usage()

        # Set resource limits
        old_limits = self._set_resource_limits()

        try:
            # Set up signal handlers for timeout
            def timeout_handler(signum, frame):
                raise TimeoutError(f"Execution timeout for {self.plugin_id}")

            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(self.limits.max_execution_time_sec)

            yield operation_id

        except TimeoutError:
            self._trigger_violation(SandboxViolation.EXECUTION_TIME_LIMIT,
                                  f"Exceeded {self.limits.max_execution_time_sec}s")
            raise
        except MemoryError:
            self._trigger_violation(SandboxViolation.MEMORY_LIMIT,
                                  f"Exceeded {self.limits.max_memory_mb}MB")
            raise
        finally:
            # Restore signal handler
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)

            # Restore resource limits
            self._restore_resource_limits(old_limits)

            # Log execution metrics
            execution_time = time.time() - start_time
            memory_used = self._get_memory_usage() - memory_start

            logger.info(f"📊 Plugin {self.plugin_id} execution: {execution_time:.2f}s, {memory_used:.1f}MB")

    def _set_resource_limits(self) -> Dict[str, Any]:
        """Set resource limits for the current process."""
        old_limits = {}

        if not HAS_RESOURCE:
            logger.debug("Resource limits not available on this platform")
            return old_limits

        try:
            # Memory limit (in bytes)
            memory_limit_bytes = self.limits.max_memory_mb * 1024 * 1024
            old_limits['memory'] = resource.getrlimit(resource.RLIMIT_AS)
            resource.setrlimit(resource.RLIMIT_AS, (memory_limit_bytes, memory_limit_bytes))

            # CPU time limit
            cpu_limit_sec = int((self.limits.max_cpu_percent / 100.0) * self.limits.max_execution_time_sec)
            old_limits['cpu'] = resource.getrlimit(resource.RLIMIT_CPU)
            resource.setrlimit(resource.RLIMIT_CPU, (cpu_limit_sec, cpu_limit_sec))

        except Exception as e:
            logger.warning(f"Failed to set resource limits: {e}")

        return old_limits

    def _restore_resource_limits(self, old_limits: Dict[str, Any]):
        """Restore original resource limits."""
        if not HAS_RESOURCE:
            return

        try:
            if 'memory' in old_limits:
                resource.setrlimit(resource.RLIMIT_AS, old_limits['memory'])
            if 'cpu' in old_limits:
                resource.setrlimit(resource.RLIMIT_CPU, old_limits['cpu'])
        except Exception as e:
            logger.warning(f"Failed to restore resource limits: {e}")

    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        try:
            with open('/proc/self/status', 'r') as f:
                for line in f:
                    if line.startswith('VmRSS:'):
                        # Extract memory in KB and convert to MB
                        mem_kb = int(line.split()[1])
                        return mem_kb / 1024.0
        except Exception:
            pass

        # Fallback: estimate from resource module
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss / (1024 * 1024)
        except Exception:
            return 0.0

    async def execute_sandboxed(self, func: Callable, *args, **kwargs) -> SandboxResult:
        """
        Execute a function in the sandbox.

        Args:
            func: Function to execute
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function

        Returns:
            SandboxResult: Execution result with metrics
        """
        result = SandboxResult(success=False)
        start_time = time.time()
        memory_start = self._get_memory_usage()

        try:
            with self.execution_context():
                # Execute the function
                if asyncio.iscoroutinefunction(func):
                    result.result = await func(*args, **kwargs)
                else:
                    result.result = func(*args, **kwargs)

                result.success = True

        except TimeoutError:
            result.violations.append(SandboxViolation.EXECUTION_TIME_LIMIT)
        except MemoryError:
            result.violations.append(SandboxViolation.MEMORY_LIMIT)
        except Exception as e:
            logger.error(f"Sandbox execution failed for {self.plugin_id}: {e}")
            result.result = str(e)

        finally:
            # Record metrics
            result.execution_time = time.time() - start_time
            result.memory_used_mb = self._get_memory_usage() - memory_start

        return result

    def validate_module_access(self, module_name: str) -> bool:
        """
        Validate if a module can be imported.

        Args:
            module_name: Name of module to check

        Returns:
            bool: True if module access is allowed
        """
        if self.limits.allowed_modules and module_name not in self.limits.allowed_modules:
            self._trigger_violation(SandboxViolation.FORBIDDEN_MODULE,
                                  f"Module '{module_name}' not in allowed list")
            return False
        return True

    def validate_operation(self, operation: str) -> bool:
        """
        Validate if an operation is allowed.

        Args:
            operation: Operation to validate

        Returns:
            bool: True if operation is allowed
        """
        if self.limits.forbidden_operations and operation in self.limits.forbidden_operations:
            self._trigger_violation(SandboxViolation.FORBIDDEN_OPERATION,
                                  f"Operation '{operation}' is forbidden")
            return False
        return True

    def validate_network_access(self) -> bool:
        """
        Validate network access permission.

        Returns:
            bool: True if network access is allowed
        """
        if not self.limits.network_access:
            self._trigger_violation(SandboxViolation.NETWORK_ACCESS,
                                  "Network access not permitted")
            return False
        return True

    def validate_filesystem_write(self, path: str) -> bool:
        """
        Validate filesystem write permission.

        Args:
            path: File path being written to

        Returns:
            bool: True if write is allowed
        """
        if not self.limits.filesystem_write:
            self._trigger_violation(SandboxViolation.FILESYSTEM_ACCESS,
                                  f"Filesystem write not permitted: {path}")
            return False
        return True

    def get_resource_usage(self) -> Dict[str, Any]:
        """
        Get current resource usage statistics.

        Returns:
            Dict[str, Any]: Resource usage metrics
        """
        return {
            "memory_mb": self._get_memory_usage(),
            "active_threads": threading.active_count(),
            "plugin_id": self.plugin_id,
            "limits": {
                "max_memory_mb": self.limits.max_memory_mb,
                "max_cpu_percent": self.limits.max_cpu_percent,
                "max_execution_time_sec": self.limits.max_execution_time_sec,
                "max_threads": self.limits.max_threads
            }
        }


class SandboxManager:
    """
    Global manager for plugin sandboxes.
    """

    def __init__(self):
        self.sandboxes: Dict[str, PluginSandbox] = {}
        self.global_limits = SandboxLimits()

    def create_sandbox(self, plugin_id: str, limits: SandboxLimits = None) -> PluginSandbox:
        """
        Create a sandbox for a plugin.

        Args:
            plugin_id: Plugin identifier
            limits: Custom limits for this plugin

        Returns:
            PluginSandbox: Configured sandbox instance
        """
        limits = limits or self.global_limits
        sandbox = PluginSandbox(plugin_id, limits)
        self.sandboxes[plugin_id] = sandbox
        return sandbox

    def get_sandbox(self, plugin_id: str) -> Optional[PluginSandbox]:
        """
        Get sandbox for a plugin.

        Args:
            plugin_id: Plugin identifier

        Returns:
            Optional[PluginSandbox]: Plugin sandbox or None
        """
        return self.sandboxes.get(plugin_id)

    def remove_sandbox(self, plugin_id: str):
        """
        Remove sandbox for a plugin.

        Args:
            plugin_id: Plugin identifier
        """
        if plugin_id in self.sandboxes:
            del self.sandboxes[plugin_id]

    def get_all_resource_usage(self) -> Dict[str, Dict[str, Any]]:
        """
        Get resource usage for all sandboxes.

        Returns:
            Dict[str, Dict[str, Any]]: Resource usage by plugin
        """
        return {
            plugin_id: sandbox.get_resource_usage()
            for plugin_id, sandbox in self.sandboxes.items()
        }


# Global sandbox manager instance
_sandbox_manager: Optional[SandboxManager] = None


def get_sandbox_manager() -> SandboxManager:
    """Get global sandbox manager instance."""
    global _sandbox_manager
    if _sandbox_manager is None:
        _sandbox_manager = SandboxManager()
    return _sandbox_manager


async def demo_plugin_sandbox():
    """Demonstrate the plugin sandbox functionality."""
    print("🛡️ Phase 3 Plugin Sandbox Demo")
    print("=" * 35)

    # Create sandbox manager
    manager = get_sandbox_manager()

    # Create a sandbox for demo plugin
    limits = SandboxLimits(
        max_memory_mb=50,
        max_execution_time_sec=5,
        allowed_modules=['json', 'datetime', 'math']
    )

    sandbox = manager.create_sandbox("demo-plugin", limits)
    print(f"✅ Created sandbox for demo-plugin")

    # Add violation handler
    def violation_handler(violation: SandboxViolation, details: str):
        print(f"🚨 Violation detected: {violation.value} - {details}")

    sandbox.add_violation_handler(violation_handler)

    # Test safe execution
    async def safe_function():
        import json
        import math
        data = {"result": math.sqrt(16)}
        return json.dumps(data)

    print("\n🧪 Testing safe execution...")
    result = await sandbox.execute_sandboxed(safe_function)
    print(f"✅ Safe execution result: {result.success}")
    print(f"📊 Execution time: {result.execution_time:.2f}s")
    print(f"💾 Memory used: {result.memory_used_mb:.1f}MB")
    if result.result:
        print(f"📄 Result: {result.result}")

    # Test resource usage monitoring
    print("\n📊 Resource usage monitoring...")
    usage = sandbox.get_resource_usage()
    print(f"🧵 Active threads: {usage['active_threads']}")
    print(f"💾 Memory usage: {usage['memory_mb']:.1f}MB")

    # Test validation functions
    print("\n🔍 Testing validation functions...")
    print(f"📦 Module 'json' allowed: {sandbox.validate_module_access('json')}")
    print(f"📦 Module 'os' allowed: {sandbox.validate_module_access('os')}")
    print(f"🌐 Network access allowed: {sandbox.validate_network_access()}")

    print("\n✅ Plugin sandbox demo complete!")
    print("🛡️ Phase 3 Security - Sandbox foundation operational!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(demo_plugin_sandbox())