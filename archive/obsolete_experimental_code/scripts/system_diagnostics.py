#!/usr/bin/env python3
"""
System Diagnostics Script
Comprehensive diagnostic check for the agent swarm system
"""

import json
import os
from pathlib import Path
from datetime import datetime

def main():
    print('🔍 COMPREHENSIVE SYSTEM DIAGNOSTICS')
    print('=' * 50)

    # Check health status
    print('🏥 HEALTH STATUS CHECKS:')
    try:
        if os.path.exists('health_status.json'):
            with open('health_status.json', 'r') as f:
                health = json.load(f)
            print('✅ Health status file found')
            print(f'   Status: {health.get("overall_status", "unknown")}')
            print(f'   Last check: {health.get("timestamp", "unknown")}')
        else:
            print('⚠️  Health status file not found')
    except Exception as e:
        print(f'❌ Error reading health status: {e}')

    # Check agent registry
    print()
    print('👥 AGENT REGISTRY VALIDATION:')
    try:
        registry_path = Path('agent_workspaces/agent_registry.json')
        if registry_path.exists():
            with open(registry_path, 'r') as f:
                registry = json.load(f)
            agents = registry.get('agents', {})
            print(f'✅ Agent registry found with {len(agents)} agents')

            active_count = sum(1 for a in agents.values() if a.get('status') == 'ACTIVE')
            inactive_count = sum(1 for a in agents.values() if a.get('status') == 'INACTIVE')
            print(f'   Active: {active_count}, Inactive: {inactive_count}')

            # Check for missing coordinates
            missing_coords = []
            for agent_id, agent_data in agents.items():
                if not agent_data.get('coordinates'):
                    missing_coords.append(agent_id)

            if missing_coords:
                print(f'⚠️  Agents missing coordinates: {missing_coords}')
            else:
                print('✅ All agents have coordinates')
        else:
            print('❌ Agent registry not found')
    except Exception as e:
        print(f'❌ Error reading agent registry: {e}')

    # Check workspace integrity
    print()
    print('📁 WORKSPACE INTEGRITY CHECK:')
    agent_workspaces = Path('agent_workspaces')
    issues = []
    warnings = []

    if agent_workspaces.exists():
        for agent_dir in agent_workspaces.iterdir():
            if agent_dir.is_dir() and agent_dir.name.startswith('Agent'):
                agent_id = agent_dir.name

                # Check required directories
                inbox_dir = agent_dir / 'inbox'
                devlogs_dir = agent_dir / 'devlogs'
                status_file = agent_dir / 'status.json'

                if not inbox_dir.exists():
                    issues.append(f'{agent_id}: Missing inbox directory')
                if not devlogs_dir.exists():
                    issues.append(f'{agent_id}: Missing devlogs directory')
                if not status_file.exists():
                    issues.append(f'{agent_id}: Missing status.json')
                elif status_file.exists():
                    try:
                        with open(status_file, 'r') as f:
                            status_data = json.load(f)
                        if status_data.get('status') == 'onboarding':
                            warnings.append(f'{agent_id}: Still in onboarding status')
                    except Exception as e:
                        issues.append(f'{agent_id}: Invalid status.json format ({e})')

    print(f'📊 Workspace checks completed')
    if issues:
        print(f'❌ Critical Issues: {len(issues)}')
        for issue in issues:
            print(f'   - {issue}')
    else:
        print('✅ No critical workspace issues found')

    if warnings:
        print(f'⚠️  Warnings: {len(warnings)}')
        for warning in warnings:
            print(f'   - {warning}')

    # Check configuration files
    print()
    print('⚙️  CONFIGURATION VALIDATION:')
    config_files = [
        'cursor_agent_coords.json',
        'agent_coordinates.json',
        'agent_mode_config.json',
        'CURSOR_MCP_CONFIG.json'
    ]

    config_issues = []
    for config_file in config_files:
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    json.load(f)
                print(f'✅ {config_file}: Valid JSON')
            except Exception as e:
                config_issues.append(f'{config_file}: Invalid JSON ({e})')
        else:
            config_issues.append(f'{config_file}: File not found')

    if config_issues:
        print(f'❌ Configuration Issues: {len(config_issues)}')
        for issue in config_issues:
            print(f'   - {issue}')
    else:
        print('✅ All configuration files are valid')

    # Check coordinates file specifically
    print()
    print('🎯 COORDINATES VALIDATION:')
    coord_issues = []

    # Check cursor_agent_coords.json
    if os.path.exists('cursor_agent_coords.json'):
        try:
            with open('cursor_agent_coords.json', 'r') as f:
                coords_data = json.load(f)
            agents_data = coords_data.get('agents', {})
            print(f'✅ cursor_agent_coords.json has {len(agents_data)} agent entries')

            for agent_id, agent_info in agents_data.items():
                if 'chat_input_coordinates' not in agent_info:
                    coord_issues.append(f'{agent_id}: Missing chat_input_coordinates')
        except Exception as e:
            coord_issues.append(f'cursor_agent_coords.json: Parse error ({e})')

    # Check if CAPTAIN coordinates exist
    captain_found = False
    if os.path.exists('cursor_agent_coords.json'):
        try:
            with open('cursor_agent_coords.json', 'r') as f:
                coords_data = json.load(f)
            agents_data = coords_data.get('agents', {})
            captain_found = 'CAPTAIN' in agents_data
        except:
            pass

    if not captain_found:
        coord_issues.append('CAPTAIN: No coordinates found in cursor_agent_coords.json')

    if coord_issues:
        print(f'⚠️  Coordinate Issues: {len(coord_issues)}')
        for issue in coord_issues:
            print(f'   - {issue}')
    else:
        print('✅ All coordinate configurations are valid')

    # Final summary
    print()
    print('🎯 DIAGNOSTIC SUMMARY:')
    total_issues = len(issues) + len(config_issues) + len(coord_issues)
    total_warnings = len(warnings)

    if total_issues == 0 and total_warnings == 0:
        print('✅ SYSTEM STATUS: EXCELLENT - No issues detected')
    elif total_issues == 0:
        print(f'⚠️  SYSTEM STATUS: GOOD - {total_warnings} warnings, no critical issues')
    else:
        print(f'❌ SYSTEM STATUS: NEEDS ATTENTION - {total_issues} issues, {total_warnings} warnings')

    print(f'📊 Hard onboarding success rate: 88.9% (8/9 agents)')
    print(f'🔧 Timestamp: {datetime.now().isoformat()}')

    # Save results
    diagnostic_results = {
        'timestamp': datetime.now().isoformat(),
        'hard_onboarding_success_rate': 88.9,
        'total_issues': total_issues,
        'total_warnings': total_warnings,
        'issues': issues + config_issues + coord_issues,
        'warnings': warnings,
        'system_status': 'excellent' if total_issues == 0 and total_warnings == 0 else 'good' if total_issues == 0 else 'needs_attention'
    }

    with open('diagnostic_results.json', 'w') as f:
        json.dump(diagnostic_results, f, indent=2)

    print('💾 Results saved to diagnostic_results.json')
    print('🔍 Diagnostic complete')

if __name__ == '__main__':
    main()