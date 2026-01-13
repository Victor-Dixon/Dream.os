"""
Validation Handlers
===================

Handler classes for unified validation tool operations.
Wires unified_validator.py to web layer with BaseHandler pattern.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, handler pattern.
"""

import json
from pathlib import Path
from typing import Any, Dict

from flask import jsonify, request

from src.core.base.base_handler import BaseHandler

# Import validation runner
from src.cli.validation_runner import ValidationRunner


class ValidationHandlers(BaseHandler):
    """Handler class for validation operations."""

    def __init__(self):
        """Initialize validation handlers."""
        super().__init__("ValidationHandlers")
        self.validator = ValidationRunner()

    def handle_validate(self, request) -> tuple:
        """
        Handle comprehensive validation request.

        Expected JSON body:
        {
            "output_file": "path/to/output.json" (optional)
        }
        """
        try:
            data = request.get_json() or {}
            output_file = data.get("output_file", "validation_results.json")

            # Run comprehensive validation
            result = self.validator.run_comprehensive_validation(output_file)

            from flask import jsonify
            return jsonify(self.format_response({
                "validation": result,
                "output_file": output_file
            })), 200
        except Exception as e:
            error_response = self.handle_error(e, "Validation failed")
            from flask import jsonify
            return jsonify(error_response), 500

    def handle_get_categories(self, request) -> tuple:
        """List available validation capabilities."""
        capabilities = [
            "comprehensive_validation",
            "ssot_compliance",
            "v2_compliance",
            "integration_status",
            "service_readiness",
            "code_quality"
        ]
        from flask import jsonify
        return jsonify(self.format_response({
            "capabilities": capabilities,
            "count": len(capabilities)
        })), 200

    def handle_full_validation(self, request) -> tuple:
        """
        Run full validation suite.
        
        Expected JSON body:
        {
            "file": "path/to/file" (optional)
        }
        """
        try:
            data = request.get_json() or {}
            file_path = data.get("file")
            results = self.validator.run_full_validation(file_path)
            from flask import jsonify
            return jsonify(self.format_response({
                "full_validation": results
            })), 200
        except Exception as e:
            error_response = self.handle_error(e, "Full validation failed")
            from flask import jsonify
            return jsonify(error_response), 500




