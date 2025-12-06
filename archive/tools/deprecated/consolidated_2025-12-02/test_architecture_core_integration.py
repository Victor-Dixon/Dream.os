#!/usr/bin/env python3
"""Test Phase 3 Architecture Core Integration"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.architecture.unified_architecture_core import UnifiedArchitectureCore

def test_phase3_integration():
    """Test Phase 3 integration features."""
    print("🧪 Testing Phase 3 Architecture Core Integration\n")
    
    core = UnifiedArchitectureCore()
    
    # Test auto-discovery
    print("1. Testing Component Auto-Discovery...")
    discovered = core.auto_discover_components()
    print(f"   ✅ Auto-discovered {len(discovered)} components")
    for name in discovered.keys():
        print(f"      - {name}")
    
    # Test integrated health
    print("\n2. Testing Integrated Health Monitoring...")
    health = core.get_integrated_health()
    print(f"   ✅ Health check complete")
    print(f"      - Total components: {health.get('total_components', 0)}")
    print(f"      - Active components: {health.get('active_components', 0)}")
    print(f"      - Health percentage: {health.get('health_percentage', 0):.1f}%")
    if 'orchestrator' in health:
        print(f"      - Orchestrator: {health['orchestrator'].get('status', 'unknown')}")
    if 'message_queue' in health:
        print(f"      - Message Queue: {health['message_queue'].get('status', 'unknown')}")
    if 'performance' in health:
        print(f"      - Performance: {health['performance'].get('status', 'unknown')}")
    
    # Test consolidation
    print("\n3. Testing Architecture Consolidation...")
    result = core.consolidate_architecture()
    print(f"   ✅ Consolidation complete")
    print(f"      - Components registered: {result.get('components_registered', 0)}")
    print(f"      - Auto-discovered: {result.get('auto_discovered', 0)}")
    print(f"      - Status: {result.get('consolidation_status', 'unknown')}")
    
    print("\n✅ Phase 3 Integration Test Complete!")
    return True

if __name__ == '__main__':
    test_phase3_integration()

