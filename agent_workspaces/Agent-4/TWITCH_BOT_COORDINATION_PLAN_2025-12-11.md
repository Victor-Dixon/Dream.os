# Twitch Bot Coordination Plan

**Agent:** Agent-4 (Captain)  
**Date:** 2025-12-11  
**Priority:** HIGH  
**Status:** ACTIVE

---

## 📊 CURRENT STATUS SUMMARY

### **Bot Status: RUNNING BUT NOT CONNECTING** 🔴

**Last Update:** 2025-12-09 (Agent-1)  
**Current Issue:** Connection disconnects after ~8 seconds

---

## 🔍 ISSUE ANALYSIS

### **1. Connection Issue** (PRIMARY BLOCKER)

**Symptoms:**
- ✅ Bot process starts successfully
- ✅ Configuration valid
- ✅ Password/OAuth token set correctly (`oauth:czs1fnkyh4633a...`)
- ✅ Connection attempt returns `True`
- ❌ Bot disconnects after ~8 seconds
- ❌ No "Improperly formatted auth" error (good sign)
- ❌ Connection reset: "Connection reset by peer"
- ❌ `bridge.connected` remains `False`
- ❌ Never receives `on_welcome` event

**Possible Causes:**
1. **OAuth token invalid** (even though no explicit error)
2. **IRC library not sending PASS command correctly**
3. **Twitch silently rejecting connection**
4. **Network/firewall blocking IRC connection**

---

### **2. Callback/Message Handling Issue** (SECONDARY)

**Symptoms:**
- ✅ Messages ARE being received (`on_pubmsg` called)
- ❌ Callback doesn't execute or fails silently
- ❌ No response to `!status` command

**Possible Causes:**
1. Event loop not running
2. Silent exception in callback
3. Status reader not initialized
4. Message interpreter issue

---

## 📋 COMPONENTS IDENTIFIED

### **Core Files:**
1. `src/services/chat_presence/twitch_bridge.py` - Twitch IRC bridge (203 lines)
2. `src/services/chat_presence/chat_presence_orchestrator.py` - Main orchestrator
3. `tools/chat_presence_cli.py` - CLI launcher
4. `tools/START_CHAT_BOT_NOW.py` - Quick start script
5. `tools/debug_twitch_bot.py` - Debug tool
6. `config/chat_presence.json` - Config file

### **Monitoring Tools:**
- `tools/monitor_twitch_bot.py` - Domain-specific Twitch monitoring
- `tools/check_twitch_bot_live_status.py` - Live status checker
- ✅ Verified: NOT covered by unified_monitor.py (IRC protocol-specific)
- ✅ Recommendation: KEEP SEPARATE (Agent-1, 2025-12-10)

---

## 🎯 RESOLUTION PLAN

### **Phase 1: Connection Diagnostics** (URGENT)

**Owner:** Agent-1 (Integration & Core Systems)

**Actions:**
1. ✅ **Verify OAuth Token:**
   - Check token validity at https://twitchapps.com/tmi/
   - Confirm token is not expired
   - Verify token has correct scopes

2. ✅ **Check Twitch Chat:**
   - See if bot appears in chat at all during the 8-second window
   - Verify bot username in Twitch chat

3. ✅ **Enhanced Logging:**
   - Add detailed IRC protocol logging
   - Log all IRC NOTICE messages
   - Capture connection handshake sequence

4. ✅ **Manual IRC Test:**
   - Test connecting with IRC client (HexChat, mIRC) using same token
   - Verify token works outside of bot code
   - Isolate whether issue is token or code

**Deliverables:**
- Token verification report
- IRC protocol log analysis
- Manual test results

---

### **Phase 2: Connection Fix** (HIGH)

**Owner:** Agent-1 (Integration & Core Systems)

**Actions:**
1. **Fix Connection Handshake:**
   - Verify PASS command is sent correctly
   - Check CAP negotiation (if required)
   - Ensure proper IRC protocol sequence

2. **Fix OAuth Token Handling:**
   - Verify token format (`oauth:` prefix)
   - Check token is sent in PASS command
   - Ensure token is set before connection

3. **Add Connection Retry Logic:**
   - Implement exponential backoff
   - Add reconnection on disconnect
   - Log reconnection attempts

**Deliverables:**
- Connection fix implementation
- Connection stability test results
- Reconnection logic verified

---

### **Phase 3: Message Handling Fix** (MEDIUM)

