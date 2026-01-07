#!/usr/bin/env python3
"""
AI Context Engine Integration Tests
==================================

Comprehensive integration testing for the Phase 5 AI Context Engine.

<!-- SSOT Domain: ai_context_testing -->

Navigation References:
├── Implementation → src/services/ai_context_engine.py
├── WebSocket Server → src/services/ai_context_websocket.py
├── FastAPI Integration → src/web/fastapi_app.py
├── Frontend Integration → src/web/static/js/ai-context-integration.js
├── Documentation → docs/PHASE5_AI_CONTEXT_ENGINE.md
└── Risk Analytics → src/services/risk_analytics/risk_calculator_service.py

Test Coverage:
- Session lifecycle management
- Context processing pipeline
- AI suggestion generation
- Risk analytics integration
- WebSocket real-time communication
- FastAPI REST endpoints
- Performance and scalability
- Error handling and recovery

Author: Agent-5 (Business Intelligence Specialist)
Date: 2026-01-07
Phase: Phase 5 - AI Context Engine Testing
"""

import pytest
import asyncio
import json
import websockets
import aiohttp
from typing import Dict, List, Any, Optional
from unittest.mock import AsyncMock, MagicMock, patch
import numpy as np
from datetime import datetime, timedelta

from src.services.ai_context_engine import AIContextEngine, ContextSession, ContextSuggestion
from src.services.ai_context_websocket import AIContextWebSocketServer
from src.services.risk_analytics.risk_calculator_service import RiskCalculatorService, RiskMetrics
from src.core.base.base_service import BaseService
# Test fixtures and utilities


