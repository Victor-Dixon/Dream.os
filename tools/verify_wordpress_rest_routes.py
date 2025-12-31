#!/usr/bin/env python3
"""
Verify WordPress REST API routes are registered for TradingRobotPlug.

<!-- SSOT Domain: web -->
"""

import requests
import sys
from pathlib import Path

def check_rest_routes(base_url="http://localhost:8000"):
    """Check if REST API routes are registered."""
    endpoints = [
        "/wp-json/tradingrobotplug/v1/trades",
        "/wp-json/tradingrobotplug/v1/strategies",
        "/wp-json/tradingrobotplug/v1/account",
        "/wp-json/tradingrobotplug/v1/positions",
        "/wp-json/tradingrobotplug/v1/orders",
    ]
    
    print("🔍 Checking WordPress REST API Routes\n")
    
    results = {}
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        try:
            response = requests.get(url, timeout=5)
            status = response.status_code
            
            if status == 200:
                results[endpoint] = "✅ 200 OK"
                print(f"✅ {endpoint}: 200 OK")
            elif status == 401:
                results[endpoint] = "⚠️  401 Unauthorized (endpoint exists, auth required)"
                print(f"⚠️  {endpoint}: 401 Unauthorized (endpoint exists)")
            elif status == 404:
                results[endpoint] = "❌ 404 Not Found (endpoint not registered)"
                print(f"❌ {endpoint}: 404 Not Found")
            else:
                results[endpoint] = f"⚠️  {status}"
                print(f"⚠️  {endpoint}: {status}")
        except requests.exceptions.ConnectionError:
            results[endpoint] = "❌ Connection Error (WordPress not running)"
            print(f"❌ {endpoint}: Connection Error")
        except requests.exceptions.RequestException as e:
            results[endpoint] = f"❌ Error: {e}"
            print(f"❌ {endpoint}: {e}")
    
    print("\n📊 Summary:")
    registered = sum(1 for r in results.values() if "200" in r or "401" in r)
    not_found = sum(1 for r in results.values() if "404" in r)
    
    print(f"   Registered endpoints: {registered}/{len(endpoints)}")
    print(f"   Not found (404): {not_found}/{len(endpoints)}")
    
    if not_found > 0:
        print("\n⚠️  Some endpoints returning 404 - possible causes:")
        print("   1. Plugin not activated")
        print("   2. REST API routes need flush: wp rewrite flush")
        print("   3. API_Client class missing or not working")
    
    return registered == len(endpoints)

def main():
    """Verify REST API routes."""
    all_registered = check_rest_routes()
    
    if all_registered:
        print("\n✅ All endpoints registered and accessible")
        return 0
    else:
        print("\n⚠️  Some endpoints not accessible - review required")
        return 1

if __name__ == "__main__":
    sys.exit(main())


