#!/usr/bin/env python3
"""
Manager Registry Routes - Web Integration
========================================

Flask routes for Manager Registry functionality.
Exposes manager registration and access operations to web UI.

<!-- SSOT Domain: web -->

Author: Agent-7 (Web Development Specialist)
Date: 2025-12-05
V2 Compliant: Yes (<300 lines)
"""

from flask import Blueprint, jsonify, request
from typing import Any, Dict

# Lazy import to avoid circular dependencies
def _get_manager_registry():
    from src.core.managers.registry import ManagerRegistry
    return ManagerRegistry

# Create blueprint
manager_registry_bp = Blueprint(
    "manager_registry",
    __name__,
    url_prefix="/api/manager-registry"
)


@manager_registry_bp.route("/managers", methods=["GET"])
def list_managers():
    """List all registered managers."""
    try:
        registry = _get_manager_registry()()
        managers = registry.get_all_managers()
        
        manager_list = []
        for name, manager in managers.items():
            manager_list.append({
                "name": name,
                "type": type(manager).__name__,
                "initialized": hasattr(manager, '_initialized') and manager._initialized
            })
        
        return jsonify({
            "status": "success",
            "managers": manager_list,
            "total": len(manager_list)
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@manager_registry_bp.route("/managers/<manager_name>", methods=["GET"])
def get_manager(manager_name: str):
    """Get details for a specific manager."""
    try:
        registry = _get_manager_registry()()
        manager = registry.get_manager(manager_name)
        
        if not manager:
            return jsonify({
                "status": "error",
                "error": f"Manager '{manager_name}' not found"
            }), 404
        
        return jsonify({
            "status": "success",
            "manager": {
                "name": manager_name,
                "type": type(manager).__name__,
                "initialized": hasattr(manager, '_initialized') and manager._initialized
            }
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@manager_registry_bp.route("/managers/<manager_name>/execute", methods=["POST"])
def execute_manager_operation(manager_name: str):
    """Execute an operation on a specific manager."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "error": "No data provided"}), 400
        
        operation = data.get("operation")
        payload = data.get("payload", {})
        
        if not operation:
            return jsonify({"status": "error", "error": "Operation not specified"}), 400
        
        registry = _get_manager_registry()()
        from src.core.managers.contracts import ManagerContext
        context = ManagerContext(
            logger=lambda msg: None,
            config={}
        )
        
        result = registry.execute_operation(manager_name, context, operation, payload)
        
        return jsonify({
            "status": "success",
            "manager": manager_name,
            "operation": operation,
            "result": result.data if hasattr(result, 'data') else result
        }), 200
    except ValueError as e:
        return jsonify({"status": "error", "error": str(e)}), 404
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@manager_registry_bp.route("/types", methods=["GET"])
def list_manager_types():
    """List all registered manager types."""
    try:
        registry = _get_manager_registry()()
        manager_types = registry._manager_types if hasattr(registry, '_manager_types') else {}
        
        type_list = [
            {"name": name, "class": cls.__name__}
            for name, cls in manager_types.items()
        ]
        
        return jsonify({
            "status": "success",
            "manager_types": type_list,
            "total": len(type_list)
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@manager_registry_bp.route("/types", methods=["POST"])
def register_manager_type():
    """Register a new manager type."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "error": "No data provided"}), 400
        
        name = data.get("name")
        class_name = data.get("class_name")
        
        if not name or not class_name:
            return jsonify({
                "status": "error",
                "error": "name and class_name are required"
            }), 400
        
        # Import the manager class dynamically
        try:
            from src.core.managers import contracts
            manager_class = getattr(contracts, class_name, None)
            if not manager_class:
                # Try importing from managers module
                import importlib
                managers_module = importlib.import_module("src.core.managers")
                manager_class = getattr(managers_module, class_name, None)
            
            if not manager_class:
                return jsonify({
                    "status": "error",
                    "error": f"Manager class '{class_name}' not found"
                }), 404
            
            registry = _get_manager_registry()()
            registry.register_manager_type(name, manager_class)
            
            return jsonify({
                "status": "success",
                "message": f"Manager type '{name}' registered successfully"
            }), 201
        except Exception as e:
            return jsonify({
                "status": "error",
                "error": f"Failed to register manager type: {str(e)}"
            }), 500
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

