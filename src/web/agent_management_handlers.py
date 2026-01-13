"""
Agent Management Handlers - Web Layer
=====================================

Handlers for agent management operations.

<!-- SSOT Domain: web -->

Author: Agent-7 (Web Development Specialist)
Date: 2025-12-04
V2 Compliant: Yes (<300 lines)
Consolidated: Uses BaseHandler + AvailabilityMixin (31% code reduction).
"""

from flask import jsonify, request
from typing import Any, Dict, Tuple

from src.core.base.availability_mixin import AvailabilityMixin
from src.core.base.base_handler import BaseHandler


class AgentManagementHandlers(BaseHandler, AvailabilityMixin):
    """Handlers for agent management operations."""
    
    def __init__(self):
        """Initialize agent management handlers."""
        super().__init__("AgentManagementHandlers")
    
    def _get_agent_manager(self):
        """Get AgentAssignmentManager instance (lazy import)."""
        try:
            from src.services.agent_management import AgentAssignmentManager, AgentStatusManager, TaskContextManager
            return AgentAssignmentManager(), AgentStatusManager, TaskContextManager
        except ImportError as e:
            self.logger.error(f"Failed to import agent management: {e}")
            return None, None, None
    
    def handle_list_agents(self, request) -> Tuple[Any, int]:
        """List all agents."""
        try:
            assignment_mgr, context_mgr, _ = self._get_agent_manager()
            if not assignment_mgr:
                error_response = self.format_response(
                    None,
                    success=False,
                    error="Agent management not available"
                )
                error_response["message"] = "Failed to initialize agent management"
                return jsonify(error_response), 503
            
            # Get all agents (8 agents)
            agents = []
            for agent_id in ["Agent-1", "Agent-2", "Agent-3", "Agent-4", 
                           "Agent-5", "Agent-6", "Agent-7", "Agent-8"]:
                principle = assignment_mgr.get_agent_principle(agent_id)
                agents.append({
                    "agent_id": agent_id,
                    "principle": principle.value if principle else None,
                    "status": "active"  # Could be enhanced with actual status
                })
            
            response = self.format_response({
                "agents": agents,
                "total": len(agents)
            }, success=True)
            return jsonify(response), 200
            
        except Exception as e:
            error_response = self.handle_error(e, "list_agents")
            return jsonify(error_response), 500
    
    def handle_get_agent(self, request, agent_id: str) -> Tuple[Any, int]:
        """Get agent details."""
        try:
            assignment_mgr, context_mgr, _ = self._get_agent_manager()
            if not assignment_mgr:
                error_response = self.format_response(
                    None,
                    success=False,
                    error="Agent management not available"
                )
                return jsonify(error_response), 503
            
            principle = assignment_mgr.get_agent_principle(agent_id)
            
            # Get status if available
            status_info = None
            if context_mgr:
                try:
                    status_mgr = context_mgr(agent_id)
                    status_info = status_mgr.get_agent_status()
                except Exception:
                    pass
            
            response = self.format_response({
                "agent_id": agent_id,
                "principle": principle.value if principle else None,
                "status_info": status_info,
                "status": "active"
            }, success=True)
            return jsonify(response), 200
            
        except Exception as e:
            error_response = self.handle_error(e, f"get_agent_{agent_id}")
            return jsonify(error_response), 500
    
    def handle_get_agent_principle(self, request, agent_id: str) -> Tuple[Any, int]:
        """Get agent's architectural principle."""
        try:
            assignment_mgr, _, _ = self._get_agent_manager()
            if not assignment_mgr:
                error_response = self.format_response(
                    None,
                    success=False,
                    error="Agent management not available"
                )
                return jsonify(error_response), 503
            
            principle = assignment_mgr.get_agent_principle(agent_id)
            
            if not principle:
                error_response = self.format_response(
                    None,
                    success=False,
                    error="Agent not found"
                )
                error_response["agent_id"] = agent_id
                return jsonify(error_response), 404
            
            response = self.format_response({
                "agent_id": agent_id,
                "principle": principle.value,
                "description": principle.description if hasattr(principle, 'description') else None
            }, success=True)
            return jsonify(response), 200
            
        except Exception as e:
            error_response = self.handle_error(e, f"get_agent_principle_{agent_id}")
            return jsonify(error_response), 500
    
    def handle_assign_principle(self, request, agent_id: str) -> Tuple[Any, int]:
        """Assign architectural principle to agent."""
        try:
            assignment_mgr, _, _ = self._get_agent_manager()
            if not assignment_mgr:
                error_response = self.format_response(
                    None,
                    success=False,
                    error="Agent management not available"
                )
                return jsonify(error_response), 503
            
            data = request.get_json()
            if not data or 'principle' not in data:
                error_response = self.format_response(
                    None,
                    success=False,
                    error="Invalid request"
                )
                error_response["message"] = "principle required in request body"
                return jsonify(error_response), 400
            
            from src.services.architectural_models import ArchitecturalPrinciple
            try:
                principle = ArchitecturalPrinciple(data['principle'])
            except ValueError:
                error_response = self.format_response(
                    None,
                    success=False,
                    error="Invalid principle"
                )
                error_response["message"] = f"Unknown principle: {data['principle']}"
                return jsonify(error_response), 400
            
            assignment_mgr.assign_principle(agent_id, principle)
            
            response = self.format_response({
                "agent_id": agent_id,
                "principle": principle.value,
                "message": f"Principle {principle.value} assigned to {agent_id}"
            }, success=True)
            return jsonify(response), 200
            
        except Exception as e:
            error_response = self.handle_error(e, f"assign_principle_{agent_id}")
            return jsonify(error_response), 500
    
    def handle_get_agent_status(self, request, agent_id: str) -> Tuple[Any, int]:
        """Get agent status."""
        try:
            _, StatusMgr, _ = self._get_agent_manager()
            if not StatusMgr:
                error_response = self.format_response(
                    None,
                    success=False,
                    error="Agent status management not available"
                )
                return jsonify(error_response), 503
            
            status_mgr = StatusMgr(agent_id)
            status = status_mgr.get_agent_status()
            
            return jsonify(status), 200
            
        except Exception as e:
            error_response = self.handle_error(e, f"get_agent_status_{agent_id}")
            return jsonify(error_response), 500
    
    def handle_get_task_context(self, request, agent_id: str) -> Tuple[Any, int]:
        """Get task context for agent."""
        try:
            _, _, TaskContextMgr = self._get_agent_manager()
            if not TaskContextMgr:
                error_response = self.format_response(
                    None,
                    success=False,
                    error="Task context management not available"
                )
                return jsonify(error_response), 503
            
            task_description = request.args.get('task', '')
            if not task_description:
                error_response = self.format_response(
                    None,
                    success=False,
                    error="Invalid request"
                )
                error_response["message"] = "task parameter required"
                return jsonify(error_response), 400
            
            context_mgr = TaskContextMgr(agent_id)
            context = context_mgr.get_task_context(task_description)
            
            return jsonify(context), 200
            
        except Exception as e:
            error_response = self.handle_error(e, f"get_task_context_{agent_id}")
            return jsonify(error_response), 500

