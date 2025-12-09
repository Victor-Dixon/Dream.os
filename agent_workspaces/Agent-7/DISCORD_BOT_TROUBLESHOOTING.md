# 🔧 Discord Bot Troubleshooting Guide

**Date**: 2025-12-06  
**Status**: ⚠️ **ISSUE IDENTIFIED - DISCORD_BOT_TOKEN NOT SET**

---

## 🚨 **PRIMARY ISSUE IDENTIFIED**

**Problem**: `DISCORD_BOT_TOKEN` environment variable is **NOT SET**

**Impact**: Bot cannot connect to Discord without a valid token

**Status**: 
- ❌ `DISCORD_BOT_TOKEN`: NOT SET
- ⚠️ `DISCORD_CHANNEL_ID`: NOT SET (optional)
- ✅ `discord.py`: Installed (version 2.5.2)

---

## 🔧 **TROUBLESHOOTING STEPS**

### **Step 1: Set Discord Bot Token**

**Option A: Using .env file (Recommended)**

1. Create or edit `.env` file in project root:
```env
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_CHANNEL_ID=your_channel_id_here
```

2. Make sure `.env` file is in project root (same directory as `src/`)

**Option B: Using Environment Variable (Windows PowerShell)**

```powershell
$env:DISCORD_BOT_TOKEN="your_bot_token_here"
$env:DISCORD_CHANNEL_ID="your_channel_id_here"
```

**Option C: Using Environment Variable (Windows CMD)**

```cmd
set DISCORD_BOT_TOKEN=your_bot_token_here
set DISCORD_CHANNEL_ID=your_channel_id_here
```

**Option D: Using Environment Variable (Linux/Mac)**

```bash
export DISCORD_BOT_TOKEN="your_bot_token_here"
export DISCORD_CHANNEL_ID="your_channel_id_here"
```

---

### **Step 2: Get Discord Bot Token**

1. Go to https://discord.com/developers/applications
2. Select your application (or create a new one)
3. Go to **Bot** section
4. Click **Reset Token** or **Copy** to get your token
5. **IMPORTANT**: Keep token secret - never commit to git!

---

### **Step 3: Verify Token is Set**

Run this command to verify:
```bash
python -c "import os; print('Token set:', 'YES' if os.getenv('DISCORD_BOT_TOKEN') else 'NO')"
```

---

### **Step 4: Check Bot Permissions**

In Discord Developer Portal:
1. Go to **Bot** section
2. Enable these **Privileged Gateway Intents**:
   - ✅ **MESSAGE CONTENT INTENT** (Required)
   - ✅ **SERVER MEMBERS INTENT** (Optional but recommended)
   - ✅ **PRESENCE INTENT** (Optional)

---

### **Step 5: Invite Bot to Server**

1. Go to **OAuth2** → **URL Generator**
2. Select scopes:
   - ✅ `bot`
   - ✅ `applications.commands` (for slash commands)
3. Select bot permissions:
   - ✅ Send Messages
   - ✅ Read Message History
   - ✅ Use Slash Commands
   - ✅ Embed Links
   - ✅ Attach Files
4. Copy the generated URL and open in browser
5. Select your server and authorize

---

### **Step 6: Start the Bot**

**Option A: Using the runner script (Recommended)**
```bash
python tools/run_unified_discord_bot_with_restart.py
```

**Option B: Direct execution**
```bash
python src/discord_commander/unified_discord_bot.py
```

**Option C: Debug instance (for testing)**
```bash
python tools/test_discord_bot_debug.py
```

---

## 🔍 **COMMON ERRORS & SOLUTIONS**

### **Error: "DISCORD_BOT_TOKEN not set in environment!"**

**Solution**: Set the token using one of the methods in Step 1

---

### **Error: "Invalid Discord token"**

**Causes**:
- Token is incorrect or expired
- Token was reset in Discord Developer Portal
- Token has extra spaces or characters

**Solution**:
1. Get a fresh token from Discord Developer Portal
2. Make sure there are no extra spaces
3. Update `.env` file or environment variable

---

### **Error: "Missing required intents"**

**Solution**: Enable **MESSAGE CONTENT INTENT** in Discord Developer Portal:
1. Go to https://discord.com/developers/applications
2. Select your application
3. Go to **Bot** section
4. Scroll to **Privileged Gateway Intents**
5. Enable **MESSAGE CONTENT INTENT**
6. Save changes
7. Restart bot

---

### **Error: "Bot is not in any guilds"**

**Solution**: Invite bot to your Discord server (see Step 5)

---

### **Error: "Connection timeout" or "Network error"**

**Causes**:
- Internet connection issue
- Discord API is down
- Firewall blocking connection

**Solution**:
1. Check internet connection
2. Check Discord status: https://discordstatus.com/
3. Check firewall settings
4. Bot will auto-reconnect (built-in retry logic)

---

### **Error: "ModuleNotFoundError: No module named 'discord'"**

**Solution**: Install discord.py:
```bash
pip install discord.py
```

---

## 📊 **VERIFICATION CHECKLIST**

Before starting the bot, verify:

- [ ] `DISCORD_BOT_TOKEN` is set in environment or `.env` file
- [ ] Token is valid (not expired, no extra spaces)
- [ ] **MESSAGE CONTENT INTENT** is enabled in Discord Developer Portal
- [ ] Bot is invited to your Discord server
- [ ] `discord.py` is installed (`pip install discord.py`)
- [ ] Bot has required permissions in server
- [ ] Internet connection is working

---

## 🚀 **QUICK START COMMANDS**

**1. Check current status:**
```bash
python -c "import os; print('Token:', 'SET' if os.getenv('DISCORD_BOT_TOKEN') else 'NOT SET')"
```

**2. Set token (Windows PowerShell):**
```powershell
$env:DISCORD_BOT_TOKEN="your_token_here"
```

**3. Start bot:**
```bash
python tools/run_unified_discord_bot_with_restart.py
```

---

## 📝 **NEXT STEPS**

1. ✅ **Set `DISCORD_BOT_TOKEN`** in `.env` file or environment variable
2. ✅ **Enable MESSAGE CONTENT INTENT** in Discord Developer Portal
3. ✅ **Invite bot to server** if not already done
4. ✅ **Start bot** using runner script
5. ✅ **Verify connection** - bot should appear online in Discord

---

**Status**: ⚠️ **WAITING FOR TOKEN CONFIGURATION**

🐝 **WE. ARE. SWARM. ⚡🔥**

