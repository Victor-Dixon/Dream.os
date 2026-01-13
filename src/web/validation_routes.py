"""
Validation Routes
=================

Flask routes for unified validation tool integration.
Provides API access to unified_validator.py functionality.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, single responsibility, route definitions.
"""

from flask import Blueprint, jsonify, request

from src.web.validation_handlers import ValidationHandlers

# Create blueprint
validation_bp = Blueprint("validation", __name__, url_prefix="/api/validation")

# Create handler instance (BaseHandler pattern)
validation_handlers = ValidationHandlers()


@validation_bp.route("/validate", methods=["POST"])
def validate():
    """Run validation by category."""
    return validation_handlers.handle_validate(request)


@validation_bp.route("/categories", methods=["GET"])
def get_categories():
    """List available validation categories."""
    return validation_handlers.handle_get_categories(request)


@validation_bp.route("/full", methods=["POST"])
def full_validation():
    """Run full validation suite."""
    return validation_handlers.handle_full_validation(request)


@validation_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "ok", "service": "validation"})




