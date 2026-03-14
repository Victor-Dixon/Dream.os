"""
Engine Registry - Plugin Discovery Pattern Implementation
=========================================================

<!-- SSOT Domain: integration -->

Registry using Plugin Discovery Pattern for auto-discovery of engines.
Eliminates circular dependencies by using protocol-based registration.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-12-03
V2 Compliant: Yes (<300 lines)
"""

from __future__ import annotations

import importlib
import logging
import pkgutil
from pathlib import Path
from typing import Any, Optional, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from .contracts import Engine, EngineContext

logger = logging.getLogger(__name__)


class EngineRegistry:
    """
    Registry for all core engines - SSOT for engine management.
    
    Uses Plugin Discovery Pattern to auto-discover engines implementing
    the Engine protocol, eliminating circular dependencies.
    """

    def __init__(self):
        """Initialize registry with auto-discovery."""
        self._engines: dict[str, Type[Any]] = {}
        self._instances: dict[str, object] = {}
        self._discover_engines()

    def _discover_engines(self) -> None:
        """
        Auto-discover engines implementing Engine protocol.
        
        Uses pkgutil and importlib to scan for engine modules and
        register classes that implement the Engine protocol.
        """
        from .contracts import Engine
        
        package_path = Path(__file__).parent
        # Get package name from __package__ or derive from file path
        if __package__:
            package_name = __package__
        else:
            # Fallback: derive from file path
            # __file__ is src/core/engines/registry.py
            # Package is src.core.engines
            parts = Path(__file__).parts
            if 'src' in parts:
                src_idx = parts.index('src')
                package_name = '.'.join(parts[src_idx:-1])
            else:
                package_name = "src.core.engines"
        
        discovered_count = 0
        failed_count = 0
        
        logger.info("🔍 Starting engine discovery...")
        
        try:
            modules = list(pkgutil.iter_modules([str(package_path)]))
        except Exception as e:
            logger.error(
                f"❌ Failed to scan package {package_path}: {e}",
                exc_info=True
            )
            return  # Can't discover engines if we can't scan the package
        
        for finder, name, ispkg in modules:
            # Only process engine modules (ending with _core_engine)
            if name.endswith('_core_engine') and not ispkg:
                try:
                    module = importlib.import_module(f'{package_name}.{name}')
                    engine_class = self._find_engine_class(module, Engine)
                    
                    if engine_class:
                        engine_type = name.replace('_core_engine', '')
                        self._engines[engine_type] = engine_class
                        discovered_count += 1
                        logger.info(
                            f"✅ Discovered engine: {engine_type} "
                            f"({engine_class.__name__})"
                        )
                    else:
                        logger.warning(
                            f"⚠️ Module {name} found but no Engine implementation"
                        )
                        
                except (ImportError, AttributeError) as e:
                    failed_count += 1
                    logger.warning(
                        f"⚠️ Failed to discover {name}: {e}",
                        exc_info=False
                    )
                    continue
                except Exception as e:
                    failed_count += 1
                    logger.error(
                        f"❌ Unexpected error discovering {name}: {e}",
                        exc_info=True
                    )
                    continue
        
        logger.info(
            f"📊 Discovery complete: {discovered_count} engines found, "
            f"{failed_count} failed"
        )
        
        if discovered_count == 0:
            logger.warning("⚠️ No engines discovered! Check engine implementations.")

    def _find_engine_class(
        self, 
        module: Any, 
        protocol: Type[Any]
    ) -> Optional[Type[Any]]:
        """
        Find Engine implementation in module.
        
        For Protocol-based classes, we check for required methods
        rather than using issubclass (which doesn't work with Protocols).
        
        Args:
            module: Python module to search
            protocol: Protocol class to match (Engine)
            
        Returns:
            Engine class if found, None otherwise
        """
        # Required methods from Engine protocol
        required_methods = ['initialize', 'execute', 'cleanup', 'get_status']
        
        for attr_name in dir(module):
            # Skip private attributes
            if attr_name.startswith('_'):
                continue
            
            # Must end with CoreEngine (naming convention)
            if not attr_name.endswith('CoreEngine'):
                continue
                
            try:
                attr = getattr(module, attr_name)
                
                # Check if it's a class
                if not isinstance(attr, type):
                    continue
                
                # Check if it has all required methods (Protocol compliance)
                has_all_methods = all(
                    hasattr(attr, method) and callable(getattr(attr, method))
                    for method in required_methods
                )
                
                if has_all_methods:
                    return attr
                    
            except (TypeError, AttributeError):
                # Not a class or can't check, skip
                continue
                
        return None

    def get_engine(self, engine_type: str):
        """Get engine instance by type."""
        if engine_type not in self._engines:
            raise ValueError(f"Unknown engine type: {engine_type}")

        if engine_type not in self._instances:
            self._instances[engine_type] = self._engines[engine_type]()

        return self._instances[engine_type]

    def get_engine_types(self) -> list[str]:
        """Get all available engine types."""
        return list(self._engines.keys())

    def initialize_all(self, context) -> dict[str, bool]:
        """Initialize all engines."""
        results = {}
        for engine_type in self._engines:
            try:
                engine = self.get_engine(engine_type)
                results[engine_type] = engine.initialize(context)
            except Exception as e:
                results[engine_type] = False
                context.logger.error(f"Failed to initialize {engine_type} engine: {e}")
        return results

    def cleanup_all(self, context) -> dict[str, bool]:
        """Cleanup all engines."""
        results = {}
        for engine_type, engine in self._instances.items():
            try:
                results[engine_type] = engine.cleanup(context)
            except Exception as e:
                results[engine_type] = False
                context.logger.error(f"Failed to cleanup {engine_type} engine: {e}")
        return results

    def get_all_status(self) -> dict[str, dict[str, Any]]:
        """Get status of all engines."""
        status = {}
        for engine_type, engine in self._instances.items():
            try:
                status[engine_type] = engine.get_status()
            except Exception as e:
                status[engine_type] = {"error": str(e)}
        return status