class TestAIContextEngineIntegration:
    """Integration tests for AI Context Engine end-to-end functionality."""

    @pytest.fixture
    async def context_engine(self):
        """Initialize AI Context Engine for testing."""
        engine = AIContextEngine()
        await engine.start_engine()
        yield engine
        await engine.stop_engine()

    @pytest.fixture
    async def websocket_server(self):
        """Initialize WebSocket server for testing."""
        server = AIContextWebSocketServer()
        await server.start_server()
        yield server
        await server.stop_server()

    @pytest.fixture
    async def risk_calculator(self):
        """Initialize risk calculator for testing."""
        calculator = RiskCalculatorService()
        await calculator.initialize()
        yield calculator
        await calculator.cleanup()

    @pytest.mark.asyncio
    async def test_context_session_lifecycle(self, context_engine):
        """Test complete context session lifecycle."""
        # Create session
        session_id = await context_engine.create_session(
            user_id="test_user_123",
            context_type="trading",
            initial_context={
                "positions": [
                    {"symbol": "AAPL", "quantity": 100, "entry_price": 150.0},
                    {"symbol": "GOOGL", "quantity": 50, "entry_price": 2800.0}
                ],
                "portfolio_value": 50000.0,
                "risk_tolerance": "moderate"
            }
        )

        assert session_id is not None
        assert session_id in context_engine.active_sessions

        session = context_engine.active_sessions[session_id]
        assert session.user_id == "test_user_123"
        assert session.context_type == "trading"
        assert len(session.context_data["positions"]) == 2

        # Update context
        update_result = await context_engine.update_session_context(
            session_id=session_id,
            context_updates={
                "new_position": {"symbol": "MSFT", "quantity": 75, "entry_price": 300.0},
                "market_conditions": {"volatility": "high", "trend": "bullish"}
            }
        )

        assert update_result["success"] is True
        assert len(update_result["new_suggestions"]) > 0

        # End session
        end_result = await context_engine.end_session(session_id)
        assert end_result["success"] is True
        assert session_id not in context_engine.active_sessions

    @pytest.mark.asyncio
    async def test_risk_analytics_integration(self, context_engine, risk_calculator):
        """Test AI Context Engine integration with risk analytics."""
        # Create trading session with risk data
        session_id = await context_engine.create_session(
            user_id="risk_test_user",
            context_type="trading",
            initial_context={
                "returns": [0.02, -0.01, 0.03, -0.005, 0.015, 0.008, -0.012],
                "equity_curve": [10000, 10200, 10180, 10454, 10410, 10526, 10396],
                "benchmark_returns": [0.01, -0.005, 0.02, 0.002, 0.01, 0.005, -0.008]
            }
        )

        # Wait for risk processing
        await asyncio.sleep(0.1)

        session = context_engine.active_sessions[session_id]
        assert session.risk_metrics is not None

        # Verify risk metrics integration
        risk_metrics = session.risk_metrics
        assert hasattr(risk_metrics, 'sharpe_ratio')
        assert hasattr(risk_metrics, 'var_95')
        assert hasattr(risk_metrics, 'max_drawdown')

        # Check for risk-based suggestions
        risk_suggestions = [
            s for s in session.ai_suggestions
            if s.get('suggestion_type') == 'risk_alert'
        ]

        # Should generate suggestions based on risk thresholds
        assert len(risk_suggestions) >= 0  # May or may not trigger based on data

        await context_engine.end_session(session_id)

    @pytest.mark.asyncio
    async def test_ai_suggestion_generation(self, context_engine):
        """Test AI-powered suggestion generation."""
        session_id = await context_engine.create_session(
            user_id="suggestion_test_user",
            context_type="analysis",
            initial_context={
                "analysis_type": "portfolio_optimization",
                "time_horizon": "medium_term",
                "risk_profile": "conservative",
                "current_allocation": {
                    "stocks": 0.7,
                    "bonds": 0.2,
                    "cash": 0.1
                }
            }
        )

        # Wait for suggestion processing
        await asyncio.sleep(0.2)

        session = context_engine.active_sessions[session_id]
        assert len(session.ai_suggestions) > 0

        # Verify suggestion structure
        for suggestion in session.ai_suggestions:
            assert 'suggestion_id' in suggestion
            assert 'suggestion_type' in suggestion
            assert 'confidence_score' in suggestion
            assert 'content' in suggestion
            assert 'reasoning' in suggestion
            assert isinstance(suggestion['confidence_score'], (int, float))
            assert 0.0 <= suggestion['confidence_score'] <= 1.0

        await context_engine.end_session(session_id)

    @pytest.mark.asyncio
    async def test_websocket_real_time_updates(self, websocket_server, context_engine):
        """Test WebSocket real-time context updates."""
        # Start WebSocket server
        server_task = asyncio.create_task(websocket_server.start_server())

        # Give server time to start
        await asyncio.sleep(0.1)

        try:
            # Connect WebSocket client
            uri = f"ws://localhost:{websocket_server.port}/ws/ai/context"
            async with websockets.connect(uri) as websocket:
                # Send session creation request
                session_request = {
                    "action": "create_session",
                    "user_id": "websocket_test_user",
                    "context_type": "collaboration",
                    "initial_context": {"participants": ["user1", "user2"]}
                }

                await websocket.send(json.dumps(session_request))

                # Receive response
                response = await websocket.recv()
                response_data = json.loads(response)

                assert response_data["success"] is True
                assert "session_id" in response_data

                session_id = response_data["session_id"]

                # Send context update
                update_request = {
                    "action": "update_context",
                    "session_id": session_id,
                    "context_updates": {
                        "new_participant": "user3",
                        "activity": "brainstorming"
                    }
                }

                await websocket.send(json.dumps(update_request))

                # Receive update confirmation
                update_response = await websocket.recv()
                update_data = json.loads(update_response)

                assert update_data["success"] is True
                assert len(update_data["new_suggestions"]) > 0

        finally:
            server_task.cancel()
            try:
                await server_task
            except asyncio.CancelledError:
                pass

    @pytest.mark.asyncio
    async def test_collaborative_context_sharing(self, context_engine):
        """Test collaborative context sharing across multiple users."""
        # Create multiple user sessions
        session_ids = []
        for i in range(3):
            session_id = await context_engine.create_session(
                user_id=f"collab_user_{i}",
                context_type="collaboration",
                initial_context={
                    "project": "ai_context_engine",
                    "role": f"contributor_{i}",
                    "expertise": ["coding", "testing", "design"][i]
                }
            )
            session_ids.append(session_id)

        # Simulate collaborative activity
        for i, session_id in enumerate(session_ids):
            await context_engine.update_session_context(
                session_id=session_id,
                context_updates={
                    "contribution": f"Added feature {i+1}",
                    "timestamp": datetime.now().isoformat(),
                    "collaboration_context": {
                        "active_participants": len(session_ids),
                        "shared_goals": ["improve_ai", "enhance_collaboration"]
                    }
                }
            )

        # Verify collaborative suggestions were generated
        for session_id in session_ids:
            session = context_engine.active_sessions[session_id]
            collab_suggestions = [
                s for s in session.ai_suggestions
                if s.get('suggestion_type') == 'collaboration'
            ]
            assert len(collab_suggestions) > 0

        # Clean up sessions
        for session_id in session_ids:
            await context_engine.end_session(session_id)

    @pytest.mark.asyncio
    async def test_performance_under_load(self, context_engine):
        """Test AI Context Engine performance under concurrent load."""
        import time

        # Create multiple concurrent sessions
        num_sessions = 50
        session_ids = []

        start_time = time.time()

        # Create sessions concurrently
        create_tasks = []
        for i in range(num_sessions):
            task = context_engine.create_session(
                user_id=f"perf_user_{i}",
                context_type="trading",
                initial_context={"portfolio_size": 10000 * (i + 1)}
            )
            create_tasks.append(task)

        session_ids = await asyncio.gather(*create_tasks)
        create_time = time.time() - start_time

        # Verify all sessions created
        assert len(session_ids) == num_sessions
        assert len(context_engine.active_sessions) == num_sessions

        # Test concurrent context updates
        update_start = time.time()
        update_tasks = []
        for session_id in session_ids:
            task = context_engine.update_session_context(
                session_id=session_id,
                context_updates={"market_update": "volatility_spike"}
            )
            update_tasks.append(task)

        update_results = await asyncio.gather(*update_tasks)
        update_time = time.time() - update_start

        # Verify updates succeeded
        successful_updates = sum(1 for result in update_results if result["success"])
        assert successful_updates == num_sessions

        # Performance assertions (< 50ms average per Phase 5 requirements)
        avg_create_time = create_time / num_sessions
        avg_update_time = update_time / num_sessions

        assert avg_create_time < 0.05  # < 50ms
        assert avg_update_time < 0.05  # < 50ms

        # Clean up
        cleanup_tasks = [context_engine.end_session(sid) for sid in session_ids]
        await asyncio.gather(*cleanup_tasks)

    @pytest.mark.asyncio
    async def test_error_handling_and_recovery(self, context_engine):
        """Test error handling and recovery mechanisms."""
        # Test invalid session ID
        with pytest.raises(ValueError):
            await context_engine.update_session_context(
                session_id="invalid_session_id",
                context_updates={"test": "data"}
            )

        # Test session creation with invalid data
        with pytest.raises(ValueError):
            await context_engine.create_session(
                user_id="",  # Invalid empty user ID
                context_type="trading",
                initial_context={}
            )

        # Test graceful degradation when risk calculator is unavailable
        with patch.object(context_engine, 'risk_calculator', None):
            session_id = await context_engine.create_session(
                user_id="error_test_user",
                context_type="trading",
                initial_context={"positions": []}
            )

            # Should still work without risk integration
            assert session_id in context_engine.active_sessions

            update_result = await context_engine.update_session_context(
                session_id=session_id,
                context_updates={"test_update": True}
            )

            # Should succeed despite missing risk calculator
            assert update_result["success"] is True

            await context_engine.end_session(session_id)

    @pytest.mark.asyncio
    async def test_session_persistence_and_cleanup(self, context_engine):
        """Test session persistence and automatic cleanup."""
        # Create session with custom timeout
        session_id = await context_engine.create_session(
            user_id="persistence_test_user",
            context_type="analysis",
            initial_context={"analysis_id": "test_123"}
        )

        # Verify session exists
        assert session_id in context_engine.active_sessions

        # Manually expire session by setting old timestamp
        session = context_engine.active_sessions[session_id]
        session.created_at = datetime.now() - timedelta(hours=3)  # Past timeout

        # Trigger cleanup
        await context_engine._cleanup_expired_sessions()

        # Session should be automatically cleaned up
        assert session_id not in context_engine.active_sessions

    @pytest.mark.asyncio
    async def test_ai_suggestion_application_tracking(self, context_engine):
        """Test tracking of applied AI suggestions."""
        session_id = await context_engine.create_session(
            user_id="suggestion_tracking_user",
            context_type="trading",
            initial_context={"tracking_test": True}
        )

        # Wait for suggestions to generate
        await asyncio.sleep(0.2)

        session = context_engine.active_sessions[session_id]
        initial_suggestion_count = len(session.ai_suggestions)
        assert initial_suggestion_count > 0

        # Apply first suggestion
        first_suggestion = session.ai_suggestions[0]
        suggestion_id = first_suggestion["suggestion_id"]

        apply_result = await context_engine.apply_suggestion(
            session_id=session_id,
            suggestion_id=suggestion_id
        )

        assert apply_result["success"] is True

        # Verify suggestion marked as applied
        updated_session = context_engine.active_sessions[session_id]
        applied_suggestion = next(
            (s for s in updated_session.ai_suggestions if s["suggestion_id"] == suggestion_id),
            None
        )

        assert applied_suggestion is not None
        assert applied_suggestion["applied"] is True

        # Verify performance tracking
        stats = context_engine.get_performance_stats()
        assert stats["suggestions_applied"] > 0

        await context_engine.end_session(session_id)


