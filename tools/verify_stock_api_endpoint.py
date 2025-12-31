#!/usr/bin/env python3
"""
Stock API Endpoint Verifier
============================
Quick utility to verify TradingRobotPlug stock data API endpoint is working.

Usage:
    python tools/verify_stock_api_endpoint.py
    python tools/verify_stock_api_endpoint.py --site tradingrobotplug.com
"""

import argparse
import requests
import json
from datetime import datetime

def verify_stock_api(site_url: str = "https://tradingrobotplug.com"):
    """Verify stock data API endpoint."""
    endpoint = f"{site_url}/wp-json/tradingrobotplug/v1/stock-data"
    
    print(f"🔍 Verifying: {endpoint}")
    print("-" * 60)
    
    try:
        response = requests.get(endpoint, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if 'stock_data' in data and len(data['stock_data']) > 0:
                print(f"✅ SUCCESS: {len(data['stock_data'])} symbols returned")
                print("\nSymbols:")
                for stock in data['stock_data']:
                    symbol = stock.get('symbol', 'N/A')
                    price = stock.get('price', 'N/A')
                    change_pct = stock.get('change_percent', 'N/A')
                    source = stock.get('source', 'N/A')
                    print(f"  {symbol}: ${price} ({change_pct}%) [source: {source}]")
                
                if 'timestamp' in data:
                    print(f"\nTimestamp: {data['timestamp']}")
                
                return True
            else:
                print("❌ ERROR: No stock data in response")
                print(f"Response: {json.dumps(data, indent=2)}")
                return False
        else:
            print(f"❌ ERROR: HTTP {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: Request failed - {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ ERROR: Invalid JSON response - {e}")
        print(f"Response: {response.text[:200]}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify TradingRobotPlug stock API endpoint")
    parser.add_argument("--site", default="https://tradingrobotplug.com", help="Site URL")
    
    args = parser.parse_args()
    
    success = verify_stock_api(args.site)
    exit(0 if success else 1)


