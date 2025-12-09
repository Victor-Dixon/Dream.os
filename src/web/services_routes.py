"""
Services Routes
===============

Flask routes for service layer operations.
Wires services to web layer.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, single responsibility, route definitions.
"""

from flask import Blueprint, jsonify, request

from src.web.services_handlers import ServicesHandlers

# Create blueprint
services_bp = Blueprint("services", __name__, url_prefix="/api/services")

# Create handler instance (BaseHandler pattern)
services_handlers = ServicesHandlers()


@services_bp.route("/chat-presence/status", methods=["GET"])
def get_chat_presence_status():
    """Get chat presence orchestrator status."""
    return services_handlers.handle_get_chat_presence_status(request)


@services_bp.route("/chat-presence/start", methods=["POST"])
def start_chat_presence():
    """Start chat presence orchestrator."""
    return services_handlers.handle_start_chat_presence(request)


@services_bp.route("/chat-presence/stop", methods=["POST"])
def stop_chat_presence():
    """Stop chat presence orchestrator."""
    return services_handlers.handle_stop_chat_presence(request)


@services_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for services."""
    return jsonify({"status": "ok", "service": "services_layer"}), 200




