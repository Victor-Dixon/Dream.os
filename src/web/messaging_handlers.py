"""
Messaging Handlers
==================

Handler classes for messaging operations.
Wires messaging services to web layer.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, handler pattern.
Consolidated: Uses BaseHandler + AvailabilityMixin.
"""

from flask import jsonify, request
from typing import Tuple, Any

from src.core.base.availability_mixin import AvailabilityMixin
from src.core.base.base_handler import BaseHandler

# Lazy import with availability flags
try:
    from src.services.messaging_cli_parser import create_messaging_parser
    MESSAGING_CLI_AVAILABLE = True
except ImportError:
    MESSAGING_CLI_AVAILABLE = False


class MessagingHandlers(BaseHandler, AvailabilityMixin):
    """Handler class for messaging operations."""
    
    def __init__(self):
        """Initialize messaging handlers."""
        super().__init__("MessagingHandlers")
    
    def handle_parse_cli(self, request) -> Tuple[Any, int]:
        """
        Handle request to parse messaging CLI command.
        
        Args:
            request: Flask request object
            
        Returns:
            Tuple of (response_data, status_code)
        """
        availability_error = self.check_availability(
            MESSAGING_CLI_AVAILABLE,
            "MessagingCLI"
        )
        if availability_error:
            return availability_error
        
        try:
            data = request.get_json() or {}
            command = data.get("command", "")
            
            if not command:
                error_response = self.format_response(
                    None,
                    success=False,
                    error="command is required"
                )
                return jsonify(error_response), 400
            
            parser = create_messaging_parser()
            args = parser.parse_args(command.split())
            
            result = {
                "parsed": True,
                "args": vars(args) if args else {}
            }
            
            response = self.format_response(result, success=True)
            return jsonify(response), 200
            
        except Exception as e:
            error_response = self.handle_error(e, "handle_parse_cli")
            return jsonify(error_response), 500
    
    def handle_get_cli_help(self, request) -> Tuple[Any, int]:
        """
        Handle request to get CLI help documentation.
        
        Args:
            request: Flask request object
            
        Returns:
            Tuple of (response_data, status_code)
        """
        availability_error = self.check_availability(
            MESSAGING_CLI_AVAILABLE,
            "MessagingCLI"
        )
        if availability_error:
            return availability_error
        
        try:
            parser = create_messaging_parser()
            help_text = parser.format_help()
            
            result = {
                "help": help_text,
                "available_commands": [
                    "parse", "help", "execute"
                ]
            }
            
            response = self.format_response(result, success=True)
            return jsonify(response), 200
            
        except Exception as e:
            error_response = self.handle_error(e, "handle_get_cli_help")
            return jsonify(error_response), 500
    
    def handle_execute_cli(self, request) -> Tuple[Any, int]:
        """
        Handle request to execute messaging CLI command.
        
        Args:
            request: Flask request object
            
        Returns:
            Tuple of (response_data, status_code)
        """
        availability_error = self.check_availability(
            MESSAGING_CLI_AVAILABLE,
            "MessagingCLI"
        )
        if availability_error:
            return availability_error
        
        try:
            data = request.get_json() or {}
            command = data.get("command", "")
            
            if not command:
                error_response = self.format_response(
                    None,
                    success=False,
                    error="command is required"
                )
                return jsonify(error_response), 400
            
            # Note: Actual execution would require subprocess or direct function calls
            # This is a placeholder for the execution logic
            result = {
                "executed": True,
                "command": command,
                "message": "CLI execution would be performed here"
            }
            
            response = self.format_response(result, success=True)
            return jsonify(response), 200
            
        except Exception as e:
            error_response = self.handle_error(e, "handle_execute_cli")
            return jsonify(error_response), 500
    
    # Template handlers moved to messaging_template_handlers.py for V2 compliance
    # Import and delegate to MessagingTemplateHandlers if needed


