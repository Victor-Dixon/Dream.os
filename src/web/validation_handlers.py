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

# Import unified validator
import sys
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))
from tools.unified_validator import UnifiedValidator


class ValidationHandlers(BaseHandler):
    """Handler class for validation operations."""

    def __init__(self):
        """Initialize validation handlers."""
        super().__init__("ValidationHandlers")
        self.validator = UnifiedValidator()

    def handle_validate(self, request) -> tuple:
        """
        Handle validation request by category.
        
        Expected JSON body:
        {
            "category": "ssot_config|imports|code_docs|queue|session|refactor|tracker",
            "file": "path/to/file" (optional),
            "dir": "path/to/dir" (optional),
            "code_file": "path/to/code" (for code_docs),
            "doc_files": ["path1", "path2"] (for code_docs),
            "agent": "Agent-1" (for session)
        }
        """
        try:
            data = request.get_json() or {}
            category = data.get("category", "all")
            
            if category == "ssot_config":
                if data.get("file"):
                    result = self.validator.validate_ssot_config(file_path=data["file"])
                elif data.get("dir"):
                    result = self.validator.validate_ssot_config(dir_path=data["dir"])
                else:
                    result = self.validator.validate_ssot_config()
            elif category == "imports":
                if not data.get("file"):
                    return self.format_error("File path required for import validation", 400)
                result = self.validator.validate_imports(data["file"])
            elif category == "code_docs":
                if not data.get("code_file") or not data.get("doc_files"):
                    return self.format_error("Code file and doc files required", 400)
                result = self.validator.validate_code_docs_alignment(
                    data["code_file"], data["doc_files"]
                )
            elif category == "queue":
                result = self.validator.validate_queue_behavior()
            elif category == "session":
                result = self.validator.validate_session_transition(data.get("agent"))
            elif category == "refactor":
                if data.get("file"):
                    result = self.validator.validate_refactor_status(file_path=data["file"])
                elif data.get("dir"):
                    result = self.validator.validate_refactor_status(dir_path=data["dir"])
                else:
                    return self.format_error("File or directory path required", 400)
            elif category == "tracker":
                result = self.validator.validate_tracker_status()
            else:
                return self.format_error(f"Invalid category: {category}", 400)
            
            from flask import jsonify
            return jsonify(self.format_response({
                "category": category,
                "validation": result
            })), 200
        except Exception as e:
            error_response = self.handle_error(e, "Validation failed")
            from flask import jsonify
            return jsonify(error_response), 500

    def handle_get_categories(self, request) -> tuple:
        """List available validation categories."""
        categories = [
            "ssot_config",
            "imports",
            "code_docs",
            "queue",
            "session",
            "refactor",
            "tracker",
            "all"
        ]
        from flask import jsonify
        return jsonify(self.format_response({
            "categories": categories,
            "count": len(categories)
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




