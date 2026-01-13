#!/usr/bin/env python3
"""
Test Quantum Trading API Integration - TradingRobotPlug Ready
=============================================================

Tests the quantum trading API integration for TradingRobotPlug.
Demonstrates how to integrate quantum intelligence into trading bots.
"""

import asyncio
import requests
import json
import time
from typing import Dict, Any


def test_api_health():
    """Test if the quantum trading service is healthy."""
    try:
        response = requests.get("http://127.0.0.1:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Quantum Trading Service Health Check:")
            print(f"   Status: {data['status']}")
            print(f"   Service: {data['service']}")
            print(f"   Version: {data['version']}")
            print(f"   Quantum Intelligence: {data['quantum_intelligence']}")
            return True
        else:
            print(f"❌ Health check failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to quantum trading service: {e}")
        print("💡 Make sure to run: python quantum_trading_service_launcher.py")
        return False


def test_trading_signal():
    """Test quantum trading signal generation."""
    try:
        # Sample market data for AAPL
        payload = {
            "symbol": "AAPL",
            "market_data": {
                "price": 185.42,
                "volume": 52847392,
                "change_percent": 2.34,
                "market_cap": 2900000000000,
                "pe_ratio": 28.5
            }
        }

        print("📤 Testing Quantum Trading Signal for AAPL...")
        response = requests.post("http://127.0.0.1:8000/trading-signal", json=payload, timeout=10)

        if response.status_code == 200:
            signal = response.json()
            print("✅ Quantum Trading Signal Generated:")
            print(f"   🎯 Symbol: {signal['symbol']}")
            print(f"   📈 Action: {signal['action']}")
            print(f"   🎚️  Confidence: {signal['confidence']:.2f}")
            print(f"   ⚡ Quantum Amplification: {signal['quantum_amplification']:.1f}x")
            print(f"   🤖 Swarm Consensus: {signal['swarm_consensus']} agents")
            print(f"   ⚠️  Risk Level: {signal['risk_level']}")
            print(f"   🧠 Reasoning: {signal['reasoning'][:100]}...")
            return True
        else:
            print(f"❌ Trading signal failed: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"❌ Trading signal test failed: {e}")
        return False


def test_market_analysis():
    """Test quantum market analysis."""
    try:
        payload = {
            "symbol": "TSLA",
            "market_data": {
                "price": 248.50,
                "volume": 89567234,
                "change_percent": -0.87,
                "market_cap": 790000000000,
                "pe_ratio": 65.2
            }
        }

        print("📊 Testing Quantum Market Analysis for TSLA...")
        response = requests.post("http://127.0.0.1:8000/market-analysis", json=payload, timeout=10)

        if response.status_code == 200:
            analysis = response.json()
            print("✅ Quantum Market Analysis Complete:")
            print(f"   📈 Trend: {analysis['trend_direction']}")
            print(f"   📊 Volatility Index: {analysis['volatility_index']:.2f}")
            print(f"   🎚️  Quantum Confidence: {analysis['quantum_confidence']:.2f}")
            print(f"   🔮 Swarm Prediction: {analysis['swarm_prediction']}")
            print(f"   ⚠️  Risk Level: {analysis['risk_assessment']['level']}")
            return True
        else:
            print(f"❌ Market analysis failed: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"❌ Market analysis test failed: {e}")
        return False


def test_portfolio_analysis():
    """Test quantum portfolio optimization."""
    try:
        payload = {
            "holdings": [
                {"symbol": "AAPL", "quantity": 100, "current_price": 185.42},
                {"symbol": "TSLA", "quantity": 50, "current_price": 248.50},
                {"symbol": "BTC/USD", "quantity": 0.5, "current_price": 45123.67}
            ]
        }

        print("💼 Testing Quantum Portfolio Analysis...")
        response = requests.post("http://127.0.0.1:8000/portfolio-analysis", json=payload, timeout=10)

        if response.status_code == 200:
            portfolio = response.json()
            print("✅ Quantum Portfolio Analysis Complete:")
            print(".2f"            print(f"   🔄 Rebalancing Actions: {len(portfolio['rebalancing_actions'])}")
            print(f"   ⚠️  Risk Adjustments: {len(portfolio['risk_adjustments'])}")
            print(f"   🎯 Quantum Opportunities: {len(portfolio['quantum_opportunities'])}")

            if portfolio['rebalancing_actions']:
                print("   📋 Recommended Actions:")
                for action in portfolio['rebalancing_actions'][:2]:  # Show first 2
                    print(f"      • {action['symbol']}: {action['action']} ({action['confidence']:.2f})")
            else:
                print("   ✅ Portfolio optimally balanced")
            return True
        else:
            print(f"❌ Portfolio analysis failed: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"❌ Portfolio analysis test failed: {e}")
        return False


def test_batch_signals():
    """Test batch signal processing."""
    try:
        payload = [
            {
                "symbol": "AAPL",
                "market_data": {
                    "price": 185.42,
                    "volume": 52847392,
                    "change_percent": 2.34
                }
            },
            {
                "symbol": "GOOGL",
                "market_data": {
                    "price": 2750.80,
                    "volume": 1847392,
                    "change_percent": 1.45
                }
            }
        ]

        print("⚡ Testing Batch Quantum Signals...")
        response = requests.post("http://127.0.0.1:8000/batch-signals", json=payload, timeout=15)

        if response.status_code == 200:
            result = response.json()
            signals = result['signals']
            print(f"✅ Batch Processing Complete: {len(signals)} signals generated")

            for i, signal in enumerate(signals[:2]):  # Show first 2
                print(f"   Signal {i+1}: {signal['symbol']} - {signal['action']} ({signal['confidence']:.2f})")
            return True
        else:
            print(f"❌ Batch signals failed: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"❌ Batch signals test failed: {e}")
        return False


def show_integration_example():
    """Show TradingRobotPlug integration example."""
    print("\n" + "=" * 60)
    print("🎯 TRADINGROBOTPLUG INTEGRATION EXAMPLE")
    print("=" * 60)

    integration_code = '''
# TradingRobotPlug Quantum Integration Example
import requests
import time

class QuantumTradingBot:
    def __init__(self):
        self.quantum_api_url = "http://127.0.0.1:8000"
        self.confidence_threshold = 0.8

    def get_quantum_signal(self, symbol, market_data):
        """Get quantum-enhanced trading signal."""
        try:
            response = requests.post(
                f"{self.quantum_api_url}/trading-signal",
                json={"symbol": symbol, "market_data": market_data},
                timeout=5
            )

            if response.status_code == 200:
                signal = response.json()
                return signal
            else:
                print(f"Quantum API error: {response.status_code}")
                return None

        except Exception as e:
            print(f"Quantum API connection failed: {e}")
            return None

    def should_trade(self, symbol, market_data):
        """Determine if quantum intelligence recommends trading."""
        signal = self.get_quantum_signal(symbol, market_data)

        if signal and signal['confidence'] > self.confidence_threshold:
            if signal['action'] in ['BUY', 'SELL']:
                return {
                    'action': signal['action'],
                    'confidence': signal['confidence'],
                    'amplification': signal['quantum_amplification'],
                    'reasoning': signal['reasoning']
                }

        return None

    def execute_quantum_trade(self, symbol, market_data):
        """Execute trade based on quantum intelligence."""
        trade_decision = self.should_trade(symbol, market_data)

        if trade_decision:
            print(f"⚡ QUANTUM TRADE: {symbol} {trade_decision['action']}")
            print(f"   Confidence: {trade_decision['confidence']:.2f}")
            print(f"   Quantum Amplification: {trade_decision['amplification']:.1f}x")

            # Execute actual trade here
            # self.broker.place_order(symbol, trade_decision['action'], quantity)

            return True

        return False

# Usage Example
if __name__ == "__main__":
    bot = QuantumTradingBot()

    # Example market data
    market_data = {
        "price": 185.42,
        "volume": 52847392,
        "change_percent": 2.34
    }

    # Get quantum trading decision
    trade_executed = bot.execute_quantum_trade("AAPL", market_data)

    if trade_executed:
        print("✅ Quantum-powered trade executed!")
    else:
        print("⏸️  No quantum trade opportunity found")
'''

    print(integration_code)


def main():
    """Run comprehensive quantum API integration tests."""
    print("🧪 QUANTUM TRADING API INTEGRATION TESTS")
    print("=" * 50)
    print("Testing TradingRobotPlug quantum intelligence integration")
    print()

    # Test service health
    if not test_api_health():
        print("\n❌ Quantum Trading Service not available")
        print("💡 Start with: python quantum_trading_service_launcher.py")
        return 1

    print()

    # Run all tests
    tests = [
        ("Trading Signal Generation", test_trading_signal),
        ("Market Analysis", test_market_analysis),
        ("Portfolio Optimization", test_portfolio_analysis),
        ("Batch Signal Processing", test_batch_signals)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"🧪 Running: {test_name}")
        if test_func():
            passed += 1
            print("✅ PASSED")
        else:
            print("❌ FAILED")
        print("-" * 40)

    print(f"\n📊 TEST RESULTS: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Quantum Trading API ready for TradingRobotPlug integration")
        print("⚡ Revolutionary trading intelligence operational")

        # Show integration example
        show_integration_example()

        return 0
    else:
        print("⚠️  Some tests failed - check quantum service status")
        return 1


if __name__ == "__main__":
    exit(main())