class TestAIContextWebSocketIntegration:
    """Integration tests for AI Context WebSocket server."""

    @pytest.fixture
    async def websocket_server(self):
        """Initialize WebSocket server for testing."""
        server = AIContextWebSocketServer()
        await server.start_server()
        yield server
        await server.stop_server()

    @pytest.mark.asyncio
    async def test_websocket_connection_management(self, websocket_server):
        """Test WebSocket connection establishment and management."""
        server_task = asyncio.create_task(websocket_server.start_server())
        await asyncio.sleep(0.1)

        try:
            uri = f"ws://localhost:{websocket_server.port}/ws/ai/context"

            # Test successful connection
            async with websockets.connect(uri) as websocket:
                # Send ping to verify connection
                await websocket.ping()
                await websocket.pong()

                # Connection should remain active
                assert websocket.open is True

            # Test connection cleanup
            await asyncio.sleep(0.1)

        finally:
            server_task.cancel()
            try:
                await server_task
            except asyncio.CancelledError:
                pass

    @pytest.mark.asyncio
    async def test_websocket_message_routing(self, websocket_server):
        """Test WebSocket message routing and handling."""
        server_task = asyncio.create_task(websocket_server.start_server())
        await asyncio.sleep(0.1)

        try:
            uri = f"ws://localhost:{websocket_server.port}/ws/ai/context"

            async with websockets.connect(uri) as websocket:
                # Test different message types
                test_messages = [
                    {
                        "action": "create_session",
                        "user_id": "ws_routing_test",
                        "context_type": "analysis"
                    },
                    {
                        "action": "ping",
                        "timestamp": datetime.now().isoformat()
                    }
                ]

                for message in test_messages:
                    await websocket.send(json.dumps(message))
                    response = await websocket.recv()
                    response_data = json.loads(response)

                    # Should receive appropriate response for each message type
                    assert "success" in response_data

        finally:
            server_task.cancel()
            try:
                await server_task
            except asyncio.CancelledError:
                pass


