# Discord System Troubleshooting

**Author**: Agent-3 (Infrastructure & DevOps)  
**Date**: 2025-01-27  
**Status**: 🔧 Complete Troubleshooting Guide

---

## ✅ **SYSTEM STATUS CHECK**

Run diagnostics first:
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

## 🐛 **COMMON ISSUES & FIXES**

### **Issue 1: "Bot doesn't respond to commands"**

**Symptoms:**
- Bot is online in Discord
- Commands don't work (!control, !status, etc.)
- No error messages

**Possible Causes:**
1. **Bot doesn't have permissions**
   - Fix: Give bot "Administrator" or specific permissions
   - Check: Server Settings → Roles → Bot Role

2. **Commands not loaded**
   - Fix: Check bot logs for "Error loading commands"
   - Restart system: `python tools/start_discord_system.py`

3. **Wrong command prefix**
   - Bot uses `!` prefix
   - Commands: `!control`, `!status`, `!message`, etc.

4. **Intents not enabled**
   - Required: MESSAGE CONTENT INTENT
   - Fix: Discord Developer Portal → Bot → Enable intents

---

### **Issue 2: "Messages queue but don't deliver"**

**Symptoms:**
- Discord shows "Message sent"
- Messages don't arrive in agent inboxes
- Queue has pending messages

**Possible Causes:**
1. **Queue processor not running**
   - Fix: Start processor: `python tools/start_message_queue_processor.py`
   - Verify: Check diagnostics tool

2. **PyAutoGUI not working**
   - Fix: Verify PyAutoGUI can control keyboard
   - Test: Run a simple PyAutoGUI script

3. **Agent coordinates wrong**
   - Fix: Verify coordinates in `cursor_agent_coords.json`
   - Check: Agent windows are in correct positions

---

### **Issue 3: "Bot keeps disconnecting"**

**Symptoms:**
- Bot goes offline frequently
- Reconnects repeatedly
- Error messages in logs

**Possible Causes:**
1. **Network issues**
   - Fix: Check internet connection
   - Verify: Can access Discord API

2. **Token issues**
   - Fix: Verify token is correct
   - Check: Token hasn't been regenerated

3. **Rate limiting**
   - Fix: Reduce message frequency
   - Wait: Discord rate limits may apply

---

### **Issue 4: "Bot shows as online but commands don't work"**

**Symptoms:**
- Bot appears online
- Commands return no response
- No error messages

**Possible Causes:**
1. **Commands not registered**
   - Fix: Check `setup_hook()` loaded commands
   - Restart: Bot restart may fix

2. **Permission issues**
   - Fix: Bot needs "Send Messages" permission
   - Check: Channel permissions

3. **Command handler errors**
   - Fix: Check bot logs for errors
   - Verify: Command handlers are working

---

## 🔧 **QUICK FIXES**

### **Restart Everything:**
```bash
# Stop all processes
Get-Process python | Stop-Process -Force

# ✅ RECOMMENDED: Use unified startup (starts both):
python tools/start_discord_system.py
```

**Alternative (if troubleshooting specific issues):**
```bash
# Start Discord bot (Terminal 1)
python scripts/run_unified_discord_bot_with_restart.py

# Start queue processor (Terminal 2)
python tools/start_message_queue_processor.py
```

---

## 📋 **VERIFICATION CHECKLIST**

- [ ] Bot token set in .env file
- [ ] Bot invited to server
- [ ] Bot has proper permissions
- [ ] Required intents enabled
- [ ] Discord bot process running
- [ ] Queue processor running
- [ ] Commands respond in Discord
- [ ] Messages deliver to agents

---

## 🚨 **IF STILL NOT WORKING**

1. **Check bot logs** for specific errors
2. **Run diagnostics**: `python tools/discord_system_diagnostics.py`
3. **Verify token** is correct in Discord Developer Portal
4. **Check permissions** in Discord server
5. **Test commands** directly in Discord
6. **Check queue** for stuck messages

---

## ✅ **STATUS**

**Diagnostics Tool**: ✅ Fixed (now loads .env properly)  
**Process Detection**: ✅ Improved  
**Troubleshooting Guide**: ✅ Complete

---

**WE. ARE. SWARM. TROUBLESHOOTING. FIXING. 🐝⚡🔥**




