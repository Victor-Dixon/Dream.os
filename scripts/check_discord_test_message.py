#!/usr/bin/env python3
"""Check Discord test message in message history."""

import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

history_file = project_root / "data" / "message_history.json"

if not history_file.exists():
    print("❌ Message history file not found")
    sys.exit(1)

with open(history_file, encoding="utf-8") as f:
    data = json.load(f)

messages = data.get("messages", [])
print(f"Total messages in history: {len(messages)}")

# Find recent messages (last 5)
recent = messages[-5:] if len(messages) >= 5 else messages
print("\n📨 Recent messages:")
for i, msg in enumerate(recent, 1):
    print(f"\n{i}. From: {msg.get('from', 'N/A')}")
    print(f"   To: {msg.get('to', 'N/A')}")
    print(f"   Content: {msg.get('content', 'N/A')[:50]}...")
    print(f"   Source: {msg.get('source', 'N/A')}")
    print(f"   Discord Username: {msg.get('discord_username', 'N/A')}")
    print(f"   Discord User ID: {msg.get('discord_user_id', 'N/A')}")
    print(f"   Timestamp: {msg.get('timestamp', 'N/A')}")

# Check for Discord messages specifically
discord_messages = [
    m for m in messages
    if m.get('source') == 'discord' or 'discord' in str(m.get('from', '')).lower()
]
print(f"\n🔍 Discord messages found: {len(discord_messages)}")
if discord_messages:
    print("\nRecent Discord messages:")
    for i, msg in enumerate(discord_messages[-3:], 1):
        print(f"\n{i}. From: {msg.get('from', 'N/A')}")
        print(f"   Discord Username: {msg.get('discord_username', 'N/A')}")
        print(f"   Discord User ID: {msg.get('discord_user_id', 'N/A')}")
        print(f"   Content: {msg.get('content', 'N/A')[:50]}...")




