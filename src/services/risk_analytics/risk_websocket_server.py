#!/usr/bin/env python3
"""
Risk Analytics WebSocket Server
==============================

Real-time WebSocket server for streaming risk metrics to dashboard clients.
Provides live VaR, CVaR, Sharpe Ratio, and other risk analytics data.

Purpose: Real-time risk metrics streaming infrastructure for live dashboard
Usage: Run as standalone server or integrate into risk analytics platform
Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-29
Description: WebSocket server providing 1Hz live risk metrics updates with <100ms latency

<!-- SSOT Domain: analytics -->

Navigation References:
├── Related Files:
│   ├── Risk Calculator → src/services/risk_analytics/risk_calculator_service.py
│   ├── API Endpoints → src/services/risk_analytics/risk_api_endpoints.py
│   ├── Risk Integration → src/web/static/js/trading-robot/risk-dashboard-integration.js
│   ├── Trading Dashboard → src/web/static/js/trading-robot/trading-dashboard.js
│   ├── Dashboard UI → docs/analytics/risk_dashboard.html
│   └── Database Schema → database/migrations/phase2_2_risk_analytics_schema.sql
├── Documentation:
│   ├── Architecture → docs/analytics/TRADINGROBOTPLUG_ANALYTICS_ARCHITECTURE.md
│   ├── Integration Demo → docs/analytics/trading_robot_risk_integration_demo.html
│   ├── WebSocket Architecture → docs/analytics/AGENT2_WEBSOCKET_ARCHITECTURE_REVIEW.md
│   └── Testing → tools/test_risk_websocket.py
└── Usage:
    └── Start Server → python src/services/risk_analytics/risk_websocket_server.py

Bidirectional Links:
├── From Code to Docs:
│   ├── This server → docs/analytics/TRADINGROBOTPLUG_ANALYTICS_ARCHITECTURE.md
│   ├── This server → docs/analytics/risk_dashboard.html
│   ├── This server → docs/analytics/trading_robot_risk_integration_demo.html
│   └── This server → docs/analytics/AGENT2_WEBSOCKET_ARCHITECTURE_REVIEW.md
└── From Docs to Code:
    ├── docs/analytics/TRADINGROBOTPLUG_ANALYTICS_ARCHITECTURE.md → This server
    ├── docs/analytics/risk_dashboard.html → This server
    ├── docs/analytics/trading_robot_risk_integration_demo.html → This server
    └── docs/analytics/AGENT2_WEBSOCKET_ARCHITECTURE_REVIEW.md → This server

Endpoints:
- /ws/risk/live - Live risk metrics streaming
- /ws/risk/dashboard - Dashboard-specific data
- /ws/risk/alerts - Real-time risk alerts

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-29
Phase: Phase 2.2 Week 2 - Real-time Risk Dashboard
"""

import asyncio
import json
import logging
import threading
import time
from typing import Dict, List, Optional, Any, Set
import websockets
from websockets.exceptions import ConnectionClosedError, WebSocketException

from src.services.risk_analytics.risk_calculator_service import RiskCalculatorService, RiskMetrics

logger = logging.getLogger(__name__)


