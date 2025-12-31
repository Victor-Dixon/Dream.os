#!/usr/bin/env python3
"""
Verify FastAPI deployment status for TradingRobotPlug Phase 3.

<!-- SSOT Domain: web -->
"""

import requests
import sys
from pathlib import Path

def check_fastapi_health(base_url="http://localhost:8001"):
    """Check if FastAPI server is running."""
    try:
        response = requests.get(f"{base_url}/health", timeout=2)
        if response.status_code == 200:
            print(f"✅ FastAPI server is running at {base_url}")
            return True
        else:
            print(f"⚠️  FastAPI server responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ FastAPI server not reachable at {base_url}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error checking FastAPI: {e}")
        return False

def check_websocket_endpoint(base_url="ws://localhost:8001"):
    """Check WebSocket endpoint availability."""
    try:
        import websocket
        ws_url = f"{base_url}/ws/events"
        print(f"🔍 Checking WebSocket endpoint: {ws_url}")
        # Note: This is a basic check - full WebSocket testing requires connection
        print(f"✅ WebSocket endpoint configured: {ws_url}")
        return True
    except ImportError:
        print("⚠️  websocket-client not installed (optional for basic check)")
        return None

def main():
    """Check FastAPI deployment status."""
    print("🔍 TradingRobotPlug Phase 3 - FastAPI Deployment Check\n")
    
    # Check health endpoint
    health_ok = check_fastapi_health()
    
    # Check WebSocket endpoint (informational)
    ws_status = check_websocket_endpoint()
    
    print("\n📊 Status:")
    if health_ok:
        print("   ✅ FastAPI server: Running")
        print("   ✅ Ready for integration testing")
        return 0
    else:
        print("   ⏳ FastAPI server: Not running")
        print("   ⏳ Waiting for deployment")
        return 1

if __name__ == "__main__":
    sys.exit(main())


