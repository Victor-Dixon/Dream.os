"""
Contract Management Routes
==========================

Flask routes for contract system operations.
Wires contract manager to web layer.

V2 Compliance: < 300 lines, single responsibility, route definitions.
"""

from flask import Blueprint, jsonify, request

from src.web.contract_handlers import ContractHandlers

# Create blueprint
contract_bp = Blueprint("contract", __name__, url_prefix="/api/contracts")


@contract_bp.route("/status", methods=["GET"])
def get_system_status():
    """Get overall system contract status."""
    return ContractHandlers.handle_get_system_status(request)


@contract_bp.route("/agent/<agent_id>", methods=["GET"])
def get_agent_status(agent_id: str):
    """Get contract status for specific agent."""
    return ContractHandlers.handle_get_agent_status(request, agent_id)


@contract_bp.route("/next-task", methods=["POST"])
def get_next_task():
    """Get next available task for an agent."""
    return ContractHandlers.handle_get_next_task(request)


@contract_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for contract services."""
    return jsonify({"status": "ok", "service": "contract_management"}), 200