**Owner:** Agent-2 (Architecture & Design) / Agent-1

**Actions:**
1. **Fix Event Loop:**
   - Verify event loop is running correctly
   - Ensure callbacks are scheduled properly
   - Add event loop health checks

2. **Fix Callback Execution:**
   - Add exception handling in callbacks
   - Log all callback execution attempts
   - Verify status reader initialization

3. **Fix Message Interpreter:**
   - Verify `is_status_command` logic
   - Test command parsing
   - Add debug logging for message handling

**Deliverables:**
- Event loop fix
- Callback execution verified
- `!status` command working

---

## 🔧 TECHNICAL INVESTIGATION ITEMS

### **1. IRC Protocol Sequence**
```
[Client] → PASS oauth:TOKEN
[Client] → NICK BOT_USERNAME
[Server] → :tmi.twitch.tv 001 BOT_USERNAME :Welcome, GLHF!
[Server] → :tmi.twitch.tv 002 BOT_USERNAME :Your host is tmi.twitch.tv
[Server] → :tmi.twitch.tv 003 BOT_USERNAME :This server is rather new
[Server] → :tmi.twitch.tv 004 BOT_USERNAME :-
[Server] → :tmi.twitch.tv 375 BOT_USERNAME :-
[Server] → :tmi.twitch.tv 372 BOT_USERNAME :You are in a maze of twisty passages, all alike.
[Server] → :tmi.twitch.tv 376 BOT_USERNAME :>
[Client] → JOIN #CHANNEL
```

**Check:**
- Is PASS command sent before NICK?
- Are we waiting for 001 welcome message?
- Is JOIN command sent after welcome?

### **2. Token Verification Steps**
1. Visit https://twitchapps.com/tmi/
2. Generate new token if needed
3. Test token in IRC client
4. Verify token in bot config
5. Test bot connection with new token

### **3. Network/Firewall Checks**
- Check if IRC port (6667) is accessible
- Verify no firewall blocking outbound IRC
- Check if proxy/VPN is interfering

---

## 📨 COORDINATION ACTIONS

### **Immediate Actions:**

1. **Agent-1 Assignment:**
   - **Task:** Phase 1 Connection Diagnostics
   - **Priority:** URGENT
   - **ETA:** 1-2 hours
   - **Deliverables:** Token verification, IRC logs, manual test results

2. **Agent-2 Coordination:**
   - **Task:** Review message handling architecture
   - **Priority:** MEDIUM
   - **ETA:** After Phase 1 complete
   - **Deliverables:** Event loop analysis, callback fix

3. **Agent-3 Monitoring:**
   - **Task:** Verify monitoring tools operational
   - **Priority:** LOW
   - **Status:** ✅ Already verified (2025-12-10)

---

## 🚨 BLOCKERS IDENTIFIED

### **Blocker 1: Connection Issue** 🔴 HIGH
- **Status:** ACTIVE
- **Owner:** Agent-1
- **Impact:** Bot cannot connect to Twitch IRC
- **Resolution:** Phase 1 diagnostics → Phase 2 fix

### **Blocker 2: Message Handling** 🟡 MEDIUM
- **Status:** ACTIVE (may be dependent on connection)
- **Owner:** Agent-1 / Agent-2
- **Impact:** Bot doesn't respond to commands
- **Resolution:** Phase 3 fix (after connection working)

---

## ✅ SUCCESS CRITERIA

### **Phase 1 Complete:**
- [ ] OAuth token verified valid
- [ ] IRC protocol logs captured
- [ ] Manual IRC test completed
- [ ] Root cause identified

### **Phase 2 Complete:**
- [ ] Bot connects successfully
- [ ] Connection remains stable (>5 minutes)
- [ ] `on_welcome` event received
- [ ] `bridge.connected` = `True`

### **Phase 3 Complete:**
- [ ] `!status` command responds
- [ ] Messages trigger callbacks
- [ ] Event loop running correctly
- [ ] All bot commands functional

---

## 📝 NEXT STEPS

1. **Send coordination message to Agent-1:**
   - Assign Phase 1 Connection Diagnostics
   - Provide investigation checklist
   - Request status update

2. **Monitor progress:**
   - Check Agent-1 status updates
   - Review diagnostic results
   - Coordinate Phase 2 fix

3. **Update coordination status:**
   - Document findings
   - Update blocker status
   - Report resolution progress

---

**🐝 WE. ARE. SWARM. ⚡🔥**



