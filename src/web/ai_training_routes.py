"""
AI Training Routes
==================

Flask routes for AI training operations.
Wires AI training services to web layer.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, single responsibility, route definitions.
"""

from flask import Blueprint, jsonify, request

from src.web.ai_training_handlers import AITrainingHandlers

# Create blueprint
ai_training_bp = Blueprint("ai_training", __name__, url_prefix="/api/ai-training")

# Instantiate handler (BaseHandler pattern)
ai_training_handlers = AITrainingHandlers()


@ai_training_bp.route("/dreamvault/status", methods=["GET"])
def get_dreamvault_status():
    """Get DreamVault training status."""
    return ai_training_handlers.handle_get_dreamvault_status(request)


@ai_training_bp.route("/dreamvault/run", methods=["POST"])
def run_dreamvault_batch():
    """Run DreamVault batch processing."""
    return ai_training_handlers.handle_run_dreamvault_batch(request)


@ai_training_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for AI training services."""
    return jsonify({"status": "ok", "service": "ai_training"}), 200

