# 🚀 HOW TO ACTIVATE AGENT MONITORING SYSTEM

**Author:** Agent-3  
**Date:** 2025-01-27  
**Status:** ✅ READY

---

## 🎯 QUICK START

### **Method 1: Discord Command (Easiest)**

```
!monitor start
```

This will:
- ✅ Start Agent Status Monitor (checks every 60 seconds)
- ✅ Start Self-Healing System (checks every 30 seconds)
- ✅ Start Recovery System
- ✅ Run continuously (autonomous)

**Check Status:**
```
!monitor status
```

**Stop:**
```
!monitor stop
```

---

### **Method 2: Command Line**

```bash
python tools/start_monitoring_system.py
```

This starts the orchestrator which includes:
- Agent Status Monitor
- Self-Healing System
- Recovery System
- All running autonomously

**To run in background (Windows):**
```powershell
start /B python tools/start_monitoring_system.py
```

**To run in background (Linux/Mac):**
```bash
python tools/start_monitoring_system.py &
```

---

## 📋 WHAT GETS ACTIVATED

When you start monitoring, these systems activate:

### **1. Agent Status Monitor**
- **Checks:** Every 60 seconds
- **Detects:** Stalled agents (5+ minutes inactive)
- **Tracks:** Agent activity, task completion, health status
- **Location:** `src/orchestrators/overnight/monitor.py`

### **2. Self-Healing System**
- **Checks:** Every 30 seconds
- **Detects:** Stalled agents (2+ minutes)
- **Actions:**
  - 5 minutes: Cancel terminal (SHIFT+BACKSPACE)
  - 8 minutes: Rescue message + Clear tasks + Reset
  - 10 minutes: Hard onboard
- **Location:** `src/core/agent_self_healing_system.py`

### **3. Recovery System**
- **Handles:** Complex recovery scenarios
- **Sends:** Discord alerts for stalled agents
- **Reassigns:** Failed tasks
- **Location:** `src/orchestrators/overnight/recovery.py`

---

## 🔍 VERIFY IT'S RUNNING

### **Discord:**
```
!monitor status
```

### **Command Line:**
```bash
# Check for running process
# Windows:
tasklist | findstr python

# Linux/Mac:
ps aux | grep start_monitoring_system
```

### **Check Agent Status:**
```
!heal status
```

Or:
```bash
python tools/heal_stalled_agents.py --check-now
```

---

## ⚙️ CONFIGURATION

The system uses `config/orchestration.yml`:

```yaml
overnight:
  enabled: true
  max_cycles: 0              # 0 = infinite (never stops)
  auto_restart: true
  
  monitoring:
    check_interval: 60      # Check every 60 seconds
    stall_timeout: 300       # 5 minutes = stalled
    
  self_healing:
    enabled: true
    check_interval: 30       # Check every 30 seconds
    stall_threshold: 120     # 2 minutes = stalled
```

---

## 🎮 DISCORD COMMANDS

| Command | Description |
|---------|-------------|
| `!monitor start` | Start monitoring system |
| `!monitor stop` | Stop monitoring system |
| `!monitor status` | Check if running |
| `!monitor restart` | Restart monitoring |
| `!heal status` | Show healing statistics |
| `!heal check` | Immediately heal stalled agents |

---

## 🚨 TROUBLESHOOTING

### **Monitoring Not Starting?**

1. **Check Configuration:**
   ```yaml
   # config/orchestration.yml
   overnight:
     enabled: true  # Must be true
   ```

2. **Check Logs:**
   - Look for errors in console output
   - Check for import errors

3. **Manual Start:**
   ```python
   from src.orchestrators.overnight.orchestrator import OvernightOrchestrator
   import asyncio
   
   orchestrator = OvernightOrchestrator()
   asyncio.run(orchestrator.start())
   ```

### **Monitoring Stops After Some Time?**

- Check for crashes in logs
- Verify `auto_restart: true` in config
- Use `!monitor status` to check

### **Agents Not Being Detected?**

- Verify `max_cycles: 0` (infinite)
- Check `check_interval` is reasonable (60 seconds)
- Verify agent workspaces exist

---

## ✅ SUMMARY

**To Activate Monitoring:**

1. **Easiest:** `!monitor start` in Discord
2. **Command Line:** `python tools/start_monitoring_system.py`
3. **Programmatic:** Import and call `orchestrator.start()`

**What Runs:**
- ✅ Agent Status Monitor (60s checks)
- ✅ Self-Healing System (30s checks)
- ✅ Recovery System
- ✅ Continuous autonomous operation

**Result:** Agents are monitored 24/7 and automatically healed when stalled!

---

**🎯 READY TO ACTIVATE:** Use `!monitor start` in Discord or run the startup script!

