#!/usr/bin/env python3
"""
Analytics Domain Import Validation
Validates that all analytics core components can be imported and instantiated.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

results = {
    "imports": {},
    "instantiations": {},
    "status": "UNKNOWN"
}

try:
    # Test MetricsEngine
    from core.analytics.engines.metrics_engine import MetricsEngine
    results["imports"]["MetricsEngine"] = "✅ SUCCESS"
    
    engine = MetricsEngine()
    results["instantiations"]["MetricsEngine"] = "✅ SUCCESS"
    
except Exception as e:
    results["imports"]["MetricsEngine"] = f"❌ FAILED: {str(e)}"
    results["instantiations"]["MetricsEngine"] = "❌ FAILED"

try:
    # Test BusinessIntelligenceEngine
    from core.analytics.intelligence.business_intelligence_engine import BusinessIntelligenceEngine
    results["imports"]["BusinessIntelligenceEngine"] = "✅ SUCCESS"
    
    bi = BusinessIntelligenceEngine()
    results["instantiations"]["BusinessIntelligenceEngine"] = "✅ SUCCESS"
    
except Exception as e:
    results["imports"]["BusinessIntelligenceEngine"] = f"❌ FAILED: {str(e)}"
    results["instantiations"]["BusinessIntelligenceEngine"] = "❌ FAILED"

try:
    # Test ProcessingCoordinator
    from core.analytics.coordinators.processing_coordinator import ProcessingCoordinator
    results["imports"]["ProcessingCoordinator"] = "✅ SUCCESS"
    
    coord = ProcessingCoordinator()
    results["instantiations"]["ProcessingCoordinator"] = "✅ SUCCESS"
    
except Exception as e:
    results["imports"]["ProcessingCoordinator"] = f"❌ FAILED: {str(e)}"
    results["instantiations"]["ProcessingCoordinator"] = "❌ FAILED"

# Determine overall status
all_passed = all(
    "✅" in status for status in list(results["imports"].values()) + list(results["instantiations"].values())
)

results["status"] = "✅ PASS" if all_passed else "❌ FAIL"

# Print results
print("=" * 60)
print("ANALYTICS DOMAIN IMPORT VALIDATION")
print("=" * 60)
print("\nIMPORTS:")
for component, status in results["imports"].items():
    print(f"  {component}: {status}")

print("\nINSTANTIATIONS:")
for component, status in results["instantiations"].items():
    print(f"  {component}: {status}")

print(f"\nOVERALL STATUS: {results['status']}")
print("=" * 60)

# Exit with appropriate code
sys.exit(0 if all_passed else 1)

