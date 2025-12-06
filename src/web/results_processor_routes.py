#!/usr/bin/env python3
"""
Results Processor Routes - Web Integration
==========================================

Flask routes for Results Processor functionality.
Exposes analysis and validation results processing to web UI.

<!-- SSOT Domain: web -->

Author: Agent-7 (Web Development Specialist)
Date: 2025-12-05
V2 Compliant: Yes (<300 lines)
"""

from flask import Blueprint, jsonify, request
from typing import Any, Dict

# Lazy import to avoid circular dependencies
def _get_analysis_processor():
    from src.core.managers.results.analysis_results_processor import AnalysisResultsProcessor
    return AnalysisResultsProcessor

def _get_validation_processor():
    from src.core.managers.results.validation_results_processor import ValidationResultsProcessor
    return ValidationResultsProcessor

# Create blueprint
results_processor_bp = Blueprint(
    "results_processor",
    __name__,
    url_prefix="/api/results-processor"
)


@results_processor_bp.route("/analysis", methods=["POST"])
def process_analysis():
    """Process analysis results."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "error": "No data provided"}), 400
        
        processor = _get_analysis_processor()()
        from src.core.managers.contracts import ManagerContext
        context = ManagerContext(
            logger=lambda msg: None,
            config={}
        )
        
        result_type = data.get("result_type", "analysis")
        result_data = data.get("result_data", {})
        
        processed = processor._process_result_by_type(context, result_type, result_data)
        
        return jsonify({
            "status": "success",
            "result_type": result_type,
            "processed_result": processed
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@results_processor_bp.route("/analysis/stats", methods=["POST"])
def get_analysis_stats():
    """Get analysis statistics for data points."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "error": "No data provided"}), 400
        
        data_points = data.get("data_points", [])
        if not data_points:
            return jsonify({"status": "error", "error": "No data points provided"}), 400
        
        processor = _get_analysis_processor()()
        from src.core.managers.contracts import ManagerContext
        context = ManagerContext(
            logger=lambda msg: None,
            config={}
        )
        
        result_data = {
            "analysis_type": data.get("analysis_type", "statistical"),
            "data_points": data_points,
            "analysis_config": data.get("analysis_config", {})
        }
        
        processed = processor._process_analysis_result(context, result_data)
        
        return jsonify({
            "status": "success",
            "statistics": processed.get("analysis_result", {}),
            "data_points_processed": processed.get("data_points_processed", 0)
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@results_processor_bp.route("/validation", methods=["POST"])
def process_validation():
    """Process validation results."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "error": "No data provided"}), 400
        
        processor = _get_validation_processor()()
        from src.core.managers.contracts import ManagerContext
        context = ManagerContext(
            logger=lambda msg: None,
            config={}
        )
        
        result_type = data.get("result_type", "validation")
        result_data = data.get("result_data", {})
        
        processed = processor._process_result_by_type(context, result_type, result_data)
        
        return jsonify({
            "status": "success",
            "result_type": result_type,
            "processed_result": processed
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@results_processor_bp.route("/validation/validate", methods=["POST"])
def validate_data():
    """Validate data against rules."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "error": "No data provided"}), 400
        
        validation_data = data.get("validation_data", {})
        validation_rules = data.get("validation_rules", [])
        
        if not validation_data or not validation_rules:
            return jsonify({
                "status": "error",
                "error": "validation_data and validation_rules are required"
            }), 400
        
        processor = _get_validation_processor()()
        from src.core.managers.contracts import ManagerContext
        context = ManagerContext(
            logger=lambda msg: None,
            config={}
        )
        
        result_data = {
            "validation_type": data.get("validation_type", "general"),
            "validation_data": validation_data,
            "validation_rules": validation_rules,
            "validation_config": data.get("validation_config", {})
        }
        
        processed = processor._process_validation_result(context, result_data)
        
        return jsonify({
            "status": "success",
            "validation_result": processed.get("validation_result", {}),
            "validation_passed": processed.get("validation_success", False),
            "errors": processed.get("validation_errors", [])
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

