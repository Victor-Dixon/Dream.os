# Discord System Fix Guide

**Author**: Agent-3 (Infrastructure & DevOps)  
**Date**: 2025-01-27  
**Status**: 🔧 Troubleshooting Guide

---

## 🚨 **CRITICAL ISSUES IDENTIFIED**

Diagnostics found 3 critical issues preventing Discord system from working:

1. **❌ DISCORD_BOT_TOKEN NOT SET** - Bot cannot connect without token
2. **❌ Discord Bot Process NOT RUNNING** - Bot needs to be started
3. **❌ Queue Processor NOT RUNNING** - Messages won't be delivered

---

## 🔧 **FIX STEPS**

### **Step 1: Set Discord Bot Token**

**Option A: Add to .env file (Recommended)**
```bash
# Edit .env file and add:
DISCORD_BOT_TOKEN=your_actual_bot_token_here
DISCORD_CHANNEL_ID=your_channel_id_here  # Optional
```

**Option B: Set in PowerShell (Temporary)**
```powershell
$env:DISCORD_BOT_TOKEN="your_actual_bot_token_here"
$env:DISCORD_CHANNEL_ID="your_channel_id_here"  # Optional
```

**Where to get token:**
1. Go to https://discord.com/developers/applications
2. Select your bot application
3. Go to "Bot" section
4. Click "Reset Token" or "Copy" to get token
5. **Keep token secret!**

---

### **Step 2: Start Discord Bot**

```bash
python scripts/start_discord_bot.py
```

**Expected output:**
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

### **Step 3: Start Queue Processor**

**In a separate terminal/process:**
```bash
python tools/start_message_queue_processor.py
```

**Expected output:**
```
🚀 Starting Message Queue Processor...
📬 This will process queued messages and deliver them via PyAutoGUI
🛑 Press Ctrl+C to stop

🔄 Message queue processor started
```

---

## ✅ **VERIFICATION**

### **Run Diagnostics:**
```bash
python tools/discord_system_diagnostics.py
```

**All should show ✅:**
- ✅ Discord Bot Token: SET
- ✅ Discord.py Library: INSTALLED
- ✅ Discord Bot Process: RUNNING
- ✅ Queue Processor: RUNNING
- ✅ Message Queue: EXISTS

---

## 🐛 **COMMON ISSUES**

### **Issue: "Invalid Discord token"**
**Causes:**
- Token is incorrect
- Token was regenerated
- Token has extra spaces/quotes

**Fix:**
1. Get fresh token from Discord Developer Portal
2. Ensure no quotes around token in .env
3. Ensure no trailing spaces

---

### **Issue: "Missing required intents"**
**Causes:**
- Bot needs MESSAGE CONTENT INTENT
- Bot needs SERVER MEMBERS INTENT (if using member features)

**Fix:**
1. Go to Discord Developer Portal
2. Select your bot application
3. Go to "Bot" section
4. Enable "MESSAGE CONTENT INTENT"
5. Enable "SERVER MEMBERS INTENT" (if needed)
6. Save changes

---

### **Issue: "Bot process not running"**
**Causes:**
- Process crashed
- Process was stopped
- Token validation failed

**Fix:**
1. Check if token is set correctly
2. Restart bot: `python scripts/start_discord_bot.py`
3. Check for error messages in output

---

### **Issue: "Queue processor not running"**
**Causes:**
- Process crashed
- Process was stopped
- Import errors

**Fix:**
1. Check for error messages
2. Restart processor: `python tools/start_message_queue_processor.py`
3. Verify all dependencies installed

---

## 📋 **REQUIREMENTS CHECKLIST**

- [ ] Discord bot token set in .env or environment
- [ ] discord.py library installed (`pip install discord.py`)
- [ ] Bot invited to Discord server
- [ ] Bot has proper permissions
- [ ] Required intents enabled in Discord Developer Portal
- [ ] Discord bot process running
- [ ] Queue processor running
- [ ] PyAutoGUI working (for message delivery)

---

## 🚀 **QUICK START COMMANDS**

```bash
# 1. Set token (if not in .env)
$env:DISCORD_BOT_TOKEN="your_token"

# 2. Start Discord bot (Terminal 1)
python scripts/start_discord_bot.py

# 3. Start queue processor (Terminal 2)
python tools/start_message_queue_processor.py

# 4. Verify (Terminal 3)
python tools/discord_system_diagnostics.py
```

---

## ✅ **STATUS**

**Diagnostics Tool**: ✅ Created  
**Fix Guide**: ✅ Complete  
**Next Steps**: Set token and start both processes

---

**WE. ARE. SWARM. FIXING. TROUBLESHOOTING. 🐝⚡🔥**




