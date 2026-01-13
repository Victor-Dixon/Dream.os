"""
Base Engine - SSOT for all engine classes

<!-- SSOT Domain: infrastructure -->

=========================================

Base class for all engine implementations.
Provides common functionality and interface for engines.

Author: Agent-2 (Architecture & Design Specialist) - Created to fix broken imports
License: MIT
"""

from abc import ABC, abstractmethod
from typing import Any, Optional, Dict
from datetime import datetime
import logging


class BaseEngine(ABC):
    """Base class for all engine implementations."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize base engine."""
        self.config = config or {}
        self.logger = logging.getLogger(self.__class__.__name__)
        self.is_active = False
        self.start_time: Optional[datetime] = None
    
    def start(self) -> bool:
        """Start the engine."""
        if self.is_active:
            self.logger.warning("Engine is already active")
            return True
        
        try:
            self.is_active = True
            self.start_time = datetime.now()
            self.logger.info(f"{self.__class__.__name__} started")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start engine: {e}")
            return False
    
    def stop(self) -> bool:
        """Stop the engine."""
        if not self.is_active:
            self.logger.warning("Engine is not active")
            return True
        
        try:
            self.is_active = False
            self.logger.info(f"{self.__class__.__name__} stopped")
            return True
        except Exception as e:
            self.logger.error(f"Failed to stop engine: {e}")
            return False
    
    @abstractmethod
    def process(self, data: Any) -> Any:
        """Process data - must be implemented by subclasses."""
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """Get engine status."""
        uptime = None
        if self.start_time:
            uptime = (datetime.now() - self.start_time).total_seconds()
        
        return {
            "engine_name": self.__class__.__name__,
            "is_active": self.is_active,
            "uptime_seconds": uptime,
            "start_time": self.start_time.isoformat() if self.start_time else None,
        }


__all__ = ["BaseEngine"]

