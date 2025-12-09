"""
AI Training Handlers
====================

Handler classes for AI training operations.
Wires AI training services to web layer.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, handler pattern.
Consolidated: Uses BaseHandler + AvailabilityMixin.
"""

from flask import jsonify, request
from typing import Any, Tuple

from src.core.base.availability_mixin import AvailabilityMixin
from src.core.base.base_handler import BaseHandler

# Lazy import with availability flag
try:
    from src.ai_training.dreamvault.runner import BatchRunner
    AI_TRAINING_AVAILABLE = True
except ImportError:
    AI_TRAINING_AVAILABLE = False


class AITrainingHandlers(BaseHandler, AvailabilityMixin):
    """Handler class for AI training operations."""

    def __init__(self):
        """Initialize AI training handlers."""
        super().__init__("AITrainingHandlers")

    def handle_get_dreamvault_status(self, request) -> Tuple[Any, int]:
        """
        Handle request to get DreamVault training status.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        availability_error = self.check_availability(
            AI_TRAINING_AVAILABLE,
            "AI Training services"
        )
        if availability_error:
            return availability_error

        try:
            response_data = {
                "status": "available",
                "service": "dreamvault_batch_runner"
            }
            response = self.format_response(response_data, success=True)
            return jsonify(response), 200
        except Exception as e:
            error_response = self.handle_error(e, "handle_get_dreamvault_status")
            return jsonify(error_response), 500

    def handle_run_dreamvault_batch(self, request) -> Tuple[Any, int]:
        """
        Handle request to run DreamVault batch processing.

        Args:
            request: Flask request object

        Returns:
            Tuple of (response_data, status_code)
        """
        availability_error = self.check_availability(
            AI_TRAINING_AVAILABLE,
            "AI Training services"
        )
        if availability_error:
            return availability_error

        try:
            data = request.get_json()
            config = data.get("config") if data else None
            
            if not config:
                error_response = self.format_response(
                    None,
                    success=False,
                    error="Config required for batch runner"
                )
                return jsonify(error_response), 400
            
            runner = BatchRunner(config)
            response_data = {
                "message": "Batch runner initialized",
                "runner_id": id(runner)
            }
            response = self.format_response(response_data, success=True)
            return jsonify(response), 200
        except Exception as e:
            error_response = self.handle_error(e, "handle_run_dreamvault_batch")
            return jsonify(error_response), 500

