"""
Agent Management Routes - Web Layer
===================================

Flask routes for agent management operations.

<!-- SSOT Domain: web -->

Author: Agent-7 (Web Development Specialist)
Date: 2025-12-04
V2 Compliant: Yes (<300 lines)
"""

from flask import Blueprint, request

from src.web.agent_management_handlers import AgentManagementHandlers

# Create blueprint
agent_management_bp = Blueprint("agent_management", __name__, url_prefix="/api/agents")

# Create handler instance (BaseHandler pattern)
agent_management_handlers = AgentManagementHandlers()


@agent_management_bp.route("", methods=["GET"])
def list_agents():
    """List all agents."""
    return agent_management_handlers.handle_list_agents(request)


@agent_management_bp.route("/<agent_id>", methods=["GET"])
def get_agent(agent_id: str):
    """Get agent details."""
    return agent_management_handlers.handle_get_agent(request, agent_id)


@agent_management_bp.route("/<agent_id>/principle", methods=["GET"])
def get_agent_principle(agent_id: str):
    """Get agent's architectural principle."""
    return agent_management_handlers.handle_get_agent_principle(request, agent_id)


@agent_management_bp.route("/<agent_id>/principle", methods=["POST", "PUT"])
def assign_principle(agent_id: str):
    """Assign architectural principle to agent."""
    return agent_management_handlers.handle_assign_principle(request, agent_id)


@agent_management_bp.route("/<agent_id>/status", methods=["GET"])
def get_agent_status(agent_id: str):
    """Get agent status."""
    return agent_management_handlers.handle_get_agent_status(request, agent_id)


@agent_management_bp.route("/<agent_id>/task-context", methods=["GET"])
def get_task_context(agent_id: str):
    """Get task context for agent."""
    return agent_management_handlers.handle_get_task_context(request, agent_id)

