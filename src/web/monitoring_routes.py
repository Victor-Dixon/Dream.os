"""
Monitoring Routes
================

Flask routes for monitoring lifecycle operations.
Wires monitoring services to web layer.

V2 Compliance: < 300 lines, single responsibility, route definitions.
"""

from flask import Blueprint, jsonify, request

from src.web.monitoring_handlers import MonitoringHandlers

# Create blueprint
monitoring_bp = Blueprint("monitoring", __name__, url_prefix="/api/monitoring")


@monitoring_bp.route("/lifecycle/status", methods=["GET"])
def get_monitoring_status():
    """Get monitoring lifecycle status."""
    return MonitoringHandlers.handle_get_monitoring_status(request)


@monitoring_bp.route("/lifecycle/initialize", methods=["POST"])
def initialize_monitoring():
    """Initialize monitoring lifecycle."""
    return MonitoringHandlers.handle_initialize_monitoring(request)


@monitoring_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for monitoring services."""
    return jsonify({"status": "ok", "service": "monitoring"}), 200



