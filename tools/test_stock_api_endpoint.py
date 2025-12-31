#!/usr/bin/env python3
"""
Utility script to test TradingRobotPlug stock data API endpoint.

Usage:
    python tools/test_stock_api_endpoint.py [symbol]
    
Example:
    python tools/test_stock_api_endpoint.py TSLA
"""

import sys
import requests
import json
from datetime import datetime

def test_stock_api(symbol='TSLA', base_url='https://tradingrobotplug.com'):
    """Test the stock data API endpoint."""
    endpoint = f"{base_url}/wp-json/tradingrobotplug/v1/stock-data"
    
    print(f"Testing stock data API endpoint: {endpoint}")
    print(f"Symbol: {symbol}")
    print("-" * 60)
    
    try:
        response = requests.get(endpoint, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response.elapsed.total_seconds():.2f}s")
        print("\nResponse Data:")
        print(json.dumps(data, indent=2))
        
        if 'stock_data' in data:
            stock_data = data['stock_data']
            print(f"\nFound {len(stock_data)} stock records")
            
            for stock in stock_data:
                if stock.get('symbol') == symbol:
                    print(f"\n{symbol} Data:")
                    print(f"  Price: ${stock.get('price', 'N/A')}")
                    print(f"  Change: {stock.get('change_percent', 'N/A')}%")
                    print(f"  Volume: {stock.get('volume', 'N/A'):,}" if stock.get('volume') else "  Volume: N/A")
                    print(f"  Source: {stock.get('source', 'unknown')}")
                    print(f"  Timestamp: {stock.get('timestamp', 'N/A')}")
                    return True
            
            print(f"\nWarning: {symbol} not found in response")
            print("Available symbols:", [s.get('symbol') for s in stock_data])
        else:
            print("\nWarning: No 'stock_data' field in response")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON response - {e}")
        return False

if __name__ == '__main__':
    symbol = sys.argv[1] if len(sys.argv) > 1 else 'TSLA'
    success = test_stock_api(symbol)
    sys.exit(0 if success else 1)


