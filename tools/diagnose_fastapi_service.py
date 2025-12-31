#!/usr/bin/env python3
"""
FastAPI Service Diagnostic Tool
Comprehensive service diagnostics for troubleshooting.

Usage:
    python tools/diagnose_fastapi_service.py [--endpoint URL]
    
Provides comprehensive diagnostics to help identify service issues.
"""

import sys
import argparse
import requests
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent


def check_endpoint(endpoint: str, path: str) -> dict:
    """Check a specific endpoint."""
    try:
        url = f"{endpoint}{path}"
        response = requests.get(url, timeout=5)
        return {
            "available": True,
            "status_code": response.status_code,
            "url": url
        }
    except requests.exceptions.ConnectionError:
        return {
            "available": False,
            "error": "Connection refused",
            "url": url
        }
    except requests.exceptions.Timeout:
        return {
            "available": False,
            "error": "Connection timeout",
            "url": url
        }
    except Exception as e:
        return {
            "available": False,
            "error": str(e),
            "url": url
        }


def diagnose_service(endpoint: str = "http://localhost:8001"):
    """Run comprehensive service diagnostics."""
    print("="*70)
    print("FASTAPI SERVICE DIAGNOSTICS")
    print("="*70)
    print(f"Endpoint: {endpoint}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    diagnostics = {
        "endpoint": endpoint,
        "timestamp": datetime.now().isoformat(),
        "checks": {}
    }
    
    # Check 1: Health endpoint
    print("1. Health Endpoint Check")
    print("-" * 70)
    health_check = check_endpoint(endpoint, "/health")
    diagnostics["checks"]["health"] = health_check
    
    if health_check["available"]:
        print(f"   ✅ Health endpoint responding: {health_check['url']}")
        print(f"   Status Code: {health_check['status_code']}")
    else:
        print(f"   ❌ Health endpoint not available: {health_check['url']}")
        print(f"   Error: {health_check.get('error', 'Unknown')}")
    print()
    
    # Check 2: API root
    print("2. API Root Check")
    print("-" * 70)
    api_check = check_endpoint(endpoint, "/api/v1")
    diagnostics["checks"]["api_root"] = api_check
    
    if api_check["available"]:
        print(f"   ✅ API root responding: {api_check['url']}")
        print(f"   Status Code: {api_check['status_code']}")
    else:
        print(f"   ❌ API root not available: {api_check['url']}")
        print(f"   Error: {api_check.get('error', 'Unknown')}")
    print()
    
    # Check 3: Trades endpoint
    print("3. Trades Endpoint Check")
    print("-" * 70)
    trades_check = check_endpoint(endpoint, "/api/v1/trades")
    diagnostics["checks"]["trades"] = trades_check
    
    if trades_check["available"]:
        print(f"   ✅ Trades endpoint responding: {trades_check['url']}")
        print(f"   Status Code: {trades_check['status_code']}")
    else:
        print(f"   ❌ Trades endpoint not available: {trades_check['url']}")
        print(f"   Error: {trades_check.get('error', 'Unknown')}")
    print()
    
    # Summary
    print("="*70)
    print("DIAGNOSTIC SUMMARY")
    print("="*70)
    
    available_count = sum(1 for check in diagnostics["checks"].values() if check.get("available"))
    total_checks = len(diagnostics["checks"])
    
    print(f"Endpoints Available: {available_count}/{total_checks}")
    print()
    
    if health_check["available"]:
        print("✅ Service is READY for testing")
        print("   Health endpoint responding - validation can proceed")
    else:
        print("❌ Service is NOT READY")
        print()
        print("Troubleshooting Steps:")
        print("1. Verify service is running: sudo systemctl status tradingrobotplug-fastapi")
        print("2. Check service logs: sudo journalctl -u tradingrobotplug-fastapi -n 50")
        print("3. Verify .env file configuration (DATABASE_URL, API keys, etc.)")
        print("4. Restart service if needed: sudo systemctl restart tradingrobotplug-fastapi")
        print("5. Verify service starts: sudo systemctl status tradingrobotplug-fastapi")
    
    print("="*70)
    
    return diagnostics


def main():
    parser = argparse.ArgumentParser(description="Diagnose FastAPI service status")
    parser.add_argument("--endpoint", default="http://localhost:8001", help="FastAPI endpoint URL")
    args = parser.parse_args()
    
    diagnostics = diagnose_service(args.endpoint)
    
    # Exit with appropriate code
    health_available = diagnostics["checks"]["health"].get("available", False)
    sys.exit(0 if health_available else 1)


if __name__ == "__main__":
    main()

