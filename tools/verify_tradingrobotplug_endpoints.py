#!/usr/bin/env python3
"""
Verify TradingRobotPlug WordPress REST API endpoints after FastAPI deployment.

<!-- SSOT Domain: web -->
"""

import requests
import json
import sys
from typing import Dict, List, Tuple

BASE_URL = "https://tradingrobotplug.com/wp-json/tradingrobotplug/v1"

def test_endpoint(method: str, endpoint: str, data: dict = None) -> Tuple[int, dict]:
    """Test an endpoint and return status code and response."""
    url = f"{BASE_URL}/{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(
                url,
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
        else:
            return 0, {"error": f"Unsupported method: {method}"}
        
        try:
            response_data = response.json()
        except:
            response_data = {"raw": response.text[:200]}
        
        return response.status_code, response_data
    except Exception as e:
        return 0, {"error": str(e)}

def verify_endpoints() -> Dict[str, bool]:
    """Verify all endpoints and return results."""
    results = {}
    
    print("🔍 Verifying TradingRobotPlug WordPress REST API endpoints...\n")
    
    # 1. Account endpoint
    print("1. Testing /account endpoint...")
    status, data = test_endpoint("GET", "account")
    success = status == 200
    results["account"] = success
    print(f"   Status: {status} {'✅' if success else '❌'}")
    if not success:
        print(f"   Response: {json.dumps(data, indent=2)[:200]}")
    print()
    
    # 2. Positions endpoint
    print("2. Testing /positions endpoint...")
    status, data = test_endpoint("GET", "positions")
    success = status == 200
    results["positions"] = success
    print(f"   Status: {status} {'✅' if success else '❌'}")
    if not success:
        print(f"   Response: {json.dumps(data, indent=2)[:200]}")
    print()
    
    # 3. Trades endpoint
    print("3. Testing /trades endpoint...")
    status, data = test_endpoint("GET", "trades")
    success = status == 200
    results["trades"] = success
    print(f"   Status: {status} {'✅' if success else '❌'}")
    if not success:
        print(f"   Response: {json.dumps(data, indent=2)[:200]}")
    print()
    
    # 4. Strategies endpoint
    print("4. Testing /strategies endpoint...")
    status, data = test_endpoint("GET", "strategies")
    success = status == 200
    results["strategies"] = success
    print(f"   Status: {status} {'✅' if success else '❌'}")
    if not success:
        print(f"   Response: {json.dumps(data, indent=2)[:200]}")
    print()
    
    # 5. Orders endpoint (validation test - should return 400)
    print("5. Testing /orders endpoint (validation test)...")
    status, data = test_endpoint("POST", "orders", {})
    success = status == 400  # Expected 400 for missing required fields
    results["orders_validation"] = success
    print(f"   Status: {status} {'✅' if success else '❌'} (expected 400 for validation)")
    if not success:
        print(f"   Response: {json.dumps(data, indent=2)[:200]}")
    print()
    
    # 6. Orders endpoint (with valid data - should return 200)
    print("6. Testing /orders endpoint (with valid data)...")
    order_data = {
        "symbol": "TSLA",
        "side": "buy",
        "quantity": 10,
        "order_type": "market"
    }
    status, data = test_endpoint("POST", "orders", order_data)
    success = status == 200
    results["orders_submit"] = success
    print(f"   Status: {status} {'✅' if success else '❌'}")
    if not success:
        print(f"   Response: {json.dumps(data, indent=2)[:200]}")
    print()
    
    return results

def main():
    """Main verification function."""
    results = verify_endpoints()
    
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
        return 0
    else:
        print(f"⚠️  {failed} endpoint(s) need attention")
        return 1

if __name__ == "__main__":
    sys.exit(main())


