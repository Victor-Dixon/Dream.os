"""
<!-- SSOT Domain: integration -->

Coordinator Service - Agent Cellphone V2
=======================================

Service for managing coordinator operations.

Author: Agent-1 (System Recovery Specialist)
License: MIT
"""

from typing import Any, Dict, Optional

from ..core.base.base_service import BaseService


class Coordinator(BaseService):
    """Basic coordinator implementation."""

    def __init__(self, name: str, logger: Optional[Any] = None):
        """Initialize coordinator."""
        super().__init__("Coordinator")
        self.name = name
        # Use BaseService logger if no custom logger provided
        if logger:
            self.custom_logger = logger
        self.status = {"name": name, "status": "active"}

    def get_status(self) -> Dict[str, Any]:
        """Get coordinator status."""
        return self.status

    def get_name(self) -> str:
        """Get coordinator name."""
        return self.name

    def shutdown(self) -> None:
        """Shutdown coordinator."""
        self.status["status"] = "shutdown"
        # Use custom logger if provided, otherwise use BaseService logger
        logger = getattr(self, 'custom_logger', None) or self.logger
        if logger:
            logger.info(f"Coordinator {self.name} shut down")
