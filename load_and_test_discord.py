#!/usr/bin/env python3
"""Load Discord environment variables and run test"""

import os
import re

def load_env_file(filepath):
    """Load environment variables from a file"""
    if not os.path.exists(filepath):
        print(f"❌ Environment file not found: {filepath}")
        return False

    try:
        with open(filepath, 'r') as f:
            content = f.read()

        # Parse and set environment variables
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                # Handle both KEY=value and KEY="value" formats
                match = re.match(r'^([^=]+)=(.*)$', line)
                if match:
                    key, value = match.groups()
                    key = key.strip()

                    # Remove quotes if present
                    value = value.strip()
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]

                    os.environ[key] = value
                    print(f"✅ Loaded: {key}")

        return True

    except Exception as e:
        print(f"❌ Error loading environment file: {e}")
        return False

# Load the Discord environment file
print('🔧 LOADING DISCORD ENVIRONMENT VARIABLES')
print('=' * 50)

env_file = '.env.discord'
if load_env_file(env_file):
    print(f'\n✅ Successfully loaded environment from {env_file}')
else:
    print(f'\n❌ Failed to load environment from {env_file}')
    exit(1)

# Now run the test
print('\n🤖 RUNNING DISCORD ENVIRONMENT TEST')
print('=' * 50)

# Required environment variables
required_vars = [
    'DISCORD_BOT_TOKEN',
    'DISCORD_INFRASTRUCTURE_CHANNEL_ID',
    'DISCORD_ARCHITECTURE_CHANNEL_ID',
    'DISCORD_COORDINATION_CHANNEL_ID',
    'DISCORD_A2A_COORDINATION_CHANNEL_ID',
    'DISCORD_AGENT1_WEBHOOK_URL',
    'DISCORD_AGENT2_WEBHOOK_URL',
    'DISCORD_AGENT3_WEBHOOK_URL',
    'DISCORD_AGENT4_WEBHOOK_URL'
]

all_present = True
for var in required_vars:
    value = os.getenv(var)
    if value:
        # Mask sensitive values
        if 'TOKEN' in var:
            display_value = value[:10] + '...' + value[-5:] if len(value) > 15 else value
        elif 'WEBHOOK' in var:
            display_value = value[:30] + '...' if len(value) > 30 else value
        else:
            display_value = value
        print(f'✅ {var}: {display_value}')
    else:
        print(f'❌ {var}: MISSING')
        all_present = False

print()
if all_present:
    print('🎉 SUCCESS! All Discord environment variables are configured!')
    print('✅ Your Discord bot test should now pass')
    print('\n📝 Next steps:')
    print('1. Copy the variables from .env.discord to your main .env file')
    print('2. Or load .env.discord in your application startup')
    print('3. Test your Discord bot integration')
else:
    print('⚠️ Some environment variables are still missing')
    print('💡 Run: python tools/discord_manager.py --setup')