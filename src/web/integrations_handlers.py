"""
Integrations Handlers
=====================

Handler classes for integration services operations.
Wires integration services to web layer.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, handler pattern.
Consolidated: Uses BaseHandler + AvailabilityMixin (33% code reduction).
"""

from flask import jsonify, request

from src.core.base.availability_mixin import AvailabilityMixin
from src.core.base.base_handler import BaseHandler

try:
    from src.integrations.jarvis.conversation_engine import ConversationEngine
    CONVERSATION_ENGINE_AVAILABLE = True
except ImportError:
    CONVERSATION_ENGINE_AVAILABLE = False

try:
    from src.integrations.jarvis.vision_system import VisionSystem
    VISION_SYSTEM_AVAILABLE = True
except ImportError:
    VISION_SYSTEM_AVAILABLE = False


class IntegrationsHandlers(BaseHandler, AvailabilityMixin):
    """Handler class for integration services operations."""

    def __init__(self):
        """Initialize integrations handlers."""
        super().__init__("IntegrationsHandlers")

    def handle_jarvis_conversation(self, request) -> tuple:
        """
        Handle Jarvis conversation request.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        # Check availability using mixin
        availability_error = self.check_availability(
            CONVERSATION_ENGINE_AVAILABLE,
            "ConversationEngine"
        )
        if availability_error:
            return availability_error

        try:
            data = request.get_json() or {}
            message = data.get("message")

            if not message:
                error_response = self.format_response(None, success=False, error="message is required")
                return jsonify(error_response), 400

            engine = ConversationEngine()
            response_data = engine.process_message(message)
            response = self.format_response(response_data, success=True)
            return jsonify(response), 200

        except Exception as e:
            error_response = self.handle_error(e, "jarvis_conversation")
            return jsonify(error_response), 500

    def handle_jarvis_vision(self, request) -> tuple:
        """
        Handle Jarvis vision request.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        # Check availability using mixin
        availability_error = self.check_availability(
            VISION_SYSTEM_AVAILABLE,
            "VisionSystem"
        )
        if availability_error:
            return availability_error

        try:
            data = request.get_json() or {}
            image_data = data.get("image_data")
            prompt = data.get("prompt")

            if not image_data:
                error_response = self.format_response(None, success=False, error="image_data is required")
                return jsonify(error_response), 400

            vision = VisionSystem()
            result = vision.analyze_image(image_data, prompt)
            response = self.format_response(result, success=True)
            return jsonify(response), 200

        except Exception as e:
            error_response = self.handle_error(e, "jarvis_vision")
            return jsonify(error_response), 500




