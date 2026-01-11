#!/usr/bin/env python3
"""Test OT integration for configuration and task management systems."""

from src.services.messaging.phase5_integration import enable_phase5_system, get_phase5_status

def main():
    print("🧪 Testing OT Integration for Configuration and Task Management...")
    print("=" * 60)

    print("\nEnabling configuration OT...")
    config_success = enable_phase5_system('configuration')
    print(f"Configuration OT: {'✅ ENABLED' if config_success else '❌ FAILED'}")

    print("\nEnabling task_management OT...")
    task_success = enable_phase5_system('task_management')
    print(f"Task Management OT: {'✅ ENABLED' if task_success else '❌ FAILED'}")

    # Get overall status
    status = get_phase5_status()
    print(f"\n📊 Overall Status: {status['overall_progress']}")
    print(f"Phase: {status['phase']}")

    print("\nOT Enabled Systems:")
    for system, enabled in status['ot_enabled_systems'].items():
        status_indicator = "✅" if enabled else "❌"
        print(f"  {status_indicator} {system}: {status['integration_status'].get(system, 'unknown')}")

    print("\n✅ OT integration test completed!")

if __name__ == '__main__':
    main()