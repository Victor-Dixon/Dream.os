#!/usr/bin/env python3
"""
FastAPI Service Verification Tool
Verifies FastAPI service is running and ready for testing.

Usage:
    python tools/verify_fastapi_service_ready.py [--endpoint URL]
    
Default endpoint: http://localhost:8001
"""

import sys
import argparse
import requests
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent


def verify_service(endpoint: str = "http://localhost:8001") -> dict:
    """Verify FastAPI service is running and healthy."""
    results = {
        "endpoint": endpoint,
        "timestamp": datetime.now().isoformat(),
        "checks": {}
    }
    
    # Check 1: Health endpoint
    print(f"🔍 Verifying FastAPI service at {endpoint}...")
    print()
    
    try:
        health_url = f"{endpoint}/health"
        print(f"1. Health check: {health_url}")
        response = requests.get(health_url, timeout=5)
        
        if response.status_code == 200:
            results["checks"]["health"] = {
                "status": "✅ PASS",
                "status_code": response.status_code,
                "response": response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text
            }
            print(f"   ✅ Health check passed (200)")
        else:
            results["checks"]["health"] = {
                "status": "❌ FAIL",
                "status_code": response.status_code,
                "error": f"Unexpected status code: {response.status_code}"
            }
            print(f"   ❌ Health check failed ({response.status_code})")
    except requests.exceptions.ConnectionError:
        results["checks"]["health"] = {
            "status": "❌ FAIL",
            "error": "Connection refused - service not running"
        }
        print(f"   ❌ Connection refused - service not running")
    except requests.exceptions.Timeout:
        results["checks"]["health"] = {
            "status": "❌ FAIL",
            "error": "Connection timeout"
        }
        print(f"   ❌ Connection timeout")
    except Exception as e:
        results["checks"]["health"] = {
            "status": "❌ FAIL",
            "error": str(e)
        }
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Check 2: API endpoint (if health passed)
    if results["checks"]["health"].get("status") == "✅ PASS":
        try:
            api_url = f"{endpoint}/api/v1/trades"
            print(f"2. API endpoint check: {api_url}")
            response = requests.get(api_url, timeout=5)
            
            if response.status_code in [200, 401, 403]:  # 401/403 means endpoint exists but needs auth
                results["checks"]["api"] = {
                    "status": "✅ PASS",
                    "status_code": response.status_code,
                    "note": "Endpoint accessible (auth may be required)"
                }
                print(f"   ✅ API endpoint accessible ({response.status_code})")
            else:
                results["checks"]["api"] = {
                    "status": "⚠️ WARN",
                    "status_code": response.status_code,
                    "note": f"Unexpected status code: {response.status_code}"
                }
                print(f"   ⚠️  API endpoint returned {response.status_code}")
        except Exception as e:
            results["checks"]["api"] = {
                "status": "⚠️ WARN",
                "error": str(e)
            }
            print(f"   ⚠️  API check error: {e}")
        
        print()
    
    # Summary
    all_passed = all(
        check.get("status") == "✅ PASS" 
        for check in results["checks"].values()
    )
    
    results["overall_status"] = "✅ READY" if all_passed else "❌ NOT READY"
    
    print("=" * 60)
    if all_passed:
        print("✅ Service is READY for testing")
    else:
        print("❌ Service is NOT READY")
        print("   Check systemd service status:")
        print("   sudo systemctl status tradingrobotplug-fastapi")
    print("=" * 60)
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Verify FastAPI service is ready for testing")
    parser.add_argument("--endpoint", default="http://localhost:8001", help="FastAPI endpoint URL")
    args = parser.parse_args()
    
    results = verify_service(args.endpoint)
    
    sys.exit(0 if results["overall_status"] == "✅ READY" else 1)


if __name__ == "__main__":
    main()

