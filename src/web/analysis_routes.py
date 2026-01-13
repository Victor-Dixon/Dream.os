"""
Analysis Routes
===============

Flask routes for unified analysis tool integration.
Provides API access to unified_analyzer.py functionality.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, single responsibility, route definitions.
"""

from flask import Blueprint, jsonify, request

from src.web.analysis_handlers import AnalysisHandlers

# Create blueprint
analysis_bp = Blueprint("analysis", __name__, url_prefix="/api/analysis")

# Create handler instance (BaseHandler pattern)
analysis_handlers = AnalysisHandlers()


@analysis_bp.route("/analyze", methods=["POST"])
def analyze():
    """Run analysis by category."""
    return analysis_handlers.handle_analyze(request)


@analysis_bp.route("/categories", methods=["GET"])
def get_categories():
    """List available analysis categories."""
    return analysis_handlers.handle_get_categories(request)


@analysis_bp.route("/repository", methods=["POST"])
def repository_analysis():
    """Run repository analysis."""
    return analysis_handlers.handle_repository_analysis(request)


@analysis_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "ok", "service": "analysis"})




