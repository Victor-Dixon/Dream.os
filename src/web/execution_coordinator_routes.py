#!/usr/bin/env python3
"""
Execution Coordinator Routes - Web Integration
=============================================

Flask routes for Execution Coordinator functionality.
Exposes execution coordination operations to web UI.

<!-- SSOT Domain: web -->

Author: Agent-7 (Web Development Specialist)
Date: 2025-12-05
V2 Compliant: Yes (<300 lines)
"""

from flask import Blueprint, jsonify, request
from typing import Any, Dict

# Lazy import to avoid circular dependencies
def _get_execution_coordinator():
    from src.core.managers.execution.execution_coordinator import ExecutionCoordinator
    return ExecutionCoordinator

# Create blueprint
execution_coordinator_bp = Blueprint(
    "execution_coordinator",
    __name__,
    url_prefix="/api/execution-coordinator"
)


@execution_coordinator_bp.route("/status", methods=["GET"])
def get_execution_status():
    """Get execution coordinator status."""
    try:
        coordinator = _get_execution_coordinator()()
        # Create minimal context for status check
        from src.core.managers.contracts import ManagerContext
        context = ManagerContext(
            logger=lambda msg: None,
            config={}
        )
        
        # Get status via execute operation
        result = coordinator.execute(context, "get_execution_status", {})
        
        return jsonify({
            "status": "success",
            "execution_status": result.data if hasattr(result, 'data') else "unknown",
            "coordinator_initialized": coordinator._initialized if hasattr(coordinator, '_initialized') else False
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@execution_coordinator_bp.route("/tasks", methods=["GET"])
def list_tasks():
    """List all execution tasks."""
    try:
        coordinator = _get_execution_coordinator()()
        from src.core.managers.contracts import ManagerContext
        context = ManagerContext(
            logger=lambda msg: None,
            config={}
        )
        
        result = coordinator.execute(context, "list_tasks", {})
        
        return jsonify({
            "status": "success",
            "tasks": result.data if hasattr(result, 'data') else []
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@execution_coordinator_bp.route("/tasks", methods=["POST"])
def create_task():
    """Create a new execution task."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "error": "No data provided"}), 400
        
        coordinator = _get_execution_coordinator()()
        from src.core.managers.contracts import ManagerContext
        context = ManagerContext(
            logger=lambda msg: None,
            config={}
        )
        
        result = coordinator.execute(context, "create_task", data)
        
        return jsonify({
            "status": "success",
            "task": result.data if hasattr(result, 'data') else None,
            "message": result.message if hasattr(result, 'message') else "Task created"
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@execution_coordinator_bp.route("/tasks/<task_id>", methods=["GET"])
def get_task_status(task_id: str):
    """Get status of a specific task."""
    try:
        coordinator = _get_execution_coordinator()()
        from src.core.managers.contracts import ManagerContext
        context = ManagerContext(
            logger=lambda msg: None,
            config={}
        )
        
        result = coordinator.execute(context, "get_task_status", {"task_id": task_id})
        
        return jsonify({
            "status": "success",
            "task_id": task_id,
            "task_status": result.data if hasattr(result, 'data') else None
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@execution_coordinator_bp.route("/tasks/<task_id>/execute", methods=["POST"])
def execute_task(task_id: str):
    """Execute a specific task."""
    try:
        data = request.get_json() or {}
        coordinator = _get_execution_coordinator()()
        from src.core.managers.contracts import ManagerContext
        context = ManagerContext(
            logger=lambda msg: None,
            config={}
        )
        
        payload = {"task_id": task_id, **data}
        result = coordinator.execute(context, "execute_task", payload)
        
        return jsonify({
            "status": "success",
            "task_id": task_id,
            "result": result.data if hasattr(result, 'data') else None,
            "message": result.message if hasattr(result, 'message') else "Task executed"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@execution_coordinator_bp.route("/protocols", methods=["GET"])
def list_protocols():
    """List all registered protocols."""
    try:
        coordinator = _get_execution_coordinator()()
        from src.core.managers.contracts import ManagerContext
        context = ManagerContext(
            logger=lambda msg: None,
            config={}
        )
        
        result = coordinator.execute(context, "list_protocols", {})
        
        return jsonify({
            "status": "success",
            "protocols": result.data if hasattr(result, 'data') else []
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@execution_coordinator_bp.route("/protocols", methods=["POST"])
def register_protocol():
    """Register a new protocol."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "error": "No data provided"}), 400
        
        coordinator = _get_execution_coordinator()()
        from src.core.managers.contracts import ManagerContext
        context = ManagerContext(
            logger=lambda msg: None,
            config={}
        )
        
        result = coordinator.execute(context, "register_protocol", data)
        
        return jsonify({
            "status": "success",
            "protocol": result.data if hasattr(result, 'data') else None,
            "message": result.message if hasattr(result, 'message') else "Protocol registered"
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

