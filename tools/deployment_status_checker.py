#!/usr/bin/env python3
"""
Deployment Status Checker

Quick utility to verify deployment status by checking live site for specific code patterns.
Useful for verifying frontend deployments and API endpoints.

Usage:
    python tools/deployment_status_checker.py <url> <pattern1> [pattern2] ...
    python tools/deployment_status_checker.py https://tradingrobotplug.com/ fetchStockData market-items-container
"""

import sys
import requests
from typing import List, Tuple


def check_deployment(url: str, patterns: List[str]) -> Tuple[bool, dict]:
    """
    Check if deployment patterns are present on live site.
    
    Args:
        url: Site URL to check
        patterns: List of string patterns to search for
        
    Returns:
        Tuple of (all_found, results_dict)
    """
    try:
        r = requests.get(url, headers={'Cache-Control': 'no-cache', 'Pragma': 'no-cache'}, timeout=10)
        r.raise_for_status()
        html = r.text
        
        results = {}
        all_found = True
        
        for pattern in patterns:
            found = pattern in html
            results[pattern] = found
            if not found:
                all_found = False
        
        return all_found, results
        
    except requests.RequestException as e:
        print(f"❌ Error checking {url}: {e}")
        return False, {}


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    
    url = sys.argv[1]
    patterns = sys.argv[2:]
    
    print(f"🔍 Checking deployment status for: {url}")
    print(f"   Patterns: {', '.join(patterns)}\n")
    
    all_found, results = check_deployment(url, patterns)
    
    for pattern, found in results.items():
        status = "✅" if found else "❌"
        print(f"{status} {pattern}: {'Found' if found else 'Not found'}")
    
    print()
    if all_found:
        print("✅ DEPLOYMENT COMPLETE - All patterns found")
    else:
        print("❌ DEPLOYMENT INCOMPLETE - Some patterns missing")


if __name__ == "__main__":
    main()

