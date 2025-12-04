#!/usr/bin/env python3
"""
Initialization Mixin - Code Consolidation
==========================================

Mixin class for common initialization patterns across services, handlers, and managers.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-12-02
License: MIT
"""

import logging
from typing import Any, Optional

from src.core.config.config_manager import UnifiedConfigManager
from src.core.logging.unified_logging_system import UnifiedLoggingSystem


class InitializationMixin:
    """
    Mixin for common initialization patterns.
    
    Provides:
    - Logging setup
    - Configuration loading
    - Environment variable loading
    - Common initialization utilities
    
    Usage:
        class MyClass(InitializationMixin):
            def __init__(self):
                self.setup_logging("MyClass")
                self.load_config("my_config_section")
    """
    
    def setup_logging(self, name: str, level: Optional[str] = None) -> logging.Logger:
        """
        Setup logging for class.
        
        Args:
            name: Logger name
            level: Optional log level (default: INFO)
        
        Returns:
            Logger instance
        """
        logger = UnifiedLoggingSystem(name).get_logger()
        if level:
            logger.setLevel(getattr(logging, level.upper(), logging.INFO))
        return logger
    
    def load_config(self, section: Optional[str] = None) -> dict[str, Any]:
        """
        Load configuration section.
        
        Args:
            section: Config section name (default: class name)
        
        Returns:
            Config dict
        """
        config = UnifiedConfigManager()
        section_name = section or self.__class__.__name__.lower()
        return config.get_section(section_name, {})
    
    def get_config_value(self, key: str, default: Any = None, section: Optional[str] = None) -> Any:
        """
        Get config value.
        
        Args:
            key: Config key
            default: Default value if not found
            section: Optional config section
        
        Returns:
            Config value or default
        """
        config_dict = self.load_config(section)
        return config_dict.get(key, default)
    
    def ensure_initialized(self, attribute: str = "_initialized") -> bool:
        """
        Ensure class is initialized (check for _initialized attribute).
        
        Args:
            attribute: Attribute name to check (default: _initialized)
        
        Returns:
            True if initialized
        """
        if not hasattr(self, attribute):
            return False
        return getattr(self, attribute, False)



