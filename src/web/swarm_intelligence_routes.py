#!/usr/bin/env python3
"""
Swarm Intelligence Routes - Web Integration
===========================================

Flask routes for Swarm Intelligence Manager functionality.
Exposes swarm intelligence operations to web UI.

<!-- SSOT Domain: web -->

Author: Agent-7 (Web Development Specialist)
Date: 2025-12-05
V2 Compliant: Yes (<300 lines)
"""

from flask import Blueprint, jsonify, request
from typing import Any, Dict

# Lazy import to avoid circular dependencies
def _get_swarm_intelligence_manager(agent_id: str = "Agent-7"):
<<<<<<< HEAD
    from src.services.unified_service_managers import SwarmIntelligenceManager
=======
    from src.services.swarm_intelligence_manager import SwarmIntelligenceManager
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
    return SwarmIntelligenceManager(agent_id)

# Create blueprint
swarm_intelligence_bp = Blueprint(
    "swarm_intelligence",
    __name__,
    url_prefix="/api/swarm-intelligence"
)


@swarm_intelligence_bp.route("/status", methods=["GET"])
def get_swarm_status():
    """Get swarm intelligence status."""
    try:
        agent_id = request.args.get("agent_id", "Agent-7")
        manager = _get_swarm_intelligence_manager(agent_id)
        
        return jsonify({
            "status": "success",
            "agent_id": agent_id,
            "swarm_status": {
                "vector_integration": manager.vector_integration,
                "config": manager.config,
                "swarm_agents": manager.config.get("swarm_agents", [])
            }
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@swarm_intelligence_bp.route("/intelligence", methods=["POST"])
def get_intelligence():
    """Get swarm intelligence insights for a query."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "error": "No data provided"}), 400
        
        query = data.get("query")
        agent_id = data.get("agent_id", "Agent-7")
        
        if not query:
            return jsonify({"status": "error", "error": "query is required"}), 400
        
        manager = _get_swarm_intelligence_manager(agent_id)
        intelligence = manager.get_swarm_intelligence(query)
        
        return jsonify({
            "status": "success",
            "query": query,
            "intelligence": intelligence
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@swarm_intelligence_bp.route("/analyze", methods=["POST"])
def analyze_swarm():
    """Trigger swarm analysis."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "error": "No data provided"}), 400
        
        query = data.get("query")
        agent_id = data.get("agent_id", "Agent-7")
        
        if not query:
            return jsonify({"status": "error", "error": "query is required"}), 400
        
        manager = _get_swarm_intelligence_manager(agent_id)
        analysis_result = manager.get_swarm_intelligence(query)
        
        return jsonify({
            "status": "success",
            "query": query,
            "analysis": analysis_result
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@swarm_intelligence_bp.route("/coordination", methods=["GET"])
def get_coordination_opportunities():
    """Get coordination opportunities across swarm."""
    try:
        agent_id = request.args.get("agent_id", "Agent-7")
        manager = _get_swarm_intelligence_manager(agent_id)
        
        # Get coordination opportunities (requires a query context)
        query = request.args.get("query", "general coordination")
        opportunities = manager._find_coordination_opportunities(query)
        
        return jsonify({
            "status": "success",
            "agent_id": agent_id,
            "query": query,
            "coordination_opportunities": opportunities
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@swarm_intelligence_bp.route("/patterns", methods=["GET"])
def get_swarm_patterns():
    """Get swarm behavior patterns."""
    try:
        agent_id = request.args.get("agent_id", "Agent-7")
        manager = _get_swarm_intelligence_manager(agent_id)
        
        query = request.args.get("query", "swarm patterns")
        patterns = manager._analyze_swarm_patterns(query)
        
        return jsonify({
            "status": "success",
            "agent_id": agent_id,
            "query": query,
            "swarm_patterns": patterns
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

