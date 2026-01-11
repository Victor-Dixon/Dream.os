#!/usr/bin/env python3
"""
Quantum Trading Service Launcher - FastAPI Integration for TradingRobotPlug
=============================================================================

Launches the FastAPI quantum trading service for easy integration.
Provides REST API endpoints for quantum-enhanced trading intelligence.

Usage:
    python quantum_trading_service_launcher.py

API Endpoints:
    GET  /               - API information
    POST /trading-signal - Get quantum trading signals
    POST /market-analysis - Get market analysis
    POST /portfolio-analysis - Get portfolio recommendations
    GET  /metrics        - Get trading performance metrics
    GET  /health         - Service health check
    POST /batch-signals  - Batch processing for multiple symbols

Example Integration in TradingRobotPlug:
    import requests

    # Get quantum trading signal
    response = requests.post('http://localhost:8000/trading-signal', json={
        'symbol': 'AAPL',
        'market_data': {
            'price': 185.42,
            'volume': 52847392,
            'change_percent': 2.34
        }
    })

    signal = response.json()
    if signal['action'] == 'BUY' and signal['confidence'] > 0.8:
        # Execute trade with quantum intelligence
        execute_trade(signal['symbol'], signal['action'])
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Launch the quantum trading service."""
    print("🚀 QUANTUM TRADING SERVICE LAUNCHER")
    print("=" * 50)
    print("FastAPI service for TradingRobotPlug integration")
    print()

    try:
        from src.quantum.quantum_trading_service import start_quantum_trading_service

        print("📡 Starting FastAPI quantum trading service...")
        print("🔗 API will be available at: http://127.0.0.1:8000")
        print("📋 API Documentation: http://127.0.0.1:8000/docs")
        print()
        print("🎯 Integration Ready for TradingRobotPlug!")
        print("⚡ Revolutionary quantum trading intelligence operational")
        print()

        # Start the service
        start_quantum_trading_service(host="127.0.0.1", port=8000)

    except KeyboardInterrupt:
        print("\n🛑 Quantum Trading Service stopped by user")
    except Exception as e:
        print(f"❌ Failed to start quantum trading service: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())