"""
Integrations Routes
==================

Flask routes for integration services (Jarvis, Vision, etc.).
Wires integration services to web layer.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, single responsibility, route definitions.
"""

from flask import Blueprint, jsonify, request

from src.web.integrations_handlers import IntegrationsHandlers

# Create blueprint
integrations_bp = Blueprint("integrations", __name__, url_prefix="/api/integrations")

# Create handler instance (BaseHandler pattern)
integrations_handlers = IntegrationsHandlers()


@integrations_bp.route("/jarvis/conversation", methods=["POST"])
def jarvis_conversation():
    """Handle Jarvis conversation request."""
    return integrations_handlers.handle_jarvis_conversation(request)


@integrations_bp.route("/jarvis/vision", methods=["POST"])
def jarvis_vision():
    """Handle Jarvis vision request."""
    return integrations_handlers.handle_jarvis_vision(request)


@integrations_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for integration services."""
    return jsonify({"status": "ok", "service": "integrations"}), 200



