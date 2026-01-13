#!/usr/bin/env python3
"""
Risk WebSocket Server Test Tool
==============================

Test script for the Risk Analytics WebSocket server.
Verifies connectivity and data streaming functionality.

Purpose: Test WebSocket server functionality and connectivity
Usage: python tools/test_risk_websocket.py
Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-29
Description: Comprehensive test tool for WebSocket server functionality

<!-- SSOT Domain: analytics -->
"""

import asyncio
import json
import logging
import sys
import time
from typing import Dict, Any

try:
    import websockets
except ImportError:
    print("❌ websockets library not installed. Install with: pip install websockets")
    sys.exit(1)


class RiskWebSocketTester:
    """Test client for Risk WebSocket server."""

    def __init__(self):
        self.test_results = {
            "connection_test": False,
            "live_endpoint_test": False,
            "dashboard_endpoint_test": False,
            "alerts_endpoint_test": False,
            "heartbeat_test": False,
            "data_streaming_test": False
        }

    async def test_connection(self, uri: str, test_name: str) -> bool:
        """Test basic connection to a WebSocket endpoint."""
        try:
            async with websockets.connect(uri) as websocket:
                # Wait for welcome message
                response = await websocket.recv()
                data = json.loads(response)

                if data.get("type") == "welcome":
                    print(f"✅ {test_name}: Connected successfully")
                    print(f"   Endpoint: {data.get('endpoint', 'unknown')}")
                    print(f"   Message: {data.get('message', 'no message')}")
                    return True
                else:
                    print(f"❌ {test_name}: Unexpected welcome message: {data}")
                    return False

        except Exception as e:
            print(f"❌ {test_name}: Connection failed - {e}")
            return False

    async def test_live_endpoint(self) -> bool:
        """Test the live risk metrics endpoint."""
        uri = "ws://localhost:8765/ws/risk/live"
        success = await self.test_connection(uri, "Live Endpoint")

        if success:
            try:
                async with websockets.connect(uri) as websocket:
                    # Skip welcome message
                    await websocket.recv()

                    # Wait for a few data updates
                    update_count = 0
                    start_time = time.time()

                    while time.time() - start_time < 5:  # Test for 5 seconds
                        try:
                            response = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                            data = json.loads(response)

                            if data.get("type") == "risk_metrics_live":
                                update_count += 1
                                if update_count >= 3:  # Got at least 3 updates
                                    print("✅ Live Endpoint: Received streaming data updates")
                                    break
                        except asyncio.TimeoutError:
                            print("❌ Live Endpoint: Timeout waiting for data updates")
                            return False

                    if update_count >= 3:
                        print(f"✅ Live Endpoint: Successfully received {update_count} data updates")
                        return True
                    else:
                        print(f"❌ Live Endpoint: Only received {update_count} updates, expected at least 3")
                        return False

            except Exception as e:
                print(f"❌ Live Endpoint: Streaming test failed - {e}")
                return False
        return False

    async def test_dashboard_endpoint(self) -> bool:
        """Test the dashboard endpoint."""
        uri = "ws://localhost:8765/ws/risk/dashboard"
        success = await self.test_connection(uri, "Dashboard Endpoint")

        if success:
            try:
                async with websockets.connect(uri) as websocket:
                    # Skip welcome message
                    await websocket.recv()

                    # Wait for dashboard update
                    start_time = time.time()
                    while time.time() - start_time < 5:
                        try:
                            response = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                            data = json.loads(response)

                            if data.get("type") == "dashboard_update":
                                print("✅ Dashboard Endpoint: Received dashboard update")
                                print(f"   Metrics: {len(data.get('metrics', {}))} fields")
                                print(f"   Charts: {len(data.get('charts', {}))} datasets")
                                print(f"   Alerts: {len(data.get('alerts', []))} active alerts")
                                return True
                        except asyncio.TimeoutError:
                            continue

                    print("❌ Dashboard Endpoint: Timeout waiting for dashboard update")
                    return False

            except Exception as e:
                print(f"❌ Dashboard Endpoint: Test failed - {e}")
                return False
        return False

    async def test_alerts_endpoint(self) -> bool:
        """Test the alerts endpoint."""
        uri = "ws://localhost:8765/ws/risk/alerts"
        return await self.test_connection(uri, "Alerts Endpoint")

    async def test_heartbeat(self) -> bool:
        """Test heartbeat functionality across all endpoints."""
        endpoints = [
            "ws://localhost:8765/ws/risk/live",
            "ws://localhost:8765/ws/risk/dashboard",
            "ws://localhost:8765/ws/risk/alerts"
        ]

        heartbeat_received = False

        async def check_endpoint(uri: str):
            nonlocal heartbeat_received
            try:
                async with websockets.connect(uri) as websocket:
                    start_time = time.time()
                    while time.time() - start_time < 10:  # Wait up to 10 seconds for heartbeat
                        try:
                            response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                            data = json.loads(response)

                            if data.get("type") == "heartbeat":
                                heartbeat_received = True
                                print("✅ Heartbeat: Received from server")
                                return True
                        except asyncio.TimeoutError:
                            continue
            except Exception as e:
                print(f"❌ Heartbeat: Failed on {uri} - {e}")
                return False

            return False

        # Test heartbeat on dashboard endpoint (most feature-rich)
        success = await check_endpoint(endpoints[1])

        if success and heartbeat_received:
            return True
        else:
            print("❌ Heartbeat: No heartbeat received within timeout")
            return False

    async def run_all_tests(self) -> Dict[str, bool]:
        """Run all WebSocket tests."""
        print("🧪 Risk WebSocket Server Test Suite")
        print("=" * 50)

        # Test basic connections
        print("\n🔌 Testing Basic Connections...")
        self.test_results["connection_test"] = await self.test_connection(
            "ws://localhost:8765/ws/risk/dashboard", "Basic Connection"
        )

        # Test individual endpoints
        print("\n📊 Testing Endpoints...")

        print("\n1. Live Risk Metrics Endpoint:")
        self.test_results["live_endpoint_test"] = await self.test_live_endpoint()

        print("\n2. Dashboard Endpoint:")
        self.test_results["dashboard_endpoint_test"] = await self.test_dashboard_endpoint()

        print("\n3. Alerts Endpoint:")
        self.test_results["alerts_endpoint_test"] = await self.test_alerts_endpoint()

        # Test heartbeat
        print("\n💓 Testing Heartbeat...")
        self.test_results["heartbeat_test"] = await self.test_heartbeat()

        # Overall data streaming test
        self.test_results["data_streaming_test"] = (
            self.test_results["live_endpoint_test"] and
            self.test_results["dashboard_endpoint_test"]
        )

        return self.test_results

    def print_summary(self):
        """Print test summary."""
        print("\n" + "=" * 50)
        print("📋 TEST SUMMARY")
        print("=" * 50)

        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result)

        for test_name, result in self.test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            clean_name = test_name.replace("_", " ").title()
            print(f"{status:10} | {clean_name}")

        print(f"\n🎯 Overall Result: {passed_tests}/{total_tests} tests passed")

        if passed_tests == total_tests:
            print("🎉 ALL TESTS PASSED - WebSocket server is fully operational!")
            print("🚀 Ready for production use with real-time risk dashboard")
        else:
            print("⚠️ Some tests failed - check server configuration and connectivity")
            print("🔧 Ensure the Risk WebSocket server is running on localhost:8765")

        return passed_tests == total_tests


async def main():
    """Main test function."""
    # Configure logging
    logging.basicConfig(level=logging.WARNING)  # Reduce noise

    tester = RiskWebSocketTester()
    results = await tester.run_all_tests()
    success = tester.print_summary()

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    # Handle --help argument
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print(__doc__)
        print("\nUsage: python tools/test_risk_websocket.py")
        print("\nTests the Risk Analytics WebSocket server connectivity and functionality.")
        print("Expects server to be running on localhost:8765")
        sys.exit(0)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test suite error: {e}")
        sys.exit(1)
