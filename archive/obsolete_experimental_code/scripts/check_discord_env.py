#!/usr/bin/env python3
"""Check Discord environment variables"""

import os

print('🔍 CURRENT ENVIRONMENT VARIABLES')
print('=' * 50)

discord_vars = {k: v for k, v in os.environ.items() if 'DISCORD' in k.upper()}
if discord_vars:
    print('\n📋 DISCORD VARIABLES FOUND:')
    for k, v in discord_vars.items():
        # Mask the token for security
        if 'TOKEN' in k.upper():
            display_value = v[:10] + '...' if len(v) > 10 else v
        else:
            display_value = v
        print(f'  {k} = {display_value}')
else:
    print('\n❌ NO DISCORD VARIABLES FOUND')
    print('\n💡 To set Discord token:')
    print('  $env:DISCORD_BOT_TOKEN = "your_token_here"')
    print('  # Then run: python tools/discord_manager.py --setup')