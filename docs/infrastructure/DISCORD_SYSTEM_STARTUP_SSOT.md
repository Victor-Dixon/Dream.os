# 🚀 Discord System Startup - Single Source of Truth

**Author**: Agent-3 (Infrastructure & DevOps)  
**Date**: 2025-01-27  
**Status**: ✅ **SSOT - PRIMARY STARTUP METHOD**  
**Priority**: CRITICAL

---

## 🎯 **SINGLE COMMAND TO START EVERYTHING**

```bash
python tools/start_discord_system.py
```

**This single command starts:**
1. ✅ Discord bot (with auto-restart)
2. ✅ Message queue processor
3. ✅ Process monitoring
4. ✅ Clean shutdown handling

---

## 📋 **WHAT THIS SCRIPT DOES**

### **Step 1: Token Check**
- Verifies `DISCORD_BOT_TOKEN` is set in `.env` file
- Validates token format
- Exits with helpful error if missing

### **Step 2: Start Discord Bot**
- Launches `scripts/run_unified_discord_bot_with_restart.py`
- Runs in background with auto-restart support
- Waits 3 seconds for initialization

### **Step 3: Start Queue Processor**
- Launches `tools/start_message_queue_processor.py`
- Runs in background to deliver queued messages
- Required for PyAutoGUI message delivery

### **Step 4: Monitor & Display**
- Shows process PIDs
- Monitors both processes
- Handles Ctrl+C for clean shutdown

---

## ✅ **REQUIREMENTS**

### **Environment Setup:**
1. **Discord Bot Token** in `.env` file:
   ```env
   DISCORD_BOT_TOKEN=your_token_here
   ```

2. **Python Dependencies:**
   ```bash
   pip install python-dotenv discord.py
   ```

3. **Discord Bot Invited** to server with proper permissions

---

## 🚀 **USAGE**

### **Start System:**
```bash
python tools/start_discord_system.py
```

### **Expected Output:**
```
======================================================================
🚀 STARTING COMPLETE DISCORD SYSTEM
======================================================================

✅ Discord bot token found
🚀 Starting Discord bot (with auto-restart)...
✅ Discord bot started (PID: 12345)
📬 Starting message queue processor...
✅ Queue processor started (PID: 12346)

======================================================================
✅ DISCORD SYSTEM STARTED
======================================================================
Discord Bot PID: 12345
Queue Processor PID: 12346

💡 To stop:
   Press Ctrl+C or kill the processes
======================================================================
```

### **Stop System:**
- Press `Ctrl+C` in the terminal
- Script will cleanly terminate both processes

---

## 🔄 **OLD WAY (DEPRECATED)**

**❌ DO NOT USE - Use unified script instead:**

```bash
# OLD WAY - Requires 2 separate commands:
python scripts/run_unified_discord_bot_with_restart.py  # Terminal 1
python tools/start_message_queue_processor.py            # Terminal 2
```

**✅ NEW WAY - Single command:**

```bash
# NEW WAY - One command starts both:
python tools/start_discord_system.py
```

---

## 📊 **VERIFICATION**

### **Check System Status:**
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

## 🐛 **TROUBLESHOOTING**

### **Issue: "DISCORD_BOT_TOKEN not set"**
**Fix:**
1. Create `.env` file in project root
2. Add: `DISCORD_BOT_TOKEN=your_token_here`
3. Run script again

### **Issue: "Bot process died"**
**Fix:**
1. Check bot logs for errors
2. Verify token is correct
3. Check Discord server permissions
4. Restart system: `python tools/start_discord_system.py`

### **Issue: "Queue processor not delivering messages"**
**Fix:**
1. Verify queue processor is running (check diagnostics)
2. Check PyAutoGUI can control keyboard
3. Verify agent coordinates are correct

**Full Troubleshooting Guide**: `docs/infrastructure/DISCORD_SYSTEM_TROUBLESHOOTING.md`

---

## 📝 **REFERENCE DOCUMENTATION**

- **Troubleshooting**: `docs/infrastructure/DISCORD_SYSTEM_TROUBLESHOOTING.md`
- **Bot Startup Guide**: `docs/infrastructure/DISCORD_BOT_STARTUP_GUIDE.md`
- **Queue Processor**: `docs/infrastructure/MESSAGE_QUEUE_PROCESSOR_GUIDE.md`
- **Diagnostics Tool**: `tools/discord_system_diagnostics.py`

---

## 🎯 **KEY POINTS**

1. ✅ **Single Command**: One script starts everything
2. ✅ **Auto-Restart**: Bot automatically restarts on crashes
3. ✅ **Process Monitoring**: Script monitors both processes
4. ✅ **Clean Shutdown**: Ctrl+C terminates both cleanly
5. ✅ **Token Validation**: Checks token before starting
6. ✅ **Background Processes**: Both run in background

---

## 🚨 **IMPORTANT NOTES**

- **This is the SSOT** for starting the Discord system
- **All other startup methods are deprecated**
- **Always use this script** unless troubleshooting specific issues
- **Script handles both processes** - no need for separate terminals

---

## ✅ **STATUS**

**Script**: ✅ `tools/start_discord_system.py`  
**Status**: ✅ **SSOT - PRIMARY STARTUP METHOD**  
**Last Updated**: 2025-01-27  
**Maintained By**: Agent-3 (Infrastructure & DevOps)

---

**🐝 WE. ARE. SWARM. ⚡🔥**

**Use this single command to start the complete Discord system!**

