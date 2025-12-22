"""
Messaging Template Handlers
===========================

Handler classes for messaging template operations.
Extracted from messaging_handlers.py for V2 compliance.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, handler pattern.
"""

from flask import jsonify, request
from typing import Tuple, Any

from src.core.base.availability_mixin import AvailabilityMixin
from src.core.base.base_handler import BaseHandler

try:
    from src.services.utils.messaging_templates import (
        format_template,
        validate_template_vars,
        SURVEY_MESSAGE_TEMPLATE,
        CONSOLIDATION_MESSAGE_TEMPLATE
    )
    MESSAGING_TEMPLATES_AVAILABLE = True
except ImportError:
    MESSAGING_TEMPLATES_AVAILABLE = False


class MessagingTemplateHandlers(BaseHandler, AvailabilityMixin):
    """Handler class for messaging template operations."""
    
    def __init__(self):
        """Initialize messaging template handlers."""
        super().__init__("MessagingTemplateHandlers")
    
    def handle_list_templates(self, request) -> Tuple[Any, int]:
        """
        Handle request to list available messaging templates.
        
        Args:
            request: Flask request object
            
        Returns:
            Tuple of (response_data, status_code)
        """
        availability_error = self.check_availability(
            MESSAGING_TEMPLATES_AVAILABLE,
            "MessagingTemplates"
        )
        if availability_error:
            return availability_error
        
        try:
            templates = [
                {
                    "name": "survey",
                    "description": "Survey coordination message template"
                },
                {
                    "name": "consolidation",
                    "description": "Consolidation coordination message template"
                }
            ]
            
            result = {
                "templates": templates,
                "total": len(templates)
            }
            
            response = self.format_response(result, success=True)
            return jsonify(response), 200
            
        except Exception as e:
            error_response = self.handle_error(e, "handle_list_templates")
            return jsonify(error_response), 500
    
    def handle_render_template(self, request) -> Tuple[Any, int]:
        """
        Handle request to render messaging template with variables.
        
        Args:
            request: Flask request object
            
        Returns:
            Tuple of (response_data, status_code)
        """
        availability_error = self.check_availability(
            MESSAGING_TEMPLATES_AVAILABLE,
            "MessagingTemplates"
        )
        if availability_error:
            return availability_error
        
        try:
            data = request.get_json() or {}
            template_name = data.get("template_name", "")
            variables = data.get("variables", {})
            
            if not template_name:
                error_response = self.format_response(
                    None,
                    success=False,
                    error="template_name is required"
                )
                return jsonify(error_response), 400
            
            # Get template
            if template_name == "survey":
                template = SURVEY_MESSAGE_TEMPLATE
            elif template_name == "consolidation":
                template = CONSOLIDATION_MESSAGE_TEMPLATE
            else:
                error_response = self.format_response(
                    None,
                    success=False,
                    error=f"Template '{template_name}' not found"
                )
                return jsonify(error_response), 404
            
            # Validate and render
            is_valid, error = validate_template_vars(template, variables)
            if not is_valid:
                error_response = self.format_response(
                    None,
                    success=False,
                    error=error
                )
                return jsonify(error_response), 400
            
            rendered = format_template(template, **variables)
            
            result = {
                "template_name": template_name,
                "rendered": rendered
            }
            
            response = self.format_response(result, success=True)
            return jsonify(response), 200
            
        except Exception as e:
            error_response = self.handle_error(e, "handle_render_template")
            return jsonify(error_response), 500
    
    def handle_get_template(self, request) -> Tuple[Any, int]:
        """
        Handle request to get specific template by name.
        
        Args:
            request: Flask request object
            
        Returns:
            Tuple of (response_data, status_code)
        """
        availability_error = self.check_availability(
            MESSAGING_TEMPLATES_AVAILABLE,
            "MessagingTemplates"
        )
        if availability_error:
            return availability_error
        
        try:
            template_name = request.args.get("name", "")
            
            if not template_name:
                error_response = self.format_response(
                    None,
                    success=False,
                    error="name parameter is required"
                )
                return jsonify(error_response), 400
            
            # Get template
            if template_name == "survey":
                template = SURVEY_MESSAGE_TEMPLATE
            elif template_name == "consolidation":
                template = CONSOLIDATION_MESSAGE_TEMPLATE
            else:
                error_response = self.format_response(
                    None,
                    success=False,
                    error=f"Template '{template_name}' not found"
                )
                return jsonify(error_response), 404
            
            result = {
                "template_name": template_name,
                "template": template
            }
            
            response = self.format_response(result, success=True)
            return jsonify(response), 200
            
        except Exception as e:
            error_response = self.handle_error(e, "handle_get_template")
            return jsonify(error_response), 500

