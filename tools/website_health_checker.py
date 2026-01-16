#!/usr/bin/env python3
"""
Website Health Checker - Agent-7 Closure Improvement
==============================================

Simple utility to check basic website health and responsiveness.
Created as closure improvement for website enhancement work.

Usage:
    python tools/website_health_checker.py [url]

Author: Agent-7
Date: 2026-01-16
"""

import sys
import requests
from urllib.parse import urlparse

def check_website_health(url):
    """Check basic website health and return status."""
    try:
        # Validate URL
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return {"status": "error", "message": "Invalid URL format"}

        # Make request with timeout
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'WebsiteHealthChecker/1.0'
        })

        result = {
            "url": url,
            "status_code": response.status_code,
            "response_time": response.elapsed.total_seconds(),
            "server": response.headers.get('server', 'Unknown'),
            "content_type": response.headers.get('content-type', 'Unknown')
        }

        if response.status_code == 200:
            result["status"] = "healthy"
            result["message"] = f"Website is responding normally ({response.elapsed.total_seconds():.2f}s)"
        elif response.status_code < 400:
            result["status"] = "warning"
            result["message"] = f"Website responded with status {response.status_code}"
        else:
            result["status"] = "error"
            result["message"] = f"Website error: HTTP {response.status_code}"

        return result

    except requests.exceptions.Timeout:
        return {"status": "error", "message": "Request timed out"}
    except requests.exceptions.ConnectionError:
        return {"status": "error", "message": "Connection failed"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}

def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: python tools/website_health_checker.py <url>")
        print("Example: python tools/website_health_checker.py https://weareswarm.site")
        sys.exit(1)

    url = sys.argv[1]
    result = check_website_health(url)

    print(f"Website Health Check: {url}")
    print(f"Status: {result['status'].upper()}")
    print(f"Message: {result['message']}")

    if 'status_code' in result:
        print(f"HTTP Status: {result['status_code']}")
        print(f"Response Time: {result['response_time']:.2f}s")
        print(f"Server: {result['server']}")
        print(f"Content-Type: {result['content_type']}")

if __name__ == "__main__":
    main()