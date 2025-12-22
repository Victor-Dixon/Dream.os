"""
Messaging Routes
================

Flask routes for messaging operations.
Wires messaging services to web layer.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, single responsibility, route definitions.
"""

from flask import Blueprint, jsonify, request

from src.web.messaging_handlers import MessagingHandlers
from src.web.messaging_template_handlers import MessagingTemplateHandlers

# Create blueprint
messaging_bp = Blueprint("messaging", __name__, url_prefix="/api/messaging")

# Create handler instances (BaseHandler pattern)
messaging_handlers = MessagingHandlers()
template_handlers = MessagingTemplateHandlers()


@messaging_bp.route("/cli/parse", methods=["POST"])
def parse_cli():
    """Parse messaging CLI command."""
    return messaging_handlers.handle_parse_cli(request)


@messaging_bp.route("/cli/help", methods=["GET"])
def get_cli_help():
    """Get CLI help documentation."""
    return messaging_handlers.handle_get_cli_help(request)


@messaging_bp.route("/cli/execute", methods=["POST"])
def execute_cli():
    """Execute messaging CLI command."""
    return messaging_handlers.handle_execute_cli(request)


@messaging_bp.route("/templates/list", methods=["GET"])
def list_templates():
    """List available messaging templates."""
    return template_handlers.handle_list_templates(request)


@messaging_bp.route("/templates/render", methods=["POST"])
def render_template():
    """Render messaging template with variables."""
    return template_handlers.handle_render_template(request)


@messaging_bp.route("/templates/get", methods=["GET"])
def get_template():
    """Get specific template by name."""
    return template_handlers.handle_get_template(request)


@messaging_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for messaging services."""
    return jsonify({"status": "ok", "service": "messaging"}), 200


