"""
Monitoring Routes
================

Flask routes for monitoring lifecycle operations.
Wires monitoring services to web layer.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, single responsibility, route definitions.
"""

from flask import Blueprint, jsonify, request

from src.web.monitoring_handlers import MonitoringHandlers

# Create blueprint
monitoring_bp = Blueprint("monitoring", __name__, url_prefix="/api/monitoring")

# Create handler instance (BaseHandler pattern)
monitoring_handlers = MonitoringHandlers()


@monitoring_bp.route("/lifecycle/status", methods=["GET"])
def get_monitoring_status():
    """Get monitoring lifecycle status."""
    return monitoring_handlers.handle_get_monitoring_status(request)


@monitoring_bp.route("/lifecycle/initialize", methods=["POST"])
def initialize_monitoring():
    """Initialize monitoring lifecycle."""
    return monitoring_handlers.handle_initialize_monitoring(request)


@monitoring_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for monitoring services."""
    return jsonify({"status": "ok", "service": "monitoring"}), 200


# --- Metric Manager Routes ---

@monitoring_bp.route("/metrics", methods=["GET"])
def list_metrics():
    """List all metrics."""
    try:
        from src.core.managers.monitoring.metric_manager import MetricManager
        from src.core.managers.contracts import ManagerContext
        
        manager = MetricManager()
        context = ManagerContext(logger=lambda msg: None, config={})
        
        result = manager.list_metrics(context)
        metrics = result.data if hasattr(result, 'data') else {}
        
        return jsonify({
            "status": "success",
            "metrics": metrics,
            "total": len(metrics)
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@monitoring_bp.route("/metrics/<metric_name>", methods=["GET"])
def get_metric(metric_name: str):
    """Get a specific metric."""
    try:
        from src.core.managers.monitoring.metric_manager import MetricManager
        from src.core.managers.contracts import ManagerContext
        
        manager = MetricManager()
        context = ManagerContext(logger=lambda msg: None, config={})
        
        result = manager.get_metric(context, metric_name)
        metric = result.data if hasattr(result, 'data') else None
        
        if not metric:
            return jsonify({
                "status": "error",
                "error": f"Metric '{metric_name}' not found"
            }), 404
        
        return jsonify({
            "status": "success",
            "metric": metric
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@monitoring_bp.route("/metrics", methods=["POST"])
def record_metric():
    """Record a new metric value."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "error": "No data provided"}), 400
        
        metric_name = data.get("metric_name")
        metric_value = data.get("metric_value")
        
        if not metric_name or metric_value is None:
            return jsonify({
                "status": "error",
                "error": "metric_name and metric_value are required"
            }), 400
        
        from src.core.managers.monitoring.metric_manager import MetricManager
        from src.core.managers.contracts import ManagerContext
        
        manager = MetricManager()
        context = ManagerContext(logger=lambda msg: None, config={})
        
        result = manager.record_metric(context, metric_name, metric_value)
        
        return jsonify({
            "status": "success",
            "result": result.data if hasattr(result, 'data') else None,
            "message": result.message if hasattr(result, 'message') else "Metric recorded"
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


# --- Alert Manager Routes ---

@monitoring_bp.route("/alerts", methods=["GET"])
def list_alerts():
    """List all alerts."""
    try:
        from src.core.managers.monitoring.alert_manager import AlertManager
        from src.core.managers.contracts import ManagerContext
        
        manager = AlertManager()
        context = ManagerContext(logger=lambda msg: None, config={})
        
        result = manager.list_alerts(context)
        alerts = result.data if hasattr(result, 'data') else {}
        
        return jsonify({
            "status": "success",
            "alerts": alerts,
            "total": len(alerts)
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@monitoring_bp.route("/alerts", methods=["POST"])
def create_alert():
    """Create a new alert."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "error": "No data provided"}), 400
        
        from src.core.managers.monitoring.alert_manager import AlertManager
        from src.core.managers.contracts import ManagerContext
        
        manager = AlertManager()
        context = ManagerContext(logger=lambda msg: None, config={})
        
        result = manager.create_alert(context, data)
        
        return jsonify({
            "status": "success",
            "result": result.data if hasattr(result, 'data') else None,
            "message": result.message if hasattr(result, 'message') else "Alert created"
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@monitoring_bp.route("/alerts/<alert_id>/acknowledge", methods=["POST"])
def acknowledge_alert(alert_id: str):
    """Acknowledge an alert."""
    try:
        from src.core.managers.monitoring.alert_manager import AlertManager
        from src.core.managers.contracts import ManagerContext
        
        manager = AlertManager()
        context = ManagerContext(logger=lambda msg: None, config={})
        
        result = manager.acknowledge_alert(context, alert_id)
        
        return jsonify({
            "status": "success",
            "result": result.data if hasattr(result, 'data') else None,
            "message": result.message if hasattr(result, 'message') else "Alert acknowledged"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


# --- Widget Manager Routes ---

@monitoring_bp.route("/widgets", methods=["GET"])
def list_widgets():
    """List all monitoring widgets."""
    try:
        from src.core.managers.monitoring.widget_manager import WidgetManager
        from src.core.managers.contracts import ManagerContext
        
        manager = WidgetManager()
        context = ManagerContext(logger=lambda msg: None, config={})
        
        result = manager.list_widgets(context)
        widgets = result.data if hasattr(result, 'data') else {}
        
        return jsonify({
            "status": "success",
            "widgets": widgets,
            "total": len(widgets)
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@monitoring_bp.route("/widgets", methods=["POST"])
def create_widget():
    """Create a new monitoring widget."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "error": "No data provided"}), 400
        
        from src.core.managers.monitoring.widget_manager import WidgetManager
        from src.core.managers.contracts import ManagerContext
        
        manager = WidgetManager()
        context = ManagerContext(logger=lambda msg: None, config={})
        
        result = manager.create_widget(context, data)
        
        return jsonify({
            "status": "success",
            "result": result.data if hasattr(result, 'data') else None,
            "message": result.message if hasattr(result, 'message') else "Widget created"
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

