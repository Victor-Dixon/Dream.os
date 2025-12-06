"""
Assignment Service Routes
=========================

Flask routes for assignment service operations.
Wires assignment service to web layer.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, single responsibility, route definitions.
"""

from flask import Blueprint, jsonify, request

from src.web.assignment_handlers import AssignmentHandlers

# Create blueprint
assignment_bp = Blueprint("assignment", __name__, url_prefix="/api/assignments")


@assignment_bp.route("/assign", methods=["POST"])
def assign():
    """Assign task to best agent."""
    return AssignmentHandlers.handle_assign(request)


@assignment_bp.route("/list", methods=["GET"])
def list_assignments():
    """List all assignments."""
    return AssignmentHandlers.handle_list(request)


@assignment_bp.route("/status", methods=["GET"])
def get_status():
    """Get assignment service status."""
    return AssignmentHandlers.handle_get_status(request)


@assignment_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for assignment services."""
    return jsonify({"status": "ok", "service": "assignment_service"}), 200



