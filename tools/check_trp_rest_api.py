#!/usr/bin/env python3
"""Check TradingRobotPlug REST API routes."""

import requests
import json

base_url = "https://tradingrobotplug.com"

# Get REST API index
print("Fetching REST API index...")
try:
    response = requests.get(f"{base_url}/wp-json/", timeout=10)
    data = response.json()
    
    routes = data.get('routes', {})
    trp_routes = {k: v for k, v in routes.items() if 'tradingrobotplug' in k}
    
    print(f"\nFound {len(trp_routes)} TradingRobotPlug routes:")
    for route, info in sorted(trp_routes.items()):
        methods = info.get('methods', [])
        print(f"  {route}: {methods}")
    
    # Check specific endpoints
    print("\nChecking specific endpoints:")
    endpoints = [
        '/wp-json/tradingrobotplug/v1/waitlist',
        '/wp-json/tradingrobotplug/v1/contact',
        '/wp-json/tradingrobotplug/v1/dashboard',
        '/wp-json/tradingrobotplug/v1/performance',
        '/wp-json/tradingrobotplug/v1/strategies',
        '/wp-json/tradingrobotplug/v1/trades',
    ]
    
    for endpoint in endpoints:
        try:
            resp = requests.get(f"{base_url}{endpoint}", timeout=5)
            status = "✅" if resp.status_code == 200 else "❌"
            print(f"  {status} {endpoint}: {resp.status_code}")
        except Exception as e:
            print(f"  ❌ {endpoint}: Error - {e}")
            
except Exception as e:
    print(f"Error: {e}")




