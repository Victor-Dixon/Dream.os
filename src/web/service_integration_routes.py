#!/usr/bin/env python3
"""
Service Integration Routes - Web Integration
============================================

Flask routes for various service integrations.
Consolidates portfolio, AI, chat presence, learning, recommendation, performance, and work indexer services.

<!-- SSOT Domain: web -->

Author: Agent-7 (Web Development Specialist)
Date: 2025-12-05
V2 Compliant: Yes (<300 lines)
"""

from flask import Blueprint, jsonify, request
from typing import Any, Dict

# Import handlers (BaseHandler pattern)
from src.web.portfolio_handlers import PortfolioHandlers
from src.web.ai_handlers import AIHandlers

# Create handler instances
portfolio_handlers = PortfolioHandlers()
ai_handlers = AIHandlers()

# Lazy imports for other services (to be migrated to handlers)
def _get_chat_presence_orchestrator():
    from src.services.chat_presence.chat_presence_orchestrator import ChatPresenceOrchestrator
    return ChatPresenceOrchestrator()

def _get_learning_recommender():
    from src.services.learning_recommender import LearningRecommender
    return LearningRecommender()

def _get_recommendation_engine():
    from src.services.recommendation_engine import RecommendationEngine
    return RecommendationEngine()

def _get_performance_analyzer():
    from src.services.performance_analyzer import PerformanceAnalyzer
    return PerformanceAnalyzer()

def _get_work_indexer():
    from src.services.work_indexer import WorkIndexer
    return WorkIndexer()

# Create blueprint
service_integration_bp = Blueprint(
    "service_integration",
    __name__,
    url_prefix="/api/services"
)


# --- Portfolio Service Routes ---

@service_integration_bp.route("/portfolio", methods=["GET"])
def list_portfolios():
    """List all portfolios."""
    return portfolio_handlers.handle_list_portfolios(request)


@service_integration_bp.route("/portfolio", methods=["POST"])
def create_portfolio():
    """Create a new portfolio."""
    return portfolio_handlers.handle_create_portfolio(request)


# --- AI Service Routes ---

@service_integration_bp.route("/ai/conversations", methods=["GET"])
def list_conversations():
    """List all AI conversations."""
    return ai_handlers.handle_list_conversations(request)


@service_integration_bp.route("/ai/process", methods=["POST"])
def process_ai_message():
    """Process an AI message."""
    return ai_handlers.handle_process_message(request)


# --- Chat Presence Routes ---

@service_integration_bp.route("/chat-presence/status", methods=["GET"])
def get_chat_presence_status():
    """Get chat presence orchestrator status."""
    try:
        orchestrator = _get_chat_presence_orchestrator()
        status = orchestrator.get_status() if hasattr(orchestrator, 'get_status') else {"status": "active"}
        
        return jsonify({
            "status": "success",
            "chat_presence": status
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


# --- Learning Recommender Routes ---

@service_integration_bp.route("/learning/recommendations", methods=["POST"])
def get_learning_recommendations():
    """Get learning recommendations."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "error": "No data provided"}), 400
        
        user_id = data.get("user_id")
        context = data.get("context", {})
        
        if not user_id:
            return jsonify({"status": "error", "error": "user_id is required"}), 400
        
        recommender = _get_learning_recommender()
        recommendations = recommender.get_recommendations(user_id, context) if hasattr(recommender, 'get_recommendations') else []
        
        return jsonify({
            "status": "success",
            "user_id": user_id,
            "recommendations": recommendations
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


# --- Recommendation Engine Routes ---

@service_integration_bp.route("/recommendations", methods=["POST"])
def get_recommendations():
    """Get recommendations from recommendation engine."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "error": "No data provided"}), 400
        
        query = data.get("query")
        user_id = data.get("user_id")
        
        if not query:
            return jsonify({"status": "error", "error": "query is required"}), 400
        
        engine = _get_recommendation_engine()
        recommendations = engine.get_recommendations(query, user_id) if hasattr(engine, 'get_recommendations') else []
        
        return jsonify({
            "status": "success",
            "query": query,
            "recommendations": recommendations
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


# --- Performance Analyzer Routes ---

@service_integration_bp.route("/performance/analyze", methods=["POST"])
def analyze_performance():
    """Analyze performance metrics."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "error": "No data provided"}), 400
        
        metrics_data = data.get("metrics_data", {})
        
        analyzer = _get_performance_analyzer()
        analysis = analyzer.analyze(metrics_data) if hasattr(analyzer, 'analyze') else {}
        
        return jsonify({
            "status": "success",
            "analysis": analysis
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


# --- Work Indexer Routes ---

@service_integration_bp.route("/work-indexer/index", methods=["POST"])
def index_work():
    """Index work items."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "error": "No data provided"}), 400
        
        work_items = data.get("work_items", [])
        
        if not work_items:
            return jsonify({"status": "error", "error": "work_items are required"}), 400
        
        indexer = _get_work_indexer()
        result = indexer.index(work_items) if hasattr(indexer, 'index') else {"indexed": 0}
        
        return jsonify({
            "status": "success",
            "result": result
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@service_integration_bp.route("/work-indexer/search", methods=["POST"])
def search_work():
    """Search indexed work items."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "error": "No data provided"}), 400
        
        query = data.get("query")
        
        if not query:
            return jsonify({"status": "error", "error": "query is required"}), 400
        
        indexer = _get_work_indexer()
        results = indexer.search(query) if hasattr(indexer, 'search') else []
        
        return jsonify({
            "status": "success",
            "query": query,
            "results": results
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

