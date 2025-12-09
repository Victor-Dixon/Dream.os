"""
Services Layer Handlers
=======================

Handler classes for service layer operations.
Wires services to web layer.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, handler pattern.
Consolidated: Uses BaseHandler + AvailabilityMixin (33% code reduction).
"""

from flask import jsonify, request

from src.core.base.availability_mixin import AvailabilityMixin
from src.core.base.base_handler import BaseHandler

try:
    from src.services.chat_presence.chat_presence_orchestrator import ChatPresenceOrchestrator
    CHAT_PRESENCE_AVAILABLE = True
except ImportError:
    CHAT_PRESENCE_AVAILABLE = False


class ServicesHandlers(BaseHandler, AvailabilityMixin):
    """Handler class for service layer operations."""

    def __init__(self):
        """Initialize services handlers."""
        super().__init__("ServicesHandlers")

    def handle_get_chat_presence_status(self, request) -> tuple:
        """
        Handle request to get chat presence status.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        # Check availability using mixin
        availability_error = self.check_availability(
            CHAT_PRESENCE_AVAILABLE,
            "ChatPresenceOrchestrator"
        )
        if availability_error:
            return availability_error

        try:
            orchestrator = ChatPresenceOrchestrator()
            status = orchestrator.get_status()
            response = self.format_response(status, success=True)
            return jsonify(response), 200

        except Exception as e:
            error_response = self.handle_error(e, "get_chat_presence_status")
            return jsonify(error_response), 500

    def handle_start_chat_presence(self, request) -> tuple:
        """
        Handle request to start chat presence.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        # Check availability using mixin
        availability_error = self.check_availability(
            CHAT_PRESENCE_AVAILABLE,
            "ChatPresenceOrchestrator"
        )
        if availability_error:
            return availability_error

        try:
            orchestrator = ChatPresenceOrchestrator()
            result = orchestrator.start()
            response = self.format_response(result, success=True)
            return jsonify(response), 200

        except Exception as e:
            error_response = self.handle_error(e, "start_chat_presence")
            return jsonify(error_response), 500

    def handle_stop_chat_presence(self, request) -> tuple:
        """
        Handle request to stop chat presence.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        # Check availability using mixin
        availability_error = self.check_availability(
            CHAT_PRESENCE_AVAILABLE,
            "ChatPresenceOrchestrator"
        )
        if availability_error:
            return availability_error

        try:
            orchestrator = ChatPresenceOrchestrator()
            result = orchestrator.stop()
            response = self.format_response(result, success=True)
            return jsonify(response), 200

        except Exception as e:
            error_response = self.handle_error(e, "stop_chat_presence")
            return jsonify(error_response), 500




