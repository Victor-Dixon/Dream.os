"""
Architecture Handlers
=====================

Handler classes for architectural principles operations.
Wires architectural principles data to web layer.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, handler pattern.
Consolidated: Uses BaseHandler + AvailabilityMixin.
"""

from flask import jsonify, request
from typing import Any, Tuple

from src.core.base.availability_mixin import AvailabilityMixin
from src.core.base.base_handler import BaseHandler

# Lazy import with availability flag
try:
    from src.services.architectural_principles_data import (
        get_srp_guidance,
        get_ocp_guidance,
        get_lsp_guidance,
        get_isp_guidance,
        get_dip_guidance
    )
    ARCHITECTURE_AVAILABLE = True
except ImportError:
    ARCHITECTURE_AVAILABLE = False


class ArchitectureHandlers(BaseHandler, AvailabilityMixin):
    """Handler class for architectural principles operations."""

    def __init__(self):
        """Initialize architecture handlers."""
        super().__init__("ArchitectureHandlers")

    def handle_get_all_principles(self, request) -> Tuple[Any, int]:
        """
        Handle request to get all architectural principles.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        availability_error = self.check_availability(
            ARCHITECTURE_AVAILABLE,
            "Architecture services"
        )
        if availability_error:
            return availability_error

        try:
            principles = {
                "srp": get_srp_guidance().dict() if hasattr(get_srp_guidance(), 'dict') else str(get_srp_guidance()),
                "ocp": get_ocp_guidance().dict() if hasattr(get_ocp_guidance(), 'dict') else str(get_ocp_guidance()),
                "lsp": get_lsp_guidance().dict() if hasattr(get_lsp_guidance(), 'dict') else str(get_lsp_guidance()),
                "isp": get_isp_guidance().dict() if hasattr(get_isp_guidance(), 'dict') else str(get_isp_guidance()),
                "dip": get_dip_guidance().dict() if hasattr(get_dip_guidance(), 'dict') else str(get_dip_guidance())
            }
            
            response_data = {
                "principles": principles
            }
            response = self.format_response(response_data, success=True)
            return jsonify(response), 200
        except Exception as e:
            error_response = self.handle_error(e, "handle_get_all_principles")
            return jsonify(error_response), 500

    def handle_get_principle(self, request, principle_name: str) -> Tuple[Any, int]:
        """
        Handle request to get specific architectural principle.

        Args:
            request: Flask request object
            principle_name: Name of the principle to retrieve

        Returns:
            Tuple of (response_data, status_code)
        """
        availability_error = self.check_availability(
            ARCHITECTURE_AVAILABLE,
            "Architecture services"
        )
        if availability_error:
            return availability_error

        try:
            principle_map = {
                "srp": get_srp_guidance,
                "ocp": get_ocp_guidance,
                "lsp": get_lsp_guidance,
                "isp": get_isp_guidance,
                "dip": get_dip_guidance
            }
            
            if principle_name.lower() not in principle_map:
                error_response = self.format_response(
                    None,
                    success=False,
                    error=f"Unknown principle: {principle_name}"
                )
                return jsonify(error_response), 404
            
            guidance = principle_map[principle_name.lower()]()
            principle_data = guidance.dict() if hasattr(guidance, 'dict') else str(guidance)
            
            response_data = {
                "principle": principle_data
            }
            response = self.format_response(response_data, success=True)
            return jsonify(response), 200
        except Exception as e:
            error_response = self.handle_error(e, "handle_get_principle")
            return jsonify(error_response), 500

