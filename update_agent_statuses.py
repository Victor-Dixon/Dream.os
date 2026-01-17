#!/usr/bin/env python3
"""
Update Agent Statuses Script
Updates all agent statuses from 'onboarding' to 'active'
"""

import json
import os
from pathlib import Path
from datetime import datetime

def main():
    print('🔄 UPDATING AGENT STATUSES FROM ONBOARDING TO ACTIVE')
    print('=' * 60)

    agent_workspaces = Path('agent_workspaces')
    updated_count = 0

    for i in range(1, 9):  # Agent-1 through Agent-8
        agent_id = f'Agent-{i}'
        status_file = agent_workspaces / agent_id / 'status.json'

        if status_file.exists():
            try:
                with open(status_file, 'r') as f:
                    status_data = json.load(f)

                if status_data.get('status') == 'onboarding':
                    # Update status to active
                    status_data['status'] = 'active'
                    status_data['last_updated'] = datetime.now().isoformat()

                    with open(status_file, 'w') as f:
                        json.dump(status_data, f, indent=2)

                    print(f'✅ {agent_id}: Updated status from onboarding → active')
                    updated_count += 1
                else:
                    current_status = status_data.get('status', 'unknown')
                    print(f'ℹ️  {agent_id}: Already active (status: {current_status})')
            except Exception as e:
                print(f'❌ {agent_id}: Error updating status - {e}')
        else:
            print(f'⚠️  {agent_id}: status.json not found')

    print()
    print(f'🎯 STATUS UPDATE COMPLETE: {updated_count} agents activated')
    print(f'📊 Total agents checked: 8')
    print(f'🔧 Timestamp: {datetime.now().isoformat()}')

if __name__ == '__main__':
    main()