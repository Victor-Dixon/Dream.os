"""
Vision Routes
=============

Flask routes for vision/analysis operations.
Wires vision services to web layer.

V2 Compliance: < 300 lines, single responsibility, route definitions.
"""

from flask import Blueprint, jsonify, request

from src.web.vision_handlers import VisionHandlers

# Create blueprint
vision_bp = Blueprint("vision", __name__, url_prefix="/api/vision")


@vision_bp.route("/analyze-color", methods=["POST"])
def analyze_color():
    """Analyze color in image."""
    return VisionHandlers.handle_analyze_color(request)


@vision_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for vision services."""
    return jsonify({"status": "ok", "service": "vision"}), 200



