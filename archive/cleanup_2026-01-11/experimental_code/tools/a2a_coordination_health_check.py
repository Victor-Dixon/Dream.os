#!/usr/bin/env python3
"""
A2A Coordination Health Check Tool
==================================

Simple utility to verify A2A coordination system health and status.
Checks messaging infrastructure, coordination protocols, and system readiness.

Usage:
    python tools/a2a_coordination_health_check.py

V2 Compliance: <150 lines, single responsibility
Author: Agent-2 - Architecture & Design Specialist
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def check_coordination_infrastructure():
    """Check if coordination infrastructure is operational."""
    try:
        from src.services.messaging_cli import MessagingCLI
        return True, "Messaging CLI available"
    except ImportError as e:
        return False, f"Messaging CLI not available: {e}"

def check_ai_capabilities():
    """Check if AI capabilities are operational."""
    try:
        from src.ai_training.dreamvault.advanced_reasoning import AdvancedReasoningEngine
        engine = AdvancedReasoningEngine()
        stats = engine.get_performance_stats()
        return True, f"AI reasoning available with {stats.get('supported_modes', 0)} modes"
    except Exception as e:
        return False, f"AI capabilities not available: {e}"

def check_vector_database():
    """Check if vector database is operational."""
    try:
        from src.services.vector.vector_database_service import get_vector_database_service
        vdb = get_vector_database_service()
        stats = vdb.get_performance_stats()
        return True, f"Vector DB available with {stats.get('collections_count', 0)} collections"
    except Exception as e:
        return False, f"Vector database not available: {e}"

def check_web_performance():
    """Check if web performance optimizations are active."""
    try:
        import requests
        # Try to connect to FastAPI health endpoint
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("performance"):
                return True, "Web performance monitoring active"
            else:
                return True, "Web API available (performance monitoring not configured)"
        else:
            return False, f"Web API returned status {response.status_code}"
    except Exception as e:
        return False, f"Web API not accessible: {e}"

def main():
    """Run comprehensive coordination health check."""
    print("🐝 A2A Coordination Health Check")
    print("=" * 50)

    checks = [
        ("Coordination Infrastructure", check_coordination_infrastructure),
        ("AI Capabilities", check_ai_capabilities),
        ("Vector Database", check_vector_database),
        ("Web Performance", check_web_performance),
    ]

    all_passed = True
    for name, check_func in checks:
        print(f"\n🔍 Checking {name}...")
        try:
            passed, message = check_func()
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"   {status}: {message}")
            if not passed:
                all_passed = False
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            all_passed = False

    print(f"\n{'='*50}")
    if all_passed:
        print("🎯 A2A Coordination System: HEALTHY")
        print("   All components operational and ready for coordination.")
        return 0
    else:
        print("⚠️  A2A Coordination System: DEGRADED")
        print("   Some components may not be fully operational.")
        return 1

if __name__ == "__main__":
    sys.exit(main())