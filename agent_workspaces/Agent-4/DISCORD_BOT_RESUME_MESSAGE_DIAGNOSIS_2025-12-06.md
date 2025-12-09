# 🔍 Discord Bot Resume Message Diagnosis

**Date**: 2025-12-06  
**Agent**: Agent-4 (Captain - Strategic Oversight)  
**Issue**: Discord bot not sending resume messages to stalled agents  
**Status**: 🔍 **DIAGNOSING**

---

## 🐛 **ISSUE REPORTED**

**User Report**: "the discord bot is suppose to send resume messages to stalled agents thats not working"

**Expected Behavior**: Discord bot should automatically detect stalled agents and send resume messages via PyAutoGUI to chat input coordinates.

---

## 🔍 **DIAGNOSIS CHECKLIST**

### **1. Status Monitor Running?** ⏳
- [ ] Check if `monitor_status_changes` loop is running
- [ ] Verify bot is started and monitor auto-started
- [ ] Check Discord bot logs for monitor startup messages

### **2. Inactivity Detection Working?** ⏳
- [ ] Verify `_inactivity_check_counter` is initialized correctly
- [ ] Check if counter reaches 20 iterations (5 minutes)
- [ ] Verify `_check_inactivity()` is being called

### **3. Activity Detector Working?** ⏳
- [ ] Verify `AgentActivityDetector` is imported successfully
- [ ] Check if `detect_agent_activity()` returns correct results
- [ ] Verify inactivity threshold (5 minutes) is being checked

### **4. Resume Message Sending?** ⏳
- [ ] Check if `_send_resume_message_to_agent()` is being called
- [ ] Verify `send_message()` from `messaging_core` is working
- [ ] Check for errors in resume message sending
- [ ] Verify PyAutoGUI delivery is enabled

### **5. Error Handling?** ⏳
- [ ] Check for silent failures in exception handlers
- [ ] Verify error logging is working
- [ ] Check Discord bot logs for errors

---

## 📋 **CODE ANALYSIS**

### **Status Monitor Setup** (`unified_discord_bot.py`):
```python
# Line 239-267: Auto-start in on_ready()
self.status_monitor = setup_status_monitor(self, self.channel_id, scheduler=scheduler)
if hasattr(self.status_monitor, 'start_monitoring'):
    self.status_monitor.start_monitoring()
```

### **Monitor Loop** (`status_change_monitor.py`):
```python
# Line 91-92: Runs every 15 seconds
@tasks.loop(seconds=15)
async def monitor_status_changes(self):
```

### **Inactivity Check Counter** (Lines 140-162):
```python
# Should check every 20 iterations (5 minutes)
if activity_detector:
    if not hasattr(self, '_inactivity_check_counter'):
        self._inactivity_check_counter = {}
    if agent_id not in self._inactivity_check_counter:
        self._inactivity_check_counter[agent_id] = 0
    
    self._inactivity_check_counter[agent_id] += 1
    if self._inactivity_check_counter[agent_id] >= 20:  # 5 minutes
        self._inactivity_check_counter[agent_id] = 0
        await self._check_inactivity(agent_id, activity_detector)
```

### **Resume Message Sending** (Lines 432-521):
```python
async def _send_resume_message_to_agent(self, agent_id: str, prompt: str, summary, skip_wrapper: bool = False):
    # Uses send_message() from messaging_core
    success = send_message(
        content=resume_message,
        sender="Status Monitor",
        recipient=agent_id,
        message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,
        priority=UnifiedMessagePriority.URGENT,
        tags=[UnifiedMessageTag.CAPTAIN],
    )
```

---

## 🚨 **POTENTIAL ISSUES**

### **Issue 1: Monitor Not Running**
**Symptoms**: No resume messages sent, no activity detection
**Check**: Verify `monitor_status_changes.is_running()` returns `True`
**Fix**: Ensure monitor auto-starts in `on_ready()`

### **Issue 2: Inactivity Counter Not Incrementing**
**Symptoms**: Counter never reaches 20, `_check_inactivity()` never called
**Check**: Verify counter initialization and increment logic
**Fix**: Ensure counter is properly initialized per agent

### **Issue 3: Activity Detector Not Detecting Stalls**
**Symptoms**: Activity detector returns false positives (agents not actually stalled)
**Check**: Verify `detect_agent_activity()` logic and thresholds
**Fix**: Review activity detection logic

### **Issue 4: Resume Message Sending Failing Silently**
**Symptoms**: `_check_inactivity()` called but no messages sent
**Check**: Verify `send_message()` success/failure handling
**Fix**: Add better error logging and retry logic

### **Issue 5: PyAutoGUI Delivery Not Working**
**Symptoms**: Messages queued but not delivered to chat input coordinates
**Check**: Verify PyAutoGUI mode is enabled in `send_message()`
**Fix**: Ensure `use_pyautogui=True` is set

---

## 🔧 **DIAGNOSTIC STEPS**

### **Step 1: Check Monitor Status**
```python
# In Discord: !monitor status
# Should show: "🟢 RUNNING - Auto-starts with bot"
```

### **Step 2: Check Bot Logs**
```bash
# Look for:
# "✅ Status change monitor started and running automatically"
# "✅ Status change monitor started"
# Any errors in monitor loop
```

### **Step 3: Test Inactivity Detection**
```python
# Manually trigger inactivity check
# Check if counter reaches 20
# Verify _check_inactivity() is called
```

### **Step 4: Test Resume Message Sending**
```python
# Manually call _send_resume_message_to_agent()
# Verify send_message() is called
# Check for errors in message delivery
```

---

## 📊 **NEXT STEPS**

1. **Verify Monitor Running**: Check Discord bot logs and `!monitor status` command
2. **Check Inactivity Counter**: Verify counter logic is working correctly
3. **Test Activity Detection**: Manually test activity detector with known stalled agent
4. **Test Resume Sending**: Manually trigger resume message and verify delivery
5. **Fix Identified Issues**: Apply fixes based on diagnosis results

---

**Status**: 🔍 **DIAGNOSING**  
**Priority**: HIGH - Critical for agent recovery system

🐝 **WE. ARE. SWARM.** ⚡🔥

