#!/usr/bin/env python3
"""
AI Context WebSocket Server - Phase 5 Real-time Intelligence
==========================================================

Real-time WebSocket server for AI-powered context processing and live suggestions.

<!-- SSOT Domain: ai_context -->

Navigation References:
├── Related Files:
│   ├── Context Engine → src/services/ai_context_engine.py::AIContextEngine
│   ├── Risk WebSocket → src/services/risk_analytics/risk_websocket_server.py
│   ├── FastAPI Integration → src/web/fastapi_app.py
│   ├── Dashboard Integration → src/web/static/js/trading-robot/risk-dashboard-integration.js
│   └── Real-time Processing → src/core/analytics/engines/realtime_analytics_engine.py
├── Documentation:
│   ├── Phase 5 Architecture → docs/PHASE5_AI_CONTEXT_ENGINE.md
│   ├── WebSocket Architecture → docs/analytics/AGENT2_WEBSOCKET_ARCHITECTURE_REVIEW.md
│   └── Integration Demo → docs/analytics/trading_robot_risk_integration_demo.html
└── Testing:
    └── Integration Tests → tests/integration/test_ai_context_websocket.py

Features:
- Real-time context processing and suggestions
- Live collaborative context sharing
- Intelligent UX personalization
- Performance monitoring and optimization
- Session state synchronization

Author: Agent-5 (Business Intelligence Specialist)
Date: 2026-01-07
Phase: Phase 5 - AI Context Engine
"""

import asyncio
import json
import logging
import threading
import time
from typing import Dict, List, Any, Optional, Set
import websockets
from websockets.exceptions import ConnectionClosedError, WebSocketException

from src.services.ai_context_engine import ai_context_engine, ContextSuggestion

logger = logging.getLogger(__name__)


