#!/usr/bin/env python3
"""
Manager Operations Routes - Web Integration
==========================================

Flask routes for Manager Metrics and Manager Operations functionality.
Exposes manager metrics tracking and operations to web UI.

<!-- SSOT Domain: web -->

Author: Agent-7 (Web Development Specialist)
Date: 2025-12-05
V2 Compliant: Yes (<300 lines)
"""

from flask import Blueprint, jsonify, request
from typing import Any, Dict

# Lazy imports to avoid circular dependencies
def _get_manager_metrics_tracker():
    from src.core.managers.manager_metrics import ManagerMetricsTracker
    return ManagerMetricsTracker()

# Create blueprint
manager_operations_bp = Blueprint(
    "manager_operations",
    __name__,
    url_prefix="/api/manager-operations"
)


@manager_operations_bp.route("/metrics", methods=["GET"])
def get_manager_metrics():
    """Get manager metrics."""
    try:
        tracker = _get_manager_metrics_tracker()
        metrics = tracker.get_metrics()
        
        return jsonify({
            "status": "success",
            "metrics": metrics
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@manager_operations_bp.route("/metrics/status", methods=["GET"])
def get_metrics_for_status():
    """Get metrics suitable for status reporting."""
    try:
        tracker = _get_manager_metrics_tracker()
        metrics = tracker.get_metrics_for_status()
        
        return jsonify({
            "status": "success",
            "metrics": metrics
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@manager_operations_bp.route("/metrics/reset", methods=["POST"])
def reset_metrics():
    """Reset manager metrics."""
    try:
        tracker = _get_manager_metrics_tracker()
        success = tracker.reset()
        
        return jsonify({
            "status": "success" if success else "error",
            "message": "Metrics reset successfully" if success else "Failed to reset metrics"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@manager_operations_bp.route("/metrics/record-operation", methods=["POST"])
def record_operation():
    """Record an operation start."""
    try:
        tracker = _get_manager_metrics_tracker()
        tracker.record_operation_start()
        
        return jsonify({
            "status": "success",
            "message": "Operation recorded"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@manager_operations_bp.route("/metrics/record-success", methods=["POST"])
def record_success():
    """Record a successful operation."""
    try:
        tracker = _get_manager_metrics_tracker()
        tracker.record_success()
        
        return jsonify({
            "status": "success",
            "message": "Success recorded"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@manager_operations_bp.route("/metrics/record-error", methods=["POST"])
def record_error():
    """Record a failed operation."""
    try:
        tracker = _get_manager_metrics_tracker()
        tracker.record_error()
        
        return jsonify({
            "status": "success",
            "message": "Error recorded"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

