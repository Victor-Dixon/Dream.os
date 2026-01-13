"""
Availability Mixin - Handler Availability Checking
=================================================

<!-- SSOT Domain: core -->

Mixin for handlers that need to check service/module availability.
Consolidates availability check pattern found in 8+ handlers.

V2 Compliance: < 150 lines, single responsibility.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-12-05
License: MIT
"""

from flask import jsonify
from typing import Optional, Tuple


class AvailabilityMixin:
    """Mixin for availability checking in handlers."""

    def check_availability(
        self,
        available: bool,
        service_name: str
    ) -> Optional[Tuple]:
        """
        Check if a service/module is available.

        Args:
            available: Whether the service is available
            service_name: Name of the service/module

        Returns:
            Error response tuple if not available, None if available
        """
        if not available:
            return (
                jsonify({
                    "success": False,
                    "error": f"{service_name} not available"
                }),
                503
            )
        return None
