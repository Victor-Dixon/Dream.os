#!/usr/bin/env python3
"""
🔌 Plugin System Demo
====================

Demonstrates the Phase 3 MVP plugin framework.
Shows plugin discovery, loading, and execution.

Usage:
    python demo_plugin_system.py

<!-- SSOT Domain: plugins -->
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from plugins.plugin_manager import demo_plugin_system


if __name__ == "__main__":
    try:
        demo_plugin_system()
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()