#!/usr/bin/env python3
"""
Endpoint Status Verifier
Quick utility to verify WordPress REST API endpoint status.

Usage:
    python tools/verify_endpoint_status.py --endpoint /wp-json/tradingrobotplug/v1/trades
    python tools/verify_endpoint_status.py --base-url https://tradingrobotplug.com --endpoint /wp-json/tradingrobotplug/v1/account
"""

import argparse
import requests
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def verify_endpoint(base_url: str, endpoint: str) -> dict:
    """Verify endpoint status and return diagnostic info."""
    url = f"{base_url.rstrip('/')}{endpoint}"
    
    try:
        response = requests.get(url, timeout=10)
        return {
            "status_code": response.status_code,
            "url": url,
            "response_preview": response.text[:200] if len(response.text) > 200 else response.text,
            "headers": dict(response.headers),
            "success": response.status_code < 500
        }
    except requests.exceptions.ConnectionError as e:
        return {
            "status_code": None,
            "url": url,
            "error": f"Connection error: {str(e)}",
            "success": False
        }
    except Exception as e:
        return {
            "status_code": None,
            "url": url,
            "error": f"Error: {str(e)}",
            "success": False
        }


def main():
    parser = argparse.ArgumentParser(description="Verify WordPress REST API endpoint status")
    parser.add_argument("--endpoint", required=True, help="Endpoint path (e.g., /wp-json/tradingrobotplug/v1/trades)")
    parser.add_argument("--base-url", default="https://tradingrobotplug.com", help="Base URL (default: https://tradingrobotplug.com)")
    
    args = parser.parse_args()
    
    result = verify_endpoint(args.base_url, args.endpoint)
    
    if result["success"]:
        print(f"✅ Endpoint accessible: {result['url']}")
        print(f"   Status: {result['status_code']}")
    else:
        print(f"❌ Endpoint issue: {result['url']}")
        if "status_code" in result and result["status_code"]:
            print(f"   Status: {result['status_code']}")
        if "error" in result:
            print(f"   Error: {result['error']}")
    
    if "response_preview" in result:
        print(f"\nResponse preview:\n{result['response_preview']}")
    
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())