class AIContextWebSocketServer:
    """
    WebSocket server for real-time AI context processing.

    Features:
    - Live context updates and suggestions
    - Collaborative session sharing
    - Intelligent personalization
    - Performance optimization for <50ms latency
    """

    def __init__(self, host: str = "localhost", port: int = 8766):  # Different port from risk websocket
        self.host = host
        self.port = port
        self.server = None
        self.running = False

        # Connection management
        self.active_connections: Dict[str, Set[websockets.WebSocketServerProtocol]] = {
            "context": set(),
            "suggestions": set(),
            "collaboration": set()
        }

        # Session tracking
        self.session_connections: Dict[str, Set[websockets.WebSocketServerProtocol]] = {}

        # Performance monitoring
        self.performance_stats = {
            "total_connections": 0,
            "active_connections": 0,
            "messages_processed": 0,
            "suggestions_delivered": 0,
            "context_updates": 0,
            "avg_response_time": 0.0
        }

        # Background tasks
        self.heartbeat_task = None
        self.monitoring_task = None

    async def start(self):
        """Start the AI Context WebSocket server."""
        if self.running:
            logger.warning("Server is already running")
            return

        self.running = True
        logger.info(f"🧠 Starting AI Context WebSocket Server on {self.host}:{self.port}")

        # Start background tasks
        self.heartbeat_task = asyncio.create_task(self._heartbeat())
        self.monitoring_task = asyncio.create_task(self._performance_monitor())

        try:
            # Start WebSocket server
            self.server = await websockets.serve(
                self._handle_connection,
                self.host,
                self.port,
                ping_interval=20,
                ping_timeout=10,
                max_size=1_048_576,
                compression=None
            )

            logger.info("✅ AI Context WebSocket Server started successfully")
            logger.info("Available endpoints:")
            logger.info("  - ws://localhost:8766/ws/ai/context")
            logger.info("  - ws://localhost:8766/ws/ai/suggestions")
            logger.info("  - ws://localhost:8766/ws/ai/collaboration")

            # Keep server running
            await self.server.wait_closed()

        except Exception as e:
            logger.error(f"Failed to start WebSocket server: {e}")
            raise
        finally:
            self.running = False
            if self.heartbeat_task:
                self.heartbeat_task.cancel()
            if self.monitoring_task:
                self.monitoring_task.cancel()

    async def stop(self):
        """Stop the WebSocket server."""
        if not self.running:
            return

        logger.info("🛑 Stopping AI Context WebSocket Server")
        self.running = False

        if self.server:
            self.server.close()
            await self.server.wait_closed()

    async def _heartbeat(self):
        """Send periodic heartbeat to all connected clients."""
        while self.running:
            try:
                heartbeat_data = {
                    "type": "heartbeat",
                    "timestamp": time.time(),
                    "server_status": "active",
                    "active_connections": sum(len(conns) for conns in self.active_connections.values())
                }

                # Send heartbeat to all connections
                for endpoint, connections in self.active_connections.items():
                    dead_connections = set()
                    for conn in connections:
                        try:
                            await conn.send(json.dumps(heartbeat_data))
                        except (ConnectionClosedError, WebSocketException):
                            dead_connections.add(conn)

                    # Remove dead connections
                    connections -= dead_connections

                await asyncio.sleep(30)  # Heartbeat every 30 seconds

            except Exception as e:
                logger.error(f"Heartbeat error: {e}")
                await asyncio.sleep(30)

    async def _performance_monitor(self):
        """Monitor and log performance statistics."""
        while self.running:
            try:
                # Update connection counts
                total_connections = sum(len(conns) for conns in self.active_connections.values())
                self.performance_stats["active_connections"] = total_connections

                logger.info(f"📊 AI Context WS Performance: {self.performance_stats}")
                await asyncio.sleep(300)  # Log every 5 minutes

            except Exception as e:
                logger.error(f"Performance monitoring error: {e}")
                await asyncio.sleep(60)

    async def broadcast_to_session(self, session_id: str, message: Dict[str, Any]):
        """Broadcast a message to all clients connected to a specific session."""
        if session_id not in self.session_connections:
            return

        connections = self.session_connections[session_id]
        dead_connections = set()

        for conn in connections:
            try:
                await conn.send(json.dumps(message))
                self.performance_stats["messages_processed"] += 1
            except (ConnectionClosedError, WebSocketException):
                dead_connections.add(conn)

        # Remove dead connections
        connections -= dead_connections

    async def broadcast_to_endpoint(self, endpoint: str, message: Dict[str, Any]):
        """Broadcast a message to all clients connected to an endpoint."""
        if endpoint not in self.active_connections:
            return

        connections = self.active_connections[endpoint]
        dead_connections = set()

        for conn in connections:
            try:
                await conn.send(json.dumps(message))
                self.performance_stats["messages_processed"] += 1
            except (ConnectionClosedError, WebSocketException):
                dead_connections.add(conn)

        # Remove dead connections
        connections -= dead_connections

    async def _handle_connection(self, websocket: websockets.WebSocketServerProtocol, path: str):
        """Route connections based on path."""
        if path == "/ws/ai/context":
            await self._handle_context_connection(websocket, path)
        elif path == "/ws/ai/suggestions":
            await self._handle_suggestions_connection(websocket, path)
        elif path == "/ws/ai/collaboration":
            await self._handle_collaboration_connection(websocket, path)
        else:
            logger.warning(f"Unknown WebSocket path: {path}")
            await websocket.close(code=1003, reason="Unknown endpoint")

    async def _handle_context_connection(self, websocket: websockets.WebSocketServerProtocol, path: str):
        """Handle connections to /ws/ai/context endpoint."""
        logger.info(f"🧠 New context connection from {websocket.remote_address}")
        self.active_connections["context"].add(websocket)
        self.performance_stats["total_connections"] += 1

        try:
            # Send welcome message
            welcome_data = {
                "type": "welcome",
                "endpoint": "context",
                "message": "Connected to AI Context processing stream",
                "features": ["real_time_context", "ai_suggestions", "risk_integration"],
                "update_frequency": "dynamic"
            }
            await websocket.send(json.dumps(welcome_data))

            # Handle client messages
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self._handle_context_message(websocket, data)
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON received from context client {websocket.remote_address}")

        except (ConnectionClosedError, WebSocketException):
            logger.info(f"Context connection closed for {websocket.remote_address}")
        finally:
            self.active_connections["context"].discard(websocket)

    async def _handle_suggestions_connection(self, websocket: websockets.WebSocketServerProtocol, path: str):
        """Handle connections to /ws/ai/suggestions endpoint."""
        logger.info(f"💡 New suggestions connection from {websocket.remote_address}")
        self.active_connections["suggestions"].add(websocket)
        self.performance_stats["total_connections"] += 1

        try:
            welcome_data = {
                "type": "welcome",
                "endpoint": "suggestions",
                "message": "Connected to AI Suggestions stream",
                "features": ["real_time_suggestions", "confidence_scores", "action_tracking"]
            }
            await websocket.send(json.dumps(welcome_data))

            # Handle client messages
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self._handle_suggestions_message(websocket, data)
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON received from suggestions client {websocket.remote_address}")

        except (ConnectionClosedError, WebSocketException):
            logger.info(f"Suggestions connection closed for {websocket.remote_address}")
        finally:
            self.active_connections["suggestions"].discard(websocket)

    async def _handle_collaboration_connection(self, websocket: websockets.WebSocketServerProtocol, path: str):
        """Handle connections to /ws/ai/collaboration endpoint."""
        logger.info(f"🤝 New collaboration connection from {websocket.remote_address}")
        self.active_connections["collaboration"].add(websocket)
        self.performance_stats["total_connections"] += 1

        try:
            welcome_data = {
                "type": "welcome",
                "endpoint": "collaboration",
                "message": "Connected to Collaborative Context stream",
                "features": ["shared_context", "collaborative_suggestions", "activity_sync"]
            }
            await websocket.send(json.dumps(welcome_data))

            # Handle client messages
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self._handle_collaboration_message(websocket, data)
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON received from collaboration client {websocket.remote_address}")

        except (ConnectionClosedError, WebSocketException):
            logger.info(f"Collaboration connection closed for {websocket.remote_address}")
        finally:
            self.active_connections["collaboration"].discard(websocket)

    async def _handle_context_message(self, websocket: websockets.WebSocketServerProtocol, data: Dict[str, Any]):
        """Handle messages from context clients."""
        message_type = data.get("type")

        if message_type == "ping":
            await websocket.send(json.dumps({"type": "pong", "timestamp": time.time()}))
        elif message_type == "subscribe_session":
            session_id = data.get("session_id")
            if session_id:
                if session_id not in self.session_connections:
                    self.session_connections[session_id] = set()
                self.session_connections[session_id].add(websocket)
                await websocket.send(json.dumps({
                    "type": "subscription_confirmed",
                    "session_id": session_id,
                    "timestamp": time.time()
                }))
        elif message_type == "update_context":
            session_id = data.get("session_id")
            context_updates = data.get("context_updates", {})

            if session_id:
                start_time = time.time()
                try:
                    result = await ai_context_engine.update_session_context(
                        session_id=session_id,
                        context_updates=context_updates
                    )

                    # Update performance stats
                    processing_time = time.time() - start_time
                    self.performance_stats["context_updates"] += 1
                    self.performance_stats["avg_response_time"] = (
                        (self.performance_stats["avg_response_time"] * 0.9) + (processing_time * 0.1)
                    )

                    # Send results to session subscribers
                    update_message = {
                        "type": "context_updated",
                        "session_id": session_id,
                        "result": result,
                        "processing_time": processing_time,
                        "timestamp": time.time()
                    }
                    await self.broadcast_to_session(session_id, update_message)

                except Exception as e:
                    logger.error(f"Context update error: {e}")
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": str(e),
                        "timestamp": time.time()
                    }))

    async def _handle_suggestions_message(self, websocket: websockets.WebSocketServerProtocol, data: Dict[str, Any]):
        """Handle messages from suggestions clients."""
        message_type = data.get("type")

        if message_type == "ping":
            await websocket.send(json.dumps({"type": "pong", "timestamp": time.time()}))
        elif message_type == "apply_suggestion":
            session_id = data.get("session_id")
            suggestion_id = data.get("suggestion_id")

            if session_id and suggestion_id:
                try:
                    applied = await ai_context_engine.apply_suggestion(session_id, suggestion_id)

                    if applied:
                        self.performance_stats["suggestions_delivered"] += 1
                        await websocket.send(json.dumps({
                            "type": "suggestion_applied",
                            "session_id": session_id,
                            "suggestion_id": suggestion_id,
                            "timestamp": time.time()
                        }))

                        # Broadcast to session
                        await self.broadcast_to_session(session_id, {
                            "type": "suggestion_applied_broadcast",
                            "suggestion_id": suggestion_id,
                            "applied_by": getattr(websocket, 'remote_address', 'client'),
                            "timestamp": time.time()
                        })
                    else:
                        await websocket.send(json.dumps({
                            "type": "error",
                            "message": "Suggestion not found",
                            "timestamp": time.time()
                        }))

                except Exception as e:
                    logger.error(f"Suggestion application error: {e}")
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": str(e),
                        "timestamp": time.time()
                    }))

    async def _handle_collaboration_message(self, websocket: websockets.WebSocketServerProtocol, data: Dict[str, Any]):
        """Handle messages from collaboration clients."""
        message_type = data.get("type")

        if message_type == "ping":
            await websocket.send(json.dumps({"type": "pong", "timestamp": time.time()}))
        elif message_type == "share_context":
            session_id = data.get("session_id")
            shared_context = data.get("context", {})

            if session_id:
                # Broadcast shared context to all collaboration clients
                collaboration_update = {
                    "type": "shared_context_update",
                    "session_id": session_id,
                    "shared_context": shared_context,
                    "shared_by": getattr(websocket, 'remote_address', 'client'),
                    "timestamp": time.time()
                }

                await self.broadcast_to_endpoint("collaboration", collaboration_update)
        elif message_type == "join_collaboration":
            session_id = data.get("session_id")
            user_info = data.get("user_info", {})

            if session_id:
                # Add to session connections
                if session_id not in self.session_connections:
                    self.session_connections[session_id] = set()
                self.session_connections[session_id].add(websocket)

                # Notify others of new collaborator
                join_notification = {
                    "type": "collaborator_joined",
                    "session_id": session_id,
                    "user_info": user_info,
                    "timestamp": time.time()
                }

                await self.broadcast_to_session(session_id, join_notification)

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get current performance statistics."""
        return {
            **self.performance_stats,
            "connection_breakdown": {
                endpoint: len(connections)
                for endpoint, connections in self.active_connections.items()
            },
            "active_sessions": len(self.session_connections)
        }


# Global instance
ai_context_websocket_server = AIContextWebSocketServer()

# Example usage
async def main():
    """Example usage of the AI Context WebSocket Server."""
    server = AIContextWebSocketServer()
    try:
        await server.start()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        await server.stop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())