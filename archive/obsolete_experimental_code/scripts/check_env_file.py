#!/usr/bin/env python3
"""
Check .env.discord file contents
"""

from pathlib import Path
import os

print('🔍 CHECKING .env.discord FILE')
print('=' * 50)

env_file = Path('.env.discord')
if env_file.exists():
    print('✅ .env.discord file exists')

    with open(env_file, 'r') as f:
        lines = f.readlines()
        print(f'Contains {len(lines)} lines')

        print()
        print('📋 FILE CONTENTS:')
        for i, line in enumerate(lines, 1):
            line = line.rstrip()
            if line:
                print("2d")

        print()
        print('🔍 CHANNEL ID ANALYSIS:')
        channel_lines = [line.strip() for line in lines if 'CHANNEL_ID=' in line]
        if channel_lines:
            print(f'✅ Found {len(channel_lines)} channel ID lines:')
            for line in channel_lines:
                print(f'   {line}')
        else:
            print('❌ No channel ID lines found in .env.discord')

        print()
        print('🔧 LOADING TEST:')
        # Load variables manually
        loaded_vars = 0
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                os.environ[key] = value
                loaded_vars += 1

        print(f'✅ Loaded {loaded_vars} environment variables')

        # Check channel availability
        channel_vars = ['DISCORD_INFRASTRUCTURE_CHANNEL_ID', 'DISCORD_ARCHITECTURE_CHANNEL_ID',
                        'DISCORD_COORDINATION_CHANNEL_ID', 'DISCORD_A2A_COORDINATION_CHANNEL_ID']

        loaded_channels = 0
        for var in channel_vars:
            if os.getenv(var):
                loaded_channels += 1

        print(f'✅ Channel IDs now available: {loaded_channels}/{len(channel_vars)}')

else:
    print('❌ .env.discord file does not exist')
    print('💡 Run: python tools/discord_manager.py --setup')