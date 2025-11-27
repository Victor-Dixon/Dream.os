# Discord Bot Startup Guide

**Author**: Agent-3 (Infrastructure & DevOps)  
**Date**: 2025-01-27  
**Status**: ✅ Ready

---

## 🚀 **QUICK START**

### **1. Set Environment Variables**

The bot requires `DISCORD_BOT_TOKEN` to be set. You can either:

**Option A: Use .env file (Recommended)**
```bash
# Create .env file in project root
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_CHANNEL_ID=your_channel_id_here  # Optional
```

**Option B: Set in PowerShell (Windows)**
```powershell
$env:DISCORD_BOT_TOKEN="your_bot_token_here"
$env:DISCORD_CHANNEL_ID="your_channel_id_here"  # Optional
```

**Option C: Set in Command Prompt (Windows)**
```cmd
set DISCORD_BOT_TOKEN=your_bot_token_here
set DISCORD_CHANNEL_ID=your_channel_id_here  # Optional
```

---

### **2. Start the Bot**

**✅ RECOMMENDED: Unified Startup** (starts bot + queue processor):
```bash
python tools/start_discord_system.py
```
**This is the single source of truth for starting the Discord system!**

**Alternative Options** (if troubleshooting):
- **Standard Startup** (single run): `python scripts/start_discord_bot.py`
- **With Auto-Restart** (production): `python scripts/run_unified_discord_bot_with_restart.py`

**See**: `docs/infrastructure/DISCORD_SYSTEM_STARTUP_SSOT.md` for complete details.

---

## ✅ **VERIFICATION**

### **Check if Bot is Running**:
```powershell
Get-Process python | Where-Object {$_.CommandLine -like "*discord*"}
```

### **Check Environment Variables**:
```python
python -c "import os; print('Token:', 'SET' if os.getenv('DISCORD_BOT_TOKEN') else 'NOT SET')"
```

### **Expected Startup Messages**:
```
======================================================================
🚀 DISCORD BOT STARTUP
======================================================================
Python: 3.11.9
Discord.py: 2.5.2
Workspace: D:\Agent_Cellphone_V2_Repository\agent_workspaces
======================================================================

🚀 Starting Unified Discord Bot...
🐝 WE. ARE. SWARM.
🚀 Starting Discord Commander...
✅ Discord Commander Bot ready: BotName#1234
📊 Guilds: 1
🤖 Latency: 45.23ms
```

---

## 🐛 **TROUBLESHOOTING**

### **Issue: "DISCORD_BOT_TOKEN not set"**
**Solution**: Set the token in `.env` file or environment variable

### **Issue: "Invalid Discord token"**
**Solution**: 
1. Verify token is correct in Discord Developer Portal
2. Check token hasn't been regenerated
3. Ensure bot is invited to server with proper permissions

### **Issue: "Missing required intents"**
**Solution**: Enable these intents in Discord Developer Portal:
- MESSAGE CONTENT INTENT
- SERVER MEMBERS INTENT (if using member features)

### **Issue: Bot keeps restarting**
**Solution**: See `docs/infrastructure/DISCORD_BOT_RESTART_FIX.md`

---

## 📋 **REQUIREMENTS**

- Python 3.11+
- discord.py library: `pip install discord.py`
- python-dotenv (optional): `pip install python-dotenv`
- Valid Discord bot token
- Bot invited to Discord server

---

## 🎯 **COMMANDS**

Once bot is running, use these commands in Discord:

- `!control` or `!panel` - Open main control panel
- `!status` - View swarm status
- `!message <agent> <message>` - Send message to agent
- `!broadcast <message>` - Broadcast to all agents
- `!restart` - Restart bot (admin only)
- `!shutdown` - Shutdown bot (admin only)

---

## ✅ **STATUS**

**Startup Script**: ✅ Ready  
**Error Handling**: ✅ Implemented  
**Auto-Restart**: ✅ Available  
**Documentation**: ✅ Complete

---

**WE. ARE. SWARM. READY. 🐝⚡🔥**




