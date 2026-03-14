#!/usr/bin/env python3
"""
Check Discord bot startup status
"""

import psutil
import os

print('🔍 DISCORD BOT STARTUP STATUS')
print('=' * 50)

# Check if bot is running
bot_running = False
for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
    try:
        if proc.info['name'] and 'python' in proc.info['name'].lower():
            cmdline = proc.info['cmdline']
            if cmdline and 'unified_discord_bot.py' in str(cmdline):
                bot_running = True
                print(f'✅ Bot is running (PID: {proc.pid})')
                break
    except:
        continue

if not bot_running:
    print('❌ Bot failed to start')
    exit(1)

# Check if environment variables are loaded
channel_vars = ['DISCORD_INFRASTRUCTURE_CHANNEL_ID', 'DISCORD_ARCHITECTURE_CHANNEL_ID',
                'DISCORD_COORDINATION_CHANNEL_ID', 'DISCORD_A2A_COORDINATION_CHANNEL_ID']

channels_loaded = sum(1 for var in channel_vars if os.getenv(var))
print(f'✅ Environment variables loaded: {channels_loaded}/{len(channel_vars)}')

if channels_loaded == len(channel_vars):
    print('🎉 SUCCESS: Bot restarted with full Discord configuration!')
    print('💡 Test commands in Discord: !help, !status')
    print('💡 Try: !message Agent-1 "test message"')
else:
    print('⚠️ WARNING: Some environment variables not loaded')
    print('🔧 The bot may not route messages correctly to agent channels')