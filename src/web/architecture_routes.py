"""
Architecture Routes
===================

Flask routes for architectural principles operations.
Wires architectural principles data to web layer.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, single responsibility, route definitions.
"""

from flask import Blueprint, jsonify, request

from src.web.architecture_handlers import ArchitectureHandlers

# Create blueprint
architecture_bp = Blueprint("architecture", __name__, url_prefix="/api/architecture")

# Instantiate handler (BaseHandler pattern)
architecture_handlers = ArchitectureHandlers()


@architecture_bp.route("/principles", methods=["GET"])
def get_architectural_principles():
    """Get all architectural principles."""
    return architecture_handlers.handle_get_all_principles(request)


@architecture_bp.route("/principles/<principle_name>", methods=["GET"])
def get_principle(principle_name: str):
    """Get specific architectural principle."""
    return architecture_handlers.handle_get_principle(request, principle_name)


@architecture_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for architecture services."""
    return jsonify({"status": "ok", "service": "architecture"}), 200

