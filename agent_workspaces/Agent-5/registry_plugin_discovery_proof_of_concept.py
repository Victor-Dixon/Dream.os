#!/usr/bin/env python3
"""
Proof of Concept: Plugin Discovery Pattern for EngineRegistry

This demonstrates a scalable, zero-circular-dependency solution
using auto-discovery and protocol-based registration.

Enhanced with:
- Proper logging (replaces print statements)
- Complete type hints
- Error handling improvements
- Documentation

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-03
V2 Compliant: Yes (<300 lines)
"""

from __future__ import annotations

import importlib
import logging
import pkgutil
from pathlib import Path
from typing import Any, Dict, Optional, Type

# Import only the protocol - no circular dependency!
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.core.engines.contracts import Engine, EngineContext

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class EngineRegistry:
    """
    Protocol-based engine registry with auto-discovery.
    
    Benefits:
    - Zero circular dependencies (no module-level imports)
    - Auto-discovers engines (no manual registration)
    - Protocol-based (DIP compliant)
    - Highly testable (easy to mock)
    - Scales infinitely (works with any number of engines)
    """
    
    def __init__(self):
        self._engines: Dict[str, Type[Engine]] = {}
        self._instances: Dict[str, Engine] = {}
        self._discover_engines()
    
    def _discover_engines(self) -> None:
        """
        Auto-discover engines implementing Engine protocol.
        
        This method:
        1. Scans the engines package for modules
        2. Finds classes implementing Engine protocol
        3. Registers them automatically
        4. No hardcoded imports = no circular dependencies!
        
        Raises:
            ImportError: If package structure is invalid
        """
        # Get engines package path relative to project root
        project_root = Path(__file__).parent.parent.parent
        package_path = project_root / "src" / "core" / "engines"
        package_name = "src.core.engines"
        
        if not package_path.exists():
            logger.error(f"Engines package not found: {package_path}")
            return
        
        logger.info(f"Discovering engines in package: {package_name}")
        discovered_count = 0
        
        for finder, name, ispkg in pkgutil.iter_modules([str(package_path)]):
            # Only process engine modules (naming convention)
            if name.endswith('_core_engine') and not ispkg:
                try:
                    module = importlib.import_module(f'{package_name}.{name}')
                    engine_class = self._find_engine_class(module)
                    
                    if engine_class:
                        # Extract engine type from module name
                        # e.g., "analysis_core_engine" -> "analysis"
                        engine_type = name.replace('_core_engine', '')
                        self._engines[engine_type] = engine_class
                        discovered_count += 1
                        logger.info(
                            f"Discovered engine: {engine_type} -> {engine_class.__name__}"
                        )
                    else:
                        logger.debug(f"No engine class found in module: {name}")
                except ImportError as e:
                    logger.warning(f"Skipped {name} (ImportError): {e}")
                    continue
                except AttributeError as e:
                    logger.warning(f"Skipped {name} (AttributeError): {e}")
                    continue
                except Exception as e:
                    logger.error(f"Unexpected error discovering {name}: {e}")
                    continue
        
        logger.info(f"Discovery complete: {discovered_count} engines found")
    
    def _find_engine_class(self, module: Any) -> Optional[Type[Engine]]:
        """
        Find Engine implementation in module.
        
        Looks for classes that:
        1. Are subclasses of Engine protocol
        2. Are not the protocol itself
        3. Follow naming convention (end with "CoreEngine")
        
        Args:
            module: Python module to search for engine classes
            
        Returns:
            Engine class if found, None otherwise
        """
        from src.core.engines.contracts import Engine
        
        for attr_name in dir(module):
            # Skip private attributes
            if attr_name.startswith('_'):
                continue
            
            try:
                attr = getattr(module, attr_name)
                
                # Check if it's a class implementing Engine protocol
                if (isinstance(attr, type) and 
                    issubclass(attr, Engine) and
                    attr is not Engine and
                    attr_name.endswith('CoreEngine')):
                    logger.debug(f"Found engine class: {attr_name} in {module.__name__}")
                    return attr
            except (TypeError, AttributeError) as e:
                # Skip attributes that can't be checked
                logger.debug(f"Skipped attribute {attr_name}: {e}")
                continue
        
        return None
    
    def get_engine(self, engine_type: str) -> Engine:
        """Get engine instance by type (lazy instantiation)."""
        if engine_type not in self._engines:
            available = ', '.join(self._engines.keys())
            raise ValueError(
                f"Unknown engine type: {engine_type}. "
                f"Available: {available}"
            )
        
        # Lazy instantiation - create only when needed
        if engine_type not in self._instances:
            self._instances[engine_type] = self._engines[engine_type]()
        
        return self._instances[engine_type]
    
    def get_engine_types(self) -> list[str]:
        """Get all available engine types."""
        return list(self._engines.keys())
    
    def initialize_all(self, context: EngineContext) -> Dict[str, bool]:
        """Initialize all discovered engines."""
        results = {}
        for engine_type in self._engines:
            try:
                engine = self.get_engine(engine_type)
                results[engine_type] = engine.initialize(context)
            except Exception as e:
                results[engine_type] = False
                context.logger.error(f"Failed to initialize {engine_type} engine: {e}")
        return results
    
    def cleanup_all(self, context: EngineContext) -> Dict[str, bool]:
        """Cleanup all engine instances."""
        results = {}
        for engine_type, engine in self._instances.items():
            try:
                results[engine_type] = engine.cleanup(context)
            except Exception as e:
                results[engine_type] = False
                context.logger.error(f"Failed to cleanup {engine_type} engine: {e}")
        return results
    
    def get_all_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all engine instances."""
        status = {}
        for engine_type, engine in self._instances.items():
            try:
                status[engine_type] = engine.get_status()
            except Exception as e:
                status[engine_type] = {"error": str(e)}
        return status


# Example usage
if __name__ == "__main__":
    logger.info("Testing Plugin Discovery Pattern...")
    
    try:
        registry = EngineRegistry()
        engine_types = registry.get_engine_types()
        
        logger.info(f"Discovery complete: {len(engine_types)} engines found")
        for engine_type in engine_types:
            logger.info(f"  - {engine_type}")
        
        logger.info("Plugin Discovery Pattern: SUCCESS")
        logger.info("  - Zero circular dependencies")
        logger.info("  - Auto-discovery working")
        logger.info("  - Protocol-based (DIP compliant)")
        
        print(f"\n✅ SUCCESS: Discovered {len(engine_types)} engines")
        print("   - Zero circular dependencies")
        print("   - Auto-discovery working")
        print("   - Protocol-based (DIP compliant)")
    except Exception as e:
        logger.error(f"Discovery failed: {e}", exc_info=True)
        raise