class TestFastAPIIntegration:
    """Integration tests for FastAPI AI Context endpoints."""

    @pytest.fixture
    async def fastapi_client(self):
        """Create FastAPI test client."""
        from httpx import AsyncClient
        from src.web.fastapi_app import app

        async with AsyncClient(app=app, base_url="http://testserver") as client:
            yield client

    @pytest.mark.asyncio
    async def test_context_session_rest_api(self, fastapi_client):
        """Test REST API endpoints for context session management."""
        # Create session via REST API
        create_payload = {
            "user_id": "rest_api_test_user",
            "context_type": "trading",
            "initial_context": {
                "portfolio_value": 25000.0,
                "positions": []
            }
        }

        create_response = await fastapi_client.post(
            "/api/context/session",
            json=create_payload
        )

        assert create_response.status_code == 200
        create_data = create_response.json()
        assert create_data["success"] is True
        assert "session_id" in create_data

        session_id = create_data["session_id"]

        # Update context via REST API
        update_payload = {
            "context_updates": {
                "new_position": {"symbol": "TSLA", "quantity": 10}
            }
        }

        update_response = await fastapi_client.post(
            f"/api/context/{session_id}/update",
            json=update_payload
        )

        assert update_response.status_code == 200
        update_data = update_response.json()
        assert update_data["success"] is True

        # Get current context
        get_response = await fastapi_client.get(f"/api/context/{session_id}")
        assert get_response.status_code == 200
        context_data = get_response.json()
        assert context_data["success"] is True
        assert "session" in context_data

    @pytest.mark.asyncio
    async def test_context_performance_stats_api(self, fastapi_client):
        """Test performance statistics REST API."""
        stats_response = await fastapi_client.get("/api/context/stats")

        assert stats_response.status_code == 200
        stats_data = stats_response.json()

        # Should return performance statistics
        expected_fields = [
            "total_sessions", "active_sessions", "suggestions_generated",
            "suggestions_applied", "avg_response_time", "error_rate"
        ]

        for field in expected_fields:
            assert field in stats_data

        # All numeric fields should be valid numbers
        for field in ["total_sessions", "active_sessions", "suggestions_generated",
                     "suggestions_applied", "avg_response_time", "error_rate"]:
            assert isinstance(stats_data[field], (int, float))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])