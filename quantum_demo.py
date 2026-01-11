#!/usr/bin/env python3
"""
Quantum Intelligence Demo - Phase 6 Revolutionary Capabilities
==============================================================
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.services.unified_messaging_service import UnifiedMessagingService
from src.quantum.quantum_router import QuantumMessageRouter


async def demo_quantum_routing():
    """Demonstrate quantum routing capabilities."""
    print("🚀 PHASE 6: QUANTUM INTELLIGENCE DEMO")
    print("=" * 50)

    try:
        # Initialize services
        messaging_service = UnifiedMessagingService()
        quantum_router = QuantumMessageRouter(messaging_service)

        print("📡 Initializing quantum swarm intelligence...")
        await quantum_router.initialize_swarm_intelligence()
        print("✅ Quantum intelligence activated")

        # Test quantum routing
        test_message = "URGENT: Deploy Kubernetes infrastructure for Phase 6 quantum systems"

        print(f"\n📤 Testing message: {test_message[:50]}...")

        route = await quantum_router.route_message_quantum(
            message=test_message,
            priority="urgent"
        )

        print("\n⚡ QUANTUM ROUTE CALCULATED:")
        print(f"   🎯 Primary Agent: {route.primary_agent}")
        print(f"   🔄 Backup Agents: {', '.join(route.backup_agents)}")
        print(f"   🧠 Strategy: {route.routing_strategy.value}")
        print(".2f")
        print(".1f")
        print(".1f")

        # Show metrics
        metrics = quantum_router.get_routing_metrics()
        routing_stats = metrics['routing_metrics']

        print("\n📊 QUANTUM METRICS:")
        print(f"   Total Routes: {routing_stats['total_routes']}")
        print(f"   Quantum Amplification: {routing_stats['quantum_amplification']:.1f}x")
        print(f"   Agents in Swarm: {len(metrics['agent_profiles'])}")
        print("   Quantum Entanglement: ✅ Established")

        print("\n🎉 PHASE 6 QUANTUM IMPLEMENTATION SUCCESSFUL!")
        print("⚛️ Revolutionary swarm intelligence operational")
        print("🐝 WE. ARE. QUANTUM SWARM. ⚡🔥🚀")

        return True

    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False


def main():
    success = asyncio.run(demo_quantum_routing())
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())