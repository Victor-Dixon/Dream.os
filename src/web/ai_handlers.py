"""
AI Handlers
===========

Handler classes for AI service operations.
Wires AIService to web layer.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, handler pattern.
Consolidated: Uses BaseHandler.
"""

from flask import jsonify, request
from typing import Tuple, Any

from src.core.base.base_handler import BaseHandler
from src.services.ai_service import AIService


class AIHandlers(BaseHandler):
    """Handler class for AI operations."""
    
    def __init__(self):
        """Initialize AI handlers."""
        super().__init__("AIHandlers")
        self.service = AIService()
    
    def handle_list_conversations(self, request) -> Tuple[Any, int]:
        """
        Handle request to list all AI conversations.
        
        Args:
            request: Flask request object
            
        Returns:
            Tuple of (response_data, status_code)
        """
        try:
            conversations = list(self.service.conversations.values())
            
            conversations_data = [
                {
                    "id": c.id,
                    "user_id": c.user_id,
                    "title": c.title,
                    "message_count": len(c.messages)
                }
                for c in conversations
            ]
            
            response = self.format_response(
                {
                    "conversations": conversations_data,
                    "total": len(conversations)
                },
                success=True
            )
            return jsonify(response), 200
            
        except Exception as e:
            error_response = self.handle_error(e, "handle_list_conversations")
            return jsonify(error_response), 500
    
    def handle_process_message(self, request) -> Tuple[Any, int]:
        """
        Handle request to process an AI message.
        
        Args:
            request: Flask request object
            
        Returns:
            Tuple of (response_data, status_code)
        """
        try:
            data = request.get_json()
            if not data:
                error_response = self.format_response(
                    None,
                    success=False,
                    error="No data provided"
                )
                return jsonify(error_response), 400
            
            message = data.get("message")
            user_id = data.get("user_id")
            conversation_id = data.get("conversation_id")
            
            if not message or not user_id:
                error_response = self.format_response(
                    None,
                    success=False,
                    error="message and user_id are required"
                )
                return jsonify(error_response), 400
            
            result = self.service.process_message(message, user_id, conversation_id)
            
            response = self.format_response(
                {"result": result},
                success=True
            )
            return jsonify(response), 200
            
        except Exception as e:
            error_response = self.handle_error(e, "handle_process_message")
            return jsonify(error_response), 500

