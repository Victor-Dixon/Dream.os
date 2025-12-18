#!/usr/bin/env python3
"""
Test script for main.py agent mode integration
"""

import sys
import os
sys.path.insert(0, '.')

from main import ServiceManager

def test_agent_mode_integration():
    """Test that agent mode integration works."""
    print("Testing main.py agent mode integration...")

    # Test agent mode display
    manager = ServiceManager()
    success = manager.setup_agent_mode_manager()

    if success and manager.agent_mode_manager:
        current_mode = manager.agent_mode_manager.get_current_mode()
        active_agents = manager.agent_mode_manager.get_active_agents()
        monitor_setup = manager.agent_mode_manager.get_monitor_setup()

        print('🚀 AGENT CELLPHONE V2 - SERVICE LAUNCHER')
        print('=' * 60)
        print(f'Agent Mode: {current_mode} ({len(active_agents)} agents, {monitor_setup} monitor)')
        print(f'Active Agents: {", ".join(active_agents)}')
        print()
        print('✅ Agent mode integration working!')

        # Test mode selection (non-interactive)
        print("\n🔧 Testing mode selection display...")
        manager.select_agent_mode()  # This will show the menu but fail on input

    else:
        print('❌ Agent mode manager not available')
        return False

    return True

if __name__ == "__main__":
    test_agent_mode_integration()
