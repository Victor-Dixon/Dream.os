#!/usr/bin/env python3
"""
Quantum Trading API Demo - Integration Guide for TradingRobotPlug
==================================================================

Demonstrates quantum-powered trading intelligence for TradingRobotPlug integration.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.quantum.quantum_trading_api import get_quantum_trading_api


async def demonstrate_quantum_trading():
    """Demonstrate quantum trading capabilities."""
    print("🚀 QUANTUM TRADING API DEMO")
    print("=" * 50)
    print("Integration Guide for TradingRobotPlug")
    print()

    # Initialize quantum trading API
    print("⚡ Initializing quantum trading intelligence...")
    trading_api = await get_quantum_trading_api()
    print("✅ Quantum trading API ready")
    print()

    # Sample market data for demonstration
    sample_data = {
        'AAPL': {
            'price': 185.42,
            'volume': 52847392,
            'change_percent': 2.34,
            'market_cap': 2.9e12,
            'pe_ratio': 28.5
        },
        'BTC/USD': {
            'price': 45123.67,
            'volume': 2847392056,
            'change_percent': -1.23,
            'market_cap': 8.7e11,
            'volatility': 0.85
        },
        'TSLA': {
            'price': 248.50,
            'volume': 89567234,
            'change_percent': -0.87,
            'market_cap': 7.9e11,
            'pe_ratio': 65.2
        }
    }

    print("📊 DEMONSTRATING QUANTUM TRADING SIGNALS")
    print("-" * 45)

    for symbol, market_data in sample_data.items():
        print(f"\n🎯 Analyzing {symbol}")
        print(f"   Price: ${market_data['price']:,.2f}")
        print(f"   Change: {market_data['change_percent']:+.2f}%")
        print(f"   Volume: {market_data['volume']:,.0f}")

        # Get quantum trading signal
        signal = await trading_api.get_trading_signal(symbol, market_data)

        print("\n⚡ QUANTUM SIGNAL:")
        print(f"   🎯 Action: {signal.action}")
        print(f"   🎚️  Confidence: {signal.confidence:.2f}")
        print(f"   ⚡ Quantum Amplification: {signal.quantum_amplification:.1f}x")
        print(f"   🤖 Swarm Consensus: {signal.swarm_consensus} agents")
        print(f"   ⚠️  Risk Level: {signal.risk_level}")
        print(f"   🧠 Reasoning: {signal.reasoning[:100]}...")

    print("\n\n📈 DEMONSTRATING MARKET ANALYSIS")
    print("-" * 40)

    for symbol, market_data in list(sample_data.items())[:2]:  # Analyze first 2 symbols
        print(f"\n📊 Quantum Analysis for {symbol}")

        analysis = await trading_api.get_market_analysis(symbol, market_data)

        print(f"   📈 Trend: {analysis.trend_direction}")
        print(f"   📊 Volatility Index: {analysis.volatility_index:.2f}")
        print(f"   🎚️  Quantum Confidence: {analysis.quantum_confidence:.2f}")
        print(f"   🔮 Swarm Prediction: {analysis.swarm_prediction}")
        print(f"   ⚠️  Risk Assessment: {analysis.risk_assessment['level']}")

    print("\n\n💼 DEMONSTRATING PORTFOLIO OPTIMIZATION")
    print("-" * 45)

    # Sample portfolio
    sample_portfolio = [
        {'symbol': 'AAPL', 'quantity': 100, 'current_price': 185.42},
        {'symbol': 'TSLA', 'quantity': 50, 'current_price': 248.50},
        {'symbol': 'BTC/USD', 'quantity': 0.5, 'current_price': 45123.67}
    ]

    print("📋 Sample Portfolio:")
    total_value = 0
    for holding in sample_portfolio:
        value = holding['quantity'] * holding['current_price']
        total_value += value
        print(".2f")

    print(".2f")
    print()

    # Get portfolio recommendations
    recommendations = await trading_api.get_portfolio_recommendations(sample_portfolio)

    print("🎯 Quantum Portfolio Recommendations:")
    print(f"   📊 Overall Confidence: {recommendations['overall_confidence']:.2f}")

    if recommendations['rebalancing_actions']:
        print("   🔄 Rebalancing Actions:")
        for action in recommendations['rebalancing_actions']:
            print(f"      • {action['symbol']}: {action['action']} "
                  f"(confidence: {action['confidence']:.2f})")
            print(f"        Reason: {action['reason']}")
    else:
        print("   ✅ Portfolio optimally balanced")

    print("\n\n📊 QUANTUM TRADING METRICS")
    print("-" * 35)
    metrics = trading_api.get_trading_metrics()

    print(f"📈 Signals Generated: {metrics['signals_generated']}")
    print(f"🎯 Successful Predictions: {metrics['successful_predictions']}")
    print(f"⚡ Quantum Accuracy: {metrics['quantum_accuracy']:.2f}")
    print(f"🤖 Active Signals: {metrics['active_signals']}")
    print(f"🧠 Swarm Intelligence: {metrics['swarm_intelligence']['agents_coordinating']} agents coordinating")
    print(f"🔗 Quantum Entanglement: {metrics['swarm_intelligence']['quantum_entanglement']}")
    print(f"🔮 Predictive Routing: {metrics['swarm_intelligence']['predictive_routing']}")

    print("\n" + "=" * 60)
    print("🎉 QUANTUM TRADING INTEGRATION COMPLETE!")
    print("=" * 60)
    print("📝 Integration Steps for TradingRobotPlug:")
    print("1. Import: from src.quantum.quantum_trading_api import get_quantum_trading_api")
    print("2. Initialize: api = await get_quantum_trading_api()")
    print("3. Get signals: signal = await api.get_trading_signal(symbol, market_data)")
    print("4. Use in trading logic: if signal.action == 'BUY' and signal.confidence > 0.8:")
    print("5. Monitor metrics: metrics = api.get_trading_metrics()")
    print()
    print("⚡ Revolutionary trading intelligence ready for deployment!")
    print("🐝 WE. ARE. QUANTUM TRADING SWARM. 🚀🔥⚡")


def main():
    """Run the quantum trading demo."""
    success = asyncio.run(demonstrate_quantum_trading())
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())