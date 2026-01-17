#!/usr/bin/env python3
"""Test Discord environment variables after setup"""

import os

print('🤖 DISCORD ENVIRONMENT TEST')
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

print('🔍 CHECKING REQUIRED ENVIRONMENT VARIABLES')
print('-' * 50)

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
    print('🎉 ALL REQUIRED ENVIRONMENT VARIABLES ARE CONFIGURED!')
    print('✅ Discord bot test should now pass')
else:
    print('⚠️ SOME ENVIRONMENT VARIABLES ARE STILL MISSING')
    print('💡 Run: python tools/discord_manager.py --setup')