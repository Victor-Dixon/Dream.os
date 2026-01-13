"""
Pipeline Routes
===============

Flask routes for pipeline operations.
Wires pipeline systems to web layer.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, single responsibility, route definitions.
"""

from flask import Blueprint, jsonify, request

from src.web.pipeline_handlers import PipelineHandlers

# Create blueprint
pipeline_bp = Blueprint("pipeline", __name__, url_prefix="/api/pipeline")

# Create handler instance (BaseHandler pattern)
pipeline_handlers = PipelineHandlers()


@pipeline_bp.route("/gas/status", methods=["GET"])
def get_gas_pipeline_status():
    """Get gas pipeline system status."""
    return pipeline_handlers.handle_get_gas_pipeline_status(request)


@pipeline_bp.route("/gas/monitor", methods=["POST"])
def monitor_gas_pipeline():
    """Monitor and send gas to agents."""
    return pipeline_handlers.handle_monitor_gas_pipeline(request)


@pipeline_bp.route("/gas/agent/<agent_id>/status", methods=["GET"])
def get_agent_gas_status(agent_id: str):
    """Get gas status for specific agent."""
    return pipeline_handlers.handle_get_agent_gas_status(request, agent_id)


@pipeline_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for pipeline services."""
    return jsonify({"status": "ok", "service": "pipeline"}), 200


