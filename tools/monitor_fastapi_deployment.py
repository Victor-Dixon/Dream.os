#!/usr/bin/env python3
"""
Monitor FastAPI deployment and verify endpoints when service becomes available.

<!-- SSOT Domain: web -->
"""

import requests
import time
import sys
from typing import Tuple

FASTAPI_URL = "http://localhost:8001"
WORDPRESS_BASE = "https://tradingrobotplug.com/wp-json/tradingrobotplug/v1"

def check_fastapi_health() -> Tuple[bool, str]:
    """Check if FastAPI service is running."""
    try:
        response = requests.get(f"{FASTAPI_URL}/health", timeout=5)
        if response.status_code == 200:
            return True, "FastAPI service is running"
        return False, f"FastAPI returned {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "FastAPI service not accessible (connection refused)"
    except Exception as e:
        return False, f"Error checking FastAPI: {str(e)}"

def verify_endpoint(endpoint: str) -> Tuple[int, dict]:
    """Verify a WordPress endpoint."""
    url = f"{WORDPRESS_BASE}/{endpoint}"
    try:
        if endpoint == "orders":
            response = requests.post(url, json={}, timeout=10)
        else:
            response = requests.get(url, timeout=10)
        
        try:
            data = response.json()
        except:
            data = {"raw": response.text[:200]}
        
        return response.status_code, data
    except Exception as e:
        return 0, {"error": str(e)}

def main():
    """Monitor FastAPI deployment and verify endpoints."""
    print("🔍 Monitoring FastAPI deployment...\n")
    
    # Check FastAPI health
    print("1. Checking FastAPI service health...")
    is_running, message = check_fastapi_health()
    print(f"   {message}")
    
    if not is_running:
        print("\n⚠️  FastAPI service is not running yet.")
        print("   Waiting for service to start...")
        print("   (Run this script again after service starts)\n")
        return 1
    
    print("   ✅ FastAPI service is running!\n")
    
    # Verify WordPress endpoints
    print("2. Verifying WordPress REST API endpoints...\n")
    
    endpoints = [
        ("account", "GET"),
        ("positions", "GET"),
        ("trades", "GET"),
        ("strategies", "GET"),
        ("orders", "POST"),
    ]
    
    results = {}
    for endpoint, method in endpoints:
        print(f"   Testing /{endpoint}...")
        status, data = verify_endpoint(endpoint)
        success = status == 200 or (endpoint == "orders" and status == 400)
        results[endpoint] = success
        print(f"   Status: {status} {'✅' if success else '❌'}")
        if not success and status != 400:
            print(f"   Response: {str(data)[:150]}")
        print()
    
    # Summary
    print("=" * 60)
    print("📊 Verification Summary:")
    print("=" * 60)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    for endpoint, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {endpoint}: {status}")
    
    print()
    print(f"Total: {total} | Passed: {passed} | Failed: {failed}")
    print()
    
    if failed == 0:
        print("✅ All endpoints verified successfully!")
        print("✅ FastAPI deployment complete and integrated!")
        return 0
    else:
        print(f"⚠️  {failed} endpoint(s) need attention")
        return 1

if __name__ == "__main__":
    sys.exit(main())


