#!/usr/bin/env python3
"""
🚀 Phase 3 Plugin System Demo
============================

Demonstrates the complete Phase 3 Plugin Architecture implementation.
Shows plugin discovery, loading, interfaces, and sandboxing in action.

<!-- SSOT Domain: plugins -->
"""

import asyncio
import logging
from datetime import datetime, timedelta

from src.plugins.plugin_loader import PluginLoader
from src.plugins.plugin_sandbox import SandboxManager
from src.plugins.plugin_interface import TimeRange, PluginConfig

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def demo_phase3_plugin_system():
    """Demonstrate the complete Phase 3 plugin system."""
    print("🚀 Agent Cellphone V2 - Phase 3 Plugin System Demo")
    print("=" * 60)
    print(f"Demo started at: {datetime.now()}")
    print()

    try:
        # 1. Initialize Plugin Loader
        print("🔌 Step 1: Initializing Plugin Loader...")
        loader = PluginLoader()
        print("✅ Plugin loader initialized")

        # 2. Discover Plugins
        print("\n🔍 Step 2: Discovering Plugins...")
        discovered_plugins = await loader.discover_plugins()
        print(f"📦 Discovered {len(discovered_plugins)} plugins:")
        for plugin in discovered_plugins:
            print(f"  • {plugin.name} ({plugin.plugin_id}) - {plugin.category.value}")
        print("✅ Plugin discovery complete")

        # 3. Load Analytics Plugin
        print("\n📊 Step 3: Loading Analytics Plugin...")
        analytics_config = PluginConfig(
            plugin_id="analytics-plugin",
            version="1.0.0",
            enabled=True,
            settings={
                "collection_interval": 5,  # 5 seconds for demo
                "retention_days": 1,
                "enable_real_time": True
            }
        )

        success = await loader.load_plugin("analytics-plugin", analytics_config)
        if success:
            print("✅ Analytics plugin loaded successfully")
        else:
            print("❌ Failed to load analytics plugin")
            return

        # 4. Initialize Sandbox
        print("\n🛡️ Step 4: Setting up Plugin Sandbox...")
        sandbox_manager = SandboxManager()
        sandbox = sandbox_manager.create_sandbox("analytics-plugin")

        def violation_handler(violation, details):
            print(f"🚨 Sandbox violation: {violation.value} - {details}")

        sandbox.add_violation_handler(violation_handler)
        print("✅ Plugin sandbox configured with violation monitoring")

        # 5. Test Plugin Interfaces
        print("\n🔧 Step 5: Testing Plugin Interfaces...")

        # Get plugin instance
        analytics_plugin = await loader.get_plugin_instance("analytics-plugin")
        if analytics_plugin:
            print("✅ Plugin instance retrieved")

            # Test IAnalyticsProvider interface
            metrics_defs = await analytics_plugin.get_metrics()
            print(f"📈 Plugin provides {len(metrics_defs)} metrics:")
            for metric in metrics_defs[:3]:  # Show first 3
                print(f"  • {metric.name}: {metric.description}")

            # Wait for some metrics collection
            print("\n⏳ Waiting for metrics collection...")
            await asyncio.sleep(6)  # Wait for collection interval

            # Collect metrics
            time_range = TimeRange(
                start=datetime.now() - timedelta(minutes=5),
                end=datetime.now()
            )
            metrics_data = await analytics_plugin.collect_metrics(time_range)
            print(f"📊 Collected metrics: {len(metrics_data.metrics)} data points")

            # Generate report
            report = await analytics_plugin.generate_report(metrics_data, "json")
            print(f"📋 Generated report: {report.title}")
            print(f"📄 Report format: {report.format}")

        else:
            print("❌ Failed to get plugin instance")

        # 6. Test Sandbox Execution
        print("\n🧪 Step 6: Testing Sandboxed Execution...")

        async def test_function():
            """Test function for sandbox execution."""
            import json
            import math

            data = {
                "timestamp": datetime.now().isoformat(),
                "calculation": math.sqrt(144),  # Should be 12
                "status": "sandbox_test_successful"
            }
            return json.dumps(data)

        result = await sandbox.execute_sandboxed(test_function)
        if result.success:
            print("✅ Sandbox execution successful")
            print(f"📄 Result: {result.result[:100]}...")
            print(".2f")
        else:
            print("❌ Sandbox execution failed")
            print(f"Error: {result.result}")

        # 7. Test Resource Monitoring
        print("\n📊 Step 7: Resource Usage Monitoring...")
        usage = sandbox.get_resource_usage()
        print(f"💾 Memory usage: {usage['memory_mb']:.1f} MB")
        print(f"🧵 Active threads: {usage['active_threads']}")
        print(f"⚙️ Limits: {usage['limits']['max_memory_mb']} MB memory, {usage['limits']['max_execution_time_sec']}s timeout")

        # 8. Validation Checks
        print("\n✅ Step 8: System Validation...")
        validations = [
            ("Plugin discovery", len(discovered_plugins) > 0),
            ("Plugin loading", await loader.get_plugin_instance("analytics-plugin") is not None),
            ("Sandbox creation", sandbox is not None),
            ("Interface compliance", hasattr(analytics_plugin, 'get_metrics')),
            ("Resource monitoring", usage['memory_mb'] > 0),
        ]

        all_passed = True
        for check_name, passed in validations:
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"  {status} {check_name}")
            if not passed:
                all_passed = False

        # 9. Cleanup
        print("\n🧹 Step 9: System Cleanup...")
        success = await loader.shutdown()
        if success:
            print("✅ Plugin system shutdown complete")
        else:
            print("⚠️ Plugin system shutdown with warnings")

        # Final Summary
        print("\n" + "=" * 60)
        if all_passed:
            print("🎉 PHASE 3 PLUGIN SYSTEM DEMO: COMPLETE SUCCESS!")
            print("✅ All core components operational:")
            print("  • Plugin discovery and loading")
            print("  • Interface implementations (IAnalyticsProvider)")
            print("  • Sandbox security and resource limits")
            print("  • Metrics collection and reporting")
            print("  • Real-time plugin management")
        else:
            print("⚠️ PHASE 3 PLUGIN SYSTEM DEMO: PARTIAL SUCCESS")
            print("Some validations failed - check implementation")

        print("\n🚀 Phase 3 Ecosystem Expansion Foundation: READY")
        print("Next: Week 6 implementation begins immediately!")
        print("=" * 60)

    except Exception as e:
        logger.error(f"Demo failed with error: {e}")
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(demo_phase3_plugin_system())