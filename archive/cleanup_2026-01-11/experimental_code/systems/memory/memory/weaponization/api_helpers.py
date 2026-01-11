"""
API helper functions for memory weaponization
Handles API script generation and deployment.
"""

import logging

logger = logging.getLogger(__name__)

def create_api_script() -> str:
    """
    Create context injection API script.
    
    Returns:
        String containing the API script
    """
    return '''#!/usr/bin/env python3
"""
Context Injection API
====================

API for injecting conversation context into AI interactions.
"""

from flask import Flask, request, jsonify
import json
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# In-memory storage for conversation context
conversation_context = {}

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "context_injection_api"})

@app.route('/inject_context', methods=['POST'])
def inject_context():
    """Inject conversation context."""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        conversation_id = data.get('conversation_id')
        context = data.get('context', {})
        
        if not conversation_id:
            return jsonify({"error": "conversation_id is required"}), 400
        
        # Store context
        conversation_context[conversation_id] = context
        
        logger.info(f"Context injected for conversation: {conversation_id}")
        
        return jsonify({
            "status": "success",
            "conversation_id": conversation_id,
            "context_size": len(str(context))
        })
        
    except Exception as e:
        logger.error(f"Error injecting context: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/get_context/<conversation_id>', methods=['GET'])
def get_context(conversation_id: str):
    """Get conversation context."""
    try:
        context = conversation_context.get(conversation_id, {})
        
        return jsonify({
            "status": "success",
            "conversation_id": conversation_id,
            "context": context,
            "found": bool(context)
        })
        
    except Exception as e:
        logger.error(f"Error getting context: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/list_contexts', methods=['GET'])
def list_contexts():
    """List all stored contexts."""
    try:
        return jsonify({
            "status": "success",
            "conversation_ids": list(conversation_context.keys()),
            "total_contexts": len(conversation_context)
        })
        
    except Exception as e:
        logger.error(f"Error listing contexts: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/clear_context/<conversation_id>', methods=['DELETE'])
def clear_context(conversation_id: str):
    """Clear conversation context."""
    try:
        if conversation_id in conversation_context:
            del conversation_context[conversation_id]
            logger.info(f"Context cleared for conversation: {conversation_id}")
            return jsonify({"status": "success", "message": "Context cleared"})
        else:
            return jsonify({"status": "not_found", "message": "Context not found"}), 404
            
    except Exception as e:
        logger.error(f"Error clearing context: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    logger.info("Starting Context Injection API...")
    app.run(debug=True, host='0.0.0.0', port=5000)
''' 