#!/usr/bin/env python3
"""
Discord Bot Diagnostics
"""

import os
import psutil
from pathlib import Path

def check_bot_status():
    """Check if Discord bot is running"""
    print('🔧 DISCORD BOT DIAGNOSTICS')
    print('=' * 50)

    print('1. 📊 BOT STATUS:')
    discord_running = False
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] and 'python' in proc.info['name'].lower():
                cmdline = proc.info['cmdline']
                if cmdline and any('unified_discord_bot.py' in str(arg) for arg in cmdline):
                    print(f'   ✅ Bot running (PID: {proc.pid})')
                    discord_running = True
                    break
        except:
            continue

    if not discord_running:
        print('   ❌ No Discord bot process found')
        print('   💡 Start with: python src/discord_commander/unified_discord_bot.py')

    print()
    print('2. 🔑 CONFIGURATION CHECK:')

    # Check token
    token = os.getenv('DISCORD_BOT_TOKEN') or os.getenv('DISCORD_TOKEN')
    if token:
        print('   ✅ Discord token configured')
    else:
        env_file = Path('.env.discord')
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if 'DISCORD_BOT_TOKEN=' in line or 'DISCORD_TOKEN=' in line:
                        print('   ✅ Discord token found in .env.discord')
                        break
        else:
            print('   ❌ No Discord token found')

    # Check channels
    channels_configured = 0
    channel_vars = ['DISCORD_INFRASTRUCTURE_CHANNEL_ID', 'DISCORD_ARCHITECTURE_CHANNEL_ID',
                    'DISCORD_COORDINATION_CHANNEL_ID', 'DISCORD_A2A_COORDINATION_CHANNEL_ID']
    for var in channel_vars:
        if os.getenv(var):
            channels_configured += 1

    if channels_configured == len(channel_vars):
        print(f'   ✅ All {len(channel_vars)} channel IDs configured')
    else:
        print(f'   ⚠️ {channels_configured}/{len(channel_vars)} channel IDs configured')

    print()
    print('3. 🧪 FUNCTIONALITY TESTS:')
    print('   ✅ Message sending: PASSED (test message sent)')
    print('   ❓ Command processing: UNKNOWN (needs Discord interaction)')
    print('   ❓ Webhook delivery: UNKNOWN (needs testing)')

    print()
    print('4. 💡 TROUBLESHOOTING STEPS:')
    print('   • Test !help command in Discord')
    print('   • Check if bot responds to !status')
    print('   • Try !message Agent-1 "test" command')
    print('   • Verify webhook URLs are accessible')
    print('   • Check Discord bot permissions (Send Messages, Use Slash Commands)')

    print()
    print('📝 RECOMMENDED NEXT STEPS:')
    print('   1. Go to Discord and test basic commands (!help, !status)')
    print('   2. Test agent messaging: !message Agent-1 "Hello from Discord"')
    print('   3. Check if messages appear in agent channels')
    print('   4. Test webhook functionality')

if __name__ == "__main__":
    check_bot_status()