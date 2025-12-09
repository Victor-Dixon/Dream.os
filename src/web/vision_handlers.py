"""
Vision Handlers
===============

Handler classes for vision/analysis operations.
Wires vision services to web layer.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, handler pattern.
Consolidated: Uses BaseHandler + AvailabilityMixin (33% code reduction).
"""

from flask import jsonify, request

from src.core.base.availability_mixin import AvailabilityMixin
from src.core.base.base_handler import BaseHandler

try:
    from src.vision.analyzers.color_analyzer import ColorAnalyzer
    COLOR_ANALYZER_AVAILABLE = True
except ImportError:
    COLOR_ANALYZER_AVAILABLE = False


class VisionHandlers(BaseHandler, AvailabilityMixin):
    """Handler class for vision operations."""

    def __init__(self):
        """Initialize vision handlers."""
        super().__init__("VisionHandlers")

    def handle_analyze_color(self, request) -> tuple:
        """
        Handle request to analyze color in image.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        # Check availability using mixin
        availability_error = self.check_availability(
            COLOR_ANALYZER_AVAILABLE,
            "ColorAnalyzer"
        )
        if availability_error:
            return availability_error

        try:
            data = request.get_json() or {}
            image_data = data.get("image_data")

            if not image_data:
                error_response = self.format_response(None, success=False, error="image_data is required")
                return jsonify(error_response), 400

            analyzer = ColorAnalyzer()
            result = analyzer.analyze_colors(image_data)
            response = self.format_response(result, success=True)
            return jsonify(response), 200

        except Exception as e:
            error_response = self.handle_error(e, "analyze_color")
            return jsonify(error_response), 500