class RiskWebSocketServer:
    """
    WebSocket server for real-time risk analytics streaming.

    Features:
    - Live risk metrics streaming (VaR, CVaR, Sharpe Ratio, etc.)
    - Dashboard-specific data feeds
    - Real-time risk alerts
    - Connection management with heartbeat
    - Performance optimized for <100ms latency
    """

    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.server = None
        self.active_connections: Dict[str, Set[websockets.WebSocketServerProtocol]] = {
            "live": set(),
            "dashboard": set(),
            "alerts": set()
        }
        self.risk_calculator = RiskCalculatorService()
        self.running = False
        self.heartbeat_interval = 30  # seconds
        self.update_interval = 1.0  # seconds (1Hz updates for real-time feel)

    async def _heartbeat(self):
        """Send periodic heartbeat to all connected clients."""
        while self.running:
            try:
                heartbeat_data = {
                    "type": "heartbeat",
                    "timestamp": time.time(),
                    "server_status": "active"
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

                await asyncio.sleep(self.heartbeat_interval)

            except Exception as e:
                logger.error(f"Heartbeat error: {e}")
                await asyncio.sleep(self.heartbeat_interval)

    async def _stream_risk_updates(self):
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
        """
        Stream live risk metric updates to connected clients.

        Navigation References:
        ├── Risk Calculator → src/services/risk_analytics/risk_calculator_service.py::calculate_comprehensive_risk_metrics()
        ├── Dashboard Integration → src/web/static/js/trading-robot/risk-dashboard-integration.js::handleMessage()
        ├── Real-time Charts → src/web/static/js/trading-robot/risk-charts.js
        ├── Performance Monitoring → docs/analytics/AGENT2_WEBSOCKET_ARCHITECTURE_REVIEW.md#performance-metrics
        ├── Connection Management → WebSocket heartbeat system (see _heartbeat())
        └── Load Testing → tools/test_risk_websocket.py

        Critical real-time pipeline:
        1. Generate live risk data (1Hz updates)
        2. Stream to /ws/risk/live endpoint subscribers
        3. Generate enhanced dashboard data with charts
        4. Stream to /ws/risk/dashboard endpoint subscribers
        5. Handle connection cleanup and error recovery
        """
<<<<<<< HEAD
=======
        """Stream live risk metric updates to connected clients."""
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
        while self.running:
            try:
                # Generate mock real-time risk data (in production, this would come from live trading data)
                risk_data = await self._generate_live_risk_data()

                # Send to live endpoint subscribers
                live_connections = self.active_connections["live"]
                dead_connections = set()

                for conn in live_connections:
                    try:
                        await conn.send(json.dumps(risk_data))
                    except (ConnectionClosedError, WebSocketException):
                        dead_connections.add(conn)

                # Remove dead connections
                live_connections -= dead_connections

                # Send dashboard-specific data
                dashboard_data = await self._generate_dashboard_data()
                dashboard_connections = self.active_connections["dashboard"]
                dead_connections = set()

                for conn in dashboard_connections:
                    try:
                        await conn.send(json.dumps(dashboard_data))
                    except (ConnectionClosedError, WebSocketException):
                        dead_connections.add(conn)

                dashboard_connections -= dead_connections

                await asyncio.sleep(self.update_interval)

            except Exception as e:
                logger.error(f"Risk update streaming error: {e}")
                await asyncio.sleep(self.update_interval)

    async def _generate_live_risk_data(self) -> Dict[str, Any]:
        """Generate live risk metrics data for streaming."""
        # In production, this would calculate from real trading data
        # For now, we'll simulate realistic risk data
        import random
        import numpy as np

        # Simulate realistic risk metrics that would fluctuate in real trading
        base_var = 0.15  # 15% VaR (conservative)
        base_cvar = 0.22  # 22% CVaR
        base_sharpe = 1.8  # Good Sharpe ratio

        # Add some realistic volatility
        var_noise = random.gauss(0, 0.02)
        cvar_noise = random.gauss(0, 0.03)
        sharpe_noise = random.gauss(0, 0.1)

        return {
            "type": "risk_metrics_live",
            "timestamp": time.time(),
            "portfolio_id": "TRADINGROBOTPLUG_PORTFOLIO",
            "metrics": {
                "var_95": max(0.05, base_var + var_noise),  # Min 5%
                "cvar_95": max(0.08, base_cvar + cvar_noise),  # Min 8%
                "sharpe_ratio": max(0.5, base_sharpe + sharpe_noise),  # Min 0.5
                "max_drawdown": random.uniform(0.02, 0.08),  # 2-8% drawdown
                "sortino_ratio": random.uniform(1.2, 2.5),
                "information_ratio": random.uniform(0.8, 1.8)
            },
            "status": "live_update",
            "update_frequency": "1Hz"
        }

    async def _generate_dashboard_data(self) -> Dict[str, Any]:
        """Generate dashboard-specific data with additional context."""
        # Enhanced data for dashboard visualization
        live_data = await self._generate_live_risk_data()

        # Add dashboard-specific fields
        dashboard_data = {
            **live_data,
            "type": "dashboard_update",
            "charts": {
                "var_history": [0.12, 0.15, 0.13, 0.18, 0.14, live_data["metrics"]["var_95"]],
                "sharpe_trend": [1.6, 1.7, 1.8, 1.9, 1.7, live_data["metrics"]["sharpe_ratio"]],
                "drawdown_series": [0.03, 0.05, 0.04, 0.06, 0.05, live_data["metrics"]["max_drawdown"]]
            },
            "alerts": await self._check_risk_alerts(live_data["metrics"]),
            "performance_indicators": {
                "risk_adjusted_return": live_data["metrics"]["sharpe_ratio"] * 0.1,  # Rough estimate
                "volatility_adjusted": 1 / (1 + live_data["metrics"]["var_95"]),  # Lower VaR = higher score
                "efficiency_ratio": live_data["metrics"]["information_ratio"] / live_data["metrics"]["var_95"]
            }
        }

        return dashboard_data

    async def _check_risk_alerts(self, metrics: Dict[str, float]) -> List[Dict[str, Any]]:
        """Check for risk alerts based on current metrics."""
        alerts = []

        # VaR threshold alerts
        if metrics["var_95"] > 0.20:  # 20% VaR threshold
            alerts.append({
                "level": "high",
                "message": f"High VaR Alert: {metrics['var_95']:.1%} exceeds 20% threshold",
                "metric": "var_95",
                "value": metrics["var_95"],
                "threshold": 0.20
            })

        # Sharpe ratio alerts
        if metrics["sharpe_ratio"] < 1.0:  # Below 1.0 is concerning
            alerts.append({
                "level": "medium",
                "message": f"Low Sharpe Ratio: {metrics['sharpe_ratio']:.2f} below 1.0 minimum",
                "metric": "sharpe_ratio",
                "value": metrics["sharpe_ratio"],
                "threshold": 1.0
            })

        # Drawdown alerts
        if metrics["max_drawdown"] > 0.10:  # 10% drawdown threshold
            alerts.append({
                "level": "critical",
                "message": f"Critical Drawdown: {metrics['max_drawdown']:.1%} exceeds 10% threshold",
                "metric": "max_drawdown",
                "value": metrics["max_drawdown"],
                "threshold": 0.10
            })

        return alerts

    async def _handle_live_connection(self, websocket: websockets.WebSocketServerProtocol, path: str):
        """Handle connections to /ws/risk/live endpoint."""
        logger.info(f"New live connection from {websocket.remote_address}")
        self.active_connections["live"].add(websocket)

        try:
            # Send welcome message
            welcome_data = {
                "type": "welcome",
                "endpoint": "live",
                "message": "Connected to live risk metrics stream",
                "update_frequency": "1Hz"
            }
            await websocket.send(json.dumps(welcome_data))

            # Keep connection alive and handle client messages
            async for message in websocket:
                try:
                    data = json.loads(message)
                    # Handle client requests (e.g., parameter changes, filters)
                    if data.get("type") == "ping":
                        await websocket.send(json.dumps({"type": "pong", "timestamp": time.time()}))
                    elif data.get("type") == "subscribe":
                        # Handle subscription requests
                        await websocket.send(json.dumps({
                            "type": "subscription_confirmed",
                            "endpoint": "live",
                            "timestamp": time.time()
                        }))
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON received from {websocket.remote_address}")

        except (ConnectionClosedError, WebSocketException):
            logger.info(f"Live connection closed for {websocket.remote_address}")
        finally:
            self.active_connections["live"].discard(websocket)

    async def _handle_dashboard_connection(self, websocket: websockets.WebSocketServerProtocol, path: str):
        """Handle connections to /ws/risk/dashboard endpoint."""
        logger.info(f"New dashboard connection from {websocket.remote_address}")
        self.active_connections["dashboard"].add(websocket)

        try:
            # Send welcome message with dashboard configuration
            welcome_data = {
                "type": "welcome",
                "endpoint": "dashboard",
                "message": "Connected to risk dashboard stream",
                "features": ["charts", "alerts", "performance_indicators"],
                "update_frequency": "1Hz"
            }
            await websocket.send(json.dumps(welcome_data))

            # Keep connection alive
            async for message in websocket:
                try:
                    data = json.loads(message)
                    if data.get("type") == "ping":
                        await websocket.send(json.dumps({"type": "pong", "timestamp": time.time()}))
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON received from dashboard client {websocket.remote_address}")

        except (ConnectionClosedError, WebSocketException):
            logger.info(f"Dashboard connection closed for {websocket.remote_address}")
        finally:
            self.active_connections["dashboard"].discard(websocket)

    async def _handle_alerts_connection(self, websocket: websockets.WebSocketServerProtocol, path: str):
        """Handle connections to /ws/risk/alerts endpoint."""
        logger.info(f"New alerts connection from {websocket.remote_address}")
        self.active_connections["alerts"].add(websocket)

        try:
            welcome_data = {
                "type": "welcome",
                "endpoint": "alerts",
                "message": "Connected to risk alerts stream",
                "alert_levels": ["low", "medium", "high", "critical"]
            }
            await websocket.send(json.dumps(welcome_data))

            # Keep connection alive
            async for message in websocket:
                try:
                    data = json.loads(message)
                    if data.get("type") == "ping":
                        await websocket.send(json.dumps({"type": "pong", "timestamp": time.time()}))
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON received from alerts client {websocket.remote_address}")

        except (ConnectionClosedError, WebSocketException):
            logger.info(f"Alerts connection closed for {websocket.remote_address}")
        finally:
            self.active_connections["alerts"].discard(websocket)

    async def _handle_connection(self, websocket: websockets.WebSocketServerProtocol, path: str):
        """Route connections based on path."""
        if path == "/ws/risk/live":
            await self._handle_live_connection(websocket, path)
        elif path == "/ws/risk/dashboard":
            await self._handle_dashboard_connection(websocket, path)
        elif path == "/ws/risk/alerts":
            await self._handle_alerts_connection(websocket, path)
        else:
            logger.warning(f"Unknown WebSocket path: {path}")
            await websocket.close(code=1003, reason="Unknown endpoint")

    async def start(self):
        """Start the WebSocket server."""
        if self.running:
            logger.warning("Server is already running")
            return

        self.running = True
        logger.info(f"Starting Risk WebSocket Server on {self.host}:{self.port}")

        # Start background tasks
        heartbeat_task = asyncio.create_task(self._heartbeat())
        stream_task = asyncio.create_task(self._stream_risk_updates())

        try:
            # Start WebSocket server
            self.server = await websockets.serve(
                self._handle_connection,
                self.host,
                self.port,
                ping_interval=20,  # Send ping every 20 seconds
                ping_timeout=10,   # Wait 10 seconds for pong
                max_size=1_048_576,  # 1MB max message size
                compression=None    # Disable compression for real-time performance
            )

            logger.info("Risk WebSocket Server started successfully")
            logger.info("Available endpoints:")
            logger.info("  - ws://localhost:8765/ws/risk/live")
            logger.info("  - ws://localhost:8765/ws/risk/dashboard")
            logger.info("  - ws://localhost:8765/ws/risk/alerts")

            # Keep server running
            await self.server.wait_closed()

        except Exception as e:
            logger.error(f"Failed to start WebSocket server: {e}")
            raise
        finally:
            self.running = False
            heartbeat_task.cancel()
            stream_task.cancel()

            # Close all connections
            for endpoint, connections in self.active_connections.items():
                for conn in connections:
                    try:
                        await conn.close()
                    except:
                        pass
                connections.clear()

    async def stop(self):
        """Stop the WebSocket server."""
        if not self.running:
            return

        logger.info("Stopping Risk WebSocket Server")
        self.running = False

        if self.server:
            self.server.close()
            await self.server.wait_closed()

    def start_in_thread(self):
        """Start the server in a background thread."""
        def run_server():
            asyncio.run(self.start())

        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()
        logger.info("Risk WebSocket Server started in background thread")
        return thread


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Start server
    server = RiskWebSocketServer()
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        asyncio.run(server.stop())
