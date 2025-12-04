"""
Vision Handlers
===============

Handler classes for vision/analysis operations.
Wires vision services to web layer.

V2 Compliance: < 300 lines, handler pattern.
"""

from flask import jsonify, request

try:
    from src.vision.analyzers.color_analyzer import ColorAnalyzer
    COLOR_ANALYZER_AVAILABLE = True
except ImportError:
    COLOR_ANALYZER_AVAILABLE = False


class VisionHandlers:
    """Handler class for vision operations."""

    @staticmethod
    def handle_analyze_color(request) -> tuple:
        """
        Handle request to analyze color in image.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        if not COLOR_ANALYZER_AVAILABLE:
            return jsonify({"success": False, "error": "ColorAnalyzer not available"}), 503

        try:
            data = request.get_json() or {}
            image_data = data.get("image_data")

            if not image_data:
                return jsonify({"error": "image_data is required"}), 400

            analyzer = ColorAnalyzer()
            result = analyzer.analyze_colors(image_data)

            return jsonify({"success": True, "data": result}), 200

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500



