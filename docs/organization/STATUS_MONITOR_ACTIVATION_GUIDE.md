# 📊 Status Monitor Resume Logic - Activation Guide

**Date**: 2025-12-02  
**Agent**: Agent-4 (Captain)  
**Status**: ✅ **RESUME LOGIC DEPLOYED**

---

## 🎯 **HOW IT WORKS**

The status monitor resume logic is **automatically activated** when the Discord bot starts. It runs in the background and checks for inactive agents every 5 minutes.

---

## ✅ **AUTOMATIC ACTIVATION**

### **When Discord Bot Starts**:
1. Bot connects to Discord
2. `on_ready()` event fires
3. Status monitor automatically starts (line 228-230 in `unified_discord_bot.py`)
4. Resume logic is active immediately

**No manual activation needed** - it starts automatically!

---

## 🔍 **VERIFY IT'S RUNNING**

### **Method 1: Discord Command** (Easiest)
```
!monitor status
```

**Response will show**:
- 🟢 **RUNNING** - Monitor is active
- 🔴 **STOPPED** - Monitor is not running
- Check interval: 15 seconds
- Tracked agents: X/8 agents

### **Method 2: Check Bot Logs**
Look for this message in Discord bot logs:
```
✅ Status change monitor started
```

### **Method 3: Check Bot Startup**
When bot starts, you should see:
```
✅ Discord Commander Bot ready: <bot_name>
✅ Status change monitor started
```

---

## 🚀 **MANUAL CONTROL** (If Needed)

### **Start Monitor**:
```
!monitor start
```

### **Stop Monitor**:
```
!monitor stop
```

### **Check Status**:
```
!monitor status
```

---

## ⏱️ **HOW RESUME LOGIC WORKS**

### **Timing**:
1. **Every 15 seconds**: Status monitor checks all agent `status.json` files
2. **Every 5 minutes** (20 iterations): Inactivity check runs
3. **If inactive 30+ minutes**: Resume message sent to agent

### **Resume Message Flow**:
1. **Detect Inactivity**: Agent inactive 30+ minutes
2. **Generate Resume Prompt**: Using `generate_optimized_resume_prompt()`
3. **Send to Agent**: Via messaging system (direct inbox/chat delivery)
4. **Post to Discord**: For visibility (status update channel)

---

## 📋 **REQUIREMENTS**

### **For Resume Logic to Work**:
1. ✅ **Discord Bot Running**: Bot must be connected
2. ✅ **Status Monitor Started**: Automatically on bot startup
3. ✅ **Agent Activity Detector**: Must be available (`tools/agent_activity_detector.py`)
4. ✅ **Resume Prompt Generator**: Must be available (`src/core/optimized_stall_resume_prompt.py`)
5. ✅ **Messaging System**: Must be operational

---

## 🔧 **TROUBLESHOOTING**

### **Monitor Not Starting**:
1. **Check Bot Logs**: Look for error messages
2. **Verify Discord Connection**: Bot must be connected
3. **Check Dependencies**: Ensure all imports work
4. **Manual Start**: Use `!monitor start` command

### **Resume Messages Not Sending**:
1. **Check Activity Detector**: Verify `agent_activity_detector.py` exists
2. **Check Resume Prompt Generator**: Verify `optimized_stall_resume_prompt.py` exists
3. **Check Messaging System**: Verify messaging system is operational
4. **Check Logs**: Look for error messages in bot logs

### **Monitor Stopped**:
1. **Restart Bot**: Use `!restart` command
2. **Manual Start**: Use `!monitor start` command
3. **Check Errors**: Review bot logs for issues

---

## 📊 **MONITORING STATUS**

### **What Gets Monitored**:
- Agent `status.json` file modification times
- Agent activity (via Activity Detector)
- Status changes (status, phase, mission, tasks)
- Inactivity duration

### **What Triggers Resume**:
- Agent inactive for **30+ minutes**
- No recent activity detected
- Status file not updated recently

---

## 🎯 **QUICK START**

### **To Activate Resume Logic**:
1. **Start Discord Bot**: 
   ```bash
   python tools/start_discord_system.py
   ```
2. **Verify Monitor Started**: 
   ```
   !monitor status
   ```
3. **Done!** Resume logic is now active

### **To Verify It's Working**:
1. Wait 5 minutes (inactivity check interval)
2. Check bot logs for inactivity checks
3. If agent inactive 30+ minutes, resume message will be sent

---

## 📝 **SUMMARY**

**Status Monitor Resume Logic**:
- ✅ **Automatically activated** when Discord bot starts
- ✅ **Runs in background** every 15 seconds
- ✅ **Checks inactivity** every 5 minutes
- ✅ **Sends resume messages** when agents inactive 30+ minutes
- ✅ **Posts to Discord** for visibility

**No manual activation needed** - just start the Discord bot!

---

**Guide Created**: 2025-12-02  
**Agent**: Agent-4 (Captain)  
**Status**: ✅ **ACTIVATION GUIDE COMPLETE**

🐝 **WE. ARE. SWARM. ⚡🔥**

