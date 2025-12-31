#!/usr/bin/env python3
"""
TradingRobotPlug Phase 3 Integration Test Helper
Validates WordPress REST API endpoints and WebSocket connectivity.

<!-- SSOT Domain: web -->
"""

import requests
import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

def test_rest_api_endpoints(base_url="http://localhost:8000"):
    """Test WordPress REST API endpoints."""
    endpoints = [
        "/wp-json/tradingrobotplug/v1/stock-data",
        "/wp-json/tradingrobotplug/v1/strategies",
        "/wp-json/tradingrobotplug/v1/performance",
        "/wp-json/tradingrobotplug/v1/trades",
        "/wp-json/tradingrobotplug/v1/backtest",
        "/wp-json/tradingrobotplug/v1/analytics"
    ]
    
    results = {}
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        try:
            response = requests.get(url, timeout=5)
            results[endpoint] = {
                "status": response.status_code,
                "ok": response.ok,
                "content_type": response.headers.get("Content-Type", ""),
                "has_data": len(response.content) > 0
            }
            print(f"✅ {endpoint}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            results[endpoint] = {
                "status": "error",
                "error": str(e)
            }
            print(f"❌ {endpoint}: {e}")
    
    return results

def test_websocket_url_config():
    """Verify WebSocket URL configuration in dashboard.js."""
    # Try multiple possible paths
    possible_paths = [
        Path("websites/websites/tradingrobotplug.com/wp/wp-content/themes/tradingrobotplug-theme/assets/js/dashboard.js"),
        Path("websites/tradingrobotplug.com/wp/wp-content/themes/tradingrobotplug-theme/assets/js/dashboard.js"),
        Path("D:/websites/websites/tradingrobotplug.com/wp/wp-content/themes/tradingrobotplug-theme/assets/js/dashboard.js"),
    ]
    
    dashboard_path = None
    for path in possible_paths:
        if path.exists():
            dashboard_path = path
            break
    
    if not dashboard_path.exists():
        print(f"❌ Dashboard.js not found: {dashboard_path}")
        return False
    
    content = dashboard_path.read_text()
    
    required_features = [
        "getWebSocketUrl",
        "initWebSocket",
        "handleWebSocketMessage",
        "subscribeToEvents",
        "startHeartbeat",
        "fallbackToPolling"
    ]
    
    missing = [feature for feature in required_features if feature not in content]
    
    if missing:
        print(f"❌ Missing WebSocket features: {missing}")
        return False
    
    # Check for FastAPI WebSocket endpoint reference
    if "/ws/events" in content or "ws://" in content or "wss://" in content:
        print("✅ WebSocket URL configuration found")
        return True
    else:
        print("⚠️  WebSocket URL configuration may be missing")
        return False

def main():
    """Run integration validation tests."""
    print("🔍 TradingRobotPlug Phase 3 Integration Validation\n")
    
    print("1. Testing WebSocket client configuration...")
    ws_ok = test_websocket_url_config()
    
    print("\n2. Testing REST API endpoints...")
    print("   (Note: Requires WordPress site running)")
    api_results = test_rest_api_endpoints()
    
    print("\n📊 Summary:")
    print(f"   WebSocket client: {'✅ Ready' if ws_ok else '❌ Issues found'}")
    
    successful_endpoints = sum(1 for r in api_results.values() if r.get("ok", False))
    total_endpoints = len(api_results)
    print(f"   REST API endpoints: {successful_endpoints}/{total_endpoints} responding")
    
    if ws_ok and successful_endpoints == total_endpoints:
        print("\n✅ Integration validation complete - Ready for joint testing")
        return 0
    else:
        print("\n⚠️  Some validation checks failed - Review required")
        return 1

if __name__ == "__main__":
    sys.exit(main())

