"""
Discord Handlers
================

Handler classes for Discord operations.
Wires Discord controllers and views to web layer.

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
    from src.discord_commander.controllers.swarm_tasks_controller_view import SwarmTasksControllerView
    from src.discord_commander.templates.broadcast_templates import ENHANCED_BROADCAST_TEMPLATES
    from src.discord_commander.views.main_control_panel_view import MainControlPanelView
    from src.services.messaging_infrastructure import ConsolidatedMessagingService
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False


class DiscordHandlers(BaseHandler, AvailabilityMixin):
    """Handler class for Discord operations."""

    def __init__(self):
        """Initialize Discord handlers."""
        super().__init__("DiscordHandlers")

    def handle_get_swarm_tasks(self, request) -> Tuple[Any, int]:
        """
        Handle request to get swarm tasks information.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        availability_error = self.check_availability(
            DISCORD_AVAILABLE,
            "Discord services"
        )
        if availability_error:
            return availability_error

        try:
            messaging_service = ConsolidatedMessagingService()
            controller = SwarmTasksControllerView(messaging_service)
            
            # Get tasks data
            tasks_data = controller._get_tasks_data()
            
            response_data = {
                "data": tasks_data
            }
            response = self.format_response(response_data, success=True)
            return jsonify(response), 200
        except Exception as e:
            error_response = self.handle_error(e, "handle_get_swarm_tasks")
            return jsonify(error_response), 500

    def handle_get_broadcast_templates(self, request) -> Tuple[Any, int]:
        """
        Handle request to get broadcast templates.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        availability_error = self.check_availability(
            DISCORD_AVAILABLE,
            "Discord templates"
        )
        if availability_error:
            return availability_error

        try:
            response_data = {
                "templates": ENHANCED_BROADCAST_TEMPLATES
            }
            response = self.format_response(response_data, success=True)
            return jsonify(response), 200
        except Exception as e:
            error_response = self.handle_error(e, "handle_get_broadcast_templates")
            return jsonify(error_response), 500

    def handle_get_control_panel_status(self, request) -> Tuple[Any, int]:
        """
        Handle request to get control panel status.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        availability_error = self.check_availability(
            DISCORD_AVAILABLE,
            "Discord control panel"
        )
        if availability_error:
            return availability_error

        try:
            messaging_service = ConsolidatedMessagingService()
            panel = MainControlPanelView(messaging_service)
            
            response_data = {
                "status": "active",
                "panel_type": "main_control_panel"
            }
            response = self.format_response(response_data, success=True)
            return jsonify(response), 200
        except Exception as e:
            error_response = self.handle_error(e, "handle_get_control_panel_status")
            return jsonify(error_response), 500

