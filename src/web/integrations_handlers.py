"""
Integrations Handlers
=====================

Handler classes for integration services operations.
Wires integration services to web layer.

V2 Compliance: < 300 lines, handler pattern.
"""

from flask import jsonify, request

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


class IntegrationsHandlers:
    """Handler class for integration services operations."""

    @staticmethod
    def handle_jarvis_conversation(request) -> tuple:
        """
        Handle Jarvis conversation request.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        if not CONVERSATION_ENGINE_AVAILABLE:
            return jsonify({"success": False, "error": "ConversationEngine not available"}), 503

        try:
            data = request.get_json() or {}
            message = data.get("message")

            if not message:
                return jsonify({"error": "message is required"}), 400

            engine = ConversationEngine()
            response = engine.process_message(message)

            return jsonify({"success": True, "data": response}), 200

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @staticmethod
    def handle_jarvis_vision(request) -> tuple:
        """
        Handle Jarvis vision request.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        if not VISION_SYSTEM_AVAILABLE:
            return jsonify({"success": False, "error": "VisionSystem not available"}), 503

        try:
            data = request.get_json() or {}
            image_data = data.get("image_data")
            prompt = data.get("prompt")

            if not image_data:
                return jsonify({"error": "image_data is required"}), 400

            vision = VisionSystem()
            result = vision.analyze_image(image_data, prompt)

            return jsonify({"success": True, "data": result}), 200

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500



