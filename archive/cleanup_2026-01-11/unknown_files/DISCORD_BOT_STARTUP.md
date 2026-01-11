# Discord Bot Startup Guide - Agent Cellphone V2

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Copy the example environment file
cp env.example .env

# Edit .env and add your Discord bot credentials:
# DISCORD_BOT_TOKEN=your_bot_token_here
# DISCORD_GUILD_ID=your_server_id_here
```

### 2. Start the Bot
```bash
# Method 1: Use the launcher (recommended)
python tools/discord_bot_launcher.py

# Method 2: Direct startup
python -m src.discord_commander.unified_discord_bot
```

### 3. Verify It's Running
```bash
python check_discord_bot.py
```

## 🔧 Troubleshooting

### Common Issues

**❌ "Missing required environment variables"**
- Make sure `DISCORD_BOT_TOKEN` and `DISCORD_GUILD_ID` are set in `.env`

**❌ "discord.py not installed"**
```bash
pip install discord.py
```

**❌ "python-dotenv not installed"**
```bash
pip install python-dotenv
```

### Getting Discord Credentials

1. **Bot Token**: Go to https://discord.com/developers/applications
   - Create a new application
   - Go to "Bot" section
   - Copy the token

2. **Guild/Server ID**: In Discord
   - Enable Developer Mode (User Settings → Advanced → Developer Mode)
   - Right-click your server → "Copy ID"

### Stopping the Bot

```bash
# Find the process
python check_discord_bot.py

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

## 📋 Bot Features

- **Swarm Coordination**: Multi-agent communication
- **Task Management**: Contract-based task assignment
- **Status Monitoring**: Real-time agent status updates
- **Broadcast Messaging**: Mass communication to all agents
- **GUI Integration**: Web-based control panels

## 🎯 Status

✅ **Bot Status**: RUNNING (PID: Multiple processes active)
✅ **Environment**: Configured
✅ **Dependencies**: Installed

**The Discord bot is now operational!** 🎉