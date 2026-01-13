# 🤖 Discord Integration Guide

## Overview

The Agent Cellphone V2 project includes comprehensive Discord integration for multi-agent communication and coordination. This guide explains how to set up and use the Discord infrastructure.

## 🛠️ Quick Setup

### Automated Setup (Recommended)

The Discord Manager tool automates the entire setup process:

```bash
# Run automated setup
python tools/discord_manager.py --setup

# Merge configuration into main .env file
python merge_discord_env.py

# Test the configuration
python discord_bot_test.py

# Test agent webhooks (including agent-7)
python test_agent7_webhook.py
```

### Manual Setup

If you prefer manual configuration:

1. Get your Discord bot token from https://discord.com/developers/applications
2. Set environment variable: `$env:DISCORD_BOT_TOKEN = "your_token"`
3. Run: `python tools/discord_manager.py --setup`

## 📊 What Gets Configured

The Discord Manager automatically creates:

### Channels
- 🏗️ `#infrastructure` - System infrastructure discussions
- 🏛️ `#architecture` - Architecture and design discussions
- 🤝 `#coordination` - General coordination
- 🐝 `#a2a-coordination` - Agent-to-agent coordination

### Agent Channels & Webhooks
- 🤖 `#agent-1` through `#agent-8` - Individual agent channels
- Webhooks for each agent channel for automated messaging

### Environment Variables
```env
DISCORD_BOT_TOKEN=your_bot_token
DISCORD_INFRASTRUCTURE_CHANNEL_ID=channel_id
DISCORD_ARCHITECTURE_CHANNEL_ID=channel_id
DISCORD_COORDINATION_CHANNEL_ID=channel_id
DISCORD_A2A_COORDINATION_CHANNEL_ID=channel_id
DISCORD_AGENT1_WEBHOOK_URL=webhook_url
DISCORD_AGENT2_WEBHOOK_URL=webhook_url
# ... through AGENT8_WEBHOOK_URL
```

## 🧪 Testing & Validation

### Comprehensive Test
```bash
python discord_bot_test.py
```
Validates all environment variables and Discord connectivity.

### Agent Webhook Test
```bash
python test_agent7_webhook.py
```
Tests webhook functionality for all agents, with special focus on agent-7.

### Token Check
```bash
python tools/discord_manager.py --check-token
```
Validates your Discord bot token format and permissions.

## 🔧 Discord Manager Tool

### Commands

```bash
# Automated setup (creates channels, webhooks, generates config)
python tools/discord_manager.py --setup

# Check token validity
python tools/discord_manager.py --check-token

# Generate config without connecting (if bot already exists)
python tools/discord_manager.py --config-only

# Custom token setup
python tools/discord_manager.py --token YOUR_TOKEN --setup
```

### Required Bot Permissions

Your Discord bot needs these permissions:
- ✅ Manage Channels
- ✅ Manage Webhooks
- ✅ Read Messages
- ✅ Send Messages
- ✅ Use Slash Commands

## 🤖 Agent Communication

### Webhook Usage

Each agent has a dedicated webhook for sending messages:

```python
import os
import requests

# Get agent webhook URL
webhook_url = os.getenv('DISCORD_AGENT7_WEBHOOK_URL')

# Send message
requests.post(webhook_url, json={
    "content": "Agent-7 reporting status",
    "embeds": [{
        "title": "Agent Status Update",
        "description": "Current operational status",
        "color": 0x00ff00
    }]
})
```

### Channel Structure

- **Agent-specific channels** (`#agent-N`): Individual agent communications
- **Coordination channels**: Multi-agent collaboration
- **Infrastructure channels**: System-level discussions

## 🔄 Maintenance

### Updating Configuration

If you need to recreate channels/webhooks:

```bash
# Backup current config
cp .env .env.backup

# Regenerate Discord setup
python tools/discord_manager.py --setup

# Merge new config
python merge_discord_env.py
```

### Adding More Agents

To support more than 8 agents, edit `tools/discord_manager.py`:

```python
# Change this range to support more agents
for i in range(1, 9):  # Currently 1-8, change to 1-16 for 16 agents
```

## 🚨 Troubleshooting

### Common Issues

1. **"No Discord token found"**
   - Set `DISCORD_BOT_TOKEN` environment variable
   - Or add to `.env` file
   - Or use `--token` parameter

2. **"Missing permissions"**
   - Ensure bot has required permissions in Discord Developer Portal
   - Re-invite bot with proper permissions

3. **Webhook tests fail**
   - Check webhook URLs are valid
   - Verify bot has webhook creation permissions
   - Test individual webhooks manually

4. **Channel creation fails**
   - Bot needs "Manage Channels" permission
   - Check server permissions and roles

### Debug Commands

```bash
# Check current environment
python check_discord_env.py

# Load and test Discord config
python load_and_test_discord.py

# Test specific agent webhook
python test_agent7_webhook.py
```

## 📋 Files Overview

- `tools/discord_manager.py` - Main Discord setup tool
- `discord_bot_test.py` - Comprehensive configuration validator
- `test_agent7_webhook.py` - Agent webhook tester
- `merge_discord_env.py` - Environment file merger
- `load_and_test_discord.py` - Environment loader and tester
- `check_discord_env.py` - Simple environment checker

## 🎯 Agent-7 Integration

Agent-7 is fully integrated with:
- ✅ Dedicated channel: `#agent-7`
- ✅ Functional webhook for messaging
- ✅ Environment variable: `DISCORD_AGENT7_WEBHOOK_URL`
- ✅ Swarm coordination capabilities

The system is now ready for multi-agent collaboration with agent-7 as an active participant.